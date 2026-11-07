from thermal_wave_common import *
from kernel_ladder import KernelLadder
from high_degree_waves import RefinedLadder
sys.path.insert(0, str(PARENT))
from cold_control import exact_cold


def main():
    modest()
    folder = ROOT / 'results/high-degree-refinement'
    assert not folder.exists()
    checks, rows, inputs = [], [], []
    prior_path = ROOT / 'results/temperature-interpolation/status.json'
    original = json.loads(prior_path.read_text())
    failed = [row for row in original['checks'] if not row['passed']]
    assert failed and all(row['name'].startswith('event6-8: degree8 ') for row in failed)
    retained = [row for row in original['checks'] if not row['name'].startswith('event6-8: degree8 ')]
    checks.append(dict(name='All prior midpoint, frequency and degree0-7 event checks retained unchanged',
                       passed=all(row['passed'] for row in retained), retained_count=len(retained)))
    inputs.append(prior_path)
    ladder = RefinedLadder(16)
    basis = ladder.basis
    probes = [basis.temperature, basis.project(basis.nodes * np.exp(-basis.nodes / 4)),
              basis.project(np.exp(-basis.nodes / 3) * np.sin(np.log(basis.nodes + .2)))]
    for index in range(10):
        fine_path = ROOT / 'banks/high8-16-event10' / ('theta-' + str(index) + '.npz')
        coarse_path = ROOT / 'banks/high8-16-event8' / ('theta-' + str(index) + '.npz')
        inputs.extend([fine_path, coarse_path])
        with np.load(fine_path) as saved:
            fine, mass, theta = saved['stiffness'], saved['mass'], float(saved['theta'])
        with np.load(coarse_path) as saved:
            coarse = saved['stiffness']
        comparisons = [('event8-10', coarse)]
        if index == 9:
            comparisons.append(('hot-midpoint-refined', ladder.at(theta, 8)))
        cold = np.kron(exact_cold(8), mass)
        for comparison, candidate in comparisons:
            for probe_index, probe in enumerate(probes):
                for mode in range(4):
                    vector = np.zeros(4 * basis.count)
                    vector[mode * basis.count:(mode + 1) * basis.count] = probe
                    scale = float(np.linalg.norm((fine - cold) @ vector))
                    error = float(np.linalg.norm((candidate - fine) @ vector) / scale)
                    checks.append(dict(name=comparison + ': temperature' + str(index) + ': mode' + str(mode) + ': probe' + str(probe_index),
                                       passed=error < .002, value=error))
                    rows.append(dict(kind=comparison, temperature_index=index, relative=error))
    for model in ['heavy', 'cold']:
        arrays = []
        for name in [model + '24-3200', model + '24-high8-3200']:
            path = ROOT / 'paired' / name / 'evolution.npz'
            inputs.extend([path, path.parent / 'status.json'])
            assert json.loads((path.parent / 'status.json').read_text())['all_checks_passed']
            with np.load(path) as saved:
                arrays.append((saved['features'], saved['baselines']))
        for column in range(12):
            scale = float(np.max(abs(arrays[1][0][:, column])))
            difference = float(np.max(abs(arrays[0][0][:, column] - arrays[1][0][:, column])))
            floor = 1e-14 * max(float(np.max(abs(arrays[1][1][:, column]))), 1e-30)
            resolved = scale > 100 * floor
            error = difference / scale if resolved else None
            passed = error < .002 if resolved else difference < floor
            checks.append(dict(name=model + ': propagated correction after highest-block quadrature repair, feature' + str(column),
                               passed=passed, value=error))
            rows.append(dict(kind='propagated', model=model, feature=column, relative=error, difference=difference))
    inputs.extend(ladder.inputs)
    inputs.extend([ROOT / 'banks/high8-16-event10/status.json', ROOT / 'banks/high8-24-event8/status.json',
                   ROOT / 'high_degree_waves.py', ROOT / 'thermal_wave_system.py', ROOT / 'stable_spectral_basis.py'])
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        previous_failure=failed, tolerance_unchanged=.002,
                        corrected_quadrature_not_physical_reparameterization=True,
                        final_paired_runs=['heavy24-high8-3200', 'cold24-high8-3200']), __file__, sorted(set(inputs)))
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
                          worst_event=max(row['relative'] for row in rows if row['kind'] == 'event8-10'),
                          worst_propagated=max(row['relative'] for row in rows if row['kind'] == 'propagated' and row['relative'] is not None))), flush=True)


if __name__ == '__main__':
    main()
