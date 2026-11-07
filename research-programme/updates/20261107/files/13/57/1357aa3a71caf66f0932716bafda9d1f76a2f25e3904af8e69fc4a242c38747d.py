from soft_population import *
from fractions import Fraction
import mpmath as mp


def main():
    modest()
    mp.mp.dps=60
    folder=ROOT/'results/derived-soft-coefficient'
    folder.mkdir(parents=True,exist_ok=False)
    denominator=Fraction(8,3)
    numerator=Fraction(56,15)
    angular=numerator/denominator
    occupation=lambda frequency:1/mp.expm1(frequency)
    weight=lambda frequency:occupation(frequency)*(1+occupation(frequency))
    integral4=mp.quad(lambda frequency:frequency**4*weight(frequency),[0,1,5,20,mp.inf])
    integral6=mp.quad(lambda frequency:frequency**6*weight(frequency),[0,1,5,20,mp.inf])
    squared_weight=mp.quad(lambda frequency:frequency**6*weight(frequency)**2,[0,1,5,20,mp.inf])
    derivative_weight=mp.quad(lambda frequency:frequency**5*weight(frequency)*(1+2*occupation(frequency)),[0,1,5,20,mp.inf])
    first_order=-(6+mp.mpf(angular.numerator)/angular.denominator*(-3*derivative_weight+2*squared_weight)/integral4)
    closed=1+4*mp.pi**2/3
    checks=[dict(name='Thomson recoil angular ratio is exactly7/5',passed=angular==Fraction(7,5)),
            check('Planck fourth moment',abs(integral4/(4*mp.pi**4/15)-1),1e-50),
            check('Planck sixth-to-fourth ratio',abs(integral6/integral4-20*mp.pi**2/7),1e-48),
            check('Integrated occupation derivative identity',abs(derivative_weight/(5*integral4)-1),1e-50),
            check('Squared Bose weight identity',abs(squared_weight/(5*integral4-integral6/6)-1),1e-49),
            check('Population recoil and stimulation give exact closed coefficient',abs(first_order-closed),1e-47),
            dict(name='Published14.16 is rounded coefficient, not a fitted MTS parameter',passed=round(float(closed),2)==14.16)]
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
                       exact_first_order_coefficient='1+4*pi^2/3',coefficient=float(closed),
                       first_order_gaunt='g(theta)=1-(1+4*pi^2/3)*theta+O(theta^2)',
                       inverse_ansatz_not_proven_beyond_first_order=True,
                       fine_structure_and_electron_mass_inherited=True),__file__,[ROOT/'soft_population.py',
                       BACKGROUND/'emission_rates.py',BACKGROUND/'integrated_dc.py'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],coefficient=float(closed))),flush=True)


if __name__=='__main__':
    main()
