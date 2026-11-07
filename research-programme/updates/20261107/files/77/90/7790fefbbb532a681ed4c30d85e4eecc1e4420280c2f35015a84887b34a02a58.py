import argparse
from gould_angles import *


def build(basis, total_order, fraction_order, maximum):
    total_nodes, total_weights = np.polynomial.legendre.leggauss(total_order)
    lower, upper = math.log(2 * basis.minimum), math.log(basis.maximum)
    totals = np.exp(.5 * (lower + upper) + .5 * (upper - lower) * total_nodes)
    total_weights = total_weights * .5 * (upper - lower) * totals
    fraction_nodes, fraction_weights = np.polynomial.legendre.leggauss(fraction_order)
    blocks = [np.zeros_like(basis.mass) for degree in range(maximum + 1)]
    soft_absorption = np.zeros_like(basis.mass)
    event_energy_error = 0.
    for total, total_weight in zip(totals, total_weights):
        log_minimum, log_maximum = math.log(basis.minimum / total), math.log(.5)
        fractions = np.exp(.5 * (log_minimum + log_maximum) + .5 * (log_maximum - log_minimum) * fraction_nodes)
        share_weights = fraction_weights * .5 * (log_maximum - log_minimum) * fractions
        soft = total * fractions
        companion = total - soft
        product = fractions * (1 - fractions)
        gould = (1 - 3 * product + 1.5 * product ** 2 - product ** 3) / (1 - fractions)
        statistical = np.exp(-total) / ((-np.expm1(-total)) * (-np.expm1(-companion)) * (-np.expm1(-soft)))
        weight = total_weight * share_weights * total ** 4 / (I3 * fractions) * gould * statistical
        incident_values = np.broadcast_to(basis.evaluate(total), (len(fractions), basis.count))
        companion_values, soft_values = basis.evaluate(companion), basis.evaluate(soft)
        difference = incident_values - companion_values - soft_values
        difference[:, 0] = -1 / basis.norms[0]
        difference[:, 1] = basis.mean / basis.norms[1]
        event_energy_error = max(event_energy_error, float(np.max(abs(difference @ basis.temperature))))
        blocks[0] -= (difference.T * weight) @ difference
        soft_absorption += (soft_values.T * weight) @ soft_values
        vectors = np.stack([incident_values, -companion_values, -soft_values], axis=1)
        for degree in range(1, maximum + 1):
            hard, incoming, outgoing = correlations(fractions, degree)
            gram = np.broadcast_to(np.eye(3), (len(fractions), 3, 3)).copy()
            gram[:, 0, 1] = gram[:, 1, 0] = hard
            gram[:, 0, 2] = gram[:, 2, 0] = incoming
            gram[:, 1, 2] = gram[:, 2, 1] = outgoing
            factor = np.linalg.cholesky(gram)
            transformed = np.einsum('nij,nik->njk', factor, vectors)
            stacked = (np.sqrt(weight / (2 * degree + 1))[:, None, None] * transformed).reshape(-1, basis.count)
            blocks[degree] -= stacked.T @ stacked
    return blocks, soft_absorption, event_energy_error


def main(arguments):
    modest()
    folder = ROOT / 'banks' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    specification = dict(count=arguments.count, quadrature=700, minimum=1e-5, maximum=60., pivot=.1)
    basis = ConsistentBasis(**specification)
    started = time.perf_counter()
    blocks, absorption, event_error = build(basis, arguments.total_order, arguments.fraction_order, arguments.maximum)
    checks = [check('Event-level photon energy identity before integration', event_error, 1e-12)]
    for degree, block in enumerate(blocks):
        eigenvalues = linalg.eigh(block, basis.mass / (2 * degree + 1), eigvals_only=True)
        scale = max(abs(eigenvalues).max(), 1e-30)
        checks.append(check('Reaction entropy dissipation degree=' + str(degree), max(0., eigenvalues.max()) / scale, 1e-12))
        np.savez_compressed(folder / ('block-' + str(degree) + '.npz'), stiffness=block, mass=basis.mass / (2 * degree + 1), eigenvalues=eigenvalues)
    energy_error = float(linalg.norm(blocks[0] @ basis.temperature) / (linalg.norm(blocks[0]) * linalg.norm(basis.temperature)))
    number_loss = float(basis.chemical @ blocks[0] @ basis.chemical)
    checks.append(check('Full Gould reaction conserves photon energy', energy_error, 1e-12))
    checks.append(dict(name='Full Gould reaction changes photon number', passed=number_loss < 0, chemical_quadratic_form=number_loss))
    np.savez_compressed(folder / 'soft-absorption.npz', stiffness=absorption)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        basis_spec=specification, total_order=arguments.total_order, fraction_order=arguments.fraction_order,
        maximum_degree=arguments.maximum, elapsed=time.perf_counter() - started,
        multiplicative_rate='4 alpha/(3pi) theta_star^2/(1+14.16 theta_star), per Thomson optical depth.',
        angular_scope='Unpolarized intensity block; polarization coupling not inferred from a polarization-summed differential cross section.',
        approximation='Gould cold-electron leading-photon-energy reaction, with inherited near-Planck scalar rate correction; no claim of a full thermal/relativistic DC kernel.',
        full_three_photon_energy_ledger=True, energy_reassigned_to_gas=False,
        coefficients_fitted=False, no_eigenvalue_clipping=True), __file__,
        [ROOT / 'gould_angles.py', BRANCH / 'scaled-spectral-evolution-20261007/sources/2005.06941v1.html'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], elapsed=time.perf_counter() - started)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--count', type=int, default=104)
    parser.add_argument('--total-order', type=int, default=300)
    parser.add_argument('--fraction-order', type=int, default=180)
    parser.add_argument('--maximum', type=int, default=4)
    main(parser.parse_args())
