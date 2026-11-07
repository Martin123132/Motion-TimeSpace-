import argparse
from thermal_wave_common import *
from thermal_wave_system import ThermalWaveSystem


def main(arguments):
    modest()
    folder = ROOT / 'runs' / arguments.name
    assert not folder.exists()
    folder.mkdir(parents=True, exist_ok=False)
    system = ThermalWaveSystem(arguments.model, arguments.count, arguments.maximum, arguments.control)
    state, initial = system.initial()
    previous = state.copy()
    step = system.geometry.thermal.end / arguments.steps
    states, features, moments, constraints = [], [], [], []
    started = time.perf_counter()
    residuals = []
    for index in range(arguments.steps + 1):
        expansion = index * step
        if index:
            mass, operator, _ = system.matrices(expansion)
            if index == 1:
                alpha, history = 1 / step, state / step
            else:
                alpha, history = 1.5 / step, (2 * state - .5 * previous) / step
            factor = sparse_linalg.splu(alpha * mass - operator)
            right = mass @ history
            updated = factor.solve(right)
            residual = alpha * (mass @ updated) - operator @ updated - right
            residuals.append(float(np.linalg.norm(residual) / max(np.linalg.norm(right), 1e-100)))
            previous, state = state, updated
        if index % max(1, arguments.steps // 40) == 0 or index == arguments.steps:
            raw, scale = system.constraints(expansion, state)
            moments.append(expansion)
            states.append(state.copy())
            features.append(system.features(expansion, state))
            constraints.append(abs(raw) / scale)
        if index and index % max(1, arguments.steps // 10) == 0:
            np.savez_compressed(folder / 'checkpoint.npz', state=state, previous=previous, step=index, expansion=expansion)
            write_json(folder / 'progress.json', dict(state='running', step=index, steps=arguments.steps,
                                                     elapsed=time.perf_counter() - started))
            print(json.dumps(dict(step=index, elapsed=time.perf_counter() - started)), flush=True)
    constraints = np.array(constraints)
    checks = [dict(name='Full linear thermal/gravity evolution remains finite', passed=bool(np.isfinite(states).all())),
              dict(name='Hamiltonian and momentum constraints propagate without repair',
                   passed=float(np.max(constraints)) < .002, value=float(np.max(constraints))),
              dict(name='Coupled implicit equations solved', passed=max(residuals) < 1e-8, value=max(residuals))]
    np.savez_compressed(folder / 'evolution.npz', expansion=moments, states=states, features=features,
                        constraints=constraints, steps=arguments.steps, basis_count=arguments.count,
                        maximum=arguments.maximum, physical_heat=system.geometry.heat)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        model=arguments.model, control=arguments.control, basis_count=arguments.count, maximum=arguments.maximum,
                        steps=arguments.steps, initial=initial, initial_only_constraint_solve=True,
                        no_constraint_projection_during_evolution=True, background_thermal_stress_and_field_feedback=True,
                        collision_scope='Linearized physical Planck-bath kernel plus derived background density and boost sources; higher mixed nonequilibrium Jacobian requires separate control.',
                        elapsed=time.perf_counter() - started), __file__,
           [ROOT / 'thermal_wave_system.py', ROOT / 'background_geometry.py', ROOT / 'kernel_ladder.py',
            ROOT / 'stable_spectral_basis.py', *system.ladder.inputs, system.geometry.source,
            WAVES / 'initial_state.py', WAVES / 'coupled_system.py', system.geometry.parent.source])
    print(json.dumps(dict(checks=checks, elapsed=time.perf_counter() - started)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--model', choices=['heavy', 'cold'], default='heavy')
    parser.add_argument('--count', type=int, default=16)
    parser.add_argument('--steps', type=int, default=800)
    parser.add_argument('--maximum', type=int, default=8)
    parser.add_argument('--control', choices=['physical', 'matched-elastic', 'dust'], default='physical')
    main(parser.parse_args())
