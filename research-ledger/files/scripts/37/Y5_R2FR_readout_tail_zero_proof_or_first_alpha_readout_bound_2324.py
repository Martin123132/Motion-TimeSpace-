from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_READOUT_TAIL_ZERO_OR_BOUND_2324"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2324-Y5-R2FR-readout-tail-zero-proof-or-first-alpha-readout-bound.md"

PATHS = {
    "2323_doc": ROOT / "2323-Y5-R2FR-common-matter-frame-action-signature-or-readout-tail-row.md",
    "2323_validation": OUT / "P8_Y5_BRR545_2323_VALIDATION.csv",
    "2323_tail": OUT / "P8_Y5_PARENT_QLOC_2323_ALPHA_READOUT_TAIL_ROW.csv",
    "2323_comm": OUT / "P8_Y5_PARENT_QLOC_2323_SOURCE_FEEDBACK_COMMUTATOR_BRIDGE.csv",
    "2323_theorem": OUT / "P8_Y5_PARENT_QLOC_2323_COMMON_FRAME_THEOREM_ATTEMPT.csv",
    "2200_source": OUT / "P8_Y5_PARENT_QLOC_2200_PPN_VECTOR_SOURCE_ROW.csv",
    "2200_contract": OUT / "P8_Y5_PARENT_QLOC_2200_PPN_COMPONENT_CONTRACT.csv",
    "2203_readout": OUT / "P8_Y5_PARENT_QLOC_2203_ALPHA_READOUT_ROW.csv",
    "2203_fixed": OUT / "P8_Y5_PARENT_QLOC_2203_FIXED_BEFORE_READOUT_MAP_ATTEMPT.csv",
    "2203_gm": OUT / "P8_Y5_PARENT_QLOC_2203_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
    "2208_blockers": OUT / "P8_Y5_PARENT_QLOC_2208_PPN_BLOCKER_LEDGER.csv",
    "2122_owner": OUT / "P8_Y5_PARENT_QLOC_2122_SOURCE_READOUT_OWNER_LEMMA.csv",
    "2122_comm": OUT / "P8_Y5_PARENT_QLOC_2122_COMMUTATOR_OBSTRUCTION_LEDGER.csv",
    "2123_pi": OUT / "P8_Y5_PARENT_QLOC_2123_PI_SPLIT_THEOREM.csv",
    "2123_zero": OUT / "P8_Y5_PARENT_QLOC_2123_COMMUTATOR_ZERO_CONDITIONS.csv",
    "2124_chain": OUT / "P8_Y5_PARENT_QLOC_2124_SOURCE_FEEDBACK_CHAIN_RULE.csv",
    "2124_gm": OUT / "P8_Y5_PARENT_QLOC_2124_GM_GUARD_DESCENT_AUDIT.csv",
    "2125_common": OUT / "P8_Y5_PARENT_QLOC_2125_COMMON_MODE_DESCENT_AUDIT.csv",
    "2125_refusal": OUT / "P8_Y5_PARENT_QLOC_2125_GM_ABSORPTION_REFUSAL.csv",
}

