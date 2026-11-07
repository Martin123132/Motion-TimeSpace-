from colder_common import *
from evolve_adjacent_window import integrate,terminal


def main():
    modest()
    folder=ROOT/'results/colder-response'
    folder.mkdir(parents=True,exist_ok=False)
    source_report=verify_packet(ROOT/'results/colder-source')
    assert source_report['energy_coordinate_evolution_allowed']
    source_path=ROOT/'results/colder-source/source.npz'
    data=read_npz(source_path)
    anchor_path=ANCHORS/'results/adjacent-sources/source.npz'
    warm_path=PARENT/'results/holdout-source/source.npz'
    anchors=read_npz(anchor_path)
    warm=read_npz(warm_path)['defect']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    checks,rows,inputs=[],{},[source_path,anchor_path,warm_path,ROOT/'results/colder-source/status.json',*ladder.inputs]
    groups=['frozen_stage144_curve','revised_five_node_curve','isolated_colder_defect',
            'zero_extra_source','old_window_replay','old_plus_revised_direct']
    for model,selection in [('heavy',slice(0,2)),('cold',slice(2,4))]:
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        inputs.extend([*emission.inputs,background.parent.source,background.native_constants])
        for kind in ['local','cubic']:
            prior_active_path=PARENT/'results/holdout-response'/f'{model}-{kind}-active.npz'
            prior_final_path=PARENT/'results/holdout-response'/f'{model}-{kind}-transfer.npz'
            prior_active,prior_final=read_npz(prior_active_path),read_npz(prior_final_path)
            inputs.extend([prior_active_path,prior_final_path])
            initial={key:np.zeros((96,12)) if key=='photon' else np.zeros(12)
                     for key in ['photon','energy','gas','work','integrated_number_source']}
            for key in initial:
                initial[key][...,8:10]=prior_active[key][0,...,8:10]
                initial[key][...,10:12]=prior_active[key][0,...,8:10]
            def forcing(phase):
                original=forecast(anchors,warm,phase,kind)[:,selection]
                increment=cold_bubble(phase,kind)*data[kind+'_defect'][:,selection]
                revised=original+increment
                zero=np.zeros_like(original)
                return np.column_stack([original,revised,increment,zero,zero,revised])
            active,active_checks,active_row=integrate(model,1024,initial,forcing,ladder,background,
                emission,.5,.75,f'{model}-{kind}-active')
            final,final_checks,final_row=integrate(model,1024,terminal(active),
                lambda phase:np.zeros((98,12)),ladder,background,emission,.75,1.,f'{model}-{kind}-transfer')
            checks.extend(active_checks+final_checks)
            replay={}
            for phase,value,prior in [('active',active,prior_active),('transfer',final,prior_final)]:
                for key in ['photon','energy','gas','work','integrated_number_source']:
                    scale=max(float(np.max(abs(prior[key][...,2:4]))),1e-300)
                    error=float(np.max(abs(value[key][...,:2]-prior[key][...,2:4]))/scale)
                    replay[phase+'_'+key]=error
                    test(checks,'Frozen Stage144 replay:'+model+':'+kind+':'+phase+':'+key,error,1e-10)
                np.savez_compressed(folder/f'{model}-{kind}-{phase}.npz',**value)
            rows[f'{model}-{kind}']=dict(active=active_row,transfer=final_row,replay=replay)
            print(json.dumps(dict(model=model,kind=kind,complete=True)),flush=True)
    finish(folder,dict(checks=checks,rows=rows,column_groups=groups,steps=1024,
        source_interval=[.5,.75],transfer_interval=[.75,1.],
        interpolation_updates={'local':'two_half_piecewise_quadratic','cubic':'five_node_quartic'},
        original_integrator_reused=True,frequency_grid_unchanged=96,
        interpolation_shapes_frozen_before_holdout=True,full_history_not_rerun=True,
        source_error_bound=False),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
