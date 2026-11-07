from thermal_radial import *


def main():
    modest()
    mp.mp.dps=65
    folder=ROOT/'results/pole-prescription'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows=[],[]
    for location in ['.03','.3','1','10']:
        scaled=mp.mpf(location)
        principal=thermal_hilbert(scaled)
        for sign in [-1,1]:
            expected=principal-mp.j*sign*mp.pi/(2*mp.expm1(scaled))
            differences=[]
            for relative in ['1e-8','1e-12']:
                regulator=mp.mpf(relative)*scaled**2
                argument=mp.sqrt(-scaled**2+sign*mp.j*regulator)/(2*mp.pi)
                continued=(mp.log(argument)-1/(2*argument)-mp.digamma(argument))/2
                differences.append(abs(continued-expected))
            checks.append(check('Feynman boundary value versus exact delta pole z='+location+' sign='+str(sign),differences[-1]/max(1,abs(expected)),1e-10))
            checks.append(check('Analytic i0 limit convergence z='+location+' sign='+str(sign),abs(differences[0]/differences[1]/mp.mpf('1e4')-1),1e-6))
            rows.append(dict(pole_over_temperature=float(scaled),denominator_prescription_sign=sign,
                             principal_value=float(principal),imaginary_part=float(mp.im(expected)),
                             last_analytic_continuation_error=float(differences[-1])))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
                       regulator_only_for_check_of_distributional_limit=True,
                       no_regulator_or_width_retained_in_physical_candidate=True),__file__,[ROOT/'thermal_radial.py'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
