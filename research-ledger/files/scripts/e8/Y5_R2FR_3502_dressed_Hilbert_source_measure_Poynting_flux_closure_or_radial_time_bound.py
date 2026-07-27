from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3502-Y5-R2FR-dressed-Hilbert-source-measure-Poynting-flux-closure-or-radial-time-bound.md"
EM_FLUX_VECTOR = OUT / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3502": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3501": {
        "path": ROOT / "3501-Y5-R2FR-mu-extra-over-Gref-MH-vector-zero-or-coefficient-fill.md",
        "role": "3501 handoff",
    },
    "next_3501": {
        "path": OUT / "P8_Y5_R2FR_3501_NEXT_TARGET.csv",
        "role": "3501 selected next target",
    },
    "epsilon_vector_3501": {
        "path": OUT / "P8_mu_extra_over_Geff_Meff_vector.csv",
        "role": "canonical epsilon_mu vector from 3501",
    },
    "em_route_3501": {
        "path": OUT / "P8_Y5_R2FR_3501_EM_POYNTING_STRESS_ROUTE.csv",
        "role": "3501 EM/Poynting route",
    },
    "source_flux_theorem": {
        "path": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
        "role": "source measure M_eff flux theorem attempt",
    },
    "source_flux_residual_map": {
        "path": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "role": "source flux residual map",
    },
    "worldtube_measure_theorem": {
        "path": OUT / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "role": "worldtube dressed source measure theorem",
    },
    "hilbert_worldtube_glue": {
        "path": OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
        "role": "Hilbert worldtube glue theorem attempt",
    },
    "maxwell_poynting_ledger": {
        "path": OUT / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv",
        "role": "Maxwell stress and Poynting ledger",
    },
    "em_owner_package": {
        "path": OUT / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv",
        "role": "EM owner package audit",
    },
    "maxwell_descent": {
        "path": OUT / "P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv",
        "role": "Maxwell descent attempt",
    },
}


def generated_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(metadata["path"]),
            "exists": str(Path(metadata["path"]).exists()),
            "role": metadata["role"],
            "valid_for_claim": "False",
        }
        for source_id, metadata in SOURCES.items()
    ]


