from azimuth_common import *
from compare_source_vectors import dual_norm
from inspect_coupled_response import response, NonlocalEmission, infrared_ladder


def main():
    modest()
    folder = ROOT / 'results/azimuth-budget'
    folder.mkdir(parents=True, exist_ok=False)
    fine_path = ROOT / 'results/combined-source/source.npz'
    coarse_path = PARENT / 'results/combined-source/source.npz'
    incoming_path = PARENT / 'results/direction-budget/responses.npz'
    fine, coarse, incoming = [dict(np.load(path)) for path in [fine_path, coarse_path, incoming_path]]
    spectra = Spectra(.5)
    mass = spectra.basis.mass
    deltas = {'azimuth-' + key:fine[key] - coarse[key] for key in ['kinematic_remainder', 'difference', 'virtual', 'state']}
    deltas.update({key.removeprefix('delta-'):value for key,value in incoming.items() if key.startswith('delta-')})
    denominator = dual_norm(fine['remainder'][1:-1], mass)
    components = {key:dual_norm(value[1:-1], mass) / denominator for key,value in deltas.items()}
    budget = sum(components.values())
    azimuth_budget = sum(value for key,value in components.items() if key.startswith('azimuth-'))
    coherent = dual_norm(fine['remainder'][1:-1] - coarse['remainder'][1:-1], mass) / denominator
    checks = [
        dict(name='Observed electron-azimuth component-sum budget within1percent', value=float(azimuth_budget.max()), passed=bool(azimuth_budget.max() < .01)),
        dict(name='Observed combined azimuth/inherited-hard/incoming source budget within1percent', value=float(budget.max()), passed=bool(budget.max() < .01)),
    ]
    arrays = {**{'delta-' + key:value for key,value in deltas.items()}, 'remainder':fine['remainder']}
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
            solved, gases = {}, {}
            for label, value in {'fine':fine['remainder'], **deltas}.items():
                photon, gas, metrics = response(ladder.basis, stiffness, rate, heat, value[1:-1, selection], value[-1, selection], duration)
                key = f'{model}-{duration}-{label}'
                arrays[key], arrays[key + '-gas'] = photon, gas
                solved[label], gases[label] = photon, gas
                checks.append(dict(name='Original coupled equations and energy/work budget: ' + key,
                    passed=bool(metrics['photon_equation_relative'] < 1e-7 and metrics['gas_equation_absolute'] < 1e-8 and metrics['energy_work_balance_absolute'] < 1e-14), **metrics))
            def norm(value):
                return np.sqrt(np.maximum(np.sum(value * (mass @ value), axis=0), 0.))
            photon_norm, gas_norm = norm(solved['fine']), abs(gases['fine'])
            assert np.min(photon_norm) > 0 and np.min(gas_norm) > 0
            photon_components = {key:norm(solved[key]) / photon_norm for key in deltas}
            gas_components = {key:abs(gases[key]) / gas_norm for key in deltas}
            photon_budget, gas_budget = sum(photon_components.values()), sum(gas_components.values())
            for label,value in [('spectral',photon_budget),('gas',gas_budget)]:
                checks.append(dict(name=f'Observed combined {label} budget within1percent: {model}-{duration}',
                    value=float(value.max()), passed=bool(value.max() < .01)))
            response_rows.append(dict(model=model, duration=duration, photon_budget=photon_budget.tolist(), gas_budget=gas_budget.tolist(),
                photon_components={key:value.tolist() for key,value in photon_components.items()},
                gas_components={key:value.tolist() for key,value in gas_components.items()}))
        dependencies.extend([*emission.inputs, background.parent.source, background.native_constants])
    np.savez(folder / 'responses.npz', **arrays)
    finish(folder, dict(checks=checks, source_budget=budget.tolist(), azimuth_budget=azimuth_budget.tolist(),
        coherent_azimuth_change=coherent.tolist(), source_components={key:value.tolist() for key,value in components.items()},
        response_rows=response_rows, combined_observed_budget_passed=all(row['passed'] for row in checks),
        incoming_evidence_hard_order=3, inherited_electron_azimuth=4, current_electron_azimuth=8,
        expensive_mixed_angle_frequency_difference_tested=False, mixed_electron_frequency_angle_difference_tested=False,
        rigorous_continuum_error_bound=False, all_dimension_remainder_gate_closed=False,
        new_parent_history=False, full_parent_feedback_applied=False), __file__,
        [fine_path, coarse_path, incoming_path, *spectra.inputs, *ladder.inputs, *dependencies])
    print(json.dumps(dict(source_budget=budget.tolist(), azimuth_budget=azimuth_budget.tolist(), coherent_azimuth_change=coherent.tolist(),
        response_summary=[dict(model=row['model'],duration=row['duration'],photon=max(row['photon_budget']),gas=max(row['gas_budget'])) for row in response_rows],
        failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
