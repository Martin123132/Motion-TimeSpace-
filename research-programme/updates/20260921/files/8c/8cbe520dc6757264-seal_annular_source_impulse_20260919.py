from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import math
import re
import traceback


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-source-impulse-final-integrity.json'
    table = intake/'annular-Gram-energy-error-bounds.csv'
    snapshot = intake/'annular-source-impulse-resume-snapshot.md'
    executed = intake/'annular-source-impulse-executed-sealer.py'
    if any(path.exists() for path in [destination, table, snapshot, executed]):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False,
        subagents_used=False, full_GR_limit_proven=False, valid_for_physics_claim=False,
        full_live_P2_force_convergence_proven=False, no_new_finite_element_evolution=True,
        instantaneous_requirement_unchanged=True,
        protected_scan_scope='mtime since2026-09-19T06:39:11Z; not a pre-turn full hash baseline')
    cache = {}

    def digest(path):
        path = path.resolve()
        if path not in cache:
            hasher = hashlib.sha256()
            with path.open('rb') as stream:
                while chunk := stream.read(1024*1024):
                    hasher.update(chunk)
            cache[path] = hasher.hexdigest()
        return cache[path]

    def own(path, category='inputs'):
        report[category][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name, passed=bool(passed), detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(path):
        data = json.loads(path.read_text())
        for category in ['inputs', 'outputs']:
            for name, expected in data[category].items():
                source = (root/name).resolve()
                key = str(source.relative_to(root))
                if not source.is_file() or digest(source) != expected:
                    raise RuntimeError('Changed sealed source: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting sealed source: '+name)
                report['inputs'][key] = expected
        own(path)
        return data

    def no_claims(value):
        if isinstance(value, dict):
            return all(not item if name in ['valid_for_claim', 'valid_for_physics_claim', 'full_GR_limit_proven',
                'full_live_P2_force_convergence_proven'] else no_claims(item) for name, item in value.items())
        if isinstance(value, list):
            return all(no_claims(item) for item in value)
        return True

    save()
    try:
        previous = inherit(intake/'annular-P2-weighted-consistency-final-integrity.json')
        check('previous_checkpoint_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['total_failed_attempts_preserved'] == 40)
        names = ['annular-P2-saved-impulse-reference-attempt01', 'annular-P2-saved-impulse-MTS-attempt01',
            'annular-P2-saved-impulse-coarse16-reference-attempt01', 'annular-P2-saved-impulse-coarse16-MTS-attempt01',
            'annular-continuum-source-impulse-attempt01', 'annular-P2-Gram-energy-error-bound-attempt01',
            'annular-P2-source-impulse-comparison-attempt01']
        statuses = {}
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses[name] = status
            check(name+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            check(name+'_nonclaim_and_private', no_claims(status) and not status['github_action'] and not status['subagents_used'])
        failures = []
        for prefix in ['annular-P2-saved-impulse-', 'annular-continuum-source-impulse-',
                'annular-P2-Gram-energy-error-bound-', 'annular-P2-source-impulse-comparison-']:
            for path in sorted(intake.glob(prefix+'*/status.json')):
                if path.parent.name not in statuses:
                    failed = inherit(path)
                    check(path.parent.name+'_failed_execution_preserved', failed['state'] == 'failed')
                    failures.append(dict(folder=path.parent.name, error=failed['error']))
        comparison = statuses[names[-1]]
        oracle = statuses[names[-3]]
        energy = statuses[names[-2]]
        count = sum(len(status['checks']) for status in statuses.values())
        check('380_current_successful_implementation_checks', count == 380, count)
        check('fair_branch_space_time_and_quadrature_controls', len(comparison['cases']) == 96
            and len(comparison['refinements']) == 72 and comparison['original_instantaneous_force_requirement_unchanged']
            and comparison['finite_polynomial_family_not_a_weak_convergence_proof']
            and comparison['sampled_bounds_not_continuous_time_supremum_bounds'])
        check('independent_augmented_oracle_no_feedback', len(oracle['cases']) == 4
            and oracle['augmented_observables_do_not_feed_back'] and oracle['real_time_step_halving'])
        check('full_energy_bound_not_a_continuum_error_claim', len(energy['cases']) == 2
            and energy['current_full_scalar_energy_used'] and energy['fixed_geometry_field_only_bound']
            and energy['hierarchical_defects_not_known_continuum_error'])
        rows = []
        for branch in energy['cases']:
            for item in branch['cases']:
                rows.append(dict(branch=branch['branch'], kind=item['kind'],
                    energy_error=item['field_energy_norm'], dual_gain=item['force_energy_dual_gain'],
                    quadratic_bound=item['quadratic_operator_bound'], force_bound=item['energy_force_error_bound'],
                    measured_force_difference=item['measured_fixed_geometry_force_change'], valid_for_claim=False,
                    source_path=str((intake/names[-2]/'status.json').relative_to(root))))
        with table.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        with table.open(encoding='utf-8', newline='') as stream:
            parsed = list(csv.DictReader(stream))
        check('four_sourced_energy_rows_parse', len(parsed) == 4 and all(None not in row
            and row['valid_for_claim'] == 'False' and (root/row['source_path']).is_file()
            and all(math.isfinite(float(row[key])) for key in ['energy_error', 'dual_gain', 'quadratic_bound',
                'force_bound', 'measured_force_difference']) for row in parsed))
        own(table, 'outputs')
        with (intake/names[-1]/'matched-impulses.csv').open(encoding='utf-8', newline='') as stream:
            parsed = list(csv.DictReader(stream))
        check('96_sourced_impulse_rows_parse', len(parsed) == 96 and all(None not in row
            and row['valid_for_claim'] == 'False' and (root/row['source_path']).is_file() for row in parsed))
        note = root/'DERIVATION-20260919-source-impulse-and-force-energy-control.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('no_pending_results_or_false_GR_claim', 'Results will be entered' not in content
            and 'does not establish the full GR limit' in content and '13.58%' in content
            and 'not the unknown continuum error' in content)
        own(note)
        scripts = ['run_annular_P2_saved_impulse_20260919.py', 'run_annular_P2_saved_coarse_impulse_20260919.py',
            'run_annular_continuum_impulse_20260919.py', 'derive_annular_P2_Gram_energy_error_bound_20260919.py',
            'compare_annular_source_impulse_20260919.py', 'seal_annular_source_impulse_20260919.py']
        for name in scripts:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 19, 6, 39, 11, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            implementation_checks=count, total_failed_attempts_preserved=40+len(failures),
            new_failed_executions=len(failures), new_failures=failures,
            inherited_scientific_failures_unchanged=True, distinct_files_rehashed=len(cache),
            full_interval_retested=False, impulse_rows=96, energy_rows=4, refinement_rows=72)
        save()
        print(json.dumps(dict(state='complete', implementation_checks=count, integrity_checks=len(report['checks']),
            files_rehashed=len(cache), failed_attempts_preserved=40+len(failures), impulse_rows=96, energy_rows=4)), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
