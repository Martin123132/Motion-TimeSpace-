from rectangular_common import *


class Rectangular:
    def __init__(self, spectra, density=48001, exact=False):
        self.spectra = spectra
        self.tests = TestFunctions(spectra.basis, density, exact)
        self.gas = np.repeat(spectra.gas, 2)

    def jumps(self, incoming, hard, soft, electron):
        left = self.tests.evaluate(hard) - self.tests.evaluate(incoming)
        right = self.spectra.functions(hard)[..., 1:] - self.spectra.functions(incoming)[..., 1:]
        if soft is not None:
            signed, frequency = soft
            left += signed[..., None] * self.tests.evaluate(frequency)
            right += signed[..., None] * self.spectra.functions(frequency)[..., 1:]
        left = np.concatenate([left, np.asarray(electron)[..., None]], axis=-1)
        right += np.asarray(electron)[..., None] * self.gas
        return left, right

    def born_jumps(self, parameters):
        temperature = parameters['temperature']
        incident = parameters['lab_energy'] / temperature
        outgoing = parameters['hard'] * parameters['hard_doppler'] / temperature
        recoil = np.array([0., 0., parameters['energy']]) - parameters['hard'] * parameters['hard_direction']
        recoil_energy = recoil @ recoil / (math.sqrt(1 + recoil @ recoil) + 1)
        transfer = parameters['transform'] @ np.r_[recoil_energy, recoil]
        return self.jumps(incident, outgoing, None, transfer[0] / temperature)

    def born_data(self, parameters, chemical=False):
        left, right = self.born_jumps(parameters)
        return left, np.outer(left, right)

    def born_weak(self, parameters, velocity):
        shifted = weak.source.context(parameters['lab_energy'], parameters['lab_cosine'], velocity, parameters['temperature'])
        left, product = self.born_data(shifted)
        return .5 * shifted['born_differential_over_thomson'] * product

    def state_correction(self, parameters, step=1e-3):
        left, right = self.born_jumps(parameters)
        product = np.outer(left, right)
        response = weak.source.previous.phase_response(
            weak.source.exact.mp.mpf(str(parameters['energy'])),
            weak.source.exact.mp.mpf(str(parameters['cosine'])),
            weak.source.exact.mp.mpf(str(parameters['temperature'])))
        photon_shift = parameters['transform'] @ np.array([float(value) for value in response['photon_delta']])
        electron_shift = parameters['transform'] @ np.array([float(value) for value in response['electron_delta']])
        outgoing = parameters['hard'] * parameters['hard_doppler'] / parameters['temperature']
        photon_delta = photon_shift[0] / parameters['temperature']
        electron_delta = electron_shift[0] / parameters['temperature']
        left_shift = np.r_[self.tests.derivative(outgoing) * photon_delta, electron_delta]
        right_shift = self.spectra.derivatives(outgoing)[1:] * photon_delta + self.gas * electron_delta
        shifted_product = np.outer(left_shift, right) + np.outer(left, right_shift)
        bose_delta = -(parameters['hard_bose'] - 1) * photon_delta
        phase = .5 * (float(response['phase_delta']) + bose_delta) * product
        observable = .5 * shifted_product
        velocity = parameters['velocity']
        gamma_squared = 1 / (1 - velocity @ velocity)
        tangent = -velocity / (2 * gamma_squared)
        delta_mass = float(response['mass_squared'])
        def sample(offset):
            return self.born_weak(parameters, velocity + offset * tangent)
        canonical = delta_mass * (-sample(2 * step) + 8 * sample(step) - 8 * sample(-step) + sample(-2 * step)) / (12 * step)
        canonical /= parameters['born_differential_over_thomson']
        momentum_squared = gamma_squared * (velocity @ velocity)
        score = weak.normalized_mass_score(momentum_squared, parameters['temperature'])
        population = .5 * delta_mass * score * product
        return dict(phase=phase, observable_shift=observable, canonical=canonical,
                    population=population, total=phase + observable + canonical + population)

    def event_products(self, parameters, soft, direction, chemical=False):
        energy = parameters['energy']
        intensity, photons, final, hard, denominator = weak.intensity_batch(
            energy, soft, parameters['hard_direction'], direction)
        tree_intensity = 2 * (1 + parameters['cosine']**2
                             + energy**2 * (1 - parameters['cosine'])**2 / (1 + energy * (1 - parameters['cosine'])))
        density = weak.source.ALPHA / (4 * np.pi**2) * hard * abs(soft) * intensity
        density /= energy * denominator * (parameters['hard'] / energy)**2 * tree_intensity
        doppler = weak.source.dot(parameters['bath'], np.r_[1., direction])
        soft_frequency = abs(soft) * doppler / parameters['temperature']
        hard_frequency = hard * parameters['hard_doppler'] / parameters['temperature']
        incident = parameters['lab_energy'] / parameters['temperature']
        recoil = final[:, 1:]
        recoil_energy = np.sum(recoil**2, axis=1) / (final[:, 0] + 1)
        electron = (parameters['transform'][0, 0] * recoil_energy + recoil @ parameters['transform'][0, 1:]) / parameters['temperature']
        left, right = self.jumps(incident, hard_frequency, (np.sign(soft), soft_frequency), electron)
        bose = (1 + 1 / np.expm1(hard_frequency)) / parameters['hard_bose']
        return density * bose, np.einsum('ni,nj->nij', left, right), left

    @contextmanager
    def real_context(self):
        saved_born, saved_event = weak.born_data, weak.event_products
        weak.born_data, weak.event_products = self.born_data, self.event_products
        try:
            yield
        finally:
            weak.born_data, weak.event_products = saved_born, saved_event

    def matched(self, parameters, virtual_scalar, angular=3, radial=24, floor=1e-6):
        left, product = self.born_data(parameters)
        with self.real_context():
            real = weak.real_subtracted(parameters, angular=angular, radial=radial, lower_fraction=floor)
        weak.vacuum.mp.mp.dps = 60
        vacuum = float(weak.vacuum.finite_virtual_ratio(parameters['energy'], parameters['cosine'])
                       + weak.vacuum.soft_constant(parameters['energy'], parameters['cosine']))
        virtual = .5 * (vacuum + virtual_scalar) * product
        state = self.state_correction(parameters)
        return dict(total=real['total'] + virtual + state['total'], born=.5 * product,
                    real=real['total'], virtual=virtual, state=state['total'],
                    event_energy_null=real['maximum_event_energy_null_residual'])
