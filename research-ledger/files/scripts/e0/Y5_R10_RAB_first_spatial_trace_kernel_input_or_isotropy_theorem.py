from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1300"
TITLE = "1300-Y5-R10-RAB-first-spatial-trace-kernel-input-or-isotropy-theorem"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
FIRST_TRACE_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_FIRST_TRACE_INPUT_AUDIT.csv"
SUM_MM_INPUT_PATH = OUT_DIR / f"{PACK_ID}_SUM_i_M_m_ii_INPUT_ROW_NONCLAIM.csv"
ISOTROPY_THEOREM_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_ISOTROPY_TRACEFREE_THEOREM_AUDIT.csv"
KBAR_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_KBAR_UPDATE_PREVIEW_NONCLAIM.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1300_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    candidate_path = Path(relative_path)
    if candidate_path.is_absolute():
        return candidate_path
    return ROOT / candidate_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for entry in rows:
            for key in entry:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for entry in rows:
            writer.writerow({field: entry.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = ["| " + " | ".join(md_escape(entry.get(field, "")) for field in fields) + " |" for entry in rows]
    return "\n".join([header, divider, *body])


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
        is_false(entry.get("valid_for_claim", False)) and is_false(entry.get("claim_allowed", False))
        for rows in tables
        for entry in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        FIRST_TRACE_AUDIT_PATH,
        SUM_MM_INPUT_PATH,
        ISOTROPY_THEOREM_AUDIT_PATH,
        KBAR_UPDATE_PATH,
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
            "source_id": "SRC1300_0_1299_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1299_NEXT_TARGET.csv",
            "needle": "NEXT1299_0_1300",
            "role": "handoff into first spatial trace input/theorem gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1300_1_1299_spatial_trace_kernel",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1299_SPATIAL_TRACE_KERNEL_ROWS_NONCLAIM.csv",
            "needle": "MISSING_SUM_i_M_m_ii_BOUND",
            "role": "explicit first missing spatial trace kernel input",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1300_2_1298_trace_requirement",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1298_SPATIAL_TRACE_REQUIREMENTS.csv",
            "needle": "STR1298_0_m_spatial_trace",
            "role": "prior proof that Kbar_00 needs the m spatial trace",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1300_3_1289_derivative_chain",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "needle": "M_m^{00}:=metric response kernel for m",
            "role": "available 00 metric-response kernel definition to generalize only as a schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1300_4_1286_scalar_projection",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1286_FIRST_RESPONSE_FIELD_COMPONENT_ROW_NONCLAIM.csv",
            "needle": "Gamma_eff = L_cg^-2 F(m)",
            "role": "source-backed scalar projection whose m variation creates the m-kernel term",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1300_5_1299_trace_theorem_audit",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1299_TRACE_THEOREM_AUDIT.csv",
            "needle": "FAIL_CURRENT_CORPUS_KEEP_SPATIAL_TRACE_ROWS",
            "role": "current-corpus rejection of trace/isotropy shortcut",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1300_6_no_anisotropy_attempt",
            "local_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
            "needle": "T3_no_anisotropic_selector_stress",
            "role": "conditional no-anisotropy route cannot yet promote isotropy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1300_7_boundary_scalar_attempt",
            "local_path": "source-intake/mts_residuals/P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv",
            "needle": "O2_scalar_not_enough_warning",
            "role": "warning that scalar-looking boundary terms do not by themselves prove metric trace silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for entry in source_register:
        exists, needle_found = exists_and_contains(str(entry["local_path"]), str(entry["needle"]))
        entry["exists"] = exists
        entry["needle_found"] = needle_found

    first_trace_audit = [
        {
            "audit_id": "FTI1300_0_abs_spatial_m_kernel_sum",
            "target_input": "sum_i |M_m^{ii}|",
            "what_is_known": "1299 identifies this as the first required m-chain spatial trace input.",
            "candidate_formula": "M_m^Sigma_abs := sum_i |M_m^{ii}|",
            "status": "SCHEMA_DEFINED_VALUE_MISSING",
            "missing_to_score": "MISSING_NUMERIC_OR_THEOREM_BOUND_FOR_SUM_i_M_m_ii;MISSING_PARENT_METRIC_RESPONSE_COMPONENTS",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1299_SPATIAL_TRACE_KERNEL_ROWS_NONCLAIM.csv",
            "source_anchor": "STK1299_0_m_spatial_trace",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FTI1300_1_signed_spatial_m_trace",
            "target_input": "sum_i M_m^{ii}",
            "what_is_known": "The signed trace would be sharper, but current rows only justify an absolute-value nonclaim template.",
            "candidate_formula": "M_m^tr := M_m^{11}+M_m^{22}+M_m^{33}",
            "status": "SIGNED_TRACE_RELATION_NOT_DERIVED",
            "missing_to_score": "MISSING_SIGNED_PARENT_TRACE_THEOREM;MISSING_INDEX_CONVENTION_LOCK",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1298_SPATIAL_TRACE_REQUIREMENTS.csv",
            "source_anchor": "STR1298_0_m_spatial_trace",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FTI1300_2_parent_variation_owner",
            "target_input": "M_m^{ii}",
            "what_is_known": "1289 defines M_m^{00} as a metric response kernel for m, but does not supply spatial components.",
            "candidate_formula": "M_m^{mu nu} := delta m / delta g_{mu nu} or the parent-owned equivalent in the local frame",
            "status": "PARENT_METRIC_RESPONSE_COMPONENTS_MISSING",
            "missing_to_score": "MISSING_PARENT_DEFINITION_OF_m_AS_METRIC_FUNCTIONAL;MISSING_LOCAL_FRAME_VARIATION_RULE",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "source_anchor": "KDR1289_0_Gamma_m_L_chain_kernel_00",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FTI1300_3_units_and_domain",
            "target_input": "units/domain for M_m^Sigma_abs",
            "what_is_known": "1289 says the term has Gamma_eff units only if response kernels are dimensionless.",
            "candidate_formula": "units(M_m^Sigma_abs)=dimensionless only after parent normalization proves it",
            "status": "UNITS_AND_DOMAIN_LEDGER_MISSING",
            "missing_to_score": "MISSING_UNITS_LEDGER;MISSING_LOCAL_DOMAIN_PROFILE;MISSING_PROJECTOR_DOMAIN_LOCK",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1286_FIRST_RESPONSE_FIELD_COMPONENT_ROW_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "source_anchor": "RFR1286_0_Gamma_memory_scalar_projection;KDR1289_0_Gamma_m_L_chain_kernel_00",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    sum_m_input_rows = [
        {
            "input_id": "MMT1300_0_sum_abs_Mm_ii_schema",
            "target_kernel": "STK1299_0_m_spatial_trace",
            "input_symbol": "M_m^Sigma_abs",
            "definition": "M_m^Sigma_abs := sum_i |M_m^{ii}| in the locked local frame",
            "bound_form": "|R_m^Sigma| <= |C_sign| L_cg^-2 |F_prime(m)| M_m^Sigma_abs",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1299_SPATIAL_TRACE_KERNEL_ROWS_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "source_anchor": "STK1299_0_m_spatial_trace;KDR1289_0_Gamma_m_L_chain_kernel_00",
            "supplied_value": "MISSING_NUMERIC_OR_THEOREM_BOUND",
            "supplied_units": "dimensionless_if_M_m_dimensionless_else_missing",
            "remaining_missing": "MISSING_SUM_i_M_m_ii_NUMERIC_OR_THEOREM_BOUND;MISSING_PARENT_METRIC_RESPONSE_COMPONENTS;MISSING_UNITS_LEDGER;MISSING_DOMAIN_FRAME_LOCK",
            "current_status": "SOURCE_BACKED_SCHEMA_ROW_VALUE_MISSING_NONCLAIM",
            "usable_for_scoring": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "next_action": "derive M_m^{ij} from the parent m[g,fields] variation or source a parent theorem bounding its local spatial trace",
        },
        {
            "input_id": "MMT1300_1_conditional_isotropic_parameterization",
            "target_kernel": "STK1299_0_m_spatial_trace",
            "input_symbol": "mu_m_iso",
            "definition": "If a parent theorem proves M_m^{ij}=mu_m_iso delta^{ij}, then M_m^Sigma_abs <= 3 |mu_m_iso|.",
            "bound_form": "|R_m^Sigma| <= 3 |C_sign| L_cg^-2 |F_prime(m)| |mu_m_iso|",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1299_TRACE_THEOREM_AUDIT.csv;source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
            "source_anchor": "TTA1299_1_isotropic_pressure_shortcut;T3_no_anisotropic_selector_stress",
            "supplied_value": "MISSING_PARENT_ISOTROPY_THEOREM_AND_mu_m_iso_VALUE",
            "supplied_units": "same_as_M_m_kernel_after_parent_normalization",
            "remaining_missing": "MISSING_PARENT_ISOTROPY_THEOREM;MISSING_mu_m_iso_BOUND;MISSING_RELATION_TO_M_m_00",
            "current_status": "CONDITIONAL_PARAMETERIZATION_NOT_SCOREABLE",
            "usable_for_scoring": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "next_action": "prove isotropy from parent local symmetry and boundary/domain silence, or discard this parameterization",
        },
    ]

    isotropy_theorem_audit = [
        {
            "theorem_id": "ISO1300_0_tracefree_m_kernel",
            "candidate_theorem": "M_m metric response is trace-free in the local flat frame",
            "would_supply": "a signed relation between M_m^{00} and sum_i M_m^{ii}",
            "audit_result": "NOT_DERIVED",
            "reason": "1299 rejected the tracefree shortcut and no parent variation row fixes the spatial components.",
            "missing_to_promote": "MISSING_TRACEFREE_PARENT_THEOREM;MISSING_INDEX_CONVENTION_LOCK;MISSING_PROJECTOR_DOMAIN_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "ISO1300_1_isotropic_m_kernel",
            "candidate_theorem": "local m response is isotropic, M_m^{ij}=mu_m delta^{ij}",
            "would_supply": "sum_i |M_m^{ii}| <= 3 |mu_m|",
            "audit_result": "CONDITIONAL_NOT_ENOUGH",
            "reason": "isotropy still leaves mu_m unbounded and unrelated to the known 00 template.",
            "missing_to_promote": "MISSING_PARENT_ISOTROPY_THEOREM;MISSING_mu_m_VALUE_OR_BOUND;MISSING_STRESS_RELATION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "ISO1300_2_metric_invisible_m_kernel",
            "candidate_theorem": "m is locally metric-invisible after quotient/projector descent",
            "would_supply": "M_m^{ii}=0 and R_m^Sigma=0",
            "audit_result": "BLOCKED_NOT_PARENT_DERIVED",
            "reason": "topological/projector silence remains conditional in the inherited ledgers.",
            "missing_to_promote": "MISSING_METRIC_INVISIBILITY_PARENT_CLAUSE;MISSING_NO_FLUX_THEOREM;MISSING_BOUNDARY_SILENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "ISO1300_3_scalar_domain_no_STF_route",
            "candidate_theorem": "no local vector/tensor selector exists, so the m response has no anisotropic STF part",
            "would_supply": "a route toward isotropic parameterization, not a numerical bound by itself",
            "audit_result": "NOT_PROMOTED",
            "reason": "the no-anisotropy rows are conditional and do not give a parent-owned response-kernel amplitude.",
            "missing_to_promote": "MISSING_DOMAIN_SELECTOR_PROOF;MISSING_RESPONSE_KERNEL_AMPLITUDE;MISSING_BOUNDARY_SCALAR_OWNER",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "ISO1300_4_current_verdict",
            "candidate_theorem": "current corpus replaces M_m^Sigma_abs by an earned theorem",
            "would_supply": "removal of MISSING_SUM_i_M_m_ii_BOUND from STK1299_0",
            "audit_result": "FAIL_CURRENT_CORPUS_KEEP_INPUT_ROW_NONCLAIM",
            "reason": "1300 can define the missing input cleanly, but cannot yet fill its value or theorem replacement.",
            "missing_to_promote": "derive parent m metric-response components or prove a trace/isotropy/metric-invisibility theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    kbar_update = [
        {
            "update_id": "KBU1300_0_STK1299_0_m_trace_input",
            "target_row": "STK1299_0_m_spatial_trace",
            "old_missing": "MISSING_SUM_i_M_m_ii_BOUND",
            "new_named_input": "M_m^Sigma_abs",
            "new_status": "INPUT_SCHEMA_DEFINED_VALUE_MISSING",
            "effect_on_bound": "|R_m^Sigma| <= |C_sign| L_cg^-2 |F_prime(m)| M_m^Sigma_abs",
            "effect_on_scoring": "NO_SCORE_STILL_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "KBU1300_1_total_Kbar_bound",
            "target_row": "KBA1299_0_total_Kbar_abs_bound",
            "old_missing": "MISSING_NUMERIC_OR_THEOREM_INPUTS_FOR_ALL_SPATIAL_TRACE_ROWS",
            "new_named_input": "M_m^Sigma_abs is now named but not valued",
            "new_status": "ASSEMBLY_SHARPENED_NOT_SCOREABLE",
            "effect_on_bound": "|Kbar_L,loc,00| still contains unvalued R_m^Sigma, R_L^Sigma, R_cdb^Sigma, and projector-boundary terms",
            "effect_on_scoring": "NO_SCORE_NO_NEWTON_PPN_R10_SCORE_ALLOWED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "KBU1300_2_00_only_guard",
            "target_row": "all local response runners",
            "old_missing": "00-only rows tempted a premature Newton budget",
            "new_named_input": "explicit spatial trace requirement retained",
            "new_status": "SAFETY_GUARD_REINFORCED",
            "effect_on_bound": "00-only bounds remain insufficient for Kbar_00",
            "effect_on_scoring": "PREVENTS_FALSE_LOCAL_GR_PASS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1300_0_sources",
            "claim": "1300 cited local sources exist",
            "current_status": "PASS_FOR_AUDIT_ONLY",
            "reason": "source register checks path and anchor existence, not physics truth",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1300_1_first_trace_input_named",
            "claim": "first m spatial trace input is explicitly named",
            "current_status": "SATISFIED_FOR_NONCLAIM_SCHEMA",
            "reason": "M_m^Sigma_abs row records the exact missing object needed by STK1299_0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1300_2_first_trace_value",
            "claim": "first m spatial trace input is valued or theorem-bounded",
            "current_status": "BLOCKED_VALUE_MISSING",
            "reason": "no numeric bound, response-kernel component derivation, or parent theorem is present",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1300_3_isotropy_tracefree_theorem",
            "claim": "isotropy/tracefree/metric-invisibility theorem replaces spatial trace input",
            "current_status": "BLOCKED_NOT_DERIVED",
            "reason": "candidate theorem routes are conditional, amplitude-free, or parent-unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1300_4_local_GR",
            "claim": "local GR/Newton/PPN recovery pass",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "Kbar_00 still lacks the first spatial trace value and later Lcg/CDB/projector trace inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1300_0_no_theorem_promotion",
            "decision": "do not promote tracefree, isotropic, or metric-invisible shortcut",
            "because": "no parent-owned theorem currently supplies the missing m spatial trace amplitude or relation",
            "next_action": "derive actual parent metric-response components for m, starting with M_m^{ij}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1300_1_keep_input_schema",
            "decision": "retain M_m^Sigma_abs as the exact first missing input",
            "because": "it prevents the project from smuggling a 00-only local Newton budget through trace reversal",
            "next_action": "try to compute or bound M_m^Sigma_abs from m[g,fields], local symmetry, and boundary/domain clauses",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1300_0_1301",
            "target_file": "1301-Y5-R10-RAB-parent-metric-response-components-for-m-spatial-trace.md",
            "target_script": "scripts/Y5_R10_RAB_parent_metric_response_components_for_m_spatial_trace.py",
            "task": "derive or reject the parent metric-response components M_m^{ij}; if derivation fails, write the exact closure contract needed to bound M_m^Sigma_abs",
            "success_condition": "M_m^Sigma_abs receives a real value/theorem bound or a hard parent-action closure contract with no hidden local-GR claim",
            "do_not": "do not use isotropy, tracefree, or 00-only substitutions without parent-signed proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(FIRST_TRACE_AUDIT_PATH, first_trace_audit)
    write_csv(SUM_MM_INPUT_PATH, sum_m_input_rows)
    write_csv(ISOTROPY_THEOREM_AUDIT_PATH, isotropy_theorem_audit)
    write_csv(KBAR_UPDATE_PATH, kbar_update)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for entry in source_register if entry["exists"] and entry["needle_found"])
    validations.append(
        validation_row(
            "VAL1300_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1300_1_first_trace_schema",
            "first m spatial trace input schema row exists and remains value-missing",
            any(
                entry["input_id"] == "MMT1300_0_sum_abs_Mm_ii_schema"
                and entry["supplied_value"] == "MISSING_NUMERIC_OR_THEOREM_BOUND"
                and not bool(entry["usable_for_scoring"])
                for entry in sum_m_input_rows
            ),
            ";".join(str(entry["input_id"]) + "=" + str(entry["current_status"]) for entry in sum_m_input_rows),
        )
    )
    validations.append(
        validation_row(
            "VAL1300_2_theorem_not_promoted",
            "isotropy/tracefree routes remain unpromoted",
            any(entry["audit_result"] == "FAIL_CURRENT_CORPUS_KEEP_INPUT_ROW_NONCLAIM" for entry in isotropy_theorem_audit)
            and not any(entry["audit_result"] == "DERIVED_FOR_CLAIM" for entry in isotropy_theorem_audit),
            ";".join(str(entry["theorem_id"]) + "=" + str(entry["audit_result"]) for entry in isotropy_theorem_audit),
        )
    )
    validations.append(
        validation_row(
            "VAL1300_3_Kbar_not_scoreable",
            "Kbar update preview keeps scoring blocked",
            all("NO_SCORE" in str(entry["effect_on_scoring"]) or "PREVENTS_FALSE" in str(entry["effect_on_scoring"]) for entry in kbar_update),
            ";".join(str(entry["update_id"]) + "=" + str(entry["effect_on_scoring"]) for entry in kbar_update),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        FIRST_TRACE_AUDIT_PATH,
        SUM_MM_INPUT_PATH,
        ISOTROPY_THEOREM_AUDIT_PATH,
        KBAR_UPDATE_PATH,
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
    validations.append(validation_row("VAL1300_4_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1300_5_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1300_6_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, first_trace_audit, sum_m_input_rows, isotropy_theorem_audit, kbar_update, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1300_7_next_target_1301",
            "next target routes to parent metric-response components for m spatial trace",
            next_target[0]["next_id"] == "NEXT1300_0_1301" and "metric-response-components" in str(next_target[0]["target_file"]),
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(entry["status"] == "PASS" for entry in validations)
    validations.append(
        validation_row(
            "VAL1300_8_overall",
            "overall 1300 validation",
            overall_pass,
            "1300 names the first spatial trace input, rejects unsupported theorem shortcuts, keeps Kbar scoring blocked, and routes to parent response-component derivation",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1300 Y5 R10 RAB first spatial-trace kernel input or isotropy theorem

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1300 does not derive a parent-owned tracefree/isotropic/metric-invisible theorem for the m-chain spatial response. The first missing input is now named cleanly as `M_m^Sigma_abs := sum_i |M_m^{{ii}}|`, but its value/theorem bound is still absent.

**Main progress:** the m spatial trace blocker is no longer vague. The correct first-row nonclaim form is `|R_m^Sigma| <= |C_sign| L_cg^-2 |F_prime(m)| M_m^Sigma_abs`. This is a useful hard target for the next derivation attempt.

**Still blocked:** `M_m^Sigma_abs` has no numeric value, no parent variation derivation, no units lock, and no domain/frame lock. Therefore no Newton/PPN/R10/local-GR score is allowed from the 00-only rows.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## First Trace Input Audit

{markdown_table(first_trace_audit, ["audit_id", "target_input", "what_is_known", "candidate_formula", "status", "missing_to_score", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

## `sum_i M_m^{{ii}}` Input Rows

{markdown_table(sum_m_input_rows, ["input_id", "target_kernel", "input_symbol", "definition", "bound_form", "source_path", "source_anchor", "supplied_value", "supplied_units", "remaining_missing", "current_status", "usable_for_scoring", "valid_for_claim", "claim_allowed", "next_action"])}

## Isotropy / Tracefree Theorem Audit

{markdown_table(isotropy_theorem_audit, ["theorem_id", "candidate_theorem", "would_supply", "audit_result", "reason", "missing_to_promote", "valid_for_claim", "claim_allowed"])}

## Kbar Update Preview

{markdown_table(kbar_update, ["update_id", "target_row", "old_missing", "new_named_input", "new_status", "effect_on_bound", "effect_on_scoring", "valid_for_claim", "claim_allowed"])}

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
