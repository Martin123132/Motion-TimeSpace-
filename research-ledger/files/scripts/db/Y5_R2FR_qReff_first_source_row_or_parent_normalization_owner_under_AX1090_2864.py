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

DOC = ROOT / "2864-Y5-R2FR-qReff-first-source-row-or-parent-normalization-owner-under-AX1090.md"

SRC_2863_DOC = ROOT / "2863-Y5-R2FR-QCAB-first-source-row-or-parent-zero-owner-under-AX1090.md"
SRC_2863_NEXT = RESIDUALS / "P8_Y5_R2FR_2863_NEXT_TARGET.csv"
SRC_2863_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2863_QCAB_BLOCKER_LEDGER.csv"
SRC_2863_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2863_VALIDATION.csv"
SRC_2862_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2862_FIRST_ROW_SOURCE_REQUEST_PACK.csv"
SRC_2862_SCHEMA = RESIDUALS / "P8_Y5_R2FR_2862_STRICT_RUNNER_SCHEMA_SPLIT.csv"
SRC_2861_SCAN = RESIDUALS / "P8_Y5_R2FR_2861_FIRST_ROW_SOURCE_SCAN.csv"
SRC_2839_DOC = ROOT / "2839-Y5-R2FR-finite-RAB-residual-green-kernel-normalization-or-first-source-backed-row-under-AX1090.md"
SRC_2839_KERNEL = RESIDUALS / "P8_Y5_R2FR_2839_GREEN_KERNEL_NORMALIZATION.csv"
SRC_2839_SELECTOR = RESIDUALS / "P8_Y5_R2FR_2839_FIRST_SOURCE_ROW_SELECTOR.csv"
SRC_2839_ZERO = RESIDUALS / "P8_Y5_R2FR_2839_THEOREM_ZERO_OR_SOURCE_ROW_ATTEMPT.csv"
SRC_2839_DIM = RESIDUALS / "P8_Y5_R2FR_2839_DIMENSIONAL_CONTRACT.csv"
SRC_2839_PROJ = RESIDUALS / "P8_Y5_R2FR_2839_ARENA_PROJECTION_CONTRACT.csv"
SRC_2840_DOC = ROOT / "2840-Y5-R2FR-first-finite-RAB-normalization-pack-or-parent-zero-certificate-under-AX1090.md"
SRC_2840_PACK = RESIDUALS / "P8_Y5_R2FR_2840_NORMALIZATION_PACK_CONTRACT.csv"
SRC_2840_FILL = RESIDUALS / "P8_Y5_R2FR_2840_FIRST_PACK_FILL_ATTEMPT_NONCLAIM.csv"
SRC_2840_ZERO = RESIDUALS / "P8_Y5_R2FR_2840_PARENT_ZERO_CERTIFICATE_AUDIT.csv"
SRC_2840_ACCEPT = RESIDUALS / "P8_Y5_R2FR_2840_PACK_ACCEPTANCE_VALIDATOR.csv"
SRC_2841_BRIDGE = RESIDUALS / "P8_Y5_R2FR_2841_QREFF_TO_QRHAT_CONDITIONAL_BRIDGE.csv"
SRC_2841_COND = RESIDUALS / "P8_Y5_R2FR_2841_PPN_BRIDGE_CONDITIONS.csv"
SRC_2842_DOC = ROOT / "2842-Y5-R2FR-PPN-bridge-condition-closure-or-finite-tauPPN-profile-under-AX1090.md"
SRC_2842_PROFILE = RESIDUALS / "P8_Y5_R2FR_2842_FINITE_TAUPPN_PROFILE.csv"
SRC_2842_REQ = RESIDUALS / "P8_Y5_R2FR_2842_PROFILE_SOURCE_REQUIREMENTS.csv"
SRC_2844_PACK = RESIDUALS / "P8_Y5_R2FR_2844_CAB_AMPLITUDE_SOURCE_PACK.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2849_SCAN = RESIDUALS / "P8_Y5_R2FR_2849_CORE_AMPLITUDE_SOURCE_SCAN.csv"
SRC_2850_HUNT = RESIDUALS / "P8_Y5_R2FR_2850_PARENT_EQUATION_HUNT_LEDGER.csv"
SRC_2850_MANUAL = RESIDUALS / "P8_Y5_R2FR_2850_MANUAL_SOURCE_LEDGER.csv"
SRC_2851_DOC = ROOT / "2851-Y5-R2FR-minimal-parent-amplitude-owner-ansatz-or-no-go-under-AX1090.md"
SRC_2852_FALLBACK = RESIDUALS / "P8_Y5_R2FR_2852_FINITE_AMPLITUDE_FALLBACK_CONTRACT.csv"
SRC_2854_SCAN = RESIDUALS / "P8_Y5_R2FR_2854_REAL_SOURCE_ACQUISITION_SCAN.csv"
SRC_2854_BLOCKER = RESIDUALS / "P8_Y5_R2FR_2854_BLOCKER_LEDGER.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2864_SOURCE_REGISTER.csv",
    "evidence": RESIDUALS / "P8_Y5_R2FR_2864_QREFF_SOURCE_EVIDENCE_SCAN.csv",
    "normalization": RESIDUALS / "P8_Y5_R2FR_2864_QREFF_PARENT_NORMALIZATION_AUDIT.csv",
    "acceptance": RESIDUALS / "P8_Y5_R2FR_2864_QREFF_ACCEPTANCE_GATE.csv",
    "template": RESIDUALS / "P8_Y5_R2FR_2864_QREFF_FIRST_ROW_TEMPLATE_NONCLAIM.csv",
    "blockers": RESIDUALS / "P8_Y5_R2FR_2864_QREFF_BLOCKER_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2864_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2864_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2864_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2864_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "evidence_copy": LOCAL_BOUNDS / "RAB_QREFF_SOURCE_EVIDENCE_SCAN_2864_NONCLAIM.csv",
    "blocker_copy": SOURCE_WEIGHT / "RAB_QREFF_BLOCKER_LEDGER_2864_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2864_sigma_source_sign_owner_NEXT.csv",
    "template_copy": BETA_DOCS / "RAB_QREFF_FIRST_ROW_TEMPLATE_2864_NONCLAIM.csv",
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
        ("SRC2864_0_2863_doc", SRC_2863_DOC, "NEXT2863_0_2864;VAL2863_OVERALL", "2863 handoff selects q_R_eff"),
        ("SRC2864_1_2863_next", SRC_2863_NEXT, "NEXT2863_0_2864", "selected 2864 next target"),
        ("SRC2864_2_2863_blockers", SRC_2863_BLOCKERS, "BLOCK2863_0_Q_CAB_PARENT_INPUT;BLOCK2863_6_HANDOFF", "Q_CAB blocker carried forward"),
        ("SRC2864_3_2863_validation", SRC_2863_VALIDATION, "VAL2863_OVERALL", "2863 validation"),
        ("SRC2864_4_2862_requests", SRC_2862_REQUESTS, "REQ2862_1_q_R_eff", "exact q_R_eff source request"),
        ("SRC2864_5_2862_schema", SRC_2862_SCHEMA, "SCHEMA2862_1_q_R_eff_value", "strict runner q_R_eff slot"),
        ("SRC2864_6_2861_scan", SRC_2861_SCAN, "SCAN2861_1_q_R_eff", "first-row q_R_eff source scan"),
        ("SRC2864_7_2839_doc", SRC_2839_DOC, "KER2839_4_compact_body;ZOS2839_4_first_source_row", "finite Green kernel checkpoint"),
        ("SRC2864_8_2839_kernel", SRC_2839_KERNEL, "KER2839_1_normalized_operator;KER2839_3_solution;KER2839_4_compact_body", "q_R_eff kernel grammar"),
        ("SRC2864_9_2839_selector", SRC_2839_SELECTOR, "SEL2839_0_minimal_pair;SEL2839_4_projection", "first source row selector"),
        ("SRC2864_10_2839_zero", SRC_2839_ZERO, "ZOS2839_2_try_JR_zero;ZOS2839_4_first_source_row", "zero/source-row attempt"),
        ("SRC2864_11_2839_dim", SRC_2839_DIM, "DIM2839_1_ell;DIM2839_3_point_charge", "dimension contract"),
        ("SRC2864_12_2839_proj", SRC_2839_PROJ, "PROJ2839_0_R10;PROJ2839_1_PPN;PROJ2839_4_WEP", "arena projection contract"),
        ("SRC2864_13_2840_doc", SRC_2840_DOC, "FILL2840_0_first_RAB_finite_pack;PACK2840_1_amplitude", "normalization pack doc"),
        ("SRC2864_14_2840_pack", SRC_2840_PACK, "PACK2840_0_range;PACK2840_1_amplitude;PACK2840_2_sign", "normalization pack contract"),
        ("SRC2864_15_2840_fill", SRC_2840_FILL, "FILL2840_0_first_RAB_finite_pack;MISSING_Q_R_EFF", "failed pack fill"),
        ("SRC2864_16_2840_zero", SRC_2840_ZERO, "PZ2840_2_source_zero;PZ2840_5_joint_certificate", "parent zero certificate audit"),
        ("SRC2864_17_2840_accept", SRC_2840_ACCEPT, "ACC2840_1_amplitude;ACC2840_OVERALL", "pack acceptance validator"),
        ("SRC2864_18_2841_bridge", SRC_2841_BRIDGE, "BRG2841_0_kernel_exterior;BRG2841_4_qRhat_map", "conditional PPN bridge"),
        ("SRC2864_19_2841_cond", SRC_2841_COND, "COND2841_2_long_range;COND2841_3_sign;COND2841_4_GM", "PPN bridge conditions"),
        ("SRC2864_20_2842_doc", SRC_2842_DOC, "TAUP2842_0_deltaR_profile;REQ2842_1_qeff", "finite tauPPN profile"),
        ("SRC2864_21_2842_profile", SRC_2842_PROFILE, "TAUP2842_0_deltaR_profile;TAUP2842_3_explicit_profile", "finite tauPPN profile rows"),
        ("SRC2864_22_2842_req", SRC_2842_REQ, "REQ2842_0_ell;REQ2842_1_qeff", "profile source requirements"),
        ("SRC2864_23_2844_pack", SRC_2844_PACK, "PACK2844_4_q_R_eff", "amplitude source pack"),
        ("SRC2864_24_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_0_operator;CONTRACT2844_4_range;CONTRACT2844_5_sign", "parent amplitude contract"),
        ("SRC2864_25_2849_scan", SRC_2849_SCAN, "SCAN2849_1_q_R_eff", "core amplitude source scan"),
        ("SRC2864_26_2850_hunt", SRC_2850_HUNT, "HUNT2850_1_q_R_eff", "parent equation hunt"),
        ("SRC2864_27_2850_manual", SRC_2850_MANUAL, "MAN2850_2_deltaR_equation;MAN2850_4_identity", "manual source ledger"),
        ("SRC2864_28_2851_doc", SRC_2851_DOC, "ANS2851_0_general_source_doublet;ALG2851_3_identity", "conditional common-current ansatz"),
        ("SRC2864_29_2852_fallback", SRC_2852_FALLBACK, "FB2852_1_q_R_eff", "finite amplitude fallback contract"),
        ("SRC2864_30_2854_scan", SRC_2854_SCAN, "SCAN2854_1_q_R_eff", "real source acquisition scan"),
        ("SRC2864_31_2854_blocker", SRC_2854_BLOCKER, "BLOCK2854_1_q_R_eff", "q_R_eff blocker"),
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


