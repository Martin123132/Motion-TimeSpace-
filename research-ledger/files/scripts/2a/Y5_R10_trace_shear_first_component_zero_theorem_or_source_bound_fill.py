from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_trace_shear_split_locked_projected_channel_not_metric_shear_zero_nonclaim"
CLAIM_CEILING = "trace_shear_first_component_gate_only_no_epsilon_tau_claim_no_MH_ref_no_Qbar_no_R10_no_PPN_no_orbital_no_local_GR_claim"
NEXT_TARGET = "691-Y5-R10-shear-channel-bound-source-pack-or-boundary-nohair-theorem.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "690-Y5-R10-trace-shear-first-component-zero-theorem-or-source-bound-fill.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "132_doc": ROOT / "132-smooth-memory-growth-theorem-attempt.md",
    "142_doc": ROOT / "142-domain-load-tensor-owner-promotion-gate.md",
    "143_doc": ROOT / "143-domain-selector-variational-action-attempt.md",
    "247_doc": ROOT / "247-local-EH-exterior-sufficiency-stack-no-promotion.md",
    "276_doc": ROOT / "276-coherent-domain-projector-from-parent-variables.md",
    "327_doc": ROOT / "327-JC-parent-current-bridge-gate.md",
    "328_doc": ROOT / "328-topological-MTS-support-projector-gate.md",
    "347_doc": ROOT / "347-local-GR-parent-reduction-theorem-attempt.md",
    "352_doc": ROOT / "352-boundary-nohair-and-PPN-residual-vector-gate.md",
    "603_doc": ROOT / "603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md",
    "655_eh_audit": RESIDUALS / "P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv",
    "655_validation": RESIDUALS / "P8_Y5_BRR545_655_VALIDATION.csv",
    "688_validation": RESIDUALS / "P8_Y5_BRR545_688_VALIDATION.csv",
    "688_decomposition": RESIDUALS / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv",
    "688_input_template": RESIDUALS / "P8_Y5_R10_688_COMPONENT_BOUND_INPUT_TEMPLATE.csv",
    "689_validation": RESIDUALS / "P8_Y5_BRR545_689_VALIDATION.csv",
    "689_zero_audit": RESIDUALS / "P8_Y5_R10_689_COMPONENT_ZERO_THEOREM_AUDIT.csv",
    "689_source_pack": RESIDUALS / "P8_Y5_R10_689_COMPONENT_SOURCE_PACK.csv",
    "boundary_reference_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "MISSING_VALIDATION_FILE", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate_path in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate_path.is_file()
        and datetime.fromtimestamp(candidate_path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "132_doc": "coherence invariant records theta/shear/vorticity separation",
        "142_doc": "domain projector says tracefree shear/GW is only trace-channel conditional",
        "143_doc": "domain variational attempt leaves second-order and boundary terms open",
        "247_doc": "local EH exterior stack keeps trace-free shear zero conditional",
        "276_doc": "coherent projection kills tracefree part in J_C channel for fixed domain",
        "327_doc": "J_C bridge marks tracefree shear killed by P_coh/Q_coh",
        "328_doc": "topological support projector marks projected tracefree shear exact",
        "347_doc": "local GR reduction keeps no trace-free/shear stress conditional",
        "352_doc": "boundary no-hair ledger leaves trace-free/shear boundary terms open",
        "603_doc": "A_D/N_D primitive and selector context for trace channel",
        "655_eh_audit": "EH-only premise audit for physical local exterior",
        "655_validation": "655 validation gate",
        "688_validation": "688 validation gate",
        "688_decomposition": "symgrad tau decomposition with theta versus shear split",
        "688_input_template": "component bound template inherited by 689/690",
        "689_validation": "689 validation gate",
        "689_zero_audit": "component zero-theorem predecessor",
        "689_source_pack": "component source-pack predecessor",
        "boundary_reference_status": "M_H_ref denominator remains blocked",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def trace_zero_theorem_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "audit_id": "TZ690_0_trace_identity",
            "component": "theta_D_or_X_D",
            "candidate_zero_route": "stable local domain gives vanishing scalar coherent volume channel",
            "mathematical_status": "identity_plus_conditional_selector",
            "supporting_logic": "P_coh retains only the scalar trace/coherent volume part, so trace silence is meaningful inside J_C",
            "missing_parent_clause": "physical domain D, P_MTS kernel, and X_D ownership remain unsigned",
            "result": "conditional_not_claim_ready",
            "valid_for_claim": "false",
            "source_paths": source_list("142_doc", "156_doc") if "156_doc" in SOURCE_PATHS else source_list("142_doc", "603_doc"),
            "generated_utc": now,
        },
        {
            "audit_id": "TZ690_1_selector",
            "component": "A_D_or_N_D_selector",
            "candidate_zero_route": "parent activation selector sets local coherent load to zero",
            "mathematical_status": "promising_but_not_signed",
            "supporting_logic": "603 supplies the right primitive shape for scalar memory silence",
            "missing_parent_clause": "selector is not yet a full local stationary/Killing theorem",
            "result": "conditional_not_claim_ready",
            "valid_for_claim": "false",
            "source_paths": source_list("603_doc", "688_decomposition", "689_zero_audit"),
            "generated_utc": now,
        },
        {
            "audit_id": "TZ690_2_dynamic_safety",
            "component": "local_trace_under_dynamic_perturbations",
            "candidate_zero_route": "local branch remains on trace plateau under perturbations",
            "mathematical_status": "open",
            "supporting_logic": "older domain work warned that boundary and second-order terms can re-enter",
            "missing_parent_clause": "no parent proof that local systems stay in the zero scalar channel after perturbations",
            "result": "source_bound_required",
            "valid_for_claim": "false",
            "source_paths": source_list("143_doc", "352_doc", "688_input_template"),
            "generated_utc": now,
        },
        {
            "audit_id": "TZ690_3_trace_verdict",
            "component": "B_trace",
            "candidate_zero_route": "promote trace to theorem_zero",
            "mathematical_status": "blocked",
            "supporting_logic": "trace channel is the best route but still depends on unsigned selector/domain clauses",
            "missing_parent_clause": "claim-grade zero theorem or numeric bound with units/source path",
            "result": "keep_missing_bound_row",
            "valid_for_claim": "false",
            "source_paths": source_list("688_input_template", "689_source_pack"),
            "generated_utc": now,
        },
    ]


