from grid_common import *


def load_run(label):
    folder = ROOT / 'runs' / label
    metadata = json.loads((folder / 'status.json').read_text())
    assert metadata['all_checks_passed']
    blocks = []
    for degree in range(9):
        with np.load(folder / ('evolution-' + str(degree) + '.npz'), allow_pickle=False) as saved:
            block = {name: saved[name].copy() for name in saved.files}
        block['names'] = metadata['rows'][degree]['names']
        blocks.append(block)
    return blocks


def interpolation(nodes, values, target):
    result = np.empty((len(values), len(target)), dtype=complex)
    for index, value in enumerate(values):
        result[index] = np.interp(target, nodes, value.real) + 1j * np.interp(target, nodes, value.imag)
    return result


def quadrature(nodes):
    points, weights = np.polynomial.legendre.leggauss(6)
    width = np.diff(nodes)
    targets = (nodes[:-1, None] + .5 * (points[None, :] + 1) * width[:, None]).ravel()
    measure = (.5 * width[:, None] * weights[None, :]).ravel()
    occupation = 1 / np.expm1(targets)
    return targets, measure * targets ** 2 * occupation * (1 + occupation) / I3


def compare(left, right, elastic_left=None, elastic_right=None):
    sectors = {name: dict(delta=None, reference=None, initial=None) for name in ['I', 'E', 'B', 'V', 'plasma_temperature', 'plasma_velocity']}
    checks, details = [], []
    for degree, (coarse, fine) in enumerate(zip(left, right)):
        assert np.allclose(coarse['times'], fine['times'], rtol=0, atol=1e-16)
        lower = max(coarse['nodes'][0], fine['nodes'][0])
        upper = min(coarse['nodes'][-1], fine['nodes'][-1])
        nodes = np.unique(np.r_[lower, upper, coarse['nodes'], fine['nodes']])
        nodes = nodes[(nodes >= lower) & (nodes <= upper)]
        targets, weights = quadrature(nodes)
        weights /= 2 * degree + 1
        coarse_values, fine_values = coarse['defects'].copy(), fine['defects'].copy()
        if elastic_left is not None:
            for warm, cold in [(coarse, elastic_left[degree]), (fine, elastic_right[degree])]:
                checks.append(float(np.linalg.norm(warm['equilibrium'] - cold['equilibrium'])))
            coarse_values -= elastic_left[degree]['defects']
            fine_values -= elastic_right[degree]['defects']
        for mode, name in enumerate(coarse['names']):
            coarse_slice = slice(mode * len(coarse['nodes']), (mode + 1) * len(coarse['nodes']))
            fine_slice = slice(mode * len(fine['nodes']), (mode + 1) * len(fine['nodes']))
            first = interpolation(coarse['nodes'], coarse_values[:, coarse_slice], targets)
            second = interpolation(fine['nodes'], fine_values[:, fine_slice], targets)
            initial = interpolation(fine['nodes'], fine['initial'][None, fine_slice], targets)[0]
            difference = np.sum(abs(first - second) ** 2 * weights, axis=1)
            reference = np.sum(abs(second) ** 2 * weights, axis=1)
            initial_size = float(np.sum(abs(initial) ** 2 * weights))
            section = sectors[name]
            section['delta'] = difference if section['delta'] is None else section['delta'] + difference
            section['reference'] = reference if section['reference'] is None else section['reference'] + reference
            section['initial'] = initial_size if section['initial'] is None else section['initial'] + initial_size
            details.append(dict(degree=degree, sector=name, peak_reference_norm=float(np.sqrt(max(reference))),
                                peak_difference_norm=float(np.sqrt(max(difference)))))
        if degree in [0, 1]:
            name = 'plasma_temperature' if degree == 0 else 'plasma_velocity'
            assert coarse['capacity'] == fine['capacity']
            capacity = float(fine['capacity'])
            sectors[name] = dict(delta=capacity * abs(coarse_values[:, -1] - fine_values[:, -1]) ** 2,
                                 reference=capacity * abs(fine_values[:, -1]) ** 2,
                                 initial=capacity * abs(fine['initial'][-1]) ** 2)
    initial_norm = float(np.sqrt(sum(section['initial'] for section in sectors.values())))
    floor = 1e-12 * initial_norm
    rows = []
    for name, section in sectors.items():
        reference = float(np.sqrt(max(section['reference'])))
        error = float(np.sqrt(max(section['delta'])))
        resolved = reference > floor
        rows.append(dict(sector=name, peak_reference_norm=reference, peak_difference_norm=error,
                         relative_discrepancy=error / reference if resolved else None,
                         numerically_resolved=resolved, absolute_roundoff_floor=floor,
                         meets_accuracy_gate=error <= .002 * reference if resolved else error <= floor))
    return rows, details, max(checks, default=0.)


def main():
    modest()
    folder = ROOT / 'results/response-refinements'
    assert not folder.exists()
    pairs = [('96', '144', 'frequency96to144'), ('144', '192', 'frequency144to192'),
             ('192', '192-refined', 'event-and-cell'), ('192-refined', '224-band', 'expanded-band')]
    records, checks, inputs = [], [], []
    for fixture in ['heavy', 'cold', 'synthetic']:
        for first, second, label in pairs:
            left, right = load_run(fixture + '-' + first), load_run(fixture + '-' + second)
            labels = [fixture + '-' + first, fixture + '-' + second]
            if fixture == 'synthetic':
                elastic_left, elastic_right = None, None
            else:
                labels += [fixture + '-' + first + '-elastic', fixture + '-' + second + '-elastic']
                elastic_left, elastic_right = load_run(labels[-2]), load_run(labels[-1])
            rows, details, equilibrium_error = compare(left, right, elastic_left, elastic_right)
            records.append(dict(fixture=fixture, comparison=label, sectors=rows, degree_diagnostics=details,
                                warm_elastic_equilibrium_difference=equilibrium_error,
                                passed=all(row['meets_accuracy_gate'] for row in rows)))
            checks.append(dict(name=fixture + ':' + label + ': each resolved sector meets small-response refinement',
                               passed=all(row['meets_accuracy_gate'] for row in rows)))
            if fixture != 'synthetic':
                checks.append(dict(name=fixture + ':' + label + ': same equilibrium before subtracting cold control',
                                   passed=equilibrium_error < 1e-14, value=equilibrium_error))
            for name in labels:
                inputs.append(ROOT / 'runs' / name / 'status.json')
                inputs.extend((ROOT / 'runs' / name).glob('*.npz'))
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        rows=records, gate=.002, raw_failed_accuracy_trials_retained=True,
                        norm='Peak over saved optical depths of continuous spectral entropy norm, sector by sector.',
                        parent_comparison='Warm minus same-grid elastic, computed from evolving defects, not bulk states.',
                        synthetic_comparison='Full equilibrium-subtracted heat and polarized relaxation.',
                        floor='1e-12 times total initial norm; raw null/roundoff diagnostics retained.',
                        common_domain_band_check=True, outside_common_domain_not_compared=True),
           __file__, sorted(set(inputs)))
    print(json.dumps(dict(count=len(checks), failed=[row['name'] for row in checks if not row['passed']],
                          summary=[dict(fixture=row['fixture'], comparison=row['comparison'],
                                        sectors=[dict(sector=sector['sector'], error=sector['relative_discrepancy'],
                                                      passed=sector['meets_accuracy_gate']) for sector in row['sectors']])
                                   for row in records])), flush=True)


if __name__ == '__main__':
    main()
