from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1915"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1915-Y5-R2FR-finite-residual-priority-and-first-fill-row.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1914_doc": ROOT / "1914-Y5-R2FR-finite-residual-branch-v0-no-cancellation-interface.md",
    "1914_validation": OUT / "P8_Y5_BRR545_1914_VALIDATION.csv",
    "1914_residual_vector": OUT / "P8_Y5_PARENT_QLOC_1914_FINITE_RESIDUAL_VECTOR_V0_NONCLAIM.csv",
    "1914_arena_interface": OUT / "P8_Y5_PARENT_QLOC_1914_ARENA_PROJECTION_INTERFACE_V0_NONCLAIM.csv",
    "1914_no_cancellation": OUT / "P8_Y5_PARENT_QLOC_1914_NO_CANCELLATION_POLICY.csv",
    "1914_next": OUT / "P8_Y5_PARENT_QLOC_1914_NEXT_TARGET.csv",
    "1913_residual_branch": OUT / "P8_Y5_PARENT_QLOC_1913_FINITE_RESIDUAL_BRANCH_NONCLAIM.csv",
    "943_doc": ROOT / "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
    "943_derivation_attempt": OUT / "P8_Y5_R10_943_DERIVATION_ATTEMPT.csv",
    "943_coframe_contract": OUT / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
    "943_frame_source_pack": OUT / "P8_Y5_R10_943_FRAME_RESIDUAL_SOURCE_PACK.csv",
    "1045_doc": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
    "1045_matter_functor": OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
    "1045_qbar_geom": OUT / "P8_Y5_R10_1045_QBAR_GEOM_ZERO_ATTEMPT.csv",
    "1045_vertical_lift": OUT / "P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv",
}


