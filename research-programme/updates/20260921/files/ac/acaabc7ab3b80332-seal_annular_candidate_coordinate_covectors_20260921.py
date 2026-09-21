from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_mixed_weak_maps_20260920 import MixedMap
from decimal import Decimal, localcontext
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import re
import traceback
import numpy as np
import sympy as sp


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    prefix = 'annular-candidate-coordinate-covectors'
    destination = intake/(prefix+'-final-integrity.json')
    snapshot = intake/(prefix+'-resume-snapshot.md')
    executed = intake/(prefix+'-executed-sealer.py')
    specifications = [('cases', 'force', 'cases', 6), ('derivatives', 'force', 'derivative_controls', 90),
        ('quadrature', 'force', 'quadrature', 18), ('arithmetic', 'force', 'arithmetic', 3),
        ('envelope', 'envelope', 'comparisons', 9), ('envelope-differences', 'envelope', 'finite_differences', 27),
        ('gravity-runs', 'envelope', 'cases', 54)]
    tables = [intake/(prefix+'-'+label+'.csv') for label, unused, unused_key, unused_count in specifications]
    if any(path.exists() for path in [destination, snapshot, executed]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', inputs={}, outputs={}, checks=[], github_action=False, subagents_used=False,
        candidate_only=True, polar_zero_shift_only=True, no_new_evolution=True, new_coupled_evolution=False,
        full_GR_limit_proven=False, valid_for_physics_claim=False, modes_deleted=False,
        exact_finite_label_Galerkin_evolution_qualified=False, physical_force_mismatch_fixed=False,
        general_nonzero_shift_or_temporal_current_derived=False, spatial_convergence_proven=False,
        full_live_P2_force_convergence_proven=False,
        protected_scan_scope='mtime since2026-09-20T23:20:19Z; not a pre-turn whole-tree hash baseline')
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
                    raise RuntimeError('Changed sealed input: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting sealed input: '+name)
                report['inputs'][key] = expected
        own(path)
        return data

    save()
    try:
        prior = inherit(intake/'annular-candidate-full-canonical-inverse-final-integrity.json')
        check('full_inverse_evidence_unchanged', prior['state'] == 'complete'
            and all(row['passed'] for row in prior['checks']) and prior['full_canonical_inverse_qualified'])
        paths = {'force':intake/'annular-candidate-coordinate-covectors-attempt01/status.json',
            'envelope':intake/'annular-candidate-coordinate-envelope-attempt01/status.json'}
        runs = {key:inherit(path) for key, path in paths.items()}
        for key, status in runs.items():
            check(key+'_execution_complete_and_all_implementation_checks_pass', status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']))
            check(key+'_private_conditional_nonclaim_scope', status['candidate_only'] and status['polar_zero_shift_only']
                and status['no_new_evolution'] and status['original_live_action_unchanged']
                and not status['github_action'] and not status['subagents_used'] and not status['new_coupled_evolution']
                and not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['physical_force_mismatch_fixed'] and not status['spatial_convergence_proven']
                and not status['full_live_P2_force_convergence_proven']
                and not status['general_nonzero_shift_or_temporal_current_derived'] and not status['modes_deleted']
                and not status['exact_finite_label_Galerkin_evolution_qualified'])
        force, envelope = runs['force'], runs['envelope']
        expected = {(branch, extension, reference_order, material_order)
            for branch, extension in [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]
            for reference_order, material_order in [(10, 32), (16, 48)]}
        check('all_branches_and_equal_force_controls', len(force['cases']) == 6
            and {(row['branch'], row['extension'], row['reference_order'], row['material_order'])
                for row in force['cases']} == expected
            and all(row['full_components'] == 16425 and row['minimum_F'] > 0 and row['maximum_speed_ratio'] < 1
                for row in force['cases']))
        check('all_coordinate_derivatives_and_negative_controls', force['full_coordinate_covectors_computed']
            and force['independent_coordinate_derivatives_qualified'] and len(force['derivative_controls']) == 90
            and all(row['passed'] for row in force['derivative_controls'])
            and all(row['omitted_metric_terms_relative_discrepancy'] > 1e-4 for row in force['cases']))
        check('quadrature_gate_matches_actual_rows_not_spatial_claim', len(force['quadrature']) == 18
            and force['quadrature_qualified'] == all(row['passed'] for row in force['quadrature'])
            and all(not row['spatial_convergence_test'] for row in force['quadrature']))
        check('arithmetic_controls_are_not_physical_precision_claims', len(force['arithmetic']) == 3
            and all(row['transpose_40_64_digit_relative_difference'] < 1e-20
                and row['original_binary_inputs_not_64_digit_physical_accuracy'] for row in force['arithmetic']))
        report['unrounded_transpose_precision_checks'] = []
        for branch, extension in [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]:
            case = branch+'-'+extension
            packet_path = intake/'annular-complete-frozen-candidate-attempt01'/(case+'-action.json')
            vector_path = paths['force'].parent/(case+'-16-48-covectors.npz')
            own(packet_path)
            own(vector_path)
            packet = json.loads(packet_path.read_text())['gram_factor']
            factor = MixedMap(packet['rows'], packet['columns'])
            with np.load(vector_path, allow_pickle=False) as data:
                moments = np.array([[Decimal(value) for value in row] for row in data['gram_moments']])
                moments = moments.reshape(factor.shape[0], 15)
                expected = np.array([[Decimal(value) for value in row] for row in data['gram_decimal'][:-1]])
            with localcontext() as context:
                context.prec = 40
                lower = -factor.apply(moments, transpose=True)
            with localcontext() as context:
                context.prec = 64
                higher = -factor.apply(moments, transpose=True)
                error = max(abs(lower-higher).ravel())/max(max(abs(higher).ravel()), Decimal('1e-90'))
                exact_recovery = bool(np.all(higher == expected))
            row = dict(branch=branch, extension=extension, relative_difference_before_float_rounding=str(error),
                saved_decimal_vector_exactly_recovered=exact_recovery, valid_for_claim=False)
            report['unrounded_transpose_precision_checks'].append(row)
            check(case+'_unrounded_40_64_digit_transpose_and_exact_recovery', error < Decimal('1e-20')
                and exact_recovery, row)
        check('independent_moving_support_full_action_test_recorded', envelope['on_shell_coordinate_envelope_numerically_tested']
            and envelope['fixed_rates_under_coordinate_variation'] and envelope['source_support_and_radial_edges_rebuilt']
            and len(envelope['cases']) == 54 and all(row['residual'] < 2e-12 for row in envelope['cases'])
            and len(envelope['finite_differences']) == 27 and len(envelope['comparisons']) == 9)
        check('envelope_gate_matches_actual_comparisons', envelope['coordinate_envelope_qualified']
            == all(row['passed'] for row in envelope['comparisons'])
            and all(row['directional_test_not_global_stationarity_theorem'] for row in envelope['comparisons']))
        step = sp.symbols('step', positive=True)
        mass = sp.Matrix([[2, sp.Rational(1, 3)], [sp.Rational(1, 3), 3]])
        stiffness = sp.Matrix([[5, sp.Rational(1, 2)], [sp.Rational(1, 2), 7]])
        transport = sp.Matrix([[1, 2], [-3, 4]])
        coordinates = sp.Matrix(sp.symbols('q0:2'))
        velocities = sp.Matrix(sp.symbols('v0:2'))
        momentum = sp.Matrix(sp.symbols('p0:2'))
        midpoint = coordinates+step*velocities/2
        residual = mass*velocities+transport*midpoint-momentum-step*(transport.T*velocities-stiffness*midpoint)/2
        expected = mass+step*(transport-transport.T)/2+step**2*stiffness/4
        check('midpoint_reduced_velocity_residual_jacobian_identity', residual.jacobian(velocities).applyfunc(sp.expand)
            == expected.applyfunc(sp.expand))
        check('midpoint_gyroscopic_term_is_skew_not_discarded', (expected+expected.T)/2
            == mass+step**2*stiffness/4 and transport != transport.T)
        counts = []
        for path, (label, run, key, expected_count) in zip(tables, specifications):
            rows = [dict(**row, source_path=str(paths[run].relative_to(root))) for row in runs[run][key]]
            fields = list(dict.fromkeys(field for row in rows for field in row))
            with path.open('w', encoding='utf-8', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            with path.open(encoding='utf-8', newline='') as stream:
                parsed = list(csv.DictReader(stream))
            check(label+'_sourced_nonclaim_CSV_rows_parse', len(parsed) == expected_count
                and all(None not in row and None not in row.values() and row['valid_for_claim'] == 'False'
                    and (root/row['source_path']).is_file() for row in parsed))
            counts.append(len(parsed))
            own(path, 'outputs')
        note = root/'DERIVATION-20260921-action-owned-coordinate-covectors.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv|npz))`', content)
        check('completed_report_and_all_cited_sources_exist', 'RESULTS_PENDING' not in content and bool(cited)
            and all((root/name).is_file() for name in cited), cited)
        for name in cited:
            own(root/name)
        own(note)
        for name in ['annular_candidate_coordinate_covectors_20260921.py',
                'derive_annular_candidate_coordinate_covectors_20260921.py',
                'derive_annular_candidate_coordinate_envelope_20260921.py',
                'seal_annular_candidate_coordinate_covectors_20260921.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('all_new_scripts_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 20, 23, 20, 19, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= start]
        check('protected_workbench_mtime_unchanged', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            implementation_checks={key:len(status['checks']) for key, status in runs.items()},
            total_failed_attempts_preserved=prior['total_failed_attempts_preserved'], new_failures=[],
            distinct_files_rehashed=len(cache), table_rows=counts, full_coordinate_covectors_computed=True,
            independent_coordinate_derivatives_qualified=True, quadrature_qualified=force['quadrature_qualified'],
            coordinate_envelope_qualified=envelope['coordinate_envelope_qualified'],
            on_shell_scope='Three native coordinate directions with re-solved gravity, finite-difference refinement and all three branches; not an exact finite-dimensional stationarity theorem.',
            next_target='If the coordinate-envelope gate passes, implement a precision-preserving short canonical source/field/gravity trajectory with a justified local step and equal reference/MTS step-refinement controls. The old frozen scalar frequency bound is not a bound on the full coupled Jacobian. If the gate fails, resolve the measured on-shell discrepancy first. No physical acceleration, spatial-convergence or full-GR claim from coordinate covectors alone.')
        save()
        print(json.dumps(dict(state='complete', implementation_checks=report['implementation_checks'],
            integrity_checks=len(report['checks']), files_rehashed=len(cache), table_rows=counts,
            envelope_qualified=report['coordinate_envelope_qualified'], failures_preserved=report['total_failed_attempts_preserved'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
