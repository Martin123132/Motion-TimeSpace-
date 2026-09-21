import numpy as np
from scipy.integrate import solve_ivp


def frozen_response_matrices(model, offset):
    data = model.stencil([offset])
    radii = data['R'][0]
    fields = {key: value[0] for key, value in data['fields'].items()}
    geometric_weight = fields['N'] * fields['U'] * np.exp(fields['g'])
    factor_density = model.sampling @ (radii**2 * geometric_weight)
    mass = model.node_weights * radii**2 / geometric_weight
    stiffness = model.factors.T @ ((factor_density / model.spacing)[:, None] * model.factors)
    initial = data['chi'][0]
    velocity = np.exp(fields['g']) * data['q'][0]
    outside = np.flatnonzero((radii < model.radii[0]) | (radii > model.radii[-1]))
    if len(outside) != 1:
        raise ValueError('This first response construction requires one exterior node per translated copy.')
    exterior = int(outside[0])
    interior = np.delete(np.arange(len(radii)), exterior)
    return {'M': mass, 'K': stiffness, 'chi0': initial, 'v0': velocity, 'H': geometric_weight,
            'g': fields['g'], 'N': fields['N'], 'U': fields['U'], 'radii': radii,
            'factor_density': factor_density, 'exterior': exterior, 'interior': interior,
            'parent_Gchi': data['Gchi'][0], 'parent_q': data['q'][0]}


def free_response_control(data, horizon=.025):
    mass, stiffness, initial, velocity = [data[key] for key in ['M', 'K', 'chi0', 'v0']]
    count, exterior, interior = len(mass), data['exterior'], data['interior']
    exterior_mass = mass[exterior]
    exterior_stiffness = stiffness[exterior, exterior]
    frequency = np.sqrt(exterior_stiffness / exterior_mass)
    coupling = stiffness[exterior, interior]

    def equation(time, state):
        return np.concatenate([state[count:], -(stiffness @ state[:count]) / mass])

    solution = solve_ivp(equation, (0., horizon), np.concatenate([initial, velocity]), method='DOP853', rtol=2e-12, atol=2e-14, max_step=horizon / 32, dense_output=True)
    if not solution.success:
        raise RuntimeError(solution.message)
    times = np.linspace(0., horizon, 41)
    trajectory = solution.sol(times)
    inverse_sqrt = 1 / np.sqrt(mass)
    normalized = inverse_sqrt[:, None] * stiffness * inverse_sqrt
    eigenvalues, eigenvectors = np.linalg.eigh(normalized)
    rounding_bound = 128 * np.finfo(float).eps * np.linalg.norm(normalized, 2)
    if abs(eigenvalues[0]) > rounding_bound or eigenvalues[1] <= rounding_bound:
        raise ValueError('Expected one exact constant null mode, not an unreported unstable or extra zero mode.')
    recorded_minimum = float(eigenvalues[0])
    eigenvalues[0] = 0.
    frequencies = np.sqrt(eigenvalues)
    positions = eigenvectors.T @ (np.sqrt(mass) * initial)
    speeds = eigenvectors.T @ (np.sqrt(mass) * velocity)
    oscillation = frequencies[:, None] * times
    spectral = inverse_sqrt[:, None] * (eigenvectors @ (np.cos(oscillation) * positions[:, None] + times * np.sinc(oscillation / np.pi) * speeds[:, None]))
    gauss, weights = np.polynomial.legendre.leggauss(48)
    rebuilt = []
    memory_only = []
    for time in times:
        integration_times = time * (gauss + 1) / 2
        inside_values = solution.sol(integration_times)[interior]
        memory = -time / 2 * weights @ (np.sin(frequency * (time - integration_times)) * (coupling @ inside_values) / (exterior_mass * frequency))
        homogeneous = np.cos(frequency * time) * initial[exterior] + np.sin(frequency * time) * velocity[exterior] / frequency
        rebuilt.append(homogeneous + memory)
        memory_only.append(memory)
    rebuilt = np.asarray(rebuilt)
    total_energy = .5 * np.sum(mass[:, None] * trajectory[count:]**2, axis=0) + .5 * np.sum(trajectory[:count] * (stiffness @ trajectory[:count]), axis=0)
    position, speed = trajectory[:count], trajectory[count:]
    inside_power = -(speed[interior].T @ coupling) * position[exterior]
    exterior_power = -speed[exterior] * (coupling @ position[interior])
    cross_energy_rate = (speed[interior].T @ coupling) * position[exterior] + (position[interior].T @ coupling) * speed[exterior]
    reconstructed_traction = -coupling[:, None] * rebuilt
    actual_traction = -coupling[:, None] * position[exterior]
    row = {'frequency_in_auxiliary_frozen_clock': float(frequency), 'exterior_mass': float(exterior_mass),
           'exterior_stiffness': float(exterior_stiffness), 'spectral_ODE_error': float(abs(spectral - position).max()),
           'retarded_exterior_error': float(abs(rebuilt - position[exterior]).max()),
           'retarded_traction_error': float(abs(reconstructed_traction - actual_traction).max()),
           'energy_drift': float(abs(total_energy - total_energy[0]).max()),
           'cross_energy_power_balance_error': float(abs(inside_power + exterior_power + cross_energy_rate).max()),
           'drop_initial_reservoir_data_error': float(abs(np.asarray(memory_only) - position[exterior]).max()),
           'drop_cross_energy_power_error': float(abs(inside_power + exterior_power).max()),
           'minimum_computed_eigenvalue_before_roundoff_null_handling': recorded_minimum,
           'roundoff_null_bound': float(rounding_bound), 'positive_first_nonzero_eigenvalue': float(eigenvalues[1]),
           'constant_null_mode_residual': float(abs(stiffness @ np.ones(count)).max()), 'horizon': horizon,
           'full_geometric_evolution': False}
    arrays = {'time': times, 'trajectory': trajectory, 'spectral_position': spectral, 'rebuilt_exterior': rebuilt,
              'energy': total_energy, 'interior_traction': actual_traction,
              'memory_kernel_at_half_horizon': coupling[:, None] * coupling[None, :] * np.sin(frequency * horizon / 2) / (exterior_mass * frequency)}
    return row, arrays


