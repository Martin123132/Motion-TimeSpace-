from stage152_order6_common import *


def main():
    modest()
    folder=ROOT/'results/readiness'
    folder.mkdir(parents=True,exist_ok=False)
    source_folder=ROOT/'results/integration-source'
    report=verify_packet(source_folder)
    assert report['numerical_integrity_all_passed']
    data=read_npz(source_folder/'source.npz')
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    coordinates=EnergyCoordinates(ladder.basis)
    checks,rows,allowed=[],{},{}
    for case,(route,order) in CASES.items():
        maxima=dict(rewrite=0.,moment=0.,pair=0.)
        sources={'source':data['source'+str(order)],'central':data['source5'],
            'total':data[f'delta{order}_total'],
            **{key:data[f'delta{order}_{key}'] for key in COMPONENTS}}
        for index,phase in enumerate(np.linspace(0,1,101)):
            bubble=cold_bubble(phase,route)
            original=central_source(data,phase,route)
            components=[bubble*data[f'delta{order}_{key}'] for key in COMPONENTS]
            total=bubble*data[f'delta{order}_total']
            sources[f'phase{index}']=np.column_stack([original,original+total,total,*components])
        for label,source in sources.items():
            force,spectral,gas,metrics=coordinates.source(source)
            moment=float(max(abs(ladder.basis.temperature@spectral-source[0])/np.maximum(abs(source[0]),1e-300)))
            pair=float(max(abs(gas-source[-1])))
            maxima['rewrite']=max(maxima['rewrite'],metrics['relative_change'])
            maxima['moment']=max(maxima['moment'],moment)
            maxima['pair']=max(maxima['pair'],pair)
            if not label.startswith('phase'):
                rows[case+':'+label]=dict(**metrics,corrected_moment=moment,gas_absolute_change=pair)
        current=[]
        for label,limit in [('rewrite',1e-10),('moment',1e-10),('pair',1e-20)]:
            test(current,'READINESS:'+case+':'+label,maxima[label],limit)
        allowed[case]=all(row['passed'] for row in current)
        checks.extend(current)
        rows[case]=maxima
    test(checks,'Inherited invertible energy coordinates',coordinates.mass_rewrite_error,1e-12)
    finish(folder,dict(checks=checks,rows=rows,allowed_cases=allowed),__file__,
        [source_folder/'status.json',source_folder/'source.npz',*ladder.inputs])
    print(json.dumps(dict(allowed_cases=allowed,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
