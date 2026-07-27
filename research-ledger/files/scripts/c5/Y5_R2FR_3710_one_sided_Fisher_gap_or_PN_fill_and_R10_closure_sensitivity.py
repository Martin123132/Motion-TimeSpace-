from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3710"
BRANCH_ID = "MTS_R2FR_Y5_ONE_SIDED_FISHER_GAP_OR_PN_FILL_AND_R10_CLOSURE_SENSITIVITY_3710"
DOC = ROOT / "3710-Y5-R2FR-one-sided-Fisher-gap-or-PN-fill-and-R10-closure-sensitivity.md"

DOC_3709 = ROOT / "3709-Y5-R2FR-Fisher-gap-and-PN-parent-source-row-fill-or-closure-demotion.md"
NEXT_3709 = RESIDUALS / "P8_Y5_R2FR_3709_NEXT_TARGET.csv"
INEQUALITY_3709 = RESIDUALS / "P8_Y5_R2FR_3709_DESIGN_INEQUALITY_ROWS.csv"
FILL_3709 = RESIDUALS / "P8_Y5_R2FR_3709_PARENT_FILL_ROWS.csv"
STATUS_3709 = RESIDUALS / "P8_Y5_R2FR_3709_STATUS.csv"
SCORE_3708 = RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_SCORE_ROWS.csv"
ANCHOR_3708 = RESIDUALS / "P8_Y5_R2FR_3708_OFFICIAL_ANCHOR_FISHER_GAP_ROWS.csv"
CURVE_STATUS_3702 = RESIDUALS / "P8_Y5_R2FR_3702_STATUS.csv"


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


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def sci(value: float) -> str:
    return f"{value:.12e}"


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3709", DOC_3709, "Theta_H*iota_H", "3709 coupled gate and closure demotion"),
        ("next_3709", NEXT_3709, "one side of the Xi_H/P_N gate", "declared 3710 target"),
        ("inequality_3709", INEQUALITY_3709, "DI3709_1_parent_gap_requirement", "coupled design inequalities"),
        ("fill_3709", FILL_3709, "FILL3709_2_PN_symbolic", "symbolic Xi_H/P_N fill rows"),
        ("status_3709", STATUS_3709, "SYMBOLIC_XIH_PN_ROWS_FILLED", "3709 status row"),
        ("score_3708", SCORE_3708, "FGS3708_066", "candidate Fisher-gap/R10 score table"),
        ("anchor_3708", ANCHOR_3708, "FGA3708_0_alpha1_anchor_gap", "official alpha=1 anchor consequence"),
        ("curve_status_3702", CURVE_STATUS_3702, "R10_CANDIDATE_CURVE", "candidate curve nonclaim status"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(timestamp),
            "source_id": source_id,
            "role": role,
            "path": str(path),
            "needle": needle,
            "exists": exists,
            "needle_found": needle in text if exists else False,
            "claim_allowed": False,
        })
    return rows


def numeric_rows(score_rows: list[dict[str, str]]) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for row in score_rows:
        rows.append({
            "gap_score_id": row["gap_score_id"],
            "lambda_um": float(row["lambda_um"]),
            "xi": float(row["Xi_H_required_clean_m2"]),
            "pn_eta0": float(row["P_N_max_eta0_m4"]),
            "pn_eta10": float(row["P_N_max_eta10_m4"]),
            "pn_eta50": float(row["P_N_max_eta50_m4"]),
            "sqrt_eta10": float(row["sqrt_P_N_max_eta10_m2"]),
        })
    return rows


