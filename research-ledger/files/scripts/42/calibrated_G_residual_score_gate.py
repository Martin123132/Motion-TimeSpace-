from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Tuple


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(value: object) -> Optional[float]:
    try:
        if value is None:
            return None
        text = str(value).strip()
        if not text or text.upper().startswith("MISSING") or text == "alpha(lambda)":
            return None
        return float(text)
    except (TypeError, ValueError):
        return None


def row_by_observable(rows: Iterable[Mapping[str, object]], observable: str) -> Optional[Mapping[str, object]]:
    for row in rows:
        if str(row.get("observable", "")) == observable:
            return row
    return None


def nearest_r10_bound(
    r10_rows: Iterable[Mapping[str, object]],
    target_lambda_m: float,
) -> Optional[Tuple[Mapping[str, object], float, float, float]]:
    candidates: List[Tuple[float, Mapping[str, object], float, float]] = []
    for row in r10_rows:
        lambda_value = as_float(row.get("lambda_value"))
        alpha_bound = as_float(row.get("alpha_bound"))
        if lambda_value is None or alpha_bound is None or lambda_value <= 0 or alpha_bound <= 0:
            continue
        distance = abs(math.log(lambda_value / target_lambda_m))
        candidates.append((distance, row, lambda_value, alpha_bound))
    if not candidates:
        return None
    _, row, lambda_value, alpha_bound = sorted(candidates, key=lambda item: item[0])[0]
    return row, lambda_value, alpha_bound, abs(lambda_value - target_lambda_m)


