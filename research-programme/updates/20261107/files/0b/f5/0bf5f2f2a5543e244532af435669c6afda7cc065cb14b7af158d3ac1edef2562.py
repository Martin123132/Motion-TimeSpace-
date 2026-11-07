from thermal_wave_common import *
from thermal_wave_system import ThermalWaveSystem
import sympy as symbolic


def coefficients(first_frequency, second_frequency, first_potential, second_potential, heat, temperature_shift, theta, gamma):
    first_planck, second_planck = 1 / np.expm1(first_frequency), 1 / np.expm1(second_frequency)
    electron_theta = theta * (1 + temperature_shift)
    log_normalization = (-math.log1p(temperature_shift)
                         + math.log(special.kve(2, 1 / theta) / special.kve(2, 1 / electron_theta)))
    log_forward = (gamma - 1) * temperature_shift / (theta * (1 + temperature_shift)) + log_normalization
    log_ratio = (first_frequency - second_frequency) * temperature_shift / (1 + temperature_shift)
    forward = np.exp(log_forward)
    reverse = np.exp(log_forward + log_ratio)
    difference = -forward * np.expm1(log_ratio)
    left_defect = (np.expm1(log_forward) + difference * first_planck
                   + heat * second_potential * (forward * (second_planck - first_planck)
                                               + difference * first_planck * (1 + second_planck)))
    right_defect = (np.expm1(log_forward + log_ratio) - difference * second_planck
                    + heat * first_potential * (reverse * (first_planck - second_planck)
                                               - difference * second_planck * (1 + first_planck)))
    return left_defect, right_defect


def algebra():
    first, second, first_planck, second_planck, forward, reverse = symbolic.symbols('N_i N_j n_i n_j a b')
    flux = forward * first / first_planck * (1 + second) / (1 + second_planck) - reverse * second / second_planck * (1 + first) / (1 + first_planck)
    left = forward * (1 + first_planck) * (1 + second) / (1 + second_planck) - reverse * first_planck * second / second_planck
    right = reverse * (1 + second_planck) * (1 + first) / (1 + first_planck) - forward * second_planck * first / first_planck
    equilibrium = {first: first_planck, second: second_planck, forward: 1, reverse: 1}
    checks = [
        dict(name='Intensity-pair incoming occupation derivative derived from Bose flux',
             passed=symbolic.simplify(symbolic.diff(flux, first) * first_planck * (1 + first_planck) - left) == 0),
        dict(name='Intensity-pair outgoing occupation derivative derived from Bose flux',
             passed=symbolic.simplify(symbolic.diff(flux, second) * second_planck * (1 + second_planck) + right) == 0),
        dict(name='Both derivatives reduce to the retained equilibrium pair difference',
             passed=left.subs(equilibrium) == right.subs(equilibrium) == 1),
        dict(name='Planck equilibrium flux vanishes', passed=flux.subs(equilibrium) == 0),
    ]
    return checks


def main():
    modest()
    folder = ROOT / 'results/mixed-pair-coefficients'
    assert not folder.exists()
    checks, rows, inputs = algebra(), [], []
    for model in ['heavy', 'cold']:
        system = ThermalWaveSystem(model, 16, 8, 'physical')
        basis = system.basis
        for expansion in [0., .5 * system.geometry.thermal.end, system.geometry.thermal.end]:
            local = system.background(expansion)
            theta, heat = local['theta'], local['heat']
            temperature_shift = heat * float(system.geometry.temperature(expansion))
            background = system.geometry.profiles(expansion)
            frequency = np.geomspace(1.01 * basis.minimum, .99 * basis.maximum, 96)
            potential = basis.evaluate(frequency) @ background
            events = prior.event_geometry(theta, 6)
            speeds, _ = prior.prior.juttner_rule(theta, 6)
            gamma = np.repeat(1 / np.sqrt(1 - speeds ** 2), 2 * 6 ** 3)
            assert len(gamma) == len(events['weight'])
            maximum, occupation, samples = 0., 0., 0
            for incoming, initial in zip(frequency, potential):
                recoil = 1 / (1 + theta * incoming * events['incident'] * (1 - events['cosine']))
                outgoing = incoming * events['incident'] * recoil * events['outgoing']
                inside = (outgoing >= basis.minimum) & (outgoing <= basis.maximum)
                outgoing = outgoing[inside]
                final = basis.evaluate(outgoing) @ background
                left, right = coefficients(incoming, outgoing, initial, final, heat, temperature_shift, theta, gamma[inside])
                maximum = max(maximum, float(np.max(abs(left))), float(np.max(abs(right))))
                occupation = max(occupation, float(np.max(abs(heat * (1 + 1 / np.expm1(outgoing)) * final))))
                samples += len(outgoing)
            checks.append(dict(name=model + ': finite mixed occupation coefficients at ' + str(expansion),
                               passed=math.isfinite(maximum) and occupation < .002, maximum_sampled_coefficient_change=maximum,
                               maximum_sampled_fractional_occupation_change=occupation))
            if expansion == 0.:
                checks.append(dict(name=model + ': initial Planck mixed correction exactly zero', passed=maximum == 0.))
            rows.append(dict(model=model, expansion=expansion, theta=theta, temperature_shift=temperature_shift,
                             maximum_sampled_coefficient_change=maximum, maximum_sampled_fractional_occupation_change=occupation,
                             accepted_events=samples))
        inputs.extend([system.geometry.source, system.geometry.parent.source, *system.ladder.inputs])
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        scope='Exact scalar intensity-pair Jacobian algebra and sampled physical-background coefficients.',
                        full_polarized_nonequilibrium_generator_assembled=False, full_evolution_error_bound=False,
                        sampled_maximum_not_uniform_bound=True,
                        next_implementation='Assemble these pair derivatives and electron-temperature derivative, derive the full polarized lift, preserve photon number and opposite gas sources, then repeat the paired expanding wave.'),
           __file__, [ROOT / 'thermal_wave_system.py', ROOT / 'background_geometry.py', ROOT / 'kernel_ladder.py',
                      PARENT / 'grid_common.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
