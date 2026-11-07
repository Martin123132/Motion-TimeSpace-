from gravity228 import *
from launch228 import windows_modest


def identity():
    names = ['results/gravity.json', 'results/thermodynamics-reviewed.json',
             'results/heavy-gravity.npz', 'results/cold-gravity.npz',
             'results/heavy-stress.npz', 'results/cold-stress.npz', 'DERIVATIVE-CHECK.md', 'derivative228.py']
    return {name: digest(ROOT / name) for name in names}


def evaluate():
    windows_modest()
    protocol()
    assert read(ROOT / 'derivative-configuration.json')['input_hashes'] == identity()
    original = read(ROOT / 'results/gravity.json')
    assert not original['qualified'] and len(original['failed']) == 3
    inputs = read(ROOT / 'results/gravity-inputs.json')
    checks, rows = [], []
    for model in ('heavy', 'cold'):
        background, mixture = load_background(model, inputs)
        with np.load(ROOT / f'results/{model}-stress.npz') as saved:
            system = Response(background, dict(saved))
        with np.load(ROOT / f'results/{model}-gravity.npz') as saved:
            samples, states = saved['expansion'], saved['response']
        analytic_ward, analytic_ray = [], []
        differences = {step: [[], []] for step in (1e-5, 5e-6, 2.5e-6, 1.25e-6)}
        for coordinate, response in zip(samples[1:-1], states[1:-1]):
            derivative = system.rhs(float(coordinate), response.ravel()).reshape(6, 3)
            state, density, pressure, fraction = system.stress(float(coordinate), response)
            scale, hubble = state['scale'], state['hubble']
            field_s = state['prime'] / hubble
            prime_s = -2 * state['prime'] - scale**2 * system.mass2 * state['fields'] / hubble
            density_shapes, pressure_shapes = system.sources(float(coordinate))
            slopes = np.array([-1., system.energy(coordinate) / system.initial_energy, math.exp(-coordinate)])
            density_s = state['photon'] * (slopes - 4 * density_shapes)
            density_s += (prime_s @ response[2:4] + state['prime'] @ derivative[2:4] - 2 * state['prime'] @ response[2:4]) / scale**2
            density_s += (system.mass2 * field_s) @ response[:2] + (system.mass2 * state['fields']) @ derivative[:2]
            rho0 = 3 * hubble**2 / scale**2
            pressure0 = (state['photon'] + state['neutrino']) / 3 + np.sum(state['prime']**2 / scale**2 - system.mass2 * state['fields']**2) / 2
            analytic_ward.append(abs(density_s + 3 * (density + pressure)) / np.maximum(abs(density_s) + 3 * abs(density + pressure), 1e-100))
            exact_rate = density_s / (2 * rho0) + 3 * fraction * (1 + pressure0 / rho0)
            predicted_rate = -1.5 * (pressure - pressure0 * density / rho0) / rho0
            analytic_ray.append(abs(exact_rate - predicted_rate) / np.maximum(abs(exact_rate) + abs(predicted_rate), 1e-100))
            for step, values in differences.items():
                plus = system.stress(float(coordinate + step), response + step * derivative)
                minus = system.stress(float(coordinate - step), response - step * derivative)
                numerical = (plus[1] - minus[1]) / (2 * step)
                values[0].append(abs(numerical + 3 * (density + pressure)) / np.maximum(abs(numerical) + 3 * abs(density + pressure), 1e-100))
                numerical_rate = (plus[3] - minus[3]) / (2 * step)
                values[1].append(abs(numerical_rate - predicted_rate) / np.maximum(abs(numerical_rate) + abs(predicted_rate), 1e-100))
        check(checks, model + ': actual-equation stress derivative', np.max(analytic_ward), 1e-10)
        check(checks, model + ': actual-equation Raychaudhuri derivative', np.max(analytic_ray), 1e-10)
        values = []
        for step, probes in differences.items():
            values.append(dict(step=step, maximum_continuity=float(np.max(probes[0])), maximum_raychaudhuri=float(np.max(probes[1])),
                continuity_by_source=np.max(probes[0], axis=0).tolist(), raychaudhuri_by_source=np.max(probes[1], axis=0).tolist()))
        for key in ('maximum_continuity', 'maximum_raychaudhuri'):
            check(checks, model + ': finest derivative ' + key, values[-1][key], 1e-8)
            if values[0][key] > 1e-8:
                check(checks, model + ': first halving reduces failed derivative ' + key, values[1][key] / values[0][key], .5)
        rows.append(dict(model=model, probes=values))
        print(json.dumps(rows[-1]), flush=True)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    report = dict(stage=228, state='complete', finished_at=now(), checks=checks, models=rows,
        qualified=all(row['passed'] for row in checks), failed=[row for row in checks if not row['passed']],
        original_failed_report_sha256=digest(ROOT / 'results/gravity.json'),
        source_and_evolution_unchanged=True, identity_gate_unchanged=True)
    assert not (ROOT / 'results/derivative-check.json').exists()
    write(ROOT / 'results/derivative-check.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'], qualified=report['qualified'])), flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'freeze':
        assert not (ROOT / 'derivative-configuration.json').exists()
        write(ROOT / 'derivative-configuration.json', dict(frozen_at=now(), input_hashes=identity(),
              probe_steps=[1e-5, 5e-6, 2.5e-6, 1.25e-6], numeric_gate=1e-8, analytic_gate=1e-10, first_halving_ratio=.5))
        print('Derivative supplement frozen', flush=True)
    elif sys.argv[1] == 'evaluate':
        evaluate()
    else:
        raise ValueError(sys.argv[1])
