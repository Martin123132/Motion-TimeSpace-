import numpy as numerical
from scipy.integrate import solve_ivp

from annular_adm_mixed_action_20260909 import linear_value_gradient
from annular_canonical_mesh_transfer_20260911 import fields


def hermite_fields(basis, coefficients, points):
    count = basis.radii.size
    slopes = basis.derivative @ coefficients[:count] + coefficients[count:] / basis.spacing
    left = numerical.clip(numerical.searchsorted(basis.radii, points, side='right') - 1, 0, count - 2)
    width = basis.radii[left + 1] - basis.radii[left]
    fraction = (points - basis.radii[left]) / width
    value = (2 * fraction**3 - 3 * fraction**2 + 1) * coefficients[left] + (-2 * fraction**3 + 3 * fraction**2) * coefficients[left + 1]
    value += width * ((fraction**3 - 2 * fraction**2 + fraction) * slopes[left] + (fraction**3 - fraction**2) * slopes[left + 1])
    gradient = (6 * fraction**2 - 6 * fraction) * (coefficients[left] - coefficients[left + 1]) / width
    gradient += (3 * fraction**2 - 4 * fraction + 1) * slopes[left] + (3 * fraction**2 - 2 * fraction) * slopes[left + 1]
    second = (12 * fraction - 6) * (coefficients[left] - coefficients[left + 1]) / width**2
    second += ((6 * fraction - 4) * slopes[left] + (6 * fraction - 2) * slopes[left + 1]) / width
    return value, gradient, second


class ConstructedGRFields:
    def __init__(self, basis, saved, clock):
        self.basis = basis
        self.configuration = saved['configuration']
        packed = saved['original_packed']
        count, face_count = basis.radii.size, basis.faces.size
        self.lapse_seed = packed[face_count:face_count + count]
        self.velocity_seed = packed[face_count + count:]
        self.inner_mass = packed[0]
        self.boundary_drive = saved['boundary_drive']
        self.knots = saved['knots']
        inner_f = 1 - 2 * self.inner_mass / basis.radii[0]
        inner_w = hermite_fields(basis, self.configuration, basis.radii[:1])[1][0]
        self.velocity_change = self.boundary_drive[0] / (.1 * basis.radii[0]**2 * inner_f * inner_w) - self.velocity_seed[0]
        self.solutions = []
        state = numerical.array([self.inner_mass, 0.])
        for left, right in zip(self.knots[:-1], self.knots[1:]):
            def right_hand_side(position, values):
                data = self.free(numerical.array([position]))
                multiplier = .1 * position * data['w'][0]**2
                source = .05 * position**2 * numerical.array([data['w'][0]**2, data['q'][0]**2 / data['N0'][0]**2])
                return source - multiplier * values
            solved = solve_ivp(right_hand_side, (left, right), state, dense_output=True, method='DOP853', rtol=2e-12, atol=2e-14)
            if not solved.success:
                raise RuntimeError(solved.message)
            self.solutions.append(solved.sol)
            state = solved.y[:, -1]
        clock_factor = clock**2 / self.lapse_seed[-1]**2
        geometry_a = 1 - 2 * state[0] / basis.radii[-1]
        discriminant = (clock_factor * geometry_a)**2 - 8 * clock_factor * state[1] / basis.radii[-1]
        self.scale_squared = (clock_factor * geometry_a + numerical.sqrt(discriminant)) / 2
        self.scale = numerical.sqrt(self.scale_squared)
        self.original_agreement = float(abs(self.evaluate(saved['radii'])['mu'] - saved['mass']).max())

    def free(self, points):
        scalar, gradient, second = hermite_fields(self.basis, self.configuration, points)
        velocity, velocity_r, unused_second = hermite_fields(self.basis, self.velocity_seed, points)
        width = self.basis.radii[-1] - self.basis.radii[0]
        fraction = (points - self.basis.radii[0]) / width
        velocity += self.velocity_change * (1 - 3 * fraction**2 + 2 * fraction**3)
        velocity_r += self.velocity_change * (-6 * fraction + 6 * fraction**2) / width
        value, derivative = linear_value_gradient(self.basis.radii, points)
        return {'chi': scalar, 'w': gradient, 'w_r': second, 'q': velocity, 'q_r': velocity_r, 'N0': value @ self.lapse_seed, 'N0_r': derivative @ self.lapse_seed}

    def evaluate(self, points):
        data = self.free(points)
        segment = numerical.clip(numerical.searchsorted(self.knots, points, side='right') - 1, 0, len(self.solutions) - 1)
        values = numerical.empty((2, points.size))
        for index in numerical.unique(segment):
            selected = segment == index
            values[:, selected] = self.solutions[index](points[selected])
        data['mu'] = values[0] + values[1] / self.scale_squared
        data['N'] = self.scale * data['N0']
        data['N_r'] = self.scale * data['N0_r']
        data['mu_r'] = .05 * points**2 * (data['w']**2 + data['q']**2 / data['N']**2) - .1 * points * data['w']**2 * data['mu']
        data['F'] = 1 - 2 * data['mu'] / points
        data['F_r'] = -2 * data['mu_r'] / points + 2 * data['mu'] / points**2
        kinetic = points**2 / (data['N'] * numerical.sqrt(data['F']))
        data['pi'] = kinetic * data['q']
        data['pi_r'] = kinetic * (data['q_r'] + data['q'] * (2 / points - data['N_r'] / data['N'] - data['F_r'] / (2 * data['F'])))
        return data


