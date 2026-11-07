from kinetic_common import *


def normalized_mass_score(momentum_squared,temperature):
    mean_inverse_energy=special.kve(1,1/temperature)/special.kve(2,1/temperature)
    return (mean_inverse_energy-1/np.sqrt(1+momentum_squared))/(2*temperature)


def mass_reweight(momentum_squared,temperature,mass_squared_delta):
    mass=math.sqrt(1+mass_squared_delta)
    original_energy=np.sqrt(1+momentum_squared)
    changed_energy=np.sqrt(mass**2+momentum_squared)
    subtracted_energy=mass_squared_delta*((mass+1)-(changed_energy+original_energy))/((changed_energy+original_energy)*(mass+1))
    logratio=-subtracted_energy/temperature-2*math.log(mass)-math.log(special.kve(2,mass/temperature)/special.kve(2,1/temperature))
    return np.exp(logratio)


def main():
    modest()
    folder=ROOT/'results/mass-shell-population'
    folder.mkdir(parents=True,exist_ok=False)
    metadata,saved,spectrum=snapshot()
    checks,rows=[],[]
    for temperature in [metadata['reference_temperature'],.00045962015785263325,.03]:
        nodes,weights=special.roots_genlaguerre(28,.5)
        gamma=1+temperature*nodes
        squared=temperature*nodes*(2+temperature*nodes)
        weights=weights*gamma*np.sqrt(2+temperature*nodes)
        weights/=weights.sum()
        score=normalized_mass_score(squared,temperature)
        checks.append(check('Fixed-density Juttner mass score has zero mean T='+str(temperature),abs(weights@score),3e-10))
        step=1e-3
        derivative=(-mass_reweight(squared,temperature,2*step)+8*mass_reweight(squared,temperature,step)
                    -8*mass_reweight(squared,temperature,-step)+mass_reweight(squared,temperature,-2*step))/(12*step)
        checks.append(check('Mass score matches independently normalized massive population T='+str(temperature),
                            np.linalg.norm((derivative-score)*np.sqrt(weights))/np.linalg.norm(score*np.sqrt(weights)),1e-8))
        for shift in [-.002,.002]:
            checks.append(check('Mass-shifted gas normalization T='+str(temperature)+' shift='+str(shift),abs(weights@mass_reweight(squared,temperature,shift)-1),1e-11))
        def speed_moment(shift):
            return weights@(mass_reweight(squared,temperature,shift)*squared/(squared+1+shift))
        direct=(-speed_moment(2*step)+8*speed_moment(step)-8*speed_moment(-step)+speed_moment(-2*step))/(12*step)
        kernel=weights@(-squared/(squared+1)**2)
        distribution=weights@(score*squared/(squared+1))
        checks.append(check('Gas-average derivative includes kernel and population terms T='+str(temperature),abs((kernel+distribution)/direct-1),1e-8))
        checks.append(dict(name='Dropping population derivative changes speed response T='+str(temperature),passed=abs(kernel/direct-1)>.3))
        rows.append(dict(temperature=temperature,mean_speed_squared=float(speed_moment(0)),
                         direct_mass_squared_derivative=float(direct),kernel_derivative=float(kernel),population_derivative=float(distribution)))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
                       fixed_density_mass_distribution_derivative_derived=True,
                       full_nlo_population_source_numerically_folded=False),__file__,
           [ROOT/'results/saved-state/status.json',ROOT/'results/saved-state/state.npz'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],rows=rows)),flush=True)


if __name__=='__main__':
    main()
