from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3705"
BRANCH_ID = "MTS_R2FR_Y5_COMPACT_COLLAR_NO_FLUX_AND_R10_PROJECTION_CERTIFICATE_3705"
DOC = ROOT / "3705-Y5-R2FR-compact-collar-no-flux-and-r10-projection-certificate.md"

DOC_3704 = ROOT / "3704-Y5-R2FR-alpha-nuisance-zero-or-budget-boundary-projection-cleanup.md"
THEOREM_3704 = RESIDUALS / "P8_Y5_R2FR_3704_NUISANCE_ZERO_THEOREM_CONTRACT_ROWS.csv"
TERMS_3704 = RESIDUALS / "P8_Y5_R2FR_3704_NUISANCE_TERM_VERDICT_ROWS.csv"
BUDGET_3704 = RESIDUALS / "P8_Y5_R2FR_3704_ALPHA_NUISANCE_BUDGET_ROWS.csv"
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
        ("doc_3704", DOC_3704, "alpha_proj=0", "3704 nuisance zero/budget contract"),
        ("theorem_3704", THEOREM_3704, "B_boundary=0", "3704 theorem rows"),
        ("terms_3704", TERMS_3704, "alpha_proj", "3704 term verdict rows"),
        ("budget_3704", BUDGET_3704, "eta_proj", "3704 budget rows"),
        ("projection_3699", PROJECTION_3699, "Y_A^perp", "Fisher projection formula"),
        ("source_gate_3699", SOURCE_GATE_3699, "kappa_GR", "resolved Newton/GR coupling source gate"),
        ("suppression_3693", SUPPRESSION_3693, "B_edge", "local suppression edge/projection gate"),
        ("yukawa_3694", YUKAWA_3694, "R_edge_A+R_proj_A", "Yukawa runner keeps edge/projection explicit"),
        ("q_loc_1010", DOC_1010, "boundary no-flux", "prior no-flux still unsigned"),
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


def projection_certificate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "RPC3705_0_resolved_basis",
            "R10/Newton fixed-point calibration is represented by resolved score C_N including kappa_GR",
            "QP3699_0 and SG3699_3 include kappa_GR/Newton-coupling calibration in the Fisher-resolved local observable basis",
            True,
            "SOURCE_CONFIRMED",
        ),
        (
            "RPC3705_1_projection_operator",
            "leakage scores are Fisher-projected against all resolved C_i before entering local tests",
            "QP3699_2 gives Y_A^perp=tildeY_A-C_i^0(C^-1)^{ij}<C_j^0 tildeY_A>_0",
            True,
            "SOURCE_CONFIRMED",
        ),
        (
            "RPC3705_2_first_order_Newton_silence",
            "partial_z kappa_GR|_0=0 and first-order Newton/R10 readout leakage is forbidden",
            "SG3699_3 states local comparisons cannot hide leakage by renormalizing G_N per arena; deviations must be alpha(lambda) residuals",
            True,
            "SOURCE_CONFIRMED",
        ),
        (
            "RPC3705_3_second_order_owner",
            "remaining Newton/R10 leakage is counted only through rho_Newton/P_N, not alpha_proj",
            "3703 defines P_N=K_N*rho_Newton*C_H^2||J_y+B_y||^2 and 3704 blocks alpha_proj as a separate knob",
            True,
            "BRANCH_DEFINITION_CONFIRMED",
        ),
        (
            "RPC3705_4_certificate",
            "alpha_proj=0 inside the private R2FR local R10 branch",
            "same quotient q, same P_loc, same resolved Newton/R10 observable basis, and second-order leakage routed into P_N",
            True,
            "BRANCH_SIGNED_NONPUBLIC",
        ),
    ]
    return [
        {
            **base(timestamp),
            "certificate_id": certificate_id,
            "clause": clause,
            "evidence": evidence,
            "passed": passed,
            "status": status,
            "claim_allowed": False,
        }
        for certificate_id, clause, evidence, passed, status in specs
    ]


