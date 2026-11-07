from common import *
from thermal_candidate import Thermal
from phase_math import invariant,tube_parameters,tube,symbolic
from scipy.integrate import solve_ivp
import numpy as np
import time


def prepare(model,target):
    accepted=load(BACKGROUND/'runs'/model/'dop-half-cap.npz')
    params=read(ROOT/'thermal-qualification'/(model+'-parameters.json'))['parameters']
    thermal=Thermal(params)
    scale=float(accepted['a'][0])
    masses=accepted['masses']
    fields,velocities=accepted['fields'][0],accepted['velocities'][0]
    initial=np.stack([scale*masses*fields,velocities],axis=1)
    density=np.sum(initial**2,axis=1)/2
    external=thermal.values([np.log(scale)])[0]
    hubble=float(np.sqrt((external[0]+density.sum())/3))
    require(density[0]>0,'nonzero slow-field energy')
    uncertainty=None
    if model=='heavy':
        polar=invariant(np.array([scale]),fields[None,:],velocities[None,:],masses,np.array([hubble]),external[1:2])
        uncertainty=tube_parameters(scale,target['scale_end'],masses,density,external[0],(params['cdm']+params['baryon'])/scale,hubble,polar['first'][0],polar['second'][0])
    else:
        require(density[1]==0,'cold control has no heavy field')
    return dict(model=model,initial_efold=float(np.log(scale)),initial_scale=scale,final_efold=float(np.log(target['scale_end'])),
                old_resolved_end=float(accepted['efold'][-1]),initial_clock=float(accepted['times'][0]),initial_hubble=hubble,
                initial_energy_coordinates=initial.tolist(),initial_scalar_density=density.tolist(),masses=masses.tolist(),
                slow_unit=float(np.sqrt(2*density[0])),thermal_parameters=params,tube=uncertainty,
                accepted_path=str(BACKGROUND/'runs'/model/'dop-half-cap.npz'),accepted_sha256=digest(BACKGROUND/'runs'/model/'dop-half-cap.npz'))


def heavy_values(configuration,efold):
    if configuration['tube'] is None:
        return 0.,0.,0.,0.
    return tuple(float(value) for value in tube(configuration['tube'],efold))


def make_rhs(configuration,thermal):
    unit=configuration['slow_unit']
    initial_hubble=configuration['initial_hubble']
    mass=configuration['masses'][0]
    def rhs(efold,state):
        guard()
        coordinate=state[:2]*unit
        radius=max(0.,float(state[3]))*unit
        amplitude=float(np.linalg.norm(coordinate))
        external=thermal.values([efold])[0,0]
        mean,width,drift,inverse=heavy_values(configuration,efold)
        hubble=np.sqrt((external+mean+amplitude**2/2)/3)
        lower=np.sqrt((external+mean*np.exp(-width)+max(amplitude-radius,0.)**2/2)/3)
        density_error=mean*np.expm1(width)
        coefficient=np.exp(efold)*mass/(3*lower*hubble*(lower+hubble))
        radius_rate=radius+coefficient*(amplitude*density_error+.5*amplitude**2*radius+.5*amplitude*radius**2)
        total_error=density_error+amplitude*radius+.5*radius**2
        clock_rate=total_error/(3*lower*hubble*(lower+hubble))
        ratio=np.exp(efold)*mass/hubble
        return np.array([state[0]+ratio*state[1],-2*state[1]-ratio*state[0],initial_hubble/hubble,radius_rate/unit,initial_hubble*clock_rate])
    return rhs


def observables(configuration,thermal,efold,states):
    coordinates=states[:,:2]*configuration['slow_unit']
    amplitude=np.linalg.norm(coordinates,axis=1)
    radius=np.maximum(states[:,3],0)*configuration['slow_unit']
    external=thermal.values(efold)[:,0]
    if configuration['tube'] is None:
        mean,width,drift,inverse=(np.zeros_like(efold) for index in range(4))
    else:
        mean,width,drift,inverse=tube(configuration['tube'],efold)
    hubble=np.sqrt((external+mean+amplitude**2/2)/3)
    lower=np.sqrt((external+mean*np.exp(-width)+np.maximum(amplitude-radius,0)**2/2)/3)
    density_error=mean*np.expm1(width)+amplitude*radius+.5*radius**2
    hubble_error=density_error/(3*(lower+hubble))
    return dict(efold=efold,a=np.exp(efold),states=states,slow_coordinates=coordinates,slow_error_radius=radius,
                hubble=hubble,hubble_error=hubble_error,heavy_mean=mean,heavy_log_width=width,invariant_drift_bound=drift,
                inverse_frequency_upper=inverse,external=external,clock=configuration['initial_clock']+states[:,2]/configuration['initial_hubble'],
                clock_error=states[:,4]/configuration['initial_hubble'])


