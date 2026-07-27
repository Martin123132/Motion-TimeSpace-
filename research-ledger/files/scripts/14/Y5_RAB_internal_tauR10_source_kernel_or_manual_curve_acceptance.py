from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1573"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1573-Y5-RAB-internal-tauR10-source-kernel-or-manual-curve-acceptance.md"

SOURCE_FILES = {
    "1572_doc": ROOT / "1572-Y5-RAB-tauR10-source-normalization-or-accepted-curve-QA.md",
    "1572_validation": OUT / "P8_Y5_BRR545_1572_VALIDATION.csv",
    "1572_tau": OUT / "P8_Y5_PARENT_QLOC_1572_TAU_R10_SOURCE_NORMALIZATION_DERIVATION_ATTEMPT.csv",
    "1572_acceptance": OUT / "P8_Y5_PARENT_QLOC_1572_CURVE_ACCEPTANCE_GATE.csv",
    "04_action_contract": ROOT / "04-vacuum-reciprocity-action-contract.md",
    "05_theorem_attempt": ROOT / "05-reciprocity-theorem-attempt.md",
    "07_constraint_route": ROOT / "07-nonpropagating-reciprocity-constraint.md",
    "1483_tau_lock": OUT / "P8_Y5_R10_1483_SYMBOLIC_TAU_FUNCTIONAL_LOCK.csv",
    "1402_transfer": OUT / "P8_Y5_R10_1402_SHARED_TAU_TRANSFER_THEOREM_AUDIT.csv",
    "1519_coframe_tau": OUT / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv",
    "1322_clock_readout": OUT / "P8_Y5_R10_1322_TAU_READOUT_DERIVATION_ATTEMPT.csv",
}

