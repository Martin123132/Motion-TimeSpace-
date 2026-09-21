from derive_annular_source_gravity_20260914 import EvidenceRun, DustGravityCollar
from run_annular_source_gravity_20260914 import cycloid
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import json


def polynomial_minimum(system,state):
    position=system.unpack(state)[0]
    coefficients=system.rule.inverse @ (position-system.initial_radius)
    first=2*np.polynomial.chebyshev.chebder(coefficients)
    second=np.polynomial.chebyshev.chebder(first)
    roots=np.polynomial.chebyshev.chebroots(second)
    interior=roots.real[(abs(roots.imag)<1e-7)&(roots.real>-1)&(roots.real<1)]
    probes=np.concatenate(([-1.,1.],interior))
    values=np.polynomial.chebyshev.chebval(probes,first)
    selected=int(np.argmin(values))
    return float(values[selected]),float(probes[selected]/2)


def independent_GR_jacobian(system,state):
    data=system.geometry(state)
    clocks=system.unpack(state)[2]
    initial=system.initial_geometry
    answer=[]
    for radius,mass,mass_z,clock,geometry,binding in zip(initial['position'],initial['mass'],
            initial['mass_z'],clocks,data['F'],initial['F']):
        scale=np.sqrt(radius**3/(8*mass))
        phase=0. if clock<=0 else brentq(lambda value:scale*(value+np.sin(value))-clock,
                                        0.,np.pi-1e-8,xtol=1e-14)
        scale_gradient=1.5*system.width/radius-.5*mass_z/mass
        at_proper_time=system.width*(1+np.cos(phase))/2
        at_proper_time+=radius*np.sin(phase)/(2*(1+np.cos(phase)))*(phase+np.sin(phase))*scale_gradient
        answer.append(geometry/binding*at_proper_time)
    return np.array(answer)


def one_case(evidence,width,degree=16,steps=100,tag=''):
    system=DustGravityCollar(degree,width)
    acceleration,leading,prediction=system.initial_focusing()
    def event(time,state):
        return polynomial_minimum(system,state)[0]
    event.terminal=True
    event.direction=-1
    solution=solve_ivp(system.rhs,(0,1.35*prediction),system.initial_state,method='DOP853',
                       rtol=2e-11,atol=2e-14,max_step=prediction/steps,events=event,dense_output=True)
    name='width-'+format(width,'.0e')+'-degree-'+str(degree)+tag
    raw=evidence.output/(name+'.npz')
    np.savez_compressed(raw,times=solution.t,states=solution.y,event_times=solution.t_events[0],
                        event_states=solution.y_events[0],offsets=system.offsets,
                        initial_mass=system.initial_geometry['mass'],width=width,degree=degree)
    evidence.own(raw,'outputs')
    evidence.check(name+'_first_crossing_captured',solution.success and len(solution.t_events[0])==1,
                   solution.message)
    crossing=float(solution.t_events[0][0])
    rows=[]
    for time in np.linspace(0,crossing*.99,25):
        state=solution.sol(time)
        data=system.geometry(state)
        exact=independent_GR_jacobian(system,state)
        jacobian_error=float(np.max(abs(data['position_z']-exact)))
        clock_gradient=system.derivative @ system.unpack(state)[2]
        proper_rate=data['F']*data['momentum']/system.source_mass
        clock_error=float(np.max(abs(clock_gradient+proper_rate*data['position_z']/data['F'])))
        diagnostics=system.diagnostics(state)
        rows.append(dict(time=float(time),jacobian_error=jacobian_error,clock_gradient_error=clock_error,
                         minimum_F=diagnostics['minimum_F'],material_mass_error=diagnostics['max_material_mass_error'],
                         binding_error=diagnostics['max_binding_error'],
                         minimum_jacobian=polynomial_minimum(system,state)[0]))
    event_state=solution.y_events[0][0]
    event_data=system.geometry(event_state)
    exact_event=independent_GR_jacobian(system,event_state)
    result=dict(width=width,degree=degree,steps=steps,crossing_time=crossing,
                leading_prediction=prediction,ratio=crossing/prediction,
                time_over_sqrt_width=crossing/np.sqrt(width),
                crossing_label=polynomial_minimum(system,event_state)[1],
                minimum_F=min(row['minimum_F'] for row in rows),
                max_GR_jacobian_error=max(row['jacobian_error'] for row in rows),
                max_clock_gradient_error=max(row['clock_gradient_error'] for row in rows),
                max_mass_error=max(row['material_mass_error'] for row in rows),
                max_binding_error=max(row['binding_error'] for row in rows),
                event_GR_jacobian_error=float(np.max(abs(exact_event-event_data['position_z']))),
                physical_evolution_stopped_at_crossing=True,nfev=solution.nfev)
    path=evidence.output/(name+'-diagnostics.json')
    path.write_text(json.dumps(dict(summary=result,regular_samples=rows),indent=2)+'\n',encoding='utf-8')
    evidence.own(path,'outputs')
    evidence.report['cases'].append(result)
    evidence.check(name+'_GR_clock_and_label_control',
                   max(result['max_GR_jacobian_error'],result['event_GR_jacobian_error'])<2e-10 and
                   result['max_clock_gradient_error']<2e-9,result)
    evidence.check(name+'_no_mass_loss_or_chart_horizon',
                   result['max_mass_error']<2e-11 and result['max_binding_error']<2e-9 and result['minimum_F']>.7)
    evidence.check(name+'_square_root_leading_window',
                   abs(result['ratio']-1)<.03 if width<=1e-5 else abs(result['ratio']-1)<.2,result['ratio'])
    print(result,flush=True)
    return result


def main():
    evidence=EvidenceRun('annular-source-gravity-focusing-attempt01',__file__)
    try:
        evidence.report.update(scalar_wave_identically_zero=True,
                               reference_and_MTS_same_source_sector=True,
                               dust_caustic_is_not_MTS_specific=True,
                               weak_thin_shell_limit_ruled_out=False,
                               uniform_fixed_time_ordered_dust_thin_limit_proven=False,
                               pressure_or_rigid_lock_added=False,
                               event_scope='First zero of the interpolated material Jacobian; not a horizon test.',
                               gates=dict(GR_jacobian_error=2e-10,clock_gradient_error=2e-9,
                                          material_mass_error=2e-11,binding_error=2e-9))
        originals={}
        for width in [1e-4,3e-5,1e-5,3e-6,1e-6,3e-7,1e-7]:
            originals[width]=one_case(evidence,width)
        degree=one_case(evidence,1e-6,degree=24)
        half=one_case(evidence,1e-6,steps=200,tag='-half-step')
        original=originals[1e-6]
        evidence.check('crossing_degree_and_time_step_controls',
                       max(abs(degree['crossing_time']/original['crossing_time']-1),
                           abs(half['crossing_time']/original['crossing_time']-1))<2e-5,
                       dict(degree=degree['crossing_time'],original=original['crossing_time'],
                            half_step=half['crossing_time']))
        narrow=[originals[width] for width in [3e-6,1e-6,3e-7,1e-7]]
        slope=float(np.polyfit(np.log([row['width'] for row in narrow]),
                               np.log([row['crossing_time'] for row in narrow]),1)[0])
        evidence.report['measured_thin_width_exponent']=slope
        evidence.check('narrow_width_exponent_near_derived_half',abs(slope-.5)<.01,slope)
        evidence.check('first_caustic_near_positive_density_center',
                       max(abs(row['crossing_label']) for row in narrow)<.01)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

