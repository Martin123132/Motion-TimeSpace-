from aligned_common import *
from compare_source_vectors import dual_norm


def main():
    modest()
    folder = ROOT / 'results/inner-extremes'
    folder.mkdir(parents=True, exist_ok=False)
    location = ROOT / 'runs/compact160-h3-g2-2-4'
    report = json.loads((location / 'status.json').read_text())
    assert report['all_checks_passed']
    theta = report['configuration']['temperature']
    source = dict(np.load(location / 'source.npz'))
    spectra = Spectra(.5)
    model = SplitReal(spectra, 'control')
    denominator = dual_norm(source['remainder'][1:-1], spectra.basis.mass)
    selections = [electron * 480 + frequency * 3 + hard
        for electron in [0, 7, 8, 15] for frequency in [0, 40, 80, 120, 159] for hard in [0, 2]]
    inputs, rows, checks = [], [], []
    changes = {key:np.zeros(4) for key in ['radial', 'angular']}
    maximum_null = 0.
    for index in selections:
        path = location / 'nodes' / f'{index // 500:03d}' / f'{index:05d}.npz'
        saved = dict(np.load(path))
        identity = json.loads(str(saved['identity']))
        parameters = weak.source.context(theta * identity['frequency'], identity['cosine'], np.array(identity['velocity']), theta)
        original_norm = dual_norm(saved['control'][1:-1], spectra.basis.mass)
        row = dict(index=index, frequency=identity['frequency'], velocity=identity['velocity'], cosine=identity['cosine'])
        arrays = {}
        for label, angular, radial, width in [('radial', 4, 24, .25), ('angular', 6, 18, .5)]:
            result = model.real(parameters, angular=angular, radial=radial, rule=PanelRule(width))
            difference = result['total'] - saved['control']
            change = dual_norm(difference[1:-1], spectra.basis.mass)
            row[label + '_pointwise_relative_change'] = (change / np.maximum(original_norm, 1e-300)).tolist()
            weighted = float(saved['weight']) * change / denominator
            row[label + '_sampled_contribution_over_remainder'] = weighted.tolist()
            changes[label] += weighted
            arrays[label] = result['total']
            maximum_null = max(maximum_null, result['event_energy_null'])
        np.savez(folder / f'probe-{index:05d}.npz', **arrays)
        rows.append(row)
        inputs.append(path)
    checks = [
        dict(name='Forty declared extreme/interior control probes finite', passed=bool(all(np.isfinite(np.asarray(list(row.values())[4:], dtype=float)).all() for row in rows))),
        dict(name='Refined radial/angular events preserve exact photon/gas exchange', value=maximum_null, passed=maximum_null < 1e-10),
    ]
    finish(folder, dict(checks=checks, rows=rows,
        sampled_contribution_sums={key:value.tolist() for key,value in changes.items()},
        scope='Forty declared control nodes only; sums omit untested nodes and are not global inner-error bounds.',
        full_population_inner_error_bound=False, new_virtual_loop_evaluations=0), __file__,
        [*inputs, *spectra.inputs, location / 'status.json', location / 'source.npz'])
    print(json.dumps(dict(checks=checks, sampled_contribution_sums={key:value.tolist() for key,value in changes.items()})), flush=True)


if __name__ == '__main__':
    main()