NEEDLES = {
    "1572_doc": ["internal `tau_R10` source-normalization kernel remains the hard blocker", "NEXT_1573_INTERNAL_TAU_R10_SOURCE_KERNEL_OR_MANUAL_CURVE_ACCEPTANCE"],
    "1572_validation": ["VAL1572_OVERALL", "PASS"],
    "1572_tau": ["TAUN1572_4_verdict", "NOT_READY"],
    "1572_acceptance": ["ACCEPT1572_3_curve_status", "NOT_ACCEPTED"],
    "04_action_contract": ["d/dr [ W(r,L,fields) dR_AB/dr ] = J_R", "J_R = 0 in local vacuum"],
    "05_theorem_attempt": ["S_R = integral dr [0.5 W(r) (R_AB')^2 + J_R R_AB].", "Q_R = integral J_R dr = 0"],
    "07_constraint_route": ["S_constraint = integral lambda_R R_AB.", "R_AB = 0."],
    "1483_tau_lock": ["TAULOCK1483_6_output", "tau_eff_X", "forbidden_shortcuts"],
    "1402_transfer": ["DTT1402_3_tau_R10_kernel_owner", "Z_shared_tau_domain=false"],
    "1519_coframe_tau": ["OCF1519_4_tau_lock", "MISSING_TAU_LOCK"],
    "1322_clock_readout": ["TAU1322_3_local_silence", "CONDITIONAL_ONLY_NOT_ACTIVE"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1573_SOURCE_REGISTER.csv"
KERNEL_DERIVATION = OUT / "P8_Y5_PARENT_QLOC_1573_TAU_R10_KERNEL_DERIVATION_CONTRACT.csv"
ZERO_CONDITIONS = OUT / "P8_Y5_PARENT_QLOC_1573_R10_ZERO_CONDITION_AUDIT.csv"
REQUIRED_INPUTS = OUT / "P8_Y5_PARENT_QLOC_1573_TAU_R10_REQUIRED_INPUTS.csv"
SCORING_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1573_TAU_R10_SCORING_INTERFACE_TEMPLATE_NONCLAIM.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1573_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1573_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1573_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1573_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1573_VALIDATION.csv"

COPY_TARGETS = {
    KERNEL_DERIVATION: [
        QUARANTINE / "TAU_R10_KERNEL_DERIVATION_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "tau_R10_kernel_derivation_contract_nonclaim_1573.csv",
    ],
    ZERO_CONDITIONS: [
        QUARANTINE / "R10_ZERO_CONDITION_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R10_zero_condition_audit_nonclaim_1573.csv",
    ],
    REQUIRED_INPUTS: [
        QUARANTINE / "TAU_R10_REQUIRED_INPUTS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "tau_R10_required_inputs_nonclaim_1573.csv",
    ],
    SCORING_TEMPLATE: [
        QUARANTINE / "TAU_R10_SCORING_INTERFACE_TEMPLATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "tau_R10_scoring_interface_template_nonclaim_1573.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "internal_tauR10_kernel_decision_nonclaim_1573.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
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


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


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


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "numeric_value_present",
        "source_backed",
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
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1573_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, NEEDLES[key]),
                "needles": "; ".join(NEEDLES[key]),
                "purpose": "derive tau_R10 source-normalized kernel or prove zero route",
                **flags(),
            }
        )
    return rows


def kernel_derivation_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_id": "KDER1573_0_parent_quadratic_block",
            "statement": "Use a local scalar reciprocity residual R=R_AB with quadratic parent block.",
            "equation": "S_R = integral sqrt(-g)[-1/2 Z_R (nabla R)^2 -1/2 M_R^2 R^2 + R J_R] + S_boundary",
            "derived_output": "linearized source equation after normalization",
            "status": "FORMAL_CONTRACT_WRITTEN",
            "blocking_gap": "Z_R, M_R^2, J_R and boundary term are not source-backed in one parent normalization",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_id": "KDER1573_1_eom",
            "statement": "Variation gives the finite-range reciprocity equation when Z_R and M_R^2 are nonzero.",
            "equation": "Z_R Box R - M_R^2 R = -J_R plus boundary/corner readout terms",
            "derived_output": "m_R^2=M_R^2/Z_R and lambda_R=sqrt(Z_R/M_R^2)",
            "status": "FORMAL_RANGE_LAW_DERIVED_CONDITIONAL",
            "blocking_gap": "positive same-frame Z_R and M_R^2 are missing",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_id": "KDER1573_2_source_charge",
            "statement": "Matter coupling must define source-normalized charges, not guessed tau=1.",
            "equation": "beta_i^R := partial ln m_i / partial R_AB,  J_R(x)=sum_i beta_i^R m_i delta_3(x-x_i)/sqrt(g_3)",
            "derived_output": "source and test legs are beta_S^R and beta_T^R in the same observed frame",
            "status": "FORMAL_SOURCE_CHARGE_LAW_DERIVED_CONDITIONAL",
            "blocking_gap": "beta_S^R and beta_T^R are not parent-signed or numerically sourced",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_id": "KDER1573_3_green_function",
            "statement": "The static Green function maps a point source into a Yukawa profile.",
            "equation": "R(r)=-(beta_S^R m_S)/(4 pi Z_R) exp(-r/lambda_R)/r, ignoring unsigned boundary tails",
            "derived_output": "finite R_AB residual has the same radial language as R10 alpha(lambda)",
            "status": "FORMAL_YUKAWA_PROFILE_DERIVED_CONDITIONAL",
            "blocking_gap": "boundary/tail/readout silence is not signed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_id": "KDER1573_4_alpha_match",
            "statement": "Matching delta V_R to V=-G m_S m_T alpha exp(-r/lambda)/r gives the tau_R10 bridge.",
            "equation": "alpha_MTS(lambda_R)=Xi_R10[beta_S^R beta_T^R/(4 pi G Z_R)+alpha_boundary_tail]",
            "derived_output": "tau_R10 = Xi_R10/(4 pi G Z_R), A_R=beta_S^R beta_T^R + 4 pi G Z_R alpha_boundary_tail",
            "status": "FORMAL_TAU_KERNEL_LAW_DERIVED_CONDITIONAL",
            "blocking_gap": "Xi_R10, beta legs, Z_R units, and boundary tail are not source-backed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_id": "KDER1573_5_claim_ceiling",
            "statement": "The kernel law is useful but not a claim row.",
            "equation": "score only if lambda_R>0, alpha_MTS numeric, accepted alpha_bound(lambda_R), and abs(alpha_MTS)<=alpha_bound",
            "derived_output": "ready scoring interface without numeric promotion",
            "status": "FORMAL_INTERFACE_READY_VALUES_MISSING",
            "blocking_gap": "no accepted curve plus no internal numeric/theorem-zero inputs",
            **flags(),
        },
    ]
    return rows