def bound_anchor_rows(
    local_bound_rows: List[Dict[str, str]],
    r10_review_rows: List[Dict[str, str]],
    r10_live_rows: List[Dict[str, str]],
    target_lambda_m: float = 7.639299809562832e-05,
) -> List[Dict[str, object]]:
    observable_map = [
        ("BA4464_0_WEP_direct", "MICROSCOPE_WEP", "eta_WEP_direct_geometry", "direct geometry/WEP null row"),
        ("BA4464_1_WEP_source", "MICROSCOPE_WEP", "eta_WEP_source_charge", "source-charge proxy for Delta_C_AB product"),
        ("BA4464_2_clock", "CLOCK_REDSHIFT", "alpha_clock_redshift", "clock/redshift source-frame row"),
        ("BA4464_3_gamma", "PPN_LIGHT", "gamma_minus_1", "Cassini PPN gamma row"),
        ("BA4464_4_beta", "PPN_ORBIT", "beta_minus_1", "planetary/LLR PPN beta row"),
        ("BA4464_5_alpha1", "PPN_PREFERRED_FRAME", "alpha1", "preferred-frame alpha1 row"),
        ("BA4464_6_alpha2", "PPN_PREFERRED_FRAME", "alpha2", "preferred-frame alpha2 row"),
        ("BA4464_7_alpha3", "PPN_MOMENTUM_FLUX", "alpha3", "momentum-flux alpha3 row"),
        ("BA4464_8_xi", "PPN_PREFERRED_LOCATION", "xi", "preferred-location xi row"),
        ("BA4464_9_Gdot", "LLR_GDOT", "Gdot_over_G", "time-drift of calibrated coupling row"),
    ]
    rows: List[Dict[str, object]] = []
    for anchor_id, arena, observable, notes in observable_map:
        source = row_by_observable(local_bound_rows, observable)
        rows.append(
            {
                "anchor_id": anchor_id,
                "arena": arena,
                "observable": observable,
                "bound_value": source.get("upper_bound", "MISSING_BOUND") if source else "MISSING_BOUND",
                "units": source.get("units", "MISSING_UNITS") if source else "MISSING_UNITS",
                "source_ref": source.get("reference_path_or_url", "MISSING_SOURCE") if source else "MISSING_SOURCE",
                "source_status": "SOURCE_BACKED_EMPIRICAL_BOUND" if source else "MISSING_LOCAL_BOUND_ROW",
                "extraction_method": source.get("confidence_label", "MISSING_EXTRACTION") if source else "MISSING_EXTRACTION",
                "theory_mapping": notes,
                "valid_for_claim": False,
                "notes": source.get("reference_note", "fill source-backed row") if source else "fill source-backed row",
            }
        )

    live_numeric = [
        row
        for row in r10_live_rows
        if as_float(row.get("lambda_value")) is not None and as_float(row.get("alpha_bound")) is not None
    ]
    review_nearest = nearest_r10_bound(r10_review_rows, target_lambda_m)
    if review_nearest:
        review_row, lambda_value, alpha_bound, delta_lambda = review_nearest
        cmatter_limit = math.sqrt(3.0 * alpha_bound)
        universal_alpha = 1.0 / 3.0
        rows.append(
            {
                "anchor_id": "BA4464_10_R10_review_candidate_at_lambda_R2",
                "arena": "R10_YUKAWA_SHORT_RANGE",
                "observable": "alpha_bound(lambda_R2_pressure)",
                "bound_value": f"{alpha_bound:.12g}",
                "units": "dimensionless_at_lambda_m",
                "source_ref": review_row.get("alpha_bound_source", "MISSING_SOURCE"),
                "source_status": "REVIEW_CANDIDATE_NONCLAIM_NOT_LIVE_CURVE",
                "extraction_method": review_row.get("digitization_method", "MISSING_METHOD"),
                "theory_mapping": f"nearest lambda={lambda_value:.12g} m to pressure lambda={target_lambda_m:.12g} m; |C_matter| <= {cmatter_limit:.6g}; alpha=1/3 pass={abs(universal_alpha) <= alpha_bound}",
                "valid_for_claim": False,
                "notes": f"review candidate only; delta_lambda={delta_lambda:.3g} m; live_numeric_rows={len(live_numeric)}",
            }
        )
    else:
        rows.append(
            {
                "anchor_id": "BA4464_10_R10_review_candidate_at_lambda_R2",
                "arena": "R10_YUKAWA_SHORT_RANGE",
                "observable": "alpha_bound(lambda_R2_pressure)",
                "bound_value": "MISSING_NUMERIC_REVIEW_BOUND",
                "units": "dimensionless_at_lambda_m",
                "source_ref": "MISSING_R10_REVIEW_CANDIDATE",
                "source_status": "MISSING_REVIEW_CANDIDATE",
                "extraction_method": "MISSING_METHOD",
                "theory_mapping": "cannot smoke-score R2 scalar against R10",
                "valid_for_claim": False,
                "notes": f"live_numeric_rows={len(live_numeric)}",
            }
        )
    return rows


