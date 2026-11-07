from common239 import *


def polynomial_add(*values):
    result = [mp.mpf(0)] * max(map(len, values))
    for value in values:
        for index, coefficient in enumerate(value):
            result[index] += coefficient
    return result


def polynomial_scale(value, factor):
    return [factor * coefficient for coefficient in value]


def polynomial_product(*values):
    result = [mp.mpf(1)]
    for value in values:
        updated = [mp.mpf(0)] * (len(result) + len(value) - 1)
        for left, first in enumerate(result):
            for right, second in enumerate(value):
                updated[left + right] += first * second
        result = updated
    return result


def evaluate(coefficients, fraction):
    result = coefficients[-1]
    for coefficient in reversed(coefficients[:-1]):
        result = result * fraction + coefficient
    return result


class RationalDirection(Direction):
    def __init__(self, parameters, direction):
        started = time.perf_counter()
        super().__init__(parameters, direction)
        self.inherited_construction_seconds = time.perf_counter() - started
        self.build()
        self.construction_seconds = time.perf_counter() - started

    def build(self):
        energy = self.energy
        angle01 = 1 - self.cosine
        angle12 = 1 - mp.fsum(first * second for first, second in zip(self.hard_direction, self.direction))
        angle02 = 1 - self.direction[2]
        self.denominator_polynomial = [1 + energy * angle01, -energy * angle12]
        self.hard_polynomial = [mp.mpf(1), -(1 + energy * angle02)]
        self.projection_polynomial = [mp.mpf(1), energy * (angle01 - angle12 - angle02), energy**2 * angle12 * angle02]
        self.constant_projection = (1 + energy * angle02) * (1 + energy * angle01) - energy * angle12
        self.common_denominator = polynomial_product([0, 1], self.projection_polynomial, self.denominator_polynomial, self.hard_polynomial)
        momentum = [polynomial_add(polynomial_product([1 + energy, -energy], self.denominator_polynomial),
            polynomial_scale(self.hard_polynomial, -energy))]
        for axis in range(3):
            momentum.append(polynomial_add(polynomial_product([energy * self.directions[0][axis], -energy * self.direction[axis]], self.denominator_polynomial),
                polynomial_scale(self.hard_polynomial, -energy * self.hard_direction[axis])))
        self.momentum_polynomial = [mp.matrix([row[index] for row in momentum]) for index in range(3)]
        spin_weights = [self.spin.gamma_matrices()[0] * (self.spin.slash(value)
            + (self.denominator_polynomial[index] if index < 2 else 0) * mp.eye(4))
            for index, value in enumerate(self.momentum_polynomial)]
        self.numerator_matrices = []
        intensity = [mp.mpc(0)] * 15
        for polarization, blocks in self.blocks:
            matrices = [mp.zeros(4, 2) for unused in range(7)]
            for last, (matrix, reduced) in enumerate(blocks):
                epsilon = self.frames[last][polarization[last]]
                projected = [self.spin.dot(value, epsilon) for value in self.momentum_polynomial]
                if last == 0:
                    direct = polynomial_scale(polynomial_product([0, 1], self.denominator_polynomial, self.denominator_polynomial, self.hard_polynomial), mp.mpf('.5'))
                    recoil = polynomial_scale(polynomial_product([0, 1], self.denominator_polynomial, self.hard_polynomial, projected), -1 / energy)
                elif last == 1:
                    direct = polynomial_scale(polynomial_product([0, 1], self.projection_polynomial, self.hard_polynomial), mp.mpf('.5'))
                    recoil = polynomial_scale(polynomial_product([0, 1], self.projection_polynomial, projected), 1 / energy)
                else:
                    direct = polynomial_scale(polynomial_product([0, 1], self.projection_polynomial, self.denominator_polynomial,
                        self.denominator_polynomial, self.hard_polynomial), 1 / (2 * self.constant_projection))
                    recoil = polynomial_scale(polynomial_product(self.projection_polynomial, self.denominator_polynomial,
                        self.hard_polynomial, projected), 1 / (energy * self.constant_projection))
                for index, coefficient in enumerate(direct):
                    matrices[index] += coefficient * matrix
                for index, coefficient in enumerate(recoil):
                    matrices[index] += coefficient * reduced
            self.numerator_matrices.append(matrices)
            for power, weight in enumerate(spin_weights):
                transformed = [weight * value for value in matrices]
                for left, before in enumerate(matrices):
                    for right, after in enumerate(transformed):
                        intensity[power + left + right] += mp.fsum(mp.conj(before[row, column]) * after[row, column]
                            for row in range(4) for column in range(2)) / 4
        self.imaginary_residual = max(abs(mp.im(value)) for value in intensity) / max(max(abs(value) for value in intensity), mp.mpf('1e-300'))
        self.intensity_numerator = [mp.re(value) for value in intensity]

    def intensity(self, signed_soft):
        fraction = scalar(signed_soft) / self.energy
        denominator = evaluate(self.denominator_polynomial, fraction)
        common = evaluate(self.common_denominator, fraction)
        return evaluate(self.intensity_numerator, fraction) / (denominator * common**2)

    def rational_amplitude(self, event):
        fraction = event['soft'] / self.energy
        common = evaluate(self.common_denominator, fraction)
        left = self.spin.spinors(event['final']).transpose_conj() * self.spin.gamma_matrices()[0]
        return [left * evaluate(coefficients, fraction) / common for coefficients in self.numerator_matrices]

    def densities(self, signed_soft):
        event = self.event(signed_soft)
        fraction = event['soft'] / self.energy
        rational = mp.matrix([1, fraction, 1 / fraction, 1 / (1 - fraction)])
        leading = (rational.transpose() * self.gram * rational)[0]
        outgoing_x = event['hard'] * self.hard_doppler / self.temperature
        original_x = self.hard0 * self.hard_doppler / self.temperature
        stimulation = (1 + 1 / mp.expm1(outgoing_x)) / (1 + 1 / mp.expm1(original_x))
        prefactor = self.alpha_factor * event['hard'] * abs(event['soft']) * stimulation / (
            self.energy * event['denominator'] * (self.hard0 / self.energy)**2 * self.tree)
        full, control = prefactor * self.intensity(signed_soft), prefactor * leading
        return dict(full=full, control=control, difference=full - control), event

    def soft_residue(self):
        return self.alpha_factor * self.energy**2 * self.intensity_numerator[0] / (
            self.tree * self.denominator_polynomial[0]**3)
