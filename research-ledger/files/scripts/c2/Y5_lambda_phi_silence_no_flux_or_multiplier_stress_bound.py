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
DOC = ROOT / "1528-Y5-lambda-phi-silence-no-flux-or-multiplier-stress-bound.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "reciprocity_attempt": ROOT / "05-reciprocity-theorem-attempt.md",
    "source_boundary": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "lambda_constraint": ROOT / "07-nonpropagating-reciprocity-constraint.md",
    "observer_symplectic": ROOT / "10-observer-map-symplectic-contract.md",
    "1007_doc": ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md",
    "1010_doc": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
    "1011_doc": ROOT / "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md",
    "1527_doc": ROOT / "1527-Y5-phi-owner-and-current-Khat-symbol-match-source-hunt.md",
    "1527_validation": OUT / "P8_Y5_BRR545_1527_VALIDATION.csv",
    "1527_aux": OUT / "P8_Y5_PARENT_QLOC_1527_LOCAL_AUXILIARY_ACTION_CONTRACT.csv",
    "1527_multiplier": OUT / "P8_Y5_PARENT_QLOC_1527_MULTIPLIER_STRESS_SILENCE_GATE.csv",
    "1527_khat": OUT / "P8_Y5_PARENT_QLOC_1527_KHAT_ADOPTION_ROW.csv",
    "1527_claim_gate": OUT / "P8_Y5_PARENT_QLOC_1527_CLAIM_GATE.csv",
    "1527_next": OUT / "P8_Y5_PARENT_QLOC_1527_NEXT_TARGET.csv",
    "1526_contract": OUT / "P8_Y5_PARENT_QLOC_1526_COEFFICIENT_SIGN_CONTRACT.csv",
    "1526_variation": OUT / "P8_Y5_PARENT_QLOC_1526_VARIATION_DERIVATION.csv",
    "gk_contract": OUT / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1528_SOURCE_REGISTER.csv"
ENERGY_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1528_LAMBDA_PHI_ENERGY_THEOREM.csv"
BOUNDARY_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1528_BOUNDARY_ZERO_MODE_AUDIT.csv"
STRESS_BOUND = OUT / "P8_Y5_PARENT_QLOC_1528_MULTIPLIER_STRESS_BOUND_SCHEMA.csv"
THEOREM_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1528_THEOREM_OR_BOUND_RUNNER.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1528_REJECTION_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1528_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1528_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_QLOC_1528_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1528_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1528_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1528"
QUAR_THEOREM = QUARANTINE / "LAMBDA_PHI_ENERGY_THEOREM_NONCLAIM.csv"
QUAR_BOUNDARY = QUARANTINE / "BOUNDARY_ZERO_MODE_AUDIT_NONCLAIM.csv"
QUAR_STRESS = QUARANTINE / "MULTIPLIER_STRESS_BOUND_SCHEMA_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_THEOREM = BRANCH_RESIDUALS / "lambda_phi_energy_theorem_nonclaim_1528.csv"
BRANCH_BOUNDARY = BRANCH_RESIDUALS / "lambda_phi_boundary_zero_mode_audit_nonclaim_1528.csv"
BRANCH_STRESS = BRANCH_RESIDUALS / "lambda_phi_multiplier_stress_bound_nonclaim_1528.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "lambda_phi_decision_nonclaim_1528.csv"


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
            "source_id": f"SRC1528_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for lambda_phi silence/no-flux theorem or multiplier-stress bound",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def energy_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LPE1528_0_multiplier_equation",
            "lambda_phi equation",
            "from 1527, Box lambda_phi=-c_I R plus convention/boundary terms",
            "EQUATION_IMPORTED",
            "sign convention and boundary terms still inherited from S_phiK",
            source_list("1527_aux", "1527_multiplier"),
        ),
        (
            "LPE1528_1_static_elliptic_reduction",
            "local compact static branch",
            "for stationary local branch, Box lambda_phi reduces to +/- Delta_h lambda_phi on the spatial collar",
            "ELLIPTIC_REDUCTION_REQUIRED",
            "not parent-signed; Lorentzian hyperbolic data would need a different energy theorem",
            source_list("1010_doc", "1527_claim_gate"),
        ),
        (
            "LPE1528_2_Ricci_flat_harmonic",
            "Ricci-flat/local vacuum condition",
            "if R=0, then Delta_h lambda_phi=0 on the compact local collar",
            "CONDITIONAL_HARMONIC_EQUATION",
            "Ricci-flat/local vacuum branch must be the same branch used for the GR reduction, not assumed post-hoc",
            source_list("1527_multiplier", "gk_contract"),
        ),
        (
            "LPE1528_3_energy_identity",
            "harmonic energy identity",
            "int_D |grad lambda_phi|_h^2 dV = int_boundary lambda_phi n.grad(lambda_phi) dS - int_D lambda_phi Delta_h lambda_phi dV",
            "ENERGY_IDENTITY_DERIVED",
            "requires positive spatial metric/domain and differentiable boundary data",
            source_list("1007_doc", "1010_doc"),
        ),
        (
            "LPE1528_4_zero_gradient_condition",
            "gradient silence",
            "if Delta_h lambda_phi=0 and the boundary flux term vanishes, then grad lambda_phi=0",
            "CONDITIONAL_GRADIENT_ZERO",
            "gradient zero alone leaves a constant zero mode",
            source_list("1527_multiplier", "source_boundary"),
        ),
        (
            "LPE1528_5_zero_mode_condition",
            "constant mode removal",
            "lambda_phi=0 follows only with Dirichlet lambda_phi|boundary=0, or Neumann/no-flux plus zero-mean/reference normalization",
            "ZERO_MODE_GUARD_REQUIRED",
            "constant lambda_phi can still multiply metric-dependent S_Gamma and is not automatically harmless",
            source_list("1527_aux", "1527_khat"),
        ),
        (
            "LPE1528_6_theorem_shape",
            "lambda_phi silence theorem",
            "Ricci-flat + static elliptic collar + parent boundary/no-flux + zero-mode fixing imply lambda_phi=0 and T_lambda_phi=0",
            "THEOREM_SHAPE_WRITTEN_NOT_SIGNED",
            "boundary/no-flux, zero-mode, and branch-owner certificates are missing",
            source_list("1527_claim_gate", "1010_doc"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "object": obj,
            "formula_or_statement": formula,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": sources,
            **flags(),
        }
        for theorem_id, obj, formula, status, missing, sources in rows
    ]


