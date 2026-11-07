from evolve_spectrum import implicit_step
from thermal_common import *


def main():
    modest()
    folder=ROOT/'results/limits'
    folder.mkdir(parents=True,exist_ok=False)
    grid=SpectralGrid(400)
    checks=[]
    generator=np.random.default_rng(7007)
    dissipation_rows=[]
    for trial in range(5):
        coefficients=generator.normal(size=4)
        potential=sum(coefficient*np.sin((index+1)*np.log(grid.frequency)) for index,coefficient in enumerate(coefficients))
        temperature=float(generator.normal())
        coefficient=3.
        chi=.002
        derivative=coefficient*grid.source(potential,temperature)
        temperature_derivative=-(grid.energy@derivative)/chi
        observed=np.sum(grid.mass*potential*derivative)+chi*I3_PLANCK*temperature*temperature_derivative
        distance=np.diff(grid.frequency)
        expected=-coefficient*np.sum(grid.conductivity*(np.diff(potential)-temperature*distance)**2/distance)
        error=float(abs(observed-expected)/max(abs(expected),1e-100))
        checks.append(dict(name='Coupled collision entropy-defect dissipation '+str(trial),passed=error<1e-11 and observed<=0,value=error,gate=1e-11))
        dissipation_rows.append(dict(observed=float(observed),derived=float(expected),relative_error=error))
    chi=.002
    alpha=100.
    for label,potential,temperature in [('temperature',grid.frequency.copy(),1.),('chemical',np.ones(grid.count),0.)]:
        updated,updated_temperature=implicit_step(grid,10.,chi,alpha,alpha*potential,alpha*temperature,expansion=0.)
        error=max(float(np.max(abs(updated-potential))/max(np.max(abs(potential)),1)),abs(updated_temperature-temperature))
        checks.append(dict(name='Finite heat-capacity '+label+' equilibrium preserved',passed=error<1e-8,value=error,gate=1e-8))
    end=math.log(10)
    rows=[]
    for steps in [400,800]:
        step=end/steps
        potential=np.zeros(grid.count)
        previous_potential=potential.copy()
        temperature=0.
        previous_temperature=0.
        for index in range(1,steps+1):
            alpha=1/step if index==1 else 1.5/step
            vector_history=potential/step if index==1 else (2*potential-.5*previous_potential)/step
            scalar_history=temperature/step if index==1 else (2*temperature-.5*previous_temperature)/step
            updated,updated_temperature=implicit_step(grid,0.,chi,alpha,vector_history,scalar_history)
            previous_potential,potential=potential,updated
            previous_temperature,temperature=temperature,updated_temperature
        ratio=1+chi*temperature
        error=abs(ratio/math.exp(-end)-1)
        checks.append(dict(name='Cold elastic energy-transfer limit keeps photons unchanged '+str(steps),passed=np.max(abs(potential))==0))
        checks.append(dict(name='Decoupled nonrelativistic plasma cools as a^-2 '+str(steps),passed=error<1e-5,value=error,gate=1e-5))
        rows.append(dict(steps=steps,electron_to_reference_temperature=ratio,relative_error=error))
    checks.append(dict(name='Cold-limit temperature error converges at second order',passed=3<rows[0]['relative_error']/rows[1]['relative_error']<5))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
        dissipation=dissipation_rows,cold_limit=rows,synthetic_chi=chi,
        cold_test_uses_finite_capacity_not_invalid_zero_capacity_zero_coupling_limit=True),__file__,[ROOT/'evolve_spectrum.py'])
    print(json.dumps(dict(checks=len(checks),failed=[dict(row,passed=bool(row['passed'])) for row in checks if not row['passed']],cold_limit=rows)),flush=True)


if __name__=='__main__':
    main()
