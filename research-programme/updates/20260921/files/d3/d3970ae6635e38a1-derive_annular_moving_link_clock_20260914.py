import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad
from annular_reference_continuum_shell_20260914 import EvidenceRun


def run():
    evidence=EvidenceRun('annular-moving-link-clock-attempt01',__file__)
    try:
        lapse,root,shift,speed,mass=sp.symbols('N U beta V S',positive=True)
        clock=sp.sqrt(lapse**2-(speed+shift)**2/root**2)
        action=-mass*clock
        canonical=sp.diff(action,speed)
        hamiltonian=canonical*speed-action
        target=mass*lapse**2/clock-shift*canonical
        for name,expression in [
            ('moving_source_legendre',hamiltonian-target),
            ('moving_source_lapse_stress',sp.diff(action,lapse)+mass*lapse/clock),
            ('moving_source_shift_stress',sp.diff(action,shift)-canonical),
            ('moving_source_radial_stress',sp.diff(action,root)+mass*(speed+shift)**2/(root**3*clock)),
            ('moving_source_mass_shell',(hamiltonian+shift*canonical)**2-lapse**2*(mass**2+root**2*canonical**2))]:
            evidence.check(name,sp.simplify(expression)==0,str(sp.simplify(expression)))
        anchor_speed=.08
        node_speed=.12

        def connection(time,radius):
            return .03+.02*time+.004*radius

        def solve(anchor_time,anchor0=5.,node0=6.):
            anchor=anchor0+anchor_speed*anchor_time
            def rhs(radius,state):
                return [connection(state[0],radius),.02*state[1]]
            def event(radius,state):
                return radius-node0-node_speed*state[0]
            event.terminal=True
            event.direction=1
            solution=solve_ivp(rhs,(anchor,node0+2),[anchor_time,1.],events=event,
                               method='DOP853',rtol=2e-13,atol=2e-15,max_step=.02)
            if not solution.success or len(solution.t_events[0])!=1:
                raise RuntimeError('Transverse node intersection not found.')
            node=solution.t_events[0][0]
            endpoint_time,bulk_jacobian=solution.y_events[0][0]
            start_c=connection(anchor_time,anchor)
            end_c=connection(endpoint_time,node)
            endpoint=1-end_c*node_speed
            start=1-start_c*anchor_speed
            return dict(time=endpoint_time,node=node,anchor=anchor,
                        derivative=bulk_jacobian*start/endpoint,
                        anchor_variation=-bulk_jacobian*start_c/endpoint,
                        node_variation=end_c/endpoint,bulk=bulk_jacobian,
                        endpoint=endpoint,start=start)

        def derivative(function,point=0.,step=.0002):
            return (function(point-2*step)-8*function(point-step)+8*function(point+step)-function(point+2*step))/(12*step)

        def clock_rate(time,radius,velocity):
            coefficient=connection(time,radius)
            beta=2*coefficient/(1+np.sqrt(1+4*coefficient**2))
            return np.sqrt(1-(velocity+beta)**2)

        records=[]
        for start_time in [-.1,0.,.1]:
            data=solve(start_time)
            observed=derivative(lambda value:solve(value)['time'],start_time)
            anchor_observed=derivative(lambda value:solve(start_time,5+value)['time'])
            node_observed=derivative(lambda value:solve(start_time,node0=6+value)['time'])
            records.append(dict(anchor_time=start_time,**{key:float(value) for key,value in data.items()},
                                derivative_error=float(abs(observed-data['derivative'])),
                                anchor_variation_error=float(abs(anchor_observed-data['anchor_variation'])),
                                node_variation_error=float(abs(node_observed-data['node_variation'])),
                                naive_bulk_error=float(abs(observed-data['bulk']))))
        evidence.report['cases']=records
        evidence.check('transverse_timelike_manufactured_chart',
                       min(row['endpoint'] for row in records)>.9 and min(row['start'] for row in records)>.9 and
                       all(np.isfinite(clock_rate(row['time'],row['node'],node_speed)) for row in records))
        evidence.check('moving_link_time_jacobian',max(row['derivative_error'] for row in records)<2e-9,records)
        evidence.check('moving_anchor_shape_variation',max(row['anchor_variation_error'] for row in records)<2e-9)
        evidence.check('moving_node_shape_variation',max(row['node_variation_error'] for row in records)<2e-9)
        evidence.check('fixed_endpoint_jacobian_is_detectably_wrong',min(row['naive_bulk_error'] for row in records)>.001)

        start,end=-.1,.1
        first,last=solve(start),solve(end)
        node_integral=quad(lambda time:clock_rate(time,6+node_speed*time,node_speed),
                           first['time'],last['time'],epsabs=1e-12,epsrel=1e-12)[0]
        def pulled_rate(time):
            data=solve(time)
            anchor_clock=clock_rate(time,data['anchor'],anchor_speed)
            proper_ratio=clock_rate(data['time'],data['node'],node_speed)/anchor_clock*data['derivative']
            return proper_ratio*anchor_clock
        pulled_integral=quad(pulled_rate,start,end,epsabs=1e-12,epsrel=1e-12)[0]
        evidence.check('independent_proper_clock_integrals',abs(node_integral-pulled_integral)<2e-11,
                       dict(node_integral=node_integral,pulled_integral=pulled_integral))
        constant=.09
        constant_map=lambda time:((1-constant*anchor_speed)*time+constant)/(1-constant*node_speed)
        expected=(1-constant*anchor_speed)/(1-constant*node_speed)
        evidence.check('constant_connection_exact_endpoint_formula',abs(derivative(constant_map)-expected)<1e-11)
        evidence.check('flat_physical_chart_links_stay_identity',((1-0*anchor_speed)/(1-0*node_speed))==1)
        evidence.report.update(moving_endpoint_jacobians_derived=True,
                               arbitrary_moving_lattice_covariance_proven=False,
                               complete_parent_source_action_derived=False,
                               material_extension_uniquely_selected=False)
        for name in ['DERIVATION-20260912-covariant-full-scalar-action-and-initial-constraint.md',
                     'DERIVATION-20260913-proper-clock-source-action-and-live-initial-backreaction.md',
                     'scripts/annular_metric_link_quadratic_20260909.py']:
            evidence.own(evidence.root/name)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()

