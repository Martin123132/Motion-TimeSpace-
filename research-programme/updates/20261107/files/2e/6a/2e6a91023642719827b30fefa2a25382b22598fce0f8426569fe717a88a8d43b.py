import argparse
from observer_common import *
from consistent_system import ConsistentSystem
import run_mixed_waves as engine


def local_finish(folder, report, script, extra):
    mapped = [PARENT / path.name if path.parent == ROOT and path.name in ['mixed_wave_system.py', 'stable_pair.py'] else path for path in extra]
    report.update(refinement_of='Same physical equations and24-function background; construction-consistent basis evaluation.', no_new_physical_parameters=True)
    finish(folder, report, __file__, [Path(script), ROOT / 'extended_system.py', ROOT / 'consistent_system.py',
                                    ROOT / 'consistent_spectral_basis.py', *mapped])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, choices=['heavy', 'cold'])
    parser.add_argument('--count', type=int, default=32)
    parser.add_argument('--steps', type=int, default=3200)
    arguments = parser.parse_args()
    arguments.name = arguments.model + str(arguments.count) + '-' + str(arguments.steps)
    arguments.maximum, arguments.bank, arguments.stride, arguments.include_residual = 8, None, 1, False
    engine.ROOT = ROOT
    engine.MixedSystem = ConsistentSystem
    engine.finish = local_finish
    engine.main(arguments)
