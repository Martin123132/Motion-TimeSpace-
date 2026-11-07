import csv
from common import ROOT, SECOND, ALGEBRA, GATE, modest, guard, check_parent, require, read, write, digest
from canonical_math import Background, transform, joint_extractor, JFULL, transpose, multiply, load, sup, norm
import numpy as np
from scipy.interpolate import CubicSpline


def vector_errors(difference, reference, alternative=None):
    scales = np.max(abs(reference), axis=0)
    if alternative is not None:
        scales = np.maximum(scales, np.max(abs(alternative), axis=0))
    return np.max(abs(difference), axis=0) / np.maximum(scales, 1e-80)


def constraints(packet, state, transformation, transformed, wave, model):
    scale, hubble, meta, terms = packet["a"], packet["H"], packet["metadata"], packet["terms"]
    count = len(scale)
    source_row = np.zeros((count, 8))
    density_row = np.zeros_like(source_row)
    source_row[:, 0] = meta[:, 5]
    density_row[:, 0] = (scale * meta[:, 8])**2 * meta[:, 4]
    density_row[:, 1] = meta[:, 5] / scale**2
    if model == "heavy":
        phase = packet["carrier_phase"]
        carrier = scale * np.sqrt(scale * meta[:, 18])
        displacement = np.column_stack([np.cos(phase), np.sin(phase)]) / carrier[:, None]
        velocity = carrier[:, None] * np.column_stack([-np.sin(phase), np.cos(phase)]) / scale[:, None]**2
        source_row[:, 2:4] = meta[:, 15, None] * displacement
        density_row[:, 2:4] = meta[:, 15, None] * velocity + ((scale * meta[:, 18])**2 * meta[:, 14])[:, None] * displacement
    geometry_row = np.zeros_like(source_row)
    geometry_row[:, 5], geometry_row[:, 7] = -6., 1.
    ham = 1.5 * hubble[:, None] * source_row - hubble[:, None] * geometry_row / (2 * scale[:, None]**2) + density_row / 2
    ham[:, 6] += wave**2
    mom = np.zeros_like(ham)
    mom[:, 5] = 1 / scale**2
    other_density = terms[:, :5, 0].sum(axis=1)
    other_current = terms[:, :5, 1].sum(axis=1)
    checks, diagnostics = {}, {}
    for name, row, constant in (("hamiltonian", ham, other_density / 2), ("momentum", mom, -other_current / (2 * wave))):
        original = np.sum(row * state, axis=1) + constant
        new_row = np.einsum("ni,nij->nj", row, transformation)
        new_value = np.sum(new_row * transformed, axis=1) + constant
        scale_value = norm(np.sum(abs(row * state), axis=1) + abs(constant))
        checks[name + "_pullback"] = sup(original - new_value) / scale_value
        diagnostics[name + "_native_residual"] = sup(original) / scale_value
        diagnostics[name + "_transformed_residual"] = sup(new_value) / scale_value
    scalar_density = np.sum(density_row * state, axis=1)
    scalar_current = wave * np.sum(source_row * state, axis=1)
    checks["density_reconstruction"] = sup(scalar_density - terms[:, 5:, 0].sum(axis=1)) / norm(scalar_density)
    checks["current_reconstruction"] = sup(scalar_current - terms[:, 5:, 1].sum(axis=1)) / norm(scalar_current)
    return checks, diagnostics


def replay_integrals(efold, state, raw, accounted):
    rows = []
    replays = {}
    for stride in (1, 2, 4):
        keep = np.unique(np.r_[np.arange(0, len(efold), stride), len(efold) - 1])
        row = dict(stride=stride, samples=len(keep))
        for name, rates in (("raw", raw), ("accounted", accounted)):
            primitive = CubicSpline(efold[keep], rates[keep], axis=0).antiderivative()
            reconstructed = state[0] + primitive(efold) - primitive(efold[0])
            error = vector_errors(reconstructed - state, state)
            row[name + "_component_errors"] = error.tolist()
            row[name + "_maximum"] = float(np.max(error))
            row[name + "_within_gate"] = bool(np.max(error) < GATE)
            replays[(stride, name)] = reconstructed
        rows.append(row)
    refinement = {}
    for name in ("raw", "accounted"):
        changes = [float(np.max(vector_errors(replays[(first, name)] - replays[(second, name)], state))) for first, second in ((4, 2), (2, 1))]
        refinement[name] = dict(coarse_to_medium=changes[0], medium_to_fine=changes[1],
                                fine_change_within_gate=changes[1] < GATE,
                                change_shrinks=changes[1] < changes[0] or changes[0] == changes[1] == 0)
    return rows, refinement


