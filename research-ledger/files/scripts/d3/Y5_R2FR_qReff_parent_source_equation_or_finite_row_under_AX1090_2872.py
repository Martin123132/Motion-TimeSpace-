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

DOC = ROOT / "2872-Y5-R2FR-qReff-parent-source-equation-or-finite-row-under-AX1090.md"

SRC_2871_DOC = ROOT / "2871-Y5-R2FR-QCAB-parent-source-equation-or-finite-row-under-AX1090.md"
SRC_2871_NEXT = RESIDUALS / "P8_Y5_R2FR_2871_NEXT_TARGET.csv"
SRC_2871_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2871_VALIDATION.csv"
SRC_2870_REVIEW = RESIDUALS / "P8_Y5_R2FR_2870_FIRST_TRIPLET_CANDIDATE_REVIEW.csv"
SRC_2870_EXTRACTION = RESIDUALS / "P8_Y5_R2FR_2870_DEEP_EXTRACTION_RESULTS.csv"
SRC_2870_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2870_REFINED_SOURCE_REQUESTS.csv"

SRC_2864_DOC = ROOT / "2864-Y5-R2FR-qReff-first-source-row-or-parent-normalization-owner-under-AX1090.md"
SRC_2864_EVIDENCE = RESIDUALS / "P8_Y5_R2FR_2864_QREFF_SOURCE_EVIDENCE_SCAN.csv"
SRC_2864_NORMALIZATION = RESIDUALS / "P8_Y5_R2FR_2864_QREFF_PARENT_NORMALIZATION_AUDIT.csv"
SRC_2864_ACCEPTANCE = RESIDUALS / "P8_Y5_R2FR_2864_QREFF_ACCEPTANCE_GATE.csv"
SRC_2864_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2864_QREFF_BLOCKER_LEDGER.csv"
SRC_2864_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2864_VALIDATION.csv"

