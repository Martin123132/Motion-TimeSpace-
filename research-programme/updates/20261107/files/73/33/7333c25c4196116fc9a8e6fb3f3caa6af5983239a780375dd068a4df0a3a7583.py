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
PARENT=BRANCH/'matched-cubic-uncertainty-separation-20261018'
sys.path.insert(0,str(PARENT))
from stage156_common import *
import stage156_common as stage156_parent
from decimal import Decimal,localcontext
ROOT=Path(__file__).resolve().parent
PARENT=BRANCH/'matched-cubic-uncertainty-separation-20261018'
SOURCE155=BRANCH/'predictor-anchor-order6-20261018'
PARENT_SEAL='56f946960e8f44b4f370116c412163664236445abc0b593aca81855e34fbc4c0'
STARTED=datetime(2026,10,18,12,31,24,tzinfo=timezone.utc)
INHERITED_PAYLOADS=291654
SITES=['cold','warm','centre']
COEFFICIENTS=np.asarray([1.,1.,-1.5])
BOUNDARIES=np.asarray([1e-5,.05,.2,1.,3.,8.,20.,24.])
ORDERS=[4,5,6]


def ancestors():
    chain=stage156_parent.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'stage157_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',
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


def bank_folder(site,order):
    if order==4:
        owner={'cold':STAGE150,'warm':STAGE149,'centre':STAGE148}[site]
        return owner/'runs'/('expensive-centre' if site=='centre' else 'expensive-holdout')
    if site=='cold':
        return SOURCE152/'runs/part0' if order==6 else STAGE151/'runs/order5'
    return (SOURCE154 if order==5 else SOURCE155)/'runs'/site


def node_path(site,order,node,config,theta):
    reused=site=='cold' and order==5 and str(node['index']) in config['shared_order3']
    original=node
    folder=bank_folder(site,order)
    if reused:
        original=list(integration_nodes(theta,3))[config['shared_order3'][str(node['index'])]]
        folder=STAGE151/'runs/order3'
    elif site=='cold' and order==6:
        folder=SOURCE152/'runs'/f"part{node['index']%2}"
    return folder/'nodes'/f"{original['index']//500:03d}"/f"{original['index']:05d}.npz",original,reused


def virtual_reference(data,site,order):
    if site=='cold':
        value=data['actual_virtual'].copy()
        for current in range(5,order+1):
            value+=data[f'delta{current}_virtual']
        return value
    return data[site+'_virtual'] if order==4 else data[f'{site}_order{order}_virtual']


def stable_sum(values):
    array=np.asarray(values)
    flat=array.reshape(array.shape[0],-1)
    return np.asarray([math.fsum(flat[:,column]) for column in range(flat.shape[1])]).reshape(array.shape[1:])


def planned_inputs():
    inputs=[SOURCE155/'results/anchor-sources/source.npz',PARENT/'NUMERICAL-SUMMARY.json',
        PARENT/'results/analysis/source-separation.npz']
    for site in SITES:
        for order in ORDERS:
            folder=bank_folder(site,order)
            inputs.extend([folder/'configuration.json',folder/'status.json'])
    inputs.extend([STAGE151/'runs/order3/configuration.json',STAGE151/'runs/order3/status.json',
        SOURCE152/'runs/part1/configuration.json',SOURCE152/'runs/part1/status.json'])
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                for stage in [STAGE150,STAGE151,SOURCE152,SOURCE154,SOURCE155]:
                    folder=stage156_parent.location(stage,model,route,count)
                    inputs.extend([folder/'response.npz',folder/'status.json'])
                for match in [20,40]:
                    for stage in [STAGE150,SOURCE155]:
                        inputs.append(stage/'results/comparison'/f'{model}-m{match}-{route}-{count}.npz')
    return sorted(set(inputs))
