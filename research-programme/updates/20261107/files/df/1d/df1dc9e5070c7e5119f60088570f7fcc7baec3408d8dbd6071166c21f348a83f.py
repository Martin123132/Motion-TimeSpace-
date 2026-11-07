from stage168_common import *
from evolve_heldout import integrate


def main():
    modest()
    preflight=verify_packet(ROOT/'results/preflight')
    assert preflight['numerical_production_allowed'] and preflight['closed_reference_bitwise_recovered']
    evaluator=HeldoutSources()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    for model in ['heavy','cold']:
        selection=slice(0,2) if model=='heavy' else slice(2,4)
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        for route in ['local','cubic']:
            for count in COUNTS:
                folder=ROOT/'results/response'/f'{model}-{route}-{count}'
                if (folder/'COMPLETE').exists():
                    assert verify_packet(folder)['all_checks_passed']
                    continue
                if datetime.now(timezone.utc)>=datetime.fromisoformat(DEADLINE):
                    raise SystemExit(75)
                folder.mkdir(parents=True,exist_ok=False)
                write_json(folder/'progress.json',dict(state='running',model=model,route=route,count=count,started_utc=datetime.now(timezone.utc).isoformat()))
                initial={key:np.zeros((96,24)) if key=='photon' else np.zeros(24) for key in
                    ['photon','energy','gas','work','integrated_number_source']}
                result,checks,diagnostics=integrate(model,count,initial,lambda phase:evaluator.forcing(phase,route,selection),
                    ladder,background,emission,.75,1.,f'{model}-{route}-{count}')
                for key in ['photon','energy','gas','work','number','integrated_number_source']:
                    close(checks,'Direct current duplicate:'+key,result[key][...,20:22],result[key][...,2:4],1e-10)
                assert np.array_equal(result['integrated_imbalance'][:,2:4],np.zeros_like(result['integrated_imbalance'][:,2:4]))
                np.savez_compressed(folder/'response.npz',**result)
                finish(folder,dict(checks=checks,model=model,route=route,steps=count,heat=background.chi,metrics=diagnostics,
                    groups=GROUPS,source_imbalance_is_diagnostic_not_physical_injection=True,baseline_inner_rerun=False,
                    independent_raw_physical_source_qualified=False,temperature_curve_changed=False),
                    [ROOT/'results/preflight/status.json',*evaluator.inputs,*ladder.inputs,*emission.inputs,
                        background.parent.source,background.native_constants,folder/'response.npz'])
                write_json(folder/'progress.json',dict(state='complete',finished_utc=datetime.now(timezone.utc).isoformat()))
                failures=[row for row in checks if not row['passed']]
                print(json.dumps(dict(case=folder.name,checks=len(checks),failures=failures)),flush=True)
                assert not failures


if __name__=='__main__':
    main()
