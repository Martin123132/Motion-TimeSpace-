from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1529-Y5-parent-boundary-no-flux-zero-mode-certificate-or-lambda-phi-bound-inputs.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "reciprocity_attempt": ROOT / "05-reciprocity-theorem-attempt.md",
    "source_boundary": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "lambda_constraint": ROOT / "07-nonpropagating-reciprocity-constraint.md",
    "observer_symplectic": ROOT / "10-observer-map-symplectic-contract.md",
    "1007_doc": ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md",
    "1010_doc": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
    "1011_doc": ROOT / "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md",
    "1528_doc": ROOT / "1528-Y5-lambda-phi-silence-no-flux-or-multiplier-stress-bound.md",
    "1528_validation": OUT / "P8_Y5_BRR545_1528_VALIDATION.csv",
    "1528_theorem": OUT / "P8_Y5_PARENT_QLOC_1528_LAMBDA_PHI_ENERGY_THEOREM.csv",
    "1528_boundary": OUT / "P8_Y5_PARENT_QLOC_1528_BOUNDARY_ZERO_MODE_AUDIT.csv",
    "1528_stress": OUT / "P8_Y5_PARENT_QLOC_1528_MULTIPLIER_STRESS_BOUND_SCHEMA.csv",
    "1528_claim_gate": OUT / "P8_Y5_PARENT_QLOC_1528_CLAIM_GATE.csv",
    "1528_next": OUT / "P8_Y5_PARENT_QLOC_1528_NEXT_TARGET.csv",
    "1527_aux": OUT / "P8_Y5_PARENT_QLOC_1527_LOCAL_AUXILIARY_ACTION_CONTRACT.csv",
    "1527_khat": OUT / "P8_Y5_PARENT_QLOC_1527_KHAT_ADOPTION_ROW.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1529_SOURCE_REGISTER.csv"
CERTIFICATE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv"
BOUND_INPUTS = OUT / "P8_Y5_PARENT_QLOC_1529_LAMBDA_PHI_BOUND_INPUT_LEDGER.csv"
CERT_OR_BOUND_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1529_CERTIFICATE_OR_BOUND_RUNNER.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1529_REJECTION_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1529_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1529_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_QLOC_1529_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1529_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1529_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1529"
QUAR_CERT = QUARANTINE / "BOUNDARY_CERTIFICATE_AUDIT_NONCLAIM.csv"
QUAR_INPUTS = QUARANTINE / "LAMBDA_PHI_BOUND_INPUT_LEDGER_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "CERTIFICATE_OR_BOUND_RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_CERT = BRANCH_RESIDUALS / "lambda_phi_boundary_certificate_audit_nonclaim_1529.csv"
BRANCH_INPUTS = BRANCH_RESIDUALS / "lambda_phi_bound_input_ledger_nonclaim_1529.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "lambda_phi_certificate_or_bound_runner_nonclaim_1529.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "lambda_phi_decision_nonclaim_1529.csv"


def flags() -> dict[str, bool]:
    return {
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": f"SRC1529_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for lambda_phi boundary/no-flux certificate or multiplier-stress bound inputs",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def certificate_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BND1529_0_domain_certificate",
            "parent compact local collar D",
            "D, h_ij, boundary normal n^i, orientation, and local branch must be parent-defined before energy identity is live",
            "MISSING_PARENT_DOMAIN_CERTIFICATE",
            "no current source signs the lambda_phi domain",
            source_list("1528_boundary", "1010_doc"),
        ),
        (
            "BND1529_1_boundary_condition",
            "Dirichlet or Neumann/no-flux",
            "need either lambda_phi|boundary=0, or n.grad(lambda_phi)=0 plus zero-mode/reference condition",
            "MISSING_BOUNDARY_CONDITION_CERTIFICATE",
            "older boundary rows are conditional and cannot be imported",
            source_list("reciprocity_attempt", "source_boundary", "1007_doc"),
        ),
        (
            "BND1529_2_zero_mode_reference",
            "zero-mode fixing",
            "Neumann/no-flux requires mean(lambda_phi)=0 or a fixed reference value so constant lambda_phi cannot survive",
            "MISSING_ZERO_MODE_CERTIFICATE",
            "constant mode would still couple through lambda_phi S_Gamma",
            source_list("1528_theorem", "1527_aux"),
        ),
        (
            "BND1529_3_static_elliptic_owner",
            "Box-to-Delta_h reduction",
            "the local branch must be stationary/elliptic, not a Lorentzian free-wave multiplier problem",
            "MISSING_STATIC_BRANCH_CERTIFICATE",
            "energy proof is conditional without this",
            source_list("1528_theorem", "1010_doc"),
        ),
        (
            "BND1529_4_source_boundary_matching",
            "source/collar matching",
            "source boundary work must not inject lambda_phi flux or a boundary value",
            "MISSING_SOURCE_BOUNDARY_CERTIFICATE",
            "source matching was already a missing theorem in early reciprocity work",
            source_list("reciprocity_attempt", "source_boundary", "1011_doc"),
        ),
        (
            "BND1529_5_verdict",
            "boundary/no-flux certificate",
            "no parent-signed certificate found; the zero theorem cannot be promoted",
            "CERTIFICATE_NOT_FOUND",
            "must use bound-input route unless certificate is derived later",
            source_list("1528_claim_gate", "1528_validation"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "certificate_id": certificate_id,
            "target": target,
            "requirement": requirement,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": sources,
            **flags(),
        }
        for certificate_id, target, requirement, status, missing, sources in rows
    ]


