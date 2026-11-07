from __future__ import annotations

from precision_common import *


def main():
    modest()
    folder=ROOT/'results/low-k-domain'
    folder.mkdir(parents=True,exist_ok=False)
    source=PARENT/'runs/heavy-fine/trajectory.npz'
    seed=np.load(source)
    named={name:seed['values'][index] for index,name in enumerate(seed['names'])}
    efold=seed['efold']
    scale=np.exp(efold)
    selected=scale>=.00016
    scale=scale[selected]
    named={name:value[selected] for name,value in named.items()}
    mass=float(seed['masses'][1])
    energy=named['dotphi_h']*named['dotf_h']+mass**2*named['phi_h']*named['f_h']
    pressure=named['dotphi_h']*named['dotf_h']-mass**2*named['phi_h']*named['f_h']
    names=['a','mts_drho_h','mts_q_h','mts_dp_h','H']
    modes=inherited.modes(2)
    small=modes[modes<=.0004]
    values=np.zeros((len(small),len(scale),len(names)))
    for index,wave in enumerate(small):
        values[index]=np.array([scale,4*wave**2*scale**2*energy,
            4*wave**3*scale*named['dotphi_h']*named['f_h'],4*wave**2*scale**2*pressure,scale*named['H']]).T
    synthetic=dict(names=np.array(names),modes=small,values=values)
    rows=[]
    paths=[source,ROOT/'runs/projection/status.json']
    for tag in ['a200','a225','a250']:
        path=ROOT/'runs/projection'/(tag+'-w6-d8.npz')
        table=np.load(path)
        expected=projection(synthetic,table,float(table['matching_scale']),float(table['matching_density']),6,8)['delta']
        old_path=SPECTRUM/'runs/projection'/(tag+'-w6-d8.npz')
        old=np.load(old_path)
        for index,wave in enumerate(small):
            rows.append(dict(matching=tag,k_Mpc_inverse=float(wave),curvature_prediction=float(expected[index]),
                corrected_numeric=float(table['matching_delta'][index]),original_numeric=float(old['matching_delta'][index]),
                corrected_relative_difference=float(table['matching_delta'][index]/expected[index]-1),
                original_relative_difference=float(old['matching_delta'][index]/expected[index]-1),
                interpretation='Leading-gradient reference with its own finite-k remainder; very-low-k native absolute-error floor is not a fitted physical feature.'))
        paths.extend([path,old_path])
    tails=[]
    for label in ['heavy','cold','heavy-200','heavy-250','heavy-window4']:
        source_path=ROOT/'results/spectrum'/(label+'.npz')
        packet=np.load(source_path)
        grid=packet['modes']
        trusted=grid<=5
        columns={key:packet[key][trusted] for key in ['delta_m','delta_cb','velocity_cdm','velocity_cb']}
        main=spectrum_summary(grid[trusted],columns,packet['scales'])
        cut=spectrum_summary(grid[trusted],columns,packet['scales'],kmin=1e-4)
        tails.append(dict(label=label,changes={key:max(abs(other[key]/base[key]-1) for base,other in zip(main,cut))
            for key in ['sigma8_m','fsigma8_cdm_m','velocity_sigma8_cb']}))
        paths.append(source_path)
    checks=[dict(name=row['label']+' integral robustness to kmin1e-4',passed=bool(max(row['changes'].values())<1e-4)) for row in tails]
    finish(folder,dict(rows=rows,tail_checks=tails,checks=checks,all_checks_passed=all(row['passed'] for row in checks),
        root_cause_scope='Compare the native tiny-amplitude response with the independent leading-gradient result. The requested-time schedule also changed; old/new differences alone do not isolate the slow-source correction.',
        no_rows_replaced_by_reference=True),__file__,paths)
    print(json.dumps(dict(tail_checks=tails,smallest_mode=[row for row in rows if row['k_Mpc_inverse']==float(small[0])])),flush=True)


if __name__=='__main__':
    main()
