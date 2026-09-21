import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator
from annular_dynamical_source_20260914 import outgoing_profile
from annular_moving_collar_action_20260914 import MovingCollarAction
from annular_reference_continuum_shell_20260914 import EvidenceRun


class ExactLayer:
    def __init__(self,initial_radius,amplitude=.01,mass=.003):
        self.initial_radius=initial_radius
        self.amplitude=amplitude
        def rhs(retarded,state):
            profile,rate=outgoing_profile(retarded,amplitude)
            return [2*float(rate)**2/mass,state[0]**2]
        solution=solve_ivp(rhs,(-initial_radius,-4.4),[1.,initial_radius],method='DOP853',
                           rtol=2e-13,atol=2e-15,max_step=.0005,dense_output=True)
        if not solution.success:
            raise RuntimeError(solution.message)
        self.solution=solution
        retarded=np.linspace(-initial_radius,-4.4,20001)
        doppler,advanced=solution.sol(retarded)
        self.time_to_u=PchipInterpolator((advanced+retarded)/2,retarded,extrapolate=False)
        self.advanced_to_u=PchipInterpolator(advanced,retarded,extrapolate=False)
        self.advanced_min=initial_radius
        self.advanced_max=advanced[-1]

    def source(self,time):
        retarded=self.time_to_u(time)
        doppler,advanced=self.solution.sol(retarded)
        return (advanced-retarded)/2,(doppler**2-1)/(doppler**2+1)

    def field(self,time,radius):
        value,rate=outgoing_profile(time-radius,self.amplitude)
        incoming=np.zeros_like(radius)
        incoming_rate=np.zeros_like(radius)
        advanced=time+radius
        selected=(advanced>=self.advanced_min)&(advanced<=self.advanced_max)
        if np.any(selected):
            retarded=self.advanced_to_u(advanced[selected])
            doppler=self.solution.sol(retarded)[0]
            incoming[selected],incoming_rate[selected]=outgoing_profile(retarded,self.amplitude)
            incoming[selected]*=-1
            incoming_rate[selected]/=-doppler**2
        scalar=(value+incoming)/radius
        scalar_time=(rate+incoming_rate)/radius
        scalar_radius=(-rate+incoming_rate)/radius-scalar/radius
        return scalar,scalar_time,scalar_radius


