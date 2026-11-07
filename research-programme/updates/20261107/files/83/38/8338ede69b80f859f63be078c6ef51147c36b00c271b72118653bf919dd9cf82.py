from types import SimpleNamespace
from density_tangent import main
from wave_common import *


def run():
    modest()
    jobs = []
    for model in ['heavy', 'cold']:
        jobs.append(dict(model=model, name=model + '-tangent-6400', offset=0., steps=6400, omit_ion=False))
        jobs.append(dict(model=model, name=model + '-tangent-3200', offset=0., steps=3200, omit_ion=False))
        jobs.append(dict(model=model, name=model + '-omit-ion-6400', offset=0., steps=6400, omit_ion=True))
        for offset in [-.002, -.001, .001, .002]:
            label = ('plus-' if offset > 0 else 'minus-') + str(abs(offset))
            jobs.append(dict(model=model, name=model + '-' + label + '-6400', offset=offset, steps=6400, omit_ion=False))
    for job in jobs:
        folder = ROOT / 'density' / job['name']
        if (folder / 'COMPLETE').exists():
            packet = json.loads((folder / 'status.json').read_text())
            assert packet['all_checks_passed']
            for path, expected in packet['input_hashes'].items():
                assert digest(path) == expected
            continue
        assert not folder.exists(), str(folder)
        main(SimpleNamespace(**job))


if __name__ == '__main__':
    run()
