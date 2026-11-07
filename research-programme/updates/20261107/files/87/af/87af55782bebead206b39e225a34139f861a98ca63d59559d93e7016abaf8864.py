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
PARENT=BRANCH/'residual-kinetic-drive-20261012'
sys.path.insert(0,str(PARENT))
import residual_kinetic_common as inherited
from residual_kinetic_common import np,math,json,linalg,special,digest,write_json,modest,ShapeReadout,ResidualMap,infrared_ladder,thermal_wave,WINDOW,BASELINE
from scipy import interpolate,sparse
from scipy.sparse import linalg as sparse_linalg
import tail_common as tail
from tail_common import FreeFree,split_matrix
PARENT_SEAL='d56cdf8cb12dbf64b448cbe566b914876a9c49bebf89be167334c62973511c0e'
STARTED=datetime(2026,10,12,19,29,10,tzinfo=timezone.utc)
TAIL=BRANCH/'dynamical-infrared-tail-20261008'
I3=math.pi**4/15


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def verify_source(path,chain):
    inherited.verify_source(path,chain)


def finish(folder,report,script,extra=()):
    paths={ROOT/'turnover_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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


def hard_row(basis,minimum,count=384):
    nodes,weights=special.roots_legendre(count)
    half=math.log(basis.maximum/minimum)/2
    frequency=np.exp(math.log(basis.maximum*minimum)/2+half*nodes)
    occupation=1/np.expm1(frequency)
    weight=weights*half*frequency**5*occupation*(1+occupation)
    normalization=float(weight.sum())
    return weight@basis.derivative(frequency)/normalization,normalization


def load_histories(model):
    baseline_path=BASELINE/f'{model}-nonlocal-refined-6400/history.npz'
    window_path=WINDOW/f'{model}-main-1024.npz'
    with np.load(baseline_path) as saved:
        baseline={key:saved[key].copy() for key in saved.files}
    with np.load(window_path) as saved:
        window={key:saved[key].copy() for key in saved.files}
    return baseline,window,[baseline_path,window_path]


def profile_at(coordinate,baseline,window):
    def interp(times,values):
        return interpolate.interp1d(times,values,axis=0,bounds_error=True)(coordinate)
    return np.column_stack([interp(baseline['expansion'],baseline['profiles']),interp(window['coordinate'],window['photon'])])


def make_drivers(basis,baseline,window,high_grid,hard_minimum):
    slope,normalization=hard_row(basis,hard_minimum)
    high=basis.evaluate(high_grid)/high_grid[:,None]
    baseline_drive=np.column_stack([baseline['temperature_scaled'],baseline['profiles']@slope,baseline['profiles']@high.T])
    window_drive=np.concatenate([window['gas'][:,None,:],np.einsum('i,nij->nj',slope,window['photon'])[:,None,:],
                                np.einsum('fi,nik->nfk',high,window['photon'])],axis=1)
    baseline_interp=interpolate.interp1d(baseline['expansion'],baseline_drive,axis=0,bounds_error=True)
    window_interp=interpolate.interp1d(window['coordinate'],window_drive,axis=0,bounds_error=True)
    def driver(coordinate):
        return np.column_stack([baseline_interp(coordinate),window_interp(coordinate)])
    return driver,normalization


def reconstruct(basis,model,baseline,window,settings):
    background=thermal_wave.thermal.ThermalBackground(model)
    transport_name='heavy-base' if settings.get('coarse',False) else model+'-production'
    transport_path=TAIL/'runs'/transport_name/'tail.npz'
    clock_path=TAIL/'runs'/(model+'-production')/'tail.npz'
    with np.load(transport_path) as archive:
        old_grid=archive['frequency']
        spacing=float(np.log(old_grid[1]/old_grid[0]))
        offsets=archive['offsets'].copy()
        knot_times=archive['coefficient_knots'].copy()
        transport_bank=archive['coefficient_bank'][:,:len(offsets)+2].copy()
    with np.load(clock_path) as archive:
        clock_times=archive['coefficient_knots'].copy()
        clock=archive['coefficient_bank'][:,len(archive['offsets'])+2].copy()
    minimum,maximum=settings['minimum'],settings['maximum']
    size=int(math.ceil(math.log(maximum/minimum)/spacing))+1
    frequency=minimum*np.exp(spacing*np.arange(size))
    margin=int(max(-offsets[0],offsets[-1]))
    all_grid=minimum*np.exp(spacing*np.arange(-margin,size+margin))
    high_grid=all_grid[margin+size:]
    assert frequency[0]>=basis.minimum and high_grid.min()>.01 and high_grid.max()<basis.maximum
    driver,hard_normalization=make_drivers(basis,baseline,window,high_grid,settings['hard_floor'])
    free_free=FreeFree(background,all_grid)
    start,end=window['coordinate'][0],window['coordinate'][-1]
    knots=np.unique(np.r_[start,knot_times[(knot_times>start)&(knot_times<end)],end])
    transport_interp=interpolate.interp1d(knot_times,transport_bank,axis=0,bounds_error=True)
    clock_interp=interpolate.interp1d(clock_times,clock,bounds_error=True)
    coefficient_bank=[]
    for coordinate in knots:
        theta=background.at(float(coordinate))['thermal_parameter']
        values=transport_interp(coordinate)
        coefficient_bank.append(np.r_[values,float(clock_interp(coordinate)),free_free.br_rates(theta)])
    coefficient_bank=np.array(coefficient_bank)
    bank_at=interpolate.interp1d(knots,coefficient_bank,axis=0,bounds_error=True)
    initial=profile_at(float(start),baseline,window)
    state=(basis.evaluate(frequency)@initial)/frequency[:,None]
    snapshots=[state.copy()]
    targets=[]
    local_corrections=[]
    steps=settings['steps']
    step=(end-start)/steps
    identity=sparse.eye(size,format='csc')
    errors=dict(linear_solve=0.,equilibrium=0.,offdiagonal_negative=0.)
    minimum_margin=1e300
    maximum_growth_bound=0.
    previous_target=None
    for index in range(steps+1):
        coordinate=float(start+(end-start)*index/steps)
        values=bank_at(coordinate)
        stencil=values[:len(offsets)]
        eigenvalue,dc_constant,clock_rate=values[len(offsets):len(offsets)+3]
        br=values[len(offsets)+3:]
        dc=dc_constant/all_grid**2
        gamma=dc+br
        drives=driver(coordinate)
        gas,hard,upper=drives[0],drives[1],drives[2:]
        target=(dc[:,None]*hard+br[:,None]*gas)/gamma[:,None]
        internal,lower_matrix,upper_matrix=split_matrix(stencil,offsets,size)
        interior=slice(margin,margin+size)
        generator=clock_rate*(internal+sparse.diags(eigenvalue-gamma[interior],format='csc'))
        forcing=clock_rate*(dc[interior,None]*hard+br[interior,None]*gas-eigenvalue*gas
                           +lower_matrix@target[:margin]+upper_matrix@upper)
        equilibrium=generator@np.ones(size)+clock_rate*(gamma[interior]-eigenvalue
                         +lower_matrix@np.ones(margin)+upper_matrix@np.ones(margin))
        normalization=abs(generator)@np.ones(size)+clock_rate*(gamma[interior]+abs(eigenvalue)
                         +lower_matrix@np.ones(margin)+upper_matrix@np.ones(margin))
        errors['equilibrium']=max(errors['equilibrium'],float(np.max(abs(equilibrium)/np.maximum(normalization,1e-300))))
        offdiagonal=internal-sparse.diags(internal.diagonal())
        errors['offdiagonal_negative']=max(errors['offdiagonal_negative'],float(-offdiagonal.data.min(initial=0.)))
        minimum_margin=min(minimum_margin,float(np.min(1+step*clock_rate*(gamma[interior]-eigenvalue))))
        maximum_growth_bound=max(maximum_growth_bound,float(np.max(clock_rate*(eigenvalue-gamma[interior]))))
        if index:
            matrix=identity-step*generator
            right=state+step*forcing
            updated=sparse_linalg.splu(matrix).solve(right)
            errors['linear_solve']=max(errors['linear_solve'],float(np.max(abs(matrix@updated-right))/
                max(float(np.max(abs(matrix)@abs(updated)+abs(right))),1e-300)))
            state=updated
        if index%(steps//64)==0:
            if index:
                snapshots.append(state.copy())
            targets.append(target[interior].copy())
            if previous_target is None:
                local_corrections.append(target[interior].copy())
            else:
                target_rate=(target[interior]-previous_target[interior])/step
                full_transport=internal@target[interior]+lower_matrix@target[:margin]+upper_matrix@target[margin+size:]
                correction=(full_transport+eigenvalue*(target[interior]-gas)-target_rate/clock_rate)/gamma[interior,None]
                local_corrections.append(target[interior]+correction)
        previous_target=target.copy()
    return dict(frequency=frequency,coordinate=np.linspace(start,end,65),slope=np.array(snapshots),
        source_target=np.array(targets),first_correction=np.array(local_corrections),coefficient_knots=knots,
        coefficient_bank=coefficient_bank,offsets=offsets,hard_normalization=hard_normalization),dict(
        errors=errors,implicit_diagonal_margin=minimum_margin,positive_growth_bound=maximum_growth_bound,
        numerical_domain=[float(frequency[0]),float(frequency[-1])],size=size,transport=transport_name),[
        transport_path,clock_path,*free_free.inputs,background.parent.source,background.native_constants]
