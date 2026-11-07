from stage162_common import *


def aggregate(endpoint,order,theta,folder,inputs):
    nodes=list(integration_nodes(theta,order))
    frequencies=[value for value,weight in incoming_rule(order,BOUNDARIES[0],BOUNDARIES[-1])]
    slots={value:index for index,value in enumerate(frequencies)}
    terms=[[[] for component in COMPONENTS] for value in frequencies]
    sequential={component:np.zeros((98,4)) for component in COMPONENTS}
    with localcontext() as context:
        context.prec=60
        exact=np.empty((len(frequencies),3,4,4),dtype=object)
        exact.fill(Decimal(0))
        for node in nodes:
            event,weight,path,loop_path=load_node162(endpoint,order,node,theta)
            inputs.extend([path,loop_path])
            slot=slots[node['frequency']]
            for component_index,component in enumerate(COMPONENTS):
                contribution=-weight*event[component]
                sequential[component]+=contribution
                terms[slot][component_index].append(contribution)
                for position,moment in enumerate([0,1,2,97]):
                    for column in range(4):
                        exact[slot,component_index,position,column]+=Decimal.from_float(-weight)*Decimal.from_float(float(event[component][moment,column]))
        values=np.asarray([[stable_sum(group) for group in frequency] for frequency in terms])
        assert all(len(group)==36 for frequency in terms for group in frequency)
        values[:,:,[0,1,2,97],:]=np.asarray(exact,dtype=float)
    panels=np.asarray([[stable_sum(values[panel*order:(panel+1)*order,component])
        for component in range(3)] for panel in range(7)])
    totals=np.asarray([stable_sum(panels[:,component]) for component in range(3)])
    if order!=4:
        packet_folder=ROOT/'runs'/endpoint/f'order{order}'
        assert verify_packet(packet_folder)['all_checks_passed']
        stored=read_npz(packet_folder/'sequential.npz')
        assert all(np.array_equal(sequential[key],stored[key]) for key in COMPONENTS)
        inputs.extend([packet_folder/'status.json',packet_folder/'sequential.npz'])
    np.savez_compressed(folder/f'{endpoint}-order{order}-panels.npz',frequency_values=values,
        panels=panels,totals=totals,frequencies=frequencies,theta=theta)
    return panels,totals