def residual_zero_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "RZ4464_0_delta_kappa",
            "residual": "delta_kappa = D ln(kappa_eff)",
            "exact_zero_condition": "topological/superselection kappa sector plus Hilbert source-measure descent gives D ln(kappa_* Z_H)=0 on the connected local domain",
            "derivation_move": "separate calibrated value from drift: numeric G may be fitted, but time/space variation cannot be hidden",
            "status": "CONDITIONAL_ZERO_IF_CONNECTED_SECTOR_AND_ZH_DESCENT_SIGNED",
            "finite_fallback": "|Gdot/G| <= 9.6e-15 yr^-1 and spatial/frame drift rows",
            "primary_arena": "LLR_GDOT; clocks; orbital ephemerides",
            "bound_anchor_id": "BA4464_9_Gdot",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RZ4464_1_Delta_C_AB",
            "residual": "Delta_C_AB = C_A - C_B",
            "exact_zero_condition": "one adopted standard matter action, one Hilbert source, empty source-Hom, and source-label-forgetting for material composition",
            "derivation_move": "turn the coupling problem into a functorial no-extra-source-label theorem rather than a fitted material coefficient",
            "status": "PRIVATE_BRANCH_CONDITIONAL_ZERO_NOT_GLOBAL_PARENT_PROOF",
            "finite_fallback": "|Delta_C_AB*C_S*alpha_0*Y(lambda)| <= 2.8e-15",
            "primary_arena": "MICROSCOPE_WEP",
            "bound_anchor_id": "BA4464_1_WEP_source",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RZ4464_2_C_S",
            "residual": "C_S - 1 or C_S source-normalization drift",
            "exact_zero_condition": "the exterior source charge is the same Hamiltonian/Hilbert worldtube mass that appears in Poisson/Gauss/Newton",
            "derivation_move": "make source mass anti-circular: defined by H_tau/M_H before orbital GM readout",
            "status": "CONDITIONAL_ZERO_IF_WORLDTUBE_CHARGE_AND_BOUNDARY_SILENCE_SIGNED",
            "finite_fallback": "WEP source response plus orbital/short-range source-charge rows",
            "primary_arena": "WEP; R10; orbital GM",
            "bound_anchor_id": "BA4464_1_WEP_source",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RZ4464_3_cD_qbar",
            "residual": "c_D/qbar_geom shadow-frame or disformal source readout",
            "exact_zero_condition": "ordinary matter, photons, clocks, rods and EM are functors of one observed coframe/metric with no second readout geometry",
            "derivation_move": "delete a whole family of PPN/WEP/clock leaks if the same-coframe selector is parent-owned",
            "status": "CONDITIONAL_ZERO_PRIVATE_SELECTOR",
            "finite_fallback": "PPN gamma/beta/preferred-frame and clock redshift bounds",
            "primary_arena": "PPN_LIGHT; CLOCK_REDSHIFT",
            "bound_anchor_id": "BA4464_3_gamma",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RZ4464_4_DeltaGamma_WEP",
            "residual": "DeltaGamma_WEP and connection-force leakage",
            "exact_zero_condition": "connection is Levi-Civita of g_obs, or non-LC pieces are algebraic/source-silent and vanish for spinless local matter",
            "derivation_move": "force local acceleration to be geodesic/Newtonian instead of an independent connection force",
            "status": "CONDITIONAL_ZERO_IF_CONNECTION_OWNER_AND_TORSION_MARGIN_SIGNED",
            "finite_fallback": "WEP, clocks and PPN residual vector",
            "primary_arena": "MICROSCOPE_WEP; PPN_LIGHT",
            "bound_anchor_id": "BA4464_0_WEP_direct",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RZ4464_5_alpha_R2",
            "residual": "alpha_eff(lambda_R2) finite curvature-scalar tail",
            "exact_zero_condition": "c_R2_eff=0 by refinement/hinge owner theorem, or C_matter=0 by scalar/source decoupling",
            "derivation_move": "universal metric scalar gives alpha=1/3, so the clean route is a real zero/decoupling theorem, not wishful small coupling",
            "status": "FINITE_BRANCH_PRESSURED_BY_R10_REVIEW_CANDIDATE",
            "finite_fallback": "alpha_eff = C_matter^2/3 <= alpha_bound(lambda_R2)",
            "primary_arena": "R10_YUKAWA_SHORT_RANGE; PPN_LIGHT; orbital inverse-square",
            "bound_anchor_id": "BA4464_10_R10_review_candidate_at_lambda_R2",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RZ4464_6_epsilon_EM",
            "residual": "epsilon_EM_extra_inner / standalone Poynting-background source",
            "exact_zero_condition": "Maxwell-Hodge stress and Poynting flux are Hilbert-stress components on g_obs with radiative boundary routing",
            "derivation_move": "keep the Poynting intuition, but put it inside the stress tensor unless an extra parent coefficient is signed",
            "status": "FIXED_BRANCH_CONDITIONAL_ZERO_OPEN_RADIATIVE_REENTRY",
            "finite_fallback": "EM side-channel coefficient and clock/source-energy rows",
            "primary_arena": "EM propagation; clocks; source energy accounting",
            "bound_anchor_id": "BA4464_2_clock",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RZ4464_7_PPN_preferred_frame",
            "residual": "alpha1, alpha2, alpha3, xi preferred-frame/preferred-location tails",
            "exact_zero_condition": "parent motion-frame gauge signature fixes local Lorentz/diffeomorphism structure without an extra local frame vector",
            "derivation_move": "A_MF-style frame closure converts preferred-frame rows into zero rows; otherwise they are brutally bounded",
            "status": "CONDITIONAL_ZERO_IF_A_MF_PARENT_SIGNATURE_SIGNED",
            "finite_fallback": "alpha1<=1e-4, alpha2<=2e-9, alpha3<=4e-20, xi<=4e-9",
            "primary_arena": "PPN preferred-frame/location",
            "bound_anchor_id": "BA4464_5_alpha1;BA4464_6_alpha2;BA4464_7_alpha3;BA4464_8_xi",
            "valid_for_claim": False,
        },
    ]


