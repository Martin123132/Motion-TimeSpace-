from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_SOURCE_SUPPORT_QBASIC_WORLDTUBE_3560"
CHECKPOINT_ID = "3560"


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
        "handoff_3559": RESIDUALS / "P8_Y5_R2FR_3559_NEXT_TARGET.csv",
        "adoption_theorem_3559": RESIDUALS / "P8_Y5_R2FR_3559_HILBERT_IDENTITY_PIM_ADOPTION_THEOREM.csv",
        "obstruction_3559": RESIDUALS / "P8_Y5_R2FR_3559_SOURCE_SUPPORT_OBSTRUCTION_MAP.csv",
        "coefficients_3559": RESIDUALS / "P8_Y5_R2FR_3559_COEFFICIENT_BOUND_ROWS.csv",
        "source_coordinate_descent_3516": RESIDUALS / "P8_EM_quotient_source_coordinate_descent_certificate.csv",
        "source_connection_law_3515": RESIDUALS / "P8_EM_source_branch_mass_connection_flatness_law.csv",
        "mhref_descent_3551": RESIDUALS / "P8_Y5_R2FR_3551_MHREF_DESCENT_THEOREM.csv",
        "htau_qbasic_3552": RESIDUALS / "P8_Y5_R2FR_3552_HTAU_QBASIC_THEOREM.csv",
        "worldtube_owner_2611": RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv",
        "current_source_ward_3508": RESIDUALS / "P8_EM_current_source_Ward_alpha_source_residual.csv",
        "ellj_source_owner": RESIDUALS / "P8_EM_ellJ_source_current_owner_residual_law.csv",
        "actual_q_candidate": RESIDUALS / "P8_EM_actual_q_map_vertical_basis_candidate.csv",
        "dq_vertical_2570": RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv",
        "closure_theorem_3558": RESIDUALS / "P8_Y5_R2FR_3558_HILBERT_CURRENT_CLOSURE_THEOREM.csv",
        "em_poynting": RESIDUALS / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3559": "declares 3560 target",
        "adoption_theorem_3559": "imports Pi_M^H operator-zero branch",
        "obstruction_3559": "imports live source-support obstruction split",
        "coefficients_3559": "imports support/domain/frame coefficient rows",
        "source_coordinate_descent_3516": "q-basic source-coordinate theorem",
        "source_connection_law_3515": "A_X=dY(v_X) and mass-flatness corollary",
        "mhref_descent_3551": "M_H_ref q-basic difference theorem",
        "htau_qbasic_3552": "H_tau q-basic and integrability guard",
        "worldtube_owner_2611": "worldtube support parent ownership audit",
        "current_source_ward_3508": "Hilbert/source functor and no-source-only residuals",
        "ellj_source_owner": "source-current residual decomposition",
        "actual_q_candidate": "visible q slots and anti-tautology guard",
        "dq_vertical_2570": "actual q-map/vertical-basis ledger",
        "closure_theorem_3558": "same-frame Hilbert source-current closure theorem",
        "em_poynting": "EM Hilbert/Poynting stress dressing and leakage rows",
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
            "theorem_id": "SWT3560_0_support_functor_definition",
            "name": "Hilbert support functor definition",
            "statement": "Define rho_H[tau,e_obs]=n_mu tau_nu T_H^{mu nu} and W_source:=closure(supp(rho_H dV_H)) on the same e_obs/tau branch before readout.",
            "derivation": "The support is defined from the Hilbert density itself, not from orbital GM, R10 fitting, or an external domain mask.",
            "required_premises": "T_H exists from the same matter+EM Hilbert variation; tau/e_obs are fixed; compact regular support",
            "current_status": "EXACT_DEFINITION_WITH_UNSIGNED_INPUTS",
            "payoff": "removes fitted source-domain freedom if parent-owned",
            "source_path": str(source_paths["worldtube_owner_2611"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "SWT3560_1_qbasic_support_lemma",
            "name": "q-basic support descent lemma",
            "statement": "If rho_H dV_H is q-basic and the support has a stable regular boundary class, then W_source descends through q; for v_X in ker(Dq), D_X W_source=0.",
            "derivation": "rho_H dV_H=rhobar_H(q(Phi)) implies D_X(rho_H dV_H)=drhobar_H(Dq(v_X))=0. The support of an unchanged regular density is unchanged under vertical variation, except for explicitly retained birth/death boundary events.",
            "required_premises": "rho_H q-basic; actual vertical basis; no zero-crossing/birth-death of support; no readout domain mask",
            "current_status": "EXACT_CONDITIONAL_ZERO_THEOREM_NOT_LIVE",
            "payoff": "kills Delta_W and the support part of C_domain if premises are signed",
            "source_path": str(source_paths["source_coordinate_descent_3516"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "SWT3560_2_Reynolds_shape_moment_zero",
            "name": "shape moment vertical-zero lemma",
            "statement": "For sigma^a=I^a[W_source,rho_H,e_obs,tau]/M_H_ref, D_X sigma^a=0 if I^a, rho_H dV_H and M_H_ref are q-basic and W_source is vertically fixed.",
            "derivation": "Use Reynolds transport: D_X int_W f rho dV = int_W D_X(f rho dV)+int_boundary f rho v_n dS. The bulk term is zero for q-basic integrand and Dq(v_X)=0; the boundary term is zero for fixed support or vanishing density on the regular support boundary. Dividing by q-basic M_H_ref preserves q-basicness.",
            "required_premises": "q-basic moment integrand; W_source fixed; rho_H boundary regularity; M_H_ref q-basic and positive",
            "current_status": "EXACT_CONDITIONAL_ZERO_THEOREM_NOT_LIVE",
            "payoff": "kills C_shape once M_H_ref and support descent are signed",
            "source_path": str(source_paths["source_connection_law_3515"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "SWT3560_3_Y_qbasic_bundle_theorem",
            "name": "Y source-coordinate q-basic bundle theorem",
            "statement": "If M_H_ref is q-basic and the support/shape coordinates sigma^a are q-basic, then Y=(M_H_ref,sigma^a)=Ybar(q(Phi)); for v_X in ker(Dq), A_X=dY(v_X)=0.",
            "derivation": "Combine the M_H_ref difference theorem with the support and shape lemmas. Then apply the chain rule A_X=dYbar(Dq(v_X)).",
            "required_premises": "H_tau/H_ref q-basic; support lemma; actual Dq(v_X)=0",
            "current_status": "EXACT_CONDITIONAL_BUNDLE_THEOREM_NOT_LIVE",
            "payoff": "kills A_X, C_M, C_shape and the source-coordinate part of Delta_support",
            "source_path": str(source_paths["mhref_descent_3551"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "SWT3560_4_failure_decomposition",
            "name": "support descent failure decomposition",
            "statement": "If the support theorem does not fire, D_X Y decomposes into E_rho_qbasic + E_boundary_birth + E_Dq + E_tau_eobs + E_Href + E_readout_mask + E_EM_flux.",
            "derivation": "Apply the chain rule plus Reynolds transport to the source density and support integrals, then isolate non-q-basic density, boundary motion, nonvertical directions, same-frame drift, reference drift, readout masks and EM leakage.",
            "required_premises": "none; this is the nonclaim bookkeeping law",
            "current_status": "EXACT_RESIDUAL_DECOMPOSITION",
            "payoff": "surviving source-support failure becomes source-ready rows rather than a vague coupling complaint",
            "source_path": str(source_paths["coefficients_3559"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "SWT3560_5_local_closure_consequence",
            "name": "local closure consequence after support descent",
            "statement": "With 3559 Pi_M^H adoption plus SWT3560_1 through SWT3560_3, Delta_W=C_domain=C_shape=C_M=0. The remaining local closure gates are Pi_M^H dJ_extra, A_parent and side flux.",
            "derivation": "3559 removes the identity-operator commutator. 3560 removes the source-support/source-coordinate drift if the q-basic support bundle theorem fires.",
            "required_premises": "Pi_M^H branch adoption; support descent; M_H_ref descent; actual q vertical basis",
            "current_status": "CONDITIONAL_REDUCTION_NOT_LOCAL_GR_CLAIM",
            "payoff": "turns the local-GR route into three remaining source-current gates",
            "source_path": str(source_paths["adoption_theorem_3559"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def clause_audit(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("SCL3560_0_rho_H_qbasic", "rho_H dV_H descends through q from same matter+EM Hilbert variation", "UNSIGNED", "blocks support descent", "current_source_ward_3508"),
        ("SCL3560_1_regular_support", "support boundary is compact, regular and has no vertical birth/death event", "NEW_REGULARITY_PREMISE_UNSIGNED", "blocks W_source zero if matter density can appear/disappear at boundary", "worldtube_owner_2611"),
        ("SCL3560_2_no_readout_mask", "no fitted/source-specific domain mask enters W_source", "GUARD_ACTIVE_NOT_THEOREM", "prevents orbital-GM laundering", "actual_q_candidate"),
        ("SCL3560_3_MHref_qbasic", "M_H_ref=H_tau-H_ref descends through q", "CONDITIONAL_UNSIGNED", "blocks C_M zero", "mhref_descent_3551"),
        ("SCL3560_4_actual_vertical_basis", "actual residual directions satisfy Dq(v_X)=0", "MISSING_ACTUAL_QMAP_AND_BASIS", "blocks all q-basic zero claims", "dq_vertical_2570"),
        ("SCL3560_5_same_frame_tau_eobs", "same tau/e_obs branch feeds source density, support, charge and readout", "CONDITIONAL_UNSIGNED", "blocks frame/domain zero", "closure_theorem_3558"),
        ("SCL3560_6_EM_stress_dressing", "stationary minimal EM stress included in T_H; nonstationary/nonminimal flux retained", "CONDITIONAL_DRESSING_RULE", "prevents Poynting double-counting", "em_poynting"),
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
        ("SRD3560_0_E_rho_qbasic", "E_rho_qbasic", "D_X(rho_H dV_H) not forced to zero", "LIVE_UNSIGNED", "same matter+EM Hilbert functor q-basic", "source density owner", "current_source_ward_3508"),
        ("SRD3560_1_E_boundary_birth", "E_boundary_birth", "support boundary births, deaths, discontinuities or distributional layers", "LIVE_UNSIGNED", "regular compact support class and no source-shell retune", "regularity gate", "worldtube_owner_2611"),
        ("SRD3560_2_E_Dq_source", "Dq(v_X)", "residual direction is not proven vertical for the actual q map", "LIVE_UNSIGNED", "actual q map and basis", "verticality gate", "dq_vertical_2570"),
        ("SRD3560_3_E_tau_eobs", "Delta_tau+Delta_eobs", "source density and support not evaluated on same frame as readout", "LIVE_UNSIGNED", "same-frame tau/e_obs lock", "frame gate", "closure_theorem_3558"),
        ("SRD3560_4_E_Href", "D_X H_ref", "reference selector drift contaminates M_H_ref", "LIVE_UNSIGNED", "source-blind H_ref", "reference gate", "mhref_descent_3551"),
        ("SRD3560_5_E_readout_mask", "Delta_mask", "domain/support chosen after readout or arena fit", "LIVE_UNSIGNED", "variation-before-readout and no domain mask", "anti-tautology gate", "actual_q_candidate"),
        ("SRD3560_6_E_EM_flux", "Phi_EM_rad;epsilon_EM_extra", "nonstationary or nonminimal EM/Poynting leakage outside T_H", "LIVE_UNSIGNED", "stationary minimal EM stress or explicit flux row", "EM stress gate", "em_poynting"),
        ("SRD3560_7_Delta_support_total", "Delta_W+C_domain+C_shape+C_frame", "total source-support drift after 3559 Pi_M^H adoption", "BOUND_VECTOR_REQUIRED_IF_THEOREM_UNSIGNED", "all support theorem clauses zero", "support total", "coefficients_3559"),
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
        ("BF3560_0_E_rho_qbasic", "source_density_descent", "E_rho_qbasic", "normalized vertical derivative of Hilbert source density", "MISSING_JH_QBASIC_OWNER_OR_BOUND", "dimensionless_or_density_weighted", "WEP;R10;PPN;orbital source", "P8_JH_density_qbasic_or_bound.csv", "current_source_ward_3508"),
        ("BF3560_1_E_boundary_birth", "support_regular_boundary", "E_boundary_birth", "support birth/death or boundary layer term in Reynolds transport", "MISSING_REGULAR_SUPPORT_CERTIFICATE_OR_BOUND", "boundary_flux_or_dimensionless", "Gdot;orbital radial hair;PPN", "P8_support_regular_boundary_or_bound.csv", "worldtube_owner_2611"),
        ("BF3560_2_E_Dq_source", "actual_verticality", "E_Dq_source", "actual q-map verticality failure for source residual direction", "MISSING_ACTUAL_QMAP_VERTICAL_BASIS", "map_norm", "all local invisibility gates", "P8_actual_qmap_source_vertical_basis.csv", "dq_vertical_2570"),
        ("BF3560_3_E_tau_eobs", "same_frame_support", "Delta_tau;Delta_eobs;C_frame", "frame/coframe/time mismatch in source support", "MISSING_SAME_FRAME_SOURCE_SUPPORT_LOCK_OR_BOUND", "dimensionless", "clock;PPN alpha_i;R10;orbital", "P8_same_frame_support_bound.csv", "closure_theorem_3558"),
        ("BF3560_4_E_Href", "reference_selector", "D_X H_ref", "source-blind reference failure in M_H_ref", "MISSING_HREF_SOURCE_BLINDNESS_OR_BOUND", "charge_units_or_dimensionless_ratio", "R10 denominator;orbital GM;Gdot", "P8_Href_source_blindness_or_bound.csv", "mhref_descent_3551"),
        ("BF3560_5_E_readout_mask", "readout_domain_mask", "Delta_mask", "post-fit support/domain selector", "MISSING_NO_READOUT_MASK_THEOREM_OR_BOUND", "dimensionless", "anti-tautology;all local tests", "P8_no_readout_domain_mask_or_bound.csv", "actual_q_candidate"),
        ("BF3560_6_E_EM_flux", "EM_Poynting_leakage", "Phi_EM_rad;epsilon_EM_extra", "radiative/nonminimal EM stress not inside stationary Hilbert source", "MISSING_STATIONARY_MINIMAL_EM_ZERO_OR_FLUX_BOUND", "flux_ratio", "clocks;Coulomb;PPN;local source", "P8_EM_flux_support_bound.csv", "em_poynting"),
        ("BF3560_7_Delta_support_total", "support_total", "Delta_W+C_domain+C_shape+C_frame", "total source-support residual for 3559 preferred branch", "NONCLAIM_SUM_OF_ROWS_UNTIL_ALL_COMPONENTS_ZERO_OR_NUMERIC", "dimensionless_or_declared", "PPN;R10;Gdot;orbital", "P8_source_support_total_bound_vector.csv", "coefficients_3559"),
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
            "decision_id": "DEC3560_0",
            "decision": "The source-support descent lemma exists.",
            "meaning": "If the Hilbert density is q-basic and its support is regular, the worldtube support descends too. This is an actual derivation route, not just a missing-label audit.",
            "claim_effect": "conditional theorem only",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3560_1",
            "decision": "The new hard premise is rho_H q-basicness plus regular support.",
            "meaning": "The support problem has been pushed back to the source-density owner and boundary regularity, which is a sharper target than generic coupling.",
            "claim_effect": "E_rho_qbasic and E_boundary_birth remain active",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3560_2",
            "decision": "Poynting/EM stress stays inside the same rule.",
            "meaning": "Stationary minimal EM energy is part of the Hilbert density support; radiative or nonminimal Poynting leakage is not ignored and becomes E_EM_flux.",
            "claim_effect": "no EM double-counting",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3560_3",
            "decision": "Next target should prove or bound rho_H q-basicness.",
            "meaning": "Without the Hilbert source density owner, the worldtube theorem cannot go live even though the support lemma is mathematically clean.",
            "claim_effect": "sets up 3561",
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STAT3560_0",
            "status": "SOURCE_SUPPORT_QBASIC_LEMMA_DERIVED_UNSIGNED",
            "summary": "If rho_H dV_H is q-basic, support is regular, M_H_ref is q-basic, and Dq(v_X)=0, then W_source and sigma^a are vertically fixed, so Delta_W, C_domain, C_shape and C_M vanish.",
            "strongest_result": "conditional support/worldtube descent theorem with Reynolds boundary obstruction isolated",
            "still_missing": "rho_H q-basic owner, regular support certificate, H_tau/H_ref q-basic lock, actual q-map vertical basis, EM flux silence",
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
            "next_id": "NEXT3560_0",
            "target_doc": "3561-Y5-R2FR-Hilbert-source-density-qbasic-owner-or-bound.md",
            "target_script": "scripts/Y5_R2FR_3561_Hilbert_source_density_qbasic_owner_or_bound.py",
            "objective": "try to prove rho_H dV_H is q-basic from the same matter+EM Hilbert functor with no source-only weights, or fill E_rho_qbasic, prevariation_weight, nonHilbert_bypass and EM_flux bound rows",
            "success_gate": "rho_H q-basic theorem signed, or every density-owner failure becomes a source-ready nonclaim bound row",
            "reason": "3560 proves support descent conditional on q-basic Hilbert density; the density owner is now the bottleneck",
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
        ("VAL3560_0_sources_exist", not missing_sources, f"{len(source_paths)-len(missing_sources)}/{len(source_paths)} cited source paths exist" if not missing_sources else "; ".join(missing_sources)),
        ("VAL3560_1_generated_csvs_parse", not parse_failures, f"{sum(1 for path in outputs.values() if path.suffix.lower()=='.csv')} generated CSV files parse" if not parse_failures else "; ".join(parse_failures)),
        ("VAL3560_2_support_lemma_present", {"SWT3560_1_qbasic_support_lemma","SWT3560_2_Reynolds_shape_moment_zero","SWT3560_3_Y_qbasic_bundle_theorem"}.issubset(theorem_ids), "support, Reynolds shape, and Y q-basic theorem rows present"),
        ("VAL3560_3_regular_support_clause_present", "SCL3560_1_regular_support" in clause_ids, "regular support/no birth-death clause present"),
        ("VAL3560_4_failure_decomposition_present", {"SRD3560_0_E_rho_qbasic","SRD3560_1_E_boundary_birth","SRD3560_7_Delta_support_total"}.issubset(residual_ids), "rho, boundary, and total support residuals present"),
        ("VAL3560_5_bound_rows_nonclaim", not unsafe_claims, "all bound rows remain nonclaim" if not unsafe_claims else "; ".join(unsafe_claims)),
        ("VAL3560_6_required_bound_rows_present", {"BF3560_0_E_rho_qbasic","BF3560_1_E_boundary_birth","BF3560_2_E_Dq_source","BF3560_6_E_EM_flux","BF3560_7_Delta_support_total"}.issubset(bound_ids), "rho, boundary, Dq, EM flux, and total support rows present"),
        ("VAL3560_7_formalization_workbench_untouched", not formalization_touched, "3560 generated outputs only inside post-checkpoint-work"),
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
        "# 3560 - Source-support q-basic worldtube descent or bound vector",
        "",
        "## Verdict",
        "3560 derives the worldtube/support route in the clean form: if the Hilbert source density `rho_H dV_H` is q-basic, the support is regular, `M_H_ref` is q-basic, and the residual direction is genuinely vertical (`Dq(v_X)=0`), then `W_source`, the shape coordinates `sigma^a`, and `Y=(M_H_ref,sigma^a)` descend through `q`.",
        "",
        "That gives the wanted zero route: `D_X W_source=0`, `D_X sigma^a=0`, `A_X=dY(v_X)=0`, hence `Delta_W=C_domain=C_shape=C_M=0` on the preferred 3559 `Pi_M^H` branch.",
        "",
        "Still not a local-GR claim. The newly exposed boss is sharper: prove `rho_H dV_H` is q-basic and the support boundary is regular, or bound those failures.",
        "",
        "## Exact support lemma",
        "`rho_H dV_H=rhobar_H(q(Phi))` and `Dq(v_X)=0` imply `D_X(rho_H dV_H)=0`.",
        "",
        "For a regular support class, unchanged density means unchanged support. For shape moments, Reynolds transport gives a bulk term plus a boundary term; both vanish only when the integrand is q-basic and the support boundary has no birth/death or leakage event.",
        "",
        "## What moved",
        "- The worldtube is now tied to the Hilbert density support, not an arbitrary fitted domain.",
        "- `C_shape` and `C_domain` have a real zero route through q-basic support descent.",
        "- A new honest regularity gate appears: boundary birth/death or source-shell layers must be zero or bounded.",
        "- Poynting/EM is handled consistently: stationary minimal EM stress is in `rho_H`; radiative/nonminimal leakage is `E_EM_flux`.",
        "- Next target is the Hilbert density owner: prove or bound `rho_H dV_H` q-basicness.",
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
    clauses = clause_audit(source_paths)
    residuals = residual_rows(source_paths)
    bounds = bound_rows(source_paths)
    decisions = decision_rows()
    statuses = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3560_SOURCE_REGISTER.csv",
        "support_qbasic_theorem": RESIDUALS / "P8_Y5_R2FR_3560_SOURCE_SUPPORT_QBASIC_THEOREM.csv",
        "support_clause_audit": RESIDUALS / "P8_Y5_R2FR_3560_SUPPORT_CLAUSE_AUDIT.csv",
        "support_residual_decomposition": RESIDUALS / "P8_Y5_R2FR_3560_SUPPORT_RESIDUAL_DECOMPOSITION.csv",
        "bound_vector": RESIDUALS / "P8_Y5_R2FR_3560_BOUND_VECTOR.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3560_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3560_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3560_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_source_support_qbasic_worldtube_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3560_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["support_qbasic_theorem"], theorem)
    write_csv(outputs["support_clause_audit"], clauses)
    write_csv(outputs["support_residual_decomposition"], residuals)
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
