import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'endpoint-moment-repair-20261019'))
from stage163_common import *
import stage163_common as parent163
from probe_correlated_soft import CorrelatedSoft
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/'endpoint-moment-repair-20261019'
PARENT_SEAL='ad7e0e227042f3bf36f325487700e4b17cd1c5c9d9e9562b1cb01453a0e93312'
INHERITED_PAYLOADS=316585
STARTED=datetime(2026,10,19,3,11,0,tzinfo=timezone.utc)
DEADLINE='2026-10-19T06:45:00+00:00'
SOURCE162=BRANCH/'endpoint-anchor-integration-20261018'


def ancestors():
    chain=parent163.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'stage164_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),
        PARENT/'results/stage-integrity.json'}
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