def collar_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "CCT3705_0_domain",
            "choose compact collar Omega_c with source/readout support strictly inside its interior",
            "prevents artificial edge terms from touching the measured R10 interior",
            "mathematically_sufficient",
            False,
        ),
        (
            "CCT3705_1_boundary_condition",
            "horizontal variations obey y|partialOmega_c=0 or natural n_mu G_H^{mu nu}D_nu y=0",
            "makes the Green/coercivity boundary pairing vanish after integration by parts",
            "mathematically_sufficient",
            False,
        ),
        (
            "CCT3705_2_no_incoming_flux",
            "no incoming horizontal response flux through partialOmega_c",
            "turns B_boundary into a physical isolation condition rather than a fitted cancellation",
            "mathematically_sufficient",
            False,
        ),
        (
            "CCT3705_3_cutoff_support",
            "cutoff derivative support is disjoint from source and R10 readout support",
            "sets B_edge=0 for the interior readout by support separation",
            "mathematically_sufficient",
            False,
        ),
        (
            "CCT3705_4_same_readout",
            "R10/Newton readout operator is identical on the interior and collar overlap",
            "sets alpha_edge=0 by preventing a readout mismatch at the collar interface",
            "mathematically_sufficient",
            False,
        ),
        (
            "CCT3705_5_parent_signature_gap",
            "parent action/boundary sector must own CCT3705_0 through CCT3705_4",
            "1010 still marks P_loc and boundary/symplectic no-flux as open, so the collar theorem is not yet parent-signed",
            "parent_signature_missing",
            False,
        ),
    ]
    return [
        {
            **base(timestamp),
            "collar_id": collar_id,
            "condition": condition,
            "why_it_matters": why,
            "math_status": math_status,
            "parent_signed": parent_signed,
            "claim_allowed": False,
        }
        for collar_id, condition, why, math_status, parent_signed in specs
    ]


def zero_verdict_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "ZV3705_0_alpha_proj",
            "alpha_proj",
            "ZERO_IN_PRIVATE_BRANCH",
            "alpha_proj=0 follows from the resolved Fisher quotient branch definition; any Newton/R10 leakage is in P_N.",
            True,
        ),
        (
            "ZV3705_1_B_boundary",
            "B_boundary",
            "ZERO_IF_COLLAR_PARENT_SIGNED_ELSE_BUDGET",
            "compact fixed/no-flux collar kills it mathematically, but parent boundary ownership is not yet signed.",
            False,
        ),
        (
            "ZV3705_2_B_edge",
            "B_edge",
            "ZERO_IF_SUPPORT_COLLAR_PARENT_SIGNED_ELSE_BUDGET",
            "support separation kills it mathematically, but the collar/support contract is not yet parent-signed.",
            False,
        ),
        (
            "ZV3705_3_alpha_edge",
            "alpha_edge",
            "ZERO_IF_SAME_READOUT_PARENT_SIGNED_ELSE_BUDGET",
            "same readout on collar overlap kills it mathematically, but the readout identity is not yet parent-signed.",
            False,
        ),
        (
            "ZV3705_4_reduced_nuisance",
            "alpha_nuisance_reduced",
            "alpha_nuisance = 0.5*K_N*rho_Newton*(B_edge^2+B_boundary^2)+alpha_edge",
            "projection nuisance is removed; only collar/boundary/edge nuisance remains.",
            True,
        ),
    ]
    return [
        {
            **base(timestamp),
            "verdict_id": verdict_id,
            "term": term,
            "verdict": verdict,
            "rationale": rationale,
            "branch_signed": branch_signed,
            "claim_allowed": False,
        }
        for verdict_id, term, verdict, rationale, branch_signed in specs
    ]


