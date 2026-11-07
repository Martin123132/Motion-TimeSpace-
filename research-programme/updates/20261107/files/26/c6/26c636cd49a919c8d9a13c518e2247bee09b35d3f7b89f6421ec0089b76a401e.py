from vacuum_virtual import *


def main():
    modest()
    mp.mp.dps = 140
    folder = ROOT / 'results/finite-virtual'
    assert not (folder/'COMPLETE').exists()
    folder.mkdir(parents=True, exist_ok=True)
    checks, rows = [], []
    for rapidity in ['1e-8', '.001', '.4', '3']:
        value = mp.mpf(rapidity)
        discrepancy = abs(h_closed(value) - h_integral(value))
        checks.append(check('h integral versus corrected closed form y=' + rapidity, discrepancy, 1e-65))
    for invariant in ['-20', '-.2', '-1e-4', '1e-4', '.3', '1.4']:
        value = mp.mpf(invariant)
        checks.append(check('G real integral branch x=' + invariant, abs(g_closed(value) - g_integral(value)), 1e-65))
    for energy in ['0.00045962015785263325', '.001', '.1', '1', '9']:
        for cosine in ['-.9', '.1', '.6']:
            direct = brown_finite(energy, cosine)
            recast = recast_finite(energy, cosine)
            checks.append(check('Original1952 and recast2020 finite terms E=' + energy + ' c=' + cosine, abs(direct-recast) / max(abs(direct), mp.mpf('1e-40')), 1e-55))
            with mp.workdps(50):
                lower_precision = recast_finite(energy, cosine)
            checks.append(check('50/140 digit stability E=' + energy + ' c=' + cosine, abs(recast-lower_precision) / abs(recast), 1e-32))
            first, second, rapidity = kinematics(energy, cosine)
            gamma = 1 - first - second
            speed = mp.sqrt(1 - 1 / gamma ** 2)
            independent_cusp = 2 * mp.mpf(str(ALPHA)) / mp.pi * (mp.atanh(speed) / speed - 1)
            checks.append(check('Virtual logarithm matches conserved-current coefficient E=' + energy + ' c=' + cosine, abs(cusp(energy, cosine)-independent_cusp), 1e-70))
            rows.append(dict(energy=float(energy), cosine=float(cosine), finite_virtual_ratio=float(finite_virtual_ratio(energy, cosine)),
                cusp=float(cusp(energy, cosine)), soft_constant=float(soft_constant(energy, cosine)),
                literal_printed_G_argument_ratio=float(-mp.mpf(str(ALPHA))/mp.pi*recast_finite(energy,cosine,1)/compton(first,second))))
    for cosine in ['-.9', '.1', '.6']:
        angle = mp.mpf(cosine)
        expected = 1 + angle + angle ** 2 - angle ** 3 / 3
        errors = []
        for energy in ['1e-8', '1e-16', '1e-24']:
            value = mp.mpf(energy)
            actual = recast_finite(energy, cosine) / (4 * value ** 2 * mp.log(value))
            errors.append(float(abs(actual-expected) / abs(expected)))
        checks.append(dict(name='Brown-Feynman low-energy logarithm c=' + cosine, passed=errors[2] < errors[1] < errors[0] and errors[2] < .02, errors=errors))
    checks.append(dict(name='Literal h closed form fails its defining integral by factor12', passed=abs(12*h_closed(mp.mpf('.3'))/h_integral(mp.mpf('.3'))-12) < mp.mpf('1e-70')))
    checks.append(dict(name='Literal G(kappa0) instead of G(2kappa0) rejected by original formula', passed=all(abs(row['literal_printed_G_argument_ratio']-row['finite_virtual_ratio']) > 1e-4 for row in rows)))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        rows=rows, normalization='delta_virtual = -(alpha/pi)*Re[U1]/U in Brown-Feynman Gaussian convention; ALPHA=e_Gaussian^2',
        source_corrections=['Equation57 closed h needs denominator12y, not y', 'Equation63 G0 argument needs2kappa0 relative to Equation58 definition'],
        unpolarized_vacuum_only=True), __file__, [ROOT/'vacuum_virtual.py', ROOT/'sources/BROpr52.pdf',
        BRANCH/'scaled-spectral-evolution-20261007/sources/2005.06941v1.html'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
