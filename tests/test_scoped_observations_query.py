"""Standalone tests for tools/scoped_observations_query.py.

Copy to tests/ after adding the helper and query patch to a repository. All
registers and bundles below are synthetic and need no private-stage layout.
"""
from contextlib import ExitStack
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
MODULE = REPO/'tools/scoped_observations_query.py'
spec = importlib.util.spec_from_file_location('scoped_observations_query_under_test', MODULE)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

# Independent expected mapping, not generated from the implementation.
ROLES = {
    'PRINTDWEMPTY01': (('command_or_syntax','PRINTDW'),),
    'PRINTDWSPACE01': (('command_or_syntax','PRINTDW'),),
    'ARRAY_BOUNDARY_NORMAL_CORRECTED_20261115': (('expression_function','MAXARRAY'),('expression_function','MINARRAY'),('expression_function','SUMARRAY')),
    'LEVEL_BOUNDARY_GETPALAMLV_NEGATIVE_20261115': (('expression_function','GETPALAMLV'),),
    'LEVEL_BOUNDARY_GETPALAMLV_SIZEPLUS1_20261115': (('expression_function','GETPALAMLV'),),
    'LEVEL_BOUNDARY_GETEXPLV_NEGATIVE_20261115': (('expression_function','GETEXPLV'),),
    'LEVEL_BOUNDARY_GETEXPLV_SIZEPLUS1_20261115': (('expression_function','GETEXPLV'),),
    'SAVECHARA_FINITE_BOUNDARIES_EVALUATION_ORDER_20261115': (('command_or_syntax','SAVECHARA'),),
    'DOLOOP259_BREAK_SUPPRESSION': (('command_or_syntax','DO'),('command_or_syntax','LOOP'),
                                    ('structural_syntax','DO'),('structural_syntax','LOOP')),
}


