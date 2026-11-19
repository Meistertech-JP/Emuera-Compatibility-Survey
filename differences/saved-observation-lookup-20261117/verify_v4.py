#!/usr/bin/env python3
import argparse,hashlib,json,re
from pathlib import Path,PurePosixPath
H=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok: raise ValueError(msg)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def decode_pointer(path):
    need(isinstance(path,str),"JSON Pointer must be a string")
    need(path=="" or path.startswith("/"),"JSON Pointer must be empty or start with slash")
    if path=="": return []
    tokens=path[1:].split("/")
    for token in tokens: need(re.search(r"~(?![01])",token) is None,"invalid JSON Pointer escape")
    return [t.replace("~1","/").replace("~0","~") for t in tokens]
def pointer(obj,path):
    cur=obj
    for token in decode_pointer(path):
        if isinstance(cur,list):
            need(re.fullmatch(r"0|[1-9][0-9]*",token) is not None,"noncanonical array index in JSON Pointer")
            i=int(token);need(i<len(cur),"JSON Pointer array index out of range");cur=cur[i]
        elif isinstance(cur,dict):
            need(token in cur,"JSON Pointer object member missing");cur=cur[token]
        else: raise ValueError("JSON Pointer traverses a scalar")
    return cur
def link_signature(x):
    return {k:x[k] for k in ("target","case_id","original_case_verdict","field","record","role","sharing","scope")}
