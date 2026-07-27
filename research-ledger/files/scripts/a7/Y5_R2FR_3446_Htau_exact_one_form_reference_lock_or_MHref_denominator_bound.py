from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3446-Y5-R2FR-Htau-exact-one-form-reference-lock-or-MHref-denominator-bound-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3445": ROOT / "3445-Y5-R2FR-Hilbert-identity-PiM-parent-adoption-or-Htau-source-current-lock-under-AX1090.md",
    "next_3445": OUT / "P8_Y5_R2FR_3445_NEXT_TARGET.csv",
    "htau_lock_3445": OUT / "P8_Y5_R2FR_3445_HTAU_SOURCE_CURRENT_LOCK_AUDIT.csv",
    "residual_3445": OUT / "P8_Y5_R2FR_3445_RESIDUAL_VECTOR_AFTER_PIMH_ADOPTION.csv",
    "pc3400_3445": OUT / "P8_Y5_R2FR_3445_PC3400_3_UPDATE.csv",
    "curl_law_3208": OUT / "P8_Y5_R2FR_3208_HTAU_ONE_FORM_CURL_LAW.csv",
    "curl_audit_2667": OUT / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_CURL_PROOF_AUDIT.csv",
    "integrability_gate_2667": OUT / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv",
    "reference_lock_1017": OUT / "P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv",
    "reference_selector_2382": OUT / "P8_Y5_PARENT_QLOC_2382_FIXED_REFERENCE_SELECTOR_THEOREM.csv",
    "htau_href_status_2351": OUT / "P8_Y5_PARENT_QLOC_2351_HTAU_HREF_SOURCE_ROW_STATUS.csv",
    "mhref_schema_1017": OUT / "P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv",
    "theta_qtau_reference_2339": OUT / "P8_Y5_PARENT_QLOC_2339_THETA_QTAU_FIXED_REFERENCE_AUDIT.csv",
    "theta_qtau_owner_1646": OUT / "P8_Y5_PARENT_QLOC_1646_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
    "hamiltonian_charge_contract": OUT / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
    "htau_certificate_2445": OUT / "P8_Y5_PARENT_QLOC_2445_HTAU_SOURCE_CHARGE_CERTIFICATE_AUDIT.csv",
    "htau_mhref_1732": OUT / "P8_Y5_PARENT_QLOC_1732_HTAU_MHREF_SOURCE_ROWS.csv",
    "htau_worldtube_2938": OUT / "P8_Y5_R2FR_2938_HTAU_WORLDTUBE_SOURCE_MEASURE_THEOREM_ATTEMPT.csv",
    "htau_extraction_3006": OUT / "P8_Y5_R2FR_3006_HTAU_EXTRACTION_ROWS.csv",
    "parent_adoption_3445": OUT / "P8_Y5_R2FR_3445_HILBERT_IDENTITY_PIM_PARENT_ADOPTION_CONTRACT.csv",
    "commutator_reduction_3445": OUT / "P8_Y5_R2FR_3445_COMMUTATOR_REDUCTION.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3446_SOURCE_REGISTER.csv",
    "exact_one_form_theorem": OUT / "P8_Y5_R2FR_3446_HTAU_EXACT_ONE_FORM_THEOREM.csv",
    "reference_lock_split": OUT / "P8_Y5_R2FR_3446_REFERENCE_LOCK_SPLIT.csv",
    "denominator_bound_rows": OUT / "P8_Y5_R2FR_3446_MHREF_DENOMINATOR_BOUND_ROWS.csv",
    "pimh_carryforward": OUT / "P8_Y5_R2FR_3446_PIMH_CARRYFORWARD.csv",
    "source_denominator_residual": OUT / "P8_Y5_R2FR_3446_SOURCE_DENOMINATOR_RESIDUAL_VECTOR.csv",
    "pc3400_update": OUT / "P8_Y5_R2FR_3446_PC3400_3_HTAU_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3446_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3446_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3446_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3446_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3446_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3445": "immediate Htau handoff",
        "next_3445": "machine-readable 3446 target",
        "htau_lock_3445": "Htau lock audit",
        "residual_3445": "denominator residual vector target",
        "pc3400_3445": "PC3400.3 split after PiMH adoption",
        "curl_law_3208": "closed-one-form and field-space Stokes law",
        "curl_audit_2667": "prior Htau curl audit",
        "integrability_gate_2667": "integrability gates",
        "reference_lock_1017": "reference/tau/MHref lock law",
        "reference_selector_2382": "source-blind reference selector theorem",
        "htau_href_status_2351": "Htau/Href source row status",
        "mhref_schema_1017": "M_H_ref first-row schema",
        "theta_qtau_reference_2339": "theta/Q_tau/fixed-reference audit",
        "theta_qtau_owner_1646": "parent current owner audit",
        "hamiltonian_charge_contract": "mass-current Hamiltonian charge contract",
        "htau_certificate_2445": "Htau source-charge certificate blockers",
        "htau_mhref_1732": "M_H_ref source rows",
        "htau_worldtube_2938": "Htau/worldtube source measure theorem",
        "htau_extraction_3006": "theta/Q_tau/Htau extraction rows",
        "parent_adoption_3445": "PiMH branch adoption contract",
        "commutator_reduction_3445": "PiMH commutator carryforward",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path in SOURCES.items()
    ]


