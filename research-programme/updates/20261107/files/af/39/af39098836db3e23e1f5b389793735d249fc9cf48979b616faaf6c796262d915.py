from curvature_source_common import *
from inspect_coupled_response import NonlocalEmission,infrared_ladder


class EnergyCoordinates:
    def __init__(self,basis):
        self.basis=basis
        self.pivot=1
        self.others=np.r_[0,np.arange(2,96)]
        self.transform=np.zeros((96,96))
        self.transform[self.pivot,0]=1/basis.energy[self.pivot]
        self.transform[self.others,1:]=np.eye(95)
        self.transform[self.pivot,1:]=-basis.energy[self.others]/basis.energy[self.pivot]
        self.tests=np.vstack([basis.temperature,np.eye(96)[self.others]])
        numerical_mass=self.tests@basis.mass@self.transform
        self.mass=numerical_mass.copy()
        self.mass[0]=np.r_[1.,np.zeros(95)]
        self.mass_rewrite_error=float(np.max(abs(self.mass-numerical_mass)))
        assert self.mass_rewrite_error<1e-12
        assert np.linalg.matrix_rank(self.transform)==96

    def source(self,original):
        energy=original[0]
        spectral=original[1:-1].copy()
        original_gas=original[-1]
        spectral[self.pivot]=(energy-self.basis.temperature[self.others]@spectral[self.others])/self.basis.temperature[self.pivot]
        force=np.vstack([energy,spectral[self.others]])
        correction=spectral-original[1:-1]
        scale=np.maximum(dual_norm(original[1:-1],self.basis.mass),1e-300)
        relative=dual_norm(correction,self.basis.mass)/scale
        assert np.array_equal(spectral[0],original[1])
        return force,spectral,-energy,dict(relative_change=float(relative.max()),
            independent_pair_defect=float(np.max(abs(energy+original_gas))),
            source_temperature_defect=float(np.max(abs(self.basis.temperature@original[1:-1]-energy))))


