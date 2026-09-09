import argparse
import hashlib
import json
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from scipy.linalg import eigvalsh
    from annular_adm_mixed_action_20260909 import MixedActionBasis, real_linear
    from annular_action_boundary_current_20260909 import boundary_balance, gram_current
    from annular_boundary_ramp_bound_20260909 import affine_link_bound
    from annular_local_ward_identity_20260909 import LocalWardIdentity
    from annular_mass_trace_remainder_bound_20260909 import affine_bulk_remainder_bound, affine_gram_coefficient_bound, mass_trace_bound, metric_cell_bounds
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-mass-trace-remainder-bound-derived'
    final_path = intake / 'annular-mass-trace-final-integrity.json'
    inputs, outputs = {}, {}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path):
        inputs[str(path.relative_to(root))] = digest(path)

    def artifact(path):
        outputs[str(path.relative_to(root))] = digest(path)

    def inherit(table, inherited):
        for name, expected in inherited.items():
            actual = digest(root / name)
            if actual != expected or name in table and table[name] != actual:
                raise RuntimeError('Changed evidence: ' + name)
            table[name] = actual

    def load_arrays(path):
        own(path)
        with numerical.load(path) as loaded:
            return {name: loaded[name].copy() for name in loaded.files}

    def maximum(value):
        return float(numerical.max(numerical.abs(value)))

    prior_path = intake / 'annular-boundary-current-final-integrity.json'
    prior = json.loads(prior_path.read_text())
    if prior['state'] != 'complete':
        raise RuntimeError('Previous boundary checkpoint incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    scripts = ['annular_mass_trace_remainder_bound_20260909.py', 'derive_annular_mass_trace_bound_20260909.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'energy_counterexamples': [], 'valid_for_physics_claim': False, 'scope': 'Derive physical mass-pairing trace control and exact affine bulk commutators on unchanged saved GR/MTS states. No new trajectories, refits or boundary adjustments. Uniform estimates remain conditional on stated norms.'}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        class CurrentWard(LocalWardIdentity):
            def connection_transport(self):
                system, packed = self.system, self.arrays['corrected']
                return system.links.matrix(packed[system.slices[0]], packed[system.slices[1]], system.constants)

        save()
        try:
            position, width, left_value, slope, first, second, third, fourth = symbolic.symbols('position width left_value slope first second third fourth', real=True)
            linear = left_value + slope * position
            product = position * linear
            interpolated = position / width * product.subs(position, width)
            check('symbolic_P1_affine_product_error', symbolic.expand(interpolated - product - slope * position * (width - position)) == 0)
            cubic = first + second * position + third * position**2 + fourth * position**3
            quartic = position * cubic
            fraction = position / width
            hermite = (2 * fraction**3 - 3 * fraction**2 + 1) * quartic.subs(position, 0) + (-2 * fraction**3 + 3 * fraction**2) * quartic.subs(position, width)
            hermite += width * (fraction**3 - 2 * fraction**2 + fraction) * symbolic.diff(quartic, position).subs(position, 0)
            hermite += width * (fraction**3 - fraction**2) * symbolic.diff(quartic, position).subs(position, width)
            check('symbolic_Hermite_affine_product_error', symbolic.simplify(hermite - quartic + fourth * position**2 * (position - width)**2) == 0)
            check('symbolic_mass_derivative_zero_cell_moment', symbolic.integrate(symbolic.diff(slope * position * (width - position), position), (position, 0, width)) == 0)
            for case_name in ['canonical', 'nonlinear_modulated']:
                case_path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
                own(case_path)
                case = json.loads(case_path.read_text())
                constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
                kappa = float(symbolic.sympify(case['normalization_kappa']))
                for intervals in [16, 32, 64]:
                    for branch in ['GR', 'metric_Gram']:
                        tag = case_name + '_N' + str(intervals) + '_' + branch
                        report['active_job'] = tag
                        save()
                        source = load_arrays(intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                        folder = intake / ('annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke')
                        steps = 64 if intervals == 64 else 32
                        trajectory = load_arrays(folder / (tag + '_steps' + str(steps) + '.npz'))
                        basis = MixedActionBasis(source['radius'])
                        links = MetricLinkQuadrature(basis)
                        count = basis.radii.size
                        length = basis.radii[-1] - basis.radii[0]
                        parameters = numerical.concatenate([(basis.radii - basis.radii[0]) / length, numerical.full(count, basis.spacing / length)])
                        include_gram = branch != 'GR'
                        for index in [0, steps // 2, steps]:
                            time, state = trajectory['time'][index], trajectory['state'][index]
                            scalar, slope_values, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                            packed = state[4 * count:]
                            system = ReleasedHermiteRouthian(basis, scalar, slope_values, constants, kappa, momentum, slope_momentum, source['outer_clock'][0] + time * source['outer_clock'][1], links)
                            tangent = system.constraint_tangent(packed, include_gram, source['endpoint_acceleration'], source['outer_clock'][1])
                            balance = boundary_balance(system, packed, tangent, include_gram, source['outer_clock'][1])
                            unused_value, gradient, hessian = system.evaluate(packed, include_gram)
                            arrays = dict(source, scalar=scalar, corrected=packed, defect=slope_values / basis.spacing, defect_time=packed[system.slope_slice] / basis.spacing, defect_acceleration=tangent['packed_speed'][system.slope_slice] / basis.spacing, gradient_final=gradient, Hessian_final=hessian, **tangent)
                            ward = CurrentWard(system, arrays).evaluate(include_gram)
                            trace = mass_trace_bound(system, packed, tangent)
                            label = tag + '_sample' + str(index)
                            check(label + '_same_owned_shift_vector', maximum(tangent['shift_residual'] - trajectory['shifts'][index]) < 1e-13)
                            check(label + '_independent_mass_pairing', maximum(trace['pairing'] - tangent['pairing']) < 1e-13)
                            check(label + '_full_shift_equals_pairing_times_mass_mismatch', maximum(tangent['shift_residual'] - real_linear(trace['pairing'], trace['mass_rate_mismatch'])) < 1e-13)
                            check(label + '_positive_trace_weights', numerical.all(trace['trace_weights'] > 0))
                            check(label + '_positive_partition_mass_constant', maximum(real_linear(basis.face_value, numerical.ones(basis.faces.size)) - 1) < 1e-14)
                            shift_trace = -numerical.dot(trace['affine_shift_generator'], tangent['shift_residual'])
                            check(label + '_trace_identity_without_nodal_norm_scaling', abs(shift_trace - float(trace['signed_trace'])) < 1e-13)
                            check(label + '_physical_infinity_trace_bound', abs(shift_trace) <= float(trace['trace_bound']) + 1e-13)
                            check(label + '_explicit_mesh_independent_coefficient_envelope', float(trace['coefficient_exact']) <= float(trace['coefficient_uniform_bound']))
                            eigenvalues = eigvalsh(trace['pairing'], trace['unweighted_pairing'])
                            check(label + '_mass_pairing_coercivity_in_physical_L2', eigenvalues[0] >= float(trace['pairing_lower_bound']) * (1 - 1e-12) and eigenvalues[-1] <= float(trace['pairing_upper_bound']) * (1 + 1e-12))
                            if include_gram:
                                current = gram_current(system, packed, tangent)
                                pair_current = current['pair_current']
                            else:
                                pair_current = numerical.zeros(links.node.size)
                            link = affine_link_bound(system, packed, pair_current)
                            bulk = affine_bulk_remainder_bound(system, packed, tangent, link)
                            expected = {'mass_product': ward['bulk_amplitude_mass_product'], 'mass_radial_product': ward['bulk_amplitude_mass_radial_product'], 'lapse_commutator': ward['bulk_amplitude_lapse_product'] - ward['bulk_time_derivative_lapse_product'], 'scalar_commutator': ward['bulk_amplitude_scalar_product'] + ward['bulk_amplitude_velocity_product'] - ward['bulk_time_derivative_scalar_product'], 'scalar_radial_product': ward['bulk_amplitude_scalar_radial_product'], 'shift_product': ward['bulk_amplitude_shift_product']}
                            for name, vector in expected.items():
                                direct = float(numerical.dot(parameters, vector))
                                check(label + '_independent_affine_formula_' + name, abs(direct - float(bulk['signed_' + name])) < 2e-13, abs(direct - float(bulk['signed_' + name])))
                                check(label + '_derived_bulk_bound_' + name, abs(direct) <= float(bulk['bound_' + name]) + 2e-13)
                            check(label + '_time_product_cancellations_reconstruct_bulk', abs(float(bulk['bulk_remainder']) - numerical.dot(parameters, ward['bulk_remainder'])) < 2e-13)
                            check(label + '_mass_radial_cell_cancellation', maximum(bulk['mass_radial_zero_moments']) < 1e-14 and abs(float(bulk['centered_mass_radial_term'] - bulk['signed_mass_radial_product'])) < 1e-13)
                            check(label + '_piecewise_A_Lipschitz_bound', numerical.all(numerical.abs(bulk['mass_radial_coefficient'] - bulk['mass_radial_center_coefficient']) <= bulk['mass_radial_coefficient_difference_bound'] + 1e-13))
                            gram = affine_gram_coefficient_bound(system, packed, tangent, link) if include_gram else {'coefficient_remainder': numerical.asarray(0.), 'coefficient_bound': numerical.asarray(0.)}
                            check(label + '_independent_Gram_coefficient_formula', abs(float(gram['coefficient_remainder']) - numerical.dot(parameters, ward['Gram_coefficient_remainder'])) < 2e-13)
                            check(label + '_Gram_coefficient_bound', abs(float(gram['coefficient_remainder'])) <= float(gram['coefficient_bound']) + 1e-13)
                            ramp = load_arrays(intake / 'annular-boundary-affine-ramp-analysis' / (tag + '_sample' + str(index) + '.npz'))
                            check(label + '_same_previous_boundary_offset', maximum(balance['local_boundary_balance'] - ramp['local_boundary_balance']) < 1e-13)
                            other = sum(abs(float(ramp['term_' + name])) for name in ['lifting_work', 'lapse_constraint_derivative_work', 'free_scalar_mass_work'])
                            reconstruction_bound = float(bulk['bulk_bound'] + gram['coefficient_bound'] + link['Gram_affine_link_remainder_bound']) + other
                            boundary_bound = float(trace['trace_bound']) + reconstruction_bound
                            check(label + '_complete_boundary_bound_no_shift_row_omission', maximum(balance['local_boundary_balance']) <= boundary_bound + maximum(balance['global_boundary_remainder']) + 3e-13)
                            path = destination / (label + '.npz')
                            numerical.savez_compressed(path, **{'trace_' + name: value for name, value in trace.items()}, **{'bulk_' + name: value for name, value in bulk.items()}, **{'Gram_' + name: value for name, value in gram.items()}, **{'link_' + name: value for name, value in link.items()}, boundary_offset=balance['local_boundary_balance'], reconstructed_boundary_bound=boundary_bound)
                            artifact(path)
                            record = {'case': case_name, 'intervals': intervals, 'branch': branch, 'time': float(time), 'mass_rate_mismatch_norm': float(trace['mass_rate_norm']), 'trace_coefficient': float(trace['coefficient_exact']), 'trace_coefficient_uniform_envelope': float(trace['coefficient_uniform_bound']), 'pairing_generalized_min': float(eigenvalues[0]), 'pairing_generalized_max': float(eigenvalues[-1]), 'signed_trace': float(trace['signed_trace']), 'trace_bound': float(trace['trace_bound']), 'boundary_offset_max': maximum(balance['local_boundary_balance']), 'full_boundary_bound': boundary_bound, 'bulk_signed': float(bulk['bulk_remainder']), 'bulk_bound': float(bulk['bulk_bound']), 'bulk_component_bounds': {name: float(bulk['bound_' + name]) for name in expected}, 'Gram_coefficient_bound': float(gram['coefficient_bound']), 'Gram_link_bound': float(link['Gram_affine_link_remainder_bound']), 'maximum_mass_time_radial': maximum(bulk['mass_time_radial']), 'maximum_lapse_radial': maximum(bulk['lapse_radial']), 'maximum_velocity_third': maximum(bulk['velocity_third']), 'maximum_lapse_force_time': maximum(bulk['lapse_force_time']), 'maximum_scalar_Euler_density': maximum(bulk['scalar_Euler_density']), 'maximum_gamma_variation_over_cell_width': float(bulk['max_gamma_variation_over_cell_width']), 'source_trajectory': str((folder / (tag + '_steps' + str(steps) + '.npz')).relative_to(root))}
                            report['samples'].append(record)
                            if case_name == 'canonical' and index == 0 and branch == 'GR':
                                manufactured = packed.copy()
                                manufactured[system.slices[0]] = 0
                                manufactured[system.slices[1]] = 1
                                manufactured[system.slices[2]] = (-1.)**numerical.arange(count)
                                manufactured[system.slope_slice] = -basis.spacing * real_linear(basis.derivative, manufactured[system.slices[2]])
                                kinetic = system.kinetic_matrix(manufactured, False)
                                velocities = manufactured[system.velocity_indices]
                                norm = numerical.sqrt(numerical.dot(velocities, real_linear(kinetic, velocities)))
                                manufactured[system.velocity_indices] /= norm
                                velocities = manufactured[system.velocity_indices]
                                gradient_node = real_linear(basis.derivative, manufactured[system.slices[2]]) + manufactured[system.slope_slice] / basis.spacing
                                third_derivative = 12 * numerical.diff(-manufactured[system.slices[2]]) / basis.spacing**3 + 6 * (gradient_node[:-1] + gradient_node[1:]) / basis.spacing**2
                                energy = numerical.dot(velocities, real_linear(kinetic, velocities))
                                check(label + '_bounded_kinetic_norm_counterexample', abs(energy - 1) < 1e-12 and maximum(gradient_node) < 1e-12)
                                check(label + '_counterexample_same_canonical_Gram_kinetic', maximum(system.kinetic_matrix(manufactured, True) - kinetic) == 0)
                                path = destination / ('energy_only_counterexample_N' + str(intervals) + '.npz')
                                numerical.savez_compressed(path, packed=manufactured, kinetic=kinetic, third_derivative=third_derivative, kinetic_norm_squared=energy)
                                artifact(path)
                                report['energy_counterexamples'].append({'intervals': intervals, 'kinetic_norm_squared': float(energy), 'maximum_velocity_third': maximum(third_derivative), 'not_a_constraint_solution': True})
                                invalid = packed.copy()
                                invalid[system.slices[1]] = 0
                                rejected = False
                                try:
                                    metric_cell_bounds(system, invalid)
                                except ValueError:
                                    rejected = True
                                check(label + '_invalid_chart_not_clipped', rejected)
                        save()
                        print(json.dumps({'finished': tag, 'final_sample': report['samples'][-1]}), flush=True)
            counterexamples = report['energy_counterexamples']
            check('bounded_energy_does_not_supply_uniform_third_derivative', len(counterexamples) == 3 and all(counterexamples[index + 1]['maximum_velocity_third'] > 5 * counterexamples[index]['maximum_velocity_third'] for index in range(2)))
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('all_inputs_preserved', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_outputs_preserved', all(digest(root / name) == expected for name, expected in outputs.items()))
            check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
            report.update(state='complete', passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
            save()
            (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
            print(json.dumps({key: report[key] for key in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
            return
        except Exception as error:
            report.update(state='failed', failure=repr(error), traceback=traceback.format_exc(), completed_utc=datetime.now(timezone.utc).isoformat())
            save()
            raise
    if final_path.exists():
        raise FileExistsError('Final evidence already exists.')
    report_path = destination / 'status.json'
    report = json.loads(report_path.read_text())
    if report['state'] != 'complete' or report['passed'] != report['total'] or not (destination / 'COMPLETE').exists():
        raise RuntimeError('Derivation/validation gate incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260909-mass-trace-control-and-bulk-commutator-bound.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.json', '.md', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-mass-trace-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 16, 1, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench or cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'implementation_check_count': report['total'], 'samples': len(report['samples']), 'energy_counterexamples': len(report['energy_counterexamples']), 'compiled_scripts': scripts, 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T16:01:00Z, not a full pre-turn hash comparison; all writes scoped to post-checkpoint-work', 'mutable_resume_pinned_as_snapshot': True, 'no_bytecode_cache': True, 'physical_mass_trace_estimate_derived': True, 'affine_bulk_commutators_derived': True, 'uniform_high_derivative_control_proved': False, 'full_coupled_DAE_solved': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'state': final['state'], 'checks': final['implementation_check_count'], 'samples': final['samples'], 'input_hashes': len(inputs), 'output_hashes': len(outputs), 'protected_workbench_files_written_since_turn_start': len(touched)}), flush=True)


if __name__ == '__main__':
    run()
