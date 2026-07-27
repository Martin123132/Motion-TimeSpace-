from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1299"
TITLE = "1299-Y5-R10-RAB-spatial-trace-kernel-bound-or-trace-theorem"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
TRACE_THEOREM_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_TRACE_THEOREM_AUDIT.csv"
SPATIAL_TRACE_KERNELS_PATH = OUT_DIR / f"{PACK_ID}_SPATIAL_TRACE_KERNEL_ROWS_NONCLAIM.csv"
KBAR_BOUND_PATH = OUT_DIR / f"{PACK_ID}_KBAR_BOUND_ASSEMBLY_NONCLAIM.csv"
RUNNER_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_MISSING_INPUT_UPDATE.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1299_VALIDATION.csv"


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
        TRACE_THEOREM_AUDIT_PATH,
        SPATIAL_TRACE_KERNELS_PATH,
        KBAR_BOUND_PATH,
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
            "source_id": "SRC1299_0_1298_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1298_NEXT_TARGET.csv",
            "needle": "NEXT1298_0_1299",
            "role": "handoff into spatial trace theorem/bound gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1299_1_projection_formula",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1298_KBAR_PROJECTION_FORMULA_NONCLAIM.csv",
            "needle": "MISSING_R_m_ii_BOUND",
            "role": "1298 proof that spatial trace is required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1299_2_trace_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1298_SPATIAL_TRACE_REQUIREMENTS.csv",
            "needle": "MISSING_SPATIAL_M_KERNEL_TRACE",
            "role": "explicit spatial trace missing inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1299_3_derivative_chain",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "needle": "Kmetric_chain^{00}=C_sign",
            "role": "available 00 kernel shape to generalize symbolically to ii rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1299_4_bound_ledger",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
            "needle": "BOUND_FORM_ONLY_NONCLAIM",
            "role": "00 component bound forms retained as known symbolic pieces",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1299_5_trace_map_score",
            "local_path": "source-intake/mts_residuals/P8_EXCHANGE_COMPONENT_MAP_SCORE.csv",
            "needle": "Y0_trace_expansion",
            "role": "current corpus says trace-load closure is not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1299_6_no_anisotropy_attempt",
            "local_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
            "needle": "T3_no_anisotropic_selector_stress",
            "role": "no-STF/no-anisotropy route remains conditional, not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1299_7_boundary_scalar_attempt",
            "local_path": "source-intake/mts_residuals/P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv",
            "needle": "O2_scalar_not_enough_warning",
            "role": "scalar/homogeneous shortcut can fail if angular scalar terms generate trace-free pieces",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1299_8_R11_gates",
            "local_path": "source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_GATES.csv",
            "needle": "G4_stress_Bianchi_closed",
            "role": "stress/Bianchi closure still fails for claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    trace_theorem_audit = [
        {
            "audit_id": "TTA1299_0_tracefree_shortcut",
            "candidate_theorem": "K_chain is trace-free in the local flat frame",
            "would_imply": "sum_i K_chain^{ii}=K_chain^{00}, so Kbar_L,loc,00 reduces to K_chain^{00} up to projection/boundary terms",
            "evidence_found": "none in 1289/1291; 1298 marks tracefree/isotropy shortcut blocked",
            "status": "NOT_DERIVED",
            "missing_to_promote": "MISSING_TRACEFREE_PARENT_THEOREM;MISSING_INDEX_CONVENTION_LOCK;MISSING_PROJECTOR_DOMAIN_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "TTA1299_1_isotropic_pressure_shortcut",
            "candidate_theorem": "local spatial response is isotropic, K_chain^{ij}=p_K delta^{ij}",
            "would_imply": "sum_i K_chain^{ii}=3 p_K, but p_K/K_chain^{00} still requires an equation of state or parent stress theorem",
            "evidence_found": "boundary scalar rows give conditional isotropic/stationary routes only; not parent-owned",
            "status": "CONDITIONAL_NOT_SCOREABLE",
            "missing_to_promote": "MISSING_EQUATION_OF_STATE_OR_STRESS_RELATION;MISSING_PARENT_OWNER;MISSING_BOUNDARY_FLUX_CLOSURE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "TTA1299_2_metric_invisible_shortcut",
            "candidate_theorem": "K_chain is topological/improvement/projector-silent in the local metric equation",
            "would_imply": "Kbar_L,loc,00=0 and no spatial trace bound needed",
            "evidence_found": "topological/projector silence remains conditional; R11 stress/Bianchi closure fails for claim",
            "status": "BLOCKED_NOT_PARENT_DERIVED",
            "missing_to_promote": "MISSING_TOPOLOGICAL_PROJECTOR_OWNER;MISSING_NO_FLUX_THEOREM;MISSING_R11_STRESS_SILENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "TTA1299_3_Ward_Bianchi_shortcut",
            "candidate_theorem": "Ward/Bianchi conservation alone fixes the spatial trace",
            "would_imply": "no independent spatial trace inputs needed",
            "evidence_found": "existing ledgers distinguish conservation/ownership from absence or smallness",
            "status": "REJECTED_SHORTCUT",
            "missing_to_promote": "not promotable without additional local stress theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "TTA1299_4_current_verdict",
            "candidate_theorem": "current corpus proves a trace/isotropy shortcut usable for Kbar_00 scoring",
            "would_imply": "1298 spatial trace missing inputs could be removed",
            "evidence_found": "all candidate routes are absent, conditional, or failed-for-claim",
            "status": "FAIL_CURRENT_CORPUS_KEEP_SPATIAL_TRACE_ROWS",
            "missing_to_promote": "derive parent trace theorem or fill explicit spatial trace kernels",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    spatial_trace_kernels = [
        {
            "kernel_id": "STK1299_0_m_spatial_trace",
            "component": "R_m^Sigma := sum_i R_m^{ii}",
            "symbolic_bound": "|R_m^Sigma| <= |C_sign| L_cg^-2 |F_prime(m)| sum_i |M_m^{ii}|",
            "needed_inputs": "ABS_C_SIGN_EQ_1_BOUND_ONLY;MISSING_L_cg_VALUE;MISSING_m_PROFILE;MISSING_F_PRIME_BOUND;MISSING_SUM_i_M_m_ii_BOUND",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_1298_SPATIAL_TRACE_REQUIREMENTS.csv",
            "source_anchor": "KDR1289_0_Gamma_m_L_chain_kernel_00;STR1298_0_m_spatial_trace",
            "current_status": "SPATIAL_TRACE_BOUND_TEMPLATE_NONCLAIM_MISSING_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "STK1299_1_Lcg_spatial_trace",
            "component": "R_L^Sigma := sum_i R_L^{ii}",
            "symbolic_bound": "|R_L^Sigma| <= 2 |C_sign| L_cg^-3 |F(m)| sum_i |M_L^{ii}|",
            "needed_inputs": "ABS_C_SIGN_EQ_1_BOUND_ONLY;MISSING_L_cg_VALUE;MISSING_LCG_LOWER_BOUND;MISSING_m_PROFILE;MISSING_F_BOUND;MISSING_SUM_i_M_L_ii_BOUND",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_1298_SPATIAL_TRACE_REQUIREMENTS.csv",
            "source_anchor": "KDR1289_0_Gamma_m_L_chain_kernel_00;STR1298_1_Lcg_spatial_trace",
            "current_status": "SPATIAL_TRACE_BOUND_TEMPLATE_NONCLAIM_MISSING_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "STK1299_2_cdb_spatial_trace",
            "component": "R_cdb^Sigma := sum_i R_cdb^{ii}",
            "symbolic_bound": "|R_cdb^Sigma| <= sum_i(|K_conn^{ii}|+|K_domain^{ii}|+|K_boundary^{ii}|)",
            "needed_inputs": "MISSING_SUM_i_K_CONN_ii_BOUND;MISSING_SUM_i_K_DOMAIN_ii_BOUND;MISSING_SUM_i_K_BOUNDARY_ii_BOUND;MISSING_NO_FLUX_SOURCE",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv;source-intake/mts_residuals/P8_Y5_R10_1298_SPATIAL_TRACE_REQUIREMENTS.csv",
            "source_anchor": "KRB1291_2_cdb_bound;STR1298_2_cdb_spatial_trace",
            "current_status": "SPATIAL_TRACE_CDB_TEMPLATE_NONCLAIM_MISSING_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "STK1299_3_projector_boundary_trace",
            "component": "Delta_projector_boundary",
            "symbolic_bound": "|Delta_projector_boundary| <= |[P_loc, trace_reverse]K_chain| + |boundary_reference_trace|",
            "needed_inputs": "MISSING_PROJECTOR_COMMUTATOR_BOUND;MISSING_BOUNDARY_REFERENCE_TRACE_BOUND;MISSING_INDEX_CONVENTION_LOCK",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1298_SPATIAL_TRACE_REQUIREMENTS.csv;source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "source_anchor": "STR1298_3_projector_domain;KGL776_3_boundary_reference_terms",
            "current_status": "PROJECTOR_BOUNDARY_TRACE_TEMPLATE_NONCLAIM_MISSING_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    kbar_bound = [
        {
            "assembly_id": "KBA1299_0_total_Kbar_abs_bound",
            "assembled_bound": "|Kbar_L,loc,00| <= 0.5*(|R_m^{00}|+|R_L^{00}|+|R_cdb^{00}|+|R_m^Sigma|+|R_L^Sigma|+|R_cdb^Sigma|)+|Delta_projector_boundary|",
            "known_from_prior": "00 symbolic templates from 1291/1292; projection identity from 1298; source normalization from 1297",
            "new_from_1299": "spatial trace kernel templates for R_m^Sigma, R_L^Sigma, R_cdb^Sigma",
            "still_missing": "MISSING_NUMERIC_OR_THEOREM_INPUTS_FOR_ALL_SPATIAL_TRACE_ROWS;MISSING_RHO_REF;MISSING_MEASURED_GM_CALIBRATION;MISSING_OBSERVABLE_MAPS",
            "current_status": "ASSEMBLED_BOUND_FORM_ONLY_NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "assembly_id": "KBA1299_1_Newton_budget_bound",
            "assembled_bound": "epsilon_K <= |c^2|/(4*pi*G*rho_ref) * KBA1299_0_total_Kbar_abs_bound",
            "known_from_prior": "1297 source normalization bridge",
            "new_from_1299": "explicit spatial trace term inventory",
            "still_missing": "MISSING_TRACE_INPUTS;MISSING_RHO_REF;MISSING_MEASURED_GM_CALIBRATION;MISSING_LOCAL_TOLERANCE",
            "current_status": "NEWTON_BUDGET_BOUND_FORM_ONLY_NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_update = [
        {
            "update_id": "RUP1299_0_m_chain",
            "runner_id": "RRI1292_0_m_chain",
            "old_missing": "MISSING_M_m_00_BOUND",
            "new_missing_added": "MISSING_SUM_i_M_m_ii_BOUND",
            "reason": "Kbar_00 requires spatial trace of the m-chain response, not just 00",
            "runner_status": "TRACE_INPUT_ADDED_STILL_REJECTED_NONCLAIM_NO_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "RUP1299_1_Lcg_chain",
            "runner_id": "RRI1292_1_Lcg_chain",
            "old_missing": "MISSING_M_L_00_BOUND",
            "new_missing_added": "MISSING_SUM_i_M_L_ii_BOUND",
            "reason": "Kbar_00 requires spatial trace of the Lcg-chain response, not just 00",
            "runner_status": "TRACE_INPUT_ADDED_STILL_REJECTED_NONCLAIM_NO_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "RUP1299_2_cdb_chain",
            "runner_id": "RRI1292_2_cdb_chain",
            "old_missing": "MISSING_K_CONN_BOUND;MISSING_K_DOMAIN_BOUND;MISSING_K_BOUNDARY_BOUND",
            "new_missing_added": "MISSING_SUM_i_K_CONN_ii_BOUND;MISSING_SUM_i_K_DOMAIN_ii_BOUND;MISSING_SUM_i_K_BOUNDARY_ii_BOUND",
            "reason": "connection/domain/boundary terms can enter Kbar through the spatial trace",
            "runner_status": "TRACE_INPUT_ADDED_STILL_REJECTED_NONCLAIM_NO_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "RUP1299_3_chain_vector",
            "runner_id": "RRI1292_3_chain_vector",
            "old_missing": "MISSING_OBSERVABLE_RESPONSE_MATRIX",
            "new_missing_added": "MISSING_FULL_KBAR_TRACE_BOUND;MISSING_TRACE_THEOREM_OR_SPATIAL_KERNELS",
            "reason": "total local response vector cannot be built from 00 rows alone",
            "runner_status": "TRACE_INPUT_ADDED_STILL_REJECTED_NONCLAIM_NO_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1299_0_trace_theorem",
            "claim": "current corpus derives trace/isotropy shortcut",
            "current_status": "BLOCKED_NOT_DERIVED",
            "reason": "candidate tracefree/isotropic/topological/Ward routes are absent, conditional, or rejected",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1299_1_spatial_trace_templates",
            "claim": "spatial trace kernel rows exist",
            "current_status": "SATISFIED_FOR_NONCLAIM_TEMPLATES",
            "reason": "1299 produces R_m^Sigma, R_L^Sigma, R_cdb^Sigma, and projector-boundary templates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1299_2_Kbar_score",
            "claim": "Kbar_L,loc,00 bound is scoreable",
            "current_status": "BLOCKED_MISSING_TRACE_INPUTS",
            "reason": "spatial trace templates still contain MISSING numeric/theorem inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1299_3_local_GR",
            "claim": "local GR/Newton/PPN recovery pass",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "trace templates sharpen the target but do not prove smallness/silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1299_0_no_trace_shortcut",
            "decision": "reject trace/isotropy shortcut for current corpus",
            "because": "no parent-owned tracefree, isotropic equation-of-state, or metric-invisible theorem is present",
            "next_action": "derive or source explicit spatial trace kernel bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1299_1_add_trace_templates",
            "decision": "add spatial trace kernel templates rather than pretending 00 is enough",
            "because": "1298 projection formula forces spatial trace into Kbar_00",
            "next_action": "target the m-spatial trace first because it is the smallest kernel family",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1299_0_1300",
            "target_file": "1300-Y5-R10-RAB-first-spatial-trace-kernel-input-or-isotropy-theorem.md",
            "target_script": "scripts/Y5_R10_RAB_first_spatial_trace_kernel_input_or_isotropy_theorem.py",
            "task": "try to derive the first spatial trace input, prioritizing sum_i M_m^{ii} or a parent isotropy/tracefree theorem; otherwise create nonclaim input rows for the missing trace kernels",
            "success_condition": "one spatial trace kernel receives a source-backed nonclaim bound/theorem row, or the blocker ledger proves all trace routes remain missing",
            "do_not": "do not compute Newton/PPN/R10 scores from 00-only bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(TRACE_THEOREM_AUDIT_PATH, trace_theorem_audit)
    write_csv(SPATIAL_TRACE_KERNELS_PATH, spatial_trace_kernels)
    write_csv(KBAR_BOUND_PATH, kbar_bound)
    write_csv(RUNNER_UPDATE_PATH, runner_update)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1299_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1299_1_trace_shortcut_rejected",
            "trace theorem audit rejects current shortcut while preserving conditional routes",
            any(row["status"] == "FAIL_CURRENT_CORPUS_KEEP_SPATIAL_TRACE_ROWS" for row in trace_theorem_audit)
            and not any(row["status"] == "DERIVED_FOR_CLAIM" for row in trace_theorem_audit),
            ";".join(row["audit_id"] + "=" + row["status"] for row in trace_theorem_audit),
        )
    )
    validations.append(
        validation_row(
            "VAL1299_2_spatial_trace_templates_written",
            "spatial trace kernel templates exist and contain MISSING guards",
            len(spatial_trace_kernels) == 4 and all("MISSING" in row["needed_inputs"] for row in spatial_trace_kernels),
            ";".join(row["kernel_id"] for row in spatial_trace_kernels),
        )
    )
    validations.append(
        validation_row(
            "VAL1299_3_Kbar_bound_not_scoreable",
            "assembled Kbar/Newton bounds remain non-scoreable",
            len(kbar_bound) == 2 and all("NOT_SCOREABLE" in row["current_status"] for row in kbar_bound),
            ";".join(row["assembly_id"] for row in kbar_bound),
        )
    )
    validations.append(
        validation_row(
            "VAL1299_4_runner_updates_no_score",
            "runner update rows remain rejected/no-score",
            len(runner_update) == 4 and all("NO_SCORE" in row["runner_status"] for row in runner_update),
            ";".join(row["runner_id"] for row in runner_update),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        TRACE_THEOREM_AUDIT_PATH,
        SPATIAL_TRACE_KERNELS_PATH,
        KBAR_BOUND_PATH,
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
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{exc}")
    validations.append(validation_row("VAL1299_5_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1299_6_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1299_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, trace_theorem_audit, spatial_trace_kernels, kbar_bound, runner_update, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1299_8_next_target_1300",
            "next target routes to first spatial trace kernel input or theorem",
            next_target[0]["next_id"] == "NEXT1299_0_1300" and "spatial-trace-kernel" in next_target[0]["target_file"],
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1299_9_overall",
            "overall 1299 validation",
            overall_pass,
            "1299 rejects an unsupported trace shortcut, writes spatial trace kernel templates, assembles the correct Kbar bound form, keeps scoring blocked, and routes to first trace input/theorem",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1299 Y5 R10 RAB spatial-trace kernel bound or trace theorem

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1299 does not find a parent-owned trace/isotropy theorem in the current corpus. The clean shortcut `Kbar_{{00}} ~ K^{{00}}` is therefore rejected for now. Instead, 1299 writes the required spatial-trace kernel templates so the Newton bridge cannot accidentally use 00-only data.

**Main progress:** the correct nonclaim assembly is now explicit: `|Kbar_L,loc,00| <= 0.5*(|R_m^{{00}}|+|R_L^{{00}}|+|R_cdb^{{00}}|+|R_m^Sigma|+|R_L^Sigma|+|R_cdb^Sigma|)+|Delta_projector_boundary|`. This is the right shape for the local Newton source budget once the missing trace inputs are derived.

**Still blocked:** every spatial trace route is still non-scoreable. The missing inputs are `sum_i M_m^{{ii}}`, `sum_i M_L^{{ii}}`, spatial CDB bounds, projector/domain commutator bounds, or a real parent trace/isotropy/metric-invisibility theorem.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Trace Theorem Audit

{markdown_table(trace_theorem_audit, ["audit_id", "candidate_theorem", "would_imply", "evidence_found", "status", "missing_to_promote", "valid_for_claim", "claim_allowed"])}

## Spatial Trace Kernel Rows

{markdown_table(spatial_trace_kernels, ["kernel_id", "component", "symbolic_bound", "needed_inputs", "source_path", "source_anchor", "current_status", "valid_for_claim", "claim_allowed"])}

## Kbar Bound Assembly

{markdown_table(kbar_bound, ["assembly_id", "assembled_bound", "known_from_prior", "new_from_1299", "still_missing", "current_status", "valid_for_claim", "claim_allowed"])}

## Runner Missing-Input Update

{markdown_table(runner_update, ["update_id", "runner_id", "old_missing", "new_missing_added", "reason", "runner_status", "valid_for_claim", "claim_allowed"])}

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
