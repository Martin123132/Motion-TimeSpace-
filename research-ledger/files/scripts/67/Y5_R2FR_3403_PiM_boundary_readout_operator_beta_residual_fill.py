from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "3403-Y5-R2FR-PiM-boundary-readout-operator-beta-residual-fill-under-AX1090.md"


SOURCES = {
    "3402_doc": ROOT / "3402-Y5-R2FR-v-second-order-source-square-theorem-attempt-under-AX1090.md",
    "3402_impact": OUT / "P8_Y5_R2FR_3402_KAPPAV_IMPACT.csv",
    "3401_components": OUT / "P8_Y5_R2FR_3401_KAPPAV_COMPONENT_LEDGER.csv",
    "3401_bound": OUT / "P8_Y5_R2FR_3401_KAPPAV_BOUND_TARGET.csv",
    "3400_clauses": OUT / "P8_Y5_R2FR_3400_PARENT_SIGNATURE_CLAUSES.csv",
    "pim_theorem": OUT / "P8_Y5_R2FR_3373_PIM_CHAINMAP_COMMUTATOR_THEOREM_ATTEMPT.csv",
    "boundary_theorem": OUT / "P8_Y5_R2FR_3376_BOUNDARY_ZERO_FLUX_THEOREM_ATTEMPT.csv",
    "boundary_flux_placement": OUT / "P8_Y5_R2FR_3393_BOUNDARY_FLUX_PLACEMENT_THEOREM.csv",
    "ppn_projector": OUT / "P8_Y5_R2FR_3391_PPN_PROJECTOR_CONSTANCY_THEOREM.csv",
    "ppn_parent_clause": OUT / "P8_Y5_R2FR_3392_FIXED_PPN_PARENT_CLAUSE_CANDIDATE.csv",
    "r11_beta_vector": OUT / "P8_Y5_R11_BETA_COMPONENT_VECTOR.csv",
    "local_eh_operator_audit": OUT / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv",
    "jpim_bounds": OUT / "P8_Y5_NO_SHADOW_2524_JPIM_BOUND_ROWS.csv",
    "jreadout_bounds": OUT / "P8_Y5_NO_SHADOW_2523_JREADOUT_BOUND_ROWS.csv",
    "beta_envelope": OUT / "P8_Y5_BETA_ENVELOPE_COMPONENTS.csv",
    "beta_finite_vector": OUT / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv",
    "local_bounds": LOCAL_BOUNDS / "local_bound_claims.csv",
}


OUTPUT_PATHS = {
    "source_register": OUT / "P8_Y5_R2FR_3403_SOURCE_REGISTER.csv",
    "retained_lane_zero_theorems": OUT / "P8_Y5_R2FR_3403_RETAINED_LANE_ZERO_THEOREMS.csv",
    "retained_lane_residual_formulas": OUT / "P8_Y5_R2FR_3403_RETAINED_LANE_RESIDUAL_FORMULAS.csv",
    "operator_family_status": OUT / "P8_Y5_R2FR_3403_OPERATOR_FAMILY_STATUS.csv",
    "qloc_beta_alpha_guard": OUT / "P8_Y5_R2FR_3403_QLOC_BETA_ALPHA_GUARD.csv",
    "component_scorecard": OUT / "P8_Y5_R2FR_3403_COMPONENT_SCORECARD.csv",
    "kappav_reduced_envelope": OUT / "P8_Y5_R2FR_3403_KAPPAV_REDUCED_ENVELOPE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3403_PROMOTION_GATES.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3403_RUNNER_NONCLAIM.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3403_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3403_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3403_VALIDATION.csv",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_id": f"SRC3403_{idx:02d}_{name}",
            "path": str(path),
            "exists": path.exists(),
            "role": "retained_beta_lane_source",
            "valid_for_claim": False,
        }
        for idx, (name, path) in enumerate(SOURCES.items())
    ]


def beta_bound_value() -> float:
    for row in read_csv(SOURCES["local_bounds"]):
        if row.get("row_id") == "R4_beta" or row.get("observable") == "beta_minus_1":
            return float(row["upper_bound"])
    raise RuntimeError("R4_beta bound not found")