def pn_sensitivity_rows(timestamp: str, rows: list[dict[str, float | str]]) -> list[dict[str, object]]:
    eta_columns = [
        ("eta0", 0.0, "pn_eta0"),
        ("eta10", 0.1, "pn_eta10"),
        ("eta50", 0.5, "pn_eta50"),
    ]
    pn_grid = [
        1e6,
        1e8,
        1e10,
        3.782222325794e10,
        1e12,
        1e15,
        1e18,
        1e21,
        1e24,
        1e27,
        1e28,
    ]
    out: list[dict[str, object]] = []
    for eta_name, eta, column in eta_columns:
        min_bound = min(float(row[column]) for row in rows)
        max_bound = max(float(row[column]) for row in rows)
        for pn_value in pn_grid:
            allowed = [row for row in rows if pn_value <= float(row[column])]
            if not allowed:
                classification = "NO_CANDIDATE_ROW_PASSES"
                max_lambda = ""
                min_lambda = ""
                min_xi = ""
                best_margin = sci(max_bound / pn_value)
            else:
                max_lambda_row = max(allowed, key=lambda row: float(row["lambda_um"]))
                min_lambda_row = min(allowed, key=lambda row: float(row["lambda_um"]))
                max_lambda = f"{float(max_lambda_row['lambda_um']):.6f}"
                min_lambda = f"{float(min_lambda_row['lambda_um']):.6f}"
                min_xi = sci(float(max_lambda_row["xi"]))
                best_margin = sci(max(float(row[column]) / pn_value for row in rows))
                classification = "ALL_CANDIDATE_ROWS_PASS" if len(allowed) == len(rows) and pn_value <= min_bound else "PARTIAL_CANDIDATE_ROWS_PASS"
            out.append({
                **base(timestamp),
                "sensitivity_id": f"PNS3710_{eta_name}_{len(out):03d}",
                "eta_name": eta_name,
                "eta": f"{eta:.3f}",
                "P_N_closure_m4": sci(pn_value),
                "candidate_rows_allowed": len(allowed),
                "candidate_rows_total": len(rows),
                "classification": classification,
                "min_lambda_allowed_um": min_lambda,
                "max_lambda_allowed_um": max_lambda,
                "least_Xi_H_required_m2_among_allowed": min_xi,
                "best_margin_PNmax_over_PN": best_margin,
                "all_rows_threshold_m4": sci(min_bound),
                "no_rows_threshold_m4": sci(max_bound),
                "score_status": "PRIVATE_CANDIDATE_CURVE_NONCLAIM",
                "claim_allowed": False,
            })
    return out


def xih_sensitivity_rows(timestamp: str, rows: list[dict[str, float | str]], anchor: dict[str, str]) -> list[dict[str, object]]:
    selected_indices = sorted(set([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 66]))
    selected_rows = [rows[index] for index in selected_indices if index < len(rows)]
    out: list[dict[str, object]] = []
    for index, row in enumerate(selected_rows):
        out.append({
            **base(timestamp),
            "xih_id": f"XIS3710_candidate_{index:02d}",
            "row_kind": "private_candidate_curve_row",
            "source_row_id": row["gap_score_id"],
            "lambda_um": f"{float(row['lambda_um']):.6f}",
            "Xi_H_clean_m2": sci(float(row["xi"])),
            "u1_clean_m2": sci(0.5 * float(row["xi"])),
            "P_N_max_eta0_m4": sci(float(row["pn_eta0"])),
            "P_N_max_eta10_m4": sci(float(row["pn_eta10"])),
            "P_N_max_eta50_m4": sci(float(row["pn_eta50"])),
            "J_eff_max_unit_factor_eta10_m2": sci(math.sqrt(float(row["pn_eta10"]))),
            "score_status": "PRIVATE_CANDIDATE_CURVE_NONCLAIM",
            "claim_allowed": False,
        })
    out.append({
        **base(timestamp),
        "xih_id": "XIS3710_anchor_alpha1",
        "row_kind": "official_alpha1_anchor_only",
        "source_row_id": anchor["anchor_gap_id"],
        "lambda_um": anchor["lambda_um"],
        "Xi_H_clean_m2": anchor["Xi_H_required_clean_m2"],
        "u1_clean_m2": anchor["u1_required_clean_m2"],
        "P_N_max_eta0_m4": anchor["P_N_max_eta0_m4"],
        "P_N_max_eta10_m4": anchor["P_N_max_eta10_m4"],
        "P_N_max_eta50_m4": "",
        "J_eff_max_unit_factor_eta10_m2": sci(math.sqrt(float(anchor["P_N_max_eta10_m4"]))),
        "score_status": "OFFICIAL_ANCHOR_ONLY_NOT_FULL_CURVE",
        "claim_allowed": False,
    })
    return out


