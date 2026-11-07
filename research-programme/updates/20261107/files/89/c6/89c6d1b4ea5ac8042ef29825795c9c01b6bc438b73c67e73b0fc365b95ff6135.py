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
PARENT=BRANCH/'seven-eighths-history-cubic-carry-20261015'
P139=BRANCH/'three-quarter-history-cubic-carry-20261015'
P138=BRANCH/'beyond-midpoint-cubic-carry-20261014'
P137=BRANCH/'half-history-cubic-carry-20261014'
P136=BRANCH/'next-eight-intervals-20261014'
P135=BRANCH/'quarter-history-cubic-carry-20261014'
P134=BRANCH/'extended-cubic-history-20261014'
P133=BRANCH/'continuous-cubic-carry-20261014'
sys.path.insert(0,str(PARENT))
import seven_eighths_history_common as inherited
from seven_eighths_history_common import np,math,json,linalg,interpolate,digest,write_json,modest,thermal_wave,infrared_ladder,read_npz,NonlocalEmission,compact_defect,local_packet,check,I3,norm,refined_owner,photon_norm,sparse,sparse_linalg,FreeFree,load_histories,make_drivers,stable_adjoint,deposit_cubic,pair_cubic,symbol_bound,tail
P132=BRANCH/'cubic-adjoint-inner-correction-20261014'
PARENT_SEAL='d1e971752f8f245a33f16e207118eb39b8f7f6ebef91de84963b67f848e30503'
STARTED=datetime(2026,10,15,17,19,10,tzinfo=timezone.utc)
FIRST_STEP,LAST_STEP=35840,40960
SOURCE_STEPS=np.arange(FIRST_STEP,LAST_STEP+1,20)


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def verify_source(path,chain):
    inherited.verify_source(Path(path),chain)


def finish(folder,report,script,extra=()):
    paths={ROOT/'complete_history_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
    paths.update(Path(path).resolve() for path in extra)
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename:
            path=Path(filename).resolve()
            if path.suffix=='.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),script_sha256=digest(script),
        input_hashes={str(path):digest(path) for path in sorted(paths)})
    report['count']=len(report['checks'])
    report['all_checks_passed']=all(bool(row['passed']) for row in report['checks'])
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def event_path(step):
    if step%640==0:
        return BRANCH/'direct-doppler-compton-feedback-20261012/results/bank-o6-q32-m40'/f'epoch-{step//640:02d}.npz'
    return ROOT/'results/coefficients'/f'event-{step:05d}.npz'
