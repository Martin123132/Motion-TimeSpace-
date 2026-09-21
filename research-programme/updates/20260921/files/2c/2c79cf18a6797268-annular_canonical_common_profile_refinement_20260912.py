from pathlib import Path

import numpy as numerical

from annular_adm_mixed_action_20260909 import MixedActionBasis, linear_value_gradient
from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
from annular_canonical_inverse_boundary_20260911 import InverseBoundaryInitialData
from annular_canonical_reference_fields_20260911 import hermite_fields, local_rate_families
from annular_canonical_mesh_transfer_20260911 import kinetic_weight
from annular_canonical_rate_completion_20260911 import OriginalFrames, bubbles, complete_phase, evaluate_initial
from annular_canonical_trace_context_20260911 import TraceContext, load_archive
from annular_canonical_trace_projection_stable_20260911 import kernel_family, trace_extension
from annular_canonical_trace_boundary_data_20260911 import BoundaryPreparation
from annular_gram_joint_action_20260909 import gram_matrices


def transfer_hermite(source_basis, coefficients, target_basis):
    value, gradient, unused_second = hermite_fields(source_basis, coefficients, target_basis.radii)
    return numerical.concatenate([value, target_basis.spacing * (gradient - target_basis.derivative @ value)])


class CommonProfile:
    def __init__(self, root):
        self.root = Path(root)
        self.coarse = TraceContext(root, 'metric_Gram')
        self.prepared_path = self.root / 'source-intake/navier-stokes/20260911/annular-canonical-trace-boundary-control-attempt01/MTS_prepared_initial_data.npz'
        self.prepared = load_archive(self.prepared_path)
        self.source = load_archive(self.coarse.source_path)
        self.packed = (self.source['initial_root_box_lower'] + self.source['initial_root_box_upper']) / 2

    def kinetic(self, points):
        return kinetic_weight(self.coarse.model, points)

    def physical_free(self, points):
        scalar, gradient, second = hermite_fields(self.coarse.basis, self.prepared['configuration'], points)
        auxiliary, auxiliary_r, unused_second = hermite_fields(self.coarse.basis, self.prepared['pi_coefficients'], points)
        weight, weight_r = self.kinetic(points)
        lapse = linear_value_gradient(self.coarse.basis.radii, points)[0] @ self.coarse.model.original_lapse
        return {'chi': scalar, 'w': gradient, 'w_r': second, 'pi': weight * auxiliary, 'pi_r': weight_r * auxiliary + weight * auxiliary_r, 'N_shape': lapse}


class RefinedFields:
    def __init__(self, context, selected):
        self.context, self.selected = context, selected

    def evaluate(self, points):
        context, selected = self.context, self.selected
        face, face_r = linear_value_gradient(context.basis.faces, points)
        eta, eta_r = linear_value_gradient(context.basis.radii, points)
        mass = face @ selected['mass_coefficients'][:context.basis.faces.size]
        mass_r = face_r @ selected['mass_coefficients'][:context.basis.faces.size]
        scalar, gradient, second = hermite_fields(context.basis, selected['configuration'], points)
        auxiliary, auxiliary_r, unused_second = hermite_fields(context.basis, selected['pi_coefficients'], points)
        weight, weight_r = context.common.kinetic(points)
        return {'chi': scalar, 'w': gradient, 'w_r': second, 'pi': weight * auxiliary, 'pi_r': weight_r * auxiliary + weight * auxiliary_r, 'mu': mass, 'mu_r': mass_r, 'F': 1 - 2 * mass / points, 'F_r': -2 * mass_r / points + 2 * mass / points**2, 'N': eta @ selected['fixed_lapse'], 'N_r': eta_r @ selected['fixed_lapse']}


