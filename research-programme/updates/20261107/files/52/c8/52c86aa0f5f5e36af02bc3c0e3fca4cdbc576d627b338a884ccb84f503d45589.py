from spectrum_decomposition_common import *
import mpmath as mp


def main():
    modest()
    folder = ROOT / 'results/validation'
    folder.mkdir(parents=True, exist_ok=False)
    data_folder = ROOT / 'results/decomposition-v2'
    report = json.loads((data_folder / 'status.json').read_text())
    chain = ancestors()
    parent = chain[PARENT / 'results/stage-integrity.json']
    assert sum(len(packet['file_hashes']) for packet in chain.values()) == 219814
    hashes = {}
    for name, sha in parent['file_hashes'].items():
        path = PARENT / name
        assert digest(path) == sha, path
        hashes[str(path)] = sha
    for filename, sha in report['input_hashes'].items():
        path = Path(filename)
        assert digest(path) == sha, path
        if not path.is_relative_to(ROOT):
            inherited.verify_source(path, chain)
            hashes[filename] = sha
    checks = [dict(name='Immediate parent and consumed sources unchanged', passed=True)]
    assert report['count'] == len(report['checks']) == 589
    failed = [row for row in report['checks'] if not row['passed']]
    assert len(failed) == 16
    assert all(row['name'].startswith('Independent energy input:') and ':full2100:' in row['name'] for row in failed)
    assert all(row['passed'] for row in report['checks'] if ':canonical700' in row['name'])
    assert report['source_column_order'] == ['central-seed4-join1', 'central-seed4-join2']
    assert report['evolution_steps'] == report['source_evaluations'] == 0
    assert report['inherited_stage141_flags'] == parent['retained_failed_checks'] == 10
    checks.append(dict(name='Column semantics and canonical acceptance; sixteen fine-rule flags retained', passed=True))
    inputs = [data_folder / 'status.json', ROOT / 'DEVELOPMENT-NOTE.md']
    maximum_svd, maximum_metric = 0., 0.
    comparisons, physical_rows = {}, {}
    for case, variants in report['cases'].items():
        model = case.split('-')[0]
        heat = report['metadata'][model]['heat']
        for variant, rules in variants.items():
            for rule, groups in rules.items():
                path = data_folder / f'{case}-{variant}-{rule}.npz'
                packet = read_npz(path)
                templates_path = data_folder / (rule + '-templates.npz')
                templates = read_npz(templates_path)
                inputs.extend([path, templates_path])
                assert all(np.isfinite(value).all() for value in packet.values())
                measure, frequency = templates['measure'], templates['frequency']
                assert np.array_equal(packet['measure'], measure) and np.array_equal(packet['frequency'], frequency)
                design = np.sqrt(measure)[:, None] * templates['templates']
                for group, table in groups.items():
                    potential, energy = packet[group + '_potential'], packet[group + '_energy']
                    eta = energy / float(templates['capacity'])
                    distortion = potential - frequency[:, None] * eta
                    amplitudes = np.linalg.lstsq(design, np.sqrt(measure)[:, None] * distortion, rcond=None)[0]
                    residual = distortion - templates['templates'] @ amplitudes
                    scale = np.maximum(np.sqrt(np.sum(measure[:, None] * distortion ** 2, axis=0)), 1e-300)
                    svd_error = np.sqrt(np.sum(measure[:, None] * (residual - packet[group + '_residual']) ** 2, axis=0)) / scale
                    maximum_svd = max(maximum_svd, float(svd_error.max()))
                    stored = np.array([table['mu'], table['y']])
                    errors = abs(heat * amplitudes - stored) / np.maximum(abs(stored), 1e-300)
                    maximum_metric = max(maximum_metric, float(errors.max()))
                    residual_norm = np.sqrt(np.sum(measure[:, None] * packet[group + '_residual'] ** 2, axis=0))
                    assert np.array_equal(residual_norm, np.array(table['residual_norm']))
                    fractions = np.array(table['residual_squared_fraction_by_frequency_bin'])
                    assert np.max(abs(fractions.sum(axis=0) - 1)) < 1e-12
                for key in ['potential', 'energy', 'amplitudes', 'residual']:
                    saved = packet['saved_' + key]
                    feedback = packet['feedback_' + key]
                    combined = packet['corrected_' + key]
                    delta = combined[..., :3] - (saved + feedback)
                    assert np.max(abs(delta)) < 1e-10 * max(float(np.max(abs(combined))), 1e-300)
                    assert np.max(abs(combined[..., 3:] - (combined[..., :1] + combined[..., 1:3]))) < 1e-10 * max(float(np.max(abs(combined))), 1e-300)
        primary = variants['physical']['canonical700']['corrected']
        original = variants['physical']['canonical700']['saved']
        feedback = variants['physical']['canonical700']['feedback']
        common = variants['cubic']['canonical700']['corrected']
        medium = variants['physical']['full1400']['corrected']
        fine = variants['physical']['full2100']['corrected']
        comparison = {}
        for field in ['mu', 'y']:
            central = np.array(primary[field])
            denominator = abs(central)
            comparison[field] = dict(
                common_minus_physical_absolute=(abs(np.array(common[field]) - central)).tolist(),
                common_difference_over_physical=(abs(np.array(common[field]) - central) / denominator).tolist(),
                readout_1400_minus_700_absolute=(abs(np.array(medium[field]) - central)).tolist(),
                readout_2100_minus_1400_absolute=(abs(np.array(fine[field]) - np.array(medium[field]))).tolist(),
                readout_2100_minus_1400_over_primary=(abs(np.array(fine[field]) - np.array(medium[field])) / denominator).tolist(),
                feedback_over_original=(abs(np.array(feedback[field]) / np.array(original[field]))).tolist(),
                window_over_baseline_signed=(central[1:3] / central[0]).tolist())
        comparisons[case] = comparison
        physical_rows[case] = primary
        packet = read_npz(data_folder / f'{case}-physical-canonical700.npz')
        meta = report['metadata'][model]
        frequency = packet['frequency']
        weight = np.exp(-frequency) / (-np.expm1(-frequency)) ** 2
        frequency_hz = frequency * meta['k_B'] * meta['reference_temperature_K'] / meta['h_P']
        factor = 2 * meta['h_P'] * frequency_hz ** 3 / meta['c'] ** 2
        potential = packet['corrected_potential']
        occupation = heat * weight[:, None] * potential
        intensity = factor[:, None] * occupation
        reconstructed = heat * weight[:, None] * (packet['corrected_temperature'] + packet['corrected_joint'] + packet['corrected_residual'])
        test(checks, 'Physical occupation reconstruction:' + case,
             np.max(abs(reconstructed - occupation)) / max(float(np.max(abs(occupation))), 1e-300))
        assert np.all(np.isfinite(intensity))
        np.savez_compressed(folder / (case + '-normalized-spectrum.npz'),
                            dimensionless_frequency=frequency, frequency_Hz=frequency_hz,
                            delta_occupation=occupation, delta_specific_intensity_W_m2_Hz_sr=intensity,
                            heat=heat, reference_temperature_K=meta['reference_temperature_K'], scale=meta['scale'])
    test(checks, 'Independent direct SVD residuals for all24 readouts', maximum_svd)
    test(checks, 'Independent physical mu y amplitudes for all72 group readouts', maximum_metric, 1e-9)
    capacities = {}
    for digits in [50, 70]:
        with mp.workdps(digits):
            def integrand(frequency):
                occupation = 1 / mp.expm1(frequency)
                return frequency ** 4 * occupation * (1 + occupation) / (mp.pi ** 4 / 15)
            value = mp.quad(integrand, [mp.mpf('1e-5'), mp.mpf('.001'), mp.mpf('.1'), 1, 10, 60])
            capacities[str(digits)] = mp.nstr(value, digits)
    with mp.workdps(80):
        precision_difference = float(abs(mp.mpf(capacities['50']) - mp.mpf(capacities['70'])))
    test(checks, '50 and70 digit independent finite-band capacity', precision_difference, 1e-45)
    finite_capacity = float(capacities['70'])
    quadrature = {}
    for rule, info in report['rules'].items():
        quadrature[rule] = dict(capacity=info['capacity'],
                               capacity_minus_precise=info['capacity'] - finite_capacity,
                               capacity_fractional_discrepancy=info['capacity'] / finite_capacity - 1)
    matching = {}
    for model in ['heavy', 'cold']:
        first = physical_rows[model + '-m20']
        second = physical_rows[model + '-m40']
        matching[model] = {field: (abs(np.array(second[field]) - np.array(first[field])) /
                           abs(np.array(first[field]))).tolist() for field in ['mu', 'y']}
    for script in ROOT.glob('*.py'):
        compile(script.read_text(encoding='utf-8'), str(script), 'exec')
    assert not list(ROOT.rglob('__pycache__'))
    workbench = POST.parent / 'formalization-workbench'
    recent = [str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime > STARTED.timestamp()]
    assert not recent
    checks.append(dict(name='Scripts compile without caches;protected workbench modification-time count zero', passed=True))
    failed_by_scope = dict(current_finer_readout_energy_input=failed,
                           inherited_stage141=parent['retained_failure_names'])
    summary = dict(stage=142, physical_rows=physical_rows, comparisons=comparisons,
                   matching_width_sensitivities=matching, metadata=report['metadata'],
                   physical_column_order=DISPLAY_NAMES, frequency_bin_edges=BINS.tolist(),
                   precise_finite_band_capacity=capacities, readout_quadrature_moments=quadrature,
                   scientific_checks=len(report['checks']), passing_scientific_checks=sum(row['passed'] for row in report['checks']),
                   current_retained_flags=len(failed), inherited_retained_flags=10, failed_by_scope=failed_by_scope,
                   canonical_checks_all_pass=True, readout_units='dimensionless occupation; SI specific intensity at a=1e-5',
                   final_epoch_scale=1e-5, physical_extra_source_window_fraction=[.25, .5],
                   full_source_history_completed=False, observational_fit=False,
                   numerical_sensitivities_are_total_uncertainty=False,
                   next_target='Extend the actual extra source into the next adjacent temperature interval using saved event evaluations where available; propagate its contribution through the same temperature/mu/y/residual map. The corrected feedback history is complete, but the physical extra source still covers only .25U to .5U. Do not launch another whole-history numerical refinement by default.')
    write_json(ROOT / 'NUMERICAL-SUMMARY.json', summary)
    finish(folder, dict(checks=checks, accepted_scope_verified=True,
                        rehashed_prior_files=len(hashes), consumed_and_immediate_rehashed=hashes,
                        canonical_scientific_checks_accepted=True, all_finer_energy_checks_passed=False,
                        all_readouts_verified_independently=True, current_retained_flags=len(failed),
                        inherited_retained_flags=10, precise_capacities=capacities,
                        independent_svd_maximum=maximum_svd, independent_amplitude_maximum=maximum_metric,
                        compiled_scripts=len(list(ROOT.glob('*.py'))),
                        protected_workbench_recent_modified_file_count=0),
           __file__, [*inputs, ROOT / 'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(validation_checks=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                          rehashed_prior_files=len(hashes), current_flags=len(failed), inherited_flags=10,
                          independent_svd=maximum_svd, independent_amplitude=maximum_metric,
                          precise_capacity=capacities['70'], rule_moments=quadrature)), flush=True)


if __name__ == '__main__':
    main()
