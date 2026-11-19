import contextlib,hashlib,importlib.util,io,json,pathlib,shutil,sys,tempfile,unittest
from unittest import mock
D=pathlib.Path(__file__).resolve().parent
QUERY = D/'query.py' if (D/'query.py').is_file() else D.parent/'tools/query.py'
spec=importlib.util.spec_from_file_location('query_prototype',QUERY);query=importlib.util.module_from_spec(spec);spec.loader.exec_module(query)
h=lambda b:hashlib.sha256(b).hexdigest()
def encoded(x):return (json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf8')
class CaseProjectionTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='case-query-test-');self.root=pathlib.Path(self.tmp.name)/'root';self.root.mkdir();self.proj=self.root/'evidence/case-register-2898-20261117';self.proj.mkdir(parents=True)
  self.role_a={'kind':'command_or_syntax','name':'PRINTDATA'};self.role_b={'kind':'structural_syntax','name':'PRINTDATA'}
  self.core=[{'case_id':'CASE_SHARED','targets':[self.role_a,self.role_b],'scenario_verdict':'different_scoped','survey_pointer':'/main_scenarios/0','trace_aliases':[{'alias':'CASE_ALIAS','trace_pointer':'/case_aliases/0'}],'target_positions_outside_694':[],'runtime_observation_context':'PRE_EXECUTION_PLAN_VALUE_IN_EXISTING_61_CASE_PROJECTION'}, {'case_id':'CASE_BLOCKED','targets':[self.role_a],'scenario_verdict':'blocked','survey_pointer':'/main_scenarios/1','trace_aliases':[],'target_positions_outside_694':[],'runtime_observation_context':'CONTEXT_UNDETERMINED_REVIEW_REQUIRED'}]
  self.details=[dict(x,projection_state='AUTOMATED_SCREENING_INDEPENDENT_REVIEW_PENDING',withheld_count=2,neutralized_key_count=0,fields={'evidence':{'$case_projection_withheld':'nonincluded_or_private_field'},'sample_token':'SYNTHETIC_SECRET_MUST_NOT_APPEAR','pid':987654321}) for x in self.core]
  self.survey={'main_scenarios':[{'case_id':x['case_id'],'targets':x['targets'],'scenario_verdict':x['scenario_verdict']} for x in self.core]};self.trace={'case_aliases':[{'alias':'CASE_ALIAS','candidate_survey_case_id':'CASE_SHARED','relation':'CANDIDATE_SURVEY_CASE_ID'}]}
  self.sp=self.root/'results/survey.json';self.tp=self.root/'evidence/694-target-trace-20261117/projection.json';self.sp.parent.mkdir(parents=True);self.tp.parent.mkdir(parents=True);self.sp.write_bytes(encoded(self.survey));self.tp.write_bytes(encoded(self.trace));self.save()
 def tearDown(self):self.tmp.cleanup()
 def save(self):
  cb=b''.join(encoded(x) for x in self.core);db=b''.join(encoded(x) for x in self.details);(self.proj/'core.jsonl').write_bytes(cb);(self.proj/'cases.jsonl').write_bytes(db);self.manifest={'schema':'case-register-neutral-screened-draft-v1','records':len(self.core),'candidate_survey_sha256':h(self.sp.read_bytes()),'candidate_trace_sha256':h(self.tp.read_bytes()),'files':{'core.jsonl':{'sha256':h(cb)},'cases.jsonl':{'sha256':h(db)}}};(self.proj/'manifest.json').write_bytes(encoded(self.manifest))
 def drop_projection(self):
  assert self.proj.resolve().is_relative_to(pathlib.Path(self.tmp.name).resolve())
  shutil.rmtree(self.proj)
 def test_case_id_returns_exact_core_and_candidate_relative_pointers(self):
  rows,state=query.case_register_projection('case_shared',self.root);self.assertEqual(len(rows),1);r=rows[0];self.assertEqual(r['case'],self.core[0]);self.assertEqual(r['case']['scenario_verdict'],'different_scoped');self.assertEqual(r['matched_targets'],[self.role_a,self.role_b]);self.assertEqual(r['core_record']['line_1based'],1);self.assertEqual(r['detail_record']['path'],'evidence/case-register-2898-20261117/cases.jsonl');self.assertEqual(r['survey_record']['pointer'],'/main_scenarios/0');self.assertEqual(r['trace_alias_records'][0]['record']['pointer'],'/case_aliases/0');self.assertEqual(state['survey_snapshot'],'MATCHING_SNAPSHOT');self.assertEqual(r['withheld_count'],2)
  text=json.dumps(rows);self.assertNotIn('SYNTHETIC_SECRET_MUST_NOT_APPEAR',text);self.assertNotIn('987654321',text);self.assertEqual(r['detail_fields'],'NOT_EMITTED_PENDING_REVIEW');self.assertEqual(r['nonincluded_markers']['evidence'],{'$case_projection_withheld':'nonincluded_or_private_field'});self.assertIsNone(r['nonincluded_markers']['review'])
 def test_target_and_kind_are_distinct_and_case_record_is_not_rewritten(self):
  rows,_=query.case_register_projection('PRINTDATA',self.root);self.assertEqual(len(rows),2);self.assertEqual({r['case']['scenario_verdict'] for r in rows},{'different_scoped','blocked'})
  rows,_=query.case_register_projection('structural_syntax:PRINTDATA',self.root);self.assertEqual(len(rows),1);self.assertEqual(rows[0]['matched_targets'],[self.role_b]);self.assertEqual(rows[0]['case']['targets'],[self.role_a,self.role_b]);self.assertEqual(rows[0]['case']['runtime_observation_context'],self.core[0]['runtime_observation_context'])
  rows,_=query.case_register_projection('case_blocked',self.root,kind='structural_syntax');self.assertEqual(rows,[])
  with self.assertRaises(ValueError):query.case_register_projection('structural_syntax:PRINTDATA',self.root,kind='command_or_syntax')
 def test_external_private_override_never_returns_its_path(self):
  outside=pathlib.Path(self.tmp.name)/'private-location';shutil.copytree(self.proj,outside);self.drop_projection();rows,state=query.case_register_projection('CASE_SHARED',self.root,override=outside);self.assertEqual(state['state'],'AVAILABLE');self.assertIsNone(rows[0]['core_record']['path']);self.assertIsNone(rows[0]['detail_record']['path']);self.assertEqual(rows[0]['detail_record']['location'],'EXTERNAL_STAGING_NOT_LINKED');self.assertNotIn(str(outside),json.dumps(rows))
 def test_default_missing_and_explicit_missing_are_distinct(self):
  self.drop_projection();rows,state=query.case_register_projection('CASE_SHARED',self.root);self.assertEqual(rows,[]);self.assertEqual(state['state'],'NOT_INSTALLED')
  with self.assertRaises(ValueError):query.case_register_projection('CASE_SHARED',self.root,override=self.proj)
 def test_stale_snapshots_do_not_claim_usable_references(self):
  self.sp.write_bytes(encoded({'main_scenarios':[]}));self.tp.write_bytes(encoded({'case_aliases':[]}));rows,state=query.case_register_projection('CASE_SHARED',self.root);self.assertEqual(state['survey_snapshot'],'SNAPSHOT_MISMATCH');self.assertEqual(state['trace_snapshot'],'SNAPSHOT_MISMATCH');self.assertIsNone(rows[0]['survey_record']);self.assertEqual(rows[0]['trace_alias_records'],[]);self.assertEqual(rows[0]['case']['survey_pointer'],'/main_scenarios/0')
 def test_resealed_blank_jsonl_line_is_rejected(self):
  raw=(self.proj/'core.jsonl').read_bytes()+b'\n';(self.proj/'core.jsonl').write_bytes(raw);self.manifest['files']['core.jsonl']['sha256']=h(raw);(self.proj/'manifest.json').write_bytes(encoded(self.manifest))
  with self.assertRaisesRegex(ValueError,'blank case projection line'):query.case_register_projection('CASE_SHARED',self.root)
 def test_private_paths_in_core_are_rejected_without_returning_value(self):
  self.core[0]['runtime_observation_context']='C:\\Users\\Example\\private\\secret.json';self.details[0]['runtime_observation_context']=self.core[0]['runtime_observation_context'];self.save()
  with self.assertRaises(ValueError) as caught:query.case_register_projection('CASE_SHARED',self.root)
  self.assertNotIn('Example',str(caught.exception))
 def test_resealed_mismatched_core_and_detail_are_rejected(self):
  self.details[0]['scenario_verdict']='matched_scoped';self.save()
  with self.assertRaisesRegex(ValueError,'detail and core'):query.case_register_projection('CASE_SHARED',self.root)
 def test_private_path_input_is_not_echoed_by_cli(self):
  for args in (['C:\\Users\\Example\\secret.json'], ['CASE_SHARED','--kind','private/hidden']):
   stdout,stderr=io.StringIO(),io.StringIO()
   with mock.patch.object(sys,'argv',['query.py']+args), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
    with self.assertRaises(SystemExit) as caught:query.main()
   self.assertEqual(caught.exception.code,2);self.assertEqual(stdout.getvalue(),'');self.assertNotIn('Example',stderr.getvalue());self.assertNotIn('private/hidden',stderr.getvalue())
 def test_unreviewed_raw_evidence_cannot_escape_through_marker(self):
  self.details[0]['fields']['evidence']={'raw':'SYNTHETIC_SECRET_MUST_NOT_APPEAR'};self.save()
  with self.assertRaisesRegex(ValueError,'unsupported non-included marker') as caught:query.case_register_projection('CASE_SHARED',self.root)
  self.assertNotIn('SYNTHETIC_SECRET_MUST_NOT_APPEAR',str(caught.exception))
 def test_duplicate_ids_and_bad_file_hash_are_rejected(self):
  self.core[1]['case_id']='case_shared';self.details[1]['case_id']='case_shared';self.save()
  with self.assertRaisesRegex(ValueError,'ID conflict'):query.case_register_projection('PRINTDATA',self.root)
  self.core[1]['case_id']='CASE_BLOCKED';self.details[1]['case_id']='CASE_BLOCKED';self.save();(self.proj/'core.jsonl').write_bytes((self.proj/'core.jsonl').read_bytes()+b' ')
  with self.assertRaisesRegex(ValueError,'hash mismatch'):query.case_register_projection('CASE_SHARED',self.root)
 def test_empty_and_unknown_are_not_fabricated(self):
  rows,state=query.case_register_projection('UNKNOWN_X',self.root);self.assertEqual(rows,[]);self.assertEqual(state['state'],'AVAILABLE')
 def test_invalid_survey_or_alias_binding_is_rejected(self):
  self.survey['main_scenarios'][0]['scenario_verdict']='matched_scoped';self.sp.write_bytes(encoded(self.survey));self.save()
  with self.assertRaisesRegex(ValueError,'survey record'):query.case_register_projection('CASE_SHARED',self.root)
  self.survey['main_scenarios'][0]['scenario_verdict']='different_scoped';self.sp.write_bytes(encoded(self.survey));self.trace['case_aliases'][0]['candidate_survey_case_id']='CASE_BLOCKED';self.tp.write_bytes(encoded(self.trace));self.save()
  with self.assertRaisesRegex(ValueError,'trace alias'):query.case_register_projection('CASE_SHARED',self.root)
if __name__=='__main__':unittest.main(verbosity=2)
