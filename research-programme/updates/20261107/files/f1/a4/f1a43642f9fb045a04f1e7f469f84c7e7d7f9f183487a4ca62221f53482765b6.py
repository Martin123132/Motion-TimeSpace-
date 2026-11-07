from observer_common import *


class ExtendedLadder:
    def __init__(self, folder, basis):
        packet = json.loads((folder / 'status.json').read_text())
        assert packet['all_checks_passed']
        self.basis = basis
        self.temperatures = np.asarray(packet['temperatures'])
        self.inputs, self.blocks = [folder / 'status.json'], []
        for index in range(len(self.temperatures)):
            path = folder / ('planck-' + str(index) + '.npz')
            self.inputs.append(path)
            with np.load(path) as saved:
                self.blocks.append([saved['block_' + str(degree)].copy() for degree in range(9)])

    def at(self, theta, degree):
        assert self.temperatures[0] * (1 - 1e-9) <= theta <= self.temperatures[-1] * (1 + 1e-9)
        upper = int(np.clip(np.searchsorted(self.temperatures, theta), 1, len(self.temperatures) - 1))
        fraction = float(np.clip((theta - self.temperatures[upper - 1]) / (self.temperatures[upper] - self.temperatures[upper - 1]), 0., 1.))
        return (1 - fraction) * self.blocks[upper - 1][degree] + fraction * self.blocks[upper][degree]


class ExtendedBank:
    def __init__(self, folder, model):
        packet = json.loads((folder / 'status.json').read_text())
        assert packet['all_checks_passed']
        self.knots = np.asarray(packet['knots'])
        self.inputs = [folder / 'status.json']
        blocks, temperature, residual = [[] for degree in range(9)], [], []
        selected = 0 if model == 'heavy' else 1
        for index in range(len(self.knots)):
            path = folder / ('mixed-' + str(index) + '.npz')
            self.inputs.append(path)
            with np.load(path) as saved:
                for degree in range(9):
                    blocks[degree].append(saved['block_' + str(degree)][selected].copy())
                temperature.append(saved['temperature'][selected].copy())
                residual.append(saved['residual'][selected].copy())
        self.blocks = [interpolate.CubicSpline(self.knots, block) for block in blocks]
        self.temperature = interpolate.CubicSpline(self.knots, temperature)
        self.residual = interpolate.CubicSpline(self.knots, residual)


class ExtendedSystem(MixedSystem):
    def __init__(self, model, count=28, maximum=8, bank=None, stride=1):
        assert count >= 24 and stride == 1
        super().__init__(model, 24, maximum, 'fine16')
        self.count = count
        self.basis = StableBasis(count)
        folder = ROOT / 'banks' / ('basis' + str(count))
        self.ladder = ExtendedLadder(folder, self.basis)
        self.bank = ExtendedBank(folder, model)
        original_profile = self.geometry.profiles
        self.geometry.profiles = lambda expansion, derivative=0: np.pad(original_profile(expansion, derivative), (0, count - 24))
        self.geometry_basis = self.basis
        self.geometry.basis = self.basis
        vectors = np.column_stack([self.basis.chemical, self.basis.temperature])
        self.moment_lift = vectors @ linalg.inv(np.vstack([self.basis.number, self.basis.energy]) @ vectors)
        values, derivative = self.basis.values, self.basis.derivative(self.basis.nodes)
        self.redshift_weak = ((3 * values + self.basis.nodes[:, None] * derivative).T * self.basis.measure) @ values
        self.boost_weak = ((2 * values + self.basis.nodes[:, None] * derivative).T * self.basis.measure) @ values
        self.mass_inverse = linalg.inv(self.basis.mass)
        index = 11
        self.slices = []
        for names in self.names:
            self.slices.append(slice(index, index + count * len(names)))
            index += count * len(names)
        self.neutrino = slice(index, index + maximum + 1)
        self.size = self.neutrino.stop
        self.density_row = np.zeros(self.size, complex)
        self.density_row[[0, 1, 8]] = [-1., -.5, 1.]
