from stage165_common import *
from stable_phase_sources import StablePhaseSources
from reconcile_reference import cardinal_weights
from assemble_repair import decimal_array


def twofold(value):
    high = float(value)
    low = float(value - Decimal.from_float(high))
    return Decimal.from_float(high) + Decimal.from_float(low)


def main():
    modest()
    folder = ROOT / 'results/basis-representation-diagnosis'
    folder.mkdir(parents=True, exist_ok=False)
    certified = verify_packet(ROOT / 'results/reference-certified')
    evaluator = StablePhaseSources()
    inputs = [ROOT / 'results/reference-certified/status.json', *evaluator.inputs]
    checks, records, primitives = [], {}, {}
    with localcontext() as context:
        context.prec = 80
        bases = [EpochBundle(ENDPOINTS[endpoint]).basis for endpoint in ENDPOINTS]
        assert all(np.array_equal(bases[0].norms, basis.norms) and bases[0].mean == basis.mean for basis in bases)
        norm0, norm1 = decimal_array(bases[0].norms[:2])
        mean = Decimal.from_float(float(bases[0].mean))
        temperature0, temperature1 = decimal_array(evaluator.data['temperature'][:2])
        assert temperature1 == norm1
        assert float(mean * norm0) == float(temperature0)
        coefficient_energy = temperature1 / norm1 - 1
        coefficient_number = temperature0 / norm0 - temperature1 * mean / norm1
        exact_temperature0 = mean * norm0
        constants = dict(norm0=str(norm0), norm1=str(norm1), mean=str(mean),
            stored_temperature0=str(temperature0), exact_product_temperature0=str(exact_temperature0),
            temperature0_low_part=str(exact_temperature0 - temperature0),
            coefficient_energy=str(coefficient_energy), coefficient_number=str(coefficient_number))
        for endpoint in ENDPOINTS:
            sums = {}
            for order in [4, 5, 6]:
                path = ROOT / 'results/sources-refined' / f'{endpoint}-order{order}-moments.json'
                packet = json.loads(path.read_text())
                sums[order] = np.array([Decimal(value) for value in packet['primitive_values']], dtype=object).reshape(packet['primitive_shape']).sum(axis=(0, 1))
                inputs.append(path)
            for step, high, low in [('54', 5, 4), ('65', 6, 5), ('64', 6, 4)]:
                primitives[(endpoint, step)] = sums[high] - sums[low]
        for window in ['earlier', 'terminal']:
            for route in ['local', 'cubic']:
                for step in ['54', '65', '64']:
                    maxima = {key: 0. for key in ['factorization_error', 'moment_reconstruction_error', 'twofold_probe', 'number_energy_condition']}
                    worst = {key: dict(relative=-1.) for key in ['basis_defect', 'rounded_defect', 'rounding_only']}
                    for phase in np.linspace(0, 1, 4097):
                        weights = cardinal_weights(phase, route)
                        factors = [weights[4], 0.] if window == 'earlier' else [weights[0], weights[4]]
                        photon, number, gas = sum(Decimal.from_float(float(factor)) * primitives[(endpoint, step)] for endpoint, factor in zip(ENDPOINTS, factors))
                        values, exact = evaluator.physical(phase, route, window, step)
                        rounded = decimal_array(values[[0, 1, 2, 97]])
                        for column in range(4):
                            scale = max(abs(photon[column]), Decimal('1e-300'))
                            exact_defect = temperature0 * exact[1, column] + temperature1 * exact[2, column] - exact[0, column]
                            factorized = coefficient_energy * photon[column] + coefficient_number * number[column]
                            rounded_defect = temperature0 * rounded[1, column] + temperature1 * rounded[2, column] - rounded[0, column]
                            first = number[column] / norm0
                            second = (photon[column] - mean * number[column]) / norm1
                            reconstruction = max(abs(first - exact[1, column]), abs(second - exact[2, column]), abs(photon[column] - exact[0, column]))
                            probe = twofold(exact_temperature0) * twofold(first) + twofold(norm1) * twofold(second) - twofold(photon[column])
                            metrics = dict(factorization_error=abs(exact_defect - factorized) / scale,
                                moment_reconstruction_error=reconstruction / scale,
                                twofold_probe=abs(probe) / scale, number_energy_condition=abs(number[column]) / scale)
                            for name, value in metrics.items():
                                maxima[name] = max(maxima[name], float(value))
                            for name, defect in [('basis_defect', exact_defect), ('rounded_defect', rounded_defect), ('rounding_only', rounded_defect - exact_defect)]:
                                ratio = float(abs(defect) / scale)
                                if ratio > worst[name]['relative']:
                                    worst[name] = dict(relative=ratio, phase=float(phase), column=column,
                                        photon=str(photon[column]), number=str(number[column]), defect=str(defect),
                                        predicted_basis_defect=str(factorized), basis_defect=str(exact_defect),
                                        rounded_defect=str(rounded_defect))
                    label = window + '-' + route + '-' + step
                    records[label] = dict(maxima=maxima, worst=worst)
                    test(checks, 'Independent basis-defect factorization:' + label, maxima['factorization_error'], 1e-50)
                    test(checks, 'Primitive-to-moment identity:' + label, maxima['moment_reconstruction_error'], 1e-50)
                    test(checks, 'Unadopted twofold representation probe:' + label, maxima['twofold_probe'], 1e-10)
                    for quantity, suffix in [('basis_defect', 'exact_moment'), ('rounded_defect', 'rounded_exact_moment')]:
                        expected = certified['phase_records'][window + '-' + route][step + '_' + suffix]
                        test(checks, 'Reproduce certified maximum:' + label + ':' + quantity,
                            abs(worst[quantity]['relative'] - expected) / max(expected, 1e-300), 1e-10)
                print(json.dumps(dict(window=window, route=route, checks=len(checks), failures=[row for row in checks if not row['passed']])), flush=True)
    finish(folder, dict(checks=checks, constants=constants, records=records, phases_per_route=4097,
        source_arrays_changed=False, basis_arrays_changed=False, probe_adopted=False,
        temperature_curve_changed=False, tolerance_changed=False, response_propagation_allowed=False,
        interpretation='Unrounded residual is exactly the frozen float basis-product mismatch; rounded residual also contains component casting. Twofold representation is a probe only.'),
        __file__, [ROOT / 'BASIS-REPRESENTATION-DERIVATION.md', *inputs])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], constants=constants, records=records)), flush=True)


if __name__ == '__main__':
    main()
