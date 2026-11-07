from exact_angular_factor import *


def main():
    modest()
    folder = ROOT / 'results/exact-factor'
    folder.mkdir(parents=True, exist_ok=False)
    parent = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    for name, expected in parent['file_hashes'].items():
        assert digest(PARENT / name) == expected
    rows, benchmark = [], []
    for cosine in [-.8, -.2, .6]:
        hard = np.array([math.sqrt(1 - cosine**2), 0., cosine])
        for soft_direction, measure in weak.source.angular_nodes(3):
            angular = angular_basis(hard, soft_direction)
            for energy in [1e-7, 1e-4, .0035, .03, .2]:
                fractions = np.r_[np.geomspace(1e-8, .25, 17), -np.geomspace(1e-8, 1.1, 17)]
                soft = fractions * energy
                start = time.monotonic()
                original, photons, final, outgoing, denominator = tensor_batch(energy, soft, hard, soft_direction)
                direct_seconds = time.monotonic() - start
                tensor = factorized_tensor(energy, soft, hard, soft_direction, angular)
                start = time.monotonic()
                intensity = factorized_intensity(energy, soft, hard, soft_direction, angular)[0]
                fast_seconds = time.monotonic() - start
                expected = np.sum(abs(original)**2, axis=(1, 2, 3, 4, 5)) / 4
                relative_tensor = np.linalg.norm((tensor - original).reshape(len(soft), -1), axis=1) / np.linalg.norm(original.reshape(len(soft), -1), axis=1)
                rows.append(dict(energy=energy, tensor_relative=float(relative_tensor.max()),
                                 intensity_relative=float(np.max(abs(intensity / expected - 1)))))
                benchmark.append((direct_seconds, fast_seconds))
    checks = [
        dict(name='All4089 sealed parent payloads verified', passed=True),
        dict(name='Exact nine-tensor factorization reproduces full reduced amplitude',
             value=max(row['tensor_relative'] for row in rows), passed=max(row['tensor_relative'] for row in rows) < 1e-10),
        dict(name='Spin-completeness Gram intensity reproduces full spin/polarization sum',
             value=max(row['intensity_relative'] for row in rows), passed=max(row['intensity_relative'] for row in rows) < 1e-10),
    ]
    finish(folder, dict(checks=checks, cases=len(rows), events=len(rows) * 34, rows=rows,
        cached_evaluation_speed_ratio=sum(value[0] for value in benchmark) / sum(value[1] for value in benchmark),
        angular_precomputation_excluded_from_benchmark=True, finite_energy_truncation=False,
        coefficient_fit=False, gauge_scope='Exactly the same physical rest-frame transverse polarizations as inherited scalar source.'), __file__)
    print(json.dumps(dict(checks=checks, cases=len(rows), speed_ratio=sum(value[0] for value in benchmark) / sum(value[1] for value in benchmark))), flush=True)


if __name__ == '__main__':
    main()
