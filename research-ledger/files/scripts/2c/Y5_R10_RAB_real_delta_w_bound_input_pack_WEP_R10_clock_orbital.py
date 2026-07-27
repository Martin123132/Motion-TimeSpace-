from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1491-Y5-R10-RAB-real-delta-w-bound-input-pack-WEP-R10-clock-orbital.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1490_next": OUT / "P8_Y5_R10_1490_NEXT_TARGET.csv",
    "1490_validation": OUT / "P8_Y5_BRR545_1490_VALIDATION.csv",
    "1490_delta_requirements": OUT / "P8_Y5_R10_1490_DELTA_W_REAL_INPUT_REQUIREMENTS.csv",
    "1489_delta_interface": OUT / "P8_Y5_R10_1489_DELTA_W_BOUND_INTERFACE_NONCLAIM.csv",
    "1488_delta_lock": OUT / "P8_Y5_R10_1488_WA_DELTAW_RESIDUAL_LOCK.csv",
    "1479_bound_anchor_pack": OUT / "P8_Y5_R10_1479_DELTA_W_BOUND_ANCHOR_PACK_NONCLAIM.csv",
    "1479_bound_requirements": OUT / "P8_Y5_R10_1479_DELTA_W_BOUND_INPUT_REQUIREMENTS.csv",
    "1480_wep_input_matrix": OUT / "P8_Y5_R10_1480_SAME_BRANCH_WEP_DELTA_W_INPUT_MATRIX.csv",
    "1480_wep_smoke": OUT / "P8_Y5_R10_1480_SAME_BRANCH_WEP_DELTA_W_SMOKE_RESULTS_NONCLAIM.csv",
    "1438_microscope_manifest": OUT / "P8_Y5_R10_1438_OFFICIAL_MICROSCOPE_SOURCE_PACK_MANIFEST.csv",
    "1482_microscope_directory": OUT / "P8_Y5_R10_1482_MICROSCOPE_INTAKE_DIRECTORY_STATUS.csv",
    "1070_microscope_external": OUT / "P8_Y5_R10_1070_EXTERNAL_MICROSCOPE_READOUT_SOURCE_LEDGER.csv",
    "1070_orbit_kernel": OUT / "P8_Y5_R10_1070_ORBIT_KERNEL_SOURCE_ROWS.csv",
    "1084_microscope_gate": OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
    "1066_delta_bound_import": OUT / "P8_Y5_R10_1066_WEP_DELTA_W_BOUND_IMPORT.csv",
    "1066_delta_prior_schema": OUT / "P8_Y5_R10_1066_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv",
    "1321_clock_bound_import": OUT / "P8_Y5_R10_1321_CLOCK_BOUND_IMPORT.csv",
    "1051_clock_product": OUT / "P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv",
    "988_clock_product": OUT / "P8_Y5_R10_988_CLOCK_PRODUCT_IMPORT.csv",
    "gauss_orbital_calibration": OUT / "P8_Y5_GAUSS_ORBITAL_CALIBRATION_CHAIN.csv",
    "701_orbit_bridge": OUT / "P8_Y5_R10_701_GAUSS_ORBIT_BRIDGE_GATE.csv",
    "778_readout_candidate": OUT / "P8_Y5_R10_778_EM_CLOCK_ORBIT_READOUT_INPUT_CANDIDATE.csv",
    "local_bounds": LOCAL_BOUNDS,
}

