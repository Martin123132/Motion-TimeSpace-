from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_Legendre_current_20260921 import samples
from annular_directional_coupled_Euler_20260928 import interpolate_nodal
from derive_annular_native_shape_stress_20260928 import physical_data
from annular_physical_native_kernel_20260928 import decimals
from decimal import Decimal
from time import perf_counter
import numpy as np
import sympy as sp


def coefficient_data(radius, values, radial):
    mass, nu = values
    metric = 1 - 2 * mass / radius
    metric_r = -2 * radial[0] / radius + 2 * mass / radius**2
    alpha = radius**2 / (np.exp(nu) * np.sqrt(metric))
    beta = radius**2 * np.exp(nu) * np.sqrt(metric)
    alpha_r = alpha * (2 / radius - radial[1] - metric_r / (2 * metric))
    beta_r = beta * (2 / radius + radial[1] + metric_r / (2 * metric))
    return alpha, beta, alpha_r, beta_r


def dust_covectors(radius, velocity, values, radial, source_mass, acceleration=None, metric_time=None):
    mass, nu = values
    metric = 1 - 2 * mass / radius
    metric_r = -2 * radial[0] / radius + 2 * mass / radius**2
    lapse = np.exp(nu)
    clock = np.sqrt(lapse**2 - velocity**2 / metric)
    momentum = source_mass * velocity / (metric * clock)
    force = -source_mass * (lapse**2 * radial[1] + velocity**2 * metric_r / (2 * metric**2)) / clock
    if acceleration is None:
        return momentum, force
    nu_time = metric_time[1] + velocity * radial[1]
    metric_rate = -2 * (metric_time[0] + velocity * radial[0]) / radius + 2 * mass * velocity / radius**2
    clock_rate = (lapse**2 * nu_time - velocity * acceleration / metric + velocity**2 * metric_rate / (2 * metric**2)) / clock
    momentum_rate = source_mass * (acceleration / (metric * clock) - velocity * metric_rate / (metric**2 * clock)
        - velocity * clock_rate / (metric * clock**2))
    return momentum, force, momentum_rate


def wave_packet(row, values, radial, metric_time, rate, rate_r, acceleration, speed, speed_r, speed_rate):
    geometry = row['geometry']
    radius = geometry['radius']
    gradient = row['gradient'] / geometry['jacobian']
    alpha, beta, alpha_r, beta_r = coefficient_data(radius, values, radial)
    temporal = rate - speed * gradient
    gradient_rate = rate_r - speed_r * gradient
    temporal_rate = acceleration - speed_rate * gradient - speed * gradient_rate
    metric = 1 - 2 * values[0] / radius
    metric_material_rate = -2 * (metric_time[0] + speed * radial[0]) / radius + 2 * values[0] * speed / radius**2
    alpha_ratio = 2 * speed / radius - metric_time[1] - speed * radial[1] - metric_material_rate / (2 * metric)
    momentum = alpha * temporal
    momentum_rate = alpha * (temporal_rate + (speed_r + alpha_ratio) * temporal)
    displacement = geometry['displacement']
    displacement_r = geometry['jacobian_source'] / geometry['jacobian']
    force_field = -(alpha * temporal * speed + beta * gradient)
    force_source = (displacement * alpha_r + alpha * displacement_r) * temporal**2 / 2
    force_source += alpha * temporal * speed * gradient * displacement_r
    force_source -= (displacement * beta_r - beta * displacement_r) * gradient**2 / 2
    return dict(momentum=momentum, momentum_rate=momentum_rate, force_field=force_field,
        force_source=force_source, source_momentum_rate=-displacement * (gradient * momentum_rate + gradient_rate * momentum))


