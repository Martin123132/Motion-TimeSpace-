from spectrum_decomposition_common import *


def main():
    modest()
    folder = ROOT / 'results/decomposition-v2'
    folder.mkdir(parents=True, exist_ok=False)
    chain = ancestors()
    checks, inputs, cases = [], [], {}
    specification_path = BRANCH / 'emitting-thermal-background-20261008/banks/infrared96-q700/status.json'
    specification = json.loads(specification_path.read_text())['basis_spec']
    basis = infrared_ladder.ConsistentBasis(**specification)
    readers = {'canonical700': ShapeReadout(basis, canonical=True),
               'full1400': ShapeReadout(basis, 1400),
               'full2100': ShapeReadout(basis, 2100)}
    projection_path = BRANCH / 'temperature-distortion-projection-20261012/results/projection/status.json'
    projection = json.loads(projection_path.read_text())
    column_path = BRANCH / 'downstream-window-transfer-20261012/results/window-transfer/status.json'
    column_metadata = json.loads(column_path.read_text())
    assert column_metadata['column_order'][:2] == ['central-seed4-join1', 'central-seed4-join2']
    inputs.extend([specification_path, projection_path, column_path])
    documentation = ['temperature-distortion-projection-20261012/DERIVATION.md',
                     'mu-y-residual-decomposition-20261012/DERIVATION.md',
                     'downstream-window-transfer-20261012/DERIVATION.md',
                     'driven-low-frequency-turnover-20261012/turnover_common.py']
    inputs.extend(BRANCH / path for path in documentation)
    for label, reader in readers.items():
        np.savez_compressed(folder / (label + '-templates.npz'), frequency=reader.frequency, measure=reader.measure,
                            standard=reader.standard, templates=reader.templates, shifts=reader.shifts,
                            capacity=reader.capacity, gram=reader.gram, amplitude_matrix=reader.amplitude_matrix,
                            basis_values=reader.values, temperature_coefficients=basis.temperature)
        coefficients = np.array([[.21, -.15, 0., .13], [0., 0., -.26, .17]])
        temperatures = np.array([.1, -.2, .04, .09])
        synthetic = reader.templates @ coefficients + reader.frequency[:, None] * temperatures
        split = reader.split_values(synthetic, reader.capacity * temperatures)
        test(checks, 'Synthetic amplitudes:' + label, np.max(abs(split['amplitudes'] - coefficients)))
        test(checks, 'Synthetic residual:' + label, np.max(norm(split['residual'], reader.measure)))
        pure = reader.split_values(reader.frequency[:, None] * temperatures, reader.capacity * temperatures)
        test(checks, 'Pure temperature not mislabeled:' + label, np.max(abs(pure['amplitudes'])))
        test(checks, 'Template conditioning:' + label, reader.condition, 1e6)
        test(checks, 'Finite-band capacity near four:' + label, abs(reader.capacity - 4), 1e-8)
        invariants(checks, reader, split, 'synthetic-' + label)
    metadata = {}
    for model in ['heavy', 'cold']:
        baseline, window, paths = load_histories(model)
        inputs.extend(paths)
        heat = float(baseline['heat'])
        metadata[model] = projection['models'][model]['metadata']
        assert metadata[model]['heat'] == heat
        assert metadata[model]['scale'] == 1e-5
        saved_energy = np.r_[baseline['energy_scaled'][-1], window['energy'][-1, :2]]
        saved_coefficients = np.column_stack([baseline['profiles'][-1], window['photon'][-1, :, :2]])
        for match in [20, 40]:
            case = f'{model}-m{match}'
            owner = PARENT / 'results' / ('feedback-' + case)
            endpoint_path = owner / 'corrected-readout-state.npz'
            endpoint = read_npz(endpoint_path)
            inputs.append(endpoint_path)
            lineage_difference = endpoint['profiles'][0] - saved_coefficients
            test(checks, 'Endpoint coefficient lineage:' + case,
                 np.max(norm(basis.values @ lineage_difference, basis.measure) /
                        np.maximum(norm(basis.values @ saved_coefficients, basis.measure), 1e-300)))
            saved_coefficients = endpoint['profiles'][0].copy()
            assert endpoint['coordinate'][0] == window['coordinate'][-1] == baseline['expansion'][-1]
            cases[case] = {}
            for variant in ['physical', 'cubic']:
                response_path = owner / (variant + '-response.npz')
                source_path = owner / (variant + '-source.npz')
                response = read_npz(response_path)
                with np.load(source_path) as saved:
                    projected = saved['projected_replacement'][-1].copy()
                    source_endpoint = float(saved['coordinate'][-1])
                inputs.extend([response_path, source_path])
                assert source_endpoint == float(endpoint['coordinate'][0])
                assert response['photon_final'].shape == (96, 12)
                assert int(response['integration_steps']) == 2048
                cases[case][variant] = {}
                for rule, reader in readers.items():
                    raw = compact_defect(reader.frequency, endpoint['frequency'], endpoint['defect'][0], match / 1000)
                    unresolved = raw - reader.values @ projected
                    resolved = reader.values @ response['photon_final'][:, :3]
                    saved_potential = reader.values @ saved_coefficients
                    correction = resolved + unresolved
                    if rule == 'canonical700':
                        assert np.array_equal(response['frequency'], reader.frequency)
                        assert np.array_equal(response['measure'], reader.measure)
                        assert np.array_equal(saved_potential, response['saved_potential'])
                        for key, values in [('unresolved_change', unresolved), ('resolved_change', resolved), ('physical_change', correction)]:
                            test(checks, 'Parent readout:' + case + ':' + variant + ':' + key,
                                 np.max(norm(values - response[key], reader.measure) /
                                        np.maximum(norm(response[key], reader.measure), 1e-300)))
                    correction_energy = response['energy'][-1, :3] + (reader.measure * reader.frequency) @ unresolved
                    corrected = saved_potential + correction
                    corrected_energy = saved_energy + correction_energy
                    populations = {
                        'saved': (saved_potential, saved_energy),
                        'feedback': (correction, correction_energy),
                        'corrected': (expanded(corrected), expanded(corrected_energy))}
                    results, archive = {}, {}
                    for group, (values, energy) in populations.items():
                        result = reader.split_values(values, energy)
                        invariants(checks, reader, result, ':'.join([case, variant, rule, group]))
                        results[group] = result
                        for key, item in result.items():
                            archive[group + '_' + key] = item
                        if group != 'feedback':
                            allowance = 256 * EPS * np.maximum((reader.measure * reader.frequency) @ abs(values), 1e-300)
                            test(checks, 'Independent energy input:' + ':'.join([case, variant, rule, group]),
                                 np.max(abs(result['energy_defect']) / allowance), 1.)
                    joined_amplitudes = results['saved']['amplitudes'] + results['feedback']['amplitudes']
                    test(checks, 'Saved plus feedback amplitudes:' + ':'.join([case, variant, rule]),
                         np.max(norm(reader.templates @ (joined_amplitudes - results['corrected']['amplitudes'][:, :3]), reader.measure) /
                                np.maximum(results['corrected']['distortion_norm'][:3], 1e-300)))
                    total_amplitudes = expanded(results['corrected']['amplitudes'][:, :3])
                    test(checks, 'Baseline plus direct MTS amplitudes:' + ':'.join([case, variant, rule]),
                         np.max(norm(reader.templates @ (total_amplitudes - results['corrected']['amplitudes']), reader.measure) /
                                np.maximum(results['corrected']['distortion_norm'], 1e-300)))
                    np.savez_compressed(folder / f'{case}-{variant}-{rule}.npz', **archive,
                                        heat=heat, saved_independent_energy=saved_energy,
                                        response_independent_energy=response['energy'][-1, :3],
                                        unresolved=unresolved, resolved=resolved, raw_endpoint=raw,
                                        frequency=reader.frequency, measure=reader.measure)
                    cases[case][variant][rule] = {
                        group: metrics(reader, result, heat) for group, result in results.items()}
            print(json.dumps(dict(case=case, completed=True)), flush=True)
    for path in sorted(set(inputs)):
        inherited.verify_source(path, chain)
    report = dict(checks=checks, cases=cases, metadata=metadata, original_column_names=NAMES,
                  corrected_display_columns=DISPLAY_NAMES, source_column_order=column_metadata['column_order'][:2],
                  frequency_bin_edges=BINS.tolist(), basis_specification=specification,
                  rules={label: dict(capacity=reader.capacity, condition=reader.condition,
                                    correlation=reader.correlation, shifts=reader.shifts.tolist()) for label, reader in readers.items()},
                  inherited_stage141_flags=10, source_evaluations=0, evolution_steps=0,
                  source_window_fraction=[.25, .5], endpoint_scale=1e-5,
                  physical_amplitudes_are_at_saved_epoch=True, present_day_observation_comparison=False,
                  outside_window_source_completed=False, new_physical_fit=False)
    finish(folder, report, __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failures=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
