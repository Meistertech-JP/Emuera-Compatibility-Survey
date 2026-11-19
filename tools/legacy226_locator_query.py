"""Read the legacy-226 source locator. It does not replay or alter verdicts."""
import json
from collections import Counter
from pathlib import Path

LOCATOR = 'evidence/legacy226-source-locator-20261118/locator.json'
READMES = ('README.ja.md', 'README.md')
_CACHE = {}


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def _load(root):
    root = Path(root).resolve()
    cached = _CACHE.get(root)
    if cached is not None:
        return cached
    directory = root / 'evidence' / 'legacy226-source-locator-20261118'
    path = directory / 'locator.json'
    if not path.is_file():
        data = None
    else:
        for name in READMES:
            if not (directory / name).is_file():
                raise ValueError('legacy226 locator explanation is incomplete')
        data = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=_pairs)
        if data.get('schema') not in {'legacy226-source-locator.v2','legacy226-source-locator.v3'} or data.get('rows') != 226:
            raise ValueError('legacy226 locator schema mismatch')
        records = data.get('records')
        if not isinstance(records, list) or len(records) != 226:
            raise ValueError('legacy226 locator does not contain 226 records')
        index = {}
        for row in records:
            key = (row.get('kind'), str(row.get('name', '')).casefold())
            if key in index:
                raise ValueError('legacy226 target is duplicated')
            index[key] = row
        data = {'index': index}
    _CACHE[root] = data
    return data


def _project(row):
    references = row.get('references') or []
    views = {}
    for ref in references:
        if ref.get('readable_view'):
            entry = views.setdefault(ref['review_file_id'],{
                'source_file_id':ref['review_file_id'],'view':ref['readable_view'],
                'classification':ref['classification'],'reference_ids':[]})
            entry['reference_ids'].append(ref['id'])
    return {
        'schema': 'legacy226-source-locator-query.v2',
        'kind': row.get('kind'),
        'name': row.get('name'),
        'row_outcome': row.get('row_outcome'),
        'acceptance_schema': row.get('acceptance_schema'),
        'gap_codes': row.get('gap_codes'),
        'reference_count': len(references),
        'original_present': sum(bool(item.get('original_exists')) for item in references),
        'candidate_present': sum(bool(item.get('candidate_exists')) for item in references),
        'reference_class_counts': dict(Counter(item['classification'] for item in references)),
        'individually_reviewed_artifacts':list(views.values()),
        'recorded_sha_checked': sum('recorded_sha_matches' in item for item in references),
        'recorded_sha_matched': sum(bool(item.get('recorded_sha_matches')) for item in references),
        'independent_reproduction': 'not_established_from_candidate_alone',
        'locator': LOCATOR,
    }


def lookup(root, kind, name):
    """Return one typed target, or None when the locator is not installed."""
    data = _load(root)
    if data is None:
        return None
    row = data["index"].get((kind, name.casefold()))
    if row is None:
        raise ValueError('legacy226 target is missing or ambiguous')
    return _project(row)


def lookup_name(root, name):
    """Return every typed kind for one name. Empty means not installed."""
    data = _load(root)
    if data is None:
        return []
    wanted = name.casefold()
    rows = [row for (row_kind, row_name), row in data["index"].items() if row_name == wanted]
    return [_project(row) for row in sorted(rows, key=lambda item: (item.get("kind") or "", item.get("name") or ""))]
