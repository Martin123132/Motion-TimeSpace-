from evolution_common import *


def feature_errors(left,right):
    groups=[('cold_density',slice(0,1)),('baryon_density',slice(1,2)),('photon_density',slice(2,3)),('neutrino_density',slice(3,4)),
        ('photon_flux',slice(4,7)),('neutrino_flux',slice(7,10)),('baryon_momentum',slice(10,13)),
        ('slow_field',slice(13,14)),('heavy_field',slice(14,15)),('slow_prime',slice(15,16)),('heavy_prime',slice(16,17)),('metric_trace_rate',slice(17,18))]
    output=[]
    for block in range(4):
        for name,indices in groups:
            first=left[block,indices]
            second=right[block,indices]
            error=float(np.linalg.norm(first-second)/max(np.linalg.norm(first),np.linalg.norm(second),1e-100))
            output.append(dict(block=block,observable=name,relative_error=error))
    return output


def main():
    modest()
    folder=ROOT/'results/refinements'
    folder.mkdir(parents=True,exist_ok=True)
    assert not (folder/'COMPLETE').exists()
    checks=[]
    inputs=[]
    rows=[]
    responses=[]
    for model in ['heavy','cold']:
        packets={}
        for name in ['base','half','quarter','angular','earlier']:
            path=ROOT/'runs'/(model+'-'+name)/'evolution.npz'
            packets[name]=np.load(path)
            inputs.append(path)
            inputs.append(path.parent/'status.json')
        for name,first,second in [('all_steps_halved','base','half'),('all_steps_quartered','half','quarter'),('angular_6_to_8','quarter','angular'),('start_twice_earlier','angular','earlier')]:
            errors=feature_errors(packets[first]['features'][-1],packets[second]['features'][-1])
            maximum=max(row['relative_error'] for row in errors)
            checks.append(dict(name=model+': '+name,passed=maximum<.001,value=maximum,gate=.001))
            rows.append(dict(model=model,comparison=name,maximum_error=maximum,observables=errors))
        principal=packets['earlier']
        final=principal['features'][-1]
        responses.append(dict(model=model,
            primary_density_linear=final[0,:4].real.tolist(),primordial_density_response_per_zeta2=final[2,:4].real.tolist(),
            particular_density_response=final[3,:4].real.tolist(),
            primary_heavy_field=float(final[0,14].real),primordial_heavy_field_per_zeta2=float(final[2,14].real),particular_heavy_field=float(final[3,14].real),
            maximum_stored_constraint=float(np.max(principal['constraints'])),
            maximum_stored_screen_error=float(np.max(principal['screens']))))
        check_report=json.loads((ROOT/'runs'/(model+'-earlier')/'status.json').read_text())
        check_value=max(np.max(sample['residuals']) for sample in check_report['ward_samples'])
        checks.append(dict(name=model+': endpoint/intermediate Ward check',passed=bool(check_value<2e-7),value=float(check_value),gate=2e-7))
    differences={row['model']:row for row in responses}
    difference=(np.array(differences['heavy']['particular_density_response'])-np.array(differences['cold']['particular_density_response']))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,responses=responses,
        heavy_minus_cold_particular_densities=difference.tolist(),
        cold_not_fitted_to_match_heavy=True,primordial_amplitude_unassigned=True,
        comparisons_are_endpoint_envelopes_not_uniform_error_theorems=True),__file__,inputs)
    print(json.dumps(dict(checks=checks,responses=responses,heavy_minus_cold_particular_densities=difference.tolist())),flush=True)


if __name__=='__main__':
    main()
