import hashlib
import project_population as runner
from population_common import *


def sharded_cache(parameters, order):
    identity = dict(lab_energy=parameters['lab_energy'], cosine=parameters['lab_cosine'],
                    velocity=parameters['velocity'].tolist(), temperature=parameters['temperature'], order=order,
                    script_sha256=digest(weak.source.__file__), stage88_sha256=digest(MATCHED / 'results/stage-integrity.json'))
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    flat = ROOT / 'virtual-cache' / (key + '.json')
    path = ROOT / 'virtual-cache' / key[:2] / (key + '.json')
    existing = flat if flat.is_file() else path
    if existing.is_file():
        saved = json.loads(existing.read_text())
        assert saved['identity'] == identity
        return saved['scalar'], existing, False
    tensor, response = weak.source.virtual_map(parameters, order)
    scalar = float(response[0, 0])
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    write_json(temporary, dict(identity=identity, scalar=scalar, finite=bool(np.isfinite(scalar))))
    temporary.replace(path)
    return scalar, path, True


if __name__ == '__main__':
    runner.source_cache = sharded_cache
    runner.main()