class RefinedContext:
    def __init__(self, common, intervals, branch):
        if intervals not in [16, 32, 64] or branch not in ['GR', 'metric_Gram']:
            raise ValueError('Declared nested meshes and branches only.')
        self.common, self.root, self.branch = common, common.root, branch
        self.include_gram = branch == 'metric_Gram'
        self.basis = MixedActionBasis(numerical.linspace(common.coarse.basis.radii[0], common.coarse.basis.radii[-1], intervals + 1))
        basis = self.basis
        count = basis.radii.size
        self.links = MetricLinkQuadrature(basis)
        self.check_links = MetricLinkQuadrature(basis, order=12)
        coarse = common.coarse
        configuration = transfer_hermite(coarse.basis, common.prepared['configuration'], basis)
        auxiliary = transfer_hermite(coarse.basis, common.prepared['pi_coefficients'], basis)
        mass_seed = linear_value_gradient(coarse.basis.faces, basis.faces)[0] @ common.packed[coarse.system.slices[0]]
        lapse_seed = linear_value_gradient(coarse.basis.radii, basis.radii)[0] @ common.packed[coarse.system.slices[1]]
        velocity_seed = transfer_hermite(coarse.basis, common.packed[coarse.system.slices[2].start:], basis)
        packed = numerical.concatenate([mass_seed, lapse_seed, velocity_seed])
        self.system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], coarse.system.constants, .1, numerical.zeros(count), numerical.zeros(count), coarse.system.outer_clock, self.links)
        self.model = InverseBoundaryInitialData(self.system, packed, configuration, self.include_gram, common.prepared['boundary_velocity'].copy(), normalize_clock=True)
        mass_initial = linear_value_gradient(coarse.basis.faces, basis.faces)[0] @ common.prepared['mass_coefficients'][:coarse.basis.faces.size]
        self.model.mass_coeff_seed[0] = common.prepared['mass_coefficients'][0]
        self.model.pi_coeff_seed = auxiliary.copy()
        state = numerical.concatenate([mass_initial[1:], auxiliary[:count], common.prepared['state'][-3:]])
        self.model.set_state(state)
        self.saved = {'state': state, 'mass_coefficients': numerical.concatenate([mass_initial, numerical.zeros(count - 2)]), 'pi_coefficients': auxiliary, 'configuration': configuration, 'fixed_lapse': self.model.fixed_lapse.copy(), 'boundary_velocity': common.prepared['boundary_velocity'].copy(), 'canonical_kinetic_owner_intervals': numerical.array(16)}
        self.original = OriginalFrames(self.model)
        self.knots = numerical.unique(numerical.concatenate([self.original.knots, common.coarse.knots]))
        self.points, self.weights = self.quadrature(12)
        self.check_points, self.check_weights = self.quadrature(16)
        survey_knots = numerical.linspace(basis.radii[0], basis.radii[-1], 257)
        gauss, weights = numerical.polynomial.legendre.leggauss(4)
        halfwidth = numerical.diff(survey_knots) / 2
        survey = ((survey_knots[:-1] + survey_knots[1:])[:, None] / 2 + halfwidth[:, None] * gauss).ravel()
        self.survey_weights = (halfwidth[:, None] * weights).ravel()
        self.surfaces = {'quad': self.points, 'check': self.check_points, 'nodes': basis.radii, 'links': self.links.points, 'links_check': self.check_links.points, 'survey': survey}
        self.old_frames = {phase: {} for phase in ['mass', 'scalar']}
        self.reservoir = {}
        for surface, points in self.surfaces.items():
            maps = self.original.evaluate(points)
            maps['scalar']['p'] = common.kinetic(points)[0][:, None] * maps['scalar']['q']
            for phase in self.old_frames:
                self.old_frames[phase][surface] = maps[phase]
            value, gradient = bubbles(self.knots, points, 4)
            self.reservoir[surface] = {'q': value, 'qr': gradient}

    def quadrature(self, order):
        nodes, weights = numerical.polynomial.legendre.leggauss(order)
        halfwidth = numerical.diff(self.knots) / 2
        return ((self.knots[:-1] + self.knots[1:])[:, None] / 2 + halfwidth[:, None] * nodes).ravel(), (halfwidth[:, None] * weights).ravel()

    def build(self, selected=None):
        physical = RefinedFields(self, self.saved if selected is None else selected)
        data, reservoir = {}, self.reservoir
        families = {phase: {} for phase in self.old_frames}
        for surface, points in self.surfaces.items():
            eta, eta_r = linear_value_gradient(self.basis.radii, points)
            data[surface] = physical.evaluate(points)
            data[surface].update({'R': points, 'eta': eta, 'eta_r': eta_r})
            rates = local_rate_families(data[surface], points, eta, eta_r)
            for phase in families:
                families[phase][surface] = {kind: rates[phase + '_' + kind] for kind in ['q', 'qr', 'p']}
        frames, diagnostics = {}, {}
        for phase in families:
            frames[phase], diagnostics[phase] = complete_phase(self.old_frames[phase], families[phase], reservoir, self.weights)
        return data, frames, diagnostics


