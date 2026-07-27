from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_parent_domain_selector_to_stationary_generator_attempt_failed_epsilon_tau_bound_contract_staged_nonclaim"
CLAIM_CEILING = "selector_to_tau_theorem_or_epsilon_tau_bound_contract_only_no_MH_ref_no_Qbar_no_R10_no_PPN_no_orbital_no_local_GR_claim"
NEXT_TARGET = "688-Y5-R10-symgrad-tau-kinematic-decomposition-bound-or-source-input-fill.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "687-Y5-R10-parent-domain-selector-to-stationary-generator-or-epsilon-tau-bound.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "455_doc": ROOT / "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
    "455_contract": RESIDUALS / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
    "602_doc": ROOT / "602-Y5-R10-bound-domain-selector-or-compact-shell-unit-map-fill.md",
    "602_validation": RESIDUALS / "P8_Y5_BRR545_602_VALIDATION.csv",
    "603_doc": ROOT / "603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md",
    "603_validation": RESIDUALS / "P8_Y5_BRR545_603_VALIDATION.csv",
    "603_nd_attempt": RESIDUALS / "P8_Y5_R10_603_ND_PRIMITIVE_DERIVATION_ATTEMPT.csv",
    "603_parent_gate": RESIDUALS / "P8_Y5_R10_603_PARENT_OWNERSHIP_GATE.csv",
    "603_zero_lemma": RESIDUALS / "P8_Y5_R10_603_ZERO_NONZERO_LEMMA.csv",
    "604_doc": ROOT / "604-Y5-R10-PMTS-boundary-kernel-block-or-unit-map-channel-fill.md",
    "604_validation": RESIDUALS / "P8_Y5_BRR545_604_VALIDATION.csv",
    "604_kernel_gate": RESIDUALS / "P8_Y5_R10_604_BOUNDARY_KERNEL_BLOCK_GATE.csv",
    "604_sector_theorem": RESIDUALS / "P8_Y5_R10_604_SECTOR_CHARGE_THEOREM_ATTEMPT.csv",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "655_validation": RESIDUALS / "P8_Y5_BRR545_655_VALIDATION.csv",
    "655_eh_audit": RESIDUALS / "P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv",
    "684_doc": ROOT / "684-Y5-R10-observed-frame-tau-coframe-lock-for-MH-ref.md",
    "684_validation": RESIDUALS / "P8_Y5_BRR545_684_VALIDATION.csv",
    "684_tau_audit": RESIDUALS / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
    "685_doc": ROOT / "685-Y5-R10-tau-generator-Killing-clock-lock-or-frame-residual-fill.md",
    "685_validation": RESIDUALS / "P8_Y5_BRR545_685_VALIDATION.csv",
    "685_residual_template": RESIDUALS / "P8_Y5_R10_685_TAU_FRAME_RESIDUAL_TEMPLATE.csv",
    "686_doc": ROOT / "686-Y5-R10-local-stationary-domain-Killing-certificate-or-tau-residual-row.md",
    "686_validation": RESIDUALS / "P8_Y5_BRR545_686_VALIDATION.csv",
    "686_certificate": RESIDUALS / "P8_Y5_R10_686_LOCAL_STATIONARY_CERTIFICATE.csv",
    "686_identity": RESIDUALS / "P8_Y5_R10_686_KILLING_IDENTITY_ATTEMPT.csv",
    "686_tau_residual": RESIDUALS / "P8_Y5_R10_686_NONSTATIONARY_TAU_RESIDUAL_ROW.csv",
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
        "455_doc": "Ward/Killing mass-current route",
        "455_contract": "stationary generator and residual fallback contract",
        "602_doc": "bound-domain selector theorem skeleton",
        "602_validation": "602 validation gate",
        "603_doc": "N_D/A_D activation primitive checkpoint",
        "603_validation": "603 validation gate",
        "603_nd_attempt": "N_D primitive candidate rows",
        "603_parent_gate": "N_D parent ownership blockers",
        "603_zero_lemma": "zero/nonzero activation lemma rows",
        "604_doc": "P_MTS kernel block checkpoint",
        "604_validation": "604 validation gate",
        "604_kernel_gate": "boundary kernel block gates",
        "604_sector_theorem": "sector charge theorem attempt",
        "655_doc": "EH/R11 exterior gate",
        "655_validation": "655 validation gate",
        "655_eh_audit": "EH-only premise audit",
        "684_doc": "tau/coframe lock checkpoint",
        "684_validation": "684 validation gate",
        "684_tau_audit": "tau role audit rows",
        "685_doc": "tau generator/Killing-clock lock checkpoint",
        "685_validation": "685 validation gate",
        "685_residual_template": "tau/frame residual templates",
        "686_doc": "local stationary/Killing certificate attempt",
        "686_validation": "686 validation gate",
        "686_certificate": "local stationary certificate rows",
        "686_identity": "Killing identity attempt rows",
        "686_tau_residual": "nonstationary tau residual rows",
        "boundary_reference_status": "M_H_ref status rows",
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


