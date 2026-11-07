import functools
from vacuum_virtual import *


def iterated_series(word, order):
    @functools.lru_cache(None)
    def build(letters):
        if not letters:
            return {(0,0):mp.mpf(1)}
        if letters==(0,):
            return {(0,1):mp.mpf(1)}
        letter=letters[0]
        tail=build(letters[1:])
        if letter=='y':
            weights=[(2*degree-1,mp.binomial(-mp.mpf('.5'),degree)/(2*4**degree)) for degree in range(order+1)]
        elif letter==0:
            weights=[(-2,mp.mpf(1))]
        else:
            weights=[(2*degree,-mp.mpf(letter)**(-degree-1)) for degree in range(order+1)]
        result={}
        for (power,log_power),coefficient in tail.items():
            for weight_power,weight in weights:
                integrated_power=power+weight_power+2
                if integrated_power>2*order:
                    continue
                if integrated_power==0:
                    key=(0,log_power+1)
                    result[key]=result.get(key,0)+coefficient*weight/(log_power+1)
                    continue
                assert integrated_power>0
                denominator=mp.mpf(integrated_power)/2
                for position in range(log_power+1):
                    key=(integrated_power,log_power-position)
                    value=coefficient*weight*(-1)**position*mp.factorial(log_power)/mp.factorial(log_power-position)/denominator**(position+1)
                    result[key]=result.get(key,0)+value
        return result
    return build(tuple(word))


def iterated(word, argument, order=70):
    argument=mp.mpf(argument)
    if not 0<argument<1:
        raise ValueError('Power-log evaluation is certified only inside 0<x<1')
    coefficients=iterated_series(tuple(word),order)
    logarithm=mp.log(argument)
    return mp.fsum(coefficient*argument**(mp.mpf(power)/2)*logarithm**log_power for (power,log_power),coefficient in coefficients.items())


def born_scaled(energy):
    argument=2*mp.mpf(str(energy))
    return mp.pi/(argument+1)*((argument**3+18*argument**2+32*argument+16)/(argument**2*(argument+1))
        +(2*argument**3-6*argument**2-24*argument-16)/argument**3*mp.log1p(argument))


def nlo_scaled(energy, order=70):
    argument=2*mp.mpf(str(energy))
    root=mp.sqrt(argument/(argument+4))
    logarithm=mp.log(argument)
    shifted_log=mp.log1p(argument)
    poly2=lambda value:mp.polylog(2,value)
    poly3=lambda value:mp.polylog(3,value)
    integral=lambda *word:iterated(word,argument,order)
    result=-argument*(273*argument**3-982*argument**2-2960*argument-1744)/(24*(argument+1)**2)
    result+=(37*argument**4-54*argument**3-339*argument**2-428*argument-184)/(4*(argument+1)**2)*shifted_log
    result+=argument**2*(14*argument**4+17*argument**3-17*argument**2-22*argument-8)/(2*(1-argument)*(1+argument)**3)*logarithm
    result-=(4*argument**6+35*argument**5-31*argument**4-755*argument**3-1765*argument**2-1506*argument-440)/(2*(argument+1)**2*(argument+4))*shifted_log**2
    result-=(argument**6+7*argument**5-28*argument**4-239*argument**3-449*argument**2-338*argument-88)/((argument+1)**2*(argument+4))*poly2(-argument)
    result-=(argument**2-16*argument-23)*shifted_log**3/3
    result+=(argument**2-argument+2)*(poly2(1-argument)-mp.pi**2/6)
    result+=(argument**4+7*argument**3+argument**2-3*argument-2)/(argument+1)**2*shifted_log*logarithm
    result+=(argument**2+2*argument-6)*(poly3(argument**2)-poly2(argument**2)*logarithm)
    result-=4*(argument**5+26*argument**4+146*argument**3+316*argument**2+288*argument+96)/((argument+1)**2*(argument+4))*integral(-2,-1)
    result+=8*(argument**2-4*argument-6)*integral(-1,-2,-1)
    result+=4*(2*argument**2-argument-6)*integral(-1,-1,0)
    result+=2*(2*argument**2-7*argument-12)*integral(-1,0,-1)
    result-=(5*argument**2+32*argument-8)*integral(0,-1,-1)
    result-=3*(argument-2)*(argument+4)*root*(integral(0,'y',-1)+2*integral('y',-1,0))
    result-=8*root*(argument**4+3*argument**3-18*argument**2-68*argument-24)/((argument+4)*argument)*integral('y',0,-1)
    result+=3*root*(5*argument**4+14*argument**3-96*argument**2-352*argument-128)/((argument+4)*argument)*integral('y',-1,-1)
    result-=16*root*(argument**4+2*argument**3-24*argument**2-80*argument-48)/((argument+4)*argument)*integral('y',-2,-1)
    result+=(3*argument**4+18*argument**3+44*argument**2-8*argument-64)/argument*root*integral('y',-1)
    result-=6*root*(argument**3-12*argument-8)/argument*integral(-4,'y',-1)
    result+=3*(3*argument**2-8)*integral('y','y',-1)
    return result/argument**3
