from __future__ import annotations

from precision_common import *


def main():
    modest()
    folder=ROOT/'runs/projection'
    folder.mkdir(parents=True,exist_ok=False)
    table_path=ROOT/'runs/sources/unmatched-base.npz'
    table=np.load(table_path)
    exact=ROOT/'runs/exact'
    assert json.loads((exact/'status.json').read_text())['state']=='complete'
    packets=sorted(exact.glob('chunk-*.npz'))
    configurations=[('a200',6,8),('a225',6,8),('a250',6,8),('a225',4,8),('a225',6,10)]
    reports=[]
    paths=[table_path,exact/'status.json',*packets,SPECTRUM/'project_grid.py']
    for tag,width,degree in configurations:
        source=ROOT/'runs/sources'/(tag+'-base.npz')
        corrected=np.load(source)
        center=float(corrected['matching_scale'])
        density=float(corrected['matching_density'])
        projected=[]
        modes=[]
        for path in packets:
            packet=np.load(path)
            projected.append(projection(packet,table,center,density,width,degree))
            modes.extend(packet['modes'])
        modes=np.array(modes)
        assert np.array_equal(modes,inherited.modes(2))
        combined={key:np.concatenate([item[key] for item in projected]) for key in ['delta','momentum','pressure','norm','closure_error']}
        base={key:corrected[key] for key in corrected.files if key not in ['modes','matching_delta','matching_momentum']}
        label=f'{tag}-w{width}-d{degree}'
        output=folder/(label+'.npz')
        np.savez_compressed(output,**base,modes=modes,matching_delta=combined['delta'],matching_momentum=combined['momentum'],
            projected_pressure=combined['pressure'],projection_norm=combined['norm'],closure_error=combined['closure_error'])
        old_path=SPECTRUM/'runs/projection'/(label+'.npz')
        old=np.load(old_path)
        trusted=modes<=5
        reports.append(dict(label=label,maximum_pressure_closure_error_trusted=float(max(combined['closure_error'][trusted])),
            failing_trusted_modes=modes[trusted&(combined['closure_error']>=2e-6)].tolist(),
            exploratory_failing_modes=modes[(modes>5)&(combined['closure_error']>=2e-6)].tolist(),
            maximum_projection_condition=float(max(item['condition'] for item in projected)),
            maximum_density_change_over_mode_norm=float(max(abs(combined['delta']-old['matching_delta'])/combined['norm'])),
            maximum_momentum_change_over_mode_norm=float(max(abs(combined['momentum']-old['matching_momentum'])/combined['norm']))))
        paths.extend([source,old_path,output])
    finish(folder,dict(configurations=reports,k_count=len(modes),matching_rows_recomputed=True),__file__,paths)
    print(json.dumps(reports),flush=True)


if __name__=='__main__':
    main()