def factor_budget_rows(timestamp: str, rows: list[dict[str, float | str]], anchor: dict[str, str]) -> list[dict[str, object]]:
    tightest = min(rows, key=lambda row: float(row["pn_eta10"]))
    shortest = max(rows, key=lambda row: float(row["pn_eta10"]))
    anchor_pn = float(anchor["P_N_max_eta10_m4"])
    specs = [
        ("FB3710_0_private_tightest", "private candidate tightest eta=0.1", float(tightest["pn_eta10"]), float(tightest["lambda_um"]), float(tightest["xi"]), "candidate curve requires review before claims"),
        ("FB3710_1_official_alpha1_anchor", "official alpha=1 anchor eta=0.1", anchor_pn, float(anchor["lambda_um"]), float(anchor["Xi_H_required_clean_m2"]), "anchor-only; does not cover arbitrary lambda"),
        ("FB3710_2_private_shortest_lambda", "private candidate shortest-lambda eta=0.1", float(shortest["pn_eta10"]), float(shortest["lambda_um"]), float(shortest["xi"]), "short-range/high-gap end of private candidate curve"),
    ]
    return [
        {
            **base(timestamp),
            "factor_budget_id": budget_id,
            "budget_role": role,
            "lambda_um": f"{lambda_um:.6f}",
            "Xi_H_clean_m2": sci(xi),
            "P_N_max_eta10_m4": sci(pn_max),
            "J_eff_bound_unit_factor": sci(math.sqrt(pn_max)),
            "factor_formula": "J_eff <= sqrt(P_N_max/(K_N*rho_Newton*C_H^2))",
            "source_product_formula": "P_N=K_N*rho_Newton*C_H^2*J_eff^2",
            "caveat": caveat,
            "claim_allowed": False,
        }
        for budget_id, role, pn_max, lambda_um, xi, caveat in specs
    ]


def branch_selection_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "selection_id": "SEL3710_0_selected_side",
            "selected_side": "P_N source-product side",
            "reason": "A sourced or bounded P_N immediately maps onto allowed lambda_H/Xi_H intervals using the existing R10 score table.",
            "first_fill_targets": "K_N; rho_Newton; C_H; J_eff=||J_y+B_y||; same-basis source normalization",
            "deferred_side": "Theta_H; iota_H; R_loss Fisher stiffness side",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "selection_id": "SEL3710_1_failure_rule",
            "selected_side": "P_N source-product side",
            "reason": "If a derived P_N lies above the candidate no-row threshold, R10 screening fails for this closure route regardless of Fisher-gap tuning inside the candidate range.",
            "first_fill_targets": "derive upper bound on K_N*rho_Newton*C_H^2*J_eff^2",
            "deferred_side": "Fisher stiffness cannot rescue a source product beyond candidate coverage without moving to shorter unreviewed lambda",
            "claim_allowed": False,
        },
    ]


