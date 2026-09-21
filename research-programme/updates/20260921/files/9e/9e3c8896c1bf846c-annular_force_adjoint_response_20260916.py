import numpy as np
from scipy.interpolate import CubicHermiteSpline, CubicSpline


class ResponsePath:
    def __init__(self,times,states,derivatives):
        self.origin = states[0].copy()
        self.polynomial = CubicHermiteSpline(times,states-self.origin,derivatives,axis=0,extrapolate=False)

    def value(self,instant):
        return self.origin+self.polynomial(instant)

    def derivative(self,instant):
        return self.polynomial(instant,1)


class AdjointResponse:
    def __init__(self,model,data,stride):
        self.model = model
        self.times = data['times'][::stride]
        self.raw = ResponsePath(self.times,data['raw_states'][::stride],data['raw_derivatives'][::stride])
        self.reduced = ResponsePath(self.times,data['reduced_states'][::stride],data['reduced_derivatives'][::stride])
        self.defect = CubicSpline(self.times,data['physical_defects'][::stride],axis=0,extrapolate=False)
        self.dimension = data['raw_states'].shape[1]
        self.initial_error = data['raw_states'][0]-data['reduced_states'][0]
        self.final_error = data['raw_states'][-1]-data['reduced_states'][-1]
        self.terminal = model.evaluate(data['reduced_states'][-1],True)['force_gradient']
        self.original_data = data

    def terms(self,instant):
        reduced_state = self.reduced.value(instant)
        raw_state = self.raw.value(instant)
        reduced = self.model.evaluate(reduced_state,True)
        raw = self.model.evaluate(raw_state)
        motion_defect = self.defect(instant)
        reduced_residual = reduced['flow']-self.reduced.derivative(instant)
        raw_residual = raw['flow']-self.raw.derivative(instant)
        nonlinear = raw['flow']-reduced['flow']-reduced['jacobian'] @ (raw_state-reduced_state)
        return reduced['jacobian'],motion_defect,reduced_residual-motion_defect,raw_residual,nonlinear

    def backward(self,instant,state):
        covector = state[:self.dimension]
        jacobian,motion,interpolation,raw_residual,nonlinear = self.terms(instant)
        integrands = np.array([covector @ motion,covector @ interpolation,-covector @ raw_residual,covector @ nonlinear])
        return np.concatenate([-jacobian.T @ covector,-integrands])

    def tangent(self,instant,state):
        perturbations = state.reshape(3,self.dimension)
        jacobian,motion,interpolation,raw_residual,nonlinear = self.terms(instant)
        derivative = perturbations @ jacobian.T
        derivative[1] += motion
        derivative[2] += motion+interpolation-raw_residual
        return derivative.ravel()

    def summarize(self,result):
        final = result.y[:,-1]
        initial_response = float(final[:self.dimension] @ self.initial_error)
        motion,interpolation,raw_residual,nonlinear = final[self.dimension:]
        raw_force = self.model.evaluate(self.original_data['raw_states'][-1])['force']
        lifted_force = self.model.evaluate(self.original_data['reduced_states'][-1])['force']
        observed = float(raw_force-self.original_data['reduced_forces'][-1])
        direct = float(lifted_force-self.original_data['reduced_forces'][-1])
        observable_remainder = float(raw_force-lifted_force-self.terminal @ self.final_error)
        physical_linear_prediction = direct+initial_response+motion
        numerical_contribution = interpolation+raw_residual
        remainder = nonlinear+observable_remainder
        complete_prediction = physical_linear_prediction+numerical_contribution+remainder
        return dict(observed_total_force_difference=observed,direct_same_state_omission=direct,
            initial_preparation_linear_response=initial_response,accumulated_motion_linear_response=float(motion),
            reduced_interpolation_contribution=float(interpolation),full_replay_residual_contribution=float(raw_residual),
            net_reconstruction_contribution=float(numerical_contribution),
            absolute_reconstruction_contributions=float(abs(interpolation)+abs(raw_residual)),
            dynamical_nonlinear_remainder=float(nonlinear),observable_nonlinear_remainder=observable_remainder,
            total_measured_nonlinear_remainder=float(remainder),physical_linear_prediction=float(physical_linear_prediction),
            prediction_including_numerical_and_nonlinear_terms=float(complete_prediction),
            exact_identity_closure_error=abs(float(complete_prediction-observed)),
            physical_linear_prediction_error=abs(float(physical_linear_prediction-observed)),
            counterfactual_initial_effect=float(self.original_data['initial_force_effect'][-1]),
            counterfactual_motion_effect=float(self.original_data['moving_force_effect'][-1]),
            initial_counterfactual_linear_difference=float(initial_response-self.original_data['initial_force_effect'][-1]),
            motion_counterfactual_linear_difference=float(direct+motion-self.original_data['moving_force_effect'][-1]),
            initial_adjoint_clock_component=float(final[self.dimension-1]),
            path_node_count=len(self.times),nfev=result.nfev,nonlinear_remainder_is_measured_not_uniform_bound=True)
