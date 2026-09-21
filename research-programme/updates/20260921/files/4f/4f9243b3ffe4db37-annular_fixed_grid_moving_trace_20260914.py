from annular_moving_live_gravity_20260914 import MovingGeometry
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from annular_covariant_scalar_action_20260912 import full_spatial_factors
from annular_finite_width_bulk_current_20260913 import shape_weight
import numpy as np
from scipy.sparse import csr_matrix


class FixedGridMovingTrace:
    def __init__(self,count=33,gram=False,degree=4,radial_degree=14,width=.001,amplitude=.01,
                 coupling=.1,central_mass=.8):
        self.count=count
        self.free=count
        self.gram=gram
        self.degree=degree
        self.grid=ChebyshevRule(degree)
        self.offsets=self.grid.points/2
        self.layers=degree+1
        self.radial_rule=ChebyshevRule(radial_degree)
        self.width=width
        self.coupling=coupling
        self.central_mass=central_mass
        self.source_mass=.003
        self.radii=np.linspace(3,7,count)
        self.spacing=4/(count-1)
        self.node_weights=np.full(count,self.spacing)
        self.node_weights[[0,-1]]/=2
        factors,sampling=full_spatial_factors(count,gram)
        self.factors=csr_matrix(factors)
        self.sampling=csr_matrix(sampling)
        self.factor,self.node=np.nonzero((factors!=0)|(sampling!=0))
        self.bpair=factors[self.factor,self.node]
        self.spair=sampling[self.factor,self.node]
        self.anchor=(sampling @ self.radii)[self.factor]
        self.target=self.radii[self.node]
        self.orientation=np.sign(self.target-self.anchor)
        distance=abs(self.radii-6.03)
        envelope=np.ones(count)
        outside=distance>=.55
        transition=(distance>.20)&(~outside)
        fraction=(distance[transition]-.20)/.35
        envelope[transition]=1-(6*fraction**5-15*fraction**4+10*fraction**3)
        envelope[outside]=0.
        values=np.zeros((self.layers,2*count+3))
        values[:,:count]=amplitude*(self.radii-6.03)*envelope
        values[:,2*count]=6.03+width*self.offsets
        self.initial_state=values.ravel()

    def values(self,state):
        return state.reshape(self.layers,2*self.count+3)

    def geometry(self,state):
        return TraceGeometry(self,state)

    def preparation(self,state):
        geometry=self.geometry(state)
        data=geometry.layer(self.offsets)
        coefficient=data['R'][:,:self.count]**2*data['N'][:,:self.count]*data['U'][:,:self.count]
        qdot=coefficient*data['pi']/(self.node_weights*data['R'][:,:self.count]**4)
        force=-(self.factors.T @ (data['A']*(self.sampling @ coefficient.T).T).T).T/self.spacing
        particle_force=-data['E']*data['N'][:,-1]*data['log_N_R'][:,-1]
        particle_force-=data['N'][:,-1]*data['U'][:,-1]*data['U_R'][:,-1]*data['p_s']**2/data['E']
        rhs=np.column_stack([qdot,force,data['V'],particle_force,
                             data['N'][:,-1]*self.source_mass/data['E']]).ravel()
        trace=np.sum(data['trace_weights']*data['q'],axis=1)
        gradient=np.sum(data['trace_gradient']*data['q'],axis=1)
        trace_rate=np.sum(data['trace_weights']*qdot,axis=1)+data['V']*gradient
        return dict(geometry=geometry,data=data,qdot=qdot,rhs0=rhs,
                    trace=trace,trace_rate=trace_rate,trace_gradient=gradient)

    def rate_constraint(self,state):
        return self.preparation(state)['trace_rate']

    def evaluate(self,time,state):
        prepared=self.preparation(state)
        step=1e-22
        base=self.rate_constraint(state.astype(complex)+1j*step*prepared['rhs0']).imag/step
        directions=np.zeros((self.layers,len(state)))
        for layer in range(self.layers):
            values=self.values(directions[layer])
            values[layer,self.count:2*self.count]=prepared['data']['trace_weights'][layer]
            values[layer,2*self.count+1]=prepared['trace_gradient'][layer]
        matrix=np.column_stack([self.rate_constraint(state.astype(complex)+1j*step*direction).imag/step
                                for direction in directions])
        multipliers=np.linalg.solve(matrix,-base)
        rhs=prepared['rhs0']+multipliers @ directions
        return dict(prepared,rhs=rhs,multipliers=multipliers,multiplier_matrix=matrix,
                    acceleration_constraint=base+matrix @ multipliers)

    def rhs(self,time,state):
        return self.evaluate(time,state)['rhs']