def selector_to_tau_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "step_id": "STT687_0_selector_activation",
            "object": "A_D=b_D c_D / N_D",
            "attempted_implication": "parent selector chooses the compact local inactive branch",
            "mathematical_form": "A_D=0 => chi_D=0 under the 602/603 selector action, if P_MTS,D, c_D, and normalization are parent-owned",
            "result": "conditional_selector_silence_only",
            "why_not_stationary": "A_D=0 controls selector/memory activation, not the full time derivative of g_obs",
            "residual_if_missing": "delta_tau_domain_selector",
            "valid_for_claim": "false",
            "source_paths": source_list("602_doc", "603_nd_attempt", "603_zero_lemma"),
            "generated_utc": now,
        },
        {
            "step_id": "STT687_1_kernel_block",
            "object": "P_MTS,D boundary kernel",
            "attempted_implication": "ordinary local baths cannot falsely activate or time-drive the MTS selector",
            "mathematical_form": "P_MTS,D=1_{q_MTS}(Q_sec), [K_B,Q_sec]=0 => K_cross=0",
            "result": "conditional_not_parent_derived",
            "why_not_stationary": "604 requires a parent sector charge Q_sec; without it the selector can be polluted or metric-dependent",
            "residual_if_missing": "projector_boundary_tau_leak",
            "valid_for_claim": "false",
            "source_paths": source_list("604_doc", "604_kernel_gate", "604_sector_theorem"),
            "generated_utc": now,
        },
        {
            "step_id": "STT687_2_volume_trace",
            "object": "X_D or theta_D",
            "attempted_implication": "inactive local branch has zero coherent volume expansion",
            "mathematical_form": "theta_D=<nabla_mu u^mu>_D=0 or X_D=0",
            "result": "not_derived_from_A_D_alone",
            "why_not_stationary": "603 separates A_D branch activation from J_C/X_D amplitude; A_D=0 does not prove X_D=0",
            "residual_if_missing": "theta_D_bound",
            "valid_for_claim": "false",
            "source_paths": source_list("603_nd_attempt", "603_parent_gate", "686_certificate"),
            "generated_utc": now,
        },
        {
            "step_id": "STT687_3_Killing_upgrade",
            "object": "symgrad(tau_obs)",
            "attempted_implication": "zero coherent scalar load upgrades to a Killing/stationary generator",
            "mathematical_form": "theta_D=0 ?=> nabla_(mu tau_{nu)}=0",
            "result": "counterexample_block",
            "why_not_stationary": "zero trace expansion does not kill shear, lapse/shift drift, radiation, boundary flux, or non-EH operator time dependence",
            "residual_if_missing": "epsilon_nonstationary_tau",
            "valid_for_claim": "false",
            "source_paths": source_list("686_identity", "655_eh_audit", "455_contract"),
            "generated_utc": now,
        },
        {
            "step_id": "STT687_4_tau_normalization",
            "object": "tau_obs",
            "attempted_implication": "domain-selected flow is the same source/clock/charge/orbit/boundary tau",
            "mathematical_form": "tau_D=tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary",
            "result": "blocked_by_tau_lock",
            "why_not_stationary": "domain labels and volume flow do not fix clock normalization or Hamiltonian boundary normalization",
            "residual_if_missing": "delta_tau_source_charge;delta_tau_clock_charge;Delta_ref_stationary_tau_over_Mref",
            "valid_for_claim": "false",
            "source_paths": source_list("684_tau_audit", "685_residual_template", "686_tau_residual"),
            "generated_utc": now,
        },
        {
            "step_id": "STT687_5_verdict",
            "object": "selector-to-stationary-generator theorem",
            "attempted_implication": "parent domain selector forces the local Killing branch",
            "mathematical_form": "A_D=0 + parent domain selection + exterior/stress/boundary silence => L_tau g_obs=0",
            "result": "failed_for_claim",
            "why_not_stationary": "the current corpus has selector silence targets, not a derived stationary observed generator",
            "residual_if_missing": "epsilon_tau_bound_contract_required",
            "valid_for_claim": "false",
            "source_paths": source_list("602_doc", "603_doc", "604_doc", "655_doc", "686_doc"),
            "generated_utc": now,
        },
    ]


