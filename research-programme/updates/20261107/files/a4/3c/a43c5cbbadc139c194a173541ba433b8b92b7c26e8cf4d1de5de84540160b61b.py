from __future__ import annotations

from spectrum_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]

    def check(name,passed,value=None,limit=None):
        checks.append(dict(name=name,passed=bool(passed),value=value,limit=limit))

    def report(relative):
        return json.loads((ROOT/relative).read_text())

    projection=report('runs/projection/status.json')
    spectrum=report('results/spectrum/status.json')
    screen=report('results/growth-screen/status.json')
    sources=report('sources/sdss-growth/status.json')
    check('parent_native_loaded_read_only',Path(camb.__file__).resolve().is_relative_to(PARENT/'native'))
    check('nested_grid',np.isin(modes(1),modes(2)).all())
    check('all_modes_sourced',projection['sourced_all_modes'] and not projection['interpolated_matching_rows'])
    for config in projection['configurations']:
        table=np.load(ROOT/'runs/projection'/(config['label']+'.npz'))
        mask=table['modes']<=5
        maximum=float(max(table['closure_error'][mask]))
        check(config['label']+'_qualified_pressure',maximum<2e-6,maximum,2e-6)
        check(config['label']+'_full_grid_finite',all(np.isfinite(table[key]).all() for key in table.files))
        for row in config['anchors']:
            maximum=max(row['delta_change_over_mode_norm'],row['momentum_change_over_mode_norm'])
            check(config['label']+'_anchor_'+str(row['k']),maximum<1e-5,maximum,1e-5)
    check('failed_tail_gate_explicitly_retained',any(row['modes_above_inherited_pressure_gate'] for row in projection['configurations']))
    for branch in spectrum['branches']:
        label=branch['label']
        status=report('runs/'+label+'/status.json')
        check(label+'_complete',status['state']=='complete' and status['completed']==len(modes(2)))
        output=load_evolution(label)
        expected=1 if status['arguments']['branch']=='heavy' else 0
        counts=output['values'][:,-1,output['names'].index('mts_match_count')]
        check(label+'_event_count',np.all(counts==expected))
        maximum=float(np.max(abs(output['values'][:,:,output['names'].index('mts_nonheavy_change')])))
        check(label+'_all_other_states_preserved',maximum==0,maximum,0)
        check(label+'_primary_cutoff',branch['integral_cutoff_Mpc_inverse']==5.)
        for name,metrics in branch['maximum_fractional_changes'].items():
            for metric,value in metrics.items():
                check(label+'_'+name+'_'+metric,value<.002,value,.002)
        maximum=max(row['derivative_step_change'] for row in branch['central'])
        check(label+'_time_derivative_stencil',maximum<1e-4,maximum,1e-4)
        maximum=max(row['fsigma8_cb_m']/row['velocity_sigma8_cb']-1 for row in branch['central'])
        check(label+'_velocity_density_Cauchy_Schwarz',maximum<1e-8,maximum,1e-8)
    for control in screen['native_control_checks']:
        for name in ['sigma8_max_relative_error','fsigma8_max_relative_error']:
            check(control['branch']+'_native_'+name,control[name]<.002,control[name],.002)
    for row in screen['matching_variations']:
        for name in ['sigma8_max_change','growth_max_change']:
            check(row['label']+'_'+name,row[name]<.002,row[name],.002)
    for row in sources['source_records']:
        check('source_hash_'+row['item_id'],digest(ROOT/'sources/sdss-growth'/row['item_id'])==row['sha256'])
    covariance=np.load(ROOT/'sources/sdss-growth/growth-only.npz')['covariance']
    check('growth_covariance_symmetric',np.allclose(covariance,covariance.T,rtol=0,atol=1e-12))
    check('growth_covariance_positive',min(np.linalg.eigvalsh(covariance))>0)
    check('four_unique_growth_bins',len(set(screen['data_redshifts']))==screen['number_of_observations']==4)
    check('no_statistical_preference_claim',not screen['formal_model_preference'] and screen['free_parameters_fitted']==0)
    check('mapping_limits_explicit',all(not value['claim_valid_as_general_MTS_likelihood'] for row in screen['rows'] for value in row['mappings']))
    prior=json.loads((PARENT/'results/late-comparison/status.json').read_text())
    heavy=np.load(ROOT/'results/spectrum/heavy.npz')
    cold=np.load(ROOT/'results/spectrum/cold.npz')
    ratio=heavy['linear_power_Mpc3'][:,-1]/cold['linear_power_Mpc3'][:,-1]
    for row in prior['rows']:
        index=int(np.argmin(abs(heavy['modes']-row['k_Mpc_inverse'])))
        error=float(abs(ratio[index]/row['power_ratio_heavy_to_slow_cold']-1))
        check('stage55_power_anchor_'+str(row['k_Mpc_inverse']),error<1e-4,error,1e-4)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
        admission_scope='Qualified k<=5 band and common finite integral; exploratory high-k pressure failures retained, not counted as passes.',
        observational_score_scope='Conditional screening with actual marginal covariance; no automatic validation of the survey compression for MTS.'),
        __file__,[ROOT/'runs/projection/status.json',ROOT/'results/spectrum/status.json',ROOT/'results/growth-screen/status.json',
            ROOT/'sources/sdss-growth/status.json',PARENT/'results/late-comparison/status.json',ROOT/'ACCEPTANCE.md'])
    print(json.dumps(dict(count=len(checks),failed=[row for row in checks if not row['passed']]),indent=2))
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
