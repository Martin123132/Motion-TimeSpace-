from common235 import *
from functools import lru_cache
import argparse


@lru_cache(maxsize=128)
def mean_energy(temperature_text, eta_text='0'):
    temperature, eta = mp.mpf(temperature_text), mp.mpf(eta_text)
    mass = mp.sqrt(1 + eta)
    inverse = mass / temperature
    return mass * mp.besselk(1, inverse) / mp.besselk(2, inverse) + 3 * temperature


@lru_cache(maxsize=16)
def mean_tangent(temperature_text):
    temperature = mp.mpf(temperature_text)
    ratio = mp.besselk(1, 1 / temperature) / mp.besselk(2, 1 / temperature)
    return 2 * ratio + (ratio**2 - 1) / (2 * temperature)


def contraction(values, coefficients):
    return mp.fsum(scalar(value) * coefficient for value, coefficient in zip(values, coefficients))


def phase_geometry(parameters):
    response = angular.inherited.source.previous.phase_response(mp.mpf(str(parameters['energy'])),
        mp.mpf(str(parameters['cosine'])), mp.mpf(str(parameters['temperature'])))
    mass = response['mass_squared']
    transform = mp.matrix(parameters['transform'].tolist())
    photon = transform * (response['photon_delta'] / mass)
    electron = transform * (response['electron_delta'] / mass)
    initial = transform * mp.matrix([mp.mpf('.5'), 0, 0, 0])
    event = geometry(parameters)
    momenta = np.array(event['photons'])
    shift = np.array([[0.] * 4, list(map(float, photon))])
    directions = np.array(event['directions'])
    norms = np.linalg.norm(momenta[:, 1:], axis=1)
    direction_shift = (shift[:, 1:] - directions * np.einsum('ni,ni->n', directions, shift[:, 1:])[:, None]) / norms[:, None]
    return dict(event=event, photon_shift=shift, frequency_shift=[mp.mpf(0), photon[0] / scalar(parameters['temperature'])],
        direction_shift=direction_shift, initial_shift=list(initial), transfer_shift=list(electron),
        phase=float(response['phase_delta'] / mass), planck_mass_squared=mass,
        bose=-(parameters['hard_bose'] - 1) * float(photon[0] / scalar(parameters['temperature'])))


def coefficients_at(event, potential, gas, eta=0):
    temperature = scalar(event['temperature'])
    mean = mean_energy(mp.nstr(temperature, 85), mp.nstr(eta, 85))
    initial = scalar(event['electron_initial'][0])
    transfer = list(map(scalar, event['electron_transfer']))
    scores = [(initial - mean) / temperature, (initial + transfer[0] - mean) / temperature]
    occupation = [1 / mp.expm1(scalar(value)) for value in event['frequencies']]
    forward = [value + int(sign < 0) for value, sign in zip(occupation, event['signs'])]
    reverse = [value + int(sign > 0) for value, sign in zip(occupation, event['signs'])]
    forward_photon = mp.fsum(value * shift for value, shift in zip(forward, potential))
    reverse_photon = mp.fsum(value * shift for value, shift in zip(reverse, potential))
    changes = [scores[0] * gas + forward_photon, scores[1] * gas + reverse_photon]
    initial_momentum = list(map(scalar, event['electron_initial'][1:]))
    final_momentum = [value + delta for value, delta in zip(initial_momentum, transfer[1:])]
    mixed = dict(photon=[first * (changes[0] - first * value) - second * (changes[1] - second * value)
        for first, second, value in zip(forward, reverse, potential)],
        gas=(scores[0]**2 - scores[1]**2 - 2 * (scores[0] - scores[1])) * gas + scores[0] * forward_photon - scores[1] * reverse_photon,
        velocity=[(before * (changes[0] - gas) - after * (changes[1] - gas)) / temperature for before, after in zip(initial_momentum, final_momentum)],
        density=changes[0] - changes[1])
    equilibrium = dict(photon=[mp.mpf(-sign) for sign in event['signs']], gas=-transfer[0] / temperature,
        velocity=[-value / temperature for value in transfer[1:]], density=mp.mpf(0))
    return dict(mixed=mixed, equilibrium=equilibrium, scores=scores, forward=forward, reverse=reverse,
        occupation=occupation, changes=changes, initial_momentum=initial_momentum, final_momentum=final_momentum)


