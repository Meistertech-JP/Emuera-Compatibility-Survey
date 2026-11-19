"""Pure-expression plan, fixture and comparison logic derived from the v3 runner."""
import hashlib
import json
import re
import validator

read_json = validator.read
PLAN_PINS = set()
PURE = set("ABS MIN MAX LIMIT INRANGE LOG LOG10 STRCOUNT REPLACE ESCAPE TOSTR STRFIND STRFINDU".split())
TOKEN = re.compile(r'"[^"\\\x00-\x1f]*"|RESULT:[01](?!\d)|[A-Z][A-Z0-9_]*|[0-9]+|==|!=|<=|>=|[+*%/<>()?,# -]')
CASE_ID = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.-]{0,90}")
SENTINELS = [("result0", "numeric"), ("result1", "numeric"), ("results", "string")]

def digest(value):
    data = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def validate_expression(expr, typed_key):
    if not isinstance(expr, str) or len(expr) > 512 or any(ord(c) < 32 for c in expr):
        raise ValueError("expression must be a bounded single line")
    pos = 0
    tokens = []
    while pos < len(expr):
        match = TOKEN.match(expr, pos)
        if not match:
            raise ValueError(f"invalid expression token near {expr[pos:]!r}")
        token = match[0]
        if token != " ":
            tokens.append(token)
        pos = match.end()
    if len(tokens) < 3 or tokens[0] not in PURE or tokens[1] != "(" or tokens[-1] != ")":
        raise ValueError(f"not an approved pure function call: {expr}")
    if typed_key != "expression_function:" + tokens[0]:
        raise ValueError(f"typed_key does not match {tokens[0]}")
    depth = 0
    for i, token in enumerate(tokens):
        if token == "(":
            depth += 1
        elif token == ")":
            depth -= 1
            if depth < 0 or (depth == 0 and i != len(tokens)-1):
                raise ValueError("unbalanced expression")
        elif token[0].isalpha() and token not in ("RESULT:0", "RESULT:1", "RESULTS"):
            if token not in PURE or tokens[i+1:i+2] != ["("]:
                raise ValueError(f"unapproved identifier: {token}")
    if depth:
        raise ValueError("unbalanced expression")


def load_plan(path, selected=()):
    data = read_json(path)
    if isinstance(data, list) and validator.sha(path) in PLAN_PINS:
        rows = data
        approved = {r["expression"] for r in rows}
    elif isinstance(data, dict) and data.get("schema") == "pyemuera.batch-plan.v1":
        rows = data["cases"]
        approved = set(data["approved_pure_expressions"])
    else:
        raise ValueError("use the pinned classification plans or pyemuera.batch-plan.v1")
    if not isinstance(rows, list) or not 1 <= len(rows) <= 100:
        raise ValueError("plan must provide 1–100 cases")
    cases = []
    ids = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) - {"case_id", "typed_key", "expression", "scope",
                                                    "observations", "expected_optional"}:
            raise ValueError("invalid case fields (setup/helpers are outside batch scope)")
        ident, key, scope = row["case_id"], row["typed_key"], row["scope"]
        if not isinstance(ident, str) or not CASE_ID.fullmatch(ident) or ident in ids:
            raise ValueError(f"invalid or duplicate case_id: {ident!r}")
        if not isinstance(scope, (dict, str)) or not scope:
            raise ValueError(f"missing scope: {ident}")
        ids.add(ident)
        expressions = row["expression"]
        if isinstance(expressions, str):
            expressions = [expressions]
        if not isinstance(expressions, list) or not 1 <= len(expressions) <= 4:
            raise ValueError(f"invalid expressions: {ident}")
        for expr in expressions:
            validate_expression(expr, key)
            if expr not in approved:
                raise ValueError(f"expression not on explicit allowlist: {expr}")
        obs = row.get("observations")
        if obs is None and isinstance(scope, dict):
            typ = scope.get("value_type")
            obs = [{"name": "value", "type": "numeric" if typ == "int64" else typ}]
        if not isinstance(obs, list) or len(obs) != len(expressions):
            raise ValueError(f"provide one typed observation per expression: {ident}")
        names = set()
        for item in obs:
            name = item["name"]
            if (set(item) != {"name", "type"} or item["type"] not in ("numeric", "string")
                    or not re.fullmatch(r"[a-z][a-z0-9_]{0,30}", name) or name in names
                    or name in {k for k, _ in SENTINELS}
                    or re.fullmatch(r"e\d+_(?:result0|result1|results)", name)):
                raise ValueError(f"invalid observation: {item}")
            names.add(name)
        expected = row.get("expected_optional")
        if expected is not None and (not isinstance(expected, list) or len(expected) != len(obs)
                                     or not all(isinstance(v, str) for v in expected)):
            raise ValueError("expected_optional must contain one exact text value per expression")
        cases.append(dict(row, expression=expressions, observations=obs, expected_optional=expected))
    if set(selected) - ids or len(set(selected)) != len(selected):
        raise ValueError(f"unknown or duplicate --case; unknown: {set(selected)-ids}")
    return [r for r in cases if not selected or r["case_id"] in selected]


def fields(case):
    result = []
    for i, item in enumerate(case["observations"]):
        prefix = f"e{i}_" if len(case["observations"]) > 1 else ""
        result += [(item["name"], item["type"], f"ZZAV{i}" if item["type"] == "numeric" else f"ZZAS{i}")]
        result += [(prefix+n, t, f"ZZAR{i}{j}") for j, (n, t) in enumerate(SENTINELS)]
    return result


def marker(case):
    return "ZZBATCH_" + case["case_id"]


