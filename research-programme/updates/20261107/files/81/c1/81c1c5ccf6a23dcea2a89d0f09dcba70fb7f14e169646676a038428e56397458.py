from __future__ import annotations

from itertools import product
import hashlib
import json
from pathlib import Path

import psutil
import sympy as sp


ROOT = Path(__file__).resolve().parent


def stf_two(matrix):
    symmetric = (matrix+matrix.T)/2
    return sp.simplify(symmetric-sp.eye(3)*sp.trace(symmetric)/3)


def stf_three(tensor):
    traces = [sum(tensor[first, contracted, contracted] for contracted in range(3)) for first in range(3)]
    return {indices: sp.simplify(value-(sp.KroneckerDelta(indices[1], indices[2])*traces[indices[0]]
                                      +sp.KroneckerDelta(indices[0], indices[2])*traces[indices[1]]
                                      +sp.KroneckerDelta(indices[0], indices[1])*traces[indices[2]])/5)
            for indices, value in tensor.items()}


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/transport'
    output.mkdir(parents=True, exist_ok=False)
    phase = sp.symbols('phase', real=True)
    radius, total_mass, frequency, deformability = sp.symbols('r Mtotal Omega lambda', positive=True)
    central_fraction = sp.symbols('chi', positive=True)
    companion_fraction = 1-central_fraction
    eta = central_fraction*companion_fraction
    normal = sp.Matrix([sp.cos(phase), sp.sin(phase), 0])
    tangent = sp.diff(normal, phase)
    angular_normal = sp.Matrix([0, 0, 1])
    basis_two = stf_two(normal*normal.T)
    basis_three = stf_three({indices: sp.prod(normal[index] for index in indices) for indices in product(range(3), repeat=3)})
    basis_current = stf_two(angular_normal*normal.T)
    position_central = companion_fraction*radius*normal
    position_companion = -central_fraction*radius*normal
    velocity_central = frequency*sp.diff(position_central, phase)
    quadrupole_amplitude = 3*deformability*companion_fraction*total_mass/radius**3
    quadrupole = quadrupole_amplitude*basis_two
    quadrupole_derivative = frequency*sp.diff(quadrupole, phase)
    translated_mass_three = {}
    for first, second, third in product(range(3), repeat=3):
        translated_mass_three[first, second, third] = (
            central_fraction*total_mass*position_central[first]*position_central[second]*position_central[third]
            +companion_fraction*total_mass*position_companion[first]*position_companion[second]*position_companion[third]
            +position_central[first]*quadrupole[second, third]+position_central[second]*quadrupole[first, third]
            +position_central[third]*quadrupole[first, second])
    translated_mass_three = stf_three(translated_mass_three)
    current_tide = sp.zeros(3)
    for first, second, index_a, index_b in product(range(3), repeat=4):
        current_tide[first, second] += sp.LeviCivita(index_a, index_b, first)*(
            quadrupole[second, index_a]*velocity_central[index_b]
            +position_central[index_a]*quadrupole_derivative[second, index_b]/2)
    current_tide = stf_two(current_tide)
    checks = []

    def exact(name, expression):
        assert sp.simplify(sp.expand_trig(expression)) == 0, name
        checks.append({'name': name, 'passed': True})

    predicted_octupole = eta*total_mass*radius**3*(1-2*central_fraction)+9*deformability*companion_fraction**2*total_mass/radius**2
    for indices in product(range(3), repeat=3):
        exact('translated_mass_octupole_'+''.join(map(str, indices)), translated_mass_three[indices]-predicted_octupole*basis_three[indices])
    current_amplitude = sp.Rational(9, 2)*deformability*companion_fraction**2*total_mass*frequency/radius**2
    for first, second in product(range(3), repeat=2):
        exact('continuity_current_quadrupole_'+str(first)+str(second), current_tide[first, second]-current_amplitude*basis_current[first, second])
    three_norm = sum(sp.diff(value, phase, 4).subs(phase, 0)**2 for value in basis_three.values())
    current_third = basis_current.diff(phase, 3).subs(phase, 0)
    current_norm = sp.trace(current_third.T*current_third)
    two_third = basis_two.diff(phase, 3).subs(phase, 0)
    two_norm = sp.trace(two_third.T*two_third)
    exact('mass_quadrupole_third_derivative_norm', two_norm-32)
    exact('mass_octupole_fourth_derivative_norm', three_norm-sp.Rational(8202, 5))
    exact('current_quadrupole_third_derivative_norm', current_norm-sp.Rational(1, 2))
    for contracted in range(3):
        exact('mass_octupole_trace_'+str(contracted), sum(basis_three[contracted, index, index] for index in range(3)))
    eta_symbol, tide = sp.symbols('eta t')
    fractional_radius_shift = 3*companion_fraction/central_fraction*tide
    octupole_circle = sp.expand((1-2*central_fraction)*(1+3*fractional_radius_shift)+9*companion_fraction/central_fraction*tide)
    current_circle = sp.expand((1-2*central_fraction)*(1+3*fractional_radius_shift)+sp.Rational(9, 2)*companion_fraction/central_fraction*tide)
    exact('circular_transported_mass_octupole', octupole_circle-(1-2*central_fraction)-18*companion_fraction**2/central_fraction*tide)
    exact('circular_transported_current_quadrupole', current_circle-(1-2*central_fraction)-sp.Rational(9, 2)*companion_fraction*(3-4*central_fraction)/central_fraction*tide)
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'checks': checks, 'mass_octupole_amplitude': str(sp.factor(predicted_octupole)),
              'transported_tidal_current_amplitude': str(sp.factor(current_amplitude)),
              'circular_mass_octupole_relative_amplitude': str(sp.factor(octupole_circle)),
              'circular_current_quadrupole_relative_amplitude': str(sp.factor(current_circle)),
              'derivative_norms': {'electric_quadrupole': str(two_norm), 'mass_octupole': str(three_norm), 'current_quadrupole': str(current_norm)},
              'assumptions': ['Center-of-mass frame; only body2 (fraction chi) is electrically deformable.',
                              'Conserved density/current second moment: integral xi_a j_b = dot(Q_ab)/2 up to trace when internal spin vanishes.',
                              'Linear parity-even quadrupole has no intrinsic odd current quadrupole; transported current is derived separately from an axial tidal response.',
                              'Adiabatic nonspinning circular response; no assertion that magnetic Love number is zero.']}
    (output/'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'derivative_norms': report['derivative_norms']}))


if __name__ == '__main__':
    main()
