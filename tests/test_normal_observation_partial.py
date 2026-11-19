"""C196 partial availability, safe failures, and same-byte mode binding."""
import contextlib,copy,hashlib,importlib.util,io,json,pathlib,shutil,subprocess,sys,tempfile,unittest
from unittest.mock import patch
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(name,p):
    spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec)
    # Keep sealed evidence trees byte-identical: importing must not add __pycache__.
    bytecode=sys.dont_write_bytecode;sys.dont_write_bytecode=True
    try: spec.loader.exec_module(m)
    finally: sys.dont_write_bytecode=bytecode
    return m
query=load('partial_query',ROOT/'tools/query.py')
class PartialTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(prefix='c196-partial-');cls.root=pathlib.Path(cls.tmp.name)/'candidate';shutil.copytree(ROOT,cls.root)
    @classmethod
    def tearDownClass(cls): cls.tmp.cleanup()
    def run_cli(self,term,partial=False,kind=None):
        args=['query.py',term]+(['--partial'] if partial else [])+(['--kind',kind] if kind else [])
        with patch.object(query,'ROOT',self.root),patch.object(sys,'argv',args),contextlib.redirect_stdout(io.StringIO()) as out,contextlib.redirect_stderr(io.StringIO()) as err:
            try: code=query.main()
            except SystemExit as exc:code=exc.code
        return code,json.loads(out.getvalue()) if out.getvalue() else None,err.getvalue()
    def test_strict_and_partial_valid_and_kind(self):
        code,base,_=self.run_cli('WAIT'); self.assertEqual(code,0)
        code,data,_=self.run_cli('WAIT',True); self.assertEqual(code,0)
        self.assertEqual(data.pop('search_status')['state'],'NO_C196_INCONSISTENCY_DETECTED');self.assertEqual(data,base)
        code,data,_=self.run_cli('C196_04',True);self.assertEqual(code,0)
        self.assertEqual(len([x for x in data['saved_observations'] if x['collection']=='normal_observations_196']),1)
        code,data,_=self.run_cli('C196_04',True,'expression_function');self.assertEqual(code,1)
        self.assertEqual(data['saved_observation_availability']['normal_observations_196'],'AVAILABLE')
    def test_c196_corruption_keeps_other_results_but_is_partial(self):
        bundle=self.root/'evidence/normal-observation-access-20261117';record=bundle/'observations.json';original=record.read_bytes()
        _,valid,_=self.run_cli('WAIT');record.write_bytes(original+b'X')
        try:
            code,data,err=self.run_cli('WAIT');self.assertEqual(code,2);self.assertIsNone(data);self.assertNotIn(str(self.root),err)
            code,data,err=self.run_cli('WAIT',True);self.assertEqual(code,3);self.assertEqual(err,'')
            self.assertEqual(data.pop('search_status'),{'state':'PARTIAL','reason':'NORMAL_OBSERVATIONS_196_INCONSISTENT'})
            self.assertEqual(data['saved_observation_availability'].pop('normal_observations_196'),'INCONSISTENT')
            valid['saved_observation_availability'].pop('normal_observations_196');self.assertEqual(data,valid)
            code,data,_=self.run_cli('C196_04',True);self.assertEqual(code,3)
            self.assertEqual(data['saved_observation_availability']['normal_observations_196'],'INCONSISTENT')
            self.assertFalse(any(x['collection']=='normal_observations_196' for x in data['saved_observations']))
        finally:record.write_bytes(original)
    def test_not_installed_is_distinct_and_other_search_works(self):
        bundle=self.root/'evidence/normal-observation-access-20261117';held=bundle.with_name('held-c196');bundle.rename(held)
        try:
            code,data,_=self.run_cli('WAIT',True);self.assertEqual(code,0)
            self.assertEqual(data['saved_observation_availability']['normal_observations_196'],'NOT_INSTALLED')
            self.assertEqual(data['search_status']['state'],'NO_C196_INCONSISTENCY_DETECTED')
            code,data,_=self.run_cli('C196_04',True);self.assertEqual(code,1)
        finally:held.rename(bundle)
    def test_dependency_raw_corruption_is_partial(self):
        raw=self.root/'evidence/multi-group-101-20261117/assets/bbdfcba295b75e9aeb4106422889f6615054e7d8f7198a24ac9ce7855856725b.bin';old=raw.read_bytes();raw.write_bytes(old+b'X')
        try:
            code,data,_=self.run_cli('WAIT',True);self.assertEqual(code,3)
            self.assertEqual(data['saved_observation_availability']['normal_observations_196'],'INCONSISTENT')
            self.assertEqual(data['search_status']['state'],'PARTIAL')
            self.assertTrue(data['targets'] or data['cases'] or data['saved_observations'])
        finally:raw.write_bytes(old)
    def test_other_collection_failure_remains_fail_fast(self):
        p=self.root/'evidence/printdata-61-20261117/index.json';old=p.read_bytes();p.write_bytes(b'{')
        try:
            code,data,err=self.run_cli('WAIT',True);self.assertEqual(code,2);self.assertIsNone(data)
            self.assertNotIn(str(self.root),err)
        finally:p.write_bytes(old)
    def test_missing_source_and_helper_do_not_leak_path_or_execute_stub(self):
        bundle=self.root/'evidence/normal-observation-access-20261117'; manifest=bundle/'manifest.json';pin=hashlib.sha256(manifest.read_bytes()).hexdigest()
        def standalone():return subprocess.run([sys.executable,'-I','-B',str(bundle/'verify.py'),'--evidence-root',str(self.root/'evidence'),'--manifest-sha256',pin],capture_output=True,text=True,encoding='utf8')
        for path in (self.root/'evidence/multi-group-101-20261117/index.json',self.root/'evidence/multi-group-101-20261117/assets/60d4874a8e3d7495a9d6adad8bdf11fb7cf11d8226ac94ab94fee7e7018237e3.bin',self.root/'evidence/multi-group-101-20261117/assets/bbdfcba295b75e9aeb4106422889f6615054e7d8f7198a24ac9ce7855856725b.bin'):
            old=path.read_bytes();path.unlink()
            try:
                p=standalone();self.assertNotEqual(p.returncode,0);self.assertNotIn(str(self.root),p.stderr+p.stdout)
                self.assertEqual(p.stderr,'FAIL: evidence or verification tool is unavailable or inconsistent\n')
            finally:path.write_bytes(old)
        tool=self.root/'tools/file_set_manifest.py';original=tool.read_bytes();stub=b"raise RuntimeError('UNTRUSTED_TOOL_EXECUTED')\n";tool.write_bytes(stub)
        readme=bundle/'README.md';old_readme=readme.read_bytes();readme.write_bytes(old_readme+b'X')
        try:
            isolated=load('query_untrusted_tool_check',self.root/'tools/query.py')
            with self.assertRaisesRegex(ValueError,'verification tool unavailable or inconsistent'):
                isolated._normal_observations_196('C196_04',self.root,None)
            with patch.object(isolated,'ROOT',self.root),patch.object(sys,'argv',['query.py','WAIT','--partial']),contextlib.redirect_stdout(io.StringIO()) as stdout,contextlib.redirect_stderr(io.StringIO()) as stderr:
                with self.assertRaises(SystemExit) as exc:isolated.main()
            self.assertEqual(exc.exception.code,2);self.assertNotIn('UNTRUSTED_TOOL_EXECUTED',stdout.getvalue()+stderr.getvalue());self.assertNotIn(str(self.root),stderr.getvalue())
            p=standalone();self.assertNotEqual(p.returncode,0);self.assertNotIn('UNTRUSTED_TOOL_EXECUTED',p.stderr+p.stdout);self.assertNotIn(str(self.root),p.stderr+p.stdout)
        finally:tool.write_bytes(original);readme.write_bytes(old_readme)
        tool.unlink()
        try:
            isolated=load('query_missing_tool_check',self.root/'tools/query.py')
            with self.assertRaisesRegex(ValueError,'verification tool unavailable or inconsistent'): isolated._normal_observations_196('C196_04',self.root,None)
            p=standalone();self.assertNotEqual(p.returncode,0);self.assertNotIn(str(self.root),p.stderr+p.stdout)
        finally:tool.write_bytes(original)
    def test_equal_sha_mode_swap_resealed_rejected(self):
        bundle=self.root/'evidence/normal-observation-access-20261117';data=bundle/'observations.json';manifest=bundle/'manifest.json';old_data=data.read_bytes();old_manifest=manifest.read_bytes();old_pin=hashlib.sha256(old_manifest).hexdigest()
        d=json.loads(old_data);obs=d['cases'][0]['observations'];self.assertEqual(obs[0]['history_sha256'],obs[1]['history_sha256']);self.assertNotEqual(obs[0]['mode_source_record_sha256'],obs[1]['mode_source_record_sha256'])
        obs[0],obs[1]=obs[1],obs[0];obs[0]['mode']='native-01';obs[1]['mode']='native-02'
        data.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
        try:
            manifest.unlink();p=subprocess.run([sys.executable,'-I','-B',str(self.root/'tools/file_set_manifest.py'),'create','--manifest',str(manifest),'--root','evidence='+str(bundle)],capture_output=True);self.assertEqual(p.returncode,0)
            new_pin=hashlib.sha256(manifest.read_bytes()).hexdigest(); self.assertNotEqual(new_pin,old_pin)
            verifier=load('mode_binding_verifier',bundle/'verify.py')
            with self.assertRaisesRegex(ValueError,'mode source record binding'):verifier.run(data,self.root/'evidence')
            p=subprocess.run([sys.executable,'-I','-B',str(bundle/'verify.py'),'--evidence-root',str(self.root/'evidence'),'--manifest-sha256',new_pin],capture_output=True,encoding='utf8');self.assertNotEqual(p.returncode,0)
            code,result,_=self.run_cli('WAIT',True);self.assertEqual(code,3);self.assertEqual(result['saved_observation_availability']['normal_observations_196'],'INCONSISTENT')
            self.assertTrue(result['targets'] or result['cases'] or result['saved_observations'])
            code,result,_=self.run_cli('C196_04',True);self.assertEqual(code,3)
            self.assertFalse(any(x['collection']=='normal_observations_196' for x in result['saved_observations']))
        finally:data.write_bytes(old_data);manifest.write_bytes(old_manifest)
if __name__=='__main__':unittest.main()
