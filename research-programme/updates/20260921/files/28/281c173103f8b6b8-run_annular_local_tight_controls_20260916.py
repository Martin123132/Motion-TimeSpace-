from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_local_spectral_step_20260916 import spectral_step
from run_annular_source_fitted_crossing_20260915 import initial,diagnostics
from scipy.integrate import solve_ivp
import ctypes
import os
import time
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-local-tight-controls-attempt01',__file__)
    try:
        mask = 256 if os.cpu_count()>8 else 2
        kernel = ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
        if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),mask):
            raise ctypes.WinError(ctypes.get_last_error())
        evidence.report.update(process_id=os.getpid(),single_core_affinity_mask=mask,priority='BelowNormal inherited from EvidenceRun import')
        path = evidence.root/'source-intake/navier-stokes/20260914/annular-local-refinement-qualification-attempt04/status.json'
        status = json.loads(path.read_text())
        evidence.check('local_action_qualified',status['state']=='complete' and all(row['passed'] for row in status['checks']))
        evidence.own(path)
        times = np.array([0.,.05])
        for gram in [False,True]:
            branch = 'MTS' if gram else 'reference'
            system = LocallyRefinedSourceAction(513,gram,background_mass=0.,source_splits=4)
            maximum_step = spectral_step(system,initial(system))['maximum_step']/2
            def flow(instant,state):
                coordinates,rates = np.split(state[:-1],2)
                return np.append(system.rhs(instant,state[:-1]),system.evaluate(instant,coordinates,rates)['clock'])
            started = time.monotonic()
            solution = solve_ivp(flow,(0.,.05),initial(system),t_eval=times,method='DOP853',rtol=2e-12,atol=2e-14,
                max_step=maximum_step,first_step=maximum_step/2)
            evidence.check(branch+'_tight_solve_complete',solution.success,solution.message)
            states = solution.y.T
            row = diagnostics(system,times,states)
            evidence.check(branch+'_finite_timelike_control',np.isfinite(states).all() and max(abs(states[:,2*system.count+1]))<1.)
            evidence.check(branch+'_EL_and_energy',row['maximum_euler_residual']<2e-10 and row['energy_relative_drift']<2e-8,row)
            destination = evidence.output/(branch+'-513-tight-first-twentieth.npz')
            np.savez_compressed(destination,times=times,states=states)
            evidence.own(destination,'outputs')
            row.update(branch=branch,count=513,source_splits=4,duration=.05,rtol=2e-12,atol=2e-14,
                maximum_step=maximum_step,seconds=time.monotonic()-started,rhs_evaluations=solution.nfev)
            evidence.report['cases'].append(row)
            evidence.save()
            print(json.dumps(dict(branch=branch,seconds=row['seconds'],state='control_complete')),flush=True)
        evidence.report.update(scope='Independent tighter first-eighth time integration; comparison to the baseline occurs separately after its completion.',
            baseline_agreement_not_yet_asserted=True,live_quadratic_geometry_qualified=False,uniform_all_time_force_bound_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
