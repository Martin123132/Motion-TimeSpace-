import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from annular_reference_continuum_shell_20260914 import EvidenceRun


def run():
    evidence=EvidenceRun('annular-moving-material-pullback-attempt01',__file__)
    try:
        radius,lapse,root,length,coefficient=sp.symbols('R N U H C',positive=True)
        shift,velocity,connection,time_rate,coordinate_rate=sp.symbols('beta W c psi_t psi_xi',real=True)
        delta=1-shift**2/(lapse**2*root**2)
        original_c=shift/(lapse**2*root**2-shift**2)
        original_C=radius**2*lapse*root*delta
        eulerian=time_rate-velocity*coordinate_rate/length
        horizontal=connection*time_rate+(1-connection*velocity)*coordinate_rate/length
        transformed=length*radius**4*eulerian**2/(2*coefficient)-length*coefficient*horizontal**2/2
        ADM=length*radius**2*(time_rate-(velocity+shift)*coordinate_rate/length)**2/(2*lapse*root)-lapse*root*radius**2*coordinate_rate**2/(2*length)
        residual=sp.factor(transformed.subs({coefficient:original_C,connection:original_c})-ADM)
        evidence.check('exact_general_metric_material_pullback_equals_ADM',residual==0,str(residual))
        transverse=1-connection*velocity
        mapped_connection=connection*length/transverse
        mapped_C=coefficient*transverse**2/length
        mapped_spatial=-mapped_C*(coordinate_rate+mapped_connection*time_rate)**2/2
        evidence.check('horizontal_spatial_coefficient_and_connection',sp.simplify(mapped_spatial+length*coefficient*horizontal**2/2)==0)
        evidence.check('static_grid_exact_old_connection_and_coefficient',
                       sp.simplify(mapped_connection.subs(velocity,0)-connection*length)==0 and
                       sp.simplify(mapped_C.subs(velocity,0)-coefficient/length)==0)
        evidence.check('flat_physical_links_not_mesh_shift_links',mapped_connection.subs(connection,0)==0)
        wrong=mapped_spatial.subs(mapped_C,coefficient/length) if False else -coefficient*(coordinate_rate+mapped_connection*time_rate)**2/(2*length)
        evidence.check('omitted_transversality_weight_detectably_wrong',sp.simplify(wrong-mapped_spatial)!=0)
        dC,dc,dH,dV=sp.symbols('delta_C delta_c delta_H delta_W',real=True)
        mapped_c_variation=length*dc/transverse**2+connection*dH/transverse+connection**2*length*dV/transverse**2
        mapped_C_variation=transverse**2*dC/length-2*coefficient*transverse*(velocity*dc+connection*dV)/length-coefficient*transverse**2*dH/length**2
        evidence.check('material_connection_shape_derivative',
                       sp.simplify(mapped_c_variation-sum(sp.diff(mapped_connection,var)*step for var,step in
                                                        [(connection,dc),(length,dH),(velocity,dV)]))==0)
        evidence.check('material_spatial_weight_shape_derivative',
                       sp.simplify(mapped_C_variation-sum(sp.diff(mapped_C,var)*step for var,step in
                                                        [(coefficient,dC),(connection,dc),(length,dH),(velocity,dV)]))==0)

        anchor0,node0,anchor_speed,node_speed=5.,6.,.08,.12
        def cfun(time,position):
            return .03+.02*time+.004*position

        rows=[]
        for start in [-.1,0.,.1]:
            def physical_rhs(position,state):
                return [cfun(state[0],position),.02*state[1]]
            def event(position,state):
                return position-node0-node_speed*state[0]
            event.terminal=True
            event.direction=1
            physical=solve_ivp(physical_rhs,(anchor0+anchor_speed*start,8),[start,1],
                               events=event,method='DOP853',rtol=2e-13,atol=2e-15,max_step=.02)
            if not physical.success or len(physical.t_events[0])!=1:
                raise RuntimeError('Physical link failed.')
            end,bulk=physical.y_events[0][0]
            jacobian=bulk*(1-cfun(start,anchor0+anchor_speed*start)*anchor_speed)/(1-cfun(end,node0+node_speed*end)*node_speed)
            def material_rhs(coordinate,state):
                time=state[0]
                width=node0-anchor0+(node_speed-anchor_speed)*time
                motion=anchor_speed+coordinate*(node_speed-anchor_speed)
                position=anchor0+anchor_speed*time+coordinate*width
                local_c=cfun(time,position)
                c_rate=.02+.004*motion
                denominator=1-local_c*motion
                mapped=local_c*width/denominator
                derivative=width*c_rate/denominator**2+local_c*(node_speed-anchor_speed)/denominator
                return [mapped,derivative*state[1]]
            material=solve_ivp(material_rhs,(0,1),[start,1],method='DOP853',
                               rtol=2e-13,atol=2e-15,max_step=.02)
            if not material.success:
                raise RuntimeError('Material link failed.')
            row=dict(anchor_time=start,endpoint_time_error=float(abs(material.y[0,-1]-end)),
                     endpoint_jacobian_error=float(abs(material.y[1,-1]-jacobian)))
            rows.append(row)
        evidence.report['cases']=rows
        evidence.check('independent_material_and_physical_link_times',max(row['endpoint_time_error'] for row in rows)<2e-12,rows)
        evidence.check('independent_material_and_physical_clock_jacobians',max(row['endpoint_jacobian_error'] for row in rows)<2e-12)

        wall_speed,gradient=sp.symbols('V grad',real=True)
        wall_time=-wall_speed*gradient
        shape_force=radius**2*(gradient**2/2+wall_speed*wall_time*gradient+wall_time**2/2)
        pressure=(1-wall_speed**2)*gradient**2/2
        evidence.check('continuum_moving_Dirichlet_shape_force',sp.simplify(shape_force-radius**2*pressure)==0)
        field_work=radius**2*(wall_time*gradient+wall_speed*(wall_time**2+gradient**2)/2)
        evidence.check('continuum_wave_and_source_work_cancel',sp.simplify(field_work+wall_speed*radius**2*pressure)==0)
        evidence.report.update(exact_continuum_material_pullback_derived=True,
                               complete_finite_factor_moving_action_candidate_written=True,
                               finite_moving_covariance_uniqueness_proven=False,
                               curved_moving_finite_collar_evolution_completed=False,
                               full_GR_limit_proven=False,valid_for_physics_claim=False)
        for name in ['scripts/annular_covariant_scalar_action_20260912.py',
                     'scripts/annular_moving_collar_action_20260914.py',
                     'scripts/derive_annular_moving_link_clock_20260914.py']:
            evidence.own(evidence.root/name)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()

