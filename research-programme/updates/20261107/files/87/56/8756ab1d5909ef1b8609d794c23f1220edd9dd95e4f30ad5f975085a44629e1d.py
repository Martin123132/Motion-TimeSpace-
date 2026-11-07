from panel_rule import *
from compare_source_vectors import dual_norm


def main():
    modest()
    folder = ROOT / 'results/panel-rule'
    folder.mkdir(parents=True, exist_ok=False)
    parent_seal = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    for name, expected in parent_seal['file_hashes'].items():
        assert digest(PARENT / name) == expected
    rule = PanelRule(.5)
    errors, positivity = [], []
    for lower, upper in [(1e-11, 2e-7), (1e-6, 60.), (.01, .0101), (.3, .8)]:
        nodes, weights = rule(12, lower, upper)
        positivity.append(bool(np.min(nodes) > lower and np.max(nodes) < upper and np.min(weights) > 0 and np.all(np.diff(nodes) > 0)))
        for power in [-1, 0, 1, 2, 4]:
            exact = math.log(upper / lower) if power == -1 else (upper**(power + 1) - lower**(power + 1)) / (power + 1)
            errors.append(float(abs(weights @ nodes**power / exact - 1)))
    spectra = Spectra(.5)
    model = SplitReal(spectra, 'control')
    origin = BRANCH / 'population-matched-source-20261008/runs/midpoint-real-refinement'
    source = json.loads((origin / 'status.json').read_text())
    rows, inputs = [], [origin / 'status.json']
    for index in [0, 25, 190, 671]:
        source_path = origin / 'nodes' / f'{index:05d}.json'
        context = json.loads(source_path.read_text())['identity']
        parameters = weak.source.context(source['temperature'] * context['frequency'], context['cosine'],
                                         np.array(context['velocity']), source['temperature'])
        values, timings, energy = [], [], []
        for order in [12, 18, 24]:
            started = time.monotonic()
            result = model.real(parameters, angular=4, radial=order, rule=rule)
            values.append(result['total'])
            timings.append(time.monotonic() - started)
            energy.append(result['event_energy_null'])
        scale = dual_norm(values[-1][1:-1], spectra.basis.mass)
        relative = [float(np.max(dual_norm(value[1:-1] - values[-1][1:-1], spectra.basis.mass) / scale)) for value in values[:-1]]
        rows.append(dict(node=index, relative_to_order24=relative, seconds=timings, energy_null=max(energy)))
        inputs.append(source_path)
        print(json.dumps(rows[-1]), flush=True)
    checks = [
        dict(name='Parent sealed payloads verified before use', passed=True, count=len(parent_seal['file_hashes'])),
        dict(name='Logarithmic Jacobian integral controls', value=max(errors), passed=max(errors) < 1e-10),
        dict(name='Ordered positive quadrature stays inside original endpoints', passed=all(positivity)),
        dict(name='Pilot order18-to24 control source within0.01percent', value=max(row['relative_to_order24'][1] for row in rows),
             passed=max(row['relative_to_order24'][1] for row in rows) < 1e-4),
        dict(name='Exact event energy exchange retained', value=max(row['energy_null'] for row in rows),
             passed=max(row['energy_null'] for row in rows) < 1e-10),
    ]
    finish(folder, dict(checks=checks, rows=rows, orders=[12, 18, 24], maximum_log_width=.5,
        convergence_scope='Four-node pilot only; full population and finite-remainder budget required.'), __file__, [*inputs, *spectra.inputs])
    print(json.dumps(dict(checks=checks)), flush=True)


if __name__ == '__main__':
    main()