def symbolic_checks(evidence):
    jac, alpha, beta, gradient, rate, speed, displacement, slope = sp.symbols('J alpha beta g v W D d', real=True)
    alpha_r, beta_r, variation, field_r = sp.symbols('alpha_R beta_R epsilon field_R', real=True)
    temporal = rate - speed * gradient
    source_moved = (jac + variation * slope) * ((alpha + variation * displacement * alpha_r)
        * (rate - speed * gradient * jac / (jac + variation * slope))**2
        - (beta + variation * displacement * beta_r) * (gradient * jac / (jac + variation * slope))**2) / 2
    expected = jac * ((displacement * alpha_r + alpha * slope / jac) * temporal**2 / 2
        + alpha * temporal * speed * gradient * slope / jac
        - (displacement * beta_r - beta * slope / jac) * gradient**2 / 2)
    evidence.check('exact_source_wave_force', sp.simplify(sp.diff(source_moved, variation).subs(variation, 0) - expected) == 0)
    field_moved = jac * (alpha * (rate - speed * (gradient + variation * field_r))**2
        - beta * (gradient + variation * field_r)**2) / 2
    evidence.check('exact_field_wave_force', sp.expand(sp.diff(field_moved, variation).subs(variation, 0)
        + jac * (alpha * temporal * speed + beta * gradient) * field_r) == 0)
    time = sp.symbols('time')
    jac_t, alpha_t, grad_t, rate_t, speed_t = [sp.Function(name)(time) for name in ['J', 'alpha', 'g', 'v', 'W']]
    direct = sp.diff(jac_t * alpha_t * (rate_t - speed_t * grad_t), time)
    expected = jac_t * alpha_t * (sp.diff(rate_t, time) - sp.diff(speed_t, time) * grad_t - speed_t * sp.diff(grad_t, time)
        + (sp.diff(jac_t, time) / jac_t + sp.diff(alpha_t, time) / alpha_t) * (rate_t - speed_t * grad_t))
    evidence.check('exact_material_momentum_rate', sp.simplify(direct - expected) == 0)


def native_velocity_force(native, loads, action, label, response, step=Decimal('1e-12')):
    if not native.enabled:
        return np.zeros(loads.rates.shape[1])
    data = physical_data(native, loads, action, label)
    radius = np.asarray(data['edges'][native.native_edges], float)
    values, radial = action.solver.values(action.solution, radius)
    variation, variation_r = response.solver.values(response.solution, radius)
    amount = 1j * 1e-25
    unused, changed_beta, unused2, changed_beta_r = coefficient_data(radius, values + amount * variation, radial + amount * variation_r)
    beta_variation = decimals(changed_beta.imag / 1e-25)
    beta_r_variation = decimals(changed_beta_r.imag / 1e-25)
    plus = native.evaluate(data['edges'], data['field'], data['beta'] + step * beta_variation)
    minus = native.evaluate(data['edges'], data['field'], data['beta'] - step * beta_variation)
    field = -(plus['field_gradient'] - minus['field_gradient']) / (2 * step)
    edges = -(plus['edge_gradient'] - minus['edge_gradient']) / (2 * step)
    source = sum(edges * data['displacement'], Decimal(0))
    source -= sum(plus['load'] * beta_r_variation * data['displacement'][native.native_edges], Decimal(0))
    return np.r_[np.asarray(field, float), float(source)]


