from pathlib import Path
from datetime import datetime, timezone
import csv
import ctypes
import hashlib
import json
import re


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << 2):
        raise OSError('Affinity failed')
    root = Path(__file__).resolve().parents[1]
    directory = root / 'source-intake/navier-stokes/20260914'
    target = directory / 'annular-live-refinement-time-jet-integrity-20261002.json'
    if target.exists():
        raise FileExistsError(target)
    hashes, mismatches, authorities = {}, [], {}
    def verify(relative, expected=None):
        path = (root / relative).resolve()
        if path == root / 'CURRENT_LOCAL_RESUME.md':
            return
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Invalid integrity path ' + str(relative))
        key = str(path.relative_to(root))
        if key not in hashes:
            hashes[key] = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and hashes[key] != expected:
            mismatches.append(key)
    parent_path = directory / 'annular-quadratic-transmission-integrity-20261002.json'
    parent = json.loads(parent_path.read_text())
    if parent['state'] != 'complete' or parent['mismatches']:
        raise RuntimeError('Incomplete parent')
    verify(parent_path.relative_to(root))
    for relative, expected in parent['hashes'].items():
        verify(relative, expected)
    failures = {
        'annular-live-native-transmission-fourth-primary-attempt01': 'same_old_field_and_source',
        'annular-live-native-transmission-fourth-reference-attempt01': 'same_old_field_and_source',
        'annular-live-native-transmission-fourth-primary-attempt02': 'ConversionSyntax',
        'annular-native-curvature-repair-attempt01': 'source_value_retained',
    }
    names = list(failures) + ['annular-live-native-transmission-fourth-primary-attempt03',
        'annular-live-native-transmission-fourth-reference-attempt03', 'annular-moving-native-transmission-algebra-attempt01',
        'annular-live-transmission-time-jet-third-attempt01', 'annular-live-transmission-time-jet-fourth-attempt01',
        'annular-native-curvature-repair-attempt02',
        'annular-live-refinement-time-jet-analysis-attempt01']
    for name in names:
        path = directory / name / 'status.json'
        report = json.loads(path.read_text())
        if name in failures:
            if report['state'] != 'failed' or failures[name] not in report['error']:
                raise RuntimeError('Unexpected retained failure ' + name)
            failed = [row['name'] for row in report['checks'] if not row['passed']]
            expected_failed = [] if name.endswith('attempt02') else ['same_old_field_and_source']
            if name == 'annular-native-curvature-repair-attempt01':
                expected_failed = ['third:-0.5:source_value_retained']
            if failed != expected_failed:
                raise RuntimeError('Changed original failure ' + name)
        elif report['state'] != 'complete' or not report['checks'] or not all(row['passed'] for row in report['checks']):
            raise RuntimeError('Incomplete authority ' + name)
        verify(path.relative_to(root))
        for category in ['inputs', 'outputs']:
            for relative, expected in report[category].items():
                verify(relative, expected)
        for member in path.parent.iterdir():
            if member.is_file():
                verify(member.relative_to(root))
        authorities[name] = dict(state=report['state'], checks=len(report['checks']), passed_checks=sum(row['passed'] for row in report['checks']))
    scripts = ['annular_live_transmission_system_20261002.py', 'annular_live_transmission_system_v2_20261002.py',
        'refine_annular_live_transmission_20261002.py', 'refine_annular_live_transmission_v2_20261002.py',
        'refine_annular_live_transmission_v3_20261002.py', 'probe_annular_live_time_jet_20261002.py',
        'verify_annular_moving_transmission_20261002.py', 'analyze_annular_live_refinement_20261002.py',
        'construct_annular_native_curvature_repair_20261002.py', 'construct_annular_native_curvature_repair_v2_20261002.py',
        'seal_annular_live_refinement_20261002.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_text(), str(path), 'exec')
        verify(path.relative_to(root))
    citations = []
    for name in ['DERIVATION-20261002-fixed-profile-native-refinement.md', 'DERIVATION-20261002-live-transmission-time-jet.md',
        'DERIVATION-20261002-moving-native-transmission-and-third-jets.md', 'DERIVATION-20261002-native-curvature-corner-repair.md',
        'DERIVATION-20261002-quintic-source-anchor-lift.md', 'RESULTS-20261002-live-refinement-and-preservation.md']:
        verify(name)
        for relative in re.findall(r'`([^`]+\.(?:md|py|json|npz|csv))`', (root / name).read_text()):
            verify(relative)
            citations.append(relative)
    csv_count = 0
    for path in (directory / names[-1]).glob('*.csv'):
        with path.open(encoding='utf-8', newline='') as stream:
            rows = list(csv.DictReader(stream))
        if any(None in row or any(value is None for value in row.values()) or row['valid_for_claim'] != 'False' for row in rows):
            raise RuntimeError('Malformed CSV ' + str(path))
        csv_count += len(rows)
    if csv_count != 10:
        raise RuntimeError('Unexpected CSV row count ' + str(csv_count))
    start = datetime(2026, 10, 2, 21, 36, 47, tzinfo=timezone.utc).timestamp()
    protected = root.parent / 'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
    bytecode = list((root / 'scripts').rglob('__pycache__'))
    if mismatches or changed or bytecode:
        raise RuntimeError(dict(mismatches=mismatches, protected_changes=changed, bytecode=list(map(str, bytecode))))
    analysis = json.loads((directory / names[-1] / 'status.json').read_text())
    result = dict(state='complete', sealed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes, mismatches=mismatches,
        unique_files_rehashed=len(hashes), authorities=authorities, scripts_compiled=scripts, csv_rows_parsed=csv_count,
        cited_local_paths_validated=sorted(set(citations)), refinement=analysis['refinement_rows'],
        time_jet_witnesses=analysis['time_jet_witnesses'], time_jet_grid_comparison=analysis['time_jet_grid_comparison'],
        frozen_curvature_repair=analysis['frozen_curvature_repair'],
        moving_transmission_derived=True, independent_third_jet_lift_derived=True, higher_jet_repair_solved=False,
        physical_trajectory_computed=False, continuous_material_bound_proven=False, valid_for_physics_claim=False,
        retained_failure_reason='Pre-solve decoder failures retained. First quintic also failed its separate source-value gate; daughter imposes an exact seventh interpolation condition with a degree-six endpoint-jet-null lift, not a relaxed tolerance.',
        protected_workbench_changed_since_turn_start=0, bytecode_cache_present=False, pending={}, current_resume_excluded=True,
        github_action=False, subagents_used=False)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(state='complete', files=len(hashes), mismatches=len(mismatches), scripts=len(scripts),
        csv_rows=csv_count, passed_checks=sum(row['passed_checks'] for row in authorities.values()), protected_changes=0)), flush=True)


if __name__ == '__main__':
    main()