SRC_2839_KERNEL = RESIDUALS / "P8_Y5_R2FR_2839_GREEN_KERNEL_NORMALIZATION.csv"
SRC_2839_SELECTOR = RESIDUALS / "P8_Y5_R2FR_2839_FIRST_SOURCE_ROW_SELECTOR.csv"
SRC_2839_ZERO = RESIDUALS / "P8_Y5_R2FR_2839_THEOREM_ZERO_OR_SOURCE_ROW_ATTEMPT.csv"
SRC_2839_DIM = RESIDUALS / "P8_Y5_R2FR_2839_DIMENSIONAL_CONTRACT.csv"
SRC_2839_PROJ = RESIDUALS / "P8_Y5_R2FR_2839_ARENA_PROJECTION_CONTRACT.csv"
SRC_2840_PACK = RESIDUALS / "P8_Y5_R2FR_2840_NORMALIZATION_PACK_CONTRACT.csv"
SRC_2840_FILL = RESIDUALS / "P8_Y5_R2FR_2840_FIRST_PACK_FILL_ATTEMPT_NONCLAIM.csv"
SRC_2840_ZERO = RESIDUALS / "P8_Y5_R2FR_2840_PARENT_ZERO_CERTIFICATE_AUDIT.csv"
SRC_2841_BRIDGE = RESIDUALS / "P8_Y5_R2FR_2841_QREFF_TO_QRHAT_CONDITIONAL_BRIDGE.csv"
SRC_2841_COND = RESIDUALS / "P8_Y5_R2FR_2841_PPN_BRIDGE_CONDITIONS.csv"
SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_2844_PACK = RESIDUALS / "P8_Y5_R2FR_2844_CAB_AMPLITUDE_SOURCE_PACK.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2850_HUNT = RESIDUALS / "P8_Y5_R2FR_2850_PARENT_EQUATION_HUNT_LEDGER.csv"
SRC_2855_EQUATION_DRAFT = RESIDUALS / "P8_Y5_R2FR_2855_PARENT_SOURCE_EQUATION_DRAFT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2872_SOURCE_REGISTER.csv",
    "review": RESIDUALS / "P8_Y5_R2FR_2872_QREFF_EVIDENCE_REVIEW.csv",
    "source_law": RESIDUALS / "P8_Y5_R2FR_2872_QREFF_SOURCE_EQUATION_AUDIT.csv",
    "zero_audit": RESIDUALS / "P8_Y5_R2FR_2872_QREFF_PARENT_ZERO_AUDIT.csv",
    "template": RESIDUALS / "P8_Y5_R2FR_2872_QREFF_FINITE_ROW_TEMPLATE_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2872_ACCEPTANCE_GATES.csv",
    "request": RESIDUALS / "P8_Y5_R2FR_2872_NARROW_SOURCE_REQUEST.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2872_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2872_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2872_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2872_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2872_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "law_copy": LOCAL_BOUNDS / "RAB_QREFF_SOURCE_EQUATION_AUDIT_2872_NONCLAIM.csv",
    "request_copy": SOURCE_WEIGHT / "RAB_QREFF_NARROW_SOURCE_REQUEST_2872_NONCLAIM.csv",
    "template_copy": BETA_DOCS / "RAB_QREFF_FINITE_ROW_TEMPLATE_2872_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2872_first_triplet_parent_reentry_NEXT.csv",
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
        ("SRC2872_0_2871_doc", SRC_2871_DOC, "NEXT2871_0_2872;VAL2871_OVERALL", "2871 selected q_R_eff single-row focus"),
        ("SRC2872_1_2871_next", SRC_2871_NEXT, "NEXT2871_0_2872", "handoff into 2872"),
        ("SRC2872_2_2871_validation", SRC_2871_VALIDATION, "VAL2871_OVERALL", "2871 validation"),
        ("SRC2872_3_2870_review", SRC_2870_REVIEW, "REV2870_CAND2869_eff_01;REV2870_CAND2869_eff_15", "first-triplet q_R_eff candidate review"),
        ("SRC2872_4_2870_extraction", SRC_2870_EXTRACTION, "EXT2870_eff", "q_R_eff deep extraction refusal"),
        ("SRC2872_5_2870_requests", SRC_2870_REQUESTS, "REQ2870_eff", "refined q_R_eff source request"),
        ("SRC2872_6_2864_doc", SRC_2864_DOC, "VAL2864_OVERALL;EVID2864_1_compact_body_charge;ACC2864_0_value", "prior q_R_eff source-row attempt"),
        ("SRC2872_7_2864_evidence", SRC_2864_EVIDENCE, "EVID2864_0_normalized_operator;EVID2864_1_compact_body_charge;EVID2864_7_conditional_ppn_bridge", "prior q_R_eff evidence scan"),
        ("SRC2872_8_2864_normalization", SRC_2864_NORMALIZATION, "NORM2864_0_operator;NORM2864_6_verdict", "prior normalization audit"),
        ("SRC2872_9_2864_acceptance", SRC_2864_ACCEPTANCE, "ACC2864_0_value;ACC2864_7_runner_guard", "prior q_R_eff acceptance gates"),
        ("SRC2872_10_2864_blockers", SRC_2864_BLOCKERS, "BLOCK2864_0_q_R_eff_VALUE;BLOCK2864_3_SR_ZR;BLOCK2864_5_BOUNDARY", "prior q_R_eff blockers"),
        ("SRC2872_11_2864_validation", SRC_2864_VALIDATION, "VAL2864_OVERALL", "2864 validation"),
        ("SRC2872_12_2839_kernel", SRC_2839_KERNEL, "KER2839_1_normalized_operator;KER2839_3_solution;KER2839_4_compact_body", "normalized Yukawa kernel"),
        ("SRC2872_13_2839_selector", SRC_2839_SELECTOR, "SEL2839_0_minimal_pair;SEL2839_4_projection", "first finite row selector"),
        ("SRC2872_14_2839_zero", SRC_2839_ZERO, "ZOS2839_2_try_JR_zero;ZOS2839_4_first_source_row", "source-zero attempt"),
        ("SRC2872_15_2839_dim", SRC_2839_DIM, "DIM2839_1_ell;DIM2839_3_point_charge", "dimension contract"),
        ("SRC2872_16_2839_proj", SRC_2839_PROJ, "PROJ2839_0_R10;PROJ2839_1_PPN;PROJ2839_4_WEP", "arena projection contract"),
        ("SRC2872_17_2840_pack", SRC_2840_PACK, "PACK2840_0_range;PACK2840_1_amplitude;PACK2840_3_boundary", "normalization pack contract"),
        ("SRC2872_18_2840_fill", SRC_2840_FILL, "FILL2840_0_first_RAB_finite_pack;MISSING_Q_R_EFF", "failed finite pack fill"),
        ("SRC2872_19_2840_zero", SRC_2840_ZERO, "PZ2840_2_source_zero;PZ2840_5_joint_certificate", "parent zero certificate audit"),
        ("SRC2872_20_2841_bridge", SRC_2841_BRIDGE, "BRG2841_0_kernel_exterior;BRG2841_4_qRhat_map;BRG2841_5_delta_p_map", "conditional PPN bridge"),
        ("SRC2872_21_2841_cond", SRC_2841_COND, "COND2841_2_long_range;COND2841_3_sign;COND2841_4_GM", "PPN bridge conditions"),
        ("SRC2872_22_2844_flux", SRC_2844_FLUX, "FLUX2844_3_deltaR_amplitude;FLUX2844_4_local_ppn_amplitude", "A_delta/A_total conditional amplitude"),
        ("SRC2872_23_2844_pack", SRC_2844_PACK, "PACK2844_4_q_R_eff;PACK2844_5_tail_bound", "q_R_eff source pack slot"),
        ("SRC2872_24_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_0_operator;CONTRACT2844_4_range;CONTRACT2844_5_sign", "common Green/range/sign contract"),
        ("SRC2872_25_2850_hunt", SRC_2850_HUNT, "HUNT2850_1_q_R_eff;HUNT2850_4_relation", "parent source equation hunt"),
        ("SRC2872_26_2855_source_equation", SRC_2855_EQUATION_DRAFT, "PEQ2855_1_R_source;PEQ2855_3_amp_current_identity", "draft R-source equation and shared-current identity"),
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


