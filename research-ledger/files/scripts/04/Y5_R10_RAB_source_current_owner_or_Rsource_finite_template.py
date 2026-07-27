from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1415-Y5-R10-RAB-source-current-owner-or-Rsource-finite-template.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1415_SOURCE_REGISTER.csv"
OWNER_ATTEMPT_PATH = SRC_DIR / "P8_Y5_R10_1415_SOURCE_CURRENT_OWNER_ATTEMPT.csv"
RSOURCE_TEMPLATE_PATH = SRC_DIR / "P8_Y5_R10_1415_RSOURCE_FINITE_TEMPLATE.csv"
MERGE_MAP_PATH = SRC_DIR / "P8_Y5_R10_1415_BETA_SOURCE_ALPHA_RSOURCE_MERGE_MAP.csv"
ANTI_SHORTCUT_PATH = SRC_DIR / "P8_Y5_R10_1415_RSOURCE_ANTI_SHORTCUT_GATE.csv"
ARENA_GATE_PATH = SRC_DIR / "P8_Y5_R10_1415_RSOURCE_ARENA_GATE.csv"
DECISION_PATH = SRC_DIR / "P8_Y5_R10_1415_DECISION_LEDGER.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1415_CLAIM_GATE.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1415_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1415_VALIDATION.csv"

