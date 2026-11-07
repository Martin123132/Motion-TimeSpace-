from repair238 import *
from types import SimpleNamespace
sys.path.insert(0, str(BRANCH / 'expanding-thermal-gravity-20261007'))
from thermal_wave_system import ThermalWaveSystem


class SavedFrame(ThermalWaveSystem):
    def __init__(self, system, history, context, basis):
        self.count, self.maximum, self.momentum = 96, 2, .1
        self.basis = SimpleNamespace(energy=basis['energy'])
        self.geometry = SimpleNamespace(mass2=system.mass**2)
        self.slices, self.names = [], []
        index = 11
        for degree in range(3):
            names = ['I', 'V'] if degree < 2 else ['I', 'E', 'B', 'V']
            self.names.append(names)
            self.slices.append(slice(index, index + self.count * len(names)))
            index += self.count * len(names)
        self.neutrino = slice(index, index + 3)
        self.size = self.neutrino.stop
        self.density_row = np.zeros(self.size, complex)
        self.density_row[[0, 1, 8]] = [-1., -.5, 1.]
        coordinate, scale = context['coordinate'], context['scale']
        total_fields = history['fields'].sum(axis=-1)
        fields = np.array([[np.interp(coordinate, history['rows'][:, 0], total_fields[:, derivative, field])
            for field in range(2)] for derivative in range(2)])
        parent, local = system.background.parent, context['local']
        self.local = dict(scale=scale, hubble=local['H'], heat=local['chi'], temperature_ratio=local['R'],
            photon_reference=context['reference'], baryon=parent.baryons / scale**3, cold=parent.cold / scale**3,
            neutrino=(parent.radiation - parent.photons) / scale**4, fields=fields[0], prime=fields[1], inertia=local['B'])
        self.eos = local

    def background(self, expansion):
        return self.local

    def stress_rows(self, expansion):
        local, energy, current, transverse, longitudinal = super().stress_rows(expansion)
        correction = (self.eos['A'] - self.eos['R']) * self.density_row.copy()
        correction[10] += self.eos['C'] - 1
        energy = energy + local['photon_reference'] * local['heat'] * correction
        return local, energy, current, transverse, longitudinal


def stable_rows(frame, degree, moment, checks, prefix):
    local, energy, current, transverse, longitudinal = frame.stress_rows(0.)
    rows = [energy, current, transverse, longitudinal]
    gas_index = 10 if degree == 0 else 9
    selected = np.r_[np.arange(frame.mode_slice(degree).start, frame.mode_slice(degree).stop), gas_index]
    high = np.column_stack([row[selected].real / local['photon_reference'] for row in rows])
    low = np.zeros_like(high)
    factors = ((1, 0, mp.mpf(1)/3, mp.mpf(1)/3) if degree == 0 else
               (0, mp.mpf(1)/3, 0, 0) if degree == 1 else (0, 0, -mp.mpf(1)/15, mp.mpf(2)/15))
    with mp.workdps(100):
        factors = ([mp.mpf(1), mp.mpf(0), mp.mpf(1)/3, mp.mpf(1)/3] if degree == 0 else
            [mp.mpf(0), mp.mpf(1)/3, mp.mpf(0), mp.mpf(0)] if degree == 1 else
            [mp.mpf(0), mp.mpf(0), -mp.mpf(1)/15, mp.mpf(2)/15])
        for column, factor in enumerate(factors):
            expected = np.array([float(factor * value) for value in moment.exact])
            check(checks, prefix + f':native photon stress row{column}',
                np.linalg.norm(high[:96, column] - expected) / max(np.linalg.norm(expected), 1e-300))
            upper, lower = split_exact([factor * value for value in moment.exact])
            high[:96, column], low[:96, column] = upper[:, 0], lower[:, 0]
        gas_expected = ([scalar(frame.eos['chi']) * scalar(frame.eos['C']), mp.mpf(0),
            2 * scalar(frame.eos['chi']) / 3, 2 * scalar(frame.eos['chi']) / 3] if degree == 0 else
            [mp.mpf(0), scalar(frame.eos['B']), mp.mpf(0), mp.mpf(0)])
        for column, expected in enumerate(gas_expected):
            check(checks, prefix + f':native EOS gas row{column}',
                abs(high[-1, column] - float(expected)) / max(abs(float(expected)), 1e-300))
            high[-1, column], low[-1, column] = split_exact([expected])[0][0, 0], split_exact([expected])[1][0, 0]
    return high, low


