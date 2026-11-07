from stage146_precision_common import *
from evolve_adjacent_window import integrate,terminal
import argparse


def run(model,kind,ladder):
    source_folder=ROOT/'results/repaired-readiness'
    readiness=verify_packet(source_folder)
    assert readiness['allowed_routes'][kind]
    source_path=source_folder/'source.npz'
    data=read_npz(source_path)
    folder=ROOT/'results/response'/f'{model}-{kind}'
    if (folder/'COMPLETE').exists():
        assert verify_packet(folder)['all_checks_passed']
        return
    folder.mkdir(parents=True,exist_ok=True)
    background=thermal_wave.thermal.ThermalBackground(model)
    emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    prior_active_path=WARM/'results/holdout-response'/f'{model}-{kind}-active.npz'
    prior_final_path=WARM/'results/holdout-response'/f'{model}-{kind}-transfer.npz'
    prior_active,prior_final=read_npz(prior_active_path),read_npz(prior_final_path)
    inputs=[source_path,source_folder/'status.json',prior_active_path,prior_final_path,
            *ladder.inputs,*emission.inputs,background.parent.source,background.native_constants]
    selection=slice(0,2) if model=='heavy' else slice(2,4)
    initial={key:np.zeros((96,12)) if key=='photon' else np.zeros(12)
             for key in ['photon','energy','gas','work','integrated_number_source']}
    for key in initial:
        initial[key][...,8:10]=prior_active[key][0,...,8:10]
        initial[key][...,10:12]=prior_active[key][0,...,8:10]
    def forcing(phase):
        original=forecast(data,data['warm_defect'],phase,kind)[:,selection]
        increment=cold_bubble(phase,kind)*data[kind+'_defect'][:,selection]
        revised=original+increment
        zero=np.zeros_like(original)
        return np.column_stack([original,revised,increment,zero,zero,revised])
    results,phase_reports={},{}
    for phase,lower,upper in [('active',.5,.75),('transfer',.75,1.)]:
        destination=folder/phase
        if (destination/'COMPLETE').exists():
            report=verify_packet(destination)
            assert report['all_checks_passed']
            value=read_npz(destination/'response.npz')
        else:
            destination.mkdir(parents=True,exist_ok=False)
            seed=initial if phase=='active' else terminal(results['active'])
            source=forcing if phase=='active' else lambda fraction:np.zeros((98,12))
            value,checks,row=integrate(model,1024,seed,source,ladder,background,emission,
                                       lower,upper,f'{model}-{kind}-{phase}')
            np.savez_compressed(destination/'response.npz',**value)
            extra=inputs+[destination/'response.npz']
            if phase=='transfer':
                extra.extend([folder/'active/response.npz',folder/'active/status.json'])
            report=dict(checks=checks,model=model,kind=kind,phase=phase,metrics=row,steps=1024,modes=96)
            finish(destination,report,__file__,extra)
            assert report['all_checks_passed']
            print(json.dumps(dict(model=model,kind=kind,phase=phase,metrics=row)),flush=True)
        results[phase]=value
        phase_reports[phase]=report
    checks,precision_changes=[],{}
    for phase,value,prior in [('active',results['active'],prior_active),('transfer',results['transfer'],prior_final)]:
        precision_changes[phase]={}
        for key in ['photon','energy','gas','work','integrated_number_source']:
            scale=max(float(np.max(abs(prior[key][...,2:4]))),1e-300)
            precision_changes[phase][key]=float(np.max(abs(value[key][...,:2]-prior[key][...,2:4]))/scale)
            old_scale=max(float(np.max(abs(prior[key][...,8:10]))),1e-300)
            old_error=float(np.max(abs(value[key][...,8:10]-prior[key][...,8:10]))/old_scale)
            test(checks,'Unchanged old-window replay:'+phase+':'+key,old_error,1e-10)
        inputs.extend([folder/phase/'status.json',folder/phase/'response.npz'])
    for key in initial:
        assert np.array_equal(results['active'][key][-1],results['transfer'][key][0])
    checks.append(dict(name='All physical restart offsets retained across seam',passed=True))
    finish(folder,dict(checks=checks,model=model,kind=kind,heat=background.chi,
        precision_change_from_saved_stage144_curve=precision_changes,
        column_groups=['refined_stage144_curve','refined_five_node_curve','isolated_colder_defect',
                       'zero_extra_source','old_window_replay','old_plus_revised_direct'],
        source_interval=[.5,.75],transfer_interval=[.75,1.],original_integrator_reused=True,
        modes=96,steps_per_phase=1024,literal_frozen_forecast_not_overwritten=True,
        full_inner_history_rerun=False),__file__,inputs)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    args=parser.parse_args()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    readiness=verify_packet(ROOT/'results/repaired-readiness')
    for kind in ['local','cubic']:
        if readiness['allowed_routes'][kind]:
            run(args.model,kind,ladder)
