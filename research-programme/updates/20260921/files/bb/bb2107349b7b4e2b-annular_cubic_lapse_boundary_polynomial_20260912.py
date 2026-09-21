import numpy as numerical
from scipy.linalg import solve

from annular_adm_mixed_action_20260909 import linear_value_gradient
from annular_canonical_common_profile_aligned_20260912 import RefinedContext, RefinedFields, RefinedPreparation
from annular_canonical_rate_completion_20260911 import complete_phase, normalized_transform
from annular_canonical_reference_fields_20260911 import local_rate_families
from annular_canonical_trace_projection_stable_20260911 import GlobalPrimitive, kernel_family, trace_extension
from annular_gram_joint_action_20260909 import gram_matrices


class CubicFamily:
    def __init__(self, context):
        self.basis = context.basis
        self.length = self.basis.radii[-1] - self.basis.radii[0]
        self.knots = context.knots
        hats = linear_value_gradient(self.basis.radii, context.points)[0]
        raw = self.raw(context.points)[0]
        self.projection = solve(hats.T @ (context.weights[:, None] * hats), hats.T @ (context.weights[:, None] * raw))
        residual = raw - hats @ self.projection
        self.transform = normalized_transform(residual, context.weights)
        extended = numerical.longdouble
        length = extended(self.length)
        widths = numerical.diff(self.basis.radii).astype(extended)
        fraction = (self.basis.radii[:-1].astype(extended) - extended(self.basis.radii[0])) / length
        coefficients = numerical.empty((len(widths), 4, 2), dtype=extended)
        coefficients[:, 0, 0] = length * (fraction**3 - 2 * fraction**2 + fraction)
        coefficients[:, 0, 1] = length * (fraction**3 - fraction**2)
        coefficients[:, 1, 0] = widths * (3 * fraction**2 - 4 * fraction + 1)
        coefficients[:, 1, 1] = widths * (3 * fraction**2 - 2 * fraction)
        coefficients[:, 2, 0] = widths**2 / length * (3 * fraction - 2)
        coefficients[:, 2, 1] = widths**2 / length * (3 * fraction - 1)
        coefficients[:, 3, :] = (widths**3 / length**2)[:, None]
        projection = self.projection.astype(extended)
        coefficients[:, 0] -= projection[:-1]
        coefficients[:, 1] -= projection[1:] - projection[:-1]
        self.polynomials = numerical.asarray(coefficients @ self.transform.astype(extended), dtype=float)
        integrals = widths[:, None] * numerical.sum(coefficients @ self.transform.astype(extended) / numerical.arange(1, 5, dtype=extended)[None, :, None], axis=1)
        self.prefix = numerical.asarray(numerical.concatenate([numerical.zeros((1, 2), dtype=extended), numerical.cumsum(integrals, axis=0)]), dtype=float)
        self.endpoint_origin = numerical.zeros(2)
        self.endpoint_drift = self.prefix[-1].copy()
        self.mass_scale = numerical.ones(2)
        self.mass_scale = numerical.sqrt(context.weights @ self.mass(context.points)[0]**2)

    def raw(self, points):
        fraction = (points - self.basis.radii[0]) / self.length
        values = self.length * numerical.column_stack([fraction**3 - 2 * fraction**2 + fraction, fraction**3 - fraction**2])
        gradients = numerical.column_stack([3 * fraction**2 - 4 * fraction + 1, 3 * fraction**2 - 2 * fraction])
        return values, gradients

    def local(self, points):
        cell = numerical.clip(numerical.searchsorted(self.basis.radii, points, side='right') - 1, 0, self.basis.radii.size - 2)
        width = self.basis.radii[cell + 1] - self.basis.radii[cell]
        fraction = (points - self.basis.radii[cell]) / width
        return cell, width, fraction[:, None], self.polynomials[cell]

    def evaluate(self, points):
        hats, hat_gradient = linear_value_gradient(self.basis.radii, points)
        unused_cell, width, fraction, coefficients = self.local(points)
        extra = coefficients[:, 0] + fraction * (coefficients[:, 1] + fraction * (coefficients[:, 2] + fraction * coefficients[:, 3]))
        extra_gradient = (coefficients[:, 1] + fraction * (2 * coefficients[:, 2] + 3 * fraction * coefficients[:, 3])) / width[:, None]
        return numerical.concatenate([hats, extra], axis=1), numerical.concatenate([hat_gradient, extra_gradient], axis=1)

    def mass(self, points):
        cell, width, fraction, coefficients = self.local(points)
        primitive = fraction * (coefficients[:, 0] + fraction * (coefficients[:, 1] / 2 + fraction * (coefficients[:, 2] / 3 + fraction * coefficients[:, 3] / 4)))
        global_fraction = (points - self.basis.radii[0]) / self.length
        values = self.prefix[cell] + width[:, None] * primitive - global_fraction[:, None] * self.endpoint_drift
        gradients = self.evaluate(points)[0][:, -2:] - self.endpoint_drift / self.length
        return values / self.mass_scale, gradients / self.mass_scale


