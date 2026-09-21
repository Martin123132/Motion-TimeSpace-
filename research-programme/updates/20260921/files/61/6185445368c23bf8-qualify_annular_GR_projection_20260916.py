from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_GR_projection_20260916 import GRProjection, manufactured
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
import argparse
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label,__file__)
    try:
        evidence.report.update(flat_prescribed_background_only=True,finite_trajectories_read=False,
            source_trace_constant_fixed_by_Dirichlet=True,kinematic_projection_defect_not_discarded=True)
        folder = evidence.root/'source-intake/navier-stokes/20260914/annular-dense-GR-references-attempt01'
        path = folder/'status.json'
        evidence.own(path)
        status = json.loads(path.read_text())
        evidence.check('independent_reference_complete',status['state']=='complete' and all(row['passed'] for row in status['checks']))
        for degree in [384,512,768]:
            oracle = TwoSidedGRCharacteristics(degree,mass=0.,source=.03)
            path = folder/('oracle-'+str(degree)+'.npz')
            evidence.own(path)
            with np.load(path,allow_pickle=False) as saved:
                times,states = saved['times'].copy(),saved['states'].copy()
            for count in [257,513,1025]:
                system = LocallyRefinedSourceAction(count,True,background_mass=0.,source_splits=8)
                projection = GRProjection(oracle,system)
                prefix = str(degree)+'-'+str(count)
                position,speed,acceleration = 6.041,.061,.007
                seed = manufactured(oracle,position,speed)
                tangent = manufactured(oracle,position+1e-25j*speed,speed+1e-25j*acceleration,
                    1e-25j*np.sqrt(1-speed**2)).imag/1e-25
                projected,derivative = projection.reconstruct(seed,tangent)
                coordinate = projection.coordinate
                polynomial = np.where(projection.left,coordinate**2-1,2*coordinate-coordinate**2)
                lengths = np.where(projection.left,position-oracle.inner,oracle.outer-position)
                signs = np.where(projection.left,1.,-1.)
                exact = np.concatenate([lengths*polynomial,[position],signs*speed*polynomial,[speed,0.]])
                exact_rate = np.concatenate([signs*speed*polynomial,[speed],signs*acceleration*polynomial,
                    [acceleration,np.sqrt(1-speed**2)]])
                polynomial_error = float(np.max(abs(projected-exact)))
                derivative_error = float(np.max(abs(derivative-exact_rate)))
                evidence.check(prefix+'_moving_polynomial_state',polynomial_error<2e-12,polynomial_error)
                evidence.check(prefix+'_moving_polynomial_derivative',derivative_error<2e-12,derivative_error)
                complex_errors,central_errors,sampling_errors,primitive_errors,boundary_errors = [],[],[],[],[]
                selected_indices = [0,37,42,80]
                for index in selected_indices:
                    state = states[index]
                    tangent = oracle.rhs(times[index],state)
                    projected,derivative = projection.reconstruct(state,tangent)
                    complex_rate = projection.reconstruct(state.astype(complex)+1e-25j*tangent).imag/1e-25
                    complex_errors.append(float(np.max(abs(complex_rate-derivative))))
                    central = (projection.reconstruct(state+1e-6*tangent)-projection.reconstruct(state-1e-6*tangent))/2e-6
                    central_errors.append(float(np.max(abs(central-derivative))))
                    radius,unused,displacement = system.mapping(system.radii,state[-3])
                    temporal,gradient = oracle.sample(state,radius)
                    sampling_errors.append(float(np.max(abs(projected[system.count+1:-2]-temporal-projected[-2]*displacement*gradient))))
                    fields,position,momentum,speed = oracle.unpack(state)
                    boundary_errors.append(float(max(abs((fields[0,0,-1]+fields[0,1,-1])/2+speed*(fields[0,0,-1]-fields[0,1,-1])/2),
                        abs((fields[1,0,0]+fields[1,1,0])/2+speed*(fields[1,0,0]-fields[1,1,0])/2))))
                    points,weights = np.polynomial.legendre.leggauss((degree+2)//2)
                    for node in [0,system.count//4,system.count//2,3*system.count//4,system.count-1]:
                        lower,upper = position,radius[node]
                        probes = (lower+upper)/2+(upper-lower)/2*points
                        unused,gradient = oracle.sample(state,probes)
                        integral = (upper-lower)/2*(weights @ gradient)
                        primitive_errors.append(float(abs(integral-projected[node])))
                evidence.check(prefix+'_whole_projection_complex_derivative',max(complex_errors)<2e-11,max(complex_errors))
                evidence.check(prefix+'_central_directional_derivative',max(central_errors)<2e-8,max(central_errors))
                evidence.check(prefix+'_independent_physical_sampling',max(sampling_errors)<2e-12,max(sampling_errors))
                evidence.check(prefix+'_independent_primitive_quadrature',max(primitive_errors)<2e-12,max(primitive_errors))
                evidence.check(prefix+'_moving_Dirichlet_constraint',max(boundary_errors)<2e-12,max(boundary_errors))
                row = dict(degree=degree,count=count,splits=8,polynomial_error=polynomial_error,
                    polynomial_derivative_error=derivative_error,complex_derivative_error=max(complex_errors),
                    central_derivative_error=max(central_errors),sampling_error=max(sampling_errors),primitive_error=max(primitive_errors))
                evidence.report['cases'].append(row)
                evidence.save()
                print(row,flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
