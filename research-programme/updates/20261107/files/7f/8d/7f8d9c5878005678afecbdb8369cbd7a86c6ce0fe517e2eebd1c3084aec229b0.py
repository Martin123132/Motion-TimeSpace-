import argparse
from thermal_common import *


def implicit_step(grid,coefficient,chi,alpha,history,temperature_history,expansion=1.):
    columns=grid.solve(alpha,coefficient,np.column_stack([history,coefficient*grid.temperature_source]))
    free,thermal=columns[:,0],columns[:,1]
    denominator=chi*(alpha+expansion)+alpha*(grid.energy@thermal)
    numerator=chi*temperature_history-expansion-grid.energy@(alpha*free-history)
    temperature=numerator/denominator
    potential=free+thermal*temperature
    return potential,float(temperature)


def run(model,name,count,steps,minimum=1e-4,maximum=40.,chi_override=None):
    modest()
    folder=ROOT/'runs'/name
    folder.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter()
    background=ThermalBackground(model)
    chi=background.chi if chi_override is None else chi_override
    grid=SpectralGrid(count,minimum,maximum)
    delta=background.end/steps
    potential=np.zeros(count)
    temperature=0.
    previous_potential=potential.copy()
    previous_temperature=0.
    work=0.
    previous_work=0.
    history=[]
    frequency_history=[]
    maximum_number_error=0.
    maximum_energy_error=0.
    maximum_equation_residual=0.
    for index in range(1,steps+1):
        log_expansion=index*delta
        local=background.at(log_expansion)
        if index==1:
            alpha=1/delta
            vector_history=potential/delta
            scalar_history=temperature/delta
            work_history=work/delta
        else:
            alpha=1.5/delta
            vector_history=(2*potential-.5*previous_potential)/delta
            scalar_history=(2*temperature-.5*previous_temperature)/delta
            work_history=(2*work-.5*previous_work)/delta
        updated,updated_temperature=implicit_step(grid,local['coefficient'],chi,alpha,vector_history,scalar_history)
        updated_work=(work_history+1+chi*updated_temperature)/alpha
        number=grid.mass@updated
        energy=grid.energy@updated
        balance=energy+chi*updated_temperature+updated_work
        maximum_number_error=max(maximum_number_error,float(abs(number)/max(np.sum(abs(grid.mass*updated)),1e-30)))
        maximum_energy_error=max(maximum_energy_error,float(abs(balance)/max(abs(energy),abs(updated_work),1e-30)))
        source=local['coefficient']*grid.source(updated,updated_temperature)
        residual=alpha*updated-vector_history-source
        residual_norm=math.sqrt(np.sum(grid.mass*abs(residual)**2)/max(np.sum(grid.mass*abs(source)**2),1e-100))
        maximum_equation_residual=max(maximum_equation_residual,residual_norm)
        previous_potential,potential=potential,updated
        previous_temperature,temperature=temperature,updated_temperature
        previous_work,work=work,updated_work
        if index==1 or index%max(1,steps//40)==0 or index==steps:
            relative_spectrum=chi*(1+planck(grid.frequency))*potential
            history.append(dict(log_expansion=log_expansion,scale=local['scale'],comoving_photon_energy_scaled=float(energy),
                photon_energy_fraction=float(chi*energy),temperature_scaled=temperature,electron_temperature_fraction=float(chi*temperature),
                compton_coefficient=local['coefficient'],energy_work_balance=float(balance),photon_number_residual=float(number),
                maximum_relative_occupation_perturbation=float(np.max(abs(relative_spectrum)))))
            frequency_history.append(potential.copy())
    final_ratio=1+chi*(1+planck(grid.frequency))*potential
    checks=[dict(name='Photon number conserved by flux differences',passed=maximum_number_error<1e-8,value=maximum_number_error,gate=1e-8),
        dict(name='Photon and plasma energy plus expansion work balance',passed=maximum_energy_error<1e-8,value=maximum_energy_error,gate=1e-8),
        dict(name='Recovered physical photon occupation remains positive',passed=bool(np.min(final_ratio)>0),minimum_ratio=float(np.min(final_ratio))),
        dict(name='Frequency-resolved implicit equations solved',passed=maximum_equation_residual<1e-7,value=maximum_equation_residual,gate=1e-7)]
    np.savez_compressed(folder/'spectrum.npz',frequency=grid.frequency,potential=potential,mass=grid.mass,energy=grid.energy,
        temperature_scaled=temperature,chi=chi,physical_chi=background.chi,history_potentials=frequency_history,
        history_log_expansion=[row['log_expansion'] for row in history],points=count,steps=steps,minimum=minimum,maximum=maximum)
    finish(folder,dict(model=model,run_name=name,points=count,steps=steps,minimum=minimum,maximum=maximum,
        chi=chi,physical_chi=background.chi,override_is_numerical_test_only=chi_override is not None,
        helium_mass_fraction=background.helium_fraction,particles_per_electron=background.particles_per_electron,
        checks=checks,all_checks_passed=all(row['passed'] for row in checks),history=history,
        final_photon_energy_fraction=float(chi*(grid.energy@potential)),final_electron_temperature_fraction=float(chi*temperature),
        expansion_work_scaled=work,elapsed_seconds=time.perf_counter()-started,
        first_order_heat_capacity_expansion=True,isotropic_background_only=True,
        full_nonlinear_anisotropic_compton=False,photon_production_omitted=True,feedback_on_metric_not_applied=True),__file__,
        [background.parent.source,background.native_constants,COLLISION/'runs/backgrounds'/(model+'.npz')])
    print(json.dumps(dict(run=name,checks=checks,chi=chi,energy_change=chi*(grid.energy@potential),temperature_shift=chi*temperature,elapsed_seconds=time.perf_counter()-started)),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],default='heavy')
    parser.add_argument('--name',required=True)
    parser.add_argument('--points',type=int,default=800)
    parser.add_argument('--steps',type=int,default=400)
    parser.add_argument('--minimum',type=float,default=1e-4)
    parser.add_argument('--maximum',type=float,default=40.)
    parser.add_argument('--chi',type=float)
    arguments=parser.parse_args()
    run(arguments.model,arguments.name,arguments.points,arguments.steps,arguments.minimum,arguments.maximum,arguments.chi)
