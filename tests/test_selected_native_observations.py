"""Check selected observations against saved engine output."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'evidence' / 'nine-saved-observations-20261117'

def saved_text(mode, role):
    material, = [item for item in mode['materials'] if item['role'] == role]
    relative = Path(material['readable_path'])
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('invalid observation path')
    return (ROOT / relative).read_text(encoding='utf-8')

class SelectedObservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / 'data' / 'cases.jsonl').open(encoding='utf-8') as stream:
            cls.cases = {row['case_id']: row for row in map(json.loads, stream)}

    def test_limit_and_inrange_selected_values_come_from_saved_logs(self):
        for command in ('LIMIT', 'INRANGE'):
            row = self.cases[f'METHOD_BOUNDARY_{command}_NORMAL_20261115']
            modes = {mode['mode']: mode for mode in row['modes']}
            for observed in row['observation']['modes']:
                role = 'native_emuera_log' if observed['mode'].startswith('native-') else 'public_process_stdout'
                lines = saved_text(modes[observed['mode']], role).splitlines()
                for marker in observed['selected_after_markers']:
                    self.assertEqual(lines.count(marker), 1, (command, observed['mode'], marker))
                self.assertIn('DONE', lines)
            differences = {(v['x'], v['min'], v['max'], v['native_result'], v['pyemuera_result'])
                           for v in row['observation']['vectors_and_results'] if v['native_result'] != v['pyemuera_result']}
            expected = {(8, 8, 4, 4, 8), (9, 8, 4, 4, 8)} if command == 'LIMIT' else set()
            self.assertEqual(differences, expected)

    def test_division_fault_diagnostics_are_observations_not_success(self):
        for command in ('LIMIT', 'INRANGE'):
            for slot in (1, 2, 3):
                row = self.cases[f'METHOD_BOUNDARY_{command}_{command}_FAULT_{slot}_20261115']
                self.assertEqual(row['observation']['condition']['faulting_helper_slot'], slot)
                modes = {mode['mode']: mode for mode in row['modes']}
                for observed in row['observation']['modes']:
                    mode = modes[observed['mode']]
                    native = observed['mode'].startswith('native-')
                    output = saved_text(mode, 'native_emuera_log' if native else 'public_process_stdout')
                    diagnostic = output if native else saved_text(mode, 'public_process_stderr')
                    for marker in observed['selected_helper_markers']:
                        self.assertIn(marker, output)
                    self.assertIn(observed['diagnostic_excerpt'], diagnostic)
                    self.assertFalse(observed['after_or_done_observed'])
                    self.assertNotIn('DONE', output.splitlines())

    def test_printvw_before_and_after_are_saved_history_lines(self):
        row = self.cases['PRINTVWPOSTWAITTRACE01']
        modes = {mode['mode']: mode for mode in row['modes']}
        for observed in row['observation']['modes']:
            role = 'native_emuera_log' if observed['mode'].startswith('native-') else 'public_emuera_log'
            lines = saved_text(modes[observed['mode']], role).splitlines()
            for selected in observed['selected_lines']:
                self.assertEqual(lines.count(selected), 1, (observed['mode'], selected))

if __name__ == '__main__':
    unittest.main()