class TraceGeometry(MovingGeometry):
    def material(self,offsets):
        offsets=np.asarray(offsets).reshape(-1)
        system=self.system
        values=np.polynomial.chebyshev.chebval(2*offsets,self.coefficients).T
        scalar=values[:,:system.count]
        momentum=values[:,system.count:2*system.count]
        position=values[:,2*system.count]
        particle=values[:,2*system.count+1]
        fixed=system.radii[None,:]+system.width*offsets[:,None]
        radii=np.column_stack([fixed,position])
        derivative=np.polynomial.chebyshev.chebval(2*offsets,self.b_derivative)
        jacobian=np.column_stack([np.full_like(fixed,system.width),derivative])
        amplitudes=(system.factors @ scalar.T).T
        potential=fixed**2*(system.sampling.T @ (amplitudes**2).T).T/(2*system.spacing)
        energy=momentum**2/(2*system.node_weights*fixed**2)+potential
        trace_coordinate=(position-system.width*offsets-system.radii[0])/system.spacing
        cell=np.floor(trace_coordinate.real).astype(int)
        if np.any(cell<0) or np.any(cell>=system.count-1):
            raise ValueError('Moving source left scalar interpolation domain.')
        fraction=trace_coordinate-cell
        trace=np.zeros_like(scalar)
        gradient=np.zeros_like(scalar)
        rows=np.arange(len(offsets))
        trace[rows,cell]=1-fraction
        trace[rows,cell+1]=fraction
        gradient[rows,cell]=-1/system.spacing
        gradient[rows,cell+1]=1/system.spacing
        return dict(z=offsets,q=scalar,pi=momentum,b=position,PB=particle,p_s=particle,R=radii,J=jacobian,
                    A=amplitudes,potential=potential,fixed_energy=np.column_stack([energy,np.zeros(len(offsets))]),
                    trace_weights=trace,trace_gradient=gradient,cell=cell,theta=values[:,-1])

    def packet(self,radius,node):
        system=self.system
        if node<system.count:
            offsets=(radius-system.radii[node])/system.width
        else:
            offsets=self.inverse_map(radius,1.)
        data=self.material(offsets)
        density=shape_weight(offsets,'beta22')/data['J'][:,node]
        result=dict(density=density,fixed=data['fixed_energy'][:,node],node=node)
        if node==system.count:
            result.update(target=data['p_s'],coefficient=np.zeros_like(data['p_s']))
        return result

    def layer(self,offsets):
        data=self.material(offsets)
        fields=self.metric(data['R'])
        geometry=fields['U'][:,-1]**2
        energy=np.sqrt(self.system.source_mass**2+geometry*data['p_s']**2)
        velocity=fields['N'][:,-1]*geometry*data['p_s']/energy
        return dict(data,**fields,E=energy,V=velocity)

    def mass_current(self,radius,multipliers,current_degree=None):
        system=self.system
        degree=2*system.degree+12 if current_degree is None else current_degree
        rule=ChebyshevRule(degree)
        offsets=rule.points/2
        data=self.layer(offsets)
        metric_coefficient=data['R'][:,:system.count]**2*data['N'][:,:system.count]*data['U'][:,:system.count]
        qdot=metric_coefficient*data['pi']/(system.node_weights*data['R'][:,:system.count]**4)
        amplitude_rate=(system.factors @ qdot.T).T
        dual=(system.sampling @ metric_coefficient.T).T
        pair=data['A'][:,system.factor]*(amplitude_rate[:,system.factor]*system.spair*metric_coefficient[:,system.node]-
                  dual[:,system.factor]*system.bpair*qdot[:,system.node])/system.spacing
        weighted=shape_weight(offsets,'beta22')[:,None]*pair
        primitive=np.polynomial.chebyshev.chebint(rule.inverse @ weighted,axis=0)/2
        radius=np.asarray(radius).reshape(-1)
        lower=np.clip((radius[:,None]-np.maximum(system.anchor,system.target)[None,:])/system.width,-.5,.5)
        upper=np.clip((radius[:,None]-np.minimum(system.anchor,system.target)[None,:])/system.width,-.5,.5)
        bulk=(np.polynomial.chebyshev.chebval(2*upper,primitive,tensor=False)-
              np.polynomial.chebyshev.chebval(2*lower,primitive,tensor=False)) @ system.orientation
        multiplier_values=np.polynomial.chebyshev.chebval(2*offsets,system.grid.inverse @ multipliers)
        trace_pair=multiplier_values[:,None]*data['trace_weights']*qdot
        trace_primitive=np.polynomial.chebyshev.chebint(rule.inverse @
                            (shape_weight(offsets,'beta22')[:,None]*trace_pair),axis=0)/2
        source_offsets=self.inverse_map(radius[:,None],np.ones((1,system.count)))
        node_offsets=np.clip((radius[:,None]-system.radii[None,:])/system.width,-.5,.5)
        integrated_trace=np.sum(np.polynomial.chebyshev.chebval(2*source_offsets,trace_primitive,tensor=False)-
                                np.polynomial.chebyshev.chebval(2*node_offsets,trace_primitive,tensor=False),axis=1)
        source=np.zeros_like(radius,dtype=np.result_type(self.state,radius))
        selected=(radius.real>self.node_lower[-1].real)&(radius.real<self.node_upper[-1].real)
        if np.any(selected):
            locations=radius[selected]
            offsets=self.inverse_map(locations,1.)
            local=self.layer(offsets)
            source[selected]=local['p_s']*shape_weight(offsets,'beta22')/local['J'][:,-1]
        fields=self.metric(radius)
        return dict(total=-system.coupling*fields['U']/fields['N']*(bulk+integrated_trace)
                          -system.coupling*fields['N']*fields['U']**3*source,
                    bulk=bulk,trace=integrated_trace,source=source)

