from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import psutil
import sympy as sym


ROOT = Path(__file__).resolve().parent
POST = ROOT.parent
OUTPUT = ROOT / 'results' / 'first-candidate'
SOURCE_NAMES = [
    '4901-Y5-R2FR-nonabelian-SU2xSU3-parent-and-chiral-anomaly-cancellation-or-standard-model-correspondence-freeze.md',
    '4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md',
    '4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md',
    '5184-Y5-R2FR-stationary-PX-background-no-lump-and-mixed-Hessian-gate.md',
    '5187-Y5-R2FR-canonical-local-parent-action-Hessian-source-residue-and-scale-setting-theorem.md',
    '5188-Y5-R2FR-relational-clock-scalar-no-go-minimal-coframe-parent-and-Fierz-Pauli-selection-theorem.md',
    'RESULTS-20261003-fixed-profile-P7-bisection.md',
]


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    checkpoint = POST / '_checkpoints' / '20261003-pre-condensate-origin'
    backup = json.loads((checkpoint / 'status.json').read_text())
    if backup['state'] != 'complete':
        raise RuntimeError('Finish and verify the rollback snapshot before running candidate science.')
    if OUTPUT.exists():
        raise RuntimeError('Refusing to overwrite an executed result. Use a daughter run.')
    OUTPUT.mkdir(parents=True)
    checks = []

    def verify(name, actual, expected=0):
        difference = sym.simplify(actual - expected)
        passed = difference == 0
        checks.append({'name': name, 'passed': passed, 'difference': str(difference)})
        if not passed:
            raise AssertionError(f'{name}: {difference}')

    amplitude, mass_squared, quartic, chemical, phase_kinetic = sym.symbols(
        'amplitude mass_squared quartic chemical X_theta', positive=True)
    epsilon = sym.symbols('epsilon', real=True)
    amplitude_perturbation, amplitude_rate, amplitude_gradient = sym.symbols('sigma sigma_dot sigma_grad', real=True)
    phase_rate, phase_gradient = sym.symbols('pi_dot pi_grad', real=True)
    time = sym.symbols('time', real=True)
    field = sym.Function('psi')(time)
    friction = sym.symbols('gamma', real=True)
    boundary_lagrangian = -friction * field * sym.diff(field, time)
    boundary_euler = sym.diff(boundary_lagrangian, field) - sym.diff(sym.diff(boundary_lagrangian, sym.diff(field, time)), time)
    verify('constant_gamma_term_is_boundary', boundary_euler)
    derivative_symbols = sym.symbols('psi_t psi_x psi_y psi_z', real=True)
    old_kinetic = (derivative_symbols[0]**2 - sum(value**2 for value in derivative_symbols[1:])) / 2
    old_hessian = sym.hessian(old_kinetic, derivative_symbols)
    verify('old_scalar_principal_matrix_is_fixed', sym.trace((old_hessian - sym.diag(1, -1, -1, -1))**2))

    potential = mass_squared * amplitude**2 / 2 + quartic * amplitude**4 / 4
    algebraic_lagrangian = amplitude**2 * phase_kinetic - potential
    amplitude_squared = (2 * phase_kinetic - mass_squared) / quartic
    verify('amplitude_stationarity', (sym.diff(algebraic_lagrangian, amplitude) / amplitude).subs(amplitude**2, amplitude_squared))
    phase_pressure = sym.factor(algebraic_lagrangian.subs(amplitude**2, amplitude_squared))
    verify('eliminated_phase_pressure', phase_pressure, (2 * phase_kinetic - mass_squared)**2 / (4 * quartic))
    pressure_first = sym.diff(phase_pressure, phase_kinetic)
    pressure_second = sym.diff(phase_pressure, phase_kinetic, 2)
    verify('pressure_first_is_amplitude_squared', pressure_first, amplitude_squared)
    verify('pressure_second', pressure_second, 2 / quartic)
    background_amplitude_squared = (chemical**2 - mass_squared) / quartic
    phase_time_coefficient = sym.simplify((pressure_first + 2 * phase_kinetic * pressure_second).subs(phase_kinetic, chemical**2 / 2))
    sound_squared = sym.factor(background_amplitude_squared / phase_time_coefficient)
    verify('sound_speed_squared', sound_squared, (chemical**2 - mass_squared) / (3 * chemical**2 - mass_squared))

    full_lagrangian = (epsilon**2 * (amplitude_rate**2 - amplitude_gradient**2) / 2
        + (amplitude + epsilon * amplitude_perturbation)**2 * ((chemical + epsilon * phase_rate)**2 - epsilon**2 * phase_gradient**2) / 2
        - potential.subs(amplitude, amplitude + epsilon * amplitude_perturbation))
    quadratic = sym.expand(full_lagrangian).coeff(epsilon, 2)
    radial_mass_squared = 2 * (chemical**2 - mass_squared)
    expected_quadratic = ((amplitude_rate**2 - amplitude_gradient**2) / 2
        - radial_mass_squared * amplitude_perturbation**2 / 2
        + amplitude**2 * (phase_rate**2 - phase_gradient**2) / 2
        + 2 * amplitude * chemical * amplitude_perturbation * phase_rate)
    verify('full_quadratic_expansion', sym.expand(quadratic - expected_quadratic).subs(amplitude**2, background_amplitude_squared))
    verify('kinetic_hessian_positive_identity', sym.det(sym.hessian(quadratic, (amplitude_rate, phase_rate))), amplitude**2)
    momentum_phase = sym.symbols('p_phase', real=True)
    phase_canonical_rate = sym.symbols('canonical_phase_dot', real=True)
    mixing_kinetic = phase_canonical_rate**2 / 2 + 2 * chemical * amplitude_perturbation * phase_canonical_rate
    solved_rate = momentum_phase - 2 * chemical * amplitude_perturbation
    verify('hamiltonian_mixing_complete_square', (momentum_phase * phase_canonical_rate - mixing_kinetic).subs(phase_canonical_rate, solved_rate), solved_rate**2 / 2)

    frequency, wave_squared, frequency_squared = sym.symbols('omega k_squared omega_squared', real=True)
    inverse_propagator = sym.Matrix([[wave_squared + radial_mass_squared - frequency**2, 2 * sym.I * chemical * frequency], [-2 * sym.I * chemical * frequency, wave_squared - frequency**2]])
    dispersion_polynomial = sym.expand(inverse_propagator.det()).subs(frequency**4, frequency_squared**2).subs(frequency**2, frequency_squared)
    gap_squared = radial_mass_squared + 4 * chemical**2
    verify('dispersion_determinant', dispersion_polynomial, frequency_squared**2 - (2 * wave_squared + gap_squared) * frequency_squared + wave_squared * (wave_squared + radial_mass_squared))
    radical = sym.sqrt(gap_squared**2 / 4 + 4 * chemical**2 * wave_squared)
    lower_root = wave_squared + gap_squared / 2 - radical
    upper_root = wave_squared + gap_squared / 2 + radical
    verify('dispersion_lower_root', dispersion_polynomial.subs(frequency_squared, lower_root))
    verify('dispersion_upper_root', dispersion_polynomial.subs(frequency_squared, upper_root))
    verify('root_sum', lower_root + upper_root, 2 * wave_squared + gap_squared)
    verify('root_product', lower_root * upper_root, wave_squared * (wave_squared + radial_mass_squared))
    verify('low_energy_dispersion_matches_phase_metric', radial_mass_squared / gap_squared, sound_squared)
    expansion = sound_squared * wave_squared + 16 * chemical**4 * wave_squared**2 / gap_squared**3
    substituted_polynomial = sym.Poly(sym.expand(dispersion_polynomial.subs(frequency_squared, expansion)), wave_squared)
    verify('dispersion_series_linear', substituted_polynomial.coeff_monomial(wave_squared))
    verify('dispersion_series_quadratic', substituted_polynomial.coeff_monomial(wave_squared**2))

    pressure = sym.factor(phase_pressure.subs(phase_kinetic, chemical**2 / 2))
    energy = sym.factor(chemical**2 * background_amplitude_squared - pressure)
    verify('energy_density', energy, (chemical**2 - mass_squared) * (3 * chemical**2 + mass_squared) / (4 * quartic))
    verify('enthalpy_nonzero_expression', energy + pressure, chemical**2 * background_amplitude_squared)
    verify('equation_of_state', pressure / energy, (chemical**2 - mass_squared) / (3 * chemical**2 + mass_squared))
    vacuum_shift = sym.symbols('vacuum_shift', real=True)
    verify('vacuum_shift_does_not_remove_enthalpy', (energy + vacuum_shift) + (pressure - vacuum_shift), energy + pressure)
    verify('charge_from_pressure', sym.diff(pressure, chemical), chemical * background_amplitude_squared)
    verify('thermodynamic_energy_identity', chemical * sym.diff(pressure, chemical) - pressure, energy)

    power, legacy_coupling = sym.symbols('power legacy_coupling', positive=True)
    radial_power_potential = legacy_coupling * amplitude**power / power
    circular_frequency_squared = sym.diff(radial_power_potential, amplitude) / amplitude
    power_stiffness = sym.diff(radial_power_potential, amplitude, 2) - circular_frequency_squared
    verify('general_power_radial_stiffness', power_stiffness, (power - 2) * circular_frequency_squared)
    power_sound_squared = sym.simplify(power_stiffness / (power_stiffness + 4 * circular_frequency_squared))
    verify('general_power_sound_speed', power_sound_squared, (power - 2) / (power + 2))
    legacy_sound_squared = power_sound_squared.subs(power, sym.Rational(4, 3))
    verify('charged_extension_of_original_power_is_unstable', legacy_sound_squared, -sym.Rational(1, 5))
    verify('legacy_instability_band_upper_k_squared', (-(power - 2) * chemical**2).subs(power, sym.Rational(4, 3)), 2 * chemical**2 / 3)
    repaired_potential = radial_power_potential.subs(power, sym.Rational(4, 3)) + quartic * amplitude**4 / 4
    repaired_frequency_squared = sym.factor(sym.diff(repaired_potential, amplitude) / amplitude)
    repaired_stiffness = sym.factor(sym.diff(repaired_potential, amplitude, 2) - repaired_frequency_squared)
    verify('legacy_plus_quartic_radial_stiffness', repaired_stiffness, -2 * legacy_coupling * amplitude**(-sym.Rational(2, 3)) / 3 + 2 * quartic * amplitude**2)
    repair_ratio = sym.symbols('repair_ratio', nonnegative=True)
    ratio_substitution = {quartic: repair_ratio * legacy_coupling / amplitude**sym.Rational(8, 3)}
    repaired_sound_squared = sym.factor((repaired_stiffness / (repaired_stiffness + 4 * repaired_frequency_squared)).subs(ratio_substitution))
    verify('repaired_sound_speed_ratio', repaired_sound_squared, (3 * repair_ratio - 1) / (5 + 9 * repair_ratio))
    repaired_pressure = sym.simplify(repaired_frequency_squared * amplitude**2 / 2 - repaired_potential)
    repaired_energy = sym.simplify(repaired_frequency_squared * amplitude**2 - repaired_pressure)
    grand_potential = sym.simplify(repaired_potential - repaired_frequency_squared * amplitude**2 / 2)
    verify('repaired_pressure', repaired_pressure, (quartic * amplitude**4 - legacy_coupling * amplitude**sym.Rational(4, 3)) / 4)
    verify('repaired_grand_potential', grand_potential.subs(ratio_substitution), legacy_coupling * amplitude**sym.Rational(4, 3) * (1 - repair_ratio) / 4)
    verify('repaired_equation_of_state', (repaired_pressure / repaired_energy).subs(ratio_substitution), (repair_ratio - 1) / (5 + 3 * repair_ratio))
    verify('repaired_local_stability_boundary', repaired_sound_squared.subs(repair_ratio, sym.Rational(1, 3)))
    verify('repaired_coexistence_sound_speed', repaired_sound_squared.subs(repair_ratio, 1), sym.Rational(1, 7))
    verify('repaired_coexistence_pressure', repaired_pressure.subs(ratio_substitution).subs(repair_ratio, 1))
    verify('repaired_never_hides_enthalpy', (repaired_energy + repaired_pressure).subs(ratio_substitution), legacy_coupling * amplitude**sym.Rational(4, 3) * (1 + repair_ratio))

    sound_speed, kinetic_scale, normalization = sym.symbols('sound_speed kinetic_scale normalization', positive=True)
    flat_metric = sym.diag(-1, 1, 1, 1)
    raised_flow = sym.Matrix([1, 0, 0, 0])
    lowered_flow = flat_metric * raised_flow
    metric = kinetic_scale / (normalization * sound_speed) * (flat_metric + (1 - sound_speed**2) * lowered_flow * lowered_flow.T)
    principal = kinetic_scale * (flat_metric - (sound_speed**-2 - 1) * raised_flow * raised_flow.T)
    volume = kinetic_scale**2 / (normalization**2 * sound_speed)
    verify('effective_metric_volume', -metric.det(), volume**2)
    for row in range(4):
        for column in range(4):
            verify(f'effective_metric_principal_{row}_{column}', normalization * volume * metric.inv()[row, column], principal[row, column])
    verify('metric_null_speed', metric[0, 0] + sound_speed**2 * metric[1, 1])

    stress_background = sym.diag(energy, pressure, pressure, pressure)
    shear_plus = sym.diag(0, 1, -1, 0)
    shear_cross = sym.zeros(4)
    shear_cross[1, 2] = shear_cross[2, 1] = 1
    verify('homogeneous_plus_shear_zero', sym.trace(stress_background * shear_plus))
    verify('homogeneous_cross_shear_zero', sym.trace(stress_background * shear_cross))
    isotropic_pressure_variation = sym.symbols('delta_pressure', real=True)
    spatial_stress_variation = sym.diag(0, isotropic_pressure_variation, isotropic_pressure_variation, isotropic_pressure_variation)
    verify('linear_matter_plus_shear_zero', sym.trace(spatial_stress_variation * shear_plus))
    verify('linear_matter_cross_shear_zero', sym.trace(spatial_stress_variation * shear_cross))

    polar, azimuth = sym.symbols('polar azimuth', real=True)
    angular_integral = sym.integrate(sym.sin(polar)**5, (polar, 0, sym.pi)) * sym.integrate(sym.cos(azimuth)**2 * sym.sin(azimuth)**2, (azimuth, 0, 2 * sym.pi))
    verify('shear_angular_integral', angular_integral, 4 * sym.pi / 15)
    positive_frequency = sym.symbols('positive_frequency', positive=True)
    shear_density = sym.simplify(2 * sound_speed**4 * 2 * sym.pi / (4 * sound_speed**2 * (2 * sym.pi)**3) * angular_integral * (positive_frequency / (2 * sound_speed))**4 / (2 * sound_speed))
    verify('leading_phonon_shear_spectral_density', shear_density, positive_frequency**4 / (960 * sym.pi * sound_speed**3))

    samples = []
    for ratio in [sym.Rational(1001, 1000), sym.Rational(11, 10), sym.Integer(2), sym.Integer(10)]:
        substitutions = {chemical: ratio, mass_squared: 1, quartic: sym.Rational(3, 2)}
        speed_value = sound_squared.subs(substitutions)
        equation_value = (pressure / energy).subs(substitutions)
        assert 0 < speed_value < sym.Rational(1, 3)
        assert 0 < equation_value < sym.Rational(1, 3)
        for momentum_value in [sym.Rational(1, 100000), sym.Rational(1, 100), sym.Integer(1), sym.Integer(100)]:
            point = {**substitutions, wave_squared: momentum_value**2}
            low_value = lower_root.subs(point).evalf(65)
            high_value = upper_root.subs(point).evalf(65)
            assert low_value > 0 and high_value > 0
            samples.append({'chemical_over_mass': str(ratio), 'momentum_over_mass': str(momentum_value), 'omega_low_squared': str(low_value), 'omega_high_squared': str(high_value), 'sound_squared': str(speed_value), 'pressure_over_energy': str(equation_value)})
    source_hashes = {}
    for name in SOURCE_NAMES:
        source_hashes[name] = hashlib.sha256((POST / name).read_bytes()).hexdigest()
    formulas = {
        'amplitude_squared': str(amplitude_squared), 'phase_pressure': str(phase_pressure),
        'sound_squared': str(sound_squared), 'radial_mass_squared': str(radial_mass_squared),
        'gap_squared': str(gap_squared), 'omega_lower_squared': str(lower_root), 'omega_upper_squared': str(upper_root),
        'energy_density': str(energy), 'pressure': str(pressure),
        'original_power_charged_extension_sound_squared': str(legacy_sound_squared),
        'repair_ratio_definition': 'quartic * amplitude**(8/3) / legacy_coupling',
        'repaired_sound_squared': str(repaired_sound_squared),
        'repaired_pressure': str(repaired_pressure), 'repaired_energy': str(repaired_energy),
        'repaired_grand_potential': str(grand_potential),
        'positive_frequency_shear_density_at_zero_spatial_momentum': str(shear_density),
    }
    report = {
        'state': 'complete', 'created_at': datetime.now(timezone.utc).isoformat(),
        'checks': checks, 'exact_identity_checks': len(checks), 'numeric_spectrum_samples': samples,
        'formulas': formulas, 'source_hashes': source_hashes,
        'assumptions': ['natural_units_hbar_c_equal_one', 'flat_eta_is_assumed_not_derived', 'new_physical_complex_scalar_with_global_U1', 'positive_quartic_and_nonnegative_mass_squared', 'homogeneous_charged_state_mu_squared_gt_mass_squared', 'phase_EFT_requires_gradients_small_relative_to_radial_mass', 'shear_spectrum_is_leading_Gaussian_phonon_vacuum_contribution_only'],
        'scientific_results': {'old_canonical_real_scalar_changes_its_principal_cone': False, 'new_candidate_has_derived_phase_metric': True, 'new_candidate_is_derived_from_old_MTS': False, 'charged_background_is_cosmological_constant': False, 'elementary_linear_tensor_mode_in_this_candidate': False, 'nonperturbative_composite_spin_two_excluded': False, 'standard_model_derived': False, 'underlying_spacetime_derived': False, 'charged_original_power_extension_has_longwave_instability': True, 'this_does_not_establish_instability_of_original_real_MTS': True, 'added_quartic_local_stability_requires_ratio_gt_one_third': True, 'added_quartic_grand_canonical_preference_over_empty_state_requires_ratio_gt_one': True},
        'web_sources': ['https://arxiv.org/abs/1001.1044', 'https://arxiv.org/abs/1407.7896', 'https://arxiv.org/abs/0807.4910', 'https://arxiv.org/html/gr-qc/0505065v4'],
        'cpu_affinity': process.cpu_affinity(), 'subagents': 0, 'github_action': False,
    }
    (OUTPUT / 'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks), 'numeric_samples': len(samples), 'candidate': 'new_complex_scalar_not_adopted_into_MTS'}))


if __name__ == '__main__':
    main()
