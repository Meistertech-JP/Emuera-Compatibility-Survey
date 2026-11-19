"""Create or verify a SHA-256 inventory for named, separately staged file trees."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import unicodedata

SCHEMA = 'selected-file-set.v1'
ROOT_NAME = re.compile(r'[a-z][a-z0-9_-]{0,31}\Z')
SHA = re.compile(r'[0-9a-f]{64}\Z')
DEVICE = re.compile(r'(?:CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|COM[1-9]|LPT[1-9])\Z', re.IGNORECASE)
REPARSE = getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400)


class InventoryError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InventoryError(message)


def collision_key(path):
    return unicodedata.normalize('NFC', path).casefold()


def safe_relative(value):
    require(isinstance(value, str) and value, 'empty or non-string path')
    require('\\' not in value and not value.startswith('/') and not value.endswith('/'), 'absolute or noncanonical path')
    for part in value.split('/'):
        require(part not in ('', '.', '..'), 'unsafe path segment')
        require(not part.endswith((' ', '.')), 'trailing dot or space')
        require(not any(ord(c) < 32 or c in '<>:"|?*' for c in part), 'unsafe Windows path character')
        # Windows also treats e.g. "CON .txt" as a device. Check the stem
        # before the first dot, ignoring spaces at the extension boundary.
        stem = unicodedata.normalize('NFKC', part).split('.', 1)[0].rstrip(' ')
        require(not DEVICE.fullmatch(stem), 'reserved Windows device name')
    return value


def is_link(info):
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, 'st_file_attributes', 0) & REPARSE)


def check_path_components(path, allow_missing_leaf=False):
    """Check each original component before resolving aliases and spelling."""
    path = Path(path)
    if sys.platform == 'win32':
        require(not (path.drive and not path.root), 'drive-relative path is ambiguous')
    if not path.is_absolute():
        path = Path.cwd() / path
    parts = path.parts
    current = Path(path.anchor)
    require(current.anchor, 'absolute path required')
    components = [current]
    for part in parts[1:]:
        if part == '..':
            current = current.parent
        else:
            current = current / part
        components.append(current)
    for index, item in enumerate(components):
        try:
            info = item.lstat()
        except FileNotFoundError:
            if allow_missing_leaf and index == len(components)-1:
                continue
            raise InventoryError('missing path component: ' + str(item))
        require(not is_link(info), 'link or reparse point: ' + str(item))
    if allow_missing_leaf and not os.path.lexists(current):
        # Resolve the existing parent to its actual spelling; keep the new leaf.
        return current.parent.resolve(strict=True) / current.name
    return current.resolve(strict=True)


def ancestor_relative(parent, root):
    """Find physical root ancestry without relying on Windows path spelling."""
    parts = []
    current = parent
    while True:
        if os.path.samefile(current, root):
            return tuple(reversed(parts))
        next_parent = current.parent
        if next_parent == current:
            return None
        parts.append(current.name)
        current = next_parent


def canonical_roots(specs):
    require(isinstance(specs, dict) and specs, 'at least one named root is required')
    roots = {}
    for name, value in specs.items():
        require(isinstance(name, str) and ROOT_NAME.fullmatch(name), 'invalid root name')
        require(name not in roots, 'duplicate root name')
        path = check_path_components(value)
        require(path.is_dir(), 'root is not a directory: ' + name)
        roots[name] = path
    values = list(roots.items())
    for i, (name, path) in enumerate(values):
        for other_name, other in values[i+1:]:
            overlap = ancestor_relative(path, other) is not None or ancestor_relative(other, path) is not None
            require(not overlap,
                    f'roots overlap or alias: {name} and {other_name}')
    return roots


def manifest_location(manifest, roots, creating=False):
    path = check_path_components(manifest, allow_missing_leaf=creating)
    if creating:
        require(not os.path.lexists(path), 'manifest already exists')
    else:
        require(path.is_file(), 'manifest is not a regular file')
    found = []
    for name, root in roots.items():
        parts = ancestor_relative(path.parent, root)
        if parts is None:
            continue
        found.append({'root': name, 'path': safe_relative('/'.join((*parts, path.name)))})
    require(len(found) <= 1, 'ambiguous manifest location')
    return path, found[0] if found else None


def file_hash(path, info):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        opened = os.fstat(stream.fileno())
        require(not is_link(opened) and stat.S_ISREG(opened.st_mode), 'not a regular file: ' + str(path))
        require((opened.st_dev, opened.st_ino) == (info.st_dev, info.st_ino), 'file replaced during scan: ' + str(path))
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
        end = os.fstat(stream.fileno())
    after = path.lstat()
    key = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns)
    require(not is_link(after) and key(info) == key(opened) == key(end) == key(after),
            'file changed during scan: ' + str(path))
    return info.st_size, h.hexdigest()


def inventory(roots, location):
    files = []
    for name, root in sorted(roots.items()):
        seen = {}
        def walk(directory, prefix=''):
            with os.scandir(directory) as entries:
                for entry in sorted(entries, key=lambda x: x.name):
                    rel = safe_relative(prefix + entry.name)
                    key = collision_key(rel)
                    require(key not in seen, f'name collision in {name}: {seen.get(key)} / {rel}')
                    if location and location['root'] == name and key == collision_key(location['path']):
                        require(rel == location['path'], 'manifest path collides with another name')
                    seen[key] = rel
                    path = Path(entry.path)
                    # Windows DirEntry.stat may report zero device/inode; lstat
                    # obtains the actual file ID used by fstat on the handle.
                    info = path.lstat()
                    require(not is_link(info), f'link or reparse point: {name}/{rel}')
                    if stat.S_ISDIR(info.st_mode):
                        walk(path, rel+'/')
                    elif stat.S_ISREG(info.st_mode):
                        if location == {'root': name, 'path': rel}:
                            continue
                        size, digest = file_hash(path, info)
                        files.append({'root': name, 'path': rel, 'size': size, 'sha256': digest})
                    else:
                        raise InventoryError(f'non-regular file: {name}/{rel}')
        walk(root)
    return sorted(files, key=lambda r: (r['root'], r['path']))


def strict_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON object key')
            result[key] = value
        return result
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(InventoryError('invalid JSON value: '+x)))


def validate_envelope(data, roots, expected_location, manifest_path):
    require(isinstance(data, dict) and set(data)=={'schema','roots','manifest_location','files'}, 'invalid manifest envelope')
    require(data['schema']==SCHEMA, 'unknown manifest schema')
    require(isinstance(data['roots'], list) and data['roots']==sorted(roots), 'root names differ')
    recorded_location = data['manifest_location']
    if recorded_location != expected_location:
        # An older manifest can contain a differently cased or short spelling.
        # Accept it only if the OS confirms that it names this exact file.
        require(isinstance(recorded_location,dict) and set(recorded_location)=={'root','path'}
                and isinstance(expected_location,dict)
                and recorded_location['root']==expected_location['root'], 'manifest location differs')
        recorded_name = safe_relative(recorded_location['path'])
        try:
            recorded_path = check_path_components(roots[recorded_location['root']]/recorded_name)
        except (OSError, InventoryError) as exc:
            raise InventoryError('manifest location differs or is unsafe') from exc
        require(recorded_path.is_file() and os.path.samefile(recorded_path,manifest_path), 'manifest location differs')
    require(isinstance(data['files'], list), 'files must be a list')
    seen = set()
    prefixes, file_keys, directory_keys = {}, set(), set()
    for item in data['files']:
        require(isinstance(item, dict) and set(item)=={'root','path','size','sha256'}, 'invalid file entry')
        name = item['root']
        require(isinstance(name, str) and name in roots, 'unknown root')
        path = safe_relative(item['path'])
        require(type(item['size']) is int and item['size']>=0, 'invalid size')
        require(isinstance(item['sha256'], str) and SHA.fullmatch(item['sha256']), 'invalid SHA-256')
        require(expected_location != {'root': name, 'path': path}, 'manifest cannot inventory itself')
        key = (name, collision_key(path))
        require(key not in seen, 'duplicate or colliding path')
        seen.add(key)
        parts = path.split('/')
        for i in range(1, len(parts)+1):
            prefix = '/'.join(parts[:i])
            pkey = (name, collision_key(prefix))
            old = prefixes.setdefault(pkey, prefix)
            require(old == prefix, 'component name collision')
            if i == len(parts):
                require(pkey not in directory_keys, 'file/directory collision')
                file_keys.add(pkey)
            else:
                require(pkey not in file_keys, 'file/directory collision')
                directory_keys.add(pkey)
    require(data['files']==sorted(data['files'], key=lambda r: (r['root'],r['path'])), 'entries not sorted')


def create(manifest, root_specs):
    roots = canonical_roots(root_specs)
    path, location = manifest_location(manifest, roots, creating=True)
    entries = inventory(roots, location)
    data = {'schema':SCHEMA, 'roots':sorted(roots), 'manifest_location':location, 'files':entries}
    validate_envelope(data, roots, location, path)
    encoded = (json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode('utf-8')
    # Exclusive create, never overwrite an existing manifest.
    with path.open('xb') as stream:
        stream.write(encoded)
    return len(entries)


def verify(manifest, root_specs):
    roots = canonical_roots(root_specs)
    path, location = manifest_location(manifest, roots)
    before = path.lstat()
    data = strict_json(path)
    validate_envelope(data, roots, location, path)
    current = inventory(roots, location)
    require(current==data['files'], 'file set, size or SHA-256 mismatch')
    after = path.lstat()
    require(not is_link(after) and (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)==
            (after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns), 'manifest changed during verification')
    return len(current)


def parse_root_options(values):
    result = {}
    for item in values:
        require('=' in item, 'root must be NAME=PATH')
        name, path = item.split('=', 1)
        require(ROOT_NAME.fullmatch(name) and path, 'invalid root specification')
        require(name not in result, 'duplicate root name: '+name)
        result[name] = path
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('create','verify'))
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--root', required=True, action='append', metavar='NAME=PATH')
    args = parser.parse_args(argv)
    try:
        roots = parse_root_options(args.root)
        count = create(args.manifest, roots) if args.action=='create' else verify(args.manifest, roots)
        print(f'{args.action}: OK; files={count}; manifest is an integrity record, not publication approval')
        return 0
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as exc:
        print(f'{args.action}: FAIL: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