def boundary_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BZA1528_0_domain_owner",
            "compact local collar/domain D",
            "parent-owned domain with positive spatial metric h_ij and boundary normal",
            "MISSING_PARENT_DOMAIN_CERTIFICATE",
            "needed for the elliptic identity",
        ),
        (
            "BZA1528_1_Dirichlet_route",
            "lambda_phi|boundary=0",
            "Dirichlet boundary would kill the boundary term and constant mode",
            "NOT_SOURCED",
            "cannot impose because it may tune away a physical response",
        ),
        (
            "BZA1528_2_Neumann_route",
            "n.grad(lambda_phi)|boundary=0",
            "Neumann/no-flux kills boundary flux but leaves constant mode",
            "ZERO_MEAN_STILL_REQUIRED",
            "must also parent-fix mean(lambda_phi)=0 or a reference value",
        ),
        (
            "BZA1528_3_asymptotic_route",
            "lambda_phi -> 0 at infinity",
            "asymptotic decay can remove the constant mode in exterior noncompact limit",
            "NOT_CURRENT_COMPACT_PROOF",
            "needs falloff, finite energy, and source-boundary matching",
        ),
        (
            "BZA1528_4_boundary_flux_precedent",
            "prior boundary/no-flux materials",
            "older boundary and symplectic rows repeatedly treat no-flux as conditional and unsigned",
            "PRECEDENT_NOT_CERTIFICATE",
            "cannot promote lambda_phi silence from precedent alone",
        ),
        (
            "BZA1528_5_verdict",
            "boundary zero-mode audit",
            "no parent-signed boundary/zero-mode certificate exists for lambda_phi",
            "BOUNDARY_ZERO_MODE_BLOCKED",
            "lambda_phi theorem remains nonclaim",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "target": target,
            "condition": condition,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("reciprocity_attempt", "source_boundary", "1007_doc", "1010_doc", "1011_doc"),
            **flags(),
        }
        for audit_id, target, condition, status, missing in rows
    ]


