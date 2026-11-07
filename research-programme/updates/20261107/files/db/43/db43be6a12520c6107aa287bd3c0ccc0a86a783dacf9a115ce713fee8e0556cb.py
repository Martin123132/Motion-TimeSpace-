from source201 import *
from assess201 import COMPONENTS, norms, subtract


def main():
    selected=ROOT/'precision-representation'
    initial=read(ROOT/'results/source-assessment.json')
    repaired=read(selected/'results/source-assessment.json')
    assert digest(ROOT/'results/x14-source.npz')==initial['result_sha256']
    assert digest(selected/'results/x14-source.npz')==repaired['result_sha256']
    before=packet(ROOT/'results/x14-source.npz')
    after=packet(selected/'results/x14-source.npz')
    bundle,unused=source.context(.90625)
    factor=linear.cholesky(bundle.basis.mass,lower=True)
    records=[]
    for field in ('absolute','delta','prediction'):
        previous_pair=(before[field+'_high'],before[field+'_low'])
        current_pair=(after[field+'_high'],after[field+'_low'])
        difference=subtract(current_pair,previous_pair)
        for measure,operation in [('photon',lambda values:norms(values,factor)),('gas',lambda values:abs(values[...,-1,:]))]:
            denominator=operation(current_pair[0]+current_pair[1])
            relative=operation(difference[0]+difference[1])/np.maximum(denominator,1e-300)
            for group,component,column in np.ndindex(relative.shape):
                records.append(dict(field=field,group=group,component=COMPONENTS[component],
                    model=('heavy','cold')[column//2],join=column%2,measure=measure,
                    relative=float(relative[group,component,column])))
    write(ROOT/'results/representation-comparison.json',dict(records=records,
        initial_result_sha256=initial['result_sha256'],selected_result_sha256=repaired['result_sha256'],
        diagnostics_only=True,new_acceptance_tolerance_added=False,
        maxima={field:max(row['relative'] for row in records if row['field']==field)
                for field in ('absolute','delta','prediction')}))
    print(json.dumps(dict(maxima={field:max(row['relative'] for row in records if row['field']==field)
                for field in ('absolute','delta','prediction')})),flush=True)


if __name__=='__main__':
    source.modest()
    main()
