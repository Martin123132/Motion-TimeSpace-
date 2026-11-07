from stage149_holdout_common import *


def main():
    modest()
    folder=ROOT/'results/readiness'
    folder.mkdir(parents=True,exist_ok=False)
    source_folder=ROOT/'results/holdout-source'
    report=verify_packet(source_folder)
    assert report['numerical_integrity_all_passed']
    data=read_npz(source_folder/'source.npz')
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    coordinates=EnergyCoordinates(ladder.basis)
    checks,rows,allowed=[],{},{}
    for route in ['local','cubic']:
        route_checks=[]
        sources={name:data[name] for name in ['actual','prediction_quadratic','defect']}
        for index,phase in enumerate(np.linspace(0,1,101)):
            original=quadratic(data,phase)
            increment=bubble(phase,route)*data['defect']
            sources[f'phase-{index:03d}']=np.column_stack([original,original+increment,increment])
        maximum_rewrite=maximum_moment=maximum_pair=0.
        for label,source in sources.items():
            force,spectral,gas,metrics=coordinates.source(source)
            moment=float(np.max(abs(ladder.basis.temperature@spectral-source[0])/np.maximum(abs(source[0]),1e-300)))
            pair=float(np.max(abs(gas-source[-1])))
            maximum_rewrite=max(maximum_rewrite,metrics['relative_change'])
            maximum_moment=max(maximum_moment,moment)
            maximum_pair=max(maximum_pair,pair)
            if label in ['actual','prediction_quadratic','defect']:
                rows[route+':'+label]=dict(**metrics,corrected_moment=moment,gas_absolute_change=pair)
        test(route_checks,'Unchanged own-source rewrite gate:'+route,maximum_rewrite,1e-10)
        test(route_checks,'Corrected energy moment:'+route,maximum_moment,1e-10)
        test(route_checks,'Independent gas absolute change:'+route,maximum_pair,1e-20)
        allowed[route]=all(row['passed'] for row in route_checks)
        rows[route]=dict(maximum_rewrite=maximum_rewrite,maximum_moment=maximum_moment,maximum_pair=maximum_pair)
        checks.extend(route_checks)
    test(checks,'Inherited invertible energy coordinates',coordinates.mass_rewrite_error,1e-12)
    finish(folder,dict(checks=checks,rows=rows,allowed_routes=allowed,raw_failures_retained=True),
        __file__,[source_folder/'status.json',source_folder/'source.npz',*ladder.inputs])
    print(json.dumps(dict(allowed_routes=allowed,rows=rows,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()

