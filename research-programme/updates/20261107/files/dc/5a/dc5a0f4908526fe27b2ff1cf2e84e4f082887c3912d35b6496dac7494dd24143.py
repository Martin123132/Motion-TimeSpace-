from stage158_common import *
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
    initial={key:np.zeros((96,24)) if key=='photon' else np.zeros(24)
        for key in ['photon','energy','gas','work','integrated_number_source']}
    def forcing(phase):
        pieces=[site_basis(phase,route,site)*data[f'band{band}_{site}_total'][:,selection]
            for band in BANDS for site in SITES]
        first=sum(pieces[:3])
        second=sum(pieces[3:])
        zero=np.zeros_like(first)
        return np.column_stack([first,first+second,second,zero,zero,first+second,*pieces])
    background=thermal_wave.thermal.ThermalBackground(model)
    emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    result,checks,metrics=integrate(model,count,initial,forcing,ladder,background,emission,.75,1.,f'{model}-{route}-{count}')
    for key in ['photon','gas','energy','work','number','integrated_number_source']:
        value=result[key]
        for group,selection,starts in [('band3',slice(0,2),[12,14,16]),('band4',slice(4,6),[18,20,22])]:
            close(checks,'Site response sum:'+group+':'+key,sum(value[...,start:start+2] for start in starts),value[...,selection],1e-8)
    np.savez_compressed(folder/'response.npz',**result)
    finish(folder,dict(checks=checks,model=model,route=route,steps=count,heat=background.chi,metrics=metrics,
        columns=['band3','both_bands','band4','zero','zero_old','both_direct',
            'band3_cold','band3_warm','band3_centre','band4_cold','band4_warm','band4_centre'],
        initial_increment_zero=True,baseline_inner_rerun=False,temperature_curve_changed=False),__file__,
        [source_path,source_path.parent/'status.json',*ladder.inputs,*emission.inputs,
            background.parent.source,background.native_constants,folder/'response.npz'])
    print(json.dumps(dict(model=model,route=route,count=count,checks=len(checks),
        failed=[row for row in checks if not row['passed']])),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--stop-at',default='2026-10-18T20:00:00+00:00')
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

