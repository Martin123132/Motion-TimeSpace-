from stage155_anchor_common import *
from assemble_terminal_sources import combine
from decimal import Decimal,localcontext


def aggregate(anchor,proof,folder,inputs,checks):
    location=ROOT/'runs'/anchor
    packet=verify_packet(location)
    assert packet['all_checks_passed'] and packet['nodes']==1512
    stored=read_npz(location/'unique-source.npz')
    theta=proof['contexts'][anchor][0]['theta']
    raw={key:np.zeros((98,4)) for key in COMPONENTS}
    terms={key:[] for key in COMPONENTS}
    rows=[0,1,2,97]
    with localcontext() as context:
        context.prec=60
        exact={key:[[Decimal(0) for column in range(4)] for row in rows] for key in COMPONENTS}
        for node in integration_nodes(theta,6):
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
            flat=np.asarray(terms[key]).reshape(1512,-1)
            result=np.asarray([math.fsum(flat[:,column]) for column in range(flat.shape[1])]).reshape(98,4)
            fsum=result.copy()
            result[rows]=[[float(value) for value in row] for row in exact[key]]
            stable[key]=result
            np.savez_compressed(folder/f'{anchor}-{key}-sums.npz',sequential=raw[key],fsum=fsum,refined=result)
    assert len(list((location/'nodes').rglob('*.npz')))==1512
    checks.append(dict(name='1512 sourced events,positive weights,owned loops and exact sums:'+anchor,passed=True))
    inputs.extend([location/'status.json',location/'unique-source.npz'])
    return raw,stable


