import os

from common import ROOT, modest, guard, require, read, write, digest
from probe_analysis import packet, fields
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline


def replay(model, data, values, variable_names, offset, stride, tolerance, metric_on):
    window = slice(offset, offset + 129)
    times = data["times"][window]
    response = values[window]
    observers = data["observer"][window]
    observer_names = data["observer_names"].tolist()
    knots = np.arange(0, 129, stride)
    hubble = CubicSpline(times[knots], observers[knots, observer_names.index("H_native")])
    scale = CubicSpline(times[knots], observers[knots, observer_names.index("a_native")])
    phi = CubicSpline(times[knots], response[knots, variable_names.index("Phi")])
    psi = CubicSpline(times[knots], response[knots, variable_names.index("Psi")])
    field, speed, mass = fields(model)
    wave = float(data["k"])
    names = ["u", "p", "d_c", "theta_c"] if model == "heavy" else ["d_c", "theta_c"]
    native = response[:, [variable_names.index(name) for name in names]]
    normalization = np.maximum(np.max(abs(native), axis=0), 1e-30)

    def rhs(time, scaled):
        guard()
        state = scaled * normalization
        aa, hh = float(scale(time)), float(hubble(time))
        ph, ps = (float(phi(time)), float(psi(time))) if metric_on else (0., 0.)
        if model == "heavy":
            background, velocity = float(field(np.log(aa))), float(speed(np.log(aa)))
            derivative = np.array([state[1] + velocity * (ps + 3 * ph),
                -2 * hh * state[1] - (wave**2 + (aa * mass)**2) * state[0] + (aa * mass)**2 * background * (3 * ph - ps),
                -state[3], -hh * state[3] + wave**2 * ps])
        else:
            derivative = np.array([-state[1], -hh * state[1] + wave**2 * ps])
        return derivative / normalization

    probes = np.array([32, 64, 96, 128])
    solution = solve_ivp(rhs, (times[0], times[-1]), native[0] / normalization,
        method="DOP853", rtol=tolerance, atol=tolerance / 100, t_eval=times[probes])
    require(solution.success, "physical response replay failed")
    prediction = solution.y.T * normalization
    discrepancy = np.max(abs(prediction - native[probes]), axis=0) / normalization
    return dict(names=names, prediction=prediction, expected=native[probes], normalization=normalization,
        errors=discrepancy, evaluations=solution.nfev, duration=float(times[-1] - times[0]),
        stride=stride, tolerance=tolerance, metric_on=metric_on)


def main():
    modest()
    checked = read(ROOT / "probe-check-result.json")
    require(digest(ROOT / "probe_analysis.py") == checked["analysis_source_sha256"], "changed analysis")
    folder = ROOT / "replay"
    folder.mkdir(exist_ok=False)
    reports = []
    for row in checked["reports"]:
        require(digest(ROOT / row["response_file"]) == row["response_sha256"], "changed response")
        model, index = row["model"], row["index"]
        source_core = ("u", "p", "d_c", "theta_c", "Phi", "Psi") if model == "heavy" else ("d_c", "theta_c", "Phi", "Psi")
        require(all(item["passed"] for item in row["checks"] if item["variable"] in source_core), "unresolved replay inputs")
        data = packet(model, index, "zero")
        with np.load(ROOT / row["response_file"]) as saved:
            values, names = saved["values"], saved["names"].tolist()
        for window in range(3):
            tests = [replay(model, data, values, names, window * 129, stride, tol, True)
                for stride, tol in ((1, 2e-11), (2, 2e-11), (4, 2e-11), (1, 2e-12))]
            frozen = replay(model, data, values, names, window * 129, 1, 2e-12, False)
            best = tests[0]
            refinements = [float(np.max(abs(test["prediction"] - best["prediction"]) / best["normalization"])) for test in tests[1:]]
            max_error = max(float(np.max(test["errors"])) for test in tests)
            feedback = np.max(abs(frozen["prediction"] - best["prediction"]), axis=0) / best["normalization"]
            filename = f"{model}-{index}-window{window}.npz"
            np.savez_compressed(folder / filename, names=np.array(best["names"]), expected=best["expected"],
                prediction=best["prediction"], frozen=frozen["prediction"], normalization=best["normalization"],
                errors=best["errors"], feedback=feedback, refinements=np.array(refinements))
            report = dict(model=model, k=row["k"], window=window, duration_Mpc=best["duration"],
                source_all_species_passed=row["passed"], replay_core_inputs_passed=True,
                state_names=best["names"], state_errors=best["errors"].tolist(), maximum_error=max_error,
                measured_refinements=refinements, frozen_discrepancy=frozen["errors"].tolist(),
                local_feedback_change=feedback.tolist(), passed=bool(max(max_error, max(refinements)) < 2e-5),
                file=filename, sha256=digest(folder / filename), rhs_evaluations=sum(test["evaluations"] for test in tests) + frozen["evaluations"])
            reports.append(report)
            write(folder / (filename + ".json"), report)
            print(model, row["k"], window, "error", max_error, "feedback", feedback.tolist(), flush=True)
    output = dict(passed=all(row["passed"] for row in reports), all_species_source_passed=checked["passed"],
        pid=os.getpid(), reports=reports, input_sha256=digest(ROOT / "probe-check-result.json"),
        source_sha256=digest(__file__), gate=2e-5,
        scope="Local physical response replay and fixed-metric counterfactual in three separately anchored windows. Paired native evolution carries the response across intervening gaps; these replays do not interpolate across those gaps.")
    write(ROOT / "replay-result.json", output)
    print(dict(passed=output["passed"], source_all_species_passed=output["all_species_source_passed"],
        maximum_error=max(row["maximum_error"] for row in reports), failed=[(row["model"], row["k"], row["window"]) for row in reports if not row["passed"]]), flush=True)
    require(output["passed"], "replay tolerance failed; preserve and inspect")


if __name__ == "__main__":
    main()
