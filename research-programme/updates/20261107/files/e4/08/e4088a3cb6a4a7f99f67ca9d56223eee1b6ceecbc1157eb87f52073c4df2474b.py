import argparse
from thermal_wave_common import *
from kernel_ladder import KernelLadder


def main(arguments):
    modest()
    folder = ROOT / 'backgrounds' / arguments.name
    assert not folder.exists()
    folder.mkdir(parents=True, exist_ok=False)
    ladder = KernelLadder(arguments.count)
    basis = ladder.basis
    background = thermal.ThermalBackground(arguments.model)
    heat = background.chi
    steps, step = arguments.steps, background.end / arguments.steps
    potential, previous = np.zeros(basis.count), np.zeros(basis.count)
    temperature, old_temperature, work, old_work = 0., 0., 0., 0.
    history, profiles, errors = [], [], []
    started = time.perf_counter()
    for index in range(steps + 1):
        expansion = index * step
        local = background.at(expansion)
        if index:
            rate = local['coefficient'] / local['thermal_parameter']
            stiffness = ladder.at(local['thermal_parameter'], 0)[:basis.count, :basis.count]
            if index == 1:
                alpha, vector, scalar, work_history = 1 / step, potential / step, temperature / step, work / step
            else:
                alpha = 1.5 / step
                vector = (2 * potential - .5 * previous) / step
                scalar = (2 * temperature - .5 * old_temperature) / step
                work_history = (2 * work - .5 * old_work) / step
            thermal_source = -rate * stiffness @ basis.temperature
            solution = linalg.solve(alpha * basis.mass - rate * stiffness,
                                    np.column_stack([basis.mass @ vector, thermal_source]), assume_a='pos')
            free, response = solution[:, 0], solution[:, 1]
            updated_temperature = (heat * scalar - 1 - basis.energy @ (alpha * free - vector)) / (
                heat * (alpha + 1) + alpha * (basis.energy @ response))
            updated = free + response * updated_temperature
            updated_work = (work_history + 1 + heat * updated_temperature) / alpha
            equation = alpha * basis.mass @ updated - basis.mass @ vector - rate * stiffness @ (updated - basis.temperature * updated_temperature)
            norm = max(np.linalg.norm(rate * stiffness @ (updated - basis.temperature * updated_temperature)), 1e-30)
            errors.append(float(np.linalg.norm(equation) / norm))
            previous, potential = potential, updated
            old_temperature, temperature = temperature, updated_temperature
            old_work, work = work, updated_work
        energy = float(basis.energy @ potential)
        history.append([expansion, energy, temperature, work, float(basis.number @ potential)])
        profiles.append(potential.copy())
        if index and index % max(1, steps // 10) == 0:
            write_json(folder / 'progress.json', dict(state='running', step=index, steps=steps, elapsed=time.perf_counter() - started))
    history = np.array(history)
    energy_balance = float(np.max(abs(history[:, 1] + heat * history[:, 2] + history[:, 3])))
    number_balance = float(np.max(abs(history[:, 4])))
    occupation_fraction = heat * (1 + 1 / np.expm1(basis.nodes)) * (basis.values @ potential)
    checks = [dict(name='Physical finite-shift background number conserved', passed=number_balance < 1e-8, value=number_balance),
              dict(name='Radiation plus plasma heat plus expansion work balance', passed=energy_balance < 1e-8, value=energy_balance),
              dict(name='Finite-capacity implicit equations solved', passed=max(errors) < 1e-7, value=max(errors)),
              dict(name='Positive photon occupation on spectral quadrature', passed=float(min(1 + occupation_fraction)) > 0),
              dict(name='Retained linear distortion remains small', passed=float(max(abs(occupation_fraction))) < .002,
                   value=float(max(abs(occupation_fraction))))]
    np.savez_compressed(folder / 'history.npz', expansion=history[:, 0], energy_scaled=history[:, 1],
                        temperature_scaled=history[:, 2], expansion_work=history[:, 3], number_scaled=history[:, 4],
                        profiles=np.array(profiles), heat=heat, coefficients=basis.coefficients,
                        norms=basis.norms, mean=basis.mean, theta0=background.theta0, start_scale=background.start_scale)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        model=arguments.model, basis_count=arguments.count, steps=steps, heat=heat,
                        final_energy_fraction=heat * history[-1, 1], final_temperature_fraction=heat * temperature,
                        kernel='Physical finite-shift polarized kernel, isotropic block; not Taylor Kompaneets',
                        reference_geometry= 'Retained parent to leading order in sourced heat capacity',
                        finite_heat_capacity_kept=True, photon_production_included=False,
                        elapsed=time.perf_counter() - started), __file__,
           [*ladder.inputs, ROOT / 'kernel_ladder.py', ROOT / 'stable_spectral_basis.py',
            background.parent.source, background.native_constants])
    print(json.dumps(dict(checks=checks, energy=heat * history[-1, 1], temperature=heat * temperature)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', choices=['heavy', 'cold'], default='heavy')
    parser.add_argument('--name', required=True)
    parser.add_argument('--count', type=int, default=16)
    parser.add_argument('--steps', type=int, default=800)
    main(parser.parse_args())
