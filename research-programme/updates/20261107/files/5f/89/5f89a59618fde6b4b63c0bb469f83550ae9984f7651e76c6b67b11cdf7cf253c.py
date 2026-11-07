from thermal_event_source import *
import thermal_insertions as vertex
spin=vertex.spin


def scalar_mass_response(energy,cosine):
    initial=mp.matrix([1,0,0,0])
    incoming=spin.photon(energy,mp.matrix([0,0,1]))
    direction=mp.matrix([mp.sqrt(1-cosine**2),0,cosine])
    hard=energy/(1+energy*(1-cosine))
    outgoing=spin.photon(hard,direction)
    final=initial+incoming-outgoing
    final_energy_shift=1/final[0]
    hard_shift=(1-final_energy_shift)/(1-sum(final[index+1]*direction[index] for index in range(3))/final[0])
    gamma0=spin.gamma_matrices()[0]
    hamiltonian=final[0]*mp.eye(4)-gamma0*vertex.inverse(final)
    final_spin=(mp.eye(4)-hamiltonian/final[0])/2*gamma0*spin.spinors(final)/(2*final[0])
    from thermal_dressed import kinematic_spinor_shift
    final_spin+=kinematic_spinor_shift(final,-hard_shift*direction)
    initial_states=spin.spinors(initial)
    final_states=spin.spinors(final)
    initial_delta=mp.matrix([1,0,0,0])
    hard_delta=spin.photon(hard_shift,direction)
    direct,crossed=spin.propagator(initial+incoming),spin.propagator(initial-outgoing)
    squared,interference=mp.mpf(0),mp.mpf(0)
    for first,second in itertools.product([0,1],repeat=2):
        first_pol=spin.frame(mp.matrix([0,0,1]))[first]
        second_pol=spin.frame(direction)[second]
        first_vertex,second_vertex=spin.slash(first_pol),spin.slash(second_pol)
        bare=vertex.compton(initial,incoming,outgoing,first_pol,second_pol)
        insertion=(second_vertex*direct*(mp.eye(4)-spin.slash(initial_delta))*direct*first_vertex
                   +first_vertex*crossed*(mp.eye(4)-spin.slash(initial_delta-hard_delta))*crossed*second_vertex)
        amplitude=final_states.transpose_conj()*gamma0*bare*initial_states
        variation=final_states.transpose_conj()*gamma0*insertion*initial_states+final_spin.transpose_conj()*gamma0*bare*initial_states
        squared+=sum(abs(value)**2 for value in amplitude)
        interference+=2*mp.re(sum(mp.conj(amplitude[row,column])*variation[row,column] for row in range(2) for column in range(2)))
    phase=mp.diff(lambda shifted_mass:mp.log(dressed_phase(energy,cosine,shifted_mass**2-1)[0]),mp.mpf(1))
    return interference/squared+phase


def klein_nishina(energy,cosine,mass):
    ratio=1/(1+energy*(1-cosine)/mass)
    return ratio**2*(ratio+1/ratio-(1-cosine**2))/mass**2


def main():
    modest()
    mp.mp.dps=65
    folder=ROOT/'results/dressed-phase-space'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows=[],[]
    for energy_text in ['.00045962015785263325','.1','1']:
        for cosine_text in ['-.8','.1','.7']:
            energy,cosine=mp.mpf(energy_text),mp.mpf(cosine_text)
            result=phase_response(energy,cosine,energy)
            derivative=mp.diff(lambda displacement:mp.log(dressed_phase(energy,cosine,displacement)[0]),mp.mpf(0))
            hard_derivative=mp.diff(lambda displacement:dressed_phase(energy,cosine,displacement)[1],mp.mpf(0))
            electron_derivative=mp.diff(lambda displacement:dressed_phase(energy,cosine,displacement)[2],mp.mpf(0))
            label=' E='+energy_text+' cosine='+cosine_text
            checks.append(check('Dressed phase-space exact derivative'+label,abs(result['phase_delta']/result['mass_squared']-derivative),1e-51))
            checks.append(check('Dressed recoil energy exact derivative'+label,abs(result['hard_delta']/result['mass_squared']-hard_derivative),1e-51))
            checks.append(check('Independent dressed electron energy derivative'+label,abs(result['electron_delta'][0]/result['mass_squared']-electron_derivative),1e-51))
            checks.append(check('Dressed photon/electron source balance'+label,mp.norm(result['photon_delta']+result['electron_delta']),1e-51))
            scalar=scalar_mass_response(energy,cosine)
            independent=mp.diff(lambda mass:mp.log(klein_nishina(energy,cosine,mass)),mp.mpf(1))
            checks.append(check('Canonical residue/measure scheme reproduces independent Klein-Nishina mass derivative'+label,abs(scalar-independent),1e-48))
            rows.append(dict(energy=float(energy),cosine=float(cosine),scalar_mass_rate_derivative=float(scalar),
                             phase_correction=float(result['phase_delta']),final_bose_correction=float(result['bose_delta'])))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
                       dressed_state_measure_derived=True,scalar_mass_model_used_only_as_independent_normalization_control=True),__file__,
           [ROOT/'thermal_event_source.py',PARENT/'thermal_insertions.py',PARENT/'thermal_dressed.py'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],rows=rows)),flush=True)


if __name__=='__main__':
    import itertools
    main()
