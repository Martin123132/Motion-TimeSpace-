from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_fixed_grid_moving_trace_20260914 import FixedGridMovingTrace
import numpy as np
import time


def tangent_preparation(system):
    state=system.initial_state.copy()
    values=system.values(state)
    values[:,2*system.count+1]=-.00008*(1+.03*system.offsets)
    for iteration in range(8):
        prepared=system.preparation(state)
        data=prepared['data']
        inverse_mass=data['N'][:,:system.count]*data['U'][:,:system.count]/(system.node_weights*data['R'][:,:system.count]**2)
        normal=data['trace_weights']*inverse_mass
        values[:,system.count:2*system.count]-=prepared['trace_rate'][:,None]*normal/np.sum(normal**2,axis=1)[:,None]
    return state


def main():
    evidence=EvidenceRun('annular-fixed-grid-moving-trace-qualification-attempt01',__file__)
    try:
        for gram in [False,True]:
            system=FixedGridMovingTrace(33,gram,degree=4,radial_degree=18)
            state=tangent_preparation(system)
            started=time.perf_counter()
            evaluation=system.evaluate(0,state)
            elapsed=time.perf_counter()-started
            geometry=evaluation['geometry']
            probes=geometry.material(np.array([-.3,0.,.3]))['R'].ravel()
            current=geometry.mass_current(probes,evaluation['multipliers'])
            step=1e-22
            varied=system.geometry(state.astype(complex)+1j*step*evaluation['rhs'])
            actual=varied.metric(probes)['mu'].imag/step
            error=float(np.max(abs(actual-current['total'])))
            row=dict(branch='MTS' if gram else 'reference',seconds_per_evaluation=elapsed,
                     trace_error=float(np.max(abs(evaluation['trace']))),
                     trace_rate_error=float(np.max(abs(evaluation['trace_rate']))),
                     trace_acceleration_error=float(np.max(abs(evaluation['acceleration_constraint']))),
                     current_error=error,current_scale=float(np.max(abs(current['total']))),
                     outer_mass_rate=float(varied.outer_mass.imag/step),
                     multiplier_condition=float(np.linalg.cond(evaluation['multiplier_matrix'])),
                     multiplier_maximum=float(np.max(abs(evaluation['multipliers']))),
                     minimum_source_jacobian=geometry.minimum_source_jacobian)
            evidence.report['cases'].append(row)
            path=evidence.output/(row['branch']+'-current.npz')
            np.savez_compressed(path,state=state,rhs=evaluation['rhs'],multipliers=evaluation['multipliers'],
                                radii=probes,mass_rate=actual,**current)
            evidence.own(path,'outputs')
            evidence.check(row['branch']+'_compatible_reflecting_trace',
                           max(row['trace_error'],row['trace_rate_error'],row['trace_acceleration_error'])<2e-11,row)
            evidence.check(row['branch']+'_independent_temporal_gravity_equation',error<2e-7,row)
            evidence.check(row['branch']+'_independent_exterior_energy_rate',abs(row['outer_mass_rate'])<2e-10)
            print(row,flush=True)
        evidence.report.update(fixed_scalar_grid_moving_source_trace_candidate=True,
                               previous_affine_grid_current_failure_repaired_by_changing_action=True,
                               full_GR_limit_proven=False,full_wave_gravity_evolved=False,
                               equivalence_to_previous_one_sided_source_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