def zero_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "zero_id": "ZERO1573_0_constraint_route",
            "zero_condition": "R_AB is a first-class/nonpropagating constraint with R_AB=0 before matter readout.",
            "required_parent_signature": "lambda_R R_AB constraint belongs to parent action and descends through observed matter variables",
            "current_evidence": "07 supplies route; not parent-origin signed",
            "current_status": "CONDITIONAL_ONLY_NOT_ACTIVE",
            "claim_effect": "cannot set tau_R10=0",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "zero_id": "ZERO1573_1_source_silence",
            "zero_condition": "beta_S^R=0 and beta_T^R=0 for R10 source/test bodies in the observed matter action.",
            "required_parent_signature": "matter masses/material response descend without representative R_AB dependence",
            "current_evidence": "1519 says matter constants descent and tau lock are not parent-signed",
            "current_status": "NOT_PROVED",
            "claim_effect": "cannot remove source amplitude",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "zero_id": "ZERO1573_2_boundary_silence",
            "zero_condition": "boundary/corner/readout tail alpha_boundary_tail=0.",
            "required_parent_signature": "no R_AB boundary charge, no shadow frame, and no readout leakage",
            "current_evidence": "04/05 require vacuum source and boundary silence; 1519 no-shadow frame is classification only",
            "current_status": "NOT_PROVED",
            "claim_effect": "cannot drop B_R/readout tail",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "zero_id": "ZERO1573_3_range_decoupling",
            "zero_condition": "finite residual decouples from R10 by lambda_R outside the tested range or M_R^2/Z_R limit.",
            "required_parent_signature": "positive same-frame Z_R/M_R^2 plus accepted comparison range",
            "current_evidence": "1572 reviewed curve is not accepted and Z_R/M_R^2 are missing",
            "current_status": "NOT_EVALUABLE",
            "claim_effect": "cannot score or decouple by range",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "zero_id": "ZERO1573_4_transfer_shortcut",
            "zero_condition": "borrow clock/WEP tau silence to set tau_R10=0.",
            "required_parent_signature": "shared parent tau/domain transfer theorem across clock, WEP, R10 and PPN",
            "current_evidence": "1402 forbids clock/WEP to R10 transfer without kernel and domain theorem",
            "current_status": "FORBIDDEN_SHORTCUT",
            "claim_effect": "tau_R10 must be sourced separately",
            **flags(),
        },
    ]


