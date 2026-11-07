from aligned_common import *
from compare_source_vectors import dual_norm
from inspect_coupled_response import response, NonlocalEmission, infrared_ladder


def main():
    modest()
    folder = ROOT / 'results/incoming-budget'
    folder.mkdir(parents=True, exist_ok=False)
    locations = [ROOT / 'runs' / f'compact{order}-h3-g2-2-4' for order in [128, 160]]
    sources = [dict(np.load(location / 'source.npz')) for location in locations]
    assert all(json.loads((location / 'status.json').read_text())['all_checks_passed'] for location in locations)
    old_paths = [PARENT / 'runs' / f's{order}-h3-g2-2-4/source.npz' for order in [3, 4]]
    old = [dict(np.load(path)) for path in old_paths]
    fine = sources[1]
    spectra = Spectra(.5)
    mass = spectra.basis.mass
    deltas = {'control':fine['kinematic_remainder'] - sources[0]['kinematic_remainder']}
    deltas.update({key:old[1][key] - old[0][key] for key in ['difference', 'virtual', 'state']})
    denominator = dual_norm(fine['remainder'][1:-1], mass)
    components = {key:dual_norm(value[1:-1], mass) / denominator for key, value in deltas.items()}
    budget = sum(components.values())
    checks = [dict(name='Observed full96 incoming component-sum budget within1percent',
        value=float(budget.max()), passed=bool(budget.max() < .01))]
    changed = dual_norm(fine['remainder'][1:-1] - old[1]['remainder'][1:-1], mass) / denominator
    arrays = {'remainder':fine['remainder'], **{'delta-' + key:value for key, value in deltas.items()}}
    ladder = infrared_ladder.InfraredLadder(BRANCH / 'emitting-thermal-background-20261008/banks/infrared96-q700')
    dependencies, response_rows = [], []
    for model_index, model in enumerate(['heavy', 'cold']):
        background = thermal_wave.thermal.ThermalBackground(model)
        local = background.at(spectra.coordinate)
        theta, rate, heat = local['thermal_parameter'], local['coefficient'] / local['thermal_parameter'], background.chi
        emission = NonlocalEmission(ladder.basis, background, 'nonlocal-leading', BRANCH / 'infrared-source-domain-20261008/banks/s960-i256')
        stiffness = ladder.at(theta, 0)[:96, :96] - emission.at(theta, 'dcbr')
        selection = slice(2 * model_index, 2 * model_index + 2)
        for duration in [1e-3, 1e-2]:
            solved, gas_solved = {}, {}
            for label, source in {'fine':fine['remainder'], **deltas}.items():
                photon, gas, metrics = response(ladder.basis, stiffness, rate, heat,
                    source[1:-1, selection], source[-1, selection], duration)
                key = f'{model}-{duration}-{label}'
                arrays[key], arrays[key + '-gas'] = photon, gas
                solved[label], gas_solved[label] = photon, gas
                checks.append(dict(name='Original coupled equations and energy/work budget: ' + key,
                    passed=bool(metrics['photon_equation_relative'] < 1e-7 and metrics['gas_equation_absolute'] < 1e-8 and metrics['energy_work_balance_absolute'] < 1e-14), **metrics))
            def norm(value):
                return np.sqrt(np.maximum(np.sum(value * (mass @ value), axis=0), 0.))
            photon_norm, gas_norm = norm(solved['fine']), abs(gas_solved['fine'])
            assert np.min(photon_norm) > 0 and np.min(gas_norm) > 0
            photon_pieces = {key:norm(solved[key]) / photon_norm for key in deltas}
            gas_pieces = {key:abs(gas_solved[key]) / gas_norm for key in deltas}
            photon_budget, gas_budget = sum(photon_pieces.values()), sum(gas_pieces.values())
            for label, value in [('spectral', photon_budget), ('gas', gas_budget)]:
                checks.append(dict(name=f'Observed {label} incoming component-sum budget within1percent: {model}-{duration}',
                    value=float(value.max()), passed=bool(value.max() < .01)))
            response_rows.append(dict(model=model, duration=duration, photon_budget=photon_budget.tolist(), gas_budget=gas_budget.tolist(),
                photon_components={key:value.tolist() for key,value in photon_pieces.items()},
                gas_components={key:value.tolist() for key,value in gas_pieces.items()}))
        dependencies.extend([*emission.inputs, background.parent.source, background.native_constants])
    np.savez(folder / 'responses.npz', **arrays)
    finish(folder, dict(checks=checks, remainder_norm=denominator.tolist(), source_budget=budget.tolist(),
        source_components={key:value.tolist() for key,value in components.items()}, response_rows=response_rows,
        change_from_unresolved_seed4=changed.tolist(), incoming_frequency_observed_budget_passed=all(row['passed'] for row in checks),
        all_dimension_remainder_gate_closed=False, rigorous_continuum_error_bound=False,
        source_smallness_used_to_waive_gate=False, new_parent_history=False, full_parent_feedback_applied=False),
        __file__, [*old_paths, *spectra.inputs, *ladder.inputs, *dependencies,
            *[location / filename for location in locations for filename in ['status.json', 'source.npz']]])
    print(json.dumps(dict(source_budget=budget.tolist(), responses=response_rows,
        failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
