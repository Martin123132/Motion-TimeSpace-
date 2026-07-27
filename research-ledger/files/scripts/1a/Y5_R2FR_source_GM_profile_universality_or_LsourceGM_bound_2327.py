from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_SOURCE_GM_PROFILE_UNIVERSALITY_OR_LSOURCEGM_BOUND_2327"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2327-Y5-R2FR-source-GM-profile-universality-or-LsourceGM-bound.md"

PATHS = {
    "2326_doc": ROOT / "2326-Y5-R2FR-epsilon-sigma-zero-certificate-or-first-protocol-leakage-row.md",
    "2326_validation": OUT / "P8_Y5_BRR545_2326_VALIDATION.csv",
    "2326_leakage": OUT / "P8_Y5_PARENT_QLOC_2326_FIRST_PROTOCOL_LEAKAGE_ROW.csv",
    "2326_inputs": OUT / "P8_Y5_PARENT_QLOC_2326_PROTOCOL_INPUT_REQUIREMENTS.csv",
    "1068_worldtube": OUT / "P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv",
    "1083_caveat": OUT / "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
    "1424_contract": OUT / "P8_Y5_R10_1424_SOURCE_VECTOR_CONTRACT.csv",
    "1425_zero": OUT / "P8_Y5_R10_1425_COMMON_MODE_WEP_ZERO_PROOF_ATTEMPT.csv",
    "1425_guard": OUT / "P8_Y5_R10_1425_MEASURED_G_COMMON_MODE_GUARD.csv",
    "1425_premise": OUT / "P8_Y5_R10_1425_COMMON_MODE_PREMISE_AUDIT.csv",
    "1456_worldtube": OUT / "P8_Y5_R10_1456_SOURCE_WORLDTUBE_PROJECTION_THEOREM_ATTEMPT.csv",
    "1817_transfer": OUT / "P8_Y5_PARENT_QLOC_1817_SOURCE_WORLDTUBE_TRANSFER_KERNEL_THEOREM.csv",
    "1900_point": OUT / "P8_Y5_PARENT_QLOC_1900_WEP_SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_ATTEMPT.csv",
    "1900_residual": OUT / "P8_Y5_PARENT_QLOC_1900_WEP_POINT_SOURCE_RESIDUAL_LEDGER_NONCLAIM.csv",
    "2124_protocol": OUT / "P8_Y5_PARENT_QLOC_2124_PROTOCOL_VARIABLE_NORMAL_FORM.csv",
    "2124_schema": OUT / "P8_Y5_PARENT_QLOC_2124_FIRST_BOUNDED_ROW_SCHEMA.csv",
    "2124_gm": OUT / "P8_Y5_PARENT_QLOC_2124_GM_GUARD_DESCENT_AUDIT.csv",
    "2125_common": OUT / "P8_Y5_PARENT_QLOC_2125_COMMON_MODE_DESCENT_AUDIT.csv",
    "2125_refusal": OUT / "P8_Y5_PARENT_QLOC_2125_GM_ABSORPTION_REFUSAL.csv",
    "2200_source": OUT / "P8_Y5_PARENT_QLOC_2200_PPN_VECTOR_SOURCE_ROW.csv",
}

