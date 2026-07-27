from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_symgrad_tau_kinematic_decomposition_written_component_source_rows_staged_nonclaim"
CLAIM_CEILING = "symgrad_tau_decomposition_and_source_input_contract_only_no_MH_ref_no_Qbar_no_R10_no_PPN_no_orbital_no_local_GR_claim"
NEXT_TARGET = "689-Y5-R10-symgrad-tau-component-source-pack-or-zero-theorem.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "688-Y5-R10-symgrad-tau-kinematic-decomposition-bound-or-source-input-fill.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "132_doc": ROOT / "132-smooth-memory-growth-theorem-attempt.md",
    "142_doc": ROOT / "142-domain-load-tensor-owner-promotion-gate.md",
    "143_doc": ROOT / "143-domain-selector-variational-action-attempt.md",
    "155_doc": ROOT / "155-redshift-projection-clock-map-owner.md",
    "156_doc": ROOT / "156-clock-projection-functional-theorem-or-demotion.md",
    "455_doc": ROOT / "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
    "455_contract": RESIDUALS / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
    "603_doc": ROOT / "603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md",
    "603_validation": RESIDUALS / "P8_Y5_BRR545_603_VALIDATION.csv",
    "603_nd_attempt": RESIDUALS / "P8_Y5_R10_603_ND_PRIMITIVE_DERIVATION_ATTEMPT.csv",
    "604_doc": ROOT / "604-Y5-R10-PMTS-boundary-kernel-block-or-unit-map-channel-fill.md",
    "604_validation": RESIDUALS / "P8_Y5_BRR545_604_VALIDATION.csv",
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
    "687_doc": ROOT / "687-Y5-R10-parent-domain-selector-to-stationary-generator-or-epsilon-tau-bound.md",
    "687_validation": RESIDUALS / "P8_Y5_BRR545_687_VALIDATION.csv",
    "687_epsilon_contract": RESIDUALS / "P8_Y5_R10_687_EPSILON_TAU_BOUND_CONTRACT.csv",
    "687_obstruction": RESIDUALS / "P8_Y5_R10_687_STATIONARITY_OBSTRUCTION_LEDGER.csv",
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
        "132_doc": "theta/shear/vorticity coherence invariant and gauge warning",
        "142_doc": "domain load tensor and trace/shear local-silence warnings",
        "143_doc": "domain selector stress and dynamic local safety warning",
        "155_doc": "clock/lapse gauge warning",
        "156_doc": "clock functional and gauge-safety target",
        "455_doc": "Ward/Killing mass-current route",
        "455_contract": "mass-current closure and retained residual fallback",
        "603_doc": "A_D/N_D activation primitive checkpoint",
        "603_validation": "603 validation gate",
        "603_nd_attempt": "A_D, X_D, J_C primitive rows",
        "604_doc": "P_MTS boundary kernel checkpoint",
        "604_validation": "604 validation gate",
        "604_kernel_gate": "boundary kernel block gate",
        "655_doc": "EH/R11 exterior gate",
        "655_validation": "655 validation gate",
        "655_eh_audit": "EH-only premise audit",
        "684_validation": "684 validation gate",
        "684_tau_audit": "tau role audit",
        "685_validation": "685 validation gate",
        "685_residual_template": "tau/frame residual templates",
        "686_validation": "686 validation gate",
        "686_identity": "Killing identity attempt",
        "686_tau_residual": "nonstationary tau residual rows",
        "687_doc": "selector-to-stationary generator predecessor",
        "687_validation": "687 validation gate",
        "687_epsilon_contract": "epsilon tau bound contract",
        "687_obstruction": "stationarity obstruction ledger",
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


