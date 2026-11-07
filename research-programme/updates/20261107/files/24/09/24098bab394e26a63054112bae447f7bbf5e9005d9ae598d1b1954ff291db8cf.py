from __future__ import annotations

import hashlib
import json
from pathlib import Path

import psutil
import sympy as sp


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/derivation'
    output.mkdir(parents=True, exist_ok=False)
    checks = []

    def exact(name, expression):
        entries = list(expression) if isinstance(expression, sp.MatrixBase) else [expression]
        remainders = [sp.factor(entry) for entry in entries]
        assert all(value == 0 for value in remainders), (name, remainders)
        checks.append({'name': name, 'passed': True})

    radius, field, coefficient, xi, frequency = sp.symbols('radius field coefficient xi frequency', positive=True)
    amplitude, phase, radial_momentum, charge_density = sp.symbols('amplitude phase radial_momentum charge_density')
    gradient, gradient_shift, phase_gradient, parameter = sp.symbols('gradient gradient_shift phase_gradient parameter')
    background_momentum = radius**2*frequency*field/coefficient
    background_charge = field*background_momentum
    transform = sp.Matrix([[1, 0, 0, 0], [0, field, 0, 0],
                           [0, -background_momentum, 1, 0], [-background_momentum/field, 0, 0, 1/field]])
    symplectic = sp.Matrix([[0, 0, 1, 0], [0, 0, 0, 1], [-1, 0, 0, 0], [0, -1, 0, 0]])
    exact('linear_polar_transformation_is_canonical', transform.T*symplectic*transform-symplectic)
    cartesian_momentum_v = (charge_density-background_momentum*amplitude)/field
    exact('charge_tangent_is_density_integral', background_momentum*amplitude+field*cartesian_momentum_v-charge_density)
    trial_field = field+parameter*amplitude
    trial_charge = background_charge+parameter*charge_density
    trial_kinetic = (gradient+parameter*gradient_shift)**2+trial_field**2*(parameter*phase_gradient)**2
    trial_kinetic += (parameter*radial_momentum)**2/radius**4+trial_charge**2/(radius**4*trial_field**2)
    first = 2*gradient*gradient_shift+2*frequency*charge_density/(coefficient*radius**2)-2*frequency**2*field*amplitude/coefficient**2
    exact('polar_first_kinetic_variation', sp.diff(trial_kinetic, parameter).subs(parameter, 0)-first)
    exact('polar_Cartesian_metric_source_agrees', first-(2*gradient*gradient_shift+2*background_momentum*cartesian_momentum_v/radius**4))
    second = sp.diff(trial_kinetic, parameter, 2).subs(parameter, 0)
    expected_half_second = gradient_shift**2+field**2*phase_gradient**2+radial_momentum**2/radius**4
    expected_half_second += charge_density**2/(radius**4*field**2)-4*frequency*amplitude*charge_density/(coefficient*radius**2*field)+3*frequency**2*amplitude**2/coefficient**2
    exact('polar_second_kinetic_variation', second/2-expected_half_second)
    even_polar = coefficient*radius**2*(gradient_shift**2+charge_density**2/(radius**4*field**2)
                  -4*frequency*amplitude*charge_density/(coefficient*radius**2*field)+3*frequency**2*amplitude**2/coefficient**2)
    even_cartesian = coefficient*radius**2*gradient_shift**2+coefficient*cartesian_momentum_v**2/radius**2-2*frequency*amplitude*cartesian_momentum_v
    exact('even_polar_Hessian_matches_Cartesian_Routhian', even_polar-even_cartesian)
    phase_value = field*phase
    cartesian_momentum_u = radial_momentum-background_momentum*phase
    exact('odd_momentum_square_removes_phase_mixing', coefficient/radius**2*(cartesian_momentum_u+frequency*radius**2*phase_value/coefficient)**2-coefficient*radial_momentum**2/radius**2)
    phase_rate = sp.Symbol('phase_rate')
    flat_charge = radius**2*(field**2*phase_rate+2*frequency*field*amplitude)
    exact('flat_phase_velocity_from_charge', flat_charge/(radius**2*field**2)-2*frequency*amplitude/field-phase_rate)
    wave_number, frequency_squared, mass_squared = sp.symbols('wave_number frequency_squared mass_squared')
    stiffness = sp.Matrix([[wave_number**2+mass_squared-frequency_squared, -2*frequency*sp.sqrt(frequency_squared)],
                           [-2*frequency*sp.sqrt(frequency_squared), wave_number**2-frequency_squared]])
    polynomial = frequency_squared**2-(2*wave_number**2+mass_squared+4*frequency**2)*frequency_squared+wave_number**2*(wave_number**2+mass_squared)
    exact('flat_bulk_gyroscopic_dispersion', stiffness.det()-polynomial)
    potential = sp.Rational(3, 8)*field**sp.Rational(4, 3)+field**4/8
    amplitude_mass2 = sp.diff(potential, field, 2).subs(field, 1)-1
    exact('coexistence_amplitude_mass_squared', amplitude_mass2-sp.Rational(2, 3))
    exact('coexistence_sound_speed_squared', amplitude_mass2/(amplitude_mass2+4)-sp.Rational(1, 7))
    exact('coexistence_gapped_frequency_squared', amplitude_mass2+4-sp.Rational(14, 3))
    small_speed = sp.Symbol('small_speed')
    leading = sp.expand(polynomial.subs(frequency_squared, small_speed*wave_number**2)).coeff(wave_number, 2)
    exact('long_wave_sound_branch', leading.subs(small_speed, mass_squared/(mass_squared+4*frequency**2)))
    parent = ROOT.parent/'radial-gravity-stability-20261003/results/stage-integrity.json'
    report = {'state': 'complete', 'checks': checks, 'exact_check_count': len(checks),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'parent_seal_sha256': hashlib.sha256(parent.read_bytes()).hexdigest(),
              'uniform_coexistence_sound_speed_squared': '1/7', 'uniform_gapped_frequency_squared': '14/3',
              'bulk_dispersion_is_not_a_finite_body_frequency': True}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks)}))


if __name__ == '__main__':
    main()
