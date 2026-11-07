from stage162_common import *
from evolve_adjacent_window import integrate
import argparse


def run(model,route,count,ladder):
    folder=ROOT/'results/response'/f'{model}-{route}-{count}'
    if (folder/'COMPLETE').exists():
        assert verify_packet(folder)['all_checks_passed']
        return
    folder.mkdir(parents=True,exist_ok=False)
    source_path=ROOT/'results/sources/source.npz'
    assert verify_packet(source_path.parent)['all_checks_passed']
    data=read_npz(source_path)
    selection=slice(0,2) if model=='heavy' else slice(2,4)
    initial={key:np.zeros((96,24)) if key=='photon' else np.zeros(24)
        for key in ['photon','energy','gas','work','integrated_number_source']}
    vectors={step:data['endpoint_delta'+step].sum(axis=(0,2)) for step in ['54','65','64']}
    def forcing(phase):
        pieces={step:[endpoint_response_basis(phase,route,endpoint)*vectors[step][index][:,selection]
            for index,endpoint in enumerate(ENDPOINTS)] for step in vectors}
        start,end=pieces['64']
        total=start+end
        zero=np.zeros_like(total)
        return np.column_stack([start,total,end,zero,zero,total,*pieces['65'],sum(pieces['65']),*pieces['54'],sum(pieces['54'])])
    background=thermal_wave.thermal.ThermalBackground(model)
    emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    result,checks,metrics=integrate(model,count,initial,forcing,ladder,background,emission,.75,1.,f'{model}-{route}-{count}')
    for key in ['photon','gas','energy','work','number','integrated_number_source']:
        value=result[key]
        close(checks,'Endpoint last-step superposition:'+key,value[...,12:14]+value[...,14:16],value[...,16:18],1e-8)
        close(checks,'Endpoint first-step superposition:'+key,value[...,18:20]+value[...,20:22],value[...,22:24],1e-8)
        close(checks,'Endpoint response order telescope:'+key,value[...,16:18]+value[...,22:24],value[...,2:4],1e-8)
    np.savez_compressed(folder/'response.npz',**result)
    finish(folder,dict(checks=checks,model=model,route=route,steps=count,heat=background.chi,metrics=metrics,
        columns=['start64','total64','end64','zero','zero_old','duplicate64','start65','end65','total65','start54','end54','total54'],
        diagnostic_only=True,temperature_curve_changed=False,earlier_window_history_fixed=True,
        baseline_inner_rerun=False,lower_bands_rerun=False),__file__,
        [source_path,source_path.parent/'status.json',*ladder.inputs,*emission.inputs,
            background.parent.source,background.native_constants,folder/'response.npz'])
    print(json.dumps(dict(model=model,route=route,count=count,checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--stop-at',default=DEADLINE)
    args=parser.parse_args()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    for route in ['local','cubic']:
        for count in COUNTS:
            if datetime.now(timezone.utc)>=datetime.fromisoformat(args.stop_at):
                raise SystemExit(75)
            run(args.model,route,count,ladder)