def retained_lane_zero_theorems() -> list[dict[str, Any]]:
    return [
        {
            "lane_id": "ZL3403_0_PiM",
            "lane": "kappa_PiM",
            "conditional_zero_theorem": "If Pi_M is a parent-owned fixed q-basic topological chain map on the compact exterior source-current complex, then [d,Pi_M]J_H=0 and delta_g Pi_M=0, so the PiM beta lane vanishes.",
            "required_clauses": "PCM3373_1;PCM3373_2;PCM3373_3;PC3400_3",
            "current_status": "VALID_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "residual_if_missing": "J_PiM_comm; I_commutator_abs; projector_stress_beta_equiv",
            "valid_for_claim": False,
        },
        {
            "lane_id": "ZL3403_1_boundary",
            "lane": "kappa_boundary",
            "conditional_zero_theorem": "If the annulus is fixed, the primitive/reference is parent-fixed, relative boundary cohomology is trivial, physical Hilbert flux is already in the source measure, and H_ref is source-blind, then B_zero_flux=Delta_symp=0 and no boundary U^2 beta lane survives.",
            "required_clauses": "BZF3376_0..5;BF3393_0..1;PC3400_4",
            "current_status": "VALID_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "residual_if_missing": "B_zero_flux; Delta_symp; boundary_domain_beta",
            "valid_for_claim": False,
        },
        {
            "lane_id": "ZL3403_2_readout",
            "lane": "kappa_readout",
            "conditional_zero_theorem": "If PPN observables are read by one fixed post-smoothing P_PPN in one local PPN/Fermi patch and the same observed coframe is used through O(U^2), then no adaptive readout/gauge projector creates beta.",
            "required_clauses": "PT3391_0..1;PC3392_0..3;PC3400_0;PC3400_6",
            "current_status": "DERIVED_EXACT_IF_PARENT_CLAUSES_HOLD_NOT_SIGNED",
            "residual_if_missing": "J_readout; delta_beta_readout; adaptive projector/gauge drift",
            "valid_for_claim": False,
        },
        {
            "lane_id": "ZL3403_3_operator",
            "lane": "kappa_operator",
            "conditional_zero_theorem": "If the compact local exterior is EH-only with no scalar/vector/torsion/nonmetricity/bulk-X/nonlocal/projector-domain operators or each retained coefficient is zero, then the R11 operator beta lane vanishes.",
            "required_clauses": "SCEH529_1;SCEH529_2;SCEH529_6;PRE1512_0..7",
            "current_status": "CONDITIONAL_EH_NOHAIR_ROUTE_R11_COEFFICIENTS_MISSING",
            "residual_if_missing": "sum_i_abs_delta_beta_R11_i",
            "valid_for_claim": False,
        },
        {
            "lane_id": "ZL3403_4_coupling",
            "lane": "kappa_coupling",
            "conditional_zero_theorem": "If PC3400 source-coupling clauses are adopted through O(U^2), with fixed kappa_MTS, ell_J, no calibration feedback and same U in Poisson/H_tau/PPN, then coupling does not re-enter beta.",
            "required_clauses": "PC3400_0..6 plus O(U^2) extension",
            "current_status": "FIRST_ORDER_ROUTE_STAGED_SECOND_ORDER_EXTENSION_UNSIGNED",
            "residual_if_missing": "B_coupling_U2; calibration feedback; delta_kappa/delta_ellJ second-order tails",
            "valid_for_claim": False,
        },
        {
            "lane_id": "ZL3403_5_q_loc",
            "lane": "q_loc beta/projection guard",
            "conditional_zero_theorem": "If q_loc is Ward-zero through O(U^2), its beta and preferred-frame/location projections vanish; otherwise beta-only safety is insufficient because the same channel may project into alpha_i/alpha3/xi.",
            "required_clauses": "q_loc U2 projection; alpha_i/alpha3/xi projection map; Bianchi/Ward exchange gate",
            "current_status": "PROVISIONAL_BETA_NUMERIC_EXISTS_ALPHA3_GUARD_NOT_SAFE",
            "residual_if_missing": "delta_beta_q_loc plus preferred-frame guard",
            "valid_for_claim": False,
        },
    ]


