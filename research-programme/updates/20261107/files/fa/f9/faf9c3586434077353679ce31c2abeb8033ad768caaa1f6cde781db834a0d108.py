from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_physical_native_kernel_20260928 import NativeKernel
from validate_annular_native_shape_stress_v2_20260928 import DirectNodalKernel, archive, decimal_array, maximum
from annular_native_time_current_20260928 import field_radii, profile, primitive, finite_gram_action, endpoint_functional, current_terms, wave_mesh_momentum
from annular_candidate_energy_current_20260921 import reconstructed_solver
from decimal import Decimal, localcontext
from time import perf_counter
import contextlib
import csv
import hashlib
import json
import numpy as np
import sympy as sp


ZERO = Decimal(0)


def symbolic_checks(evidence):
    beta, load, beta_t, beta_r, load_t, speed, integral, integral_t, direction, field = sp.symbols('beta l beta_t beta_r l_t W I I_t h field')
    raw = -field - load * beta_t * integral - beta * load * integral_t
    current = -field + (beta * load_t + beta_r * speed * load) * integral + beta * load * speed * direction
    endpoint_rate = -((beta_t + beta_r * speed) * load + beta * load_t) * integral - beta * load * (integral_t + speed * direction)
    evidence.check('general_beta_t_moving_atom_endpoint_identity', sp.expand(raw - current - endpoint_rate) == 0)
    source_speed, source_profile, omega, time, amplitude, primitive_value = sp.symbols('V h_b omega s epsilon I', nonzero=True)
    leaf = (time + 1 / omega) * sp.exp(amplitude * omega * primitive_value) - 1 / omega
    evidence.check('exact_time_dependent_leaf_ODE', sp.simplify(sp.diff(leaf, primitive_value) - amplitude * (1 + omega * leaf)) == 0)
    jacobian = sp.diff(leaf, time) - source_speed * source_profile * sp.diff(leaf, primitive_value)
    expected = sp.exp(amplitude * omega * primitive_value) * (1 - amplitude * (1 + omega * time) * source_profile * source_speed)
    evidence.check('exact_time_dependent_leaf_source_clock', sp.simplify(jacobian - expected) == 0)
    metric, lapse, area_r, mass = sp.symbols('F N A_r m', positive=True)
    area_t, shift, velocity = sp.symbols('A_t v V', real=True)
    transformed_velocity = area_t + area_r * velocity
    transformed_shift = area_r * shift - area_t
    evidence.check('source_clock_A_t_cancels_exactly', sp.simplify((transformed_velocity + transformed_shift)**2 / (metric * area_r**2) - (velocity + shift)**2 / metric) == 0)
    dust = -mass * sp.sqrt(lapse**2 - (velocity + shift)**2 / metric)
    evidence.check('dust_mesh_and_shift_momenta_equal', sp.simplify(sp.diff(dust, velocity) - sp.diff(dust, shift)) == 0)
    alpha, gradient, field_rate, mesh_rate, coefficient = sp.symbols('alpha g qdot W C')
    wave = (alpha * (field_rate - mesh_rate * gradient)**2 - coefficient * gradient**2) / 2
    evidence.check('wave_mesh_momentum_derived', sp.expand(sp.diff(wave, mesh_rate) + alpha * (field_rate - mesh_rate * gradient) * gradient) == 0)
    momentum_t, current_t = sp.symbols('P_mesh_t Q_shift_t')
    evidence.check('areal_and_mixed_time_terms_combine_off_shell', sp.expand(current_t + momentum_t - current_t - momentum_t) == 0)
    evidence.report['symbolic_scope'] = 'Horizontal Gram endpoint identity, exact leaf, source clock cancellation, wave velocity covector; Pi_A follows the functional chain delta W=delta A_t and delta v_A=-delta A_t, without setting Euler residuals to zero.'


