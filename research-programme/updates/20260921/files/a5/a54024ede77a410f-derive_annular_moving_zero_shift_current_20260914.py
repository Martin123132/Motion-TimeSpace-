import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()
import numpy as np
import sympy as sp
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_covariant_scalar_action_20260912 import full_spatial_factors
from verify_annular_moving_curved_factor_variation_20260914 import action,field


def setup():
    time,coordinate,parameter=sp.symbols('t xi epsilon',real=True)
    length=3+sp.Rational(1,20)*time+sp.Rational(1,100)*sp.sin(time)
    velocity=sp.diff(length,time)
    radius=3+length*coordinate
    lapse=1+sp.Rational(1,50)*time+sp.Rational(3,200)*(radius-5)
    root=sp.Rational(9,10)+sp.Rational(1,200)*sp.sin(time+sp.Rational(3,10)*radius)
    profile=sp.Rational(1,50)*sp.cos(sp.Rational(2,5)*time)*(1+sp.Rational(1,10)*(radius-3))
    shift=parameter*profile
    connection=shift/(lapse**2*root**2-shift**2)
    coefficient=radius**2*lapse*root*(1-shift**2/(lapse**2*root**2))
    motion=coordinate*velocity
    transverse=1-connection*motion
    mapped=connection*length/transverse
    spatial=coefficient*transverse**2/length
    kinetic=length*radius**4/coefficient
    transport=motion/length
    proper=sp.sqrt(lapse**2-(velocity+shift)**2/root**2)
    expressions=[mapped,sp.diff(mapped,time),sp.diff(mapped,parameter),
                 sp.diff(mapped,time,2),sp.diff(mapped,time,parameter),
                 spatial,sp.diff(spatial,time),sp.diff(spatial,parameter),
                 kinetic,sp.diff(kinetic,parameter),transport,sp.diff(transport,parameter),
                 proper,sp.diff(proper,parameter),transverse]
    evaluate=sp.lambdify((time,coordinate,parameter),expressions,modules='numpy',cse=True,docstring_limit=0)
    zero=sp.lambdify((time,coordinate),[length,velocity,radius,lapse,root,profile],modules='numpy',cse=True)
    return evaluate,zero


def adjoint(gram,geometry,order=12):
    count=17
    coordinate=np.linspace(0,1,count)
    spacing=1/(count-1)
    factors,sampling=full_spatial_factors(count,gram)
    factor_indices,node_indices=np.nonzero((factors!=0)|(sampling!=0))
    endpoints=coordinate[node_indices]
    anchors=(sampling @ coordinate)[factor_indices]
    distances=endpoints-anchors
    factor_weights=factors[factor_indices,node_indices]
    sample_weights=sampling[factor_indices,node_indices]
    quadrature,weights=np.polynomial.legendre.leggauss(order)
    fraction=(quadrature+1)/2
    fraction_weights=weights/2

    def slice_data(time):
        length,velocity,radius,lapse,root,profile=geometry(time,coordinate)
        motion=coordinate*velocity
        coefficient=radius**2*lapse*root/length
        scalar,rate=field(time,coordinate)
        amplitudes=factors @ scalar
        amplitude_rate=factors @ rate
        dual=sampling @ coefficient
        transported=anchors[:,None]+distances[:,None]*fraction
        along=geometry(time,transported)
        link_variation=distances*np.sum(fraction_weights*along[0]*along[5]/(along[3]**2*along[4]**2),axis=1)
        kernel=(amplitudes[factor_indices]*amplitude_rate[factor_indices]*sample_weights*coefficient[node_indices]-
                amplitudes[factor_indices]*dual[factor_indices]*factor_weights*rate[node_indices])/spacing
        transported_part=float(kernel @ link_variation)
        nodal_part=float(np.sum(amplitudes**2*(sampling @ (radius**2*motion*profile/(length*lapse*root))))/spacing)
        proper=np.sqrt(lapse[-1]**2-velocity**2/root[-1]**2)
        source=.003*velocity*profile[-1]/(root[-1]**2*proper)
        temporal=-float(np.sum(amplitudes[factor_indices]**2*sample_weights*coefficient[node_indices]*link_variation)/(2*spacing))
        return np.array([transported_part,nodal_part,source,temporal])

    integrated=sum(.1*weight*slice_data(.1*point) for point,weight in zip(quadrature,weights))
    boundary=slice_data(.1)[3]-slice_data(-.1)[3]
    return dict(transport=integrated[0],direct_node=integrated[1],source=integrated[2],boundary=boundary,
                total=float(sum(integrated[:3])+boundary))


def main():
    evidence=EvidenceRun('annular-moving-zero-shift-current-attempt01',__file__)
    try:
        evaluate,geometry=setup()
        for gram in [False,True]:
            tangent=action(gram,0.,evaluate)
            reduced=adjoint(gram,geometry)
            step=.002
            values={multiple:action(gram,multiple*step,evaluate)['action'] for multiple in [-2,-1,1,2]}
            difference=(values[-2]-8*values[-1]+8*values[1]-values[2])/(12*step)
            row=dict(branch='MTS' if gram else 'reference',**{name:float(value) for name,value in reduced.items()},
                     tangent_derivative=tangent['derivative'],independent_difference=difference,
                     adjoint_tangent_error=abs(reduced['total']-tangent['derivative']),
                     independent_error=abs(reduced['total']-difference))
            evidence.report['cases'].append(row)
            evidence.check(row['branch']+'_zero_shift_current_adjoint',row['adjoint_tangent_error']<2e-11,row)
            evidence.check(row['branch']+'_independent_full_action_shift_difference',row['independent_error']<2e-10)
            evidence.check(row['branch']+'_temporal_endpoint_term_is_nonzero',abs(row['boundary'])>1e-8)
            evidence.check(row['branch']+'_mesh_motion_direct_term_is_nonzero',abs(row['direct_node'])>1e-7)
        evidence.report.update(full_zero_shift_scalar_and_source_first_variation_derived=True,
                               gravity_constraint_assembled_or_solved=False,
                               full_GR_limit_proven=False,valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

