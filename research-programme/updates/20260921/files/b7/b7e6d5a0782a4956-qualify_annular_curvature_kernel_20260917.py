from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_finite_width_curvature_20260917 import source_curvature_kernel
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow, band_product
from scipy.linalg import solve_banded
import argparse
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label, __file__)
    try:
        evidence.report.update(original_action_unchanged=True, finite_future_trajectories_read=False,
            force_fit=False, force_correction=False, interval_arithmetic=False,
            prescribed_flat_background_only=True, continuum_regularities_established=False,
            endpoint_Taylor_truncation_used=False, floating_slope_moments_retained=True)
        systems = {}
        evidence.report['manufactured_cases'] = []
        for count in [33,257,513,1025,2049]:
            system = LocallyRefinedSourceAction(count,True,background_mass=0.,source_splits=8)
            rows, columns, kernel = source_curvature_kernel(system)
            offsets = kernel.offsets
            coefficients = np.array([[.7,-.2,.4,-.3,.1],[1.1,.3,-.6,.2,-.15]])
            values = np.zeros_like(offsets)
            for side, selection in enumerate([offsets<0.,offsets>0.]):
                for power in range(1,6):
                    values[selection] += coefficients[side,power-1]*offsets[selection]**power
            integrated = kernel.moments @ coefficients[:,0]
            for side in range(2):
                points, weights = kernel.quadrature(side,8)
                curvature = sum(power*(power-1)*coefficients[side,power-1]*points**(power-2) for power in range(2,6))
                integrated += weights @ curvature
            polynomial_error = float(max(abs(kernel.coefficients @ values-integrated)))
            evidence.check(str(count)+'_independent_quintic_curvature_identity',polynomial_error<3e-14,polynomial_error)
            frequency = 21/system.gram_spacing
            slopes, amplitudes = np.array([.7,1.1]),np.array([.8,-.6])
            selection = offsets>0.
            values = slopes[selection.astype(int)]*offsets+amplitudes[selection.astype(int)]*2*np.sin(frequency*offsets/2)**2/frequency**2
            integrated = kernel.moments @ slopes
            for side in range(2):
                points,weights = kernel.quadrature(side,96)
                integrated += weights @ (amplitudes[side]*np.cos(frequency*points))
            oscillatory_error = float(max(abs(kernel.coefficients @ values-integrated)))
            evidence.check(str(count)+'_independent_oscillatory_curvature_identity',oscillatory_error<3e-14,oscillatory_error)
            absolute = kernel.absolute_integrals()
            bound = abs(kernel.moments) @ abs(slopes)+absolute @ abs(amplitudes)
            evidence.check(str(count)+'_absolute_kernel_integral_bound',np.all(abs(integrated)<=bound+3e-14))
            evidence.report['manufactured_cases'].append(dict(count=count,rows=len(rows),
                polynomial_error=polynomial_error,oscillatory_error=oscillatory_error,
                maximum_slope_moment=float(np.max(abs(kernel.moments))),
                scaled_kernel_L1_maximum=float(max(np.sum(absolute,axis=1))/system.gram_spacing**2)))
            if count in [257,513,1025]:
                systems[count] = (system,rows,columns,kernel)
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        labels = ['annular-dense-GR-references-attempt01','annular-GR-projection-residual-attempt02','annular-source-trace-refinement-attempt03']
        statuses = {}
        for label in labels:
            path = intake/label/'status.json'
            evidence.own(path)
            statuses[label] = json.loads(path.read_text())
            evidence.check(label+'_complete',statuses[label]['state']=='complete')

        def read(label,name):
            path = intake/label/name
            evidence.own(path)
            if hashlib.sha256(path.read_bytes()).hexdigest()!=statuses[label]['outputs'][str(path.relative_to(evidence.root))]:
                raise RuntimeError('Source changed: '+str(path))
            with np.load(path,allow_pickle=False) as saved:
                return {key:saved[key].copy() for key in saved.files}

        for degree in [512,768]:
            oracle = TwoSidedGRCharacteristics(degree,mass=0.,source=.03)
            saved = read(labels[0],'oracle-'+str(degree)+'.npz')
            times,states = saved['times'],saved['states']
            lengths = np.array([.83,.77])
            curvature_coefficients,slopes = [],[]
            for state in states:
                fields,position,momentum,speed = oracle.unpack(state)
                coefficients = ((fields[:,0]-fields[:,1])/2) @ oracle.inverse.T
                jacobians = np.array([position-oracle.inner,oracle.outer-position])/lengths
                curvature_coefficients.append([jacobians[side]*2/lengths[side]*np.polynomial.chebyshev.chebder(coefficients[side]) for side in range(2)])
                slopes.append([jacobians[side]*np.polynomial.chebyshev.chebval([1.,-1.][side],coefficients[side]) for side in range(2)])
            curvature_coefficients,slopes = np.array(curvature_coefficients),np.array(slopes)
            for count,(system,rows,columns,kernel) in systems.items():
                prefix = str(degree)+'_'+str(count)
                projection = read(labels[1],'projection-'+str(degree)+'-'+str(count)+'.npz')
                earlier = read(labels[2],'trace-'+str(degree)+'-'+str(count)+'.npz')
                evidence.check(prefix+'_matching_reference_samples',np.array_equal(times,projection['times'])
                    and np.array_equal(times,earlier['times']) and np.array_equal(rows,earlier['source_rows']))
                predictions = {}
                for order in [16,32,64,degree//2+1,degree//2+9]:
                    maps = kernel.chebyshev_maps(degree,lengths,order)
                    predictions[order] = np.einsum('tsk,rsk->tr',curvature_coefficients,maps)+slopes @ kernel.moments.T
                actual = earlier['actual_source_factor']
                factor = predictions[degree//2+1]
                factor_error = float(np.max(abs(factor-actual)))
                control = float(np.max(abs(factor-predictions[degree//2+9])))
                evidence.check(prefix+'_full_width_factor_identity',factor_error<3e-14,factor_error)
                evidence.check(prefix+'_independent_quadrature_control',control<3e-14,control)
                model = FlatPreassembledFlow(system)
                predicted_force,force_difference_bound = [],[]
                for index,state in enumerate(projection['states']):
                    field,position,speed = state[:system.count],state[system.count],state[-2]
                    matrices = model.matrices(position)
                    cross = band_product(matrices['transport'],field)
                    inverse = solve_banded((2,2),matrices['mass'],cross,check_finite=False)
                    inertia = system.source_mass/(1-speed**2)**1.5
                    schur = inertia+field @ band_product(matrices['square'],field)-cross @ inverse
                    weight = (system.lifted @ inverse)[rows]
                    diagonal,diagonal_b = matrices['gram'][rows],matrices['gram_b'][rows]
                    candidate = factor[index]
                    predicted_force.append(inertia/schur*(weight @ (diagonal*candidate)-candidate @ (diagonal_b*candidate)/2))
                    remainder = np.linalg.norm(candidate-actual[index])
                    force_difference_bound.append(inertia/schur*(np.linalg.norm(diagonal*weight-diagonal_b*actual[index])*remainder
                        +max(abs(diagonal_b))*remainder**2/2))
                predicted_force,force_difference_bound = np.array(predicted_force),np.array(force_difference_bound)
                error = abs(predicted_force-earlier['source_Gram_force'])
                evidence.check(prefix+'_source_force_identity',max(error)<2e-11,float(max(error)))
                evidence.check(prefix+'_force_error_bound',np.all(error<=force_difference_bound+3e-14))
                maximum_curvature = np.sum(abs(curvature_coefficients),axis=2)
                absolute_bound = maximum_curvature @ kernel.absolute_integrals().T+abs(slopes) @ abs(kernel.moments).T
                evidence.check(prefix+'_C2_curvature_only_bound',np.all(abs(actual)<=absolute_bound+3e-14))
                row = dict(degree=degree,count=count,maximum_factor_error=factor_error,
                    maximum_quadrature_control=control,maximum_source_force_error=float(max(error)),
                    actual_source_force_at_021=float(earlier['source_Gram_force'][42]),
                    kernel_source_force_at_021=float(predicted_force[42]),
                    failed_endpoint_source_force_at_021=float(earlier['quadratic_Gram_force'][42]),
                    maximum_actual_factor=float(np.max(abs(actual))),
                    maximum_curvature_bound=float(np.max(absolute_bound)),
                    lower_order_quadrature_errors={str(order):float(np.max(abs(predictions[order]-factor))) for order in [16,32,64]},
                    full_GR_gate_upgraded=False)
                evidence.report['cases'].append(row)
                destination = evidence.output/('kernel-'+str(degree)+'-'+str(count)+'.npz')
                np.savez_compressed(destination,times=times,source_rows=rows,nodal_columns=columns,
                    offsets=kernel.offsets,row_coefficients=kernel.coefficients,slope_moments=kernel.moments,
                    kernel_absolute_integrals=kernel.absolute_integrals(),curvature_coefficients=curvature_coefficients,
                    slope_contribution=slopes @ kernel.moments.T,actual_factor=actual,kernel_factor=factor,
                    quadrature_control=predictions[degree//2+9],source_force=predicted_force,
                    actual_source_force=earlier['source_Gram_force'],force_error_bound=force_difference_bound,
                    curvature_bound=absolute_bound)
                evidence.own(destination,'outputs')
                evidence.save()
                print(row,flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
