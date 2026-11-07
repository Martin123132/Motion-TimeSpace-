from stage159_common import *
from decimal import Decimal,localcontext


def main():
    modest()
    folder=ROOT/'results/sources'
    folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    manifest_path=ROOT/'results/preflight/events.json'
    assert digest(manifest_path)==proof['manifest_sha256']
    assert digest(ROOT/'results/preflight/frozen-reference.npz')==proof['frozen_sha256']
    manifest=json.loads(manifest_path.read_text())
    data=read_npz(ROOT/'results/preflight/frozen-reference.npz')
    inputs=[manifest_path,ROOT/'results/preflight/status.json',ROOT/'results/preflight/frozen-reference.npz']
    checks=[]
    for part in [0,1]:
        location=ROOT/'runs/band3'/f'part{part}'
        assert verify_packet(location)['all_checks_passed']
        inputs.append(location/'status.json')
    factor=np.linalg.cholesky(data['mass'])
    def norm(value):
        value=np.asarray(value)
        shape=value.shape
        spectral=np.moveaxis(value[...,1:-1,:],-2,0).reshape(96,-1)
        return np.linalg.norm(np.linalg.solve(factor,spectral),axis=0).reshape(shape[:-2]+(shape[-1],))
    scale=norm(data['actual'])
    panels={}
    frequency_metrics={}
    for order,which in [(7,'old'),(8,'new')]:
        site_arrays=[]
        for site in SITES:
            rows=[row for row in manifest[which] if row['site']==site]
            frequencies=sorted(set(row['node']['frequency'] for row in rows))
            assert len(frequencies)==order and len(rows)==36*order
            weights=[next(row['node']['seed_weight'] for row in rows if row['node']['frequency']==value) for value in frequencies]
            slots={value:index for index,value in enumerate(frequencies)}
            terms=[[[] for value in frequencies] for component in COMPONENTS]
            with localcontext() as context:
                context.prec=60
                exact=np.empty((3,order,4,4),dtype=object)
                exact.fill(Decimal(0))
                for row in rows:
                    event,weight,path,loop_path=load_event(row)
                    inputs.extend([path,loop_path])
                    slot=slots[row['node']['frequency']]
                    for component_index,component in enumerate(COMPONENTS):
                        value=event[component]
                        terms[component_index][slot].append(-weight*value)
                        for position,moment in enumerate([0,1,2,97]):
                            for column in range(4):
                                exact[component_index,slot,position,column]+=Decimal.from_float(-weight)*Decimal.from_float(float(value[moment,column]))
                values=np.asarray([[stable_sum(group) for group in component] for component in terms])
                for component_index in range(3):
                    for slot in range(order):
                        values[component_index,slot,[0,1,2,97]]=np.asarray(exact[component_index,slot],dtype=float)
            site_arrays.append(values)
            if site==SITES[0]:
                common_frequencies=frequencies
                common_weights=weights
            else:
                assert frequencies==common_frequencies and weights==common_weights
        values=np.asarray(site_arrays)
        panels[order]=np.asarray([[stable_sum(component) for component in site] for site in values])
        joint=np.einsum('s,scfij->cfij',COEFFICIENTS,values)
        separate=np.sum(abs(COEFFICIENTS)[:,None,None,None]*norm(values),axis=0)
        joint_frequency=norm(joint)
        ratio=joint_frequency.sum(axis=1)/separate.sum(axis=1)
        test(checks,'Frequency triangle:'+str(order),float(np.max(ratio)),1+1e-12)
        frequency_metrics[str(order)]={component:ratio[index].tolist() for index,component in enumerate(COMPONENTS)}
        np.savez_compressed(folder/f'order{order}-frequency.npz',frequencies=common_frequencies,
            seed_weights=common_weights,sites=values,joint=joint,separate_frequency_norm=separate,
            joint_frequency_norm=joint_frequency,mass=data['mass'],scale=scale)
    test(checks,'Retained order7 panel reconstructed',float(np.max(norm(panels[7]-data['new_panels'][0])/scale)),1e-10)
    delta=panels[8]-panels[7]
    for site_index,site in enumerate(SITES):
        for component_index,component in enumerate(COMPONENTS):
            data[f'order8_{site}_{component}']=delta[site_index,component_index]
        data['order8_'+site+'_total']=sum(delta[site_index])
    current_joint=np.einsum('s,scij->cij',COEFFICIENTS,delta)
    previous_joint=np.einsum('s,scij->cij',COEFFICIENTS,data['delta_panels'][0])
    coherent=norm(current_joint)
    separate=np.sum(abs(COEFFICIENTS)[:,None,None]*norm(delta),axis=0)
    ratio=coherent/np.maximum(norm(previous_joint),1e-300)
    def cosine(first,second):
        inner=np.sum(first[1:-1]*np.linalg.solve(data['mass'],second[1:-1]),axis=0)
        return np.clip(inner/np.maximum(norm(first)*norm(second),1e-300),-1.,1.)
    full_joint=current_joint.sum(axis=0)
    previous_full_joint=previous_joint.sum(axis=0)
    panel_metrics=dict(component_joint_step_over_coldS4=(coherent/scale).tolist(),
        component_separate_site_budget_over_coldS4=(separate/scale).tolist(),
        component_coherence=(coherent/np.maximum(separate,1e-300)).tolist(),
        component_step_ratio_vs_order7_minus6=ratio.tolist(),
        component_step_cosines=[cosine(current_joint[index],previous_joint[index]).tolist() for index in range(3)],
        full_joint_step_over_coldS4=(norm(full_joint)/scale).tolist(),
        full_step_ratio=(norm(full_joint)/norm(previous_full_joint)).tolist(),
        full_step_cosine=cosine(full_joint,previous_full_joint).tolist())
    test(checks,'Component triangle',float(np.max(norm(full_joint)/coherent.sum(axis=0))),1+1e-12)
    increments=delta.sum(axis=1)
    previous_full=np.asarray([original_full(data,site) for site in SITES])
    full=previous_full+increments
    diagnostics={}
    for route in ['local','cubic']:
        prediction=current_prediction(data,route)
        previous_error=previous_full[0]-prediction
        prediction_shift=sum(source155.predictor_basis(.75,route,site)*increments[SITES.index(site)] for site in ['warm','centre'])
        current_error=full[0]-prediction-prediction_shift
        error_step=increments[0]-prediction_shift
        close(checks,'Fixed-basis error telescope:'+route,previous_error+error_step,current_error,1e-10)
        diagnostics[route]=dict(previous_relative_error=(norm(previous_error)/norm(previous_full[0])).tolist(),
            updated_relative_error=(norm(current_error)/norm(full[0])).tolist(),
            matched_shift_over_coldS4=(norm(error_step)/scale).tolist(),curve_adopted=False)
    data['order8_panel']=panels[8]
    data['order7_reference_panel']=panels[7]
    data['order8_delta']=delta
    data['after_order8_full']=full
    readiness,allowed={},{}
    basis=EpochBundle(FRACTIONS['cold']).basis
    coordinates=EnergyCoordinates(basis)
    for route in ['local','cubic']:
        maxima=dict(rewrite=0.,moment=0.,gas=0.)
        for phase in np.linspace(0,1,101):
            base=base_source(data,phase,route)
            pieces=[increment_source(data,phase,route,site) for site in SITES]
            change=sum(pieces)
            source=np.column_stack([base,base+change,change,*pieces])
            force,spectral,gas,metrics=coordinates.source(source)
            maxima['rewrite']=max(maxima['rewrite'],metrics['relative_change'])
            maxima['moment']=max(maxima['moment'],float(np.max(abs(basis.temperature@spectral-source[0])/np.maximum(abs(source[0]),1e-300))))
            maxima['gas']=max(maxima['gas'],float(np.max(abs(gas-source[-1]))))
        current=[]
        for name,limit in [('rewrite',1e-10),('moment',1e-10),('gas',1e-20)]:
            test(current,'READINESS:'+route+':'+name,maxima[name],limit)
        allowed[route]=all(row['passed'] for row in current)
        readiness[route]=maxima
        checks.extend(current)
    numerical=all(row['passed'] for row in checks)
    np.savez_compressed(folder/'source.npz',**data)
    finish(folder,dict(checks=checks,numerical_integrity_passed=numerical,panel_metrics=panel_metrics,
        frequency_metrics=frequency_metrics,diagnostics=diagnostics,readiness=readiness,allowed_routes=allowed,
        per_site_change_over_saved_source=(norm(increments)/norm(previous_full)).tolist(),
        temperature_curve_changed=False,band38_changed=False,other_axes_changed=False,
        continuum_error_bound=False),__file__,[*inputs,*folder.glob('*.npz')])
    print(json.dumps(dict(numerical=numerical,allowed=allowed,panel_metrics=panel_metrics,
        diagnostics=diagnostics,failed=[row for row in checks if not row['passed']])),flush=True)
    assert numerical


if __name__=='__main__':
    main()

