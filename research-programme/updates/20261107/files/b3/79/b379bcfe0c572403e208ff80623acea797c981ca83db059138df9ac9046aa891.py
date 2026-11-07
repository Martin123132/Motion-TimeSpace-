from seven_eighths_history_common import *
from matched_feedback_common import EnergyCoordinates


def solve_response_trace(model,source,steps,ladder,emission,background,trace):
    basis=ladder.basis
    coordinates=EnergyCoordinates(basis)
    forcing=interpolate.interp1d(source['coordinate'],source['source'],axis=0,bounds_error=True)
    start,end=source['coordinate'][[0,-1]]
    step=(end-start)/steps
    state,previous=np.zeros((96,12)),np.zeros((96,12))
    gas,old_gas,work,old_work,created,old_created=[np.zeros(12) for unused in range(6)]
    states,gases,works,numbers=[state.copy()],[gas.copy()],[work.copy()],[created.copy()]
    errors={key:0. for key in ['photon','gas','energy_spectrum','energy_step']}
    for index in range(1,steps+1):
        position=float(start+(end-start)*index/steps)
        local=background.at(position)
        theta,rate,heat=local['thermal_parameter'],local['coefficient']/local['thermal_parameter'],background.chi
        stiffness=ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr')
        pieces=forcing(position)
        external=np.column_stack([pieces.sum(axis=0),*pieces])
        force=coordinates.tests@external
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
        matrix=alpha*coordinates.mass-rate*coordinates.tests@stiffness@coordinates.transform
        coupling=-rate*coordinates.tests@stiffness@basis.temperature
        gas_free=(history[0]+heat*gas_history)/(heat*(alpha+1))
        energy_coefficient=alpha/(heat*(alpha+1))
        matrix[:,0]+=coupling*energy_coefficient
        right=coordinates.mass@history+rate*force+coupling[:,None]*gas_free
        updated=linalg.solve(matrix,right)
        new_gas=gas_free-energy_coefficient*updated[0]
        new_work=(work_history+heat*new_gas)/alpha
        photon=coordinates.transform@updated
        photon_history=coordinates.transform@history
        physical=stiffness@(photon-basis.temperature[:,None]*new_gas)+external
        derivative=alpha*photon-photon_history
        residual=basis.mass@derivative-rate*physical
        scale=np.maximum(np.linalg.norm(basis.mass@photon_history,axis=0)+np.linalg.norm(rate*physical,axis=0)+np.linalg.norm(alpha*basis.mass@photon,axis=0),1e-300)
        errors['photon']=max(errors['photon'],float(np.max(np.linalg.norm(residual,axis=0)/scale)))
        gas_residual=heat*((alpha+1)*new_gas-gas_history)+rate*basis.temperature@physical
        gas_scale=np.maximum(abs(heat*(alpha+1)*new_gas)+abs(heat*gas_history)+abs(rate)*abs(basis.temperature)@abs(physical),1e-300)
        errors['gas']=max(errors['gas'],float(np.max(abs(gas_residual)/gas_scale)))
        if trace is not None:
            trace(index,photon,abs(gas_residual)/gas_scale)
        spectrum_energy=basis.energy@photon
        allowance=256*np.finfo(float).eps*np.maximum(abs(basis.energy)@abs(photon),1e-300)
        errors['energy_spectrum']=max(errors['energy_spectrum'],float(np.max(abs(spectrum_energy-updated[0])/allowance)))
        energy_error=alpha*updated[0]-history[0]+heat*((alpha+1)*new_gas-gas_history)
        energy_scale=np.maximum(abs(alpha*updated[0])+abs(history[0])+heat*(abs((alpha+1)*new_gas)+abs(gas_history)),1e-300)
        errors['energy_step']=max(errors['energy_step'],float(np.max(abs(energy_error)/energy_scale)))
        number_rate=rate*basis.chemical@physical
        new_created=(number_history+number_rate)/alpha
        previous,state=state,updated
        old_gas,gas=gas,new_gas
        old_work,work=work,new_work
        old_created,created=created,new_created
        states.append(state.copy())
        gases.append(gas.copy())
        works.append(work.copy())
        numbers.append(created.copy())
    states=np.array(states)
    photons=np.einsum('ij,njk->nik',coordinates.transform,states)
    gases,works,numbers=np.array(gases),np.array(works),np.array(numbers)
    energy=states[:,0]
    number_moment=np.einsum('i,nik->nk',basis.number,photons)
    energy_scale=np.maximum(np.max(abs(energy)+background.chi*abs(gases)+abs(works),axis=0),1e-300)
    number_scale=np.maximum(np.max(abs(number_moment)+abs(numbers),axis=0),1e-300)
    errors['energy_work']=float(np.max(abs(energy+background.chi*gases+works)/energy_scale))
    errors['number']=float(np.max(abs(number_moment-numbers)/number_scale))
    components=[photons[:,:,offset:offset+3] for offset in [3,6,9]]
    component_norm=sum(photon_norm(component,basis.mass) for component in components)
    errors['linearity']=float(np.max(photon_norm(photons[:,:,:3]-sum(components),basis.mass)/np.maximum(component_norm.max(axis=0),1e-300)))
    return dict(coordinate=np.linspace(start,end,steps+1),photon=photons,gas=gases,energy=energy,work=works,number=number_moment,integrated_number=numbers),errors
