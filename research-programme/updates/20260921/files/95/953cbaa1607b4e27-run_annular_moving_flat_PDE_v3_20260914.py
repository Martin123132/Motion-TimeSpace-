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
from annular_exact_flat_wave_v2_20260914 import ExactFlatWave


def run():
    evidence = EvidenceRun('annular-moving-flat-PDE-attempt03', __file__)
    try:
        failure_path = evidence.output.parent/'annular-moving-flat-PDE-attempt01/status.json'
        failure = json.loads(failure_path.read_text())
        evidence.own(failure_path)
        evidence.check('first_empty_reflected_support_failure_preserved', failure['state']=='failed' and 'at least one array' in failure['error'])
        evidence.report['correction'] = 'Handle exact target empty reflected support before first reflection; save completed PDE states before target comparisons. PDE core and accuracy gates unchanged.'
        coarse_path = evidence.output.parent/'annular-moving-flat-PDE-attempt02/status.json'
        coarse = json.loads(coarse_path.read_text())
        evidence.own(coarse_path)
        evidence.check('coarse_grid_accuracy_failure_preserved', coarse['state']=='failed' and 'finest_accuracy_gates' in coarse['error'])
        evidence.report['cases'] = list(coarse['cases'])
        evidence.report['resolution_extension'] = 'Original PDE, reflection force, integrator and final accuracy gates unchanged. Retain129/257/513 results, extend to1025/2049 nodes; second amplitude257/513/1025/2049.'
        prior = evidence.output.parent/'annular-moving-wave-algebra-attempt01/status.json'
        algebra = json.loads(prior.read_text())
        evidence.own(prior)
        evidence.check('boundary_energy_identity_complete', algebra['state']=='complete' and all(row['passed'] for row in algebra['checks']))
        evidence.report.update(scope='Actual coupled scalar PDE and dust-shell ODE in moving coordinates, flat space; no input analytic reflection waveform used by PDE.',
                               coupling=0., inner_radius=3., reservoir=.003, coupled_moving_GR_scalar_PDE_tested=False,
                               gates=dict(finest_relative_wave_error=.005,finest_source_position_error=.001,finest_proper_rate_error=.005,
                                          finest_SAT_loss_fraction=.001, refinement_ratio=.8, target_noise=1e-8))
        for amplitude in [.01,.02]:
            exact = ExactFlatWave(amplitude)
            finer_exact = ExactFlatWave(amplitude,inverse_count=32769)
            duration = float(exact.final_proper_time)
            target_noise = 0.
            for fraction in [.25,.5,.75,1.]:
                shell = exact.shell(fraction*duration)
                radii = np.linspace(3.,shell['radius'],2049)
                first = exact.wave(shell['time'],radii)
                second = finer_exact.wave(shell['time'],radii)
                target_noise = max(target_noise,max(np.max(abs(first[name]-second[name])) for name in first))
            evidence.check(str(amplitude)+'_exact_target_interpolation_refines',target_noise<1e-8,target_noise)
            evidence.check(str(amplitude)+'_before_inner_reflector_return',exact.shell(duration)['time']<3.2)
            for count in ([1025,2049] if amplitude == .01 else [257,513,1025,2049]):
                started = perf_counter()
                system = MovingWave(count,amplitude=amplitude)
                times = np.linspace(0.,duration,33)
                result = solve_ivp(system.rhs,(0.,duration),system.initial_state,method='DOP853',rtol=2e-10,atol=2e-12,
                                   max_step=3/(count-1)/8,t_eval=times)
                evidence.check(str(amplitude)+'_'+str(count)+'_solver_finished',result.success and np.isfinite(result.y).all())
                raw_file = evidence.output/('raw_amplitude_'+str(amplitude)+'_count'+str(count)+'.npz')
                np.savez_compressed(raw_file,times=times,states=result.y.T)
                evidence.own(raw_file,'outputs')
                evidence.save()
                diagnostics = [system.diagnostics(time,state) for time,state in zip(times,result.y.T)]
                rows = []
                for time,state,data in zip(times,result.y.T,diagnostics):
                    shell = exact.shell(time)
                    radii = 3.+(shell['radius']-3)*system.coordinate
                    wave = exact.wave(shell['time'],radii)
                    outgoing,incoming,source = system.unpack(state)
                    norm = np.sqrt((shell['radius']-3)/4*(system.weights @ ((outgoing-wave['outgoing'])**2+(incoming-wave['incoming'])**2)))
                    rows.append(dict(time=float(time),energy_norm_error=float(norm),
                                     relative_wave_error=float(norm/np.sqrt(exact.total_incident)),
                                     source_position_error=float(abs(source[0]-shell['radius'])),
                                     source_rate_error=float(abs(source[1]-shell['proper_rate'])),
                                     source_clock_error=float(abs(source[2]-shell['time'])),
                                     scalar_max_error=float(np.max(abs(data['scalar']-wave['scalar'])))))
                final = rows[-1]
                total_energy = np.array([data['flat_energy_with_SAT'] for data in diagnostics])
                loss = np.array([data['accumulated_SAT_loss'] for data in diagnostics])
                row = dict(amplitude=amplitude,count=count,duration=duration,seconds=perf_counter()-started,
                           **{name:max(item[name] for item in rows) for name in ['relative_wave_error','source_position_error','source_rate_error','source_clock_error','scalar_max_error']},
                           final_relative_wave_error=final['relative_wave_error'],
                           corrected_energy_drift=float(max(abs(total_energy-total_energy[0]))),
                           SAT_loss_fraction=float(loss[-1]/exact.total_incident),
                           maximum_boundary_mismatch=float(max(abs(data['right_boundary_mismatch']) for data in diagnostics)),
                           final_source=result.y[-5:,-1].tolist())
                evidence.check(str(amplitude)+'_'+str(count)+'_energy_with_recorded_SAT_loss',row['corrected_energy_drift']<2e-10,row['corrected_energy_drift'])
                evidence.check(str(amplitude)+'_'+str(count)+'_SAT_loss_nonnegative',np.min(loss)>-1e-12 and loss[-1]>0)
                filename=evidence.output/('amplitude_'+str(amplitude)+'_count'+str(count)+'.npz')
                np.savez_compressed(filename,times=times,states=result.y.T,
                                    total_energy_with_SAT=total_energy,SAT_loss=loss,
                                    mass=np.array([data['mass'] for data in diagnostics]),
                                    radii=np.array([data['radii'] for data in diagnostics]))
                evidence.own(filename,'outputs')
                evidence.report['cases'].append(row)
                evidence.save()
                print(row,flush=True)
            cases=[row for row in evidence.report['cases'] if row['amplitude']==amplitude]
            for quantity in ['relative_wave_error','source_position_error','source_rate_error','scalar_max_error','SAT_loss_fraction']:
                evidence.check(str(amplitude)+'_'+quantity+'_refines',all(later[quantity]<.8*earlier[quantity] for earlier,later in zip(cases,cases[1:])),
                               [row[quantity] for row in cases])
            fine=cases[-1]
            evidence.check(str(amplitude)+'_finest_accuracy_gates',fine['relative_wave_error']<.005 and fine['source_position_error']<.001 and fine['source_rate_error']<.005 and fine['SAT_loss_fraction']<.001)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    run()
