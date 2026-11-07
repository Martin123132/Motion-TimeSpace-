from thermal_wave_common import *
from kernel_ladder import KernelLadder
from stable_spectral_basis import load_basis
sys.path.insert(0, str(PARENT))
from cold_control import exact_cold


def main():
    modest()
    folder = ROOT / 'results/temperature-interpolation'
    assert not folder.exists()
    ladder = KernelLadder(16)
    checks, rows, inputs = [], [], list(ladder.inputs)
    for tag, coarse_name, fine_name in [
        ('hot-midpoint', None, 'midpoint16'),
        ('event6-8', 'midpoint16', 'midpoint16-event8'),
        ('frequency300-420', 'midpoint16-event8', 'midpoint16-quadrature420'),
    ]:
        fine_folder = ROOT / 'banks' / fine_name
        fine_basis = load_basis(fine_folder)
        report = json.loads((fine_folder / 'status.json').read_text())
        assert report['all_checks_passed']
        inputs.append(fine_folder / 'status.json')
        probes = [fine_basis.temperature,
                  fine_basis.project(fine_basis.nodes * np.exp(-fine_basis.nodes / 4)),
                  fine_basis.project(np.exp(-fine_basis.nodes / 3) * np.sin(np.log(fine_basis.nodes + .2)))]
        if coarse_name:
            coarse_folder = ROOT / 'banks' / coarse_name
            coarse_basis = load_basis(coarse_folder)
            coarse_values = coarse_basis.evaluate(fine_basis.nodes)
            transfer = linalg.solve(fine_basis.mass,
                                    fine_basis.values.T @ (fine_basis.measure[:, None] * coarse_values), assume_a='pos')
            inputs.append(coarse_folder / 'status.json')
        else:
            transfer = np.eye(fine_basis.count)
        for degree in range(9):
            fine_path = fine_folder / ('block-' + str(degree) + '.npz')
            with np.load(fine_path) as saved:
                fine_matrix, mass = saved['stiffness'], saved['mass']
            inputs.append(fine_path)
            modes = len(fine_matrix) // fine_basis.count
            if coarse_name:
                coarse_path = coarse_folder / ('block-' + str(degree) + '.npz')
                with np.load(coarse_path) as saved:
                    coarse_matrix = saved['stiffness']
                inputs.append(coarse_path)
                inverse_transfer = linalg.inv(transfer)
                full_transfer = linalg.block_diag(*([inverse_transfer] * modes))
                coarse_matrix = full_transfer.T @ coarse_matrix @ full_transfer
            else:
                coarse_matrix = ladder.at(report['theta'], degree)
            cold = np.kron(exact_cold(degree), mass)
            for probe_index, probe in enumerate(probes):
                for mode in range(modes):
                    vector = np.zeros(len(fine_matrix))
                    vector[mode * fine_basis.count:(mode + 1) * fine_basis.count] = probe
                    response = (fine_matrix - cold) @ vector
                    difference = (coarse_matrix - fine_matrix) @ vector
                    scale = float(np.linalg.norm(response))
                    error = float(np.linalg.norm(difference) / max(scale, 1e-100))
                    checks.append(dict(name=tag + ': degree' + str(degree) + ' mode' + str(mode) + ' probe' + str(probe_index),
                                       passed=error < .002, value=error))
                    rows.append(dict(comparison=tag, degree=degree, mode=mode, probe=probe_index, relative=error, response_norm=scale))
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        scope='Independent hot-end midpoint and event/frequency quadrature probes; not a uniform operator-norm proof.',
                        cold_subtracted=True, gate=.002), __file__, sorted(set(inputs)))
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
                          worst=max(row['relative'] for row in rows))), flush=True)


if __name__ == '__main__':
    main()
