from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3501-Y5-R2FR-mu-extra-over-Gref-MH-vector-zero-or-coefficient-fill.md"
CANONICAL_VECTOR = OUT / "P8_mu_extra_over_Geff_Meff_vector.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3501": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3500": {
        "path": ROOT / "3500-Y5-R2FR-constant-Gref-and-muobs-derivative-hair-zero-or-residual-fill.md",
        "role": "3500 handoff",
    },
    "fills_3500": {
        "path": OUT / "P8_Y5_R2FR_3500_RESIDUAL_FILL_ROWS.csv",
        "role": "3500 demanded epsilon_mu vector",
    },
    "channels_3500": {
        "path": OUT / "P8_Y5_R2FR_3500_DERIVATIVE_CHANNEL_GATE.csv",
        "role": "3500 derivative channel gates",
    },
    "prior_vector_skeleton": {
        "path": OUT / "P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
        "role": "prior mu_extra coefficient skeleton",
    },
    "prior_owner_gate": {
        "path": OUT / "P8_MU_EXTRA_ZERO_OWNER_GATE.csv",
        "role": "prior mu_extra owner gate",
    },
    "prior_owner_ledger": {
        "path": OUT / "P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv",
        "role": "prior channel owner ledger",
    },
    "local_bound_scorecard": {
        "path": OUT / "P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv",
        "role": "local bound map for mu_extra channels",
    },
    "source_flux_theorem": {
        "path": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
        "role": "M_H flux theorem attempt",
    },
    "worldtube_measure_theorem": {
        "path": OUT / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "role": "worldtube dressed source measure theorem",
    },
    "projector_naturality_3498": {
        "path": OUT / "P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv",
        "role": "projector naturality and source-hypermomentum split",
    },
    "hsrc_status_3498": {
        "path": OUT / "P8_Y5_R2FR_3498_HSRC_STATUS_UPDATE.csv",
        "role": "source-hypermomentum status update",
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


def decomposition_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "EMV3501_0_sum_rule",
            "claim_piece": "epsilon_mu component sum",
            "statement": "epsilon_mu is not a single foggy parameter; it is the normalized sum of explicitly typed extra source-charge channels.",
            "mathematical_form": "epsilon_mu := mu_extra/(G_ref M_H) = sum_i epsilon_i, epsilon_i := mu_i/(G_ref M_H)",
            "derivation": "Start from mu_obs=G_ref M_H+mu_extra. Split mu_extra by source of non-EH charge: flux leakage, boundary terms, projector stress, range tails, non-EH potential, source labels, frame/domain split, EM field dressing and calibration.",
            "result": "EXACT_DECOMPOSITION_FRAME",
            "remaining_gap": "each epsilon_i still needs theorem-zero, harmless-constant status, or a scored coefficient",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "EMV3501_1_projector_split",
            "claim_piece": "projector source-hypermomentum vs metric stress",
            "statement": "The projector obstruction splits into a candidate-zero independent-Gamma source-hypermomentum piece and a still-retained metric-stress/source-normalization piece.",
            "mathematical_form": "delta_Gamma_ind(Pi J_H)=0 candidate, but delta_g(Pi J_H) and monopole metric response remain separate",
            "derivation": "3498 proves that q/e_obs/tau functoriality kills D_Gamma_ind Pi inside the candidate branch; it explicitly does not kill Hodge/DeWitt/e_obs metric variation.",
            "result": "ONE_SUBCOMPONENT_ADVANCED_TO_CANDIDATE_ZERO",
            "remaining_gap": "metric projector stress must be mapped into PPN/R11 or theorem-zero",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "EMV3501_2_dressed_source_measure",
            "claim_piece": "M_H includes field dressing",
            "statement": "The least-dangerous source definition is a dressed Hamiltonian/Hilbert charge M_H, not bare rest mass. Field energy, binding and stationary EM stress belong in M_H when minimally coupled.",
            "mathematical_form": "M_H[W] := H_tau[S_outer]-H_tau[S_ref], T_total = T_matter + T_EM + T_binding + ...",
            "derivation": "Worldtube glue says the exterior 1/r charge must be the Noether/Hamiltonian source charge. Therefore ordinary stationary Maxwell energy is not an extra fifth-force mu_extra term if it is part of the same Hilbert source.",
            "result": "SOURCE_DEFINITION_CORRECTION",
            "remaining_gap": "nonminimal MTS-EM cross terms or radiative Poynting leakage still need a separate row",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "EMV3501_3_flux_zero_route",
            "claim_piece": "radial/time M_H leakage",
            "statement": "If the exterior projected Hilbert current is closed and the Poynting/field flux through the annulus is stationary or zero, M_H is independent of linking radius and local time.",
            "mathematical_form": "M_H(S2)-M_H(S1)=integral_A d(Pi_M J_H); d(Pi_M J_H)=0 => D_r M_H=0; partial_t H_tau= - flux_boundary = 0 => D_t M_H=0",
            "derivation": "This is the actual no-hair target for source normalization: do not erase fields, include them in the dressed charge and prove no exterior leakage in the local stationary branch.",
            "result": "CONDITIONAL_ZERO_ROUTE",
            "remaining_gap": "MTS must inherit the EH symplectic charge and prove no radiative/background-field Poynting leakage for the local branch",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "EMV3501_4_no_absorption",
            "claim_piece": "no hidden GM fit",
            "statement": "Only a parent-fixed universal constant calibration can be absorbed into measured GM. Any dependence on time, radius, species, range, frame or source domain is live hair.",
            "mathematical_form": "D_X epsilon_calibration = 0 for all active X, otherwise epsilon_calibration is part of epsilon_mu",
            "derivation": "A constant number can set units; a channel-dependent residue changes local physics. This keeps the Newton limit honest.",
            "result": "CALIBRATION_GUARD",
            "remaining_gap": "absolute calibration owner still needs parent-fixed proof",
            "valid_for_claim": "False",
        },
    ]