def obstruction_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "obstruction_id": "OBS687_0_selector_not_geometry",
            "missing_bridge": "A_D=0 to L_tau g_obs=0",
            "counterexample": "a selector/memory scalar can be zero while a local metric has shear, lapse drift, or external tidal time dependence",
            "required_repair": "derive a parent theorem that the selected compact local branch is stationary in the observed metric",
            "current_status": "not_derived",
            "valid_for_claim": "false",
            "source_paths": source_list("603_zero_lemma", "686_certificate"),
            "generated_utc": now,
        },
        {
            "obstruction_id": "OBS687_1_trace_not_Killing",
            "missing_bridge": "theta_D=0 to symgrad(tau)=0",
            "counterexample": "vanishing expansion trace leaves shear and time-dependent shape modes legal",
            "required_repair": "kinematic decomposition plus zero theorem or sourced bounds for shear/lapse/shift pieces",
            "current_status": "residual_bound_needed",
            "valid_for_claim": "false",
            "source_paths": source_list("686_identity", "686_tau_residual"),
            "generated_utc": now,
        },
        {
            "obstruction_id": "OBS687_2_domain_not_clock",
            "missing_bridge": "domain flow to observed clock/Hamiltonian tau",
            "counterexample": "a comoving domain parameter can be rescaled without fixing clock or Hamiltonian charge normalization",
            "required_repair": "same tau normalization theorem tying e_obs clocks, H_tau, source current, orbit readout, and boundary reference",
            "current_status": "blocked_by_684_685",
            "valid_for_claim": "false",
            "source_paths": source_list("684_tau_audit", "685_residual_template"),
            "generated_utc": now,
        },
        {
            "obstruction_id": "OBS687_3_exterior_operator_open",
            "missing_bridge": "selected local branch to EH stationary exterior",
            "counterexample": "non-EH/R11 operators can preserve a selector zero while sourcing time-dependent or preferred-frame residuals",
            "required_repair": "EH-only theorem-zero or executable R11 coefficient vector with weak-field/time-dependence maps",
            "current_status": "blocked_by_655",
            "valid_for_claim": "false",
            "source_paths": source_list("655_doc", "655_eh_audit"),
            "generated_utc": now,
        },
        {
            "obstruction_id": "OBS687_4_exchange_and_boundary_flux",
            "missing_bridge": "stationary-looking local branch to closed mass current",
            "counterexample": "hidden/projector/boundary/coupling exchange can keep d(Pi_M J_H) nonzero even if a scalar selector is inactive",
            "required_repair": "zero Pi_M projection of all retained exchange terms or explicit residual coefficients",
            "current_status": "not_parent_derived",
            "valid_for_claim": "false",
            "source_paths": source_list("455_contract", "604_kernel_gate"),
            "generated_utc": now,
        },
        {
            "obstruction_id": "OBS687_5_denominator_open",
            "missing_bridge": "epsilon_tau numerator to claim-grade dimensionless bound",
            "counterexample": "without M_H_ref or a same-frame M_ref candidate, a small-looking numerator has no claim-grade normalization",
            "required_repair": "M_H_ref denominator closure or explicitly nonclaim reference-mass candidate with units and source path",
            "current_status": "blocked_by_boundary_reference",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "686_tau_residual"),
            "generated_utc": now,
        },
    ]


