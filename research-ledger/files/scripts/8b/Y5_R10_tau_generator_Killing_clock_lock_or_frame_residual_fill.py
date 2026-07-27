from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_tau_generator_Killing_clock_lock_attempt_failed_frame_residual_rows_staged_nonclaim"
CLAIM_CEILING = "tau_generator_contract_and_frame_residual_template_only_no_MH_ref_no_Qbar_no_R10_no_PPN_no_orbital_no_local_GR_claim"
NEXT_TARGET = "686-Y5-R10-local-stationary-domain-Killing-certificate-or-tau-residual-row.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "685-Y5-R10-tau-generator-Killing-clock-lock-or-frame-residual-fill.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "455_doc": ROOT / "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
    "455_contract": RESIDUALS / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
    "457_doc": ROOT / "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
    "457_contract": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
    "647_doc": ROOT / "647-Y5-R10-derive-or-define-chiX-and-tau-clock-map.md",
    "647_validation": RESIDUALS / "P8_Y5_BRR545_647_VALIDATION.csv",
    "647_tau_map": RESIDUALS / "P8_Y5_R10_647_TAU_CLOCK_MAP.csv",
    "647_tau_requirement": RESIDUALS / "P8_Y5_R10_647_TAU_REQUIREMENT_DIAGNOSTIC.csv",
    "648_doc": ROOT / "648-Y5-R10-clock-product-bound-runner-or-derive-local-chiX-dynamics.md",
    "648_validation": RESIDUALS / "P8_Y5_BRR545_648_VALIDATION.csv",
    "648_tau_survival": RESIDUALS / "P8_Y5_R10_648_TAU_SURVIVAL_REQUIREMENTS.csv",
    "662_doc": ROOT / "662-Y5-R10-Hilbert-worldtube-source-measure-glue-or-equality-residual-bound.md",
    "662_validation": RESIDUALS / "P8_Y5_BRR545_662_VALIDATION.csv",
    "662_parent_clause": RESIDUALS / "P8_Y5_R10_662_PARENT_CLAUSE_AUDIT.csv",
    "663_doc": ROOT / "663-Y5-R10-minimal-parent-action-source-current-Euler-Ward-test-or-residual-input-fill.md",
    "663_validation": RESIDUALS / "P8_Y5_BRR545_663_VALIDATION.csv",
    "663_chain": RESIDUALS / "P8_Y5_R10_663_EULER_WARD_CHAIN_RESULT.csv",
    "664_doc": ROOT / "664-Y5-R10-Hamiltonian-PiM-integrability-source-equality-or-first-residual-fill.md",
    "664_validation": RESIDUALS / "P8_Y5_BRR545_664_VALIDATION.csv",
    "664_integrability": RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv",
    "666_doc": ROOT / "666-Y5-R10-parent-boundary-reference-lock-or-FB554-0-source-value-hunt.md",
    "666_validation": RESIDUALS / "P8_Y5_BRR545_666_VALIDATION.csv",
    "666_source_hunt": RESIDUALS / "P8_Y5_R10_666_FB5540_SOURCE_VALUE_HUNT_LEDGER.csv",
    "683_doc": ROOT / "683-Y5-R10-MH-ref-same-frame-denominator-or-Qedge-numerator-source.md",
    "683_validation": RESIDUALS / "P8_Y5_BRR545_683_VALIDATION.csv",
    "683_mh_attempt": RESIDUALS / "P8_Y5_R10_683_MH_REF_DENOMINATOR_ATTEMPT.csv",
    "683_same_frame_gate": RESIDUALS / "P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv",
    "684_doc": ROOT / "684-Y5-R10-observed-frame-tau-coframe-lock-for-MH-ref.md",
    "684_validation": RESIDUALS / "P8_Y5_BRR545_684_VALIDATION.csv",
    "684_frame_contract": RESIDUALS / "P8_Y5_R10_684_FRAME_LOCK_CONTRACT.csv",
    "684_tau_audit": RESIDUALS / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
    "684_mh_impact": RESIDUALS / "P8_Y5_R10_684_MH_REF_IMPACT_MAP.csv",
    "same_coframe_clause": RESIDUALS / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
    "hamiltonian_measure_contract": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
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
        "455_contract": "PiM flux closure contract including stationary generator",
        "457_doc": "Hamiltonian boundary charge route",
        "457_contract": "Hamiltonian boundary charge contract including HC1",
        "647_doc": "chiX/tau clock product map",
        "647_validation": "647 validation gate",
        "647_tau_map": "tau clock map rows",
        "647_tau_requirement": "clock tau requirement diagnostic",
        "648_doc": "clock product-bound and local chiX dynamics audit",
        "648_validation": "648 validation gate",
        "648_tau_survival": "tau survival rows",
        "662_doc": "Hilbert/worldtube same-object theorem",
        "662_validation": "662 validation gate",
        "662_parent_clause": "same-object parent clause audit",
        "663_doc": "Euler/Ward chain and PiM blocker",
        "663_validation": "663 validation gate",
        "663_chain": "Euler/Ward chain rows",
        "664_doc": "Hamiltonian integrability/source equality attempt",
        "664_validation": "664 validation gate",
        "664_integrability": "integrability attempt rows",
        "666_doc": "boundary/reference lock and source hunt",
        "666_validation": "666 validation gate",
        "666_source_hunt": "source hunt including tau and M_H_ref",
        "683_doc": "M_H_ref same-frame denominator predecessor",
        "683_validation": "683 validation gate",
        "683_mh_attempt": "M_H_ref denominator attempt rows",
        "683_same_frame_gate": "same-frame GM gates",
        "684_doc": "observed frame tau/coframe contract predecessor",
        "684_validation": "684 validation gate",
        "684_frame_contract": "frame lock contract rows",
        "684_tau_audit": "tau generator audit rows",
        "684_mh_impact": "M_H_ref impact map",
        "same_coframe_clause": "one-coframe parent clauses",
        "hamiltonian_measure_contract": "Hamiltonian source-measure contract",
        "boundary_reference_status": "M_H_ref first-row status",
    }
    return [
        {
            "source_id": source_id,
            "source_path": str(source_path),
            "exists": bool_text(source_path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, source_path in SOURCE_PATHS.items()
    ]


def tau_generator_contract_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "contract_id": "TGC685_0_define_tau_obs",
            "object": "tau_obs",
            "required_identity": "tau_obs is a parent-selected observed time-flow vector, not a post-readout label",
            "mathematical_form": "tau_obs in Gamma(T M_local) selected by e_obs and boundary/clock normalization",
            "current_status": "definition_target_only",
            "why_not_signed": "no parent clause constructs tau_obs from the local branch and boundary clock data",
            "if_signed": "all later source/charge/clock/orbit comparisons can use one generator",
            "valid_for_claim": "false",
            "source_paths": source_list("684_tau_audit", "same_coframe_clause"),
            "generated_utc": now,
        },
        {
            "contract_id": "TGC685_1_Killing_stationary_route",
            "object": "stationary Killing generator xi",
            "required_identity": "L_xi g_obs=0 and xi is timelike with fixed observed-clock normalization",
            "mathematical_form": "j_M^mu=T_H^{mu nu} xi_nu; nabla_mu j_M^mu=0 if xi Killing and nabla_mu T_H^{mu nu}=0",
            "current_status": "conditional_not_parent_derived",
            "why_not_signed": "local stationary domain/Killing certificate and same-frame Hilbert conservation are not derived",
            "if_signed": "Ward conservation can become a mass-current conservation theorem",
            "valid_for_claim": "false",
            "source_paths": source_list("455_doc", "455_contract", "457_doc"),
            "generated_utc": now,
        },
        {
            "contract_id": "TGC685_2_Hamiltonian_boundary_route",
            "object": "H_tau",
            "required_identity": "tau_obs generates an integrable Hamiltonian boundary charge with fixed reference",
            "mathematical_form": "delta H_tau = integral_S(delta Q_tau - i_tau theta); H_ref fixed once",
            "current_status": "not_derived_for_current_MTS",
            "why_not_signed": "parent symplectic current, boundary conditions, and reference subtraction remain open",
            "if_signed": "M_H_ref=H_tau[S]-H_ref becomes a stable charge functional",
            "valid_for_claim": "false",
            "source_paths": source_list("457_contract", "664_integrability", "hamiltonian_measure_contract"),
            "generated_utc": now,
        },
        {
            "contract_id": "TGC685_3_clock_normalization_route",
            "object": "clock normalization",
            "required_identity": "tau_obs is normalized by the same local clocks used in redshift/clock comparisons",
            "mathematical_form": "tau_clock = tau_obs and proper-time readout follows e_obs clocks, not chiX closure dynamics alone",
            "current_status": "clock_product_bound_only",
            "why_not_signed": "647/648 define tau_clock_time=dchi_X/dt product constraints, not the Hamiltonian time generator",
            "if_signed": "clock normalization can support the Hamiltonian generator instead of merely bounding alpha drift",
            "valid_for_claim": "false",
            "source_paths": source_list("647_tau_map", "648_tau_survival", "684_tau_audit"),
            "generated_utc": now,
        },
        {
            "contract_id": "TGC685_4_no_lapse_gauge_cheat",
            "object": "lapse/time reparametrization",
            "required_identity": "a homogeneous lapse or time-coordinate choice is not evidence unless parent-coupled to clocks and charge",
            "mathematical_form": "tau -> f tau is gauge/normalization until H_tau, clocks, and boundary reference transform consistently",
            "current_status": "guardrail_written",
            "why_not_signed": "no parent normalization theorem fixes f across source, clocks, and H_ref",
            "if_signed": "prevents denominator rescaling ambiguity",
            "valid_for_claim": "false",
            "source_paths": source_list("648_doc", "684_frame_contract", "457_doc"),
            "generated_utc": now,
        },
        {
            "contract_id": "TGC685_5_orbit_readout_route",
            "object": "orbital tau",
            "required_identity": "slow-orbit readout uses the same tau_obs and g_obs as H_tau",
            "mathematical_form": "a_orbit=-grad Phi[g_obs,tau_obs] and H_tau -> Poisson/Gauss source before GM fitting",
            "current_status": "Poisson_Gauss_orbit_not_parent_derived",
            "why_not_signed": "683 already blocks GM_orbit/G_ref as circular without the bridge",
            "if_signed": "GM_orbit/G_ref could become a derived readout of M_H_ref rather than an input",
            "valid_for_claim": "false",
            "source_paths": source_list("683_same_frame_gate", "457_contract", "684_mh_impact"),
            "generated_utc": now,
        },
        {
            "contract_id": "TGC685_6_verdict",
            "object": "tau generator lock",
            "required_identity": "one tau_obs controls source, Hamiltonian charge, clocks, boundary reference, and orbital readout",
            "mathematical_form": "tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit=tau_obs",
            "current_status": "blocked_nonclaim",
            "why_not_signed": "every nontrivial route still has a missing parent certificate",
            "if_signed": "one major M_H_ref denominator blocker would close",
            "valid_for_claim": "false",
            "source_paths": source_list("684_tau_audit", "683_same_frame_gate", "boundary_reference_status"),
            "generated_utc": now,
        },
    ]


