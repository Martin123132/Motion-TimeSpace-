from rational239 import *
import sympy as symbolic


def algebra(checks):
    energy, angle01, angle12, angle02, fraction = symbolic.symbols('E a b c f')
    denominator = 1 + energy * angle01 - energy * angle12 * fraction
    hard_numerator = 1 - (1 + energy * angle02) * fraction
    hard = energy * hard_numerator / denominator
    soft = energy * fraction
    final_energy = 1 + energy - hard - soft
    spatial_squared = energy**2 + hard**2 + soft**2 - 2 * energy * hard * (1 - angle01)
    spatial_squared += -2 * energy * soft * (1 - angle02) + 2 * hard * soft * (1 - angle12)
    projection = 1 + energy * (angle01 - angle12 - angle02) * fraction + energy**2 * angle12 * angle02 * fraction**2
    constant = (1 + energy * angle02) * (1 + energy * angle01) - energy * angle12
    expressions = {'mass shell': final_energy**2 - spatial_squared - 1,
        'incident projection': 1 - hard * angle01 - soft * angle02 - projection / denominator,
        'hard projection': 1 + energy * angle01 - soft * angle12 - denominator,
        'soft projection': 1 + energy * angle02 - hard * angle12 - constant / denominator}
    epsilon = symbolic.symbols('epsilon0:3')
    common = fraction * projection * denominator * hard_numerator
    original_projection = [projection / denominator, denominator, constant / denominator]
    signed_energy = [energy, -hard, -soft]
    direct = [fraction * denominator**2 * hard_numerator / 2,
        fraction * projection * hard_numerator / 2, fraction * projection * denominator**2 * hard_numerator / (2 * constant)]
    recoil = [-fraction * denominator * hard_numerator * epsilon[0] / energy,
        fraction * projection * epsilon[1] / energy, projection * denominator * hard_numerator * epsilon[2] / (energy * constant)]
    for last in range(3):
        expressions[f'matrix coefficient{last}'] = direct[last] / common - 1 / (2 * original_projection[last])
        expressions[f'recoil coefficient{last}'] = recoil[last] / common + epsilon[last] / (denominator * signed_energy[last] * original_projection[last])
    for name, value in expressions.items():
        check(checks, 'symbolic:' + name, int(symbolic.factor(value) != 0), 0)
    check(checks, 'symbolic:common denominator degree', int(symbolic.degree(common, fraction) != 5), 0)
    check(checks, 'symbolic:common denominator has exactly one soft zero', int(symbolic.factor((common / fraction).subs(fraction, 0) - (1 + energy * angle01)) != 0), 0)


