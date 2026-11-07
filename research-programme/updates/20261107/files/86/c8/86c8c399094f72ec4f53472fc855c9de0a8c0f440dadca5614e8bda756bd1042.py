import urllib.request
import mpmath as mp
from scaled_common import *


def main():
    modest()
    folder = ROOT / 'results/emission-jacobian'
    folder.mkdir(parents=True, exist_ok=False)
    source_folder = ROOT / 'sources'
    source_folder.mkdir(exist_ok=True)
    sources, inputs, checks = [], [], []
    for identifier, title, doi in [
        ('2112.06699v1', 'CMB spectral distortions from continuous large energy release', '10.1093/mnras/stac2137'),
        ('2005.06941v1', 'The double Compton process in astrophysical plasmas', '10.1088/1475-7516/2020/10/025')
    ]:
        url = 'https://arxiv.org/html/' + identifier
        target = source_folder / (identifier + '.html')
        assert not target.exists()
        request = urllib.request.Request(url, headers={'User-Agent': 'MTS-private-research-source-check/1.0'})
        with urllib.request.urlopen(request, timeout=90) as response:
            payload = response.read()
        assert title.lower() in payload.decode('utf-8').lower()
        target.write_bytes(payload)
        sources.append(dict(source_url=url, title=title, doi=doi, path=str(target), sha256=digest(target)))
        inputs.append(target)
    def check(name, passed, **details):
        checks.append(dict(name=name, passed=bool(passed), **details))
    nodes, weights = np.polynomial.legendre.leggauss(96)
    nodes = .5 * (25. - .002) * nodes + .5 * (25. + .002)
    weights *= .5 * (25. - .002)
    planck = 1 / np.expm1(nodes)
    occupation = planck * (1 + .04 * nodes / (1 + nodes))
    direction = planck * (.13 + .02 * np.cos(nodes))
    temperature_ratio, temperature_direction = 1.03, -.017
    moment_weights = weights * nodes ** 4
    coefficient = 4 * 7.2973525643e-3 / (3 * math.pi) * (4.6e-4) ** 2
    def source(spectrum, ratio):
        integral = moment_weights @ (spectrum * (1 + spectrum))
        bracket = np.exp(-nodes / ratio) * (1 + spectrum) - spectrum
        return coefficient * integral * bracket / nodes ** 3
    integral = moment_weights @ (occupation * (1 + occupation))
    bracket = np.exp(-nodes / temperature_ratio) * (1 + occupation) - occupation
    moment_row = moment_weights * (1 + 2 * occupation)
    absorption = coefficient * integral * (-np.expm1(-nodes / temperature_ratio)) / nodes ** 3
    outer = np.outer(coefficient * bracket / nodes ** 3, moment_row)
    jacobian = -np.diag(absorption) + outer
    thermal = coefficient * integral / nodes ** 3 * np.exp(-nodes / temperature_ratio) * (1 + occupation) * nodes / temperature_ratio ** 2
    analytic = jacobian @ direction + thermal * temperature_direction
    complex_step = 1e-24
    measured = source(occupation + 1j * complex_step * direction, temperature_ratio + 1j * complex_step * temperature_direction).imag / complex_step
    relative = float(np.max(abs(measured - analytic)) / np.max(abs(analytic)))
    check('Non-equilibrium source Jacobian matches complex-step derivative', relative < 1e-10, value=relative)
    direction_second = .1 * planck / (1 + nodes)
    curvature = 2 * (moment_weights @ (direction * direction_second))
    step = .1
    delta_row = (moment_weights * (1 + 2 * (occupation + step * direction_second)) - moment_row) / step
    check('Spectrum functional second derivative retained', abs(delta_row @ direction - curvature) < 1e-11 * abs(curvature))
    singular = linalg.svdvals(outer)
    check('Nonlocal radiation Jacobian is rank one', singular[1] < 1e-12 * singular[0], value=float(singular[1] / singular[0]))
    check('Non-equilibrium rank-one term is nonzero', singular[0] > 0)
    equilibrium = 1 / np.expm1(nodes / temperature_ratio)
    equilibrium_source = source(equilibrium, temperature_ratio)
    null_derivative = nodes / temperature_ratio ** 2 * equilibrium * (1 + equilibrium)
    null = source(equilibrium + 1j * complex_step * null_derivative, temperature_ratio + 1j * complex_step).imag / complex_step
    scale = np.max(coefficient * integral * equilibrium / nodes ** 3)
    check('Joint-temperature equilibrium is a source null', np.max(abs(equilibrium_source)) < 1e-12 * scale)
    check('Joint-temperature derivative is a Jacobian null', np.max(abs(null)) < 1e-11 * scale)
    energy_row = weights * nodes ** 3
    photon_source = source(occupation, temperature_ratio)
    gas_source = -energy_row @ photon_source
    gas_jacobian = -energy_row @ jacobian
    gas_thermal = -energy_row @ thermal
    check('Approximate source energy exchange uses the same photon moment', abs(energy_row @ photon_source + gas_source) < 1e-25)
    energy_residual = energy_row @ analytic + gas_jacobian @ direction + gas_thermal * temperature_direction
    check('Differentiated approximate source preserves paired energy exchange', abs(energy_residual) < 1e-12 * max(abs(energy_row @ analytic), 1e-30), value=float(abs(energy_residual)))
    chemical_response = coefficient * (moment_weights @ (equilibrium * (1 + equilibrium))) * (-np.expm1(-nodes / temperature_ratio)) / nodes ** 3 * equilibrium * (1 + equilibrium)
    check('Photon-production removes the chemical-potential null', weights @ (nodes ** 2 * chemical_response) > 0)
    with mp.workdps(60):
        planck_integral = 4 * mp.pi ** 4 / 15
        ratio = mp.mpf('1.07')
        numerical = mp.quad(lambda frequency: frequency ** 4 * mp.exp(-frequency / ratio) / (-mp.expm1(-frequency / ratio)) ** 2, [0, 1, 5, 20, mp.inf])
        ratio_error = abs(numerical / (ratio ** 5 * planck_integral) - 1)
        check('Fixed-reference Planck functional scales with the fifth power', ratio_error < mp.mpf('1e-45'), value=float(ratio_error))
        chi = mp.mpf('1e-18')
        for frequency in map(mp.mpf, ['0.003', '0.03', '0.3', '1', '8']):
            planck_value = 1 / mp.expm1(frequency)
            weight = planck_value * (1 + planck_value)
            profile = frequency / (1 + frequency)
            background_slip = mp.mpf('.11')
            full_bracket = mp.exp(-frequency / (1 + chi * background_slip)) * (1 + planck_value + chi * weight * profile) - planck_value - chi * weight * profile
            leading = (-mp.expm1(-frequency)) * weight * (frequency * background_slip - profile)
            error = abs(full_bracket / chi - leading) / abs(leading)
            check('Analytic small-background emission bracket x=' + str(frequency), error < mp.mpf('1e-15'), value=float(error))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), sources=sources,
        scope='Leading isotropic nonrelativistic approximate DC source functional and Jacobian; no wave or background emission evolved.',
        spectrum_jacobian_rank_one=True, full_double_compton_redistribution_included=False,
        empirical_claim=False, finite_quadrature_jacobian_tests_not_frequency_convergence=True), __file__, inputs + [ROOT / 'EMISSION-JACOBIAN.md'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
