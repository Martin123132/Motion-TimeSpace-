from types import SimpleNamespace
from wave_common import *
from infrared_ladder import InfraredLadder
import density_tangent as engine


def main():
    modest()
    ladder = InfraredLadder(PARENT / 'banks/infrared88-q700')
    engine.InfraredLadder = lambda ignored_path: ladder
    def local_finish(folder, report, script, extra):
        report.update(basis_spec=ladder.specification, basis_refinement=True)
        finish(folder, report, __file__, [Path(script), *extra])
    engine.finish = local_finish
    for model in ['heavy', 'cold']:
        engine.main(SimpleNamespace(model=model, steps=6400, offset=0., omit_ion=False,
                                    name=model + '-tangent88-6400'))


if __name__ == '__main__':
    main()
