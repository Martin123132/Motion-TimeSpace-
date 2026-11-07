import numpy as np
from scipy.sparse import diags, vstack, coo_matrix
from annular_compatible_current_restoring_20260909 import unit_gram_template
from annular_moving_collar_action_20260914 import MovingCollarAction
from annular_dynamical_source_20260914 import outgoing_profile


def sparse_factors(count,include_gram):
    base=diags([-np.ones(count-1),np.ones(count-1)],[0,1],shape=(count-1,count),format='csr')
    sampling=diags([np.full(count-1,.5),np.full(count-1,.5)],[0,1],shape=(count-1,count),format='csr')
    if not include_gram:
        return base,sampling
    margin,adjacent,extras=unit_gram_template(count)
    differences=diags([np.full(count-3,value) for value in [-1,3,-3,1]],
                       [0,1,2,3],shape=(count-3,count),format='csr')
    rows=[diags(np.sqrt(margin)) @ differences,
          diags(np.sqrt(abs(adjacent))) @ (differences[:-1]+diags(np.sign(adjacent)) @ differences[1:])]
    locations=list(np.arange(count-3)+1.5)
    locations.extend(np.arange(count-4)+2.)
    for first,second,weight in extras:
        rows.append(np.sqrt(abs(weight))*(differences[first]+np.sign(weight)*differences[second]))
        locations.append((first+second)/2+1.5)
    locations=np.asarray(locations)
    left=np.floor(locations).astype(int)
    fraction=locations-left
    indices=np.arange(len(locations))
    extra_sampling=coo_matrix((np.concatenate([1-fraction,fraction]),
                               (np.concatenate([indices,indices]),np.concatenate([left,left+1]))),
                              shape=(len(locations),count)).tocsr()
    return vstack([base,*rows],format='csr'),vstack([sampling,extra_sampling],format='csr')


class SparseMovingCollarAction(MovingCollarAction):
    def __init__(self,count,include_gram=False,offsets=(0.,),weights=(1.,),amplitude=.01,
                 source_mass=.003,inner_radius=3.,initial_radius=6.):
        if count<17:
            raise ValueError('At least17 nodes required.')
        self.count=count
        self.free=count-1
        self.gram=bool(include_gram)
        self.coordinate=np.linspace(0.,1.,count)
        self.reference_spacing=1/(count-1)
        self.trapezoid=np.full(count,self.reference_spacing)
        self.trapezoid[[0,-1]]/=2
        self.width=(initial_radius-inner_radius)*self.reference_spacing/2
        self.offsets=np.asarray(offsets,dtype=float)
        self.weights=np.asarray(weights,dtype=float)
        if len(self.offsets)!=len(self.weights) or np.any(self.weights<=0) or abs(sum(self.weights)-1)>1e-12:
            raise ValueError('Positive normalized layer quadrature required.')
        self.layers=len(self.offsets)
        self.inner=inner_radius+self.width*self.offsets
        self.source_mass=source_mass
        factors,sampling=sparse_factors(count,include_gram)
        self.factors=factors[:,:-1].tocsr()
        self.sampling=sampling
        base_factors,base_sampling=sparse_factors(count,False)
        derivative=diags(1/self.trapezoid) @ base_sampling.T @ base_factors
        transport=diags(self.coordinate) @ derivative
        self.transport_free=transport[:-1,:-1].tocsr()
        self.transport_endpoint=transport[-1,:-1].tocsr()
        radii=self.inner[:,None]+(initial_radius-inner_radius)*self.coordinate
        profile,profile_rate=outgoing_profile(-radii,amplitude)
        scalar=profile[:,:-1]/radii[:,:-1]
        mass=(initial_radius-inner_radius)*self.trapezoid*radii**2
        momentum=mass[:,:-1]*profile_rate[:,:-1]/radii[:,:-1]
        position=initial_radius+self.width*self.offsets
        self.initial_state=self.pack(scalar,momentum,position,np.zeros(self.layers))

