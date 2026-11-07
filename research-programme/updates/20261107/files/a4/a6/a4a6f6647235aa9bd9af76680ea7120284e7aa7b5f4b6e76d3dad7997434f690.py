from thermal_insertions import *


def main():
    modest()
    mp.mp.dps=65
    initial=mp.matrix([mp.mpf('1.13'),mp.mpf('.1'),mp.mpf('-.04'),mp.mpf('.2')])
    incoming=spin.photon(mp.mpf('.07'),spin.unit([0,0,1]))
    outgoing=spin.photon(mp.mpf('.04'),spin.unit([.7,.2,.3]))
    bath=spin.photon(mp.mpf('.017'),spin.unit([-.2,.8,-.1]))
    polarization=spin.frame(spin.unit([.7,.2,.3]))[0]
    difference=vertex(initial+incoming,initial,incoming,bath)-self_energy(initial,bath)+self_energy(initial+incoming,bath)
    left=compton(initial,incoming,outgoing,incoming,polarization,bath)
    right=incoming_ward_rhs(initial,incoming,outgoing,polarization,bath)
    print('vertex',mp.nstr(mp.norm(difference),8),'compton',mp.nstr(mp.norm(left-right)/mp.norm(left),8),flush=True)
    initial=mp.matrix([1,0,0,0])
    print('self',mp.nstr(mp.norm(self_energy(initial,bath)-2*spin.slash(bath)/spin.dot(initial,bath)),8),flush=True)
    for epsilon in ['1e-6','1e-8','1e-10']:
        sample=dressed_event(mp.mpf('.07'),spin.unit([.7,.2,.3]),bath,mp.mpf(epsilon))
        matrix=compton(sample['initial'],sample['incoming'],sample['outgoing'],sample['incoming'],polarization)
        correction=compton(sample['initial'],sample['incoming'],sample['outgoing'],sample['incoming'],polarization,bath)
        result=sample['final_states'].transpose_conj()*spin.gamma_matrices()[0]*(matrix+mp.mpf(epsilon)*correction)*sample['initial_states']
        print('dressed',epsilon,mp.nstr(mp.norm(result),10),flush=True)


if __name__=='__main__':
    main()
