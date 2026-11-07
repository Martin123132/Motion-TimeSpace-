from response221 import *


def budget():
    protocol();rows=[];records=[]
    for method,directory in [('original',ROOT),('causal_startup',ROOT/'causal-startup')]:
        for model in MODELS:
            fine=packet(directory/f'responses/{model}-4096/increment-readout.npz')
            coarse=packet(directory/f'responses/{model}-2048/increment-readout.npz')
            for profile,field,join in [(profile,field,join) for profile in (0,1) for field in ('gas','energy','residual') for join in (0,1)]:
                def select(values,grid,component):
                    column=np.ravel_multi_index((profile,grid,component,join),(2,3,6,2))
                    return values[field][...,column]
                def measure(values):
                    return float(np.sqrt(np.sum(fine['measure']*values**2))) if field=='residual' else float(abs(values))
                baseline=select(fine,1,0);mts=select(fine,1,4);total=select(fine,1,5)
                scale=max(measure(total),1e-300)
                kappa=(measure(baseline)+measure(mts))/scale
                for kind,alternative,grid in [('history',fine,0),('response',coarse,1)]:
                    other_baseline=select(alternative,grid,0);other_mts=select(alternative,grid,4);other_total=select(alternative,grid,5)
                    component_bound=measure(other_baseline-baseline)+measure(other_mts-mts)
                    representation_bound=measure(total-baseline-mts)+measure(other_total-other_baseline-other_mts)
                    difference=measure(other_total-total)
                    upper=component_bound+representation_bound
                    excess=max(difference-upper,0)/max(upper,1e-300)
                    check(rows,f'{method}:{model}:{profile}:{field}:{join}:{kind}:triangle budget',excess,1e-10,'identity')
                    records.append(dict(method=method,model=model,profile=PROFILES[profile],field=field,join=join,comparison=kind,
                        condition_factor=kappa,observed_relative=difference/scale,component_triangle_relative=component_bound/scale,
                        representation_remainder_relative=representation_bound/scale,full_difference_bound_relative=upper/scale,
                        sufficient_component_relative_for_one_percent=.01/max(kappa,1e-300),
                        total_reference_magnitude=measure(total),baseline_reference_magnitude=measure(baseline),MTS_reference_magnitude=measure(mts)))
    write(ROOT/'results/cancellation-budget.json',dict(checks=rows,failed_checks=[row for row in rows if not row['passed']],records=records,
        true_continuum_error_certified=False,scope='Algebraic bounds on observed discrete differences and sufficient component-accuracy targets, not bounds on uncomputed continuum errors.'))
    print(json.dumps(dict(checks=len(rows),failed=sum(not row['passed'] for row in rows),
        worst_condition=max(row['condition_factor'] for row in records),
        smallest_component_target=min(row['sufficient_component_relative_for_one_percent'] for row in records))),flush=True)


if __name__=='__main__':
    source.modest()
    budget()