def target_key(x): return (x["kind"],x["name"])
def verify(candidate,index_pin,profile_pin,dependencies_pin):
    candidate=Path(candidate).resolve();ip=H/"data/p2-index.json";pp=H/"data/p2-profile.json";dp=H/"data/dependencies.json"
    need(sha(ip)==index_pin,"P2 index SHA-256 mismatch");need(sha(pp)==profile_pin,"public profile SHA-256 mismatch");need(sha(dp)==dependencies_pin,"dependency contract SHA-256 mismatch")
    ix=read(ip);profile=read(pp);deps=read(dp)
    need(ix.get("schema")=="p2-limited-search-index-v2","index schema mismatch")
    need(profile.get("schema")=="p2-public-observation-profile-v4","profile schema mismatch")
    need(deps.get("schema")=="p2-explicit-dependencies-v2","dependency schema mismatch")
    need(sha(candidate/"differences/catalog.json")==profile["provenance"]["candidate_base_catalog_sha256"],"base catalog/profile mismatch")
    need(deps["dependencies"].get("differences/catalog.json",{}).get("sha256")==profile["provenance"]["candidate_base_catalog_sha256"],"base catalog dependency/profile mismatch")
    for rel,pin in deps["dependencies"].items():
        pp0=PurePosixPath(rel);need(not pp0.is_absolute() and ".." not in pp0.parts and "\\" not in rel,"unsafe dependency path")
        f=candidate.joinpath(*pp0.parts);need(f.is_file() and not f.is_symlink(),"required dependency missing or symlink: "+rel)
        cur=candidate
        for part in pp0.parts:
            cur=cur/part;need(not cur.is_symlink(),"symlink in dependency path: "+rel)
        need(f.stat().st_size==pin["bytes"] and sha(f)==pin["sha256"],"candidate dependency changed: "+rel)
    expected_targets=profile["targets"]; actual_targets=ix.get("navigation",{}).get("targets")
    need(isinstance(actual_targets,list),"navigation targets missing")
    def canonical_targets(a):return sorted((json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":")) for x in a))
    need(len(expected_targets)==129 and len(actual_targets)==129,"P2 target population mismatch")
    exp_keys=[(x["target"]["kind"],x["target"]["name"]) for x in expected_targets]
    got_keys=[(x["target"]["kind"],x["target"]["name"]) for x in actual_targets]
    need(len(set(exp_keys))==129,"original profile contains duplicate target")
    need(len(set(got_keys))==129,"navigation contains duplicate or missing target")
    need(set(got_keys)==set(exp_keys),"navigation target set differs from independent profile")
    need(canonical_targets(actual_targets)==canonical_targets(expected_targets),"navigation states/counts/caveats differ from independent profile")
    expected_links=profile["links"]; rows=[]
    for item in ix.get("links",[]):
        need(set(item)=={"target","case_id","original_case_verdict","field","record","role","sharing","scope"},"index link has missing or extra fields")
        rows.append(link_signature(item))
    need(len(rows)==1842 and len(expected_links)==1842,"P2 link population mismatch")
    sig=lambda x:json.dumps(link_signature(x),ensure_ascii=False,sort_keys=True,separators=(",",":"))
    expected=[sig(x) for x in expected_links];actual=[sig(x) for x in rows]
    need(len(set(expected))==1842,"independent profile has duplicate field links")
    need(len(set(actual))==1842,"index has duplicate field links")
    need(set(actual)==set(expected),"index field/case/typed-role/pointer set differs from independent profile")
    index_by_sig={sig(x):x for x in ix["links"]}
    pins={k:v for k,v in deps["dependencies"].items() if k!="differences/catalog.json"}; docs={};catalog=read(candidate/"differences/catalog.json")
    cases={x["case_id"]:x for x in catalog["main_scenarios"]}
    for expected_link in expected_links:
        l=index_by_sig.get(sig(expected_link));need(l is not None,"profile-linked index row disappeared")
        need(l["original_case_verdict"]=="different_scoped","case verdict changed")
        case=cases.get(l["case_id"]);need(case is not None,"linked case not in base catalog")
        need(l["target"] in case["targets"] and case["verdict"]==l["original_case_verdict"],"base catalog case/target/verdict mismatch")
        rec=l["record"];role=l["role"];rel=rec["path"]
        need(rel in pins,"record path is outside pinned dependency set")
        need(rec["path"]==role["path"] and rec["line_1based"]==role["line_1based"],"field and role source differ")
        pin=pins[rel];need(rec["sha256"]==pin["sha256"]==role["sha256"],"source SHA/profile mismatch")
        need(l["field"]==expected_link["field"],"field/profile mismatch")
        if rel not in docs:
            f=candidate.joinpath(*PurePosixPath(rel).parts)
            if f.suffix==".jsonl": docs[rel]=[json.loads(line) for line in f.read_text(encoding="utf-8").splitlines()]
            else: docs[rel]=read(f)
        all_doc=docs[rel];line=rec["line_1based"]
        if line is None:
            need(PurePosixPath(rel).suffix==".json","line-less source must be JSON")
            d=all_doc
        else:
            need(type(line) is int and line>0 and PurePosixPath(rel).suffix==".jsonl","line source must be positive JSONL row")
            need(line<=len(all_doc),"JSONL line outside file");d=all_doc[line-1]
        actual_value=pointer(d,rec["pointer"]);need(actual_value==expected_link["value"],"record value differs from original mapping profile")
        need(pointer(d,role["pointer"])==l["target"],"typed role pointer does not resolve")
        parts=decode_pointer(rec["pointer"])
        if line is not None: case_obj=d
        else:
            need(len(parts)>=2 and parts[0]=="cases","JSON document pointer lacks case container")
            case_obj=pointer(d,"/"+"/".join(str(x).replace("~","~0").replace("/","~1") for x in parts[:2]))
        need(case_obj.get("case_id")==l["case_id"],"record field belongs to different case")
    return {"status":"PASS","typed_targets":129,"targets_with_case_fields":83,"shared_batch_only_targets":46,"field_links":1842,"verified_repository_dependencies":len(deps["dependencies"]),"profile_match":"EXACT","pointer_and_case_binding":"PASS"}
def main():
    a=argparse.ArgumentParser();a.add_argument("--candidate-root","--repository-root",dest="candidate_root",required=True);a.add_argument("--index-sha256",required=True);a.add_argument("--profile-sha256",required=True);a.add_argument("--dependencies-sha256",required=True);x=a.parse_args()
    print(json.dumps(verify(x.candidate_root,x.index_sha256,x.profile_sha256,x.dependencies_sha256),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
