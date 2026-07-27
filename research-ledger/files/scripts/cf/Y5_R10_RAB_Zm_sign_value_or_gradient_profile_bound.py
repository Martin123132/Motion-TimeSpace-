from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1305"
TITLE = "1305-Y5-R10-RAB-Zm-sign-value-or-gradient-profile-bound"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
ZM_SIGN_VALUE_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_ZM_SIGN_VALUE_AUDIT.csv"
ZM_ACQUISITION_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_ZM_ACQUISITION_CONTRACT.csv"
B_GRAD_REQUIREMENTS_PATH = OUT_DIR / f"{PACK_ID}_B_GRAD_PROFILE_BOUND_REQUIREMENTS.csv"
BOUND_INPUT_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_BOUND_INPUT_UPDATE_NONCLAIM.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1305_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        ZM_SIGN_VALUE_AUDIT_PATH,
        ZM_ACQUISITION_CONTRACT_PATH,
        B_GRAD_REQUIREMENTS_PATH,
        BOUND_INPUT_UPDATE_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1305_0_1304_doc",
            "local_path": "1304-Y5-R10-RAB-memory-operator-owner-or-first-stress-bound-input.md",
            "needle": "Z_m_bar := sup_D |Z_m(X_B)|",
            "role": "handoff document naming the first Z_m_bar and B_grad_sp bound rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1305_1_1304_first_bound_rows",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1304_FIRST_STRESS_BOUND_INPUT_ROWS_NONCLAIM.csv",
            "needle": "KMS1304_0_Zm_bar_first_row",
            "role": "prior nonclaim bound rows being tightened",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1305_2_1304_positive_gap",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1304_ZM_POSITIVE_GAP_MAP_NONCLAIM.csv",
            "needle": "ZPG1304_0_Zm_positive",
            "role": "prior positive ellipticity map for Z_m",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1305_3_1304_gradient_route",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1304_GRADIENT_BOUND_ROUTE_NONCLAIM.csv",
            "needle": "GBR1304_0_energy_to_L2_gradient",
            "role": "prior gradient energy route for B_grad_sp",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1305_4_826_coefficients",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_826_COEFFICIENT_LEDGER.csv",
            "needle": "C826_0_Zm",
            "role": "Z_m is named as a needed memory kinetic coefficient but has missing parent value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1305_5_826_action_ansatz",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
            "needle": "L_m = -1/2 Z_m(X_B) nabla_mu m nabla^mu m - V_R(m;X_B)",
            "role": "candidate parent scalar-memory kinetic term that would own the Z_m sign",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1305_6_967_positive_operator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
            "needle": "RELATIVE_LEMMA_READY_PARENT_INPUTS_UNSIGNED",
            "role": "positive-operator theorem available only after signed parent inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1305_7_968_input_audit",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
            "needle": "MISSING_SIGN_CERTIFICATE",
            "role": "operator sign certificate explicitly missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1305_8_1042_nohair_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv",
            "needle": "FORMULA_ONLY_NOT_PARENT_SIGNED",
            "role": "nohair route blocked because positive kinetic operator is formula-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1305_9_970_quadratic_action",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
            "needle": "CONDITIONAL_POSITIVITY_OK_INPUTS_UNSIGNED",
            "role": "quadratic action route supports conditional positivity but not a parent-signed value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    z_m_sign_value_audit = [
        {
            "audit_id": "ZSA1305_0_no_ghost_sign",
            "target": "Z_m > 0",
            "derivation_attempt": "For the candidate Lorentzian scalar-memory term L_m=-1/2 Z_m(X_B) nabla_mu m nabla^mu m - V_R, healthy kinetic energy and the static elliptic reduction require Z_m positive on the selected local branch.",
            "current_evidence": "The coefficient ledger names Z_m and says positive/no-ghost is the acceptance gate, but supplies no parent sign theorem or value.",
            "result": "CONDITIONAL_SIGN_RULE_ONLY",
            "missing_to_close": "MISSING_PARENT_MEMORY_SECTOR_SIGNATURE;MISSING_Z_m_FUNCTION;MISSING_X_B_BRANCH_RANGE;MISSING_UNITS_NORMALIZATION",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_COEFFICIENT_LEDGER.csv;source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
            "source_anchor": "C826_0_Zm;AA826_1_memory_sector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ZSA1305_1_static_ellipticity",
            "target": "A_m^{ij}=Z_m h^{ij} positive",
            "derivation_attempt": "In the static local branch the operator map gives A_m^{ij}=Z_m h^{ij}; if h^{ij} is positive spatial metric, ellipticity reduces to Z_m >= Z_m_min > 0.",
            "current_evidence": "1304 derives the operator map, while 967/970 provide only relative positive-operator lemmas with unsigned inputs.",
            "result": "ELLIPTICITY_REDUCED_TO_Z_m_MIN_BUT_NOT_CLOSED",
            "missing_to_close": "MISSING_Z_m_MIN;MISSING_LOCAL_BRANCH;MISSING_DOMAIN_D_LOC;MISSING_FRAME_LOCK",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1304_ZM_POSITIVE_GAP_MAP_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
            "source_anchor": "ZPG1304_0_Zm_positive;MPO967_1_operator",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ZSA1305_2_upper_bound",
            "target": "finite Z_m_bar",
            "derivation_attempt": "A finite stress envelope needs Z_m_bar := sup_{x in D_loc}|Z_m(X_B(x))| on the same local domain and branch used by K_mem_stress^Sigma.",
            "current_evidence": "The symbol row exists, but no Z_m(X_B) function, X_B range, compact-domain selector, or normalization is supplied.",
            "result": "UPPER_BOUND_REDUCED_TO_PARENT_FUNCTION_AND_DOMAIN",
            "missing_to_close": "MISSING_Z_m_FUNCTION;MISSING_X_B_RANGE;MISSING_DOMAIN_COMPACTNESS;MISSING_UNITS_NORMALIZATION",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1304_FIRST_STRESS_BOUND_INPUT_ROWS_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_826_COEFFICIENT_LEDGER.csv",
            "source_anchor": "KMS1304_0_Zm_bar_first_row;C826_0_Zm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ZSA1305_3_same_branch_rule",
            "target": "same local/cosmology coefficient rule",
            "derivation_attempt": "If Z_m is allowed to float independently between local and cosmological fits, it becomes a hidden patch; a parent coefficient law must state which background scalars X_B set it in each arena.",
            "current_evidence": "C826_0 explicitly demands positive/no-ghost and same local/cosmology value rule, but the rule is absent.",
            "result": "BRANCH_MATCHING_RULE_REQUIRED",
            "missing_to_close": "MISSING_X_B_BACKGROUND_MAP;MISSING_BRANCH_SELECTOR;MISSING_RENORMALIZATION_RULE;MISSING_ARENA_MATCHING_PROOF",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_COEFFICIENT_LEDGER.csv",
            "source_anchor": "C826_0_Zm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ZSA1305_4_verdict",
            "target": "claim-grade Z_m sign/value",
            "derivation_attempt": "Attempted to promote the conditional no-ghost/ellipticity rule into a sourced parent sign/value.",
            "current_evidence": "All available rows stop at formula-only or missing-parent-value status.",
            "result": "NO_ZM_SIGN_OR_VALUE_CLAIM_KEEP_ACQUISITION_CONTRACT",
            "missing_to_close": "SUPPLY_PARENT_Z_m_LAW_OR_DEMOTE_MEMORY_STRESS_BOUND_TO_EXTERNAL_CLOSURE",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_COEFFICIENT_LEDGER.csv;source-intake/mts_residuals/P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv",
            "source_anchor": "C826_0_Zm;NHP1042_1_Z_positive",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    z_m_acquisition_contract = [
        {
            "contract_id": "ZAC1305_0_Zm_min",
            "symbol": "Z_m_min",
            "definition": "Z_m_min := inf_{x in D_loc} Z_m(X_B(x)) in the selected local branch and frame",
            "required_for": "positive ellipticity; energy-to-gradient bound; no-ghost gate",
            "acceptance_condition": "numeric or theorem-backed Z_m_min > 0 with source path, units, branch, and domain",
            "current_status": "MISSING_PARENT_FUNCTION_AND_BRANCH_RANGE",
            "first_source_path": "source-intake/mts_residuals/P8_Y5_R10_826_COEFFICIENT_LEDGER.csv",
            "first_source_anchor": "C826_0_Zm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ZAC1305_1_Zm_bar",
            "symbol": "Z_m_bar",
            "definition": "Z_m_bar := sup_{x in D_loc} |Z_m(X_B(x))| in the same local branch and frame",
            "required_for": "K_mem_stress^Sigma envelope; stress bound runner",
            "acceptance_condition": "numeric or theorem-backed finite upper bound with the same domain/branch as Z_m_min",
            "current_status": "MISSING_PARENT_FUNCTION_DOMAIN_AND_UNITS",
            "first_source_path": "source-intake/mts_residuals/P8_Y5_R10_1304_FIRST_STRESS_BOUND_INPUT_ROWS_NONCLAIM.csv",
            "first_source_anchor": "KMS1304_0_Zm_bar_first_row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ZAC1305_2_XB_range",
            "symbol": "Range_D(X_B)",
            "definition": "image of the background variables X_B(x) over D_loc for the local branch",
            "required_for": "evaluating inf/sup of Z_m(X_B)",
            "acceptance_condition": "source-backed local branch map or conservative interval for every X_B argument of Z_m",
            "current_status": "MISSING_X_B_ARGUMENT_LIST_AND_LOCAL_RANGE",
            "first_source_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
            "first_source_anchor": "AA826_1_memory_sector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ZAC1305_3_D_loc",
            "symbol": "D_loc",
            "definition": "compact local exterior/domain used for the local memory-stress and PPN/R10 branch",
            "required_for": "sup/inf, Sobolev constants, boundary flux, zero-mode rule",
            "acceptance_condition": "parent-selected or explicitly benchmarked domain with boundary class and coframe",
            "current_status": "MISSING_PARENT_SELECTED_DOMAIN",
            "first_source_path": "source-intake/mts_residuals/P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
            "first_source_anchor": "MOI968_1_domain_D",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ZAC1305_4_units_normalization",
            "symbol": "[Z_m]",
            "definition": "normalization of Z_m relative to m units, metric signature, and stress tensor convention",
            "required_for": "dimensional consistency of K_mem_stress^Sigma and alpha/PPN translations",
            "acceptance_condition": "one source-backed convention used across local and cosmology branches",
            "current_status": "MISSING_PARENT_LAGRANGIAN_NORMALIZATION",
            "first_source_path": "source-intake/mts_residuals/P8_Y5_R10_1304_FIRST_STRESS_BOUND_INPUT_ROWS_NONCLAIM.csv",
            "first_source_anchor": "KMS1304_0_Zm_bar_first_row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ZAC1305_5_same_branch_rule",
            "symbol": "Z_m^{local}=Z_m[X_B^{local}] and Z_m^{cosmo}=Z_m[X_B^{cosmo}]",
            "definition": "single parent coefficient law evaluated on different backgrounds, not separately tuned coefficients",
            "required_for": "avoiding patchwork coefficient freedom",
            "acceptance_condition": "parent law plus branch selector, or explicit theorem that local coefficient decouples from cosmology without retuning",
            "current_status": "MISSING_ARENA_MATCHING_RULE",
            "first_source_path": "source-intake/mts_residuals/P8_Y5_R10_826_COEFFICIENT_LEDGER.csv",
            "first_source_anchor": "C826_0_Zm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    b_grad_requirements = [
        {
            "requirement_id": "BGR1305_0_energy_route",
            "target": "B_grad_sp",
            "bound_formula": "G2_m := int_D sum_i |nabla^i m nabla^i m| <= Z_m_min^-1 (||m||_2 ||J_m||_2 + |Phi_boundary| + |E_indef|)",
            "required_inputs": "Z_m_min;J_m_L2_norm;m_L2_norm;Phi_boundary_bound;E_indef_sign_or_bound;M_m2_nonnegative;D_loc_measure",
            "status": "FORMAL_ROUTE_LOCKED_INPUTS_MISSING",
            "effect_if_supplied": "gives an L2 gradient bound but not yet a pointwise stress envelope",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1304_GRADIENT_BOUND_ROUTE_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
            "source_anchor": "GBR1304_0_energy_to_L2_gradient;MPO967_4_energy_identity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "BGR1305_1_pointwise_lift",
            "target": "B_grad_sp",
            "bound_formula": "B_grad_sp <= C_reg(D_loc,L_m) [G2_m + source_norms + boundary_norms]",
            "required_inputs": "C_reg;domain_regular_boundary;operator_coefficient_bounds;source_norm_class;boundary_norm_class;frame_lock",
            "status": "POINTWISE_LIFT_MISSING",
            "effect_if_supplied": "turns the L2 route into the sup_x sum_i |nabla^i m nabla^i m| input used by K_mem_stress^Sigma",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1304_GRADIENT_BOUND_ROUTE_NONCLAIM.csv",
            "source_anchor": "GBR1304_1_L2_to_pointwise",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "BGR1305_2_direct_profile_route",
            "target": "B_grad_sp",
            "bound_formula": "B_grad_sp >= sup_{x in D_loc} sum_i |nabla^i m_profile(x) nabla^i m_profile(x)| after solving the local sourced/boundary equation",
            "required_inputs": "local_operator;J_m_profile;boundary_condition;D_loc;coframe;regular_solution_class",
            "status": "DIRECT_PROFILE_MISSING",
            "effect_if_supplied": "bypasses Sobolev constants but requires a real local profile or conservative envelope",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
            "source_anchor": "MOI968_2_operator_L;MOI968_5_zero_source;MOI968_6_boundary_data",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "BGR1305_3_nohair_zero_shortcut",
            "target": "B_grad_sp=0",
            "bound_formula": "B_grad_sp=0 if signed operator owner, Z_m_min>0, M_m^2>=0/gap or zero-mode removal, J_m=0, boundary flux=0, and frame/projector silence all hold",
            "required_inputs": "parent_operator_owner;Z_m_min;M_m2_or_zero_mode_rule;J_m_zero;boundary_flux_zero;readout_silence",
            "status": "ZERO_SHORTCUT_BLOCKED_NOT_PARENT_SIGNED",
            "effect_if_supplied": "would close memory-gradient contribution without empirical profile fitting",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv",
            "source_anchor": "NHP1042_6_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "BGR1305_4_verdict",
            "target": "B_grad_sp acquisition",
            "bound_formula": "No numeric/profile bound follows until Z_m_min and source/boundary/domain data exist.",
            "required_inputs": "Z_m_min first, then source/boundary/domain/regularity package",
            "status": "B_GRAD_PROFILE_BOUND_NOT_CLOSED",
            "effect_if_supplied": "route remains acquisition-ready, not score-ready",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1304_FIRST_STRESS_BOUND_INPUT_ROWS_NONCLAIM.csv",
            "source_anchor": "KMS1304_1_B_grad_sp_first_row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    bound_input_update = [
        {
            "update_id": "BUI1305_0_Zm_bar",
            "prior_input": "KMS1304_0_Zm_bar_first_row",
            "symbol": "Z_m_bar",
            "new_status": "ACQUISITION_CONTRACT_LOCKED_VALUE_MISSING",
            "supplied_value": "MISSING_Z_m_FUNCTION_AND_X_B_RANGE",
            "runner_effect": "K_mem_stress runner remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "BUI1305_1_B_grad_sp",
            "prior_input": "KMS1304_1_B_grad_sp_first_row",
            "symbol": "B_grad_sp",
            "new_status": "PROFILE_BOUND_REQUIREMENTS_LOCKED_VALUE_MISSING",
            "supplied_value": "MISSING_Z_m_min_SOURCE_BOUNDARY_DOMAIN_REGULARITY",
            "runner_effect": "K_mem_stress runner remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "BUI1305_2_Zm_min_supporting_input",
            "prior_input": "ZPG1304_0_Zm_positive",
            "symbol": "Z_m_min",
            "new_status": "FIRST_SUPPORTING_INPUT_CREATED_VALUE_MISSING",
            "supplied_value": "MISSING_PARENT_SIGN_THEOREM_OR_NUMERIC_LOWER_BOUND",
            "runner_effect": "energy route cannot execute without positive lower bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "BUI1305_3_no_score",
            "prior_input": "KMRUN1303_0_bound_formula",
            "symbol": "K_mem_stress^Sigma",
            "new_status": "NO_SCORE_NO_LOCAL_GR_CLAIM",
            "supplied_value": "NONE",
            "runner_effect": "bound schema is sharpened only; no numerical/local-GR pass is recorded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1305_0_Zm_positive",
            "claim": "Z_m is positive in the local branch",
            "current_status": "BLOCKED_PARENT_SIGN_NOT_SUPPLIED",
            "reason": "the corpus gives the no-ghost/ellipticity condition but not a parent-signed Z_m law",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1305_1_Zm_bar",
            "claim": "finite source-backed Z_m_bar exists",
            "current_status": "BLOCKED_FUNCTION_DOMAIN_RANGE_MISSING",
            "reason": "Z_m(X_B), Range_D(X_B), D_loc, and units normalization are absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1305_2_B_grad_sp",
            "claim": "B_grad_sp is bounded",
            "current_status": "BLOCKED_PROFILE_AND_POINTWISE_LIFT_MISSING",
            "reason": "energy route needs Z_m_min/source/boundary inputs; pointwise route needs C_reg and domain regularity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1305_3_K_mem_runner",
            "claim": "K_mem_stress^Sigma is scoreable",
            "current_status": "BLOCKED_NO_NUMERIC_OR_THEOREM_INPUTS",
            "reason": "Z_m_bar and B_grad_sp remain acquisition contracts only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1305_4_local_GR",
            "claim": "local GR/Newton/PPN recovery follows from this route",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "memory stress channel is not closed and cannot be used as a local-GR proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1305_0_Zm_value_not_derived",
            "decision": "do not claim Z_m positivity/value",
            "because": "all evidence is conditional or formula-only, and C826_0 explicitly records missing parent value",
            "next_action": "try to derive/source the parent function Z_m(X_B) and the local X_B branch range",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1305_1_gradient_route_order",
            "decision": "attack Z_m_min before trying to score B_grad_sp",
            "because": "the energy-to-gradient route has Z_m_min as its first multiplicative denominator and sign gate",
            "next_action": "if Z_m(X_B) remains absent, demote memory stress closure to explicit external input rather than hiding it",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1305_0_1306",
            "target_file": "1306-Y5-R10-RAB-Zm-parent-function-or-XB-domain-range.md",
            "target_script": "scripts/Y5_R10_RAB_Zm_parent_function_or_XB_domain_range.py",
            "task": "try to derive or source the parent function Z_m(X_B), the local branch/domain range of X_B, and the normalization needed to compute Z_m_min and Z_m_bar",
            "success_condition": "source-backed parent coefficient law or theorem-bound gives Z_m_min>0 and finite Z_m_bar, or the missing coefficient is demoted to explicit closure input",
            "do_not": "do not tune Z_m separately per arena or claim K_mem_stress/local-GR from an unsigned coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(ZM_SIGN_VALUE_AUDIT_PATH, z_m_sign_value_audit)
    write_csv(ZM_ACQUISITION_CONTRACT_PATH, z_m_acquisition_contract)
    write_csv(B_GRAD_REQUIREMENTS_PATH, b_grad_requirements)
    write_csv(BOUND_INPUT_UPDATE_PATH, bound_input_update)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1305_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1305_1_zm_verdict_nonclaim",
            "Z_m sign/value audit blocks claims",
            any(
                row["audit_id"] == "ZSA1305_4_verdict"
                and row["result"] == "NO_ZM_SIGN_OR_VALUE_CLAIM_KEEP_ACQUISITION_CONTRACT"
                for row in z_m_sign_value_audit
            ),
            ";".join(str(row["audit_id"]) + "=" + str(row["result"]) for row in z_m_sign_value_audit),
        )
    )
    required_contracts = {"ZAC1305_0_Zm_min", "ZAC1305_1_Zm_bar", "ZAC1305_2_XB_range", "ZAC1305_3_D_loc", "ZAC1305_4_units_normalization"}
    validations.append(
        validation_row(
            "VAL1305_2_acquisition_contract_complete",
            "Z_m acquisition contract includes lower bound, upper bound, branch range, domain, and units",
            required_contracts.issubset({str(row["contract_id"]) for row in z_m_acquisition_contract}),
            ";".join(str(row["contract_id"]) for row in z_m_acquisition_contract),
        )
    )
    gradient_text = ";".join(str(row["required_inputs"]) for row in b_grad_requirements)
    validations.append(
        validation_row(
            "VAL1305_3_gradient_requirements_locked",
            "B_grad_sp requirements include Z_m_min, source, boundary, and regularity inputs",
            all(token in gradient_text for token in ["Z_m_min", "J_m", "boundary", "C_reg"]),
            gradient_text,
        )
    )
    validations.append(
        validation_row(
            "VAL1305_4_bound_updates_non_executable",
            "bound input updates do not execute the K_mem_stress score",
            len(bound_input_update) == 4 and all("blocked" in str(row["runner_effect"]).lower() or "cannot execute" in str(row["runner_effect"]).lower() or "no numerical" in str(row["runner_effect"]).lower() for row in bound_input_update),
            ";".join(str(row["update_id"]) + "=" + str(row["runner_effect"]) for row in bound_input_update),
        )
    )
    validations.append(
        validation_row(
            "VAL1305_5_claim_gates_block",
            "all local claim gates remain blocked",
            len(claim_gates) == 5 and all(str(row["current_status"]).startswith("BLOCKED") for row in claim_gates),
            ";".join(str(row["gate_id"]) + "=" + str(row["current_status"]) for row in claim_gates),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        ZM_SIGN_VALUE_AUDIT_PATH,
        ZM_ACQUISITION_CONTRACT_PATH,
        B_GRAD_REQUIREMENTS_PATH,
        BOUND_INPUT_UPDATE_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as error:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{error}")
    validations.append(validation_row("VAL1305_6_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1305_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1305_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, z_m_sign_value_audit, z_m_acquisition_contract, b_grad_requirements, bound_input_update, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1305_9_next_target_1306",
            "next target routes to Z_m parent function or X_B domain range",
            next_target[0]["next_id"] == "NEXT1305_0_1306" and "Zm-parent-function" in str(next_target[0]["target_file"]),
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1305_10_overall",
            "overall 1305 validation",
            overall_pass,
            "1305 fails to prove Z_m sign/value, locks exact Z_m_min/Z_m_bar/X_B/domain/units acquisition contract, locks B_grad_sp route requirements, keeps K_mem_stress and local-GR claims blocked, and routes to 1306",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1305 Y5 R10 RAB Zm sign value or gradient profile bound

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** the `Z_m` sign/value proof does **not** close from the current corpus. The work reduces the problem cleanly: `Z_m > 0` is the no-ghost/static-ellipticity condition, `Z_m_min` is the first energy-bound denominator, and `Z_m_bar` is the first stress-envelope multiplier. But the parent function `Z_m(X_B)`, local `X_B` range, domain `D_loc`, and units normalization are not supplied.

**Main progress:** the missing coupling is now a precise acquisition contract, not a vague complaint. This is the coupling bottleneck in a form we can hunt: source/derive `Z_m(X_B)`, then compute or theorem-bound `Z_m_min` and `Z_m_bar`.

**Still blocked:** no `K_mem_stress^Sigma`, R10, PPN, no-hair, or local-GR claim follows from 1305. The gradient route is ready in form but cannot score until `Z_m_min`, source/boundary terms, domain regularity, and a pointwise lift are supplied.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## `Z_m` Sign/Value Audit

{markdown_table(z_m_sign_value_audit, ["audit_id", "target", "derivation_attempt", "current_evidence", "result", "missing_to_close", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

## `Z_m` Acquisition Contract

{markdown_table(z_m_acquisition_contract, ["contract_id", "symbol", "definition", "required_for", "acceptance_condition", "current_status", "first_source_path", "first_source_anchor", "valid_for_claim", "claim_allowed"])}

## `B_grad_sp` Profile-Bound Requirements

{markdown_table(b_grad_requirements, ["requirement_id", "target", "bound_formula", "required_inputs", "status", "effect_if_supplied", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

## Bound Input Update

{markdown_table(bound_input_update, ["update_id", "prior_input", "symbol", "new_status", "supplied_value", "runner_effect", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
