from thermal_dressed import *


def main():
    modest()
    mp.mp.dps=60
    energy=mp.mpf('.00045962015785263325')
    initial=mp.matrix([1,0,0,0])
    incoming=spin.photon(energy,spin.unit([0,0,1]))
    direction=spin.unit([.7,.2,.3])
    outgoing=spin.photon(energy/(1+energy*(1-direction[2])),direction)
    bath_direction=spin.unit([-.2,.8,-.1])
    first,second=spin.frame(spin.unit([0,0,1]))[0],spin.frame(direction)[0]
    physical=finite_dressed(initial,incoming,outgoing,first,second,bath_direction,energy)
    first_ward=finite_dressed(initial,incoming,outgoing,incoming/energy,second,bath_direction,energy)
    second_ward=finite_dressed(initial,incoming,outgoing,first,outgoing/outgoing[0],bath_direction,energy)
    print('finite',mp.nstr(mp.norm(physical),12),'ward',mp.nstr(mp.norm(first_ward),12),mp.nstr(mp.norm(second_ward),12),flush=True)


if __name__=='__main__':
    main()
