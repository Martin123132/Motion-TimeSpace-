from curvature_source_common import *


def ratio_metrics(actual,predicted,mass,chemical):
    denominator=dual_norm(actual[1:-1],mass)
    assert np.min(denominator)>0
    relative=dual_norm((actual-predicted)[1:-1],mass)/denominator
    observed=dict(photon_energy=actual[0],gas_energy=actual[-1],photon_number=chemical@actual[1:-1])
    forecasts=dict(photon_energy=predicted[0],gas_energy=predicted[-1],photon_number=chemical@predicted[1:-1])
    result=[]
    for column,label in enumerate(['heavy-join1','heavy-join2','cold-join1','cold-join2']):
        row=dict(profile=label,source_relative_error=float(relative[column]),
            actual_source_norm=float(denominator[column]),moments={})
        for name in observed:
            actual_value,predicted_value=float(observed[name][column]),float(forecasts[name][column])
            difference=abs(actual_value-predicted_value)
            row['moments'][name]=dict(actual=actual_value,predicted=predicted_value,absolute_error=difference,
                relative_error=difference/abs(actual_value) if actual_value!=0 else None,zero_denominator=actual_value==0)
        result.append(row)
    return result


def main():
    modest()
    folder=ROOT/'results/holdout-sources'
    folder.mkdir(parents=True,exist_ok=False)
    proof_path=ROOT/'results/frozen-predictions/status.json'
    proof=json.loads(proof_path.read_text())
    assert proof['all_checks_passed']
    for path,expected in proof['input_hashes'].items():
        assert digest(path)==expected,path
    prediction_path=ROOT/'results/frozen-predictions/prediction.npz'
    assert digest(prediction_path)==proof['prediction_sha256']
    prediction=dict(np.load(prediction_path))
    sampled_path=ROOT/'results/frozen-predictions/sampled-leading.npz'
    sampled=dict(np.load(sampled_path))
    mass,temperature,chemical=[prediction[key] for key in ['mass','temperature','chemical']]
    checks,inputs,rows,arrays,metrics=[],[proof_path,prediction_path,sampled_path],[],{},{}
    components={}
    for epoch,fraction in FRACTIONS.items():
        bundle=EpochBundle(fraction)
        theta=epoch_context(bundle)[0][0]['theta']
        assert theta==proof['epoch_contexts'][epoch][0][0]['theta']
        inputs+=bundle.inputs
        totals={key:np.zeros((98,4)) for key in ['difference','virtual','state','control']}
        for part in ['expensive','control']:
            keys=['difference','virtual','state'] if part=='expensive' else ['control']
            location=ROOT/'runs'/f'{part}-{epoch}'
            packet=json.loads((location/'status.json').read_text())
            assert (location/'COMPLETE').exists() and packet['all_checks_passed']
            for path,expected in packet['input_hashes'].items():
                assert digest(path)==expected,path
            aggregate=dict(np.load(location/'source.npz'))
            independent={key:np.zeros((98,4)) for key in keys}
            count=0
            for node in physical_nodes(theta,part):
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
                    assert loop['identity']==inherited.virtual_identity(parameters)
                    assert loop['scalar']==float(saved['loop_scalar']) and loop['finite']
                inputs.append(path)
                count+=1
            assert count==packet['nodes']==len(list((location/'nodes').rglob('*.npz')))
            error=max(float(np.max(abs(independent[key]-aggregate[key]))/max(np.max(abs(aggregate[key])),1e-300)) for key in keys)
            checks.append(dict(name=f'Actual nodes,weights,loops and independently reconstructed aggregate:{epoch}-{part}',value=error,passed=error<1e-12))
            rows.append(dict(epoch=epoch,part=part,nodes=count,theta=theta))
            for key in keys:
                totals[key]+=aggregate[key]
            inputs.extend([location/'status.json',location/'source.npz'])
        totals['sampled_leading']=sampled[epoch]
        totals['kinematic_remainder']=totals['control']-sampled[epoch]
        totals['remainder']=sum(totals[key] for key in ['kinematic_remainder','difference','virtual','state'])
        actual=totals['remainder']
        forecast=prediction[epoch+'_remainder']
        linear=prediction[epoch+'_linear_remainder']
        defect=actual-forecast
        for label,source in [('actual',actual),('quadratic',forecast),('linear',linear),('defect',defect)]:
            scale=max(float(np.max(abs(source[0]))),1e-30)
            pairing=float(np.max(abs(source[0]+source[-1])))
            projection=float(np.max(abs(temperature@source[1:-1]-source[0])))
            checks.extend([dict(name=f'Independent photon/gas pairing:{epoch}-{label}',value=pairing,passed=pairing<1e-6*scale),
                dict(name=f'Spectral projection equals independent energy:{epoch}-{label}',value=projection,passed=projection<1e-6*scale)])
        component_defects={key:totals[key]-prediction[epoch+'_'+key] for key in totals}
        denominator=dual_norm(actual[1:-1],mass)
        sum_error=dual_norm((sum(component_defects[key] for key in ['kinematic_remainder','difference','virtual','state'])-defect)[1:-1],mass)/denominator
        checks.append(dict(name='All component defects sum to full residual:'+epoch,value=float(sum_error.max()),passed=bool(sum_error.max()<1e-12)))
        components[epoch]={key:(dual_norm(value[1:-1],mass)/denominator).tolist() for key,value in component_defects.items()}
        metrics[epoch]={name:ratio_metrics(actual,source,mass,chemical) for name,source in [('quadratic',forecast),('linear',linear)]}
        arrays.update({epoch+'_'+key:value for key,value in totals.items()})
        arrays.update({epoch+'_delta_'+key:value for key,value in component_defects.items()})
        arrays.update({epoch+'_actual':actual,epoch+'_predicted':forecast,epoch+'_linear_predicted':linear,epoch+'_defect':defect})
    quarter,middle,last=prediction['anchors']
    central_defect=middle-(quarter+last)/2
    actual_nodes=[quarter,arrays['early_actual'],middle,arrays['late_actual'],last]
    node_errors=[]
    for phase,actual_node in zip([0.,.25,.5,.75,1.],actual_nodes):
        quadratic=(1-phase)*quarter+phase*last+4*phase*(1-phase)*central_defect
        left=max(0.,1-4*abs(phase-.25))*arrays['early_defect']
        right=max(0.,1-4*abs(phase-.75))*arrays['late_defect']
        error=dual_norm((quadratic+left+right-actual_node)[1:-1],mass)/np.maximum(dual_norm(actual_node[1:-1],mass),1e-300)
        node_errors.append(float(error.max()))
    checks.append(dict(name='Defect-corrected quadratic reproduces all five source nodes without moving old anchors',values=node_errors,passed=max(node_errors)<1e-12))
    structural_passed=all(bool(row['passed']) for row in checks)
    assert structural_passed,[row for row in checks if not row['passed']]
    for epoch,comparisons in metrics.items():
        for method,measurements in comparisons.items():
            for row in measurements:
                prefix=f"FROZEN_FORECAST: {method}:{epoch}:{row['profile']}:"
                checks.append(dict(name=prefix+'source within1percent',value=row['source_relative_error'],
                    passed=row['source_relative_error']<=proof['source_relative_gate']))
                for name,value in row['moments'].items():
                    relative=value['relative_error']
                    passed=value['absolute_error']==0 if relative is None else relative<=proof['source_relative_gate']
                    checks.append(dict(name=prefix+name+' within1percent',value=relative,absolute_error=value['absolute_error'],passed=passed))
    np.savez(folder/'source.npz',**arrays,anchors=prediction['anchors'],mass=mass,temperature=temperature,chemical=chemical)
    finish(folder,dict(checks=checks,rows=rows,profile_metrics=metrics,relative_component_defects=components,
        numerical_integrity_all_passed=structural_passed,every_source_node_verified=True,
        frozen_prediction_sha256=digest(prediction_path),both_predictions_precede_production=True,
        source_interpolation_error_bounded=False,new_epoch_precision_gate_closed=False,
        new_parent_history=False,leading_total_addback_newly_computed=False,
        complete_finite_remainder_retained=True),__file__,inputs)
    print(json.dumps(dict(profile_metrics=metrics,relative_component_defects=components,
        failed=[row['name'] for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()

