from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1650"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md"

SOURCE_FILES = {
    "1649_doc": ROOT / "1649-Y5-R2FR-reduced-GK-symbol-match-or-observed-boundary-flux-input-runner.md",
    "1649_validation": OUT / "P8_Y5_BRR545_1649_VALIDATION.csv",
    "1649_next": OUT / "P8_Y5_PARENT_QLOC_1649_NEXT_TARGET.csv",
    "1649_symbol_audit": OUT / "P8_Y5_PARENT_QLOC_1649_REDUCED_GK_SYMBOL_MATCH_AUDIT.csv",
    "1649_repair": OUT / "P8_Y5_PARENT_QLOC_1649_RESPONSE_DISPLACEMENT_REPAIR_CONTRACT.csv",
    "1649_bobs_schema": OUT / "P8_Y5_PARENT_QLOC_1649_BOBS_INPUT_RUNNER_SCHEMA.csv",
    "1619_normal_form": OUT / "P8_Y5_PARENT_QLOC_1619_POSITIVE_AUXILIARY_NORMAL_FORM.csv",
    "1619_silence": OUT / "P8_Y5_PARENT_QLOC_1619_LOCAL_SILENCE_THEOREM.csv",
    "1620_bridge": OUT / "P8_Y5_PARENT_QLOC_1620_PARENT_SIGNATURE_BRIDGE_CONTRACT.csv",
    "1620_chain": OUT / "P8_Y5_PARENT_QLOC_1620_CHAIN_RULE_SOURCE_CURRENT_ZERO_ATTEMPT.csv",
    "1620_verticality": OUT / "P8_Y5_PARENT_QLOC_1620_QUOTIENT_VERTICALITY_MAP_AUDIT.csv",
    "1621_constraint": OUT / "P8_Y5_PARENT_QLOC_1621_CONSTRAINT_FIRST_ZMAP_GATE.csv",
    "1621_no_pole": OUT / "P8_Y5_PARENT_QLOC_1621_NO_POLE_THEOREM_AUDIT.csv",
    "1624_no_vertical_metric": OUT / "P8_Y5_PARENT_QLOC_1624_NO_VERTICAL_METRIC_DECISION.csv",
    "1629_source_slot": OUT / "P8_Y5_PARENT_QLOC_1629_RAB_SOURCE_SLOT_EXCLUSION_ATTEMPT.csv",
    "1630_action_scale": OUT / "P8_Y5_PARENT_QLOC_1630_ACTION_SCALE_MEASURE_OWNER_AUDIT.csv",
    "1630_refusal": OUT / "P8_Y5_PARENT_QLOC_1630_PRIOR_WIDTH_REFUSAL_RUNNER.csv",
    "1633_range_decision": OUT / "P8_Y5_PARENT_QLOC_1633_FINITE_RANGE_DECISION.csv",
    "1639_law": OUT / "P8_Y5_PARENT_QLOC_1639_NR_LAW_CONDITIONAL.csv",
    "1639_blockers": OUT / "P8_Y5_PARENT_QLOC_1639_SOURCE_MASS_AND_TAIL_BLOCKERS.csv",
    "1640_boundary": OUT / "P8_Y5_PARENT_QLOC_1640_BOUNDARY_SILENCE_CLAUSE_LEDGER.csv",
    "1643_inputs": OUT / "P8_Y5_PARENT_QLOC_1643_NORMALIZED_PPN_INPUT_STATUS.csv",
    "1644_denominator": OUT / "P8_Y5_PARENT_QLOC_1644_SAME_FRAME_DENOMINATOR_CLAUSE_MAP.csv",
    "1645_curl": OUT / "P8_Y5_PARENT_QLOC_1645_FIELD_SPACE_CURL_OBSTRUCTION.csv",
    "1646_deltaH_schema": OUT / "P8_Y5_PARENT_QLOC_1646_DELTAH_COMPONENT_SOURCE_SCHEMA.csv",
    "1647_curl": OUT / "P8_Y5_PARENT_QLOC_1647_DELTAH_CURL_DECOMPOSITION.csv",
    "1647_fallback": OUT / "P8_Y5_PARENT_QLOC_1647_DELTAH_CURL_SOURCE_FILL_FALLBACK.csv",
    "1648_clause_gate": OUT / "P8_Y5_PARENT_QLOC_1648_OBSERVED_FLUX_ZERO_CLAUSE_GATE.csv",
    "1648_component_fill": OUT / "P8_Y5_PARENT_QLOC_1648_DELTAH_CURL_COMPONENT_FILL.csv",
    "1648_dryrun": OUT / "P8_Y5_PARENT_QLOC_1648_BOBS_INPUT_RUNNER_DRYRUN.csv",
}

