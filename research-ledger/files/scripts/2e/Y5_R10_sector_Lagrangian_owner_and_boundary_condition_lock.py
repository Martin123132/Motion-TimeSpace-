from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_sector_Lagrangian_owner_boundary_condition_lock_attempted_LX_Bref_boundary_tau_MHref_unsigned_nonclaim"
CLAIM_CEILING = "sector_Lagrangian_owner_and_boundary_condition_lock_only_no_FB5540_zero_no_stable_Hamiltonian_source_charge_no_Newton_no_PPN_no_R10_no_R11_no_local_GR_claim"
NEXT_TARGET = "669-Y5-R10-minimal-LX-sector-operator-owner-or-retained-residual-vector.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "668-Y5-R10-sector-Lagrangian-owner-and-boundary-condition-lock.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "667_doc": ROOT / "667-Y5-R10-explicit-parent-boundary-action-ansatz-and-variation-ledger.md",
    "667_validation": RESIDUALS / "P8_Y5_BRR545_667_VALIDATION.csv",
    "667_ansatz": RESIDUALS / "P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv",
    "667_variation": RESIDUALS / "P8_Y5_R10_667_VARIATION_LEDGER.csv",
    "667_fallback": RESIDUALS / "P8_Y5_R10_667_RESIDUAL_FALLBACK_ROWS.csv",
    "667_term_map": RESIDUALS / "P8_Y5_R10_667_FB5540_TERM_MAP.csv",
    "666_validation": RESIDUALS / "P8_Y5_BRR545_666_VALIDATION.csv",
    "666_clause_test": RESIDUALS / "P8_Y5_R10_666_BOUNDARY_REFERENCE_CLAUSE_TEST.csv",
    "654_doc": ROOT / "654-Y5-R10-local-GR-reduction-spine-under-explicit-WEP-closure.md",
    "653_doc": ROOT / "653-Y5-R10-parent-matter-functor-signature-or-WEP-closure-demotion.md",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "656_doc": ROOT / "656-Y5-R10-R11-executable-vector-minimum-skeleton-under-WEP-closure.md",
    "637_doc": ROOT / "637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md",
    "622_doc": ROOT / "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md",
    "621_doc": ROOT / "621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md",
    "511_doc": ROOT / "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
    "506_doc": ROOT / "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
    "min_parent_blocks": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "min_parent_conditions": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
    "source_owner_terms": RESIDUALS / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "parent_local_zero_clause": RESIDUALS / "P8_PARENT_LOCAL_ZERO_ACTION_CLAUSE.csv",
    "parent_local_zero_variation": RESIDUALS / "P8_PARENT_LOCAL_ZERO_VARIATION_CHAIN.csv",
    "domain_clause": RESIDUALS / "P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv",
    "boundary_contract": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv",
    "boundary_ownership": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_PARENT_OWNERSHIP_AUDIT.csv",
    "hamiltonian_contract": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
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


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "667_doc": "immediate predecessor requesting sector Lagrangian and boundary-condition ownership",
        "667_validation": "prior 667 validation",
        "667_ansatz": "parent-boundary action scaffold",
        "667_variation": "variation ledger mapping FB554_0 terms",
        "667_fallback": "missing owner fallback rows",
        "667_term_map": "FB554_0 term map",
        "666_validation": "prior 666 validation",
        "666_clause_test": "boundary/reference clause gaps",
        "654_doc": "local-GR spine under explicit WEP closure",
        "653_doc": "WEP/common matter functor demotion",
        "655_doc": "EH operator selection gate",
        "656_doc": "R11 executable vector skeleton",
        "637_doc": "constant ownership derivation and blockers",
        "622_doc": "parent matter sector contract",
        "621_doc": "matter coupling normal form theorem",
        "511_doc": "minimal parent action local-GR fixed-point ansatz",
        "506_doc": "local EH reduction and extra-sector silence theorem",
        "min_parent_blocks": "minimal parent action blocks",
        "min_parent_conditions": "local-GR fixed-point conditions",
        "source_owner_terms": "source owner parent-action terms",
        "parent_local_zero_clause": "local-zero parent action clause",
        "parent_local_zero_variation": "local-zero variation chain",
        "domain_clause": "domain selector parent action clause",
        "boundary_contract": "boundary/reference minimal action contract",
        "boundary_ownership": "boundary/reference parent ownership audit",
        "hamiltonian_contract": "Hamiltonian boundary charge contract",
    }
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def sector_owner_audit_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "sector_id": "SO668_0_EH_metric",
            "sector": "EH_metric_core",
            "candidate_Lagrangian": "(16*pi*G_ref)^-1(R-2*Lambda_loc)*epsilon",
            "owner_status": "conditional_template_not_parent_selected",
            "owned_if": "local operator selection proves EH-only metric dynamics in compact exterior",
            "current_blocker": "EH operator selection remains blocked/retained as R11 vector",
            "feeds": "R3_gamma;R4_beta;R5_alpha1;R6_alpha2;R7_alpha3;R8_xi;R11",
            "valid_for_claim": "false",
            "source_paths": source_list("654_doc", "655_doc", "min_parent_blocks"),
            "generated_utc": now,
        },
        {
            "sector_id": "SO668_1_observed_matter",
            "sector": "observed_matter_and_coframe",
            "candidate_Lagrangian": "L_matter[g_obs,psi]",
            "owner_status": "explicit_closure_label_not_parent_derived",
            "owned_if": "matter/source/clocks/orbits are forced by parent functor to one observed geometry with no constant/material marker leakage",
            "current_blocker": "WEP/common geometry is closure-labelled and constants/material labels remain open",
            "feeds": "R0_identity;R1_WEP;R2_clock;time_generator_lock;Delta_frame",
            "valid_for_claim": "false",
            "source_paths": source_list("653_doc", "654_doc", "621_doc", "622_doc"),
            "generated_utc": now,
        },
        {
            "sector_id": "SO668_2_MTS_extra_LX",
            "sector": "MTS_extra_fields_X",
            "candidate_Lagrangian": "L_X[g,X_MTS,nabla X_MTS]",
            "owner_status": "missing_sector_Lagrangian_owner",
            "owned_if": "each extra field has explicit operator, source term, boundary condition, Theta_X, Q_X, and positive/nohair or executable residual route",
            "current_blocker": "L_X, Theta_X, Q_X, C_X, and omega_X are not specified sector-by-sector",
            "feeds": "delta_H_tau_nonintegrable_over_MH;symplectic_boundary_flux_over_MH;C_extra;R10;R11",
            "valid_for_claim": "false",
            "source_paths": source_list("667_fallback", "506_doc", "source_owner_terms"),
            "generated_utc": now,
        },
        {
            "sector_id": "SO668_3_boundary_reference",
            "sector": "B_ref_reference",
            "candidate_Lagrangian": "B_ref[gamma_ref,tau_ref,C_top]",
            "owner_status": "missing_parent_reference_functional",
            "owned_if": "B_ref is selected before source/readout and derivative-silent in source, surface, frame, time, and range",
            "current_blocker": "reference branch remains a contract, not parent-owned",
            "feeds": "Delta_ref_over_MH;Delta_symp_over_MH",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_contract", "boundary_ownership", "666_clause_test"),
            "generated_utc": now,
        },
        {
            "sector_id": "SO668_4_boundary_class_nohair",
            "sector": "B_class_C_top_chi_B",
            "candidate_Lagrangian": "B_class[chi_B,C_top]+boundary no-hair constraints",
            "owner_status": "missing_boundary_class_selection",
            "owned_if": "relative class is parent-selected and boundary stress has no vector/tensor/shear/radial/time hair",
            "current_blocker": "scalar/no-flux conditions are conditional and do not kill vector/tensor boundary hair",
            "feeds": "B_zero_flux_over_MH;symplectic_boundary_flux_over_MH;R7_alpha3;R8_xi",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_contract", "boundary_ownership", "parent_local_zero_variation"),
            "generated_utc": now,
        },
        {
            "sector_id": "SO668_5_projector_domain",
            "sector": "projector_domain_selector",
            "candidate_Lagrangian": "S_projector+S_domain",
            "owner_status": "retained_symbolic_not_parent_owned",
            "owned_if": "projector/domain selector is covariant, topological or first-class, and has zero metric stress/flux",
            "current_blocker": "domain selector and projector stress remain retained symbolic rows",
            "feeds": "projector_stress;preferred_frame;R5_alpha1;R6_alpha2;R7_alpha3;R8_xi;R10;R11",
            "valid_for_claim": "false",
            "source_paths": source_list("domain_clause", "source_owner_terms", "667_variation"),
            "generated_utc": now,
        },
        {
            "sector_id": "SO668_6_tau_clock",
            "sector": "tau_and_clock_generator",
            "candidate_Lagrangian": "tau fixed by observed coframe/matter clock functor",
            "owner_status": "missing_observed_tau_functor",
            "owned_if": "tau_source=tau_charge=tau_clock=tau_readout and delta tau=0 follows from parent matter/coframe coupling",
            "current_blocker": "same observed generator is required but not derived",
            "feeds": "time_generator_lock;Delta_frame;R2_clock;R9_Gdot",
            "valid_for_claim": "false",
            "source_paths": source_list("667_fallback", "hamiltonian_contract", "654_doc"),
            "generated_utc": now,
        },
        {
            "sector_id": "SO668_7_source_normalization",
            "sector": "M_H_ref_G_eff_source_readout",
            "candidate_Lagrangian": "S_source_norm[kappa,G_eff,M_H_ref,Q_tau]",
            "owner_status": "missing_source_measure_and_Gauss_readout",
            "owned_if": "worldtube source equality and Poisson/Gauss/orbital readout derive measured GM from the same Q_tau",
            "current_blocker": "M_H_ref remains a guardrail definition, not measured source mass",
            "feeds": "M_H_ref;Delta_cal;R1_WEP;R9_Gdot;PPN_vector",
            "valid_for_claim": "false",
            "source_paths": source_list("hamiltonian_contract", "source_owner_terms", "667_fallback"),
            "generated_utc": now,
        },
        {
            "sector_id": "SO668_8_constants_couplings",
            "sector": "constants_and_material_labels",
            "candidate_Lagrangian": "constant sector descends to quotient or appears as representation/topological data",
            "owner_status": "constant_ownership_not_closed",
            "owned_if": "alpha_EM, mass ratios, clock transitions, species labels, and measured GM are quotient/topological/representation data",
            "current_blocker": "637 leaves constants and material labels open",
            "feeds": "R1_WEP;R2_clock;R9_Gdot;R10;source_normalization",
            "valid_for_claim": "false",
            "source_paths": source_list("637_doc", "621_doc", "622_doc"),
            "generated_utc": now,
        },
        {
            "sector_id": "SO668_9_memory_kernel",
            "sector": "memory_kernel_local_silence",
            "candidate_Lagrangian": "S_memory or nonlocal kernel sector",
            "owner_status": "retained",
            "owned_if": "compact-local memory kernel is silent, screened, or constant universal calibration",
            "current_blocker": "local memory kernel silence is not parent-derived",
            "feeds": "R7_alpha3;R9_Gdot;R10;R11",
            "valid_for_claim": "false",
            "source_paths": source_list("source_owner_terms", "min_parent_conditions", "654_doc"),
            "generated_utc": now,
        },
    ]


