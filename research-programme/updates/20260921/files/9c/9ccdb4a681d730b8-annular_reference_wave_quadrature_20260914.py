import numpy as np

from annular_finite_width_bulk_current_20260913 import shape_weight


def root_split_variation_norm(system, velocity, order=12):
    coefficients = system.grid.coefficients(system.unpack(velocity)[0])
    free = len(system.radii)-1
    points, weights = np.polynomial.legendre.leggauss(order)
    integral, segments = 0.,0
    for center,part in zip([-.25,.25],coefficients):
        scalar = np.column_stack([part[:,:free],np.zeros(len(part))])
        differences = np.diff(scalar,n=2,axis=1)/system.spacing
        endpoints = [-1.,1.]
        for column in differences.T:
            if np.max(abs(column))>0:
                roots = np.polynomial.chebyshev.chebroots(column)
                endpoints.extend(float(root.real) for root in roots if abs(root.imag)<1e-8 and -1<root.real<1)
        endpoints = np.unique(endpoints)
        lower,upper = endpoints[:-1],endpoints[1:]
        selected = upper-lower>1e-14
        lower,upper = lower[selected],upper[selected]
        locations = ((lower+upper)[:,None]/2+(upper-lower)[:,None]*points/2).reshape(-1)
        integration = (.25*(upper-lower)[:,None]*weights/2).reshape(-1)
        variation = np.sum(abs(np.polynomial.chebyshev.chebval(locations,differences)),axis=0)
        integral += float(integration @ (shape_weight(center+.25*locations,system.shape)*variation**2))
        segments += len(lower)
    return float(np.sqrt(integral)),segments

