from common235 import *
import state235
from functools import lru_cache
import copy


@lru_cache(maxsize=256)
def scaled_bessel(mass_text, temperature_text):
    inverse = mp.mpf(mass_text) / mp.mpf(temperature_text)
    return mp.exp(inverse) * mp.besselk(2, inverse)


def massive_raw(event, potential, gas, velocity, eta):
    temperature = scalar(event['temperature'])
    mass = mp.sqrt(1 + eta)
    ratio = 1 + gas
    mass_text = mp.nstr(mass, 85)
    normalization = scaled_bessel(mass_text, mp.nstr(temperature, 85)) / (ratio * scaled_bessel(mass_text, mp.nstr(temperature * ratio, 85)))
    initial = list(map(scalar, event['electron_initial']))
    final = [value + scalar(transfer) for value, transfer in zip(initial, event['electron_transfer'])]
    lorentz = 1 / mp.sqrt(1 - mp.fsum(value**2 for value in velocity))
    rates = []
    for momentum in (initial, final):
        shifted = lorentz * (momentum[0] - mp.fsum(value * speed for value, speed in zip(momentum[1:], velocity)))
        rates.append(mp.exp((momentum[0] - mass) / temperature - (shifted - mass) / (temperature * ratio)) * normalization)
    for sign, frequency, change in zip(event['signs'], event['frequencies'], potential):
        reference = 1 / mp.expm1(scalar(frequency))
        occupation = reference + reference * (1 + reference) * change
        rates[0] *= occupation / reference if sign < 0 else (1 + occupation) / (1 + reference)
        rates[1] *= (1 + occupation) / (1 + reference) if sign < 0 else occupation / reference
    return rates[0] - rates[1]


