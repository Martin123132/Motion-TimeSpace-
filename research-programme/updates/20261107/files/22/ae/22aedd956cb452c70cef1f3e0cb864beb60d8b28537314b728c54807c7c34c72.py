from weak_common import *


def functions(frequency, chemical=False):
    frequency = np.asarray(frequency)
    columns = [frequency, frequency**2 / (1 + frequency),
               frequency**3 / (1 + frequency)**2]
    if chemical:
        columns.insert(0, np.ones_like(frequency))
    return np.stack(columns, axis=-1)


def derivatives(frequency, chemical=False):
    columns = [1., frequency * (2 + frequency) / (1 + frequency)**2,
               frequency**2 * (3 + frequency) / (1 + frequency)**3]
    if chemical:
        columns.insert(0, 0.)
    return np.array(columns)


def born_data(parameters, chemical=False):
    temperature = parameters['temperature']
    incident = parameters['lab_energy'] / temperature
    outgoing = parameters['hard'] * parameters['hard_doppler'] / temperature
    recoil = np.array([0., 0., parameters['energy']]) - parameters['hard'] * parameters['hard_direction']
    recoil_energy = recoil @ recoil / (math.sqrt(1 + recoil @ recoil) + 1)
    transfer = parameters['transform'] @ np.r_[recoil_energy, recoil]
    jump = np.r_[functions(outgoing, chemical) - functions(incident, chemical),
                 transfer[0] / temperature]
    return jump, np.outer(jump, jump)


def born_weak(lab_energy, cosine, velocity, temperature, chemical=False, mass=1.):
    parameters = source.context(lab_energy / mass, cosine, velocity, temperature / mass)
    jump, product = born_data(parameters, chemical)
    return .5 * parameters['born_differential_over_thomson'] / mass**2 * product


def state_correction(parameters, chemical=False, step=1e-3):
    jump, product = born_data(parameters, chemical)
    response = source.previous.phase_response(
        source.exact.mp.mpf(str(parameters['energy'])),
        source.exact.mp.mpf(str(parameters['cosine'])),
        source.exact.mp.mpf(str(parameters['temperature'])))
    photon_shift = parameters['transform'] @ np.array([float(value) for value in response['photon_delta']])
    electron_shift = parameters['transform'] @ np.array([float(value) for value in response['electron_delta']])
    outgoing = parameters['hard'] * parameters['hard_doppler'] / parameters['temperature']
    shifted_jump = np.r_[derivatives(outgoing, chemical) * photon_shift[0] / parameters['temperature'],
                         electron_shift[0] / parameters['temperature']]
    shifted_product = np.outer(shifted_jump, jump) + np.outer(jump, shifted_jump)
    bose_delta = -(parameters['hard_bose'] - 1) * photon_shift[0] / parameters['temperature']
    phase = .5 * (float(response['phase_delta']) + bose_delta) * product
    observable = .5 * shifted_product
    velocity = parameters['velocity']
    gamma_squared = 1 / (1 - velocity @ velocity)
    tangent = -velocity / (2 * gamma_squared)
    delta_mass = float(response['mass_squared'])
    def sample(offset):
        return born_weak(parameters['lab_energy'], parameters['lab_cosine'],
                         velocity + offset * tangent, parameters['temperature'], chemical)
    canonical = delta_mass * (-sample(2 * step) + 8 * sample(step) - 8 * sample(-step) + sample(-2 * step)) / (12 * step)
    canonical /= parameters['born_differential_over_thomson']
    momentum_squared = gamma_squared * (velocity @ velocity)
    score = normalized_mass_score(momentum_squared, parameters['temperature'])
    population = .5 * delta_mass * score * product
    return dict(phase=phase, observable_shift=observable, canonical=canonical,
                population=population, mass_shift=delta_mass, population_score=float(score),
                shifted_jump=shifted_jump, total=phase + observable + canonical + population)


def event_products(parameters, soft, direction, chemical=False):
    energy = parameters['energy']
    intensity, photons, final, hard, denominator = intensity_batch(
        energy, soft, parameters['hard_direction'], direction)
    tree_intensity = 2 * (1 + parameters['cosine']**2
                         + energy**2 * (1 - parameters['cosine'])**2 / (1 + energy * (1 - parameters['cosine'])))
    density = source.ALPHA / (4 * np.pi**2) * hard * abs(soft) * intensity
    density /= energy * denominator * (parameters['hard'] / energy)**2 * tree_intensity
    soft_doppler = source.dot(parameters['bath'], np.r_[1., direction])
    soft_frequency = abs(soft) * soft_doppler / parameters['temperature']
    hard_frequency = hard * parameters['hard_doppler'] / parameters['temperature']
    incoming_frequency = parameters['lab_energy'] / parameters['temperature']
    jump_photon = (functions(hard_frequency, chemical)
                   + np.sign(soft)[:, None] * functions(soft_frequency, chemical)
                   - functions(incoming_frequency, chemical))
    recoil = final[:, 1:]
    recoil_energy = np.sum(recoil**2, axis=1) / (final[:, 0] + 1)
    electron_energy = (parameters['transform'][0, 0] * recoil_energy
                       + recoil @ parameters['transform'][0, 1:]) / parameters['temperature']
    jumps = np.column_stack([jump_photon, electron_energy])
    bose = (1 + 1 / np.expm1(hard_frequency)) / parameters['hard_bose']
    products = np.einsum('ni,nj->nij', jumps, jumps)
    return density * bose, products, jumps


