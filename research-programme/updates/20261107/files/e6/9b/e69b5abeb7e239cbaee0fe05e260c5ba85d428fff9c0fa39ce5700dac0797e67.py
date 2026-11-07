from derive_annular_source_gravity_20260914 import EvidenceRun
from validate_annular_native_shape_stress_v2_20260928 import DirectNodalKernel, archive, decimal_array, maximum
from decimal import Decimal, localcontext
from time import perf_counter
import contextlib
import csv
import hashlib
import json
import numpy as np
import sympy as sp


ZERO = Decimal(0)


def symbolic_covariance(evidence):
    area, lapse, metric, area_r = sp.symbols('A N F A_r', positive=True)
    area_rr, lapse_r, metric_r, generator, generator_r = sp.symbols('A_rr N_r F_r zeta zeta_r', real=True)
    coefficient = area**2 * lapse * sp.sqrt(metric) * area_r
    fields = [area, lapse, metric, area_r]
    radial = [area_r, lapse_r, metric_r, area_rr]
    variation = [-generator * area_r, -generator * lapse_r,
                 -generator * metric_r + 2 * metric * generator_r,
                 -generator * area_rr - generator_r * area_r]
    response = sum(sp.diff(coefficient, field) * delta for field, delta in zip(fields, variation))
    derivative = sum(sp.diff(coefficient, field) * value for field, value in zip(fields, radial))
    evidence.check('coframe_radial_scalar_identity', sp.simplify(response + generator * derivative) == 0)
    area_only = area**2 * lapse * sp.sqrt(metric)
    omitted = sum(sp.diff(area_only, field) * delta for field, delta in zip(fields, variation))
    omitted += generator * sum(sp.diff(area_only, field) * value for field, value in zip(fields, radial))
    evidence.check('missing_A_r_negative_control', sp.simplify(omitted - area_only * generator_r) == 0
                   and sp.simplify(omitted) != 0)
    stretch = sp.symbols('positive_coordinate_stretch', positive=True)
    transformed = coefficient.subs({metric: metric * stretch**2, area_r: area_r / stretch}, simultaneous=True)
    evidence.check('finite_radial_coordinate_coframe_identity', sp.simplify(transformed - coefficient) == 0)
    evidence.report['symbolic'] = dict(coframe=str(coefficient), missing_coframe_response=str(sp.simplify(omitted)))


def derivative_trace(edges, values, native):
    slopes = np.diff(values) / np.diff(edges)
    return np.array([(slopes[index - 1] + slopes[index]) / 2 if 0 < index < len(slopes)
                     else slopes[0 if index == 0 else -1] for index in native], dtype=object)


