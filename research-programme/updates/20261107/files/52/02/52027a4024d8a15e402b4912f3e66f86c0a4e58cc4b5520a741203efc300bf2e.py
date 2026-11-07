from stage159_common import *
from evolve_adjacent_window import integrate
import argparse


def run(model,route,count,ladder):
    folder=ROOT/'results/response'/f'{model}-{route}-{count}'
    if (folder/'COMPLETE').exists():
        assert verify_packet(folder)['all_checks_passed']
        return
    folder.mkdir(parents=True,exist_ok=False)
    source_path=ROOT/'results/sources/source.npz'
    data=read_npz(source_path)
    proof=verify_packet(source_path.parent)
    assert proof['numerical_integrity_passed'] and proof['allowed_routes'][route]
    selection=slice(0,2) if model=='heavy' else slice(2,4)
    initial={key:np.zeros((96,18)) if key=='photon' else np.zeros(18)
        for key in ['photon','energy','gas','work','integrated_number_source']}
    def forcing(phase):
        pieces=[increment_source(data,phase,route,site)[:,selection] for site in SITES]
        cold=pieces[0]
        remainder=sum(pieces[1:])
        total=cold+remainder
        zero=np.zeros_like(total)
        return np.column_stack([cold,total,remainder,zero,zero,total,*pieces])
    background=thermal_wave.thermal.ThermalBackground(model)
    emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    result,checks,metrics=integrate(model,count,initial,forcing,ladder,background,emission,.75,1.,f'{model}-{route}-{count}')
    for key in ['photon','gas','energy','work','number','integrated_number_source']:
        value=result[key]
        close(checks,'Three site responses sum on own scale:'+key,
            sum(value[...,start:start+2] for start in [12,14,16]),value[...,2:4],1e-8)
        close(checks,'Independent cold-response duplicate:'+key,value[...,12:14],value[...,:2],1e-10)
    np.savez_compressed(folder/'response.npz',**result)
    finish(folder,dict(checks=checks,model=model,route=route,steps=count,heat=background.chi,metrics=metrics,
        columns=['cold','all_temperatures','warm_plus_centre','zero','zero_old','all_direct','cold_piece','warm_piece','centre_piece'],
        initial_increment_zero=True,baseline_inner_rerun=False,band38_rerun=False,
        temperature_curve_changed=False),__file__,
        [source_path,source_path.parent/'status.json',*ladder.inputs,*emission.inputs,
            background.parent.source,background.native_constants,folder/'response.npz'])
    print(json.dumps(dict(model=model,route=route,count=count,checks=len(checks),
        failed=[row for row in checks if not row['passed']])),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--stop-at',default='2026-10-18T22:05:00+00:00')
    args=parser.parse_args()
    stop_at=datetime.fromisoformat(args.stop_at)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    allowed=verify_packet(ROOT/'results/sources')['allowed_routes']
    for route in ['local','cubic']:
        if allowed[route]:
            for count in COUNTS:
                if datetime.now(timezone.utc)>=stop_at:
                    raise SystemExit(75)
                run(args.model,route,count,ladder)

