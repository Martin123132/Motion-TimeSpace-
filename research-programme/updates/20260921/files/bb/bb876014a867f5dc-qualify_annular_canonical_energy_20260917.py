from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_canonical_energy_20260917 import CanonicalEnergy
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from annular_GR_projection_20260916 import GRProjection
from scipy.linalg import eigh, cholesky, solve
import argparse
import hashlib
import json
import numpy as np


def relative_error(actual,expected):
    return float(np.linalg.norm(actual-expected)/max(1.,np.linalg.norm(expected)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label,__file__)
    try:
        evidence.report.update(original_action_unchanged=True,finite_future_trajectories_read=False,
            interval_arithmetic=False,uniform_dynamical_stability_proven=False,
            nonlinear_remainder_bound_uniform_in_mesh=False,finite_sample_diagnostics_only=True,
            reference_residual_coordinate_correction_retained=True,metric_source_shift_beta=1.,
            force_fit=False,force_correction=False,prescribed_flat_background_only=True)
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        status_path = intake/'annular-dense-GR-references-attempt01/status.json'
        status = json.loads(status_path.read_text())
        evidence.own(status_path)
        path = intake/'annular-dense-GR-references-attempt01/oracle-768.npz'
        evidence.own(path)
        evidence.check('GR_source_hash',status['state']=='complete'
            and hashlib.sha256(path.read_bytes()).hexdigest()==status['outputs'][str(path.relative_to(evidence.root))])
        with np.load(path,allow_pickle=False) as saved:
            times,states = saved['times'].copy(),saved['states'].copy()
        oracle = TwoSidedGRCharacteristics(768,mass=0.,source=.03)
        for count in [33,65,129,257]:
            for gram in [False,True]:
                branch = 'MTS' if gram else 'reference'
                system = LocallyRefinedSourceAction(count,gram,background_mass=0.,source_splits=8)
                model = FlatPreassembledFlow(system)
                energy = CanonicalEnergy(model)
                projection = GRProjection(oracle,system)
                for index in [0,42,80]:
                    instant = times[index]
                    state,derivative = projection.reconstruct(states[index],oracle.rhs(instant,states[index]))
                    blocks = energy.stability(state,derivative)
                    transform,inverse,hessian = [blocks[name] for name in ['transform','inverse_transform','hessian']]
                    prefix = str(count)+'_'+branch+'_'+str(index)
                    direction = np.random.default_rng(872+index).normal(size=len(state))
                    direction[-1] = 0.
                    direction /= np.linalg.norm(direction)
                    stepped = state.astype(complex)+1e-25j*direction
                    direct = energy.lagrangian(stepped)
                    momentum_derivative = direct['canonical_state'].imag/1e-25
                    gradient_derivative = direct['Hamiltonian_gradient'].imag/1e-25
                    evidence.check(prefix+'_Legendre_derivative',relative_error(momentum_derivative,transform @ direction[:-1])<2e-11)
                    evidence.check(prefix+'_Hamiltonian_Hessian',relative_error(gradient_derivative,hessian @ transform @ direction[:-1])<2e-11)
                    evidence.check(prefix+'_inverse_transform',relative_error(transform @ inverse,np.eye(len(inverse)))<2e-10)
                    evidence.check(prefix+'_symmetric_Hessian',relative_error(hessian,hessian.T)<2e-11)
                    velocity_flow = model.evaluate(state)['flow']
                    canonical_flow = energy.canonical_J @ blocks['Hamiltonian_gradient']
                    evidence.check(prefix+'_Hamilton_equations',relative_error(transform @ velocity_flow[:-1],canonical_flow)<2e-11)
                    flow_tangent = model.evaluate(stepped)['flow'].imag/1e-25
                    transformed_tangent = transform @ flow_tangent[:-1]+blocks['transform_rate'] @ direction[:-1]
                    predicted_tangent = blocks['generator'] @ transform @ direction[:-1]
                    evidence.check(prefix+'_off_solution_coordinate_identity',relative_error(transformed_tangent,predicted_tangent)<2e-10)
                    metric = blocks['metric']
                    rate = blocks['symmetric_rate']
                    direct_rate = blocks['metric_rate']+metric @ blocks['generator']+blocks['generator'].T @ metric
                    cancellation_error = relative_error(direct_rate,rate)
                    evidence.check(prefix+'_stiff_Hamiltonian_cancellation',cancellation_error<3e-10,cancellation_error)
                    potential = -blocks['coordinate']
                    beta_threshold = float(-potential[-1,-1]+potential[-1,:-1] @ solve(potential[:-1,:-1],potential[:-1,-1],assume_a='pos'))
                    cholesky(metric,lower=True)
                    evidence.check(prefix+'_positive_shifted_energy',beta_threshold<1.,beta_threshold)
                    eigenvalues = eigh((rate+rate.T)/2,(metric+metric.T)/2,eigvals_only=True,subset_by_index=[len(metric)-1,len(metric)-1])
                    no_correction = blocks['metric_rate']+(metric-hessian) @ blocks['canonical_generator']+blocks['canonical_generator'].T @ (metric-hessian)
                    omitted = eigh((no_correction+no_correction.T)/2,(metric+metric.T)/2,eigvals_only=True,subset_by_index=[len(metric)-1,len(metric)-1])
                    forcing_norm = float(np.sqrt(blocks['forcing'] @ metric @ blocks['forcing']))
                    force_step = model.evaluate(stepped)['force'].imag/1e-25
                    offset = system.radii-system.anchor
                    shape = offset*np.exp(-20*offset**2)
                    perturbation = np.concatenate([1e-6*shape,[1e-6],1e-6*shape,[-1e-6,0.]])
                    linear_flow = model.evaluate(state.astype(complex)+1e-25j*perturbation)['flow'].imag/1e-25
                    remainders = []
                    for scale in [1.,.5]:
                        remainder = model.evaluate(state+scale*perturbation)['flow']-velocity_flow-scale*linear_flow
                        mapped = transform @ remainder[:-1]
                        remainders.append(float(np.sqrt(mapped @ metric @ mapped)))
                    row = dict(count=count,branch=branch,time=float(instant),dimension=len(metric),
                        beta_positive_threshold=beta_threshold,maximum_energy_squared_growth_rate=float(eigenvalues[0]),
                        maximum_rate_if_residual_correction_omitted=float(omitted[0]),
                        forcing_energy_norm=forcing_norm,coordinate_identity_relative_error=relative_error(transformed_tangent,predicted_tangent),
                        cancellation_relative_error=cancellation_error,
                        nonlinear_remainder_norm=remainders[0],halved_remainder_ratio=remainders[1]/remainders[0],
                        nonzero_clock_force_direction_probe=float(force_step),uniform_stability_claim=False)
                    evidence.report['cases'].append(row)
                    destination = evidence.output/(prefix+'.npz')
                    values = dict(state=state,derivative=derivative,beta_threshold=beta_threshold,
                        growth_rate=eigenvalues,forcing=blocks['forcing'],nonlinear_remainders=np.array(remainders))
                    if count==33:
                        values.update(transform=transform,inverse_transform=inverse,hessian=hessian,metric=metric,
                            metric_rate=blocks['metric_rate'],generator=blocks['generator'],symmetric_rate=rate,
                            reference_residual_correction=blocks['reference_residual_correction'])
                    np.savez_compressed(destination,**values)
                    evidence.own(destination,'outputs')
                    evidence.save()
                    print(row,flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
