from stage149_holdout_common import *
from assemble_terminal_sources import combine
from decimal import Decimal,localcontext


def aggregate(part,theta,folder,checks,inputs):
    keys=['control'] if part=='control' else ['difference','virtual','state']
    location=ROOT/'runs'/f'{part}-holdout'
    report=verify_packet(location)
    assert report['all_checks_passed']
    stored=read_npz(location/'source.npz')
    nodes=list(physical_nodes(theta,part))
    assert len(list((location/'nodes').rglob('*.npz')))==len(nodes)==report['nodes']
    reference={key:np.zeros((98,4)) for key in keys}
    terms={key:[] for key in keys}
    moment_rows=[0,1,2,97]
    with localcontext() as context:
        context.prec=60
        exact={key:[[Decimal(0) for column in range(4)] for row in moment_rows] for key in keys}
        for node in nodes:
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
        refined={}
        for key in keys:
            assert np.array_equal(reference[key],stored[key])
            flat=np.asarray(terms[key]).reshape(len(nodes),-1)
            stable=np.asarray([math.fsum(flat[:,column]) for column in range(flat.shape[1])]).reshape(98,4)
            fsum_only=stable.copy()
            stable[moment_rows]=[[float(value) for value in row] for row in exact[key]]
            refined[key]=stable
            np.savez_compressed(folder/(key+'-sums.npz'),sequential=reference[key],fsum=fsum_only,
                refined=stable,moment_rows=moment_rows)
    checks.append(dict(name='Verified physical identities,weights,loops and sequential sums:'+part,passed=True))
    inputs.extend([location/'status.json',location/'source.npz'])
    return reference,refined


def main():
    modest()
    folder=ROOT/'results/holdout-source'
    folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    assert proof['all_checks_passed']
    frozen=read_npz(ROOT/'results/preflight/frozen-inputs.npz')
    theta=proof['epoch_contexts']['holdout'][0]['theta']
    inputs=[ROOT/'results/preflight/status.json',ROOT/'results/preflight/frozen-inputs.npz']
    checks,raw,refined=[],{},{}
    for part in ['control','expensive']:
        sequential,stable=aggregate(part,theta,folder,checks,inputs)
        raw.update(sequential)
        refined.update(stable)
    raw['sampled_leading']=frozen['raw_sampled_leading']
    refined['sampled_leading']=frozen['sampled_leading']
    for collection in [raw,refined]:
        collection['kinematic_remainder']=collection['control']-collection['sampled_leading']
    raw['remainder']=sum(raw[key] for key in ['kinematic_remainder','difference','virtual','state'])
    refined['remainder']=combine([refined[key] for key in
        ['control','sampled_leading','difference','virtual','state']],[1,-1,1,1,1])
    mass,temperature,chemical=[frozen[key] for key in ['mass','temperature','chemical']]
    actual=refined['remainder']
    defect=combine([actual,frozen['prediction_quadratic']],[1,-1])
    arithmetic=dual_norm((actual-raw['remainder'])[1:-1],mass)/dual_norm(raw['remainder'][1:-1],mass)
    leading_change=dual_norm((refined['sampled_leading']-raw['sampled_leading'])[1:-1],mass)/dual_norm(raw['sampled_leading'][1:-1],mass)
    test(checks,'Same-event arithmetic change',float(max(arithmetic)),1e-10)
    test(checks,'Same-quadrature leading arithmetic change',float(max(leading_change)),1e-10)
    scale=np.maximum(abs(actual[0]),1e-300)
    pair=abs(actual[0]+actual[-1])/scale
    moment=abs(temperature@actual[1:-1]-actual[0])/scale
    raw_moment=abs(temperature@raw['remainder'][1:-1]-raw['remainder'][0])/np.maximum(abs(raw['remainder'][0]),1e-300)
    test(checks,'Independent photon gas pair',float(max(pair)),1e-10)
    test(checks,'RAW_MOMENT_DIAGNOSTIC:repaired unprojected moment',float(max(moment)),1e-10)
    metrics={}
    for kind in ['quadratic','secant']:
        predicted=frozen['prediction_'+kind]
        relative=dual_norm((actual-predicted)[1:-1],mass)/dual_norm(actual[1:-1],mass)
        metrics[kind]=dict(source_relative=relative.tolist(),
            energy_relative=(abs(actual[0]-predicted[0])/scale).tolist(),
            number_relative=(abs(chemical@(actual-predicted)[1:-1])/np.maximum(abs(chemical@actual[1:-1]),1e-300)).tolist())
        for column,label in enumerate(COLUMN_NAMES):
            test(checks,'PREDICTION_DIAGNOSTIC:'+kind+':'+label,float(relative[column]),.01)
    arrays={key:frozen[key] for key in ['start','centre','end','curvature','prediction_quadratic','prediction_secant']}
    arrays.update(actual=actual,defect=defect,mass=mass,temperature=temperature,chemical=chemical)
    arrays.update({'actual_'+key:value for key,value in refined.items()})
    arrays.update({'raw_'+key:value for key,value in raw.items()})
    numerical=all(row['passed'] for row in checks if not row['name'].startswith(('PREDICTION_DIAGNOSTIC:','RAW_MOMENT_DIAGNOSTIC:')))
    np.savez_compressed(folder/'source.npz',**arrays)
    finish(folder,dict(checks=checks,metrics=metrics,theta=theta,fraction=FRACTIONS['holdout'],phase=PHASE,
        arithmetic_relative_change=arithmetic.tolist(),leading_relative_change=leading_change.tolist(),
        raw_temperature_moment=raw_moment.tolist(),repaired_unprojected_moment=moment.tolist(),
        independent_pair_relative=pair.tolist(),numerical_integrity_all_passed=numerical,
        primary_prediction_passed=bool(max(metrics['quadratic']['source_relative'])<.01),
        new_event_nodes=5616,new_virtual_coefficients=1008,source_grid_error_bounded=False,
        no_projection_used=True,baseline_inner_history_refined=False),
        __file__,[*inputs,folder/'source.npz'])
    print(json.dumps(dict(numerical_integrity=numerical,metrics=metrics,arithmetic=arithmetic.tolist(),
        moment=moment.tolist(),pair=pair.tolist(),failed=[row['name'] for row in checks if not row['passed']])),flush=True)
    assert numerical


if __name__=='__main__':
    main()

