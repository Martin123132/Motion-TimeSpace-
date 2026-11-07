from stage148_terminal_common import *
from compare_steps import state_difference


def main():
    modest()
    folder=ROOT/'results/comparison'
    folder.mkdir(parents=True,exist_ok=False)
    old_report_path=PARENT/'results/comparison/status.json'
    old_report=verify_packet(old_report_path.parent)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    checks,inputs,readouts,comparisons=[],[old_report_path,*ladder.inputs],{},{}
    selections={'secant':slice(3,5),'quadratic':slice(5,7),'combined':slice(9,11),
                'baseline_plus_mts':slice(13,15),'curvature':slice(15,17)}
    for model in ['heavy','cold']:
        heat=old_report['metadata'][model]['heat']
        states={}
        for count in COUNTS:
            location=ROOT/'results/response'/f'{model}-{count}'
            assert verify_packet(location)['all_checks_passed']
            states[count]=read_npz(location/'response.npz')
            final=states[count]
            secant,quadratic_value,increment=[reader.values@final['photon'][-1,:,selection]
                for selection in [slice(0,2),slice(2,4),slice(4,6)]]
            secant_energy,quadratic_energy,increment_energy=[final['energy'][-1,selection]
                for selection in [slice(0,2),slice(2,4),slice(4,6)]]
            for match in [20,40]:
                key=f'{model}-m{match}'
                prior_path=PARENT/'results/comparison'/f'{key}-4096.npz'
                prior=read_npz(prior_path)
                assert np.array_equal(prior['frequency'],reader.frequency)
                assert np.array_equal(prior['measure'],reader.measure)
                baseline,old=prior['potential'][:,:1],prior['potential'][:,9:11]
                baseline_energy,old_energy=prior['energy'][:1],prior['energy'][9:11]
                potential=np.column_stack([baseline,old,secant,quadratic_value,old+secant,old+quadratic_value,
                    baseline+old,baseline+old+quadratic_value,increment])
                energy=np.r_[baseline_energy,old_energy,secant_energy,quadratic_energy,
                    old_energy+secant_energy,old_energy+quadratic_energy,
                    baseline_energy+old_energy,baseline_energy+old_energy+quadratic_energy,increment_energy]
                split=reader.split_values(potential,energy)
                label=key+'-'+str(count)
                inherited.invariants(checks,reader,split,label)
                assert np.array_equal(split['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                assert np.array_equal(potential[:,1:3],prior['potential'][:,9:11])
                checks.append(dict(name='Saved nonzero baseline and old MTS preserved:'+label,passed=True))
                test(checks,'Identical baseline/MTS projection:'+label,
                    np.max(abs(split['amplitudes'][:,13:15]-split['amplitudes'][:,:1]-split['amplitudes'][:,9:11]))/
                    max(float(np.max(abs(split['amplitudes'][:,9:11]))),1e-300),1e-8)
                metrics=inherited.metrics(reader,split,heat)
                readouts[label]=dict(metrics=metrics,
                    new_fraction_of_prior={name:(np.asarray(metrics[name])[5:7]/np.asarray(metrics[name])[1:3]).tolist()
                                           for name in ['mu','y']},
                    interpolation_fraction={name:(np.asarray(metrics[name])[15:17]/np.asarray(metrics[name])[5:7]).tolist()
                                            for name in ['mu','y']})
                np.savez_compressed(folder/(label+'.npz'),**split,frequency=reader.frequency,measure=reader.measure,heat=heat)
                inputs.append(prior_path)
            inputs.extend([location/'status.json',location/'response.npz'])
        comparisons[model]={'state':{},'spectral':{}}
        for group,selection in [('secant',slice(0,2)),('quadratic',slice(2,4)),('curvature',slice(4,6))]:
            record=state_difference(states[2048],states[4096],selection,ladder.basis.mass)
            comparisons[model]['state'][group]=record
            for name,values in record['relative'].items():
                test(checks,'CONVERGENCE:'+model+':'+group+':'+name,float(max(values)),.01)
        for match in [20,40]:
            key=f'{model}-m{match}'
            comparisons[model]['spectral'][key]={}
            for metric in ['mu','y']:
                coarse=np.asarray(readouts[key+'-2048']['metrics'][metric])
                fine=np.asarray(readouts[key+'-4096']['metrics'][metric])
                assert np.array_equal(coarse[:3],fine[:3])
                records={}
                for group,selection in selections.items():
                    relative=abs(fine[selection]-coarse[selection])/np.maximum(abs(fine[selection]),1e-300)
                    records[group]=dict(fine=fine[selection].tolist(),signed_change=(fine[selection]-coarse[selection]).tolist(),
                        relative_change=relative.tolist())
                    test(checks,'CONVERGENCE:'+key+':'+metric+':'+group,float(max(relative)),.01)
                comparisons[model]['spectral'][key][metric]=records
    column_order=['baseline','old_mts_m20','old_mts_m40','secant_m20','secant_m40',
        'quadratic_m20','quadratic_m40','old_plus_secant_m20','old_plus_secant_m40',
        'old_plus_quadratic_m20','old_plus_quadratic_m40','baseline_plus_old_m20','baseline_plus_old_m40',
        'baseline_plus_old_plus_quadratic_m20','baseline_plus_old_plus_quadratic_m40','curvature_m20','curvature_m40']
    finish(folder,dict(checks=checks,comparisons=comparisons,readouts=readouts,column_order=column_order,
        metadata=old_report['metadata'],counts=COUNTS,modes=96,source_interval=[.75,1.],
        represented_source_union=[.25,1.],final_epoch=1e-5,baseline_preserved=True,
        baseline_inner_history_refined=False,observed_sky_likelihood=False,
        interpolation_spread_is_error_bound=False,new_window_inner_feedback_recomputed=False,
        convergence_passed=all(row['passed'] for row in checks if row['name'].startswith('CONVERGENCE:'))),
        __file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],
        latest={key:value for key,value in readouts.items() if key.endswith('4096')})),flush=True)


if __name__=='__main__':
    main()

