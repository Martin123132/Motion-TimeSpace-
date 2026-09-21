import numpy as np
from scipy.sparse import csr_matrix
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from annular_covariant_scalar_action_20260912 import full_spatial_factors
from annular_finite_width_bulk_current_20260913 import shape_weight


class MovingLiveGravity:
    def __init__(self,count=33,gram=False,degree=6,radial_degree=12,width=.001,
                 amplitude=.01,coupling=.1,central_mass=.8):
        self.count=count
        self.free=count-1
        self.gram=gram
        self.degree=degree
        self.grid=ChebyshevRule(degree)
        self.radial_rule=ChebyshevRule(radial_degree)
        self.offsets=self.grid.points/2
        self.layers=degree+1
        self.width=width
        self.coupling=coupling
        self.central_mass=central_mass
        self.source_mass=.003
        self.coordinate=np.linspace(0.,1.,count)
        self.delta=1/self.free
        self.quadrature=np.full(count,self.delta)
        self.quadrature[[0,-1]]/=2
        factors,sampling=full_spatial_factors(count,gram)
        base,base_sampling=full_spatial_factors(count,False)
        self.factors=csr_matrix(factors)
        self.sampling=csr_matrix(sampling)
        derivative=(base_sampling.T @ base)/self.quadrature[:,None]
        self.transport=csr_matrix(self.coordinate[:,None]*derivative)
        self.factor,self.node=np.nonzero((factors!=0)|(sampling!=0))
        self.bpair=factors[self.factor,self.node]
        self.spair=sampling[self.factor,self.node]
        self.anchor=(sampling @ self.coordinate)[self.factor]
        self.target=self.coordinate[self.node]
        self.orientation=np.sign(self.target-self.anchor)
        pulse=(self.coordinate-.9)/.25
        selected=abs(pulse)<1
        profile=np.zeros(count)
        profile[selected]=amplitude*(1-self.coordinate[selected])*np.exp(1-1/(1-pulse[selected]**2))
        values=np.zeros((self.layers,2*self.free+3))
        values[:,:self.free]=profile[:-1]
        values[:,2*self.free]=6+self.width*self.offsets
        self.initial_state=values.ravel()

    def values(self,state):
        return state.reshape(self.layers,2*self.free+3)

    def geometry(self,state):
        return MovingGeometry(self,state)

    def evaluate(self,time,state):
        geometry=self.geometry(state)
        data=geometry.layer(self.offsets)
        free=self.free
        kinetic=data['measure']*data['R']**2/(data['N']*data['U'])
        eulerian=data['pi'][:,:-1]/kinetic[:,:-1]
        velocity=data['V']
        scalar_rate=eulerian+velocity[:,None]*data['Tq'][:,:-1]
        scalar_rate_full=np.column_stack([scalar_rate,np.zeros(self.layers)])
        coefficient=(self.sampling @ (data['R']**2*data['N']*data['U']).T).T/data['spacing'][:,None]
        force=(self.factors.T @ (coefficient*data['A']).T).T
        transported_momentum=(self.transport[:free,:free].T @ data['pi'][:,:-1].T).T/data['H'][:,None]
        edge_gradient=2*kinetic[:,-1,None]*data['Tq'][:,-1,None]*self.transport[-1,:free].toarray()/data['H'][:,None]
        momentum_rate=-force[:,:-1]-velocity[:,None]*transported_momentum+velocity[:,None]**2*edge_gradient/2
        metric_log_gradient=data['log_N_R']+data['U_R']/data['U']
        kinetic_b=kinetic*(1/data['H'][:,None]+2*self.coordinate/data['R']-self.coordinate*metric_log_gradient)
        coefficient_b=(self.sampling @ (self.coordinate*(2*data['R']*data['N']*data['U']+
                         data['R']**2*data['N']*(data['U']*data['log_N_R']+data['U_R']))).T).T/data['spacing'][:,None]
        coefficient_b-=coefficient/data['H'][:,None]
        edge_inertia=kinetic[:,-1]*data['Tq'][:,-1]**2
        edge_b=edge_inertia*(2/data['b']-1/data['H']-metric_log_gradient[:,-1])
        source_force=-data['E']*data['N'][:,-1]*data['log_N_R'][:,-1]
        source_force-=data['N'][:,-1]*data['U'][:,-1]*data['U_R'][:,-1]*data['p_s']**2/data['E']
        embedding_rate=np.sum(kinetic_b[:,:-1]*eulerian**2,axis=1)/2
        embedding_rate+=velocity/data['H']*np.sum(data['pi'][:,:-1]*data['Tq'][:,:-1],axis=1)
        embedding_rate+=edge_b*velocity**2/2-np.sum(coefficient_b*data['A']**2,axis=1)/2+source_force
        clock_rate=data['N'][:,-1]*self.source_mass/data['E']
        result=np.column_stack([scalar_rate,momentum_rate,velocity,embedding_rate,clock_rate]).ravel()
        return dict(rhs=result,geometry=geometry,data=data,qdot=scalar_rate_full)

    def rhs(self,time,state):
        return self.evaluate(time,state)['rhs']


