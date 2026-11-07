from stage151_integration_common import *
from assemble_terminal_sources import combine
from decimal import Decimal,localcontext


def aggregate(order,proof,folder,checks,inputs):
    location=ROOT/'runs'/f'order{order}'
    packet=verify_packet(location)
    assert packet['all_checks_passed']
    stored=read_npz(location/'unique-source.npz')
    nodes=list(integration_nodes(proof['theta'],order))
    shared=proof['order5_shared_order3'] if order==5 else {}
    third=list(integration_nodes(proof['theta'],3))
    unique_sums={key:np.zeros((98,4)) for key in COMPONENTS}
    sequential={key:np.zeros((98,4)) for key in COMPONENTS}
    terms={key:[] for key in COMPONENTS}
    moment_rows=[0,1,2,97]
    with localcontext() as context:
        context.prec=60
        exact={key:[[Decimal(0) for column in range(4)] for row in moment_rows] for key in COMPONENTS}
        for node in nodes:
            reused=str(node['index']) in shared
            original=third[shared[str(node['index'])]] if reused else node
            path=event_path(3 if reused else order,original['index'])
            saved=read_npz(path)
            assert json.loads(str(saved['identity']))==original
            assert event_signature(original)==event_signature(node)
            parameters,weight=parameters_and_weight(proof['theta'],node)
            original_parameters,original_weight=parameters_and_weight(proof['theta'],original)
            assert weight>0 and float(saved['weight'])==original_weight
            assert event_owner.inherited.virtual_identity(parameters)==event_owner.inherited.virtual_identity(original_parameters)
            loop_path=Path(str(saved['loop_path']))
            assert loop_path.is_relative_to(ROOT/'virtual-cache')
            loop=json.loads(loop_path.read_text())
            assert loop['finite'] and loop['identity']==event_owner.inherited.virtual_identity(parameters)
            assert loop['scalar']==float(saved['loop_scalar'])
            for key in COMPONENTS:
                value=saved[key]
                assert value.shape==(98,4) and np.isfinite(value).all()
                contribution=-weight*value
                sequential[key]+=contribution
                if not reused:
                    unique_sums[key]+=contribution
                terms[key].append(contribution)
                for position,row in enumerate(moment_rows):
                    for column in range(4):
                        exact[key][position][column]+=Decimal.from_float(-weight)*Decimal.from_float(float(value[row,column]))
            inputs.extend([path,loop_path])
        stable={}
        for key in COMPONENTS:
            assert np.array_equal(unique_sums[key],stored[key])
            flat=np.asarray(terms[key]).reshape(len(nodes),-1)
            values=np.asarray([math.fsum(flat[:,column]) for column in range(flat.shape[1])]).reshape(98,4)
            fsum_only=values.copy()
            values[moment_rows]=[[float(item) for item in row] for row in exact[key]]
            stable[key]=values
            np.savez_compressed(folder/f'order{order}-{key}-sums.npz',
                sequential=sequential[key],fsum=fsum_only,refined=values,moment_rows=moment_rows)
    assert len(list((location/'nodes').rglob('*.npz')))==len(nodes)-len(shared)==packet['nodes']
    checks.append(dict(name='Exact new weights,shared nodes,coefficient ownership and unique sums:order'+str(order),passed=True))
    inputs.extend([location/'status.json',location/'unique-source.npz'])
    return sequential,stable


def metrics(reference,deltas,mass,chemical):
    denominator=dual_norm(reference[1:-1],mass)
    assert (denominator>0).all()
    component=np.asarray([dual_norm(delta[1:-1],mass) for delta in deltas])
    coherent=dual_norm(combine(deltas,[1,1,1])[1:-1],mass)
    result=dict(source_component_relative=(component/denominator).tolist(),
        source_component_sum=(component.sum(axis=0)/denominator).tolist(),
        source_coherent=(coherent/denominator).tolist())
    for label,selector in [('energy',lambda value:value[0]),
                           ('gas',lambda value:value[-1]),
                           ('number',lambda value:chemical@value[1:-1])]:
        denominator=abs(selector(reference))
        assert (denominator>0).all()
        moments=np.asarray([selector(delta) for delta in deltas])
        result[label]=dict(component_sum=(abs(moments).sum(axis=0)/denominator).tolist(),
            coherent=(abs(moments.sum(axis=0))/denominator).tolist(),
            signed_components=moments.tolist())
    return result


