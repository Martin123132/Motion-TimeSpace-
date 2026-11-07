import argparse
from infrared_ladder import *
import evolve_emitting_background as engine


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bank', required=True)
    parser.add_argument('--model', choices=['heavy', 'cold'], required=True)
    parser.add_argument('--steps', type=int, default=3200)
    parser.add_argument('--quadrature', type=int, default=900)
    parser.add_argument('--emission', choices=['none', 'soft', 'dc'], default='dc')
    parser.add_argument('--name', required=True)
    arguments = parser.parse_args()
    ladder = InfraredLadder(ROOT / 'banks' / arguments.bank)
    arguments.count = ladder.basis.count
    engine.ConsistentBasis = lambda count: ladder.basis
    engine.ExtendedLadder = lambda folder, basis: ladder
    def local_finish(folder, report, script, extra):
        report.update(basis_spec=ladder.specification, bank=arguments.bank)
        finish(folder, report, __file__, [Path(script), ROOT / 'infrared_ladder.py', *extra])
    engine.finish = local_finish
    engine.main(arguments)