def save_dense(path,solution,method):
    interpolants=solution.sol.interpolants
    coefficients=np.asarray([item.F if method=='DOP853' else item.Q.T for item in interpolants])
    np.savez_compressed(path,method=method,segment_start=solution.sol.ts[:-1],segment_end=solution.sol.ts[1:],
                        segment_initial=np.asarray([item.y_old for item in interpolants]),coefficients=coefficients,
                        solver_nodes=solution.t,solver_states=solution.y.T)


def direct_replay(configuration,thermal,mean_solution,destination):
    initial=np.asarray(configuration['initial_energy_coordinates'])
    units=np.linalg.norm(initial,axis=1)
    units=np.where(units>0,units,1.)
    masses=np.asarray(configuration['masses'])
    initial_hubble=configuration['initial_hubble']
    state=np.concatenate([(initial/units[:,None]).ravel(),[0.]])
    def rhs(efold,value):
        guard()
        coordinates=value[:4].reshape(2,2)*units[:,None]
        external=thermal.values([efold])[0,0]
        hubble=np.sqrt((external+.5*np.sum(coordinates**2))/3)
        ratio=np.exp(efold)*masses/hubble
        rate=np.column_stack([coordinates[:,0]+ratio*coordinates[:,1],-2*coordinates[:,1]-ratio*coordinates[:,0]])/units[:,None]
        return np.concatenate([rate.ravel(),[initial_hubble/hubble]])
    solution=solve_ivp(rhs,(configuration['initial_efold'],configuration['old_resolved_end']),state,
                       method='DOP853',rtol=2e-12,atol=2e-14,max_step=.00012623704630795892,dense_output=True)
    require(solution.success,'phase-resolved early candidate replay')
    old=load(configuration['accepted_path'])
    efold=old['efold']
    value=solution.sol(efold).T
    coordinates=value[:,:4].reshape(-1,2,2)*units[None,:,None]
    fields=old['fields'].copy()
    for index,mass in enumerate(masses):
        if mass>0:
            fields[:,index]=coordinates[:,index,0]/(np.exp(efold)*mass)
    velocity=coordinates[:,:,1]
    external=thermal.values(efold)
    hubble=np.sqrt((external[:,0]+np.sum(coordinates**2,axis=(1,2))/2)/3)
    mean=observables(configuration,thermal,efold,mean_solution.sol(efold).T)
    slow_error=np.linalg.norm(coordinates[:,0]-mean['slow_coordinates'],axis=1)
    relative_slow_excess=float(np.max((slow_error-mean['slow_error_radius'])/np.maximum(np.linalg.norm(coordinates[:,0],axis=1),configuration['slow_unit'])))
    relative_hubble_excess=float(np.max((abs(hubble-mean['hubble'])-mean['hubble_error'])/hubble))
    clock=configuration['initial_clock']+value[:,4]/initial_hubble
    clock_excess=float(np.max((abs(clock-mean['clock'])-mean['clock_error'])/clock))
    require(max(relative_slow_excess,relative_hubble_excess,clock_excess)<ALGEBRA,'early direct replay outside analytic tube plus algebra padding')
    report=dict(points=len(efold),nfev=solution.nfev,slow_enclosure_relative_excess=relative_slow_excess,
                hubble_enclosure_relative_excess=relative_hubble_excess,clock_enclosure_relative_excess=clock_excess,
                legacy_hubble_relative_difference=float(np.max(abs(hubble-old['H'])/hubble)),
                initial_fields_velocities_clock_preserved=True,reference_uses_same_repaired_thermal_source=True)
    extra={}
    if configuration['tube'] is not None:
        polar=invariant(np.exp(efold),fields,velocity,masses,hubble,external[:,1])
        drift=polar['invariant']-polar['invariant'][0]
        excess=float(np.max(abs(drift)-mean['invariant_drift_bound']))
        require(excess<ALGEBRA,'phase invariant replay')
        report.update(invariant_drift_max=float(np.max(abs(drift))),derived_drift_bound=float(mean['invariant_drift_bound'][-1]),invariant_excess=excess)
        extra=dict(invariant_drift=drift,derived_drift=mean['invariant_drift_bound'])
    np.savez_compressed(destination/'resolved-replay.npz',efold=efold,coordinates=coordinates,hubble=hubble,clock=clock,
                        mean_slow=mean['slow_coordinates'],slow_radius=mean['slow_error_radius'],mean_hubble=mean['hubble'],
                        hubble_error=mean['hubble_error'],mean_clock=mean['clock'],clock_error=mean['clock_error'],**extra)
    save_dense(destination/'resolved-replay-dense.npz',solution,'DOP853')
    write(destination/'replay-result.json',report)
    return report


