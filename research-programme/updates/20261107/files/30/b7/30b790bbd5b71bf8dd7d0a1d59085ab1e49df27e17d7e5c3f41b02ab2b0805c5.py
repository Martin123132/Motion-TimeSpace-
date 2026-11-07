import argparse
from step_common import *


def saved_mode(label, model):
    path = WAVES / 'runs' / (label + '-sixteenth') / 'evolution.npz'
    with np.load(path, allow_pickle=False) as saved:
        maximum = int(saved['angular_maximum'])
        state = saved['final_state'][0]
    angular = inherited.AngularKernel(maximum + 4, 2 * (maximum + 4))
    photon = state[26:26 + 9 * angular.count].reshape(angular.count, 3, 3)
    axis = np.array([1., 0., 0.])
    cosine = angular.directions @ axis
    sine = np.sqrt(1 - cosine ** 2)
    meridian = (cosine[:, None] * angular.directions - axis) / sine[:, None]
    azimuth = np.cross(axis, angular.directions) / sine[:, None]
    polarization = np.einsum('ni,nj->nij', meridian, meridian) - np.einsum('ni,nj->nij', azimuth, azimuth)
    intensity = np.trace(photon, axis1=1, axis2=2)
    polarized = np.einsum('nij,nij->n', photon, polarization)
    target = model.angular.cosine
    intensity_coefficients = [(2 * degree + 1) * np.dot(angular.weights, intensity * special.eval_legendre(degree, cosine))
                              for degree in range(9)]
    polarization_coefficients = [(2 * degree + 1) * math.factorial(degree - 2) / math.factorial(degree + 2)
                                 * np.dot(angular.weights, polarized * special.lpmv(2, degree, cosine)) for degree in range(2, 9)]
    intensity_target = sum(value * special.eval_legendre(degree, target) for degree, value in enumerate(intensity_coefficients))
    polarization_target = sum(value * special.lpmv(2, degree, target) for degree, value in zip(range(2, 9), polarization_coefficients))
    reconstructed_intensity = sum(value * special.eval_legendre(degree, cosine) for degree, value in enumerate(intensity_coefficients))
    reconstructed_polarization = sum(value * special.lpmv(2, degree, cosine) for degree, value in zip(range(2, 9), polarization_coefficients))
    intensity_error = float(np.linalg.norm(reconstructed_intensity - intensity) / np.linalg.norm(intensity))
    polarization_error = float(np.linalg.norm(reconstructed_polarization - polarized) / np.linalg.norm(polarized))
    potential = np.kron(model.grid.frequency / 2, np.r_[intensity_target, polarization_target])
    temperature = intensity_coefficients[0] / 4
    velocity = state[23]
    return potential, temperature, velocity, [path], dict(intensity_reconstruction_error=intensity_error,
        polarization_reconstruction_error=polarization_error,
        temperature_initial_condition='Initial local adiabatic temperature perturbation; subsequently evolved, not constrained.',
        same_scalar_mode_rotated_to_z=True)


def synthetic_mode(model):
    frequency = model.grid.frequency
    cosine = model.angular.cosine
    spectral = frequency * np.exp(-frequency / 3) * np.sin(np.log(frequency + .2))
    intensity = (2 * (.02 * frequency + .003 * spectral)[:, None]
                 + .002 * frequency[:, None] * cosine
                 + .002 * frequency[:, None] * special.eval_legendre(2, cosine))
    polarization = .0006 * frequency[:, None] * (1 - cosine ** 2)
    potential = np.concatenate([intensity, polarization], axis=1).ravel().astype(complex)
    return potential, .01 + 0j, 0j, [], dict(non_equilibrium_static_plasma_benchmark=True,
        not_a_cosmological_frozen_background_approximation_over_the_full_duration=True)


def equilibrium(model, invariants):
    chemical, temperature, velocity = model.chemical_equilibrium, model.temperature_equilibrium, model.velocity_equilibrium
    matrix = np.column_stack([model.invariants(chemical, 0., 0.), model.invariants(temperature, 1., 0.), model.invariants(velocity, 0., 1.)])
    coefficients = np.linalg.solve(matrix, invariants)
    return chemical * coefficients[0] + temperature * coefficients[1] + velocity * coefficients[2], coefficients[1], coefficients[2]