def run(model,count,anchor,ladder):
    basis=ladder.basis
    coordinates=EnergyCoordinates(basis)
    background=thermal_wave.thermal.ThermalBackground(model)
    emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    start,end=.25*background.end,.5*background.end
    step=(end-start)/count
    selection=slice(0,2) if model=='heavy' else slice(2,4)
    state,previous=np.zeros((96,10)),np.zeros((96,10))
    gas,old_gas,work,old_work,created,old_created=[np.zeros(10) for unused in range(6)]
    saved_states=[state.copy()]
    saved_gas,saved_work,saved_numbers=[gas.copy()],[work.copy()],[created.copy()]
    maxima={key:0. for key in ['source_rewrite','raw_pair','raw_projection','original_photon_relative',
        'original_gas_absolute','energy_roundoff_ratio','step_balance_absolute']}
    for index in range(1,count+1):
        coordinate=start+index*step
        fraction=index/count
        local=background.at(coordinate)
        theta,rate,heat=local['thermal_parameter'],local['coefficient']/local['thermal_parameter'],background.chi
        stiffness=ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr')
        quarter,middle,midpoint=anchor['anchors'][:,:,selection]
        delta=middle-(quarter+midpoint)/2
        secant=(1-fraction)*quarter+fraction*midpoint
        linear=secant+2*min(fraction,1-fraction)*delta
        quadratic=secant+4*fraction*(1-fraction)*delta
        left=max(0.,1-4*abs(fraction-.25))*anchor['early_defect'][:,selection]
        right_defect=max(0.,1-4*abs(fraction-.75))*anchor['late_defect'][:,selection]
        original_source=np.column_stack([linear,quadratic,quadratic+left+right_defect,left,right_defect])
        force,spectral_source,gas_source,source_metrics=coordinates.source(original_source)
        maxima['source_rewrite']=max(maxima['source_rewrite'],source_metrics['relative_change'])
        maxima['raw_pair']=max(maxima['raw_pair'],source_metrics['independent_pair_defect'])
        maxima['raw_projection']=max(maxima['raw_projection'],source_metrics['source_temperature_defect'])
        if index==1:
            alpha=1/step
            history=state/step
            gas_history=gas/step
            work_history=work/step
            number_history=created/step
        else:
            alpha=1.5/step
            history=(2*state-.5*previous)/step
            gas_history=(2*gas-.5*old_gas)/step
            work_history=(2*work-.5*old_work)/step
            number_history=(2*created-.5*old_created)/step
        projected_stiffness=coordinates.tests@stiffness@coordinates.transform
        coupling=-rate*coordinates.tests@stiffness@basis.temperature
        gas_free=(history[0]+heat*gas_history)/(heat*(alpha+1))
        energy_coefficient=alpha/(heat*(alpha+1))
        matrix=alpha*coordinates.mass-rate*projected_stiffness
        matrix[:,0]+=coupling*energy_coefficient
        right=coordinates.mass@history+rate*force+coupling[:,None]*gas_free
        updated=linalg.solve(matrix,right)
        new_gas=gas_free-energy_coefficient*updated[0]
        new_work=(work_history+heat*new_gas)/alpha
        photon=coordinates.transform@updated
        photon_history=coordinates.transform@history
        physical=stiffness@(photon-basis.temperature[:,None]*new_gas)
        derivative=alpha*photon-photon_history
        residual=basis.mass@derivative-rate*physical-rate*original_source[1:-1]
        normalization=max(float(np.linalg.norm(basis.mass@photon_history+rate*original_source[1:-1])),1e-300)
        gas_residual=heat*((alpha+1)*new_gas-gas_history)+rate*basis.temperature@physical-rate*original_source[-1]
        maxima['original_photon_relative']=max(maxima['original_photon_relative'],float(np.linalg.norm(residual)/normalization))
        maxima['original_gas_absolute']=max(maxima['original_gas_absolute'],float(np.max(abs(gas_residual))))
        reconstructed=basis.energy@photon
        roundoff_bound=256*np.finfo(float).eps*np.maximum(abs(basis.energy)@abs(photon),1e-300)
        maxima['energy_roundoff_ratio']=max(maxima['energy_roundoff_ratio'],float(np.max(abs(reconstructed-updated[0])/roundoff_bound)))
        derivative_balance=alpha*updated[0]-history[0]+heat*(alpha*new_gas-gas_history)+heat*new_gas
        maxima['step_balance_absolute']=max(maxima['step_balance_absolute'],float(np.max(abs(derivative_balance))))
        number_rate=rate*basis.chemical@(physical+spectral_source)
        new_created=(number_history+number_rate)/alpha
        previous,state=state,updated
        old_gas,gas=gas,new_gas
        old_work,work=work,new_work
        old_created,created=created,new_created
        saved_states.append(state.copy())
        saved_gas.append(gas.copy())
        saved_work.append(work.copy())
        saved_numbers.append(created.copy())
    states=np.asarray(saved_states)
    photons=np.einsum('ij,njk->nik',coordinates.transform,states)
    gases,works,numbers=np.asarray(saved_gas),np.asarray(saved_work),np.asarray(saved_numbers)
    energy=states[:,0,:]
    balance=energy+background.chi*gases+works
    scale=np.maximum(np.max(abs(energy)+abs(background.chi*gases)+abs(works),axis=0),1e-300)
    relative_balance=float(np.max(abs(balance)/scale))
    number_moment=np.einsum('i,nij->nj',basis.number,photons)
    number_error=float(np.max(abs(number_moment-numbers))/max(np.max(abs(number_moment)),1e-300))
    checks=[
        dict(name=f'Invertible96-mode energy coordinate mass identity:{model}-{count}',value=coordinates.mass_rewrite_error,passed=coordinates.mass_rewrite_error<1e-12),
        dict(name=f'Analytic redundant source reconstruction below1e-10 relative:{model}-{count}',value=maxima['source_rewrite'],passed=maxima['source_rewrite']<1e-10),
        dict(name=f'Original raw photon equations retained:{model}-{count}',value=maxima['original_photon_relative'],passed=maxima['original_photon_relative']<1e-7),
        dict(name=f'Original independent gas equation retained:{model}-{count}',value=maxima['original_gas_absolute'],passed=maxima['original_gas_absolute']<1e-8),
        dict(name=f'Energy plus expansion work without false source leakage:{model}-{count}',value=relative_balance,passed=relative_balance<1e-7),
        dict(name=f'Reconstructed spectral energy agrees within explicit float roundoff allowance:{model}-{count}',value=maxima['energy_roundoff_ratio'],passed=maxima['energy_roundoff_ratio']<1),
        dict(name=f'Photon number response is not projected away:{model}-{count}',value=number_error,passed=number_error<1e-7)]
    result=dict(coordinate=np.linspace(start,end,count+1),photon=photons,energy=energy,gas=gases,work=works,
        number=number_moment,integrated_number_source=numbers,
        energy_from_spectrum=np.einsum('i,nij->nj',basis.energy,photons))
    return result,checks,[*emission.inputs,background.parent.source,background.native_constants],dict(model=model,steps=count,heat=background.chi,
        energy_work_relative=relative_balance,number_relative=number_error,**maxima)