SOURCE_NEEDLES = {
    "1914_doc": ["FRV1914_frame_or_coframe_residual", "NEXT1914_0_primary"],
    "1914_validation": ["VAL1914_OVERALL,PASS"],
    "1914_residual_vector": ["FRV1914_frame_or_coframe_residual", "FRV1914_readout_tau_residual"],
    "1914_arena_interface": ["ARI1914_WEP_MICROSCOPE_TiPt", "ARI1914_orbital_GM_inverse_square"],
    "1914_no_cancellation": ["NCP1914_0_absolute_sum", "NCP1914_4_one_branch"],
    "1914_next": ["NEXT1914_0_primary", "1915-Y5-R2FR-finite-residual-priority-and-first-fill-row.md"],
    "1913_residual_branch": ["FR1913_frame", "FR1913_readout_tau"],
    "943_doc": ["DER943_0_vertical_blindness", "FRS943_0_common_frame_log_derivative"],
    "943_derivation_attempt": ["DER943_0_vertical_blindness", "DER943_5_shadow_counterexample"],
    "943_coframe_contract": ["CFC943_0_parent_quotient_map", "CFC943_4_connection_lock", "CFC943_6_no_shadow_frame_rule"],
    "943_frame_source_pack": ["FRS943_0_common_frame_log_derivative", "FRS943_6_nonHilbert_current_projection"],
    "1045_doc": ["MFS1045_0_parent_field_quotient", "QG1045_4_current_verdict"],
    "1045_matter_functor": ["MFS1045_0_parent_field_quotient", "MFS1045_6_verdict"],
    "1045_qbar_geom": ["QG1045_1_functor_chain_rule", "QG1045_4_current_verdict"],
    "1045_vertical_lift": ["VLG1045_0_fixed_lift", "VLG1045_4_verdict"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1915_SOURCE_REGISTER.csv",
    "priority_matrix": OUT / "P8_Y5_PARENT_QLOC_1915_RESIDUAL_PRIORITY_MATRIX_NONCLAIM.csv",
    "first_fill": OUT / "P8_Y5_PARENT_QLOC_1915_FIRST_FILL_FRAME_RESIDUAL_ATTEMPT.csv",
    "blocker_ledger": OUT / "P8_Y5_PARENT_QLOC_1915_FIRST_FILL_BLOCKER_LEDGER_NONCLAIM.csv",
    "dryrun": OUT / "P8_Y5_PARENT_QLOC_1915_NO_CANCELLATION_FIRST_FILL_DRYRUN.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1915_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1915_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1915_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1915_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1915_VALIDATION.csv",
}


BRANCH_COPIES = {
    "priority_matrix": SOURCE_WEIGHT_DOCS / "FINITE_RESIDUAL_PRIORITY_MATRIX_1915_NONCLAIM.csv",
    "first_fill": MICROSCOPE_RESIDUALS / OUTPUTS["first_fill"].name,
    "blocker_ledger": QUEUE / "JR1915_FIRST_FILL_BLOCKERS_NONCLAIM.csv",
    "dryrun": QUARANTINE / OUTPUTS["dryrun"].name,
}


def ensure_dirs() -> None:
    for path in [OUT, MICROSCOPE_RESIDUALS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def markdown_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, Any]]:
    rows = []
    for key, path in INPUTS.items():
        needles = SOURCE_NEEDLES[key]
        exists = path.exists()
        text = source_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        status = "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_OR_NEEDLE_FAILED"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "needed_for": "1915 residual prioritisation and frame/coframe first-fill attempt",
                "needles": ";".join(needles),
                "status": status,
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def build_priority_matrix() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "priority_rank": 1,
            "residual_component": "frame_or_coframe_residual",
            "source_residual_id": "FRV1914_frame_or_coframe_residual",
            "derivation_route": "DER943_0/QG1045_1 chain-rule zero if q_loc and Obs_e are parent-owned",
            "derivability_score_1to5": 5,
            "empirical_leverage_score_1to5": 5,
            "arena_count": 4,
            "arena_targets": "WEP_MICROSCOPE_TiPt;PPN_beta_gamma_source;clock_and_constant_drift;orbital_GM_inverse_square",
            "zero_requirements": "parent q_loc; observed coframe descent; no shadow frame; connection lock; matter lift/boundary silence",
            "finite_fallback_requirements": "source b_g, b_dis, q_nonH, tau/frame support shifts with units and uncertainties",
            "first_fill_decision": "SELECTED_FIRST_FILL_TARGET",
            "current_status": "CONDITIONAL_ZERO_ROUTE_EXISTS_BUT_PARENT_SIGNATURES_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_rank": 2,
            "residual_component": "readout_tau_residual",
            "source_residual_id": "FRV1914_readout_tau_residual",
            "derivation_route": "readout-after-variation and tau/source-normal lock; broad but data/kernel heavy",
            "derivability_score_1to5": 3,
            "empirical_leverage_score_1to5": 5,
            "arena_count": 5,
            "arena_targets": "WEP_MICROSCOPE_TiPt;R10_short_range;PPN_beta_gamma_source;clock_and_constant_drift;orbital_GM_inverse_square",
            "zero_requirements": "owned readout map; source worldtube; tau/n lock; no calibration hiding",
            "finite_fallback_requirements": "source tau kernels and readout arrays per arena",
            "first_fill_decision": "DEFER_AFTER_FRAME_TARGET",
            "current_status": "HIGH_LEVERAGE_BUT_KERNELS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_rank": 3,
            "residual_component": "source_weight_residual",
            "source_residual_id": "FRV1914_source_weight_residual",
            "derivation_route": "source-label forgetting/common-current theorem or finite relative-weight vector",
            "derivability_score_1to5": 3,
            "empirical_leverage_score_1to5": 4,
            "arena_count": 4,
            "arena_targets": "WEP_MICROSCOPE_TiPt;R10_short_range;PPN_beta_gamma_source;orbital_GM_inverse_square",
            "zero_requirements": "common measure/current owner; no species/source-only slot; material/source map",
            "finite_fallback_requirements": "source-backed Delta w_A rows and arena projection kernels",
            "first_fill_decision": "DEFER_AFTER_FRAME_AND_READOUT",
            "current_status": "COUPLING_PRESSURE_HIGH_BUT_PARENT_CURRENT_OWNER_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_rank": 4,
            "residual_component": "constant_sector_residual",
            "source_residual_id": "FRV1914_constant_sector_residual",
            "derivation_route": "constant superselection/quotient ownership or finite alpha/mass/clock coefficient rows",
            "derivability_score_1to5": 3,
            "empirical_leverage_score_1to5": 4,
            "arena_count": 3,
            "arena_targets": "WEP_MICROSCOPE_TiPt;R10_short_range;clock_and_constant_drift",
            "zero_requirements": "theta_A superselection; fixed charge/mass lattice; alpha/clock owner",
            "finite_fallback_requirements": "alpha_EM, mass-ratio, clock-sensitivity coefficient vector",
            "first_fill_decision": "DEFER",
            "current_status": "IMPORTANT_BUT_SPLITS_INTO_MULTIPLE_CONSTANT_SUBSECTORS",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_rank": 5,
            "residual_component": "EM_hidden_F2_residual",
            "source_residual_id": "FRV1914_EM_hidden_F2_residual",
            "derivation_route": "unique Maxwell/F_Q2 owner and no independent hidden visible F2 operator",
            "derivability_score_1to5": 3,
            "empirical_leverage_score_1to5": 4,
            "arena_count": 3,
            "arena_targets": "WEP_MICROSCOPE_TiPt;R10_short_range;clock_and_constant_drift",
            "zero_requirements": "single gauge kinetic owner; no extra F2; radiative closure",
            "finite_fallback_requirements": "finite alpha_EM or hidden-F2 coefficient with provenance",
            "first_fill_decision": "DEFER",
            "current_status": "PHYSICALLY_SHARP_BUT_NOT_FIRST_LOCAL_GR_GATE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_rank": 6,
            "residual_component": "boundary_domain_residual",
            "source_residual_id": "FRV1914_boundary_domain_residual",
            "derivation_route": "boundary/domain/source-worldtube silence or finite edge/domain coefficient",
            "derivability_score_1to5": 2,
            "empirical_leverage_score_1to5": 3,
            "arena_count": 3,
            "arena_targets": "R10_short_range;PPN_beta_gamma_source;orbital_GM_inverse_square",
            "zero_requirements": "compact support; owned exact boundary; no domain flux/source edge leakage",
            "finite_fallback_requirements": "boundary/domain coefficient and source-worldtube support map",
            "first_fill_decision": "DEFER",
            "current_status": "REAL_BUT_TOO_BROAD_FOR_FIRST_FILL",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_rank": 7,
            "residual_component": "matter_lift_residual",
            "source_residual_id": "FRV1914_matter_lift_residual",
            "derivation_route": "parent-assigned fixed/gauge vertical lift or finite matter-lift source row",
            "derivability_score_1to5": 2,
            "empirical_leverage_score_1to5": 2,
            "arena_count": 2,
            "arena_targets": "WEP_MICROSCOPE_TiPt;clock_and_constant_drift",
            "zero_requirements": "parent matter bundle and vertical lift for every ordinary species",
            "finite_fallback_requirements": "species/material lift coefficients and boundary terms",
            "first_fill_decision": "DEFER_BUT_INCLUDED_IN_FRAME_BLOCKERS",
            "current_status": "NARROWER_AND_DEPENDS_ON_PARENT_MATTER_FUNCTOR",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_first_fill_attempt() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "FF1915_0_target_selection",
            "target_component": "frame_or_coframe_residual",
            "proof_step": "Select first row",
            "condition_or_formula": "FRV1914_frame_or_coframe_residual has conditional zero route plus four-arena leverage",
            "source_ids": "FRV1914_frame_or_coframe_residual;DER943_0_vertical_blindness;QG1045_1_functor_chain_rule",
            "result": "TARGET_SELECTED_NONCLAIM",
            "theorem_zero_imported": False,
            "finite_value_sourced": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "FF1915_1_exact_chain_rule_core",
            "target_component": "frame_or_coframe_residual",
            "proof_step": "Local vertical blindness",
            "condition_or_formula": "If e_obs=Obs_e(q_loc(Phi)) and Dq_loc[v_X]=0, then Lie_v e_obs = D Obs_e[Dq_loc[v_X]] = 0",
            "source_ids": "DER943_0_vertical_blindness;QG1045_1_functor_chain_rule",
            "result": "EXACT_CONDITIONAL_SUBLEMMA_AVAILABLE",
            "theorem_zero_imported": False,
            "finite_value_sourced": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "FF1915_2_metric_connection_extension",
            "target_component": "frame_or_coframe_residual",
            "proof_step": "Extend coframe zero to metric/connection",
            "condition_or_formula": "Lie_v g_obs=0 follows from Lie_v e_obs=0; Lie_v omega=0 only if omega is Levi-Civita/coframe-owned",
            "source_ids": "MFS1045_1_observed_coframe_functor;QG1045_2_connection_stack;CFC943_4_connection_lock",
            "result": "CONDITIONAL_CONNECTION_CAVEAT_RETAINED",
            "theorem_zero_imported": False,
            "finite_value_sourced": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "FF1915_3_shadow_frame_countermodel",
            "target_component": "frame_or_coframe_residual",
            "proof_step": "Test no-shadow frame loophole",
            "condition_or_formula": "A hidden A_A(X)^2 g_obs or disformal B_A(X) frame gives nonzero b_g/b_dis unless parent-forbidden or retained",
            "source_ids": "DER943_5_shadow_counterexample;MFS1045_4_no_shadow_frame;QG1045_3_shadow_countermodel",
            "result": "BLOCKER_RETAINED_NO_SHADOW_FRAME_NOT_PARENT_DERIVED",
            "theorem_zero_imported": False,
            "finite_value_sourced": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "FF1915_4_matter_functor_lift_boundary",
            "target_component": "frame_or_coframe_residual",
            "proof_step": "Check ordinary matter lift and boundary silence",
            "condition_or_formula": "S_A must be a descended matter functor with fixed/gauge vertical lift and compact/exact boundary variation",
            "source_ids": "MFS1045_2_matter_bundle_functor;MFS1045_3_vertical_lift;VLG1045_4_verdict",
            "result": "BLOCKER_RETAINED_MATTER_FUNCTOR_AND_VERTICAL_LIFT_UNSIGNED",
            "theorem_zero_imported": False,
            "finite_value_sourced": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "FF1915_5_finite_source_fallback",
            "target_component": "frame_or_coframe_residual",
            "proof_step": "If zero proof fails, define source rows",
            "condition_or_formula": "Use FRS943 b_g, b_dis, b_A, partial_v kappa, Delta_tau_n, Delta_W_support, q_nonH as finite source targets",
            "source_ids": "P8_Y5_R10_943_FRAME_RESIDUAL_SOURCE_PACK.csv",
            "result": "FINITE_SOURCE_FALLBACK_IDENTIFIED_BUT_NUMERIC_VALUES_MISSING",
            "theorem_zero_imported": False,
            "finite_value_sourced": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "FF1915_6_result",
            "target_component": "frame_or_coframe_residual",
            "proof_step": "First-fill verdict",
            "condition_or_formula": "Conditional chain-rule zero is real, but parent q/Obs_e/no-shadow/connection/matter-lift signatures are unsigned and no finite coefficient is sourced",
            "source_ids": "CFC943_7_contract_verdict;MFS1045_6_verdict;QG1045_4_current_verdict;VLG1045_4_verdict",
            "result": "FIRST_FILL_BLOCKED_CONDITIONAL_ZERO_ONLY",
            "theorem_zero_imported": False,
            "finite_value_sourced": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_blocker_ledger() -> list[dict[str, Any]]:
    blockers = [
        (
            "BL1915_0_parent_q_owner",
            "parent q_loc object and v_X in ker(Dq_loc) for all local sectors",
            "CFC943_0_parent_quotient_map;MFS1045_0_parent_field_quotient",
            "MISSING_PARENT_SIGNATURE",
            "1916 prove parent q_loc or keep finite frame residual branch",
        ),
        (
            "BL1915_1_observed_coframe_descent",
            "Obs_e(q_loc(Phi)) parent-owned before readout",
            "CFC943_1_observed_coframe_descent;MFS1045_1_observed_coframe_functor",
            "SUFFICIENT_CONDITION_UNSIGNED",
            "1916 sign observed coframe functor or source b_g/b_dis",
        ),
        (
            "BL1915_2_no_shadow_frame",
            "no hidden conformal/disformal/source-only material frame",
            "DER943_5_shadow_counterexample;CFC943_6_no_shadow_frame_rule;MFS1045_4_no_shadow_frame",
            "COUNTERMODEL_RETAINED",
            "prove no-shadow frame theorem or create finite b_g/b_dis rows",
        ),
        (
            "BL1915_3_connection_lock",
            "matter connection induced by e_obs or independent connection retained",
            "CFC943_4_connection_lock;QG1045_2_connection_stack",
            "CONNECTION_CAVEAT_OPEN",
            "prove connection lock or add q_nonH/torsion/nonmetricity finite source row",
        ),
        (
            "BL1915_4_matter_functor_lift",
            "ordinary matter bundle functor and vertical lift owned by parent",
            "MFS1045_2_matter_bundle_functor;MFS1045_3_vertical_lift;VLG1045_4_verdict",
            "MISSING_PARENT_MATTER_FUNCTOR",
            "construct matter functor signature or retain matter_lift_residual",
        ),
        (
            "BL1915_5_boundary_projection_silence",
            "matter-domain boundary/support variation compact, exact, or separately retained",
            "VLG1045_3_boundary_lift;FRS943_5_worldtube_support_shift",
            "BOUNDARY_LOCAL_PROJECTION_OPEN",
            "source support-shift row or prove boundary exactness in the same branch",
        ),
        (
            "BL1915_6_finite_value_source",
            "numeric finite frame/coframe coefficient with units, uncertainty, and source path",
            "FRS943_0_common_frame_log_derivative;FRS943_1_disformal_frame_derivative;FRS943_6_nonHilbert_current_projection",
            "MISSING_NUMERIC_PARENT_VALUE",
            "build source-ready finite coefficient rows only if zero proof fails",
        ),
        (
            "BL1915_7_arena_projection_kernels",
            "WEP/PPN/clock/orbital kernels for projected frame residual",
            "ARI1914_WEP_MICROSCOPE_TiPt;ARI1914_PPN_beta_gamma_source;ARI1914_clock_and_constant_drift;ARI1914_orbital_GM_inverse_square",
            "MISSING_ARENA_PROJECTION_KERNELS",
            "do not score until one residual row and one arena kernel are source-backed",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "target_component": "frame_or_coframe_residual",
            "missing_clause": missing_clause,
            "blocking_source_ids": source_ids,
            "status": status,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for blocker_id, missing_clause, source_ids, status, next_action in blockers
    ]


def build_dryrun() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "dryrun_id": "DFF1915_0_unsigned_conditional_zero",
            "scenario": "Use DER943/QG1045 chain-rule zero while q/Obs_e are unsigned",
            "component_values": "frame_or_coframe_residual=conditional_zero_only",
            "arena_kernel_status": "MISSING_ARENA_KERNELS",
            "has_parent_identity": False,
            "attempted_cancellation": False,
            "decision": "BLOCK_IMPORT_ZERO_UNTIL_PARENT_SIGNED",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "dryrun_id": "DFF1915_1_placeholder_finite_bg",
            "scenario": "Insert symbolic b_g without source path, units, or uncertainty",
            "component_values": "b_g=MISSING_NUMERIC_PARENT_VALUE",
            "arena_kernel_status": "MISSING_ARENA_KERNELS",
            "has_parent_identity": False,
            "attempted_cancellation": False,
            "decision": "BLOCK_MISSING_NUMERIC_SOURCE",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "dryrun_id": "DFF1915_2_cancellation_fit",
            "scenario": "Let frame residual cancel readout_tau/source_weight residual",
            "component_values": "signed_fit_between_unfilled_rows",
            "arena_kernel_status": "MISSING_ARENA_KERNELS",
            "has_parent_identity": False,
            "attempted_cancellation": True,
            "decision": "REFUSE_CANCELLATION_WITHOUT_PARENT_IDENTITY",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "dryrun_id": "DFF1915_3_forward_wep_projection",
            "scenario": "Project frame residual into MICROSCOPE Ti/Pt WEP envelope",
            "component_values": "frame_or_coframe_residual=MISSING_OR_UNBOUNDED",
            "arena_kernel_status": "MISSING_MATERIAL_SOURCE_READOUT_TAU_KERNELS",
            "has_parent_identity": False,
            "attempted_cancellation": False,
            "decision": "BLOCK_MISSING_ARENA_KERNELS",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "dryrun_id": "DFF1915_4_hypothetical_signed_zero",
            "scenario": "All q/Obs_e/no-shadow/connection/matter-lift clauses signed in one parent action",
            "component_values": "frame_or_coframe_residual=DERIVED_ZERO_WITH_SOURCE_PATHS",
            "arena_kernel_status": "still_requires_projection_kernel_for_arena_scores",
            "has_parent_identity": True,
            "attempted_cancellation": False,
            "decision": "ACCEPT_SCHEMA_ONLY_NOT_CURRENTLY_TRUE",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_claim_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1915_0_sources",
            "requirement": "all cited 1914/943/1045 source paths exist and needles are found",
            "current_status": "SOURCE_REGISTER_PASS_IF_VALIDATION_PASS",
            "blocks_claim_if_failed": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1915_1_priority",
            "requirement": "one residual selected by derivability and empirical leverage",
            "current_status": "FRAME_OR_COFRAME_SELECTED",
            "blocks_claim_if_failed": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1915_2_zero_theorem",
            "requirement": "selected residual theorem-zero imported only if parent q/Obs_e/no-shadow/connection/matter-lift clauses are signed",
            "current_status": "BLOCKED_UNSIGNED_PARENT_CLAUSES",
            "blocks_claim_if_failed": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1915_3_finite_fallback",
            "requirement": "if theorem-zero fails, finite residual value must have units, uncertainty, source path, and branch-locked arena kernel",
            "current_status": "BLOCKED_NO_NUMERIC_SOURCE_OR_ARENA_KERNEL",
            "blocks_claim_if_failed": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1915_4_no_cancellation",
            "requirement": "no tuned cancellation between residual rows without parent identity",
            "current_status": "NO_CANCELLATION_GUARD_ACTIVE",
            "blocks_claim_if_failed": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1915_5_claim",
            "requirement": "1915 supports local-GR/WEP/PPN/R10 claim-grade scoring",
            "current_status": "CLAIM_BLOCKED",
            "blocks_claim_if_failed": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_decision() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1915_0_first_target",
            "decision": "SELECT_FRAME_OR_COFRAME_RESIDUAL_FIRST",
            "reason": "It has the cleanest exact conditional zero route and hits WEP/PPN/clock/orbital without being merely a data fit.",
            "consequence": "1916 should try to sign q/Obs_e/no-shadow/connection/matter-lift clauses or produce finite frame-leak rows.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1915_1_zero_status",
            "decision": "DO_NOT_IMPORT_FRAME_ZERO_YET",
            "reason": "DER943/QG1045 prove the chain-rule sublemma only under parent-owned quotient/coframe assumptions; shadow-frame and connection countermodels remain live.",
            "consequence": "Frame residual remains unfilled/nonclaim until parent signatures or finite sources exist.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1915_2_scoring_status",
            "decision": "NO_BROAD_LOCAL_SCORING",
            "reason": "At least one residual row and one arena kernel must be source-backed before WEP/PPN/R10/clock/orbital comparisons are meaningful.",
            "consequence": "Next progress is proof/source filling, not more benchmark comparisons.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_next_target() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1915_0_primary",
            "selection_status": "selected",
            "target_doc": "1916-Y5-R2FR-frame-residual-zero-proof-or-source-bound-row.md",
            "target_script": "scripts/Y5_R2FR_frame_residual_zero_proof_or_source_bound_row_1916.py",
            "objective": "focus only on the selected frame/coframe residual: either sign q/Obs_e/no-shadow/connection/matter-lift clauses into a theorem-zero, or write finite source-ready b_g/b_dis/q_nonH rows",
            "success_condition": "Z_frame=true with parent source paths, or a finite nonclaim frame residual row with units, uncertainty, source path, and no-cancellation projection requirements",
            "do_not": "do not set frame residual to zero by minimality, do not infer it from empirical bounds, and do not cancel it against other residual rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def build_project_status() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "STAT1915_0_gain",
            "area": "finite residual branch",
            "summary": "1915 ranks all seven 1914 residual rows and chooses frame/coframe as the first-fill target.",
            "risk_level": "STRUCTURE_GAINED_NONCLAIM",
            "project_meaning": "the local-GR bridge now has an ordered attack list instead of a fog bank",
            "next_action": "attempt frame residual zero proof or finite source row in 1916",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "STAT1915_1_result",
            "area": "frame/coframe residual",
            "summary": "The exact chain-rule zero exists conditionally, but parent q/Obs_e/no-shadow/connection/matter-lift signatures are unsigned.",
            "risk_level": "PROMISING_BUT_BLOCKED",
            "project_meaning": "this is not dead; it is a precise coupling/geometry ownership problem",
            "next_action": "prove the missing parent signatures or retain finite b_g/b_dis/q_nonH rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "STAT1915_2_guard",
            "area": "claim discipline",
            "summary": "No theorem-zero or finite value was imported, and no cancellation or bound inversion is allowed.",
            "risk_level": "CLAIM_DISCIPLINE_MAINTAINED",
            "project_meaning": "we are not cheating the local branch into existence",
            "next_action": "keep rows nonclaim until source-backed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": build_source_register(),
        "priority_matrix": build_priority_matrix(),
        "first_fill": build_first_fill_attempt(),
        "blocker_ledger": build_blocker_ledger(),
        "dryrun": build_dryrun(),
        "claim_gate": build_claim_gate(),
        "decision": build_decision(),
        "next_target": build_next_target(),
        "project_status": build_project_status(),
    }


