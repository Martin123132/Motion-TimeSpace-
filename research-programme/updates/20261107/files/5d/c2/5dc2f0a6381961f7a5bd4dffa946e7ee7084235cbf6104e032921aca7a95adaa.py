from stage149_holdout_common import *
from evolve_adjacent_window import integrate
import argparse


def run(model,route,count,ladder):
    folder=ROOT/'results/response'/f'{model}-{route}-{count}'
    if (folder/'COMPLETE').exists():
        assert verify_packet(folder)['all_checks_passed']
        return
    folder.mkdir(parents=True,exist_ok=False)
    source_path=ROOT/'results/holdout-source/source.npz'
    source=read_npz(source_path)
    readiness=verify_packet(ROOT/'results/readiness')
    assert readiness['allowed_routes'][route]
    prior_path=PARENT/'results/response'/f'{model}-{count}/response.npz'
    prior=read_npz(prior_path)
    initial={key:prior[key][0].copy() for key in ['photon','energy','gas','work','integrated_number_source']}
    selection=slice(0,2) if model=='heavy' else slice(2,4)
    def forcing(phase):
        original=quadratic(source,phase)[:,selection]
        increment=bubble(phase,route)*source['defect'][:,selection]
        revised=original+increment
        zero=np.zeros_like(original)
        return np.column_stack([original,revised,increment,zero,zero,revised])
    background=thermal_wave.thermal.ThermalBackground(model)
    emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    result,checks,metrics=integrate(model,count,initial,forcing,ladder,background,emission,.75,1.,
                                   f'{model}-{route}-{count}')
    for row in checks:
        row['name']=row['name'].replace('quadratic=secant+defect','revised=original+increment').replace(
            'old+new=old+quadratic','combined=old+revised')
    for key in ['photon','energy','gas','work','integrated_number_source']:
        for new_selection,old_selection,label in [(slice(0,2),slice(2,4),'original quadratic'),
                                                  (slice(8,10),slice(8,10),'old correction')]:
            error=result[key][...,new_selection]-prior[key][...,old_selection]
            scale=max(float(np.max(abs(prior[key][...,old_selection]))),1e-300)
            test(checks,'Saved response replay:'+label+':'+key,float(np.max(abs(error)))/scale,1e-10)
    np.savez_compressed(folder/'response.npz',**result)
    finish(folder,dict(checks=checks,model=model,route=route,steps=count,modes=96,metrics=metrics,
        heat=background.chi,interval=[.75,1.],response_to_measured_defect=True,
        column_groups=['original','revised','increment','zero','old','combined_direct'],
        baseline_inner_history_refined=False),__file__,
        [source_path,ROOT/'results/readiness/status.json',prior_path,*ladder.inputs,*emission.inputs,
         background.parent.source,background.native_constants,folder/'response.npz'])
    print(json.dumps(dict(model=model,route=route,steps=count,metrics=metrics,
        failed=[row for row in checks if not row['passed']])),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    args=parser.parse_args()
    allowed=verify_packet(ROOT/'results/readiness')['allowed_routes']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    for route in ['local','cubic']:
        if allowed[route]:
            for count in COUNTS:
                run(args.model,route,count,ladder)