def run():
    modest()
    config, frozen = repair_protocol()
    assert read(ROOT / 'results/repaired-ports.json')['qualified']
    assert not (ROOT / 'results/frame.json').exists()
    inputs = read(ROOT / 'results/port-inputs.json')
    register(inputs, BRANCH / 'expanding-thermal-gravity-20261007/thermal_wave_system.py')
    systems = {model: gravity.prior.System(model, 6400, inputs) for model in ('heavy', 'cold')}
    histories = {model: packet(BRANCH / 'two-way-thermal-gravity-20261026/runs' / (model + '-6400') / 'history.npz') for model in systems}
    basis = packet(ROOT / 'frozen/basis.npz')
    moment = SameMassMoment(basis)
    checks, records, frame_records = [], [], []
    for event in config['events']:
        anchor = event['label']
        raw = packet(ROOT / 'results' / (anchor + '-ports.npz'))
        protected = packet(ROOT / 'results' / (anchor + '-protected-ports.npz'))
        contexts = read(ROOT / 'results' / (anchor + '-contexts.json'))
        for state, context in zip(config['states'], contexts):
            frame = SavedFrame(systems[state['model']], histories[state['model']], context, basis)
            prefix = f'{anchor}:{state["model"]}:{state["history"]}'
            frame_records.append(dict(anchor=anchor, model=state['model'], history=state['history'],
                fields=frame.local['fields'].tolist(), prime=frame.local['prime'].tolist(), size=frame.size))
            for degree in config['multipoles']:
                high, low = stable_rows(frame, degree, moment, checks, prefix + f':l{degree}')
                for join in config['joins']:
                    for component in config['components']:
                        for version in config['angular_versions']:
                            key = f'angular{version}:join{join}:{state["model"]}:{state["history"]}:l{degree}:{component}'
                            gas_rate = raw[key + ':gas_rate'] if degree < 2 else np.zeros(99)
                            source = np.vstack([raw[key + ':photon'], gas_rate])
                            normalized = precise.stable_dot(source.T, high, low).T
                            energy, current, transverse, longitudinal = context['reference'] * normalized
                            direct_scale = context['reference'] * max(np.linalg.norm(protected[key + ':photon_moment'])
                                + np.linalg.norm(raw[key + ':gas_moment']), 1e-300)
                            maximum_error = 0.
                            for name, value in [('energy', energy), ('current', current),
                                ('stress_transverse', transverse), ('stress_longitudinal', longitudinal)]:
                                error = normalization_error(value, protected[key + ':' + name], direct_scale)
                                check(checks, anchor + ':' + key + ':native frame ' + name, error)
                                maximum_error = max(maximum_error, error)
                            metric_transverse = context['scale']**2 * (energy - longitudinal) / 2
                            metric_longitudinal = context['scale']**2 * (energy + longitudinal - 2 * transverse) / 2
                            for name, value in [('sigma_transverse_second', metric_transverse), ('sigma_longitudinal_second', metric_longitudinal)]:
                                error = normalization_error(value, protected[key + ':' + name], context['scale']**2 * direct_scale)
                                check(checks, anchor + ':' + key + ':native Einstein response ' + name, error)
                                maximum_error = max(maximum_error, error)
                            old_eos_defect = 0.
                            if degree == 0:
                                old_eos = energy + context['reference'] * context['local']['chi'] * (1 - context['local']['C']) * gas_rate
                                old_eos_defect = normalization_error(old_eos, energy, direct_scale)
                                check(checks, anchor + ':' + key + ':uncorrected NR stress rejected', int(old_eos_defect <= 1e-7), 0)
                            records.append(dict(anchor=anchor, key=key, model=state['model'], component=component,
                                maximum_frame_error=maximum_error, uncorrected_NR_defect=old_eos_defect))
        print(json.dumps(dict(anchor=anchor, checks=len(checks), failures=sum(not row['passed'] for row in checks))), flush=True)
    modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    repair_protocol()
    failed = [row for row in checks if not row['passed']]
    write(ROOT / 'results/frame-inputs.json', inputs)
    result = dict(stage=238, qualified=not failed, checks=checks, failed=failed, records=records,
        frames=frame_records, maximum_frame_error=max(row['maximum_frame_error'] for row in records),
        minimum_nonzero_NR_defect=min(row['uncorrected_NR_defect'] for row in records if row['uncorrected_NR_defect']),
        source='Retained ThermalWaveSystem.stress_rows plus Stage231 EOS energy row, evaluated in a mass-consistent representation',
        scope='Instantaneous collision injection into actual saved scalar/metric/gas/radiation frame; no full wave evolution',
        script_sha256=digest(__file__), finished_at=now())
    write(ROOT / 'results/frame.json', result)
    print(json.dumps({name: value for name, value in result.items() if name not in ('checks', 'failed', 'records', 'frames')})
        + '\n' + json.dumps(failed[:8]), flush=True)


if __name__ == '__main__':
    run()
