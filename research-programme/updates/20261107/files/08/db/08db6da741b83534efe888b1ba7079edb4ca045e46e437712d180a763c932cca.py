from response221 import *

CANDIDATE=ROOT/'causal-startup'


def candidate_protocol():
    protocol()
    frozen=read(CANDIDATE/'configuration.json')
    assert digest(ROOT/'causal_startup221.py')==frozen['script_sha256']
    assert digest(ROOT/'CAUSAL-STARTUP-DERIVATION.md')==frozen['derivation_sha256']
    assert digest(ROOT/'results/assessment.json')==frozen['original_assessment_sha256']
    return frozen


def prepare():
    protocol();path=CANDIDATE/'configuration.json';assert not path.exists()
    write(path,dict(frozen_at=now(),script_sha256=digest(ROOT/'causal_startup221.py'),
        derivation_sha256=digest(ROOT/'CAUSAL-STARTUP-DERIVATION.md'),
        original_assessment_sha256=digest(ROOT/'results/assessment.json'),
        method='one derived trapezoidal right-hand startup for the interval increment, then unchanged BDF2',
        source_support=[START,STOP],response_counts=[2048,4096],identity_tolerance=1e-10,comparison_tolerance=.01,
        original_runs_retained=True,global_bank_unchanged=True,grids_unchanged=True,
        physical_matching_adopted=False,source_only_closure=False))
    rows=[]
    for count in (32,64):
        current=0.;older=0.
        for index in range(1,count+1):
            updated=(2*current-.5*older+1.)/1.5
            older,current=current,updated
        exact=count-.5+.5*3.**(-count)
        check(rows,f'constant-source zero-past BDF2 law N{count}',current-exact,1e-10,'identity')
        current=1.;older=0.
        for index in range(2,count+1):
            updated=(2*current-.5*older+1.)/1.5
            older,current=current,updated
        check(rows,f'constant-source right-hand-start law N{count}',current-count,1e-10,'identity')
    write(CANDIDATE/'startup-algebra.json',dict(checks=rows,failed_checks=[row for row in rows if not row['passed']],
        original_coarse_fine_constant_source_difference=1/127))
    print('Causal-startup candidate frozen before left endpoint or response calculation.',flush=True)


def left_source(model):
    config=candidate_protocol();folder=CANDIDATE/f'left/{model}'
    if (folder/'result.json').exists():
        report=read(folder/'result.json')
        assert digest(folder/'source.npz')==report['source_sha256'] and not report['failed_checks']
        return packet(folder/'source.npz')
    inputs=read(ROOT/'inputs.json');rows=[]
    coefficients,theta,fraction=coefficients_at(model,FIRST,inputs,rows)
    parent_config=read(PARENT/'configuration.json')
    anchors=[packet(PARENT/f'results/operator-panel-{label}.npz') for label in panel.LABELS]
    pairs=[(values['high'],values['low']) for values in anchors]
    nodes=parent_config['anchor_offsets'];offset=(.875-fraction)*math.log(10)
    quadratic=history.weights(offset,nodes);secant=history.weights(offset,[nodes[0],nodes[2]])
    weights=[quadratic,[secant[0],0.,secant[1]]]
    high=np.zeros((2,3,6,98,2));low=high.copy()
    for profile,values in enumerate(weights):
        matrix=panel.weighted_matrix(pairs,values)
        for join in (0,1):
            result=api.apply_coefficients(matrix,coefficients,join,80)
            high[profile,...,join]=np.moveaxis(result[0],2,0)
            low[profile,...,join]=np.moveaxis(result[1],2,0)
    check(rows,'left endpoint exactly on original grid',fraction-START,0,'integrity')
    check(rows,'zero history',np.max(abs(high[:,2]))+np.max(abs(low[:,2])),0,'identity')
    save(folder/'source.npz',high=high,low=low,theta=theta,fraction=fraction)
    save(folder/'coefficients.npz',high=coefficients[0],low=coefficients[1])
    write(folder/'result.json',dict(checks=rows,failed_checks=[row for row in rows if not row['passed']],
        source_sha256=digest(folder/'source.npz'),coefficients_sha256=digest(folder/'coefficients.npz'),
        weights=weights,finished_at=now(),inputs=inputs))
    assert all(row['passed'] for row in rows)
    return packet(folder/'source.npz')


