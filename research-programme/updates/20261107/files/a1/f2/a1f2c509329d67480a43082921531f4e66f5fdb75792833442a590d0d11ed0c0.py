from adjacent_source_common import *


def main():
    modest()
    folder=ROOT/'results/adjacent-sources'
    folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    frozen=read_npz(ROOT/'results/preflight/frozen-inputs.npz')
    inputs=[ROOT/'results/preflight/status.json',ROOT/'results/preflight/frozen-inputs.npz']
    checks,arrays,metrics=[],{},{}
    mass,temperature,chemical=[frozen[key] for key in ['mass','temperature','chemical']]
    arrays['start']=frozen['start_source']
    background=thermal_wave.thermal.ThermalBackground('heavy')
    midpoint_theta=background.at(.5*background.end)['thermal_parameter']
    for epoch,fraction in FRACTIONS.items():
        bundle=EpochBundle(fraction)
        theta=proof['epoch_contexts'][epoch][0]['theta']
        test(checks,'Independent exponential temperature history:'+epoch,
             abs(theta/(midpoint_theta*math.exp(-background.end*(fraction-.5)))-1),1e-14)
        totals={}
        for part in ['expensive','control']:
            location=ROOT/'runs'/f'{part}-{epoch}'
            report=verify_packet(location)
            assert report['all_checks_passed']
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
                    assert np.isfinite(record[key]).all() and record[key].shape==(98,4)
                    aggregate[key]-=weight*record[key]
                if part=='expensive':
                    loop_path=Path(str(record['loop_path']))
                    assert loop_path.is_relative_to(ROOT/'virtual-cache')
                    loop=json.loads(loop_path.read_text())
                    assert loop['identity']==event_owner.inherited.virtual_identity(parameters)
                    assert loop['scalar']==float(record['loop_scalar']) and loop['finite']
                    inputs.append(loop_path)
                inputs.append(path)
                count+=1
            assert count==report['nodes']==len(list((location/'nodes').rglob('*.npz')))
            assert all(np.array_equal(aggregate[key],stored[key]) for key in keys)
            totals.update(aggregate)
            checks.append(dict(name='All node identities weights loops and aggregates:'+epoch+':'+part,
                               count=count,passed=True))
        totals['sampled_leading']=frozen[epoch+'_sampled_leading']
        totals['kinematic_remainder']=totals['control']-totals['sampled_leading']
        totals['remainder']=sum(totals[key] for key in ['kinematic_remainder','difference','virtual','state'])
        actual=totals['remainder']
        arrays[epoch]=actual
        for key,value in totals.items():
            arrays[epoch+'_'+key]=value
        scale=np.maximum(np.max(abs(actual[0])),1e-300)
        test(checks,'Independent photon gas energy pair:'+epoch,np.max(abs(actual[0]+actual[-1]))/scale)
        test(checks,'Temperature moment:'+epoch,np.max(abs(temperature@actual[1:-1]-actual[0]))/scale)
        predicted=frozen[epoch+'_old_extrapolation_remainder']
        metrics[epoch]=dict(fraction=fraction,theta=theta,
                           source_norm=dual_norm(actual[1:-1],mass).tolist(),
                           old_extrapolation_relative=(dual_norm((actual-predicted)[1:-1],mass)/
                                                       dual_norm(actual[1:-1],mass)).tolist(),
                           energy=actual[0].tolist(),number=(chemical@actual[1:-1]).tolist())
    secant=(arrays['start']+arrays['end'])/2
    arrays['curvature']=arrays['centre']-secant
    midpoint_error=dual_norm(arrays['curvature'][1:-1],mass)/dual_norm(arrays['centre'][1:-1],mass)
    metrics['centre_vs_endpoint_secant']=dict(source_relative=midpoint_error.tolist(),
        energy_relative=(abs(arrays['curvature'][0])/abs(arrays['centre'][0])).tolist(),
        number_relative=(abs(chemical@arrays['curvature'][1:-1])/abs(chemical@arrays['centre'][1:-1])).tolist())
    structural=all(row['passed'] for row in checks)
    for column,label in enumerate(COLUMN_NAMES):
        test(checks,'INTERPOLATION_DIAGNOSTIC:centre source within1percent:'+label,midpoint_error[column],.01)
    np.savez_compressed(folder/'source.npz',**arrays,mass=mass,temperature=temperature,chemical=chemical)
    finish(folder,dict(checks=checks,metrics=metrics,numerical_integrity_all_passed=structural,
                       nodes_verified=11232,new_virtual_coefficients=2016,old_endpoint_reused=True,
                       full_source_grid_error_bounded=False,all_physical_profiles_retained=True,
                       source_window=[.5,.75],forecast_is_not_an_observational_test=True),
           __file__,[*inputs,folder/'source.npz'])
    print(json.dumps(dict(complete=True,metrics=metrics,
                          failed=[row['name'] for row in checks if not row['passed']])),flush=True)
    assert structural


if __name__=='__main__':
    main()
