from run228 import *


def state_at_scale(background, scale):
    moment = background.parent.time_at(scale)
    for iteration in range(3):
        state = background.parent.at(moment)
        moment -= (state['scale'] - scale) / (state['scale'] * state['hubble'])
    return background.parent.at(moment)


class Response:
    def __init__(self, background, packet):
        self.background = background
        self.mass2 = background.parent.masses**2
        self.energy = interpolate.CubicSpline(packet['expansion'], packet['delta_A'])
        self.primitive = self.energy.antiderivative()
        self.initial_energy = float(packet['delta_A'][0])
        self.physical_amplitudes = np.array([background.chi, background.chi * self.initial_energy,
                                             background.chi * float(packet['D0'])])

    def sources(self, coordinate):
        density = np.array([1 - coordinate,
            1 + (self.primitive(coordinate) - self.primitive(0)) / self.initial_energy,
            2 - math.exp(-coordinate)])
        slope = np.array([-1., self.energy(coordinate) / self.initial_energy, math.exp(-coordinate)])
        return density, (density - slope) / 3

    def stress(self, coordinate, response):
        scale = self.background.start_scale * math.exp(coordinate)
        state = state_at_scale(self.background, scale)
        kinetic = state['prime'] @ response[2:4] / scale**2
        potential = (self.mass2 * state['fields']) @ response[:2]
        density_shape, pressure_shape = self.sources(coordinate)
        density = state['photon'] * density_shape + kinetic + potential
        pressure = state['photon'] * pressure_shape + kinetic - potential
        fraction = density * scale**2 / (6 * state['hubble']**2)
        return state, density, pressure, fraction

    def rhs(self, coordinate, flattened):
        response = flattened.reshape(6, 3)
        state, density, pressure, fraction = self.stress(coordinate, response)
        scale, hubble = state['scale'], state['hubble']
        field = response[2:4] / hubble - state['prime'][:, None] * fraction / hubble
        prime = -2 * response[2:4] - (scale**2 * self.mass2 / hubble)[:, None] * response[:2] + (scale**2 * self.mass2 * state['fields'] / hubble)[:, None] * fraction
        return np.vstack([field, prime, -fraction / hubble, -scale * fraction / hubble]).ravel()

    def solve(self, max_step):
        result = integrate.solve_ivp(self.rhs, (0, self.background.end), np.zeros(18),
            method='DOP853', rtol=3e-11, atol=1e-27, max_step=max_step, dense_output=True)
        assert result.success
        return result

    def full_variation(self, amplitude):
        parent = self.background.parent
        initial = state_at_scale(self.background, self.background.start_scale)
        def hubble(coordinate, state):
            scale = self.background.start_scale * math.exp(coordinate)
            density = parent.radiation / scale**4 + (parent.baryons + parent.cold) / scale**3 + np.sum(state[2:4]**2 / scale**2 + self.mass2 * state[:2]**2) / 2 + amplitude * parent.photons / scale**4 * self.sources(coordinate)[0][1]
            assert density > 0
            return scale * math.sqrt(density / 3)
        def rhs(coordinate, state):
            scale = self.background.start_scale * math.exp(coordinate)
            rate = hubble(coordinate, state)
            return np.r_[state[2:4] / rate, -2 * state[2:4] - scale**2 * self.mass2 * state[:2] / rate,
                          1 / rate, scale / rate]
        result = integrate.solve_ivp(rhs, (0, self.background.end), np.r_[initial['fields'], initial['prime'], 0., 0.],
            method='DOP853', rtol=3e-12, atol=1e-28, max_step=.01, dense_output=True)
        assert result.success
        return result, hubble


