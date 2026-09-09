from functools import lru_cache

import numpy as numerical
import sympy as symbolic
from scipy.integrate import solve_ivp

from annular_covariant_time_transport_20260909 import ReferenceGeometry
from annular_mixed_grid_basis_20260909 import mixed_basis
from sbp4_derived_operator_20260909 import derivative


def real_linear(matrix, values):
    if numerical.iscomplexobj(values):
        return matrix @ values.real + 1j * (matrix @ values.imag)
    return matrix @ values


def linear_value_gradient(source, target):
    left = numerical.clip(numerical.searchsorted(source, target, side='right') - 1, 0, source.size - 2)
    width = source[left + 1] - source[left]
    fraction = (target - source[left]) / width
    basis = numerical.zeros((target.size, source.size))
    gradient = basis.copy()
    basis[numerical.arange(target.size), left] = 1 - fraction
    basis[numerical.arange(target.size), left + 1] = fraction
    gradient[numerical.arange(target.size), left] = -1 / width
    gradient[numerical.arange(target.size), left + 1] = 1 / width
    return basis, gradient


def hermite_matrices(source, target, nodal_derivative):
    left = numerical.clip(numerical.searchsorted(source, target, side='right') - 1, 0, source.size - 2)
    width = source[left + 1] - source[left]
    fraction = (target - source[left]) / width
    value, slope, gradient, slope_gradient = [numerical.zeros((target.size, source.size)) for unused in range(4)]
    rows = numerical.arange(target.size)
    value[rows, left] = 2 * fraction**3 - 3 * fraction**2 + 1
    value[rows, left + 1] = -2 * fraction**3 + 3 * fraction**2
    slope[rows, left] = width * (fraction**3 - 2 * fraction**2 + fraction)
    slope[rows, left + 1] = width * (fraction**3 - fraction**2)
    gradient[rows, left] = (6 * fraction**2 - 6 * fraction) / width
    gradient[rows, left + 1] = (-6 * fraction**2 + 6 * fraction) / width
    slope_gradient[rows, left] = 3 * fraction**2 - 4 * fraction + 1
    slope_gradient[rows, left + 1] = 3 * fraction**2 - 2 * fraction
    return value + slope @ nodal_derivative, gradient + slope_gradient @ nodal_derivative, slope, slope_gradient


