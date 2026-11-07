from stage164_common import *
from reconcile_reference import cardinal_weights
from evolve_adjacent_window import integrate,terminal
import argparse


def run(model,route,count,ladder):
    folder=ROOT/'results/response'/f'{model}-{route}-{count}'
    if (folder/'COMPLETE').exists():
        assert verify_packet(folder)['all_checks_passed']
        return
    reference=verify_packet(ROOT/'results/reference')
    assert reference['reference_replay_qualified'] and reference['all_checks_passed']
    assert verify_packet(ROOT/'results/sources')['all_checks_passed']
    folder.mkdir(parents=True,exist_ok=False)
    data=read_npz(ROOT/'results/sources/source.npz')
    refs=read_npz(ROOT/'results/reference/reference.npz')
    selection=slice(0,2) if model=='heavy' else slice(2,4)
    initial={key:np.zeros((96,24)) if key=='photon' else np.zeros(24)
        for key in ['photon','energy','gas','work','integrated_number_source']}
    background=thermal_wave.thermal.ThermalBackground(model)
    emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    checks,metrics,outputs=[],{},[]
    for window,lower,upper in [('earlier',.5,.75),('terminal',.75,1.)]:
        def forcing(phase):
            weights=cardinal_weights(phase,route)
            start_weight=weights[4] if window=='earlier' else weights[0]
            end_weight=0. if window=='earlier' else weights[4]
            arithmetic_start=start_weight*refs['start_coordinate_reference'][:,selection]
            arithmetic_end=end_weight*refs['end_coordinate_reference'][:,selection]
            arithmetic=arithmetic_start+arithmetic_end
            physical_start=start_weight*data['soft_start_total64'][:,selection]
            physical_end=end_weight*data['soft_end_total64'][:,selection]
            physical=physical_start+physical_end
            physical54=start_weight*data['soft_start_total54'][:,selection]+end_weight*data['soft_end_total54'][:,selection]
            physical65=start_weight*data['soft_start_total65'][:,selection]+end_weight*data['soft_end_total65'][:,selection]
            zero=np.zeros_like(arithmetic)
            return np.column_stack([arithmetic_start,arithmetic,arithmetic_end,zero,physical,arithmetic+physical,
                physical_start,physical_end,physical54,physical65,arithmetic+physical54,arithmetic+physical])
        result,current_checks,current_metrics=integrate(model,count,initial,forcing,ladder,background,emission,lower,upper,
            f'{model}-{route}-{count}-{window}')
        checks.extend(current_checks)
        metrics[window]=current_metrics
        for quantity in ['photon','gas','energy','work','number','integrated_number_source']:
            values=result[quantity]
            close(checks,'Physical endpoint superposition:'+window+':'+quantity,values[...,12:14]+values[...,14:16],values[...,8:10],1e-8)
            close(checks,'Physical order telescope:'+window+':'+quantity,values[...,16:18]+values[...,18:20],values[...,8:10],1e-8)
            close(checks,'Reference separated from physical:'+window+':'+quantity,values[...,2:4]+values[...,8:10],values[...,22:24],1e-8)
        path=folder/(window+'.npz')
        np.savez_compressed(path,**result)
        outputs.append(path)
        initial=terminal(result)
    finish(folder,dict(checks=checks,model=model,route=route,steps_per_window=count,heat=background.chi,metrics=metrics,
        numerical_reference_columns=[2,3],physical64_columns=[8,9],combined_columns=[10,11],
        source_windows=[[.5,.75],[.75,1.]],shared_endpoint_updated_in_both=True,inner_histories_rerun=False,
        curve_basis_changed=False,diagnostic_not_adopted=True),__file__,
        [ROOT/'REFERENCE-CONTRACT.md',ROOT/'results/reference/status.json',ROOT/'results/reference/reference.npz',
            ROOT/'results/sources/status.json',ROOT/'results/sources/source.npz',*ladder.inputs,*emission.inputs,
            background.parent.source,background.native_constants,*outputs])
    print(json.dumps(dict(model=model,route=route,steps=count,failed=[row for row in checks if not row['passed']])),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    args=parser.parse_args()
    assert verify_packet(ROOT/'results/reference')['reference_replay_qualified']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    for route in ['local','cubic']:
        for count in COUNTS:
            if datetime.now(timezone.utc)>=datetime.fromisoformat(DEADLINE):
                raise SystemExit(75)
            run(args.model,route,count,ladder)
