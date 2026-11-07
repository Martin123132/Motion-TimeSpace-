from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_bvp

import validate_finite_bodies as runner
from run_verified_profiles import reconstruct_canonical_spline
from solve_finite_family import cut_distance, tail_state


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'results/regular-center-bodies'


def solve_regular(radius, floor, tolerance, coefficients, previous=None):
    assert previous is not None
    old_radius, old_cut, old_solution = previous
    frequency2 = float(old_solution.p[0])
    central_coordinate = 1e-6
    mesh = np.linspace(central_coordinate, 1, max(250, int(25*radius)))
    cut = radius-cut_distance(radius, frequency2, floor, coefficients)
    old_position = np.clip(cut*mesh/old_cut, 0, 1)
    initial = old_solution.sol(old_position)
    initial[1] *= cut/old_cut
    initial[0, -1] = floor
    def force(amplitude, frequency2):
        return .5*(np.cbrt(amplitude)+amplitude**3)-frequency2*amplitude
    def equation(position, fields, parameter):
        cut = radius-cut_distance(radius, parameter[0], floor, coefficients)
        return np.array([fields[1], cut**2*force(fields[0], parameter[0])-2*fields[1]/position])
    def jacobian(position, fields, parameter):
        frequency2 = parameter[0]
        cut = radius-cut_distance(radius, frequency2, floor, coefficients)
        increment = 1e-5
        cut_derivative = (cut_distance(radius, frequency2-increment, floor, coefficients)
                          -cut_distance(radius, frequency2+increment, floor, coefficients))/(2*increment)
        amplitude = fields[0]
        field_jacobian = np.zeros((2, 2, len(position)))
        field_jacobian[0, 1] = 1
        field_jacobian[1, 0] = cut**2*(np.maximum(abs(amplitude), 1e-30)**(-2/3)/6+1.5*amplitude**2-frequency2)
        field_jacobian[1, 1] = -2/position
        parameter_jacobian = np.zeros((2, 1, len(position)))
        parameter_jacobian[1, 0] = 2*cut*cut_derivative*force(amplitude, frequency2)-cut**2*amplitude
        return field_jacobian, parameter_jacobian
    def boundary(left, right, parameter):
        distance = cut_distance(radius, parameter[0], floor, coefficients)
        cut = radius-distance
        slope = tail_state(distance, radius, parameter[0], coefficients)[1]
        return np.array([left[1]-cut**2*force(left[0], parameter[0])*central_coordinate/3,
                         right[0]-floor, right[1]-cut*slope])
    solution = solve_bvp(equation, boundary, mesh, initial, p=[frequency2], fun_jac=jacobian,
                         tol=tolerance, bc_tol=2e-12, max_nodes=60000)
    cut = radius-cut_distance(radius, solution.p[0], floor, coefficients)
    largest = int(np.argmax(solution.rms_residuals))
    diagnostic = {'radius': radius, 'success': bool(solution.success), 'message': solution.message,
                  'nodes': len(solution.x), 'max_residual': float(solution.rms_residuals[largest]),
                  'max_residual_at_normalized_radius': float(solution.x[largest]),
                  'center_cut_normalized': central_coordinate,
                  'center_boundary': "h_x=cut_radius^2 F(h) x_min/3; error O(r_min^3) in physical derivative"}
    (OUTPUT/f'center-diagnostic-R{radius:g}.json').write_text(json.dumps(diagnostic, indent=2), encoding='utf-8')
    return solution, cut, radius-cut


def main():
    runner.OUTPUT = OUTPUT
    runner.PPoly = reconstruct_canonical_spline
    runner.solve = solve_regular
    try:
        runner.main()
    finally:
        record = {'state': 'execution_metadata', 'wrapper_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'base_runner_sha256': hashlib.sha256((ROOT/'validate_finite_bodies.py').read_bytes()).hexdigest(),
                  'spline_loader_sha256': hashlib.sha256((ROOT/'run_verified_profiles.py').read_bytes()).hexdigest(),
                  'prior_verified_attempt': 'R6 through R40 passed profile and spectra; singular-center S formulation failed its high-accuracy mesh convergence at R80; all retained',
                  'method_change': 'Use the regular radial Taylor condition at x_min=1e-6 and an analytic field Jacobian; full-force equation unchanged.',
                  'prior_evidence_modified': False}
        if OUTPUT.is_dir():
            (OUTPUT/'execution-provenance.json').write_text(json.dumps(record, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
