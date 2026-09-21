import numpy as np
from scipy.sparse import csr_matrix, diags
from scipy.sparse.linalg import eigsh
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_boundary_response_20260916 import field_matrices
from verify_annular_quadratic_crossing_precision_20260915_v2 import shape_force as unrelaxed_shape_force


class RelaxedTraceSourceAction(LocallyRefinedSourceAction):
    def __init__(self, base_count=17, gram=True, order=10, background_mass=0., anchor=6.03, source_splits=1):
        super().__init__(base_count, gram, order, background_mass, anchor, source_splits)
        self.branch_name = 'relaxed_auxiliary_trace_candidate' if gram else 'reference'

    def gram_data(self, position, scalar):
        raise ValueError('Use trace_data with the physical source position; the old physical-jump helper is not this candidate action.')

    def trace_data(self, time, coordinates):
        radius, jacobian, unused = self.mapping(self.radii, coordinates[-1])
        nodal = self.coefficient(time, radius)
        weights = np.asarray(self.sampling @ (nodal/jacobian))/self.gram_spacing
        values = self.original @ coordinates[:-1]
        denominator = self.lifted_hinge @ (weights*self.lifted_hinge)
        if self.gram:
            if np.real(denominator) <= 0:
                raise ValueError('Relaxed trace requires positive hinge weight.')
            auxiliary = self.lifted_hinge @ (weights*values)/denominator
        else:
            auxiliary = 0.*np.sum(coordinates)
        residual = values-self.lifted_hinge*auxiliary
        return dict(auxiliary_trace=auxiliary, physical_reference_jump=self.jump @ coordinates[:-1],
                    residual=residual, weights=weights, denominator=denominator, node_jacobian=jacobian)

    def evaluate(self, time, coordinates, rates, pulled=None):
        data = super().evaluate(time, coordinates, rates, pulled=pulled)
        trace = self.trace_data(time, coordinates)
        potential = np.dot(data['weight']*data['coefficient'], data['field_radial']**2)/2
        potential += np.dot(trace['weights'], trace['residual']**2)/2
        indices, radial = self.reference_indices, self.reference_radial
        unused, jacobian, displacement = self.mapping(self.reference_radius, coordinates[-1])
        motion = -displacement[:, None]*radial/jacobian[:, None]
        temporal_weight = data['weight']*data['radius']**4/data['coefficient']
        covector = self.assemble_quadratic(indices, rates[-1]*motion*(temporal_weight*data['field_time'])[:, None]
                    -radial*(self.reference_weight*data['coefficient']*data['field_radial'])[:, None])
        covector -= self.original.T @ (trace['weights']*trace['residual'])
        data.update(potential=potential, action=data['kinetic']-potential-self.source_mass*data['clock'],
                    wave_action=data['kinetic']-potential, scalar_covector=covector,
                    nodal_dual=-(self.sampling.T @ trace['residual']**2)/(2*self.gram_spacing*trace['node_jacobian']),
                    auxiliary_trace=trace['auxiliary_trace'], physical_reference_jump=trace['physical_reference_jump'],
                    relaxed_Gram_energy=np.dot(trace['weights'], trace['residual']**2)/2,
                    auxiliary_stationarity=self.lifted_hinge @ (trace['weights']*trace['residual']))
        return data


def relaxed_shape_force(system, instant, coordinates, rates):
    result = unrelaxed_shape_force(system, instant, coordinates, rates)
    trace = system.trace_data(instant, coordinates)
    radius, jacobian, displacement = system.mapping(system.radii, coordinates[-1])
    jacobian_b = np.where(system.radii < system.anchor, 1/(system.anchor-system.radii[0]), -1/(system.radii[-1]-system.anchor))
    coefficient = system.coefficient(instant, radius)
    radial_coefficient = system.coefficient(instant, radius+1e-24j).imag/1e-24
    gamma = np.asarray(system.sampling.T @ trace['residual']**2)/(2*system.gram_spacing)
    relaxed_force = float(-gamma @ (radial_coefficient*displacement/jacobian-coefficient*jacobian_b/jacobian**2))
    old_gram = result['Gram_shape_force']
    result.update(derived_force=result['derived_force']-old_gram+relaxed_force,
                  Gram_shape_force=relaxed_force, unused_unrelaxed_diagnostic_Gram_force=old_gram,
                  auxiliary_trace=float(trace['auxiliary_trace']), physical_reference_jump=float(trace['physical_reference_jump']))
    return result


def relaxed_spectral_step(system, state):
    coordinates, rates = np.split(state[:-1], 2)
    matrices = field_matrices(system, coordinates[-1])
    trace = system.trace_data(0., coordinates)
    stiffness = matrices['bulk']+system.original.T @ diags(trace['weights']) @ system.original
    if system.gram:
        contact = np.asarray(system.original.T @ (trace['weights']*system.lifted_hinge)).ravel()
        stiffness -= csr_matrix(contact[:, None]) @ csr_matrix(contact[None, :])/trace['denominator']
    values, vectors = eigsh(stiffness, k=1, M=matrices['mass'], which='LM', tol=1e-11, v0=np.linspace(1., 2., system.count))
    eigenvalue, vector = float(values[0]), vectors[:, 0]
    residual = float(np.linalg.norm(stiffness @ vector-eigenvalue*(matrices['mass'] @ vector))/np.linalg.norm(stiffness @ vector))
    data = system.evaluate(0., coordinates, rates)
    lapse, root = system.metric(0., coordinates[-1])
    material = system.source_mass*lapse**2/(root**2*data['clock']**3)
    frequency = float(np.sqrt(eigenvalue*data['source_inertia']/material))
    return dict(largest_field_eigenvalue=eigenvalue, eigen_residual=residual, frequency_estimate=frequency,
                maximum_step=float(min(.2*system.spacing, .8/(1.25*frequency))),
                relaxed_stiffness_used=True, nonlinear_stability_proven=False)
