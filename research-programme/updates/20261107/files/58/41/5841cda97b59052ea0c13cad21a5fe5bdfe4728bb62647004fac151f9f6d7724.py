from consecutive_common import *
import mpmath as mp
import argparse
import time


def mp_columns(left,right):
    joined=mp.matrix(left.rows,left.cols+right.cols)
    for row in range(joined.rows):
        for column in range(left.cols):
            joined[row,column]=left[row,column]
            joined[row,column+left.cols]=right[row,column]
    return joined


def coupled_matrix(mass,temperature,heat,alpha,stiffness,rate):
    spectral=alpha*mass-rate*stiffness
    column=rate*stiffness*temperature
    row=rate*temperature.T*stiffness
    matrix=mp.matrix(97,97)
    for index in range(96):
        for other in range(96):
            matrix[index,other]=spectral[index,other]
        matrix[index,96]=column[index]
        matrix[96,index]=row[index]
    matrix[96,96]=heat*(alpha+1)-(row*temperature)[0]
    return matrix


def evolve(data,digits,folder):
    with mp.workdps(digits):
        mass=mp.matrix(data['mass'].tolist())
        temperature=mp.matrix(data['temperature'].tolist())
        heat,step=mp.mpf(float(data['heat'])),mp.mpf(float(data['step']))
        alpha=mp.mpf('1.5')/step
        storage=mp.matrix(97,97)
        for row in range(96):
            for column in range(96):
                storage[row,column]=mass[row,column]
        storage[96,96]=heat
        older=mp.matrix(data['reference'][0].tolist())
        previous=mp.matrix(data['reference'][1].tolist())
        records=[]
        for offset,index in enumerate(data['indices']):
            reference=mp.matrix(data['reference'][offset+2].tolist())
            old_reference=mp.matrix(data['reference'][offset+1].tolist())
            older_reference=mp.matrix(data['reference'][offset].tolist())
            stiffness=mp.matrix(data['stiffness'][offset].tolist())
            rate=mp.mpf(float(data['rate'][offset]))
            external=mp.matrix(data['external'][offset].tolist())
            forcing=mp.matrix(97,3)
            gas_force=-rate*temperature.T*external
            for row in range(96):
                for column in range(3):
                    forcing[row,column]=rate*external[row,column]
            for column in range(3):
                forcing[96,column]=gas_force[column]
            history=(2*previous-mp.mpf('.5')*older)/step
            reset_history=(2*old_reference-mp.mpf('.5')*older_reference)/step
            all_history=mp_columns(history,reset_history)
            right=storage*all_history+mp_columns(forcing,forcing)
            matrix=coupled_matrix(mass,temperature,heat,alpha,stiffness,rate)
            combined,pivots=mp.mp.LU_decomp(matrix)
            solved=mp.matrix(97,6)
            for column in range(6):
                answer=mp.mp.U_solve(combined,mp.mp.L_solve(combined,right.column(column),pivots))
                for row in range(97):
                    solved[row,column]=answer[row]
            photon,gas=solved[:96,:],solved[96:97,:]
            physical=stiffness*(photon-temperature*gas)+mp_columns(external,external)
            photon_residual=mass*(alpha*photon-all_history[:96,:])-rate*physical
            gas_residual=heat*((alpha+1)*gas-all_history[96:97,:])+rate*temperature.T*physical
            photon_errors,gas_errors,energy_errors=[],[],[]
            for column in range(6):
                photon_scale=mp.norm(alpha*mass*photon.column(column))+mp.norm(mass*all_history[:96,column])+mp.norm(rate*physical.column(column))
                gas_scale=abs(heat*(alpha+1)*gas[column])+abs(heat*all_history[96,column])+abs(rate)*mp.fsum(abs(temperature[row])*abs(physical[row,column]) for row in range(96))
                energy=(temperature.T*mass*(alpha*photon.column(column)-all_history[:96,column]))[0]+heat*((alpha+1)*gas[column]-all_history[96,column])
                energy_scale=abs((temperature.T*mass*(alpha*photon.column(column)))[0])+abs((temperature.T*mass*all_history[:96,column])[0])+abs(heat*(alpha+1)*gas[column])+abs(heat*all_history[96,column])
                photon_errors.append(float(mp.norm(photon_residual.column(column))/max(photon_scale,mp.mpf('1e-300'))))
                gas_errors.append(float(abs(gas_residual[column])/max(gas_scale,mp.mpf('1e-300'))))
                energy_errors.append(float(abs(energy)/max(energy_scale,mp.mpf('1e-300'))))
            accumulated=solved[:,:3]
            delta=accumulated-reference
            delta_history=(2*(previous-old_reference)-mp.mpf('.5')*(older-older_reference))/step
            raw_residual=matrix*reference-storage*reset_history-forcing
            identity=matrix*delta-storage*delta_history+raw_residual
            identity_scale=mp.norm(matrix*reference)+mp.norm(storage*reset_history+forcing)+mp.norm(matrix*delta)+mp.norm(storage*delta_history)
            identity_error=float(mp.norm(identity)/max(identity_scale,mp.mpf('1e-300')))
            gas_accum,gas_reset,photon_accum=[],[],[]
            for column in range(3):
                peak=mp.mpf(float(data['gas_peak'][column]))
                gas_accum.append(float(abs(delta[96,column])/peak))
                gas_reset.append(float(abs(solved[96,column+3]-reference[96,column])/peak))
                difference=delta[:96,column]
                photon_accum.append(float(mp.sqrt(max((difference.T*mass*difference)[0],0))/mp.mpf(float(data['photon_peak'][column]))))
            cast=np.array(solved.tolist(),dtype=float)
            cast_previous=np.array(mp_columns(previous,old_reference).tolist(),dtype=float)
            cast_older=np.array(mp_columns(older,older_reference).tolist(),dtype=float)
            cast_history=(2*cast_previous-.5*cast_older)/float(data['step'])
            cast_physical=data['stiffness'][offset]@(cast[:96]-data['temperature'][:,None]*cast[96])+np.tile(data['external'][offset],(1,2))
            cast_alpha=1.5/float(data['step'])
            cast_residual=data['heat']*((cast_alpha+1)*cast[96]-cast_history[96])+data['rate'][offset]*data['temperature']@cast_physical
            cast_scale=np.maximum(abs(data['heat']*(cast_alpha+1)*cast[96])+abs(data['heat']*cast_history[96])+abs(data['rate'][offset])*abs(data['temperature'])@abs(cast_physical),1e-300)
            record=dict(index=int(index),digits=digits,solution=[[mp.nstr(solved[row,column],digits+12) for column in range(6)] for row in range(97)],
                photon_relative=photon_errors,gas_relative=gas_errors,energy_relative=energy_errors,error_recurrence_relative=identity_error,
                gas_accumulated_change_over_peak=gas_accum,gas_reset_change_over_peak=gas_reset,
                photon_accumulated_change_over_peak=photon_accum,cast_gas_relative=(abs(cast_residual)/cast_scale).tolist())
            path=folder/f'digits{digits}-step{int(index):04d}.json'
            assert not path.exists()
            write_json(path,record)
            records.append(record)
            older,previous=previous,accumulated
            if (offset+1)%8==0:
                progress=dict(state='running',digits=digits,completed=offset+1,total=len(data['indices']),step=int(index),
                    peak_gas_delta=max(gas_accum))
                write_json(folder/'progress.json',progress)
                print(json.dumps(progress),flush=True)
        return records


