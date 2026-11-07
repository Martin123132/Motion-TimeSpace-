from control_common import *
from compare_source_vectors import dual_norm
from inspect_coupled_response import response, NonlocalEmission, infrared_ladder


def main():
    modest()
    folder = ROOT / 'results/angular-budget'
    folder.mkdir(parents=True, exist_ok=False)
    paths = [ROOT / 'runs/a4-p18-w0.5', ROOT / 'angular/a4-p18-w0.5', ROOT / 'angular/a6-p18-w0.5']
    packets = [json.loads((path / 'status.json').read_text()) for path in paths]
    assert all(packet['all_checks_passed'] for packet in packets)
    sources = [dict(np.load(path / 'source.npz')) for path in paths]
    spectra = Spectra(.5)
    mass = spectra.basis.mass
    checks, rows, dependencies, arrays = [], [], [], {}
    for first, second, label in [(0, 1, 'Independent amplitude radial-method replay'), (1, 2, 'Full soft-angular4-to6 refinement')]:
        components = {}
        for key in ['remainder', 'difference', 'kinematic_remainder']:
            norm = dual_norm(sources[second][key][1:-1], mass)
            change = dual_norm(sources[first][key][1:-1] - sources[second][key][1:-1], mass)
            components[key] = dict(norm=norm.tolist(), absolute_change=change.tolist(), relative_change=(change / norm).tolist())
        relative = max(components['remainder']['relative_change'])
        checks.append(dict(name=label + ' within1percent of full96 remainder', value=relative, passed=relative < .01))
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
            for index, source in enumerate(sources):
                value = source['remainder']
                photon, gas, metrics = response(ladder.basis, stiffness, rate, heat,
                    value[1:-1, selection], value[-1, selection], duration)
                solved.append(photon)
                label = f'{model}-{duration}-source{index}'
                arrays[label], arrays[label + '-gas'] = photon, gas
                checks.append(dict(name='Original coupled equations and energy/work budget: ' + label,
                    passed=metrics['photon_equation_relative'] < 1e-7 and metrics['gas_equation_absolute'] < 1e-8
                           and metrics['energy_work_balance_absolute'] < 1e-14, **metrics))
            def norm(value):
                return np.sqrt(np.maximum(np.sum(value * (mass @ value), axis=0), 0.))
            for first, second, label in [(0, 1, 'radial-method'), (1, 2, 'angular4-to6')]:
                relative = norm(solved[first] - solved[second]) / norm(solved[second])
                checks.append(dict(name=f'Full96 spectral response refinement within1percent: {model}-{duration}-{label}',
                    value=float(relative.max()), passed=bool(relative.max() < .01)))
                response_rows.append(dict(model=model, duration=duration, comparison=label, relative_change=relative.tolist()))
        dependencies.extend([*emission.inputs, background.parent.source, background.native_constants])
    np.savez(folder / 'responses.npz', **arrays)
    finish(folder, dict(checks=checks, comparisons=rows, response_comparisons=response_rows,
        soft_angular_gate_closed=all(row['passed'] for row in checks), all_dimension_remainder_gate_closed=False,
        outer_population_refinement_complete=False, full_parent_feedback_applied=False,
        new_parent_history=False, preferred_diagnostic=str(paths[-1] / 'source.npz')),
        __file__, [*spectra.inputs, *ladder.inputs, *dependencies,
                   *[path / name for path in paths for name in ['status.json', 'source.npz']]])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
        comparisons=rows, responses=response_rows)), flush=True)


if __name__ == '__main__':
    main()