SOURCES = [
    ("SRC2324_00_2323_doc", "2323_doc", PATHS["2323_doc"], ["NEXT2323_0", "readout-tail-zero-proof"], "2323 handoff"),
    ("SRC2324_01_2323_validation", "2323_validation", PATHS["2323_validation"], ["VAL2323_OVERALL", "PASS"], "2323 validation"),
    ("SRC2324_02_2323_tail", "2323_tail", PATHS["2323_tail"], ["ART2323_0_alpha_readout", "RETAINED_NONCLAIM_COMPONENT"], "current alpha_readout row"),
    ("SRC2324_03_2323_comm", "2323_comm", PATHS["2323_comm"], ["SFC2323_1_bound_route", "FINITE_BOUND_NORMAL_FORM_DERIVED"], "source feedback bridge"),
    ("SRC2324_04_2323_theorem", "2323_theorem", PATHS["2323_theorem"], ["CFT2323_0_candidate_theorem", "EXACT_CONDITIONAL_THEOREM"], "common-frame theorem"),
    ("SRC2324_05_2200_source", "2200_source", PATHS["2200_source"], ["PVS2200_2_vector_contract", "0.005788015401465051"], "PPN vector source ceiling"),
    ("SRC2324_06_2200_contract", "2200_contract", PATHS["2200_contract"], ["PCC2200_5_readout", "tau_readout*C_readout"], "PPN component contract"),
    ("SRC2324_07_2203_readout", "2203_readout", PATHS["2203_readout"], ["ARW2203_0_alpha_readout", "MISSING_FIXED_READOUT_FUNCTOR"], "readout row"),
    ("SRC2324_08_2203_fixed", "2203_fixed", PATHS["2203_fixed"], ["FBR2203_7_verdict", "source identity exists only as residual/obstruction vector"], "fixed-before-readout map"),
    ("SRC2324_09_2203_gm", "2203_gm", PATHS["2203_gm"], ["MGV2203_7_calibration_PPN_tail", "MISSING_GAUSS_ORBITAL_PPN_RESIDUAL"], "measured-GM obstruction"),
    ("SRC2324_10_2208_blockers", "2208_blockers", PATHS["2208_blockers"], ["PPNB2208_3_PPN_gauge", "MISSING_PPN_GAUGE_TRANSFORM"], "PPN blockers"),
    ("SRC2324_11_2122_owner", "2122_owner", PATHS["2122_owner"], ["SRO2122_0_exact_conditional", "CONDITIONAL_PROOF_VALID"], "source/readout owner lemma"),
    ("SRC2324_12_2122_comm", "2122_comm", PATHS["2122_comm"], ["COM2122_1_when_zero", "CONDITIONAL_ZERO_ROUTE"], "commutator zero route"),
    ("SRC2324_13_2123_pi", "2123_pi", PATHS["2123_pi"], ["PIS2123_2_q_descended_projector", "CONDITIONAL_ZERO_VALID"], "Pi split theorem"),
    ("SRC2324_14_2123_zero", "2123_zero", PATHS["2123_zero"], ["ZC2123_5_no_cancellation", "RETAINED"], "zero conditions"),
    ("SRC2324_15_2124_chain", "2124_chain", PATHS["2124_chain"], ["CR2124_3_bound_case", "FINITE_BOUND_NORMAL_FORM_DERIVED"], "source feedback chain rule"),
    ("SRC2324_16_2124_gm", "2124_gm", PATHS["2124_gm"], ["GM2124_3_verdict", "GUARD_NORMAL_FORM_CLOSED_DATA_OPEN"], "GM guard"),
    ("SRC2324_17_2125_common", "2125_common", PATHS["2125_common"], ["CMD2125_4_verdict", "THEOREM_TARGET_SHARPENED_NOT_CLOSED"], "common-mode descent"),
    ("SRC2324_18_2125_refusal", "2125_refusal", PATHS["2125_refusal"], ["REF2125_1_measured_G_hiding", "REFUSED"], "GM absorption refusal"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2324_SOURCE_REGISTER.csv",
    "zero": OUT / "P8_Y5_PARENT_QLOC_2324_ALPHA_READOUT_ZERO_PROOF_ATTEMPT.csv",
    "bound": OUT / "P8_Y5_PARENT_QLOC_2324_FIRST_ALPHA_READOUT_BOUND_ROW.csv",
    "acquisition": OUT / "P8_Y5_PARENT_QLOC_2324_READOUT_INPUT_ACQUISITION_LEDGER.csv",
    "vector": OUT / "P8_Y5_PARENT_QLOC_2324_PPN_VECTOR_UPDATE.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2324_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2324_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2324_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2324_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2324_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2324_0_zero", OUTPUTS["zero"], BETA_DOCS / "ALPHA_READOUT_ZERO_PROOF_ATTEMPT_2324_NONCLAIM.csv"),
    ("COPY2324_1_bound", OUTPUTS["bound"], MICRO_RESIDUALS / "first_alpha_readout_bound_row_nonclaim_2324.csv"),
    ("COPY2324_2_acquisition", OUTPUTS["acquisition"], RAB_QUEUE / "JR2324_READOUT_INPUT_ACQUISITION_LEDGER_NONCLAIM.csv"),
    ("COPY2324_3_vector", OUTPUTS["vector"], RAB_QUEUE / "JR2324_PPN_VECTOR_UPDATE_NONCLAIM.csv"),
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


def build_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARZ2324_0_exact_zero_theorem",
            "proof_piece": "readout-tail zero theorem",
            "formal_statement": "If Pi_gamma, source support sigma_A, GM calibration, and PPN gauge/readout maps descend through fixed (q,e_obs,theta) or are fixed external protocol after variation, then D_v readout=0 and alpha_readout=0.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "active_branch_gap": "descent certificates for support/projector/GM/gauge/readout are not parent-signed",
            "claim_effect": "zero not promoted",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARZ2324_1_projector_support",
            "proof_piece": "projector/support descent",
            "formal_statement": "Pi_A=Pi_bar_A(q,e_obs,theta) and sigma_A=sigma_bar_A(q,e_obs,theta) imply D_v(Pi_A J_A)=0 for v in ker(Dq).",
            "proof_status": "CONDITIONAL_ZERO_VALID",
            "active_branch_gap": "source worldtube, support mask, boundary transport, and material/source weights remain unsigned",
            "claim_effect": "source-feedback tail retained",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARZ2324_2_fixed_readout",
            "proof_piece": "fixed-before-readout map",
            "formal_statement": "PPN gamma/Shapiro readout is a post-solution reporting map with no arrow into S_parent, coefficient extraction, source normalization, or calibration.",
            "proof_status": "ZERO_BY_TYPE_FOR_POSTPROCESSING_ONLY",
            "active_branch_gap": "physically relevant GM/source/gauge feedback maps are not pure postprocessing",
            "claim_effect": "postprocessing report part closed; source-feedback part retained",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARZ2324_3_GM_guard",
            "proof_piece": "measured-GM guard",
            "formal_statement": "Only universal common-mode source calibration can be absorbed into measured G/GM; relative or protocol-dependent readout tails cannot.",
            "proof_status": "GUARD_DERIVED_NOT_ZERO",
            "active_branch_gap": "relative source vector and calibration equation are missing",
            "claim_effect": "prevents hiding alpha_readout by fitted GM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARZ2324_4_verdict",
            "proof_piece": "alpha_readout zero in active branch",
            "formal_statement": "ARZ2324_0 through ARZ2324_3 all pass with parent-signed descent certificates",
            "proof_status": "NOT_DERIVED_RETAIN_BOUND_ROW",
            "active_branch_gap": "exact theorem available, premises unsigned",
            "claim_effect": "first alpha_readout bound row required",
            "valid_for_claim": "false",
        },
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARB2324_0_source_ceiling",
            "quantity": "alpha_readout_abs_target",
            "formula_or_bound": "abs(alpha_readout) <= 0.005788015401465051 as a single-component target inside the PPN absolute-vector budget",
            "numeric_value": "0.005788015401465051",
            "units": "dimensionless",
            "source_path": str(PATHS["2200_source"]),
            "source_row_id": "PVS2200_2_vector_contract",
            "status": "SOURCE_BACKED_TARGET_NOT_MTS_PREDICTION",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARB2324_1_readout_normal_form",
            "quantity": "alpha_readout",
            "formula_or_bound": "alpha_readout = Pi_gamma[Delta_cal + Delta_PPN + C_feedback + C_protocol]",
            "numeric_value": "MISSING_COMPONENT_VALUES",
            "units": "dimensionless",
            "source_path": str(PATHS["2323_tail"]),
            "source_row_id": "ART2323_0_alpha_readout",
            "status": "NORMAL_FORM_DERIVED_VALUES_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARB2324_2_triangle_bound",
            "quantity": "alpha_readout_abs_envelope",
            "formula_or_bound": "abs(alpha_readout) <= abs(Pi_gamma Delta_cal)+abs(Pi_gamma Delta_PPN)+abs(Pi_gamma C_feedback)+abs(Pi_gamma C_protocol)",
            "numeric_value": "MISSING_TERM_BOUNDS",
            "units": "dimensionless",
            "source_path": str(PATHS["2124_chain"]),
            "source_row_id": "CR2124_3_bound_case",
            "status": "BOUND_FORM_DERIVED_VALUES_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARB2324_3_score_gate",
            "quantity": "alpha_readout_pass_condition",
            "formula_or_bound": "alpha_readout_abs_envelope <= alpha_readout_abs_target and all other PPN vector components are theorem-zero or independently bounded",
            "numeric_value": "MISSING_VECTOR_COMPONENTS",
            "units": "dimensionless",
            "source_path": str(PATHS["2200_contract"]),
            "source_row_id": "PCC2200_6_total",
            "status": "CLAIM_BLOCKED_UNTIL_VECTOR_COMPLETE",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_acquisition_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "RIA2324_0_Delta_cal",
            "needed_input": "Delta_cal",
            "meaning": "calibration mismatch between closed parent source charge and observed GM/PPN mass",
            "current_status": "MISSING_GAUSS_ORBITAL_PPN_RESIDUAL",
            "source_basis": "MGV2203_7_calibration_PPN_tail",
            "next_evidence": "Gauss/orbital calibration theorem or numeric residual bound",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RIA2324_1_Delta_PPN",
            "needed_input": "Delta_PPN",
            "meaning": "second-order PPN readout/source-normalization tail after measured-GM normalization",
            "current_status": "MISSING_PPN_GAUGE_AND_SOURCE_NORMALIZATION",
            "source_basis": "PPNB2208_2_source_normalization;PPNB2208_3_PPN_gauge",
            "next_evidence": "observed PPN gauge transform and source-normalization row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RIA2324_2_C_feedback",
            "needed_input": "C_feedback",
            "meaning": "source-feedback commutator kernel from D_v(Pi_A J_A)",
            "current_status": "NORMAL_FORM_DERIVED_VALUES_MISSING",
            "source_basis": "CR2124_3_bound_case;SFC2323_1_bound_route",
            "next_evidence": "operator norm and epsilon_sigma_A for source/readout protocol",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RIA2324_3_C_protocol",
            "needed_input": "C_protocol",
            "meaning": "support/mask/orbit-window/boundary transport protocol tail",
            "current_status": "CLOSURE_OR_SOURCE_REQUIRED",
            "source_basis": "PIS2123_3_external_protocol;ZC2123_2_fixed_protocol",
            "next_evidence": "parent protocol declaration, q/e_obs descent proof, or finite source-backed bound",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RIA2324_4_vector_completion",
            "needed_input": "all sibling PPN components",
            "meaning": "alpha_readout cannot pass by cancellation against alpha_cg/disformal/nonH/support/boundary",
            "current_status": "ABSOLUTE_VECTOR_COMPONENTS_MISSING",
            "source_basis": "PCC2200_6_total;ART2323_3_no_cancellation",
            "next_evidence": "component-wise zero theorems or source-backed bounds",
            "valid_for_claim": "false",
        },
    ]


