from scaled_system import *
import mpmath as mp


def main():
    modest()
    mp.mp.dps = 70
    folder = ROOT / 'results/scaled-equations'
    folder.mkdir(parents=True, exist_ok=False)
    checks, inputs = [], []
    generator = np.random.default_rng(7801)
    for model in ['heavy', 'cold']:
        system = ScaledSystem(model)
        inputs.extend(system.inputs)
        initial, provenance = system.initial()
        checks.append(dict(name=model + ': thermal initial condition unchanged', passed=provenance['physical_reencoding_error'] < 1e-15, value=provenance['physical_reencoding_error']))
        for expansion in [0., .7, 2.1]:
            mass, operator, delta = system.matrices(expansion)
            old_mass, old_operator, _ = system.physical.matrices(expansion)
            old_delta = system.heat * system.physical.correction(expansion, False)
            state = generator.normal(size=system.size) + 1j * generator.normal(size=system.size)
            rate = sparse_linalg.spsolve(mass, (operator + delta) @ state)
            right = (old_operator + old_delta) @ system.physical_state(state)
            error = float(linalg.norm(old_mass @ system.physical_state(rate) - right) / linalg.norm(right))
            checks.append(dict(name=model + ':' + str(expansion) + ': full equation equivalence including metric and matter', passed=error < 1e-11, value=error))
            local = system.physical.background(expansion)
            rates = sparse_linalg.spsolve(mass, delta)
            physical_rates = system.transform @ rates
            first, dipole = system.mode_slice(0), system.mode_slice(1)
            photon_energy = np.asarray(system.basis.energy @ physical_rates[first].toarray()).ravel()
            energy_error = float(linalg.norm(photon_energy + local['heat'] * physical_rates[10].toarray().ravel()) / max(linalg.norm(photon_energy), 1e-100))
            photon_momentum = np.asarray(system.basis.energy @ physical_rates[dipole].toarray()).ravel() / 3
            momentum_error = float(linalg.norm(photon_momentum + local['inertia'] * physical_rates[9].toarray().ravel()) / max(linalg.norm(photon_momentum), 1e-100))
            number_error = float(linalg.norm(system.basis.number @ physical_rates[first].toarray()) / max(linalg.norm(physical_rates[first].toarray()), 1e-100))
            checks.extend([
                dict(name=model + ':' + str(expansion) + ': mixed operator retains paired energy exchange', passed=energy_error < 1e-10, value=energy_error),
                dict(name=model + ':' + str(expansion) + ': mixed operator retains paired momentum exchange', passed=momentum_error < 1e-10, value=momentum_error),
                dict(name=model + ':' + str(expansion) + ': mixed operator conserves photon number', passed=number_error < 1e-10, value=number_error)])
            background = system.reference_readout.background(expansion)
            large, small, _ = system.collision_parts(expansion, 0, local, background)
            thermal = np.zeros(system.size)
            thermal[first.start] = 1.
            thermal_residual = float(linalg.norm((large + system.heat * small) @ thermal))
            checks.append(dict(name=model + ':' + str(expansion) + ': shared photon-gas temperature collision null', passed=thermal_residual == 0., value=thermal_residual))
            reading = system.readout(expansion, state)
            projection = system.reference_readout.apply(expansion, system.physical_state(state))
            difference = float(np.max(abs(reading['shapes'] - projection['shapes'])))
            checks.append(dict(name=model + ':' + str(expansion) + ': direct readout matches physical reconstruction to its rounding scale', passed=difference < 2e-14, value=difference))
            heat = mp.mpf(system.heat)
            number = [mp.mpf(value) for value in system.basis.number]
            density = mp.mpc(complex(system.physical.density_row @ state))
            shape_values = system.complement @ state[first.start + 1:first.stop]
            amplitude = mp.mpc(complex(state[first.start]))
            dilation = [mp.mpf(base) + mp.mpf(background['heat']) * mp.mpf(change) for base, change in zip(system.temperature, background['dilation_change'])]
            physical = [mp.mpf(base) * amplitude + heat * mp.mpc(complex(change)) for base, change in zip(system.temperature, shape_values)]
            relational = [value + (mp.mpf(background['heat']) * mp.mpf(prime) - tangent) * density / 3 for value, prime, tangent in zip(physical, background['profile_prime'], dilation)]
            temperature = mp.fsum(moment * value for moment, value in zip(number, relational)) / mp.fsum(moment * value for moment, value in zip(number, dilation))
            precise = np.array([complex(value - tangent * temperature) for value, tangent in zip(relational, dilation)])
            precise_error = float(linalg.norm(reading['shapes'][0] - precise) / max(linalg.norm(precise), 1e-100))
            checks.append(dict(name=model + ':' + str(expansion) + ': direct small readout independently matches70-digit reconstruction', passed=precise_error < 1e-10, value=precise_error))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        same_fields_and_coefficients=True, no_gauge_or_metric_projection_added=True,
                        full_operator_equivalence_gate=1e-11, small_readout_reference_gate=1e-10), __file__,
           [ROOT / 'scaled_system.py', PARENT / 'spectral_readout.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
