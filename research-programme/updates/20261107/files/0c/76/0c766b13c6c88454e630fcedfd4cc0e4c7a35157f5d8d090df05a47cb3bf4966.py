from thermal_wave_common import *
from stable_spectral_basis import load_basis


class KernelLadder:
    def __init__(self, count=16):
        self.folders = [ROOT / 'banks' / ('stable' + str(count) + '-late')]
        self.folders += [ROOT / 'banks' / ('stable' + str(count) + '-t' + str(index)) for index in range(1, 9)]
        self.basis = load_basis(self.folders[0])
        self.blocks, self.temperatures, self.inputs = [], [], []
        for folder in self.folders:
            report = json.loads((folder / 'status.json').read_text())
            assert report['all_checks_passed']
            assert report['basis_count'] == count
            self.temperatures.append(report['theta'])
            self.inputs.append(folder / 'status.json')
            blocks = []
            for degree in range(9):
                path = folder / ('block-' + str(degree) + '.npz')
                with np.load(path) as data:
                    blocks.append(data['stiffness'])
                    assert np.max(abs(data['mass'] - self.basis.mass / (2 * degree + 1))) < 1e-12
                self.inputs.append(path)
            self.blocks.append(blocks)
        self.temperatures = np.array(self.temperatures)

    def at(self, theta, degree):
        assert self.temperatures[0] * (1 - 1e-9) <= theta <= self.temperatures[-1] * (1 + 1e-9), theta
        upper = int(np.clip(np.searchsorted(self.temperatures, theta), 1, len(self.temperatures) - 1))
        fraction = float(np.clip((theta - self.temperatures[upper - 1]) / (self.temperatures[upper] - self.temperatures[upper - 1]), 0., 1.))
        return (1 - fraction) * self.blocks[upper - 1][degree] + fraction * self.blocks[upper][degree]