def stress_bound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "MSB1528_0_lambda_norm",
            "||lambda_phi||",
            "||lambda_phi|| <= C_P(|c_I| ||R|| + boundary_source_norm + initial_data_norm)",
            "SYMBOLIC_BOUND_SCHEMA",
            "C_P, R norm, boundary source, initial data not sourced",
        ),
        (
            "MSB1528_1_gradient_norm",
            "||grad lambda_phi||",
            "||grad lambda_phi|| <= C_E(|c_I| ||R|| + boundary_source_norm + initial_data_norm)",
            "SYMBOLIC_BOUND_SCHEMA",
            "C_E and same-frame norms missing",
        ),
        (
            "MSB1528_2_stress_norm",
            "||T_lambda_phi||",
            "||T_lambda_phi|| <= C_T(||grad lambda_phi||^2 + ||lambda_phi|| ||delta_g S_Gamma||)",
            "SYMBOLIC_BOUND_SCHEMA",
            "delta_g S_Gamma operator norm and constants missing",
        ),
        (
            "MSB1528_3_q_loc_injection",
            "lambda_phi contribution to S_total/q_loc",
            "S_total gains S_lambda unless lambda_phi=0; use absolute-sum no-cancellation envelope",
            "RETAIN_IF_THEOREM_FAILS",
            "needs observable projection and C_op/q_loc normalization",
        ),
        (
            "MSB1528_4_verdict",
            "multiplier-stress fallback",
            "fallback schema is ready but has no numeric/source-backed values",
            "BOUND_SCHEMA_ONLY",
            "not scoreable",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_id": bound_id,
            "quantity": quantity,
            "bound_formula": formula,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("1527_multiplier", "1526_contract", "1527_claim_gate"),
            **flags(),
        }
        for bound_id, quantity, formula, status, missing in rows
    ]


