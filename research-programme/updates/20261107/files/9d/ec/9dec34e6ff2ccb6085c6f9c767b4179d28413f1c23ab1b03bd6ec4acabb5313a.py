from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_P2_canonical_v2_20260918 import material_weight
import numpy as np


def material_weak_derivative(engine, material_order):
    labels, weights = np.polynomial.legendre.leggauss(material_order)
    labels, weights = labels / 2, weights / 2
    weights *= material_weight(labels)
    points, spatial_weights = np.polynomial.legendre.leggauss(4)
    local = (points + 1) / 2
    model, action = engine.owner.model, engine.action
    widths = np.diff(model.edges)
    reference = model.edges[:-1, None] + widths[:, None] * local
    measure = widths[:, None] * spatial_weights / 2
    answer = np.zeros((4, 3))
    for label, weight in zip(labels, weights):
        cardinal = engine.material.interpolation(np.array([label]))[0]
        coefficients = np.einsum('cpl,l->cp', engine.material.gradient_coefficients, cardinal)
        derivative_coefficients = np.einsum('cpl,l->cp', engine.direction_gradient, cardinal)
        rate_coefficients = np.einsum('cpl,l->cp', action.rate_polynomial, cardinal)
        radial, jacobian, unused, displacement, slope, source_direction = engine.mapping(reference, label)
        unused, unused2, unused3, unused4, unused5, velocity, unused6, velocity_direction = engine.source(np.array([label]))
        jacobian_rate = slope * source_direction
        gradient = (coefficients[:, :1] + coefficients[:, 1:] * local) / jacobian
        gradient_rate = (derivative_coefficients[:, :1] + derivative_coefficients[:, 1:] * local) / jacobian
        gradient_rate -= gradient * jacobian_rate / jacobian
        rate = rate_coefficients[:, :1] + local * (rate_coefficients[:, 1:2] + local * rate_coefficients[:, 2:3])
        temporal = rate - displacement * velocity * gradient
        if np.any(engine.velocity_direction):
            raise ValueError('Weak coordinate check requires fixed nodal velocities')
        temporal_rate = -displacement * velocity * gradient_rate
        speed = displacement * source_direction
        for power in range(3):
            profile = radial**power
            profile_rate = np.zeros_like(radial) if power == 0 else power * radial**(power - 1) * speed
            answer[0, power] += weight * np.sum(measure * (profile * (jacobian_rate * temporal**2 + 2 * jacobian * temporal * temporal_rate) + profile_rate * jacobian * temporal**2))
            answer[1, power] += weight * np.sum(measure * (profile * (jacobian_rate * gradient**2 + 2 * jacobian * gradient * gradient_rate) + profile_rate * jacobian * gradient**2))
        if engine.extension != 'reference':
            images = engine.loads.factor_vertices[engine.extension].T @ cardinal
            image_rate = engine.factor_direction.T @ cardinal
            nodal_load = np.asarray(engine.loads.sampling.T @ (images**2 / 2)).ravel()
            nodal_rate = np.asarray(engine.loads.sampling.T @ (images * image_rate)).ravel()
            radial, jacobian, unused, displacement, slope, direction = engine.mapping(engine.loads.knots, label)
            density = nodal_load / jacobian
            density_rate = nodal_rate / jacobian - density * slope * direction / jacobian
            for power in range(3):
                answer[2, power] += weight * np.sum(radial**power * density_rate)
                if power:
                    answer[2, power] += weight * np.sum(power * radial**(power - 1) * displacement * direction * density)
        source, unused, unused2, direction, unused3, unused4, unused5, unused6 = engine.source(np.array([label]))
        for power in [1, 2]:
            answer[3, power] += weight * float((power * source**(power - 1) * direction)[0])
    return answer


def radial_weak_derivative(response):
    solver = response.solver
    measure = (solver.lengths[:, None] * solver.rule.integration[-1][None, :] / 2).ravel()
    radius = solver.nodes.ravel()
    return np.array([[measure @ (response.field_rates[name] * radius**power) for power in range(3)]
        for name in ['temporal_square', 'gradient_square', 'gram', 'source_density']])
