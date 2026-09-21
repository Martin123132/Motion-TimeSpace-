import hashlib
import json
import sys
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    import sympy as sp
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_covariant_canonical_ports_20260912 import CanonicalPortPreparation
    from annular_interface_layer_clock_20260912 import solve_layer, action_controls, profile
    from annular_interface_layer_bounds_20260912 import limit_bounds

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    destination = intake / 'annular-interface-layer-clock-attempt03'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'sources': [],
              'layers': [], 'action_controls': [], 'valid_for_physics_claim': False,
              'full_first_jet_closed': False, 'full_GR_limit_proven': False, 'new_evolution': False,
              'full_scalar_action_descent_proven': False, 'regulator_choice_parent_signed': False,
              'conditional_geometry_and_clock_layer_derived': True,
              'single_interface_not_global_initial_data': True,
              'test_tolerances_are_local_identity_controls_not_original_C1_pass': True}

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    report['attempt01_validator_correction'] = 'Total peak-rate ratio includes finite vacuum/background rate; verify derived source-term inverse-width scaling instead. No physical C1 threshold changed.'
    report['validator_corrections'] = ['attempt01 compared total rate including bounded background instead of source inverse-width scaling', 'attempt02 demanded an empirical error reduction ratio even for errors near rounding floor; attempt03 uses derived analytic error envelopes plus stated 1e-12 numerical allowance. No physical C1 gate changed.']
    save()
    try:
        previous_path = intake / 'annular-local-gauge-budget-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_evidence_complete_not_promoted', previous['state'] == 'complete' and not previous['full_first_jet_closed'])
        for table in ['inputs', 'outputs']:
            for name, expected in previous[table].items():
                if name in report['inputs']:
                    continue
                if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed inherited evidence: ' + name)
                report['inputs'][name] = expected
        own(previous_path)
        snapshot = destination / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        radius, mass, lapse, density, coupling, mass_r, lapse_r, rate = sp.symbols('R mu N rho kappa mu_R N_R P1', positive=True)
        geometry = 1 - 2 * mass / radius
        root_f = sp.sqrt(geometry)
        root_derivative = sp.diff(root_f, radius) + sp.diff(root_f, mass) * mass_r
        constraint_mass_rate = coupling * geometry * density
        algebraic_root = sp.simplify(root_derivative.subs(mass_r, constraint_mass_rate) / root_f - mass / (radius**2 * geometry) + coupling * density / radius)
        solved_lapse = lapse * mass / (radius**2 * geometry) + coupling * lapse * density / radius - coupling * root_f * rate
        lapse_identity = sp.simplify(-solved_lapse / (coupling * root_f) + lapse * mass / (coupling * radius**2 * root_f**3) + lapse * density / (radius * root_f) - rate)
        density_identity = sp.simplify(solved_lapse / lapse + root_derivative.subs(mass_r, constraint_mass_rate) / root_f + coupling * root_f * rate / lapse - 2 * mass / (radius**2 * geometry))
        check('symbolic_root_lapse_transport_identities', algebraic_root == 0 and lapse_identity == 0 and density_identity == 0)
        fraction = sp.symbols('fraction', real=True)
        for name, expression in [('beta22', 6 * fraction * (1 - fraction)), ('beta33', 30 * fraction**2 * (1 - fraction)**2), ('beta23', 12 * fraction * (1 - fraction)**2)]:
            check(name + '_exact_unit_mass_normalization', sp.integrate(expression, (fraction, 0, 1)) == 1)
        common = CommonProfile(root)
        for branch in ['GR', 'metric_Gram']:
            model = CanonicalPortPreparation(common, branch)
            source_path = intake / 'annular-covariant-canonical-ports-attempt02' / (branch + '_original79_canonical_port_candidate.npz')
            saved = load_archive(source_path)
            result = model.evaluate(saved['coefficients'])
            node = 8
            fields = result['fields']['nodes']
            independent_energy = model.node_weights * result['momentum']**2 / (2 * model.radii**2)
            independent_energy += model.radii**2 * (model.sampling.T @ (model.factors @ model.scalar)**2) / (2 * model.spacing)
            check(branch + '_parent_energy_all_nodes_reconstructed', abs(independent_energy - result['energy']).max() < 1e-13 and independent_energy.min() > 0)
            source = {'branch': branch, 'node': node, 'radius': float(model.radii[node]), 'mass_left': float(fields['mu'][node]), 'lapse_left': float(fields['N'][node]), 'energy': float(result['energy'][node]), 'spacing': float(model.spacing), 'parent_path': str(source_path.relative_to(root)), 'source_kind': 'actual_parent_nodal_energy_not_new_global_solution'}
            report['sources'].append(source)
            own(source_path)
            path = destination / (branch + '_source_snapshot.npz')
            np.savez_compressed(path, energy=result['energy'], radii=model.radii, scalar=model.scalar, momentum=result['momentum'], factors=model.factors, sampling=model.sampling, mu=fields['mu'], lapse=fields['N'])
            own(path, 'outputs')
        report['sources'].append({'branch': 'manufactured_zeta_0p2', 'radius': 6., 'mass_left': 1., 'lapse_left': .85, 'energy': 12., 'spacing': 1 / 64, 'source_kind': 'manufactured_stress_control_not_MTS_prediction', 'parent_path': None})
        widths = [1 / 2, 1 / 8, 1 / 32, 1 / 512, 1 / 8192, 1 / 1048576]
        for source in report['sources']:
            branch = source['branch']
            for name in ['beta22', 'beta33', 'beta23']:
                family = []
                for index, relative_width in enumerate(widths):
                    row, arrays = solve_layer(source['radius'], source['mass_left'], source['lapse_left'], source['energy'], source['spacing'] * relative_width, name)
                    source_peak = float((source['lapse_left'] * arrays['rho'] / (arrays['R'] * arrays['U'])).max())
                    row.update({'branch': branch, 'width_index': index, 'source_only_peak_P1': source_peak, 'width_times_source_peak_P1': row['width'] * source_peak})
                    bounds = limit_bounds(source['radius'], source['mass_left'], source['lapse_left'], source['energy'], row['width'])
                    row['analytic_bounds'] = bounds
                    row['proper_clock_transfer_if_horizontal_link_is_gluing'] = float(np.exp(row['I_background'] + row['I_source']))
                    row['proper_clock_mismatch_if_horizontal_link_is_gluing'] = float(np.expm1(row['I_background'] + row['I_source']))
                    prefix = branch + '_' + name + '_' + str(index)
                    check(prefix + '_derived_thin_limit_envelopes', all(row[key] <= bounds[key] + 1e-12 for key in ['root_limit_error', 'mass_limit_error', 'mean_limit_error', 'G_limit_error', 'P1_integral_limit_error']))
                    check(prefix + '_finite_geometry_and_positive_source', row['minimum_F'] > .1 and all(np.isfinite(value).all() for value in arrays.values()) and np.min(arrays['rho']) >= 0)
                    check(prefix + '_exact_finite_width_geometry_and_clock_identities', max(row['log_U_identity_error'], row['JC_over_R2_identity_error']) < 1e-10, [row['log_U_identity_error'], row['JC_over_R2_identity_error']])
                    check(prefix + '_derived_rate_bound_satisfied', row['constant_clock_peak_P1'] >= row['required_peak_P1_lower_bound'])
                    controls = action_controls(arrays, source['lapse_left'], row['width'])
                    check(prefix + '_all_compact_action_variations', max(max(item['lapse_action_constraint_error'], item['mass_action_force_error']) for item in controls) < 1e-10)
                    check(prefix + '_omitting_source_force_detected', min(item['missing_matter_force_negative_control'] for item in controls) > 1e-10)
                    for item in controls:
                        report['action_controls'].append({'branch': branch, 'profile': name, 'width_index': index, **item})
                    path = destination / (prefix + '_layer.npz')
                    np.savez_compressed(path, **arrays)
                    own(path, 'outputs')
                    report['layers'].append(row)
                    family.append(row)
                    save()
                check(branch + '_' + name + '_analytic_limit_bounds_shrink', all(family[-1]['analytic_bounds'][key] < family[0]['analytic_bounds'][key] / 1000 for key in ['root_limit_error', 'mass_limit_error', 'mean_limit_error', 'G_limit_error', 'P1_integral_limit_error']))
                check(branch + '_' + name + '_source_rate_has_derived_inverse_width_scaling', abs(family[-1]['width_times_source_peak_P1'] / family[0]['width_times_source_peak_P1'] - 1) < .01 and family[-1]['source_only_peak_P1'] / family[0]['source_only_peak_P1'] > .99 * family[0]['width'] / family[-1]['width'])
                finer, unused_arrays = solve_layer(source['radius'], source['mass_left'], source['lapse_left'], source['energy'], family[-1]['width'], name, order=128, tolerance=8e-14)
                check(branch + '_' + name + '_tighter_ODE_and_quadrature_control', max(abs(finer[key] - family[-1][key]) for key in ['root_right', 'mass_right', 'effective_U_trace', 'constant_clock_G', 'P1_integral']) < 1e-10)
                print(json.dumps({'branch': branch, 'profile': name, 'zeta': family[-1]['zeta'], 'mean_limit_error': family[-1]['mean_limit_error'], 'G_limit_error': family[-1]['G_limit_error'], 'peak_P1_at_thinnest_width': family[-1]['constant_clock_peak_P1'], 'zero_P1_lapse_ratio': family[-1]['zero_P1_lapse_ratio']}), flush=True)
        for branch in [source['branch'] for source in report['sources']]:
            final_rows = [row for row in report['layers'] if row['branch'] == branch and row['width_index'] == 5]
            check(branch + '_three_shapes_same_thin_limit', np.ptp([row['effective_U_trace'] for row in final_rows]) < 2e-8 and np.ptp([row['constant_clock_G'] for row in final_rows]) < 2e-8)
        for row in report['layers']:
            ratio_U = row['root_right'] / row['root_left_actual']
            transfer = row['proper_clock_transfer_if_horizontal_link_is_gluing']
            transported_density = row['constant_clock_J'] * ratio_U
            expected_density = np.exp(2 * row['I_background'])
            check(row['branch'] + '_' + row['profile'] + '_' + str(row['width_index']) + '_density_transport_is_not_proper_clock_matching', abs(transported_density - expected_density) < 1e-10 and transfer > 1 + 1e-8)
        zeta = .2
        ratio = np.exp(-zeta)
        midpoint_ratio = (1 - zeta / 2) / (1 + zeta / 2)
        logarithmic_mean = -np.expm1(-zeta) / zeta
        arithmetic_mean = (1 + ratio) / 2
        check('arithmetic_trace_is_detectably_different_extension', abs(ratio - midpoint_ratio) > 1e-4 and abs(1 - ratio - zeta * arithmetic_mean) > 1e-4)
        report['trace_negative_control'] = {'manufactured_zeta': zeta, 'derived_exponential_ratio': float(ratio), 'midpoint_Cayley_ratio': float(midpoint_ratio), 'derived_logarithmic_mean_per_Uleft': float(logarithmic_mean), 'arithmetic_mean_per_Uleft': float(arithmetic_mean), 'not_a_parent_selection_proof': True}
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        for name in ['annular_interface_layer_clock_20260912.py', Path(__file__).name]:
            path = root / 'scripts' / name
            compile(path.read_bytes(), str(path), 'exec')
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
