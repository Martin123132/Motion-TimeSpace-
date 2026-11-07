from population_common import *


def main():
    modest()
    folder = ROOT / 'results/population-comparison'
    folder.mkdir(parents=True, exist_ok=False)
    names = ['midpoint-pilot', 'midpoint-population-v2', 'midpoint-population-v3',
             'quarter-population-v2', 'final-population-v2']
    for optional in ['midpoint-real-refinement', 'midpoint-floor-control']:
        if (ROOT / 'runs' / optional / 'COMPLETE').is_file():
            names.append(optional)
    packets, arrays, paths = {}, {}, []
    for name in names:
        location = ROOT / 'runs' / name
        packets[name] = json.loads((location / 'status.json').read_text())
        assert (location / 'COMPLETE').exists() and packets[name]['all_checks_passed']
        arrays[name] = dict(np.load(location / 'projection.npz'))
        paths.extend([location / 'status.json', location / 'projection.npz'])
    control_path = ROOT / 'results/input-and-born-control/status.json'
    control = json.loads(control_path.read_text())
    assert control['all_checks_passed']
    absolute_tolerance = control['source_absolute_tolerance_for_projection']
    checks, comparisons, rows = [], [], []
    backgrounds = [thermal_wave.thermal.ThermalBackground(model) for model in ['heavy', 'cold']]
    comparison_pairs = [('midpoint-pilot', 'midpoint-population-v2', 'Full population, seed, hard and real refinement'),
                        ('midpoint-population-v2', 'midpoint-population-v3', 'Thermal loop angular refinement on same outer grid')]
    for optional in names[5:]:
        comparison_pairs.append(('midpoint-population-v2', optional, optional))
    for first, second, label in comparison_pairs:
        before, after = arrays[first]['current_total'][0], arrays[second]['current_total'][0]
        error = float(np.max(abs(before - after)))
        tolerance = max(.01 * float(np.max(abs(after))), absolute_tolerance)
        relative = error / float(np.max(abs(after)))
        comparisons.append(dict(name=label, first=first, second=second, max_absolute_change=error,
                                relative_to_correction=relative, tolerance=tolerance,
                                absolute_accuracy_gate_used=absolute_tolerance > .01 * float(np.max(abs(after)))))
        checks.append(dict(name=label, value=error, limit=tolerance, passed=error < tolerance))
    for name in names:
        saved, packet = arrays[name], packets[name]
        nlo = saved['current_total'][0]
        born = saved['current_born'][0]
        symmetry = float(np.linalg.norm(saved['total'] - saved['total'].T) / np.linalg.norm(saved['total']))
        eigenvalues = np.linalg.eigvalsh(saved['born'] + saved['total'])
        minimum_ratio = float(eigenvalues[0] / max(abs(eigenvalues[-1]), 1e-300))
        checks.append(dict(name='Projected matched symmetry ' + name, value=symmetry, passed=symmetry < 1e-10))
        checks.append(dict(name='Born plus correction nonnegative in tested actual-profile span ' + name,
                           value=minimum_ratio, passed=minimum_ratio > -1e-10))
        joining = float(max(abs(nlo[0] - nlo[1]), abs(nlo[2] - nlo[3])))
        checks.append(dict(name='Reported joining sensitivity below retained absolute source tolerance ' + name,
                           value=joining, limit=absolute_tolerance, passed=joining < absolute_tolerance))
        absolute_node_bound = np.zeros(4)
        part_bound = np.zeros(4)
        for path in sorted((ROOT / 'runs' / name / 'nodes').glob('*.json')):
            row = json.loads(path.read_text())
            absolute_node_bound += row['weight'] * abs((-np.asarray(row['parts']['total']) @ saved['coefficients'])[0])
            part_bound += row['weight'] * sum(abs((-np.asarray(row['parts'][key]) @ saved['coefficients'])[0]) for key in ['real', 'virtual', 'state'])
            paths.append(path)
        checks.append(dict(name='Finite-quadrature triangle bound contains signed source ' + name,
                           passed=bool(np.all(abs(nlo) <= absolute_node_bound * (1 + 1e-12)))))
        locals_at_epoch = [background.at(packet['configuration']['fraction'] * math.log(10)) for background in backgrounds]
        rate = np.repeat([local['coefficient'] / local['thermal_parameter'] for local in locals_at_epoch], 2)
        heat = np.repeat([background.chi for background in backgrounds], 2)
        conductance = float(saved['born'][0, 0])
        susceptibility = 1 / (conductance + heat / rate)
        checks.append(dict(name='Finite-capacity fixed-spectrum response has positive conductance ' + name,
                           value=conductance, passed=conductance > 0))
        rows.append(dict(name=name, fraction=packet['configuration']['fraction'], temperature=packet['temperature'],
            photon_source_per_tau=nlo.tolist(), gas_source_per_tau=saved['current_total'][-1].tolist(),
            baseline_photon_source_per_tau=born.tolist(), correction_over_own_born=(nlo / born).tolist(),
            source_per_expansion_fraction=(heat * rate * nlo).tolist(),
            joining_absolute_difference=joining, finite_quadrature_absolute_node_bound=absolute_node_bound.tolist(),
            finite_quadrature_absolute_component_bound=part_bound.tolist(),
            fixed_spectrum_gas_gain=susceptibility.tolist(),
            local_fixed_spectrum_gas_response_estimate=(-susceptibility * nlo).tolist(),
            continuous_domain_bound=False, full_spectrum_feedback_applied=False))
    finish(folder, dict(checks=checks, comparisons=comparisons, rows=rows,
        absolute_tolerance=absolute_tolerance, numerical_finite_domain_energy_projection_accepted=all(item['passed'] for item in checks),
        relative_one_percent_precision_claimed=False, omitted_seed_tail_bounded=False,
        collective_region_bounded=False, full_parent_feedback_applied=False,
        statistical_measure='Normalized Maxwell-Juttner, seed Planck and angular quadrature; same ordinary Born control.',
        scope='Resolved-domain actual-profile energy source and numerical sensitivity, not an unconditional all-frequency remainder bound.'),
        __file__, [control_path, *paths])
    print(json.dumps(dict(checks=len(checks), failed=[item['name'] for item in checks if not item['passed']],
                         comparisons=comparisons, rows=rows)), flush=True)


if __name__ == '__main__':
    main()
