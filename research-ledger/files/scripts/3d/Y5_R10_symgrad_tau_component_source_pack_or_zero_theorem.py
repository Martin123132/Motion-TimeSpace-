from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_symgrad_tau_component_source_pack_written_zero_theorems_fail_or_remain_conditional_nonclaim"
CLAIM_CEILING = "component_source_pack_and_zero_theorem_audit_only_no_epsilon_tau_claim_no_MH_ref_no_Qbar_no_R10_no_PPN_no_orbital_no_local_GR_claim"
NEXT_TARGET = "690-Y5-R10-trace-shear-first-component-zero-theorem-or-source-bound-fill.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "689-Y5-R10-symgrad-tau-component-source-pack-or-zero-theorem.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "132_doc": ROOT / "132-smooth-memory-growth-theorem-attempt.md",
    "142_doc": ROOT / "142-domain-load-tensor-owner-promotion-gate.md",
    "143_doc": ROOT / "143-domain-selector-variational-action-attempt.md",
    "155_doc": ROOT / "155-redshift-projection-clock-map-owner.md",
    "156_doc": ROOT / "156-clock-projection-functional-theorem-or-demotion.md",
    "455_contract": RESIDUALS / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
    "603_doc": ROOT / "603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md",
    "604_kernel_gate": RESIDUALS / "P8_Y5_R10_604_BOUNDARY_KERNEL_BLOCK_GATE.csv",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "655_validation": RESIDUALS / "P8_Y5_BRR545_655_VALIDATION.csv",
    "655_eh_audit": RESIDUALS / "P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv",
    "684_validation": RESIDUALS / "P8_Y5_BRR545_684_VALIDATION.csv",
    "684_tau_audit": RESIDUALS / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
    "685_validation": RESIDUALS / "P8_Y5_BRR545_685_VALIDATION.csv",
    "685_residual_template": RESIDUALS / "P8_Y5_R10_685_TAU_FRAME_RESIDUAL_TEMPLATE.csv",
    "686_validation": RESIDUALS / "P8_Y5_BRR545_686_VALIDATION.csv",
    "686_identity": RESIDUALS / "P8_Y5_R10_686_KILLING_IDENTITY_ATTEMPT.csv",
    "686_tau_residual": RESIDUALS / "P8_Y5_R10_686_NONSTATIONARY_TAU_RESIDUAL_ROW.csv",
    "687_validation": RESIDUALS / "P8_Y5_BRR545_687_VALIDATION.csv",
    "687_epsilon_contract": RESIDUALS / "P8_Y5_R10_687_EPSILON_TAU_BOUND_CONTRACT.csv",
    "687_obstruction": RESIDUALS / "P8_Y5_R10_687_STATIONARITY_OBSTRUCTION_LEDGER.csv",
    "688_doc": ROOT / "688-Y5-R10-symgrad-tau-kinematic-decomposition-bound-or-source-input-fill.md",
    "688_validation": RESIDUALS / "P8_Y5_BRR545_688_VALIDATION.csv",
    "688_decomposition": RESIDUALS / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv",
    "688_input_template": RESIDUALS / "P8_Y5_R10_688_COMPONENT_BOUND_INPUT_TEMPLATE.csv",
    "688_num_den_map": RESIDUALS / "P8_Y5_R10_688_NUMERATOR_DENOMINATOR_MAP.csv",
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
        "132_doc": "coherence invariant with theta/shear/vorticity and gauge warning",
        "142_doc": "domain trace/shear local-silence warnings",
        "143_doc": "domain-boundary stress and dynamic local safety warning",
        "155_doc": "clock/lapse gauge warning",
        "156_doc": "clock functional and gauge safety target",
        "455_contract": "mass-current residual fallback",
        "603_doc": "A_D/N_D activation primitive checkpoint",
        "604_kernel_gate": "P_MTS boundary kernel block gate",
        "655_doc": "EH/R11 local exterior blocker",
        "655_validation": "655 validation gate",
        "655_eh_audit": "EH-only premise audit",
        "684_validation": "684 validation gate",
        "684_tau_audit": "tau role blocker audit",
        "685_validation": "685 validation gate",
        "685_residual_template": "tau/frame residual template rows",
        "686_validation": "686 validation gate",
        "686_identity": "Killing identity rows",
        "686_tau_residual": "nonstationary tau residual rows",
        "687_validation": "687 validation gate",
        "687_epsilon_contract": "epsilon tau bound contract",
        "687_obstruction": "stationarity obstruction ledger",
        "688_doc": "symgrad tau decomposition predecessor",
        "688_validation": "688 validation gate",
        "688_decomposition": "symgrad tau decomposition rows",
        "688_input_template": "component input template rows",
        "688_num_den_map": "numerator/denominator map",
        "boundary_reference_status": "M_H_ref denominator status",
    }
    return [
        {
            "source_id": source_id,
            "path": str(source_path),
            "exists": bool_text(source_path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, source_path in SOURCE_PATHS.items()
    ]


def zero_theorem_audit_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "audit_id": "ZTA689_0_theta",
            "component": "theta_D_or_X_D",
            "zero_route": "stationary compact domain, stable volume, or parent A_D/N_D selector gives scalar trace silence",
            "attempt_result": "conditional_promising_not_closed",
            "blocker": "domain selector, P_MTS kernel, X_D ownership, and dynamic local safety remain conditional",
            "fallback_row": "CSI688_0_theta",
            "priority": "1",
            "valid_for_claim": "false",
            "source_paths": source_list("142_doc", "143_doc", "603_doc", "688_input_template"),
            "generated_utc": now,
        },
        {
            "audit_id": "ZTA689_1_shear",
            "component": "sigma_mu_nu",
            "zero_route": "show selected local branch is static/spherical/EH or no tracefree coherent response survives",
            "attempt_result": "fail_current_corpus",
            "blocker": "trace silence and selector silence do not kill shear; EH/R11 branch still open",
            "fallback_row": "CSI688_1_shear",
            "priority": "2",
            "valid_for_claim": "false",
            "source_paths": source_list("132_doc", "142_doc", "143_doc", "655_eh_audit", "688_input_template"),
            "generated_utc": now,
        },
        {
            "audit_id": "ZTA689_2_lapse_acceleration",
            "component": "a_mu_and_grad_lapse",
            "zero_route": "prove lapse is gauge-fixed by physical clocks and same Hamiltonian tau, with no residual clock coupling",
            "attempt_result": "fail_current_corpus",
            "blocker": "clock/lapse route is known gauge-dangerous and tau lock is unsigned",
            "fallback_row": "CSI688_2_lapse_acceleration",
            "priority": "3",
            "valid_for_claim": "false",
            "source_paths": source_list("155_doc", "156_doc", "684_tau_audit", "685_residual_template"),
            "generated_utc": now,
        },
        {
            "audit_id": "ZTA689_3_shift_extrinsic",
            "component": "shift_or_extrinsic_curvature",
            "zero_route": "derive observed spatial metric stationarity or EH stationary exterior so K_ij/shift terms cancel",
            "attempt_result": "fail_current_corpus",
            "blocker": "no EH-only stationary exterior or ADM convention/source row is signed",
            "fallback_row": "CSI688_3_shift_extrinsic",
            "priority": "4",
            "valid_for_claim": "false",
            "source_paths": source_list("655_doc", "655_eh_audit", "688_decomposition"),
            "generated_utc": now,
        },
        {
            "audit_id": "ZTA689_4_boundary_motion",
            "component": "boundary_velocity_and_reference_shift",
            "zero_route": "prove comoving boundary, no boundary current, and fixed reference class",
            "attempt_result": "fail_current_corpus",
            "blocker": "domain-boundary exchange and M_H_ref reference remain open",
            "fallback_row": "CSI688_4_boundary_motion",
            "priority": "5",
            "valid_for_claim": "false",
            "source_paths": source_list("143_doc", "604_kernel_gate", "boundary_reference_status", "688_input_template"),
            "generated_utc": now,
        },
        {
            "audit_id": "ZTA689_5_tau_mismatch",
            "component": "tau_source_clock_charge_orbit_boundary_mismatch",
            "zero_route": "prove one tau for source, clock, charge, orbit, and boundary readout",
            "attempt_result": "blocked_by_prior_tau_lock",
            "blocker": "684/685 leave tau roles separately normalized or conditional",
            "fallback_row": "CSI688_5_tau_mismatch",
            "priority": "6",
            "valid_for_claim": "false",
            "source_paths": source_list("684_tau_audit", "685_residual_template", "686_tau_residual"),
            "generated_utc": now,
        },
        {
            "audit_id": "ZTA689_6_stress_envelope",
            "component": "same_frame_T_H_envelope",
            "zero_route": "show stress contraction vanishes by symmetry/sign, or same-frame Hilbert stress is conserved with zero exchange",
            "attempt_result": "fail_current_corpus",
            "blocker": "Ward total conservation does not close mass-channel stress/exchange contraction",
            "fallback_row": "CSI688_6_stress_envelope",
            "priority": "7",
            "valid_for_claim": "false",
            "source_paths": source_list("455_contract", "686_identity", "688_num_den_map"),
            "generated_utc": now,
        },
        {
            "audit_id": "ZTA689_7_denominator",
            "component": "M_ref_candidate",
            "zero_route": "not a zero theorem; needs a same-frame claim-grade denominator",
            "attempt_result": "blocked_by_boundary_reference",
            "blocker": "boundary/reference status has no valid M_H_ref row",
            "fallback_row": "CSI688_7_denominator",
            "priority": "8",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "686_tau_residual", "688_num_den_map"),
            "generated_utc": now,
        },
        {
            "audit_id": "ZTA689_8_coefficients",
            "component": "component_norm_coefficients",
            "zero_route": "not a physical zero theorem; coefficients must be derived by norm choice or set by sourced convention",
            "attempt_result": "schema_required",
            "blocker": "component norm coefficients are not filled",
            "fallback_row": "CSI688_8_coefficients",
            "priority": "9",
            "valid_for_claim": "false",
            "source_paths": source_list("687_epsilon_contract", "688_input_template"),
            "generated_utc": now,
        },
    ]


