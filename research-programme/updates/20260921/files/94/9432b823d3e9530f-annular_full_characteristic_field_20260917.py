from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_characteristic_source_20260917 import rhs, force
from run_annular_source_fitted_crossing_20260915 import profile
from numpy.polynomial import Polynomial
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import numpy as np


class InitialPrimitives:
    def __init__(self):
        offset = Polynomial([0., 1.])
        envelope = Polynomial([1., 0., 0., -10., 15., -6.])
        self.edges = np.array([-.83, -.55, -.2, .2, .55, .77])
        self.pieces = [Polynomial([0.]), .01*offset*envelope((-offset-.2)/.35),
            .01*offset, .01*offset*envelope((offset-.2)/.35), Polynomial([0.])]
        self.integrals = []
        accumulated = 0.
        for lower, upper, piece in zip(self.edges[:-1], self.edges[1:], self.pieces):
            primitive = piece.integ()
            primitive += accumulated-primitive(lower)
            self.integrals.append(primitive)
            accumulated = primitive(upper)
        self.origin_integral = self.integrals[2](0.)

    def profile(self, radius, derivative=0):
        offset = np.asarray(radius, dtype=float)-6.03
        labels = np.searchsorted(self.edges[1:-1], offset, side='right')
        answer = np.zeros_like(offset)
        for index, piece in enumerate(self.pieces):
            selected = labels == index
            answer[selected] = piece.deriv(derivative)(offset[selected])
        return answer

    def integral(self, radius):
        offset = np.asarray(radius, dtype=float)-6.03
        labels = np.searchsorted(self.edges[1:-1], offset, side='right')
        answer = np.zeros_like(offset)
        for index, piece in enumerate(self.integrals):
            selected = labels == index
            answer[selected] = piece(offset[selected])-self.origin_integral
        return answer

    def incoming(self, argument, kind):
        radius = -np.asarray(argument) if kind == 'F' else np.asarray(argument)
        scalar = self.profile(radius)
        radial = self.profile(radius, 1)
        second = self.profile(radius, 2)
        velocity = .06 if kind == 'F' else -.06
        value = ((1+velocity)*radius*scalar-velocity*self.integral(radius))/2
        first = (scalar+(1+velocity)*radius*radial)/2
        if kind == 'F':
            first = -first
        curvature = ((2+velocity)*radial+(1+velocity)*radius*second)/2
        return value, first, curvature


