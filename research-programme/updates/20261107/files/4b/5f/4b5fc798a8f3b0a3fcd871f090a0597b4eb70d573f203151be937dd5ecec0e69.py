import argparse
from emission_common import *
from emission_rates import EmissionMatrices


def main(arguments):
    modest()
    name = arguments.name or (arguments.model + str(arguments.count) + '-' + arguments.emission + '-' + str(arguments.steps))
    folder = ROOT / 'backgrounds' / name
    folder.mkdir(parents=True, exist_ok=False)
    basis = ConsistentBasis(arguments.count)
    ladder = ExtendedLadder(OBSERVER / 'banks' / ('basis' + str(arguments.count)), basis)
    emission = EmissionMatrices(basis, arguments.quadrature)
    background = thermal_wave.thermal.ThermalBackground(arguments.model)
    heat, step = background.chi, background.end / arguments.steps
    potential, previous = np.zeros(basis.count), np.zeros(basis.count)
    temperature, old_temperature, work, old_work, created, old_created = [0.] * 6
    history, profiles, errors, source_residuals = [], [], [], []
    started = time.perf_counter()
    for index in range(arguments.steps + 1):
        expansion = index * step
        local = background.at(expansion)
        if index:
            rate = local['coefficient'] / local['thermal_parameter']
            scattering = ladder.at(local['thermal_parameter'], 0)[:basis.count, :basis.count]
            damping = emission.at(local['thermal_parameter'], arguments.emission)
            stiffness = scattering - damping
            if index == 1:
                alpha, vector, scalar, work_history, number_history = 1 / step, potential / step, temperature / step, work / step, created / step
            else:
                alpha = 1.5 / step
                vector = (2 * potential - .5 * previous) / step
                scalar = (2 * temperature - .5 * old_temperature) / step
                work_history = (2 * work - .5 * old_work) / step
                number_history = (2 * created - .5 * old_created) / step
            thermal_source = -rate * stiffness @ basis.temperature
            solution = linalg.solve(alpha * basis.mass - rate * stiffness,
                np.column_stack([basis.mass @ vector, thermal_source]), assume_a='pos')
            free, response = solution[:, 0], solution[:, 1]
            updated_temperature = (heat * scalar - 1 - basis.energy @ (alpha * free - vector)) / (
                heat * (alpha + 1) + alpha * (basis.energy @ response))
            updated = free + response * updated_temperature
            updated_work = (work_history + 1 + heat * updated_temperature) / alpha
            photon_emission = -rate * damping @ (updated - basis.temperature * updated_temperature)
            updated_created = (number_history + basis.chemical @ photon_emission) / alpha
            equation = alpha * basis.mass @ updated - basis.mass @ vector - rate * stiffness @ (updated - basis.temperature * updated_temperature)
            norm = max(linalg.norm(rate * stiffness @ (updated - basis.temperature * updated_temperature)), 1e-30)
            errors.append(float(linalg.norm(equation) / norm))
            source_residuals.append(float(basis.temperature @ photon_emission))
            previous, potential = potential, updated
            old_temperature, temperature = temperature, updated_temperature
            old_work, work = work, updated_work
            old_created, created = created, updated_created
        history.append([expansion, basis.energy @ potential, temperature, work, basis.number @ potential, created])
        profiles.append(potential.copy())
    history, profiles = np.asarray(history), np.asarray(profiles)
    energy_balance = float(np.max(abs(history[:, 1] + heat * history[:, 2] + history[:, 3])))
    number_balance = float(np.max(abs(history[:, 4] - history[:, 5])))
    occupation_fraction = heat * (1 + 1 / np.expm1(emission.frequency))[None, :] * (profiles @ emission.values.T)
    checks = [
        dict(name='Radiation plus finite gas heat plus expansion work balance', passed=energy_balance < 1e-8, value=energy_balance),
        dict(name='Photon number follows integrated emission source', passed=number_balance < 1e-8, value=number_balance),
        dict(name='Coupled finite-capacity implicit kinetic equations solved', passed=max(errors) < 1e-7, value=max(errors)),
        dict(name='Photon occupation remains positive at independent quadrature', passed=bool(np.min(1 + occupation_fraction) > 0)),
        dict(name='Retained linear occupation distortion remains small', passed=float(np.max(abs(occupation_fraction))) < .002, value=float(np.max(abs(occupation_fraction)))),
        dict(name='Emission-off number control or nonzero physical number response', passed=abs(history[-1, 4]) < 1e-8 if arguments.emission == 'none' else abs(history[-1, 4]) > 1e-6, value=float(history[-1, 4]))]
    np.savez_compressed(folder / 'history.npz', expansion=history[:, 0], energy_scaled=history[:, 1],
        temperature_scaled=history[:, 2], expansion_work=history[:, 3], number_scaled=history[:, 4],
        integrated_number_source=history[:, 5], profiles=profiles, heat=heat, basis_count=basis.count,
        temperature_template=basis.temperature, number_row=basis.number, energy_row=basis.energy)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        model=arguments.model, basis_count=basis.count, steps=arguments.steps, heat=heat, emission=arguments.emission,
        emission_quadrature=arguments.quadrature, elapsed=time.perf_counter() - started,
        final_energy_fraction=float(heat * history[-1, 1]), final_temperature_fraction=float(heat * history[-1, 2]),
        final_photon_number_moment=float(heat * history[-1, 4]),
        kernel='Unchanged physical finite-shift Compton kernel, plus sourced linearized isotropic DC emission/absorption.',
        coefficient_scope='DC coefficient evaluated on reference Planck spectrum, correct at leading background heat order; finite gas heat capacity retained.',
        bremsstrahlung_included=False, full_double_compton_redistribution_included=False,
        reference_geometry='Retained parent Hubble history to leading sourced-heat order; emitting stress geometry checked separately.',
        no_photon_number_conservation_projection=True), __file__,
        [ROOT / 'emission_rates.py', OBSERVER / 'consistent_spectral_basis.py', OBSERVER / 'extended_system.py',
         THERMAL_STAGE / 'evolve_expanding_spectrum.py', *ladder.inputs, background.parent.source, background.native_constants])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
        model=arguments.model, emission=arguments.emission, energy=heat * history[-1, 1],
        number=heat * history[-1, 4], temperature=heat * history[-1, 2], elapsed=time.perf_counter() - started)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', choices=['heavy', 'cold'], required=True)
    parser.add_argument('--count', type=int, default=36)
    parser.add_argument('--steps', type=int, default=3200)
    parser.add_argument('--quadrature', type=int, default=600)
    parser.add_argument('--emission', choices=['none', 'soft', 'dc'], default='dc')
    parser.add_argument('--name')
    main(parser.parse_args())
