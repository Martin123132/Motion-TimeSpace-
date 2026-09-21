import numpy as np
from scipy.linalg import solve_banded
from annular_flat_preassembled_flow_20260916 import polynomial, derivative, band_product


def second_polynomial(coefficients, displacement):
    return polynomial([degree*(degree-1)*value for degree,value in enumerate(coefficients) if degree>=2],displacement)


def dense_bands(bands):
    count = bands.shape[1]
    result = np.zeros((count,count),dtype=bands.dtype)
    for offset in range(-2,3):
        columns = np.arange(max(0,-offset),min(count,count-offset))
        result[columns+offset,columns] = bands[2+offset,columns]
    return result


class CanonicalEnergy:
    def __init__(self, model):
        self.model = model
        self.count = model.count
        self.configuration_count = self.count+1
        self.identity = np.eye(self.configuration_count)
        self.canonical_J = np.block([[np.zeros_like(self.identity),self.identity],[-self.identity,np.zeros_like(self.identity)]])

    def matrices(self, position):
        model = self.model
        values = model.matrices(position)
        displacement = position-model.system.anchor
        values['mass_bb'] = second_polynomial(model.mass,displacement)
        values['transport_bb'] = second_polynomial(model.transport,displacement)
        for name,coefficients in [('square',model.square),('bulk',model.bulk),('gram',model.gram)]:
            terms = []
            for side in range(2):
                slope = model.jacobian_slopes[side]
                jacobian = 1+slope*displacement
                terms.append(second_polynomial(coefficients[side],displacement)/jacobian
                    -2*slope*derivative(coefficients[side],displacement)/jacobian**2
                    +2*slope**2*polynomial(coefficients[side],displacement)/jacobian**3)
            values[name+'_bb'] = terms[0]+terms[1]
        return values

    def lagrangian(self, state, blocks=False):
        model,count = self.model,self.count
        field,position = state[:count],state[count]
        velocity,speed = state[count+1:2*count+1],state[2*count+1]
        matrices = self.matrices(position)
        factor = model.lifted @ field

        def stiffness(suffix):
            return band_product(matrices['bulk'+suffix],field)+model.lifted_transpose @ (matrices['gram'+suffix]*factor)

        cross = band_product(matrices['transport'],field)
        square = band_product(matrices['square'],field)
        momentum = np.append(band_product(matrices['mass'],velocity)+speed*cross,
            velocity @ cross+speed*field @ square+model.system.source_mass*speed/np.sqrt(1-speed**2))
        gradient = np.append(speed*band_product(matrices['transport'],velocity,True)+speed**2*square-stiffness(''),
            velocity @ band_product(matrices['mass_b'],velocity)/2
            +speed*velocity @ band_product(matrices['transport_b'],field)
            +speed**2*field @ band_product(matrices['square_b'],field)/2-field @ stiffness('_b')/2)
        result = dict(momentum=momentum,gradient=gradient,
            canonical_state=np.concatenate([state[:count+1],momentum]),
            Hamiltonian_gradient=np.concatenate([-gradient,state[count+1:2*count+2]]))
        if not blocks:
            return result
        mass,transport,square_matrix = [dense_bands(matrices[name]) for name in ['mass','transport','square']]
        inertia = model.system.source_mass/(1-speed**2)**1.5
        mass_inverse = solve_banded((2,2),matrices['mass'],np.eye(count),check_finite=False)
        inverse_cross = mass_inverse @ cross
        schur = inertia+field @ square-cross @ inverse_cross
        kinetic = np.block([[mass,cross[:,None]],[cross[None,:],np.array([[inertia+field @ square]])]])
        inverse = np.block([[mass_inverse+np.outer(inverse_cross,inverse_cross)/schur,-inverse_cross[:,None]/schur],
            [-inverse_cross[None,:]/schur,np.array([[1/schur]])]])
        mixed = np.empty((count+1,count+1),dtype=state.dtype)
        mixed[:-1,:-1] = speed*transport
        mixed[:-1,-1] = band_product(matrices['mass_b'],velocity)+speed*band_product(matrices['transport_b'],field)
        mixed[-1,:-1] = transport.T @ velocity+2*speed*square
        mixed[-1,-1] = velocity @ band_product(matrices['transport_b'],field)+speed*field @ band_product(matrices['square_b'],field)
        coordinate = np.empty_like(mixed)
        stiffness_matrix = dense_bands(matrices['bulk'])+(model.lifted_transpose @ model.lifted.multiply(matrices['gram'][:,None])).toarray()
        coordinate[:-1,:-1] = speed**2*square_matrix-stiffness_matrix
        coordinate[:-1,-1] = speed*band_product(matrices['transport_b'],velocity,True)+speed**2*band_product(matrices['square_b'],field)-stiffness('_b')
        coordinate[-1,:-1] = coordinate[:-1,-1]
        coordinate[-1,-1] = velocity @ band_product(matrices['mass_bb'],velocity)/2
        coordinate[-1,-1] += speed*velocity @ band_product(matrices['transport_bb'],field)
        coordinate[-1,-1] += speed**2*field @ band_product(matrices['square_bb'],field)/2-field @ stiffness('_bb')/2
        result.update(kinetic=kinetic,kinetic_inverse=inverse,mixed=mixed,coordinate=coordinate,schur=schur)
        return result

    def evaluate(self, state):
        blocks = self.lagrangian(state,True)
        inverse,mixed,coordinate = [blocks[name] for name in ['kinetic_inverse','mixed','coordinate']]
        zero = np.zeros_like(self.identity)
        inverse_mixed = inverse @ mixed
        transform = np.block([[self.identity,zero],[mixed,blocks['kinetic']]])
        inverse_transform = np.block([[self.identity,zero],[-inverse_mixed,inverse]])
        hessian = np.block([[-coordinate+mixed.T @ inverse_mixed,-inverse_mixed.T],[-inverse_mixed,inverse]])
        blocks.update(transform=transform,inverse_transform=inverse_transform,hessian=hessian)
        return blocks

    def stability(self, state, derivative, beta=1.):
        blocks = self.evaluate(state)
        model = self.model
        residual = model.evaluate(state)['flow']-derivative
        scale = 1e-25
        changing = self.evaluate(state.astype(complex)+scale*1j*derivative)
        residual_change = self.evaluate(state.astype(complex)+scale*1j*residual)
        hessian = blocks['hessian']
        hessian_rate = changing['hessian'].imag/scale
        correction = residual_change['transform'].imag/scale @ blocks['inverse_transform']
        canonical = self.canonical_J @ hessian
        generator = canonical-correction
        source = np.zeros_like(hessian)
        source[self.count,self.count] = beta
        metric = hessian+source
        symmetric_rate = hessian_rate+source @ canonical+canonical.T @ source-metric @ correction-correction.T @ metric
        blocks.update(metric=metric,metric_rate=hessian_rate,generator=generator,
            symmetric_rate=symmetric_rate,canonical_generator=canonical,
            reference_residual_correction=correction,reference_residual=residual,
            transform_rate=changing['transform'].imag/scale,
            forcing=blocks['transform'] @ residual[:-1])
        return blocks
