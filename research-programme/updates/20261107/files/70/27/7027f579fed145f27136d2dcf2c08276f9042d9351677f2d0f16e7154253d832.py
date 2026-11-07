from coupling238 import *
import argparse


def split_exact(values):
    high = np.array([float(value) for value in values])[:, None]
    low = np.array([float(value - scalar(float(value))) for value in values])[:, None]
    return high, low


class SameMassMoment:
    def __init__(self, basis):
        self.mass = np.triu(basis['mass']) + np.triu(basis['mass'], 1).T
        with mp.workdps(100):
            self.exact = [mp.fsum(scalar(basis['temperature'][index]) * scalar(self.mass[index, column])
                for index in (0, 1)) for column in range(96)]
            self.high, self.low = split_exact(self.exact)
            self.defect_high, self.defect_low = split_exact([scalar(value) - exact
                for value, exact in zip(basis['energy'], self.exact)])
        self.original = basis['energy'][:, None]

    def contract(self, source, degree):
        divisor = 2 * degree + 1
        protected = precise.stable_dot(source.T, self.high, self.low)[:, 0] / divisor
        original = precise.stable_dot(source.T, self.original, np.zeros_like(self.original))[:, 0] / divisor
        defect = precise.stable_dot(source.T, self.defect_high, self.defect_low)[:, 0] / divisor
        return protected, original, defect


def freeze():
    config = protocol()
    assert not (ROOT / 'repair-configuration.json').exists()
    raw = read(ROOT / 'results/ports.json')
    assert len(raw['failed']) == 83
    assert all(row['name'].endswith(':weak-to-physical photon moment') for row in raw['failed'])
    inputs = {name: digest(ROOT / name) for name in ['results/ports.json', 'results/precision-diagnosis.json',
        'frozen/basis.npz', 'port-configuration.json'] + [f'results/{anchor}-{suffix}'
        for anchor in ('warm', 'middle', 'cold') for suffix in ('ports.npz', 'contexts.json')]}
    write(ROOT / 'repair-configuration.json', dict(frozen_at=now(), identity_tolerance=config['identity_tolerance'],
        physical_response_tolerance=config['physical_response_tolerance'], inputs=inputs,
        code={name: digest(ROOT / name) for name in ('repair238.py', 'frame238.py', 'PRECISION-REPAIR.md')},
        original_failed_checks=83, change='Readout only; no source state, gas row, bank, history or gate change'))


def repair_protocol():
    config = protocol()
    frozen = read(ROOT / 'repair-configuration.json')
    for group in ('code', 'inputs'):
        for name, expected in frozen[group].items():
            assert digest(ROOT / name) == expected, name
    assert config['identity_tolerance'] == frozen['identity_tolerance']
    return config, frozen


