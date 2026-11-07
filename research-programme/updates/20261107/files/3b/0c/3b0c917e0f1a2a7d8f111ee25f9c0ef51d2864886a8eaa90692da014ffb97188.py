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
PARENT=BRANCH/'temperature-distortion-projection-20261012'
sys.path.insert(0,str(PARENT))
import projection_common as inherited
from projection_common import np,math,json,re,linalg,special,infrared_ladder
digest,write_json,modest=inherited.digest,inherited.write_json,inherited.modest
STARTED=datetime(2026,10,12,18,47,50,tzinfo=timezone.utc)
PARENT_SEAL='b7f51e21dc6450d05da4beb3d5d0fd6d087b2d8e72ba356652645483f80d5be6'
URLS=['https://academic.oup.com/mnras/article/466/2/2390/2669327',
      'https://doi.org/10.1093/mnras/stw3230',
      'https://arxiv.org/abs/1306.5751','https://doi.org/10.1093/mnras/stt2327']
I3=math.pi**4/15
BETA=3*special.zeta(3)/special.zeta(2)


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'shape_common.py',ROOT/'ACCEPTANCE.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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


def weighted_norm(values,measure):
    return np.sqrt(np.sum(measure[:,None]*values**2,axis=0))


class ShapeReadout:
    def __init__(self,basis,count=700,minimum=1e-5,canonical=False):
        self.minimum,self.maximum,self.count=minimum,basis.maximum,count
        if canonical:
            assert minimum==basis.minimum and count==len(basis.nodes)
            self.frequency,self.measure,self.values=basis.nodes,basis.measure,basis.values
        else:
            nodes,weights=special.roots_legendre(count)
            lower,upper=math.log(minimum),math.log(basis.maximum)
            self.frequency=np.exp((lower+upper)/2+(upper-lower)/2*nodes)
            occupation=1/np.expm1(self.frequency)
            self.measure=weights*(upper-lower)/2*self.frequency**3*occupation*(1+occupation)/I3
            self.values=basis.evaluate(self.frequency)
        frequency,measure=self.frequency,self.measure
        self.capacity=float(np.sum(measure*frequency**2))
        self.standard=np.column_stack([frequency/BETA-1,frequency*(frequency/np.tanh(frequency/2)-4)])
        self.shifts=(measure*frequency)@self.standard/self.capacity
        self.templates=self.standard-frequency[:,None]*self.shifts
        self.gram=(self.templates.T*measure)@self.templates
        self.template_norms=np.sqrt(np.diag(self.gram))
        self.design=np.sqrt(measure)[:,None]*self.templates/self.template_norms
        self.orthogonal,self.triangular=linalg.qr(self.design,mode='economic')
        self.singular=linalg.svdvals(self.design)
        self.condition=float(self.singular[0]/self.singular[-1])
        self.correlation=float(self.gram[0,1]/np.prod(self.template_norms))
        self.amplitude_matrix=linalg.solve_triangular(self.triangular,
            self.orthogonal.T*np.sqrt(measure)[None,:])/self.template_norms[:,None]

    def split_values(self,potential,energy=None):
        spectral_energy=(self.measure*self.frequency)@potential
        if energy is None:
            energy=spectral_energy.copy()
        eta=energy/self.capacity
        temperature=self.frequency[:,None]*eta
        distortion=potential-temperature
        amplitudes=self.amplitude_matrix@distortion
        joint=self.templates@amplitudes
        residual=distortion-joint
        input_norm=weighted_norm(distortion,self.measure)
        residual_norm=weighted_norm(residual,self.measure)
        joint_norm=weighted_norm(joint,self.measure)
        return dict(potential=potential,energy=energy,spectral_energy=spectral_energy,
            energy_defect=spectral_energy-energy,eta=eta,temperature=temperature,
            distortion=distortion,amplitudes=amplitudes,joint=joint,residual=residual,
            distortion_norm=input_norm,joint_norm=joint_norm,residual_norm=residual_norm,
            residual_fraction=np.divide(residual_norm,input_norm,out=np.zeros_like(input_norm),where=input_norm>0),
            captured_squared_fraction=np.divide(joint_norm**2,input_norm**2,out=np.zeros_like(input_norm),where=input_norm>0),
            eta_standard=eta-self.shifts@amplitudes)

    def apply(self,photon,energy=None):
        return self.split_values(self.values@photon,energy)