def main():
    modest()
    protocol()
    source_report = read(ROOT / 'results/thermodynamics-reviewed.json')
    assert source_report['qualified']
    assert not (ROOT / 'results/gravity.json').exists()
    inputs = read(ROOT / 'results/thermodynamic-inputs.json')
    register(inputs, ROOT / 'results/thermodynamics-reviewed.json')
    checks, reports = [], []
    for model in ('heavy', 'cold'):
        background, mixture = load_background(model, inputs)
        with np.load(register(inputs, ROOT / f'results/{model}-stress.npz')) as saved:
            packet = dict(saved)
        system = Response(background, packet)
        solution = system.solve(.01)
        refined = system.solve(.005)
        samples = np.linspace(0, background.end, 101)
        states = solution.sol(samples).T.reshape(-1, 6, 3)
        refined_states = refined.sol(samples).T.reshape(-1, 6, 3)
        fractions = np.array([system.stress(point, state)[3] for point, state in zip(samples, states)])
        refined_fractions = np.array([system.stress(point, state)[3] for point, state in zip(samples, refined_states)])
        for column, name in enumerate(('NR', 'EOS', 'leading_EOS')):
            check(checks, model + ':' + name + ': response step refinement', relative(fractions[:, column], refined_fractions[:, column]), .01)
            check(checks, model + ':' + name + ': clock step refinement', relative(states[:, 4:, column], refined_states[:, 4:, column]), .01)
        with np.load(BRANCH / f'thermal-recoil-and-spectral-response-20261007/results/flrw-response/{model}.npz') as old:
            assert np.array_equal(old['log_expansion'], samples)
            check(checks, model + ': original Stage70 NR H response', relative(fractions[:, 0], old['hubble_response_per_chi']), 5e-5)
            check(checks, model + ': original Stage70 clock response', relative(states[:, 4:, 0], old['response_per_chi'][:, 4:]), 5e-5)
        ward, raychaudhuri = [], []
        for coordinate in samples[1:-1]:
            response = solution.sol(coordinate).reshape(6, 3)
            derivative = system.rhs(coordinate, response.ravel()).reshape(6, 3)
            state, density, pressure, fraction = system.stress(coordinate, response)
            step = 1e-5
            plus = system.stress(coordinate + step, response + step * derivative)
            minus = system.stress(coordinate - step, response - step * derivative)
            numerical = (plus[1] - minus[1]) / (2 * step)
            ward.append(abs(numerical + 3 * (density + pressure)) / np.maximum(abs(numerical) + 3 * abs(density + pressure), 1e-100))
            rho0 = 3 * state['hubble']**2 / state['scale']**2
            pressure0 = (state['photon'] + state['neutrino']) / 3 + np.sum(state['prime']**2 / state['scale']**2 - system.mass2 * state['fields']**2) / 2
            predicted = -1.5 * (pressure - pressure0 * density / rho0) / rho0
            numerical = (plus[3] - minus[3]) / (2 * step)
            raychaudhuri.append(abs(numerical - predicted) / np.maximum(abs(numerical) + abs(predicted), 1e-100))
        check(checks, model + ': all normalized source stress continuity', np.max(ward), 1e-8)
        check(checks, model + ': all normalized Raychaudhuri identities', np.max(raychaudhuri), 1e-8)
        signed = []
        for amplitude in (1e-3, 1e-4):
            positive, positive_rate = system.full_variation(amplitude)
            negative, negative_rate = system.full_variation(-amplitude)
            direct = (positive.sol(samples) - negative.sol(samples)).T / (2 * amplitude)
            rate = np.array([(positive_rate(point, positive.sol(point)) - negative_rate(point, negative.sol(point))) / (2 * amplitude * state_at_scale(background, background.start_scale * math.exp(point))['hubble']) for point in samples])
            error = relative(rate, fractions[:, 1])
            clock_error = relative(direct[:, 4:], states[:, 4:, 1])
            field_error = 0. if model == 'cold' else relative(direct[:, [1, 3]], states[:, [1, 3], 1])
            check(checks, model + ': signed EOS full variation ' + str(amplitude), max(error, clock_error, field_error), 5e-5)
            signed.append(dict(amplitude=amplitude, hubble_error=error, clock_error=clock_error, heavy_field_error=field_error))
        physical = fractions * system.physical_amplitudes
        check(checks, model + ': exact versus leading EOS propagated response', relative(physical[:, 2], physical[:, 1]), .01)
        np.savez_compressed(ROOT / f'results/{model}-gravity.npz', expansion=samples, response=states,
            hubble_response=fractions, physical_hubble_response=physical,
            amplitudes=system.physical_amplitudes, physical_clock_response=states[:, 4:, :] * system.physical_amplitudes)
        reports.append(dict(model=model, labels=['NR thermal baseline', 'electron EOS increment', 'leading EOS approximation'],
            amplitudes=system.physical_amplitudes.tolist(),
            maximum_hubble_fractions=np.max(abs(physical), axis=0).tolist(), final_hubble_fractions=physical[-1].tolist(),
            initial_hubble_fractions=physical[0].tolist(),
            final_proper_time_shifts_seconds=(states[-1, 5, :] * system.physical_amplitudes * background.constants['Mpc'] / background.constants['c']).tolist(),
            corrected_final_hubble_fraction=float(physical[-1, 0] + physical[-1, 1]),
            signed_checks=signed, source_scope='Leading-chi energy-completed electron EOS; fixed incoming scalar fields; no new photon spectral evolution'))
        print(json.dumps(dict(model=model, final_hubble=physical[-1].tolist(), checks=len(checks))), flush=True)
    add_modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    write(ROOT / 'results/gravity-inputs.json', inputs)
    report = dict(stage=228, state='complete', finished_at=now(), models=reports, checks=checks,
                  failed=[row for row in checks if not row['passed']], qualified=all(row['passed'] for row in checks), inputs_rehashed=len(inputs))
    write(ROOT / 'results/gravity.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'], qualified=report['qualified'])), flush=True)


if __name__ == '__main__':
    main()
