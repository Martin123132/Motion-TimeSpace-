import hashlib
import json
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_frozen_second_jet_complex_20260912 import FrozenSecondJet
    from annular_covariant_scalar_action_20260912 import full_spatial_factors

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    source = intake / 'annular-covariant-scalar-source-jet-attempt01'
    destination = intake / 'annular-covariant-scalar-preparation-control-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'cases': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'full_second_jet_closed': False, 'interval_certificate': False, 'boundary_clock_and_scalar_velocity_formula_derived_not_applied': True, 'C0_only_roots_not_full_initial_data': True}

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    prior_path = source / 'status.json'
    prior = json.loads(prior_path.read_text())
    check('source_jet_and_C0_preparation_complete', prior['state'] == 'complete' and all(row['passed'] for row in prior['checks']))
    inherited = dict(prior['inputs'])
    inherited.update(prior['outputs'])
    for name, expected in inherited.items():
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
            raise RuntimeError('Changed evidence: ' + name)
        report['inputs'][name] = expected
    for path in [prior_path, Path(__file__)]:
        own(path)
    snapshot = destination / ('executed-' + Path(__file__).name)
    snapshot.write_bytes(Path(__file__).read_bytes())
    own(snapshot, 'outputs')
    common = CommonProfile(root)
    for branch in ['GR', 'metric_Gram']:
        prepared = load_archive(source / (branch + '_source_jet_and_C0_only_preparation.npz'))
        model = FrozenSecondJet(common, branch, higher=True)
        nodes = model.data['nodes']
        factors, sampling = full_spatial_factors(nodes['R'].size, model.gram)
        spacing = model.basis.spacing
        weights_node = np.full(nodes['R'].size, spacing)
        weights_node[[0, -1]] /= 2
        dvalue = sampling.T @ (factors @ nodes['chi'])**2 / (2 * spacing)
        energy = weights_node * nodes['pi']**2 / (2 * nodes['R']**2) + nodes['R']**2 * dvalue
        values = model.data['check']
        root_f = np.sqrt(1 - 2 * prepared['check_prepared_mass'] / values['R'])
        node_root = np.sqrt(1 - 2 * prepared['nodes_prepared_mass'] / nodes['R'])
        reference = np.sqrt(2 / 3)
        constraint = values['eta'].T @ (model.weights * (root_f + 1 / root_f - 2 * reference) / .2)
        constraint += values['eta_r'].T @ (model.weights * values['R'] * (root_f - reference) / .1)
        constraint -= nodes['eta'][-1] * nodes['R'][-1] * (node_root[-1] - reference) / .1
        constraint += nodes['eta'][0] * nodes['R'][0] * (node_root[0] - reference) / .1
        constraint -= nodes['eta'].T @ (node_root * energy)
        check(branch + '_independent_higher_quadrature_all19_C0', abs(constraint).max() < 1e-10, float(abs(constraint).max()))
        outer_clock = model.context.system.outer_clock
        outer_velocity = model.saved['boundary_velocity'][2]
        required_N = outer_clock * node_root[-1]
        required_pi = nodes['R'][-1]**2 * outer_velocity / (outer_clock * node_root[-1]**2)
        check(branch + '_derived_joint_outer_clock_and_scalar_drive_identity', abs(required_N / node_root[-1] - outer_clock) < 1e-14 and abs(required_N * node_root[-1] * required_pi / nodes['R'][-1]**2 - outer_velocity) < 1e-14)
        factor, node = np.nonzero((factors != 0) | (sampling != 0))
        factor_weight, sample_weight = factors[factor, node], sampling[factor, node]
        coefficient = nodes['R']**2 * nodes['N'] * np.sqrt(nodes['F'])
        jacobian = prepared['endpoint_J']
        amplitude = factors @ prepared['scalar']
        density = np.bincount(factor, weights=sample_weight * jacobian * coefficient[node], minlength=factors.shape[0])
        amplitude_first = np.bincount(factor, weights=factor_weight * jacobian * prepared['scalar_velocity'][node], minlength=factors.shape[0])
        current = amplitude[factor] * (sample_weight * coefficient[node] * amplitude_first[factor] - factor_weight * prepared['scalar_velocity'][node] * density[factor]) / spacing
        dfirst = np.bincount(node, weights=sample_weight * amplitude[factor] * amplitude_first[factor] / (spacing * jacobian), minlength=nodes['R'].size)
        force = weights_node * prepared['momentum_first'] - prepared['prescribed_port_force']
        boundary_K = np.array([-1., 1.]) * (coefficient * dfirst + force * prepared['scalar_velocity'])[[0, -1]]
        direct_jump = -np.bincount(node, weights=current / jacobian, minlength=nodes['R'].size)
        direct_K = np.array([direct_jump[0], -direct_jump[-1]])
        check(branch + '_full_base_and_Gram_boundary_current_identity', abs(boundary_K - direct_K).max() < 1e-12)
        mass_flux = -.1 * np.sqrt(nodes['F'][[0, -1]]) * boundary_K / nodes['N'][[0, -1]]
        record = {'branch': branch, 'primary_C0_max': float(abs(prepared['prepared_C0']).max()), 'higher_C0_max': float(abs(constraint).max()), 'C0_quadrature_difference_max': float(abs(constraint - prepared['prepared_C0']).max()), 'required_outer_lapse_NOT_APPLIED': float(required_N), 'required_outer_auxiliary_NOT_APPLIED': float(required_pi), 'relative_required_outer_auxiliary_change': float(required_pi / nodes['pi'][-1] - 1), 'inner_mass_flux_on_old_prescribed_metric_jet': float(mass_flux[0]), 'inner_mass_drive_gap_on_old_prescribed_metric_jet': float(mass_flux[0] - model.saved['boundary_velocity'][0]), 'boundary_kernel_including_C_d_t_term': boundary_K.tolist(), 'new_full_boundary_and_first_jet_problem_remains': True}
        report['cases'].append(record)
        path = destination / (branch + '_higher_C0_and_boundary_targets.npz')
        np.savez_compressed(path, higher_C0=constraint, boundary_K=boundary_K, mass_flux=mass_flux, unapplied_outer_N=required_N, unapplied_outer_auxiliary=required_pi)
        own(path, 'outputs')
        save()
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    report['state'] = 'complete'
    save()
    print(json.dumps({'state': report['state'], 'checks': len(report['checks']), 'cases': report['cases']}), flush=True)


if __name__ == '__main__':
    run()
