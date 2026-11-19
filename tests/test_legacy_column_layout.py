"""Anonymous fixtures for the PRINTC/PRINTLC shared-column legacy layout."""
import hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('legacy_column',HERE.parent/'tools/legacy_evidence.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)

def digest(b):return hashlib.sha256(b).hexdigest()

class ColumnLayout(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='synthetic-column-',dir=HERE);self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  self.names={'PRINTC':'COLUMN_PRINTC_EMPTY_SHORT_EQUAL_20261115','PRINTLC':'COLUMN_PRINTLC_EMPTY_SHORT_EQUAL_20261115'}
  self.values=[('EMPTY','',0),('SHORT','ABC',3),('EQUAL','ABCDEFGHIJKLMNOPQRSTUVWXY',25)]
  self.members=[]; fixture=['@SYSTEM_TITLE','; synthetic fixture','RESULT = 777','RESULTS = SENTINEL']; output=['synthetic loading'];case_rows=[]
  for target in ('PRINTC','PRINTLC'):
   for suffix,value,width in self.values:
    label=target+'_'+suffix;case_rows.append({'target':target,'id':label,'value':value,'ascii_width':width})
    fixture.extend(['PRINTL '+label+'_BEGIN',target+(' '+value if value else ''),'PRINTL |'+label+'_END','PRINTFORML '+label+'_STATE R={RESULT} S=[%RESULTS%]'])
    rendered='' if not value else value.rjust(25) if target=='PRINTC' else value.ljust(25)+' '
    output.extend([label+'_BEGIN',rendered+'|'+label+'_END',label+'_STATE R=777 S=[SENTINEL]'])
  fixture.extend(['PRINTL COLUMN_DONE','OUTPUTLOG','QUIT']);output.append('COLUMN_DONE')
  self.fixture=('\n'.join(fixture)+'\n').encode('utf8');self.config='PRINTCの文字数:25\r\n'.encode('cp932');self.text='\r\n'.join(output)+'\r\n';self.pyz=digest(b'synthetic public engine');self.exe=b'synthetic native executable';self.comp={'verdict':'matched_scoped','raw_native_repeat_equal':True,'raw_public_equal':True,'state_sentinels_match':True,'cases':case_rows,'texts':{m:self.text for m in ('native-01','native-02','public-01')}}
  self.put('COMPARISON.json',self.comp)
  for mode in ('native-01','native-02','public-01'):
   self.put(mode+'/ERB/SEARCHBOUND01.ERB',self.fixture);self.put(mode+'/emuera.config',self.config);raw=mode+'/emuera.log' if mode.startswith('native') else mode+'/.pyemuera/logs/emuera.log';self.put(raw,self.text.encode('utf-16'))
   self.put(mode+'/stdout.bin',b'synthetic output');self.put(mode+'/stderr.bin',b'')
   inputs={'ERB/SEARCHBOUND01.ERB':digest(self.fixture),'emuera.config':digest(self.config)}; argv=['synthetic-runner','anon-run/'+mode] if mode.startswith('native') else ['synthetic-pyz','.'];before={'argv':argv,'inputs_before':inputs,'pyz_before':self.pyz,'exe_before':digest(self.exe) if mode.startswith('native') else None};after={**before,'inputs_after':inputs,'pyz_after':self.pyz,'returncode':0}
   self.put(mode+'/RECEIPT_BEFORE.json',before);self.put(mode+'/RECEIPT_AFTER.json',after)
   if mode.startswith('native'):
    self.put(mode+'/Emuera1824+v24.exe',self.exe);self.put(mode+'/probe.json',{'fixture_sha256':digest(self.fixture),'config_sha256':digest(self.config),'native_exe_sha256':digest(self.exe),'process_created':True,'cwd':'anon-run/'+mode,'exit_code_observed':False,'cleanup_terminate_ok':True})
  self.register={'records':[{'case_id':cid,'targets':[{'kind':'command_or_syntax','name':name}],'scenario_verdict':'matched_scoped'} for name,cid in self.names.items()]};self.put_root('audit/snapshot/CASE_SCENARIO_REGISTER.json',self.register);self.seal()
 def put_root(self,path,value):
  f=self.root/path;f.parent.mkdir(parents=True,exist_ok=True);b=value if isinstance(value,bytes) else (json.dumps(value,ensure_ascii=False)+'\n').encode('utf8');f.write_bytes(b);return digest(b)
 def put(self,path,value):
  if path not in self.members:self.members.append(path)
  return self.put_root('records/'+path,value)
 def get(self,path):return json.loads((self.root/'records'/path).read_text(encoding='utf8'))
 def reanchor(self):
  manifest_hash=digest((self.root/'records/MANIFEST.json').read_bytes());rows=[]
  for i,(name,cid) in enumerate(self.names.items()):
   target={'kind':'command_or_syntax','name':name};doc={'schema':'target-finite-comparison-adjudication-1','target':target,'decision':'necessary_comparison_complete','comparison_outcome':'matched_in_finite_scope','case_ids':[cid],'manifest_path':'records/MANIFEST.json','manifest_sha256':manifest_hash};ph=self.put_root('records/'+name+'.json',doc)
   rows.append({'target':target,'row_outcome':'matched_in_finite_scope','gaps':[{'code':'ORIGINAL_REQUIREMENT_LINK_ADAPTER_REQUIRED'}],'errors':[],'case_role_links':[{'case_id':cid,'registered_typed_target_matches':True,'register_snapshot':'snapshot/CASE_SCENARIO_REGISTER.json','register_pointer':'/records/'+str(i)}],'acceptance':{'path':'records/'+name+'.json','sha256':ph,'record_pointer':'','schema':doc['schema']},'readbacks':[]})
  audit={'schema':a.AUDIT_SCHEMA,'root_capture_pins':{'CASE_SCENARIO_REGISTER.json':digest((self.root/'audit/snapshot/CASE_SCENARIO_REGISTER.json').read_bytes())},'rows':rows};self.pin=self.put_root('audit/result.json',audit)
 def seal(self):
  entries=[]
  for rel in self.members:
   f=self.root/'records'/rel;b=f.read_bytes();entries.append({'path':rel,'size':len(b),'sha256':digest(b)})
  self.put_root('records/MANIFEST.json',{'files':entries});self.reanchor()
 def inspect(self,name='PRINTC'):return a.adapt(self.root,'audit/result.json',self.pin,'command_or_syntax',name)
 def test_both_target_roles_share_three_modes_and_remain_partial(self):
  for name in ('PRINTC','PRINTLC'):
   r=self.inspect(name);self.assertEqual(r['status'],'PARTIAL');self.assertEqual(r['case_ids'],[self.names[name]]);self.assertEqual(r['declared_outcome'],'matched_in_finite_scope');self.assertTrue(r['shared_fixture']);self.assertEqual([x['name'] for x in r['modes']],['native-01','native-02','public-01']);self.assertEqual(r['modes'][0]['natural_exit'],'unobserved');self.assertEqual(r['modes'][2]['public_returncode'],0);self.assertTrue(r['gaps'])
   observed=r['selected_observations'];self.assertEqual([x['condition'] for x in observed],['EMPTY','SHORT','EQUAL']);self.assertEqual(observed[1]['rendered_text'],(' '*22+'ABC') if name=='PRINTC' else ('ABC'+' '*23));self.assertEqual(observed[1]['RESULT'],777);self.assertEqual(observed[1]['RESULTS'],'SENTINEL')
 def test_unrecognized_target_not_generalized(self):
  f=self.root/'audit/result.json';d=json.loads(f.read_text(encoding='utf8'));d['rows'][0]['target']['name']='ONEINPUTS';self.pin=self.put_root('audit/result.json',d);r=a.adapt(self.root,'audit/result.json',self.pin,'command_or_syntax','ONEINPUTS');self.assertEqual(r['status'],'UNSUPPORTED')
 def test_wrong_target_kind_rejected(self):
  with self.assertRaises(a.EvidenceError):a.adapt(self.root,'audit/result.json',self.pin,'method_as_command','PRINTC')
 def test_missing_and_modified_raw_rejected(self):
  f=self.root/'records/native-01/emuera.log';original=f.read_bytes();f.unlink()
  with self.assertRaises(OSError):self.inspect()
  f.write_bytes(original+b'X')
  with self.assertRaises(a.EvidenceError):self.inspect()
 def test_parent_manifest_pin_mismatch_rejected(self):
  f=self.root/'records/MANIFEST.json';f.write_bytes(f.read_bytes()+b' ')
  with self.assertRaisesRegex(a.EvidenceError,'hash mismatch'):self.inspect()
 def test_native_receipt_mode_swap_even_when_raw_is_identical(self):
  for typ in ('RECEIPT_BEFORE.json','RECEIPT_AFTER.json'):
   p=self.root/'records/native-01'/typ;q=self.root/'records/native-02'/typ;x=p.read_bytes();p.write_bytes(q.read_bytes());q.write_bytes(x)
  self.seal()
  with self.assertRaisesRegex(a.EvidenceError,'receipt mode'):self.inspect()
 def test_fixture_condition_spoof_even_after_repin(self):
  changed=self.fixture.replace(b'PRINTC ABC\n',b'PRINTC XYZ\n');self.assertNotEqual(changed,self.fixture);new=digest(changed)
  for mode in ('native-01','native-02','public-01'):
   self.put(mode+'/ERB/SEARCHBOUND01.ERB',changed)
   for typ in ('RECEIPT_BEFORE.json','RECEIPT_AFTER.json'):
    d=self.get(mode+'/'+typ);d['inputs_before']['ERB/SEARCHBOUND01.ERB']=new
    if 'inputs_after' in d:d['inputs_after']['ERB/SEARCHBOUND01.ERB']=new
    self.put(mode+'/'+typ,d)
   if mode.startswith('native'):
    d=self.get(mode+'/probe.json');d['fixture_sha256']=new;self.put(mode+'/probe.json',d)
  self.seal()
  with self.assertRaisesRegex(a.EvidenceError,'fixture condition body'):self.inspect()
 def test_forged_output_even_after_repin(self):
  text=self.text.replace('                      ABC|PRINTC_SHORT_END',' ABC|PRINTC_SHORT_END');self.assertNotEqual(text,self.text)
  for mode in ('native-01','native-02','public-01'):
   path=mode+'/emuera.log' if mode.startswith('native') else mode+'/.pyemuera/logs/emuera.log';self.put(path,text.encode('utf-16'));self.comp['texts'][mode]=text
  self.put('COMPARISON.json',self.comp);self.seal()
  with self.assertRaisesRegex(a.EvidenceError,'padding'):self.inspect()
 def test_wrong_typed_case_register_even_after_repin(self):
  self.register['records'][0]['targets'][0]['kind']='expression_function';self.put_root('audit/snapshot/CASE_SCENARIO_REGISTER.json',self.register);self.seal()
  with self.assertRaisesRegex(a.EvidenceError,'case register'):self.inspect()
 def test_manifest_duplicate_even_after_repin(self):
  p=self.root/'records/MANIFEST.json';d=json.loads(p.read_text(encoding='utf8'));d['files'].append(d['files'][0]);self.put_root('records/MANIFEST.json',d);self.reanchor()
  with self.assertRaisesRegex(a.EvidenceError,'duplicate manifest'):self.inspect()
 def test_source_verdict_is_not_rewritten(self):
  p=self.root/'records/PRINTC.json';d=json.loads(p.read_text(encoding='utf8'));d['comparison_outcome']='different_scoped';ph=self.put_root('records/PRINTC.json',d);q=self.root/'audit/result.json';aud=json.loads(q.read_text(encoding='utf8'));aud['rows'][0]['acceptance']['sha256']=ph;self.pin=self.put_root('audit/result.json',aud)
  with self.assertRaisesRegex(a.EvidenceError,'outcome mismatch'):self.inspect()
if __name__=='__main__':unittest.main()
