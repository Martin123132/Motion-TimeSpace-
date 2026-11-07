from common197 import *

def collapse(values):
    width=values.shape[-1]//2
    return values[...,:width]+values[...,width:]

def weights(offset,profile):
    assert OFFSETS[0]-1e-14<=offset<=OFFSETS[-1]+1e-14
    if profile=='quadratic':
        indices=[0,1,2] if offset<0 else [2,3,4]
    else:
        lower=min(max(int(np.searchsorted(OFFSETS,offset,side='right'))-1,0),3)
        indices=[lower,lower+1]
    result=np.zeros(5)
    for index in indices:
        result[index]=math.prod((offset-OFFSETS[other])/(OFFSETS[index]-OFFSETS[other]) for other in indices if other!=index)
    assert abs(result.sum()-1)<1e-14
    return result

class Forcing:
    def __init__(self,model,basis,inputs):
        self.config=frozen();self.basis=basis
        selection=slice(0,2) if model=='heavy' else slice(2,4)
        self.high=[];self.low=[]
        for tag in TAGS:
            path=register(inputs,ROOT/f'sources/{tag}.npz')
            data=packet(path)
            for name in ('high','low'):
                values=np.moveaxis(data[name][...,selection],2,0).reshape(98,36)
                getattr(self,name).append(np.column_stack([values,np.zeros(98)]))
        self.high=np.array(self.high);self.low=np.array(self.low)
        self.factor=linalg.cholesky(basis.mass,lower=True)
        self.pivot_norm=float(np.linalg.norm(linalg.solve_triangular(self.factor,np.eye(96)[:,1],lower=True)))
        self.maximum=dict(rewrite=0.,pair=0.,physical_moment=0.,stored_moment=0.)
        self.zeros={name:np.zeros((rows,74)) for name,rows in [('high',98),('low',98),('force_high',96),('force_low',96),('spectral_high',96),('spectral_low',96)]}
        self.zeros['rewrite']=0.

    def at(self,fraction):
        offset=(.875-fraction)*self.config['expansion_span']
        profiles=[]
        for profile in self.config['profiles']:
            coefficients=weights(offset,profile)
            product_high=self.high*coefficients[:,None,None]
            product_low=self.low*coefficients[:,None,None]
            for site,row,column in np.ndindex(product_high.shape):
                product_low[site,row,column]+=math.fma(float(coefficients[site]),float(self.high[site,row,column]),-float(product_high[site,row,column]))
            profiles.append(parts_sum(product_high,product_low))
        high=np.column_stack([pair[0] for pair in profiles]);low=np.column_stack([pair[1] for pair in profiles])
        spectral_high=high[1:-1].copy();spectral_low=low[1:-1].copy()
        changes=[]
        with localcontext() as context:
            context.prec=80
            temperature=[Decimal.from_float(float(value)) for value in self.basis.temperature[:2]]
            exact_temperature=temperature.copy()
            exact_temperature[0]=Decimal.from_float(float(self.basis.mean))*Decimal.from_float(float(self.basis.norms[0]))
            for column in range(high.shape[1]):
                values=[Decimal.from_float(float(high[row,column]))+Decimal.from_float(float(low[row,column])) for row in (0,1,2,97)]
                mapped=(values[0]-temperature[0]*values[1])/temperature[1]
                upper=float(mapped);lower=float(mapped-Decimal.from_float(upper))
                spectral_high[1,column]=upper;spectral_low[1,column]=lower
                changes.append(float(mapped-values[2]))
                scale=max(abs(values[0]),Decimal('1e-300'))
                for name,value in [('pair',values[0]+values[3]),('physical_moment',exact_temperature[0]*values[1]+exact_temperature[1]*values[2]-values[0]),('stored_moment',temperature[0]*values[1]+temperature[1]*values[2]-values[0])]:
                    self.maximum[name]=max(self.maximum[name],float(abs(value)/scale))
        denominator=np.maximum(np.linalg.norm(linalg.solve_triangular(self.factor,high[1:-1]+low[1:-1],lower=True),axis=0),1e-300)
        rewrite=float(np.max(abs(np.array(changes))*self.pivot_norm/denominator))
        self.maximum['rewrite']=max(self.maximum['rewrite'],rewrite)
        others=np.r_[0,np.arange(2,96)]
        return dict(high=high,low=low,force_high=np.vstack([high[0],high[1:-1][others]]),
                    force_low=np.vstack([low[0],low[1:-1][others]]),spectral_high=spectral_high,
                    spectral_low=spectral_low,rewrite=rewrite)