C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1491_SOURCE_REGISTER.csv"
BOUND_ANCHORS = OUT / "P8_Y5_R10_1491_DELTA_W_BOUND_ANCHORS.csv"
INPUT_PACK = OUT / "P8_Y5_R10_1491_REAL_DELTA_W_INPUT_PACK_NONCLAIM.csv"
PROJECTION_REQUIREMENTS = OUT / "P8_Y5_R10_1491_ARENA_PROJECTION_REQUIREMENTS.csv"
CALIBRATION_GATES = OUT / "P8_Y5_R10_1491_COMMON_CALIBRATION_NO_CANCELLATION_GATES.csv"
READINESS_MATRIX = OUT / "P8_Y5_R10_1491_DELTA_W_READINESS_MATRIX.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1491_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1491_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1491_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1491_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1491_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1491_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1491"
QUAR_INPUTS = QUARANTINE / "REAL_DELTA_W_INPUT_PACK_NONCLAIM.csv"
QUAR_ANCHORS = QUARANTINE / "DELTA_W_BOUND_ANCHORS_NONCLAIM.csv"
QUAR_REQUIREMENTS = QUARANTINE / "ARENA_PROJECTION_REQUIREMENTS_NONCLAIM.csv"
BRANCH_INPUTS = BRANCH_RESIDUALS / "real_delta_w_input_pack_nonclaim_1491.csv"
BRANCH_ANCHORS = BRANCH_RESIDUALS / "delta_w_bound_anchors_nonclaim_1491.csv"
BRANCH_REQUIREMENTS = BRANCH_RESIDUALS / "arena_projection_requirements_nonclaim_1491.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def false_flags() -> dict[str, bool]:
    return {
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def source_rows() -> list[dict[str, Any]]:
    usage = {
        "1490_next": "authoritative 1491 handoff",
        "1490_validation": "previous validation state",
        "1490_delta_requirements": "real delta_w input requirements",
        "1489_delta_interface": "delta_w bound-interface skeleton",
        "1488_delta_lock": "symbolic delta_w residual lock",
        "1479_bound_anchor_pack": "older bound anchors and why nonclaim",
        "1479_bound_requirements": "delta_w missing input requirements",
        "1480_wep_input_matrix": "same-branch WEP input matrix",
        "1480_wep_smoke": "quarantined WEP delta_w smoke rows",
        "1438_microscope_manifest": "official MICROSCOPE source-pack manifest",
        "1482_microscope_directory": "MICROSCOPE intake directory status",
        "1070_microscope_external": "source-backed MICROSCOPE readout/source ledger",
        "1070_orbit_kernel": "partial orbit/readout kernel rows",
        "1084_microscope_gate": "MICROSCOPE official readout import gate",
        "1066_delta_bound_import": "WEP delta_w bound anchor import",
        "1066_delta_prior_schema": "delta_w prior-width schema",
        "1321_clock_bound_import": "clock product bound import",
        "1051_clock_product": "clock product source URLs and bounds",
        "988_clock_product": "clock product imported comparison rows",
        "gauss_orbital_calibration": "orbital/Newton calibration chain",
        "701_orbit_bridge": "Gauss/orbit bridge gate",
        "778_readout_candidate": "clock/orbit readout candidate placeholders",
        "local_bounds": "local empirical bound anchor table",
    }
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": f"SRC1491_{index}_{key}",
            "path_or_url": rel(path),
            "source_kind": "local_file",
            "exists_or_resolved": path.exists(),
            "usage": usage[key],
            **false_flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def bound_anchor_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "anchor_id": "BAN1491_0_MICROSCOPE_TiPt",
            "arena": "WEP_MICROSCOPE_TiPt",
            "observable": "eta_TiPt / delta_w source-weight contrast anchor",
            "bound_value": "2.8e-15",
            "bound_units": "dimensionless",
            "bound_status": "SOURCE_BACKED_BOUND_ANCHOR_AVAILABLE",
            "source_path": rel(LOCAL_BOUNDS),
            "source_anchor": "R1_WEP_source_charge;EXT1070_6_PRL_eta_bound_anchor",
            "source_url_or_doi": "https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102",
            "why_nonclaim": "official eta bound exists, but C_parent/source vector/material tensor/K_CMSM/product convention/tau_eff remain missing",
            "source_backed_bound": True,
            "score_ready": False,
            **false_flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "anchor_id": "BAN1491_1_EotWash_WEP",
            "arena": "WEP_EotWash_material_pairs",
            "observable": "torsion-balance composition contrast",
            "bound_value": "MISSING_SOURCE_BACKED_BOUND",
            "bound_units": "dimensionless",
            "bound_status": "LOCAL_SOURCE_ACQUISITION_REQUIRED",
            "source_path": "MISSING_EOTWASH_WEP_SOURCE_PATH",
            "source_anchor": "MISSING_EOTWASH_MATERIAL_PAIR_ROW",
            "source_url_or_doi": "MISSING_EOTWASH_WEP_REFERENCE",
            "why_nonclaim": "no local EotWash WEP material/source vector and eta row is available in this workspace yet",
            "source_backed_bound": False,
            "score_ready": False,
            **false_flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "anchor_id": "BAN1491_2_R10_short_range",
            "arena": "R10_short_range_inverse_square",
            "observable": "alpha(lambda) bound curve",
            "bound_value": "alpha(lambda)",
            "bound_units": "range-dependent",
            "bound_status": "SYMBOLIC_CURVE_ANCHOR_ONLY",
            "source_path": rel(LOCAL_BOUNDS),
            "source_anchor": "R10_fifth_force",
            "source_url_or_doi": "https://arxiv.org/abs/hep-ph/0307284; doi:10.1146/annurev.nucl.53.041002.110503",
            "why_nonclaim": "review/source anchor exists, but no promoted digitized alpha(lambda) curve, lambda convention, or delta_w kernel is loaded",
            "source_backed_bound": False,
            "score_ready": False,
            **false_flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "anchor_id": "BAN1491_3_clock_product",
            "arena": "clock_alpha_mass",
            "observable": "|b_alpha * tau_clock_time| best imported product",
            "bound_value": "2.1e-18",
            "bound_units": "yr^-1",
            "bound_status": "SOURCE_BACKED_PRODUCT_BOUND_AVAILABLE",
            "source_path": rel(OUT / "P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv"),
            "source_anchor": "BAP1051_2_best_current_product;CBI1321_2",
            "source_url_or_doi": "https://oar.ptb.de/resources/show/10.7795/110.20211216; https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2023.1104848/full",
            "why_nonclaim": "clock row bounds a product; tau_clock/source-coefficient split and delta_w projection are missing",
            "source_backed_bound": True,
            "score_ready": False,
            **false_flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "anchor_id": "BAN1491_4_orbital_Gdot",
            "arena": "orbital_GM_time_drift",
            "observable": "Gdot/G source-calibration anchor",
            "bound_value": "9.6e-15",
            "bound_units": "yr^-1",
            "bound_status": "SOURCE_BACKED_BOUND_ANCHOR_AVAILABLE",
            "source_path": rel(LOCAL_BOUNDS),
            "source_anchor": "R9_Gdot;GOB701;CAL523",
            "source_url_or_doi": "doi:10.3390/universe7020034",
            "why_nonclaim": "orbital/GM bound anchor exists, but worldtube source map, measured-GM convention, and delta_w projection are missing",
            "source_backed_bound": True,
            "score_ready": False,
            **false_flags(),
        },
    ]


