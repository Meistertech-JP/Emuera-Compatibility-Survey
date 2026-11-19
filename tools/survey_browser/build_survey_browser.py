
"""Build the offline survey browser from the publication candidate."""
import argparse
from collections import Counter
import json
import re
from collections import defaultdict
from pathlib import Path
from saved_case_results import collect

HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = HERE.parents[1]
OBSERVATIONS = 'evidence/saved-case-observations/observations.json'
NATIVE = 'evidence/native-oracle-20261117'
RECOVERY = 'evidence/case-observation-recovery-20261117'


def read(path):
    return path.read_text(encoding='utf-8-sig')


def jsonl(path):
    return [json.loads(line) for line in read(path).splitlines()]


def key(target):
    return target['kind'], target['name']


def build(root, frozen_review=None):
    def load(path):
        return json.loads(read(root / path))

    survey = load('results/survey.json')
    locator = load('evidence/legacy226-source-locator-20261118/locator.json')
    restored_path = root/'evidence/legacy226-restored/index.json'
    restored = load('evidence/legacy226-restored/index.json') if restored_path.is_file() else {'files':[]}
    restored_views = {r['public_file']['path']:r['readable_view']['path']
                      for r in restored['files'] if r.get('public_file')}
    trace = root / 'evidence/694-target-trace-20261117/requirements/requirements.jsonl'
    requirements = defaultdict(list)
    reference = load('reference/entries.json')
    descriptions = {key(r['typed_key']): r for r in reference['entries']}
    genres = load('reference/genres.json')
    target_genres = load('reference/target-genres.json')
    genre_ids = {g['id'] for g in genres['genres']}
    genre_by_target = {}
    for row in target_genres['targets']:
        target = key(row['typed_key'])
        if target in genre_by_target:
            raise ValueError('Duplicate genre assignment: ' + repr(target))
        if row['primary'] not in genre_ids:
            raise ValueError('Unknown primary genre: ' + row['primary'])
        if len(set(row['secondary'])) != len(row['secondary']) or any(
                secondary not in genre_ids or secondary == row['primary']
                for secondary in row['secondary']):
            raise ValueError('Invalid secondary genres: ' + repr(target))
        genre_by_target[target] = row
    if set(genre_by_target) != set(descriptions):
        missing = set(descriptions) - set(genre_by_target)
        extra = set(genre_by_target) - set(descriptions)
        raise ValueError('Genre assignments do not match reference targets: '
                        + repr((sorted(missing), sorted(extra))))
    translated = {r['requirement_id']: r for r in jsonl(root / 'reference/requirements_ja.jsonl')}
    aliases = {r['case_alias']:r['case_id'] for r in load(
        'evidence/694-target-trace-20261117/requirements/case-id-crosswalk.json')['mappings']}
    notes = {r['requirement_id']:r for r in load('reference/requirement-notes.json')['notes']}
    for row in jsonl(trace):
        translation = translated[row['requirement_id']]
        if any(translation.get(k) != v for k, v in row.items()):
            raise ValueError('Original requirement changed: ' + row['requirement_id'])
        requirements[key(row['typed_key'])].append({
            'i': row['requirement_id'], 't': row['verification_requirement'],
            'status': row['text_status'],
            'ja': translation['ja'], 'plain': translation['plain_ja'],
            'hash': row['original_text_sha256'], 'derivedHash': row['derived_text_sha256'],
            'roles': row['case_roles'],
            'caseLinks': {r['case']:aliases[r['case']] for r in row['case_roles'] if r['case'] in aliases},
            'note': notes.get(row['requirement_id']),
        })
    evidence = defaultdict(list)
    for row in load('results/evidence-index.json')['entries']:
        for case in {row['case_id'], *row['historical_case_ids']}:
            evidence[key(row['target']), case].append(row)
    targets = []
    for row in survey['targets']:
        typed = key(row)
        genre = genre_by_target[typed]
        links = {}
        for case in row['case_ids']:
            for entry in evidence[typed, case]:
                links[(entry['case_id'], entry['readme_ja'])] = {
                    'c': entry['case_id'], 'j': entry['readme_ja'], 'e': entry['readme_en'],
                }
        targets.append({
            'k': row['kind'], 'n': row['name'], 'o': row['comparison_outcome'],
            'g': genre['primary'], 'sg': genre['secondary'],
            'c': row['case_ids'], 'r': requirements[typed], 'ev': list(links.values()),
            'ref': descriptions[typed],
        })

    old_html = read(root / NATIVE / 'docs/native-oracle.html')
    scripts = re.findall(r'<script(?: [^>]*)?>(.*?)</script>', old_html, re.S)
    original = json.loads(scripts[0])
    # Reuse the selected-observation viewer's translated labels and card rendering.
    start = scripts[1].index('const dict=')
    stop = scripts[1].index('for(const r of rows)')
    native_renderer = scripts[1][start:stop]
    native_renderer = native_renderer.replace(
        "const href=p=>'../'+p.split('/').map(encodeURIComponent).join('/')",
        "const href=p=>evidenceLink('evidence/native-oracle-20261117/'+p)",
    )
    if "const href=p=>evidenceLink(" not in native_renderer:
        raise ValueError('Native viewer link helper changed')

    recovery = []
    sources = (
        ('marker-recovery/current-candidate-corrections.jsonl', 'correction'),
        ('observations.jsonl', 'projection'),
        ('marker-recovery/risk-observations.jsonl', 'supplement'),
    )
    for path, category in sources:
        for row in jsonl(root / RECOVERY / path):
            if category == 'correction':
                fields = row['fields']
            elif category == 'projection':
                fields = {k: row[k] for k in ('recovered', 'recovered_context', 'limitations') if row[k]}
            else:
                fields = {'observations': row['projection']}
            recovery.append({'id': row['case_id'], 'roles': row['targets'], 'v': row['scenario_verdict'],
                             'type': category, 'fields': fields})

    data = {
        'referenceSources': load('reference/sources.json'),
        'glossary': load('reference/glossary.json'),
        'genres': genres['genres'],
        'targets': targets,
        'scenarios': [{'i': row['case_id'], 'v': row['scenario_verdict'],
                       't': row['targets']} for row in survey['main_scenarios']],
        'grammar': survey['grammar_cases'],
        'supplemental': survey['supplemental_items'],
        'supplementalModes': survey['supplemental_modes'],
        'legacy': [{
            'k': row['kind'], 'n': row['name'], 'o': row['row_outcome'],
            's': row['acceptance_schema'], 'g': row['gap_codes'],
            'cp': [{'p': ref['path'], 'sha': ref['sha256'], 'm': ref.get('archive_members', []),
                    'derived': ref.get('derived', []), 'view':restored_views.get(ref['path'])}
                   for ref in row['references'] if ref['classification'] in {'PUBLIC_INCLUDED','PUBLIC_DERIVED'}],
            'classes': dict(Counter(ref['classification'] for ref in row['references'])),
            'withheld': [{'id':ref['id'],'view':ref['readable_view'],'reason':ref['selection_reason_ja']}
                         for ref in row['references'] if ref['classification']=='PRIVATE_RETAINED' and ref.get('readable_view')],
            'op': sum(1 for ref in row['references'] if ref['original_exists']),
        } for row in locator['records']],
        'native': original,
        'recovery': recovery,
        'saved': collect(root, survey, original, recovery),
    }
    if frozen_review is not None:
        wanted = {row['i'] for row in data['scenarios']}
        existing = set(data['saved']['coverage']['mainCaseIds'])
        recovered = [row['id'] for row in frozen_review['records']]
        if len(recovered) != len(set(recovered)) or not set(recovered) <= wanted - existing:
            raise ValueError('Invalid frozen result case mapping')
        if frozen_review['baseline'] != len(existing):
            raise ValueError('Frozen result baseline changed')
        data['frozenResults'] = frozen_review
    # Escape the HTML parser's script delimiters without changing the JSON values.
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', r'\u003c')
    script = read(HERE / 'integrated-viewer.js').replace('/* NATIVE_RENDERER */', native_renderer)
    template = read(HERE / 'integrated-template.html')
    return template.replace('__JS__', script, 1).replace('__DATA__', payload, 1).encode('utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=DEFAULT_ROOT)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    path = args.root / 'docs/survey-browser.html'
    evidence = json.loads(read(args.root / OBSERVATIONS))
    result = build(args.root, evidence)
    if args.check:
        if path.read_bytes() != result:
            parser.exit(1, 'survey browser is out of date\n')
    else:
        staging = path.with_suffix('.html.tmp')
        staging.write_bytes(result)
        staging.replace(path)
    print(f'{path.name}: {len(result):,} bytes')


if __name__ == '__main__':
    main()

