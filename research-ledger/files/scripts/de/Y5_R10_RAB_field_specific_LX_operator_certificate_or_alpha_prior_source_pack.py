from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
R10 = ROOT / "source-intake" / "r10"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1508-Y5-R10-RAB-field-specific-LX-operator-certificate-or-alpha-prior-source-pack.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1507_validation": OUT / "P8_Y5_BRR545_1507_VALIDATION.csv",
    "1507_nohair_audit": OUT / "P8_Y5_R10_1507_POSITIVE_NOHAIR_CHARGE_ZERO_AUDIT.csv",
    "1507_nohair_theorem": OUT / "P8_Y5_R10_1507_NOHAIR_THEOREM_LEDGER.csv",
    "1507_certificate_requirements": OUT / "P8_Y5_R10_1507_THEOREM_ZERO_CERTIFICATE_REQUIREMENTS.csv",
    "1507_alpha_prior_requirements": OUT / "P8_Y5_R10_1507_SOURCE_BACKED_ALPHA_PRIOR_REQUIREMENTS.csv",
    "1507_alpha_template": OUT / "R10_alpha_lambda_curve_MTS_1507_ALPHA_PRIOR_TEMPLATE_NONCLAIM.csv",
    "1507_target_blockers": OUT / "P8_Y5_R10_1507_TARGET_PROMOTION_BLOCKERS.csv",
    "energy_identity": OUT / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
    "hamiltonian_silence": ROOT / "runs" / "20260605-141500-Y5-extra-sector-Hamiltonian-charge-silence-or-channel-fill" / "results" / "P8_Y5_HAMILTONIAN_EXTRA_CHARGE_SILENCE_ATTEMPT.csv",
    "hamiltonian_channel_map": ROOT / "runs" / "20260605-141500-Y5-extra-sector-Hamiltonian-charge-silence-or-channel-fill" / "results" / "P8_Y5_HAMILTONIAN_EXTRA_CHARGE_CHANNEL_MAP.csv",
    "positive_operator_attempt": ROOT / "runs" / "20260605-142500-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill" / "results" / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_POSITIVE_OPERATOR_ATTEMPT.csv",
    "force_law_map": ROOT / "runs" / "20260605-142500-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill" / "results" / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_FORCE_LAW_MAP.csv",
    "r10_curve_contract": ROOT / "runs" / "20260605-142500-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill" / "results" / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_R10_CURVE_CONTRACT.csv",
    "decision_557": ROOT / "runs" / "20260605-142500-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill" / "results" / "P8_Y5_BRR545_557_DECISION.csv",
}

CURVE_TARGET = R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
KERNEL_TARGET = R10 / "derived" / "R10_delta_w_kernel_lambda.csv"
C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

OPERATOR_AUDIT = OUT / "P8_Y5_R10_1508_FIELD_SPECIFIC_LX_OPERATOR_AUDIT.csv"
OPERATOR_THEOREM = OUT / "P8_Y5_R10_1508_LX_THEOREM_LEDGER.csv"
OPERATOR_MATRIX = OUT / "P8_Y5_R10_1508_OPERATOR_CANDIDATE_MATRIX.csv"
CERT_TRIAL = OUT / "P8_Y5_R10_1508_LX_CERTIFICATE_TRIAL.csv"
ALPHA_PACK = OUT / "P8_Y5_R10_1508_ALPHA_PRIOR_SOURCE_PACK.csv"
SOURCE_LEDGER = OUT / "P8_Y5_R10_1508_SOURCE_ACQUISITION_LEDGER.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1508_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1508_DELTA_W_SCORE_READINESS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1508_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1508_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1508_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1508_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1508_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1508_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1508"
QUAR_AUDIT = QUARANTINE / "FIELD_SPECIFIC_LX_OPERATOR_AUDIT_NONCLAIM.csv"
QUAR_THEOREM = QUARANTINE / "LX_THEOREM_LEDGER_NONCLAIM.csv"
QUAR_MATRIX = QUARANTINE / "OPERATOR_CANDIDATE_MATRIX_NONCLAIM.csv"
QUAR_TRIAL = QUARANTINE / "LX_CERTIFICATE_TRIAL_NONCLAIM.csv"
QUAR_ALPHA = QUARANTINE / "ALPHA_PRIOR_SOURCE_PACK_NONCLAIM.csv"
BRANCH_AUDIT = BRANCH_RESIDUALS / "r10_field_specific_lx_operator_audit_nonclaim_1508.csv"
BRANCH_THEOREM = BRANCH_RESIDUALS / "r10_lx_theorem_ledger_nonclaim_1508.csv"
BRANCH_MATRIX = BRANCH_RESIDUALS / "r10_operator_candidate_matrix_nonclaim_1508.csv"
BRANCH_TRIAL = BRANCH_RESIDUALS / "r10_lx_certificate_trial_nonclaim_1508.csv"
BRANCH_ALPHA = BRANCH_RESIDUALS / "r10_alpha_prior_source_pack_nonclaim_1508.csv"


