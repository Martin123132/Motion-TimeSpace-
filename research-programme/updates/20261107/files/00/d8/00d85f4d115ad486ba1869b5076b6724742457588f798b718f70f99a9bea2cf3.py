from lift214 import np,mp,source,owner,precise,cached,OperatorBundle,ACTIVE
from node214 import matrix_sum


def evaluators(original):
    bundle=OperatorBundle(cached.CachedFeatures(original),original.inputs)
    return bundle,cached.models(bundle)


def evaluate_event(parameters,bundle,models,virtual_scalar,event_weight):
    previous=source.physics.precise_state
    try:
        source.physics.precise_state=precise.precise_state
        with mp.workdps(60):
            high,low,diagnostics=owner.microscopic.weighted(parameters,bundle,models,virtual_scalar,event_weight)
            assert mp.mp.dps==60
    finally:
        source.physics.precise_state=previous
    arrays=tuple(np.moveaxis(values,0,2).reshape(6,98,98,2) for values in (high,low))
    assert all(np.all(values[:,:,97,:]==0) for values in arrays)
    return tuple(values[:,:,:97,:] for values in arrays),diagnostics


def sum_events(event_matrices):
    return matrix_sum(event_matrices)


def apply_coefficients(matrix,coefficients,join,digits=80):
    high,low=map(np.asarray,matrix)
    coefficient_high,coefficient_low=map(np.asarray,coefficients)
    if high.shape!=(6,98,97,2) or low.shape!=high.shape:
        raise ValueError('Expected a (6,98,97,2) compensated operator.')
    if coefficient_high.ndim!=2 or coefficient_high.shape[0]!=97 or coefficient_low.shape!=coefficient_high.shape:
        raise ValueError('Expected two (97,N) coefficient arrays, with no tail-repair coordinates.')
    if join not in (0,1) or digits<80:
        raise ValueError('Use a retained join (0 or 1) and at least80 decimal digits.')
    if not all(np.isfinite(values).all() for values in (high,low,coefficient_high,coefficient_low)):
        raise ValueError('Operator and coefficients must be finite.')
    output_high=np.zeros((6,98,coefficient_high.shape[1]))
    output_low=np.zeros_like(output_high)
    with mp.workdps(digits):
        vectors=[[mp.mpf(float(coefficient_high[index,column]))+mp.mpf(float(coefficient_low[index,column])) for index in range(97)]
                 for column in range(coefficient_high.shape[1])]
        for component,row in np.ndindex(6,98):
            entries=[mp.mpf(float(high[component,row,index,join]))+mp.mpf(float(low[component,row,index,join])) for index in range(97)]
            for column,vector in enumerate(vectors):
                exact=mp.fsum(left*right for left,right in zip(entries,vector))
                output_high[component,row,column]=float(exact)
                output_low[component,row,column]=float(exact-mp.mpf(float(exact)))
    return output_high,output_low