def tangent_coefficients(event, tangent, potential, potential_shift, gas, omit_mean=False):
    state = coefficients_at(event, potential, gas)
    temperature = scalar(event['temperature'])
    mean_prime = mp.mpf(0) if omit_mean else mean_tangent(mp.nstr(temperature, 85))
    scores_prime = [(tangent['initial_shift'][0] - mean_prime) / temperature,
        (tangent['initial_shift'][0] + tangent['transfer_shift'][0] - mean_prime) / temperature]
    occupation_prime = [-value * (1 + value) * shift for value, shift in zip(state['occupation'], tangent['frequency_shift'])]
    forward_photon = mp.fsum(value * shift for value, shift in zip(state['forward'], potential))
    reverse_photon = mp.fsum(value * shift for value, shift in zip(state['reverse'], potential))
    forward_prime = mp.fsum(change * value + slope * value_prime for change, value, slope, value_prime in zip(occupation_prime, potential, state['forward'], potential_shift))
    reverse_prime = mp.fsum(change * value + slope * value_prime for change, value, slope, value_prime in zip(occupation_prime, potential, state['reverse'], potential_shift))
    changes_prime = [scores_prime[0] * gas + forward_prime, scores_prime[1] * gas + reverse_prime]
    photon_prime = []
    for forward, reverse, change, value, value_prime in zip(state['forward'], state['reverse'], occupation_prime, potential, potential_shift):
        photon_prime.append(change * (state['changes'][0] - forward * value) + forward * (changes_prime[0] - change * value - forward * value_prime)
            - change * (state['changes'][1] - reverse * value) - reverse * (changes_prime[1] - change * value - reverse * value_prime))
    gas_prime = 2 * ((state['scores'][0] - 1) * scores_prime[0] - (state['scores'][1] - 1) * scores_prime[1]) * gas
    gas_prime += scores_prime[0] * forward_photon + state['scores'][0] * forward_prime - scores_prime[1] * reverse_photon - state['scores'][1] * reverse_prime
    velocity_prime = []
    for axis in range(3):
        before, after = state['initial_momentum'][axis], state['final_momentum'][axis]
        before_prime = tangent['initial_shift'][axis + 1]
        after_prime = before_prime + tangent['transfer_shift'][axis + 1]
        velocity_prime.append((before_prime * (state['changes'][0] - gas) + before * changes_prime[0]
            - after_prime * (state['changes'][1] - gas) - after * changes_prime[1]) / temperature)
    mixed = dict(photon=photon_prime, gas=gas_prime, velocity=velocity_prime, density=changes_prime[0] - changes_prime[1])
    equilibrium = dict(photon=[mp.mpf(0)] * len(potential), gas=-tangent['transfer_shift'][0] / temperature,
        velocity=[-value / temperature for value in tangent['transfer_shift'][1:]], density=mp.mpf(0))
    return dict(equilibrium=equilibrium, mixed=mixed)


def projected_tangent(event, tangent, tests, test_shift, features, feature_shift, coefficients, coefficient_shift, degree):
    block, unused, left, right = projected(event, tests, features, coefficients, degree)
    harmonic = angular.angular_feature(np.array(event['directions']), degree)
    harmonic_prime = angular.angular_feature_derivative(np.array(event['directions']), tangent['direction_shift'], degree)
    left_prime = np.einsum('n,na,ni->ai', event['signs'], test_shift, harmonic)
    left_prime += np.einsum('n,na,ni->ai', event['signs'], tests, harmonic_prime)
    transfer_prime = np.array(list(map(float, tangent['transfer_shift']))) / event['temperature']
    gas_left_prime = transfer_prime[:1] if degree == 0 else transfer_prime[1:] if degree == 1 else np.zeros(harmonic.shape[-1])
    left_prime = np.vstack([left_prime, gas_left_prime])
    photon = np.array(list(map(float, coefficients['photon'])))
    photon_prime = np.array(list(map(float, coefficient_shift['photon'])))
    right_prime = np.einsum('n,na,ni->ai', photon_prime, features, harmonic)
    right_prime += np.einsum('n,na,ni->ai', photon, feature_shift, harmonic)
    right_prime += np.einsum('n,na,ni->ai', photon, features, harmonic_prime)
    gas_right_prime = np.array([float(coefficient_shift['gas'])]) if degree == 0 else np.array(list(map(float, coefficient_shift['velocity']))) if degree == 1 else np.zeros(harmonic.shape[-1])
    right_prime = np.vstack([right_prime, gas_right_prime])
    return block, (left_prime @ right.T + left @ right_prime.T) / (2 * degree + 1)


