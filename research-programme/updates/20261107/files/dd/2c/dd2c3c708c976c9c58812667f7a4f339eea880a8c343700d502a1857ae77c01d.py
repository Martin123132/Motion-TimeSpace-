import argparse
from emission_angular_common import *
from integrated_dc import IntegratedDCEmission
from emission_rates import ALPHA


def main(arguments):
    modest()
    folder = ROOT / 'results' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    fine_path, coarse_path = ROOT / 'banks' / arguments.fine, ROOT / 'banks' / arguments.coarse
    packet = json.loads((fine_path / 'status.json').read_text())
    basis = ConsistentBasis(**packet['basis_spec'])
    inputs = [fine_path / 'status.json', coarse_path / 'status.json']
    checks = []
    for degree in range(packet['maximum_degree'] + 1):
        fine_file, coarse_file = fine_path / ('block-' + str(degree) + '.npz'), coarse_path / ('block-' + str(degree) + '.npz')
        with np.load(fine_file) as fine, np.load(coarse_file) as coarse:
            error = linalg.norm(fine['stiffness'] - coarse['stiffness']) / linalg.norm(fine['stiffness'])
        checks.append(check('Reaction quadrature refinement degree=' + str(degree), error, .002))
        inputs.extend([fine_file, coarse_file])
    background = thermal_wave.thermal.ThermalBackground('heavy')
    emission = IntegratedDCEmission(basis, background, 1400, 81)
    theta = background.theta0 / background.start_scale
    legacy = emission.at(theta, 'dc') / (4 * ALPHA / (3 * math.pi) * theta ** 2 / (1 + 14.16 * theta))
    path = fine_path / 'soft-absorption.npz'
    with np.load(path) as saved:
        absorption = saved['stiffness']
    error = float(linalg.norm(absorption - legacy) / linalg.norm(legacy))
    checks.append(check('Independent legacy soft absorption normalization recovered', error, .002))
    inputs.extend([path, BACKGROUND / 'integrated_dc.py', *emission.inputs])
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        matrix_norm_gate_only=True, observable_response_refinement_not_implied=True), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], maximum=max(row['value'] for row in checks))), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fine', required=True)
    parser.add_argument('--coarse', required=True)
    parser.add_argument('--name', required=True)
    main(parser.parse_args())
