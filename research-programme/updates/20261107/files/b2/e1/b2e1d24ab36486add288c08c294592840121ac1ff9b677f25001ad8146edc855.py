from analyse_stage186 import *

PRECISION = ROOT / "results/precision"


def matrix_norm(matrix):
    return mp.sqrt(mp.fsum(value * value for value in matrix))


def precise_relative(actual, expected):
    denominator = matrix_norm(expected)
    if denominator == 0:
        raise ValueError("Undefined matrix relative error")
    return float(matrix_norm(actual - expected) / denominator)


def run():
    assert read(ROOT / "progress.json")["state"] == "validation_complete"
    assert not (PRECISION / "status.json").exists()
    original_status = read(ROOT / "results/status.json")
    original_failures = original_status["failed_checks"]
    assert len(original_failures) == 1
    assert original_failures[0]["name"] == "0.0005: centered boundary algebra with saved rounding"
    paths = authenticate()
    assert paths == original_status["authenticated_inputs"]
    analytic, targets = load_packets()
    bank, basis, theta = old.setup()
    checks, matrix_rows, centered_rows, boundary_rows, gas_models = [], [], [], [], []
    with mp.workdps(80):
        anchor, tangent, curvature = [prior.mp_matrix(analytic[key]) for key in ["block", "tangent", "curvature"]]
        precise_targets = []
        for offset, packet in zip(OFFSETS, targets):
            live = prior.mp_matrix(packet["block"])
            boundary = prior.mp_matrix(packet["boundary"])
            rounded_fixed = prior.mp_matrix(packet["fixed_mask"])
            exact_fixed = live - boundary
            rounding = exact_fixed - rounded_fixed
            precise_targets.append(dict(block=live, fixed_mask=exact_fixed, boundary=boundary,
                                        rounded_fixed=rounded_fixed, rounding=rounding))
            check(checks, f"{offset}: exact saved-operand mask split", precise_relative(exact_fixed + boundary, live))
            for kind, actual in [("block", live), ("fixed_mask", exact_fixed)]:
                step = mp.mpf(offset)
                change = actual - anchor
                remainder = change - step * tangent
                quadratic = step ** 2 * curvature / 2
                error = precise_relative(quadratic, remainder)
                small_error = precise_relative(step * tangent + quadratic, change)
                check(checks, f"{offset}:{kind}: precision curvature remainder", error, .01, "curvature")
                check(checks, f"{offset}:{kind}: precision small-change prediction", small_error, .01, "prediction")
                negative = precise_relative(mp.zeros(96), remainder)
                assert negative > .01
                check(checks, f"{offset}:{kind}: zero-curvature negative control rejected", 0)
                matrix_rows.append(dict(offset=offset, kind=kind, curvature_remainder_error=error,
                                        small_change_error=small_error, passed=error <= .01))
        for index in range(0, len(OFFSETS), 2):
            step = mp.mpf(OFFSETS[index])
            plus, minus = precise_targets[index:index + 2]
            live = (plus["block"] + minus["block"] - 2 * anchor) / step ** 2
            fixed = (plus["fixed_mask"] + minus["fixed_mask"] - 2 * anchor) / step ** 2
            boundary = (plus["boundary"] + minus["boundary"]) / step ** 2
            rounded = (plus["rounded_fixed"] + minus["rounded_fixed"] - 2 * anchor) / step ** 2
            representation = (plus["rounding"] + minus["rounding"]) / step ** 2
            check(checks, f"{step}: exact curvature boundary identity", precise_relative(fixed + boundary, live))
            check(checks, f"{step}: original rounded identity plus explicit representation residual",
                  precise_relative(rounded + boundary + representation, live))
            with mp.workdps(100):
                repeated = (plus["fixed_mask"] + minus["fixed_mask"] - 2 * anchor) / step ** 2
                check(checks, f"{step}: matrix curvature 80/100 digit agreement", precise_relative(fixed, repeated))
            for kind, actual in [("block", live), ("fixed_mask", fixed)]:
                error = precise_relative(curvature, actual)
                check(checks, f"{step}:{kind}: precision centered curvature", error, .01, "curvature")
                centered_rows.append(dict(step=float(step), kind=kind, relative_error=error, passed=error <= .01))
            boundary_rows.append(dict(step=float(step), boundary_over_live=float(matrix_norm(boundary) / matrix_norm(live)),
                                      saved_rounding_over_live=float(matrix_norm(representation) / matrix_norm(live)),
                                      uncorrected_high_precision_split=float(matrix_norm(live - rounded - boundary) / matrix_norm(live))))
        for model in old.MODELS:
            state = gas_state(model, basis, bank, analytic)
            equilibrium, first, second = [state[key] for key in ["equilibrium", "first", "second"]]
            values, rows, centered = {}, [], []
            for offset, packet in zip(OFFSETS, precise_targets):
                step = mp.mpf(offset)
                for kind in ["block", "fixed_mask"]:
                    difference = packet[kind] - anchor
                    response = state["rate"] * state["dual"] * difference
                    capacity_change = -(response * state["template"])[0]
                    numerator_change = (response * state["profile"])[0]
                    actual = -(state["numerator"] + numerator_change) / (state["capacity"] + capacity_change)
                    change = actual - equilibrium
                    remainder = change - step * first
                    predicted = step ** 2 * second / 2
                    error = float(abs(predicted - remainder) / abs(remainder))
                    small_error = float(abs(step * first + predicted - change) / abs(change))
                    check(checks, f"{model}:{offset}:{kind}: precision gas curvature", error, .01, "gas_curvature")
                    check(checks, f"{model}:{offset}:{kind}: precision gas small change", small_error, .01, "gas_prediction")
                    values[(offset, kind)] = actual
                    rows.append(dict(offset=offset, kind=kind, remainder=str(remainder), predicted_remainder=str(predicted),
                                     relative_error=error, small_change_error=small_error, passed=error <= .01))
            for step in OFFSETS[::2]:
                for kind in ["block", "fixed_mask"]:
                    actual = (values[(step, kind)] + values[(-step, kind)] - 2 * equilibrium) / mp.mpf(step) ** 2
                    error = float(abs(second - actual) / abs(actual))
                    check(checks, f"{model}:{step}:{kind}: precision gas centered curvature", error, .01, "gas_curvature")
                    centered.append(dict(step=step, kind=kind, relative_error=error, passed=error <= .01))
            gas_models.append(dict(model=model, equilibrium=str(equilibrium), first=str(first), second=str(second),
                                   linear_second=str(state["linear_second"]), capacity_term=str(state["capacity_second_term"]),
                                   predictions=rows, centered=centered))
    with np.load(PARENT / "results/gas-responses.npz") as packet:
        kernels, components = packet["kernels"].copy(), list(packet["components"])
    with np.load(source.ROOT / "results/preparation/basis.npz") as packet:
        factor = linear.cholesky(packet["mass"], lower=True)
    def norm(vector):
        return float(np.linalg.norm(linear.solve_triangular(factor, vector[1:97], lower=True)))
    source_rows = []
    for component in [0, 4, 5]:
        for column in range(4):
            model = gas_models[column // 2]
            kernel = kernels[component, :, column]
            for record in model["predictions"]:
                actual = float(record["remainder"]) * kernel
                prediction = float(record["predicted_remainder"]) * kernel
                error = norm(prediction - actual) / norm(actual)
                check(checks, f"{components[component]}:{column}:{record['offset']}:{record['kind']}: repaired source curvature",
                      error, .01, "source_curvature")
                check(checks, f"{components[component]}:{column}:{record['offset']}:{record['kind']}: gas/kernel fractional agreement",
                      error - record["relative_error"])
                source_rows.append(dict(component=str(components[component]), column=column, model=model["model"],
                                        offset=record["offset"], kind=record["kind"], relative_error=error,
                                        passed=error <= .01, remainder_norm=norm(actual)))
    assert authenticate() == paths
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    assert not list(ROOT.rglob("__pycache__"))
    check(checks, "all consumed files unchanged after precision repair", 0)
    failed = [row for row in checks if not row["passed"]]
    payload = dict(stage=186, state="precision_reconciled", completed_at_utc=datetime.now(timezone.utc).isoformat(),
                   count=original_status["count"] + len(checks),
                   passed_checks=original_status["passed_checks"] + len(checks) - len(failed),
                   checks=checks, current_check_count=len(checks), current_passed=len(checks) - len(failed),
                   failed_checks=original_failures + failed, legacy_failed_checks=original_failures,
                   active_failed_checks=failed, identity_failures=[row for row in failed if row["category"] == "identity"],
                   all_checks_passed=False, all_current_precision_checks_passed=not failed,
                   matrix_predictions=matrix_rows, matrix_centered=centered_rows, boundary_rows=boundary_rows,
                   gas_models=gas_models, source_rows=source_rows,
                   authenticated_inputs=paths, original_status_sha256=saved.digest(ROOT / "results/status.json"),
                   protected_workbench_recent_modified_file_count=original_status["protected_workbench_recent_modified_file_count"],
                   protected_check_scope=original_status["protected_check_scope"],
                   precision_scope="80-digit arithmetic of saved binary operands; fixed-mask represented as live minus explicit boundary before subtraction",
                   no_new_physical_integrations=True, original_packets_changed=False, tolerances_changed=False)
    write(PRECISION / "status.json", payload)
    print(json.dumps(dict(current_checks=len(checks), current_failed=failed, retained_original_failures=original_failures,
                          boundary_rows=boundary_rows, max_source_error=max(row["relative_error"] for row in source_rows))), flush=True)


if __name__ == "__main__":
    source.modest()
    run()