def bare_blocks(parameters, features, tests_owner, join, physical, degree):
    event = geometry(parameters)
    frequency = np.array(event['frequencies'])
    basis = features.evaluate(frequency, join)
    tests = tests_owner.evaluate(frequency)
    potential = [contraction(line, physical[:98]) for line in basis]
    stats = coefficients_at(event, potential, physical[-1])
    return {part: projected(event, tests, basis, stats[part], degree)[0] for part in ('equilibrium', 'mixed')}


def unit_state(parameters, features, tests_owner, join, physical, degree, step):
    tangent = phase_geometry(parameters)
    event = tangent['event']
    frequency = np.array(event['frequencies'])
    basis = features.evaluate(frequency, join)
    basis_prime = features.evaluate(frequency, join, True) * np.array(list(map(float, tangent['frequency_shift'])))[:, None]
    tests = tests_owner.evaluate(frequency)
    test_prime = np.array([tests_owner.derivative(value) for value in frequency]) * np.array(list(map(float, tangent['frequency_shift'])))[:, None]
    potential = [contraction(line, physical[:98]) for line in basis]
    potential_prime = [contraction(line, physical[:98]) for line in basis_prime]
    state = coefficients_at(event, potential, physical[-1])
    derivative = tangent_coefficients(event, tangent, potential, potential_prime, physical[-1])
    velocity = parameters['velocity']
    gamma_squared = 1 / (1 - velocity @ velocity)
    velocity_tangent = -velocity / (2 * gamma_squared)
    samples = []
    for offset in (2 * step, step, -step, -2 * step):
        shifted = angular.inherited.source.context(parameters['lab_energy'], parameters['lab_cosine'], velocity + offset * velocity_tangent, parameters['temperature'])
        matrices = bare_blocks(shifted, features, tests_owner, join, physical, degree)
        ratio = shifted['born_differential_over_thomson'] / parameters['born_differential_over_thomson']
        samples.append({part: ratio * matrix for part, matrix in matrices.items()})
    score = angular.inherited.normalized_mass_score(gamma_squared * (velocity @ velocity), parameters['temperature'])
    output = {}
    for part in ('equilibrium', 'mixed'):
        original, changed = projected_tangent(event, tangent, tests, test_prime, basis, basis_prime, state[part], derivative[part], degree)
        phase = .5 * (tangent['phase'] + tangent['bose']) * original
        observable = .5 * changed
        canonical = .5 * (-samples[0][part] + 8 * samples[1][part] - 8 * samples[2][part] + samples[3][part]) / (12 * step)
        population = .5 * float(score) * original
        output[part] = dict(phase=phase, observable=observable, canonical=canonical, population=population,
            total=phase + observable + canonical + population)
    return output


def freeze():
    config = protocol()
    assert read(ROOT / 'results/mass.json')['qualified']
    assert not (ROOT / 'state-configuration.json').exists()
    write(ROOT / 'state-configuration.json', dict(frozen_at=now(), script_sha256=digest(Path(__file__)),
        mass_sha256=digest(ROOT / 'results/mass-coefficients.npz'), identity_tolerance=config['identity_tolerance'],
        refinement_tolerance=config['refinement_tolerance'], steps=config['canonical_steps']))