def killing_clock_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "KCG685_0_observed_vector",
            "gate": "observed time vector exists",
            "pass_condition": "parent action selects tau_obs from e_obs and local boundary/clock data",
            "observed_state": "MISSING_PARENT_SELECTED_TAU_OBS",
            "result": "fail_blocked",
            "claim_effect": "no unique Hamiltonian mass generator",
            "valid_for_claim": "false",
            "source_paths": source_list("684_tau_audit", "same_coframe_clause"),
            "generated_utc": now,
        },
        {
            "gate_id": "KCG685_1_stationarity",
            "gate": "stationary/Killing local branch",
            "pass_condition": "L_tau g_obs=0 or admissible asymptotic/quasilocal time-flow conditions hold",
            "observed_state": "MISSING_LOCAL_STATIONARY_KILLING_CERTIFICATE",
            "result": "fail_blocked",
            "claim_effect": "Ward current cannot be promoted to mass-current closure",
            "valid_for_claim": "false",
            "source_paths": source_list("455_contract", "457_contract"),
            "generated_utc": now,
        },
        {
            "gate_id": "KCG685_2_clock_normalization",
            "gate": "clock normalization",
            "pass_condition": "tau_obs is normalized by the same observed clocks used in lab/redshift comparisons",
            "observed_state": "MISSING_CLOCK_NORMALIZATION_THEOREM",
            "result": "fail_blocked",
            "claim_effect": "charge can be rescaled relative to clocks",
            "valid_for_claim": "false",
            "source_paths": source_list("647_tau_map", "648_tau_survival", "684_frame_contract"),
            "generated_utc": now,
        },
        {
            "gate_id": "KCG685_3_integrable_charge",
            "gate": "Hamiltonian integrability",
            "pass_condition": "delta H_tau is finite, integrable, and reference-subtracted once",
            "observed_state": "MISSING_INTEGRABLE_CHARGE_AND_REFERENCE_LOCK",
            "result": "fail_blocked",
            "claim_effect": "M_H_ref cannot be defined as a stable denominator",
            "valid_for_claim": "false",
            "source_paths": source_list("664_integrability", "666_source_hunt", "hamiltonian_measure_contract"),
            "generated_utc": now,
        },
        {
            "gate_id": "KCG685_4_boundary_reference",
            "gate": "boundary/reference tau lock",
            "pass_condition": "H_ref and boundary counterterms use the same tau_obs and do not carry source-dependent shifts",
            "observed_state": "MISSING_FIXED_REFERENCE_TAU_BOUNDARY_CLASS",
            "result": "fail_blocked",
            "claim_effect": "reference energy can contaminate M_H_ref",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "666_source_hunt"),
            "generated_utc": now,
        },
        {
            "gate_id": "KCG685_5_orbit_bridge",
            "gate": "Poisson/Gauss/orbit bridge",
            "pass_condition": "same H_tau charge controls weak-field Phi and inverse-square orbital readout",
            "observed_state": "MISSING_POISSON_GAUSS_ORBITAL_READOUT",
            "result": "fail_blocked",
            "claim_effect": "GM_orbit/G_ref remains empirical and circular as denominator proof",
            "valid_for_claim": "false",
            "source_paths": source_list("683_same_frame_gate", "457_contract"),
            "generated_utc": now,
        },
        {
            "gate_id": "KCG685_6_no_exchange_leak",
            "gate": "hidden exchange/boundary silence",
            "pass_condition": "extra/projector/domain/boundary/coupling currents have zero mass-channel projection",
            "observed_state": "MISSING_ZERO_EXCHANGE_PROJECTION",
            "result": "fail_blocked",
            "claim_effect": "even a good tau would not make the charge pure Hilbert mass",
            "valid_for_claim": "false",
            "source_paths": source_list("455_contract", "457_contract", "662_parent_clause"),
            "generated_utc": now,
        },
        {
            "gate_id": "KCG685_7_total",
            "gate": "tau lock claim readiness",
            "pass_condition": "all gates pass with no MISSING markers and no closure-only clock coordinate",
            "observed_state": "seven blocking gates remain open",
            "result": "fail_blocked",
            "claim_effect": "no M_H_ref, Qbar, R10, PPN, orbital, or local-GR claim",
            "valid_for_claim": "false",
            "source_paths": source_list("684_doc", "683_doc"),
            "generated_utc": now,
        },
    ]


