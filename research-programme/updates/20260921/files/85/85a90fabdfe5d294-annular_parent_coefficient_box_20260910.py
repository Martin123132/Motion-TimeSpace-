import numpy as numerical
from scipy.linalg import solve

from annular_gram_joint_action_20260909 import gram_matrices
from annular_paired_variational_energy_20260910 import scalar_maps
from annular_adm_mixed_action_20260909 import linear_value_gradient
from annular_first_derivative_energy_20260909 import affine_lift_matrix


def down(value):
    return numerical.nextafter(value, -numerical.inf)


def up(value):
    return numerical.nextafter(value, numerical.inf)


class Box:
    __array_priority__ = 10000

    def __init__(self, lower, upper=None):
        self.lo = numerical.asarray(lower, dtype=float)
        self.hi = numerical.asarray(lower if upper is None else upper, dtype=float)
        self.lo, self.hi = numerical.broadcast_arrays(self.lo, self.hi)
        if numerical.any(self.lo > self.hi) or not numerical.all(numerical.isfinite(self.lo)) or not numerical.all(numerical.isfinite(self.hi)):
            raise ValueError('Invalid finite interval.')

    @staticmethod
    def cast(value):
        return value if isinstance(value, Box) else Box(value)

    def __add__(self, other):
        if isinstance(other, Taylor):
            return NotImplemented
        other = Box.cast(other)
        return Box(down(self.lo + other.lo), up(self.hi + other.hi))

    __radd__ = __add__

    def __neg__(self):
        return Box(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -Box.cast(other)

    def __rsub__(self, other):
        return Box.cast(other) + -self

    def __mul__(self, other):
        if isinstance(other, Taylor):
            return NotImplemented
        other = Box.cast(other)
        values = numerical.stack(numerical.broadcast_arrays(self.lo * other.lo, self.lo * other.hi, self.hi * other.lo, self.hi * other.hi))
        return Box(down(values.min(axis=0)), up(values.max(axis=0)))

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, Taylor):
            return NotImplemented
        other = Box.cast(other)
        if numerical.any((other.lo <= 0) & (other.hi >= 0)):
            raise ValueError('Interval division crosses zero.')
        return self * Box(down(1 / other.hi), up(1 / other.lo))

    def __rtruediv__(self, other):
        return Box.cast(other) / self

    def __pow__(self, exponent):
        if exponent == 0:
            return Box(numerical.ones_like(self.lo))
        if exponent < 0:
            return Box(1.) / self**(-exponent)
        if int(exponent) == exponent:
            if exponent == 2:
                lower = numerical.minimum(self.lo**2, self.hi**2)
                lower = numerical.where((self.lo <= 0) & (self.hi >= 0), 0., lower)
                return Box(numerical.maximum(0., down(lower)), up(numerical.maximum(self.lo**2, self.hi**2)))
            result = Box(1.)
            for unused in range(int(exponent)):
                result = result * self
            return result
        if exponent * 2 == int(exponent * 2):
            if numerical.any(self.lo < 0):
                raise ValueError('Square root outside nonnegative chart.')
            return Box(numerical.maximum(0., down(numerical.sqrt(self.lo))), up(numerical.sqrt(self.hi)))**int(exponent * 2)
        raise ValueError('Only integer/half-integer interval powers are supported.')

    def __getitem__(self, selected):
        return Box(self.lo[selected], self.hi[selected])

    @property
    def T(self):
        return Box(self.lo.T, self.hi.T)

    @property
    def magnitude(self):
        return numerical.maximum(abs(self.lo), abs(self.hi))

    @property
    def midpoint(self):
        return self.lo / 2 + self.hi / 2

    def __matmul__(self, other):
        other = Box.cast(other)
        first = self if self.lo.ndim == 2 else Box(self.lo[None, :], self.hi[None, :])
        second = other if other.lo.ndim == 2 else Box(other.lo[:, None], other.hi[:, None])
        if first.lo.shape[1] != second.lo.shape[0]:
            raise ValueError('Interval matrix shape mismatch.')
        result = Box(numerical.zeros((first.lo.shape[0], second.lo.shape[1])))
        for column in range(first.lo.shape[1]):
            result = result + first[:, column:column + 1] * second[column:column + 1, :]
        if self.lo.ndim == 1:
            result = result[0]
        if other.lo.ndim == 1:
            result = result[..., 0]
        return result

    def __rmatmul__(self, other):
        return Box.cast(other) @ self


