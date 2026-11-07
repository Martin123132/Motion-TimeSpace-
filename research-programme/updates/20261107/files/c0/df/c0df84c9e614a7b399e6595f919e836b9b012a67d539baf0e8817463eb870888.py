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
PARENT=BRANCH/'mu-y-residual-decomposition-20261012'
sys.path.insert(0,str(PARENT))
import shape_common as inherited
from shape_common import np,math,json,linalg,special,digest,write_json,modest,ShapeReadout
from window_transfer_common import thermal_wave,NonlocalEmission,infrared_ladder
PARENT_SEAL='9896ef22c7cce9d68d1730721a3f3b423e42839daeccd43b6bd0844d666c55cd'
STARTED=datetime(2026,10,12,19,13,41,tzinfo=timezone.utc)
WINDOW=BRANCH/'downstream-window-transfer-20261012/results/window-transfer'
BASELINE=BRANCH/'infrared-source-domain-20261008/backgrounds'
TERM_NAMES=['Compton','double_Compton','bremsstrahlung']
DRIVE_NAMES=['residual_self','temperature_mismatch','mu_drive','y_drive']


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def verify_source(path,chain):
    path=Path(path).resolve()
    if path not in chain:
        inherited.inherited.inherited.verify_reference(path,chain)


def finish(folder,report,script,extra=()):
    paths={ROOT/'residual_kinetic_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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


def norm(values,measure):
    return np.sqrt(np.sum(measure[:,None]*values**2,axis=0))


class ResidualMap:
    def __init__(self,basis):
        self.basis=basis
        self.reader=ShapeReadout(basis,canonical=True)
        self.energy=(self.reader.measure*self.reader.frequency)@basis.values
        self.eta=self.energy/self.reader.capacity
        self.amplitude=self.reader.amplitude_matrix@basis.values
        self.mapping=basis.values-self.reader.frequency[:,None]*self.eta-self.reader.templates@self.amplitude
        self.dual=linalg.solve(basis.mass,(basis.values.T*self.reader.measure)@self.mapping,assume_a='pos')
        self.projected_templates=linalg.solve(basis.mass,(basis.values.T*self.reader.measure)@self.reader.templates,assume_a='pos')
        self.bands=[('full',basis.nodes,basis.measure,self.mapping)]
        for name,lower,upper in [('low',basis.minimum,.1),('peak',.001,.01)]:
            nodes,weights=special.roots_legendre(600)
            half=math.log(upper/lower)/2
            frequency=np.exp(math.log(lower*upper)/2+half*nodes)
            occupation=1/np.expm1(frequency)
            measure=weights*half*frequency**3*occupation*(1+occupation)/inherited.I3
            standard=np.column_stack([frequency/inherited.BETA-1,frequency*(frequency/np.tanh(frequency/2)-4)])
            templates=standard-frequency[:,None]*self.reader.shifts
            mapping=basis.evaluate(frequency)-frequency[:,None]*self.eta-templates@self.amplitude
            self.bands.append((name,frequency,measure,mapping))

    def pieces(self,photon,gas):
        amplitudes=self.amplitude@photon
        return np.stack([self.dual@photon,self.basis.temperature[:,None]*(self.eta@photon-gas),
            self.projected_templates[:,0,None]*amplitudes[0],
            self.projected_templates[:,1,None]*amplitudes[1]],axis=0)