def inspect_case(packet, extracted, operators, wave, model):
    state, actual, generated, predicted, linear = [extracted[name] for name in ("state", "actual", "generated", "predicted", "linear")]
    count = len(state)
    if model == "heavy":
        units, matrix, rate, fast = [operators[name] for name in ("balance", "transform", "rate", "fast_rate")]
        analytic_hessian = operators["hessian"]
    else:
        units = np.ones((count, 8))
        matrix = np.broadcast_to(np.eye(8), (count, 8, 8))
        rate = fast = np.zeros_like(matrix)
        analytic_hessian = extracted["hessian"]
    inverse = -JFULL @ transpose(matrix) @ JFULL
    transformed_scaled = multiply(inverse, state / units)
    transformed_state = units * transformed_scaled
    hscale = units[:, :, None] * units[:, None, :]
    native_hessian = extracted["hessian"] * hscale
    connection = transpose(matrix) @ JFULL @ rate
    new_hessian = transpose(matrix) @ native_hessian @ matrix + connection
    frozen_hessian = transpose(matrix) @ native_hessian @ matrix + transpose(matrix) @ JFULL @ fast
    new_linear = multiply(transpose(matrix), linear * units)
    raw_scaled = multiply(JFULL, multiply(new_hessian, transformed_scaled) + new_linear)
    accounted_scaled = raw_scaled + multiply(inverse, predicted / units)
    chain_scaled = multiply(inverse, actual / units - multiply(rate, transformed_scaled))
    frozen_scaled = multiply(JFULL, multiply(frozen_hessian, transformed_scaled) + new_linear)
    raw, accounted, chain, frozen = [units * value for value in (raw_scaled, accounted_scaled, chain_scaled, frozen_scaled)]
    physical_matrix = matrix * units[:, :, None] / units[:, None, :]
    checks = dict(extracted["checks"])
    checks.update(dict(
        full_hessian_reconstruction=sup((analytic_hessian - extracted["hessian"]) * hscale) / norm(native_hessian),
        symplectic=sup(transpose(matrix) @ JFULL @ matrix - JFULL),
        inverse=sup(inverse @ matrix - np.eye(8)),
        symplectic_derivative=sup(transpose(rate) @ JFULL @ matrix + transpose(matrix) @ JFULL @ rate) / norm(rate),
        transformed_symmetry=sup(new_hessian - transpose(new_hessian)) / norm(new_hessian),
        coordinate_roundtrip=float(np.max(vector_errors(units * multiply(matrix, transformed_scaled) - state, state))),
        full_accounted_time_chain=float(np.max(vector_errors(chain - accounted, chain, accounted))),
        action_source_pullback=float(np.max(vector_errors(raw - units * multiply(inverse, generated / units - multiply(rate, transformed_scaled)), raw))),
        frozen_omission_identity=float(np.max(vector_errors(raw - frozen + units * multiply(inverse, multiply(rate - fast, transformed_scaled)), raw, frozen)))))
    constraint_checks, constraint_diagnostics = constraints(packet, state, physical_matrix, transformed_state, wave, model)
    checks.update(constraint_checks)
    zero = not np.any(state)
    if model == "cold":
        checks["cold_identity"] = sup(transformed_state - state)
    if zero:
        checks["zero_state"] = max(sup(transformed_state), sup(chain), sup(raw), sup(accounted))
    active = list(range(8)) if model == "heavy" else [0, 1, 4, 5, 6, 7]
    raw_errors = vector_errors(chain - raw, chain, raw)
    frozen_errors = vector_errors(chain - frozen, chain, frozen)
    omission = vector_errors(raw - frozen, chain, raw)
    integrated, refinement = replay_integrals(packet["efold"], transformed_state, raw, accounted)
    diagnostics = dict(raw_flow_component_errors=raw_errors.tolist(), frozen_flow_component_errors=frozen_errors.tolist(),
                       omitted_actual_coefficient_rate_errors=omission.tolist(),
                       constraints=constraint_diagnostics, integral_replays=integrated, replay_refinement=refinement,
                       raw_flow_within_gate=bool(max(raw_errors[active]) < GATE),
                       replay_accounted_within_gate=integrated[0]["accounted_within_gate"],
                       replay_raw_within_gate=integrated[0]["raw_within_gate"],
                       source_interface="saved current rest-species stress; saved-history replay, not independent forward prediction",
                       zero_control=zero)
    algebra_pass = all(np.isfinite(value) and 0 <= value < ALGEBRA for value in checks.values())
    diagnostics["numerical_passed"] = bool(diagnostics["raw_flow_within_gate"] and diagnostics["replay_accounted_within_gate"]
                                          and diagnostics["replay_raw_within_gate"] and all(item["fine_change_within_gate"] for item in refinement.values())
                                          and max(constraint_diagnostics.values()) < GATE)
    return checks, diagnostics, algebra_pass


