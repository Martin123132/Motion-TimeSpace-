from gould_angles import *
from emission_rates import ALPHA


def dipole_rates(cutoff, total_order=360, fraction_order=220):
    total_nodes, total_weights = np.polynomial.legendre.leggauss(total_order)
    lower, upper = math.log(2 * cutoff), math.log(60.)
    totals = np.exp(.5 * (lower + upper) + .5 * (upper - lower) * total_nodes)
    total_weights *= .5 * (upper - lower) * totals
    fraction_nodes, fraction_weights = np.polynomial.legendre.leggauss(fraction_order)
    rates = np.zeros(4)
    for total, total_weight in zip(totals, total_weights):
        lower, upper = math.log(cutoff / total), math.log(.5)
        fractions = np.exp(.5 * (lower + upper) + .5 * (upper - lower) * fraction_nodes)
        share_weights = fraction_weights * .5 * (upper - lower) * fractions
        soft, companion = total * fractions, total * (1 - fractions)
        product = fractions * (1 - fractions)
        gould = (1 - 3 * product + 1.5 * product ** 2 - product ** 3) / (1 - fractions)
        forward = np.exp(-total) / ((-np.expm1(-total)) * (-np.expm1(-companion)) * (-np.expm1(-soft)))
        measure = total_weight * share_weights * total ** 4 / (I3 * fractions) * gould * forward
        for degree in range(1, 5):
            hard, incoming, outgoing = correlations(fractions, degree)
            norm = total ** 2 + companion ** 2 + soft ** 2 - 2 * total * companion * hard - 2 * total * soft * incoming + 2 * companion * soft * outgoing
            rates[degree - 1] += np.sum(measure * norm) / 4
    return rates


def main():
    modest()
    folder = ROOT / 'results/resolved-infrared-asymptotic'
    folder.mkdir(parents=True, exist_ok=False)
    cutoffs = np.array([1e-3, 1e-4, 1e-5, 1e-6])
    actual = np.array([dipole_rates(cutoff) for cutoff in cutoffs])
    leading = np.array([40 * math.pi ** 2 / 7 * (1 - float(marginal_eigenvalue(1., degree))) for degree in range(1, 5)])
    checks = []
    for degree in range(1, 5):
        residual = abs(cutoffs * actual[:, degree - 1] / leading[degree - 1] - 1)
        checks.append(check('Resolved real-photon asymptotic coefficient l=' + str(degree), residual[-1], .002))
        checks.append(dict(name='Asymptotic improves under decreasing resolution l=' + str(degree), passed=bool(np.all(np.diff(residual) < 0)), residuals=residual.tolist()))
    thermal = thermal_wave.thermal.ThermalBackground('heavy')
    theta = thermal.theta0 / thermal.start_scale
    scalar_rate = 4 * ALPHA / (3 * math.pi) * theta ** 2 / (1 + 14.16 * theta)
    np.savez_compressed(folder / 'cutoff.npz', cutoffs=cutoffs, resolved_angular_rates=actual, leading_coefficient=leading)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        cutoffs=cutoffs.tolist(), rates_per_scalar_dc_rate=actual.tolist(), asymptotic_coefficient=leading.tolist(),
        temperature_at_start=theta, rates_per_thomson_depth_at_start=(scalar_rate * actual).tolist(),
        full_planck_temperature_template_mass=4,
        formula='beta_l(xmin) ~ [40 pi^2/7] [1-lambda_l(1)] / xmin for the x*P_l temperature template, l>=1.',
        cutoff_independent_transport=False, finite_virtual_term_derived=False,
        next_route='Combine unresolved stimulated real events with medium-consistent virtual correction; do not pass the resolved rate alone into a physical wave run.'), __file__,
        [ROOT / 'gould_angles.py', BACKGROUND / 'emission_rates.py',
         BRANCH / 'scaled-spectral-evolution-20261007/sources/2005.06941v1.html'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rates_at_start=(scalar_rate * actual).tolist())), flush=True)


if __name__ == '__main__':
    main()