def input_pack_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DWI1491_0_core_model",
            "core",
            "delta_w_vector",
            "eta_AB ~= sum_i DeltaQ_i(AB) * delta_w_i * tau_i",
            "MISSING_PARENT_COMPONENT_BASIS",
            "MISSING",
            "MISSING",
            "MISSING",
            "parent component basis, covariance/no-cancellation policy, same-branch convention",
        ),
        (
            "DWI1491_1_MICROSCOPE_TiPt",
            "WEP_MICROSCOPE_TiPt",
            "delta_w_TiPt",
            "|eta_TiPt| <= |DeltaQ_TiPt dot delta_w| * |tau_WEP|",
            "BOUND_ANCHOR_AVAILABLE_PROJECTION_BLOCKED",
            "2.8e-15",
            "dimensionless",
            rel(LOCAL_BOUNDS),
            "official readout arrays, source worldtube, full material tensor, product convention, tau_eff",
        ),
        (
            "DWI1491_2_EotWash_WEP",
            "WEP_EotWash_material_pairs",
            "delta_w_EotWash_AB",
            "|eta_AB| <= |DeltaQ_AB dot delta_w| * |tau_EotWash|",
            "SOURCE_ACQUISITION_REQUIRED",
            "MISSING_SOURCE_BACKED_BOUND",
            "dimensionless",
            "MISSING_EOTWASH_WEP_SOURCE_PATH",
            "published eta bound, material/source composition vectors, attractor/source map, range/profile transfer",
        ),
        (
            "DWI1491_3_R10",
            "R10_short_range",
            "delta_w_R10(lambda)",
            "alpha_delta_w(lambda) = K_R10(lambda) * DeltaQ_source_test(lambda) dot delta_w",
            "SYMBOLIC_ANCHOR_ONLY_CURVE_KERNEL_MISSING",
            "alpha(lambda)",
            "range-dependent",
            rel(LOCAL_BOUNDS),
            "promoted digitized alpha(lambda) curve, lambda convention, Yukawa/non-Yukawa kernel, source/test composition",
        ),
        (
            "DWI1491_4_clock",
            "clock_alpha_mass",
            "delta_w_clock_product",
            "|clock product| <= |K_clock dot delta_w| * |tau_clock| plus alpha/mass split",
            "PRODUCT_BOUND_AVAILABLE_PROJECTION_BLOCKED",
            "2.1e-18",
            "yr^-1",
            rel(OUT / "P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv"),
            "tau_clock, clock readout kernel, alpha/mass/source-coefficient split, no cross-arena transfer proof",
        ),
        (
            "DWI1491_5_orbital",
            "orbital_GM_time_drift",
            "delta_w_orbital",
            "|d ln GM/dt| or source calibration residual <= projection(delta_w)",
            "BOUND_ANCHOR_AVAILABLE_PROJECTION_BLOCKED",
            "9.6e-15",
            "yr^-1",
            rel(LOCAL_BOUNDS),
            "source body composition, worldtube/Gauss bridge, measured GM convention, orbital residual projection",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": input_id,
            "arena": arena,
            "symbol": symbol,
            "formula": formula,
            "current_status": status,
            "bound_or_value": value,
            "units": units,
            "source_path": source_path,
            "missing_for_claim": missing,
            "score_ready": False,
            **false_flags(),
        }
        for input_id, arena, symbol, formula, status, value, units, source_path, missing in rows
    ]


