import numpy as np
from scipy.integrate import solve_ivp

from annular_finite_width_bulk_current_20260913 import shape_weight


class RadialGeometryVariation:
    def __init__(self, system, evaluation, direction, parameter_direction):
        self.system = system
        self.geometry = evaluation['geometry']
        self.parameter = evaluation['parameter']
        self.parameter_direction = parameter_direction
        self.variation_coefficients = system.grid.coefficients(system.unpack(direction)[0])
        self.pieces = []
        seed = np.zeros(2)
        for piece in self.geometry.pieces:
            lower,upper = piece['lower'],piece['upper']
            node = None if piece['gap'] else int(np.argmin(abs(system.radii-(lower+upper)/2)))
            solution = solve_ivp(lambda radius,values:self.equation(radius,values,node),
                                 (lower,upper),seed,method='DOP853',rtol=2e-11,atol=1e-15,
                                 max_step=(upper-lower)/4,dense_output=True)
            if not solution.success:
                raise RuntimeError(solution.message)
            self.pieces.append({'lower':lower,'upper':upper,'solution':solution})
            seed = solution.y[:,-1]
        self.edges = np.array([piece['lower'] for piece in self.pieces]+[self.pieces[-1]['upper']])
        outer = np.array([system.radii[-1]])
        raw = self.raw(outer)[0]
        fields = self.geometry.metric(outer)
        self.normalization = -raw[0]/(outer[0]*fields['U'][0]**2)-raw[1]

    def densities(self, radius, node):
        if node is None:
            return np.zeros(6)
        system = self.system
        offsets = np.array([(radius-system.radii[node])/system.width])
        data = self.geometry.scalar(offsets)
        variation = system.grid.evaluate(self.variation_coefficients,offsets)
        free = len(system.radii)-1
        theta = data['theta'][0]
        delta_theta = variation[0,2*free]
        delta_chi = np.append(variation[0,:free],data['source_velocity'][0]*delta_theta+self.parameter_direction*theta**3/6)
        delta_amplitude = system.factors @ delta_chi
        measure = shape_weight(offsets,system.shape)[0]/system.width
        fixed = measure*data['potential'][0,node]
        delta_fixed = measure*radius**2*((data['A'][0]*delta_amplitude) @ system.sampling[:,node])/system.spacing
        kinetic,delta_kinetic,source,delta_source = 0.,0.,0.,0.
        if node == free:
            velocity = data['source_velocity'][0]
            delta_velocity = (system.proper_acceleration+self.parameter*theta)*delta_theta+self.parameter_direction*theta**2/2
            kinetic = measure*system.node_weights[node]*radius**2*velocity**2/2
            delta_kinetic = measure*system.node_weights[node]*radius**2*velocity*delta_velocity
            source = measure*data['energy'][0]
            delta_source = measure*variation[0,-1]
        else:
            momentum = data['p'][0,node]
            delta_momentum = variation[0,free+node]
            fixed += measure*system.node_weights[node]*momentum**2/(2*radius**2)
            delta_fixed += measure*system.node_weights[node]*momentum*delta_momentum/radius**2
        return np.array([fixed,kinetic,source,delta_fixed,delta_kinetic,delta_source])

    def equation(self, radius, values, node):
        fields = self.geometry.metric(np.array([radius]))
        root = fields['U'][0]
        geometry = root**2
        fixed,kinetic,source,delta_fixed,delta_kinetic,delta_source = self.densities(radius,node)
        coupling = self.system.coupling
        mass_rate = -coupling*(2*fixed/radius+source/(radius*root))*values[0]
        mass_rate += coupling*(geometry*delta_fixed+delta_kinetic+root*delta_source)
        log_rate = (1+2*coupling*kinetic)*values[0]/(radius**2*geometry**2)
        log_rate += coupling*(delta_fixed+delta_kinetic/geometry)/radius
        return np.array([mass_rate,log_rate])

    def raw(self, radius):
        radius = np.asarray(radius).reshape(-1)
        indices = np.clip(np.searchsorted(self.edges,radius,side='right')-1,0,len(self.pieces)-1)
        result = np.empty((len(radius),2))
        for index in np.unique(indices):
            selected = indices==index
            result[selected] = self.pieces[index]['solution'].sol(radius[selected]).T
        return result

    def evaluate(self, radius):
        radius = np.asarray(radius).reshape(-1)
        values = self.raw(radius)
        fields = self.geometry.metric(radius)
        log_variation = values[:,1]+self.normalization
        return {'mu':values[:,0], 'log_N':log_variation, 'N':fields['N']*log_variation,
                'U':-values[:,0]/(radius*fields['U'])}

