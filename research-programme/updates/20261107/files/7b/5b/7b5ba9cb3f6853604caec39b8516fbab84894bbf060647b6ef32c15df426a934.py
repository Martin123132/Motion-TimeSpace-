from common232 import *


def angular_feature(direction, degree):
    direction = np.asarray(direction)
    if degree == 0:
        return np.ones(direction.shape[:-1] + (1,))
    if degree == 1:
        return direction
    if degree == 2:
        tensor = math.sqrt(1.5) * (direction[..., :, None] * direction[..., None, :] - np.eye(3) / 3)
        return tensor.reshape(direction.shape[:-1] + (9,))
    raise ValueError('Only scalar, vector and STF rank-two projection are implemented')


def angular_feature_derivative(direction, tangent, degree):
    if degree == 0:
        return np.zeros(direction.shape[:-1] + (1,))
    if degree == 1:
        return tangent
    tensor = math.sqrt(1.5) * (direction[..., :, None] * tangent[..., None, :] + tangent[..., :, None] * direction[..., None, :])
    return tensor.reshape(direction.shape[:-1] + (9,))


def photon_features(four, temperature, degree):
    four = np.asarray(four)
    frequency = four[..., 0] / temperature
    direction = four[..., 1:] / np.linalg.norm(four[..., 1:], axis=-1, keepdims=True)
    radial = inherited.functions(frequency)
    return radial[..., :, None] * angular_feature(direction, degree)[..., None, :]


def photon_tangent(four, tangent, temperature, degree):
    frequency = four[0] / temperature
    norm = np.linalg.norm(four[1:])
    direction = four[1:] / norm
    direction_tangent = (tangent[1:] - direction * np.dot(direction, tangent[1:])) / norm
    radial = inherited.functions(frequency)
    radial_tangent = inherited.derivatives(frequency) * tangent[0] / temperature
    return (radial_tangent[:, None] * angular_feature(direction, degree)[None, :]
        + radial[:, None] * angular_feature_derivative(direction, direction_tangent, degree)[None, :])


def lab_born(parameters):
    energy, hard = parameters['energy'], parameters['hard']
    incident = parameters['transform'] @ np.array([energy, 0., 0., energy])
    outgoing = parameters['transform'] @ np.r_[hard, hard * parameters['hard_direction']]
    recoil = np.array([0., 0., energy]) - hard * parameters['hard_direction']
    recoil_energy = recoil @ recoil / (math.sqrt(1 + recoil @ recoil) + 1)
    electron = parameters['transform'] @ np.r_[recoil_energy, recoil]
    return incident, outgoing, electron