def build_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PVU2324_0_alpha_readout_live",
            "component": "alpha_readout",
            "status": "LIVE_NONCLAIM_COMPONENT_WITH_SOURCE_TARGET",
            "current_best_object": "abs(alpha_readout) target <= 0.005788015401465051; prediction missing",
            "effect_on_local_GR": "local GR remains blocked unless zero theorem or bound gate closes",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PVU2324_1_no_tau_activation",
            "component": "tau_PPN=1 activation",
            "status": "BLOCKED_BY_READOUT_DESCENT",
            "current_best_object": "2322 conditional tau remains inactive until alpha_readout/readout descent closes",
            "effect_on_local_GR": "cannot score alpha_cg as strict scalar-tensor branch yet",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PVU2324_2_absolute_vector",
            "component": "alpha_PPN_total_abs",
            "status": "VECTOR_SCHEMA_READY_VALUES_MISSING",
            "current_best_object": "sum_abs(alpha_cg,alpha_dis,alpha_nonH,alpha_support,alpha_boundary,alpha_readout)",
            "effect_on_local_GR": "no single-component local-GR pass allowed",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2324_0_sources",
            "gate": "source paths and needles valid",
            "passed": "true",
            "claim_effect": "audit reproducible",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2324_1_conditional_zero",
            "gate": "alpha_readout zero theorem exact conditionally",
            "passed": "true",
            "claim_effect": "proof shape valid if descent premises are signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2324_2_active_zero",
            "gate": "alpha_readout=0 in active branch",
            "passed": "false",
            "claim_effect": "descent certificates missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2324_3_bound_score",
            "gate": "alpha_readout bound row score-ready",
            "passed": "false",
            "claim_effect": "source target exists, prediction/bound components missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2324_4_local_GR_Newton",
            "gate": "local GR/Newton recovery derived",
            "passed": "false",
            "claim_effect": "still a target, not a result",
            "valid_for_claim": "false",
        },
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2324_0_zero_promotion",
            "claim": "alpha_readout=0 now",
            "allowed": "false",
            "reason": "zero theorem premises are exact but not parent-signed in the active branch",
            "blocking_rows": "ARZ2324_1_projector_support;ARZ2324_4_verdict",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2324_1_bound_claim",
            "claim": "alpha_readout passes the PPN bound",
            "allowed": "false",
            "reason": "2324 has a source-backed target but no MTS prediction or term-by-term envelope values",
            "blocking_rows": "ARB2324_1_readout_normal_form;ARB2324_2_triangle_bound;ARB2324_3_score_gate",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2324_2_measured_G_absorption",
            "claim": "measured GM absorbs alpha_readout",
            "allowed": "false",
            "reason": "common-mode calibration guard is active; relative/protocol tails cannot be hidden by fitted GM",
            "blocking_rows": "ARZ2324_3_GM_guard;RIA2324_0_Delta_cal",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2324_3_local_GR",
            "claim": "2324 derives local GR/Newton",
            "allowed": "false",
            "reason": "readout tail is now theorem-or-bound shaped, but the full PPN residual vector is not complete",
            "blocking_rows": "PVU2324_2_absolute_vector;CG2324_4_local_GR_Newton",
            "valid_for_claim": "false",
        },
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2324_0",
            "next_target": "2325-Y5-R2FR-source-feedback-epsilon-sigma-or-PPN-gauge-bound-row.md",
            "why": "2324 reduces alpha_readout to a concrete envelope; the next useful input is either epsilon_sigma/operator norm for C_feedback or a source-backed PPN gauge/calibration residual bound.",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2324_1",
            "next_target": "2325b-Y5-R2FR-NoSourceOnlySpeciesSlot-parent-syntax-proof.md",
            "why": "parallel derivation route: eliminate the relative source-weight countermodel before it feeds C_feedback and Delta_cal.",
            "claim_status": "parallel_nonclaim",
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

    add("VAL2324_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists")
    add("VAL2324_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found")
    zero_rows = read_csv_rows(OUTPUTS["zero"])
    add("VAL2324_02_conditional_zero", any(row.get("row_id") == "ARZ2324_0_exact_zero_theorem" and row.get("proof_status") == "EXACT_CONDITIONAL_THEOREM" for row in zero_rows), "conditional alpha_readout zero theorem row exists")
    add("VAL2324_03_active_zero_blocked", any(row.get("row_id") == "ARZ2324_4_verdict" and row.get("proof_status") == "NOT_DERIVED_RETAIN_BOUND_ROW" for row in zero_rows), "active zero not promoted")
    bound_rows = read_csv_rows(OUTPUTS["bound"])
    add("VAL2324_04_source_target", any(row.get("row_id") == "ARB2324_0_source_ceiling" and row.get("numeric_value") == "0.005788015401465051" for row in bound_rows), "source-backed alpha_readout target exists")
    add("VAL2324_05_bound_not_score_ready", all(row.get("score_ready") == "false" for row in bound_rows), "bound rows remain non-score-ready")
    acquisition_rows = read_csv_rows(OUTPUTS["acquisition"])
    add("VAL2324_06_acquisition_inputs", len(acquisition_rows) >= 4, "readout acquisition inputs listed")
    vector_rows = read_csv_rows(OUTPUTS["vector"])
    add("VAL2324_07_vector_blocks_score", all(row.get("score_ready") == "false" for row in vector_rows), "PPN vector rows remain non-score-ready")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2324_08_claim_gates_block", any(row.get("row_id") == "CG2324_4_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim remains blocked")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2324_09_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks premature readout/local-GR claims")
    add("VAL2324_10_next_target", len(read_csv_rows(OUTPUTS["next"])) >= 1, "next target selected")
    add("VAL2324_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")
    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2324_12_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        checkpoint_patterns = ("*P8_Y5*2324*.csv", "*2324-Y5*.md", "*ALPHA_READOUT*2324*", "*MTS_R2FR_READOUT_TAIL_ZERO_OR_BOUND_2324*")
        for pattern in checkpoint_patterns:
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2324_13_formalization_untouched_by_2324", not formalization_hits, "no 2324 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2324_OVERALL", all(row["status"] == "PASS" for row in rows), "2324 proves alpha_readout=0 only conditionally, creates the first source-backed alpha_readout target row, leaves component values missing, and blocks local-GR/Newton claims.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    acquisition_rows: list[dict[str, Any]],
    vector_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2324 - Readout Tail Zero Proof Or First alpha_readout Bound

