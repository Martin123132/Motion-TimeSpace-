import numpy as np


class GRProjection:
    def __init__(self, oracle, system):
        if oracle.mass != 0. or system.background_mass != 0.:
            raise ValueError('Qualified only for the prescribed flat background.')
        if oracle.source != system.source_mass:
            raise ValueError('Different source masses.')
        if not np.array_equal(system.radii[[0,-1]], [oracle.inner,oracle.outer]):
            raise ValueError('Different outer boundaries.')
        self.oracle, self.system = oracle, system
        self.left = system.radii < system.anchor
        self.coordinate = np.where(self.left,
            (system.radii-oracle.inner)/(system.anchor-oracle.inner),
            (system.radii-system.anchor)/(oracle.outer-system.anchor))
        self.displacement = np.where(self.left,self.coordinate,1-self.coordinate)

    def reconstruct(self, state, tangent=None):
        oracle, system = self.oracle,self.system
        fields,position,momentum,speed = oracle.unpack(state)
        scalar = np.empty(system.count,dtype=state.dtype)
        temporal,gradient = np.empty_like(scalar),np.empty_like(scalar)
        lengths = [position-oracle.inner,oracle.outer-position]
        coefficients = fields @ oracle.inverse.T
        for side,selected in enumerate([self.left,~self.left]):
            mapped = 2*self.coordinate[selected]-1
            plus,minus = np.polynomial.chebyshev.chebval(mapped,coefficients[side].T)
            temporal[selected],gradient[selected] = (plus+minus)/2,(plus-minus)/2
            primitive = np.polynomial.chebyshev.chebint((coefficients[side,0]-coefficients[side,1])/2)
            anchor = 1. if side==0 else -1.
            scalar[selected] = lengths[side]/2*(np.polynomial.chebyshev.chebval(mapped,primitive)
                -np.polynomial.chebyshev.chebval(anchor,primitive))
        rates = temporal+speed*self.displacement*gradient
        projected = np.concatenate([scalar,[position],rates,[speed,state[-1]]])
        if tangent is None:
            return projected
        if np.iscomplexobj(state) or np.iscomplexobj(tangent):
            raise ValueError('Derivative qualification takes real state and tangent.')
        full_rates = oracle.unpack(state.astype(complex)+1e-25j*tangent)
        field_rates = full_rates[0].imag/1e-25
        position_rate,speed_rate = full_rates[1].imag/1e-25,full_rates[3].imag/1e-25
        derivative_coefficients = field_rates @ oracle.inverse.T
        scalar_rate,velocity_rate = np.empty_like(scalar),np.empty_like(scalar)
        for side,selected in enumerate([self.left,~self.left]):
            mapped = 2*self.coordinate[selected]-1
            plus_rate,minus_rate = np.polynomial.chebyshev.chebval(mapped,derivative_coefficients[side].T)
            temporal_rate,gradient_rate = (plus_rate+minus_rate)/2,(plus_rate-minus_rate)/2
            primitive_rate = np.polynomial.chebyshev.chebint((derivative_coefficients[side,0]-derivative_coefficients[side,1])/2)
            anchor = 1. if side==0 else -1.
            length_rate = position_rate if side==0 else -position_rate
            scalar_rate[selected] = length_rate*scalar[selected]/lengths[side]+lengths[side]/2*(
                np.polynomial.chebyshev.chebval(mapped,primitive_rate)-np.polynomial.chebyshev.chebval(anchor,primitive_rate))
            velocity_rate[selected] = temporal_rate+speed_rate*self.displacement[selected]*gradient[selected]
            velocity_rate[selected] += speed*self.displacement[selected]*gradient_rate
        projected_rate = np.concatenate([scalar_rate,[position_rate],velocity_rate,[speed_rate,tangent[-1]]])
        return projected,projected_rate


def manufactured(oracle, position, speed, clock=0.):
    coordinate = oracle.coordinate
    polynomial = np.stack([coordinate**2-1,2*coordinate-coordinate**2])
    gradient = np.stack([2*coordinate,2-2*coordinate])
    displacement = np.stack([coordinate,1-coordinate])
    temporal = np.array([speed,-speed])[:,None]*polynomial-speed*displacement*gradient
    fields = np.stack([temporal+gradient,temporal-gradient],axis=1)
    return oracle.pack(fields,np.array([position,oracle.source*speed/np.sqrt(1-speed**2),clock]))
