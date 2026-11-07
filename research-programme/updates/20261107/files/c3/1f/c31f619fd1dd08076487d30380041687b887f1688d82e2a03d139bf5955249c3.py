from vacuum_soft_match import *


def main():
    modest()
    mp.mp.dps = 65
    folder = ROOT/'results/massive-regulator-match'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows = [], []
    for energy, cosine in [('0.00045962015785263325','-.5'), ('.1','.2'), ('1','-.9')]:
        separator = mp.mpf(energy) * mp.mpf('.001')
        expected = matched_soft_ratio(energy, cosine, separator)
        coefficient = cusp(energy, cosine)
        for ratio in ['1e-3','1e-6','1e-9']:
            photon_mass = separator * mp.mpf(ratio)
            real = massive_soft_integral(energy, cosine, separator, photon_mass)
            virtual = virtual_with_mass(energy, cosine, photon_mass)
            analytic = massive_soft_asymptotic(energy, cosine, separator, photon_mass)
            checks.append(check('Direct massive phase space versus Brown39 E='+energy+' lambda/Delta='+ratio, abs(real-analytic)/coefficient, 10*float(ratio)**2))
            checks.append(check('Finite real plus virtual match E='+energy+' lambda/Delta='+ratio, abs(real+virtual-expected)/coefficient, 10*float(ratio)**2))
            rows.append(dict(energy=float(energy),cosine=float(cosine), separator=float(separator), mass=float(photon_mass),
                real=float(real),virtual=float(virtual),sum=float(real+virtual),regulator_free=float(expected)))
        second = matched_soft_ratio(energy,cosine,separator/7)
        checks.append(check('Matching scale derivative fixed not fitted E='+energy, abs(expected-second-coefficient*mp.log(7)),1e-58))
        wrong = expected-soft_constant(energy,cosine)
        checks.append(dict(name='Dropping massive-regulator finite constant detected E='+energy, passed=abs(wrong-expected)>coefficient/2))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
        direct_massive_phase_space=True, laboratory_rest_electron=True,
        physical_separator_remains_until_resolved_real_added=True),__file__,[ROOT/'vacuum_soft_match.py',ROOT/'vacuum_virtual.py',ROOT/'sources/BROpr52.pdf'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],rows=rows)),flush=True)


if __name__=='__main__':
    main()
