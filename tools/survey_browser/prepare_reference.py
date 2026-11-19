"""Validate and assemble independently authored explanations and translations.

Reads only the public repository. Generates C# source views from the pinned
bundled archive, not from a developer checkout or the network.
"""
import argparse
from collections import Counter
from hashlib import sha256
from html import escape
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
PARTS = ('commands-display','commands-other','functions-1','functions-2','syntax')
TRANSLATIONS = ('commands','functions','syntax')
CHECK_ONLY = False


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines() if line.strip()]


def emit(path, text):
    raw=text.encode('utf-8')
    if CHECK_ONLY:
        assert path.read_bytes()==raw, 'Generated reference is out of date: '+path.name
    else:
        path.write_bytes(raw)


def write_json(path, value):
    emit(path,json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def typed(row):
    return row['kind'], row['name']


def bilingual(value):
    return isinstance(value,dict) and all(isinstance(value.get(k),str) and value[k].strip() for k in ('ja','en'))


def decode(raw):
    for encoding in ('utf-8-sig','cp932'):
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise ValueError('Source encoding could not be decoded without loss')


def native_members(root):
    registry = json.loads((root/'reference/sources.json').read_text(encoding='utf-8-sig'))
    s = next(s for s in registry['sources'] if s['id']=='SRC-NATIVE-V24')['retrieval']
    raw = (root/s['archive']).read_bytes()
    assert sha256(raw).hexdigest()==s['archive_sha256'], 'Native outer archive hash'
    with ZipFile(BytesIO(raw)) as outer:
        inner = outer.read(s['nested_archive_member'])
    assert sha256(inner).hexdigest()==s['nested_archive_sha256'], 'Native inner archive hash'
    with ZipFile(BytesIO(inner)) as archive:
        members = {p:archive.read(p) for p in archive.namelist() if '/Emuera/' in p and p.endswith('.cs')}
    return members, s


def prepare(root):
    ref = root/'reference'
    survey = json.loads((root/'results/survey.json').read_bytes())
    expected = {typed(r) for r in survey['targets']}
    assert len(expected)==694
    entries = [row for part in PARTS for row in read_jsonl(ref/f'entries-{part}.jsonl')]
    keys = [typed(e['typed_key']) for e in entries]
    assert len(keys)==len(set(keys))==694 and set(keys)==expected, 'Target set changed or incomplete'
    original = read_jsonl(root/'evidence/694-target-trace-20261117/requirements/requirements.jsonl')
    originals = {r['requirement_id']:r for r in original}
    translated = [r for part in TRANSLATIONS for r in read_jsonl(ref/f'requirements-ja-{part}.jsonl')]
    ids = [r['requirement_id'] for r in translated]
    assert len(ids)==len(set(ids))==3359 and set(ids)==set(originals), 'Translation ID set'
    for r in translated:
        o = originals[r['requirement_id']]
        assert {k:r[k] for k in o}==o, ('English source/attributes changed',r['requirement_id'])
        assert isinstance(r.get('ja'),str) and r['ja'].strip(), r['requirement_id']
        assert isinstance(r.get('plain_ja'),str) and r['plain_ja'].strip(), r['requirement_id']
        assert sha256(o['verification_requirement'].encode()).hexdigest()==o['derived_text_sha256']
        if o['text_status']=='verbatim':
            assert o['derived_text_sha256']==o['original_text_sha256']
    registry = json.loads((ref/'sources.json').read_text(encoding='utf-8-sig'))
    source_ids = {s['id'] for s in registry['sources']}
    members, archive_info = native_members(root)
    views, locations = {}, []
    for e in entries:
        label = ':'.join(typed(e['typed_key']))
        for field in ('summary','usage','effects','limits'):
            assert bilingual(e[field]), (label,field)
        assert isinstance(e['syntax'],list) and all(isinstance(x,str) and x.strip() for x in e['syntax']), label
        if 'syntax_en' in e:
            assert isinstance(e['syntax_en'],list) and len(e['syntax_en'])==len(e['syntax'])
            assert all(isinstance(x,str) and x.strip() for x in e['syntax_en']),label
        assert e['syntax'] or any('syntax' in u.get('field','').split('/') for u in e.get('unconfirmed',[])), label
        assert e['sources'] and (e['examples'] or e.get('unconfirmed')), label
        assert all(isinstance(t,dict) and typed(t) in expected for t in e['related']), (label,'Invalid typed relation')
        for p in e['parameters']:
            assert all(p.get(k) for k in ('name','type','ja','en')), (label,'parameter')
        for x in e['examples']:
            assert x.get('erb') and bilingual(x['expected']) and bilingual(x['context']), (label,'example')
            assert x['evidence_class']=='EXAMPLE_DERIVED' and x['source_refs'] and x.get('verification'), label
        for s in e['sources']:
            assert s['source_id'] in source_ids, (label,'Unknown source')
            if s['source_id']!='SRC-NATIVE-V24':
                continue
            path = s['path'].replace('\\','/').removeprefix('src1824/Emuera/').removeprefix('Emuera/')
            assert not PurePosixPath(path).is_absolute() and '..' not in PurePosixPath(path).parts, path
            matches = [m for m in members if m.endswith('/Emuera/'+path)]
            assert len(matches)==1, (label,'Missing/ambiguous source path',path)
            member = matches[0]; raw = members[member]
            content, encoding = decode(raw)
            lines = content.splitlines()
            a, b = s['start_line'], s['end_line']
            assert isinstance(a,int) and isinstance(b,int) and 1<=a<=b<=len(lines), (label,path,a,b,len(lines))
            viewer = 'reference/native-source/'+path.replace('/','__')+'.html'
            s.update(path=path,archive_member=member,member_sha256=sha256(raw).hexdigest(),viewer_path=viewer)
            views[viewer] = (content, encoding, member, s['member_sha256'])
            locations.append({'typed_key':e['typed_key'],'source_id':s['source_id'],'fields':s.get('fields',[]),
                              'path':path,'start_line':a,'end_line':b,'archive_member':member,
                              'member_sha256':s['member_sha256'],'viewer_path':viewer})
        for x in e['examples']:
            for s in x['source_refs']:
                assert s['source_id'] in source_ids, (label,'Example source')
                if s['source_id']=='SRC-NATIVE-V24':
                    path=s['path'].replace('\\','/').removeprefix('src1824/Emuera/').removeprefix('Emuera/')
                    matches=[m for m in members if m.endswith('/Emuera/'+path)]
                    assert len(matches)==1,(label,'Example source path',path)
                    member=matches[0];raw=members[member]
                    content,encoding=decode(raw)
                    assert 1<=s['start_line']<=s['end_line']<=len(content.splitlines()),(label,'Example source range')
                    view='reference/native-source/'+path.replace('/','__')+'.html'
                    s.update(path=path,archive_member=member,member_sha256=sha256(raw).hexdigest(),viewer_path=view)
                    views[view]=(content,encoding,member,s['member_sha256'])
    notes=json.loads((ref/'requirement-notes-input.json').read_text(encoding='utf-8-sig'))
    note_ids=[n['requirement_id'] for n in notes['notes']]
    assert len(note_ids)==len(set(note_ids)) and set(note_ids)<=set(originals), 'Requirement-note IDs'
    for n in notes['notes']:
        assert n['typed_key']==originals[n['requirement_id']]['typed_key'] and bilingual(n)
        for s in n['source_refs']:
            assert s['source_id']=='SRC-NATIVE-V24'
            path=s['path'];matches=[m for m in members if m.endswith('/Emuera/'+path)]
            assert len(matches)==1, path
            member=matches[0];raw=members[member];content,encoding=decode(raw)
            assert 1<=s['start_line']<=s['end_line']<=len(content.splitlines())
            view='reference/native-source/'+path.replace('/','__')+'.html'
            s.update(classification='SOURCE_CONFIRMED',archive_member=member,member_sha256=sha256(raw).hexdigest(),viewer_path=view)
            views[view]=(content,encoding,member,s['member_sha256'])
    write_json(ref/'requirement-notes.json',notes)
    (ref/'native-source').mkdir(exist_ok=True)
    for view,(content,encoding,member,pin) in views.items():
        title = member.split('/Emuera/',1)[1]
        rows = '\n'.join(f'<span id="L{i}"><a href="#L{i}" aria-label="line {i}">{i:5}</a> {escape(line)}</span>'
                         for i,line in enumerate(content.splitlines(),1))
        page = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
                f'<title>{escape(title)} — Emuera1824+v24</title>'
                '<style>body{font:15px system-ui;margin:1.5rem}pre{white-space:pre;overflow:auto;font:14px/1.5 monospace}'
                'pre span{display:block}pre span:target{background:#fff0a6}a{color:#165b90}</style>'
                f'<h1>{escape(title)}</h1><p>Emuera1824+v24 · SOURCE_CONFIRMED · {escape(encoding)}</p>'
                '<p>本家C#ソースの閲覧用表示 / Readable view of the pinned upstream C# source. '
                'Line numbers refer to decoded physical lines. Source comments retain their original language.</p>'
                '<p><a href="../../LICENSES/Emuera1824-v24-license-original.txt">Original source license</a> · '
                '<a href="../../vendor/emuera/NOTICE.en.md">Third-party notices</a> · '
                '<a href="../../vendor/emuera/Emuera1824-v24-with-notices.zip">Unmodified source archive and notices</a></p>'
                f'<p>Archive member: {escape(member)}</p><p>SHA-256 (original member bytes): {pin}</p><pre>{rows}</pre></html>')
        emit(root/view,page)
    write_json(ref/'entries.json',{'schema_version':1,'basis':'Emuera1824+v24; explanations are independent of survey verdicts',
                                  'entries':sorted(entries,key=lambda e:typed(e['typed_key']))})
    emit(ref/'requirements_ja.jsonl',''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in sorted(translated,key=lambda r:r['requirement_id'])))
    write_json(ref/'source-locations.json',{'archive':archive_info['archive'],
        'archive_sha256':archive_info['archive_sha256'],'locations':locations})
    glossary = json.loads((ref/'glossary.json').read_text(encoding='utf-8-sig'))
    body = ''.join('<tr>'+''.join('<td>'+escape(r[k])+'</td>' for k in ('en','ja','explanation_ja','explanation_en'))+'</tr>' for r in glossary['terms'])
    emit(ref/'glossary.html','<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
        '<title>Emuera 用語集 / Glossary</title><style>body{font:16px/1.6 system-ui;margin:2rem}td,th{border:1px solid #aaa;padding:.6rem}table{border-collapse:collapse}</style>'
        '<h1>Emuera 用語集 / Glossary</h1><p><a href="../docs/survey-browser.html">リファレンス / Reference</a></p>'
        '<table><tr><th>English</th><th>日本語</th><th>説明</th><th>Explanation</th></tr>'+body+'</table></html>')
    return {'targets':len(entries),'requirements':len(translated),'original_fields_unchanged':True,
        'requirement_status':dict(Counter(r['text_status'] for r in translated)),
        'examples':sum(len(e['examples']) for e in entries),'source_locations':len(locations),'source_views':len(views),
        'unconfirmed_fields':sum(len(e.get('unconfirmed',[])) for e in entries),
        'original_requirement_notes':len(notes['notes']),
        'target_kinds':dict(Counter(e['typed_key']['kind'] for e in entries))}


def main():
    global CHECK_ONLY
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=ROOT)
    p.add_argument('--check',action='store_true',help='Compare generated bytes without rewriting files')
    args=p.parse_args()
    CHECK_ONLY=args.check
    print(json.dumps(prepare(args.root),ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
