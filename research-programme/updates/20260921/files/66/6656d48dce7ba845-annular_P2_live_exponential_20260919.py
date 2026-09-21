from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_graded_source_20260919 import scalar_pencil
from scipy.linalg import eigh
from time import perf_counter
import numpy as np


class RotationFlow:
    def __init__(self, frequency):
        self.frequency = np.asarray(frequency)
        if not np.all(np.isfinite(self.frequency)) or np.any(self.frequency < 0):
            raise ValueError('Finite nonnegative frequencies required.')

    def linear(self, state):
        return self.frequency[None, ...]*np.stack([state[1], -state[0]])

    def exponential(self, step, state):
        angle = step*self.frequency
        cosine, sine = np.cos(angle), np.sin(angle)
        return np.stack([cosine*state[0]+sine*state[1], cosine*state[1]-sine*state[0]])

    def phi1(self, step, state):
        angle = step*self.frequency
        diagonal = np.sinc(angle/np.pi)
        off_diagonal = .5*angle*np.sinc(angle/(2*np.pi))**2
        return np.stack([diagonal*state[0]+off_diagonal*state[1],
            diagonal*state[1]-off_diagonal*state[0]])


class FrozenCanonicalSplit(RotationFlow):
    def __init__(self, system, initial, geometry):
        self.system = system
        self.initial = np.asarray(initial).reshape(2, len(system.labels), system.count+1).copy()
        self.modes, self.mass_modes, frequencies, self.pencils = [], [], [], []
        self.factor_diagnostics = []
        for label, position in zip(system.labels, self.initial[0]):
            mass, stiffness = scalar_pencil(system.layer(label, geometry), position)
            eigenvalues, modes = eigh(stiffness, mass, check_finite=False)
            if eigenvalues[0] <= 0:
                raise ValueError('Scalar pencil is not positive; no eigenvalue clipping permitted.')
            mass_modes = mass @ modes
            residual = stiffness @ modes-mass_modes*eigenvalues[None, :]
            self.factor_diagnostics.append(dict(label=float(label),
                mass_orthogonality=float(np.max(abs(modes.T @ mass_modes-np.eye(system.count)))),
                normwise_backward_residual=float(np.max(np.linalg.norm(residual, axis=0)/
                    ((np.linalg.norm(stiffness)+eigenvalues*np.linalg.norm(mass))*np.linalg.norm(modes, axis=0)))),
                minimum_eigenvalue=float(eigenvalues[0]), maximum_frequency=float(np.sqrt(eigenvalues[-1]))))
            self.modes.append(modes)
            self.mass_modes.append(mass_modes)
            self.pencils.append((mass, stiffness))
            frequencies.append(np.append(np.sqrt(eigenvalues), 0.))
        super().__init__(frequencies)
        self.evaluations = 0
        self.rhs_seconds = 0.
        self.maximum_wall_seconds = 7200.
        self.started = perf_counter()

    def encode(self, delta):
        delta = np.asarray(delta).reshape(self.initial.shape)
        transformed = delta.copy()
        for index, (modes, mass_modes) in enumerate(zip(self.modes, self.mass_modes)):
            transformed[0, index, :-1] = self.frequency[index, :-1]*(mass_modes.T @ delta[0, index, :-1])
            transformed[1, index, :-1] = modes.T @ delta[1, index, :-1]
        return transformed

    def decode(self, transformed):
        delta = np.asarray(transformed).copy()
        for index, (modes, mass_modes) in enumerate(zip(self.modes, self.mass_modes)):
            delta[0, index, :-1] = modes @ (transformed[0, index, :-1]/self.frequency[index, :-1])
            delta[1, index, :-1] = mass_modes @ transformed[1, index, :-1]
        return delta

    def physical(self, transformed):
        return self.initial+self.decode(transformed)

    def live(self, transformed):
        if perf_counter()-self.started > self.maximum_wall_seconds:
            raise RuntimeError('Safe wall budget reached; accepted steps are preserved.')
        started = perf_counter()
        flow = self.system.rhs(0., self.physical(transformed).ravel()).reshape(self.initial.shape)
        self.rhs_seconds += perf_counter()-started
        self.evaluations += 1
        return self.encode(flow)

    def remainder(self, transformed):
        return self.live(transformed)-self.linear(transformed)

    def relative_energy_difference(self, first, second):
        initial_modes = self.encode(self.initial)
        numerator = np.linalg.norm((first-second)[:, :, :-1])
        denominator = np.linalg.norm(initial_modes[:, :, :-1])
        return float(numerator/denominator)


def exponential_midpoint(flow, state, step, first_remainder=None):
    start = flow.remainder(state) if first_remainder is None else first_remainder
    middle = flow.exponential(step/2, state)+(step/2)*flow.phi1(step/2, start)
    return flow.exponential(step, state)+step*flow.phi1(step, flow.remainder(middle))
