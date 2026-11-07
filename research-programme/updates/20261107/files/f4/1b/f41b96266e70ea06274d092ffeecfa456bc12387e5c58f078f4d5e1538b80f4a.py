from matching198 import *

def main():
    config=protocol();inputs=read(ROOT/'inputs.json');checks=[];records=[];cases={}
    for model in ('heavy','cold'):
        system=System(model,2048,inputs);heat=system.background.chi
        reader=saved.response.ShapeReadout(system.basis,canonical=True)
        for count in (2048,4096):
            folder=ROOT/'runs-matched'/f'{model}-{count}';status=read(folder/'status.json')
            for name,value in status['output_hashes'].items():
                assert digest(folder/name)==value,name
            checks.extend(dict(row,name=f'{model}:{count}:'+row['name']) for row in status['checks'])
            stop=round((config['interval'][1]-.75)*count/.25);target=round((config['target']-.75)*count/.25)
            boundary=packet(folder/f'interfaces/step-{stop}.npz')
            arrays={config['interval'][1]:boundary['current']}
            for fraction,index in [(config['target'],target),(1.,count)]:
                arrays[fraction]=packet(folder/f'transfer/step-{index}.npz')['current'][:,:148]
            output={}
            for fraction,values in arrays.items():
                selected=collapsed(values[:,SELECTED]);photon=system.coordinates.transform@selected[:96]
                split=reader.apply(photon,selected[0]);metrics=saved.response.metrics(split,heat,reader.measure)
                output[str(fraction)]=dict(metrics=metrics.tolist(),gas=(heat*selected[96]).tolist(),
                    energy=(heat*selected[0]).tolist(),work=(heat*selected[97]).tolist())
                save(ROOT/f'readouts/{model}-{count}-{fraction}.npz',**split,frequency=reader.frequency,
                     measure=reader.measure,heat=heat,gas=selected[96],work=selected[97],fraction=fraction)
            cases[(model,count)]=dict(output=output,status=status)
            record=dict(model=model,count=count,history=output,residual_gain=status['residual_gain'],
                        gain_bound_preimage=status['MTS_partial_allowance_boundary_norm'],
                        negative_controls=status['negative_controls'],failed_checks=len(status['failed_checks']))
            records.append(record)
        coarse=cases[(model,2048)];fine=cases[(model,4096)]
        check(checks,model+':residual gain step convergence',abs(coarse['status']['residual_gain']/fine['status']['residual_gain']-1),.01)
        for fraction in coarse['output']:
            first=packet(ROOT/f'readouts/{model}-2048-{fraction}.npz');second=packet(ROOT/f'readouts/{model}-4096-{fraction}.npz')
            for kind,offset in [('baseline',0),('MTS',2),('total',4)]:
                for profile in (0,1):
                    indices=slice(offset+6*profile,offset+6*profile+2)
                    denominator=np.maximum(saved.response.norm(second['residual'][:,indices],reader.measure),1e-300)
                    difference=saved.response.norm(first['residual'][:,indices]-second['residual'][:,indices],reader.measure)
                    check(checks,f'{model}:{fraction}:{kind}:profile{profile}:residual step convergence',np.max(difference/denominator),.01)
                    check(checks,f'{model}:{fraction}:{kind}:profile{profile}:gas step convergence',np.max(abs(first['gas'][indices]-second['gas'][indices])/np.maximum(abs(second['gas'][indices]),1e-300)),.01)
    retained=[]
    for attempt in ('runs','runs-stable','runs-connected'):
        path=ROOT/attempt/'heavy-2048/status.json';data=read(path)
        retained.append(dict(attempt=attempt,path=str(path),failed_checks=data['failed_checks'],count=len(data['failed_checks'])))
    for name in list(inputs):
        if Path(name).is_relative_to(ROOT):
            inputs.pop(name)
    for name,value in inputs.items():
        assert digest(name)==value,name
    check(checks,'consumed sources unchanged',0,0,'integrity')
    for name,value in config['bookmarks'].items():
        assert digest(name)==value,name
    started=datetime.fromisoformat(config['started_utc']).timestamp()
    workbench=BRANCH.parent.parent/'formalization-workbench'
    changed=[str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    check(checks,'protected workbench recent changes',len(changed),0,'integrity')
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    check(checks,'no bytecode or partial files',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial'))),0,'integrity')
    failed=[row for row in checks if not row['passed']]
    report=dict(stage=198,state='assessed',checks=checks,failed_checks=failed,all_selected_checks_passed=not failed,
                retained_attempts=retained,records=records,inputs_rehashed=len(inputs),
                scope='Derived and tested discrete matching of the known interval contribution; exterior source and full matching state not assigned',
                original_bank_changed=False,source_curve_changed=False,tolerances_changed=False,
                grids_changed=False,new_scattering_integrals=0,new_observational_test=False,
                protected_workbench_recent_modified_file_count=len(changed))
    write(ROOT/'results/status.json',report);write(ROOT/'inputs.json',inputs)
    contract=dict(state_representation='100 rows; high74 columns then low74; physical response and passive ledgers',
        rows={'energy_coordinate':0,'other95_photon_coordinates':[1,95],'gas':96,'expansion_work':97,'integrated_number':98,'integrated_source_pair':99},
        columns=dict(primary_high_columns=PRIMARY.tolist(),meaning='quadratic then linear: baseline join0/1, MTS increment join0/1, total join0/1',
                     low_offset=74,heavy_cold='background histories, not theory labels'),
        inside_interval=dict(required=['current','previous','step','index','global_startup_schedule'],files='runs-matched/<model>-<count>/interfaces/step-<index>.npz'),
        after_interval=dict(files='runs-matched/<model>-<count>/transfer/step-<index>.npz',
                            operator='ledger-evaluated energy row; raw_operator retained',
                            initial_older_state='discarded only by the inherited first homogeneous BE step'),
        ordinary_BDF_cut=dict(files='runs-matched/<model>-<count>/transfer/composition.npz',required=['current_map','previous_map']),
        history_input=dict(source=str(BRANCH/'precision-carried-gas-evolution-20261021'),
                           use='input h in microscopic F(theta,h), not an interchangeable response initial state'),
        unresolved_terms=['physical incoming response matching state from before the local interval','microscopic-source correction outside the verified interval'],
        derived_rule='Y_final=G(final,a)Y_incoming+known_interval_contribution+integral_after_interval(G*B*source_difference)',
        no_default_values_for_unresolved_terms=True)
    write(ROOT/'MATCHING-CONTRACT.json',contract)
    write(ROOT/'progress.json',dict(state='assessed',selected_failures=len(failed)))
    print(json.dumps(dict(checks=len(checks),selected_failures=failed,retained_failure_counts=[row['count'] for row in retained],
          summaries=[dict(model=row['model'],count=row['count'],gain=row['residual_gain'],boundary_norm=row['gain_bound_preimage']) for row in records])),flush=True)

if __name__=='__main__':
    main()
