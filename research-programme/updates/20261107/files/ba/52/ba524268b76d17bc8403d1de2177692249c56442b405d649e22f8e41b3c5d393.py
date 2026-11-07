from stage148_terminal_common import *
from decimal import Decimal,localcontext


def combine(arrays,coefficients):
    with localcontext() as context:
        context.prec=60
        values=[float(sum((Decimal.from_float(float(coefficient))*Decimal.from_float(float(array.flat[index]))
                           for array,coefficient in zip(arrays,coefficients)),Decimal(0)))
                for index in range(arrays[0].size)]
    return np.asarray(values).reshape(arrays[0].shape)


def main():
    modest()
    folder=ROOT/'results/terminal-sources'
    folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    assert proof['all_checks_passed']
    frozen=read_npz(ROOT/'results/preflight/frozen-inputs.npz')
    inputs=[ROOT/'results/preflight/status.json',ROOT/'results/preflight/frozen-inputs.npz']
    checks,arrays,metrics=[],{'start':frozen['start_source']},{ }
    mass,temperature,chemical=[frozen[key] for key in ['mass','temperature','chemical']]
    moment_rows=[0,1,2,97]
    for epoch,fraction in FRACTIONS.items():
        theta=proof['epoch_contexts'][epoch][0]['theta']
        refined,raw,diagnostics={},{},{}
        for part,keys in [('control',['control']),('expensive',['difference','virtual','state'])]:
            location=ROOT/'runs'/f'{part}-{epoch}'
            report=verify_packet(location)
            assert report['all_checks_passed']
            stored=read_npz(location/'source.npz')
            expected=list(physical_nodes(theta,part))
            assert len(list((location/'nodes').rglob('*.npz')))==len(expected)==report['nodes']
            reference={key:np.zeros((98,4)) for key in keys}
            terms={key:[] for key in keys}
            with localcontext() as context:
                context.prec=60
                exact={key:[[Decimal(0) for column in range(4)] for row in moment_rows] for key in keys}
                for node in expected:
                    path=location/'nodes'/f"{node['index']//500:03d}"/f"{node['index']:05d}.npz"
                    saved=read_npz(path)
                    assert json.loads(str(saved['identity']))==node
                    parameters,weight=parameters_and_weight(theta,node)
                    assert weight>0 and abs(float(saved['weight'])/weight-1)<1e-14
                    weight_exact=Decimal.from_float(-weight)
                    for key in keys:
                        value=saved[key]
                        assert value.shape==(98,4) and np.isfinite(value).all()
                        contribution=-weight*value
                        reference[key]+=contribution
                        terms[key].append(contribution)
                        for index,row in enumerate(moment_rows):
                            for column in range(4):
                                exact[key][index][column]+=weight_exact*Decimal.from_float(float(value[row,column]))
                    inputs.append(path)
                    if part=='expensive':
                        loop_path=Path(str(saved['loop_path']))
                        assert loop_path.is_relative_to(ROOT/'virtual-cache')
                        loop=json.loads(loop_path.read_text())
                        assert loop['finite'] and loop['identity']==event_owner.inherited.virtual_identity(parameters)
                        assert loop['scalar']==float(saved['loop_scalar'])
                        inputs.append(loop_path)
                for key in keys:
                    assert np.array_equal(reference[key],stored[key])
                    flat=np.asarray(terms[key]).reshape(len(expected),-1)
                    stable=np.asarray([math.fsum(flat[:,column]) for column in range(flat.shape[1])]).reshape(98,4)
                    fsum_only=stable.copy()
                    stable[moment_rows]=[[float(value) for value in row] for row in exact[key]]
                    raw[key]=reference[key]
                    refined[key]=stable
                    diagnostics[key]=dict(exact_moment_rows=[[str(value) for value in row] for row in exact[key]],
                        sequential_reproduced_exactly=True,node_count=len(expected))
                    np.savez_compressed(folder/f'{epoch}-{key}-sums.npz',sequential=reference[key],
                        fsum=fsum_only,refined=stable,moment_rows=moment_rows)
            checks.append(dict(name='All node identities weights loops and sums:'+epoch+':'+part,passed=True))
            inputs.extend([location/'status.json',location/'source.npz'])
        raw['sampled_leading']=frozen[epoch+'_raw_sampled_leading']
        refined['sampled_leading']=frozen[epoch+'_sampled_leading']
        for collection in [raw,refined]:
            collection['kinematic_remainder']=collection['control']-collection['sampled_leading']
        raw['remainder']=sum(raw[key] for key in ['kinematic_remainder','difference','virtual','state'])
        refined['remainder']=combine([refined[key] for key in
            ['control','sampled_leading','difference','virtual','state']],[1,-1,1,1,1])
        actual=refined['remainder']
        arithmetic=dual_norm((actual-raw['remainder'])[1:-1],mass)/dual_norm(raw['remainder'][1:-1],mass)
        leading_change=dual_norm((refined['sampled_leading']-raw['sampled_leading'])[1:-1],mass)/dual_norm(raw['sampled_leading'][1:-1],mass)
        test(checks,'Same event source arithmetic change:'+epoch,float(max(arithmetic)),1e-10)
        test(checks,'Same leading quadrature arithmetic change:'+epoch,float(max(leading_change)),1e-10)
        scale=np.maximum(abs(actual[0]),1e-300)
        pairing=abs(actual[0]+actual[-1])/scale
        moment=abs(temperature@actual[1:-1]-actual[0])/scale
        test(checks,'Independent photon gas pair:'+epoch,float(max(pairing)),1e-10)
        raw_moment=abs(temperature@raw['remainder'][1:-1]-raw['remainder'][0])/np.maximum(abs(raw['remainder'][0]),1e-300)
        test(checks,'RAW_MOMENT_DIAGNOSTIC:repaired unprojected source:'+epoch,float(max(moment)),1e-10)
        forecasts={}
        for kind in ['quadratic','quartic']:
            predicted=frozen[epoch+'_'+kind+'_extrapolation']
            relative=dual_norm((actual-predicted)[1:-1],mass)/dual_norm(actual[1:-1],mass)
            forecasts[kind]=dict(source_relative=relative.tolist(),
                energy_relative=(abs(actual[0]-predicted[0])/scale).tolist(),
                number_relative=(abs(chemical@(actual-predicted)[1:-1])/np.maximum(abs(chemical@actual[1:-1]),1e-300)).tolist())
            for column,name in enumerate(COLUMN_NAMES):
                test(checks,'FORECAST_DIAGNOSTIC:'+epoch+':'+kind+':'+name,float(relative[column]),.01)
        arrays[epoch]=actual
        for key in COMPONENTS:
            arrays[epoch+'_'+key]=refined[key]
            arrays[epoch+'_raw_'+key]=raw[key]
        metrics[epoch]=dict(fraction=fraction,theta=theta,forecasts=forecasts,
            arithmetic_relative_change=arithmetic.tolist(),leading_relative_change=leading_change.tolist(),
            source_norm=dual_norm(actual[1:-1],mass).tolist(),raw_temperature_moment=raw_moment.tolist(),
            repaired_unprojected_temperature_moment=moment.tolist(),independent_pair_relative=pairing.tolist(),
            aggregation=diagnostics)
    arrays['curvature']=combine([arrays['centre'],arrays['start'],arrays['end']],[1,-.5,-.5])
    secant_error=dual_norm(arrays['curvature'][1:-1],mass)/dual_norm(arrays['centre'][1:-1],mass)
    metrics['centre_vs_new_secant']=secant_error.tolist()
    for column,name in enumerate(COLUMN_NAMES):
        test(checks,'INTERPOLATION_DIAGNOSTIC:centre versus endpoint secant:'+name,float(secant_error[column]),.01)
    numerical=all(row['passed'] for row in checks if not any(row['name'].startswith(prefix) for prefix in
        ['FORECAST_DIAGNOSTIC:','INTERPOLATION_DIAGNOSTIC:','RAW_MOMENT_DIAGNOSTIC:']))
    np.savez_compressed(folder/'source.npz',**arrays,mass=mass,temperature=temperature,chemical=chemical)
    finish(folder,dict(checks=checks,metrics=metrics,numerical_integrity_all_passed=numerical,
        new_event_nodes=11232,new_virtual_coefficients=2016,reused_start=True,no_projection_used=True,
        source_interval=[.75,1.],forecast_preproduction=True,source_grid_error_bounded=False,
        raw_moment_diagnostics_retained=True),__file__,[*inputs,folder/'source.npz'])
    print(json.dumps(dict(state='complete',numerical_integrity=numerical,metrics={
        key:{name:value for name,value in item.items() if name!='aggregation'} if isinstance(item,dict) else item
        for key,item in metrics.items()},failed=[row['name'] for row in checks if not row['passed']])),flush=True)
    assert numerical


if __name__=='__main__':
    main()

