import argparse
from scaled_system import *


def main(arguments):
    modest()
    folder = ROOT / 'waves' / (arguments.model + str(arguments.count) + '-' + str(arguments.steps))
    folder.mkdir(parents=True, exist_ok=False)
    system = ScaledSystem(arguments.model, arguments.count)
    baseline, provenance = system.initial()
    difference = np.zeros_like(baseline)
    previous, previous_difference = baseline.copy(), difference.copy()
    step = system.physical.geometry.thermal.end / arguments.steps
    times, bases, differences, shapes, base_shapes, temperatures, constraints, features = [], [], [], [], [], [], [], []
    residuals = []
    started = time.perf_counter()
    for index in range(arguments.steps + 1):
        expansion = index * step
        if index:
            mass, operator, correction = system.matrices(expansion)
            if index == 1:
                alpha, history, delta_history = 1 / step, baseline / step, difference / step
            else:
                alpha = 1.5 / step
                history = (2 * baseline - .5 * previous) / step
                delta_history = (2 * difference - .5 * previous_difference) / step
            baseline_factor = sparse_linalg.splu(alpha * mass - operator)
            full_factor = sparse_linalg.splu(alpha * mass - operator - correction)
            new_baseline = baseline_factor.solve(mass @ history)
            right = mass @ delta_history + correction @ new_baseline
            new_difference = full_factor.solve(right)
            residuals.append(float(linalg.norm((alpha * mass - operator - correction) @ new_difference - right) / max(linalg.norm(right), 1e-100)))
            previous, baseline = baseline, new_baseline
            previous_difference, difference = difference, new_difference
        if index % max(1, arguments.steps // 40) == 0 or index == arguments.steps:
            times.append(expansion)
            bases.append(baseline.copy())
            differences.append(difference.copy())
            reading = system.readout(expansion, baseline + difference)
            shapes.append(reading['shapes'])
            base_shapes.append(system.readout(expansion, baseline)['shapes'])
            temperatures.append(reading['temperatures'])
            raw, scale = system.constraints(expansion, baseline + difference)
            constraints.append(abs(raw) / scale)
            features.append(system.physical.features(expansion, system.physical_state(baseline + difference)))
        if index and index % max(1, arguments.steps // 10) == 0:
            np.savez_compressed(folder / 'checkpoint.npz', baseline=baseline, previous=previous,
                                difference=difference, previous_difference=previous_difference, step=index, steps=arguments.steps)
            write_json(folder / 'progress.json', dict(state='running', step=index, steps=arguments.steps, elapsed=time.perf_counter() - started))
            print(json.dumps(dict(step=index, steps=arguments.steps, elapsed=time.perf_counter() - started)), flush=True)
    number_error = float(np.max(abs(np.asarray(shapes) @ system.basis.number))) / max(float(np.max(spectral_norm(np.asarray(shapes), system.basis.mass))), 1e-100)
    checks = [dict(name='Finite directly evolved shape and full state', passed=bool(np.isfinite(shapes).all() and np.isfinite(bases).all() and np.isfinite(differences).all())),
              dict(name='Scaled paired mixed-response equation solved', passed=max(residuals) < 1e-8, value=max(residuals)),
              dict(name='Unprojected metric constraints propagate', passed=float(np.max(constraints)) < .002, value=float(np.max(constraints))),
              dict(name='Direct shape readout retains number-free split', passed=number_error < 1e-10, value=number_error)]
    np.savez_compressed(folder / 'evolution.npz', expansion=times, baseline_coordinates=bases,
                        coordinate_differences=differences, full_shapes=shapes, baseline_shapes=base_shapes,
                        full_temperatures=temperatures, full_features=features, constraints=constraints,
                        heat=system.heat, basis_count=arguments.count, steps=arguments.steps, maximum=system.maximum)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        model=arguments.model, basis_count=arguments.count, steps=arguments.steps,
                        elapsed=time.perf_counter() - started, initial=provenance,
                        coordinates='Each spectral block: theta then y; gas index10=eta. X=q_T theta+chi V y, t=theta0+chi eta.',
                        difference_is_coordinate_difference_not_divided_by_heat=True,
                        microscopic_banks_reused_unchanged=True, no_new_physical_coefficient=True), __file__,
           [ROOT / 'scaled_system.py', PARENT / 'spectral_readout.py', *sorted(set(system.inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, choices=['heavy', 'cold'])
    parser.add_argument('--count', type=int, default=36)
    parser.add_argument('--steps', type=int, default=3200)
    main(parser.parse_args())
