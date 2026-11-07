from stage146_precision_common import *


def main():
    modest()
    folder=ROOT/'results/spectral-readout'
    folder.mkdir(parents=True,exist_ok=False)
    readiness=verify_packet(ROOT/'results/repaired-readiness')
    prior_report=json.loads((WARM/'results/spectral-readout/status.json').read_text())
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    checks,inputs,rows=[],[WARM/'results/spectral-readout/status.json',ROOT/'results/repaired-readiness/status.json',*ladder.inputs],{}
    names=['baseline','old1','old2','new_refined_original1','new_refined_original2',
           'new_revised1','new_revised2','combined_refined_original1','combined_refined_original2',
           'combined_revised1','combined_revised2','baseline_plus_refined_original1',
           'baseline_plus_refined_original2','baseline_plus_revised1','baseline_plus_revised2',
           'defect1','defect2']
    for model in ['heavy','cold']:
        heat=prior_report['metadata'][model]['heat']
        for kind in ['local','cubic']:
            if not readiness['allowed_routes'][kind]:
                continue
            response_folder=ROOT/'results/response'/f'{model}-{kind}'
            assert verify_packet(response_folder)['all_checks_passed']
            response_path=response_folder/'transfer/response.npz'
            response=read_npz(response_path)
            original=reader.values@response['photon'][-1,:,:2]
            revised=reader.values@response['photon'][-1,:,2:4]
            delta=reader.values@response['photon'][-1,:,4:6]
            original_e,revised_e,delta_e=[response['energy'][-1,section] for section in [slice(0,2),slice(2,4),slice(4,6)]]
            inputs.extend([response_folder/'status.json',response_path])
            for match in [20,40]:
                label=f'{model}-m{match}-{kind}'
                prior_path=WARM/'results/spectral-readout'/(label+'.npz')
                prior=read_npz(prior_path)
                assert np.array_equal(prior['frequency'],reader.frequency)
                assert np.array_equal(prior['measure'],reader.measure)
                base,old=[prior['potential'][:,section] for section in [slice(0,1),slice(1,3)]]
                base_e,old_e=[prior['energy'][section] for section in [slice(0,1),slice(1,3)]]
                potential=np.column_stack([base,old,original,revised,old+original,old+revised,
                    base+old+original,base+old+revised,delta])
                energy=np.r_[base_e,old_e,original_e,revised_e,old_e+original_e,old_e+revised_e,
                             base_e+old_e+original_e,base_e+old_e+revised_e,delta_e]
                result=reader.split_values(potential,energy)
                inherited.invariants(checks,reader,result,label)
                assert np.array_equal(potential[:,:3],prior['potential'][:,:3])
                checks.append(dict(name='Nonzero baseline and previous window unchanged:'+label,passed=True))
                test(checks,'Direct revised response equals refined original plus isolated increment:'+label,
                     np.max(abs(revised-original-delta))/np.max(abs(revised)),1e-10)
                amplitude=result['amplitudes']
                test(checks,'Same projection for baseline and MTS:'+label,
                     np.max(abs(amplitude[:,13:15]-amplitude[:,:1]-amplitude[:,9:11]))/
                     max(float(np.max(abs(amplitude[:,9:11]))),1e-300),1e-8)
                metrics=inherited.metrics(reader,result,heat)
                ratios={}
                for name in ['mu','y']:
                    values=np.array(metrics[name])
                    saved_values=np.array(prior_report['rows'][label]['metrics'][name])
                    ratios[name]=dict(change_over_refined_original_new=(values[15:17]/values[3:5]).tolist(),
                        change_over_refined_original_combined=(values[15:17]/values[7:9]).tolist(),
                        change_over_baseline=(values[15:17]/values[0]).tolist(),
                        revised_combined=values[9:11].tolist(),original_combined=values[7:9].tolist(),
                        revised_new=values[5:7].tolist(),original_new=values[3:5].tolist(),
                        refined_original_change_over_saved=(values[3:5]/saved_values[5:7]-1).tolist())
                rows[label]=dict(metrics=metrics,ratios=ratios)
                inputs.append(prior_path)
                np.savez_compressed(folder/(label+'.npz'),**result,frequency=reader.frequency,
                                    measure=reader.measure,heat=heat)
    route_comparison={}
    if all(readiness['allowed_routes'].values()):
        for model in ['heavy','cold']:
            for match in [20,40]:
                key=f'{model}-m{match}'
                local=rows[key+'-local']['metrics']
                cubic=rows[key+'-cubic']['metrics']
                route_comparison[key]={name:((np.array(cubic[name])[9:11]-np.array(local[name])[9:11])/
                    np.maximum(abs(np.array(cubic[name])[9:11]),1e-300)).tolist() for name in ['mu','y']}
    finish(folder,dict(checks=checks,rows=rows,column_order=names,metadata=prior_report['metadata'],
        route_comparison_relative_to_cubic=route_comparison,final_epoch=1e-5,baseline_preserved=True,
        increment_computed_without_large_baseline_subtraction=True,
        precision_change_diagnostic_from_saved_readout=True,shapes_are_not_error_bounds=True,
        observational_fit=False),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],
        ratios={key:value['ratios'] for key,value in rows.items()},route_comparison=route_comparison)),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
