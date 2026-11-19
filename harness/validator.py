"""Strict v3 evidence envelopes. A seal does not establish semantic correctness."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import math
import os
import re
import sys

EXCLUDED = {"MANIFEST.json", "SEAL.json", "VALIDATION.json"}
MANIFEST = "pyemuera-evidence-manifest-v3"
SEAL = "pyemuera-evidence-seal-v3"


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for data in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(data)
    return h.hexdigest()


def loads(text):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError("duplicate JSON key: " + key)
            out[key] = value
        return out
    def number(value):
        n = float(value)
        if not math.isfinite(n):
            raise ValueError("nonfinite JSON number")
        return n
    return json.loads(text, object_pairs_hook=pairs, parse_float=number,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError("nonfinite JSON: "+value)))


def read(path):
    return loads(Path(path).read_text(encoding="utf-8-sig"))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+"\n",
                          encoding="utf-8")


def safe_member(name):
    p = PurePosixPath(name)
    if (not isinstance(name, str) or not name or p.is_absolute() or ".." in p.parts
            or "\\" in name or ":" in name or p.as_posix() != name or name == "."):
        raise ValueError("unsafe member: " + str(name))
    return name


def inventory(root):
    root = Path(root).absolute()
    if root.is_symlink():
        raise ValueError("symlink root")
    files = []
    for p in sorted(root.rglob("*")):
        name = p.relative_to(root).as_posix()
        safe_member(name)
        if p.is_symlink() or not p.resolve().is_relative_to(root.resolve()):
            raise ValueError("nonlocal member: " + name)
        if p.is_file() and name not in EXCLUDED:
            files.append({"path": name, "size": p.stat().st_size, "sha256": sha(p)})
    return files


def hash_text(value):
    if not isinstance(value, str) or not re.fullmatch("[0-9a-f]{64}", value):
        raise ValueError("invalid sha256")
    return value


def canonical_external(root, rows):
    if not isinstance(rows, list):
        raise ValueError("external_inputs must be a list")
    seen, normalized = set(), []
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "sha256"} or not isinstance(row["path"], str):
            raise ValueError("invalid external input record")
        path = (Path(root)/row["path"]).resolve()
        key = os.path.normcase(str(path))
        if key in seen:
            raise ValueError("duplicate external input: " + key)
        seen.add(key)
        normalized.append({"path": str(path), "sha256": hash_text(row["sha256"])})
    return sorted(normalized, key=lambda x: os.path.normcase(x["path"]))


def external_records(root, pins):
    out = []
    for path, hashed in sorted(pins.items(), key=lambda x: os.path.normcase(x[0])):
        try:
            name = Path(os.path.relpath(path, root)).as_posix()
        except ValueError:
            name = str(Path(path).resolve())
        out.append({"path": name, "sha256": hashed})
    canonical_external(root, out)
    return out


def seal(root, external_inputs=None):
    root = Path(root)
    if (root/"MANIFEST.json").exists() or (root/"SEAL.json").exists():
        raise ValueError("refuse resealing")
    external = external_inputs or []
    canonical_external(root, external)
    write(root/"MANIFEST.json", {"schema": MANIFEST, "files": inventory(root), "external_inputs": external})
    write(root/"SEAL.json", {"schema": SEAL, "manifest_sha256": sha(root/"MANIFEST.json")})


def validate(root, expected_external=None, legacy=False):
    errors = []
    root = Path(root).absolute()
    try:
        if root.is_symlink():
            raise ValueError("symlink root")
        m, s = read(root/"MANIFEST.json"), read(root/"SEAL.json")
        if (not isinstance(m, dict) or set(m) != {"schema", "files", "external_inputs"}
                or m["schema"] != ("pyemuera-evidence-manifest-v2" if legacy else MANIFEST)):
            raise ValueError("manifest schema/envelope")
        if (not isinstance(s, dict) or set(s) != {"schema", "manifest_sha256"}
                or s["schema"] != ("pyemuera-evidence-seal-v2" if legacy else SEAL)):
            raise ValueError("seal schema/envelope")
        if hash_text(s["manifest_sha256"]) != sha(root/"MANIFEST.json"):
            raise ValueError("seal hash")
        if not isinstance(m["files"], list):
            raise ValueError("files list")
        seen = set()
        for item in m["files"]:
            if (not isinstance(item, dict) or set(item) != {"path", "size", "sha256"}
                    or type(item["size"]) is not int or item["size"] < 0):
                raise ValueError("invalid file record")
            name = safe_member(item["path"])
            if name.casefold() in seen or name in EXCLUDED:
                raise ValueError("duplicate/excluded member")
            seen.add(name.casefold())
            hash_text(item["sha256"])
        if m["files"] != inventory(root):
            raise ValueError("member set/size/hash mismatch")
        actual = canonical_external(root, m["external_inputs"])
        if expected_external is not None and actual != canonical_external(root, expected_external):
            raise ValueError("required external input set/hash mismatch")
        for item in actual:
            if not Path(item["path"]).is_file() or sha(item["path"]) != item["sha256"]:
                raise ValueError("external input mismatch: " + item["path"])
    except (OSError, ValueError, KeyError, TypeError) as e:
        errors.append(str(e))
    return {"schema": "pyemuera-evidence-validation-v3", "valid": not errors,
            "errors": errors, "scope": "strict envelope, exact inventory and supplied required external set; semantic replay separate"}


if __name__ == "__main__":
    result = validate(sys.argv[1])
    print(json.dumps(result))
    raise SystemExit(not result["valid"])
