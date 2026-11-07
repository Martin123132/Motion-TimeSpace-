from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260914'
    hashes, authorities, tables = {}, {}, {}
    names = ['annular-position-time-loads-attempt01', 'annular-position-time-load-validation-attempt01',
        'annular-position-time-probe-attempt02', 'annular-position-time-radial-attempt03']
    for name in names:
        status_path = intake / name / 'status.json'
        status = json.loads(status_path.read_text())
        expected_cases = 3 if name.endswith('radial-attempt03') else 4
        if len(status['cases']) != expected_cases or not all(row['passed'] for row in status['checks']):
            raise RuntimeError('Incomplete saved authority: ' + name)
        if expected_cases == 3:
            if not status.get('external_safe_boundary_stop') or status.get('numerical_failure') is not False:
                raise RuntimeError('Not a controlled completed-case handoff')
        elif status['state'] != 'complete':
            raise RuntimeError('Authority not complete')
        hashes[str(status_path.relative_to(root))] = hashlib.sha256(status_path.read_bytes()).hexdigest()
        authorities[name] = dict(cases=expected_cases, computational_checks=len(status['checks']), state=status['state'])
        for relative, expected in status['outputs'].items():
            path = root / relative
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if expected != actual:
                raise RuntimeError('Changed saved output: ' + relative)
            hashes[relative] = actual
            if path.suffix == '.csv':
                with path.open(encoding='utf-8', newline='') as stream:
                    rows = list(csv.DictReader(stream))
                if not rows or any(None in row or any(value is None for value in row.values()) for row in rows):
                    raise RuntimeError('Malformed CSV: ' + relative)
                if any(row.get('valid_for_claim', 'False') != 'False' for row in rows):
                    raise RuntimeError('Unexpected physics claim')
                tables[relative] = len(rows)
    scripts = list((root / 'scripts').glob('*position_time*20260929.py'))
    documents = list(root.glob('DERIVATION-20260929-position-*.md'))
    documents += [root / 'CURRENT_LOCAL_RESUME.md', root / 'RESULTS-20260929-position-time-loading-and-metric-response.md']
    for path in scripts + documents:
        if path.suffix == '.py':
            compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        hashes[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    since = datetime.fromisoformat('2026-09-29T00:59:30+00:00').timestamp()
    protected = [str(path) for path in (root.parent / 'formalization-workbench').rglob('*')
        if path.is_file() and path.stat().st_mtime >= since]
    if protected or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected-workbench or bytecode guard failed')
    workflow = json.loads((intake / 'annular-position-time-background-workflow/status.json').read_text())
    active = json.loads((intake / 'annular-position-time-radial-attempt04/status.json').read_text())
    report = dict(state='completed_handoff_validation', timestamp=datetime.now(timezone.utc).isoformat(),
        hashes=hashes, authorities=authorities, tables=tables, csv_rows=sum(tables.values()),
        scripts_compiled=len(scripts), immutable_outputs_rehashed=True, final_four_case_radial_seal=False,
        B0_completed_cases=3, pending=['MTS third radial calculation', 'four-case off-grid radial validation', 'final integrity seal'],
        workflow_state_at_handoff=workflow['state'], numerical_state_at_handoff=active['state'],
        last_progress=active.get('progress'), protected_workbench_changed_since_turn_start=0,
        bytecode_cache_present=False, github_action=False, subagents_used=False)
    path = intake / 'annular-position-time-handoff-integrity-20260929.json'
    with path.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'hashes'}))


if __name__ == '__main__':
    main()
