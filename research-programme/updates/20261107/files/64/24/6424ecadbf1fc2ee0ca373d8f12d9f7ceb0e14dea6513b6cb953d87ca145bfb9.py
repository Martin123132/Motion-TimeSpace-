from thermal_radial import *


def main():
    modest()
    mp.mp.dps=65
    energy=mp.mpf('.00045962015785263325')
    initial=mp.matrix([1,0,0,0])
    hard_direction=spin.unit([.7,.2,.3])
    bath_direction=spin.unit([-.2,.8,-.1])
    incoming=spin.photon(energy,spin.unit([0,0,1]))
    outgoing=spin.photon(energy/(1+energy*(1-hard_direction[2])),hard_direction)
    first_pol=spin.frame(spin.unit([0,0,1]))[0]
    second_pol=spin.frame(hard_direction)[0]
    coefficients=radial_decomposition(initial,incoming,outgoing,first_pol,second_pol,bath_direction)
    for ratio in ['.03','.3','.9','1.2','3','20']:
        radial=energy*mp.mpf(ratio)
        actual=compton(initial,incoming,outgoing,first_pol,second_pol,spin.photon(radial,bath_direction))
        expected=reconstruct(coefficients,radial)
        print('ratio',ratio,'reconstruction',mp.nstr(mp.norm(actual-expected)/mp.norm(actual),8),flush=True)
    print('poles',[(mp.nstr(pole['location']/energy,14),float(pole['denominator_slope_sign'])) for pole in coefficients['poles']],flush=True)
    for location in ['.1','.3','1','2','10']:
        print('J',location,mp.nstr(thermal_hilbert(mp.mpf(location)),20),flush=True)


if __name__=='__main__':
    main()
