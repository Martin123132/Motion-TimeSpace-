import argparse
from thermal_wave_common import *
from thermal_wave_system import ThermalWaveSystem


def main(arguments):
    modest()
    folder = ROOT / 'paired' / arguments.name
    assert not folder.exists()
    folder.mkdir(parents=True, exist_ok=False)
    physical = ThermalWaveSystem(arguments.model, arguments.count, arguments.maximum, 'physical')
    elastic = ThermalWaveSystem(arguments.model, arguments.count, arguments.maximum, 'matched-elastic')
    state, initial = elastic.initial()
    physical_initial, _ = physical.initial()
    assert np.max(abs(physical_initial - state)) == 0
    difference = np.zeros_like(state)
    previous, previous_difference = state.copy(), difference.copy()
    step = physical.geometry.thermal.end / arguments.steps
    moments, states, differences, features, baselines, constraints = [], [], [], [], [], []
    residuals = []
    started = time.perf_counter()
    for index in range(arguments.steps + 1):
        expansion = index * step
        if index:
            mass, operator, _ = physical.matrices(expansion)
            elastic_mass, elastic_operator, _ = elastic.matrices(expansion)
            assert (mass - elastic_mass).nnz == 0
            delta_operator = operator - elastic_operator
            if index == 1:
                alpha, history, delta_history = 1 / step, state / step, difference / step
            else:
                alpha = 1.5 / step
                history = (2 * state - .5 * previous) / step
                delta_history = (2 * difference - .5 * previous_difference) / step
            elastic_factor = sparse_linalg.splu(alpha * mass - elastic_operator)
            physical_factor = sparse_linalg.splu(alpha * mass - operator)
            new_state = elastic_factor.solve(mass @ history)
            right = mass @ delta_history + delta_operator @ new_state
            new_difference = physical_factor.solve(right)
            residuals.append(float(np.linalg.norm((alpha * mass - operator) @ new_difference - right)
                                   / max(np.linalg.norm(right), 1e-100)))
            previous, state = state, new_state
            previous_difference, difference = difference, new_difference
        if index % max(1, arguments.steps // 40) == 0 or index == arguments.steps:
            moments.append(expansion)
            states.append(state.copy())
            differences.append(difference.copy())
            features.append(physical.features(expansion, difference))
            baselines.append(elastic.features(expansion, state))
            raw, scale = physical.constraints(expansion, state + difference)
            constraints.append(abs(raw) / scale)
        if index and index % max(1, arguments.steps // 10) == 0:
            np.savez_compressed(folder / 'checkpoint.npz', baseline=state, previous=previous,
                                difference=difference, previous_difference=previous_difference, step=index)
            write_json(folder / 'progress.json', dict(state='running', step=index, steps=arguments.steps,
                                                     elapsed=time.perf_counter() - started))
    checks = [dict(name='Paired difference evolved without subtracting large solutions', passed=True),
              dict(name='Finite paired response', passed=bool(np.isfinite(differences).all())),
              dict(name='Unprojected gravity constraints propagate', passed=float(np.max(constraints)) < .002,
                   value=float(np.max(constraints))),
              dict(name='Paired implicit equations solved at correction scale', passed=max(residuals) < 1e-8,
                   value=max(residuals))]
    np.savez_compressed(folder / 'evolution.npz', expansion=moments, baseline_states=states,
                        differences=differences, features=features, baselines=baselines, constraints=constraints,
                        steps=arguments.steps, basis_count=arguments.count, maximum=arguments.maximum)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        model=arguments.model, basis_count=arguments.count, maximum=arguments.maximum, steps=arguments.steps,
                        initial=initial, no_constraint_projection_during_evolution=True,
                        scope='Physical minus matched-elastic angular scattering; identical warm background and monopole heat. Conservative Planck-linearized kernel, not full mixed nonequilibrium Jacobian.',
                        elapsed=time.perf_counter() - started), __file__,
           [ROOT / 'thermal_wave_system.py', ROOT / 'background_geometry.py', ROOT / 'kernel_ladder.py',
            ROOT / 'stable_spectral_basis.py', *physical.ladder.inputs, physical.geometry.source,
            WAVES / 'initial_state.py', WAVES / 'coupled_system.py', physical.geometry.parent.source])
    print(json.dumps(dict(checks=checks, elapsed=time.perf_counter() - started)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--model', choices=['heavy', 'cold'], default='heavy')
    parser.add_argument('--count', type=int, default=16)
    parser.add_argument('--steps', type=int, default=3200)
    parser.add_argument('--maximum', type=int, default=8)
    main(parser.parse_args())