def exact_one_form_theorem() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "HOT3446_0_define_alpha",
            "claim_piece": "Hamiltonian variation one-form",
            "statement": "alpha_tau(delta Phi)=int_S(delta Q_tau^MTS-i_tau Theta_MTS(delta Phi))-delta H_ref",
            "derivation": "This is the covariant phase-space definition of the Hamiltonian variation on a fixed branch.",
            "result": "EXACT_CONDITIONAL_DEFINITION",
            "missing_to_promote": "Theta_MTS, Q_tau^MTS, tau_id, surface_pair and fixed H_ref must be parent-owned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "HOT3446_1_curl_law",
            "claim_piece": "field-space curl law",
            "statement": "d_F alpha_tau(delta_1,delta_2)=-int_S i_tau omega_MTS(delta_1,delta_2)+C_tau+C_S+C_ref",
            "derivation": "For fixed tau, surface class and reference selector, only the symplectic flux term remains; moving branch data add explicit correction terms rather than hidden H_tau shifts.",
            "result": "DERIVED_ACCOUNTING_IDENTITY",
            "missing_to_promote": "sector omega_MTS, boundary pullback units, tau/surface/reference variation rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "HOT3446_2_exact_denominator_route",
            "claim_piece": "H_tau-H_ref as state-function denominator",
            "statement": "If d_F alpha_tau=0 on the allowed local branch and H_ref is fixed/source-blind, then H_tau exists path-independently and M_H_ref:=H_tau[S_outer]-H_ref can be a pre-orbit source denominator.",
            "derivation": "A closed one-form on the branch integrates to a state function. Positivity and same-frame/source-current equality are separate gates, so exactness alone is not enough for Newton.",
            "result": "EXACT_IF_CLOSED_ONE_FORM_REFERENCE_AND_POSITIVITY_LOCKS_PASS",
            "missing_to_promote": "all curl components theorem-zero, positive same-frame M_H_ref, no orbital-GM import",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "HOT3446_3_bound_route",
            "claim_piece": "non-integrable denominator bound",
            "statement": "|Delta H_tau(path_1,path_0)| <= int_BF |d_F alpha_tau| <= A_F sup_BF |d_F alpha_tau|",
            "derivation": "Field-space Stokes converts nonzero curl into an explicit denominator ambiguity bound. This is the correct fallback if exactness fails.",
            "result": "DERIVED_BOUND_ROUTE_NO_NUMERIC_VALUES",
            "missing_to_promote": "field-space patch B_F, area/norm convention, component sup bounds, M_H_ref lower bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "HOT3446_4_verdict",
            "claim_piece": "current H_tau exactness",
            "statement": "The exact theorem shape exists, but current MTS does not parent-own Theta/Q_tau, curl silence, fixed reference, tau/surface lock or M_H_ref positivity together.",
            "derivation": "The result is not another vague gap: it is a precise denominator residual vector with a Stokes-bound route.",
            "result": "HTAU_DENOMINATOR_NOT_PROMOTED_BOUND_VECTOR_REQUIRED",
            "missing_to_promote": "Theta/Q_tau parent current extraction is the next root",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def reference_lock_split() -> list[dict[str, Any]]:
    return [
        {
            "lock_id": "RLS3446_0_selector",
            "object": "Sigma_ref",
            "zero_condition": "Sigma_ref depends only on fixed boundary class, topology, orientation/corner convention, asymptotic coframe, tau convention and stationary/vacuum branch data",
            "exact_rule": "if D_source Sigma_ref=0 then D_source H_ref=0 by chain rule",
            "current_status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "fallback_component": "epsilon_ref_source",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "lock_id": "RLS3446_1_no_GM_laundering",
            "object": "H_ref provenance",
            "zero_condition": "partial_{GM_obs,M_fit,M_H_ref,kappa_A,composition_A} Sigma_ref=0 before source bridge is derived",
            "exact_rule": "forbid any reference selector that uses the target measured source normalization",
            "current_status": "FORBIDDEN_INPUT_RULE_ACTIVE_SOURCE_CERTIFICATE_MISSING",
            "fallback_component": "epsilon_ref_laundering_guard",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "lock_id": "RLS3446_2_surface_no_retune",
            "object": "S_outer/S_inner/reference surface class",
            "zero_condition": "linked surfaces stay in one parent boundary class and are not retuned with source/radius/orbit",
            "exact_rule": "D_source S=0 and D_source corner convention=0",
            "current_status": "CONDITIONAL_ROUTE_NOT_SIGNED",
            "fallback_component": "epsilon_surface_retune",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "lock_id": "RLS3446_3_same_frame_sidecar",
            "object": "M_H_ref denominator frame",
            "zero_condition": "M_H_ref is finite, positive, same tau/coframe/frame and not imported from orbital GM",
            "exact_rule": "all normalized reference/curl residuals use this denominator only after it is independently sourced",
            "current_status": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "fallback_component": "M_H_ref_lower_bound_missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def denominator_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DBR3446_0_M_H_ref",
            "quantity": "M_H_ref",
            "definition": "positive same-frame Hamiltonian source denominator H_tau[S_outer]-H_ref for the Pi_M^H branch",
            "formula": "M_H_ref := H_tau[tau_obs,S_outer]-H_ref[S_outer]",
            "required_columns": "system_id;tau_id;frame_id;surface_outer;Q_tau_integral;H_ref;M_H_ref;M_H_ref_lower;units;reference_rule;source_path;no_orbital_GM",
            "current_status": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "numeric_or_theorem_value": "MISSING_M_H_REF",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DBR3446_1_delta_H_curl",
            "quantity": "Delta_H_curl_bound",
            "definition": "field-space path-dependence of H_tau from nonzero d_F alpha_tau",
            "formula": "int_BF |d_F alpha_tau| <= A_F sup_BF|-int_S i_tau omega_MTS + C_tau+C_S+C_ref|",
            "required_columns": "system_id;field_space_patch;variation_pair;A_F;curl_sup_bound;components;units;source_path",
            "current_status": "MISSING_CURL_COMPONENT_BOUNDS",
            "numeric_or_theorem_value": "MISSING_DELTA_H_CURL_BOUND",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DBR3446_2_reference_shift",
            "quantity": "Delta_ref_over_MH",
            "definition": "source/range/time/frame dependence of H_ref or reference subtraction normalized by M_H_ref",
            "formula": "abs(Delta_ref)/M_H_ref_lower if source-blind reference theorem is not signed",
            "required_columns": "system_id;reference_selector;Delta_ref;derivative_profile;M_H_ref_lower;units;source_path;no_GM_laundering",
            "current_status": "MISSING_REFERENCE_ZERO_OR_VALUE",
            "numeric_or_theorem_value": "MISSING_DELTA_REF",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DBR3446_3_tau_surface_frame",
            "quantity": "epsilon_tau_surface_frame",
            "definition": "mismatch from tau, surface, coframe or frame moving between source charge, clocks, orbitals, PPN and R10",
            "formula": "(abs(C_tau)+abs(C_S)+abs(C_frame))/M_H_ref_lower",
            "required_columns": "system_id;tau_source;tau_charge;tau_clock;tau_readout;surface_pair;frame_id;mismatch_bound;units;source_path",
            "current_status": "MISSING_TAU_SURFACE_FRAME_LOCK_OR_BOUND",
            "numeric_or_theorem_value": "MISSING_TAU_SURFACE_FRAME_BOUND",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DBR3446_4_symplectic_boundary",
            "quantity": "epsilon_symplectic_boundary",
            "definition": "boundary/corner/projector/non-EH symplectic flux contribution to H_tau exactness",
            "formula": "abs(int_S i_tau omega_extra + B_zero_flux + Delta_symp)/M_H_ref_lower",
            "required_columns": "system_id;sector;surface_pair;symplectic_boundary_flux;B_zero_flux;Delta_symp;M_H_ref_lower;units;source_path",
            "current_status": "MISSING_SYMPLECTIC_BOUNDARY_ZERO_OR_BOUND",
            "numeric_or_theorem_value": "MISSING_SYMPLECTIC_BOUNDARY_BOUND",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DBR3446_5_epsilon_den_total",
            "quantity": "epsilon_Htau_denominator_abs",
            "definition": "absolute no-cancellation denominator residual after Pi_M^H adoption",
            "formula": "(abs(Delta_H_curl_bound)+abs(Delta_ref)+abs(C_tau)+abs(C_S)+abs(C_frame)+abs(symplectic_boundary_flux))/M_H_ref_lower",
            "required_columns": "all DBR3446_0..4 component columns plus source_paths and no_cancellation_flag",
            "current_status": "MISSING_COMPONENT_VALUES_TOTAL_NONCLAIM",
            "numeric_or_theorem_value": "MISSING_COMPONENT_VALUES",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def pimh_carryforward() -> list[dict[str, Any]]:
    return [
        {
            "carry_id": "PCH3446_0_commutator",
            "quantity": "I_commutator^H",
            "3445_status": "0 in the Hilbert identity branch",
            "3446_effect": "removed from the denominator residual unless non-identity PiM is reintroduced",
            "reactivates_if": "old topological, Hodge, Green, DeWitt, domain or post-readout PiM is used",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "carry_id": "PCH3446_1_projector_stress",
            "quantity": "epsilon_projector_stress^H",
            "3445_status": "no independent projector stress for identity/inclusion map",
            "3446_effect": "not part of H_tau curl for preferred Pi_M^H branch",
            "reactivates_if": "metric/domain projector replaces Pi_M^H",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "carry_id": "PCH3446_2_extra_current",
            "quantity": "-Pi_M^H dJ_extra",
            "3445_status": "retained",
            "3446_effect": "not solved by H_tau exactness; remains separate source-exchange term in Omega_GM^H",
            "reactivates_if": "always live until extra-current zero theorem or source-bound vector exists",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def source_denominator_residual() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "SDR3446_0_denominator",
            "symbol": "epsilon_Htau_denominator_abs",
            "definition": "absolute H_tau/H_ref/tau/reference/symplectic denominator ambiguity normalized by M_H_ref_lower",
            "after_3446": "exact formula and bound schema derived, values missing",
            "zero_or_bound_next": "derive theta/Q_tau/current-chain exactness or fill DBR3446 rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "SDR3446_1_total_source_bridge",
            "symbol": "Omega_GM^H",
            "definition": "-Pi_M^H dJ_extra + A_parent + Delta_coupling + Delta_cal + Delta_PPN + epsilon_Htau_denominator_abs",
            "after_3446": "I_commutator^H removed; denominator residual isolated; extra/current/coupling terms still live",
            "zero_or_bound_next": "attack parent theta/Q_tau extraction, then source-exchange/coupling calibration",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def pc3400_update() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "PCU3446_0_PC3400_3",
            "pc_clause": "PC3400_3_Htau_PiM_chain",
            "before": "PiM chain-map component solved conditionally by Pi_M^H; H_tau/MHref/reference/tau still unsigned",
            "after": "H_tau exactness is reduced to closed-one-form plus source-blind reference plus positive same-frame M_H_ref",
            "delta": "PC3400_3 is now blocked by theta/Q_tau/current-chain and denominator rows, not by PiM commutator",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "update_id": "PCU3446_1_RSB3424_0",
            "pc_clause": "epsilon_HPiM_Z",
            "before": "|partial_Z ln(M_H/(J_H^M))| + epsilon_Htau_curl + epsilon_ref + epsilon_tau_frame",
            "after": "epsilon_Htau_denominator_abs with explicit DBR3446 component rows and field-space Stokes bound",
            "delta": "source denominator ambiguity is executable as a future bound vector",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3446_0_sources",
            "claim": "all 3446 cited source paths exist",
            "gate_pass": all(path.exists() for path in SOURCES.values()),
            "reason": "source register path check",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3446_1_closed_one_form_theorem",
            "claim": "the exact H_tau closed-one-form theorem and Stokes bound are written",
            "gate_pass": True,
            "reason": "HOT3446_2 and HOT3446_3 provide exact and bound routes",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3446_2_Htau_exactness_claim",
            "claim": "H_tau-H_ref is currently a parent-signed exact denominator",
            "gate_pass": False,
            "reason": "Theta/Q_tau, d_F alpha closure, reference selector, tau/frame and M_H_ref positivity are not all signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3446_3_bound_rows_ready",
            "claim": "denominator bound rows are schema-ready but nonclaim",
            "gate_pass": True,
            "reason": "DBR3446 rows name components, required columns and no-cancellation total",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3446_4_local_GR_Newton",
            "claim": "local GR/Newton/source coupling can be promoted",
            "gate_pass": False,
            "reason": "denominator values/source proofs, extra-current projection, coupling and PPN calibration remain live",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3446_0_Htau_status",
            "decision": "Do not treat H_tau as a denominator unless alpha_tau is closed or bounded.",
            "because": "non-integrable Hamiltonian variation is path-dependent and can hide source-normalization drift",
            "next_action": "attack Theta/Q_tau parent current extraction first",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3446_1_bound_route",
            "decision": "Use field-space Stokes as the fallback instead of handwaving integrability.",
            "because": "it turns failure of exactness into a quantitative residual route once component bounds exist",
            "next_action": "fill Delta_H_curl_bound, Delta_ref, tau/surface/frame and M_H_ref_lower rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3446_2_PiM_not_reopened",
            "decision": "Do not reopen the PiM commutator while staying in the Hilbert-identity branch.",
            "because": "3445 already killed I_commutator^H; the remaining obstruction is denominator ownership",
            "next_action": "only reactivate I_commutator if a non-identity PiM branch is used",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3447-Y5-R2FR-parent-Theta-Q_tau-extraction-or-deltaH-curl-first-component-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3447_parent_Theta_Qtau_extraction_or_deltaHcurl_first_component_row.py",
            "objective": "extract or bound the first missing H_tau denominator component by deriving parent Theta_MTS and Q_tau^MTS for the adopted Hilbert-identity branch; if extraction fails, stage the first source-backed Delta_H_curl component row with units, surface pair, variation pair and source path",
            "success_condition": "Theta/Q_tau owner chain exists for the local branch, or DBR3446_1 receives a schema-valid nonclaim component row instead of staying symbolic",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3446_0_exact_route",
            "branch": "Pi_M^H_Htau_denominator",
            "closed_one_form_theorem_written": True,
            "theta_qtau_owned": False,
            "mhref_positive": False,
            "score_ready": False,
            "result": "EXACT_ROUTE_DEFINED_NOT_CLAIM_READY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN3446_1_bound_route",
            "branch": "Htau_field_space_Stokes_bound",
            "closed_one_form_theorem_written": True,
            "theta_qtau_owned": False,
            "mhref_positive": False,
            "score_ready": False,
            "result": "BOUND_SCHEMA_READY_VALUES_MISSING_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1
            for checked_path in FORMALIZATION.rglob("*")
            if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )

    nonclaim_ok = True
    for output_name, rows in rows_by_name.items():
        if output_name == "validation":
            continue
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                nonclaim_ok = False
            if str(row.get("claim_allowed", "")).lower() == "true":
                nonclaim_ok = False

    parse_ok = True
    for output_name, path in OUTPUTS.items():
        if output_name == "validation":
            continue
        if path.exists():
            try:
                read_csv(path)
            except csv.Error:
                parse_ok = False

    validations = [
        {
            "check_id": "VAL3446_0_sources_exist",
            "condition": "all cited 3446 source paths exist",
            "passed": all(path.exists() for path in SOURCES.values()),
            "detail": f"{sum(1 for path in SOURCES.values() if path.exists())}/{len(SOURCES)} source paths exist",
        },
        {
            "check_id": "VAL3446_1_closed_one_form",
            "condition": "exact closed-one-form theorem route is present",
            "passed": any(row["theorem_id"] == "HOT3446_2_exact_denominator_route" for row in rows_by_name["exact_one_form_theorem"]),
            "detail": "H_tau exact route written",
        },
        {
            "check_id": "VAL3446_2_stokes_bound",
            "condition": "field-space Stokes fallback bound is present",
            "passed": any(row["theorem_id"] == "HOT3446_3_bound_route" for row in rows_by_name["exact_one_form_theorem"]),
            "detail": "non-integrability bound route written",
        },
        {
            "check_id": "VAL3446_3_mhref_row",
            "condition": "M_H_ref denominator row remains explicit and nonclaim",
            "passed": any(
                row["row_id"] == "DBR3446_0_M_H_ref"
                and row["current_status"] == "MISSING_POSITIVE_SAME_FRAME_MHREF"
                for row in rows_by_name["denominator_bound_rows"]
            ),
            "detail": "M_H_ref not imported from orbital GM",
        },
        {
            "check_id": "VAL3446_4_reference_split",
            "condition": "reference selector chain-rule and no-GM laundering rules are retained",
            "passed": any(row["lock_id"] == "RLS3446_0_selector" for row in rows_by_name["reference_lock_split"])
            and any(row["lock_id"] == "RLS3446_1_no_GM_laundering" for row in rows_by_name["reference_lock_split"]),
            "detail": "reference lock split written",
        },
        {
            "check_id": "VAL3446_5_PiMH_carryforward",
            "condition": "I_commutator^H remains removed and not reopened",
            "passed": any(
                row["carry_id"] == "PCH3446_0_commutator"
                and "removed" in row["3446_effect"]
                for row in rows_by_name["pimh_carryforward"]
            ),
            "detail": "PiMH improvement carried forward",
        },
        {
            "check_id": "VAL3446_6_exact_not_promoted",
            "condition": "H_tau exactness is not falsely promoted",
            "passed": any(
                row["theorem_id"] == "HOT3446_4_verdict"
                and row["result"] == "HTAU_DENOMINATOR_NOT_PROMOTED_BOUND_VECTOR_REQUIRED"
                for row in rows_by_name["exact_one_form_theorem"]
            ),
            "detail": "denominator remains nonclaim",
        },
        {
            "check_id": "VAL3446_7_next_target",
            "condition": "next target attacks Theta/Q_tau extraction or first curl row",
            "passed": rows_by_name["next_target"][0]["target_doc"].startswith("3447-Y5-R2FR-parent-Theta-Q_tau-extraction"),
            "detail": rows_by_name["next_target"][0]["target_doc"],
        },
        {
            "check_id": "VAL3446_8_generated_csv_parse",
            "condition": "generated CSV rows parse cleanly",
            "passed": parse_ok,
            "detail": "CSV reader pass for generated outputs present before validation write",
        },
        {
            "check_id": "VAL3446_9_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim_ok,
            "detail": "valid_for_claim=false and claim_allowed=false wherever present",
        },
        {
            "check_id": "VAL3446_10_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3446_11_overall",
            "condition": "3446 Htau denominator checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3446 - Htau Exact One-Form Reference Lock or MHref Denominator Bound

## Summary
- This checkpoint attacks the denominator left open by 3445: `H_tau-H_ref`.
- The exact route is now precise: define the Hamiltonian variation one-form `alpha_tau`; if `d_F alpha_tau=0`, with fixed source-blind `H_ref`, same `tau/frame`, and positive non-orbital `M_H_ref`, then `H_tau-H_ref` can be a source denominator.
- The fallback is also precise: field-space Stokes turns nonzero curl into `Delta_H_curl_bound`, which feeds an absolute denominator residual.
- Current MTS does not yet parent-own `Theta_MTS`, `Q_tau^MTS`, curl silence, fixed reference, or positive same-frame `M_H_ref`, so no local-GR/Newton promotion is allowed.
- The `Pi_M^H` win from 3445 is preserved: `I_commutator^H` stays removed in the preferred branch and is not reopened here.

## Source Register
{md_table(rows_by_name["source_register"])}

## Exact One-Form Theorem
{md_table(rows_by_name["exact_one_form_theorem"])}

## Reference Lock Split
{md_table(rows_by_name["reference_lock_split"])}

## MHref Denominator Bound Rows
{md_table(rows_by_name["denominator_bound_rows"])}

## PiMH Carryforward
{md_table(rows_by_name["pimh_carryforward"])}

## Source Denominator Residual Vector
{md_table(rows_by_name["source_denominator_residual"])}

## PC3400.3 Htau Update
{md_table(rows_by_name["pc3400_update"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
The source denominator is no longer a fog bank. Either `alpha_tau` is a closed one-form on the adopted branch, or the failure is an explicit field-space curl/reference/frame residual normalized by a non-orbital `M_H_ref`. The next honest move is `Theta_MTS` and `Q_tau^MTS`; without them, `H_tau` is not a derived mass denominator.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "exact_one_form_theorem": exact_one_form_theorem(),
        "reference_lock_split": reference_lock_split(),
        "denominator_bound_rows": denominator_bound_rows(),
        "pimh_carryforward": pimh_carryforward(),
        "source_denominator_residual": source_denominator_residual(),
        "pc3400_update": pc3400_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3446 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
