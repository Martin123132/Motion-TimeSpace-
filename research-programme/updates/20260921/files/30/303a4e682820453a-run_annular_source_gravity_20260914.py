from derive_annular_source_gravity_20260914 import EvidenceRun, DustGravityCollar
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from annular_covariant_scalar_action_20260912 import full_spatial_factors
import json


def cycloid(radius,mass,proper_time):
    if proper_time<=0:
        return radius,0.
    scale=np.sqrt(radius**3/(8*mass))
    phase=brentq(lambda value:scale*(value+np.sin(value))-proper_time,0.,np.pi-1e-8,xtol=1e-14)
    return radius*(1+np.cos(phase))/2,-np.sqrt(2*mass/radius)*np.tan(phase/2)


def one_case(evidence,degree,width=.001,step=.01,tag=''):
    system=DustGravityCollar(degree,width)
    times=np.linspace(0,1.6,41)
    solution=solve_ivp(system.rhs,(0,1.6),system.initial_state,method='DOP853',rtol=2e-11,
                       atol=2e-14,max_step=step,t_eval=times)
    name='degree-'+str(degree)+tag
    path=evidence.output/(name+'.npz')
    np.savez_compressed(path,times=solution.t,states=solution.y,offsets=system.offsets,
                        initial_mass=system.initial_geometry['mass'],width=width,degree=degree)
    evidence.own(path,'outputs')
    evidence.check(name+'_integrator_complete',solution.success and len(solution.t)==len(times),solution.message)
    rows=[]
    for time,state in zip(solution.t,solution.y.T):
        diagnostics=system.diagnostics(state)
        exact=np.array([cycloid(initial,enclosed,clock) for initial,enclosed,clock in
                        zip(system.initial_state[:system.count],system.initial_geometry['mass'],diagnostics['proper_times'])])
        flow=system.rhs(time,state)
        varied=system.geometry(state.astype(complex)+1e-25j*flow)
        rows.append(dict(time=float(time),
                         position_error=float(np.max(abs(exact[:,0]-diagnostics['position']))),
                         proper_velocity_error=float(np.max(abs(exact[:,1]-diagnostics['proper_rate']))),
                         material_mass_error=diagnostics['max_material_mass_error'],
                         exterior_mass_error=diagnostics['exterior_mass_error'],
                         binding_error=diagnostics['max_binding_error'],
                         material_mass_rate_error=float(np.max(abs(varied['mass'].imag/1e-25))),
                         minimum_jacobian=diagnostics['minimum_jacobian'],
                         minimum_F=diagnostics['minimum_F'],
                         radial_constraint_defect=diagnostics['constraint_defect']))
    diagnostic_path=evidence.output/(name+'-diagnostics.json')
    diagnostic_path.write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    evidence.own(diagnostic_path,'outputs')
    result=dict(degree=degree,width=width,step=step,nfev=solution.nfev,
                max_position_error=max(row['position_error'] for row in rows),
                max_proper_velocity_error=max(row['proper_velocity_error'] for row in rows),
                max_material_mass_error=max(row['material_mass_error'] for row in rows),
                max_exterior_mass_error=max(row['exterior_mass_error'] for row in rows),
                max_binding_error=max(row['binding_error'] for row in rows),
                max_material_mass_rate_error=max(row['material_mass_rate_error'] for row in rows),
                minimum_jacobian=min(row['minimum_jacobian'] for row in rows),
                minimum_F=min(row['minimum_F'] for row in rows),
                final_central_position=float(solution.y[degree//2,-1]),
                final_central_proper_time=float(solution.y[2*system.count+degree//2,-1]))
    evidence.report['cases'].append(result)
    evidence.check(name+'_independent_GR_proper_time_trajectory',
                   max(result['max_position_error'],result['max_proper_velocity_error'])<2e-8,result)
    evidence.check(name+'_mass_and_energy_not_imposed',
                   max(result['max_material_mass_error'],result['max_material_mass_rate_error'])<2e-11 and
                   result['max_binding_error']<2e-9)
    evidence.check(name+'_regular_ordered_timelike_window',result['minimum_jacobian']>0 and result['minimum_F']>.15)
    print(result,flush=True)
    return system,solution


def main():
    evidence=EvidenceRun('annular-source-gravity-evolution-attempt01',__file__)
    try:
        evidence.report.update(scalar_wave_identically_zero=True,
                               source_force_from_live_metric=True,
                               material_mass_or_ADM_energy_imposed=False,
                               no_independent_MTS_advantage_in_zero_scalar_sector=True,
                               full_scalar_gravity_coupling_evolved=False)
        for gram in [False,True]:
            factors,sampling=full_spatial_factors(33,gram)
            zero=np.zeros(33)
            evidence.check(str(gram)+'_zero_scalar_action_and_gradient_exactly_zero',
                           np.array_equal(factors @ zero,np.zeros(len(factors))) and
                           np.array_equal(factors.T @ (factors @ zero),zero))
        for degree in [8,12,16,24]:
            one_case(evidence,degree)
        half_system,half_solution=one_case(evidence,16,step=.005,tag='-half')
        original=np.load(evidence.output/'degree-16.npz')
        difference=float(np.max(abs(original['states']-half_solution.y)))
        evidence.check('independent_half_step_evolution',difference<2e-9,difference)
        flat=DustGravityCollar(12,.001,coupling=0,central_mass=0)
        state=flat.initial_state.copy()
        state[flat.count:2*flat.count]=-.0001
        solution=solve_ivp(flat.rhs,(0,1.6),state,method='DOP853',rtol=2e-12,atol=2e-14,max_step=.01)
        energy=np.sqrt(.003**2+.0001**2)
        expected=state.copy()
        expected[:flat.count]-=1.6*.0001/energy
        expected[2*flat.count:]=1.6*.003/energy
        error=float(np.max(abs(solution.y[:,-1]-expected)))
        evidence.check('zero_gravity_inertial_source_control',solution.success and error<2e-11,error)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