def frame_residual_template_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "residual_id": "TRF685_0_delta_tau_source_charge",
            "quantity": "delta_tau_source_charge",
            "definition": "fractional mismatch between tau used in J_H[tau] and tau used in H_tau",
            "required_columns": "system_id;tau_source;tau_charge;delta_tau_source_charge;units;source_file;assumptions;valid_for_claim",
            "current_status": "MISSING_TAU_SOURCE_CHARGE_BOUND_OR_THEOREM_ZERO",
            "local_rows_affected": "R1;R4;R9;R11",
            "valid_for_claim": "false",
            "source_paths": source_list("684_tau_audit", "666_source_hunt"),
            "generated_utc": now,
        },
        {
            "residual_id": "TRF685_1_delta_tau_clock_charge",
            "quantity": "delta_tau_clock_charge",
            "definition": "fractional mismatch between local clock normalization and Hamiltonian charge normalization",
            "required_columns": "system_id;clock_pair;tau_clock;tau_charge;delta_tau_clock_charge;bound_source;source_file;valid_for_claim",
            "current_status": "MISSING_CLOCK_NORMALIZATION_BOUND_OR_THEOREM_ZERO",
            "local_rows_affected": "R2;R9;R11",
            "valid_for_claim": "false",
            "source_paths": source_list("647_tau_requirement", "648_tau_survival", "684_tau_audit"),
            "generated_utc": now,
        },
        {
            "residual_id": "TRF685_2_delta_tau_orbit_charge",
            "quantity": "delta_tau_orbit_charge",
            "definition": "fractional mismatch between orbital readout time and Hamiltonian charge time",
            "required_columns": "system_id;tau_orbit;tau_charge;delta_tau_orbit_charge;orbit_source;source_file;valid_for_claim",
            "current_status": "MISSING_ORBITAL_TAU_BRIDGE",
            "local_rows_affected": "R4;R9;R10;R11",
            "valid_for_claim": "false",
            "source_paths": source_list("683_same_frame_gate", "457_contract"),
            "generated_utc": now,
        },
        {
            "residual_id": "TRF685_3_nonstationarity_flux",
            "quantity": "epsilon_nonstationary_tau",
            "definition": "mass-current leakage from T_H^{mu nu} nabla_(mu tau_nu) when tau is not Killing/stationary",
            "required_columns": "system_id;surface_pair;int_T_sym_grad_tau;M_ref;units;source_file;valid_for_claim",
            "current_status": "MISSING_STATIONARY_KILLING_RESIDUAL",
            "local_rows_affected": "R4;R9;R11",
            "valid_for_claim": "false",
            "source_paths": source_list("455_contract", "457_contract"),
            "generated_utc": now,
        },
        {
            "residual_id": "TRF685_4_reference_tau_shift",
            "quantity": "Delta_ref_tau_over_MH",
            "definition": "reference/boundary charge shift induced by tau normalization or boundary class choice",
            "required_columns": "system_id;H_ref_tau_shift;M_H_ref;units;source_file;assumptions;valid_for_claim",
            "current_status": "MISSING_REFERENCE_TAU_SHIFT",
            "local_rows_affected": "R3;R4;R7;R9;R11",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "666_source_hunt"),
            "generated_utc": now,
        },
        {
            "residual_id": "TRF685_5_lapse_gauge_ambiguity",
            "quantity": "epsilon_lapse_gauge",
            "definition": "unfixed tau rescaling/lapse convention not tied to parent clocks and Hamiltonian charge",
            "required_columns": "system_id;lapse_rule;clock_normalization;charge_normalization;epsilon_lapse_gauge;source_file;valid_for_claim",
            "current_status": "MISSING_LAPSE_NORMALIZATION_RULE",
            "local_rows_affected": "R2;R4;R9;R11",
            "valid_for_claim": "false",
            "source_paths": source_list("648_doc", "684_frame_contract"),
            "generated_utc": now,
        },
    ]


