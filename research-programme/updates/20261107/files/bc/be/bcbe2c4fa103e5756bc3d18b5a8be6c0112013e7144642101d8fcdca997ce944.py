from azimuth_common import *
from project_azimuth import physical_nodes


def main():
    modest()
    folder = ROOT / 'results/preflight'
    folder.mkdir(parents=True, exist_ok=False)
    assert digest(PARENT / 'results/stage-integrity.json') == PARENT_SEAL
    seal = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    assert seal['state'] == 'complete' and len(seal['file_hashes']) == 14309
    for name, expected in seal['file_hashes'].items():
        assert digest(PARENT / name) == expected, name
    checks = [dict(name='All14309 sealed parent payloads verified unchanged', passed=True)]
    theta = json.loads((PARENT / 'runs/expensive-h5/status.json').read_text())['configuration']['temperature']
    rows = []
    for part in ['expensive', 'control']:
        coarse = {node_key(identity):identity for identity in physical_nodes(theta, part, 5, 4)}
        fine = list(physical_nodes(theta, part, 5, 8))
        matches = [identity for identity in fine if node_key(identity) in coarse]
        assert len(fine) == 2 * len(coarse) and len(matches) == len(coarse)
        error = max(abs(identity['electron_weight'] / coarse[node_key(identity)]['electron_weight'] - .5) for identity in matches)
        assert error == 0.
        assert len({node_key(identity) for identity in fine}) == len(fine)
        assert all(identity['electron_weight'] > 0 and identity['seed_weight'] > 0 and identity['hard_weight'] > 0 for identity in fine)
        checks.append(dict(name='Nested physical identities, positive and halved shared weights: ' + part, passed=True))
        rows.append(dict(part=part, total=len(fine), reused=len(matches), new=len(fine)-len(matches)))
    fourier = []
    for count in [4, 8]:
        phases = np.arange(count) * 2 * np.pi / count
        residual = max(abs(np.mean(np.exp(1j * harmonic * phases)) - (1 if harmonic % count == 0 else 0)) for harmonic in range(-16, 17))
        fourth = float(np.mean(np.cos(phases)**4))
        mixed = float(np.mean(np.cos(phases)**2 * np.sin(phases)**2))
        target_fourth, target_mixed = (.5, 0.) if count == 4 else (.375, .125)
        checks.append(dict(name='Fourier selection and transverse fourth moments: azimuth' + str(count),
            value=float(residual), passed=bool(residual < 1e-13 and abs(fourth-target_fourth) < 1e-14 and abs(mixed-target_mixed) < 1e-14)))
        fourier.append(dict(count=count, maximum_fourier_residual=float(residual), cos_fourth=fourth, cos_squared_sin_squared=mixed))
    finish(folder, dict(checks=checks, projected_nodes=rows, angular_moments=fourier,
        exact_rule_identity_not_full_integrand_error_bound=True, total_new_virtual_loops_expected=2240,
        maximum_compute_workers=2, library_threads=1, modes_removed=0),
        __file__, [PARENT / 'runs/expensive-h5/status.json', ROOT / 'project_azimuth.py'])
    print(json.dumps(dict(checks=checks, projected_nodes=rows, angular_moments=fourier)), flush=True)


if __name__ == '__main__':
    main()
