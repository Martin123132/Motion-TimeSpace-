from stage146_precision_common import *
from decimal import Decimal,localcontext


def combine(values,weights):
    with localcontext() as context:
        context.prec=60
        coefficients=[Decimal.from_float(float(weight)) for weight in weights]
        arrays=[value.ravel() for value in values]
        return np.array([float(sum((weight*Decimal.from_float(float(array[index]))
            for weight,array in zip(coefficients,arrays)),Decimal(0)))
            for index in range(values[0].size)]).reshape(values[0].shape)


def main():
    modest()
    folder=ROOT/'results/repaired-readiness'
    folder.mkdir(parents=True,exist_ok=False)
    inputs,checks,sources=[],[],{}
    for case in CASES:
        source_folder=ROOT/'results/reaggregation'/case
        report=verify_packet(source_folder)
        assert report['all_checks_passed']
        sources[case]=read_npz(source_folder/'source.npz')['remainder']
        inputs.extend([source_folder/'status.json',source_folder/'source.npz'])
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    coordinates=EnergyCoordinates(ladder.basis)
    mass,temperature,chemical=ladder.basis.mass,ladder.basis.temperature,ladder.basis.chemical
    anchors={key:sources[key] for key in ['start','centre','end']}
    anchors['curvature']=combine([sources['centre'],sources['start'],sources['end']],[1,-.5,-.5])
    warm_prediction=combine([sources['start'],sources['centre'],sources['end']],[.375,.75,-.125])
    warm_defect=combine([sources['warm'],warm_prediction],[1,-1])
    local_prediction=combine([sources['start'],sources['centre'],sources['end']],[-.125,.75,.375])
    cubic_prediction=combine([local_prediction,warm_defect],[1,-1])
    predictions={'local':local_prediction,'cubic':cubic_prediction}
    defects={kind:combine([sources['colder'],prediction],[1,-1]) for kind,prediction in predictions.items()}
    raw_path=PARENT/'results/colder-source/source.npz'
    frozen_path=PARENT/'results/preflight/frozen-prediction.npz'
    lock_path=PARENT/'results/preflight/prediction-lock.json'
    raw,frozen=read_npz(raw_path),read_npz(frozen_path)
    assert digest(frozen_path)==json.loads(lock_path.read_text())['prediction_sha256']
    inputs.extend([raw_path,frozen_path,lock_path,*ladder.inputs])
    rows={}
    for name,value in {**sources,'warm_defect':warm_defect,
                       **{kind+'_defect':value for kind,value in defects.items()},
                       **{'prediction_'+kind:value for kind,value in predictions.items()}}.items():
        rows[name]=coordinates.source(value)[3]
        with localcontext() as context:
            context.prec=60
            convert=lambda scalar:Decimal.from_float(float(scalar))
            rows[name]['raw_moments_60digits']=[str(sum((convert(temperature[index])*convert(value[index+1,column])
                for index in range(96)),Decimal(0))-convert(value[0,column])) for column in range(4)]
    actual_scale=max(float(np.max(abs(sources['colder'][0]))),1e-300)
    actual_checks=[]
    test(actual_checks,'Unprojected colder-source temperature moment',
         np.max(abs(temperature@sources['colder'][1:-1]-sources['colder'][0]))/actual_scale,1e-10)
    test(actual_checks,'Unprojected colder-source photon/gas energy pair',
         np.max(abs(sources['colder'][0]+sources['colder'][-1]))/actual_scale,1e-10)
    checks.extend(actual_checks)
    allowed,maximum,diagnostics={},{},{}
    for kind in ['local','cubic']:
        largest=max(rows[name]['relative_change'] for name in [*sources,'warm_defect',kind+'_defect','prediction_'+kind])
        largest_pair=0.
        largest_corrected_moment=0.
        for phase in np.linspace(0,1,1025):
            original=forecast(anchors,warm_defect,phase,kind)
            increment=cold_bubble(phase,kind)*defects[kind]
            value=np.column_stack([original,increment,original+increment])
            force,spectral,gas,record=coordinates.source(value)
            largest=max(largest,record['relative_change'])
            largest_pair=max(largest_pair,float(np.max(abs(gas-value[-1]))))
            largest_corrected_moment=max(largest_corrected_moment,float(np.max(abs(temperature@spectral-value[0])))/
                max(float(np.max(abs(value[0]))),1e-300))
        maximum[kind]=largest
        route_checks=[]
        test(route_checks,'Unchanged small-defect rewrite gate:'+kind,largest,1e-10)
        test(route_checks,'Independent gas pairing:'+kind,largest_pair,1e-20)
        test(route_checks,'Reconstructed moment:'+kind,largest_corrected_moment,1e-10)
        checks.extend(route_checks)
        allowed[kind]=all(row['passed'] for row in route_checks+actual_checks)
        diagnostics[kind]=dict(
            raw_defect_rewrite=coordinates.source(raw[kind+'_defect'])[3]['relative_change'],
            repaired_defect_rewrite=rows[kind+'_defect']['relative_change'],
            source_prediction_relative=(dual_norm(defects[kind][1:-1],mass)/dual_norm(sources['colder'][1:-1],mass)).tolist(),
            energy_prediction_relative=(abs(defects[kind][0])/abs(sources['colder'][0])).tolist(),
            number_prediction_relative=(abs(chemical@defects[kind][1:-1])/abs(chemical@sources['colder'][1:-1])).tolist(),
            prediction_change_over_literal=(dual_norm((predictions[kind]-frozen['prediction_'+kind])[1:-1],mass)/
                                           dual_norm(frozen['prediction_'+kind][1:-1],mass)).tolist(),
            defect_change_over_raw=(dual_norm((defects[kind]-raw[kind+'_defect'])[1:-1],mass)/
                                   dual_norm(raw[kind+'_defect'][1:-1],mass)).tolist())
    test(checks,'Energy-coordinate invertibility',coordinates.mass_rewrite_error,1e-12)
    test(checks,'Both cold defects differ by warm defect',np.max(abs(defects['cubic']-defects['local']-warm_defect))/
         np.max(abs(warm_defect)),1e-10)
    checks.append(dict(name='Literal frozen prediction hash retained',passed=True))
    np.savez_compressed(folder/'source.npz',**anchors,warm_defect=warm_defect,actual=sources['colder'],
        local_defect=defects['local'],cubic_defect=defects['cubic'],prediction_local=local_prediction,
        prediction_cubic=cubic_prediction,mass=mass,temperature=temperature,chemical=chemical)
    finish(folder,dict(checks=checks,rows=rows,diagnostics=diagnostics,allowed_routes=allowed,
        maximum_rewrite_by_route=maximum,threshold=1e-10,phases_checked=1025,
        literal_frozen_predictions_sha256=digest(frozen_path),original_raw_failure_retained=True,
        independent_holdout_repeated=False,interpretation='Numerical input repair of the previously tested curve; not a new blinded prediction.',
        no_projection_before_gate=True),__file__,[*inputs,folder/'source.npz'])
    print(json.dumps(dict(allowed_routes=allowed,maxima=maximum,diagnostics=diagnostics,
        failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
