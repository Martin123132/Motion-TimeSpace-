from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2876-Y5-R2FR-shared-green-sign-convention-source-or-two-branch-nonclaim-interface-under-AX1090.md"

SRC_2875_DOC = ROOT / "2875-Y5-R2FR-finite-first-triplet-acquisition-after-parent-action-clause-rejection-under-AX1090.md"
SRC_2875_NEXT = RESIDUALS / "P8_Y5_R2FR_2875_NEXT_TARGET.csv"
SRC_2875_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2875_VALIDATION.csv"
SRC_2875_ACQUISITION = RESIDUALS / "P8_Y5_R2FR_2875_FINITE_TRIPLET_ACQUISITION_MATRIX.csv"
SRC_2875_CONVENTION = RESIDUALS / "P8_Y5_R2FR_2875_WORKING_CONVENTION_NONCLAIM.csv"
SRC_2875_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2875_SOURCE_REQUEST_QUEUE.csv"
SRC_2875_GATES = RESIDUALS / "P8_Y5_R2FR_2875_ACCEPTANCE_GATES.csv"

SRC_2865_SIGMA = RESIDUALS / "P8_Y5_R2FR_2865_SIGMA_SOURCE_SIGN_EVIDENCE_SCAN.csv"
SRC_2865_GREEN = RESIDUALS / "P8_Y5_R2FR_2865_COMMON_GREEN_CONVENTION_AUDIT.csv"
SRC_2865_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2865_SIGN_BLOCKER_LEDGER.csv"
SRC_2865_GATES = RESIDUALS / "P8_Y5_R2FR_2865_SIGMA_ACCEPTANCE_GATE.csv"
SRC_2862_DICT = RESIDUALS / "P8_Y5_R2FR_2862_SIGMA_CANONICAL_DICTIONARY.csv"
SRC_2862_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2862_FIRST_ROW_SOURCE_REQUEST_PACK.csv"
SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_2871_LAW = RESIDUALS / "P8_Y5_R2FR_2871_QCAB_SOURCE_EQUATION_AUDIT.csv"
SRC_2872_LAW = RESIDUALS / "P8_Y5_R2FR_2872_QREFF_SOURCE_EQUATION_AUDIT.csv"
SRC_2874_REJECTION = RESIDUALS / "P8_Y5_R2FR_2874_PARENT_ORIGIN_REJECTION_LEDGER.csv"
SRC_2855_DRAFT = RESIDUALS / "P8_Y5_R2FR_2855_PARENT_SOURCE_EQUATION_DRAFT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2876_SOURCE_REGISTER.csv",
    "derivation": RESIDUALS / "P8_Y5_R2FR_2876_COMMON_RADIAL_CONVENTION_DERIVATION_AUDIT.csv",
    "sign_audit": RESIDUALS / "P8_Y5_R2FR_2876_SIGN_SOURCE_OWNER_AUDIT.csv",
    "interface": RESIDUALS / "P8_Y5_R2FR_2876_TWO_BRANCH_NONCLAIM_INTERFACE.csv",
    "promotion": RESIDUALS / "P8_Y5_R2FR_2876_PROMOTION_REQUIREMENTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2876_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2876_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2876_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2876_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2876_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2876_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "interface_copy": LOCAL_BOUNDS / "RAB_TWO_SIGN_FIRST_TRIPLET_INTERFACE_2876_NONCLAIM.csv",
    "promotion_copy": SOURCE_WEIGHT / "RAB_SIGN_GREEN_PROMOTION_REQUIREMENTS_2876_NONCLAIM.csv",
    "sign_copy": BETA_DOCS / "RAB_SIGN_SOURCE_OWNER_AUDIT_2876_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2876_first_finite_row_fill_under_two_sign_interface_NEXT.csv",
}