def evidence_review_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "review_id": "REV2872_0_normalized_operator",
            "quantity": "q_R_eff",
            "source_path": str(SRC_2839_KERNEL),
            "source_anchor": "KER2839_1_normalized_operator",
            "candidate": "(-Laplace+ell_R^-2) delta_R=-S_R/Z_R with ell_R^2=Z_R/M_R^2",
            "verdict": "SYMBOLIC_OPERATOR_ONLY",
            "reason_not_accepted": "does not source finite ell_R, S_R/Z_R, or parent sign convention",
        },
        {
            "review_id": "REV2872_1_compact_body_charge",
            "quantity": "q_R_eff",
            "source_path": str(SRC_2839_KERNEL),
            "source_anchor": "KER2839_4_compact_body",
            "candidate": "delta_R=q_R_eff exp(-r/ell_R)/(4*pi*r)+boundary_homogeneous; q_R_eff=-int_body S_R/Z_R d^3x",
            "verdict": "SYMBOLIC_KERNEL_ONLY",
            "reason_not_accepted": "defines the charge but lacks finite integral value, source support, units/source path, and boundary class",
        },
        {
            "review_id": "REV2872_2_range_amplitude_pair",
            "quantity": "ell_R+q_R_eff",
            "source_path": str(SRC_2839_SELECTOR),
            "source_anchor": "SEL2839_0_minimal_pair",
            "candidate": "first finite row must source ell_R plus q_R_eff or equivalent source amplitude",
            "verdict": "SCHEMA_NOT_FILLED",
            "reason_not_accepted": "range and amplitude are selected but still missing",
        },
        {
            "review_id": "REV2872_3_pack_amplitude",
            "quantity": "q_R_eff",
            "source_path": str(SRC_2840_PACK),
            "source_anchor": "PACK2840_1_amplitude",
            "candidate": "q_R_eff=-integral_body S_R/Z_R d^3x, length units",
            "verdict": "MISSING_Q_R_EFF",
            "reason_not_accepted": "normalization pack marks the amplitude missing",
        },
        {
            "review_id": "REV2872_4_parent_source_draft",
            "quantity": "q_R_eff",
            "source_path": str(SRC_2855_EQUATION_DRAFT),
            "source_anchor": "PEQ2855_1_R_source",
            "candidate": "L_R delta_R=J_R; q_R_eff=integral_W J_R dV + surface_integral_boundary B_R",
            "verdict": "DRAFT_EQUATION_NOT_PARENT_DERIVED",
            "reason_not_accepted": "draft requires parent L_R, J_R, Green normalization, and boundary policy",
        },
        {
            "review_id": "REV2872_5_conditional_bridge",
            "quantity": "q_R_eff_to_q_R_hat",
            "source_path": str(SRC_2841_BRIDGE),
            "source_anchor": "BRG2841_4_qRhat_map",
            "candidate": "q_R_hat=-sigma_R*q_R_eff*c^2/(4*pi*G*M_source)",
            "verdict": "CONDITIONAL_OBSERVABLE_MAP_ONLY",
            "reason_not_accepted": "requires source mass convention, sign, q_R_eff value, boundary and range conditions",
        },
        {
            "review_id": "REV2872_6_prior_normalization_verdict",
            "quantity": "q_R_eff",
            "source_path": str(SRC_2864_NORMALIZATION),
            "source_anchor": "NORM2864_6_verdict",
            "candidate": "q_R_eff finite row or parent normalization owner accepted",
            "verdict": "NOT_ACCEPTED",
            "reason_not_accepted": "q_R_eff remains missing source normalization",
        },
        {
            "review_id": "REV2872_7_deep_extraction",
            "quantity": "q_R_eff",
            "source_path": str(SRC_2870_EXTRACTION),
            "source_anchor": "EXT2870_eff",
            "candidate": "2870 deep extraction over top q_R_eff candidates",
            "verdict": "NO_ACCEPTED_SOURCE_ROW",
            "reason_not_accepted": "top rows are blockers, placeholders, requests, or one unresolved possible candidate",
        },
    ]
    for row in rows:
        row.update(
            {
                "accepted_source_row": False,
                "finite_numeric_value_present": False,
                "parent_zero_theorem_present": False,
            }
        )
    return [add_common(row) for row in rows]