def main():
    modest()
    check_parent()
    require(read(ROOT / "probe-result.json")["passed"], "independent derivative qualification")
    write(ROOT / "replay-frozen-inputs.json", dict(sources={str(path): digest(path) for path in ROOT.iterdir() if path.suffix in (".py", ".md", ".ps1")},
                                                 probe=digest(ROOT / "probe-result.json"), algebra=ALGEBRA, numerical=GATE))
    owner = read(SECOND / "prediction-result.json")
    extract = joint_extractor()[0]
    records = ROOT / "records"
    operators_path = ROOT / "operators"
    records.mkdir(exist_ok=False)
    operators_path.mkdir(exist_ok=False)
    background = Background("heavy")
    rows = []
    for family in owner["reports"]:
        guard()
        operators = None
        if family["model"] == "heavy":
            pieces = []
            for start in range(0, len(background.efold), 1024):
                guard()
                pieces.append(transform(background.evaluate(background.efold[start:start + 1024]), family["wave"]))
                if start % 4096 == 0:
                    print("Operator", family["label"], start, "/", len(background.efold), flush=True)
            operators = {name: np.concatenate([piece[name] for piece in pieces]) for name in pieces[0]}
            del pieces
            path = operators_path / (family["label"] + ".npz")
            np.savez_compressed(path, efold=background.efold, **operators)
            print("Saved", path.name, digest(path), flush=True)
        for case in family["cases"]:
            guard()
            path = SECOND / "runs-second" / (family["model"] + "-" + family["label"]) / case["file"]
            require(digest(path) == case["sha256"], "saved packet changed")
            packet = load(path)
            if operators is not None:
                require(np.array_equal(packet["efold"], background.efold), "original grid")
            extracted = extract(packet, family["wave"], family["model"])
            checks, diagnostics, algebra_pass = inspect_case(packet, extracted, operators, family["wave"], family["model"])
            row = dict(family=family["model"] + "-" + family["label"], tag=case["tag"], wave=family["wave"],
                       input=str(path), sha256=case["sha256"], points=len(packet["efold"]), algebra_checks=checks,
                       diagnostics=diagnostics, algebra_passed=algebra_pass,
                       passed=bool(algebra_pass and diagnostics["numerical_passed"]))
            write(records / (row["family"] + "-" + row["tag"] + ".json"), row)
            rows.append(row)
            print(row["family"], row["tag"], "algebra", max(checks.values()), "rawflow", max(diagnostics["raw_flow_component_errors"]),
                  "replay", diagnostics["integral_replays"][0]["raw_maximum"], diagnostics["integral_replays"][0]["accounted_maximum"],
                  "passed", row["passed"], flush=True)
            del packet, extracted
        del operators
    check_parent()
    passed = all(row["passed"] for row in rows)
    write(ROOT / "result.json", dict(state="complete", passed=passed, histories=len(rows), new_evolutions=0,
          full_actual_background_derivative_derived=True, averaged_forward_qualification_claimed=False,
          independent_forward_prediction=False, algebra_all_pass=all(row["algebra_passed"] for row in rows),
          rows=rows))
    with (ROOT / "summary.csv").open("x", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["family", "case", "algebra_max", "raw_flow_max", "frozen_flow_max", "raw_replay_max", "accounted_replay_max", "passed"])
        for row in rows:
            diagnostics = row["diagnostics"]
            writer.writerow([row["family"], row["tag"], max(row["algebra_checks"].values()),
                             max(diagnostics["raw_flow_component_errors"]), max(diagnostics["frozen_flow_component_errors"]),
                             diagnostics["integral_replays"][0]["raw_maximum"], diagnostics["integral_replays"][0]["accounted_maximum"], row["passed"]])
    print("Completed all saved histories; qualification", passed, flush=True)


if __name__ == "__main__":
    main()
