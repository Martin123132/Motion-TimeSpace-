import numpy as np
from scipy.linalg import cholesky_banded, cho_solve_banded
from annular_flat_preassembled_flow_20260916 import band_product
from annular_matrix_free_adjoint_20260917 import MatrixFreeAdjoint


class FrozenInitialLayer:
    def __init__(self, model, state):
        self.model, self.state = model, state.copy()
        self.count = model.count
        self.adjoint = MatrixFreeAdjoint(model)
        self.context = context = self.adjoint.context(state)
        self.matrices = matrices = context['matrices']
        self.mass_cholesky = cholesky_banded(matrices['mass'][2:], lower=True, check_finite=False)
        field, velocity, speed = context['field'], context['velocity'], context['speed']
        acceleration = context['value']['acceleration'][:-1]
        source_acceleration = context['value']['acceleration'][-1]
        self.base_flow = context['value']['flow'].copy()
        self.base_force = float(context['value']['force'])
        self.gradient = self.adjoint.force_gradient(state, context)

        def product(name, vector, transpose=False):
            return band_product(matrices[name], vector, transpose)

        self.source_field = -2*speed*product('square', velocity)-speed**2*product('square_b', field)
        self.source_field -= self.adjoint.stiffness(matrices, field, '_b')+product('transport', acceleration, True)
        self.source_field -= 2*source_acceleration*product('square', field)
        self.source_velocity = product('mass_b', velocity)-product('transport', velocity)-product('transport', velocity, True)
        self.source_velocity -= 2*speed*product('square', field)
        self.field_position = -speed*(product('mass_bb', velocity)+product('transport_b', velocity)-product('transport_b', velocity, True))
        self.field_position -= self.adjoint.stiffness(matrices, field, '_b')
        self.field_position -= speed**2*(product('transport_bb', field)-product('square_b', field))
        self.field_position -= product('mass_b', acceleration)+source_acceleration*product('transport_b', field)
        self.source_position = velocity @ (product('mass_bb', velocity)/2-product('transport_b', velocity))
        self.source_position -= 2*speed*velocity @ product('square_b', field)
        self.source_position -= speed**2*field @ product('square_bb', field)/2
        self.source_position -= field @ self.adjoint.stiffness(matrices, field, '_bb')/2
        self.source_position -= product('transport_b', field) @ acceleration
        self.source_position -= source_acceleration*field @ product('square_b', field)
        self.field_speed = -product('mass_b', velocity)-product('transport', velocity)+product('transport', velocity, True)
        self.field_speed -= 2*speed*(product('transport_b', field)-product('square', field))
        self.source_speed = -2*velocity @ product('square', field)-speed*field @ product('square_b', field)
        self.source_speed -= context['inertia_speed']*source_acceleration
        self.scale = np.ones(len(state))
        self.scale[:self.count+1] = model.system.gram_spacing
        self.scale[-1] = model.system.gram_spacing
        self.scaled_forcing = model.system.gram_spacing*self.base_flow/self.scale

    def multiply(self, vector):
        count, matrices, context = self.count, self.matrices, self.context
        field, position = vector[:count], vector[count]
        velocity, speed = vector[count+1:-2], vector[-2]
        base_speed = context['speed']
        source_acceleration = context['value']['acceleration'][-1]
        right = -self.adjoint.stiffness(matrices, field)
        right -= base_speed**2*(band_product(matrices['transport_b'], field)-band_product(matrices['square'], field))
        right -= source_acceleration*band_product(matrices['transport'], field)
        right -= base_speed*(band_product(matrices['mass_b'], velocity)+band_product(matrices['transport'], velocity)
            -band_product(matrices['transport'], velocity, True))
        right += self.field_position*position+self.field_speed*speed
        source_right = self.source_field @ field+self.source_velocity @ velocity+self.source_position*position+self.source_speed*speed
        solved = cho_solve_banded((self.mass_cholesky, True), right, check_finite=False)
        source_rate = (source_right-context['cross'] @ solved)/context['value']['schur']
        field_rate = solved-context['inverse_cross']*source_rate
        clock_rate = -base_speed*speed/np.sqrt(1-base_speed**2)
        return np.concatenate([velocity, [speed], field_rate, [source_rate, clock_rate]])

    def scaled_rhs(self, instant, perturbation):
        return self.scaled_forcing+self.model.system.gram_spacing*self.multiply(self.scale*perturbation)/self.scale

    def reconstruct(self, perturbations):
        displacements = perturbations*self.scale
        linear_force = self.base_force+displacements @ self.gradient
        evaluated_force = np.array([self.model.evaluate(self.state+displacement)['force'] for displacement in displacements])
        linear_rate = np.array([self.gradient @ (self.base_flow+self.multiply(displacement)) for displacement in displacements])
        return displacements, linear_force, evaluated_force, linear_rate
