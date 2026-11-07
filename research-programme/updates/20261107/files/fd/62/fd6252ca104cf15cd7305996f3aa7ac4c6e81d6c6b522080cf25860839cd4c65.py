import argparse
from mixed_common import *
from mixed_wave_system import MixedSystem
from relaxed_background_wave import RelaxedSource


def main(arguments):
    modest()
    folder = ROOT / 'waves' / (arguments.model + '-relaxed-source-probe')
    folder.mkdir(parents=True, exist_ok=False)
    system = MixedSystem(arguments.model, 24, 8, 'event8')
    relaxed = RelaxedSource(system)
    state, initial = system.initial()
    previous = state.copy()
    response, previous_response = np.zeros_like(state), np.zeros_like(state)
    heat = system.background(0.)['heat']
    step = system.geometry.thermal.end / arguments.steps
    moments, responses, features, residuals = [], [], [], []
    started = time.perf_counter()
    for index in range(arguments.steps + 1):
        expansion = index * step
        if index:
            mass, original, _ = system.matrices(expansion)
            baseline_operator = original + heat * system.correction(expansion)
            delta = relaxed.operator(expansion)
            operator = baseline_operator + heat ** 2 * delta
            if index == 1:
                alpha, history, delta_history = 1 / step, state / step, response / step
            else:
                alpha = 1.5 / step
                history = (2 * state - .5 * previous) / step
                delta_history = (2 * response - .5 * previous_response) / step
            new_state = sparse_linalg.splu(alpha * mass - baseline_operator).solve(mass @ history)
            right = mass @ delta_history + delta @ new_state
            new_response = sparse_linalg.splu(alpha * mass - operator).solve(right)
            residuals.append(float(linalg.norm((alpha * mass - operator) @ new_response - right) / max(linalg.norm(right), 1e-100)))
            previous, state = state, new_state
            previous_response, response = response, new_response
        if index % max(1, arguments.steps // 40) == 0:
            moments.append(expansion)
            responses.append(response.copy())
            features.append(system.features(expansion, response))
        if index and index % max(1, arguments.steps // 10) == 0:
            write_json(folder / 'progress.json', dict(state='running', step=index, elapsed=time.perf_counter() - started))
    source = ROOT / 'waves' / (arguments.model + '24-event8-3200') / 'evolution.npz'
    with np.load(source) as saved:
        original_features = saved['scaled_features'].copy()
        original_response = saved['scaled_differences'].copy()
    checks, rows = [], []
    for column, name in enumerate(['cold_density', 'baryon_density', 'photon_energy', 'neutrino_energy', 'photon_flux',
                                   'neutrino_flux', 'baryon_velocity', 'temperature', 'field1', 'field2', 'prime1', 'prime2']):
        original_amplitude = float(np.max(abs(original_features[:, column])))
        amplitude = heat * float(np.max(abs(np.asarray(features)[:, column])))
        relative = amplitude / original_amplitude if original_amplitude > 1e-35 else None
        checks.append(dict(name=name + ': relaxed background-source response at mixed response scale',
                           passed=relative < .002 if relative is not None else amplitude < 1e-35, value=relative))
        rows.append(dict(feature=name, physical_amplitude=heat * amplitude, fraction_of_mixed=relative))
    for degree in range(9):
        for name in system.names[degree]:
            section = system.mode_slice(degree, name)
            original_amplitude = float(np.max(linalg.norm(original_response[:, section], axis=1)))
            amplitude = heat * float(np.max(linalg.norm(np.asarray(responses)[:, section], axis=1)))
            relative = amplitude / original_amplitude if original_amplitude > 1e-18 else None
            checks.append(dict(name=str(degree) + name + ': relaxed source spectral response',
                               passed=relative < .002 if relative is not None else amplitude < 1e-18, value=relative))
    checks.append(dict(name='Second-order probe equation residual', passed=max(residuals) < 1e-8, value=max(residuals)))
    np.savez_compressed(folder / 'evolution.npz', expansion=moments, scaled_responses=responses, scaled_features=features,
                        physical_scale=heat ** 2, heat=heat, steps=arguments.steps)
    finish(folder, dict(checks=checks, all_checks_passed=all(row['passed'] for row in checks), count=len(checks), rows=rows,
                        scope='Relaxed background collision, boost, redshift and temperature-pressure source sensitivity. Not a complete order-chi^2 Jacobian or new Friedmann background.',
                        no_unrelaxed_residual_inserted=True, elapsed=time.perf_counter() - started), __file__,
           [ROOT / 'relaxed_background_wave.py', ROOT / 'mixed_wave_system.py', *relaxed.inputs, *system.bank.inputs,
            source, source.parent / 'status.json'])
    print(json.dumps(dict(model=arguments.model, failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', choices=['heavy', 'cold'], required=True)
    parser.add_argument('--steps', type=int, default=3200)
    main(parser.parse_args())
