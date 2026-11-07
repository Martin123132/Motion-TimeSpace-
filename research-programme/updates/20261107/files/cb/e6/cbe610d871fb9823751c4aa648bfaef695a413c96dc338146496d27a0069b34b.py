from stage152_order6_common import *
from assemble_terminal_sources import combine
from assemble_integration import metrics
from decimal import Decimal,localcontext


def aggregate(proof,folder,checks,inputs):
    packets={part:verify_packet(ROOT/'runs'/f'part{part}') for part in [0,1]}
    assert all(packet['all_checks_passed'] for packet in packets.values())
    stored={part:read_npz(ROOT/'runs'/f'part{part}/unique-source.npz') for part in [0,1]}
    shard_sums={part:{key:np.zeros((98,4)) for key in COMPONENTS} for part in [0,1]}
    sequential={key:np.zeros((98,4)) for key in COMPONENTS}
    terms={key:[] for key in COMPONENTS}
    rows=[0,1,2,97]
    nodes=list(integration_nodes(proof['theta'],6))
    with localcontext() as context:
        context.prec=60
        exact={key:[[Decimal(0) for column in range(4)] for row in rows] for key in COMPONENTS}
        for node in nodes:
            path=event_path(node['index'])
            saved=read_npz(path)
            assert json.loads(str(saved['identity']))==node
            parameters,weight=parameters_and_weight(proof['theta'],node)
            assert weight>0 and float(saved['weight'])==weight
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
                shard_sums[node['index']%2][key]+=contribution
                terms[key].append(contribution)
                for position,row in enumerate(rows):
                    for column in range(4):
                        exact[key][position][column]+=Decimal.from_float(-weight)*Decimal.from_float(float(value[row,column]))
            inputs.extend([path,loop_path])
        stable={}
        for key in COMPONENTS:
            for part in [0,1]:
                assert np.array_equal(shard_sums[part][key],stored[part][key])
            flat=np.asarray(terms[key]).reshape(len(nodes),-1)
            values=np.asarray([math.fsum(flat[:,column]) for column in range(flat.shape[1])]).reshape(98,4)
            fsum_only=values.copy()
            values[rows]=[[float(value) for value in row] for row in exact[key]]
            stable[key]=values
            np.savez_compressed(folder/(key+'-sums.npz'),sequential=sequential[key],fsum=fsum_only,refined=values,moment_rows=rows)
    for part in [0,1]:
        location=ROOT/'runs'/f'part{part}'
        assert len(list((location/'nodes').rglob('*.npz')))==756==packets[part]['nodes']
        inputs.extend([location/'status.json',location/'unique-source.npz'])
    checks.append(dict(name='1512 exact nodes,positive weights,loop ownership and shard sums',passed=True))
    return sequential,stable


def main():
    modest()
    folder=ROOT/'results/integration-source'
    folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    reference=read_npz(ROOT/'results/preflight/frozen-reference.npz')
    assert proof['all_checks_passed']
    checks,inputs=[],[ROOT/'results/preflight/status.json',ROOT/'results/preflight/frozen-reference.npz',
        PARENT/'results/integration-source/status.json']
    raw,stable=aggregate(proof,folder,checks,inputs)
    arrays=dict(reference)
    mass,chemical=reference['mass'],reference['chemical']
    scale=dual_norm(reference['actual'][1:-1],mass)
    full=combine([reference['actual_control'],reference['actual_sampled_leading'],
        *[stable[key] for key in COMPONENTS]],[1,-1,1,1,1])
    raw_full=combine([reference['actual_control'],reference['actual_sampled_leading'],
        *[raw[key] for key in COMPONENTS]],[1,-1,1,1,1])
    change=dual_norm((full-raw_full)[1:-1],mass)/scale
    test(checks,'Same-event source arithmetic:order6',float(max(change)),1e-10)
    deltas=[combine([stable[key],reference['order5_'+key]],[1,-1]) for key in COMPONENTS]
    total=combine(deltas,[1,1,1])
    test(checks,'S6-S5 equals sum of component differences',
         float(max(dual_norm((full-reference['source5']-total)[1:-1],mass)/scale)),1e-12)
    test(checks,'S6-S4 equals delta54+delta65',
         float(max(dual_norm((full-reference['actual']-reference['delta5_total']-total)[1:-1],mass)/scale)),1e-12)
    pair=abs(full[0]+full[-1])/abs(full[0])
    test(checks,'Independent full photon/gas exchange',float(max(pair)),1e-10)
    moment=abs(reference['temperature']@full[1:-1]-full[0])/abs(full[0])
    test(checks,'RAW_MOMENT_DIAGNOSTIC:order6',float(max(moment)),1e-10)
    arrays.update(source6=full,raw_source6=raw_full,delta6_total=total)
    for key,delta in zip(COMPONENTS,deltas):
        arrays['order6_'+key]=stable[key]
        arrays['delta6_'+key]=delta
    previous=metrics(reference['actual'],[reference['delta5_'+key] for key in COMPONENTS],mass,chemical)
    parent=verify_packet(PARENT/'results/integration-source')
    assert previous==parent['metrics']['5']
    current=metrics(reference['actual'],deltas,mass,chemical)
    test(checks,'Source triangle inequality',
         max(np.asarray(current['source_coherent'])-current['source_component_sum']),1e-12)
    contraction={}
    for name in ['source_component_sum','source_coherent']:
        ratio=np.asarray(current[name])/previous[name]
        contraction[name]=ratio.tolist()
        if name=='source_component_sum':
            for column,label in enumerate(COLUMN_NAMES):
                test(checks,'ACCURACY:delta65 component sum:'+label,current[name][column],.01)
                test(checks,'CONTRACTION:total:'+label,float(ratio[column]),1.)
    component_ratio=np.asarray(current['source_component_relative'])/previous['source_component_relative']
    contraction['components']=component_ratio.tolist()
    for position,key in enumerate(COMPONENTS):
        for column,label in enumerate(COLUMN_NAMES):
            test(checks,'CONTRACTION:'+key+':'+label,float(component_ratio[position,column]),1.)
    forecasts={}
    for route in ['local','cubic']:
        error=dual_norm((full-reference['prediction_'+route])[1:-1],mass)/dual_norm(full[1:-1],mass)
        forecasts[route]=error.tolist()
        for column,label in enumerate(COLUMN_NAMES):
            test(checks,'FORECAST_DIAGNOSTIC:order6:'+route+':'+label,float(error[column]),.01)
    numerical=all(row['passed'] for row in checks if not row['name'].startswith(
        ('ACCURACY:','CONTRACTION:','FORECAST_DIAGNOSTIC:','RAW_MOMENT_DIAGNOSTIC:')))
    np.savez_compressed(folder/'source.npz',**arrays)
    finish(folder,dict(checks=checks,metrics={'5':previous,'6':current},contraction=contraction,
        forecasts={'6':forecasts},prior_forecasts=parent['forecasts'],
        numerical_integrity_all_passed=numerical,source_arithmetic_change=change.tolist(),
        source_photon_gas_pair=pair.tolist(),unprojected_moment=moment.tolist(),
        source_quadrature_continuum_error_bounded=False,other_axes_refined=False,
        reused_control_nodes=4608,reused_orders=[3,4,5],new_unique_events=1512,
        baseline_inner_history_refined=False),__file__,[*inputs,folder/'source.npz'])
    print(json.dumps(dict(metrics=current,contraction=contraction,forecasts=forecasts,
        failed=[row['name'] for row in checks if not row['passed']])),flush=True)
    assert numerical


if __name__=='__main__':
    main()