NEEDLES = {
    "1649_doc": ["The reduced GK/Ward route is still alive", "1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md"],
    "1649_validation": ["VAL1649_OVERALL", "PASS"],
    "1649_next": ["1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md", "actual quotient vertical generator"],
    "1649_symbol_audit": ["RGM1649_7_verdict", "FAIL_CURRENT_CORPUS"],
    "1649_repair": ["RDR1649_1_vertical_generator_lock", "NOT_FILLED"],
    "1649_bobs_schema": ["BIR1649_5_total_Bobs", "MISSING_COMPONENTS"],
    "1619_normal_form": ["NF1619_6_verdict", "FORMAL_MECHANISM_EXISTS_NOT_PARENT_SIGNED"],
    "1619_silence": ["LS1619_3_q_loc_zero", "CONDITIONAL_QLOC_ZERO_FOR_NORMAL_FORM"],
    "1620_bridge": ["BRC1620_6_verdict", "PARENT_SIGNATURE_BRIDGE_NOT_CLOSED"],
    "1620_chain": ["CR1620_5_verdict", "CHAIN_RULE_THEOREM_CLOSED_APPLICATION_BLOCKED"],
    "1620_verticality": ["QVM1620_5_verdict", "VERTICALITY_MAP_NOT_CLOSED"],
    "1621_constraint": ["CFG1621_2_algebraic_elimination", "BEST_CONDITIONAL_ROUTE_NOT_SIGNED"],
    "1621_no_pole": ["NPA1621_5_verdict", "NO_POLE_NOT_DERIVED_CURRENT_MTS"],
    "1624_no_vertical_metric": ["NVD1624_4_verdict", "NO_VERTICAL_METRIC_THEOREM_NOT_DERIVED_FINAL_CURRENT_AUDIT"],
    "1629_source_slot": ["RSE1629_7_verdict", "RAB_SOURCE_SLOT_EXCLUSION_NOT_DERIVED_CURRENT_CORPUS"],
    "1630_action_scale": ["ASR1630_6_verdict", "ACTION_SCALE_MEASURE_OWNER_NOT_DERIVED_CURRENT_CORPUS"],
    "1630_refusal": ["RUN1630_7_local_GR_lock", "REFUSE_SCORING"],
    "1633_range_decision": ["FR1633_2_demote", "MASSLESS_TAIL_DEMOTED_FROM_R10_TO_PPN_LOCAL"],
    "1639_law": ["NRL1639_0_geometrized_mass", "CONDITIONAL_DENOMINATOR_DERIVED_UNDER_CORPUS_TAIL_NORMALIZATION"],
    "1639_blockers": ["NRB1639_1_same_frame_mass", "MISSING_PARENT_SOURCE_MASS_CALIBRATION"],
    "1640_boundary": ["BSC1640_5_all_clauses", "FAIL_CURRENT_PROOF"],
    "1643_inputs": ["IN1643_0_PiR_boundary_abs", "MISSING_BOUND_VALUE"],
    "1644_denominator": ["MDC1644_6_poisson_gauss", "MISSING_BRIDGE"],
    "1645_curl": ["ICO1645_5_curl_verdict", "NOT_PROVED_ZERO"],
    "1646_deltaH_schema": ["DHS1646_0_deltaH_curl", "SCHEMA_ONLY_MISSING_PARENT_CURRENT_OR_NUMERIC_SOURCE"],
    "1647_curl": ["CDC1647_2_observed_reduced_boundary_flux", "OPEN_PRIMARY_NEXT_TARGET"],
    "1647_fallback": ["HSF1647_0_observed_reduced_boundary_flux", "MISSING_OBSERVED_REDUCED_BOUNDARY_FLUX_ZERO_OR_NUMERIC"],
    "1648_clause_gate": ["OFC1648_1_Gamma_Khat_Ploc_owner", "BLOCKED_BY_REDUCED_GK_SYMBOL_MATCH"],
    "1648_component_fill": ["BCF1648_5_total_B_observed", "MISSING_COMPONENTS"],
    "1648_dryrun": ["BIR1648_0_no_candidate", "BLOCKED_MISSING_COMPONENTS"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1650_SOURCE_REGISTER.csv"
PARENT_VERDICT = OUT / "P8_Y5_PARENT_QLOC_1650_PARENT_SIGNATURE_VERDICT.csv"
Z_MAP_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1650_RESPONSE_DISPLACEMENT_TO_RAB_MAP.csv"
BOBS_PRIORITY = OUT / "P8_Y5_PARENT_QLOC_1650_BOBS_SOURCE_ACQUISITION_PRIORITY.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_QLOC_1650_LOCAL_GR_STATUS_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1650_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1650_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1650_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1650_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    PARENT_VERDICT,
    Z_MAP_AUDIT,
    BOBS_PRIORITY,
    LOCAL_STATUS,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    PARENT_VERDICT,
    Z_MAP_AUDIT,
    BOBS_PRIORITY,
    LOCAL_STATUS,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

COPY_TARGETS = {
    PARENT_VERDICT: [
        QUARANTINE / "PARENT_SIGNATURE_VERDICT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_parent_signature_verdict_nonclaim_1650.csv",
        QUEUE / "JR1650_PARENT_SIGNATURE_VERDICT_NONCLAIM.csv",
    ],
    Z_MAP_AUDIT: [
        QUARANTINE / "RESPONSE_DISPLACEMENT_TO_RAB_MAP_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_response_displacement_to_RAB_map_nonclaim_1650.csv",
        QUEUE / "JR1650_RESPONSE_DISPLACEMENT_TO_RAB_MAP_NONCLAIM.csv",
    ],
    BOBS_PRIORITY: [
        QUARANTINE / "BOBS_SOURCE_ACQUISITION_PRIORITY_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Bobs_source_acquisition_priority_nonclaim_1650.csv",
        QUEUE / "JR1650_BOBS_SOURCE_ACQUISITION_PRIORITY_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1650.csv",
        QUEUE / "JR1650_NEXT_TARGET_NONCLAIM.csv",
    ],
}


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {
        "accepted_as_zero",
        "accepted_for_scoring",
        "claim_allowed",
        "parent_signed",
        "reopens_local_claim",
        "score_allowed",
        "score_ready",
        "source_ready",
        "valid_for_claim",
        "valid_for_mts_claim",
        "valid_prediction_row",
    }
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1650 response-displacement parent-owner and Bobs acquisition synthesis",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def parent_verdict_rows() -> list[dict[str, object]]:
    rows = [
        (
            "PSV1650_0_formal_mechanism",
            "1619 positive auxiliary / response-displacement normal form",
            "formal action owns Gamma_eff, defines K_hat, passes Helmholtz by construction, and gives F_1=0 inside the constructed class",
            "FORMAL_MECHANISM_EXISTS",
            "not parent-signed to current MTS variables or observed residual vector",
        ),
        (
            "PSV1650_1_vertical_generator",
            "Z/R_AB as actual quotient-vertical generator",
            "Dq[Z]=0 or constraint-first removal before matter coupling",
            "NOT_PARENT_SIGNED",
            "1620 verticality map says Z/R_AB is coframe-visible or uncomputed; 1621 constraint route is best but unsigned",
        ),
        (
            "PSV1650_2_no_pole_no_vertical_metric",
            "no kinetic pole / no vertical metric constructor",
            "R_AB derivative operator illegal or algebraically eliminated by parent grammar",
            "NOT_DERIVED_CURRENT_CORPUS",
            "1621 no-pole and 1624 no-vertical-metric routes remain conditional with active countermodels",
        ),
        (
            "PSV1650_3_source_current_zero",
            "J_Z/J_R source-current zero by matter descent",
            "delta_v S_matter vanishes by quotient chain rule if verticality, no-marker, no direct source slot, and boundary silence all hold",
            "EXACT_CONDITIONAL_APPLICATION_BLOCKED",
            "1620 closes the formula but not the MTS application; 1629/1630 keep source-slot/action-scale countermodels active",
        ),
        (
            "PSV1650_4_reciprocal_hair",
            "massless Q_R/r reciprocal tail",
            "Q_R=-Pi_R and q_R=-Pi_R c^2/(2GM_*) under conditional tail/source-mass normalization",
            "LIVE_LOCAL_PPN_HAZARD",
            "1633 demotes finite-range R10; 1639 gives conditional q_R law; Pi_R=0/Mstar remain unsigned",
        ),
        (
            "PSV1650_5_boundary_and_denominator",
            "Pi_R=0, Mstar/M_H_ref, and boundary/source reference locks",
            "proper boundary silence plus same-frame Hamiltonian source denominator would recover q_R=0 and support bounds",
            "NOT_CLOSED",
            "1640-1645 keep boundary, Mstar, Htau/reference, positivity, and Poisson/Gauss bridge blocked",
        ),
        (
            "PSV1650_6_observed_flux",
            "B_observed_reduced_flux_over_MH and deltaH curl",
            "reduced GK Ward/no-flux theorem or source-backed component rows",
            "LIVE_FALLBACK_REQUIRED",
            "1647-1649 leave observed reduced flux, source/projector flux, and Bobs components unfilled",
        ),
        (
            "PSV1650_7_verdict",
            "response-displacement parent owner for current MTS",
            "all parent signature, source-current, boundary, denominator, and observed-flux clauses close jointly",
            "PARENT_OWNER_NOT_CLOSED_CURRENT_CORPUS",
            "keep derivation contracts, but move next work to source-ready Bobs priority runner unless new parent primitives appear",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "verdict_id": verdict_id,
            "target": target,
            "required_result": required_result,
            "status": status,
            "effect": effect,
            "parent_signed": False,
            "source_ready": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for verdict_id, target, required_result, status, effect in rows
    ]


def z_map_rows() -> list[dict[str, object]]:
    rows = [
        (
            "ZMAP1650_0_formal_Z",
            "Z^A response-displacement coordinates",
            "formal odd residual coordinate in the 1619 normal form",
            "FORMAL_ONLY",
            "useful derivation mechanism, not yet actual MTS variable",
        ),
        (
            "ZMAP1650_1_RAB_candidate",
            "R_AB = ln(A B) / reciprocal cell-visible channel",
            "candidate physical/representative residual behind the response-displacement route",
            "VISIBLE_OR_UNCOMPUTED",
            "cannot call it vertical without Dq calculation or constraint-first origin",
        ),
        (
            "ZMAP1650_2_Dq_test",
            "Dq[v_Z] or Dq[v_R]",
            "must vanish on an open local branch or be removed before matter coupling",
            "VERTICALITY_MAP_NOT_CLOSED",
            "source-current zero chain rule does not fire",
        ),
        (
            "ZMAP1650_3_constraint_first",
            "algebraic/no-pole removal",
            "parent second-class/no-pole route removes R_AB before matter/readout",
            "BEST_CONDITIONAL_ROUTE_NOT_SIGNED",
            "do not insert lambda_R by hand as a proof",
        ),
        (
            "ZMAP1650_4_chain_rule",
            "J_Z=0 / J_R=0",
            "descent makes source current vanish only after verticality, no-marker, no direct slot, and boundary clauses close",
            "EXACT_CONDITIONAL_APPLICATION_BLOCKED",
            "finite source-current rows remain live",
        ),
        (
            "ZMAP1650_5_local_tail",
            "Q_R/r and q_R",
            "if Pi_R survives, R_AB ~ Q_R/r and Delta_gamma ~= q_R",
            "LOCAL_PPN_RESIDUAL_LIVE",
            "Pi_R zero theorem or absolute q_R bound required",
        ),
        (
            "ZMAP1650_6_exact_GR_condition",
            "Pi_R=0 plus Bobs=0 plus M_H_ref owner",
            "Pi_R=0 -> Q_R=0 -> q_R=0, while Bobs/deltaH vanish independently",
            "EXACT_ROUTE_IDENTIFIED_NOT_PROVED",
            "this is the local-GR target, not a current result",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "map_id": map_id,
            "object": obj,
            "meaning": meaning,
            "status": status,
            "effect": effect,
            "parent_signed": False,
            "accepted_as_zero": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for map_id, obj, meaning, status, effect in rows
    ]


def bobs_priority_rows() -> list[dict[str, object]]:
    rows = [
        (
            "BPA1650_0_denominator",
            "M_H_ref / Mstar_same_frame",
            "global denominator for normalized Bobs, q_R, Pi_R, and PPN residuals",
            "derive H_tau-H_ref integrability/reference/positivity/Poisson-Gauss bridge or source parent row",
            "MISSING_STABLE_MH_REF_AND_NONCIRCULAR_DENOMINATOR",
            "blocks every finite bound runner",
            0,
        ),
        (
            "BPA1650_1_source_measure_projector",
            "B_obs_source_measure_over_MH; Y5_projected_source_flux_over_MH",
            "coupling/source-normalization flux and projected source current leakage",
            "derive source-measure silence, Pi_M/P_loc descent, or source-backed flux bound",
            "MISSING_SOURCE_MEASURE_SILENCE_OR_NUMERIC",
            "highest coupling-facing Bobs component",
            1,
        ),
        (
            "BPA1650_2_boundary_improvement",
            "B_obs_boundary_improvement_over_MH; B_zero_flux; Pi_R_boundary_abs",
            "observed boundary/reference/worldtube flux",
            "derive proper/exact boundary zero projection or source finite boundary flux",
            "MISSING_BOUNDARY_REFERENCE_NO_FLUX_OR_NUMERIC",
            "direct route to Q_R/r hair and deltaH curl",
            2,
        ),
        (
            "BPA1650_3_projector_commutator",
            "B_obs_projector_commutator_over_MH",
            "commutator leakage from applying P_loc/Pi_M after readout/domain split",
            "derive parent projector algebra and commutator silence or source finite commutator bound",
            "MISSING_PROJECTOR_DESCENT_ZERO_OR_NUMERIC",
            "prevents hidden projection cancellations",
            3,
        ),
        (
            "BPA1650_4_bulk_Euler_symbol_owner",
            "B_obs_bulk_Euler_over_MH; Gamma_eff/K_hat owner",
            "bulk Ward/Euler term in the reduced GK stress identity",
            "parent-sign reduced action, Gamma scalar density, Khat metric response, Helmholtz, and on-shell branch",
            "MISSING_REDUCED_EULER_ZERO_OR_NUMERIC",
            "keeps derivation-first route alive but currently not executable",
            4,
        ),
        (
            "BPA1650_5_corner_tau_reference",
            "B_obs_corner_edge_over_MH; tau_ref_surface_mismatch_over_MH",
            "corner/edge, tau, reference, and surface mismatch residuals",
            "derive same tau/reference/surface theorem or source absolute mismatch rows",
            "MISSING_OBSERVED_EDGE_ZERO_OR_NUMERIC",
            "prevents boundary bookkeeping from moving the local charge",
            5,
        ),
        (
            "BPA1650_6_total_no_cancellation",
            "B_observed_reduced_flux_over_MH; delta_H_tau_nonintegrable_over_MH",
            "absolute sum of all live components",
            "all components zero/bounded with M_H_ref and no cancellation credit",
            "MISSING_COMPONENTS",
            "no score or local-GR claim until every row is real",
            6,
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "priority_id": priority_id,
            "quantity": quantity,
            "role": role,
            "required_next_input": required_next_input,
            "current_status": current_status,
            "why_priority": why_priority,
            "priority_rank": priority_rank,
            "source_ready": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for priority_id, quantity, role, required_next_input, current_status, why_priority, priority_rank in rows
    ]


def local_status_rows() -> list[dict[str, object]]:
    rows = [
        (
            "LGR1650_0_exact_route",
            "local GR/Newton recovery by theorem",
            "Pi_R=0, q_R=0, Bobs=0, deltaH curl=0, and M_H_ref owns same-frame Newton denominator",
            "EXACT_ROUTE_IDENTIFIED_NOT_PROVED",
            "do not claim; preserve as derivation target",
        ),
        (
            "LGR1650_1_finite_route",
            "local PPN/residual bound route",
            "absolute Pi_R/Bobs/source/projector/tau residual vector with M_H_ref and external bounds",
            "BLOCKED_MISSING_MTS_INPUTS",
            "build source-ready rows before any score",
        ),
        (
            "LGR1650_2_R10",
            "R10 finite-range comparison",
            "requires parent finite reciprocal range and alpha(lambda) kernel",
            "NOT_CURRENT_ROUTE",
            "massless Q_R/r tail stays local/PPN/orbital, not R10",
        ),
        (
            "LGR1650_3_coupling",
            "coupling/source-normalization problem",
            "source measure, action-scale owner, no source-only slots, Pi_M/P_loc descent",
            "PRIMARY_OPEN_PHYSICS_BLOCKER",
            "ties user gut-level coupling concern to exact ledgers rather than vague suspicion",
        ),
        (
            "LGR1650_4_current_position",
            "overall project state for local branch",
            "formal mechanism plus exact conditional lemmas exist, but current MTS lacks parent signatures and source-backed residual rows",
            "PROMISING_BUT_NOT_CLAIMABLE",
            "next work should make the fallback executable without demoting the derivation route",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": status_id,
            "target": target,
            "condition": condition,
            "current_status": current_status,
            "interpretation": interpretation,
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for status_id, target, condition, current_status, interpretation in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1650_0_parent_owner", "response-displacement mechanism is parent-signed to current MTS", False, "BLOCKED", "verticality/source-current/object-language/boundary/denominator clauses do not close"),
        ("CG1650_1_formal_normal_form", "1619 formal normal form proves local GR", False, "REFUSED", "formal class not mapped to actual parent vertical generator"),
        ("CG1650_2_Bobs_source_ready", "Bobs fallback has source-ready rows", False, "NOT_READY", "priority rows are schemas/blockers, not sourced values or theorem zeros"),
        ("CG1650_3_local_GR_PPN_Newton", "local GR/Newton/PPN follows from 1650", False, "NO_CLAIM", "exact route not proved and finite route not score-ready"),
        ("CG1650_4_guardrail", "1650 synthesis guardrail is installed", "INTERNAL_ONLY", "PASS_AS_INTERNAL_GUARDRAIL_ONLY", "guardrail is not evidence"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "status": status,
            "blocker": blocker,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, gate_pass, status, blocker in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        (
            "DEC1650_0_parent_owner",
            "PARENT_OWNER_NOT_CLOSED_CURRENT_CORPUS",
            "1619-1649 prove useful conditional lemmas but not the joint parent signature",
            "do not promote response-displacement to local GR proof",
        ),
        (
            "DEC1650_1_keep_derivation",
            "KEEP_EXACT_CONDITIONAL_ROUTE",
            "the formal mechanism, chain-rule lemma, Pi_R=0 chain, and Ward/no-flux contract remain real targets",
            "future new parent primitives can reopen theorem-zero path",
        ),
        (
            "DEC1650_2_Bobs_fallback",
            "BOBS_SOURCE_PRIORITY_STAGED_NONCLAIM",
            "current evidence says source-backed component rows are needed before empirical/local scoring",
            "build an executable priority runner, starting with M_H_ref and source-measure/projector/boundary flux",
        ),
        (
            "DEC1650_3_no_recycling",
            "STOP_RECYCLING_VERTICALITY_WITHOUT_NEW_PRIMITIVES",
            "1624 already records that repeated schema-only no-vertical-metric checks are not useful",
            "do not spend another turn relabeling R_AB as vertical without Dq or constraint origin",
        ),
        (
            "DEC1650_4_next",
            "NEXT_1651_BOBS_PRIORITY_RUNNER_AND_FIRST_SOURCE_ROW",
            "1650 finishes the synthesis; the next concrete progress is an executable refusal/first-source-row runner",
            "select 1651 Bobs priority runner",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1651-Y5-R2FR-Bobs-component-priority-runner-and-first-source-row.md",
            "script": "scripts/Y5_R2FR_Bobs_component_priority_runner_and_first_source_row.py",
            "objective": "turn the Bobs priority ledger into an executable refusal/first-source-row runner, starting with M_H_ref/Mstar and the source-measure/projector/boundary flux components",
            "success_condition": "either one priority component has a parent-signed zero or source-backed finite row with units/projection/source path, or the runner hard-refuses scoring with exact missing fields and next acquisition target",
            "forbidden_shortcuts": "no formal-normal-form promotion; no representative-boundary zero; no orbital-GM denominator import; no cancellation between components; no local-GR/PPN/R10/WEP claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    z_rows: list[dict[str, object]],
    priority_rows: list[dict[str, object]],
    local_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = (
        FORMALIZATION.exists()
        and any(path.name.startswith("P8_Y5_PARENT_QLOC_1650") or "1650" in path.name for path in FORMALIZATION.rglob("*") if path.is_file())
    )

    checks = [
        (
            "VAL1650_0_sources_exist",
            all(row["path_exists"] and row["needles_found"] for row in source_rows),
            "all cited 1650 source paths exist and needles are present",
        ),
        (
            "VAL1650_1_parent_verdict_complete",
            len(parent_rows) == 8 and any(row["status"] == "PARENT_OWNER_NOT_CLOSED_CURRENT_CORPUS" for row in parent_rows),
            "parent-signature verdict is complete and nonclaim",
        ),
        (
            "VAL1650_2_formal_mechanism_retained",
            any(row["status"] == "FORMAL_MECHANISM_EXISTS" for row in parent_rows)
            and any(row["status"] == "FORMAL_ONLY" for row in z_rows),
            "formal response-displacement mechanism is retained but not promoted",
        ),
        (
            "VAL1650_3_verticality_not_recycled",
            any(row["status"] == "VERTICALITY_MAP_NOT_CLOSED" for row in z_rows)
            and any(row["decision"] == "STOP_RECYCLING_VERTICALITY_WITHOUT_NEW_PRIMITIVES" for row in decisions),
            "verticality route is not re-used without new primitives",
        ),
        (
            "VAL1650_4_Bobs_priority_complete",
            len(priority_rows) == 7
            and any(row["quantity"] == "M_H_ref / Mstar_same_frame" for row in priority_rows)
            and any(row["quantity"] == "B_observed_reduced_flux_over_MH; delta_H_tau_nonintegrable_over_MH" for row in priority_rows),
            "Bobs acquisition priorities cover denominator, components, and total",
        ),
        (
            "VAL1650_5_local_status_nonclaim",
            any(row["current_status"] == "PROMISING_BUT_NOT_CLAIMABLE" for row in local_rows)
            and all(row["valid_for_claim"] is False for row in local_rows),
            "local status ledger stays nonclaim",
        ),
        (
            "VAL1650_6_claim_gates_safe",
            all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim_rows),
            "all claim gates keep MTS claims false",
        ),
        (
            "VAL1650_7_next_target_selected",
            next_targets[0]["next_target"] == "1651-Y5-R2FR-Bobs-component-priority-runner-and-first-source-row.md",
            "next target selects Bobs component priority runner",
        ),
        (
            "VAL1650_8_csv_parse",
            generated_csv_parse,
            "all generated 1650 CSVs parse",
        ),
        (
            "VAL1650_9_no_mts_claim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1650 generated rows keep MTS claim/no-score flags false",
        ),
        (
            "VAL1650_10_branch_copies",
            all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1650_11_queue_copies",
            all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1650_12_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1650_13_formalization_untouched",
            not formalization_dirty,
            "no 1650 outputs found under formalization-workbench",
        ),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1650_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1650 response-displacement parent-owner or Bobs source acquisition validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    z_rows: list[dict[str, object]],
    priority_rows: list[dict[str, object]],
    local_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1650 - Response Displacement Parent Owner Or Bobs Source Acquisition

**Private status:** nonclaim synthesis checkpoint. No response-displacement parent owner, reduced GK symbol match, observed flux zero, `delta_H_tau` zero, stable Hamiltonian charge, `M_H_ref`, `M_*`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, EM pass, orbital pass, or public claim is made.

## Verdict

The response-displacement route is not dead. It has real mathematical bones:

```text
1619: formal Z normal form -> F_1=0 and q_loc silence inside the constructed class
1620: exact chain-rule source-current lemma if Z is quotient-vertical and matter descends
1639: conditional local tail law q_R = Q_R c^2/(2 G M_*) = -Pi_R c^2/(2 G M_*)
1648/1649: reduced Ward/no-flux contract if Gamma_eff/K_hat/P_loc are parent-owned
```

But the parent-owner route still does **not** close for current MTS. The worktree already chased the hard clauses: verticality, constraint/no-pole origin, no vertical metric, source-slot exclusion, action-scale ownership, Pi_R boundary silence, same-frame `M_H_ref`, current ownership, and observed `B_obs`. They all remain conditional, unsigned, or source-row-only.

So `1650` makes the honest pivot: keep the derivation route alive, but stop recycling the same verticality theorem without new parent primitives. The next concrete move is an executable `B_obs` priority runner that starts filling or refusing real source rows.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Parent Signature Verdict

{markdown_table(parent_rows, ["verdict_id", "target", "required_result", "status", "effect"])}

## Response-Displacement To RAB Map

{markdown_table(z_rows, ["map_id", "object", "meaning", "status", "effect"])}

## Bobs Source Acquisition Priority

{markdown_table(priority_rows, ["priority_id", "quantity", "role", "required_next_input", "current_status", "priority_rank"])}

## Local GR Status Ledger

{markdown_table(local_rows, ["status_id", "target", "condition", "current_status", "interpretation"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

This is actually a good place to be scientifically: the local branch now has a clean theorem route and a clean fallback route. The theorem route needs new parent primitives or a real vertical-generator/constraint origin. The fallback route needs source-backed `B_obs` rows and a noncircular `M_H_ref` denominator. What we should not do is pretend the formal `Z` field already is the observed MTS residual, or pretend missing boundary/source flux is zero because it is inconvenient.
"""
    DOC.write_text(text, encoding="utf-8")


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    parent_rows = parent_verdict_rows()
    z_rows = z_map_rows()
    priority_rows = bobs_priority_rows()
    local_rows = local_status_rows()
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_target_rows()

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(PARENT_VERDICT, parent_rows)
    write_csv(Z_MAP_AUDIT, z_rows)
    write_csv(BOBS_PRIORITY, priority_rows)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(CLAIM_GATE, claim_rows)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_targets)
    copy_outputs()

    validation = validation_rows(source_rows, parent_rows, z_rows, priority_rows, local_rows, claim_rows, decisions, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, parent_rows, z_rows, priority_rows, local_rows, claim_rows, decisions, next_targets, validation)
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