SOURCES = [
    ("SRC2327_00_2326_doc", "2326_doc", PATHS["2326_doc"], ["NEXT2326_0", "source_GM"], "2326 handoff"),
    ("SRC2327_01_2326_validation", "2326_validation", PATHS["2326_validation"], ["VAL2326_OVERALL", "PASS"], "2326 validation"),
    ("SRC2327_02_2326_leakage", "2326_leakage", PATHS["2326_leakage"], ["PLR2326_0_source_GM", "L_source_GM * epsilon_sigma_source_GM"], "source_GM leakage contract"),
    ("SRC2327_03_2326_inputs", "2326_inputs", PATHS["2326_inputs"], ["PIR2326_0_profile", "PIR2326_1_GM_calibration"], "source/GM input requirements"),
    ("SRC2327_04_1068_worldtube", "1068_worldtube", PATHS["1068_worldtube"], ["SWT1068_0_source_stress_profile", "SOURCE_WORLDTUBE_NOT_ACQUIRED"], "source worldtube requirements"),
    ("SRC2327_05_1083_caveat", "1083_caveat", PATHS["1083_caveat"], ["SCG1083_0_profile_weighting", "NO_ABSORPTION_SHORTCUT_ALLOWED"], "source-vector caveat gate"),
    ("SRC2327_06_1424_contract", "1424_contract", PATHS["1424_contract"], ["SRCMAP1424_0_R_source", "MISSING_SOURCE_VECTOR"], "source vector contract"),
    ("SRC2327_07_1425_zero", "1425_zero", PATHS["1425_zero"], ["CMZ1425_0_target", "NOT_PROVED_DEMOTE_FINITE_WEP_TO_SOURCED_INPUT_ONLY"], "common-mode zero attempt"),
    ("SRC2327_08_1425_guard", "1425_guard", PATHS["1425_guard"], ["GCG1425_0_common_scale", "RELATIVE_BRANCH_RETAINED"], "measured-G guard"),
    ("SRC2327_09_1425_premise", "1425_premise", PATHS["1425_premise"], ["PREM1425_3_no_relative_source_prefactors", "EXACT_HIGH_PRESSURE_MISSING_CLAUSE"], "missing no-source-prefactor premise"),
    ("SRC2327_10_1456_worldtube", "1456_worldtube", PATHS["1456_worldtube"], ["SWP1456_1_linear_functional", "THEOREM_CONDITIONAL_NOT_PROMOTED"], "source-worldtube projection theorem"),
    ("SRC2327_11_1817_transfer", "1817_transfer", PATHS["1817_transfer"], ["KWT1817_0_target", "CONDITIONAL_THEOREM_NOT_CURRENT_PROOF"], "arena transfer theorem"),
    ("SRC2327_12_1900_point", "1900_point", PATHS["1900_point"], ["PSR1900_1_common_monopole_lemma", "PSR1900_6_verdict"], "point-source reduction attempt"),
    ("SRC2327_13_1900_residual", "1900_residual", PATHS["1900_residual"], ["PSE1900_1_relative_source_vector", "PSE1900_6_verdict"], "point-source residual ledger"),
    ("SRC2327_14_2124_protocol", "2124_protocol", PATHS["2124_protocol"], ["SIG2124_0_source_profile", "SIG2124_1_GM_calibration"], "protocol variable normal form"),
    ("SRC2327_15_2124_schema", "2124_schema", PATHS["2124_schema"], ["FK2124_0_source_GM", "epsilon_sigma_source_GM"], "LsourceGM schema"),
    ("SRC2327_16_2124_gm", "2124_gm", PATHS["2124_gm"], ["GM2124_0_common_mode_rule", "GM2124_3_verdict"], "GM guard descent audit"),
    ("SRC2327_17_2125_common", "2125_common", PATHS["2125_common"], ["CMD2125_1_minimal_missing_clause", "THEOREM_TARGET_SHARPENED_NOT_CLOSED"], "common-mode descent audit"),
    ("SRC2327_18_2125_refusal", "2125_refusal", PATHS["2125_refusal"], ["REF2125_1_measured_G_hiding", "REFUSED"], "GM absorption refusal"),
    ("SRC2327_19_2200_source", "2200_source", PATHS["2200_source"], ["PVS2200_2_vector_contract", "0.005788015401465051"], "PPN vector budget target"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2327_SOURCE_REGISTER.csv",
    "universality": OUT / "P8_Y5_PARENT_QLOC_2327_SOURCE_GM_UNIVERSALITY_ATTEMPT.csv",
    "bound": OUT / "P8_Y5_PARENT_QLOC_2327_LSOURCEGM_BOUND_ROW.csv",
    "inputs": OUT / "P8_Y5_PARENT_QLOC_2327_PROFILE_GM_INPUT_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2327_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2327_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2327_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2327_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2327_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2327_0_universality", OUTPUTS["universality"], BETA_DOCS / "SOURCE_GM_UNIVERSALITY_ATTEMPT_2327_NONCLAIM.csv"),
    ("COPY2327_1_bound", OUTPUTS["bound"], MICRO_RESIDUALS / "LsourceGM_bound_row_nonclaim_2327.csv"),
    ("COPY2327_2_inputs", OUTPUTS["inputs"], RAB_QUEUE / "JR2327_PROFILE_GM_INPUT_LEDGER_NONCLAIM.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "missing_needles=" + ";".join(missing)
    return True, "all_needles_found"


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, key, path, needles, role in SOURCES:
        found, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needles": ";".join(needles),
                "needles_found": bool_text(found),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def build_universality_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "UGM2327_0_target",
            "claim_piece": "source_GM profile universality",
            "formal_statement": "D_v(sigma_source_profile, sigma_GM_common_mode)=0, hence epsilon_sigma_source_GM=0, if the source profile/support and GM calibration descend through the same observed quotient data.",
            "status": "TARGET_SHARPENED",
            "proof_or_obstruction": "this is the exact zero route for the first source_GM leakage channel selected in 2326",
            "source_anchor": "PLR2326_0_source_GM;PIR2326_0_profile;PIR2326_1_GM_calibration",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "UGM2327_1_common_monopole",
            "claim_piece": "universal exterior common-mode monopole",
            "formal_statement": "If J_H is conserved, source support is fixed, one G_ref/source measure is used, and all source response is common-mode, the leading exterior source leg is calibrated GM/r^2 plus bounded multipoles.",
            "status": "EXACT_CONDITIONAL_LEMMA",
            "proof_or_obstruction": "ordinary Gauss/Newton exterior-source reasoning works only for the universal source factor, not for relative profile/composition residuals",
            "source_anchor": "PSR1900_1_common_monopole_lemma;KWT1817_2_worldtube_support",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "UGM2327_2_no_source_only_species_slot",
            "claim_piece": "NoSourceOnlySpeciesSlot",
            "formal_statement": "The parent object language must not admit species/material source weights w_A that multiply active gravitational source strength independently of non-gravitational normalization.",
            "status": "SHARPEST_MISSING_PREMISE",
            "proof_or_obstruction": "without this clause, S_m=sum_A(1+epsilon_A)S_A remains a covariant countermodel with relative source weights",
            "source_anchor": "CMD2125_1_minimal_missing_clause;PREM1425_3_no_relative_source_prefactors",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "UGM2327_3_GM_calibration",
            "claim_piece": "measured GM common-mode guard",
            "formal_statement": "Fitted GM may absorb one universal source normalization, but it cannot absorb relative source/profile/composition residuals.",
            "status": "GUARD_ACTIVE_NOT_NUMERIC",
            "proof_or_obstruction": "the algebraic guard exists, but the same-branch calibration equation and relative source basis are not source-filled",
            "source_anchor": "GM2124_0_common_mode_rule;GCG1425_0_common_scale;GCG1425_1_relative_residual",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "UGM2327_4_profile_weighting",
            "claim_piece": "orbit/worldtube-weighted source profile",
            "formal_statement": "sigma_source_profile must be either quotient-owned/fixed-protocol data or a source-backed orbit/profile/worldtube vector in the same basis as the response projection.",
            "status": "SOURCE_PROFILE_AND_COMPOSITION_OBSTRUCTION_ACTIVE",
            "proof_or_obstruction": "bulk Earth composition is not enough; the branch needs profile/support weighting or a theorem proving it cancels",
            "source_anchor": "SCG1083_0_profile_weighting;SRCMAP1424_0_R_source;PSE1900_1_relative_source_vector",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "UGM2327_5_same_frame_pullback",
            "claim_piece": "same-frame source pullback",
            "formal_statement": "force law, source variation, clocks, orbit, and eta/PPN readout must use the same observed coframe/time generator or retain a frame-source residual.",
            "status": "SAME_FRAME_SOURCE_PULLBACK_NOT_DERIVED",
            "proof_or_obstruction": "a profile theorem cannot close local GR if the source leg and readout leg live in different effective frames",
            "source_anchor": "PSR1900_5_same_frame_obstruction;SWP1456_6_verdict",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "UGM2327_6_verdict",
            "claim_piece": "promote epsilon_sigma_source_GM=0",
            "formal_statement": "Current MTS parent primitives prove source_GM profile/GM universality strongly enough to set epsilon_sigma_source_GM=0.",
            "status": "NOT_PROVED_USE_BOUND_ROUTE",
            "proof_or_obstruction": "NoSourceOnlySpeciesSlot, profile/source vector, GM calibration equation, finite-source/multipole handling, and same-frame pullback are still open",
            "source_anchor": "UGM2327_2_no_source_only_species_slot through UGM2327_5_same_frame_pullback",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "LSGM2327_0_bound_contract",
            "quantity": "C_source_GM",
            "formula_or_bound": "|Pi_gamma C_source_GM| <= |Pi_gamma| * L_source_GM * epsilon_sigma_source_GM",
            "lipschitz_factor": "L_source_GM = ||D_sigma Pi_source||||J_source|| + ||Pi_source||||D_sigma J_source||",
            "epsilon_symbol": "epsilon_sigma_source_GM = ||D_v(sigma_source_profile, sigma_GM_common_mode)||",
            "target_value": "0.005788015401465051",
            "target_units": "dimensionless alpha_PPN_total_abs_vector budget",
            "source_basis": "FK2124_0_source_GM;PVS2200_2_vector_contract",
            "current_status": "CONTRACT_READY_VALUES_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "LSGM2327_1_LsourceGM_input",
            "quantity": "L_source_GM",
            "formula_or_bound": "operator/source-current Lipschitz norm in the same units as Pi_gamma projection",
            "lipschitz_factor": "requires norm convention, J_source norm, D_sigma Pi_source, D_sigma J_source, and arena projection",
            "epsilon_symbol": "not applicable",
            "target_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "target_units": "dimensionless_per_protocol_norm after PPN normalization",
            "source_basis": "PIR2326_2_L_source_GM;FK2124_0_source_GM",
            "current_status": "MISSING_OPERATOR_NORM_AND_SOURCE_CURRENT_NORM",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "LSGM2327_2_epsilon_input",
            "quantity": "epsilon_sigma_source_GM",
            "formula_or_bound": "zero if profile/GM universality is parent-signed; otherwise source-backed protocol-leakage norm",
            "lipschitz_factor": "multiplies L_source_GM only after common units are declared",
            "epsilon_symbol": "||D_v(sigma_source_profile, sigma_GM_common_mode)||",
            "target_value": "MISSING_ZERO_CERTIFICATE_OR_NUMERIC_BOUND",
            "target_units": "declared_protocol_norm",
            "source_basis": "PIR2326_0_profile;PIR2326_1_GM_calibration",
            "current_status": "MISSING_PROFILE_GM_ZERO_OR_BOUND",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "LSGM2327_3_no_cancellation_policy",
            "quantity": "alpha_readout/source_GM contribution",
            "formula_or_bound": "source_GM must fit by absolute budget, not cancellation against other PPN/local tails",
            "lipschitz_factor": "absolute-vector policy inherited from PVS2200_2",
            "epsilon_symbol": "epsilon_sigma_source_GM",
            "target_value": "0.005788015401465051 ceiling before other tails",
            "target_units": "dimensionless",
            "source_basis": "PLR2326_1_target_budget;PVS2200_2_vector_contract",
            "current_status": "NONCLAIM_TARGET_ONLY",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PGI2327_0_no_source_only_species_slot",
            "needed_input": "NoSourceOnlySpeciesSlot theorem",
            "why_needed": "kills covariant relative source-weight countermodel w_A",
            "current_status": "EXACT_HIGH_PRESSURE_MISSING_CLAUSE",
            "accepted_resolution": "parent-signed object-language theorem or explicit retained source-weight vector",
            "source_anchor": "CMD2125_1_minimal_missing_clause;PREM1425_3_no_relative_source_prefactors",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PGI2327_1_source_profile_vector",
            "needed_input": "orbit/worldtube-weighted source profile/composition vector",
            "why_needed": "bulk Earth composition does not define the source vector seen by local/WEP/PPN projections",
            "current_status": "MISSING_SOURCE_VECTOR_OR_PROFILE_WEIGHTING",
            "accepted_resolution": "theorem proving profile is universal/common-mode or sourced profile/support vector with units",
            "source_anchor": "SCG1083_0_profile_weighting;SRCMAP1424_0_R_source",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PGI2327_2_GM_calibration_equation",
            "needed_input": "same-branch measured GM calibration equation",
            "why_needed": "separates absorbable common mode from forbidden relative-source hiding",
            "current_status": "GUARD_WRITTEN_NOT_NUMERIC",
            "accepted_resolution": "equation showing only one universal source factor enters fitted GM/G",
            "source_anchor": "GM2124_0_common_mode_rule;GCG1425_0_common_scale",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PGI2327_3_same_frame_source_pullback",
            "needed_input": "same observed frame for source and readout",
            "why_needed": "prevents a source-profile theorem from living in a different frame than PPN/WEP readout",
            "current_status": "SAME_FRAME_SOURCE_PULLBACK_NOT_DERIVED",
            "accepted_resolution": "parent coframe/time-generator certificate or explicit frame residual bound",
            "source_anchor": "PSR1900_5_same_frame_obstruction;SWP1456_6_verdict",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PGI2327_4_finite_source_multipole",
            "needed_input": "finite-source/multipole/profile error",
            "why_needed": "point-source common-mode lemma does not bound retained relative profile tails at orbit/readout level",
            "current_status": "FINITE_SOURCE_ERROR_BOUND_MISSING",
            "accepted_resolution": "profile theorem, conservative envelope, or official model import with units",
            "source_anchor": "SWT1068_3_finite_source_correction;PSE1900_3_multipole_error",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PGI2327_5_LsourceGM_norm",
            "needed_input": "L_source_GM operator norm and Pi_gamma projection",
            "why_needed": "turns the leakage contract into an actual bounded alpha_PPN contribution",
            "current_status": "MISSING_OPERATOR_NORM_AND_SOURCE_CURRENT_NORM",
            "accepted_resolution": "norm convention, source current norm, derivative norms, and target projection in declared units",
            "source_anchor": "FK2124_0_source_GM;LSGM2327_0_bound_contract",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2327_0_sources", "gate": "source paths and needles valid", "passed": "true", "claim_effect": "audit reproducible", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2327_1_conditional_common_monopole", "gate": "common-mode source monopole theorem exact conditionally", "passed": "true", "claim_effect": "useful theorem skeleton only", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2327_2_active_profile_GM_zero", "gate": "epsilon_sigma_source_GM=0 in active parent branch", "passed": "false", "claim_effect": "NoSourceOnlySpeciesSlot/profile/GM/same-frame gates still open", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2327_3_LsourceGM_score", "gate": "source_GM leakage numerically bounded", "passed": "false", "claim_effect": "L_source_GM and epsilon_sigma_source_GM values missing", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2327_4_local_GR_Newton", "gate": "local GR/Newton recovery derived", "passed": "false", "claim_effect": "still private theorem-building work, not a claim", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2327_5_github_public_update", "gate": "safe to push as public evidence", "passed": "false", "claim_effect": "do not publish this as a pass; checkpoint can be private only", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2327_0_measured_G_hiding", "claim": "absorb relative source/profile residual into measured GM", "allowed": "false", "reason": "only one universal common-mode source factor may be calibrated away", "blocking_rows": "UGM2327_3_GM_calibration;PGI2327_2_GM_calibration_equation", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2327_1_point_source_shortcut", "claim": "use exterior point source to remove all source_GM tails", "allowed": "false", "reason": "point-source reduction is conditional and does not kill relative profile/composition residuals", "blocking_rows": "UGM2327_4_profile_weighting;PGI2327_4_finite_source_multipole", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2327_2_bulk_as_profile", "claim": "use bulk Earth composition as the profile/worldtube source vector", "allowed": "false", "reason": "bulk composition is context, not orbit/support/projection-weighted source data", "blocking_rows": "PGI2327_1_source_profile_vector", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2327_3_zero_promotion", "claim": "set epsilon_sigma_source_GM=0 now", "allowed": "false", "reason": "NoSourceOnlySpeciesSlot, source profile, GM calibration, and same-frame pullback remain unsigned", "blocking_rows": "UGM2327_6_verdict", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2327_4_public_claim", "claim": "publish 2327 as local-GR/R10/PPN pass", "allowed": "false", "reason": "2327 is a derivation gate and acquisition ledger, not an empirical or local-GR pass", "blocking_rows": "CG2327_4_local_GR_Newton;CG2327_5_github_public_update", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2327_0",
            "next_target": "2328-Y5-R2FR-NoSourceOnlySpeciesSlot-or-source-profile-vector-first-row.md",
            "why": "2327 shows the cleanest zero proof now bottlenecks on no source-only species slots; if that fails, source/profile vector acquisition is the honest finite route.",
            "claim_status": "private_nonclaim_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2327_1",
            "next_target": "2328b-Y5-R2FR-same-frame-source-pullback-certificate.md",
            "why": "same-frame source pullback is the parallel route that prevents frame/source leakage across WEP, PPN, clocks, and orbit tests.",
            "claim_status": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2327_2",
            "next_target": "private-summary-before-any-GitHub-update",
            "why": "the current branch is useful but not public-claim safe; summarize publish readiness only after the next source-slot gate.",
            "claim_status": "no_github_yet",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dest in BRANCH_COPY_SPECS:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": relative_path(src),
                "branch_copy_path": str(dest),
                "copy_exists": bool_text(dest.exists()),
                "row_count": str(len(read_csv_rows(dest))),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation_rows(source_rows: list[dict[str, Any]], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths += [Path(row["branch_copy_path"]) for row in branch_copy_rows]
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": "false",
            }
        )

    add("VAL2327_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists")
    add("VAL2327_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found")
    universality_rows = read_csv_rows(OUTPUTS["universality"])
    add("VAL2327_02_common_monopole_conditional", any(row.get("row_id") == "UGM2327_1_common_monopole" and row.get("status") == "EXACT_CONDITIONAL_LEMMA" for row in universality_rows), "common-mode monopole lemma retained as conditional")
    add("VAL2327_03_active_zero_blocked", any(row.get("row_id") == "UGM2327_6_verdict" and row.get("status") == "NOT_PROVED_USE_BOUND_ROUTE" for row in universality_rows), "active source_GM zero not promoted")
    bound_rows = read_csv_rows(OUTPUTS["bound"])
    add("VAL2327_04_bound_row_exists", any(row.get("row_id") == "LSGM2327_0_bound_contract" and "L_source_GM" in row.get("formula_or_bound", "") for row in bound_rows), "L_source_GM bound row exists")
    add("VAL2327_05_bound_nonready", all(row.get("score_ready") == "false" for row in bound_rows), "bound rows remain non-score-ready")
    input_rows = read_csv_rows(OUTPUTS["inputs"])
    add("VAL2327_06_inputs_listed", len(input_rows) >= 6, "source_GM profile/GM input ledger populated")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2327_07_claim_gates_block", any(row.get("row_id") == "CG2327_4_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim remains blocked")
    add("VAL2327_08_github_blocked", any(row.get("row_id") == "CG2327_5_github_public_update" and row.get("passed") == "false" for row in claim_rows), "public GitHub update not recommended as evidence")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2327_09_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks shortcut claims")
    add("VAL2327_10_next_target", len(read_csv_rows(OUTPUTS["next"])) >= 2, "next targets selected")
    add("VAL2327_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")
    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2327_12_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        checkpoint_patterns = ("*P8_Y5*2327*.csv", "*2327-Y5*.md", "*SOURCE_GM*2327*", "*LSOURCEGM*2327*")
        for pattern in checkpoint_patterns:
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2327_13_formalization_untouched_by_2327", not formalization_hits, "no 2327 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2327_OVERALL", all(row["status"] == "PASS" for row in rows), "2327 keeps source_GM zero conditional, refuses measured-G/point-source shortcuts, stages the L_source_GM bound route, and recommends no GitHub evidence update yet.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    universality_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2327 - source_GM Profile Universality Or LsourceGM Bound

## Summary

2327 tries the clean route first: prove that the source profile and measured-GM convention are universal enough that
`epsilon_sigma_source_GM=0`.

Result: the proof is exact only as a conditional common-mode theorem. The universal exterior monopole survives as a
useful lemma, but the active MTS branch cannot yet set the source_GM leakage to zero. The sharp missing clause is still
`NoSourceOnlySpeciesSlot`, backed by source profile/vector, GM calibration, finite-source, and same-frame pullback gates.

So this checkpoint keeps the honest route open:
`|Pi_gamma C_source_GM| <= |Pi_gamma| * L_source_GM * epsilon_sigma_source_GM`.

This is private theorem-building, not a GitHub/public evidence update.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Universality Attempt

{markdown_table(universality_rows, ["row_id", "claim_piece", "formal_statement", "status", "proof_or_obstruction", "source_anchor", "valid_for_claim"])}

## LsourceGM Bound Row

{markdown_table(bound_rows, ["row_id", "quantity", "formula_or_bound", "epsilon_symbol", "target_value", "current_status", "score_ready", "valid_for_claim"])}

## Profile/GM Input Ledger

{markdown_table(input_rows, ["row_id", "needed_input", "why_needed", "current_status", "accepted_resolution", "source_anchor", "valid_for_claim"])}

## Claim Gates

{markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"])}

## Branch Copies

{markdown_table(branch_copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_output = {
        "sources": build_sources(),
        "universality": build_universality_rows(),
        "bound": build_bound_rows(),
        "inputs": build_input_rows(),
        "claims": build_claim_rows(),
        "refusal": build_refusal_rows(),
        "next": build_next_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(OUTPUTS[key], rows)
    branch_copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], branch_copy_rows)
    validation_rows = build_validation_rows(rows_by_output["sources"], branch_copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_doc(
        rows_by_output["sources"],
        rows_by_output["universality"],
        rows_by_output["bound"],
        rows_by_output["inputs"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2327 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