def mh_ref_impact_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "impact_id": "MHI685_0_denominator",
            "target": "M_H_ref",
            "tau_result": "not_locked",
            "effect": "M_H_ref remains a conditional charge definition, not a denominator row",
            "remaining_debt": "stationary generator, integrability, fixed reference, positive same-frame source mass, Poisson/Gauss calibration",
            "valid_for_claim": "false",
            "source_paths": source_list("683_mh_attempt", "684_mh_impact", "boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "impact_id": "MHI685_1_mass_current",
            "target": "d(Pi_M J_H)=0",
            "tau_result": "Killing_route_conditional_only",
            "effect": "Ward conservation does not become mass-flux closure",
            "remaining_debt": "same-frame Hilbert stress, Killing/stationarity, zero exchange projection",
            "valid_for_claim": "false",
            "source_paths": source_list("455_contract", "457_contract"),
            "generated_utc": now,
        },
        {
            "impact_id": "MHI685_2_clock_branch",
            "target": "clock constraints",
            "tau_result": "product_bound_only",
            "effect": "clock rows constrain kappa_alpha*dchi_X/dt, not H_tau normalization",
            "remaining_debt": "derive local chiX dynamics or separate clock-product branch from tau_obs generator",
            "valid_for_claim": "false",
            "source_paths": source_list("647_tau_map", "648_tau_survival"),
            "generated_utc": now,
        },
        {
            "impact_id": "MHI685_3_Qbar_R10",
            "target": "Qbar/R10",
            "tau_result": "denominator_not_safe",
            "effect": "Qbar denominator and alpha_edge remain blocked before any R10 claim",
            "remaining_debt": "M_H_ref plus Q_edge numerator plus R10 bound curve promotion",
            "valid_for_claim": "false",
            "source_paths": source_list("683_doc", "684_doc"),
            "generated_utc": now,
        },
    ]