def run(label, name, points, polar, fixture, maximum_step, growth, end_depth, cold):
    modest()
    folder = ROOT / 'runs' / name
    folder.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    write_json(folder / 'status.json', dict(state='running', pid=os.getpid(), model=label, points=points, fixture=fixture))
    background = inherited.inherited.ThermalBackground(label)
    scale = 1e-5 if fixture == 'saved' else 1e-6
    local = background.at(math.log(scale / background.start_scale))
    base = background.parent.at(local['moment'])
    chi = background.chi
    inertia = base['baryon'] / base['photon'] + 5 * chi / 3
    theta = 0. if cold else local['thermal_parameter']
    model = CollisionStep(points, polar, theta, chi, inertia)
    if cold:
        symmetric_angular = np.diag(np.sqrt(model.angular.metric)) @ (model.angular.scatter - np.eye(model.dimension)) @ np.diag(1 / np.sqrt(model.angular.metric))
        largest = float(max(np.linalg.eigvalsh(symmetric_angular)))
    else:
        largest = float(spla.eigsh(model.symmetric_photon(), k=1, which='LA', return_eigenvectors=False, tol=1e-8)[0])
    if largest > 1e-10:
        write_json(folder / 'status.json', dict(state='failed', reason='Collision entropy has a growing grid mode; no evolution launched.',
                                              largest_eigenvalue=largest))
        raise RuntimeError('Unstable frequency/angular grid')
    if fixture == 'saved':
        potential, temperature, velocity, inputs, initial_details = saved_mode(label, model)
    else:
        potential, temperature, velocity, inputs, initial_details = synthetic_mode(model)
    inputs.append(background.parent.source)
    initial = potential.copy()
    initial_temperature, initial_velocity = temperature, velocity
    invariants = model.invariants(potential, temperature, velocity)
    equilibrium_state = equilibrium(model, invariants)
    norm_scale = math.sqrt(2 * model.entropy(*equilibrium_state))
    initial_defect = model.entropy(potential - equilibrium_state[0], temperature - equilibrium_state[1], velocity - equilibrium_state[2])
    duration = (6. if fixture == 'saved' else 4 / local['thermal_parameter']) if end_depth is None else end_depth
    step_cap = (.01 if fixture == 'saved' else duration / 200) if maximum_step is None else maximum_step
    depth = 0.
    step = min(step_cap, .02 * chi / (4 * local['thermal_parameter']))
    history, spectra = [], []
    max_invariant_error, max_equation_error, max_entropy_increase = 0., 0., 0.
    previous_entropy = model.entropy(potential - equilibrium_state[0], temperature - equilibrium_state[1], velocity - equilibrium_state[2])
    sample_times = np.unique(np.r_[0., np.geomspace(step, min(.001, duration), 30), np.linspace(min(.001, duration), duration, 101)])
    sample_index = 0
    iterations = 0
    while True:
        while sample_index < len(sample_times) and depth >= sample_times[sample_index] - 1e-13 * max(duration, 1):
            defect = model.entropy(potential - equilibrium_state[0], temperature - equilibrium_state[1], velocity - equilibrium_state[2])
            source = model.source(potential, temperature, velocity)
            history.append(dict(optical_depth=depth, temperature_real=float(temperature.real), temperature_imaginary=float(temperature.imag),
                velocity_real=float(velocity.real), velocity_imaginary=float(velocity.imag),
                photon_energy_real=float((model.energy @ potential).real), photon_energy_imaginary=float((model.energy @ potential).imag),
                photon_flux_real=float((model.flux @ potential).real), photon_flux_imaginary=float((model.flux @ potential).imag),
                entropy_defect=float(defect), instantaneous_heat_real=float((model.energy @ source).real),
                instantaneous_heat_imaginary=float((model.energy @ source).imag)))
            spectra.append(potential.copy())
            sample_index += 1
        if depth >= duration - 1e-13 * max(duration, 1):
            break
        step = min(step, step_cap, duration - depth, sample_times[sample_index] - depth)
        source = model.source(potential, temperature, velocity)
        alpha = 2 / step
        updated = model.solve(alpha, alpha * potential + source,
                              alpha * temperature - (model.energy @ source) / chi,
                              alpha * velocity - (model.flux @ source) / inertia)
        updated_source = model.source(*updated)
        equation_residual = updated[0] - potential - step * (source + updated_source) / 2
        equation_error = math.sqrt(float(np.vdot(equation_residual, model.entropy_metric * equation_residual).real)) / max(norm_scale, 1e-100)
        max_equation_error = max(max_equation_error, equation_error)
        potential, temperature, velocity = updated
        new_invariants = model.invariants(potential, temperature, velocity)
        invariant_error = float(np.max(abs(new_invariants - invariants)) / max(norm_scale, 1e-100))
        max_invariant_error = max(max_invariant_error, invariant_error)
        entropy = model.entropy(potential - equilibrium_state[0], temperature - equilibrium_state[1], velocity - equilibrium_state[2])
        max_entropy_increase = max(max_entropy_increase, float((entropy - previous_entropy) / max(initial_defect, 1e-100)))
        previous_entropy = entropy
        depth += step
        step = min(step_cap, step * growth)
        iterations += 1
        if iterations % 500 == 0:
            write_json(folder / 'progress.json', dict(state='running', iterations=iterations, optical_depth=depth,
                                                     target=duration, elapsed_seconds=time.perf_counter() - started))
            print(json.dumps(dict(run=name, optical_depth=depth, iterations=iterations)), flush=True)
    checks = [dict(name='Combined species energy/momentum and photon number invariants', passed=max_invariant_error < 1e-9,
                   value=max_invariant_error, gate=1e-9),
              dict(name='Implicit midpoint photon equation residual', passed=max_equation_error < 1e-9,
                   value=max_equation_error, gate=1e-9),
              dict(name='Coupled entropy defect does not increase', passed=max_entropy_increase < 1e-9,
                   value=max_entropy_increase, gate=1e-9),
              dict(name='Finite spectral/plasma state', passed=bool(np.isfinite(potential).all() and np.isfinite(temperature) and np.isfinite(velocity)))]
    if fixture == 'saved':
        checks.append(dict(name='Parent scalar-mode polarization reconstruction',
                           passed=initial_details['polarization_reconstruction_error'] < .001,
                           value=initial_details['polarization_reconstruction_error'], gate=.001))
    np.savez_compressed(folder / 'evolution.npz', frequency=model.grid.frequency, cosine=model.angular.cosine,
        mass=model.grid.mass, angular_weights=model.angular.weights, initial=initial, final=potential,
        initial_temperature=initial_temperature, initial_velocity=initial_velocity, temperature=temperature, velocity=velocity,
        equilibrium=equilibrium_state[0], equilibrium_temperature=equilibrium_state[1], equilibrium_velocity=equilibrium_state[2],
        entropy_metric=model.entropy_metric, invariants=invariants, optical_depth=[row['optical_depth'] for row in history],
        spectrum_history=spectra, heat_capacity=chi, inertia=inertia, theta=theta)
    finish(folder, dict(model=label, run_name=name, fixture=fixture, points=points, polar_points=polar,
        scale=scale, heat_capacity=chi, inertia=inertia, theta=theta, cold_control=cold,
        checks=checks, all_checks_passed=all(row['passed'] for row in checks), history=history,
        duration_optical_depth=duration, maximum_step=step_cap, growth=growth, iterations=iterations,
        initial_details=initial_details, photon_largest_eigenvalue=largest,
        final_to_initial_entropy_defect=float(previous_entropy / initial_defect),
        frozen_background_fractional_Hubble_duration=float(duration / (base['opacity'] / base['hubble'])) if fixture == 'saved' else None,
        elapsed_seconds=time.perf_counter() - started, coupled_temperature_not_algebraically_fixed=True,
        collision_substep_not_full_cosmological_evolution=True, axisymmetric_scalar_test_not_full_nonparallel_evolution=True), __file__, inputs)
    print(json.dumps(dict(run=name, checks=checks, iterations=iterations, entropy_ratio=previous_entropy / initial_defect,
                         elapsed_seconds=time.perf_counter() - started)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', choices=['heavy', 'cold'], default='heavy')
    parser.add_argument('--name', required=True)
    parser.add_argument('--points', type=int, default=96)
    parser.add_argument('--polar', type=int, default=10)
    parser.add_argument('--fixture', choices=['saved', 'synthetic'], default='saved')
    parser.add_argument('--step', type=float)
    parser.add_argument('--growth', type=float, default=1.05)
    parser.add_argument('--depth', type=float)
    parser.add_argument('--cold', action='store_true')
    arguments = parser.parse_args()
    run(arguments.model, arguments.name, arguments.points, arguments.polar, arguments.fixture,
        arguments.step, arguments.growth, arguments.depth, arguments.cold)
