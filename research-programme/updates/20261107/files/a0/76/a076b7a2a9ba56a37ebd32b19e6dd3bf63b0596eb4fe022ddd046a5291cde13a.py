import argparse
from consistent_spectral_basis import *


def main(arguments):
    modest()
    folder = ROOT / 'results' / ('readout-quadrature' + str(arguments.count))
    folder.mkdir(parents=True, exist_ok=False)
    basis = ConsistentBasis(arguments.count)
    native_derivative = basis.derivative(basis.nodes)
    native_redshift = ((3 * basis.values + basis.nodes[:, None] * native_derivative).T * basis.measure) @ basis.values
    checks, rows = [], []
    for order in [600, 900]:
        nodes, measure = frequency_quadrature(order, basis.minimum, basis.maximum)
        values, derivative = basis.evaluate(nodes), basis.derivative(nodes)
        mass = (values.T * measure) @ values
        redshift = ((3 * values + nodes[:, None] * derivative).T * measure) @ values
        for name, reference, candidate in [('mass', basis.mass, mass), ('redshift', native_redshift, redshift),
                                            ('number', basis.number, basis.chemical @ mass), ('energy', basis.energy, basis.temperature @ mass)]:
            error = float(linalg.norm(candidate - reference) / linalg.norm(candidate))
            checks.append(dict(name=name + ':300-to' + str(order) + ' fixed-basis quadrature', passed=error < 1e-8, value=error))
            rows.append(dict(quantity=name, order=order, relative_error=error))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        basis_count=arguments.count, scope='Basis moments and dilation readout quadrature only; not a re-evolved collision-kernel quadrature test.'), __file__,
           [ROOT / 'consistent_spectral_basis.py', THERMAL_PARENT / 'stable_spectral_basis.py'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=36)
    main(parser.parse_args())
