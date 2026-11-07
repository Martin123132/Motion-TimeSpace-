from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import psutil
import sympy as sp
from scipy.integrate import simpson
from scipy.interpolate import PPoly


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'results/identities'


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    OUTPUT.mkdir(parents=True, exist_ok=False)
    checks = []
    def exact(name, expression):
        remainder = sp.simplify(expression)
        assert remainder == 0, (name, remainder)
        checks.append({'name': name, 'passed': True})
    radius, frequency, distance, coupling = sp.symbols('radius frequency distance coupling', positive=True)
    amplitude = sp.Function('h')(radius)
    potential = sp.Rational(3, 8)*amplitude**sp.Rational(4, 3)+amplitude**4/8
    potential_prime = amplitude**sp.Rational(1, 3)/2+amplitude**3/2
    potential_second = amplitude**(-sp.Rational(2, 3))/6+3*amplitude**2/2
    first = sp.diff(amplitude, radius)
    second = sp.diff(amplitude, radius, 2)
    field_rhs = potential_prime-frequency**2*amplitude-2*first/radius
    radial_pressure = first**2/2+frequency**2*amplitude**2/2-potential
    tangent_pressure = -first**2/2+frequency**2*amplitude**2/2-potential
    exact('radial_stress_conservation',
          sp.diff(radial_pressure, radius)+2*(radial_pressure-tangent_pressure)/radius-first*(second-field_rhs))
    phase_zero = radius*amplitude
    exact('phase_zero_mode', (-sp.diff(phase_zero, radius, 2)+(potential_prime/amplitude-frequency**2)*phase_zero).subs(second, field_rhs))
    translation_zero = radius*first
    third_rhs = (potential_second-frequency**2)*first-2*second/radius+2*first/radius**2
    translation_equation = -sp.diff(translation_zero, radius, 2)+(potential_second-frequency**2+2/radius**2)*translation_zero
    exact('translation_zero_mode', translation_equation.subs(sp.diff(amplitude, radius, 3), third_rhs).subs(second, field_rhs))
    physical_coefficient = (coupling/6)**sp.Rational(3, 2)
    exact('physical_cubic_edge', 6*physical_coefficient-coupling*physical_coefficient**sp.Rational(1, 3))
    coefficient = 12**(-sp.Rational(3, 2))
    exact('dimensionless_cubic_edge', 6*coefficient-coefficient**sp.Rational(1, 3)/2)
    exact('amplitude_inverse_square_endpoint', coefficient**(-sp.Rational(2, 3))/6-2)
    exact('phase_inverse_square_endpoint', coefficient**(-sp.Rational(2, 3))/2-6)
    for name, exponent, strength in [('amplitude_regular', 2, 2), ('amplitude_excluded', -1, 2),
                                     ('phase_regular', 3, 6), ('phase_excluded', -2, 6)]:
        exact(name, exponent*(exponent-1)-strength)
    ground = sp.Function('u')(radius)
    multiplier = sp.Function('z')(radius)
    trial = ground*multiplier
    exact('ground_state_transform', sp.diff(trial, radius)**2+sp.diff(ground, radius, 2)/ground*trial**2
          -ground**2*sp.diff(multiplier, radius)**2-sp.diff(ground*sp.diff(ground, radius)*multiplier**2, radius))
    inertia, overlap, norm, charge, parameter = sp.symbols('I overlap norm charge parameter', positive=True)
    rotation_variation = charge**2/(2*(inertia+2*parameter*overlap+parameter**2*norm))
    exact('fixed_charge_rank_one_second_variation',
          sp.diff(rotation_variation, parameter, 2).subs(parameter, 0).subs(charge, frequency*inertia)
          -(-frequency**2*norm+4*frequency**2*overlap**2/inertia))
    gradient, fractional, quartic, rotation, scale, size = sp.symbols('T F L K scale size', positive=True)
    scaled_energy = rotation/(scale**2*size**3)+gradient*scale**2*size+fractional*scale**sp.Rational(4, 3)*size**3+quartic*scale**4*size**3
    exact('radius_virial', sp.diff(scaled_energy, size).subs({scale: 1, size: 1})-(gradient+3*(fractional+quartic-rotation)))
    exact('amplitude_stationarity', sp.diff(scaled_energy, scale).subs({scale: 1, size: 1})
          -(-2*rotation+2*gradient+sp.Rational(4, 3)*fractional+4*quartic))
    exact('fixed_charge_dilation_convexity', sp.diff(scaled_energy.subs(scale, 1), size, 2)
          -(12*rotation/size**5+6*(fractional+quartic)*size))
    exact('fixed_charge_amplitude_convexity', sp.diff(scaled_energy.subs(size, 1), scale, 2)
          -(6*rotation/scale**4+2*gradient+sp.Rational(4, 9)*fractional/scale**sp.Rational(2, 3)+12*quartic*scale**2))
    exact('grand_potential_virial_value', (gradient+fractional+quartic-rotation).subs(rotation, fractional+quartic+gradient/3)-2*gradient/3)
    exact('integrated_stress_virial', 3*rotation-gradient-3*(fractional+quartic)+(gradient+3*(fractional+quartic-rotation)))
    sigma, charge_radius = sp.symbols('sigma charge_radius', positive=True)
    asymptotic_charge = 4*sp.pi*charge_radius**3/3
    asymptotic_energy = asymptotic_charge+4*sp.pi*sigma*charge_radius**2
    exact('large_charge_chemical_shift', sp.diff(asymptotic_energy, charge_radius)/sp.diff(asymptotic_charge, charge_radius)-1-2*sigma/charge_radius)
    near_edge = distance+distance**2/(5*radius)
    edge_residual = 3*near_edge*sp.diff(near_edge, distance, 2)+6*sp.diff(near_edge, distance)**2-6*near_edge*sp.diff(near_edge, distance)/(radius-distance)-6
    exact('first_spherical_edge_correction', sp.series(edge_residual, distance, 0, 2).removeO())
    hessian = sp.hessian(scaled_energy, (scale, size)).subs({scale: 1, size: 1})
    hessian_function = sp.lambdify((gradient, fractional, quartic, rotation), hessian, 'numpy')
    data = json.loads((ROOT/'results/regular-center-bodies/status.json').read_text(encoding='utf-8'))
    numerical = []
    for row in data['rows']:
        support = row['support_radius']
        archive = np.load(ROOT/f'results/regular-center-bodies/profile-R{support:g}.npz')
        spline = PPoly.construct_fast(archive['spline_coefficients'], archive['spline_knots'], axis=1)
        cut = float(archive['cut_radius'])
        points = np.linspace(0, cut, max(12001, int(400*support)+1))
        values = spline(points/cut)[0]
        fractional_energy = float(simpson(4*np.pi*points**2*.375*values**(4/3), x=points))
        quartic_energy = float(simpson(4*np.pi*points**2*.125*values**4, x=points))
        gradient_energy = row['gradient_energy']
        rotation_energy = row['rotation_energy']
        amplitude_residual = -2*rotation_energy+2*gradient_energy+4*fractional_energy/3+4*quartic_energy
        matrix = np.asarray(hessian_function(gradient_energy, fractional_energy, quartic_energy, rotation_energy), dtype=float)
        eigenvalues = np.linalg.eigvalsh(matrix)/row['energy']
        changes = []
        for amplitude_scale, radius_scale in [(1.1, 1), (.9, 1), (1, 1.1), (1, .9), (1.03, .98), (.97, 1.02)]:
            energy = rotation_energy/(amplitude_scale**2*radius_scale**3)+gradient_energy*amplitude_scale**2*radius_scale
            energy += (fractional_energy*amplitude_scale**(4/3)+quartic_energy*amplitude_scale**4)*radius_scale**3
            changes.append({'amplitude_scale': amplitude_scale, 'radius_scale': radius_scale,
                            'relative_energy_increase': (energy-row['energy'])/row['energy']})
        assert abs(amplitude_residual)/row['energy'] < 1e-8
        assert eigenvalues[0] > 0 and all(item['relative_energy_increase'] > 0 for item in changes)
        numerical.append({'radius': support, 'amplitude_stationarity_relative': abs(amplitude_residual)/row['energy'],
                          'scaling_hessian_eigenvalues_per_energy': eigenvalues.tolist(), 'finite_fixed_charge_trials': changes})
    spectral_convergence = []
    for row in data['spectra']:
        medium, fine = row['levels'][-2:]
        difference = abs(fine['fixed_charge_radial'][0]-medium['fixed_charge_radial'][0])
        ratio = difference/fine['fixed_charge_radial'][0]
        assert ratio < .001
        assert fine['amplitude_l2'][0] > 10*abs(fine['amplitude_l1_translation'][0])
        spectral_convergence.append({'radius': row['radius'], 'fixed_charge_lowest_relative_change': ratio,
                                      'l2_positive_margin_over_translation_zero_error': fine['amplitude_l2'][0]/abs(fine['amplitude_l1_translation'][0])})
    report = {'state': 'complete', 'checks': checks, 'exact_check_count': len(checks),
              'numerical_scaling_tests': numerical, 'spectral_convergence': spectral_convergence,
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'profile_report_sha256': hashlib.sha256((ROOT/'results/regular-center-bodies/status.json').read_bytes()).hexdigest(),
              'proof_scope': 'Exact algebraic identities; conditional ground-state angular positivity; finite numerical radial Hessian checks, not a nonlinear orbital-stability theorem.'}
    (OUTPUT/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks), 'finite_fixed_charge_trials': 6*len(numerical),
                      'max_fixed_charge_eigenvalue_relative_change': max(item['fixed_charge_lowest_relative_change'] for item in spectral_convergence)}))


if __name__ == '__main__':
    main()