def boundary_condition_lock_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "lock_id": "BCL668_0_variational_principle",
            "boundary_condition": "Theta_total + delta B_total vanishes or is fixed on allowed variations",
            "needed_for": "well-defined H_tau and delta_H_tau_nonintegrable control",
            "current_result": "fail_current_claim",
            "missing": "sector boundary conditions for L_X plus B_ref/B_class variation",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "lock_id": "BCL668_1_reference_fixed_branch",
            "boundary_condition": "delta B_ref has no source/surface/frame/time/range derivative",
            "needed_for": "Delta_ref_over_MH=0",
            "current_result": "fail_current_claim",
            "missing": "parent-selected reference branch",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "lock_id": "BCL668_2_relative_class",
            "boundary_condition": "relative boundary class C_top is selected by parent topology and not by readout",
            "needed_for": "B_zero_flux_over_MH=0",
            "current_result": "fail_current_claim",
            "missing": "trivial relative class proof or source-backed boundary flux",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "lock_id": "BCL668_3_no_vector_tensor_hair",
            "boundary_condition": "boundary stress has no vector, trace-free tensor, shear, radial, or time hair",
            "needed_for": "symplectic_boundary_flux_over_MH=0 and PPN preferred-frame safety",
            "current_result": "fail_current_claim",
            "missing": "boundary action/nohair theorem",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "lock_id": "BCL668_4_domain_projector_fixed",
            "boundary_condition": "domain/projector variables have no metric variation stress or local flux",
            "needed_for": "projector silence and preferred-frame locks",
            "current_result": "fail_current_claim",
            "missing": "parent-owned topological/first-class projector-domain action",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "lock_id": "BCL668_5_stationary_tau",
            "boundary_condition": "tau is fixed across charge, clocks, source variation, and readout",
            "needed_for": "time_generator_lock",
            "current_result": "fail_current_claim",
            "missing": "observed tau/coframe functor",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "lock_id": "BCL668_6_worldtube_linking_surfaces",
            "boundary_condition": "S_inner and S_outer link the same source worldtube with no source support in the annulus",
            "needed_for": "source measure and radial closure",
            "current_result": "setup_allowed_not_calibration",
            "missing": "same-frame source equality and measured-GM readout",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def lagrangian_owner_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "LOG668_0_EH_template",
            "gate": "EH local metric operator is available as conditional template",
            "result": "pass_conditional",
            "reason": "formal EH block exists but operator selection is not parent-derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "LOG668_1_matter_owner",
            "gate": "matter/coframe source owner is parent-derived",
            "result": "fail_current_claim",
            "reason": "one observed geometry remains closure-labelled and constants/material labels are open",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "LOG668_2_LX_owner",
            "gate": "every MTS extra sector has L_X, Theta_X, Q_X, and boundary conditions",
            "result": "fail_current_claim",
            "reason": "the sector Lagrangian owner is missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "LOG668_3_boundary_owner",
            "gate": "B_ref and B_class are parent-selected",
            "result": "fail_current_claim",
            "reason": "reference and relative boundary class are still contracts",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "LOG668_4_tau_source_owner",
            "gate": "tau and measured source denominator are parent-owned",
            "result": "fail_current_claim",
            "reason": "tau functor, source-measure equality, and Gauss readout are missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "LOG668_5_FB5540_owner_lock",
            "gate": "all owners needed for FB554_0 zero are signed",
            "result": "blocked_as_expected",
            "reason": "L_X, B_ref, B_class, tau, and M_H_ref are unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def fb5540_impact_map_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "impact_id": "IM668_0_delta_H_tau",
            "FB5540_quantity": "delta_H_tau_nonintegrable_over_MH",
            "owner_needed": "L_X;Theta_X;Q_X;B_total;tau;domain/projector variation",
            "current_owner_status": "missing_LX_and_boundary_conditions",
            "effect": "integrability remains unproved",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "impact_id": "IM668_1_Delta_ref",
            "FB5540_quantity": "Delta_ref_over_MH",
            "owner_needed": "B_ref fixed branch",
            "current_owner_status": "missing_parent_reference_functional",
            "effect": "reference residual retained",
            "next_action": "after L_X owner, attack B_ref derivative silence",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "impact_id": "IM668_2_symplectic_boundary_flux",
            "FB5540_quantity": "symplectic_boundary_flux_over_MH",
            "owner_needed": "B_class;C_top;boundary nohair;projector/domain silence",
            "current_owner_status": "missing_boundary_class_and_projector_silence",
            "effect": "boundary/projector residual retained",
            "next_action": "after L_X owner, lock boundary class/nohair or residualize",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "impact_id": "IM668_3_tau_lock",
            "FB5540_quantity": "time_generator_lock",
            "owner_needed": "observed tau/coframe functor",
            "current_owner_status": "missing_observed_tau_functor",
            "effect": "same-frame Hamiltonian source charge not signed",
            "next_action": "matter/coframe functor theorem or residual mismatch row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "impact_id": "IM668_4_M_H_ref",
            "FB5540_quantity": "M_H_ref",
            "owner_needed": "worldtube source equality and Poisson/Gauss readout",
            "current_owner_status": "missing_source_measure_and_Gauss_readout",
            "effect": "normalization remains guardrail only",
            "next_action": "source-measure/Gauss readout after charge owners are signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def residual_demotion_queue_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "queue_id": "RDQ668_0_LX_first",
            "priority": "1",
            "missing_owner": "L_X;Theta_X;Q_X",
            "demote_to_if_fail": "R11/R10/extra-sector residual vector with coefficients, units, profiles, source files",
            "why_first": "without L_X no integrability curl, Q_X, or extra-sector silence can be computed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "queue_id": "RDQ668_1_Bref",
            "priority": "2",
            "missing_owner": "B_ref",
            "demote_to_if_fail": "Delta_ref_over_MH value/profile row",
            "why_first": "reference can absorb source calibration unless fixed",
            "next_target": "after_669",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "queue_id": "RDQ668_2_boundary_class",
            "priority": "3",
            "missing_owner": "B_class;C_top;nohair",
            "demote_to_if_fail": "B_zero_flux/symplectic_boundary_flux value/profile rows",
            "why_first": "boundary flux is an independent local mass/PPN leakage channel",
            "next_target": "after_Bref",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "queue_id": "RDQ668_3_tau",
            "priority": "4",
            "missing_owner": "observed tau/coframe functor",
            "demote_to_if_fail": "time_generator_mismatch;Delta_frame;clock/Gdot residual rows",
            "why_first": "same source/readout frame is needed before measured mass",
            "next_target": "after_boundary",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "queue_id": "RDQ668_4_source_readout",
            "priority": "5",
            "missing_owner": "M_H_ref;GM_orbit relation",
            "demote_to_if_fail": "Delta_cal;source_normalization;PPN residual rows",
            "why_first": "do not use orbital GM as denominator before Gauss/readout theorem",
            "next_target": "after_tau",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def evaluator_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "evaluator_id": "EV668_0_owner_lock",
            "target": "sector_Lagrangian_owner_lock",
            "status": "not_claimable",
            "reason": "only EH is a conditional template; every nontrivial owner needed by FB554_0 remains unsigned, closure-labelled, or retained",
            "claim_effect": "no FB554_0 zero",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV668_1_boundary_lock",
            "target": "boundary_condition_lock",
            "status": "not_claimable",
            "reason": "B_ref, B_class, nohair, domain/projector, tau, and source worldtube readout are not simultaneously locked",
            "claim_effect": "boundary/reference residuals retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV668_2_next_route",
            "target": "minimal_LX_sector_operator_owner",
            "status": "derive_first",
            "reason": "L_X is upstream of Theta_X, Q_X, integrability, extra-sector silence, and R10/R11 residualization",
            "claim_effect": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def scoreability_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "G668_0_sources_exist",
            "gate": "every cited source path exists",
            "result": "pass",
            "detail": "checked by validation",
            "claim_effect": "evidence plumbing only",
            "generated_utc": now,
        },
        {
            "gate_id": "G668_1_prior_validations_clean",
            "gate": "prior 667/666 validations are clean",
            "result": "pass",
            "detail": "checked by validation",
            "claim_effect": "checkpoint chain usable",
            "generated_utc": now,
        },
        {
            "gate_id": "G668_2_sector_audit_complete",
            "gate": "major sectors audited for parent ownership",
            "result": "pass_nonclaim",
            "detail": "EH, matter, L_X, boundary, projector/domain, tau, source normalization, constants, and memory rows written",
            "claim_effect": "owner map only",
            "generated_utc": now,
        },
        {
            "gate_id": "G668_3_boundary_lock_attempted",
            "gate": "boundary condition lock attempted",
            "result": "blocked_as_expected",
            "detail": "reference, boundary class/nohair, projector/domain, tau, and source readout locks fail current claim",
            "claim_effect": "no boundary/reference pass",
            "generated_utc": now,
        },
        {
            "gate_id": "G668_4_LX_next_selected",
            "gate": "minimal L_X sector owner selected first",
            "result": "pass",
            "detail": "L_X is upstream of Theta_X, Q_X, integrability, extra-sector silence, R10, and R11",
            "claim_effect": "next target only",
            "generated_utc": now,
        },
        {
            "gate_id": "G668_5_no_claim_rows",
            "gate": "all generated rows remain nonclaim",
            "result": "pass",
            "detail": CLAIM_CEILING,
            "claim_effect": "private derivation audit only",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D668_0_owner_lock",
            "status": "not_signed",
            "meaning": "sector Lagrangian ownership is not closed; EH is conditional and all critical non-EH/source/boundary owners remain open",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D668_1_boundary_conditions",
            "status": "not_locked",
            "meaning": "boundary/reference conditions are mapped but not parent-selected",
            "claim_status": "false",
            "next_action": "after_LX_owner_attempt",
            "generated_utc": now,
        },
        {
            "decision_id": "D668_2_best_route",
            "status": "LX_first",
            "meaning": "minimal L_X owner is the least-vague next target because it determines Theta_X, Q_X, C_X, omega_X, R10, and R11 rows",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
    ]


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for path in FORMALIZATION_WORKBENCH.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def prior_validation_failures(source_id: str) -> list[str]:
    rows = read_csv(SOURCE_PATHS[source_id])
    return [row.get("check_id", row.get("validation_id", "?")) for row in rows if row.get("result") != "pass"]


