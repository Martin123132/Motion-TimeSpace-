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
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_canonical_trace_projection_stable_20260911 import GlobalPrimitive
    from annular_covariant_joint_preparation_20260912 import JointPreparation

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    source = intake / 'annular-covariant-joint-preparation-attempt01'
    destination = intake / 'annular-covariant-joint-control-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'cases': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'full_second_jet_closed': False, 'interval_certificate': False, 'first_runner_Ward_diagnostic_omitted_radial_port_work': True, 'derived_energy_balanced_port_values_not_parent_signed_full_histories': True, 'port_fitted_C1_rows_not_used_for_final_candidate': True}

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    save()
    try:
        previous_path = source / 'status.json'
        previous = json.loads(previous_path.read_text())
        check('joint_run_complete_but_not_a_first_jet_pass', previous['state'] == 'complete' and all(not item['full_first_jet_gate'] for case in previous['cases'] for item in case['quadratures']))
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
            model = JointPreparation(common, branch)
            archive = load_archive(source / (branch + '_joint_candidate.npz'))
            arrays = {}
            for surface, order, weights in [('quad', 12, model.context.weights), ('check', 16, model.context.check_weights)]:
                result = model.evaluate(archive['coefficients'], surface)
                values, nodes = result['fields'][surface], result['fields']['nodes']
                current = result['current']
                outward = np.array([-1., 1.])
                boundary_work = -nodes['eta'][[0, -1]].T @ (outward * current['K']['nodes'][[0, -1]] / nodes['N'][[0, -1]])
                ward_error = result['Ward_error'] - boundary_work
                rho = np.zeros(model.radii.size)
                rho[[0, -1]] = -outward * current['K']['nodes'][[0, -1]] / current['q'][[0, -1]]
                p_first = (current['Gchi'] + rho) / model.node_weights
                source_work = -nodes['eta'].T @ (rho * current['q'] / nodes['N'])
                constraint_rate = result['C1_no_ports'] + source_work
                check(branch + '_' + surface + '_corrected_Ward_retains_radial_source_work', abs(ward_error).max() < 1e-9, {'reconstruction': float(abs(ward_error).max()), 'omitted_radial_work': float(abs(boundary_work).max())})
                check(branch + '_' + surface + '_derived_port_work_exact_not_constraint_row_fit', max(abs(source_work + boundary_work).max(), abs(model.node_weights * p_first - current['Gchi'] - rho).max()) < 1e-12)
                step = 1e-24j
                mass_direction = model.frame[surface]['q'] @ result['mu_coeff']
                node_mass_direction = result['mu_nodes']
                geometry = 1 - 2 * (values['mu'] + step * mass_direction) / values['R']
                node_geometry = 1 - 2 * (nodes['mu'] + step * node_mass_direction) / model.radii
                root_f, node_root = np.sqrt(geometry), np.sqrt(node_geometry)
                coefficient = model.radii**2 * nodes['N'] * np.sqrt(nodes['F'])
                density = model.collect(model.spair * current['J'] * coefficient[model.node])
                amplitude_first = model.collect(model.bpair * current['J'] * current['q'][model.node])
                transported_amplitude = model.amplitude[model.factor] + amplitude_first[model.factor] * step / current['J']
                nodal_d = model.scatter(model.spair * transported_amplitude**2 / (2 * model.spacing))
                momentum = result['momentum'] + step * p_first
                momentum_metric = model.frame[surface]['p'] @ result['P_coeff'] * step
                node_metric = result['P_nodes'] * step
                chart = 1 - .1**2 * geometry**2 * momentum_metric**2
                node_chart = 1 - .1**2 * node_geometry**2 * node_metric**2
                scalar_energy = model.node_weights * momentum**2 / (2 * model.radii**2) + model.radii**2 * nodal_d
                residual = values['eta'].T @ (weights * (root_f + 1 / root_f - 2 * model.reference) / .2)
                residual += values['eta_r'].T @ (weights * values['R'] * (root_f - model.reference) / .1)
                residual -= nodes['eta'][-1] * model.radii[-1] * (node_root[-1] - model.reference) / .1
                residual += nodes['eta'][0] * model.radii[0] * (node_root[0] - model.reference) / .1
                residual -= nodes['eta'].T @ (node_root * node_chart * scalar_energy)
                transport = values['eta'].T @ (weights * current['K'][surface] * (-.1 * root_f * momentum_metric / (values['N']**2 * chart)))
                residual += transport
                direct_rate = residual.imag / step.imag
                check(branch + '_' + surface + '_independent_first_order_history_constraint_curve', abs(direct_rate - constraint_rate).max() < 1e-10, float(abs(direct_rate - constraint_rate).max()))
                scalar_untransported_d_first = model.sampling.T @ (model.amplitude * (model.factors @ current['q'])) / model.spacing
                untransported_d_change = nodes['eta'].T @ (model.radii**2 * np.sqrt(nodes['F']) * (current['d_first'] - scalar_untransported_d_first))
                c_p = .1 * np.sqrt(values['F']) / values['N']
                primitive = current['primitive']
                weak_columns = model.frame[surface]['p'] * (c_p * np.exp(-2 * primitive.evaluate(values['R'])))[:, None]
                link_load = []
                for column in range(weak_columns.shape[1]):
                    integrated = GlobalPrimitive(model.context.knots, weak_columns[:, column], order)
                    link_load.append((integrated.evaluate(model.targets) - integrated.evaluate(model.anchors)) @ current['global_current'])
                direct_load = model.frame[surface]['p'].T @ (weights * c_p * current['K'][surface])
                check(branch + '_' + surface + '_all79_oriented_link_loads_match_cell_integrals', abs(np.array(link_load) - direct_load).max() < 1e-9, float(abs(np.array(link_load) - direct_load).max()))
                directions = [0, 1, 10, 25, 40, 55, 70, 76, 77, 78]
                force_errors = []
                inner_reaction = nodes['N'][0] / (.1 * np.sqrt(nodes['F'][0]))
                for column in directions:
                    mass = values['mu'] + step * model.frame[surface]['q'][:, column]
                    node_mass = nodes['mu'] + step * model.frame['nodes']['q'][:, column]
                    root_f = np.sqrt(1 - 2 * mass / values['R'])
                    node_root = np.sqrt(1 - 2 * node_mass / model.radii)
                    hamiltonian = weights @ (-values['N'] * (root_f + 1 / root_f - 2 * model.reference) / .2 - values['R'] * values['N_r'] * (root_f - model.reference) / .1)
                    hamiltonian += (model.radii * nodes['N'] * (node_root - model.reference))[-1] / .1 - (model.radii * nodes['N'] * (node_root - model.reference))[0] / .1
                    hamiltonian += model.clock * node_mass[-1] / .1 + (nodes['N'] * node_root) @ result['energy']
                    derivative = -hamiltonian.imag / step.imag + inner_reaction * model.frame['nodes']['q'][0, column]
                    force_errors.append(abs(derivative - result['P_force'][column]))
                check(branch + '_' + surface + '_ten_new_gravity_plus_full_scalar_metric_force_variations', max(force_errors) < 1e-10, max(force_errors))
                row = {'branch': branch, 'quadrature': surface, 'C1_energy_balanced_ports_max': float(abs(constraint_rate).max()), 'C1_interior_P1_max': float(abs(constraint_rate[1:16]).max()), 'C1_cubic_max': float(abs(constraint_rate[17:]).max()), 'C1_endpoint_row_max': float(abs(constraint_rate[[0, 16]]).max()), 'derived_scalar_port_forces': rho[[0, -1]].tolist(), 'difference_from_row_fitted_ports': (rho - result['rho'])[[0, -1]].tolist(), 'corrected_Ward_reconstruction': float(abs(ward_error).max()), 'untransported_scalar_density_negative_control': float(abs(untransported_d_change).max()), 'omit_connection_load_negative_control': float(abs(transport.imag / step.imag).max()), 'retained_radial_port_work_max': float(abs(boundary_work).max()), 'metric_Euler_work_max': float(abs(result['metric_work']).max()), 'mass_projection_work_max': float(abs(result['projection_work']).max()), 'direct_constraint_curve_error': float(abs(direct_rate - constraint_rate).max()), 'metric_force_variation_max': float(max(force_errors)), 'port_histories_parent_signed': False, 'first_jet_gate': bool(abs(constraint_rate).max() < 1e-10 and abs(result['mu_nodes'] - result['raw_nodes'])[[0, -1]].max() < 1e-10)}
                report['cases'].append(row)
                for key, value in [('C1', constraint_rate), ('rho', rho), ('p_first', p_first), ('direct_C1', direct_rate), ('boundary_work', boundary_work), ('corrected_Ward_error', ward_error), ('metric_work', result['metric_work']), ('projection_work', result['projection_work'])]:
                    arrays[surface + '__' + key] = value
                save()
                print(json.dumps(row), flush=True)
            path = destination / (branch + '_energy_balanced_port_and_Ward_control.npz')
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
