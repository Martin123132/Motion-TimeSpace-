import csv
import os
from common import ROOT, modest, require, read, write, digest
import numpy as np

GATE = 2e-5
ALGEBRA = 1e-10


def load(path):
    with np.load(path) as data:
        return {name: data[name].copy() for name in data.files}


def scales(values):
    return np.maximum(np.max(abs(values), axis=0), 1e-30)


def errors(prediction, reference):
    return np.max(abs(prediction - reference), axis=0) / scales(reference)


def physical(observer, names):
    get = lambda name: observer[:, names.index(name)]
    hubble = get("H_native")
    enthalpy = get("R") + get("Pbar")
    alpha = get("sigma") / 5.
    phi = get("eta_sync") - hubble * alpha
    return dict(Phi=phi, Psi=2 * get("Weyl") - phi, D=get("D_sync") - 3 * hubble * enthalpy * alpha, Q=get("Q_sync") + enthalpy * get("sigma"), Pi=get("Pi"), delta_b=get("delta_baryon64") - 3 * hubble * alpha, delta_gamma=get("delta_gamma64") - 4 * hubble * alpha, delta_massless=get("delta_massless64") - 4 * hubble * alpha)


def main():
    modest()
    owner = read(ROOT / "hierarchy-balanced-result.json")
    require(owner["state"] == "complete" and len(owner["reports"]) == 2, "completed hierarchy")
    require(owner["source_sha256"] == digest(ROOT / "run_hierarchy_balanced.py"), "runner source")
    reports, state_rows, kernel_rows = [], [], []
    for item in owner["reports"]:
        model = item["model"]
        folder = ROOT / "runs-balanced" / model
        reference = load(folder / "native-reference.npz")
        require(digest(folder / "native-reference.npz") == item["captured_reference_sha256"], "captured reference owner")
        packets = {}
        for case in item["cases"]:
            require(digest(folder / case["file"]) == case["sha256"], "prediction owner")
            packets[case["tag"]] = load(folder / case["file"])
        full, fine = packets["full"], packets["precision"]
        state_error = errors(full["state"], reference["state"])
        refinement = errors(full["state"], fine["state"])
        negative = errors(-packets["negative"]["state"], full["state"])
        names, probes = reference["observer_names"].tolist(), reference["probes"]
        expected_observer = reference["observer"][probes]
        background = {"R", "Pbar", "R_cdm", "R_baryon", "R_gamma", "R_massless", "R_massive", "R_scalar", "a_native", "H_native", "tau_native"}
        columns = [index for index, name in enumerate(names) if name not in background]
        source_errors = errors(full["observer"][:, columns], expected_observer[:, columns])
        source_refinement = errors(full["observer"][:, columns], fine["observer"][:, columns])
        zero = np.count_nonzero(packets["zero"]["state"]) == 0 and np.count_nonzero(packets["zero"]["observer"][:, columns]) == 0
        physical_reference = physical(expected_observer, names)
        physical_prediction = physical(full["observer"], names)
        physical_errors = {name: float(errors(physical_prediction[name], physical_reference[name])) for name in physical_reference}
        algebra = {}
        physical_data = physical_prediction
        get = lambda name: full["observer"][:, names.index(name)]
        for name, terms in dict(Hamiltonian=[50 * physical_data["Phi"], physical_data["D"], 3 * get("H_native") * physical_data["Q"] / 5.], slip=[physical_data["Phi"], -physical_data["Psi"], -physical_data["Pi"] / 25.]).items():
            array = np.array(terms)
            algebra[name] = float(np.max(abs(array.sum(axis=0))) / max(float(np.max(abs(array))), 1e-30))
        audit = load(folder / "operator-audit.npz")
        selected, remaining = reference["selected"], reference["remaining"]
        kernels = []
        for release_fraction in (0., .25, .5):
            base_item = next(row for row in item["kernels"] if row["release_fraction"] == release_fraction and row["rtol"] == 2e-11)
            fine_item = next(row for row in item["kernels"] if row["release_fraction"] == release_fraction and row["rtol"] == 2e-12)
            for candidate in (base_item, fine_item):
                require(digest(folder / candidate["file"]) == candidate["sha256"], "kernel owner")
            base = load(folder / base_item["file"])
            refined = load(folder / fine_item["file"])
            require(np.array_equal(base["times"], refined["times"]) and np.all(base["times"] >= base["release"]), "retarded times")
            matrix_index = int(round(release_fraction * 8))
            operator = audit["matrices"][matrix_index]
            instantaneous = operator[np.ix_(selected, remaining)] @ operator[np.ix_(remaining, selected)]
            exact_zero_lag = float(np.max(abs(base["kernel"][0] - instantaneous)) / max(float(np.max(abs(instantaneous))), 1e-30))
            difference = np.max(abs(base["kernel"] - refined["kernel"]), axis=0) / np.maximum(np.max(abs(refined["kernel"]), axis=0), 1e-30)
            kernel = dict(release_fraction=release_fraction, release=float(base["release"]), maximum_refinement=float(np.max(difference)), component_refinements=difference.tolist(), zero_lag_identity=exact_zero_lag, max_absolute_kernel=np.max(abs(refined["kernel"]), axis=0).tolist(), final_kernel=refined["kernel"][-1].tolist(), nonzero=bool(np.any(refined["kernel"] != 0)), samples=len(base["times"]), passed=bool(np.max(difference) < GATE and exact_zero_lag < ALGEBRA))
            kernels.append(kernel)
            for index, stamp in enumerate(refined["times"]):
                for row, selected_row in enumerate(selected):
                    for column, selected_column in enumerate(selected):
                        kernel_rows.append(dict(model=model, release_fraction=release_fraction, release=float(base["release"]), time=float(stamp), row_native=int(reference["mapping"][selected_row]), column_native=int(reference["mapping"][selected_column]), kernel=float(refined["kernel"][index, row, column])))
        old_unit_difference = None
        if model == "heavy":
            old = load(ROOT / "runs-startstep/heavy/full.npz")
            old_unit_difference = float(np.max(errors(old["state"], full["state"])))
        for index, native_index in enumerate(reference["mapping"]):
            state_rows.append(dict(model=model, native_index=int(native_index), selected=bool(index in selected), max_reference=float(scales(reference["state"])[index]), state_error=float(state_error[index]), refinement=float(refinement[index]), negative_error=float(negative[index])))
        tests = [float(np.max(state_error)), float(np.max(refinement)), float(np.max(negative)), float(np.max(source_errors)), float(np.max(source_refinement)), *physical_errors.values()]
        if old_unit_difference is not None:
            tests.append(old_unit_difference)
        passed = max(tests) < GATE and max(algebra.values()) < ALGEBRA and zero and all(row["passed"] for row in kernels)
        report = dict(model=model, passed=bool(passed), dimension=item["dimension"], full_state_error=float(np.max(state_error)), maximum_state_refinement=float(np.max(refinement)), negative_error=float(np.max(negative)), zero_exact=bool(zero), maximum_observer_error=float(np.max(source_errors)), observer_errors=dict(zip([names[index] for index in columns], source_errors.tolist())), maximum_observer_refinement=float(np.max(source_refinement)), physical_errors=physical_errors, algebra=algebra, prior_unit_prediction_difference=old_unit_difference, native_adapter_overlap=item["adapter_overlap"], operator_observer_error=item["operator_observer_error"], operator_derivative_error=item["operator_derivative_error"], operator_linearity=item["maximum_linearity_error"], preparation_remaining_zero=item["remaining_initial_zero"], kernels=kernels, future_metric_or_species_histories_supplied=False, imported_approximations_explicit=True)
        reports.append(report)
        print(report, flush=True)
    for filename, rows in (("state-comparison.csv", state_rows), ("retarded-kernel.csv", kernel_rows)):
        with (ROOT / filename).open("x", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    result = dict(passed=all(row["passed"] for row in reports), pid=os.getpid(), reports=reports, gate=GATE, algebra_gate=ALGEBRA, runner_result_sha256=digest(ROOT / "hierarchy-balanced-result.json"), source_sha256=digest(__file__), state_csv_sha256=digest(ROOT / "state-comparison.csv"), kernel_csv_sha256=digest(ROOT / "retarded-kernel.csv"), scope="independent integration of retained native RHS and explicit retarded columns; not an independent discretized Volterra solution or an exact untruncated Boltzmann hierarchy")
    write(ROOT / "comparison-result.json", result)
    require(result["passed"], "frozen hierarchy/kernel gates failed; preserve and diagnose")


if __name__ == "__main__":
    main()