def concatenate(values, axis=0):
    return Box(numerical.concatenate([value.lo for value in values], axis=axis), numerical.concatenate([value.hi for value in values], axis=axis))


class Taylor:
    __array_priority__ = 20000

    def __init__(self, coefficients):
        values = [Box.cast(value) for value in coefficients]
        self.coefficients = values + [Box(numerical.zeros_like(values[0].lo)) for unused in range(4 - len(values))]

    @staticmethod
    def cast(value):
        return value if isinstance(value, Taylor) else Taylor([value])

    def __add__(self, other):
        other = Taylor.cast(other)
        return Taylor([first + second for first, second in zip(self.coefficients, other.coefficients)])

    __radd__ = __add__

    def __neg__(self):
        return Taylor([-value for value in self.coefficients])

    def __sub__(self, other):
        return self + -Taylor.cast(other)

    def __rsub__(self, other):
        return Taylor.cast(other) + -self

    def __mul__(self, other):
        other = Taylor.cast(other)
        return Taylor([sum((self.coefficients[index] * other.coefficients[order - index] for index in range(order + 1)), Box(0.)) for order in range(4)])

    __rmul__ = __mul__

    def __pow__(self, exponent):
        if int(exponent) == exponent and exponent >= 0:
            result = Taylor([Box(1.)])
            for unused in range(int(exponent)):
                result = result * self
            return result
        base = self.coefficients[0]
        remainder = Taylor([Box(numerical.zeros_like(base.lo))] + [value / base for value in self.coefficients[1:]])
        result, power, binomial = Taylor([Box(1.)]), Taylor([Box(1.)]), Box(1.)
        for order in range(1, 4):
            power = power * remainder
            binomial = binomial * (exponent - order + 1) / order
            result = result + power * binomial
        return result * base**exponent

    def __truediv__(self, other):
        return self * Taylor.cast(other)**-1

    def __rtruediv__(self, other):
        return Taylor.cast(other) * self**-1

    def selected(self, selected):
        return Taylor([value[selected] for value in self.coefficients])

    def mapped(self, matrix):
        return Taylor([Box(matrix) @ value for value in self.coefficients])


def bilinear_box(weight, first, second):
    lower = numerical.zeros((first.shape[1], second.shape[1]))
    upper = lower.copy()
    for point in range(first.shape[0]):
        rows = numerical.flatnonzero(first[point])
        columns = numerical.flatnonzero(second[point])
        selection = numerical.ix_(rows, columns)
        addition = weight[point] * Box(first[point, rows][:, None]) * Box(second[point, columns][None, :])
        lower[selection] = down(lower[selection] + addition.lo)
        upper[selection] = up(upper[selection] + addition.hi)
    return Box(lower, upper)


