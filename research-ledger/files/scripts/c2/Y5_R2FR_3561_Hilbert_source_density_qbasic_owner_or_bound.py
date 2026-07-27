from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3561-Y5-R2FR-Hilbert-source-density-qbasic-owner-or-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_HILBERT_SOURCE_DENSITY_QBASIC_3561"
CHECKPOINT_ID = "3561"


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
        "handoff_3560": RESIDUALS / "P8_Y5_R2FR_3560_NEXT_TARGET.csv",
        "support_theorem_3560": RESIDUALS / "P8_Y5_R2FR_3560_SOURCE_SUPPORT_QBASIC_THEOREM.csv",
        "support_bounds_3560": RESIDUALS / "P8_Y5_R2FR_3560_BOUND_VECTOR.csv",
        "hilbert_signature_3293": RESIDUALS / "P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv",
        "hilbert_source_3340": RESIDUALS / "P8_Y5_R2FR_3340_HILBERT_SOURCE_THEOREM_OR_FAIL.csv",
        "hilbert_descent_3055": RESIDUALS / "P8_Y5_R2FR_3055_HILBERT_SOURCE_DESCENT_THEOREM_ATTEMPT.csv",
        "no_source_only_3509": RESIDUALS / "P8_EM_no_source_only_matter_functor_residual.csv",
        "hom_audit_2612": RESIDUALS / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_SOURCE_ONLY_HOM_AUDIT.csv",
        "minimal_matter_contract_2587": RESIDUALS / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv",
        "matter_normalization_2646": RESIDUALS / "P8_Y5_MATTER_NORMALIZATION_OWNER_2646_OWNER_THEOREM_ATTEMPT.csv",
        "ordinary_matter_signature_2647": RESIDUALS / "P8_Y5_ORDINARY_MATTER_SIGNATURE_2647_SIGNATURE_ATTEMPT.csv",
        "em_qbasic_3142": RESIDUALS / "P8_Y5_R2FR_3142_EM_QBASIC_THEOREM.csv",
        "poynting_qbasic_3285": RESIDUALS / "P8_Y5_R2FR_3285_POYNTING_QBASIC_LEMMA.csv",
        "em_weight_measure_3127": RESIDUALS / "P8_Y5_R2FR_3127_HILBERT_EM_WEIGHT_MEASURE_OUTPUT.csv",
        "current_source_ward_3508": RESIDUALS / "P8_EM_current_source_Ward_alpha_source_residual.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3560": "declares 3561 target",
        "support_theorem_3560": "imports support descent theorem depending on q-basic density",
        "support_bounds_3560": "imports E_rho_qbasic and EM flux bound rows",
        "hilbert_signature_3293": "single descended Hilbert-source signature and source-only exclusion",
        "hilbert_source_3340": "sufficient Hilbert source theorem and fallback vector",
        "hilbert_descent_3055": "single universal matter action and countermodel survival",
        "no_source_only_3509": "source-only matter functor residuals",
        "hom_audit_2612": "no-source-only Hom audit",
        "minimal_matter_contract_2587": "minimal parent matter coupling contract",
        "matter_normalization_2646": "matter normalization owner and source-weight countermodel",
        "ordinary_matter_signature_2647": "ordinary matter action signature and kernel fallback",
        "em_qbasic_3142": "q-basic Maxwell sector and Hilbert stress/Poynting readout",
        "poynting_qbasic_3285": "Poynting q-basic lemma and flux escape",
        "em_weight_measure_3127": "Hilbert EM stress energy measure and static/radiative guard",
        "current_source_ward_3508": "current/source Ward residuals and non-Hilbert bypass",
    }
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": roles[source_id],
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
            "theorem_id": "HDQ3561_0_density_definition",
            "name": "same-frame Hilbert source density",
            "statement": "Define rho_H dV_H := n_mu tau_nu T_H^{mu nu}[e_obs,A_obs,psi,theta] dSigma_H, with T_H from variation of the same matter+EM action before readout.",
            "derivation": "This is the density entering the 3560 support functor; it is not orbital GM, not a post-fit domain mask, and not a separate source selector.",
            "required_premises": "same e_obs/tau; Hilbert variation before readout; ordinary matter+stationary EM stress included",
            "current_status": "EXACT_DEFINITION_WITH_UNSIGNED_OWNER",
            "payoff": "gives the object whose q-basicness controls the worldtube theorem",
            "source_path": str(source_paths["support_theorem_3560"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "HDQ3561_1_pullback_density_theorem",
            "name": "Hilbert density q-basic pullback theorem",
            "statement": "If S_matter+S_EM=q^*Sbar_src[q(Phi),psi,theta] with fixed representation data, no source-only weights, q-basic measure/coframe/time/EM coefficient, and variation-before-readout, then rho_H dV_H=rhobar_H(q(Phi),psi,theta).",
            "derivation": "Functional differentiation of a pullback source action gives a stress tensor whose geometric arguments are the q-owned observed stack. Contracting it with q-owned n, tau and dSigma keeps the density in the q-basic algebra.",
            "required_premises": "single descended source action; no w_A/kappa_A/hidden marker source slot; q-basic EM sector; same-frame source readout",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_LIVE",
            "payoff": "would set E_rho_qbasic=0 for vertical residual directions",
            "source_path": str(source_paths["hilbert_signature_3293"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "HDQ3561_2_vertical_zero_corollary",
            "name": "density vertical-zero corollary",
            "statement": "If rho_H dV_H=rhobar_H(q(Phi),psi,theta) and v_X is vertical with Dq(v_X)=0 while matter labels are fixed/gauge/on-shell, then D_X(rho_H dV_H)=0.",
            "derivation": "Apply the chain rule: D_X(rho_H dV_H)=d rhobar_H(Dq(v_X)) plus matter/gauge/Euler terms. The first vanishes by verticality and the remaining terms vanish only under the fixed/gauge/on-shell source-branch premise.",
            "required_premises": "actual q map; actual vertical basis; no hidden matter lift; no boundary source layer",
            "current_status": "EXACT_COROLLARY_NOT_LIVE",
            "payoff": "feeds 3560 support descent and kills the density part of Delta_support",
            "source_path": str(source_paths["support_theorem_3560"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "HDQ3561_3_source_weight_countermodel",
            "name": "source-only weight countermodel",
            "statement": "If S_src=sum_A(1+epsilon_A(X))S_A or T_source=sum_A kappa_A(X)T_A is legal before variation, then rho_H is not q-basic in general even when ordinary equations can look acceptable.",
            "derivation": "Hilbert variation differentiates the weighted action-density line, so D_X rho_H contains sum_A D_X epsilon_A rho_A or D_X kappa_A rho_A. These terms are active-source density variations, not removable by post-readout calibration.",
            "required_premises": "countermodel legal unless no-Hom/source-signature theorem forbids it",
            "current_status": "EXACT_COUNTERMODEL_RETAINED",
            "payoff": "prevents false promotion of the density theorem",
            "source_path": str(source_paths["matter_normalization_2646"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "HDQ3561_4_EM_density_branch",
            "name": "EM stress density q-basic branch",
            "statement": "If the Maxwell sector is q-basic with fixed Z_Q and stationary/no-net-flux support, then the EM contribution to rho_H dV_H is q-basic; radiative or nonminimal Poynting leakage is an explicit E_EM_flux row.",
            "derivation": "T_EM is the Hilbert variation of the q-basic Maxwell scalar density. Its observed energy density and Poynting flux are contractions with q-owned tetrad data. Nonstationary boundary flux obeys the energy-balance law and cannot be folded into static mass density silently.",
            "required_premises": "q-basic Maxwell action; fixed Z_Q; stationary support or explicit flux coefficient",
            "current_status": "EXACT_CONDITIONAL_THEOREM_WITH_FLUX_ESCAPE",
            "payoff": "integrates Poynting intuition without double-counting it",
            "source_path": str(source_paths["em_qbasic_3142"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "HDQ3561_5_live_density_verdict",
            "name": "current density-owner verdict",
            "statement": "The q-basic density theorem is mathematically clean but not live for current MTS because the parent has not signed the unique matter grammar, no-source-only Hom exclusion, non-Hilbert current silence, q-basic EM ownership, actual q-map verticality and boundary regularity together.",
            "derivation": "Existing source rows mark each clause as conditional or unsigned, and retained countermodels show why Ward/Hilbert language alone is insufficient.",
            "required_premises": "all HDQ3561 clauses parent-signed together",
            "current_status": "CONDITIONAL_THEOREM_PLUS_BOUND_ROWS",
            "payoff": "turns the density bottleneck into finite residual rows",
            "source_path": str(source_paths["hilbert_source_3340"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def clause_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("HDC3561_0_single_source_action", "S_src=q^*Sbar_src[q(Phi),psi,theta] owns matter+EM source density", "TARGET_SHARP_NOT_PARENT_SIGNED", "without it rho_H may have hidden dependence", "hilbert_signature_3293"),
        ("HDC3561_1_no_source_only_weights", "no w_A(X), kappa_A(X), hidden marker or source-only prefactor", "NOT_DERIVED_COUNTERMODEL_RETAINED", "blocks E_rho_qbasic zero", "no_source_only_3509"),
        ("HDC3561_2_noHom_source_slot", "Hom(species/hidden/readout selector, active-source-prefactor) empty or common constant", "NOT_DERIVED", "needed to forbid source-only weights as grammar", "hom_audit_2612"),
        ("HDC3561_3_variation_before_readout", "T_H and J_H are functional derivatives before material projection/support fitting", "CONDITIONAL_WORKFLOW_CONTRACT", "blocks readout mask and source calibration laundering", "minimal_matter_contract_2587"),
        ("HDC3561_4_qbasic_EM", "Maxwell/Hodge sector has q-basic Z_Q and no extra F^2 counterterm", "CONDITIONAL_UNSIGNED", "needed for EM density q-basicness", "em_qbasic_3142"),
        ("HDC3561_5_flux_guard", "stationary support has no unresolved Poynting/radiative boundary leakage", "CONDITIONAL_UNSIGNED", "needed to use EM energy as static source density", "em_weight_measure_3127"),
        ("HDC3561_6_nonHilbert_silence", "non-Hilbert currents are exact improvements with zero exterior flux or explicit residuals", "RETAINED_PARALLEL_GATE", "blocks density closure if active sources bypass Hilbert variation", "current_source_ward_3508"),
        ("HDC3561_7_actual_vertical_basis", "actual residual directions satisfy Dq(v_X)=0", "MISSING_ACTUAL_QMAP_AND_BASIS", "required for any q-basic zero claim", "support_bounds_3560"),
        ("HDC3561_8_boundary_regular_density", "rho_H support boundary has no hidden source shell/birth-death event", "UNSIGNED_FROM_3560", "needed before q-basic density gives q-basic support", "support_theorem_3560"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": clause_id,
            "required_clause": required_clause,
            "status": status,
            "effect": effect,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for clause_id, required_clause, status, effect, source_key in rows
    ]


def residual_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("HDR3561_0_E_action_pullback", "E_action_pullback", "source action not proven to factor through q", "LIVE_UNSIGNED", "single descended matter+EM source action", "source-action owner", "minimal_matter_contract_2587"),
        ("HDR3561_1_delta_w_species", "delta_w_species", "relative species/action-density source weights", "LIVE_COUNTERMODEL", "no source-only weights and one action-density line", "species source weights", "matter_normalization_2646"),
        ("HDR3561_2_kappa_A_source", "kappa_A_source", "post-variation active-source coupling selector", "LIVE_COUNTERMODEL", "source functor sees only total Hilbert source object", "active source selector", "no_source_only_3509"),
        ("HDR3561_3_hidden_marker_source", "hidden_marker_source", "hidden/domain/material marker feeding source coefficient", "LIVE_UNSIGNED", "no-Hom from hidden marker to source coefficient", "hidden source marker", "hom_audit_2612"),
        ("HDR3561_4_nonHilbert_bypass", "nonHilbert_source_bypass", "active source current not generated by Hilbert variation", "LIVE_PARALLEL_GATE", "exact improvement with zero exterior flux or explicit bound", "non-Hilbert current", "current_source_ward_3508"),
        ("HDR3561_5_EM_coefficient_drift", "D_X Z_Q;extra_F2", "Maxwell/Hodge coefficient or extra F^2 term not q-owned", "LIVE_UNSIGNED", "q-basic Maxwell sector and no extra F^2 counterterms", "EM source density", "em_qbasic_3142"),
        ("HDR3561_6_EM_flux", "Phi_EM_rad;epsilon_EM_extra", "radiative/nonminimal Poynting flux not part of stationary density", "LIVE_UNSIGNED", "stationary/no-net-flux branch or explicit flux row", "EM boundary flux", "poynting_qbasic_3285"),
        ("HDR3561_7_readout_mask", "Delta_mask", "support/source density selected after readout", "LIVE_GUARD", "variation-before-readout and no fitted domain mask", "readout source mask", "minimal_matter_contract_2587"),
        ("HDR3561_8_E_rho_qbasic_total", "E_rho_qbasic", "total vertical derivative of rho_H dV_H after all density-owner channels", "BOUND_VECTOR_REQUIRED_IF_THEOREM_UNSIGNED", "all density-owner channels zero or numeric", "density total", "support_bounds_3560"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "residual_id": residual_id,
            "symbol": symbol,
            "meaning": meaning,
            "status": status,
            "zero_condition": zero_condition,
            "gate": gate,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for residual_id, symbol, meaning, status, zero_condition, gate, source_key in rows
    ]


def bound_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("BD3561_0_E_action_pullback", "source_action_pullback", "E_action_pullback", "failure of S_src to factor through q-owned observed stack", "MISSING_PARENT_SOURCE_ACTION_PULLBACK_OR_BOUND", "dimensionless_action_density_slope", "WEP;R10;PPN;orbital;Gdot", "P8_source_action_pullback_density_bound.csv", "minimal_matter_contract_2587"),
        ("BD3561_1_delta_w_species", "relative_species_weight", "delta_w_species", "relative active source density weight between matter species", "MISSING_NO_SOURCE_ONLY_WEIGHT_THEOREM_OR_NUMERIC_EPSILON_A", "dimensionless", "WEP;composition;R10;source_normalization", "P8_density_species_weight_bound.csv", "matter_normalization_2646"),
        ("BD3561_2_kappa_A_source", "active_source_selector", "kappa_A_source", "post-variation source coupling selector", "MISSING_SOURCE_LABEL_FORGETTING_OR_KAPPA_VECTOR", "dimensionless", "WEP;R10;PPN;orbital", "P8_kappa_A_source_selector_bound.csv", "no_source_only_3509"),
        ("BD3561_3_hidden_marker_source", "hidden_marker_source", "hidden_marker_source", "hidden/domain/material marker to source coefficient", "MISSING_NOHOM_HIDDEN_MARKER_OR_BOUND", "dimensionless", "preferred_frame;PPN;source_composition", "P8_hidden_marker_source_bound.csv", "hom_audit_2612"),
        ("BD3561_4_nonHilbert_bypass", "nonHilbert_current", "nonHilbert_source_bypass", "active source current not from Hilbert variation", "MISSING_IMPROVEMENT_ZERO_FLUX_OR_NONHILBERT_BOUND", "flux_or_dimensionless", "PPN;source_normalization;boundary_flux", "P8_nonHilbert_source_bypass_bound.csv", "current_source_ward_3508"),
        ("BD3561_5_EM_coefficient_drift", "EM_qbasic_coefficient", "D_X Z_Q;extra_F2", "non-q-owned Maxwell/Hodge coefficient or extra F^2 term", "MISSING_QBASIC_MAXWELL_OWNER_OR_COEFFICIENT_BOUND", "dimensionless", "alpha_EM;clocks;Coulomb;source_density", "P8_EM_qbasic_density_coefficient_bound.csv", "em_qbasic_3142"),
        ("BD3561_6_EM_flux", "EM_Poynting_flux", "Phi_EM_rad;epsilon_EM_extra", "radiative/nonminimal Poynting leakage outside stationary density", "MISSING_STATIONARY_FLUX_ZERO_OR_NUMERIC_FLUX_BOUND", "flux_ratio", "clocks;PPN;local source;EM", "P8_EM_density_flux_bound.csv", "em_weight_measure_3127"),
        ("BD3561_7_readout_mask", "readout_mask", "Delta_mask", "post-fit/source-domain readout mask in density", "MISSING_NO_READOUT_MASK_THEOREM_OR_BOUND", "dimensionless", "anti-tautology;all local arenas", "P8_density_readout_mask_bound.csv", "minimal_matter_contract_2587"),
        ("BD3561_8_E_rho_qbasic_total", "density_total", "E_rho_qbasic", "total density q-basic failure feeding support theorem", "NONCLAIM_SUM_OF_ROWS_UNTIL_ALL_COMPONENTS_ZERO_OR_NUMERIC", "dimensionless_or_declared", "WEP;R10;PPN;orbital;Gdot;support", "P8_density_qbasic_total_bound_vector.csv", "support_bounds_3560"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": bound_id,
            "channel": channel,
            "symbol": symbol,
            "definition": definition,
            "current_value_or_theorem": current_value_or_theorem,
            "units": units,
            "observable_links": observable_links,
            "required_artifact": required_artifact,
            "source_path": str(source_paths[source_key]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for bound_id, channel, symbol, definition, current_value_or_theorem, units, observable_links, required_artifact, source_key in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3561_0",
            "decision": "The Hilbert density q-basic theorem is derived conditionally.",
            "meaning": "One descended matter+EM Hilbert action with no source-only weights makes rho_H dV_H a q-basic density, so 3560 support descent can fire.",
            "claim_effect": "conditional theorem only",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3561_1",
            "decision": "The live obstruction is no-Hom/source-only grammar.",
            "meaning": "The countermodel S_src=sum_A(1+epsilon_A(X))S_A survives unless the parent object language forbids relative active-source weights.",
            "claim_effect": "density rows remain nonclaim",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3561_2",
            "decision": "EM/Poynting is included without double-counting.",
            "meaning": "q-basic stationary Maxwell stress contributes to rho_H; radiative/nonminimal flux remains a separate E_EM_flux row.",
            "claim_effect": "Poynting intuition becomes disciplined source-density bookkeeping",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3561_3",
            "decision": "Next target should attack the no-source-only Hom theorem.",
            "meaning": "If species/hidden/readout selectors cannot map to active-source prefactors, the density theorem becomes much closer to live.",
            "claim_effect": "sets up 3562",
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STAT3561_0",
            "status": "HILBERT_DENSITY_QBASIC_THEOREM_DERIVED_UNSIGNED",
            "summary": "rho_H dV_H is q-basic if one descended matter+EM source action owns the Hilbert density, no source-only weights or non-Hilbert bypasses exist, EM coefficients are q-owned, and readout/boundary flux terms are fixed or explicit.",
            "strongest_result": "conditional pullback theorem: S_src=q^*Sbar_src implies rho_H dV_H=rhobar_H(q(Phi),psi,theta)",
            "still_missing": "no-source-only Hom theorem, parent matter grammar uniqueness, non-Hilbert flux silence, q-basic Maxwell ownership, actual q vertical basis, support regularity",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3561_0",
            "target_doc": "3562-Y5-R2FR-no-source-only-Hom-theorem-or-density-weight-bound.md",
            "target_script": "scripts/Y5_R2FR_3562_no_source_only_Hom_theorem_or_density_weight_bound.py",
            "objective": "try to prove species labels, hidden markers and readout/worldtube selectors have no parent Hom into active-source prefactors except common constants; if not, fill delta_w_species, kappa_A_source, hidden_marker_source and Delta_mask bound rows",
            "success_gate": "source-only active weight theorem signed, or every surviving source-weight channel becomes a source-ready nonclaim bound row",
            "reason": "3561 shows rho_H q-basicness is blocked mainly by legal source-only weights and non-Hilbert bypasses",
            "valid_for_claim": False,
        }
    ]


def validation(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    residuals: list[dict[str, object]],
    bounds: list[dict[str, object]],
) -> list[dict[str, object]]:
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
    residual_ids = {str(row["residual_id"]) for row in residuals}
    bound_ids = {str(row["bound_id"]) for row in bounds}
    unsafe_claims = [
        str(row["bound_id"])
        for row in bounds
        if str(row.get("valid_for_claim", "")).lower() == "true"
        or str(row.get("score_ready", "")).lower() == "true"
        or str(row.get("claim_allowed", "")).lower() == "true"
    ]
    formalization_touched = any(path == FORMALIZATION or FORMALIZATION in path.parents for path in outputs.values())
    rows = [
        ("VAL3561_0_sources_exist", not missing_sources, f"{len(source_paths)-len(missing_sources)}/{len(source_paths)} cited source paths exist" if not missing_sources else "; ".join(missing_sources)),
        ("VAL3561_1_generated_csvs_parse", not parse_failures, f"{sum(1 for path in outputs.values() if path.suffix.lower()=='.csv')} generated CSV files parse" if not parse_failures else "; ".join(parse_failures)),
        ("VAL3561_2_density_theorem_present", {"HDQ3561_1_pullback_density_theorem","HDQ3561_2_vertical_zero_corollary","HDQ3561_3_source_weight_countermodel"}.issubset(theorem_ids), "pullback theorem, vertical-zero corollary and countermodel rows present"),
        ("VAL3561_3_source_only_clauses_present", {"HDC3561_1_no_source_only_weights","HDC3561_2_noHom_source_slot","HDC3561_6_nonHilbert_silence"}.issubset(clause_ids), "source-only and non-Hilbert clauses present"),
        ("VAL3561_4_residual_decomposition_present", {"HDR3561_1_delta_w_species","HDR3561_2_kappa_A_source","HDR3561_4_nonHilbert_bypass","HDR3561_8_E_rho_qbasic_total"}.issubset(residual_ids), "species, source selector, non-Hilbert and total density residuals present"),
        ("VAL3561_5_bound_rows_nonclaim", not unsafe_claims, "all bound rows remain nonclaim" if not unsafe_claims else "; ".join(unsafe_claims)),
        ("VAL3561_6_required_bound_rows_present", {"BD3561_1_delta_w_species","BD3561_2_kappa_A_source","BD3561_3_hidden_marker_source","BD3561_4_nonHilbert_bypass","BD3561_6_EM_flux","BD3561_8_E_rho_qbasic_total"}.issubset(bound_ids), "source weight, hidden marker, non-Hilbert, EM flux and total density rows present"),
        ("VAL3561_7_formalization_workbench_untouched", not formalization_touched, "3561 generated outputs only inside post-checkpoint-work"),
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


def write_doc(
    output_paths: dict[str, Path],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    residuals: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> None:
    lines = [
        "# 3561 - Hilbert source density q-basic owner or bound",
        "",
        "## Verdict",
        "3561 derives the clean density-owner theorem: if the source action is one descended matter+EM Hilbert action `S_src=q^*Sbar_src[q(Phi),psi,theta]`, with fixed representation data, q-owned measure/coframe/time/EM coefficients, no source-only weights, no non-Hilbert bypass, and variation before readout, then `rho_H dV_H` is q-basic.",
        "",
        "So for a true vertical residual direction `Dq(v_X)=0`, the density derivative vanishes: `D_X(rho_H dV_H)=0`. That is exactly the missing input needed by the 3560 worldtube/support lemma.",
        "",
        "But it is not live yet. The surviving countermodel is simple and dangerous: `S_src=sum_A(1+epsilon_A(X))S_A` or `T_source=sum_A kappa_A(X)T_A`. Ordinary equations can look respectable while the active source density is still weighted. That has to be forbidden by parent grammar or bounded.",
        "",
        "## Density theorem",
        "`S_src=q^*Sbar_src` implies `T_H=Tbar_H(q(Phi),psi,theta)`; contracting with q-owned `n`, `tau` and `dSigma_H` gives `rho_H dV_H=rhobar_H(q(Phi),psi,theta)`.",
        "",
        "The theorem fails exactly through named channels: source-only weights, hidden markers, non-Hilbert currents, non-q-owned EM coefficients, radiative Poynting flux, readout masks, or nonvertical `Dq(v_X)`.",
        "",
        "## What moved",
        "- The density bottleneck is now a precise pullback theorem, not a vague coupling complaint.",
        "- The source-only species-weight countermodel is explicitly retained and cannot be waved away by Ward identities.",
        "- EM/Poynting is split correctly: stationary q-basic Maxwell stress is in `rho_H`; radiative/nonminimal flux is a bound row.",
        "- The next clean target is the no-source-only `Hom` theorem for active-source prefactors.",
        "",
        "## Generated outputs",
    ]
    for name, path in output_paths.items():
        lines.append(f"- `{name}`: `{path}`")
    lines.extend(["", "## Theorem rows"])
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['statement']}")
    lines.extend(["", "## Clause audit"])
    for row in clauses:
        lines.append(f"- `{row['clause_id']}`: {row['required_clause']} -> {row['status']}")
    lines.extend(["", "## Residual decomposition"])
    for row in residuals:
        lines.append(f"- `{row['residual_id']}` `{row['symbol']}`: {row['status']} ({row['meaning']})")
    lines.extend(["", "## Bound rows"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}` `{row['symbol']}`: {row['current_value_or_theorem']}")
    lines.extend(["", "## Decision ledger"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} {row['meaning']}")
    lines.extend(["", "## Next target", f"- `{next_rows[0]['target_doc']}`", f"- Objective: {next_rows[0]['objective']}"])
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    source_rows = source_register(source_paths)
    theorem = theorem_rows(source_paths)
    clauses = clause_rows(source_paths)
    residuals = residual_rows(source_paths)
    bounds = bound_rows(source_paths)
    decisions = decision_rows()
    statuses = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3561_SOURCE_REGISTER.csv",
        "density_qbasic_theorem": RESIDUALS / "P8_Y5_R2FR_3561_HILBERT_DENSITY_QBASIC_THEOREM.csv",
        "density_clause_audit": RESIDUALS / "P8_Y5_R2FR_3561_DENSITY_CLAUSE_AUDIT.csv",
        "density_residual_decomposition": RESIDUALS / "P8_Y5_R2FR_3561_DENSITY_RESIDUAL_DECOMPOSITION.csv",
        "bound_vector": RESIDUALS / "P8_Y5_R2FR_3561_BOUND_VECTOR.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3561_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3561_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3561_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_Hilbert_source_density_qbasic_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3561_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["density_qbasic_theorem"], theorem)
    write_csv(outputs["density_clause_audit"], clauses)
    write_csv(outputs["density_residual_decomposition"], residuals)
    write_csv(outputs["bound_vector"], bounds)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], statuses)
    write_csv(outputs["next_target"], next_rows)
    write_csv(outputs["canonical_status"], [{
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "canonical_status": statuses[0]["status"],
        "strongest_result": statuses[0]["strongest_result"],
        "still_missing": statuses[0]["still_missing"],
        "next_target": next_rows[0]["target_doc"],
        "claim_allowed": False,
        "valid_for_claim": False,
    }])
    validation_rows = validation(source_paths, {key: path for key, path in outputs.items() if key != "validation"}, theorem, clauses, residuals, bounds)
    write_csv(outputs["validation"], validation_rows)
    write_doc(outputs, theorem, clauses, residuals, bounds, decisions, next_rows)
    for path in [DOC, *outputs.values()]:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
