from reduced_amplitude import *


def joint_channel(amplitudes,density):
    output=np.zeros((4,4),complex)
    for final_spin,initial_spin in itertools.product([0,1],repeat=2):
        kraus=amplitudes[:,:,:,final_spin,initial_spin].transpose(1,2,0).reshape(4,2)
        output+=kraus@density@kraus.conj().T/2
    return output


def adjoint_channel(amplitudes,observable):
    output=np.zeros((2,2),complex)
    for final_spin,initial_spin in itertools.product([0,1],repeat=2):
        kraus=amplitudes[:,:,:,final_spin,initial_spin].transpose(1,2,0).reshape(4,2)
        output+=kraus.conj().T@observable@kraus/2
    return output


def main():
    modest()
    folder=ROOT/'results/joint-readout'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    rng=np.random.default_rng(861008)
    for energy in [.00045962015785263325,.1]:
        sample=event(energy,.2*energy,np.array([math.sqrt(.99),0,.1]),np.array([0.,.8,.6]))
        amplitudes=tensor(sample)
        hard_map=mueller(amplitudes)
        soft_map=mueller(amplitudes.swapaxes(1,2))
        for probe in range(4):
            state=rng.normal(size=2)+1j*rng.normal(size=2)
            state/=np.linalg.norm(state)
            density=np.outer(state,state.conj())
            stokes=np.einsum('aij,ji->a',PAULI,density).real
            joint=joint_channel(amplitudes,density)
            block=joint.reshape(2,2,2,2)
            hard=np.einsum('abcb->ac',block)
            soft=np.einsum('abad->bd',block)
            hard_stokes=np.einsum('aij,ji->a',PAULI,hard).real
            soft_stokes=np.einsum('aij,ji->a',PAULI,soft).real
            label=' E='+str(energy)+' probe='+str(probe)
            checks.append(check('Hard Mueller agrees with joint density partial trace'+label,
                                np.linalg.norm(hard_stokes-hard_map@stokes)/np.trace(joint).real,2e-13))
            checks.append(check('Second photon Mueller from same amplitude'+label,
                                np.linalg.norm(soft_stokes-soft_map@stokes)/np.trace(joint).real,2e-13))
            checks.append(check('Both readouts count the same reaction'+label,abs(np.trace(hard)/np.trace(soft)-1),2e-13))
            checks.append(check('Joint photon density remains positive'+label,
                                max(0.,-np.linalg.eigvalsh(joint).min())/np.trace(joint).real,2e-13))
            raw=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
            observable=raw+raw.conj().T
            forward=np.trace(observable@joint)
            reverse=np.trace(adjoint_channel(amplitudes,observable)@density)
            checks.append(check('Reverse channel is exact observable adjoint'+label,
                                abs(forward-reverse)/np.linalg.norm(joint),2e-13))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
                       both_photon_readouts_derived=True,reverse_amplitude_adjoint_derived=True,
                       finite_frequency_resolved_collision_integral=False),__file__,[ROOT/'reduced_amplitude.py'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
