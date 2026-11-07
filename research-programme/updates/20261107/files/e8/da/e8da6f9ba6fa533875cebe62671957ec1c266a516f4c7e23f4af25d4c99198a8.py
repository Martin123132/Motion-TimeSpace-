import argparse
from grid_common import *


def exact_cold(degree):
    if degree == 0:
        return np.diag([0., -1.])
    if degree == 1:
        return np.diag([-1., -.5])
    result = -np.eye(4)
    if degree == 2:
        result[:2, :2] = [[-.9, -np.sqrt(6) / 10], [-np.sqrt(6) / 10, -.4]]
    return result


def projected_maps(degree):
    kernel = angular.AngularKernel(degree + 5, 2 * (degree + 5))
    tensors, names = modal_tensors(kernel.directions, np.array([0., 0., 1.]), degree)
    result = []
    for values in [kernel.scatter(tensors) - tensors, kernel.recoil_angular(tensors), kernel.thermal_angular(tensors)]:
        projected = (2 * degree + 1) / 2 * np.einsum('n,anij,bnji->ab', kernel.weights, tensors, values)
        assert np.max(abs(projected.imag)) < 1e-12
        result.append(projected.real)
    return result


def main(arguments):
    modest()
    source = ROOT / 'banks' / arguments.bank
    metadata = json.loads((source / 'status.json').read_text())
    folder = ROOT / 'banks' / (arguments.bank + '-elastic')
    assert not folder.exists()
    folder.mkdir(parents=True, exist_ok=False)
    checks, inputs = [], [source / 'status.json']
    for degree in range(metadata['maximum_degree'] + 1):
        path = source / ('block-' + str(degree) + '.npz')
        with np.load(path, allow_pickle=False) as saved:
            nodes, mass = saved['nodes'], saved['mass']
        exact = exact_cold(degree)
        projected = projected_maps(degree)[0]
        error = float(np.max(abs(exact - projected)))
        checks.append(dict(name='Elastic block derives from independently projected Thomson tensor degree' + str(degree), passed=error < 1e-10, value=error))
        stiffness = np.kron(exact, mass)
        np.savez_compressed(folder / ('block-' + str(degree) + '.npz'), nodes=nodes, mass=mass, stiffness=stiffness,
                            eigenvalues=np.linalg.eigvalsh(exact), theta=0., reference_theta=metadata['theta'], degree=degree)
        inputs.append(path)
    report = {key: metadata[key] for key in ['points', 'maximum_degree', 'theta', 'minimum_frequency', 'maximum_frequency', 'rows']}
    report.update(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                  cold_control=True, theta_is_parent_reference_for_identical_sampling_not_active_thermal_rate=True,
                  active_thermal_and_recoil_collision_rate=0.)
    finish(folder, report, __file__, inputs)
    print(json.dumps(dict(checks=checks)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bank', required=True)
    main(parser.parse_args())