def projection_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("APR1491_0_component_basis", "all_arenas", "parent delta_w component basis", "MISSING_PARENT_COUPLING_BASIS", "same basis across WEP/R10/clock/orbital"),
        ("APR1491_1_material_source", "WEP/R10", "material/source response vectors", "PARTIAL_OR_MISSING", "Ti/Pt full tensor, EotWash material pairs, R10 source/test composition"),
        ("APR1491_2_tau_projection", "all_arenas", "arena tau/projection kernels", "MISSING_ARENA_PROJECTIONS", "tau_WEP, tau_R10(lambda), tau_clock, orbital/worldtube projection"),
        ("APR1491_3_readout", "MICROSCOPE/clock/orbital", "official readout kernels", "MISSING_OR_PARTIAL", "CMSM arrays, clock readout functional, measured GM convention"),
        ("APR1491_4_R10_curve", "R10", "digitized alpha(lambda) bound curve", "MISSING_PROMOTED_CURVE_AND_KERNEL", "full curve or machine-readable table with lambda convention"),
        ("APR1491_5_no_cancellation", "all_arenas", "covariance/no-cancellation envelope", "MISSING_NO_CANCELLATION_ENVELOPE", "norm/covariance policy before comparing multi-component vectors"),
        ("APR1491_6_same_branch", "all_arenas", "same-branch convention lock", "MISSING_SAME_BRANCH_PRODUCT_CONVENTION", "C_parent/source/material/readout/bound must share units/sign/basis"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": requirement_id,
            "arena": arena,
            "required_object": required_object,
            "current_status": current_status,
            "acceptance_rule": acceptance_rule,
            **false_flags(),
        }
        for requirement_id, arena, required_object, current_status, acceptance_rule in rows
    ]


