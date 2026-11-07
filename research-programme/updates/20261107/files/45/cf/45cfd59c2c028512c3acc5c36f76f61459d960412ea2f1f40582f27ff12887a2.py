import argparse
from wave_common import *
from infrared_ladder import InfraredLadder
from integrated_dc import IntegratedDCEmission


def evolve(model, steps=6400, offset=0., tangent=True, omit_ion=False):
    ladder = InfraredLadder(PARENT / 'banks/infrared96-q700')
    basis = ladder.basis
    background = thermal_wave.thermal.ThermalBackground(model)
    emission = IntegratedDCEmission(basis, background, 900, 81)
    heat = background.chi
    density = 1 + offset
    local_heat = heat * density
    step = background.end / steps
    profile = np.zeros(basis.count)
    response = np.zeros(basis.count)
    old_profile, old_response = profile.copy(), response.copy()
    temperature, old_temperature, gas_response, old_gas_response = [0.] * 4
    work, old_work, response_work, old_response_work = [0.] * 4
    number, old_number, response_number, old_response_number = [0.] * 4
    snapshots, profiles, responses, errors, tangent_errors = [], [], [], [], []
    for index in range(steps + 1):
        expansion = index * step
        local = background.at(expansion)
        theta = local['thermal_parameter']
        if index:
            rate = local['coefficient'] / theta
            scattering = ladder.at(theta, 0)[:basis.count, :basis.count]
            dc = emission.at(theta, 'dc')
            br = emission.at(theta, 'dcbr') - dc
            kernel = scattering - dc - density * br
            damping = dc + density * br
            weighted = density * rate * kernel
            alpha = (1 if index == 1 else 1.5) / step
            def history(current, previous):
                return current / step if index == 1 else (2 * current - .5 * previous) / step
            profile_history = history(profile, old_profile)
            temperature_history = history(temperature, old_temperature)
            matrix = alpha * basis.mass - weighted
            factor = linalg.cho_factor(matrix)
            free, thermal = linalg.cho_solve(factor, np.column_stack([
                basis.mass @ profile_history, -weighted @ basis.temperature])).T
            denominator = local_heat * (alpha + 1) + alpha * (basis.energy @ thermal)
            updated_temperature = (local_heat * temperature_history - 1 -
                basis.energy @ (alpha * free - profile_history)) / denominator
            updated = free + thermal * updated_temperature
            departure = updated - basis.temperature * updated_temperature
            profile_prime = alpha * updated - profile_history
            work_updated = (history(work, old_work) + 1 + local_heat * updated_temperature) / alpha
            emission_source = -density * rate * damping @ departure
            number_updated = (history(number, old_number) + basis.chemical @ emission_source) / alpha
            residual = matrix @ updated - basis.mass @ profile_history + weighted @ basis.temperature * updated_temperature
            errors.append(float(linalg.norm(residual) / max(linalg.norm(weighted @ departure), 1e-30)))
            if tangent:
                assert offset == 0.
                response_history = history(response, old_response)
                gas_history = history(gas_response, old_gas_response)
                ion_forcing = np.zeros(basis.count) if omit_ion else -rate * br @ departure
                forcing = basis.mass @ profile_prime + ion_forcing
                response_free = linalg.cho_solve(factor, basis.mass @ response_history + forcing)
                updated_gas = (heat * gas_history + basis.energy @ profile_prime -
                    basis.energy @ (alpha * response_free - response_history)) / denominator
                updated_response = response_free + thermal * updated_gas
                response_prime = alpha * updated_response - response_history
                response_work_updated = (history(response_work, old_response_work) +
                    1 + heat * updated_temperature + heat * updated_gas) / alpha
                response_emission = -rate * damping @ (updated_response - basis.temperature * updated_gas) - rate * damping @ departure + ion_forcing
                response_number_updated = (history(response_number, old_response_number) + basis.chemical @ response_emission) / alpha
                tangent_residual = basis.mass @ response_prime - weighted @ (updated_response - basis.temperature * updated_gas) - forcing
                tangent_errors.append(float(linalg.norm(tangent_residual) / max(linalg.norm(forcing), 1e-30)))
                old_response, response = response, updated_response
                old_gas_response, gas_response = gas_response, updated_gas
                old_response_work, response_work = response_work, response_work_updated
                old_response_number, response_number = response_number, response_number_updated
            old_profile, profile = profile, updated
            old_temperature, temperature = temperature, updated_temperature
            old_work, work = work, work_updated
            old_number, number = number, number_updated
        if index % max(1, steps // 80) == 0 or index == steps:
            snapshots.append([expansion, basis.energy @ profile, temperature, work, basis.number @ profile,
                              number, basis.energy @ response, gas_response, response_work, basis.number @ response, response_number])
            profiles.append(profile.copy())
            responses.append(response.copy())
    snapshots = np.array(snapshots)
    checks = [check('Background kinetic residual', max(errors), 1e-7),
              check('Background energy plus expansion work', np.max(abs(snapshots[:, 1] + local_heat * snapshots[:, 2] + snapshots[:, 3])), 1e-8),
              check('Background photon number follows emission', np.max(abs(snapshots[:, 4] - snapshots[:, 5])), 1e-8)]
    if tangent:
        checks += [check('Derived density tangent kinetic residual', max(tangent_errors), 1e-7),
                   check('Density tangent total energy and expansion work',
                         np.max(abs(snapshots[:, 6] + heat * (1 + snapshots[:, 2] + snapshots[:, 7]) + snapshots[:, 8] - heat)), 1e-8),
                   check('Density tangent photon number follows source', np.max(abs(snapshots[:, 9] - snapshots[:, 10])), 1e-8)]
    return dict(history=snapshots, profiles=np.asarray(profiles), responses=np.asarray(responses),
                heat=heat, density_factor=density, mass=basis.mass, number=basis.number,
                energy=basis.energy, temperature_template=basis.temperature), checks, ladder, emission, background


def main(arguments):
    modest()
    folder = ROOT / 'density' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    saved, checks, ladder, emission, background = evolve(arguments.model, arguments.steps, arguments.offset,
                                                       arguments.offset == 0., arguments.omit_ion)
    np.savez_compressed(folder / 'history.npz', **saved)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        model=arguments.model, steps=arguments.steps, density_offset=arguments.offset,
        ion_density_derivative_omitted=arguments.omit_ion, elapsed=time.perf_counter() - started,
        scope='Fixed-reference-expansion density derivative of the Stage79 retained finite-capacity, leading-heat kinetic model; not yet a self-gravitating finite-k mode.',
        no_number_conservation_projection=True, no_new_fitted_parameter=True), __file__,
        [PARENT / 'integrated_dc.py', PARENT / 'sourced_emission.py', PARENT / 'infrared_ladder.py',
         *ladder.inputs, *emission.inputs, background.parent.source, background.native_constants])
    print(json.dumps(dict(name=arguments.name, elapsed=time.perf_counter() - started,
                         failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, choices=['heavy', 'cold'])
    parser.add_argument('--name', required=True)
    parser.add_argument('--steps', type=int, default=6400)
    parser.add_argument('--offset', type=float, default=0.)
    parser.add_argument('--omit-ion', action='store_true')
    main(parser.parse_args())