def shear_zero_theorem_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "audit_id": "SZ690_0_projected_channel",
            "component": "projected_tracefree_shear_in_J_C",
            "candidate_zero_route": "P_coh/Q_coh removes tracefree shear from coherent scalar memory current",
            "mathematical_status": "channel_silence_only",
            "supporting_logic": "fixed-domain coherent projection is orthogonal to the tracefree part and can kill shear inside J_C",
            "fatal_gap_for_local_GR": "this is not the same proposition as physical metric shear sigma_mu_nu=0",
            "result": "useful_internal_support_no_metric_claim",
            "valid_for_claim": "false",
            "source_paths": source_list("276_doc", "327_doc", "328_doc"),
            "generated_utc": now,
        },
        {
            "audit_id": "SZ690_1_metric_shear",
            "component": "sigma_mu_nu",
            "candidate_zero_route": "infer physical metric shear zero from trace/projector silence",
            "mathematical_status": "invalid_inference",
            "supporting_logic": "zero trace does not imply zero tracefree tensor; a projected scalar current can ignore shear while the metric still carries it",
            "fatal_gap_for_local_GR": "Killing stationarity needs symgrad tau components suppressed in the observed metric, not only in the scalar memory projection",
            "result": "theorem_zero_rejected",
            "valid_for_claim": "false",
            "source_paths": source_list("688_decomposition", "689_zero_audit"),
            "generated_utc": now,
        },
        {
            "audit_id": "SZ690_2_EH_nohair",
            "component": "trace_free_boundary_or_exterior_shear",
            "candidate_zero_route": "derive metric-only EH exterior/no-hair branch",
            "mathematical_status": "conditional_open",
            "supporting_logic": "local EH/no-hair work names sufficient conditions, including no trace-free/shear stress",
            "fatal_gap_for_local_GR": "EH-only selection and boundary no-hair are not parent-derived",
            "result": "not_claim_ready",
            "valid_for_claim": "false",
            "source_paths": source_list("247_doc", "347_doc", "352_doc", "655_eh_audit"),
            "generated_utc": now,
        },
        {
            "audit_id": "SZ690_3_source_bound",
            "component": "B_shear_metric",
            "candidate_zero_route": "replace proof with sourced bound row",
            "mathematical_status": "required_fallback",
            "supporting_logic": "if no no-hair proof is available, local residual runner must carry a numeric/theorem source row",
            "fatal_gap_for_local_GR": "current corpus has no sourced metric shear amplitude bound for R10/PPN/clock/orbital arenas",
            "result": "keep_missing_bound_row",
            "valid_for_claim": "false",
            "source_paths": source_list("688_input_template", "689_source_pack"),
            "generated_utc": now,
        },
        {
            "audit_id": "SZ690_4_shear_verdict",
            "component": "B_shear",
            "candidate_zero_route": "promote projected shear kill to physical shear zero",
            "mathematical_status": "rejected",
            "supporting_logic": "the projector result is real but scoped to the scalar/coherent memory channel",
            "fatal_gap_for_local_GR": "local GR requires metric shear/Killing residual control",
            "result": "source_bound_or_nohair_theorem_required",
            "valid_for_claim": "false",
            "source_paths": source_list("276_doc", "327_doc", "328_doc", "352_doc", "689_source_pack"),
            "generated_utc": now,
        },
    ]


