from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1306"
TITLE = "1306-Y5-R10-RAB-Zm-parent-function-or-XB-domain-range"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
PARENT_FUNCTION_SCAN_PATH = OUT_DIR / f"{PACK_ID}_PARENT_FUNCTION_SCAN.csv"
FIELD_REDEFINITION_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_FIELD_REDEFINITION_AUDIT.csv"
XB_DOMAIN_GATE_PATH = OUT_DIR / f"{PACK_ID}_XB_DOMAIN_NORMALIZATION_GATE.csv"
ZM_CLOSURE_TEMPLATE_PATH = OUT_DIR / f"{PACK_ID}_ZM_CLOSURE_INPUT_TEMPLATE_NONCLAIM.csv"
BOUND_INPUT_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_BOUND_INPUT_UPDATE_NONCLAIM.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1306_VALIDATION.csv"


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
        PARENT_FUNCTION_SCAN_PATH,
        FIELD_REDEFINITION_AUDIT_PATH,
        XB_DOMAIN_GATE_PATH,
        ZM_CLOSURE_TEMPLATE_PATH,
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
            "source_id": "SRC1306_0_1305_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1305_NEXT_TARGET.csv",
            "needle": "NEXT1305_0_1306",
            "role": "handoff into parent Z_m function or X_B range hunt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1306_1_1305_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1305_ZM_ACQUISITION_CONTRACT.csv",
            "needle": "ZAC1305_0_Zm_min",
            "role": "Z_m_min/Z_m_bar/X_B/domain/units acquisition contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1306_2_1305_audit",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1305_ZM_SIGN_VALUE_AUDIT.csv",
            "needle": "NO_ZM_SIGN_OR_VALUE_CLAIM_KEEP_ACQUISITION_CONTRACT",
            "role": "prior verdict that sign/value proof did not close",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1306_3_826_coefficients",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_826_COEFFICIENT_LEDGER.csv",
            "needle": "missing_parent_value",
            "role": "Z_m coefficient named but parent value absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1306_4_826_ansatz",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
            "needle": "Z_m(X_B)",
            "role": "symbolic parent action ansatz with unsourced Z_m(X_B)",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1306_5_826_local_cosmo",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_826_LOCAL_COSMO_GATE.csv",
            "needle": "same R/X_B/L_cg coefficients",
            "role": "same local/cosmology coefficient rule is required but missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1306_6_1302_stress",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
            "needle": "MISSING_Z_m_SIGN_AND_VALUE",
            "role": "memory stress residual depends directly on Z_m sign/value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1306_7_1303_inputs",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1303_K_MEM_STRESS_SIGMA_BOUND_INPUT_LEDGER_NONCLAIM.csv",
            "needle": "KMS1303_0_Zm_abs_bound",
            "role": "original stress-bound input requiring Z_m upper bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1306_8_1304_operator_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1304_MEMORY_OPERATOR_OWNER_ATTEMPT.csv",
            "needle": "A_m^{ij}=Z_m h^{ij}",
            "role": "static elliptic map where Z_m becomes the positivity owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1306_9_968_domain",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
            "needle": "MISSING_PARENT_SELECTED_DOMAIN",
            "role": "local domain D is still not parent selected",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1306_10_1042_nohair",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv",
            "needle": "FORMULA_ONLY_NOT_PARENT_SIGNED",
            "role": "positive kinetic premise remains formula-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1306_11_970_action",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
            "needle": "CONDITIONAL_POSITIVITY_OK_INPUTS_UNSIGNED",
            "role": "relative quadratic construction but no parent coefficient law",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    parent_function_scan = [
        {
            "scan_id": "PFS1306_0_symbolic_function",
            "target": "explicit parent function Z_m(X_B)",
            "evidence_found": "Only the symbol Z_m(X_B) is present in the scalar-memory ansatz.",
            "missing_detail": "No equation of the form Z_m(X_B)=..., no invariant argument list, no numerical constant, and no theorem-bound are supplied.",
            "status": "SYMBOL_ONLY_NO_PARENT_FUNCTION",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
            "source_anchor": "AA826_1_memory_sector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "scan_id": "PFS1306_1_coefficient_ledger",
            "target": "source-backed sign/value",
            "evidence_found": "C826_0_Zm names the coefficient and says the acceptance gate is positive/no-ghost plus same local/cosmology value rule.",
            "missing_detail": "The same row marks current_status=missing_parent_value.",
            "status": "LEDGER_EXPLICITLY_MISSING_PARENT_VALUE",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_COEFFICIENT_LEDGER.csv",
            "source_anchor": "C826_0_Zm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "scan_id": "PFS1306_2_local_cosmo_rule",
            "target": "same coefficient across arenas",
            "evidence_found": "The 826 local/cosmology gate requires the same R/X_B/L_cg coefficients to generate local and cosmology behaviour.",
            "missing_detail": "The X_B coefficients and branch-routing projectors remain open, so Z_m cannot be retuned per arena.",
            "status": "SAME_RULE_REQUIRED_NOT_SUPPLIED",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_LOCAL_COSMO_GATE.csv",
            "source_anchor": "LC826_2_cosmology_source;LC826_3_galaxy_firewall",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "scan_id": "PFS1306_3_domain_range",
            "target": "Range_D(X_B) and D_loc",
            "evidence_found": "The 1305 contract names Range_D(X_B) and D_loc as required inputs.",
            "missing_detail": "No parent-selected D_loc, argument list for X_B, local branch map, or compactness/regularity package is supplied.",
            "status": "DOMAIN_AND_RANGE_MISSING",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1305_ZM_ACQUISITION_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
            "source_anchor": "ZAC1305_2_XB_range;ZAC1305_3_D_loc;MOI968_1_domain_D",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "scan_id": "PFS1306_4_stress_dependence",
            "target": "why Z_m cannot be ignored",
            "evidence_found": "The memory Hilbert stress and spatial trace bound contain Z_m multiplying gradient terms.",
            "missing_detail": "Without sign/value/normalization, the stress channel cannot be compared to Kbar/Newton/PPN/R10 budgets.",
            "status": "ZM_IS_ACTIVE_STRESS_COEFFICIENT",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_1303_K_MEM_STRESS_SIGMA_BOUND_INPUT_LEDGER_NONCLAIM.csv",
            "source_anchor": "MSR1302_1_spatial_trace_bound_template;KMS1303_0_Zm_abs_bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "scan_id": "PFS1306_5_verdict",
            "target": "parent Z_m(X_B) source",
            "evidence_found": "No parent function, bound theorem, or domain/range package was found in the selected source chain.",
            "missing_detail": "Z_m must be supplied as a parent coefficient law or demoted to an explicit closure input.",
            "status": "NO_PARENT_FUNCTION_FOUND_DEMOTE_TO_EXPLICIT_CLOSURE",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1305_ZM_SIGN_VALUE_AUDIT.csv",
            "source_anchor": "ZSA1305_4_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    field_redefinition_audit = [
        {
            "audit_id": "FRA1306_0_constant_positive",
            "case": "Z_m=Z_0>0 constant",
            "derivation": "For L_m=-1/2 Z_0 nabla m nabla m - V_R(m;X_B), define m_c=sqrt(Z_0) m. The kinetic term becomes canonical, while V_R, J_m, qbar, and every source/test coupling must be rewritten as functions of m_c/sqrt(Z_0).",
            "result": "CANONICALIZATION_MATH_OK_IF_CONSTANT",
            "claim_limit": "This can set Z_m_min=Z_m_bar=1 only after the parent adopts constant positive Z_m and the transferred potential/source couplings are audited.",
            "hidden_residual_if_misused": "Z_0 can reappear in V_R Hessian, source charge, test charge, alpha numerator, and PPN source normalization.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FRA1306_1_XB_dependent",
            "case": "Z_m=Z_m(X_B(x))",
            "derivation": "A local rescaling by sqrt(Z_m(X_B)) is not a harmless global field redefinition when X_B varies over spacetime or differs between arenas; gradients and metric variations generate additional X_B derivative and response terms.",
            "result": "CANNOT_ABSORB_VARIABLE_ZM_WITHOUT_NEW_RESIDUALS",
            "claim_limit": "A variable Z_m needs explicit X_B argument/range, metric response T_ZX, and same-arena branch law.",
            "hidden_residual_if_misused": "Derivative couplings, X_B metric response, and arena retuning can be hidden by notation.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FRA1306_2_sign_indefinite",
            "case": "Z_m changes sign or reaches zero",
            "derivation": "The static operator A_m^{ij}=Z_m h^{ij} loses uniform ellipticity if Z_m<=0 or inf_D Z_m=0.",
            "result": "LOCAL_NOHAIR_AND_GRADIENT_BOUND_FAIL",
            "claim_limit": "No local-GR, nohair, or bounded stress claim can use this branch.",
            "hidden_residual_if_misused": "Ghost/anti-elliptic or strong-gradient modes can evade the positive-operator identity.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FRA1306_3_verdict",
            "case": "best current closure route",
            "derivation": "The only low-scrutiny temporary route is a constant canonical closure Z_m=1 in declared m_c units, with an explicit transfer audit so no coupling is hidden.",
            "result": "CONSTANT_CANONICAL_CLOSURE_ALLOWED_FOR_PRIVATE_SENSITIVITY_ONLY",
            "claim_limit": "Closure can support smoke tests and algebra bookkeeping, not public claims or local-GR proof.",
            "hidden_residual_if_misused": "The coupling may simply move into V_R/J_m/qbar rather than disappear.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    xb_domain_gate = [
        {
            "gate_id": "XDG1306_0_argument_list",
            "needed_object": "Arg[Z_m]=X_B components",
            "acceptance_test": "every background argument of Z_m is named with units and parent definition",
            "current_status": "MISSING_ARGUMENT_LIST",
            "effect": "cannot compute Z_m_min or Z_m_bar",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "XDG1306_1_local_branch_map",
            "needed_object": "X_B^{local}(x)",
            "acceptance_test": "local branch map or conservative interval over D_loc is source-backed",
            "current_status": "MISSING_LOCAL_BRANCH_RANGE",
            "effect": "cannot evaluate inf/sup on local branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "XDG1306_2_domain",
            "needed_object": "D_loc and coframe",
            "acceptance_test": "compact local exterior, boundary class, and frame/index convention are specified",
            "current_status": "MISSING_PARENT_SELECTED_DOMAIN",
            "effect": "no Sobolev/pointwise constants or boundary flux statements are legal",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "XDG1306_3_units",
            "needed_object": "m and Z_m normalization",
            "acceptance_test": "one Lagrangian normalization is used in stress, alpha, and PPN translations",
            "current_status": "MISSING_UNITS_NORMALIZATION",
            "effect": "Z_m_bar and B_grad units cannot be compared to residual budgets",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "XDG1306_4_arena_rule",
            "needed_object": "same parent coefficient law across local/cosmology/galaxy arenas",
            "acceptance_test": "coefficients are evaluated from the same Z_m(X_B), not fitted independently by arena",
            "current_status": "MISSING_ARENA_MATCHING_RULE",
            "effect": "otherwise this becomes patchwork tuning rather than field theory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    z_m_closure_template = [
        {
            "closure_id": "ZMC1306_A_constant_canonical",
            "closure_type": "temporary_private_canonical_closure",
            "assumption": "Adopt constant positive kinetic normalization and define canonical field units so Z_m=1.",
            "would_supply": "Z_m_min=1;Z_m_bar=1 in canonical m_c units",
            "must_also_supply": "transformed V_R(m_c/sqrt(Z_0));transformed J_m;transformed source/test charges;stress units;same-arena rule",
            "allowed_use": "private algebra/sensitivity branch only",
            "forbidden_use": "local-GR proof;R10/PPN claim;public claim;hiding source/test coupling",
            "current_status": "CLOSURE_TEMPLATE_READY_NOT_ADOPTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "ZMC1306_B_bounded_positive_function",
            "closure_type": "temporary_private_bounded_function_closure",
            "assumption": "Provide an explicit positive interval 0<Z_m_min<=Z_m(X_B)<=Z_m_bar over D_loc.",
            "would_supply": "Z_m_min;Z_m_bar",
            "must_also_supply": "Z_m(X_B) formula or interval source;X_B range;D_loc;units;T_ZX response bound",
            "allowed_use": "private stress-bound runner once all numeric/theorem inputs are filled",
            "forbidden_use": "arena-by-arena retuning or claim rows with MISSING fields",
            "current_status": "CLOSURE_TEMPLATE_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "ZMC1306_C_parent_function",
            "closure_type": "preferred_derivation_route",
            "assumption": "Derive Z_m(X_B) from the parent action or microscopic/coarse-grained theorem.",
            "would_supply": "claim-eligible route to Z_m_min/Z_m_bar after validation",
            "must_also_supply": "sign proof;argument list;local and cosmology branch evaluation;metric response;units",
            "allowed_use": "future claim path only after validation",
            "forbidden_use": "declaring theorem without source path and branch/domain evidence",
            "current_status": "PREFERRED_BUT_NOT_FOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    bound_input_update = [
        {
            "update_id": "BUI1306_0_Zm_min",
            "prior_input": "ZAC1305_0_Zm_min",
            "symbol": "Z_m_min",
            "new_status": "PARENT_FUNCTION_NOT_FOUND_CLOSURE_TEMPLATE_CREATED",
            "supplied_value": "NONE_FOR_CLAIM;OPTIONAL_PRIVATE_CLOSURE_ZMC1306_A_WOULD_SET_1_IF_ADOPTED",
            "runner_effect": "energy route still blocked for claims",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "BUI1306_1_Zm_bar",
            "prior_input": "ZAC1305_1_Zm_bar",
            "symbol": "Z_m_bar",
            "new_status": "PARENT_FUNCTION_NOT_FOUND_CLOSURE_TEMPLATE_CREATED",
            "supplied_value": "NONE_FOR_CLAIM;OPTIONAL_PRIVATE_CLOSURE_ZMC1306_A_WOULD_SET_1_IF_ADOPTED",
            "runner_effect": "K_mem_stress runner still blocked for claims",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "BUI1306_2_XB_range",
            "prior_input": "ZAC1305_2_XB_range",
            "symbol": "Range_D(X_B)",
            "new_status": "MISSING_ARGUMENT_LIST_AND_LOCAL_RANGE",
            "supplied_value": "NONE",
            "runner_effect": "variable Z_m branch cannot be evaluated",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "BUI1306_3_no_score",
            "prior_input": "BUI1305_3_no_score",
            "symbol": "K_mem_stress^Sigma",
            "new_status": "NO_SCORE_NO_LOCAL_GR_CLAIM",
            "supplied_value": "NONE",
            "runner_effect": "1306 creates closure templates only; it does not execute or pass a local residual score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1306_0_parent_function",
            "claim": "Z_m(X_B) is parent-derived",
            "current_status": "BLOCKED_SYMBOL_ONLY",
            "reason": "selected source chain contains symbolic Z_m(X_B) but no explicit function/value/theorem-bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1306_1_canonical_normalization",
            "claim": "Z_m can be set to one without loss",
            "current_status": "BLOCKED_UNLESS_CONSTANT_AND_TRANSFER_AUDITED",
            "reason": "constant positive Z_m can be canonicalized, but source/potential/test couplings inherit the normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1306_2_variable_absorption",
            "claim": "X_B-dependent Z_m can be absorbed away",
            "current_status": "REJECTED_AS_GENERAL_PROOF",
            "reason": "X_B variation creates derivative/metric-response residuals and requires T_ZX bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1306_3_bound_inputs",
            "claim": "Z_m_min/Z_m_bar are supplied",
            "current_status": "BLOCKED_CLOSURE_TEMPLATE_ONLY",
            "reason": "templates exist, but no parent value is claim-valid",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1306_4_local_GR",
            "claim": "local GR/Newton/PPN recovery follows",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "the coupling is now explicit but not derived or scored",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1306_0_parent_function_absent",
            "decision": "do not pretend Z_m(X_B) has been derived",
            "because": "the source chain contains a symbolic coefficient scaffold, not a parent function or bound theorem",
            "next_action": "use explicit nonclaim closure templates only for private sensitivity/algebra",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1306_1_best_low_scrutiny_route",
            "decision": "if a temporary branch is needed, use constant canonical Z_m=1 with transfer audit",
            "because": "constant normalization is mathematically clean; variable X_B-dependent normalization is not safely absorbable",
            "next_action": "audit where the coupling reappears in V_R, J_m, source/test charges, alpha, and PPN normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1306_0_1307",
            "target_file": "1307-Y5-R10-RAB-canonical-Zm-closure-transfer-audit.md",
            "target_script": "scripts/Y5_R10_RAB_canonical_Zm_closure_transfer_audit.py",
            "task": "if the private constant-canonical Z_m closure is adopted for algebra, audit exactly where the normalization moves into V_R, J_m, source/test charges, alpha numerator, and PPN source normalization",
            "success_condition": "either the canonical closure is proven transfer-clean for private smoke tests, or every transferred coupling is retained as an explicit nonclaim residual input",
            "do_not": "do not treat Z_m=1 as derived; do not use it for public/local-GR/R10/PPN claims",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(PARENT_FUNCTION_SCAN_PATH, parent_function_scan)
    write_csv(FIELD_REDEFINITION_AUDIT_PATH, field_redefinition_audit)
    write_csv(XB_DOMAIN_GATE_PATH, xb_domain_gate)
    write_csv(ZM_CLOSURE_TEMPLATE_PATH, z_m_closure_template)
    write_csv(BOUND_INPUT_UPDATE_PATH, bound_input_update)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1306_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1306_1_parent_function_not_found",
            "parent function scan demotes Z_m to explicit closure if no law is found",
            any(
                row["scan_id"] == "PFS1306_5_verdict"
                and row["status"] == "NO_PARENT_FUNCTION_FOUND_DEMOTE_TO_EXPLICIT_CLOSURE"
                for row in parent_function_scan
            ),
            ";".join(str(row["scan_id"]) + "=" + str(row["status"]) for row in parent_function_scan),
        )
    )
    validations.append(
        validation_row(
            "VAL1306_2_field_redefinition_guard",
            "field redefinition audit separates constant canonical closure from variable Z_m absorption",
            any(row["audit_id"] == "FRA1306_0_constant_positive" and row["result"] == "CANONICALIZATION_MATH_OK_IF_CONSTANT" for row in field_redefinition_audit)
            and any(row["audit_id"] == "FRA1306_1_XB_dependent" and row["result"] == "CANNOT_ABSORB_VARIABLE_ZM_WITHOUT_NEW_RESIDUALS" for row in field_redefinition_audit),
            ";".join(str(row["audit_id"]) + "=" + str(row["result"]) for row in field_redefinition_audit),
        )
    )
    gate_statuses = ";".join(str(row["current_status"]) for row in xb_domain_gate)
    validations.append(
        validation_row(
            "VAL1306_3_xb_domain_gates_missing",
            "X_B/domain/units/arena rule gates remain explicit and missing",
            all(str(row["current_status"]).startswith("MISSING") for row in xb_domain_gate),
            gate_statuses,
        )
    )
    validations.append(
        validation_row(
            "VAL1306_4_closure_templates_nonclaim",
            "closure templates exist but are not adopted for claims",
            len(z_m_closure_template) == 3 and all("CLOSURE" in str(row["current_status"]) or "PREFERRED" in str(row["current_status"]) for row in z_m_closure_template),
            ";".join(str(row["closure_id"]) + "=" + str(row["current_status"]) for row in z_m_closure_template),
        )
    )
    validations.append(
        validation_row(
            "VAL1306_5_bound_updates_no_score",
            "bound input updates do not supply claim-valid values or run a score",
            len(bound_input_update) == 4 and all(is_false(row["valid_for_claim"]) for row in bound_input_update),
            ";".join(str(row["update_id"]) + "=" + str(row["new_status"]) for row in bound_input_update),
        )
    )
    validations.append(
        validation_row(
            "VAL1306_6_claim_gates_block",
            "all claim gates remain blocked or rejected",
            len(claim_gates) == 5 and all(str(row["current_status"]).startswith(("BLOCKED", "REJECTED")) for row in claim_gates),
            ";".join(str(row["gate_id"]) + "=" + str(row["current_status"]) for row in claim_gates),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        PARENT_FUNCTION_SCAN_PATH,
        FIELD_REDEFINITION_AUDIT_PATH,
        XB_DOMAIN_GATE_PATH,
        ZM_CLOSURE_TEMPLATE_PATH,
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
    validations.append(validation_row("VAL1306_7_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1306_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1306_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, parent_function_scan, field_redefinition_audit, xb_domain_gate, z_m_closure_template, bound_input_update, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1306_10_next_target_1307",
            "next target routes to canonical Z_m closure transfer audit",
            next_target[0]["next_id"] == "NEXT1306_0_1307" and "canonical-Zm-closure" in str(next_target[0]["target_file"]),
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1306_11_overall",
            "overall 1306 validation",
            overall_pass,
            "1306 finds no parent Z_m(X_B) function, rejects variable absorption as a proof, permits constant canonical Z_m only as private nonclaim closure, and routes to transfer-audit 1307",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1306 Y5 R10 RAB Zm parent function or XB domain range

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** no parent `Z_m(X_B)` function, source-backed `X_B` range, or local domain/units package was found in the selected evidence chain. The coefficient remains real and important, but it is not derived.

**Main progress:** the coupling bottleneck is now split cleanly. A constant positive `Z_m=Z_0` can be canonical-normalized by `m_c=sqrt(Z_0)m`, but only if `V_R`, `J_m`, source/test charges, alpha normalization, and PPN source normalization are transfer-audited. A variable `Z_m(X_B)` cannot be absorbed away without new residuals.

**Decision:** demote `Z_m` to an explicit nonclaim closure template for private algebra/sensitivity only. No local-GR, R10, PPN, no-hair, or public claim is allowed from this closure.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Parent Function Scan

{markdown_table(parent_function_scan, ["scan_id", "target", "evidence_found", "missing_detail", "status", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

## Field Redefinition Audit

{markdown_table(field_redefinition_audit, ["audit_id", "case", "derivation", "result", "claim_limit", "hidden_residual_if_misused", "valid_for_claim", "claim_allowed"])}

## `X_B` Domain and Normalization Gate

{markdown_table(xb_domain_gate, ["gate_id", "needed_object", "acceptance_test", "current_status", "effect", "valid_for_claim", "claim_allowed"])}

## `Z_m` Closure Input Template

{markdown_table(z_m_closure_template, ["closure_id", "closure_type", "assumption", "would_supply", "must_also_supply", "allowed_use", "forbidden_use", "current_status", "valid_for_claim", "claim_allowed"])}

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
