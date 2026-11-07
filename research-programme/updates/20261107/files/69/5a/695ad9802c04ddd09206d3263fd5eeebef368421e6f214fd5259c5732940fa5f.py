from common import *
import numpy as np


class EnergyMap:
    def __init__(self, system):
        self.system = system
        self.size = len(system.core)
        self.diagonal = np.ones(self.size)
        self.quadrupoles = np.array([int(np.flatnonzero(system.core == system.context["all_moments"][2, node])[0]) for node in range(5)])
        for node in range(5):
            quadrupole = self.quadrupoles[node]
            for degree in (0, 1):
                position = int(np.flatnonzero(system.core == system.context["all_moments"][degree, node])[0])
                self.diagonal[position] = np.sqrt((2 * degree + 1) / 5) * system.units[position] / system.units[quadrupole]
        tail = system.units[self.size:].reshape(190, 5)
        self.tail_weights = np.sqrt((2 * np.arange(3, 193)[:, None] + 1) / 5) * tail / system.units[self.quadrupoles]
        self.heavy = np.array(system.slots if system.model == "heavy" else [], dtype=int)
        self.rest = np.array([index for index in range(self.size) if index not in self.heavy])

    def blocks(self, efold):
        transform = np.diag(self.diagonal)
        inverse = np.diag(1 / self.diagonal)
        derivative = np.zeros((self.size, self.size))
        condition = 1.
        if len(self.heavy):
            point = self.system.context["point"](efold)
            omega = point[10] * self.system.background["masses"][1]
            ratio = self.system.wave / omega
            scale = (1 + ratio**2)**.25
            rate = -ratio**2 / (2 * (1 + ratio**2))
            phase, mu = self.system.owner.phase(efold)
            cosine, sine = np.cos(phase), np.sin(phase)
            rotation = np.array([[cosine, sine], [-sine, cosine]])
            scaling = np.diag([scale, 1 / scale])
            block = scaling @ rotation
            inverse_block = rotation.T @ np.diag([1 / scale, scale])
            skew = np.array([[0., -1.], [1., 0.]])
            rate_block = np.diag([rate, -rate]) - mu * scaling @ skew @ np.diag([1 / scale, scale])
            selection = np.ix_(self.heavy, self.heavy)
            transform[selection], inverse[selection], derivative[selection] = block, inverse_block, rate_block
            condition = scale**2
        return transform, inverse, derivative, condition

    def generator(self, efold, core):
        transform, inverse, derivative, condition = self.blocks(efold)
        return transform @ core @ inverse + derivative, transform, inverse, condition

    def comparison(self, matrix):
        remainder = matrix[np.ix_(self.rest, self.rest)]
        remainder_rate = max(0., float(np.linalg.eigvalsh((remainder + remainder.T) / 2)[-1]))
        if len(self.heavy):
            heavy = matrix[np.ix_(self.heavy, self.heavy)]
            heavy_rate = float(np.linalg.eigvalsh((heavy + heavy.T) / 2)[-1])
            to_heavy = float(np.linalg.norm(matrix[np.ix_(self.heavy, self.rest)], ord=2))
            to_rest = float(np.linalg.norm(matrix[np.ix_(self.rest, self.heavy)], ord=2))
        else:
            heavy_rate, to_heavy, to_rest = 0., 0., 0.
        return np.array([[heavy_rate, to_heavy], [to_rest, remainder_rate]])

    def hierarchy_skew(self, operator, efold):
        _, into_core, into_tail, speed, _, _ = operator.blocks(efold, 0)
        boundary = into_core / self.tail_weights[0] + into_tail * self.tail_weights[0]
        lower = operator.lower[1:, None] * speed[None, :] * self.tail_weights[1:] / self.tail_weights[:-1]
        upper = operator.upper[:-1, None] * speed[None, :] * self.tail_weights[:-1] / self.tail_weights[1:]
        scale = max(float(np.max(abs(lower))), float(np.max(abs(upper))), 1e-80)
        return max(float(np.max(abs(boundary))), float(np.max(abs(lower + upper)))) / scale