def copy_branch_artifacts() -> None:
    for key, destination in BRANCH_COPIES.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUTPUTS[key], destination)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def claim_flags_safe(paths: list[Path]) -> tuple[bool, str]:
    unsafe: list[str] = []
    for path in paths:
        for row in csv_rows(path):
            if "valid_for_claim" in row and bool_string(row["valid_for_claim"]) != "false":
                unsafe.append(f"{path.name}:valid_for_claim")
            if "claim_allowed" in row and bool_string(row["claim_allowed"]) != "false":
                unsafe.append(f"{path.name}:claim_allowed")
    return not unsafe, "claim flags all false" if not unsafe else ";".join(unsafe)


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    failures: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
        except Exception as exc:  # pragma: no cover - validation detail
            failures.append(f"{path.name}:{exc}")
            continue
        if not rows:
            failures.append(f"{path.name}:no_rows")
    return not failures, "all generated CSVs parse with rows" if not failures else ";".join(failures)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append(
        {
            "validation_id": "VAL1915_00_sources",
            "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL",
            "detail": "all local source paths exist and needles found",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    priority_rows = csv_rows(OUTPUTS["priority_matrix"])
    checks.append(
        {
            "validation_id": "VAL1915_01_priority_matrix",
            "status": "PASS"
            if len(priority_rows) == 7
            and any(
                row["priority_rank"] == "1"
                and row["residual_component"] == "frame_or_coframe_residual"
                and row["first_fill_decision"] == "SELECTED_FIRST_FILL_TARGET"
                for row in priority_rows
            )
            else "FAIL",
            "detail": "seven residuals ranked with frame/coframe selected first",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    first_fill_rows = csv_rows(OUTPUTS["first_fill"])
    checks.append(
        {
            "validation_id": "VAL1915_02_first_fill_result",
            "status": "PASS"
            if any(row["attempt_id"] == "FF1915_6_result" and row["result"] == "FIRST_FILL_BLOCKED_CONDITIONAL_ZERO_ONLY" for row in first_fill_rows)
            and all(bool_string(row["theorem_zero_imported"]) == "false" for row in first_fill_rows)
            and all(bool_string(row["finite_value_sourced"]) == "false" for row in first_fill_rows)
            else "FAIL",
            "detail": "first fill attempted but no theorem-zero or finite value imported",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    blocker_rows = csv_rows(OUTPUTS["blocker_ledger"])
    checks.append(
        {
            "validation_id": "VAL1915_03_blocker_ledger",
            "status": "PASS" if len(blocker_rows) >= 6 and all(bool_string(row["valid_for_claim"]) == "false" for row in blocker_rows) else "FAIL",
            "detail": "frame/coframe blockers retained as nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    dry_rows = csv_rows(OUTPUTS["dryrun"])
    checks.append(
        {
            "validation_id": "VAL1915_04_no_cancellation_dryrun",
            "status": "PASS"
            if any(row["dryrun_id"] == "DFF1915_2_cancellation_fit" and row["decision"] == "REFUSE_CANCELLATION_WITHOUT_PARENT_IDENTITY" for row in dry_rows)
            else "FAIL",
            "detail": "dry-run refuses cancellation fit",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    gates = csv_rows(OUTPUTS["claim_gate"])
    checks.append(
        {
            "validation_id": "VAL1915_05_claim_gate",
            "status": "PASS" if any(row["gate_id"] == "CG1915_5_claim" and row["current_status"] == "CLAIM_BLOCKED" for row in gates) else "FAIL",
            "detail": "claim remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append(
        {
            "validation_id": "VAL1915_06_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1915_0_primary" and row["selection_status"] == "selected" for row in next_rows)
            else "FAIL",
            "detail": "1916 frame residual route selected",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    flags_ok, flags_detail = claim_flags_safe(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1915_07_claim_flags_safe",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1915_08_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1915_09_branch_copies",
            "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL",
            "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1915_10_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    formalization_hits = []
    if FORMALIZATION.exists():
        artifact_needles = [
            "1915-Y5-R2FR-finite-residual",
            "P8_Y5_PARENT_QLOC_1915",
            "Y5_R2FR_finite_residual_priority_and_first_fill_row_1915",
        ]
        formalization_hits = [
            path
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and any(needle in path.name for needle in artifact_needles)
        ]
    checks.append(
        {
            "validation_id": "VAL1915_11_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1915_artifact_count={len(formalization_hits)}",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1915_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1915 finite residual priority and frame/coframe first-fill row",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1915 - Finite Residual Priority and First-Fill Row

## Purpose

This checkpoint takes the 1914 finite residual vector and ranks the rows by derivability plus empirical leverage. It then attempts the first fill on the frame/coframe residual without importing a zero theorem, fitting a value, or allowing cancellation.

## Result

- The first target is `frame_or_coframe_residual`.
- The exact chain-rule core is real: if `e_obs=Obs_e(q_loc(Phi))` and `Dq_loc[v_X]=0`, then `Lie_v e_obs=0`.
- That does **not** yet prove the local branch, because the parent quotient, observed coframe functor, no-shadow frame rule, connection lock, matter lift, and boundary silence are unsigned.
- No finite coefficient is sourced yet (`b_g`, `b_dis`, `q_nonH`, support/readout shifts remain source targets).
- Claim status remains blocked.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Residual Priority Matrix

{markdown_table(rows_by_name["priority_matrix"])}

## First-Fill Frame Residual Attempt

{markdown_table(rows_by_name["first_fill"])}

## Blocker Ledger

{markdown_table(rows_by_name["blocker_ledger"])}

## No-Cancellation First-Fill Dry Run

{markdown_table(rows_by_name["dryrun"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
