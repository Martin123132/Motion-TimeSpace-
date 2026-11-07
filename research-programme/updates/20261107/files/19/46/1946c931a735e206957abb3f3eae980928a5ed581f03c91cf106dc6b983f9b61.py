import mpmath as mp
import sympy as symbolic
from inclusive_soft import *


def main():
    modest()
    mp.mp.dps = 70
    folder = ROOT / 'results/inclusive-thermal-functional'
    folder.mkdir(parents=True, exist_ok=False)
    frequency, conjugate, temperature = symbolic.symbols('x z T', positive=True)
    occupation = 1 / (symbolic.exp(frequency / temperature) - 1)
    combined = ((1 + occupation) * (symbolic.exp(symbolic.I * frequency * conjugate) - 1)
                + occupation * (symbolic.exp(-symbolic.I * frequency * conjugate) - 1)) / frequency
    limiting = symbolic.simplify(symbolic.limit(combined, frequency, 0, dir='+'))
    checks = [dict(name='Exact soft integrand limit i*z-T*z^2', passed=symbolic.simplify(limiting - symbolic.I * conjugate + temperature * conjugate ** 2) == 0)]
    rows = []
    for heat in [.7, 1., 1.3]:
        for separator in [.001, .02, .1]:
            checks.append(check('Inclusive normalization T=' + str(heat) + ' separator=' + str(separator), abs(exponent(0., separator, temperature=heat)), 1e-14))
            for phase in [.1, 1., 7.]:
                exact = exponent(phase, separator, temperature=heat)
                detailed_balance = exponent(-phase + 1j / heat, separator, temperature=heat)
                checks.append(check('Thermal detailed-balance characteristic symmetry', abs(exact - detailed_balance), 1e-12))
                checks.append(dict(name='Characteristic attenuation nonnegative', passed=exact.real <= 0, value=float(exact.real)))
                for lower in [1e-4, 1e-6, 1e-8]:
                    truncated = exponent(phase, separator, lower, heat)
                    error = abs(truncated - exact)
                    bound = unresolved_bound(phase, lower, heat)
                    checks.append(dict(name='Derived unresolved remainder bound', passed=error <= bound * (1 + 1e-10), value=error, bound=bound))
                rows.append(dict(temperature=heat, separator=separator, conjugate=phase,
                    exponent_real=exact.real, exponent_imaginary=exact.imag, last_cutoff_error=error, last_bound=bound))
            mean, variance = cumulants(separator, heat)
            checks.append(dict(name='Finite positive transferred-energy cumulants', passed=mean > 0 and variance > 0, mean=mean, variance=variance))
    comparisons = []
    for lower in ['0.001', '0.00001', '0.0000001']:
        minimum, maximum, phase = mp.mpf(lower), mp.mpf('.02'), mp.mpf('3')
        emission = mp.quad(lambda energy: (1 + 1 / mp.expm1(energy)) * mp.exp(mp.j * energy * phase) / energy, [minimum, maximum])
        absorption = mp.quad(lambda energy: mp.exp(-mp.j * energy * phase) / (energy * mp.expm1(energy)), [minimum, maximum])
        virtual = -mp.quad(lambda energy: mp.coth(energy / 2) / energy, [minimum, maximum])
        reference = complex(emission + absorption + virtual)
        stable = exponent(float(phase), float(maximum), float(minimum))
        checks.append(check('Independent high-precision real/absorption/virtual sum xmin=' + lower, abs(reference - stable), 1e-12))
        comparisons.append(dict(lower=float(minimum), emission_real=float(emission.real), absorption_real=float(absorption.real),
            virtual_real=float(virtual), sum_real=reference.real, sum_imaginary=reference.imag))
    checks.append(dict(name='Missing absorption breaks normalization: negative control',
        passed=abs(comparisons[-1]['virtual_real'] + comparisons[-1]['emission_real']) > 1e6))
    checks.append(dict(name='Separate pieces diverge while inclusive sum converges',
        passed=abs(comparisons[-1]['virtual_real']) > 90 * abs(comparisons[-2]['virtual_real']) and abs(comparisons[-1]['sum_real']) < 1))
    write_json(folder / 'independent-pieces.json', comparisons)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        exact_thermal_eikonal_functional=True, nonthermal_bath_extension_proved=False,
        arbitrary_separator_removed_from_full_observable=False, finite_hard_virtual_matching=False,
        conclusion='Leading soft cancellation and its finite transfer functional are derived, with explicit remainder bound; no arbitrary finite virtual constant selected.'), __file__,
        [ROOT / 'inclusive_soft.py', ROOT / 'sources/hep-ph-9308249.html', ROOT / 'sources/hep-ph-9507341.html'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], last_pieces=comparisons[-1])), flush=True)


if __name__ == '__main__':
    main()