class CubicFields(RefinedFields):
    def evaluate(self, points):
        result = super().evaluate(points)
        mass, mass_gradient = self.context.family.mass(points)
        result['mu'] += mass @ self.selected['mass_lift_coefficients']
        result['mu_r'] += mass_gradient @ self.selected['mass_lift_coefficients']
        result['F'] = 1 - 2 * result['mu'] / points
        result['F_r'] = -2 * result['mu_r'] / points + 2 * result['mu'] / points**2
        lift, lift_gradient = self.context.family.raw(points)
        result['N'] += lift @ self.selected['lapse_boundary_amplitudes']
        result['N_r'] += lift_gradient @ self.selected['lapse_boundary_amplitudes']
        return result


class CubicContext(RefinedContext):
    def __init__(self, common, branch):
        super().__init__(common, 16, branch)
        self.family = CubicFamily(self)
        self.saved['mass_lift_coefficients'] = numerical.zeros(2)
        self.saved['lapse_boundary_amplitudes'] = numerical.zeros(2)

    def build(self, selected=None):
        selected = self.saved if selected is None else selected
        physical = CubicFields(self, selected)
        data, families = {}, {phase: {} for phase in self.old_frames}
        for surface, points in self.surfaces.items():
            eta, eta_gradient = self.family.evaluate(points)
            data[surface] = physical.evaluate(points)
            data[surface].update({'R': points, 'eta': eta, 'eta_r': eta_gradient})
            rates = local_rate_families(data[surface], points, eta, eta_gradient)
            for phase in families:
                families[phase][surface] = {kind: rates[phase + '_' + kind] for kind in ['q', 'qr', 'p']}
            mass, mass_gradient = self.family.mass(points)
            families['mass'][surface]['q'] = numerical.concatenate([families['mass'][surface]['q'], mass], axis=1)
            families['mass'][surface]['qr'] = numerical.concatenate([families['mass'][surface]['qr'], mass_gradient], axis=1)
        frames, diagnostics = {}, {}
        for phase in families:
            frames[phase], diagnostics[phase] = complete_phase(self.old_frames[phase], families[phase], self.reservoir, self.weights)
        return data, frames, diagnostics