class SavedCanonicalFields:
    def __init__(self, model, saved):
        self.model = model
        self.mass = saved['mass_coefficients']
        self.pi = saved['pi_coefficients']
        self.configuration = saved['configuration']
        model.fixed_lapse = saved['fixed_lapse'].copy()
        self.knots = numerical.unique(numerical.concatenate([model.basis.radii, model.basis.faces]))
        self.boundary_drive = saved['boundary_velocity']

    def evaluate(self, points):
        sampled = fields(self.model, self.mass, self.pi, points)
        unused_chi, unused_gradient, second = hermite_fields(self.model.basis, self.configuration, points)
        lapse_r = linear_value_gradient(self.model.basis.radii, points)[1] @ self.model.fixed_lapse
        return {'chi': sampled['chi'], 'w': sampled['chi_gradient'], 'w_r': second, 'mu': sampled['mass'], 'mu_r': sampled['mass_gradient'], 'pi': sampled['pi'], 'pi_r': sampled['pi_gradient'], 'N': sampled['lapse'], 'N_r': lapse_r, 'F': sampled['F'], 'F_r': -2 * sampled['mass_gradient'] / points + 2 * sampled['mass'] / points**2}


def local_rate_families(data, points, lapse_value, lapse_gradient):
    geometry, geometry_r = data['F'], data['F_r']
    energy = data['pi']**2 / (2 * points**2) + points**2 * data['w']**2 / 2
    mass_factor = .1 * geometry**1.5 * data['pi'] * data['w']
    mass_factor_r = .1 * (1.5 * numerical.sqrt(geometry) * geometry_r * data['pi'] * data['w'] + geometry**1.5 * (data['pi_r'] * data['w'] + data['pi'] * data['w_r']))
    scalar_factor = numerical.sqrt(geometry) * data['pi'] / points**2
    scalar_factor_r = scalar_factor * (geometry_r / (2 * geometry) - 2 / points) + numerical.sqrt(geometry) * data['pi_r'] / points**2
    scalar_flux = numerical.sqrt(geometry) * points**2 * data['w']
    scalar_flux_r = geometry_r * points**2 * data['w'] / (2 * numerical.sqrt(geometry)) + numerical.sqrt(geometry) * (2 * points * data['w'] + points**2 * data['w_r'])
    geometric_factor = energy / (points * numerical.sqrt(geometry)) + data['mu'] / (.1 * points**2 * geometry**1.5)
    return {
        'mass_q': lapse_value * mass_factor[:, None],
        'mass_qr': lapse_gradient * mass_factor[:, None] + lapse_value * mass_factor_r[:, None],
        'mass_p': lapse_value * geometric_factor[:, None] - lapse_gradient / (.1 * numerical.sqrt(geometry))[:, None],
        'scalar_q': lapse_value * scalar_factor[:, None],
        'scalar_qr': lapse_gradient * scalar_factor[:, None] + lapse_value * scalar_factor_r[:, None],
        'scalar_p': lapse_gradient * scalar_flux[:, None] + lapse_value * scalar_flux_r[:, None],
    }
