from independent_total import *


def main():
    modest()
    mp.mp.dps=100
    folder=ROOT/'results/independent-total-reference'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows=[],[]
    for argument in ['.001','.02','.2']:
        value=mp.mpf(argument)
        logarithm=mp.log1p(value)
        formulas={
            (-2,-1):mp.polylog(2,-value-1)+logarithm*mp.log(value+2)+mp.pi**2/12,
            (-1,-2,-1):2*mp.polylog(3,-value-1)-mp.polylog(2,-value-1)*logarithm+mp.pi**2/12*logarithm+3*mp.zeta(3)/2,
            (-1,-1,0):mp.polylog(3,-value)+mp.polylog(3,value/(value+1))+logarithm**2*mp.log(value)/2-logarithm**3/6,
            (-1,0,-1):-2*mp.polylog(3,-value)-2*mp.polylog(3,value/(value+1))+mp.polylog(2,-value)*logarithm+logarithm**3/3,
            (0,-1,-1):mp.polylog(3,-value)+mp.polylog(3,value/(value+1))-mp.polylog(2,-value)*logarithm-logarithm**3/6}
        for word,expected in formulas.items():
            checks.append(check('Iterated definition versus published closed G='+str(word)+' x='+argument,abs(iterated(word,value)-expected),1e-45))
        direct=mp.quad(lambda position: mp.log1p(position)/mp.sqrt(position*(position+4)),[0,value])
        checks.append(check('Square-root weight G(y,-1) direct quadrature x='+argument,abs(iterated(('y',-1),value)-direct),1e-45))
    for energy in ['0.00045962015785263325','.01','.1','1e-8']:
        value=nlo_scaled(energy,70)
        reference=nlo_scaled(energy,90)
        checks.append(check('Independent total series70/90 E='+energy,abs(value-reference)/abs(reference),1e-38))
        rows.append(dict(energy=float(energy),nlo_over_alpha3=float(reference),born_over_alpha2=float(born_scaled(energy)),
            relative_nlo=float(mp.mpf(str(ALPHA))*reference/born_scaled(energy))))
    energy=mp.mpf('1e-8')
    argument=2*energy
    constant=nlo_scaled(energy,40)/argument**2+mp.mpf(16)/9*mp.log(argument)
    checks.append(check('Independent analytic threshold constant7/15',abs(constant-mp.mpf(7)/15),1e-5))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
        source='Lee-Schwartz-Zhang2021 Equations5-8; no Brown-Feynman functions or DC angular kernel used in this reference',
        threshold_constant=float(constant),series_domain='0<x=2E<1; tested throughx=.2; orders70/90'),__file__,
        [ROOT/'independent_total.py',ROOT/'sources/2102.06718v2.html'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],rows=rows,threshold_constant=float(constant))),flush=True)


if __name__=='__main__':
    main()
