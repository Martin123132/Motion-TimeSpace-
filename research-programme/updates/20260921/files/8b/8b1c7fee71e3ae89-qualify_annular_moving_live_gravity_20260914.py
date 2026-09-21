from derive_annular_source_gravity_20260914 import EvidenceRun, DustGravityCollar
from annular_moving_live_gravity_20260914 import MovingLiveGravity
from annular_moving_collar_action_20260914 import MovingCollarAction
import numpy as np
import time


def main():
    evidence=EvidenceRun('annular-moving-live-gravity-qualification-attempt01',__file__)
    try:
        for gram in [False,True]:
            system=MovingLiveGravity(33,gram,degree=6,radial_degree=16)
            state=system.initial_state.copy()
            values=system.values(state)
            values[:,system.free:2*system.free]=.005*values[:,:system.free]
            values[:,2*system.free+1]=-.00008*(1+.03*system.offsets)
            started=time.perf_counter()
            evaluation=system.evaluate(0,state)
            duration=time.perf_counter()-started
            geometry=evaluation['geometry']
            probes=geometry.material(np.array([-.3,0.,.3]))['R'].ravel()
            current=geometry.mass_current(probes)
            step=1e-22
            varied=system.geometry(state.astype(complex)+1j*step*evaluation['rhs'])
            derivative=varied.metric(probes)['mu'].imag/step
            error=float(np.max(abs(derivative-current['total'])))
            scale=float(np.max(abs(current['total'])))
            data=dict(branch='MTS' if gram else 'reference',seconds_per_evaluation=duration,
                      radial_constraint_defect=geometry.constraint_defect,
                      current_error=error,current_scale=scale,relative_current_error=error/max(scale,1e-30),
                      source_jacobian=geometry.minimum_source_jacobian,
                      initial_outer_mass=float(geometry.outer_mass),
                      independent_outer_mass_rate=float(varied.outer_mass.imag/step))
            evidence.report['cases'].append(data)
            raw=evidence.output/(data['branch']+'-state-current.npz')
            np.savez_compressed(raw,state=state,rhs=evaluation['rhs'],radii=probes,mass_rate=derivative,**current)
            evidence.own(raw,'outputs')
            evidence.check(data['branch']+'_finite_radial_geometry',geometry.constraint_defect<2e-11 and
                           np.all(np.isfinite(evaluation['rhs'])),data)
            print(data,flush=True)
        dust=MovingLiveGravity(17,False,degree=8,radial_degree=20,amplitude=0)
        state=dust.initial_state.copy()
        values=dust.values(state)
        values[:,2*dust.free+1]=-.00008*(1+.03*dust.offsets)
        test=dust.evaluate(0,state)
        direct=DustGravityCollar(8,width=dust.width)
        direct_state=direct.initial_state.copy()
        direct_state[direct.count:2*direct.count]=values[:,2*dust.free+1]
        direct_flow=direct.rhs(0,direct_state).reshape(3,direct.count).T
        derived=dust.values(test['rhs'])[:,2*dust.free:]
        error=float(np.max(abs(direct_flow-derived)))
        evidence.check('independent_live_dust_control',error<2e-8,error)
        flat=MovingLiveGravity(33,True,degree=6,radial_degree=12,coupling=0,central_mass=0)
        state=flat.initial_state.copy()
        values=flat.values(state)
        values[:,flat.free:2*flat.free]=.005*values[:,:flat.free]
        values[:,2*flat.free+1]=.0002
        test=flat.evaluate(0,state)
        center=flat.degree//2
        older=MovingCollarAction(33,True)
        old_state=older.pack(test['data']['q'][center: center+1,:-1],
                            test['data']['pi'][center: center+1,:-1],
                            test['data']['b'][center:center+1],test['data']['V'][center:center+1])
        flow=older.rhs(0,old_state)
        old_q,old_pi,old_b,old_v=older.unpack(flow)
        total_rate=older.source_canonical(old_state.astype(complex)+1e-22j*flow).imag/1e-22
        flat_rate=flat.values(test['rhs'])[center]
        error=max(float(np.max(abs(old_q[0]-flat_rate[:flat.free]))),
                  float(np.max(abs(old_pi[0]-flat_rate[flat.free:2*flat.free]))),
                  float(abs(old_b[0]-flat_rate[2*flat.free])),
                  float(abs(total_rate[0]-flat_rate[2*flat.free+1])))
        evidence.check('independent_old_flat_action_control',error<2e-10,error)
        for row in evidence.report['cases']:
            evidence.check(row['branch']+'_independent_temporal_mass_equation',row['current_error']<2e-7,row)
        evidence.report.update(full_wave_gravity_evolved=False,full_GR_limit_proven=False,
                               conditional_radial_and_embedding_implementation=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

