from stage158_common import *
from decimal import Decimal,localcontext


def main():
    modest()
    folder=ROOT/'results/sources'
    folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    manifest_path=ROOT/'results/preflight/events.json'
    assert digest(manifest_path)==proof['manifest_sha256']
    manifest=json.loads(manifest_path.read_text())
    data=read_npz(ROOT/'results/preflight/frozen-reference.npz')
    assert digest(ROOT/'results/preflight/frozen-reference.npz')==proof['frozen_sha256']
    inputs=[manifest_path,ROOT/'results/preflight/status.json',ROOT/'results/preflight/frozen-reference.npz']
    checks=[]
    for band in BANDS:
        for part in [0,1]:
            location=ROOT/'runs'/f'band{band}'/f'part{part}'
            assert verify_packet(location)['all_checks_passed']
            inputs.append(location/'status.json')
    factor=np.linalg.cholesky(data['mass'])
    def norm(value):
        value=np.asarray(value)
        shape=value.shape
        spectral=np.moveaxis(value[...,1:-1,:],-2,0).reshape(96,-1)
        return np.linalg.norm(np.linalg.solve(factor,spectral),axis=0).reshape(shape[:-2]+(shape[-1],))
    scale=norm(data['actual'])
    arrays={}
    frequency_diagnostics={}
    for order,which in [(6,'old'),(7,'new')]:
        panels=np.zeros((2,3,3,98,4))
        for band_index,band in enumerate(BANDS):
            site_arrays=[]
            site_weights=[]
            site_frequencies=[]
            for site_index,site in enumerate(SITES):
                rows=[row for row in manifest[which] if row['site']==site and row['band']==band]
                frequencies=sorted(set(row['node']['frequency'] for row in rows))
                assert len(frequencies)==order and len(rows)==order*36
                frequency_slots={value:position for position,value in enumerate(frequencies)}
                terms=[[[] for frequency in frequencies] for component in COMPONENTS]
                moment_rows=[0,1,2,97]
                with localcontext() as context:
                    context.prec=60
                    exact=np.empty((3,order,4,4),dtype=object)
                    exact.fill(Decimal(0))
                    for row in rows:
                        saved,weight,path,loop_path=load_event(row)
                        inputs.extend([path,loop_path])
                        slot=frequency_slots[row['node']['frequency']]
                        for component_index,component in enumerate(COMPONENTS):
                            value=saved[component]
                            terms[component_index][slot].append(-weight*value)
                            for position,moment in enumerate(moment_rows):
                                for column in range(4):
                                    exact[component_index,slot,position,column]+=Decimal.from_float(-weight)*Decimal.from_float(float(value[moment,column]))
                    values=np.asarray([[stable_sum(group) for group in component_terms] for component_terms in terms])
                    for component_index in range(3):
                        for slot in range(order):
                            values[component_index,slot,moment_rows]=np.asarray(exact[component_index,slot],dtype=float)
                for component_index,component in enumerate(COMPONENTS):
                    panels[band_index,site_index,component_index]=stable_sum(values[component_index])
                weights=[next(row['node']['seed_weight'] for row in rows if row['node']['frequency']==frequency) for frequency in frequencies]
                site_arrays.append(values)
                site_weights.append(weights)
                site_frequencies.append(frequencies)
            assert np.array_equal(site_frequencies[0],site_frequencies[1]) and np.array_equal(site_frequencies[0],site_frequencies[2])
            assert np.array_equal(site_weights[0],site_weights[1]) and np.array_equal(site_weights[0],site_weights[2])
            values=np.asarray(site_arrays)
            joint=np.einsum('s,scfij->cfij',COEFFICIENTS,values)
            separate=np.sum(abs(COEFFICIENTS)[:,None,None,None]*norm(values),axis=0)
            coherent=norm(joint)
            fractions=coherent.sum(axis=1)/separate.sum(axis=1)
            frequency_diagnostics[f'band{band}-order{order}']={component:fractions[index].tolist() for index,component in enumerate(COMPONENTS)}
            test(checks,'Frequency triangle:'+str(band)+':'+str(order),float(np.max(fractions)),1+1e-12)
            np.savez_compressed(folder/f'band{band}-order{order}-frequencies.npz',
                frequencies=site_frequencies[0],seed_weights=site_weights[0],sites=values,joint=joint,
                separated_frequency_norm=separate,joint_frequency_norm=coherent,mass=data['mass'],scale=scale)
        arrays[order]=panels
    prior_frequency=read_npz(PARENT/'results/analysis/order6-frequency.npz')
    inputs.append(PARENT/'results/analysis/order6-frequency.npz')
    for band_index,band in enumerate(BANDS):
        test(checks,'Prior virtual panel replay:'+str(band),float(np.max(norm(arrays[6][band_index,:,1]-prior_frequency['panels'][:,band])/scale)),1e-10)
    delta=arrays[7]-arrays[6]
    for band_index,band in enumerate(BANDS):
        for site_index,site in enumerate(SITES):
            for component_index,component in enumerate(COMPONENTS):
                data[f'band{band}_{site}_{component}']=delta[band_index,site_index,component_index]
            data[f'band{band}_{site}_total']=sum(delta[band_index,site_index])
    previous=read_npz(PARENT/'results/analysis/step6-panels.npz')
    inputs.append(PARENT/'results/analysis/step6-panels.npz')
    panel_metrics={}
    for band_index,band in enumerate(BANDS):
        total=delta[band_index].sum(axis=1)
        joint=np.einsum('s,scij->cij',COEFFICIENTS,delta[band_index])
        coherent=norm(joint)
        separate=np.sum(abs(COEFFICIENTS)[:,None,None]*norm(delta[band_index]),axis=0)
        full_joint=joint.sum(axis=0)
        ratio=norm(joint[1])/norm(previous['joint_delta'][band])
        test(checks,'Panel component triangle:'+str(band),float(np.max(norm(full_joint)/coherent.sum(axis=0))),1+1e-12)
        panel_metrics[str(band)]=dict(bounds=list(BANDS[band]),component_joint_step_over_coldS4=(coherent/scale).tolist(),
            component_separate_site_budget_over_coldS4=(separate/scale).tolist(),
            component_coherence=(coherent/np.maximum(separate,1e-300)).tolist(),
            full_joint_step_over_coldS4=(norm(full_joint)/scale).tolist(),
            virtual_step_ratio_vs_order6_minus5=ratio.tolist(),
            per_site_total_change_over_coldS4=(norm(total)/scale).tolist())
    stages={}
    for phase,indices in [('after3',[0]),('after34',[0,1])]:
        increments=sum(delta[index].sum(axis=1) for index in indices)
        full=np.asarray([original_full(data,site)+increments[index] for index,site in enumerate(SITES)])
        diagnostic={}
        for route in ['local','cubic']:
            coefficients=[1.,-source155.predictor_basis(.75,route,'warm'),-source155.predictor_basis(.75,route,'centre')]
            shift=np.einsum('s,sij->ij',coefficients,increments)
            old_error=data['source6']-data[route+'_diagnostic_prediction6']
            updated_error=old_error+shift
            prediction=data[route+'_diagnostic_prediction6']+sum(source155.predictor_basis(.75,route,site)*increments[SITES.index(site)] for site in ['warm','centre'])
            close(checks,'Frozen-basis diagnostic telescope:'+phase+':'+route,full[0]-prediction,updated_error,1e-10)
            diagnostic[route]=dict(old_relative_error=(norm(old_error)/norm(data['source6'])).tolist(),
                updated_relative_error=(norm(updated_error)/norm(full[0])).tolist(),
                matched_shift_over_coldS4=(norm(shift)/scale).tolist(),
                curve_adopted=False)
        stages[phase]=dict(diagnostics=diagnostic,site_change_over_own_source=(norm(increments)/norm(np.asarray([original_full(data,site) for site in SITES]))).tolist())
        data[phase+'_full']=full
    basis=EpochBundle(FRACTIONS['cold']).basis
    coordinates=EnergyCoordinates(basis)
    allowed={}
    readiness={}
    for route in ['local','cubic']:
        maxima=dict(rewrite=0.,moment=0.,gas=0.)
        for phase in np.linspace(0,1,101):
            base=base_source(data,phase,route)
            pieces=[site_basis(phase,route,site)*data[f'band{band}_{site}_total'] for band in BANDS for site in SITES]
            first=sum(pieces[:3])
            second=sum(pieces[3:])
            source=np.column_stack([base,base+first,base+first+second,first,second,*pieces])
            force,spectral,gas,metrics=coordinates.source(source)
            maxima['rewrite']=max(maxima['rewrite'],metrics['relative_change'])
            maxima['moment']=max(maxima['moment'],float(np.max(abs(basis.temperature@spectral-source[0])/np.maximum(abs(source[0]),1e-300))))
            maxima['gas']=max(maxima['gas'],float(np.max(abs(gas-source[-1]))))
        current=[]
        for name,limit in [('rewrite',1e-10),('moment',1e-10),('gas',1e-20)]:
            test(current,'READINESS:'+route+':'+name,maxima[name],limit)
        allowed[route]=all(row['passed'] for row in current)
        checks.extend(current)
        readiness[route]=maxima
    numerical=all(row['passed'] for row in checks)
    np.savez_compressed(folder/'source.npz',**data,old_panels=arrays[6],new_panels=arrays[7],delta_panels=delta)
    finish(folder,dict(checks=checks,numerical_integrity_passed=numerical,
        panel_metrics=panel_metrics,frequency_diagnostics=frequency_diagnostics,stages=stages,
        allowed_routes=allowed,readiness=readiness,temperature_curve_changed=False,
        updated_interpolation_form=False,unselected_panels_unchanged=True,
        continuum_error_bound=False,new_event_evaluations=1296,reused_event_values=216),__file__,
        [*inputs,*folder.glob('*.npz')])
    print(json.dumps(dict(numerical=numerical,allowed=allowed,panel_metrics=panel_metrics,
        stages=stages,failed=[row for row in checks if not row['passed']])),flush=True)
    assert numerical


if __name__=='__main__':
    main()