def source_law_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "law_id": "LAW2872_0_static_parent_operator",
            "clause": "static residual operator",
            "conditional_statement": "If the finite residual Euler equation has E_R=-Div(Z_R Grad delta_R)+M_R^2 delta_R+S_R=0 with constant positive Z_R and M_R^2, then L_R delta_R=J_R becomes (-Laplace+ell_R^-2)delta_R=-S_R/Z_R and ell_R^2=Z_R/M_R^2.",
            "derived_status": "DERIVED_CONDITIONAL_OPERATOR",
            "parent_status": "SYMBOLIC_NOT_SOURCE_BACKED",
            "missing_for_claim": "finite Z_R/M_R^2 or direct ell_R; parent sign/metric convention; source path and equation anchor",
            "source_path": str(SRC_2839_KERNEL),
            "source_anchor": "KER2839_0_static_operator;KER2839_1_normalized_operator",
        },
        {
            "law_id": "LAW2872_1_compact_source_charge",
            "clause": "q_R_eff source integral",
            "conditional_statement": "For compact S_R/Z_R and the normalized Green kernel G_ell=exp(-r/ell_R)/(4*pi*r), the exterior solution is delta_R(r)=q_R_eff exp(-r/ell_R)/(4*pi*r)+H_R(r), with q_R_eff=-int_W S_R/Z_R d^3x plus any owned boundary contribution.",
            "derived_status": "DERIVED_CONDITIONAL_SOURCE_CONTRACT",
            "parent_status": "SOURCE_VALUE_NOT_SOURCED",
            "missing_for_claim": "finite integral value or source-zero theorem; source support; units; boundary/no-hair class; branch id",
            "source_path": str(SRC_2839_KERNEL),
            "source_anchor": "KER2839_3_solution;KER2839_4_compact_body",
        },
        {
            "law_id": "LAW2872_2_dimension_range_pair",
            "clause": "range/amplitude paired row",
            "conditional_statement": "A runner-ready q_R_eff row must carry ell_R and q_R_eff together; with dimensionless delta_R, q_R_eff has length units in the 1/r convention.",
            "derived_status": "REQUIRED_CLAUSE_IDENTIFIED",
            "parent_status": "MISSING_ELL_R_AND_Q_R_EFF_PAIR",
            "missing_for_claim": "ell_R value or theorem/hierarchy plus q_R_eff value/theorem in the same row family",
            "source_path": str(SRC_2839_SELECTOR),
            "source_anchor": "SEL2839_0_minimal_pair",
        },
        {
            "law_id": "LAW2872_3_long_range_ppn_limit",
            "clause": "local one-over-r limit",
            "conditional_statement": "Only if r_arena/ell_R << 1 and H_R is zero/bounded does delta_R reduce to q_R_eff/(4*pi*r) for the local PPN amplitude lane.",
            "derived_status": "DERIVED_CONDITIONAL_LIMIT",
            "parent_status": "RANGE_AND_BOUNDARY_NOT_SOURCED",
            "missing_for_claim": "arena scale hierarchy, finite ell_R, and no-hair/boundary theorem or finite H_R bound",
            "source_path": str(SRC_2841_BRIDGE),
            "source_anchor": "BRG2841_1_ppn_long_range_limit",
        },
        {
            "law_id": "LAW2872_4_observable_bridge",
            "clause": "q_R_eff to q_R_hat",
            "conditional_statement": "The bridge q_R_hat=-sigma_R*q_R_eff*c^2/(4*pi*G*M_source) is usable only after sigma_R_source_sign, measured GM, C_R=delta_R, range, and boundary conditions close.",
            "derived_status": "DERIVED_IF_MATCH_CONDITIONS_HOLD",
            "parent_status": "CONDITIONAL_OBSERVABLE_MAP_ONLY",
            "missing_for_claim": "sigma_R_source_sign, M_source/GM owner, q_R_eff value, boundary class and range conditions",
            "source_path": str(SRC_2841_BRIDGE),
            "source_anchor": "BRG2841_4_qRhat_map",
        },
        {
            "law_id": "LAW2872_5_common_amplitude",
            "clause": "shared A_total convention",
            "conditional_statement": "q_R_eff can enter A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi) only in the same exterior 4*pi radial convention as Q_CAB and with a parent-owned sigma_R_source_sign.",
            "derived_status": "REQUIRED_CLAUSE_IDENTIFIED",
            "parent_status": "MISSING_COMMON_GREEN_SIGN_CONVENTION",
            "missing_for_claim": "Q_CAB accepted row, sigma_R_source_sign, and shared Green/sign convention",
            "source_path": str(SRC_2844_FLUX),
            "source_anchor": "FLUX2844_3_deltaR_amplitude;FLUX2844_4_local_ppn_amplitude",
        },
        {
            "law_id": "LAW2872_6_verdict",
            "clause": "q_R_eff source law acceptance",
            "conditional_statement": "The exact q_R_eff source contract is explicit, but it remains nonclaim: no finite q_R_eff, no finite ell_R/hierarchy, and no parent-zero theorem are accepted.",
            "derived_status": "CONTRACT_WRITTEN",
            "parent_status": "NOT_ACCEPTED_FOR_CLAIM",
            "missing_for_claim": "L_R/J_R source owner, S_R/Z_R, ell_R, boundary/no-hair class, units, branch id, common sign/Green, and source path/equation anchor",
            "source_path": str(SRC_2864_NORMALIZATION),
            "source_anchor": "NORM2864_6_verdict",
        },
    ]
    for row in rows:
        row.update(
            {
                "source_equation_parent_accepted": False,
                "finite_row_ready": False,
                "parent_zero_ready": False,
            }
        )
    return [add_common(row) for row in rows]


