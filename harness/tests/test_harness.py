import contextlib
import hashlib
import io
import json
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import core
import harness
import local_cases
import validator

PLAN = ROOT / "fixtures" / "representative-plan.json"


def log_for(cases, side):
    lines = []
    for case in cases:
        tag = core.marker(case)
        value = "7" if case["case_id"].endswith("ABS") else "-1" if side == "native" else "3"
        values = {"value": value, "result0": "701", "result1": "702", "results": "AUTO_SENT"}
        lines.append(tag + "_BEGIN")
        for name, _, _ in core.fields(case):
            lines.append(f"{tag}_OBS_{name}=[{values[name]}]")
        lines.append(tag + "_END")
    return ("\r\n".join(lines + ["ZZBATCH_DONE"]) + "\r\n").encode("ascii")


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="test-", dir=ROOT / "tests")
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.cases = core.load_plan(PLAN)

    def test_fixture_and_scoped_comparison(self):
        data = core.fixture(self.cases)
        self.assertIn(b"RESULT:0=701\r\n", data)
        self.assertIn(b"PRINTL ZZBATCH_DONE\r\n", data)
        rows = core.compare_logs(self.cases, log_for(self.cases, "native"), log_for(self.cases, "py"))["cases"]
        self.assertEqual([r["status"] for r in rows], ["matched_scoped", "different", "different"])
        self.assertEqual(rows[1]["native"]["observations"]["value"], "-1")
        self.assertEqual(rows[1]["py"]["observations"]["value"], "3")

    def test_missing_duplicate_and_tampered_sentinel(self):
        raw = log_for(self.cases, "native")
        for altered in (raw.replace(b"ZZBATCH_DONE", b"MISSING"), raw + b"ZZBATCH_DONE\r\n"):
            results = core.compare_logs(self.cases, altered, raw)["cases"]
            self.assertTrue(all(r["status"] == "failure" for r in results))
        bad = raw.replace(b"OBS_result0=[701]", b"OBS_result0=[700]", 1)
        rows = core.compare_logs(self.cases, bad, bad)["cases"]
        self.assertEqual(rows[0]["status"], "different")

    def test_strict_json_and_expression_checks(self):
        with self.assertRaises(ValueError):
            validator.loads('{"a":1,"a":2}')
        with self.assertRaises(ValueError):
            validator.loads('{"a":1e999}')
        with self.assertRaises(ValueError):
            core.validate_expression("ABS(EVIL(1))", "expression_function:ABS")
        with self.assertRaises(ValueError):
            core.load_plan(PLAN, ["not-a-case"])

    def test_isolated_cli_plan_uses_sibling_modules(self):
        proc = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'harness.py'), 'plan', str(PLAN)],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(len(json.loads(proc.stdout)['cases']), len(self.cases))

    def test_seal_detects_tamper_and_extra_file(self):
        folder = self.path / "attempt"
        folder.mkdir()
        (folder / "RESULT.json").write_text("{}", encoding="utf-8")
        validator.seal(folder)
        self.assertTrue(validator.validate(folder, expected_external=[])["valid"])
        (folder / "RESULT.json").write_text('{"changed":true}', encoding="utf-8")
        self.assertFalse(validator.validate(folder, expected_external=[])["valid"])
        (folder / "RESULT.json").write_text("{}", encoding="utf-8")
        (folder / "extra").write_text("x", encoding="utf-8")
        self.assertFalse(validator.validate(folder, expected_external=[])["valid"])

    def test_lock_refusal_and_owned_release(self):
        with harness.shared_lock(self.path) as nonce:
            harness.check_lock(self.path, nonce)
            with self.assertRaises(RuntimeError):
                with harness.shared_lock(self.path):
                    self.fail("must refuse")
        self.assertFalse((self.path / "NATIVE_LOCK.json").exists())
        (self.path / "MEASURE_LOCK.json").write_text("{}", encoding="utf-8")
        with self.assertRaises(RuntimeError):
            with harness.shared_lock(self.path):
                self.fail("must refuse")

    def test_lock_does_not_remove_someone_elses_lock(self):
        with self.assertRaises(RuntimeError):
            with harness.shared_lock(self.path):
                (self.path / "NATIVE_LOCK.json").write_text('{"nonce":"different"}', encoding="utf-8")
        self.assertEqual(validator.read(self.path / "NATIVE_LOCK.json")["nonce"], "different")

    def test_process_enumeration_settles_without_termination(self):
        with mock.patch.object(harness, "native_processes", side_effect=[[{"ProcessId": 123}], []]), \
             mock.patch.object(harness.time, "sleep"):
            self.assertEqual(harness.wait_for_native_absence(), [])

    def test_local_case_fixture_pins(self):
        for name, (path, _) in local_cases.CASES.items():
            self.assertEqual(validator.sha(ROOT / path), local_cases.FIXTURE_SHA[name], name)

    def test_local_case_rejects_changed_fixture_before_lock(self):
        exe = self.path / 'Emuera1824+v24.exe'
        pyz = self.path / 'engine.pyz'
        config = self.path / 'emuera.config'
        for path in (exe, pyz, config):
            path.write_bytes(path.name.encode())
        with mock.patch.object(harness.sys, 'platform', 'win32'), \
             mock.patch.object(harness, 'validate_inputs'), \
             mock.patch.dict(local_cases.FIXTURE_SHA, {'P35': '0' * 64}), \
             mock.patch.object(harness, 'shared_lock') as lock:
            with self.assertRaisesRegex(ValueError, 'fixture SHA-256 mismatch'):
                local_cases.run_case('P35', exe, pyz, config, self.path, self.path / 'out')
            lock.assert_not_called()

    def test_complete_controller_with_synthetic_engines(self):
        exe = self.path / "Emuera1824+v24.exe"
        pyz = self.path / "engine.pyz"
        config = self.path / "emuera.config"
        for p in (exe, pyz, config):
            p.write_bytes(p.name.encode())
        def selected_cases(cwd):
            fixture = (cwd / "ERB" / "SEARCHBOUND01.ERB").read_text(encoding="cp932")
            return [case for case in self.cases if core.marker(case) + "_BEGIN" in fixture]
        def fake_public(*args, **kwargs):
            cwd = Path(kwargs["cwd"])
            log = cwd / ".pyemuera" / "logs" / "emuera.log"
            log.parent.mkdir(parents=True)
            log.write_bytes(log_for(selected_cases(cwd), "py"))
            return subprocess.CompletedProcess(args[0], 0, b"", b"")
        def fake_native(executable, cwd):
            (cwd / "emuera.log").write_bytes(log_for(selected_cases(cwd), "native"))
            return {"outcome": "forced_termination", "pid": 123, "desktop_closed": True,
                    "desktop_created": True, "process_created": True, "input_sent": False, "exit_code": None}
        with mock.patch.object(harness.sys, "platform", "win32"), \
             mock.patch.object(harness, "NATIVE_SHA", validator.sha(exe)), \
             mock.patch.object(harness, "PYZ_SHA", validator.sha(pyz)), \
             mock.patch.object(harness, "CONFIG_SHA", validator.sha(config)), \
             mock.patch.object(harness, "native_processes", return_value=[]), \
             mock.patch.object(harness.native, "run", side_effect=fake_native), \
             mock.patch.object(harness.subprocess, "run", side_effect=fake_public):
            attempt, result = harness.execute(PLAN, exe, pyz, config, self.path, self.path / "out", repeats=2)
            seal = validator.sha(attempt/'SEAL.json')
            checked = harness.audit.audit_attempt(harness, attempt, PLAN, exe, pyz, config, (), 2, seal)
            self.assertEqual(checked['status'], 'completed_with_forced_native_cleanup')
        self.assertEqual(result["status"], "completed_with_forced_native_cleanup")
        self.assertEqual([c["status"] for c in result["cases"]], ["matched_scoped", "different", "different"])
        self.assertTrue(validator.validate(attempt, expected_external=[])["valid"])
        self.assertFalse((self.path / "NATIVE_LOCK.json").exists())

    def test_semantic_audit_resume_and_mutations_without_engines(self):
        exe, pyz, config = (self.path / name for name in ('Emuera1824+v24.exe', 'engine.pyz', 'emuera.config'))
        for p in (exe, pyz, config):
            p.write_bytes(p.name.encode())
        def group(cwd):
            fixture = (cwd/'ERB'/'SEARCHBOUND01.ERB').read_text(encoding='cp932')
            return [case for case in self.cases if core.marker(case)+'_BEGIN' in fixture]
        def fake_public(*args, **kwargs):
            cwd = Path(kwargs['cwd'])
            log = cwd/'.pyemuera'/'logs'/'emuera.log'
            log.parent.mkdir(parents=True)
            log.write_bytes(log_for(group(cwd), 'py'))
            return subprocess.CompletedProcess(args[0], 0, b'out', b'err')
        def fake_native(executable, cwd):
            (cwd/'emuera.log').write_bytes(log_for(group(cwd), 'native'))
            return {'desktop_created':True, 'process_created':True, 'input_sent':False, 'pid':123,
                    'outcome':'natural_rc0', 'exit_code':0, 'desktop_closed':True}
        with mock.patch.object(harness.sys, 'platform', 'win32'), \
             mock.patch.object(harness, 'NATIVE_SHA', validator.sha(exe)), \
             mock.patch.object(harness, 'PYZ_SHA', validator.sha(pyz)), \
             mock.patch.object(harness, 'CONFIG_SHA', validator.sha(config)), \
             mock.patch.object(harness, 'native_processes', return_value=[]), \
             mock.patch.object(harness.native, 'run', side_effect=fake_native), \
             mock.patch.object(harness.subprocess, 'run', side_effect=fake_public):
            attempt, result = harness.execute(PLAN, exe, pyz, config, self.path, self.path/'out', repeats=2)
            self.assertEqual(result['status'], 'completed')
            trusted = validator.sha(attempt/'SEAL.json')
            def audit(path, plan=PLAN, repeats=2, selected=(), seal=trusted):
                with mock.patch.object(harness.native, 'run', side_effect=AssertionError('engine started')), \
                     mock.patch.object(harness.subprocess, 'run', side_effect=AssertionError('process started')):
                    return harness.audit.audit_attempt(harness, path, plan, exe, pyz, config, selected, repeats, seal)
            self.assertTrue(audit(attempt)['valid'])
            arguments = ['harness.py', 'resume', str(attempt), str(PLAN), '--native', str(exe), '--pyz', str(pyz),
                         '--config', str(config), '--repeat-native', '2', '--seal-sha256', trusted]
            with mock.patch.object(sys, 'argv', arguments), contextlib.redirect_stdout(io.StringIO()) as output, \
                 mock.patch.object(harness.native, 'run', side_effect=AssertionError('engine started')), \
                 mock.patch.object(harness.subprocess, 'run', side_effect=AssertionError('process started')):
                self.assertEqual(harness.main(), 0)
            self.assertTrue(json.loads(output.getvalue())['reused'])
            for kwargs in ({'repeats':1}, {'selected':[self.cases[0]['case_id']]}):
                with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                    audit(attempt, **kwargs)
            altered_plan = self.path/'different-plan.json'
            altered_plan.write_bytes(PLAN.read_bytes()+b' ')
            with self.assertRaises(ValueError):
                audit(attempt, plan=altered_plan)
            with mock.patch.dict('os.environ', {'PORTABLE_HARNESS_TEST_CHANGED': '1'}):
                with self.assertRaises(ValueError):
                    audit(attempt)
            original_exe = exe.read_bytes()
            exe.write_bytes(b'different engine')
            with self.assertRaises(ValueError):
                audit(attempt)
            exe.write_bytes(original_exe)
            def mutation(name, change, reseal=True):
                copy = self.path/name
                shutil.copytree(attempt, copy)
                change(copy)
                if reseal:
                    (copy/'SEAL.json').unlink()
                    (copy/'MANIFEST.json').unlink()
                    validator.seal(copy)
                return copy
            def change_result(folder, callback):
                path = folder/'RESULT.json'
                data = validator.read(path)
                callback(data)
                validator.write(path, data)
            raw = mutation('raw-tamper', lambda d:(d/'single'/'native-01'/'emuera.log').write_bytes(b'tampered'), False)
            with self.assertRaises(ValueError):
                audit(raw)
            def alter_raw(folder):
                path = folder/'single'/'native-01'/'emuera.log'
                original = path.read_bytes()
                changed = original.replace(b'OBS_value=[7]', b'OBS_value=[8]', 1)
                self.assertNotEqual(original, changed)
                path.write_bytes(changed)
            resealed_raw = mutation('resealed-raw', alter_raw)
            with self.assertRaises(ValueError):
                audit(resealed_raw, seal=validator.sha(resealed_raw/'SEAL.json'))
            forged = mutation('forged', lambda d:change_result(d, lambda r:r['cases'][0].update(status='different')))
            with self.assertRaises(ValueError):
                audit(forged)
            with self.assertRaises(ValueError):
                audit(forged, seal=validator.sha(forged/'SEAL.json'))
            forged_stage = mutation('forged-stage', lambda d:change_result(d, lambda r:r['stages'][0]['comparisons'][0]['cases'][0].update(status='different')))
            with self.assertRaises(ValueError):
                audit(forged_stage, seal=validator.sha(forged_stage/'SEAL.json'))
            changed_fixture = mutation('fixture', lambda d:(d/'single'/'py'/'ERB'/'SEARCHBOUND01.ERB').write_bytes(b'fake'))
            with self.assertRaises(ValueError):
                audit(changed_fixture, seal=validator.sha(changed_fixture/'SEAL.json'))
            missing_receipt = mutation('missing-receipt', lambda d:change_result(d, lambda r:r['stages'][0].pop('py_inputs_after')))
            with self.assertRaises(ValueError):
                audit(missing_receipt, seal=validator.sha(missing_receipt/'SEAL.json'))
            old = mutation('old-v1', lambda d:change_result(d, lambda r:r.update(schema='portable-expression-run.v1')))
            with self.assertRaises(ValueError):
                audit(old, seal=validator.sha(old/'SEAL.json'))
            invalid_exit = mutation('invalid-exit', lambda d:change_result(d, lambda r:r['stages'][0]['native'][0].update(exit_code=9)))
            with self.assertRaises(ValueError):
                audit(invalid_exit, seal=validator.sha(invalid_exit/'SEAL.json'))
            missing_log = mutation('missing-log', lambda d:(d/'single'/'native-01'/'emuera.log').unlink())
            with self.assertRaises(OSError):
                audit(missing_log, seal=validator.sha(missing_log/'SEAL.json'))
            missing_csv = mutation('missing-csv', lambda d:(d/'single'/'py'/'csv').rmdir())
            with self.assertRaises(ValueError):
                audit(missing_csv, seal=validator.sha(missing_csv/'SEAL.json'))
            failed = mutation('first-failure', lambda d:change_result(d, lambda r:r.update(status='failure', error='initial failure')))
            with self.assertRaises(ValueError):
                audit(failed, seal=validator.sha(failed/'SEAL.json'))
            self.assertEqual(validator.read(failed/'RESULT.json')['status'], 'failure')
            self.assertTrue(audit(attempt)['valid'])
            with mock.patch.object(harness.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1, b'', b'')):
                initial, failure = harness.execute(PLAN, exe, pyz, config, self.path, self.path/'out', repeats=2)
            self.assertEqual(failure['status'], 'failure')
            with self.assertRaises(ValueError):
                audit(initial, seal=validator.sha(initial/'SEAL.json'))
            self.assertEqual(validator.read(initial/'RESULT.json')['status'], 'failure')


if __name__ == "__main__":
    unittest.main()
