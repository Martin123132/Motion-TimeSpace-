from rectangular_weak import *


class ControlSpectrum:
    def __init__(self, basis, thermal):
        self.basis = basis
        self.gas = [float(thermal), float(thermal)]
        self.thermal = thermal

    def functions(self, frequency):
        frequency = np.asarray(frequency)
        return np.column_stack([frequency, *([frequency * self.thermal] * 4)]) if frequency.ndim else np.r_[frequency, np.repeat(frequency * self.thermal, 4)]

    def derivatives(self, frequency):
        return np.r_[1., np.repeat(float(self.thermal), 4)]


def main():
    modest()
    folder = ROOT / 'results/input-controls'
    folder.mkdir(parents=True, exist_ok=False)
    spectra = Spectra(.5)
    model = Rectangular(spectra)
    frequency = np.geomspace(1.000003e-6, 59.999, 1379)
    exact = spectra.basis.evaluate(frequency)
    actual = model.tests.evaluate(frequency)[:, 1:]
    derivatives = spectra.basis.derivative(frequency)
    actual_derivatives = model.tests.derivative(frequency)[:, 1:]
    value_error = float(np.max(abs(actual - exact) / (1 + abs(exact))))
    derivative_error = float(np.max(abs(actual_derivatives - derivatives) / (1 + abs(derivatives))))
    temperature_error = float(np.max(abs(actual @ spectra.basis.temperature - frequency) / frequency))
    number_error = float(np.max(abs(actual @ spectra.basis.chemical - 1)))
    checks = [
        dict(name='Interpolated original96 test functions agree with direct recurrence', value=value_error, passed=value_error < 1e-5),
        dict(name='Same interpolant derivatives agree with original derivatives', value=derivative_error, passed=derivative_error < 1e-3),
        dict(name='Energy test reproduced analytically', value=temperature_error, passed=temperature_error < 1e-10),
        dict(name='Number test reproduced analytically', value=number_error, passed=number_error < 1e-13),
    ]
    parent = PARENT / 'runs/midpoint-population-v2'
    packet = json.loads((parent / 'status.json').read_text())
    rows = [parent / 'nodes' / ('%05d.json' % index) for index in [0, 25, 190, 671]]
    errors, exchange = [], []
    for path in rows:
        saved = json.loads(path.read_text())
        identity = saved['identity']
        parameters = weak.source.context(packet['temperature'] * identity['frequency'], identity['cosine'],
                                         np.array(identity['velocity']), packet['temperature'])
        weak.functions, weak.derivatives = spectra.functions, spectra.derivatives
        original = weak.matched(parameters, saved['virtual_scalar'], angular=2, radial=16, lower_fraction=1e-6)
        rectangular = model.matched(parameters, saved['virtual_scalar'], angular=2, radial=16)
        for key in ['total', 'born', 'virtual']:
            reference = -original[key] @ spectra.coefficients()
            tested = -rectangular[key]
            errors.append(float(np.max(abs(tested[[0, -1]] - reference[[0, -1]])) / max(np.max(abs(reference[[0, -1]])), 1e-30)))
        controls = []
        for thermal in [False, True]:
            controlled = Rectangular(ControlSpectrum(spectra.basis, thermal))
            tested = controlled.matched(parameters, saved['virtual_scalar'], angular=2, radial=16)
            controls.append(float(np.linalg.norm(tested['total'])))
        exchange.append(dict(index=identity['index'], zero_norm=controls[0], equilibrium_norm=controls[1],
                             physical_norm=float(np.linalg.norm(rectangular['total']))))
    checks.append(dict(name='Rectangular bilinear agrees with independent symmetric energy contraction', value=max(errors), passed=max(errors) < 1e-6))
    checks.append(dict(name='Exactly zero departure has exactly zero source', passed=all(row['zero_norm'] == 0 for row in exchange)))
    checks.append(dict(name='Common-temperature source null without output projection', value=max(row['equilibrium_norm'] / max(row['physical_norm'], 1e-30) for row in exchange),
                       passed=all(row['equilibrium_norm'] < 1e-6 * max(row['physical_norm'], 1e-30) for row in exchange)))
    finish(folder, dict(checks=checks, event_controls=exchange, test_count=96,
        numerical_source_projection_only=True), __file__, [*spectra.inputs, parent / 'status.json', *rows])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], checks_detail=checks)), flush=True)


if __name__ == '__main__':
    main()