def comparison_solve(matrix, load, reference=None):
    midpoint = matrix.midpoint
    inverse = solve(midpoint, numerical.eye(midpoint.shape[0]), assume_a='gen')
    defect = Box(numerical.eye(midpoint.shape[0])) - Box(inverse) @ matrix
    majorant = defect.magnitude
    row_sum = (Box(majorant) @ Box(numerical.ones(midpoint.shape[0]))).hi
    contraction = float(max(row_sum))
    if not numerical.isfinite(contraction) or contraction >= 1:
        raise ValueError('Coefficient-box inverse gate failed: ' + str(contraction))
    center = solve(midpoint, load.midpoint, assume_a='gen') if reference is None else reference
    residual = Box(inverse) @ (load - matrix @ Box(center))
    positive = residual.magnitude
    candidate = solve(numerical.eye(midpoint.shape[0]) - majorant, positive, assume_a='gen')
    candidate = numerical.maximum(0., candidate)
    defect_bound = (Box(majorant) @ Box(candidate) + Box(positive)).hi - candidate
    margin = max(0., float(numerical.max(defect_bound)))
    padding = up((margin + 1e-13 * (1 + float(numerical.max(candidate)))) / down(1 - contraction))
    radius = up(candidate + padding)
    inequality = (Box(majorant) @ Box(radius) + Box(positive)).hi <= radius
    if not numerical.all(inequality):
        raise RuntimeError('Componentwise inverse enclosure did not close.')
    enclosure = Box(down(center - radius), up(center + radius))
    return enclosure, {'contraction': contraction, 'max_solution_radius': float(max(radius)), 'componentwise_majorant_verified': True}


def jet_solve(matrix_coefficients, load_coefficients):
    result, diagnostics = [], []
    for order in range(3):
        load = load_coefficients[order]
        for earlier in range(order):
            load = load - matrix_coefficients[order - earlier] @ result[earlier]
        value, diagnostic = comparison_solve(matrix_coefficients[0], load)
        result.append(value)
        diagnostics.append(diagnostic)
    return result, diagnostics


def coefficient_inputs(system, packed, speed, second, radius):
    if radius < 0 or not numerical.isfinite(radius):
        raise ValueError('Invalid coefficient neighborhood radius.')
    orders = []
    widths = []
    for level, order in enumerate([packed, speed, second]):
        scale = numerical.maximum(1., abs(order))
        width = up(radius * scale) if radius else numerical.zeros_like(order)
        if level:
            width[system.fixed[1:]] = 0.
        lower, upper = down(order - width), up(order + width)
        if level:
            lower[system.fixed[1:]], upper[system.fixed[1:]] = order[system.fixed[1:]], order[system.fixed[1:]]
        orders.append(Box(lower, upper))
        widths.append(width)
    configuration = numerical.concatenate([system.scalar, system.slope])
    width = up(radius * numerical.maximum(1., abs(configuration))) if radius else numerical.zeros_like(configuration)
    configuration_box = Box(down(configuration - width), up(configuration + width))
    packed_jet = Taylor([orders[0], orders[1], orders[2] / 2])
    selected = slice(system.slices[2].start, system.count)
    configuration_jet = Taylor([configuration_box, orders[0][selected], orders[1][selected] / 2, orders[2][selected] / 6])
    return packed_jet, configuration_jet, widths


