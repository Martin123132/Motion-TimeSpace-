from quadrature_common import *


def paired_difference(basis,frequency,ratios):
    frequency=np.asarray(frequency)
    ratios=np.asarray(ratios)
    base=basis.evaluate(frequency)
    compact=(frequency-basis.pivot)/(frequency+basis.pivot)
    ratio=ratios[:,None]
    delta=ratio-1.
    positive_shift=2*basis.pivot*frequency[None,:]*delta/((ratio*frequency+basis.pivot)*(frequency+basis.pivot))
    negative_shift=-2*basis.pivot*frequency[None,:]*delta/((frequency+basis.pivot*ratio)*(frequency+basis.pivot))
    paired_shift=2*basis.pivot**2*frequency[None,:]*delta**2*(ratio+1)/(
        (frequency+basis.pivot)*ratio*(ratio*frequency+basis.pivot)*(frequency+basis.pivot*ratio))
    shape=(len(ratios),len(frequency),basis.count)
    positive=np.zeros(shape)
    negative=np.zeros(shape)
    paired=np.zeros(shape)
    positive[:,:,1]=frequency[None,:]*delta/basis.norms[1]
    negative[:,:,1]=-frequency[None,:]*delta/(ratio*basis.norms[1])
    paired[:,:,1]=frequency[None,:]*delta**2*(ratio+1)/(ratio**2*basis.norms[1])
    for degree in range(2,basis.count):
        positive_value=(compact+positive_shift)*positive[:,:,degree-1]+positive_shift*base[None,:,degree-1]
        negative_value=(compact+negative_shift)*negative[:,:,degree-1]+negative_shift*base[None,:,degree-1]
        paired_value=compact*paired[:,:,degree-1]+positive_shift*positive[:,:,degree-1]
        paired_value+=negative_shift*negative[:,:,degree-1]/ratio+paired_shift*base[None,:,degree-1]
        for repeat in range(2):
            projection=basis.projections[degree,repeat,:degree]
            positive_value-=positive[:,:,:degree]@projection
            negative_value-=negative[:,:,:degree]@projection
            paired_value-=paired[:,:,:degree]@projection
        positive[:,:,degree]=positive_value/basis.norms[degree]
        negative[:,:,degree]=negative_value/basis.norms[degree]
        paired[:,:,degree]=paired_value/basis.norms[degree]
    return paired


def stable_adjoint(basis,frequency,weights,ratios,rates,chunk=32):
    result=np.zeros((len(frequency),basis.count))
    crossing_count=0
    weighted_crossing=0.
    total_weight=0.
    shifted_min=float('inf')
    shifted_max=0.
    for start in range(0,len(ratios),chunk):
        ratio=ratios[start:start+chunk]
        kernel=rates[start:start+chunk]/ratio
        paired=paired_difference(basis,frequency,ratio)
        result+=np.einsum('e,efk->fk',kernel,paired)
        forward=ratio[:,None]*frequency
        backward=frequency/ratio[:,None]
        outside=(forward<basis.minimum)|(forward>basis.maximum)|(backward<basis.minimum)|(backward>basis.maximum)
        crossing_count+=int(np.count_nonzero(outside))
        integration_weight=kernel[:,None]*weights
        weighted_crossing+=float(np.sum(integration_weight*outside))
        total_weight+=float(np.sum(integration_weight))
        shifted_min=min(shifted_min,float(forward.min()),float(backward.min()))
        shifted_max=max(shifted_max,float(forward.max()),float(backward.max()))
    moment=float(np.sum(rates*(ratios-1)**2*(ratios+1)/ratios**3))
    expected=frequency*moment
    raw_energy_error=float(np.linalg.norm(result@basis.temperature-expected)/np.linalg.norm(expected))
    result[:,0]=0.
    result[:,1]=expected/basis.norms[1]
    diagnostics=dict(raw_energy_error=raw_energy_error,domain_crossing_pairs=crossing_count,
        domain_pair_count=len(ratios)*len(frequency),positive_weight_crossing_fraction=weighted_crossing/total_weight,
        shifted_frequency_min=shifted_min,shifted_frequency_max=shifted_max,
        basis_evaluation_extrapolates_not_clips=True)
    return result.T*weights/(2*I3),moment,diagnostics