for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2876_0_2875_doc", SRC_2875_DOC, "Status: `Y5_R2FR_2875_finite_first_triplet_acquisition_pack_written_runner_refused_shared_green_sign_2876_next`;0/4", "2875 selected sign/common Green target after finite acquisition pack"),
        ("SRC2876_1_2875_next", SRC_2875_NEXT, "NEXT2875_0_2876", "handoff to 2876"),
        ("SRC2876_2_2875_validation", SRC_2875_VALIDATION, "VAL2875_OVERALL", "2875 validation"),
        ("SRC2876_3_2875_acquisition", SRC_2875_ACQUISITION, "ACQ2875_2_sigma_R_source_sign;ACQ2875_3_common_Green", "2875 acquisition rows for sign/Green"),
        ("SRC2876_4_2875_convention", SRC_2875_CONVENTION, "CONV2875_0_internal_radial_formula;CONV2875_3_sign_guard", "2875 working convention nonclaim"),
        ("SRC2876_5_2875_requests", SRC_2875_REQUESTS, "REQ2875_2_sigma_common_green", "2875 selected request"),
        ("SRC2876_6_2875_gates", SRC_2875_GATES, "GATE2875_2_sigma;GATE2875_3_common_green", "2875 fail-closed gates"),
        ("SRC2876_7_2865_sigma", SRC_2865_SIGMA, "SIGEV2865_0_canonical_source_sign;SIGEV2865_3_kernel_solution_sign;SIGEV2865_5_conditional_bridge", "sigma evidence scan"),
        ("SRC2876_8_2865_green", SRC_2865_GREEN, "GREEN2865_0_common_operator_pair;GREEN2865_3_radial_coefficient;GREEN2865_5_profile_import", "common Green/radial convention audit"),
        ("SRC2876_9_2865_blockers", SRC_2865_BLOCKERS, "BLOCK2865_0_SIGMA_SIGN;BLOCK2865_1_COMMON_GREEN;BLOCK2865_5_BOUNDARY_MEASURE", "sign/common/boundary blockers"),
        ("SRC2876_10_2865_gates", SRC_2865_GATES, "ACC2865_0_parent_action_sign;ACC2865_5_A_total_scoring", "sign acceptance gate"),
        ("SRC2876_11_2862_dict", SRC_2862_DICT, "SIG2862_0_source_sign;SIG2862_1_profile;SIG2862_2_bridge", "sigma semantic dictionary"),
        ("SRC2876_12_2862_requests", SRC_2862_REQUESTS, "REQ2862_2_sigma_R_source_sign;REQ2862_4_sigma_bridge", "source sign and bridge requests"),
        ("SRC2876_13_2844_flux", SRC_2844_FLUX, "FLUX2844_3_deltaR_amplitude;FLUX2844_4_local_ppn_amplitude;FLUX2844_5_local_suppression_condition", "conditional amplitude formula"),
        ("SRC2876_14_2871_law", SRC_2871_LAW, "LAW2871_1_operator_source_contract;LAW2871_5_common_green_sign", "Q_CAB radial convention contract"),
        ("SRC2876_15_2872_law", SRC_2872_LAW, "LAW2872_1_compact_source_charge;LAW2872_5_common_amplitude", "q_R_eff radial convention contract"),
        ("SRC2876_16_2874_rejection", SRC_2874_REJECTION, "REJ2874_6_total_route", "rank-one route demotion"),
        ("SRC2876_17_2855_draft", SRC_2855_DRAFT, "PEQ2855_2_sigma_sign;PEQ2855_3_amp_current_identity", "draft sign/current identity"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def derivation_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "derivation_id": "DER2876_0_CAB_leg",
            "step": "Read C_AB exterior coefficient",
            "formula": "C_AB=Q_CAB/(4*pi*r)+regular",
            "source_path": str(SRC_2871_LAW),
            "source_anchor": "LAW2871_1_operator_source_contract",
            "status": "WORKING_RADIAL_LEG_RECORDED",
            "claim_status": "NONCLAIM_UNTIL_L_CAB_J_CAB_BOUNDARY_SOURCE",
            "parent_owned": False,
        },
        {
            "derivation_id": "DER2876_1_deltaR_leg",
            "step": "Read delta_R exterior coefficient",
            "formula": "delta_R=sigma_R_source_sign*q_R_eff*exp(-r/ell_R)/(4*pi*r)+H_R",
            "source_path": str(SRC_2872_LAW),
            "source_anchor": "LAW2872_1_compact_source_charge",
            "status": "WORKING_RADIAL_LEG_RECORDED",
            "claim_status": "NONCLAIM_UNTIL_q_R_eff_ellR_HR_SIGN_SOURCE",
            "parent_owned": False,
        },
        {
            "derivation_id": "DER2876_2_A_total_formula",
            "step": "Combine radial legs in the same bookkeeping convention",
            "formula": "A_total=(Q_CAB+sigma_R_source_sign*q_R_eff)/(4*pi)",
            "source_path": str(SRC_2844_FLUX),
            "source_anchor": "FLUX2844_4_local_ppn_amplitude",
            "status": "FORMULA_RECORDED_NOT_SCORE_READY",
            "claim_status": "NONCLAIM_UNTIL_ALL_FIRST_TRIPLET_ROWS_PASS",
            "parent_owned": False,
        },
        {
            "derivation_id": "DER2876_3_suppression_condition",
            "step": "Record exact cancellation target",
            "formula": "A_total=0 iff Q_CAB=-sigma_R_source_sign*q_R_eff",
            "source_path": str(SRC_2844_FLUX),
            "source_anchor": "FLUX2844_5_local_suppression_condition",
            "status": "TARGET_CONDITION_ONLY",
            "claim_status": "NOT_PARENT_THEOREM_AFTER_2874",
            "parent_owned": False,
        },
        {
            "derivation_id": "DER2876_4_verdict",
            "step": "Shared radial convention verdict",
            "formula": "shared 4*pi bookkeeping can be written; physical sign cannot be chosen from current parent evidence",
            "source_path": str(SRC_2865_GREEN),
            "source_anchor": "GREEN2865_3_radial_coefficient",
            "status": "WORKING_CONVENTION_ONLY",
            "claim_status": "TWO_BRANCH_NONCLAIM_INTERFACE_REQUIRED",
            "parent_owned": False,
        },
    ]
    return [add_common(row) for row in rows]


