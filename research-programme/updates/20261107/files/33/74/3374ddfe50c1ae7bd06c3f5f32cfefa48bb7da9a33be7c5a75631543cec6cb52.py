from join_common import *
from propagate_matched_feedback import solve_response,readout


def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',required=True)
    parser.add_argument('--steps',type=int,choices=[512,1024],default=1024)
    args=parser.parse_args()
    modest()
    source_folder=ROOT/'results'/args.source
    metadata=json.loads((source_folder/'status.json').read_text())
    assert metadata['all_checks_passed']
    for path,sha in metadata['input_hashes'].items():
        assert digest(path)==sha,path
    folder=ROOT/'results'/('response-'+args.source.removeprefix('sources-')+'-n'+str(args.steps))
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    checks,models,inputs=[],{},[source_folder/'status.json',*ladder.inputs]
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        inputs.extend([*emission.inputs,background.parent.source,background.native_constants])
        for upper in UPPERS:
            path=source_folder/f'{model}-m{int(upper*1000)}.npz'
            inputs.append(path)
            source=read_npz(path)
            solution,errors=solve_response(model,source,args.steps,ladder,emission,background)
            metrics,view,dependencies=readout(basis,model,source,solution,'fine',upper)
            inputs.extend(dependencies)
            label=model+f'-m{int(upper*1000)}'
            for name,value in errors.items():
                checks.append(check(name+':'+label,value,1. if name=='energy_spectrum' else 1e-7))
            checks.append(check('Unresolved stored moments:'+label,metrics['unresolved_energy_number_defect'],1e-10))
            assert all(np.isfinite(value).all() for value in [*solution.values(),*view.values()])
            np.savez_compressed(folder/(label+'.npz'),**solution,**view)
            models[label]=dict(errors=errors,metrics=metrics)
            print(json.dumps(dict(case=args.source,model=label,steps=args.steps,errors=errors,metrics=metrics)),flush=True)
    finish(folder,dict(checks=checks,models=models,steps=args.steps,source_packet=args.source,
        forcing_groups=metadata['forcing_groups'],conditional_response=True,
        parent_history_rerun=False,paired_gas_exchange=True,join_term_discarded=False),__file__,inputs)


if __name__=='__main__':
    main()