class MixedActionBasis:
    def __init__(self, radii, order=4):
        self.radii = radii
        self.spacing = float(radii[1] - radii[0])
        self.faces, self.weights, self.face_to_node, self.node_to_face, self.incidence = mixed_basis(radii)
        self.derivative = derivative(numerical.eye(radii.size), self.spacing).T
        knots = numerical.unique(numerical.concatenate([radii, self.faces]))
        nodes, weights = numerical.polynomial.legendre.leggauss(order)
        centers, halfwidth = (knots[:-1] + knots[1:]) / 2, numerical.diff(knots) / 2
        self.quadrature = (centers[:, None] + halfwidth[:, None] * nodes).ravel()
        self.quadrature_weights = (halfwidth[:, None] * weights).ravel()
        self.face_value, self.face_gradient = linear_value_gradient(self.faces, self.quadrature)
        self.node_value, self.node_gradient = linear_value_gradient(radii, self.quadrature)
        self.scalar_value, self.scalar_gradient, self.lift_value, self.lift_gradient = hermite_matrices(radii, self.quadrature, self.derivative)

    def unpack(self, position, velocity, defect, defect_time, constants):
        scalar, mass, lapse, shift = position
        scalar_time, mass_time, unused_lapse_time, unused_shift_time = velocity
        radius = self.quadrature
        mass_q = real_linear(self.face_value, mass)
        mass_r = real_linear(self.face_gradient, mass)
        mass_t = real_linear(self.face_value, mass_time)
        lapse_q, lapse_r = real_linear(self.node_value, lapse), real_linear(self.node_gradient, lapse)
        shift_q, shift_r = real_linear(self.face_value, shift), real_linear(self.face_gradient, shift)
        scalar_q = real_linear(self.scalar_value, scalar) + real_linear(self.lift_value, defect)
        scalar_r = real_linear(self.scalar_gradient, scalar) + real_linear(self.lift_gradient, defect)
        scalar_t = real_linear(self.scalar_value, scalar_time) + real_linear(self.lift_value, defect_time)
        spatial_f = 1 - 2 * mass_q / radius - constants['Lambda'] * radius**2 / 3
        radial_scale = spatial_f**(-0.5)
        radial_scale_t = mass_t / (radius * spatial_f**1.5)
        spatial_f_r = -2 * mass_r / radius + 2 * mass_q / radius**2 - 2 * constants['Lambda'] * radius / 3
        radial_scale_r = -spatial_f_r / (2 * spatial_f**1.5)
        return radius, radial_scale, radial_scale_t, radial_scale_r, lapse_q, lapse_r, shift_q, shift_r, scalar_q, scalar_t, scalar_r

    def action(self, position, velocity, defect, defect_time, constants, kappa):
        radius, radial_scale, radial_scale_t, radial_scale_r, lapse, lapse_r, shift, shift_r, scalar, scalar_t, scalar_r = self.unpack(position, velocity, defect, defect_time, constants)
        gravity = (radius * shift * radial_scale_t / lapse - radius * shift**2 * radial_scale_r / lapse - radius * radial_scale * shift * shift_r / lapse - radial_scale * shift**2 / (2 * lapse) + lapse * (radial_scale - 1 / radial_scale) / 2 + lapse * radius * radial_scale_r / radial_scale**2 - constants['Lambda'] * lapse * radial_scale * radius**2 / 2) / kappa
        kinetic = -(scalar_t - shift * scalar_r)**2 / lapse**2 + scalar_r**2 / radial_scale**2
        matter_function = -kinetic / 2 - constants['m_chi']**2 * scalar**2 / 2 + constants['b2'] * kinetic**2 + constants['b3'] * kinetic**3
        matter = radius**2 * lapse * radial_scale * matter_function
        return numerical.dot(self.quadrature_weights, gravity + matter)

    def kinetic_matrix(self, position, velocity, defect, defect_time, constants):
        radius, radial_scale, unused_scale_t, unused_scale_r, lapse, unused_lapse_r, shift, unused_shift_r, scalar, scalar_t, scalar_r = self.unpack(position, velocity, defect, defect_time, constants)
        normal_velocity = (scalar_t - shift * scalar_r) / lapse
        kinetic = -normal_velocity**2 + scalar_r**2 / radial_scale**2
        principal = 1 - 4 * constants['b2'] * kinetic - 6 * constants['b3'] * kinetic**2
        slope = -4 * constants['b2'] - 12 * constants['b3'] * kinetic
        coefficient = radius**2 * radial_scale / lapse * (principal - 2 * slope * normal_velocity**2)
        return self.scalar_value.T @ ((self.quadrature_weights * coefficient)[:, None] * self.scalar_value)


@lru_cache(maxsize=1)
def coefficient_evaluator():
    velocity, gradient, mass, lapse, shift, radius, quartic, sextic, cosmological = symbolic.symbols('q w mu N V r b2 b3 Lambda', real=True)
    spatial_f = 1 - 2 * mass / radius - cosmological * radius**2 / 3
    radial_scale = spatial_f**(-symbolic.Rational(1, 2))
    kinetic = -(velocity - shift * gradient)**2 / lapse**2 + spatial_f * gradient**2
    principal = 1 - 4 * quartic * kinetic - 6 * sextic * kinetic**2
    slope = -4 * quartic - 12 * sextic * kinetic
    inverse_radial = spatial_f - shift**2 / lapse**2
    raised_radial = spatial_f * gradient + shift * (velocity - shift * gradient) / lapse**2
    coefficient = radius**2 * lapse * radial_scale * (principal * inverse_radial + 2 * slope * raised_radial**2)
    variables = [velocity, gradient, mass, lapse, shift]
    expressions = [coefficient.subs(shift, 0)]
    expressions += [symbolic.diff(coefficient, variable).subs(shift, 0) for variable in variables]
    expressions += [symbolic.diff(coefficient, first, second).subs(shift, 0) for first in variables for second in variables]
    return symbolic.lambdify([velocity, gradient, mass, lapse, radius, quartic, sextic, cosmological], expressions, 'numpy', cse=True, docstring_limit=0)


