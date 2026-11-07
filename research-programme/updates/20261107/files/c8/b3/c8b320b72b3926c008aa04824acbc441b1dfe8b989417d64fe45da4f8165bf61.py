from compare_refinements import feature_errors
from evolution_common import *


def main():
    modest()
    folder=ROOT/'results/accepted-refinements'
    folder.mkdir(parents=True,exist_ok=False)
    old_path=ROOT/'results/refinements/status.json'
    previous=json.loads(old_path.read_text())
    inputs=[old_path,ROOT/'compare_refinements.py']
    checks=[]
    rows=[]
    responses=[]
    for model in ['heavy','cold']:
        packets={}
        for name in ['quarter','eighth','sixteenth']:
            path=ROOT/'runs'/(model+'-'+name)/'evolution.npz'
            packets[name]=np.load(path)
            inputs.extend([path,path.parent/'status.json'])
        for name,first,second in [('quarter_to_eighth','quarter','eighth'),('eighth_to_sixteenth','eighth','sixteenth')]:
            errors=feature_errors(packets[first]['features'][-1],packets[second]['features'][-1])
            maximum=max(row['relative_error'] for row in errors)
            rows.append(dict(model=model,comparison=name,maximum_error=maximum,observables=errors,passes_original_gate=maximum<.001))
            if name=='eighth_to_sixteenth':
                checks.append(dict(name=model+': fine time refinement meets original gate',passed=maximum<.001,value=maximum,gate=.001))
        history=[row['maximum_error'] for row in previous['rows'] if row['model']==model and row['comparison'] in ['all_steps_halved','all_steps_quartered']]
        history+=[row['maximum_error'] for row in rows if row['model']==model]
        ratios=[history[index]/history[index+1] for index in range(len(history)-1)]
        checks.append(dict(name=model+': quadratic flow error shrinks consistently',passed=all(3<value<5 for value in ratios),error_sequence=history,reduction_ratios=ratios))
        for name in ['angular_6_to_8','start_twice_earlier']:
            saved=next(row for row in previous['checks'] if row['name']==model+': '+name)
            checks.append(dict(saved,name=model+': retained independent '+name+' check'))
        principal=packets['sixteenth']
        features=principal['features'][-1]
        status=json.loads((ROOT/'runs'/(model+'-sixteenth')/'status.json').read_text())
        check_value=max(np.max(sample['residuals']) for sample in status['ward_samples'])
        checks.append(dict(name=model+': finest-time Ward check',passed=bool(check_value<2e-7),value=float(check_value),gate=2e-7))
        responses.append(dict(model=model,principal_run=model+'-sixteenth',
            primary_density_linear=features[0,:4].real.tolist(),primordial_density_response_per_zeta2=features[2,:4].real.tolist(),
            particular_density_response=features[3,:4].real.tolist(),
            particular_photon_flux_imaginary=features[3,4:7].imag.tolist(),particular_baryon_momentum_imaginary=features[3,10:13].imag.tolist(),
            primary_heavy_field=float(features[0,14].real),primordial_heavy_field_per_zeta2=float(features[2,14].real),particular_heavy_field=float(features[3,14].real),
            maximum_stored_constraint=float(np.max(principal['constraints'])),
            maximum_stored_screen_error=float(np.max(principal['screens'])),native_comparison=status['native_comparison']))
    failed=[row for row in previous['checks'] if not row['passed']]
    checks.append(dict(name='Four original coarse failures retained without changing the gate',passed=len(failed)==4 and all(row['gate']==.001 for row in failed)))
    differences={row['model']:row for row in responses}
    difference=np.array(differences['heavy']['particular_density_response'])-np.array(differences['cold']['particular_density_response'])
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,responses=responses,
        retained_coarse_failures=failed,additional_underresolved_comparisons=[dict(model=row['model'],comparison=row['comparison'],value=row['maximum_error'],gate=.001) for row in rows if not row['passes_original_gate']],
        heavy_minus_cold_particular_densities=difference.tolist(),
        principal_time_grid_subdivisions=16,principal_angular_maximum=6,principal_start_scale=1e-6,
        angular_and_start_tests_at_quarter_time_resolution=True,joint_finest_grid_error_not_certified=True,
        primordial_amplitude_unassigned=True,physical_model_scope_unchanged=True),__file__,inputs)
    print(json.dumps(dict(checks=checks,probe_errors=[dict(model=row['model'],comparison=row['comparison'],value=row['maximum_error']) for row in rows],responses=responses,heavy_minus_cold_particular_densities=difference.tolist())),flush=True)


if __name__=='__main__':
    main()
