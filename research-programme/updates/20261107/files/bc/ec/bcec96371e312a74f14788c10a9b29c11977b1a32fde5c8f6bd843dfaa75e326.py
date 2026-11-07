from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_joint_first_tangent_20260922 import joint_iteration
import numpy as np


class JointMetricTangent:
    def __init__(self, coordinate_rate, velocity_responses):
        self.coordinate_rate = coordinate_rate
        self.velocity_responses = velocity_responses

    def values(self, radius):
        partial = self.coordinate_rate.values(radius)
        return partial + np.array([response.values(radius) for response in self.velocity_responses])

    def at(self, radius):
        rate = self.values(radius)
        return rate[:, 1], -2 * rate[:, 0] / radius


def solve_joint_rhs(system, response, momentum_response, rhs, record):
    synthetic = dict(inverse=system['inverse'], matrix=system['matrix'], force=rhs,
                     convection=np.zeros((2,) + rhs.shape))
    return joint_iteration(synthetic, response, momentum_response, np.zeros_like(rhs), record)


def symbolic_checks(evidence):
    import sympy as sp
    coordinate, velocity = sp.symbols('q v', real=True)
    momentum = coordinate**2 * velocity + velocity**3 + 2 * velocity + coordinate
    force = coordinate * velocity + coordinate**3 - velocity
    geometry = coordinate**2 + coordinate * velocity + velocity**3
    inertia = sp.diff(momentum, velocity)
    acceleration = (force - sp.diff(momentum, coordinate) * velocity) / inertia
    flow_derivative = lambda value: sp.diff(value, coordinate) * velocity + sp.diff(value, velocity) * acceleration
    jerk = flow_derivative(acceleration)
    fixed_acceleration = sp.symbols('a0')
    residual = force - sp.diff(momentum, coordinate) * velocity - inertia * fixed_acceleration
    rhs = flow_derivative(residual).subs(fixed_acceleration, acceleration)
    evidence.check('symbolic_differentiated_Schur_equation', sp.simplify(inertia * jerk - rhs) == 0)
    gamma = flow_derivative(geometry)
    eta = flow_derivative(gamma)
    hessian = (sp.diff(geometry, coordinate, 2) * velocity**2
               + 2 * sp.diff(geometry, coordinate, velocity) * velocity * acceleration
               + sp.diff(geometry, velocity, 2) * acceleration**2)
    expanded = sp.diff(geometry, coordinate) * acceleration + sp.diff(geometry, velocity) * jerk + hessian
    evidence.check('symbolic_second_metric_chain_rule', sp.simplify(eta - expanded) == 0)
    curvature = (sp.diff(momentum, coordinate, 2) * velocity**2
                 + 2 * sp.diff(momentum, coordinate, velocity) * velocity * acceleration
                 + sp.diff(momentum, velocity, 2) * acceleration**2)
    expanded_rhs = flow_derivative(force) - sp.diff(momentum, coordinate) * acceleration - curvature
    evidence.check('symbolic_second_momentum_chain_rule', sp.simplify(rhs - expanded_rhs) == 0)
