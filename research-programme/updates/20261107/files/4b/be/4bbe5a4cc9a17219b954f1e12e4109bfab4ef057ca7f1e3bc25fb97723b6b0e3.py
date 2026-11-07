import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'endpoint-anchor-integration-20261018'))
from stage162_common import *
import stage162_common as parent162
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/'endpoint-anchor-integration-20261018'
PARENT_SEAL='b58d962f589def96b807be5b008c67d1da3fed6860c42c4b577c76db8665e042'
INHERITED_PAYLOADS=308908
STARTED=datetime(2026,10,19,1,47,2,tzinfo=timezone.utc)
DEADLINE='2026-10-19T05:25:00+00:00'
READOUT_OWNER=BRANCH/'incoming-band820-order7-20261018'


def ancestors():
    chain=parent162.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'stage163_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',
        Path(script).resolve(),PARENT/'results/stage-integrity.json'}
    paths.update(Path(path).resolve() for path in extra)
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename:
            path=Path(filename).resolve()
            if path.suffix=='.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        input_hashes={str(path):digest(path) for path in sorted(paths)})
    report['count']=len(report['checks'])
    report['all_checks_passed']=all(bool(row['passed']) for row in report['checks'])
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def moment_path(endpoint,order,index):
    return ROOT/'runs'/endpoint/f'order{order}'/'nodes'/f'{index//500:03d}'/f'{index:05d}.npz'


def low_rows(primitive,basis):
    photon,number,gas=primitive
    return np.stack([photon,number/basis.norms[0],(photon-basis.mean*number)/basis.norms[1],gas])
