from spatial_defect_common import *
from fractions import Fraction


def falling(value,count):
    result=1
    for index in range(count):
        result*=value-index
    return result


def main():
    modest()
    folder=ROOT/'results/inner-counterpart'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    half=Fraction(1,2)
    position=Fraction(7,6)
    for inverse in [Fraction(4,5),Fraction(10,9),Fraction(7,6)]:
        for power in [-3,-2,-1,0,1,2,4]:
            def derivative(point,order):
                return falling(power,order)*point**(power-order)
            second=half*(2*position*inverse**-3*derivative(position/inverse,1)
                +position**2*inverse**-4*derivative(position/inverse,2)
                +6*inverse*derivative(position*inverse,0)
                +6*inverse**2*position*derivative(position*inverse,1)
                +inverse**3*position**2*derivative(position*inverse,2)-2*derivative(position,0))
            third=half*(-6*position*inverse**-4*derivative(position/inverse,1)
                -6*position**2*inverse**-5*derivative(position/inverse,2)
                -position**3*inverse**-6*derivative(position/inverse,3)
                +6*derivative(position*inverse,0)+18*inverse*position*derivative(position*inverse,1)
                +9*inverse**2*position**2*derivative(position*inverse,2)
                +inverse**3*position**3*derivative(position*inverse,3))
            for order,value in [(2,second),(3,third)]:
                exact=half*position**power*(falling(-power,order)*inverse**(-power-order)
                    +falling(power+3,order)*inverse**(power+3-order)
                    -falling(1,order)*inverse**(1-order)-falling(2,order)*inverse**(2-order))
                checks.append(dict(name=f'Exact inner derivative:{inverse}:{power}:{order}',passed=value==exact))
            source_power=-power-2
            inner=half*(inverse**(-power)+inverse**(power+3)-inverse-inverse**2)
            source=half*(inverse**(1-source_power)+inverse**(2+source_power)-inverse-inverse**2)
            checks.append(dict(name=f'Exact Mellin duality:{inverse}:{power}',passed=inner==source))
            if power in [-1,-2]:
                checks.append(dict(name=f'Exact null mode:{inverse}:{power}',passed=second==third==inner==0))
            for test_power in [0,1,3]:
                exponent=power+test_power+2
                if exponent==0:
                    continue
                lower,upper=Fraction(2,3),Fraction(5,2)
                def integral(first,last):
                    return (last**exponent-first**exponent)/exponent
                domain=integral(lower,upper)
                weak=half*(inverse**(1-test_power)+inverse**(2+test_power)-inverse-inverse**2)
                boundary=half*inverse**(2+test_power)*(integral(lower/inverse,upper/inverse)-domain)
                boundary+=half*inverse**(1-test_power)*(integral(lower*inverse,upper*inverse)-domain)
                checks.append(dict(name=f'Exact finite boundary:{inverse}:{power}:{test_power}',passed=(inner-weak)*domain==boundary))
    assert all(row['passed'] for row in checks),[row for row in checks if not row['passed']]
    finish(folder,dict(checks=checks,arithmetic='exact rational',source_inner_adjoint_derived=True,
        corrected_inner_implemented=False,positivity_or_time_stability_claim=False),
        __file__,[ROOT/'INNER-CORRECTION-CONTRACT.md'])
    print(json.dumps(dict(checks=len(checks),all_pass=True)),flush=True)


if __name__=='__main__':
    main()
