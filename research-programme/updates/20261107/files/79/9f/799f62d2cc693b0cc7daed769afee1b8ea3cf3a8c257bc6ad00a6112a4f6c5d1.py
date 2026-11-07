from __future__ import annotations

import hashlib
import json
from pathlib import Path

import fitz
import psutil
import sympy as sp


ROOT = Path(__file__).resolve().parent


def stf(matrix):
    symmetric = (matrix+matrix.T)/2
    return symmetric-sp.eye(3)*sp.trace(symmetric)/3


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/matching'
    output.mkdir(parents=True, exist_ok=False)
    checks = []

    def exact(name, expression):
        reduced = sp.simplify(expression)
        assert reduced == 0, (name, reduced)
        checks.append({'name': name, 'passed': True})

    radius, mass, polar, azimuth = sp.symbols('r M theta phi', positive=True)
    metric, lapse, shift_function = [sp.Function(name)(radius) for name in ['F', 'nu', 'f']]
    coefficient = sp.diff(lapse, radius)-sp.diff(metric, radius)/(2*metric)
    response = radius**2*shift_function
    operator = sp.diff(response, radius, 2)-coefficient*sp.diff(response, radius)
    operator += (2*coefficient/radius-2/radius**2-4/(radius**2*metric))*response
    weight = radius**4*sp.sqrt(metric)*sp.exp(-lapse)
    positive_potential = 4*radius**2*sp.exp(-lapse)/sp.sqrt(metric)
    self_adjoint = sp.diff(weight*sp.diff(shift_function, radius), radius)-positive_potential*shift_function
    exact('positive_static_form', self_adjoint-weight*operator/radius**2)
    ratio = sp.symbols('z', positive=True)
    special = sp.Function('H')(ratio)
    hyper_equation = ratio*(1-ratio)*sp.diff(special, ratio, 2)+6*(1-ratio)*sp.diff(special, ratio)-4*special
    vacuum_expression = 6*special+6*ratio*sp.diff(special, ratio)+ratio**2*sp.diff(special, ratio, 2)-(6-2*ratio)*special/(1-ratio)
    exact('decaying_hypergeometric_vacuum_equation', vacuum_expression-ratio*hyper_equation/(1-ratio))
    wronskian = (-5+4*ratio)*special-ratio*(1-ratio)*sp.diff(special, ratio)
    exact('constant_vacuum_Wronskian', sp.diff(wronskian, ratio)+hyper_equation)
    exact('vacuum_Wronskian_normalization', wronskian.subs({ratio: 0, special: 1})+5)
    edge_metric, distance = sp.symbols('Fs d', positive=True)
    edge_coefficient = (12*edge_metric)**(-sp.Rational(3, 2))
    amplitude = edge_coefficient*distance**3
    edge_gradient_energy = edge_metric*sp.diff(amplitude, distance)**2/2
    edge_potential = sp.Rational(3, 8)*amplitude**sp.Rational(4, 3)
    exact('compact_edge_pressure_order4_cancels', edge_gradient_energy-edge_potential)
    exact('compact_edge_density_order4', edge_gradient_energy+edge_potential-distance**4/(192*edge_metric**2))
    cartesian = sp.Matrix(sp.symbols('x y zeta', real=True))
    curvature_amplitude, current_amplitude = sp.symbols('B S', real=True)
    magnetic = sp.diag(-curvature_amplitude/2, -curvature_amplitude/2, curvature_amplitude)
    current = sp.diag(-current_amplitude/2, -current_amplitude/2, current_amplitude)
    applied_metric = sp.Matrix([sp.Rational(2, 3)*sum(sp.LeviCivita(index, first, second)*magnetic[first, third]*cartesian[second]*cartesian[third]
                                         for first in range(3) for second in range(3) for third in range(3)) for index in range(3)])
    magnetic_reconstructed = sp.zeros(3)
    for first in range(3):
        for second in range(3):
            magnetic_reconstructed[first, second] = sum(sp.LeviCivita(contracted, vector, first)*sp.diff(applied_metric[vector], cartesian[second], cartesian[contracted])
                                                        +sp.LeviCivita(contracted, vector, second)*sp.diff(applied_metric[vector], cartesian[first], cartesian[contracted])
                                                        for contracted in range(3) for vector in range(3))/4
            exact('magnetic_curvature_convention_'+str(first)+str(second), magnetic_reconstructed[first, second]-magnetic[first, second])
    normal = sp.Matrix([sp.sin(polar)*sp.cos(azimuth), sp.sin(polar)*sp.sin(azimuth), sp.cos(polar)])
    angular_tangent = radius*sp.diff(normal, azimuth)
    angular_applied = (applied_metric.subs(dict(zip(cartesian, radius*normal))).T*angular_tangent)[0]
    induced_metric = sp.Matrix([-4/radius**3*sum(sp.LeviCivita(index, first, second)*current[first, third]*normal[second]*normal[third]
                                         for first in range(3) for second in range(3) for third in range(3)) for index in range(3)])
    angular_induced = (induced_metric.T*angular_tangent)[0]
    exact('external_angular_metric', angular_applied-curvature_amplitude*radius**3*sp.sin(polar)**2*sp.cos(polar))
    exact('induced_angular_metric', angular_induced+6*current_amplitude/radius**2*sp.sin(polar)**2*sp.cos(polar))
    exact('response_sigma_conversion', angular_induced/ angular_applied*radius**5+6*current_amplitude/curvature_amplitude)
    recovered = sp.zeros(3)
    for first in range(3):
        for second in range(3):
            recovered[first, second] = sum(sp.LeviCivita(left, vector, first)*sp.LeviCivita(vector, inner, derivative)*current[inner, other]
                  *(sp.KroneckerDelta(left, derivative)*sp.KroneckerDelta(second, other)+sp.KroneckerDelta(left, other)*sp.KroneckerDelta(second, derivative))
                  for left in range(3) for vector in range(3) for inner in range(3) for derivative in range(3) for other in range(3))/3
    recovered = stf(recovered)
    for first in range(3):
        for second in range(3):
            exact('source_current_moment_normalization_'+str(first)+str(second), recovered[first, second]-current[first, second])
    sigma_bar, scalar_current, scalar_tide = sp.symbols('sigma_bar Sscalar Bscalar', nonzero=True)
    auxiliary = sp.Rational(2, 3)*scalar_current*scalar_tide-scalar_current**2/(3*sigma_bar)
    exact('constitutive_variation', sp.diff(auxiliary, scalar_current).subs(scalar_current, sigma_bar*scalar_tide))
    exact('half_interaction_after_elimination', auxiliary.subs(scalar_current, sigma_bar*scalar_tide)-sigma_bar*scalar_tide**2/3)
    companion, total, separation, frequency, reduced, perturbation = sp.symbols('mu MT d Omega mur epsilon', positive=True)
    correction_radius = sp.symbols('dr')
    lagrangian = reduced*(separation**2*frequency**2/2+total/separation)+6*perturbation*sigma_bar*companion**2*frequency**2/separation**4
    reference = sp.symbols('d0', positive=True)
    force = sp.diff(lagrangian, separation).subs(separation, reference*(1+perturbation*correction_radius)).series(perturbation, 0, 2).removeO()
    first_force = sp.factor(force.coeff(perturbation, 1).subs(frequency**2, total/reference**3))
    radial_shift = sp.solve(first_force, correction_radius)[0]
    exact('circular_magnetic_radius_shift', radial_shift-8*sigma_bar*companion**2/(reduced*reference**6))
    energy = frequency*sp.diff(lagrangian, frequency)-lagrangian
    energy = energy.subs(separation, reference*(1+perturbation*radial_shift)).series(perturbation, 0, 2).removeO()
    energy_tide = sp.factor(energy.coeff(perturbation, 1).subs(frequency**2, total/reference**3))
    exact('circular_magnetic_energy', energy_tide-22*sigma_bar*companion**2*total/reference**7)
    source = ROOT.parent/'pn-balance-20261004/sources/banihashemi-vines-2020.pdf'
    document = fitz.open(source)
    for page in [5, 6, 7]:
        document[page].get_pixmap(matrix=fitz.Matrix(1.7, 1.7)).save(ROOT/f'sources/banihashemi-vines-2020-page{page+1}.png')
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'checks': checks, 'input_hashes': {str(source): hashlib.sha256(source.read_bytes()).hexdigest()},
              'normalization': 'q=a P+b Q; geometric sigma_bar=G*sigma_bar=-b/(6a); geometric sigma_BV=-b/(12a), with c=1.',
              'positive_static_form': '(p f_prime)_prime-V f=0, f=q/r^2, p=r^4 sqrt(F)/N>0, V=4r^2/(N sqrt(F))>0.',
              'edge': 'h~(R-r)^3; rho~(R-r)^4/(192 Fs^2), leading p_r order4 cancels, no axial scalar/edge displacement or linear shell; q and q_prime continuous.',
              'matched_action': 'L_B=(geometric sigma_bar/3)*B_ij B_ij in G=1; standard retained-GR source coupling, not a free healthy oscillator proof.',
              'conservative_circle': 'delta r/d0=8 sigma_bar mu^2/(mur*d0^6); deltaE=22 sigma_bar mu^2 MT/d0^7.',
              'scope': 'Static response and leading conservative matching; full magnetic radiation/balance remains next.',
              'reference': 'Banihashemi-Vines2020 Eqs20,25,32-35; moment normalization independently checked against the conserved current definition.'}
    (output/'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'normalization': report['normalization']}))


if __name__ == '__main__':
    main()
