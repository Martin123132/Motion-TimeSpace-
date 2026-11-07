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
PARENT=BRANCH/'completed-spectrum-decomposition-20261015'
sys.path.insert(0,str(PARENT))
import spectrum_decomposition_common as inherited
from spectrum_decomposition_common import np,math,json,linalg,digest,write_json,modest,read_npz,ShapeReadout,norm
sys.path.insert(0,str(BRANCH/'curvature-holdouts-20261011'))
import curvature_source_common as event_owner
from curvature_source_common import time,weak,thermal_wave,EpochBundle,epoch_context,physical_nodes,parameters_and_weight,FastSplit,SplitReal,PanelRule,dual_norm,sampled_leading
from inspect_coupled_response import NonlocalEmission,infrared_ladder
sys.path.insert(0,str(BRANCH/'late-frequency-refinement-20261012'))
from evolve_stable_late_refinement import EnergyCoordinates
import hashlib
PARENT_SEAL='4821c5591720e66dc916a4fe827f25d9dce4f612ba49aed6e32fa0d97a93ccab'
STARTED=datetime(2026,10,15,20,32,11,tzinfo=timezone.utc)
FRACTIONS={'centre':.625,'end':.75}
MID=BRANCH/'frequency-aligned-control-20261009/runs/compact128-h3-g2-2-4'
COLUMN_NAMES=['heavy-join1','heavy-join2','cold-join1','cold-join2']
COMPONENTS=['control','sampled_leading','kinematic_remainder','difference','virtual','state','remainder']


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'adjacent_source_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',
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


def test(checks,name,value,limit=1e-10):
    value=float(value)
    checks.append(dict(name=name,value=value,limit=limit,passed=bool(np.isfinite(value) and value<limit)))


def verify_packet(folder):
    packet=json.loads((folder/'status.json').read_text())
    assert packet['state']=='complete' and (folder/'COMPLETE').exists()
    for path,sha in packet['input_hashes'].items():
        assert digest(path)==sha,path
    return packet


def owned_loop(parameters):
    identity=event_owner.inherited.virtual_identity(parameters)
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