def trace_shear_source_bound_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        (
            "TSB690_0_trace",
            "theta_D_or_X_D",
            "B_trace",
            "theorem_zero_or_numeric_trace_bound",
            "MISSING_THETA_D_OR_XD_SOURCE_BOUND",
            "scalar/coherent memory channel only unless lifted to observed metric",
            "142_doc;143_doc;603_doc;689_source_pack",
        ),
        (
            "TSB690_1_projected_shear",
            "projected_tracefree_shear_in_J_C",
            "Z_projected_shear_channel",
            "fixed-domain projector proof plus parent-owned domain/kernel",
            "MISSING_PROJECTED_SHEAR_CHANNEL_CERTIFICATE",
            "validates J_C channel silence only, not physical sigma_mu_nu",
            "276_doc;327_doc;328_doc",
        ),
        (
            "TSB690_2_metric_shear",
            "sigma_mu_nu",
            "B_shear_metric",
            "metric no-hair theorem or sourced bound with units",
            "MISSING_METRIC_SHEAR_SOURCE_BOUND",
            "required for local-GR/PPN residual vector",
            "247_doc;347_doc;352_doc;655_eh_audit;689_source_pack",
        ),
        (
            "TSB690_3_cross_guard",
            "trace_to_shear_nonimplication_guard",
            "logic_guard",
            "proof that the runner never treats trace/projected-channel zero as metric shear zero",
            "SCHEMA_ONLY_NONCLAIM_TRACE_SHEAR_GUARD",
            "prevents false local-GR promotion",
            "688_decomposition;689_zero_audit",
        ),
        (
            "TSB690_4_denominator",
            "M_ref_candidate",
            "denominator",
            "claim-ready same-frame M_H_ref or nonclaim denominator",
            "MISSING_CLAIM_READY_M_REF_CANDIDATE",
            "epsilon_tau still cannot be dimensionless claim-grade",
            "boundary_reference_status;689_source_pack",
        ),
    ]
    output_rows = []
    for row_id, component, symbol, evidence, status, arena_role, source_ids_text in rows:
        source_ids = source_ids_text.split(";")
        output_rows.append(
            {
                "row_id": row_id,
                "component": component,
                "bound_symbol": symbol,
                "required_evidence": evidence,
                "current_status": status,
                "arena_role": arena_role,
                "valid_for_claim": "false",
                "source_paths": source_list(*source_ids),
                "generated_utc": now,
            }
        )
    return output_rows


