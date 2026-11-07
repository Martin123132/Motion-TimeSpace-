from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_background_time_tangent_20260928 import BackgroundLoads, FIELD_NAMES
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from annular_radial_time_forcing_20260928 import explicit_time_forcing
from annular_candidate_canonical_response_20260920 import solve_tangent
from annular_joint_first_tangent_20260922 import MetricResponse
from copy import copy
import numpy as np


def assemble_background(engine, action, progress):
    solver = copy(action.solver)
    solver.loads, solver.owner = engine.loads, engine.owner
    solver.rule, solver.label_order = ChebyshevRule(22), 28
    engine.owner.label_order = 28
    solver.nodes = solver.centers[:, None] + solver.lengths[:, None] * solver.rule.points / 2
    fields, field_rates = engine.sample(solver.nodes.ravel(), progress=progress)
    solver.fields = dict(fields, gram={engine.extension: fields['gram']})
    state = action.solution['state']
    mass, lapse = state.reshape(2, -1)
    forcing = explicit_time_forcing(solver.nodes.ravel(), mass, lapse, fields['source_density'], fields['velocity'],
        *[field_rates[name] for name in FIELD_NAMES], engine.owner.coupling, engine.owner.source_mass)
    tangent, residual, history = solve_tangent(solver, state, engine.extension, forcing)
    unused, local = solver.rhs(state, engine.extension, True)
    rhs = (np.einsum('abn,bn->an', local, tangent.reshape(2, -1)) + forcing).reshape(2, *solver.nodes.shape)
    coefficients = rhs @ solver.rule.inverse.T
    primitives = np.stack([np.polynomial.chebyshev.chebint(values.T).T * solver.lengths[:, None] / 2 for values in coefficients])
    for component in range(2):
        primitives[component, :, 0] -= np.polynomial.chebyshev.chebval(-1., primitives[component].T)
    increments = np.array([np.polynomial.chebyshev.chebval(1., values.T) for values in primitives])
    outer = -sum(increments[0]) / (solver.edges[-1] - 2 * state[0, -1, -1])
    left = np.array([np.r_[0., np.cumsum(increments[0, :-1])],
        outer - sum(increments[1]) + np.r_[0., np.cumsum(increments[1, :-1])]])
    solution = dict(state=tangent, rhs_coefficients=coefficients, primitives=primitives, left=left)
    response = MetricResponse(solver, solution, forcing, residual, history)
    response.fields, response.field_rates = fields, field_rates
    response.grid_rate = np.zeros_like(solver.nodes)
    response.edge_rates = np.zeros_like(solver.edges)
    response.edge_velocity_spread = None
    response.background_residual = float(np.max(abs(solver.residual(state, engine.extension))))
    return response


def complex_radial_response(response, action, extension):
    step = 1e-28
    solver = copy(response.solver)
    solver.fields = {name: response.fields[name] + 1j * step * response.field_rates[name] for name in FIELD_NAMES}
    solver.fields['gram'] = {extension: solver.fields['gram']}
    current = action.solution['state'].astype(complex)
    for unused in range(30):
        rhs = solver.rhs(current, extension)
        mass = solver.owner.central_mass + solver.integrated(rhs[0])
        primitive = solver.integrated(rhs[1])
        lapse = .5 * np.log(1 - 2 * mass[-1, -1] / solver.edges[-1]) + primitive - primitive[-1, -1]
        current = np.stack([mass, lapse])
    return current.imag / step
