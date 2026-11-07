from observer_common import *
from thermal_wave_common import frequency_quadrature


class ConsistentBasis(StableBasis):
    def __init__(self, count=32, quadrature=300, minimum=1e-5, maximum=60., pivot=3.):
        self.count, self.pivot = count, pivot
        self.minimum, self.maximum = minimum, maximum
        self.nodes, self.measure = frequency_quadrature(quadrature, minimum, maximum)
        constant_norm = math.sqrt(sum(self.measure))
        first = np.ones_like(self.nodes) / constant_norm
        self.mean = float(self.measure @ self.nodes / sum(self.measure))
        temperature_norm = math.sqrt(float(self.measure @ (self.nodes - self.mean) ** 2))
        second = (self.nodes - self.mean) / temperature_norm
        columns = [first, second]
        self.coefficients = np.zeros((count, count))
        self.projections = np.zeros((count, 2, count))
        self.norms = np.zeros(count)
        self.norms[:2] = [constant_norm, temperature_norm]
        compact = (self.nodes - pivot) / (self.nodes + pivot)
        for degree in range(2, count):
            value = compact * columns[-1]
            previous_values = np.column_stack(columns)
            for repeat in range(2):
                correction = previous_values.T @ (self.measure * value)
                value -= previous_values @ correction
                self.projections[degree, repeat, :degree] = correction
                self.coefficients[degree, :degree] += correction
            norm = math.sqrt(float(self.measure @ value ** 2))
            assert norm > 1e-8
            self.norms[degree] = norm
            columns.append(value / norm)
        self.values = np.column_stack(columns)
        self.mass = (self.values.T * self.measure) @ self.values
        self.chemical = np.r_[constant_norm, np.zeros(count - 1)]
        self.temperature = np.r_[self.mean * constant_norm, temperature_norm, np.zeros(count - 2)]
        self.energy = self.temperature @ self.mass
        self.number = self.chemical @ self.mass
        self.qr_orthogonality = float(linalg.norm(self.mass - np.eye(count)))

    def evaluate(self, frequency):
        frequency = np.asarray(frequency)
        compact = (frequency - self.pivot) / (frequency + self.pivot)
        values = np.empty(frequency.shape + (self.count,))
        values[..., 0] = 1 / self.norms[0]
        values[..., 1] = (frequency - self.mean) / self.norms[1]
        for degree in range(2, self.count):
            value = compact * values[..., degree - 1]
            for repeat in range(2):
                value -= values[..., :degree] @ self.projections[degree, repeat, :degree]
            values[..., degree] = value / self.norms[degree]
        return values

    def derivative(self, frequency):
        frequency = np.asarray(frequency)
        values = self.evaluate(frequency)
        compact = (frequency - self.pivot) / (frequency + self.pivot)
        compact_prime = 2 * self.pivot / (frequency + self.pivot) ** 2
        derivatives = np.zeros_like(values)
        derivatives[..., 1] = 1 / self.norms[1]
        for degree in range(2, self.count):
            derivative = compact_prime * values[..., degree - 1] + compact * derivatives[..., degree - 1]
            for repeat in range(2):
                derivative -= derivatives[..., :degree] @ self.projections[degree, repeat, :degree]
            derivatives[..., degree] = derivative / self.norms[degree]
        return derivatives
