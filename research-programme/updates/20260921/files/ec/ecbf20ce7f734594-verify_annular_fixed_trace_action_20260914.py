from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_fixed_grid_moving_trace_20260914 import FixedGridMovingTrace
from qualify_annular_fixed_grid_moving_trace_20260914 import tangent_preparation
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import roots_legendre


NODES=np.array([5.875,6.,6.125,6.25])


def source(time):
    return 6.03+.07*time+.01*np.sin(time),.07+.01*np.cos(time)


def scalar(time,radius):
    return .03*np.sin(.7*time+.4*radius)


def scalar_rate(time,radius):
    return .021*np.cos(.7*time+.4*radius)


def multiplier(time):
    return .04*(1+.2*np.cos(time))


def weights(position):
    cell=np.searchsorted(NODES,position.real)-1
    values=np.zeros(len(NODES),dtype=np.result_type(position))
    fraction=(position-NODES[cell])/(NODES[cell+1]-NODES[cell])
    values[cell]=1-fraction
    values[cell+1]=fraction
    return values


def clock(time,radius):
    offset=radius-6
    scale=np.exp(.3*offset)
    displacement=.15*offset+.04*offset**2
    value=scale*time+displacement
    radial=.3*scale*time+.15+.08*offset
    return value,scale,radial


def original_metric(time,radius):
    return .93+.012*(radius-6),.85+.01*(radius-6)


def transformed_metric(time,radius):
    old,scale,radial=clock(time,radius)
    lapse,root=original_metric(old,radius)
    radial_metric=1/root**2-lapse**2*radial**2
    cross=-scale*lapse**2*radial
    geometry=1/radial_metric
    shift=cross/radial_metric
    new_lapse=np.sqrt(scale**2*lapse**2+cross**2/radial_metric)
    return new_lapse,np.sqrt(geometry),shift


def inverse_source_time(old):
    position,velocity=source(old)
    displacement=clock(0.,position)[0]
    scale=clock(0.,position)[1]
    return (old-displacement)/scale


def transformed_slice(new_time):
    old_time=brentq(lambda old:clock(new_time,source(old)[0])[0]-old,-1.,1.,xtol=2e-14)
    position,velocity=source(old_time)
    unused,scale,radial=clock(new_time,position)
    clock_rate=scale/(1-velocity*radial)
    new_velocity=velocity*clock_rate
    lapse,root,shift=transformed_metric(new_time,position)
    proper=np.sqrt(lapse**2-(new_velocity+shift)**2/root**2)
    original_lapse,original_root=original_metric(old_time,position)
    old_proper=np.sqrt(original_lapse**2-velocity**2/original_root**2)
    trace=0.
    naive=0.
    for radius,weight in zip(NODES,weights(position)):
        if weight==0:
            continue
        def rhs(location,value):
            unused,local_scale,local_radial=clock(value[0],location)
            return [-local_radial/local_scale]
        link=solve_ivp(rhs,(position,radius),[new_time],method='DOP853',rtol=2e-12,atol=2e-14)
        if not link.success:
            raise RuntimeError(link.message)
        linked_old=clock(link.y[0,-1],radius)[0]
        trace+=weight*scalar(linked_old,radius)
        naive+=weight*scalar(clock(new_time,radius)[0],radius)
    original_trace=weights(position) @ scalar(old_time,NODES)
    actual=-.003*proper+multiplier(old_time)*clock_rate*trace
    expected=clock_rate*(-.003*old_proper+multiplier(old_time)*original_trace)
    return dict(actual=actual,expected=expected,trace_error=abs(trace-original_trace),
                clock_error=abs(proper-clock_rate*old_proper),naive_error=abs(naive-original_trace))