def parent_box_data(system, packed, speed, second, radius, include_gram):
    if any(system.constants[name] != 0 for name in ['Lambda', 'm_chi', 'b2', 'b3']):
        raise ValueError('Only the original canonical branch is covered.')
    if numerical.any(second[system.fixed[1:]] != 0):
        raise ValueError('Quadratic endpoint histories require zero endpoint velocity second rates.')
    basis, weights = system.basis, system.basis.quadrature_weights
    radius_q = basis.quadrature
    kappa = Box(1.) / 10
    if system.kappa != .1:
        raise ValueError('This sourced normalization is kappa=1/10.')
    packed_jet, configuration_jet, widths = coefficient_inputs(system, packed, speed, second, radius)
    mass, lapse, velocity = [packed_jet.selected(selected) for selected in system.slices]
    velocity_full = packed_jet.selected(slice(system.slices[2].start, system.count))
    maps = scalar_maps(basis, radius_q)
    mass_q, mass_r = mass.mapped(basis.face_value), mass.mapped(basis.face_gradient)
    lapse_q = lapse.mapped(basis.node_value)
    velocity_q = velocity_full.mapped(maps[0])
    gradient_q = configuration_jet.mapped(maps[1])
    spatial_f = 1 - 2 * mass_q / radius_q
    node_f = 1 - 2 * mass.mapped(basis.face_to_node) / basis.radii
    face_f = 1 - 2 * mass.coefficients[0] / basis.faces
    if min(numerical.min(face_f.lo), numerical.min(spatial_f.coefficients[0].lo), numerical.min(node_f.coefficients[0].lo), numerical.min(lapse.coefficients[0].lo)) <= 0:
        raise ValueError('Coefficient neighborhood crosses the positive metric chart.')
    mass_value, mass_gradient, lapse_value, scalar_velocity, scalar_gradient, field_f = [value.coefficients[0] for value in [mass_q, mass_r, lapse_q, velocity_q, gradient_q, spatial_f]]
    reciprocal = field_f**-.5
    local = [[Box(numerical.zeros_like(radius_q)) for other in range(4)] for first in range(4)]
    local[0][0] = 3 * lapse_value * mass_gradient / (kappa * radius_q**2) * field_f**-2.5 + 1.5 * scalar_velocity**2 / lapse_value * field_f**-2.5 + .5 * lapse_value * scalar_gradient**2 * field_f**-1.5
    local[0][1] = lapse_value / (kappa * radius_q) * field_f**-1.5
    local[0][2] = mass_gradient / (kappa * radius_q) * field_f**-1.5 - radius_q * scalar_velocity**2 / (2 * lapse_value**2) * field_f**-1.5 + radius_q * scalar_gradient**2 / 2 * reciprocal
    local[0][3] = radius_q * scalar_velocity / lapse_value * field_f**-1.5
    local[1][2] = reciprocal / kappa
    local[2][2] = radius_q**2 * scalar_velocity**2 / lapse_value**3 * reciprocal
    local[2][3] = -radius_q**2 * scalar_velocity / lapse_value**2 * reciprocal
    local[3][3] = radius_q**2 / lapse_value * reciprocal
    jacobian = Box(numerical.zeros((system.count, system.count)))
    for first in range(4):
        for other in range(first, 4):
            if numerical.all(local[first][other].magnitude == 0):
                continue
            contribution = bilinear_box(local[first][other] * weights, system.maps[first], system.maps[other])
            jacobian = jacobian + contribution
            if first != other:
                jacobian = jacobian + contribution.T
    factors, sampling = gram_matrices(system.node_count)
    scalar_nodes = configuration_jet.selected(slice(0, system.node_count))
    density_gram = (scalar_nodes.mapped(factors)**2).mapped(sampling.T) / (2 * basis.spacing)
    if include_gram:
        density_zero = density_gram.coefficients[0]
        gram_mm = density_zero * lapse.coefficients[0] * node_f.coefficients[0]**-1.5
        gram_mn = density_zero * basis.radii * node_f.coefficients[0]**-.5
        jacobian = jacobian + bilinear_box(gram_mm, system.node_maps[0], system.node_maps[0])
        mixed = bilinear_box(gram_mn, system.node_maps[0], system.node_maps[1])
        jacobian = jacobian + mixed + mixed.T
    mass_density = lapse_q * mass_r / (kappa * radius_q) * spatial_f**-1.5 + radius_q * velocity_q**2 / (2 * lapse_q) * spatial_f**-1.5 + radius_q * lapse_q * gradient_q**2 / 2 * spatial_f**-.5
    lapse_density = mass_r / kappa * spatial_f**-.5 - radius_q**2 * velocity_q**2 / (2 * lapse_q**2) * spatial_f**-.5 - radius_q**2 * gradient_q**2 / 2 * spatial_f**.5
    mass_row = (mass_density * weights).mapped(basis.face_value.T) + (lapse_q / kappa * spatial_f**-.5 * weights).mapped(basis.face_gradient.T)
    lapse_row = (lapse_density * weights).mapped(basis.node_value.T)
    momentum_density = radius_q**2 * velocity_q / lapse_q * spatial_f**-.5
    velocity_row = (momentum_density * weights).mapped(maps[0].T)
    stiffness_action = (radius_q**2 * lapse_q * spatial_f**.5 * gradient_q * weights).mapped(maps[1].T)
    coefficient = basis.radii**2 * lapse * node_f**.5
    if include_gram:
        mass_row = mass_row + (density_gram * basis.radii * lapse * node_f**-.5).mapped(basis.face_to_node.T)
        lapse_row = lapse_row - density_gram * basis.radii**2 * node_f**.5
        embed = numerical.pad(factors, ((0, 0), (0, system.node_count)))
        stiffness_action = stiffness_action + (coefficient.mapped(sampling) * configuration_jet.mapped(embed) / basis.spacing).mapped(embed.T)
    momentum_third = -2 * stiffness_action.coefficients[2]
    momentum_lower, momentum_upper = momentum_third.lo.copy(), momentum_third.hi.copy()
    momentum_lower[[0, system.node_count - 1]] = 0.
    momentum_upper[[0, system.node_count - 1]] = 0.
    momentum_third = Box(momentum_lower, momentum_upper)
    known = concatenate([6 * mass_row.coefficients[3], 6 * lapse_row.coefficients[3], 6 * velocity_row.coefficients[3] - momentum_third])
    pairing_weight = 1 / (kappa * lapse_q * spatial_f**1.5)
    pairing = [bilinear_box(value * weights, basis.face_value, basis.face_value) for value in pairing_weight.coefficients[:3]]
    matter = (-weights * radius_q**2 * velocity_q * gradient_q / (lapse_q * spatial_f**.5)).mapped(basis.face_value.T)
    gram_shift = Taylor([numerical.zeros(system.face_count)])
    if include_gram:
        links = system.links
        leading = scalar_nodes.mapped(factors)
        leading_time = velocity.mapped(factors)
        sampled = coefficient.mapped(sampling)
        current = coefficient.selected(links.node) * links.sweight * leading.selected(links.factor) * leading_time.selected(links.factor) / basis.spacing
        current = current - velocity.selected(links.node) * links.tweight * sampled.selected(links.factor) * leading.selected(links.factor) / basis.spacing
        inverse = 1 / (lapse.mapped(links.node_value)**2 * (1 - 2 * mass.mapped(links.face_value) / links.points))
        link_coefficients = []
        for value in inverse.coefficients[:3]:
            integrand = value[:, None] * links.face_value
            accumulated = Box(numerical.zeros((links.node.size, system.face_count)))
            lower, upper = accumulated.lo.copy(), accumulated.hi.copy()
            for point in range(links.points.size):
                added = integrand[point] * links.weights[point]
                pair = links.pairs[point]
                lower[pair] = down(lower[pair] + added.lo)
                upper[pair] = up(upper[pair] + added.hi)
            link_coefficients.append(Box(lower, upper))
        gram_coefficients = []
        for order in range(3):
            gram_coefficients.append(-sum((link_coefficients[index].T @ current.coefficients[order - index] for index in range(order + 1)), Box(numerical.zeros(system.face_count))))
        gram_shift = Taylor(gram_coefficients)
    shift_coefficients, shift_diagnostics = jet_solve(pairing, [(gram_shift - matter).coefficients[order] for order in range(3)])
    fixed_lower, fixed_upper = numerical.zeros(system.count), numerical.zeros(system.count)
    inner = 2 * shift_coefficients[2][0]
    fixed_lower[system.fixed[0]], fixed_upper[system.fixed[0]] = inner.lo, inner.hi
    fixed = Box(fixed_lower, fixed_upper)
    forcing = -(known + jacobian @ fixed)
    third_free, inverse_diagnostics = comparison_solve(jacobian[numerical.ix_(system.free, system.free)], forcing[system.free])
    third_lower, third_upper = fixed.lo.copy(), fixed.hi.copy()
    third_lower[system.free], third_upper[system.free] = third_free.lo, third_free.hi
    third = Box(third_lower, third_upper)
    endpoints = basis.radii[[0, -1]]
    endpoint_mass = mass.mapped(linear_value_gradient(basis.faces, endpoints)[0])
    endpoint_lapse = lapse.mapped(linear_value_gradient(basis.radii, endpoints)[0])
    mass0, mass1, mass2 = endpoint_mass.coefficients[:3]
    lapse0, lapse1, lapse2 = endpoint_lapse.coefficients[:3]
    denominator = endpoints - 2 * mass0
    mass_third = Box(linear_value_gradient(basis.faces, endpoints)[0]) @ third[system.slices[0]]
    lapse_third = Box(linear_value_gradient(basis.radii, endpoints)[0]) @ third[system.slices[1]]
    theta_tt = lapse_third / lapse0 - 6 * lapse1 * lapse2 / lapse0**2 + 2 * (lapse1 / lapse0)**3
    theta_tt = theta_tt - mass_third / denominator - 12 * mass1 * mass2 / denominator**2 - 8 * (mass1 / denominator)**3
    boundary = boundary_rate_box(system, packed_jet, configuration_jet, spatial_f, lapse_q, coefficient, theta_tt, include_gram)
    return {'jacobian': jacobian, 'known_third': known, 'fixed_third': fixed, 'forcing': forcing, 'third': third, 'theta_tt': theta_tt, 'boundary': boundary, 'inverse_diagnostics': inverse_diagnostics, 'shift_diagnostics': shift_diagnostics, 'minimum_F': float(min(face_f.lo.min(), spatial_f.coefficients[0].lo.min(), node_f.coefficients[0].lo.min())), 'minimum_N': float(lapse.coefficients[0].lo.min()), 'relative_radius': radius, 'packed_widths': widths}