def run():
    modest()
    config, frozen = repair_protocol()
    assert not (ROOT / 'results/repaired-ports.json').exists()
    basis = packet(ROOT / 'frozen/basis.npz')
    moment = SameMassMoment(basis)
    checks, records, refinements = [], [], []
    for event in config['events']:
        anchor = event['label']
        matrices = packet(PARENT / 'results' / (anchor + '-assessment.npz'))
        raw = packet(ROOT / 'results' / (anchor + '-ports.npz'))
        contexts = read(ROOT / 'results' / (anchor + '-contexts.json'))
        output = {}
        for state, context in zip(config['states'], contexts):
            opacity, local = context['opacity'], context['local']
            for join in config['joins']:
                for component in config['components']:
                    versions = {}
                    for version in config['angular_versions']:
                        versions[version] = {}
                        for degree in config['multipoles']:
                            key = f'angular{version}:join{join}:{state["model"]}:{state["history"]}:l{degree}:{component}'
                            source = raw[key + ':photon']
                            protected, exact_original, predicted_defect = moment.contract(source, degree)
                            original = raw[key + ':photon_moment']
                            direct = opacity * matrices[key][0]
                            gas = raw[key + ':gas_moment']
                            scale = max(float(np.linalg.norm(direct)), 1e-300)
                            defect_error = np.linalg.norm((exact_original - protected) - predicted_defect) / scale
                            check(checks, anchor + ':' + key + ':unfitted row defect identity', defect_error)
                            roundoff_bound = 256 * np.finfo(float).eps * (abs(basis['energy']) @ abs(source)) / (2 * degree + 1)
                            roundoff_ratio = float(np.max(abs(original - exact_original) / np.maximum(roundoff_bound, 1e-300)))
                            check(checks, anchor + ':' + key + ':ordinary dot rounding bound', roundoff_ratio, 1.)
                            error = normalization_error(protected, direct)
                            check(checks, anchor + ':' + key + ':same-mass direct photon energy', error)
                            pair_scale = max(np.linalg.norm(direct) + np.linalg.norm(gas), 1e-300)
                            exchange = float(np.linalg.norm(protected + gas) / pair_scale) if degree < 2 else 0.
                            if degree < 2:
                                check(checks, anchor + ':' + key + ':independent gas exchange', exchange)
                            port = dict(photon_moment=protected, gas_moment=gas)
                            metric = metric_response(port, degree, context['reference'], context['scale'], local['C'])
                            output[key + ':photon_moment'] = protected
                            output[key + ':readout_change'] = protected - original
                            output[key + ':predicted_row_defect'] = predicted_defect
                            for name, value in metric.items():
                                output[key + ':' + name] = value
                            versions[version][degree] = metric
                            records.append(dict(anchor=anchor, key=key, model=state['model'], component=component, degree=degree,
                                direct_relative_error=error, exchange_residual=exchange, defect_identity_error=float(defect_error),
                                roundoff_bound_ratio=roundoff_ratio, readout_change_relative=float(np.linalg.norm(protected - original) / scale)))
                    for degree in config['multipoles']:
                        for name in ('pressure', 'shear', 'sigma_transverse_second', 'sigma_longitudinal_second'):
                            old, middle, last = [versions[version][degree][name] for version in config['angular_versions']]
                            error = relative(middle, last)
                            label = f'{anchor}:join{join}:{state["model"]}:{state["history"]}:l{degree}:{component}:{name}'
                            check(checks, label + ':repaired angular6-to8', error, config['physical_response_tolerance'])
                            output[label + ':candidate_minus_original'] = last - old
                            refinements.append(dict(key=label, angular6_to8=error, original_to8=relative(old, last),
                                refinement_over_delta=float(np.linalg.norm(last - middle) / max(np.linalg.norm(last - old), 1e-300))))
        save(ROOT / 'results' / (anchor + '-protected-ports.npz'), **output)
        print(json.dumps(dict(anchor=anchor, checks=len(checks), failures=sum(not row['passed'] for row in checks))), flush=True)
    repair_protocol()
    failed = [row for row in checks if not row['passed']]
    result = dict(stage=238, qualified=not failed, checks=checks, failed=failed, records=records, refinements=refinements,
        original_trial_preserved=True, original_failed_checks=frozen['original_failed_checks'],
        maximum_direct_error=max(row['direct_relative_error'] for row in records),
        maximum_exchange_residual=max(row['exchange_residual'] for row in records),
        maximum_defect_identity_error=max(row['defect_identity_error'] for row in records),
        maximum_refinement=max(row['angular6_to8'] for row in refinements),
        script_sha256=digest(__file__), finished_at=now(), spectrum_and_gas_unchanged=True)
    write(ROOT / 'results/repaired-ports.json', result)
    print(json.dumps({name: value for name, value in result.items() if name not in ('checks', 'records', 'refinements', 'failed')})
        + '\n' + json.dumps(failed[:6]), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['freeze', 'run'])
    {'freeze': freeze, 'run': run}[parser.parse_args().mode]()
