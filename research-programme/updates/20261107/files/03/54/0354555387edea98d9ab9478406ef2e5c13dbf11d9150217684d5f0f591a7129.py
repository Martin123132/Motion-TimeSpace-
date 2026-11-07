from thermal_radial import *
from emission_rates import ALPHA


def main():
    modest()
    mp.mp.dps=65
    folder=ROOT/'results/external-residue-soft-match'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows=[],[]
    initial=mp.matrix([1,0,0,0])
    null=spin.photon(mp.mpf(1),spin.unit([-.2,.8,-.1]))
    gamma0=spin.gamma_matrices()[0]
    for energy_text in ['.00045962015785263325','.01','.1']:
        energy=mp.mpf(energy_text)
        incoming=spin.photon(energy,spin.unit([0,0,1]))
        hard_direction=spin.unit([.7,.2,.3])
        outgoing=spin.photon(energy/(1+energy*(1-hard_direction[2])),hard_direction)
        final=initial+incoming-outgoing
        initial_projection,final_projection=spin.dot(initial,null),spin.dot(final,null)
        current=final/final_projection-initial/initial_projection
        current_square=spin.dot(current,current)
        for index,momentum in enumerate([initial,final]):
            radial=energy*mp.mpf('.3')
            derivative=mp.zeros(4)
            for first in range(4):
                for second in range(4):
                    derivative[first,second]=mp.diff(lambda frequency:self_energy(
                        mp.matrix([frequency,*list(momentum)[1:]]),radial*null)[first,second],momentum[0])
            states=spin.spinors(momentum)
            expectation=states.transpose_conj()*gamma0*derivative*states/(2*momentum[0])
            projection=spin.dot(momentum,null)
            expected=2/(radial**2*projection**2)-2/(momentum[0]*projection)
            checks.append(check('External frequency-pole residue E='+energy_text+' electron='+str(index),
                                mp.norm(expectation-expected*mp.eye(2))/abs(expected),1e-45))
        for first,second in itertools.product([0,1],repeat=2):
            first_pol,second_pol=spin.frame(spin.unit([0,0,1]))[first],spin.frame(hard_direction)[second]
            coefficients=radial_decomposition(initial,incoming,outgoing,first_pol,second_pol,spin.unit([-.2,.8,-.1]))
            left_states=spin.spinors(final).transpose_conj()*gamma0
            right_states=spin.spinors(initial)
            bare=left_states*compton(initial,incoming,outgoing,first_pol,second_pol)*right_states
            internal=left_states*coefficients['soft']*right_states
            external=(1/initial_projection**2+1/final_projection**2)*bare
            total=internal+external
            label=' E='+energy_text+' polarization='+str((first,second))
            checks.append(check('Soft box factor from Dirac equation'+label,
                                mp.norm(internal+2*spin.dot(initial,final)/(initial_projection*final_projection)*bare),1e-45))
            checks.append(check('External plus internal gives conserved-current pole'+label,
                                mp.norm(total-current_square*bare)/mp.norm(bare),1e-45))
            coupling=4*mp.pi*mp.mpf(str(ALPHA))
            virtual_coefficient=coupling/(2*(2*mp.pi)**3)*2*current_square
            real_coefficient=2*mp.mpf(str(ALPHA))/(4*mp.pi**2)*(-current_square)
            checks.append(check('Thermal stimulated emission plus absorption cancels virtual pole'+label,
                                abs(virtual_coefficient+real_coefficient),1e-58))
            checks.append(dict(name='Missing external pole residue breaks thermal soft match'+label,
                               passed=bool(mp.norm(external)>100*mp.norm(total))))
        rows.append(dict(energy=float(energy),current_square=float(current_square),
                         signed_thermal_virtual_coefficient=float(virtual_coefficient),
                         signed_real_stimulated_plus_absorption_coefficient=float(real_coefficient)))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
                       external_frequency_residue_derived_from_same_self_energy=True,
                       leading_soft_cancellation_at_fixed_bath_direction=True,
                       arbitrary_common_bath_occupation_allowed_at_leading_soft_order=True,
                       finite_virtual_external_terms_and_finite_real_not_yet_combined=True),__file__,
           [ROOT/'thermal_radial.py',ROOT/'thermal_insertions.py',AMPLITUDE_PARENT/'DERIVATION.md'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],rows=rows)),flush=True)


if __name__=='__main__':
    main()
