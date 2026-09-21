import numpy as np
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from annular_finite_width_bulk_current_20260913 import shape_weight


class DustGravityCollar:
    def __init__(self,degree=16,width=.001,coupling=.1,source_mass=.003,central_mass=.8,initial_radius=6.):
        self.degree=degree
        self.rule=ChebyshevRule(degree)
        self.offsets=self.rule.points/2
        self.integral=self.rule.integration/2
        derivative_coefficients=np.polynomial.chebyshev.chebder(self.rule.inverse,axis=0)
        self.derivative=2*np.polynomial.chebyshev.chebval(self.rule.points,derivative_coefficients).T
        self.probes=np.linspace(-1,1,8*degree+1)
        self.probe_derivative=2*np.polynomial.chebyshev.chebval(self.probes,derivative_coefficients).T
        self.shape=shape_weight(self.offsets,'beta22')
        self.width=width
        self.coupling=coupling
        self.source_mass=source_mass
        self.central_mass=central_mass
        self.initial_radius=initial_radius
        self.count=degree+1
        position=initial_radius+width*self.offsets
        self.initial_state=np.concatenate([position,np.zeros(2*self.count)])
        self.initial_geometry=self.geometry(self.initial_state)

    def unpack(self,state):
        return state[:self.count],state[self.count:2*self.count],state[2*self.count:]

    def geometry(self,state):
        position,momentum,proper_time=self.unpack(state)
        if np.min(np.real(position))<=0:
            raise ValueError('Nonpositive areal radius.')
        mass=np.full(self.count,self.central_mass,dtype=np.result_type(state))
        for iteration in range(6):
            geometry=1-2*mass/position
            if np.min(np.real(geometry))<=.15:
                raise ValueError('Outside declared regular polar chart.')
            root=np.sqrt(geometry)
            energy=np.sqrt(self.source_mass**2+geometry*momentum**2)
            loading=self.coupling*self.shape*root*energy
            slope=-self.coupling*self.shape*(self.source_mass**2+2*geometry*momentum**2)/(position*root*energy)
            residual=mass-self.central_mass-self.integral @ loading
            jacobian=np.eye(self.count)-self.integral*slope[None,:]
            mass-=np.linalg.solve(jacobian,residual)
        geometry=1-2*mass/position
        root=np.sqrt(geometry)
        energy=np.sqrt(self.source_mass**2+geometry*momentum**2)
        mass_gradient=self.coupling*self.shape*root*energy
        defect=np.max(abs(mass-self.central_mass-self.integral @ mass_gradient))
        position_gradient=self.derivative @ (position-self.initial_radius)
        log_gradient=position_gradient*mass/(position**2*geometry)+self.coupling*self.shape*root*momentum**2/(position*energy)
        log_lapse=self.integral @ log_gradient
        log_lapse+=np.log(root[-1])-log_lapse[-1]
        lapse=np.exp(log_lapse)
        return dict(position=position,momentum=momentum,mass=mass,F=geometry,U=root,N=lapse,
                    E=energy,mass_z=mass_gradient,position_z=position_gradient,log_N_z=log_gradient,
                    constraint_defect=float(defect))

    def rhs(self,time,state):
        data=self.geometry(state)
        position_rate=data['N']*data['F']*data['momentum']/data['E']
        momentum_rate=-data['N']*data['mass']/data['position']**2*(data['E']/data['F']+data['momentum']**2/data['E'])
        clock_rate=data['N']*self.source_mass/data['E']
        return np.concatenate([position_rate,momentum_rate,clock_rate])

    def minimum_jacobian(self,state):
        position=self.unpack(state)[0]
        return float(np.min(self.probe_derivative @ (position-self.initial_radius)))

    def diagnostics(self,state):
        data=self.geometry(state)
        source_rate=data['F']*data['momentum']/self.source_mass
        binding=data['U']*data['E']/self.source_mass
        initial_binding=self.initial_geometry['U']
        return dict(max_material_mass_error=float(np.max(abs(data['mass']-self.initial_geometry['mass']))),
                    exterior_mass_error=float(abs(data['mass'][-1]-self.initial_geometry['mass'][-1])),
                    max_binding_error=float(np.max(abs(binding-initial_binding))),
                    minimum_F=float(np.min(data['F'])),
                    minimum_jacobian=self.minimum_jacobian(state),
                    proper_rate=source_rate,position=data['position'],proper_times=self.unpack(state)[2],
                    constraint_defect=data['constraint_defect'])

    def initial_focusing(self):
        data=self.initial_geometry
        shape_acceleration=-data['N']**2*data['mass_z']/data['position']**2
        shape_acceleration+=2*data['N']**2*self.width*(data['mass']/data['position']**3-data['mass']**2/(data['position']**4*data['F']))
        leading=-data['N']**2*data['mass_z']/data['position']**2
        duration=np.sqrt(2*self.width/(-np.min(leading)))
        return shape_acceleration,leading,float(duration)