def zero_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "zero_id": "ZERO2872_0_source_silence",
            "theorem_route": "S_R/Z_R integrates to zero over compact body",
            "needed_premise": "J_R, Pi_R and readout source terms vanish or are exact with zero monopole in the parent branch",
            "current_status": "NOT_DERIVED",
            "blocker": "MISSING_JR_SOURCE_SILENCE_THEOREM",
            "source_path": str(SRC_2864_NORMALIZATION),
            "source_anchor": "NORM2864_2_source_zero",
        },
        {
            "zero_id": "ZERO2872_1_boundary_homogeneous",
            "theorem_route": "H_R boundary homogeneous mode is zero or bounded below local thresholds",
            "needed_premise": "parent no-hair/boundary class removes unowned homogeneous source",
            "current_status": "NOT_DERIVED",
            "blocker": "MISSING_BOUNDARY_HOMOGENEOUS_CLASS",
            "source_path": str(SRC_2864_NORMALIZATION),
            "source_anchor": "NORM2864_3_boundary_homogeneous",
        },
        {
            "zero_id": "ZERO2872_2_mass_gap_or_range",
            "theorem_route": "finite range decouples local arenas or ell_R hierarchy is sourced",
            "needed_premise": "ell_R is finite and mapped, or ell_R >> arena scale is explicitly accepted",
            "current_status": "NOT_SOURCED",
            "blocker": "MISSING_ELL_R_OR_ZR_MR2_SOURCE",
            "source_path": str(SRC_2864_NORMALIZATION),
            "source_anchor": "NORM2864_0_operator",
        },
        {
            "zero_id": "ZERO2872_3_shared_current_balance",
            "theorem_route": "J_CAB+sigma_R J_R=dK_amp forces Q_CAB+sigma_R q_R_eff=0",
            "needed_premise": "one parent current identity owns both charges, boundary terms, and forbids independent rescaling",
            "current_status": "DERIVATION_ATTEMPT_REQUIRES_PARENT_IDENTITY",
            "blocker": "MISSING_PARENT_CURRENT_OWNER_AND_SIGMA_SOURCE_SIGN",
            "source_path": str(SRC_2855_EQUATION_DRAFT),
            "source_anchor": "PEQ2855_3_amp_current_identity",
        },
        {
            "zero_id": "ZERO2872_4_arena_readout_silence",
            "theorem_route": "q_R_eff exists but projects to zero in R10/PPN/clock/orbital arenas",
            "needed_premise": "tau_R10, tau_PPN, tau_clock, and tau_orbital are all parent-zero or bounded",
            "current_status": "NOT_SCORE_READY",
            "blocker": "MISSING_ARENA_PROJECTION",
            "source_path": str(SRC_2839_PROJ),
            "source_anchor": "PROJ2839_0_R10;PROJ2839_1_PPN",
        },
        {
            "zero_id": "ZERO2872_5_verdict",
            "theorem_route": "q_R_eff=0 or no local residual theorem",
            "needed_premise": "source silence, boundary silence, range/hierarchy, readout silence, and common convention all close",
            "current_status": "NOT_ACCEPTED",
            "blocker": "q_R_eff_ZERO_NOT_PARENT_SIGNED",
            "source_path": str(SRC_2864_NORMALIZATION),
            "source_anchor": "NORM2864_6_verdict",
        },
    ]
    for row in rows:
        row.update(
            {
                "parent_signed": False,
                "qreff_zero_accepted": False,
                "accepted_source_row": False,
            }
        )
    return [add_common(row) for row in rows]