class RefinedPreparation(BoundaryPreparation):
    def __init__(self, context):
        self.context = context
        basis = context.basis
        self.face_count = basis.faces.size
        fraction = (basis.radii - basis.radii[0]) / (basis.radii[-1] - basis.radii[0])
        value = numerical.column_stack([1 - 3 * fraction**2 + 2 * fraction**3, 3 * fraction**2 - 2 * fraction**3])
        derivative = numerical.column_stack([-6 * fraction + 6 * fraction**2, 6 * fraction - 6 * fraction**2]) / (basis.radii[-1] - basis.radii[0])
        self.pi_lifts = numerical.concatenate([value, basis.spacing * (derivative - basis.derivative @ value)])
        self.face, self.face_r = linear_value_gradient(basis.faces, context.points)
        self.face_nodes = linear_value_gradient(basis.faces, basis.radii)[0]
        self.eta = linear_value_gradient(basis.radii, context.points)[0]
        factors, sampling = gram_matrices(basis.radii.size)
        self.gram_density = sampling.T @ (factors @ context.saved['configuration'][:basis.radii.size])**2 / (2 * basis.spacing) if context.include_gram else numerical.zeros(basis.radii.size)
        self.calls = 0

    def mass_equations(self, selected):
        context = self.context
        physical = RefinedFields(context, selected)
        values, nodes = physical.evaluate(context.points), physical.evaluate(context.basis.radii)
        radius, weights, geometry = context.points, context.weights, values['F']
        if numerical.real(geometry).min() <= .1 or numerical.real(nodes['F']).min() <= .1:
            raise ValueError('Trial leaves the positive annular chart.')
        energy = values['pi']**2 / (2 * radius**2) + radius**2 * values['w']**2 / 2
        constraint = self.eta.T @ (weights * (values['mu_r'] / (.1 * numerical.sqrt(geometry)) - numerical.sqrt(geometry) * energy))
        constraint -= context.basis.radii**2 * numerical.sqrt(nodes['F']) * self.gram_density
        coefficient = values['mu_r'] / (.1 * radius * geometry**1.5) + energy / (radius * numerical.sqrt(geometry))
        derivative = self.eta.T @ (weights[:, None] * (self.face_r[:, 1:] / (.1 * numerical.sqrt(geometry))[:, None] + coefficient[:, None] * self.face[:, 1:]))
        derivative += (context.basis.radii * self.gram_density / numerical.sqrt(nodes['F']))[:, None] * self.face_nodes[:, 1:]
        return constraint, derivative

    def evaluate(self, amplitudes):
        self.calls += 1
        selected = self.candidate(amplitudes)
        history = self.project_mass(selected)
        context = self.context
        data, frames, completion = context.build(selected)
        baseline = evaluate_initial(frames['mass'], frames['scalar'], data, context.basis, context.weights, context.links, context.include_gram, context.system.outer_clock)
        family, unused_primitive, unused_carrier = kernel_family(context, data, frames['mass'], baseline['P_rate_coeff'])
        extended, diagnostics = trace_extension(context, frames['mass'], family)
        actual = evaluate_initial(extended, frames['scalar'], data, context.basis, context.weights, context.links, context.include_gram, context.system.outer_clock)
        nodes = data['nodes']
        parent_inner = .1 * nodes['N'][0] * nodes['F'][0]**1.5 * nodes['pi'][0] * nodes['w'][0]
        parent_inner += .1 * numerical.sqrt(nodes['F'][0]) * actual['q_nodes'][0] * actual['gram_scalar'][0] / nodes['N'][0]
        bulk_coefficient = .1 * nodes['R'][0]**2 * nodes['F'][0] * nodes['w'][0]
        residual = numerical.array([(parent_inner - selected['boundary_velocity'][0]) / bulk_coefficient, actual['q_nodes'][-1] - selected['boundary_velocity'][2]])
        count = context.basis.radii.size
        selected['state'][:count] = selected['mass_coefficients'][1:self.face_count]
        selected['state'][count:2 * count] = selected['pi_coefficients'][:count]
        selected['state'][-3:] = actual['reactions']
        return {'residual': residual, 'saved': selected, 'data': data, 'frames': {'mass': extended, 'scalar': frames['scalar']}, 'baseline': baseline, 'actual': actual, 'mass_history': history, 'completion': completion, 'extension': diagnostics, 'parent_inner_mass_rate': float(parent_inner)}
