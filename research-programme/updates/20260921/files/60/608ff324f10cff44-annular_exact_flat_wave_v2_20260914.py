import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq
from annular_dynamical_source_20260914 import outgoing_profile


class ExactFlatWave:
    def __init__(self, amplitude, reservoir=.003, inverse_count=16385):
        self.amplitude = amplitude
        self.reservoir = reservoir
        def null_rhs(retarded, state):
            derivative = float(outgoing_profile(retarded, amplitude)[1])
            return [2*derivative**2/reservoir, state[0]**2, state[0]]
        self.solution = solve_ivp(null_rhs, (-6., -4.8), [1.,6.,0.], method='DOP853',
                                  rtol=2e-13, atol=2e-15, max_step=.0005, dense_output=True)
        if not self.solution.success:
            raise RuntimeError(self.solution.message)
        retarded = np.linspace(-6.,-4.8,inverse_count)
        factor, advanced, proper_time = self.solution.sol(retarded)
        self.inverse_advanced = PchipInterpolator(advanced, retarded, extrapolate=False)
        self.final_proper_time = self.solution.sol(-5.2)[2]
        self.pulse_final_advanced = self.solution.sol(-5.2)[1]
        self.total_incident = reservoir*(self.solution.sol(-5.2)[0]-1)/2

    def shell(self, proper_time):
        if proper_time == 0:
            retarded = -6.
        else:
            retarded = brentq(lambda value: self.solution.sol(value)[2]-proper_time, -6.,-4.8,xtol=5e-15)
        factor, advanced, actual_proper = self.solution.sol(retarded)
        return dict(radius=(advanced-retarded)/2, time=(advanced+retarded)/2,
                    proper_rate=(factor-1/factor)/2, factor=factor, retarded=retarded)

    def wave(self, time, radii):
        value, derivative = outgoing_profile(time-radii, self.amplitude)
        advanced = time+radii
        returning = np.zeros_like(radii)
        returning_derivative = np.zeros_like(radii)
        selected = (advanced > 6.2)&(advanced < self.pulse_final_advanced)
        if not np.any(selected):
            scalar = value/radii
            return dict(outgoing=2*derivative+scalar, incoming=-scalar, scalar=scalar)
        emission = self.inverse_advanced(advanced[selected])
        factor = self.solution.sol(emission)[0]
        mirror_value, mirror_derivative = outgoing_profile(emission, self.amplitude)
        returning[selected] = -mirror_value
        returning_derivative[selected] = -mirror_derivative/factor**2
        scalar = (value+returning)/radii
        radial_field = -derivative+returning_derivative-scalar
        time_field = derivative+returning_derivative
        return dict(outgoing=time_field-radial_field, incoming=time_field+radial_field, scalar=scalar)