def claim_gate_evaluation_rows(
    contract_rows: list[dict[str, str]],
    killing_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    impact_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    promoted = [
        row
        for row in contract_rows + killing_rows + residual_rows + impact_rows
        if row.get("valid_for_claim") == "true"
    ]
    return [
        {
            "evaluation_id": "CGE685_0_tau_generator",
            "target": "tau_obs",
            "status": "blocked_nonclaim",
            "reason": "no parent-selected observed stationary/Killing/Hamiltonian generator",
            "claim_effect": "tau lock not promoted",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluation_id": "CGE685_1_frame_residuals",
            "target": "tau/frame residual template",
            "status": "staged_nonclaim",
            "reason": f"residual_rows={len(residual_rows)}; all missing/theorem-zero slots explicit",
            "claim_effect": "fallback rows exist but are unfilled",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluation_id": "CGE685_2_MH_ref",
            "target": "M_H_ref denominator",
            "status": "blocked_nonclaim",
            "reason": "tau lock, integrability, reference, and calibration gates remain open",
            "claim_effect": "no denominator, Qbar, R10, or local-GR claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluation_id": "CGE685_3_claim_guard",
            "target": "685 generated rows",
            "status": "pass_nonclaim",
            "reason": f"generated_claim_rows={len(promoted)}",
            "claim_effect": "all 685 rows remain internal scaffold only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D685_0_tau_lock",
            "target": "tau_obs generator",
            "result": "not_parent_signed",
            "reason": "Killing, Hamiltonian, clock, boundary, and orbit versions of tau are not one derived object",
            "next_action": "do not promote tau lock",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D685_1_residual_template",
            "target": "tau/frame residual rows",
            "result": "staged",
            "reason": "if tau lock cannot be derived, source/clock/orbit/boundary mismatches must become explicit residuals",
            "next_action": "keep rows unfilled until source-backed or theorem-zero inputs exist",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D685_2_next",
            "target": "local stationary domain/Killing certificate",
            "result": "selected",
            "reason": "the least-circular next proof is to decide whether the compact local branch really supplies a stationary observed generator",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S685_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "tau generator lock attempted; all routes remain conditional or missing; residual rows staged",
            "blocked_claims": "M_H_ref;Qbar;alpha_edge;R10;PPN;orbital;local_GR",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def boundary_reference_mh_ref_claim_ready() -> bool:
    status_path = SOURCE_PATHS["boundary_reference_status"]
    if not status_path.exists():
        return False
    for source_row in read_csv(status_path):
        if source_row.get("quantity") == "M_H_ref":
            return (
                source_row.get("valid_for_claim") == "true"
                and source_row.get("claim_valid_data_rows") not in {"", "0"}
            )
    return False


def validation_rows(
    source_register: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    killing_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    impact_rows: list[dict[str, str]],
    claim_gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    missing_sources = [source_row["source_id"] for source_row in source_register if source_row["exists"] != "true"]
    rows.append({
        "check_id": "V685_0_source_paths_exist",
        "result": "pass" if not missing_sources else "fail",
        "detail": "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources),
        "generated_utc": now,
    })

    validation_ids = ["647_validation", "648_validation", "662_validation", "663_validation", "664_validation", "666_validation", "683_validation", "684_validation"]
    prior_failures = {source_id: len(validation_failures_for(source_id)) for source_id in validation_ids}
    rows.append({
        "check_id": "V685_1_prior_validations_clean",
        "result": "pass" if all(failure_count == 0 for failure_count in prior_failures.values()) else "fail",
        "detail": ";".join(f"{source_id}={failure_count}" for source_id, failure_count in prior_failures.items()),
        "generated_utc": now,
    })

    rows.append({
        "check_id": "V685_2_tau_contract_complete",
        "result": "pass" if len(contract_rows) >= 7 else "fail",
        "detail": f"contract_rows={len(contract_rows)}",
        "generated_utc": now,
    })

    failed_gates = [row for row in killing_rows if row["result"] != "pass"]
    rows.append({
        "check_id": "V685_3_Killing_clock_gates_blocked",
        "result": "pass" if len(failed_gates) == len(killing_rows) and len(killing_rows) >= 8 else "fail",
        "detail": f"failed_gates={len(failed_gates)};gate_rows={len(killing_rows)}",
        "generated_utc": now,
    })

    required_residuals = [
        "delta_tau_source_charge",
        "delta_tau_clock_charge",
        "delta_tau_orbit_charge",
        "epsilon_nonstationary_tau",
        "Delta_ref_tau_over_MH",
        "epsilon_lapse_gauge",
    ]
    observed_residuals = {row["quantity"] for row in residual_rows}
    missing_residuals = [quantity for quantity in required_residuals if quantity not in observed_residuals]
    rows.append({
        "check_id": "V685_4_residual_template_complete",
        "result": "pass" if not missing_residuals else "fail",
        "detail": "all tau/frame residual templates present" if not missing_residuals else "missing=" + ";".join(missing_residuals),
        "generated_utc": now,
    })

    rows.append({
        "check_id": "V685_5_MH_ref_not_claim_ready",
        "result": "pass" if not boundary_reference_mh_ref_claim_ready() else "fail",
        "detail": "boundary reference status has no claim-ready M_H_ref row",
        "generated_utc": now,
    })

    clock_product_only = any("product" in row["current_status"] for row in contract_rows)
    rows.append({
        "check_id": "V685_6_clock_product_not_tau_generator",
        "result": "pass" if clock_product_only else "fail",
        "detail": "clock product rows are separated from Hamiltonian tau generator",
        "generated_utc": now,
    })

    generated_rows = contract_rows + killing_rows + residual_rows + impact_rows + claim_gate_rows + decision
    promoted_rows = [row for row in generated_rows if row.get("valid_for_claim") == "true"]
    rows.append({
        "check_id": "V685_7_no_claim_rows_promoted",
        "result": "pass" if not promoted_rows else "fail",
        "detail": "all generated 685 rows remain valid_for_claim=false" if not promoted_rows else f"claim_rows={len(promoted_rows)}",
        "generated_utc": now,
    })

    blocked_text = ";".join(";".join(row.values()) for row in generated_rows).lower()
    rows.append({
        "check_id": "V685_8_missing_markers_retained",
        "result": "pass" if any(token in blocked_text for token in ["missing", "blocked", "not_parent", "not parent", "nonclaim"]) else "fail",
        "detail": "blocking markers retained",
        "generated_utc": now,
    })

    selected_rows = [row for row in decision if row["next_action"] == NEXT_TARGET]
    rows.append({
        "check_id": "V685_9_next_target_selected",
        "result": "pass" if selected_rows else "fail",
        "detail": NEXT_TARGET,
        "generated_utc": now,
    })

    output_paths = [
        RESIDUALS / "P8_Y5_R10_685_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
        RESIDUALS / "P8_Y5_R10_685_KILLING_CLOCK_GATE.csv",
        RESIDUALS / "P8_Y5_R10_685_TAU_FRAME_RESIDUAL_TEMPLATE.csv",
        RESIDUALS / "P8_Y5_R10_685_MH_REF_IMPACT.csv",
        RESIDUALS / "P8_Y5_R10_685_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_685_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_685_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_685_VALIDATION.csv",
        DOC_PATH,
    ]
    rows.append({
        "check_id": "V685_10_generated_outputs_scoped",
        "result": "pass" if all(str(output_path).startswith(str(ROOT)) for output_path in output_paths) else "fail",
        "detail": "all 685 outputs target post-checkpoint-work",
        "generated_utc": now,
    })

    changed_count = formalization_changed_count()
    rows.append({
        "check_id": "V685_11_formalization_workbench_untouched",
        "result": "pass" if changed_count == 0 else "fail",
        "detail": f"formalization_changed_after_cutoff={changed_count}",
        "generated_utc": now,
    })

    rows.append({
        "check_id": "V685_12_status_nonclaim",
        "result": "pass" if "no_MH_ref" in CLAIM_CEILING and "no_local_GR" in CLAIM_CEILING else "fail",
        "detail": CLAIM_CEILING,
        "generated_utc": now,
    })

    return rows


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        rendered_values = [
            str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            for column in columns
        ]
        lines.append("| " + " | ".join(rendered_values) + " |")
    return "\n".join(lines)


def write_doc(
    source_register: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    killing_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    impact_rows: list[dict[str, str]],
    claim_gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 685 - Y5 R10 Tau Generator Killing Clock Lock Or Frame Residual Fill

## Verdict

685 tried to turn `tau_obs` into a real parent-selected generator.

The clean route would be:

```text
tau_source = tau_charge = tau_clock = tau_boundary = tau_orbit = tau_obs
L_tau_obs g_obs = 0
delta H_tau = integral_S(delta Q_tau - i_tau theta)
M_H_ref = H_tau_obs[S_link] - H_ref
```

That is exactly the GR-like route: a stationary/Killing or Hamiltonian time generator turns Hilbert stress conservation into a conserved mass current. But current MTS has not parent-derived the local stationary generator, clock normalization, Hamiltonian integrability, fixed boundary reference, orbit bridge, or zero exchange projection.

So 685 does not promote `tau_obs`, `M_H_ref`, `Qbar`, R10, PPN, orbital, or local GR. It stages the residual rows that must be filled if the tau-lock proof keeps failing.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_register, ["source_id", "source_path", "exists", "role"])}

## Tau Generator Contract

{markdown_table(contract_rows, ["contract_id", "object", "required_identity", "mathematical_form", "current_status", "why_not_signed", "if_signed", "valid_for_claim"])}

## Killing Clock Gate

{markdown_table(killing_rows, ["gate_id", "gate", "pass_condition", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Tau Frame Residual Template

{markdown_table(residual_rows, ["residual_id", "quantity", "definition", "required_columns", "current_status", "local_rows_affected", "valid_for_claim"])}

## MH Ref Impact

{markdown_table(impact_rows, ["impact_id", "target", "tau_result", "effect", "remaining_debt", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(claim_gate_rows, ["evaluation_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Next Target

`{NEXT_TARGET}`

Default next route: try to prove the compact local branch actually supplies a stationary observed generator. If that fails, keep `tau_obs` as a residual-bearing frame choice rather than using it inside `M_H_ref`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_register = source_register_rows()
    contract_rows = tau_generator_contract_rows()
    killing_rows = killing_clock_gate_rows()
    residual_rows = frame_residual_template_rows()
    impact_rows = mh_ref_impact_rows()
    claim_gate_rows = claim_gate_evaluation_rows(contract_rows, killing_rows, residual_rows, impact_rows)
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_register, contract_rows, killing_rows, residual_rows, impact_rows, claim_gate_rows, decision)

    write_csv(RESIDUALS / "P8_Y5_R10_685_SOURCE_REGISTER.csv", source_register, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv", contract_rows, ["contract_id", "object", "required_identity", "mathematical_form", "current_status", "why_not_signed", "if_signed", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_685_KILLING_CLOCK_GATE.csv", killing_rows, ["gate_id", "gate", "pass_condition", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_685_TAU_FRAME_RESIDUAL_TEMPLATE.csv", residual_rows, ["residual_id", "quantity", "definition", "required_columns", "current_status", "local_rows_affected", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_685_MH_REF_IMPACT.csv", impact_rows, ["impact_id", "target", "tau_result", "effect", "remaining_debt", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_685_CLAIM_GATE_EVALUATION.csv", claim_gate_rows, ["evaluation_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_685_DECISION.csv", decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_685_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "blocked_claims", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_685_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_register, contract_rows, killing_rows, residual_rows, impact_rows, claim_gate_rows, decision, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"contract_rows={len(contract_rows)}")
    print(f"killing_gates={len(killing_rows)}")
    print(f"residual_rows={len(residual_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
