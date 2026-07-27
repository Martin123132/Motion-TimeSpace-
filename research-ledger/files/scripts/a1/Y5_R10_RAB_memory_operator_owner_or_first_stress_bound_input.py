from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1304"
TITLE = "1304-Y5-R10-RAB-memory-operator-owner-or-first-stress-bound-input"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
OPERATOR_OWNER_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_MEMORY_OPERATOR_OWNER_ATTEMPT.csv"
POSITIVE_GAP_MAP_PATH = OUT_DIR / f"{PACK_ID}_ZM_POSITIVE_GAP_MAP_NONCLAIM.csv"
FIRST_BOUND_INPUT_PATH = OUT_DIR / f"{PACK_ID}_FIRST_STRESS_BOUND_INPUT_ROWS_NONCLAIM.csv"
GRADIENT_BOUND_ROUTE_PATH = OUT_DIR / f"{PACK_ID}_GRADIENT_BOUND_ROUTE_NONCLAIM.csv"
RUNNER_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_INPUT_UPDATE_NONCLAIM.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1304_VALIDATION.csv"


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
        OPERATOR_OWNER_ATTEMPT_PATH,
        POSITIVE_GAP_MAP_PATH,
        FIRST_BOUND_INPUT_PATH,
        GRADIENT_BOUND_ROUTE_PATH,
        RUNNER_UPDATE_PATH,
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
            "source_id": "SRC1304_0_1303_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1303_NEXT_TARGET.csv",
            "needle": "NEXT1303_0_1304",
            "role": "handoff into memory operator owner or first bound input",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1304_1_1303_bound_inputs",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1303_K_MEM_STRESS_SIGMA_BOUND_INPUT_LEDGER_NONCLAIM.csv",
            "needle": "KMS1303_0_Zm_abs_bound",
            "role": "first missing stress-bound input rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1304_2_1303_runner_schema",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1303_K_MEM_STRESS_BOUND_RUNNER_SCHEMA_NONCLAIM.csv",
            "needle": "KMRUN1303_0_bound_formula",
            "role": "bound formula that consumes Z_m_bar and B_grad_sp",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1304_3_826_ansatz",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
            "needle": "L_m = -1/2 Z_m(X_B) nabla_mu m nabla^mu m - V_R(m;X_B)",
            "role": "candidate scalar-memory action form",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1304_4_826_coefficients",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_826_COEFFICIENT_LEDGER.csv",
            "needle": "C826_0_Zm",
            "role": "Z_m coefficient explicitly named but missing parent value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1304_5_967_positive_operator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
            "needle": "RELATIVE_LEMMA_READY_PARENT_INPUTS_UNSIGNED",
            "role": "positive-operator gradient/nohair theorem shape",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1304_6_968_input_audit",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
            "needle": "MISSING_SIGN_CERTIFICATE",
            "role": "operator owner, sign, gap, source, boundary, projection inputs remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1304_7_970_variation",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
            "needle": "RELATIVE_VARIATION_OK",
            "role": "relative action variation gives operator equation shape",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1304_8_1042_premise_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv",
            "needle": "FAIL_CURRENT_CLAIM_NOHAIR_NOT_PARENT_SIGNED",
            "role": "nohair premise gate remains failed for claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    operator_owner_attempt = [
        {
            "attempt_id": "OO1304_0_action_form",
            "target": "memory operator owner",
            "derived_or_sourced": "candidate action form L_m=-1/2 Z_m(X_B) nabla m nabla m - V_R(m;X_B) is present",
            "operator_implication": "Euler equation has schematic owner shape div(Z_m nabla m)-partial_m V_R = J_m plus source/bath/boundary terms",
            "status": "FORM_ADVANCES_OPERATOR_TARGET_NOT_PARENT_SIGNED",
            "missing_to_promote": "MISSING_PARENT_ADOPTION;MISSING_FIELD_DOMAIN;MISSING_SOURCE_BATH_TERMS;MISSING_BOUNDARY_CLASS",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv;source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
            "source_anchor": "AA826_1_memory_sector;QMA970_1_variation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OO1304_1_static_local_operator_map",
            "target": "positive local operator map",
            "derived_or_sourced": "in a static local branch the scalar-memory form maps to L_m,loc delta m = -nabla_i(Z_m h^{ij} nabla_j delta m)+M_m^2 delta m plus sources",
            "operator_implication": "A_m^{ij}=Z_m h^{ij}; M_m^2=partial_m^2 V_R evaluated at the local branch, modulo X_B/source/bath corrections",
            "status": "RELATIVE_OPERATOR_MAP_WRITTEN",
            "missing_to_promote": "MISSING_Z_m_SIGN;MISSING_M_m2_HESSIAN;MISSING_LOCAL_BRANCH;MISSING_X_B_CORRECTIONS",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv;source-intake/mts_residuals/P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
            "source_anchor": "AA826_1_memory_sector;MPO967_1_operator",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OO1304_2_owner_verdict",
            "target": "claim-grade memory operator owner",
            "derived_or_sourced": "current corpus supplies a scaffold and relative variation, not a signed parent sector",
            "operator_implication": "operator-owner premise advances in form only; no nohair/local-GR claim follows",
            "status": "NOT_PARENT_SIGNED_KEEP_NONCLAIM",
            "missing_to_promote": "MISSING_PARENT_MEMORY_SECTOR_SIGNATURE;MISSING_NOHIDDEN_READOUT;MISSING_BOUNDARY_SOURCE_CLOSURE",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv",
            "source_anchor": "MOI968_8_verdict;NHP1042_6_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    positive_gap_map = [
        {
            "map_id": "ZPG1304_0_Zm_positive",
            "premise": "Z_m(X_B) is positive in the local branch",
            "candidate_map": "A_m^{ij}=Z_m h^{ij}; positive ellipticity requires Z_m >= Z_m_min > 0",
            "source_status": "SOURCE_NAMES_COEFFICIENT_VALUE_MISSING",
            "needed_value_or_theorem": "Z_m_min and Z_m_bar from parent coefficient law or positivity theorem",
            "current_status": "NONCLAIM_MAP_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "ZPG1304_1_Zm_abs_bound",
            "premise": "finite upper bound on |Z_m| for stress envelope",
            "candidate_map": "Z_m_bar := sup_D |Z_m(X_B)|",
            "source_status": "C826_0_Zm_NAMES_SYMBOL_BUT_VALUE_MISSING",
            "needed_value_or_theorem": "source-backed upper bound or compact-domain continuity plus X_B range",
            "current_status": "FIRST_BOUND_INPUT_ROW_READY_VALUE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "ZPG1304_2_mass_gap",
            "premise": "local Hessian/gap removes zero modes",
            "candidate_map": "M_m^2 := partial_m^2 V_R(m_*;X_B) and lambda_eff >= M_m^2 + lambda_1(D) > 0",
            "source_status": "R_POTENTIAL_AND_mL_NAMED_BUT_FUNCTIONAL_FORM_MISSING",
            "needed_value_or_theorem": "V_R functional form, stable local extremum, boundary/zero-mode removal",
            "current_status": "GAP_MAP_ONLY_VALUE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "ZPG1304_3_gradient_energy_route",
            "premise": "energy identity bounds gradients rather than proving zero",
            "candidate_map": "if Z_m>=Z_m_min>0 then int_D |grad m|^2 <= Z_m_min^-1 (int_D m J_m + boundary - M_m^2 int_D m^2)",
            "source_status": "RELATIVE_IDENTITY_ONLY",
            "needed_value_or_theorem": "J_m norm, boundary flux bound, Z_m_min, M_m^2, domain norm conversion to pointwise B_grad_sp",
            "current_status": "B_GRAD_ROUTE_WRITTEN_NOT_EXECUTABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    first_bound_inputs = [
        {
            "input_id": "KMS1304_0_Zm_bar_first_row",
            "fills_prior_input": "KMS1303_0_Zm_abs_bound",
            "symbol": "Z_m_bar",
            "definition": "Z_m_bar := sup_{x in D_loc} |Z_m(X_B(x))| for the same local domain and branch used by K_mem_stress^Sigma",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_COEFFICIENT_LEDGER.csv;source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
            "source_anchor": "C826_0_Zm;AA826_1_memory_sector",
            "supplied_value": "MISSING_PARENT_VALUE_OR_BOUND",
            "units": "parent_L_m_normalization_required",
            "remaining_missing": "MISSING_Z_m_FUNCTION;MISSING_X_B_RANGE;MISSING_DOMAIN_D_LOC;MISSING_UNITS_NORMALIZATION",
            "current_status": "SOURCE_BACKED_SYMBOL_ROW_VALUE_MISSING_NONCLAIM",
            "usable_for_scoring": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "KMS1304_1_B_grad_sp_first_row",
            "fills_prior_input": "KMS1303_1_spatial_gradient_bound",
            "symbol": "B_grad_sp",
            "definition": "B_grad_sp >= sup_{x in D_loc} sum_i |nabla^i m nabla^i m| in the Kbar local coframe",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv;source-intake/mts_residuals/P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
            "source_anchor": "MPO967_4_energy_identity;MOI968_8_verdict",
            "supplied_value": "MISSING_PROFILE_OR_ENERGY_TO_POINTWISE_BOUND",
            "units": "m_units^2/length^2_after_frame_lock",
            "remaining_missing": "MISSING_Z_m_min;MISSING_J_m_NORM;MISSING_BOUNDARY_FLUX_BOUND;MISSING_DOMAIN_REGULARITY;MISSING_SOBOLEV_OR_POINTWISE_CONSTANT;MISSING_FRAME_LOCK",
            "current_status": "SOURCE_BACKED_BOUND_ROUTE_ROW_VALUE_MISSING_NONCLAIM",
            "usable_for_scoring": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    gradient_bound_route = [
        {
            "route_id": "GBR1304_0_energy_to_L2_gradient",
            "input_target": "B_grad_sp",
            "route_formula": "G2_m := int_D sum_i |nabla^i m nabla^i m| <= Z_m_min^-1 (|int_D m J_m| + |Phi_boundary| + retained nonpositive/zero-mode terms)",
            "required_inputs": "Z_m_min;J_m_norm;boundary_flux_bound;domain_measure;zero_mode_rule",
            "status": "ROUTE_WRITTEN_NOT_EXECUTABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "GBR1304_1_L2_to_pointwise",
            "input_target": "B_grad_sp",
            "route_formula": "B_grad_sp <= C_reg(D,L_m) * G2_m or direct profile bound, if elliptic regularity/domain smoothness is supplied",
            "required_inputs": "regularity_constant;domain_geometry;operator_coefficients;source_norm_class",
            "status": "POINTWISE_LIFT_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "GBR1304_2_nohair_shortcut",
            "input_target": "B_grad_sp",
            "route_formula": "B_grad_sp=0 if operator owner, positive gap, source silence, boundary zero, and zero-mode removal all pass",
            "required_inputs": "full nohair premise gate",
            "status": "ZERO_SHORTCUT_BLOCKED_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_update = [
        {
            "update_id": "RUN1304_0_Zm_bar_named",
            "prior_input": "KMS1303_0_Zm_abs_bound",
            "new_row": "KMS1304_0_Zm_bar_first_row",
            "update": "symbol is source-backed to C826_0_Zm but value/theorem remains missing",
            "runner_effect": "still no execution",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "RUN1304_1_B_grad_sp_route_named",
            "prior_input": "KMS1303_1_spatial_gradient_bound",
            "new_row": "KMS1304_1_B_grad_sp_first_row",
            "update": "gradient bound has energy/nohair route, but profile/pointwise value remains missing",
            "runner_effect": "still no execution",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "RUN1304_2_operator_premise_advanced",
            "prior_input": "NHM1302_0_operator_owner",
            "new_row": "OO1304_1_static_local_operator_map",
            "update": "operator form maps to A_m^{ij}=Z_m h^{ij}, M_m^2=partial_m^2 V_R",
            "runner_effect": "premise sharpened but not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1304_0_operator_owner",
            "claim": "memory operator owner is parent-signed",
            "current_status": "BLOCKED_FORM_ONLY",
            "reason": "action scaffold and relative variation exist, but parent adoption/domain/source/boundary signatures are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1304_1_positive_gap",
            "claim": "Z_m positivity/gap is established",
            "current_status": "BLOCKED_VALUE_AND_SIGN_MISSING",
            "reason": "Z_m and V_R Hessian are named but not source-valued or theorem-bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1304_2_first_bound_inputs",
            "claim": "first K_mem_stress bound inputs are source-backed rows",
            "current_status": "SATISFIED_FOR_NONCLAIM_ROWS",
            "reason": "KMS1304_0 and KMS1304_1 cite existing source rows and expose missing values/theorems",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1304_3_bound_score",
            "claim": "K_mem_stress^Sigma bound is scoreable",
            "current_status": "BLOCKED_VALUES_MISSING",
            "reason": "Z_m_bar and B_grad_sp are still missing values, units, domain, and frame lock",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1304_4_local_GR",
            "claim": "local GR/Newton/PPN recovery pass",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "memory stress bound inputs are sharpened but not scored, and other Kbar channels remain unresolved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1304_0_operator_form_progress",
            "decision": "record the scalar-memory operator form as a nonclaim advancement",
            "because": "the 826 action scaffold plus 970 variation identifies Z_m and V_R Hessian as the exact positivity/gap owners",
            "next_action": "try to source or derive Z_m_min/Z_m_bar and the gradient/profile bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1304_1_first_bound_rows",
            "decision": "stage Z_m_bar and B_grad_sp as first concrete nonclaim bound rows",
            "because": "they are the first multiplicative factors in the 1303 K_mem_stress runner schema",
            "next_action": "attack Z_m value/sign first, then B_grad_sp via nohair or energy-to-pointwise route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1304_0_1305",
            "target_file": "1305-Y5-R10-RAB-Zm-sign-value-or-gradient-profile-bound.md",
            "target_script": "scripts/Y5_R10_RAB_Zm_sign_value_or_gradient_profile_bound.py",
            "task": "try to derive/source Z_m positivity and an upper bound Z_m_bar; if unavailable, derive the gradient profile/energy-to-pointwise bound requirements for B_grad_sp",
            "success_condition": "Z_m_bar or B_grad_sp receives a real sourced/theorem value, or the exact missing parent coefficient/domain inputs are locked for acquisition",
            "do_not": "do not run the K_mem_stress score or claim nohair/local-GR from schema-only rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(OPERATOR_OWNER_ATTEMPT_PATH, operator_owner_attempt)
    write_csv(POSITIVE_GAP_MAP_PATH, positive_gap_map)
    write_csv(FIRST_BOUND_INPUT_PATH, first_bound_inputs)
    write_csv(GRADIENT_BOUND_ROUTE_PATH, gradient_bound_route)
    write_csv(RUNNER_UPDATE_PATH, runner_update)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1304_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1304_1_operator_form_advanced",
            "operator-owner premise advances in form but not claim",
            any(row["attempt_id"] == "OO1304_1_static_local_operator_map" and row["status"] == "RELATIVE_OPERATOR_MAP_WRITTEN" for row in operator_owner_attempt)
            and not any("PARENT_SIGNED" == row["status"] for row in operator_owner_attempt),
            ";".join(str(row["attempt_id"]) + "=" + str(row["status"]) for row in operator_owner_attempt),
        )
    )
    validations.append(
        validation_row(
            "VAL1304_2_first_bound_rows_written",
            "Z_m_bar and B_grad_sp first bound rows exist and remain value-missing",
            len(first_bound_inputs) == 2 and all("MISSING" in str(row["supplied_value"]) for row in first_bound_inputs),
            ";".join(str(row["input_id"]) + "=" + str(row["supplied_value"]) for row in first_bound_inputs),
        )
    )
    validations.append(
        validation_row(
            "VAL1304_3_positive_gap_values_missing",
            "positive/gap map does not claim values",
            len(positive_gap_map) == 4
            and all(str(row["current_status"]) in {"NONCLAIM_MAP_ONLY", "FIRST_BOUND_INPUT_ROW_READY_VALUE_MISSING", "GAP_MAP_ONLY_VALUE_MISSING", "B_GRAD_ROUTE_WRITTEN_NOT_EXECUTABLE"} for row in positive_gap_map),
            ";".join(str(row["map_id"]) + "=" + str(row["current_status"]) for row in positive_gap_map),
        )
    )
    validations.append(
        validation_row(
            "VAL1304_4_runner_update_no_execution",
            "runner update remains non-executable/no-score",
            len(runner_update) == 3 and all("still no execution" in str(row["runner_effect"]) or "not parent-signed" in str(row["runner_effect"]) for row in runner_update),
            ";".join(str(row["update_id"]) + "=" + str(row["runner_effect"]) for row in runner_update),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        OPERATOR_OWNER_ATTEMPT_PATH,
        POSITIVE_GAP_MAP_PATH,
        FIRST_BOUND_INPUT_PATH,
        GRADIENT_BOUND_ROUTE_PATH,
        RUNNER_UPDATE_PATH,
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
    validations.append(validation_row("VAL1304_5_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1304_6_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1304_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, operator_owner_attempt, positive_gap_map, first_bound_inputs, gradient_bound_route, runner_update, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1304_8_next_target_1305",
            "next target routes to Z_m sign/value or gradient profile bound",
            next_target[0]["next_id"] == "NEXT1304_0_1305" and "Zm-sign-value" in str(next_target[0]["target_file"]),
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1304_9_overall",
            "overall 1304 validation",
            overall_pass,
            "1304 sharpens the memory operator form, maps Z_m positivity/gap owners, writes first Z_m_bar and B_grad_sp bound rows, keeps scoring blocked, and routes to Z_m sign/value or gradient profile",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1304 Y5 R10 RAB memory operator owner or first stress-bound input

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1304 advances the operator-owner route in form, not in claim. The scalar-memory ansatz identifies the local operator map `A_m^{{ij}}=Z_m h^{{ij}}` and `M_m^2=partial_m^2 V_R`, but the parent action still does not supply signed `Z_m`, a Hessian/gap, source silence, boundary data, or domain/frame normalization.

**Main progress:** the first two stress-bound inputs are now concrete nonclaim rows: `Z_m_bar := sup_D |Z_m(X_B)|` and `B_grad_sp >= sup_D sum_i |nabla^i m nabla^i m|`. They are source-backed to existing corpus rows but remain value-missing.

**Still blocked:** `K_mem_stress^Sigma` is not scoreable. No no-hair, Newton, PPN, R10, or local-GR claim is allowed.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Memory Operator Owner Attempt

{markdown_table(operator_owner_attempt, ["attempt_id", "target", "derived_or_sourced", "operator_implication", "status", "missing_to_promote", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

## `Z_m` Positive-Gap Map

{markdown_table(positive_gap_map, ["map_id", "premise", "candidate_map", "source_status", "needed_value_or_theorem", "current_status", "valid_for_claim", "claim_allowed"])}

## First Stress-Bound Input Rows

{markdown_table(first_bound_inputs, ["input_id", "fills_prior_input", "symbol", "definition", "source_path", "source_anchor", "supplied_value", "units", "remaining_missing", "current_status", "usable_for_scoring", "valid_for_claim", "claim_allowed"])}

## Gradient Bound Route

{markdown_table(gradient_bound_route, ["route_id", "input_target", "route_formula", "required_inputs", "status", "valid_for_claim", "claim_allowed"])}

## Runner Input Update

{markdown_table(runner_update, ["update_id", "prior_input", "new_row", "update", "runner_effect", "valid_for_claim", "claim_allowed"])}

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