def run():
    modest()
    config = protocol()
    assert not (ROOT / 'results/points.json').exists()
    checks, records, coefficients = [], [], []
    algebra(checks)
    angular_nodes = list(angular.inherited.source.angular_nodes(config['point_angular_order']))
    for row in config['events']:
        raw_parameters, event_weight = source.physics.parameters_and_weight(row['theta'], row['node'])
        for ray in config['point_rays']:
            previous_values = {}
            for digits in (config['digits'], config['control_digits']):
                with mp.workdps(digits):
                    parameters = precise_context(raw_parameters)
                    owner = RationalDirection(parameters, angular_nodes[ray][0])
                    name = f'{row["label"]}:ray{ray}:digits{digits}'
                    check(checks, name + ':real polynomial coefficients', owner.imaginary_residual)
                    check(checks, name + ':derived soft residue', abs(owner.soft_residue() / owner.pole['full'] - 1))
                    coefficients.append(dict(anchor=row['label'], ray=ray, digits=digits,
                        numerator=[str(value) for value in owner.intensity_numerator],
                        denominator=[str(value) for value in owner.common_denominator],
                        final_denominator=[str(value) for value in owner.denominator_polynomial],
                        construction_seconds=owner.construction_seconds,
                        inherited_construction_seconds=owner.inherited_construction_seconds))
                    emission, absorption, temperature = integration.upper_limits(owner)
                    cases = [(f'x{frequency}:sign{sign}', sign * scalar(frequency) * temperature)
                        for frequency in config['point_frequencies'] + [config['independent_frequency']] for sign in (1, -1)]
                    cases.extend([('independent-emission-edge', mp.mpf('.9731') * emission),
                        ('independent-absorption-edge', -mp.mpf('.9173') * absorption)])
                    for label, signed in cases:
                        started = time.perf_counter()
                        reference, event = Direction.densities(owner, signed)
                        reference_seconds = time.perf_counter() - started
                        started = time.perf_counter()
                        candidate, candidate_event = owner.densities(signed)
                        accelerated_seconds = time.perf_counter() - started
                        key = name + ':' + label
                        comparison = {}
                        for component in ('full', 'control', 'difference'):
                            for subtracted in (False, True):
                                source_pole = owner.pole[component] / abs(signed) if subtracted else 0
                                expected, measured = reference[component] - source_pole, candidate[component] - source_pole
                                error = abs(measured - expected) / max(abs(expected), mp.mpf('1e-300'))
                                suffix = component + ('_minus_pole' if subtracted else '')
                                check(checks, key + ':' + suffix, error)
                                comparison[suffix] = str(measured)
                                if digits == config['control_digits']:
                                    before = mp.mpf(previous_values[label][suffix])
                                    check(checks, key + ':' + suffix + ':60to80', abs(measured - before) / max(abs(measured), mp.mpf('1e-300')))
                        if digits == config['digits']:
                            previous_values[label] = comparison
                        fraction = signed / owner.energy
                        rational_final = evaluate(owner.momentum_polynomial, fraction) / evaluate(owner.denominator_polynomial, fraction)
                        check(checks, key + ':rational final four-momentum', mp.norm(rational_final - event['final']) / mp.norm(event['final']))
                        check(checks, key + ':event unchanged', mp.norm(event['final'] - candidate_event['final']))
                        if label.startswith('independent') or str(config['independent_frequency']) in label:
                            direct = owner.amplitude(event)
                            recovered = owner.rational_amplitude(event)
                            error = mp.sqrt(mp.fsum(mp.norm(before - after)**2 for before, after in zip(direct, recovered))
                                / mp.fsum(mp.norm(value)**2 for value in direct))
                            check(checks, key + ':independent amplitude replay', error)
                            left = owner.spin.spinors(event['final']).transpose_conj() * owner.spin.gamma_matrices()[0]
                            spin_sum = owner.spin.gamma_matrices()[0] * (owner.spin.slash(event['final']) + mp.eye(4))
                            check(checks, key + ':independent final spin sum', mp.norm(left.transpose_conj() * left - spin_sum) / mp.norm(spin_sum))
                        records.append(dict(anchor=row['label'], ray=ray, digits=digits, case=label,
                            signed_soft=str(signed), values=comparison, reference_seconds=reference_seconds,
                            accelerated_seconds=accelerated_seconds, speedup=reference_seconds / max(accelerated_seconds, 1e-300)))
            print(json.dumps(dict(anchor=row['label'], ray=ray, checks=len(checks), failures=sum(not value['passed'] for value in checks))), flush=True)
    for digits in (config['digits'], config['control_digits']):
        group = [row for row in records if row['digits'] == digits]
        ratio = sum(row['reference_seconds'] for row in group) / sum(row['accelerated_seconds'] for row in group)
        check(checks, f'digits{digits}:equal-precision event speedup exceeds one', int(ratio <= config['minimum_event_speedup']), 0)
    failed = [value for value in checks if not value['passed']]
    write(ROOT / 'results/derived-coefficients.json', coefficients)
    result = dict(stage=239, state='complete', qualified=not failed, checks=checks, failed=failed, records=records,
        coefficient_fitting_used=False, saved_reference_points_used_to_construct_coefficients=False,
        maximum_accuracy_error=max(row['value'] for row in checks),
        mean_construction_seconds=float(np.mean([row['construction_seconds'] for row in coefficients])),
        event_speedup=sum(row['reference_seconds'] for row in records) / sum(row['accelerated_seconds'] for row in records),
        script_sha256=digest(__file__), finished_at=now())
    write(ROOT / 'results/points.json', result)
    print(json.dumps({name: value for name, value in result.items() if name not in ('checks', 'records', 'failed')})
        + '\n' + json.dumps(failed[:12]), flush=True)


if __name__ == '__main__':
    run()
