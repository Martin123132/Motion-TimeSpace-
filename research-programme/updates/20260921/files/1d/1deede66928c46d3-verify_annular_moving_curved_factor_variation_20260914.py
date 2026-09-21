import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from annular_covariant_scalar_action_20260912 import full_spatial_factors
from annular_reference_continuum_shell_20260914 import EvidenceRun


def evaluators():
    time,coordinate,parameter=sp.symbols('t xi epsilon',real=True)
    length=3+sp.Rational(1,20)*time+sp.Rational(1,100)*sp.sin(time)+parameter*sp.Rational(1,50)*sp.cos(sp.Rational(13,10)*time)
    velocity=sp.diff(length,time)
    radius=3+length*coordinate
    lapse=1+sp.Rational(1,50)*time+sp.Rational(3,200)*(radius-5)
    root=sp.Rational(9,10)+sp.Rational(1,200)*sp.sin(time+sp.Rational(3,10)*radius)
    shift=sp.Rational(3,50)+sp.Rational(1,100)*time+sp.Rational(1,250)*(radius-5)
    physical_c=shift/(lapse**2*root**2-shift**2)
    coefficient=radius**2*lapse*root*(1-shift**2/(lapse**2*root**2))
    motion=coordinate*velocity
    transverse=1-physical_c*motion
    mapped_c=physical_c*length/transverse
    mapped_C=coefficient*transverse**2/length
    kinetic=length*radius**4/coefficient
    transport=motion/length
    proper=sp.sqrt(lapse**2-(velocity+shift)**2/root**2)
    expressions=[mapped_c,sp.diff(mapped_c,time),sp.diff(mapped_c,parameter),
                 sp.diff(mapped_c,time,2),sp.diff(mapped_c,time,parameter),
                 mapped_C,sp.diff(mapped_C,time),sp.diff(mapped_C,parameter),
                 kinetic,sp.diff(kinetic,parameter),transport,sp.diff(transport,parameter),
                 proper,sp.diff(proper,parameter),transverse]
    return sp.lambdify((time,coordinate,parameter),expressions,modules='numpy',cse=True,docstring_limit=0)


def field(time,coordinate):
    shape=coordinate*(1-coordinate)
    return shape*(1+.1*np.sin(time)+.1*np.cos(2*np.pi*coordinate)),.1*shape*np.cos(time)