def main():
    modest()
    folder=ROOT/'results/curvature-response'
    folder.mkdir(parents=True,exist_ok=False)
    source_path=ROOT/'results/holdout-sources/source.npz'
    anchor=dict(np.load(source_path))
    audit=json.loads((source_path.parent/'status.json').read_text())
    assert audit['numerical_integrity_all_passed']
    for path,expected in audit['input_hashes'].items():
        assert digest(path)==expected,path
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    endpoint=Spectra(.5)
    checks,rows,inputs,results=[],[],[source_path,source_path.parent/'status.json',ROOT/'DERIVATION.md',*ladder.inputs,*endpoint.inputs],{}
    assert np.array_equal(anchor['mass'],basis.mass)
    def norm(value):
        return np.sqrt(np.maximum(np.sum(value*(basis.mass@value),axis=0),0.))
    def history_norm(value):
        return np.sqrt(np.maximum(np.einsum('nik,ij,njk->nk',value,basis.mass,value),0.))
    for model in ['heavy','cold']:
        solutions={}
        for count in [128,256,512]:
            solved,tests,dependencies,row=run(model,count,anchor,ladder)
            solutions[count]=solved
            checks+=tests
            rows.append(row)
            inputs+=dependencies
            np.savez(folder/f'{model}-{count}.npz',**solved)
            write_json(folder/f'{model}-{count}-diagnostics.json',dict(checks=tests,metrics=row))
        fine,coarse=solutions[512],solutions[256]
        photon_change=norm(fine['photon'][-1]-coarse['photon'][-1])/np.maximum(norm(fine['photon'][-1]),1e-300)
        gas_change=abs(fine['gas'][-1]-coarse['gas'][-1])/np.maximum(np.max(abs(fine['gas']),axis=0),1e-300)
        checks.append(dict(name='All five forcing variants refine within1percent:'+model,
            photon=float(photon_change.max()),gas=float(gas_change.max()),passed=bool(max(photon_change.max(),gas_change.max())<.01)))
        baseline_path=PARENT/'results/withheld-response'/f'{model}-512.npz'
        baseline=dict(np.load(baseline_path))
        inputs.extend([baseline_path,baseline_path.parent/'status.json'])
        assert np.array_equal(fine['coordinate'],baseline['coordinate'])
        replay_photon=history_norm(fine['photon'][:,:,:2]-baseline['photon'][:,:,2:4])/np.maximum(np.max(history_norm(baseline['photon'][:,:,2:4]),axis=0),1e-300)
        replay_gas=abs(fine['gas'][:,:2]-baseline['gas'][:,2:4])/np.maximum(np.max(abs(baseline['gas'][:,2:4]),axis=0),1e-300)
        replay=float(max(replay_photon.max(),replay_gas.max()))
        checks.append(dict(name='Stage103 three-anchor full-trajectory replay:'+model,value=replay,passed=replay<1e-9))
        identity=fine['photon'][:,:,4:6]-fine['photon'][:,:,2:4]-fine['photon'][:,:,6:8]-fine['photon'][:,:,8:10]
        scale=np.max(history_norm(fine['photon'][:,:,6:8]+fine['photon'][:,:,8:10]))
        identity_errors=dict(photon=float(np.max(history_norm(identity))/max(scale,1e-300)))
        for key in ['gas','energy','work','number']:
            residual=fine[key][:,4:6]-fine[key][:,2:4]-fine[key][:,6:8]-fine[key][:,8:10]
            scale=np.max(abs(fine[key][:,6:8])+abs(fine[key][:,8:10]))
            identity_errors[key]=float(np.max(abs(residual))/max(scale,1e-300))
        checks.append(dict(name='Two-local-hat response identity at every step:'+model,
            errors=identity_errors,passed=max(identity_errors.values())<1e-8))
        linear,quadratic,corrected,left,right=np.split(fine['photon'][-1],5,axis=1)
        photon_error=norm(corrected-quadratic)/np.maximum(norm(corrected),1e-300)
        gas_error=abs(fine['gas'][-1,4:6]-fine['gas'][-1,2:4])/np.maximum(np.max(abs(fine['gas'][:,4:6]),axis=0),1e-300)
        photon_history_error=np.max(history_norm(fine['photon'][:,:,4:6]-fine['photon'][:,:,2:4]),axis=0)/np.maximum(np.max(history_norm(fine['photon'][:,:,4:6]),axis=0),1e-300)
        gas_history_error=np.max(abs(fine['gas'][:,4:6]-fine['gas'][:,2:4]),axis=0)/np.maximum(np.max(abs(fine['gas'][:,4:6]),axis=0),1e-300)
        baseline_error=norm(corrected-linear)/np.maximum(norm(corrected),1e-300)
        baseline_gas_error=abs(fine['gas'][-1,4:6]-fine['gas'][-1,:2])/np.maximum(np.max(abs(fine['gas'][:,4:6]),axis=0),1e-300)
        for join in range(2):
            checks.append(dict(name=f'FROZEN_FORECAST: quadratic photon response within1percent:{model}-join{join+1}',
                value=float(photon_error[join]),passed=bool(photon_error[join]<=.01)))
            checks.append(dict(name=f'FROZEN_FORECAST: quadratic gas response within1percent:{model}-join{join+1}',
                value=float(gas_error[join]),passed=bool(gas_error[join]<=.01)))
        parent_profile=np.asarray(endpoint.original[model])
        assert parent_profile.shape==(96,)
        parent_norm=float(norm(parent_profile[:,None])[0])
        parent_gas=float(endpoint.gas[0 if model=='heavy' else 1])
        results[model]=dict(step_photon_relative=photon_change.tolist(),step_gas_relative_to_peak=gas_change.tolist(),
            baseline_replay_max=replay,local_hat_identity_errors=identity_errors,
            quadratic_endpoint_photon_error=photon_error.tolist(),quadratic_endpoint_gas_error=gas_error.tolist(),
            quadratic_history_photon_error=photon_history_error.tolist(),quadratic_history_gas_error=gas_history_error.tolist(),
            linear_endpoint_photon_error=baseline_error.tolist(),linear_endpoint_gas_error=baseline_gas_error.tolist(),
            final_corrected_photon_norm=norm(corrected).tolist(),
            interval_increment_relative_to_saved_endpoint_departure=(norm(corrected)/max(parent_norm,1e-300)).tolist(),
            interval_gas_increment_relative_to_saved_endpoint_gas=(abs(fine['gas'][-1,4:6])/abs(parent_gas)).tolist() if parent_gas!=0 else None,
            saved_endpoint_photon_departure_norm=parent_norm,saved_endpoint_gas=parent_gas,
            final_gas=fine['gas'][-1].tolist(),final_energy=fine['energy'][-1].tolist(),
            final_work=fine['work'][-1].tolist(),final_number=fine['number'][-1].tolist())
    structural=[row for row in checks if not row['name'].startswith('FROZEN_FORECAST:')]
    structural_passed=all(bool(row['passed']) for row in structural)
    finish(folder,dict(checks=checks,rows=rows,response_results=results,
        numerical_integrity_all_passed=structural_passed,energy_coordinate_is_invertible=True,
        column_order=['linear-join1','linear-join2','quadratic-join1','quadratic-join2','corrected-join1','corrected-join2','left-defect-join1','left-defect-join2','right-defect-join1','right-defect-join2'],
        number_source_unchanged=True,independent_energy_source_used=True,
        source_interpolation_error_bounded=False,new_epoch_precision_gate_closed=False,new_parent_history=False,
        first_order_fixed_geometry_response=True,correction_initial_condition='Zero at .25,increment to .5.',
        forcing_interpolation='Three-anchor quadratic plus two independently measured local hat defects;original three-anchor linear baseline retained.'),__file__,inputs)
    print(json.dumps(dict(response_results=results,failed=[row['name'] for row in checks if not row['passed']],
        maximum_energy_work_residual=max(row['energy_work_relative'] for row in rows))),flush=True)
    if not structural_passed:
        raise SystemExit(1)


if __name__=='__main__':
    main()

