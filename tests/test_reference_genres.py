"""Public-data checks for the purpose-based genre classification."""
from collections import Counter
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class GenreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = json.loads((ROOT / 'reference/entries.json').read_bytes())['entries']
        cls.genres = json.loads((ROOT / 'reference/genres.json').read_bytes())
        cls.targets = json.loads((ROOT / 'reference/target-genres.json').read_bytes())
        cls.html = (ROOT / 'docs/survey-browser.html').read_text(encoding='utf-8')
        payload = re.search(r'<script id="data" type="application/json">(.*?)</script>', cls.html, re.S)
        cls.payload = json.loads(payload.group(1))

    def test_genre_catalog_is_complete_and_bilingual(self):
        genres = self.genres['genres']
        self.assertEqual(len(genres), 18)
        ids = [g['id'] for g in genres]
        self.assertEqual(len(set(ids)), 18)
        self.assertEqual([g['order'] for g in genres], list(range(1, 19)))
        for genre in genres:
            with self.subTest(genre=genre['id']):
                self.assertTrue(genre['ja'].strip())
                self.assertTrue(genre['en'].strip())
                self.assertTrue(genre['description_ja'].strip())
                self.assertTrue(genre['description_en'].strip())

    def test_every_target_has_exactly_one_primary_genre(self):
        entries = {(e['typed_key']['kind'], e['typed_key']['name']) for e in self.entries}
        rows = self.targets['targets']
        keys = [(r['typed_key']['kind'], r['typed_key']['name']) for r in rows]
        self.assertEqual(len(rows), 694)
        self.assertEqual(len(set(keys)), 694)
        self.assertEqual(set(keys), entries)
        genre_ids = {g['id'] for g in self.genres['genres']}
        primary = Counter(r['primary'] for r in rows)
        self.assertEqual(sum(primary.values()), 694)
        for row in rows:
            with self.subTest(target=row['typed_key']):
                self.assertIn(row['primary'], genre_ids)
                self.assertNotIn(row['primary'], row['secondary'])
                self.assertEqual(len(set(row['secondary'])), len(row['secondary']))
                for secondary in row['secondary']:
                    self.assertIn(secondary, genre_ids)
                self.assertTrue(row['rationale'].strip())
                self.assertTrue(row['rationale_en'].strip())

    def test_same_name_command_and_method_forms_share_classification(self):
        rows = {(r['typed_key']['kind'], r['typed_key']['name']): r
                for r in self.targets['targets']}
        function_names = {r['typed_key']['name'] for r in self.targets['targets']
                          if r['typed_key']['kind'] == 'expression_function'}
        for name in function_names:
            command = rows.get(('method_as_command', name))
            function = rows.get(('expression_function', name))
            if command is None:
                continue
            with self.subTest(name=name):
                self.assertEqual(command['primary'], function['primary'])
                self.assertEqual(command['secondary'], function['secondary'])

    def test_classification_examples_from_the_public_scope(self):
        rows = {(r['typed_key']['kind'], r['typed_key']['name']): r
                for r in self.targets['targets']}
        self.assertEqual(rows[('command_or_syntax', 'PRINTW')]['primary'], 'display')
        self.assertIn('input', rows[('command_or_syntax', 'PRINTW')]['secondary'])
        self.assertEqual(rows[('expression_function', 'ABS')]['primary'], 'math')
        self.assertEqual(rows[('expression_function', 'STRFIND')]['primary'], 'string')
        self.assertEqual(rows[('command_or_syntax', 'SET')]['primary'], 'variable')
        self.assertEqual(rows[('expression_function', 'FIND_VARDATA')]['primary'], 'internal')
        self.assertEqual(rows[('expression_function', 'CHKGLOBALDATA')]['primary'], 'internal')
        self.assertEqual(rows[('command_or_syntax', 'CUPCHECK')]['primary'], 'character')

    def test_embedded_browser_data_matches_master(self):
        self.assertEqual(len(self.payload['genres']), 18)
        embedded = {(t['k'], t['n']): (t['g'], t['sg']) for t in self.payload['targets']}
        self.assertEqual(len(embedded), 694)
        for row in self.targets['targets']:
            with self.subTest(target=row['typed_key']):
                self.assertEqual(embedded[(row['typed_key']['kind'], row['typed_key']['name'])],
                                 (row['primary'], row['secondary']))
        catalog = {(g['id'], g['ja'], g['en'], g['order']) for g in self.payload['genres']}
        self.assertEqual(catalog, {(g['id'], g['ja'], g['en'], g['order'])
                                   for g in self.genres['genres']})

