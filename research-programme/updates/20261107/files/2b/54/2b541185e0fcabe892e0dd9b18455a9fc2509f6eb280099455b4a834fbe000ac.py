from run228 import *


def freeze():
    path = ROOT / 'protocol-repair.json'
    assert not path.exists()
    original = read(ROOT / 'configuration.json')
    replacements = {name: dict(original=original['protocol_hashes'][name], corrected=digest(ROOT / name))
                    for name in ('run228.py', 'gravity228.py')}
    write(path, dict(configuration_sha256=digest(ROOT / 'configuration.json'), replacements=replacements,
          verifier_sha256=digest(__file__), notes_sha256=digest(ROOT / 'CHECK-REPAIR.md'),
          original_report_sha256=digest(ROOT / 'results/thermodynamics.json'),
          arrays={model: digest(ROOT / f'results/{model}-stress.npz') for model in ('heavy', 'cold')},
          frozen_at=now(), tolerances_changed=False, numerical_sources_changed=False))
    print('Check repair frozen; original failed report preserved', flush=True)


def validate():
    protocol()
    repair = read(ROOT / 'protocol-repair.json')
    assert digest(__file__) == repair['verifier_sha256']
    assert digest(ROOT / 'CHECK-REPAIR.md') == repair['notes_sha256']
    assert digest(ROOT / 'results/thermodynamics.json') == repair['original_report_sha256']
    report = read(ROOT / 'results/thermodynamics.json')
    assert len(report['failed']) == 2 and all('derived completed stress continuity' in row['name'] for row in report['failed'])
    replacements = {}
    negative_controls = []
    for model in ('heavy', 'cold'):
        path = ROOT / f'results/{model}-stress.npz'
        assert digest(path) == repair['arrays'][model]
        with np.load(path) as packet:
            residual = float(packet['chi']) * packet['delta_A'] - packet['delta_q'] + 3 * packet['delta_p']
            error = float(np.max(abs(residual)) / np.max(abs(packet['delta_q'])))
            name = model + ': derived completed stress continuity'
            replacements[name] = dict(name=name, value=error, limit=1e-10, passed=error <= 1e-10)
            derivative = interpolate.CubicSpline(packet['expansion'], packet['delta_A']).derivative()(packet['expansion'])
            gas_only_defect = derivative - packet['delta_A']
            ratio = float(np.max(abs(gas_only_defect)) / np.max(abs(packet['delta_A'])))
            negative_controls.append(dict(name=model + ': omitting photon energy completion fails conservation',
                value=ratio, required_minimum=1., passed=ratio > 1.))
    report['checks'] = [replacements.get(row['name'], row) for row in report['checks']] + negative_controls
    report['failed'] = [row for row in report['checks'] if not row['passed']]
    report['qualified'] = not report['failed']
    report['reviewed_at'] = now()
    report['original_report_sha256'] = repair['original_report_sha256']
    report['repair_manifest_sha256'] = digest(ROOT / 'protocol-repair.json')
    assert not (ROOT / 'results/thermodynamics-reviewed.json').exists()
    write(ROOT / 'results/thermodynamics-reviewed.json', report)
    print(json.dumps(dict(checks=len(report['checks']), failed=report['failed'], qualified=report['qualified'])), flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'freeze':
        freeze()
    elif sys.argv[1] == 'validate':
        validate()
    else:
        raise ValueError(sys.argv[1])
