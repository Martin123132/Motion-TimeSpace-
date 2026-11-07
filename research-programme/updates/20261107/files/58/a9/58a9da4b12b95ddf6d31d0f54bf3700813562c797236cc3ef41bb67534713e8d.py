from stage148_terminal_common import *


def main():
    modest()
    folder=ROOT/'results/readiness'
    folder.mkdir(parents=True,exist_ok=False)
    source_folder=ROOT/'results/terminal-sources'
    report=verify_packet(source_folder)
    assert report['numerical_integrity_all_passed']
    data=read_npz(source_folder/'source.npz')
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    coordinates=EnergyCoordinates(ladder.basis)
    checks,rows=[],{}
    sources={key:data[key] for key in ['start','centre','end','curvature']}
    for index,phase in enumerate(np.linspace(0,1,101)):
        secant=(1-phase)*data['start']+phase*data['end']
        defect=4*phase*(1-phase)*data['curvature']
        sources[f'phase-{index:03d}']=np.column_stack([secant,secant+defect,defect])
    maximum_rewrite=maximum_corrected_moment=maximum_pair=0.
    for label,original in sources.items():
        force,spectral,gas,metrics=coordinates.source(original)
        moment_scale=np.maximum(abs(original[0]),1e-300)
        moment=float(np.max(abs(ladder.basis.temperature@spectral-original[0])/moment_scale))
        pair=float(np.max(abs(gas-original[-1])))
        maximum_rewrite=max(maximum_rewrite,metrics['relative_change'])
        maximum_corrected_moment=max(maximum_corrected_moment,moment)
        maximum_pair=max(maximum_pair,pair)
        rows[label]=dict(**metrics,corrected_relative_energy_moment=moment,gas_absolute_change=pair)
    test(checks,'Inherited invertible energy representation',coordinates.mass_rewrite_error,1e-12)
    test(checks,'Unchanged source rewrite gate including isolated curvature',maximum_rewrite,1e-10)
    test(checks,'Corrected source temperature moment',maximum_corrected_moment,1e-10)
    test(checks,'Independent paired gas absolute change',maximum_pair,1e-20)
    allowed=all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,rows=rows,energy_coordinate_evolution_allowed=allowed,
        maximum_source_rewrite=maximum_rewrite,maximum_corrected_energy_moment=maximum_corrected_moment,
        maximum_gas_absolute_change=maximum_pair,raw_failures_retained=True),
        __file__,[source_folder/'status.json',source_folder/'source.npz',*ladder.inputs])
    print(json.dumps(dict(readiness=allowed,maximum_rewrite=maximum_rewrite,
        maximum_moment=maximum_corrected_moment,failed=[row for row in checks if not row['passed']])),flush=True)
    assert allowed


if __name__=='__main__':
    main()

