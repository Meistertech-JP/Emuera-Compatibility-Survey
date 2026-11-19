"""Verify bundled environment inputs and optional engine binaries without executing them."""
from pathlib import Path
import argparse, hashlib, io, json, zipfile

ROOT = Path(__file__).resolve().parent.parent

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def check(path, expected):
    got = digest(path)
    if got != expected:
        raise ValueError('SHA-256 mismatch: ' + path.name)
    return {'file': path.name, 'sha256': got, 'status': 'PASS'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', type=Path, help='optional extracted Emuera executable')
    parser.add_argument('--pyz', type=Path, help='optional public PyEmuera executable archive')
    args = parser.parse_args()
    env = json.loads((ROOT / 'manifests/environment.json').read_text(encoding='utf-8'))
    native, target = env['native'], env['comparison_engine']
    bundle = ROOT / native['notice_bundle']
    config = ROOT / env['harness']['input_template']
    results = [check(bundle, native['notice_bundle_sha256']),
               check(config, env['harness']['input_template_sha256'])]
    with zipfile.ZipFile(bundle) as z:
        expected = {'Emuera1824+v24.zip', 'NOTICE.ja.md', 'NOTICE.en.md'}
        if set(z.namelist()) != expected or len(z.namelist()) != len(expected):
            raise ValueError('Unexpected or duplicate bundle members')
        if z.testzip() is not None:
            raise ValueError('Bundle CRC failure')
        inner = z.read(native['retained_archive'])
        if hashlib.sha256(inner).hexdigest() != native['retained_archive_sha256']:
            raise ValueError('Retained archive SHA-256 mismatch')
        with zipfile.ZipFile(io.BytesIO(inner)) as reference:
            if reference.testzip() is not None:
                raise ValueError('Retained archive CRC failure')
            exe_name = 'Emuera1824+v24/Emuera1824+v24.exe'
            if reference.namelist().count(exe_name) != 1:
                raise ValueError('Expected exactly one reference executable')
            if hashlib.sha256(reference.read(exe_name)).hexdigest() != native['sha256']:
                raise ValueError('Reference executable SHA-256 mismatch')
        for name in ('NOTICE.ja.md', 'NOTICE.en.md'):
            if z.read(name) != (bundle.parent / name).read_bytes():
                raise ValueError('Bundle and standalone notice differ: ' + name)
    results.append({'file': native['retained_archive'], 'status': 'PASS',
                    'sha256': native['retained_archive_sha256']})
    results.append({'file': native['executable'] + ' (inside retained archive)',
                    'status': 'PASS', 'sha256': native['sha256']})
    if args.native:
        results.append(check(args.native, native['sha256']))
    if args.pyz:
        results.append(check(args.pyz, target['sha256']))
    print(json.dumps({'status': 'PASS', 'checks': results,
                      'scope': 'File identity only; not compatibility, license completeness or executable behavior.'}, indent=2))

if __name__ == '__main__':
    main()
