from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1800"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1800_0_1799_doc",
        "source_key": "1799_handoff",
        "source_path": ROOT / "1799-Y5-R2FR-minimal-parent-current-action-skeleton-or-first-Ix-row.md",
        "needles": ["DEC1799_3_next", "NEXT1799_0_primary"],
        "role": "selects X positive-operator activation or Yukawa fallback as 1800 target",
    },
    {
        "source_id": "SRC1800_1_1799_validation",
        "source_key": "1799_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1799_VALIDATION.csv",
        "needles": ["VAL1799_OVERALL", "PASS"],
        "role": "confirms 1799 passed before 1800 starts",
    },
    {
        "source_id": "SRC1800_2_1799_ix_row",
        "source_key": "1799_ix_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1799_FIRST_IX_SOURCE_BOUND_ROW.csv",
        "needles": ["IXR1799_1_operator_sign", "IXR1799_7_acceptance"],
        "role": "declares operator/source/boundary/projection/fallback inputs for I_X",
    },
    {
        "source_id": "SRC1800_3_967_lemma",
        "source_key": "memory_operator_lemma",
        "source_path": RESIDUALS / "P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
        "needles": ["MPO967_4_energy_identity", "MPO967_6_verdict"],
        "role": "relative positive-operator zero theorem",
    },
    {
        "source_id": "SRC1800_4_968_inputs",
        "source_key": "memory_input_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
        "needles": ["MOI968_2_operator_L", "MOI968_8_verdict"],
        "role": "activation inputs missing for positive-operator route",
    },
    {
        "source_id": "SRC1800_5_973_JX",
        "source_key": "JX_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_973_JX_DECOMPOSITION_GATE.csv",
        "needles": ["JXD973_0_kinetic_affine", "JXD973_6_verdict"],
        "role": "J_X source-zero gate",
    },
    {
        "source_id": "SRC1800_6_970_action",
        "source_key": "quadratic_action",
        "source_path": RESIDUALS / "P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
        "needles": ["QMA970_0_action", "QMA970_7_verdict"],
        "role": "relative quadratic X action and branch tension",
    },
    {
        "source_id": "SRC1800_7_557_force",
        "source_key": "bulk_memory_force_map",
        "source_path": RESIDUALS / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_FORCE_LAW_MAP.csv",
        "needles": ["BMRF557_0_static_bulk_operator", "BMRF557_3_Hamiltonian_projection"],
        "role": "finite-range force law and Hamiltonian projection map",
    },
    {
        "source_id": "SRC1800_8_557_yukawa",
        "source_key": "bulk_memory_yukawa_row",
        "source_path": RESIDUALS / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_YUKAWA_FILL_ROW.csv",
        "needles": ["FB557_0_bulk_memory_range_zero_or_Yukawa_bound", "MISSING_SOURCE_NORMALIZED_ALPHA_LAMBDA_CURVE"],
        "role": "unfilled Yukawa bound row",
    },
    {
        "source_id": "SRC1800_9_prefactor",
        "source_key": "zx_lambda_prefactor",
        "source_path": RESIDUALS / "P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv",
        "needles": ["PR562_2_canonical_mass_and_range", "PR562_5_positive_operator_identity"],
        "role": "lambda and alpha prefactor formula register",
    },
    {
        "source_id": "SRC1800_10_alpha_template",
        "source_key": "zx_lambda_alpha_template",
        "source_path": RESIDUALS / "P8_Y5_R10_ZX_LAMBDA_ALPHA_ROW_TEMPLATE.csv",
        "needles": ["R10_ZX_lambda_prefactor_branch", "MISSING_DIGITIZED_ALPHA_BOUND"],
        "role": "alpha(lambda) row template",
    },
    {
        "source_id": "SRC1800_11_1035_template",
        "source_key": "r10_1035_template",
        "source_path": RESIDUALS / "R10_alpha_lambda_curve_MTS_1035_KX_PROFILE_TEMPLATE_NONCLAIM.csv",
        "needles": ["MTS_1035_KX_PROFILE_TEMPLATE_NONCLAIM", "MISSING_KX_BETA_SOURCE_BETA_TEST_TAILS"],
        "role": "K_X/profile product nonclaim template",
    },
    {
        "source_id": "SRC1800_12_1036_template",
        "source_key": "r10_1036_template",
        "source_path": RESIDUALS / "R10_alpha_lambda_curve_MTS_1036_PARENT_X_BETA_TEMPLATE_NONCLAIM.csv",
        "needles": ["parent_X_beta_product_template", "MISSING_KX_BETA_SOURCE_BETA_TEST_TAIL_ENVELOPE"],
        "role": "source-test product law nonclaim template",
    },
    {
        "source_id": "SRC1800_13_1038_template",
        "source_key": "r10_1038_template",
        "source_path": RESIDUALS / "R10_alpha_lambda_curve_MTS_1038_OMEGA_DCX_OR_BETA_BOUND_TEMPLATE_NONCLAIM.csv",
        "needles": ["bounded_beta_cross_arena_template", "MISSING_KX_TIMES_BETA_S_ABS_BETA_T_ABS_PLUS_TAILS"],
        "role": "absolute beta/tail bound template",
    },
    {
        "source_id": "SRC1800_14_1039_template",
        "source_key": "r10_1039_template",
        "source_path": RESIDUALS / "R10_alpha_lambda_curve_MTS_1039_BOUNDARY_QX_KBOUNDARY_TEMPLATE_NONCLAIM.csv",
        "needles": ["R10_edge_beta_template", "MISSING_KX_QBAR_EDGE_XH_QBAR_XT"],
        "role": "boundary/source-test edge projection template",
    },
    {
        "source_id": "SRC1800_15_1041_template",
        "source_key": "r10_1041_template",
        "source_path": RESIDUALS / "R10_alpha_lambda_curve_MTS_1041_THETAX_PX_TEMPLATE_NONCLAIM.csv",
        "needles": ["MTS_1041_POSITIVE_NOHAIR_TEMPLATE", "MISSING_POSITIVE_OPERATOR_SOURCE_FILE"],
        "role": "Theta_X/P_X nohair template",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1800_SOURCE_REGISTER.csv",
    "positive_operator_activation_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1800_POSITIVE_OPERATOR_ACTIVATION_AUDIT.csv",
    "yukawa_fallback_row": RESIDUALS / "P8_Y5_PARENT_QLOC_1800_YUKAWA_FALLBACK_ROW.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1800_ACCEPTANCE_GATE.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1800_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1800_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1800_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1800_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1800_VALIDATION.csv",
}

