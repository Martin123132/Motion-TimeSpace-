from stage154_anchor_common import *
from assemble_terminal_sources import combine
from decimal import Decimal,localcontext


def aggregate(anchor,proof,folder,inputs,checks):
    location=ROOT/'runs'/anchor
    packet=verify_packet(location)
    assert packet['all_checks_passed'] and packet['nodes']==1260
    stored=read_npz(location/'unique-source.npz')
    theta=proof['contexts'][anchor][0]['theta']
    raw={key:np.zeros((98,4)) for key in COMPONENTS}
    terms={key:[] for key in COMPONENTS}
    rows=[0,1,2,97]
    with localcontext() as context:
        context.prec=60
        exact={key:[[Decimal(0) for column in range(4)] for row in rows] for key in COMPONENTS}
        for node in integration_nodes(theta,5):
            path=event_path(anchor,node['index'])
            saved=read_npz(path)
            assert json.loads(str(saved['identity']))==node
            parameters,weight=parameters_and_weight(theta,node)
            assert weight>0 and weight==float(saved['weight'])
            loop_path=Path(str(saved['loop_path']))
            assert loop_path.is_relative_to(ROOT/'virtual-cache')
            loop=json.loads(loop_path.read_text())
            assert loop['identity']==event_owner.inherited.virtual_identity(parameters)
            assert loop['finite'] and loop['scalar']==float(saved['loop_scalar'])
            for key in COMPONENTS:
                value=saved[key]
                assert value.shape==(98,4) and np.isfinite(value).all()
                raw[key]-=weight*value
                terms[key].append(-weight*value)
                for position,row in enumerate(rows):
                    for column in range(4):
                        exact[key][position][column]+=Decimal.from_float(-weight)*Decimal.from_float(float(value[row,column]))
            inputs.extend([path,loop_path])
        stable={}
        for key in COMPONENTS:
            assert np.array_equal(raw[key],stored[key])
            flat=np.asarray(terms[key]).reshape(1260,-1)
            result=np.asarray([math.fsum(flat[:,column]) for column in range(flat.shape[1])]).reshape(98,4)
            fsum=result.copy()
            result[rows]=[[float(value) for value in row] for row in exact[key]]
            stable[key]=result
            np.savez_compressed(folder/f'{anchor}-{key}-sums.npz',sequential=raw[key],fsum=fsum,refined=result)
    assert len(list((location/'nodes').rglob('*.npz')))==1260
    checks.append(dict(name='1260 sourced events,positive weights,owned loops and exact sums:'+anchor,passed=True))
    inputs.extend([location/'status.json',location/'unique-source.npz'])
    return raw,stable


