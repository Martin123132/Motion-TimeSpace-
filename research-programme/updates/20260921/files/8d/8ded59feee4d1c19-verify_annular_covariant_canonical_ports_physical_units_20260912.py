import hashlib
import json
import sys
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from scipy.linalg import solve
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_covariant_canonical_ports_20260912 import CanonicalPortPreparation
    from annular_covariant_flux_moments_20260912 import install, energy_balanced

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    destination = intake / 'annular-covariant-canonical-ports-attempt02'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'cases': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'full_first_jet_closed': False, 'full_second_jet_closed': False, 'interval_certificate': False, 'boundary_port_action_power_used_not_C1_row_fit': True, 'raw_vs_projected_mass_flux_gate_retained': True, 'source_histories_parent_signed': False, 'no_publication': True, 'attempt01_test_normalization_bug_corrected': 'Check physical drive errors at 1e-10, not Newton residual divided by .02. No physical tolerance changed.'}

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    save()
    try:
        previous_path = intake / 'annular-covariant-flux-feedback-attempt01/status.json'
        previous = json.loads(previous_path.read_text())
        check('bounded_feedback_finished_not_a_pass', previous['state'] == 'complete' and not previous['full_first_jet_closed'])
        for table in ['inputs', 'outputs']:
            for name, expected in previous[table].items():
                if name in report['inputs']:
                    continue
                if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed evidence: ' + name)
                report['inputs'][name] = expected
        own(previous_path)
        snapshot = destination / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        common = CommonProfile(root)
        for branch in ['GR', 'metric_Gram']:
            for selection in ['original79', 'one_pass95', 'feedback_last95']:
                model = CanonicalPortPreparation(common, branch)
                if selection != 'original79':
                    path = intake / 'annular-covariant-flux-moments-attempt01' / (branch + '_frozen_extended_frames.npz') if selection == 'one_pass95' else intake / 'annular-covariant-flux-feedback-attempt01' / (branch + '_iteration4_frames.npz')
                    raw = load_archive(path)
                    install(model, {surface: {kind: raw[surface + '__' + kind] for kind in ['q', 'qr', 'p']} for surface in model.frame})
                coefficients, primary, history = model.solve()
                higher = model.evaluate(coefficients, 'check')
                arrays = {'coefficients': coefficients, 'momentum': primary['momentum'], 'lapse_amplitudes': primary['lapse_amplitudes']}
                for surface, result, weights in [('quad', primary, model.context.weights), ('check', higher, model.context.check_weights)]:
                    nodes, values = result['fields']['nodes'], result['fields'][surface]
                    raw_port = energy_balanced(model, result)
                    signed_power = np.array([-1., 1.]) * nodes['N'][[0, -1]] * result['mu_nodes'][[0, -1]] / (.1 * np.sqrt(nodes['F'][[0, -1]]))
                    scalar_power = result['rho'][[0, -1]] * result['current']['q'][[0, -1]]
                    lapse_coefficients = solve(values['eta'].T @ (weights[:, None] * values['eta']), values['eta'].T @ (weights * values['N']))
                    lapse_reconstruction = max(abs(values['eta'] @ lapse_coefficients - values['N']).max(), abs(nodes['eta'] @ lapse_coefficients - nodes['N']).max())
                    total_constraint_power = lapse_coefficients @ result['C1']
                    metric_pair_power = (model.frame[surface]['p'] @ result['P_coeff']) @ (weights * (result['mu_first'] - result['raw_mu']))
                    rule_difference_error = result['C1'] - raw_port['C1'] + result['boundary_projection']
                    prefix = branch + '_' + selection + '_' + surface
                    check(prefix + '_joint_physical_drive_and_C0', max(abs(result['residual'][:19]).max(), abs(result['mu_nodes'][0] - model.saved['boundary_velocity'][0]), abs(result['current']['q'][-1] - model.saved['boundary_velocity'][2]), abs(nodes['N'][-1] / np.sqrt(nodes['F'][-1]) - model.clock)) < 1e-10)
                    check(prefix + '_metric_and_scalar_port_powers_match', abs(scalar_power - signed_power).max() < 1e-12)
                    check(prefix + '_no_C1_fitted_force_exact_port_difference', abs(rule_difference_error).max() < 1e-12)
                    check(prefix + '_global_canonical_power_identity', lapse_reconstruction < 1e-12 and max(abs(total_constraint_power), abs(metric_pair_power)) < 1e-11, {'lapse_reconstruction': float(lapse_reconstruction), 'N_weighted_C1': float(total_constraint_power), 'pair_power': float(metric_pair_power)})
                    check(prefix + '_full_local_Ward_including_both_ports', abs(result['Ward_error']).max() < 1e-10)
                    row = {'branch': branch, 'frame': selection, 'surface': surface, 'C0': float(abs(result['residual'][:19]).max()), 'C1': float(abs(result['C1']).max()), 'C1_interior': float(abs(result['C1'][1:16]).max()), 'C1_cubic': float(abs(result['C1'][17:]).max()), 'metric_work': float(abs(result['metric_work']).max()), 'bulk_nodal_projection_work': float(abs(result['bulk_nodal_projection_work']).max()), 'N_weighted_C1': float(total_constraint_power), 'port_rule_difference': float(abs(rule_difference_error).max()), 'projected_inner_drive_error': float(result['mu_nodes'][0] - model.saved['boundary_velocity'][0]), 'raw_inner_drive_error': float(result['raw_nodes'][0] - model.saved['boundary_velocity'][0]), 'mass_endpoint_error': float(abs(result['mu_nodes'][[0, -1]] - result['raw_nodes'][[0, -1]]).max()), 'P1_endpoint': float(abs(result['P_nodes'][[0, -1]]).max()), 'rho': result['rho'][[0, -1]].tolist(), 'Ward_error': float(abs(result['Ward_error']).max()), 'F_min': min(float(data['F'].min()) for data in result['fields'].values()), 'N_min': min(float(data['N'].min()) for data in result['fields'].values()), 'J_min': float(result['current']['J'].min()), 'J_max': float(result['current']['J'].max()), 'same_state_raw_port_C1': float(abs(raw_port['C1']).max())}
                    row['full_first_jet_gate'] = max(row['C0'], row['C1'], abs(row['projected_inner_drive_error']), row['mass_endpoint_error'], row['P1_endpoint']) < 1e-10
                    report['cases'].append(row)
                    for key in ['C1', 'rho', 'p_first', 'mu_coeff', 'P_coeff', 'mu_nodes', 'P_nodes', 'raw_nodes', 'projection_work', 'metric_work', 'bulk_nodal_projection_work', 'boundary_projection', 'Ward_error', 'residual']:
                        arrays[surface + '__' + key] = result[key]
                    arrays[surface + '__N_coefficients'] = lapse_coefficients
                    save()
                    print(json.dumps(row), flush=True)
                path = destination / (branch + '_' + selection + '_canonical_port_candidate.npz')
                np.savez_compressed(path, **arrays)
                own(path, 'outputs')
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        save()
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
