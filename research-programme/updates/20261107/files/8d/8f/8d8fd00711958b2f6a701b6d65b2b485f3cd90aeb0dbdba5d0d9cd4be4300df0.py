from __future__ import annotations

from feedback_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    def check(name,passed,measured=None):
        checks.append(dict(name=name,passed=bool(passed),measured=measured))
    derivation=json.loads((ROOT/'results/derivation/status.json').read_text())
    kernels=json.loads((ROOT/'results/mode-kernels/status.json').read_text())
    feedback=json.loads((ROOT/'results/feedback/status.json').read_text())
    projection=json.loads((ROOT/'results/source-projection/status.json').read_text())
    for packet in [derivation,kernels]:
        for row in packet['checks']:
            check(row['name'],row['passed'],row['residual'])
    check('all nine common branch/wavenumber cases present',
        {(row['branch'],row['k_Mpc_inverse']) for row in feedback['rows']}==
        {(label,wave) for label in ['heavy','cold','lcdm'] for wave in [.03,.1,1.]})
    for row in feedback['rows']:
        tag=row['branch']+' k='+str(row['k_Mpc_inverse'])
        check(tag+' same declared native linear gate',row['max_native_linear_relative_error']<.005,row['max_native_linear_relative_error'])
        check(tag+' tight-loose integration gate',row['integration_change']<1e-7,row['integration_change'])
        check(tag+' background interpolation gate',row['interpolation_quadratic_fraction']<.001,row['interpolation_quadratic_fraction'])
        check(tag+' no complete second-order native claim',not row['full_native_second_order'])
        packet=np.load(ROOT/'results/feedback'/(row['branch']+'-'+str(row['k_Mpc_inverse'])+'.npz'))
        initial=packet['initial'].reshape(4,-1)
        check(tag+' second-order initial condition explicitly zero',np.all(initial[2:]==0))
        check(tag+' resolved state finite',np.isfinite(packet['state']).all())
        check(tag+' c and b not merged',row['species'][:2]==['cdm','baryon'])
        if row['branch']=='heavy':
            check(tag+' inherited mass and slow-envelope regime',row['heavy_mass_Mpc_inverse']>0 and row['max_kappa']<1e-3 and row['max_H_over_M']<1e-6)
        else:
            check(tag+' zero quantum response in cold limit',row['max_pressure_lambda']==0 and row['omitted_quantum_source_endpoint_change']==0)
    for wave in [.03,.1,1.]:
        norms=[row['common_normalization'] for row in feedback['rows'] if row['k_Mpc_inverse']==wave]
        check('common amplitude normalization k='+str(wave),len(set(norms))==1 and norms[0]>0)
    for row in feedback['analytic_controls']:
        check(row['name'],row['error']<1e-10,row['error'])
    for row in feedback['periodic_checks']:
        tag=row['branch']+' A='+str(row['amplitude'])+' N='+str(row['count'])
        check(tag+' positive density',row['min_density_seen']>0,row['min_density_seen'])
        check(tag+' mass conservation',row['max_mass_error']<1e-10,row['max_mass_error'])
        check(tag+' full nonlinear versus quadratic coefficient',row['max_coefficient_error']<.002,row['max_coefficient_error'])
    for label in ['heavy','cold','lcdm','quantum-sensitive control']:
        rows=[row for row in feedback['periodic_checks'] if row['branch']==label]
        coarse=next(row for row in rows if row['amplitude']==.02)
        small=next(row for row in rows if row['amplitude']==.01 and row['count']==64)
        fine=next(row for row in rows if row['count']==128)
        ratio=coarse['max_coefficient_error']/small['max_coefficient_error']
        check(label+' amplitude convergence approximately fourth order in raw harmonic',3.5<ratio<4.5,ratio)
        spread=max(np.max(abs(np.array(small[key])-fine[key])) for key in ['second_density','second_velocity'])
        check(label+' spatial resolution gate',spread<1e-6,float(spread))
        if label=='quantum-sensitive control':
            check('removing derived quadratic quantum source fails negative control',
                fine['omitted_quantum_source_error']>.01 and fine['omitted_quantum_source_error']>1000*fine['max_coefficient_error'],
                fine['omitted_quantum_source_error'])
    for row in projection['phase_rows']:
        check('canonical phase average case '+str(row['case'])+' N='+str(row['count']),
            row['max_absolute_error']<1e-14 and abs(row['trace'])<1e-14,row['max_absolute_error'])
    check('Hilbert source not replaced by improved fluid flux',projection['hilbert_momentum_flux_improvement_not_used_as_gravity_source'])
    check('no observational refit or fitted coefficients',not feedback['actual_survey_refit'] and feedback['new_parameters_fitted']==0)
    source_paths=[]
    for row in projection['source_records']:
        path=Path(row['path'])
        check('archived source '+row['url'],path.is_file() and digest(path)==row['sha256'] and row['bytes']>500)
        source_paths.append(path)
    success=all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=success,
        identity_count_included_not_additive=derivation['count']+kernels['count'],
        full_native_second_order_validated=False),
        __file__,[ROOT/'results'/name/'status.json' for name in ['derivation','mode-kernels','feedback','source-projection']]+source_paths)
    print(json.dumps(dict(state='complete',checks=len(checks),all_checks_passed=success,
        failures=[row for row in checks if not row['passed']])))
    assert success


if __name__=='__main__':
    main()
