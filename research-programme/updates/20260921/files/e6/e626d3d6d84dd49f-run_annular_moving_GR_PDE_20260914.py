import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()
import json
from time import perf_counter
import numpy as np
from scipy.integrate import solve_ivp
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_moving_wave_20260914 import MovingWave


def run():
    evidence = EvidenceRun('annular-moving-GR-PDE-attempt01', __file__)
    try:
        prior=evidence.output.parent/'annular-moving-flat-PDE-attempt03/status.json'
        qualified=json.loads(prior.read_text())
        evidence.own(prior)
        evidence.check('flat_coupled_PDE_accuracy_qualified',qualified['state']=='complete' and all(row['passed'] for row in qualified['checks']))
        evidence.report.update(scope='Coupled moving dust shell and spherical Einstein-scalar field on a regular annulus; constrained radial metric with evolving characteristics.',
                               coupling=.1, inner_radius=3., reduced_central_mass=8., reservoir=.003, amplitude=.01,
                               duration=1.4, moving_finite_collar_MTS_boundary_derived=False,
                               coupled_moving_GR_scalar_PDE_tested=True, external_force_history_prescribed=False,
                               time_gauge='shell proper time, L_minus at shell=beta_minus; evolve exterior Schwarzschild time separately',
                               prior_original_rigid_pulse_replayed=False,
                               gates=dict(finest_mass_drift=5e-8,finest_mass_work_error=5e-8,
                                          field_difference_refinement_ratio=.8,finest_normalized_field_difference=.005,
                                          finest_boundary_mismatch=.0002))
        duration=1.4
        times=np.linspace(0.,duration,57)
        for count in [257,513,1025,2049,4097]:
            started=perf_counter()
            system=MovingWave(count,coupling=.1)
            result=solve_ivp(system.rhs,(0.,duration),system.initial_state,method='DOP853',
                             rtol=2e-10,atol=2e-12,max_step=3/(count-1)/8,t_eval=times)
            evidence.check(str(count)+'_solver_finished',result.success and np.isfinite(result.y).all())
            raw=evidence.output/('raw_count'+str(count)+'.npz')
            np.savez_compressed(raw,times=times,states=result.y.T)
            evidence.own(raw,'outputs')
            evidence.save()
            data=[system.diagnostics(time,state) for time,state in zip(times,result.y.T)]
            masses=np.array([row['mass_plus'] for row in data])
            density0=system.geometry(system.initial_state)['density']
            energy0=3*(system.weights @ density0)
            row=dict(count=count,seconds=perf_counter()-started,initial_bulk_reduced_energy=float(energy0),
                     initial_interior_mass=float(system.initial_interior_mass), initial_exterior_mass=float(masses[0]),
                     mass_drift=float(max(abs(masses-masses[0]))),
                     maximum_mass_work_error=float(max(abs(item['mass_work_error']) for item in data)),
                     maximum_boundary_mismatch=float(max(abs(item['right_boundary_mismatch']) for item in data)),
                     left_boundary_mismatch=float(max(abs(item['left_boundary_mismatch']) for item in data)),
                     minimum_F=float(min(item['minimum_F'] for item in data)),
                     peak_normal_pressure=float(max(item['normal_pressure'] for item in data)),
                     peak_outgoing_trace=float(max(abs(state[count-1]) for state in result.y.T)),
                     final_source=result.y[-5:,-1].tolist(),
                     interior_mass_lost=float(data[0]['mass'][-1]-data[-1]['mass'][-1]),
                     final_mass_work=float(result.y[-1,-1]))
            filename=evidence.output/('count'+str(count)+'.npz')
            np.savez_compressed(filename,times=times,states=result.y.T,
                                mass=np.array([item['mass'] for item in data]),
                                L=np.array([item['L'] for item in data]),
                                scalar=np.array([item['scalar'] for item in data]),
                                mass_plus=masses,
                                normal_pressure=np.array([item['normal_pressure'] for item in data]),
                                mass_work_error=np.array([item['mass_work_error'] for item in data]),
                                right_mismatch=np.array([item['right_boundary_mismatch'] for item in data]),
                                radii=np.array([item['radii'] for item in data]))
            evidence.own(filename,'outputs')
            evidence.report['cases'].append(row)
            evidence.check(str(count)+'_actual_impact_and_recoil',row['peak_normal_pressure']>1e-5 and row['final_source'][1]>.05 and row['interior_mass_lost']>1e-6)
            evidence.check(str(count)+'_regular_and_quiet_inner_boundary',row['minimum_F']>.15 and row['left_boundary_mismatch']<1e-6)
            evidence.save()
            print(row,flush=True)
        comparisons=[]
        for coarse_count,fine_count in [(257,513),(513,1025),(1025,2049),(2049,4097)]:
            coarse=np.load(evidence.output/('count'+str(coarse_count)+'.npz'))
            fine=np.load(evidence.output/('count'+str(fine_count)+'.npz'))
            system=MovingWave(coarse_count,coupling=.1)
            coarse_char=coarse['states'][:,:2*coarse_count].reshape(-1,2,coarse_count)
            fine_char=fine['states'][:,:2*fine_count].reshape(-1,2,fine_count)[:,:,::2]
            difference=coarse_char-fine_char
            lengths=coarse['states'][:,-5]-3
            norm=np.sqrt(lengths/4*np.sum(system.weights*np.sum(difference**2,axis=1),axis=1))
            energy0=next(row for row in evidence.report['cases'] if row['count']==fine_count)['initial_bulk_reduced_energy']
            row=dict(coarse=coarse_count,fine=fine_count,maximum_relative_wave_difference=float(np.max(norm)/np.sqrt(energy0)),
                     source_position_difference=float(np.max(abs(coarse['states'][:,-5]-fine['states'][:,-5]))),
                     source_rate_difference=float(np.max(abs(coarse['states'][:,-4]-fine['states'][:,-4]))),
                     exterior_clock_difference=float(np.max(abs(coarse['states'][:,-3]-fine['states'][:,-3]))),
                     scalar_difference=float(np.max(abs(coarse['scalar']-fine['scalar'][:,::2]))),
                     mass_profile_difference=float(np.max(abs(coarse['mass']-fine['mass'][:,::2]))),
                     speed_profile_difference=float(np.max(abs(coarse['L']-fine['L'][:,::2]))))
            comparisons.append(row)
        evidence.report['refinement']=comparisons
        evidence.save()
        for name in ['maximum_relative_wave_difference','source_position_difference','source_rate_difference','exterior_clock_difference','scalar_difference','mass_profile_difference','speed_profile_difference']:
            values=[row[name] for row in comparisons]
            evidence.check(name+'_refines',all(later<.8*earlier for earlier,later in zip(values,values[1:])),values)
        fine=evidence.report['cases'][-1]
        evidence.check('finest_mass_and_source_work_gates',fine['mass_drift']<5e-8 and fine['maximum_mass_work_error']<5e-8,
                       dict(mass_drift=fine['mass_drift'],mass_work_error=fine['maximum_mass_work_error']))
        evidence.check('finest_boundary_and_field_gates',fine['maximum_boundary_mismatch']<.0002 and comparisons[-1]['maximum_relative_wave_difference']<.005)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    run()
