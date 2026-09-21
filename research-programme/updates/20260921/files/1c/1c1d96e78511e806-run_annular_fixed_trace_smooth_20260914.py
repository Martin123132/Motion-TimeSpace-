from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_smooth_trace_preparation_20260914 import smooth_preparation as tangent_preparation
from annular_fixed_grid_moving_trace_20260914 import FixedGridMovingTrace
from scipy.integrate import solve_ivp
import numpy as np
import json
import time


def run_case(evidence,count,gram,degree=4,step=.008,tag=''):
    system=FixedGridMovingTrace(count,gram,degree=degree,radial_degree=18)
    initial=tangent_preparation(system)
    initial_geometry=system.geometry(initial)
    initial_mass=float(initial_geometry.outer_mass)
    initial_cells=initial_geometry.layer(system.offsets)['cell']
    times=np.linspace(0.,.2,11)
    def cell_event(time,state):
        positions=system.values(state)[:,2*system.count]-system.width*system.offsets
        return float(min(np.min(positions-system.radii[initial_cells]),
                         np.min(system.radii[initial_cells+1]-positions))-1e-8)
    cell_event.terminal=True
    cell_event.direction=-1
    started=time.perf_counter()
    result=solve_ivp(system.rhs,(0,.2),initial,method='DOP853',rtol=2e-10,atol=2e-13,
                     max_step=step,t_eval=times,events=cell_event)
    label=('MTS' if gram else 'reference')+'-'+str(count)+'-degree-'+str(degree)+tag
    path=evidence.output/(label+'.npz')
    np.savez_compressed(path,times=result.t,states=result.y,initial_state=initial,
                        event_times=result.t_events[0],event_states=result.y_events[0],
                        offsets=system.offsets,radii=system.radii)
    evidence.own(path,'outputs')
    evidence.check(label+'_completed_regular_cell_window',result.success and len(result.t)==len(times) and
                   not len(result.t_events[0]),result.message)
    rows=[]
    for time_point,state in zip(result.t,result.y.T):
        evaluation=system.evaluate(time_point,state)
        geometry=evaluation['geometry']
        probes=geometry.material(np.array([-.3,0.,.3]))['R'].ravel()
        current=geometry.mass_current(probes,evaluation['multipliers'])
        varied=system.geometry(state.astype(complex)+1e-22j*evaluation['rhs'])
        derivative=varied.metric(probes)['mu'].imag/1e-22
        mass_error=float(abs(geometry.outer_mass-initial_mass))
        rows.append(dict(time=float(time_point),trace_error=float(np.max(abs(evaluation['trace']))),
                         trace_rate_error=float(np.max(abs(evaluation['trace_rate']))),
                         current_error=float(np.max(abs(derivative-current['total']))),
                         current_scale=float(np.max(abs(current['total']))),
                         outer_mass_error=mass_error,
                         relative_active_energy_error=mass_error/abs(initial_mass-system.central_mass),
                         independent_outer_mass_rate=float(varied.outer_mass.imag/1e-22),
                         minimum_F=float(np.min(evaluation['data']['U']**2)),
                         minimum_source_jacobian=geometry.minimum_source_jacobian,
                         source_force_max=float(np.max(abs(evaluation['multipliers']*evaluation['trace_gradient']))),
                         source_position=float(evaluation['data']['b'][degree//2]),
                         source_proper_clock=float(evaluation['data']['theta'][degree//2]),
                         maximum_overlap=geometry.maximum_overlap))
    summary=dict(branch='MTS' if gram else 'reference',count=count,degree=degree,step=step,tag=tag,
                 wall_seconds=time.perf_counter()-started,nfev=result.nfev,initial_outer_mass=initial_mass,
                 max_trace_error=max(row['trace_error'] for row in rows),
                 max_trace_rate_error=max(row['trace_rate_error'] for row in rows),
                 max_current_error=max(row['current_error'] for row in rows),
                 max_outer_mass_error=max(row['outer_mass_error'] for row in rows),
                 max_relative_active_energy_error=max(row['relative_active_energy_error'] for row in rows),
                 minimum_F=min(row['minimum_F'] for row in rows),
                 minimum_source_jacobian=min(row['minimum_source_jacobian'] for row in rows),
                 maximum_source_wave_force=max(row['source_force_max'] for row in rows),
                 final_source_position=rows[-1]['source_position'],final_source_proper_clock=rows[-1]['source_proper_clock'])
    evidence.report['cases'].append(summary)
    diagnostics=evidence.output/(label+'-diagnostics.json')
    diagnostics.write_text(json.dumps(dict(summary=summary,samples=rows),indent=2)+'\n',encoding='utf-8')
    evidence.own(diagnostics,'outputs')
    evidence.check(label+'_independent_local_gravity',summary['max_current_error']<2e-7,summary)
    evidence.check(label+'_trace_no_projection',max(summary['max_trace_error'],summary['max_trace_rate_error'])<2e-9)
    evidence.check(label+'_active_energy_no_projection',summary['max_relative_active_energy_error']<1e-7)
    evidence.check(label+'_regular_positive_window',summary['minimum_F']>.15 and summary['minimum_source_jacobian']>0)
    evidence.check(label+'_nonzero_wave_force',summary['maximum_source_wave_force']>1e-6)
    print(summary,flush=True)
    return result.y


def main():
    evidence=EvidenceRun('annular-fixed-grid-moving-trace-smooth-evolution-attempt01',__file__)
    try:
        evidence.report.update(scope='Two-sided finite-width moving reflecting trace on fixed scalar nodes, with live spherical gravity.',
                               elapsed_target=.2,source_initial_width=.001,
                               initial_velocity_preparation='Global smooth source-comoving velocity, not a stencil-local momentum patch.',
                               conservation_or_trace_position_projection=False,
                               full_GR_limit_proven=False,
                               previous_one_sided_moving_collar_equivalence_proven=False,
                               continuum_waveform_accuracy_qualified=False,
                               gates=dict(local_mass_current=2e-7,trace_and_trace_rate=2e-9,
                                          relative_active_energy=1e-7))
        originals={}
        for count in [33,65,129]:
            for gram in [False,True]:
                originals[count,gram]=run_case(evidence,count,gram)
        for gram in [False,True]:
            half=run_case(evidence,33,gram,step=.004,tag='-half-step')
            error=float(np.max(abs(half-originals[33,gram])))
            evidence.check(('MTS' if gram else 'reference')+'_half_step_state',error<2e-8,error)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()



