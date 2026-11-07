from common import *
import numpy as np
import sympy as sp
from source_adapter import other_density


def symbolic():
    theta, inverse, eta0, fraction = sp.symbols('theta u eta0 f', real=True)
    coefficient_a=sp.Rational(3,2)*(1-eta0)
    coefficient_b=sp.Rational(9,8)*(2-fraction)
    eta=eta0+sp.Rational(3,2)*fraction*sp.cos(2*theta)
    theta_rate=1/inverse-sp.Rational(3,2)*sp.sin(2*theta)
    inverse_rate=inverse*(eta-1)
    correction1=sp.Rational(3,2)*inverse*sp.sin(2*theta)
    first_rate=sp.diff(correction1,theta)*theta_rate+sp.diff(correction1,inverse)*inverse_rate
    checks=dict(first_corrector=sp.trigsimp(3*sp.cos(2*theta)-first_rate-inverse*(coefficient_a*sp.sin(2*theta)+coefficient_b*sp.sin(4*theta))))
    coefficient_a,coefficient_b,rate_a,rate_b,eta=sp.symbols('A B AN BN eta',real=True)
    correction2=-coefficient_a*inverse**2*sp.cos(2*theta)/2-coefficient_b*inverse**2*sp.cos(4*theta)/4
    second_rate=(sp.diff(correction2,theta)*theta_rate+sp.diff(correction2,inverse)*inverse*(eta-1)
                 +sp.diff(correction2,coefficient_a)*rate_a+sp.diff(correction2,coefficient_b)*rate_b)
    residual=inverse**2*((rate_a/2+coefficient_a*(eta-1))*sp.cos(2*theta)
                        +(rate_b/4+coefficient_b*(eta-1)/2)*sp.cos(4*theta)
                        +sp.Rational(3,2)*sp.sin(2*theta)*(coefficient_a*sp.sin(2*theta)+coefficient_b*sp.sin(4*theta)))
    checks['second_corrector']=sp.trigsimp(inverse*(coefficient_a*sp.sin(2*theta)+coefficient_b*sp.sin(4*theta))-second_rate-residual)
    speed=sp.symbols('v',real=True)
    checks['free_gas_second_derivative']=sp.expand((1+speed**2)**2+2*speed**2*(1-speed**2)-(1+4*speed**2-speed**4))
    require(all(value==0 for value in checks.values()),'phase invariant identities')
    return {name:str(value) for name,value in checks.items()}


def other_derivative(native,efold,width=1e-3):
    efold=np.atleast_1d(efold)
    values=[other_density(native,np.exp(efold+shift*width)) for shift in (-2,-1,1,2)]
    return (values[0]-8*values[1]+8*values[2]-values[3])/(12*width)


def invariant(scale,fields,velocities,masses,hubble,other_rate):
    omega=scale[:,None]*masses
    rho=(velocities**2+(omega*fields)**2)/2
    theta=np.arctan2(-velocities[:,1],omega[:,1]*fields[:,1])
    inverse=hubble/omega[:,1]
    eta0=(other_rate-2*velocities[:,0]**2+(omega[:,0]*fields[:,0])**2-rho[:,1])/(6*hubble**2)
    fraction=rho[:,1]/(3*hubble**2)
    coefficient_a=1.5*(1-eta0)
    coefficient_b=1.125*(2-fraction)
    first=1.5*inverse*np.sin(2*theta)
    second=-.5*coefficient_a*inverse**2*np.cos(2*theta)-.25*coefficient_b*inverse**2*np.cos(4*theta)
    logarithm=np.log((scale*rho[:,1])/(scale[0]*rho[0,1]))
    return dict(rho=rho,theta=theta,inverse=inverse,eta0=eta0,fraction=fraction,first=first,second=second,
                invariant=logarithm-first-second)


def tube_parameters(initial_scale,final_scale,masses,rho,other,cold_density,initial_hubble,first,second):
    inverse=initial_hubble/(initial_scale*masses[1])
    maximum_slow_ratio=np.sqrt(3)*masses[0]*final_scale**1.5/np.sqrt(initial_scale*cold_density)
    bootstrap=1e-4
    heavy_log_bound=abs(first+second)+1.5*inverse+2.8125*inverse**2+bootstrap
    matter_coefficient=(other+rho[1]*np.exp(heavy_log_bound))/(3*(initial_scale*masses[1])**2)
    slow_coefficient=rho[0]/(3*(initial_scale*masses[1])**2)
    coefficient=41.25+2.25*maximum_slow_ratio
    span=np.log(final_scale/initial_scale)
    drift=coefficient*(matter_coefficient*(-np.expm1(-3*span))/3+slow_coefficient*span)
    require(inverse>0 and inverse<.01 and drift<bootstrap,'invariant bootstrap does not close')
    return dict(initial_scale=float(initial_scale),final_scale=float(final_scale),inverse_initial=float(inverse),
                maximum_slow_ratio=float(maximum_slow_ratio),bootstrap=bootstrap,heavy_log_bound=float(heavy_log_bound),
                matter_coefficient=float(matter_coefficient),slow_coefficient=float(slow_coefficient),
                residual_coefficient=float(coefficient),final_drift_bound=float(drift),invariant_initial=float(-first-second),
                initial_heavy_density=float(rho[1]))


def tube(parameters,efold):
    efold=np.asarray(efold)
    elapsed=efold-np.log(parameters['initial_scale'])
    require(np.min(elapsed)>=-ALGEBRA and np.max(efold)<=np.log(parameters['final_scale'])+ALGEBRA,'tube domain')
    inverse_upper=np.sqrt(parameters['matter_coefficient']*np.exp(-3*elapsed)+parameters['slow_coefficient'])
    inverse_upper=np.minimum(inverse_upper,parameters['inverse_initial'])
    drift=parameters['residual_coefficient']*(parameters['matter_coefficient']*(-np.expm1(-3*elapsed))/3+parameters['slow_coefficient']*elapsed)
    width=1.5*inverse_upper+2.8125*inverse_upper**2+drift
    mean=parameters['initial_heavy_density']*np.exp(-elapsed+parameters['invariant_initial'])
    return mean,width,drift,inverse_upper