def main():
    evidence = EvidenceRun('annular-native-areal-lift-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 1800
    try:
        authority_path = evidence.output.parent / 'annular-native-shape-stress-validation-attempt02/status.json'
        authority = json.loads(authority_path.read_text())
        evidence.check('native_derivatives_independently_validated', authority['state'] == 'complete'
                       and all(check['passed'] for check in authority['checks']))
        evidence.own(authority_path)
        digests = {}
        for category in ['inputs', 'outputs']:
            for relative, digest in authority[category].items():
                if relative in digests and digests[relative] != digest:
                    raise RuntimeError('Conflicting input hashes')
                digests[relative] = digest
        for relative, digest in digests.items():
            path = evidence.root / relative
            evidence.check('hash:' + relative, path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest)
            evidence.own(path)
        evidence.own(evidence.root / 'DERIVATION-20260928-native-areal-metric-lift.md')
        symbolic_covariance(evidence)
        main_path = evidence.output.parent / 'annular-native-shape-stress-attempt01/status.json'
        parent = json.loads(main_path.read_text())
        evidence.own(main_path)
        response_rows, ward_rows, power_rows = [], [], []
        with localcontext() as context:
            context.prec = 80
            for case in parent['cases']:
                print(json.dumps(dict(stage=case['branch'] + '-' + case['level'], seconds=perf_counter() - started)), flush=True)
                packet = json.loads((evidence.root / case['sources']['packet']).read_text())
                kernel = DirectNodalKernel(packet['mesh'], packet['gram_support'], case['branch'] == 'MTS-primary')
                for probe, relative in enumerate(case['probe_paths']):
                    if perf_counter() > deadline:
                        raise RuntimeError('Safe areal-lift validation boundary')
                    raw = archive(evidence.root / relative)
                    edges, field, beta, beta_r, load, gradient, tests = [decimal_array(raw[key])
                        for key in ['edges', 'field', 'beta', 'beta_radial', 'load', 'edge_gradient', 'edge_tests']]
                    radius = edges[kernel.native]
                    energy_atoms = beta * load
                    source = edges[kernel.anchor]
                    source_velocity = Decimal(str(raw['source_velocity']))
                    dilation = np.array([1 / (source - edges[0]) if point < source else -1 / (edges[-1] - source)
                                         for point in radius], dtype=object)
                    expected_power = -energy_atoms * dilation * source_velocity
                    actual_power = decimal_array(raw['kernel_power'])
                    power_error = maximum(expected_power - actual_power)
                    evidence.check(relative + ':actual_source_affine_power', power_error <= Decimal('1e-30') * max(maximum(actual_power), Decimal('1e-80')))
                    power_rows.append(dict(branch=case['branch'], level=case['level'], probe=probe,
                        maximum_kernel_power=str(maximum(actual_power)), maximum_affine_discrepancy=str(power_error)))
                    dilation_factor = Decimal('1.0001')
                    dilated_energy = kernel.evaluate(dilation_factor * edges, field, dilation_factor**3 * beta)['energy']
                    expected_energy = dilation_factor**2 * Decimal(str(raw['energy']))
                    evidence.check(relative + ':finite_global_areal_scaling',
                        abs(dilated_energy - expected_energy) <= Decimal('1e-30') * max(abs(expected_energy), Decimal('1e-80')))
                    for test, edge_test in enumerate(tests):
                        native_test = edge_test[kernel.native]
                        trace = derivative_trace(edges, edge_test, kernel.native)
                        shape = sum(gradient * edge_test, ZERO)
                        area_only = sum(2 * energy_atoms * native_test / radius, ZERO)
                        coframe = sum(energy_atoms * trace, ZERO)
                        coefficient = sum(load * beta_r * native_test, ZERO)
                        old_spatial = coefficient - coframe
                        new_spatial = shape + coefficient
                        angular_difference = shape + coframe
                        evidence.check(relative + ':distributional_Ward:' + str(test),
                            abs(new_spatial - old_spatial - angular_difference) <= Decimal('1e-30') * max(abs(shape), abs(coframe), abs(coefficient), Decimal('1e-80')))
                        ward_rows.append(dict(branch=case['branch'], level=case['level'], probe=probe, test=test,
                            material_label=float(raw['label']), kernel_shape=str(shape), coframe=str(coframe),
                            area_only=str(area_only), area_action_derivative=str(shape + area_only + coframe),
                            old_spatial=str(old_spatial), new_spatial=str(new_spatial), angular_difference=str(angular_difference)))
                        for sector in ['areal', 'lapse', 'radial_metric']:
                            if sector == 'areal':
                                predicted = shape + area_only + coframe
                                term_scale = sum(abs(gradient * edge_test), ZERO)
                                term_scale += sum(abs(2 * energy_atoms * native_test / radius), ZERO) + sum(abs(energy_atoms * trace), ZERO)
                                bounds = [width / abs(change) for width, change in zip(np.diff(edges), np.diff(edge_test)) if change]
                                bounds += [point / abs(change) for point, change in zip(radius, native_test) if change]
                            else:
                                factor = Decimal(1) if sector == 'lapse' else Decimal('0.5')
                                predicted = factor * sum(energy_atoms * native_test, ZERO)
                                term_scale = factor * sum(abs(energy_atoms * native_test), ZERO)
                                bounds = [1 / abs(value) for value in native_test if value]
                            step = Decimal('0.001') * min(bounds, default=Decimal(1))
                            differences = []
                            for resolution in range(3):
                                amount = step / 2**resolution
                                energies = []
                                for sign in [1, -1]:
                                    increment = sign * amount
                                    positions = edges + increment * edge_test if sector == 'areal' else edges
                                    if sector == 'areal':
                                        coefficients = beta * (1 + increment * native_test / radius)**2 * (1 + increment * trace)
                                    elif sector == 'lapse':
                                        coefficients = beta * (1 + increment * native_test)
                                    else:
                                        coefficients = beta * np.array([(1 + increment * value).sqrt() for value in native_test], dtype=object)
                                    evidence.check(relative + ':positive_coframe:' + str(test) + ':' + sector + ':' + str(resolution) + ':' + str(sign),
                                        min(coefficients) > 0 and min(np.diff(positions)) > 0)
                                    energies.append(kernel.evaluate(positions, field, coefficients)['energy'])
                                differences.append((energies[0] - energies[1]) / (2 * amount))
                            extrapolated = (4 * differences[2] - differences[1]) / 3
                            error = abs(extrapolated - predicted)
                            tolerance = Decimal('1e-22') + Decimal('2e-7') * term_scale
                            evidence.check(relative + ':metric_derivative:' + str(test) + ':' + sector, error <= tolerance,
                                           dict(error=str(error), tolerance=str(tolerance)))
                            response_rows.append(dict(branch=case['branch'], level=case['level'], probe=probe, test=test,
                                sector=sector, step=str(step), predicted=str(predicted), coarse=str(differences[0]), middle=str(differences[1]),
                                fine=str(differences[2]), extrapolated=str(extrapolated), error=str(error), tolerance=str(tolerance)))
                evidence.report['cases'].append(dict(branch=case['branch'], level=case['level'], raw_probes=len(case['probe_paths'])))
                evidence.save()
        for name, rows in [('areal-metric-responses.csv', response_rows), ('native-spatial-Ward.csv', ward_rows), ('source-affine-power.csv', power_rows)]:
            path = evidence.output / name
            with path.open('w', newline='', encoding='utf-8') as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, metric_derivative_cases=len(response_rows),
            signed_pairs=3 * len(response_rows), selected_label_Ward_rows=len(ward_rows),
            maximum_metric_derivative_error=str(max(Decimal(row['error']) for row in response_rows)),
            specified_Gram_areal_lift=True, all_label_metric_evolution_recomputed=False,
            full_spacetime_covariance_proven=False, mixed_current_recomputed=False, new_nonlinear_solves=0)
        completion = evidence.output / 'completion.txt'
        with completion.open('w', encoding='utf-8') as handle, contextlib.redirect_stdout(handle):
            evidence.complete()
        evidence.own(completion, 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=evidence.report['seconds'],
            derivative_cases=len(response_rows), maximum_error=evidence.report['maximum_metric_derivative_error'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
