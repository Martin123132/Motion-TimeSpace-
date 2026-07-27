from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3700"
BRANCH_ID = "MTS_R2FR_Y5_SECOND_ORDER_SOURCE_RESIDUAL_VECTOR_AND_LOCAL_TEST_RUNNER_3700"
DOC = ROOT / "3700-Y5-R2FR-second-order-source-residual-vector-and-local-test-runner.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3699", RESIDUALS / "P8_Y5_R2FR_3699_NEXT_TARGET.csv", "derive the second-order residual vector"),
        ("residuals_3699", RESIDUALS / "P8_Y5_R2FR_3699_RESIDUAL_BOUND_ROWS.csv", "Delta O_i"),
        ("projection_3699", RESIDUALS / "P8_Y5_R2FR_3699_QUOTIENT_PROJECTION_ROWS.csv", "Y_A^perp"),
        ("source_gates_3699", RESIDUALS / "P8_Y5_R2FR_3699_SOURCE_GATE_ROWS.csv", "Poynting"),
        ("suppression_3693", RESIDUALS / "P8_Y5_R2FR_3693_LOCAL_SUPPRESSION_LAW_ROWS.csv", "A_loc"),
        ("yukawa_3694", RESIDUALS / "P8_Y5_R2FR_3694_YUKAWA_ARENA_BOUND_RUNNER_ROWS.csv", "alpha_N"),
        ("ppn_trace_90", FORMALIZATION / "90-Lcg-gradient-trace-bound.md", "S_PPN ~ |q| R L_cg^2 / u"),
        ("parent_clock_newton_83", FORMALIZATION / "83-parent-equations-v1.md", "Weak-field clock/Newton target:"),
        ("red_team_06", FORMALIZATION / "06-consistency-red-team.md", "Local PPN branch is now the live gate"),
    ]
    rows = []
    for source_id, path, needle in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                **base(timestamp),
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": "second-order local residual vector construction input",
            }
        )
    return rows


def residual_tensor_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "RT3700_0_first_order_zero",
            "Fisher projection gives <C_i^0 Y_A^perp>_0=0, so partial_A<O_i>_0=0.",
            "The local observable leakage begins at quadratic order if the 3699 projection is exact.",
            "DERIVED_FROM_3699",
        ),
        (
            "RT3700_1_second_derivative",
            "R_iAB := partial_A partial_B<O_i>_0 = <C_i^0 Y_A^perp Y_B^perp>_0 - <C_i^0>_0 I_AB^perp.",
            "This is the actual residual tensor that must be sourced or bounded for each arena.",
            "RESIDUAL_TENSOR_DEFINED",
        ),
        (
            "RT3700_2_dimensionless_norm",
            "rho_i := ||G_H^-1/2 R_i G_H^-1/2||_op / N_i.",
            "Normalizes each residual to its tested observable scale N_i before comparing to experiment.",
            "NORM_GATE_DEFINED",
        ),
        (
            "RT3700_3_amplitude_bound",
            "z2_bound := (C_H ||J_y+B_y||/mu_H^2)^2 + B_edge^2 + B_boundary^2.",
            "Links the second-order source residual to the 3693 mass-gap suppression chain.",
            "AMPLITUDE_BOUND_CONDITIONAL",
        ),
        (
            "RT3700_4_master_bound",
            "epsilon_i^MTS <= 0.5 rho_i z2_bound + epsilon_edge_i + epsilon_proj_i + epsilon_boundary_i.",
            "This is the local-test pass condition before adding arena-specific kernels.",
            "MASTER_LOCAL_BOUND_DERIVED",
        ),
        (
            "RT3700_5_yukawa_kernel",
            "epsilon_i^MTS(r) <= 0.5 rho_i z0^2 exp(-2r/lambda_H)(1+r/lambda_H)^2 + epsilon_edge_i + epsilon_proj_i.",
            "First-order Yukawa suppression squares because local source leakage is second order after projection.",
            "SECOND_ORDER_YUKAWA_KERNEL_DERIVED",
        ),
    ]
    return [
        {
            **base(timestamp),
            "tensor_id": tensor_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for tensor_id, formula, meaning, status in specs
    ]


def arena_runner_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "AR3700_0_PPN",
            "PPN/local metric",
            "S_PPN := max(|gamma-1|,|beta-1|,|alpha1|,|alpha2|,|xi|,clock_metric_leak) <= epsilon_PPN",
            "S_PPN <= 0.5 rho_PPN z2_bound + K_Kperp||Kperp||/N_PPN + K_q||q_loc||/N_PPN",
            "needs rho_PPN, Kperp, q_loc Green-function normalizer, Solar baseline",
        ),
        (
            "AR3700_1_R10_Newton",
            "short-range Newton/R10",
            "abs(alpha_eff(lambda_H)) <= alpha_bound_R10(lambda_H)",
            "alpha_eff(lambda_H)=K_N * 0.5 rho_Newton z0^2 + alpha_edge + alpha_proj",
            "needs real alpha_bound_R10 curve, K_N, lambda_H, rho_Newton",
        ),
        (
            "AR3700_2_clock",
            "precision clocks/time",
            "|delta nu/nu| <= epsilon_clock",
            "|delta nu/nu| <= 0.5 rho_clock z2_bound + clock_projection_error",
            "needs clock observable C_clock, rho_clock, metric convention Gamma_kappa=h_00 or -h_00",
        ),
        (
            "AR3700_3_EM",
            "Maxwell/EM/Poynting stress",
            "max(||Delta T_EM||/||T_EM||, |Delta alpha_fs/alpha_fs|, ||Delta S_EM(Poynting)||/||S_EM||) <= epsilon_EM",
            "EM residual <= 0.5 rho_EM z2_bound + alpha_source_leak + current_normalization_error",
            "needs EM stress/Poynting residual tensor, alpha_fs source silence, charge/current normalization",
        ),
        (
            "AR3700_4_orbital",
            "orbital dynamics",
            "max(|delta a/a|, |delta precession|, |delta n/n|) <= epsilon_orbital",
            "orbital residual <= K_orbit * 0.5 rho_Newton z0^2 exp(-2r/lambda_H)(1+r/lambda_H)^2 + boundary terms",
            "needs orbital sensitivity kernels, source model, lambda_H",
        ),
        (
            "AR3700_5_WEP_species",
            "WEP/species dependence",
            "eta_species <= epsilon_WEP",
            "eta_species <= 0.5 ||rho_species_a-rho_species_b|| z2_bound + species_projection_error",
            "needs species score functions and Fisher-projected residual difference",
        ),
    ]
    return [
        {
            **base(timestamp),
            "arena_id": arena_id,
            "arena": arena,
            "pass_condition": pass_condition,
            "mts_prediction_bound": mts_prediction_bound,
            "required_inputs": required_inputs,
            "status": "NONCLAIM_RUNNER_SCHEMA_READY_VALUES_MISSING",
            "claim_allowed": False,
            "score_ready": False,
        }
        for arena_id, arena, pass_condition, mts_prediction_bound, required_inputs in specs
    ]


