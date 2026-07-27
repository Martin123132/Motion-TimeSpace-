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

DOC = ROOT / "2875-Y5-R2FR-finite-first-triplet-acquisition-after-parent-action-clause-rejection-under-AX1090.md"

SRC_2874_DOC = ROOT / "2874-Y5-R2FR-rank-one-amplitude-parent-action-clause-search-under-AX1090.md"
SRC_2874_NEXT = RESIDUALS / "P8_Y5_R2FR_2874_NEXT_TARGET.csv"
SRC_2874_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2874_VALIDATION.csv"
SRC_2874_REJECTION = RESIDUALS / "P8_Y5_R2FR_2874_PARENT_ORIGIN_REJECTION_LEDGER.csv"
SRC_2874_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2874_EXACT_SOURCE_REQUESTS.csv"

SRC_2871_LAW = RESIDUALS / "P8_Y5_R2FR_2871_QCAB_SOURCE_EQUATION_AUDIT.csv"
SRC_2871_TEMPLATE = RESIDUALS / "P8_Y5_R2FR_2871_QCAB_FINITE_ROW_TEMPLATE_NONCLAIM.csv"
SRC_2871_REQUEST = RESIDUALS / "P8_Y5_R2FR_2871_NARROW_SOURCE_REQUEST.csv"
SRC_2871_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2871_VALIDATION.csv"
SRC_2872_LAW = RESIDUALS / "P8_Y5_R2FR_2872_QREFF_SOURCE_EQUATION_AUDIT.csv"
SRC_2872_TEMPLATE = RESIDUALS / "P8_Y5_R2FR_2872_QREFF_FINITE_ROW_TEMPLATE_NONCLAIM.csv"
SRC_2872_REQUEST = RESIDUALS / "P8_Y5_R2FR_2872_NARROW_SOURCE_REQUEST.csv"
SRC_2872_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2872_VALIDATION.csv"

SRC_2870_EXTRACTION = RESIDUALS / "P8_Y5_R2FR_2870_DEEP_EXTRACTION_RESULTS.csv"
SRC_2870_CANDIDATES = RESIDUALS / "P8_Y5_R2FR_2870_FIRST_TRIPLET_CANDIDATE_REVIEW.csv"
SRC_2870_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2870_REFINED_SOURCE_REQUESTS.csv"
SRC_2870_GATES = RESIDUALS / "P8_Y5_R2FR_2870_FIRST_TRIPLET_ACCEPTANCE_GATES.csv"
SRC_2870_RUNNER = RESIDUALS / "P8_Y5_R2FR_2870_RUNNER_STATUS.csv"
SRC_2870_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2870_VALIDATION.csv"

SRC_2868_ACQUISITION = RESIDUALS / "P8_Y5_R2FR_2868_FINITE_CORE_ACQUISITION_PACK.csv"
SRC_2868_SCHEMA = RESIDUALS / "P8_Y5_R2FR_2868_SOURCE_ROW_SCHEMA.csv"
SRC_2868_PREFLIGHT = RESIDUALS / "P8_Y5_R2FR_2868_ROW_READINESS_PREFLIGHT.csv"
SRC_2868_GATES = RESIDUALS / "P8_Y5_R2FR_2868_ACCEPTANCE_GATES.csv"
SRC_2868_RUNNER = RESIDUALS / "P8_Y5_R2FR_2868_RUNNER_REFUSAL.csv"
SRC_2868_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2868_VALIDATION.csv"

SRC_2862_DICT = RESIDUALS / "P8_Y5_R2FR_2862_SIGMA_CANONICAL_DICTIONARY.csv"
SRC_2862_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2862_FIRST_ROW_SOURCE_REQUEST_PACK.csv"
SRC_2863_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2863_QCAB_BLOCKER_LEDGER.csv"
SRC_2863_GATES = RESIDUALS / "P8_Y5_R2FR_2863_QCAB_ACCEPTANCE_GATE.csv"
SRC_2864_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2864_QREFF_BLOCKER_LEDGER.csv"
SRC_2864_GATES = RESIDUALS / "P8_Y5_R2FR_2864_QREFF_ACCEPTANCE_GATE.csv"
SRC_2865_SIGMA = RESIDUALS / "P8_Y5_R2FR_2865_SIGMA_SOURCE_SIGN_EVIDENCE_SCAN.csv"
SRC_2865_GREEN = RESIDUALS / "P8_Y5_R2FR_2865_COMMON_GREEN_CONVENTION_AUDIT.csv"
SRC_2865_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2865_SIGN_BLOCKER_LEDGER.csv"
SRC_2865_GATES = RESIDUALS / "P8_Y5_R2FR_2865_SIGMA_ACCEPTANCE_GATE.csv"

SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_2844_PACK = RESIDUALS / "P8_Y5_R2FR_2844_CAB_AMPLITUDE_SOURCE_PACK.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2855_DRAFT = RESIDUALS / "P8_Y5_R2FR_2855_PARENT_SOURCE_EQUATION_DRAFT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2875_SOURCE_REGISTER.csv",
    "acquisition": RESIDUALS / "P8_Y5_R2FR_2875_FINITE_TRIPLET_ACQUISITION_MATRIX.csv",
    "working_convention": RESIDUALS / "P8_Y5_R2FR_2875_WORKING_CONVENTION_NONCLAIM.csv",
    "template": RESIDUALS / "P8_Y5_R2FR_2875_STRICT_IMPORT_ROW_TEMPLATE.csv",
    "preflight": RESIDUALS / "P8_Y5_R2FR_2875_FIELD_READINESS_PREFLIGHT.csv",
    "candidate_rollup": RESIDUALS / "P8_Y5_R2FR_2875_CANDIDATE_REVIEW_ROLLUP.csv",
    "requests": RESIDUALS / "P8_Y5_R2FR_2875_SOURCE_REQUEST_QUEUE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2875_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2875_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2875_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2875_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2875_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2875_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "acquisition_copy": LOCAL_BOUNDS / "RAB_FINITE_FIRST_TRIPLET_ACQUISITION_MATRIX_2875_NONCLAIM.csv",
    "request_copy": SOURCE_WEIGHT / "RAB_FINITE_FIRST_TRIPLET_SOURCE_REQUEST_QUEUE_2875_NONCLAIM.csv",
    "template_copy": BETA_DOCS / "RAB_STRICT_FIRST_TRIPLET_IMPORT_TEMPLATE_2875_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2875_common_green_sign_convention_NEXT.csv",
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
        ("SRC2875_0_2874_doc", SRC_2874_DOC, "Status: `Y5_R2FR_2874_rank_one_parent_action_clause_not_source_backed_route_demoted_to_closure_only_2875_next`;move next to finite first-triplet acquisition", "2874 rejected theorem route and selected finite first-triplet acquisition"),
        ("SRC2875_1_2874_next", SRC_2874_NEXT, "NEXT2874_0_2875", "handoff to 2875"),
        ("SRC2875_2_2874_validation", SRC_2874_VALIDATION, "VAL2874_OVERALL", "2874 validation"),
        ("SRC2875_3_2874_rejection", SRC_2874_REJECTION, "REJ2874_6_total_route", "rank-one route closure-only verdict"),
        ("SRC2875_4_2874_requests", SRC_2874_REQUESTS, "REQ2874_0_rank_one_action_source;REQ2874_4_boundary_readout", "parent route source requests carried as nonclaim"),
        ("SRC2875_5_2871_law", SRC_2871_LAW, "LAW2871_1_operator_source_contract;LAW2871_6_verdict", "Q_CAB conditional source contract"),
        ("SRC2875_6_2871_template", SRC_2871_TEMPLATE, "TPL2871_0_QCAB_parent_source_row;TPL2871_3_BCAB_boundary", "Q_CAB finite row template"),
        ("SRC2875_7_2871_request", SRC_2871_REQUEST, "REQ2871_QCAB_PARENT_SOURCE_ROW", "Q_CAB narrow request"),
        ("SRC2875_8_2871_validation", SRC_2871_VALIDATION, "VAL2871_OVERALL", "2871 validation"),
        ("SRC2875_9_2872_law", SRC_2872_LAW, "LAW2872_1_compact_source_charge;LAW2872_6_verdict", "q_R_eff compact source contract"),
        ("SRC2875_10_2872_template", SRC_2872_TEMPLATE, "TPL2872_0_qReff_parent_source_row;TPL2872_4_tau_arena", "q_R_eff finite row template"),
        ("SRC2875_11_2872_request", SRC_2872_REQUEST, "REQ2872_QREFF_PARENT_SOURCE_ROW", "q_R_eff narrow request"),
        ("SRC2875_12_2872_validation", SRC_2872_VALIDATION, "VAL2872_OVERALL", "2872 validation"),
        ("SRC2875_13_2870_extraction", SRC_2870_EXTRACTION, "EXT2870_CAB;EXT2870_eff;EXT2870_sign;EXT2870_Green", "deep extraction found no accepted first-triplet rows"),
        ("SRC2875_14_2870_candidates", SRC_2870_CANDIDATES, "REV2870_CAND2869_CAB_01;REV2870_CAND2869_eff_15", "candidate rollup including one rejected possible q_R_eff hit"),
        ("SRC2875_15_2870_requests", SRC_2870_REQUESTS, "REQ2870_CAB;REQ2870_eff;REQ2870_sign;REQ2870_Green", "refined source requests"),
        ("SRC2875_16_2870_gates", SRC_2870_GATES, "GATE2870_0_Q_CAB;GATE2870_4_triplet_complete", "first-triplet acceptance gates"),
        ("SRC2875_17_2870_runner", SRC_2870_RUNNER, "RUN2870_0_A_total", "runner refusal"),
        ("SRC2875_18_2870_validation", SRC_2870_VALIDATION, "VAL2870_3_extraction_no_accepts;VAL2870_7_runner_refused", "2870 validation"),
        ("SRC2875_19_2868_acquisition", SRC_2868_ACQUISITION, "ACQ2868_0_Q_CAB;ACQ2868_7_full_local_vector", "finite core acquisition pack"),
        ("SRC2875_20_2868_schema", SRC_2868_SCHEMA, "SCHEMA2868_1_Q_CAB;SCHEMA2868_8_claim_flags", "strict source row schema"),
        ("SRC2875_21_2868_preflight", SRC_2868_PREFLIGHT, "PF2868_0_Q_CAB_value;PF2868_OVERALL", "strict row readiness preflight"),
        ("SRC2875_22_2868_gates", SRC_2868_GATES, "GATE2868_0_first_triplet;GATE2868_6_runner", "finite acquisition gates"),
        ("SRC2875_23_2868_runner", SRC_2868_RUNNER, "RUNREF2868_0_template;RUNREF2868_4_local_GR", "runner refusal guard"),
        ("SRC2875_24_2868_validation", SRC_2868_VALIDATION, "VAL2868_2_acquisition_covers_core;VAL2868_7_gates_fail_closed", "2868 validation"),
        ("SRC2875_25_2862_dict", SRC_2862_DICT, "SIG2862_0_source_sign;SIG2862_1_profile;SIG2862_2_bridge", "sigma semantic split"),
        ("SRC2875_26_2862_requests", SRC_2862_REQUESTS, "REQ2862_0_Q_CAB;REQ2862_4_sigma_bridge", "first-row request pack"),
        ("SRC2875_27_2863_blockers", SRC_2863_BLOCKERS, "BLOCK2863_0_Q_CAB_PARENT_INPUT;BLOCK2863_6_HANDOFF", "Q_CAB blockers"),
        ("SRC2875_28_2863_gates", SRC_2863_GATES, "ACC2863_0_value_or_zero;ACC2863_5_local_claim_guard", "Q_CAB gate refusal"),
        ("SRC2875_29_2864_blockers", SRC_2864_BLOCKERS, "BLOCK2864_0_q_R_eff_VALUE;BLOCK2864_7_QCAB_CARRY", "q_R_eff blockers"),
        ("SRC2875_30_2864_gates", SRC_2864_GATES, "ACC2864_0_value;ACC2864_7_runner_guard", "q_R_eff gate refusal"),
        ("SRC2875_31_2865_sigma", SRC_2865_SIGMA, "SIGEV2865_0_canonical_source_sign;SIGEV2865_5_conditional_bridge", "sigma evidence scan"),
        ("SRC2875_32_2865_green", SRC_2865_GREEN, "GREEN2865_0_common_operator_pair;GREEN2865_5_profile_import", "common Green audit"),
        ("SRC2875_33_2865_blockers", SRC_2865_BLOCKERS, "BLOCK2865_0_SIGMA_SIGN;BLOCK2865_5_BOUNDARY_MEASURE", "sign/common/boundary blockers"),
        ("SRC2875_34_2865_gates", SRC_2865_GATES, "ACC2865_0_parent_action_sign;ACC2865_5_A_total_scoring", "sign acceptance gate"),
        ("SRC2875_35_2844_flux", SRC_2844_FLUX, "FLUX2844_4_local_ppn_amplitude;FLUX2844_5_local_suppression_condition", "A_total conditional formula"),
        ("SRC2875_36_2844_pack", SRC_2844_PACK, "PACK2844_0_Q_CAB;PACK2844_4_q_R_eff", "amplitude source pack slots"),
        ("SRC2875_37_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_0_operator;CONTRACT2844_4_range", "parent amplitude contract"),
        ("SRC2875_38_2855_draft", SRC_2855_DRAFT, "PEQ2855_0_CAB_source;PEQ2855_3_amp_current_identity", "source equation draft"),
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


def acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "acquisition_id": "ACQ2875_0_Q_CAB",
            "layer": "first_triplet",
            "quantity": "Q_CAB",
            "required_object": "finite target-map/source monopole or parent-zero theorem",
            "strict_acceptance": "finite Q_CAB or Q_CAB=0 theorem with L_CAB,J_CAB/rho_CAB,boundary policy, units, branch, source path and equation anchor",
            "best_current_source": str(SRC_2871_LAW),
            "best_current_anchor": "LAW2871_1_operator_source_contract",
            "current_status": "CONTRACT_WRITTEN_VALUE_MISSING",
            "blocking_marker": "MISSING_Q_CAB",
            "accepted_source_present": False,
            "numeric_or_theorem_zero_present": False,
            "ready_for_strict_runner": False,
        },
        {
            "acquisition_id": "ACQ2875_1_q_R_eff",
            "layer": "first_triplet",
            "quantity": "q_R_eff",
            "required_object": "finite residual-curvature compact-source Green charge or source-zero theorem",
            "strict_acceptance": "finite q_R_eff or q_R_eff=0 theorem with S_R/Z_R, ell_R/long-range hierarchy, H_R boundary, units, branch, source path and equation anchor",
            "best_current_source": str(SRC_2872_LAW),
            "best_current_anchor": "LAW2872_1_compact_source_charge",
            "current_status": "CONTRACT_WRITTEN_VALUE_AND_RANGE_MISSING",
            "blocking_marker": "MISSING_q_R_eff;MISSING_ELL_R",
            "accepted_source_present": False,
            "numeric_or_theorem_zero_present": False,
            "ready_for_strict_runner": False,
        },
        {
            "acquisition_id": "ACQ2875_2_sigma_R_source_sign",
            "layer": "first_triplet",
            "quantity": "sigma_R_source_sign",
            "required_object": "operator/Green/source sign multiplying q_R_eff",
            "strict_acceptance": "parent sign convention with metric signature, kinetic/operator sign, Green orientation, source equation convention and no sigma_R_profile import",
            "best_current_source": str(SRC_2865_SIGMA),
            "best_current_anchor": "SIGEV2865_0_canonical_source_sign",
            "current_status": "SEMANTIC_SLOT_DEFINED_SIGN_OWNER_MISSING",
            "blocking_marker": "MISSING_sigma_R_source_sign",
            "accepted_source_present": False,
            "numeric_or_theorem_zero_present": False,
            "ready_for_strict_runner": False,
        },
        {
            "acquisition_id": "ACQ2875_3_common_Green",
            "layer": "first_triplet",
            "quantity": "shared Green/radial convention",
            "required_object": "one exterior 4*pi radial convention for C_AB and delta_R",
            "strict_acceptance": "C_AB=Q_CAB/(4*pi*r)+regular and delta_R=sigma_R_source_sign*q_R_eff*exp(-r/ell_R)/(4*pi*r)+H_R in one parent-owned operator/range/sign convention",
            "best_current_source": str(SRC_2865_GREEN),
            "best_current_anchor": "GREEN2865_3_radial_coefficient",
            "current_status": "WORKING_CONVENTION_RECORDED_PARENT_OWNER_MISSING",
            "blocking_marker": "MISSING_COMMON_GREEN_CONVENTION",
            "accepted_source_present": False,
            "numeric_or_theorem_zero_present": False,
            "ready_for_strict_runner": False,
        },
        {
            "acquisition_id": "ACQ2875_4_boundary_tail",
            "layer": "second_layer",
            "quantity": "B_CAB+B_R+K_amp+regular_tail",
            "required_object": "boundary/tail zero, exact, included charge, or finite arena-projected bound",
            "strict_acceptance": "worldtube/corner rule, compact support, tail bound, source path and equation anchor",
            "best_current_source": str(SRC_2844_CONTRACT),
            "best_current_anchor": "CONTRACT2844_2_boundary",
            "current_status": "BOUNDARY_AND_TAIL_OWNER_MISSING",
            "blocking_marker": "MISSING_BOUNDARY_POLICY;MISSING_TAIL_BOUND",
            "accepted_source_present": False,
            "numeric_or_theorem_zero_present": False,
            "ready_for_strict_runner": False,
        },
        {
            "acquisition_id": "ACQ2875_5_measured_GM_readout",
            "layer": "second_layer",
            "quantity": "measured GM/source denominator",
            "required_object": "same-frame weak-field mass/readout denominator",
            "strict_acceptance": "M_source/GM relation, source worldtube measure, observed metric/coframe readout and units",
            "best_current_source": str(SRC_2868_ACQUISITION),
            "best_current_anchor": "ACQ2868_5_measured_GM",
            "current_status": "GM_PARENT_GLUE_MISSING",
            "blocking_marker": "MISSING_GM",
            "accepted_source_present": False,
            "numeric_or_theorem_zero_present": False,
            "ready_for_strict_runner": False,
        },
        {
            "acquisition_id": "ACQ2875_6_full_local_vector",
            "layer": "third_layer",
            "quantity": "full local residual vector",
            "required_object": "same-branch PPN/clock/orbital/q_loc/endpoint vector",
            "strict_acceptance": "gamma,beta,preferred-frame,conservation,clock,orbital,q_loc and endpoint rows finite or theorem-zero in one branch",
            "best_current_source": str(SRC_2868_ACQUISITION),
            "best_current_anchor": "ACQ2868_7_full_local_vector",
            "current_status": "FULL_VECTOR_MISSING",
            "blocking_marker": "MISSING_FULL_LOCAL_VECTOR",
            "accepted_source_present": False,
            "numeric_or_theorem_zero_present": False,
            "ready_for_strict_runner": False,
        },
        {
            "acquisition_id": "ACQ2875_7_A_total_runner",
            "layer": "runner_guard",
            "quantity": "A_total",
            "required_object": "strict numerator scorer",
            "strict_acceptance": "A_total=(Q_CAB+sigma_R_source_sign*q_R_eff)/(4*pi) only after ACQ2875_0 through ACQ2875_6 pass",
            "best_current_source": str(SRC_2844_FLUX),
            "best_current_anchor": "FLUX2844_4_local_ppn_amplitude",
            "current_status": "FORMULA_READY_INPUTS_MISSING",
            "blocking_marker": "FIRST_TRIPLET_INCOMPLETE",
            "accepted_source_present": False,
            "numeric_or_theorem_zero_present": False,
            "ready_for_strict_runner": False,
        },
    ]
    return [add_common(row) for row in rows]


