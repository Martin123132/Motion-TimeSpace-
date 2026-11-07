from joint_weak_form import *


def main():
    modest()
    folder=ROOT/'results/joint-weak-form'
    folder.mkdir(parents=True,exist_ok=False)
    rng=np.random.default_rng(871008)
    checks=[]
    temperature=.00014534465573404461
    sample=reduced.event(temperature,.2*temperature,np.array([math.sqrt(.99),0,.1]),np.array([0.,.8,.6]))
    amplitude=reduced.tensor(sample)
    frequencies=sample['photons'][:,0]/temperature
    occupations=1/np.expm1(frequencies)
    reverse_electron=math.exp(frequencies[1]+frequencies[2]-frequencies[0])
    equilibrium_weight=occupations[0]*(1+occupations[1])*(1+occupations[2])
    intensity=np.sum(abs(amplitude)**2)/4
    for trial in range(8):
        hermitian=lambda:sum(coefficient*matrix for coefficient,matrix in zip(rng.normal(size=4)*.1,reduced.PAULI))
        observables=[hermitian() for index in range(3)]
        perturbations=[hermitian() for index in range(3)]
        electron_observables=tuple(rng.normal(size=2)*.1)
        electron_perturbations=tuple(rng.normal(size=2)*.1)
        expected=equilibrium_weight*linear_pair(amplitude,observables,perturbations,electron_observables,electron_perturbations)
        def evaluate(value):
            occupation_matrices=[matrix_occupation(frequency,potential,value) for frequency,potential in zip(frequencies,perturbations)]
            weights=(math.exp(value*electron_perturbations[0]),reverse_electron*math.exp(value*electron_perturbations[1]))
            return nonlinear_weak(amplitude,observables,occupation_matrices,weights,electron_observables)
        step=2e-5
        derivative=(-evaluate(2*step)+8*evaluate(step)-8*evaluate(-step)+evaluate(-2*step))/(12*step)
        checks.append(check('Noncommuting matrix occupation finite derivative trial'+str(trial),abs(derivative-expected)/max(abs(expected),intensity*1e-3),2e-8))
        checks.append(check('Quantum equilibrium is stationary trial'+str(trial),abs(evaluate(0))/(equilibrium_weight*intensity),1e-13))
        dissipation=linear_pair(amplitude,perturbations,perturbations,electron_perturbations,electron_perturbations)
        checks.append(dict(name='Polarized entropy quadratic nonpositive trial'+str(trial),passed=dissipation<=0,value=dissipation))
    for component in range(4):
        observables=[photon[component]*np.eye(2) for photon in sample['photons']]
        delta=difference(amplitude,observables,sample['initial'][component],sample['final'][component])
        checks.append(check('Common four-momentum null without projection component'+str(component),np.linalg.norm(delta)/(np.linalg.norm(amplitude)*temperature),2e-11))
    scalar=[.3,-.2,.1]
    electron=[.1,-.05]
    jump=scalar[1]+scalar[2]-scalar[0]+electron[1]-electron[0]
    scalar_value=linear_pair(amplitude,[value*np.eye(2) for value in scalar],[value*np.eye(2) for value in scalar],electron,electron)
    checks.append(check('Scalar restriction reproduces physical gain-loss entropy weight',abs(scalar_value/(-intensity*jump**2)-1),2e-13))
    chemical=linear_pair(amplitude,[np.eye(2)]*3,[np.eye(2)]*3)
    checks.append(check('Photon chemical mode is not projected to a conserved number',abs(chemical/(-intensity)-1),2e-13))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
                       quantum_gain_loss_linearization_derived=True,full_virtual_collision_cut_matched=False),__file__,
           [ROOT/'joint_weak_form.py',ROOT/'batched_real.py',PARENT/'reduced_amplitude.py'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