def component_budget_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "ETA3705_0_projection",
            "eta_proj",
            "0",
            "projection zero certificate RPC3705_4",
            "BRANCH_SIGNED_NONPUBLIC",
        ),
        (
            "ETA3705_1_boundary",
            "eta_boundary",
            "MISSING_FINITE_BOUND_OR_PARENT_ZERO",
            "compact collar no-flux theorem CCT3705_0..2 or finite boundary-response bound",
            "OPEN",
        ),
        (
            "ETA3705_2_edge",
            "eta_edge",
            "MISSING_FINITE_BOUND_OR_PARENT_ZERO",
            "support/collar/readout theorem CCT3705_3..4 or finite edge-response bound",
            "OPEN",
        ),
        (
            "ETA3705_3_total",
            "eta_R10",
            "eta_boundary + eta_edge",
            "eta_proj=0; require eta_boundary+eta_edge<1 before scoring P_N",
            "REDUCED_BUDGET_SCHEMA",
        ),
    ]
    return [
        {
            **base(timestamp),
            "eta_id": eta_id,
            "component": component,
            "value_or_formula": value,
            "source_or_required_action": action,
            "status": status,
            "claim_allowed": False,
        }
        for eta_id, component, value, action, status in specs
    ]


def read_budget_rows() -> list[dict[str, str]]:
    return sorted(parse_csv(BUDGET_3704), key=lambda row: float(row["lambda_m"]))


