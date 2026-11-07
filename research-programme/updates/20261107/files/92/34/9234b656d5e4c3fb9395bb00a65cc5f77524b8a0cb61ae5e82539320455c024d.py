from bridge215 import *


def prepare_analysis():
    assert not (ROOT/'frozen/analysis-contract.json').exists()
    write(ROOT/'frozen/analysis-contract.json',dict(frozen_at=now(),sha256=digest(Path(__file__)),
          representation_tolerance=1e-10,physical_prediction_tolerance=.01,operator_block_tolerance=.01,
          baseline_and_mts_same_gates=True,replay_not_new_holdout=True))
    print('Analysis contract frozen.',flush=True)


def block_norms(values,factor,inverse_transpose):
    return dict(
        photon_to_photon=float(linear.svdvals(linear.solve_triangular(factor,values[1:97,:96]@inverse_transpose,lower=True))[0]),
        gas_to_photon=float(np.linalg.norm(linear.solve_triangular(factor,values[1:97,96],lower=True))),
        photon_to_gas=float(np.linalg.norm(values[97,:96]@inverse_transpose)),
        gas_to_gas=float(abs(values[97,96])))


def assess():
    config=protocol()
    analysis=read(ROOT/'frozen/analysis-contract.json')
    assert digest(Path(__file__))==analysis['sha256']
    assert not (ROOT/'results/assessment.json').exists()
    manifest=read(ROOT/'frozen/prediction-manifest.json')
    assert manifest['configuration_sha256']==digest(ROOT/'configuration.json')
    for name,value in manifest['files'].items():
        assert digest(ROOT/name)==value,name
    assert digest(config['target_operator_path'])==config['target_operator_sha256']
    assert digest(config['target_source_path'])==config['target_source_sha256']
    basis=packet(ROOT/'frozen/basis-metric.npz')
    factor=linear.cholesky(basis['mass'],lower=True)
    inverse_transpose=linear.solve_triangular(factor.T,np.eye(96),lower=False)
    coefficients=packet(ROOT/'frozen/history-coefficients.npz')
    checks=[];replays=[];column_identities={}
    for label in LABELS:
        actuals=[]
        for row in [row for row in config['events'] if row['label']==label]:
            values,report=verify_event(row)
            checks.extend(dict(entry,name=f"{label}:{row['event']}:"+entry['name']) for entry in report['checks'])
            assert datetime.fromisoformat(report['finished_at'])<datetime.fromisoformat(manifest['frozen_at'])
            assert digest(row['source_path'])==row['source_sha256']
            direct=packet(row['source_path'])
            assert float(direct['theta'])==row['theta'] and float(direct['weight'])==row['weight']
            actual=(direct['high'],direct['low'])
            actuals.append(actual)
            prediction=packet(ROOT/f"frozen/replay/{label}/event-{row['event']:02d}.npz")
            helpers.compare(f"{label}:event-{row['event']}",(prediction['high'],prediction['low']),actual,factor,checks,replays)
        summed=metrics.primitives(actuals)
        prediction=packet(ROOT/f'frozen/source-{label}.npz')
        helpers.compare(label+':aggregate',(prediction['high'],prediction['low']),summed,factor,checks,replays)
        local=[]
        column_identities[label]=helpers.matrix_identities(packet(ROOT/f'results/operator-{label}.npz'),basis,local)
        checks.extend(dict(entry,name=label+':'+entry['name']) for entry in local)
    target_values=packet(config['target_operator_path'])
    target=(target_values['high'],target_values['low'])
    target_contraction=contract_histories(target,coefficients)
    old=packet(config['target_source_path'])
    helpers.compare('target operator replay',target_contraction,(old['actual_high'],old['actual_low']),factor,checks,replays)
    predicted=packet(ROOT/'frozen/predicted-source.npz')
    predicted_source=(predicted['high'],predicted['low'])
    helpers.compare('original source forecast replay',predicted_source,(old['predicted_high'],old['predicted_low']),factor,checks,replays)
    prediction_values=packet(ROOT/'frozen/predicted-operator.npz')
    operator_prediction=(prediction_values['high'],prediction_values['low'])
    error=metrics.subtract(operator_prediction,target)
    save(ROOT/'results/operator-error.npz',high=error[0],low=error[1])
    error_contraction=contract_histories(error,coefficients)
    source_error=metrics.subtract(predicted_source,target_contraction)
    helpers.compare('operator-error contraction identity',error_contraction,source_error,factor,checks,replays)
    local=[]
    column_identities['predicted']=helpers.matrix_identities(prediction_values,basis,local)
    checks.extend(dict(entry,name='predicted:'+entry['name']) for entry in local)
    physical=[]
    original_source_error=metrics.subtract(predicted_source,(old['actual_high'],old['actual_low']))
    for name,measure in [('photon',lambda values:metrics.norms(values,factor)),('gas',lambda values:abs(values[...,-1,:]))]:
        relative=measure(original_source_error[0][:2]+original_source_error[1][:2])/np.maximum(measure(old['actual_high'][:2]+old['actual_low'][:2]),1e-300)
        for grid,component,column in np.ndindex(relative.shape):
            value=float(relative[grid,component,column])
            physical.append(dict(grid=('half','quarter')[grid],component=COMPONENTS[component],
                background=('heavy','cold')[column//2],join=column%2,measure=name,relative=value))
            check(checks,f'physical prediction:{grid}:{component}:{column}:{name}',value,.01,'physical_prediction')
    error_values=error[0]+error[1]
    target_array=target[0]+target[1]
    blocks=[];bounds=[]
    for component,join in np.ndindex(6,2):
        absolute=block_norms(error_values[component,:,:,join],factor,inverse_transpose)
        reference=block_norms(target_array[component,:,:,join],factor,inverse_transpose)
        for name in absolute:
            ratio=absolute[name]/reference[name] if reference[name]>0 else None
            passed=ratio<=.01 if ratio is not None else absolute[name]==0
            blocks.append(dict(component=COMPONENTS[component],join=join,block=name,error_norm=absolute[name],
                reference_norm=reference[name],relative=ratio,passed=bool(passed),
                numerical_norm_not_interval_enclosure=True))
            check(checks,f'operator block:{component}:{join}:{name}',ratio if ratio is not None else int(not passed),
                  .01 if ratio is not None else 0,'operator_prediction')
        for grid,background in np.ndindex(2,2):
            column=4*grid+2*background+join
            delta=coefficients['high'][:,column]+coefficients['low'][:,column]
            photon_norm=float(np.linalg.norm(factor.T@delta[:96]))
            gas_norm=float(abs(delta[98]))
            raw=error_contraction[0][grid,component,:,2*background+join]+error_contraction[1][grid,component,:,2*background+join]
            for name,actual,bound in (
                ('photon',float(np.linalg.norm(linear.solve_triangular(factor,raw[1:97],lower=True))),
                 absolute['photon_to_photon']*photon_norm+absolute['gas_to_photon']*gas_norm),
                ('gas',float(abs(raw[97])),absolute['photon_to_gas']*photon_norm+absolute['gas_to_gas']*gas_norm)):
                violation=max(0.,actual-bound)/max(bound,1e-300)
                check(checks,f'error bound:{component}:{join}:{grid}:{background}:{name}',violation,1e-10,'bound')
                bounds.append(dict(component=COMPONENTS[component],join=join,grid=('half','quarter')[grid],
                   background=('heavy','cold')[background],measure=name,actual=actual,bound=bound,
                   overestimate=bound/actual if actual>0 else None))
    failed=[entry for entry in checks if not entry['passed']]
    integrity=all(entry['passed'] for entry in checks if entry['category'] not in ('physical_prediction','operator_prediction'))
    physical_pass=all(entry['passed'] for entry in checks if entry['category']=='physical_prediction')
    operator_pass=all(entry['passed'] for entry in checks if entry['category']=='operator_prediction')
    report=dict(stage=215,checks=checks,failed_checks=failed,replays=replays,physical_records=physical,
        operator_blocks=blocks,error_bounds=bounds,column_identities=column_identities,
        integrity_passed=integrity,physical_history_prediction_passed=physical_pass,
        operator_block_prediction_passed=operator_pass,qualified=integrity and physical_pass and operator_pass,
        new_virtual_integrals=0,events=108,uniform_temperature_qualified=False,permission_to_propagate=False,
        original_bank_changed=False,grids_changed=False,tolerances_changed=False)
    write(ROOT/'results/assessment.json',report)
    write(ROOT/'progress.json',dict(state='assessed',integrity_passed=integrity,
        physical_history_prediction_passed=physical_pass,operator_block_prediction_passed=operator_pass))
    print(json.dumps(dict(checks=len(checks),failed=len(failed),integrity_passed=integrity,
        physical_history_prediction_passed=physical_pass,operator_block_prediction_passed=operator_pass,
        physical_maxima={name:max(row['relative'] for row in physical if row['component']==name) for name in COMPONENTS},
        operator_maxima={name:max(row['relative'] for row in blocks if row['component']==name and row['relative'] is not None) for name in COMPONENTS})),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['contract','assess'])
    args=parser.parse_args()
    {'contract':prepare_analysis,'assess':assess}[args.phase]()
