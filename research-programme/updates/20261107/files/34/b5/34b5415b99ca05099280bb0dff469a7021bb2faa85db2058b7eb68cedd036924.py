from __future__ import annotations

from spectrum_common import *


def projection(packet,table,center,density0,width,degree):
    names=packet['names'].tolist()
    values=packet['values']
    scales=values[0,:,names.index('a')]
    valid=scales>0
    phase=np.full(len(scales),np.nan)
    phase_of_n=interpolate.CubicSpline(table['heavy_efold'],table['phase_h'])
    phase[valid]=phase_of_n(np.log(scales[valid]))
    middle=float(phase_of_n(math.log(center)))
    chosen=abs(phase-middle)<width*math.pi
    coordinate=(phase[chosen]-middle)/(width*math.pi)
    basis=np.column_stack([coordinate**power for power in range(degree+1)]+
        [coordinate**power*trig(2*phase[chosen]) for power in range(degree-1) for trig in [np.cos,np.sin]]+
        [coordinate**power*trig(4*phase[chosen]) for power in range(3) for trig in [np.cos,np.sin]])
    weights=np.linalg.pinv(basis)[0]
    selected=values[:,chosen]
    density=(selected[:,:,names.index('mts_drho_h')]*scales[chosen])@weights/density0
    momentum=(selected[:,:,names.index('mts_q_h')]*scales[chosen])@weights/density0
    pressure=(selected[:,:,names.index('mts_dp_h')]*scales[chosen])@weights/density0
    hubble=selected[:,:,names.index('H')]@weights
    mode=packet['modes']
    ratio=(mode/(center*float(table['heavy_mass_mpc'])))**2
    sound2=ratio/(np.sqrt(1+ratio)+1)**2
    predicted=sound2*(density+3*hubble*momentum/mode)
    norm=np.maximum.reduce([abs(density),abs(mode*momentum/hubble)/np.maximum(1,mode/hubble*np.sqrt(sound2)),
        np.full(len(mode),1e-6)])
    return dict(delta=density,momentum=momentum,pressure=pressure,norm=norm,
        closure_error=abs(pressure-predicted)/norm,condition=np.linalg.cond(basis))


def main():
    modest()
    folder=ROOT/'runs/projection'
    folder.mkdir(parents=True,exist_ok=False)
    exact=ROOT/'runs/exact-grid'
    assert json.loads((exact/'status.json').read_text())['state']=='complete'
    paths=sorted(exact.glob('chunk-*.npz'))
    table=np.load(BACKGROUND)
    configurations=[('a200',6,8),('a225',6,8),('a250',6,8),('a225',4,8),('a225',6,10)]
    summaries=[]
    for tag,width,degree in configurations:
        parent_path=PARENT/'runs/matching-inputs'/(tag+'-w6-d8.npz')
        parent=np.load(parent_path)
        center=float(parent['matching_scale'])
        density0=float(parent['matching_density'])
        outputs=[]; all_modes=[]
        for path in paths:
            packet=np.load(path)
            outputs.append(projection(packet,table,center,density0,width,degree))
            all_modes.extend(packet['modes'])
        grid=np.array(all_modes)
        assert np.array_equal(grid,modes(2))
        combined={key:np.concatenate([row[key] for row in outputs]) for key in ['delta','momentum','pressure','norm','closure_error']}
        new={key:parent[key] for key in parent.files if key not in ['modes','matching_delta','matching_momentum']}
        label=f'{tag}-w{width}-d{degree}'
        np.savez_compressed(folder/(label+'.npz'),**new,modes=grid,
            matching_delta=combined['delta'],matching_momentum=combined['momentum'],
            projected_pressure=combined['pressure'],projection_norm=combined['norm'],closure_error=combined['closure_error'])
        anchor_errors=[]
        if degree==8 and width==6:
            for index,mode in enumerate(parent['modes']):
                current=int(np.argmin(abs(grid-mode)))
                assert abs(grid[current]/mode-1)<1e-12
                anchor_errors.append(dict(k=float(mode),delta_change_over_mode_norm=float(abs(combined['delta'][current]-parent['matching_delta'][index])/combined['norm'][current]),
                    momentum_change_over_mode_norm=float(abs(combined['momentum'][current]-parent['matching_momentum'][index])/combined['norm'][current])))
        summaries.append(dict(label=label,maximum_closure_error=float(max(combined['closure_error'])),
            maximum_condition=float(max(row['condition'] for row in outputs)),
            modes_above_inherited_pressure_gate=grid[combined['closure_error']>=2e-6].tolist(),anchors=anchor_errors))
    finish(folder,dict(configurations=summaries,k_count=len(grid),sourced_all_modes=True,interpolated_matching_rows=False),
        __file__,[BACKGROUND,exact/'status.json',*paths,*folder.glob('*.npz'),
            *[PARENT/'runs/matching-inputs'/(tag+'-w6-d8.npz') for tag in ['a200','a225','a250']]])
    print(json.dumps(summaries,indent=2))


if __name__=='__main__':
    main()