def closure_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "DFC3502_0_dressed_source_definition",
            "claim_piece": "M_H is dressed Hilbert source charge",
            "statement": "The source mass that can reduce to Newton is not bare rest mass; it is the Hamiltonian/Hilbert charge of the total observed source, including binding and field dressing.",
            "mathematical_form": "M_H[S] := (4*pi*G_ref)^-1 integral_S Pi_M J_H[tau] = H_tau[S]-H_tau[S_ref]",
            "derivation": "Use the worldtube source measure correction: the exterior 1/r coefficient must be sourced by the same Noether/Hamiltonian charge seen by the local field equation.",
            "result": "DEFINITION_LOCK_ADOPTED_FOR_LOCAL_BRANCH",
            "remaining_gap": "MTS must parent-sign Pi_M, tau, e_obs, and source pullback as the same object before this is a claim",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DFC3502_1_total_Hilbert_current_closure",
            "claim_piece": "radial flux closure",
            "statement": "If the local exterior annulus is source-free and the total projected Hilbert current is closed, the dressed charge is independent of linking radius.",
            "mathematical_form": "M_H(S2)-M_H(S1) = (4*pi*G_ref)^-1 integral_A d(Pi_M J_H[tau]); d(Pi_M J_H)=0 => D_r M_H=0",
            "derivation": "This is Stokes' theorem plus the Noether/Hilbert current closure in the exterior. It is a real derivation once the parent current and projector are signed.",
            "result": "CONDITIONAL_ZERO_FOR_D_R_MH",
            "remaining_gap": "extra-sector current, metric projector stress, nonEH charge and frame/domain leakage still have to vanish or be bounded",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DFC3502_2_time_flux_closure",
            "claim_piece": "time drift closure",
            "statement": "If the local branch is stationary with no net flux through the timelike boundary, the dressed charge is time-independent.",
            "mathematical_form": "dM_H/dt = - integral_boundary T_total^{0i} n_i dA + explicit_nonstationary_boundary_terms; zero flux => D_t M_H=0",
            "derivation": "Hamiltonian charge conservation converts time drift into boundary energy-current flux. For a stationary isolated local source that flux must vanish.",
            "result": "CONDITIONAL_ZERO_FOR_D_T_MH",
            "remaining_gap": "stationarity, radiative leakage, background-field flux and moving boundary terms must be parent-silent or coefficient-filled",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DFC3502_3_Maxwell_stress_dressing",
            "claim_piece": "ordinary EM belongs inside M_H",
            "statement": "For minimally coupled Maxwell on the observed geometry, EM energy, pressure, momentum density and Poynting flow are components of T_EM and therefore dress M_H rather than becoming an extra fifth force.",
            "mathematical_form": "T_total = T_matter + T_EM + T_binding + ...; T_EM^{0i}=S_Poynting^i/c^2 in a local inertial frame",
            "derivation": "Vary S_EM with respect to the same observed metric/coframe. The resulting Hilbert stress enters the same source charge as matter.",
            "result": "CONDITIONAL_ZERO_FOR_ORDINARY_STATIONARY_EM_EXTRA",
            "remaining_gap": "observed Hodge/coframe, EM normalization, charge/current normalization and unique F2 owner remain unsigned",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DFC3502_4_matter_EM_exchange_cancels_in_total",
            "claim_piece": "internal Lorentz exchange is not source leakage",
            "statement": "Matter and EM exchange energy-momentum internally, but only the total stress-current must be conserved; internal Lorentz exchange is not a loss of M_H.",
            "mathematical_form": "nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda; nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda; nabla_mu T_total^{mu nu}=0",
            "derivation": "The Poynting theorem is a bookkeeping identity inside total Hilbert stress. It sharpens the coupling target rather than defeating it.",
            "result": "INTERNAL_EXCHANGE_CANCELS_CONDITIONALLY",
            "remaining_gap": "the charged matter current owner and representation/charge normalization must be fixed",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DFC3502_5_cross_term_fallback",
            "claim_piece": "when EM becomes mu_extra",
            "statement": "Nonminimal MTS-EM terms, independent EM action multipliers, hidden gauge-kinetic functions, radiative Poynting leakage, or wave/relic background flux are not absorbed into M_H unless parent-owned.",
            "mathematical_form": "epsilon_EM_extra = (Phi_rad + Phi_nonminimal + Phi_lambdaF2 + Phi_hodge + Phi_readout)/(G_ref M_H)",
            "derivation": "Anything outside the same minimally coupled observed Hilbert stress is an explicit coefficient, not a silent Newton calibration.",
            "result": "COEFFICIENT_FALLBACK_REQUIRED_IF_PRESENT",
            "remaining_gap": "fill P8_EM_Poynting_source_flux_or_cross_term_vector.csv rows or derive their parent exclusion",
            "valid_for_claim": "False",
        },
    ]


def radial_time_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "RT3502_0_radial_MH",
            "target": "D_r M_H",
            "candidate_result": "0 if d(Pi_M J_H)=0 on the source-free exterior annulus",
            "derived_formula": "D_r M_H maps to integral_A d(Pi_M J_H)",
            "blocking_terms": "Delta_nonEH;Delta_PiM_metric;Delta_extra;Delta_frame;Delta_cal;Delta_PPN",
            "observable_pressure": "partial_r_ln_mu_obs;R10_alpha_lambda;PPN_beta",
            "artifact_if_failed": "P8_radial_mu_profile_or_zero.csv",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "status_id": "RT3502_1_time_MH",
            "target": "D_t M_H",
            "candidate_result": "0 if tau is stationary and total boundary energy flux vanishes",
            "derived_formula": "D_t M_H = - integral_boundary T_total^{0i} n_i dA + boundary/reference terms",
            "blocking_terms": "radiative_Poynting_flux;background_field_flux;moving_boundary;time_dependent_memory;reference_drift",
            "observable_pressure": "Gdot_over_G;clock_drift;orbital_GMdot",
            "artifact_if_failed": "P8_time_drift_residual_or_zero.csv",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "status_id": "RT3502_2_EM_ordinary",
            "target": "epsilon_EM_extra ordinary minimal Maxwell",
            "candidate_result": "0 if S_EM is minimally coupled to e_obs and its stress is inside T_total",
            "derived_formula": "mu_EM_bound_fields subset M_H, not mu_extra",
            "blocking_terms": "observed_Hodge_unsigned;EM_normalization_unsigned;charge_current_owner_unsigned",
            "observable_pressure": "Maxwell stress;clock energy;source coupling;alpha owner",
            "artifact_if_failed": "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
            "current_status": "CONDITIONAL_DRESSING_ROUTE",
            "valid_for_claim": "False",
        },
        {
            "status_id": "RT3502_3_EM_leakage",
            "target": "epsilon_EM_extra leakage",
            "candidate_result": "retained coefficient unless parent excludes or flux is zero",
            "derived_formula": "epsilon_EM_extra=(Phi_rad+Phi_nonminimal+Phi_lambdaF2+Phi_hodge+Phi_readout)/(G_ref M_H)",
            "blocking_terms": "nonminimal_XF2;w_EM;hidden_gauge_kinetic;radiative_flux;readout_regeneration",
            "observable_pressure": "Gdot;WEP;clock;PPN;source normalization",
            "artifact_if_failed": "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
            "current_status": "RETAINED_COEFFICIENT_VECTOR_CREATED",
            "valid_for_claim": "False",
        },
    ]


