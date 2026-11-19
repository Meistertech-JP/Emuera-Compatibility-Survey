"""Public-data checks for the bilingual reference and its offline generator."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/survey_browser'))
from prepare_reference import native_members, decode


def rows(path):
    return [json.loads(s) for s in (ROOT/path).read_text(encoding='utf-8-sig').splitlines() if s.strip()]


class ReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries=json.loads((ROOT/'reference/entries.json').read_bytes())['entries']
        cls.requirements=rows('reference/requirements_ja.jsonl')
        cls.original=rows('evidence/694-target-trace-20261117/requirements/requirements.jsonl')
        cls.survey=json.loads((ROOT/'results/survey.json').read_bytes())
        cls.sources=json.loads((ROOT/'reference/sources.json').read_bytes())
        cls.html=(ROOT/'docs/survey-browser.html').read_text(encoding='utf-8')
        cls.data=json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',cls.html,re.S)[1])

    def test_target_identity(self):
        keys=lambda seq:[(r['typed_key']['kind'],r['typed_key']['name']) for r in seq]
        original={(r['kind'],r['name']) for r in self.survey['targets']}
        self.assertEqual(len(self.entries),694)
        self.assertEqual(len(set(keys(self.entries))),694)
        self.assertEqual(set(keys(self.entries)),original)

    def test_english_and_all_provenance_attributes_unchanged(self):
        original={r['requirement_id']:r for r in self.original}
        self.assertEqual(len(self.requirements),3359)
        self.assertEqual(len({r['requirement_id'] for r in self.requirements}),3359)
        self.assertEqual({r['requirement_id'] for r in self.requirements},set(original))
        for r in self.requirements:
            with self.subTest(requirement=r['requirement_id']):
                self.assertEqual({k:r[k] for k in original[r['requirement_id']]},original[r['requirement_id']])
                self.assertTrue(r['ja'].strip())
                self.assertTrue(r['plain_ja'].strip())
                self.assertNotEqual(r['ja'],r['verification_requirement'])
                self.assertRegex(r['ja'],r'[ぁ-んァ-ン一-龯]')
                self.assertEqual(sha256(r['verification_requirement'].encode()).hexdigest(),r['derived_text_sha256'])
        self.assertEqual(Counter(r['text_status'] for r in self.requirements),{'verbatim':3278,'neutralized':81})

    def test_each_explanation_has_bilingual_content_and_specific_sources(self):
        ids={s['id'] for s in self.sources['sources']}
        for e in self.entries:
            with self.subTest(target=e['typed_key']):
                for field in ('summary','usage','effects','limits'):
                    for lang in ('ja','en'): self.assertTrue(e[field][lang].strip(),field)
                self.assertTrue(e['syntax'] or any('syntax' in u.get('field','').split('/') for u in e.get('unconfirmed',[])))
                self.assertTrue(e['sources'])
                english_syntax=e.get('syntax_en',e['syntax'])
                self.assertEqual(len(english_syntax),len(e['syntax']))
                self.assertNotRegex(' '.join(english_syntax),r'[ぁ-んァ-ン一-龯]','English syntax still contains Japanese metanotation')
                self.assertTrue(all(isinstance(t,dict) and (t['kind'],t['name']) in
                    {(x['kind'],x['name']) for x in self.survey['targets']} for t in e['related']))
                self.assertTrue(e['examples'] or e.get('unconfirmed'))
                for s in e['sources']: self.assertIn(s['source_id'],ids)
                for field in ('summary','syntax','parameters','usage','examples','effects'):
                    self.assertTrue(any(field in s.get('fields',[]) for s in e['sources']) or
                                    any(field in u.get('field','').split('/') for u in e.get('unconfirmed',[])),field)

    def test_examples_are_separate_from_observations(self):
        for e in self.entries:
            for x in e['examples']:
                with self.subTest(target=e['typed_key'],example=x.get('id')):
                    self.assertEqual(x['evidence_class'],'EXAMPLE_DERIVED')
                    self.assertTrue(x['erb'].strip())
                    self.assertTrue(x['expected']['ja'].strip())
                    self.assertTrue(x['expected']['en'].strip())
                    self.assertTrue(x['context']['ja'].strip())
                    self.assertTrue(x['context']['en'].strip())
                    self.assertTrue(x['verification']['method'])
                    self.assertTrue(x['source_refs'])

    def test_source_views_match_fixed_archive_members(self):
        members,_=native_members(ROOT)
        for e in self.entries:
            for s in e['sources']:
                if s['source_id']!='SRC-NATIVE-V24': continue
                with self.subTest(target=e['typed_key'],path=s['path']):
                    raw=members[s['archive_member']]
                    self.assertEqual(sha256(raw).hexdigest(),s['member_sha256'])
                    content,_=decode(raw)
                    self.assertLessEqual(s['end_line'],len(content.splitlines()))
                    view=(ROOT/s['viewer_path']).read_text(encoding='utf-8')
                    self.assertIn('id="L'+str(s['start_line'])+'"',view)
                    self.assertIn(s['member_sha256'],view)

    def test_generated_browser_preserves_target_verdicts_cases_and_requirements(self):
        original={(r['kind'],r['name']):r for r in self.survey['targets']}
        for t in self.data['targets']:
            o=original[(t['k'],t['n'])]
            self.assertEqual(t['o'],o['comparison_outcome'])
            self.assertEqual(t['c'],o['case_ids'])
        self.assertEqual(len(self.data['scenarios']),2898)
        self.assertEqual(len(self.data['grammar']),114)
        self.assertEqual(len(self.data['supplemental']),16)
        actual={r['i']:r for t in self.data['targets'] for r in t['r']}
        self.assertEqual(len(actual),3359)
        for r in self.requirements:
            self.assertEqual(actual[r['requirement_id']]['t'],r['verification_requirement'])
            self.assertEqual(actual[r['requirement_id']]['ja'],r['ja'])
            self.assertEqual(actual[r['requirement_id']]['plain'],r['plain_ja'])

    def test_phase_one_evidence_and_readable_results_retained(self):
        loc=json.loads((ROOT/'evidence/legacy226-source-locator-20261118/locator.json').read_bytes())
        classes=Counter(r['classification'] for record in loc['records'] for r in record['references'])
        self.assertEqual(classes,{'PUBLIC_INCLUDED':1750,'PUBLIC_DERIVED':726})
        coverage=set(self.data['saved']['coverage']['mainCaseIds'])
        coverage.update(r['id'] for r in self.data['frozenResults']['records'])
        self.assertEqual(len(coverage),2855)
        self.assertEqual(len(self.data['legacy']),226)

    def test_browser_regeneration_uses_only_public_inputs(self):
        from build_survey_browser import build, read
        observations=json.loads(read(ROOT/'evidence/saved-case-observations/observations.json'))
        self.assertEqual(build(ROOT,observations),(ROOT/'docs/survey-browser.html').read_bytes())

    def test_historical_requirement_notes_do_not_replace_source_fields(self):
        notes=json.loads((ROOT/'reference/requirement-notes.json').read_bytes())['notes']
        original={r['requirement_id']:r for r in self.original}
        actual={r['i']:r for t in self.data['targets'] for r in t['r']}
        self.assertEqual(len(notes),14)
        self.assertEqual(len({n['requirement_id'] for n in notes}),14)
        for n in notes:
            r=actual[n['requirement_id']]
            self.assertEqual(r['t'],original[n['requirement_id']]['verification_requirement'])
            self.assertEqual(r['note'],n)
            self.assertTrue(n['source_refs'])
            for s in n['source_refs']: self.assertTrue((ROOT/s['viewer_path']).is_file())

    def test_no_automatic_external_content(self):
        self.assertNotRegex(self.html,r'''(?i)<(?:script|iframe|link)\b[^>]*(?:src|href)=["']https?://''')
        self.assertNotRegex(self.html,r'''(?i)<img\b[^>]*src=["']https?://''')
        self.assertNotIn('fetch(',self.html)


if __name__=='__main__': unittest.main()
