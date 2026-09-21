import numpy as np
from scipy.integrate import quad_vec

from annular_compatible_h_evolution_20260914 import gram_energy_triplet
from annular_finite_width_bulk_current_20260913 import shape_weight


def adaptive_energy_integral(system,solution,duration,tolerance=1e-11):
    def integrand(time):
        triplet=gram_energy_triplet(system,system.geometry(time,solution.sol(time)))
        return np.array([triplet[2],np.sqrt(max(0.,triplet[1]))])
    value,error,info=quad_vec(integrand,0.,duration,epsabs=tolerance,epsrel=tolerance,limit=256,full_output=True)
    if not info.success:
        raise RuntimeError('Adaptive energy quadrature failed: '+info.message)
    return value,float(error),int(info.neval)


def velocity_commutator(system,geometry,order=24):
    points,weights=np.polynomial.legendre.leggauss(order)
    offsets=np.concatenate([-.25+.25*points,.25+.25*points])
    weights=np.concatenate([.25*weights,.25*weights])*shape_weight(offsets,system.shape)
    data=geometry.layer(offsets)
    coefficient=data['N']*data['U']/data['R']**2
    momentum=data['p']
    coefficient_differences=[np.diff(coefficient,n=index,axis=1) for index in range(4)]
    momentum_differences=[np.diff(momentum,n=index,axis=1) for index in range(4)]
    terms=np.stack([
        coefficient[:,3:]*momentum_differences[3],
        3*coefficient_differences[1][:,2:]*momentum_differences[2][:,:-1],
        3*coefficient_differences[2][:,1:]*momentum_differences[1][:,:-2],
        coefficient_differences[3]*momentum[:,:-3]])
    actual=np.diff(data['q'],n=3,axis=1)
    term_norms=np.sqrt(np.sum(terms**2,axis=2)*system.spacing)/system.spacing**3
    combined=np.sqrt(weights @ np.sum(term_norms,axis=0)**2)
    discrete_third_norm=np.sqrt(weights @ np.sum(actual**2,axis=1)*system.spacing)/system.spacing**3
    term_global_norms=np.sqrt(term_norms**2 @ weights)
    rate_energy=gram_energy_triplet(system,geometry,order)[1]
    return {'product_identity_error':float(abs(actual-terms.sum(axis=0)).max()),
            'q_equals_coefficient_times_p_error':float(abs(data['q']-coefficient*momentum).max()),
            'local_product_bound':float(combined),'discrete_velocity_third_norm':float(discrete_third_norm),
            'component_norms':term_global_norms.tolist(),
            'coefficient_third_sup':float(abs(coefficient_differences[3]).max()/system.spacing**3),
            'rate_sqrt_over_h2':float(np.sqrt(rate_energy)/system.spacing**2),
            'rate_sqrt_over_h2_bound':float(6.1*combined/4)}