def evidence_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "evidence_id": "EVID2864_0_normalized_operator",
            "quantity": "q_R_eff",
            "candidate_type": "operator_normalization",
            "source_path": str(SRC_2839_KERNEL),
            "source_anchor": "KER2839_1_normalized_operator",
            "evidence": "(-Laplace+ell_R^-2) delta_R=-S_R/Z_R with ell_R^2=Z_R/M_R^2",
            "status": "SYMBOLIC_NORMALIZATION_ONLY",
            "missing_for_acceptance": "finite ell_R or Z_R/M_R^2; sourced S_R/Z_R; parent sign convention",
        },
        {
            "evidence_id": "EVID2864_1_compact_body_charge",
            "quantity": "q_R_eff",
            "candidate_type": "compact_body_green_charge",
            "source_path": str(SRC_2839_KERNEL),
            "source_anchor": "KER2839_4_compact_body",
            "evidence": "outside compact body delta_R=q_R_eff exp(-r/ell_R)/(4*pi*r)+boundary_homogeneous; q_R_eff=-int_body S_R/Z_R d^3x",
            "status": "SYMBOLIC_KERNEL_ONLY",
            "missing_for_acceptance": "finite integral value; source support; units; source path; boundary class",
        },
        {
            "evidence_id": "EVID2864_2_minimal_pair_selector",
            "quantity": "ell_R+q_R_eff",
            "candidate_type": "first_row_schema",
            "source_path": str(SRC_2839_SELECTOR),
            "source_anchor": "SEL2839_0_minimal_pair",
            "evidence": "first finite row must be ell_R plus q_R_eff or equivalent source amplitude",
            "status": "SELECTED_SCHEMA_NOT_FILLED",
            "missing_for_acceptance": "range and amplitude must be sourced together before scoring",
        },
        {
            "evidence_id": "EVID2864_3_pack_contract",
            "quantity": "q_R_eff",
            "candidate_type": "normalization_pack_slot",
            "source_path": str(SRC_2840_PACK),
            "source_anchor": "PACK2840_1_amplitude",
            "evidence": "q_R_eff=-integral_body S_R/Z_R d^3x, length units",
            "status": "MISSING_Q_R_EFF",
            "missing_for_acceptance": "numeric/source-normalized compact amplitude with source path and equation anchor",
        },
        {
            "evidence_id": "EVID2864_4_failed_pack_fill",
            "quantity": "q_R_eff",
            "candidate_type": "first_pack_fill",
            "source_path": str(SRC_2840_FILL),
            "source_anchor": "FILL2840_0_first_RAB_finite_pack",
            "evidence": "candidate profile keeps q_R_eff=MISSING_Q_R_EFF",
            "status": "FAILED_TO_FILL_FROM_CURRENT_CORPUS",
            "missing_for_acceptance": "ell_R, q_R_eff, source sign, boundary class, tau_arena and source provenance",
        },
        {
            "evidence_id": "EVID2864_5_parent_equation_hunt",
            "quantity": "q_R_eff",
            "candidate_type": "parent_equation_hunt",
            "source_path": str(SRC_2850_HUNT),
            "source_anchor": "HUNT2850_1_q_R_eff",
            "evidence": "symbol exists but parent delta_R source equation does not own it",
            "status": "FOUND_SYMBOL_ONLY_PARENT_EQUATION_MISSING",
            "missing_for_acceptance": "L_R delta_R=J_R, q_R_eff=int J_R in same charge convention as Q_CAB",
        },
        {
            "evidence_id": "EVID2864_6_real_acquisition_scan",
            "quantity": "q_R_eff",
            "candidate_type": "real_source_scan",
            "source_path": str(SRC_2854_SCAN),
            "source_anchor": "SCAN2854_1_q_R_eff",
            "evidence": "finite Green charge slot found",
            "status": "MISSING_SOURCE_NORMALIZATION",
            "missing_for_acceptance": "no finite numeric q_R_eff and no parent source normalization",
        },
        {
            "evidence_id": "EVID2864_7_conditional_ppn_bridge",
            "quantity": "q_R_eff_to_q_R_hat",
            "candidate_type": "conditional_observable_map",
            "source_path": str(SRC_2841_BRIDGE),
            "source_anchor": "BRG2841_4_qRhat_map",
            "evidence": "q_R_hat=-sigma_R*q_R_eff*c^2/(4*pi*G*M_source)",
            "status": "DERIVED_IF_MATCH_CONDITIONS_HOLD",
            "missing_for_acceptance": "source mass convention, q_R_eff value, sign, C_R=delta_R, boundary/range conditions",
        },
    ]
    for row in rows:
        row.update(
            {
                "accepted_source_row": False,
                "finite_numeric_value_present": False,
                "theorem_zero_owner_present": False,
            }
        )
    return [add_common(row) for row in rows]


