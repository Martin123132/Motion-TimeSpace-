from test216 import *


def analysis_contract():
    assert not (ROOT/'frozen/analysis-contract.json').exists()
    write(ROOT/'frozen/analysis-contract.json',dict(frozen_at=now(),sha256=digest(Path(__file__)),
        identity_tolerance=1e-10,source_prediction_tolerance=.01,operator_block_tolerance=.01,history_mesh_tolerance=.01,
        new_physical_histories=True,baseline_and_mts_same_gates=True))
    print('Analysis contract frozen.',flush=True)


def assess():
    config=protocol()
    assert read(ROOT/'frozen/analysis-contract.json')['sha256']==digest(Path(__file__))
    assert not (ROOT/'results/assessment.json').exists()
    manifest=read(ROOT/'frozen/prediction-manifest.json')
    assert manifest['configuration_sha256']==digest(ROOT/'configuration.json')
    basis=packet(ROOT/'frozen/basis-metric.npz')
    factor=linear.cholesky(basis['mass'],lower=True)
    inverse_transpose=linear.solve_triangular(factor.T,np.eye(96),lower=False)
    coefficients=packet(ROOT/'frozen/history-coefficients.npz')
    checks=list(read(ROOT/'results/preparation.json')['checks'])
    replays=[];matrices=[];directs=[];predictions=[];new_loops=0
    for row in config['events']:
        report=verify_completed(row)
        assert datetime.fromisoformat(report['started_at'])>datetime.fromisoformat(manifest['frozen_at'])
        assert datetime.fromisoformat(report['replay_frozen_before_direct'])<datetime.fromisoformat(report['finished_at'])
        checks.extend(dict(entry,name=f"event{row['event']}:"+entry['name']) for entry in report['checks'])
        operator=packet(ROOT/report['operator_path'])
        direct=packet(ROOT/report['direct_path'])
        prediction=packet(ROOT/report['prediction_path'])
        assert float(operator['theta'])==float(direct['theta'])==config['theta']
        assert float(operator['weight'])==float(direct['weight'])==row['weight']
        matrix=(operator['high'],operator['low'])
        actual=(direct['high'],direct['low'])
        predicted=(prediction['high'],prediction['low'])
        matrices.append(matrix);directs.append(actual);predictions.append(predicted)
        helpers.compare(f"event-{row['event']}",predicted,actual,factor,checks,replays)
        new_loops+=int(report['new_virtual_integral'])
    target=api.sum_events(matrices)
    actual=metrics.primitives(directs)
    target_contraction=contract_histories(target,coefficients)
    summed_contraction=metrics.primitives(predictions)
    helpers.compare('full-node replay',target_contraction,actual,factor,checks,replays)
    helpers.compare('contract before/after sum',target_contraction,summed_contraction,factor,checks,replays)
    save(ROOT/'results/operator-target.npz',high=target[0],low=target[1],theta=config['theta'],frequency=config['frequency'])
    save(ROOT/'results/direct-source.npz',high=actual[0],low=actual[1])
    save(ROOT/'results/operator-source.npz',high=target_contraction[0],low=target_contraction[1])
    predicted_operator=packet(ROOT/'frozen/predicted-operator.npz')
    predicted_values=(predicted_operator['high'],predicted_operator['low'])
    predicted_source=packet(ROOT/'frozen/predicted-source.npz')
    predicted=(predicted_source['high'],predicted_source['low'])
    error=metrics.subtract(predicted_values,target)
    error_source=contract_histories(error,coefficients)
    helpers.compare('operator-error contraction',error_source,metrics.subtract(predicted,target_contraction),factor,checks,replays)
    save(ROOT/'results/operator-error.npz',high=error[0],low=error[1])
    identities={}
    for label,matrix in [('target',dict(high=target[0],low=target[1])),('prediction',predicted_operator)]:
        local=[]
        identities[label]=helpers.matrix_identities(matrix,basis,local)
        checks.extend(dict(entry,name=label+':'+entry['name']) for entry in local)
    source_error=metrics.subtract(predicted,actual)
    physical=[];mesh=[]
    for name,measure in [('photon',lambda values:metrics.norms(values,factor)),('gas',lambda values:abs(values[...,-1,:]))]:
        relative=measure(source_error[0][:2]+source_error[1][:2])/np.maximum(measure(actual[0][:2]+actual[1][:2]),1e-300)
        for grid,component,column in np.ndindex(relative.shape):
            value=float(relative[grid,component,column])
            physical.append(dict(grid=('half','quarter')[grid],component=COMPONENTS[component],background=('heavy','cold')[column//2],join=column%2,measure=name,relative=value))
            check(checks,f'physical forecast:{grid}:{component}:{column}:{name}',value,.01,'physical_prediction')
        for label,pair in [('actual',actual),('predicted',predicted)]:
            delta=metrics.subtract((pair[0][0],pair[1][0]),(pair[0][1],pair[1][1]))
            relative=measure(delta[0]+delta[1])/np.maximum(measure(pair[0][1]+pair[1][1]),1e-300)
            for component,column in np.ndindex(relative.shape):
                value=float(relative[component,column])
                mesh.append(dict(source=label,component=COMPONENTS[component],background=('heavy','cold')[column//2],join=column%2,measure=name,relative=value))
                check(checks,f'{label} source mesh:{component}:{column}:{name}',value,.01,'mesh')
    error_values=error[0]+error[1];target_values=target[0]+target[1]
    blocks=[];bounds=[]
    for component,join in np.ndindex(6,2):
        absolute=previous_assessment.block_norms(error_values[component,:,:,join],factor,inverse_transpose)
        reference=previous_assessment.block_norms(target_values[component,:,:,join],factor,inverse_transpose)
        for name in absolute:
            ratio=absolute[name]/reference[name] if reference[name]>0 else None
            passed=ratio<=.01 if ratio is not None else absolute[name]==0
            blocks.append(dict(component=COMPONENTS[component],join=join,block=name,error_norm=absolute[name],
                reference_norm=reference[name],relative=ratio,passed=bool(passed),numerical_norm_not_interval_enclosure=True))
            check(checks,f'operator block:{component}:{join}:{name}',ratio if ratio is not None else int(not passed),.01 if ratio is not None else 0,'operator_prediction')
        for grid,background in np.ndindex(2,2):
            column=4*grid+2*background+join
            delta=coefficients['high'][:,column]+coefficients['low'][:,column]
            photon_norm=float(np.linalg.norm(factor.T@delta[:96]));gas_norm=float(abs(delta[98]))
            raw=error_source[0][grid,component,:,2*background+join]+error_source[1][grid,component,:,2*background+join]
            for name,measured,bound in (
                ('photon',float(np.linalg.norm(linear.solve_triangular(factor,raw[1:97],lower=True))),
                    absolute['photon_to_photon']*photon_norm+absolute['gas_to_photon']*gas_norm),
                ('gas',float(abs(raw[97])),absolute['photon_to_gas']*photon_norm+absolute['gas_to_gas']*gas_norm)):
                violation=max(0.,measured-bound)/max(bound,1e-300)
                check(checks,f'error bound:{component}:{join}:{grid}:{background}:{name}',violation,1e-10,'bound')
                bounds.append(dict(component=COMPONENTS[component],join=join,grid=('half','quarter')[grid],
                    background=('heavy','cold')[background],measure=name,measured=measured,bound=bound,
                    overestimate=bound/measured if measured>0 else None))
    failed=[row for row in checks if not row['passed']]
    integrity=all(row['passed'] for row in checks if row['category'] not in ('physical_prediction','operator_prediction','mesh'))
    report=dict(stage=216,checks=checks,failed_checks=failed,replays=replays,physical_records=physical,mesh_records=mesh,
        operator_blocks=blocks,error_bounds=bounds,column_identities=identities,integrity_passed=integrity,
        physical_history_prediction_passed=all(row['passed'] for row in checks if row['category']=='physical_prediction'),
        operator_block_prediction_passed=all(row['passed'] for row in checks if row['category']=='operator_prediction'),
        history_mesh_passed=all(row['passed'] for row in checks if row['category']=='mesh'),qualified=not failed,
        new_virtual_integrals=new_loops,events=36,uniform_temperature_qualified=False,permission_to_propagate=False,
        original_bank_changed=False,grids_changed=False,tolerances_changed=False)
    write(ROOT/'results/assessment.json',report)
    write(ROOT/'progress.json',dict(state='assessed',qualified=report['qualified'],events_complete=36,active_workers=0))
    print(json.dumps(dict(checks=len(checks),failed=len(failed),qualified=report['qualified'],
        physical={name:max(row['relative'] for row in physical if row['component']==name) for name in COMPONENTS},
        operator={name:max(row['relative'] for row in blocks if row['component']==name and row['relative'] is not None) for name in COMPONENTS},
        new_virtual_integrals=new_loops)),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['contract','assess'])
    args=parser.parse_args()
    {'contract':analysis_contract,'assess':assess}[args.phase]()