def main():
    modest()
    folder=ROOT/'results/anchor-sources'
    folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    data=read_npz(ROOT/'results/preflight/frozen-reference.npz')
    checks,inputs=[],[ROOT/'results/preflight/status.json',ROOT/'results/preflight/frozen-reference.npz',PARENT/'FINAL-SUMMARY.json']
    mass=data['mass']
    norm=lambda value:dual_norm(value[1:-1],mass)
    cold_scale=norm(data['actual'])
    source_metrics={}
    for anchor in ANCHORS:
        raw,stable=aggregate(anchor,proof,folder,inputs,checks)
        fixed=[data[anchor+'_control'],data[anchor+'_sampled_leading']]
        full=combine([*fixed,*[stable[key] for key in COMPONENTS]],[1,-1,1,1,1])
        sequential=combine([*fixed,*[raw[key] for key in COMPONENTS]],[1,-1,1,1,1])
        original=data[anchor+'_source4']
        scale=norm(original)
        deltas=[combine([stable[key],data[anchor+'_'+key]],[1,-1]) for key in COMPONENTS]
        total=combine(deltas,[1,1,1])
        test(checks,'Stable versus raw full source:'+anchor,float(max(norm(full-sequential)/scale)),1e-10)
        test(checks,'Full source equals old plus component changes:'+anchor,float(max(norm(full-original-total)/scale)),1e-12)
        pair=abs(full[0]+full[-1])/np.maximum(abs(full[0]),1e-300)
        test(checks,'Independent photon/gas exchange:'+anchor,float(max(pair)),1e-10)
        moment=abs(data['temperature']@full[1:-1]-full[0])/np.maximum(abs(full[0]),1e-300)
        test(checks,'RAW_MOMENT:'+anchor,float(max(moment)),1e-10)
        component_norms=np.asarray([norm(value) for value in deltas])
        budget=component_norms.sum(axis=0)/scale
        for column,label in enumerate(COLUMN_NAMES):
            test(checks,'ACCURACY:'+anchor+':'+label,float(budget[column]),.01)
        source_metrics[anchor]=dict(component_relative=(component_norms/scale).tolist(),
            component_sum=budget.tolist(),coherent=(norm(total)/scale).tolist(),
            component_sum_over_coldS4=(component_norms.sum(axis=0)/cold_scale).tolist(),
            arithmetic=(norm(full-sequential)/scale).tolist(),pair=pair.tolist(),raw_moment=moment.tolist(),
            new_order=5,reference_order=4,convergence_order_known=False)
        data[anchor+'_source5']=full
        data[anchor+'_raw_source5']=sequential
        data[anchor+'_delta_total']=total
        for key,value,delta in zip(COMPONENTS,stable.values(),deltas):
            data[anchor+'_order5_'+key]=value
            data[anchor+'_delta_'+key]=delta
    cold_radius=sum(norm(data['delta6_'+key]) for key in COMPONENTS)/cold_scale
    margin=np.asarray(json.loads((PARENT/'FINAL-SUMMARY.json').read_text())['source']['routes']['cubic']['conditional_weighted_anchor_budget_to_keep_miss'])
    diagnostic={}
    for route in ['local','cubic']:
        coefficients={anchor:predictor_basis(.75,route,anchor) for anchor in ANCHORS}
        shift=combine([data[anchor+'_delta_total'] for anchor in ANCHORS],list(coefficients.values()))
        prediction=combine([data['prediction_'+route],shift],[1,1])
        error=data['source6']-prediction
        observed_radius=sum(abs(coefficients[anchor])*sum(norm(data[anchor+'_delta_'+key]) for key in COMPONENTS) for anchor in ANCHORS)/cold_scale
        before=norm(data['source6']-data['prediction_'+route])/norm(data['source6'])
        after=norm(error)/norm(data['source6'])
        cold5=norm(data['source5']-prediction)/norm(data['source5'])
        for column,label in enumerate(COLUMN_NAMES):
            test(checks,'REFRESHED_FORECAST_DIAGNOSTIC:'+route+':'+label,float(after[column]),.01)
            if route=='cubic':
                test(checks,'CONDITIONAL_ANCHOR_BUDGET:'+label,float(observed_radius[column]/margin[column]),1.)
        diagnostic[route]=dict(coefficients=coefficients,original_frozen_error=before.tolist(),
            diagnostic_refreshed_error=after.tolist(),predictor_shift_over_coldS4=(norm(shift)/cold_scale).tolist(),
            diagnostic_cold5_error=cold5.tolist(),endpoint_orders_unchanged=[4,4],
            noncancelling_anchor_budget_over_coldS4=observed_radius.tolist(),
            latest_cold_budget_over_coldS4=cold_radius.tolist(),
            remaining_allowance_from153=margin.tolist() if route=='cubic' else None,
            conditional_lower_original_interpolation=(np.maximum(norm(data['source6']-data['prediction_'+route])/cold_scale-cold_radius-observed_radius,0)/(norm(data['source6'])/cold_scale+cold_radius)).tolist(),
            only_two_anchors_tested=True,certified_continuum_radius=False,curve_adopted=False)
        data[route+'_diagnostic_prediction']=prediction
        data[route+'_predictor_shift']=shift
    numerical=all(row['passed'] for row in checks if not row['name'].startswith(('ACCURACY:','RAW_MOMENT:','REFRESHED_FORECAST_DIAGNOSTIC:','CONDITIONAL_ANCHOR_BUDGET:')))
    np.savez_compressed(folder/'source.npz',**data)
    finish(folder,dict(checks=checks,numerical_integrity_passed=numerical,source_metrics=source_metrics,
        prediction_diagnostics=diagnostic,other_quadrature_axes_refined=False,curve_adopted=False),
        __file__,[*inputs,folder/'source.npz'])
    print(json.dumps(dict(metrics=source_metrics,prediction=diagnostic,failed=[row for row in checks if not row['passed']])),flush=True)
    assert numerical


if __name__=='__main__':
    main()
