from turnover_common import *


def main():
    modest()
    folder=ROOT/'results/turnover-comparison'
    folder.mkdir(parents=True,exist_ok=False)
    specification_path=BRANCH/'temperature-distortion-projection-20261012/results/projection/status.json'
    specification=json.loads(specification_path.read_text())['basis_specification']
    basis=infrared_ladder.ConsistentBasis(**specification)
    inputs=[specification_path,ROOT/'INVARIANT-INTERPOLATION.md']
    checks,summary=[],{}
    def test(name,value,limit):
        checks.append(dict(name=name,value=float(value),limit=limit,passed=bool(np.isfinite(value) and value<=limit)))
    rows={}
    for floor in [.1,.05,1e-5]:
        row,normalization=hard_row(basis,floor,384 if floor>1e-5 else 700)
        fine,unused=hard_row(basis,floor,768 if floor>1e-5 else 1400)
        rows[floor]=(row,normalization)
        test('Hard functional preserves temperature:'+str(floor),abs(row@basis.temperature-1),1e-12)
        test('Hard functional quadrature:'+str(floor),np.linalg.norm(row-fine)/np.linalg.norm(fine),1e-8)
    for model in ['heavy','cold']:
        paths={'old640':ROOT/'runs'/f'{model}-main640/prediction.npz',
            'old1280':ROOT/'runs'/f'{model}-main1280/prediction.npz',
            'oldwide':ROOT/'runs'/f'{model}-wide1280/prediction.npz',
            'lower':ROOT/'runs'/f'{model}-lower1280/prediction.npz',
            'hard005':ROOT/'runs'/f'{model}-hard005/prediction.npz',
            'oldcoarse':ROOT/'runs'/f'{model}-coarse1280/prediction.npz',
            'invariant':ROOT/'invariant-prediction/runs'/f'{model}-main1280/prediction.npz',
            'half':ROOT/'invariant-half-prediction/runs'/f'{model}-main1280/prediction.npz',
            'halfwide':ROOT/'invariant-half-prediction/runs'/f'{model}-wide1280/prediction.npz',
            'half_time2':ROOT/'invariant-half-time2-prediction/runs'/f'{model}-main1280/prediction.npz'}
        cases={}
        for name,path in paths.items():
            inputs.extend([path,path.parent/'status.json'])
            with np.load(path) as saved:
                cases[name]={key:saved[key].copy() for key in ['coordinate','predicted_residual','true_residual',
                    'core_measure','actual_power','predicted_power','predicted_core','true_core']}
        reference=cases['half_time2']
        weight=reference['core_measure']
        peak=np.sqrt(reference['actual_power'].max(axis=0))
        norm_history=lambda value:np.sqrt(np.einsum('i,nik,nik->nk',weight,value,value))
        comparisons={}
        for label,new,old in [('original_time','old1280','old640'),('lower_domain','old1280','lower'),
            ('upper_domain_old','old1280','oldwide'),('hard_driver_floor','old1280','hard005'),
            ('joint_original_discretization','old1280','oldcoarse'),
            ('invariant_spacing','half','invariant'),('invariant_time','half_time2','half'),
            ('invariant_upper_domain','half','halfwide')]:
            difference=norm_history(cases[new]['predicted_residual']-cases[old]['predicted_residual'])
            comparisons[label]=dict(maximum_over_saved_residual_peak=(difference.max(axis=0)/peak).tolist(),
                endpoint_over_saved_residual=(difference[-1]/np.sqrt(reference['actual_power'][-1])).tolist())
        test('Invariant time refinement within1percent of saved residual peak:'+model,
             max(comparisons['invariant_time']['maximum_over_saved_residual_peak'][:3]),.01)
        actual_path=PARENT/'results/kinetic-drive'/f'{model}-1024.npz'
        inputs.append(actual_path)
        with np.load(actual_path) as actual:
            test('Saved core target reproduces Stage110:'+model,
                np.max(abs(reference['actual_power']-actual['residual_power'][:,2])/np.maximum(actual['residual_power'][:,2].max(axis=0),1e-300)),1e-10)
        parts=[reference['predicted_residual'][:,:,index:index+2] for index in [11,13,15]]
        direct=reference['predicted_residual'][:,:,3:5]
        component_norm=sum(norm_history(part) for part in parts)
        test('Derived prediction retains direct54 component linearity:'+model,
            np.max(norm_history(direct-sum(parts))/np.maximum(component_norm.max(axis=0),1e-300)),1e-8)
        test('Predicted source54 residual obeys triangle inequality:'+model,
            np.max((norm_history(direct)-component_norm)/np.maximum(component_norm.max(axis=0),1e-300)),1e-12)
        budget=(component_norm[-1]/np.sqrt(reference['predicted_power'][-1,1:3])).tolist()
        baseline,window,dependencies=load_histories(model)
        inputs.extend(dependencies)
        profiles=np.stack([profile_at(float(coordinate),baseline,window) for coordinate in reference['coordinate']])
        beta_hard=np.einsum('i,nik->nk',rows[.1][0],profiles)
        beta_full=np.einsum('i,nik->nk',rows[1e-5][0],profiles)
        beta_difference=np.max(abs(beta_hard-beta_full),axis=0)
        slope_scale=np.maximum(np.max(abs(beta_full),axis=0),1e-300)
        latest=json.loads((paths['half_time2'].parent/'status.json').read_text())
        wide=json.loads((paths['halfwide'].parent/'status.json').read_text())
        summary[model]=dict(comparisons=comparisons,
            hard_driver_omitted_planck_weight=1-rows[.1][1]/rows[1e-5][1],
            hard_driver_vs_saved_full_functional_relative=(beta_difference/slope_scale).tolist(),
            predicted_source54_component_budget=budget,
            authoritative_metrics=latest['metrics'],wide_domain_metrics=wide['metrics'])
    spacing_controls={}
    for name in ['heavy-production','heavy-base']:
        path=TAIL/'runs'/name/'tail.npz'
        inputs.append(path)
        with np.load(path) as saved:
            spacing=math.log(saved['frequency'][1]/saved['frequency'][0])
            count=len(saved['offsets'])
            selected=saved['coefficient_knots']>=math.log(10)/2-1e-12
            bank=saved['coefficient_bank'][selected]
            defect=bank[:,:count]@np.exp(-saved['offsets']*spacing)+bank[:,count]
            spacing_controls[name]=dict(chemical_mode_over_lambda1_min=float(np.min(defect/bank[:,count])),
                chemical_mode_over_lambda1_max=float(np.max(defect/bank[:,count])))
    checks.append(dict(name='Original interpolation bias explicitly measured,not silently reused as exact physics',passed=True))
    finish(folder,dict(checks=checks,models=summary,old_chemical_mode_defect=spacing_controls,
        authoritative_case='invariant-half-time2-prediction/main1280 (actual2560 steps)',
        physical_cutoff_fitted=False,full_parent_histories_rerun=False,conditional_prediction=True,
        regenerated_soft_temperature_nodes=65,finite_frequency_source_sweep=False,
        future_core_values_used_in_evolution=False),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],
        models={model:dict(sensitivity=value['comparisons'],core_errors=value['authoritative_metrics']['residual_error_over_peak'][:3],
            endpoint_errors=value['authoritative_metrics']['endpoint_residual_error_relative'][:3],
            minima=value['authoritative_metrics']['predicted_minimum_epoch'][:3],
            slopes=value['authoritative_metrics']['predicted_to_actual_late_power_slope'][:3],
            omitted_weight=value['hard_driver_omitted_planck_weight']) for model,value in summary.items()})),flush=True)


if __name__=='__main__':
    main()
