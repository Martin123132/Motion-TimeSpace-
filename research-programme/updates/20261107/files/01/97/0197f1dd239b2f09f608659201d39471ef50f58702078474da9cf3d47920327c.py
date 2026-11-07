from common197 import *

def metric(split,heat,measure):
    return response.metrics(split,heat,measure)

def assess():
    config=frozen();inputs=read(ROOT/'inputs.json');checks=list(read(ROOT/'sources/status.json')['checks']);summaries=[]
    for model in ('heavy','cold'):
        ladder,background,emission=setup(model,inputs)
        reader=response.ShapeReadout(ladder.basis,canonical=True)
        cases={}
        for count in config['counts']:
            folder=ROOT/'responses'/f'{model}-{count}'
            status=read(folder/'status.json')
            assert status['full_final_epoch'] and digest(folder/'terminal.npz')==status['terminal_sha256']
            checks.extend(dict(row,name=f'{model}:{count}:'+row['name']) for row in status['checks'])
            data=packet(folder/'terminal.npz');assert float(data['final_fraction'])==1.
            upper=reader.apply(data['photon_high'],data['energy_high'])
            lower=reader.apply(data['photon_low'],data['energy_low'])
            split=reader.split_values(upper['potential']+lower['potential'],data['energy_high']+data['energy_low'])
            cases[count]=(data,split)
            save(ROOT/f'readouts/{model}-{count}.npz',**split,frequency=reader.frequency,measure=reader.measure,heat=background.chi)
            independent=linalg.lstsq(reader.design,np.sqrt(reader.measure)[:,None]*split['distortion'],lapack_driver='gelsd')[0]/reader.template_norms[:,None]
            check(checks,f'{model}:{count}:independent SVD mu-y',np.max(abs(independent-split['amplitudes']))/max(float(np.max(abs(split['amplitudes']))),1e-300),1e-10,'identity')
        coarse,coarse_split=cases[2048];fine,fine_split=cases[4096]
        for version in range(6):
            for kind in range(3):
                selection=slice(version*6+kind*2,version*6+kind*2+2)
                for quantity in ('potential','residual'):
                    difference=response.norm(fine_split[quantity][:,selection]-coarse_split[quantity][:,selection],reader.measure)
                    scale=np.maximum(response.norm(fine_split[quantity][:,selection],reader.measure),1e-300)
                    check(checks,f'{model}:time-step:{VERSIONS[version]}:{KINDS[kind]}:{quantity}',np.max(difference/scale),.01)
                check(checks,f'{model}:time-step:{VERSIONS[version]}:{KINDS[kind]}:gas',
                      np.max(abs(fine['gas'][selection]-coarse['gas'][selection])/np.maximum(abs(fine['gas'][selection]),1e-300)),.01)
        for kind in range(3):
            primary=slice(24+kind*2,26+kind*2);alternative=slice(61+kind*2,63+kind*2)
            history=slice(18+kind*2,20+kind*2)
            for name,other in [('linear-quadratic',alternative),('history-half-quarter',history)]:
                error=response.norm(fine_split['residual'][:,primary]-fine_split['residual'][:,other],reader.measure)
                scale=np.maximum(response.norm(fine_split['residual'][:,primary],reader.measure),1e-300)
                check(checks,f'{model}:{name}:{KINDS[kind]}:residual',np.max(error/scale),.01)
        for route in ('local','cubic'):
            for matching in (20,40):
                reference_path=BRANCH/f'endpoint-twofold-response-20261019/results/comparison/{model}-{route}-4096-m{matching}.npz'
                budget_path=BRANCH/f'final-spectrum-uncertainty-20261019/results/budget-ready/{model}-{route}-m{matching}.npz'
                reference=packet(register(inputs,reference_path));budget=packet(register(inputs,budget_path))
                assert np.array_equal(reference['frequency'],reader.frequency) and np.array_equal(reference['measure'],reader.measure)
                assert np.array_equal(reference['potential'][:,0],budget['central_potential'][:,0])
                assert np.array_equal(reference['potential'][:,3:5],budget['central_potential'][:,5:7])
                selected=[0,0,3,4,7,8]
                saved=reader.split_values(reference['potential'][:,selected],reference['energy'][selected])
                delta=reader.split_values(fine_split['potential'][:,24:30],fine['energy'][24:30])
                updated=reader.split_values(saved['potential']+delta['potential'],saved['energy']+delta['energy'])
                direct=metric(delta,background.chi,reader.measure)
                saved_metrics=metric(saved,background.chi,reader.measure)
                updated_metrics=metric(updated,background.chi,reader.measure)
                coarse_delta=reader.split_values(coarse_split['potential'][:,24:30],coarse['energy'][24:30])
                timestep=reader.split_values(delta['potential']-coarse_delta['potential'],delta['energy']-coarse_delta['energy'])
                shapechange=reader.split_values(fine_split['potential'][:,61:67]-delta['potential'],fine['energy'][61:67]-delta['energy'])
                time_metrics=metric(timestep,background.chi,reader.measure)
                profile_metrics=metric(shapechange,background.chi,reader.measure)
                check(checks,f'{model}:{route}:{matching}:updated baseline+MTS=total',np.max(abs(updated['potential'][:,4:6]-updated['potential'][:,:2]-updated['potential'][:,2:4]))/max(float(np.max(abs(updated['potential'][:,4:6]))),1e-300),1e-8,'identity')
                relative=abs(direct[3,2:4])/np.maximum(saved_metrics[3,2:4],1e-300)
                row=dict(model=model,route=route,matching=matching,
                         MTS_residual_interval_addition=direct[3,2:4].tolist(),
                         MTS_residual_saved=saved_metrics[3,2:4].tolist(),
                         MTS_residual_norm_change=(updated_metrics[3,2:4]-saved_metrics[3,2:4]).tolist(),
                         MTS_residual_addition_fraction=relative.tolist(),
                         MTS_partial_allowance=budget['allowance'][3].tolist(),
                         MTS_addition_over_partial_allowance=(direct[3,2:4]/budget['allowance'][3]).tolist(),
                         baseline_residual_interval_addition=direct[3,:2].tolist(),
                         baseline_residual_saved=saved_metrics[3,:2].tolist(),
                         baseline_residual_addition_fraction=(direct[3,:2]/saved_metrics[3,:2]).tolist(),
                         MTS_residual_time_step_change=time_metrics[3,2:4].tolist(),
                         MTS_residual_profile_change=profile_metrics[3,2:4].tolist(),
                         MTS_temperature_mu_y_interval_addition=direct[:3,2:4].tolist(),
                         baseline_temperature_mu_y_interval_addition=direct[:3,:2].tolist(),
                         baseline_gas_interval_addition=(background.chi*fine['gas'][24:26]).tolist(),
                         MTS_gas_interval_addition=(background.chi*fine['gas'][26:28]).tolist())
                summaries.append(row)
                save(ROOT/f'comparisons/{model}-{route}-m{matching}.npz',frequency=reader.frequency,measure=reader.measure,
                     saved_potential=saved['potential'],delta_potential=delta['potential'],conditional_potential=updated['potential'],
                     saved_residual=saved['residual'],delta_residual=delta['residual'],conditional_residual=updated['residual'],
                     saved_metrics=saved_metrics,delta_metrics=direct,conditional_metrics=updated_metrics,
                     timestep_metrics=time_metrics,profile_metrics=profile_metrics,partial_MTS_allowance=budget['allowance'],
                     heat=background.chi)
    for path,value in inputs.items():
        assert digest(path)==value,path
    check(checks,'all consumed inputs unchanged',0,0,'integrity')
    for path,value in config['bookmark_hashes'].items():
        assert digest(path)==value,path
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    check(checks,'no bytecode or partial files',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial'))),0,'integrity')
    protected=BRANCH.parent.parent/'formalization-workbench'
    began=datetime.fromisoformat(config['started_utc']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=began]
    check(checks,'protected workbench recent changes',len(changed),0,'integrity')
    failed=[row for row in checks if not row['passed']]
    report=dict(stage=197,state='assessed',checks=checks,failed_checks=failed,all_checks_passed=not failed,
                summary=summaries,interval=config['interval'],covered_fraction=config['covered_fraction_of_local_span'],
                scope='Conditional local interval Duhamel contribution on original meshes; no complement or matching-state contribution',
                original_bank_changed=False,temperature_curve_changed=False,tolerances_changed=False,
                full_history_prediction_updated=False,protected_workbench_recent_modified_file_count=len(changed),
                completed_utc=datetime.now(timezone.utc).isoformat())
    write(ROOT/'results/status.json',report);write(ROOT/'inputs.json',inputs)
    write(ROOT/'progress.json',dict(state='assessed',failures=len(failed)))
    print(json.dumps(dict(checks=len(checks),failed=failed,summary=[row for row in summaries if row['route']=='cubic' and row['matching']==20])),flush=True)

if __name__=='__main__':
    assess()