def dump(value):
    return json.dumps(value, ensure_ascii=False, separators=(',',':')).encode('utf-8')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class ScopedQuerySelfContainedTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get('SCOPED_OBS_TEST_TMPDIR'))
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.assertEqual({**helper.EIGHT_TARGETS, helper.DO_CASE:helper.DO_TARGETS}, ROLES)
        self.assertEqual(helper.REGISTER_SNAPSHOT_SHA256,
                         '8d3a3dd1b3e87403df8e518461fbe12439bd1810195c29d4eb2747fd9e8efb94')
        original_pins = dict(helper.PINS)
        self.assertEqual(original_pins[helper.EIGHT][1], 'e80ffb9ccd0be5917fb85919aa129232fc733a8825c4f965872804607550a119')
        self.assertEqual(original_pins[helper.DOLOOP][1], 'c46dcbaa2bbd57d6665fa17a498a9c497a3e73dbe3cbd2a4bb4c1307deb7e7e8')

        rows = []
        for cid, roles in ROLES.items():
            rows.append({'case_id':cid, 'targets':[{'kind':k,'name':n} for k,n in roles],
                         'scenario_verdict':'different_scoped' if cid.startswith('LEVEL_') else 'matched_scoped'})
        for i in range(2898-len(rows)):
            rows.append({'case_id':'FILLER_'+str(i),'targets':[], 'scenario_verdict':'unverified'})
        cases = b''.join(dump(row)+b'\n' for row in rows)
        core = cases
        reg = self.root/helper.REGISTER
        reg.mkdir(parents=True)
        (reg/'cases.jsonl').write_bytes(cases)
        (reg/'core.jsonl').write_bytes(core)
        manifest = {'schema':'case-register-neutral-screened-draft-v2','records':2898,'files':{
            'cases.jsonl':{'size':len(cases),'sha256':digest(cases)},
            'core.jsonl':{'size':len(core),'sha256':digest(core)}}}
        manifest_raw=dump(manifest)
        (reg/'manifest.json').write_bytes(manifest_raw)
        self.stack.enter_context(mock.patch.object(helper,'REGISTER_SNAPSHOT_SHA256',digest(cases)))
        self.stack.enter_context(mock.patch.object(helper,'REGISTER_CORE_SHA256',digest(core)))
        self.stack.enter_context(mock.patch.object(helper,'REGISTER_MANIFEST_SHA256',digest(manifest_raw)))

        records=[]
        for cid in list(ROLES)[:-1]:
            verdict='different_scoped' if cid.startswith('LEVEL_') else 'matched_scoped'
            records.append({'case_id':cid, 'scenario_verdict':verdict,
                            'facts':{'native':-1,'public':0,'unobserved':['natural_exit']},
                            'run_counts':{'native':2,'public':1,'scope':'synthetic'}})
        eight={'schema':'eight-case-independent-observations.v1',
               'source_register_sha256':digest(cases),'records':records}
        do={'case_id':'DOLOOP259_BREAK_SUPPRESSION',
            'typed_targets':[{'kind':k,'name':n} for k,n in ROLES['DOLOOP259_BREAK_SUPPRESSION']],
            'original_verdict':'matched_scoped','conditions':{'fixture':'shared'},
            'observations':{'final':{'O':12113,'X':0}},'runs':[{'id':'native-01'},{'id':'public-01'}],
            'unobserved':['Native natural exit'],'limitations':['synthetic selected evidence only']}
        replacement_pins={}
        for rel, (manifest_name, _, root_name, names) in original_pins.items():
            folder=self.root/rel
            folder.mkdir(parents=True)
            entries=[]
            for name in sorted(names):
                raw = dump(eight) if name=='observations.json' else dump(do) if name=='observation.json' else b'synthetic fixture\n'
                (folder/name).write_bytes(raw)
                entries.append({'root':root_name,'path':name,'size':len(raw),'sha256':digest(raw)})
            m=dump({'schema':'selected-file-set.v1','roots':[root_name],
                    'manifest_location':{'root':root_name,'path':manifest_name},'files':entries})
            (folder/manifest_name).write_bytes(m)
            replacement_pins[rel]=(manifest_name,digest(m),root_name,names)
        self.stack.enter_context(mock.patch.object(helper,'PINS',replacement_pins))

    def test_nine_ids_all_typed_keys_and_selected_pointers(self):
        for cid, roles in ROLES.items():
            with self.subTest(case=cid):
                hits,states=helper.lookup(cid.swapcase(),self.root)
                self.assertEqual(len(hits),1)
                self.assertEqual({states[k]['state'] for k in ('eight_scoped', 'doloop259')},{'AVAILABLE'})
                self.assertEqual(states['legacy50_selected']['state'], 'NOT_INSTALLED')
                hit=hits[0]
                self.assertEqual(hit['case_id'],cid)
                self.assertEqual(hit['matched_targets'],[{'kind':k,'name':n} for k,n in roles])
                self.assertIn('not included',hit['raw_scope'])
                doc=json.loads((self.root/hit['record']['path']).read_bytes())
                for item in hit['selected']:
                    value=doc
                    for part in item['pointer'].strip('/').split('/'):
                        value=value[int(part)] if isinstance(value,list) else value[part]
                    self.assertEqual(value,item['value'])
                for kind,name in roles:
                    found,_=helper.lookup(kind.upper()+':'+name.lower(),self.root)
                    match=[x for x in found if x['case_id']==cid]
                    self.assertEqual(len(match),1)
                    self.assertEqual(match[0]['matched_targets'],[{'kind':kind,'name':name}])
        self.assertFalse(helper.lookup('expression_function:PRINTDW',self.root)[0])
        self.assertEqual(helper.lookup('command_or_syntax:DO',self.root,'structural_syntax')[1]['doloop259']['state'],'INVALID_QUERY')

    def test_missing_corrupt_and_resealed_bundle_do_not_affect_other_bundle(self):
        folder=self.root/helper.EIGHT
        observation=folder/'observations.json'
        saved=observation.read_bytes()
        observation.unlink()
        hits,states=helper.lookup('PRINTDWEMPTY01',self.root)
        self.assertEqual(hits,[])
        self.assertEqual(states['eight_scoped']['state'],'MISSING_FILES')
        self.assertEqual(states['doloop259']['state'],'AVAILABLE')
        observation.write_bytes(saved+b' ')
        self.assertEqual(helper.lookup('PRINTDWEMPTY01',self.root)[1]['eight_scoped']['state'],'INCONSISTENT')
        manifest=folder/'MANIFEST.json'
        m=json.loads(manifest.read_bytes())
        raw=observation.read_bytes()
        entry=next(x for x in m['files'] if x['path']=='observations.json')
        entry['size'],entry['sha256']=len(raw),digest(raw)
        manifest.write_bytes(dump(m))
        self.assertEqual(helper.lookup('PRINTDWEMPTY01',self.root)[1]['eight_scoped']['state'],'INCONSISTENT')

    def test_register_drift_self_consistent_is_not_current(self):
        reg=self.root/helper.REGISTER
        manifest=json.loads((reg/'manifest.json').read_bytes())
        for name in ('core.jsonl','cases.jsonl'):
            path=reg/name
            records=path.read_bytes().splitlines()
            row=json.loads(records[0])
            row['scenario_verdict']='unverified'
            row['targets']=[{'kind':'command_or_syntax','name':'CHANGED'}]
            records[0]=dump(row)
            raw=b'\n'.join(records)+b'\n'
            path.write_bytes(raw)
            manifest['files'][name]={'size':len(raw),'sha256':digest(raw)}
        (reg/'manifest.json').write_bytes(dump(manifest))
        for term in ('PRINTDWEMPTY01','command_or_syntax:PRINTDW','structural_syntax:LOOP'):
            hits,states=helper.lookup(term,self.root)
            self.assertEqual(hits,[])
            self.assertEqual(states['eight_scoped'],{'state':'REGISTER_SNAPSHOT_MISMATCH',
                             'bundle_integrity':'AVAILABLE','register_scope':'CANDIDATE_REGISTER'})
            self.assertEqual(states['doloop259']['state'],'REGISTER_SNAPSHOT_MISMATCH')

    def test_explicit_projection_override_never_mixes_snapshots(self):
        for override in (str(self.root/helper.REGISTER),r'C:\private\other', ''):
            for term in ('PRINTDWEMPTY01','structural_syntax:LOOP'):
                hits,states=helper.lookup(term,self.root,case_projection_override=override)
                self.assertEqual(hits,[])
                for label in ('eight_scoped','doloop259'):
                    self.assertEqual(states[label],{'state':'REGISTER_OVERRIDE_NOT_CHECKED',
                        'bundle_integrity':'AVAILABLE','register_scope':'EXPLICIT_CASE_PROJECTION_OVERRIDE'})
                self.assertNotIn('private',json.dumps(states))

    def test_query_forwards_explicit_projection_override(self):
        tree=ast.parse((REPO/'tools/query.py').read_text(encoding='utf-8'))
        calls=[x for x in ast.walk(tree) if isinstance(x,ast.Call) and
               isinstance(x.func,ast.Attribute) and x.func.attr=='lookup' and
               isinstance(x.func.value,ast.Name) and x.func.value.id=='scoped_helper']
        self.assertEqual(len(calls),1)
        values=[x.value for x in calls[0].keywords if x.arg=='case_projection_override']
        self.assertEqual(len(values),1)
        self.assertIsInstance(values[0],ast.Attribute)
        self.assertEqual(values[0].attr,'case_projection_dir')
        self.assertIsInstance(values[0].value,ast.Name)
        self.assertEqual(values[0].value.id,'args')

    def test_doloop_missing_and_corrupt_leaves_eight_available(self):
        observation=self.root/helper.DOLOOP/'observation.json'
        original=observation.read_bytes()
        observation.unlink()
        hits,states=helper.lookup('PRINTDWEMPTY01',self.root)
        self.assertEqual(len(hits),1)
        self.assertEqual(states['eight_scoped']['state'],'AVAILABLE')
        self.assertEqual(states['doloop259']['state'],'MISSING_FILES')
        observation.write_bytes(original+b' ')
        hits,states=helper.lookup('PRINTDWEMPTY01',self.root)
        self.assertEqual(len(hits),1)
        self.assertEqual(states['doloop259']['state'],'INCONSISTENT')

    def test_missing_and_corrupt_register_do_not_return_hits(self):
        core=self.root/helper.REGISTER/'core.jsonl'
        original=core.read_bytes()
        core.unlink()
        hits,states=helper.lookup('PRINTDWEMPTY01',self.root)
        self.assertEqual(hits,[])
        self.assertEqual(states['eight_scoped']['state'],'REGISTER_MISSING_FILES')
        core.write_bytes(original+b' ')
        self.assertEqual(helper.lookup('PRINTDWEMPTY01',self.root)[1]['eight_scoped']['state'],'REGISTER_INCONSISTENT')

    @unittest.skipUnless(os.name=='nt','Windows junction test')
    def test_actual_windows_junctions_rejected(self):
        for kind in ('bundle','parent','register'):
            with self.subTest(kind=kind):
                root=self.root/('search_'+kind)
                root.mkdir()
                if kind=='parent':
                    link=root/'evidence'
                    target=self.root/'evidence'
                else:
                    (root/'evidence').mkdir()
                    rel=helper.EIGHT if kind=='bundle' else helper.REGISTER
                    link=root/rel
                    target=self.root/rel
                    if kind=='register':
                        for bundle in helper.PINS:
                            shutil.copytree(self.root/bundle,root/bundle)
                self.assertTrue(link.parent.resolve().is_relative_to(self.root.resolve()))
                self.assertTrue(target.resolve().is_relative_to(self.root.resolve()))
                p=subprocess.run(['cmd','/c','mklink','/J',str(link),str(target)],capture_output=True,text=True,timeout=20)
                self.assertEqual(p.returncode,0,p.stderr)
                try:
                    self.assertTrue(getattr(link.lstat(),'st_file_attributes',0)&0x400)
                    self.assertFalse(link.resolve().is_relative_to(root.resolve()))
                    hits,states=helper.lookup('PRINTDWEMPTY01',root)
                    self.assertEqual(hits,[])
                    self.assertEqual(states['eight_scoped']['state'],
                                     'REGISTER_INCONSISTENT' if kind=='register' else 'INCONSISTENT')
                finally:
                    os.rmdir(link)

    def test_missing_helper_query_diagnostic_and_help(self):
        tools=self.root/'separate_tools'
        tools.mkdir()
        shutil.copyfile(REPO/'tools/query.py',tools/'query.py')
        for content in (None,'invalid python !','unrelated = 1'):
            if content is not None:
                (tools/'scoped_observations_query.py').write_text(content,encoding='utf-8')
            proc=subprocess.run([sys.executable,'-I','-B',str(tools/'query.py'),'PRINTDWEMPTY01'],
                                capture_output=True,encoding='utf-8',timeout=20)
            self.assertEqual(proc.returncode,2)
            self.assertEqual(proc.stdout,'')
            self.assertIn('required tools/scoped_observations_query.py is missing or cannot be loaded',proc.stderr)
            self.assertNotIn('Traceback',proc.stderr)
        (tools/'scoped_observations_query.py').unlink()
        proc=subprocess.run([sys.executable,'-I','-B',str(tools/'query.py'),'--help'],
                            capture_output=True,encoding='utf-8',timeout=20)
        self.assertEqual(proc.returncode,0)


if __name__=='__main__':
    unittest.main()
