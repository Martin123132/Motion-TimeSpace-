from grid_common import *
from cold_control import projected_maps, exact_cold


def main():
    modest()
    folder = ROOT / 'results/continuum-limits'
    assert not folder.exists()
    bank = ROOT / 'banks/main-192'
    metadata = json.loads((bank / 'status.json').read_text())
    quadrature, weights = np.polynomial.legendre.leggauss(400)
    minimum, maximum = metadata['minimum_frequency'], metadata['maximum_frequency']
    frequency = (maximum + minimum) / 2 + quadrature * (maximum - minimum) / 2
    weights *= (maximum - minimum) / 2
    occupation = 1 / np.expm1(frequency)
    spectral_weight = occupation * (1 + occupation)
    local = 2 * frequency * (1 + 2 * occupation) - 2 * frequency ** 2 * spectral_weight
    thermal_integral = float(np.dot(weights, frequency ** 4 * spectral_weight) / (2 * I3))
    local_integral = float(np.dot(weights, frequency ** 4 * spectral_weight * local) / (2 * I3))
    checks, rows, inputs = [], [], [bank / 'status.json', ROOT / 'cold_control.py']
    for degree in range(metadata['maximum_degree'] + 1):
        path = bank / ('block-' + str(degree) + '.npz')
        with np.load(path) as saved:
            nodes, mass, stiffness, theta = saved['nodes'], saved['mass'], saved['stiffness'], float(saved['theta'])
        cold, recoil, thermal = projected_maps(degree)
        modes = len(cold)
        basis = np.kron(np.eye(modes), nodes[:, None])
        actual = (basis.T @ stiffness @ basis - (nodes @ mass @ nodes) * exact_cold(degree)) / theta
        target = 2 / (2 * degree + 1) * (thermal_integral * (thermal + recoil) + local_integral * (np.eye(modes) - recoil))
        error = float(np.linalg.norm(actual - target) / max(np.linalg.norm(target), 1e-100))
        checks.append(dict(name='Physical bank weak thermal/recoil correction matches independent parent tensor degree' + str(degree),
                           passed=error < .002, value=error, gate=.002))
        rows.append(dict(degree=degree, relative_thermal_coefficient_error=error,
                         actual=actual.tolist(), target=target.tolist()))
        inputs.append(path)
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        rows=rows, coefficient_comparison_not_large_elastic_norm=True,
                        finite_temperature_higher_order_remainder_retained=True), __file__, inputs)
    print(json.dumps(dict(checks=checks)), flush=True)


if __name__ == '__main__':
    main()