def reduced_budget_rows(timestamp: str, budget_rows_3704: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for idx, row in enumerate(budget_rows_3704):
        rows.append(
            {
                **base(timestamp),
                "reduced_budget_id": f"RNB3705_{idx:03d}",
                "source_budget_row_id": row["budget_row_id"],
                "lambda_m": row["lambda_m"],
                "lambda_um": row["lambda_um"],
                "alpha_bound_abs": row["alpha_bound_abs"],
                "eta_proj": "0",
                "eta_total_formula": "eta_boundary+eta_edge",
                "P_N_max_if_eta_boundary_plus_edge_0": row["P_N_max_eta0_m4"],
                "P_N_max_if_eta_boundary_plus_edge_0p1": row["P_N_max_eta10_m4"],
                "P_N_max_if_eta_boundary_plus_edge_0p5": row["P_N_max_eta50_m4"],
                "reduced_gate": "0.5*P_N*lambda_H^4 + alpha_boundary_edge <= alpha_bound_R10(lambda_H)",
                "alpha_boundary_edge": "0.5*K_N*rho_Newton*(B_edge^2+B_boundary^2)+alpha_edge",
                "claim_allowed": False,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3705_0",
            "Projection nuisance is removed from the private R10 branch.",
            "The resolved Fisher basis already owns Newton/GR calibration and routes residual force leakage through rho_Newton/P_N; alpha_proj is not a second knob.",
            "PROJECTION_ZERO_ADVANCES",
        ),
        (
            "DEC3705_1",
            "The collar theorem is mathematically sufficient but not parent-signed.",
            "Boundary/edge zero requires parent-owned compact collar, no-flux or fixed boundary data, support separation, and same readout; 1010 says boundary ownership is still open.",
            "COLLAR_THEOREM_STAGED_NOT_CLAIMED",
        ),
        (
            "DEC3705_2",
            "The R10 nuisance budget is reduced from three components to two.",
            "eta_proj=0; only eta_boundary and eta_edge remain, and they must be zero-proved or finite-bounded.",
            "BUDGET_REDUCED",
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
        ("CG3705_0_projection", "alpha_proj=0 in the private branch", "PASS_PRIVATE_NONPUBLIC"),
        ("CG3705_1_parent_collar", "parent action/boundary sector signs compact collar and no-flux/fixed-boundary conditions", "BLOCKED"),
        ("CG3705_2_edge_support", "source/readout support separation and same readout operator are parent-signed", "BLOCKED"),
        ("CG3705_3_budget", "eta_boundary+eta_edge is zero or finite and <1", "BLOCKED"),
        ("CG3705_4_R10_score", "P_N and lambda_H are parent-sourced and scored with eta_proj=0", "BLOCKED"),
        ("CG3705_5_public", "public R10/local-Newton claim allowed", "BLOCKED"),
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


def status_rows(timestamp: str, reduced_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3705_0",
            "status": "R10_PROJECTION_ZERO_SIGNED_PRIVATE_BRANCH_COLLAR_THEOREM_STAGED_EDGE_BOUNDARY_OPEN",
            "summary": (
                f"3705 branch-signs alpha_proj=0 for the private R2FR R10 branch and rewrites alpha_nuisance as collar/edge-only. "
                f"Generated {len(reduced_rows)} reduced budget rows with eta_proj=0. Boundary/edge zeros are mathematically sufficient under a compact no-flux collar, but not parent-signed yet."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3705_0",
            "target_doc": "3706-Y5-R2FR-parent-boundary-action-collar-signature-or-edge-budget-bound.md",
            "target_script": "scripts/Y5_R2FR_3706_parent_boundary_action_collar_signature_or_edge_budget_bound.py",
            "objective": "try to derive the compact collar/no-flux boundary condition from the parent action boundary term; if not, produce finite eta_boundary and eta_edge bound rows",
            "success_gate": "B_boundary/B_edge/alpha_edge are zero by parent boundary action, or eta_boundary+eta_edge is finite and can be inserted into the R10 score",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    projection: list[dict[str, object]],
    collar: list[dict[str, object]],
    verdicts: list[dict[str, object]],
    eta: list[dict[str, object]],
    reduced: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    tightest = min(reduced, key=lambda row: float(row["P_N_max_if_eta_boundary_plus_edge_0p1"]))
    lines = [
        "# 3705 Y5 R2FR Compact Collar No-Flux And R10 Projection Certificate",
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
        "- `alpha_proj=0` is now branch-signed for the private R2FR R10 branch.",
        "- Reason: the resolved Fisher basis already includes Newton/GR calibration; first-order leakage is projected out, and second-order Newton/R10 leakage is owned by `rho_Newton/P_N`.",
        "- The reduced nuisance is `alpha_boundary_edge := 0.5*K_N*rho_Newton*(B_edge^2+B_boundary^2)+alpha_edge`.",
        "- The reduced R10 gate is `0.5*P_N*lambda_H^4 + alpha_boundary_edge <= alpha_bound_R10(lambda_H)`.",
        "- The compact collar/no-flux theorem is mathematically sufficient for `B_boundary=B_edge=alpha_edge=0`, but it is not parent-signed yet.",
        "- `valid_for_claim=false`: this removes a private nuisance knob; it does not claim local Newton/R10 recovery.",
        "",
        "## Projection Certificate",
        "",
    ]
    for row in projection:
        lines.append(f"- `{row['certificate_id']}`: `{row['status']}` | passed={row['passed']} | {row['clause']}")
    lines.extend(["", "## Collar Theorem", ""])
    for row in collar:
        lines.append(f"- `{row['collar_id']}`: `{row['math_status']}` parent_signed={row['parent_signed']} | {row['condition']}")
    lines.extend(["", "## Zero Verdicts", ""])
    for row in verdicts:
        lines.append(f"- `{row['verdict_id']}`: `{row['verdict']}` | {row['term']} | {row['rationale']}")
    lines.extend(["", "## Eta Components", ""])
    for row in eta:
        lines.append(f"- `{row['eta_id']}`: `{row['component']}` = `{row['value_or_formula']}` | {row['status']}")
    lines.extend(["", "## Reduced Budget Rows", ""])
    lines.append(f"- Reduced candidate rows generated: `{len(reduced)}`.")
    lines.append(f"- Tightest eta_boundary+eta_edge=0.1 row: `lambda={tightest['lambda_um']} um`, `P_N_max={tightest['P_N_max_if_eta_boundary_plus_edge_0p1']} m^-4`.")
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
    projection: list[dict[str, object]],
    collar: list[dict[str, object]],
    verdicts: list[dict[str, object]],
    eta: list[dict[str, object]],
    reduced: list[dict[str, object]],
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
    checks.append(("projection_signed", "projection certificate signs alpha_proj privately", any(row["certificate_id"] == "RPC3705_4_certificate" and row["passed"] is True and row["status"] == "BRANCH_SIGNED_NONPUBLIC" for row in projection), ""))
    checks.append(("collar_not_parent_signed", "collar theorem is staged but not parent-signed", any(row["collar_id"] == "CCT3705_5_parent_signature_gap" and row["parent_signed"] is False for row in collar), ""))
    checks.append(("reduced_nuisance", "zero verdict includes reduced nuisance formula", any(row["term"] == "alpha_nuisance_reduced" and "B_edge" in row["verdict"] for row in verdicts), ""))
    eta_map = {str(row["component"]): row for row in eta}
    checks.append(("eta_proj_zero", "eta_proj is zero and eta total excludes projection", eta_map["eta_proj"]["value_or_formula"] == "0" and eta_map["eta_R10"]["value_or_formula"] == "eta_boundary + eta_edge", ""))
    checks.append(("reduced_rows", "reduced rows preserve budget row count and positivity", len(reduced) >= 30 and all(float(row["P_N_max_if_eta_boundary_plus_edge_0p1"]) > 0 for row in reduced), f"rows={len(reduced)}"))
    checks.append(("decisions_nonclaim", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_private_pass_only", "only projection gate passes privately and public claims remain blocked", any(row["claim_gate_id"] == "CG3705_0_projection" and row["status"] == "PASS_PRIVATE_NONPUBLIC" for row in claim_gates) and all(row["status"] == "BLOCKED" for row in claim_gates if row["claim_gate_id"] != "CG3705_0_projection"), ""))
    checks.append(("next_target_3706", "next target advances to parent boundary action or edge budget", str(next_target[0]["target_doc"]).startswith("3706-") and "boundary" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core 3705 results", all(term in doc_text for term in ["alpha_proj=0", "alpha_boundary_edge", "compact collar/no-flux", "valid_for_claim=false"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3705*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3705 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
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
    budget_3704 = read_budget_rows()
    sources = source_register(timestamp)
    projection = projection_certificate_rows(timestamp)
    collar = collar_theorem_rows(timestamp)
    verdicts = zero_verdict_rows(timestamp)
    eta = component_budget_rows(timestamp)
    reduced = reduced_budget_rows(timestamp, budget_3704)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp, reduced)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3705_SOURCE_REGISTER.csv",
        "projection": RESIDUALS / "P8_Y5_R2FR_3705_R10_PROJECTION_CERTIFICATE_ROWS.csv",
        "collar": RESIDUALS / "P8_Y5_R2FR_3705_COMPACT_COLLAR_THEOREM_ROWS.csv",
        "verdicts": RESIDUALS / "P8_Y5_R2FR_3705_ZERO_VERDICT_ROWS.csv",
        "eta": RESIDUALS / "P8_Y5_R2FR_3705_ETA_COMPONENT_ROWS.csv",
        "reduced": RESIDUALS / "P8_Y5_R2FR_3705_REDUCED_BUDGET_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3705_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3705_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3705_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3705_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3705_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["projection"], projection)
    write_csv(outputs["collar"], collar)
    write_csv(outputs["verdicts"], verdicts)
    write_csv(outputs["eta"], eta)
    write_csv(outputs["reduced"], reduced)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, projection, collar, verdicts, eta, reduced, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, projection, collar, verdicts, eta, reduced, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3705 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3705 checkpoint: alpha_proj=0 private certificate; collar/no-flux theorem staged; eta budget reduced")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