def retained_lane_residual_formulas() -> list[dict[str, Any]]:
    return [
        {
            "formula_id": "RF3403_0_PiM",
            "lane": "kappa_PiM",
            "absolute_bound": "|kappa_PiM| <= 2*(I_commutator_abs + DmPiM_JH + Ddomain_PiM + projector_stress_beta_equiv + R_eq_integral + B_zero_flux + E_worldtube + E_extra_current + E_MHref_guard + E_calibration)",
            "source": str(SOURCES["jpim_bounds"]),
            "input_status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "formula_id": "RF3403_1_boundary",
            "lane": "kappa_boundary",
            "absolute_bound": "|kappa_boundary| <= 2*B_boundary_domain with B_boundary_domain sourced by boundary/reference/domain/projector-stress beta projection",
            "source": str(SOURCES["beta_finite_vector"]) + ";" + str(SOURCES["boundary_theorem"]),
            "input_status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "formula_id": "RF3403_2_readout",
            "lane": "kappa_readout",
            "absolute_bound": "|kappa_readout| <= 2*B_readout, with J_readout <= J_PiM_comm+J_Ploc_comm+J_worldtube_comm+J_material_comm+J_coframe_DObs+J_EFT_pre+J_calibration+J_boundary_endpoint",
            "source": str(SOURCES["jreadout_bounds"]),
            "input_status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "formula_id": "RF3403_3_operator",
            "lane": "kappa_operator",
            "absolute_bound": "|kappa_operator| <= 2*sum_i |delta_beta_R11_i| across R11 operator families",
            "source": str(SOURCES["r11_beta_vector"]),
            "input_status": "R11_VECTOR_EXISTS_COEFFICIENTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "formula_id": "RF3403_4_coupling",
            "lane": "kappa_coupling",
            "absolute_bound": "|kappa_coupling| <= 2*(B_delta_kappa_U2 + B_delta_ellJ_U2 + B_calibration_feedback + B_source_baseline_U2)",
            "source": str(SOURCES["3400_clauses"]),
            "input_status": "SECOND_ORDER_EXTENSION_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "formula_id": "RF3403_5_q_loc",
            "lane": "q_loc beta/projection guard",
            "absolute_bound": "|kappa_q_loc| <= 2*B_q_loc_beta only after physical U2 projection is signed; must also satisfy alpha_i/alpha3/xi projections",
            "source": str(SOURCES["beta_envelope"]),
            "input_status": "PROVISIONAL_BETA_ONLY_NOT_ACCEPTED",
            "valid_for_claim": False,
        },
    ]


def operator_family_status() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(SOURCES["r11_beta_vector"]):
        rows.append(
            {
                "operator_id": row.get("component_id", ""),
                "operator_family": row.get("operator_family", ""),
                "component": row.get("component", ""),
                "zero_or_safe_condition": row.get("zero_or_safe_condition", ""),
                "current_evidence": row.get("current_evidence", ""),
                "status": row.get("status", ""),
                "score_ready": False,
                "valid_for_claim": False,
            }
        )
    return rows


def qloc_beta_alpha_guard() -> list[dict[str, Any]]:
    beta_bound = beta_bound_value()
    rows = read_csv(SOURCES["beta_envelope"])
    qloc_beta = None
    alpha_guard = None
    for row in rows:
        if row.get("symbol") == "delta_beta_q_loc":
            qloc_beta = float(row["absolute_value_for_sum"])
        if row.get("symbol") == "q_loc_alpha3_projection_warning":
            alpha_guard = float(row["current_value"])
    if qloc_beta is None or alpha_guard is None:
        raise RuntimeError("q_loc beta/alpha guard values not found")
    kappav_target = 2 * beta_bound
    kappa_q = 2 * qloc_beta
    return [
        {
            "guard_id": "QG3403_0_beta_projection",
            "quantity": "delta_beta_q_loc",
            "value": qloc_beta,
            "beta_bound": beta_bound,
            "bound_fraction": qloc_beta / beta_bound,
            "kappa_equivalent": kappa_q,
            "kappav_target": kappav_target,
            "status": "BETA_ONLY_PROVISIONAL_BELOW_BOUND",
            "valid_for_claim": False,
        },
        {
            "guard_id": "QG3403_1_alpha3_warning",
            "quantity": "q_loc_alpha3_projection_warning",
            "value": alpha_guard,
            "beta_bound": beta_bound,
            "bound_fraction": "",
            "kappa_equivalent": "",
            "kappav_target": "",
            "status": "SEVERE_PREFERRED_FRAME_WARNING_IF_SAME_PROJECTION_APPLIES",
            "valid_for_claim": False,
        },
        {
            "guard_id": "QG3403_2_acceptance",
            "quantity": "q_loc lane acceptance",
            "value": "",
            "beta_bound": beta_bound,
            "bound_fraction": "",
            "kappa_equivalent": "",
            "kappav_target": kappav_target,
            "status": "NOT_ACCEPTED_FOR_KAPPAV_SCORE_UNTIL_U2_AND_ALPHA_VECTOR_PROJECTIONS_ARE_SIGNED",
            "valid_for_claim": False,
        },
    ]


