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
PARENT=BRANCH/'colder-half-source-prediction-test-20261016'
sys.path.insert(0,str(PARENT))
import colder_common as prior_stage
from colder_common import *
ROOT=Path(__file__).resolve().parent
PARENT=BRANCH/'colder-half-source-prediction-test-20261016'
WARM=BRANCH/'independent-source-temperature-holdout-20261016'
PARENT_SEAL='1bbf1dd542613fdef6eaccc5f52b59eaad513465fc2d31740ba03e3f29bcd172'
STARTED=datetime(2026,10,16,13,35,45,tzinfo=timezone.utc)
INHERITED_PAYLOADS=246554
FRACTIONS={'start':.5,'warm':.5625,'centre':.625,'colder':.6875,'end':.75}
CASES={
    'start':dict(control=BRANCH/'frequency-aligned-control-20261009/runs/compact128-h3-g2-2-4',
                 expensive=BRANCH/'outer-population-source-20261008/runs/s4-h3-g2-2-4',
                 raw=BRANCH/'frequency-aligned-control-20261009/runs/compact128-h3-g2-2-4/source.npz',
                 control_nodes=6144,expensive_nodes=1344),
    'warm':dict(control=WARM/'runs/control-holdout',expensive=WARM/'runs/expensive-holdout',
                raw=WARM/'results/holdout-source/source.npz',control_nodes=4608,expensive_nodes=1008),
    'centre':dict(control=ANCHORS/'runs/control-centre',expensive=ANCHORS/'runs/expensive-centre',
                  raw=ANCHORS/'results/adjacent-sources/source.npz',prefix='centre_',control_nodes=4608,expensive_nodes=1008),
    'colder':dict(control=PARENT/'runs/control-colder',expensive=PARENT/'runs/expensive-colder',
                  raw=PARENT/'results/colder-source/source.npz',control_nodes=4608,expensive_nodes=1008),
    'end':dict(control=ANCHORS/'runs/control-end',expensive=ANCHORS/'runs/expensive-end',
               raw=ANCHORS/'results/adjacent-sources/source.npz',prefix='end_',control_nodes=4608,expensive_nodes=1008)
}


def ancestors():
    chain=prior_stage.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'stage146_precision_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',
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


def raw_components(case):
    spec=CASES[case]
    saved=read_npz(spec['raw'])
    prefix=spec.get('prefix','')
    return {key:saved[prefix+key] for key in COMPONENTS}