def state_protocol():
    config = protocol()
    frozen = read(ROOT / 'state-configuration.json')
    assert digest(Path(__file__)) == frozen['script_sha256']
    assert digest(ROOT / 'results/mass-coefficients.npz') == frozen['mass_sha256']
    return config, frozen


def run(label):
    modest()
    config, frozen = state_protocol()
    target = ROOT / 'runs' / label / 'state.json'
    assert not target.exists()
    original, features, models = setup(config)
    tests_owner = models[0]['difference'].tests
    row = next(row for row in config['events'] if row['label'] == label)
    parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
    moments = packet(ROOT / 'results/mass-coefficients.npz')
    checks, records, output = [], [], {}
    began = time.monotonic()
    with mp.workdps(80):
        planck = phase_geometry(parameters)['planck_mass_squared']
        for join in config['joins']:
            mass_coefficients = moments[f'{label}:join{join}:order6:mass_coefficients']
            mass_vector = np.r_[mass_coefficients, 0.]
            for state_index, state in enumerate(config['states']):
                physical = [scalar(config['heat']) * mp.mpf(value) for value in state['coefficients']]
                mass_background = contraction(mass_coefficients, physical[:98])
                for degree in config['multipoles']:
                    values = {}
                    for step in config['canonical_steps']:
                        unit = unit_state(parameters, features, tests_owner, join, physical, degree, step)
                        first = float(planck) * unit['mixed']['total']
                        second = float(mass_background) * unit['equilibrium']['total']
                        equilibrium_source = unit['equilibrium']['total'] @ np.array(list(map(float, physical))) if degree == 0 else np.zeros(98)
                        third = np.outer(equilibrium_source, mass_vector) if degree == 0 else np.zeros_like(first)
                        combined = weight * (first + second + third)
                        values[step] = combined
                        prefix = f'join{join}:state{state_index}:l{degree}:step{step}'
                        for name, matrix in [('statistical', weight * first), ('background_mass', weight * second), ('wave_mass', weight * third), ('total', combined)]:
                            output[prefix + ':' + name] = matrix
                            if degree < 2 and np.linalg.norm(matrix) > 0:
                                scale = max(np.linalg.norm(matrix[0]) + np.linalg.norm(matrix[-1]), 1e-300)
                                check(checks, prefix + ':' + name + ':independent gas force', np.linalg.norm(matrix[0] + matrix[-1]) / scale)
                        output[prefix + ':equilibrium'] = weight * float(planck) * unit['equilibrium']['total']
                        for name in ('phase', 'observable', 'canonical', 'population'):
                            output[prefix + ':mixed_unit:' + name] = unit['mixed'][name]
                    error = relative(values[config['canonical_steps'][0]], values[config['canonical_steps'][1]])
                    check(checks, prefix + ':step refinement', error, .002)
                    records.append(dict(anchor=label, join=join, model=state['model'], history=state['history'], degree=degree,
                        canonical_step_refinement=error, mass_background=float(mass_background),
                        background_mass_over_statistical=float(np.linalg.norm(second) / max(np.linalg.norm(first), 1e-300)),
                        wave_mass_over_total=float(np.linalg.norm(third) / max(np.linalg.norm(first + second + third), 1e-300))))
            print(json.dumps(dict(anchor=label, join=join, checks=len(checks), failed=sum(not entry['passed'] for entry in checks))), flush=True)
    destination = target.with_suffix('.npz')
    save(destination, **output)
    failed = [entry for entry in checks if not entry['passed']]
    write(target, dict(state='complete', qualified=not failed, checks=checks, failed=failed, records=records,
        sha256=digest(destination), seconds=time.monotonic() - began, finished_at=now(),
        scope='Three mixed displaced-state terms; matched real-event integration remains separate'))
    print(json.dumps(dict(anchor=label, checks=len(checks), failed=failed, seconds=time.monotonic() - began)), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['freeze', 'warm', 'middle', 'cold'])
    args = parser.parse_args()
    modest()
    freeze() if args.mode == 'freeze' else run(args.mode)
