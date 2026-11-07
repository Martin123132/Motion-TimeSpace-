from __future__ import annotations

from window_common import *
from build_response import convolved_basis
from test_compression import recover


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[];recoveries=[]
    def check(name,passed,value=None,limit=None):
        checks.append(dict(name=name,passed=bool(passed),value=value,limit=limit))
    sources=json.loads((ROOT/'sources/manifest.json').read_text())
    fits=json.loads((ROOT/'results/diagnostic-fits/status.json').read_text())
    compression=json.loads((ROOT/'results/compression-test/status.json').read_text())
    response=json.loads((ROOT/'results/response/status.json').read_text())
    for row in sources['records']:
        check('source_'+row['local_file'],digest(ROOT/'sources'/row['local_file'])==row['sha256'])
    for cap in ['NGC','SGC']:
        packet=np.load(ROOT/'results/prepared'/(cap+'.npz'))
        check(cap+'_full_covariance_SPD',min(linalg.eigvalsh(packet['covariance']))>0)
        rng=np.random.default_rng(5701)
        test_vector=rng.normal(size=1200)
        sequential=packet['window']@(packet['wide_angle']@test_vector)
        combined=packet['operator']@test_vector
        error=float(max(abs(sequential-combined)))
        check(cap+'_operator_order',error<1e-12,error,1e-12)
        indices=select()
        covariance=packet['covariance'][np.ix_(indices,indices)]
        chol=linalg.cholesky(covariance,lower=True)
        template=multipole_basis('lcdm',geom=geometry('lcdm'),template=True)
        basis=convolved_basis(template,packet['operator'])[:,indices]
        truth=(1.53,.437,321.)
        synthetic=physical_vector(basis,truth[0],truth[2],truth[1])
        recovered=recover(basis,synthetic,covariance)
        errors=[abs(recovered['B']/truth[0]-1),abs(recovered['F']/truth[1]-1),abs(recovered['noise']-truth[2])]
        check(cap+'_nonstart_template_recovery',errors[0]<1e-5 and errors[1]<1e-5 and errors[2]<.01,errors,[1e-5,1e-5,.01])
        check(cap+'_nonstart_injection_score',recovered['chi2_raw']<1e-10,recovered['chi2_raw'],1e-10)
        recoveries.append(dict(cap=cap,injected_B_F_N=truth,recovered=recovered))
        for label in ['heavy','cold','lcdm']:
            packet_response=np.load(ROOT/'results/response'/(label+'-'+cap+'.npz'))
            primary=next(row for row in fits['rows'] if row['branch']==label and row['cap']==cap and row['kmax']==.1 and row['ells']==[0,2])
            fit=primary['fit']
            basis_physical=packet_response['basis'][:,indices]
            synthetic=physical_vector(basis_physical,1.973,-217.)
            recovered_physical=fit_nuisance(basis_physical,synthetic,covariance)
            errors=[abs(recovered_physical['bias']/1.973-1),abs(recovered_physical['noise']+217)]
            check(label+'_'+cap+'_tracer_recovery',errors[0]<1e-5 and errors[1]<.01,errors,[1e-5,.01])
            residual=packet['data'][indices]-np.array(fit['prediction'])
            whitened=linalg.solve_triangular(chol,residual,lower=True)
            score=float(whitened@whitened)
            check(label+'_'+cap+'_independent_score',abs(score-fit['chi2_raw'])<1e-8,abs(score-fit['chi2_raw']),1e-8)
            grid=np.linspace(*BIAS_BOUNDS,501)
            grid_values=[]
            whitened_basis=linalg.solve_triangular(chol,basis_physical.T,lower=True).T
            data=linalg.solve_triangular(chol,packet['data'][indices],lower=True)
            for bias in grid:
                leftover=data-bias*bias*whitened_basis[0]-bias*whitened_basis[1]-whitened_basis[2]
                noise=np.clip(leftover@whitened_basis[3]/(whitened_basis[3]@whitened_basis[3]),*NOISE_BOUNDS)
                grid_values.append(float(np.sum((leftover-noise*whitened_basis[3])**2)))
            check(label+'_'+cap+'_profile_grid_minimum',score<=min(grid_values)+1e-8,score-min(grid_values),1e-8)
    for row in response['branches']:
        geom=row['geometry']
        mu=np.array([-.85,-.2,.15,.95]);wave=np.array([.005,.035,.1,.3])
        fid_hubble=100*math.sqrt(.31*(1+REDSHIFT)**3+.69)
        alpha_perp=geom['model_distance_Mpc']/geom['fiducial_distance_Mpc_over_h']
        alpha_parallel=fid_hubble/geom['model_H_km_s_Mpc']
        physical=wave*np.sqrt((1-mu**2)/alpha_perp**2+mu**2/alpha_parallel**2)
        scaled=HUNIT*wave*np.sqrt((1-mu**2)/geom['q_perp']**2+mu**2/geom['q_parallel']**2)
        check(row['branch']+'_AP_wave_unit_identity',np.allclose(physical,scaled,rtol=1e-14,atol=0))
        amplitude=1/(alpha_perp**2*alpha_parallel)
        scaled_amplitude=HUNIT**3/(geom['q_perp']**2*geom['q_parallel'])
        check(row['branch']+'_AP_volume_unit_identity',abs(amplitude/scaled_amplitude-1)<1e-14)
        check(row['branch']+'_analytic_Kaiser_limit',row['identity_kaiser_error']<1e-12,row['identity_kaiser_error'],1e-12)
    for row in fits['rows']:
        prefix=f"{row['branch']}_{row['cap']}_{row['kmax']}_{len(row['ells'])}"
        for variant in ['pchip_basis','angular32_basis']:
            value=row['numerical_and_ablated_distance'][variant]
            check(prefix+'_'+variant,value<.01,value,.01)
        check(prefix+'_no_nuisance_edge',not row['fit']['boundary_hit'])
        count=row['fit']['bins']
        expected=(NMOCK-count-2)/(NMOCK-1)
        check(prefix+'_Hartlap_dimension',row['fit']['hartlap_factor']==expected)
        check(prefix+'_no_model_selection',not row['formal_model_selection'])
    for row in compression['rows']:
        prefix=f"{row['branch']}_{row['cap']}_{row['kmax']}"
        check(prefix+'_compression_converged',row['field_injection']['converged'] and not row['field_injection']['boundary_hit'])
    check('no_Stage56_double_count',fits['covariance_not_added_to_stage56'])
    check('nonlinear_limit_visible',not fits['nonlinear_model_validated'] and not fits['formal_model_selection'])
    check('compression_not_observed_growth_fit',not compression['observational_growth_fitted'])
    check('negative_window_control_detectable',max(row['numerical_and_ablated_distance']['no_window_basis'] for row in fits['rows'])>.1)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
        nonstart_injection_recovery=recoveries,
        scope='Data/response/units/optimizer checks, not proof that linear nuisance model describes all measured clustering.'),
        __file__,[ROOT/'test_compression.py',ROOT/'build_response.py',ROOT/'results/prepared/status.json',
            ROOT/'results/response/status.json',ROOT/'results/diagnostic-fits/status.json',ROOT/'results/compression-test/status.json',ROOT/'sources/manifest.json'])
    print(json.dumps(dict(count=len(checks),failed=[row for row in checks if not row['passed']]),indent=2))
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
