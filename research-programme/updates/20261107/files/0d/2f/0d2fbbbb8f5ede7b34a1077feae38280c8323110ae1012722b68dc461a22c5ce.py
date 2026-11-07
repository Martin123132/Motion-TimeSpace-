import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
BRANCH,POST=ROOT.parent,ROOT.parent.parent
PARENT=BRANCH/'saved-event-precision-repair-20261016'
sys.path.insert(0,str(PARENT))
from stage146_precision_common import *
import stage146_precision_common as stage146_parent
ROOT=Path(__file__).resolve().parent
PARENT=BRANCH/'saved-event-precision-repair-20261016'
PARENT_SEAL='d7aff30c3ee570a4a195ef4457cf49d858294154d9e6249dea7cda5ed5e5d750'
STARTED=datetime(2026,10,16,16,10,17,tzinfo=timezone.utc)
INHERITED_PAYLOADS=246659
COUNTS=[1024,2048,4096]
GROUPS={'original':slice(0,2),'revised':slice(2,4),'increment':slice(4,6),
        'zero':slice(6,8),'old':slice(8,10),'combined_direct':slice(10,12)}


def ancestors():
    chain=stage146_parent.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'stage147_step_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',
           Path(script).resolve(),PARENT/'results/stage-integrity.json'}
    paths.update(Path(path).resolve() for path in extra)
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename:
            path=Path(filename).resolve()
            if path.suffix=='.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in sorted(paths)})
    report['count']=len(report['checks'])
    report['all_checks_passed']=all(bool(row['passed']) for row in report['checks'])
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def response_folder(model,count,phase):
    if count==1024:
        return PARENT/'results/response'/f'{model}-cubic'/phase
    return ROOT/'results/response'/f'{model}-{count}'/phase


def photon_norm(value,mass):
    return np.sqrt(np.maximum(np.einsum('...ik,ij,...jk->...k',value,mass,value),0.))
