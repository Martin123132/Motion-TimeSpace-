from stage154_anchor_common import *


def main():
    modest()
    folder=ROOT/'results/readiness'
    folder.mkdir(parents=True,exist_ok=False)
    source_path=ROOT/'results/anchor-sources/source.npz'
    assert verify_packet(ROOT/'results/anchor-sources')['numerical_integrity_passed']
    data=read_npz(source_path)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    coordinates=EnergyCoordinates(ladder.basis)
    checks,allowed,rows=[],{},{}
    for route in ['local','cubic']:
        maxima=dict(rewrite=0.,moment=0.,gas=0.)
        for phase in np.linspace(0,1,101):
            original=central_source(data,phase,route)
            components=delta_components(data,phase,route)
            total=sum(components)
            source=np.column_stack([original,original+total,total,*components])
            force,spectral,gas,metrics=coordinates.source(source)
            maxima['rewrite']=max(maxima['rewrite'],metrics['relative_change'])
            maxima['moment']=max(maxima['moment'],float(max(abs(ladder.basis.temperature@spectral-source[0])/np.maximum(abs(source[0]),1e-300))))
            maxima['gas']=max(maxima['gas'],float(max(abs(gas-source[-1]))))
        current=[]
        for name,limit in [('rewrite',1e-10),('moment',1e-10),('gas',1e-20)]:
            test(current,'READINESS:'+route+':'+name,maxima[name],limit)
        allowed[route]=all(row['passed'] for row in current)
        checks.extend(current)
        rows[route]=maxima
    test(checks,'Energy coordinate mass rewrite',coordinates.mass_rewrite_error,1e-12)
    finish(folder,dict(checks=checks,allowed_routes=allowed,rows=rows),__file__,
        [source_path,ROOT/'results/anchor-sources/status.json',*ladder.inputs])
    print(json.dumps(dict(allowed=allowed,rows=rows)),flush=True)


if __name__=='__main__':
    main()