def calibration_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG1491_0_common_mode", "common w_star calibration", "guarded", "w_star is not a WEP signal only if species/time/range/frame/source-body silent"),
        ("CG1491_1_delta_definition", "delta_w_A = w_A - w_star", "locked", "all arena rows compare relative source weights, not common calibration"),
        ("CG1491_2_no_cancellation", "no tuned vector cancellation", "active_block", "component products must pass by norm/covariance or parent identity, not cherry-picked cancellation"),
        ("CG1491_3_same_branch", "same branch product", "active_block", "do not mix DD smoke, MICROSCOPE surrogate, and parent basis rows as one claim"),
        ("CG1491_4_cross_arena", "no cross-arena transfer", "active_block", "clock product bound cannot become WEP/R10 bound without a projection theorem"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "current_status": status,
            "rule": rule,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, status, rule in rows
    ]


def readiness_rows() -> list[dict[str, Any]]:
    rows = [
        ("RDY1491_0_MICROSCOPE", "WEP_MICROSCOPE_TiPt", True, False, "bound anchor exists; official readout/material/source/product convention missing"),
        ("RDY1491_1_EotWash", "WEP_EotWash_material_pairs", False, False, "local source-backed WEP material-pair bound row missing"),
        ("RDY1491_2_R10", "R10_short_range", False, False, "symbolic alpha(lambda) anchor only; curve/kernel missing"),
        ("RDY1491_3_clock", "clock_alpha_mass", True, False, "product bound exists; tau/readout/alpha-mass-source split missing"),
        ("RDY1491_4_orbital", "orbital_GM_time_drift", True, False, "Gdot/GM anchor exists; worldtube/orbital projection missing"),
        ("RDY1491_5_overall", "all_arenas", False, False, "no arena has all bound, source vector, projection kernel, units, and same-branch lock"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "readiness_id": readiness_id,
            "arena": arena,
            "source_backed_bound_anchor_available": anchor_available,
            "score_ready": score_ready,
            "status_detail": status_detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for readiness_id, arena, anchor_available, score_ready, status_detail in rows
    ]


def c_parent_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "CPR1491_0_live_import",
            "forbidden_object": rel(C_PARENT_IMPORT),
            "exists": C_PARENT_IMPORT.exists(),
            "current_status": "ABSENT_OK" if not C_PARENT_IMPORT.exists() else "ERROR_LIVE_IMPORT_PRESENT",
            "reason": "1491 is a residual-bound input pack, not a coupling theorem or C_parent zero/import",
            "action_taken": "no C_parent import written",
            "parent_signed": False,
            **false_flags(),
        }
    ]


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("LRS1491_0_delta_w", "delta_w residual branch", "nonclaim input pack built", "INPUTS_STAGED_NOT_SCORE_READY", "source-backed anchors are partial; projections missing", "coupling still not theorem-zero"),
        ("LRS1491_1_WEP", "WEP/MICROSCOPE", "eta anchor available", "BOUND_ANCHOR_ONLY", "official source/readout/material/product kernels missing", "WEP claim blocked"),
        ("LRS1491_2_R10", "short-range/R10", "symbolic curve anchor", "CURVE_KERNEL_MISSING", "promoted alpha(lambda) curve and kernel missing", "R10 claim blocked"),
        ("LRS1491_3_clock_orbit", "clock/orbital", "product/bound anchors available", "PROJECTION_MISSING", "tau/readout/worldtube maps missing", "cannot transfer to local-GR coupling"),
        ("LRS1491_4_verdict", "local GR/Newton status", "empirical residual branch staged", "NOT_CLOSED_NEXT_SOURCE_ACQUISITION_RUNNER", "real EotWash/R10/MICROSCOPE source files and kernels needed", "no local-GR/Newton/WEP/R10 claim from 1491"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "target": target,
            "evidence_status": evidence_status,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            "claim_effect": claim_effect,
            "parent_signed": False,
            **false_flags(),
        }
        for status_id, target, evidence_status, current_status, missing_for_claim, claim_effect in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1491_0_theorem", "COUPLING_THEOREM_NOT_DERIVED", "delta_w remains a residual branch, not theorem-zero"),
        ("REJ1491_1_projection", "ARENA_PROJECTIONS_MISSING", "tau/readout/worldtube kernels are missing or partial"),
        ("REJ1491_2_EotWash", "EOTWASH_SOURCE_ACQUISITION_REQUIRED", "no local EotWash WEP source-backed bound row exists"),
        ("REJ1491_3_R10", "R10_CURVE_KERNEL_MISSING", "alpha(lambda) is symbolic and not promoted"),
        ("REJ1491_4_MICROSCOPE", "MICROSCOPE_OFFICIAL_FILES_MISSING", "official arrays/source/product/full material tensor missing"),
        ("REJ1491_5_clock", "CLOCK_PRODUCT_NOT_DELTA_W", "clock bounds product terms only and cannot transfer without projection"),
        ("REJ1491_6_orbit", "ORBITAL_WORLDTUBE_MAP_MISSING", "Gdot/GM anchor lacks delta_w source projection"),
        ("REJ1491_7_Cparent", "C_PARENT_IMPORT_FORBIDDEN", "no coupling theorem/import allowed"),
        ("REJ1491_8_claim", "CLAIM_PROMOTION_FORBIDDEN", "no WEP/local-GR/Newton/R10 claim allowed"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "blocking_marker": marker,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rejection_id, marker, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1491_0_bound_pack", "keep delta_w pack nonclaim", "anchors are partial and projections are missing", "do not run score/comparison yet"),
        ("DEC1491_1_source_priority", "prioritize source acquisition", "EotWash WEP and R10 curve are the largest source gaps", "build acquisition ledger for EotWash/R10/MICROSCOPE official files"),
        ("DEC1491_2_MICROSCOPE", "retain MICROSCOPE as strongest bound anchor", "2.8e-15 anchor exists but official kernels are missing", "fill official files/product convention before claim-grade WEP run"),
        ("DEC1491_3_no_transfer", "do not transfer clock/orbital anchors to WEP", "cross-arena projections are not derived", "keep each arena separate until tau maps exist"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1491_0_1492",
            "next_target": "1492-Y5-R10-RAB-delta-w-source-acquisition-ledger-EotWash-R10-MICROSCOPE.md",
            "script": "scripts/Y5_R10_RAB_delta_w_source_acquisition_ledger_EotWash_R10_MICROSCOPE.py",
            "objective": "acquire or ledger real source files for EotWash WEP material-pair bounds, R10 alpha(lambda) curve, and MICROSCOPE official readout/source/product files before any delta_w scoring",
            "include": "source URLs/DOIs; local target paths; required columns; extraction method; confidence; valid_for_claim gates",
            "exclude": "GitHub action; formalization-workbench edits; C_parent import; theorem-zero coupling claim; numeric WEP claim without full projections",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        BOUND_ANCHORS,
        INPUT_PACK,
        PROJECTION_REQUIREMENTS,
        CALIBRATION_GATES,
        READINESS_MATRIX,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(INPUT_PACK, QUAR_INPUTS)
    shutil.copyfile(BOUND_ANCHORS, QUAR_ANCHORS)
    shutil.copyfile(PROJECTION_REQUIREMENTS, QUAR_REQUIREMENTS)
    shutil.copyfile(INPUT_PACK, BRANCH_INPUTS)
    shutil.copyfile(BOUND_ANCHORS, BRANCH_ANCHORS)
    shutil.copyfile(PROJECTION_REQUIREMENTS, BRANCH_REQUIREMENTS)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows() -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    anchors = read_csv(BOUND_ANCHORS)
    inputs = read_csv(INPUT_PACK)
    requirements = read_csv(PROJECTION_REQUIREMENTS)
    calibration = read_csv(CALIBRATION_GATES)
    readiness = read_csv(READINESS_MATRIX)
    c_parent = read_csv(C_PARENT_REFUSAL)
    local = read_csv(LOCAL_STATUS)
    rejections = read_csv(REJECTION_LEDGER)
    decisions = read_csv(DECISION_LEDGER)
    next_rows = read_csv(NEXT_TARGET)

    checks: list[tuple[str, bool, str]] = [
        ("VAL1491_0_sources", all(row["exists_or_resolved"].lower() == "true" for row in sources), "all cited local source paths exist"),
        ("VAL1491_1_anchor_rows", len(anchors) == 5, "five arena anchor rows written"),
        (
            "VAL1491_2_source_backed_paths",
            all(row["source_path"] != "MISSING_EOTWASH_WEP_SOURCE_PATH" for row in anchors if row["source_backed_bound"].lower() == "true"),
            "source-backed anchors have local source paths",
        ),
        (
            "VAL1491_3_missing_rows_nonclaim",
            all(row["claim_allowed"].lower() == "false" for row in anchors if "MISSING" in row["bound_value"] or row["bound_status"].startswith("SYMBOLIC")),
            "missing/symbolic anchors remain nonclaim",
        ),
        (
            "VAL1491_4_input_pack_nonclaim",
            all(row["score_ready"].lower() == "false" and row["claim_allowed"].lower() == "false" for row in inputs),
            "all delta_w input rows are nonclaim and not score-ready",
        ),
        (
            "VAL1491_5_projection_requirements_open",
            any(row["current_status"] == "MISSING_ARENA_PROJECTIONS" for row in requirements),
            "arena projection requirements remain open",
        ),
        (
            "VAL1491_6_calibration_gates",
            any(row["current_status"] == "active_block" for row in calibration),
            "common calibration/no-cancellation gates are active",
        ),
        (
            "VAL1491_7_overall_not_ready",
            any(row["readiness_id"] == "RDY1491_5_overall" and row["score_ready"].lower() == "false" for row in readiness),
            "overall delta_w branch is not score-ready",
        ),
        (
            "VAL1491_8_no_Cparent_import",
            (not C_PARENT_IMPORT.exists()) and all(row["claim_allowed"].lower() == "false" for row in c_parent),
            "live C_parent import remains absent and refused",
        ),
        (
            "VAL1491_9_local_blocked",
            any(row["current_status"] == "NOT_CLOSED_NEXT_SOURCE_ACQUISITION_RUNNER" for row in local),
            "local GR/Newton/WEP remains blocked pending source acquisition",
        ),
        (
            "VAL1491_10_rejections",
            len(rejections) >= 8 and all(row["claim_allowed"].lower() == "false" for row in rejections),
            "rejection ledger blocks claim promotion",
        ),
        (
            "VAL1491_11_decisions",
            any(row["decision_id"] == "DEC1491_1_source_priority" for row in decisions),
            "decision ledger prioritizes source acquisition",
        ),
        (
            "VAL1491_12_next",
            len(next_rows) == 1 and next_rows[0]["next_id"] == "NEXT1491_0_1492",
            "1492 handoff written",
        ),
        ("VAL1491_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1491 CSVs parse cleanly"),
        (
            "VAL1491_14_branch_copies",
            all(path.exists() for path in [QUAR_INPUTS, QUAR_ANCHORS, QUAR_REQUIREMENTS, BRANCH_INPUTS, BRANCH_ANCHORS, BRANCH_REQUIREMENTS]),
            "branch/quarantine nonclaim copies written",
        ),
    ]
    remove_pycache()
    checks.append(("VAL1491_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"))
    modified_count = formalization_modified_count()
    checks.append(("VAL1491_16_formalization_untouched", modified_count == 0, f"formalization modified-file count since start={modified_count}"))
    claim_paths = generated_csvs() + [QUAR_INPUTS, QUAR_ANCHORS, QUAR_REQUIREMENTS, BRANCH_INPUTS, BRANCH_ANCHORS, BRANCH_REQUIREMENTS]
    claim_flags_false = True
    for path in claim_paths:
        for row in read_csv(path):
            for flag in ("valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if flag in row and row[flag].lower() != "false":
                    claim_flags_false = False
    checks.append(("VAL1491_17_claim_flags_false", claim_flags_false, "all prediction/claim flags remain false"))
    overall = all(result for _, result, _ in checks)
    checks.append(("VAL1491_18_overall", overall, "1491 builds a nonclaim source-backed delta_w input pack and hands off to source acquisition"))
    return [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": utc_now(),
        }
        for check_id, result, detail in checks
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("|", "/") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    anchors = read_csv(BOUND_ANCHORS)
    inputs = read_csv(INPUT_PACK)
    requirements = read_csv(PROJECTION_REQUIREMENTS)
    calibration = read_csv(CALIBRATION_GATES)
    readiness = read_csv(READINESS_MATRIX)
    local = read_csv(LOCAL_STATUS)
    rejections = read_csv(REJECTION_LEDGER)
    decisions = read_csv(DECISION_LEDGER)
    validation = read_csv(VALIDATION)
    next_rows = read_csv(NEXT_TARGET)

    lines = [
        "# 1491 - Real delta w Bound Input Pack: WEP, R10, Clock, Orbital",
        "",
        "## Verdict",
        "- `delta_w` is now staged as an empirical residual branch, not a theorem-zero coupling claim.",
        "- MICROSCOPE, clocks, and orbital/Gdot have useful source-backed bound anchors; EotWash WEP and R10 still need source acquisition or curve/kernel promotion.",
        "- No arena is score-ready because component basis, projection kernels, same-branch convention, and no-cancellation policy are still missing.",
        "",
        "## Bound Anchors",
        markdown_table(anchors, ["anchor_id", "arena", "bound_status", "bound_value", "why_nonclaim"]),
        "",
        "## Delta w Input Pack",
        markdown_table(inputs, ["input_id", "arena", "current_status", "bound_or_value", "missing_for_claim"]),
        "",
        "## Projection Requirements",
        markdown_table(requirements, ["requirement_id", "arena", "current_status", "acceptance_rule"]),
        "",
        "## Calibration Gates",
        markdown_table(calibration, ["gate_id", "gate", "current_status", "rule"]),
        "",
        "## Readiness Matrix",
        markdown_table(readiness, ["readiness_id", "arena", "source_backed_bound_anchor_available", "score_ready", "status_detail"]),
        "",
        "## Local GR/Newton Status",
        markdown_table(local, ["status_id", "target", "current_status", "claim_effect"]),
        "",
        "## Rejection Ledger",
        markdown_table(rejections, ["rejection_id", "blocking_marker", "reason"]),
        "",
        "## Decision Ledger",
    ]
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} - {row['next_action']}.")
    lines.extend(
        [
            "",
            "## Validation",
            markdown_table(validation, ["check_id", "result", "detail"]),
            "",
            "## Next Target",
            markdown_table(next_rows, ["next_id", "next_target", "script", "objective"]),
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(BOUND_ANCHORS, bound_anchor_rows())
    write_csv(INPUT_PACK, input_pack_rows())
    write_csv(PROJECTION_REQUIREMENTS, projection_requirement_rows())
    write_csv(CALIBRATION_GATES, calibration_gate_rows())
    write_csv(READINESS_MATRIX, readiness_rows())
    write_csv(C_PARENT_REFUSAL, c_parent_refusal_rows())
    write_csv(LOCAL_STATUS, local_status_rows())
    write_csv(REJECTION_LEDGER, rejection_rows())
    write_csv(DECISION_LEDGER, decision_rows())
    write_csv(NEXT_TARGET, next_target_rows())
    copy_outputs()
    write_csv(VALIDATION, validation_rows())
    write_doc()
    remove_pycache()
    print(f"Wrote {DOC}")
    print(f"Wrote {VALIDATION}")


if __name__ == "__main__":
    main()
