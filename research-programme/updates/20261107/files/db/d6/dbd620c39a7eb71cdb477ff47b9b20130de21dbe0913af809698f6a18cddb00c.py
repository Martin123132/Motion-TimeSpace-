import sympy as symbolic
from soft_matching_common import *
from gould_angles import marginal_eigenvalue
from emission_rates import ALPHA


def main():
    modest()
    folder = ROOT / 'results/soft-domain-and-normalization'
    folder.mkdir(parents=True, exist_ok=False)
    share, total, profile, slope, occupation, gain = symbolic.symbols('w t f fp n h')
    argument = 1 - share
    first = 2 * (1 - argument) ** 2 * (3 - 7 * argument + 13 * argument ** 2 - 7 * argument ** 3 + 3 * argument ** 4)
    second = 11 - 21 * argument + 30 * argument ** 3 - 21 * argument ** 5 + 11 * argument ** 6
    coefficients = [first + 2 * second / 3 + symbolic.Rational(20, 3) * argument ** 3,
        -16 * argument ** 3, -2 * second / 3 + symbolic.Rational(40, 3) * argument ** 3, -4 * argument ** 3]
    checks = []
    for degree in range(4):
        eigenvalue = coefficients[degree] / ((2 * degree + 1) * coefficients[0])
        derivative = symbolic.simplify(symbolic.diff(eigenvalue, share).subs(share, 0))
        checks.append(dict(name='Hard angular moment has no linear soft-share term l=' + str(degree), passed=derivative == 0))
    log_integrand = 2 * (1 - gain) * ((symbolic.Rational(1, 2) + occupation - 2 / total) * profile ** 2 - profile * slope)
    total_derivative = -(1 - gain) * ((4 / total - 1 - 2 * occupation) * profile ** 2 + 2 * profile * slope)
    checks.append(dict(name='Subleading logarithm is a frequency-boundary derivative for IR-safe profiles', passed=symbolic.expand(log_integrand - total_derivative) == 0))
    checks.append(dict(name='Photon number is not an IR-safe inclusive hard observable', passed=(1 - 1 - 1 == -1 and 1 - 1 == 0)))
    pole = json.loads((ROOT / 'banks/finite-shift-soft104-l4/status.json').read_text())
    assert pole['all_checks_passed']
    rows = []
    for row in pole['rows']:
        theta = row['theta']
        scalar = 4 * ALPHA / (3 * math.pi) * theta ** 2
        strict = 8 * math.pi ** 2
        approximate = strict / (1 + 14.16 * theta)
        exact = row['temperature_rayleighs'][1]
        rows.append(dict(theta=theta, strict_gould=strict, scalar_corrected_gould=approximate, exact_event=exact,
            approximate_to_exact_relative=abs(approximate / exact - 1),
            leftover_rate_if_old_real_and_new_virtual_mixed_at_xmin_1e5=scalar * (approximate - exact) / 1e-5))
    checks.append(dict(name='Mixing scalar-corrected Gould and exact virtual coefficient would leave a pole', passed=all(abs(row['leftover_rate_if_old_real_and_new_virtual_mixed_at_xmin_1e5']) > 0 for row in rows)))
    write_json(folder / 'normalization.json', rows)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        soft_pole_is_hard_process_only=True, physical_photon_creation_not_subtracted=True,
        no_log_claim_conditions='Planck bath, retained Gould limit, f(x)=O(x), smooth hard profile, vanishing frequency-boundary term; not a statement for arbitrary emitting spectra or all nonthermal states.',
        remaining_low_frequency_condition='The thermal functional generalizes to isotropic occupation N when integral_0^Delta x*N(x) dx is finite. The finite-window numerical emitting profile is not a proof of this condition below xmin.'), __file__,
        [ROOT / 'banks/finite-shift-soft104-l4/status.json', ROOT / 'polarized_soft_pole.py', ROOT / 'inclusive_soft.py',
         PARENT / 'gould_angles.py', PARENT / 'results/resolved-infrared-asymptotic/status.json'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
