from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import psutil
import sympy as sp

from dynamic_system import ROOT, edge_state, vacuum_data
from outgoing_modes import asymptotic_coefficients, outgoing_boundary


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/edge-vacuum'
    output.mkdir(exist_ok=False)
    power = sp.symbols('power')
    surface, constant, amplitude, frequency, shift, phase_prime, displacement = sp.symbols('surface constant amplitude frequency shift phase_prime displacement', nonzero=True)
    checks = []

    def exact(name, expression):
        assert sp.simplify(expression) == 0, name
        checks.append({'name': name, 'passed': True})

    exact('amplitude_indicial_roots_2_minus1', power*(power-1)-2-(power-2)*(power+1))
    exact('phase_indicial_roots_0_minus5', power*(power-1)+6*power-power*(power+5))
    leading_current = -6*phase_prime+2*frequency*amplitude/(surface**2*constant)+6*frequency*shift/surface
    boundary_phase_prime = frequency*amplitude/(3*constant*surface**2)+frequency*shift/surface
    exact('finite_phase_frobenius_kinematic_condition', leading_current.subs(phase_prime, boundary_phase_prime))
    velocity_displacement = surface**2/frequency*(phase_prime-frequency*shift/surface)
    exact('current_velocity_equals_moving_support_velocity', velocity_displacement.subs(phase_prime, boundary_phase_prime)-amplitude/(3*constant))
    distance = sp.symbols('distance')
    exact('cubic_edge_translation_amplitude', sp.diff(constant*(distance+displacement)**3, displacement).subs(displacement, 0)*displacement-3*constant*distance**2*displacement)
    coefficients = asymptotic_coefficients(0., 10)
    assert np.max(abs(coefficients-np.r_[1., 3j, -3., np.zeros(8)])) < 1e-14
    checks.append({'name': 'flat_outgoing_series_terminates_exactly', 'passed': True})
    parent_path = ROOT.parent/'gravitating-tides-20261004/results/edge-weak-v2/status.json'
    parent = json.loads(parent_path.read_text())
    symbols = sp.symbols(' '.join(parent['edge_symbols']), real=True)
    environment = dict(zip(parent['edge_symbols'], symbols))
    background = sp.lambdify(symbols[:3], [sp.sympify(value, locals=environment) for value in parent['background_coefficients_orders_2_to_4']], 'numpy')
    old_coefficients = sp.lambdify(symbols, [sp.sympify(value, locals=environment) for value in parent['edge_coefficients_orders_3_to_5']], 'numpy')
    static_edges = []
    for compactness in [0., .03, .2]:
        radius, frequency_value, amplitude_value, phase0 = 20., 1.04, -.1, .3
        mass = compactness*radius/2
        pair = np.array([-2., -.4])
        time_row, flow, second_flow, time_prime, time_second = vacuum_data(radius, mass, 0.)
        tide, tide_prime = (time_row@pair)[0], (time_prime@pair)[0]
        original = [amplitude_value, *old_coefficients(radius, compactness, frequency_value**2, amplitude_value, tide, tide_prime, *background(radius, compactness, frequency_value**2))]
        for distance_value in [.08, .04, .02]:
            expected = sum(value*distance_value**order for order, value in enumerate(original, 2))
            actual = edge_state(radius, mass, frequency_value, 0., distance_value, amplitude_value, phase0, pair)[2]
            error = abs(actual/expected-1)
            assert error < 1e-12
            static_edges.append({'compactness': compactness, 'distance': distance_value, 'relative_static_edge_difference': float(error)})
    phase_edges = []
    for compactness in [0., .03]:
        radius, frequency_value, sigma, amplitude_value, phase0 = 20., 1.04, .021, -.1, .3
        mass = compactness*radius/2
        surface_value = 1-compactness
        constant_value = (12*surface_value)**(-1.5)
        bg2, bg3, bg4 = background(radius, compactness, frequency_value**2)
        pair = np.array([-2., -.4])
        for distance_value in [.08, .04, .02, .01]:
            position = radius-distance_value
            polynomial = 1+bg2*distance_value+bg3*distance_value**2+bg4*distance_value**3
            polynomial_prime = bg2+2*bg3*distance_value+3*bg4*distance_value**2
            field = constant_value*distance_value**3*polynomial**3
            gradient = -3*constant_value*distance_value**2*polynomial**2*(polynomial+distance_value*polynomial_prime)
            state = edge_state(radius, mass, frequency_value, sigma**2, distance_value, amplitude_value, phase0, pair)
            shifted = edge_state(radius, mass, frequency_value, sigma**2, distance_value+1e-25j, amplitude_value, phase0, pair)
            scalar_second, phase_second = -shifted[[3, 5]].imag/1e-25
            metric = 1-2*mass/position
            lapse_prime_value = mass/(position**2*metric)
            first_value = (1+metric)/(position*metric)
            tide = (vacuum_data(position, mass, sigma**2)[0]@state[:2])[0]
            energy_prime = .5*(field**(1/3)+field**3)
            energy_second = field**(-2/3)/6+1.5*field**2
            drive = energy_prime-2*frequency_value**2*field/metric-2*metric*lapse_prime_value*gradient
            scalar_residual = scalar_second+first_value*state[3]-(6/position**2+energy_second-(frequency_value**2+sigma**2)/metric)*state[2]/metric-drive*tide/metric+2*frequency_value*field*sigma**2*state[4]/metric**2
            phase_residual = phase_second+(first_value+2*gradient/field)*state[5]-(6/(position**2*metric)-sigma**2/metric**2)*state[4]+2*frequency_value*state[2]/(metric**2*field)-2*frequency_value/metric*(1/position-lapse_prime_value+gradient/field)*state[1]
            phase_edges.append({'compactness': compactness, 'distance': distance_value, 'amplitude_equation_residual': float(abs(scalar_residual)), 'phase_equation_residual': float(abs(phase_residual))})
    vacuum_rows = []
    for sigma in [.01, .02, .03]:
        argument = sigma*20
        wave = 1+3j/argument-3/argument**2
        wave_prime = -3j/argument**2+6/argument**3
        exact_logarithm = 1j*sigma+sigma*wave_prime/wave
        for far_phase in [20., 40., 60.]:
            value, diagnostics = outgoing_boundary(20., 0., complex(sigma), far_phase, 10)
            error = abs(value-exact_logarithm)
            assert error < 1e-10
            vacuum_rows.append({'sigma': sigma, 'mass': 0., 'far_phase': far_phase, 'absolute_logarithmic_derivative_error': float(error)})
    report = json.loads((ROOT/'results/mode-edge004/status.json').read_text())
    radius, mass = report['radius'], report['geometric_mass']
    sigma = complex(report['sigma']['real'], report['sigma']['imaginary'])
    reference, details = outgoing_boundary(radius, mass, sigma, 60., 14)
    for far_phase, order in [(20., 8), (30., 8), (40., 10), (50., 12)]:
        value, details = outgoing_boundary(radius, mass, sigma, far_phase, order)
        error = abs(value-reference)
        assert error < 1e-10
        vacuum_rows.append({'sigma': {'real': sigma.real, 'imaginary': sigma.imag}, 'mass': mass, 'far_phase': far_phase, 'series_order': order, 'absolute_logarithmic_derivative_error': float(error)})
    result = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'exact_checks': checks,
              'static_edge_checks': static_edges, 'dynamic_edge_residuals': phase_edges, 'vacuum_checks': vacuum_rows,
              'parent_edge_path': str(parent_path), 'parent_edge_sha256': hashlib.sha256(parent_path.read_bytes()).hexdigest(),
              'scope': 'Leading endpoint identities; full static coefficient replay; dynamic Taylor residual scaling; independent flat outgoing spherical-wave and Schwarzschild far-boundary controls.'}
    (output/'status.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks), 'static_edges': len(static_edges), 'vacuum_checks': len(vacuum_rows), 'edge_residuals': phase_edges}))


if __name__ == '__main__':
    main()
