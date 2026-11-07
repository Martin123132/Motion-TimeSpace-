from emission_angular_common import *


def main():
    modest()
    folder = ROOT / 'results/matched-integrated-parity'
    folder.mkdir(parents=True, exist_ok=False)
    bank = ROOT / 'banks/matched104-l4'
    packet = json.loads((bank / 'status.json').read_text())
    failures = [row for row in packet['checks'] if not row['passed']]
    assert len(failures) == 39 and all(row['name'].startswith('Scalar I/E parity closure') for row in failures)
    checks = [dict(name='Raw bank failures isolated to incorrect eventwise parity requirement', passed=True)]
    rows, inputs = [], [bank / 'status.json', ROOT / 'build_matched_compton.py', BRANCH / 'polarized-heat-momentum-grid-20261007/grid_common.py']
    for index, expansion in enumerate(packet['knots']):
        path = bank / ('knot-' + str(index) + '.npz')
        inputs.append(path)
        with np.load(path) as saved:
            theta = float(saved['theta'])
            basis = ConsistentBasis(**packet['basis_spec'])
            for model in range(2):
                checks.append(check('Stored mixed number null knot=' + str(index) + ' model=' + str(model),
                    linalg.norm(basis.chemical @ saved['mixed_0'][model]) / max(linalg.norm(saved['mixed_0'][model]), 1e-30), 1e-10))
        events = thermal_wave.prior.event_geometry(theta, 6)
        partners = np.arange(len(events['weight'])).reshape(-1, 12)[:, ::-1].ravel()
        checks.append(dict(name='Reflection pairing is an involution knot=' + str(index), passed=bool(np.array_equal(partners[partners], np.arange(len(partners))))))
        for name in ['incident', 'outgoing', 'cosine', 'weight']:
            error = np.max(abs(events[name] - events[name][partners])) / max(np.max(abs(events[name])), 1e-30)
            checks.append(check('Reflection leaves scalar ' + name + ' invariant knot=' + str(index), error, 1e-12))
        for degree in range(packet['maximum_degree'] + 1):
            first, second, names = thermal_wave.prior.angular_correlations(events, degree)
            retained = [names.index(name) for name in (['I'] if degree < 2 else ['I', 'E'])]
            excluded = [mode for mode in range(len(names)) if mode not in retained]
            error = 0.
            for source in retained:
                for target in excluded:
                    for values in [first, second]:
                        error = max(error, float(np.max(abs(values[source, target] + values[source, target, partners]))),
                                    float(np.max(abs(values[target, source] + values[target, source, partners]))))
            checks.append(check('Reflected-pair I/E versus B/V cancellation knot=' + str(index) + ' degree=' + str(degree), error, 1e-12))
            rows.append(dict(knot=index, degree=degree, pair_sum_error=error))
    checks.extend(dict(row) for row in packet['checks'] if not row['name'].startswith('Scalar I/E parity closure'))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        raw_bank=str(bank), validated_numerical_archives=[str(path) for path in inputs if path.suffix == '.npz'],
        original_failed_diagnostics_preserved=True,
        reason='Parity removes cross blocks after azimuthal reflection averaging, not per event. Reflection also preserves frequency, Bose and isotropic-background weights, so it cancels both Planck and mixed gain cross blocks.',
        baseline_matrices_unscaled=True, mixed_and_temperature_matrices_per_unit_heat=True,
        time_interpolation_refinement=False, full_wave_evolution=False), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], maximum_pair_sum=max(row['pair_sum_error'] for row in rows))), flush=True)


if __name__ == '__main__':
    main()
