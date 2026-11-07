from thermal_insertions import *
from emission_rates import ALPHA


def main():
    modest()
    mp.mp.dps=65
    folder=ROOT/'results/ward-and-dressing'
    assert not (folder/'COMPLETE').exists()
    folder.mkdir(parents=True,exist_ok=True)
    checks,rows=[],[]
    for scale in ['.07','.00045962015785263325']:
        energy=mp.mpf(scale)
        initial=mp.matrix([mp.mpf('1.13'),mp.mpf('.1'),mp.mpf('-.04'),mp.mpf('.2')])
        incoming=spin.photon(energy,spin.unit([0,0,1]))
        direction=spin.unit([.7,.2,.3])
        outgoing=spin.photon(energy*mp.mpf('.57'),direction)
        bath=spin.photon(energy*mp.mpf('.24'),spin.unit([-.2,.8,-.1]))
        for state in [0,1]:
            polarization=spin.frame(direction)[state]
            difference=vertex(initial+incoming,initial,incoming,bath)-self_energy(initial,bath)+self_energy(initial+incoming,bath)
            checks.append(check('Off-shell one-photon Ward E='+scale+' pol='+str(state),mp.norm(difference),1e-54))
            left=compton(initial,incoming,outgoing,incoming,polarization,bath)
            right=incoming_ward_rhs(initial,incoming,outgoing,polarization,bath)
            checks.append(check('Eight-insertion off-shell Ward E='+scale+' pol='+str(state),mp.norm(left-right)/mp.norm(left),1e-54))
            for spatial in [[0,0,0],[mp.mpf('.1'),mp.mpf('-.2'),mp.mpf('.04')]]:
                momentum=on_shell(spatial)
                checks.append(check('On-shell self-energy exact E='+scale+' p='+str(spatial),
                                    mp.norm(self_energy(momentum,bath)-2*spin.slash(bath)/spin.dot(momentum,bath)),1e-52))
                shift,correction=external_shift(momentum,bath)
                checks.append(check('Photon-cut pole dispersion E='+scale+' p='+str(spatial),abs(shift-2/momentum[0]),1e-54))
                defect=inverse(momentum)*correction+(shift*spin.gamma_matrices()[0]-self_energy(momentum,bath))*spin.spinors(momentum)
                checks.append(check('External spinor equation E='+scale+' p='+str(spatial),mp.norm(defect),1e-53))
            for ward_leg in [0,1]:
                norms=[]
                controls=[]
                for epsilon in [mp.mpf('1e-14'),mp.mpf('1e-16')]:
                    sample=dressed_event(energy,direction,bath,epsilon)
                    incoming_pol=spin.frame(spin.unit([0,0,1]))[state]
                    outgoing_pol=polarization
                    if ward_leg==0:
                        incoming_pol=sample['incoming']/energy
                    else:
                        outgoing_pol=sample['outgoing']/sample['outgoing'][0]
                    bare=compton(sample['initial'],sample['incoming'],sample['outgoing'],incoming_pol,outgoing_pol)
                    loop=compton(sample['initial'],sample['incoming'],sample['outgoing'],incoming_pol,outgoing_pol,bath)
                    left_states=sample['final_states'].transpose_conj()*spin.gamma_matrices()[0]
                    norms.append(mp.norm(left_states*(bare+epsilon*loop)*sample['initial_states']))
                    controls.append(mp.norm(left_states*bare*sample['initial_states']))
                ratio=norms[0]/norms[1]
                checks.append(check('Dressed Ward quadratic convergence E='+scale+' leg='+str(ward_leg)+' pol='+str(state),abs(ratio/mp.mpf('1e4')-1),1e-5))
                checks.append(dict(name='Omitting thermal insertion fails dressed Ward E='+scale+' leg='+str(ward_leg)+' pol='+str(state),passed=bool(controls[-1]>1000*norms[-1])))
                rows.append(dict(energy=float(energy),ward_leg=ward_leg,polarization=state,
                                 small_epsilon=1e-16,ward_norm=float(norms[-1]),quadratic_ratio=float(ratio),
                                 missing_insertion_norm=float(controls[-1])))
        bare_initial=mp.matrix([1,0,0,0])
        hard=spin.photon(energy/(1+energy*(1-direction[2])),direction)
        final=bare_initial+incoming-hard
        left_states=spin.spinors(final).transpose_conj()*spin.gamma_matrices()[0]
        internal=left_states*compton(bare_initial,incoming,hard,incoming/energy,spin.frame(direction)[0],bath)*spin.spinors(bare_initial)
        checks.append(dict(name='Internal-only on-shell Ward defect detected E='+scale,passed=bool(mp.norm(internal)>mp.mpf('1e-4'))))
        wrong=compton(initial,incoming,outgoing,incoming,spin.frame(direction)[0],bath,omit='box')
        rhs=incoming_ward_rhs(initial,incoming,outgoing,spin.frame(direction)[0],bath)
        checks.append(dict(name='Omitting spanning box fails off-shell Ward E='+scale,passed=bool(mp.norm(wrong-rhs)>mp.mpf('1e-6'))))
    integral=mp.quad(lambda value: value/mp.expm1(value),[0,1,mp.inf])
    checks.append(check('Planck radial moment equals pi squared over six',abs(integral-mp.pi**2/6),1e-58))
    for temperature in [mp.mpf('.00045962015785263325'),mp.mpf('.01')]:
        mass_shift=4*mp.pi*mp.mpf(str(ALPHA))*temperature**2/(2*mp.pi**2)*integral
        expected=mp.pi*mp.mpf(str(ALPHA))*temperature**2/3
        checks.append(check('Thermal mass normalization T='+str(temperature),abs(mass_shift/expected-1),1e-58))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
                       off_shell_pointwise_photon_cut_ward=True,perturbative_external_poles_and_spinors=True,
                       external_residue_inclusive_cancellation_not_yet_integrated=True),__file__,
           [ROOT/'thermal_insertions.py',AMPLITUDE_PARENT/'dirac_amplitude.py',PARENT/'sources/Varma1992.pdf'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],rows=rows)),flush=True)


if __name__=='__main__':
    main()