def first_score_pack_rows(bound_rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    bounds = {str(row["anchor_id"]): row for row in bound_rows}
    r10 = bounds.get("BA4464_10_R10_review_candidate_at_lambda_R2", {})
    r10_bound = as_float(r10.get("bound_value"))
    universal_alpha = 1.0 / 3.0
    if r10_bound and r10_bound > 0:
        r10_ratio = universal_alpha / r10_bound
        r10_status = "UNIVERSAL_ALPHA_FAILS_REVIEW_CANDIDATE_PRESSURE" if universal_alpha > r10_bound else "UNIVERSAL_ALPHA_PASSES_REVIEW_CANDIDATE_SMOKE"
        cmatter_limit = math.sqrt(3.0 * r10_bound)
    else:
        r10_ratio = math.nan
        r10_status = "R10_BOUND_MISSING"
        cmatter_limit = math.nan
    return [
        {
            "score_id": "SP4464_0_clean_calibrated_GR",
            "arena": "local_GR_Newton_clean_branch",
            "branch": "same Hilbert source, constant calibrated G, LC connection, no scalar/frame/EM leakage",
            "prediction_formula": "eta_AB=0; gamma-1=0; beta-1=0; Gdot/G=0; alpha(lambda)=0; orbital GM source-owned",
            "required_theory_inputs": "source functor, kappa drift zero, connection owner, c_R2/C_matter zero, no shadow frame, EM-Hilbert routing",
            "source_anchor": "4462/4463 local source-coupling and calibrated-G rows",
            "bound_value": "not a finite bound row",
            "branch_score_status": "THEOREM_CONDITIONAL_NOT_PUBLIC_CLAIM",
            "edge_dependency": "parent selector signatures must be signed together",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "score_id": "SP4464_1_WEP_species_source",
            "arena": "MICROSCOPE_WEP",
            "branch": "finite nonuniversal source charge",
            "prediction_formula": "|Delta_C_AB*C_S*alpha_0*(1+r/lambda)exp(-r/lambda)| <= 2.8e-15",
            "required_theory_inputs": "Delta_C_AB, C_S, alpha_0, lambda or same-source zero theorem",
            "source_anchor": "BA4464_1_WEP_source",
            "bound_value": bounds.get("BA4464_1_WEP_source", {}).get("bound_value", "MISSING"),
            "branch_score_status": "BOUND_OPERATOR_READY_BUT_THEORY_VECTOR_MISSING",
            "edge_dependency": "coupling/source universality is the most valuable next proof target",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "score_id": "SP4464_2_R10_R2_scalar",
            "arena": "R10_YUKAWA_SHORT_RANGE",
            "branch": "finite pure-R2 scalar with pressure lambda_R2=76.39299809562831 um",
            "prediction_formula": f"alpha_eff=C_matter^2/3; universal C_matter=1 gives alpha=1/3; review-bound ratio={r10_ratio:.6g}; |C_matter|<={cmatter_limit:.6g}",
            "required_theory_inputs": "c_R2_eff or c2 zero/finite value, C_matter, source-backed live alpha(lambda) curve",
            "source_anchor": "BA4464_10_R10_review_candidate_at_lambda_R2",
            "bound_value": r10.get("bound_value", "MISSING"),
            "branch_score_status": r10_status,
            "edge_dependency": "derive c_R2_eff=0, C_matter=0, screening, or a shorter/source-backed lambda",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "score_id": "SP4464_3_PPN_gamma_beta",
            "arena": "Cassini/planetary_PPN",
            "branch": "frame/connection/scalar light-propagation residual",
            "prediction_formula": "|gamma-1|<=2.3e-5; |beta-1|<=7.8e-5; scalar gamma(r)-1=-2 alpha_eff e^{-r/lambda}/(1+alpha_eff e^{-r/lambda})",
            "required_theory_inputs": "PPN projection matrix for DeltaGamma, c_D/qbar_geom, scalar tail and metric readout",
            "source_anchor": "BA4464_3_gamma;BA4464_4_beta",
            "bound_value": f"gamma={bounds.get('BA4464_3_gamma', {}).get('bound_value', 'MISSING')}; beta={bounds.get('BA4464_4_beta', {}).get('bound_value', 'MISSING')}",
            "branch_score_status": "EMPIRICAL_ANCHORS_READY_PROJECTION_MATRIX_MISSING",
            "edge_dependency": "PPN projection must be derived, not tuned after the fact",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "score_id": "SP4464_4_Gdot_clock",
            "arena": "LLR_GDOT_and_CLOCKS",
            "branch": "time variation of calibrated coupling/source-frame readout",
            "prediction_formula": "|D_t ln kappa_eff|<=9.6e-15 yr^-1; |alpha_clock|<=2.48e-5",
            "required_theory_inputs": "kappa/Z_H drift profile or topological zero, clock-source frame projection",
            "source_anchor": "BA4464_9_Gdot;BA4464_2_clock",
            "bound_value": f"Gdot={bounds.get('BA4464_9_Gdot', {}).get('bound_value', 'MISSING')}; clock={bounds.get('BA4464_2_clock', {}).get('bound_value', 'MISSING')}",
            "branch_score_status": "ANCHORS_READY_DRIFT_PROFILE_OR_ZERO_THEOREM_REQUIRED",
            "edge_dependency": "calibrated G is allowed only if its drift residual is separately zero/bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "score_id": "SP4464_5_orbital_GM_source",
            "arena": "orbital_GM_Newton_limit",
            "branch": "source mass/GM readout absorption guard",
            "prediction_formula": "Phi_N=-G_cal M_H^dress/r and a_r=-G_cal M_H^dress/r^2, with M_H defined before orbital fitting",
            "required_theory_inputs": "H_tau/MHref worldtube mass, compact-exterior flux closure, no extra source charge",
            "source_anchor": "4462 worldtube charge and Poisson/Newton rows",
            "bound_value": "no numeric score until source mass projection is filled",
            "branch_score_status": "THEORY_CONTRACT_READY_NUMERIC_SOURCE_PROJECTION_MISSING",
            "edge_dependency": "prevents hiding coupling errors in fitted GM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def arena_score_status_rows(score_rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for row in score_rows:
        status = str(row["branch_score_status"])
        rows.append(
            {
                "arena": row["arena"],
                "current_readiness": status,
                "score_ready": status in {
                    "BOUND_OPERATOR_READY_BUT_THEORY_VECTOR_MISSING",
                    "EMPIRICAL_ANCHORS_READY_PROJECTION_MATRIX_MISSING",
                    "ANCHORS_READY_DRIFT_PROFILE_OR_ZERO_THEOREM_REQUIRED",
                },
                "public_claim_ready": False,
                "next_needed": row["edge_dependency"],
                "valid_for_claim": False,
            }
        )
    return rows


def claim_gate_rows(
    source_rows: List[Dict[str, object]],
    bound_rows: List[Dict[str, object]],
    zero_rows: List[Dict[str, object]],
    score_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    source_paths_ok = all(str(row.get("local_path_exists")) == "True" or row.get("local_path_exists") is True for row in source_rows)
    needles_ok = all(str(row.get("needle_found")) == "True" or row.get("needle_found") is True for row in source_rows)
    r10_review = next((row for row in bound_rows if row.get("anchor_id") == "BA4464_10_R10_review_candidate_at_lambda_R2"), {})
    return [
        {
            "gate_id": "CG4464_0_sources",
            "claim": "all local source files exist and cited needles are found",
            "gate_pass": bool(source_paths_ok and needles_ok),
            "claim_allowed": False,
            "detail": "source register validates local handoff and bound files",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4464_1_bound_anchors",
            "claim": "WEP, clock, PPN, Gdot and R10 anchors are registered",
            "gate_pass": len(bound_rows) >= 11 and all(row.get("source_status") != "MISSING_LOCAL_BOUND_ROW" for row in bound_rows[:10]),
            "claim_allowed": False,
            "detail": "empirical anchors are source-backed where possible; R10 remains review-candidate/nonclaim",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4464_2_zero_theorem_attempt",
            "claim": "residual zero theorem clauses are explicit",
            "gate_pass": len(zero_rows) >= 8,
            "claim_allowed": False,
            "detail": "zero clauses are conditional; finite fallbacks are kept",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4464_3_score_pack",
            "claim": "first calibrated-G residual score pack is written",
            "gate_pass": len(score_rows) >= 6,
            "claim_allowed": False,
            "detail": "score pack separates clean theorem branch, WEP, R10, PPN, drift/clock and orbital source branches",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4464_4_R10_pressure",
            "claim": "universal R2 alpha=1/3 is not silently treated as safe",
            "gate_pass": "FAILS" in str(next((row for row in score_rows if row.get("score_id") == "SP4464_2_R10_R2_scalar"), {}).get("branch_score_status", "")),
            "claim_allowed": False,
            "detail": f"R10 status: {r10_review.get('theory_mapping', 'missing')}",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4464_5_public_local_GR",
            "claim": "public local-GR/Newton pass is allowed",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "conditional clean branch exists but source, frame, scalar and projection signatures are not globally signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4464_6_no_generated_claim_rows",
            "claim": "no generated row is promoted to claim evidence",
            "gate_pass": not any(str(row.get("valid_for_claim")).lower() == "true" for row in bound_rows + zero_rows + score_rows),
            "claim_allowed": False,
            "detail": "all 4464 rows remain private nonclaim",
            "valid_for_claim": False,
        },
    ]


def decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4464_0_score_result",
            "finding": "calibrated G is fair only if residual coupling channels are theorem-zero or explicitly bounded",
            "consequence": "the local problem is now a residual vector, not a vague missing-coupling complaint",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4464_1_coupling_priority",
            "finding": "the strongest route is to prove same-Hilbert/source-label-forgetting so WEP source charge vanishes",
            "consequence": "one proof can close Delta_C_AB, much of C_S, and a large chunk of fitted-G absorption risk",
            "next_action": "attack source-charge universality before chasing many isolated numeric bounds",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4464_2_R2_pressure",
            "finding": "the universal metric R2 scalar at the current pressure lambda is not safe under the review-candidate R10 curve",
            "consequence": "finite c2 needs a parent zero/decoupling/shorter-range derivation or a source-backed revised curve",
            "next_action": "keep R10 as pressure, not claim, while deriving c_R2_eff=0 or C_matter=0",
            "valid_for_claim": False,
        },
    ]
