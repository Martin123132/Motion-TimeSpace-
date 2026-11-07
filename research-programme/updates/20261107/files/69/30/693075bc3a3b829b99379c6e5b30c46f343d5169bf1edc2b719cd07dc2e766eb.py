from join_common import *
from propagate_matched_feedback import solve_response,readout


def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--steps',type=int,choices=[2048,4096,8192,16384],required=True)
    args=parser.parse_args()
    modest()
    source_folder=ROOT/'results/sources-o8-q32'
    metadata=json.loads((source_folder/'status.json').read_text())
    assert metadata['all_checks_passed']
    for path,sha in metadata['input_hashes'].items():
        assert digest(path)==sha,path
    folder=ROOT/'results'/f'response-o8-q32-n{args.steps}'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    checks,models,inputs=[],{},[source_folder/'status.json',*ladder.inputs,ROOT/'TIME-REFINEMENT-ADDENDUM.md']
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        inputs.extend([*emission.inputs,background.parent.source,background.native_constants])
        for upper in UPPERS:
            label=f'{model}-m{int(upper*1000)}'
            path=source_folder/(label+'.npz')
            source=read_npz(path)
            inputs.append(path)
            solution,errors=solve_response(model,source,args.steps,ladder,emission,background)
            metrics,view,dependencies=readout(basis,model,source,solution,'fine',upper)
            inputs.extend(dependencies)
            for name,value in errors.items():
                checks.append(check(name+':'+label,value,1. if name=='energy_spectrum' else 1e-7))
            checks.append(check('Unresolved stored moments:'+label,metrics['unresolved_energy_number_defect'],1e-10))
            selected=np.linspace(0,args.steps,129,dtype=int)
            sampled={key:value[selected] for key,value in solution.items()}
            assert all(np.isfinite(value).all() for value in [*sampled.values(),*view.values()])
            np.savez_compressed(folder/(label+'.npz'),**sampled,**view,integration_steps=args.steps,saved_step_indices=selected)
            models[label]=dict(errors=errors,metrics=metrics)
            print(json.dumps(dict(model=label,steps=args.steps,errors=errors)),flush=True)
    finish(folder,dict(checks=checks,models=models,steps=args.steps,source_packet=source_folder.name,
        saved_snapshots=129,snapshots_are_not_adjacent_integration_steps=True,
        equation_checks_at_all_integration_steps=True,forcing_groups=metadata['forcing_groups'],
        parent_history_rerun=False,paired_gas_exchange=True,join_term_discarded=False),__file__,inputs)


if __name__=='__main__':
    main()

