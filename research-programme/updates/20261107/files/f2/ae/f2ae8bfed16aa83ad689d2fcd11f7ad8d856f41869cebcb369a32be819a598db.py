from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'panel-correction-saved-response-20261022'
sys.path.insert(0,str(PARENT))
import common197 as saved
import propagate197 as inherited
np,linalg,math,json=saved.np,saved.linalg,saved.math,saved.json
read,write,packet,save,check,digest=saved.read,saved.write,saved.packet,saved.save,saved.check,saved.digest
datetime,timezone,time=saved.datetime,saved.timezone,saved.time
SEAL='d8b89e694b8ab1adf50bc7a71afca304590d5355c54ed3a64e1a07e2077d653a'
PRIMARY=np.r_[24:30,61:67]
SELECTED=np.r_[PRIMARY,PRIMARY+74]
FIELDS={'energy':slice(0,1),'photon_coordinates':slice(0,96),'gas':slice(96,97),
        'work':slice(97,98),'number':slice(98,99),'injection':slice(99,100)}

def protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    return config

def prepare():
    assert not (ROOT/'configuration.json').exists()
    parent=read(PARENT/'results/stage-integrity.json');assert digest(PARENT/'results/stage-integrity.json')==SEAL
    inputs=dict(parent['consumed_and_immediate_rehashed'])
    for name,value in parent['file_hashes'].items():
        inputs[str(PARENT/name)]=value
    inputs[str(PARENT/'results/stage-integrity.json')]=SEAL
    for name,value in inputs.items():
        assert digest(name)==value,name
    previous=read(PARENT/'configuration.json')
    config=dict(stage=198,started_utc=datetime.now(timezone.utc).isoformat(),parent_seal_sha256=SEAL,
                interval=previous['interval'],counts=previous['counts'],cuts=[.873046875,.875,.876953125],
                target=.90625,identity_tolerance=1e-10,comparison_tolerance=.01,
                protocol_hashes={path.name:digest(path) for path in [*ROOT.glob('*.py'),ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md']},
                bookmarks={str(path):digest(path) for path in [BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md']})
    write(ROOT/'configuration.json',config);write(ROOT/'inputs.json',inputs)
    write(ROOT/'progress.json',dict(state='prepared'))
    print(json.dumps(dict(state='prepared',inputs=len(inputs))),flush=True)

def collapsed(values):
    width=values.shape[-1]//2
    return values[...,:width]+values[...,width:]

def relative(first,second):
    return float(np.max(abs(first-second))/max(float(np.max(abs(second))),1e-300))

def compare(checks,label,first,second,tolerance=1e-10):
    for field,indices in FIELDS.items():
        for column in range(first.shape[-1]):
            check(checks,f'{label}:{field}:{column}',relative(first[indices,column],second[indices,column]),tolerance,'identity')

class System:
    def __init__(self,model,count,inputs):
        self.config=protocol();self.count=count
        self.ladder,self.background,self.emission=saved.setup(model,inputs)
        self.basis=self.ladder.basis;self.coordinates=saved.response.EnergyCoordinates(self.basis)
        self.source=inherited.Forcing(model,self.basis,inputs)
        self.start=round((self.config['interval'][0]-.75)*count/.25)
        self.stop=round((self.config['interval'][1]-.75)*count/.25)
        self.cuts=[round((fraction-.75)*count/.25) for fraction in self.config['cuts']]
        self.target=round((self.config['target']-.75)*count/.25)
        self.step=.25*self.background.end/count
        self.cache={}

    def make_step(self,index):
        fraction=.75+index*.25/self.count
        local=self.background.at(fraction*self.background.end)
        theta=local['thermal_parameter'];rate=local['coefficient']/theta;heat=self.background.chi
        stiffness=self.ladder.at(theta,0)[:96,:96]-self.emission.at(theta,'dcbr')
        restart=index in (self.start+1,self.stop+1)
        alpha=(1 if restart else 1.5)/self.step
        coupling=-rate*self.coordinates.tests@stiffness@self.basis.temperature
        coefficient=alpha/(heat*(alpha+1))
        projected=self.coordinates.tests@stiffness@self.coordinates.transform
        matrix=alpha*self.coordinates.mass-rate*projected
        factor=linalg.lu_factor(matrix)
        gas_response=linalg.lu_solve(factor,coupling)
        denominator=heat*(alpha+1)+alpha*gas_response[0]
        assert np.isfinite(denominator) and denominator>0
        return dict(index=index,fraction=fraction,rate=rate,heat=heat,stiffness=stiffness,restart=restart,
                    alpha=alpha,coupling=coupling,coefficient=coefficient,factor=factor,
                    gas_response=gas_response,denominator=denominator)

    def advance(self,current,older,step,source=None,diagnostics=False):
        history=current/self.step if step['restart'] else (2*current-.5*older)/self.step
        alpha,heat,rate=step['alpha'],step['heat'],step['rate']
        if source is None:
            pair=0.;force=0.;spectral_source=0.
        else:
            pair=source['original'][0]+source['original'][-1]
            force=source['force'];spectral_source=source['spectral']
        free=linalg.lu_solve(step['factor'],self.coordinates.mass@history[:96]+rate*force)
        cancellation=np.array([math.fma(-alpha,float(value),float(previous)) for value,previous in zip(free[0],history[0])])
        gas=(cancellation+heat*history[96]+rate*pair)/step['denominator']
        updated=free+step['gas_response'][:,None]*gas
        photon=self.coordinates.transform@updated
        physical=step['stiffness']@(photon-self.basis.temperature[:,None]*gas)
        work=(history[97]+heat*gas)/alpha
        number=(history[98]+rate*self.basis.chemical@(physical+spectral_source))/alpha
        injection=(history[99]+rate*pair)/alpha
        result=np.vstack([updated,gas,work,number,injection])
        record={}
        if diagnostics:
            original=np.zeros((98,current.shape[-1])) if source is None else source['original']
            old_photon=self.coordinates.transform@history[:96]
            residual=self.basis.mass@(alpha*photon-old_photon)-rate*physical-rate*original[1:-1]
            normalization=np.maximum(np.linalg.norm(collapsed(self.basis.mass@old_photon+rate*original[1:-1]),axis=0),1e-300)
            record['photon']=float(np.max(np.linalg.norm(collapsed(residual),axis=0)/normalization))
            gas_error=heat*((alpha+1)*gas-history[96])+rate*self.basis.temperature@physical-rate*original[-1]
            record['gas']=float(np.max(abs(collapsed(gas_error))))
            allowance=256*np.finfo(float).eps*np.maximum(abs(self.basis.energy)@abs(collapsed(photon)),1e-300)
            record['spectral']=float(np.max(abs(collapsed(self.basis.energy@photon)-collapsed(updated[0]))/allowance))
        return result,record

    def forcing(self,index):
        value=self.source.at(.75+index*.25/self.count)
        return {name:np.column_stack([value[high],value[low]]) for name,high,low in
                [('original','high','low'),('force','force_high','force_low'),('spectral','spectral_high','spectral_low')]}

def physical_state(system,terminal):
    result=[]
    for suffix in ('_high','_low'):
        result.append(np.vstack([terminal['energy'+suffix],terminal['photon'+suffix][system.coordinates.others],
                                terminal['gas'+suffix],terminal['work'+suffix],terminal['number'+suffix],terminal['integrated_injection'+suffix]]))
    return np.column_stack(result)

def spectral(system,state):
    reader=saved.response.ShapeReadout(system.basis,canonical=True)
    return reader,reader.apply(system.coordinates.transform@state[:96],state[0])

def run(model,count):
    config=protocol();inputs=read(ROOT/'inputs.json');checks=[];folder=ROOT/'runs-stable'/f'{model}-{count}'
    assert not (folder/'status.json').exists()
    system=System(model,count,inputs);heat=system.background.chi
    width=148+len(system.cuts)*48
    current=np.zeros((100,width));older=current.copy();snapshots={};maximum=dict(photon=0.,gas=0.,spectral=0.)
    ledger_scale=np.zeros(74);ledger_error=np.zeros(74);number_scale=np.zeros(74);number_error=np.zeros(74)
    began=time.monotonic()
    for index in range(system.start+1,system.stop+1):
        step=system.make_step(index);source=system.forcing(index)
        system.cache[index]=(step,source)
        expanded={}
        for name,values in source.items():
            subset=values[:,SELECTED]
            expanded[name]=np.column_stack([values,*[piece for cut in system.cuts for piece in
                                                   (subset if index<=cut else np.zeros_like(subset),subset if index>cut else np.zeros_like(subset))]])
        updated,_=system.advance(current,older,step,expanded)
        audited,diagnostic=system.advance(current[:,:148],older[:,:148],step,source,True)
        check(checks,f'joint versus isolated solve:{index}',relative(updated[:,:148],audited),1e-10,'identity')
        for name,value in diagnostic.items():
            maximum[name]=max(maximum[name],value)
        older,current=current,updated
        mono=collapsed(current[:,:148])
        scale=abs(mono[0])+abs(heat*mono[96])+abs(mono[97])+abs(mono[99])
        ledger_scale=np.maximum(ledger_scale,scale);ledger_error=np.maximum(ledger_error,abs(mono[0]+heat*mono[96]+mono[97]-mono[99]))
        photons=system.coordinates.transform@mono[:96];number=system.basis.number@photons
        number_scale=np.maximum(number_scale,abs(number)+abs(mono[98]));number_error=np.maximum(number_error,abs(number-mono[98]))
        if index in [*system.cuts,system.stop]:
            path=folder/f'interfaces/step-{index}.npz'
            save(path,current=current[:,:148],previous=older[:,:148],fraction=step['fraction'],step=system.step,index=index)
            snapshots[index]=path
    boundary=current.copy();boundary_previous=older.copy()
    for cut in system.cuts:
        stored=packet(snapshots[cut]);rejoined=stored['current'];previous=stored['previous']
        for index in range(cut+1,system.stop+1):
            step,source=system.cache[index];updated,_=system.advance(rejoined,previous,step,source)
            previous,rejoined=rejoined,updated
        compare(checks,f'rejoin at{cut}',collapsed(rejoined[:,SELECTED]),collapsed(boundary[:,SELECTED]))
    middle=system.cuts[1];stored=packet(snapshots[middle]);negative=[]
    for kind in ('erase_previous','erase_gas'):
        rejoined=stored['current'][:,SELECTED].copy();previous=stored['previous'][:,SELECTED].copy()
        if kind=='erase_previous':
            previous=rejoined.copy()
        else:
            rejoined[96]=0.;previous[96]=0.
        initial_jump=collapsed(rejoined-stored['current'][:,SELECTED])
        for index in range(middle+1,system.stop+1):
            step,source=system.cache[index]
            selected={name:values[:,SELECTED] for name,values in source.items()}
            updated,_=system.advance(rejoined,previous,step,selected);previous,rejoined=rejoined,updated
        error=collapsed(rejoined-boundary[:,SELECTED]);reference=collapsed(boundary[:,SELECTED])
        reader,split=spectral(system,error);_,exact=spectral(system,reference)
        residual_ratio=saved.response.norm(split['residual'],reader.measure)/np.maximum(saved.response.norm(exact['residual'],reader.measure),1e-300)
        negative.append(dict(kind=kind,residual_ratio=residual_ratio.tolist(),
                             max_physical_state_jump=float(np.max(abs(initial_jump))),
                             fails_superposition_gate=bool(np.max(residual_ratio)>1e-8)))
        save(folder/f'negative/{kind}.npz',error=error,reference=reference)
    for cut_index,cut in enumerate(system.cuts):
        start=148+48*cut_index
        combined=collapsed(boundary[:,start:start+24])+collapsed(boundary[:,start+24:start+48])
        compare(checks,f'source partition at{cut}',combined,collapsed(boundary[:,SELECTED]),1e-8)
    current=np.column_stack([current,np.eye(100)]);older=np.column_stack([older,np.zeros((100,100))])
    transfer_slice=slice(width,width+100);target_record=None
    for index in range(system.stop+1,count+1):
        step=system.make_step(index)
        updated,_=system.advance(current,older,step)
        audited,diagnostic=system.advance(current[:,:148],older[:,:148],step,None,True)
        for name,value in diagnostic.items():
            maximum[name]=max(maximum[name],value)
        older,current=current,updated
        mono=collapsed(current[:,:148])
        ledger_scale=np.maximum(ledger_scale,abs(mono[0])+abs(heat*mono[96])+abs(mono[97])+abs(mono[99]))
        ledger_error=np.maximum(ledger_error,abs(mono[0]+heat*mono[96]+mono[97]-mono[99]))
        number=system.basis.number@(system.coordinates.transform@mono[:96])
        number_scale=np.maximum(number_scale,abs(number)+abs(mono[98]));number_error=np.maximum(number_error,abs(number-mono[98]))
        if index in (system.target,count):
            transfer=current[:,transfer_slice].copy();previous_transfer=older[:,transfer_slice].copy()
            mapped=transfer@boundary[:,:148]
            compare(checks,f'boundary transfer to{index}',collapsed(mapped[:,SELECTED]),collapsed(current[:,SELECTED]))
            energy_row=np.zeros(100);energy_row[[0,96,97,99]]=[1.,heat,1.,-1.]
            number_row=np.zeros(100);number_row[:96]=system.basis.number@system.coordinates.transform;number_row[98]=-1
            check(checks,f'energy invariant transfer:{index}',relative(energy_row@transfer,energy_row),1e-10,'identity')
            check(checks,f'number invariant transfer:{index}',relative(number_row@transfer,number_row),1e-10,'identity')
            save(folder/f'transfer/step-{index}.npz',operator=transfer,previous_operator=previous_transfer,
                 current=current[:,:width],previous=older[:,:width],fraction=step['fraction'])
            if index==system.target:
                target_record=(transfer,previous_transfer)
                current=np.column_stack([current,np.eye(100),np.zeros((100,100))])
                older=np.column_stack([older,np.zeros((100,100)),np.eye(100)])
        if index%512==0:
            write(ROOT/'progress.json',dict(state='evolving',model=model,count=count,index=index,seconds=time.monotonic()-began))
    final_transfer=current[:,transfer_slice]
    tail=current[:,width+100:width+300]
    composed=tail[:,:100]@target_record[0]+tail[:,100:]@target_record[1]
    check(checks,'two-level transfer composition',relative(composed,final_transfer),1e-10,'identity')
    save(folder/'transfer/composition.npz',current_map=tail[:,:100],previous_map=tail[:,100:],composed=composed)
    reference_path=PARENT/f'responses/{model}-{count}/terminal.npz'
    terminal=packet(saved.register(inputs,reference_path));expected=physical_state(system,terminal)
    compare(checks,'Stage197 final replay',collapsed(current[:,:148][:,SELECTED]),collapsed(expected[:,SELECTED]))
    for cut_index,cut in enumerate(system.cuts):
        start=148+48*cut_index
        combined=collapsed(current[:,start:start+24])+collapsed(current[:,start+24:start+48])
        compare(checks,f'final source partition at{cut}',combined,collapsed(current[:,SELECTED]),1e-8)
    for name,limit in [('photon',1e-7),('gas',1e-8),('spectral',1.)]:
        check(checks,'original '+name+' equation',maximum[name],limit)
    check(checks,'energy ledger',np.max(ledger_error/np.maximum(ledger_scale,1e-300)),1e-7)
    check(checks,'number ledger',np.max(number_error/np.maximum(number_scale,1e-300)),1e-7)
    for name in ('rewrite','pair','physical_moment'):
        check(checks,'source '+name,system.source.maximum[name],1e-10)
    reader=saved.response.ShapeReadout(system.basis,canonical=True)
    mass_factor=linalg.cholesky(system.basis.mass,lower=True)
    inverse_whitening=linalg.solve_triangular(mass_factor.T,np.eye(96),lower=False)
    injection=np.zeros((100,97))
    to_coordinates=np.vstack([system.basis.energy,np.eye(96)[system.coordinates.others]])
    injection[:96,:96]=to_coordinates@inverse_whitening;injection[96,96]=1/math.sqrt(heat)
    injection[97]=-injection[0]-heat*injection[96]
    injection[98,:96]=system.basis.number@inverse_whitening
    propagated=final_transfer@injection
    split=reader.apply(system.coordinates.transform@propagated[:96],propagated[0])
    gain_matrix=np.sqrt(reader.measure)[:,None]*heat*split['residual']
    left,singular,right=linalg.svd(gain_matrix,full_matrices=False)
    direction=injection@right[0];mode=direction[:,None];previous=np.zeros_like(mode)
    for index in range(system.stop+1,count+1):
        updated,_=system.advance(mode,previous,system.make_step(index));previous,mode=mode,updated
    mode_split=reader.apply(system.coordinates.transform@mode[:96],mode[0])
    measured=abs(heat)*saved.response.norm(mode_split['residual'],reader.measure)[0]
    check(checks,'independent maximizing-mode evolution',abs(measured/singular[0]-1),1e-10,'identity')
    check(checks,'whitened maximizing direction norm',abs(float(np.linalg.norm(right[0]))-1),1e-10,'identity')
    physical_norm=np.sqrt(np.sum((mass_factor.T@(system.coordinates.transform@collapsed(boundary[:,SELECTED])[:96]))**2,axis=0)+heat*collapsed(boundary[:,SELECTED])[96]**2)
    final_split=reader.apply(system.coordinates.transform@collapsed(current[:,SELECTED])[:96],collapsed(current[:,SELECTED])[0])
    final_norm=abs(heat)*saved.response.norm(final_split['residual'],reader.measure)
    ratio=final_norm/np.maximum(singular[0]*physical_norm,1e-300)
    check(checks,'saved physical directions satisfy computed gain',max(float(np.max(ratio))-1,0),1e-10,'identity')
    budget_path=BRANCH/f'final-spectrum-uncertainty-20261019/results/budget-ready/{model}-cubic-m20.npz'
    budget=packet(saved.register(inputs,budget_path))
    save(folder/'transfer/residual-gain.npz',gain=singular[0],singular_values=singular,injection=injection,
         maximizing_direction=direction,gain_matrix=gain_matrix,actual_boundary_norm=physical_norm,actual_final_residual=final_norm,
         budget_boundary_norm=budget['allowance'][3]/singular[0])
    for path in list(inputs):
        if Path(path).is_relative_to(ROOT):
            inputs.pop(path)
    write(ROOT/'inputs.json',inputs)
    report=dict(stage=198,model=model,count=count,checks=checks,failed_checks=[row for row in checks if not row['passed']],
                negative_controls=negative,maximum=maximum,source_maximum=system.source.maximum,
                residual_gain=float(singular[0]),gain_forward_check=float(measured),
                MTS_partial_allowance_boundary_norm=(budget['allowance'][3]/singular[0]).tolist(),
                physical_directions_gain_ratio=ratio.tolist(),seconds=time.monotonic()-began,
                output_hashes={str(path.relative_to(folder)):digest(path) for path in folder.rglob('*.npz')})
    write(folder/'status.json',report)
    print(json.dumps(dict(model=model,count=count,checks=len(checks),failed=report['failed_checks'],gain=report['residual_gain'],seconds=report['seconds'])),flush=True)

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--prepare',action='store_true');parser.add_argument('--model',choices=['heavy','cold']);parser.add_argument('--count',type=int,choices=[2048,4096])
    args=parser.parse_args()
    if args.prepare:
        prepare()
    else:
        assert args.model and args.count;run(args.model,args.count)
