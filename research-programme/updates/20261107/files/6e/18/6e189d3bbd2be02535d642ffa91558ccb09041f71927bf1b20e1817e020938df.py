from common223 import *
import replay223
import tail223

def prepare_pipeline():
    protocol()
    path=ROOT/'continuation-configuration.json'
    assert not path.exists()
    write(path,dict(frozen_at=now(),hashes={name:digest(ROOT/name) for name in ('continue223.py','replay223.py','tail223.py','assess223.py','TAIL-DERIVATION.md')},
        continuation='Only after short-window assessment passes; independent midpoint restart, then direct coupled final-epoch propagation',
        stop_at='2026-10-26T14:20:00+00:00'))

def run(model,deadline):
    protocol()
    frozen=read(ROOT/'continuation-configuration.json')
    for name,value in frozen['hashes'].items():
        assert digest(ROOT/name)==value,name
    assert read(ROOT/'results/window-assessment.json')['qualified']
    for count in COUNTS:
        if datetime.now(timezone.utc)>=deadline:
            return
        replay223.replay(model,count)
        assert not read(ROOT/f'restart-check/{model}-{count}/complete.json')['failed_checks']
    for count in (4096,2048):
        if datetime.now(timezone.utc)>=deadline:
            return
        tail223.run_case(model,count,deadline)
        if not (ROOT/f'tail/{model}-{count}/complete.json').exists():
            return

if __name__=='__main__':
    old.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','run'])
    parser.add_argument('--model',choices=MODELS)
    parser.add_argument('--stop-at',default='2026-10-26T14:20:00+00:00')
    args=parser.parse_args()
    if args.phase=='prepare':
        prepare_pipeline()
    else:
        run(args.model,datetime.fromisoformat(args.stop_at))