def working_convention_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "convention_id": "CONV2875_0_internal_radial_formula",
            "formula": "A_total=(Q_CAB+sigma_R_source_sign*q_R_eff)/(4*pi)",
            "source_path": str(SRC_2844_FLUX),
            "source_anchor": "FLUX2844_4_local_ppn_amplitude",
            "internal_use": "may be used to shape future smoke-runner columns",
            "claim_use": "forbidden until source-backed rows and parent/common convention pass",
            "parent_owned": False,
            "runner_column_ready": False,
        },
        {
            "convention_id": "CONV2875_1_CAB_radial_leg",
            "formula": "C_AB=Q_CAB/(4*pi*r)+regular",
            "source_path": str(SRC_2871_LAW),
            "source_anchor": "LAW2871_1_operator_source_contract",
            "internal_use": "Q_CAB slot definition",
            "claim_use": "forbidden until L_CAB,J_CAB,boundary and units are sourced",
            "parent_owned": False,
            "runner_column_ready": False,
        },
        {
            "convention_id": "CONV2875_2_deltaR_radial_leg",
            "formula": "delta_R=sigma_R_source_sign*q_R_eff*exp(-r/ell_R)/(4*pi*r)+H_R",
            "source_path": str(SRC_2872_LAW),
            "source_anchor": "LAW2872_1_compact_source_charge",
            "internal_use": "q_R_eff and ell_R slot definition",
            "claim_use": "forbidden until q_R_eff,ell_R,H_R and sign are sourced",
            "parent_owned": False,
            "runner_column_ready": False,
        },
        {
            "convention_id": "CONV2875_3_sign_guard",
            "formula": "sigma_R_source_sign != sigma_R_profile unless a parent bridge is supplied",
            "source_path": str(SRC_2862_DICT),
            "source_anchor": "SIG2862_0_source_sign;SIG2862_1_profile;SIG2862_2_bridge",
            "internal_use": "blocks accidental profile import",
            "claim_use": "profile-as-sign forbidden",
            "parent_owned": False,
            "runner_column_ready": False,
        },
    ]
    return [add_common(row) for row in rows]


