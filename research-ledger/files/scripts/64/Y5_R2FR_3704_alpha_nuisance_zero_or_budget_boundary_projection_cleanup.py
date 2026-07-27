from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3704"
BRANCH_ID = "MTS_R2FR_Y5_ALPHA_NUISANCE_ZERO_OR_BUDGET_BOUNDARY_PROJECTION_CLEANUP_3704"
DOC = ROOT / "3704-Y5-R2FR-alpha-nuisance-zero-or-budget-boundary-projection-cleanup.md"

DOC_3703 = ROOT / "3703-Y5-R2FR-MTS-rho-Newton-z2bound-muH-numeric-or-symbolic-bound.md"
PRODUCT_3703 = RESIDUALS / "P8_Y5_R2FR_3703_R10_PRODUCT_BOUND_ROWS.csv"
MISSING_3703 = RESIDUALS / "P8_Y5_R2FR_3703_MISSING_PARENT_INPUT_ROWS.csv"
PROJECTION_3699 = RESIDUALS / "P8_Y5_R2FR_3699_QUOTIENT_PROJECTION_ROWS.csv"
SOURCE_GATE_3699 = RESIDUALS / "P8_Y5_R2FR_3699_SOURCE_GATE_ROWS.csv"
SUPPRESSION_3693 = RESIDUALS / "P8_Y5_R2FR_3693_LOCAL_SUPPRESSION_LAW_ROWS.csv"
YUKAWA_3694 = RESIDUALS / "P8_Y5_R2FR_3694_YUKAWA_ARENA_BOUND_RUNNER_ROWS.csv"
DOC_1010 = ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md"


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


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3703", DOC_3703, "alpha_nuisance", "3703 nuisance decomposition and P_N gate"),
        ("product_3703", PRODUCT_3703, "P_N_max_eta10_m4", "candidate P_N budget rows"),
        ("missing_3703", MISSING_3703, "alpha_nuisance", "3703 identified nuisance as next target"),
        ("projection_3699", PROJECTION_3699, "Y_A^perp", "Fisher projection mechanism"),
        ("source_gate_3699", SOURCE_GATE_3699, "kappa_GR", "Newton/GR coupling appears in resolved source gate"),
        ("suppression_3693", SUPPRESSION_3693, "R_edge_A+R_proj_A", "edge/projection local-kernel terms"),
        ("yukawa_3694", YUKAWA_3694, "R_edge_A+R_proj_A", "Yukawa arena runner keeps edge/projection explicit"),
        ("q_loc_1010", DOC_1010, "boundary no-flux", "q_loc/local-GR boundary no-flux still unsigned"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
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
                "role": role,
            }
        )
    return rows


def theorem_contract_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "NZT3704_0_decomposition",
            "alpha_nuisance",
            "0.5*K_N*rho_Newton*(B_edge^2+B_boundary^2)+alpha_edge+alpha_proj",
            "identity imported from 3703",
            "separates bulk source product from edge, boundary, and projection leakage",
            "DERIVED_INPUT",
        ),
        (
            "NZT3704_1_projection_zero",
            "alpha_proj=0",
            "R10/Newton readout O_N is in the Fisher-resolved basis C_i and uses the same quotient q/P_loc as the GR/Newton fixed point",
            "3699 includes kappa_GR and Newton-coupling source silence; second-order Newton residual is already carried by rho_Newton/P_N",
            "projection leakage is not allowed to be an extra fitted force channel",
            "CONDITIONAL_ZERO_THEOREM",
        ),
        (
            "NZT3704_2_boundary_zero",
            "B_boundary=0",
            "local R10 branch is posed on a compact collar domain with fixed quotient data, y|partialOmega=0 or natural n.G_H Dy=0, and no incoming horizontal flux",
            "standard Green/coercivity boundary term vanishes only under a parent-owned no-flux or fixed-boundary condition",
            "kills the boundary part of the amplitude nuisance instead of absorbing it into P_N",
            "CONDITIONAL_ZERO_THEOREM_UNSIGNED",
        ),
        (
            "NZT3704_3_edge_zero",
            "B_edge=0 and alpha_edge=0",
            "source support lies strictly inside the collar, cutoff derivatives do not overlap horizontal response support, and the readout operator is the same on the interior and collar",
            "edge terms are integration/collar artifacts, so they vanish only if the branch owns its support/collar geometry",
            "kills the edge part of alpha_nuisance without tuning to R10",
            "CONDITIONAL_ZERO_THEOREM_UNSIGNED",
        ),
        (
            "NZT3704_4_full_zero",
            "alpha_nuisance=0",
            "NZT3704_1, NZT3704_2, and NZT3704_3 all hold simultaneously",
            "then R10 reduces to the clean product gate 0.5*P_N*lambda_H^4 <= alpha_bound_R10(lambda_H)",
            "this is the best local-Newton route, but it is not claimable until the three clauses are parent-signed",
            "CONDITIONAL_BRANCH_CONTRACT",
        ),
        (
            "NZT3704_5_budget_fallback",
            "alpha_nuisance <= eta_R10*alpha_bound_R10(lambda_H), 0<=eta_R10<1",
            "if any zero clause is unsigned or finite, allocate a sourced absolute budget rather than claiming zero",
            "gives P_N <= 2*(1-eta_R10)*alpha_bound_R10(lambda_H)/lambda_H^4",
            "keeps local R10 score possible without hiding boundary/projection leakage",
            "BUDGET_THEOREM",
        ),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "target": target,
            "condition_or_formula": condition,
            "derivation_basis": basis,
            "meaning": meaning,
            "status": status,
            "parent_signed": False,
            "claim_allowed": False,
        }
        for theorem_id, target, condition, basis, meaning, status in specs
    ]


