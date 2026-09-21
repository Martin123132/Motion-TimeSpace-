import hashlib
import json
import sys
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_covariant_canonical_ports_20260912 import CanonicalPortPreparation
    from annular_covariant_flux_moments_20260912 import install
    from annular_local_gauge_commutator_20260912 import gauge_budget
    from annular_local_gauge_trace_stable_20260912 import polynomial_completion

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    destination = intake / 'annular-local-gauge-trace-stable-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'cases': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'full_first_jet_closed': False, 'full_second_jet_closed': False, 'interval_certificate': False, 'matched_trace_preserving_interior_polynomial_trials_not_current_fitting': True, 'physical_scalar_stencil_and_sources_fixed': True, 'old_working_branch_unchanged': True}

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
        previous_path = intake / 'annular-covariant-flux-ports-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_seal_complete_not_full_first_jet', previous['state'] == 'complete' and not previous['full_first_jet_closed'])
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
            for modes in [2, 4]:
                print('Gauge work/stable trace-preserving interior trial: ' + branch + ' modes=' + str(modes), flush=True)
                model = CanonicalPortPreparation(common, branch)
                construction = {'new_phase_dimension': 79, 'no_enrichment': True}
                if modes:
                    original = model.frame
                    frames, construction = polynomial_completion(model, modes)
                    check(branch + '_' + str(modes) + '_canonical_completion_and_old_columns', construction['pairing_condition'] < 100 and construction['canonical_block_error'] < 1e-8 and all(np.array_equal(frames[surface][kind][:, :original[surface][kind].shape[1]], original[surface][kind]) for surface in frames for kind in ['q', 'qr', 'p']), construction)
                    install(model, frames)
                case = {'branch': branch, 'bubble_modes': modes, 'construction': construction, 'surfaces': []}
                report['cases'].append(case)
                save()
                coefficients, primary, history = model.solve()
                case['Newton_history'] = history
                higher = model.evaluate(coefficients, 'check')
                arrays = {'coefficients': coefficients, 'momentum': primary['momentum'], 'lapse_amplitudes': primary['lapse_amplitudes']}
                for surface, result in [('quad', primary), ('check', higher)]:
                    budget = gauge_budget(model, result, surface)
                    prefix = branch + '_' + str(modes) + '_' + surface
                    check(prefix + '_local_gauge_two_work_identity', abs(budget['identity_error']).max() < 1e-10, float(abs(budget['identity_error']).max()))
                    check(prefix + '_represented_tests_vanish_by_actual_canonical_equations', max(abs(budget['q_weak_equation_error']).max(), abs(budget['p_weak_equation_error']).max()) < 1e-10)
                    check(prefix + '_graph_and_L2_bounds_really_dominate_work', np.all(abs(budget['metric_residual_work']) <= budget['q_bound'] + 1e-12) and np.all(abs(budget['momentum_residual_work']) <= budget['p_bound'] + 1e-12))
                    check(prefix + '_joint_C0_and_actual_drives', max(abs(result['residual'][:19]).max(), abs(result['mu_nodes'][0] - model.saved['boundary_velocity'][0]), abs(result['current']['q'][-1] - model.saved['boundary_velocity'][2])) < 1e-10)
                    row = {'surface': surface, 'C0': float(abs(result['residual'][:19]).max()), 'C1': float(abs(result['C1']).max()), 'configuration_gauge_work': float(abs(budget['coordinate_work']).max()), 'momentum_gauge_work': float(abs(budget['momentum_work']).max()), 'q_graph_error': float(budget['q_graph_error'].max()), 'p_L2_error': float(budget['p_error'].max()), 'honest_Cauchy_bound': float(budget['bound'].max()), 'mass_velocity_L2_error': budget['mass_velocity_L2_error'], 'identity_error': float(abs(budget['identity_error']).max()), 'missing_gradient_negative_control': float(abs(budget['missing_gradient_negative_control']).max()), 'mass_endpoint_error': float(abs(result['mu_nodes'][[0, -1]] - result['raw_nodes'][[0, -1]]).max()), 'raw_inner_drive_error': float(result['raw_nodes'][0] - model.saved['boundary_velocity'][0]), 'P1_endpoint': float(abs(result['P_nodes'][[0, -1]]).max()), 'F_min': min(float(data['F'].min()) for data in result['fields'].values()), 'N_min': min(float(data['N'].min()) for data in result['fields'].values()), 'J_min': float(result['current']['J'].min()), 'J_max': float(result['current']['J'].max())}
                    row['full_first_jet_gate'] = max(row['C0'], row['C1'], row['mass_endpoint_error'], row['P1_endpoint']) < 1e-10
                    case['surfaces'].append(row)
                    for key, value in budget.items():
                        arrays[surface + '__' + key] = np.asarray(value)
                    for key in ['C1', 'rho', 'p_first', 'mu_coeff', 'P_coeff', 'mu_nodes', 'P_nodes', 'raw_nodes', 'residual']:
                        arrays[surface + '__' + key] = result[key]
                    save()
                    print(json.dumps({'branch': branch, 'modes': modes, 'dimension': construction['new_phase_dimension'], **row}), flush=True)
                path = destination / (branch + '_modes' + str(modes) + '_candidate.npz')
                np.savez_compressed(path, **arrays)
                own(path, 'outputs')
                path = destination / (branch + '_modes' + str(modes) + '_frames.npz')
                np.savez_compressed(path, **{surface + '__' + kind: array for surface, maps in model.frame.items() for kind, array in maps.items()})
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