def fixture(cases):
    lines = ["@SYSTEM_TITLE"]
    declarations = {}
    for row in cases:
        for _, typ, var in fields(row):
            declarations[var] = "#DIM " if typ == "numeric" else "#DIMS "
    lines += [decl + var for var, decl in declarations.items()]
    for row in cases:
        for i, (expr, obs) in enumerate(zip(row["expression"], row["observations"])):
            target = f"ZZAV{i}=" if obs["type"] == "numeric" else f"ZZAS{i} '= "
            lines += ["RESULT:0=701", "RESULT:1=702", "RESULTS '= \"AUTO_SENT\"",
                      target + expr, f"ZZAR{i}0=RESULT:0", f"ZZAR{i}1=RESULT:1",
                      f"ZZAR{i}2 '= RESULTS"]
        tag = marker(row)
        lines.append("PRINTL " + tag + "_BEGIN")
        for name, typ, var in fields(row):
            interpolation = "{" + var + "}" if typ == "numeric" else "%" + var + "%"
            lines.append(f"PRINTFORML {tag}_OBS_{name}=[{interpolation}]")
        lines.append("PRINTL " + tag + "_END")
    lines += ["PRINTL ZZBATCH_DONE", "OUTPUTLOG", "QUIT"]
    return ("\r\n".join(lines) + "\r\n").encode("cp932", errors="strict")


def decode_log(raw, side):
    if raw.startswith((b"\xff\xfe\x00\x00", b"\x00\x00\xfe\xff")):
        raise UnicodeError("UTF-32 is outside the recorded OUTPUTLOG contract")
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        codec, rule = "utf-16", "utf16_bom"
    elif raw.startswith(b"\xef\xbb\xbf"):
        codec, rule = "utf-8-sig", "utf8_bom"
    else:
        codec, rule = {"native": ("cp932", "native_no_bom_cp932"),
                       "py": ("utf-8", "py_no_bom_utf8")}[side]
    return raw.decode(codec, errors="strict"), {"encoding": codec, "rule": rule, "errors": "strict"}


def parse_log(text, cases):
    lines = text.replace("\r\n", "\n").split("\n")
    out = {}
    last = -1
    for case in cases:
        ident, tag = case["case_id"], marker(case)
        starts = [i for i, line in enumerate(lines) if line == tag+"_BEGIN"]
        ends = [i for i, line in enumerate(lines) if line == tag+"_END"]
        if len(starts) > 1 or len(ends) > 1:
            out[ident] = {"status": "failure", "reason": "duplicate_marker"}
        elif not starts or not ends:
            out[ident] = {"status": "missing", "reason": "missing_marker"}
        elif not last < starts[0] < ends[0]:
            out[ident] = {"status": "failure", "reason": "marker_order"}
        else:
            first, end = starts[0], ends[0]
            last = end
            block = lines[first+1:end]
            spec = fields(case)
            values = {}
            for (name, typ, _), line in zip(spec, block):
                prefix = f"{tag}_OBS_{name}=["
                if not line.startswith(prefix) or not line.endswith("]"):
                    break
                value = line[len(prefix):-1]
                if typ == "numeric" and (not re.fullmatch(r"0|-?[1-9][0-9]{0,18}", value)
                        or not -(2**63) <= int(value) < 2**63):
                    break
                values[name] = value
            if len(spec) != len(block) or len(values) != len(spec):
                out[ident] = {"status": "failure", "reason": "malformed_observations"}
            else:
                out[ident] = {"status": "observed", "observations": values}
    return out


def compare(a, b, expected=None):
    if "failure" in (a["status"], b["status"]):
        return "failure"
    if a["status"] != "observed" or b["status"] != "observed":
        return "missing"
    if a["observations"] != b["observations"]:
        return "different"
    if expected and any(a["observations"].get(k) != v for k, v in expected.items()):
        return "different"
    return "matched_scoped"


def parse_complete(text, cases):
    """Require the final marker and reject unexpected batch markers."""
    lines = text.replace("\r\n", "\n").split("\n")
    end = marker(cases[-1]) + "_END"
    actual = [line for line in lines if line.startswith("ZZBATCH_")]
    expected_count = sum(2 + len(fields(case)) for case in cases) + 1
    if (lines.count("ZZBATCH_DONE") != 1 or lines.count(end) != 1
            or lines.index("ZZBATCH_DONE") <= lines.index(end)
            or len(actual) != expected_count or actual[-1:] != ["ZZBATCH_DONE"]):
        return {case["case_id"]: {"status": "failure", "reason": "final_or_unexpected_marker"}
                for case in cases}
    return parse_log(text, cases)


def compare_logs(cases, native_raw, py_raw):
    native_text, native_encoding = decode_log(native_raw, "native")
    py_text, py_encoding = decode_log(py_raw, "py")
    native = parse_complete(native_text, cases)
    public = parse_complete(py_text, cases)
    rows = []
    for case in cases:
        expected = dict(zip((o["name"] for o in case["observations"]), case["expected_optional"] or []))
        for i in range(len(case["observations"])):
            prefix = f"e{i}_" if len(case["observations"]) > 1 else ""
            expected.update({prefix+"result0": "701", prefix+"result1": "702", prefix+"results": "AUTO_SENT"})
        ident = case["case_id"]
        rows.append({"case_id": ident, "typed_key": case["typed_key"], "scope": case["scope"],
                     "native": native[ident], "py": public[ident],
                     "status": compare(native[ident], public[ident], expected)})
    return {"native_decode": native_encoding, "py_decode": py_encoding, "cases": rows}
