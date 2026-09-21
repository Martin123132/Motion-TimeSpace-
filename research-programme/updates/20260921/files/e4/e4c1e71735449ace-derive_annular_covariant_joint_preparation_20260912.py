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
    from annular_covariant_joint_preparation_20260912 import JointPreparation

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    destination = intake / 'annular-covariant-joint-preparation-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'cases': [], 'inputs': {}, 'outputs': {}, 'new_evolution': False, 'valid_for_physics_claim': False, 'interval_certificate': False, 'full_second_jet_closed': False, 'new_finite_action_not_old_certificate': True, 'inferred_port_forces_not_parent_signed_histories': True, 'previous_working_branch_unchanged': True}

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
        previous_path = intake / 'annular-covariant-scalar-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_seal_complete_not_full_initial_data', previous['state'] == 'complete' and previous['new_C0_only_roots_not_full_initial_data'])
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
            print('Joint new-action preparation: ' + branch, flush=True)
            model = JointPreparation(common, branch)
            coefficients, result, history = model.solve()
            higher = model.evaluate(coefficients, 'check')
            old_ports = model.evaluate(coefficients, inferred_ports=False)
            nodes = result['fields']['nodes']
            summaries = []
            for label, current in [('primary', result), ('higher', higher)]:
                data = current['fields']['nodes']
                row = {'quadrature': label, 'C0_max': float(abs(current['residual'][:19]).max()), 'C1_max': float(abs(current['C1']).max()), 'C1_interior_P1_max': float(abs(current['C1'][1:16]).max()), 'C1_cubic_max': float(abs(current['C1'][17:]).max()), 'P1_endpoint_max': float(abs(current['P_nodes'][[0, -1]]).max()), 'clock_gap': float(data['N'][-1] / np.sqrt(data['F'][-1]) - model.clock), 'outer_scalar_drive_gap': float(current['current']['q'][-1] - model.saved['boundary_velocity'][2]), 'raw_inner_mass_drive_gap': float(current['raw_nodes'][0] - model.saved['boundary_velocity'][0]), 'projected_inner_mass_drive_gap': float(current['mu_nodes'][0] - model.saved['boundary_velocity'][0]), 'all_endpoint_mass_projection_defect': float(abs(current['mu_nodes'][[0, -1]] - current['raw_nodes'][[0, -1]]).max()), 'lapse_min': min(float(item['N'].min()) for item in current['fields'].values()), 'F_min': min(float(item['F'].min()) for item in current['fields'].values()), 'J_min': float(current['current']['J'].min()), 'J_max': float(current['current']['J'].max()), 'inferred_scalar_port_forces': current['rho'][[0, -1]].tolist(), 'C1_metric_projection_work_max': float(abs(current['metric_work']).max()), 'C1_mass_velocity_projection_work_max': float(abs(current['projection_work']).max()), 'C1_source_work_max': float(abs(current['source_work']).max()), 'Ward_reconstruction_max': float(abs(current['Ward_error']).max()), 'boundary_K_identity_error': float(abs(current['boundary_K_error']).max())}
                row['full_first_jet_gate'] = max(row[key] for key in ['C0_max', 'C1_max', 'P1_endpoint_max', 'all_endpoint_mass_projection_defect']) < 1e-10 and abs(row['projected_inner_mass_drive_gap']) < 1e-10
                summaries.append(row)
                check(branch + '_' + label + '_joint_C0_clock_and_raw_drive_solved', max(row['C0_max'], abs(row['clock_gap']), abs(row['outer_scalar_drive_gap']), abs(row['raw_inner_mass_drive_gap'])) < 1e-10, row)
                check(branch + '_' + label + '_scalar_canonical_equation_exact', abs(model.node_weights * current['p_first'] - current['current']['Gchi'] - current['rho']).max() < 1e-12)
                check(branch + '_' + label + '_full_current_boundary_and_anchor_identities', max(abs(current['boundary_K_error']).max(), current['current']['anchor_error'], current['current']['cell_anchor_error']) < 1e-10)
            record = {'branch': branch, 'mass_phase_dimension': model.pairings['quad'].shape[0], 'lapse_amplitudes': result['lapse_amplitudes'].tolist(), 'lapse_response_condition': float(np.linalg.cond(result['lapse_response'])), 'dependent_momentum_amplitudes': coefficients[19:].tolist(), 'momentum_change_max': float(abs(result['momentum'] - model.momentum_seed).max()), 'unchanged_free_profile_modulo_two_sourced_boundary_lifts': True, 'scalar_profile_change': float(abs(model.scalar - model.data['nodes']['chi']).max()), 'inner_mass_change': float(nodes['mu'][0] - model.data['nodes']['mu'][0]), 'Newton_history': history, 'quadratures': summaries, 'old_port_samples_C1_max': float(abs(old_ports['C1']).max()), 'old_port_samples_C1_endpoint_rows': old_ports['C1'][[0, 16]].tolist()}
            report['cases'].append(record)
            archive = {'coefficients': coefficients, 'momentum': result['momentum'], 'scalar': model.scalar, 'lapse_amplitudes': result['lapse_amplitudes']}
            for label, current in [('primary', result), ('higher', higher)]:
                for key in ['P_coeff', 'mu_coeff', 'P_nodes', 'mu_nodes', 'raw_nodes', 'p_first', 'rho', 'C1', 'C1_no_ports', 'projection_work', 'metric_work', 'source_work', 'Ward_error', 'residual']:
                    archive[label + '__' + key] = current[key]
                for key in ['q', 'J', 'Gchi', 'd_first', 'current', 'global_current', 'cell_current']:
                    archive[label + '__' + key] = current['current'][key]
            for surface, data in result['fields'].items():
                for key in ['mu', 'F', 'N', 'N_r']:
                    archive[surface + '__' + key] = data[key]
            path = destination / (branch + '_joint_candidate.npz')
            np.savez_compressed(path, **archive)
            own(path, 'outputs')
            save()
            print(json.dumps(record), flush=True)
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