def main():
    modest()
    check_parent()
    qualified=read(ROOT/'thermal-qualification/result.json')
    require(qualified['passed'] and qualified['state']=='qualified_separate_thermal_candidate','qualified thermal repair')
    destination=ROOT/'extension'
    destination.mkdir(exist_ok=False)
    target=read(ROOT/'inventory/cold-target.json')
    controls=[('base','DOP853',2e-10),('fine','DOP853',2e-12),('independent','RK45',2e-11)]
    configurations={model:prepare(model,target) for model in ('heavy','cold')}
    write(destination/'freeze.json',dict(configurations=configurations,controls=controls,target=target,sources=frozen_sources(),symbolic=symbolic(),
                                      independent_initial_state='accepted field, velocity and clock; H recomputed from same thermal integral'))
    reports=[]
    for model,configuration in configurations.items():
        folder=destination/model
        folder.mkdir(exist_ok=False)
        thermal=Thermal(configuration['thermal_parameters'])
        initial=np.zeros(5)
        initial[:2]=np.asarray(configuration['initial_energy_coordinates'])[0]/configuration['slow_unit']
        grid=np.unique(np.concatenate([np.linspace(configuration['initial_efold'],configuration['final_efold'],1025),
                                      np.linspace(np.log(target['scale_start']),configuration['final_efold'],129)]))
        saved={}
        details=[]
        fine_solution=None
        for label,method,tolerance in controls:
            guard()
            started=time.monotonic()
            solution=solve_ivp(make_rhs(configuration,thermal),(configuration['initial_efold'],configuration['final_efold']),initial,
                               method=method,rtol=tolerance,atol=tolerance/100,dense_output=True,max_step=.05)
            require(solution.success,'slow/clock/comparison solve')
            packet=observables(configuration,thermal,grid,solution.sol(grid).T)
            require(all(np.all(np.isfinite(value)) for value in packet.values()),'finite cold candidate')
            require(np.min(packet['states'][:,3:])>=-ALGEBRA,'nonnegative comparison radii')
            np.savez_compressed(folder/(label+'.npz'),**packet)
            save_dense(folder/(label+'-dense.npz'),solution,method)
            saved[label]=packet
            details.append(dict(label=label,method=method,rtol=tolerance,atol=tolerance/100,nfev=solution.nfev,elapsed_seconds=time.monotonic()-started))
            if label=='fine':
                fine_solution=solution
            print(model,label,'nfev',solution.nfev,'seconds',details[-1]['elapsed_seconds'],flush=True)
        comparisons=[]
        for label in ('base','independent'):
            for quantity in ('hubble','slow_coordinates','clock','slow_error_radius','hubble_error','clock_error'):
                expected=saved['fine'][quantity]
                error=float(np.max(abs(saved[label][quantity]-expected))/max(float(np.max(abs(expected))),1e-100))
                comparisons.append(dict(label=label,quantity=quantity,error=error))
        require(max(item['error'] for item in comparisons)<GATE,'background refinement and independent method')
        fine=saved['fine']
        selected=fine['a']>=target['scale_start']*(1-1e-12)
        cold_uncertainty=dict(hubble=float(np.max(fine['hubble_error'][selected]/fine['hubble'][selected])),
                              slow_energy_coordinates=float(np.max(fine['slow_error_radius'][selected]/np.linalg.norm(fine['slow_coordinates'][selected],axis=1))),
                              clock=float(np.max(fine['clock_error'][selected]/fine['clock'][selected])),
                              heavy_log_density=float(np.max(fine['heavy_log_width'][selected])))
        replay=direct_replay(configuration,thermal,fine_solution,folder)
        passed=all(value<GATE for value in cold_uncertainty.values())
        report=dict(model=model,controls=details,comparisons=comparisons,cold_relative_uncertainty=cold_uncertainty,
                    cold_uncertainty_gate_pass=passed,replay=replay,thermal_source_qualified=True,
                    phase_resolved_late_history=False,original_scattering_bank_changed=False)
        write(folder/'result.json',report)
        reports.append(report)
        print(model,'cold uncertainty',cold_uncertainty,'passes',passed,flush=True)
    check_parent()
    write(destination/'result.json',dict(state='candidate_complete',cold_target=target,reports=reports,
                                       handoff_eligible=all(item['cold_uncertainty_gate_pass'] for item in reports),
                                       original_inventory_pass=False,physical_ode_solves=8,source_hashes=frozen_sources()))


if __name__=='__main__':
    main()
