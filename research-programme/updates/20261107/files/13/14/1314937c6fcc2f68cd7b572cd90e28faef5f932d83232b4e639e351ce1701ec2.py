import sympy as symbolic
from thermal_common import *


def main():
    modest()
    folder=ROOT/'results/derivation'
    folder.mkdir(parents=True,exist_ok=True)
    assert not (folder/'COMPLETE').exists()
    frequency,ratio,chemical,first,second=symbolic.symbols('x r mu t1 t2',positive=True)
    occupation=1/(symbolic.exp(frequency)-1)
    be=1/(symbolic.exp(frequency/ratio+chemical)-1)
    checks=[]
    def identity(name,expression):
        residual=symbolic.simplify(expression)
        checks.append(dict(name=name,passed=residual==0,residual=str(residual)))
        assert residual==0,(name,residual)
    identity('Bose-Einstein stationary flux',ratio*symbolic.diff(be,frequency)+be*(1+be))
    identity('Planck stationary flux',symbolic.diff(occupation,frequency)+occupation*(1+occupation))
    weight_expr=occupation*(1+occupation)
    identity('Detailed-balance integrating factor',symbolic.diff(weight_expr,frequency)+(1+2*occupation)*weight_expr)
    temperature_mode=-frequency*symbolic.diff(occupation,frequency)
    y_mode=symbolic.diff(frequency**4*symbolic.diff(occupation,frequency),frequency)/frequency**2
    identity('Temperature squared creates an independent y-shape',-frequency*symbolic.diff(temperature_mode,frequency)-3*temperature_mode-y_mode)
    wien_y=(frequency**2-4*frequency)*symbolic.exp(-frequency)
    wien_evolved=symbolic.expand(symbolic.diff(frequency**4*(symbolic.diff(wien_y,frequency)+wien_y),frequency)/frequency**2)
    identity('Kompaneets produces a cubic Wien shape outside temperature/y closure',wien_evolved-(-2*frequency**3+14*frequency**2-16*frequency)*symbolic.exp(-frequency))
    first_occupation=first*temperature_mode
    second_occupation=second*temperature_mode+first**2*(temperature_mode+y_mode/2)
    linear_flux=symbolic.diff(first_occupation,frequency)+(1+2*occupation)*first_occupation+first*symbolic.diff(occupation,frequency)
    quadratic_flux=(symbolic.diff(second_occupation,frequency)+(1+2*occupation)*second_occupation+
        second*symbolic.diff(occupation,frequency)+first*symbolic.diff(first_occupation,frequency)+first_occupation**2)
    identity('First-order moving thermal equilibrium',linear_flux)
    identity('Quadratic thermal equilibrium requires induced and temperature cross terms',quadratic_flux)
    potential=symbolic.Function('v')(frequency)
    identity('Spectral operator is self-adjoint flux in the detailed-balance weight',
        symbolic.diff(weight_expr*potential,frequency)+(1+2*occupation)*weight_expr*potential-weight_expr*symbolic.diff(potential,frequency))
    polynomial=frequency**2-8*frequency+12
    perturbation=symbolic.exp(-frequency)*polynomial
    identity('Counterexample preserves photon number',symbolic.integrate(frequency**2*perturbation,(frequency,0,symbolic.oo)))
    identity('Counterexample preserves bolometric energy',symbolic.integrate(frequency**3*perturbation,(frequency,0,symbolic.oo)))
    induced_linear=720*(2*symbolic.zeta(7)-1)-960*(2*symbolic.zeta(6)-1)+288*(2*symbolic.zeta(5)-1)
    induced_quadratic=symbolic.integrate(frequency**4*perturbation**2,(frequency,0,symbolic.oo))
    amplitude=.001
    change=float(amplitude*induced_linear+amplitude**2*induced_quadratic)
    checks.append(dict(name='Same number and energy but different recoil moment',passed=change>0,recoil_moment_difference=change))
    checks.append(dict(name='Counterexample remains strictly positive',passed=0<amplitude<.25,proof='n/nP=1+epsilon(1-exp(-x))*[(x-4)^2-4] >= 1-4epsilon > 0'))
    numerical=integrate.quad(lambda value:value**4*(planck(value)+amplitude*math.exp(-value)*(value**2-8*value+12))*(1+planck(value)+amplitude*math.exp(-value)*(value**2-8*value+12))-value**4*planck(value)*(1+planck(value)),1e-8,100,epsabs=1e-12)[0]
    checks.append(dict(name='Counterexample recoil difference independently integrated',passed=abs(numerical/change-1)<1e-9,relative_error=abs(numerical/change-1)))
    speed,heat=symbolic.symbols('v Q',real=True)
    gamma=1/symbolic.sqrt(1-speed**2)
    time_force=gamma*heat
    spatial_force=gamma*heat*speed
    identity('Rest-frame heat recovered from covariant four-force',gamma*(time_force-speed*spatial_force)-heat)
    identity('Equal/opposite photon and matter four-forces',time_force-time_force+spatial_force-spatial_force)
    identity('Boosted heat momentum begins with Q v',symbolic.diff(spatial_force,speed).subs(speed,0)-heat)
    grid=SpectralGrid(800)
    random=np.sin(np.log(grid.frequency))
    source=grid.source(random,.3)
    number_error=abs(grid.mass@source)/max(np.sum(abs(grid.mass*source)),1e-100)
    checks.append(dict(name='Discrete photon number is conserved',passed=number_error<1e-12,value=number_error))
    stationarity=float(np.max(abs(grid.source(grid.frequency,1.))))
    checks.append(dict(name='Discrete common temperature mode is stationary',passed=stationarity<1e-12,value=stationarity))
    chemical_error=float(np.max(abs(grid.source(np.ones(grid.count),0.))))
    checks.append(dict(name='Discrete chemical-potential mode is stationary',passed=chemical_error<1e-12,value=chemical_error))
    energy_coefficient=grid.temperature_energy
    checks.append(dict(name='Discrete thermal energy coefficient approaches four',passed=abs(energy_coefficient/4-1)<.001,value=energy_coefficient))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
        counterexample=dict(amplitude=amplitude,linear_recoil_moment=float(induced_linear),quadratic_recoil_moment=float(induced_quadratic),
            fractional_compton_temperature_change=change/(4*I3_PLANCK)),
        number_energy_closure_disproved=True,full_anisotropic_thermal_operator_not_implemented=True),__file__)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],compton_temperature_shift=change/(4*I3_PLANCK))),flush=True)


if __name__=='__main__':
    main()
