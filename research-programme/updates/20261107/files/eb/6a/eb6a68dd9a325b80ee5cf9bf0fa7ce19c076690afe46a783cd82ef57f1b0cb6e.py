from rational_leading import *
from log_rectangular import logarithmic_rule


class SplitReal(Rectangular):
    def __init__(self, spectra, mode, density=48001):
        super().__init__(spectra, density)
        assert mode in ['full', 'control', 'difference']
        self.mode = mode
        self.grams = {}

    def gram(self, hard, soft):
        key = tuple(hard) + tuple(soft)
        if key not in self.grams:
            self.grams[key] = angular_gram(hard, soft)
        return self.grams[key]

    def event_products(self, parameters, soft, direction, chemical=False):
        energy = parameters['energy']
        if self.mode == 'control':
            denominator = 1 + energy * (1 - parameters['cosine']) - soft * (1 - parameters['hard_direction'] @ direction)
            hard = (energy - soft - energy * soft * (1 - direction[2])) / denominator
            recoil = np.array([0., 0., energy]) - hard[:, None] * parameters['hard_direction'] - soft[:, None] * direction
            final_energy = np.sqrt(1 + np.sum(recoil**2, axis=1))
            intensity = fast_intensity(soft / energy, self.gram(parameters['hard_direction'], direction))
        else:
            intensity, photons, final, hard, denominator = weak.intensity_batch(energy, soft, parameters['hard_direction'], direction)
            recoil, final_energy = final[:, 1:], final[:, 0]
            if self.mode == 'difference':
                intensity = intensity - fast_intensity(soft / energy, self.gram(parameters['hard_direction'], direction))
        assert np.min(hard) > 0 and np.min(denominator) > 0
        tree_intensity = 2 * (1 + parameters['cosine']**2 + energy**2 * (1 - parameters['cosine'])**2 / (1 + energy * (1 - parameters['cosine'])))
        density = weak.source.ALPHA / (4 * np.pi**2) * hard * abs(soft) * intensity
        density /= energy * denominator * (parameters['hard'] / energy)**2 * tree_intensity
        doppler = weak.source.dot(parameters['bath'], np.r_[1., direction])
        soft_frequency = abs(soft) * doppler / parameters['temperature']
        hard_frequency = hard * parameters['hard_doppler'] / parameters['temperature']
        incident = parameters['lab_energy'] / parameters['temperature']
        recoil_energy = np.sum(recoil**2, axis=1) / (final_energy + 1)
        electron = (parameters['transform'][0, 0] * recoil_energy + recoil @ parameters['transform'][0, 1:]) / parameters['temperature']
        left, right = self.jumps(incident, hard_frequency, (np.sign(soft), soft_frequency), electron)
        bose = (1 + 1 / np.expm1(hard_frequency)) / parameters['hard_bose']
        return density * bose, np.einsum('ni,nj->nij', left, right), left

    def poles(self, parameters, direction):
        energy, cosine = parameters['energy'], parameters['cosine']
        recoil = np.array([0., 0., energy]) - parameters['hard'] * parameters['hard_direction']
        exact = weak.source.ALPHA / (4 * np.pi**2) * np.linalg.norm(np.cross(recoil, direction))**2
        exact /= (math.sqrt(1 + recoil @ recoil) - recoil @ direction)**2
        reference_recoil = np.array([0., 0., 1.]) - parameters['hard_direction']
        tree_intensity = 2 * (1 + cosine**2 + energy**2 * (1 - cosine)**2 / (1 + energy * (1 - cosine)))
        control = weak.source.ALPHA / (4 * np.pi**2) * energy**2 * 2 * (1 + cosine**2) / tree_intensity
        control *= np.linalg.norm(np.cross(reference_recoil, direction))**2
        return dict(full=exact, control=control, difference=exact - control)[self.mode]

    def real(self, parameters, angular=3, radial=32, floor=1e-6, rule=logarithmic_rule):
        jump, product = self.born_data(parameters)
        spontaneous, thermal, logarithm = [np.zeros_like(product) for unused in range(3)]
        maximum_null = 0.
        for direction, angular_weight in weak.source.angular_nodes(angular):
            doppler = weak.source.dot(parameters['bath'], np.r_[1., direction])
            local_temperature = parameters['temperature'] / doppler
            emission_upper = weak.source.bath_ordered_upper(parameters, direction)
            absorption_upper = parameters['lab_energy'] / doppler
            lower = floor * local_temperature
            assert lower < min(emission_upper, absorption_upper)
            pole = self.poles(parameters, direction)
            values, weights = rule(radial, lower, emission_upper)
            density, products, jumps = self.event_products(parameters, values, direction)
            residual = density[:, None, None] * products - pole / values[:, None, None] * product
            spontaneous += .5 * angular_weight * np.einsum('n,nij->ij', weights, residual)
            maximum_null = max(maximum_null, float(np.max(abs(jumps[:, 0] + jumps[:, -1]))))
            logarithm += .5 * angular_weight * pole * math.log(2 * emission_upper) * product
            tail_upper = max(60 * local_temperature, emission_upper, absorption_upper)
            boundaries = [lower, emission_upper, absorption_upper, tail_upper]
            boundaries += [scale * local_temperature for scale in [.1, .5, 1, 2, 5, 10, 20, 40]
                           if lower < scale * local_temperature < tail_upper]
            boundaries = sorted(set(boundaries))
            for left, right in zip(boundaries[:-1], boundaries[1:]):
                values, weights = rule(radial, left, right)
                occupation = 1 / np.expm1(values / local_temperature)
                residual = -2 * pole / values[:, None, None] * product
                for sign, upper in [(1, emission_upper), (-1, absorption_upper)]:
                    if right <= upper * (1 + 1e-14):
                        density, products, jumps = self.event_products(parameters, sign * values, direction)
                        residual += density[:, None, None] * products
                        maximum_null = max(maximum_null, float(np.max(abs(jumps[:, 0] + jumps[:, -1]))))
                thermal += .5 * angular_weight * np.einsum('n,nij->ij', weights * occupation, residual)
        return dict(total=spontaneous + thermal + logarithm, spontaneous=spontaneous,
                    thermal=thermal, logarithm=logarithm, event_energy_null=maximum_null)