def flags() -> dict[str, bool]:
    return {"score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_paths(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
    claim_keys = ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "R10_pass_for_claim"]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def operator_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("LXA1508_0_reference_identity", "positive energy identity", "CONDITIONAL_REFERENCE", "previous ledgers contain the theorem shape but not the actual R10-active operator"),
        ("LXA1508_1_field_identity", "R10-active X_a", "MISSING_PARENT_FIELD_ID", "no parent-owned field/component is yet selected as the finite R10 carrier"),
        ("LXA1508_2_operator_form", "L_X", "MISSING_FIELD_SPECIFIC_OPERATOR", "generic Helmholtz/vector/memory templates do not instantiate the actual Euler operator"),
        ("LXA1508_3_sign_domain", "positivity and domain", "MISSING_SIGNED_DOMAIN", "need a positive self-adjoint domain, gauge fixing, and boundary conditions"),
        ("LXA1508_4_source_charge", "J_X / Q_X_source", "MISSING_SOURCE_ZERO_OR_VALUE", "nonzero source charge gives a Yukawa force rather than nohair"),
        ("LXA1508_5_test_charge", "q_test_X", "MISSING_TEST_ZERO_OR_VALUE", "R10 readout response cannot be set to zero by geometry language alone"),
        ("LXA1508_6_projection", "PiM_H Q_X", "MISSING_HAMILTONIAN_PROJECTION", "local measured-G normalization remains blocked"),
        ("LXA1508_7_boundary_history", "boundary/history flux", "MISSING_BOUNDARY_HISTORY_SILENCE", "positive identities still carry surface/history terms"),
        ("LXA1508_8_verdict", "field-specific L_X certificate", "NOT_INSTANTIATED", "move to explicit source-backed alpha-prior acquisition while keeping no local-GR/R10 claim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "object": obj,
            "current_status": status,
            "effect": effect,
            **flags(),
        }
        for audit_id, obj, status, effect in rows
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1508_0_field_specific_positive_operator_zero",
            "statement": "If the parent action yields the actual R10-active Euler operator L_X, L_X is positive/self-adjoint on the local annulus, source/test charges vanish, boundary/history flux vanishes, and PiM_H projection vanishes, then the R10-active alpha_X(lambda) is zero.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_sketch": "The source-free field equation paired with X gives a positive norm plus boundary/history terms. With all charge, projection, and boundary terms zero, the physical R10 readout is silent modulo gauge/topological constants.",
            "current_claim_status": "CONDITIONAL_NOT_PARENT_INSTANTIATED",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1508_1_template_operator_no_instantiation",
            "statement": "A generic positive operator template is insufficient unless it is the parent Euler operator for the same field and the same R10 readout variables.",
            "proof_status": "COUNTERMODEL_GUARDRAIL",
            "proof_sketch": "A different positive operator can be source-free while the actual coupled finite-range carrier has nonzero source/test charge.",
            "current_claim_status": "BLOCKS_TEMPLATE_SUBSTITUTION",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1508_2_current_verdict",
            "statement": "The current route does not close the field-specific L_X certificate; the disciplined next move is a source-backed alpha-prior pack, not a local-R10 or local-GR claim.",
            "proof_status": "DERIVED_AS_GATE_LOGIC",
            "proof_sketch": "1507 certificate requirements and older 556/557 ledgers keep field identity, operator sign, source/test charge, boundary/history, projection, tau, and bound curve as missing inputs.",
            "current_claim_status": "KEEP_NONCLAIM_SOURCE_PACK",
            **flags(),
        },
    ]


