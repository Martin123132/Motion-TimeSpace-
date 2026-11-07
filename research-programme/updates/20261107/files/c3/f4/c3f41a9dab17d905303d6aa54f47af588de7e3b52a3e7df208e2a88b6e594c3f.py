from stage158_common import *


def main():
    modest()
    folder=ROOT/'results/comparison'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    allowed=verify_packet(ROOT/'results/sources')['allowed_routes']
    checks,inputs,records=[],[*ladder.inputs,ROOT/'results/sources/status.json'],{}
    maximum_precision=maximum_svd=0.
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            if not allowed[route]:
                continue
            states={}
            for count in COUNTS:
                location=ROOT/'results/response'/f'{model}-{route}-{count}'
                proof=verify_packet(location)
                assert proof['all_checks_passed']
                response=read_npz(location/'response.npz')
                old_path=SOURCE155/'results/response'/f'{model}-{route}-{count}/response.npz'
                old=read_npz(old_path)
                assert np.array_equal(response['coordinate'],old['coordinate'])
                states[count]=response
                heat=proof['heat']
                inputs.extend([location/'status.json',location/'response.npz',old_path])
                state_metrics={}
                for name in ['photon','gas']:
                    measure=lambda value:state_norm(value,ladder.basis.mass) if name=='photon' else abs(value)
                    reference=measure(old[name][...,10:12])
                    endpoint_denominator=reference[-1] if name=='photon' else reference.max(axis=0)
                    state_metrics[name]={}
                    for stage,selection in [('band3',slice(0,2)),('band4',slice(4,6)),('both',slice(2,4))]:
                        value=measure(response[name][...,selection])
                        state_metrics[name][stage]=dict(endpoint_over_order6= (value[-1]/endpoint_denominator).tolist(),
                            history_over_order6_peak=(value.max(axis=0)/reference.max(axis=0)).tolist())
                for stage,selection in [('after3',slice(0,2)),('after34',slice(2,4))]:
                    energy=old['energy'][...,10:12]+response['energy'][...,selection]
                    gas=old['gas'][...,10:12]+response['gas'][...,selection]
                    work=old['work'][...,10:12]+response['work'][...,selection]
                    balance=energy+heat*gas+work
                    scale=np.maximum(np.max(abs(energy)+abs(heat*gas)+abs(work),axis=0),1e-300)
                    test(checks,'Updated MTS energy/work:'+model+':'+route+':'+str(count)+':'+stage,
                        float(np.max(abs(balance-balance[0])/scale)),1e-7)
                label=f'{model}-{route}-{count}'
                readouts={}
                for match in [20,40]:
                    prior_path=SOURCE155/'results/comparison'/f'{model}-m{match}-{route}-{count}.npz'
                    prior=read_npz(prior_path)
                    inputs.append(prior_path)
                    baseline=prior['potential'][:,:1]
                    original=prior['potential'][:,9:11]
                    first_update=reader.values@response['photon'][-1,:,:2]
                    second_update=reader.values@response['photon'][-1,:,4:6]
                    first_energy=response['energy'][-1,:2]
                    second_energy=response['energy'][-1,4:6]
                    for band,previous,current,previous_energy,current_energy,delta,delta_energy,starts in [
                        (3,original,original+first_update,prior['energy'][9:11],prior['energy'][9:11]+first_energy,
                            first_update,first_energy,[12,14,16]),
                        (4,original+first_update,original+first_update+second_update,
                            prior['energy'][9:11]+first_energy,prior['energy'][9:11]+first_energy+second_energy,
                            second_update,second_energy,[18,20,22])]:
                        pieces=[reader.values@response['photon'][-1,:,start:start+2] for start in starts]
                        potential=np.column_stack([baseline,previous,current,baseline+previous,baseline+current,delta,*pieces])
                        energy=np.r_[prior['energy'][:1],previous_energy,current_energy,
                            prior['energy'][:1]+previous_energy,prior['energy'][:1]+current_energy,
                            delta_energy,*[response['energy'][-1,start:start+2] for start in starts]]
                        split=reader.split_values(potential,energy)
                        key=label+f'-m{match}-band{band}'
                        inherited.invariants(checks,reader,split,key)
                        assert np.array_equal(split['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                        assert np.array_equal(potential[:,:1],baseline)
                        if band==3:
                            assert np.array_equal(potential[:,1:3],original)
                        precise=precise_readout(dict(potential=potential,energy=energy),reader)
                        maximum_precision=max(maximum_precision,precise['same_baseline_cancellation'])
                        test(checks,'60digit paired baseline/MTS:'+key,precise['same_baseline_cancellation'],1e-8)
                        close(checks,'Independent60digit increment amplitudes:'+key,precise['amplitudes'][:,3:5],split['amplitudes'][:,9:11],1e-8)
                        close(checks,'Independent60digit increment residual:'+key,precise['residual'][:,3:5],split['residual'][:,9:11],1e-10)
                        alternate=np.linalg.lstsq(np.sqrt(reader.measure)[:,None]*reader.templates,
                            np.sqrt(reader.measure)[:,None]*split['distortion'],rcond=None)[0]
                        numerator=np.linalg.norm(np.sqrt(reader.measure)[:,None]*(reader.templates@(alternate-split['amplitudes'])),axis=0)
                        denominator=np.linalg.norm(np.sqrt(reader.measure)[:,None]*split['distortion'],axis=0)
                        maximum_svd=max(maximum_svd,float(np.max(numerator/np.maximum(denominator,1e-300))))
                        metrics={}
                        for position,name in enumerate(['mu','y']):
                            values=split['amplitudes'][position]
                            budget=sum(abs(values[start:start+2]) for start in [11,13,15])
                            metrics[name]=dict(signed_amplitude=(heat*values[9:11]).tolist(),
                                increment_over_saved_MTS=(abs(values[9:11])/abs(prior['amplitudes'][position,9:11])).tolist(),
                                site_coherence=(abs(values[9:11])/np.maximum(budget,1e-300)).tolist())
                        readouts[f'm{match}-band{band}']=metrics
                        np.savez_compressed(folder/(key+'.npz'),**split,frequency=reader.frequency,measure=reader.measure,heat=heat)
                records[label]=dict(state=state_metrics,readouts=readouts,baseline_preserved=True)
            step_metrics={}
            for group,selection in [('band3',slice(0,2)),('band4',slice(4,6)),('both',slice(2,4))]:
                step_metrics[group]={}
                for quantity in ['photon','gas']:
                    measure=lambda value:state_norm(value,ladder.basis.mass) if quantity=='photon' else abs(value)
                    coarse=states[2048][quantity][...,selection]
                    fine=states[4096][quantity][...,selection]
                    ratio=measure(fine[::2]-coarse).max(axis=0)/np.maximum(measure(fine).max(axis=0),1e-300)
                    step_metrics[group][quantity]=ratio.tolist()
                    test(checks,'CONVERGENCE:'+model+':'+route+':'+group+':'+quantity,float(np.max(ratio)),.01)
            records[model+'-'+route+'-steps']=step_metrics
    test(checks,'Independent weightedSVD',maximum_svd,1e-10)
    numerical=all(row['passed'] for row in checks if not row['name'].startswith('CONVERGENCE:'))
    source_packet=verify_packet(ROOT/'results/sources')
    summary=dict(stage=158,source={key:source_packet[key] for key in
        ['panel_metrics','frequency_diagnostics','stages','allowed_routes','readiness']},
        response=dict(records=records,maximum_precision_cancellation=maximum_precision,
            maximum_independent_svd=maximum_svd,
            convergence_passed=all(row['passed'] for row in checks if row['name'].startswith('CONVERGENCE:'))),
        numerical_integrity_passed=numerical,temperature_curve_changed=False,
        frozen_predictions_preserved=True,baseline_preserved=True,baseline_inner_rerun=False,
        new_event_evaluations=1296,reused_event_values=216,new_response_evolutions=8,
        refined_panels=[[1.,3.],[3.,8.]],selected_panel_order=7,other_panel_order=6,
        incoming_continuum_error_certified=False,
        next_target='Test the dominant remaining1–3 incoming integration change with a matched order8 rule at H/W/C, retaining order7 in3–8 and saved other panels;keep the adopted temperature curve fixed and distinguish measured contraction from a certified tail bound.')
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    finish(folder,dict(checks=checks,records=records,numerical_integrity_passed=numerical,
        convergence_passed=all(row['passed'] for row in checks if row['name'].startswith('CONVERGENCE:')),
        maximum_precision_cancellation=maximum_precision,maximum_independent_svd=maximum_svd,
        temperature_curve_changed=False,baseline_preserved=True,baseline_inner_rerun=False,
        source_update_scope='Two incoming bands only;fixed interpolation bases;all D/V/S components',
        incoming_continuum_error_certified=False),__file__,[*inputs,*folder.glob('*.npz'),ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(checks=len(checks),numerical=numerical,failed=[row for row in checks if not row['passed']])),flush=True)
    assert numerical


if __name__=='__main__':
    main()

