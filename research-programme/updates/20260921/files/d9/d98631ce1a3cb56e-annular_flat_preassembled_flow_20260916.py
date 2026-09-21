import numpy as np
from scipy.linalg import solve_banded


def band_product(bands, vector, transpose=False):
    result = np.zeros_like(vector, dtype=np.result_type(bands,vector))
    count = len(vector)
    for offset in range(-2,3):
        left, right = max(0,-offset), min(count,count-offset)
        if transpose:
            result[left:right] += bands[2+offset,left:right]*vector[left+offset:right+offset]
        else:
            result[left+offset:right+offset] += bands[2+offset,left:right]*vector[left:right]
    return result


def polynomial(coefficients, displacement):
    result = coefficients[-1].copy()
    for coefficient in coefficients[-2::-1]:
        result = result*displacement+coefficient
    return result


def derivative(coefficients, displacement):
    return polynomial([degree*value for degree,value in enumerate(coefficients) if degree],displacement)


class FlatPreassembledFlow:
    def __init__(self, system):
        if system.background_mass != 0.:
            raise ValueError('This exact preassembly is qualified only for the flat prescribed background.')
        self.system, self.count = system, system.count
        radius = system.reference_radius
        unused,unused2,displacement = system.mapping(radius,system.anchor)
        inner,outer = system.radii[[0,-1]]
        self.jacobian_slopes = np.array([1/(system.anchor-inner),-1/(outer-system.anchor)])
        side = radius<system.anchor
        jacobian_slope = np.where(side,*self.jacobian_slopes)
        square = [radius**2,2*radius*displacement,displacement**2]

        def assemble(left, right, weight):
            bands = np.zeros((5,self.count))
            indices = system.reference_indices
            for first in range(3):
                for second in range(3):
                    values = system.reference_weight*weight*left[:,first]*right[:,second]
                    selected = values!=0.
                    rows,columns = indices[selected,first],indices[selected,second]
                    np.add.at(bands,(2+rows-columns,columns),values[selected])
            return bands

        shape,radial = system.reference_shape,system.reference_radial
        mass_weights = [square[0],square[1]+jacobian_slope*square[0],
            square[2]+jacobian_slope*square[1],jacobian_slope*square[2]]
        self.mass = np.array([assemble(shape,shape,value) for value in mass_weights])
        self.transport = np.array([assemble(shape,radial,-displacement*value) for value in square])
        self.square, self.bulk, self.gram = [],[],[]
        nodes = system.radii
        unused,unused2,nodal_displacement = system.mapping(nodes,system.anchor)
        for selected,nodal_selected in [(side,nodes<system.anchor),(~side,nodes>=system.anchor)]:
            self.square.append(np.array([assemble(radial,radial,selected*displacement**2*value) for value in square]))
            self.bulk.append(np.array([assemble(radial,radial,selected*value) for value in square]))
            self.gram.append(np.array([np.asarray(system.sampling @ (nodal_selected*value))/system.gram_spacing
                for value in [nodes**2,2*nodes*nodal_displacement,nodal_displacement**2]]))
        self.lifted, self.lifted_transpose = system.lifted.tocsr(),system.lifted.T.tocsr()

    def matrices(self, position):
        displacement = position-self.system.anchor
        jacobians = 1+self.jacobian_slopes*displacement
        if np.min(np.real(jacobians))<=0.:
            raise ValueError('Nonpositive source map.')
        mass = polynomial(self.mass,displacement)
        transport = polynomial(self.transport,displacement)
        values = dict(mass=mass,mass_b=derivative(self.mass,displacement),
            transport=transport,transport_b=derivative(self.transport,displacement))
        for name,coefficients in [('square',self.square),('bulk',self.bulk),('gram',self.gram)]:
            terms,derivatives = [],[]
            for side in range(2):
                numerator = polynomial(coefficients[side],displacement)
                terms.append(numerator/jacobians[side])
                derivatives.append(derivative(coefficients[side],displacement)/jacobians[side]
                    -numerator*self.jacobian_slopes[side]/jacobians[side]**2)
            values[name],values[name+'_b'] = terms[0]+terms[1],derivatives[0]+derivatives[1]
        return values

    def evaluate(self, state, diagnostics=False):
        coordinates,rates = np.split(state[:-1],2)
        field,position,velocity,speed = coordinates[:-1],coordinates[-1],rates[:-1],rates[-1]
        clock_squared = 1-speed**2
        if np.real(clock_squared)<=0.:
            raise ValueError('Source left the timelike branch.')
        clock = np.sqrt(clock_squared)
        material_inertia = self.system.source_mass/clock**3
        matrices = self.matrices(position)
        factor = self.lifted @ field
        cross = band_product(matrices['transport'],field)
        square_field = band_product(matrices['square'],field)
        stiffness_field = band_product(matrices['bulk'],field)+self.lifted_transpose @ (matrices['gram']*factor)
        transport_velocity = band_product(matrices['transport'],velocity)
        mass_b_velocity = band_product(matrices['mass_b'],velocity)
        drift_velocity = mass_b_velocity+transport_velocity-band_product(matrices['transport'],velocity,True)
        field_rhs = -speed*drift_velocity-stiffness_field-speed**2*(band_product(matrices['transport_b'],field)-square_field)
        source_rhs = velocity @ (mass_b_velocity/2-transport_velocity)-2*speed*velocity @ square_field
        source_rhs -= speed**2*(field @ band_product(matrices['square_b'],field))/2
        source_rhs -= (field @ band_product(matrices['bulk_b'],field)+factor @ (matrices['gram_b']*factor))/2
        solved = solve_banded((2,2),matrices['mass'],np.column_stack([field_rhs,cross]),check_finite=False)
        schur = material_inertia+field @ square_field-cross @ solved[:,1]
        if np.real(schur)<=0.:
            raise ValueError('Nonpositive original coupled inertia.')
        source_acceleration = (source_rhs-cross @ solved[:,0])/schur
        acceleration = np.append(solved[:,0]-solved[:,1]*source_acceleration,source_acceleration)
        result = dict(flow=np.concatenate([rates,acceleration,[clock]]),force=material_inertia*source_acceleration,
            acceleration=acceleration,schur=schur)
        if diagnostics:
            kinetic = velocity @ band_product(matrices['mass'],velocity)/2+speed*velocity @ cross+speed**2*field @ square_field/2
            potential = field @ stiffness_field/2
            result.update(action=kinetic-potential-self.system.source_mass*clock,
                energy=kinetic+potential+self.system.source_mass/clock)
        return result

    def rhs(self, instant, state):
        return self.evaluate(state)['flow']
