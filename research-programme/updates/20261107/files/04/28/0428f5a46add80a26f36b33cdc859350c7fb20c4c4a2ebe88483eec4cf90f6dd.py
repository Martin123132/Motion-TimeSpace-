from common236 import *
from density236 import Direction


def precise_context(parameters):
    spin = angular.inherited.source.exact
    velocity = mp.matrix([scalar(value) for value in parameters['velocity']])
    squared = mp.fsum(value**2 for value in velocity)
    gamma = 1 / mp.sqrt(1 - squared)
    def boost(sign):
        result = mp.eye(4)
        result[0, 0] = gamma
        for axis in range(3):
            result[0, axis + 1] = result[axis + 1, 0] = sign * gamma * velocity[axis]
            for other in range(3):
                result[axis + 1, other + 1] += gamma**2 * velocity[axis] * velocity[other] / (gamma + 1)
        return result
    lab_cosine, lab_energy = scalar(parameters['lab_cosine']), scalar(parameters['lab_energy'])
    incoming = boost(-1) * mp.matrix([lab_energy, 0, 0, lab_energy])
    outgoing = boost(-1) * mp.matrix([1, mp.sqrt(1 - lab_cosine**2), 0, lab_cosine])
    first_direction = mp.matrix(list(incoming)[1:]) / incoming[0]
    last_direction = mp.matrix(list(outgoing)[1:]) / outgoing[0]
    cosine = mp.fsum(left * right for left, right in zip(first_direction, last_direction))
    first = last_direction - cosine * first_direction
    first /= mp.sqrt(mp.fsum(value**2 for value in first))
    second = spin.cross(first_direction, first)
    rotation = mp.eye(4)
    for axis in range(3):
        for column, vector in enumerate((first, second, first_direction)):
            rotation[axis + 1, column + 1] = vector[axis]
    transform = boost(1) * rotation
    bath = rotation.transpose() * boost(-1) * mp.matrix([1, 0, 0, 0])
    result = dict(parameters)
    result.update(energy=incoming[0], cosine=cosine, temperature=scalar(parameters['temperature']),
        transform=np.array(transform.tolist(), dtype=object), bath=np.array(list(bath), dtype=object))
    return result


def spline_difference(spline, frequency, shifts):
    coordinate = math.log(frequency)
    differences = np.log1p(np.asarray(shifts) / frequency)
    location = min(max(int(np.searchsorted(spline.x, coordinate, side='right') - 1), 0), len(spline.x) - 2)
    displacement = coordinate - spline.x[location]
    coefficient = spline.c[:, location]
    destination = np.clip(np.searchsorted(spline.x, coordinate + differences, side='right') - 1, 0, len(spline.x) - 2)
    output = np.empty((len(differences), coefficient.shape[-1]))
    same = destination == location
    change = differences[same, None]
    output[same] = change * ((3 * coefficient[0] * displacement + 2 * coefficient[1]) * displacement + coefficient[2]
        + change * (3 * coefficient[0] * displacement + coefficient[1]) + change**2 * coefficient[0])
    for index in np.flatnonzero(~same):
        if abs(differences[index]) >= 1e-3:
            output[index] = spline(coordinate + differences[index]) - spline(coordinate)
        else:
            with mp.workdps(60):
                before = scalar(coordinate) - scalar(spline.x[location])
                after = scalar(coordinate) + scalar(differences[index]) - scalar(spline.x[destination[index]])
                for column in range(coefficient.shape[-1]):
                    first = [scalar(value) for value in coefficient[:, column]]
                    last = [scalar(value) for value in spline.c[:, destination[index], column]]
                    old = ((first[0] * before + first[1]) * before + first[2]) * before + first[3]
                    new = ((last[0] * after + last[1]) * after + last[2]) * after + last[3]
                    output[index, column] = float(new - old)
    return output


def coefficient_state(event, potential, gas):
    temperature = scalar(event['temperature'])
    transfer = list(map(scalar, event['electron_transfer']))
    initial = list(map(scalar, event['electron_initial']))
    mean = state235.mean_energy(mp.nstr(temperature, 85))
    score_initial = (initial[0] - mean) / temperature
    score_difference = -transfer[0] / temperature
    score_final = score_initial - score_difference
    occupation = [1 / mp.expm1(scalar(value)) for value in event['frequencies']]
    forward = [value + int(sign < 0) for value, sign in zip(occupation, event['signs'])]
    reverse = [value + int(sign > 0) for value, sign in zip(occupation, event['signs'])]
    signed = mp.fsum(sign * value for sign, value in zip(event['signs'], potential))
    forward_photon = mp.fsum(value * change for value, change in zip(forward, potential))
    reverse_change = score_final * gas + mp.fsum(value * change for value, change in zip(reverse, potential))
    source_change = score_difference * gas - signed
    return dict(photon=[first * source_change - sign * reverse_change + sign * (first + last) * value
        for first, last, sign, value in zip(forward, reverse, event['signs'], potential)],
        gas=score_difference * (score_initial + score_final - 2) * gas + score_difference * forward_photon - score_final * signed,
        velocity=[(before * source_change - change * (reverse_change - gas)) / temperature for before, change in zip(initial[1:], transfer[1:])],
        density=source_change)


