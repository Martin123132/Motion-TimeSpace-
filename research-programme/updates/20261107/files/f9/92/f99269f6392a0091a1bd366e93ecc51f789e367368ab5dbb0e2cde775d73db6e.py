from vacuum_virtual import *


def geometry(energy, hard_cosine, soft_cosine, azimuth):
    energy, hard_cosine, soft_cosine, azimuth = [mp.mpf(value) for value in [energy, hard_cosine, soft_cosine, azimuth]]
    pair_cosine = hard_cosine*soft_cosine + mp.sqrt((1-hard_cosine**2)*(1-soft_cosine**2))*mp.cos(azimuth)
    return energy, 1-hard_cosine, 1-soft_cosine, 1-pair_cosine


def ordered_upper(energy, angle01, angle02, angle12):
    middle = 2+energy*(angle01+angle02)
    return 2*energy/(middle+mp.sqrt(middle**2-4*angle12*energy))


def amplitude_squared(energy, emitted, angle01, angle02, angle12):
    denominator = 1+energy*angle01-emitted*angle12
    companion = (energy-emitted-energy*emitted*angle02)/denominator
    incoming = [-energy, companion, emitted]
    outgoing = [energy*(1-companion*angle01-emitted*angle02),
                -companion*denominator, -emitted*(1+energy*angle02-companion*angle12)]
    inverse_sum = sum(1/value for value in incoming)
    reverse_sum = sum(1/value for value in outgoing)
    inverse_pairs = sum(1/(left*right) for left,right in zip(incoming,outgoing))
    energy_sum = sum(incoming)
    pair_sum = sum(left*right for left,right in zip(incoming,outgoing))
    product, reverse_product = mp.fprod(incoming), mp.fprod(outgoing)
    ratios = sum(left/right+right/left for left,right in zip(incoming,outgoing))
    difference = inverse_sum*reverse_sum-inverse_pairs
    squared = 2*difference*((inverse_sum+reverse_sum)*(2+energy_sum)-difference-8)
    squared -= 2*energy_sum*(inverse_sum**2+reverse_sum**2)
    squared -= 2*(inverse_sum*reverse_sum+inverse_pairs*(1-energy_sum))*ratios+8*inverse_pairs
    bracket = (product+reverse_product)*(1+energy_sum)+energy_sum**2*(1-pair_sum)+2*pair_sum
    bracket -= (inverse_sum*product+reverse_sum*reverse_product)*(2+(1-energy_sum)*pair_sum/energy_sum)
    squared += 4*energy_sum/(product*reverse_product)*bracket
    if not (squared >= 0 and companion > 0):
        raise ValueError('Unphysical double-Compton point')
    return squared, companion, denominator


def real_density(energy, emitted, angle01, angle02, angle12):
    squared, companion, denominator = amplitude_squared(energy,emitted,angle01,angle02,angle12)
    ratio = 1/(1+energy*angle01)
    born = compton(-energy,energy*ratio)
    return mp.mpf(str(ALPHA))/(8*mp.pi**2)*squared*companion*emitted/(energy*denominator*ratio**2*born)


def pole_density(energy, angle01, angle02, angle12):
    hard = energy/(1+energy*angle01)
    gamma = 1+energy-hard
    dot_soft = 1+energy*angle02-hard*angle12
    current_square = 2*gamma/dot_soft-1-1/dot_soft**2
    return mp.mpf(str(ALPHA))/(4*mp.pi**2)*current_square


def angular_nodes(order):
    cosines, weights = np.polynomial.legendre.leggauss(order)
    for cosine, weight in zip(cosines,weights):
        for index in range(2*order):
            yield mp.mpf(float(cosine)), 2*mp.pi*(mp.mpf(index)+mp.mpf('.5'))/(2*order), mp.mpf(float(weight))*2*mp.pi/(2*order)


def integrate_ordered(energy, hard_cosine, angular_order, radial_order, lower=0):
    energy, hard_cosine, lower = mp.mpf(str(energy)),mp.mpf(str(hard_cosine)),mp.mpf(str(lower))
    nodes,weights = np.polynomial.legendre.leggauss(radial_order)
    radial = [(mp.mpf(float(node))+1)/2 for node in nodes]
    radial_weights = [mp.mpf(float(weight))/2 for weight in weights]
    finite, angular_log, integrated_pole, raw_above = mp.mpf(0),mp.mpf(0),mp.mpf(0),mp.mpf(0)
    for soft_cosine,azimuth,angular_weight in angular_nodes(angular_order):
        values = geometry(energy,hard_cosine,soft_cosine,azimuth)
        upper = ordered_upper(*values)
        assert upper>lower
        pole = pole_density(*values)
        remainder = mp.mpf(0)
        for unit,weight in zip(radial,radial_weights):
            emitted = lower+(upper-lower)*unit
            remainder += weight*(upper-lower)*(real_density(energy,emitted,*values[1:])-pole/emitted)
        finite += angular_weight*remainder
        angular_log += angular_weight*pole*mp.log(2*upper)
        integrated_pole += angular_weight*pole
        if lower>0:
            raw_above += angular_weight*(remainder+pole*mp.log(upper/lower))
    ratio = finite_virtual_ratio(energy,hard_cosine)+soft_constant(energy,hard_cosine)+finite+angular_log
    return dict(energy=float(energy),cosine=float(hard_cosine),angular_order=angular_order,radial_order=radial_order,
        lower=float(lower),finite_real_remainder=float(finite),upper_log_term=float(angular_log),
        integrated_pole=float(integrated_pole),analytic_pole=float(cusp(energy,hard_cosine)),
        finite_virtual=float(finite_virtual_ratio(energy,hard_cosine)),soft_regulator_constant=float(soft_constant(energy,hard_cosine)),
        matched_ratio=float(ratio),resolved_real_above=float(raw_above))
