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
PARENT=BRANCH/'withheld-history-source-20261011'
sys.path.insert(0,str(BRANCH/'mixed-frequency-source-20261011'))
import frequency_grid_common as inherited
from frequency_grid_common import np,math,json,time,special,linalg,interpolate,weak,thermal_wave,I3,Spectra,TestFunctions,SplitReal,PanelRule,population_nodes,node_key,compact_rule,FastSplit
from resolved_redistribution import incoming_rule
from compare_source_vectors import dual_norm
import sampled_gould_control as leading
digest,write_json=inherited.digest,inherited.write_json
STARTED=datetime(2026,10,11,21,59,28,tzinfo=timezone.utc)
PARENT_SEAL='82db494fdb669a13426ef0f77c6f0135eb47b13c6112993c4a98e75ca394bfa4'
MID=BRANCH/'frequency-aligned-control-20261009/runs/compact128-h3-g2-2-4'
OUTER=BRANCH/'outer-population-source-20261008/runs/s4-h3-g2-2-4'
FRACTIONS={'early':.3125,'late':.4375}


def modest():
    import psutil
    process=psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([int(os.environ.get('MTS_CPU','2'))])


def finish(folder,report,script,extra=()):
    paths={ROOT/'curvature_source_common.py',ROOT/'ACCEPTANCE.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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


def physical_nodes(theta,part):
    electrons={}
    for node in population_nodes(theta,4,3,radial=2,polar=2,azimuthal=4):
        electrons[tuple(node['velocity'])]=node['electron_weight']
    assert len(electrons)==16
    frequencies=incoming_rule(4,1e-5,24.) if part=='expensive' else compact_rule(128,1e-5,24.)
    frequencies=list(frequencies)
    cosines,hard_weights=np.polynomial.legendre.leggauss(3)
    index=0
    for electron_index,(velocity,measure) in enumerate(electrons.items()):
        azimuth_index=electron_index%4
        if azimuth_index==3:
            continue
        multiplicity=2 if azimuth_index==1 else 1
        for frequency,seed_weight in frequencies:
            for cosine,hard_weight in zip(cosines,hard_weights):
                yield dict(index=index,frequency=float(frequency),seed_weight=float(seed_weight),
                    cosine=float(cosine),hard_weight=float(hard_weight),velocity=list(velocity),
                    electron_weight=float(measure),electron_index=electron_index,
                    azimuth_index=azimuth_index,reflection_multiplicity=multiplicity)
                index+=1


def parameters_and_weight(theta,node):
    parameters=weak.source.context(theta*node['frequency'],node['cosine'],np.array(node['velocity']),theta)
    weight=node['electron_weight']*node['reflection_multiplicity']*node['seed_weight']
    weight*=node['frequency']**2/math.expm1(node['frequency'])/I3
    weight*=2*np.pi*node['hard_weight']*parameters['born_differential_over_thomson']
    return parameters,float(weight)


def owned_loop(parameters):
    identity=inherited.virtual_identity(parameters)
    key=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
    path=ROOT/'virtual-cache'/key[:2]/(key+'.json')
    if path.exists():
        saved=json.loads(path.read_text())
        assert saved['identity']==identity and saved['finite']
    else:
        tensor,response=weak.source.virtual_map(parameters,2)
        saved=dict(identity=identity,scalar=float(response[0,0]),finite=bool(np.isfinite(response[0,0])))
        assert saved['finite']
        path.parent.mkdir(parents=True,exist_ok=True)
        temporary=path.with_suffix('.tmp')
        write_json(temporary,saved)
        temporary.replace(path)
    return saved['scalar'],path


def expensive_components(parameters,model):
    result=model.real(parameters,angular=4,radial=18,rule=PanelRule(.5))
    scalar,path=owned_loop(parameters)
    weak.vacuum.mp.mp.dps=60
    vacuum=float(weak.vacuum.finite_virtual_ratio(parameters['energy'],parameters['cosine'])
        +weak.vacuum.soft_constant(parameters['energy'],parameters['cosine']))
    jump,product=model.born_data(parameters)
    return dict(difference=result['total'],virtual=.5*(vacuum+scalar)*product,
        state=model.state_correction(parameters)['total']),result['event_energy_null'],scalar,path


def sampled_leading(bundle,theta):
    old_incoming,old_radial=leading.incoming_rule,leading.logarithmic_rule
    leading.incoming_rule,leading.logarithmic_rule=compact_rule,PanelRule(.5)
    try:
        return np.column_stack([leading.sampled(epoch,TestFunctions(epoch.basis),theta,128,18) for epoch in bundle.epochs])
    finally:
        leading.incoming_rule,leading.logarithmic_rule=old_incoming,old_radial


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


