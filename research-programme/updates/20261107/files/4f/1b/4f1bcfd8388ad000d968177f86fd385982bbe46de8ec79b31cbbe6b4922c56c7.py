import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import inspect,re
ROOT=Path(__file__).resolve().parent
BRANCH,POST=ROOT.parent,ROOT.parent.parent
PARENT=BRANCH/'downstream-window-transfer-20261012'
sys.path.insert(0,str(PARENT))
import window_transfer_common as inherited
from window_transfer_common import np,math,json,linalg,special,thermal_wave,infrared_ladder
digest,write_json,modest=inherited.digest,inherited.write_json,inherited.modest
STARTED=datetime(2026,10,12,17,11,56,tzinfo=timezone.utc)
PARENT_SEAL='6aa1cd2ba7227c2210709ec112633695e020a91ef2747fb0169133db76f2341a'
SOURCE_DOCS=[BRANCH/path for path in [
    'emitting-thermal-background-20261008/DERIVATION.md',
    'population-matched-source-20261008/DERIVATION.md',
    'emitting-thermal-background-20261008/evolve_emitting_background.py',
    'infrared-source-domain-20261008/evolve_nonlocal_background.py',
    'observer-frequency-projection-20261007/consistent_spectral_basis.py',
    'expanding-thermal-gravity-20261007/thermal_wave_common.py',
    'thermal-recoil-and-spectral-response-20261007/thermal_common.py',
    'native-heavy-matching-20261007/native/fortran/constants.f90']]
URLS=['https://academic.oup.com/mnras/article/466/2/2390/2669327',
      'https://doi.org/10.1093/mnras/stw3230',
      'https://academic.oup.com/mnras/article/535/2/1874/7853135',
      'https://doi.org/10.1093/mnras/stae2464']


def ancestors():
    chain=inherited.sealed_ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'projection_common.py',ROOT/'ACCEPTANCE.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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


def norm(value,mass):
    return np.sqrt(np.maximum(np.einsum('ik,ij,jk->k',value,mass,value),0.))


def read_final(model,label):
    path=PARENT/'results/window-transfer'/f'{model}-{label}.npz'
    with np.load(path) as saved:
        state={key:saved[key][-1].copy() for key in saved.files if key!='coordinate'}
        state['coordinate']=float(saved['coordinate'][-1])
    return state,path


def decompose(photon,energy,basis):
    capacity=float(basis.energy@basis.temperature)
    eta=energy/capacity
    temperature=basis.temperature[:,None]*eta
    return dict(photon=photon,energy=energy,eta=eta,temperature=temperature,
        distortion=photon-temperature)