## Summary

2324 gets the readout tail into a proper theorem-or-bound form. The zero proof is exact conditionally:
if the PPN readout, measured-GM calibration, source support, and projectors descend through the same fixed
`(q,e_obs,theta)` data, then the vertical readout variation vanishes and `alpha_readout=0`.

The active branch still cannot claim that zero. The descent certificates are not parent-signed, and the physically
relevant source-feedback/calibration maps are not just harmless postprocessing. So 2324 keeps `alpha_readout` live and
adds the first source-backed target row: `abs(alpha_readout) <= 0.005788015401465051` as a nonclaim component target
inside the PPN absolute-vector budget.

No local-GR win is claimed. The good news is that the ghost has a shape now: `Delta_cal`, `Delta_PPN`, `C_feedback`,
and `C_protocol` are the four named inputs we either have to prove zero or bound.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## alpha_readout Zero Proof Attempt

{markdown_table(zero_rows, ["row_id", "proof_piece", "formal_statement", "proof_status", "active_branch_gap", "claim_effect", "valid_for_claim"])}

## First alpha_readout Bound Row

{markdown_table(bound_rows, ["row_id", "quantity", "formula_or_bound", "numeric_value", "units", "status", "score_ready", "valid_for_claim"])}

## Readout Input Acquisition Ledger

{markdown_table(acquisition_rows, ["row_id", "needed_input", "meaning", "current_status", "source_basis", "next_evidence", "valid_for_claim"])}

## PPN Vector Update

{markdown_table(vector_rows, ["row_id", "component", "status", "current_best_object", "effect_on_local_GR", "score_ready", "valid_for_claim"])}

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
        "zero": build_zero_rows(),
        "bound": build_bound_rows(),
        "acquisition": build_acquisition_rows(),
        "vector": build_vector_rows(),
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
        rows_by_output["zero"],
        rows_by_output["bound"],
        rows_by_output["acquisition"],
        rows_by_output["vector"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2324 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
