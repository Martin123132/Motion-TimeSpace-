from pathlib import Path
from datetime import datetime, timezone
from time import monotonic, sleep
import json
import os
import subprocess
import sys
import psutil


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260914'
    output = intake / 'annular-position-time-background-workflow'
    output.mkdir(exist_ok=False)
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([0])
    state = dict(state='waiting', pid=os.getpid(), started_at=datetime.now(timezone.utc).isoformat(),
        original_parent='annular-position-time-radial-attempt04', actual_parent=None,
        validator='annular-position-time-radial-validation-attempt01', github_action=False,
        subagents_used=False, numerical_workers=1)
    deadline = monotonic() + 10800

    def save(**values):
        state.update(values)
        (output / 'status.json').write_text(json.dumps(state, indent=2) + '\n', encoding='utf-8')

    def read_status(name):
        try:
            return json.loads((intake / name / 'status.json').read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def wait_status(name):
        while monotonic() < deadline:
            data = read_status(name)
            if data and data['state'] in ['complete', 'failed']:
                return data
            sleep(15)
        raise RuntimeError('Background workflow safety deadline')

    def execute(script, arguments, label):
        save(state='running', stage=label)
        with (intake / (label + '.log')).open('x', encoding='utf-8') as stream:
            result = subprocess.run([sys.executable, '-B', str(root / 'scripts' / script), *arguments],
                cwd=root, stdout=stream, stderr=subprocess.STDOUT, check=False)
        if result.returncode:
            raise RuntimeError('Child calculation stopped; inspect ' + label)

    save(stage='waiting_for_current_radial_calculation')
    try:
        parent = wait_status(state['original_parent'])
        if parent['state'] == 'failed':
            safe_errors = ['Safe mixed Eulerian density boundary', 'Safe radial position-time boundary']
            if not any(message in parent.get('error', '') for message in safe_errors):
                raise RuntimeError('Parent stopped on a non-time-limit failure; no automatic retry')
            actual = 'annular-position-time-radial-attempt05'
            save(actual_parent=actual, stage='resuming_saved_density_blocks')
            execute('derive_annular_position_time_radial_v5_20260929.py',
                ['--resume', state['original_parent'], '--max-seconds', '2700'], actual)
            execute('validate_annular_position_time_radial_20260929.py',
                ['--parent', actual, '--max-seconds', '1200'], state['validator'])
        else:
            save(actual_parent=state['original_parent'], stage='waiting_for_existing_final_validator')
        validator = wait_status(state['validator'])
        if validator['state'] != 'complete' or len(validator['cases']) != 4 or not all(row['passed'] for row in validator['checks']):
            raise RuntimeError('Final validator did not complete successfully')
        save(state='complete', stage='ready_for_review_and_integrity_seal',
            completed_at=datetime.now(timezone.utc).isoformat())
        (output / 'COMPLETE').write_text('Calculations complete; read authorities and seal before advancing.\n', encoding='utf-8')
    except BaseException as error:
        save(state='failed', error=repr(error), completed_at=datetime.now(timezone.utc).isoformat())
        (output / 'FAILED').write_text(repr(error) + '\n', encoding='utf-8')
        raise


if __name__ == '__main__':
    main()