def term_verdict_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "TERM3704_0_alpha_proj",
            "alpha_proj",
            "conditionallly_zero_if_resolved_Newton_R10_basis_complete",
            "best current status",
            "Fisher projection already includes kappa_GR/Newton coupling; any remaining R10 Newton second-order leakage belongs in rho_Newton/P_N, not an extra projection knob.",
            "needs parent certificate that the actual R10 force readout and P_loc are in the same resolved quotient basis",
        ),
        (
            "TERM3704_1_B_boundary",
            "B_boundary",
            "not_zero_without_no_flux_or_fixed_boundary_contract",
            "hard obstruction",
            "1010 still marks boundary no-flux unsigned; therefore boundary leakage cannot be deleted by rhetoric.",
            "prove compact no-flux collar or keep finite eta_boundary budget",
        ),
        (
            "TERM3704_2_B_edge",
            "B_edge",
            "not_zero_without_collar_support_contract",
            "hard obstruction",
            "3693/3694 keep R_edge explicit; it can vanish for compact support/collar geometry but is not yet parent-signed.",
            "prove edge/collar theorem or keep finite eta_edge budget",
        ),
        (
            "TERM3704_3_alpha_edge",
            "alpha_edge",
            "not_zero_without_same_readout_operator_contract",
            "hard obstruction",
            "edge readout mismatch is separate from the bulk P_N product and must not be hidden inside rho_Newton.",
            "prove same interior/collar readout or keep finite eta_edge budget",
        ),
    ]
    return [
        {
            **base(timestamp),
            "term_id": term_id,
            "term": term,
            "verdict": verdict,
            "severity": severity,
            "rationale": rationale,
            "next_action": next_action,
            "claim_allowed": False,
        }
        for term_id, term, verdict, severity, rationale, next_action in specs
    ]


def read_product_rows() -> list[dict[str, str]]:
    rows = parse_csv(PRODUCT_3703)
    return sorted(rows, key=lambda row: float(row["lambda_m"]))