def main():
    modest()
    folder=ROOT/'results/sources'
    folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    assert proof['all_checks_passed']
    data=read_npz(ROOT/'results/preflight/frozen-reference.npz')
    measure=SourceNorm(data['mass'])
    scale=measure(data['actual'])
    inputs=[ROOT/'results/preflight/status.json',ROOT/'results/preflight/frozen-reference.npz']
    checks,all_panels,metrics=[],{order:[] for order in [4,5,6]},{}
    for endpoint in ENDPOINTS:
        reference_path=ROOT/'results/preflight'/(endpoint+'-reference.npz')
        reference=read_npz(reference_path)
        inputs.append(reference_path)
        theta=proof['contexts'][endpoint][0]['theta']
        totals={}
        for order in [4,5,6]:
            panels,totals[order]=aggregate(endpoint,order,theta,folder,inputs)
            all_panels[order].append(panels)
        for component_index,component in enumerate(COMPONENTS):
            test(checks,'Original endpoint component independently reproduced:'+endpoint+':'+component,
                float(np.max(measure(totals[4][component_index]-endpoint_component(reference,endpoint,component))/scale)),1e-10)
        for order in [5,6]:
            delta=sum(totals[order]-totals[4])
            newfull=data[endpoint]+delta
            data[f'endpoint_{endpoint}_source{order}']=newfull
            pairing=abs(delta[0]+delta[-1])/np.maximum(abs(delta[0]),1e-300)
            moment=abs(data['temperature']@delta[1:-1]-delta[0])/np.maximum(abs(delta[0]),1e-300)
            test(checks,f'Endpoint photon/gas exchange:{endpoint}:{order}',float(max(pairing)),1e-10)
            test(checks,f'Endpoint unprojected moment:{endpoint}:{order}',float(max(moment)),1e-10)
        change54=sum(totals[5]-totals[4])
        change65=sum(totals[6]-totals[5])
        metrics[endpoint]=dict(theta=theta,fraction=ENDPOINTS[endpoint],
            step54_over_endpoint4=(measure(change54)/measure(data[endpoint])).tolist(),
            step65_over_endpoint4=(measure(change65)/measure(data[endpoint])).tolist(),
            step65_over_step54=(measure(change65)/measure(change54)).tolist(),
            cumulative64_over_endpoint4=(measure(change54+change65)/measure(data[endpoint])).tolist())
        print(json.dumps(dict(endpoint=endpoint,metrics=metrics[endpoint])),flush=True)
    panels={order:np.swapaxes(np.asarray(values),0,1) for order,values in all_panels.items()}
    for order,values in panels.items():
        data[f'endpoint_panels{order}']=values
    deltas={'54':panels[5]-panels[4],'65':panels[6]-panels[5],'64':panels[6]-panels[4]}
    for step,values in deltas.items():
        data['endpoint_delta'+step]=values
    close(checks,'Panel endpoint telescope',deltas['54']+deltas['65'],deltas['64'],1e-10)
    diagnostics,uncertainty={},{ }
    current=data['after_band820_full']
    for route in ['local','cubic']:
        weights=np.array([endpoint_basis(.75,route,endpoint) for endpoint in ENDPOINTS])
        old_prediction=old_prediction162(data,route)
        if route=='cubic':
            independent=data['start']/4-current[1]+1.5*current[2]+data['end']/4
            test(checks,'Independent cubic prediction from five frozen anchors',
                float(np.max(measure(independent-old_prediction)/scale)),1e-10)
        old_error=current[0]-old_prediction
        data['endpoint_'+route+'_error4']=old_error
        route_steps={}
        for step,values in deltas.items():
            matched_panels=-np.einsum('e,pecij->pij',weights,values)
            full_step=stable_sum(matched_panels)
            independent_budget=(abs(weights)[None,:,None,None]*measure(values)/scale).sum(axis=(0,1,2))
            matched_budget=(measure(matched_panels)/scale).sum(axis=0)
            norm_step=measure(full_step)/scale
            test(checks,'Endpoint independent/matched triangle:'+route+':'+step,
                float(max(matched_budget/np.maximum(independent_budget,1e-300))),1+1e-10)
            test(checks,'Endpoint panel/full triangle:'+route+':'+step,
                float(max(norm_step/np.maximum(matched_budget,1e-300))),1+1e-10)
            data['endpoint_'+route+'_step'+step]=full_step
            route_steps[step]=dict(full_step_over_coldH4=norm_step.tolist(),
                independent_budget_over_coldH4=independent_budget.tolist(),
                matched_panel_budget_over_coldH4=matched_budget.tolist(),
                independent_panel_budgets=(abs(weights)[None,:,None,None]*measure(values)/scale).sum(axis=(1,2)).tolist(),
                component_step_over_coldH4=(measure(-np.einsum('e,pecij->cij',weights,values))/scale).tolist())
        error5=old_error+data['endpoint_'+route+'_step54']
        error6=old_error+data['endpoint_'+route+'_step64']
        data['endpoint_'+route+'_error5']=error5
        data['endpoint_'+route+'_error6']=error6
        close(checks,'Fixed-predictor endpoint telescope:'+route,
            error5+data['endpoint_'+route+'_step65'],error6,1e-10)
        diagnostics[route]=dict(saved_relative_discrepancy=(measure(old_error)/measure(current[0])).tolist(),
            diagnostic_order5_relative=(measure(error5)/measure(current[0])).tolist(),
            diagnostic_order6_relative=(measure(error6)/measure(current[0])).tolist(),
            matched_step_contraction=(measure(data['endpoint_'+route+'_step65'])/
                measure(data['endpoint_'+route+'_step54'])).tolist(),
            steps=route_steps,curve_adopted=False,endpoint_weights=weights.tolist())
        interior=data['band820_latest_steps']
        interior_weights=parent160.weights_for(route)
        independent_interior=(abs(interior_weights)[None,:,None,None]*measure(interior)/scale).sum(axis=(0,1,2))
        matched_interior=(measure(np.einsum('s,pscij->pij',interior_weights,interior))/scale).sum(axis=0)
        cold_radius=(measure(interior[:,0])/scale).sum(axis=(0,1))
        independent_radius=independent_interior+np.array(route_steps['65']['independent_budget_over_coldH4'])
        matched_radius=matched_interior+np.array(route_steps['65']['matched_panel_budget_over_coldH4'])
        full_matched_step=np.einsum('s,pscij->pij',interior_weights,interior)-np.einsum('e,pecij->pij',weights,deltas['65'])
        allsite_matched_radius=(measure(full_matched_step)/scale).sum(axis=0)
        uncertainty[route]=dict(interior_independent=independent_interior.tolist(),
            interior_matched=matched_interior.tolist(),endpoint_latest=route_steps['65'],
            independent_conditional=parent160.conditional_radius(measure(error6)/scale,measure(current[0])/scale,independent_radius,cold_radius),
            group_matched_conditional=parent160.conditional_radius(measure(error6)/scale,measure(current[0])/scale,matched_radius,cold_radius),
            allsite_matched_conditional=parent160.conditional_radius(measure(error6)/scale,measure(current[0])/scale,allsite_matched_radius,cold_radius),
            certified=False,endpoint_axes_tested='incoming4/5/6 only',other_axes_radius=None)
    for key in ['endpoint_cubic_error4','endpoint_cubic_error5','endpoint_cubic_error6']:
        assert np.isfinite(data[key]).all()
    np.savez_compressed(folder/'source.npz',**data)
    summary=dict(stage=162,endpoints=metrics,diagnostics=diagnostics,uncertainty=uncertainty,
        interior_orders=[6,6,6,8,7,7,6],source_shape=[98,4],column_order=COLUMN_NAMES,
        endpoint_orders=[4,5,6],new_events=5544,reused_reference_events=2016,
        temperature_curve_changed=False,lower_bands_changed=False,
        incoming_continuum_error_certified=False,
        other_unbounded_axes=parent160.unresolved_axes()[1:])
    write_json(ROOT/'SOURCE-SUMMARY.json',summary)
    finish(folder,dict(checks=checks,summary=summary,numerical_integrity_passed=all(row['passed'] for row in checks)),__file__,
        [*inputs,folder/'source.npz',ROOT/'SOURCE-SUMMARY.json'])
    print(json.dumps(dict(source_complete=True,checks=len(checks),failed=[row for row in checks if not row['passed']],diagnostics=diagnostics)),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
