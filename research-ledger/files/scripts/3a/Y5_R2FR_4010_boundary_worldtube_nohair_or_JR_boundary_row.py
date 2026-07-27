from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4010"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4010-Y5-R2FR-boundary-worldtube-nohair-or-JR-boundary-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

ALPHA3_BOUND = 4e-20

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4010_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_4010_BOUNDARY_WORLDTUBE_NOHAIR_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_4010_BOUNDARY_WORLDTUBE_AUDIT.csv",
    "finite": SRC / "P8_Y5_R2FR_4010_JR_BOUNDARY_FINITE_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4010_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4010_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4010_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4010_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4010_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4010_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4010_VALIDATION.csv",
}

NEXT_DOC = "4011-Y5-R2FR-Hilbert-worldtube-source-owner-lock-or-support-flux-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4011_Hilbert_worldtube_source_owner_lock_or_support_flux_row.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4010_00_handoff", SRC / "P8_Y5_R2FR_4009_NEXT_TARGET.csv", "NEXT4009_0", "4009 handoff"),
        ("SRC4010_01_branch_gate", SRC / "P8_Y5_R2FR_4009_SINGLE_BRANCH_GATE.csv", "SBG4009_4_boundary_worldtube", "boundary/worldtube gate"),
        ("SRC4010_02_geom_master", SRC / "P8_Y5_R2FR_4009_GEOM_JR_ROWS.csv", "GJR4009_0_master", "J_R_geom context"),
        ("SRC4010_03_next_decision", SRC / "P8_Y5_R2FR_4009_DECISION_GATE.csv", "DEC4009_3_next", "4009 next decision"),
        ("SRC4010_04_boundary_packet", SRC / "P8_Y5_R2FR_4006_PARENT_INSERTION_PACKET.csv", "PIP4006_4_boundary", "4006 boundary nohair packet"),
        ("SRC4010_05_no_deriv_packet", SRC / "P8_Y5_R2FR_4006_PARENT_INSERTION_PACKET.csv", "PIP4006_2_no_derivative_language", "no derivative grammar"),
        ("SRC4010_06_delta_boundary", SRC / "P8_Y5_R2FR_4006_VARIATION_CHAIN.csv", "VAR4006_3_delta_boundary", "boundary fork"),
        ("SRC4010_07_symplectic", SRC / "P8_Y5_R2FR_4006_VARIATION_CHAIN.csv", "VAR4006_4_symplectic_potential", "symplectic boundary guard"),
        ("SRC4010_08_BR_row", SRC / "P8_Y5_R2FR_4006_FINITE_COEFFICIENT_ACQUISITION_ROWS.csv", "FR4006_2_B_R", "finite boundary row"),
        ("SRC4010_09_prem_worldtube", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv", "PRE2611_5_worldtube_support", "worldtube support premise"),
        ("SRC4010_10_prem_boundary", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv", "PRE2611_6_boundary", "matter boundary premise"),
        ("SRC4010_11_chain_worldtube", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_CHAIN_RULE_DECOMPOSITION.csv", "CR2611_4_worldtube", "worldtube chain term"),
        ("SRC4010_12_chain_boundary", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_CHAIN_RULE_DECOMPOSITION.csv", "CR2611_5_boundary", "boundary chain term"),
        ("SRC4010_13_status_worldtube", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_SOURCE_ZERO_STATUS.csv", "SZ2611_3_worldtube", "worldtube status"),
        ("SRC4010_14_audit_4007", SRC / "P8_Y5_R2FR_4007_MATTER_READOUT_DESCENT_AUDIT.csv", "AUD4007_6_boundary_worldtube", "4007 boundary audit"),
        ("SRC4010_15_fsig_boundary", SRC / "P8_Y5_FIELD_QUOTIENT_2570_FIELD_SIGNATURE_ATTEMPT.csv", "FSIG2570_6_boundary_reference", "boundary reference signature"),
        ("SRC4010_16_dq_boundary", SRC / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv", "DQ2570_7_boundary", "boundary Dq ledger"),
        ("SRC4010_17_dq_projector", SRC / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv", "DQ2570_5_projector", "projector/readout boundary"),
        ("SRC4010_18_alpha3_target", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T0_target_projection", "boundary alpha3 target"),
        ("SRC4010_19_scalar_boundary", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T1_scalar_boundary_action", "scalar boundary lemma"),
        ("SRC4010_20_no_flux", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T2_no_normal_flux_from_tangential_trace", "no normal flux lemma"),
        ("SRC4010_21_parent_owner", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T5_parent_owner_audit", "parent ownership failure"),
        ("SRC4010_22_numeric_fallback", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T6_numeric_fallback", "numeric fallback"),
        ("SRC4010_23_boundary_decision", SRC / "P8_BOUNDARY_ALPHA3_DECISION.csv", "D1_parent_ownership", "boundary parent ownership decision"),
        ("SRC4010_24_boundary_closure", SRC / "P8_BOUNDARY_ALPHA3_CLOSURE_STATUS.csv", "boundary_alpha3", "boundary closure status"),
        ("SRC4010_25_alpha3_gate", SRC / "P8_ALPHA3_THEOREM_ZERO_GATE.csv", "TG_boundary_zero", "alpha3 theorem gate"),
        ("SRC4010_26_alpha3_template", SRC / "P8_ALPHA3_NUMERIC_PRODUCT_INPUT_TEMPLATE.csv", "A3_BOUNDARY_NUMERIC_OR_ZERO", "alpha3 numeric template"),
        ("SRC4010_27_alpha3_total_guard", SRC / "P8_ALPHA3_TOTAL_GUARD.csv", "G_boundary_channel", "boundary alpha3 total guard"),
        ("SRC4010_28_worldtube_residual", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_6_R_W", "worldtube residual"),
        ("SRC4010_29_ward_boundary", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_2_R_Ward", "Ward boundary tails"),
        ("SRC4010_30_domain_support", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_4_C_domain", "domain/worldtube support"),
        ("SRC4010_31_ref_boundary", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_5_C_ref", "reference boundary"),
        ("SRC4010_32_sigma_descent", SRC / "P8_EM_quotient_source_coordinate_descent_certificate.csv", "QSC3516_2_sigma_descent", "sigma/worldtube descent"),
        ("SRC4010_33_wta_support", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv", "WTA2611_0_support_selector", "worldtube support selector"),
        ("SRC4010_34_wta_verdict", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv", "WTA2611_3_matter_worldtube_verdict", "worldtube verdict"),
        ("SRC4010_35_nonhilbert", SRC / "P8_EM_current_source_Ward_alpha_source_residual.csv", "CSR3508_6_nonHilbert_bypass", "non-Hilbert boundary bypass"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "BWT4010_0_boundary_decomposition",
            "claim_piece": "reciprocal boundary/worldtube source",
            "mathematical_form": "J_R_boundary := Pi_R^n + delta_R B_R + delta_R W_source + delta_R Pi_loc + nonHilbert_boundary_tail",
            "derived_result": "4010 splits the last live J_R term into boundary momentum, boundary action, worldtube/support, projector/local projection and non-Hilbert tails",
            "status": "EXACT_DECOMPOSITION_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "BWT4010_1_no_derivative_boundary",
            "claim_piece": "Pi_R^n zero",
            "mathematical_form": "If the parent boundary grammar contains no D_n R_AB and no R_AB boundary improvement, then Pi_R^n=partial L_boundary/partial(D_n R_AB)=0",
            "derived_result": "the no-derivative coframe-cell grammar kills canonical reciprocal boundary momentum conditionally",
            "status": "EXACT_IF_GRAMMAR_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "BWT4010_2_proper_boundary_action",
            "claim_piece": "delta_R B_R zero/proper",
            "mathematical_form": "If B_R is absent, topological/class-only, exact/proper on the fixed variational class, or scalar stationary with no normal momentum flux, then delta_R B_R has zero local projection",
            "derived_result": "boundary action can be silent only when its variational class is parent-owned before readout",
            "status": "CONDITIONAL_LEMMA_PARENT_OWNER_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "BWT4010_3_worldtube_support",
            "claim_piece": "delta_R W_source zero",
            "mathematical_form": "If W_source=closure(supp J_H[tau]) on the same parent Hilbert current/tau/coframe branch, then support variation is inherited from the already-reduced source current instead of fitted after readout",
            "derived_result": "worldtube flux is zero only after Hilbert source support is parent-owned",
            "status": "CONDITIONAL_WORLD_TUBE_THEOREM_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "BWT4010_4_alpha3_scalar_boundary",
            "claim_piece": "boundary preferred-momentum flux",
            "mathematical_form": "scalar stationary boundary stress tau_AB=tau gamma_AB gives n_mu P_loc_nu tau^{mu nu}=0, hence W_boundary_alpha3=0 under scalar/no-marker/no-normal-exchange premises",
            "derived_result": "alpha3 boundary zero lemma exists, but parent ownership and numeric product are missing",
            "status": "CONDITIONAL_ALPHA3_ZERO_LEMMA_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "BWT4010_5_full_zero_condition",
            "claim_piece": "J_R_boundary zero",
            "mathematical_form": "J_R_boundary=0 if Pi_R^n=0, delta_R B_R=0/proper, delta_R W_source=0, [D_R,Pi_loc] boundary tail=0, and nonHilbert_boundary_tail=0 in one branch",
            "derived_result": "full boundary/worldtube silence is a real derivable target, not a closure axiom; current corpus does not yet sign it",
            "status": "EXACT_CONDITIONAL_FULL_GATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "BWA4010_0_no_derivative_grammar",
            "clause": "no D_n R_AB and no R_AB boundary improvement",
            "current_status": "PACKET_EXISTS_NOT_ADOPTED",
            "risk_if_open": "Pi_R^n gives boundary charge/current hair",
            "next_action": "adopt no-derivative boundary grammar in parent branch or fill Pi_R^n",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BWA4010_1_boundary_class",
            "clause": "boundary action is absent, class-only/topological, exact/proper, or scalar stationary no-flux",
            "current_status": "CONDITIONAL_LEMMA_NOT_PARENT_OWNED",
            "risk_if_open": "B_R can carry compact local reciprocal hair",
            "next_action": "derive parent boundary action owner or keep B_R finite row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BWA4010_2_worldtube_support",
            "clause": "W_source=closure(supp J_H[tau]) before readout",
            "current_status": "WORLDTUBE_DESCENT_NOT_PARENT_SIGNED",
            "risk_if_open": "support/domain selector drift changes source mass and local projection",
            "next_action": "derive Hilbert worldtube source owner lock",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BWA4010_3_projector_local_projection",
            "clause": "Pi_loc/Pi_M/source projection is fixed or commutes with the parent current before readout",
            "current_status": "PROJECTOR_OBSTRUCTION_RETAINED",
            "risk_if_open": "boundary noflux can fail after projection/readout even when Ward identity holds",
            "next_action": "tie to Pi_M/H_tau/source support lock",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BWA4010_4_nonHilbert_tail",
            "clause": "all non-Hilbert boundary currents are exact improvements with zero exterior flux or explicit residuals",
            "current_status": "PARALLEL_GATE_OPEN",
            "risk_if_open": "non-Hilbert source bypass enters PPN/source normalization",
            "next_action": "retain nonHilbert_boundary_tail unless owner theorem closes",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BWA4010_5_alpha3_numeric",
            "clause": "boundary alpha3 product theorem-zero or |W_boundary_alpha3 epsilon_boundary_flux| <= 4e-20",
            "current_status": "TEMPLATE_UNFILLED_NOT_SCOREABLE",
            "risk_if_open": "PPN alpha3/local momentum-conservation row blocks local-GR promotion",
            "next_action": "supply parent no-flux certificate or numeric product",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BWA4010_6_same_branch",
            "clause": "cell-lock, 4008 matter constructor, 4009 reduced coframe and boundary/worldtube clauses close together",
            "current_status": "MISSING_SINGLE_BRANCH_ADOPTION",
            "risk_if_open": "stitched conditional lemmas do not prove local GR",
            "next_action": "do not promote; continue with worldtube source owner lock",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def finite_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "JRBND4010_0_master",
            "coefficient": "J_R_boundary",
            "formula": "|J_R_boundary| <= |Pi_R^n| + |delta_R B_R| + |delta_R W_source| + |[D_R,Pi_loc]B| + |nonHilbert_boundary_tail|",
            "value": "ZERO_IF_FULL_BOUNDARY_WORLDTUBE_GATE_SIGNED_ELSE_COMPONENT_ENVELOPE",
            "units": "same_as_J_R_or_normalized_dimensionless_after_projection",
            "observable_link": "local_GR;Newton_G;PPN_alpha3;R10;WEP;orbits",
            "source_status": "COMPONENT_ENVELOPE_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JRBND4010_1_Pi_R",
            "coefficient": "Pi_R^n",
            "formula": "partial L_boundary / partial(D_n R_AB)",
            "value": "ZERO_IF_NO_DERIVATIVE_BOUNDARY_GRAMMAR_ELSE_MISSING_NUMERIC_FLUX",
            "units": "boundary_momentum_per_RAB",
            "observable_link": "R10;PPN;clock;boundary_hair",
            "source_status": "DERIVED_ZERO_CONDITIONAL_OR_MISSING_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JRBND4010_2_B_R",
            "coefficient": "delta_R B_R",
            "formula": "R_AB derivative of any reciprocal boundary/corner/reference action",
            "value": "MISSING_PARENT_PROPER_BOUNDARY_THEOREM_OR_NUMERIC_ROW",
            "units": "boundary_action_derivative_per_RAB",
            "observable_link": "local_GR;R10;source_normalization",
            "source_status": "MISSING_PARENT_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JRBND4010_3_worldtube",
            "coefficient": "delta_R W_source",
            "formula": "D_R ln int_W rho_H dV_H minus D_R ln int_closure(supp J_H[tau]) rho_H dV_H",
            "value": "MISSING_HILBERT_WORLDTUBE_SOURCE_OWNER_LOCK",
            "units": "per_RAB_or_dimensionless_support_drift",
            "observable_link": "Newton_source;R10_source_support;WEP;PPN_profile",
            "source_status": "MISSING_PARENT_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JRBND4010_4_alpha3_boundary",
            "coefficient": "W_boundary_alpha3_epsilon_boundary_flux",
            "formula": "alpha3_boundary = W_boundary_alpha3 * epsilon_boundary_flux",
            "value": "MISSING_NUMERIC_PRODUCT_OR_PARENT_NOFLUX_CERTIFICATE",
            "units": "dimensionless",
            "observable_link": "PPN_alpha3;momentum_conservation",
            "source_status": "TARGET_BOUND_4E-20_NOT_SCOREABLE",
            "bound": ALPHA3_BOUND,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JRBND4010_5_projection",
            "coefficient": "boundary_arena_projection",
            "formula": "map any surviving boundary/worldtube coefficient to PPN/R10/WEP/clock/orbital kernels",
            "value": "MISSING_ARENA_PROJECTION_IF_ANY_COMPONENT_SURVIVES",
            "units": "arena_dependent",
            "observable_link": "all_local_tests",
            "source_status": "MISSING_IF_NOT_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"case_id": "CASE4010_0_full_gate_signed", "no_derivative": True, "proper_boundary": True, "worldtube_owned": True, "projection_fixed": True, "nonhilbert_zero": True, "numeric_pack": False, "timestamp_utc": timestamp},
        {"case_id": "CASE4010_1_boundary_action_open", "no_derivative": True, "proper_boundary": False, "worldtube_owned": True, "projection_fixed": True, "nonhilbert_zero": True, "numeric_pack": False, "timestamp_utc": timestamp},
        {"case_id": "CASE4010_2_worldtube_open", "no_derivative": True, "proper_boundary": True, "worldtube_owned": False, "projection_fixed": True, "nonhilbert_zero": True, "numeric_pack": False, "timestamp_utc": timestamp},
        {"case_id": "CASE4010_3_projection_open", "no_derivative": True, "proper_boundary": True, "worldtube_owned": True, "projection_fixed": False, "nonhilbert_zero": True, "numeric_pack": False, "timestamp_utc": timestamp},
        {"case_id": "CASE4010_4_nonhilbert_open", "no_derivative": True, "proper_boundary": True, "worldtube_owned": True, "projection_fixed": True, "nonhilbert_zero": False, "numeric_pack": False, "timestamp_utc": timestamp},
        {"case_id": "CASE4010_5_derivative_boundary_open", "no_derivative": False, "proper_boundary": True, "worldtube_owned": True, "projection_fixed": True, "nonhilbert_zero": True, "numeric_pack": False, "timestamp_utc": timestamp},
        {"case_id": "CASE4010_6_numeric_pack", "no_derivative": False, "proper_boundary": False, "worldtube_owned": False, "projection_fixed": False, "nonhilbert_zero": False, "numeric_pack": True, "timestamp_utc": timestamp},
    ]


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        no_derivative = bool(case["no_derivative"])
        proper_boundary = bool(case["proper_boundary"])
        worldtube_owned = bool(case["worldtube_owned"])
        projection_fixed = bool(case["projection_fixed"])
        nonhilbert_zero = bool(case["nonhilbert_zero"])
        numeric_pack = bool(case["numeric_pack"])

        if numeric_pack:
            boundary_status = "FINITE_BOUNDARY_PACK_NONCLAIM"
            jr_status = "J_R_BOUNDARY_COMPONENT_ENVELOPE"
            next_action = "fill numeric source paths, units and arena projections"
        elif not no_derivative:
            boundary_status = "DERIVATIVE_BOUNDARY_MOMENTUM_OPEN"
            jr_status = "PI_R_N_LIVE"
            next_action = "adopt no-derivative grammar or fill Pi_R^n"
        elif not proper_boundary:
            boundary_status = "BOUNDARY_ACTION_OPEN"
            jr_status = "DELTA_R_B_R_LIVE"
            next_action = "derive proper/scalar/topological boundary owner or fill B_R"
        elif not worldtube_owned:
            boundary_status = "WORLDTUBE_SUPPORT_OPEN"
            jr_status = "DELTA_R_W_SOURCE_LIVE"
            next_action = "derive Hilbert worldtube source owner lock"
        elif not projection_fixed:
            boundary_status = "PROJECTION_BOUNDARY_OPEN"
            jr_status = "PILOC_COMMUTATOR_TAIL_LIVE"
            next_action = "prove projector/source support commutation or retain C_domain"
        elif not nonhilbert_zero:
            boundary_status = "NONHILBERT_BOUNDARY_OPEN"
            jr_status = "NONHILBERT_BOUNDARY_TAIL_LIVE"
            next_action = "prove exact improvement zero-flux or retain nonHilbert row"
        else:
            boundary_status = "CONDITIONAL_BOUNDARY_WORLDTUBE_ZERO"
            jr_status = "J_R_BOUNDARY_ZERO_IF_SINGLE_BRANCH_SIGNED"
            next_action = "assemble with 4006/4008/4009 branch and move to source-current normalization"

        rows.append(
            {
                "case_id": case["case_id"],
                "boundary_status": boundary_status,
                "J_R_boundary_status": jr_status,
                "claim_allowed": False,
                "valid_for_claim": False,
                "next_action": next_action,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4010_0_conditional_zero",
            "decision": "boundary/worldtube nohair has an exact conditional route",
            "reason": "no-derivative grammar, proper/scalar boundary, Hilbert-owned worldtube support, fixed projection and exact-improvement currents kill every component",
            "effect": "J_R_boundary is no longer vague; it is a five-part zero gate",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4010_1_no_promotion",
            "decision": "do not promote boundary/local-GR claim",
            "reason": "parent ownership of boundary action and Hilbert worldtube support is missing; alpha3 product is unfilled",
            "effect": "boundary remains nonclaim even though the route is sharper",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4010_2_finite_policy",
            "decision": "if nohair fails, retain J_R_boundary component envelope",
            "reason": "Pi_R^n, B_R, W_source drift, projection tails and non-Hilbert bypass each have observable locks",
            "effect": "no hidden cancellation or broad closure language is allowed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4010_3_next",
            "decision": "next target is Hilbert worldtube source-owner lock",
            "reason": "worldtube support ownership is the central dependency for boundary flux, source normalization, R10 and Newton source mass",
            "effect": "4011 should derive W_source=closure(supp J_H[tau]) or create support-flux rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CLAIM4010_0_JR_boundary_zero",
            "claim": "J_R_boundary=0",
            "allowed": False,
            "blocker": "boundary action ownership, Hilbert worldtube support, projector/local projection and non-Hilbert zero-flux are not parent-signed in one branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4010_1_alpha3_boundary",
            "claim": "boundary alpha3 passes",
            "allowed": False,
            "blocker": "scalar no-flux lemma is conditional and W_boundary_alpha3 epsilon_boundary_flux numeric product is missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4010_2_local_GR",
            "claim": "local GR/Newton recovered",
            "allowed": False,
            "blocker": "source-current/worldtube owner, source normalization, Pi_M/H_tau and PPN second-order gates remain",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4010_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive W_source=closure(supp J_H[tau]) and parent-owned Hilbert source measure on the reduced cell-lock branch, or create explicit support-flux/source-shape rows",
            "success_condition": "worldtube support, sigma^a shape coordinates, Pi_M source support and linked surfaces descend from the same Hilbert current before readout; otherwise support drift rows get units, source paths and valid_for_claim=false",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "boundary/worldtube nohair split into exact conditional zero gate and finite J_R_boundary component envelope; no local-GR claim promoted",
            "current_best_next": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    lines = [
        "# 4010 - Boundary/Worldtube Nohair Or J_R Boundary Row",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "The boundary/worldtube obstruction is now decomposed instead of waved away:",
        "",
        "`J_R_boundary := Pi_R^n + delta_R B_R + delta_R W_source + delta_R Pi_loc + nonHilbert_boundary_tail`.",
        "",
        "The zero route is exact but conditional. `J_R_boundary=0` requires no derivative boundary momentum, proper/scalar/topological boundary action, parent-owned Hilbert worldtube support, fixed local projection, and zero-flux non-Hilbert improvements.",
        "",
        "## Boundary Lemma",
        "",
        "The scalar stationary boundary lemma is real: if the boundary stress is a pure tangential trace, then `n_mu P_loc_nu tau^{mu nu}=0`, so the preferred-momentum/alpha3 boundary channel vanishes.",
        "",
        "But the corpus does not yet parent-own those premises, and the numeric product `W_boundary_alpha3 epsilon_boundary_flux` is still missing.",
        "",
        "## Finite Row",
        "",
        "If the nohair theorem fails, the retained row is",
        "",
        "`|J_R_boundary| <= |Pi_R^n| + |delta_R B_R| + |delta_R W_source| + |[D_R,Pi_loc]B| + |nonHilbert_boundary_tail|`.",
        "",
        "No cancellation between components is credited.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: boundary=`{row['boundary_status']}`, J_R=`{row['J_R_boundary_status']}`, next=`{row['next_action']}`"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "This is a useful narrowing: the boundary problem is no longer a fog bank. It is a finite list of gates, and the hardest one is now the Hilbert worldtube source-owner lock.",
            "",
            "## Next Target",
            "",
            f"- `{NEXT_DOC}`",
            f"- `{NEXT_SCRIPT}`",
            "",
            "## Source Count",
            "",
            f"- source needles found: `{found}/{len(sources)}`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def append_spine(timestamp: str) -> None:
    marker = "## 4010 - Boundary/Worldtube Nohair Gate"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: `J_R_boundary` is decomposed as `Pi_R^n + delta_R B_R + delta_R W_source + delta_R Pi_loc + nonHilbert_boundary_tail`.
- Conditional zero: no derivative boundary momentum, proper/scalar/topological boundary action, Hilbert-owned worldtube support, fixed projection and zero-flux non-Hilbert improvements.
- Alpha3 note: scalar stationary boundary no-flux lemma is mathematically valid, but parent ownership and numeric `W_boundary_alpha3 epsilon_boundary_flux` are missing.
- No claim: local GR/Newton/PPN boundary pass is not promoted; finite component envelope remains.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4010 - Boundary/Worldtube Nohair Gate" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4010_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4010_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL4010_02_decomposition", any(row["theorem_id"] == "BWT4010_0_boundary_decomposition" for row in theorem), "boundary decomposition present")
    add("VAL4010_03_no_derivative", any(row["theorem_id"] == "BWT4010_1_no_derivative_boundary" for row in theorem), "no-derivative theorem present")
    add("VAL4010_04_boundary_action", any(row["theorem_id"] == "BWT4010_2_proper_boundary_action" for row in theorem), "proper boundary theorem present")
    add("VAL4010_05_worldtube", any(row["theorem_id"] == "BWT4010_3_worldtube_support" for row in theorem), "worldtube theorem present")
    add("VAL4010_06_alpha3", any(row["theorem_id"] == "BWT4010_4_alpha3_scalar_boundary" for row in theorem), "alpha3 scalar boundary lemma present")
    add("VAL4010_07_full_gate", any(row["theorem_id"] == "BWT4010_5_full_zero_condition" for row in theorem), "full zero gate present")
    add("VAL4010_08_audit_boundary", any(row["audit_id"] == "BWA4010_1_boundary_class" for row in audit), "boundary action audit present")
    add("VAL4010_09_audit_worldtube", any(row["audit_id"] == "BWA4010_2_worldtube_support" for row in audit), "worldtube audit present")
    add("VAL4010_10_audit_projection", any(row["audit_id"] == "BWA4010_3_projector_local_projection" for row in audit), "projection audit present")
    add("VAL4010_11_audit_alpha3", any(row["audit_id"] == "BWA4010_5_alpha3_numeric" for row in audit), "alpha3 numeric audit present")
    master = next(row for row in finite if row["row_id"] == "JRBND4010_0_master")
    alpha = next(row for row in finite if row["row_id"] == "JRBND4010_4_alpha3_boundary")
    add("VAL4010_12_master_bound", "Pi_R^n" in master["formula"] and "nonHilbert" in master["formula"], "master finite envelope present")
    add("VAL4010_13_Pi_row", any(row["row_id"] == "JRBND4010_1_Pi_R" for row in finite), "Pi_R row present")
    add("VAL4010_14_BR_row", any(row["row_id"] == "JRBND4010_2_B_R" for row in finite), "B_R row present")
    add("VAL4010_15_worldtube_row", any(row["row_id"] == "JRBND4010_3_worldtube" for row in finite), "worldtube row present")
    add("VAL4010_16_alpha3_bound", float(alpha["bound"]) == ALPHA3_BOUND and alpha["source_status"] == "TARGET_BOUND_4E-20_NOT_SCOREABLE", "alpha3 bound retained as nonclaim")
    add("VAL4010_17_projection_row", any(row["row_id"] == "JRBND4010_5_projection" for row in finite), "projection guard row present")
    full = next(row for row in results if row["case_id"] == "CASE4010_0_full_gate_signed")
    bopen = next(row for row in results if row["case_id"] == "CASE4010_1_boundary_action_open")
    wopen = next(row for row in results if row["case_id"] == "CASE4010_2_worldtube_open")
    popen = next(row for row in results if row["case_id"] == "CASE4010_3_projection_open")
    nopen = next(row for row in results if row["case_id"] == "CASE4010_4_nonhilbert_open")
    dopen = next(row for row in results if row["case_id"] == "CASE4010_5_derivative_boundary_open")
    finite_case = next(row for row in results if row["case_id"] == "CASE4010_6_numeric_pack")
    add("VAL4010_18_full_case", full["J_R_boundary_status"] == "J_R_BOUNDARY_ZERO_IF_SINGLE_BRANCH_SIGNED", "full gate conditionally zeros")
    add("VAL4010_19_boundary_case", bopen["J_R_boundary_status"] == "DELTA_R_B_R_LIVE", "boundary action open routed")
    add("VAL4010_20_worldtube_case", wopen["J_R_boundary_status"] == "DELTA_R_W_SOURCE_LIVE", "worldtube open routed")
    add("VAL4010_21_projection_case", popen["J_R_boundary_status"] == "PILOC_COMMUTATOR_TAIL_LIVE", "projection open routed")
    add("VAL4010_22_nonhilbert_case", nopen["J_R_boundary_status"] == "NONHILBERT_BOUNDARY_TAIL_LIVE", "non-Hilbert open routed")
    add("VAL4010_23_derivative_case", dopen["J_R_boundary_status"] == "PI_R_N_LIVE", "derivative boundary open routed")
    add("VAL4010_24_finite_case", finite_case["boundary_status"] == "FINITE_BOUNDARY_PACK_NONCLAIM", "finite pack case routed")
    add("VAL4010_25_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4010_26_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4010_27_doc_exists", DOC_PATH.exists() and "Finite Row" in read_text(DOC_PATH), "document written")
    add("VAL4010_28_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4010_29_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4010_30_compile", compile_ok, "script compiles")
    add("VAL4010_31_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    output_tables = [sources, theorem, audit, finite, results, read_csv(OUTPUTS["decision"]), read_csv(OUTPUTS["claim_gate"]), read_csv(OUTPUTS["next"]), read_csv(OUTPUTS["status"])]
    add("VAL4010_32_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4010_33_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4010_34_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4010_35_forward_target", "worldtube" in read_text(OUTPUTS["next"]) and "Hilbert" in read_text(OUTPUTS["next"]), "forward target is Hilbert worldtube owner")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    finite = finite_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["finite"], finite)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, theorem, audit, finite, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4010 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