def evolve(model,count,smoke=False):
    config=frozen();inputs=read(ROOT/'inputs.json');checks=[]
    destination=ROOT/('smoke' if smoke else 'responses')/f'{model}-{count}'
    if (destination/'status.json').exists():
        previous=read(destination/'status.json')
        assert digest(destination/'terminal.npz')==previous['terminal_sha256']
        print('Reusing '+str(destination),flush=True);return
    ladder,background,emission=setup(model,inputs)
    assert abs(background.end-config['expansion_span'])<1e-14
    coordinates=response.EnergyCoordinates(ladder.basis);basis=ladder.basis
    supplied=Forcing(model,basis,inputs)
    start_index=round((config['interval'][0]-.75)*count/.25)
    stop_index=round((config['interval'][1]-.75)*count/.25)
    assert .75+start_index*.25/count==config['interval'][0]
    assert .75+stop_index*.25/count==config['interval'][1]
    final_index=min(stop_index+8,start_index+16) if smoke else count
    width=74;state=np.zeros((96,2*width));previous=state.copy()
    gas=np.zeros(2*width);work=gas.copy();number=gas.copy();injected=gas.copy()
    old_gas=gas.copy();old_work=gas.copy();old_number=gas.copy();old_injected=gas.copy()
    step=.25*background.end/count
    maximum={name:0. for name in ['photon_equation','gas_equation','spectral_energy_roundoff']}
    ledger_numerator=np.zeros(width);ledger_scale=np.zeros(width)
    number_numerator=np.zeros(width);number_scale=np.zeros(width)
    samples=[];began=time.monotonic()
    for index in range(start_index+1,final_index+1):
        fraction=.75+index*.25/count;coordinate=fraction*background.end
        local=background.at(coordinate);theta=local['thermal_parameter'];rate=local['coefficient']/theta;heat=background.chi
        assert ladder.temperatures[0]*(1-1e-12)<=theta<=ladder.temperatures[-1]*(1+1e-12)
        stiffness=ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr')
        source=supplied.at(fraction) if index<=stop_index else supplied.zeros
        original=np.column_stack([source['high'],source['low']])
        force=np.column_stack([source['force_high'],source['force_low']])
        spectral_source=np.column_stack([source['spectral_high'],source['spectral_low']])
        restart=index in (start_index+1,stop_index+1)
        alpha=(1 if restart else 1.5)/step
        history=state/step if restart else (2*state-.5*previous)/step
        gas_previous=gas/step if restart else (2*gas-.5*old_gas)/step
        work_previous=work/step if restart else (2*work-.5*old_work)/step
        number_previous=number/step if restart else (2*number-.5*old_number)/step
        injected_previous=injected/step if restart else (2*injected-.5*old_injected)/step
        projected=coordinates.tests@stiffness@coordinates.transform
        coupling=-rate*coordinates.tests@stiffness@basis.temperature
        pair=original[0]+original[-1]
        gas_free=(history[0]+heat*gas_previous+rate*pair)/(heat*(alpha+1))
        energy_coefficient=alpha/(heat*(alpha+1))
        matrix=alpha*coordinates.mass-rate*projected
        matrix[:,0]+=coupling*energy_coefficient
        right=coordinates.mass@history+rate*force+coupling[:,None]*gas_free
        updated=linalg.solve(matrix,right)
        new_gas=gas_free-energy_coefficient*updated[0]
        new_work=(work_previous+heat*new_gas)/alpha
        new_injected=(injected_previous+rate*pair)/alpha
        photon=coordinates.transform@updated;photon_previous=coordinates.transform@history
        physical=stiffness@(photon-basis.temperature[:,None]*new_gas)
        residual=basis.mass@(alpha*photon-photon_previous)-rate*physical-rate*original[1:-1]
        normalization=np.maximum(np.linalg.norm(collapse(basis.mass@photon_previous+rate*original[1:-1]),axis=0),1e-300)
        maximum['photon_equation']=max(maximum['photon_equation'],float(np.max(np.linalg.norm(collapse(residual),axis=0)/normalization)))
        gas_residual=heat*((alpha+1)*new_gas-gas_previous)+rate*basis.temperature@physical-rate*original[-1]
        maximum['gas_equation']=max(maximum['gas_equation'],float(np.max(abs(collapse(gas_residual)))))
        spectral=collapse(basis.energy@photon)
        allowance=256*np.finfo(float).eps*np.maximum(abs(basis.energy)@abs(collapse(photon)),1e-300)
        maximum['spectral_energy_roundoff']=max(maximum['spectral_energy_roundoff'],float(np.max(abs(spectral-collapse(updated[0]))/allowance)))
        new_number=(number_previous+rate*basis.chemical@(physical+spectral_source))/alpha
        balance=collapse(updated[0]+heat*new_gas+new_work-new_injected)
        ledger_numerator=np.maximum(ledger_numerator,abs(balance))
        ledger_scale=np.maximum(ledger_scale,abs(collapse(updated[0]))+abs(heat*collapse(new_gas))+abs(collapse(new_work))+abs(collapse(new_injected)))
        number_moment=basis.number@photon
        number_numerator=np.maximum(number_numerator,abs(collapse(number_moment-new_number)))
        number_scale=np.maximum(number_scale,abs(collapse(number_moment))+abs(collapse(new_number)))
        previous,state=state,updated
        old_gas,gas=gas,new_gas;old_work,work=work,new_work
        old_number,number=number,new_number;old_injected,injected=injected,new_injected
        if index%64==0 or index in (stop_index,final_index):
            samples.append(dict(index=index,fraction=fraction,max_gas=float(np.max(abs(collapse(gas))))))
        if index%512==0 or index==final_index:
            write(ROOT/'progress.json',dict(state='propagating',model=model,count=count,index=index,total=final_index,seconds=time.monotonic()-began))
            print(json.dumps(dict(model=model,count=count,index=index,total=final_index,seconds=time.monotonic()-began)),flush=True)
    for name,limit in [('photon_equation',1e-7),('gas_equation',1e-8),('spectral_energy_roundoff',1.)]:
        check(checks,name,maximum[name],limit)
    check(checks,'energy plus work minus measured injection',np.max(ledger_numerator/np.maximum(ledger_scale,1e-300)),1e-7)
    check(checks,'photon number ledger',np.max(number_numerator/np.maximum(number_scale,1e-300)),1e-7)
    for name in ('rewrite','pair','physical_moment'):
        check(checks,'source '+name,supplied.maximum[name],1e-10)
    arrays=dict(photon=photon,energy=state[0],gas=gas,work=work,number=number,integrated_injection=injected)
    terminal={}
    for key,values in arrays.items():
        terminal[key+'_high']=values[...,:width];terminal[key+'_low']=values[...,width:]
        terminal[key]=collapse(values)
        for profile in range(2):
            block=terminal[key][...,profile*37:(profile+1)*37]
            check(checks,key+f':zero:{profile}',np.max(abs(block[...,-1])),0,'identity')
            for version in range(6):
                part=block[...,version*6:version*6+6]
                check(checks,key+f':baseline+MTS=total:{profile}:{version}',
                      np.max(abs(part[...,4:6]-part[...,:2]-part[...,2:4]))/max(float(np.max(abs(part[...,4:6]))),1e-300),1e-8,'identity')
            check(checks,key+f':original+delta=candidate:{profile}',np.max(abs(block[...,:6]+block[...,24:30]-block[...,30:36]))/max(float(np.max(abs(block[...,30:36]))),1e-300),1e-8,'identity')
    save(destination/'terminal.npz',**terminal,heat=background.chi,labels=np.array(LABELS),profiles=np.array(config['profiles']),final_fraction=.75+final_index*.25/count)
    write(destination/'status.json',dict(model=model,count=count,smoke=smoke,checks=checks,
          failed_checks=[row for row in checks if not row['passed']],maximum=maximum,source_maximum=supplied.maximum,
          samples=samples,seconds=time.monotonic()-began,terminal_sha256=digest(destination/'terminal.npz'),
          inputs=inputs,interval=config['interval'],full_final_epoch=final_index==count))
    write(ROOT/'inputs.json',inputs)
    print(json.dumps(dict(model=model,count=count,failed=[row for row in checks if not row['passed']])),flush=True)

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--count',type=int,choices=[2048,4096],required=True);parser.add_argument('--smoke',action='store_true')
    arguments=parser.parse_args();evolve(arguments.model,arguments.count,arguments.smoke)
