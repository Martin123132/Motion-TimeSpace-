import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()
import json
import warnings
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_moving_wave_20260914 import MovingWave
from annular_dynamical_source_20260914 import DustSurface, vacuum_rhs


def run():
    evidence=EvidenceRun('annular-moving-GR-independent-attempt01',__file__)
    try:
        prior=evidence.output.parent/'annular-moving-GR-PDE-attempt01/status.json'
        main=json.loads(prior.read_text())
        evidence.own(prior)
        evidence.check('coupled_GR_numerical_run_qualified',main['state']=='complete' and all(row['passed'] for row in main['checks']))
        evidence.report.update(scope='Independent radial ODE, temporal Einstein/scalar identities, time-step refinement, vacuum baseline; no additional MTS parent derivation.',
                               coupled_moving_GR_scalar_PDE_tested=True,
                               boundary_force_discrete_projection_explicit=True,
                               complex_step_size=1e-24,
                               gates=dict(finest_mass_time_residual=2e-7,finest_scalar_time_residual=2e-5,
                                          independent_radial_error=2e-9,time_refinement_error=2e-8))
        rows=[]
        for count in [257,513,1025,2049,4097]:
            system=MovingWave(count,coupling=.1)
            path=prior.parent/('count'+str(count)+'.npz')
            evidence.own(path)
            archive=np.load(path)
            maximum_mass_time=0.
            maximum_scalar_time=0.
            maximum_clock=0.
            with warnings.catch_warnings():
                warnings.simplefilter('error')
                for time,state in zip(archive['times'],archive['states']):
                    rhs=system.rhs(time,state)
                    data=system.geometry(state)
                    perturbed=system.diagnostics(time,state.astype(complex)+1e-24j*rhs)
                    mass_derivative=np.imag(perturbed['mass'])/1e-24
                    scalar_derivative=np.imag(perturbed['scalar'])/1e-24
                    outgoing,incoming,source=system.unpack(state)
                    radial=(incoming-outgoing)/2
                    momentum=(incoming+outgoing)/2
                    expected_mass=.1*data['F']*(data['L']*radial*momentum+system.coordinate*source[1]*data['density'])
                    expected_scalar=(data['L']*momentum+system.coordinate*source[1]*radial)/data['radii']
                    maximum_mass_time=max(maximum_mass_time,float(np.max(abs(mass_derivative-expected_mass))))
                    maximum_scalar_time=max(maximum_scalar_time,float(np.max(abs(scalar_derivative-expected_scalar))))
                    shell=data['shell']
                    minus_lapse=data['L'][-1]/np.sqrt(shell['F_minus'])
                    plus_clock=shell['beta_plus']/shell['F_plus']
                    minus_norm=-minus_lapse**2+source[1]**2/shell['F_minus']
                    plus_norm=-shell['F_plus']*plus_clock**2+source[1]**2/shell['F_plus']
                    maximum_clock=max(maximum_clock,abs(minus_norm+1),abs(plus_norm+1))
            row=dict(count=count,maximum_mass_time_residual=maximum_mass_time,
                     maximum_scalar_time_residual=maximum_scalar_time,maximum_induced_clock_error=float(maximum_clock))
            rows.append(row)
            evidence.report['cases'].append(row)
            evidence.check(str(count)+'_both_induced_metrics_agree',maximum_clock<2e-13,float(maximum_clock))
            evidence.save()
            print(row,flush=True)
        for name in ['maximum_mass_time_residual','maximum_scalar_time_residual']:
            values=[row[name] for row in rows]
            evidence.check(name+'_refines',all(later<.8*earlier for earlier,later in zip(values,values[1:])),values)
        evidence.check('finest_temporal_constraint_gates',rows[-1]['maximum_mass_time_residual']<2e-7 and rows[-1]['maximum_scalar_time_residual']<2e-5)
        system=MovingWave(4097,coupling=.1)
        archive=np.load(prior.parent/'count4097.npz')
        radial_rows=[]
        for index in [16,32,56]:
            state=archive['states'][index]
            data=system.geometry(state)
            radii=data['radii']
            density=PchipInterpolator(radii,data['density'])
            def radial_rhs(position,metric):
                energy=float(density(position))
                geometry=1-2*metric[0]/position
                return [.1*geometry*energy,metric[0]/(position**2*geometry)+.1*energy/position]
            result=solve_ivp(radial_rhs,(3.,radii[-1]),[.8,0.],method='DOP853',
                             rtol=2e-12,atol=2e-14,max_step=(radii[-1]-3)/4096,t_eval=radii)
            evidence.check(str(index)+'_independent_radial_solver_finished',result.success)
            final_log_lapse=np.log(data['shell']['beta_minus']/np.sqrt(data['F'][-1]))
            independent_log_lapse=result.y[1]+final_log_lapse-result.y[1,-1]
            local_log_lapse=np.log(data['L'])-.5*np.log(data['F'])
            row=dict(index=index,time=float(archive['times'][index]),
                     mass_error=float(max(abs(result.y[0]-data['mass']))),
                     log_lapse_error=float(max(abs(independent_log_lapse-local_log_lapse))))
            radial_rows.append(row)
            evidence.check(str(index)+'_independent_radial_equations',max(row['mass_error'],row['log_lapse_error'])<2e-9,row)
        evidence.report['independent_radial']=radial_rows
        evidence.save()
        system=MovingWave(1025,coupling=.1)
        archive=np.load(prior.parent/'count1025.npz')
        result=solve_ivp(system.rhs,(0.,1.4),system.initial_state,method='DOP853',
                         rtol=2e-11,atol=2e-13,max_step=3/1024/16,t_eval=archive['times'])
        evidence.check('halved_step_solver_finished',result.success)
        time_error=float(np.max(abs(result.y.T-archive['states'])))
        evidence.check('independent_time_step_refinement',time_error<2e-8,time_error)
        output=evidence.output/'halved_step_count1025.npz'
        np.savez_compressed(output,times=result.t,states=result.y.T)
        evidence.own(output,'outputs')
        sample=archive['states'][32]
        vector=system.rhs(archive['times'][32],sample)
        complex_mass=np.imag(system.geometry(sample.astype(complex)+1e-24j*vector)['mass'])/1e-24
        epsilon=2e-6
        finite_mass=(system.geometry(sample+epsilon*vector)['mass']-system.geometry(sample-epsilon*vector)['mass'])/(2*epsilon)
        evidence.check('complex_step_mass_derivative_crosscheck',np.max(abs(finite_mass-complex_mass))<2e-9,float(np.max(abs(finite_mass-complex_mass))))
        vacuum=MovingWave(129,coupling=.1,amplitude=0.)
        times=np.linspace(0.,1.4,29)
        result=solve_ivp(vacuum.rhs,(0.,1.4),vacuum.initial_state,method='DOP853',
                         rtol=2e-12,atol=2e-14,max_step=.01,t_eval=times)
        reference=solve_ivp(vacuum_rhs(DustSurface(),.1),(0.,1.4),[6.,0.,.8],method='DOP853',
                            rtol=2e-12,atol=2e-14,max_step=.007,t_eval=times)
        evidence.check('vacuum_both_solvers_finished',result.success and reference.success)
        vacuum_error=float(np.max(abs(result.y[-5:-3]-reference.y[:2])))
        evidence.check('vacuum_source_equations_recovered',vacuum_error<2e-11,vacuum_error)
        evidence.check('vacuum_scalar_stays_zero',np.max(abs(result.y[:258]))==0)
        vacuum_data=vacuum.geometry(result.y[:,-1])
        exact_speed=vacuum_data['shell']['beta_minus']*vacuum_data['F']/vacuum_data['F'][-1]
        evidence.check('vacuum_Schwarzschild_radial_clock',np.max(abs(vacuum_data['L']-exact_speed))<2e-8,float(np.max(abs(vacuum_data['L']-exact_speed))))
        evidence.report['time_refinement_error']=time_error
        evidence.report['vacuum_source_error']=vacuum_error
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()