class MovingGeometry:
    def __init__(self,system,state):
        self.system=system
        self.state=state
        self.coefficients=system.grid.inverse @ system.values(state)
        self.b_coefficients=self.coefficients[:,2*system.free]
        self.b_derivative=2*np.polynomial.chebyshev.chebder(self.b_coefficients)
        probes=np.linspace(-.5,.5,4*system.degree+1)
        self.minimum_source_jacobian=float(np.min(np.real(np.polynomial.chebyshev.chebval(2*probes,self.b_derivative))))
        if self.minimum_source_jacobian<=0:
            raise ValueError('Source map lost order; no physical continuation through a dust caustic.')
        ends=self.material(np.array([-.5,.5]))['R']
        self.node_lower,self.node_upper=ends[0],ends[1]
        all_edges=np.concatenate([self.node_lower,self.node_upper])
        self.edges=all_edges[np.argsort(all_edges.real)]
        if np.any(np.diff(self.edges.real)<=1e-13):
            raise ValueError('Coincident support edges require a separate topology treatment.')
        self.pieces=[]
        self.constraint_defect=0.
        self.maximum_overlap=0
        mass_seed=np.asarray(system.central_mass,dtype=np.result_type(state))[()]
        log_seed=np.asarray(0.,dtype=np.result_type(state))[()]
        rule=system.radial_rule
        for lower,upper in zip(self.edges[:-1],self.edges[1:]):
            middle=(lower+upper)/2
            active=np.where((self.node_lower.real<middle.real)&(self.node_upper.real>middle.real))[0]
            self.maximum_overlap=max(self.maximum_overlap,len(active))
            if not len(active):
                self.pieces.append(dict(lower=lower,upper=upper,gap=True,mass=mass_seed,log_N=log_seed))
                log_seed+=.5*np.log((1-2*mass_seed/upper)/(1-2*mass_seed/lower))
                continue
            radii=(lower+upper)/2+(upper-lower)*rule.points/2
            integral=(upper-lower)*rule.integration/2
            packets=[self.packet(radii,node) for node in active]
            masses=np.full(len(radii),mass_seed,dtype=np.result_type(state))
            for iteration in range(7):
                loading,slope,unused=self.loadings(radii,masses,packets)
                residual=masses-mass_seed-integral @ loading
                masses-=np.linalg.solve(np.eye(len(radii))-integral*slope[None,:],residual)
            loading,slope,lapse_loading=self.loadings(radii,masses,packets)
            defect=float(np.max(abs(masses-mass_seed-integral @ loading)))
            self.constraint_defect=max(self.constraint_defect,defect)
            geometry=1-2*masses/radii
            if np.min(geometry.real)<=.15:
                raise ValueError('Outside declared regular polar chart.')
            log_derivative=masses/(radii**2*geometry)+lapse_loading
            logs=log_seed+integral @ log_derivative
            self.pieces.append(dict(lower=lower,upper=upper,gap=False,
                                    mass=rule.inverse @ masses,log_N=rule.inverse @ logs,active=active))
            mass_seed,log_seed=masses[-1],logs[-1]
        if self.constraint_defect>2e-11:
            raise ValueError('Nonlinear radial constraint failed.')
        self.outer_mass=mass_seed
        self.normalization=np.log(np.sqrt(1-2*mass_seed/self.edges[-1]))-log_seed

    def material(self,offsets):
        offsets=np.asarray(offsets).reshape(-1)
        system=self.system
        values=np.polynomial.chebyshev.chebval(2*offsets,self.coefficients).T
        scalar=np.column_stack([values[:,:system.free],np.zeros(len(offsets))])
        momentum=np.column_stack([values[:,system.free:2*system.free],np.zeros(len(offsets))])
        position=values[:,2*system.free]
        total=values[:,2*system.free+1]
        inner=3+system.width*offsets
        length=position-inner
        radii=inner[:,None]+length[:,None]*system.coordinate
        derivative=np.polynomial.chebyshev.chebval(2*offsets,self.b_derivative)
        jacobian=system.width+(derivative[:,None]-system.width)*system.coordinate
        if np.min(length.real)<=0:
            raise ValueError('Nonpositive scalar interval.')
        amplitudes=(system.factors @ scalar.T).T
        transported=(system.transport @ scalar.T).T/length[:,None]
        measure=length[:,None]*system.quadrature
        spacing=length*system.delta
        potential=radii**2*(system.sampling.T @ (amplitudes**2).T).T/(2*spacing[:,None])
        fixed_energy=momentum**2/(2*measure*radii**2)+potential
        target=total+np.sum(momentum[:,:-1]*transported[:,:-1],axis=1)
        return dict(z=offsets,q=scalar,pi=momentum,b=position,PB=total,H=length,R=radii,J=jacobian,
                    A=amplitudes,Tq=transported,measure=measure,spacing=spacing,potential=potential,
                    fixed_energy=fixed_energy,target=target,theta=values[:,-1])

    def inverse_map(self,radius,coordinate):
        radius,coordinate=np.broadcast_arrays(np.asarray(radius),np.asarray(coordinate))
        lower=(3-self.system.width/2)*(1-coordinate)+np.polynomial.chebyshev.chebval(-1.,self.b_coefficients)*coordinate
        upper=(3+self.system.width/2)*(1-coordinate)+np.polynomial.chebyshev.chebval(1.,self.b_coefficients)*coordinate
        below=radius.real<=lower.real
        above=radius.real>=upper.real
        offsets=(radius-lower)/(upper-lower)-.5
        offsets=np.where(below,-.5,np.where(above,.5,offsets))
        for iteration in range(7):
            position=np.polynomial.chebyshev.chebval(2*offsets,self.b_coefficients)
            slope=np.polynomial.chebyshev.chebval(2*offsets,self.b_derivative)
            mapped=(3+self.system.width*offsets)*(1-coordinate)+position*coordinate
            jacobian=self.system.width*(1-coordinate)+slope*coordinate
            offsets-=np.where(below|above,0.,(mapped-radius)/jacobian)
        return offsets

    def packet(self,radius,node):
        coordinate=self.system.coordinate[node]
        offsets=self.inverse_map(radius,coordinate)
        data=self.material(offsets)
        density=shape_weight(offsets,'beta22')/data['J'][:,node]
        packet=dict(density=density,fixed=data['fixed_energy'][:,node],node=node)
        if node==self.system.free:
            packet.update(target=data['target'],
                          coefficient=data['measure'][:,-1]*data['b']**2*data['Tq'][:,-1]**2)
        return packet

    def source_momentum(self,geometry,target,coefficient):
        root=np.sqrt(geometry)
        source=self.system.source_mass
        momentum=target/(1+coefficient*root/source)
        for iteration in range(10):
            energy=np.sqrt(source**2+geometry*momentum**2)
            residual=momentum+coefficient*root*momentum/energy-target
            derivative=1+coefficient*root*source**2/energy**3
            momentum-=residual/derivative
        energy=np.sqrt(source**2+geometry*momentum**2)
        return momentum,energy

    def loadings(self,radius,mass,packets):
        system=self.system
        geometry=1-2*mass/radius
        if np.min(geometry.real)<=.15:
            raise ValueError('Mass iteration left regular chart.')
        root=np.sqrt(geometry)
        loading=np.zeros_like(mass)
        slope=np.zeros_like(mass)
        lapse=np.zeros_like(mass)
        for packet in packets:
            density,fixed=packet['density'],packet['fixed']
            loading+=system.coupling*geometry*fixed*density
            slope-=2*system.coupling*fixed*density/radius
            lapse+=system.coupling*fixed*density/radius
            if packet['node']==system.free:
                coefficient=packet['coefficient']
                momentum,energy=self.source_momentum(geometry,packet['target'],coefficient)
                derivative=1+coefficient*root*system.source_mass**2/energy**3
                momentum_mu=coefficient*momentum*system.source_mass**2/(radius*root*energy**3*derivative)
                endpoint=coefficient*geometry*momentum**2/(2*energy**2)
                endpoint_mu=coefficient*system.source_mass**2/energy**4*(geometry*momentum*momentum_mu-momentum**2/radius)
                source_mu=-(system.source_mass**2+2*geometry*momentum**2)/(radius*root*energy)
                source_mu+=root*geometry*momentum*momentum_mu/energy
                loading+=system.coupling*(geometry*endpoint+root*energy)*density
                slope+=system.coupling*(-2*endpoint/radius+geometry*endpoint_mu+source_mu)*density
                lapse+=system.coupling*(endpoint+root*momentum**2/energy)*density/radius
        return loading,slope,lapse

    def metric(self,radius):
        shape=np.shape(radius)
        radius=np.asarray(radius).reshape(-1)
        if np.min(radius.real)<self.edges[0].real-1e-11 or np.max(radius.real)>self.edges[-1].real+1e-11:
            raise ValueError('No radial extrapolation.')
        indices=np.clip(np.searchsorted(self.edges.real,radius.real,side='right')-1,0,len(self.pieces)-1)
        dtype=np.result_type(self.state,radius)
        mass=np.empty(len(radius),dtype=dtype)
        log_N=np.empty_like(mass)
        mass_R=np.empty_like(mass)
        log_N_R=np.empty_like(mass)
        for index in np.unique(indices):
            selected=indices==index
            piece=self.pieces[index]
            locations=radius[selected]
            if piece['gap']:
                mass[selected]=piece['mass']
                mass_R[selected]=0
                log_N[selected]=piece['log_N']+.5*np.log((1-2*piece['mass']/locations)/(1-2*piece['mass']/piece['lower']))
                log_N_R[selected]=piece['mass']/(locations**2*(1-2*piece['mass']/locations))
            else:
                mapped=(2*locations-piece['lower']-piece['upper'])/(piece['upper']-piece['lower'])
                mass[selected]=np.polynomial.chebyshev.chebval(mapped,piece['mass'])
                log_N[selected]=np.polynomial.chebyshev.chebval(mapped,piece['log_N'])
                mass_R[selected]=2*np.polynomial.chebyshev.chebval(mapped,np.polynomial.chebyshev.chebder(piece['mass']))/(piece['upper']-piece['lower'])
                log_N_R[selected]=2*np.polynomial.chebyshev.chebval(mapped,np.polynomial.chebyshev.chebder(piece['log_N']))/(piece['upper']-piece['lower'])
        root=np.sqrt(1-2*mass/radius)
        root_R=(mass/radius**2-mass_R/radius)/root
        return {key:value.reshape(shape) for key,value in dict(mu=mass,U=root,N=np.exp(log_N+self.normalization),
                    mu_R=mass_R,U_R=root_R,log_N_R=log_N_R).items()}

    def layer(self,offsets):
        data=self.material(offsets)
        fields=self.metric(data['R'])
        geometry=fields['U'][:,-1]**2
        coefficient=data['measure'][:,-1]*data['b']**2*data['Tq'][:,-1]**2
        momentum,energy=self.source_momentum(geometry,data['target'],coefficient)
        velocity=fields['N'][:,-1]*geometry*momentum/energy
        data['pi'][:,-1]=-data['measure'][:,-1]*data['b']**2*fields['U'][:,-1]*momentum/energy*data['Tq'][:,-1]
        return dict(data,**fields,p_s=momentum,E=energy,V=velocity)

    def mass_current(self,radius,current_degree=None):
        system=self.system
        degree=2*system.degree+12 if current_degree is None else current_degree
        rule=ChebyshevRule(degree)
        offsets=rule.points/2
        data=self.layer(offsets)
        kinetic=data['measure']*data['R']**2/(data['N']*data['U'])
        qdot=data['pi']/kinetic+data['V'][:,None]*data['Tq']
        qdot[:,-1]=0
        amplitude_rate=(system.factors @ qdot.T).T
        coefficient=data['R']**2*data['N']*data['U']
        dual=(system.sampling @ coefficient.T).T
        pair=data['A'][:,system.factor]*(amplitude_rate[:,system.factor]*system.spair*coefficient[:,system.node]-
                dual[:,system.factor]*system.bpair*qdot[:,system.node])/data['spacing'][:,None]
        weighted=shape_weight(offsets,'beta22')[:,None]*pair
        primitive=np.polynomial.chebyshev.chebint(rule.inverse @ weighted,axis=0)/2
        radius=np.asarray(radius).reshape(-1)
        lower=self.inverse_map(radius[:,None],np.maximum(system.anchor,system.target)[None,:])
        upper=self.inverse_map(radius[:,None],np.minimum(system.anchor,system.target)[None,:])
        integral=np.polynomial.chebyshev.chebval(2*upper,primitive,tensor=False)-np.polynomial.chebyshev.chebval(2*lower,primitive,tensor=False)
        transported=integral @ system.orientation
        direct=np.zeros_like(radius,dtype=np.result_type(self.state,radius))
        source=np.zeros_like(direct)
        for node in range(system.count):
            selected=(radius.real>self.node_lower[node].real)&(radius.real<self.node_upper[node].real)
            if not np.any(selected):
                continue
            locations=radius[selected]
            offsets=self.inverse_map(locations,system.coordinate[node])
            local=self.layer(offsets)
            density=shape_weight(offsets,'beta22')/local['J'][:,node]
            direct[selected]+=2*local['potential'][:,node]*system.coordinate[node]*local['V']*density
            if node==system.free:
                source[selected]+=local['p_s']*density
        fields=self.metric(radius)
        return dict(total=-system.coupling*fields['U']/fields['N']*transported
                          -system.coupling*fields['U']**2*direct
                          -system.coupling*fields['N']*fields['U']**3*source,
                    transported=transported,direct=direct,source=source)