def sign_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "SIGN2876_0_source_sign_slot",
            "object": "sigma_R_source_sign",
            "evidence": "canonical runner sign slot exists",
            "source_path": str(SRC_2862_DICT),
            "source_anchor": "SIG2862_0_source_sign",
            "status": "SLOT_DEFINED_OWNER_MISSING",
            "reason_not_parent_owned": "operator/Green/source sign not derived from parent quadratic action or source convention",
            "sign_chosen": "UNSET",
        },
        {
            "audit_id": "SIGN2876_1_profile_rejection",
            "object": "sigma_R_profile",
            "evidence": "weak-field profile is semantically distinct from source sign",
            "source_path": str(SRC_2862_DICT),
            "source_anchor": "SIG2862_1_profile",
            "status": "REJECT_AS_SOURCE_SIGN",
            "reason_not_parent_owned": "profile response cannot populate source sign without a bridge",
            "sign_chosen": "UNSET",
        },
        {
            "audit_id": "SIGN2876_2_kernel_orientation",
            "object": "delta_R Green sign",
            "evidence": "symbolic kernel orientation exists",
            "source_path": str(SRC_2865_SIGMA),
            "source_anchor": "SIGEV2865_3_kernel_solution_sign",
            "status": "SYMBOLIC_ONLY",
            "reason_not_parent_owned": "observable/source sign still requires parent source equation and signature convention",
            "sign_chosen": "UNSET",
        },
        {
            "audit_id": "SIGN2876_3_parent_action_sign",
            "object": "quadratic action sign",
            "evidence": "acceptance gate says parent action sign is absent",
            "source_path": str(SRC_2865_GATES),
            "source_anchor": "ACC2865_0_parent_action_sign",
            "status": "MISSING_PARENT_ACTION_SIGN",
            "reason_not_parent_owned": "no parent-signed S_R^(2), metric signature, or operator orientation",
            "sign_chosen": "UNSET",
        },
        {
            "audit_id": "SIGN2876_4_verdict",
            "object": "physical sign choice",
            "evidence": "no source owner found",
            "source_path": str(SRC_2865_BLOCKERS),
            "source_anchor": "BLOCK2865_0_SIGMA_SIGN",
            "status": "DO_NOT_CHOOSE_SIGN",
            "reason_not_parent_owned": "choosing + or - now would be a hidden closure assumption",
            "sign_chosen": "TWO_BRANCH_NONCLAIM_ONLY",
        },
    ]
    return [add_common(row) for row in rows]