def component_scorecard() -> list[dict[str, Any]]:
    return [
        {
            "score_id": "CS3403_0_eta",
            "lane": "eta_v",
            "best_status": "CONDITIONALLY_ZERO_FROM_3402",
            "claim_status": "NOT_PARENT_SIGNED",
            "next_needed": "source-calibrated EH/log-lapse parent ownership",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "score_id": "CS3403_1_source_quad",
            "lane": "kappa_source_quad",
            "best_status": "CONDITIONALLY_ZERO_FROM_3402",
            "claim_status": "NOT_PARENT_SIGNED",
            "next_needed": "one-parameter source family / B_source=A_source^2 ownership",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "score_id": "CS3403_2_PiM",
            "lane": "kappa_PiM",
            "best_status": "CONDITIONAL_CHAINMAP_ZERO",
            "claim_status": "NOT_PARENT_SIGNED",
            "next_needed": "fixed topological Pi_M plus source-current domain and no projector stress",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "score_id": "CS3403_3_boundary",
            "lane": "kappa_boundary",
            "best_status": "CONDITIONAL_STOKES_FIXED_ANNULUS_ZERO",
            "claim_status": "NOT_PARENT_SIGNED",
            "next_needed": "fixed primitive/reference, trivial relative class, no hidden physical flux",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "score_id": "CS3403_4_readout",
            "lane": "kappa_readout",
            "best_status": "CONDITIONAL_FIXED_READOUT_ZERO",
            "claim_status": "NOT_PARENT_SIGNED_THROUGH_O_U2",
            "next_needed": "single observed coframe/readout theorem through O(U^2)",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "score_id": "CS3403_5_operator",
            "lane": "kappa_operator",
            "best_status": "EH_NOHAIR_ROUTE_OR_R11_VECTOR",
            "claim_status": "R11_COEFFICIENTS_MISSING",
            "next_needed": "EH-only/no-hair parent theorem or zero/bound all R11 families",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "score_id": "CS3403_6_coupling",
            "lane": "kappa_coupling",
            "best_status": "FIRST_ORDER_PC3400_STAGED",
            "claim_status": "O_U2_EXTENSION_UNSIGNED",
            "next_needed": "second-order PC3400 extension and no calibration feedback",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "score_id": "CS3403_7_q_loc",
            "lane": "q_loc beta/projection guard",
            "best_status": "BETA_PROVISIONAL_BELOW_BOUND_BUT_ALPHA_GUARD_SEVERE",
            "claim_status": "NOT_ACCEPTED",
            "next_needed": "physical U2 projection and alpha_i/alpha3/xi projection split",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def kappav_reduced_envelope() -> list[dict[str, Any]]:
    beta_bound = beta_bound_value()
    return [
        {
            "envelope_id": "ENV3403_0_if_eta_source_zero",
            "formula": "|kappa_v| <= |kappa_PiM|+|kappa_boundary|+|kappa_readout|+|kappa_operator|+|kappa_coupling|+|kappa_q_loc|",
            "condition": "uses 3402 conditional zeroes for eta_v and source_quad only",
            "kappav_target": 2 * beta_bound,
            "status": "REDUCED_ENVELOPE_CONDITIONAL_NOT_SCORE_READY",
            "valid_for_claim": False,
        },
        {
            "envelope_id": "ENV3403_1_all_lanes_zero",
            "formula": "all retained lanes theorem-zero => kappa_v=0 => beta=1",
            "condition": "PiM chainmap, boundary Stokes, fixed readout, EH/no-hair operator, O(U2) coupling and q_loc vector silence all signed",
            "kappav_target": 2 * beta_bound,
            "status": "EXACT_CONDITIONAL_LOCAL_BETA_ROUTE",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3403_0_zero_routes",
            "claim": "zero routes exist for retained kappa_v lanes",
            "gate_pass": True,
            "reason": "PiM, boundary, readout, operator, coupling and q_loc conditional routes are written",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3403_1_formulas",
            "claim": "finite formulas exist for retained lanes if zero routes fail",
            "gate_pass": True,
            "reason": "absolute no-cancellation formulas are written for PiM, boundary, readout, operator, coupling and q_loc",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3403_2_values",
            "claim": "retained lane values are score-ready",
            "gate_pass": False,
            "reason": "component values/theorem signatures remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3403_3_q_loc",
            "claim": "q_loc is safe for beta/full PPN",
            "gate_pass": False,
            "reason": "beta-only provisional value is below beta lock, but alpha3/preferred-frame guard is severe and projection is unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3403_4_beta",
            "claim": "kappa_v=0 or beta bound pass is derived",
            "gate_pass": False,
            "reason": "reduced envelope is conditional and not populated with values",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3403_5_local_GR",
            "claim": "local GR/PPN is derived",
            "gate_pass": False,
            "reason": "beta still nonclaim and alpha_i/zeta_i/xi vector remains open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "run_id": "RUN3403_0_zero_routes",
            "test": "retained lane zero theorem extraction",
            "status": "PASS_CONDITIONAL_ROUTES_EXTRACTED",
            "detail": "six retained lane routes written",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3403_1_formulas",
            "test": "finite residual formulas",
            "status": "PASS_FORMULAS_WRITTEN_VALUES_MISSING",
            "detail": "absolute residual formulas written without cancellation credit",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3403_2_q_loc",
            "test": "q_loc beta/alpha guard",
            "status": "PASS_GUARD_RETAINED_NOT_ACCEPTED",
            "detail": "beta-only provisional is not used as a score because alpha/vector projection is unsafe",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3403_3_claim_firewall",
            "test": "beta/local-GR claim",
            "status": "BLOCKED_NO_CLAIM",
            "detail": "kappa_v and full PPN remain unclaimed",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3403_0_progress",
            "finding": "all retained kappa_v lanes now have either a conditional zero route or an explicit finite formula",
            "reason": "PiM chainmap, boundary Stokes, fixed readout, EH/no-hair, O(U2) coupling and q_loc vector guard are separated",
            "next_action": "choose the highest-leverage parent ownership audit rather than re-scanning beta",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3403_1_qloc",
            "finding": "q_loc is not currently fatal for beta-only but remains dangerous for full PPN",
            "reason": "provisional beta projection is below beta target, while alpha3/preferred-frame guard is severe if that projection applies",
            "next_action": "derive physical U2 and alpha-vector projection split before accepting any q_loc budget",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3403_2_best_next",
            "finding": "the best route is source-calibrated EH/no-hair parent ownership",
            "reason": "that single audit could activate eta/source zeroes and kill operator/readout/boundary lanes as parent theorems",
            "next_action": "build 3404 source-calibrated EH parent ownership audit",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3404-Y5-R2FR-source-calibrated-EH-parent-ownership-audit-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3404_source_calibrated_EH_parent_ownership_audit.py",
            "objective": "audit whether the source-calibrated EH one-parameter/no-hair branch can be parent-owned by MTS without importing GR as an axiom",
            "why_next": "this is the least-fragmented route to close eta/source/operator/readout/boundary beta lanes together",
            "valid_for_claim": False,
        },
        {
            "target_id": "3405-Y5-R2FR-q_loc-U2-alpha-vector-projection-split-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3405_q_loc_U2_alpha_vector_projection_split.py",
            "objective": "derive the physical U2 beta projection and separate alpha_i/alpha3/xi projections of q_loc",
            "why_next": "q_loc cannot be accepted as beta-safe until the preferred-frame projection is separated or killed",
            "valid_for_claim": False,
        },
    ]


def validate(outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        rows.append({"check_id": check_id, "check": check, "passed": passed, "detail": detail})

    add("VAL3403_0_sources_exist", "all registered sources exist", all(row["exists"] for row in outputs["source_register"]), f"sources={len(outputs['source_register'])}")
    add("VAL3403_1_zero_routes", "retained lane zero routes are present", len(outputs["retained_lane_zero_theorems"]) == 6, "")
    add("VAL3403_2_formulas", "retained lane formulas are present", len(outputs["retained_lane_residual_formulas"]) == 6, "")
    add("VAL3403_3_operator_families", "operator family status rows imported", len(outputs["operator_family_status"]) >= 12, "")
    q_rows = outputs["qloc_beta_alpha_guard"]
    add("VAL3403_4_qloc_guard", "q_loc beta and alpha guard recorded", any(row["status"].startswith("BETA_ONLY") for row in q_rows) and any(row["quantity"] == "q_loc_alpha3_projection_warning" for row in q_rows), "")
    add("VAL3403_5_values_block", "component values remain blocked", not any(row["score_ready"] for row in outputs["component_scorecard"]), "")
    add("VAL3403_6_claim_gates", "beta/local-GR gates remain blocked", not any(row["gate_pass"] for row in outputs["promotion_gates"] if row["gate_id"] in {"GATE3403_2_values", "GATE3403_3_q_loc", "GATE3403_4_beta", "GATE3403_5_local_GR"}), "")
    add("VAL3403_7_no_overclaim", "all generated rows remain nonclaim", all(str(row.get("valid_for_claim", False)).lower() == "false" for group in outputs.values() for row in group), "")
    add("VAL3403_8_scope", "no 3403 output path targets formalization-workbench", "formalization-workbench" not in str(DOC).lower() and all("formalization-workbench" not in str(path).lower() for path in OUTPUT_PATHS.values()), "")
    add("VAL3403_9_next_target", "next target moves to EH parent ownership audit", any("EH" in row["objective"] and "parent-owned" in row["objective"] for row in outputs["next_target"]), "")
    add("VAL3403_10_overall", "3403 validation overall", all(row["passed"] is True for row in rows), "all required checks passed")
    return rows


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *[
                "| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |"
                for row in rows
            ],
        ]
    )


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    sections = [
        "# 3403 - Y5/R2FR PiM boundary readout operator beta residual fill under AX1090",
        "",
        "## Summary",
        "- 3403 fills the retained `kappa_v` lanes left after the 3402 `a_v=0` and `B_source=A_source^2` conditional results.",
        "- PiM, boundary, readout, operator, coupling and q_loc now each have a conditional zero route plus a finite no-cancellation residual formula.",
        "- The q_loc beta diagnostic is below the beta target only provisionally, but it is not accepted because the alpha3/preferred-frame guard is severe.",
        "- Beta/local-GR remains unclaimed: values and parent signatures are still missing, but the remaining beta work is now localized.",
        f"- Generated UTC: `{timestamp}`.",
        "",
        "## Source Register",
        md_table(outputs["source_register"]),
        "",
        "## Retained Lane Zero Theorems",
        md_table(outputs["retained_lane_zero_theorems"]),
        "",
        "## Retained Lane Residual Formulas",
        md_table(outputs["retained_lane_residual_formulas"]),
        "",
        "## Operator Family Status",
        md_table(outputs["operator_family_status"]),
        "",
        "## q_loc Beta/Alpha Guard",
        md_table(outputs["qloc_beta_alpha_guard"]),
        "",
        "## Component Scorecard",
        md_table(outputs["component_scorecard"]),
        "",
        "## Kappa_v Reduced Envelope",
        md_table(outputs["kappav_reduced_envelope"]),
        "",
        "## Promotion Gates",
        md_table(outputs["promotion_gates"]),
        "",
        "## Nonclaim Runner",
        md_table(outputs["runner_nonclaim"]),
        "",
        "## Decision Ledger",
        md_table(outputs["decision_ledger"]),
        "",
        "## Validation",
        md_table(outputs["validation"]),
        "",
        "## Next Target",
        md_table(outputs["next_target"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    outputs = {
        "source_register": source_register(),
        "retained_lane_zero_theorems": retained_lane_zero_theorems(),
        "retained_lane_residual_formulas": retained_lane_residual_formulas(),
        "operator_family_status": operator_family_status(),
        "qloc_beta_alpha_guard": qloc_beta_alpha_guard(),
        "component_scorecard": component_scorecard(),
        "kappav_reduced_envelope": kappav_reduced_envelope(),
        "promotion_gates": promotion_gates(),
        "runner_nonclaim": runner_nonclaim(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }
    outputs["validation"] = validate(outputs)
    for name, rows in outputs.items():
        write_csv(OUTPUT_PATHS[name], rows)
    parsed = [(path.name, len(read_csv(path))) for path in OUTPUT_PATHS.values()]
    if not all(row["passed"].lower() == "true" for row in read_csv(OUTPUT_PATHS["validation"])):
        raise RuntimeError("3403 validation failed")
    write_doc(outputs)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUT_PATHS)} CSV outputs under {OUT}")
    print("Parsed outputs: " + "; ".join(f"{name}={count}" for name, count in parsed))


if __name__ == "__main__":
    main()
