import hashlib
import json
import re
import traceback
from datetime import datetime
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    import sympy as sp
    from scipy.integrate import solve_ivp
    from annular_clock_reservoir_coupling_20260913 import ClockReservoirPreparation, ProperClockDrive
    from annular_source_second_jet_20260913 import SourceSecondJet

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260913'
    destination = intake / 'annular-source-second-jet-final-integrity.json'
    snapshot = intake / 'annular-source-second-jet-resume-snapshot.md'
    if destination.exists() or snapshot.exists():
        raise FileExistsError('Existing evidence must not be overwritten.')
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'independent_cases': [],
              'full_C2_evaluated': True, 'valid_for_physics_claim': False, 'full_GR_limit_proven': False,
              'full_geometric_evolution': False, 'boundary_histories_complete': False, 'full_first_jet_closed': False,
              'apparatus_microphysics_derived': False, 'unique_parent_regularizer_derived': False,
              'source_support_stresses_derived': False, 'full_physical_radial_port_action_signed': False,
              'new_fundamental_MTS_field_claimed': False, 'point_force_adopted': False,
              'protected_scan_scope': 'mtime since 2026-09-13T11:03:10Z; not pre-turn content hashes'}

    def save():
        destination.write_text(json.dumps(report, indent=2) + '\n')

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    save()
    try:
        directory = intake / 'annular-source-second-jet-attempt01'
        batch = json.loads((directory / 'status.json').read_text())
        check('eight_completed_second_jets_with_passing_gates', batch['state'] == 'complete' and len(batch['cases']) == 8 and batch['C2_all_pass'] and batch['P2_boundary_all_pass'] and all(row['passed'] for row in batch['checks']))
        for key, value in report.items():
            if value is False:
                check(key + '_remains_false', batch[key] is False)
        for table in ['inputs', 'outputs']:
            for filename, expected in batch[table].items():
                if filename in report['inputs'] and report['inputs'][filename] != expected:
                    raise RuntimeError('Inconsistent inherited hash: ' + filename)
                if filename not in report['inputs']:
                    if hashlib.sha256((root / filename).read_bytes()).hexdigest() != expected:
                        raise RuntimeError('Changed inherited evidence: ' + filename)
                    report['inputs'][filename] = expected
        check('all_inherited_hashes_match', True, len(report['inputs']))
        for path in directory.iterdir():
            if not path.is_file():
                continue
            own(path, 'outputs')
            if path.name.startswith('executed-'):
                check(path.name + '_immutable_source_matches', path.read_bytes() == (root / 'scripts' / path.name.removeprefix('executed-')).read_bytes())
            if path.suffix == '.npz':
                with np.load(path, allow_pickle=False) as archive:
                    check(path.name + '_finite_arrays', all(np.isfinite(archive[key]).all() for key in archive.files))

        radius, root_f, lapse, coupling = sp.symbols('R U N kappa', positive=True)
        kernel, kernel1, momentum1, momentum1_r, lapse_rate, lapse_rate_r = sp.symbols('K K1 P1 P1r L Lr')
        energy, energy1, energy2, sigma, sigma1, sigma2 = sp.symbols('eps eps1 eps2 sigma sigma1 sigma2')
        mass = radius * (1 - root_f**2) / 2
        mass_r = coupling * (root_f**2 * energy + root_f * sigma)
        root_r = (1 - root_f**2) / (2 * radius * root_f) - coupling * (root_f * energy + sigma) / radius
        lapse_r = lapse * ((1 - root_f**2) / (2 * radius * root_f**2) + coupling * energy / radius) - coupling * root_f * momentum1
        generator = coupling * root_f * momentum1 / lapse
        mass1 = -coupling * root_f * kernel / lapse
        c2 = mass1 / (radius**2 * root_f**4) + coupling * energy1 / radius - lapse_rate_r - lapse_rate * generator
        kernel_r = -2 * generator * kernel - lapse * root_f * energy1 - lapse * sigma1
        kernel1_r = -3 * generator * kernel1 - 2 * c2 * kernel - lapse * root_f * (lapse_rate - mass1 / (radius * root_f**2)) * energy1 - lapse * root_f * energy2 - lapse * lapse_rate * sigma1 - lapse * sigma2
        mass2 = -coupling * root_f / lapse * (kernel1 - (lapse_rate + mass1 / (radius * root_f**2)) * kernel) - coupling**2 * radius * root_f**6 * momentum1**2

        def radial_derivative(expression):
            fields = [radius, root_f, lapse, kernel, kernel1, momentum1, lapse_rate]
            rates = [1, root_r, lapse_r, kernel_r, kernel1_r, momentum1_r, lapse_rate_r]
            return sum(sp.diff(expression, field) * rate for field, rate in zip(fields, rates))

        mass1_r, mass2_r = radial_derivative(mass1), radial_derivative(mass2)
        constraint2 = mass2_r / (coupling * root_f) + 2 * mass1_r * mass1 / (coupling * radius * root_f**3)
        constraint2 += mass_r * (mass2 / (coupling * radius * root_f**3) + 3 * mass1**2 / (coupling * radius**2 * root_f**5))
        constraint2 += mass2 * energy / (radius * root_f) + mass1**2 * energy / (radius**2 * root_f**3) + 2 * mass1 * energy1 / (radius * root_f) - root_f * energy2
        constraint2 += 2 * coupling * root_f**3 * ((root_f**2 / 2 - 3 * mass_r + 3 * mass / radius) * momentum1**2 + radius * root_f**2 * momentum1 * momentum1_r)
        constraint2 += 2 * coupling**2 * root_f**5 * energy * momentum1**2 - sigma2 + coupling**2 * root_f**4 * sigma * momentum1**2
        constraint2 += -kernel * c2 / lapse + 2 * lapse_rate * kernel * generator / lapse - 2 * kernel1 * generator / lapse
        reduced = sp.cancel(constraint2)
        check('exact_local_C2_identity_from_C0_and_differentiated_Ward', reduced == 0, str(reduced))
        report['symbolic_scope'] = 'Formal smooth interior identity on initial C0, scalar/source equations and differentiated transport Ward; no causal existence assertion.'

        prior = json.loads((intake / 'annular-clock-reservoir-coupling-attempt01/status.json').read_text())
        selected_rows = [row for row in prior['cases'] if row['case'] == 0 and row['reservoir_energy'] == .001]
        for row in selected_rows:
            branch = row['branch']
            with np.load(root / 'source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03' / (branch + '_source_snapshot.npz'), allow_pickle=False) as archive:
                source = {key: archive[key].copy() for key in archive.files}
            with np.load(intake / 'annular-finite-width-boundary-cut-attempt01' / (branch + '_0_prepared_collar.npz'), allow_pickle=False) as archive:
                prepared = {key: archive[key].copy() for key in archive.files}
            with np.load(root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02' / ('canonical_N16_' + branch + '_sample0.npz'), allow_pickle=False) as archive:
                clock = archive['affine_clock'].copy()
                acceleration = float(archive['endpoint_acceleration'][-1])
            preparation = ClockReservoirPreparation(source, branch != 'GR', prepared['kinetic_seed'], float(prepared['outer_clock']), prepared['drive'], row['width'], row['shape'], reservoir_energy=row['reservoir_energy'])
            model = preparation.build(np.asarray(row['coefficients']))
            driver = ProperClockDrive(model, float(clock[1]), acceleration)
            jet = SourceSecondJet(model, driver)
            offsets = np.array([-.4, -.1, .1, .4])
            data = jet.completed_layer(offsets)
            independent_force_rate = np.zeros_like(data['Gchi1'])
            independent_potential_second = np.zeros_like(data['d2'])
            step = 1e-24j
            for factor in range(len(model.factors)):
                mask = model.factor == factor
                indices = model.node[mask]
                initial_jacobians, second_maps = data['J'][:, mask], data['T2'][:, mask]
                for local, node in enumerate(indices):
                    anchor_time = step / initial_jacobians[:, local]
                    transported = initial_jacobians * anchor_time[:, None] + .5 * second_maps * anchor_time[:, None]**2
                    evolving_jacobian = initial_jacobians + second_maps * anchor_time[:, None]
                    scalar_values = data['chi'][:, indices] + data['q'][:, indices] * transported + .5 * data['q1'][:, indices] * transported**2
                    coefficient_values = data['C'][:, indices] + data['C1'][:, indices] * transported
                    amplitude = scalar_values @ model.factors[factor, indices]
                    density = np.sum(model.sampling[factor, indices] * evolving_jacobian * coefficient_values, axis=1)
                    force = -model.factors[factor, node] * amplitude * density / (model.spacing * evolving_jacobian[:, local])
                    independent_force_rate[:, node] += force.imag / step.imag
                    physical_first = initial_jacobians / initial_jacobians[:, local, None]
                    physical_second = second_maps / initial_jacobians[:, local, None]**2 - initial_jacobians * second_maps[:, local, None] / initial_jacobians[:, local, None]**3
                    scalar_first = data['q'][:, indices] * physical_first
                    scalar_second = data['q1'][:, indices] * physical_first**2 + data['q'][:, indices] * physical_second
                    amplitude0 = data['chi'][:, indices] @ model.factors[factor, indices]
                    amplitude1 = scalar_first @ model.factors[factor, indices]
                    amplitude2 = scalar_second @ model.factors[factor, indices]
                    independent_potential_second[:, node] += model.sampling[factor, node] * (amplitude1**2 + amplitude0 * amplitude2) / model.spacing
            force_error = float(abs(independent_force_rate - data['Gchi1']).max())
            potential_error = float(abs(independent_potential_second - data['d2']).max())
            check(branch + '_inverse_anchor_time_force_derivative', force_error < 1e-9, force_error)
            check(branch + '_composed_inverse_time_potential_second', potential_error < 1e-9, potential_error)

            metric = data['metric1']
            mass_rate_ratio = metric['mu1'] / (data['R'] * metric['U']**2)
            chart_term = model.coupling**2 * metric['U']**4 * metric['P1']**2
            for arbitrary_n2_ratio in [0., .017]:
                coefficient_second_ratio = arbitrary_n2_ratio - 2 * metric['L'] * mass_rate_ratio - data['mu2'] / (data['R'] * metric['U']**2) - mass_rate_ratio**2 - 2 * chart_term
                velocity_second = coefficient_second_ratio * data['q'] + 2 * (metric['L'] - mass_rate_ratio) * metric['N'] * metric['U'] * data['p1_driven'] / data['R']**2 + metric['N'] * metric['U'] * data['p2'] / data['R']**2
                prescribed_third = 3 * driver.proper_acceleration * metric['N'][:, -1]**2 * metric['L'][:, -1] + data['q'][:, -1] * (arbitrary_n2_ratio - chart_term[:, -1])
                check(branch + '_source_jerk_independent_of_N2_choice_' + str(arbitrary_n2_ratio), abs(velocity_second[:, -1] - prescribed_third).max() < 1e-9)

            candidates = np.flatnonzero(model.node == len(model.radii) - 1)
            pair = candidates[np.argmax(abs(model.target_base[candidates] - model.anchor_base[candidates]))]
            offset = .25
            anchor = model.anchor_base[pair] + model.width * offset
            target = model.target_base[pair] + model.width * offset

            def map_equation(radius_value, state):
                field = jet.first_fields(np.array([radius_value]))
                primitive_c1 = model.coupling * field['U'][0] * field['P1'][0] / field['N'][0]
                direct_c2 = model.coupling * field['U'][0] / field['N'][0] * (field['P2'][0] - 2 * (field['mu1'][0] / (radius_value * field['U'][0]**2) + field['L'][0]) * field['P1'][0])
                return [primitive_c1 * state[0], primitive_c1 * state[1] + direct_c2 * state[0]**2]

            map_solution = solve_ivp(map_equation, (anchor, target), [1., 0.], method='DOP853', rtol=2e-12, atol=2e-14, max_step=abs(target-anchor)/32)
            if not map_solution.success:
                raise RuntimeError(map_solution.message)
            expected_maps = jet.transport_jet([offset])
            map_error = float(max(abs(map_solution.y[0, -1] - expected_maps['J'][0, pair]), abs(map_solution.y[1, -1] - expected_maps['T2'][0, pair])))
            check(branch + '_independent_second_transport_map_ODE', map_error < 1e-9, map_error)

            direct_current_errors = []
            points, gauss_weights = np.polynomial.legendre.leggauss(24)
            for physical_cut in model.radii[[0, -1]]:
                cuts = np.concatenate([[-.5, .5], (physical_cut-model.target_base)/model.width, (physical_cut-model.anchor_base)/model.width])
                cuts = np.unique(cuts[(cuts >= -.5) & (cuts <= .5)])
                direct = 0.
                evaluation_g = model.metric(np.array([physical_cut]))['g'][0]
                evaluation_primitive = jet.primitive(np.array([physical_cut]))[0]
                for lower, upper in zip(cuts[:-1], cuts[1:]):
                    translations = (lower+upper)/2 + (upper-lower)*points/2
                    part = jet.transport_jet(translations)
                    target_radii = model.target_base + model.width * translations[:, None]
                    anchor_radii = model.anchor_base + model.width * translations[:, None]
                    hits = (physical_cut > np.minimum(target_radii, anchor_radii)) & (physical_cut < np.maximum(target_radii, anchor_radii))
                    from annular_finite_width_bulk_current_20260913 import shape_weight
                    integrand = shape_weight(translations, model.shape) * np.sum((part['global_current_jet'] - 2 * evaluation_primitive * part['global_I']) * hits * model.orientation, axis=1)
                    direct += (upper-lower)/2 * gauss_weights @ integrand
                direct *= np.exp(-3 * evaluation_g)
                direct_current_errors.append(float(abs(direct - jet.current_second(np.array([physical_cut]))['K1'][0])))
            check(branch + '_independent_split_layer_current_derivative_integral', max(direct_current_errors) < 1e-10, direct_current_errors)
            report['independent_cases'].append({'branch': branch, 'force_derivative_error': force_error, 'potential_second_error': potential_error, 'transport_map_error': map_error, 'current_derivative_errors': direct_current_errors})

        check('constant_lapse_controls_fail_boundary_not_hidden', all(row['maximum_endpoint_P2'] > 1e-5 for row in batch['constant_lapse_controls']))
        check('omission_controls_remain_nonzero', all(row['omit_source_C2'] > .01 and row['omit_radial_C2'] > .01 and row['omit_connection_C2'] > 1e-7 and row['omit_P_squared_C2'] > 1e-7 for row in batch['cases']))
        check('inner_mass_acceleration_reported_not_set_to_zero', all(abs(row['required_inner_mass_acceleration']) > .001 for row in batch['cases']))
        note = root / 'DERIVATION-20260913-source-coupled-second-jet-and-C2-propagation.md'
        for citation in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')):
            if citation.endswith(('.py', '.md', '.json', '.npz')):
                check('cited_path_exists_' + citation, (root / citation).is_file())
        own(note, 'outputs')
        for stem in ['annular_source_second_jet', 'derive_annular_source_second_jet', 'verify_annular_source_second_jet']:
            path = root / 'scripts' / (stem + '_20260913.py')
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('three_scripts_compile_without_bytecode', True)
        protected = root.parent / 'formalization-workbench'
        check('protected_workbench_exists', protected.is_dir())
        start = datetime.fromisoformat('2026-09-13T11:03:10+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
        check('protected_mtime_changed_count_zero', not changed, changed)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot, 'outputs')
        report.update({'state': 'complete', 'main_run_checks': len(batch['checks']), 'prepared_cases': len(batch['cases']), 'C2_all_pass': batch['C2_all_pass'],
                       'P2_boundary_all_pass': batch['P2_boundary_all_pass'], 'protected_changed_count': len(changed),
                       'maximum_C2': max(row['maximum_C2'] for row in batch['cases']), 'maximum_endpoint_P2': max(row['maximum_endpoint_P2'] for row in batch['cases']),
                       'formal_local_C2_identity_verified': True})
        save()
        print(json.dumps({key: report[key] for key in ['state', 'main_run_checks', 'prepared_cases', 'maximum_C2', 'maximum_endpoint_P2', 'protected_changed_count']} | {'seal_checks': len(report['checks'])}), flush=True)
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
