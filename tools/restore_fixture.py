"""Restore the recorded ERB/CSV/configuration layout into a new working folder."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

from file_set_manifest import safe_relative, check_path_components

ROOT=Path(__file__).resolve().parents[1]
INDEX='evidence/legacy226-restored/fixture-layouts.json'


def restore(source_file_id, layout_index, destination):
    document=json.loads((ROOT/INDEX).read_bytes())
    matches=[r for r in document['layouts'] if r['source_file_id']==source_file_id and r['layout_index']==layout_index]
    if len(matches)!=1:
        raise ValueError('Unknown or ambiguous recorded fixture layout')
    layout=matches[0]
    pending=[]
    for row in layout['files']:
        target=safe_relative(row['restore_path'])
        original=ROOT/safe_relative(row['path'])
        if not original.resolve().is_relative_to(ROOT):
            raise ValueError('Source escapes the package')
        raw=original.read_bytes()
        if len(raw)!=row['size'] or sha256(raw).hexdigest()!=row['sha256']:
            raise ValueError('Recorded fixture content changed')
        pending.append((target,raw))
    if len({name.casefold() for name,raw in pending})!=len(pending):
        raise ValueError('Duplicate fixture destination')
    destination=Path(destination).absolute()
    check_path_components(destination,allow_missing_leaf=True)
    destination.mkdir(exist_ok=False)
    for name,raw in pending:
        file=destination/name
        file.parent.mkdir(parents=True,exist_ok=True)
        file.write_bytes(raw)
    if layout['csv_directory_required'] and not any(name.split('/')[0].casefold()=='csv' for name,raw in pending):
        (destination/'csv').mkdir(exist_ok=True)
    return {'source_file_id':source_file_id,'layout_index':layout_index,'files':len(pending),
            'configuration_status':layout['configuration_status'],
            'meaning':'Recorded input bytes restored. No engine was executed.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_file_id')
    parser.add_argument('--layout',type=int,default=0)
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args()
    try:
        print(json.dumps(restore(args.source_file_id,args.layout,args.out),ensure_ascii=False))
    except (OSError,ValueError,KeyError) as exc:
        raise SystemExit(f'FAIL: {type(exc).__name__}: {exc}') from None


if __name__=='__main__':
    main()