def material_reaction(loads, action, native, directions, correction, mode_rate, acceleration,
                      position, velocity, metric_time, trial_time, order, deadline, progress, reference_order=12):
    points, weights = np.polynomial.legendre.leggauss(order)
    points, weights = points / 2, weights / 2
    weights *= 6 * (points + .5) * (.5 - points)
    names = ['position', 'force_wave', 'force_native', 'momentum_rate', 'base_momentum', 'base_force_wave']
    output = {name: np.zeros_like(loads.rates) for name in names}
    amount = 1j * 1e-25
    field_direction = directions['field_vertices'] - correction[:, :-1]
    source_direction = -correction[:, -1]
    reference_edges = np.asarray([float(value) for value in action.edges])
    for index, (label, weight) in enumerate(zip(points, weights)):
        if perf_counter() > deadline:
            raise RuntimeError('Safe old-field material boundary')
        row = samples(action, label, reference_order)
        geometry, quad, cardinal = row['geometry'], row['quadrature'], row['cardinal']
        radius, spatial = geometry['radius'], geometry['jacobian']
        indices = np.asarray(action.mesh['elements'])[quad['cells']]
        selected = indices >= 0
        widths = np.diff(reference_edges)[quad['cells']] * spatial
        interpolate = lambda values: interpolate_nodal(cardinal @ values, indices, quad['local'], widths)
        field, field_r = interpolate(field_direction)
        old_accel = interpolate(acceleration[:, :-1])[0]
        acceleration_change = interpolate(2 * mode_rate[:, :-1])[0]
        source_mode = float(cardinal @ source_direction)
        source_accel = float(cardinal @ acceleration[:, -1])
        source_accel_change = float(cardinal @ (2 * mode_rate[:, -1]))
        edge = cardinal @ directions['edge_vertices']
        cells, local = quad['cells'], quad['local']
        eta = (1 - local) * edge[cells] + local * edge[cells + 1]
        eta_r = (edge[cells + 1] - edge[cells]) / widths
        displacement = geometry['displacement']
        displacement_r = geometry['jacobian_source'] / spatial
        movement = eta + displacement * source_mode
        movement_r = eta_r + displacement_r * source_mode
        speed = displacement * row['velocity']
        speed_r = displacement_r * row['velocity']
        gradient = row['gradient'] / spatial
        gradient_change = field_r - gradient * movement_r
        values, radial = action.solver.values(action.solution, radius)
        position_value = position.values(radius)
        velocity_value, velocity_r = velocity.solver.values(velocity.solution, radius)
        time_value = metric_time.values(radius)
        trial_value = trial_time.values(radius)
        physical_measure = quad['measure'] * spatial
        alpha = coefficient_data(radius, values, radial)[0]
        changed_radius = radius + amount * movement
        changed_values = values + amount * (position_value + radial * movement)
        changed_alpha = coefficient_data(changed_radius, changed_values, radial)[0]
        changed_gradient = (gradient + amount * field_r) / (1 + amount * movement_r)
        changed_temporal = row['rate'] - speed * changed_gradient
        changed_momentum = (1 + amount * movement_r) * changed_alpha * changed_temporal
        position_density = changed_momentum.imag / 1e-25
        position_source_density = (-changed_momentum * displacement * changed_gradient).imag / 1e-25
        base = wave_packet(row, values, radial, time_value, row['rate'], row['rate_gradient'] / spatial,
            old_accel, speed, speed_r, displacement * source_accel)
        moved = wave_packet(row, values + amount * velocity_value, radial + amount * velocity_r,
            time_value + amount * trial_value, row['rate'] + amount * field,
            row['rate_gradient'] / spatial + amount * field_r, old_accel + amount * acceleration_change,
            speed + amount * movement, speed_r + amount * movement_r,
            displacement * (source_accel + amount * source_accel_change))
        source_radius = np.array([row['source']])
        source_values, source_radial = action.solver.values(action.solution, source_radius)
        source_position = position.values(source_radius)[:, 0]
        source_velocity, source_velocity_r = velocity.solver.values(velocity.solution, source_radius)
        source_time = metric_time.values(source_radius)[:, 0]
        source_trial = trial_time.values(source_radius)[:, 0]
        source_values, source_radial = source_values[:, 0], source_radial[:, 0]
        dust_position = dust_covectors(row['source'] + amount * source_mode, row['velocity'],
            source_values + amount * (source_position + source_radial * source_mode), source_radial, action.owner.source_mass)[0]
        dust_base = dust_covectors(row['source'], row['velocity'], source_values, source_radial,
            action.owner.source_mass, source_accel, source_time)
        dust_moved = dust_covectors(row['source'], row['velocity'] + amount * source_mode,
            source_values + amount * source_velocity[:, 0], source_radial + amount * source_velocity_r[:, 0],
            action.owner.source_mass, source_accel + amount * source_accel_change, source_time + amount * source_trial)
        target_data = [
            ('position', position_density, position_source_density, dust_position.imag / 1e-25, row['shape']),
            ('force_wave', moved['force_field'].imag / 1e-25, moved['force_source'].imag / 1e-25, dust_moved[1].imag / 1e-25, quad['radial'] / spatial[:, None]),
            ('momentum_rate', moved['momentum_rate'].imag / 1e-25, moved['source_momentum_rate'].imag / 1e-25, dust_moved[2].imag / 1e-25, row['shape']),
            ('base_momentum', base['momentum'], -displacement * gradient * base['momentum'], dust_base[0], row['shape']),
            ('base_force_wave', base['force_field'], base['force_source'], dust_base[1], quad['radial'] / spatial[:, None])]
        for name, density, source_density, dust, basis in target_data:
            field_covector = np.zeros(loads.rates.shape[1] - 1)
            local_covector = physical_measure[:, None] * density[:, None] * basis
            np.add.at(field_covector, indices[selected], local_covector[selected])
            source_covector = physical_measure @ source_density + dust
            output[name] += weight * np.outer(cardinal, np.r_[field_covector, source_covector])
        output['force_native'] += weight * np.outer(cardinal, native_velocity_force(native, loads, action, label, velocity))
        if index % 8 == 7:
            progress('material' + str(order) + '-label' + str(index + 1))
    output['force'] = output['force_wave'] + output['force_native']
    output['rhs'] = output['position'] - output['force']
    output['direct_trial_Euler'] = output['momentum_rate'] - output['force']
    return output
