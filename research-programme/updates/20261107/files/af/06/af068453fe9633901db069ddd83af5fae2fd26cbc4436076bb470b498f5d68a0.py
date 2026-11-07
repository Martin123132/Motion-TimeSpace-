from __future__ import annotations

from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from types import SimpleNamespace
import sys

import numpy as np
from scipy.integrate import solve_bvp
from scipy.interpolate import PPoly
import sympy as sp

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'response-budget-20261006'
sys.path.insert(0, str(PARENT))
from budget import digest, read_json, write_json, modest_process
sys.path.insert(0, str(BRANCH/'dynamical-tides-20261004'))
from dynamic_system import Profile, edge_state
from outgoing_modes_v4 import DynamicProblem


def dependencies():
    paths = {Path(module.__file__).resolve() for module in list(sys.modules.values())
             if getattr(module, '__file__', None) and Path(module.__file__).suffix == '.py'
             and BRANCH in Path(module.__file__).resolve().parents}
    paths.add(PARENT/'results/stage-integrity.json')
    paths.add(BRANCH/'dynamical-tides-20261004/results/reduction/status.json')
    return {str(path):digest(path) for path in sorted(paths)}


def save(name, script, report):
    directory = ROOT/'results'/name
    directory.mkdir(parents=True, exist_ok=False)
    result = dict(state='complete', time_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), **report)
    write_json(directory/'status.json', result, exclusive=True)
    (directory/'COMPLETE').write_text(result['time_utc']+'\n', encoding='utf-8')
    return result


@lru_cache(maxsize=1)
def constraint_derivative():
    source = read_json(BRANCH/'dynamical-tides-20261004/results/reduction/status.json')
    symbols = sp.symbols(' '.join(source['coefficient_symbols']), real=True)
    namespace = dict(zip(source['coefficient_symbols'], symbols))
    square = namespace['z']
    expressions = [sp.sympify(value, locals=namespace) for value in source['H_coefficients']]
    assert all(sp.diff(value, square, 2) == 0 for value in expressions)
    return sp.lambdify(symbols[:-1], [sp.diff(value, square) for value in expressions], 'numpy', cse=True)


def operator_tangent(problem, coordinate, state):
    position = coordinate*problem.radius
    field, gradient, metric, lapse2, energy, energy_prime, energy_second, rotation, lapse_prime, first = problem.background(position)
    coefficients = constraint_derivative()(position, metric, lapse2, field, gradient, energy, energy_prime,
        energy_second, problem.profile.alpha, problem.profile.frequency)
    physical = state*problem.scales[:, None]
    time_tangent = sum(coefficient*value for coefficient, value in zip(coefficients, physical))
    drive = energy_prime-2*rotation*field-2*metric*lapse_prime*gradient
    response_tangent = (drive*time_tangent-physical[2]/lapse2
                       -2*problem.profile.frequency*field*physical[4]/lapse2)/metric
    phase_tangent = -physical[4]/(metric*lapse2)
    zero = np.zeros_like(position)
    derivative = np.vstack([time_tangent/position, time_tangent/metric, zero,
                            response_tangent, zero, phase_tangent])
    return derivative/(problem.radius*problem.scales[:, None])


def boundary_matrices(problem):
    zeros, parameters = np.zeros(6), np.zeros(4)
    constant = np.asarray(problem.boundary(zeros, zeros, parameters), dtype=float)
    left = np.column_stack([problem.boundary(np.eye(6)[index], zeros, parameters)-constant for index in range(6)])
    right = np.column_stack([problem.boundary(zeros, np.eye(6)[index], parameters)-constant for index in range(6)])
    parameter = np.column_stack([problem.boundary(zeros, zeros, np.eye(4)[index])-constant for index in range(4)])
    square = sp.Symbol('square', real=True)
    amplitudes = sp.symbols('edge_amplitude edge_phase edge_angular edge_shift', real=True)
    physical = np.array(amplitudes, dtype=object)*problem.parameter_scales
    edge = edge_state(problem.radius, problem.mass, problem.profile.frequency, square, problem.distance,
                      physical[0], physical[1], physical[2:])
    derivative = sp.Matrix(list(edge)).diff(square).subs(square, 0).jacobian(amplitudes)
    edge_tangent = np.asarray(derivative, dtype=float)/problem.scales[:, None]/problem.radius**2
    edge_tangent[2] /= problem.distance**2
    edge_tangent[3] /= problem.radius*problem.distance
    tangent_parameter = np.zeros_like(parameter)
    tangent_parameter[3:9] = -edge_tangent
    return left, right, parameter, constant, tangent_parameter