def validation_rows(
    source_rows: list[dict[str, str]],
    sector_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    owner_gate_rows: list[dict[str, str]],
    impact_rows: list[dict[str, str]],
    queue_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    def add(check_id: str, result: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if result else "fail",
                "detail": detail,
                "generated_utc": now,
            }
        )

    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    add("V668_0_sources_exist", not missing_sources, "missing=" + ";".join(missing_sources))

    flat_prior_failures = [
        f"{source_id}:{failure}"
        for source_id in ["667_validation", "666_validation"]
        for failure in prior_validation_failures(source_id)
    ]
    add("V668_1_prior_validations_clean", not flat_prior_failures, "prior_failures=" + ";".join(flat_prior_failures))

    sector_ids = {row["sector_id"] for row in sector_rows}
    required_sectors = {f"SO668_{index}_{suffix}" for index, suffix in [
        (0, "EH_metric"),
        (1, "observed_matter"),
        (2, "MTS_extra_LX"),
        (3, "boundary_reference"),
        (4, "boundary_class_nohair"),
        (5, "projector_domain"),
        (6, "tau_clock"),
        (7, "source_normalization"),
        (8, "constants_couplings"),
        (9, "memory_kernel"),
    ]}
    add("V668_2_sector_owner_coverage", required_sectors.issubset(sector_ids), "sector_ids=" + ";".join(sorted(sector_ids)))

    boundary_ids = {row["lock_id"] for row in boundary_rows}
    required_boundary = {f"BCL668_{index}_{suffix}" for index, suffix in [
        (0, "variational_principle"),
        (1, "reference_fixed_branch"),
        (2, "relative_class"),
        (3, "no_vector_tensor_hair"),
        (4, "domain_projector_fixed"),
        (5, "stationary_tau"),
        (6, "worldtube_linking_surfaces"),
    ]}
    add("V668_3_boundary_lock_coverage", required_boundary.issubset(boundary_ids), "lock_ids=" + ";".join(sorted(boundary_ids)))

    owner_gate_ids = {row["gate_id"] for row in owner_gate_rows}
    required_owner_gates = {"LOG668_0_EH_template", "LOG668_1_matter_owner", "LOG668_2_LX_owner", "LOG668_3_boundary_owner", "LOG668_4_tau_source_owner", "LOG668_5_FB5540_owner_lock"}
    add("V668_4_owner_gate_coverage", required_owner_gates.issubset(owner_gate_ids), "owner_gate_ids=" + ";".join(sorted(owner_gate_ids)))

    owner_lock_block = [row for row in owner_gate_rows if row["gate_id"] == "LOG668_5_FB5540_owner_lock" and row["result"] == "blocked_as_expected"]
    add("V668_5_FB5540_owner_lock_blocked", len(owner_lock_block) == 1, "blocked_rows=" + str(len(owner_lock_block)))

    impact_ids = {row["impact_id"] for row in impact_rows}
    required_impacts = {"IM668_0_delta_H_tau", "IM668_1_Delta_ref", "IM668_2_symplectic_boundary_flux", "IM668_3_tau_lock", "IM668_4_M_H_ref"}
    add("V668_6_FB5540_impact_coverage", required_impacts.issubset(impact_ids), "impact_ids=" + ";".join(sorted(impact_ids)))

    queue_first = [row for row in queue_rows if row["queue_id"] == "RDQ668_0_LX_first" and row["next_target"] == NEXT_TARGET]
    add("V668_7_LX_next_selected", len(queue_first) == 1, "LX_first_rows=" + str(len(queue_first)))

    all_valid_flags = [
        row.get("valid_for_claim")
        for row_group in (sector_rows, boundary_rows, owner_gate_rows, impact_rows, queue_rows, evaluator_data)
        for row in row_group
    ]
    add("V668_8_no_generated_claim_rows", all(flag == "false" for flag in all_valid_flags), "valid_for_claim_flags=" + ";".join(sorted(set(all_valid_flags))))

    evaluator_claims = [row for row in evaluator_data if row["valid_for_claim"] != "false" or row["status"] not in {"not_claimable", "derive_first"}]
    add("V668_9_evaluator_nonclaim", not evaluator_claims, "claimlike_evaluator_rows=" + str(len(evaluator_claims)))

    blocked_gates = {row["gate_id"] for row in gate_rows if row["result"] == "blocked_as_expected"}
    add("V668_10_blocked_gate_present", "G668_3_boundary_lock_attempted" in blocked_gates, "blocked_gates=" + ";".join(sorted(blocked_gates)))

    next_target_rows = [row for row in decision if row["next_action"] == NEXT_TARGET]
    add("V668_11_next_target_selected", bool(next_target_rows), NEXT_TARGET)

    changed = formalization_changed_after_cutoff()
    add("V668_12_formalization_workbench_untouched", changed == 0, "formalization_changed_after_cutoff=" + str(changed))

    add("V668_13_status_nonclaim", STATUS.endswith("nonclaim") and "no_FB5540_zero" in CLAIM_CEILING, STATUS)

    return rows