DOC_PATH = ROOT / "1800-Y5-R2FR-X-positive-operator-activation-or-Yukawa-fallback-row.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and all(needle in text for needle in needles),
                "role": source["role"],
            }
        )
    return rows


def src(*keys: str) -> str:
    by_key = {source["source_key"]: source["source_path"] for source in SOURCES}
    return ";".join(str(by_key[key]) for key in keys)


def positive_operator_activation_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "XPA1800_0_parent_X_route",
            "needed_input": "parent-selected X route",
            "activation_condition": "X sector is absent/gauge/topological, or active positive source-free field, or sourced residual branch",
            "current_evidence": "1799 skeleton and 1041 route gate are contracts only",
            "current_status": "ROUTE_NOT_PARENT_SELECTED",
            "missing_input": "MISSING_PARENT_ROUTE_SELECTION",
            "source_paths": src("1799_ix_row", "r10_1041_template"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "XPA1800_1_operator_sign_gap",
            "needed_input": "Z_X/A^ij and M_X^2",
            "activation_condition": "Z_X>0 and M_X^2>0, or semidefinite operator with zero-mode removal",
            "current_evidence": "PR562 gives lambda_X=sqrt(Z_X/M_X^2), but Z_X and M_X^2 are not parent-derived",
            "current_status": "OPERATOR_SIGN_GAP_MISSING",
            "missing_input": "MISSING_ZX;MISSING_MX2;MISSING_OPERATOR_SOURCE",
            "source_paths": src("zx_lambda_prefactor", "memory_input_audit", "quadratic_action"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "XPA1800_2_JX_zero",
            "needed_input": "J_X=0",
            "activation_condition": "J_matter=J_chiD_wall=J_boundary=J_readout=J_history=0 in the local exterior",
            "current_evidence": "JXD973 splits the terms but marks total J_X zero not proved",
            "current_status": "SOURCE_ZERO_NOT_PROVED",
            "missing_input": "MISSING_JX_COMPONENT_ZERO_OR_BOUNDS",
            "source_paths": src("JX_gate", "bulk_memory_force_map"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "XPA1800_3_boundary_zero_mode",
            "needed_input": "boundary flux and zero-mode removal",
            "activation_condition": "Pi_X delta X|partialD=0 and constant/topological zero mode removed or universal derivative-free",
            "current_evidence": "MPO967 and 1799 require boundary data; no local boundary class is signed",
            "current_status": "BOUNDARY_ZERO_MODE_MISSING",
            "missing_input": "MISSING_BOUNDARY_FLUX_ZERO;MISSING_ZERO_MODE_RULE",
            "source_paths": src("memory_operator_lemma", "bulk_memory_yukawa_row"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "XPA1800_4_Hamiltonian_projection",
            "needed_input": "Pi_M^H projection of X charge",
            "activation_condition": "Pi_M^H dJ_X=0 or finite coefficient maps X exchange into source-normalized alpha(lambda)",
            "current_evidence": "BMRF557_3 keeps Hamiltonian projection missing",
            "current_status": "PIM_H_PROJECTION_MISSING",
            "missing_input": "MISSING_HAMILTONIAN_PROJECTION_ZERO_OR_COEFFICIENT",
            "source_paths": src("bulk_memory_force_map", "1799_ix_row"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "XPA1800_5_verdict",
            "needed_input": "X nohair theorem activation",
            "activation_condition": "XPA1800_0 through XPA1800_4 close in one branch",
            "current_evidence": "each activation input is source-mapped but not supplied",
            "current_status": "X_POSITIVE_OPERATOR_NOT_ACTIVATED",
            "missing_input": "MISSING_PARENT_OPERATOR_SOURCE_BOUNDARY_PROJECTION_PACK",
            "source_paths": src("1799_ix_row", "memory_operator_lemma", "zx_lambda_prefactor"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
    ]


def yukawa_fallback_row_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "YFR1800_0_formula",
            "target": "alpha_X(lambda_X)",
            "formula": "lambda_X=sqrt(Z_X/M_X^2); K_X=s_X/(4*pi*Z_X*G_obs); alpha_X(lambda)=K_X Qbar_XH(lambda) qbar_XT",
            "lambda_value": "MISSING_lambda_X",
            "alpha_predicted": "MISSING_KX_QBAR_XH_QBAR_XT",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "required_input": "Z_X;M_X^2;s_X;G_obs;Qbar_XH;qbar_XT;source/test charge normalization;R10 bound curve;source_path",
            "source_paths": src("zx_lambda_prefactor", "zx_lambda_alpha_template", "r10_1036_template"),
            "status": "STAGED_NONCLAIM_TEMPLATE",
            "units": "alpha_lambda_curve",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "YFR1800_1_nohair_zero_switch",
            "target": "alpha_X=0",
            "formula": "alpha_X=0 iff parent route absent/no-pole or X=0 theorem closes including source, boundary and projection",
            "lambda_value": "ALL_LOCAL_R10_RANGE",
            "alpha_predicted": "MISSING_SIGNED_ZERO_THEOREM",
            "alpha_bound": "not_applicable_until_zero_theorem_signed",
            "required_input": "parent no-pole/nohair certificate;hidden tails zero;boundary/source/test projection zero",
            "source_paths": src("r10_1035_template", "r10_1036_template", "r10_1038_template"),
            "status": "ZERO_SWITCH_REJECTED",
            "units": "gate",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "YFR1800_2_absolute_tail_envelope",
            "target": "bounded alpha_X fallback",
            "formula": "|alpha_X(lambda)| <= |K_X(lambda)|(|beta_s beta_t| + |edge_tail| + |history_tail| + |boundary_tail|)",
            "lambda_value": "MISSING_PARENT_LAMBDA_X",
            "alpha_predicted": "MISSING_ABSOLUTE_TAIL_ENVELOPE",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "required_input": "beta_s;beta_t;edge/history/boundary tail coefficients;profile normalization;bound curve",
            "source_paths": src("r10_1038_template", "r10_1039_template", "r10_1035_template"),
            "status": "TAIL_ENVELOPE_NOT_FILLED",
            "units": "alpha_lambda_curve",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "YFR1800_3_bound_comparison",
            "target": "R10 pass/fail comparison",
            "formula": "claim_allowed iff abs(alpha_predicted(lambda)) <= alpha_bound(lambda) for sourced rows and no MISSING markers",
            "lambda_value": "MISSING_NUMERIC_LAMBDA_ROWS",
            "alpha_predicted": "MISSING_NUMERIC_ALPHA_ROWS",
            "alpha_bound": "MISSING_DIGITIZED_ALPHA_BOUND",
            "required_input": "machine-readable R10 bound curve;valid units;source-backed predicted rows;runner output",
            "source_paths": src("zx_lambda_alpha_template", "bulk_memory_yukawa_row", "r10_1041_template"),
            "status": "BOUND_COMPARISON_NOT_RUNNABLE",
            "units": "runner_gate",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "YFR1800_4_acceptance",
            "target": "Yukawa fallback row acceptance",
            "formula": "YFR1800_0 through YFR1800_3 valid, sourced, numeric or theorem-zero, same convention, no MISSING markers",
            "lambda_value": "NOT_ACCEPTED",
            "alpha_predicted": "NOT_ACCEPTED",
            "alpha_bound": "NOT_ACCEPTED",
            "required_input": "complete source-backed row pack",
            "source_paths": src("bulk_memory_yukawa_row", "zx_lambda_prefactor", "zx_lambda_alpha_template"),
            "status": "REJECT_CURRENT_YUKAWA_FALLBACK_ROW",
            "units": "gate",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1800_0_nohair",
            "gate": "positive-operator X nohair theorem activates",
            "current_status": "FAIL_ACTIVATION_INPUTS_MISSING",
            "reason": "operator sign/gap, J_X=0, boundary zero and PiM projection are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1800_1_yukawa",
            "gate": "finite-range fallback row is executable",
            "current_status": "FAIL_NUMERIC_ALPHA_LAMBDA_INPUTS_MISSING",
            "reason": "lambda, alpha, source/test charges, projection and bound curve are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1800_2_no_linear_coupling_shortcut",
            "gate": "source-test product and absolute tails only",
            "current_status": "POLICY_PASS_NO_SCORE",
            "reason": "templates reject naked linear coupling shortcuts, but no numeric score exists",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1800_3_verdict",
            "gate": "I_X zero or finite fallback claim readiness",
            "current_status": "X_ACTIVATION_AND_FALLBACK_NOT_READY",
            "reason": "neither nohair theorem nor Yukawa fallback can be claimed",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1800_0_wrong_sign_or_zero_mode",
            "countermodel": "X has an allowed zero mode, wrong-sign kinetic term, or no positive mass gap",
            "survives_current_constraints": True,
            "why_survives": "Z_X, M_X^2 and zero-mode rules are missing",
            "what_kills_it": "operator sign/gap/zero-mode certificate",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1800_1_nonzero_source_charge",
            "countermodel": "source/test matter or readout carries nonzero X charge",
            "survives_current_constraints": True,
            "why_survives": "J_X=0 and Qbar_XH/qbar_XT are not derived",
            "what_kills_it": "source/test charge zero theorem or finite alpha(lambda) row",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1800_2_boundary_tail",
            "countermodel": "boundary/history/edge tail contributes to alpha_X or I_X",
            "survives_current_constraints": True,
            "why_survives": "boundary and tail coefficients are missing",
            "what_kills_it": "absolute tail envelope below bounds or zero theorem",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1800_3_projection_leak",
            "countermodel": "X exists but only leaks into Hamiltonian mass through Pi_M projection",
            "survives_current_constraints": True,
            "why_survives": "Pi_M^H projection is not zero-proved or sourced",
            "what_kills_it": "projection zero theorem or coefficient row",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1800_0_X_nohair",
            "claim": "X positive-operator theorem proves I_X=0",
            "status": "BLOCKED",
            "reason": "XPA1800_5 verdict is X_POSITIVE_OPERATOR_NOT_ACTIVATED",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1800_1_Yukawa_fallback",
            "claim": "finite alpha_X(lambda) fallback is scoreable",
            "status": "BLOCKED",
            "reason": "YFR1800_4 rejects the current row",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1800_2_I_X",
            "claim": "I_X is zero or bounded",
            "status": "BLOCKED",
            "reason": "neither activation nor fallback passes",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1800_3_local_GR_Newton",
            "claim": "local GR/Newton source-normalized branch is derived",
            "status": "BLOCKED",
            "reason": "first non-EH curl component remains live",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1800_0_nohair",
            "decision": "X_POSITIVE_OPERATOR_NOT_ACTIVATED",
            "reason": "operator sign/gap, J_X, boundary and projection inputs are missing",
            "next_action": "do not set I_X=0",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1800_1_fallback",
            "decision": "YUKAWA_FALLBACK_ROW_STAGED_NONCLAIM",
            "reason": "lambda/alpha formula is known, but parent coefficients and bound curve are missing",
            "next_action": "acquire or derive Z_X, M_X^2, Qbar_XH, qbar_XT, PiM projection and real R10 bound curve",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1800_2_policy",
            "decision": "NO_LINEAR_COUPLING_OR_CANCELLATION_SHORTCUT",
            "reason": "R10 templates require source-test product and absolute tail envelope",
            "next_action": "keep all finite fallback rows nonclaim until product inputs are sourced",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1800_3_next",
            "decision": "JX_SOURCE_ZERO_OR_COMPONENT_BOUND_PACK_NEXT",
            "reason": "J_X=0 is the most decisive missing nohair input and also supplies source/test charges for the fallback",
            "next_action": "build 1801 to prove J_X source silence or emit J_matter/J_chiD/J_boundary/J_readout/J_history component bounds",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1800_0_primary",
            "next_target": "1801-Y5-R2FR-JX-source-zero-or-component-bound-pack.md",
            "script": "scripts/Y5_R2FR_JX_source_zero_or_component_bound_pack.py",
            "objective": "prove J_X source silence for the X sector, or emit component bounds for J_matter, J_chiD_wall, J_boundary, J_readout and J_history",
            "selection_status": "selected",
            "success_condition": "J_X=0 theorem or finite source component envelope with source/test charges ready for alpha_X(lambda)",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1800_1_parallel_operator",
            "next_target": "1801b-Y5-R2FR-ZX-MX2-operator-sign-gap-source-row.md",
            "script": "scripts/Y5_R2FR_ZX_MX2_operator_sign_gap_source_row.py",
            "objective": "derive or source Z_X, M_X^2, lambda_X and operator sign/gap",
            "selection_status": "held_parallel",
            "success_condition": "operator sign/gap theorem or numeric lambda_X row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1800_2_parallel_R10",
            "next_target": "1801c-Y5-R2FR-real-R10-bound-curve-and-alphaX-runner.md",
            "script": "scripts/Y5_R2FR_real_R10_bound_curve_and_alphaX_runner.py",
            "objective": "acquire real R10 bound curve and run nonclaim alpha_X(lambda) fallback once coefficients exist",
            "selection_status": "held_parallel",
            "success_condition": "real bound curve plus sourced alpha_X prediction rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "positive_operator_activation_audit": positive_operator_activation_audit_rows(),
        "yukawa_fallback_row": yukawa_fallback_row_rows(),
        "acceptance_gate": acceptance_gate_rows(),
        "countermodel_ledger": countermodel_ledger_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
        shutil.copy2(path, RAB_QUEUE / f"JR1800_{key.upper()}.csv")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "pass", "passed"}


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return (
        all(boolish(row["exists"]) for row in rows),
        all(boolish(row["needles_present"]) for row in rows),
    )


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    claim_flags = (
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "valid_prediction_row",
        "theorem_zero",
        "gate_pass",
    )
    for rows in rows_map.values():
        for row in rows:
            for flag in claim_flags:
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    ready_flags = (
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "valid_prediction_row",
        "theorem_zero",
        "gate_pass",
    )
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                for flag in ready_flags:
                    if boolish(row.get(flag, False)):
                        return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not (MICROSCOPE_RESIDUALS / path.name).exists():
            return False
        if not (QUARANTINE / path.name).exists():
            return False
        if not (RAB_QUEUE / f"JR1800_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add(DOC_PATH.name)
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1800_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1800_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1800_2_nohair_not_activated",
            any(
                row["audit_id"] == "XPA1800_5_verdict"
                and row["current_status"] == "X_POSITIVE_OPERATOR_NOT_ACTIVATED"
                for row in rows_map["positive_operator_activation_audit"]
            )
            and all(not boolish(row["theorem_zero"]) and not boolish(row["valid_for_claim"]) for row in rows_map["positive_operator_activation_audit"]),
            "X positive-operator theorem is not activated",
        ),
        (
            "VAL1800_3_yukawa_row_rejected",
            any(
                row["row_id"] == "YFR1800_4_acceptance"
                and row["status"] == "REJECT_CURRENT_YUKAWA_FALLBACK_ROW"
                for row in rows_map["yukawa_fallback_row"]
            )
            and all(not boolish(row["accepted_for_scoring"]) and not boolish(row["valid_prediction_row"]) for row in rows_map["yukawa_fallback_row"]),
            "Yukawa fallback row is rejected and non-scoreable",
        ),
        (
            "VAL1800_4_acceptance_blocks",
            any(
                row["gate_id"] == "AC1800_3_verdict"
                and row["current_status"] == "X_ACTIVATION_AND_FALLBACK_NOT_READY"
                and not boolish(row["gate_pass"])
                for row in rows_map["acceptance_gate"]
            ),
            "acceptance gate blocks scoring",
        ),
        (
            "VAL1800_5_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live",
        ),
        (
            "VAL1800_6_claim_gates_blocked",
            all(row["status"] == "BLOCKED" and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "claim gates are blocked",
        ),
        ("VAL1800_7_no_claim_flags", no_claim_flags(rows_map), "no generated theorem/score/claim flags are true"),
        ("VAL1800_8_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1800_9_decision_next",
            any(
                row["decision_id"] == "DEC1800_3_next"
                and row["decision"] == "JX_SOURCE_ZERO_OR_COMPONENT_BOUND_PACK_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects J_X source zero or component bounds next",
        ),
        (
            "VAL1800_10_next_selected",
            any(row["route_id"] == "NEXT1800_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1800_11_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1800 CSVs parse"),
        ("VAL1800_12_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1800_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1800_14_formalization_untouched", formalization_untouched(), "no 1800 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1800_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1800 X positive-operator activation or Yukawa fallback row checkpoint",
        }
    )
    return rows


def clean_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(clean_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1800 - Y5/R2FR X Positive-Operator Activation or Yukawa Fallback Row",
            "",
            "## Verdict",
            "",
            "1800 tests the fork created by 1799. The clean nohair route does not activate because the operator sign/gap, `J_X=0`, boundary/zero-mode rule, and Hamiltonian projection are not parent-signed.",
            "",
            "The fallback route is now explicit but still nonclaim:",
            "",
            "`lambda_X=sqrt(Z_X/M_X^2)`, `K_X=s_X/(4*pi*Z_X*G_obs)`, and `alpha_X(lambda)=K_X Qbar_XH(lambda) qbar_XT`.",
            "",
            "That row cannot be scored until `Z_X`, `M_X^2`, source/test charges, projection coefficients, absolute tails, and a real bound curve exist.",
            "",
            "**Claim ceiling:** no `X=0` theorem, no scoreable `alpha_X(lambda)`, no `I_X` closure, no local-GR/Newton source-normalization claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1800.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Positive Operator Activation Audit",
            markdown_table(rows_map["positive_operator_activation_audit"], ["audit_id", "needed_input", "activation_condition", "current_status", "missing_input", "theorem_zero", "valid_for_claim"]),
            "",
            "## Yukawa Fallback Row",
            markdown_table(rows_map["yukawa_fallback_row"], ["row_id", "target", "formula", "lambda_value", "alpha_predicted", "alpha_bound", "status", "valid_for_claim"]),
            "",
            "## Acceptance Gate",
            markdown_table(rows_map["acceptance_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel_ledger"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a real fork in the road, not a dead end. Either `J_X` and the boundary/projection clauses go to zero, and the extra sector vanishes locally, or `X` becomes an empirical finite-range channel with the exact source/test product law. The next target is therefore `J_X`, because it feeds both exits.",
            "",
        ]
    )


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1800 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
