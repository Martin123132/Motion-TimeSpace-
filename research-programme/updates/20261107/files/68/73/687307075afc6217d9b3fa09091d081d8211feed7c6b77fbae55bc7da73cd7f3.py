from remainder_common import *
from compare_source_vectors import dual_norm


def main():
    modest()
    folder = ROOT / 'results/remaining-error'
    folder.mkdir(parents=True, exist_ok=False)
    paths = [ROOT / 'runs' / f'midpoint-real-refinement-a4-r{order}/source.npz' for order in [96, 192]]
    coarse, fine = [dict(np.load(path)) for path in paths]
    mass = fine['mass']
    errors = {key: coarse[key][1:-1] - fine[key][1:-1]
              for key in ['control', 'sampled_leading', 'kinematic_remainder', 'difference', 'remainder']}
    norms = {key: dual_norm(value, mass) for key, value in errors.items()}
    component_identity = float(np.max(abs(errors['remainder'] - errors['kinematic_remainder'] - errors['difference'])))
    lower = linalg.cholesky(mass, lower=True)
    whitened = linalg.solve_triangular(lower, errors['remainder'], lower=True)
    bands = []
    for start, end in [(0, 2), (2, 16), (16, 32), (32, 64), (64, 96)]:
        bands.append(dict(start=start, end_exclusive=end,
            whitened_error_fraction=(np.sum(whitened[start:end]**2, axis=0) / np.sum(whitened**2, axis=0)).tolist()))
    checks = [
        dict(name='Retained remainder drift decomposes into amplitude and kinematic terms', value=component_identity,
             passed=component_identity < 1e-12 * float(np.max(abs(errors['remainder'])))),
        dict(name='Whitened error reproduces full mass-dual norm',
             passed=bool(np.max(abs(np.linalg.norm(whitened, axis=0) / norms['remainder'] - 1)) < 1e-10)),
        dict(name='No modes removed from diagnosis', passed=whitened.shape == (96, 4)),
    ]
    finish(folder, dict(checks=checks, radial_comparison=[96, 192],
        drift_dual_norms={key: value.tolist() for key, value in norms.items()},
        kinematic_to_total_drift=(norms['kinematic_remainder'] / norms['remainder']).tolist(),
        amplitude_to_total_drift=(norms['difference'] / norms['remainder']).tolist(),
        whitened_bands=bands, band_interpretation='Cholesky-whitened basis coordinates, not an independent physical frequency decomposition.',
        conclusion='Refine the cheap exact-kinematics control and its matched leading subtraction before repeating expensive exact-amplitude or virtual-loop work.'),
        __file__, [*paths, *[path.parent / 'status.json' for path in paths]])
    print(json.dumps(dict(checks=checks, norms={key: value.tolist() for key, value in norms.items()},
        kinematic_to_total=(norms['kinematic_remainder'] / norms['remainder']).tolist(), bands=bands)), flush=True)


if __name__ == '__main__':
    main()