class CubicPreparation(RefinedPreparation):
    def __init__(self, context, correction=True):
        super().__init__(context)
        self.correction = correction
        mass, mass_gradient = context.family.mass(context.points)
        self.mass_map = numerical.concatenate([self.face, mass], axis=1)
        self.mass_gradient = numerical.concatenate([self.face_r, mass_gradient], axis=1)
        mass_nodes = context.family.mass(context.basis.radii)[0]
        self.mass_nodes = numerical.concatenate([self.face_nodes, mass_nodes], axis=1)
        self.eta = context.family.evaluate(context.points)[0]
        self.eta_nodes = context.family.evaluate(context.basis.radii)[0]

    def mass_equations(self, selected):
        context = self.context
        physical = CubicFields(context, selected)
        values, nodes = physical.evaluate(context.points), physical.evaluate(context.basis.radii)
        radius, weights, geometry = context.points, context.weights, values['F']
        if min(numerical.real(geometry).min(), numerical.real(nodes['F']).min()) <= .1:
            raise ValueError('Mass trial leaves the positive annular chart.')
        energy = values['pi']**2 / (2 * radius**2) + radius**2 * values['w']**2 / 2
        constraint = self.eta.T @ (weights * (values['mu_r'] / (.1 * numerical.sqrt(geometry)) - numerical.sqrt(geometry) * energy))
        constraint -= self.eta_nodes.T @ (context.basis.radii**2 * numerical.sqrt(nodes['F']) * self.gram_density)
        coefficient = values['mu_r'] / (.1 * radius * geometry**1.5) + energy / (radius * numerical.sqrt(geometry))
        derivative = self.eta.T @ (weights[:, None] * (self.mass_gradient[:, 1:] / (.1 * numerical.sqrt(geometry))[:, None] + coefficient[:, None] * self.mass_map[:, 1:]))
        derivative += self.eta_nodes.T @ ((context.basis.radii * self.gram_density / numerical.sqrt(nodes['F']))[:, None] * self.mass_nodes[:, 1:])
        return constraint, derivative

    def project_mass(self, selected):
        history = []
        for unused_iteration in range(12):
            residual, jacobian = self.mass_equations(selected)
            merit = float(abs(residual).max())
            history.append(merit)
            if merit < 2e-14:
                nodes = CubicFields(self.context, selected).evaluate(self.context.basis.radii)
                selected['fixed_lapse'] = self.context.model.original_lapse * self.context.system.outer_clock * numerical.sqrt(nodes['F'][-1]) / self.context.model.original_lapse[-1]
                selected['lapse_boundary_amplitudes'] = numerical.zeros(2)
                if self.correction:
                    values = CubicFields(self.context, selected).evaluate(self.context.basis.radii)
                    radius = self.context.basis.radii
                    energy = values['pi']**2 / (2 * radius**2) + radius**2 * values['w']**2 / 2
                    required = values['N'] * (.1 * energy / radius + values['mu'] / (radius**2 * values['F']))
                    selected['lapse_boundary_amplitudes'] = (required - values['N_r'])[[0, -1]]
                return history
            update = solve(jacobian, -residual)
            accepted = False
            for power in range(16):
                trial = {key: value.copy() for key, value in selected.items()}
                trial['mass_coefficients'][1:self.face_count] += update[:self.face_count - 1] * 2.**(-power)
                trial['mass_lift_coefficients'] += update[-2:] * 2.**(-power)
                try:
                    next_merit = float(abs(self.mass_equations(trial)[0]).max())
                except ValueError:
                    continue
                if next_merit < merit:
                    selected.update(trial)
                    accepted = True
                    break
            if not accepted:
                raise RuntimeError('Nineteen-row mass preparation stalled.')
        raise RuntimeError('Nineteen-row mass preparation iteration limit.')

    def evaluate(self, amplitudes):
        self.calls += 1
        selected = self.candidate(amplitudes)
        history = self.project_mass(selected)
        context = self.context
        data, frames, completion = context.build(selected)
        baseline = evaluate_cubic_initial(frames['mass'], frames['scalar'], data, context.basis, context.weights, context.links, context.include_gram, context.system.outer_clock)
        family, unused_primitive, unused_carrier = kernel_family(context, data, frames['mass'], baseline['P_rate_coeff'])
        extended, diagnostics = trace_extension(context, frames['mass'], family)
        actual = evaluate_cubic_initial(extended, frames['scalar'], data, context.basis, context.weights, context.links, context.include_gram, context.system.outer_clock)
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