def main():
    modest()
    config, frozen = state235.state_protocol()
    target = ROOT / 'results/state-product-control.json'
    assert not target.exists()
    write(ROOT / 'product-configuration.json', dict(frozen_at=now(), script_sha256=digest(Path(__file__)),
        eta_step='1e-12', background_step='1e-4', wave_step='1e-10', tolerance=1e-10,
        scope='Independent nonlinear normalized-mass gas/photon product, phase and population terms; canonical derivative is separately refined/replayed',
        wave_coefficients=np.r_[np.cos(np.arange(98) * .29 + .3), .3].tolist(), tested_output_row=4))
    original, features, models = setup(config)
    tests_owner = models[0]['difference'].tests
    mass_maps = packet(ROOT / 'results/mass-coefficients.npz')
    checks, records = [], []
    with mp.workdps(80):
        eta_step, background_step, wave_step = map(mp.mpf, ('1e-12', '1e-4', '1e-10'))
        wave = np.r_[np.cos(np.arange(98) * .29 + .3), .3]
        for row in config['events']:
            parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
            tangent = state235.phase_geometry(parameters)
            event = tangent['event']
            frequency = np.array(event['frequencies'])
            tests = tests_owner.evaluate(frequency)
            test_prime = tests_owner.derivative(frequency) * np.array(list(map(float, tangent['frequency_shift'])))[:, None]
            velocity = parameters['velocity']
            gamma_squared = 1 / (1 - velocity @ velocity)
            score = scalar(angular.inherited.normalized_mass_score(gamma_squared * (velocity @ velocity), parameters['temperature']))
            rate_prime = scalar(tangent['phase'] + tangent['bose']) + score
            for join in config['joins']:
                basis = features.evaluate(frequency, join)
                basis_prime = features.evaluate(frequency, join, True) * np.array(list(map(float, tangent['frequency_shift'])))[:, None]
                mass_vector = np.r_[mass_maps[f'{row["label"]}:join{join}:order6:mass_coefficients'], 0.]
                for state in config['states']:
                    physical = [scalar(config['heat']) * mp.mpf(value) for value in state['coefficients']]
                    background = [state235.contraction(line, physical[:98]) for line in basis]
                    background_prime = [state235.contraction(line, physical[:98]) for line in basis_prime]
                    mass_background = state235.contraction(mass_vector, physical)
                    for degree in config['multipoles']:
                        harmonic = angular.angular_feature(np.array(event['directions']), degree)
                        harmonic_prime = angular.angular_feature_derivative(np.array(event['directions']), tangent['direction_shift'], degree)
                        left = np.einsum('n,na,ni->ai', event['signs'], tests, harmonic)
                        left_prime = np.einsum('n,na,ni->ai', event['signs'], test_prime, harmonic) + np.einsum('n,na,ni->ai', event['signs'], tests, harmonic_prime)
                        unit = state235.unit_state(parameters, features, tests_owner, join, physical, degree, config['canonical_steps'][0])
                        equilibrium = sum(unit['equilibrium'][name] for name in ('phase', 'observable', 'population'))
                        mixed = sum(unit['mixed'][name] for name in ('phase', 'observable', 'population'))
                        predicted = float(tangent['planck_mass_squared']) * mixed + float(mass_background) * equilibrium
                        if degree == 0:
                            predicted += np.outer(equilibrium @ np.array(list(map(float, physical))), mass_vector)
                        expected = scalar(predicted[4] @ wave)
                        measured = mp.mpf(0)
                        for component in range(harmonic.shape[-1]):
                            wave_photon = [state235.contraction(line, list(map(scalar, wave[:98]))) * scalar(harmonic[index, component]) for index, line in enumerate(basis)]
                            wave_prime = [state235.contraction(basis_prime[index], list(map(scalar, wave[:98]))) * scalar(harmonic[index, component])
                                + state235.contraction(basis[index], list(map(scalar, wave[:98]))) * scalar(harmonic_prime[index, component]) for index in range(2)]
                            wave_gas = scalar(wave[-1]) if degree == 0 else mp.mpf(0)
                            wave_velocity = [scalar(wave[-1]) * int(degree == 1 and axis == component) for axis in range(3)]
                            mass_wave = state235.contraction(mass_vector, list(map(scalar, wave))) if degree == 0 else mp.mpf(0)
                            sampled = []
                            for background_sign, wave_sign in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                                amplitude, disturbance = background_sign * background_step, wave_sign * wave_step
                                eta_values = []
                                for eta in (eta_step, -eta_step):
                                    shifted = copy.deepcopy(event)
                                    for name, changes in [('frequencies', tangent['frequency_shift']), ('electron_initial', tangent['initial_shift']), ('electron_transfer', tangent['transfer_shift'])]:
                                        shifted[name] = [scalar(value) + eta * change for value, change in zip(event[name], changes)]
                                    potential = [amplitude * (before + eta * before_prime) + disturbance * (change + eta * change_prime)
                                        for before, before_prime, change, change_prime in zip(background, background_prime, wave_photon, wave_prime)]
                                    flux = massive_raw(shifted, potential, amplitude * physical[-1] + disturbance * wave_gas,
                                        [disturbance * value for value in wave_velocity], eta)
                                    weak_left = scalar(left[4, component]) + eta * scalar(left_prime[4, component])
                                    eta_values.append((1 + eta * rate_prime) * weak_left * flux / 2)
                                state_source = (eta_values[0] - eta_values[1]) / (2 * eta_step)
                                sampled.append((tangent['planck_mass_squared'] + amplitude * mass_background + disturbance * mass_wave) * state_source)
                            measured += (sampled[0] - sampled[1] - sampled[2] + sampled[3]) / (4 * background_step * wave_step * (2 * degree + 1))
                        error = float(abs(measured - expected) / max(abs(expected), mp.mpf('1e-300')))
                        prefix = f'{row["label"]}:join{join}:{state["model"]}:{state["history"]}:l{degree}'
                        check(checks, prefix + ':nonlinear state product', error)
                        records.append(dict(anchor=row['label'], join=join, model=state['model'], history=state['history'], degree=degree, relative_error=error))
            print(json.dumps(dict(anchor=row['label'], checks=len(checks), failed=sum(not entry['passed'] for entry in checks))), flush=True)
    failed = [entry for entry in checks if not entry['passed']]
    write(target, dict(state='complete', qualified=not failed, checks=checks, failed=failed, records=records, finished_at=now(),
        scope='Nonlinear phase/observable/population product on frozen broad wave and one weak row, all angular components; not every matrix element'))
    print(json.dumps(dict(checks=len(checks), failed=failed, maximum_relative_error=max(row['relative_error'] for row in records))), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    main()
