from stage147_step_common import *
from evolve_adjacent_window import integrate,terminal
import argparse


def run(model,count,ladder):
    assert count in [2048,4096]
    source_path=PARENT/'results/repaired-readiness/source.npz'
    data=read_npz(source_path)
    background=thermal_wave.thermal.ThermalBackground(model)
    emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    original_path=response_folder(model,1024,'active')/'response.npz'
    original=read_npz(original_path)
    initial={key:original[key][0].copy() for key in ['photon','energy','gas','work','integrated_number_source']}
    inputs=[source_path,PARENT/'results/repaired-readiness/status.json',original_path,
            ROOT/'results/preflight/status.json',*ladder.inputs,*emission.inputs,
            background.parent.source,background.native_constants]
    selection=slice(0,2) if model=='heavy' else slice(2,4)
    def forcing(phase):
        forecast_value=forecast(data,data['warm_defect'],phase,'cubic')[:,selection]
        increment=cold_bubble(phase,'cubic')*data['cubic_defect'][:,selection]
        revised=forecast_value+increment
        zero=np.zeros_like(revised)
        return np.column_stack([forecast_value,revised,increment,zero,zero,revised])
    active=None
    for phase,lower,upper in [('active',.5,.75),('transfer',.75,1.)]:
        folder=response_folder(model,count,phase)
        if (folder/'COMPLETE').exists():
            report=verify_packet(folder)
            assert report['all_checks_passed']
            result=read_npz(folder/'response.npz')
        else:
            folder.mkdir(parents=True,exist_ok=False)
            seed=initial if phase=='active' else terminal(active)
            source=forcing if phase=='active' else lambda fraction:np.zeros((98,12))
            result,checks,row=integrate(model,count,seed,source,ladder,background,emission,
                                       lower,upper,f'{model}-{count}-{phase}')
            np.savez_compressed(folder/'response.npz',**result)
            extra=inputs+[folder/'response.npz']
            if phase=='transfer':
                previous_folder=response_folder(model,count,'active')
                extra.extend([previous_folder/'response.npz',previous_folder/'status.json'])
            report=dict(checks=checks,model=model,steps=count,modes=96,phase=phase,metrics=row,
                source_reused=True,frequency_grid_unchanged=True,heat=background.chi)
            finish(folder,report,__file__,extra)
            print(json.dumps(dict(model=model,steps=count,phase=phase,metrics=row,
                failed=[item for item in checks if not item['passed']])),flush=True)
            assert report['all_checks_passed']
        if phase=='active':
            active=result


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    args=parser.parse_args()
    assert verify_packet(ROOT/'results/preflight')['all_checks_passed']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    for count in [2048,4096]:
        run(args.model,count,ladder)
