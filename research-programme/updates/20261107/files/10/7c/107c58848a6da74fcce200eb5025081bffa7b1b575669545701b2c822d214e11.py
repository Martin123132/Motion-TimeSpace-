from remainder_common import *
from compare_source_vectors import dual_norm
from inspect_coupled_response import response, NonlocalEmission, infrared_ladder


def main():
    modest()
    folder = ROOT / 'results/remainder-resolution'
    folder.mkdir(parents=True, exist_ok=False)
    locations = [ROOT / 'runs' / f'midpoint-real-refinement-a4-r{order}' for order in [48, 96, 192]]
    packets = [json.loads((path / 'status.json').read_text()) for path in locations]
    assert all(packet['all_checks_passed'] and packet['nodes'] == 672 for packet in packets)
    values = [dict(np.load(path / 'source.npz')) for path in locations]
    spectra = Spectra(.5)
    mass = spectra.basis.mass
    checks, rows, saved_responses, dependencies = [], [], {}, []
    for first, second in [(0, 1), (1, 2)]:
        metrics = {}
        for component in ['total', 'remainder', 'difference', 'kinematic_remainder', 'virtual', 'state']:
            norm = dual_norm(values[second][component][1:-1], mass)
            change = dual_norm(values[first][component][1:-1] - values[second][component][1:-1], mass)
            metrics[component] = dict(norm=norm.tolist(), absolute_change=change.tolist(),
                                     relative_change=(change / np.maximum(norm, 1e-300)).tolist())
        relative = max(metrics['remainder']['relative_change'])
        label = f'{[48, 96, 192][first]}-to-{[48, 96, 192][second]}'
        checks.append(dict(name='Fixed-angular full96 finite remainder within1percent: ' + label,
            value=relative, passed=relative < .01))
        rows.append(dict(comparison=label, components=metrics))
    reference_path = PARENT / 'runs/midpoint-log48/source.npz'
    reference = dict(np.load(reference_path))
    replay = float(np.max(dual_norm(values[0]['raw'][1:-1] - reference['total'][1:-1], mass) /
        np.maximum(dual_norm(reference['total'][1:-1], mass), 1e-300)))
    checks.append(dict(name='Split population adds back to saved identical-order Stage92 source', value=replay, passed=replay < 1e-9))
    ladder = infrared_ladder.InfraredLadder(prior.inherited.BACKGROUND / 'banks/infrared96-q700')
    response_rows = []
    for model_index, model in enumerate(['heavy', 'cold']):
        background = thermal_wave.thermal.ThermalBackground(model)
        local = background.at(spectra.coordinate)
        theta, heat = local['thermal_parameter'], background.chi
        rate = local['coefficient'] / theta
        emission = NonlocalEmission(ladder.basis, background, 'nonlocal-leading', inherited.inherited.SOURCE / 'banks/s960-i256')
        stiffness = ladder.at(theta, 0)[:96, :96] - emission.at(theta, 'dcbr')
        for duration in [1e-3, 1e-2]:
            photons, gases = [], []
            for order, value in zip([48, 96, 192], values):
                selection = slice(2 * model_index, 2 * model_index + 2)
                source = value['remainder']
                photon, gas, metrics = response(ladder.basis, stiffness, rate, heat,
                    source[1:-1, selection], source[-1, selection], duration)
                photons.append(photon)
                gases.append(gas)
                key = f'{model}-r{order}-duration{duration}'
                saved_responses[key] = photon
                saved_responses[key + '-gas'] = gas
                checks.append(dict(name='Original coupled equations and energy/work budget: ' + key,
                    passed=metrics['photon_equation_relative'] < 1e-7 and metrics['gas_equation_absolute'] < 1e-8
                           and metrics['energy_work_balance_absolute'] < 1e-14, **metrics))
            for first, second in [(0, 1), (1, 2)]:
                delta = photons[first] - photons[second]
                change = np.sqrt(np.maximum(np.sum(delta * (mass @ delta), axis=0), 0.))
                norm = np.sqrt(np.maximum(np.sum(photons[second] * (mass @ photons[second]), axis=0), 0.))
                relative = change / np.maximum(norm, 1e-300)
                label = f'{model}-{duration}-r{[48, 96, 192][first]}-r{[48, 96, 192][second]}'
                checks.append(dict(name='Fixed-angular remainder spectral response within1percent: ' + label,
                                   value=float(relative.max()), passed=bool(relative.max() < .01)))
                response_rows.append(dict(model=model, duration=duration, comparison=label,
                    relative_change=relative.tolist(), norm=norm.tolist(),
                    gas_absolute_change=(gases[first] - gases[second]).tolist()))
        dependencies.extend([*emission.inputs, background.parent.source, background.native_constants])
    latest_source = rows[-1]['components']['remainder']['relative_change']
    latest_responses = [row for row in response_rows if row['comparison'].endswith('r96-r192')]
    resolved = max(latest_source) < .01 and all(max(row['relative_change']) < .01 for row in latest_responses)
    np.savez(folder / 'responses.npz', **saved_responses)
    finish(folder, dict(checks=checks, comparisons=rows, response_comparisons=response_rows,
        fixed_angular_radial_gate_closed=resolved, all_dimension_remainder_gate_closed=False,
        full_parent_feedback_applied=False, new_parent_history=False, new_empirical_fit=False,
        modes_removed=0, comparison_scope='Fixed-angular and fixed-population radial refinement; independent angular and outer quadrature still required.'),
        __file__, [*spectra.inputs, *ladder.inputs, *dependencies, reference_path,
                   *[path / filename for path in locations for filename in ['status.json', 'source.npz']]])
    print(json.dumps(dict(checks=len(checks), failures=[row for row in checks if not row['passed']],
        fixed_angular_radial_gate_closed=resolved, comparisons=rows, responses=response_rows)), flush=True)


if __name__ == '__main__':
    main()
