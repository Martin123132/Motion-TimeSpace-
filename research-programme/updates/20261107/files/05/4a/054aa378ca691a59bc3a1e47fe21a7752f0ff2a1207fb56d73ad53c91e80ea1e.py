from angular232 import *


def axis_rule(order=8):
    cosines, weights = np.polynomial.legendre.leggauss(order)
    directions, measures = [], []
    for cosine, weight in zip(cosines, weights):
        for index in range(2 * order):
            angle = np.pi * (index + .5) / order
            directions.append([math.sqrt(1 - cosine**2) * math.cos(angle), math.sqrt(1 - cosine**2) * math.sin(angle), cosine])
            measures.append(weight / (4 * order))
    return np.array(directions), np.array(measures)


def independent_average(parameters, degree):
    axes, weights = axis_rule()
    incoming, outgoing, electron = lab_born(parameters)
    incoming_direction = incoming[1:] / np.linalg.norm(incoming[1:])
    outgoing_direction = outgoing[1:] / np.linalg.norm(outgoing[1:])
    left = special.eval_legendre(degree, axes @ outgoing_direction)[:, None] * inherited.functions(outgoing[0] / parameters['temperature'])
    left -= special.eval_legendre(degree, axes @ incoming_direction)[:, None] * inherited.functions(incoming[0] / parameters['temperature'])
    gas = np.full(len(axes), electron[0] / parameters['temperature']) if degree == 0 else (axes @ electron[1:] / parameters['temperature'] if degree == 1 else np.zeros(len(axes)))
    tests = np.column_stack([left, gas])
    return (tests.T * weights) @ tests


def mp_derivative(four, tangent, temperature, degree):
    four = [mp.mpf(float(value)) for value in four]
    tangent = [mp.mpf(float(value)) for value in tangent]
    temperature = mp.mpf(temperature)
    def features(amplitude):
        shifted = [value + amplitude * delta for value, delta in zip(four, tangent)]
        frequency = shifted[0] / temperature
        radial = [frequency, frequency**2 / (1 + frequency), frequency**3 / (1 + frequency)**2]
        norm = mp.sqrt(sum(value**2 for value in shifted[1:]))
        direction = [value / norm for value in shifted[1:]]
        if degree == 0:
            angular = [mp.mpf(1)]
        elif degree == 1:
            angular = direction
        else:
            angular = [mp.sqrt(mp.mpf(3) / 2) * (direction[first] * direction[second] - mp.mpf(first == second) / 3)
                       for first in range(3) for second in range(3)]
        return [value * entry for value in radial for entry in angular]
    count = len(features(mp.mpf(0)))
    return np.array([float(mp.diff(lambda amplitude: features(amplitude)[index], 0)) for index in range(count)]).reshape(3, -1)


def main():
    modest()
    config = protocol()
    inputs = read(ROOT / 'inputs.json')
    checks, diagnostics = [], []
    mp.mp.dps = 80
    for probe in config['probes']:
        parameters = inherited.source.context(probe['temperature'], probe['lab_cosine'], probe['velocity'], probe['temperature'])
        for degree in config['degrees']:
            lift = AngularWeak(degree)
            audit, product = lift.born_data(parameters)
            direct = independent_average(parameters, degree)
            label = f'{probe["label"]}:l{degree}'
            check(checks, label + ': independent rotation average', relative(product, direct), 1e-10)
            incoming, outgoing, electron = lab_born(parameters)
            tangent = outgoing[0] * np.array([.17, -.21, .13, .37])
            expected = mp_derivative(outgoing, tangent, parameters['temperature'], degree)
            check(checks, label + ': independent80-digit angular derivative', relative(photon_tangent(outgoing, tangent, parameters['temperature'], degree), expected), 1e-10)
            state = lift.state_correction(parameters)
            if degree <= 1:
                combined = lift.born_features(parameters)[0] + lift.born_features(parameters)[-1]
                check(checks, label + ': independent gas-photon common mode at Born level', np.linalg.norm(combined), 1e-12)
                check(checks, label + ': displaced gas-photon common mode', np.linalg.norm(state['shifted_features'][0] + state['shifted_features'][-1]), 1e-12)
            for sign in (1., -1.):
                direction = np.array([.3, -.4, math.sqrt(.75)])
                soft = sign * parameters['temperature'] * np.array([1e-5, .01, .1])
                density, products, audit = lift.event_products(parameters, soft, direction)
                check(checks, label + ':' + str(sign) + ': real event energy conservation', lift.maximum_energy_residual, 1e-12)
                check(checks, label + ':' + str(sign) + ': real event momentum conservation', lift.maximum_momentum_residual, 1e-12)
                if degree <= 1:
                    null = np.array([1., 0., 0., 1.])
                    check(checks, label + ':' + str(sign) + ': projected joint common mode', np.max(abs(products @ null)) / np.max(abs(products)), 1e-10)
            if degree == 0:
                inherited_audit, inherited_product = inherited.born_data(parameters)
                check(checks, label + ': exact old monopole Born block', relative(product, inherited_product), 1e-10)
                old_state = inherited.state_correction(parameters)
                check(checks, label + ': old monopole state response', relative(state['total'], old_state['total']), 1e-7)
            if degree == 1:
                check(checks, label + ': radiation-alone momentum transfer nonzero', int(product[0, 0] <= 0), 0)
                scalar_product = inherited.born_data(parameters)[1]
                check(checks, label + ': copying isotropic block detected', int(relative(product, scalar_product) < .01), 0)
            diagnostics.append(dict(probe=probe['label'], degree=degree, born_norm=float(np.linalg.norm(product)),
                state_norm=float(np.linalg.norm(state['total'])), direction_derivative_norm=float(np.linalg.norm(expected))))
    add_modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    report = dict(stage=232, state='complete', qualified=all(row['passed'] for row in checks), finished_at=now(),
        checks=checks, failed=[row for row in checks if not row['passed']], diagnostics=diagnostics)
    assert not (ROOT / 'results/preflight.json').exists()
    write(ROOT / 'results/preflight-inputs.json', inputs)
    write(ROOT / 'results/preflight.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'])), flush=True)


if __name__ == '__main__':
    main()