def template_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "template_id": "TPL2872_0_qReff_parent_source_row",
            "quantity": "q_R_eff",
            "required_equation": "L_R delta_R=J_R; normalized form (-Laplace+ell_R^-2)delta_R=-S_R/Z_R; q_R_eff=-int_W S_R/Z_R d^3x + boundary term",
            "value": "MISSING_q_R_eff",
            "units": "length_if_delta_R_dimensionless_else_DECLARED_UNITS",
            "source_path": "MISSING_PARENT_SOURCE_PATH",
            "equation_anchor": "MISSING_EQUATION_ANCHOR",
            "branch_id": "MISSING_BRANCH_ID",
            "status": "TEMPLATE_ONLY_NOT_LIVE_ROW",
            "ready_for_runner": False,
        },
        {
            "template_id": "TPL2872_1_ellR_range",
            "quantity": "ell_R",
            "required_equation": "ell_R^2=Z_R/M_R^2 or direct sourced range/hierarchy",
            "value": "MISSING_ELL_R",
            "units": "length",
            "source_path": "MISSING_PARENT_SOURCE_PATH",
            "equation_anchor": "MISSING_RANGE_ANCHOR",
            "branch_id": "MISSING_BRANCH_ID",
            "status": "TEMPLATE_ONLY_NOT_LIVE_ROW",
            "ready_for_runner": False,
        },
        {
            "template_id": "TPL2872_2_SRZR_source_density",
            "quantity": "S_R/Z_R",
            "required_equation": "compact-body source density from parent variation with support and units",
            "value": "MISSING_S_R_OVER_Z_R",
            "units": "MISSING_SOURCE_DENSITY_UNITS",
            "source_path": "MISSING_PARENT_SOURCE_PATH",
            "equation_anchor": "MISSING_SOURCE_ANCHOR",
            "branch_id": "MISSING_BRANCH_ID",
            "status": "TEMPLATE_ONLY_NOT_LIVE_ROW",
            "ready_for_runner": False,
        },
        {
            "template_id": "TPL2872_3_HR_boundary",
            "quantity": "H_R",
            "required_equation": "boundary homogeneous/no-hair class is zero, bounded, or included",
            "value": "MISSING_H_R_BOUNDARY_CLASS",
            "units": "same_as_delta_R_profile",
            "source_path": "MISSING_PARENT_SOURCE_PATH",
            "equation_anchor": "MISSING_BOUNDARY_ANCHOR",
            "branch_id": "MISSING_BRANCH_ID",
            "status": "TEMPLATE_ONLY_NOT_LIVE_ROW",
            "ready_for_runner": False,
        },
        {
            "template_id": "TPL2872_4_tau_arena",
            "quantity": "tau_R10/tau_PPN/tau_clock/tau_orbital",
            "required_equation": "arena projection from delta_R profile to observables",
            "value": "MISSING_ARENA_PROJECTION",
            "units": "arena_dependent",
            "source_path": "MISSING_PARENT_SOURCE_PATH",
            "equation_anchor": "MISSING_PROJECTION_ANCHOR",
            "branch_id": "MISSING_BRANCH_ID",
            "status": "TEMPLATE_ONLY_NOT_LIVE_ROW",
            "ready_for_runner": False,
        },
    ]
    for row in rows:
        row.update(
            {
                "accepted_source_row": False,
                "finite_numeric_value_present": False,
                "parent_zero_theorem_present": False,
            }
        )
    return [add_common(row) for row in rows]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2872_0_finite_value_or_zero", "finite q_R_eff value or parent-zero theorem", "FAIL", "no numeric/source-backed q_R_eff and no parent-signed zero theorem"),
        ("GATE2872_1_parent_source_equation", "parent L_R delta_R=J_R accepted", "FAIL", "source equation is symbolic/draft, not parent-owned"),
        ("GATE2872_2_range", "ell_R positive range or long-range hierarchy sourced", "FAIL", "ell_R or Z_R/M_R^2 remains missing"),
        ("GATE2872_3_source_density_units", "S_R/Z_R compact source density has units/support", "FAIL", "source density normalization and support remain missing"),
        ("GATE2872_4_boundary", "H_R boundary/no-hair class closed", "FAIL", "boundary homogeneous mode remains unowned"),
        ("GATE2872_5_common_green_sign", "same 4*pi radial convention as Q_CAB with sigma_R_source_sign", "FAIL", "Q_CAB, sigma_R_source_sign and common Green remain unaccepted"),
        ("GATE2872_6_arena_projection", "R10/PPN/clock/orbital projection exists", "FAIL", "arena projections remain missing"),
        ("GATE2872_7_Atotal_unlock", "A_total numerator can use q_R_eff", "FAIL", "q_R_eff remains blocked and first triplet is incomplete"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
                "runner_ready": False,
            }
        )
        for gate_id, criterion, result, reason in specs
    ]