def bound_input_rows() -> list[dict[str, Any]]:
    rows = [
        ("BIN1529_0_C_P", "C_P", "Poincare/zero-mode constant for lambda_phi on D", "dimensionless_or_length", "MISSING_BOUND_CONSTANT"),
        ("BIN1529_1_C_E", "C_E", "elliptic gradient estimate constant for lambda_phi", "dimensionless_or_length", "MISSING_BOUND_CONSTANT"),
        ("BIN1529_2_C_T", "C_T", "stress conversion constant for T_lambda_phi", "dimensionless", "MISSING_BOUND_CONSTANT"),
        ("BIN1529_3_R_norm", "||R||", "same-frame Ricci scalar norm in the local collar", "L^-2_or_geometric", "MISSING_SOURCE_NORM"),
        ("BIN1529_4_boundary_source_norm", "boundary_source_norm", "boundary/no-flux violation norm for lambda_phi", "lambda_phi_flux_units", "MISSING_BOUNDARY_NORM"),
        ("BIN1529_5_initial_data_norm", "initial_data_norm", "if hyperbolic branch is retained, lambda_phi initial data norm", "lambda_phi_units", "MISSING_INITIAL_DATA_NORM"),
        ("BIN1529_6_delta_g_SGamma_norm", "||delta_g S_Gamma||", "metric-response norm of S_Gamma=(2/3)(Gamma_eff+C)", "operator_norm", "MISSING_OPERATOR_NORM"),
        ("BIN1529_7_observable_projection", "Pi_gamma/P_loc/C_op projection", "map T_lambda_phi into S_total, q_loc_hat, and local observable channel", "mixed", "MISSING_OBSERVABLE_PROJECTION"),
        ("BIN1529_8_no_cancellation_guard", "absolute envelope", "abs-sum all multiplier contributions; no cancellation with K_L/Gamma pieces", "rule", "GUARD_WRITTEN"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": input_id,
            "quantity": quantity,
            "definition": definition,
            "units": units,
            "status": status,
            "source_paths": source_list("1528_stress", "1528_theorem", "1527_aux"),
            **flags(),
        }
        for input_id, quantity, definition, units, status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1529_0_certificate_route",
            "route": "promote lambda_phi=0 theorem",
            "required_inputs": "domain certificate; boundary/no-flux; zero-mode reference; static elliptic branch; source-boundary matching",
            "current_inputs": "all certificate clauses missing or precedent-only",
            "result": "BLOCKED_CERTIFICATE_NOT_FOUND",
            "next_required_object": "parent boundary/no-flux certificate",
            "source_paths": source_list("1528_boundary", "1007_doc"),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1529_1_bound_route",
            "route": "score retained multiplier stress",
            "required_inputs": "C_P; C_E; C_T; R_norm; boundary_source_norm; initial_data_norm; delta_g_SGamma_norm; observable projection",
            "current_inputs": "ledger exists but values are missing",
            "result": "BLOCKED_BOUND_INPUTS_MISSING",
            "next_required_object": "source-backed bound inputs",
            "source_paths": source_list("1528_stress", "1528_claim_gate"),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1529_2_Khat_route",
            "route": "promote staged Khat adoption",
            "required_inputs": "lambda_phi theorem-zero or finite bound accepted",
            "current_inputs": "lambda_phi unresolved",
            "result": "BLOCKED_NO_KHAT_PROMOTION",
            "next_required_object": "lambda_phi zero/bound decision",
            "source_paths": source_list("1527_khat", "1528_claim_gate"),
            **flags(),
        },
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1529_0_precedent_as_certificate", "treat older no-flux language as a certificate", "REJECTED", "source rows mark boundary/no-flux as conditional or missing"),
        ("REJ1529_1_choose_Dirichlet_by_hand", "impose lambda_phi=0 boundary by choice", "REJECTED", "would tune away a response unless parent-owned"),
        ("REJ1529_2_ignore_zero_mode", "accept Neumann/no-flux without zero-mode fixing", "REJECTED", "constant lambda_phi can still source metric response"),
        ("REJ1529_3_ignore_bound_values", "claim stress is bounded without constants/norms", "REJECTED", "bound route needs source-backed values"),
        ("REJ1529_4_promote_Khat", "promote Khat adoption before lambda_phi decision", "REJECTED", "multiplier stress remains unresolved"),
        ("REJ1529_5_score_local_GR", "score local GR/PPN now", "REJECTED", "local branch remains nonclaim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "shortcut": shortcut,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for rejection_id, shortcut, status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1529_0_certificate_audit", "boundary certificate audit completed", "PASS_NONCLAIM", "required clauses are identified"),
        ("GATE1529_1_boundary_certificate", "parent boundary/no-flux zero-mode certificate exists", "BLOCKED", "certificate not found"),
        ("GATE1529_2_bound_inputs", "source-backed multiplier bound inputs exist", "BLOCKED", "constants/norms/projection missing"),
        ("GATE1529_3_lambda_decision", "lambda_phi zero or bounded", "BLOCKED", "neither theorem nor bound route passes"),
        ("GATE1529_4_Khat_adoption", "Khat adoption can be promoted", "BLOCKED", "lambda_phi unresolved"),
        ("GATE1529_5_local_GR", "local GR/Newton/PPN recovery is claimable", "BLOCKED_NO_CLAIM", "q_loc local branch remains nonclaim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1529_0_no_certificate", "Do not promote lambda_phi silence.", "CERTIFICATE_NOT_FOUND", "boundary/no-flux and zero-mode clauses are missing."),
        ("DEC1529_1_bound_route", "Keep multiplier-stress bound route active.", "BOUND_INPUT_LEDGER_STAGED", "first concrete missing inputs are now named."),
        ("DEC1529_2_Khat_hold", "Keep Khat adoption staged, not live.", "KHAT_PROMOTION_BLOCKED", "lambda_phi theorem/bound is unresolved."),
        ("DEC1529_3_next", "Next target should source or estimate the bound inputs, starting with delta_g S_Gamma and domain constants.", "NEXT_1530_BOUND_INPUT_SOURCE_PASS", "this is more actionable than searching the same unsigned boundary language again."),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("LOCAL1529_0_boundary", "boundary/no-flux certificate", "NOT_FOUND", "required clauses identified but unsigned"),
        ("LOCAL1529_1_bound_inputs", "multiplier-stress inputs", "LEDGER_ONLY", "values missing"),
        ("LOCAL1529_2_lambda_phi", "lambda_phi zero/bound", "BLOCKED", "neither route passes"),
        ("LOCAL1529_3_Khat", "current Khat adoption", "NOT_PROMOTED", "lambda_phi unresolved"),
        ("LOCAL1529_4_GR", "derived local GR/Newton", "NOT_CLAIMED", "q_loc/DeltaK/C_op downstream"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "claim": claim,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for status_id, claim, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1529_0_1530",
            "next_target": "1530-Y5-lambda-phi-bound-input-source-pass.md",
            "script": "scripts/Y5_lambda_phi_bound_input_source_pass.py",
            "objective": "source or bound the first lambda_phi multiplier-stress inputs: delta_g_SGamma_norm, domain constants C_P/C_E/C_T, R_norm, boundary_source_norm, and observable projection into S_total/q_loc",
            "do_not": "do not repeat boundary precedent as proof; do not promote Khat adoption; do not score local GR/PPN; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (CERTIFICATE_AUDIT, QUAR_CERT),
        (BOUND_INPUTS, QUAR_INPUTS),
        (CERT_OR_BOUND_RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (CERTIFICATE_AUDIT, BRANCH_CERT),
        (BOUND_INPUTS, BRANCH_INPUTS),
        (CERT_OR_BOUND_RUNNER, BRANCH_RUNNER),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    cert = read_csv(CERTIFICATE_AUDIT)
    inputs = read_csv(BOUND_INPUTS)
    runners = read_csv(CERT_OR_BOUND_RUNNER)
    rejections = read_csv(REJECTION_LEDGER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    missing_inputs = [
        row for row in inputs if row["status"].startswith("MISSING")
    ]
    checks = [
        ("VAL1529_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1529 input source paths exist"),
        ("VAL1529_1_certificate_not_found", any(row["certificate_id"] == "BND1529_5_verdict" and row["status"] == "CERTIFICATE_NOT_FOUND" for row in cert), "boundary/no-flux certificate is not found"),
        ("VAL1529_2_zero_mode_clause", any(row["certificate_id"] == "BND1529_2_zero_mode_reference" and row["status"] == "MISSING_ZERO_MODE_CERTIFICATE" for row in cert), "zero-mode clause remains explicit"),
        ("VAL1529_3_bound_inputs_staged", len(inputs) >= 9 and len(missing_inputs) >= 7, "bound-input ledger stages missing constants/norms"),
        ("VAL1529_4_no_cancellation_guard", any(row["input_id"] == "BIN1529_8_no_cancellation_guard" and row["status"] == "GUARD_WRITTEN" for row in inputs), "absolute no-cancellation guard is written"),
        ("VAL1529_5_runners_blocked", all(row["result"].startswith("BLOCKED") for row in runners), "certificate/bound/Khat runners remain blocked"),
        ("VAL1529_6_rejections_guardrails", len(rejections) >= 6 and all(row["status"] == "REJECTED" for row in rejections), "unsafe shortcuts rejected"),
        ("VAL1529_7_claim_gates_block", any(row["gate_id"] == "GATE1529_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1529_8_decision_next", any(row["result"] == "NEXT_1530_BOUND_INPUT_SOURCE_PASS" for row in decisions), "decision selects bound input source pass next"),
        ("VAL1529_9_next_target", any("1530-Y5-lambda-phi-bound-input" in row["next_target"] for row in next_rows), "next target is lambda_phi bound input source pass"),
        ("VAL1529_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1529 CSVs parse cleanly"),
        ("VAL1529_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1529_12_branch_copies", all(path.exists() for path in [QUAR_CERT, QUAR_INPUTS, QUAR_RUNNER, QUAR_DECISION, BRANCH_CERT, BRANCH_INPUTS, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1529_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1529_14_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1529_15_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1529 finds no parent boundary certificate, stages lambda_phi bound inputs, keeps Khat/local-GR nonclaim, and selects bound-input sourcing next"
            if overall
            else "1529 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(output)


def write_doc(
    sources: list[dict[str, Any]],
    cert: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    local_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1529 - Parent Boundary No-Flux Zero-Mode Certificate or Lambda Phi Bound Inputs",
                "",
                "## Verdict",
                "- No parent-signed `lambda_phi` boundary/no-flux plus zero-mode certificate was found; older no-flux material remains precedent, not proof.",
                "- The certificate checklist is now explicit: parent domain, boundary condition, zero-mode reference, static elliptic branch, and source-boundary matching.",
                "- The fallback path is now concrete: source `C_P`, `C_E`, `C_T`, `R_norm`, `boundary_source_norm`, `initial_data_norm`, `delta_g_SGamma_norm`, and the observable projection.",
                "- `K_hat` adoption stays staged/nonclaim until `lambda_phi` is either theorem-zero or bounded.",
                "- No local-GR/Newton/PPN claim is promoted from 1529.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Boundary Certificate Audit",
                md_table(cert, ["certificate_id", "target", "requirement", "status", "missing_to_promote"]),
                "",
                "## Lambda Phi Bound Input Ledger",
                md_table(inputs, ["input_id", "quantity", "definition", "units", "status"]),
                "",
                "## Certificate Or Bound Runner",
                md_table(runners, ["runner_id", "route", "required_inputs", "current_inputs", "result", "next_required_object"]),
                "",
                "## Rejection Ledger",
                md_table(rejections, ["rejection_id", "shortcut", "status", "reason"]),
                "",
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Local GR / Newton Status",
                md_table(local_rows, ["status_id", "claim", "current_status", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    cert = certificate_audit_rows()
    inputs = bound_input_rows()
    runners = runner_rows()
    rejections = rejection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(CERTIFICATE_AUDIT, cert)
    write_csv(BOUND_INPUTS, inputs)
    write_csv(CERT_OR_BOUND_RUNNER, runners)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        CERTIFICATE_AUDIT,
        BOUND_INPUTS,
        CERT_OR_BOUND_RUNNER,
        REJECTION_LEDGER,
        CLAIM_GATE,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, cert, inputs, runners, rejections, gates, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()
