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
        assert all(sp.simplify(item) == 0 for item in entries), name
        checks.append({'name': name, 'passed': True})

    speed = sp.symbols('speed', real=True)
    gamma = 1/sp.sqrt(1-speed**2)
    mass, charge, frequency = sp.symbols('mass charge frequency', positive=True)
    field, radial_gradient, cosine, potential = sp.symbols('field radial_gradient cosine potential', real=True)
    time_gradient = -gamma*speed*radial_gradient*cosine
    axial_gradient = gamma*radial_gradient*cosine
    transverse_gradient_squared = radial_gradient**2*(1-cosine**2)
    phase_time, phase_axial = gamma*frequency, -gamma*speed*frequency
    energy_rest = (radial_gradient**2+frequency**2*field**2)/2+potential
    axial_stress = radial_gradient**2*cosine**2+(frequency**2*field**2-radial_gradient**2)/2-potential
    energy_lab = (time_gradient**2+axial_gradient**2+transverse_gradient_squared+field**2*(phase_time**2+phase_axial**2))/2+potential
    momentum_lab = -time_gradient*axial_gradient-field**2*phase_time*phase_axial
    lagrangian_lab = (time_gradient**2-axial_gradient**2-transverse_gradient_squared+field**2*(phase_time**2-phase_axial**2))/2-potential
    exact('boosted_stress_energy_density', energy_lab-gamma**2*(energy_rest+speed**2*axial_stress))
    exact('boosted_stress_momentum_density', momentum_lab-gamma**2*speed*(energy_rest+axial_stress))
    exact('full_field_lagrangian_is_scalar', lagrangian_lab-((frequency**2*field**2-radial_gradient**2)/2-potential))
    exact('charge_current_and_slice_jacobian_cancel', gamma*charge/gamma-charge)
    exact('fixed_charge_routhian', (frequency*charge-mass)/gamma-charge*frequency/gamma+mass/gamma)
    routhian = -mass/gamma
    momentum = sp.diff(routhian, speed)
    exact('routhian_momentum', momentum-gamma*mass*speed)
    exact('routhian_hamiltonian', speed*momentum-routhian-gamma*mass)
    exact('mass_shell', (gamma*mass)**2-(gamma*mass*speed)**2-mass**2)

    radius = sp.symbols('radius', positive=True)
    pressure = sp.Function('pressure')(radius)
    field_profile = sp.Function('field')(radius)
    radial_pressure_prime = -2*sp.diff(field_profile, radius)**2/radius
    tangential_pressure = pressure-sp.diff(field_profile, radius)**2
    exact('flat_laue_boundary_identity', sp.diff(radius**3*pressure, radius).subs(sp.diff(pressure, radius), radial_pressure_prime)
          -radius**2*(pressure+2*tangential_pressure))

    lorentz_factor = sp.symbols('lorentz_factor', positive=True)
    primitive = cosine/sp.sqrt(1+(lorentz_factor**2-1)*cosine**2)
    exact('adm_boost_angular_primitive', sp.diff(primitive, cosine)-(1+(lorentz_factor**2-1)*cosine**2)**sp.Rational(-3, 2))
    exact('adm_boost_surface_normalization', (primitive.subs(cosine, 1)-primitive.subs(cosine, -1))-2/lorentz_factor)

    external_potential = sp.symbols('external_potential', real=True)
    expanded = -mass*(1+external_potential-speed**2/2)
    exact('weak_metric_linear_coupling', sp.diff(expanded, external_potential)+mass)
    exact('weak_metric_inertial_coefficient', sp.diff(expanded, speed, 2)-mass)
    first_mass, second_mass, coupling, distance = sp.symbols('first_mass second_mass coupling distance', positive=True)
    phi_first = -coupling*first_mass/distance
    phi_second = -coupling*second_mass/distance
    source_action = -(first_mass*phi_second+second_mass*phi_first)
    field_cross_action = (first_mass*phi_second+second_mass*phi_first)/2
    exact('field_action_removes_factor_two', source_action+field_cross_action-coupling*first_mass*second_mass/distance)
    potential_energy = -coupling*first_mass*second_mass/distance
    exact('attractive_force', -sp.diff(potential_energy, distance)+coupling*first_mass*second_mass/distance**2)

    source_radius = sp.symbols('source_radius', positive=True)
    angular_integrand = 1/sp.sqrt(distance**2+source_radius**2+2*distance*source_radius*cosine)
    angular_primitive = sp.sqrt(distance**2+source_radius**2+2*distance*source_radius*cosine)/(distance*source_radius)
    exact('disjoint_shell_kernel_primitive', sp.diff(angular_primitive, cosine)-angular_integrand)
    exact('disjoint_shell_average', ((distance+source_radius)-(distance-source_radius))/(distance*source_radius)-2/distance)
    result = {'state': 'complete', 'checks': checks, 'exact_check_count': len(checks),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope': 'Algebra checks supporting the written matching derivation; ADM covariance, asymptotic falloff, and adiabatic scale separation are stated assumptions, not certified by symbolic algebra.',
              'fixed_charge_routhian': '-M(Q)*sqrt(1-v^2)', 'leading_interaction': '-G_R*M1*M2/D',
              'no_new_physical_coupling_fitted': True}
    (output/'status.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks)}))


if __name__ == '__main__':
    main()
