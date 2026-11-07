from gravity228 import *
from launch228 import windows_modest


def identity():
    names = ['results/gravity.json', 'results/derivative-check.json', 'results/heavy-gravity.npz',
             'results/cold-gravity.npz', 'results/heavy-stress.npz', 'results/cold-stress.npz',
             'precision228.py', 'PRECISION-CHECK.md']
    return {name: digest(ROOT / name) for name in names}


def number(value):
    return mp.mpf(float(value))


def probe(system, coordinate, response, step):
    background = system.background
    state = state_at_scale(background, background.start_scale * math.exp(coordinate))
    coordinate_mp, width = number(coordinate), mp.mpf(str(step))
    scale = number(background.start_scale) * mp.exp(coordinate_mp)
    fields = list(map(number, state['fields']))
    prime = list(map(number, state['prime']))
    masses = list(map(number, system.mass2))
    radiation, matter, photons = map(number, (background.parent.radiation,
        background.parent.baryons + background.parent.cold, background.parent.photons))
    def parent_density(local_scale, local_fields, local_prime):
        return radiation / local_scale**4 + matter / local_scale**3 + sum(local_prime[index]**2 / local_scale**2 + masses[index] * local_fields[index]**2 for index in range(2)) / 2
    rho0 = parent_density(scale, fields, prime)
    pressure0 = radiation / (3 * scale**4) + sum(prime[index]**2 / scale**2 - masses[index] * fields[index]**2 for index in range(2)) / 2
    hubble = scale * mp.sqrt(rho0 / 3)
    field_s = [value / hubble for value in prime]
    prime_s = [-2 * prime[index] - scale**2 * masses[index] * fields[index] / hubble for index in range(2)]
    interval = int(np.clip(np.searchsorted(system.energy.x, coordinate, side='right') - 1, 0, len(system.energy.x) - 2))
    offset = coordinate_mp - number(system.energy.x[interval])
    coefficients = list(map(number, system.energy.c[:, interval]))
    initial_energy = number(system.initial_energy)
    def energy(local_offset):
        return ((coefficients[0] * local_offset + coefficients[1]) * local_offset + coefficients[2]) * local_offset + coefficients[3]
    def primitive(local_offset):
        return coefficients[0] * local_offset**4 / 4 + coefficients[1] * local_offset**3 / 3 + coefficients[2] * local_offset**2 / 2 + coefficients[3] * local_offset
    eos_density0 = number(system.sources(coordinate)[0][1])
    def shapes(shift):
        return [1 - coordinate_mp - shift,
            eos_density0 + (primitive(offset + shift) - primitive(offset)) / initial_energy,
            2 - mp.exp(-coordinate_mp - shift)]
    slopes = [-mp.mpf(1), energy(offset) / initial_energy, mp.exp(-coordinate_mp)]
    source0 = shapes(mp.mpf(0))
    maximum = [mp.mpf(0), mp.mpf(0)]
    for column in range(3):
        delta_fields = [number(response[index, column]) for index in range(2)]
        delta_prime = [number(response[index + 2, column]) for index in range(2)]
        kinetic = sum(prime[index] * delta_prime[index] for index in range(2)) / scale**2
        potential = sum(masses[index] * fields[index] * delta_fields[index] for index in range(2))
        density = photons / scale**4 * source0[column] + kinetic + potential
        pressure = photons / scale**4 * (source0[column] - slopes[column]) / 3 + kinetic - potential
        fraction = density / (2 * rho0)
        delta_field_s = [(delta_prime[index] - prime[index] * fraction) / hubble for index in range(2)]
        delta_prime_s = [-2 * delta_prime[index] - scale**2 * masses[index] * delta_fields[index] / hubble + scale**2 * masses[index] * fields[index] * fraction / hubble for index in range(2)]
        densities, fractions = [], []
        for shift in (width, -width):
            local_scale = scale * mp.exp(shift)
            local_fields = [fields[index] + shift * field_s[index] for index in range(2)]
            local_prime = [prime[index] + shift * prime_s[index] for index in range(2)]
            local_delta_fields = [delta_fields[index] + shift * delta_field_s[index] for index in range(2)]
            local_delta_prime = [delta_prime[index] + shift * delta_prime_s[index] for index in range(2)]
            local_density = photons / local_scale**4 * shapes(shift)[column]
            local_density += sum(local_prime[index] * local_delta_prime[index] / local_scale**2 + masses[index] * local_fields[index] * local_delta_fields[index] for index in range(2))
            densities.append(local_density)
            fractions.append(local_density / (2 * parent_density(local_scale, local_fields, local_prime)))
        numerical_density = (densities[0] - densities[1]) / (2 * width)
        residual = abs(numerical_density + 3 * (density + pressure)) / (abs(numerical_density) + 3 * abs(density + pressure))
        maximum[0] = max(maximum[0], residual)
        numerical_fraction = (fractions[0] - fractions[1]) / (2 * width)
        expected = -mp.mpf('1.5') * (pressure - pressure0 * density / rho0) / rho0
        residual = abs(numerical_fraction - expected) / (abs(numerical_fraction) + abs(expected))
        maximum[1] = max(maximum[1], residual)
    return list(map(float, maximum))


def evaluate():
    windows_modest()
    protocol()
    assert read(ROOT / 'precision-configuration.json')['input_hashes'] == identity()
    mp.mp.dps = 80
    inputs = read(ROOT / 'results/gravity-inputs.json')
    rows, checks = [], []
    for model in ('heavy', 'cold'):
        background, mixture = load_background(model, inputs)
        with np.load(ROOT / f'results/{model}-stress.npz') as saved:
            system = Response(background, dict(saved))
        with np.load(ROOT / f'results/{model}-gravity.npz') as saved:
            samples, states = saved['expansion'], saved['response']
        values = []
        for step in (1e-5, 5e-6, 2.5e-6, 1.25e-6):
            residuals = np.array([probe(system, float(coordinate), response, step) for coordinate, response in zip(samples[1:-1], states[1:-1])])
            values.append(dict(step=step, continuity=float(np.max(residuals[:, 0])), raychaudhuri=float(np.max(residuals[:, 1]))))
        for key in ('continuity', 'raychaudhuri'):
            check(checks, model + ': high-precision finest ' + key, values[-1][key], 1e-8)
            for index in range(1, len(values)):
                check(checks, model + ': high-precision convergence ' + key + ':' + str(index), values[index][key] / values[index - 1][key], .5)
        rows.append(dict(model=model, probes=values))
        print(json.dumps(rows[-1]), flush=True)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    report = dict(stage=228, state='complete', finished_at=now(), checks=checks, models=rows,
        qualified=all(row['passed'] for row in checks), failed=[row for row in checks if not row['passed']],
        scope='Independent local differential-equation tangent probe; no new history evolution')
    assert not (ROOT / 'results/precision-check.json').exists()
    write(ROOT / 'results/precision-check.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'], qualified=report['qualified'])), flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'freeze':
        assert not (ROOT / 'precision-configuration.json').exists()
        write(ROOT / 'precision-configuration.json', dict(frozen_at=now(), input_hashes=identity(),
            digits=80, finest_gate=1e-8, successive_error_ratio=.5))
        print('Higher-precision derivative check frozen', flush=True)
    elif sys.argv[1] == 'evaluate':
        evaluate()
    else:
        raise ValueError(sys.argv[1])
