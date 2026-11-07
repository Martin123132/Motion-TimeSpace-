from rectangular_common import *
from compare_source_vectors import dual_norm


def main():
    modest()
    folder = ROOT / 'results/source-resolution'
    folder.mkdir(parents=True, exist_ok=False)
    names = ['midpoint-log-pilot', 'midpoint-log32', 'midpoint-log48']
    runs = [ROOT / 'runs' / name for name in names]
    controls = [ROOT / 'controls' / name for name in ['pilot-leading-control', 'main-leading-control', 'refined-leading-control']]
    raw = [dict(np.load(path / 'source.npz')) for path in runs]
    corrected = [dict(np.load(path / 'source.npz')) for path in controls]
    mass = raw[-1]['mass']
    comparisons, checks = [], []
    for label, arrays in [('raw', raw), ('control_variate', corrected)]:
        for first, second, description in [(0, 1, 'outer'), (1, 2, 'real')]:
            before, after = arrays[first]['total'][1:-1], arrays[second]['total'][1:-1]
            ratio = dual_norm(before - after, mass) / dual_norm(after, mass)
            comparisons.append(dict(estimator=label, refinement=description, relative_change=ratio.tolist()))
            checks.append(dict(name=label + ' ' + description + ' full96 source converges within1percent',
                               value=float(ratio.max()), passed=bool(ratio.max() < .01)))
    components = []
    for name, arrays in zip(names, raw):
        components.append(dict(name=name, **{key: dual_norm(arrays[key][1:-1], mass).tolist()
                                            for key in ['total', 'born', 'real', 'virtual', 'state']}))
    slices = []
    for first, second in [(0, 1), (1, 2)]:
        difference = corrected[first]['total'][1:-1] - corrected[second]['total'][1:-1]
        slices.append(dict(first=names[first], second=names[second],
            coefficient_norm_by_index_blocks={str(lower) + ':' + str(upper):
                np.linalg.norm(difference[lower:upper], axis=0).tolist() for lower, upper in [(0, 8), (8, 48), (48, 96)]}))
    current_accepted = all(row['passed'] for row in checks if row['name'].startswith('control_variate'))
    finish(folder, dict(checks=checks, comparisons=comparisons, component_norms=components,
        diagnostic_index_blocks=slices, control_variate_source_accepted=current_accepted,
        raw_source_accepted=all(row['passed'] for row in checks if row['name'].startswith('raw')),
        full_parent_feedback_applied=False, no_modes_removed=True,
        scope='Mass-dual spectral-source resolution, not an observational fit or universal continuum-error certificate.'),
        __file__, [path / filename for path in runs + controls for filename in ['status.json', 'source.npz']])
    print(json.dumps(dict(checks=checks, component_norms=components, diagnostic_index_blocks=slices,
        control_variate_source_accepted=current_accepted)), flush=True)


if __name__ == '__main__':
    main()