def nonclaim_summary_rows(
    sector_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    owner_gate_rows: list[dict[str, str]],
    impact_rows: list[dict[str, str]],
    queue_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    blocked_gates = [row["gate_id"] for row in gate_rows if row["result"] in {"blocked_as_expected", "pass_nonclaim"}]
    failures = [row["check_id"] for row in validation if row["result"] != "pass"]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "sector_rows": str(len(sector_rows)),
            "boundary_rows": str(len(boundary_rows)),
            "owner_gate_rows": str(len(owner_gate_rows)),
            "impact_rows": str(len(impact_rows)),
            "queue_rows": str(len(queue_rows)),
            "evaluator_rows": str(len(evaluator_data)),
            "blocked_or_nonclaim_gates": ";".join(blocked_gates),
            "validation_failures": ";".join(failures),
            "next_target": NEXT_TARGET,
            "generated_utc": now,
        }
    ]


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, str]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |\n"
    separator = "| " + " | ".join("---" for _ in fields) + " |\n"
    body = "".join("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |\n" for row in rows)
    return header + separator + body


def write_document(
    source_rows: list[dict[str, str]],
    sector_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    owner_gate_rows: list[dict[str, str]],
    impact_rows: list[dict[str, str]],
    queue_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    doc = f"""# 668 - Y5 R10 Sector Lagrangian Owner And Boundary Condition Lock

## Verdict

668 audited whether the pieces in the 667 parent action scaffold are actually owned by the current corpus.

Short version: no full owner lock yet. The EH metric block is a useful conditional template, but the pieces that matter for `FB554_0` are still unsigned:

```text
L_X, Theta_X, Q_X
B_ref
B_class / C_top / boundary no-hair
tau observed-frame functor
M_H_ref / measured-GM readout
```

So `FB554_0=0` is still not proved. The cleanest next target is `L_X`, because without it we cannot compute `Theta_X`, `Q_X`, `omega_X`, `C_X`, R10 force channels, or the R11 operator vector.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "role"])}

## Sector Owner Audit

{markdown_table(sector_rows, ["sector_id", "sector", "candidate_Lagrangian", "owner_status", "owned_if", "current_blocker", "feeds", "valid_for_claim"])}

## Boundary Condition Lock

{markdown_table(boundary_rows, ["lock_id", "boundary_condition", "needed_for", "current_result", "missing", "valid_for_claim"])}

## Lagrangian Owner Gates

{markdown_table(owner_gate_rows, ["gate_id", "gate", "result", "reason", "valid_for_claim"])}

## FB5540 Impact Map

{markdown_table(impact_rows, ["impact_id", "FB5540_quantity", "owner_needed", "current_owner_status", "effect", "next_action", "valid_for_claim"])}

## Residual Demotion Queue

{markdown_table(queue_rows, ["queue_id", "priority", "missing_owner", "demote_to_if_fail", "why_first", "next_target", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator_data, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Scoreability Gates

{markdown_table(gate_rows, ["gate_id", "gate", "result", "detail", "claim_effect"])}

## Decision

{markdown_table(decision, ["decision_id", "status", "meaning", "claim_status", "next_action"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "sector_rows", "boundary_rows", "owner_gate_rows", "impact_rows", "queue_rows", "evaluator_rows", "blocked_or_nonclaim_gates", "validation_failures", "next_target"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Interpretation

This is a good narrowing. We are no longer asking vaguely whether "the parent action works." The immediate upstream object is `L_X`: the sector Lagrangian owner for the MTS-extra fields. If `L_X` can be written with positive/silent/source-free local behaviour, the integrability and R10/R11 gates become mathematical. If not, those sectors must become explicit residual vectors rather than quiet assumptions.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    sector_rows = sector_owner_audit_rows()
    boundary_rows = boundary_condition_lock_rows()
    owner_gate_rows = lagrangian_owner_gate_rows()
    impact_rows = fb5540_impact_map_rows()
    queue_rows = residual_demotion_queue_rows()
    evaluator_data = evaluator_rows()
    gate_rows = scoreability_gate_rows()
    decision = decision_rows()
    validation = validation_rows(source_rows, sector_rows, boundary_rows, owner_gate_rows, impact_rows, queue_rows, evaluator_data, gate_rows, decision)
    summary_rows = nonclaim_summary_rows(sector_rows, boundary_rows, owner_gate_rows, impact_rows, queue_rows, evaluator_data, gate_rows, validation)

    write_csv(RESIDUALS / "P8_Y5_R10_668_SOURCE_REGISTER.csv", source_rows, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(
        RESIDUALS / "P8_Y5_R10_668_SECTOR_OWNER_AUDIT.csv",
        sector_rows,
        ["sector_id", "sector", "candidate_Lagrangian", "owner_status", "owned_if", "current_blocker", "feeds", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_668_BOUNDARY_CONDITION_LOCK.csv",
        boundary_rows,
        ["lock_id", "boundary_condition", "needed_for", "current_result", "missing", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_668_LAGRANGIAN_OWNER_GATES.csv",
        owner_gate_rows,
        ["gate_id", "gate", "result", "reason", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_668_FB5540_IMPACT_MAP.csv",
        impact_rows,
        ["impact_id", "FB5540_quantity", "owner_needed", "current_owner_status", "effect", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_668_RESIDUAL_DEMOTION_QUEUE.csv",
        queue_rows,
        ["queue_id", "priority", "missing_owner", "demote_to_if_fail", "why_first", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_668_EVALUATOR.csv",
        evaluator_data,
        ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_668_SCOREABILITY_GATES.csv",
        gate_rows,
        ["gate_id", "gate", "result", "detail", "claim_effect", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_668_DECISION.csv",
        decision,
        ["decision_id", "status", "meaning", "claim_status", "next_action", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_668_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "sector_rows",
            "boundary_rows",
            "owner_gate_rows",
            "impact_rows",
            "queue_rows",
            "evaluator_rows",
            "blocked_or_nonclaim_gates",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(RESIDUALS / "P8_Y5_BRR545_668_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_document(source_rows, sector_rows, boundary_rows, owner_gate_rows, impact_rows, queue_rows, evaluator_data, gate_rows, decision, summary_rows, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"sector_rows={len(sector_rows)}")
    print(f"boundary_rows={len(boundary_rows)}")
    print(f"owner_gate_rows={len(owner_gate_rows)}")
    print(f"impact_rows={len(impact_rows)}")
    print(f"queue_rows={len(queue_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