def decision_rows(timestamp: str, pn_rows: list[dict[str, object]], factor_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    eta10_rows = [row for row in pn_rows if row["eta_name"] == "eta10"]
    all_threshold = eta10_rows[0]["all_rows_threshold_m4"]
    no_threshold = eta10_rows[0]["no_rows_threshold_m4"]
    tight_factor = factor_rows[0]
    return [
        {
            **base(timestamp),
            "decision_id": "DEC3710_0_PN_side_selected",
            "decision": "Attack P_N first, not Theta_H/iota_H/R_loss.",
            "rationale": "P_N has the shortest route to an immediate R10 pass/fail interval through K_N, rho_Newton, C_H and J_eff.",
            "status": "ONE_SIDED_ROUTE_SELECTED",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "decision_id": "DEC3710_1_sensitivity_bounds",
            "decision": f"For eta=0.1 on the private candidate curve, P_N below {all_threshold} m^-4 passes all candidate rows; P_N above {no_threshold} m^-4 passes none.",
            "rationale": "This gives a quantitative target for source-product derivation instead of another missing-input list.",
            "status": "PRIVATE_CANDIDATE_SENSITIVITY_RESULT",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "decision_id": "DEC3710_2_tight_factor_budget",
            "decision": f"Tightest private eta=0.1 factor budget has J_eff/sqrt(K_N*rho_Newton*C_H^2) <= {tight_factor['J_eff_bound_unit_factor']}.",
            "rationale": "This is the cleanest source-product target if the candidate curve is retained for smoke testing.",
            "status": "FACTOR_TARGET_EXPOSED",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "decision_id": "DEC3710_3_next_target",
            "decision": "Next checkpoint should decompose P_N into its four parent factors and try to source or theorem-bound one factor at a time.",
            "rationale": "The sensitivity grid is now ready; the next useful work is factor ownership, not more closure-grid math.",
            "status": "ADVANCE_TO_PN_FACTOR_DECOMPOSITION",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3710_0_PN_factors", "K_N, rho_Newton, C_H and J_eff source rows exist in one parent basis"),
        ("CG3710_1_curve_review", "private candidate R10 curve is replaced by official/reviewed curve before claims"),
        ("CG3710_2_eta_values", "eta boundary/edge values are theorem-zero or source-bounded"),
        ("CG3710_3_XiH_parent", "Theta_H, iota_H and R_loss eventually source the selected Xi_H/lambda_H"),
        ("CG3710_4_local_arenas", "PPN/EM/clock/WEP/orbit residual tensors are scored, not inferred from R10"),
        ("CG3710_5_public", "public local GR/Newton/Maxwell/R10 claim allowed"),
    ]
    return [
        {
            **base(timestamp),
            "claim_gate_id": gate_id,
            "requirement": requirement,
            "status": "BLOCKED",
            "claim_allowed": False,
        }
        for gate_id, requirement in specs
    ]


def status_rows(timestamp: str, pn_rows: list[dict[str, object]], factor_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    eta10_rows = [row for row in pn_rows if row["eta_name"] == "eta10"]
    all_threshold = eta10_rows[0]["all_rows_threshold_m4"]
    no_threshold = eta10_rows[0]["no_rows_threshold_m4"]
    tight_factor = factor_rows[0]
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3710_0",
            "status": "PN_SIDE_SELECTED_R10_CLOSURE_SENSITIVITY_GRID_WRITTEN_NONCLAIM",
            "summary": (
                "3710 selects the P_N source-product side as the first one-sided fill target and runs a private R10 sensitivity grid. "
                f"For eta=0.1 on the candidate curve, P_N <= {all_threshold} m^-4 passes every candidate row, while P_N > {no_threshold} m^-4 passes none. "
                f"The tightest private factor budget is J_eff/sqrt(K_N*rho_Newton*C_H^2) <= {tight_factor['J_eff_bound_unit_factor']}. "
                "These are nonclaim smoke targets because the curve is candidate-only and P_N factors are not source-owned."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3710_0",
            "target_doc": "3711-Y5-R2FR-PN-factor-decomposition-KN-rho-CH-Jeff-source-bound.md",
            "target_script": "scripts/Y5_R2FR_3711_PN_factor_decomposition_KN_rho_CH_Jeff_source_bound.py",
            "objective": "decompose P_N=K_N*rho_Newton*C_H^2*J_eff^2 into four parent factors and try to source or theorem-bound at least one factor without promoting closure to evidence",
            "success_gate": "one P_N factor gets a source-owned value/bound or the exact missing parent object for that factor is isolated with a nonclaim budget row",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    pn_rows: list[dict[str, object]],
    xih_rows: list[dict[str, object]],
    factor_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    eta10_rows = [row for row in pn_rows if row["eta_name"] == "eta10"]
    all_threshold = eta10_rows[0]["all_rows_threshold_m4"]
    no_threshold = eta10_rows[0]["no_rows_threshold_m4"]
    tight_factor = factor_rows[0]
    lines = [
        "# 3710 Y5 R2FR One-Sided Fisher Gap Or P_N Fill And R10 Closure Sensitivity",
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
        "- The selected first fill side is `P_N`, not the Fisher stiffness side.",
        "- Reason: once `P_N=K_N*rho_Newton*C_H^2*J_eff^2` is bounded, the existing R10 table immediately gives the allowed `Xi_H/lambda_H` range.",
        f"- For `eta=0.1`, private candidate sensitivity gives: all candidate rows pass below `{all_threshold} m^-4`; no candidate rows pass above `{no_threshold} m^-4`.",
        f"- Tightest private factor target: `J_eff/sqrt(K_N*rho_Newton*C_H^2) <= {tight_factor['J_eff_bound_unit_factor']}`.",
        "- `valid_for_claim=false`: this is a private candidate-curve sensitivity grid, not evidence for a local-GR/R10 pass.",
        "",
        "## Branch Selection",
        "",
    ]
    for row in branch_rows:
        lines.append(f"- `{row['selection_id']}`: {row['selected_side']} | {row['reason']}")
    lines.extend(["", "## P_N Sensitivity", ""])
    for row in [row for row in pn_rows if row["eta_name"] == "eta10"]:
        lines.append(f"- `{row['sensitivity_id']}` P_N={row['P_N_closure_m4']} -> `{row['classification']}`, rows={row['candidate_rows_allowed']}/{row['candidate_rows_total']}, max_lambda={row['max_lambda_allowed_um']}")
    lines.extend(["", "## Xi_H Sample Rows", ""])
    for row in xih_rows[:6] + xih_rows[-2:]:
        lines.append(f"- `{row['xih_id']}` `{row['row_kind']}`: lambda={row['lambda_um']} um, Xi_H={row['Xi_H_clean_m2']}, P_N_max_eta10={row['P_N_max_eta10_m4']}")
    lines.extend(["", "## Factor Budgets", ""])
    for row in factor_rows:
        lines.append(f"- `{row['factor_budget_id']}` `{row['budget_role']}`: {row['factor_formula']} with unit-factor `{row['J_eff_bound_unit_factor']}`")
    lines.extend(["", "## Decisions", ""])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` | {row['decision']}")
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
    branch_rows: list[dict[str, object]],
    pn_rows: list[dict[str, object]],
    xih_rows: list[dict[str, object]],
    factor_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    timestamp = stamp()
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("sources_exist", "all cited local sources exist", all(bool(row["exists"]) for row in sources), ""))
    checks.append(("needles_found", "all source needles found", all(bool(row["needle_found"]) for row in sources), ""))
    checks.append(("outputs_exist", "all generated paths exist", all(path.exists() for path in generated_paths), ""))
    csv_parse_ok = True
    csv_error = ""
    try:
        for path in [path for path in generated_paths if path.suffix.lower() == ".csv"]:
            if not parse_csv(path):
                csv_parse_ok = False
                csv_error = f"empty csv: {path}"
                break
    except Exception as exc:  # pragma: no cover
        csv_parse_ok = False
        csv_error = str(exc)
    checks.append(("csv_parse", "all generated CSV files parse and are nonempty", csv_parse_ok, csv_error))
    checks.append(("selected_pn", "P_N side is selected explicitly", any(row["selected_side"] == "P_N source-product side" for row in branch_rows), ""))
    classifications = {row["classification"] for row in pn_rows}
    checks.append(("pn_grid_classes", "P_N grid includes all/partial/none sensitivity classes", {"ALL_CANDIDATE_ROWS_PASS", "PARTIAL_CANDIDATE_ROWS_PASS", "NO_CANDIDATE_ROW_PASSES"} <= classifications, ";".join(sorted(classifications))))
    checks.append(("pn_eta_coverage", "P_N grid covers eta0/eta10/eta50", {"eta0", "eta10", "eta50"} <= {row["eta_name"] for row in pn_rows}, ""))
    checks.append(("xih_rows", "Xi_H sensitivity includes candidate rows and official anchor", len(xih_rows) >= 10 and any(row["row_kind"] == "official_alpha1_anchor_only" for row in xih_rows), f"rows={len(xih_rows)}"))
    checks.append(("factor_budget", "factor budget rows include J_eff unit-factor formula", len(factor_rows) >= 3 and all("J_eff <=" in row["factor_formula"] for row in factor_rows), ""))
    checks.append(("decisions_nonclaim", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3711", "next target advances to P_N factor decomposition", str(next_target[0]["target_doc"]).startswith("3711-") and "PN-factor" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core 3710 terms", all(term in doc_text for term in ["P_N=K_N*rho_Newton", "all candidate rows pass", "J_eff/sqrt", "valid_for_claim=false"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3710*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3710 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
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
    scores = numeric_rows(parse_csv(SCORE_3708))
    anchor = parse_csv(ANCHOR_3708)[0]
    sources = source_register(timestamp)
    branch_rows = branch_selection_rows(timestamp)
    pn_rows = pn_sensitivity_rows(timestamp, scores)
    xih_rows = xih_sensitivity_rows(timestamp, scores, anchor)
    factor_rows = factor_budget_rows(timestamp, scores, anchor)
    decisions = decision_rows(timestamp, pn_rows, factor_rows)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp, pn_rows, factor_rows)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3710_SOURCE_REGISTER.csv",
        "branch_selection": RESIDUALS / "P8_Y5_R2FR_3710_BRANCH_SELECTION_ROWS.csv",
        "pn_sensitivity": RESIDUALS / "P8_Y5_R2FR_3710_PN_CLOSURE_SENSITIVITY_ROWS.csv",
        "xih_sensitivity": RESIDUALS / "P8_Y5_R2FR_3710_XIH_CLOSURE_SENSITIVITY_ROWS.csv",
        "factor_budgets": RESIDUALS / "P8_Y5_R2FR_3710_FACTOR_BUDGET_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3710_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3710_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3710_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3710_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3710_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["branch_selection"], branch_rows)
    write_csv(outputs["pn_sensitivity"], pn_rows)
    write_csv(outputs["xih_sensitivity"], xih_rows)
    write_csv(outputs["factor_budgets"], factor_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, branch_rows, pn_rows, xih_rows, factor_rows, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, branch_rows, pn_rows, xih_rows, factor_rows, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3710 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3710 checkpoint: P_N side selected and R10 closure sensitivity grid generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