def shifted_slice(time,parameter):
    position,velocity=source(time)
    lapse,root=original_metric(time,position)
    profile=lambda clock_value,radius:.02*(1+.1*clock_value+.05*(radius-6))
    shift=parameter*profile(time,position)
    proper=np.sqrt(lapse**2-(velocity+shift)**2/root**2)
    trace=0.
    derivative=0.
    points,quadrature=roots_legendre(16)
    for radius,weight in zip(NODES,weights(position)):
        if weight==0:
            continue
        def rhs(location,value):
            local_lapse,local_root=original_metric(value[0],location)
            beta=parameter*profile(value[0],location)
            return [beta/(local_lapse**2*local_root**2-beta**2)]
        link=solve_ivp(rhs,(position,radius),[time],method='DOP853',rtol=2e-12,atol=2e-14)
        if not link.success:
            raise RuntimeError(link.message)
        trace+=weight*scalar(link.y[0,-1],radius)
        locations=(position+radius)/2+(radius-position)*points/2
        local_lapse,local_root=original_metric(time,locations)
        connection_variation=(radius-position)/2*np.sum(quadrature*profile(time,locations)/(local_lapse**2*local_root**2))
        derivative+=weight*scalar_rate(time,radius)*connection_variation
    proper_zero=np.sqrt(lapse**2-velocity**2/root**2)
    analytic=.003*velocity*profile(time,position)/(root**2*proper_zero)+multiplier(time)*derivative
    return -.003*proper+multiplier(time)*trace,analytic


def main():
    evidence=EvidenceRun('annular-fixed-trace-action-and-clock-attempt01',__file__)
    try:
        rows=[transformed_slice(time) for time in np.linspace(-.12,.12,7)]
        evidence.check('moving_source_proper_clock_covariance',max(row['clock_error'] for row in rows)<2e-12)
        evidence.check('transported_trace_is_a_scalar',max(row['trace_error'] for row in rows)<2e-12)
        evidence.check('proper_source_plus_trace_action_density_covariance',max(abs(row['actual']-row['expected']) for row in rows)<2e-12)
        evidence.check('unlinked_simultaneous_interpolation_is_detectably_wrong',max(row['naive_error'] for row in rows)>1e-6)
        points,quadrature=roots_legendre(14)
        bounds=[inverse_source_time(value) for value in [-.1,.1]]
        transformed_integral=sum((bounds[1]-bounds[0])*weight/2*
                                  transformed_slice((bounds[0]+bounds[1])/2+(bounds[1]-bounds[0])*point/2)['actual']
                                  for point,weight in zip(points,quadrature))
        original_integral=0.
        for time,weight in zip(.1*points,.1*quadrature):
            position,velocity=source(time)
            lapse,root=original_metric(time,position)
            proper=np.sqrt(lapse**2-velocity**2/root**2)
            original_integral+=weight*(-.003*proper+multiplier(time)*(weights(position) @ scalar(time,NODES)))
        evidence.check('same_physical_source_window_action',abs(transformed_integral-original_integral)<2e-12,
                       float(abs(transformed_integral-original_integral)))
        for time in [-.1,0.,.1]:
            step=.002
            values={factor:shifted_slice(time,factor*step)[0] for factor in [-2,-1,1,2]}
            difference=(values[-2]-8*values[-1]+8*values[1]-values[2])/(12*step)
            analytic=shifted_slice(time,0.)[1]
            evidence.check(str(time)+'_independent_moving_trace_shift_variation',abs(difference-analytic)<2e-11,
                           float(abs(difference-analytic)))
        for gram in [False,True]:
            system=FixedGridMovingTrace(33,gram,coupling=0,central_mass=0)
            state=tangent_preparation(system)
            evaluation=system.evaluate(0,state)
            data=evaluation['data']
            gradient=evaluation['trace_gradient']
            expected=np.sum(data['trace_weights']**2/(system.node_weights*data['R'][:,:system.count]**2),axis=1)
            expected+=system.source_mass**2*gradient**2/data['E']**3
            error=float(np.max(abs(evaluation['multiplier_matrix']-np.diag(expected))))
            evidence.check(str(gram)+'_flat_positive_multiplier_matrix',error<2e-11,error)
            source_power=evaluation['multipliers']*data['V']*gradient
            wave_power=evaluation['multipliers']*np.sum(data['trace_weights']*evaluation['qdot'],axis=1)
            evidence.check(str(gram)+'_constraint_force_energy_exchange',np.max(abs(source_power+wave_power))<2e-12)
        evidence.report.update(manufactured_covariance_cases=rows,
                               moving_trace_added_action_covariance_checked=True,
                               full_parent_matter_action_uniqueness_proven=False,
                               arbitrary_spatial_diffeomorphism_invariance_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