def symgrad_decomposition_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "component_id": "SGT688_0_exact_congruence_identity",
            "component": "symgrad_tau",
            "decomposition": "for normalized u, nabla_(mu u_nu)=sigma_mu_nu+(theta/3)h_mu_nu-u_(mu a_nu); vorticity drops from the symmetric part",
            "bound_role": "exact kinematic split of the Killing obstruction",
            "theorem_zero_status": "identity_only_not_zero",
            "missing_for_claim": "MISSING_PARENT_SELECTED_NORMALIZED_TAU_AND_COMPONENT_ZERO_THEOREMS",
            "valid_for_claim": "false",
            "source_paths": source_list("686_identity", "687_epsilon_contract"),
            "generated_utc": now,
        },
        {
            "component_id": "SGT688_1_trace_expansion",
            "component": "theta_D_or_X_D",
            "decomposition": "trace piece: (theta/3)h_mu_nu; domain average maps to X_D or coherent volume-flow scalar when D and P_coh are fixed",
            "bound_role": "selector/domain route can at most target this scalar piece first",
            "theorem_zero_status": "conditional_only",
            "missing_for_claim": "MISSING_PARENT_DOMAIN_SELECTION_AND_XD_ZERO_SOURCE",
            "valid_for_claim": "false",
            "source_paths": source_list("132_doc", "142_doc", "143_doc", "603_nd_attempt"),
            "generated_utc": now,
        },
        {
            "component_id": "SGT688_2_shear",
            "component": "sigma_mu_nu",
            "decomposition": "tracefree symmetric piece of nabla u; zero trace/selector silence does not remove it",
            "bound_role": "dominant counterexample to theta_D=0 implying Killing",
            "theorem_zero_status": "not_derived",
            "missing_for_claim": "MISSING_SHEAR_ZERO_THEOREM_OR_BOUND",
            "valid_for_claim": "false",
            "source_paths": source_list("132_doc", "142_doc", "143_doc", "687_obstruction"),
            "generated_utc": now,
        },
        {
            "component_id": "SGT688_3_lapse_acceleration",
            "component": "a_mu_and_grad_lapse",
            "decomposition": "for tau=N u, symgrad(tau) contains N a_mu terms plus u_(mu grad_{nu)}N/lapse-normalization pieces",
            "bound_role": "separates physical clock/lapse gradients from gauge rescaling",
            "theorem_zero_status": "not_derived",
            "missing_for_claim": "MISSING_LAPSE_ACCELERATION_GAUGE_SAFE_BOUND",
            "valid_for_claim": "false",
            "source_paths": source_list("155_doc", "156_doc", "684_tau_audit", "685_residual_template"),
            "generated_utc": now,
        },
        {
            "component_id": "SGT688_4_shift_extrinsic",
            "component": "shift_or_extrinsic_curvature",
            "decomposition": "ADM-style spatial metric stationarity requires partial_t h_ij=0, equivalently a convention-dependent relation between K_ij, lapse, and D_(i beta_j)",
            "bound_role": "captures time-dependent spatial geometry not seen by scalar volume trace alone",
            "theorem_zero_status": "not_derived",
            "missing_for_claim": "MISSING_SHIFT_EXTRINSIC_CURVATURE_BOUND",
            "valid_for_claim": "false",
            "source_paths": source_list("687_obstruction", "655_eh_audit"),
            "generated_utc": now,
        },
        {
            "component_id": "SGT688_5_boundary_motion",
            "component": "boundary_velocity_and_flux",
            "decomposition": "domain-boundary motion and reference-class drift can add apparent nonstationarity even if interior trace is quiet",
            "bound_role": "prevents comoving-domain silence being confused with boundary/Hamiltonian silence",
            "theorem_zero_status": "not_derived",
            "missing_for_claim": "MISSING_BOUNDARY_MOTION_AND_REFERENCE_SHIFT_BOUND",
            "valid_for_claim": "false",
            "source_paths": source_list("143_doc", "604_kernel_gate", "boundary_reference_status", "687_obstruction"),
            "generated_utc": now,
        },
        {
            "component_id": "SGT688_6_tau_role_mismatch",
            "component": "tau_source_clock_charge_orbit_boundary_mismatch",
            "decomposition": "different tau choices for source, clock, charge, orbit, or boundary act like a residual even if one chosen flow is stationary",
            "bound_role": "keeps normalization/gauge errors out of the Killing proof",
            "theorem_zero_status": "blocked_by_684_685",
            "missing_for_claim": "MISSING_SAME_TAU_NORMALIZATION_THEOREM",
            "valid_for_claim": "false",
            "source_paths": source_list("684_tau_audit", "685_residual_template", "686_tau_residual"),
            "generated_utc": now,
        },
        {
            "component_id": "SGT688_7_stress_contraction",
            "component": "T_H_symgrad_tau_contraction",
            "decomposition": "the physical numerator is not |symgrad tau| alone but the same-frame contraction int T_H^{mu nu} symgrad(tau)_{mu nu}",
            "bound_role": "requires a stress envelope/source and same-frame integration rule",
            "theorem_zero_status": "not_derived",
            "missing_for_claim": "MISSING_SAME_FRAME_STRESS_ENVELOPE_AND_INTEGRATION_RULE",
            "valid_for_claim": "false",
            "source_paths": source_list("455_contract", "686_identity", "687_epsilon_contract"),
            "generated_utc": now,
        },
        {
            "component_id": "SGT688_8_verdict",
            "component": "epsilon_nonstationary_tau",
            "decomposition": "epsilon_tau must be bounded from trace, shear, lapse, shift/extrinsic, boundary, tau-mismatch, stress, and denominator inputs",
            "bound_role": "turns failed Killing theorem into executable source-input problem",
            "theorem_zero_status": "source_input_required_nonclaim",
            "missing_for_claim": "MISSING_ALL_COMPONENT_SOURCE_PACK_OR_ZERO_THEOREMS",
            "valid_for_claim": "false",
            "source_paths": source_list("686_tau_residual", "687_epsilon_contract"),
            "generated_utc": now,
        },
    ]