def candidate_matrix_rows() -> list[dict[str, Any]]:
    rows = [
        ("CAND1508_0_scalar_helmholtz", "massive scalar/Helmholtz", "L_X=-Delta_A+m_X^2", "cleanest theorem form", "field id; Z_X; m_X^2; source/test charges; boundary flux", "CONDITIONAL_ONLY"),
        ("CAND1508_1_vector_tensor_projector", "gauge-fixed vector/tensor/projector", "L_X=P(-nabla^2+M_X^2+curvature)P", "closer to coframe/projector language", "physical norm; gauge kernel; source readout; PiM_H projection", "CONDITIONAL_ONLY"),
        ("CAND1508_2_memory_kernel", "stable memory kernel", "int X K X >= 0", "fits memory language", "locality; no history injection; finite tau_R10; source kernel", "CONDITIONAL_ONLY"),
        ("CAND1508_3_boundary_topological", "exact/topological boundary sector", "X=dB or pure boundary class", "could kill bulk force", "surface flux quantization; no R10 readout; cohomology domain", "CONDITIONAL_ONLY"),
        ("CAND1508_4_universal_calibration", "constant universal calibration", "range-independent G rescaling", "harmless only if derivative-free", "proof no finite lambda profile; measured-G denominator", "NOT_OPERATOR_NOHAIR"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "candidate_id": candidate_id,
            "candidate_operator": operator,
            "formal_shape": shape,
            "route_strength": strength,
            "missing_inputs": missing,
            "verdict": verdict,
            "source_paths": source_paths("energy_identity", "positive_operator_attempt", "force_law_map"),
            **flags(),
        }
        for candidate_id, operator, shape, strength, missing, verdict in rows
    ]


def certificate_trial_rows() -> list[dict[str, Any]]:
    rows = [
        ("TRIAL1508_0_field_map", "field_id(X_a)", "must name the parent field/component varied by the action", "MISSING_PARENT_FIELD_ID"),
        ("TRIAL1508_1_euler_operator", "L_X", "must be extracted from second variation or Euler equation", "MISSING_PARENT_OPERATOR"),
        ("TRIAL1508_2_inner_product", "domain and norm", "must specify positive measure/coframe/domain after gauge quotient", "MISSING_DOMAIN"),
        ("TRIAL1508_3_sign", "Z_X and M_X^2", "must prove positive kinetic and non-tachyonic mass/range or constrained positive kernel", "MISSING_SIGN"),
        ("TRIAL1508_4_source", "Q_X_source", "must prove zero or provide numeric source charge", "MISSING_ZERO_OR_NUMERIC_VALUE"),
        ("TRIAL1508_5_test", "q_test_X", "must prove zero or provide numeric test/readout charge", "MISSING_ZERO_OR_NUMERIC_VALUE"),
        ("TRIAL1508_6_boundary", "boundary_flux/history", "must prove silence on R10 local annulus", "MISSING_SILENCE_PROOF"),
        ("TRIAL1508_7_projection", "PiM_H Q_X", "must prove zero or source measured-G projection coefficient", "MISSING_PROJECTION"),
        ("TRIAL1508_8_acceptance", "alpha_X(lambda)", "can be zero only after TRIAL1508_0 through TRIAL1508_7 close", "BLOCKED"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "trial_id": trial_id,
            "symbol": symbol,
            "requirement": requirement,
            "current_status": status,
            "accepted_now": False,
            **flags(),
        }
        for trial_id, symbol, requirement, status in rows
    ]


