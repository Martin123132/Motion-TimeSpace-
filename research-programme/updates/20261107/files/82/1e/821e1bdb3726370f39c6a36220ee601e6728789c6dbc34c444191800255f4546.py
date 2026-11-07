from common225 import *
from types import SimpleNamespace
import gravity225 as original

def shifted_forward(background,name,first,last):
    span=last-first
    def local_rhs(local_coordinate,values):
        parts=model_parts(background,first+local_coordinate)
        supplied=original.probe(name,local_coordinate,0.,span)[0]
        return parts['operator']@values+parts['forcing']*supplied
    solved=integrate.solve_ivp(local_rhs,(0.,span),np.zeros(4),method='DOP853',rtol=3e-11,atol=1e-40,
        max_step=.005,dense_output=True)
    assert solved.success,dict(probe=name,message=solved.message,coordinate=float(solved.t[-1]))
    adapter=SimpleNamespace(sol=lambda coordinate:solved.sol(np.asarray(coordinate)-first))
    global_rhs=lambda coordinate,values:local_rhs(coordinate-first,values)
    return adapter,global_rhs

def prepare_repair():
    protocol()
    path=ROOT/'coordinate-repair.json'
    assert not path.exists()
    write(path,dict(frozen_at=now(),original_protocol_sha256=digest(ROOT/'configuration.json'),
        hashes={name:digest(ROOT/name) for name in ('gravity_shifted225.py','gravity225.py','common225.py','COORDINATE-REPAIR.md',
            'results/original-probe-diagnosis.json')},representation='local integration coordinate only; no state scaling or tolerance changes'))
    write(ROOT/'shifted-coordinate/inputs.json',read(ROOT/'inputs.json'))

def run_repair():
    protocol()
    frozen=read(ROOT/'coordinate-repair.json')
    assert digest(ROOT/'configuration.json')==frozen['original_protocol_sha256']
    for name,value in frozen['hashes'].items():
        assert digest(ROOT/name)==value,name
    child=ROOT/'shifted-coordinate'
    assert not (child/'results/gravity.json').exists()
    original.forward=shifted_forward
    original.ROOT=child
    original.run()
    report=read(child/'results/gravity.json')
    report.update(selected_source=str(child/'results/gravity.json'),selected_source_sha256=digest(child/'results/gravity.json'),
        coordinate_repair=str(ROOT/'coordinate-repair.json'),original_probe_failure_preserved=True)
    write(ROOT/'results/gravity.json',report)
    inputs=read(child/'inputs-gravity.json')
    for path in (ROOT/'gravity_shifted225.py',ROOT/'coordinate-repair.json',ROOT/'COORDINATE-REPAIR.md',child/'results/gravity.json'):
        register(inputs,path)
    write(ROOT/'inputs-gravity.json',inputs)

if __name__=='__main__':
    parent.old.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','run'])
    args=parser.parse_args()
    prepare_repair() if args.phase=='prepare' else run_repair()