def interface_rows() -> list[dict[str, Any]]:
    common = {
        "Q_CAB_input": "MISSING_Q_CAB",
        "q_R_eff_input": "MISSING_q_R_eff",
        "ell_R_input": "MISSING_ELL_R",
        "boundary_tail_input": "MISSING_BOUNDARY_POLICY",
        "GM_input": "MISSING_GM",
        "full_vector_input": "MISSING_FULL_LOCAL_VECTOR",
        "source_paths_valid": False,
        "numeric_value_present": False,
        "score_allowed": False,
        "runner_ready": False,
    }
    rows = [
        {
            "branch_id": "SIGBR2876_PLUS",
            "sigma_candidate": "+1",
            "A_total_formula": "(Q_CAB+q_R_eff)/(4*pi)",
            "interpretation": "positive source-sign branch retained for future smoke only",
            **common,
        },
        {
            "branch_id": "SIGBR2876_MINUS",
            "sigma_candidate": "-1",
            "A_total_formula": "(Q_CAB-q_R_eff)/(4*pi)",
            "interpretation": "negative source-sign branch retained for future smoke only",
            **common,
        },
        {
            "branch_id": "SIGBR2876_SYMBOLIC",
            "sigma_candidate": "sigma_R_source_sign",
            "A_total_formula": "(Q_CAB+sigma_R_source_sign*q_R_eff)/(4*pi)",
            "interpretation": "symbolic parent-sign branch remains the only claim-compatible form",
            **common,
        },
    ]
    return [add_common(row) for row in rows]