def evolve_candidate(model,count):
    candidate_protocol();folder=CANDIDATE/f'responses/{model}-{count}'
    assert not (folder/'result.json').exists()
    left=left_source(model);inputs=read(ROOT/'inputs.json')
    system=matched.System(model,count,inputs)
    start=round((START-.75)*count/.25);stop=round((STOP-.75)*count/.25)
    current=np.zeros((100,2*WIDTH));previous=current.copy();rows=[]
    maximum=dict(photon=0.,gas=0.,spectral=0.)
    for index in range(start+1,stop+1):
        step=system.make_step(index)
        right=verify_point(model,index*(FINE//count))[0]
        if index==start+1:
            local0=system.background.at(START*system.background.end)
            rate0=local0['coefficient']/local0['thermal_parameter']
            combined=history.combine([(right['high'],right['low']),history.scaled((left['high'],left['low']),rate0/step['rate'])])
            supplied_values=dict(high=combined[0],low=combined[1])
            step=dict(step,alpha=2/system.step,restart=True)
            matrix=step['alpha']*system.coordinates.mass-step['rate']*system.coordinates.tests@step['stiffness']@system.coordinates.transform
            step['factor']=linear.lu_factor(matrix)
            step['gas_response']=linear.lu_solve(step['factor'],step['coupling'])
            step['denominator']=step['heat']*(step['alpha']+1)+step['alpha']*step['gas_response'][0]
            assert np.isfinite(step['denominator']) and step['denominator']>0
        else:
            supplied_values=right
        supplied=pair_source(supplied_values,system,rows,f'step{index}')
        updated,diagnostic=system.advance(current,previous,step,supplied,True)
        previous,current=current,updated
        for name,value in diagnostic.items():
            maximum[name]=max(maximum[name],value)
        ledger_checks(f'step{index}',current,system,rows)
        values=matched.collapsed(current).reshape(100,2,3,6,2)
        check(rows,f'step{index}:zero history',np.max(abs(values[:,:,2])),0,'identity')
        if index in (start+1,start+(stop-start)//2,stop):
            save(folder/f'step-{index}.npz',current=current,previous=previous,index=index,fraction=step['fraction'])
    for field,limit in read(ROOT/'configuration.json')['unchanged_response_gates'].items():
        check(rows,'response equation:'+field,maximum[field],limit,'equation')
    reader=matched.saved.response.ShapeReadout(system.basis,canonical=True)
    values=matched.collapsed(current)
    shapes=reader.apply(system.coordinates.transform@values[:96],values[0])
    save(folder/'increment-readout.npz',**shapes,frequency=reader.frequency,measure=reader.measure,
         gas=values[96],work=values[97],number=values[98],injection=values[99],heat=system.background.chi)
    failed=[row for row in rows if not row['passed']]
    write(folder/'result.json',dict(model=model,count=count,checks=rows,failed_checks=failed,qualified=not failed,
        maximum=maximum,finished_at=now(),file_hashes={path.name:digest(path) for path in folder.glob('*.npz')},inputs=inputs))
    print(json.dumps(dict(model=model,count=count,checks=len(rows),failed=len(failed),maximum=maximum)),flush=True)


def assess_candidate():
    candidate_protocol();rows=list(read(CANDIDATE/'startup-algebra.json')['checks']);records=[]
    for model in MODELS:
        left=read(CANDIDATE/f'left/{model}/result.json')
        rows.extend(dict(row,name=model+':left:'+row['name']) for row in left['checks'])
        for count in (2048,4096):
            folder=CANDIDATE/f'responses/{model}-{count}';report=read(folder/'result.json')
            for name,value in report['file_hashes'].items():
                assert digest(folder/name)==value,name
            rows.extend(dict(row,name=f'{model}:{count}:'+row['name']) for row in report['checks'])
        coarse=packet(CANDIDATE/f'responses/{model}-2048/increment-readout.npz')
        fine=packet(CANDIDATE/f'responses/{model}-4096/increment-readout.npz')
        for component in (0,4,5):
            for profile in (0,1):
                columns=[np.ravel_multi_index((profile,1,component,join),(2,3,6,2)) for join in (0,1)]
                half=[np.ravel_multi_index((profile,0,component,join),(2,3,6,2)) for join in (0,1)]
                compare_readouts('causal_response_step:'+PROFILES[profile],coarse,fine,columns,columns,rows,records,model,COMPONENTS[component])
                compare_readouts('causal_history_step:'+PROFILES[profile],fine,fine,half,columns,rows,records,model,COMPONENTS[component])
            quadratic=[np.ravel_multi_index((0,1,component,join),(2,3,6,2)) for join in (0,1)]
            secant=[np.ravel_multi_index((1,1,component,join),(2,3,6,2)) for join in (0,1)]
            compare_readouts('causal_operator_sensitivity',fine,fine,secant,quadratic,rows,records,model,COMPONENTS[component])
    failed=[row for row in rows if not row['passed']]
    write(CANDIDATE/'assessment.json',dict(checks=rows,failed_checks=failed,records=records,
        qualified=not failed,original_frozen_runs_preserved=True,matching_not_replaced=True))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),
        maxima={scope:max(row['relative'] for row in records if row['scope']==scope) for scope in sorted({row['scope'] for row in records})})),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','left','run','assess'])
    parser.add_argument('--model',choices=MODELS)
    parser.add_argument('--count',type=int,choices=[2048,4096])
    args=parser.parse_args()
    if args.phase=='left':
        left_source(args.model)
    elif args.phase=='run':
        evolve_candidate(args.model,args.count)
    else:
        {'prepare':prepare,'assess':assess_candidate}[args.phase]()