def normalization_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "NORM2864_0_operator",
            "claim": "parent supplies normalized operator for delta_R",
            "required_clause": "Z_R, M_R^2 and sign give ell_R^2=Z_R/M_R^2 or direct sourced ell_R",
            "current_evidence": "KER2839_1 and PACK2840_0 define the relation",
            "status": "SYMBOLIC_ONLY",
            "blocker": "MISSING_ELL_R_OR_ZR_MR2_SOURCE",
        },
        {
            "audit_id": "NORM2864_1_source_integral",
            "claim": "parent supplies q_R_eff=-int S_R/Z_R d^3x",
            "required_clause": "S_R/Z_R is sourced over a compact body with units and support",
            "current_evidence": "KER2839_4 and PACK2840_1 define the target",
            "status": "VALUE_NOT_SOURCED",
            "blocker": "MISSING_Q_R_EFF_VALUE_AND_SOURCE_NORMALIZATION",
        },
        {
            "audit_id": "NORM2864_2_source_zero",
            "claim": "q_R_eff=0 from source silence",
            "required_clause": "J_R, Pi_R and readout source terms vanish or integrate to zero in the parent branch",
            "current_evidence": "ZOS2839_2 and PZ2840_2 say source zero is not signed",
            "status": "NOT_DERIVED",
            "blocker": "MISSING_JR_SOURCE_SILENCE_THEOREM",
        },
        {
            "audit_id": "NORM2864_3_boundary_homogeneous",
            "claim": "boundary_homogeneous is zero or separately bounded",
            "required_clause": "H_R/no-hair class, edge charge and boundary primitive are parent-owned",
            "current_evidence": "ZOS2839_3 and PACK2840_3 keep boundary class missing",
            "status": "NOT_DERIVED",
            "blocker": "MISSING_BOUNDARY_HOMOGENEOUS_CLASS",
        },
        {
            "audit_id": "NORM2864_4_arena_projection",
            "claim": "q_R_eff can be scored in R10/PPN/clock/orbital arenas",
            "required_clause": "tau_arena maps delta_R into observables with same source normalization",
            "current_evidence": "PROJ2839_0-4 mark every arena projection missing",
            "status": "NOT_SCORE_READY",
            "blocker": "MISSING_ARENA_PROJECTION",
        },
        {
            "audit_id": "NORM2864_5_common_convention",
            "claim": "q_R_eff shares convention with Q_CAB and sigma_R_source_sign",
            "required_clause": "same exterior Green kernel, 4*pi normalization, sign convention and measured-GM convention",
            "current_evidence": "2863 keeps Q_CAB blocked and 2862 keeps sigma_R_source_sign blocked",
            "status": "NOT_CLOSED",
            "blocker": "MISSING_COMMON_GREEN_SIGN_CONVENTION",
        },
        {
            "audit_id": "NORM2864_6_verdict",
            "claim": "q_R_eff finite row or parent normalization owner accepted",
            "required_clause": "all source, range, sign, boundary and projection clauses close",
            "current_evidence": "source scans show symbolic rows only",
            "status": "NOT_ACCEPTED",
            "blocker": "q_R_eff_REMAINS_MISSING_SOURCE_NORMALIZATION",
        },
    ]
    for row in rows:
        row.update(
            {
                "parent_signed": False,
                "normalization_owner_accepted": False,
                "accepted_source_row": False,
            }
        )
    return [add_common(row) for row in rows]