def vector_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "component_id": "EMV3501_1_radial_MH_flux",
            "channel": "mass_flux_radial",
            "epsilon_symbol": "epsilon_radial_MH",
            "coefficient_symbol": "C_radial_MH",
            "coefficient_value": "CONDITIONAL_ZERO_IF_dPiM_JH_EQ_0_ELSE_MISSING_PROFILE",
            "units": "dimensionless",
            "definition": "epsilon_radial_MH := mu_radial_MH_flux/(G_ref M_H)",
            "candidate_zero_route": "closed projected Hilbert current in source-free exterior annulus",
            "derived_piece": "T509/T510 give d(Pi_M J_H)=0 => no radial linking-surface leakage",
            "retained_piece": "MTS inheritance of EH symplectic charge and extra-sector silence remains open",
            "status": "CONDITIONAL_ZERO_ROUTE_NOT_INHERITED",
            "derivative_tags": "D_r",
            "observable_links": "partial_r_ln_mu_obs;alpha(lambda);PPN_beta",
            "bound_or_gate": "zero radial hair or mapped profile envelope",
            "required_artifact": "P8_radial_mu_profile_or_zero.csv",
            "source_paths": str(SOURCES["source_flux_theorem"]["path"]),
            "valid_for_claim": "False",
            "notes": "This is a derivation target, not just a missing coefficient.",
        },
        {
            "component_id": "EMV3501_2_time_MH_flux",
            "channel": "time_flux",
            "epsilon_symbol": "epsilon_time_MH",
            "coefficient_symbol": "C_time_MH",
            "coefficient_value": "CONDITIONAL_ZERO_IF_STATIONARY_FLUX_EQ_0_ELSE_MISSING_DRIFT",
            "units": "dimensionless",
            "definition": "epsilon_time_MH := mu_time_flux/(G_ref M_H)",
            "candidate_zero_route": "stationary local branch with no net exterior energy/Poynting flux",
            "derived_piece": "Hamiltonian charge is conserved when boundary flux through the local annulus vanishes",
            "retained_piece": "local stationarity and background-field flux silence are not yet parent-signed",
            "status": "CONDITIONAL_ZERO_ROUTE_NOT_INHERITED",
            "derivative_tags": "D_t",
            "observable_links": "Gdot_over_G;clock_drift",
            "bound_or_gate": "abs(dln_mu_obs_dt)<=9.6e-15 yr^-1 or theorem-zero",
            "required_artifact": "P8_time_drift_residual_or_zero.csv",
            "source_paths": str(SOURCES["source_flux_theorem"]["path"]),
            "valid_for_claim": "False",
            "notes": "This is where Poynting-style flux belongs in the local-GR reduction.",
        },
        {
            "component_id": "EMV3501_3_boundary_topological_monopole",
            "channel": "boundary_topological",
            "epsilon_symbol": "epsilon_boundary",
            "coefficient_symbol": "C_boundary",
            "coefficient_value": "MISSING_OR_HARMLESS_IF_PARENT_FIXED_CONSTANT",
            "units": "dimensionless",
            "definition": "epsilon_boundary := mu_boundary/(G_ref M_H)",
            "candidate_zero_route": "exact/topological boundary term with fixed branch class has no local source derivative",
            "derived_piece": "constant branch calibration is derivative-silent if parent-fixed",
            "retained_piece": "source-dependent, time-dependent or radial boundary shift remains live",
            "status": "CONDITIONAL_HARMLESS_NOT_PARENT_FIXED",
            "derivative_tags": "D_t;D_r;D_frame;D_domain",
            "observable_links": "beta_minus_1;alpha3;xi;Gdot_over_G",
            "bound_or_gate": "parent-fixed constant or coefficient locks",
            "required_artifact": "P8_mu_extra_boundary_coefficients.csv",
            "source_paths": str(SOURCES["prior_owner_ledger"]["path"]),
            "valid_for_claim": "False",
            "notes": "Absorb only if every derivative channel is zero by parent identity.",
        },
        {
            "component_id": "EMV3501_4_projector_gamma_hypermomentum",
            "channel": "projector_independent_connection",
            "epsilon_symbol": "epsilon_Pi_Gamma",
            "coefficient_symbol": "C_Pi_Gamma",
            "coefficient_value": "0_CANDIDATE",
            "units": "dimensionless",
            "definition": "epsilon_Pi_Gamma := mu_deltaGammaPi/(G_ref M_H)",
            "candidate_zero_route": "Pi depends only on q/e_obs/tau/topology, not Gamma_ind",
            "derived_piece": "3498 chain rule gives D_Gamma_ind Pi=0 and delta_Gamma_ind(Pi J_H)=0 in the candidate branch",
            "retained_piece": "branch adoption and source charge calibration remain separate",
            "status": "CANDIDATE_ZERO_FROM_3498",
            "derivative_tags": "D_Gamma_ind",
            "observable_links": "source_hypermomentum",
            "bound_or_gate": "parent branch adoption",
            "required_artifact": "none_for_this_subcomponent",
            "source_paths": f"{SOURCES['projector_naturality_3498']['path']};{SOURCES['hsrc_status_3498']['path']}",
            "valid_for_claim": "False",
            "notes": "This is real progress: kill only the independent-Gamma source piece, not all projector stress.",
        },
        {
            "component_id": "EMV3501_5_projector_metric_stress_monopole",
            "channel": "projector_metric_response",
            "epsilon_symbol": "epsilon_Pi_metric",
            "coefficient_symbol": "C_Pi_metric",
            "coefficient_value": "MISSING_METRIC_STRESS_COEFFICIENT",
            "units": "dimensionless",
            "definition": "epsilon_Pi_metric := mu_deltaMetricPi/(G_ref M_H)",
            "candidate_zero_route": "topological metric-independent projector or metric-stress cancellation by parent identity",
            "derived_piece": "3498 explicitly separates this from the Gamma_ind zero",
            "retained_piece": "Hodge/DeWitt/e_obs projector metric variation can still source PPN/R11 residuals",
            "status": "RETAINED_COEFFICIENT_REQUIRED",
            "derivative_tags": "D_g;D_frame;D_domain",
            "observable_links": "gamma_minus_1;beta_minus_1;R11_operator_ledger",
            "bound_or_gate": "metric projector stress theorem-zero or executable coefficient",
            "required_artifact": "R11_nonEH_operator_vector_executable.csv",
            "source_paths": str(SOURCES["projector_naturality_3498"]["path"]),
            "valid_for_claim": "False",
            "notes": "This keeps us from cheating by over-reading the projector naturality win.",
        },
        {
            "component_id": "EMV3501_6_bulk_range_yukawa_tail",
            "channel": "bulk_range",
            "epsilon_symbol": "epsilon_bulk_X",
            "coefficient_symbol": "C_bulk_X",
            "coefficient_value": "MISSING_ALPHA_LAMBDA_OR_NO_POLE_THEOREM",
            "units": "dimensionless",
            "definition": "epsilon_bulk_X := mu_bulk_X_tail/(G_ref M_H)",
            "candidate_zero_route": "source-free positive mass-gap/no-physical-X-pole theorem",
            "derived_piece": "no finite-range force if the local branch has no sourced propagating X pole",
            "retained_piece": "otherwise alpha(lambda) must be scored against R10",
            "status": "RETAINED_CURVE_OR_THEOREM_REQUIRED",
            "derivative_tags": "D_lambda;D_r",
            "observable_links": "R10_alpha_lambda;fifth_force",
            "bound_or_gate": "for every lambda, abs(alpha_predicted)<=alpha_bound",
            "required_artifact": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
            "source_paths": str(SOURCES["local_bound_scorecard"]["path"]),
            "valid_for_claim": "False",
            "notes": "The range branch is now isolated instead of contaminating all of GM.",
        },
        {
            "component_id": "EMV3501_7_nonEH_operator_potential",
            "channel": "nonEH_operator",
            "epsilon_symbol": "epsilon_nonEH_source",
            "coefficient_symbol": "C_nonEH_source",
            "coefficient_value": "MISSING_OPERATOR_VECTOR_OR_EH_ONLY_THEOREM",
            "units": "dimensionless",
            "definition": "epsilon_nonEH_source := mu_nonEH_potential/(G_ref M_H)",
            "candidate_zero_route": "EH-only local exterior fixed point",
            "derived_piece": "if the local exterior operator is exactly EH at second order, nonEH source potential is zero",
            "retained_piece": "R11 operator coefficients currently remain symbolic",
            "status": "RETAINED_OPERATOR_VECTOR_REQUIRED",
            "derivative_tags": "D_g;D_r;D_lambda",
            "observable_links": "gamma_minus_1;beta_minus_1;R11_operator_ledger;R10",
            "bound_or_gate": "EH-only theorem or executable nonEH coefficient vector",
            "required_artifact": "R11_nonEH_operator_vector_executable.csv",
            "source_paths": str(SOURCES["local_bound_scorecard"]["path"]),
            "valid_for_claim": "False",
            "notes": "This is the GR-reduction side of the same source-normalization problem.",
        },
        {
            "component_id": "EMV3501_8_species_source_selector",
            "channel": "species_material_source",
            "epsilon_symbol": "epsilon_species_A",
            "coefficient_symbol": "C_species_A",
            "coefficient_value": "MISSING_SELECTOR_BLIND_THEOREM_OR_ETA",
            "units": "dimensionless",
            "definition": "epsilon_species_A := mu_species_A/(G_ref M_H)",
            "candidate_zero_route": "matter/source action descends with no species-only source selector",
            "derived_piece": "if source charge is the same Hilbert current for all compositions, source-side eta vanishes",
            "retained_piece": "direct matter WEP does not by itself prove source-charge universality",
            "status": "RETAINED_COEFFICIENT_REQUIRED",
            "derivative_tags": "D_A",
            "observable_links": "eta_source_AB;WEP;clock_redshift",
            "bound_or_gate": "abs(eta_source_AB)<=2.8e-15 or theorem-zero",
            "required_artifact": "P8_species_source_charge_residual_or_zero.csv",
            "source_paths": str(SOURCES["prior_owner_ledger"]["path"]),
            "valid_for_claim": "False",
            "notes": "This stops source coupling from becoming a composition-dependent patch.",
        },
        {
            "component_id": "EMV3501_9_frame_domain_pullback",
            "channel": "frame_domain",
            "epsilon_symbol": "epsilon_frame_domain",
            "coefficient_symbol": "C_frame_domain",
            "coefficient_value": "MISSING_SAME_PULLBACK_THEOREM_OR_DELTA_FRAME",
            "units": "dimensionless",
            "definition": "epsilon_frame_domain := mu_frame_domain/(G_ref M_H)",
            "candidate_zero_route": "one observed coframe/source pullback for variation, clocks, rods and motion",
            "derived_piece": "q/e_obs/tau naturality helps, but source variation must share the same pullback",
            "retained_piece": "domain masks, vector selectors or frame split can still source preferred-frame residuals",
            "status": "RETAINED_COEFFICIENT_REQUIRED",
            "derivative_tags": "D_frame;D_domain",
            "observable_links": "alpha1;alpha2;alpha3;clock_link",
            "bound_or_gate": "same-frame theorem or residual below WEP/clock locks",
            "required_artifact": "P8_frame_source_split_residual_or_zero.csv",
            "source_paths": str(SOURCES["prior_owner_ledger"]["path"]),
            "valid_for_claim": "False",
            "notes": "Attach the frame theorem to the source variation, not only to geodesic readout.",
        },
        {
            "component_id": "EMV3501_10_em_poynting_hilbert_dressing",
            "channel": "EM_field_stress_and_flux",
            "epsilon_symbol": "epsilon_EM_extra",
            "coefficient_symbol": "C_EM_extra",
            "coefficient_value": "0_CONDITIONAL_IF_MINIMAL_MAXWELL_AND_NO_RADIATIVE_FLUX_ELSE_MISSING_CROSS_TERM",
            "units": "dimensionless",
            "definition": "epsilon_EM_extra := mu_EM_not_in_MH/(G_ref M_H)",
            "candidate_zero_route": "minimal Maxwell stress is included in the dressed Hilbert source charge; stationary closed-surface Poynting flux vanishes",
            "derived_piece": "ordinary EM field energy should move into M_H, not mu_extra, when it is part of T_total in the same source variation",
            "retained_piece": "nonminimal MTS-EM coupling, background-field Poynting leakage, or wave/relic flux needs a separate coefficient",
            "status": "CONDITIONAL_ZERO_ROUTE_FOR_ORDINARY_EM_STRESS",
            "derivative_tags": "D_t;D_r;D_EM",
            "observable_links": "Maxwell_stress;clock_energy;local_flux;PPN",
            "bound_or_gate": "stationary Poynting flux zero or explicit EM cross-term coefficient",
            "required_artifact": "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
            "source_paths": str(SOURCES["worldtube_measure_theorem"]["path"]),
            "valid_for_claim": "False",
            "notes": "This is the useful version of the Poynting intuition: fields are not ignored; they are either in M_H or scored as leakage.",
        },
        {
            "component_id": "EMV3501_11_absolute_calibration_offset",
            "channel": "constant_calibration",
            "epsilon_symbol": "epsilon_calibration",
            "coefficient_symbol": "C_cal",
            "coefficient_value": "HARMLESS_ONLY_IF_PARENT_FIXED_AND_ALL_DERIVATIVES_ZERO",
            "units": "dimensionless",
            "definition": "epsilon_calibration := mu_absolute_offset/(G_ref M_H)",
            "candidate_zero_route": "parent-fixed universal scale choice",
            "derived_piece": "a universal constant can set the measured value of G without changing local derivatives",
            "retained_piece": "if it depends on source, frame, radius, range or time, it is not a calibration",
            "status": "CONDITIONAL_HARMLESS_NOT_CLAIMED",
            "derivative_tags": "D_t;D_r;D_A;D_lambda;D_frame;D_domain",
            "observable_links": "absolute_G_calibration;Gdot;source_charge",
            "bound_or_gate": "parent-fixed universal constant with D_X epsilon_cal=0",
            "required_artifact": "P8_absolute_calibration_owner.csv",
            "source_paths": str(SOURCES["prior_owner_ledger"]["path"]),
            "valid_for_claim": "False",
            "notes": "This answers the Newton constant point: the decimal value may be empirical, but derivative universality must be derived.",
        },
    ]
    return rows


