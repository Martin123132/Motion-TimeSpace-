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
PARENT=BRANCH/'source-adjoint-pairing-20261014'
sys.path.insert(0,str(PARENT))
import source_pair_common as inherited
from source_pair_common import np,math,json,linalg,interpolate,digest,write_json,modest,thermal_wave,infrared_ladder,read_npz,NonlocalEmission,compact_defect,local_packet,check,I3,norm,refined_owner,photon_norm,event_paths
PARENT_SEAL='1fe32097be6f71fdf0df4d66bc7816bb85ad2799ac33b1f62da18bfb7b409d3f'
STARTED=datetime(2026,10,14,10,58,13,tzinfo=timezone.utc)


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def verify_source(path,chain):
    inherited.verify_source(Path(path),chain)


def finish(folder,report,script,extra=()):
    paths={ROOT/'spatial_defect_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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


def basis_jets(basis,frequency):
    points=np.asarray(frequency)
    flat=points.ravel()
    pivot=basis.pivot
    compact=(flat-pivot)/(flat+pivot)
    first=2*pivot/(flat+pivot)**2
    second=-4*pivot/(flat+pivot)**3
    third=12*pivot/(flat+pivot)**4
    jets=np.zeros((4,len(flat),basis.count))
    jets[0,:,0]=1/basis.norms[0]
    jets[0,:,1]=(flat-basis.mean)/basis.norms[1]
    jets[1,:,1]=1/basis.norms[1]
    for degree in range(2,basis.count):
        previous=jets[:,:,degree-1]
        current=np.empty((4,len(flat)))
        current[0]=compact*previous[0]
        current[1]=compact*previous[1]+first*previous[0]
        current[2]=compact*previous[2]+2*first*previous[1]+second*previous[0]
        current[3]=compact*previous[3]+3*first*previous[2]+3*second*previous[1]+third*previous[0]
        for repeat in range(2):
            current-=jets[:,:,:degree]@basis.projections[degree,repeat,:degree]
        jets[:,:,degree]=current/basis.norms[degree]
    return jets.reshape((4,)+points.shape+(basis.count,))


def deposition_moments(ratios,spacing):
    inverse=1/ratios
    lower=np.floor(np.log(ratios)/spacing)
    upper_u=np.exp(-lower*spacing)
    lower_u=np.exp(-(lower+1)*spacing)
    variance=(upper_u-inverse)*(inverse-lower_u)
    third=variance*(upper_u+lower_u-2*inverse)
    return inverse,variance,third,upper_u,lower_u


def event_defects(basis,frequency,weights,ratios,rates,spacing,chunk=32):
    unique,inverse_index=np.unique(ratios,return_inverse=True)
    combined=np.bincount(inverse_index,weights=rates,minlength=len(unique))
    inverse,variance,third,upper_u,lower_u=deposition_moments(unique,spacing)
    base=basis.evaluate(frequency)
    physical=np.zeros_like(base)
    second_defect=np.zeros_like(base)
    third_defect=np.zeros_like(base)
    for start in range(0,len(unique),chunk):
        selection=slice(start,start+chunk)
        inv=inverse[selection,None,None]
        points=frequency[None,:,None]
        forward=basis_jets(basis,frequency[None,:]/inverse[selection,None])
        backward=basis_jets(basis,frequency[None,:]*inverse[selection,None])
        physical_event=(inv*(forward[0]-base)+inv**2*(backward[0]-base))/2
        second_event=(points**2/inv**3*forward[2]+2*(backward[0]-base)
            +4*points*inv*backward[1]+points**2*inv**2*backward[2])/2
        third_event=(-3*points**2/inv**4*forward[2]-points**3/inv**5*forward[3]
            +6*points*backward[1]+6*points**2*inv*backward[2]+points**3*inv**2*backward[3])/2
        physical+=np.einsum('e,efk->fk',combined[selection],physical_event)
        second_defect+=np.einsum('e,efk->fk',combined[selection]*variance[selection]/2,second_event)
        third_defect+=np.einsum('e,efk->fk',combined[selection]*third[selection]/6,third_event)
    physical_eigen=float(np.sum(combined*(unique-1)**2*(unique+1)/unique**3)/2)
    second_eigen=float(np.sum(combined*variance*(3*inverse-1))/2)
    third_eigen=float(np.sum(combined*third)/2)
    exact_bias=float(np.sum(combined*variance*(upper_u+lower_u+inverse-1))/2)
    diagnostics={}
    for label,matrix,eigen in [('physical',physical,physical_eigen),('second',second_defect,second_eigen),('third',third_defect,third_eigen)]:
        expected=frequency*eigen
        scale=max(float(np.linalg.norm(expected)),abs(physical_eigen)*float(np.linalg.norm(frequency))*1e-10,1e-300)
        diagnostics[label+'_raw_energy_error']=float(np.linalg.norm(matrix@basis.temperature-expected)/scale)
        diagnostics[label+'_raw_number_error']=float(np.max(abs(matrix@basis.chemical))/max(np.max(abs(matrix)),1e-300))
        matrix[:,0]=0.
        matrix[:,1]=expected/basis.norms[1]
    diagnostics.update(unique_events=len(unique),original_events=len(ratios),
        physical_eigen=physical_eigen,second_eigen=second_eigen,third_eigen=third_eigen,
        exact_bias=exact_bias,bias_identity=abs(second_eigen+third_eigen-exact_bias)/physical_eigen,
        minimum_variance=float(np.min(variance)))
    return {name:matrix.T*weights/I3 for name,matrix in [('physical',physical),('second',second_defect),('third',third_defect)]},diagnostics
