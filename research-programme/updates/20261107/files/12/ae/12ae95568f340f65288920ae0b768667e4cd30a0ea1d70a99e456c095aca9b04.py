from rational_leading import *


def main():
    modest()
    folder = ROOT / 'results/rational-leading'
    folder.mkdir(parents=True, exist_ok=False)
    fractions = np.r_[np.geomspace(1e-6, .8, 101), -np.geomspace(1e-6, 1.4, 101)]
    rows = []
    for cosine in [-.8, -.2, .6]:
        hard = np.array([math.sqrt(1 - cosine**2), 0., cosine])
        for soft, measure in weak.source.angular_nodes(3):
            coefficients = angular_coefficients(hard, soft)
            terms = np.column_stack([np.ones_like(fractions), fractions, 1 / fractions, 1 / (1 - fractions)])
            tensor = np.einsum('nq,qabcfi->nabcfi', terms, coefficients)
            direct = leading_tensor(fractions, hard, soft)
            gram = angular_gram(hard, soft)
            fast = fast_intensity(fractions, gram)
            expected = np.sum(abs(direct)**2, axis=(1, 2, 3, 4, 5)) / 4
            rows.append(dict(tensor_relative=float(np.linalg.norm(tensor - direct) / np.linalg.norm(direct)),
                intensity_relative=float(np.max(abs(fast / expected - 1))),
                gram_minimum=float(np.linalg.eigvalsh(gram)[0])))
    checks = [
        dict(name='Analytically derived four rational tensors reproduce uncompressed leading tensor',
             value=max(row['tensor_relative'] for row in rows), passed=max(row['tensor_relative'] for row in rows) < 1e-10),
        dict(name='Fast leading intensity reproduces direct spin/polarization sum',
             value=max(row['intensity_relative'] for row in rows), passed=max(row['intensity_relative'] for row in rows) < 1e-10),
        dict(name='Leading intensity Gram matrix is nonnegative to rounding',
             value=min(row['gram_minimum'] for row in rows), passed=min(row['gram_minimum'] for row in rows) > -1e-10),
    ]
    finish(folder, dict(checks=checks, cases=len(rows), fractions=len(fractions),
        rational_terms=['1', 'eta', '1/eta', '1/(1-eta)'], coefficients_fitted=False), __file__)
    print(json.dumps(dict(checks=checks, cases=len(rows))), flush=True)


if __name__ == '__main__':
    main()
