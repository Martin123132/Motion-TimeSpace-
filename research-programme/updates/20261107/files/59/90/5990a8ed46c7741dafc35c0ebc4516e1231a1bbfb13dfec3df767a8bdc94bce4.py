from response221 import *


class OutputReadout(matched.saved.response.ShapeReadout):
    def apply(self,photon,energy=None):
        values=super().apply(photon,energy)
        assert energy is not None and np.array_equal(values['energy'],energy)
        values.pop('energy')
        return values


def freeze_adapter():
    protocol()
    path=ROOT/'readout-output-contract.json'
    assert not path.exists()
    write(path,dict(frozen_at=now(),script_sha256=digest(ROOT/'evolve221.py'),
        original_runner_sha256=digest(ROOT/'response221.py'),
        reason='ShapeReadout.apply already supplies energy, while the frozen output call also supplies the identical energy keyword.',
        change='Remove only the duplicate output dictionary key; assert exact equality before removal.',
        equations_changed=False,source_changed=False,tolerances_changed=False))


def run_adapter(model,count):
    protocol();contract=read(ROOT/'readout-output-contract.json')
    assert digest(ROOT/'evolve221.py')==contract['script_sha256']
    assert digest(ROOT/'response221.py')==contract['original_runner_sha256']
    previous=matched.saved.response.ShapeReadout
    try:
        matched.saved.response.ShapeReadout=OutputReadout
        evolve(model,count)
    finally:
        matched.saved.response.ShapeReadout=previous


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['freeze','run'])
    parser.add_argument('--model',choices=MODELS)
    parser.add_argument('--count',type=int,choices=[2048,4096])
    args=parser.parse_args()
    if args.phase=='freeze':
        freeze_adapter()
    else:
        run_adapter(args.model,args.count)
