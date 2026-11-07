from log_rectangular import *


def main():
    modest()
    folder = ROOT / 'results/log-projection-controls'
    folder.mkdir(parents=True, exist_ok=False)
    spectra = Spectra(.5)
    model = LogRectangular(spectra)
    coefficients = np.zeros((7, 4))
    coefficients[2:6] = np.eye(4)
    coefficients[-1] = np.repeat(spectra.gas, 2)
    def functions(frequency, chemical=False):
        frequency = np.asarray(frequency)
        return np.concatenate([np.ones(frequency.shape + (1,)), spectra.functions(frequency)], axis=-1)
    def derivatives(frequency, chemical=False):
        return np.r_[0., spectra.derivatives(frequency)]
    weak.functions, weak.derivatives = functions, derivatives
    parent = PARENT / 'runs/midpoint-population-v2'
    packet = json.loads((parent / 'status.json').read_text())
    paths, rows = [], []
    for index in [0, 25, 190, 671]:
        path = parent / 'nodes' / ('%05d.json' % index)
        saved = json.loads(path.read_text())
        identity = saved['identity']
        parameters = weak.source.context(packet['temperature'] * identity['frequency'], identity['cosine'],
                                         np.array(identity['velocity']), packet['temperature'])
        original_quadrature = weak.quadrature
        weak.quadrature = logarithmic_rule
        try:
            symmetric = weak.matched(parameters, saved['virtual_scalar'], angular=2, radial=32, lower_fraction=1e-6, chemical=True)
        finally:
            weak.quadrature = original_quadrature
        rectangular = model.matched(parameters, saved['virtual_scalar'], angular=2, radial=32)
        errors = []
        for key in ['total', 'born', 'virtual']:
            reference = -symmetric[key] @ coefficients
            actual = -rectangular[key]
            projected = np.stack([spectra.basis.chemical @ actual[1:-1], actual[0], actual[-1]])
            scale = np.maximum(np.max(abs(reference[[0, 1, -1]]), axis=1), 1e-30)
            errors.append(float(np.max(abs(projected - reference[[0, 1, -1]]) / scale[:, None])))
        rows.append(dict(node=index, maximum_independent_readout_relative_error=max(errors)))
        paths.append(path)
    values, weights = logarithmic_rule(16, 1e-6, .1)
    logarithm_error = abs(float(weights @ (1 / values)) - math.log(1e5))
    linear_values, linear_weights = weak.quadrature(24, 1e-6, .1)
    linear_error = abs(float(linear_weights @ (1 / linear_values)) - math.log(1e5))
    checks = [
        dict(name='Independent symmetric number, energy and gas contractions reproduce logarithmic rectangular source', value=max(row['maximum_independent_readout_relative_error'] for row in rows), passed=all(row['maximum_independent_readout_relative_error'] < 1e-6 for row in rows)),
        dict(name='Logarithmic quadrature integrates the derived leading infrared logarithm', value=logarithm_error, passed=logarithm_error < 1e-12),
        dict(name='Old linear energy quadrature does not certify a logarithmic number integral', value=linear_error, passed=linear_error > .01),
    ]
    finish(folder, dict(checks=checks, rows=rows, leading_log_linear_error=linear_error,
        physical_source_precision_must_still_be_tested=True), __file__, [*spectra.inputs, parent / 'status.json', *paths])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows, linear_log_error=linear_error)), flush=True)


if __name__ == '__main__':
    main()
