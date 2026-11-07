import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'incoming-band13-order8-20261018'
sys.path.insert(0,str(PARENT))
from stage159_common import *
import stage159_common as parent159
ROOT=Path(__file__).resolve().parent
PARENT=BRANCH/'incoming-band13-order8-20261018'
SOURCE158=BRANCH/'targeted-frequency-band-refinement-20261018'
SOURCE157=BRANCH/'virtual-frequency-cancellation-20261018'
SOURCE156=BRANCH/'matched-cubic-uncertainty-separation-20261018'
PARENT_SEAL='5abea977c4858f38da0a1afedfc95a6600ceaba75b5b2ec8f73298a30b366357'
STARTED=datetime(2026,10,18,19,22,0,tzinfo=timezone.utc)
INHERITED_PAYLOADS=296279
SHAPE_CUTOFFS=[1e-8,1e-10,1e-12]
THRESHOLD=.01
QUANTITIES=['photon','gas','energy','work','number','integrated_number_source']


def ancestors():
    chain=parent159.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'stage160_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve()}
    paths.update(Path(path).resolve() for path in extra)
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename:
            path=Path(filename).resolve()
            if path.suffix=='.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        input_hashes={str(path):digest(path) for path in sorted(paths)},checks=report['checks'])
    report['count']=len(report['checks'])
    report['all_checks_passed']=all(bool(row['passed']) for row in report['checks'])
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


class Registry:
    def __init__(self):
        self.chain=ancestors()
        assert sum(len(packet['file_hashes']) for packet in self.chain.values())==INHERITED_PAYLOADS
        self.hashes={}

    def add(self,path):
        path=Path(path).resolve()
        key=str(path)
        if key in self.hashes:
            return
        actual=digest(path)
        if path in self.chain:
            assert json.loads(path.read_text())==self.chain[path]
        else:
            found=False
            for parent in path.parents:
                seal=parent/'results/stage-integrity.json'
                if seal in self.chain:
                    expected=self.chain[seal]['file_hashes'][path.relative_to(parent).as_posix()]
                    assert actual==expected,path
                    found=True
                    break
            assert found,path
        self.hashes[key]=actual

    def read(self,path):
        self.add(path)
        return read_npz(path)


class SourceNorm:
    def __init__(self,mass):
        self.mass=mass
        self.factor=np.linalg.cholesky(mass)

    def whiten(self,value):
        value=np.asarray(value)
        spectral=value[...,1:-1,:]
        shape=spectral.shape
        flat=np.moveaxis(spectral,-2,0).reshape(96,-1)
        solved=np.linalg.solve(self.factor,flat)
        return np.moveaxis(solved.reshape((96,)+shape[:-2]+(shape[-1],)),0,-2)

    def __call__(self,value):
        return np.linalg.norm(self.whiten(value),axis=-2)


def conditional_radius(error,cold,numerator_radius,cold_radius):
    return dict(numerator_radius=numerator_radius.tolist(),cold_radius=cold_radius.tolist(),
        lower_relative=(np.maximum(error-numerator_radius,0)/(cold+cold_radius)).tolist(),
        extra_numerator_allowance_for1percent=(error-numerator_radius-THRESHOLD*(cold+cold_radius)).tolist(),
        certified=False,endpoint_and_other_axis_radius=None)


def weights_for(route):
    return np.asarray([1.,-source155.predictor_basis(.75,route,'warm'),
        -source155.predictor_basis(.75,route,'centre')])


def latest_prediction(data,route):
    original=np.asarray([parent159.parent158.original_full(data,site) for site in SITES])
    shifts=data['after_order8_full']-original
    return data[route+'_diagnostic_prediction6']+sum(
        source155.predictor_basis(.75,route,site)*shifts[SITES.index(site)] for site in ['warm','centre'])


def full_component(data,site,order,component):
    return data[('' if site=='cold' else site+'_')+f'order{order}_'+component]


def response_path(owner,model,route,count):
    return owner/'results/response'/f'{model}-{route}-{count}/response.npz'


def unresolved_axes():
    return [
        dict(axis='Endpoint A/B incoming rules',status='unbounded_here',coefficient_in_cubic_error='-1/4 each',radius=None),
        dict(axis='Unresolved incoming-panel remainder, including exterior integration tails',status='no certified radius',radius=None),
        dict(axis='Electron population and hard-angle rules',status='held fixed',radius=None),
        dict(axis='Real-emission angular/radial and virtual-loop rules',status='held fixed',radius=None),
        dict(axis='Frequency-basis truncation and inherited photon/gas source history',status='reused, not re-refined',radius=None),
        dict(axis='Physical collision/emission approximation error',status='not measured by quadrature changes',radius=None)]
