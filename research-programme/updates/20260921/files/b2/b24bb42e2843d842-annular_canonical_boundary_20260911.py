import numpy as numerical
from scipy.linalg import solve

from annular_parent_root_residence_20260910 import canonical_maps
from annular_time_link_adjoint_20260911 import frozen_maps
from annular_adm_mixed_action_20260909 import linear_value_gradient
from annular_gram_joint_action_20260909 import gram_matrices


def wronskian_tent(radii, lapse, peak):
    primitive = numerical.concatenate([[0.], numerical.cumsum(numerical.diff(radii) / (lapse[:-1] * lapse[1:]))])
    shape = numerical.empty_like(lapse)
    shape[:peak + 1] = lapse[:peak + 1] / lapse[peak] * primitive[:peak + 1] / primitive[peak]
    shape[peak + 1:] = lapse[peak + 1:] / lapse[peak] * (primitive[-1] - primitive[peak + 1:]) / (primitive[-1] - primitive[peak])
    return shape, primitive


class CanonicalBoundarySystem:
    def __init__(self, system, packed, configuration, include_gram, boundary_velocity):
        self.system, self.basis, self.links = system, system.basis, system.links
        self.packed, self.configuration = packed, configuration
        self.include_gram = include_gram
        self.boundary_velocity = numerical.asarray(boundary_velocity)
        self.count, self.face_count = system.node_count, system.face_count
        self.maps = frozen_maps(system, packed, configuration)
        self.value, self.gradient = canonical_maps(self.basis)
        self.radius, self.weights = self.basis.quadrature, self.basis.quadrature_weights
        self.mass = packed[system.slices[0]]
        self.lapse_seed = packed[system.slices[1]]
        self.mass_q = self.basis.face_value @ self.mass
        self.mass_r = self.basis.face_gradient @ self.mass
        self.spatial_f = 1 - 2 * self.mass_q / self.radius
        self.node_f = 1 - 2 * (self.basis.face_to_node @ self.mass) / self.basis.radii
        lapse_q = self.basis.node_value @ self.lapse_seed
        self.kinetic_seed = self.radius**2 / (lapse_q * numerical.sqrt(self.spatial_f))
        self.rho_seed = 1 / (.1 * lapse_q * self.spatial_f**1.5)
        self.pi_map = self.kinetic_seed[:, None] * self.value
        self.momentum_map = self.rho_seed[:, None] * self.maps['shift_map']
        self.mass_pair = self.momentum_map.T @ (self.weights[:, None] * self.maps['mass_map'])
        self.scalar_pair = self.pi_map.T @ (self.weights[:, None] * self.value)
        self.mass_inverse = solve(self.mass_pair, numerical.eye(self.mass_pair.shape[0]))
        self.scalar_inverse = solve(self.scalar_pair, numerical.eye(self.scalar_pair.shape[0]))
        self.pi = self.pi_map @ packed[system.slices[2].start:]
        self.scalar_gradient = self.gradient @ configuration
        factors, self.sampling = gram_matrices(self.count)
        self.amplitude = factors @ configuration[:self.count]
        self.gram_density = self.sampling.T @ self.amplitude**2 / (2 * self.basis.spacing)
        link_lapse = self.links.node_value @ self.lapse_seed
        link_lapse_r = linear_value_gradient(self.basis.radii, self.links.points)[1] @ self.lapse_seed
        link_f = 1 - 2 * (self.links.face_value @ self.mass) / self.links.points
        link_node, link_node_r = linear_value_gradient(self.basis.radii, self.links.points)
        zeta = link_f[:, None] * (link_lapse[:, None] * link_node_r[:, 1:-1] - link_lapse_r[:, None] * link_node[:, 1:-1])
        shift_map = numerical.concatenate([self.links.face_value, zeta - self.links.face_value @ self.maps['projection']], axis=1)
        self.link_momentum_map = shift_map / (.1 * link_lapse * link_f**1.5)[:, None]
        self.link_f = link_f
        self.unknown_count = self.count + 3

    def gram_sources(self, lapse, scalar_velocity, momentum_rate):
        links, basis = self.links, self.basis
        local_lapse = links.node_value @ lapse
        if numerical.any(abs(local_lapse) < 1e-10):
            raise ValueError('Lapse leaves the nonzero transport chart.')
        momentum_time = self.link_momentum_map @ momentum_rate
        generator = .1 * numerical.sqrt(self.link_f) * momentum_time / local_lapse
        endpoint_log, partial_log = links.integrate(generator), links.partial(generator)
        if max(abs(endpoint_log).max(), abs(partial_log).max()) > 50:
            raise ValueError('Initial time-link rate outside bounded diagnostic chart.')
        endpoint, partial = numerical.exp(endpoint_log), numerical.exp(partial_log)
        coefficient = basis.radii**2 * lapse * numerical.sqrt(self.node_f)
        density = links.collect(links.sweight * endpoint * coefficient[links.node])
        amplitude_time = links.collect(links.tweight * scalar_velocity[links.node] * endpoint)
        current = self.amplitude[links.factor] * (links.sweight * coefficient[links.node] * amplitude_time[links.factor] - links.tweight * scalar_velocity[links.node] * density[links.factor]) / basis.spacing
        weighted_current = current * endpoint
        kernel = links.integrate(self.link_momentum_map * (.1 * numerical.sqrt(self.link_f) / (local_lapse * partial**2))[:, None])
        momentum_force = kernel.T @ weighted_current
        scalar_force = numerical.zeros(2 * self.count, dtype=numerical.result_type(lapse, momentum_rate))
        numerical.add.at(scalar_force, links.node, -links.tweight * self.amplitude[links.factor] * density[links.factor] / (basis.spacing * endpoint))
        density_time = numerical.zeros(self.count, dtype=scalar_force.dtype)
        numerical.add.at(density_time, links.node, links.sweight * self.amplitude[links.factor] * amplitude_time[links.factor] / (basis.spacing * endpoint))
        beta_time = .1 * local_lapse * self.link_f**1.5 * momentum_time
        transport_kernel = links.integrate(links.node_value * (beta_time / (local_lapse**3 * self.link_f * partial**2))[:, None])
        transport_time = -(transport_kernel.T @ weighted_current)
        return {'momentum_force': momentum_force, 'scalar_force': scalar_force, 'density_time': density_time, 'transport_time': transport_time, 'endpoint_log': endpoint_log, 'anchor_current': links.collect(weighted_current)}

    def evaluate(self, unknown):
        lapse, reactions = unknown[:self.count], unknown[self.count:]
        lapse_q = self.basis.node_value @ lapse
        spatial_f, radius, weights = self.spatial_f, self.radius, self.weights
        mass_density = lapse_q * self.mass_r / (.1 * radius * spatial_f**1.5)
        mass_density += lapse_q * self.pi**2 / (2 * radius**3 * numerical.sqrt(spatial_f)) + radius * lapse_q * self.scalar_gradient**2 / (2 * numerical.sqrt(spatial_f))
        mass_force = self.maps['mass_map'].T @ (weights * mass_density) + self.maps['mass_gradient'].T @ (weights * lapse_q / (.1 * numerical.sqrt(spatial_f)))
        mass_force[self.face_count - 1] -= self.system.outer_clock / .1
        if self.include_gram:
            mass_force[:self.face_count] += self.basis.face_to_node.T @ (self.basis.radii * lapse * self.gram_density / numerical.sqrt(self.node_f))
        mass_force[0] += reactions[0]
        momentum_rate = self.mass_inverse.T @ mass_force
        scalar_velocity = self.scalar_inverse @ (self.pi_map.T @ (weights * lapse_q * numerical.sqrt(spatial_f) * self.pi / radius**2))
        bulk_mass_speed = .1 * lapse_q * spatial_f**1.5 * self.pi * self.scalar_gradient
        mass_load = self.momentum_map.T @ (weights * bulk_mass_speed)
        scalar_force = -(self.gradient.T @ (weights * lapse_q * numerical.sqrt(spatial_f) * radius**2 * self.scalar_gradient))
        sources = None
        if self.include_gram:
            sources = self.gram_sources(lapse, scalar_velocity, momentum_rate)
            mass_load -= sources['momentum_force']
            scalar_force += sources['scalar_force']
        scalar_force[0] += reactions[1]
        scalar_force[self.count - 1] += reactions[2]
        mass_rate = self.mass_inverse @ mass_load
        pi_rate = self.scalar_inverse.T @ scalar_force
        physical_mass_rate = self.maps['mass_map'] @ mass_rate
        physical_mass_gradient = self.maps['mass_gradient'] @ mass_rate
        physical_pi_rate = self.pi_map @ pi_rate
        physical_momentum_rate = self.momentum_map @ momentum_rate
        scalar_velocity_gradient = self.gradient @ scalar_velocity
        constraint_density = physical_mass_gradient / (.1 * numerical.sqrt(spatial_f))
        constraint_density += (self.mass_r / (.1 * radius * spatial_f**1.5) + self.pi**2 / (2 * radius**3 * numerical.sqrt(spatial_f)) + radius * self.scalar_gradient**2 / (2 * numerical.sqrt(spatial_f))) * physical_mass_rate
        constraint_density -= numerical.sqrt(spatial_f) * self.pi * physical_pi_rate / radius**2
        constraint_density -= radius**2 * numerical.sqrt(spatial_f) * self.scalar_gradient * scalar_velocity_gradient
        constraint_density -= .1 * spatial_f**1.5 * self.pi * self.scalar_gradient * physical_momentum_rate
        constraint_rate = self.basis.node_value.T @ (weights * constraint_density)
        if self.include_gram:
            node_mass_rate = self.basis.face_to_node @ mass_rate[:self.face_count]
            constraint_rate += self.basis.radii * self.gram_density * node_mass_rate / numerical.sqrt(self.node_f) - self.basis.radii**2 * numerical.sqrt(self.node_f) * sources['density_time'] + sources['transport_time']
        boundary = numerical.array([mass_rate[0], scalar_velocity[0], scalar_velocity[self.count - 1]]) - self.boundary_velocity
        residual = numerical.concatenate([constraint_rate, boundary])
        return {'residual': residual, 'constraint_rate': constraint_rate, 'mass_rate': mass_rate, 'momentum_rate': momentum_rate, 'scalar_velocity': scalar_velocity, 'pi_rate': pi_rate, 'boundary_residual': boundary, 'sources': sources, 'minimum_lapse_node': float(numerical.real(lapse).min()), 'maximum_lapse_node': float(numerical.real(lapse).max())}

    def gr_linear_system(self):
        if self.include_gram:
            raise ValueError('The nonlocal Gram equations are not claimed linear.')
        zero = numerical.zeros(self.unknown_count)
        source = self.evaluate(zero)['residual']
        columns = []
        for column in range(self.unknown_count):
            changed = zero.copy()
            changed[column] = 1
            columns.append(self.evaluate(changed)['residual'] - source)
        return numerical.column_stack(columns), -source

    def jacobian(self, unknown):
        matrix = numerical.empty((self.unknown_count, self.unknown_count))
        for column in range(self.unknown_count):
            changed = unknown.astype(complex)
            changed[column] += 1e-25j
            matrix[:, column] = self.evaluate(changed)['residual'].imag / 1e-25
        return matrix
