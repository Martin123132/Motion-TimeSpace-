from stage166_common import *
from twofold_sources import TwofoldSources
from evolve_twofold_checked import integrate,terminal
import argparse


def run(model,route,count,smoke=False,mode='split'):
    category='response-smoke-checked' if smoke else 'response'
    label=f'{model}-{route}-{count}'+('-'+mode if smoke else '')
    folder=ROOT/'results'/category/label
    if (folder/'COMPLETE').exists():
        assert verify_packet(folder)['all_checks_passed']
        return
    qualification=verify_packet(ROOT/'results/source-qualification')
    assert qualification['all_checks_passed'] and qualification['source_qualified']
    if not smoke:
        assert verify_packet(ROOT/'results/response-readiness-checked')['all_checks_passed']
        assert count in COUNTS and mode=='split'
    folder.mkdir(parents=True,exist_ok=True)
    evaluator=TwofoldSources()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    background=thermal_wave.thermal.ThermalBackground(model)
    emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    selection=slice(0,2) if model=='heavy' else slice(2,4)
    initial={key:np.zeros((96,24)) if key=='photon' else np.zeros(24) for key in ['photon','energy','gas','work','integrated_number_source']}
    checks,metrics,source_maxima,inputs=[],{}, {}, [ROOT/'results/source-qualification/status.json',*evaluator.inputs,*ladder.inputs,*emission.inputs,background.parent.source,background.native_constants]
    if not smoke:
        inputs.append(ROOT/'results/response-readiness-checked/status.json')
    for window,lower,upper in [('earlier',.5,.75),('terminal',.75,1.)]:
        packet=folder/window
        if (packet/'COMPLETE').exists():
            saved=verify_packet(packet)
            assert saved['all_checks_passed']
            result=read_npz(folder/(window+'.npz'))
            checks.extend(saved['checks'])
            metrics[window]=saved['metrics']
            source_maxima.update(saved['source_maxima'])
            initial=terminal(result)
            inputs.extend([packet/'status.json',folder/(window+'.npz')])
            continue
        if datetime.now(timezone.utc)>=datetime.fromisoformat(DEADLINE):
            write_json(folder/'PAUSED.json',dict(next_window=window,utc=datetime.now(timezone.utc).isoformat(),reason='safe deadline'))
            raise SystemExit(75)
        packet.mkdir(parents=True,exist_ok=False)
        def forcing(phase):
            source=evaluator.forcing(phase,route,window,selection)
            for name,value in source['metrics'].items():
                key=window+':'+name
                source_maxima[key]=max(source_maxima.get(key,0.),value)
            if mode=='singlecast':
                for high,low in [('high','low'),('force_high','force_low'),('spectral_high','spectral_low')]:
                    source[high]=source[high]+source[low]
                    source[low]=np.zeros_like(source[low])
            return source
        result,window_checks,window_metrics=integrate(model,count,initial,forcing,ladder,background,emission,lower,upper,label+'-'+window)
        for quantity in ['photon','gas','energy','work','number','integrated_number_source']:
            values=result[quantity]
            close(window_checks,'Physical endpoint superposition:'+window+':'+quantity,values[...,12:14]+values[...,14:16],values[...,8:10],1e-8)
            close(window_checks,'Physical order telescope:'+window+':'+quantity,values[...,16:18]+values[...,18:20],values[...,8:10],1e-8)
            close(window_checks,'Reference/physical split:'+window+':'+quantity,values[...,2:4]+values[...,8:10],values[...,22:24],1e-8)
            close(window_checks,'Recorded high/low response:'+window+':'+quantity,result[quantity+'_high']+result[quantity+'_low'],values,1e-10)
        for name,value in source_maxima.items():
            if name.startswith(window+':'):
                test(window_checks,'Actual response raw source:'+name,value,1e-10)
        path=folder/(window+'.npz')
        np.savez_compressed(path,**result)
        finish(packet,dict(checks=window_checks,metrics=window_metrics,source_maxima={key:value for key,value in source_maxima.items() if key.startswith(window+':')},
            model=model,route=route,steps=count,window=window,mode=mode,diagnostic_smoke=smoke,high_low_outputs_retained=True),__file__,[*inputs,path])
        print(json.dumps(dict(model=model,route=route,count=count,window=window,mode=mode,passed=all(row['passed'] for row in window_checks),metrics=window_metrics,
            failed=[row for row in window_checks if not row['passed']])),flush=True)
        assert all(row['passed'] for row in window_checks)
        checks.extend(window_checks)
        metrics[window]=window_metrics
        inputs.extend([path,packet/'status.json'])
        initial=terminal(result)
    finish(folder,dict(checks=checks,metrics=metrics,source_maxima=source_maxima,model=model,route=route,steps=count,heat=background.chi,mode=mode,
        diagnostic_smoke=smoke,high_low_outputs_retained=True,reference_history_replayed=True,reference_history_adopted=False,
        source_windows=[[.5,.75],[.75,1.]],baseline_inner_history_reused=True,temperature_curve_changed=False,bands_changed=False),__file__,inputs)


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    arguments=parser.parse_args()
    for route in ['local','cubic']:
        for count in COUNTS:
            run(arguments.model,route,count)