def boundary_rate_box(system, packed_jet, configuration_jet, spatial_f, lapse_q, coefficient, theta_tt, include_gram):
    basis, count = system.basis, system.node_count
    maps = scalar_maps(basis, basis.quadrature)
    density = basis.quadrature**2 / (lapse_q * spatial_f**.5)
    radial_density = basis.quadrature**2 * lapse_q * spatial_f**.5
    mass_matrices = [bilinear_box(value * basis.quadrature_weights, maps[0], maps[0]) for value in density.coefficients[:3]]
    stiffness = [bilinear_box(value * basis.quadrature_weights, maps[1], maps[1]) for value in radial_density.coefficients[:2]]
    if include_gram:
        factors, sampling = gram_matrices(count)
        embed = numerical.pad(factors, ((0, 0), (0, count)))
        sampled = coefficient.mapped(sampling)
        stiffness = [matrix + bilinear_box(sampled.coefficients[order] / basis.spacing, embed, embed) for order, matrix in enumerate(stiffness)]
    endpoints = [0, count - 1]
    lift_map = Box(affine_lift_matrix(basis))
    lift = lift_map @ configuration_jet.coefficients[0][endpoints]
    lift_time = lift_map @ configuration_jet.coefficients[1][endpoints]
    lift_second = 2 * (lift_map @ configuration_jet.coefficients[2][endpoints])
    free = numerical.array([index for index in range(2 * count) if index not in endpoints])
    selection = numerical.ix_(free, free)
    force = -(mass_matrices[0] @ lift_second + mass_matrices[1] @ lift_time + stiffness[0] @ lift)[free]
    force_time = -(2 * (mass_matrices[1] @ lift_second) + 2 * (mass_matrices[2] @ lift_time) + stiffness[1] @ lift + stiffness[0] @ lift_time)[free]
    potential, first_diagnostic = comparison_solve(stiffness[0][selection], force)
    potential_time, second_diagnostic = comparison_solve(stiffness[0][selection], force_time - stiffness[1][selection] @ potential)
    potential_full_lo, potential_full_hi = numerical.zeros(2 * count), numerical.zeros(2 * count)
    potential_full_lo[free], potential_full_hi[free] = potential.lo, potential.hi
    potential_full = Box(potential_full_lo, potential_full_hi)
    potential_full_lo, potential_full_hi = numerical.zeros(2 * count), numerical.zeros(2 * count)
    potential_full_lo[free], potential_full_hi[free] = potential_time.lo, potential_time.hi
    potential_time_full = Box(potential_full_lo, potential_full_hi)
    points = basis.radii[endpoints]
    endmaps = scalar_maps(basis, points)
    mass_maps = linear_value_gradient(basis.faces, points)
    lapse_maps = linear_value_gradient(basis.radii, points)
    mass = packed_jet.selected(system.slices[0]).mapped(mass_maps[0])
    mass_radial = packed_jet.selected(system.slices[0]).mapped(mass_maps[1])
    lapse = packed_jet.selected(system.slices[1]).mapped(lapse_maps[0])
    lapse_radial = packed_jet.selected(system.slices[1]).mapped(lapse_maps[1])
    mass0, mass1, mass2 = mass.coefficients[:3]
    mass_r, mass1_r, mass2_r = mass_radial.coefficients[:3]
    lapse0, lapse1, lapse2 = lapse.coefficients[:3]
    lapse_r, lapse1_r, lapse2_r = lapse_radial.coefficients[:3]
    denominator, denominator_r = points - 2 * mass0, 1 - 2 * mass_r
    characteristic = lapse0 * (1 - 2 * mass0 / points)**.5
    theta = lapse1 / lapse0 - mass1 / denominator
    theta_time = 2 * lapse2 / lapse0 - (lapse1 / lapse0)**2 - 2 * mass2 / denominator - 2 * (mass1 / denominator)**2
    theta_r = lapse1_r / lapse0 - lapse1 * lapse_r / lapse0**2 - mass1_r / denominator + mass1 * denominator_r / denominator**2
    theta_tr = 2 * lapse2_r / lapse0 - 2 * lapse2 * lapse_r / lapse0**2 - 2 * lapse1 / lapse0 * (lapse1_r / lapse0 - lapse1 * lapse_r / lapse0**2)
    theta_tr = theta_tr - 2 * mass2_r / denominator + 2 * mass2 * denominator_r / denominator**2 - 4 * mass1 * mass1_r / denominator**2 + 4 * mass1**2 * denominator_r / denominator**3
    characteristic_r = characteristic * (lapse_r / lapse0 + (-mass_r / points + mass0 / points**2) / (1 - 2 * mass0 / points))
    ratio = 2 * characteristic**2 / points + characteristic * characteristic_r
    coefficient_d = characteristic**2 * theta_r
    ratio_time = 2 * theta * ratio + coefficient_d
    coefficient_time = characteristic**2 * (2 * theta * theta_r + theta_tr)
    full_gradient = Box(endmaps[1]) @ (potential_full + lift)
    full_time_gradient = Box(endmaps[1]) @ (potential_time_full + lift_time)
    ell_time, ell_second = Box(endmaps[0]) @ lift_time, Box(endmaps[0]) @ lift_second
    ell_time_r, ell_second_r = Box(endmaps[1]) @ lift_time, Box(endmaps[1]) @ lift_second
    beta = -coefficient_d * full_gradient - ratio * ell_time_r - 3 * theta * ell_second + (2 * theta**2 - theta_time) * ell_time
    beta_time = -coefficient_time * full_gradient - coefficient_d * full_time_gradient - ratio_time * ell_time_r - ratio * ell_second_r
    beta_time = beta_time + (2 * theta**2 - 4 * theta_time) * ell_second + (4 * theta * theta_time - theta_tt) * ell_time
    return {'beta': beta, 'beta_time': beta_time, 'potential': potential_full, 'potential_time': potential_time_full, 'force': force, 'force_time': force_time, 'elliptic_diagnostics': [first_diagnostic, second_diagnostic]}