def request_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "request_id": "REQ2872_QREFF_PARENT_SOURCE_ROW",
                "quantity": "q_R_eff",
                "needed_source": "one parent-owned q_R_eff compact-source Green row or theorem-zero proof",
                "narrow_request": "Provide the exact parent equation for the residual-curvature amplitude sector: L_R delta_R=J_R, or normalized (-Laplace+ell_R^-2)delta_R=-S_R/Z_R, with exterior delta_R=q_R_eff exp(-r/ell_R)/(4*pi*r)+H_R and q_R_eff=-int_W S_R/Z_R d^3x plus any owned boundary term. It must include finite q_R_eff or q_R_eff=0 theorem, ell_R or accepted long-range hierarchy, S_R/Z_R units/support, H_R boundary/no-hair policy, branch id, source path, equation anchor, measured-GM/readout convention, and the sign/common-Green convention tying it to Q_CAB and sigma_R_source_sign.",
                "must_not_be": "schema row; source request; blocker ledger; closure-only U_amp relation; fitted cancellation; profile-import sign; Z_R without source density; M_R^2 without Z_R/range",
                "status": "OPEN_SOURCE_REQUEST",
                "ready_for_runner": False,
            }
        )
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2872_0_QREFF_gate",
                "status": "REFUSED",
                "accepted_qreff_rows": 0,
                "required_qreff_rows": 1,
                "accepted_first_triplet_rows": 0,
                "required_first_triplet_rows": 4,
                "reason": "conditional q_R_eff source contract is explicit, but no finite/source-backed q_R_eff value, ell_R/range, or parent-zero theorem passed the gates",
                "runner_ready": False,
                "score_allowed": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2872_0_contract", "Write exact q_R_eff source contract.", "COMPLETE_CONDITIONAL", "the normalized Green law and compact-source charge are mathematically clear."),
        ("DEC2872_1_acceptance", "Promote q_R_eff to accepted row.", "REJECTED", "finite q_R_eff, ell_R, S_R/Z_R, boundary class, and common convention remain missing."),
        ("DEC2872_2_zero", "Prove q_R_eff=0.", "NOT_PROVEN", "source silence, boundary silence, range decoupling, and readout silence are not parent-signed."),
        ("DEC2872_3_runner", "Unlock A_total runner.", "REFUSED", "q_R_eff is still unaccepted and first-triplet rows remain incomplete."),
        ("DEC2872_4_next", "Move from row hunts to first-triplet parent re-entry identity.", "SELECTED_2873", "Q_CAB and q_R_eff now have exact source contracts, so the real next leap is one parent identity owning both charges plus sigma/common Green."),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
            }
        )
        for decision_id, decision, result, because in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2872_0_2873",
                "status": "selected_primary",
                "target_doc": "2873-Y5-R2FR-first-triplet-parent-source-current-identity-reentry-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_first_triplet_parent_source_current_identity_reentry_under_AX1090_2873.py",
                "mission": "attempt the parent re-entry identity for the first triplet: derive or reject one parent current/action owner for J_CAB + sigma_R J_R = dK_amp, shared 4*pi Green convention, boundary silence, and no independent current rescaling; if unsigned, produce the exact parent-action clause request and keep A_total locked",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("COPY2872_0_law", OUTPUTS["source_law"], BRANCH_OUTPUTS["law_copy"], "q_R_eff conditional source-equation audit nonclaim copy"),
        ("COPY2872_1_request", OUTPUTS["request"], BRANCH_OUTPUTS["request_copy"], "narrow q_R_eff source request nonclaim copy"),
        ("COPY2872_2_template", OUTPUTS["template"], BRANCH_OUTPUTS["template_copy"], "q_R_eff finite-row template nonclaim copy"),
        ("COPY2872_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to first-triplet parent re-entry"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_true_fields = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "valid_prediction_row",
        "accepted_source_row",
        "finite_numeric_value_present",
        "parent_zero_theorem_present",
        "source_equation_parent_accepted",
        "finite_row_ready",
        "parent_zero_ready",
        "parent_signed",
        "qreff_zero_accepted",
        "ready_for_runner",
        "gate_passed",
        "runner_ready",
        "score_allowed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in forbidden_true_fields and str(value).lower() == "true":
                    return False
    return True


def cited_paths_exist(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    path_keys = {"source_path", "source_table", "copy_path"}
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key not in path_keys:
                    continue
                if value in {"", None}:
                    continue
                text = str(value)
                if text.startswith("MISSING_"):
                    continue
                if not Path(text).exists():
                    return False
    return True


def template_missing_markers(rows: list[dict[str, Any]]) -> bool:
    if not rows:
        return False
    return all(any(str(value).startswith("MISSING_") for value in row.values()) for row in rows)


def generated_under_root() -> bool:
    paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    for path in paths:
        try:
            path.resolve().relative_to(ROOT.resolve())
        except ValueError:
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2872_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all registered source paths exist"),
        ("VAL2872_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all registered source anchors were found"),
        ("VAL2872_2_evidence_review_complete", len(rows_by_name["review"]) >= 8 and all(not row["accepted_source_row"] for row in rows_by_name["review"]), "q_R_eff evidence reviewed and none accepted"),
        ("VAL2872_3_source_contract_written", any(row["law_id"] == "LAW2872_1_compact_source_charge" and row["derived_status"] == "DERIVED_CONDITIONAL_SOURCE_CONTRACT" for row in rows_by_name["source_law"]), "conditional q_R_eff compact-source contract written"),
        ("VAL2872_4_source_law_not_accepted", all(not row["source_equation_parent_accepted"] for row in rows_by_name["source_law"]), "source law remains nonclaim until parent clauses close"),
        ("VAL2872_5_zero_not_proven", all(not row["qreff_zero_accepted"] for row in rows_by_name["zero_audit"]), "q_R_eff parent-zero theorem remains unproved"),
        ("VAL2872_6_template_nonclaim_missing_markers", template_missing_markers(rows_by_name["template"]) and all(not row["ready_for_runner"] for row in rows_by_name["template"]), "finite row template contains explicit MISSING markers and is not runner-ready"),
        ("VAL2872_7_gates_fail_closed", all(not row["gate_passed"] for row in rows_by_name["gates"]), "all q_R_eff acceptance gates fail closed"),
        ("VAL2872_8_request_open", rows_by_name["request"][0]["status"] == "OPEN_SOURCE_REQUEST", "narrow q_R_eff source request emitted"),
        ("VAL2872_9_runner_refused", all(row["status"] == "REFUSED" and not row["runner_ready"] for row in rows_by_name["runner"]), "runner remains refused"),
        ("VAL2872_10_next_target_2873", rows_by_name["next"][0]["next_id"] == "NEXT2872_0_2873", "first-triplet parent re-entry selected next"),
        ("VAL2872_11_outputs_exist", all(path.exists() for path in output_paths), "all generated CSV outputs exist before validation write"),
        ("VAL2872_12_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2872_13_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2872_14_cited_paths_exist", cited_paths_exist(rows_by_name), "all cited local paths exist, ignoring explicit MISSING placeholders"),
        ("VAL2872_15_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2872_16_generated_under_post_checkpoint", generated_under_root(), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2872_17_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2872_18_pycache_absent", pycache_absent(), "scripts __pycache__ absent during validation"),
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
            "validation_id": "VAL2872_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2872 wrote the exact conditional q_R_eff source-equation contract, rejected claim promotion, kept A_total locked, emitted the narrow q_R_eff source request, and selected first-triplet parent source-current re-entry for 2873.",
            "timestamp_utc": now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2872 - Y5 R2FR q_R_eff Parent Source Equation Or Finite Row Under AX1090",
        "",
        "Status: `Y5_R2FR_2872_qReff_conditional_source_contract_written_parent_row_not_accepted_parent_reentry_next`",
        "",
        "## Private Verdict",
        "",
        "2872 sharpened `q_R_eff` into the exact compact-source Green contract. In the normalized static branch:",
        "",
        "`(-Laplace+ell_R^-2) delta_R=-S_R/Z_R`, `delta_R=q_R_eff exp(-r/ell_R)/(4*pi*r)+H_R`, and `q_R_eff=-int_W S_R/Z_R d^3x` plus any parent-owned boundary term.",
        "",
        "This is good mathematics, but not yet a physics claim. The current corpus still lacks finite `q_R_eff`, finite `ell_R` or an accepted long-range hierarchy, sourced `S_R/Z_R`, `H_R` boundary/no-hair closure, measured-GM/readout convention, and the shared `Q_CAB`/`sigma_R_source_sign`/Green convention.",
        "",
        "`A_total` therefore remains locked. Since both `Q_CAB` and `q_R_eff` now have precise source contracts, the next move should not be another blind row hunt; it should be a parent re-entry attempt for the shared source-current identity that could own both charges together.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"]),
        "",
        "## q_R_eff Evidence Review",
        "",
        markdown_table(rows["review"], ["review_id", "quantity", "source_path", "source_anchor", "verdict", "accepted_source_row", "reason_not_accepted", "valid_for_claim"]),
        "",
        "## Source Equation Audit",
        "",
        markdown_table(rows["source_law"], ["law_id", "clause", "derived_status", "parent_status", "missing_for_claim", "source_equation_parent_accepted", "valid_for_claim"]),
        "",
        "## Parent Zero Audit",
        "",
        markdown_table(rows["zero_audit"], ["zero_id", "theorem_route", "current_status", "blocker", "parent_signed", "qreff_zero_accepted", "valid_for_claim"]),
        "",
        "## Finite Row Template",
        "",
        markdown_table(rows["template"], ["template_id", "quantity", "value", "units", "source_path", "equation_anchor", "ready_for_runner", "valid_for_claim"]),
        "",
        "## Acceptance Gates",
        "",
        markdown_table(rows["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"]),
        "",
        "## Narrow Source Request",
        "",
        markdown_table(rows["request"], ["request_id", "quantity", "needed_source", "narrow_request", "status", "ready_for_runner", "valid_for_claim"]),
        "",
        "## Runner Status",
        "",
        markdown_table(rows["runner"], ["runner_id", "status", "accepted_qreff_rows", "required_qreff_rows", "accepted_first_triplet_rows", "required_first_triplet_rows", "reason", "runner_ready", "score_allowed", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_register_rows()
    rows["review"] = evidence_review_rows()
    rows["source_law"] = source_law_rows()
    rows["zero_audit"] = zero_audit_rows()
    rows["template"] = template_rows()
    rows["gates"] = gate_rows()
    rows["request"] = request_rows()
    rows["runner"] = runner_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "review", "source_law", "zero_audit", "template", "gates", "request", "runner", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    remove_pycache()
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2872_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2872_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
