import argparse
from types import SimpleNamespace
from wave_common import *
from infrared_ladder import InfraredLadder
import density_tangent as engine


def main(arguments):
    modest()
    bank = ROOT / 'banks' / arguments.bank
    if not bank.exists():
        bank = PARENT / 'banks' / arguments.bank
    ladder = InfraredLadder(bank)
    engine.InfraredLadder = lambda ignored_path: ladder
    def local_finish(folder, report, script, extra):
        report.update(basis_spec=ladder.specification, bank=str(bank), basis_refinement=True)
        finish(folder, report, __file__, [Path(script), *extra])
    engine.finish = local_finish
    for model in ['heavy', 'cold']:
        engine.main(SimpleNamespace(model=model, steps=6400, offset=0., omit_ion=False,
                                    name=model + '-tangent' + str(ladder.basis.count) + '-6400'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bank', required=True)
    main(parser.parse_args())
