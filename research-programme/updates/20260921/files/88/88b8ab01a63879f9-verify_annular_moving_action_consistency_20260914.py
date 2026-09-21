import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()
import numpy as np
from scipy.integrate import quad
from annular_moving_collar_sparse_20260914 import SparseMovingCollarAction
from annular_compatible_current_restoring_20260909 import unit_gram_template
from annular_reference_continuum_shell_20260914 import EvidenceRun


def history(coordinate):
    base=coordinate*(1-coordinate)
    harmonic=1+.1*np.cos(2*np.pi*coordinate)
    value=base*harmonic
    gradient=(1-2*coordinate)*harmonic-.2*np.pi*base*np.sin(2*np.pi*coordinate)
    return value,.1*value,gradient


def continuum_integrands(coordinate):
    value,rate,gradient=history(coordinate)
    length,velocity=3.,.1
    length_shape,velocity_shape=.1,.03
    radius=3+length*coordinate
    eulerian=rate-velocity*coordinate*gradient/length
    eulerian_shape=-coordinate*gradient*(velocity_shape/length-velocity*length_shape/length**2)
    mass=length*radius**2
    mass_shape=length_shape*radius**2+2*length*radius*coordinate*length_shape
    coefficient=radius**2/length
    coefficient_shape=2*radius*coordinate*length_shape/length-radius**2*length_shape/length**2
    action=mass*eulerian**2/2-coefficient*gradient**2/2
    variation=mass_shape*eulerian**2/2+mass*eulerian*eulerian_shape-coefficient_shape*gradient**2/2
    return action,variation


def main():
    evidence=EvidenceRun('annular-moving-action-consistency-attempt01',__file__)
    try:
        continuum=np.array([quad(lambda coordinate:continuum_integrands(coordinate)[index],0,1,
                                  epsabs=2e-13,epsrel=2e-13)[0] for index in [0,1]])
        continuum+=np.array([-.003*np.sqrt(1-.1**2),.003*.1*.03/np.sqrt(1-.1**2)])
        for count in [17,33,65,129,257,513]:
            actions=[]
            variations=[]
            for gram in [False,True]:
                system=SparseMovingCollarAction(count,gram)
                scalar,rate,gradient=history(system.coordinate[:-1])
                scalar=scalar[None,:]
                rate=rate[None,:]
                action=system.lagrangian(scalar,rate,np.array([6.]),np.array([.1]))
                varied=system.lagrangian(scalar,rate,np.array([6.+1e-25j*.1]),np.array([.1+1e-25j*.03]))
                actions.append(float(action))
                variations.append(float(np.imag(varied)/1e-25))
            margin,adjacent,extras=unit_gram_template(count)
            bound=(np.sum(margin)+4*np.sum(abs(adjacent))+4*sum(abs(weight) for first,second,weight in extras))/(count-1)
            row=dict(count=count,reference_action_error=abs(actions[0]-continuum[0]),
                     reference_variation_error=abs(variations[0]-continuum[1]),
                     gram_action_difference=abs(actions[1]-actions[0]),
                     gram_variation_difference=abs(variations[1]-variations[0]),
                     gram_uniform_constant=float(bound))
            evidence.report['cases'].append(row)
            evidence.check(str(count)+'_full_factor_uniform_bound',bound<5 and np.all(margin>0),row)
        rows=evidence.report['cases']
        for key,lower in [('reference_action_error',1.8),('reference_variation_error',1.8),
                          ('gram_action_difference',3.5),('gram_variation_difference',3.5)]:
            orders=[float(np.log2(rows[index-1][key]/rows[index][key])) for index in [-2,-1]]
            evidence.check(key+'_declared_asymptotic_order',min(orders)>lower,orders)
        evidence.report.update(scope='Smooth-history action and first shape variation consistency only; not solution convergence.',
                               continuum_action_and_first_variation=continuum.tolist(),
                               uniform_moving_solution_stability_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

