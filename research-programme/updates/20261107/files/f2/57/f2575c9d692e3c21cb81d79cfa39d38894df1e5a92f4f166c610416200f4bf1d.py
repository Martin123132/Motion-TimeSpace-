from consecutive_common import *
import mpmath as mp
from validate_finer import verify_precise
from evolve_precision_segment import mp_columns,coupled_matrix


def validate_segment(folder,ladder):
    basis=ladder.basis
    packet=local_packet(folder)
    data=read_npz(folder/'inputs.npz')
    model,upper=packet['model'],packet['upper']
    source_path,response_path=Path(packet['source_path']),Path(packet['response_path'])
    source,response=read_npz(source_path),read_npz(response_path)
    selector=local_packet(Path(packet['parent_selection_source']).parent)['selections'][model]
    chosen=0 if packet['centre_kind']=='baseline' else 1+int(np.argmax(selector['raw_maximum_by_column'][1:3]))
    centre=int(selector['worst_step_by_column'][chosen])
    start=max(2,min(centre-16,2048-31))
    assert packet['centre_step']==centre and packet['selected_column']==chosen
    assert packet['start_step']==start and packet['end_step']==start+31
    assert np.array_equal(data['indices'],np.arange(start,start+32))
    reference=np.concatenate([response['photon'][start-2:start+32,:,:3],response['gas'][start-2:start+32,None,:3]],axis=1)
    background=thermal_wave.thermal.ThermalBackground(model)
    emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    forcing=interpolate.interp1d(source['coordinate'],source['source'],axis=0,bounds_error=True)
    expected=dict(reference=reference,mass=basis.mass,temperature=basis.temperature,heat=background.chi,
        step=(source['coordinate'][-1]-source['coordinate'][0])/2048,
        gas_peak=np.maximum(abs(response['gas'][:,:3]).max(axis=0),1e-300),
        photon_peak=np.maximum(photon_norm(response['photon'][:,:,:3],basis.mass).max(axis=0),1e-300))
    for key,value in expected.items():
        assert np.array_equal(data[key],value),(folder,key)
    for offset,index in enumerate(data['indices']):
        position=float(source['coordinate'][0]+(source['coordinate'][-1]-source['coordinate'][0])*int(index)/2048)
        local=background.at(position)
        theta=local['thermal_parameter']
        assert np.array_equal(data['stiffness'][offset],ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr'))
        assert data['rate'][offset]==local['coefficient']/theta
        assert np.array_equal(data['external'][offset],forcing(position).sum(axis=0))
    checks=[dict(name=folder.name+':inputs and preselected interval',passed=True)]
    inputs=[folder/'inputs.npz',folder/'provenance.json']
    saved={}
    with mp.workdps(90):
        mass,temperature=mp.matrix(data['mass'].tolist()),mp.matrix(data['temperature'].tolist())
        heat,step=mp.mpf(float(data['heat'])),mp.mpf(float(data['step']))
        alpha=mp.mpf('1.5')/step
        for digits in [50,70]:
            older=mp.matrix(reference[0].tolist())
            previous=mp.matrix(reference[1].tolist())
            records=[]
            accumulated=[]
            reset=[]
            for offset,index in enumerate(data['indices']):
                path=folder/f'digits{digits}-step{int(index):04d}.json'
                record=json.loads(path.read_text())
                inputs.append(path)
                assert record['index']==int(index) and record['digits']==digits
                old_reference=mp.matrix(reference[offset+1].tolist())
                older_reference=mp.matrix(reference[offset].tolist())
                current_reference=mp.matrix(reference[offset+2].tolist())
                prior=mp_columns(previous,old_reference)
                prior_old=mp_columns(older,older_reference)
                witness=dict(mass=data['mass'],stiffness=data['stiffness'][offset],temperature=data['temperature'],
                    heat=data['heat'],step=data['step'],index=int(index),rate=data['rate'][offset],
                    external=np.tile(data['external'][offset],(1,2)),
                    previous_photon=np.array(prior[:96,:].tolist(),dtype=object),
                    older_photon=np.array(prior_old[:96,:].tolist(),dtype=object),
                    previous_gas=np.array(prior[96:97,:].tolist()[0],dtype=object),
                    older_gas=np.array(prior_old[96:97,:].tolist()[0],dtype=object))
                error=verify_precise(witness,record)
                solved=mp.matrix(record['solution'])
                assert all(mp.isfinite(value) for value in solved)
                history=(2*prior-mp.mpf('.5')*prior_old)/step
                energy_error=mp.mpf(0)
                for column in range(6):
                    change=(temperature.T*mass*(alpha*solved[:96,column]-history[:96,column]))[0]+heat*((alpha+1)*solved[96,column]-history[96,column])
                    scale=abs((temperature.T*mass*(alpha*solved[:96,column]))[0])+abs((temperature.T*mass*history[:96,column])[0])+abs(heat*(alpha+1)*solved[96,column])+abs(heat*history[96,column])
                    energy_error=max(energy_error,abs(change)/max(scale,mp.mpf('1e-300')))
                assert energy_error<=mp.mpf('1e-35'),(folder,index,digits,energy_error)
                stiffness=mp.matrix(data['stiffness'][offset].tolist())
                rate=mp.mpf(float(data['rate'][offset]))
                external=mp.matrix(data['external'][offset].tolist())
                delta=solved[:,:3]-current_reference
                history_delta=(2*(previous-old_reference)-mp.mpf('.5')*(older-older_reference))/step
                double_history=(2*old_reference-mp.mpf('.5')*older_reference)/step
                error_photon=mass*(alpha*delta[:96,:]-history_delta[:96,:])-rate*stiffness*(delta[:96,:]-temperature*delta[96:97,:])
                error_gas=heat*((alpha+1)*delta[96:97,:]-history_delta[96:97,:])+rate*temperature.T*stiffness*(delta[:96,:]-temperature*delta[96:97,:])
                double_physical=stiffness*(current_reference[:96,:]-temperature*current_reference[96:97,:])+external
                double_photon=mass*(alpha*current_reference[:96,:]-double_history[:96,:])-rate*double_physical
                double_gas=heat*((alpha+1)*current_reference[96:97,:]-double_history[96:97,:])+rate*temperature.T*double_physical
                operand=mp.norm(alpha*mass*current_reference[:96,:])+mp.norm(mass*double_history[:96,:])+mp.norm(rate*double_physical)+mp.norm(heat*(alpha+1)*current_reference[96:97,:])+mp.norm(heat*double_history[96:97,:])
                recurrence=(mp.norm(error_photon+double_photon)+mp.norm(error_gas+double_gas))/max(operand,mp.mpf('1e-300'))
                assert recurrence<=mp.mpf('1e-35'),(folder,index,digits,recurrence)
                changes=[float(abs(delta[96,column])/mp.mpf(float(data['gas_peak'][column]))) for column in range(3)]
                reset_changes=[float(abs(solved[96,column+3]-current_reference[96,column])/mp.mpf(float(data['gas_peak'][column]))) for column in range(3)]
                assert np.allclose(changes,record['gas_accumulated_change_over_peak'],rtol=1e-9,atol=1e-28)
                assert np.allclose(reset_changes,record['gas_reset_change_over_peak'],rtol=1e-9,atol=1e-28)
                accumulated.append(changes)
                reset.append(reset_changes)
                checks.append(dict(name=f'{folder.name}:digits{digits}:step{int(index)} physical equations and error recurrence',
                    value=max(error,float(recurrence),float(energy_error)),limit=1e-35,passed=True))
                records.append(record)
                older,previous=previous,solved[:,:3]
            saved[digits]=records
            if digits==70:
                assert np.allclose(np.max(accumulated,axis=0),packet['metrics']['gas_accumulated_max_over_saved_peak'],rtol=1e-9,atol=1e-28)
                assert np.allclose(np.max(reset,axis=0),packet['metrics']['gas_reset_max_over_saved_peak'],rtol=1e-9,atol=1e-28)
        maximum=mp.mpf(0)
        for lower,higher in zip(saved[50],saved[70]):
            first,second=mp.matrix(lower['solution']),mp.matrix(higher['solution'])
            for column in range(6):
                maximum=max(maximum,mp.norm(first[:96,column]-second[:96,column])/max(mp.norm(second[:96,column]),mp.mpf('1e-300')),
                    abs(first[96,column]-second[96,column])/max(abs(second[96,column]),mp.mpf('1e-300')))
        assert maximum<=mp.mpf('1e-25'),(folder,maximum)
        checks.append(dict(name=folder.name+':independent50/70 trajectory and reset agreement',value=float(maximum),limit=1e-25,passed=True))
    return checks,inputs
