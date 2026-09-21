from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_weighted_projection_bounds_20260919 import band_action
from scipy.linalg import cholesky_banded,cho_solve_banded
from scipy.sparse.linalg import LinearOperator,expm_multiply
import numpy as np


class FactoredAction:
    def __init__(self,mass_bands,gradient,gradient_weights,gram,gram_weights):
        self.mass_bands = mass_bands
        self.count = mass_bands.shape[1]
        self.mass_factor = cholesky_banded(mass_bands[2:].copy(),lower=True,check_finite=False)
        self.gradient,self.gradient_weights = gradient,gradient_weights
        self.gram,self.gram_weights = gram,gram_weights

    def mass(self,values):
        if values.ndim == 1:
            return band_action(self.mass_bands,values)
        return np.column_stack([band_action(self.mass_bands,values[:,column]) for column in range(values.shape[1])])

    def solve_mass(self,values):
        return cho_solve_banded((self.mass_factor,True),values,check_finite=False)

    def stiffness(self,values):
        first,second = self.gradient @ values,self.gram @ values
        if values.ndim == 2:
            first,second = self.gradient_weights[:,None]*first,self.gram_weights[:,None]*second
        else:
            first,second = self.gradient_weights*first,self.gram_weights*second
        return self.gradient.T @ first+self.gram.T @ second

    def acceleration_operator(self,values):
        return self.solve_mass(self.stiffness(values))

    def acceleration_transpose(self,values):
        return self.stiffness(self.solve_mass(values))

    def energy(self,velocity,acceleration):
        return .5*float(acceleration @ self.mass(acceleration)+velocity @ self.stiffness(velocity))

    def energy_norm(self,velocity,acceleration):
        return float(np.sqrt(max(2*self.energy(velocity,acceleration),0.)))


class VelocityGenerator(LinearOperator):
    def __init__(self,action,slope,scale):
        self.action,self.slope,self.scale = action,slope,float(scale)
        self.calls = 0
        super().__init__(dtype=np.dtype(float),shape=(2*action.count+1,2*action.count+1))

    def _matmat(self,values):
        self.calls += values.shape[1]
        count = self.action.count
        first = self.scale*values[count:2*count]
        second = -self.action.acceleration_operator(values[:count])/self.scale+self.slope[:,None]*values[-1]
        return np.vstack([first,second,np.zeros((1,values.shape[1]))])

    def _rmatmat(self,values):
        count = self.action.count
        first = -self.action.acceleration_transpose(values[count:2*count])/self.scale
        second = self.scale*values[:count]
        last = self.slope @ values[count:2*count]
        return np.vstack([first,second,last[None,:]])

    def _matvec(self,values):
        return self._matmat(values.reshape(-1,1))[:,0]

    def _rmatvec(self,values):
        return self._rmatmat(values.reshape(-1,1))[:,0]


def propagate(action,velocity,acceleration,slope,step,constants,scale=1e6):
    generator = VelocityGenerator(action,slope,scale)
    state = np.vstack([scale*velocity,acceleration,np.asarray(constants)[None,:]])
    result = expm_multiply(step*generator,state,traceA=0.)
    count = action.count
    return dict(velocity=result[:count]/scale,acceleration=result[count:2*count],
        constants=result[-1],operator_vector_products=generator.calls)
