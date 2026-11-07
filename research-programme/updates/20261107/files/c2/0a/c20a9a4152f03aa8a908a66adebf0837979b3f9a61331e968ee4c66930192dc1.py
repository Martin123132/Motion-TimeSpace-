from __future__ import annotations

import hashlib
import json
from pathlib import Path
import time

import numpy as np
import psutil
from scipy.integrate import solve_bvp, simpson
from scipy.optimize import brentq
import sympy as sp


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'results/exploration'
COEFFICIENT = 12.0**(-1.5)


def endpoint_series():
    distance, radius, frequency2 = sp.symbols('distance radius frequency2', positive=True)
    series = distance
    coefficients = []
    for order in range(2, 7):
        coefficient = sp.Symbol(f'b{order}')
        trial = series + coefficient * distance**order
        residual = (3*trial*sp.diff(trial, distance, 2) + 6*sp.diff(trial, distance)**2
                    - 6*trial*sp.diff(trial, distance)/(radius-distance) - 6 + frequency2*trial**2)
        equation = sp.series(residual, distance, 0, order).removeO().expand().coeff(distance, order-1)
        value = sp.factor(sp.solve(equation, coefficient)[0])
        coefficients.append(value)
        series += value * distance**order
    return sp.lambdify((radius, frequency2), coefficients, 'numpy'), [str(value) for value in coefficients]


def endpoint(cut_radius, frequency2, floor, coefficient_function):
    target = (floor / COEFFICIENT)**(1/3)
    def evaluate(distance):
        coefficients = [1.0, *coefficient_function(cut_radius+distance, frequency2)]
        value = sum(coefficient*distance**order for order, coefficient in enumerate(coefficients, 1))
        derivative = sum(order*coefficient*distance**(order-1) for order, coefficient in enumerate(coefficients, 1))
        return value, derivative
    distance = brentq(lambda value: evaluate(value)[0]-target, target*.5, target*1.5, xtol=1e-14)
    value, derivative = evaluate(distance)
    return -3*COEFFICIENT*value**2*derivative, distance


def solve_profile(radius, floor, tolerance, coefficient_function, previous=None):
    mesh = np.linspace(0, 1, max(250, int(25*radius)))
    if previous is None:
        frequency2 = (1 + .36/radius)**2
        bulk = 1.0
        width = (bulk/COEFFICIENT)**(1/3)
        offset = (floor/COEFFICIENT)**(1/3)
        position = radius*mesh
        left = np.tanh((radius+offset-position)/width)
        right = np.tanh((radius+offset+position)/width)
        guess = bulk*(left*right)**3
        derivative = 3*bulk*(left*right)**2*((1-right**2)*left-(1-left**2)*right)*radius/width
        initial = np.array([guess, derivative])
    else:
        old_radius, old_solution = previous
        distance = radius*(1-mesh)
        old_position = np.maximum(0, 1-distance/old_radius)
        initial = old_solution.sol(old_position)
        initial[1] *= radius/old_radius
        initial[1, distance > old_radius] = 0
        frequency2 = 1 + (old_solution.p[0]-1)*old_radius/radius
    def equation(position, fields, parameter):
        amplitude, derivative = fields
        return np.array([derivative, radius**2*(.5*(np.cbrt(amplitude)+amplitude**3)-parameter[0]*amplitude)])
    def boundary(left, right, parameter):
        slope, distance = endpoint(radius, parameter[0], floor, coefficient_function)
        return np.array([left[1], right[0]-floor, right[1]-radius*slope])
    solution = solve_bvp(equation, boundary, mesh, initial, p=[frequency2],
                         S=np.array([[0., 0.], [0., -2.]]), tol=tolerance, bc_tol=1e-11, max_nodes=40000)
    return solution


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    OUTPUT.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    coefficient_function, series = endpoint_series()
    rows = []
    previous = None
    for radius in [6., 8., 12., 20., 40., 80.]:
        solution = solve_profile(radius, 1e-7, 2e-6, coefficient_function, previous)
        mesh = np.linspace(0, 1, 12001)
        amplitude, derivative = solution.sol(mesh)
        position = radius*mesh
        derivative /= radius
        frequency = float(np.sqrt(max(0, solution.p[0])))
        measure = 4*np.pi*position**2
        charge = frequency*simpson(measure*amplitude**2, x=position)
        gradient = simpson(measure*.5*derivative**2, x=position)
        potential = simpson(measure*(.375*np.abs(amplitude)**(4/3)+.125*amplitude**4), x=position)
        rotation = .5*frequency*charge
        energy = gradient+potential+rotation
        row = {'cut_radius': radius, 'frequency': frequency, 'bvp_success': bool(solution.success),
               'message': solution.message, 'nodes': len(solution.x), 'central_amplitude': float(amplitude[0]),
               'min_amplitude': float(np.min(amplitude)), 'max_increase': float(np.max(derivative)),
               'charge': float(charge), 'energy': float(energy), 'gradient': float(gradient),
               'virial_relative': float(abs(gradient+3*(potential-rotation))/max(gradient, 1e-30)),
               'max_rms_residual': float(np.max(solution.rms_residuals))}
        rows.append(row)
        print(json.dumps(row), flush=True)
        np.savez_compressed(OUTPUT/f'profile-R{radius:g}.npz', mesh=mesh, amplitude=amplitude,
                            derivative=derivative, radius=radius, frequency=frequency,
                            bvp_mesh=solution.x, bvp_fields=solution.y, bvp_parameter=solution.p)
        (OUTPUT/'progress.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
        if not solution.success or np.min(amplitude) < 0 or amplitude[0] < .05:
            break
        previous = radius, solution
    report = {'state': 'complete', 'purpose': 'exploratory solver feasibility, not acceptance evidence',
              'series_coefficients': series, 'rows': rows, 'elapsed_seconds': time.monotonic()-started,
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUTPUT/'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
