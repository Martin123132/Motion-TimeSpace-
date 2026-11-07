import numpy as numerical

from annular_action_boundary_current_20260909 import changed_system
from annular_adm_mixed_action_20260909 import linear_value_gradient, hermite_matrices
from annular_gram_joint_action_20260909 import gram_matrices


class SecondJet:
    __array_priority__ = 1000

    def __init__(self, value, first=0.0, second=0.0):
        self.value = numerical.asarray(value)
        self.first = numerical.broadcast_to(first, self.value.shape).copy()
        self.second = numerical.broadcast_to(second, self.value.shape).copy()

    def __add__(self, other):
        other = other if isinstance(other, SecondJet) else SecondJet(other)
        return SecondJet(self.value + other.value, self.first + other.first, self.second + other.second)

    __radd__ = __add__

    def __neg__(self):
        return SecondJet(-self.value, -self.first, -self.second)

    def __sub__(self, other):
        return self + (-other if isinstance(other, SecondJet) else -numerical.asarray(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = other if isinstance(other, SecondJet) else SecondJet(other)
        return SecondJet(self.value * other.value, self.first * other.value + self.value * other.first, self.second * other.value + 2 * self.first * other.first + self.value * other.second)

    __rmul__ = __mul__

    def __pow__(self, power):
        return SecondJet(self.value**power, power * self.value**(power - 1) * self.first, power * self.value**(power - 1) * self.second + power * (power - 1) * self.value**(power - 2) * self.first**2)

    def __truediv__(self, other):
        return self * (other**-1 if isinstance(other, SecondJet) else 1 / numerical.asarray(other))

    def __rtruediv__(self, other):
        return self**-1 * other

    def mapped(self, matrix):
        return SecondJet(matrix @ self.value, matrix @ self.first, matrix @ self.second)

    def selected(self, selection):
        return SecondJet(self.value[selection], self.first[selection], self.second[selection])


def canonical_constraint_jet(system, packed, configuration, momenta, clock, include_gram):
    if any(system.constants[name] != 0 for name in ['Lambda', 'm_chi', 'b2', 'b3']):
        raise ValueError('Only the canonical zero-mass, zero-Lambda branch is derived.')
    basis, radius, kappa = system.basis, system.basis.quadrature, system.kappa
    mass, lapse, velocity = [packed.selected(selection) for selection in system.slices]
    slope_velocity = packed.selected(system.slope_slice)
    reconstruction = numerical.concatenate([basis.scalar_value, basis.lift_value / basis.spacing], axis=1)
    gradient = numerical.concatenate([basis.scalar_gradient, basis.lift_gradient / basis.spacing], axis=1)
    mass_q, mass_r = mass.mapped(basis.face_value), mass.mapped(basis.face_gradient)
    lapse_q = lapse.mapped(basis.node_value)
    velocity_q = velocity.mapped(basis.scalar_value) + slope_velocity.mapped(basis.lift_value / basis.spacing)
    scalar_gradient = configuration.mapped(gradient)
    spatial_f = 1 - 2 * mass_q / radius
    weights = basis.quadrature_weights
    mass_density = lapse_q * mass_r / (kappa * radius) * spatial_f**-1.5 + radius * velocity_q**2 / (2 * lapse_q) * spatial_f**-1.5 + radius * lapse_q * scalar_gradient**2 / 2 * spatial_f**-.5
    lapse_density = mass_r / kappa * spatial_f**-.5 - radius**2 * velocity_q**2 / (2 * lapse_q**2) * spatial_f**-.5 - radius**2 * scalar_gradient**2 / 2 * spatial_f**.5
    momentum_density = radius**2 * velocity_q / lapse_q * spatial_f**-.5
    mass_row = (mass_density * weights).mapped(basis.face_value.T) + (lapse_q / kappa * spatial_f**-.5 * weights).mapped(basis.face_gradient.T)
    lapse_row = (lapse_density * weights).mapped(basis.node_value.T)
    velocity_row = (momentum_density * weights).mapped(reconstruction.T) - momenta
    if include_gram:
        factors, sampling = gram_matrices(system.node_count)
        scalar = configuration.selected(slice(0, system.node_count))
        density = (scalar.mapped(factors)**2).mapped(sampling.T) / (2 * basis.spacing)
        node_f = 1 - 2 * mass.mapped(basis.face_to_node) / basis.radii
        mass_row += (density * basis.radii * lapse * node_f**-.5).mapped(basis.face_to_node.T)
        lapse_row -= density * basis.radii**2 * node_f**.5
    boundary = numerical.zeros(system.face_count)
    boundary[-1] = 1 / kappa
    mass_row -= clock * boundary
    return SecondJet(numerical.concatenate([mass_row.value, lapse_row.value, velocity_row.value]), numerical.concatenate([mass_row.first, lapse_row.first, velocity_row.first]), numerical.concatenate([mass_row.second, lapse_row.second, velocity_row.second]))


def exact_local_acceleration(system, packed, tangent, clock_rate, include_gram):
    speed = tangent['packed_speed']
    step = 1e-25
    moved = changed_system(system, packed, tangent, 1j * step, clock_rate)
    moved_packed = packed + 1j * step * speed
    force_time = moved.scalar_force(moved_packed, include_gram).imag / step
    force_time[[0, -1]] = 0
    slope_force_time = moved.slope_force(moved_packed, include_gram).imag / step
    shift_speed_time = moved.shift_mass_velocity(moved_packed, include_gram)[0].imag / step
    configuration = SecondJet(numerical.concatenate([system.scalar, system.slope]), numerical.concatenate([packed[system.slices[2]], packed[system.slope_slice]]), numerical.concatenate([speed[system.slices[2]], speed[system.slope_slice]]))
    momenta = SecondJet(numerical.concatenate([system.momentum, system.slope_momentum]), numerical.concatenate([tangent['momentum_speed'], tangent['slope_momentum_speed']]), numerical.concatenate([force_time, slope_force_time]))
    clock = SecondJet(system.outer_clock, clock_rate)
    known = canonical_constraint_jet(system, SecondJet(packed, speed), configuration, momenta, clock, include_gram)
    jacobian = system.evaluate(packed, include_gram)[2]
    acceleration = numerical.zeros_like(packed)
    acceleration[system.fixed] = [shift_speed_time[0], 0.0, 0.0]
    acceleration[system.free] = numerical.linalg.solve(jacobian[numerical.ix_(system.free, system.free)], -(known.second + jacobian @ acceleration)[system.free])
    completed = canonical_constraint_jet(system, SecondJet(packed, speed, acceleration), configuration, momenta, clock, include_gram)
    return {'acceleration': acceleration, 'shift_speed_time': shift_speed_time, 'physical_mismatch_time': acceleration[system.slices[0]] - shift_speed_time, 'gradient': completed.value, 'first_constraint_rate': completed.first, 'second_constraint_rate': completed.second, 'known_second_forcing': known.second, 'momentum_second_rate': momenta.second}


def second_spatial_matrix(basis, points):
    count = basis.radii.size
    left = numerical.clip(numerical.searchsorted(basis.radii, points, side='right') - 1, 0, count - 2)
    fraction = (points - basis.radii[left]) / basis.spacing
    rows = numerical.arange(points.size)
    value, slope = numerical.zeros((points.size, count)), numerical.zeros((points.size, count))
    value[rows, left] = (12 * fraction - 6) / basis.spacing**2
    value[rows, left + 1] = (-12 * fraction + 6) / basis.spacing**2
    slope[rows, left] = (6 * fraction - 4) / basis.spacing
    slope[rows, left + 1] = (6 * fraction - 2) / basis.spacing
    return numerical.concatenate([value + slope @ basis.derivative, slope / basis.spacing], axis=1)


def flux_profile(system, packed, speed, points):
    basis = system.basis
    mass_map, mass_gradient = linear_value_gradient(basis.faces, points)
    lapse_map, lapse_gradient = linear_value_gradient(basis.radii, points)
    values, gradients, slopes, slope_gradients = hermite_matrices(basis.radii, points, basis.derivative)
    reconstruction = numerical.concatenate([values, slopes / basis.spacing], axis=1)
    radial = numerical.concatenate([gradients, slope_gradients / basis.spacing], axis=1)
    configuration = numerical.concatenate([system.scalar, system.slope])
    velocity = numerical.concatenate([packed[system.slices[2]], packed[system.slope_slice]])
    velocity_rate = numerical.concatenate([speed[system.slices[2]], speed[system.slope_slice]])
    mass, mass_r = mass_map @ packed[system.slices[0]], mass_gradient @ packed[system.slices[0]]
    mass_t, mass_tr = mass_map @ speed[system.slices[0]], mass_gradient @ speed[system.slices[0]]
    lapse, lapse_r = lapse_map @ packed[system.slices[1]], lapse_gradient @ packed[system.slices[1]]
    lapse_t, lapse_tr = lapse_map @ speed[system.slices[1]], lapse_gradient @ speed[system.slices[1]]
    spatial_f = 1 - 2 * mass / points
    f_r = -2 * mass_r / points + 2 * mass / points**2
    f_t = -2 * mass_t / points
    f_tr = -2 * mass_tr / points + 2 * mass_t / points**2
    characteristic = lapse * numerical.sqrt(spatial_f)
    characteristic_log_r = lapse_r / lapse + f_r / (2 * spatial_f)
    theta = lapse_t / lapse + f_t / (2 * spatial_f)
    lapse_ratio_r = lapse_tr / lapse - lapse_t * lapse_r / lapse**2
    f_ratio_r = f_tr / spatial_f - f_t * f_r / spatial_f**2
    theta_r = lapse_ratio_r + f_ratio_r / 2
    clock_log_r = lapse_r / lapse - f_r / (2 * spatial_f)
    clock_log_tr = lapse_ratio_r - f_ratio_r / 2
    velocity_q, velocity_r = reconstruction @ velocity, radial @ velocity
    scalar_r, scalar_rr = radial @ configuration, second_spatial_matrix(basis, points) @ configuration
    normalized_velocity = velocity_q / characteristic
    normalized_r = (velocity_r - characteristic_log_r * velocity_q) / characteristic
    normalized_t = (reconstruction @ velocity_rate - theta * velocity_q) / characteristic
    scalar_rt = velocity_r
    density = normalized_velocity**2 + scalar_r**2
    density_t = 2 * normalized_velocity * normalized_t + 2 * scalar_r * scalar_rt
    hamiltonian_defect = mass_r - system.kappa * points**2 * spatial_f * density / 2
    lapse_defect = clock_log_r - system.kappa * points * density
    lapse_defect_time = clock_log_tr - system.kappa * points * density_t
    scalar_defect = normalized_t - characteristic * (scalar_rr + (characteristic_log_r + 2 / points) * scalar_r)
    kinematic_defect = scalar_rt - characteristic * (normalized_r + characteristic_log_r * normalized_velocity)
    bulk_flux = system.kappa * points**2 * spatial_f * velocity_q * scalar_r
    bulk_flux_r = system.kappa * ((2 * points * spatial_f + points**2 * f_r) * velocity_q * scalar_r + points**2 * spatial_f * (velocity_r * scalar_r + velocity_q * scalar_rr))
    denominator = points * spatial_f
    denominator_r = 1 - 2 * mass_r
    strong_mismatch = mass_t - bulk_flux
    strong_mismatch_r = mass_tr - bulk_flux_r
    corrected_mismatch_r = strong_mismatch_r / denominator - strong_mismatch * denominator_r / denominator**2
    leading = 2 * bulk_flux / denominator**2
    delta_h = -4 * bulk_flux * hamiltonian_defect / denominator**2
    delta_lapse = 2 * bulk_flux * lapse_defect / denominator
    delta_wave = 2 * system.kappa * points * (normalized_velocity * scalar_defect + scalar_r * kinematic_defect)
    remainder = delta_h + delta_lapse + lapse_defect_time + delta_wave
    predicted = leading - 2 * corrected_mismatch_r + remainder
    return {'radius': points, 'theta': theta, 'theta_r': theta_r, 'theta_r_predicted': predicted, 'leading_flux_term': leading, 'strong_mismatch': strong_mismatch, 'strong_mismatch_r': strong_mismatch_r, 'mismatch_derivative_term': -2 * corrected_mismatch_r, 'remainder': remainder, 'remainder_H': delta_h, 'remainder_lapse': delta_lapse, 'remainder_lapse_time': lapse_defect_time, 'remainder_wave': delta_wave, 'hamiltonian_defect': hamiltonian_defect, 'lapse_defect': lapse_defect, 'lapse_defect_time': lapse_defect_time, 'scalar_defect': scalar_defect, 'kinematic_defect': kinematic_defect, 'bulk_flux': bulk_flux, 'F': spatial_f, 'N': lapse, 'clock': lapse / numerical.sqrt(spatial_f), 'clock_log_r': clock_log_r, 'clock_log_t': lapse_t / lapse - f_t / (2 * spatial_f), 'scalar_r': scalar_r, 'scalar_rr': scalar_rr, 'scalar_q': velocity_q, 'scalar_q_r': velocity_r}


def metric_weak_reconstruction(system, packed, profile, include_gram):
    basis, kappa = system.basis, system.kappa
    weights = basis.quadrature_weights
    radial_density = profile['hamiltonian_defect'] / (kappa * numerical.sqrt(profile['F']))
    lapse_row = basis.node_value.T @ (weights * radial_density)
    clock = profile['clock']
    mass_row = basis.face_value.T @ (weights * clock / kappa * (-profile['lapse_defect'] + profile['hamiltonian_defect'] / (profile['radius'] * profile['F'])))
    boundary_profile = flux_profile(system, packed, numerical.zeros_like(packed), basis.radii[[0, -1]])
    boundary_trace = numerical.zeros(system.face_count)
    boundary_trace[[0, -1]] = [-boundary_profile['clock'][0], boundary_profile['clock'][-1]]
    quadrature_ibp = (basis.face_gradient.T @ (weights * clock) + basis.face_value.T @ (weights * clock * profile['clock_log_r']) - boundary_trace) / kappa
    boundary_natural = boundary_trace / kappa
    boundary_natural[-1] -= system.outer_clock / kappa
    gram_mass, gram_lapse = numerical.zeros(system.face_count), numerical.zeros(system.node_count)
    if include_gram:
        node_mass = basis.face_to_node @ packed[system.slices[0]]
        node_f = 1 - 2 * node_mass / basis.radii
        gram_mass = basis.face_to_node.T @ (system.density * basis.radii * packed[system.slices[1]] / numerical.sqrt(node_f))
        gram_lapse = -system.density * basis.radii**2 * numerical.sqrt(node_f)
    return {'mass_row': mass_row + quadrature_ibp + boundary_natural + gram_mass, 'lapse_row': lapse_row + gram_lapse, 'quadrature_ibp': quadrature_ibp, 'natural_boundary': boundary_natural, 'gram_mass_row': gram_mass, 'gram_lapse_row': gram_lapse}
