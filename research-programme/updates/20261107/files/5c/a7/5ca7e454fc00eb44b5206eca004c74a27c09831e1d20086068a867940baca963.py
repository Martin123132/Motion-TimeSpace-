from ordered_real_kernel import *
import dirac_amplitude as spin


def main():
    modest()
    mp.mp.dps=140
    folder=ROOT/'results/low-energy-and-real-amplitude'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows=[],[]
    for cosine in ['-.9','.1','.6']:
        angle=mp.mpf(cosine)
        expected=1+angle+angle**2-angle**3/3
        first,second=mp.mpf('1e-14'),mp.mpf('1e-20')
        logarithmic_slope=(recast_finite(first,cosine)/first**2-recast_finite(second,cosine)/second**2)/(4*mp.log(first/second))
        checks.append(check('Leading low-energy log isolated without O(E^2) contamination c='+cosine,abs(logarithmic_slope-expected),1e-11))
        rows.append(dict(cosine=float(angle),expected_log_coefficient=float(expected),measured_log_slope=float(logarithmic_slope)))
    for energy,cosine in [('1','0'),('10','-.9')]:
        high=recast_finite(energy,cosine)
        with mp.workdps(100):
            medium=recast_finite(energy,cosine)
            direct=brown_finite(energy,cosine)
        checks.append(check('Removable kappa=1 limit accuracy E='+energy,abs(high-medium),1e-42))
        checks.append(check('Original and recast removable limit E='+energy,abs(high-direct),1e-42))
    mp.mp.dps=80
    for energy in ['0.00045962015785263325','.1','1']:
        for fraction in ['.0001','.1','.3']:
            sample=spin.event(energy,fraction,[.7,.2,-.3],[-.3,.5,.6])
            cosines=[sum(sample['directions'][left][index]*sample['directions'][right][index] for index in range(3)) for left,right in [(0,1),(0,2),(1,2)]]
            value,companion,denominator=amplitude_squared(mp.mpf(energy),mp.mpf(energy)*mp.mpf(fraction),*[1-cosine for cosine in cosines])
            tensor=spin.tensor_for_event(sample)
            numeric=float(np.vdot(tensor,tensor).real/4)
            checks.append(check('Real kernel matches six-diagram spin/polarization sum E='+energy+' fraction='+fraction,abs(float(value)-numeric)/numeric,2e-13))
    for energy in ['0.00045962015785263325','.1','1']:
        values=geometry(mp.mpf(energy),mp.mpf('.2'),mp.mpf('-.4'),mp.mpf('.7'))
        pole=pole_density(*values)
        for share in ['1e-4','1e-7','1e-10']:
            emitted=mp.mpf(energy)*mp.mpf(share)
            checks.append(check('Real phase-space soft coefficient E='+energy+' share='+share,abs(emitted*real_density(values[0],emitted,*values[1:])/pole-1),5*float(share)))
        upper=ordered_upper(*values)
        squared,companion,denominator=amplitude_squared(values[0],upper,*values[1:])
        checks.append(check('Ordered boundary exactly equal outgoing energies E='+energy,abs(companion-upper),1e-65))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),logarithm_rows=rows,
        prior_failed_test_interpretation='The raw finite-virtual packet used a 2% test on a logarithmically convergent ratio. The O(E^2) constant is retained there; this difference quotient cancels it analytically instead of loosening that threshold.'),__file__,
        [ROOT/'vacuum_virtual.py',ROOT/'ordered_real_kernel.py',PARENT/'dirac_amplitude.py',ROOT/'results/finite-virtual/status.json'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],rows=rows)),flush=True)


if __name__=='__main__':
    main()