def theorem_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1528_0_lambda_phi_zero_theorem",
            "route": "prove lambda_phi=0",
            "required_inputs": "static elliptic reduction; R=0 same branch; parent domain; boundary/no-flux; zero-mode fixing; no hidden source",
            "current_inputs": "harmonic theorem shape only; boundary/no-flux and zero-mode unsigned",
            "result": "BLOCKED_NOT_ZERO_PROVEN",
            "fallback": "retain multiplier-stress bound schema",
            "source_paths": source_list("1527_multiplier", "1010_doc"),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1528_1_multiplier_bound",
            "route": "bound retained T_lambda_phi",
            "required_inputs": "C_P, C_E, C_T, R norm, boundary source norm, delta_g S_Gamma norm, observable projection",
            "current_inputs": "symbolic schema only",
            "result": "BLOCKED_BOUND_VALUES_MISSING",
            "fallback": "next source/bound input target",
            "source_paths": source_list("1527_claim_gate", "gk_contract"),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1528_2_Khat_adoption",
            "route": "promote staged Khat=K_L adoption",
            "required_inputs": "lambda_phi zero/bound resolved plus c_I/sign/boundary/current adoption",
            "current_inputs": "lambda_phi not silent and adoption staged",
            "result": "BLOCKED_NO_KHAT_PROMOTION",
            "fallback": "do not score local GR",
            "source_paths": source_list("1527_khat", "1527_claim_gate"),
            **flags(),
        },
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1528_0_harmonic_equals_zero", "claim harmonic lambda_phi is zero", "REJECTED", "harmonic functions include constant/zero modes unless boundary/reference fixes them"),
        ("REJ1528_1_gradient_zero_enough", "claim grad lambda_phi=0 removes all stress", "REJECTED", "constant lambda_phi can still multiply metric-dependent S_Gamma"),
        ("REJ1528_2_assume_Ricci_flat", "use R=0 as an input to prove local GR without branch certificate", "REJECTED", "must be same parent local-vacuum branch, not circular GR import"),
        ("REJ1528_3_boundary_by_precedent", "import older no-flux language as certificate", "REJECTED", "prior boundary rows are conditional/unsigned"),
        ("REJ1528_4_promote_Khat", "promote staged Khat adoption before lambda_phi silence", "REJECTED", "multiplier stress remains active"),
        ("REJ1528_5_score_local_GR", "score local GR/PPN now", "REJECTED", "q_loc_hat/DeltaK/C_op still blocked"),
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
        ("GATE1528_0_energy_identity", "lambda_phi energy identity is written", "PASS_NONCLAIM", "exact theorem shape recorded"),
        ("GATE1528_1_elliptic_branch", "static elliptic branch is parent-signed", "BLOCKED", "branch reduction from Box to Delta_h not sourced"),
        ("GATE1528_2_boundary_zero_mode", "boundary/no-flux plus zero-mode certificate exists", "BLOCKED", "no parent boundary certificate"),
        ("GATE1528_3_lambda_zero", "lambda_phi=0 is proved", "BLOCKED", "zero-mode and boundary conditions unsigned"),
        ("GATE1528_4_multiplier_bound", "retained multiplier stress is bounded", "BLOCKED", "numeric/source-backed constants missing"),
        ("GATE1528_5_Khat_adoption", "current Khat adoption can be promoted", "BLOCKED", "lambda_phi silence/bound unresolved"),
        ("GATE1528_6_local_GR", "local GR/Newton/PPN recovery is claimable", "BLOCKED_NO_CLAIM", "q_loc local branch remains nonclaim"),
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
        (
            "DEC1528_0_theorem_gain",
            "Keep the lambda_phi energy theorem shape.",
            "THEOREM_SHAPE_GAIN",
            "we now know exactly which conditions imply lambda_phi=0.",
        ),
        (
            "DEC1528_1_zero_not_claimed",
            "Do not claim multiplier silence.",
            "ZERO_BLOCKED",
            "the zero-mode and boundary/no-flux certificates are not parent-signed.",
        ),
        (
            "DEC1528_2_bound_fallback",
            "Retain a multiplier-stress bound schema if zero theorem fails.",
            "BOUND_SCHEMA_STAGED",
            "this keeps the auxiliary fix honest rather than hiding a new residual.",
        ),
        (
            "DEC1528_3_next",
            "Next target is parent boundary/no-flux zero-mode certificate or first numeric multiplier-stress bound inputs.",
            "NEXT_1529_BOUNDARY_OR_BOUND_INPUTS",
            "that is the shortest route to promote or safely bound Khat adoption.",
        ),
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
        ("LOCAL1528_0_lambda_theorem", "lambda_phi silence", "THEOREM_SHAPE_ONLY", "energy identity written but not parent-signed"),
        ("LOCAL1528_1_boundary", "boundary/no-flux", "BLOCKED", "zero-mode certificate missing"),
        ("LOCAL1528_2_stress", "multiplier stress", "BOUND_SCHEMA_ONLY", "no numeric/source values"),
        ("LOCAL1528_3_Khat", "current K_hat adoption", "NOT_PROMOTED", "lambda_phi gate unresolved"),
        ("LOCAL1528_4_GR", "derived local GR/Newton", "NOT_CLAIMED", "q_loc/DeltaK/C_op downstream"),
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
            "next_id": "NEXT1528_0_1529",
            "next_target": "1529-Y5-parent-boundary-no-flux-zero-mode-certificate-or-lambda-phi-bound-inputs.md",
            "script": "scripts/Y5_parent_boundary_no_flux_zero_mode_certificate_or_lambda_phi_bound_inputs.py",
            "objective": "derive a parent boundary/no-flux plus zero-mode certificate for lambda_phi, or fill first source-backed multiplier-stress bound inputs C_P, C_E, C_T, R_norm, boundary_source_norm, and delta_g_SGamma_norm",
            "do_not": "do not claim harmonic implies zero; do not promote Khat adoption; do not score local GR/PPN; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (ENERGY_THEOREM, QUAR_THEOREM),
        (BOUNDARY_AUDIT, QUAR_BOUNDARY),
        (STRESS_BOUND, QUAR_STRESS),
        (DECISION, QUAR_DECISION),
        (ENERGY_THEOREM, BRANCH_THEOREM),
        (BOUNDARY_AUDIT, BRANCH_BOUNDARY),
        (STRESS_BOUND, BRANCH_STRESS),
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
    theorem = read_csv(ENERGY_THEOREM)
    boundary = read_csv(BOUNDARY_AUDIT)
    stress = read_csv(STRESS_BOUND)
    runner = read_csv(THEOREM_RUNNER)
    rejections = read_csv(REJECTION_LEDGER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1528_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1528 input source paths exist"),
        ("VAL1528_1_energy_identity", any(row["theorem_id"] == "LPE1528_3_energy_identity" and row["status"] == "ENERGY_IDENTITY_DERIVED" for row in theorem), "lambda_phi energy identity is written"),
        ("VAL1528_2_zero_mode_guard", any(row["theorem_id"] == "LPE1528_5_zero_mode_condition" and row["status"] == "ZERO_MODE_GUARD_REQUIRED" for row in theorem), "zero-mode guard is explicit"),
        ("VAL1528_3_theorem_not_signed", any(row["theorem_id"] == "LPE1528_6_theorem_shape" and row["status"] == "THEOREM_SHAPE_WRITTEN_NOT_SIGNED" for row in theorem), "lambda_phi zero theorem remains unsigned"),
        ("VAL1528_4_boundary_blocked", any(row["audit_id"] == "BZA1528_5_verdict" and row["status"] == "BOUNDARY_ZERO_MODE_BLOCKED" for row in boundary), "boundary zero-mode certificate is blocked"),
        ("VAL1528_5_bound_schema", any(row["bound_id"] == "MSB1528_4_verdict" and row["status"] == "BOUND_SCHEMA_ONLY" for row in stress), "multiplier-stress fallback schema exists but is nonclaim"),
        ("VAL1528_6_runner_blocked", all(row["result"].startswith("BLOCKED") for row in runner), "zero/bound/Khat runners remain blocked"),
        ("VAL1528_7_rejections_guardrails", len(rejections) >= 6 and all(row["status"] == "REJECTED" for row in rejections), "unsafe shortcuts rejected"),
        ("VAL1528_8_claim_gates_block", any(row["gate_id"] == "GATE1528_6_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1528_9_decision_next", any(row["result"] == "NEXT_1529_BOUNDARY_OR_BOUND_INPUTS" for row in decisions), "decision selects boundary/no-flux or bound inputs next"),
        ("VAL1528_10_next_target", any("1529-Y5-parent-boundary" in row["next_target"] for row in next_rows), "next target is 1529 boundary/no-flux zero-mode or bound inputs"),
        ("VAL1528_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1528 CSVs parse cleanly"),
        ("VAL1528_12_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1528_13_branch_copies", all(path.exists() for path in [QUAR_THEOREM, QUAR_BOUNDARY, QUAR_STRESS, QUAR_DECISION, BRANCH_THEOREM, BRANCH_BOUNDARY, BRANCH_STRESS, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1528_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1528_15_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1528_16_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1528 writes the lambda_phi energy theorem shape, blocks zero-mode/no-flux promotion, stages multiplier-stress bounds, and selects boundary certificate or bound inputs next"
            if overall
            else "1528 validation failed; inspect failed rows before continuing",
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
    theorem: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    stress: list[dict[str, Any]],
    runner: list[dict[str, Any]],
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
                "# 1528 - Lambda Phi Silence, No-Flux, or Multiplier-Stress Bound",
                "",
                "## Verdict",
                "- The exact energy route is now written: if `Box lambda_phi=-c_I R` reduces to a positive elliptic harmonic problem, then boundary/no-flux plus zero-mode fixing would imply `lambda_phi=0`.",
                "- Crucial guard: `grad lambda_phi=0` is not enough, because a constant `lambda_phi` can still multiply the metric-dependent `S_Gamma` term.",
                "- The theorem is not promoted because static elliptic reduction, parent boundary/no-flux, and zero-mode fixing are unsigned.",
                "- A multiplier-stress fallback bound is staged with absolute/no-cancellation structure, but no numeric/source-backed constants exist yet.",
                "- No `K_hat`, `DeltaK`, local-GR/Newton, or PPN claim is promoted from 1528.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Lambda Phi Energy Theorem",
                md_table(theorem, ["theorem_id", "object", "formula_or_statement", "status", "missing_to_promote"]),
                "",
                "## Boundary / Zero-Mode Audit",
                md_table(boundary, ["audit_id", "target", "condition", "status", "missing_to_promote"]),
                "",
                "## Multiplier-Stress Bound Schema",
                md_table(stress, ["bound_id", "quantity", "bound_formula", "status", "missing_to_promote"]),
                "",
                "## Theorem Or Bound Runner",
                md_table(runner, ["runner_id", "route", "required_inputs", "current_inputs", "result", "fallback"]),
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
    theorem = energy_theorem_rows()
    boundary = boundary_audit_rows()
    stress = stress_bound_rows()
    runner = theorem_runner_rows()
    rejections = rejection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ENERGY_THEOREM, theorem)
    write_csv(BOUNDARY_AUDIT, boundary)
    write_csv(STRESS_BOUND, stress)
    write_csv(THEOREM_RUNNER, runner)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        ENERGY_THEOREM,
        BOUNDARY_AUDIT,
        STRESS_BOUND,
        THEOREM_RUNNER,
        REJECTION_LEDGER,
        CLAIM_GATE,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, theorem, boundary, stress, runner, rejections, gates, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()
