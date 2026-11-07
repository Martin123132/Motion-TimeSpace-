from stage166_common import *
from replay_twofold import run


def main():
    modest()
    folder=ROOT/'results/response-readiness'
    folder.mkdir(parents=True,exist_ok=False)
    assert verify_packet(ROOT/'results/source-qualification')['source_qualified']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    checks,inputs,records=[],[ROOT/'results/source-qualification/status.json',*ladder.inputs],{}
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for mode in ['split','singlecast']:
                run(model,route,32,True,mode)
            paths={mode:ROOT/'results/response-smoke'/f'{model}-{route}-32-{mode}' for mode in ['split','singlecast']}
            for mode,path in paths.items():
                packet=verify_packet(path)
                assert packet['all_checks_passed']
                inputs.append(path/'status.json')
                checks.append(dict(name='Short response all equations:'+model+':'+route+':'+mode,passed=True))
            for window in ['earlier','terminal']:
                states={mode:read_npz(path/(window+'.npz')) for mode,path in paths.items()}
                inputs.extend(path/(window+'.npz') for path in paths.values())
                for quantity in ['photon','gas','energy','work','number','integrated_number_source']:
                    close(checks,f'Split versus direct singlecast control:{model}:{route}:{window}:{quantity}',states['split'][quantity],states['singlecast'][quantity],1e-8)
                assert np.any(states['split']['photon_low'])
            records[model+'-'+route]=dict(split_retained_low_state=True,control_not_source_adoption=True)
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    checks.append(dict(name='Current scripts compile without bytecode',passed=True))
    finish(folder,dict(checks=checks,records=records,production_steps=COUNTS,diagnostic_steps=32,baseline_inner_history_rerun=False,
        baseline_control='Saved nonzero baseline retained for matched readout;zero-extra-source is a separate response control.',production_allowed=all(row['passed'] for row in checks)),__file__,inputs)
    print(json.dumps(dict(allowed=all(row['passed'] for row in checks),checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
