from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_GR_causal_predictor_20260917 import HermiteReference, CausalPredictor
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_full_force_linearization_20260916 import FullForceLinearization
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from run_annular_source_fitted_crossing_20260915 import initial
import argparse
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label,__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        folder = intake/'annular-GR-projection-residual-attempt02'
        path = folder/'status.json'
        evidence.own(path)
        status = json.loads(path.read_text())
        evidence.check('GR_only_projection_complete',status['state']=='complete' and not status['finite_future_trajectories_read']
            and all(row['passed'] for row in status['checks']))
        evidence.report.update(known_benchmark_not_blind_new_experiment=True,finite_future_trajectories_read=False,
            prescribed_flat_background_only=True,original_action_unchanged=True,count=1025,source_splits=8,
            predictor_equation='eta_dot=DF(z)eta+F(z)-z_dot',
            observables_prespecified=['linearized_force','original_force_on_reconstructed_state'],
            physical_force_gate=2e-7,numerical_control_gate=2e-8)
        system = LocallyRefinedSourceAction(1025,True,background_mass=0.,source_splits=8)
        seed = initial(system)
        for degree in [384,512,768]:
            path = folder/('projection-'+str(degree)+'-1025.npz')
            evidence.own(path)
            evidence.check(str(degree)+'_projection_hash',hashlib.sha256(path.read_bytes()).hexdigest()==status['outputs'][str(path.relative_to(evidence.root))])
            with np.load(path,allow_pickle=False) as saved:
                data = {name:saved[name].copy() for name in ['times','states','derivatives','oracle_forces']}
            evidence.check(str(degree)+'_shapes_and_finite',data['states'].shape==(81,2*system.count+3)
                and data['derivatives'].shape==data['states'].shape and data['times'][0]==0. and data['times'][-1]==.4
                and all(np.isfinite(value).all() for value in data.values()))
            errors = []
            for stride in [1,2]:
                reference = HermiteReference(data['times'][::stride],data['states'][::stride],data['derivatives'][::stride])
                for instant,state,derivative in zip(reference.times,reference.states,reference.derivatives):
                    actual,actual_derivative = reference.evaluate(instant)
                    errors.append(max(float(np.max(abs(actual-state))),float(np.max(abs(actual_derivative-derivative)))))
            evidence.check(str(degree)+'_Hermite_knots_and_derivatives',max(errors)<2e-11,max(errors))
            destination = evidence.output/('GR-only-'+str(degree)+'-1025.npz')
            np.savez_compressed(destination,**data,original_initial=seed)
            evidence.own(destination,'outputs')
            evidence.report['cases'].append(dict(degree=degree,count=1025,splits=8,scalar_dofs=system.count,
                maximum_knot_error=max(errors),initial_projection_difference=float(np.max(abs(seed-data['states'][0])))))
        times = np.array([0.,.05,.11,.2])
        weights = np.array([[1.,-.3],[2.,4.],[-.7,.2],[.4,-.1]])

        def polynomial(instant):
            return weights[0]+instant*(weights[1]+instant*(weights[2]+instant*weights[3]))

        def polynomial_derivative(instant):
            return weights[1]+instant*(2*weights[2]+3*instant*weights[3])

        reference = HermiteReference(times,np.array([polynomial(value) for value in times]),
            np.array([polynomial_derivative(value) for value in times]))
        polynomial_errors,derivative_errors = [],[]
        for instant in np.linspace(0.,.2,137):
            state,derivative = reference.evaluate(instant)
            polynomial_errors.append(float(np.max(abs(state-polynomial(instant)))))
            derivative_errors.append(float(np.max(abs(derivative-polynomial_derivative(instant)))))
        evidence.check('known_cubic_reconstruction',max(polynomial_errors)<2e-13 and max(derivative_errors)<2e-12,
            dict(state=max(polynomial_errors),derivative=max(derivative_errors)))
        generator = np.random.default_rng(20260917)
        for gram in [False,True]:
            branch = 'MTS' if gram else 'reference'
            small = LocallyRefinedSourceAction(33,gram,background_mass=0.,source_splits=2)
            model = FlatPreassembledFlow(small)
            independent = FullForceLinearization(small)
            seed = initial(small)
            seed[small.count] += .009
            seed[:small.count] += generator.normal(size=small.count)*1e-6
            direction = generator.normal(size=len(seed))*1e-6
            direction[small.count] *= .01
            analytic = independent.evaluate(seed,linearize=True)
            sampled = model.evaluate(seed.astype(complex)+1e-25j*direction)
            derivative = sampled['flow'].imag/1e-25
            expected = analytic['jacobian'] @ direction
            error = float(np.linalg.norm(derivative-expected)/max(np.linalg.norm(expected),1e-30))
            evidence.check(branch+'_independent_analytic_full_Jacobian',error<2e-10,error)
            force_error = float(abs(sampled['force'].imag/1e-25-analytic['force_gradient'] @ direction))
            evidence.check(branch+'_independent_force_direction',force_error<2e-11,force_error)
            clock_direction = np.zeros_like(seed)
            clock_direction[-1] = 1.
            evidence.check(branch+'_clock_gauge_silence',np.max(abs(model.evaluate(seed.astype(complex)+1e-25j*clock_direction)['flow'].imag))==0.)
            reference = HermiteReference(np.array([0.,.05]),np.stack([seed,seed+.05*analytic['flow']]),
                np.stack([analytic['flow'],analytic['flow']]))
            predictor = CausalPredictor(model,reference)
            linear_error = float(np.max(abs(predictor.rhs(0.,direction)-expected)))
            evidence.check(branch+'_causal_initial_equation',linear_error<2e-10,linear_error)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
