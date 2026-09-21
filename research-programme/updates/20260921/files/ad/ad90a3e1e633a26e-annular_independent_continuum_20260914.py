import numpy as np
from scipy.integrate import cumulative_simpson, solve_ivp


def preparation(radius):
    radius = np.asarray(radius,dtype=float)
    coordinate = (radius-5.5)/.3
    selected = abs(coordinate)<1
    bump = np.zeros_like(radius)
    gradient = np.zeros_like(radius)
    denominator = 1-coordinate[selected]**2
    bump[selected] = np.exp(1-1/denominator)
    gradient[selected] = -2*coordinate[selected]*bump[selected]/(.3*denominator**2)
    return .02*bump,.02*gradient,.004*radius**2*bump


def derivative(values,spacing):
    values = np.asarray(values)
    result = np.empty_like(values)
    result[2:-2] = (values[:-4]-8*values[1:-3]+8*values[3:-1]-values[4:])/(12*spacing)
    result[0] = np.dot([-25,48,-36,16,-3],values[:5])/(12*spacing)
    result[1] = np.dot([-3,-10,18,-6,1],values[:5])/(12*spacing)
    result[-1] = -np.dot([-25,48,-36,16,-3],values[-1:-6:-1])/(12*spacing)
    result[-2] = -np.dot([-3,-10,18,-6,1],values[-1:-6:-1])/(12*spacing)
    return result


class ContinuumEvolution:
    def __init__(self,count,coupling=.1,reservoir=.003,clock='midpoint'):
        if count<17 or count%2!=1:
            raise ValueError('Use an odd number of at least17 uniform nodes.')
        if clock not in ['midpoint','outer']:
            raise ValueError('Unknown shell clock.')
        self.radii = np.linspace(5.,6.,count)
        self.spacing = 1/(count-1)
        self.count = count
        self.coupling = coupling
        self.reservoir = reservoir
        self.clock = clock
        self.initial_state = np.concatenate(preparation(self.radii))
        self.calls = 0

    def unpack(self,state):
        return np.asarray(state).reshape(3,self.count)

    def primitive(self,values):
        return cumulative_simpson(values,x=self.radii,initial=0.)

    def geometry(self,state):
        scalar,gradient,momentum = self.unpack(state)
        radius = self.radii
        density = .5*(radius**2*gradient**2+momentum**2/radius**2)
        exponent = self.primitive(2*self.coupling*density/radius)
        integrating = np.exp(exponent)
        mass = (.8+self.primitive(self.coupling*density*integrating))/integrating
        geometry = 1-2*mass/radius
        if geometry.min()<=.5:
            raise ValueError('Outside declared regular continuum pilot chart.')
        root_minus = np.sqrt(geometry[-1])
        geometric_source_mass = self.coupling*self.reservoir
        root_plus = root_minus-geometric_source_mass/6
        if root_plus<=0:
            raise ValueError('Source shell leaves regular chart.')
        shell_lapse = (root_minus+root_plus)/2 if self.clock=='midpoint' else root_plus
        mass_plus = mass[-1]+geometric_source_mass*root_minus-geometric_source_mass**2/12
        log_speed_primitive = self.primitive(2*mass/(radius**2*geometry))
        log_speed = np.log(shell_lapse*root_minus)+log_speed_primitive-log_speed_primitive[-1]
        speed = np.exp(log_speed)
        log_lapse = log_speed-.5*np.log(geometry)
        surface_density = self.reservoir/36
        surface_pressure = surface_density*(1/(root_minus*root_plus)-1)/4-root_minus*density[-1]/12
        return dict(density=density,mass=mass,F=geometry,L=speed,log_N=log_lapse,
                    primitive_exponent=exponent,integrating_factor=integrating,
                    energy=self.primitive(density)[-1],mass_plus=mass_plus,
                    N_shell=shell_lapse,U_minus=root_minus,U_plus=root_plus,
                    outer_clock=shell_lapse/root_plus,Sigma=surface_density,P=surface_pressure)

    def rhs(self,time,state):
        self.calls += 1
        scalar,gradient,momentum = self.unpack(state)
        geometry = self.geometry(state)
        scalar_rate = geometry['L']*momentum/self.radii**2
        gradient_rate = derivative(scalar_rate,self.spacing)
        momentum_rate = derivative(self.radii**2*geometry['L']*gradient,self.spacing)
        gradient_rate[0] = 0.
        momentum_rate[-1] = 0.
        scalar_rate[-1] = 0.
        return np.concatenate([scalar_rate,gradient_rate,momentum_rate])

    def integrate(self,duration=.06,divisor=8,tolerance=2e-11):
        solution = solve_ivp(self.rhs,(0.,duration),self.initial_state,method='DOP853',
                             rtol=tolerance,atol=tolerance/100,
                             max_step=min(duration/divisor,self.spacing/4),dense_output=True)
        if not solution.success:
            raise RuntimeError(solution.message)
        return solution

    def diagnostics(self,time,state):
        scalar,gradient,momentum = self.unpack(state)
        geometry = self.geometry(state)
        scalar_rate,gradient_rate,momentum_rate = self.unpack(self.rhs(time,state))
        density_rate = self.radii**2*gradient*gradient_rate+momentum*momentum_rate/self.radii**2
        exponent_rate = self.primitive(2*self.coupling*density_rate/self.radii)
        mass_rate = -geometry['mass']*exponent_rate+self.primitive(
            self.coupling*geometry['integrating_factor']*(density_rate+geometry['density']*exponent_rate)
        )/geometry['integrating_factor']
        flux_rate = self.coupling*geometry['F']*geometry['L']*momentum*gradient
        mass_constraint = derivative(geometry['mass'],self.spacing)-self.coupling*geometry['F']*geometry['density']
        lapse_constraint = derivative(geometry['log_N'],self.spacing)-(
            geometry['mass']/(self.radii**2*geometry['F'])+self.coupling*geometry['density']/self.radii)
        return dict(time=float(time),minimum_F=float(geometry['F'].min()),
                    mass_plus=float(geometry['mass_plus']),energy=float(geometry['energy']),
                    gradient_constraint=float(abs(derivative(scalar,self.spacing)-gradient).max()),
                    mass_constraint=float(abs(mass_constraint).max()),
                    lapse_constraint=float(abs(lapse_constraint).max()),
                    mass_time_identity=float(abs(mass_rate-flux_rate).max()),
                    midpoint_clock_error=float(abs(geometry['N_shell']-(geometry['U_minus']+geometry['U_plus'])/2)),
                    left_flux=float(abs(self.radii[0]**2*geometry['L'][0]*gradient[0])),
                    right_momentum=float(abs(momentum[-1])),
                    boundary_scalar_amplitude=float(max(abs(scalar[0]),abs(scalar[-1]))))

