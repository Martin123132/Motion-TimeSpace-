import time
from common import ROOT, PRIOR, HIERARCHY, WAVE, GATE, modest, guard, check_prior, require, read, write, digest, load, source_curves
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicHermiteSpline


def errors(left, right):
    return np.max(abs(left - right), axis=0) / np.maximum(np.max(abs(right), axis=0), 1e-80)


def main():
    modest()
    check_prior()
    frozen = read(ROOT / "frozen-predictions.json")
    spectrum_owner = next(row for row in frozen["eigen_reports"] if row["maximum"] == 192)
    spectrum_path = ROOT / "predictions" / spectrum_owner["file"]
    require(digest(spectrum_path) == spectrum_owner["sha256"], "frozen spectrum")
    spectrum = load(spectrum_path)
    eigenvalues, weights = spectrum["eigenvalues"], spectrum["weights"]
    destination = ROOT / "spectral-forcing"
    destination.mkdir(exist_ok=False)
    reports = []
    for model in ("heavy", "cold"):
        reference, groups, packets, velocity, full_forcing = source_curves(model)
        full_times = reference["times"]
        times = full_times[reference["probes"]]
        scale = np.maximum(np.max(abs(full_forcing(full_times)), axis=0), 1e-80)
        low = [int(np.flatnonzero(reference["mapping"] == group["low_native"])[0]) for group in groups]
        saved_control = load(ROOT / (model + "-forced-correction.npz"))
        results, runs = {}, []
        for tag, tolerance, stride in (("base", 2e-11, 1), ("fine", 2e-12, 1), ("coarse-source", 2e-12, 2)):
            guard()
            keep = np.unique(np.r_[np.arange(0, len(full_times), stride), len(full_times) - 1])
            forcing = CubicHermiteSpline(full_times[keep], reference["state"][keep][:, low], reference["derivative"][keep][:, low], axis=0)
            last_guard = time.monotonic()
            def rhs(stamp, flattened):
                nonlocal last_guard
                if time.monotonic() - last_guard > 2:
                    guard()
                    last_guard = time.monotonic()
                coefficients = flattened.reshape(len(eigenvalues), 5)
                speed = velocity(stamp)
                return (-1j * WAVE * eigenvalues[:, None] * speed * coefficients + speed * forcing(stamp) / scale).ravel()
            started = time.monotonic()
            solution = solve_ivp(rhs, (float(times[0]), float(times[-1])), np.zeros(len(eigenvalues) * 5, dtype=complex), method="DOP853", rtol=tolerance, atol=tolerance / 100, t_eval=times)
            require(solution.success, "spectral source solve")
            coefficients = solution.y.T.reshape(len(times), len(eigenvalues), 5)
            complex_octupole = 3 * WAVE / 7 * np.einsum("j,tjq->tq", weights, coefficients) * scale
            octupole = complex_octupole.real
            returned = -3 * WAVE / 5 * velocity(times) * octupole
            imaginary = float(np.max(abs(complex_octupole.imag)) / max(float(np.max(abs(octupole))), 1e-80))
            path = destination / (model + "-" + tag + ".npz")
            np.savez_compressed(path, times=times, octupole=octupole, returned=returned, residual_imaginary=complex_octupole.imag, normalization=scale)
            results[tag] = returned
            record = dict(tag=tag, rtol=tolerance, stride=stride, success=solution.success, evaluations=solution.nfev, seconds=time.monotonic() - started, imaginary_relative=imaginary, file=path.name, sha256=digest(path))
            runs.append(record)
            print(model, tag, record["seconds"], flush=True)
        refinement = errors(results["base"], results["fine"])
        independent = errors(saved_control["corrected_return"], results["fine"])
        source_change = errors(results["coarse-source"], results["fine"])
        report = dict(model=model, runs=runs, precision=refinement.tolist(), independent_native_L128=independent.tolist(), source_stride=source_change.tolist(), original_comparison_sha256=digest(ROOT / "closure-comparison-result.json"), passed=bool(max(np.max(refinement), np.max(independent), np.max(source_change), max(row["imaginary_relative"] for row in runs)) < GATE))
        reports.append(report)
        print(report, flush=True)
    write(ROOT / "spectral-forcing-result.json", dict(passed=all(row["passed"] for row in reports), reports=reports, source_sha256=digest(__file__), frozen_spectrum_sha256=digest(spectrum_path), decision_sha256=digest(ROOT / "SPECTRAL-FORCING-EXTENSION.md"), source_histories_fixed=True, coupled_corrected_solution_claimed=False))
    require(all(row["passed"] for row in reports), "independent spectral forcing failed; preserve and inspect")


if __name__ == "__main__":
    main()