def strict_template_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "row_id": "CAND2875_0_first_triplet_import_template_nonclaim",
                "branch_id": "R2FR_local_PPN_after_rank_one_parent_action_rejection",
                "arena_id": "R10_PPN_CLOCK_ORBITAL_LOCAL_VECTOR",
                "Q_CAB_value": "MISSING_Q_CAB",
                "Q_CAB_units": "MISSING_Q_CAB_UNITS",
                "Q_CAB_source_path": "MISSING_PARENT_SOURCE_PATH",
                "Q_CAB_equation_anchor": "MISSING_EQUATION_ANCHOR",
                "q_R_eff_value": "MISSING_q_R_eff",
                "q_R_eff_units": "MISSING_q_R_eff_UNITS",
                "q_R_eff_source_path": "MISSING_PARENT_SOURCE_PATH",
                "q_R_eff_equation_anchor": "MISSING_EQUATION_ANCHOR",
                "ell_R_value": "MISSING_ELL_R",
                "sigma_R_source_sign": "MISSING_sigma_R_source_sign",
                "sigma_source_path": "MISSING_PARENT_SOURCE_PATH",
                "sigma_equation_anchor": "MISSING_EQUATION_ANCHOR",
                "common_green_convention": "MISSING_COMMON_GREEN_CONVENTION",
                "boundary_policy": "MISSING_BOUNDARY_POLICY",
                "tail_bound": "MISSING_TAIL_BOUND",
                "GM_value": "MISSING_GM",
                "full_vector_status": "MISSING_FULL_LOCAL_VECTOR",
                "theorem_zero_authority": "NONE_PARENT_SIGNED",
                "numeric_value_present": False,
                "source_paths_valid": False,
                "no_missing_markers": False,
                "runner_ready": False,
            }
        )
    ]


def preflight_rows() -> list[dict[str, Any]]:
    fields = [
        ("PF2875_0_Q_CAB", "Q_CAB_value", "MISSING_Q_CAB", "finite numeric or accepted theorem-zero", False, "MISSING_OR_UNSOURCED"),
        ("PF2875_1_q_R_eff", "q_R_eff_value", "MISSING_q_R_eff", "finite numeric or accepted theorem-zero", False, "MISSING_OR_UNSOURCED"),
        ("PF2875_2_ell_R", "ell_R_value", "MISSING_ELL_R", "positive range or accepted long-range hierarchy", False, "MISSING_RANGE"),
        ("PF2875_3_sigma", "sigma_R_source_sign", "MISSING_sigma_R_source_sign", "parent operator/Green/source sign", False, "MISSING_SIGN_OWNER"),
        ("PF2875_4_common_green", "common_green_convention", "MISSING_COMMON_GREEN_CONVENTION", "one sourced 4*pi radial convention", False, "MISSING_COMMON_CONVENTION"),
        ("PF2875_5_boundary_tail", "boundary_policy/tail_bound", "MISSING_BOUNDARY_POLICY;MISSING_TAIL_BOUND", "zero/exact/included/finite bound", False, "MISSING_BOUNDARY_TAIL"),
        ("PF2875_6_GM", "GM_value", "MISSING_GM", "same-frame measured source denominator", False, "MISSING_GM_GLUE"),
        ("PF2875_7_full_vector", "full_vector_status", "MISSING_FULL_LOCAL_VECTOR", "full same-branch local residual vector", False, "MISSING_FULL_VECTOR"),
        ("PF2875_8_source_paths", "source paths and anchors", "MISSING_PARENT_SOURCE_PATH;MISSING_EQUATION_ANCHOR", "existing source paths and anchors for every live row", False, "MISSING_PROVENANCE"),
        ("PF2875_9_no_closure_shortcut", "theorem_zero_authority", "NONE_PARENT_SIGNED", "rank-one/U_amp closure route cannot substitute for finite rows", False, "GUARD_PASS_ONLY_NOT_RUNNER_READY"),
        ("PF2875_OVERALL", "strict_import_template", "contains MISSING markers", "all finite source rows and conventions present", False, "REFUSED_MISSING_PROVENANCE_OR_INPUTS"),
    ]
    return [
        add_common(
            {
                "preflight_id": preflight_id,
                "field": field,
                "value_or_marker": marker,
                "requirement": requirement,
                "preflight_passed": passed,
                "failure_reason": reason,
                "guard_passed_nonclaim": preflight_id == "PF2875_9_no_closure_shortcut",
            }
        )
        for preflight_id, field, marker, requirement, passed, reason in fields
    ]


