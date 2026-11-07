import argparse
from evolve_collision import saved_mode, synthetic_mode, equilibrium
from step_common import *


def run(label, name, points, polar, fixture, maximum_step, growth, end_depth, cold):
    modest()
    folder = ROOT / 'runs' / name
    folder.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    write_json(folder / 'status.json', dict(state='running', pid=os.getpid(), model=label, fixture=fixture))
    background = inherited.inherited.ThermalBackground(label)
    scale = 1e-5 if fixture == 'saved' else 1e-6
    local = background.at(math.log(scale / background.start_scale))
    base = background.parent.at(local['moment'])
    chi = background.chi
    inertia = base['baryon'] / base['photon'] + 5 * chi / 3
    theta = 0. if cold else local['thermal_parameter']
    model = CollisionStep(points, polar, theta, chi, inertia)
    if not cold:
        largest = float(spla.eigsh(model.symmetric_photon(), k=1, which='LA', return_eigenvectors=False, tol=1e-8)[0])
        assert largest < 1e-10, largest
    else:
        largest = 0.
    initializer = saved_mode if fixture == 'saved' else lambda label, model: synthetic_mode(model)
    total, temperature_total, velocity_total, inputs, initial_details = initializer(label, model)
    reference = equilibrium(model, model.invariants(total, temperature_total, velocity_total))
    potential, temperature, velocity = total - reference[0], temperature_total - reference[1], velocity_total - reference[2]
    initial = potential.copy()
    initial_temperature, initial_velocity = temperature, velocity
    invariants = model.invariants(potential, temperature, velocity)
    initial_entropy = model.entropy(potential, temperature, velocity)
    norm_scale = math.sqrt(2 * initial_entropy)
    duration = (6. if fixture == 'saved' else 4 / local['thermal_parameter']) if end_depth is None else end_depth
    step_cap = (.01 if fixture == 'saved' else duration / 200) if maximum_step is None else maximum_step
    proposal = min(step_cap, .02 * chi / (4 * local['thermal_parameter']))
    sample_times = np.unique(np.r_[0., np.geomspace(proposal, min(.001, duration), 30), np.linspace(min(.001, duration), duration, 101)])
    depth, iterations = 0., 0
    history, spectra = [], []
    max_invariant_error, max_equation_error, max_entropy_increase = 0., 0., 0.
    previous_entropy = initial_entropy
    def record():
        entropy = model.entropy(potential, temperature, velocity)
        history.append(dict(optical_depth=depth, entropy_defect=float(entropy),
            temperature_real=float((temperature + reference[1]).real), temperature_imaginary=float((temperature + reference[1]).imag),
            velocity_real=float((velocity + reference[2]).real), velocity_imaginary=float((velocity + reference[2]).imag),
            temperature_defect_real=float(temperature.real), temperature_defect_imaginary=float(temperature.imag),
            velocity_defect_real=float(velocity.real), velocity_defect_imaginary=float(velocity.imag)))
        spectra.append(potential.copy())
    record()
    for target in sample_times[1:]:
        while depth < target - 1e-13 * max(duration, 1):
            step = min(proposal, step_cap, target - depth)
            source = model.source(potential, temperature, velocity)
            alpha = 2 / step
            updated = model.solve(alpha, alpha * potential + source,
                alpha * temperature - (model.energy @ source) / chi,
                alpha * velocity - (model.flux @ source) / inertia)
            updated_source = model.source(*updated)
            residual = updated[0] - potential - step * (source + updated_source) / 2
            equation_error = math.sqrt(float(np.vdot(residual, model.entropy_metric * residual).real)) / norm_scale
            max_equation_error = max(max_equation_error, equation_error)
            potential, temperature, velocity = updated
            error = float(np.max(abs(model.invariants(potential, temperature, velocity) - invariants)) / norm_scale)
            max_invariant_error = max(max_invariant_error, error)
            entropy = model.entropy(potential, temperature, velocity)
            max_entropy_increase = max(max_entropy_increase, float((entropy - previous_entropy) / initial_entropy))
            previous_entropy = entropy
            depth += step
            proposal = min(step_cap, proposal * growth)
            iterations += 1
        depth = target
        record()
        if len(history) % 30 == 0:
            write_json(folder / 'progress.json', dict(state='running', optical_depth=depth, target=duration,
                iterations=iterations, elapsed_seconds=time.perf_counter() - started))
            print(json.dumps(dict(run=name, optical_depth=depth, iterations=iterations)), flush=True)
    checks = [dict(name='Combined invariants relative to evolving defect, not large equilibrium',
                   passed=max_invariant_error < 1e-9, value=max_invariant_error, gate=1e-9),
              dict(name='Implicit midpoint equation relative to evolving defect',
                   passed=max_equation_error < 1e-9, value=max_equation_error, gate=1e-9),
              dict(name='Coupled entropy defect never increases', passed=max_entropy_increase < 1e-9,
                   value=max_entropy_increase, gate=1e-9),
              dict(name='Finite spectral and plasma response',
                   passed=bool(np.isfinite(potential).all() and np.isfinite(temperature) and np.isfinite(velocity)))]
    if fixture == 'saved':
        checks.append(dict(name='Retained parent scalar polarization reconstructed',
                           passed=initial_details['polarization_reconstruction_error'] < .001,
                           value=initial_details['polarization_reconstruction_error'], gate=.001))
    np.savez_compressed(folder / 'evolution.npz', frequency=model.grid.frequency, cosine=model.angular.cosine,
        mass=model.grid.mass, angular_weights=model.angular.weights, initial_defect=initial, final_defect=potential,
        initial_temperature_defect=initial_temperature, initial_velocity_defect=initial_velocity,
        temperature_defect=temperature, velocity_defect=velocity, equilibrium=reference[0],
        equilibrium_temperature=reference[1], equilibrium_velocity=reference[2],
        entropy_metric=model.entropy_metric, invariants=invariants, optical_depth=sample_times,
        spectrum_history=spectra, heat_capacity=chi, inertia=inertia, theta=theta)
    inputs.extend([ROOT / 'evolve_collision.py', background.parent.source])
    finish(folder, dict(model=label, run_name=name, fixture=fixture, points=points, polar_points=polar,
        scale=scale, theta=theta, heat_capacity=chi, inertia=inertia, cold_control=cold,
        checks=checks, all_checks_passed=all(row['passed'] for row in checks), history=history,
        initial_details=initial_details, photon_largest_eigenvalue=largest,
        duration_optical_depth=duration, maximum_step=step_cap, growth=growth, iterations=iterations,
        final_to_initial_entropy_defect=float(previous_entropy / initial_entropy),
        frozen_background_fractional_Hubble_duration=float(duration / (base['opacity'] / base['hubble'])) if fixture == 'saved' else None,
        elapsed_seconds=time.perf_counter() - started, exact_equilibrium_subtracted_not_refitted_each_step=True,
        coupled_temperature_evolved=True, source_substep_not_full_cosmological_evolution=True,
        scalar_axisymmetric_validation_not_full_nonparallel_evolution=True), __file__, inputs)
    print(json.dumps(dict(run=name, checks=checks, iterations=iterations,
                         entropy_ratio=previous_entropy / initial_entropy, elapsed_seconds=time.perf_counter() - started)), flush=True)


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