def driven_response_control(data, acceleration=.05, horizon=.025):
    mass, stiffness, initial, velocity = [data[key] for key in ['M', 'K', 'chi0', 'v0']]
    exterior, interior = data['exterior'], data['interior']
    interior_mass = mass[interior]
    interior_stiffness = stiffness[np.ix_(interior, interior)]
    coupling = stiffness[interior, exterior]
    count = len(interior)

    def prescribed(time):
        return initial[exterior] + velocity[exterior] * time + .5 * acceleration * time**2

    def interior_equation(time, state):
        return np.concatenate([state[count:], -(interior_stiffness @ state[:count] + coupling * prescribed(time)) / interior_mass])

    solution = solve_ivp(interior_equation, (0., horizon), np.concatenate([initial[interior], velocity[interior]]), method='DOP853', rtol=2e-12, atol=2e-14, max_step=horizon / 32, dense_output=True)
    if not solution.success:
        raise RuntimeError(solution.message)

    def reaction(time):
        return mass[exterior] * acceleration + stiffness[exterior, exterior] * prescribed(time) + coupling @ solution.sol(time)[:count]

    def replay_equation(time, state):
        force = -(stiffness @ state[:len(mass)])
        force[exterior] += reaction(time)
        return np.concatenate([state[len(mass):], force / mass])

    replay = solve_ivp(replay_equation, (0., horizon), np.concatenate([initial, velocity]), method='DOP853', rtol=2e-12, atol=2e-14, max_step=horizon / 32, dense_output=True)
    if not replay.success:
        raise RuntimeError(replay.message)
    times = np.linspace(0., horizon, 41)
    inside = solution.sol(times)
    values = replay.sol(times)
    error = max(abs(values[exterior] - prescribed(times)).max(), abs(values[interior] - inside[:count]).max())
    position, speed = values[:len(mass)], values[len(mass):]
    energy = .5 * np.sum(mass[:, None] * speed**2, axis=0) + .5 * np.sum(position * (stiffness @ position), axis=0)
    gauss, weights = np.polynomial.legendre.leggauss(64)
    integration_times = horizon * (gauss + 1) / 2
    external_work = horizon / 2 * weights @ (reaction(integration_times) * (velocity[exterior] + acceleration * integration_times))
    action_test_times = np.linspace(.001, horizon - .001, 13)
    residual = mass[exterior] * acceleration + stiffness[exterior, exterior] * prescribed(action_test_times) + coupling @ solution.sol(action_test_times)[:count] - reaction(action_test_times)
    row = {'prescribed_auxiliary_clock_acceleration': acceleration, 'full_forced_replay_error': float(error),
           'external_work_energy_error': float(abs(energy[-1] - energy[0] - external_work)),
           'reaction_equation_error': float(abs(residual).max()), 'initial_reaction': float(reaction(0.)),
           'maximum_reaction': float(abs(reaction(times)).max()), 'prescribed_history_is_manufactured': True,
           'physical_source_history_derived': False, 'horizon': horizon}
    return row, {'time': times, 'forced_trajectory': values, 'reaction': reaction(times), 'energy': energy, 'prescribed_exterior': prescribed(times)}


def physical_outer_acceleration(model, clock_rate, target):
    data = model.stencil([0.])
    radius = model.radii[-1]
    fields = model.metric(np.array([radius]))
    root, lapse = fields['U'][0], fields['N'][0]
    clock = lapse / root
    current = model.direct_flux(radius, order=48)
    mass_rate = -model.coupling * root * current / lapse
    scalar_velocity = data['q'][0, -1]
    momentum_rate = data['p1'][0, -1]
    logarithmic_lapse_rate = clock_rate / clock - mass_rate / (radius * root**2)
    acceleration = (clock_rate / clock - 2 * mass_rate / (radius * root**2)) * scalar_velocity + lapse * root * momentum_rate / radius**2
    defect = target - acceleration
    required_reaction = model.node_weights[-1] * radius**2 * defect / (lapse * root)
    return {'free_outer_acceleration': float(acceleration), 'prescribed_outer_acceleration': float(target),
            'acceleration_defect': float(defect), 'clock_rate': float(clock_rate), 'clock_value': float(clock),
            'outer_mass_rate': float(mass_rate), 'outer_scalar_velocity': float(scalar_velocity),
            'free_outer_momentum_rate': float(momentum_rate), 'logarithmic_outer_lapse_rate': float(logarithmic_lapse_rate),
            'required_generalized_force_trace_not_installed': float(required_reaction),
            'free_boundary_second_order_pass': bool(abs(defect) < 1e-10),
            'point_force_adopted': False, 'full_C2_evaluated': False}