class TangentProblem:
    def __init__(self, profile, distance, tolerance):
        self.base = DynamicProblem(profile, 0., distance, tolerance)
        self.tolerance = tolerance
        self.left, self.right, self.parameter, self.constant, self.tangent_parameter = boundary_matrices(self.base)

    def equation(self, coordinate, state, parameters):
        zero = self.base.equation(coordinate, state[:6], parameters[:4])
        tangent = self.base.equation(coordinate, state[6:], parameters[4:])+operator_tangent(self.base, coordinate, state[:6])
        return np.vstack([zero, tangent])

    def boundary(self, left, right, parameters):
        zero = self.left@left[:6]+self.right@right[:6]+self.parameter@parameters[:4]+self.constant
        tangent = self.left@left[6:]+self.right@right[6:]+self.parameter@parameters[4:]+self.tangent_parameter@parameters[:4]
        return np.r_[zero, tangent]

    def jacobian(self, coordinate, state, parameters):
        operator = np.empty((6, 6, len(coordinate)))
        derivative = np.empty_like(operator)
        for index in range(6):
            basis = np.zeros((6, len(coordinate)))
            basis[index] = 1.
            operator[:, index] = self.base.equation(coordinate, basis, np.zeros(4))
            derivative[:, index] = operator_tangent(self.base, coordinate, basis)
        zero = np.zeros_like(operator)
        matrix = np.concatenate([np.concatenate([operator, zero], axis=1), np.concatenate([derivative, operator], axis=1)], axis=0)
        return matrix, np.zeros((12, 8, len(coordinate)))

    def boundary_jacobian(self, left, right, parameters):
        zero = np.zeros_like(self.left)
        left_matrix = np.block([[self.left, zero], [zero, self.left]])
        right_matrix = np.block([[self.right, zero], [zero, self.right]])
        parameter_matrix = np.block([[self.parameter, np.zeros_like(self.parameter)], [self.tangent_parameter, self.parameter]])
        return left_matrix, right_matrix, parameter_matrix

    def solve(self, archive):
        with np.load(archive, allow_pickle=False) as data:
            static = PPoly.construct_fast(data['spline_coefficients'].real, data['spline_knots'], axis=1)
            parameters = data['parameters'].real
            mesh = data['spline_knots']
        if abs(mesh[-1]-self.base.upper) > 1e-12:
            mesh = np.linspace(self.base.lower, self.base.upper, len(mesh))
        initial = np.vstack([static(mesh), np.zeros((6, len(mesh)))])
        return solve_bvp(self.equation, self.boundary, mesh, initial, p=np.r_[parameters, np.zeros(4)],
            fun_jac=self.jacobian, bc_jac=self.boundary_jacobian, tol=self.tolerance,
            bc_tol=self.tolerance/10, max_nodes=18000)

    def surface(self, solution):
        zeroth = self.base.surface(SimpleNamespace(p=solution.p[:4]))[2:]
        tangent = self.base.surface(SimpleNamespace(p=solution.p[4:]))[2:]
        slope = zeroth[1]/zeroth[0]
        slope_dimensionless = (tangent[1]-slope*tangent[0])/zeroth[0]
        return dict(static_slope=float(slope), derivative_wrt_omega_R_squared=float(slope_dimensionless),
            coefficient_s2=float(self.base.radius**2*slope_dimensionless),
            static_master=list(map(float, zeroth)), tangent_master=list(map(float, tangent)))