def required_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "REQ1573_0_ZR",
            "symbol": "Z_R",
            "role": "kinetic normalization in tau_R10 and range",
            "minimum_required_form": "positive same-frame parent-normalized value with units, or parent-signed operator exclusion",
            "current_status": "MISSING_ZR",
            "source_hint": "future parent R_AB quadratic block or theorem-zero certificate",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "REQ1573_1_MR2",
            "symbol": "M_R^2",
            "role": "range denominator lambda_R=sqrt(Z_R/M_R^2)",
            "minimum_required_form": "positive same-frame Hessian/mass-gap value with units",
            "current_status": "MISSING_MR2",
            "source_hint": "future parent Hessian around local vacuum branch",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "REQ1573_2_beta_source",
            "symbol": "beta_S^R",
            "role": "R10 source body R_AB charge",
            "minimum_required_form": "partial ln m_source / partial R_AB or theorem-zero for source material",
            "current_status": "MISSING_SOURCE_CHARGE",
            "source_hint": "matter action descent/material tensor in parent basis",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "REQ1573_3_beta_test",
            "symbol": "beta_T^R",
            "role": "R10 test body R_AB charge",
            "minimum_required_form": "partial ln m_test / partial R_AB or theorem-zero for test material",
            "current_status": "MISSING_TEST_CHARGE",
            "source_hint": "R10 composition/readout material response map",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "REQ1573_4_Xi",
            "symbol": "Xi_R10",
            "role": "readout/sign/window normalization from parent response to R10 alpha convention",
            "minimum_required_form": "declared convention mapping delta V_R to alpha(lambda)",
            "current_status": "MISSING_READOUT_CONVENTION",
            "source_hint": "R10 apparatus/readout convention and parent observer map",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "REQ1573_5_boundary_tail",
            "symbol": "alpha_boundary_tail or B_R",
            "role": "boundary/corner/readout residual contribution",
            "minimum_required_form": "zero theorem or finite absolute bound with no-cancellation guard",
            "current_status": "MISSING_BOUNDARY_TAIL",
            "source_hint": "boundary projection theorem or source-backed tail row",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "REQ1573_6_bound_curve",
            "symbol": "alpha_bound(lambda)",
            "role": "external R10 comparator",
            "minimum_required_form": "accepted independently checked curve/table with source/provenance",
            "current_status": "REVIEWED_CANDIDATE_NOT_ACCEPTED",
            "source_hint": "1572 curve needs independent/manual tick and curve QA",
            **flags(),
        },
    ]