def alpha_pack_rows() -> list[dict[str, Any]]:
    rows = [
        ("APACK1508_0_scalar_like", "X_scalar_candidate", "L_X=-Delta_A+m_X^2", "MISSING_Z_X", "MISSING_M_X2", "MISSING_lambda_X", "MISSING_Q_X_source", "MISSING_q_test_X"),
        ("APACK1508_1_vector_tensor_like", "X_projector_candidate", "L_X=P(-nabla^2+M_X^2+R)P", "MISSING_Z_X", "MISSING_M_X2", "MISSING_lambda_X", "MISSING_Q_X_source", "MISSING_q_test_X"),
        ("APACK1508_2_memory_like", "X_memory_candidate", "L_X=positive_history_kernel", "MISSING_KERNEL_NORM", "MISSING_KERNEL_GAP", "MISSING_effective_lambda", "MISSING_history_source", "MISSING_readout_charge"),
        ("APACK1508_3_boundary_like", "X_boundary_candidate", "L_X=boundary_exact_or_topological", "MISSING_SURFACE_NORM", "MISSING_SURFACE_GAP", "MISSING_effective_lambda", "MISSING_surface_charge", "MISSING_boundary_readout"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": pack_id,
            "field_id": field_id,
            "operator_form": operator_form,
            "Z_X": z_x,
            "M_X2": m_x2,
            "lambda_X": lambda_x,
            "Q_X_source": q_source,
            "q_test_X": q_test,
            "PiM_H_projection": "MISSING_PiM_H_projection",
            "boundary_flux": "MISSING_boundary_history_flux",
            "tau_R10": "MISSING_tau_R10",
            "alpha_predicted": "MISSING_alpha_from_parent_coefficients",
            "alpha_bound": "MISSING_reviewed_R10_bound_curve",
            "source_paths": source_paths("1507_alpha_prior_requirements", "force_law_map", "r10_curve_contract"),
            "parent_status": "SCHEMA_ONLY_NONCLAIM",
            **flags(),
        }
        for pack_id, field_id, operator_form, z_x, m_x2, lambda_x, q_source, q_test in rows
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        ("SRC1508_0_parent_action_variation", "parent action/euler variation for X_a", "second variation or Euler equation identifying the actual R10-active field", "parent derivation note or formal action file"),
        ("SRC1508_1_kinetic_mass_sign", "Z_X, M_X^2, lambda_X", "positive kinetic sign and finite range with units", "parent Hessian/eigenvalue source"),
        ("SRC1508_2_source_charge", "Q_X_source", "zero theorem or numeric source charge in R10 source body", "matter coupling/current derivation"),
        ("SRC1508_3_test_charge", "q_test_X", "zero theorem or numeric test/readout charge for R10 apparatus", "observed coframe/material response derivation"),
        ("SRC1508_4_boundary_history", "boundary/history flux", "silence theorem or numeric boundary/history coefficient", "worldtube boundary condition or memory kernel source"),
        ("SRC1508_5_projection", "PiM_H projection", "zero theorem or same-frame measured-G projection coefficient", "Hamiltonian/PiM source ledger"),
        ("SRC1508_6_tau_kernel", "tau_R10(lambda)", "finite-source geometry response kernel", "R10 tau/kernel derivation or sourced numerical kernel"),
        ("SRC1508_7_bound_curve", "alpha_bound(lambda)", "reviewed digitized or machine-readable bound curve", "Eot-Wash/R10 source-backed curve table"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": source_id,
            "target_input": target,
            "needed_evidence": evidence,
            "acceptable_source": acceptable,
            "current_status": "MISSING_SOURCE_BACKED_INPUT",
            **flags(),
        }
        for source_id, target, evidence, acceptable in rows
    ]


def blocker_rows() -> list[dict[str, Any]]:
    rows = [
        ("BLOCK1508_0", "field-specific L_X not parent-instantiated"),
        ("BLOCK1508_1", "positive domain/sign/gauge certificate missing"),
        ("BLOCK1508_2", "source/test charge zero or values missing"),
        ("BLOCK1508_3", "boundary/history silence missing"),
        ("BLOCK1508_4", "Hamiltonian/PiM projection missing"),
        ("BLOCK1508_5", "tau_R10 finite-source kernel missing"),
        ("BLOCK1508_6", "reviewed alpha_bound(lambda) curve missing"),
        ("BLOCK1508_7", "C_parent import refused until parent coefficient exists"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "blocker": blocker,
            "effect": "no R10/local-GR/Newton claim; source-pack only",
            **flags(),
        }
        for blocker_id, blocker in rows
    ]


def score_readiness_rows(blockers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "score_id": "SCORE1508_0",
            "status": "NOT_SCORE_READY",
            "missing_blockers": "; ".join(row["blocker"] for row in blockers),
            "required_before_scoring": "either close field-specific zero theorem or provide numeric source-backed alpha/tau/bound curve rows",
            **flags(),
        }
    ]


