from fast_source import *
from compare_source_vectors import dual_norm


def main():
    modest()
    folder = ROOT / 'results/fast-source'
    folder.mkdir(parents=True, exist_ok=False)
    spectra = Spectra(.5)
    model = FastSplit(spectra, 'difference')
    rule = PanelRule(.5)
    origin = BRANCH / 'population-matched-source-20261008/runs/midpoint-real-refinement'
    status = json.loads((origin / 'status.json').read_text())
    inputs, rows = [origin / 'status.json'], []
    for index in [0, 25, 190, 671]:
        source_path = origin / 'nodes' / f'{index:05d}.json'
        context = json.loads(source_path.read_text())['identity']
        parameters = weak.source.context(status['temperature'] * context['frequency'], context['cosine'],
            np.array(context['velocity']), status['temperature'])
        reference_path = PARENT / 'angular/a4-p18-w0.5/nodes' / f'{index:05d}.npz'
        reference = dict(np.load(reference_path))
        started = time.monotonic()
        value = model.real(parameters, angular=4, radial=18, rule=rule)
        relative = dual_norm(value['total'][1:-1] - reference['difference'][1:-1], spectra.basis.mass) / dual_norm(reference['difference'][1:-1], spectra.basis.mass)
        rows.append(dict(node=index, difference_relative=float(relative.max()), seconds=time.monotonic() - started,
                         energy_null=value['event_energy_null']))
        inputs.extend([source_path, reference_path])
        print(json.dumps(rows[-1]), flush=True)
    energy = .02
    hard = np.array([.8, 0., .6])
    soft_direction = np.array([0., math.sqrt(.75), -.5])
    angular = angular_basis(hard, soft_direction)
    fraction = np.array([.02, .2, .45])
    original = factorized_intensity(energy, energy * fraction, hard, soft_direction, angular)
    reverse = angular_basis(soft_direction, hard)
    swapped = factorized_intensity(energy, original[3], soft_direction, hard, reverse)
    bose = float(np.max(abs(swapped[0] / original[0] - 1)))
    checks = [
        dict(name='Actual full96 amplitude-difference source replay within1e-6 relative',
             value=max(row['difference_relative'] for row in rows), passed=max(row['difference_relative'] for row in rows) < 1e-6),
        dict(name='Actual source retains exact event photon/gas exchange',
             value=max(row['energy_null'] for row in rows), passed=max(row['energy_null'] for row in rows) < 1e-10),
        dict(name='Exact outgoing photon exchange retained', value=bose, passed=bose < 1e-10),
    ]
    finish(folder, dict(checks=checks, rows=rows, coefficient_fit=False, energy_truncation=False,
        source_modes_retained=96), __file__, [*inputs, *spectra.inputs])
    print(json.dumps(dict(checks=checks)), flush=True)


if __name__ == '__main__':
    main()
