from wave_common import *


def main():
    modest()
    comparison = json.loads((ROOT / 'results/density-comparison/status.json').read_text())
    spectral = json.loads((ROOT / 'results/density-basis96-to104/status.json').read_text())
    rejected = json.loads((ROOT / 'results/density-basis-comparison/status.json').read_text())
    thermal = json.loads((ROOT / 'results/emission-response/status.json').read_text())
    frame = json.loads((ROOT / 'results/frame-and-gas-pairing/status.json').read_text())
    pair = json.loads((ROOT / 'results/leading-compton-pair/status.json').read_text())
    assert all(packet['all_checks_passed'] for packet in [comparison, spectral, thermal, frame, pair])
    assert not rejected['all_checks_passed']
    checks = [dict(name='Named accepted density, thermal, frame and Compton tests pass', passed=True),
              dict(name='Failed88-to96 low-frequency trial remains retained, not silently promoted', passed=True)]
    review = dict(accepted_scope='Source-sector milestone: evolving fixed-expansion emitting density tangent; leading-heat isotropic common-temperature derivative; source-frame pairing; finite-shift pair derivative.',
        full_finite_wavenumber_wave_evolution=False, full_stage80_original_wave_target_completed=False,
        all_requested_numerical_gates_closed=True,
        numerical_gate_scope='Only the named source-sector tests in this review; not an angular-source or CMB-transfer validation.',
        retained_unaccepted_accuracy_trials=['results/density-basis-comparison/status.json'],
        inherited_backgrounds_modified=False, new_empirical_fit=False,
        density_jacobian_max_relative_error_at_step_0001=max(row['spectral_derivative_relative_error'] for row in comparison['rows'] if row.get('epsilon') == .001),
        density_negative_control_relative_errors=[row['missing_ion_error'] for row in comparison['rows'] if 'missing_ion_error' in row],
        time_refinement_max=max(row['value'] for row in comparison['checks'] if 'time refinement' in row['name']),
        spectral_refinement_max=spectral['maximum'],
        failed_previous_spectral_refinement_max=rejected['maximum'],
        final_refined_density_results=spectral['rows'],
        emitted_wave_source_thermal_check_max=max(row['value'] for row in thermal['checks'] if 'mixed common-thermal' in row['name']),
        frame_and_gas_check_max=max(row['value'] for row in frame['checks']),
        approximation_scope=['Retained Stage79 leading-heat emission model, finite gas heat capacity; fixed reference Hubble history for the density derivative.',
            'Numerical finite-difference agreement is not a physical-model accuracy estimate.',
            'Time refinement tested at96 functions; basis refinement96-to104 separately. No exhaustive joint refinement or independent new event/emission-quadrature sweep.',
            'First saved nonzero density-tangent time is ln(10)/80. The very fast initial electron relaxation layer is not separately resolved.',
            'Common-temperature DC derivative is determined to retained heat order; arbitrary angular/nonthermal relativistic DC derivative is not inferred from the Planck coefficient.',
            'Source four-force pairing is scoped to the retained collision model, not a derivation of the entire parent matter action.'],
        next_target='Construct emitting angular Compton bank using the new analytic pair coefficients, insert the tested density/gas source and common-temperature column, derive or control the angular DC projection, then evolve the coupled finite-k mode.',
        conclusion='A concrete missing emitting density/gas coupling is derived and independently checked in both parents; the source response now has a tested route into the existing spatial hierarchy.')
    write_json(ROOT / 'ACCURACY-REVIEW.json', review)
    folder = ROOT / 'results/accuracy-review'
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=True), __file__,
        [ROOT / 'ACCURACY-REVIEW.json', *[ROOT / 'results' / name / 'status.json' for name in
        ['density-comparison', 'density-basis96-to104', 'density-basis-comparison', 'emission-response', 'frame-and-gas-pairing', 'leading-compton-pair']]])
    print(json.dumps(review), flush=True)


if __name__ == '__main__':
    main()
