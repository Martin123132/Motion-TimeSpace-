from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "3558-Y5-R2FR-same-frame-Hilbert-source-current-closure-or-coefficient-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_SAME_FRAME_HILBERT_SOURCE_CURRENT_3558"
CHECKPOINT_ID = "3558"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty CSV requested: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def sources() -> dict[str, Path]:
    return {
        "handoff_3557": RESIDUALS / "P8_Y5_R2FR_3557_NEXT_TARGET.csv",
        "nohair_3557": RESIDUALS / "P8_Y5_R2FR_3557_DERIVATIVE_HAIR_NOHAIR_THEOREM.csv",
        "bounds_3557": RESIDUALS / "P8_Y5_R2FR_3557_DERIVATIVE_HAIR_BOUND_RUNNER_INPUT.csv",
        "charge_current_attempt": RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        "charge_current_residuals": RESIDUALS / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
        "charge_current_status": RESIDUALS / "P8_charge_current_equality_STATUS.csv",
        "source_current_ward": RESIDUALS / "P8_source_current_Ward_universality_CONTRACT.csv",
        "ward_owner": RESIDUALS / "P8_Ward_source_owner_identity_CONTRACT.csv",
        "source_measure_theorem": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
        "source_measure_clauses": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
        "source_measure_residual_map": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "worldtube_theorem": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "worldtube_clauses": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv",
        "worldtube_proof": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_PROOF_SKETCH.csv",
        "parent_source_identity": RESIDUALS / "P8_PARENT_SOURCE_IDENTITY_ATTEMPT.csv",
        "parent_source_residuals": RESIDUALS / "P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv",
        "pim_htau_commutator": RESIDUALS / "P8_Y5_R2FR_3514_PIM_HTAU_COMMUTATOR_DERIVATION.csv",
        "pim_htau_residuals": RESIDUALS / "P8_Y5_R2FR_3514_PIM_HTAU_RESIDUAL_COMPONENTS.csv",
        "pim_htau_zero_gates": RESIDUALS / "P8_Y5_R2FR_3514_PIM_HTAU_ZERO_GATES.csv",
        "pim_htau_zero_proof": RESIDUALS / "P8_Y5_R2FR_3532_PIM_HTAU_ZERO_PROOF.csv",
        "hilbert_monopole_lock": RESIDUALS / "P8_Y5_R2FR_3542_HILBERT_MONOPOLE_LOCK.csv",
        "pim_chainmap_compare": RESIDUALS / "P8_Y5_R2FR_3550_PIM_CHAINMAP_ROUTE_COMPARE.csv",
        "mu_extra_vector": RESIDUALS / "P8_mu_extra_over_Geff_Meff_vector.csv",
        "local_bounds": LOCAL_BOUNDS / "local_bound_claims.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    role = {
        "handoff_3557": "declares 3558 objective",
        "nohair_3557": "imports derivative-hair theorem clauses",
        "bounds_3557": "imports bound targets for surviving coefficients",
        "charge_current_attempt": "direct Hilbert/Hamiltonian source equality attempt",
        "charge_current_residuals": "nine residual pieces in B_tau/G - M_eff[Pi_M J_H]",
        "charge_current_status": "existing no-claim status for charge-current equality",
        "source_current_ward": "same-frame Hilbert current Ward contract",
        "ward_owner": "total Ward/source-owner contract and limits",
        "source_measure_theorem": "M_eff flux theorem and no-extra-channel rule",
        "source_measure_clauses": "source-measure closure clauses",
        "source_measure_residual_map": "Delta_flux/PiM/symp/extra/cal/frame/nonEH/PPN residual map",
        "worldtube_theorem": "GR-style worldtube source-measure theorem",
        "worldtube_clauses": "worldtube source-measure prerequisites",
        "worldtube_proof": "Noether/Hamiltonian proof sketch",
        "parent_source_identity": "exact d(Pi_M J_H) obstruction identity",
        "parent_source_residuals": "projector/extra/anomaly obstruction rows",
        "pim_htau_commutator": "Pi_M/H_tau commutator reduction",
        "pim_htau_residuals": "C_M/C_shape/C_curl/... residual components",
        "pim_htau_zero_gates": "zero gates for Pi_M/H_tau square",
        "pim_htau_zero_proof": "conditional zero mechanisms for R_PiM and R_Htau",
        "hilbert_monopole_lock": "six Hilbert monopole lock identities",
        "pim_chainmap_compare": "Hilbert identity/inclusion Pi_M route comparison",
        "mu_extra_vector": "mu_extra coefficient vector and Poynting/Hilbert dressing row",
        "local_bounds": "empirical bounds for coefficient rows",
    }
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": role[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "HC3558_0_same_frame_Hilbert_current_definition",
            "name": "same-frame Hilbert current definition",
            "statement": "If matter descends through a single observed coframe e_obs=q(Phi) before readout, the active ordinary source current is J_H[tau]=T_H^{mu nu}[e_obs] n_mu tau_nu dSigma, with T_H from the variational derivative of S_matter[e_obs].",
            "derivation": "Vary the same matter action with respect to e_obs/g_obs and contract with the same observed time generator tau. This defines source charge before orbital GM, clock, or R10 readout.",
            "required_premises": "single e_obs/q/tau branch; matter action descent; no source readout mask",
            "status": "EXACT_CONDITIONAL_DEFINITION",
            "source_path": str(source_paths["source_current_ward"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "HC3558_1_projected_flux_obstruction_identity",
            "name": "projected Hilbert flux obstruction identity",
            "statement": "For any defined mass projector Pi_M, d(Pi_M J_H)= -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent.",
            "derivation": "Split the total parent current into Hilbert plus extra-current parts and apply the projected product rule d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H. Total current conservation replaces Pi_M dJ_H by -Pi_M dJ_extra plus any parent anomaly/multiplier term.",
            "required_premises": "total Ward current decomposition and Pi_M defined on the source-current complex",
            "status": "EXACT_OBSTRUCTION_IDENTITY",
            "source_path": str(source_paths["parent_source_identity"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "HC3558_2_closure_sufficient_conditions",
            "name": "same-frame Hilbert closure sufficient theorem",
            "statement": "If Pi_M dJ_extra=0, [d,Pi_M]J_H=0, A_parent=0, tau/e_obs/source support are fixed, and the exterior is source-free/stationary, then d(Pi_M J_H)=0 and linked-surface M_eff is time/radius independent.",
            "derivation": "Set each term in the obstruction identity to zero. Stokes' theorem over the exterior annulus gives M_eff(S2)-M_eff(S1)=int_A d(Pi_M J_H)=0. Stationarity/no side flux gives D_t M_eff=0.",
            "required_premises": "extra-current mass silence; Pi_M chainmap; no parent anomaly; fixed source frame/support; compact exterior",
            "status": "EXACT_CONDITIONAL_UNSIGNED",
            "source_path": str(source_paths["source_measure_theorem"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "HC3558_3_Hilbert_identity_PiM_route",
            "name": "least-scrutiny Pi_M route",
            "statement": "The cleanest Pi_M option is not an independent topological/Hodge projector: take Pi_M as the identity/inclusion on the Hilbert mass-current object after the source branch is defined. Then [d,Pi_M]J_H=0 by construction, provided the source object is fixed before readout.",
            "derivation": "An identity/inclusion chain map commutes with d on its own current complex. This avoids introducing a separate projector stress sector, but it requires the Hilbert mass-current object to be parent-owned first.",
            "required_premises": "Hilbert mass object parent-owned; Pi_M not fitted from orbital GM; source domain/frame fixed",
            "status": "BEST_ROUTE_CONDITIONAL_UNSIGNED",
            "source_path": str(source_paths["pim_chainmap_compare"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "HC3558_4_Poynting_dressing_rule",
            "name": "EM/Poynting dressing rule",
            "statement": "Ordinary stationary Maxwell field energy belongs inside the dressed Hilbert source charge M_H; only nonminimal EM coupling, radiative Poynting leakage, or background cross-terms remain as mu_extra coefficients.",
            "derivation": "If EM stress is minimally coupled to the same e_obs, it is part of T_H and therefore part of J_H. A closed stationary worldtube has no net exterior Poynting flux. Any non-stationary or nonminimal flux is not ignored; it is moved to an explicit leakage row.",
            "required_premises": "minimal Maxwell stress in same e_obs; stationary/no net flux, or explicit flux coefficient",
            "status": "CONDITIONAL_DRESSING_RULE",
            "source_path": str(source_paths["mu_extra_vector"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "HC3558_5_Newton_first_order_corollary",
            "name": "first-order Newton corollary",
            "statement": "If HC3558_0 through HC3558_4 are signed and G_N is constant, the local first-order Newton source branch follows: nabla^2 Phi=4*pi*G_N rho_H and a_r=-G_N M_H/r^2 up to explicitly retained PPN/operator residuals.",
            "derivation": "Closed Hilbert mass flux gives a radius-independent monopole. The weak Gauss law ties that monopole to the 1/r potential coefficient. Constant G_N turns the coefficient into the empirical Newton coupling.",
            "required_premises": "same-frame Hilbert source, closed flux, Gauss/orbital readout, constant G_N, no mu_extra derivative hair",
            "status": "COROLLARY_CONDITIONAL_NOT_LIVE",
            "source_path": str(source_paths["hilbert_monopole_lock"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def clause_audit(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    clauses = [
        ("CL3558_0_same_frame", "same observed coframe/time generator", "e_obs=e_source=e_matter=e_clock=e_orbit and tau fixed", "CONDITIONAL_NOT_PARENT_DERIVED", "delta_frame_source", "frame/source split"),
        ("CL3558_1_Hilbert_current", "Hilbert current from same matter action", "J_H=delta S_matter[e_obs]/delta e_obs contracted with tau", "EXACT_CONDITIONAL_NOT_PARENT_FORCED", "eta_source_AB;nonHilbert current", "source-current definition"),
        ("CL3558_2_PiM_chainmap", "Pi_M identity/inclusion or fixed chain map", "[d,Pi_M]J_H=0", "BEST_ROUTE_CONDITIONAL_UNSIGNED", "Delta_PiM;projector stress", "projector commutator"),
        ("CL3558_3_extra_mass_silence", "extra currents have no mass projection", "Pi_M dJ_extra=0", "NOT_PARENT_DERIVED", "mu_extra_boundary_bulk_domain;alpha(lambda)", "extra-sector mass charge"),
        ("CL3558_4_parent_anomaly_zero", "no parent anomaly/multiplier term", "A_parent=0", "NOT_SATISFIED", "closure-only anomaly residual", "parent source identity"),
        ("CL3558_5_worldtube_support", "source support and linking surfaces fixed before readout", "D_X W_source=D_X Sigma=D_X H_ref=0", "WORLDTUBE_REFERENCE_UNSIGNED", "radial profile;C_domain;C_ref", "worldtube/reference selector"),
        ("CL3558_6_stationary_no_flux", "stationary local exterior/no side flux", "boundary Poynting/symplectic flux=0 or bounded", "RETAINED_FLUX_COEFFICIENT_REQUIRED", "sigma_Gdot;epsilon_EM_extra", "time flux"),
        ("CL3558_7_Gauss_orbital_readout", "closed charge calibrates to inverse-square orbit", "a_r=-G_N M_H/r^2 + controlled residuals", "NOT_DERIVED", "Delta_cal;radial hair", "Newton readout"),
        ("CL3558_8_PPN_stability", "source charge stable through PPN", "delta_beta_source=gamma_minus_1=0 or explicit vector", "NOT_DERIVED", "PPN source vector", "local GR promotion"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": clause_id,
            "required_clause": required,
            "mathematical_form": formula,
            "current_status": status,
            "residual_if_missing": residual,
            "blocks": blocks,
            "source_path": str(source_paths["hilbert_monopole_lock"] if clause_id.startswith("CL3558_") else source_paths["source_measure_clauses"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for clause_id, required, formula, status, residual, blocks in clauses
    ]


def obstruction_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("OB3558_0_projected_extra_current", "Pi_M dJ_extra", "extra non-Hilbert/boundary/domain/memory/range/connection currents project into mass channel", "Pi_M dJ_extra=0", "mu_extra_boundary_bulk_domain;alpha(lambda);epsilon_EM_extra", "R3;R4;R7;R8;R9;R10;R11"),
        ("OB3558_1_PiM_commutator", "[d,Pi_M]J_H", "projector variation or metric/Hodge/source-domain dependence shifts the Hilbert mass current", "Hilbert identity/inclusion Pi_M or parent fixed chain map", "Delta_PiM;C_M;C_shape;projector_metric_stress", "R3;R4;R7;R8;R10;R11"),
        ("OB3558_2_parent_anomaly", "A_parent", "unowned multiplier/readout mask/anomaly modifies the projected source identity", "first-class/gauge/topological owner or no multiplier", "closure_only_anomaly_residual", "R1;R4;R7;R9;R11"),
        ("OB3558_3_boundary_symplectic", "Delta_symp", "H_tau/non-EH symplectic boundary flux shifts the source charge", "integrable H_tau and exact/zero boundary flux", "C_curl;epsilon_boundary;epsilon_EM_extra", "Gdot;Newton;PPN"),
        ("OB3558_4_worldtube_reference", "C_domain+C_ref+C_units", "worldtube, reference subtraction, or units selected after readout launders mass normalization", "support/reference/denominator parent-owned before readout", "radial_profile;C_ref;C_units", "Newton_GM;R10;Gdot"),
        ("OB3558_5_frame_species", "Delta_frame + eta_source_AB", "source variation does not use the same observed branch or carries material labels", "same-frame selector-blind source action", "delta_frame_source;eta_source_AB", "WEP;clock;source-normalized Newton"),
        ("OB3558_6_Gauss_calibration", "Delta_cal", "closed charge is not yet shown to be the orbital inverse-square mass", "Gauss/orbital readout theorem", "radial_profile;Delta_cal", "Newton mechanics"),
        ("OB3558_7_PPN_source_stability", "Delta_PPN", "first-order source closure does not automatically set beta/gamma/local-GR residuals", "second-order source-normalized weak-field calculation", "delta_beta_source;gamma_minus_1", "local GR"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "obstruction_id": obstruction_id,
            "symbolic_piece": symbolic_piece,
            "meaning": meaning,
            "zero_condition": zero_condition,
            "fallback_input": fallback_input,
            "affected_rows": affected_rows,
            "source_path": str(source_paths["charge_current_residuals"]),
            "current_status": "RETAINED_UNFILLED_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for obstruction_id, symbolic_piece, meaning, zero_condition, fallback_input, affected_rows in rows
    ]


def coefficient_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("CF3558_0_sigma_Gdot", "time_drift", "sigma_Gdot", "d ln(mu_obs)/dt contribution from G_N, M_H and mu_extra", "MISSING_PARENT_COEFFICIENT_OR_DERIVED_ZERO", "yr^-1", "9.6e-15 yr^-1", "P8_time_drift_residual_or_zero.csv"),
        ("CF3558_1_eta_source_AB", "species_source_charge", "eta_source_AB", "composition/species dependence of active source charge", "MISSING_SELECTOR_BLIND_THEOREM_OR_ETA_SOURCE_VECTOR", "dimensionless", "2.8e-15", "P8_species_source_charge_residual_or_zero.csv"),
        ("CF3558_2_radial_profile", "radial_Meff_hair", "partial_r_ln_mu_obs;epsilon_radial_MH(r)", "radial drift of linked-surface Hilbert mass or exterior source strength", "MISSING_GAUSS_NOHAIR_THEOREM_OR_PROFILE", "inverse_length_or_dimensionless_profile", "MISSING_RADIAL_PROFILE_BOUND", "P8_radial_mu_profile_or_zero.csv"),
        ("CF3558_3_frame_split", "frame_calibration_split", "delta_frame_source", "source variation and matter/orbital/clock readout frame mismatch", "MISSING_SAME_FRAME_SOURCE_THEOREM_OR_DELTA_FRAME", "dimensionless", "proxy WEP/clock bounds only", "P8_frame_source_split_residual_or_zero.csv"),
        ("CF3558_4_mu_extra", "extra_mass_projection", "mu_extra_boundary_bulk_domain/(G_N M_H)", "non-Hilbert mass-channel projection from boundary, bulk, domain, memory, range, connection, nonminimal EM or q_loc", "MISSING_ZERO_THEOREM_OR_CHANNEL_VECTOR_VALUES", "dimensionless_or_channel_declared", "R3/R4/R7/R8/R9/R10/R11 locks", "P8_mu_extra_over_Geff_Meff_vector.csv"),
        ("CF3558_5_PiM_commutator", "projector_commutator", "Delta_PiM;C_M;C_shape", "projector variation/source-shape leakage in Pi_M J_H", "MISSING_HILBERT_IDENTITY_PIM_ADOPTION_OR_CHAINMAP_PROOF", "dimensionless_or_operator_units", "PPN/R11/source-normalization locks", "P8_PiM_commutator_or_zero.csv"),
        ("CF3558_6_EM_flux", "EM_field_stress_and_flux", "epsilon_EM_extra;Phi_EM_rad", "ordinary EM stress dressing or nonstationary/nonminimal Poynting leakage", "CONDITIONAL_ZERO_IF_MINIMAL_STATIONARY_ELSE_MISSING_FLUX_COEFFICIENT", "dimensionless_or_flux_units", "Gdot/PPN/local-flux locks", "P8_EM_Poynting_source_flux_or_cross_term_vector.csv"),
        ("CF3558_7_PPN_source", "second_order_source_stability", "delta_beta_source;gamma_minus_1", "PPN source-normalized weak-field residue after first-order Hilbert closure", "MISSING_SECOND_ORDER_SOURCE_PPN_VECTOR", "dimensionless", "gamma 2.3e-5; beta 7.8e-5", "P8_second_order_source_normalized_PPN_vector.csv"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": coefficient_id,
            "channel": channel,
            "symbol": symbol,
            "definition": definition,
            "current_value_or_theorem": value,
            "units": units,
            "bound_or_lock": bound,
            "required_artifact": artifact,
            "source_path": str(source_paths["mu_extra_vector"] if "mu_extra" in symbol or "EM" in channel else source_paths["bounds_3557"]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for coefficient_id, channel, symbol, definition, value, units, bound, artifact in rows
    ]


def decisions() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3558_0",
            "decision": "Same-frame Hilbert current closure is derivable in principle.",
            "meaning": "The exact theorem is not a plateau axiom: it follows from a variational Hilbert current, Pi_M chainmap/identity, zero extra mass current, zero anomaly, and fixed worldtube/frame data.",
            "claim_effect": "conditional theorem only; not a live local-GR/Newton claim",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3558_1",
            "decision": "Current MTS still fails live source-current closure.",
            "meaning": "Pi_M dJ_extra, [d,Pi_M]J_H, A_parent, boundary symplectic flux, worldtube/reference selectors, frame/species source split, and PPN stability are not all parent-signed.",
            "claim_effect": "coefficient rows remain active",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3558_2",
            "decision": "Poynting intuition is integrated rather than ignored.",
            "meaning": "Stationary minimal EM stress is part of the dressed Hilbert source; nonstationary or nonminimal Poynting/cross-term leakage remains an explicit coefficient row.",
            "claim_effect": "EM energy cannot be double-counted or silently discarded",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3558_3",
            "decision": "Next target is parent adoption of the Hilbert identity/inclusion Pi_M plus q-basic source support.",
            "meaning": "That route attacks the largest obstruction [d,Pi_M]J_H without introducing new topological projector stress.",
            "claim_effect": "3559 should try to parent-sign the Pi_M chainmap/source-support theorem",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3558_0",
            "target_doc": "3559-Y5-R2FR-Hilbert-identity-PiM-chainmap-source-support-adoption-or-bound.md",
            "target_script": "scripts/Y5_R2FR_3559_Hilbert_identity_PiM_chainmap_source_support_adoption_or_bound.py",
            "objective": "try to parent-sign Pi_M as the Hilbert mass-current identity/inclusion chainmap with q-basic source support and fixed tau/e_obs; if not, fill Delta_PiM, C_M, C_shape, C_domain, C_frame and source-support coefficient rows",
            "success_gate": "[d,Pi_M]J_H=0 and source support fixed before readout, or projector/source-support residuals become source-ready bound rows",
            "reason": "3558 shows the closure theorem is exact but the Pi_M commutator/source-support gate is the cleanest next obstruction",
            "valid_for_claim": False,
        }
    ]


def validation(source_paths: dict[str, Path], outputs: dict[str, Path], theorem: list[dict[str, object]], clauses: list[dict[str, object]], coeffs: list[dict[str, object]]) -> list[dict[str, object]]:
    missing_sources = [str(path) for path in source_paths.values() if not path.exists()]
    parse_failures: list[str] = []
    for path in outputs.values():
        if path.suffix.lower() == ".csv":
            try:
                read_csv(path)
            except Exception as exc:
                parse_failures.append(f"{path}: {exc}")
    theorem_ids = {str(row["theorem_id"]) for row in theorem}
    clause_ids = {str(row["clause_id"]) for row in clauses}
    coeff_symbols = ";".join(str(row["symbol"]) for row in coeffs)
    unsafe_claims = [str(row["coefficient_id"]) for row in coeffs if str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true"]
    formalization_touched = any(FORMALIZATION in path.parents or path == FORMALIZATION for path in outputs.values())
    rows = [
        ("VAL3558_0_sources_exist", not missing_sources, f"{len(source_paths)-len(missing_sources)}/{len(source_paths)} cited source paths exist" if not missing_sources else "; ".join(missing_sources)),
        ("VAL3558_1_generated_csvs_parse", not parse_failures, f"{sum(1 for path in outputs.values() if path.suffix.lower()=='.csv')} generated CSV files parse" if not parse_failures else "; ".join(parse_failures)),
        ("VAL3558_2_obstruction_identity_present", "HC3558_1_projected_flux_obstruction_identity" in theorem_ids and "HC3558_2_closure_sufficient_conditions" in theorem_ids, "obstruction identity and sufficient closure theorem present"),
        ("VAL3558_3_closure_clauses_present", {"CL3558_0_same_frame","CL3558_2_PiM_chainmap","CL3558_3_extra_mass_silence","CL3558_6_stationary_no_flux"}.issubset(clause_ids), "same-frame, PiM, extra-mass, and flux clauses present"),
        ("VAL3558_4_required_coefficient_rows_present", all(token in coeff_symbols for token in ["sigma_Gdot","eta_source_AB","partial_r_ln_mu_obs","delta_frame_source","mu_extra"]), "sigma_Gdot, eta_source_AB, radial profile, frame split, and mu_extra rows present"),
        ("VAL3558_5_coefficients_nonclaim", not unsafe_claims, "all coefficient rows remain nonclaim until source values/theorems exist" if not unsafe_claims else "; ".join(unsafe_claims)),
        ("VAL3558_6_formalization_workbench_untouched", not formalization_touched, "3558 generated outputs only inside post-checkpoint-work"),
    ]
    return [
        {
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
        }
        for validation_id, passes, detail in rows
    ]


def write_doc(output_paths: dict[str, Path], theorem: list[dict[str, object]], clauses: list[dict[str, object]], coeffs: list[dict[str, object]], decision_rows: list[dict[str, object]], next_rows: list[dict[str, object]]) -> None:
    lines = [
        "# 3558 - Same-frame Hilbert source-current closure or coefficient fill",
        "",
        "## Verdict",
        "3558 gets the source-current problem into its sharp form. The closure theorem is exact: if the same observed coframe/time/source branch defines the Hilbert current, `Pi_M` is the Hilbert mass-current identity/inclusion chainmap, extra currents have zero mass projection, and boundary/worldtube/frame data are fixed before readout, then `d(Pi_M J_H)=0` and the first-order Newton source charge is stable.",
        "",
        "But the current MTS branch has not signed all those clauses. The honest status is conditional theorem plus coefficient rows, not a local-GR claim.",
        "",
        "## Exact obstruction",
        "`d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent`.",
        "",
        "So the live boss fight is not vague coupling anymore. It is three concrete terms: projected extra-current, Pi_M commutator, and parent anomaly/multiplier.",
        "",
        "## What moved",
        "- The cleanest `Pi_M` route is now selected: Hilbert identity/inclusion, not a new topological projector with extra stress.",
        "- Ordinary stationary EM stress is dressed into `M_H`; only nonminimal or radiative Poynting leakage remains as `mu_extra`.",
        "- First-order Newton is reachable if the Hilbert current closure and Gauss/orbital readout clauses are parent-signed.",
        "- Full local GR still needs PPN source stability after that.",
        "",
        "## Generated outputs",
    ]
    for name, path in output_paths.items():
        lines.append(f"- `{name}`: `{path}`")
    lines.extend(["", "## Key theorem rows"])
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['statement']}")
    lines.extend(["", "## Clause audit"])
    for row in clauses:
        lines.append(f"- `{row['clause_id']}`: {row['required_clause']} -> {row['current_status']}")
    lines.extend(["", "## Coefficient fill rows"])
    for row in coeffs:
        lines.append(f"- `{row['coefficient_id']}` `{row['symbol']}`: {row['current_value_or_theorem']}")
    lines.extend(["", "## Decision ledger"])
    for row in decision_rows:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} {row['meaning']}")
    lines.extend(["", "## Next target", f"- `{next_rows[0]['target_doc']}`", f"- Objective: {next_rows[0]['objective']}"])
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    source_rows = source_register(source_paths)
    theorem = theorem_rows(source_paths)
    clauses = clause_audit(source_paths)
    obstructions = obstruction_rows(source_paths)
    coeffs = coefficient_rows(source_paths)
    decision_rows = decisions()
    next_rows = next_target()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3558_SOURCE_REGISTER.csv",
        "closure_theorem": RESIDUALS / "P8_Y5_R2FR_3558_HILBERT_CURRENT_CLOSURE_THEOREM.csv",
        "clause_audit": RESIDUALS / "P8_Y5_R2FR_3558_CLOSURE_CLAUSE_AUDIT.csv",
        "obstruction_map": RESIDUALS / "P8_Y5_R2FR_3558_OBSTRUCTION_RESIDUAL_MAP.csv",
        "coefficient_fill": RESIDUALS / "P8_Y5_R2FR_3558_COEFFICIENT_FILL_ROWS.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3558_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3558_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3558_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_same_frame_Hilbert_source_current_closure_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3558_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["closure_theorem"], theorem)
    write_csv(outputs["clause_audit"], clauses)
    write_csv(outputs["obstruction_map"], obstructions)
    write_csv(outputs["coefficient_fill"], coeffs)
    write_csv(outputs["decision_ledger"], decision_rows)
    write_csv(outputs["status"], [{
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "status_id": "STAT3558_0",
        "status": "EXACT_CLOSURE_THEOREM_WRITTEN_UNSIGNED_COEFFICIENT_ROWS_ACTIVE",
        "summary": "d(Pi_M J_H)=0 follows from explicit same-frame/PiM/extra-current/anomaly/flux clauses, but current MTS has not signed them together.",
        "claim_allowed": False,
        "valid_for_claim": False,
    }])
    write_csv(outputs["next_target"], next_rows)
    write_csv(outputs["canonical_status"], [{
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "canonical_status": "SAME_FRAME_HILBERT_SOURCE_CURRENT_CLOSURE_CONDITIONAL_UNSIGNED",
        "strongest_result": "exact obstruction identity and sufficient theorem; Hilbert identity/inclusion Pi_M selected as cleanest route",
        "next_target": next_rows[0]["target_doc"],
        "claim_allowed": False,
        "valid_for_claim": False,
    }])
    validation_rows = validation(source_paths, {key: path for key, path in outputs.items() if key != "validation"}, theorem, clauses, coeffs)
    write_csv(outputs["validation"], validation_rows)
    write_doc(outputs, theorem, clauses, coeffs, decision_rows, next_rows)
    for path in [DOC, *outputs.values()]:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
