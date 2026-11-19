#!/usr/bin/env python3
import argparse,hashlib,importlib.util,json
from pathlib import Path
H=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument("term");p.add_argument("--kind");p.add_argument("--candidate-root","--repository-root",dest="candidate_root",required=True);p.add_argument("--index-sha256",required=True);p.add_argument("--profile-sha256",required=True);p.add_argument("--dependencies-sha256",required=True);p.add_argument("--verifier-sha256",required=True);a=p.parse_args()
vp=H/"verify_v4.py"
if vp.is_symlink() or not vp.is_file() or vp.resolve().parent!=H:raise ValueError("local verifier path is missing or escapes this stage")
if hashlib.sha256(vp.read_bytes()).hexdigest()!=a.verifier_sha256:raise ValueError("local verifier SHA-256 mismatch")
spec=importlib.util.spec_from_file_location("p2_v4_pinned_local_verifier",vp)
if spec is None or spec.loader is None:raise ImportError("cannot load pinned local verifier")
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
v.verify(a.candidate_root,a.index_sha256,a.profile_sha256,a.dependencies_sha256)
ix=json.loads((H/"data/p2-index.json").read_text(encoding="utf-8"));term=a.term.upper();kind=a.kind.upper() if a.kind else None
bycase={}
for x in ix["links"]:bycase.setdefault(x["case_id"].upper(),[]).append(x)
if term in bycase:
    hits=bycase[term]
    if kind:hits=[x for x in hits if x["target"]["kind"].upper()==kind]
    target_keys={(x["target"]["kind"],x["target"]["name"]) for x in hits}
else:
    name=term;typed=kind
    if ":" in term:
        prefix,name=term.split(":",1)
        if typed and prefix.upper()!=typed:raise ValueError("conflicting typed kind")
        typed=typed or prefix.upper()
    targets=[x for x in ix["navigation"]["targets"] if x["target"]["name"].upper()==name and (typed is None or x["target"]["kind"].upper()==typed)]
    target_keys={(x["target"]["kind"],x["target"]["name"]) for x in targets}
    hits=[x for x in ix["links"] if (x["target"]["kind"],x["target"]["name"]) in target_keys]
if term in bycase:
    targets=[x for x in ix["navigation"]["targets"] if (x["target"]["kind"],x["target"]["name"]) in target_keys]
else:
    targets=[x for x in ix["navigation"]["targets"] if (x["target"]["kind"],x["target"]["name"]) in target_keys]
# Resolve each exact mapped field only; no shared raw stream is promoted into an individual case.
resolved=[];root=Path(a.candidate_root).resolve();cache={}
for x in hits:
    rel=x["record"]["path"]
    if rel not in cache:
        f=root.joinpath(*Path(rel).parts);cache[rel]=[json.loads(y) for y in f.read_text(encoding="utf-8").splitlines()] if f.suffix==".jsonl" else json.loads(f.read_text(encoding="utf-8"))
    rows=cache[rel];line=x["record"]["line_1based"];doc=rows[line-1] if line is not None else rows
    value=v.pointer(doc,x["record"]["pointer"])
    toks=v.decode_pointer(x["record"]["pointer"])
    if line is None:case_obj=v.pointer(doc,"/"+"/".join(t.replace("~","~0").replace("/","~1") for t in toks[:2]))
    else:case_obj=doc
    resolved.append({"target":x["target"],"case_id":x["case_id"],"original_case_verdict":x["original_case_verdict"],"field":x["field"],"recorded_field_value":value,"repository_relative_path":rel,"line_1based":line,"json_pointer":x["record"]["pointer"],"typed_role_pointer":x["role"]["pointer"],"sharing":x["sharing"],"case_scope":{"recorded_verdict":case_obj.get("recorded_verdict"),"verdict_scope":case_obj.get("verdict_scope"),"unobserved":case_obj.get("unobserved")},"scope":"This is a recorded field from the pinned research repository. It does not prove complete engine coverage or independent execution."})
print(json.dumps({"scope":"Limited saved-observation lookup","term":a.term,"status":"TARGETS_FOUND" if targets else "NO_MATCH_IN_INCLUDED_LOOKUP","field_link_count":len(resolved),"targets":[{"target":x["target"],"state":x["state"],"linked_field_count":x["linked_field_count"],"caveat":x["caveat"]} for x in targets],"observations":resolved,"required_repository_files":"VERIFIED","values_are":"resolved from pinned candidate JSON/JSONL field pointers"},ensure_ascii=False,indent=2))
