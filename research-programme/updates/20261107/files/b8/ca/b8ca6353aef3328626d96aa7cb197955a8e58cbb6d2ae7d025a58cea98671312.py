from colder_common import *
from decimal import Decimal,localcontext


def main():
    modest()
    folder=ROOT/'results/route-readiness'
    folder.mkdir(parents=True,exist_ok=False)
    raw=verify_packet(ROOT/'results/colder-source')
    assert not raw['energy_coordinate_evolution_allowed']
    source_path=ROOT/'results/colder-source/source.npz'
    data=read_npz(source_path)
    anchor_path=ANCHORS/'results/adjacent-sources/source.npz'
    warm_path=PARENT/'results/holdout-source/source.npz'
    anchors=read_npz(anchor_path)
    warm=read_npz(warm_path)['defect']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    coordinates=EnergyCoordinates(ladder.basis)
    rows={}
    with localcontext() as context:
        context.prec=60
        convert=lambda value:Decimal.from_float(float(value))
        for key in ['control','sampled_leading','kinematic_remainder','difference',
                    'virtual','state','actual','prediction_local','prediction_cubic',
                    'local_defect','cubic_defect']:
            value=data[key]
            moments=[str(sum((convert(ladder.basis.temperature[index])*convert(value[index+1,column])
                             for index in range(96)),Decimal(0))-convert(value[0,column]))
                     for column in range(4)]
            rows[key]=dict(exact_float_input_moments_60digits=moments,**coordinates.source(value)[3])
    maxima={}
    for kind in ['local','cubic']:
        maximum=0.
        for phase in np.linspace(0,1,129):
            original=forecast(anchors,warm,phase,kind)
            increment=cold_bubble(phase,kind)*data[kind+'_defect']
            maximum=max(maximum,coordinates.source(np.column_stack([original,increment,original+increment]))[3]['relative_change'])
        maxima[kind]=maximum
    checks=[]
    test(checks,'Local route alone retains original1e-10 rewrite gate',maxima['local'],1e-10)
    checks.append(dict(name='Cubic isolated defect fails unchanged gate and is NOT authorized for propagation',
                       passed=bool(maxima['cubic']>=1e-10)))
    checks.append(dict(name='Both full colder forecasts individually satisfy original rewrite gate',
                       passed=all(rows['prediction_'+kind]['relative_change']<1e-10 for kind in ['local','cubic'])))
    checks.append(dict(name='Actual source itself satisfies original rewrite gate',
                       passed=rows['actual']['relative_change']<1e-10))
    finish(folder,dict(checks=checks,rows=rows,maximum_rewrite_by_route=maxima,
        allowed_routes={'local':maxima['local']<1e-10,'cubic':False},
        raw_global_readiness_retained_false=True,original_threshold_unchanged=1e-10,
        decimal_scope='Exact moment of stored binary64 entries,not a higher-precision recalculation of events.',
        diagnosis='Raw input moment inconsistency becomes relatively amplified in the much smaller cubic prediction error.60digit evaluation confirms it is present in saved inputs,not just the final dot product.',
        next_required_precision='Re-evaluate control-minus-leading energy/number moment accumulation conservatively or at higher precision using saved event nodes; retain the frozen forecast and its raw failure.'),
        __file__,[source_path,ROOT/'results/colder-source/status.json',anchor_path,warm_path,*ladder.inputs])
    print(json.dumps(dict(allowed_routes={'local':True,'cubic':False},maxima=maxima,
        actual=rows['actual']['relative_change'],prediction=rows['prediction_cubic']['relative_change'],
        checks=len(checks))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