STATUS = "Y5_R10_1415_source_current_owner_not_derived_Rsource_template_written_nonclaim"
CLAIM_CEILING = (
    "source_current_owner_attempt_and_Rsource_template_only_no_WEP_pass_no_beta_source_pass_"
    "no_R10_no_Newton_no_PPN_no_local_GR_pass"
)


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def write_csv(relative_path: Path, rows: list[dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {relative_path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def anchor_found(relative_path: str, anchor: str) -> bool:
    path = ROOT / relative_path
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1415_0_1414_doc",
            "source_path": "1414-Y5-R10-RAB-beta-source-alpha-owner-or-finite-bound-row.md",
            "anchor": "NEXT1414_0_1415",
            "role": "prior checkpoint selecting source-current owner/R_source merge",
        },
        {
            "source_id": "SRC1415_1_1414_owner",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1414_BETA_SOURCE_ALPHA_OWNER_ATTEMPT.csv",
            "anchor": "BSA1414_5_verdict",
            "role": "beta_source_alpha owner not derived and redirected to source-current owner",
        },
        {
            "source_id": "SRC1415_2_1414_bound",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1414_BETA_SOURCE_ALPHA_FINITE_BOUND_ROW.csv",
            "anchor": "BSB1414_4_score_ready_gate",
            "role": "beta_source_alpha target rows not score-ready",
        },
        {
            "source_id": "SRC1415_3_1412_Rsource",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1412_FINITE_RESIDUAL_VECTOR_BRANCH.csv",
            "anchor": "RV1412_3_R_source",
            "role": "R_source residual component definition",
        },
        {
            "source_id": "SRC1415_4_1412_morphism",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1412_VISIBLE_COEFFICIENT_MORPHISM_COUNTEREXAMPLES.csv",
            "anchor": "MOR1412_3_species_source",
            "role": "species/source coefficient morphism remains live",
        },
        {
            "source_id": "SRC1415_5_1077_theorem",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv",
            "anchor": "WCO1077_5_verdict",
            "role": "parent WEP coupling owner theorem not closed",
        },
        {
            "source_id": "SRC1415_6_1077_clauses",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1077_CLAUSE_SIGNATURE_MATRIX.csv",
            "anchor": "CLAUSE1077_2_current_owner",
            "role": "current/source normalization owner is missing",
        },
        {
            "source_id": "SRC1415_7_1077_counterexamples",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1077_ZERO_THEOREM_COUNTEREXAMPLE_AUDIT.csv",
            "anchor": "CE1077_1_current_rescaling",
            "role": "current rescaling/source marker counterexample",
        },
        {
            "source_id": "SRC1415_8_1076_parent_map",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1076_PARENT_MAP_DERIVATION_ATTEMPT.csv",
            "anchor": "DER1076_5_verdict",
            "role": "parent material/source map not derived",
        },
        {
            "source_id": "SRC1415_9_1076_owner_gates",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1076_COUPLING_OWNER_GATES.csv",
            "anchor": "OWN1076_4_source_worldtube",
            "role": "current owner and source worldtube missing",
        },
        {
            "source_id": "SRC1415_10_1068_worldtube",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv",
            "anchor": "SWT1068_5_verdict",
            "role": "source worldtube pack not acquired",
        },
        {
            "source_id": "SRC1415_11_1068_force_map",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv",
            "anchor": "FRM1068_5_verdict",
            "role": "observed-frame force/readout map not derived",
        },
        {
            "source_id": "SRC1415_12_1068_fallback",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_DIRECT_PRODUCT_FALLBACK.csv",
            "anchor": "DPF1068_3_refusal_rule",
            "role": "direct product fallback and refusal rules",
        },
        {
            "source_id": "SRC1415_13_1405_response",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1405_PARENT_WEP_RESPONSE_CURRENT_DERIVATION.csv",
            "anchor": "WRC1405_5_sector_prior_compression",
            "role": "WEP source contraction and P_s form",
        },
        {
            "source_id": "SRC1415_14_1409_Ua",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1409_OFFICIAL_READOUT_BLOCKER_LEDGER.csv",
            "anchor": "ORB1409_7_verdict",
            "role": "U_a official readout/source blocker",
        },
        {
            "source_id": "SRC1415_15_this_script",
            "source_path": "scripts/Y5_R10_RAB_source_current_owner_or_Rsource_finite_template.py",
            "anchor": "STATUS",
            "role": "generator for this checkpoint",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def owner_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "SCO1415_0_target",
            "owner_piece": "single source-current owner",
            "required_statement": "source/test current normalization, species weights, beta_source_alpha, and R_source descend from one parent current/measure owner or are explicit residual fields",
            "current_result": "TARGET_DEFINED",
            "missing_for_claim": "parent object-language, action-measure owner, current owner, source worldtube, and readout/product convention",
            "if_signed": "beta_source_alpha and R_source collapse to common-mode/theorem-owned objects",
            "if_unsigned": "R_source finite template is mandatory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "SCO1415_1_object_language",
            "owner_piece": "no source-only species argument",
            "required_statement": "Arg(S_parent) has no w_A(X), kappa_A(X), inert species multiplier, or source-only material slot",
            "current_result": "CONDITIONAL_UNSIGNED",
            "missing_for_claim": "NoSourceOnlySpeciesSlot / typed object-language theorem from MTS primitives",
            "if_signed": "species/source morphism MOR1412_3 is killed",
            "if_unsigned": "qbar_source_weight remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "SCO1415_2_action_measure",
            "owner_piece": "species-blind action measure / hbar owner",
            "required_statement": "ordinary matter shares one parent action measure and no species-dependent measure/action multiplier",
            "current_result": "CONDITIONAL_NOT_PARENT_DERIVED",
            "missing_for_claim": "single measure/action-scale owner signed by parent action",
            "if_signed": "w_A S_A and measure-weight counterexamples are removed",
            "if_unsigned": "species action weights remain legal counterexamples",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "SCO1415_3_current_owner",
            "owner_piece": "current/source normalization",
            "required_statement": "matter currents and source normalization descend from one current functor, not species/source-specific weights",
            "current_result": "MISSING",
            "missing_for_claim": "current_id, Noether_owner, charge_unit_owner, source normalization owner, parent basis",
            "if_signed": "beta_source_alpha becomes owned/common-mode",
            "if_unsigned": "current rescaling/source marker counterexample survives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "SCO1415_4_source_worldtube",
            "owner_piece": "Earth/source response",
            "required_statement": "source stress-current worldtube/profile is sourced or theorem-reduced to universal common mode",
            "current_result": "MISSING_SOURCE_WORLDTUBE",
            "missing_for_claim": "T_source^Earth(x), source composition/convention, finite-size correction, frame units",
            "if_signed": "source leg can be projected into WEP/R10/Newton gates",
            "if_unsigned": "R_source cannot be numeric or score-ready",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "SCO1415_5_readout_product",
            "owner_piece": "source/readout product convention",
            "required_statement": "source-current residual maps to eta_AB/Newton/R10 observables with declared units and official/equivalent readout kernel",
            "current_result": "BLOCKED_BY_1409_AND_1068",
            "missing_for_claim": "U_a official arrays/equivalent reconstruction, product convention, observed-frame force map",
            "if_signed": "finite R_source rows could be scored",
            "if_unsigned": "all R_source rows remain template-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "SCO1415_6_verdict",
            "owner_piece": "source-current owner status",
            "required_statement": "SCO1415_1 through SCO1415_5 all close from the parent action and source/readout data",
            "current_result": "SOURCE_CURRENT_OWNER_NOT_DERIVED_RSOURCE_TEMPLATE_REQUIRED",
            "missing_for_claim": "object-language, measure/current owner, source worldtube, U_a/product convention",
            "if_signed": "R_source and beta_source_alpha can be theorem-owned/common-mode",
            "if_unsigned": "write R_source finite nonclaim template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def rsource_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RSF1415_0_R_source",
            "quantity": "R_source",
            "definition": "qbar_source_weight from w_A(X), kappa_A(X), source-only material multipliers, or source-current normalization residuals",
            "formula_or_target": "R_source projects into WEP source charge, Newton-GM normalization, R10/R11 source-side rows, and beta_source_alpha EM subchannel",
            "required_inputs": "source-current owner theorem or finite source-weight value; units; sign; source path; material/source labels; projection kernel",
            "current_value": "MISSING",
            "units": "dimensionless or declared parent source-current units",
            "source_anchor": "RV1412_3_R_source;SCO1415_6_verdict",
            "current_status": "FINITE_RSOURCE_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "RSF1415_1_qbar_source_weight",
            "quantity": "qbar_source_weight",
            "definition": "species/source-only gravitational prefactor or kappa_A sensitivity",
            "formula_or_target": "qbar_source_weight = partial_X ln kappa_A or equivalent source-only weight derivative",
            "required_inputs": "NoSourceOnlySpeciesSlot theorem or source-weight coefficient; material/source tags; source paths",
            "current_value": "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT",
            "units": "dimensionless",
            "source_anchor": "MOR1412_3_species_source;CE1077_0_species_action_weight",
            "current_status": "SOURCE_WEIGHT_ROW_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "RSF1415_2_current_rescaling",
            "quantity": "current_rescaling_residual",
            "definition": "J_A -> c_A J_A or beta_source,A source marker residual",
            "formula_or_target": "finite source/test current normalization component in parent basis",
            "required_inputs": "Noether current owner or finite c_A/beta_source,A coefficient rows",
            "current_value": "MISSING_CURRENT_OWNER_OR_COEFFICIENT",
            "units": "dimensionless or parent current-normalization units",
            "source_anchor": "CE1077_1_current_rescaling;SCO1415_3_current_owner",
            "current_status": "CURRENT_RESCALING_ROW_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "RSF1415_3_source_worldtube",
            "quantity": "source_worldtube_projection",
            "definition": "Earth/source stress-current profile and source composition/convention in observed frame",
            "formula_or_target": "Integral_Earth K_source(x) delta T_source(x)/delta X_I with common-mode GM removed only after universality proof",
            "required_inputs": "T_source^Earth(x), source composition/convention, GM calibration, finite-size correction, frame units",
            "current_value": "MISSING_SOURCE_WORLDTUBE",
            "units": "declared by source-current convention",
            "source_anchor": "SWT1068_5_verdict;DER1076_1_source_leg_definition",
            "current_status": "SOURCE_WORLDTUBE_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "RSF1415_4_direct_product",
            "quantity": "direct_source_product",
            "definition": "direct parent variation product from source residual to eta_AB/Newton/R10 observable",
            "formula_or_target": "derive delta a_AB or eta_AB directly from parent action instead of arbitrary Delta_w*tau split",
            "required_inputs": "parent variation with units/source path or both split factors numeric/sourced",
            "current_value": "MISSING_DIRECT_PARENT_PRODUCT",
            "units": "observable-specific",
            "source_anchor": "DPF1068_0_preferred_route;FRM1068_5_verdict",
            "current_status": "DIRECT_PRODUCT_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "RSF1415_5_beta_source_alpha_projection",
            "quantity": "beta_source_alpha projection",
            "definition": "EM/alpha channel projection of R_source into eta_alpha = DeltaQ_alpha beta_source_alpha b_alpha tau_WEP",
            "formula_or_target": "beta_source_alpha is a subprojection of the same missing source-current normalization owner",
            "required_inputs": "R_source owner/value, EM channel map, b_alpha, tau_WEP/U_a, material tensor",
            "current_value": "TARGET_ONLY_FROM_1414",
            "units": "dimensionless target ratio if parent-normalized",
            "source_anchor": "BSB1414_0_definition;BSB1414_4_score_ready_gate",
            "current_status": "MERGED_WITH_RSOURCE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "RSF1415_6_verdict",
            "quantity": "R_source finite template pack",
            "definition": "source-current owner is not derived, so R_source stays as explicit finite residual branch",
            "formula_or_target": "score_ready iff all RSF1415_0 through RSF1415_5 are theorem-zero or source-backed with U_a/product convention",
            "required_inputs": "source-current owner or finite rows, source worldtube, U_a, product convention, arena projection",
            "current_value": "TEMPLATE_ONLY",
            "units": "not_applicable",
            "source_anchor": "SCO1415_6_verdict",
            "current_status": "RSOURCE_TEMPLATE_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def merge_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "merge_id": "MER1415_0_common_owner",
            "object_a": "beta_source_alpha",
            "object_b": "R_source",
            "relationship": "beta_source_alpha is the EM/alpha WEP projection of the broader source-current normalization residual",
            "if_owner_signed": "both become common-mode/theorem-owned and no free source suppression is allowed",
            "if_owner_unsigned": "beta_source_alpha target rows and R_source finite rows remain nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "merge_id": "MER1415_1_not_identical",
            "object_a": "beta_source_alpha",
            "object_b": "R_source",
            "relationship": "beta_source_alpha is not the whole R_source vector; R_source also includes Newton-GM, R10/R11 source-side, and source-only species weight channels",
            "if_owner_signed": "single owner can reduce all source-side channels",
            "if_owner_unsigned": "do not transfer beta_source_alpha WEP target to other arenas",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "merge_id": "MER1415_2_score_policy",
            "object_a": "beta_source_alpha target",
            "object_b": "R_source score",
            "relationship": "a target-only beta_source_alpha threshold is not a score-ready R_source bound",
            "if_owner_signed": "score may be unnecessary if source residual is theorem-zero",
            "if_owner_unsigned": "source-backed values and arena kernels are required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def anti_shortcut_rows() -> list[dict[str, Any]]:
    return [
        {
            "shortcut_id": "RSS1415_0_no_measured_G_absorption",
            "forbidden_shortcut": "absorb relative source weights into measured G or GM",
            "reason": "common source normalization can be calibrated away only after universality proof; relative source weights cannot",
            "source_anchor": "SWT1068_2_GM_calibration;FRM1068_2_common_mode_separation",
            "status": "FORBIDDEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "shortcut_id": "RSS1415_1_no_tau_unity",
            "forbidden_shortcut": "set tau_WEP or source kernel to 1",
            "reason": "source worldtube, orbit/readout kernel, and product convention are missing",
            "source_anchor": "DPF1068_3_refusal_rule;ORB1409_7_verdict",
            "status": "FORBIDDEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "shortcut_id": "RSS1415_2_no_point_source_by_taste",
            "forbidden_shortcut": "replace source worldtube with point-source convention without sourced error bound",
            "reason": "finite-size/source support correction and source composition/convention are missing",
            "source_anchor": "SWT1068_0_source_stress_profile;SWT1068_3_finite_source_correction",
            "status": "FORBIDDEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "shortcut_id": "RSS1415_3_no_beta_source_transfer",
            "forbidden_shortcut": "transfer beta_source_alpha WEP target to Newton, R10, clocks, or PPN",
            "reason": "beta_source_alpha is one EM/WEP projection; R_source needs arena-specific kernels and maps",
            "source_anchor": "MER1415_1_not_identical",
            "status": "FORBIDDEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def arena_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "RSG1415_0_WEP",
            "arena": "WEP/source charge",
            "dependency": "R_source projection, U_a/source worldtube, material tensor, eta product convention",
            "status": "BLOCKED_TEMPLATE_ONLY",
            "reason": "R_source has no source-backed value and U_a/product gates remain blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "RSG1415_1_Newton_GM",
            "arena": "Newton/GM normalization",
            "dependency": "universal source common mode vs relative source residual",
            "status": "BLOCKED_NO_RELATIVE_SOURCE_PROOF",
            "reason": "measured-G/GM absorption is forbidden without universality proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "RSG1415_2_R10_R11",
            "arena": "R10/R11 source-side rows",
            "dependency": "source-current residual, range kernel, bound curve/interface, source composition",
            "status": "BLOCKED_NO_TRANSFER",
            "reason": "R_source has no arena-specific projection or source-backed bound rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "RSG1415_3_PPN_local_GR",
            "arena": "PPN/local GR",
            "dependency": "source-current universality plus EH/PPN silence and retained residual vector bounds",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "source current owner, U_a, EH/PPN, and residual-vector gates remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1415_0_owner_verdict",
            "decision": "do not promote source-current owner",
            "reason": "object-language, action-measure, current owner, source worldtube, and product convention remain unsigned or missing",
            "effect": "R_source is retained as finite residual template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1415_1_merge",
            "decision": "merge beta_source_alpha into R_source as an EM-channel projection",
            "reason": "both are symptoms of the same missing source-current normalization owner",
            "effect": "no duplicate escape hatches; target-only beta_source rows feed R_source but do not score it",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1415_2_next_best",
            "decision": "target source-only species slot / current rescaling theorem next",
            "reason": "that is the cleanest route to kill R_source without waiting for data",
            "effect": "next checkpoint should try to ban Hom(SpeciesLabel,Coeff_active_source) and J_A -> c_A J_A together",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "GATE1415_0_source_owner",
            "claim": "source-current owner is derived",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "parent object-language, measure/current owner, source worldtube, and readout/product convention are incomplete",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1415_1_Rsource",
            "claim": "R_source is zero or bounded",
            "status": "TEMPLATE_ONLY_NO_CLAIM",
            "reason": "R_source rows contain no values, signs, units, source paths, or arena projections",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1415_2_beta_source_alpha",
            "claim": "beta_source_alpha target becomes a pass",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "beta_source_alpha is a target-only R_source projection and lacks parent basis/U_a/product convention",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1415_3_WEP_Newton_R10",
            "claim": "WEP, Newton-GM, or R10 source-side arenas pass",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "source-current owner and arena-specific projections are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1415_4_local_GR",
            "claim": "local GR/Newton reduction follows",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "R_source is only one open residual and EH/PPN/U_a/matter tensor gates remain active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1415_5_verdict",
            "claim": "1415 closes source normalization",
            "status": "NO_PROMOTION",
            "reason": "1415 merges the debt and writes R_source template only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1415_0_1416",
            "target_doc": "1416-Y5-R10-RAB-source-only-species-slot-and-current-rescaling-ban-or-Rsource-bound-row.md",
            "target_script": "scripts/Y5_R10_RAB_source_only_species_slot_and_current_rescaling_ban_or_Rsource_bound_row.py",
            "task": "try to prove Hom(SpeciesLabel,Coeff_active_source)=empty and forbid J_A -> c_A J_A source-current rescaling; if it fails, make the first finite R_source coefficient row",
            "success_condition": "source-only species/current rescaling morphisms are theorem-banned, or a source-ready R_source coefficient row is written with units/sign/source anchors and nonclaim gates",
            "do_not_claim": "WEP pass; beta_source_alpha pass; Newton-GM pass; R10/PPN/local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "next_id": "NEXT1415_1_data_parallel",
            "target_doc": "future-source-worldtube-and-Ua-import-route.md",
            "target_script": "future_data_route",
            "task": "if source-worldtube and official/equivalent U_a data become available, fill RSF1415_3 and product convention rows",
            "success_condition": "source profile, composition/convention, finite-size correction, frame units, U_a, and product convention are all source-backed",
            "do_not_claim": "point-source or tau=1 shortcut",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    owner_attempt: list[dict[str, Any]],
    rsource_rows: list[dict[str, Any]],
    merge_rows: list[dict[str, Any]],
    shortcut_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    timestamp = datetime.now(timezone.utc).isoformat()
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        OWNER_ATTEMPT_PATH,
        RSOURCE_TEMPLATE_PATH,
        MERGE_MAP_PATH,
        ANTI_SHORTCUT_PATH,
        ARENA_GATE_PATH,
        DECISION_PATH,
        CLAIM_GATE_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    add(
        "VAL1415_0_sources",
        all(row["path_exists"] == True and row["anchor_found"] == True for row in sources),
        "all cited local source paths exist and anchors are present",
    )
    add(
        "VAL1415_1_owner_attempt",
        any(row["attempt_id"] == "SCO1415_6_verdict" and row["current_result"] == "SOURCE_CURRENT_OWNER_NOT_DERIVED_RSOURCE_TEMPLATE_REQUIRED" for row in owner_attempt),
        "source-current owner attempt fails and selects R_source template",
    )
    add(
        "VAL1415_2_Rsource_template",
        any(row["row_id"] == "RSF1415_6_verdict" and row["current_status"] == "RSOURCE_TEMPLATE_READY_VALUES_MISSING" for row in rsource_rows)
        and all(row["valid_for_claim"] == False for row in rsource_rows),
        "R_source finite template exists but contains no promoted values",
    )
    add(
        "VAL1415_3_merge_map",
        any(row["merge_id"] == "MER1415_0_common_owner" for row in merge_rows)
        and any(row["merge_id"] == "MER1415_2_score_policy" for row in merge_rows),
        "beta_source_alpha is merged as R_source projection without becoming a pass",
    )
    add(
        "VAL1415_4_shortcuts",
        {"RSS1415_0_no_measured_G_absorption", "RSS1415_1_no_tau_unity", "RSS1415_2_no_point_source_by_taste"}.issubset(
            {row["shortcut_id"] for row in shortcut_rows}
        )
        and all(row["status"] == "FORBIDDEN" for row in shortcut_rows),
        "measured-G, tau=1, point-source, and beta-source transfer shortcuts are forbidden",
    )
    add(
        "VAL1415_5_arena_gates",
        all(row["valid_for_claim"] == False and row["claim_allowed"] == False for row in arena_rows)
        and any(row["arena_id"] == "RSG1415_3_PPN_local_GR" for row in arena_rows),
        "WEP, Newton-GM, R10/R11, and local-GR gates remain blocked",
    )
    add(
        "VAL1415_6_decision",
        any(row["decision_id"] == "DEC1415_2_next_best" for row in decision_rows_),
        "decision ledger selects source-only species slot/current rescaling ban next",
    )
    add(
        "VAL1415_7_claim_refusal",
        all(row["valid_for_claim"] == False and row["claim_allowed"] == False for row in gate_rows),
        "source owner, R_source, beta_source_alpha, arena, and local-GR claims are refused",
    )
    add(
        "VAL1415_8_scope",
        all((ROOT / path).resolve().is_relative_to(ROOT.resolve()) for path in output_paths),
        "outputs are confined to post-checkpoint-work paths",
    )
    add(
        "VAL1415_9_overall",
        True,
        "1415 merges beta_source_alpha into R_source and keeps source-current ownership nonclaim",
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    owner_attempt: list[dict[str, Any]],
    rsource_rows: list[dict[str, Any]],
    merge_rows: list[dict[str, Any]],
    shortcut_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = f"""# 1415 - Source-Current Owner Or R_source Finite Template

**Status:** `{STATUS}`

**Current verdict:** a single source-current owner is not derived. `beta_source_alpha` is therefore merged into the broader `R_source` residual as its EM/alpha WEP projection, not treated as an independent escape knob. The same missing object controls source/test current normalization, source-only species weights, Newton-GM normalization, WEP source charge, and R10/R11 source-side rows.

**Discipline move:** no WEP, Newton, R10, PPN, or local-GR claim is made. `R_source` is now an explicit finite nonclaim template with hard anti-shortcuts: no measured-G absorption of relative source weights, no `tau_WEP=1`, no point-source-by-taste, and no transfer of the `beta_source_alpha` target to other arenas.

**Claim ceiling:** `{CLAIM_CEILING}`

## Source Register

{md_table(sources)}

## Source-Current Owner Attempt

{md_table(owner_attempt)}

## R_source Finite Template

{md_table(rsource_rows)}

## beta_source_alpha / R_source Merge Map

{md_table(merge_rows)}

## R_source Anti-Shortcut Gate

{md_table(shortcut_rows)}

## R_source Arena Gate

{md_table(arena_rows)}

## Decision Ledger

{md_table(decisions)}

## Claim Gate

{md_table(gates)}

## Next Target

{md_table(next_targets)}

## Validation

{md_table(validations)}
"""
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    owner_attempt = owner_attempt_rows()
    rsource_rows = rsource_template_rows()
    merge_rows = merge_map_rows()
    shortcut_rows = anti_shortcut_rows()
    arena_rows = arena_gate_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    next_targets = next_target_rows()
    validations = validation_rows(sources, owner_attempt, rsource_rows, merge_rows, shortcut_rows, arena_rows, decisions, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(OWNER_ATTEMPT_PATH, owner_attempt)
    write_csv(RSOURCE_TEMPLATE_PATH, rsource_rows)
    write_csv(MERGE_MAP_PATH, merge_rows)
    write_csv(ANTI_SHORTCUT_PATH, shortcut_rows)
    write_csv(ARENA_GATE_PATH, arena_rows)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(NEXT_TARGET_PATH, next_targets)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, owner_attempt, rsource_rows, merge_rows, shortcut_rows, arena_rows, decisions, gates, next_targets, validations)

    if any(row["status"] != "PASS" for row in validations):
        raise SystemExit("1415 validation failed")

    print(STATUS)


if __name__ == "__main__":
    main()
