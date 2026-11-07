from adjacent_source_common import *


def main():
    modest()
    folder=ROOT/'results/spectral-readout'
    folder.mkdir(parents=True,exist_ok=False)
    response_owner=ROOT/'results/adjacent-response'
    response_report=verify_packet(response_owner)
    assert response_report['all_checks_passed'],[row for row in response_report['checks'] if not row['passed']]
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    reader=ShapeReadout(basis,canonical=True)
    checks,inputs,rows=[],[response_owner/'status.json',*ladder.inputs],{}
    parent_report=json.loads((PARENT/'results/decomposition-v2/status.json').read_text())
    inputs.append(PARENT/'results/decomposition-v2/status.json')
    names=['baseline','old_window_join1','old_window_join2','new_window_join1','new_window_join2',
           'both_windows_join1','both_windows_join2','baseline_plus_old_join1','baseline_plus_old_join2',
           'baseline_plus_both_join1','baseline_plus_both_join2']
    for model in ['heavy','cold']:
        response_path=response_owner/f'{model}-transfer1024.npz'
        response=read_npz(response_path)
        coarse_path=response_owner/f'{model}-transfer512.npz'
        coarse=read_npz(coarse_path)
        inputs.extend([response_path,coarse_path])
        new=reader.values@response['photon'][-1,:,2:4]
        new_energy=response['energy'][-1,2:4]
        source_defect=reader.split_values(reader.values@response['photon'][-1,:,4:6],response['energy'][-1,4:6])
        time_defect=reader.split_values(reader.values@(response['photon'][-1,:,2:4]-coarse['photon'][-1,:,2:4]),
                                      response['energy'][-1,2:4]-coarse['energy'][-1,2:4])
        heat=parent_report['metadata'][model]['heat']
        for match in [20,40]:
            case=f'{model}-m{match}'
            prior_path=PARENT/'results/decomposition-v2'/f'{case}-physical-canonical700.npz'
            prior=read_npz(prior_path)
            inputs.append(prior_path)
            assert np.array_equal(prior['frequency'],reader.frequency) and np.array_equal(prior['measure'],reader.measure)
            old=prior['corrected_potential'][:,1:3]
            old_energy=prior['corrected_energy'][1:3]
            baseline=prior['corrected_potential'][:,:1]
            baseline_energy=prior['corrected_energy'][:1]
            both=old+new
            both_energy=old_energy+new_energy
            potential=np.column_stack([baseline,old,new,both,baseline+old,baseline+both])
            energy=np.r_[baseline_energy,old_energy,new_energy,both_energy,
                         baseline_energy+old_energy,baseline_energy+both_energy]
            result=reader.split_values(potential,energy)
            inherited.invariants(checks,reader,result,case)
            metrics=inherited.metrics(reader,result,heat)
            source_metrics=inherited.metrics(reader,source_defect,heat)
            time_metrics=inherited.metrics(reader,time_defect,heat)
            np.savez_compressed(folder/(case+'.npz'),**result,frequency=reader.frequency,measure=reader.measure,
                                heat=heat,source_defect_amplitudes=source_defect['amplitudes'],
                                source_defect_residual=source_defect['residual'],
                                time_defect_amplitudes=time_defect['amplitudes'],
                                time_defect_residual=time_defect['residual'])
            test(checks,'Unchanged nonzero baseline spectrum:'+case,
                 np.max(abs(potential[:,0]-prior['corrected_potential'][:,0])))
            test(checks,'Old MTS contribution is retained:'+case,np.max(abs(potential[:,1:3]-old)))
            test(checks,'Baseline and MTS receive identical projection:'+case,
                 np.max(abs(result['amplitudes'][:,9:11]-
                            result['amplitudes'][:,:1]-result['amplitudes'][:,1:3]-result['amplitudes'][:,3:5]))/
                 max(float(np.max(abs(result['amplitudes'][:,3:5]))),1e-300),1e-8)
            ratios={}
            for name in ['mu','y']:
                actual=np.array(metrics[name])
                ratios[name]=dict(new_over_old=(actual[3:5]/actual[1:3]).tolist(),
                                  new_over_baseline=(actual[3:5]/actual[0]).tolist(),
                                  source_interpolation_over_new=(abs(np.array(source_metrics[name]))/abs(actual[3:5])).tolist(),
                                  time_refinement_over_new=(abs(np.array(time_metrics[name]))/abs(actual[3:5])).tolist(),
                                  source_interpolation_over_both=(abs(np.array(source_metrics[name]))/abs(actual[5:7])).tolist())
            rows[case]=dict(metrics=metrics,ratios=ratios,source_interpolation=source_metrics,time_refinement=time_metrics)
    finish(folder,dict(checks=checks,rows=rows,column_order=names,metadata=parent_report['metadata'],
                       source_window=[.5,.75],old_window=[.25,.5],represented_union=[.25,.75],
                       all_epoch_extra_source_complete=False,final_epoch=1e-5,
                       independent_baseline_preserved=True,
                       new_window_low_frequency_feedback_recomputed=False,
                       event_quadrature_error_bounded=False,observational_fit=False),
           __file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],
                          quick_rows={key:value['ratios'] for key,value in rows.items()})),flush=True)


if __name__=='__main__':
    main()
