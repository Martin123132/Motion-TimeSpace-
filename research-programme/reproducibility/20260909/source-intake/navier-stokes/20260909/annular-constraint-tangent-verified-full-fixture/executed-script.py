import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis, real_linear
    from annular_adm_clock_quadratic_20260909 import LocalQuadraticPath
    from annular_constraint_routhian_20260909 import ConstraintRouthian

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    source = intake / 'annular-constraint-routhian-derived'
    destination = intake / 'annular-constraint-tangent-verified-full-fixture'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'scope': 'Independent nonlinear root-family differentiation and full shift-variation checks at corrected local initial data. Retains all nonzero mass-flux/constraint-tangent residuals. Root families are parameter probes, not time evolution; grid trends are measured, not a continuum error certificate.'}
    (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')

    def own(path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        report['inputs'][str(path.relative_to(root))] = digest
        return digest

    def verify(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        print(name + ': ' + str(bool(passed)), flush=True)

    def maximum(value):
        return float(numerical.max(numerical.abs(value)))

    save()
    try:
        prior_path = source / 'status.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        verify('initial_constraint_owner_complete', prior['state'] == 'complete' and prior['passed'] == prior['total'])
        verify('initial_constraint_sources_and_roots_unchanged', all(own(root / name) == digest for name, digest in {**prior['inputs'], **prior['outputs']}.items()))
        failed_path = intake / 'annular-constraint-tangent-verified/status.json'
        own(failed_path)
        failed = json.loads(failed_path.read_text())
        failed_script = failed_path.parent / 'executed-script.py'
        verify('earlier_checker_source_snapshot_preserved', own(failed_script) == failed['inputs'][str(Path(__file__).relative_to(root))])
        failed_checks = [check for check in failed['checks'] if not check['passed']]
        verify('earlier_failure_is_full_dictionary_vs_four_parameter_subset_only', len(failed_checks) == 12 and all(check['name'].endswith('_fixture_constants_loaded_not_guessed') for check in failed_checks))
        own(Path(__file__))
        compile(Path(__file__).read_bytes(), str(Path(__file__)), 'exec')
        for sample in prior['samples']:
            case_name, intervals, branch = sample['case'], sample['intervals'], sample['branch']
            include_gram = branch == 'Gram'
            tag = case_name + '_N' + str(intervals) + '_' + branch
            report['active_job'] = tag
            save()
            case = json.loads((intake / 'annular-constraint-correction-initial' / (case_name + '.json')).read_text())
            with numerical.load(source / (tag + '.npz')) as loaded:
                arrays = {name: loaded[name].copy() for name in loaded.files}
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            from annular_adm_mixed_action_20260909 import OrthogonalReference

            reference = OrthogonalReference(case)
            verify(tag + '_fixture_constants_loaded_not_guessed', reference.constants == constants)
            constants = reference.constants
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            basis = MixedActionBasis(arrays['radius'])
            system = ConstraintRouthian(basis, arrays['scalar'], arrays['defect'], arrays['defect_time'], constants, kappa, arrays['momentum'], arrays['outer_clock'][0])
            corrected, speed = arrays['corrected'], arrays['packed_speed']
            scaling = (arrays['unknown_scale'], arrays['row_scale'])
            differences = []
            for step in [0.001, 0.0005]:
                roots = []
                for sign in [-1, 1]:
                    time = sign * step
                    changed_system = ConstraintRouthian(basis, arrays['scalar'] + time * corrected[system.slices[2]], arrays['defect'] + time * arrays['defect_time'], arrays['defect_time'] + time * arrays['defect_acceleration'], constants, kappa, arrays['momentum'] + time * arrays['momentum_speed'], arrays['outer_clock'][0] + time * arrays['outer_clock'][1])
                    seed = corrected.copy()
                    seed[system.fixed] += time * speed[system.fixed]
                    changed_root, history, solved, reason = changed_system.solve(seed, include_gram, scaling, tolerance=2e-14)
                    roots.append(changed_root)
                    verify(tag + '_independent_neighbor_root_' + str(time), solved, {'reason': reason, 'steps': len(history) - 1})
                measured = (roots[1] - roots[0]) / (2 * step)
                error = maximum(measured - speed)
                differences.append(error)
                verify(tag + '_nonlinear_root_family_derivative_' + str(step), error < 2e-7, {'maximum_error': error, 'maximum_tangent': maximum(speed)})
            mass_slice, lapse_slice, velocity_slice = system.slices
            fields = [arrays['scalar'], corrected[mass_slice], corrected[lapse_slice], numerical.zeros(system.face_count)]
            velocities = [corrected[velocity_slice], speed[mass_slice], speed[lapse_slice], numerical.zeros(system.face_count)]
            probe = 0.02 * numerical.sin(23 * basis.faces)
            changed = [value.astype(complex) for value in fields]
            changed[3] += 1j * 1e-25 * probe
            bulk_variation = basis.action(changed, velocities, arrays['defect'], arrays['defect_time'], constants, kappa).imag / 1e-25
            expected_bulk = numerical.dot(real_linear(arrays['pairing'], speed[mass_slice]) + arrays['matter_shift'], probe)
            verify(tag + '_independent_full_ADM_matter_shift_variation', abs(bulk_variation - expected_bulk) < 1e-14)
            mismatch = speed[mass_slice] - arrays['shift_mass_speed']
            verify(tag + '_exact_retained_shift_residual_equals_B_mass_rate_mismatch', maximum(arrays['shift_residual'] - real_linear(arrays['pairing'], mismatch)) < 1e-15)
            frozen = speed.copy()
            frozen[lapse_slice] = 0
            frozen_residual = (real_linear(arrays['Hessian_final'], frozen) + arrays['data_derivative'])[system.free]
            verify(tag + '_frozen_lapse_negative_control_fails_constraint_preservation', maximum(frozen_residual) > 100 * max(maximum(arrays['constraint_derivative_residual']), 1e-14))

            if include_gram and intervals == 16:
                nodal = {'scalar': arrays['scalar'], 'scalar_time': corrected[velocity_slice], 'scalar_second': speed[velocity_slice], 'lapse': corrected[lapse_slice], 'lapse_time': speed[lapse_slice], 'gradient': real_linear(basis.derivative, arrays['scalar']) + arrays['defect'], 'gradient_time': real_linear(basis.derivative, corrected[velocity_slice]) + arrays['defect_time']}
                facial = {'mass': corrected[mass_slice], 'mass_time': speed[mass_slice]}
                path = LocalQuadraticPath(basis, nodal, facial, constants)
                displacement = [numerical.zeros_like(value) for value in fields]
                displacement[3] = probe
                zero_speed = [numerical.zeros_like(value) for value in fields]

                def time_boundary(time):
                    scalar, unused_velocity, coefficient, unused_coefficient_time, unused_first, unused_second, unused_perturbation, unused_speed, link, unused_link_time, unused_second_link = path.components(time, displacement, zero_speed)
                    leading = path.links.collect(path.links.tweight * scalar[path.links.node])
                    return numerical.dot(leading**2 / (2 * basis.spacing), path.links.collect(path.links.sweight * coefficient[path.links.node] * link))

                boundary_rate = time_boundary(1j * 1e-25).imag / 1e-25
                reduced = numerical.dot(arrays['Gram_shift'], probe)
                for amplitude in [0.001, 0.0005]:
                    raw = (path.exact_potential(0.0, displacement, zero_speed, amplitude) - path.exact_potential(0.0, displacement, zero_speed, -amplitude)) / (2 * amplitude)
                    verify(tag + '_independent_full_link_shift_after_time_boundary_' + str(amplitude), abs(raw - boundary_rate - reduced) < 2e-4 * max(abs(raw), abs(boundary_rate), abs(reduced), 1e-25) + 1e-15, {'raw': float(raw), 'boundary_rate': float(boundary_rate), 'reduced': float(reduced)})

            peak = int(numerical.argmax(numerical.abs(mismatch)))
            interior = (basis.faces > 5.90) & (basis.faces < 6.10)
            report['samples'].append({'case': case_name, 'intervals': intervals, 'branch': branch, 'nonlinear_root_family_derivative_errors': differences, 'mass_rate_mismatch_max': maximum(mismatch), 'mass_rate_mismatch_relative_to_flux_max': maximum(mismatch) / maximum(arrays['shift_mass_speed']), 'mass_rate_mismatch_interior_max': maximum(mismatch[interior]), 'peak_mass_rate_mismatch_radius': float(basis.faces[peak]), 'shift_weak_residual_max': maximum(arrays['shift_residual']), 'frozen_lapse_constraint_derivative_max': maximum(frozen_residual), 'lapse_rate_max': maximum(speed[lapse_slice]), 'all_shift_rows_closed': maximum(arrays['shift_residual']) < 1e-10, 'valid_for_physics_claim': False})
            save()

        trends = []
        for case_name in ['canonical', 'nonlinear_modulated']:
            for branch in ['GR', 'Gram']:
                samples = [sample for sample in report['samples'] if sample['case'] == case_name and sample['branch'] == branch]
                errors = [sample['mass_rate_mismatch_max'] for sample in samples]
                trends.append({'case': case_name, 'branch': branch, 'intervals': [sample['intervals'] for sample in samples], 'mass_rate_mismatch_max': errors, 'observed_adjacent_orders': [float(numerical.log2(first / second)) for first, second in zip(errors[:-1], errors[1:])], 'uniform_error_bound_derived': False})
                verify(case_name + '_' + branch + '_measured_mass_rate_mismatch_decreases_on_three_grids', all(first > second > 0 for first, second in zip(errors[:-1], errors[1:])))
        report['refinement'] = trends
        verify('all_inherited_roots_sources_and_checks_unchanged', all(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest for name, digest in report['inputs'].items()))
        verify('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
        report.update(passed=sum(check['passed'] for check in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
        report['state'] = 'complete' if report['passed'] == report['total'] else 'failed'
        save()
    except Exception as error:
        report.update(state='failed', failure=repr(error), completed_utc=datetime.now(timezone.utc).isoformat())
        save()
        raise
    print(json.dumps({key: report[key] for key in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
    if report['state'] != 'complete':
        raise SystemExit(1)
    (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')


if __name__ == '__main__':
    run()
