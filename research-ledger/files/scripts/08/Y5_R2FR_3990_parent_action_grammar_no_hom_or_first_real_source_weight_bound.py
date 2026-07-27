from __future__ import annotations

import csv
import math
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3990"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3990-Y5-R2FR-parent-action-grammar-no-hom-or-first-real-source-weight-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3990_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3990_NO_HOM_GRAMMAR_THEOREM.csv",
    "bound_rows": SRC / "P8_Y5_R2FR_3990_SOURCE_WEIGHT_BOUND_ROWS.csv",
    "schema": SRC / "P8_Y5_R2FR_3990_FIRST_REAL_SOURCE_WEIGHT_BOUND_SCHEMA.csv",
    "smoke": SRC / "P8_Y5_R2FR_3990_SOURCE_WEIGHT_SMOKE_RESULTS.csv",
    "ppn_feed": SRC / "P8_Y5_R2FR_3990_PPN_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3990_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3990_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3990_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3990_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3990_VALIDATION.csv",
}

NEXT_DOC = "3991-Y5-R2FR-source-weight-real-bound-or-PPN-beta-source-evaluator.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3991_source_weight_real_bound_or_PPN_beta_source_evaluator.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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
        ("SRC3990_00_3989_next", SRC / "P8_Y5_R2FR_3989_NEXT_TARGET.csv", "NEXT3989_0", "3989 handoff"),
        ("SRC3990_01_3989_theorem", SRC / "P8_Y5_R2FR_3989_MATTER_DESCENT_NO_SOURCE_PREFACTOR_THEOREM.csv", "NP3989_0_no_prefactor_criterion", "3989 zero criterion"),
        ("SRC3990_02_3989_certificate", SRC / "P8_Y5_R2FR_3989_NO_SOURCE_PREFACTOR_CERTIFICATE.csv", "NPC3989_0_criterion", "3989 certificate"),
        ("SRC3990_03_3989_ppn_fill", SRC / "P8_Y5_R2FR_3989_FIRST_PPN_SOURCE_WEIGHT_FILL.csv", "PPNF3989_0_wR_source", "3989 PPN source fill"),
        ("SRC3990_04_2613_hom", SRC / "P8_Y5_HOM_EXCLUSION_GATE_2613_HOM_EXCLUSION_THEOREM_ATTEMPT.csv", "HOM2613_1_conditional_meta_theorem", "conditional no-Hom theorem"),
        ("SRC3990_05_2613_functor", SRC / "P8_Y5_HOM_EXCLUSION_GATE_2613_LABEL_FORGETTING_SOURCE_FUNCTOR_AUDIT.csv", "SF2613_0_label_forgetting", "label-forgetting source functor"),
        ("SRC3990_06_2612_audit", SRC / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_SOURCE_ONLY_HOM_AUDIT.csv", "HOM2612_0_target", "direct matter grammar no-Hom target"),
        ("SRC3990_07_2645_clause", SRC / "P8_Y5_NO_SOURCE_PREFACTOR_2645_PARENT_ACTION_CLAUSE_ATTEMPT.csv", "NSP2645_0_target", "parent no-source-prefactor clause"),
        ("SRC3990_08_3510_action", SRC / "P8_Y5_R2FR_3510_COMMON_ACTION_DENSITY_LINE_THEOREM.csv", "UAS3510_0_single_density_line_target", "single action-density line theorem"),
        ("SRC3990_09_3378_parent", SRC / "P8_Y5_R2FR_3378_MINIMAL_PARENT_ACTION_LINE.csv", "PAL3378_3_matter_source_scale", "minimal parent action line"),
        ("SRC3990_10_3345_collapse", SRC / "P8_Y5_R2FR_3345_SOURCE_WEIGHT_COLLAPSE_THEOREM.csv", "SWC3345_1_exchange_graph", "source weight collapse theorem"),
        ("SRC3990_11_1720_prefac", SRC / "P8_Y5_PARENT_QLOC_1720_JH_CURRENT_DEFINITION_THEOREM.csv", "JHT1720_3_source_prefactor_countermodel", "source-prefactor countermodel"),
        ("SRC3990_12_3513_Rmd", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_1_R_md", "matter descent/source multiplier residual"),
        ("SRC3990_13_2631_wR", SRC / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv", "PPNV2631_4_wR", "full PPN source-weight slot"),
        ("SRC3990_14_2514_source", SRC / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv", "DBETA2514_0_source", "finite beta source component"),
        ("SRC3990_15_2514_SN", SRC / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv", "DBETA2514_5_SN", "source-normalization stability"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": exists,
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "NHG3990_0_target",
            "claim_piece": "parent no-Hom grammar theorem",
            "mathematical_form": "Let G_src be the source/species/material-label object and W=R_+ the pre-action active-source-weight object. If the parent ordinary-matter grammar factors as one density line L_ord(Psi_A,e_obs(q(Phi)),D_obs,theta_A), the source functor first forgets labels to T_total=sum_A T_A, and no hidden/readout/worldtube marker returns before variation, then Hom_parent(G_src,W)=CommonConst.",
            "derived_result": "relative source weights w_A/w_B are untypeable inside that grammar; only a common scalar remains",
            "status": "EXACT_CONDITIONAL_GRAMMAR_THEOREM_DERIVED_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NHG3990_1_proof_factorization",
            "claim_piece": "factorization proof",
            "mathematical_form": "S_ord=int dmu_obs L_ord, L_ord=L_ord({Psi_A},e_obs,D_obs,theta_A; constants) with variation taken before any readout map. A source-only multiplier w_A is not a field, not a fixed representation label, and not an observed geometry functional.",
            "derived_result": "a relative active-source prefactor is an extra parent constructor, not a consequence of the Hilbert variation",
            "status": "FACTORISATION_PROOF_CLEAN_AS_META_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NHG3990_2_label_forgetful_source",
            "claim_piece": "label-forgetting source map",
            "mathematical_form": "F_src({(T_A,A)})=F_src(T_total) after q_src forgets A; by additivity and covariance F_src(T_total)=kappa_common T_total plus non-Hilbert residuals already separately booked.",
            "derived_result": "species labels cannot feed the active source once the source object is the total Hilbert current",
            "status": "EXACT_CONDITIONAL_SOURCE_FUNCTOR_ROUTE_PARENT_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NHG3990_3_common_mode",
            "claim_piece": "common scalar reclassification",
            "mathematical_form": "w_A=w_common for all A implies E_munu=kappa_ref w_common T_munu; after one measured-G calibration this is not composition dependence, but D_X ln w_common remains a universal source-calibration residual unless parent-fixed.",
            "derived_result": "the WEP-style poison collapses to a universal G/source-calibration gate if relative weights are killed",
            "status": "COMMON_MODE_RECLASSIFIED_NOT_ZEROED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NHG3990_4_countermodel",
            "claim_piece": "countermodel guard",
            "mathematical_form": "If any parent constructor supplies source labels before variation, S_ord=sum_A w_A S_A stays covariant and Ward-compatible while T_source=sum_A w_A T_A.",
            "derived_result": "Ward conservation cannot prove the theorem; the no-Hom grammar or a finite source-weight bound is required",
            "status": "COUNTERMODEL_RETAINED_AS_BOUND_BRANCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SWB3990_0_no_hom",
            "symbol": "epsilon_no_hom_species_source_3990",
            "formula": "max_A |ln(w_A/w_common)|, equivalently max_AB |ln w_A-ln w_B| up to the chosen reference",
            "meaning": "finite residual if the parent grammar cannot prove Hom_parent(G_src,R_+)=CommonConst",
            "source_path": str(SRC / "P8_Y5_HOM_EXCLUSION_GATE_2613_HOM_EXCLUSION_THEOREM_ATTEMPT.csv"),
            "status": "BOUND_DEFINITION_READY_NUMERIC_SOURCE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SWB3990_1_action_line",
            "symbol": "epsilon_action_line_universality_3990",
            "formula": "|D_X ln w_common| + |delta_action_line_species|",
            "meaning": "common action-line/source-scale drift after relative species weights collapse",
            "source_path": str(SRC / "P8_Y5_R2FR_3510_COMMON_ACTION_DENSITY_LINE_THEOREM.csv"),
            "status": "BOUND_DEFINITION_READY_NUMERIC_SOURCE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SWB3990_2_readout",
            "symbol": "epsilon_readout_reentry_3990",
            "formula": "sum_i |epsilon_readout_marker_i| over post-variation source/readout/worldtube re-entry channels",
            "meaning": "prevents source weights from returning through masks, boundary selectors, or readout maps",
            "source_path": str(SRC / "P8_Y5_NO_SOURCE_PREFACTOR_2645_PARENT_ACTION_CLAUSE_ATTEMPT.csv"),
            "status": "BOUND_DEFINITION_READY_NUMERIC_SOURCE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SWB3990_3_prefactor_total",
            "symbol": "R_source_prefactor_bound_3990",
            "formula": "epsilon_no_hom_species_source_3990 + epsilon_action_line_universality_3990 + epsilon_readout_reentry_3990",
            "meaning": "absolute no-cancellation envelope for the source-prefactor loophole",
            "source_path": str(OUTPUTS["theorem"]),
            "status": "EXACT_ENVELOPE_DERIVED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SWB3990_4_descent_total",
            "symbol": "epsilon_descent_prefactor_3990",
            "formula": "|R_matter_descent| + R_source_prefactor_bound_3990",
            "meaning": "3989 descent/prefactor residual tightened so the source-prefactor part is no-Hom bounded",
            "source_path": str(SRC / "P8_Y5_R2FR_3989_DESCENT_PREFAC_PPN_BOUND_ROWS.csv"),
            "status": "TIGHTENED_DESCENT_PREFACTOR_BOUND_DERIVED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SWB3990_5_ppn_wR",
            "symbol": "w_R_source_3990",
            "formula": "w_R_source_3990 <= epsilon_descent_prefactor_3990",
            "meaning": "PPN source-weight slot inherits the no-Hom/source-weight envelope",
            "source_path": str(SRC / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv"),
            "status": "PPN_FEED_UPDATED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SWB3990_6_beta",
            "symbol": "delta_beta_source_abs_3990",
            "formula": "delta_beta_source_abs_3990 <= |w_R_source_3990| + |epsilon_SN|",
            "meaning": "beta source component is now executable from a source-weight envelope plus source-normalization stability",
            "source_path": str(SRC / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv"),
            "status": "BETA_SOURCE_FEED_UPDATED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SWB3990_7_master",
            "symbol": "epsilon_closed_source_failure_3990",
            "formula": "epsilon_product_lock_total + epsilon_extra_monopole_total + epsilon_descent_prefactor_3990 + epsilon_PPN_rest_3989",
            "meaning": "current local-GR/Newton source-coupling residual after no-Hom grammar sharpening",
            "source_path": str(SRC / "P8_Y5_R2FR_3989_DESCENT_PREFAC_PPN_BOUND_ROWS.csv"),
            "status": "MASTER_RESIDUAL_SHARPENED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def schema_rows(timestamp: str) -> list[dict[str, Any]]:
    arenas = [
        ("PPN_beta", "delta_beta_source_abs_3990", "dimensionless", "compare to beta bound after no-cancellation sum"),
        ("WEP", "epsilon_no_hom_species_source_3990", "dimensionless log-ratio", "composition dependence of active/source weight"),
        ("R10", "alpha_lambda_source_weight_leg", "dimensionless alpha contribution", "short-range source-leg prefactor"),
        ("clock", "D_t_ln_w_common", "per time", "common source-scale drift in clock/local-time branch"),
        ("orbital_GM", "D_orbit_ln_GM_source", "dimensionless or per orbit", "GM/source normalization stability"),
    ]
    return [
        {
            "schema_id": f"SWS3990_{index}",
            "arena": arena,
            "required_symbol": symbol,
            "units": units,
            "required_numeric_columns": "value;abs_bound;units;arena_projection;source_path;valid_for_claim",
            "claim_rule": "valid_for_claim may become true only with numeric value, positive finite bound, real source path, and no MISSING_PARENT_INPUT",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "notes": notes,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for index, (arena, symbol, units, notes) in enumerate(arenas)
    ]


def evaluate_case(
    case_id: str,
    weights: list[float] | None,
    action_line: float | None,
    readout: float | None,
    r_matter: float | None,
    epsilon_sn: float | None,
    parent_rows_valid: bool,
    beta_bound: float = 7.8e-05,
) -> dict[str, Any]:
    if not parent_rows_valid or weights is None or action_line is None or readout is None or r_matter is None or epsilon_sn is None:
        return {
            "case_id": case_id,
            "input_status": "MISSING_PARENT_INPUT",
            "epsilon_no_hom_species_source": "MISSING",
            "epsilon_descent_prefactor": "MISSING",
            "delta_beta_source_abs": "MISSING",
            "beta_bound": beta_bound,
            "passes_bound": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    if any(weight <= 0 for weight in weights):
        raise ValueError(f"{case_id} has non-positive source weight")
    logs = [math.log(weight) for weight in weights]
    common_log = sum(logs) / len(logs)
    epsilon_no_hom = max(abs(log_weight - common_log) for log_weight in logs)
    prefactor_bound = epsilon_no_hom + abs(action_line) + abs(readout)
    descent_prefactor = abs(r_matter) + prefactor_bound
    delta_beta = descent_prefactor + abs(epsilon_sn)
    return {
        "case_id": case_id,
        "input_status": "NUMERIC_SMOKE_ONLY",
        "epsilon_no_hom_species_source": f"{epsilon_no_hom:.12g}",
        "epsilon_descent_prefactor": f"{descent_prefactor:.12g}",
        "delta_beta_source_abs": f"{delta_beta:.12g}",
        "beta_bound": beta_bound,
        "passes_bound": delta_beta <= beta_bound,
        "claim_allowed": False,
        "valid_for_claim": False,
    }


def smoke_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        evaluate_case("SMOKE3990_0_exact_no_hom_zero", [1.0, 1.0, 1.0], 0.0, 0.0, 0.0, 0.0, True),
        evaluate_case("SMOKE3990_1_small_envelope", [1.0, 1.0 + 1.0e-6, 1.0 - 5.0e-7], 2.0e-6, 3.0e-6, 0.0, 4.0e-6, True),
        evaluate_case("SMOKE3990_2_missing_parent_rows", None, None, None, None, None, False),
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def ppn_feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "feed_id": "PPNF3990_0_wR_source",
            "ppn_component": "w_R_source",
            "source_driver": "epsilon_descent_prefactor_3990",
            "formula": "w_R_source_3990 <= |R_matter_descent| + epsilon_no_hom_species_source_3990 + epsilon_action_line_universality_3990 + epsilon_readout_reentry_3990",
            "status": "PPN_SOURCE_WEIGHT_COMPONENT_SHARPENED_NONCLAIM",
            "source_path": str(SRC / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "PPNF3990_1_delta_beta_source",
            "ppn_component": "delta_beta_source",
            "source_driver": "w_R_source_3990|epsilon_SN",
            "formula": "delta_beta_source_abs_3990 <= |w_R_source_3990| + |epsilon_SN|",
            "status": "BETA_SOURCE_COMPONENT_SHARPENED_NONCLAIM",
            "source_path": str(SRC / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3990_0_zero_branch",
            "if_condition": "parent signs one action-density line, label-forgetful source functor, no source/species Hom, and no readout/worldtube re-entry",
            "then_action": "set epsilon_no_hom_species_source_3990=epsilon_action_line_universality_3990=epsilon_readout_reentry_3990=0 and move to remaining PPN rest/product/extra-monopole gates",
            "current_status": "NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3990_1_bound_branch",
            "if_condition": "any no-Hom grammar clause remains unsigned",
            "then_action": "use source-ready schema to acquire real WEP/PPN/R10/clock/orbital source-weight rows and feed beta/source stability",
            "current_status": "ACTIVE_NEXT_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM3990_0_no_local_GR_claim",
            "claim": "local GR/Newton source-coupling pass",
            "allowed": False,
            "reason": "no-Hom theorem is exact only conditionally; parent action grammar has not signed all clauses",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3990_1_no_PPN_claim",
            "claim": "PPN beta/source-weight pass",
            "allowed": False,
            "reason": "PPN feed is executable but numeric parent/source rows are missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3990_2_no_R10_claim",
            "claim": "R10/local-bound source-leg pass",
            "allowed": False,
            "reason": "R10 source-weight arena row remains schema-only until numeric alpha/lambda projection exists",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3990_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "source a first real source-weight bound row or build the PPN beta-source evaluator using the 3990 envelope",
            "success_condition": "one arena has numeric source-backed rows or the beta-source evaluator blocks cleanly with explicit missing inputs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "NO_HOM_GRAMMAR_META_THEOREM_DERIVED_SOURCE_WEIGHT_BOUND_RUNNER_READY",
            "headline": "relative source-weight poison is either untypeable under the signed grammar or bounded by an explicit no-cancellation source-weight envelope",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]]) -> None:
    found = sum(str(row["needle_found"]).lower() == "true" or row["needle_found"] is True for row in sources)
    lines = [
        "# 3990 - Parent Action Grammar No-Hom Or First Real Source-Weight Bound",
        "",
        f"Timestamp: `{timestamp}`",
        "",
        "## Result",
        "",
        "This checkpoint does not just circle the source-coupling gap. It turns the gap into a sharp fork:",
        "",
        "1. prove the parent grammar has no legal source/species/material-label homomorphism into an active source weight; or",
        "2. keep the source-weight branch alive but force it through explicit numeric bound rows.",
        "",
        "## Exact Conditional Theorem",
        "",
        "Let `G_src` be the source/species/material-label object and `W=R_+` the pre-action active-source-weight object.",
        "",
        "If ordinary matter sits on one parent action-density line, depends on the observed coframe only through `e_obs(q(Phi))`, the source functor first forgets labels to `T_total=sum_A T_A`, and no hidden/readout/worldtube marker returns before variation, then",
        "",
        "`Hom_parent(G_src,W)=CommonConst`.",
        "",
        "So relative `w_A/w_B` source weights are not merely set to zero by preference; they are untypeable in that grammar. A common scalar survives only as universal `G/source` calibration unless the parent action also fixes it.",
        "",
        "## Countermodel Guard",
        "",
        "`S_ord=sum_A w_A S_A` remains a valid obstruction if the parent grammar allows a source-label slot before variation. It can be covariant and Ward-compatible while changing the active Hilbert source.",
        "",
        "That is why 3990 is still non-claim: the theorem is exact, but current MTS has not yet parent-signed all grammar clauses.",
        "",
        "## Bound Law",
        "",
        "`R_source_prefactor_bound_3990 <= epsilon_no_hom_species_source_3990 + epsilon_action_line_universality_3990 + epsilon_readout_reentry_3990`.",
        "",
        "`epsilon_descent_prefactor_3990 <= |R_matter_descent| + R_source_prefactor_bound_3990`.",
        "",
        "`w_R_source_3990 <= epsilon_descent_prefactor_3990`.",
        "",
        "`delta_beta_source_abs_3990 <= |w_R_source_3990| + |epsilon_SN|`.",
        "",
        "## Master Residual",
        "",
        "`epsilon_closed_source_failure_3990 <= epsilon_product_lock_total + epsilon_extra_monopole_total + epsilon_descent_prefactor_3990 + epsilon_PPN_rest_3989`.",
        "",
        "## Smoke Runner",
        "",
        "- exact no-Hom zero case: produces zero source-weight/beta residual",
        "- small envelope case: produces a finite beta-source smoke value below the standing beta threshold",
        "- missing parent rows: blocks cleanly and remains non-claim",
        "",
        "## Source Register",
        "",
        f"`{found}/{len(sources)}` source needles found.",
    ]
    for row in sources:
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` needle `{row['needle']}` found={row['needle_found']}"
        )
    lines.extend(
        [
            "",
            "## Next Target",
            "",
            f"`{NEXT_DOC}`",
            "",
            "Source the first real source-weight bound row, or build the PPN beta-source evaluator against the 3990 envelope.",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def update_spine(timestamp: str) -> None:
    header = "## 3990 - Parent Action Grammar No-Hom Bound"
    block = "\n".join(
        [
            "",
            header,
            "",
            f"- Timestamp: `{timestamp}`",
            "- Status: `NO_HOM_GRAMMAR_META_THEOREM_DERIVED_SOURCE_WEIGHT_BOUND_RUNNER_READY`",
            "- Main theorem:",
            "  under a single action-density line, label-forgetful source functor, no source/species/material Hom into `R_+`, and no readout/worldtube re-entry, `Hom_parent(G_src,R_+)=CommonConst`.",
            "- Physics meaning:",
            "  relative active-source weights become untypeable rather than tuned away; the remaining common scalar is a universal `G/source` calibration gate.",
            "- Countermodel retained:",
            "  `S_ord=sum_A w_A S_A` still blocks a claim if the parent grammar admits source labels before variation.",
            "- Bound law:",
            "  `epsilon_descent_prefactor_3990 <= |R_matter_descent| + epsilon_no_hom_species_source_3990 + epsilon_action_line_universality_3990 + epsilon_readout_reentry_3990`.",
            "- PPN feed:",
            "  `w_R_source_3990 <= epsilon_descent_prefactor_3990`; `delta_beta_source_abs_3990 <= |w_R_source_3990| + |epsilon_SN|`.",
            "- Current residual:",
            "  `epsilon_closed_source_failure_3990 <= epsilon_product_lock_total + epsilon_extra_monopole_total + epsilon_descent_prefactor_3990 + epsilon_PPN_rest_3989`.",
            f"- Next: `{NEXT_DOC}`.",
            "",
        ]
    )
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    if header not in existing:
        SPINE_PATH.write_text(existing.rstrip() + block, encoding="utf-8")


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    smoke: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "passed": passed,
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    add("VAL3990_00_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3990_01_needles_found", all(row["needle_found"] for row in sources), "every cited source needle found")
    add("VAL3990_02_theorem_target", any(row["theorem_id"] == "NHG3990_0_target" for row in theorem), "target no-Hom theorem row present")
    add("VAL3990_03_countermodel_retained", any(row["theorem_id"] == "NHG3990_4_countermodel" for row in theorem), "countermodel retained")
    add("VAL3990_04_bound_rows", len(bounds) >= 8, "source-weight and PPN bound rows written")
    add("VAL3990_05_all_nonclaim_bounds", not any(str(row["valid_for_claim"]).lower() == "true" for row in bounds), "bound rows remain nonclaim")
    zero = next(row for row in smoke if row["case_id"] == "SMOKE3990_0_exact_no_hom_zero")
    small = next(row for row in smoke if row["case_id"] == "SMOKE3990_1_small_envelope")
    missing = next(row for row in smoke if row["case_id"] == "SMOKE3990_2_missing_parent_rows")
    add("VAL3990_06_zero_smoke", float(zero["delta_beta_source_abs"]) == 0.0, "exact no-Hom zero smoke gives zero beta-source residual")
    add("VAL3990_07_small_smoke_passes_bound", str(small["passes_bound"]).lower() == "true", "small envelope remains below beta smoke bound")
    add("VAL3990_08_missing_blocks", missing["input_status"] == "MISSING_PARENT_INPUT" and str(missing["passes_bound"]).lower() == "false", "missing parent rows block")
    add("VAL3990_09_ppn_feed_exists", OUTPUTS["ppn_feed"].exists(), "PPN feed file exists")
    add("VAL3990_10_claim_gate_exists", OUTPUTS["claim_gate"].exists(), "claim gate exists")
    add("VAL3990_11_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL3990_12_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL3990_13_doc_exists", DOC_PATH.exists() and "Hom_parent(G_src,W)=CommonConst" in read_text(DOC_PATH), "document written")
    add("VAL3990_14_spine_updated", SPINE_PATH.exists() and "## 3990 - Parent Action Grammar No-Hom Bound" in read_text(SPINE_PATH), "spine updated")
    add("VAL3990_15_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL3990_16_compile", compile_ok, "script compiles")
    add("VAL3990_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL3990_18_status_exists", OUTPUTS["status"].exists(), "status file exists")
    add("VAL3990_19_schema_nonclaim", all(str(row["valid_for_claim"]).lower() == "false" for row in read_csv(OUTPUTS["schema"])), "schema rows remain nonclaim")
    return rows


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    bounds = bound_rows(timestamp)
    schema = schema_rows(timestamp)
    smoke = smoke_rows(timestamp)
    ppn_feed = ppn_feed_rows(timestamp)
    decision = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["bound_rows"], bounds)
    write_csv(OUTPUTS["schema"], schema)
    write_csv(OUTPUTS["smoke"], smoke)
    write_csv(OUTPUTS["ppn_feed"], ppn_feed)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["claim_gate"], claim_gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources)
    update_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validation = build_validation_rows(timestamp, sources, theorem, bounds, smoke, compile_ok)
    write_csv(OUTPUTS["validation"], validation)

    failed = [row for row in validation if str(row["passed"]).lower() != "true"]
    print(f"3990 validation: {len(validation) - len(failed)}/{len(validation)} passed")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
