import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import hashlib
ROOT=Path(__file__).resolve().parent
BRANCH,POST=ROOT.parent,ROOT.parent.parent
PARENT=BRANCH/'late-frequency-refinement-20261012'
ANCHOR=BRANCH/'curvature-holdouts-20261011'
sys.path.insert(0,str(BRANCH/'mixed-frequency-source-20261011'))
import frequency_grid_common as inherited
from frequency_grid_common import np,math,json,time,special,linalg,interpolate,weak,thermal_wave,I3,Spectra,TestFunctions,SplitReal,PanelRule,population_nodes,node_key,compact_rule,FastSplit
from resolved_redistribution import incoming_rule
from compare_source_vectors import dual_norm
import sampled_gould_control as leading
digest,write_json=inherited.digest,inherited.write_json
STARTED=datetime(2026,10,12,15,41,22,tzinfo=timezone.utc)
PARENT_SEAL='44ae668420f1197206ee4a4ccd8cf776b4bd6a53effcc96d72874a9c350a3656'
MID=BRANCH/'frequency-aligned-control-20261009/runs/compact128-h3-g2-2-4'
OUTER=BRANCH/'outer-population-source-20261008/runs/s4-h3-g2-2-4'
FRACTIONS={'late':.4375}


def modest():
    import psutil
    process=psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([int(os.environ.get('MTS_CPU','2'))])


def finish(folder,report,script,extra=()):
    paths={ROOT/'window_transfer_common.py',ROOT/'ACCEPTANCE.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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


class EpochBundle:
    def __init__(self,fraction):
        self.epochs=[Spectra(fraction)]
        self.basis=self.epochs[0].basis
        self.gas=[value for epoch in self.epochs for value in epoch.gas]
        self.coordinate=self.epochs[0].coordinate
        self.inputs=list(dict.fromkeys(path for epoch in self.epochs for path in epoch.inputs))

    def functions(self,frequency,chemical=False):
        values=[epoch.functions(frequency,chemical) for epoch in self.epochs]
        return np.concatenate([values[0][...,0:1],*[value[...,1:] for value in values]],axis=-1)

    def derivatives(self,frequency,chemical=False):
        values=[epoch.derivatives(frequency,chemical) for epoch in self.epochs]
        return values[0]


def epoch_context(bundle):
    contexts=[]
    for epoch in bundle.epochs:
        models=[]
        for label in ['heavy','cold']:
            background=thermal_wave.thermal.ThermalBackground(label)
            local=background.at(epoch.coordinate)
            models.append(dict(model=label,theta=local['thermal_parameter'],
                rate=local['coefficient']/local['thermal_parameter'],heat=background.chi,
                scale=local['scale'],coordinate=epoch.coordinate,
                inputs=[str(background.parent.source),str(background.native_constants)]))
        assert models[0]['theta']==models[1]['theta']
        contexts.append(models)
    return contexts


def sealed_ancestors():
    paths=[*BRANCH.glob('*/results/stage-integrity.json'),BRANCH/'results/stage-integrity.json']
    by_hash={digest(path):path for path in paths}
    cursor=PARENT/'results/stage-integrity.json'
    assert digest(cursor)==PARENT_SEAL
    result={}
    while True:
        assert cursor not in result
        packet=json.loads(cursor.read_text())
        assert packet['state']=='complete'
        result[cursor]=packet
        if cursor==BRANCH/'results/stage-integrity.json':
            break
        links=[packet[key] for key in ['parent_seal_sha256','previous_seal_sha256'] if key in packet]
        assert len(links)==1
        cursor=by_hash[links[0]]
    return result


def verify_reference(path,ancestors):
    path=Path(path).resolve()
    for seal,packet in ancestors.items():
        owner=POST if seal==BRANCH/'results/stage-integrity.json' else seal.parent.parent
        if path.is_relative_to(owner):
            key=path.relative_to(owner).as_posix()
            if key in packet['file_hashes']:
                assert digest(path)==packet['file_hashes'][key],path
                return
    raise AssertionError('No sealed owner: '+str(path))




sys.path.insert(0,str(PARENT))
from evolve_stable_late_refinement import EnergyCoordinates
from inspect_coupled_response import NonlocalEmission,infrared_ladder


def photon_norm(value,mass):
    return np.sqrt(np.maximum(np.einsum('...ik,ij,...jk->...k',value,mass,value),0.))


def load_terminal(model,count):
    path=PARENT/'results/refinement-response-stable'/f'{model}-{count}.npz'
    with np.load(path) as archive:
        saved={key:archive[key] for key in archive.files}
    return saved,path