def component_input_rows() -> list[dict[str, str]]:
    now = generated_utc()
    base_columns = "system_id;domain_id;component_value;component_units;bound_source;source_file;assumptions;valid_for_claim"
    return [
        {
            "input_id": "CSI688_0_theta",
            "component": "theta_D_or_X_D",
            "required_columns": base_columns + ";theta_definition;averaging_rule",
            "current_status": "MISSING_THETA_D_OR_XD_SOURCE_BOUND",
            "units": "1/time or dimensionless after selected normalization",
            "feeds_bound": "B_trace",
            "valid_for_claim": "false",
            "source_paths": source_list("132_doc", "142_doc", "603_nd_attempt"),
            "generated_utc": now,
        },
        {
            "input_id": "CSI688_1_shear",
            "component": "sigma_mu_nu",
            "required_columns": base_columns + ";shear_norm_definition;projection_rule",
            "current_status": "MISSING_SHEAR_SOURCE_BOUND",
            "units": "1/time or dimensionless after selected normalization",
            "feeds_bound": "B_shear",
            "valid_for_claim": "false",
            "source_paths": source_list("132_doc", "142_doc", "143_doc"),
            "generated_utc": now,
        },
        {
            "input_id": "CSI688_2_lapse_acceleration",
            "component": "a_mu_and_grad_lapse",
            "required_columns": base_columns + ";lapse_rule;clock_coupling_rule;gauge_safety_flag",
            "current_status": "MISSING_LAPSE_ACCELERATION_SOURCE_BOUND",
            "units": "1/time or dimensionless after selected normalization",
            "feeds_bound": "B_lapse",
            "valid_for_claim": "false",
            "source_paths": source_list("155_doc", "156_doc", "685_residual_template"),
            "generated_utc": now,
        },
        {
            "input_id": "CSI688_3_shift_extrinsic",
            "component": "shift_or_extrinsic_curvature",
            "required_columns": base_columns + ";Kij_or_shift_definition;ADM_convention;stationarity_rule",
            "current_status": "MISSING_SHIFT_EXTRINSIC_SOURCE_BOUND",
            "units": "1/time or dimensionless after selected normalization",
            "feeds_bound": "B_shift",
            "valid_for_claim": "false",
            "source_paths": source_list("655_eh_audit", "687_obstruction"),
            "generated_utc": now,
        },
        {
            "input_id": "CSI688_4_boundary_motion",
            "component": "boundary_velocity_and_reference_shift",
            "required_columns": base_columns + ";boundary_class;boundary_velocity_rule;reference_shift_rule",
            "current_status": "MISSING_BOUNDARY_MOTION_SOURCE_BOUND",
            "units": "dimensionless or same-frame energy fraction after denominator",
            "feeds_bound": "B_boundary",
            "valid_for_claim": "false",
            "source_paths": source_list("143_doc", "604_kernel_gate", "boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "input_id": "CSI688_5_tau_mismatch",
            "component": "tau_source_clock_charge_orbit_boundary_mismatch",
            "required_columns": base_columns + ";tau_source;tau_clock;tau_charge;tau_orbit;tau_boundary;mismatch_norm",
            "current_status": "MISSING_TAU_ROLE_MISMATCH_SOURCE_BOUND",
            "units": "dimensionless fractional mismatch",
            "feeds_bound": "B_tau_mismatch",
            "valid_for_claim": "false",
            "source_paths": source_list("684_tau_audit", "685_residual_template", "686_tau_residual"),
            "generated_utc": now,
        },
        {
            "input_id": "CSI688_6_stress_envelope",
            "component": "same_frame_T_H_envelope",
            "required_columns": base_columns + ";stress_norm;matter_source;same_frame_flag;integration_domain",
            "current_status": "MISSING_SAME_FRAME_STRESS_SOURCE_BOUND",
            "units": "energy density, mass density, or integrated mass/energy units with source convention",
            "feeds_bound": "N_tau_nonstationary",
            "valid_for_claim": "false",
            "source_paths": source_list("455_contract", "686_identity", "687_epsilon_contract"),
            "generated_utc": now,
        },
        {
            "input_id": "CSI688_7_denominator",
            "component": "M_ref_candidate",
            "required_columns": "system_id;M_ref_candidate;M_ref_units;denominator_type;source_file;same_frame_flag;valid_denominator_flag;valid_for_claim",
            "current_status": "MISSING_CLAIM_READY_M_REF_CANDIDATE",
            "units": "same mass/energy units as numerator",
            "feeds_bound": "epsilon_nonstationary_tau",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "686_tau_residual"),
            "generated_utc": now,
        },
        {
            "input_id": "CSI688_8_coefficients",
            "component": "component_norm_coefficients",
            "required_columns": "component;coefficient_symbol;coefficient_value;units;norm_definition;source_file;assumptions;valid_for_claim",
            "current_status": "MISSING_COMPONENT_NORM_COEFFICIENTS",
            "units": "dimensionless unless norm conversion requires units",
            "feeds_bound": "B_symgrad_tau",
            "valid_for_claim": "false",
            "source_paths": source_list("687_epsilon_contract"),
            "generated_utc": now,
        },
    ]


