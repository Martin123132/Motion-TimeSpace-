from emission_rates import *


class GauntTable:
    def __init__(self, path, atomic_number=None):
        self.path = Path(path)
        rows = [line.split('#', 1)[0].strip() for line in self.path.read_text().splitlines()]
        rows = [line for line in rows if line]
        magic = int(rows[0])
        assert magic in [20140210, 20140510]
        self.columns, self.rows = map(int, rows[1].split())
        self.gamma_start, self.u_start, self.step = map(float, rows[2:5])
        offset = 5
        if magic == 20140510:
            assert int(rows[5]) == atomic_number
            offset = 6
        self.values = np.array([list(map(float, line.split())) for line in rows[offset:offset + self.rows]])
        assert self.values.shape == (self.rows, self.columns)
        assert np.isfinite(self.values).all() and np.min(self.values) > 0

    def __call__(self, gamma_squared, frequency):
        gamma, frequency = np.broadcast_arrays(np.log10(gamma_squared), np.log10(frequency))
        gamma = (gamma - self.gamma_start) / self.step
        frequency = (frequency - self.u_start) / self.step
        if np.any(gamma < 0) or np.any(gamma > self.columns - 1) or np.any(frequency < 0) or np.any(frequency > self.rows - 1):
            raise ValueError('Gaunt table extrapolation is not permitted')
        gamma_index = np.clip(np.floor(gamma).astype(int) - 1, 0, self.columns - 4)
        frequency_index = np.clip(np.floor(frequency).astype(int) - 1, 0, self.rows - 4)
        output = np.zeros_like(frequency)
        for column in range(4):
            gamma_weight = np.ones_like(gamma)
            for other in range(4):
                if other != column:
                    gamma_weight *= (gamma - gamma_index - other) / (column - other)
            for row in range(4):
                frequency_weight = np.ones_like(frequency)
                for other in range(4):
                    if other != row:
                        frequency_weight *= (frequency - frequency_index - other) / (row - other)
                output += gamma_weight * frequency_weight * self.values[frequency_index + row, gamma_index + column]
        assert np.isfinite(output).all() and np.min(output) > 0
        return output


class SourcedEmission(EmissionMatrices):
    def __init__(self, basis, background, quadrature=900, temperature_knots=81, nonrelativistic=False):
        super().__init__(basis, quadrature)
        self.background = background
        self.tables = [GauntTable(ROOT / 'sources' / ('gauntff.dat' if nonrelativistic else 'gauntff_merged_Z0' + str(charge) + '.dat'), charge)
                       for charge in [1, 2]]
        self.inputs = list({table.path for table in self.tables})
        self.temperatures = np.geomspace(background.theta0 / background.end_scale, background.theta0 / background.start_scale, temperature_knots)
        self.br_blocks = np.array([self.br_matrix(theta) for theta in self.temperatures])
        self.interpolator = interpolate.CubicSpline(np.log(self.temperatures), self.br_blocks, axis=0, extrapolate=False)

    def br_rates(self, theta):
        constants = self.background.constants
        compton_wavelength = 6.62607015e-34 / (constants['m_e'] * constants['c'])
        helium_number = self.background.helium_fraction / (1 - self.background.helium_fraction) * constants['m_H'] / constants['m_He4']
        scale = self.background.theta0 / theta
        hydrogen = self.background.electron0 / scale ** 3 / (1 + 2 * helium_number)
        gaunt_h = self.tables[0](ALPHA ** 2 / (2 * theta), self.frequency)
        gaunt_he = self.tables[1](4 * ALPHA ** 2 / (2 * theta), self.frequency)
        coefficient = ALPHA * compton_wavelength ** 3 / (2 * math.pi * math.sqrt(6 * math.pi)) * theta ** (-3.5)
        return coefficient * hydrogen * (gaunt_h + 4 * helium_number * gaunt_he) * (-np.expm1(-self.frequency)) / self.frequency ** 3

    def br_matrix(self, theta):
        return (self.values.T * (self.measure * self.br_rates(theta))) @ self.values

    def at(self, theta, variant):
        if variant in ['none', 'soft', 'dc']:
            return super().at(theta, variant)
        if variant not in ['dcbr', 'dcbrnr']:
            raise ValueError(variant)
        coordinate = float(np.clip(np.log(theta), np.log(self.temperatures[0]), np.log(self.temperatures[-1])))
        assert abs(coordinate - np.log(theta)) < 1e-12
        return super().at(theta, 'dc') + self.interpolator(coordinate)
