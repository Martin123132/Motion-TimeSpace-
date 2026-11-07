from split_real import *
from log_rectangular import LogRectangular


def main():
    modest()
    folder = ROOT / 'results/split-real'
    folder.mkdir(parents=True, exist_ok=True)
    assert not (folder / 'COMPLETE').exists()
    origin = BRANCH / 'population-matched-source-20261008/runs/midpoint-population-v2'
    status = json.loads((origin / 'status.json').read_text())
    spectra = Spectra(.5)
    models = {mode: SplitReal(spectra, mode) for mode in ['full', 'control', 'difference']}
    original = LogRectangular(spectra)
    rows, inputs = [], [origin / 'status.json']
    started = time.monotonic()
    for index in [0, 25, 190, 671]:
        source_path = origin / 'nodes' / f'{index:05d}.json'
        saved = json.loads(source_path.read_text())
        context = saved['identity']
        parameters = weak.source.context(status['temperature'] * context['frequency'], context['cosine'],
                                         np.array(context['velocity']), status['temperature'])
        values, elapsed = {}, {}
        for mode, model in models.items():
            start = time.monotonic()
            values[mode] = model.real(parameters, angular=3, radial=24)
            elapsed[mode] = time.monotonic() - start
        with original.real_context():
            reference = weak.real_subtracted(parameters, angular=3, radial=24, lower_fraction=1e-6)
        scale = np.linalg.norm(values['full']['total'])
        addition = {key: float(np.linalg.norm(values['full'][key] - values['control'][key] - values['difference'][key]) / scale)
                    for key in ['total', 'spontaneous', 'thermal', 'logarithm']}
        pole_errors = []
        for direction, measure in weak.source.angular_nodes(3):
            fraction = np.array([1e-7])
            soft = fraction * parameters['energy']
            energy = parameters['energy']
            denominator = 1 + energy * (1 - parameters['cosine']) - soft * (1 - parameters['hard_direction'] @ direction)
            hard = (energy - soft - energy * soft * (1 - direction[2])) / denominator
            tree = 2 * (1 + parameters['cosine']**2 + energy**2 * (1 - parameters['cosine'])**2 / (1 + energy * (1 - parameters['cosine'])))
            intensity = fast_intensity(fraction, models['control'].gram(parameters['hard_direction'], direction))
            density = weak.source.ALPHA / (4 * np.pi**2) * hard * soft * intensity
            density /= energy * denominator * (parameters['hard'] / energy)**2 * tree
            hard_frequency = hard * parameters['hard_doppler'] / parameters['temperature']
            density *= (1 + 1 / np.expm1(hard_frequency)) / parameters['hard_bose']
            pole = models['control'].poles(parameters, direction)
            if pole > 1e-30:
                pole_errors.append(float(abs(density[0] * soft[0] / pole - 1)))
        rows.append(dict(index=index, addition_relative=addition,
            original_relative=float(np.linalg.norm(values['full']['total'] - reference['total']) / scale),
            control_soft_pole_relative=max(pole_errors), elapsed_seconds=elapsed,
            event_energy_null=max(value['event_energy_null'] for value in values.values())))
        inputs.append(source_path)
        print(json.dumps(rows[-1]), flush=True)
    checks = [
        dict(name='Full implementation reproduces original logarithmic real source',
             value=max(row['original_relative'] for row in rows), passed=max(row['original_relative'] for row in rows) < 1e-10),
        dict(name='Every finite and counterterm piece adds back to the full source',
             value=max(max(row['addition_relative'].values()) for row in rows),
             passed=max(max(row['addition_relative'].values()) for row in rows) < 1e-10),
        dict(name='Control soft-pole coefficient agrees with event density limit',
             value=max(row['control_soft_pole_relative'] for row in rows),
             passed=max(row['control_soft_pole_relative'] for row in rows) < 1e-4),
        dict(name='Both split sources retain exact photon/gas energy exchange',
             value=max(row['event_energy_null'] for row in rows), passed=max(row['event_energy_null'] for row in rows) < 1e-10),
    ]
    finish(folder, dict(checks=checks, rows=rows, elapsed_seconds=time.monotonic() - started,
        scope='Four actual midpoint population nodes; all 96 spectral tests and four physical profiles.'), __file__, inputs)
    print(json.dumps(dict(checks=checks)), flush=True)


if __name__ == '__main__':
    main()