def candidate_rollup_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "rollup_id": "ROLL2875_0_Q_CAB",
            "quantity": "Q_CAB",
            "candidate_source": str(SRC_2870_EXTRACTION),
            "candidate_anchor": "EXT2870_CAB",
            "review_verdict": "NO_ACCEPTED_SOURCE_ROW",
            "reason": "reviewed candidates were blockers, requests, schemas, placeholders, or closure-only rows",
            "accepted_source_candidate": False,
        },
        {
            "rollup_id": "ROLL2875_1_q_R_eff",
            "quantity": "q_R_eff",
            "candidate_source": str(SRC_2870_EXTRACTION),
            "candidate_anchor": "EXT2870_eff",
            "review_verdict": "NO_ACCEPTED_SOURCE_ROW",
            "reason": "one possible-source-looking row was rejected for manual provenance and wrong target class; finite q_R_eff/ell_R remain unsourced",
            "accepted_source_candidate": False,
        },
        {
            "rollup_id": "ROLL2875_2_sigma",
            "quantity": "sigma_R_source_sign",
            "candidate_source": str(SRC_2870_EXTRACTION),
            "candidate_anchor": "EXT2870_sign",
            "review_verdict": "NO_ACCEPTED_SOURCE_ROW",
            "reason": "profile sigma and symbolic sign rows are not a source-sign convention",
            "accepted_source_candidate": False,
        },
        {
            "rollup_id": "ROLL2875_3_common_green",
            "quantity": "shared Green/radial convention",
            "candidate_source": str(SRC_2870_EXTRACTION),
            "candidate_anchor": "EXT2870_Green",
            "review_verdict": "NO_ACCEPTED_SOURCE_ROW",
            "reason": "working formula exists, but parent-owned operator pair/sign/range hierarchy is not accepted",
            "accepted_source_candidate": False,
        },
        {
            "rollup_id": "ROLL2875_4_rank_one_theorem",
            "quantity": "theorem-zero shortcut",
            "candidate_source": str(SRC_2874_REJECTION),
            "candidate_anchor": "REJ2874_6_total_route",
            "review_verdict": "DEMOTED_TO_CLOSURE_ONLY",
            "reason": "rank-one action/source/boundary/readout clauses are unsigned",
            "accepted_source_candidate": False,
        },
    ]
    return [add_common(row) for row in rows]


