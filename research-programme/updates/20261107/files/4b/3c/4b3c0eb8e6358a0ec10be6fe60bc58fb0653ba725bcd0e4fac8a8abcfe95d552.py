from stage148_terminal_common import *
from evolve_adjacent_window import integrate
import argparse


def run(model,count,ladder):
    folder=ROOT/'results/response'/f'{model}-{count}'
    if (folder/'COMPLETE').exists():
        assert verify_packet(folder)['all_checks_passed']
        return
    folder.mkdir(parents=True,exist_ok=False)
    source_path=ROOT/'results/terminal-sources/source.npz'
    source=read_npz(source_path)
    readiness=verify_packet(ROOT/'results/readiness')
    assert readiness['all_checks_passed'] and readiness['energy_coordinate_evolution_allowed']
    old_path=PARENT/'results/response'/f'{model}-4096/active/response.npz'
    old=read_npz(old_path)
    initial={key:np.zeros((96,12)) if key=='photon' else np.zeros(12)
             for key in ['photon','energy','gas','work','integrated_number_source']}
    for key in initial:
        initial[key][...,8:10]=old[key][-1,...,10:12]
        initial[key][...,10:12]=old[key][-1,...,10:12]
    selection=slice(0,2) if model=='heavy' else slice(2,4)
    start,end,curvature=[source[key][:,selection] for key in ['start','end','curvature']]
    def forcing(phase):
        secant=(1-phase)*start+phase*end
        increment=4*phase*(1-phase)*curvature
        quadratic_value=secant+increment
        zero=np.zeros_like(secant)
        return np.column_stack([secant,quadratic_value,increment,zero,zero,quadratic_value])
    background=thermal_wave.thermal.ThermalBackground(model)
    emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    result,checks,metrics=integrate(model,count,initial,forcing,ladder,background,emission,.75,1.,f'{model}-{count}')
    previous_path=PARENT/'results/response'/f'{model}-4096/transfer/response.npz'
    previous=read_npz(previous_path)
    if count==4096:
        for key in ['photon','energy','gas','work','integrated_number_source']:
            difference=result[key][...,8:10]-previous[key][...,10:12]
            scale=max(float(np.max(abs(previous[key][...,10:12]))),1e-300)
            test(checks,'Unchanged saved old correction replay:'+key,float(np.max(abs(difference)))/scale,1e-10)
    np.savez_compressed(folder/'response.npz',**result)
    finish(folder,dict(checks=checks,model=model,steps=count,modes=96,metrics=metrics,heat=background.chi,
        interval=[.75,1.],source_fixed=True,baseline_inner_history_refined=False),
        __file__,[source_path,ROOT/'results/readiness/status.json',old_path,previous_path,
                  *ladder.inputs,*emission.inputs,background.parent.source,background.native_constants,
                  folder/'response.npz'])
    print(json.dumps(dict(model=model,steps=count,metrics=metrics,
        failed=[row for row in checks if not row['passed']])),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    args=parser.parse_args()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    for count in COUNTS:
        run(args.model,count,ladder)

