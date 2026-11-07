from thermal_wave_common import *


class StableBasis:
    def __init__(self, count=24, quadrature=300, minimum=1e-5, maximum=60., pivot=3.):
        self.count, self.pivot = count, pivot
        self.minimum, self.maximum = minimum, maximum
        self.nodes, self.measure = frequency_quadrature(quadrature, minimum, maximum)
        constant_norm = math.sqrt(sum(self.measure))
        first = np.ones_like(self.nodes) / constant_norm
        mean = float(self.measure @ self.nodes / sum(self.measure))
        temperature_norm = math.sqrt(float(self.measure @ (self.nodes - mean) ** 2))
        second = (self.nodes - mean) / temperature_norm
        columns = [first, second]
        self.coefficients = np.zeros((count, count))
        self.norms = np.zeros(count)
        self.norms[:2] = [constant_norm, temperature_norm]
        self.mean = mean
        compact = (self.nodes - pivot) / (self.nodes + pivot)
        for degree in range(2, count):
            value = compact * columns[-1]
            previous = np.column_stack(columns)
            projection = np.zeros(degree)
            for repeat in range(2):
                correction = previous.T @ (self.measure * value)
                value -= previous @ correction
                projection += correction
            norm = math.sqrt(float(self.measure @ value ** 2))
            assert norm > 1e-8
            self.coefficients[degree, :degree] = projection
            self.norms[degree] = norm
            columns.append(value / norm)
        self.values = np.column_stack(columns)
        self.mass = (self.values.T * self.measure) @ self.values
        self.chemical = np.r_[constant_norm, np.zeros(count - 1)]
        self.temperature = np.r_[mean * constant_norm, temperature_norm, np.zeros(count - 2)]
        self.energy = self.temperature @ self.mass
        self.number = self.chemical @ self.mass
        self.qr_orthogonality = float(np.linalg.norm(self.mass - np.eye(count)))

    def evaluate(self, frequency):
        frequency = np.asarray(frequency)
        compact = (frequency - self.pivot) / (frequency + self.pivot)
        values = np.empty(frequency.shape + (self.count,))
        values[..., 0] = 1 / self.norms[0]
        values[..., 1] = (frequency - self.mean) / self.norms[1]
        for degree in range(2, self.count):
            values[..., degree] = (compact * values[..., degree - 1]
                                  - values[..., :degree] @ self.coefficients[degree, :degree]) / self.norms[degree]
        return values

    def derivative(self, frequency):
        frequency = np.asarray(frequency)
        values = self.evaluate(frequency)
        compact = (frequency - self.pivot) / (frequency + self.pivot)
        compact_prime = 2 * self.pivot / (frequency + self.pivot) ** 2
        derivatives = np.zeros_like(values)
        derivatives[..., 1] = 1 / self.norms[1]
        for degree in range(2, self.count):
            derivatives[..., degree] = (compact_prime * values[..., degree - 1] + compact * derivatives[..., degree - 1]
                                       - derivatives[..., :degree] @ self.coefficients[degree, :degree]) / self.norms[degree]
        return derivatives

    def project(self, values):
        return linalg.solve(self.mass, self.values.T @ (self.measure * values), assume_a='pos')


def load_basis(folder):
    packet = json.loads((Path(folder) / 'status.json').read_text())
    return StableBasis(packet['basis_count'], packet['quadrature_count'],
                       packet['minimum'], packet['maximum'], packet['pivot'])
