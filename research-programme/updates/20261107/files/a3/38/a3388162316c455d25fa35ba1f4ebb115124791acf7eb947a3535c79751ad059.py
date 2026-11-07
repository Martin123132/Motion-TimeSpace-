from thermal_insertions import *
import ordered_real_kernel as scalar


def main():
    modest()
    mp.mp.dps=75
    folder=ROOT/'results/crossed-absorption'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows=[],[]
    for energy_text in ['.00045962015785263325','.1']:
        energy=mp.mpf(energy_text)
        for fraction_text in ['.01','.3','1.4']:
            fraction=mp.mpf(fraction_text)
            sample=spin.event(energy,-fraction,[.7,.2,-.3],[-.3,.5,.6])
            directions=sample['directions']
            angles=[1-sum(directions[left][index]*directions[right][index] for index in range(3)) for left,right in [(0,1),(0,2),(1,2)]]
            squared,hard,denominator=scalar.amplitude_squared(energy,-energy*fraction,*angles)
            tensor=spin.tensor_for_event(sample)
            tensor_sum=np.vdot(tensor,tensor).real/4
            label=' E='+energy_text+' absorbed/E='+fraction_text
            checks.append(check('Crossed six-diagram amplitude versus invariant formula'+label,abs(float(squared)-tensor_sum)/tensor_sum,2e-13))
            expected=(energy+energy*fraction+energy**2*fraction*angles[1])/(1+energy*angles[0]+energy*fraction*angles[2])
            checks.append(check('Physical absorption kinematics'+label,abs(hard-expected),1e-60))
            checks.append(check('Crossed outgoing electron on shell'+label,abs(spin.dot(sample['final'],sample['final'])-1),1e-60))
            for ward in [0,1,2]:
                ward_tensor=spin.tensor_for_event(sample,ward=ward)
                checks.append(check('Absorption Ward leg '+str(ward)+label,float(np.linalg.norm(ward_tensor))/float(np.linalg.norm(tensor)),1e-50))
            absorption_density=-scalar.real_density(energy,-energy*fraction,*angles)
            checks.append(dict(name='Absorption phase-space density positive'+label,passed=bool(absorption_density>0)))
            temperature=energy
            incoming_bath=energy*fraction
            occupation=lambda value:1/mp.expm1(value/temperature)
            forward=occupation(energy)*occupation(incoming_bath)*(1+occupation(hard))
            reverse=occupation(hard)*(1+occupation(energy))*(1+occupation(incoming_bath))
            electron_ratio=mp.exp(-(sample['final'][0]-1)/temperature)
            checks.append(check('Absorption reverse-emission thermal detailed balance'+label,abs(forward/(reverse*electron_ratio)-1),1e-58))
            photon_delta=sample['photons'][1]-sample['photons'][0]+sample['photons'][2]
            checks.append(check('Crossed photon/electron four-momentum balance'+label,mp.norm(photon_delta+sample['final']-sample['initial']),1e-60))
            rows.append(dict(energy=float(energy),absorbed_energy=float(incoming_bath),outgoing_energy=float(hard),
                             final_electron_energy=float(sample['final'][0]),positive_differential_density=float(absorption_density),
                             hard_incoming_spin_average=4,bath_polarizations_summed_not_averaged=True))
        values=scalar.geometry(energy,mp.mpf('.2'),mp.mpf('-.4'),mp.mpf('.7'))
        for fraction in ['1e-5','1e-8']:
            absorbed=energy*mp.mpf(fraction)
            density=-scalar.real_density(energy,-absorbed,*values[1:])
            checks.append(check('Absorption matches emission soft coefficient E='+energy_text+' fraction='+fraction,
                                abs(absorbed*density/scalar.pole_density(*values)-1),5*float(fraction)))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
                       genuine_absorption_crossing=True,electron_boltzmann_factor_in_equilibrium_test=True,
                       finite_recoil_preserved=True,full_thermal_collision_operator_not_assembled=True),__file__,
           [AMPLITUDE_PARENT/'dirac_amplitude.py',PARENT/'ordered_real_kernel.py',ROOT/'thermal_insertions.py'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],rows=rows)),flush=True)


if __name__=='__main__':
    main()
