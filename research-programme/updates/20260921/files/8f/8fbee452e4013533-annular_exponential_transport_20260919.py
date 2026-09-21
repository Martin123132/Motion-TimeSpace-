from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_live_exponential_20260919 import RotationFlow
import numpy as np


class ExponentialTransport(RotationFlow):
    def phi2(self, step, state):
        angle = step*self.frequency
        diagonal = .5*np.sinc(angle/(2*np.pi))**2
        small = abs(angle) < 1e-3
        safe = np.where(small, 1., angle)
        off_diagonal = np.where(small,
            angle*(1/6-angle**2/120+angle**4/5040-angle**6/362880),
            (angle-np.sin(angle))/safe**2)
        return np.stack([diagonal*state[0]+off_diagonal*state[1],
            diagonal*state[1]-off_diagonal*state[0]])

    def affine_forcing(self, step, first, last):
        return step*(self.phi1(step, first)+self.phi2(step, last-first))

    def dual(self, lag, covector):
        return self.exponential(-lag, covector)

    def budget(self, times, errors, remainders, covector, stride=1):
        indices = np.arange(0, len(times), stride)
        if indices[-1] != len(times)-1:
            raise ValueError('Quadrature partition must include the endpoint.')
        times, errors, remainders = times[indices], errors[indices], remainders[indices]
        initial = float(np.sum(self.dual(times[-1]-times[0], covector)*errors[0]))
        endpoint = float(np.sum(covector*errors[-1]))
        forcing_terms, defect_terms, direct_terms, ordinary_terms = [], [], [], []
        for index, step in enumerate(np.diff(times)):
            dual_end = self.dual(times[-1]-times[index+1], covector)
            propagated = self.exponential(step, errors[index])
            forcing = self.affine_forcing(step, remainders[index], remainders[index+1])
            increment = errors[index+1]-propagated
            defect = increment-forcing
            forcing_terms.append(float(np.sum(dual_end*forcing)))
            defect_terms.append(float(np.sum(dual_end*defect)))
            direct_terms.append(float(np.sum(dual_end*increment)))
            dual_start = self.dual(times[-1]-times[index], covector)
            ordinary_terms.append(float(step/2*(np.sum(dual_start*remainders[index])
                +np.sum(dual_end*remainders[index+1]))))
        forced = float(np.sum(forcing_terms))
        residual = float(np.sum(defect_terms))
        return dict(sample_intervals=len(times)-1, initial_pairing=initial, endpoint_pairing=endpoint,
            exponential_forcing=forced, unresolved_trajectory_and_quadrature_defect=residual,
            ordinary_weighted_trapezoid=float(np.sum(ordinary_terms)),
            exact_discrete_propagated_increment=float(np.sum(direct_terms)),
            forcing_absolute_interval_bound=float(np.sum(abs(np.array(forcing_terms)))),
            defect_absolute_interval_bound=float(np.sum(abs(np.array(defect_terms)))),
            endpoint_reconstruction_error=abs(initial+forced+residual-endpoint),
            forcing_only_endpoint_difference=initial+forced-endpoint,
            no_integrator_error_certificate=True, valid_for_claim=False)


class SavedCentralBasis(ExponentialTransport):
    def __init__(self, saved, index):
        self.modes = saved['modes'][index]
        self.mass_modes = saved['mass_modes'][index]
        super().__init__(saved['frequency'][index])
        if np.any(self.frequency[:-1] <= 0) or self.frequency[-1] != 0:
            raise ValueError('All positive scalar modes and the zero source block must remain.')

    def encode(self, physical):
        result = np.array(physical, copy=True)
        result[0, :-1] = self.frequency[:-1]*(self.mass_modes.T @ physical[0, :-1])
        result[1, :-1] = self.modes.T @ physical[1, :-1]
        return result

    def decode(self, encoded):
        result = np.array(encoded, copy=True)
        result[0, :-1] = self.modes @ (encoded[0, :-1]/self.frequency[:-1])
        result[1, :-1] = self.mass_modes @ encoded[1, :-1]
        return result

    def field_covector(self, gradient):
        result = np.zeros((2, len(self.frequency)))
        result[0, :-1] = (self.modes.T @ gradient)/self.frequency[:-1]
        return result
