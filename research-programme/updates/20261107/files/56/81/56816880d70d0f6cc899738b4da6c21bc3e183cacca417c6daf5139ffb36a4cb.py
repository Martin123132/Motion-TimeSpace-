from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import psutil
from scipy.integrate import solve_ivp
from scipy.optimize import root

from dynamic_system import DynamicProblem, Profile, ROOT


def asymptotic_coefficients(mass_frequency, order):
    mass = mass_frequency
    second = {5: 4, 4: 4*mass, 3: -15*mass**2, 2: -18*mass**3}
    first = {5: 8j, 4: 24j*mass, 3: 18j*mass**2+8*mass, 2: 24*mass**2, 1: 18*mass**3}
    zeroth = {3: -24, 2: -24*mass, 1: -36*mass**2, 0: -18*mass**3}
    coefficients = [1+0j]
    for level in range(order):
        power = 3-level
        known = 0j
        for index, coefficient in enumerate(coefficients):
            known += coefficient*(index*(index+1)*second.get(power+index+2, 0)-index*first.get(power+index+1, 0)+zeroth.get(power+index, 0))
        coefficients.append(known/(8j*(level+1)))
    return np.array(coefficients)


def outgoing_boundary(radius, mass, sigma, far_phase=40., order=10, tolerance=2e-11):
    assert sigma.real > 0
    outer = max(10*radius, far_phase/sigma.real)
    coefficients = asymptotic_coefficients(mass*sigma, order)
    argument = sigma*outer
    indices = np.arange(order+1)
    wave = np.sum(coefficients*argument**(-indices))
    derivative = np.sum(-indices*coefficients*argument**(-indices-1))
    metric = 1-2*mass/outer
    initial = np.array([1+0j, 1j*sigma+metric*sigma*derivative/wave])

    def equation(position, state):
        metric = 1-2*mass/position
        potential = metric*(24*position**3+24*mass*position**2+36*mass**2*position+18*mass**3)/(position**3*(2*position+3*mass)**2)
        return np.array([state[1]/metric, (potential-sigma**2)*state[0]/metric])

    solution = solve_ivp(equation, (outer, radius), initial, method='DOP853', rtol=tolerance, atol=tolerance/100)
    assert solution.success, solution.message
    return solution.y[1, -1]/solution.y[0, -1], {'outer_radius': outer, 'far_phase': far_phase, 'series_order': order, 'function_evaluations': solution.nfev}


def encode(value):
    return {'real': float(np.real(value)), 'imaginary': float(np.imag(value))}


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--nominal', type=float, default=.03)
    parser.add_argument('--distance', type=float, default=.01)
    parser.add_argument('--tolerance', type=float, default=2e-7)
    parser.add_argument('--guess', type=float, default=.0207)
    parser.add_argument('--far-phase', type=float, default=40.)
    parser.add_argument('--order', type=int, default=10)
    args = parser.parse_args()
    output = ROOT/'results'/args.label
    output.mkdir(exist_ok=False)
    profile = Profile(20., args.nominal)
    report = {'state': 'running', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'system_sha256': hashlib.sha256((ROOT/'dynamic_system.py').read_bytes()).hexdigest(),
              'arguments': vars(args), 'profile_path': str(profile.path), 'profile_sha256': hashlib.sha256(profile.path.read_bytes()).hexdigest(), 'iterations': []}
    previous, last_problem = None, None

    def mismatch(values):
        nonlocal previous, last_problem
        sigma = complex(values[0], values[1])
        problem = DynamicProblem(profile, sigma, args.distance, args.tolerance)
        solution = problem.solve(previous)
        assert solution.success, solution.message
        previous, last_problem = solution, problem
        time_value, time_prime, master, master_star_prime = problem.surface(solution)
        outgoing, diagnostics = outgoing_boundary(profile.radius, problem.mass, sigma, args.far_phase, args.order)
        difference = (master_star_prime/master-outgoing)*profile.radius
        row = {'sigma': encode(sigma), 'mismatch_times_radius': encode(difference), 'nodes': len(solution.x), 'maximum_rms_residual': float(max(solution.rms_residuals)), 'outgoing': diagnostics}
        report['iterations'].append(row)
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
        print(json.dumps(row), flush=True)
        return [difference.real, difference.imag]

    try:
        result = root(mismatch, [args.guess, -1e-7], method='hybr', options={'xtol': 2e-9, 'maxfev': 45})
        final_mismatch = mismatch(result.x)
        assert result.success and np.linalg.norm(final_mismatch) < 1e-7, (result.message, final_mismatch)
        sigma = complex(*result.x)
        assert sigma.real > 0 and sigma.imag < 0
        np.savez_compressed(output/'mode.npz', spline_knots=previous.sol.x, spline_coefficients=previous.sol.c, parameters=previous.p, scales=last_problem.scales, radius=profile.radius, alpha=profile.alpha, sigma=sigma)
        report.update({'state': 'complete', 'sigma': encode(sigma), 'damping_amplitude_time': float(-1/sigma.imag),
                       'quality_factor': float(-sigma.real/(2*sigma.imag)), 'mismatch_times_radius': final_mismatch,
                       'boundary_residual': float(max(abs(last_problem.boundary(previous.y[:, 0], previous.y[:, -1], previous.p)))),
                       'radius': profile.radius, 'geometric_mass': last_problem.mass, 'alpha': profile.alpha,
                       'zero_frequency_continuum_present': True, 'finite_outer_box_eigencondition_used': False})
        print(json.dumps({key: report[key] for key in ['state', 'sigma', 'quality_factor', 'damping_amplitude_time']}), flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        raise
    finally:
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