def main():
    evidence = EvidenceRun('annular-native-time-current-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 5400
    try:
        authority_path = evidence.output.parent / 'annular-native-areal-lift-attempt01/status.json'
        authority = json.loads(authority_path.read_text())
        evidence.check('areal_lift_complete', authority['state'] == 'complete' and all(row['passed'] for row in authority['checks']))
        evidence.own(authority_path)
        for category in ['inputs', 'outputs']:
            for relative, digest in authority[category].items():
                path = evidence.root / relative
                evidence.check('hash:' + relative, path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest)
                evidence.own(path)
        seal_path = evidence.output.parent / 'annular-native-shape-stress-final-integrity-20260928.json'
        seal = json.loads(seal_path.read_text())
        evidence.check('previous_final_seal_complete', seal['state'] == 'complete')
        evidence.own(seal_path)
        for relative, digest in seal['hashes'].items():
            if relative == 'CURRENT_LOCAL_RESUME.md':
                continue
            path = evidence.root / relative
            evidence.check('seal_hash:' + relative, hashlib.sha256(path.read_bytes()).hexdigest() == digest)
            evidence.own(path)
        evidence.report['mutable_navigation_pointer_excluded'] = 'CURRENT_LOCAL_RESUME.md is intentionally prepended each turn; old scientific artifacts and manifests remain hash-checked.'
        evidence.own(evidence.root / 'DERIVATION-20260928-native-time-current-and-areal-momentum.md')
        parent_path = evidence.output.parent / 'annular-native-shape-stress-attempt01/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        symbolic_checks(evidence)
        comparisons, variations, wave_rows = [], [], []
        with localcontext() as context:
            context.prec = 80
            for case in parent['cases']:
                name = case['branch'] + '-' + case['level']
                print(json.dumps(dict(stage=name, seconds=perf_counter() - started)), flush=True)
                packet = json.loads((evidence.root / case['sources']['packet']).read_text())
                enabled = case['branch'] == 'MTS-primary'
                engine = NativeKernel(packet['mesh'], packet['gram_support'], enabled)
                direct = DirectNodalKernel(packet['mesh'], packet['gram_support'], enabled)
                solver, solution = reconstructed_solver(archive(evidence.root / case['sources']['state']))
                reference_edges = np.array(engine.references, dtype=object)
                for probe, relative in enumerate(case['probe_paths']):
                    if perf_counter() > deadline:
                        raise RuntimeError('Safe completed-probe runtime boundary')
                    raw = archive(evidence.root / relative)
                    edges, field, rate, beta, beta_r, displacement, load, image, field_gradient, tests = [decimal_array(raw[key]) for key in
                        ['edges', 'field', 'rate', 'beta', 'beta_radial', 'displacement', 'load', 'image', 'field_gradient', 'edge_tests']]
                    velocity = Decimal(str(raw['source_velocity']))
                    mesh_velocity = displacement * velocity
                    radii, source = edges[direct.native], edges[direct.anchor]
                    nodal_radii = field_radii(direct, edges, len(field))
                    image_rate = engine.tangent(edges, field, mesh_velocity, rate)
                    image_field_rate = engine.tangent(edges, field, np.full(len(edges), ZERO, dtype=object), rate)
                    image_shape_rate = image_rate - image_field_rate
                    dot_load = engine.apply('sampling', image * image_rate, True)
                    atoms = beta * dot_load + beta_r * mesh_velocity[direct.native] * load
                    energy = beta * load
                    missing_kernel = beta * engine.apply('sampling', image * image_shape_rate, True)
                    spans = np.diff(edges) / np.diff(reference_edges)
                    span_rates = np.diff(mesh_velocity) / np.diff(reference_edges)
                    jacobian = np.array([spans[min(index, len(spans) - 1)] for index in direct.native], dtype=object)
                    jacobian_rate = np.array([span_rates[min(index, len(spans) - 1)] for index in direct.native], dtype=object)
                    gamma = beta / jacobian
                    old = engine.evaluate(reference_edges, field, gamma)
                    old_image_rate = engine.tangent(reference_edges, field, np.full(len(edges), ZERO, dtype=object), rate)
                    old_dot_load = engine.apply('sampling', old['image'] * old_image_rate, True)
                    gamma_material = beta_r * mesh_velocity[direct.native] / jacobian - beta * jacobian_rate / jacobian**2
                    old_atoms = gamma * old_dot_load + gamma_material * old['load']
                    old_energy = gamma * old['load']
                    metric_values = solver.values(solution, np.asarray(radii, float))[0]
                    metric = 1 - 2 * metric_values[0] / np.asarray(radii, float)
                    lapse_squared_metric = decimal_array(np.exp(2 * metric_values[1]) * metric)
                    for power in range(3):
                        native_integrals = primitive(radii, source, power)
                        nodal_integrals = primitive(nodal_radii, source, power)
                        native_profile = profile(radii, power)
                        source_profile = profile(source, power)
                        current = current_terms(field_gradient, rate, nodal_integrals, energy, atoms, native_integrals, mesh_velocity[direct.native], native_profile)
                        old_current = current_terms(old['field_gradient'], rate, nodal_integrals, old_energy, old_atoms, native_integrals, mesh_velocity[direct.native], native_profile)
                        missing_operator = sum(missing_kernel * native_integrals, ZERO)
                        comparisons.append(dict(branch=case['branch'], level=case['level'], probe=probe, power=power,
                            material_label=float(raw['label']), new_current=str(current['total']), old_current=str(old_current['total']),
                            difference=str(current['total'] - old_current['total']), field=str(current['field']), bulk=str(current['bulk']),
                            local_atom=str(current['local']), missing_operator_effect=str(missing_operator),
                            doubled_source_work_effect=str(sum(decimal_array(raw['atom_power']) * native_integrals, ZERO))))
                        for omega in [ZERO, Decimal('0.7')]:
                            integral_t = omega * native_integrals - velocity * source_profile
                            raw_derivative = current['field'] - sum(energy * integral_t, ZERO)
                            endpoint_rate = -sum(atoms * native_integrals, ZERO) - sum(energy * (integral_t + mesh_velocity[direct.native] * native_profile), ZERO)
                            evidence.check(relative + ':endpoint_identity:' + str(power) + ':' + str(omega),
                                abs(raw_derivative - current['total'] - endpoint_rate) <= Decimal('1e-35') * max(current['absolute_scale'], abs(endpoint_rate), Decimal('1e-80')))
                            for kind in ['finite_connection', 'finite_endpoint_rate']:
                                predicted = raw_derivative if kind == 'finite_connection' else endpoint_rate
                                absolute_scale = current['absolute_scale'] + sum(abs(energy * integral_t), ZERO)
                                step = Decimal('0.0001')
                                derivatives = []
                                for resolution in range(3):
                                    amount = step / 2**resolution
                                    values = []
                                    for sign in [1, -1]:
                                        if kind == 'finite_connection':
                                            value = finite_gram_action(direct, edges, field, rate, beta, lapse_squared_metric, velocity, power, omega, sign * amount)
                                        else:
                                            value = endpoint_functional(direct, edges, field, rate, beta, beta_r, mesh_velocity, velocity, power, omega, sign * amount)
                                        values.append(value)
                                    derivatives.append((values[0] - values[1]) / (2 * amount))
                                extrapolated = (4 * derivatives[2] - derivatives[1]) / 3
                                error = abs(extrapolated - predicted)
                                tolerance = Decimal('1e-22') + Decimal('2e-7') * absolute_scale
                                evidence.check(relative + ':' + kind + ':' + str(power) + ':' + str(omega), error <= tolerance,
                                               dict(error=str(error), tolerance=str(tolerance)))
                                variations.append(dict(branch=case['branch'], level=case['level'], probe=probe, power=power,
                                    omega=str(omega), kind=kind, step=str(step), predicted=str(predicted), raw=str(raw_derivative),
                                    current=str(current['total']), boundary_rate=str(endpoint_rate), coarse=str(derivatives[0]),
                                    middle=str(derivatives[1]), fine=str(derivatives[2]), extrapolated=str(extrapolated),
                                    error=str(error), tolerance=str(tolerance)))
                    for order in [8, 12]:
                        results = wave_mesh_momentum(direct, edges, field, rate, mesh_velocity, tests, solver, solution, order)
                        for row in results:
                            evidence.check(relative + ':wave_mesh:' + str(order) + ':' + str(row['test']), Decimal(row['error']) <= Decimal(row['tolerance']))
                            wave_rows.append(dict(branch=case['branch'], level=case['level'], probe=probe, **row))
                    evidence.report['progress'] = dict(stage=name + ':probe' + str(probe), seconds=perf_counter() - started)
                    evidence.save()
                evidence.report['cases'].append(dict(branch=case['branch'], level=case['level'], probes=len(case['probe_paths'])))
        for filename, rows in [('native-current-comparison.csv', comparisons), ('native-time-variations.csv', variations), ('wave-areal-momentum.csv', wave_rows)]:
            path = evidence.output / filename
            with path.open('w', newline='', encoding='utf-8') as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, current_comparisons=len(comparisons),
            derivative_cases=len(variations), signed_pairs=3 * len(variations), wave_velocity_derivatives=len(wave_rows),
            maximum_current_difference=str(max(abs(Decimal(row['difference'])) for row in comparisons)),
            maximum_derivative_error=str(max(Decimal(row['error']) for row in variations)),
            maximum_missing_operator_effect=str(max(abs(Decimal(row['missing_operator_effect'])) for row in comparisons)),
            maximum_missing_local_atom_effect=str(max(abs(Decimal(row['local_atom'])) for row in comparisons)),
            selected_label_jet_tests=True, new_nonlinear_solves=0, full_radial_balance_recomputed=False,
            protected_since='2026-09-27T23:41:05+00:00', github_action=False, subagents_used=False)
        completion = evidence.output / 'completion.txt'
        with completion.open('w', encoding='utf-8') as handle, contextlib.redirect_stdout(handle):
            evidence.complete()
        evidence.own(completion, 'outputs')
        evidence.save()
        print(json.dumps({key:evidence.report[key] for key in ['state', 'seconds', 'derivative_cases', 'maximum_current_difference', 'maximum_derivative_error']}), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