def promotion_rows() -> list[dict[str, Any]]:
    rows = [
        ("PROM2876_0_sign_owner", "sigma_R_source_sign", "parent kinetic/operator/source sign with metric signature and Green orientation", "MISSING_OPERATOR_GREEN_SIGN_OWNER"),
        ("PROM2876_1_Q_CAB", "Q_CAB", "finite source row or parent-zero theorem with L_CAB,J_CAB,boundary,units,branch,source anchor", "MISSING_Q_CAB"),
        ("PROM2876_2_q_R_eff", "q_R_eff", "finite compact-source Green row or source-zero theorem with ell_R,S_R/Z_R,H_R,units,source anchor", "MISSING_q_R_eff"),
        ("PROM2876_3_common_green", "common Green", "one parent-owned operator/radial coefficient convention tying both legs", "MISSING_COMMON_GREEN_CONVENTION"),
        ("PROM2876_4_boundary_tail", "boundary/tail", "zero/exact/included/finite boundary-tail row in same worldtube", "MISSING_BOUNDARY_POLICY"),
        ("PROM2876_5_GM", "measured GM", "same-frame source denominator and weak-field readout", "MISSING_GM"),
        ("PROM2876_6_full_vector", "full local vector", "same-branch gamma,beta,preferred,clock,orbital,q_loc,endpoint rows", "MISSING_FULL_LOCAL_VECTOR"),
    ]
    return [
        add_common(
            {
                "promotion_id": promotion_id,
                "object": obj,
                "required_to_promote": required,
                "current_blocker": blocker,
                "promotion_ready": False,
            }
        )
        for promotion_id, obj, required, blocker in rows
    ]


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2876_0_radial_formula", "shared symbolic 4*pi formula is recorded", "PASS_CONTROL_ONLY", "bookkeeping convention exists but is not parent-owned"),
        ("GATE2876_1_sign_owner", "physical sigma_R_source_sign is parent-owned", "FAIL", "operator/Green/source sign owner missing"),
        ("GATE2876_2_profile_guard", "sigma_R_profile cannot populate source sign", "PASS_GUARD_ONLY", "semantic split blocks profile import"),
        ("GATE2876_3_two_branch_interface", "both sign branches are explicit and nonclaim", "PASS_CONTROL_ONLY", "two sign rows written with runner_ready false"),
        ("GATE2876_4_first_triplet_values", "Q_CAB and q_R_eff values/theorems exist", "FAIL", "both finite rows remain missing"),
        ("GATE2876_5_runner", "A_total/local scorer can run", "FAIL", "interface has no numeric/provenance inputs"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
                "guard_passed_nonclaim": result == "PASS_GUARD_ONLY",
                "control_gate_recorded": result == "PASS_CONTROL_ONLY",
                "claim_unlocked": False,
            }
        )
        for gate_id, criterion, result, reason in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2876_0_two_branch_interface",
                "status": "REFUSED_FOR_SCORE_READY_FALSE",
                "branches_written": 3,
                "claim_ready_branches": 0,
                "score_ready_branches": 0,
                "reason": "two-branch interface is a future smoke scaffold only; no finite Q_CAB/q_R_eff/sign/provenance rows are accepted",
                "runner_ready": False,
                "score_allowed": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2876_0_sign_choice",
            "decision": "Choose + or - as the physical sigma_R_source_sign.",
            "result": "REFUSED",
            "because": "no parent sign owner exists; choosing would smuggle a closure axiom",
        },
        {
            "decision_id": "DEC2876_1_common_formula",
            "decision": "Record the shared 4*pi radial formula.",
            "result": "COMPLETE_NONCLAIM",
            "because": "it is needed for runner shape and source requests, but not enough for claims",
        },
        {
            "decision_id": "DEC2876_2_two_branch",
            "decision": "Write two-sign nonclaim interface.",
            "result": "COMPLETE_NONCLAIM",
            "because": "future tests can compare both sign branches without biasing the theory by hand",
        },
        {
            "decision_id": "DEC2876_3_next",
            "decision": "Move to first finite row fill under the two-sign interface.",
            "result": "SELECTED_2877",
            "because": "the interface is ready; progress now requires at least one real finite source row or parent-zero theorem",
        },
    ]
    return [add_common(row) for row in rows]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2876_0_2877",
                "status": "selected_primary",
                "target_doc": "2877-Y5-R2FR-first-finite-row-fill-under-two-sign-interface-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_first_finite_row_fill_under_two_sign_interface_under_AX1090_2877.py",
                "mission": "attempt to fill the first real finite row or parent-zero theorem under the two-sign interface, prioritizing the q_R_eff plus ell_R pair if source/range evidence exists, otherwise Q_CAB; keep both sign branches nonclaim until provenance passes",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    pairs = [
        ("COPY2876_0_interface", OUTPUTS["interface"], BRANCH_OUTPUTS["interface_copy"], "two-sign first-triplet interface nonclaim copy"),
        ("COPY2876_1_promotion", OUTPUTS["promotion"], BRANCH_OUTPUTS["promotion_copy"], "sign/Green promotion requirements nonclaim copy"),
        ("COPY2876_2_sign_audit", OUTPUTS["sign_audit"], BRANCH_OUTPUTS["sign_copy"], "sign source owner audit nonclaim copy"),
        ("COPY2876_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to first finite row fill"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in pairs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def generated_under_root(paths: list[Path]) -> bool:
    root_resolved = ROOT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "parent_owned",
        "source_paths_valid",
        "numeric_value_present",
        "score_allowed",
        "runner_ready",
        "promotion_ready",
        "gate_passed",
        "claim_unlocked",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["sources"]
    derivation = rows_by_name["derivation"]
    sign_audit = rows_by_name["sign_audit"]
    interface = rows_by_name["interface"]
    promotion = rows_by_name["promotion"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2876_0_sources_exist", all(row["path_exists"] for row in source_rows), "all registered source paths exist"),
        ("VAL2876_1_source_anchors", all(row["anchors_found"] for row in source_rows), "all registered source anchors were found"),
        ("VAL2876_2_radial_formula_recorded", any(row["derivation_id"] == "DER2876_2_A_total_formula" for row in derivation), "A_total working radial formula recorded"),
        ("VAL2876_3_no_parent_sign_choice", any(row["audit_id"] == "SIGN2876_4_verdict" and row["sign_chosen"] == "TWO_BRANCH_NONCLAIM_ONLY" for row in sign_audit), "physical sign is not chosen"),
        ("VAL2876_4_two_branch_interface_written", {row["branch_id"] for row in interface} >= {"SIGBR2876_PLUS", "SIGBR2876_MINUS", "SIGBR2876_SYMBOLIC"}, "plus, minus, and symbolic branches written"),
        ("VAL2876_5_interface_nonclaim", all(row["runner_ready"] is False and row["score_allowed"] is False for row in interface), "interface rows are nonclaim and not runner-ready"),
        ("VAL2876_6_promotion_requirements_complete", len(promotion) == 7 and all(row["promotion_ready"] is False for row in promotion), "promotion requirements remain explicit and unpassed"),
        ("VAL2876_7_gates_fail_claim_closed", all(row["gate_passed"] is False for row in gates), "all claim gates fail closed"),
        ("VAL2876_8_runner_refused", runner[0]["status"] == "REFUSED_FOR_SCORE_READY_FALSE" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2876_9_next_target_2877", next_target[0]["next_id"] == "NEXT2876_0_2877" and next_target[0]["selected"] is True, "2877 first finite row fill selected"),
        ("VAL2876_10_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2876_11_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2876_12_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2876_13_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2876_14_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2876_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2876_16_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": now(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2876_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2876 recorded the shared radial convention as nonclaim, refused to choose the physical sign, wrote plus/minus/symbolic two-branch smoke interface rows, and selected first finite row fill for 2877.",
            "timestamp_utc": now(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    text = f"""# 2876 - Y5 R2FR Shared Green Sign Convention Source Or Two Branch Nonclaim Interface Under AX1090

Status: `Y5_R2FR_2876_shared_radial_formula_recorded_sign_not_chosen_two_branch_nonclaim_interface_2877_next`

## Private Verdict

2876 does **not** pick the physical sign. That is the whole point.

The shared radial bookkeeping formula is clean:

`A_total=(Q_CAB+sigma_R_source_sign*q_R_eff)/(4*pi)`.

But the parent corpus still does not source `sigma_R_source_sign`. The profile `sigma_R_profile` is explicitly not the same object. So choosing `+1` or `-1` now would be a hidden closure axiom.

The productive move is a two-branch nonclaim interface: keep `sigma=+1`, `sigma=-1`, and symbolic `sigma_R_source_sign` rows side by side, all score-blocked until real `Q_CAB`, `q_R_eff`, `ell_R`, boundary, GM, and full-vector provenance exists. This gets us closer to testing without cheating the derivation.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Common Radial Convention Derivation Audit

{md_table(rows_by_name["derivation"], ["derivation_id", "step", "formula", "status", "claim_status", "parent_owned", "valid_for_claim"])}

## Sign Source Owner Audit

{md_table(rows_by_name["sign_audit"], ["audit_id", "object", "status", "reason_not_parent_owned", "sign_chosen", "valid_for_claim"])}

## Two Branch Nonclaim Interface

{md_table(rows_by_name["interface"], ["branch_id", "sigma_candidate", "A_total_formula", "interpretation", "Q_CAB_input", "q_R_eff_input", "runner_ready", "score_allowed", "valid_for_claim"])}

## Promotion Requirements

{md_table(rows_by_name["promotion"], ["promotion_id", "object", "required_to_promote", "current_blocker", "promotion_ready", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "guard_passed_nonclaim", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "branches_written", "claim_ready_branches", "score_ready_branches", "reason", "runner_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    remove_pycache()

    rows_by_name = {
        "sources": source_register_rows(),
        "derivation": derivation_rows(),
        "sign_audit": sign_audit_rows(),
        "interface": interface_rows(),
        "promotion": promotion_rows(),
        "gates": gate_rows(),
        "runner": runner_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branch_rows)
    rows_by_name["branches"] = branch_rows

    remove_pycache()
    validation = validation_rows(rows_by_name, branch_rows)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name, branch_rows, validation)
    remove_pycache()

    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation if row["validation_id"] == "VAL2876_OVERALL")
    print(f"VAL2876_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