def request_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "request_id": "REQ2875_0_Q_CAB",
            "priority": 1,
            "quantity": "Q_CAB",
            "needed_source": "finite source monopole or parent-zero theorem",
            "exact_request": "Fill Q_CAB with source_path, equation_anchor, units, branch_id, L_CAB, J_CAB/rho_CAB, boundary/corner policy, and finite value or parent-signed zero theorem.",
            "acceptance_rule": "no MISSING markers, no request/schema/blocker row, no U_amp closure-only authority",
            "status": "OPEN_SOURCE_REQUEST",
            "selected_for_next": False,
        },
        {
            "request_id": "REQ2875_1_q_R_eff",
            "priority": 2,
            "quantity": "q_R_eff",
            "needed_source": "finite compact-source Green charge or source-zero theorem",
            "exact_request": "Fill q_R_eff with q_R_eff=-int_W S_R/Z_R d^3x plus boundary term, ell_R or long-range hierarchy, H_R policy, units, source support, source_path and equation_anchor.",
            "acceptance_rule": "must share convention with Q_CAB and sigma_R_source_sign",
            "status": "OPEN_SOURCE_REQUEST",
            "selected_for_next": False,
        },
        {
            "request_id": "REQ2875_2_sigma_common_green",
            "priority": 3,
            "quantity": "sigma_R_source_sign + common Green",
            "needed_source": "parent-owned source sign and exterior radial convention",
            "exact_request": "Derive/source the common operator/radial sign convention: C_AB=Q_CAB/(4*pi*r)+..., delta_R=sigma_R_source_sign*q_R_eff*exp(-r/ell_R)/(4*pi*r)+H_R, with metric signature, kinetic sign, source equation convention and range hierarchy.",
            "acceptance_rule": "sigma_R_profile is rejected unless a parent bridge is supplied; working convention alone is nonclaim",
            "status": "OPEN_SOURCE_REQUEST",
            "selected_for_next": True,
        },
        {
            "request_id": "REQ2875_3_boundary_tail",
            "priority": 4,
            "quantity": "boundary/tail",
            "needed_source": "zero/exact/included/finite boundary-tail row",
            "exact_request": "Supply boundary/corner/tail theorem or finite row for K_amp+B_CAB+sigma_R_source_sign*B_R and C_AB_reg+H_R in each arena.",
            "acceptance_rule": "must specify worldtube, compact support, arena validity and source path",
            "status": "OPEN_SOURCE_REQUEST",
            "selected_for_next": False,
        },
        {
            "request_id": "REQ2875_4_GM_readout",
            "priority": 5,
            "quantity": "measured GM/readout",
            "needed_source": "same-frame source denominator and weak-field readout",
            "exact_request": "Supply M_source/GM relation, worldtube measure, observed metric/coframe readout and units for the same branch as Q_CAB and q_R_eff.",
            "acceptance_rule": "must not be a separate calibration denominator imported after the fact",
            "status": "OPEN_SOURCE_REQUEST",
            "selected_for_next": False,
        },
        {
            "request_id": "REQ2875_5_full_vector",
            "priority": 6,
            "quantity": "full local vector",
            "needed_source": "same-branch local residual vector",
            "exact_request": "Supply finite/theorem-zero rows for gamma,beta,preferred-frame,conservation,clock,orbital,q_loc and endpoint/readout in the same branch.",
            "acceptance_rule": "gamma-only local-GR pass is rejected",
            "status": "OPEN_SOURCE_REQUEST",
            "selected_for_next": False,
        },
    ]
    return [add_common(row) for row in rows]


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2875_0_Q_CAB", "Q_CAB finite/theorem-zero row accepted", "FAIL", "Q_CAB contract exists but value/zero theorem/provenance missing"),
        ("GATE2875_1_q_R_eff", "q_R_eff finite/theorem-zero row accepted", "FAIL", "q_R_eff contract exists but value/range/source density/boundary missing"),
        ("GATE2875_2_sigma", "sigma_R_source_sign accepted", "FAIL", "sign slot defined but operator/Green/source owner missing"),
        ("GATE2875_3_common_green", "common Green/radial convention accepted for claims", "FAIL", "working formula exists but parent owner missing"),
        ("GATE2875_4_boundary_tail", "boundary/tail row accepted", "FAIL", "worldtube/corner/tail row missing"),
        ("GATE2875_5_GM", "measured GM/readout accepted", "FAIL", "same-frame source denominator missing"),
        ("GATE2875_6_full_vector", "full local residual vector accepted", "FAIL", "full PPN/clock/orbital/q_loc vector missing"),
        ("GATE2875_7_no_shortcut", "rank-one closure route not used as theorem-zero", "PASS_GUARD_ONLY", "2874 demotion is enforced, but this does not unlock scoring"),
        ("GATE2875_8_runner", "strict A_total/local runner can score", "FAIL", "0/4 first-triplet claim rows and 0/3 supporting rows pass"),
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
                "claim_unlocked": False,
            }
        )
        for gate_id, criterion, result, reason in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2875_0_first_triplet_strict_import",
                "status": "REFUSED",
                "accepted_first_triplet_rows": 0,
                "required_first_triplet_rows": 4,
                "accepted_support_rows": 0,
                "required_support_rows": 3,
                "working_formula_recorded": True,
                "reason": "strict template still contains MISSING markers; rank-one theorem route is closure-only; A_total/local-GR scoring remains locked",
                "runner_ready": False,
                "score_allowed": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2875_0_route",
            "decision": "Use rank-one theorem-zero as A_total proof.",
            "result": "REFUSED",
            "because": "2874 found no source-backed parent action/source/boundary clause",
        },
        {
            "decision_id": "DEC2875_1_pack",
            "decision": "Build finite first-triplet acquisition pack.",
            "result": "COMPLETE_NONCLAIM",
            "because": "Q_CAB, q_R_eff, sigma, common Green, boundary/tail, GM and full vector slots are explicit and machine-checkable",
        },
        {
            "decision_id": "DEC2875_2_formula",
            "decision": "Retain A_total formula as working convention.",
            "result": "RECORDED_NONCLAIM",
            "because": "the formula shapes the runner but cannot substitute for source rows",
        },
        {
            "decision_id": "DEC2875_3_runner",
            "decision": "Run A_total/local-GR scorer.",
            "result": "REFUSED",
            "because": "0/4 first-triplet claim rows pass and support rows are missing",
        },
        {
            "decision_id": "DEC2875_4_next",
            "decision": "Attack the shared sign/common Green source first.",
            "result": "SELECTED_2876",
            "because": "it is the narrowest derivation-shaped choke point that makes later finite Q_CAB/q_R_eff rows comparable rather than two independent numbers",
        },
    ]
    return [add_common(row) for row in rows]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2875_0_2876",
                "status": "selected_primary",
                "target_doc": "2876-Y5-R2FR-shared-green-sign-convention-source-or-two-branch-nonclaim-interface-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_shared_green_sign_convention_source_or_two_branch_nonclaim_interface_under_AX1090_2876.py",
                "mission": "derive/source the shared exterior 4*pi Green/sign convention tying Q_CAB and q_R_eff, or if parent ownership still fails, create a two-sign nonclaim smoke interface that keeps both branches explicit without scoring claims",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    pairs = [
        ("COPY2875_0_acquisition", OUTPUTS["acquisition"], BRANCH_OUTPUTS["acquisition_copy"], "finite first-triplet acquisition matrix nonclaim copy"),
        ("COPY2875_1_requests", OUTPUTS["requests"], BRANCH_OUTPUTS["request_copy"], "finite first-triplet source request queue nonclaim copy"),
        ("COPY2875_2_template", OUTPUTS["template"], BRANCH_OUTPUTS["template_copy"], "strict first-triplet import template nonclaim copy"),
        ("COPY2875_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to shared Green/sign convention target"),
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
        "accepted_source_present",
        "numeric_or_theorem_zero_present",
        "ready_for_strict_runner",
        "runner_column_ready",
        "numeric_value_present",
        "source_paths_valid",
        "no_missing_markers",
        "runner_ready",
        "preflight_passed",
        "accepted_source_candidate",
        "gate_passed",
        "claim_unlocked",
        "score_allowed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["sources"]
    acquisition = rows_by_name["acquisition"]
    convention = rows_by_name["working_convention"]
    template = rows_by_name["template"]
    preflight = rows_by_name["preflight"]
    rollup = rows_by_name["candidate_rollup"]
    requests = rows_by_name["requests"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2875_0_sources_exist", all(row["path_exists"] for row in source_rows), "all registered source paths exist"),
        ("VAL2875_1_source_anchors", all(row["anchors_found"] for row in source_rows), "all registered source anchors were found"),
        ("VAL2875_2_acquisition_covers_required_rows", len(acquisition) == 8 and {row["quantity"] for row in acquisition} >= {"Q_CAB", "q_R_eff", "sigma_R_source_sign", "shared Green/radial convention"}, "acquisition matrix covers first triplet plus support rows"),
        ("VAL2875_3_no_accepted_rows", all(row["accepted_source_present"] is False and row["ready_for_strict_runner"] is False for row in acquisition), "no source row is accepted prematurely"),
        ("VAL2875_4_working_convention_nonclaim", len(convention) == 4 and all(row["parent_owned"] is False and row["runner_column_ready"] is False for row in convention), "working convention recorded as nonclaim only"),
        ("VAL2875_5_template_blocks_runner", "MISSING_Q_CAB" in template[0]["Q_CAB_value"] and template[0]["runner_ready"] is False, "strict import template contains explicit missing markers and runner is false"),
        ("VAL2875_6_preflight_refuses", any(row["preflight_id"] == "PF2875_OVERALL" and row["preflight_passed"] is False for row in preflight), "overall preflight refuses import"),
        ("VAL2875_7_candidate_rollup_no_accepts", len(rollup) >= 5 and not any(row["accepted_source_candidate"] for row in rollup), "candidate rollup carries no accepted first-triplet candidate"),
        ("VAL2875_8_requests_prioritized", any(row["request_id"] == "REQ2875_2_sigma_common_green" and row["selected_for_next"] is True for row in requests), "source request queue selects shared sign/common Green next"),
        ("VAL2875_9_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "all claim gates fail closed"),
        ("VAL2875_10_runner_refused", runner[0]["status"] == "REFUSED" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2875_11_next_target_2876", next_target[0]["next_id"] == "NEXT2875_0_2876" and next_target[0]["selected"] is True, "2876 shared Green/sign target selected"),
        ("VAL2875_12_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2875_13_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2875_14_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2875_15_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2875_16_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2875_17_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2875_18_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
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
            "validation_id": "VAL2875_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2875 built the finite first-triplet acquisition pack after rank-one parent-action rejection, kept all rows nonclaim, refused the strict runner, and selected shared Green/sign convention or two-branch nonclaim interface for 2876.",
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
    text = f"""# 2875 - Y5 R2FR Finite First Triplet Acquisition After Parent Action Clause Rejection Under AX1090

Status: `Y5_R2FR_2875_finite_first_triplet_acquisition_pack_written_runner_refused_shared_green_sign_2876_next`

## Private Verdict

2875 converts the failed rank-one parent-action route into the practical finite-row route. The local cancellation target is still:

`A_total=(Q_CAB+sigma_R_source_sign*q_R_eff)/(4*pi)`.

But that formula is only a working convention until the row set is real. The current state is still `0/4` for the first triplet: no accepted `Q_CAB`, no accepted `q_R_eff`, no accepted `sigma_R_source_sign`, and no parent-owned shared Green/radial convention. The support layer is also blocked: boundary/tail, measured `GM`, and full local residual vector are missing.

This is not a failure of the framework; it is the honest shape of the next work. The useful progress here is that the strict import row, preflight, request queue, and next choke point are now explicit. No `A_total`, local-GR, Newton, R10, PPN, clock, orbital, or WEP claim is unlocked.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Finite Triplet Acquisition Matrix

{md_table(rows_by_name["acquisition"], ["acquisition_id", "layer", "quantity", "current_status", "blocking_marker", "accepted_source_present", "ready_for_strict_runner", "valid_for_claim"])}

## Working Convention Nonclaim

{md_table(rows_by_name["working_convention"], ["convention_id", "formula", "internal_use", "claim_use", "parent_owned", "runner_column_ready", "valid_for_claim"])}

## Strict Import Row Template

{md_table(rows_by_name["template"], ["row_id", "branch_id", "arena_id", "Q_CAB_value", "q_R_eff_value", "sigma_R_source_sign", "common_green_convention", "boundary_policy", "GM_value", "full_vector_status", "runner_ready", "valid_for_claim"])}

## Field Readiness Preflight

{md_table(rows_by_name["preflight"], ["preflight_id", "field", "value_or_marker", "requirement", "preflight_passed", "failure_reason", "valid_for_claim"])}

## Candidate Review Rollup

{md_table(rows_by_name["candidate_rollup"], ["rollup_id", "quantity", "review_verdict", "reason", "accepted_source_candidate", "valid_for_claim"])}

## Source Request Queue

{md_table(rows_by_name["requests"], ["request_id", "priority", "quantity", "needed_source", "status", "selected_for_next", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "guard_passed_nonclaim", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_first_triplet_rows", "required_first_triplet_rows", "accepted_support_rows", "required_support_rows", "reason", "runner_ready", "valid_for_claim"])}

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
        "acquisition": acquisition_rows(),
        "working_convention": working_convention_rows(),
        "template": strict_template_rows(),
        "preflight": preflight_rows(),
        "candidate_rollup": candidate_rollup_rows(),
        "requests": request_rows(),
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
    overall = next(row for row in validation if row["validation_id"] == "VAL2875_OVERALL")
    print(f"VAL2875_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
