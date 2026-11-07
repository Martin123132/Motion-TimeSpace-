from control_common import *
from compare_source_vectors import dual_norm
from inspect_coupled_response import response, NonlocalEmission, infrared_ladder


def main():
    modest()
    folder = ROOT / 'results/radial-budget'
    folder.mkdir(parents=True, exist_ok=False)
    names = ['a4-p12-w0.5', 'a4-p18-w0.5', 'a4-p24-w0.5', 'a4-p18-w0.25']
    paths = [ROOT / 'runs' / name for name in names]
    packets = [json.loads((path / 'status.json').read_text()) for path in paths]
    assert all(packet['all_checks_passed'] and packet['nodes'] == 672 for packet in packets)
    sources = [dict(np.load(path / 'source.npz')) for path in paths]
    spectra = Spectra(.5)
    mass = spectra.basis.mass
    parent_paths = [PARENT / f'runs/midpoint-real-refinement-a4-r{order}/source.npz' for order in [96, 192]]
    old = [dict(np.load(path)) for path in parent_paths]
    addback_paths = [BRANCH / f'rectangular-matched-source-20261008/overlaps/midpoint-gould{order}/overlap.npz' for order in [24, 48]]
    addback = [dict(np.load(path))['joined_new_domain'] for path in addback_paths]
    deltas = dict(panel=sources[-1]['kinematic_remainder'] - sources[-2]['kinematic_remainder'],
        amplitude=old[1]['difference'] - old[0]['difference'], addback=addback[1] - addback[0])
    checks, rows = [], []
    for first, second in [(0, 1), (1, 2), (2, 3)]:
        change = dual_norm(sources[first]['remainder'][1:-1] - sources[second]['remainder'][1:-1], mass)
        norm = dual_norm(sources[second]['remainder'][1:-1], mass)
        relative = change / norm
        label = names[first] + ' to ' + names[second]
        checks.append(dict(name='Full96 finite remainder panel refinement within1percent: ' + label,
                           value=float(relative.max()), passed=bool(relative.max() < .01)))
        rows.append(dict(comparison=label, relative_change=relative.tolist(), remainder_norm=norm.tolist()))
    denominator = dual_norm(sources[-1]['remainder'][1:-1], mass)
    norms = {key: dual_norm(value[1:-1], mass) for key, value in deltas.items()}
    budget = sum(norms.values()) / denominator
    checks.append(dict(name='Observed independent radial refinement budget within1percent of full remainder',
                       value=float(budget.max()), passed=bool(budget.max() < .01)))
    legacy_change = dual_norm(old[-1]['remainder'][1:-1] - sources[-1]['remainder'][1:-1], mass) / denominator
    ladder = infrared_ladder.InfraredLadder(BRANCH / 'emitting-thermal-background-20261008/banks/infrared96-q700')
    response_rows, arrays, dependencies = [], {}, []
    for model_index, model in enumerate(['heavy', 'cold']):
        background = thermal_wave.thermal.ThermalBackground(model)
        local = background.at(spectra.coordinate)
        theta, rate, heat = local['thermal_parameter'], local['coefficient'] / local['thermal_parameter'], background.chi
        emission = NonlocalEmission(ladder.basis, background, 'nonlocal-leading', BRANCH / 'infrared-source-domain-20261008/banks/s960-i256')
        stiffness = ladder.at(theta, 0)[:96, :96] - emission.at(theta, 'dcbr')
        selection = slice(2 * model_index, 2 * model_index + 2)
        for duration in [1e-3, 1e-2]:
            terms = {'reference': sources[-1]['remainder'], **deltas}
            solved, gases = {}, {}
            for key, term in terms.items():
                photon, gas, metrics = response(ladder.basis, stiffness, rate, heat,
                    term[1:-1, selection], term[-1, selection], duration)
                solved[key], gases[key] = photon, gas
                label = f'{model}-{duration}-{key}'
                arrays[label] = photon
                arrays[label + '-gas'] = gas
                checks.append(dict(name='Original coupled equations and energy/work budget: ' + label,
                    passed=metrics['photon_equation_relative'] < 1e-7 and metrics['gas_equation_absolute'] < 1e-8
                           and metrics['energy_work_balance_absolute'] < 1e-14, **metrics))
            def norm(value):
                return np.sqrt(np.maximum(np.sum(value * (mass @ value), axis=0), 0.))
            scale = norm(solved['reference'])
            contributions = {key: norm(solved[key]) / scale for key in deltas}
            total = sum(contributions.values())
            checks.append(dict(name=f'Observed response refinement budget within1percent: {model}-{duration}',
                value=float(total.max()), passed=bool(total.max() < .01)))
            response_rows.append(dict(model=model, duration=duration, refinement_budget_relative=total.tolist(),
                components={key: value.tolist() for key, value in contributions.items()}, reference_norm=scale.tolist()))
        dependencies.extend([*emission.inputs, background.parent.source, background.native_constants])
    np.savez(folder / 'responses.npz', **arrays)
    accepted = all(row['passed'] for row in checks)
    finish(folder, dict(checks=checks, panel_comparisons=rows, source_budget_relative=budget.tolist(),
        source_budget_components={key: (value / denominator).tolist() for key, value in norms.items()},
        global192_to_panel_relative_change=legacy_change.tolist(), response_budgets=response_rows,
        fixed_population_radial_gate_closed=accepted, all_dimension_remainder_gate_closed=False,
        exact_rigorous_continuum_error_bound=False, virtual_and_state_refinement_proved_here=False,
        full_parent_feedback_applied=False, new_parent_history=False, preferred_diagnostic=str(paths[-1] / 'source.npz')),
        __file__, [*spectra.inputs, *ladder.inputs, *dependencies, *parent_paths, *addback_paths,
                   *[path / filename for path in paths for filename in ['status.json', 'source.npz']]])
    print(json.dumps(dict(checks=len(checks), failures=[row for row in checks if not row['passed']],
        source_budget=budget.tolist(), source_components={key:(value / denominator).tolist() for key,value in norms.items()},
        comparisons=rows, legacy_change=legacy_change.tolist(), responses=response_rows)), flush=True)


if __name__ == '__main__':
    main()