def coefficient_jets(velocity, gradient, mass, lapse, radius, constants):
    evaluated = coefficient_evaluator()(velocity, gradient, mass, lapse, radius, constants['b2'], constants['b3'], constants['Lambda'])
    values = numerical.stack([numerical.broadcast_to(value, radius.shape) for value in evaluated])
    return values[0], values[1:6], values[6:].reshape(5, 5, radius.size)


class OrthogonalReference(ReferenceGeometry):
    def __init__(self, case):
        super().__init__(case)
        advanced, radius = symbolic.symbols('v r', real=True)
        expression = symbolic.S.Zero
        epsilon = symbolic.Rational('0.1')
        for order, harmonics in case['fields']['scalar_ref'].items():
            for harmonic, amplitude in harmonics.items():
                mode = int(harmonic[3:])
                phase = symbolic.cos(mode * advanced / epsilon) if harmonic.startswith('cos') else symbolic.sin(mode * advanced / epsilon)
                expression += epsilon**int(order) * symbolic.sympify(amplitude, locals={'v': advanced, 'r': radius}) * phase
        mixed = symbolic.diff(expression, advanced, radius) + symbolic.Rational(str(self.sigma)) * symbolic.diff(expression, advanced, 2)
        self.scalar_mixed = symbolic.lambdify((advanced, radius), mixed, 'numpy', cse=True, docstring_limit=0)

    def adapted(self, tau, radii, anchor=6.0):
        distance = radii - anchor
        count = radii.size
        initial = numerical.concatenate([numerical.full(count, tau), numerical.ones(count), numerical.zeros(count)])

        def right_hand_side(position, packed):
            time, jacobian, second = packed.reshape(3, count)
            radius = anchor + position * distance
            connection, connection_time, connection_second = self.connection(time, radius)
            return numerical.concatenate([-distance * connection, -distance * connection_time * jacobian, -distance * (connection_second * jacobian**2 + connection_time * second)])

        solution = solve_ivp(right_hand_side, (0, 1), initial, method='DOP853', rtol=2e-13, atol=1e-14)
        if not solution.success:
            raise RuntimeError(solution.message)
        time, jacobian, second = solution.y[:, -1].reshape(3, count)
        data = self.fields(time, radii)
        scalar, velocity, acceleration, gradient = data['scalar_ref']
        mass, mass_time = data['mass_ref'][:2]
        old_shift, old_shift_time = data['shift_ref'][:2]
        exponential = numerical.exp(old_shift)
        spatial_f = 1 - 2 * mass / radii - self.constants['Lambda'] * radii**2 / 3
        connection, connection_time, unused_second = self.connection(time, radii)
        mixed = self.scalar_mixed(time + self.sigma * (radii - 4), radii)
        lapse = exponential * numerical.sqrt(spatial_f) * jacobian
        lapse_time = exponential * numerical.sqrt(spatial_f) * (second + jacobian**2 * (old_shift_time - mass_time / (radii * spatial_f)))
        return {'scalar': scalar, 'scalar_time': jacobian * velocity, 'scalar_second': jacobian**2 * acceleration + second * velocity, 'gradient': gradient - connection * velocity, 'gradient_time': jacobian * (mixed - connection * acceleration - connection_time * velocity), 'mass': mass, 'mass_time': jacobian * mass_time, 'lapse': lapse, 'lapse_time': lapse_time, 'old_time': time, 'jacobian': jacobian, 'spatial_f': spatial_f}