class FullCharacteristicField:
    def __init__(self, tight=False, horizon=.4):
        if horizon <= 0. or horizon > .4:
            raise ValueError('Only the energy-gated horizon (0,.4] is implemented.')
        self.horizon = horizon
        self.initial = InitialPrimitives()
        tolerance = 2e-13 if tight else 2e-12
        maximum_step = .0005 if tight else .001
        settings = dict(method='DOP853', rtol=tolerance, atol=tolerance/100,
            max_step=maximum_step, dense_output=True)
        self.source = solve_ivp(rhs, (0., horizon), [6.03, .06, 0.], **settings)
        if not self.source.success:
            raise RuntimeError(self.source.message)

        def left_rhs(instant, state):
            value, first, unused = self.initial.incoming(instant+5.2, 'G')
            return np.array([first-(value+state[0])/5.2])

        def right_rhs(instant, state):
            value, first, unused = self.initial.incoming(instant-6.8, 'F')
            return np.array([first+(value+state[0])/6.8])

        self.left = solve_ivp(left_rhs, (0., horizon), [self.initial.incoming(-5.2, 'F')[0]], **settings)
        self.right = solve_ivp(right_rhs, (0., horizon), [self.initial.incoming(6.8, 'G')[0]], **settings)
        if not self.left.success or not self.right.success:
            raise RuntimeError('Outer Robin integration failed.')
        self.transition_times = {'left': [], 'right': []}
        for side, sign, radii in [('left', -1., [5.48, 5.83]), ('right', 1., [6.23, 6.58])]:
            for radius in radii:
                def difference(instant):
                    return self.source.sol(instant)[0]+sign*instant-radius
                if difference(0.)*difference(horizon) < 0.:
                    self.transition_times[side].append(brentq(difference, 0., horizon, xtol=5e-15))

    def retarded(self, argument, sign):
        argument = np.asarray(argument, dtype=float)
        initial = sign*6.03
        final = self.horizon+sign*self.source.sol(self.horizon)[0]
        if np.any(argument < initial-3e-13) or np.any(argument > final+3e-13):
            raise ValueError('Retarded source argument outside the qualified horizon.')
        instant = np.clip((argument-initial)/(1+sign*.06), 0., self.horizon)
        for unused in range(8):
            state = self.source.sol(instant)
            defect = instant+sign*state[0]-argument
            instant = np.clip(instant-defect/(1+sign*state[1]), 0., self.horizon)
        state = self.source.sol(instant)
        if np.max(abs(instant+sign*state[0]-argument), initial=0.) > 3e-13:
            raise RuntimeError('Retarded source inversion did not converge.')
        return instant, state

    def reflected_source(self, argument, kind):
        sign = 1. if kind == 'G' else -1.
        instant, state = self.retarded(argument, sign)
        position, velocity = state[:2]
        incoming_argument = instant-sign*position
        value, first, second = self.initial.incoming(incoming_argument, 'F' if kind == 'G' else 'G')
        feet = np.stack([position-instant, position+instant])
        scalar, gradient = profile(feet)
        signs = np.array([1., -1.]).reshape((2,)+(1,)*instant.ndim)
        traces = (scalar+(1+.06*signs)*feet*gradient)/(position*(1+signs*velocity))
        acceleration = position**2*(1-velocity**2)**2.5*(traces[0]**2-traces[1]**2)/.06
        denominator = 1+sign*velocity
        ratio = (1-sign*velocity)/denominator
        return -value, -first*ratio, -second*ratio**2+sign*2*acceleration*first/denominator**3

    def reflected_outer(self, argument, kind):
        argument = np.asarray(argument)
        if kind == 'F':
            instant = argument+5.2
            value = self.left.sol(instant)[0]
            incoming, first, second = self.initial.incoming(instant+5.2, 'G')
            derivative = first-(incoming+value)/5.2
            curvature = second-(first+derivative)/5.2
        else:
            instant = argument-6.8
            value = self.right.sol(instant)[0]
            incoming, first, second = self.initial.incoming(instant-6.8, 'F')
            derivative = first+(incoming+value)/6.8
            curvature = second+(first+derivative)/6.8
        if np.any(instant < -3e-13) or np.any(instant > self.horizon+3e-13):
            raise ValueError('Outer reflection outside the qualified horizon.')
        return value, derivative, curvature

    def component(self, argument, kind, side):
        argument = np.asarray(argument, dtype=float)
        threshold = (-5.2 if kind == 'F' else 6.03) if side == 'left' else (-6.03 if kind == 'F' else 6.8)
        reflected = argument > threshold
        result = np.empty((3, argument.size))
        if np.any(~reflected):
            result[:, ~reflected] = self.initial.incoming(argument[~reflected], kind)
        if np.any(reflected):
            at_source = (side == 'left' and kind == 'G') or (side == 'right' and kind == 'F')
            evaluator = self.reflected_source if at_source else self.reflected_outer
            result[:, reflected] = evaluator(argument[reflected], kind)
        return result

    def sample(self, instant, radius, source_side='left'):
        radius = np.atleast_1d(np.asarray(radius, dtype=float))
        if radius.ndim != 1 or np.any(radius < 5.2-3e-13) or np.any(radius > 6.8+3e-13):
            raise ValueError('Sample must be a radius vector inside [5.2,6.8].')
        if instant < 0. or instant > self.horizon:
            raise ValueError('Time outside the qualified horizon.')
        position = self.source.sol(instant)[0]
        left = radius <= position if source_side == 'left' else radius < position
        outgoing, incoming = np.empty((3, len(radius))), np.empty((3, len(radius)))
        for side, selected in [('left', left), ('right', ~left)]:
            if np.any(selected):
                outgoing[:, selected] = self.component(instant-radius[selected], 'F', side)
                incoming[:, selected] = self.component(instant+radius[selected], 'G', side)
        scalar = outgoing[0]+incoming[0]
        temporal = outgoing[1]+incoming[1]
        radial = -outgoing[1]+incoming[1]
        second = outgoing[2]+incoming[2]
        mixed = -outgoing[2]+incoming[2]
        return dict(phi=scalar/radius, phi_t=temporal/radius,
            phi_r=radial/radius-scalar/radius**2,
            phi_tt=second/radius,
            phi_tr=mixed/radius-temporal/radius**2,
            phi_rr=second/radius-2*radial/radius**2+2*scalar/radius**3)

    def breakpoints(self, instant):
        position = self.source.sol(instant)[0]
        candidates = [5.2, 6.8, position, 6.03-instant, 6.03+instant, 5.2+instant, 6.8-instant]
        for radius in [5.48, 5.83, 6.23, 6.58]:
            candidates.extend([radius-instant, radius+instant, 10.4-radius+instant, 13.6-radius-instant])
        for side, times in self.transition_times.items():
            for emitted in times:
                if emitted <= instant:
                    source = self.source.sol(emitted)[0]
                    candidates.append(source+emitted-instant if side == 'left' else source-emitted+instant)
        return np.unique(np.array([value for value in candidates if 5.2 <= value <= 6.8]))

    def energy(self, instant, order=16):
        edges = self.breakpoints(instant)
        nodes, weights = np.polynomial.legendre.leggauss(order)
        radius = ((edges[1:, None]+edges[:-1, None])/2+np.diff(edges)[:, None]*nodes/2).ravel()
        measure = (np.diff(edges)[:, None]*weights/2).ravel()
        values = self.sample(instant, radius)
        field = np.dot(measure*radius**2, values['phi_t']**2+values['phi_r']**2)/2
        velocity = self.source.sol(instant)[1]
        return float(field+.03/np.sqrt(1-velocity**2))
