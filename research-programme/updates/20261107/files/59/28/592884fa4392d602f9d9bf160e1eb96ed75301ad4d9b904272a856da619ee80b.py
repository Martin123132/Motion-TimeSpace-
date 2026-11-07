import argparse
from mixed_common import *
from mixed_wave_system import MixedSystem


def main(arguments):
    modest()
    folder = ROOT / 'waves' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    system = MixedSystem(arguments.model, arguments.count, arguments.maximum, arguments.bank, arguments.stride)
    state, initial = system.initial()
    difference = np.zeros_like(state)
    previous, previous_difference = state.copy(), difference.copy()
    background = np.zeros(system.count + 1)
    previous_background = background.copy()
    step = system.geometry.thermal.end / arguments.steps
    heat = system.background(0.)['heat']
    moments, states, differences, features, baselines, constraints, corrections = [], [], [], [], [], [], []
    residuals, number_errors, exchange_errors = [], [], []
    started = time.perf_counter()
    for index in range(arguments.steps + 1):
        expansion = index * step
        if index:
            mass, baseline_operator, _ = system.matrices(expansion)
            delta = system.correction(expansion, arguments.include_residual)
            operator = baseline_operator + heat * delta
            if index == 1:
                alpha, history, delta_history, background_history = 1 / step, state / step, difference / step, background / step
            else:
                alpha = 1.5 / step
                history = (2 * state - .5 * previous) / step
                delta_history = (2 * difference - .5 * previous_difference) / step
                background_history = (2 * background - .5 * previous_background) / step
            baseline_factor = sparse_linalg.splu(alpha * mass - baseline_operator)
            physical_factor = sparse_linalg.splu(alpha * mass - operator)
            new_state = baseline_factor.solve(mass @ history)
            right = mass @ delta_history + delta @ new_state
            new_difference = physical_factor.solve(right)
            residuals.append(float(np.linalg.norm((alpha * mass - operator) @ new_difference - right)
                                   / max(np.linalg.norm(right), 1e-100)))
            previous, state = state, new_state
            previous_difference, difference = difference, new_difference
            background_mass, background_operator, source = system.background_correction_operator(expansion)
            new_background = linalg.solve(alpha * background_mass - background_operator,
                                          background_mass @ background_history + source)
            previous_background, background = background, new_background
        if index % max(1, arguments.steps // 40) == 0 or index == arguments.steps:
            moments.append(expansion)
            states.append(state.copy())
            differences.append(difference.copy())
            features.append(system.features(expansion, difference))
            baselines.append(system.features(expansion, state))
            raw, scale = system.constraints(expansion, state + heat * difference)
            constraints.append(abs(raw) / scale)
            corrections.append(background.copy())
            delta = system.correction(expansion, False).toarray()
            first, dipole = system.mode_slice(0), system.mode_slice(1)
            number_errors.append(float(np.linalg.norm(system.basis.chemical @ delta[first]) / max(np.linalg.norm(delta[first]), 1e-100)))
            for section, gas in [(first, 10), (dipole, 9)]:
                photon = system.basis.energy @ system.mass_inverse @ delta[section]
                exchange_errors.append(float(np.linalg.norm(photon + delta[gas]) / max(np.linalg.norm(photon), 1e-100)))
        if index and index % max(1, arguments.steps // 10) == 0:
            np.savez_compressed(folder / 'checkpoint.npz', baseline=state, previous=previous,
                                difference=difference, previous_difference=previous_difference,
                                background=background, previous_background=previous_background, step=index)
            write_json(folder / 'progress.json', dict(state='running', step=index, steps=arguments.steps,
                                                     elapsed=time.perf_counter() - started))
            print(json.dumps(dict(step=index, steps=arguments.steps, elapsed=time.perf_counter() - started)), flush=True)
    checks = [dict(name='Mixed difference evolved in heat-scaled variables without solution subtraction', passed=True),
              dict(name='Finite mixed response', passed=bool(np.isfinite(differences).all())),
              dict(name='Unprojected gravity constraints propagate', passed=float(np.max(constraints)) < .002, value=float(np.max(constraints))),
              dict(name='Scaled correction equations solved', passed=max(residuals) < 1e-8, value=max(residuals)),
              dict(name='Photon number at all sampled times', passed=max(number_errors) < 1e-10, value=max(number_errors)),
              dict(name='Exactly opposite photon-gas energy and momentum', passed=max(exchange_errors) < 1e-10, value=max(exchange_errors)),
              dict(name='Finite forced nonlinear background correction', passed=bool(np.isfinite(corrections).all()))]
    np.savez_compressed(folder / 'evolution.npz', expansion=moments, baseline_states=states,
                        scaled_differences=differences, scaled_features=features, baseline_features=baselines,
                        constraints=constraints, background_corrections=corrections, heat=heat,
                        steps=arguments.steps, basis_count=arguments.count, maximum=arguments.maximum)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        model=arguments.model, basis_count=arguments.count, maximum=arguments.maximum,
                        steps=arguments.steps, bank=arguments.bank, stride=arguments.stride,
                        include_residual=arguments.include_residual, initial=initial,
                        difference_scaling='Physical wave correction = heat * scaled_differences; background correction = heat^2 * background_corrections.',
                        scope='Exact mixed Jacobian on the saved 24-function conservative background, with forced leading nonlinear background residual evolved separately. No observational refit.',
                        elapsed=time.perf_counter() - started), __file__,
           [ROOT / 'mixed_wave_system.py', ROOT / 'stable_pair.py',
            PARENT / 'thermal_wave_system.py', PARENT / 'background_geometry.py', PARENT / 'high_degree_waves.py',
            *system.bank.inputs, *system.ladder.inputs, system.geometry.source, system.geometry.parent.source])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--model', choices=['heavy', 'cold'], required=True)
    parser.add_argument('--count', type=int, default=24)
    parser.add_argument('--steps', type=int, default=3200)
    parser.add_argument('--maximum', type=int, default=8)
    parser.add_argument('--bank', default='fine16')
    parser.add_argument('--stride', type=int, default=1)
    parser.add_argument('--include-residual', action='store_true')
    main(parser.parse_args())