class AngularWeak:
    def __init__(self, degree):
        self.degree = degree
        self.maximum_energy_residual = 0.
        self.maximum_momentum_residual = 0.

    def joint_features(self, incident, outgoing, electron, temperature, soft=None, signs=None):
        feature = photon_features(outgoing, temperature, self.degree) - photon_features(incident, temperature, self.degree)
        if soft is not None:
            feature = feature + np.asarray(signs)[..., None, None] * photon_features(soft, temperature, self.degree)
        if self.degree == 0:
            electron_feature = np.asarray(electron)[..., :1] / temperature
        elif self.degree == 1:
            electron_feature = np.asarray(electron)[..., 1:] / temperature
        else:
            electron_feature = np.zeros(feature.shape[:-2] + (feature.shape[-1],))
        return np.concatenate([feature, electron_feature[..., None, :]], axis=-2)

    def product(self, features):
        return np.einsum('...ai,...bi->...ab', features, features) / (2 * self.degree + 1)

    def born_features(self, parameters):
        incident, outgoing, electron = lab_born(parameters)
        return self.joint_features(incident, outgoing, electron, parameters['temperature'])

    def born_data(self, parameters, chemical=False):
        if chemical:
            raise ValueError('Chemical infrared domain is not supplied by these regular tests')
        incident, outgoing, electron = lab_born(parameters)
        scalar = inherited.functions(outgoing[0] / parameters['temperature']) - inherited.functions(incident[0] / parameters['temperature'])
        audit = np.r_[scalar, electron[0] / parameters['temperature']]
        return audit, self.product(self.born_features(parameters))

    def event_products(self, parameters, soft, direction, chemical=False):
        if chemical:
            raise ValueError('No zero-floor chemical extension')
        energy = parameters['energy']
        intensity, ignored_photons, final, hard, denominator = inherited.intensity_batch(energy, soft, parameters['hard_direction'], direction)
        tree = 2 * (1 + parameters['cosine']**2 + energy**2 * (1 - parameters['cosine'])**2 / (1 + energy * (1 - parameters['cosine'])))
        density = inherited.source.ALPHA / (4 * np.pi**2) * hard * abs(soft) * intensity / (energy * denominator * (parameters['hard'] / energy)**2 * tree)
        transform = parameters['transform']
        incident = transform @ np.array([energy, 0., 0., energy])
        outgoing = np.column_stack([hard, hard[:, None] * parameters['hard_direction']]) @ transform.T
        soft_four = np.column_stack([abs(soft), abs(soft)[:, None] * direction]) @ transform.T
        recoil = final[:, 1:]
        recoil_energy = np.sum(recoil**2, axis=1) / (final[:, 0] + 1)
        electron = np.column_stack([recoil_energy, recoil]) @ transform.T
        features = self.joint_features(incident, outgoing, electron, parameters['temperature'], soft_four, np.sign(soft))
        net = outgoing + np.sign(soft)[:, None] * soft_four - incident + electron
        self.maximum_energy_residual = max(self.maximum_energy_residual, float(np.max(abs(net[:, 0])) / parameters['temperature']))
        self.maximum_momentum_residual = max(self.maximum_momentum_residual, float(np.max(np.linalg.norm(net[:, 1:], axis=1)) / parameters['temperature']))
        incident_x = parameters['lab_energy'] / parameters['temperature']
        hard_x = outgoing[:, 0] / parameters['temperature']
        soft_x = soft_four[:, 0] / parameters['temperature']
        scalar = inherited.functions(hard_x) + np.sign(soft)[:, None] * inherited.functions(soft_x) - inherited.functions(incident_x)
        audit = np.column_stack([scalar, electron[:, 0] / parameters['temperature']])
        bose = (1 + 1 / np.expm1(hard_x)) / parameters['hard_bose']
        return density * bose, self.product(features), audit

    @contextmanager
    def real_context(self):
        original_born, original_events = inherited.born_data, inherited.event_products
        inherited.born_data, inherited.event_products = self.born_data, self.event_products
        try:
            yield
        finally:
            inherited.born_data, inherited.event_products = original_born, original_events

    def state_correction(self, parameters, step=1e-3):
        features = self.born_features(parameters)
        product = self.product(features)
        mp.mp.dps = 70
        response = inherited.source.previous.phase_response(mp.mpf(str(parameters['energy'])), mp.mpf(str(parameters['cosine'])), mp.mpf(str(parameters['temperature'])))
        photon_shift = parameters['transform'] @ np.array([float(value) for value in response['photon_delta']])
        electron_shift = parameters['transform'] @ np.array([float(value) for value in response['electron_delta']])
        incident, outgoing, electron = lab_born(parameters)
        shifted = np.zeros_like(features)
        shifted[:3] = photon_tangent(outgoing, photon_shift, parameters['temperature'], self.degree)
        if self.degree == 0:
            shifted[-1] = electron_shift[0] / parameters['temperature']
        elif self.degree == 1:
            shifted[-1] = electron_shift[1:] / parameters['temperature']
        derivative_product = (shifted @ features.T + features @ shifted.T) / (2 * self.degree + 1)
        bose_delta = -(parameters['hard_bose'] - 1) * photon_shift[0] / parameters['temperature']
        phase = .5 * (float(response['phase_delta']) + bose_delta) * product
        observable = .5 * derivative_product
        velocity = parameters['velocity']
        gamma_squared = 1 / (1 - velocity @ velocity)
        velocity_tangent = -velocity / (2 * gamma_squared)
        mass_shift = float(response['mass_squared'])
        def sample(offset):
            shifted_parameters = inherited.source.context(parameters['lab_energy'], parameters['lab_cosine'], velocity + offset * velocity_tangent, parameters['temperature'])
            return .5 * shifted_parameters['born_differential_over_thomson'] * self.product(self.born_features(shifted_parameters))
        canonical = mass_shift * (-sample(2 * step) + 8 * sample(step) - 8 * sample(-step) + sample(-2 * step)) / (12 * step * parameters['born_differential_over_thomson'])
        score = inherited.normalized_mass_score(gamma_squared * (velocity @ velocity), parameters['temperature'])
        population = .5 * mass_shift * score * product
        return dict(phase=phase, observable=observable, canonical=canonical, population=population,
                    shifted_features=shifted, total=phase + observable + canonical + population)

    def matched(self, parameters, virtual_scalar, angular, radial, profile=None, separator=1., floor=0.):
        audit, product = self.born_data(parameters)
        with self.real_context():
            real = inherited.real_subtracted(parameters, angular, radial, profile, separator, floor)
        inherited.vacuum.mp.mp.dps = 60
        vacuum = float(inherited.vacuum.finite_virtual_ratio(parameters['energy'], parameters['cosine']) + inherited.vacuum.soft_constant(parameters['energy'], parameters['cosine']))
        virtual = .5 * (vacuum + virtual_scalar) * product
        state = self.state_correction(parameters)
        return dict(total=real['total'] + virtual + state['total'], real=real, virtual=virtual, state=state,
                    born=.5 * product, audit=audit, event_energy=self.maximum_energy_residual,
                    event_momentum=self.maximum_momentum_residual)