def closure_scorecard_rows(vector: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in vector:
        status = row["status"]
        if status.startswith("CANDIDATE_ZERO"):
            closure_class = "candidate_zero_subcomponent"
            pressure = "low_once_branch_adopted"
        elif status.startswith("CONDITIONAL_ZERO_ROUTE"):
            closure_class = "conditional_zero_route"
            pressure = "high_derivation_needed"
        elif "HARMLESS" in status:
            closure_class = "harmless_only_if_parent_fixed"
            pressure = "medium_calibration_owner_needed"
        else:
            closure_class = "retained_coefficient_or_bound_required"
            pressure = "high_numeric_or_theorem_needed"
        rows.append(
            {
                "score_id": row["component_id"].replace("EMV", "SCORE"),
                "component_id": row["component_id"],
                "epsilon_symbol": row["epsilon_symbol"],
                "closure_class": closure_class,
                "pressure": pressure,
                "claim_effect": "blocks_Newton_or_local_GR_until_closed" if pressure.startswith("high") else "nonclaim_candidate_progress",
                "next_action": row["candidate_zero_route"] if closure_class != "retained_coefficient_or_bound_required" else row["required_artifact"],
                "valid_for_claim": "False",
            }
        )
    return rows


def em_poynting_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "EMPR3501_0_do_not_ignore_fields",
            "claim_piece": "EM stress belongs in source charge",
            "statement": "If Maxwell is minimally coupled to the same observed metric/coframe, its stress-energy is part of the Hilbert source and therefore part of M_H, not a separate mu_extra fudge.",
            "test": "variation of S_EM with respect to e_obs/g_obs contributes T_EM to the same Hamiltonian/Hilbert charge used by the 1/r metric coefficient",
            "result": "CONDITIONAL_SOURCE_DRESSING",
            "remaining_gap": "MTS-specific nonminimal EM/background-field couplings must be listed separately",
            "valid_for_claim": "False",
        },
        {
            "route_id": "EMPR3501_1_stationary_poynting",
            "claim_piece": "Poynting flux closure",
            "statement": "For a stationary local source, the net Poynting/field-energy flux through a closed exterior annulus must vanish, or it appears as D_t M_H/D_r M_H hair.",
            "test": "integral_boundary S_EM dot n dA = 0 for stationary bound fields; nonzero radiative/background flux becomes epsilon_EM_extra",
            "result": "LOCAL_FLUX_GATE",
            "remaining_gap": "derive the stationary local branch and separate bound-field energy from propagating wave flux",
            "valid_for_claim": "False",
        },
        {
            "route_id": "EMPR3501_2_cross_term_residual",
            "claim_piece": "MTS-EM cross term",
            "statement": "If the motion/time/space sector couples directly to F_ab, Poynting vector, wave relics or EM invariants outside minimal Maxwell stress, that term is a new coefficient row, not automatic GR.",
            "test": "look for parent terms like X F^2, X F*F, J_X dot A, S_X dot (E cross B), or wave-memory stress that survives local stationary averaging",
            "result": "COEFFICIENT_VECTOR_REQUIRED_IF_PRESENT",
            "remaining_gap": "create P8_EM_Poynting_source_flux_or_cross_term_vector.csv or prove the parent action excludes these terms",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3501_0_vector_created",
            "decision": "Create the missing canonical epsilon_mu vector.",
            "rationale": "3500 correctly identified the missing artifact; 3501 now gives every local source-normalization obstruction a named component and gate.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3501_1_real_progress_piece",
            "decision": "Keep the 3498 projector-hypermomentum zero as a real but narrow win.",
            "rationale": "It kills the independent-Gamma source commutator inside the candidate branch while explicitly retaining metric projector stress.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3501_2_poynting_route",
            "decision": "Use the Poynting/vector-field intuition as a source-flux closure gate.",
            "rationale": "Ordinary EM stress should dress M_H; only nonminimal or radiative/background leakage belongs in mu_extra.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3501_3_next_derivation",
            "decision": "Next target should prove dressed Hilbert source flux closure before another broad source sweep.",
            "rationale": "If stationary M_H/Poynting flux closes, radial and time derivative hair shrink sharply; if it fails, we get exact flux coefficients instead of vague missing rows.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3502-Y5-R2FR-dressed-Hilbert-source-measure-Poynting-flux-closure-or-radial-time-bound.md",
            "next_script": "scripts/Y5_R2FR_3502_dressed_Hilbert_source_measure_Poynting_flux_closure_or_radial_time_bound.py",
            "objective": "Prove the local stationary source charge M_H includes Maxwell/field dressing and has zero exterior radial/time flux, or fill explicit Poynting/source-flux coefficients.",
            "success_gate": "D_r M_H=0 and D_t M_H=0 from parent charge closure with ordinary EM stress inside M_H; otherwise P8_EM_Poynting_source_flux_or_cross_term_vector.csv and radial/time bound rows are filled.",
            "forbidden_shortcuts": "no bare-mass source; no ignoring field energy; no absorbing radiative flux into measured GM; no local-GR claim from stationary assumptions alone",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    vector: list[dict[str, Any]],
    scorecard: list[dict[str, Any]],
    em_route: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_files = [
        OUT / "P8_Y5_R2FR_3501_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R2FR_3501_EPSILON_MU_DECOMPOSITION_THEOREM.csv",
        OUT / "P8_Y5_R2FR_3501_MU_EXTRA_OVER_GREF_MH_VECTOR.csv",
        CANONICAL_VECTOR,
        OUT / "P8_Y5_R2FR_3501_COMPONENT_CLOSURE_SCORECARD.csv",
        OUT / "P8_Y5_R2FR_3501_EM_POYNTING_STRESS_ROUTE.csv",
        OUT / "P8_Y5_R2FR_3501_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R2FR_3501_NEXT_TARGET.csv",
    ]
    parsed_counts = [f"{output_file.name}:{len(read_csv(output_file))}" for output_file in output_files]
    all_rows = [*sources, *theorem, *vector, *scorecard, *em_route, *decisions, *next_rows]
    checks = [
        {
            "check_id": "VAL3501_0_sources_exist",
            "passed": all(source_row["exists"] == "True" for source_row in sources),
            "detail": "all cited local source-register paths exist",
        },
        {
            "check_id": "VAL3501_1_csv_parse",
            "passed": True,
            "detail": "; ".join(parsed_counts),
        },
        {
            "check_id": "VAL3501_2_canonical_vector_created",
            "passed": CANONICAL_VECTOR.exists() and len(read_csv(CANONICAL_VECTOR)) >= 10,
            "detail": str(CANONICAL_VECTOR),
        },
        {
            "check_id": "VAL3501_3_projector_subcomponent_progress",
            "passed": any(row["component_id"] == "EMV3501_4_projector_gamma_hypermomentum" and row["coefficient_value"] == "0_CANDIDATE" for row in vector),
            "detail": "independent-Gamma projector source-hypermomentum split preserved as candidate zero",
        },
        {
            "check_id": "VAL3501_4_em_poynting_gate",
            "passed": any(row["component_id"] == "EMV3501_10_em_poynting_hilbert_dressing" for row in vector) and len(em_route) >= 3,
            "detail": "ordinary EM stress vs Poynting/cross-term leakage route present",
        },
        {
            "check_id": "VAL3501_5_honest_retained_rows",
            "passed": any("RETAINED" in row["status"] for row in vector) and any("CONDITIONAL_ZERO" in row["status"] for row in vector),
            "detail": "vector contains both derivation routes and retained coefficient rows",
        },
        {
            "check_id": "VAL3501_6_no_claim",
            "passed": all(str(row.get("valid_for_claim", "False")) == "False" for row in all_rows),
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "VAL3501_7_no_formalization_outputs",
            "passed": all(not str(output_file).startswith(str(FORMALIZATION)) for output_file in output_files),
            "detail": "outputs stay under post-checkpoint-work/source-intake",
        },
        {
            "check_id": "VAL3501_8_next_target",
            "passed": len(next_rows) == 1 and "3502" in next_rows[0]["next_doc"],
            "detail": next_rows[0]["next_doc"],
        },
    ]
    checks.append(
        {
            "check_id": "VAL3501_SUMMARY",
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
    vector: list[dict[str, Any]],
    scorecard: list[dict[str, Any]],
    em_route: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3501 - Mu Extra over Gref MH Vector Zero or Coefficient Fill",
                "",
                "## Current Verdict",
                "- **The missing vector now exists:** `epsilon_mu = mu_extra/(G_ref M_H)` has been decomposed into named component channels instead of being left as a foggy blocker.",
                "- **Real narrow win kept:** the 3498 projector naturality result gives a candidate zero for the independent-Gamma source-hypermomentum subcomponent, but metric projector stress remains alive.",
                "- **Poynting route added:** ordinary stationary Maxwell/field stress should dress `M_H`; only nonminimal or radiative/background Poynting leakage belongs in `mu_extra`.",
                "- **Still no Newton/local-GR claim:** most channels are conditional zero routes or retained coefficient rows until parent charge closure or numeric bounds are supplied.",
                "",
                "## Decomposition Theorem",
                markdown_table(
                    theorem,
                    ["theorem_id", "claim_piece", "statement", "result", "remaining_gap", "valid_for_claim"],
                ),
                "",
                "## Epsilon Mu Vector",
                markdown_table(
                    vector,
                    [
                        "component_id",
                        "channel",
                        "epsilon_symbol",
                        "coefficient_value",
                        "status",
                        "derivative_tags",
                        "observable_links",
                        "required_artifact",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Component Closure Scorecard",
                markdown_table(
                    scorecard,
                    ["score_id", "component_id", "closure_class", "pressure", "claim_effect", "next_action", "valid_for_claim"],
                ),
                "",
                "## EM and Poynting Route",
                markdown_table(
                    em_route,
                    ["route_id", "claim_piece", "statement", "result", "remaining_gap", "valid_for_claim"],
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
    theorem_rows = decomposition_theorem_rows()
    mu_vector_rows = vector_rows()
    scorecard_rows = closure_scorecard_rows(mu_vector_rows)
    em_route_rows = em_poynting_route_rows()
    decision_ledger_rows = decision_rows()
    next_rows = next_target_rows()

    vector_fields = [
        "component_id",
        "channel",
        "epsilon_symbol",
        "coefficient_symbol",
        "coefficient_value",
        "units",
        "definition",
        "candidate_zero_route",
        "derived_piece",
        "retained_piece",
        "status",
        "derivative_tags",
        "observable_links",
        "bound_or_gate",
        "required_artifact",
        "source_paths",
        "valid_for_claim",
        "notes",
    ]

    write_csv(
        OUT / "P8_Y5_R2FR_3501_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "path", "exists", "role", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3501_EPSILON_MU_DECOMPOSITION_THEOREM.csv",
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
    write_csv(OUT / "P8_Y5_R2FR_3501_MU_EXTRA_OVER_GREF_MH_VECTOR.csv", mu_vector_rows, vector_fields)
    write_csv(CANONICAL_VECTOR, mu_vector_rows, vector_fields)
    write_csv(
        OUT / "P8_Y5_R2FR_3501_COMPONENT_CLOSURE_SCORECARD.csv",
        scorecard_rows,
        ["score_id", "component_id", "epsilon_symbol", "closure_class", "pressure", "claim_effect", "next_action", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3501_EM_POYNTING_STRESS_ROUTE.csv",
        em_route_rows,
        ["route_id", "claim_piece", "statement", "test", "result", "remaining_gap", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3501_DECISION_LEDGER.csv",
        decision_ledger_rows,
        ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3501_NEXT_TARGET.csv",
        next_rows,
        ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
    )

    validation_rows = validate(
        source_rows,
        theorem_rows,
        mu_vector_rows,
        scorecard_rows,
        em_route_rows,
        decision_ledger_rows,
        next_rows,
    )
    write_csv(
        OUT / "P8_Y5_BRR545_3501_VALIDATION.csv",
        validation_rows,
        ["check_id", "passed", "detail", "valid_for_claim"],
    )
    write_doc(
        theorem_rows,
        mu_vector_rows,
        scorecard_rows,
        em_route_rows,
        decision_ledger_rows,
        next_rows,
        validation_rows,
    )


if __name__ == "__main__":
    main()