def compare_precisions(lower,higher):
    agreement=np.zeros(3)
    gas_agreement=np.zeros(3)
    with mp.workdps(90):
        for first,second in zip(lower,higher):
            assert first['index']==second['index']
            low,high=mp.matrix(first['solution']),mp.matrix(second['solution'])
            for column in range(3):
                agreement[column]=max(agreement[column],float(mp.norm(low[:96,column]-high[:96,column])/max(mp.norm(high[:96,column]),mp.mpf('1e-300'))))
                gas_agreement[column]=max(gas_agreement[column],float(abs(low[96,column]-high[96,column])/max(abs(high[96,column]),mp.mpf('1e-300'))))
    return agreement,gas_agreement


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--upper',type=float,choices=[.04,.02],required=True)
    parser.add_argument('--centre',choices=['baseline','mts'],required=True)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    folder=ROOT/'results'/f'consecutive-{args.model}-m{int(args.upper*1000)}-{args.centre}'
    folder.mkdir(parents=True,exist_ok=False)
    parent_precision=PARENT/'results'/f'gas-precision-m{int(args.upper*1000)}/status.json'
    parent_packet=local_packet(parent_precision.parent)
    selection=parent_packet['selections'][args.model]
    chosen=0 if args.centre=='baseline' else 1+int(np.argmax(selection['raw_maximum_by_column'][1:3]))
    centre=int(selection['worst_step_by_column'][chosen])
    start=max(2,min(centre-16,2048-31))
    indices=np.arange(start,start+32)
    source_folder=ROOT/'results'/f'feedback-m{int(args.upper*1000)}-n5120'
    local_packet(source_folder)
    source_path,response_path=source_folder/(args.model+'-source.npz'),source_folder/(args.model+'-response.npz')
    source,response=read_npz(source_path),read_npz(response_path)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    background=thermal_wave.thermal.ThermalBackground(args.model)
    emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    forcing=interpolate.interp1d(source['coordinate'],source['source'],axis=0,bounds_error=True)
    stiffness,rates,external=[],[],[]
    for index in indices:
        position=float(source['coordinate'][0]+(source['coordinate'][-1]-source['coordinate'][0])*int(index)/2048)
        local=background.at(position)
        theta=local['thermal_parameter']
        stiffness.append(ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr'))
        rates.append(local['coefficient']/theta)
        external.append(forcing(position).sum(axis=0))
    reference=np.concatenate([response['photon'][start-2:start+32,:,:3],response['gas'][start-2:start+32,None,:3]],axis=1)
    data=dict(mass=basis.mass,temperature=basis.temperature,heat=background.chi,
        step=(source['coordinate'][-1]-source['coordinate'][0])/2048,indices=indices,
        stiffness=np.array(stiffness),rate=np.array(rates),external=np.array(external),reference=reference,
        gas_peak=np.maximum(abs(response['gas'][:,:3]).max(axis=0),1e-300),
        photon_peak=np.maximum(photon_norm(response['photon'][:,:,:3],basis.mass).max(axis=0),1e-300))
    np.savez_compressed(folder/'inputs.npz',**data)
    provenance=dict(model=args.model,upper=args.upper,centre_kind=args.centre,centre_step=centre,selected_column=chosen,
        start_step=int(indices[0]),end_step=int(indices[-1]),steps=32,parent_selection_source=str(parent_precision),
        source_path=str(source_path),response_path=str(response_path),script_sha256=digest(__file__),
        initial_states_only_from_binary64=True,subsequent_states_carried_without_cast=True,reset_control=True)
    write_json(folder/'provenance.json',provenance)
    lower,higher=evolve(data,50,folder),evolve(data,70,folder)
    photon_agreement,gas_agreement=compare_precisions(lower,higher)
    checks=[]
    for digits,records in [(50,lower),(70,higher)]:
        for quantity in ['photon_relative','gas_relative','energy_relative']:
            checks.append(check(f'digits{digits}:'+quantity,max(max(row[quantity]) for row in records),1e-35))
        checks.append(check(f'digits{digits}:error recurrence',max(row['error_recurrence_relative'] for row in records),1e-35))
    accumulated=np.array([row['gas_accumulated_change_over_peak'] for row in higher])
    reset=np.array([row['gas_reset_change_over_peak'] for row in higher])
    photon=np.array([row['photon_accumulated_change_over_peak'] for row in higher])
    cast=np.array([row['cast_gas_relative'] for row in higher])
    for column,label in enumerate(['baseline','join1','join2']):
        checks.extend([check('50to70 photon:'+label,photon_agreement[column],1e-25),
            check('50to70 gas:'+label,gas_agreement[column],1e-25),
            check('Accumulated gas numerical stress:'+label,accumulated[:,column].max(),1e-6),
            check('Cast raw gas accumulated:'+label,cast[:,column].max(),1e-7),
            check('Cast raw gas reset:'+label,cast[:,column+3].max(),1e-7)])
    inputs=[*ladder.inputs,*emission.inputs,background.parent.source,background.native_constants,
        parent_precision,source_path,response_path,source_folder/'status.json']
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    metrics=dict(gas_accumulated_max_over_saved_peak=accumulated.max(axis=0).tolist(),
        gas_reset_max_over_saved_peak=reset.max(axis=0).tolist(),
        accumulated_to_reset_peak_ratio=(accumulated.max(axis=0)/np.maximum(reset.max(axis=0),1e-300)).tolist(),
        photon_accumulated_max_over_saved_peak=photon.max(axis=0).tolist(),
        gas_accumulated_endpoint_over_saved_peak=accumulated[-1].tolist(),
        photon50to70=photon_agreement.tolist(),gas50to70=gas_agreement.tolist(),
        cast_raw_gas_max=cast.max(axis=0).tolist())
    write_json(folder/'progress.json',dict(state='complete',steps=32,precisions=[50,70]))
    finish(folder,dict(checks=checks,metrics=metrics,**provenance,precision_digits=[50,70],
        full_history_high_precision=False,raw_gas_flags_retained=True,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(model=args.model,upper=args.upper,centre=args.centre,metrics=metrics,
        failed=[row for row in checks if not row['passed']],seconds=time.monotonic()-started)),flush=True)


if __name__=='__main__':
    main()