def component_source_pack_rows() -> list[dict[str, str]]:
    now = generated_utc()
    components = [
        ("CSP689_0_theta", "theta_D_or_X_D", "B_trace", "zero_theorem_or_numeric_bound", "MISSING_THETA_D_OR_XD_SOURCE_BOUND", "highest", "142_doc;143_doc;603_doc"),
        ("CSP689_1_shear", "sigma_mu_nu", "B_shear", "zero_theorem_or_numeric_bound", "MISSING_SHEAR_SOURCE_BOUND", "highest", "132_doc;142_doc;143_doc;655_eh_audit"),
        ("CSP689_2_lapse", "a_mu_and_grad_lapse", "B_lapse", "gauge_safe_numeric_bound_or_clock_theorem", "MISSING_LAPSE_ACCELERATION_SOURCE_BOUND", "high", "155_doc;156_doc;684_tau_audit"),
        ("CSP689_3_shift", "shift_or_extrinsic_curvature", "B_shift", "ADM_convention_bound_or_stationary_exterior_theorem", "MISSING_SHIFT_EXTRINSIC_SOURCE_BOUND", "high", "655_eh_audit;688_decomposition"),
        ("CSP689_4_boundary", "boundary_velocity_and_reference_shift", "B_boundary", "boundary_no_flux_or_reference_shift_bound", "MISSING_BOUNDARY_MOTION_SOURCE_BOUND", "high", "143_doc;604_kernel_gate;boundary_reference_status"),
        ("CSP689_5_tau_mismatch", "tau_source_clock_charge_orbit_boundary_mismatch", "B_tau_mismatch", "same_tau_theorem_or_fractional_mismatch_bound", "MISSING_TAU_ROLE_MISMATCH_SOURCE_BOUND", "medium", "684_tau_audit;685_residual_template;686_tau_residual"),
        ("CSP689_6_stress", "same_frame_T_H_envelope", "stress_weight", "same_frame_stress_source_or_symmetry_contraction_zero", "MISSING_SAME_FRAME_STRESS_SOURCE_BOUND", "medium", "455_contract;686_identity"),
        ("CSP689_7_denominator", "M_ref_candidate", "denominator", "M_H_ref_or_nonclaim_M_ref_candidate", "MISSING_CLAIM_READY_M_REF_CANDIDATE", "highest", "boundary_reference_status;686_tau_residual"),
        ("CSP689_8_coefficients", "component_norm_coefficients", "C_i", "norm_coefficient_definition_or_sourced_conservative_choice", "MISSING_COMPONENT_NORM_COEFFICIENTS", "medium", "687_epsilon_contract;688_input_template"),
    ]
    rows = []
    for row_id, component, bound_symbol, required_evidence, current_status, priority, source_ids_text in components:
        source_ids = source_ids_text.split(";")
        rows.append(
            {
                "pack_id": row_id,
                "component": component,
                "bound_symbol": bound_symbol,
                "required_evidence": required_evidence,
                "minimum_columns": "system_id;domain_id;component_value;component_units;bound_source;source_file;assumptions;valid_for_claim",
                "current_status": current_status,
                "priority": priority,
                "allowed_zero_route": "parent_theorem_zero_only_no_closure_credit",
                "allowed_bound_route": "numeric_or_inequality_bound_with_units_source_path_and_same_frame_flag",
                "valid_for_claim": "false",
                "source_paths": source_list(*source_ids),
                "generated_utc": now,
            }
        )
    return rows


