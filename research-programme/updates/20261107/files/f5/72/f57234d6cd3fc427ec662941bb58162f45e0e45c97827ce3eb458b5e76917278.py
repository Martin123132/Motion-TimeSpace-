import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
import sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'endpoint-state-precision-20261019'))
from stage165_common import *
import stage165_common as parent165
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/'endpoint-state-precision-20261019'
PARENT_SEAL='f58ea535fc44c0ac54dae7edcd0e658dcac46051acb37d01b02012c3d6db6d8e'
INHERITED_PAYLOADS=332509
STARTED=datetime(2026,10,19,15,45,40,tzinfo=timezone.utc)
DEADLINE='2026-10-19T19:15:00+00:00'


def ancestors():
    chain=parent165.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'stage166_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
    paths.update(Path(path).resolve() for path in extra)
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename:
            path=Path(filename).resolve()
            if path.suffix=='.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),input_hashes={str(path):digest(path) for path in sorted(paths)})
    report['count']=len(report['checks'])
    report['all_checks_passed']=all(bool(row['passed']) for row in report['checks'])
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')