def budget_rows(timestamp: str, product_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for idx, row in enumerate(product_rows):
        lambda_m = float(row["lambda_m"])
        alpha_bound = float(row["alpha_bound_abs"])
        p_eta_0 = float(row["P_N_max_zero_nuisance_m4"])
        p_eta_10 = float(row["P_N_max_eta10_m4"])
        p_eta_50 = float(row["P_N_max_eta50_m4"])
        rows.append(
            {
                **base(timestamp),
                "budget_row_id": f"ANB3704_{idx:03d}",
                "source_bound_row_id": row["bound_row_id"],
                "curve_row_id": row["curve_row_id"],
                "lambda_m": row["lambda_m"],
                "lambda_um": row["lambda_um"],
                "alpha_bound_abs": row["alpha_bound_abs"],
                "alpha_nuisance_max_eta0": "0.000000000000e+00",
                "P_N_max_eta0_m4": f"{p_eta_0:.12e}",
                "alpha_nuisance_max_eta10": f"{0.10 * alpha_bound:.12e}",
                "P_N_max_eta10_m4": f"{p_eta_10:.12e}",
                "alpha_nuisance_max_eta50": f"{0.50 * alpha_bound:.12e}",
                "P_N_max_eta50_m4": f"{p_eta_50:.12e}",
                "component_rule": "eta_R10=eta_proj+eta_edge+eta_boundary; alpha_proj term should be zero by projection certificate or counted in eta_proj",
                "claim_allowed": False,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3704_0",
            "Alpha projection is no longer allowed to float as an independent knob.",
            "If R10/Newton readout is in the resolved Fisher quotient basis, alpha_proj=0; otherwise the branch must declare an explicit eta_proj budget.",
            "PROJECTION_BRANCH_SHARPENED",
        ),
        (
            "DEC3704_1",
            "Boundary and edge zeros are plausible but not currently parent-signed.",
            "The archive still keeps boundary no-flux and R_edge/R_proj terms explicit, so deleting them would be a closure assumption.",
            "ZERO_PROOF_INCOMPLETE",
        ),
        (
            "DEC3704_2",
            "R10 can still be scored privately through an eta_R10 budget.",
            "For any sourced eta_R10<1, the product gate becomes P_N <= 2*(1-eta_R10)*alpha_bound/lambda_H^4.",
            "BUDGET_RUNNER_READY",
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
        ("CG3704_0_projection", "R10/Newton readout and P_loc certified inside the Fisher-resolved quotient basis", "BLOCKED"),
        ("CG3704_1_boundary", "compact fixed/no-flux collar proves B_boundary=0 or finite eta_boundary is sourced", "BLOCKED"),
        ("CG3704_2_edge", "support/collar/readout theorem proves B_edge=alpha_edge=0 or finite eta_edge is sourced", "BLOCKED"),
        ("CG3704_3_eta", "eta_R10 components are zero or finite absolute-summed sourced budgets with eta_R10<1", "BLOCKED"),
        ("CG3704_4_score", "P_N/lambda_H are parent-sourced and scored against the selected eta_R10 row", "BLOCKED"),
        ("CG3704_5_public", "public R10/local-Newton claim allowed", "BLOCKED"),
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


def status_rows(timestamp: str, budgets: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3704_0",
            "status": "ALPHA_NUISANCE_SPLIT_INTO_PROJECTION_ZERO_CONTRACT_AND_EDGE_BOUNDARY_BUDGET_RUNNER",
            "summary": (
                f"3704 converts alpha_nuisance into a precise branch contract: alpha_proj can be zeroed only by a resolved Newton/R10 quotient certificate; "
                f"edge and boundary terms require compact collar/no-flux theorems or explicit eta_R10 budgets. Generated {len(budgets)} budget rows from the 3703 product curve."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3704_0",
            "target_doc": "3705-Y5-R2FR-compact-collar-no-flux-and-r10-projection-certificate.md",
            "target_script": "scripts/Y5_R2FR_3705_compact_collar_no_flux_and_r10_projection_certificate.py",
            "objective": "try to parent-sign the two remaining zero clauses: R10/Newton projection completeness and compact collar no-flux/edge silence",
            "success_gate": "alpha_proj=0 and B_boundary/B_edge/alpha_edge=0 become theorem-signed, or eta_proj/eta_boundary/eta_edge rows become finite sourced inputs",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    terms: list[dict[str, object]],
    budgets: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    tightest = min(budgets, key=lambda row: float(row["P_N_max_eta10_m4"]))
    lines = [
        "# 3704 Y5 R2FR Alpha-Nuisance Zero Or Budget Boundary Projection Cleanup",
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
        "- 3703 left `alpha_nuisance` as the local R10 obstruction.",
        "- 3704 splits it into three distinct responsibilities: projection leakage, boundary leakage, and edge/collar leakage.",
        "- The projection term has a real zero route: if the R10/Newton readout is part of the Fisher-resolved quotient basis, `alpha_proj=0`; its second-order leakage is then already counted in `rho_Newton/P_N`.",
        "- Boundary and edge terms do not get a free pass: they require a compact fixed/no-flux collar theorem or finite `eta_R10` budgets.",
        "- The clean zero branch is `alpha_nuisance=0`, which reduces R10 to `0.5*P_N*lambda_H^4 <= alpha_bound_R10(lambda_H)`.",
        "- The budget branch is `alpha_nuisance <= eta_R10*alpha_bound_R10(lambda_H)`, giving `P_N <= 2*(1-eta_R10)*alpha_bound_R10(lambda_H)/lambda_H^4`.",
        "- `valid_for_claim=false` throughout: this is a branch contract and budget runner, not a local-Newton claim.",
        "",
        "## Zero Contract",
        "",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: `{row['status']}` | {row['target']} | {row['condition_or_formula']}")
    lines.extend(["", "## Term Verdicts", ""])
    for row in terms:
        lines.append(f"- `{row['term_id']}`: `{row['verdict']}` | {row['term']} | {row['rationale']}")
    lines.extend(["", "## Budget Rows", ""])
    lines.append(f"- Candidate budget rows generated: `{len(budgets)}`.")
    lines.append(f"- Tightest eta10 row: `lambda={tightest['lambda_um']} um`, `P_N_max_eta10={tightest['P_N_max_eta10_m4']} m^-4`.")
    lines.append("- All budget rows are private/nonclaim because `eta_R10`, `P_N`, and `lambda_H` are not parent-sourced yet.")
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
    theorem: list[dict[str, object]],
    terms: list[dict[str, object]],
    budgets: list[dict[str, object]],
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
    theorem_text = " ".join(f"{row['target']} {row['condition_or_formula']} {row['derivation_basis']} {row['meaning']}" for row in theorem)
    checks.append(("zero_contract_terms", "zero contract includes alpha_proj, B_boundary, B_edge, alpha_edge", all(term in theorem_text for term in ["alpha_proj=0", "B_boundary=0", "B_edge=0", "alpha_edge=0"]), ""))
    checks.append(("budget_formula", "budget theorem includes eta_R10 product gate", "eta_R10" in theorem_text and "2*(1-eta_R10)" in theorem_text, ""))
    checks.append(("budget_rows", "budget rows preserve 3703 candidate row count and positivity", len(budgets) >= 30 and all(float(row["alpha_bound_abs"]) > 0 and float(row["P_N_max_eta10_m4"]) > 0 for row in budgets), f"rows={len(budgets)}"))
    checks.append(("projection_verdict", "term verdict separates alpha_proj from edge/boundary", any(row["term"] == "alpha_proj" and "conditionallly_zero" in row["verdict"] for row in terms), ""))
    checks.append(("boundary_not_claimed", "boundary/edge terms remain unclaimed unless signed", any(row["term"] == "B_boundary" and "not_zero" in row["verdict"] for row in terms) and any(row["term"] == "B_edge" and "not_zero" in row["verdict"] for row in terms), ""))
    checks.append(("decisions_nonclaim", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3705", "next target advances to compact collar/projection certificate", str(next_target[0]["target_doc"]).startswith("3705-") and "collar" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core nuisance cleanup terms", all(term in doc_text for term in ["alpha_nuisance", "alpha_proj=0", "eta_R10", "compact fixed/no-flux collar", "valid_for_claim=false"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3704*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3704 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
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
    product_rows = read_product_rows()
    sources = source_register(timestamp)
    theorem = theorem_contract_rows(timestamp)
    terms = term_verdict_rows(timestamp)
    budgets = budget_rows(timestamp, product_rows)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp, budgets)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3704_SOURCE_REGISTER.csv",
        "theorem": RESIDUALS / "P8_Y5_R2FR_3704_NUISANCE_ZERO_THEOREM_CONTRACT_ROWS.csv",
        "terms": RESIDUALS / "P8_Y5_R2FR_3704_NUISANCE_TERM_VERDICT_ROWS.csv",
        "budgets": RESIDUALS / "P8_Y5_R2FR_3704_ALPHA_NUISANCE_BUDGET_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3704_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3704_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3704_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3704_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3704_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["terms"], terms)
    write_csv(outputs["budgets"], budgets)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, theorem, terms, budgets, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, theorem, terms, budgets, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3704 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3704 checkpoint: alpha_nuisance split into projection-zero contract plus edge/boundary budget runner")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
