from __future__ import annotations

import sympy as sp

from matching_common import modest_process, save


def main():
    modest_process()
    checks = []

    def exact(name, expression):
        residual = sp.simplify(expression)
        assert residual == 0, (name, residual)
        checks.append(dict(name=name, residual=str(residual), passed=True))

    carrier = sp.symbols('carrier', positive=True)
    coord, momentum, phase = sp.symbols('coord momentum phase', real=True)
    envelope = sp.exp(sp.I * phase) * (carrier * coord + sp.I * momentum) / sp.sqrt(2 * carrier)
    conjugate = sp.conjugate(envelope)
    exact('invert_coordinate', (envelope * sp.exp(-sp.I * phase) + conjugate * sp.exp(sp.I * phase)) / sp.sqrt(2 * carrier) - coord)
    exact('invert_momentum', -sp.I * sp.sqrt(carrier / 2) * (envelope * sp.exp(-sp.I * phase) - conjugate * sp.exp(sp.I * phase)) - momentum)
    bracket = sp.diff(envelope, coord) * sp.diff(conjugate, momentum) - sp.diff(envelope, momentum) * sp.diff(conjugate, coord)
    exact('canonical_complex_bracket', bracket + sp.I)
    frequency2, coupling, bath = sp.symbols('frequency2 coupling bath', real=True)
    envelope_dot = sp.diff(envelope, coord) * momentum + sp.diff(envelope, momentum) * (-frequency2 * coord + coupling * bath) + carrier * sp.diff(envelope, phase)
    exact('exact_envelope_equation', sp.I * envelope_dot - sp.exp(sp.I * phase) * ((frequency2 - carrier**2) * coord - coupling * bath) / sp.sqrt(2 * carrier))
    hubble, hubble_dot, chi, chi_dot, chi_ddot, scale, bare2, wave2 = sp.symbols('hubble hubble_dot chi chi_dot chi_ddot scale bare2 wave2', real=True)
    field_dot = scale**(-sp.Rational(3, 2)) * (chi_dot - sp.Rational(3, 2) * hubble * chi)
    field_ddot = scale**(-sp.Rational(3, 2)) * (chi_ddot - 3 * hubble * chi_dot + (sp.Rational(9, 4) * hubble**2 - sp.Rational(3, 2) * hubble_dot) * chi)
    transformed = scale**sp.Rational(3, 2) * (field_ddot + 3 * hubble * field_dot + (bare2 + wave2 / scale**2) * chi * scale**(-sp.Rational(3, 2)))
    exact('FLRW_rescaling', transformed - chi_ddot - (bare2 + wave2 / scale**2 - sp.Rational(3, 2) * hubble_dot - sp.Rational(9, 4) * hubble**2) * chi)
    light2, gap2, mixing, spectral = sp.symbols('light2 gap2 mixing spectral', positive=True)
    bath2 = light2 + gap2
    bare2 = light2 + mixing**2 * gap2
    coupling = mixing * gap2
    heavy2 = light2 + (1 + mixing**2) * gap2
    mass_matrix = sp.Matrix([[bare2, -coupling], [-coupling, bath2]])
    rotation = sp.Matrix([[1, -mixing], [mixing, 1]]) / sp.sqrt(1 + mixing**2)
    residual = rotation.T * mass_matrix * rotation - sp.diag(light2, heavy2)
    for row in range(2):
        for col in range(2):
            exact(f'constant_rotation_mass_{row}_{col}', residual[row, col])
            exact(f'constant_rotation_kinetic_{row}_{col}', (rotation.T * rotation - sp.eye(2))[row, col])
    exact('mass_determinant_positive', mass_matrix.det() - light2 * heavy2)
    schur = bare2 - spectral - coupling**2 / (bath2 - spectral)
    exact('light_pole_matching', schur.subs(spectral, light2))
    exact('positive_pole_residue', -sp.diff(schur, spectral).subs(spectral, light2) - (1 + mixing**2))
    exact('Schur_equals_full_determinant', (bath2 - spectral) * schur - (light2 - spectral) * (heavy2 - spectral))
    coord_light, coord_heavy, mom_light, mom_heavy = sp.symbols('coord_light coord_heavy mom_light mom_heavy', real=True)
    old_coord = rotation * sp.Matrix([coord_light, coord_heavy])
    old_mom = rotation * sp.Matrix([mom_light, mom_heavy])
    old_energy = (old_mom.T * old_mom + old_coord.T * mass_matrix * old_coord)[0] / 2
    new_energy = (mom_light**2 + mom_heavy**2 + light2 * coord_light**2 + heavy2 * coord_heavy**2) / 2
    exact('stress_energy_no_double_count', old_energy - new_energy)
    exact('pressure_no_double_count', (old_mom.T * old_mom - old_coord.T * mass_matrix * old_coord)[0] / 2 - (mom_light**2 + mom_heavy**2 - light2 * coord_light**2 - heavy2 * coord_heavy**2) / 2)
    accelerations = -3 * hubble * old_mom - mass_matrix * old_coord
    energy_rate = (old_mom.T * accelerations + old_coord.T * mass_matrix * old_mom)[0]
    exact('full_parent_energy_continuity', energy_rate + 3 * hubble * (old_mom.T * old_mom)[0])
    fraction = mixing**2 / (1 + mixing**2)
    mass_ratio2 = bath2 / light2
    shift = (bare2 - light2) / light2
    exact('mixing_hierarchy_cost', shift - fraction / (1 - fraction) * (mass_ratio2 - 1))
    quartic = sp.symbols('quartic', real=True)
    transformed_quartic = sp.expand(quartic * (coord_light - mixing * coord_heavy)**4 / (24 * (1 + mixing**2)**2))
    exact('inherited_quartic_cross_term', transformed_quartic.coeff(coord_light, 2).coeff(coord_heavy, 2) - quartic * mixing**2 / (4 * (1 + mixing**2)**2))
    elapsed, amplitude, heavy_mass = sp.symbols('elapsed amplitude heavy_mass', positive=True)
    hubble_eds = sp.Rational(2, 3) / elapsed
    average_rho = amplitude**2 * heavy_mass**2 / (2 * elapsed**2) + amplitude**2 / (4 * elapsed**4)
    average_pressure = amplitude**2 / (4 * elapsed**4)
    exact('EdS_phase_averaged_energy_conservation', sp.diff(average_rho, elapsed) + 3 * hubble_eds * (average_rho + average_pressure))
    exact('EdS_finite_mass_correction', (average_rho / (amplitude**2 * heavy_mass**2 / (2 * elapsed**2)) - 1) - 9 * hubble_eds**2 / (8 * heavy_mass**2))
    grav, density, wave, cosmic_a = sp.symbols('grav density wave cosmic_a', positive=True)
    jeans4 = 16 * sp.pi * grav * density * heavy_mass**2
    exact('Jeans_balance', jeans4 / (4 * heavy_mass**2) - 4 * sp.pi * grav * density)
    omega_total, heavy_share = sp.symbols('omega_total heavy_share', real=True)
    exact('dust_budget_not_added_twice', omega_total * heavy_share / cosmic_a**3 + omega_total * (1 - heavy_share) / cosmic_a**3 - omega_total / cosmic_a**3)
    report = save('derivation', __file__, dict(exact_checks=checks, count=len(checks),
        actual_new_fundamental_fields=0, exact_phase_space_reorganization=True,
        condensate_candidate_identified_with_real_parent=False,
        two_mode_result_scope='Constant-coupling, canonically normalized positive quadratic subfamily of existing real scalar/bath architecture.',
        physical_bath_spectrum_selected=False, cold_state_preparation_derived=False,
        old_cosmology_replaced=False, exact_electric_charge_derived=False))
    print(dict(state=report['state'], exact_identities=len(checks)), flush=True)


if __name__ == '__main__':
    main()
