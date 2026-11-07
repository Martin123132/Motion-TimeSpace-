from stage168_common import *


def collapse(values):
    width=values.shape[-1]//2
    return values[...,:width]+values[...,width:]


def initial_parts(initial,key):
    high=initial.get(key+'_high',initial[key])
    low=initial.get(key+'_low',np.zeros_like(high))
    return np.concatenate([high,low],axis=-1)


def integrate(model,count,initial,source_at,ladder,background,emission,lower,upper,label):
    basis=ladder.basis
    coordinates=EnergyCoordinates(basis)
    begin,end=lower*background.end,upper*background.end
    step=(end-begin)/count
    state=np.vstack([initial_parts(initial,'energy'),initial_parts(initial,'photon')[coordinates.others]])
    previous=state.copy()
    gas,work,created=[initial_parts(initial,key).copy() for key in ['gas','work','integrated_number_source']]
    old_gas,old_work,old_created=gas.copy(),work.copy(),created.copy()
    injected=np.zeros_like(gas)
    old_injected=injected.copy()
    injected_history=[injected.copy()]
    histories=[state.copy()]
    gas_history,work_history,number_history=[gas.copy()],[work.copy()],[created.copy()]
    maxima={key:0. for key in ['source_rewrite','photon_equation','gas_equation','spectral_energy_roundoff']}
    for index in range(1,count+1):
        coordinate=begin+index*step
        local=background.at(coordinate)
        theta,rate,heat=local['thermal_parameter'],local['coefficient']/local['thermal_parameter'],background.chi
        assert ladder.temperatures[0]*(1-1e-12)<=theta<=ladder.temperatures[-1]*(1+1e-12)
        stiffness=ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr')
        supplied=source_at(index/count)
        original=np.column_stack([supplied['high'],supplied['low']])
        force=np.column_stack([supplied['force_high'],supplied['force_low']])
        spectral_source=np.column_stack([supplied['spectral_high'],supplied['spectral_low']])
        maxima['source_rewrite']=max(maxima['source_rewrite'],supplied['rewrite'])
        if index==1:
            alpha=1/step
            history=state/step
            gas_previous,work_previous,number_previous=gas/step,work/step,created/step
            injected_previous=injected/step
        else:
            alpha=1.5/step
            history=(2*state-.5*previous)/step
            gas_previous=(2*gas-.5*old_gas)/step
            work_previous=(2*work-.5*old_work)/step
            number_previous=(2*created-.5*old_created)/step
            injected_previous=(2*injected-.5*old_injected)/step
        projected=coordinates.tests@stiffness@coordinates.transform
        coupling=-rate*coordinates.tests@stiffness@basis.temperature
        source_pair=original[0]+original[-1]
        gas_free=(history[0]+heat*gas_previous+rate*source_pair)/(heat*(alpha+1))
        new_injected=(injected_previous+rate*source_pair)/alpha
        energy_coefficient=alpha/(heat*(alpha+1))
        matrix=alpha*coordinates.mass-rate*projected
        matrix[:,0]+=coupling*energy_coefficient
        right=coordinates.mass@history+rate*force+coupling[:,None]*gas_free
        updated=linalg.solve(matrix,right)
        new_gas=gas_free-energy_coefficient*updated[0]
        new_work=(work_previous+heat*new_gas)/alpha
        photon=coordinates.transform@updated
        photon_previous=coordinates.transform@history
        physical=stiffness@(photon-basis.temperature[:,None]*new_gas)
        residual=basis.mass@(alpha*photon-photon_previous)-rate*physical-rate*original[1:-1]
        normalization=np.maximum(np.linalg.norm(collapse(basis.mass@photon_previous+rate*original[1:-1]),axis=0),1e-300)
        equation_ratios=np.linalg.norm(collapse(residual),axis=0)/normalization
        worst=int(np.argmax(equation_ratios))
        if equation_ratios[worst]>1e-7 and equation_ratios[worst]>maxima['photon_equation']:
            scale_parts=np.linalg.norm(collapse(basis.mass@(alpha*photon)),axis=0)+np.linalg.norm(collapse(basis.mass@photon_previous),axis=0)+np.linalg.norm(collapse(rate*physical),axis=0)+np.linalg.norm(collapse(rate*original[1:-1]),axis=0)
            print(json.dumps(dict(probe_label=label,step=index,column=worst,group=GROUPS[worst//2],old_ratio=float(equation_ratios[worst]),
                residual_norm=float(np.linalg.norm(collapse(residual),axis=0)[worst]),old_denominator=float(normalization[worst]),
                terms_denominator=float(scale_parts[worst]),full_equation_ratio=float(np.linalg.norm(collapse(residual),axis=0)[worst]/max(scale_parts[worst],1e-300)))),flush=True)
        maxima['photon_equation']=max(maxima['photon_equation'],float(np.max(equation_ratios)))
        gas_residual=heat*((alpha+1)*new_gas-gas_previous)+rate*basis.temperature@physical-rate*original[-1]
        maxima['gas_equation']=max(maxima['gas_equation'],float(np.max(abs(collapse(gas_residual)))))
        spectral=collapse(basis.energy@photon)
        allowance=256*np.finfo(float).eps*np.maximum(abs(basis.energy)@abs(collapse(photon)),1e-300)
        maxima['spectral_energy_roundoff']=max(maxima['spectral_energy_roundoff'],float(np.max(abs(spectral-collapse(updated[0]))/allowance)))
        new_created=(number_previous+rate*basis.chemical@(physical+spectral_source))/alpha
        previous,state=state,updated
        old_gas,gas=gas,new_gas
        old_work,work=work,new_work
        old_created,created=created,new_created
        old_injected,injected=injected,new_injected
        injected_history.append(injected.copy())
        histories.append(state.copy())
        gas_history.append(gas.copy())
        work_history.append(work.copy())
        number_history.append(created.copy())
        if index%512==0:
            print(json.dumps(dict(label=label,step=index,total=count,utc=datetime.now(timezone.utc).isoformat())),flush=True)
    histories=np.array(histories)
    photons=np.einsum('ij,njk->nik',coordinates.transform,histories)
    gases,works,numbers=map(np.asarray,[gas_history,work_history,number_history])
    energy=histories[:,0]
    injected_history=np.asarray(injected_history)
    balance=collapse(energy+background.chi*gases+works-injected_history)
    scale=np.maximum(np.max(abs(collapse(energy))+abs(background.chi*collapse(gases))+abs(collapse(works))+abs(collapse(injected_history)),axis=0),1e-300)
    budget=float(np.max(abs(balance-balance[0])/scale))
    number_moment=np.einsum('i,nij->nj',basis.number,photons)
    number_scale=np.maximum(np.max(abs(collapse(number_moment))+abs(collapse(numbers)),axis=0),1e-300)
    number_error=float(np.max(abs(collapse((number_moment-numbers)-(number_moment[0]-numbers[0])))/number_scale))
    checks=[]
    for name,value,limit in [('Source rewrite',maxima['source_rewrite'],1e-10),
                             ('Original photon equations',maxima['photon_equation'],1e-7),
                             ('Original gas equation',maxima['gas_equation'],1e-8),
                             ('Spectral energy roundoff',maxima['spectral_energy_roundoff'],1.),
                             ('Energy/work minus recorded source imbalance',budget,1e-7),
                             ('Carried photon number bookkeeping',number_error,1e-7)]:
        test(checks,name+':'+label,value,limit)
    result=dict(coordinate=np.linspace(begin,end,count+1),photon=photons,energy=energy,gas=gases,
                work=works,number=number_moment,integrated_number_source=numbers,integrated_imbalance=injected_history)
    for key in ['photon','energy','gas','work','number','integrated_number_source','integrated_imbalance']:
        value=result[key]
        width=value.shape[-1]//2
        result[key+'_high']=value[...,:width].copy()
        result[key+'_low']=value[...,width:].copy()
        result[key]=collapse(value)
    for key in ['photon','energy','gas','work','number','integrated_number_source','integrated_imbalance']:
        value=result[key]
        assert np.array_equal(value[...,6:8],np.zeros_like(value[...,6:8]))
        errors=[value[...,2:4]-value[...,:2]-value[...,4:6],
                value[...,10:12]-value[...,8:10]-value[...,2:4]]
        for identity,error in zip(['current=old+endpoint','raw=current+raw_difference'],errors):
            expected=value[...,2:4] if identity=='current=old+endpoint' else value[...,10:12]
            denominator=max(float(np.max(abs(expected))),1e-300)
            test(checks,'Independent superposition:'+label+':'+key+':'+identity,
                 np.max(abs(error))/denominator,1e-8)
    maxima['legacy_combined_reference_normalization']=max(
        float(np.max(abs(result[key][...,10:12]-result[key][...,8:10]-result[key][...,2:4])))/
        max(float(np.max(abs(result[key][...,2:4]))),1e-300)
        for key in ['photon','energy','gas','work','number','integrated_number_source','integrated_imbalance'])
    checks.append(dict(name='Zero extra source gives exactly zero addition:'+label,passed=True))
    return result,checks,dict(budget=budget,number_error=number_error,initial_balance=balance[0].tolist(),**maxima)



def terminal(result):
    names=['photon','energy','gas','work','integrated_number_source']
    return {key:result[key][-1].copy() for name in names for key in [name,name+'_high',name+'_low']}


if __name__=='__main__':
    modest()
    evaluator=HeldoutSources()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    for model in ['heavy','cold']:
        selection=slice(0,2) if model=='heavy' else slice(2,4)
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        initial={key:np.zeros((96,24)) if key=='photon' else np.zeros(24) for key in ['photon','energy','gas','work','integrated_number_source']}
        integrate(model,32,initial,lambda phase:evaluator.forcing(phase,'cubic',selection),ladder,background,emission,.75,1.,model+'-probe')