def quadrature(order, lower, upper):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    return (lower + upper) / 2 + (upper - lower) * nodes / 2, (upper - lower) * weights / 2


def thermal_conversion(profile):
    if profile is None:
        return 0.
    def integrand(value):
        if value == 0:
            return 1 / profile**2
        return -math.expm1(-(value / profile)**2) / (math.expm1(value) * value)
    boundaries = sorted({0., min(profile, 60.), 1., 5., 20., 60.})
    return -sum(integrate.quad(integrand, lower, upper, epsabs=1e-12, epsrel=1e-12)[0]
                for lower, upper in zip(boundaries[:-1], boundaries[1:]))


def real_subtracted(parameters, angular=6, radial=40, profile=None, separator_fraction=1.,
                    lower_fraction=0., chemical=False):
    if chemical and lower_fraction <= 0:
        raise ValueError('The physical chemical mode requires a positive unresolved-IR boundary')
    if not 0 < separator_fraction <= 1:
        raise ValueError('Separator fraction must lie in (0,1]')
    jump, product = born_data(parameters, chemical)
    spontaneous, thermal, logarithm, conversion = [np.zeros_like(product) for index in range(4)]
    recoil = np.array([0., 0., parameters['energy']]) - parameters['hard'] * parameters['hard_direction']
    final_energy = math.sqrt(1 + recoil @ recoil)
    conversion_integral = thermal_conversion(profile)
    pole_total = 0.
    null_residual = 0.
    energy_index = 1 if chemical else 0
    for direction, angular_weight in source.angular_nodes(angular):
        doppler = source.dot(parameters['bath'], np.r_[1., direction])
        local_temperature = parameters['temperature'] / doppler
        emission_upper = source.bath_ordered_upper(parameters, direction)
        absorption_upper = parameters['lab_energy'] / doppler
        lower = lower_fraction * local_temperature
        separator = emission_upper * separator_fraction
        if lower >= min(separator, absorption_upper):
            raise ValueError('Soft floor is above an ordering or matching boundary')
        pole = source.ALPHA / (4 * np.pi**2) * np.linalg.norm(np.cross(recoil, direction))**2
        pole /= (final_energy - recoil @ direction)**2
        pole_total += angular_weight * pole
        boundaries = sorted({lower, separator, emission_upper})
        for left, right in zip(boundaries[:-1], boundaries[1:]):
            values, weights = quadrature(radial, left, right)
            density, products, jumps = event_products(parameters, values, direction, chemical)
            residual = density[:, None, None] * products
            if right <= separator * (1 + 1e-14):
                residual -= pole / values[:, None, None] * product
            spontaneous += .5 * angular_weight * np.einsum('n,nij->ij', weights, residual)
            null_residual = max(null_residual, float(np.max(abs(jumps[:, energy_index] + jumps[:, -1]))))
        logarithm += .5 * angular_weight * pole * math.log(2 * separator) * product
        tail_upper = max(60 * local_temperature, emission_upper, absorption_upper)
        boundaries = [lower, emission_upper, absorption_upper, tail_upper]
        boundaries += [scale * local_temperature for scale in [.1, .5, 1, 2, 5, 10, 20, 40]
                       if lower < scale * local_temperature < tail_upper]
        if profile is not None and lower < profile * local_temperature < tail_upper:
            boundaries.append(profile * local_temperature)
        boundaries = sorted(set(boundaries))
        for left, right in zip(boundaries[:-1], boundaries[1:]):
            values, weights = quadrature(radial, left, right)
            scaled = values / local_temperature
            occupation = 1 / np.expm1(scaled)
            matching = np.ones_like(values) if profile is None else np.exp(-(scaled / profile)**2)
            residual = -2 * pole * (matching / values)[:, None, None] * product
            for sign, upper in [(1, emission_upper), (-1, absorption_upper)]:
                if right <= upper * (1 + 1e-14):
                    density, products, jumps = event_products(parameters, sign * values, direction, chemical)
                    residual += density[:, None, None] * products
                    null_residual = max(null_residual, float(np.max(abs(jumps[:, energy_index] + jumps[:, -1]))))
            thermal += .5 * angular_weight * np.einsum('n,nij->ij', weights * occupation, residual)
        conversion += angular_weight * pole * conversion_integral * product
    return dict(spontaneous=spontaneous, thermal=thermal, logarithm=logarithm,
                profile_conversion=conversion, integrated_pole=pole_total,
                maximum_event_energy_null_residual=null_residual,
                total=spontaneous + thermal + logarithm + conversion)


def matched(parameters, virtual_scalar, angular=6, radial=40, profile=None,
            separator_fraction=1., lower_fraction=0., chemical=False):
    jump, product = born_data(parameters, chemical)
    real = real_subtracted(parameters, angular, radial, profile, separator_fraction,
                           lower_fraction, chemical)
    vacuum.mp.mp.dps = 60
    vacuum_value = float(vacuum.finite_virtual_ratio(parameters['energy'], parameters['cosine'])
                         + vacuum.soft_constant(parameters['energy'], parameters['cosine']))
    elastic_virtual = .5 * (vacuum_value + virtual_scalar) * product
    displaced = state_correction(parameters, chemical)
    return dict(total=real['total'] + elastic_virtual + displaced['total'],
                real=real, virtual=elastic_virtual, state=displaced,
                born=.5 * product, jump=jump, vacuum_ratio=vacuum_value,
                thermal_virtual_ratio=virtual_scalar)