def scoring_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "template_id": "SCORE1573_0_symbolic_kernel",
            "lambda_R_m": "sqrt(Z_R/M_R^2) after unit conversion to metres",
            "alpha_MTS": "Xi_R10*(beta_S^R*beta_T^R/(4*pi*G*Z_R)+alpha_boundary_tail)",
            "alpha_bound_source": "accepted R10 alpha(lambda) curve/table only",
            "pass_condition": "abs(alpha_MTS)<=alpha_bound(lambda_R)",
            "current_status": "TEMPLATE_ONLY_VALUES_MISSING",
            "failure_if_used_now": "MISSING_ZR;MISSING_MR2;MISSING_BETA_SOURCE;MISSING_BETA_TEST;MISSING_XI;MISSING_BOUNDARY;CURVE_NOT_ACCEPTED",
            "accepted_for_scoring": False,
            "passes_for_claim": False,
            **flags(),
        }
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1573_0_sources",
            "object": "1572 handoff plus parent/tau precedent sources",
            "status": "PASS",
            "detail": "all source registers are present if validation passes",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1573_1_kernel_law",
            "object": "tau_R10 source-normalized formal law",
            "status": "FORMAL_LAW_DERIVED_CONDITIONAL",
            "detail": "alpha_MTS(lambda_R)=Xi_R10[beta_S beta_T/(4 pi G Z_R)+boundary_tail]",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1573_2_zero_route",
            "object": "tau_R10=0 or q_R=0 theorem",
            "status": "NOT_PROVED",
            "detail": "constraint/source/boundary/readout zero conditions remain unsigned",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1573_3_numeric_score",
            "object": "R10 alpha(lambda) score",
            "status": "BLOCKED_NO_CLAIM",
            "detail": "formal kernel exists but required numeric/theorem-zero inputs and accepted curve are missing",
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1573_0_kernel_formula",
            "claim": "tau_R10 formal kernel law exists",
            "status": "PASS_FORMAL_NONCLAIM",
            "reason": "derived from linearized finite-range R_AB action and Yukawa matching",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1573_1_tau_zero",
            "claim": "tau_R10=0 or q_R=0",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "zero route requires parent-signed constraint/source/boundary/readout silence",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1573_2_numeric_prediction",
            "claim": "numeric alpha_MTS(lambda_R)",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "Z_R/M_R^2/beta legs/Xi/boundary tail missing",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1573_3_R10_score",
            "claim": "R10 pass/fail",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "accepted curve and internal numeric prediction both required",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1573_4_local_GR",
            "claim": "derived local GR/Newton limit",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "R10 kernel law is not a local GR theorem",
            **flags(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1573_0_progress",
            "decision": "TAU_R10_FORMAL_KERNEL_DERIVED_CONDITIONAL",
            "reason": "the R_AB finite residual now has a source-normalized Yukawa matching law",
            "consequence": "future rows must fill beta/Z/M/Xi/boundary inputs or prove all relevant zeros",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1573_1_claim_ceiling",
            "decision": "NO_R10_OR_LOCAL_GR_CLAIM",
            "reason": "formal law has no sourced numeric inputs and curve remains reviewed-only",
            "consequence": "raw/accepted finite rows stay empty",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1573_2_best_next",
            "decision": "NEXT_1574_R10_MATTER_CHARGE_AND_ZR_MR2_INPUT_ROW_OR_ZERO_THEOREM",
            "reason": "kernel law shows the next missing objects exactly: beta_S beta_T, Z_R, M_R^2, Xi_R10 and boundary tail",
            "consequence": "derive matter-charge zero/descent first; if it fails, build finite required-input acquisition rows",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1574-Y5-RAB-R10-matter-charge-and-ZR-MR2-input-row-or-zero-theorem.md",
            "script": "scripts/Y5_RAB_R10_matter_charge_and_ZR_MR2_input_row_or_zero_theorem.py",
            "objective": "try to prove beta_S^R beta_T^R=0 by parent matter descent; otherwise stage finite source-charge, Z_R, M_R^2, Xi_R10 and boundary-tail input rows",
            "do_not": "do not score R10; do not transfer WEP/clock tau; do not claim local GR; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count() -> int:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def has_1573_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1573" in path.name for path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    derivation = read_csv(KERNEL_DERIVATION)
    zeroes = read_csv(ZERO_CONDITIONS)
    required = read_csv(REQUIRED_INPUTS)
    template = read_csv(SCORING_TEMPLATE)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    checks = [
        ("VAL1573_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist"),
        ("VAL1573_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL1573_2_kernel_law",
            any(row["derivation_id"] == "KDER1573_4_alpha_match" and row["status"] == "FORMAL_TAU_KERNEL_LAW_DERIVED_CONDITIONAL" for row in derivation),
            "tau_R10 Yukawa alpha matching law written",
        ),
        (
            "VAL1573_3_zero_not_promoted",
            all(row["current_status"] != "PROVED" for row in zeroes),
            "zero route remains conditional/not proved",
        ),
        (
            "VAL1573_4_required_inputs_missing",
            all(row["current_status"].startswith("MISSING") or row["current_status"] == "REVIEWED_CANDIDATE_NOT_ACCEPTED" for row in required),
            "required internal inputs remain explicit blockers",
        ),
        (
            "VAL1573_5_template_nonclaim",
            len(template) == 1 and template[0]["current_status"] == "TEMPLATE_ONLY_VALUES_MISSING" and template[0]["accepted_for_scoring"] == "False",
            "scoring interface is template-only and not accepted",
        ),
        (
            "VAL1573_6_runner_blocks_score",
            any(row["runner_id"] == "RUN1573_3_numeric_score" and row["status"] == "BLOCKED_NO_CLAIM" for row in runner),
            "runner blocks numeric R10 scoring",
        ),
        (
            "VAL1573_7_claim_gates_closed",
            all(row["claim_allowed"] == "False" for row in gates) and any(row["gate_id"] == "GATE1573_0_kernel_formula" for row in gates),
            "claim gates closed while formula gate is nonclaim pass",
        ),
        (
            "VAL1573_8_decision_next",
            any(row["decision"] == "NEXT_1574_R10_MATTER_CHARGE_AND_ZR_MR2_INPUT_ROW_OR_ZERO_THEOREM" for row in decisions),
            "decision selects matter charge and ZR/MR2 input route",
        ),
        (
            "VAL1573_9_csv_parse",
            all(len(read_csv(path)) > 0 for path in generated_csvs),
            "all generated 1573 CSVs parse cleanly",
        ),
        (
            "VAL1573_10_claim_flags_false",
            generated_flags_false(generated_csvs),
            "all generated prediction/claim flags remain false",
        ),
        (
            "VAL1573_11_no_raw_accepted",
            not has_1573_rows(RAB_RAW) and not has_1573_rows(RAB_ACCEPTED),
            "no 1573 rows written to raw/accepted finite directories",
        ),
        (
            "VAL1573_12_branch_copies",
            all(target.exists() for targets in COPY_TARGETS.values() for target in targets),
            "branch/quarantine nonclaim copies written",
        ),
        (
            "VAL1573_13_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent after run",
        ),
        (
            "VAL1573_14_formalization_untouched",
            formalization_modified_count() == 0,
            "formalization-workbench modified-file count is 0",
        ),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1573_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1573 internal tauR10 source kernel derivation validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(col, "")) for col in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    derivation: list[dict[str, Any]],
    zeroes: list[dict[str, Any]],
    required: list[dict[str, Any]],
    template: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1573 - R_AB Internal tau_R10 Source Kernel Or Manual Curve Acceptance",
                "## Verdict\n"
                "- The derivation-first route made real progress: the finite `R_AB` residual now has a conditional source-normalized Yukawa kernel law.\n"
                "- The clean bridge is `alpha_MTS(lambda_R)=Xi_R10[beta_S^R beta_T^R/(4 pi G Z_R)+alpha_boundary_tail]` with `lambda_R=sqrt(Z_R/M_R^2)`.\n"
                "- This is not a numeric prediction: `Z_R`, `M_R^2`, `beta_S^R`, `beta_T^R`, `Xi_R10`, and boundary/readout tails are still missing or unsigned.\n"
                "- The zero route is also not closed: constraint, matter-source silence, boundary silence, and cross-arena tau transfer all remain conditional or forbidden.\n"
                "- No R10 score, local GR/Newton reduction, PPN, WEP, clock, orbital, `Z_R=0`, `tau_R10=0`, or `q_R=0` claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Kernel Derivation Contract",
                md_table(derivation, ["derivation_id", "statement", "equation", "status", "blocking_gap"]),
                "## Zero Condition Audit",
                md_table(zeroes, ["zero_id", "zero_condition", "current_status", "claim_effect"]),
                "## Required Inputs",
                md_table(required, ["input_id", "symbol", "role", "minimum_required_form", "current_status"]),
                "## Scoring Interface Template",
                md_table(template, ["template_id", "lambda_R_m", "alpha_MTS", "current_status", "failure_if_used_now"]),
                "## Runner Nonclaim",
                md_table(runner, ["runner_id", "object", "status", "detail"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "consequence"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    derivation = kernel_derivation_rows()
    zeroes = zero_condition_rows()
    required = required_input_rows()
    template = scoring_template_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        KERNEL_DERIVATION,
        ZERO_CONDITIONS,
        REQUIRED_INPUTS,
        SCORING_TEMPLATE,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(KERNEL_DERIVATION, derivation)
    write_csv(ZERO_CONDITIONS, zeroes)
    write_csv(REQUIRED_INPUTS, required)
    write_csv(SCORING_TEMPLATE, template)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, derivation, zeroes, required, template, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
