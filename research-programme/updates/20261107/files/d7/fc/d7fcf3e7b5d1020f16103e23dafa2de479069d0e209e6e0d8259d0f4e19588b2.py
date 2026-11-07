from outer_common import *
from compare_source_vectors import dual_norm
from inspect_coupled_response import response, NonlocalEmission, infrared_ladder


def main():
    modest()
    folder = ROOT / 'results/incoming-refinement'
    folder.mkdir(parents=True, exist_ok=False)
    paths = [ROOT / 'runs' / f's{order}-h3-g2-2-4' for order in [2, 3, 4]]
    reports = [json.loads((path / 'status.json').read_text()) for path in paths]
    assert all(report['all_checks_passed'] for report in reports)
    sources = [dict(np.load(path / 'source.npz')) for path in paths]
    spectra = Spectra(.5)
    mass = spectra.basis.mass
    checks, rows, dependencies, arrays = [], [], [], {}
    for first, second in [(0, 1), (1, 2)]:
        components = {}
        for key in ['total', 'remainder', 'difference', 'kinematic_remainder', 'virtual', 'state']:
            norm = dual_norm(sources[second][key][1:-1], mass)
            change = dual_norm(sources[first][key][1:-1] - sources[second][key][1:-1], mass)
            components[key] = dict(norm=norm.tolist(), absolute_change=change.tolist(), relative_change=(change / np.maximum(norm, 1e-300)).tolist())
        label = f'seed{[2, 3, 4][first]}-to-{[2, 3, 4][second]}'
        relative = max(components['remainder']['relative_change'])
        checks.append(dict(name='Full96 remainder incoming-grid refinement within1percent: ' + label,
            value=relative, passed=relative < .01))
        rows.append(dict(comparison=label, components=components))
    ladder = infrared_ladder.InfraredLadder(BRANCH / 'emitting-thermal-background-20261008/banks/infrared96-q700')
    response_rows = []
    for model_index, model in enumerate(['heavy', 'cold']):
        background = thermal_wave.thermal.ThermalBackground(model)
        local = background.at(spectra.coordinate)
        theta, rate, heat = local['thermal_parameter'], local['coefficient'] / local['thermal_parameter'], background.chi
        emission = NonlocalEmission(ladder.basis, background, 'nonlocal-leading', BRANCH / 'infrared-source-domain-20261008/banks/s960-i256')
        stiffness = ladder.at(theta, 0)[:96, :96] - emission.at(theta, 'dcbr')
        selection = slice(2 * model_index, 2 * model_index + 2)
        for duration in [1e-3, 1e-2]:
            solved = []
            for order, source in zip([2, 3, 4], sources):
                value = source['remainder']
                photon, gas, metrics = response(ladder.basis, stiffness, rate, heat,
                    value[1:-1, selection], value[-1, selection], duration)
                solved.append(photon)
                label = f'{model}-{duration}-seed{order}'
                arrays[label], arrays[label + '-gas'] = photon, gas
                checks.append(dict(name='Original coupled equations and energy/work budget: ' + label,
                    passed=metrics['photon_equation_relative'] < 1e-7 and metrics['gas_equation_absolute'] < 1e-8 and metrics['energy_work_balance_absolute'] < 1e-14, **metrics))
            def norm(value):
                return np.sqrt(np.maximum(np.sum(value * (mass @ value), axis=0), 0.))
            for first, second in [(0, 1), (1, 2)]:
                relative = norm(solved[first] - solved[second]) / norm(solved[second])
                label = f'{model}-{duration}-seed{[2, 3, 4][first]}-seed{[2, 3, 4][second]}'
                checks.append(dict(name='Full96 spectral response incoming-grid refinement within1percent: ' + label,
                    value=float(relative.max()), passed=bool(relative.max() < .01)))
                response_rows.append(dict(model=model, duration=duration, comparison=label, relative_change=relative.tolist()))
        dependencies.extend([*emission.inputs, background.parent.source, background.native_constants])
    latest_source = max(rows[-1]['components']['remainder']['relative_change']) < .01
    latest_response = all(max(row['relative_change']) < .01 for row in response_rows if row['comparison'].endswith('seed3-seed4'))
    np.savez(folder / 'responses.npz', **arrays)
    finish(folder, dict(checks=checks, comparisons=rows, response_comparisons=response_rows,
        incoming_frequency_gate_closed=latest_source and latest_response,
        electron_velocity_grid_refined=False, hard_direction_grid_refined=False,
        all_dimension_remainder_gate_closed=False, new_parent_history=False,
        full_parent_feedback_applied=False, preferred_diagnostic=str(paths[-1] / 'source.npz')),
        __file__, [*spectra.inputs, *ladder.inputs, *dependencies,
                   *[path / name for path in paths for name in ['status.json', 'source.npz']]])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
        comparisons=rows, responses=response_rows)), flush=True)


if __name__ == '__main__':
    main()
