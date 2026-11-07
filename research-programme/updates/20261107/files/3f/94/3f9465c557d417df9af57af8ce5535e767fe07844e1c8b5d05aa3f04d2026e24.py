import os

from common import ROOT, modest, guard, require, read, write, digest
from probe_analysis import packet, physical, fields
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline


def integrate(model, data, target, stride, tolerance, metric_on):
    times, names = data["times"], data["observer_names"].tolist()
    knots = np.unique(np.append(np.arange(0, len(times), stride), len(times) - 1))
    observers = data["observer"]
    scale = CubicSpline(times[knots], observers[knots, names.index("a_native")])
    hubble = CubicSpline(times[knots], observers[knots, names.index("H_native")])
    phi = CubicSpline(times[knots], target["Phi"][knots])
    psi = CubicSpline(times[knots], target["Psi"][knots])
    field, velocity, mass = fields(model)
    wave = float(data["k"])
    state_names = ["u", "p", "d_c", "theta_c"] if model == "heavy" else ["d_c", "theta_c"]
    reference = np.column_stack([target[name] for name in state_names])
    normalization = np.maximum(np.max(abs(reference), axis=0), 1e-30)
    probes = data["probe_indices"]

    def rhs(time, normalized):
        guard()
        state = normalized * normalization
        aa, hh = float(scale(time)), float(hubble(time))
        ph, ps = (float(phi(time)), float(psi(time))) if metric_on else (0., 0.)
        if model == "heavy":
            background, speed = float(field(np.log(aa))), float(velocity(np.log(aa)))
            derivative = np.array([state[1] + speed * (ps + 3 * ph),
                -2 * hh * state[1] - (wave**2 + (aa * mass)**2) * state[0] + (aa * mass)**2 * background * (3 * ph - ps),
                -state[3], -hh * state[3] + wave**2 * ps])
        else:
            derivative = np.array([-state[1], -hh * state[1] + wave**2 * ps])
        return derivative / normalization

    solution = solve_ivp(rhs, (times[0], times[-1]), reference[0] / normalization,
        method="DOP853", rtol=tolerance, atol=tolerance / 100, t_eval=times[probes])
    require(solution.success, "continuous response integration failed")
    predicted = solution.y.T * normalization
    errors = np.max(abs(predicted - reference[probes]), axis=0) / normalization
    return dict(predicted=predicted, expected=reference[probes], normalization=normalization,
        errors=errors, state_names=state_names, evaluations=solution.nfev,
        stride=stride, tolerance=tolerance, metric_on=metric_on)


def main():
    modest()
    result = read(ROOT / "tangent-check-result.json")
    require(result["passed"], "direct response not accepted")
    native = read(ROOT / "tangent-native-result.json")
    folder = ROOT / "continuous-replay"
    folder.mkdir(exist_ok=False)
    reports = []
    for model in ("heavy", "cold"):
        owner = next(row for row in native["reports"] if row["model"] == model and row["tag"] == "one")
        require(digest(ROOT / "packets" / owner["file"]) == owner["sha256"], "changed direct history")
        saved = packet(model, 3, "one")
        start, end = int(saved["original_indices"][0]), int(saved["original_indices"][-1])
        selected = np.array([saved["original_indices"][offset + point] - start for offset in (0, 129, 258) for point in (32, 64, 96, 128)])
        data = dict(standard=saved["full_standard"][start:end + 1], observer=saved["full_observer"][start:end + 1],
            times=saved["full_times"][start:end + 1], names=saved["names"], observer_names=saved["observer_names"],
            k=saved["k"], probe_indices=selected)
        require(np.all(np.diff(data["times"]) > 0), "nonmonotone source times")
        target = physical(data, model)
        tests = [integrate(model, data, target, stride, tolerance, True)
            for stride, tolerance in ((1, 2e-11), (2, 2e-11), (4, 2e-11), (1, 2e-12))]
        frozen = integrate(model, data, target, 1, 2e-12, False)
        best = tests[0]
        refinements = [float(np.max(abs(test["predicted"] - best["predicted"]) / best["normalization"])) for test in tests[1:]]
        maximum = max(float(np.max(test["errors"])) for test in tests)
        feedback = np.max(abs(frozen["predicted"] - best["predicted"]), axis=0) / best["normalization"]
        observer_names = data["observer_names"].tolist()
        scale = data["observer"][:, observer_names.index("a_native")]
        mass = fields(model)[2]
        spacing = np.diff(data["times"]) * np.sqrt(25 + (scale[:-1] * mass)**2)
        filename = model + ".npz"
        np.savez_compressed(folder / filename, predicted=np.array([test["predicted"] for test in tests]),
            errors=np.array([test["errors"] for test in tests]), expected=best["expected"], normalization=best["normalization"],
            frozen=frozen["predicted"], state_names=np.array(best["state_names"]), times=data["times"][selected],
            initial_time=data["times"][0], final_time=data["times"][-1])
        report = dict(model=model, passed=bool(max(maximum, max(refinements)) < 2e-5),
            source_snapshots=len(data["times"]), duration_Mpc=float(data["times"][-1] - data["times"][0]),
            max_source_phase_spacing=float(np.max(spacing)), state_names=best["state_names"],
            maximum_error=maximum, best_errors=best["errors"].tolist(), refinements=refinements,
            frozen_discrepancy=frozen["errors"].tolist(), feedback_change=feedback.tolist(),
            file=filename, sha256=digest(folder / filename),
            evaluations=sum(test["evaluations"] for test in tests) + frozen["evaluations"])
        reports.append(report)
        write(folder / (model + ".json"), report)
        print(report, flush=True)
    output = dict(passed=all(row["passed"] for row in reports), pid=os.getpid(), reports=reports,
        source_sha256=digest(__file__), tangent_result_sha256=digest(ROOT / "tangent-check-result.json"),
        gate=2e-5, metric_supplied=True, independently_anchored_windows=False)
    write(ROOT / "continuous-replay-result.json", output)
    require(output["passed"], "continuous replay gate failed; preserve and inspect")


if __name__ == "__main__":
    main()
