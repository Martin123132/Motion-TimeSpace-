import numpy as np
from scipy.sparse import csr_matrix, diags
from annular_covariant_scalar_action_20260912 import full_spatial_factors
from annular_dynamical_source_20260914 import outgoing_profile


class MovingCollarAction:
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
        factors,sampling=full_spatial_factors(count,include_gram)
        self.factors=csr_matrix(factors[:,:-1])
        self.sampling=csr_matrix(sampling)
        base_factors,base_sampling=full_spatial_factors(count,False)
        derivative=diags(1/self.trapezoid) @ csr_matrix(base_sampling).T @ csr_matrix(base_factors)
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

    def pack(self,scalar,momentum,position,velocity):
        return np.concatenate([scalar.ravel(),momentum.ravel(),np.asarray(position),np.asarray(velocity)])

    def unpack(self,state):
        size=self.layers*self.free
        return (state[:size].reshape(self.layers,self.free),state[size:2*size].reshape(self.layers,self.free),
                state[2*size:2*size+self.layers],state[-self.layers:])

    def fields(self,state):
        scalar,momentum,position,velocity=self.unpack(state)
        length=position-self.inner
        if np.min(np.real(length))<=0 or np.max(abs(np.real(velocity)))>=1:
            raise ValueError('Outside positive interval/timelike source chart.')
        radii=self.inner[:,None]+length[:,None]*self.coordinate
        spacing=length*self.reference_spacing
        mass=length[:,None]*self.trapezoid*radii**2
        mass_b=mass*(1/length[:,None]+2*self.coordinate/radii)
        amplitude=(self.factors @ scalar.T).T
        factor_coefficient=(self.sampling @ (radii**2).T).T/spacing[:,None]
        coefficient_b=(self.sampling @ (2*radii*self.coordinate).T).T/spacing[:,None]-factor_coefficient/length[:,None]
        force=(self.factors.T @ (factor_coefficient*amplitude).T).T
        transport=(self.transport_free @ scalar.T).T/length[:,None]
        endpoint=(self.transport_endpoint @ scalar.T).T[:,0]/length
        edge_inertia=mass[:,-1]*endpoint**2
        edge_b=edge_inertia*(2/radii[:,-1]-1/length)
        edge_gradient=np.zeros_like(scalar)
        edge_gradient[:,-1]=radii[:,-1]**2*scalar[:,-1]/spacing
        return dict(radii=radii,length=length,mass=mass[:,:-1],mass_b=mass_b[:,:-1],
                    amplitudes=amplitude,coefficient=factor_coefficient,coefficient_b=coefficient_b,
                    force=force,transport=transport,edge_inertia=edge_inertia,
                    edge_b=edge_b,edge_gradient=edge_gradient)

    def rhs(self,time,state):
        scalar,momentum,position,velocity=self.unpack(state)
        data=self.fields(state)
        rate=momentum/data['mass']
        transported_momentum=(self.transport_free.T @ momentum.T).T/data['length'][:,None]
        scalar_rate=rate+velocity[:,None]*data['transport']
        momentum_rate=-data['force']-velocity[:,None]*transported_momentum+velocity[:,None]**2*data['edge_gradient']/2
        transported_rate=(self.transport_free @ rate.T).T/data['length'][:,None]
        driving=np.sum(data['mass_b']*rate**2,axis=1)/2
        driving-=np.sum(data['coefficient_b']*data['amplitudes']**2,axis=1)/2
        driving-=np.sum(data['force']*data['transport'],axis=1)
        driving+=np.sum(momentum*transported_rate,axis=1)
        driving-=velocity*np.sum(data['edge_gradient']*rate,axis=1)
        driving-=velocity**2*(data['edge_b']+np.sum(data['edge_gradient']*data['transport'],axis=1))/2
        gamma=1/np.sqrt(1-velocity**2)
        acceleration=driving/(self.source_mass*gamma**3+data['edge_inertia'])
        return self.pack(scalar_rate,momentum_rate,velocity,acceleration)

    def lagrangian(self,scalar,scalar_rate,position,velocity):
        zero=np.zeros_like(scalar)
        state=self.pack(scalar,zero,position,velocity)
        data=self.fields(state)
        eulerian_rate=scalar_rate-velocity[:,None]*data['transport']
        kinetic=np.sum(data['mass']*eulerian_rate**2,axis=1)/2
        endpoint=data['edge_inertia']*velocity**2/2
        potential=np.sum(data['coefficient']*data['amplitudes']**2,axis=1)/2
        return self.weights @ (kinetic+endpoint-potential-self.source_mass*np.sqrt(1-velocity**2))

    def energy(self,state):
        scalar,momentum,position,velocity=self.unpack(state)
        data=self.fields(state)
        kinetic=np.sum(momentum**2/data['mass'],axis=1)/2
        potential=np.sum(data['coefficient']*data['amplitudes']**2,axis=1)/2
        source=self.source_mass/np.sqrt(1-velocity**2)
        layer_energy=kinetic+potential+source+data['edge_inertia']*velocity**2/2
        return dict(total=self.weights @ layer_energy,layers=layer_energy,field=kinetic+potential,
                    edge_inertia=data['edge_inertia'],source=source)

    def source_canonical(self,state):
        scalar,momentum,position,velocity=self.unpack(state)
        data=self.fields(state)
        gamma=1/np.sqrt(1-velocity**2)
        return self.source_mass*gamma*velocity+data['edge_inertia']*velocity-np.sum(momentum*data['transport'],axis=1)

