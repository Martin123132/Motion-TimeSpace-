from pathlib import Path
import sys
import numpy as np


class HermiteReference:
    def __init__(self, times, states, derivatives):
        self.times = np.asarray(times)
        self.states = np.asarray(states)
        self.derivatives = np.asarray(derivatives)
        widths = np.diff(self.times)
        if np.any(widths<=0.) or self.states.shape!=self.derivatives.shape or len(self.states)!=len(times):
            raise ValueError('Invalid reference data.')
        secants = np.diff(self.states,axis=0)/widths[:,None]
        cubic = (self.derivatives[:-1]+self.derivatives[1:]-2*secants)/widths[:,None]**2
        quadratic = (3*secants-2*self.derivatives[:-1]-self.derivatives[1:])/widths[:,None]
        self.coefficients = np.stack([cubic,quadratic,self.derivatives[:-1],self.states[:-1]],axis=1)

    def evaluate(self, instant):
        if instant<self.times[0]-1e-14 or instant>self.times[-1]+1e-14:
            raise ValueError('Reference extrapolation is forbidden.')
        index = int(np.clip(np.searchsorted(self.times,instant,side='right')-1,0,len(self.times)-2))
        offset = instant-self.times[index]
        cubic,quadratic,linear,constant = self.coefficients[index]
        state = ((cubic*offset+quadratic)*offset+linear)*offset+constant
        derivative = (3*cubic*offset+2*quadratic)*offset+linear
        return state,derivative


class CausalPredictor:
    def __init__(self, model, reference):
        self.model,self.reference = model,reference

    def rhs(self, instant, correction):
        state,derivative = self.reference.evaluate(instant)
        value = self.model.evaluate(state.astype(complex)+1e-25j*correction)
        return value['flow'].real+value['flow'].imag/1e-25-derivative

    def outputs(self, instant, correction):
        state,derivative = self.reference.evaluate(instant)
        value = self.model.evaluate(state.astype(complex)+1e-25j*correction)
        corrected = state+correction
        reconstructed = self.model.evaluate(corrected,True)
        linear_flow = value['flow'].real+value['flow'].imag/1e-25
        return dict(state=corrected,linear_force=value['force'].real+value['force'].imag/1e-25,
            reconstructed_force=reconstructed['force'],nonlinear_flow_remainder=reconstructed['flow']-linear_flow,
            energy=reconstructed['energy'],schur=reconstructed['schur'])


def restrict_array_reads(allowed_inputs, output):
    allowed = {Path(path).resolve() for path in allowed_inputs}
    output = Path(output).resolve()

    def guard(event, arguments):
        if event!='open' or not isinstance(arguments[0],(str,bytes,Path)):
            return
        path = Path(arguments[0]).resolve()
        if path.suffix.lower() in ['.npz','.npy'] and path not in allowed and not path.is_relative_to(output):
            raise PermissionError('Array input is outside the isolated predictor allowlist: '+str(path))

    sys.addaudithook(guard)
