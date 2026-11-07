from leading_angular import *
from batched_real import intensity_batch, tensor_batch
from nonlocal_dc import gould


def main():
    modest()
    folder = ROOT / 'results/leading-angular'
    folder.mkdir(parents=True, exist_ok=False)
    fractions = np.array([.001, .02, .2, .45, -.03, -.3, -1.1])
    geometries = [
        (np.array([math.sqrt(1 - cosine**2), 0., cosine]), soft / np.linalg.norm(soft))
        for cosine, soft in [(.4, np.array([.2, .7, -.5])), (-.6, np.array([.3, -.2, .9])),
                              (.8, np.array([-.7, .4, .2]))]]
    rows, bose, poles = [], [], []
    for hard, soft in geometries:
        reference_tensor = leading_tensor(fractions, hard, soft)
        reference = np.sum(abs(reference_tensor)**2, axis=(1, 2, 3, 4, 5)) / 4
        geometry_rows = []
        for energy in [1e-3, 1e-4, 1e-5]:
            exact, photons, final, hard_energy, denominator = tensor_batch(energy, energy * fractions, hard, soft)
            intensities = np.sum(abs(exact)**2, axis=(1, 2, 3, 4, 5)) / 4
            geometry_rows.append(dict(energy=energy,
                intensity_relative=float(np.max(abs(intensities / reference - 1))),
                tensor_relative=float(np.linalg.norm(exact - reference_tensor) / np.linalg.norm(reference_tensor))))
        rows.append(geometry_rows)
        positive = np.array([.02, .2, .45])
        before = leading_intensity(positive, hard, soft)
        after = leading_intensity(1 - positive, soft, hard)
        bose.append(float(np.max(abs(before / after - 1))))
        signed = np.array([1e-6, -1e-6])
        value = leading_intensity(signed, hard, soft) * signed**2 * (1 - signed) / (2 * (1 + hard[2]**2))
        expected = np.linalg.norm(np.cross(np.array([0., 0., 1.]) - hard, soft))**2
        poles.append(float(np.max(abs(value / expected - 1))))
    split = np.array([.01, .1, .3, .45])
    angular_rows = []
    for order in [3, 4, 6]:
        cosines, weights = np.polynomial.legendre.leggauss(order)
        integrated = np.zeros(len(split))
        for cosine, weight in zip(cosines, weights):
            hard = np.array([math.sqrt(1 - cosine**2), 0., cosine])
            for soft, soft_weight in weak.source.angular_nodes(order):
                integrated += 2 * np.pi * weight * soft_weight * 3 * weak.source.ALPHA / (128 * np.pi**3) * split * (1 - split) * leading_intensity(split, hard, soft)
        expected = 4 * weak.source.ALPHA / (3 * np.pi) * gould(split) / split
        angular_rows.append(dict(order=order, ratios=(integrated / expected).tolist(),
                                 relative_error=float(np.max(abs(integrated / expected - 1)))))
    checks = [
        dict(name='Derived tensor approaches exact six-diagram amplitude without fitted coefficients', value=max(row[-1]['tensor_relative'] for row in rows), passed=all(row[-1]['tensor_relative'] < 2e-4 for row in rows)),
        dict(name='Pointwise intensity remainder shrinks with photon energy', passed=all(row[-1]['intensity_relative'] < row[0]['intensity_relative'] * .011 for row in rows)),
        dict(name='Leading intensity respects outgoing-photon exchange', value=max(bose), passed=max(bose) < 1e-10),
        dict(name='Leading soft pole matches inherited matching subtraction', value=max(poles), passed=max(poles) < 1e-4),
        dict(name='Leading angular integral reproduces independent Gould normalization', value=angular_rows[-1]['relative_error'], passed=angular_rows[-1]['relative_error'] < 1e-10),
    ]
    finish(folder, dict(checks=checks, amplitude_limits=rows, bose_errors=bose, soft_pole_errors=poles,
        angular_integrals=angular_rows, physical_transverse_polarizations_only=True,
        arbitrary_gauge_replacement_test_claimed=False, fitted_coefficients=0), __file__)
    print(json.dumps(dict(checks=checks, angular_integrals=angular_rows, amplitude_limits=rows)), flush=True)


if __name__ == '__main__':
    main()
