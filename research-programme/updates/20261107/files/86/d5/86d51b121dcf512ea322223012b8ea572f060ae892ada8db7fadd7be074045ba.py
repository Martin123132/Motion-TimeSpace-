from holdout_common import *


def main():
    modest()
    folder=ROOT/'results/holdout-source'
    folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    frozen=read_npz(ROOT/'results/preflight/frozen-inputs.npz')
    prediction_path=ROOT/'results/preflight/frozen-prediction.npz'
    predicted=read_npz(prediction_path)
    assert digest(prediction_path)==proof['prediction_sha256']
    lock=json.loads((ROOT/'results/preflight/prediction-lock.json').read_text())
    assert lock['prediction_sha256']==digest(prediction_path)
    theta=proof['epoch_contexts']['holdout'][0]['theta']
    checks,inputs,totals=[],[prediction_path,ROOT/'results/preflight/status.json',
                            ROOT/'results/preflight/frozen-inputs.npz',
                            ROOT/'results/preflight/prediction-lock.json'],{}
    for part in ['expensive','control']:
        location=ROOT/'runs'/f'{part}-holdout'
        report=verify_packet(location)
        assert report['all_checks_passed']
        configuration=report['configuration']
        assert configuration['temperature']==theta
        stored=read_npz(location/'source.npz')
        keys=['difference','virtual','state'] if part=='expensive' else ['control']
        aggregate={key:np.zeros((98,4)) for key in keys}
        inputs.extend([location/'status.json',location/'source.npz'])
        count=0
        for node in physical_nodes(theta,part):
            path=location/'nodes'/f"{node['index']//500:03d}"/f"{node['index']:05d}.npz"
            record=read_npz(path)
            assert json.loads(str(record['identity']))==node
            parameters,weight=parameters_and_weight(theta,node)
            assert weight>0 and abs(float(record['weight'])/weight-1)<1e-14
            for key in keys:
                assert record[key].shape==(98,4) and np.isfinite(record[key]).all()
                aggregate[key]-=weight*record[key]
            if part=='expensive':
                loop_path=Path(str(record['loop_path']))
                assert loop_path.is_relative_to(ROOT/'virtual-cache')
                loop=json.loads(loop_path.read_text())
                assert loop['identity']==event_owner.inherited.virtual_identity(parameters)
                assert loop['finite'] and loop['scalar']==float(record['loop_scalar'])
                inputs.append(loop_path)
            inputs.append(path)
            count+=1
        assert count==report['nodes']==len(list((location/'nodes').rglob('*.npz')))
        assert all(np.array_equal(stored[key],aggregate[key]) for key in keys)
        totals.update(aggregate)
        checks.append(dict(name='All physical nodes weights and independent aggregates:'+part,passed=True,count=count))
    totals['sampled_leading']=frozen['holdout_sampled_leading']
    totals['kinematic_remainder']=totals['control']-totals['sampled_leading']
    totals['remainder']=sum(totals[key] for key in ['kinematic_remainder','difference','virtual','state'])
    actual=totals['remainder']
    defect=actual-predicted['predicted']
    mass,temperature,chemical=[predicted[key] for key in ['mass','temperature','chemical']]
    metrics={}
    for key in COMPONENTS:
        value=totals[key]
        error=value-predicted['predicted_'+key]
        metrics[key]=dict(source_norm=dual_norm(value[1:-1],mass).tolist(),
            prediction_error_norm=dual_norm(error[1:-1],mass).tolist(),
            relative= (dual_norm(error[1:-1],mass)/np.maximum(dual_norm(value[1:-1],mass),1e-300)).tolist())
    scale=max(float(np.max(abs(actual[0]))),1e-300)
    test(checks,'Independent event photon gas energy pair',np.max(abs(actual[0]+actual[-1]))/scale)
    assert checks[-1]['passed']
    test(checks,'RAW_MOMENT:independent temperature moment',
         np.max(abs(temperature@actual[1:-1]-actual[0]))/scale)
    source_errors=dual_norm(defect[1:-1],mass)/dual_norm(actual[1:-1],mass)
    for column,label in enumerate(COLUMN_NAMES):
        test(checks,'PREDICTION_DIAGNOSTIC:within frozen1percent:'+label,source_errors[column],.01)
    readiness=[]
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    coordinates=EnergyCoordinates(ladder.basis)
    prior=read_npz(PARENT/'results/adjacent-sources/source.npz')
    maximum_rewrite=maximum_moment=maximum_pair=0.
    samples=[actual,predicted['predicted'],defect]
    for kind in ['local','cubic']:
        for phase in np.linspace(0,1,129):
            prediction=quadratic(prior,phase)
            increment=bubble(phase,kind)*defect
            samples.append(np.column_stack([prediction,increment,prediction+increment]))
    for source in samples:
        force,spectral,gas,record=coordinates.source(source)
        maximum_rewrite=max(maximum_rewrite,record['relative_change'])
        maximum_moment=max(maximum_moment,float(np.max(abs(ladder.basis.temperature@spectral-source[0]))/
                                              max(float(np.max(abs(source[0]))),1e-300)))
        maximum_pair=max(maximum_pair,float(np.max(abs(gas-source[-1]))))
    test(readiness,'Energy-coordinate invertibility',coordinates.mass_rewrite_error,1e-12)
    test(readiness,'Unchanged1e-10 source rewrite',maximum_rewrite,1e-10)
    test(readiness,'Corrected spectral source energy',maximum_moment,1e-10)
    test(readiness,'Independent gas pairing absolute change',maximum_pair,1e-20)
    checks.extend(readiness)
    arrays=dict(actual=actual,prediction=predicted['predicted'],defect=defect,
                mass=mass,temperature=temperature,chemical=chemical,**totals)
    np.savez_compressed(folder/'source.npz',**arrays)
    inputs.extend([folder/'source.npz',PARENT/'results/adjacent-sources/source.npz',*ladder.inputs])
    report=dict(checks=checks,component_metrics=metrics,source_relative=source_errors.tolist(),
        energy_relative=(abs(defect[0])/np.maximum(abs(actual[0]),1e-300)).tolist(),
        number_relative=(abs(chemical@defect[1:-1])/np.maximum(abs(chemical@actual[1:-1]),1e-300)).tolist(),
        theta=theta,fraction=.5625,nodes_verified=5616,virtual_coefficients=1008,
        maximum_source_rewrite=maximum_rewrite,maximum_corrected_moment=maximum_moment,
        maximum_gas_pair_adjustment=maximum_pair,
        energy_coordinate_evolution_allowed=all(row['passed'] for row in readiness),
        prediction_frozen_before_events=True,
        next_interpolation_not_validated_by_fitting_holdout=True)
    finish(folder,report,__file__,inputs)
    print(json.dumps(dict(source_relative=source_errors.tolist(),theta=theta,
        rewrite=maximum_rewrite,failed=[row for row in checks if not row['passed']])),flush=True)
    assert report['energy_coordinate_evolution_allowed']


if __name__=='__main__':
    main()
