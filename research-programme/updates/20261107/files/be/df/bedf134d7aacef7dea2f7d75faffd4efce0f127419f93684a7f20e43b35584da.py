from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np
from scipy import linalg
from scipy.integrate import solve_bvp
from scipy.interpolate import PPoly
import sympy as sp


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
GRAVITY = BRANCH/'self-gravity-20261003'
PULSATION = BRANCH/'radial-pulsations-20261003'
sys.path.insert(0, str(PULSATION))
from solve_pulsations import Profile, build
from solve_self_gravity import BodySolver, potential, potential_prime


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge_function():
    report = json.loads((GRAVITY/'results/derivation/status.json').read_text(encoding='utf-8'))
    symbols = sp.symbols(' '.join(report['edge_symbols']))
    expressions = [sp.sympify(value, locals=dict(zip(report['edge_symbols'], symbols))) for value in report['edge_u_coefficients_orders_2_to_5']]
    return sp.lambdify(symbols, expressions, 'numpy')


class SequenceBody(BodySolver):
    def __init__(self, floor, tolerance):
        super().__init__(20., floor, tolerance, edge_function())
        report = json.loads((GRAVITY/'results/fine/status.json').read_text(encoding='utf-8'))
        self.seed_row = next(row for row in report['rows'] if row['base_radius'] == 20. and row['nominal_flat_compactness'] == .03)
        self.alpha = self.seed_row['alpha']
        self.target_central = None

    def boundary(self, left, right, parameters):
        residual = super().boundary(left, right, parameters)
        if self.target_central is not None:
            center_radius = self.endpoint(parameters)[0]*1e-6
            force = potential_prime(self.target_central)-parameters[0]*self.target_central*np.exp(-2*left[3])
            residual[-1] = left[0]-self.target_central-force*center_radius**2/6
        return residual

    def continue_from(self, previous, target_charge=None, target_central=None):
        self.target_central = target_central
        old_charge_scale = previous.charge_scale
        if target_charge is not None:
            self.charge_scale = target_charge/(4*np.pi)
        else:
            self.charge_scale = old_charge_scale
        mesh = np.unique(np.concatenate([np.linspace(1e-6, 1, 900), previous.sol.x]))
        initial = previous.sol(mesh)
        initial[4] *= old_charge_scale/self.charge_scale
        solution = solve_bvp(self.equation, self.boundary, mesh, initial, p=previous.p.copy(),
                             fun_jac=self.jacobian, tol=self.tolerance, bc_tol=1e-11, max_nodes=40000)
        solution.charge_scale = self.charge_scale
        return solution

    def measured(self, solution):
        report = super().observables(solution)
        for key in ['target_charge', 'flat_energy', 'fixed_charge_energy_shift', 'charge_relative_error']:
            report.pop(key)
        tail_charge = self.endpoint(solution.p)[3]
        accumulated_charge = 4*np.pi*(self.charge_scale*solution.sol(1.)[4]+tail_charge)
        report['charge_accumulation_relative_error'] = float(abs(accumulated_charge-report['charge'])/report['charge'])
        report['central_density'] = float(.5*report['central_local_frequency']**2*report['central_amplitude']**2+potential(report['central_amplitude']))
        report['central_target'] = self.target_central
        report['fixed_alpha'] = self.alpha
        return report


def load_solution(path):
    archive = np.load(path)
    spline = PPoly.construct_fast(archive['spline_coefficients'], archive['spline_knots'], axis=1)
    return SimpleNamespace(sol=spline, p=archive['parameters'], charge_scale=float(archive['charge_scale']))


def save_solution(path, body, solution):
    np.savez_compressed(path, spline_coefficients=solution.sol.c, spline_knots=solution.sol.x,
                        parameters=solution.p, alpha=body.alpha, base_radius=body.base_radius,
                        mass_scale=body.mass_scale, charge_scale=body.charge_scale, floor=body.floor)


class SequenceProfile(Profile):
    def __init__(self, path, row):
        self.path, self.row = Path(path), row
        archive = np.load(path)
        self.spline = PPoly.construct_fast(archive['spline_coefficients'], archive['spline_knots'], axis=1)
        self.parameters = archive['parameters']
        self.body = SequenceBody(float(archive['floor']), 2e-9)
        self.alpha = self.body.alpha = float(archive['alpha'])
        self.body.mass_scale = float(archive['mass_scale'])
        self.body.charge_scale = float(archive['charge_scale'])
        self.cut = self.body.endpoint(self.parameters)[0]
        self.radius = row['radius']
        self.mass = row['adm_energy']/(4*np.pi)
        self.frequency = row['frequency_at_infinity']


def signed_spectrum(profile, cells, order=8, output=None):
    system = build(profile, cells, order)
    values, vectors = linalg.eigh(system['pulsation'], subset_by_index=[0, 3], check_finite=False)
    minimum_energy = linalg.eigh(system['even'], eigvals_only=True, subset_by_index=[0, 0], check_finite=False)[0]
    modes = system['dynamic_factor']@vectors
    residual = linalg.norm(system['dynamic']@(system['even']@modes)-modes*values, axis=0)
    scale = np.maximum(abs(values), 1e-7)*linalg.norm(modes, axis=0)
    if output is not None:
        amplitude_count = cells-1
        amplitude_coefficients = linalg.solve_triangular(system['factor_amplitude'].T, modes[:amplitude_count], lower=False)
        density_coefficients = linalg.solve_triangular(system['factor_phase'].T, system['quotient']@modes[amplitude_count:], lower=False)
        np.savez_compressed(output, frequency_squared=values, nodal_position=np.linspace(0, profile.radius, cells+1),
                            amplitude_coefficients=amplitude_coefficients, density_coefficients=density_coefficients)
    return {'cells': cells, 'order': order, 'frequency_squared': values.tolist(),
            'oscillation_frequencies': [float(np.sqrt(value)) if value > 0 else None for value in values],
            'growth_rates': [float(np.sqrt(-value)) if value < 0 else None for value in values],
            'minimum_reduced_energy_eigenvalue': float(minimum_energy),
            'phase_null_relative_residual': system['phase_null_relative_residual'],
            'maximum_scaled_eigen_equation_residual': float(np.max(residual/scale)),
            'raw_lowest_sign_not_a_refined_claim': int(np.sign(values[0]))}
