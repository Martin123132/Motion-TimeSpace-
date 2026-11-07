from withheld_source_common import *


def main():
    modest()
    folder=ROOT/'results/anchor-source'
    folder.mkdir(parents=True,exist_ok=False)
    bundle=EpochBundle()
    theta=epoch_context(bundle)[0][0]['theta']
    proof_path=ROOT/'results/frozen-prediction/status.json'
    proof=json.loads(proof_path.read_text())
    assert proof['all_checks_passed']
    totals={key:np.zeros((98,4)) for key in ['difference','virtual','state','control']}
    checks,inputs,rows=[],[proof_path],[]
    for part in ['expensive','control']:
        keys=['difference','virtual','state'] if part=='expensive' else ['control']
        for shard in [0,1]:
            location=ROOT/'runs'/f'{part}-withheld-shard{shard}'
            packet=json.loads((location/'status.json').read_text())
            assert (location/'COMPLETE').exists() and packet['all_checks_passed']
            for path,expected in packet['input_hashes'].items():
                assert digest(path)==expected,path
            aggregate=dict(np.load(location/'source.npz'))
            independent={key:np.zeros((98,4)) for key in keys}
            count=0
            for node in physical_nodes(theta,part):
                if node['index']%2!=shard:
                    continue
                path=location/'nodes'/f"{node['index']//500:03d}"/f"{node['index']:05d}.npz"
                with np.load(path) as archive:
                    saved={key:archive[key] for key in archive.files}
                assert json.loads(str(saved['identity']))==node
                parameters,weight=parameters_and_weight(theta,node)
                assert weight>0 and abs(weight/float(saved['weight'])-1)<1e-14
                for key in keys:
                    assert saved[key].shape==(98,4) and np.isfinite(saved[key]).all()
                    independent[key]-=weight*saved[key]
                if part=='expensive':
                    loop_path=Path(str(saved['loop_path']))
                    assert loop_path.is_relative_to(ROOT/'virtual-cache')
                    loop=json.loads(loop_path.read_text())
                    assert loop['identity']==inherited.virtual_identity(parameters) and loop['scalar']==float(saved['loop_scalar'])
                inputs.append(path)
                count+=1
            assert count==packet['nodes']==len(list((location/'nodes').rglob('*.npz')))
            error=max(float(np.max(abs(independent[key]-aggregate[key]))/max(np.max(abs(aggregate[key])),1e-300)) for key in keys)
            checks.append(dict(name=f'Actual identities,weights,loops and independent aggregate:{part}-{shard}',value=error,passed=error<1e-12))
            rows.append(dict(part=part,shard=shard,nodes=count))
            for key in keys:
                totals[key]+=aggregate[key]
            inputs.extend([location/'status.json',location/'source.npz'])
    prediction_path=ROOT/'results/frozen-prediction/prediction.npz'
    assert digest(prediction_path)=='a9a1eeba6c18f0d6e5f820a64c7e007cbb95c68caf698db313bd232a9afcebcc'
    prediction=dict(np.load(prediction_path))
    sampled_path=ROOT/'results/frozen-prediction/sampled-leading.npz'
    sampled=dict(np.load(sampled_path))['withheld']
    totals['sampled_leading']=sampled
    totals['kinematic_remainder']=totals['control']-sampled
    totals['remainder']=sum(totals[key] for key in ['kinematic_remainder','difference','virtual','state'])
    actual=totals['remainder']
    predicted=prediction['remainder']
    delta=actual-predicted
    mass,temperature,chemical=[prediction[key] for key in ['mass','temperature','chemical']]
    denominator=dual_norm(actual[1:-1],mass)
    assert np.min(denominator)>0 and actual.shape==(98,4)
    def normalized(value):
        return dual_norm(value[1:-1],mass)/denominator
    source_error=normalized(delta)
    for label,source in [('actual',actual),('prediction',predicted),('defect',delta)]:
        scale=max(float(np.max(abs(source[0]))),1e-30)
        pair=float(np.max(abs(source[0]+source[-1])))
        projection=float(np.max(abs(temperature@source[1:-1]-source[0])))
        checks.extend([dict(name='Independent photon/gas pairing:'+label,value=pair,passed=pair<1e-6*scale),
            dict(name='Temperature projection equals independent energy:'+label,value=projection,passed=projection<1e-6*scale)])
    raw_components={key:totals[key]-prediction[key] for key in totals}
    component_sum=sum(raw_components[key] for key in ['kinematic_remainder','difference','virtual','state'])
    checks.append(dict(name='Predicted and actual component defects sum to full defect',
        value=float(normalized(component_sum-delta).max()),passed=bool(normalized(component_sum-delta).max()<1e-12)))
    observed_moments=dict(photon_energy=actual[0],gas_energy=actual[-1],photon_number=chemical@actual[1:-1])
    predicted_moments=dict(photon_energy=predicted[0],gas_energy=predicted[-1],photon_number=chemical@predicted[1:-1])
    column_labels=['heavy-join1','heavy-join2','cold-join1','cold-join2']
    metrics=[]
    for column,label in enumerate(column_labels):
        row=dict(profile=label,source_relative_error=float(source_error[column]),
            actual_source_norm=float(denominator[column]),predicted_source_norm=float(dual_norm(predicted[1:-1],mass)[column]),moments={})
        for name in observed_moments:
            observed=float(observed_moments[name][column])
            forecast=float(predicted_moments[name][column])
            discrepancy=abs(forecast-observed)
            relative=discrepancy/abs(observed) if observed!=0 else None
            row['moments'][name]=dict(actual=observed,predicted=forecast,absolute_error=discrepancy,
                relative_error=relative,zero_denominator=observed==0)
        metrics.append(row)
    integrity_passed=all(bool(row['passed']) for row in checks)
    assert integrity_passed
    for row in metrics:
        checks.append(dict(name='FROZEN_FORECAST: source within1percent:'+row['profile'],
            value=row['source_relative_error'],passed=row['source_relative_error']<=proof['source_relative_gate']))
        for name,values in row['moments'].items():
            relative=values['relative_error']
            passed=values['absolute_error']==0 if relative is None else relative<=proof['source_relative_gate']
            checks.append(dict(name='FROZEN_FORECAST: '+name+' within1percent:'+row['profile'],
                value=relative,absolute_error=values['absolute_error'],passed=passed))
    components={key:normalized(value).tolist() for key,value in raw_components.items()}
    np.savez(folder/'source.npz',**totals,actual=actual,predicted=predicted,delta=delta,
        quarter=prediction['quarter'],midpoint=prediction['midpoint'],
        mass=mass,temperature=temperature,chemical=chemical,
        **{'delta_'+key:value for key,value in raw_components.items()})
    finish(folder,dict(checks=checks,rows=rows,profile_metrics=metrics,relative_component_defects=components,
        numerical_integrity_all_passed=integrity_passed,every_source_node_verified=True,
        frozen_prediction_sha256=digest(prediction_path),withheld_theta=theta,
        prediction_precedes_all_production=True,pilot_resolution=True,
        source_forecast_gate_passed=all(bool(row['passed']) for row in checks),
        withheld_precision_gate_closed=False,source_interpolation_error_bounded=False,
        new_parent_history=False,leading_total_addback_newly_computed=False,
        complete_finite_remainder_retained=True),__file__,[*inputs,sampled_path,prediction_path,*bundle.inputs])
    print(json.dumps(dict(profile_metrics=metrics,relative_component_defects=components,
        failed=[row['name'] for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()

