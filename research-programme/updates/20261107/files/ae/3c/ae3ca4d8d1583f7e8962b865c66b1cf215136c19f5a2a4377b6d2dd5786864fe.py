import csv
import os

from common import ROOT, modest, require, read, write, digest
from probe_analysis import physical
import numpy as np
import sympy as sp
from scipy.interpolate import CubicSpline


def main():
    modest()
    folder = ROOT / "phase-resolved"
    require(read(folder / "continuous-replay-result.json")["passed"], "continuous source not accepted")
    wave_symbol, density_symbol, hubble_symbol, momentum_symbol, shear_symbol = sp.symbols("k D H Q Pi", nonzero=True)
    full_symbol = -(density_symbol + 3 * hubble_symbol * momentum_symbol / wave_symbol) / (2 * wave_symbol**2) - shear_symbol / wave_symbol**2
    require(sp.simplify(full_symbol + density_symbol / (2 * wave_symbol**2) + 3 * hubble_symbol * momentum_symbol / (2 * wave_symbol**3) + shear_symbol / wave_symbol**2) == 0, "Newton split")
    native = read(folder / "tangent-native-result.json")
    reports, rows = [], []
    for model in ("heavy", "cold"):
        owner = next(row for row in native["reports"] if row["model"] == model and row["tag"] == "one")
        path = folder / "packets" / owner["file"]
        require(digest(path) == owner["sha256"], "changed direct source")
        with np.load(path) as saved:
            start, end = int(saved["original_indices"][0]), int(saved["original_indices"][-1])
            probes = np.array([saved["original_indices"][offset + point] - start for offset in (0, 129, 258) for point in (32, 64, 96, 128)])
            data = dict(standard=saved["full_standard"][start:end + 1], observer=saved["full_observer"][start:end + 1],
                times=saved["full_times"][start:end + 1], names=saved["names"], observer_names=saved["observer_names"], k=saved["k"])
        state = physical(data, model)
        names, times = data["observer_names"].tolist(), data["times"]
        value = lambda name: data["observer"][:, names.index(name)]
        scale, hubble, wave = value("a_native"), value("H_native"), float(data["k"])
        enthalpy = value("R") + value("Pbar")
        density = value("D_sync") - 3 * hubble * enthalpy * value("sigma") / wave
        poisson = -density / (2 * wave**2)
        momentum_correction = -3 * hubble * state["Q"] / (2 * wave**3)
        shear_correction = -state["Pi"] / wave**2
        potential_scale = max(float(np.max(abs(state["Psi"]))), 1e-30)
        split_error = float(np.max(abs(state["Psi"] - poisson - momentum_correction - shear_correction)) / potential_scale)
        predictions = []
        for stride in (1, 2, 4):
            knots = np.unique(np.append(np.arange(0, len(times), stride), len(times) - 1))
            integral = CubicSpline(times[knots], scale[knots] * state["Psi"][knots]).antiderivative()
            predictions.append((scale[0] * state["theta_c"][0] + wave**2 * (integral(times[probes]) - integral(times[0]))) / scale[probes])
        poisson_integral = CubicSpline(times, scale * poisson).antiderivative()
        poisson_prediction = (scale[0] * state["theta_c"][0] + wave**2 * (poisson_integral(times[probes]) - poisson_integral(times[0]))) / scale[probes]
        correction = CubicSpline(times, scale * (state["Psi"] - poisson))
        widths = np.diff(times)
        interval_budget = sum(abs(correction.c[index]) * widths**(4 - index) / (4 - index) for index in range(4))
        accumulated_budget = wave**2 * np.concatenate([[0.], np.cumsum(interval_budget)]) / scale
        velocity_scale = max(float(np.max(abs(state["theta_c"]))), 1e-30)
        replay_error = float(np.max(abs(predictions[0] - state["theta_c"][probes])) / velocity_scale)
        refinement = max(float(np.max(abs(candidate - predictions[0])) / velocity_scale) for candidate in predictions[1:])
        signed_change = predictions[0] - poisson_prediction
        bound_residual = float(np.max((abs(signed_change) - accumulated_budget[probes]) / velocity_scale))
        require(split_error < 1e-10 and max(replay_error, refinement) < 2e-5 and bound_residual < 1e-10, "Newton reconstruction or interpolant-bound check failed")
        report = dict(model=model, split_error=split_error, velocity_replay_error=replay_error, source_refinement=refinement,
            force_error=float(np.max(abs(state["Psi"] - poisson)) / potential_scale),
            force_triangle_budget=float((np.max(abs(momentum_correction)) + np.max(abs(shear_correction))) / potential_scale),
            velocity_poisson_difference=float(np.max(abs(signed_change)) / velocity_scale),
            velocity_interpolant_budget=float(np.max(accumulated_budget[probes]) / velocity_scale),
            bound_residual=bound_residual, source_sha256=owner["sha256"])
        reports.append(report)
        for index, point in enumerate(probes):
            rows.append(dict(model=model, time=float(times[point]), a=float(scale[point]), theta_native=float(state["theta_c"][point]),
                theta_full=float(predictions[0][index]), theta_poisson=float(poisson_prediction[index]),
                absolute_interpolant_budget=float(accumulated_budget[point])))
        print(report, flush=True)
    output = ROOT / "newton-response.csv"
    with output.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    write(ROOT / "newton-response-result.json", dict(passed=True, pid=os.getpid(), reports=reports,
        source_sha256=digest(__file__), output_sha256=digest(output),
        exact_split="Psi-Psi_P = -3 H Q/(2 k^3) - Pi/k^2",
        exact_velocity_inequality="abs(theta-theta_P) <= k^2/a integral a abs(Psi-Psi_P) dtau",
        budget_scope="Coefficientwise absolute integral bound for the chosen piecewise-cubic source interpolant; does not certify the unsampled continuum source.",
        limit_scope="Cosmological Newtonian-force approximation with Hubble drag and all-species physical density retained; no static local/PPN pass asserted."))


if __name__ == "__main__":
    main()