def decision_matrix_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "DM690_0_trace",
            "route": "trace zero",
            "result": "conditional_not_closed",
            "meaning": "scalar memory trace may be silent in local domains, but the parent selector/domain proof is unsigned",
            "next_action": "carry B_trace as missing source-bound row until proof or bound exists",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DM690_1_projected_shear",
            "route": "projected shear zero",
            "result": "channel_silence_only",
            "meaning": "P_coh/Q_coh can kill tracefree shear inside J_C/coherent scalar current",
            "next_action": "record as internal support, not local-GR evidence",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DM690_2_metric_shear",
            "route": "physical metric shear zero",
            "result": "not_derived",
            "meaning": "sigma_mu_nu=0 or Killing stationarity has not been parent-derived",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DM690_3_claim_policy",
            "route": "local-GR promotion",
            "result": "forbidden",
            "meaning": "projector silence cannot be used as a metric no-hair theorem",
            "next_action": "no R10/PPN/clock/orbital/local-GR pass from 690",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "CG690_0_trace",
            "gate": "trace theorem-zero gate",
            "required_state": "parent-signed zero theorem for theta_D/X_D or numeric bound with units/source path",
            "observed_state": "conditional selector/domain route only",
            "result": "fail_blocked",
            "claim_effect": "B_trace remains missing/nonclaim",
            "valid_for_claim": "false",
            "source_paths": source_list("142_doc", "143_doc", "603_doc", "689_source_pack"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG690_1_projected_shear",
            "gate": "projected shear channel gate",
            "required_state": "prove exact scope of P_coh/Q_coh and forbid promotion to metric shear",
            "observed_state": "channel silence is supported but local metric implication is rejected",
            "result": "pass_as_scope_guard_only",
            "claim_effect": "useful internal theorem, no local-GR claim",
            "valid_for_claim": "false",
            "source_paths": source_list("276_doc", "327_doc", "328_doc"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG690_2_metric_shear",
            "gate": "physical metric shear gate",
            "required_state": "sigma_mu_nu=0 by EH/no-hair/Killing theorem or sourced bound row",
            "observed_state": "not derived; boundary no-hair remains open",
            "result": "fail_blocked",
            "claim_effect": "B_shear_metric remains missing/nonclaim",
            "valid_for_claim": "false",
            "source_paths": source_list("247_doc", "347_doc", "352_doc", "655_eh_audit", "689_source_pack"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG690_3_denominator",
            "gate": "same-frame denominator gate",
            "required_state": "claim-ready M_H_ref or equivalent same-frame denominator",
            "observed_state": "boundary/reference status remains blocked",
            "result": "fail_blocked",
            "claim_effect": "epsilon_tau cannot be claim-grade",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "689_source_pack"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG690_4_next",
            "gate": "next target selection",
            "required_state": "choose route that closes most dangerous gap",
            "observed_state": NEXT_TARGET,
            "result": "selected",
            "claim_effect": "go after metric shear by source bounds or boundary no-hair",
            "valid_for_claim": "false",
            "source_paths": source_list("352_doc", "689_source_pack"),
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D690_0_trace",
            "target": "trace zero theorem",
            "result": "not_closed",
            "reason": "trace/coherent load silence remains plausible but parent-domain selector is unsigned",
            "next_action": "keep B_trace missing until theorem or sourced bound exists",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D690_1_shear",
            "target": "metric shear zero theorem",
            "result": "rejected_for_current_corpus",
            "reason": "P_coh/Q_coh kills tracefree shear only inside the coherent scalar current, not in the observed metric",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D690_2_policy",
            "target": "local claim policy",
            "result": "nonclaim",
            "reason": "no physical sigma_mu_nu=0, no Killing stationarity, and no denominator",
            "next_action": "no R10/PPN/clock/orbital/local-GR promotion",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S690_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "trace route remains conditional; projected shear silence is real but scoped to J_C/coherent scalar channel; physical metric shear zero is not derived",
            "hardest_blocker": "projected-channel zero cannot substitute for sigma_mu_nu=0 or Killing stationarity",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def all_valid_for_claim_false(rows_by_name: dict[str, list[dict[str, str]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("valid_for_claim") == "true":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, str]],
    trace_rows: list[dict[str, str]],
    shear_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    matrix_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows_by_name = {
        "trace": trace_rows,
        "shear": shear_rows,
        "bound": bound_rows,
        "matrix": matrix_rows,
        "gates": gate_rows,
        "decision": decision_rows_,
        "summary": summary_rows,
    }
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_ids = ["655_validation", "688_validation", "689_validation"]
    prior_failure_counts = {source_id: len(validation_failures_for(source_id)) for source_id in prior_ids}
    trace_complete = len(trace_rows) == 4 and all(row["valid_for_claim"] == "false" for row in trace_rows)
    shear_complete = len(shear_rows) == 5 and all(row["valid_for_claim"] == "false" for row in shear_rows)
    projected_scope_guard = any(row["mathematical_status"] == "channel_silence_only" for row in shear_rows) and any(
        "not the same proposition as physical metric shear" in row["fatal_gap_for_local_GR"] for row in shear_rows
    )
    metric_zero_rejected = any(row["result"] == "theorem_zero_rejected" for row in shear_rows)
    bound_complete = len(bound_rows) == 5 and all(row["valid_for_claim"] == "false" for row in bound_rows)
    missing_or_schema_retained = all(
        "MISSING_" in row["current_status"] or row["current_status"].startswith("SCHEMA_ONLY") for row in bound_rows
    )
    matrix_complete = len(matrix_rows) == 4 and any(row["result"] == "forbidden" for row in matrix_rows)
    gates_block = all(row["valid_for_claim"] == "false" for row in gate_rows) and any(row["result"].startswith("fail") for row in gate_rows)
    no_claim_rows = all_valid_for_claim_false(rows_by_name)
    next_selected = any(row["next_action"] == NEXT_TARGET for row in decision_rows_) and any(
        row["next_target"] == NEXT_TARGET for row in summary_rows
    )
    formalization_count = formalization_changed_count()
    output_paths = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_690_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_690_TRACE_ZERO_THEOREM_AUDIT.csv",
        RESIDUALS / "P8_Y5_R10_690_SHEAR_ZERO_THEOREM_AUDIT.csv",
        RESIDUALS / "P8_Y5_R10_690_TRACE_SHEAR_SOURCE_BOUND_TEMPLATE.csv",
        RESIDUALS / "P8_Y5_R10_690_TRACE_SHEAR_DECISION_MATRIX.csv",
        RESIDUALS / "P8_Y5_R10_690_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_690_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_690_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_690_VALIDATION.csv",
    ]
    scoped_outputs = all(str(path).startswith(str(ROOT)) for path in output_paths)
    checks = [
        ("V690_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V690_1_prior_validations_clean", all(count == 0 for count in prior_failure_counts.values()), ";".join(f"{key}={value}" for key, value in prior_failure_counts.items())),
        ("V690_2_trace_audit_complete", trace_complete, f"trace_rows={len(trace_rows)}"),
        ("V690_3_shear_audit_complete", shear_complete, f"shear_rows={len(shear_rows)}"),
        ("V690_4_projected_scope_guard_present", projected_scope_guard, "projected shear is explicitly channel_silence_only and not metric shear zero"),
        ("V690_5_metric_shear_zero_rejected", metric_zero_rejected, "physical sigma_mu_nu zero theorem rejected for current corpus"),
        ("V690_6_bound_template_complete", bound_complete, f"bound_rows={len(bound_rows)}"),
        ("V690_7_missing_markers_retained", missing_or_schema_retained, "bound rows retain MISSING or SCHEMA_ONLY status"),
        ("V690_8_decision_matrix_blocks_promotion", matrix_complete, "decision matrix includes forbidden local-GR promotion"),
        ("V690_9_claim_gates_block", gates_block, "claim gates block trace/shear/denominator/local promotion"),
        ("V690_10_no_claim_rows_promoted", no_claim_rows, "all generated 690 rows remain valid_for_claim=false"),
        ("V690_11_next_target_selected", next_selected, NEXT_TARGET),
        ("V690_12_generated_outputs_scoped", scoped_outputs, "all 690 outputs target post-checkpoint-work"),
        ("V690_13_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V690_14_status_nonclaim", "no_epsilon_tau_claim" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now,
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, divider, *body]) + "\n"


def write_doc(
    source_rows: list[dict[str, str]],
    trace_rows: list[dict[str, str]],
    shear_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    matrix_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    doc = f"""# 690 - Y5 R10 Trace Shear First Component Zero Theorem Or Source Bound Fill

## Verdict

690 separates two propositions that must not be allowed to blur:

```text
projected tracefree shear silence in the coherent scalar memory channel
!=
physical metric shear zero, sigma_mu_nu = 0
```

The old projector route is still useful. For a fixed, parent-owned coherent domain, `P_coh/Q_coh` can remove the tracefree part from the scalar current `J_C`. That is an internal structural win.

But it is not a local-GR theorem. Local GR/PPN needs control of the observed metric residual: `sigma_mu_nu`, Killing failure, boundary trace-free stress, and the same-frame denominator. Those are still unsigned. So 690 records the useful projected-channel result, rejects promotion to physical shear zero, and writes the trace/shear source-bound template for the next pass.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Trace Zero Theorem Audit

{markdown_table(trace_rows, ["audit_id", "component", "mathematical_status", "result", "missing_parent_clause", "valid_for_claim"])}

## Shear Zero Theorem Audit

{markdown_table(shear_rows, ["audit_id", "component", "mathematical_status", "result", "fatal_gap_for_local_GR", "valid_for_claim"])}

## Trace Shear Source Bound Template

{markdown_table(bound_rows, ["row_id", "component", "bound_symbol", "required_evidence", "current_status", "arena_role", "valid_for_claim"])}

## Trace Shear Decision Matrix

{markdown_table(matrix_rows, ["decision_id", "route", "result", "meaning", "next_action", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gate_rows, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows_, ["check_id", "result", "detail"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    trace_rows = trace_zero_theorem_rows()
    shear_rows = shear_zero_theorem_rows()
    bound_rows = trace_shear_source_bound_rows()
    matrix_rows = decision_matrix_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    summary_rows = nonclaim_summary_rows()
    validation_rows_ = validation_rows(
        source_rows,
        trace_rows,
        shear_rows,
        bound_rows,
        matrix_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
    )

    write_csv(RESIDUALS / "P8_Y5_R10_690_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_690_TRACE_ZERO_THEOREM_AUDIT.csv", trace_rows, ["audit_id", "component", "candidate_zero_route", "mathematical_status", "supporting_logic", "missing_parent_clause", "result", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_690_SHEAR_ZERO_THEOREM_AUDIT.csv", shear_rows, ["audit_id", "component", "candidate_zero_route", "mathematical_status", "supporting_logic", "fatal_gap_for_local_GR", "result", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_690_TRACE_SHEAR_SOURCE_BOUND_TEMPLATE.csv", bound_rows, ["row_id", "component", "bound_symbol", "required_evidence", "current_status", "arena_role", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_690_TRACE_SHEAR_DECISION_MATRIX.csv", matrix_rows, ["decision_id", "route", "result", "meaning", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_690_CLAIM_GATE_EVALUATION.csv", gate_rows, ["gate_id", "gate", "required_state", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_690_DECISION.csv", decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_690_NONCLAIM_SUMMARY.csv", summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_690_VALIDATION.csv", validation_rows_, ["check_id", "result", "detail", "generated_utc"])

    write_doc(source_rows, trace_rows, shear_rows, bound_rows, matrix_rows, gate_rows, decision_rows_, summary_rows, validation_rows_)

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"trace_rows={len(trace_rows)}")
    print(f"shear_rows={len(shear_rows)}")
    print(f"bound_rows={len(bound_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
