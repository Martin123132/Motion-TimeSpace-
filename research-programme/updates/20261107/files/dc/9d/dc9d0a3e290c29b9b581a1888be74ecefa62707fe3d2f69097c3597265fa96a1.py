from response_time_common import *
from propagate_matched_feedback import solve_response
from propagate_repaired_feedback import readout
import argparse
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--upper',type=float,choices=[.04,.02],required=True)
    parser.add_argument('--steps',type=int,choices=[4096],default=4096)
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    label=f'm{int(args.upper*1000)}'
    folder=ROOT/'results'/(f'preflight-{label}' if args.dry_run else f'response-{label}-r{args.steps}')
    folder.mkdir(parents=True,exist_ok=False)
    parent_folder=PARENT/'results'/f'feedback-{label}-n10240'
    parent_status=local_packet(parent_folder)
    assert all(row['passed'] for row in parent_status['checks'] if row['name'].startswith('Source:'))
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=[*ladder.inputs,parent_folder/'status.json']
    checks,models=[],{}
    chain=ancestors()
    for model in ['heavy','cold']:
        source_path=parent_folder/(model+'-source.npz')
        inner_path=PARENT/'results'/f'inner-{model}-n10240/prediction.npz'
        source=read_npz(source_path)
        prediction=read_npz(inner_path)
        inner_status=local_packet(inner_path.parent)
        assert inner_status['all_checks_passed']
        before={str(path):digest(path) for path in [source_path,inner_path]}
        inputs.extend([source_path,inner_path,inner_path.parent/'status.json'])
        assert len(prediction['frequency'])==5265 and int(prediction['steps'])==10240
        assert len(source['coordinate'])==65 and np.array_equal(source['coordinate'],prediction['coordinate'])
        assert float(source['match_upper'])==args.upper
        assert np.array_equal(source['profiles'],prediction['profiles'])
        assert np.array_equal(source['gas'],prediction['gas'])
        assert not np.count_nonzero(source['source'][0])
        assert all(np.isfinite(value).all() for value in source.values())
        checks.append(dict(name='Fixed sealed inner evolution and source epochs:'+model,passed=True))
        checks.append(dict(name='Inherited physical source checks pass:'+model,passed=True))
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        inputs.extend([*emission.inputs,background.parent.source,background.native_constants])
        if not args.dry_run:
            solution,errors=solve_response(model,source,args.steps,ladder,emission,background)
            metrics,view=readout(basis,prediction,source,solution,args.upper)
            checks.extend(check('Response:'+model+':'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in errors.items())
            checks.append(check('Unresolved moments:'+model,metrics['unresolved_energy_number_defect'],1e-10))
            assert all(np.isfinite(value).all() for value in [*solution.values(),*view.values()])
            np.savez_compressed(folder/(model+'-response.npz'),**solution,**view,integration_steps=args.steps,
                saved_step_indices=np.arange(args.steps+1),all_steps_saved=True)
            models[model]=dict(errors=errors,metrics=metrics)
            print(json.dumps(dict(model=model,upper=args.upper,steps=args.steps,errors=errors,seconds=time.monotonic()-started)),flush=True)
            del solution,view
        assert all(digest(path)==sha for path,sha in before.items())
        checks.append(dict(name='Source and inner files remain byte-identical:'+model,passed=True,hashes=before))
    for path in inputs:
        verify_source(path,chain)
    finish(folder,dict(checks=checks,models=models,upper=args.upper,response_steps=args.steps,
        dry_run=args.dry_run,fixed_frequency_nodes=5265,fixed_inner_steps=10240,source_epochs=65,
        sources_reused_without_recomputation=True,all_response_states_saved=True,
        inner_evolution_recomputed=False,parent_history_rerun=False,new_physical_inputs=False,
        raw_gas_gate_relaxed=False,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(packet=folder.name,checks=len(checks),failed=[row['name'] for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