def em_flux_vector_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "component_id": "EMF3502_0_minimal_bound_field_stress",
            "source": "ordinary_minimal_Maxwell_bound_fields",
            "symbol": "epsilon_EM_bound",
            "definition": "mu_EM_bound_fields/(G_ref M_H)",
            "candidate_value": "0_CONDITIONAL_INSIDE_MH",
            "formula": "S_EM=-1/(4 mu0) int F wedge *_obs F; T_EM enters T_total and M_H",
            "units": "dimensionless",
            "zero_condition": "same observed Hodge/coframe, minimal Maxwell variation, stationary bound fields",
            "if_not_zero": "treat as source normalization coefficient, not calibrated GM",
            "observable_links": "Maxwell_stress;Newton_source_charge",
            "source_path": str(SOURCES["maxwell_poynting_ledger"]["path"]),
            "status": "CONDITIONAL_ZERO_ROUTE",
            "valid_for_claim": "False",
        },
        {
            "component_id": "EMF3502_1_radiative_poynting_flux",
            "source": "radiative_or_background_Poynting_flux",
            "symbol": "Phi_EM_rad/(G_ref M_H)",
            "definition": "net EM energy flux through the local exterior boundary normalized by source charge",
            "candidate_value": "MISSING_FLUX_OR_ZERO_THEOREM",
            "formula": "Phi_EM_rad = integral_boundary S_Poynting dot n dA",
            "units": "time^-1 or dimensionless over stated window",
            "zero_condition": "stationary isolated local branch with no net radiative/background flux",
            "if_not_zero": "contributes to D_t M_H and possibly radial source hair",
            "observable_links": "Gdot_over_G;clock_drift;source_time_hair",
            "source_path": str(SOURCES["maxwell_poynting_ledger"]["path"]),
            "status": "RETAINED_FLUX_COEFFICIENT_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "component_id": "EMF3502_2_nonminimal_XF2",
            "source": "nonminimal_MTS_EM_cross_term",
            "symbol": "C_XF2",
            "definition": "coefficient of hidden/motion/time scalar or tensor multiplying F^2 or F*F",
            "candidate_value": "MISSING_PARENT_EXCLUSION_OR_BOUND",
            "formula": "Delta S ~ int sqrt(-g) f_X(Phi) F_mn F^mn or g_X(Phi) F_mn *F^mn",
            "units": "model_dependent",
            "zero_condition": "parent operator domain forbids hidden-visible EM coefficient morphisms",
            "if_not_zero": "feeds alpha drift, clock/WEP products, and source normalization",
            "observable_links": "alpha_EM;clock;WEP;R10;PPN",
            "source_path": str(SOURCES["em_owner_package"]["path"]),
            "status": "RETAINED_OPERATOR_COEFFICIENT_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "component_id": "EMF3502_3_EM_normalization_multiplier",
            "source": "independent_EM_action_multiplier",
            "symbol": "w_EM",
            "definition": "independent multiplier of the observed Maxwell action/stress",
            "candidate_value": "MISSING_UNIQUE_F2_OR_ALPHA_OWNER",
            "formula": "S_EM -> w_EM S_EM, T_EM -> w_EM T_EM unless normalization is parent-owned",
            "units": "dimensionless",
            "zero_condition": "unique Maxwell curvature norm plus charge/current/fine-structure owner",
            "if_not_zero": "rescales Poynting source strength and material EM binding response",
            "observable_links": "alpha_EM;binding_energy;WEP;clock",
            "source_path": str(SOURCES["em_owner_package"]["path"]),
            "status": "RETAINED_NORMALIZATION_COEFFICIENT_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "component_id": "EMF3502_4_observed_Hodge_flow_rule",
            "source": "Hodge_or_constitutive_background",
            "symbol": "Delta_Hodge_EM",
            "definition": "difference between EM Hodge/constitutive flow rule and gravitational observed coframe",
            "candidate_value": "MISSING_OBSERVED_HODGE_PARENT_SIGNATURE",
            "formula": "*_EM - *_obs or constitutive tensor chi_EM - chi_obs",
            "units": "dimensionless_or_tensor",
            "zero_condition": "MTS derives the observed EM Hodge/flow rule from the same e_obs/q data",
            "if_not_zero": "Poynting flow and light cone may not source the same geometry",
            "observable_links": "Maxwell_limit;light_cone;clock;PPN",
            "source_path": str(SOURCES["em_owner_package"]["path"]),
            "status": "RETAINED_HODGE_FLOW_COEFFICIENT_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "component_id": "EMF3502_5_matter_EM_internal_exchange",
            "source": "matter_EM_Lorentz_exchange",
            "symbol": "epsilon_internal_exchange",
            "definition": "apparent matter-only nonconservation from Lorentz force exchange",
            "candidate_value": "0_CONDITIONAL_IN_TOTAL_STRESS",
            "formula": "nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda and nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda",
            "units": "dimensionless",
            "zero_condition": "matter and EM are varied in the same parent action with the same charge current",
            "if_not_zero": "charge/current owner or representation coupling is not the same source",
            "observable_links": "source_charge;WEP;EM_matter_coupling",
            "source_path": str(SOURCES["maxwell_poynting_ledger"]["path"]),
            "status": "CONDITIONAL_ZERO_IN_TOTAL_HILBERT_STRESS",
            "valid_for_claim": "False",
        },
        {
            "component_id": "EMF3502_6_readout_radiative_regeneration",
            "source": "effective_readout_or_loop_regeneration",
            "symbol": "C_EM_readout",
            "definition": "effective readout/loop-induced EM coefficient after reduction",
            "candidate_value": "MISSING_READOUT_CLOSURE_OR_BOUND",
            "formula": "S_eff or clock/readout map regenerates f_X F^2, alpha_X, or EM binding response",
            "units": "model_dependent",
            "zero_condition": "radiative/readout closure preserves visible-sector pullback and unique EM owner",
            "if_not_zero": "feeds clock/WEP/alpha/source-normalization residuals",
            "observable_links": "clock;WEP;alpha_EM;binding_response",
            "source_path": str(SOURCES["em_owner_package"]["path"]),
            "status": "RETAINED_EFFECTIVE_COEFFICIENT_REQUIRED",
            "valid_for_claim": "False",
        },
    ]
    return rows


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3502_0_MH_dressing",
            "decision": "Adopt dressed Hilbert charge as the only acceptable local Newton source definition.",
            "rationale": "Bare mass loses field energy and binding; the exterior field sees the total Hamiltonian/Hilbert charge.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3502_1_radial_time_progress",
            "decision": "D_r M_H and D_t M_H now have conditional zero proofs, not just placeholders.",
            "rationale": "Stokes/Noether closure gives radial silence; Hamiltonian flux balance gives time silence, but only after parent current and flux premises are signed.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3502_2_EM_stress_policy",
            "decision": "Ordinary stationary Maxwell stress is source dressing; nonminimal/radiative Poynting leakage is explicit mu_extra.",
            "rationale": "This uses the Poynting vector as a diagnostic instead of treating EM as either ignored or magically solved.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3502_3_next_choke",
            "decision": "Next target is observed Hodge/Maxwell owner plus total Hilbert current closure.",
            "rationale": "That is the parent signature needed to turn the conditional Poynting/Hilbert theorem into actual MTS progress.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3503-Y5-R2FR-observed-Hodge-Maxwell-owner-and-total-Hilbert-current-closure-or-EM-bound.md",
            "next_script": "scripts/Y5_R2FR_3503_observed_Hodge_Maxwell_owner_and_total_Hilbert_current_closure_or_EM_bound.py",
            "objective": "Derive that Maxwell stress, Poynting flow, matter stress and the source measure all use the same observed coframe/Hodge and one total Hilbert current; otherwise fill the EM/Hodge/current coefficient bounds.",
            "success_gate": "observed Hodge/coframe is q/e_obs-owned, Maxwell action has no independent F2 multiplier, charge/current normalization is fixed, and d(Pi_M J_H_total)=0 in the stationary exterior.",
            "forbidden_shortcuts": "no importing Maxwell by hand as a closure axiom; no ignoring Poynting flux; no bare-mass source; no alpha-owner claim from units alone",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    radial_time: list[dict[str, Any]],
    em_vector: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_files = [
        OUT / "P8_Y5_R2FR_3502_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R2FR_3502_DRESSED_SOURCE_FLUX_CLOSURE_THEOREM.csv",
        OUT / "P8_Y5_R2FR_3502_RADIAL_TIME_MH_STATUS.csv",
        OUT / "P8_Y5_R2FR_3502_EM_POYNTING_SOURCE_FLUX_VECTOR.csv",
        EM_FLUX_VECTOR,
        OUT / "P8_Y5_R2FR_3502_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R2FR_3502_NEXT_TARGET.csv",
    ]
    parsed_counts = [f"{output_file.name}:{len(read_csv(output_file))}" for output_file in output_files]
    all_rows = [*sources, *theorem, *radial_time, *em_vector, *decisions, *next_rows]
    checks = [
        {
            "check_id": "VAL3502_0_sources_exist",
            "passed": all(source_row["exists"] == "True" for source_row in sources),
            "detail": "all cited local source-register paths exist",
        },
        {
            "check_id": "VAL3502_1_csv_parse",
            "passed": True,
            "detail": "; ".join(parsed_counts),
        },
        {
            "check_id": "VAL3502_2_radial_time_conditional_zero",
            "passed": any(row["target"] == "D_r M_H" and "CONDITIONAL_ZERO" in row["current_status"] for row in radial_time)
            and any(row["target"] == "D_t M_H" and "CONDITIONAL_ZERO" in row["current_status"] for row in radial_time),
            "detail": "D_r M_H and D_t M_H conditional zero routes present",
        },
        {
            "check_id": "VAL3502_3_em_flux_vector_created",
            "passed": EM_FLUX_VECTOR.exists() and len(read_csv(EM_FLUX_VECTOR)) >= 7,
            "detail": str(EM_FLUX_VECTOR),
        },
        {
            "check_id": "VAL3502_4_ordinary_em_dressed_not_ignored",
            "passed": any(row["component_id"] == "EMF3502_0_minimal_bound_field_stress" and "INSIDE_MH" in row["candidate_value"] for row in em_vector),
            "detail": "ordinary stationary Maxwell stress is routed into M_H conditionally",
        },
        {
            "check_id": "VAL3502_5_retained_leakage_rows",
            "passed": sum(1 for row in em_vector if "RETAINED" in row["status"]) >= 4,
            "detail": "radiative/nonminimal/Hodge/readout leakage rows remain explicit",
        },
        {
            "check_id": "VAL3502_6_no_claim",
            "passed": all(str(row.get("valid_for_claim", "False")) == "False" for row in all_rows),
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "VAL3502_7_no_formalization_outputs",
            "passed": all(not str(output_file).startswith(str(FORMALIZATION)) for output_file in output_files),
            "detail": "outputs stay under post-checkpoint-work/source-intake",
        },
        {
            "check_id": "VAL3502_8_next_target",
            "passed": len(next_rows) == 1 and "3503" in next_rows[0]["next_doc"],
            "detail": next_rows[0]["next_doc"],
        },
    ]
    checks.append(
        {
            "check_id": "VAL3502_SUMMARY",
            "passed": all(bool(check["passed"]) for check in checks),
            "detail": "PASS" if all(bool(check["passed"]) for check in checks) else "FAIL",
        }
    )
    return [
        {
            "check_id": check["check_id"],
            "passed": str(bool(check["passed"])),
            "detail": check["detail"],
            "valid_for_claim": "False",
        }
        for check in checks
    ]


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    theorem: list[dict[str, Any]],
    radial_time: list[dict[str, Any]],
    em_vector: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3502 - Dressed Hilbert Source Measure, Poynting Flux Closure or Radial-Time Bound",
                "",
                "## Current Verdict",
                "- **Derivation progress:** `D_r M_H=0` and `D_t M_H=0` now have explicit conditional zero proofs from total Hilbert/Noether charge closure and boundary flux balance.",
                "- **EM/Poynting clarified:** ordinary stationary Maxwell stress dresses `M_H`; radiative, background, nonminimal, Hodge, normalization, or readout leakage becomes an explicit coefficient.",
                "- **Still not a claim:** the required parent signatures are not all signed: observed Hodge/coframe, unique Maxwell normalization, charge/current owner, total source current closure, and extra-sector silence remain gates.",
                "- **Next best move:** derive the observed Hodge/Maxwell owner and total Hilbert current closure, because that is the shortest path from conditional theorem to actual MTS local-GR progress.",
                "",
                "## Dressed Source Flux Closure Theorem",
                markdown_table(
                    theorem,
                    ["theorem_id", "claim_piece", "statement", "result", "remaining_gap", "valid_for_claim"],
                ),
                "",
                "## Radial and Time M_H Status",
                markdown_table(
                    radial_time,
                    [
                        "status_id",
                        "target",
                        "candidate_result",
                        "blocking_terms",
                        "observable_pressure",
                        "artifact_if_failed",
                        "current_status",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## EM Poynting Source-Flux Vector",
                markdown_table(
                    em_vector,
                    [
                        "component_id",
                        "source",
                        "symbol",
                        "candidate_value",
                        "zero_condition",
                        "status",
                        "observable_links",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Decisions",
                markdown_table(decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"]),
                "",
                "## Next Target",
                markdown_table(
                    next_rows,
                    ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
                ),
                "",
                "## Validation",
                markdown_table(validation, ["check_id", "passed", "detail", "valid_for_claim"]),
                "",
                f"Generated: {generated_timestamp()}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    source_rows = source_register_rows()
    theorem_rows = closure_theorem_rows()
    radial_time_rows = radial_time_status_rows()
    em_vector_rows = em_flux_vector_rows()
    decision_ledger_rows = decision_rows()
    next_rows = next_target_rows()

    em_vector_fields = [
        "component_id",
        "source",
        "symbol",
        "definition",
        "candidate_value",
        "formula",
        "units",
        "zero_condition",
        "if_not_zero",
        "observable_links",
        "source_path",
        "status",
        "valid_for_claim",
    ]

    write_csv(
        OUT / "P8_Y5_R2FR_3502_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "path", "exists", "role", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3502_DRESSED_SOURCE_FLUX_CLOSURE_THEOREM.csv",
        theorem_rows,
        [
            "theorem_id",
            "claim_piece",
            "statement",
            "mathematical_form",
            "derivation",
            "result",
            "remaining_gap",
            "valid_for_claim",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3502_RADIAL_TIME_MH_STATUS.csv",
        radial_time_rows,
        [
            "status_id",
            "target",
            "candidate_result",
            "derived_formula",
            "blocking_terms",
            "observable_pressure",
            "artifact_if_failed",
            "current_status",
            "valid_for_claim",
        ],
    )
    write_csv(OUT / "P8_Y5_R2FR_3502_EM_POYNTING_SOURCE_FLUX_VECTOR.csv", em_vector_rows, em_vector_fields)
    write_csv(EM_FLUX_VECTOR, em_vector_rows, em_vector_fields)
    write_csv(
        OUT / "P8_Y5_R2FR_3502_DECISION_LEDGER.csv",
        decision_ledger_rows,
        ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3502_NEXT_TARGET.csv",
        next_rows,
        ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
    )

    validation_rows = validate(
        source_rows,
        theorem_rows,
        radial_time_rows,
        em_vector_rows,
        decision_ledger_rows,
        next_rows,
    )
    write_csv(
        OUT / "P8_Y5_BRR545_3502_VALIDATION.csv",
        validation_rows,
        ["check_id", "passed", "detail", "valid_for_claim"],
    )
    write_doc(theorem_rows, radial_time_rows, em_vector_rows, decision_ledger_rows, next_rows, validation_rows)


if __name__ == "__main__":
    main()