def run_case(evidence,count,gram,max_step_factor=.1,stop=1.1,tag=''):
    nodes,weights=np.polynomial.legendre.leggauss(3)
    offsets=nodes/2
    weights=weights/2*6*(offsets+.5)*(.5-offsets)
    system=MovingCollarAction(count,gram,offsets,weights)
    times=np.linspace(0.,stop,45)
    branch='MTS' if gram else 'reference'
    label=branch+'-'+str(count)+tag
    solution=solve_ivp(system.rhs,(0.,stop),system.initial_state,method='DOP853',
                       rtol=3e-10,atol=3e-13,max_step=3/(count-1)*max_step_factor,
                       t_eval=times)
    raw=evidence.output/(label+'.npz')
    np.savez_compressed(raw,times=solution.t,states=solution.y,offsets=offsets,weights=weights,
                        count=count,gram=gram,max_step_factor=max_step_factor)
    evidence.own(raw,'outputs')
    evidence.check(label+'_integrator_complete',solution.success and len(solution.t)==len(times),solution.message)
    targets=[ExactLayer(6+system.width*offset) for offset in offsets]
    energy_initial=system.energy(system.initial_state)['total']
    rows=[]
    for index,time in enumerate(solution.t):
        state=solution.y[:,index]
        scalar,momentum,position,velocity=system.unpack(state)
        data=system.fields(state)
        energy=system.energy(state)
        exact_source=np.array([target.source(time) for target in targets])
        target_scalar=np.array([target.field(time,radius)[0] for target,radius in zip(targets,data['radii'])])
        target_time=np.array([target.field(time,radius)[1] for target,radius in zip(targets,data['radii'])])
        target_radius=np.array([target.field(time,radius)[2] for target,radius in zip(targets,data['radii'])])
        full_scalar=np.pad(scalar,((0,0),(0,1)))
        material_transport=(system.transport_endpoint @ scalar.T).T[:,0]/data['length']
        full_time=np.column_stack([momentum/data['mass'],-velocity*material_transport])
        full_gradient=np.zeros_like(full_scalar)
        full_gradient[:,1:-1]=(full_scalar[:,2:]-full_scalar[:,:-2])/(2*data['length'][:,None]*system.reference_spacing)
        full_gradient[:,0]=(full_scalar[:,1]-full_scalar[:,0])/(data['length']*system.reference_spacing)
        full_gradient[:,-1]=(full_scalar[:,-1]-full_scalar[:,-2])/(data['length']*system.reference_spacing)
        spatial_weights=data['length'][:,None]*system.trapezoid*data['radii']**2
        weighted=lambda values:float(system.weights @ np.sum(spatial_weights*values,axis=1))
        normalization=max(weighted(target_time**2+target_radius**2),1e-30)
        wave_error=np.sqrt(weighted((full_time-target_time)**2+(full_gradient-target_radius)**2)/normalization)
        scalar_error=np.sqrt(weighted((full_scalar-target_scalar)**2)/max(weighted(target_scalar**2),1e-30))
        rows.append(dict(time=float(time),wave_relative_error=float(wave_error),scalar_relative_error=float(scalar_error),
                         position_error=float(np.max(abs(position-exact_source[:,0]))),
                         velocity_error=float(np.max(abs(velocity-exact_source[:,1]))),
                         relative_energy_error=float(abs(energy['total']-energy_initial)/energy_initial),
                         minimum_layer_separation=float(np.min(np.diff(position))),
                         edge_inertia_ratio=float(np.max(energy['edge_inertia']/system.source_mass)),
                         positions=position.tolist(),velocities=velocity.tolist()))
    diagnostics=evidence.output/(label+'-diagnostics.json')
    import json
    diagnostics.write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    evidence.own(diagnostics,'outputs')
    result=dict(branch=branch,count=count,rhs_evaluations=solution.nfev,
                max_wave_error=max(row['wave_relative_error'] for row in rows),
                final_wave_error=rows[-1]['wave_relative_error'],
                max_scalar_error=max(row['scalar_relative_error'] for row in rows),
                max_position_error=max(row['position_error'] for row in rows),
                max_velocity_error=max(row['velocity_error'] for row in rows),
                max_relative_energy_error=max(row['relative_energy_error'] for row in rows),
                min_layer_separation=min(row['minimum_layer_separation'] for row in rows),
                max_edge_inertia_ratio=max(row['edge_inertia_ratio'] for row in rows),
                final_positions=rows[-1]['positions'],final_velocities=rows[-1]['velocities'])
    evidence.report['cases'].append(result)
    evidence.save()
    evidence.check(label+'_finite_timelike_positive_ordered',np.all(np.isfinite(solution.y)) and
                   max(abs(np.array([row['velocities'] for row in rows])).ravel())<1 and
                   result['min_layer_separation']>0)
    evidence.check(label+'_action_energy_balance',result['max_relative_energy_error']<1e-8,result['max_relative_energy_error'])
    print(result,flush=True)
    return result


def main():
    evidence=EvidenceRun('annular-moving-collar-flat-attempt01',__file__)
    evidence.report.update(external_force_history_prescribed=False,full_Gram_factors_retained=True,
                           finite_collar_motion_minimal_extension_assumed=True,
                           all_layers_rigidly_locked=False,
                           gates=dict(max_wave_error=.005,max_position_error=.001,max_velocity_error=.001,
                                      max_relative_energy_error=1e-8))
    evidence.save()
    try:
        for gram in [False,True]:
            for count in [33,65,129,257,513]:
                run_case(evidence,count,gram)
        for branch in ['reference','MTS']:
            rows=[row for row in evidence.report['cases'] if row['branch']==branch]
            evidence.check(branch+'_all_declared_errors_refine',
                           all(rows[-1][key]<rows[-2][key] for key in
                               ['max_wave_error','max_scalar_error','max_position_error','max_velocity_error']))
            evidence.check(branch+'_finest_original_accuracy_gates',
                           all(rows[-1][key]<threshold for key,threshold in evidence.report['gates'].items()),rows[-1])
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

