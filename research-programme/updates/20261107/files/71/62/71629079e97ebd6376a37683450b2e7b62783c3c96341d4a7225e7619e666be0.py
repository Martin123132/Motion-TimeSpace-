import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
import sys
from pathlib import Path
sys.dont_write_bytecode=True
BRANCH=Path('D:/Users/ollet/Desktop/Turn an intuitive research programme into a formal field-theoretic framework/Motion-TimeSpace--main/post-checkpoint-work/condensate-origin-20261003')
sys.path.insert(0,str(BRANCH/'endpoint-twofold-response-20261019'))
from stage166_common import *
import stage166_common as parent166
ROOT=Path(__file__).resolve().parent
PARENT=BRANCH/'endpoint-twofold-response-20261019'
PARENT_SEAL='c73316e28d443595a53a9f3c92874c61a069507bfe11c76d4ed8a61fc50c8559'
INHERITED_PAYLOADS=332701
STARTED=datetime(2026,10,19,16,30,22,tzinfo=timezone.utc)
BAND_SOURCES={
    'incoming13_last':('incoming-band13-order8-20261018',''),
    'incoming38_last':('targeted-frequency-band-refinement-20261018','-band4'),
    'incoming820_last':('incoming-band820-order7-20261018','')}
METRICS=['temperature_shift','mu','y','residual_norm','distortion_norm','potential_norm']
SCALAR_KEYS=['eta_standard','amplitudes']
VECTOR_KEYS=['potential','distortion','residual']


def ancestors():
    chain=parent166.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def norm(values,measure):
    return np.sqrt(np.sum(measure[:,None]*values**2,axis=0))


def metrics(split,heat,measure):
    return np.vstack([heat*split['eta_standard'],heat*split['amplitudes'],
        abs(heat)*norm(split['residual'],measure),abs(heat)*norm(split['distortion'],measure),
        abs(heat)*norm(split['potential'],measure)])


def finish(folder,report,inputs):
    paths={*ROOT.glob('*.py'),ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',PARENT/'results/stage-integrity.json'}
    paths.update(Path(path).resolve() for path in inputs)
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename and Path(filename).suffix=='.py' and Path(filename).resolve().is_relative_to(BRANCH):
            paths.add(Path(filename).resolve())
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        input_hashes={str(path):digest(path) for path in sorted(paths)},count=len(report['checks']),
        all_checks_passed=all(bool(row['passed']) for row in report['checks']))
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def get_terminal(path):
    result={}
    with np.load(path,allow_pickle=False) as archive:
        for key in ['photon','energy','photon_high','photon_low','energy_high','energy_low']:
            result[key]=archive[key][-1].copy()
    return result


def checked_readout(path,reader,inputs,checks):
    saved=read_npz(path)
    inputs.append(path)
    assert np.array_equal(saved['frequency'],reader.frequency)
    assert np.array_equal(saved['measure'],reader.measure)
    split=reader.split_values(saved['potential'],saved['energy'])
    for key in ['amplitudes','residual','eta_standard']:
        close(checks,'Reproject saved '+key+':'+path.parent.parent.parent.name+':'+path.stem,split[key],saved[key],1e-10)
    return saved
