from emission_common import *


def scalar_physical_block(basis, theta, events):
    stiffness = np.zeros_like(basis.mass)
    discarded, total = 0., 0.
    for frequency, measure, initial in zip(basis.nodes, basis.measure / 2, basis.values):
        ratio = 1 / (1 + theta * frequency * events['incident'] * (1 - events['cosine']))
        extra = (1 - ratio) ** 2 / ratio
        final = frequency * events['incident'] * ratio * events['outgoing']
        bose = (1 + 1 / np.expm1(final)) / (1 + 1 / np.expm1(frequency))
        conductance = measure * events['weight'] * 1.5 * ratio ** 2 * bose * (1 + events['cosine'] ** 2 + extra)
        inside = (final >= basis.minimum) & (final <= basis.maximum)
        discarded += float(np.sum(conductance[~inside]))
        total += float(np.sum(conductance))
        difference = initial[None, :] - basis.evaluate(final[inside])
        stiffness -= .5 * (difference.T * conductance[inside]) @ difference
    return stiffness, discarded / total


class InfraredLadder:
    def __init__(self, folder):
        report = json.loads((folder / 'status.json').read_text())
        assert report['all_checks_passed']
        self.specification = report['basis_spec']
        self.basis = ConsistentBasis(**self.specification)
        self.inputs = [folder / 'status.json']
        self.temperatures = np.array(report['temperatures'])
        self.blocks = []
        for index in range(len(self.temperatures)):
            path = folder / ('planck-' + str(index) + '.npz')
            self.inputs.append(path)
            with np.load(path) as saved:
                self.blocks.append(saved['stiffness'].copy())

    def at(self, theta, degree):
        assert degree == 0
        assert self.temperatures[0] * (1 - 1e-9) <= theta <= self.temperatures[-1] * (1 + 1e-9)
        upper = int(np.clip(np.searchsorted(self.temperatures, theta), 1, len(self.temperatures) - 1))
        fraction = float(np.clip((theta - self.temperatures[upper - 1]) / (self.temperatures[upper] - self.temperatures[upper - 1]), 0., 1.))
        return (1 - fraction) * self.blocks[upper - 1] + fraction * self.blocks[upper]
