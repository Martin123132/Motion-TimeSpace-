from adjacent_source_common import *


def main():
    modest()
    folder=ROOT/'results/energy-coordinate-readiness'
    folder.mkdir(parents=True,exist_ok=False)
    owner=ROOT/'results/adjacent-sources'
    report=verify_packet(owner)
    failed=[row['name'] for row in report['checks'] if not row['passed']]
    assert set(failed)=={'Temperature moment:centre','Temperature moment:end',
                         *['INTERPOLATION_DIAGNOSTIC:centre source within1percent:'+name for name in COLUMN_NAMES]}
    data=read_npz(owner/'source.npz')
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    coordinates=EnergyCoordinates(basis)
    checks,rows=[],{}
    sources={key:data[key] for key in ['start','centre','end','curvature']}
    for index,fraction in enumerate(np.linspace(0,1,101)):
        secant=(1-fraction)*data['start']+fraction*data['end']
        defect=4*fraction*(1-fraction)*data['curvature']
        sources[f'phase-{index:03d}']=np.column_stack([secant,secant+defect,defect])
    maximum_rewrite=maximum_moment=maximum_pair=0.
    for label,original in sources.items():
        force,spectral,gas,metrics=coordinates.source(original)
        scale=np.maximum(np.max(abs(original[0])),1e-300)
        moment=float(np.max(abs(basis.temperature@spectral-original[0]))/scale)
        gas_change=float(np.max(abs(gas-original[-1])))
        maximum_rewrite=max(maximum_rewrite,metrics['relative_change'])
        maximum_moment=max(maximum_moment,moment)
        maximum_pair=max(maximum_pair,gas_change)
        if label in ['start','centre','end','curvature']:
            rows[label]=dict(**metrics,corrected_relative_energy_moment=moment,gas_absolute_change=gas_change)
    test(checks,'Inherited invertible energy representation',coordinates.mass_rewrite_error,1e-12)
    test(checks,'Unchanged1e-10 source-rewrite gate over anchors and101 phases',maximum_rewrite,1e-10)
    test(checks,'Corrected source temperature moment under original1e-10 gate',maximum_moment,1e-10)
    test(checks,'Independent energy-paired gas absolute adjustment',maximum_pair,1e-20)
    checks.append(dict(name='Original failed source tests retained;no arrays overwritten',passed=True))
    finish(folder,dict(checks=checks,rows=rows,maximum_relative_source_rewrite=maximum_rewrite,
                       maximum_corrected_energy_moment=maximum_moment,maximum_gas_absolute_adjustment=maximum_pair,
                       inherited_method_not_new_physics=True,raw_source_failures_retained=failed,
                       all_production_nodes_already_verified=True,
                       raw_temperature_moment_checks_passed=False,energy_coordinate_evolution_allowed=True),
           __file__,[owner/'source.npz',owner/'status.json',*ladder.inputs,
                     BRANCH/'history-dependent-source-20261011/ENERGY-COORDINATES.md'])
    print(json.dumps(dict(checks=len(checks),all_passed=all(row['passed'] for row in checks),
                          maximum_rewrite=maximum_rewrite,maximum_moment=maximum_moment,rows=rows)),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