def epsilon_tau_bound_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "bound_id": "ETB687_0_exact_numerator",
            "quantity": "N_tau_nonstationary",
            "definition": "abs(int_V T_H^{mu nu} nabla_(mu tau_nu) dV_tau)",
            "bound_form": "must be evaluated in the same observed frame as J_H[tau] and H_tau",
            "required_inputs": "T_H_source;symgrad_tau_source;domain_volume_or_surface_rule;units;source_path",
            "current_status": "MISSING_SYMGRAD_TAU_AND_STRESS_SOURCE",
            "claim_use": "numerator only; not claim-grade without denominator",
            "valid_for_claim": "false",
            "source_paths": source_list("686_identity", "686_tau_residual"),
            "generated_utc": now,
        },
        {
            "bound_id": "ETB687_1_kinematic_decomposition",
            "quantity": "nabla_(mu tau_nu)",
            "definition": "schematic split into expansion trace, shear, lapse/acceleration, shift/extrinsic-curvature, and boundary-motion pieces",
            "bound_form": "|symgrad tau| <= C_theta|theta_D| + C_sigma|sigma_D| + C_lapse|grad N| + C_shift|K_shift| + C_boundary|v_boundary|",
            "required_inputs": "theta_D_bound;sigma_D_bound;lapse_bound;shift_or_extrinsic_curvature_bound;boundary_motion_bound;C_i;units;source_path",
            "current_status": "MISSING_KINEMATIC_DECOMPOSITION_IN_MTS_OBSERVED_FRAME",
            "claim_use": "turns failed Killing theorem into sourceable residual envelope",
            "valid_for_claim": "false",
            "source_paths": source_list("686_tau_residual", "685_residual_template"),
            "generated_utc": now,
        },
        {
            "bound_id": "ETB687_2_selector_contribution",
            "quantity": "delta_tau_domain_selector",
            "definition": "fractional mismatch between selector/domain flow and observed tau",
            "bound_form": "|delta_tau_domain_selector| <= C_A |delta A_D| + C_kernel |K_cross| + C_norm |delta normalization|",
            "required_inputs": "A_D_source;P_MTS_kernel_source;normalization_source;C_A;C_kernel;C_norm;units;source_path",
            "current_status": "MISSING_PARENT_SELECTOR_TO_TAU_MAP",
            "claim_use": "keeps domain selector failure separate from metric nonstationarity",
            "valid_for_claim": "false",
            "source_paths": source_list("603_parent_gate", "604_kernel_gate", "686_tau_residual"),
            "generated_utc": now,
        },
        {
            "bound_id": "ETB687_3_dimensionless_epsilon",
            "quantity": "epsilon_nonstationary_tau",
            "definition": "N_tau_nonstationary divided by a same-frame mass/energy denominator",
            "bound_form": "epsilon_nonstationary_tau <= N_tau_bound / M_ref_candidate",
            "required_inputs": "N_tau_bound;M_ref_candidate;same_frame_units;denominator_source;valid_denominator_flag",
            "current_status": "MISSING_CLAIM_READY_M_REF_CANDIDATE",
            "claim_use": "nonclaim until M_H_ref or a sourced denominator is valid",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "686_tau_residual"),
            "generated_utc": now,
        },
        {
            "bound_id": "ETB687_4_acceptance_rule",
            "quantity": "future epsilon_tau row",
            "definition": "claim gate for any future source-backed epsilon_tau value",
            "bound_form": "valid_for_claim=true only if all inputs numeric, same-frame, source-backed, units-compatible, denominator-valid, and no MISSING markers remain",
            "required_inputs": "numeric_values;source_paths;units;assumptions;denominator_gate;local_arena_mapping",
            "current_status": "SCHEMA_ONLY_NONCLAIM",
            "claim_use": "prevents a closure value being mistaken for local-GR evidence",
            "valid_for_claim": "false",
            "source_paths": source_list("686_tau_residual", "685_residual_template", "455_contract"),
            "generated_utc": now,
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "CG687_0_selector_to_tau",
            "gate": "parent selector-to-stationary tau theorem",
            "required_state": "A_D/N_D parent-owned and shown to force L_tau g_obs=0 in the observed local exterior",
            "observed_state": "selector silence is conditional and weaker than Killing stationarity",
            "result": "fail_blocked",
            "claim_effect": "do not zero epsilon_nonstationary_tau",
            "valid_for_claim": "false",
            "source_paths": source_list("603_doc", "686_certificate"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG687_1_epsilon_bound",
            "gate": "epsilon tau bound",
            "required_state": "numeric same-frame numerator, kinematic decomposition, and denominator source",
            "observed_state": "schema only with MISSING inputs",
            "result": "staged_nonclaim",
            "claim_effect": "future source-backed fallback path exists",
            "valid_for_claim": "false",
            "source_paths": source_list("686_tau_residual", "boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG687_2_MH_ref_Qbar",
            "gate": "M_H_ref/Qbar promotion",
            "required_state": "tau lock, fixed reference, denominator, and stationarity residual closed",
            "observed_state": "tau/stationarity/reference gates remain blocked",
            "result": "fail_policy",
            "claim_effect": "no M_H_ref or Qbar row promoted",
            "valid_for_claim": "false",
            "source_paths": source_list("684_doc", "685_doc", "686_doc"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG687_3_local_GR",
            "gate": "R10/PPN/orbital/local-GR claim",
            "required_state": "all local residuals theorem-zero or source-backed and scored",
            "observed_state": "epsilon_tau, R11, source-normalization, and exchange rows remain open",
            "result": "fail_policy",
            "claim_effect": "no R10, PPN, orbital, or local-GR pass",
            "valid_for_claim": "false",
            "source_paths": source_list("455_contract", "655_eh_audit", "686_certificate"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG687_4_next",
            "gate": "next target selection",
            "required_state": "choose derivation or source-fill step after selector-to-Killing failure",
            "observed_state": NEXT_TARGET,
            "result": "selected",
            "claim_effect": "derive the symgrad-tau bound contract before scoring",
            "valid_for_claim": "false",
            "source_paths": source_list("686_tau_residual"),
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D687_0_theorem_attempt",
            "target": "domain selector to stationary generator",
            "result": "failed_for_claim",
            "reason": "A_D/N_D can at best silence selector-memory activation; it does not derive full observed Killing stationarity",
            "next_action": "do not promote local stationary certificate",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D687_1_bound_contract",
            "target": "epsilon_nonstationary_tau",
            "result": "bound_contract_staged",
            "reason": "the missing theorem has been converted into a sourceable symgrad-tau/stress/denominator bound",
            "next_action": "derive kinematic decomposition and required source columns",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D687_2_next",
            "target": "symgrad tau decomposition",
            "result": "selected",
            "reason": "this is the least circular next step: bound the exact obstruction before any local-GR scoring",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S687_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "Selector-to-Killing proof fails cleanly: A_D/N_D silence is not full stationarity. A sourceable epsilon_tau bound contract is staged.",
            "hardest_blocker": "derive or bound symgrad(tau_obs) in the same observed frame with a valid denominator",
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
    selector_rows: list[dict[str, str]],
    obstruction_rows_: list[dict[str, str]],
    epsilon_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows_by_name = {
        "selector": selector_rows,
        "obstruction": obstruction_rows_,
        "epsilon": epsilon_rows,
        "gates": gate_rows,
        "decision": decision_rows_,
        "summary": summary_rows,
    }
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_ids = ["602_validation", "603_validation", "604_validation", "655_validation", "684_validation", "685_validation", "686_validation"]
    prior_failure_counts = {source_id: len(validation_failures_for(source_id)) for source_id in prior_ids}
    selector_fails_cleanly = any(row["result"] == "failed_for_claim" for row in selector_rows) and all(
        row["valid_for_claim"] == "false" for row in selector_rows
    )
    obstruction_complete = len(obstruction_rows_) == 6 and all(row["valid_for_claim"] == "false" for row in obstruction_rows_)
    epsilon_contract_complete = len(epsilon_rows) == 5 and all(row["valid_for_claim"] == "false" for row in epsilon_rows)
    missing_markers = all("MISSING_" in row["current_status"] or row["current_status"] == "SCHEMA_ONLY_NONCLAIM" for row in epsilon_rows)
    gates_block = all(row["valid_for_claim"] == "false" for row in gate_rows) and any(row["result"].startswith("fail") for row in gate_rows)
    no_claim_rows = all_valid_for_claim_false(rows_by_name)
    next_selected = any(row["next_action"] == NEXT_TARGET for row in decision_rows_)
    formalization_count = formalization_changed_count()
    output_paths = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_687_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_687_SELECTOR_TO_TAU_THEOREM_ATTEMPT.csv",
        RESIDUALS / "P8_Y5_R10_687_STATIONARITY_OBSTRUCTION_LEDGER.csv",
        RESIDUALS / "P8_Y5_R10_687_EPSILON_TAU_BOUND_CONTRACT.csv",
        RESIDUALS / "P8_Y5_R10_687_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_687_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_687_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_687_VALIDATION.csv",
    ]
    scoped_outputs = all(str(path).startswith(str(ROOT)) for path in output_paths)
    checks = [
        (
            "V687_0_source_paths_exist",
            not missing_sources,
            "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources),
        ),
        (
            "V687_1_prior_validations_clean",
            all(count == 0 for count in prior_failure_counts.values()),
            ";".join(f"{key}={value}" for key, value in prior_failure_counts.items()),
        ),
        (
            "V687_2_selector_attempt_complete",
            len(selector_rows) == 6,
            f"selector_rows={len(selector_rows)}",
        ),
        (
            "V687_3_selector_to_Killing_not_overclaimed",
            selector_fails_cleanly,
            "selector-to-Killing theorem fails and all rows remain nonclaim",
        ),
        (
            "V687_4_obstruction_ledger_complete",
            obstruction_complete,
            f"obstruction_rows={len(obstruction_rows_)}",
        ),
        (
            "V687_5_epsilon_tau_bound_contract_complete",
            epsilon_contract_complete,
            f"epsilon_rows={len(epsilon_rows)}",
        ),
        (
            "V687_6_missing_markers_retained",
            missing_markers,
            "epsilon bound contract still carries required MISSING markers",
        ),
        (
            "V687_7_claim_gates_block",
            gates_block,
            "claim gates keep M_H_ref/Qbar/R10/PPN/orbital/local_GR blocked",
        ),
        (
            "V687_8_no_claim_rows_promoted",
            no_claim_rows,
            "all generated 687 rows remain valid_for_claim=false",
        ),
        (
            "V687_9_next_target_selected",
            next_selected,
            NEXT_TARGET,
        ),
        (
            "V687_10_generated_outputs_scoped",
            scoped_outputs,
            "all 687 outputs target post-checkpoint-work",
        ),
        (
            "V687_11_formalization_workbench_untouched",
            formalization_count == 0,
            f"formalization_changed_after_cutoff={formalization_count}",
        ),
        (
            "V687_12_status_nonclaim",
            "no_MH_ref" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING,
            CLAIM_CEILING,
        ),
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
    selector_rows: list[dict[str, str]],
    obstruction_rows_: list[dict[str, str]],
    epsilon_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    doc = f"""# 687 - Y5 R10 Parent Domain Selector To Stationary Generator Or Epsilon Tau Bound

## Verdict

687 tried to make the local-domain selector do the missing heavy lifting:

```text
A_D = b_D c_D
A_D = 0  ->  chi_D = 0
chi_D = 0 -> selector/memory stress silence
```

That part is useful, but it is not the same as:

```text
L_tau g_obs = 0
nabla_(mu tau_nu) = 0
```

So the selector route does not yet derive the local stationary/Killing generator. `A_D/N_D` can be a clean branch-activation primitive, but selector silence is weaker than full observed stationarity. Zero trace/volume-flow would still not kill shear, lapse/shift drift, boundary motion, exchange flux, or non-EH operator time dependence.

The honest result is therefore a bound contract: if we cannot prove `symgrad(tau_obs)=0`, we must bound `epsilon_nonstationary_tau` from same-frame stress, symgrad-tau, kinematic pieces, and a valid denominator. No claim is promoted.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Selector To Tau Theorem Attempt

{markdown_table(selector_rows, ["step_id", "object", "attempted_implication", "result", "why_not_stationary", "residual_if_missing", "valid_for_claim"])}

## Stationarity Obstruction Ledger

{markdown_table(obstruction_rows_, ["obstruction_id", "missing_bridge", "counterexample", "required_repair", "current_status", "valid_for_claim"])}

## Epsilon Tau Bound Contract

{markdown_table(epsilon_rows, ["bound_id", "quantity", "definition", "bound_form", "current_status", "claim_use", "valid_for_claim"])}

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
    selector_rows = selector_to_tau_rows()
    obstruction_rows_ = obstruction_rows()
    epsilon_rows = epsilon_tau_bound_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    summary_rows = nonclaim_summary_rows()
    validation_rows_ = validation_rows(
        source_rows,
        selector_rows,
        obstruction_rows_,
        epsilon_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
    )

    write_csv(RESIDUALS / "P8_Y5_R10_687_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_687_SELECTOR_TO_TAU_THEOREM_ATTEMPT.csv", selector_rows, ["step_id", "object", "attempted_implication", "mathematical_form", "result", "why_not_stationary", "residual_if_missing", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_687_STATIONARITY_OBSTRUCTION_LEDGER.csv", obstruction_rows_, ["obstruction_id", "missing_bridge", "counterexample", "required_repair", "current_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_687_EPSILON_TAU_BOUND_CONTRACT.csv", epsilon_rows, ["bound_id", "quantity", "definition", "bound_form", "required_inputs", "current_status", "claim_use", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_687_CLAIM_GATE_EVALUATION.csv", gate_rows, ["gate_id", "gate", "required_state", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_687_DECISION.csv", decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_687_NONCLAIM_SUMMARY.csv", summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_687_VALIDATION.csv", validation_rows_, ["check_id", "result", "detail", "generated_utc"])

    write_doc(
        source_rows,
        selector_rows,
        obstruction_rows_,
        epsilon_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
        validation_rows_,
    )

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"selector_rows={len(selector_rows)}")
    print(f"obstruction_rows={len(obstruction_rows_)}")
    print(f"epsilon_rows={len(epsilon_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