def acceptance_rows() -> list[dict[str, Any]]:
    specs = [
        ("ACC2864_0_value", "finite q_R_eff value or parent-signed theorem-zero", "FAIL", "no numeric q_R_eff and no parent-signed zero theorem"),
        ("ACC2864_1_range", "ell_R positive range or long-range hierarchy", "FAIL", "ell_R/Z_R/M_R^2 remain unsourced"),
        ("ACC2864_2_source_equation", "parent L_R delta_R=J_R source equation", "FAIL", "delta_R source equation not owned by parent action"),
        ("ACC2864_3_integral_units", "q_R_eff=-int S_R/Z_R d^3x with units and source support", "FAIL", "source density and compact-body normalization missing"),
        ("ACC2864_4_sign_boundary", "sigma_R_source_sign and H_R/boundary class fixed", "FAIL", "sign and boundary class remain open"),
        ("ACC2864_5_common_convention", "same convention as Q_CAB numerator leg", "FAIL", "Q_CAB remains blocked and common Green convention not sourced"),
        ("ACC2864_6_arena_projection", "R10/PPN/clock/orbital tau projection exists", "FAIL", "all arena projections missing"),
        ("ACC2864_7_runner_guard", "strict A_total runner can score", "FAIL", "Q_CAB, q_R_eff, sigma_R_source_sign, GM, tail and full vector remain missing"),
    ]
    return [
        add_common(
            {
                "acceptance_id": acceptance_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "accepted_ready": False,
                "gate_passed": False,
                "runner_ready": False,
            }
        )
        for acceptance_id, criterion, result, reason in specs
    ]