def evaluate_cubic_initial(frame_mass, frame_scalar, data, basis, weights, links, gram, clock, reactions=None, surface='quad', link_surface='links'):
    radius = data[surface]['R']
    values = data[surface]
    nodes = data['nodes']
    mass_maps, scalar_maps = frame_mass[surface], frame_scalar[surface]
    mass_nodes, scalar_nodes = frame_mass['nodes']['q'], frame_scalar['nodes']['q']
    mass_pair = mass_maps['p'].T @ (weights[:, None] * mass_maps['q'])
    scalar_pair = scalar_maps['p'].T @ (weights[:, None] * scalar_maps['q'])
    geometry, lapse = values['F'], values['N']
    energy = values['pi']**2 / (2 * radius**2) + radius**2 * values['w']**2 / 2
    mass_density = lapse * values['mu_r'] / (.1 * radius * geometry**1.5) + lapse * energy / (radius * numerical.sqrt(geometry))
    mass_force = mass_maps['q'].T @ (weights * mass_density) + mass_maps['qr'].T @ (weights * lapse / (.1 * numerical.sqrt(geometry))) - clock / .1 * mass_nodes[-1]
    factors, sampling = gram_matrices(basis.radii.size)
    amplitude = factors @ nodes['chi']
    gram_density = sampling.T @ amplitude**2 / (2 * basis.spacing)
    mass_reaction = nodes['N'][0] / (.1 * numerical.sqrt(nodes['F'][0])) if reactions is None else reactions[0]
    mass_force += mass_reaction * mass_nodes[0]
    if gram:
        mass_force += mass_nodes.T @ (basis.radii * nodes['N'] * gram_density / numerical.sqrt(nodes['F']))
    momentum_rate = solve(mass_pair.T, mass_force)
    q_coeff = solve(scalar_pair, scalar_maps['p'].T @ (weights * lapse * numerical.sqrt(geometry) * values['pi'] / radius**2))
    q_nodes = scalar_nodes @ q_coeff
    gram_p_force = numerical.zeros(frame_mass[surface]['p'].shape[1])
    gram_scalar = numerical.zeros(basis.radii.size)
    density_time = numerical.zeros(basis.radii.size)
    transport = numerical.zeros(data['nodes']['eta'].shape[1])
    endpoint_log = numerical.zeros(links.node.size)
    if gram:
        link_values = data[link_surface]
        momentum_link = frame_mass[link_surface]['p']
        momentum_time = momentum_link @ momentum_rate
        generator = .1 * numerical.sqrt(link_values['F']) * momentum_time / link_values['N']
        endpoint_log, partial_log = links.integrate(generator), links.partial(generator)
        if max(abs(endpoint_log).max(), abs(partial_log).max()) > 50:
            raise ValueError('Completed phase jet leaves the bounded time-link chart.')
        endpoint, partial = numerical.exp(endpoint_log), numerical.exp(partial_log)
        coefficient = basis.radii**2 * nodes['N'] * numerical.sqrt(nodes['F'])
        density = links.collect(links.sweight * endpoint * coefficient[links.node])
        amplitude_time = links.collect(links.tweight * endpoint * q_nodes[links.node])
        current = amplitude[links.factor] * (links.sweight * coefficient[links.node] * amplitude_time[links.factor] - links.tweight * q_nodes[links.node] * density[links.factor]) / basis.spacing
        weighted_current = current * endpoint
        kernel = links.integrate(momentum_link * (.1 * numerical.sqrt(link_values['F']) / (link_values['N'] * partial**2))[:, None])
        gram_p_force = kernel.T @ weighted_current
        numerical.add.at(gram_scalar, links.node, -links.tweight * amplitude[links.factor] * density[links.factor] / (basis.spacing * endpoint))
        numerical.add.at(density_time, links.node, links.sweight * amplitude[links.factor] * amplitude_time[links.factor] / (basis.spacing * endpoint))
        node_values = data[link_surface]['eta']
        kernel_time = links.integrate(node_values * (.1 * numerical.sqrt(link_values['F']) * momentum_time / (link_values['N']**2 * partial**2))[:, None])
        transport = -(kernel_time.T @ weighted_current)
    scalar_flux_endpoints = basis.radii[[0, -1]]**2 * nodes['N'][[0, -1]] * numerical.sqrt(nodes['F'][[0, -1]]) * nodes['w'][[0, -1]]
    actual_reactions = numerical.array([mass_reaction, -scalar_flux_endpoints[0] - gram_scalar[0], scalar_flux_endpoints[1] - gram_scalar[-1]]) if reactions is None else reactions
    scalar_force = -(scalar_maps['qr'].T @ (weights * lapse * numerical.sqrt(geometry) * radius**2 * values['w'])) + scalar_nodes.T @ gram_scalar
    scalar_force += scalar_nodes[0] * actual_reactions[1] + scalar_nodes[-1] * actual_reactions[2]
    pi_rate = solve(scalar_pair.T, scalar_force)
    mass_rate = solve(mass_pair, mass_maps['p'].T @ (weights * .1 * lapse * geometry**1.5 * values['pi'] * values['w']) - gram_p_force)
    physical_mass_rate, physical_mass_rate_r = mass_maps['q'] @ mass_rate, mass_maps['qr'] @ mass_rate
    physical_pi_rate, physical_momentum_rate = scalar_maps['p'] @ pi_rate, mass_maps['p'] @ momentum_rate
    physical_q, physical_q_r = scalar_maps['q'] @ q_coeff, scalar_maps['qr'] @ q_coeff
    coefficient = values['mu_r'] / (.1 * radius * geometry**1.5) + energy / (radius * numerical.sqrt(geometry))
    density = physical_mass_rate_r / (.1 * numerical.sqrt(geometry)) + coefficient * physical_mass_rate
    density -= numerical.sqrt(geometry) * values['pi'] * physical_pi_rate / radius**2 + radius**2 * numerical.sqrt(geometry) * values['w'] * physical_q_r + .1 * geometry**1.5 * values['pi'] * values['w'] * physical_momentum_rate
    lapse_tests = data[surface]['eta']
    gram_rate = data['nodes']['eta'].T @ (basis.radii * gram_density * (mass_nodes @ mass_rate) / numerical.sqrt(nodes['F']) - basis.radii**2 * numerical.sqrt(nodes['F']) * density_time) + transport if gram else numerical.zeros(data['nodes']['eta'].shape[1])
    constraint_rate = lapse_tests.T @ (weights * density) + gram_rate
    constraint = lapse_tests.T @ (weights * (values['mu_r'] / (.1 * numerical.sqrt(geometry)) - numerical.sqrt(geometry) * energy))
    if gram:
        constraint -= data['nodes']['eta'].T @ (basis.radii**2 * numerical.sqrt(nodes['F']) * gram_density)
    return {'constraint': constraint, 'constraint_rate': constraint_rate, 'gram_constraint_rate': gram_rate, 'mu_t': physical_mass_rate, 'mu_tr': physical_mass_rate_r, 'P_t': physical_momentum_rate, 'pi_t': physical_pi_rate, 'q': physical_q, 'q_r': physical_q_r, 'mu_t_nodes': mass_nodes @ mass_rate, 'q_nodes': q_nodes, 'P_t_nodes': frame_mass['nodes']['p'] @ momentum_rate, 'gram_scalar': gram_scalar, 'endpoint_log': endpoint_log, 'reactions': actual_reactions, 'mass_pair': mass_pair, 'scalar_pair': scalar_pair, 'mass_rate_coeff': mass_rate, 'P_rate_coeff': momentum_rate, 'pi_rate_coeff': pi_rate, 'q_coeff': q_coeff}
