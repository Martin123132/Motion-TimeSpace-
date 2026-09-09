import argparse
import hashlib
import json
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from scipy.linalg import eigvalsh
    from annular_adm_mixed_action_20260909 import MixedActionBasis, linear_value_gradient
    from annular_first_derivative_energy_20260909 import canonical_matrices, growth_rates
    from annular_gram_joint_action_20260909 import gram_matrices
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_uniform_energy_bounds_20260909 import boundary_bounds, coefficient_bounds, exact_certificates, full_operator_norm, metric_envelope, projection_map

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-uniform-energy-bounds-derived'
    final_path = intake / 'annular-uniform-energy-bounds-final-integrity.json'
    prior_path = intake / 'annular-first-derivative-energy-final-integrity.json'
    previous = json.loads(prior_path.read_text())
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

    def loaded(path):
        own(path)
        with numerical.load(path) as handle:
            return {name: handle[name].copy() for name in handle.files}

    if previous['state'] != 'complete':
        raise RuntimeError('Prior gate incomplete.')
    inherit(inputs, previous['inputs'])
    inherit(outputs, previous['outputs'])
    own(prior_path)
    scripts = ['annular_uniform_energy_bounds_20260909.py', 'derive_annular_uniform_energy_bounds_20260909.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'manufactured': [], 'canonical_uniform_coefficient_bound_conditional_on_metric_envelopes': True, 'canonical_uniform_boundary_source_bound_conditional_on_metric_jets': True, 'metric_envelopes_derived_from_full_coupled_evolution': False, 'uniform_energy_estimate_closed': False, 'full_coupled_DAE_solved': False, 'valid_for_physics_claim': False, 'excluded_scope': 'Nonlinear P(X), nonzero scalar mass/Lambda, horizons, lapse collapse, nonuniform scalar meshes, arbitrary slope boundary conditions. The old nonlinear fixture is preserved but not covered by this theorem.', 'reference': {'url': 'https://people.maths.ox.ac.uk/farrellp/femvideos/notes.pdf', 'title': 'Finite Element Methods for PDEs', 'section': '7.5 and 11.4', 'retrieved_utc_date': '2026-09-09', 'role': 'General interpolation/elliptic regularity background only. Constants, positive quadrature and Gram comparison are derived locally, not attributed to this reference.', 'other_url_checked_but_unavailable': 'https://www.maths.ox.ac.uk/system/files/attachments/OxPDE_L_12_03.pdf', 'other_url_status': 'web fetch 403; not used as evidence'}}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        def maximum(values):
            return float(numerical.max(numerical.abs(values)))

        def verify_operators(label, basis, matrices, envelope, include_gram):
            count = basis.radii.size
            free = numerical.array([index for index in range(2 * count) if index not in [0, count - 1]])
            selection = numerical.ix_(free, free)
            mass, stiffness, mass_time, stiffness_time = [matrices[name][selection] for name in ['M', 'K', 'M_dot', 'K_dot']]
            bounds = coefficient_bounds(envelope, include_gram)
            rates = growth_rates(mass, stiffness, mass_time, stiffness_time)
            operator = numerical.linalg.solve(mass, stiffness_time @ numerical.linalg.solve(stiffness, mass))
            beta_l = full_operator_norm(operator, mass)
            for name in ['alpha_M', 'alpha_K', 'alpha_A', 'alpha_L']:
                check(label + '_' + name + '_bounded', rates[name] <= bounds[name + '_bound'] + 2e-10, {'measured': rates[name], 'bound': bounds[name + '_bound']})
            check(label + '_full_nonsymmetric_transport_bounded', beta_l <= bounds['beta_L_operator_bound'] + 2e-10, {'measured': beta_l, 'bound': bounds['beta_L_operator_bound']})
            reconstruction = numerical.concatenate([basis.scalar_value, basis.lift_value / basis.spacing], axis=1)[:, free]
            gradient = numerical.concatenate([basis.scalar_gradient, basis.lift_gradient / basis.spacing], axis=1)[:, free]
            unweighted_mass = reconstruction.T @ (basis.quadrature_weights[:, None] * reconstruction)
            unweighted_stiffness = gradient.T @ (basis.quadrature_weights[:, None] * gradient)
            inverse = float(eigvalsh(unweighted_stiffness, unweighted_mass)[-1])**.5 * basis.spacing
            check(label + '_actual_Hermite_inverse_16', inverse <= 16 + 1e-8, inverse)
            lower = float(eigvalsh(stiffness, unweighted_stiffness)[0])
            upper = float(eigvalsh(stiffness, unweighted_stiffness)[-1])
            check(label + '_gradient_coercivity_and_Gram_envelope', lower >= envelope['p_min'] - 1e-8 and upper <= envelope['p_max'] + bounds['Gram_gradient_bound'] + 1e-8)
            factors, sampling = gram_matrices(count)
            check(label + '_Gram_constant_and_affine_annihilation', maximum(factors @ numerical.ones(count)) < 1e-12 and maximum(factors @ basis.radii) < 1e-12)
            check(label + '_Gram_sampling_convex', numerical.min(sampling) >= 0 and maximum(numerical.sum(sampling, axis=1) - 1) < 1e-14)
            return bounds, rates, beta_l, free

        save()
        try:
            certificates = exact_certificates()
            for name, certificate in certificates.items():
                check('exact_' + name, certificate['positive'], {key: value for key, value in certificate.items() if key != 'positive'})
                certificate['positive'] = bool(certificate['positive'])
            report['exact_certificates'] = certificates
            for intervals in [16, 32, 64, 128]:
                basis = MixedActionBasis(numerical.linspace(1, 2, intervals + 1))
                count, face_count = basis.radii.size, basis.faces.size
                system = SimpleNamespace(basis=basis, node_count=count, slices=[slice(0, face_count), slice(face_count, face_count + count)], constants={'Lambda': 0.0, 'm_chi': 0.0})
                mass_values = .03 + .01 * abs(basis.faces - 1.5)
                lapse_values = 1 + .1 * (basis.radii - 1) + .03 * abs(basis.radii - 1.5)
                packed = numerical.concatenate([mass_values, lapse_values])
                for variant in ['variable', 'constant_theta', 'frozen']:
                    if variant == 'variable':
                        mass_rate = .001 * (1 + basis.faces**2)
                        lapse_rate = .02 + .007 * (basis.radii - 1) + .003 * abs(basis.radii - 1.5)
                    else:
                        mass_rate = numerical.zeros(face_count)
                        lapse_rate = lapse_values * (.02 if variant == 'constant_theta' else 0.0)
                    speed = numerical.concatenate([mass_rate, lapse_rate])
                    envelope = metric_envelope(basis, mass_values, lapse_values, mass_rate, lapse_rate)
                    if variant in ['constant_theta', 'frozen']:
                        exact_theta = .02 if variant == 'constant_theta' else 0.0
                        envelope.update(theta_min=exact_theta, theta_max=exact_theta, theta_lipschitz=0.0)
                    for include_gram in [False, True]:
                        label = 'manufactured_' + variant + '_N' + str(intervals) + ('_Gram' if include_gram else '_GR')
                        matrices = canonical_matrices(system, packed, speed, include_gram)
                        bounds, rates, beta_l, free = verify_operators(label, basis, matrices, envelope, include_gram)
                        if variant != 'variable':
                            check(label + '_constant_theta_exact_all_four', max(abs(rates[name] - abs(exact_theta)) for name in ['alpha_M', 'alpha_K', 'alpha_A', 'alpha_L']) < 2e-9)
                            check(label + '_constant_theta_bound_sharp', max(abs(bounds[name + '_bound'] - abs(exact_theta)) for name in ['alpha_M', 'alpha_K', 'alpha_A', 'alpha_L']) < 1e-14)
                        if variant == 'variable':
                            node_mass = basis.face_to_node @ mass_values
                            node_rate = basis.face_to_node @ mass_rate
                            theta_nodes = lapse_rate / lapse_values - node_rate / (basis.radii - 2 * node_mass)
                            mapping = projection_map(basis, theta_nodes)[numerical.ix_(free, free)]
                            selection = numerical.ix_(free, free)
                            mass = matrices['M'][selection]
                            projection = -numerical.linalg.solve(mass, matrices['M_dot'][selection])
                            gradient = numerical.concatenate([basis.scalar_gradient, basis.lift_gradient / basis.spacing], axis=1)[:, free]
                            value = numerical.concatenate([basis.scalar_value, basis.lift_value / basis.spacing], axis=1)[:, free]
                            unweighted_mass = value.T @ (basis.quadrature_weights[:, None] * value)
                            difference = gradient @ (projection - mapping)
                            form = difference.T @ (basis.quadrature_weights[:, None] * difference)
                            projection_error = max(0.0, float(eigvalsh(form, unweighted_mass)[-1]))**.5
                            projection_bound = 48 * numerical.sqrt(envelope['m_max'] / envelope['m_min']) * envelope['theta_lipschitz']
                            check(label + '_constructive_projection_error', projection_error <= projection_bound + 1e-8)
                        report['manufactured'].append({'label': label, 'bounds': bounds, 'rates': rates, 'beta_L': beta_l})
                if intervals == 16:
                    rejected = False
                    try:
                        metric_envelope(basis, basis.faces / 2, lapse_values, numerical.zeros(face_count), numerical.zeros(count))
                    except ValueError:
                        rejected = True
                    check('horizon_F_zero_rejected_not_claimed', rejected)
            case_path = intake / 'annular-constraint-correction-initial/canonical.json'
            own(case_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            check('canonical_scope_exact', all(constants[name] == 0 for name in ['b2', 'b3', 'm_chi', 'Lambda']))
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            for intervals in [16, 32, 64]:
                steps = 64 if intervals == 64 else 32
                for branch in ['GR', 'metric_Gram']:
                    tag = 'canonical_N' + str(intervals) + '_' + branch
                    source = loaded(intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                    folder = 'annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke'
                    trajectory = loaded(intake / folder / (tag + '_steps' + str(steps) + '.npz'))
                    basis = MixedActionBasis(source['radius'])
                    links = MetricLinkQuadrature(basis)
                    count = basis.radii.size
                    for index in [0, steps // 2, steps]:
                        label = tag + '_sample' + str(index)
                        report['active_job'] = label
                        save()
                        base = loaded(intake / 'annular-first-derivative-energy-derived' / (label + '.npz'))
                        adapted = loaded(intake / 'annular-boundary-adapted-energy-derived' / (label + '.npz'))
                        time, state = trajectory['time'][index], trajectory['state'][index]
                        scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                        packed = state[4 * count:]
                        system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, source['outer_clock'][0] + time * source['outer_clock'][1], links)
                        include_gram = branch != 'GR'
                        tangent = system.constraint_tangent(packed, include_gram, source['endpoint_acceleration'], source['outer_clock'][1])
                        speed, acceleration = tangent['packed_speed'], adapted['local_ODE_acceleration']
                        envelope = metric_envelope(basis, packed[system.slices[0]], packed[system.slices[1]], speed[system.slices[0]], speed[system.slices[1]], acceleration[system.slices[0]], acceleration[system.slices[1]])
                        matrices = canonical_matrices(system, packed, speed, include_gram)
                        bounds, rates, beta_l, free = verify_operators(label, basis, matrices, envelope, include_gram)
                        for name in ['M', 'K', 'M_dot', 'K_dot']:
                            check(label + '_same_saved_' + name, maximum(matrices[name][numerical.ix_(free, free)] - base[name]) < 1e-12)
                        for name in ['full_shift_residual', 'mass_rate_mismatch']:
                            actual = tangent['shift_residual'] if name == 'full_shift_residual' else speed[system.slices[0]] - tangent['shift_mass_speed']
                            check(label + '_preserved_' + name, maximum(actual - adapted[name]) < 1e-12)
                        boundary = boundary_bounds(envelope, bounds, scalar[[0, -1]], packed[system.slices[2]][[0, -1]], source['endpoint_acceleration'])
                        mass = base['M']
                        boundary_measured = {}
                        for name, key in [('boundary_force', 'boundary_force'), ('boundary_force_time', 'boundary_force_time'), ('boundary_source', 'boundary_source')]:
                            vector = adapted[key]
                            measured = float(numerical.sqrt(vector @ numerical.linalg.solve(mass, vector)))
                            boundary_measured[name] = measured
                            check(label + '_' + name + '_bounded', measured <= boundary[name + '_bound'] + 1e-10, {'measured': measured, 'bound': boundary[name + '_bound']})
                        energy = float(adapted['energy'])
                        analytic_rate_bound = bounds['growth_bound'] * energy + numerical.sqrt(2 * energy) * (boundary['boundary_source_bound'] + float(adapted['residual_force_K_graph_norm']))
                        check(label + '_conditional_analytic_energy_bound', float(adapted['energy_time_predicted']) <= analytic_rate_bound + 1e-10)
                        record = {'label': label, 'intervals': intervals, 'branch': branch, 'time': float(time), 'envelope': envelope, 'bounds': bounds, 'rates': rates, 'beta_L': beta_l, 'boundary_bounds': boundary, 'boundary_measured': boundary_measured, 'analytic_energy_rate_bound': analytic_rate_bound, 'old_sampled_energy_rate_bound': float(adapted['energy_rate_upper_bound']), 'physical_mass_mismatch_max': maximum(adapted['mass_rate_mismatch']), 'physical_shift_residual_max': maximum(adapted['full_shift_residual']), 'numeric_envelopes_outward_interval_certified': False, 'second_metric_jets_from_old_directional_ODE_differences': True}
                        report['samples'].append(record)
                        result_path = destination / (label + '.npz')
                        numerical.savez_compressed(result_path, packed=packed, packed_speed=speed, metric_acceleration=acceleration, full_shift_residual=adapted['full_shift_residual'], mass_rate_mismatch=adapted['mass_rate_mismatch'])
                        artifact(result_path)
                        save()
                        if index == steps:
                            print(json.dumps({'label': label, 'C_measured': rates['energy_growth_rate'], 'C_bound': bounds['growth_bound'], 'Hb_measured': boundary_measured['boundary_source'], 'Hb_bound': boundary['boundary_source_bound']}), flush=True)
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('all_old_and_new_source_hashes_preserved', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_output_hashes_preserved', all(digest(root / name) == expected for name, expected in outputs.items()))
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
    report_path = destination / 'status.json'
    report = json.loads(report_path.read_text())
    if report['state'] != 'complete' or report['passed'] != report['total'] or not (destination / 'COMPLETE').is_file():
        raise RuntimeError('New coefficient bound gate incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260909-mesh-uniform-coefficient-and-boundary-source-bounds.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.json', '.md', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-uniform-energy-bounds-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 16, 43, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench or cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'canonical_saved_states': len(report['samples']), 'manufactured_cases': len(report['manufactured']), 'compiled_scripts': scripts, 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T16:43:00Z; not full pre-turn hash comparison; writes scoped to post-checkpoint-work', 'mutable_resume_pinned_as_snapshot': True, 'no_bytecode_cache': True, 'conditional_mesh_uniform_canonical_coefficient_bounds_derived': True, 'conditional_mesh_uniform_affine_boundary_source_bound_derived': True, 'metric_jet_closure_derived': False, 'uniform_energy_estimate_closed': False, 'full_coupled_DAE_solved': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'canonical_saved_states', 'manufactured_cases', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