def c_parent_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "CP1508_0",
            "target": rel(C_PARENT_IMPORT),
            "exists_now": C_PARENT_IMPORT.exists(),
            "imported_now": False,
            "reason": "C_parent slot import remains refused without parent-owned finite coupling coefficient and source path",
            **flags(),
        }
    ]


def local_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LRS1508_0",
            "object": "R10/local-GR/Newton residual route",
            "status": "OPEN_NONCLAIM_SOURCE_PACK",
            "effect": "GR/Newton reduction still lives only as a target; not proven by the R10 branch",
            **flags(),
        }
    ]


def simple_rows_from_blockers(blockers: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            f"{prefix}_id": blocker["blocker_id"].replace("BLOCK", prefix.upper()),
            "status": "RETAIN_BLOCKER",
            "item": blocker["blocker"],
            "reason": blocker["effect"],
            **flags(),
        }
        for blocker in blockers
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1508_0_zero_proof",
            "decision": "field-specific L_X zero-proof does not close now",
            "rationale": "generic positivity exists, but actual field/operator/source/test/boundary/projection clauses remain unsigned",
            "next_action": "do not claim alpha=0; continue to source-backed alpha/tau/bound acquisition",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1508_1_source_pack",
            "decision": "alpha-prior source pack emitted as nonclaim",
            "rationale": "finite route is the honest fallback if nohair cannot be parent-signed",
            "next_action": "acquire reviewed R10 bound curve and tau kernel before any scoring",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1508_0_1509",
            "next_target": "1509-Y5-R10-RAB-acquire-reviewed-R10-bound-curve-and-tau-kernel-or-freeze-local-R10.md",
            "script": "scripts/Y5_R10_RAB_acquire_reviewed_R10_bound_curve_and_tau_kernel_or_freeze_local_R10.py",
            "objective": "acquire reviewed R10 alpha_bound(lambda) and tau_R10 inputs, or freeze the local R10 branch as closure-only while the field-specific zero theorem remains unsigned",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for path in [QUARANTINE, BRANCH_RESIDUALS]:
        path.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (OPERATOR_AUDIT, QUAR_AUDIT),
        (OPERATOR_THEOREM, QUAR_THEOREM),
        (OPERATOR_MATRIX, QUAR_MATRIX),
        (CERT_TRIAL, QUAR_TRIAL),
        (ALPHA_PACK, QUAR_ALPHA),
        (OPERATOR_AUDIT, BRANCH_AUDIT),
        (OPERATOR_THEOREM, BRANCH_THEOREM),
        (OPERATOR_MATRIX, BRANCH_MATRIX),
        (CERT_TRIAL, BRANCH_TRIAL),
        (ALPHA_PACK, BRANCH_ALPHA),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], theorem: list[dict[str, Any]], audit: list[dict[str, Any]], certs: list[dict[str, Any]], alpha_pack: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values())
    exact_conditional = any(row["theorem_id"] == "THM1508_0_field_specific_positive_operator_zero" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem)
    template_guardrail = any(row["theorem_id"] == "THM1508_1_template_operator_no_instantiation" and row["proof_status"] == "COUNTERMODEL_GUARDRAIL" for row in theorem)
    no_instantiation = any(row["audit_id"] == "LXA1508_8_verdict" and row["current_status"] == "NOT_INSTANTIATED" for row in audit)
    certificate_blocked = any(row["trial_id"] == "TRIAL1508_8_acceptance" and row["current_status"] == "BLOCKED" for row in certs)
    alpha_pack_nonclaim = all(row["parent_status"] == "SCHEMA_ONLY_NONCLAIM" and row["valid_for_claim"] is False for row in alpha_pack)
    acquisition_complete = len(read_csv(SOURCE_LEDGER)) >= 8
    live_targets_absent = not CURVE_TARGET.exists() and not KERNEL_TARGET.exists()
    c_parent_refused = read_csv(C_PARENT_REFUSAL)[0]["imported_now"] == "False"
    csv_parse_ok = all(parse_csv(path) for path in generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_AUDIT, QUAR_THEOREM, QUAR_MATRIX, QUAR_TRIAL, QUAR_ALPHA, BRANCH_AUDIT, BRANCH_THEOREM, BRANCH_MATRIX, BRANCH_TRIAL, BRANCH_ALPHA])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    checks = [
        ("VAL1508_0_local_sources", source_paths_exist, "all cited 1507/energy/operator/R10 source paths exist"),
        ("VAL1508_1_exact_conditional", exact_conditional, "field-specific positive-operator zero theorem recorded as exact conditional"),
        ("VAL1508_2_template_guardrail", template_guardrail, "generic positive operator substitution is rejected"),
        ("VAL1508_3_no_instantiation", no_instantiation, "current branch does not instantiate L_X"),
        ("VAL1508_4_certificate_blocked", certificate_blocked, "alpha=0 acceptance remains blocked"),
        ("VAL1508_5_alpha_pack_nonclaim", alpha_pack_nonclaim, "alpha source pack rows are schema-only and nonclaim"),
        ("VAL1508_6_acquisition_ledger", acquisition_complete, "source acquisition ledger covers field/operator/source/test/boundary/projection/tau/bound curve"),
        ("VAL1508_7_live_targets_absent", live_targets_absent, "live R10 bound curve/kernel targets remain absent"),
        ("VAL1508_8_Cparent_refused", c_parent_refused, "C_parent import was not performed"),
        ("VAL1508_9_csv_parse", csv_parse_ok, "all generated 1508 CSVs parse cleanly"),
        ("VAL1508_10_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1508_11_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1508_12_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1508_13_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1508_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1508 kept the L_X zero proof conditional and emitted a nonclaim alpha/tau/bound source pack"
            if overall
            else "1508 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    audit: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    certs: list[dict[str, Any]],
    alpha_pack: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1508 - Field-Specific L_X Operator Certificate or Alpha-Prior Source Pack",
                "",
                "## Verdict",
                "- The exact zero route is clear but still conditional: the parent must supply the actual R10-active L_X, a positive domain/signature, zero source/test charge, zero boundary/history flux, and zero PiM_H projection.",
                "- The current corpus has useful positive-operator templates, but none are yet the field-specific parent Euler operator for the R10 carrier.",
                "- Therefore 1508 keeps R10/local-GR nonclaim and emits a source-ready alpha/tau/bound acquisition pack instead of smuggling in alpha_X(lambda)=0.",
                "",
                "## Operator Audit",
                md_table(audit, ["audit_id", "object", "current_status", "effect"]),
                "",
                "## Theorem Ledger",
                md_table(theorem, ["theorem_id", "proof_status", "current_claim_status"]),
                "",
                "## Candidate Matrix",
                md_table(matrix, ["candidate_id", "candidate_operator", "formal_shape", "verdict"]),
                "",
                "## Certificate Trial",
                md_table(certs, ["trial_id", "symbol", "requirement", "current_status"]),
                "",
                "## Alpha Source Pack",
                md_table(alpha_pack, ["pack_id", "field_id", "operator_form", "parent_status", "valid_for_claim"]),
                "",
                "## Source Acquisition Ledger",
                md_table(acquisition, ["source_id", "target_input", "current_status"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    audit = operator_audit_rows()
    theorem = theorem_rows()
    matrix = candidate_matrix_rows()
    certs = certificate_trial_rows()
    alpha_pack = alpha_pack_rows()
    acquisition = acquisition_rows()
    blockers = blocker_rows()
    readiness = score_readiness_rows(blockers)
    c_parent = c_parent_refusal_rows()
    local_rows = local_status_rows()
    rejections = simple_rows_from_blockers(blockers, "rejection")
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OPERATOR_AUDIT, audit)
    write_csv(OPERATOR_THEOREM, theorem)
    write_csv(OPERATOR_MATRIX, matrix)
    write_csv(CERT_TRIAL, certs)
    write_csv(ALPHA_PACK, alpha_pack)
    write_csv(SOURCE_LEDGER, acquisition)
    write_csv(TARGET_BLOCKERS, blockers)
    write_csv(SCORE_READINESS, readiness)
    write_csv(C_PARENT_REFUSAL, c_parent)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        OPERATOR_AUDIT,
        OPERATOR_THEOREM,
        OPERATOR_MATRIX,
        CERT_TRIAL,
        ALPHA_PACK,
        SOURCE_LEDGER,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, theorem, audit, certs, alpha_pack)
    write_csv(VALIDATION, validation)
    write_doc(audit, theorem, matrix, certs, alpha_pack, acquisition, validation, next_rows)
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