def main():
    modest()
    folder=ROOT/'results/anchor-sources'
    folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    data=read_npz(ROOT/'results/preflight/frozen-reference.npz')
    parent_report=verify_packet(PARENT/'results/anchor-sources')
    allowance_path=stage154_parent.PARENT/'FINAL-SUMMARY.json'
    checks,inputs=[],[ROOT/'results/preflight/status.json',ROOT/'results/preflight/frozen-reference.npz',
        PARENT/'results/anchor-sources/status.json',allowance_path]
    mass=data['mass']
    norm=lambda value:dual_norm(value[1:-1],mass)
    cold_scale=norm(data['actual'])
    source_metrics={}
    for anchor in ANCHORS:
        raw,stable=aggregate(anchor,proof,folder,inputs,checks)
        fixed=[data[anchor+'_control'],data[anchor+'_sampled_leading']]
        full=combine([*fixed,*[stable[key] for key in COMPONENTS]],[1,-1,1,1,1])
        sequential=combine([*fixed,*[raw[key] for key in COMPONENTS]],[1,-1,1,1,1])
        original=data[anchor+'_source5']
        scale=norm(data[anchor+'_source4'])
        deltas=[combine([stable[key],data[anchor+'_order5_'+key]],[1,-1]) for key in COMPONENTS]
        total=combine(deltas,[1,1,1])
        previous_parts=[data[anchor+'_delta_'+key] for key in COMPONENTS]
        previous_norms=np.asarray([norm(value) for value in previous_parts])
        previous_budget=previous_norms.sum(axis=0)/scale
        close(checks,'Exact same-denominator previous anchor budget:'+anchor,previous_budget,
            parent_report['source_metrics'][anchor]['component_sum'],1e-12)
        test(checks,'Stable versus raw full source:'+anchor,float(max(norm(full-sequential)/scale)),1e-10)
        test(checks,'Full source equals order5 plus component changes:'+anchor,float(max(norm(full-original-total)/scale)),1e-12)
        pair=abs(full[0]+full[-1])/np.maximum(abs(full[0]),1e-300)
        test(checks,'Independent photon/gas exchange:'+anchor,float(max(pair)),1e-10)
        moment=abs(data['temperature']@full[1:-1]-full[0])/np.maximum(abs(full[0]),1e-300)
        test(checks,'RAW_MOMENT:'+anchor,float(max(moment)),1e-10)
        component_norms=np.asarray([norm(value) for value in deltas])
        budget=component_norms.sum(axis=0)/scale
        component_ratio=component_norms/np.maximum(previous_norms,1e-300)
        contraction=budget/np.maximum(previous_budget,1e-300)
        coherent_ratio=norm(total)/np.maximum(norm(data[anchor+'_delta_total']),1e-300)
        for column,label in enumerate(COLUMN_NAMES):
            test(checks,'ACCURACY:'+anchor+':'+label,float(budget[column]),.01)
            test(checks,'CONTRACTION:component_sum:'+anchor+':'+label,float(contraction[column]),1.)
            test(checks,'CONTRACTION:coherent:'+anchor+':'+label,float(coherent_ratio[column]),1.)
            for position,key in enumerate(COMPONENTS):
                test(checks,'CONTRACTION:'+key+':'+anchor+':'+label,float(component_ratio[position,column]),1.)
        source_metrics[anchor]=dict(component_relative=(component_norms/scale).tolist(),
            component_sum=budget.tolist(),coherent=(norm(total)/scale).tolist(),
            component_sum_over_coldS4=(component_norms.sum(axis=0)/cold_scale).tolist(),
            previous_component_sum=previous_budget.tolist(),component_contraction=component_ratio.tolist(),
            component_sum_contraction=contraction.tolist(),coherent_contraction=coherent_ratio.tolist(),
            arithmetic=(norm(full-sequential)/scale).tolist(),pair=pair.tolist(),raw_moment=moment.tolist(),
            new_order=6,reference_order=5,normalization_order=4,convergence_order_known=False)
        data[anchor+'_source6']=full
        data[anchor+'_raw_source6']=sequential
        data[anchor+'_delta6_total']=total
        for key in COMPONENTS:
            position=COMPONENTS.index(key)
            data[anchor+'_order6_'+key]=stable[key]
            data[anchor+'_delta6_'+key]=deltas[position]
    def cosine(first,second):
        inner=np.sum(first[1:-1]*np.linalg.solve(mass,second[1:-1]),axis=0)
        return np.clip(inner/np.maximum(norm(first)*norm(second),1e-300),-1.,1.)
    cold_radius=sum(norm(data['delta6_'+key]) for key in COMPONENTS)/cold_scale
    margin=np.asarray(json.loads(allowance_path.read_text())['source']['routes']['cubic']['conditional_weighted_anchor_budget_to_keep_miss'])
    diagnostic={}
    for route in ['local','cubic']:
        coefficients={anchor:predictor_basis(.75,route,anchor) for anchor in ANCHORS}
        shift=combine([data[anchor+'_delta6_total'] for anchor in ANCHORS],list(coefficients.values()))
        old_shift=data[route+'_predictor_shift']
        prediction=combine([data[route+'_diagnostic_prediction'],shift],[1,1])
        observed_radius=sum(abs(coefficients[anchor])*sum(norm(data[anchor+'_delta6_'+key]) for key in COMPONENTS) for anchor in ANCHORS)/cold_scale
        old_radius=sum(abs(coefficients[anchor])*sum(norm(data[anchor+'_delta_'+key]) for key in COMPONENTS) for anchor in ANCHORS)/cold_scale
        old_coherent=norm(old_shift)/cold_scale
        coherent=norm(shift)/cold_scale
        close(checks,'Same-denominator previous predictor budget:'+route,old_radius,
            parent_report['prediction_diagnostics'][route]['noncancelling_anchor_budget_over_coldS4'],1e-12)
        old_cancel=old_coherent/np.maximum(old_radius,1e-300)
        new_cancel=coherent/np.maximum(observed_radius,1e-300)
        contraction=observed_radius/np.maximum(old_radius,1e-300)
        coherent_contraction=coherent/np.maximum(old_coherent,1e-300)
        before=norm(data['source6']-data['prediction_'+route])/norm(data['source6'])
        order5_error=norm(data['source6']-data[route+'_diagnostic_prediction'])/norm(data['source6'])
        after=norm(data['source6']-prediction)/norm(data['source6'])
        cold5=norm(data['source5']-prediction)/norm(data['source5'])
        for column,label in enumerate(COLUMN_NAMES):
            test(checks,'REFRESHED_FORECAST_DIAGNOSTIC:'+route+':'+label,float(after[column]),.01)
            test(checks,'CONTRACTION:weighted_predictor:'+route+':'+label,float(contraction[column]),1.)
            test(checks,'CONTRACTION:coherent_predictor:'+route+':'+label,float(coherent_contraction[column]),1.)
            test(checks,'CANCELLATION_DIAGNOSTIC:'+route+':'+label,float(abs(new_cancel[column]-old_cancel[column])),.1)
            if route=='cubic':
                test(checks,'CONDITIONAL_ANCHOR_BUDGET:'+label,float(observed_radius[column]/margin[column]),1.)
        diagnostic[route]=dict(coefficients=coefficients,original_frozen_error=before.tolist(),
            order5_diagnostic_error=order5_error.tolist(),diagnostic_refreshed_error=after.tolist(),
            predictor_shift_over_coldS4=coherent.tolist(),previous_predictor_shift_over_coldS4=old_coherent.tolist(),
            noncancelling_anchor_budget_over_coldS4=observed_radius.tolist(),
            previous_noncancelling_anchor_budget_over_coldS4=old_radius.tolist(),
            budget_contraction=contraction.tolist(),coherent_contraction=coherent_contraction.tolist(),
            previous_cancellation_fraction=old_cancel.tolist(),cancellation_fraction=new_cancel.tolist(),
            cancellation_fraction_change=(new_cancel-old_cancel).tolist(),
            predictor_shift_cosine_vs_previous=cosine(old_shift,shift).tolist(),
            warm_centre_raw_cosine=cosine(data['warm_delta6_total'],data['centre_delta6_total']).tolist(),
            previous_warm_centre_raw_cosine=cosine(data['warm_delta_total'],data['centre_delta_total']).tolist(),
            diagnostic_cold5_error=cold5.tolist(),endpoint_orders_unchanged=[4,4],
            latest_cold_budget_over_coldS4=cold_radius.tolist(),
            remaining_allowance_from153=margin.tolist() if route=='cubic' else None,
            only_two_anchors_tested=True,certified_continuum_radius=False,curve_adopted=False)
        data[route+'_diagnostic_prediction6']=prediction
        data[route+'_predictor_shift6']=shift
    diagnostics=('ACCURACY:','RAW_MOMENT:','REFRESHED_FORECAST_DIAGNOSTIC:',
        'CONDITIONAL_ANCHOR_BUDGET:','CONTRACTION:','CANCELLATION_DIAGNOSTIC:')
    numerical=all(row['passed'] for row in checks if not row['name'].startswith(diagnostics))
    np.savez_compressed(folder/'source.npz',**data)
    finish(folder,dict(checks=checks,numerical_integrity_passed=numerical,source_metrics=source_metrics,
        prediction_diagnostics=diagnostic,other_quadrature_axes_refined=False,curve_adopted=False),
        __file__,[*inputs,folder/'source.npz'])
    print(json.dumps(dict(metrics=source_metrics,prediction=diagnostic,failed=[row for row in checks if not row['passed']])),flush=True)
    assert numerical


if __name__=='__main__':
    main()
