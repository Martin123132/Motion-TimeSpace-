from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4007"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4007-Y5-R2FR-cell-lock-matter-readout-descent-or-JR-bound-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

ETA_SOURCE_BOUND = 2.8e-15

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4007_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_4007_JR_CHAIN_RULE_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_4007_MATTER_READOUT_DESCENT_AUDIT.csv",
    "bounds": SRC / "P8_Y5_R2FR_4007_JR_BOUND_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4007_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4007_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4007_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4007_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4007_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4007_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4007_VALIDATION.csv",
}

NEXT_DOC = "4008-Y5-R2FR-source-label-forgetting-parent-functor-or-JR-coefficient-pack.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4008_source_label_forgetting_parent_functor_or_JR_coefficient_pack.py"


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
        ("SRC4007_00_handoff", SRC / "P8_Y5_R2FR_4006_NEXT_TARGET.csv", "NEXT4006_0", "4006 handoff to J_R"),
        ("SRC4007_01_delta_R", SRC / "P8_Y5_R2FR_4006_VARIATION_CHAIN.csv", "VAR4006_1_delta_R_or_cell_density", "4006 delta_R equation"),
        ("SRC4007_02_lambda_gate", SRC / "P8_Y5_R2FR_4006_STRESS_CURRENT_GATE.csv", "SCG4006_1_lambda", "lambda_R depends on J_R"),
        ("SRC4007_03_JR_row", SRC / "P8_Y5_R2FR_4006_FINITE_COEFFICIENT_ACQUISITION_ROWS.csv", "FR4006_1_J_R", "finite J_R handoff"),
        ("SRC4007_04_field_quotient", SRC / "P8_Y5_FIELD_QUOTIENT_2570_MATTER_DESCENT_GATE.csv", "MD2570_0_chain_rule", "matter quotient chain rule"),
        ("SRC4007_05_premise_matter", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv", "PRE2611_2_matter_functor", "matter functor premise"),
        ("SRC4007_06_premise_prefactor", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv", "PRE2611_4_no_shadow_prefactor", "no source prefactor premise"),
        ("SRC4007_07_chain_rule", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_CHAIN_RULE_DECOMPOSITION.csv", "CR2611_0_variation_identity", "full matter variation split"),
        ("SRC4007_08_direct_vertex", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_CHAIN_RULE_DECOMPOSITION.csv", "CR2611_6_direct_vertex", "direct matter/source vertex"),
        ("SRC4007_09_source_zero", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_SOURCE_ZERO_STATUS.csv", "SZ2611_0_matter", "J_matter status"),
        ("SRC4007_10_decision_best_next", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_DECISION_LEDGER.csv", "DEC2611_4_best_next", "best matter-specific obstruction"),
        ("SRC4007_11_matter_descent_theorem", SRC / "P8_Y5_R2FR_3646_MATTER_DESCENT_THEOREM_ATTEMPT.csv", "MDT3646_0_statement", "matter descent theorem"),
        ("SRC4007_12_marker_clause", SRC / "P8_Y5_R2FR_3646_MATTER_DESCENT_CLAUSE_AUDIT.csv", "MDC3646_4_no_marker_constants", "marker/constants clause"),
        ("SRC4007_13_no_prefactor", SRC / "P8_Y5_R2FR_3989_MATTER_DESCENT_NO_SOURCE_PREFACTOR_THEOREM.csv", "NP3989_0_no_prefactor_criterion", "no-source-prefactor criterion"),
        ("SRC4007_14_prefactor_countermodel", SRC / "P8_Y5_R2FR_3989_MATTER_DESCENT_NO_SOURCE_PREFACTOR_THEOREM.csv", "NP3989_1_countermodel_retained", "source-prefactor countermodel"),
        ("SRC4007_15_qmap_matter", SRC / "P8_EM_actual_q_map_vertical_basis_candidate.csv", "QMAP3517_2_matter_constants", "q-map matter constants candidate"),
        ("SRC4007_16_no_direct_constants", SRC / "P8_constant_sector_universality_CONTRACT.csv", "C2_no_direct_constant_vertices", "constant-sector direct vertex gate"),
        ("SRC4007_17_universal_source", SRC / "P8_constant_sector_universality_CONTRACT.csv", "C3_universal_source_variation", "universal source variation gate"),
        ("SRC4007_18_bulk_boundary_charge", SRC / "P8_constant_sector_universality_CONTRACT.csv", "C5_no_bulk_boundary_constant_charge", "bulk/boundary constant charge gate"),
        ("SRC4007_19_selector_blind", SRC / "P8_source_owner_parent_action_terms_CONTRACT.csv", "A6_selector_blind_source_action", "selector-blind source action"),
        ("SRC4007_20_species_zero", SRC / "P8_species_source_charge_residual_or_zero.csv", "SSC2675_1_conditional_zero", "species source conditional zero"),
        ("SRC4007_21_no_bound_inversion", SRC / "P8_species_source_charge_residual_or_zero.csv", "SSC2675_3_no_bound_inversion_guard", "bound inversion guard"),
        ("SRC4007_22_zg_owner", SRC / "P8_EM_current_source_Ward_alpha_source_residual.csv", "CSR3508_0_z_g", "current owner unsigned"),
        ("SRC4007_23_alpha_source", SRC / "P8_EM_current_source_Ward_alpha_source_residual.csv", "CSR3508_2_beta_source_alpha", "alpha/source marker live"),
        ("SRC4007_24_preweight", SRC / "P8_EM_current_source_Ward_alpha_source_residual.csv", "CSR3508_5_prevariation_weight", "prevariation weight countermodel"),
        ("SRC4007_25_same_frame", SRC / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv", "S0_same_frame", "same observed frame"),
        ("SRC4007_26_no_extra_charge", SRC / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv", "S3_no_extra_long_range_charge", "extra source charge gate"),
        ("SRC4007_27_matter_factorization", SRC / "P8_no_species_source_charge_CONTRACT.csv", "S1_matter_factorization", "no species source matter factorization"),
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
            "theorem_id": "JRT4007_0_definition",
            "claim_piece": "cell-lock matter/readout source",
            "mathematical_form": "J_R := delta_R(S_matter + B_readout + S_eff) at fixed public quotient data and fixed boundary convention",
            "derived_result": "4006 lambda equation becomes lambda_R = -(J_R + delta B_R/delta R_AB + readout_regen)",
            "status": "DEFINITION_FROM_4006",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "JRT4007_1_q_basic_chain_rule",
            "claim_piece": "geometric matter descent",
            "mathematical_form": "If S_matter = Sbar_m[Obs(q(Phi)), psi, theta] and v_R in ker(Dq), then delta_R S_matter|geom = (delta Sbar/dObs) DObs(Dq[v_R]) = 0",
            "derived_result": "Hilbert/coframe geometry does not source J_R when R_AB is a true vertical representative variable",
            "status": "EXACT_CHAIN_RULE_ZERO_IF_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "JRT4007_2_constants_source_labels",
            "claim_piece": "constant/material/source-label descent",
            "mathematical_form": "sum_A (partial Sbar/partial theta_A) delta_R theta_A = 0 if theta_A are q-basic representation data and no source/material label maps to a coupling slot",
            "derived_result": "masses, charges, alpha_EM, clock standards and material labels are harmless only after the no-marker/no-Hom grammar is parent-signed",
            "status": "EXACT_ZERO_CONDITION_WITH_LIVE_COUNTERMODEL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "JRT4007_3_readout_descent",
            "claim_piece": "readout regeneration",
            "mathematical_form": "delta_R(B_readout + S_eff) = 0 if projectors/calibration/readout kernels are fixed before variation or descend as q-basic functionals",
            "derived_result": "readout_regen is zero only for variation-before-readout with no post-variation source mask",
            "status": "EXACT_ZERO_CONDITION_READOUT_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "JRT4007_4_no_source_prefactor",
            "claim_piece": "source-label-forgetting functor",
            "mathematical_form": "No Hom(source/species/material label -> R_+ source weight) in the ordinary matter constructor implies R_source_prefactor=0",
            "derived_result": "the clean route to J_R=0 is a parent object-language ban on source-only prefactors before variation",
            "status": "CRITERION_DERIVED_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "JRT4007_5_countermodel",
            "claim_piece": "finite J_R counterterm",
            "mathematical_form": "S_matter = sum_A w_A(R_AB) S_A gives J_R = sum_A (partial_R w_A) L_A + source-normalization/readout terms",
            "derived_result": "Ward conservation does not kill pre-variation weights; they must be forbidden by grammar or carried as finite coefficients",
            "status": "COUNTERMODEL_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "JRT4007_6_lambda_closure",
            "claim_piece": "local multiplier closure",
            "mathematical_form": "If J_R=0, delta B_R/delta R_AB=0, readout_regen=0, and no derivative escape exists, then lambda_R=0 and the cell stress/current contribution is silent",
            "derived_result": "the local branch can reduce to the 4006 auxiliary route, but only conditionally; current corpus does not yet claim it",
            "status": "CONDITIONAL_LOCAL_CLOSURE_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "AUD4007_0_q_kernel",
            "clause": "R_AB variation is vertical: v_R in ker(Dq)",
            "source_anchor": "QMAP3517_7_RAB_auxiliary;MD2570_0_chain_rule",
            "current_status": "CANDIDATE_NOT_PARENT_SIGNED",
            "effect_on_JR": "geometric matter term stays open until actual R_AB verticality is signed",
            "next_action": "turn q-map candidate into a parent branch clause or keep A_geom/J_R",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4007_1_observed_coframe",
            "clause": "observed metric/coframe/connection descend through q",
            "source_anchor": "PRE2611_1_observed_geometry;QMAP3517_0_public_geometry",
            "current_status": "CONDITIONAL_UNSIGNED",
            "effect_on_JR": "Hilbert stress can source R_AB if a hidden coframe leaks into matter",
            "next_action": "same-frame observed coframe theorem, not arena-by-arena readout fitting",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4007_2_matter_functor",
            "clause": "S_matter=Sbar[Obs(q(Phi)),psi,theta]",
            "source_anchor": "PRE2611_2_matter_functor;S1_matter_factorization",
            "current_status": "CONTRACT_WRITTEN_NOT_PARENT_DERIVED",
            "effect_on_JR": "without this, direct R_AB/source/worldtube vertices remain legal",
            "next_action": "write source-label-forgetting parent matter constructor",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4007_3_no_prefactor",
            "clause": "no pre-variation source/species/material weight w_A(R_AB)",
            "source_anchor": "NP3989_0_no_prefactor_criterion;CSR3508_5_prevariation_weight",
            "current_status": "CRITERION_DERIVED_COUNTERMODEL_LIVE",
            "effect_on_JR": "this is the exact live leak: J_R contains sum_A partial_R w_A L_A",
            "next_action": "prove no-Hom/source-label-forgetting grammar or fill w'_A coefficient rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4007_4_constants_markers",
            "clause": "masses, charges, alpha_EM, clocks and material labels are R_AB-blind",
            "source_anchor": "MDC3646_4_no_marker_constants;CSR3508_2_beta_source_alpha",
            "current_status": "UNSIGNED",
            "effect_on_JR": "alpha/source/material markers can mimic a finite source charge even if geometry descends",
            "next_action": "constant-sector universality theorem or coefficient pack",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4007_5_readout_order",
            "clause": "readout/calibration/projectors fixed before R_AB variation",
            "source_anchor": "CSR3508_4_postvariation_rescaling;QMAP3517_8_projector_readout",
            "current_status": "UNSIGNED",
            "effect_on_JR": "post-variation masks produce readout_regen in the 4006 lambda equation",
            "next_action": "variation-before-readout contract or readout_regen finite row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4007_6_boundary_worldtube",
            "clause": "matter/worldtube boundary terms are zero/exact/proper or bounded",
            "source_anchor": "CR2611_5_boundary;PRE2611_5_worldtube_support",
            "current_status": "OPEN",
            "effect_on_JR": "boundary/local projection flux can re-enter even after bulk matter descent",
            "next_action": "separate boundary nohair pass after source-label grammar",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4007_7_same_branch",
            "clause": "all clauses close in one parent branch",
            "source_anchor": "MDC3646_7_same_branch",
            "current_status": "MISSING_SINGLE_BRANCH_CERTIFICATE",
            "effect_on_JR": "no ladder-magic certificate: stitched rows do not prove J_R=0",
            "next_action": "4008 must target the parent constructor, not another disconnected audit",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "JRB4007_0_master",
            "coefficient": "J_R",
            "formula": "J_R = J_R^geom + J_R^theta + J_R^prefactor + J_R^readout + J_R^worldtube + J_R^boundary",
            "value": "MISSING_ZERO_THEOREM_OR_COMPONENT_VALUES",
            "units": "action_density_per_RAB_or_dimensionless_source_charge_after_normalization",
            "observable_link": "local_GR;Newton_G;PPN;R10;WEP;clocks;EM_alpha",
            "source_path": str(SRC / "P8_Y5_R2FR_4007_JR_CHAIN_RULE_THEOREM.csv"),
            "source_status": "MASTER_RESIDUAL_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JRB4007_1_prefactor",
            "coefficient": "w_R_source_4007",
            "formula": "w_R_source_4007 := sup_A |partial_R ln w_A| for S_matter=sum_A w_A(R_AB)S_A",
            "value": "MISSING_PARENT_GRAMMAR_BAN_OR_NUMERIC_WEIGHT",
            "units": "per_RAB",
            "observable_link": "source_composition;WEP;PPN;R10",
            "source_path": str(SRC / "P8_Y5_R2FR_3989_MATTER_DESCENT_NO_SOURCE_PREFACTOR_THEOREM.csv"),
            "source_status": "COUNTERMODEL_LIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JRB4007_2_species_bound_scale",
            "coefficient": "eta_source_AB",
            "formula": "eta_source_AB = epsilon_species_A - epsilon_species_B",
            "value": ETA_SOURCE_BOUND,
            "units": "dimensionless_bound_scale",
            "observable_link": "MICROSCOPE_WEP;source_normalization",
            "source_path": str(SRC / "P8_species_source_charge_residual_or_zero.csv"),
            "source_status": "BOUND_SCALE_ONLY_NOT_THEORY_VALUE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JRB4007_3_constants_markers",
            "coefficient": "b_theta_R",
            "formula": "b_theta_R := sup_a |partial_R theta_a/theta_a| over masses, charges, alpha_EM, clocks and material standards",
            "value": "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_COMPONENTS",
            "units": "per_RAB",
            "observable_link": "clocks;alpha_EM;charge_readout;WEP",
            "source_path": str(SRC / "P8_Y5_R2FR_3646_MATTER_DESCENT_CLAUSE_AUDIT.csv"),
            "source_status": "MISSING_PARENT_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JRB4007_4_readout",
            "coefficient": "readout_regen_R",
            "formula": "readout_regen_R := delta_R(B_readout+S_eff) after variation-before-readout split",
            "value": "MISSING_READOUT_ORDER_THEOREM_OR_NUMERIC_KERNEL",
            "units": "same_as_J_R",
            "observable_link": "Newton_G;PPN;R10;orbits;clocks",
            "source_path": str(SRC / "P8_EM_current_source_Ward_alpha_source_residual.csv"),
            "source_status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JRB4007_5_no_bound_inversion_guard",
            "coefficient": "C_parent_WEP_or_JR",
            "formula": "empirical eta/source bounds may constrain but cannot define the parent coefficient",
            "value": "MISSING_PARENT_COEFFICIENT",
            "units": "declared_parent_basis",
            "observable_link": "WEP;local_GR_source",
            "source_path": str(SRC / "P8_species_source_charge_residual_or_zero.csv"),
            "source_status": "BOUND_INVERSION_FORBIDDEN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4007_0_all_clauses_signed",
            "q_vertical": True,
            "matter_functor": True,
            "no_prefactor": True,
            "constants_blind": True,
            "readout_fixed": True,
            "boundary_open": False,
            "numeric_components": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4007_1_prefactor_open",
            "q_vertical": True,
            "matter_functor": True,
            "no_prefactor": False,
            "constants_blind": True,
            "readout_fixed": True,
            "boundary_open": False,
            "numeric_components": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4007_2_marker_constants_open",
            "q_vertical": True,
            "matter_functor": True,
            "no_prefactor": True,
            "constants_blind": False,
            "readout_fixed": True,
            "boundary_open": False,
            "numeric_components": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4007_3_readout_open",
            "q_vertical": True,
            "matter_functor": True,
            "no_prefactor": True,
            "constants_blind": True,
            "readout_fixed": False,
            "boundary_open": False,
            "numeric_components": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4007_4_boundary_open",
            "q_vertical": True,
            "matter_functor": True,
            "no_prefactor": True,
            "constants_blind": True,
            "readout_fixed": True,
            "boundary_open": True,
            "numeric_components": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4007_5_numeric_bound_pack",
            "q_vertical": False,
            "matter_functor": False,
            "no_prefactor": False,
            "constants_blind": False,
            "readout_fixed": False,
            "boundary_open": True,
            "numeric_components": True,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4007_6_missing_everything",
            "q_vertical": False,
            "matter_functor": False,
            "no_prefactor": False,
            "constants_blind": False,
            "readout_fixed": False,
            "boundary_open": True,
            "numeric_components": False,
            "timestamp_utc": timestamp,
        },
    ]


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        q_vertical = bool(case["q_vertical"])
        matter_functor = bool(case["matter_functor"])
        no_prefactor = bool(case["no_prefactor"])
        constants_blind = bool(case["constants_blind"])
        readout_fixed = bool(case["readout_fixed"])
        boundary_open = bool(case["boundary_open"])
        numeric_components = bool(case["numeric_components"])
        missing_zero = not all([q_vertical, matter_functor, no_prefactor, constants_blind, readout_fixed])

        if all([q_vertical, matter_functor, no_prefactor, constants_blind, readout_fixed]) and not boundary_open:
            input_status = "CONDITIONAL_JR_ZERO"
            jr_status = "J_R_ZERO_IF_PARENT_SIGNED"
            lambda_status = "LAMBDA_R_ZERO_IF_4006_BOUNDARY_GATE_CLOSED"
            next_action = "promote only after parent action adopts the clauses in one branch"
        elif numeric_components:
            input_status = "FINITE_BOUND_PACK_NONCLAIM"
            jr_status = "J_R_RETAINED_WITH_NUMERIC_TARGETS"
            lambda_status = "LAMBDA_R_FINITE_NONCLAIM"
            next_action = "fill component coefficients and arena projections"
        elif not q_vertical or not matter_functor:
            input_status = "MISSING_PARENT_DESCENT"
            jr_status = "J_R_NOT_ZEROED"
            lambda_status = "LAMBDA_R_NOT_ZERO"
            next_action = "write the parent matter constructor rather than re-auditing symptoms"
        elif not no_prefactor:
            input_status = "PREVARIATION_WEIGHT_OPEN"
            jr_status = "J_R_PREFACTOR_COUNTERTERM_LIVE"
            lambda_status = "LAMBDA_R_NOT_ZERO"
            next_action = "prove source-label-forgetting/no-Hom grammar or bound w_R_source"
        elif not constants_blind:
            input_status = "CONSTANT_MARKER_OPEN"
            jr_status = "J_R_THETA_COUNTERTERM_LIVE"
            lambda_status = "LAMBDA_R_NOT_ZERO"
            next_action = "prove constant-sector universality or fill b_theta_R"
        elif not readout_fixed:
            input_status = "READOUT_REGEN_OPEN"
            jr_status = "J_R_READOUT_COMPONENT_LIVE"
            lambda_status = "LAMBDA_R_NOT_ZERO"
            next_action = "prove variation-before-readout or fill readout_regen_R"
        elif missing_zero:
            input_status = "MISSING_PARENT_DESCENT"
            jr_status = "J_R_NOT_ZEROED"
            lambda_status = "LAMBDA_R_NOT_ZERO"
            next_action = "write the remaining parent matter clause rather than re-auditing symptoms"
        else:
            input_status = "BOUNDARY_ONLY_OPEN"
            jr_status = "J_R_ZERO_BULK_ONLY"
            lambda_status = "LAMBDA_R_BLOCKED_BY_BOUNDARY"
            next_action = "separate boundary nohair/B_R pass"

        rows.append(
            {
                "case_id": case["case_id"],
                "input_status": input_status,
                "J_R_status": jr_status,
                "lambda_R_status": lambda_status,
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
            "decision_id": "DEC4007_0_theorem",
            "decision": "J_R=0 theorem is exact under source-label-forgetting quotient matter descent",
            "reason": "the chain rule kills geometry, constants and readout terms when they are q-basic and fixed before variation",
            "effect": "local coframe-cell route remains alive as a derivable route, not an axiom",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4007_1_countermodel",
            "decision": "current corpus cannot claim J_R=0 because pre-variation source weights remain legal",
            "reason": "S_matter=sum_A w_A(R_AB)S_A produces J_R=sum_A partial_R w_A L_A and is not killed by Ward accounting",
            "effect": "J_R finite row is mandatory unless 4008 bans the constructor",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4007_2_bound_policy",
            "decision": "WEP/source bounds may be used as bound scales but not as parent coefficients",
            "reason": "empirical eta cannot define C_parent_WEP or J_R without a source-independent parent coefficient",
            "effect": "eta_source_AB=2.8e-15 is retained as a bound scale only",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4007_3_next",
            "decision": "next target is source-label-forgetting parent functor or J_R coefficient pack",
            "reason": "this is the shortest path to actual forward movement: ban the dangerous constructor or pay it numerically",
            "effect": "4008 should attack the parent object language directly",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CLAIM4007_0_JR_zero",
            "claim": "J_R=0",
            "allowed": False,
            "blocker": "source-label-forgetting matter functor, no-prefactor, constants-blindness, readout order and single-branch adoption not parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4007_1_lambda_zero",
            "claim": "lambda_R=0",
            "allowed": False,
            "blocker": "depends on J_R=0 plus boundary/readout/derivative gates from 4006",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4007_2_local_GR",
            "claim": "local GR/Newton recovered",
            "allowed": False,
            "blocker": "4007 narrows the source coupling obstruction but does not close the full local branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4007_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "write the source-label-forgetting parent matter constructor and prove it bans pre-variation source weights, or produce the first J_R coefficient pack",
            "success_condition": "either no Hom(source/species/material label -> R_+ source weight) is parent-signed in the ordinary matter constructor, or w_R_source/b_theta_R/readout_regen_R get units, source paths, arena projections and valid_for_claim=false",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "J_R descent theorem/countermodel fork written; zero route is exact if parent-signed, but current branch keeps finite J_R because source-label weights remain legal",
            "current_best_next": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    lines = [
        "# 4007 - Cell-Lock Matter/Readout Descent Or J_R Bound Row",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "The descent route is real, but conditional. The exact object is",
        "",
        "`J_R := delta_R(S_matter + B_readout + S_eff)`.",
        "",
        "Using the 4006 equation,",
        "",
        "`lambda_R = -(J_R + delta B_R/delta R_AB + readout_regen)`.",
        "",
        "So the cell-lock branch only becomes stress/current silent if `J_R`, boundary hair and readout regeneration all vanish.",
        "",
        "## Derivation",
        "",
        "If ordinary matter is a source-label-forgetting quotient functor,",
        "",
        "`S_matter = Sbar_m[Obs(q(Phi)), psi, theta]`, with `v_R in ker(Dq)`,",
        "",
        "then",
        "",
        "`delta_R S_matter = (delta Sbar/dObs) DObs(Dq[v_R]) + sum_a (partial Sbar/partial theta_a) delta_R theta_a + marker/readout terms`.",
        "",
        "The first term vanishes by the chain rule. The constants term vanishes only if masses, charges, `alpha_EM`, clocks and material standards are q-basic/fixed. The marker/readout terms vanish only if the parent grammar forgets source labels before variation and readout is fixed before variation.",
        "",
        "## Countermodel",
        "",
        "The surviving legal countermodel is simple:",
        "",
        "`S_matter = sum_A w_A(R_AB) S_A`.",
        "",
        "Then `J_R = sum_A (partial_R w_A) L_A + ...`. Ward conservation does not remove this because the weight is inserted before variation. This is the coupling leak we have been circling; now it has a name and formula.",
        "",
        "## Verdict",
        "",
        "- `J_R=0` is derivable, not assumed, under a parent-signed source-label-forgetting matter constructor.",
        "- Current corpus does not yet sign that constructor in one branch.",
        "- Therefore `J_R` remains a finite nonclaim row, with `eta_source_AB=2.8e-15` usable only as a bound scale, not as a theory coefficient.",
        "- This moves the target from vague local-GR failure to one concrete parent-language gate: ban `w_A(R_AB)`/marker source slots or pay their coefficients.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: `{row['input_status']}`, J_R=`{row['J_R_status']}`, lambda=`{row['lambda_R_status']}`, next=`{row['next_action']}`"
        )
    lines.extend(
        [
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
    marker = "## 4007 - Cell-Lock J_R Descent Fork"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: `J_R := delta_R(S_matter+B_readout+S_eff)` now has an exact chain-rule zero theorem under source-label-forgetting quotient matter descent.
- Key formula: if `S_matter=Sbar_m[Obs(q(Phi)),psi,theta]`, `v_R in ker(Dq)`, constants are q-basic and readout is fixed before variation, then `J_R=0`.
- Countermodel retained: `S_matter=sum_A w_A(R_AB)S_A` gives `J_R=sum_A(partial_R w_A)L_A+...`; Ward accounting does not kill pre-variation weights.
- Verdict: no local-GR/Newton claim; current branch needs a parent grammar ban on source-label weights or a finite `J_R` coefficient pack.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4007_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4007_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL4007_02_definition", any(row["theorem_id"] == "JRT4007_0_definition" for row in theorem), "J_R definition present")
    add("VAL4007_03_chain_rule", any(row["theorem_id"] == "JRT4007_1_q_basic_chain_rule" for row in theorem), "q-basic chain rule present")
    add("VAL4007_04_constants", any(row["theorem_id"] == "JRT4007_2_constants_source_labels" for row in theorem), "constants/source labels theorem present")
    add("VAL4007_05_readout", any(row["theorem_id"] == "JRT4007_3_readout_descent" for row in theorem), "readout descent theorem present")
    add("VAL4007_06_no_prefactor", any(row["theorem_id"] == "JRT4007_4_no_source_prefactor" for row in theorem), "no-source-prefactor criterion present")
    add("VAL4007_07_countermodel", any(row["theorem_id"] == "JRT4007_5_countermodel" for row in theorem), "prevariation weight countermodel present")
    add("VAL4007_08_lambda", any(row["theorem_id"] == "JRT4007_6_lambda_closure" for row in theorem), "lambda closure theorem present")
    add("VAL4007_09_audit_prefactor", any(row["audit_id"] == "AUD4007_3_no_prefactor" and "partial_R w_A" in row["effect_on_JR"] for row in audit), "prefactor audit names live leak")
    add("VAL4007_10_audit_same_branch", any(row["audit_id"] == "AUD4007_7_same_branch" for row in audit), "same-branch audit guard present")
    add("VAL4007_11_bound_master", any(row["row_id"] == "JRB4007_0_master" for row in bounds), "J_R master bound row present")
    add("VAL4007_12_bound_prefactor", any(row["row_id"] == "JRB4007_1_prefactor" for row in bounds), "source-weight bound row present")
    eta = next(row for row in bounds if row["row_id"] == "JRB4007_2_species_bound_scale")
    add("VAL4007_13_eta_bound", float(eta["value"]) == ETA_SOURCE_BOUND and eta["source_status"] == "BOUND_SCALE_ONLY_NOT_THEORY_VALUE", "eta bound scale recorded as nonclaim")
    add("VAL4007_14_bound_inversion", any(row["row_id"] == "JRB4007_5_no_bound_inversion_guard" for row in bounds), "bound inversion guard present")
    zero = next(row for row in results if row["case_id"] == "CASE4007_0_all_clauses_signed")
    pref = next(row for row in results if row["case_id"] == "CASE4007_1_prefactor_open")
    marker = next(row for row in results if row["case_id"] == "CASE4007_2_marker_constants_open")
    readout = next(row for row in results if row["case_id"] == "CASE4007_3_readout_open")
    boundary = next(row for row in results if row["case_id"] == "CASE4007_4_boundary_open")
    finite = next(row for row in results if row["case_id"] == "CASE4007_5_numeric_bound_pack")
    missing = next(row for row in results if row["case_id"] == "CASE4007_6_missing_everything")
    add("VAL4007_15_zero_case", zero["input_status"] == "CONDITIONAL_JR_ZERO", "signed case gives conditional J_R zero")
    add("VAL4007_16_prefactor_case", pref["input_status"] == "PREVARIATION_WEIGHT_OPEN", "prefactor-open case routed")
    add("VAL4007_17_marker_case", marker["input_status"] == "CONSTANT_MARKER_OPEN", "marker-open case routed")
    add("VAL4007_18_readout_case", readout["input_status"] == "READOUT_REGEN_OPEN", "readout-open case routed")
    add("VAL4007_19_boundary_case", boundary["input_status"] == "BOUNDARY_ONLY_OPEN", "boundary-open case routed")
    add("VAL4007_20_finite_case", finite["input_status"] == "FINITE_BOUND_PACK_NONCLAIM", "finite bound pack remains nonclaim")
    add("VAL4007_21_missing_case", missing["input_status"] == "MISSING_PARENT_DESCENT", "missing descent blocks")
    add("VAL4007_22_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4007_23_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4007_24_doc_exists", DOC_PATH.exists() and "Countermodel" in read_text(DOC_PATH), "document written")
    add("VAL4007_25_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4007_26_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4007_27_compile", compile_ok, "script compiles")
    add("VAL4007_28_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    output_tables = [sources, theorem, audit, bounds, results, read_csv(OUTPUTS["decision"]), read_csv(OUTPUTS["claim_gate"]), read_csv(OUTPUTS["next"]), read_csv(OUTPUTS["status"])]
    add("VAL4007_29_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4007_30_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4007_31_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4007_32_forward_target", "source-label-forgetting" in read_text(OUTPUTS["next"]), "forward derivation target, not vague audit loop")
    return checks


def marker_in_spine() -> bool:
    return "## 4007 - Cell-Lock J_R Descent Fork" in read_text(SPINE_PATH)


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    bounds = bound_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["bounds"], bounds)
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

    validation = build_validation_rows(timestamp, sources, theorem, audit, bounds, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4007 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