def action(gram,parameter,evaluate,order=8):
    count=17
    coordinate=np.linspace(0,1,count)
    spacing=1/(count-1)
    norm=np.full(count,spacing)
    norm[[0,-1]]/=2
    factors,sampling=full_spatial_factors(count,gram)
    base,base_sampling=full_spatial_factors(count,False)
    derivative=base_sampling.T @ base/norm[:,None]
    factor_indices,node_indices=np.nonzero((factors!=0)|(sampling!=0))
    anchors=(sampling @ coordinate)[factor_indices]
    endpoints=coordinate[node_indices]
    distances=endpoints-anchors
    factor_weights=factors[factor_indices,node_indices]
    sample_weights=sampling[factor_indices,node_indices]
    link_count=len(anchors)
    quadrature,weights=np.polynomial.legendre.leggauss(order)
    times=.1*quadrature
    weights=.1*weights
    total=0.
    total_derivative=0.
    dropped_transport_derivative=0.
    minimum_transverse=1.
    minimum_jacobian=1.
    for start,weight in zip(times,weights):
        initial=np.concatenate([np.full(link_count,start),np.ones(link_count),np.zeros(2*link_count)])
        def rhs(fraction,state):
            linked,jacobian,variation,mixed=state.reshape(4,link_count)
            location=anchors+fraction*distances
            values=evaluate(linked,location,parameter)
            coefficient,first,shape,second,mixed_shape=values[:5]
            return np.concatenate([distances*coefficient,
                                   distances*first*jacobian,
                                   distances*(first*variation+shape),
                                   distances*((second*variation+mixed_shape)*jacobian+first*mixed)])
        solution=solve_ivp(rhs,(0,1),initial,method='DOP853',rtol=2e-12,atol=2e-14,max_step=.1)
        if not solution.success:
            raise RuntimeError(solution.message)
        linked,jacobian,variation,mixed=solution.y[:,-1].reshape(4,link_count)
        values=evaluate(linked,endpoints,parameter)
        coefficient,coefficient_time,coefficient_shape=values[5:8]
        trace,trace_time=field(linked,endpoints)
        amplitudes=np.bincount(factor_indices,weights=factor_weights*trace,minlength=len(factors))
        amplitude_variation=np.bincount(factor_indices,weights=factor_weights*trace_time*variation,minlength=len(factors))
        dual=np.bincount(factor_indices,weights=sample_weights*jacobian*coefficient,minlength=len(factors))
        dual_variation=np.bincount(factor_indices,weights=sample_weights*(mixed*coefficient+jacobian*(coefficient_shape+coefficient_time*variation)),minlength=len(factors))
        spatial=-np.sum(amplitudes**2*dual)/(2*spacing)
        spatial_derivative=-np.sum(2*amplitudes*amplitude_variation*dual+amplitudes**2*dual_variation)/(2*spacing)
        dropped=-np.sum(amplitudes**2*np.bincount(factor_indices,weights=sample_weights*jacobian*coefficient_shape,minlength=len(factors)))/(2*spacing)
        node_values=evaluate(start,coordinate,parameter)
        kinetic,kinetic_shape,transport,transport_shape=node_values[8:12]
        nodal,nodal_time=field(start,coordinate)
        nodal_gradient=derivative @ nodal
        eulerian=nodal_time-transport*nodal_gradient
        scalar_kinetic=np.sum(norm*kinetic*eulerian**2)/2
        scalar_kinetic_derivative=np.sum(norm*(kinetic_shape*eulerian**2/2-kinetic*eulerian*transport_shape*nodal_gradient))
        source=-.003*node_values[12][-1]
        source_derivative=-.003*node_values[13][-1]
        total+=weight*(spatial+scalar_kinetic+source)
        total_derivative+=weight*(spatial_derivative+scalar_kinetic_derivative+source_derivative)
        dropped_transport_derivative+=weight*(dropped+scalar_kinetic_derivative+source_derivative)
        minimum_transverse=min(minimum_transverse,float(np.min(values[-1])))
        minimum_jacobian=min(minimum_jacobian,float(np.min(jacobian)))
    return dict(action=float(total),derivative=float(total_derivative),
                frozen_link_derivative=float(dropped_transport_derivative),
                minimum_transverse=minimum_transverse,minimum_jacobian=minimum_jacobian)


def main():
    evidence=EvidenceRun('annular-moving-curved-factor-variation-attempt01',__file__)
    try:
        evaluate=evaluators()
        for gram in [False,True]:
            baseline=action(gram,0.,evaluate)
            step=.002
            samples={multiple:action(gram,multiple*step,evaluate)['action'] for multiple in [-2,-1,1,2]}
            difference=(samples[-2]-8*samples[-1]+8*samples[1]-samples[2])/(12*step)
            fine=action(gram,0.,evaluate,order=12)
            result=dict(branch='MTS' if gram else 'reference',**baseline,
                        independent_shape_derivative=difference,
                        derivative_error=abs(difference-baseline['derivative']),
                        frozen_link_error=abs(difference-baseline['frozen_link_derivative']),
                        quadrature_action_error=abs(fine['action']-baseline['action']),
                        quadrature_derivative_error=abs(fine['derivative']-baseline['derivative']))
            evidence.report['cases'].append(result)
            evidence.check(result['branch']+'_full_curved_action_shape_variation',result['derivative_error']<2e-10,result)
            evidence.check(result['branch']+'_omitting_link_motion_is_detected',result['frozen_link_error']>1e-8)
            evidence.check(result['branch']+'_temporal_quadrature_control',max(result['quadrature_action_error'],result['quadrature_derivative_error'])<2e-11)
            evidence.check(result['branch']+'_regular_link_chart',result['minimum_transverse']>.9 and result['minimum_jacobian']>.9)
        evidence.report.update(manufactured_curved_history_action_variation_checked=True,
                               coupled_curved_finite_collar_evolution_completed=False,
                               finite_moving_covariance_uniqueness_proven=False,
                               full_GR_limit_proven=False,valid_for_physics_claim=False)
        for name in ['scripts/derive_annular_moving_material_pullback_20260914.py',
                     'DERIVATION-20260912-covariant-full-scalar-action-and-initial-constraint.md']:
            evidence.own(evidence.root/name)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

