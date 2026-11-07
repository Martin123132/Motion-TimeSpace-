from join_common import *
import time


def reference_source(order,panel,upper,model):
    label=f'fine-o{order}-q{panel}-m40' if upper==.04 else 'fine-o6-q32-m20'
    return PARENT/'results'/('sources-'+label)/(model+'.npz')


def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--order',type=int,choices=[6,8],required=True)
    parser.add_argument('--panel',type=int,choices=[32,48],default=32)
    parser.add_argument('--pilot',action='store_true')
    args=parser.parse_args()
    modest()
    label=f'o{args.order}-q{args.panel}'
    folder=ROOT/'results'/(('pilot-' if args.pilot else 'sources-')+label)
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=[*ladder.inputs]
    predictions,profiles,backgrounds={},{},{}
    originals={}
    for model in ['heavy','cold']:
        prediction,profile,gas,dependencies=read_prediction(model,'fine')
        inputs.extend(dependencies)
        predictions[model],profiles[model]=prediction,profile
        backgrounds[model]=thermal_wave.thermal.ThermalBackground(model)
        inputs.extend([backgrounds[model].parent.source,backgrounds[model].native_constants])
        for upper in UPPERS:
            path=reference_source(args.order,args.panel,upper,model)
            originals[model,upper]=read_npz(path)
            inputs.extend([path,path.parent/'status.json'])
    for path in inputs:
        verify_source(path,chain)
    for key in ['coordinate','frequency']:
        assert np.array_equal(predictions['heavy'][key],predictions['cold'][key])
    prediction=predictions['heavy']
    frequency,measures=joint_grid(args.panel)
    all_profiles=np.concatenate([profiles[model] for model in ['heavy','cold']],axis=2)
    all_slopes=np.concatenate([predictions[model]['slope'] for model in ['heavy','cold']],axis=2)
    epochs=[0,32,64] if args.pilot else list(range(len(prediction['coordinate'])))
    checks,rows,bulk_bank,join_bank,total_bank=[],[],[],[],[]
    inverse_mass=linalg.inv(basis.mass)
    for epoch in epochs:
        started=time.monotonic()
        event_path=PARENT/'results'/f'bank-o{args.order}-q32-m40'/f'epoch-{epoch:02d}.npz'
        verify_source(event_path,chain)
        inputs.append(event_path)
        events=read_npz(event_path)
        theta=backgrounds['heavy'].at(float(prediction['coordinate'][epoch]))['thermal_parameter']
        assert theta==float(events['theta']) and theta==backgrounds['cold'].at(float(prediction['coordinate'][epoch]))['thermal_parameter']
        pilot_path=ROOT/'results'/('pilot-'+label)/f'epoch-{epoch:02d}.npz'
        reused=not args.pilot and pilot_path.is_file()
        if reused:
            pilot=read_npz(pilot_path)
            bulk,joining,total=[pilot[key] for key in ['bulk','joining','total']]
            domain=dict(minimum_shifted_frequency=float(pilot['minimum_shifted_frequency']),maximum_shifted_frequency=float(pilot['maximum_shifted_frequency']))
            inputs.extend([pilot_path,pilot_path.parent/'status.json'])
        else:
            spline=interpolate.CubicSpline(np.log(prediction['frequency']),all_slopes[epoch],axis=0,extrapolate=False)
            bulk,joining,total,domain=direct_split(basis,frequency,measures,events['ratios'],events['rates'],spline,all_profiles[epoch],epoch==0)
        assert all(np.isfinite(value).all() for value in [bulk,joining,total])
        scale=np.maximum(np.linalg.norm(bulk,axis=1)+np.linalg.norm(joining,axis=1)+np.linalg.norm(total,axis=1),1e-300)
        closure=float(np.max(np.linalg.norm(bulk+joining-total,axis=1)/scale))
        checks.append(check('Independent bulk plus join equals direct adjoint:'+str(epoch),closure,1e-10))
        checks.append(check('Number invariant per component:'+str(epoch),max(np.max(abs(np.einsum('i,wik->wk',basis.chemical,value))) for value in [bulk,joining]),1e-14))
        reference_errors={}
        for window_index,upper in enumerate(UPPERS):
            for model_index,model in enumerate(['heavy','cold']):
                reference=originals[model,upper]['raw_source'][epoch,0]
                current=total[window_index,:,3*model_index:3*model_index+3]
                numerator=np.linalg.norm(current-reference,axis=0)
                denominator=np.maximum(np.linalg.norm(reference,axis=0)+np.linalg.norm(current,axis=0),1e-300)
                difference=float(np.max(numerator/denominator))
                reference_errors[model+str(upper)]=difference
                if upper==.04 or (args.order==6 and args.panel==32):
                    checks.append(check(f'Same-rule Stage113 raw source:{epoch}:{model}:{upper}',difference,1e-9))
        np.savez_compressed(folder/f'epoch-{epoch:02d}.npz',bulk=bulk,joining=joining,total=total,**domain)
        bulk_bank.append(bulk)
        join_bank.append(joining)
        total_bank.append(total)
        row=dict(epoch=epoch,seconds=time.monotonic()-started,reused_pilot=reused,closure=closure,
            reference_errors=reference_errors,**domain)
        rows.append(row)
        write_json(folder/'progress.json',dict(state='running',completed_epochs=len(rows),total_epochs=len(epochs),latest=row))
        if epoch%8==0 or epoch==64:
            print(json.dumps(dict(case=label,**row)),flush=True)
    if not args.pilot:
        bulk_bank,join_bank,total_bank=np.array(bulk_bank),np.array(join_bank),np.array(total_bank)
        for window_index,upper in enumerate(UPPERS):
            for model_index,model in enumerate(['heavy','cold']):
                original=originals[model,upper]
                data={key:value.copy() for key,value in original.items()}
                selected=slice(model_index*3,model_index*3+3)
                bulk=bulk_bank[:,window_index,:,selected]
                joining=join_bank[:,window_index,:,selected]
                total=total_bank[:,window_index,:,selected]
                remainder=original['raw_source'][:,1:].sum(axis=1)-original['overlap_source'].sum(axis=1)
                data['raw_source'][:,0]=total
                data['physical_process_source']=data['raw_source']-original['overlap_source']
                data['source']=np.stack([bulk,joining,remainder],axis=1)
                data['direct_compton']=total
                data['number_source']=np.einsum('i,ntik->ntk',basis.chemical,data['source'])
                data['energy_source']=np.einsum('i,ntik->ntk',basis.temperature,data['source'])
                data['group_labels']=np.array(['bulk','joining','DC_BR_minus_represented_terms'])
                assert np.array_equal(data['raw_source'][:,1:],original['raw_source'][:,1:])
                for key in ['overlap_source','projected_replacement','replacement_moments','profiles','gas']:
                    assert np.array_equal(data[key],original[key]),key
                assert not np.count_nonzero(data['source'][0])
                np.savez_compressed(folder/f'{model}-m{int(upper*1000)}.npz',**data)
    finish(folder,dict(checks=checks,rows=rows,event_order=args.order,source_panel_order=args.panel,
        match_uppers=UPPERS,variant='fine',pilot=args.pilot,columns=['baseline','join1','join2'],
        forcing_groups=['bulk','joining','DC_BR_minus_represented_terms'],
        new_thermal_events=0,parent_history_rerun=False,window_fitted=False,
        join_term_discarded=False,source_frequencies=len(frequency)),__file__,inputs)
    write_json(folder/'progress.json',dict(state='complete',completed_epochs=len(rows),total_epochs=len(rows)))


if __name__=='__main__':
    main()