def template_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "template_id": "TEMPLATE2864_0_q_R_eff_first_row_nonclaim",
                "branch_id": "R2FR_local_PPN_constant_limit_after_Uamp_demotion",
                "quantity": "q_R_eff",
                "value": "MISSING_q_R_eff",
                "units": "m",
                "source_path": "",
                "equation_anchor": "MISSING_q_R_eff_EQUATION_ANCHOR",
                "source_equation": "MISSING_L_R_delta_R_EQUALS_J_R",
                "source_integral": "q_R_eff=-int_body S_R/Z_R d^3x",
                "ell_R_value": "MISSING_ELL_R",
                "green_convention": "MISSING_COMMON_GREEN_CONVENTION",
                "sigma_R_source_sign": "MISSING_sigma_R_source_sign",
                "boundary_class": "MISSING_H_R_BOUNDARY_CLASS",
                "arena_projection": "MISSING_TAU_ARENA",
                "qcab_status": "BLOCKED_Q_CAB_CARRIED_FROM_2863",
                "first_row_ready": False,
                "accepted_source_row": False,
            }
        )
    ]


def blocker_rows() -> list[dict[str, Any]]:
    specs = [
        ("BLOCK2864_0_q_R_eff_VALUE", "q_R_eff", "MISSING_SOURCE_NORMALIZATION", "derive/source finite compact-source Green charge", "blocks A_total numerator"),
        ("BLOCK2864_1_ELL_R", "ell_R", "MISSING_ELL_R", "source range or Z_R/M_R^2 with sign/units", "blocks finite profile and long-range limit"),
        ("BLOCK2864_2_SOURCE_EQUATION", "L_R delta_R=J_R", "MISSING_PARENT_SOURCE_EQUATION", "supply parent delta_R source equation before integral", "blocks source-backed q_R_eff"),
        ("BLOCK2864_3_SR_ZR", "S_R/Z_R", "MISSING_SOURCE_DENSITY_NORMALIZATION", "define compact-body source density over same worldtube", "blocks integral value"),
        ("BLOCK2864_4_SIGMA_SIGN", "sigma_R_source_sign", "MISSING_OPERATOR_GREEN_SIGN_OWNER", "derive parent operator/Green/source sign", "blocks sign-stable A_total"),
        ("BLOCK2864_5_BOUNDARY", "H_R", "MISSING_BOUNDARY_CLASS", "prove no-hair or bound homogeneous mode", "blocks exterior profile"),
        ("BLOCK2864_6_ARENA", "tau_arena", "MISSING_ARENA_PROJECTION", "derive R10/PPN/clock/orbital projection map", "blocks empirical scoring"),
        ("BLOCK2864_7_QCAB_CARRY", "Q_CAB", "MISSING_PARENT_INPUT", "carry 2863 Q_CAB blocker until source/zero owner exists", "blocks A_total scoring"),
        ("BLOCK2864_8_HANDOFF", "sigma_R_source_sign", "NEXT_CORE_ROW_AFTER_QREFF_BLOCKED", "attack source-sign/common Green convention next", "opens 2865 without claiming q_R_eff"),
    ]
    return [
        add_common(
            {
                "blocker_id": blocker_id,
                "quantity": quantity,
                "blocker_code": blocker_code,
                "required_resolution": required_resolution,
                "blocks": blocks,
                "accepted_source_row": False,
            }
        )
        for blocker_id, quantity, blocker_code, required_resolution, blocks in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2864_0_kernel", "Green-kernel q_R_eff grammar is usable.", "ACCEPTED_SYMBOLIC_NONCLAIM", "the normalized Yukawa solution and compact-source charge definition are mathematically clear"),
        ("DEC2864_1_no_first_row", "No q_R_eff first source row accepted.", "NO_ACCEPTED_SOURCE_ROW", "current corpus has symbolic definitions and failed fill rows, not finite source-backed values"),
        ("DEC2864_2_no_zero", "q_R_eff=0 is not parent-proved.", "SOURCE_ZERO_UNSIGNED", "J_R/source silence, boundary class, and readout silence remain unsigned"),
        ("DEC2864_3_runner", "Strict A_total runner remains blocked.", "LOCKED", "both numerator legs and sigma_R_source_sign are not sourced"),
        ("DEC2864_4_next", "Attack sigma_R_source_sign/common Green convention next.", "SELECTED_2865", "even sourced charges cannot combine until the parent operator sign and shared convention are fixed"),
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
                "next_id": "NEXT2864_0_2865",
                "status": "selected_primary",
                "target_doc": "2865-Y5-R2FR-sigmaR-source-sign-and-common-Green-convention-owner-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_sigmaR_source_sign_and_common_Green_convention_owner_under_AX1090_2865.py",
                "mission": "derive or source sigma_R_source_sign and the shared exterior Green convention tying Q_CAB and q_R_eff; reject sigma_R_profile import, keep Q_CAB/q_R_eff blockers active, and refuse A_total scoring until the sign owner is parent-signed",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("COPY2864_0_evidence", OUTPUTS["evidence"], BRANCH_OUTPUTS["evidence_copy"], "q_R_eff evidence scan nonclaim copy"),
        ("COPY2864_1_blockers", OUTPUTS["blockers"], BRANCH_OUTPUTS["blocker_copy"], "q_R_eff blocker ledger nonclaim copy"),
        ("COPY2864_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2865"),
        ("COPY2864_3_template", OUTPUTS["template"], BRANCH_OUTPUTS["template_copy"], "q_R_eff first-row template nonclaim copy"),
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
        "normalization_owner_accepted",
        "theorem_zero_owner_present",
        "finite_numeric_value_present",
        "first_row_ready",
        "accepted_ready",
        "gate_passed",
        "runner_ready",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in forbidden_true_fields and str(value).lower() == "true":
                    return False
    return True


def cited_paths_exist(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if not key.endswith("_path") and key not in {"source_table", "copy_path"}:
                    continue
                if value in {"", None}:
                    continue
                path_text = str(value)
                if path_text.startswith("scripts/") or path_text.startswith("scripts\\"):
                    continue
                if not Path(path_text).exists():
                    return False
    return True


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


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2864_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all registered source paths exist"),
        ("VAL2864_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all registered anchors were found"),
        ("VAL2864_2_evidence_scan_covers_qReff", len(rows_by_name["evidence"]) >= 8 and any(row["source_anchor"] == "KER2839_4_compact_body" for row in rows_by_name["evidence"]), "q_R_eff evidence scan covers kernel, pack, failed fill, hunt, scan, and bridge rows"),
        ("VAL2864_3_no_accepted_qReff_row", all(not row["accepted_source_row"] for row in rows_by_name["evidence"]), "no q_R_eff finite source row was accepted"),
        ("VAL2864_4_normalization_rejected", any(row["audit_id"] == "NORM2864_6_verdict" and row["status"] == "NOT_ACCEPTED" for row in rows_by_name["normalization"]), "q_R_eff parent normalization owner remains unsigned"),
        ("VAL2864_5_acceptance_gates_fail_closed", all(not row["gate_passed"] for row in rows_by_name["acceptance"]), "all q_R_eff acceptance gates fail closed"),
        ("VAL2864_6_template_blocked", rows_by_name["template"][0]["value"] == "MISSING_q_R_eff" and not rows_by_name["template"][0]["first_row_ready"], "q_R_eff template remains nonclaim"),
        ("VAL2864_7_QCAB_blocker_carried", any(row["blocker_id"] == "BLOCK2864_7_QCAB_CARRY" for row in rows_by_name["blockers"]), "Q_CAB blocker carried forward"),
        ("VAL2864_8_next_target_2865", rows_by_name["next"][0]["next_id"] == "NEXT2864_0_2865" and "sigma_R_source_sign" in rows_by_name["next"][0]["mission"], "sigma_R_source_sign/common Green target selected"),
        ("VAL2864_9_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2864_10_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2864_11_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2864_12_cited_paths_exist", cited_paths_exist(rows_by_name), "all cited local file/copy paths in generated rows exist"),
        ("VAL2864_13_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2864_14_generated_under_post_checkpoint", generated_under_root(), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2864_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2864_16_pycache_absent", pycache_absent(), "scripts __pycache__ absent during validation"),
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
            "validation_id": "VAL2864_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2864 keeps q_R_eff as a symbolic Green charge only, rejects parent-normalization promotion, carries Q_CAB as a blocker, and selects sigma_R_source_sign/common Green convention ownership for 2865.",
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
        "# 2864 - Y5 R2FR q_R_eff First Source Row Or Parent Normalization Owner Under AX1090",
        "",
        "Status: `Y5_R2FR_2864_qReff_symbolic_kernel_source_normalization_missing_sigma_next`",
        "",
        "## Private Verdict",
        "",
        "2864 tried to promote `q_R_eff` from symbolic Green charge to a real first source row.",
        "",
        "The usable kernel grammar is:",
        "",
        "```text",
        "(-Laplace + ell_R^-2) delta_R = -S_R/Z_R",
        "delta_R(r)=q_R_eff exp(-r/ell_R)/(4*pi*r)+H_R(r)",
        "q_R_eff := - integral_body S_R/Z_R d^3x",
        "```",
        "",
        "That is good mathematics, but not yet a sourced physics row. The current corpus does not provide finite `q_R_eff`, finite `ell_R`, parent `L_R delta_R=J_R`, source density normalization, boundary/no-hair class, arena projection, or the shared sign/Green convention.",
        "",
        "`q_R_eff=0` also does not follow: source silence, boundary silence, and readout silence remain unsigned. So the strict runner stays blocked, with `Q_CAB` carried forward from 2863.",
        "",
        "The next finite route is `sigma_R_source_sign` plus the common Green convention, because even real numerator charges cannot be combined safely until the parent fixes the sign and orientation.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"]),
        "",
        "## q_R_eff Source Evidence Scan",
        "",
        markdown_table(rows["evidence"], ["evidence_id", "candidate_type", "source_anchor", "status", "missing_for_acceptance", "accepted_source_row", "valid_for_claim"]),
        "",
        "## Parent Normalization Audit",
        "",
        markdown_table(rows["normalization"], ["audit_id", "claim", "status", "blocker", "parent_signed", "normalization_owner_accepted", "valid_for_claim"]),
        "",
        "## q_R_eff Acceptance Gate",
        "",
        markdown_table(rows["acceptance"], ["acceptance_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"]),
        "",
        "## First Row Template",
        "",
        markdown_table(rows["template"], ["template_id", "quantity", "value", "ell_R_value", "green_convention", "sigma_R_source_sign", "boundary_class", "arena_projection", "first_row_ready", "valid_for_claim"]),
        "",
        "## q_R_eff Blocker Ledger",
        "",
        markdown_table(rows["blockers"], ["blocker_id", "quantity", "blocker_code", "required_resolution", "blocks", "valid_for_claim"]),
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
    rows["evidence"] = evidence_rows()
    rows["normalization"] = normalization_rows()
    rows["acceptance"] = acceptance_rows()
    rows["template"] = template_rows()
    rows["blockers"] = blocker_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "evidence", "normalization", "acceptance", "template", "blockers", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2864_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2864_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
