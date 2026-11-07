import hashlib
from outer_common import *
import population_common as population
from resolved_redistribution import incoming_rule


def population_nodes(theta, seed_order, hard_order=3, radial=2, polar=2, azimuthal=4):
    cosines, hard_weights = np.polynomial.legendre.leggauss(hard_order)
    index = 0
    for meridian, electron_measure in population.prior.inherited.inherited.gas_rule(theta, radial, polar):
        for phase in np.arange(azimuthal) * 2 * np.pi / azimuthal:
            velocity = np.array([meridian[0] * math.cos(phase), meridian[0] * math.sin(phase), meridian[2]])
            for frequency, seed_weight in incoming_rule(seed_order, 1e-5, 24.):
                for cosine, hard_weight in zip(cosines, hard_weights):
                    yield dict(index=index, frequency=float(frequency), seed_weight=float(seed_weight),
                        cosine=float(cosine), hard_weight=float(hard_weight), velocity=velocity.tolist(),
                        electron_weight=float(electron_measure / azimuthal))
                    index += 1


def node_key(identity):
    selected = {key: identity[key] for key in ['frequency', 'cosine', 'velocity']}
    return json.dumps(selected, sort_keys=True)


class LoopCache:
    def __init__(self):
        self.parent = BRANCH / 'population-matched-source-20261008'
        self.seal = json.loads((self.parent / 'results/stage-integrity.json').read_text())

    def get(self, parameters, order=2):
        identity = dict(lab_energy=parameters['lab_energy'], cosine=parameters['lab_cosine'],
            velocity=parameters['velocity'].tolist(), temperature=parameters['temperature'], order=order,
            script_sha256=digest(weak.source.__file__),
            stage88_sha256=digest(BRANCH / 'matched-weak-redistribution-20261008/results/stage-integrity.json'))
        key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
        existing = self.parent / 'virtual-cache' / (key + '.json')
        target = ROOT / 'virtual-cache' / key[:2] / (key + '.json')
        computed = False
        if existing.exists():
            assert digest(existing) == self.seal['file_hashes'][existing.relative_to(self.parent).as_posix()]
            path = existing
        elif target.exists():
            path = target
        else:
            tensor, response = weak.source.virtual_map(parameters, order)
            scalar = float(response[0, 0])
            assert np.isfinite(scalar)
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_suffix('.tmp')
            write_json(temporary, dict(identity=identity, scalar=scalar, finite=True))
            temporary.replace(target)
            path, computed = target, True
        saved = json.loads(path.read_text())
        assert saved['identity'] == identity and saved['finite']
        return saved['scalar'], path, computed
