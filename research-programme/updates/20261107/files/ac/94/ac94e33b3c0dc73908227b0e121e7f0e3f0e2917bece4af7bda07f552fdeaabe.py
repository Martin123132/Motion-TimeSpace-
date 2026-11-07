from __future__ import annotations

from precision_common import *
from analyze_changes import fields


def main():
    modest()
    folder=ROOT/'results/production-spectrum'
    folder.mkdir(parents=True,exist_ok=False)
    source=ROOT/'runs/sources/unmatched-base.npz'
    table=np.load(source)
    grid=inherited.modes(2)
    selected=grid<=.0004
    tiny=grid[selected]
    old_exact=np.load(ROOT/'runs/exact/chunk-0000.npz')
    requested=old_exact['requested_scale']
    native=camb.get_background(inherited.inherited.params_for(source))
    native.Params.Accuracy.IntTolBoost=9
    times=native.conformal_time(1/requested-1,tol=1e-10)
    names=camb.model.evolve_names
    values=native.get_time_evolution(tiny,times,vars=names,lAccuracyBoost=4)
    assert np.isfinite(values).all() and np.all(values[:,:,names.index('a')]>0)
    exact_packet=dict(modes=tiny,values=values,names=np.array(names))
    exact_path=folder/'tiny-exact.npz'
    np.savez_compressed(exact_path,**exact_packet,requested_scale=requested)
    paths=[source,exact_path,ROOT/'results/tiny-mode-precision/status.json',ROOT/'results/low-k-domain/status.json']
    reports=[]
    checks=[]
    old_domain=json.loads((ROOT/'results/low-k-domain/status.json').read_text())
    matching_reports=[]
    tags={'heavy':'a225-w6-d8','heavy-200':'a200-w6-d8','heavy-250':'a250-w6-d8','heavy-window4':'a225-w4-d8'}
    for label,tag in tags.items():
        old_path=ROOT/'runs/projection'/(tag+'.npz')
        old=np.load(old_path)
        width=4 if label=='heavy-window4' else 6
        projected=projection(exact_packet,table,float(old['matching_scale']),float(old['matching_density']),width,8)
        candidate={key:old[key].copy() for key in old.files}
        for key,value in [('matching_delta','delta'),('matching_momentum','momentum'),('projected_pressure','pressure'),('projection_norm','norm'),('closure_error','closure_error')]:
            candidate[key][selected]=projected[value]
        candidate_path=folder/(tag+'-resolved.npz')
        np.savez_compressed(candidate_path,**candidate)
        comparable=[row for row in old_domain['rows'] if row['matching']==tag[:4]]
        assert len(comparable)==len(tiny)
        expected=np.array([row['curvature_prediction'] for row in comparable])
        relative=abs(projected['delta']/expected-1)
        checks.append(dict(name=tag+' tiny-mode curvature agreement',passed=bool(max(relative)<.01),value=float(max(relative)),limit=.01))
        checks.append(dict(name=tag+' pressure gate',passed=bool(max(projected['closure_error'])<2e-6),value=float(max(projected['closure_error'])),limit=2e-6))
        matching_reports.append(dict(label=label,k_count=len(tiny),maximum_curvature_relative_error=float(max(relative)),
            minimum_mode_density=float(projected['delta'][0]),minimum_mode_reference=float(expected[0])))
        native=camb.get_background(inherited.inherited.params_for(candidate_path))
        native.Params.Accuracy.IntTolBoost=9
        requested=inherited.late_scales()
        times=native.conformal_time(1/requested-1,tol=1e-10)
        late=native.get_time_evolution(tiny,times,vars=names,lAccuracyBoost=4)
        assert np.isfinite(late).all() and np.all(late[:,:,names.index('a')]>0)
        assert np.all(late[:,-1,names.index('mts_match_count')]==1)
        assert np.max(abs(late[:,:,names.index('mts_nonheavy_change')]))==0
        raw_path=folder/(label+'-tiny-native.npz')
        np.savez_compressed(raw_path,modes=tiny,requested_scale=requested,names=names,values=late)
        modes,scales,columns=fields(label)
        assert np.array_equal(modes,grid) and np.array_equal(scales,requested)
        background=np.load(ROOT/'runs'/label/'background.npz')
        cold,baryon,neutrino=[background[key] for key in ['cdm','baryon','nu']]
        combined=cold+baryon
        density_cb=(cold*late[:,:,names.index('delta_cdm')]+baryon*late[:,:,names.index('delta_baryon')])/combined
        actual=late[0,:,names.index('a')]
        density_total=(combined*density_cb+neutrino*late[:,:,names.index('delta_nu')]+actual**2*late[:,:,names.index('mts_drho_h')])/(combined+neutrino+float(old['matching_density'])*actual)
        velocity_cdm=late[:,:,names.index('v_newtonian_cdm')]
        velocity_cb=(cold*velocity_cdm+baryon*late[:,:,names.index('v_newtonian_baryon')])/combined
        for key,value in [('delta_m',density_total),('delta_cb',density_cb),('velocity_cdm',velocity_cdm),('velocity_cb',velocity_cb)]:
            columns[key][selected]=value
        trusted=modes<=5
        central=spectrum_summary(modes[trusted],{key:value[trusted] for key,value in columns.items()},scales)
        old_report=json.loads((ROOT/'results/spectrum/status.json').read_text())
        old_branch=next(row for row in old_report['branches'] if row['label']==label)
        shifts={key:max(abs(row[key]/base[key]-1) for row,base in zip(central,old_branch['central']))
            for key in ['sigma8_m','fsigma8_cdm_m','velocity_sigma8_cb']}
        output=folder/(label+'.npz')
        power=2*math.pi**2/grid[:,None]**3*previous.AS*(grid[:,None]/.05)**(previous.NS-1)*columns['delta_m']**2
        np.savez_compressed(output,modes=grid,scales=scales,linear_power_Mpc3=power,pressure_qualified_band=trusted,**columns)
        reports.append(dict(label=label,central=central,changes_from_intermediate_spectrum=shifts,
            low_k_rows_replaced_by_native=True,derived_curvature_used_only_as_check=True))
        checks.append(dict(name=label+' integrated-statistic stability',passed=bool(max(shifts.values())<1e-4),value=max(shifts.values()),limit=1e-4))
        paths.extend([old_path,candidate_path,raw_path,output,ROOT/'runs'/label/'background.npz',ROOT/'runs'/label/'status.json'])
        print(json.dumps(dict(label=label,matching=matching_reports[-1],statistic_changes=shifts)),flush=True)
    cold_path=ROOT/'results/spectrum/cold.npz'
    cold=np.load(cold_path)
    output=folder/'cold.npz'
    np.savez_compressed(output,**{key:cold[key] for key in cold.files})
    paths.extend([cold_path,output,ROOT/'results/spectrum/status.json',ROOT/'runs/exact/status.json',ROOT/'runs/projection/status.json'])
    finish(folder,dict(branches=reports,matching=matching_reports,checks=checks,all_checks_passed=all(row['passed'] for row in checks),
        corrected_low_mode_count=int(sum(selected)),precision_boost=9,analytic_rows_injected=False,
        unchanged_higher_modes_reused=True,unchanged_cold_spectrum_reused=True,
        production_matching_and_spectra_supersede_intermediate=True),__file__,paths)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
