import time
from datetime import datetime, timezone
from common import ROOT, PRIOR, HIERARCHY, WAVE, modest, guard, check_prior, require, read, write, digest, load, source_curves
import numpy as np
from scipy.integrate import solve_ivp


def main():
    modest()
    check_prior()
    frozen = read(ROOT / "frozen-predictions.json")
    require(frozen["state"] == "frozen_before_higher_order_controls" and frozen["source_sha256"] == digest(ROOT / "freeze_free_streaming.py"), "frozen prediction source")
    for row in frozen["predictions"]:
        require(digest(ROOT / "predictions" / row["file"]) == row["sha256"], "frozen prediction")
    destination = ROOT / "controls"
    destination.mkdir(exist_ok=False)
    write(ROOT / "control-config.json", dict(created_utc=datetime.now(timezone.utc).isoformat(), source_sha256=digest(__file__), frozen_result_sha256=digest(ROOT / "frozen-predictions.json"), protocol_sha256=digest(ROOT / "PROTOCOL.md"), impulse_levels=[32, 64], forced_levels=[16, 32, 64, 128], tolerances=[2e-11, 2e-12], amplitudes="unit impulse or original saved quadrupole source", no_initial_state_refit=True))
    reports, failure = [], None
    try:
        for model in ("heavy", "cold"):
            reference, groups, packets, velocity, forcing = source_curves(model)
            full_times = reference["times"]
            scale = np.maximum(np.max(abs(forcing(full_times)), axis=0), 1e-80)
            jobs = []
            for fraction in (0., .25, .5):
                prediction = load(ROOT / "predictions" / (model + "-" + str(int(100 * fraction)) + ".npz"))
                for maximum in (32, 64):
                    jobs.append(("impulse", fraction, maximum, prediction["times"]))
            for maximum in (16, 32, 64, 128):
                jobs.append(("forced", 0., maximum, full_times[reference["probes"]]))
            for kind, fraction, maximum, times in jobs:
                moments = np.arange(3, maximum + 1)
                lower = WAVE * moments / (2 * moments + 1)
                lower[-1] = WAVE
                upper = -WAVE * (moments + 1) / (2 * moments + 1)
                weights = (2 * moments + 1).astype(float)
                weights[-1] = maximum
                initial = np.zeros((len(moments), 5))
                normalization = scale if kind == "forced" else np.ones(5)
                if kind == "impulse":
                    initial[0] = 1.
                else:
                    require(all(np.count_nonzero(reference["state"][0, packet["indices"]]) == 0 for packet in packets), "forced tail preparation must be zero")
                last_guard = time.monotonic()
                def rhs(stamp, flattened):
                    nonlocal last_guard
                    if time.monotonic() - last_guard > 2:
                        guard()
                        last_guard = time.monotonic()
                    state = flattened.reshape(len(moments), 5)
                    speed = velocity(stamp)
                    derivative = np.zeros_like(state)
                    derivative[1:] += lower[1:, None] * state[:-1]
                    derivative[:-1] += upper[:-1, None] * state[1:]
                    derivative *= speed
                    derivative[-1] -= (maximum + 1) / stamp * state[-1]
                    if kind == "forced":
                        derivative[0] += 3 * WAVE / 7 * speed * forcing(stamp) / normalization
                    return derivative.ravel()
                for tolerance in (2e-11, 2e-12):
                    guard()
                    started = time.monotonic()
                    solution = solve_ivp(rhs, (float(times[0]), float(times[-1])), initial.ravel(), method="DOP853", rtol=tolerance, atol=tolerance / 100, t_eval=times)
                    require(solution.success and np.isfinite(solution.y).all(), "closure control solver")
                    states = solution.y.T.reshape(-1, len(moments), 5) * normalization
                    port = -3 * WAVE / 5 * velocity(times) * states[:, 0]
                    if kind == "impulse":
                        port *= 3 * WAVE / 7 * velocity(times[0])
                    tag = f"{model}-{kind}-{int(100 * fraction)}-L{maximum}-" + ("fine" if tolerance < 1e-11 else "base")
                    path = destination / (tag + ".npz")
                    np.savez_compressed(path, times=times, octupole=states[:, 0], returned=port, norm=np.sqrt(np.sum(weights[None, :, None] * states ** 2, axis=1)), terminal=states[:, -1], weights=weights, groups=np.array([group["name"] for group in groups]), normalization=normalization)
                    report = dict(model=model, kind=kind, release_fraction=fraction, maximum=maximum, rtol=tolerance, evaluations=solution.nfev, seconds=time.monotonic() - started, file=path.name, sha256=digest(path), success=solution.success)
                    reports.append(report)
                    write(destination / (tag + ".json"), report)
                    print(model, kind, fraction, maximum, tolerance, report["seconds"], flush=True)
    except BaseException as error:
        failure = repr(error)
        raise
    finally:
        write(ROOT / "control-result.json", dict(state="complete" if failure is None and len(reports) == 40 else "failed", error=failure, reports=reports, source_sha256=digest(__file__), config_sha256=digest(ROOT / "control-config.json"), frozen_result_sha256=digest(ROOT / "frozen-predictions.json"), parent_histories_reused=True, parent_history_changed=False))


if __name__ == "__main__":
    main()
