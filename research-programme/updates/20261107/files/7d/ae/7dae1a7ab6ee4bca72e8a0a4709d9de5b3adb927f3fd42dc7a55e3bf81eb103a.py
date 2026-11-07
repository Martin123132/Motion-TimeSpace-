from common import *
from source_adapter import native_background,other_density
from phase_math import other_derivative,invariant,tube_parameters,tube,symbolic
import numpy as np


def main():
    modest()
    check_parent()
    destination=ROOT/'inventory'
    destination.mkdir(exist_ok=False)
    write(destination/'sources.json',dict(sources=frozen_sources(),parent_seal=PARENT_SEAL,background_seal=BACKGROUND_SEAL))
    write(destination/'symbolic.json',symbolic())
    targets=[]
    evidence={}
    for model in ('heavy','cold'):
        path=STRESS/'half'/(model+'-stress.npz')
        packet=load(path)
        scale=np.exp(packet['efold'][0])
        speed=packet['speeds'][0]
        momentum_mass_ratio=scale/np.sqrt(np.expm1(-2*np.log(speed)))
        cold_scale=float(np.max(momentum_mass_ratio)*np.sqrt(.1**-2-1))
        predicted=1/np.sqrt(1+(np.exp(packet['efold'])[:,None]/momentum_mass_ratio)**2)
        error=float(np.max(abs(predicted-packet['speeds'])))
        require(error<ALGEBRA,'saved velocity redshift law')
        targets.append(dict(model=model,all_nodes_cold_scale=cold_scale,momentum_mass_ratio=momentum_mass_ratio.tolist(),velocity_map_error=error))
        evidence[str(path)]=digest(path)
    start=max(item['all_nodes_cold_scale'] for item in targets)
    end=start*np.exp(.25)
    require(0<start<end<=1,'requested cold interval outside inherited a<=1 domain')
    target=dict(speed_limit=.1,efold_span=.25,scale_start=start,scale_end=float(end),redshift_start=1/start-1,redshift_end=float(1/end-1),models=targets,selection='kinematics only, no GR/Poisson performance inspected')
    write(destination/'cold-target.json',target)
    reports=[]
    for model in ('heavy','cold'):
        guard()
        input_path=BACKGROUND/'inputs'/(model+'-input.npz')
        accepted_path=BACKGROUND/'runs'/model/'dop-half-cap.npz'
        supplied,accepted=load(input_path),load(accepted_path)
        evidence[str(input_path)],evidence[str(accepted_path)]=digest(input_path),digest(accepted_path)
        native=native_background(model)
        initial_scale=float(accepted['a'][0])
        external=other_density(native,[initial_scale])[0]
        cold_density=float(np.sum(native.get_background_densities(np.array([initial_scale]),vars=['cdm','baryon'],format='array'))/initial_scale**2)
        derivative=other_derivative(native,accepted['efold'])
        derivative_half=other_derivative(native,accepted['efold'],5e-4)
        derivative_error=float(np.max(abs(derivative-derivative_half))/np.max(abs(derivative_half)))
        require(derivative_error<GATE,'other-density derivative resolution')
        probes=np.linspace(accepted['efold'][0],np.log(end),513)
        values=other_density(native,np.exp(probes))
        rate=other_derivative(native,probes,5e-4)
        width=1e-3
        second=(-other_density(native,np.exp(probes+2*width))+16*other_density(native,np.exp(probes+width))-30*values+16*other_density(native,np.exp(probes-width))-other_density(native,np.exp(probes-2*width)))/(12*width**2)
        require(np.all(values>0) and np.all(rate/values>=-2-GATE) and np.all(rate/values<=-1+GATE),'free-gas slope qualification')
        require(np.all(second/values>=1-GATE) and np.all(second/values<=4+GATE),'free-gas curvature qualification')
        rho=(accepted['velocities'][0]**2+(initial_scale*accepted['masses']*accepted['fields'][0])**2)/2
        report=dict(model=model,accepted_input=str(accepted_path),accepted_sha256=digest(accepted_path),initial_scale=initial_scale,
                    last_resolved_scale=float(accepted['a'][-1]),native_exact_switch=.00028,masses=accepted['masses'].tolist(),
                    initial_fields=accepted['fields'][0].tolist(),initial_velocities=accepted['velocities'][0].tolist(),
                    initial_clock=float(accepted['times'][0]),initial_hubble=float(accepted['H'][0]),initial_scalar_density=rho.tolist(),
                    initial_other_density=float(external),initial_cold_density=cold_density,other_derivative_error=derivative_error,
                    other_slope_range=[float(np.min(rate/values)),float(np.max(rate/values))],
                    other_curvature_range=[float(np.min(second/values)),float(np.max(second/values))],
                    future_other_source_scope='Inherited native standard-species density functions, not the old heavy/slow DE trajectory; sampled derivative qualification, no interval-arithmetic certificate')
        if model=='heavy':
            invariants=invariant(accepted['a'],accepted['fields'],accepted['velocities'],accepted['masses'],accepted['H'],derivative_half)
            parameters=tube_parameters(initial_scale,end,accepted['masses'],rho,external,cold_density,accepted['H'][0],invariants['first'][0],invariants['second'][0])
            mean,log_width,drift,inverse_upper=tube(parameters,accepted['efold'])
            residual=invariants['invariant']-invariants['invariant'][0]
            density_difference=np.log(invariants['rho'][:,1]/mean)
            require(np.max(abs(residual)-drift)<ALGEBRA,'invariant drift exceeds derived bound')
            require(np.max(abs(density_difference)-log_width)<ALGEBRA,'resolved density outside analytic tube')
            require(np.max(invariants['inverse']-inverse_upper)<ALGEBRA,'Friedmann frequency bound')
            report.update(tube=parameters,resolved_invariant_drift_max=float(np.max(abs(residual))),
                          resolved_drift_bound_final=float(drift[-1]),resolved_density_tube_excess=float(np.max(abs(density_difference)-log_width)),
                          initial_heavy_frequency_ratio=float(1/invariants['inverse'][0]),
                          cold_interval_log_density_width=np.asarray(tube(parameters,np.log([start,end]))[1]).tolist())
            np.savez_compressed(destination/'resolved-invariant.npz',efold=accepted['efold'],rho=invariants['rho'][:,1],mean=mean,
                                log_width=log_width,invariant=invariants['invariant'],drift=drift,first=invariants['first'],second=invariants['second'],
                                inverse=invariants['inverse'],inverse_upper=inverse_upper)
        else:
            report['tube']=None
        np.savez_compressed(destination/(model+'-external-probes.npz'),efold=probes,density=values,first=rate,second=second)
        write(destination/(model+'-input.json'),report)
        reports.append(report)
        print(model,'masses',report['masses'],'last resolved a',report['last_resolved_scale'],'cold a',start,flush=True)
        if model=='heavy':
            print('invariant',report['resolved_invariant_drift_max'],'bound',report['resolved_drift_bound_final'],'cold width',report['cold_interval_log_density_width'],flush=True)
        del native,accepted,supplied
    check_parent()
    write(destination/'result.json',dict(passed=True,cold_target=target,reports=reports,evidence_hashes=evidence,
                                       exact_late_scalar_phase_available=False,background_tube_route_derived=True,
                                       new_physical_ode_solves=0))


if __name__=='__main__':
    main()
