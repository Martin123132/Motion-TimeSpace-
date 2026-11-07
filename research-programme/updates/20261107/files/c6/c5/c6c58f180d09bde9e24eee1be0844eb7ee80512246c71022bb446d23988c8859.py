import argparse
from observer_common import *
from consistent_spectral_basis import ConsistentBasis
import build_frequency_refinement as engine


def local_finish(folder, report, script, extra):
    report.update(basis_evaluation='Two-pass construction-consistent evaluation; same native basis and moment quadrature.')
    finish(folder, report, __file__, [Path(script), ROOT / 'consistent_spectral_basis.py',
                                    ROOT / 'results/consistent-basis/status.json', *extra])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=32)
    arguments = parser.parse_args()
    assert json.loads((ROOT / 'results/consistent-basis/status.json').read_text())['all_checks_passed']
    engine.StableBasis = ConsistentBasis
    engine.finish = local_finish
    engine.main(arguments)
