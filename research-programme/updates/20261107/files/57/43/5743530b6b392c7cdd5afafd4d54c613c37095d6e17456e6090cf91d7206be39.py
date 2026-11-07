from datetime import datetime, timezone
from common import ROOT, PRIOR, HIERARCHY, WAVE, GATE, ALGEBRA, modest, guard, check_prior, require, read, write, digest, load, source_curves
import numpy as np
import sympy as sp
from scipy.linalg import eigh_tridiagonal
from scipy.special import gammaln

LEVELS = (32, 64, 128, 192)


def first_return_bound(maximum, distance):
    order = 2 * (maximum - 2)
    if distance == 0:
        return 0.
    if order <= distance:
        return 2.
    log_bound = np.log(2.) + order * np.log(distance) - gammaln(order + 1) - np.log1p(-distance / (order + 1))
    return float(np.exp(min(np.log(2.), log_bound)))


def main():
    modest()
    check_prior()
    require(not (ROOT / "controls").exists(), "predictions must precede controls")
    ell = sp.symbols("ell", integer=True, positive=True)
    identity = sp.simplify((ell + 1) / (2 * ell + 1) * sp.sqrt((2 * ell + 1) / (2 * ell + 3)) - (ell + 1) / sp.sqrt((2 * ell + 1) * (2 * ell + 3)))
    require(identity == 0, "weighted Jacobi coefficient")
    destination = ROOT / "predictions"
    destination.mkdir(exist_ok=False)
    systems, eigen_reports = {}, []
    for maximum in LEVELS:
        moments = np.arange(3, maximum)
        offdiagonal = (moments + 1) / np.sqrt((2 * moments + 1) * (2 * moments + 3))
        eigenvalues, vectors = eigh_tridiagonal(np.zeros(maximum - 2), offdiagonal, lapack_driver="stev")
        matrix = np.diag(offdiagonal, 1) + np.diag(offdiagonal, -1)
        residual = float(np.max(abs(matrix @ vectors - vectors * eigenvalues)))
        orthogonality = float(np.max(abs(vectors.T @ vectors - np.eye(maximum - 2))))
        weights = vectors[0] ** 2
        require(max(residual, orthogonality, abs(np.sum(weights) - 1)) < ALGEBRA and np.max(abs(eigenvalues)) <= 1 + ALGEBRA, "spectral representation")
        systems[maximum] = (eigenvalues, weights)
        path = destination / ("jacobi-" + str(maximum) + ".npz")
        np.savez_compressed(path, offdiagonal=offdiagonal, eigenvalues=eigenvalues, weights=weights, vectors=vectors)
        eigen_reports.append(dict(maximum=maximum, dimension=maximum - 2, residual=residual, orthogonality=orthogonality, weight_sum=float(np.sum(weights)), spectral_radius=float(np.max(abs(eigenvalues))), file=path.name, sha256=digest(path)))
    predictions = []
    for model in ("heavy", "cold"):
        reference, groups, packets, velocity, forcing = source_curves(model)
        antiderivative = velocity.antiderivative()
        original = HIERARCHY / "runs-balanced" / model / "native-reference.npz"
        for fraction in (0., .25, .5):
            guard()
            saved = PRIOR / "results" / model / ("impulse-" + str(int(100 * fraction)) + ".npz")
            original_impulse = load(saved)
            times = original_impulse["times"]
            release = float(times[0])
            distances = WAVE * (antiderivative(times) - antiderivative(release))
            speeds, initial_speed = velocity(times), velocity(release)
            kernels, shapes, bounds = [], [], []
            for maximum in LEVELS:
                eigenvalues, weights = systems[maximum]
                response = np.column_stack([np.cos(np.outer(distances[:, index], eigenvalues)) @ weights for index in range(5)])
                predicted = -9 * WAVE ** 2 / 35 * speeds * initial_speed * response
                kernels.append(predicted)
                shapes.append(response)
                bounds.append([first_return_bound(maximum, float(np.max(distances[:, index]))) for index in range(5)])
            require(np.max(bounds[-1]) < GATE, "untruncated port truncation bound")
            target = destination / (model + "-" + str(int(100 * fraction)) + ".npz")
            np.savez_compressed(target, times=times, release=release, levels=np.array(LEVELS), distance=distances, speed=speeds, initial_speed=initial_speed, response=np.array(shapes), kernels=np.array(kernels), analytic_shape_error=np.array(bounds), groups=np.array([group["name"] for group in groups]))
            prediction = dict(model=model, release_fraction=fraction, source_impulse_sha256=digest(saved), native_reference_sha256=digest(original), file=target.name, sha256=digest(target), maximum_distance=float(np.max(distances)), uniform_analytic_shape_bounds=np.max(bounds, axis=1).tolist(), finest_refinement=float(np.max(abs(shapes[-1] - shapes[-2]))))
            predictions.append(prediction)
            print(prediction, flush=True)
    write(ROOT / "frozen-predictions.json", dict(state="frozen_before_higher_order_controls", created_utc=datetime.now(timezone.utc).isoformat(), source_sha256=digest(__file__), protocol_sha256=digest(ROOT / "PROTOCOL.md"), prior_closeout_sha256=digest(PRIOR / "closeout.json"), symbolic=str(identity), levels=LEVELS, eigen_reports=eigen_reports, predictions=predictions, infinite_hierarchy_derivation=True, floating_point_not_interval_certified=True, no_new_fit=True))


if __name__ == "__main__":
    main()