def runner_input_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "runner_id": "RIN689_0_component_envelope",
            "target_file": "P8_Y5_R10_689_COMPONENT_SOURCE_PACK.csv",
            "run_rule": "reject unless every component row is either theorem_zero with source path or numeric with units/source path",
            "current_status": "template_only_nonclaim",
            "failure_mode": "MISSING markers force epsilon_tau blocked",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "runner_id": "RIN689_1_numerator",
            "target_file": "future_P8_Y5_R10_EPSILON_TAU_NUMERATOR.csv",
            "run_rule": "compute or bound N_tau_nonstationary from stress-weighted component envelope only after same-frame stress exists",
            "current_status": "blocked_on_stress_and_components",
            "failure_mode": "no same-frame stress/source means no numerator",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "runner_id": "RIN689_2_denominator",
            "target_file": "future_P8_Y5_R10_EPSILON_TAU_DENOMINATOR.csv",
            "run_rule": "reject claim if denominator is not M_H_ref or a sourced same-frame nonclaim M_ref candidate",
            "current_status": "blocked_on_M_ref",
            "failure_mode": "dimensionless epsilon cannot be claim-grade",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "runner_id": "RIN689_3_claim_gate",
            "target_file": "future_P8_Y5_R10_EPSILON_TAU_CLAIM_EVALUATION.csv",
            "run_rule": "valid_for_claim=true only if no MISSING markers, all sources exist, units are compatible, and local arena mapping is explicit",
            "current_status": "schema_only_nonclaim",
            "failure_mode": "no local-GR/R10/PPN promotion",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "CG689_0_zero_theorems",
            "gate": "component zero-theorem pass",
            "required_state": "all physical symgrad components theorem-zero with source paths",
            "observed_state": "theta conditional; shear/lapse/shift/boundary/tau/stress/denominator not closed",
            "result": "fail_blocked",
            "claim_effect": "epsilon_nonstationary_tau cannot be set to zero",
            "valid_for_claim": "false",
            "source_paths": source_list("688_decomposition", "688_input_template"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG689_1_source_pack",
            "gate": "component source-pack readiness",
            "required_state": "all pack rows numeric or theorem-zero, units compatible, source-backed",
            "observed_state": "pack rows are template-only and carry MISSING status",
            "result": "staged_nonclaim",
            "claim_effect": "future executable path exists but current claim remains blocked",
            "valid_for_claim": "false",
            "source_paths": source_list("688_input_template"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG689_2_denominator",
            "gate": "same-frame denominator",
            "required_state": "M_H_ref or equivalent same-frame sourced denominator valid",
            "observed_state": "boundary/reference rows do not contain a claim-ready denominator",
            "result": "fail_blocked",
            "claim_effect": "no dimensionless epsilon_tau claim",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG689_3_local_claims",
            "gate": "R10/PPN/orbital/local-GR promotion",
            "required_state": "epsilon_tau, EH/R11, source-normalization, exchange, denominator all closed/scored",
            "observed_state": "component pack and denominator remain blocked",
            "result": "fail_policy",
            "claim_effect": "no M_H_ref, Qbar, R10, PPN, orbital, or local-GR pass",
            "valid_for_claim": "false",
            "source_paths": source_list("455_contract", "655_eh_audit", "688_num_den_map"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG689_4_next",
            "gate": "next target selection",
            "required_state": "choose first fill/zero theorem row",
            "observed_state": NEXT_TARGET,
            "result": "selected",
            "claim_effect": "attack trace/shear first because they are the core theta-not-Killing split",
            "valid_for_claim": "false",
            "source_paths": source_list("132_doc", "142_doc", "143_doc"),
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D689_0_zero_theorem",
            "target": "component zero theorem",
            "result": "failed_or_conditional",
            "reason": "only trace/selector silence is conditionally promising; full symgrad tau zero is not derived",
            "next_action": "do not claim Killing/local-GR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D689_1_source_pack",
            "target": "component source pack",
            "result": "written_nonclaim",
            "reason": "all future epsilon_tau work now has explicit rows, units, source-path, and same-frame requirements",
            "next_action": "fill or theorem-zero trace and shear first",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D689_2_next",
            "target": "trace/shear first",
            "result": "selected",
            "reason": "trace is the best theorem route and shear is the sharpest counterexample; resolving them narrows the branch fastest",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S689_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "component source pack is written; zero-theorem route fails or remains conditional; epsilon_tau remains blocked and nonclaim",
            "hardest_blocker": "trace/shear split plus denominator; theta silence is not shear silence",
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
    zero_rows: list[dict[str, str]],
    source_pack_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows_by_name = {
        "zero": zero_rows,
        "source_pack": source_pack_rows,
        "runner": runner_rows,
        "gates": gate_rows,
        "decision": decision_rows_,
        "summary": summary_rows,
    }
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_ids = ["655_validation", "684_validation", "685_validation", "686_validation", "687_validation", "688_validation"]
    prior_failure_counts = {source_id: len(validation_failures_for(source_id)) for source_id in prior_ids}
    zero_rows_complete = len(zero_rows) == 9 and all(row["valid_for_claim"] == "false" for row in zero_rows)
    zero_no_promotion = not any(row["attempt_result"] == "theorem_zero" for row in zero_rows)
    pack_complete = len(source_pack_rows) == 9 and all(row["valid_for_claim"] == "false" for row in source_pack_rows)
    pack_missing_markers = all("MISSING_" in row["current_status"] for row in source_pack_rows)
    runner_complete = len(runner_rows) == 4 and all(row["valid_for_claim"] == "false" for row in runner_rows)
    gates_block = all(row["valid_for_claim"] == "false" for row in gate_rows) and any(row["result"].startswith("fail") for row in gate_rows)
    no_claim_rows = all_valid_for_claim_false(rows_by_name)
    next_selected = any(row["next_action"] == NEXT_TARGET for row in decision_rows_)
    formalization_count = formalization_changed_count()
    output_paths = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_689_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_689_COMPONENT_ZERO_THEOREM_AUDIT.csv",
        RESIDUALS / "P8_Y5_R10_689_COMPONENT_SOURCE_PACK.csv",
        RESIDUALS / "P8_Y5_R10_689_RUNNER_INPUT_RULES.csv",
        RESIDUALS / "P8_Y5_R10_689_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_689_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_689_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_689_VALIDATION.csv",
    ]
    scoped_outputs = all(str(path).startswith(str(ROOT)) for path in output_paths)
    checks = [
        ("V689_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V689_1_prior_validations_clean", all(count == 0 for count in prior_failure_counts.values()), ";".join(f"{key}={value}" for key, value in prior_failure_counts.items())),
        ("V689_2_zero_theorem_audit_complete", zero_rows_complete, f"zero_rows={len(zero_rows)}"),
        ("V689_3_no_zero_theorem_promotion", zero_no_promotion, "no component marked theorem_zero"),
        ("V689_4_component_source_pack_complete", pack_complete, f"source_pack_rows={len(source_pack_rows)}"),
        ("V689_5_source_pack_missing_markers_retained", pack_missing_markers, "all pack rows retain MISSING markers"),
        ("V689_6_runner_input_rules_complete", runner_complete, f"runner_rows={len(runner_rows)}"),
        ("V689_7_claim_gates_block", gates_block, "claim gates keep epsilon_tau/M_H_ref/Qbar/R10/PPN/orbital/local_GR blocked"),
        ("V689_8_no_claim_rows_promoted", no_claim_rows, "all generated 689 rows remain valid_for_claim=false"),
        ("V689_9_next_target_selected", next_selected, NEXT_TARGET),
        ("V689_10_generated_outputs_scoped", scoped_outputs, "all 689 outputs target post-checkpoint-work"),
        ("V689_11_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V689_12_status_nonclaim", "no_epsilon_tau_claim" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
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
    zero_rows: list[dict[str, str]],
    source_pack_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    doc = f"""# 689 - Y5 R10 Symgrad Tau Component Source Pack Or Zero Theorem

## Verdict

689 tests the hard question after 688:

```text
Can any symgrad(tau) component be set to zero by theorem,
or must it be carried as a source-backed residual row?
```

Current answer: no component receives claim-grade theorem-zero credit.

The trace/selector piece is the best theorem route, but still conditional. Shear is the sharp counterexample: zero trace is not zero shear. Lapse/acceleration is gauge-dangerous unless clock coupling is parent-signed. Shift/extrinsic curvature needs a stationary observed exterior. Boundary motion and reference shift remain open. Tau-role mismatch is blocked by the tau-lock work. Stress weighting and denominator are still required before any dimensionless `epsilon_nonstationary_tau` value can be meaningful.

So 689 writes the component source pack and runner rules, but keeps every row nonclaim.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Component Zero Theorem Audit

{markdown_table(zero_rows, ["audit_id", "component", "attempt_result", "blocker", "fallback_row", "priority", "valid_for_claim"])}

## Component Source Pack

{markdown_table(source_pack_rows, ["pack_id", "component", "bound_symbol", "required_evidence", "current_status", "priority", "valid_for_claim"])}

## Runner Input Rules

{markdown_table(runner_rows, ["runner_id", "target_file", "run_rule", "current_status", "failure_mode", "valid_for_claim"])}

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
    zero_rows = zero_theorem_audit_rows()
    source_pack_rows = component_source_pack_rows()
    runner_rows = runner_input_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    summary_rows = nonclaim_summary_rows()
    validation_rows_ = validation_rows(source_rows, zero_rows, source_pack_rows, runner_rows, gate_rows, decision_rows_, summary_rows)

    write_csv(RESIDUALS / "P8_Y5_R10_689_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_689_COMPONENT_ZERO_THEOREM_AUDIT.csv", zero_rows, ["audit_id", "component", "zero_route", "attempt_result", "blocker", "fallback_row", "priority", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_689_COMPONENT_SOURCE_PACK.csv", source_pack_rows, ["pack_id", "component", "bound_symbol", "required_evidence", "minimum_columns", "current_status", "priority", "allowed_zero_route", "allowed_bound_route", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_689_RUNNER_INPUT_RULES.csv", runner_rows, ["runner_id", "target_file", "run_rule", "current_status", "failure_mode", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_689_CLAIM_GATE_EVALUATION.csv", gate_rows, ["gate_id", "gate", "required_state", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_689_DECISION.csv", decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_689_NONCLAIM_SUMMARY.csv", summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_689_VALIDATION.csv", validation_rows_, ["check_id", "result", "detail", "generated_utc"])

    write_doc(source_rows, zero_rows, source_pack_rows, runner_rows, gate_rows, decision_rows_, summary_rows, validation_rows_)

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"zero_rows={len(zero_rows)}")
    print(f"source_pack_rows={len(source_pack_rows)}")
    print(f"runner_rows={len(runner_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
