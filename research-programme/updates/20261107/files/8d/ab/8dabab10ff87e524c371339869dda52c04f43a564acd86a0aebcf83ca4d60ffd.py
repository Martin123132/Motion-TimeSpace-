import csv
from common import ROOT, PRIOR, HIERARCHY, WAVE, GATE, ALGEBRA, modest, guard, check_prior, require, read, write, digest, load, source_curves
import numpy as np


def component_error(prediction, target):
    return np.max(abs(prediction - target), axis=0) / np.maximum(np.max(abs(target), axis=0), 1e-80)


def main():
    modest()
    check_prior()
    frozen, controls = read(ROOT / "frozen-predictions.json"), read(ROOT / "control-result.json")
    require(controls["state"] == "complete" and len(controls["reports"]) == 40, "complete controls")
    require(controls["frozen_result_sha256"] == digest(ROOT / "frozen-predictions.json"), "frozen controls link")
    require(controls["source_sha256"] == digest(ROOT / "run_closure_controls.py"), "controls source")
    for row in controls["reports"]:
        require(digest(ROOT / "controls" / row["file"]) == row["sha256"], "control file ownership")
    packets = {}
    for row in controls["reports"]:
        packets[row["model"], row["kind"], row["release_fraction"], row["maximum"], row["rtol"]] = load(ROOT / "controls" / row["file"])
    reports, rows = [], []
    for model in ("heavy", "cold"):
        guard()
        reference, groups, old_packets, velocity, forcing = source_curves(model)
        impulse_reports, precision_reports = [], []
        for fraction in (0., .25, .5):
            frozen_row = next(row for row in frozen["predictions"] if row["model"] == model and row["release_fraction"] == fraction)
            require(digest(ROOT / "predictions" / frozen_row["file"]) == frozen_row["sha256"], "frozen prediction unchanged")
            prediction = load(ROOT / "predictions" / frozen_row["file"])
            target = prediction["kernels"][-1]
            old = load(PRIOR / "results" / model / ("impulse-" + str(int(100 * fraction)) + ".npz"))
            require(np.array_equal(old["times"], prediction["times"]), "original probe times")
            kernel_by_level = {16: old["kernels"][:, 2:]}
            for maximum in (32, 64):
                base = packets[model, "impulse", fraction, maximum, 2e-11]
                fine = packets[model, "impulse", fraction, maximum, 2e-12]
                require(np.array_equal(base["times"], prediction["times"]) and np.array_equal(fine["times"], prediction["times"]), "impulse grids")
                refinement = component_error(base["returned"], fine["returned"])
                precision_reports.append(dict(kind="impulse", release_fraction=fraction, maximum=maximum, maximum_refinement=float(np.max(refinement)), passed=bool(np.max(refinement) < GATE)))
                kernel_by_level[maximum] = fine["returned"]
            for maximum, actual in kernel_by_level.items():
                errors = component_error(actual, target)
                denominator = np.maximum(np.max(abs(target), axis=0), 1e-80)
                for index, group in enumerate(groups):
                    exceeding = np.flatnonzero(abs(actual[:, index] - target[:, index]) / denominator[index] > GATE)
                    row = dict(model=model, group=group["name"], release_fraction=fraction, maximum=maximum, error=float(errors[index]), closure_adequate=bool(errors[index] < GATE),
                               first_disagreement_time=float(prediction["times"][exceeding[0]]) if len(exceeding) else None,
                               final_retained=float(actual[-1, index]), final_untruncated=float(target[-1, index]), zero_lag=float(target[0, index]))
                    impulse_reports.append(row)
                    rows.append(row)
        original_times = reference["times"][reference["probes"]]
        old_return = np.column_stack([-3 * WAVE / 5 * packet["speed"][reference["probes"]] * reference["state"][reference["probes"], packet["indices"][0]] for packet in old_packets])
        forced_by_level = {}
        for maximum in (16, 32, 64, 128):
            base = packets[model, "forced", 0., maximum, 2e-11]
            fine = packets[model, "forced", 0., maximum, 2e-12]
            require(np.array_equal(base["times"], original_times) and np.array_equal(fine["times"], original_times), "forced grids")
            precision = component_error(base["returned"], fine["returned"])
            precision_reports.append(dict(kind="forced", maximum=maximum, maximum_refinement=float(np.max(precision)), passed=bool(np.max(precision) < GATE)))
            forced_by_level[maximum] = fine["returned"]
        replay = component_error(forced_by_level[16], old_return)
        convergence = component_error(forced_by_level[64], forced_by_level[128])
        correction = forced_by_level[128] - old_return
        difference = component_error(old_return, forced_by_level[128])
        low = [int(np.flatnonzero(reference["mapping"] == group["low_native"])[0]) for group in groups]
        original_rate = reference["derivative"][reference["probes"]][:, low]
        relative_drive = np.max(abs(correction), axis=0) / np.maximum(np.max(abs(original_rate), axis=0), 1e-80)
        path = ROOT / (model + "-forced-correction.npz")
        np.savez_compressed(path, times=original_times, original_return=old_return, replay_return=forced_by_level[16], corrected_return=forced_by_level[128], L32_return=forced_by_level[32], L64_return=forced_by_level[64], correction=correction, original_quadrupole_rate=original_rate, groups=np.array([group["name"] for group in groups]))
        report = dict(model=model, impulses=impulse_reports, precision=precision_reports, original_forcing_replay=replay.tolist(), high_order_forcing_convergence=convergence.tolist(),
                      original_forced_return_error=difference.tolist(), correction_relative_to_original_quadrupole_rate=relative_drive.tolist(),
                      source_correction_file=path.name, source_correction_sha256=digest(path), source_forcing_is_frozen=True, coupled_corrected_solution_claimed=False,
                      legacy_L16_adequate=all(row["closure_adequate"] for row in impulse_reports if row["maximum"] == 16),
                      higher_L64_adequate=all(row["closure_adequate"] for row in impulse_reports if row["maximum"] == 64))
        report["numerics_passed"] = bool(all(row["passed"] for row in precision_reports) and max(np.max(replay), np.max(convergence)) < GATE and report["higher_L64_adequate"])
        reports.append(report)
        print(dict(model=model, numerical_pass=report["numerics_passed"], legacy_L16=report["legacy_L16_adequate"], maximum_impulse_errors={maximum:max(row["error"] for row in impulse_reports if row["maximum"] == maximum) for maximum in (16,32,64)}, replay_max=float(np.max(replay)), forced_convergence=float(np.max(convergence)), forced_errors=difference.tolist(), source_drive_ratios=relative_drive.tolist()), flush=True)
    with (ROOT / "closure-comparison.csv").open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result = dict(numerics_passed=all(row["numerics_passed"] for row in reports), legacy_closure_adequate=all(row["legacy_L16_adequate"] for row in reports), reports=reports, numerical_gate=GATE, algebra_gate=ALGEBRA, source_sha256=digest(__file__), control_result_sha256=digest(ROOT / "control-result.json"), frozen_result_sha256=digest(ROOT / "frozen-predictions.json"), csv_sha256=digest(ROOT / "closure-comparison.csv"), no_parent_solution_overwrite=True)
    write(ROOT / "closure-comparison-result.json", result)
    require(result["numerics_passed"], "control accuracy failed; preserve and inspect")


if __name__ == "__main__":
    main()
