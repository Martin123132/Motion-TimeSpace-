from matched_feedback_common import *


def main():
    modest()
    folder=ROOT/'results/comparison'
    folder.mkdir(parents=True,exist_ok=False)
    names=['fine-q16-m40-n1024','fine-q24-m40-n1024','fine-q32-m40-n1024',
           'fine-q32-m40-n512','fine-q32-m20-n1024','time-q32-m40-n1024','space-q32-m40-n1024']
    checks,inputs,models=[],[],{}
    def test(name,value,limit):
        checks.append(dict(name=name,value=float(value),limit=limit,passed=bool(np.isfinite(value) and value<=limit)))
    for model in ['heavy','cold']:
        packets={}
        for name in names:
            path=ROOT/'results'/('response-'+name)/(model+'.npz')
            inputs.extend([path,path.parent/'status.json'])
            with np.load(path) as archive:
                packets[name]={key:archive[key].copy() for key in ['physical_change','saved_potential','measure','residual_change','saved_residual','gas','photon','unresolved_change']}
        reference=packets['fine-q32-m40-n1024']
        norm=lambda value:np.sqrt(np.sum(reference['measure'][:,None]*value**2,axis=0))
        original=norm(reference['saved_potential'])
        new=norm(reference['physical_change'])
        residual=norm(reference['saved_residual'])
        comparisons={}
        for label,fine,coarse in [
                ('quadrature16to24','fine-q24-m40-n1024','fine-q16-m40-n1024'),
                ('quadrature24to32','fine-q32-m40-n1024','fine-q24-m40-n1024'),
                ('response_time512to1024','fine-q32-m40-n1024','fine-q32-m40-n512'),
                ('matching_upper04to02','fine-q32-m40-n1024','fine-q32-m20-n1024'),
                ('inherited_tail_time','fine-q32-m40-n1024','time-q32-m40-n1024'),
                ('inherited_tail_spacing','fine-q32-m40-n1024','space-q32-m40-n1024')]:
            difference=norm(packets[fine]['physical_change']-packets[coarse]['physical_change'])
            residual_difference=norm(packets[fine]['residual_change']-packets[coarse]['residual_change'])
            comparisons[label]=dict(final_change_over_saved_norm=(difference/original).tolist(),
                change_over_new_response=(difference/np.maximum(new,1e-300)).tolist(),
                residual_change_over_saved_residual=(residual_difference/residual).tolist(),
                gas_difference=abs(packets[fine]['gas'][-1,:3]-packets[coarse]['gas'][-1,:3]).tolist())
            if label in ['quadrature24to32','response_time512to1024']:
                test(label+' within frozen1percent of saved spectrum:'+model,max(difference/original),.01)
        best_status=ROOT/'results/response-fine-q32-m40-n1024/status.json'
        metrics=json.loads(best_status.read_text())['models'][model]['metrics']
        component=np.array(metrics['resolved_component_norms'])
        total=np.array(metrics['final_physical_change_norm'])
        unresolved=np.array(metrics['final_unresolved_norm'])
        test('Paired component plus unresolved triangle bound:'+model,
            np.max((total-component.sum(axis=0)-unresolved)/original),1e-12)
        max_source_error=0.
        for variant in ['fine-q16-m40','fine-q24-m40','fine-q32-m40','fine-q32-m20','time-q32-m40','space-q32-m40']:
            path=ROOT/'results'/('sources-'+variant)/(model+'.npz')
            inputs.append(path)
            with np.load(path) as archive:
                expected=archive['raw_source']-archive['overlap_source']
                scale=np.maximum(np.max(abs(archive['raw_source'])+abs(archive['overlap_source'])),1e-300)
                max_source_error=max(max_source_error,float(np.max(abs(archive['source']-expected))/scale))
                assert np.count_nonzero(archive['source'][0])==0
        test('Replacement minus overlap exactly once:'+model,max_source_error,1e-14)
        models[model]=dict(authoritative_metrics=metrics,comparisons=comparisons,
            compton_component_over_total=(component[0]/total).tolist(),
            source54_budget_not_recomputed=True,continuum_precision_of_net_response_established=False,
            matching_or_spacing_dominates_quadrature=bool(
                max(comparisons['inherited_tail_spacing']['final_change_over_saved_norm'])>
                max(comparisons['quadrature24to32']['final_change_over_saved_norm'])))
    finish(folder,dict(checks=checks,models=models,finest_rule='fine-q32-m40-n1024',
        fitted_cutoff=False,physical_response_is_conditional=True,
        full_finite_frequency_compton_matching_complete=False),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],
        models={model:dict(relative_change=value['authoritative_metrics']['final_photon_change_over_saved_norm'],
                          sensitivities=value['comparisons']) for model,value in models.items()})),flush=True)


if __name__=='__main__':
    main()
