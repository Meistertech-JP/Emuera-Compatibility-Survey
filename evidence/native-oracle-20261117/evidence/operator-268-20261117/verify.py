#!/usr/bin/env python3
"""Verify this snapshot against its manifest; does not prove source semantics."""
from pathlib import Path, PurePosixPath
import hashlib,json,sys
root=Path(__file__).resolve().parent
try:
 manifest=json.loads((root/'manifest.json').read_text(encoding='utf8'))
 if manifest['schema']!='opcont268-files-v1':raise ValueError('manifest schema')
 expected={}
 for entry in manifest['files']:
  name=entry['path']; p=PurePosixPath(name)
  if p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name or p.as_posix()!=name or name in expected or name=='manifest.json':raise ValueError('unsafe or duplicate path')
  f=root.joinpath(*p.parts)
  if f.is_symlink() or not f.resolve().is_relative_to(root) or not f.is_file():raise ValueError('missing or unsafe file: '+name)
  b=f.read_bytes()
  if len(b)!=entry['size'] or hashlib.sha256(b).hexdigest()!=entry['sha256']:raise ValueError('size or hash mismatch: '+name)
  expected[name]=True
 actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='manifest.json'}
 if actual!=set(expected):raise ValueError('file set differs')
 d=json.loads((root/'observations.json').read_text(encoding='utf8'));rows=d['cases']
 if len(rows)!=33 or len({r['case_id'] for r in rows})!=33:raise ValueError('case set')
 counts={'matched_scoped':0,'different_scoped':0}
 for r in rows:
  if not r['case_id'].startswith('OPCONT268_') or r['recorded_verdict'] not in counts:raise ValueError('case identity or verdict')
  modes=r['modes']
  if set(modes)!={'native-01','native-02','public-01'} or modes['native-01']!=modes['native-02']:raise ValueError('mode mismatch')
  same=modes['native-01']==modes['public-01']
  if same!=(r['recorded_verdict']=='matched_scoped'):raise ValueError('verdict and selected output disagree')
  counts[r['recorded_verdict']]+=1
 if counts!={'matched_scoped':31,'different_scoped':2}:raise ValueError('verdict count')
 print('PASS: 33 cases, 31 scoped matches, 2 scoped differences; file-set hashes match')
except Exception as e:
 print('FAIL:',str(e),file=sys.stderr);sys.exit(1)
