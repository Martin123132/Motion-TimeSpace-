import numpy as np
from scipy.linalg import solve_banded
from annular_flat_preassembled_flow_20260916 import band_product
from annular_canonical_energy_20260917 import CanonicalEnergy


class MatrixFreeAdjoint:
    def __init__(self, model):
        self.model,self.count = model,model.count

    def context(self, state):
        model,count = self.model,self.count
        field,position = state[:count],state[count]
        velocity,speed = state[count+1:2*count+1],state[2*count+1]
        matrices = CanonicalEnergy.matrices(self,position)
        value = model.evaluate(state)
        cross = band_product(matrices['transport'],field)
        inverse_cross = solve_banded((2,2),matrices['mass'],cross,check_finite=False)
        return dict(state=state,field=field,position=position,velocity=velocity,speed=speed,
            matrices=matrices,value=value,cross=cross,inverse_cross=inverse_cross,
            inertia=model.system.source_mass/(1-speed**2)**1.5,
            inertia_speed=3*model.system.source_mass*speed/(1-speed**2)**2.5)

    def kinetic_solve(self, context, right):
        solved = solve_banded((2,2),context['matrices']['mass'],right[:-1],check_finite=False)
        source = (right[-1]-context['cross'] @ solved)/context['value']['schur']
        return np.append(solved-context['inverse_cross']*source,source)

    def stiffness(self, matrices, vector, suffix=''):
        model = self.model
        return band_product(matrices['bulk'+suffix],vector)+model.lifted_transpose @ (matrices['gram'+suffix]*(model.lifted @ vector))

    def transpose(self, state, covector, context=None):
        context = self.context(state) if context is None else context
        count = self.count
        field,velocity,speed,matrices = [context[name] for name in ['field','velocity','speed','matrices']]
        acceleration = context['value']['acceleration'][:-1]
        source_acceleration = context['value']['acceleration'][-1]
        dual = self.kinetic_solve(context,covector[count+1:2*count+2])
        field_dual,source_dual = dual[:-1],dual[-1]

        def product(name,vector,transpose=False):
            return band_product(matrices[name],vector,transpose)

        square_field = product('square',field)
        field_row = -2*speed*product('square',velocity)-speed**2*product('square_b',field)-self.stiffness(matrices,field,'_b')
        field_row -= product('transport',acceleration,True)+2*source_acceleration*square_field
        field_result = -self.stiffness(matrices,field_dual)-speed**2*(product('transport_b',field_dual,True)-product('square',field_dual))
        field_result -= source_acceleration*product('transport',field_dual,True)
        field_result += source_dual*field_row
        velocity_row = product('mass_b',velocity)-product('transport',velocity)-product('transport',velocity,True)-2*speed*square_field
        velocity_result = -speed*(product('mass_b',field_dual)+product('transport',field_dual,True)-product('transport',field_dual))
        velocity_result += source_dual*velocity_row
        field_b = -speed*(product('mass_bb',velocity)+product('transport_b',velocity)-product('transport_b',velocity,True))
        field_b -= self.stiffness(matrices,field,'_b')+speed**2*(product('transport_bb',field)-product('square_b',field))
        field_b -= product('mass_b',acceleration)+source_acceleration*product('transport_b',field)
        source_b = velocity @ (product('mass_bb',velocity)/2-product('transport_b',velocity))
        source_b -= 2*speed*velocity @ product('square_b',field)
        source_b -= speed**2*field @ product('square_bb',field)/2+field @ self.stiffness(matrices,field,'_bb')/2
        source_b -= product('transport_b',field) @ acceleration+source_acceleration*field @ product('square_b',field)
        field_speed = -product('mass_b',velocity)-product('transport',velocity)+product('transport',velocity,True)
        field_speed -= 2*speed*(product('transport_b',field)-square_field)
        source_speed = -2*velocity @ square_field-speed*field @ product('square_b',field)-context['inertia_speed']*source_acceleration
        result = np.zeros_like(covector)
        result[:count] = field_result
        result[count] = field_dual @ field_b+source_dual*source_b
        result[count+1:2*count+1] = velocity_result+covector[:count]
        result[2*count+1] = field_dual @ field_speed+source_dual*source_speed+covector[count]
        result[2*count+1] -= covector[-1]*speed/np.sqrt(1-speed**2)
        return result

    def force_gradient(self, state, context=None):
        context = self.context(state) if context is None else context
        covector = np.zeros_like(state)
        covector[2*self.count+1] = context['inertia']
        result = self.transpose(state,covector,context)
        result[2*self.count+1] += context['inertia_speed']*context['value']['acceleration'][-1]
        return result

    def canonical_covector(self, state, covector, context=None):
        context = self.context(state) if context is None else context
        count = self.count
        field,velocity,speed,matrices = [context[name] for name in ['field','velocity','speed','matrices']]
        momentum = self.kinetic_solve(context,covector[count+1:2*count+2])
        mixed_field = speed*band_product(matrices['transport'],momentum[:-1],True)
        mixed_field += momentum[-1]*(band_product(matrices['transport'],velocity,True)+2*speed*band_product(matrices['square'],field))
        mixed_source = momentum[:-1] @ (band_product(matrices['mass_b'],velocity)+speed*band_product(matrices['transport_b'],field))
        mixed_source += momentum[-1]*(velocity @ band_product(matrices['transport_b'],field)+speed*field @ band_product(matrices['square_b'],field))
        position = covector[:count+1]-np.append(mixed_field,mixed_source)
        return np.concatenate([position,momentum])

    def gram_density(self, state, covector, context=None):
        context = self.context(state) if context is None else context
        canonical = self.canonical_covector(state,covector,context)
        momentum = canonical[self.count+1:]
        factor = self.model.lifted @ state[:self.count]
        matrices = context['matrices']
        return -(self.model.lifted @ momentum[:-1]) @ (matrices['gram']*factor)-momentum[-1]*factor @ (matrices['gram_b']*factor)/2