def equilibrium(event):
    temperature = scalar(event['temperature'])
    transfer = list(map(scalar, event['electron_transfer']))
    return dict(photon=[mp.mpf(-sign) for sign in event['signs']], gas=-transfer[0] / temperature,
        velocity=[-value / temperature for value in transfer[1:]], density=mp.mpf(0))


class Factors:
    def __init__(self, owner, features, tests, states, heat):
        self.owner, self.features, self.tests = owner, features, tests
        self.physical = [[scalar(heat) * mp.mpf(value) for value in state['coefficients']] for state in states]
        self.high = np.array([[float(value) for value in values[:98]] for values in self.physical]).T
        self.low = np.array([[float(value - scalar(float(value))) for value in values[:98]] for values in self.physical]).T
        self.gas = [values[-1] for values in self.physical]
        incoming = owner.transform * owner.spin.photon(owner.energy, owner.directions[0])
        outgoing = owner.transform * owner.spin.photon(owner.hard0, owner.directions[1])
        soft_ray = owner.transform * owner.rays[2]
        initial = owner.transform * owner.initial
        transfer = owner.transform * mp.matrix([mp.fsum(value**2 for value in owner.recoil0) / (owner.final0 + 1), *owner.recoil0])
        net = owner.transform * mp.matrix([owner.hard0 - owner.energy, *(-owner.recoil0)])
        self.frequency = np.array([float(incoming[0] / owner.temperature), float(outgoing[0] / owner.temperature)])
        self.directions = np.array([list(map(float, vector[1:])) for vector in (list(incoming), list(outgoing), list(soft_ray))])
        self.directions /= np.linalg.norm(self.directions, axis=1)[:, None]
        self.event = dict(temperature=owner.temperature, frequencies=[incoming[0] / owner.temperature, outgoing[0] / owner.temperature],
            electron_initial=list(initial), electron_transfer=list(transfer), signs=[-1, 1], directions=self.directions[:2].tolist())
        self.equilibrium = equilibrium(self.event)
        self.test_base = tests.evaluate(self.frequency)
        self.basis_base = {join: features.evaluate(self.frequency, join) for join in (0, 1)}
        self.background = {join: [[state235.contraction(line, physical[:98]) for line in self.basis_base[join]] for physical in self.physical] for join in (0, 1)}
        self.coefficients = {join: [self.equilibrium] + [coefficient_state(self.event, potential, gas) for potential, gas in zip(self.background[join], self.gas)] for join in (0, 1)}
        self.left = {}
        self.right = {}
        self.harmonics = {}
        for degree in (0, 1, 2):
            harmonic = angular.angular_feature(self.directions, degree)
            self.harmonics[degree] = harmonic
            photon = np.einsum('n,na,ni->ai', [-1, 1], self.test_base, harmonic[:2])
            if degree < 2:
                photon[0] = list(map(float, mp.matrix(list(net)[:1] if degree == 0 else list(net)[1:]) / owner.temperature))
                if degree == 0:
                    photon[1] = 0.
                    photon[2] = photon[0] / tests.basis.norms[1]
            gas_left = np.array(list(map(float, transfer))) / float(owner.temperature)
            gas_left = gas_left[:1] if degree == 0 else gas_left[1:] if degree == 1 else np.zeros(9)
            self.left[degree] = np.vstack([photon, gas_left])
            for join in (0, 1):
                self.right[join, degree] = [self.project_right(coefficients, self.basis_base[join], harmonic, degree) for coefficients in self.coefficients[join]]

    @staticmethod
    def project_right(coefficients, basis, harmonic, degree):
        photon = np.einsum('n,na,ni->ai', np.array(list(map(float, coefficients['photon']))), basis, harmonic[:len(basis)])
        gas = np.array([float(coefficients['gas'])]) if degree == 0 else np.array(list(map(float, coefficients['velocity']))) if degree == 1 else np.zeros(9)
        return np.vstack([photon, gas])

    def evaluate(self, soft_values, event_values, sign):
        owner = self.owner
        frequencies = np.array([float(abs(scalar(value)) * owner.doppler / owner.temperature) for value in soft_values])
        shifts = np.array([float(event['hard_shift'] * owner.hard_doppler / owner.temperature) for event in event_values])
        test_delta = np.column_stack([shifts, spline_difference(self.tests.spline, self.frequency[1], shifts)])
        test_delta[:, 1] = 0.
        test_delta[:, 2] = shifts / self.tests.basis.norms[1]
        test_soft = self.tests.evaluate(frequencies)
        feature_soft = {join: self.features.evaluate(frequencies, join) for join in (0, 1)}
        feature_delta = {join: spline_difference(self.features.splines[join], self.frequency[1], shifts) for join in (0, 1)}
        potential_soft = {join: precise.stable_dot(feature_soft[join], self.high, self.low) for join in (0, 1)}
        potential_delta = {join: precise.stable_dot(feature_delta[join], self.high, self.low) for join in (0, 1)}
        output = {}
        coefficients = {join: [] for join in (0, 1)}
        recoil_delta, photon_delta, transfers = [], [], []
        for node_index, event in enumerate(event_values):
            transfer = owner.transform * mp.matrix([event['kinetic'], *event['recoil']])
            transfer_delta = owner.transform * mp.matrix([event['kinetic_shift'], *event['recoil_shift']])
            photon_shift = owner.transform * mp.matrix([event['hard_shift'] + event['soft'], *(-event['recoil_shift'])])
            recoil_delta.append(list(map(float, transfer_delta / owner.temperature)))
            photon_delta.append(list(map(float, photon_shift / owner.temperature)))
            transfers.append(transfer)
            current = dict(self.event, frequencies=[self.event['frequencies'][0], self.event['frequencies'][1] + scalar(shifts[node_index]), scalar(frequencies[node_index])],
                electron_transfer=list(transfer), signs=[-1, 1, sign])
            for join in (0, 1):
                values = [equilibrium(current)]
                for state_index in range(6):
                    potential = [self.background[join][state_index][0], self.background[join][state_index][1] + scalar(potential_delta[join][node_index, state_index]),
                        scalar(potential_soft[join][node_index, state_index])]
                    values.append(coefficient_state(current, potential, self.gas[state_index]))
                coefficients[join].append(values)
        recoil_delta = np.array(recoil_delta)
        photon_delta = np.array(photon_delta)
        for degree in (0, 1, 2):
            harmonic = self.harmonics[degree]
            delta_left = test_delta[:, :, None] * harmonic[1] + sign * test_soft[:, :, None] * harmonic[2]
            if degree < 2:
                delta_left[:, 0] = photon_delta[:, :1] if degree == 0 else photon_delta[:, 1:]
                if degree == 0:
                    delta_left[:, 1] = sign / self.tests.basis.norms[0]
                    delta_left[:, 2] = (photon_delta[:, :1] - self.tests.basis.mean * sign) / self.tests.basis.norms[1]
            gas_delta = recoil_delta[:, :1] if degree == 0 else recoil_delta[:, 1:] if degree == 1 else np.zeros((len(shifts), 9))
            output[degree, 'left_delta'] = np.concatenate([delta_left, gas_delta[:, None, :]], axis=1)
            for join in (0, 1):
                right_delta = np.zeros((len(shifts), 7, 99, harmonic.shape[-1]))
                reference = np.zeros_like(right_delta)
                for node_index, frequency in enumerate(frequencies):
                    occupation = 1 / mp.expm1(scalar(frequency))
                    coupling = 2 * occupation * (1 + occupation) / (1 + 2 * occupation)
                    soft_wave = np.vstack([feature_soft[join][node_index, :, None] * harmonic[2], np.zeros((1, harmonic.shape[-1]))])
                    for state_index in range(7):
                        actual = coefficients[join][node_index][state_index]
                        born = self.coefficients[join][state_index]
                        soft_background = mp.mpf(0) if state_index == 0 else scalar(potential_soft[join][node_index, state_index - 1])
                        background_source = mp.mpf(0) if state_index == 0 else born['density']
                        extra = float(coupling * soft_background) * self.right[join, degree][0] + float(coupling * background_source) * soft_wave
                        reference[node_index, state_index] = self.right[join, degree][state_index] + extra
                        difference = [actual['photon'][index] - born['photon'][index] - coupling * soft_background * self.equilibrium['photon'][index] for index in (0, 1)]
                        difference_soft = actual['photon'][2] - coupling * background_source
                        photon = np.einsum('n,na,ni->ai', list(map(float, difference)), self.basis_base[join], harmonic[:2])
                        photon += float(actual['photon'][1]) * feature_delta[join][node_index, :, None] * harmonic[1]
                        photon += float(difference_soft) * feature_soft[join][node_index, :, None] * harmonic[2]
                        gas = [actual['gas'] - born['gas'] - coupling * soft_background * self.equilibrium['gas']] if degree == 0 else [value - old - coupling * soft_background * normal
                            for value, old, normal in zip(actual['velocity'], born['velocity'], self.equilibrium['velocity'])] if degree == 1 else [0.] * 9
                        right_delta[node_index, state_index] = np.vstack([photon, list(map(float, gas))])
                output[join, degree, 'right_delta'] = right_delta
                output[join, degree, 'reference'] = reference
        return output