def main():
    modest()
    folder=ROOT/'results/integration-source'
    folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    assert proof['all_checks_passed']
    reference=read_npz(ROOT/'results/preflight/frozen-reference.npz')
    arrays=dict(reference)
    inputs=[ROOT/'results/preflight/status.json',ROOT/'results/preflight/frozen-reference.npz']
    checks,rows,arithmetic=[],{},{}
    mass,chemical=reference['mass'],reference['chemical']
    baseline=reference['actual']
    scale=dual_norm(baseline[1:-1],mass)
    for order in [3,5]:
        raw,stable=aggregate(order,proof,folder,checks,inputs)
        full=combine([reference['actual_control'],reference['actual_sampled_leading'],
            *[stable[key] for key in COMPONENTS]],[1,-1,1,1,1])
        raw_full=combine([reference['actual_control'],reference['actual_sampled_leading'],
            *[raw[key] for key in COMPONENTS]],[1,-1,1,1,1])
        change=dual_norm((full-raw_full)[1:-1],mass)/scale
        test(checks,'Same-event source arithmetic:order'+str(order),float(max(change)),1e-10)
        arithmetic[str(order)]=change.tolist()
        deltas=[combine([stable[key],reference['actual_'+key]],[1,-1]) for key in COMPONENTS]
        total=combine(deltas,[1,1,1])
        test(checks,'Independent full-source component difference identity:order'+str(order),
             float(max(dual_norm((full-baseline-total)[1:-1],mass)/scale)),1e-12)
        pair=abs(full[0]+full[-1])/abs(full[0])
        test(checks,'Independent full photon gas exchange:order'+str(order),float(max(pair)),1e-10)
        moment=abs(reference['temperature']@full[1:-1]-full[0])/abs(full[0])
        test(checks,'RAW_MOMENT_DIAGNOSTIC:order'+str(order),float(max(moment)),1e-10)
        arrays['source'+str(order)]=full
        arrays['raw_source'+str(order)]=raw_full
        arrays[f'delta{order}_total']=total
        for key,delta in zip(COMPONENTS,deltas):
            arrays[f'order{order}_{key}']=stable[key]
            arrays[f'delta{order}_{key}']=delta
        rows[str(order)]=metrics(baseline,deltas,mass,chemical)
        test(checks,'Triangle inequality:order'+str(order),
            max(np.asarray(rows[str(order)]['source_coherent'])-rows[str(order)]['source_component_sum']),1e-12)
        for column,label in enumerate(COLUMN_NAMES):
            test(checks,'ACCURACY:component sum:order'+str(order)+':'+label,
                 rows[str(order)]['source_component_sum'][column],.01)
    contraction={}
    for label in ['source_component_sum','source_coherent']:
        old,new=np.asarray(rows['3'][label]),np.asarray(rows['5'][label])
        ratio=new/old
        contraction[label]=ratio.tolist()
        if label=='source_component_sum':
            for column,name in enumerate(COLUMN_NAMES):
                test(checks,'CONTRACTION:total:'+name,float(ratio[column]),1.)
    old,new=np.asarray(rows['3']['source_component_relative']),np.asarray(rows['5']['source_component_relative'])
    contraction['components']=(new/old).tolist()
    for position,key in enumerate(COMPONENTS):
        for column,name in enumerate(COLUMN_NAMES):
            test(checks,'CONTRACTION:'+key+':'+name,float(new[position,column]/old[position,column]),1.)
    forecasts={}
    for order,source in [(4,baseline),(3,arrays['source3']),(5,arrays['source5'])]:
        forecasts[str(order)]={}
        for route in ['local','cubic']:
            error=dual_norm((source-reference['prediction_'+route])[1:-1],mass)/dual_norm(source[1:-1],mass)
            forecasts[str(order)][route]=error.tolist()
            for column,name in enumerate(COLUMN_NAMES):
                test(checks,'FORECAST_DIAGNOSTIC:order'+str(order)+':'+route+':'+name,float(error[column]),.01)
    numerical=all(row['passed'] for row in checks if not row['name'].startswith(
        ('ACCURACY:','CONTRACTION:','FORECAST_DIAGNOSTIC:','RAW_MOMENT_DIAGNOSTIC:')))
    np.savez_compressed(folder/'source.npz',**arrays)
    finish(folder,dict(checks=checks,metrics=rows,contraction=contraction,forecasts=forecasts,
        numerical_integrity_all_passed=numerical,source_arithmetic_change=arithmetic,
        source_quadrature_continuum_error_bounded=False,other_axes_refined=False,
        reused_control_nodes=4608,reused_order4_nodes=1008,shared_nodes=252,new_unique_events=1764,
        baseline_inner_history_refined=False),__file__,[*inputs,folder/'source.npz'])
    print(json.dumps(dict(metrics=rows,contraction=contraction,forecasts=forecasts,
        failed=[row['name'] for row in checks if not row['passed']])),flush=True)
    assert numerical


if __name__=='__main__':
    main()
