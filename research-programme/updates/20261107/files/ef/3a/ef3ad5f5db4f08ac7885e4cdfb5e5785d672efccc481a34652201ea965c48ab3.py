from precision214 import *
import collision_operator as api


def main():
    config,extension,repair=repair_protocol()
    assert read(REPAIR/'results/assessment.json')['qualified']
    destination=ROOT/'results/api-validation.json'
    assert not destination.exists()
    freeze_path=ROOT/'frozen/api-contract.json'
    assert not freeze_path.exists()
    write(freeze_path,dict(frozen_at=now(),files={name:digest(ROOT/name) for name in ('collision_operator.py','verify214_api.py')},
        fresh_event=0,unchanged_precision=60,identity_tolerance=1e-10,replay_not_holdout=True))
    original,theta=source.context(config['target_fraction'])
    bundle,models=api.evaluators(original)
    row=extension['events'][0]
    parameters,weight=source.physics.parameters_and_weight(theta,row['node'])
    assert digest(row['loop_path'])==row['loop_sha256']
    loop=read(row['loop_path'])
    previous=mp.mp.dps
    began=time.monotonic()
    matrix,diagnostics=api.evaluate_event(parameters,bundle,models,loop['scalar'],weight)
    rows=[]
    check(rows,'global precision restored after API',mp.mp.dps-previous,0,'integrity')
    for name,value in diagnostics.items():
        check(rows,'fresh event0:'+name,value,1e-10,'identity')
    stored=packet(REPAIR/'events/event-00.npz')
    error=metrics.subtract(matrix,(stored['high'],stored['low']))
    for component in range(6):
        relative=np.linalg.norm(error[0][component]+error[1][component])/max(np.linalg.norm(stored['high'][component]+stored['low'][component]),1e-300)
        check(rows,f'fresh production event0 vs repaired matrix:{component}',relative,1e-10,'identity')
    save(ROOT/'results/api-event-00.npz',high=matrix[0],low=matrix[1])
    total=packet(REPAIR/'results/operator-node.npz')
    operator=(total['high'],total['low'])
    coefficients=packet(ROOT/'frozen/history-coefficients.npz')
    expected=packet(REPAIR/'frozen/node-prediction.npz')
    expected_pair=tuple(np.moveaxis(expected[name],0,2).reshape(6,98,12) for name in ('high','low'))
    contraction_seconds=[]
    for join in range(2):
        columns=list(range(join,12,2))
        inputs=(coefficients['high'][np.ix_(ACTIVE,columns)],coefficients['low'][np.ix_(ACTIVE,columns)])
        tick=time.monotonic()
        result=api.apply_coefficients(operator,inputs,join)
        contraction_seconds.append(time.monotonic()-tick)
        for index,name in enumerate(('high','low')):
            check(rows,f'API replay {join}:{name} bitwise',int(not np.array_equal(result[index],expected_pair[index][:,:,columns])),0,'integrity')
        check(rows,f'API zero inputs {join}',np.max(abs(result[0][:,:,-2:]))+np.max(abs(result[1][:,:,-2:])),0,'negative_control')
    for label,matrix_value,coefficient_value,join,digits in (
        ('shape',operator,(np.zeros((98,1)),np.zeros((98,1))),0,80),
        ('join',operator,(np.zeros((97,1)),np.zeros((97,1))),2,80),
        ('precision',operator,(np.zeros((97,1)),np.zeros((97,1))),0,40),
        ('nonfinite',operator,(np.full((97,1),np.nan),np.zeros((97,1))),0,80)):
        rejected=False
        try:
            api.apply_coefficients(matrix_value,coefficient_value,join,digits)
        except ValueError:
            rejected=True
        check(rows,'API rejects '+label,int(not rejected),0,'negative_control')
    basis=packet(ROOT/'frozen/basis-metric.npz')
    factor=linear.cholesky(basis['mass'],lower=True)
    inverse_transpose=linear.solve_triangular(factor.T,np.eye(96),lower=False)
    operator_values=operator[0]+operator[1]
    bounds=[]
    for component,join in np.ndindex(6,2):
        values=operator_values[component,:,:,join]
        photon_to_photon=float(linear.svdvals(linear.solve_triangular(factor,values[1:97,:96]@inverse_transpose,lower=True))[0])
        gas_to_photon=float(np.linalg.norm(linear.solve_triangular(factor,values[1:97,96],lower=True)))
        photon_to_gas=float(np.linalg.norm(values[97,:96]@inverse_transpose))
        gas_to_gas=float(abs(values[97,96]))
        bounds.append(dict(component=COMPONENTS[component],join=join,photon_to_photon=photon_to_photon,
            gas_to_photon=gas_to_photon,photon_to_gas=photon_to_gas,gas_to_gas=gas_to_gas))
        for background in range(2):
            half=2*background+join;quarter=4+half
            delta=(coefficients['high'][:,half]-coefficients['high'][:,quarter])+(coefficients['low'][:,half]-coefficients['low'][:,quarter])
            norm_photon=np.linalg.norm(factor.T@delta[:96]);norm_gas=abs(delta[98])
            output=values@delta[ACTIVE]
            for name,actual,bound in (
                ('photon',np.linalg.norm(linear.solve_triangular(factor,output[1:97],lower=True)),photon_to_photon*norm_photon+gas_to_photon*norm_gas),
                ('gas',abs(output[97]),photon_to_gas*norm_photon+gas_to_gas*norm_gas)):
                check(rows,f'full-node block bound {component}:{join}:{background}:{name}',max(0,actual-bound)/max(bound,1e-300),1e-10,'bound')
    report=dict(checks=rows,failed_checks=[row for row in rows if not row['passed']],qualified=all(row['passed'] for row in rows),
        seconds=time.monotonic()-began,contraction_seconds=contraction_seconds,norm_blocks=bounds,
        numerical_norms_not_interval_enclosures=True,new_virtual_integrals=0,fresh_event=0,
        verified_api_hashes=read(freeze_path)['files'],event_matrix_sha256=digest(ROOT/'results/api-event-00.npz'))
    write(destination,report)
    print(json.dumps(dict(checks=len(rows),failed=report['failed_checks'],seconds=report['seconds'],contraction_seconds=contraction_seconds)),flush=True)


if __name__=='__main__':
    source.modest()
    main()