def numerator_denominator_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "map_id": "NDM688_0_component_envelope",
            "quantity": "B_symgrad_tau",
            "formula": "B_symgrad_tau <= C_theta B_trace + C_sigma B_shear + C_lapse B_lapse + C_shift B_shift + C_boundary B_boundary + C_tau B_tau_mismatch",
            "required_inputs": "CSI688_0;CSI688_1;CSI688_2;CSI688_3;CSI688_4;CSI688_5;CSI688_8",
            "current_status": "MISSING_COMPONENT_BOUNDS_AND_COEFFICIENTS",
            "valid_for_claim": "false",
            "source_paths": source_list("687_epsilon_contract"),
            "generated_utc": now,
        },
        {
            "map_id": "NDM688_1_stress_weighted_numerator",
            "quantity": "N_tau_nonstationary",
            "formula": "N_tau_nonstationary <= integral_D ||T_H||_obs ||symgrad_tau||_obs dV_tau or a sharper signed contraction if sourced",
            "required_inputs": "CSI688_6;B_symgrad_tau;integration_domain;same_frame_units",
            "current_status": "MISSING_STRESS_ENVELOPE_AND_INTEGRATION_RULE",
            "valid_for_claim": "false",
            "source_paths": source_list("455_contract", "686_identity", "687_epsilon_contract"),
            "generated_utc": now,
        },
        {
            "map_id": "NDM688_2_dimensionless_epsilon",
            "quantity": "epsilon_nonstationary_tau",
            "formula": "epsilon_nonstationary_tau <= N_tau_nonstationary / M_ref_candidate",
            "required_inputs": "N_tau_nonstationary;CSI688_7",
            "current_status": "MISSING_CLAIM_READY_DENOMINATOR",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "686_tau_residual"),
            "generated_utc": now,
        },
        {
            "map_id": "NDM688_3_claim_acceptance",
            "quantity": "future_epsilon_tau_claim_row",
            "formula": "valid_for_claim=true only if every component is theorem-zero or numeric/source-backed, same-frame, units-compatible, and denominator-valid",
            "required_inputs": "all CSI688 rows;all NDM688 rows;no MISSING markers",
            "current_status": "SCHEMA_ONLY_NONCLAIM",
            "valid_for_claim": "false",
            "source_paths": source_list("687_epsilon_contract", "685_residual_template"),
            "generated_utc": now,
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "CG688_0_Killing_zero",
            "gate": "symgrad tau theorem-zero",
            "required_state": "trace, shear, lapse, shift/extrinsic, boundary, and tau-role mismatch all vanish by parent theorem",
            "observed_state": "identity/decomposition only; component zeros not derived",
            "result": "fail_blocked",
            "claim_effect": "do not set epsilon_nonstationary_tau=0",
            "valid_for_claim": "false",
            "source_paths": source_list("686_identity", "687_obstruction"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG688_1_component_bound",
            "gate": "component source bounds",
            "required_state": "all CSI688 inputs numeric or theorem-zero with source paths",
            "observed_state": "template rows only with MISSING markers",
            "result": "staged_nonclaim",
            "claim_effect": "future executable numerator path exists",
            "valid_for_claim": "false",
            "source_paths": source_list("687_epsilon_contract"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG688_2_denominator",
            "gate": "claim-grade denominator",
            "required_state": "M_H_ref or equivalent same-frame M_ref candidate source-backed and valid",
            "observed_state": "boundary/reference status has no claim-ready denominator",
            "result": "fail_blocked",
            "claim_effect": "epsilon value cannot support M_H_ref/Qbar/R10/PPN/local-GR claim",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "686_tau_residual"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG688_3_local_GR",
            "gate": "local-GR/PPN/R10 promotion",
            "required_state": "epsilon_tau, EH/R11, source normalization, and exchange rows all closed or scored",
            "observed_state": "symgrad tau components, denominator, EH/R11, and exchange channels remain open",
            "result": "fail_policy",
            "claim_effect": "no local-GR, PPN, orbital, Qbar, M_H_ref, or R10 pass",
            "valid_for_claim": "false",
            "source_paths": source_list("455_contract", "655_eh_audit", "687_obstruction"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG688_4_next",
            "gate": "next target selection",
            "required_state": "choose component source pack or zero theorem target",
            "observed_state": NEXT_TARGET,
            "result": "selected",
            "claim_effect": "fill or theorem-zero the component pack before scoring",
            "valid_for_claim": "false",
            "source_paths": source_list("687_epsilon_contract"),
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D688_0_decomposition",
            "target": "symgrad tau decomposition",
            "result": "written",
            "reason": "the Killing obstruction is now split into trace, shear, lapse, shift/extrinsic, boundary, tau-mismatch, stress, and denominator pieces",
            "next_action": "do not treat trace/selector silence as full stationarity",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D688_1_source_inputs",
            "target": "component source-input pack",
            "result": "staged_nonclaim",
            "reason": "every future epsilon_tau value must cite same-frame component sources, units, coefficients, and denominator",
            "next_action": "fill or theorem-zero the component rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D688_2_next",
            "target": "component source pack or zero theorem",
            "result": "selected",
            "reason": "the next non-circular move is to attack the actual source rows instead of adding another broad local-stationarity axiom",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S688_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "symgrad(tau) is decomposed into sourceable components; no component is theorem-zero; epsilon_tau remains a nonclaim residual contract.",
            "hardest_blocker": "source-backed component pack plus claim-grade same-frame denominator",
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
    decomposition_rows: list[dict[str, str]],
    input_rows: list[dict[str, str]],
    map_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows_by_name = {
        "decomposition": decomposition_rows,
        "inputs": input_rows,
        "maps": map_rows,
        "gates": gate_rows,
        "decision": decision_rows_,
        "summary": summary_rows,
    }
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_ids = ["603_validation", "604_validation", "655_validation", "684_validation", "685_validation", "686_validation", "687_validation"]
    prior_failure_counts = {source_id: len(validation_failures_for(source_id)) for source_id in prior_ids}
    decomposition_complete = len(decomposition_rows) == 9 and all(row["valid_for_claim"] == "false" for row in decomposition_rows)
    input_pack_complete = len(input_rows) == 9 and all(row["valid_for_claim"] == "false" for row in input_rows)
    input_missing_markers = all("MISSING_" in row["current_status"] for row in input_rows)
    map_complete = len(map_rows) == 4 and all(row["valid_for_claim"] == "false" for row in map_rows)
    map_missing_markers = all("MISSING_" in row["current_status"] or row["current_status"] == "SCHEMA_ONLY_NONCLAIM" for row in map_rows)
    gates_block = all(row["valid_for_claim"] == "false" for row in gate_rows) and any(row["result"].startswith("fail") for row in gate_rows)
    no_claim_rows = all_valid_for_claim_false(rows_by_name)
    next_selected = any(row["next_action"] == NEXT_TARGET for row in decision_rows_)
    formalization_count = formalization_changed_count()
    output_paths = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_688_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv",
        RESIDUALS / "P8_Y5_R10_688_COMPONENT_BOUND_INPUT_TEMPLATE.csv",
        RESIDUALS / "P8_Y5_R10_688_NUMERATOR_DENOMINATOR_MAP.csv",
        RESIDUALS / "P8_Y5_R10_688_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_688_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_688_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_688_VALIDATION.csv",
    ]
    scoped_outputs = all(str(path).startswith(str(ROOT)) for path in output_paths)
    checks = [
        ("V688_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V688_1_prior_validations_clean", all(count == 0 for count in prior_failure_counts.values()), ";".join(f"{key}={value}" for key, value in prior_failure_counts.items())),
        ("V688_2_decomposition_complete", decomposition_complete, f"decomposition_rows={len(decomposition_rows)}"),
        ("V688_3_decomposition_not_overclaimed", all(row["theorem_zero_status"] != "theorem_zero" for row in decomposition_rows), "no symgrad component is promoted as theorem-zero"),
        ("V688_4_component_input_pack_complete", input_pack_complete, f"input_rows={len(input_rows)}"),
        ("V688_5_input_missing_markers_retained", input_missing_markers, "all source input rows retain MISSING markers"),
        ("V688_6_numerator_denominator_map_complete", map_complete, f"map_rows={len(map_rows)}"),
        ("V688_7_map_missing_markers_retained", map_missing_markers, "numerator/denominator map remains nonclaim"),
        ("V688_8_claim_gates_block", gates_block, "claim gates keep M_H_ref/Qbar/R10/PPN/orbital/local_GR blocked"),
        ("V688_9_no_claim_rows_promoted", no_claim_rows, "all generated 688 rows remain valid_for_claim=false"),
        ("V688_10_next_target_selected", next_selected, NEXT_TARGET),
        ("V688_11_generated_outputs_scoped", scoped_outputs, "all 688 outputs target post-checkpoint-work"),
        ("V688_12_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V688_13_status_nonclaim", "no_MH_ref" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
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
    decomposition_rows: list[dict[str, str]],
    input_rows: list[dict[str, str]],
    map_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    doc = f"""# 688 - Y5 R10 Symgrad Tau Kinematic Decomposition Bound Or Source Input Fill

## Verdict

688 splits the local stationarity obstruction into actual kinematic pieces.

For a normalized local time flow `u`, the useful schematic identity is:

```text
nabla_(mu u_nu) = sigma_mu_nu + (theta/3) h_mu_nu - u_(mu a_nu)
```

For `tau = N u`, lapse/clock-normalization terms also enter. In ADM language, stationarity of the observed spatial metric also forces a lapse/shift/extrinsic-curvature relation, not just a zero volume trace.

So the useful result is blunt: `theta_D=0` or selector silence is not full Killing stationarity. The obstruction must be bounded from trace, shear, lapse/acceleration, shift/extrinsic curvature, boundary motion, tau-role mismatch, same-frame stress, and a valid denominator.

No component is promoted as theorem-zero. 688 writes the source-input contract that future work must fill before `epsilon_nonstationary_tau`, `M_H_ref`, `Qbar`, R10, PPN, orbital, or local-GR claims can move.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Symgrad Tau Decomposition

{markdown_table(decomposition_rows, ["component_id", "component", "decomposition", "theorem_zero_status", "missing_for_claim", "valid_for_claim"])}

## Component Bound Input Template

{markdown_table(input_rows, ["input_id", "component", "current_status", "units", "feeds_bound", "valid_for_claim"])}

## Numerator Denominator Map

{markdown_table(map_rows, ["map_id", "quantity", "formula", "current_status", "valid_for_claim"])}

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
    decomposition_rows = symgrad_decomposition_rows()
    input_rows = component_input_rows()
    map_rows = numerator_denominator_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    summary_rows = nonclaim_summary_rows()
    validation_rows_ = validation_rows(source_rows, decomposition_rows, input_rows, map_rows, gate_rows, decision_rows_, summary_rows)

    write_csv(RESIDUALS / "P8_Y5_R10_688_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv", decomposition_rows, ["component_id", "component", "decomposition", "bound_role", "theorem_zero_status", "missing_for_claim", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_688_COMPONENT_BOUND_INPUT_TEMPLATE.csv", input_rows, ["input_id", "component", "required_columns", "current_status", "units", "feeds_bound", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_688_NUMERATOR_DENOMINATOR_MAP.csv", map_rows, ["map_id", "quantity", "formula", "required_inputs", "current_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_688_CLAIM_GATE_EVALUATION.csv", gate_rows, ["gate_id", "gate", "required_state", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_688_DECISION.csv", decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_688_NONCLAIM_SUMMARY.csv", summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_688_VALIDATION.csv", validation_rows_, ["check_id", "result", "detail", "generated_utc"])

    write_doc(source_rows, decomposition_rows, input_rows, map_rows, gate_rows, decision_rows_, summary_rows, validation_rows_)

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"decomposition_rows={len(decomposition_rows)}")
    print(f"input_rows={len(input_rows)}")
    print(f"map_rows={len(map_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