def break_mode_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "BM3700_0_source_projection_fail",
            "If <C_i^0 Y_A^perp>_0 != 0 for any local observable, the local branch has first-order leakage and likely fails precision tests.",
            "HARD_FAIL_OR_REPROJECT",
        ),
        (
            "BM3700_1_large_second_order",
            "If rho_i z2_bound exceeds arena tolerance, first-order silence is not enough and local GR/Maxwell/Newton recovery fails or needs a stronger mass gap.",
            "NUMERIC_BOUND_FAIL",
        ),
        (
            "BM3700_2_boundary_zero_modes",
            "Hyperbolic incoming waves, Neumann-like zero modes, topology, or nonzero boundary data add B_boundary and reopen local PPN/clock gates.",
            "BOUNDARY_THEOREM_REQUIRED",
        ),
        (
            "BM3700_3_Kperp_tensor",
            "Scalar source silence does not control tensor Kperp unless Kperp is exactly zero, cubic, or explicitly PPN-bounded.",
            "TENSOR_GATE_REQUIRED",
        ),
        (
            "BM3700_4_fitted_tolerance",
            "Choosing rho_i, z0, K_i, or alpha_eff from the local experimental budget is forbidden tuning.",
            "ANTI_TUNING_GATE",
        ),
    ]
    return [
        {
            **base(timestamp),
            "break_id": break_id,
            "failure_mode": failure_mode,
            "status": status,
            "claim_allowed": False,
        }
        for break_id, failure_mode, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3700_0",
            "Use the second-order residual vector as the local-test bridge.",
            "It converts the Fisher source-silence theorem into PPN/R10/clock/EM/orbital quantities without pretending values are known.",
            "BRIDGE_ADVANCES",
        ),
        (
            "DEC3700_1",
            "Do not claim local GR/Maxwell/Newton pass.",
            "The structural bound is derived, but rho_i, z2_bound, Kperp, q_loc, boundary amplitudes, and real experimental normalizers remain unfilled.",
            "CLAIM_BLOCKED",
        ),
        (
            "DEC3700_2",
            "Next move should be numeric-source acquisition, not more names.",
            "The runner now names exactly which rows must be sourced to score the branch.",
            "SOURCE_ROWS_NEXT",
        ),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "status": status,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale, status in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3700_0_R_tensor", "R_iAB residual tensors sourced/bounded for matter, PPN, Newton, EM/Poynting, clocks, orbits, WEP", "BLOCKED"),
        ("CG3700_1_amplitude", "z2_bound sourced from parent J_y, mu_H, C_H, edge, and boundary rows", "BLOCKED"),
        ("CG3700_2_test_normalizers", "epsilon_i and N_i sourced for each local arena", "BLOCKED"),
        ("CG3700_3_R10_curve", "real R10 alpha_bound(lambda) curve and lambda_H scoring implemented", "BLOCKED"),
        ("CG3700_4_PPN_solver", "PPN Green-function projection constants and Kperp/q_loc tensor terms bounded", "BLOCKED"),
        ("CG3700_5_EM_coupling", "Maxwell stress, Poynting flux, alpha_fs, charge/current residuals bounded", "BLOCKED"),
        ("CG3700_6_public", "public local-GR/Maxwell/Newton claim allowed", "BLOCKED"),
    ]
    return [
        {
            **base(timestamp),
            "claim_gate_id": gate_id,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
        }
        for gate_id, requirement, status in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3700_0",
            "status": "SECOND_ORDER_LOCAL_RESIDUAL_VECTOR_DERIVED_RUNNER_SCHEMA_READY_VALUES_MISSING",
            "summary": (
                "3700 turns Fisher source silence into the local-test bridge: after first-order projection, each local observable has "
                "Delta O_i=0.5 z^A z^B R_iAB+O(|z|^3). With z bounded by the horizontal mass gap, every arena gets a pass inequality. "
                "The route is mathematically sharper and test-facing, but remains nonclaim until residual tensors, amplitude rows, PPN/R10/EM/clock/orbit normalizers, and boundary/Kperp terms are sourced."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3700_0",
            "target_doc": "3701-Y5-R2FR-local-test-source-row-acquisition-and-residual-matrix.md",
            "target_script": "scripts/Y5_R2FR_3701_local_test_source_row_acquisition_and_residual_matrix.py",
            "objective": "create source-ready numeric/symbolic rows for rho_i, z2_bound, Kperp, q_loc, R10 alpha_bound(lambda), PPN normalizers, EM/Poynting residuals, clock and orbital tolerances",
            "success_gate": "at least one local arena becomes actually score-ready with sourced values, or the exact missing numeric rows are isolated without changing claim status",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    residual_tensors: list[dict[str, object]],
    arenas: list[dict[str, object]],
    break_modes: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3700 Y5 R2FR Second-Order Source Residual Vector And Local Test Runner",
        "",
        "Private checkpoint. No GitHub action. No public claim.",
        "",
        "## Status",
        "",
        f"- `{status[0]['status']}`",
        f"- {status[0]['summary']}",
        "",
        "## Main Result",
        "",
        "- `3699` gives first-order source silence: `<C_i^0 Y_A^perp>_0=0`.",
        "- Therefore each local observable starts as `Delta O_i(z)=0.5 z^A z^B R_iAB+O(|z|^3)`.",
        "- Define `rho_i=||G_H^-1/2 R_i G_H^-1/2||_op/N_i` and `z2_bound=(C_H||J_y+B_y||/mu_H^2)^2+B_edge^2+B_boundary^2`.",
        "- Master local gate: `epsilon_i^MTS <= 0.5 rho_i z2_bound + epsilon_edge_i + epsilon_proj_i + epsilon_boundary_i`.",
        "- Yukawa/local-range gate squares the first-order kernel: `epsilon_i(r) <= 0.5 rho_i z0^2 exp(-2r/lambda_H)(1+r/lambda_H)^2 + ...`.",
        "",
        "## Meaning",
        "",
        "- This is good news structurally: if Fisher projection is exact, local violations are quadratic, not linear.",
        "- It is not yet a pass: quadratic can still be far too large unless `rho_i`, `z2_bound`, `Kperp`, `q_loc`, and boundary terms are small for derived reasons.",
        "- This runner treats GR/Maxwell/Newton as the local baseline and scores only residual deviations, which is the fair comparison route.",
        "",
        "## Residual Tensor Rows",
        "",
    ]
    for row in residual_tensors:
        lines.append(f"- `{row['tensor_id']}`: `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Arena Runner Rows", ""])
    for row in arenas:
        lines.append(f"- `{row['arena_id']}`: {row['arena']} | `{row['status']}` | {row['mts_prediction_bound']}")
    lines.extend(["", "## Break Modes", ""])
    for row in break_modes:
        lines.append(f"- `{row['break_id']}`: `{row['status']}` | {row['failure_mode']}")
    lines.extend(["", "## Decisions", ""])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` | {row['decision']} | {row['rationale']}")
    lines.extend(["", "## Claim Gates", ""])
    for row in claim_gates:
        lines.append(f"- `{row['claim_gate_id']}`: `{row['status']}` | {row['requirement']}")
    lines.extend(["", "## Source Register", ""])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: exists={row['exists']} needle_found={row['needle_found']} path=`{row['path']}`")
    lines.extend(["", "## Next Target", ""])
    lines.append(f"- `{next_target[0]['target_doc']}`")
    lines.append(f"- Objective: {next_target[0]['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    generated_paths: list[Path],
    sources: list[dict[str, object]],
    residual_tensors: list[dict[str, object]],
    arenas: list[dict[str, object]],
    break_modes: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    timestamp = stamp()
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("sources_exist", "all cited local sources exist", all(bool(row["exists"]) for row in sources), ""))
    checks.append(("needles_found", "all source needles were found", all(bool(row["needle_found"]) for row in sources), ""))
    checks.append(("outputs_exist", "all generated paths exist", all(path.exists() for path in generated_paths), ""))
    csv_paths = [path for path in generated_paths if path.suffix.lower() == ".csv"]
    csv_parse_ok = True
    csv_error = ""
    try:
        for path in csv_paths:
            if not parse_csv(path):
                csv_parse_ok = False
                csv_error = f"empty csv: {path}"
                break
    except Exception as exc:  # pragma: no cover
        csv_parse_ok = False
        csv_error = str(exc)
    checks.append(("csv_parse", "all generated CSV files parse and are nonempty", csv_parse_ok, csv_error))
    tensor_by_id = {str(row["tensor_id"]): row for row in residual_tensors}
    arena_by_id = {str(row["arena_id"]): row for row in arenas}
    checks.append(("second_order_formula", "second-order Delta O formula present", "Delta O_i" in str(tensor_by_id["RT3700_1_second_derivative"]["formula"]) or "R_iAB" in str(tensor_by_id["RT3700_1_second_derivative"]["formula"]), ""))
    checks.append(("master_bound", "master local bound contains rho_i and z2_bound", "rho_i" in str(tensor_by_id["RT3700_4_master_bound"]["formula"]) and "z2_bound" in str(tensor_by_id["RT3700_4_master_bound"]["formula"]), ""))
    checks.append(("squared_yukawa", "second-order Yukawa kernel is squared", "exp(-2r/lambda_H)" in str(tensor_by_id["RT3700_5_yukawa_kernel"]["formula"]), ""))
    checks.append(("all_key_arenas", "PPN/R10/clock/EM/orbital/WEP arenas exist", all(arena_id in arena_by_id for arena_id in ["AR3700_0_PPN", "AR3700_1_R10_Newton", "AR3700_2_clock", "AR3700_3_EM", "AR3700_4_orbital", "AR3700_5_WEP_species"]), ""))
    checks.append(("em_contains_poynting", "EM arena includes Poynting residual", "Poynting" in str(arena_by_id["AR3700_3_EM"]["arena"]) or "Poynting" in str(arena_by_id["AR3700_3_EM"]["pass_condition"]), ""))
    checks.append(("runner_nonclaim", "all arena runner rows nonclaim and not score ready", all(row["claim_allowed"] is False and row["score_ready"] is False for row in arenas), ""))
    checks.append(("break_modes_present", "break modes include boundary and Kperp", any("boundary" in str(row["failure_mode"]).lower() for row in break_modes) and any("Kperp" in str(row["failure_mode"]) for row in break_modes), ""))
    checks.append(("decisions_nonclaim", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3701", "next target advances to source-row acquisition", str(next_target[0]["target_doc"]).startswith("3701-") and "source-row" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core residual vector terms", all(term in doc_text for term in ["Delta O_i(z)", "rho_i", "z2_bound", "exp(-2r/lambda_H)", "GR/Maxwell/Newton"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3700*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3700 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
    return [
        {
            **base(timestamp),
            "validation_id": check_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "details": details,
        }
        for check_id, description, passed, details in checks
    ]


def main() -> int:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    sources = source_register(timestamp)
    residual_tensors = residual_tensor_rows(timestamp)
    arenas = arena_runner_rows(timestamp)
    break_modes = break_mode_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3700_SOURCE_REGISTER.csv",
        "residual_tensors": RESIDUALS / "P8_Y5_R2FR_3700_RESIDUAL_TENSOR_ROWS.csv",
        "arenas": RESIDUALS / "P8_Y5_R2FR_3700_ARENA_RUNNER_ROWS.csv",
        "break_modes": RESIDUALS / "P8_Y5_R2FR_3700_BREAK_MODE_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3700_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3700_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3700_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3700_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3700_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["residual_tensors"], residual_tensors)
    write_csv(outputs["arenas"], arenas)
    write_csv(outputs["break_modes"], break_modes)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, residual_tensors, arenas, break_modes, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, residual_tensors, arenas, break_modes, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3700 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3700 checkpoint: second-order local residual vector and arena runner schema ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
