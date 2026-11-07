from thermal_dressed import *


def main():
    modest()
    mp.mp.dps=65
    folder=ROOT/'results/dressed-finite-ward'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows=[],[]
    initial=mp.matrix([1,0,0,0])
    direction=spin.unit([.7,.2,.3])
    for energy_text in ['.00045962015785263325','.01']:
        energy=mp.mpf(energy_text)
        incoming=spin.photon(energy,spin.unit([0,0,1]))
        outgoing=spin.photon(energy/(1+energy*(1-direction[2])),direction)
        for bath_index,bath_coordinates in enumerate([[-.2,.8,-.1],[.4,-.3,.7]]):
            bath_direction=spin.unit(bath_coordinates)
            for first,second in itertools.product([0,1],repeat=2):
                first_pol,second_pol=spin.frame(spin.unit([0,0,1]))[first],spin.frame(direction)[second]
                physical=finite_dressed(initial,incoming,outgoing,first_pol,second_pol,bath_direction,energy)
                incoming_ward=finite_dressed(initial,incoming,outgoing,incoming/energy,second_pol,bath_direction,energy)
                outgoing_ward=finite_dressed(initial,incoming,outgoing,first_pol,outgoing/outgoing[0],bath_direction,energy)
                label=' E='+energy_text+' bath='+str(bath_index)+' pol='+str((first,second))
                checks.append(check('Finite radial amplitude incoming Ward'+label,mp.norm(incoming_ward)/mp.norm(physical),1e-43))
                checks.append(check('Finite radial amplitude outgoing Ward'+label,mp.norm(outgoing_ward)/mp.norm(physical),1e-43))
                rows.append(dict(energy=float(energy),bath_direction=bath_index,polarizations=[first,second],
                                 amplitude_norm=float(mp.norm(physical)),incoming_ward_norm=float(mp.norm(incoming_ward)),
                                 outgoing_ward_norm=float(mp.norm(outgoing_ward))))
        bath=spin.photon(mp.mpf(1),spin.unit([-.2,.8,-.1]))
        first_pol,second_pol=spin.frame(spin.unit([0,0,1]))[0],spin.frame(direction)[0]
        def dressed_tree(epsilon):
            sample=dressed_event(energy,direction,bath,epsilon)
            matrix=compton(sample['initial'],sample['incoming'],sample['outgoing'],first_pol,second_pol)
            return sample['final_states'].transpose_conj()*spin.gamma_matrices()[0]*matrix*sample['initial_states']
        delta=mp.mpf('1e-20')
        finite_difference=(dressed_tree(delta)-dressed_tree(-delta))/(2*delta)
        final=initial+incoming-outgoing
        tree=dressed_tree(mp.mpf(0))
        finite_residue=-1/(initial[0]*spin.dot(initial,bath))-1/(final[0]*spin.dot(final,bath))
        exact=external_finite_constant(initial,incoming,outgoing,first_pol,second_pol,bath)
        checks.append(check('Analytic external kinematic/spinor derivative E='+energy_text,
                            mp.norm(exact-finite_difference-finite_residue*tree)/mp.norm(exact),1e-28))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
                       finite_dressed_radial_amplitude_transverse=True,
                       bare_mass_and_photon_dispersion_inherited=True,
                       common_soft_subtraction_scheme_required_for_real_matching=True),__file__,
           [ROOT/'thermal_dressed.py',ROOT/'thermal_radial.py',ROOT/'thermal_insertions.py'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
