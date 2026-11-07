from stage152_order6_common import *
from evolve_adjacent_window import integrate
import argparse


def run(model,case,count,ladder):
    folder=ROOT/'results/response'/f'{model}-{case}-{count}'
    if (folder/'COMPLETE').exists():
        assert verify_packet(folder)['all_checks_passed']
        return
    folder.mkdir(parents=True,exist_ok=False)
    source_path=ROOT/'results/integration-source/source.npz'
    source=read_npz(source_path)
    assert verify_packet(ROOT/'results/readiness')['allowed_cases'][case]
    route,order=CASES[case]
    prior_path=PARENT/'results/response'/f'{model}-{route}-order5-{count}/response.npz'
    prior=read_npz(prior_path)
    initial={}
    for key in ['photon','energy','gas','work','integrated_number_source']:
        values=prior[key][0]
        initial[key]=values.copy()
        assert initial[key].shape[-1]==18
        assert not np.any(initial[key][...,12:])
    selection=slice(0,2) if model=='heavy' else slice(2,4)
    def forcing(phase):
        original=central_source(source,phase,route)[:,selection]
        bubble=cold_bubble(phase,route)
        increment=bubble*source[f'delta{order}_total'][:,selection]
        components=[bubble*source[f'delta{order}_{key}'][:,selection] for key in COMPONENTS]
        revised=original+increment
        zero=np.zeros_like(original)
        return np.column_stack([original,revised,increment,zero,zero,revised,*components])
    background=thermal_wave.thermal.ThermalBackground(model)
    emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    result,checks,metrics=integrate(model,count,initial,forcing,ladder,background,emission,.75,1.,f'{model}-{case}-{count}')
    for row in checks:
        row['name']=row['name'].replace('quadratic=secant+defect','revised=central+increment').replace(
            'old+new=old+quadratic','combined=old+revised')
    for key in ['photon','energy','gas','work','number','integrated_number_source']:
        value=result[key]
        parts=value[...,12:14]+value[...,14:16]+value[...,16:18]
        error=value[...,4:6]-parts
        scale=max(float(np.max(abs(value[...,4:6]))),1e-300)
        test(checks,'Direct coherent increment equals D+V+S on own scale:'+key,float(np.max(abs(error)))/scale,1e-8)
        for current,previous,label in [(slice(0,2),slice(2,4),'central'),(slice(8,10),slice(8,10),'older')]:
            error=value[...,current]-prior[key][...,previous]
            scale=max(float(np.max(abs(prior[key][...,previous]))),1e-300)
            test(checks,'Stage151 replay:'+label+':'+key,float(np.max(abs(error)))/scale,1e-10)
    np.savez_compressed(folder/'response.npz',**result)
    finish(folder,dict(checks=checks,model=model,case=case,route=route,order=order,steps=count,modes=96,
        metrics=metrics,heat=background.chi,interval=[.75,1.],baseline_inner_history_refined=False,
        column_groups=['central','revised','increment','zero','old','combined_direct',*COMPONENTS]),
        __file__,[source_path,ROOT/'results/readiness/status.json',prior_path,*ladder.inputs,*emission.inputs,
            background.parent.source,background.native_constants,folder/'response.npz'])
    print(json.dumps(dict(model=model,case=case,steps=count,failed=[row for row in checks if not row['passed']])),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    args=parser.parse_args()
    allowed=verify_packet(ROOT/'results/readiness')['allowed_cases']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    for case in CASES:
        if allowed[case]:
            for count in COUNTS:
                run(args.model,case,count,ladder)
