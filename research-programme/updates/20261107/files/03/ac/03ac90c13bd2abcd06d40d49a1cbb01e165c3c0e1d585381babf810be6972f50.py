from colder_common import *


def main():
    modest()
    folder=ROOT/'results/local-readout'
    folder.mkdir(parents=True,exist_ok=False)
    report=verify_packet(ROOT/'results/local-response')
    assert report['all_checks_passed']
    prior_report=json.loads((PARENT/'results/spectral-readout/status.json').read_text())
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    checks,inputs,rows=[],[ROOT/'results/local-response/status.json',
                          PARENT/'results/spectral-readout/status.json',*ladder.inputs],{}
    names=['baseline','old1','old2','new_original1','new_original2','new_revised1','new_revised2',
           'combined_original1','combined_original2','combined_revised1','combined_revised2',
           'baseline_plus_original1','baseline_plus_original2',
           'baseline_plus_revised1','baseline_plus_revised2','defect1','defect2']
    for model in ['heavy','cold']:
        heat=prior_report['metadata'][model]['heat']
        for kind in ['local']:
            response_path=ROOT/'results/local-response'/f'{model}-{kind}-transfer.npz'
            response=read_npz(response_path)
            delta=reader.values@response['photon'][-1,:,4:6]
            delta_energy=response['energy'][-1,4:6]
            inputs.append(response_path)
            for match in [20,40]:
                case=f'{model}-m{match}'
                prior_path=PARENT/'results/spectral-readout'/(case+'-'+kind+'.npz')
                prior=read_npz(prior_path)
                inputs.append(prior_path)
                assert np.array_equal(prior['frequency'],reader.frequency)
                assert np.array_equal(prior['measure'],reader.measure)
                base,old,new=[prior['potential'][:,section] for section in [slice(0,1),slice(1,3),slice(5,7)]]
                base_e,old_e,new_e=[prior['energy'][section] for section in [slice(0,1),slice(1,3),slice(5,7)]]
                revised=new+delta
                revised_e=new_e+delta_energy
                potential=np.column_stack([base,old,new,revised,old+new,old+revised,
                                           base+old+new,base+old+revised,delta])
                energy=np.r_[base_e,old_e,new_e,revised_e,old_e+new_e,old_e+revised_e,
                             base_e+old_e+new_e,base_e+old_e+revised_e,delta_energy]
                result=reader.split_values(potential,energy)
                label=case+'-'+kind
                inherited.invariants(checks,reader,result,label)
                assert np.array_equal(potential[:,0],prior['potential'][:,0])
                assert np.array_equal(potential[:,1:3],prior['potential'][:,1:3])
                assert np.array_equal(potential[:,3:5],prior['potential'][:,5:7])
                checks.append(dict(name='Nonzero baseline and old/new MTS spectra preserved:'+label,passed=True))
                direct=reader.values@response['photon'][-1,:,2:4]
                scale=max(float(np.max(abs(revised))),1e-300)
                test(checks,'Direct revised evolution vs inherited plus increment:'+label,np.max(abs(revised-direct))/scale,1e-10)
                amplitude=result['amplitudes']
                test(checks,'Identical baseline and MTS projection:'+label,
                     np.max(abs(amplitude[:,13:15]-amplitude[:,:1]-amplitude[:,9:11]))/
                     max(float(np.max(abs(amplitude[:,9:11]))),1e-300),1e-8)
                metrics=inherited.metrics(reader,result,heat)
                ratios={}
                for name in ['mu','y']:
                    values=np.array(metrics[name])
                    ratios[name]=dict(change_over_original_new=(values[15:17]/values[3:5]).tolist(),
                        change_over_original_combined=(values[15:17]/values[7:9]).tolist(),
                        change_over_baseline=(values[15:17]/values[0]).tolist(),
                        revised_combined=values[9:11].tolist(),
                        original_combined=values[7:9].tolist(),
                        revised_new=values[5:7].tolist(),original_new=values[3:5].tolist())
                rows[label]=dict(metrics=metrics,ratios=ratios)
                np.savez_compressed(folder/(label+'.npz'),**result,
                                    frequency=reader.frequency,measure=reader.measure,heat=heat)
    finish(folder,dict(checks=checks,rows=rows,column_order=names,cubic_propagation_blocked=True,
        metadata=prior_report['metadata'],final_epoch=1e-5,baseline_preserved=True,
        changes_computed_from_direct_defect_not_large_total_subtraction=True,
        shapes_are_sensitivities_not_error_bounds=True,observational_fit=False),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],
        ratios={key:value['ratios'] for key,value in rows.items()})),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
