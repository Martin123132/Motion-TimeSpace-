from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_SOURCE_WEIGHT_RESIDUAL_BOUND_PACK_2510"
CHECKPOINT_ID = "2510"
DOC = ROOT / "2510-Y5-R2FR-source-weight-residual-bound-pack-WEP-R10-PPN-clock-orbit.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2510_SOURCE_REGISTER.csv",
    "component_schema": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2510_DELTAW_COMPONENT_SCHEMA.csv",
    "arena_requirements": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2510_ARENA_BOUND_REQUIREMENTS.csv",
    "acquisition_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2510_INPUT_ACQUISITION_LEDGER.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2510_NONCLAIM_DRYRUN_RESULTS.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2510_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2510_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2510_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2510_VALIDATION.csv",
}

BRANCH_COPIES = {
    "bound_pack": ROOT
    / "source-intake"
    / "local_bounds"
    / "Source_weight_residual_bound_pack_2510_NONCLAIM.csv",
    "no_cancellation_policy": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Source_weight_residual_no_cancellation_policy_2510_NONCLAIM.csv",
    "acquisition_queue": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2510_SOURCE_WEIGHT_RESIDUAL_BOUND_PACK_NONCLAIM.csv",
    "next_source_input": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2510_NEXT_SOURCE_WEIGHT_INPUT_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2510_0_2509_pivot",
        "path": "2509-Y5-R2FR-parent-constructor-exhaustion-from-MTS-primitives-or-source-weight-residual-pivot.md",
        "needles": ["NEXT2509_0_selected", "PIVOT_TO_SOURCE_WEIGHT_RESIDUAL_BOUND_PACK"],
        "role": "authoritative pivot into this bound-pack checkpoint",
    },
    {
        "source_id": "SRC2510_1_2509_runner",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2509_SOURCE_WEIGHT_RESIDUAL_RUNNER_STATUS.csv",
        "needles": ["SWR2509_0_core_vector", "SWR2509_6_verdict"],
        "role": "core residual vector inherited from the constructor-exhaustion failure",
    },
    {
        "source_id": "SRC2510_2_1065_wA_gate",
        "path": "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md",
        "needles": ["CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED", "WEP1065_4_product"],
        "role": "relative source-weight counterexample and first WEP product gate",
    },
    {
        "source_id": "SRC2510_3_1065_wep_schema",
        "path": "source-intake/mts_residuals/P8_Y5_R10_1065_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv",
        "needles": ["WEP1065_2_delta_w", "WEP1065_4_product"],
        "role": "existing strict WEP product schema for Delta_w times tau_WEP",
    },
    {
        "source_id": "SRC2510_4_2440_wep_k_vector",
        "path": "source-intake/beta-source/docs/WEP_K_VECTOR_MATERIAL_SENSITIVITY_2440_NONCLAIM.csv",
        "needles": ["WKP2440_2_no_cancellation_bound", "PARTIAL_K_VECTOR_NOT_CLAIM_READY"],
        "role": "source-backed material contrast plus missing MTS coupling legs",
    },
    {
        "source_id": "SRC2510_5_570_r10_review_curve",
        "path": "source-intake/local_bounds/P8_Y5_R10_570_REVIEW_CURVE_SUMMARY.csv",
        "needles": ["CS570_0_rows", "not live claim curve"],
        "role": "R10 review candidate curve status, explicitly nonclaim",
    },
    {
        "source_id": "SRC2510_6_2489_ppn_interface",
        "path": "source-intake/local_bounds/PPN_residual_vector_interface_2489_NONCLAIM.csv",
        "needles": ["PPNV2489_7_total_abs", "MISSING_SOURCE_PREFACTOR_ZERO_OR_KERNEL"],
        "role": "PPN residual vector and source-weight leak slots",
    },
    {
        "source_id": "SRC2510_7_2489_ppn_bounds",
        "path": "source-intake/local_bounds/PPN_bound_ledger_2489_NONCLAIM.csv",
        "needles": ["PBOUND2489_0_gamma", "PBOUND2489_4_alpha3"],
        "role": "source-backed comparator bounds for PPN only, not MTS predictions",
    },
    {
        "source_id": "SRC2510_8_2443_shared_projection",
        "path": "source-intake/clocks/branch_locked_local/shared_local_arena_projection_queue_nonclaim_2443.csv",
        "needles": ["SAP2443_2_clocks", "SAP2443_3_PPN"],
        "role": "shared local arena projection queue including clocks and PPN",
    },
    {
        "source_id": "SRC2510_9_2488_orbit_kernel",
        "path": "source-intake/local_bounds/Common_frame_response_kernel_acquisition_2488_NONCLAIM.csv",
        "needles": ["KER2488_2_orbital_light_time", "MISSING_RESPONSE_KERNEL"],
        "role": "orbital/light-time response-kernel acquisition status",
    },
    {
        "source_id": "SRC2510_10_2500_full_ppn",
        "path": "source-intake/local_bounds/Full_PPN_vector_requirements_2500_NONCLAIM.csv",
        "needles": ["VREQ2500_6_total_no_cancellation", "MISSING_SOURCE_PREFACTOR_CLOSURE"],
        "role": "full PPN vector claim requirements and no-cancellation guard",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), "OK"
    except Exception as exc:  # pragma: no cover - validation report path
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", "<br>").replace("|", "\\|")
            cells.append(value)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = ROOT / spec["path"]
        text = read_text(path)
        found = [needle for needle in spec["needles"] if needle in text]
        rows.append(
            base_row(
                source_id=spec["source_id"],
                source_path=spec["path"],
                path_exists=path.exists(),
                required_needles=";".join(spec["needles"]),
                found_needles=";".join(found),
                role=spec["role"],
                source_pass=path.exists() and len(found) == len(spec["needles"]),
            )
        )
    return rows


def component_schema_rows() -> list[dict[str, Any]]:
    components = [
        {
            "component_id": "DWC2510_0_delta_w_species",
            "symbol": "Delta_w_species",
            "definition": "relative source-only species/class weight after removing one universal measured-G normalization",
            "units": "dimensionless",
            "enters_arenas": "WEP;PPN;R10;clock;orbital",
            "zero_route": "parent no-source-only-slot grammar or source-label-forgetting theorem",
            "finite_route": "numeric prior/bound for species/source class contrast with source path",
            "current_status": "MISSING_PARENT_ZERO_OR_NUMERIC_DELTA_W",
        },
        {
            "component_id": "DWC2510_1_beta_w_common_frame",
            "symbol": "beta_w",
            "definition": "common-frame/source normalization slope that can be universal in WEP but visible in PPN/clocks/orbits",
            "units": "dimensionless_or_per_q_unit",
            "enters_arenas": "PPN;clock;orbital;WEP",
            "zero_route": "single public coframe plus fixed readout and source descent",
            "finite_route": "common-frame response kernel K_beta_w with sourced coefficient",
            "current_status": "MISSING_COMMON_FRAME_ZERO_OR_KERNEL_VALUE",
        },
        {
            "component_id": "DWC2510_2_nonHilbert_current",
            "symbol": "J_NH",
            "definition": "non-Hilbert source-current leakage not generated by the same matter action Hilbert variation",
            "units": "source-current units fixed by local field-equation normalization",
            "enters_arenas": "PPN;R10;clock;orbital",
            "zero_route": "same-action Hilbert source owner plus no independent source current",
            "finite_route": "J_NH bound row with equation normalization and arena kernels",
            "current_status": "MISSING_HILBERT_SOURCE_OWNER_OR_NUMERIC_JNH",
        },
        {
            "component_id": "DWC2510_3_projector_measure",
            "symbol": "Delta_mu_projector",
            "definition": "measure/coframe/projector mismatch between parent source and observed local source readout",
            "units": "dimensionless_or_projector_norm",
            "enters_arenas": "WEP;PPN;clock;orbital",
            "zero_route": "measure, coframe, and projection descend through the same quotient object",
            "finite_route": "operator-norm/source-map bound with chosen local frame",
            "current_status": "MISSING_PROJECTOR_DESCENT_OR_NORM_BOUND",
        },
        {
            "component_id": "DWC2510_4_readout_endpoint",
            "symbol": "epsilon_readout_endpoint",
            "definition": "post-variation gauge/readout/endpoint tail that could move a reported local observable",
            "units": "dimensionless",
            "enters_arenas": "PPN;clock;orbital",
            "zero_route": "fixed-before-readout theorem and boundary/endpoint silence",
            "finite_route": "readout transfer kernel with source-backed endpoint coefficient",
            "current_status": "MISSING_READOUT_ENDPOINT_ZERO_OR_BOUND",
        },
        {
            "component_id": "DWC2510_5_boundary_source",
            "symbol": "Q_edge_or_Delta_worldtube",
            "definition": "boundary/worldtube/source-support residual in the active gravitational source charge",
            "units": "source-charge units or fractional GM units after normalization",
            "enters_arenas": "PPN;orbital;R10",
            "zero_route": "worldtube selector, boundary cohomology, and symplectic flux theorem",
            "finite_route": "finite boundary/source-support charge bound with surface convention",
            "current_status": "MISSING_BOUNDARY_SOURCE_ZERO_OR_NUMERIC_BOUND",
        },
        {
            "component_id": "DWC2510_6_total_abs_envelope",
            "symbol": "Delta_w_eff_abs",
            "definition": "componentwise absolute envelope used when no parent identity proves cancellation",
            "units": "arena-dependent residual units after transfer kernel",
            "enters_arenas": "WEP;PPN;R10;clock;orbital",
            "zero_route": "all components parent-zero or exact signed cancellation identity",
            "finite_route": "sum_i abs(T_arena_i component_i) <= accepted bound",
            "current_status": "NO_CANCELLATION_POLICY_ACTIVE_VALUES_MISSING",
        },
    ]
    return [
        base_row(
            score_ready=False,
            valid_prediction_row=False,
            refusal_gate="no component can be scored until zero theorem or numeric finite bound is source-backed",
            **component,
        )
        for component in components
    ]


def arena_requirement_rows() -> list[dict[str, Any]]:
    arenas = [
        {
            "arena_id": "ARENA2510_0_WEP",
            "arena": "MICROSCOPE_WEP_TiPt",
            "observable": "eta_TiPt",
            "bound_object": "eta_AB bound and material charge contrast",
            "residual_law": "abs(eta_source_weight) <= sum_i abs(K_WEP_i Delta_w_eff_i)",
            "available_evidence": "WEP material contrast and eta anchor exist in 2440/1065",
            "missing_inputs": "Delta_w_TiPt;tau_WEP;MTS_to_Damour_Donoghue_charge_map;source leg",
            "acceptance_gate": "numeric eta prediction <= bound with all K_i and Delta_w_i sourced, or parent-zero theorem",
        },
        {
            "arena_id": "ARENA2510_1_R10",
            "arena": "R10_short_range",
            "observable": "alpha(lambda)",
            "bound_object": "alpha(lambda) curve or nonclaim review candidate",
            "residual_law": "abs(alpha_source_weight(lambda)) <= sum_i abs(K_R10_i(lambda) Delta_w_eff_i)",
            "available_evidence": "570 review candidate has 390 nonclaim curve rows; live claim curve remains blocked",
            "missing_inputs": "K_R10(lambda);tau_R10;finite range lambda_w;source/test charges;promoted claim-grade curve",
            "acceptance_gate": "real curve plus source/test product below bound for each lambda; anchors alone cannot claim",
        },
        {
            "arena_id": "ARENA2510_2_PPN",
            "arena": "local_GR_PPN",
            "observable": "gamma,beta,alpha1,alpha2,alpha3,xi",
            "bound_object": "PPN comparator bounds from 2489",
            "residual_law": "||Delta_PPN||_abs <= sum_i abs(K_PPN_i Delta_w_eff_i) compared componentwise",
            "available_evidence": "PPN residual vector and comparator bounds exist, but source-weight kernel is missing",
            "missing_inputs": "C_gamma_source_weight;C_beta_source_weight;preferred-frame/source-exchange kernels;readout GM map",
            "acceptance_gate": "every PPN component below its sourced comparator without absorbing relative weights into fitted GM",
        },
        {
            "arena_id": "ARENA2510_3_clock",
            "arena": "clock_ratios_redshift",
            "observable": "d ln R_ab and redshift residuals",
            "bound_object": "clock sensitivity/protocol bound set",
            "residual_law": "abs(delta_clock) <= sum_i abs(K_clock_i Delta_w_eff_i)",
            "available_evidence": "shared local projection queue includes clock formula skeleton",
            "missing_inputs": "K_alpha/K_mu/K_nuc; tau_clock; source-leg owner; readout descent",
            "acceptance_gate": "clock residual below sourced protocol bound with coefficient sensitivities and units",
        },
        {
            "arena_id": "ARENA2510_4_orbital",
            "arena": "orbital_light_time",
            "observable": "delta a, light-time, ephemeris/source-normalization residual",
            "bound_object": "orbital/light-time residual convention",
            "residual_law": "abs(delta_orbit) <= sum_i abs(K_orbit_i Delta_w_eff_i)",
            "available_evidence": "2488 identifies orbital/light-time kernel as acquisition row",
            "missing_inputs": "orbital response kernel; endpoint projection; ephemeris baseline; measured-GM transfer",
            "acceptance_gate": "no hidden GM absorption; residual is compared in a fixed predeclared ephemeris convention",
        },
        {
            "arena_id": "ARENA2510_5_cross_arena",
            "arena": "cross_arena_consistency",
            "observable": "single Delta_w_eff used everywhere",
            "bound_object": "shared source-weight vector",
            "residual_law": "same component vector must feed WEP/R10/PPN/clock/orbit with arena-specific kernels",
            "available_evidence": "2509 pivot fixes this as the next target",
            "missing_inputs": "one owned component basis and one transfer dictionary",
            "acceptance_gate": "do not tune separate weights per arena; one coupling vector survives all gates",
        },
    ]
    return [
        base_row(
            score_ready=False,
            valid_prediction_row=False,
            refusal_gate="arena row remains nonclaim until every required input is real or parent-zero",
            **arena,
        )
        for arena in arenas
    ]


def acquisition_ledger_rows() -> list[dict[str, Any]]:
    ledger = [
        {
            "input_id": "ACQ2510_0_delta_w_TiPt",
            "quantity": "Delta_w_TiPt",
            "arena": "WEP",
            "units": "dimensionless",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1065_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv",
            "source_row": "WEP1065_2_delta_w",
            "current_value_or_status": "MISSING_PARENT_GRAMMAR_ZERO_OR_NUMERIC_PRIOR",
            "needed_for": "first scoreable source-weight product",
        },
        {
            "input_id": "ACQ2510_1_tau_WEP",
            "quantity": "tau_WEP",
            "arena": "WEP",
            "units": "dimensionless",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1065_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv",
            "source_row": "WEP1065_3_tau_WEP",
            "current_value_or_status": "MISSING_LAB_SOURCE_ORBIT_PROJECTION",
            "needed_for": "first scoreable source-weight product",
        },
        {
            "input_id": "ACQ2510_2_K_WEP_material",
            "quantity": "K_WEP material vector",
            "arena": "WEP",
            "units": "dimensionless material-charge contrast",
            "source_path": "source-intake/beta-source/docs/WEP_K_VECTOR_MATERIAL_SENSITIVITY_2440_NONCLAIM.csv",
            "source_row": "WKP2440_0_DD_material_formula;WKP2440_2_no_cancellation_bound",
            "current_value_or_status": "PARTIAL_MATERIAL_CONTRAST_READY_SOURCE_LEG_MISSING",
            "needed_for": "WEP absolute envelope",
        },
        {
            "input_id": "ACQ2510_3_R10_bound_curve",
            "quantity": "alpha_bound(lambda)",
            "arena": "R10",
            "units": "dimensionless with lambda in meters",
            "source_path": "source-intake/local_bounds/P8_Y5_R10_570_REVIEW_CURVE_SUMMARY.csv",
            "source_row": "CS570_0_rows;CS570_3_min_alpha",
            "current_value_or_status": "REVIEW_CANDIDATE_NONCLAIM_NOT_LIVE_CURVE",
            "needed_for": "R10 scoring only after promotion gate",
        },
        {
            "input_id": "ACQ2510_4_K_R10",
            "quantity": "K_R10(lambda), tau_R10, source/test charges",
            "arena": "R10",
            "units": "dimensionless alpha transfer",
            "source_path": "source-intake/clocks/branch_locked_local/shared_local_arena_projection_queue_nonclaim_2443.csv",
            "source_row": "SAP2443_1_R10",
            "current_value_or_status": "MISSING_FINITE_RANGE_OPERATOR_AND_CHARGES",
            "needed_for": "R10 source-weight product",
        },
        {
            "input_id": "ACQ2510_5_PPN_source_kernel",
            "quantity": "C_gamma_source_weight,C_beta_source_weight,C_alpha_i_source_weight",
            "arena": "PPN",
            "units": "dimensionless PPN residual per source-weight unit",
            "source_path": "source-intake/local_bounds/PPN_residual_vector_interface_2489_NONCLAIM.csv",
            "source_row": "PPNV2489_4_wR;PPNV2489_7_total_abs",
            "current_value_or_status": "MISSING_SOURCE_PREFACTOR_ZERO_OR_KERNEL",
            "needed_for": "local GR PPN residual comparison",
        },
        {
            "input_id": "ACQ2510_6_clock_kernel",
            "quantity": "K_clock_i and tau_clock",
            "arena": "clock",
            "units": "clock residual per source-weight unit",
            "source_path": "source-intake/clocks/branch_locked_local/shared_local_arena_projection_queue_nonclaim_2443.csv",
            "source_row": "SAP2443_2_clocks",
            "current_value_or_status": "MISSING_CLOCK_SOURCE_LEG_OWNER",
            "needed_for": "clock/redshift source-weight bound",
        },
        {
            "input_id": "ACQ2510_7_orbital_kernel",
            "quantity": "K_orbit_i and measured-GM transfer",
            "arena": "orbital",
            "units": "orbital residual per source-weight unit",
            "source_path": "source-intake/local_bounds/Common_frame_response_kernel_acquisition_2488_NONCLAIM.csv",
            "source_row": "KER2488_2_orbital_light_time",
            "current_value_or_status": "MISSING_ORBIT_KERNEL_AND_ENDPOINT_PROJECTION",
            "needed_for": "orbital/light-time source-weight bound",
        },
        {
            "input_id": "ACQ2510_8_no_absorb_G",
            "quantity": "measured-G common-mode policy",
            "arena": "cross_arena",
            "units": "policy gate",
            "source_path": "source-intake/local_bounds/Full_PPN_vector_requirements_2500_NONCLAIM.csv",
            "source_row": "VREQ2500_6_total_no_cancellation",
            "current_value_or_status": "NO_CANCELLATION_AND_NO_RELATIVE_G_ABSORPTION_ACTIVE",
            "needed_for": "all scoring",
        },
    ]
    return [
        base_row(
            status="ACQUISITION_REQUIRED_NONCLAIM",
            score_ready=False,
            valid_prediction_row=False,
            refusal_gate="missing input blocks all source-weight claims",
            **row,
        )
        for row in ledger
    ]


def dryrun_result_rows() -> list[dict[str, Any]]:
    cases = [
        {
            "case_id": "DRY2510_0_all_placeholders",
            "case_description": "all Delta_w_eff components and kernels missing",
            "arena": "all",
            "result_status": "REFUSED_MISSING_COMPONENTS_AND_KERNELS",
            "blocking_markers": "MISSING_PARENT_ZERO_OR_NUMERIC_DELTA_W;MISSING_KERNELS;VALID_FOR_CLAIM_FALSE",
        },
        {
            "case_id": "DRY2510_1_WEP_bound_only",
            "case_description": "eta bound and material contrast exist, but Delta_w_TiPt and tau_WEP are missing",
            "arena": "WEP",
            "result_status": "REFUSED_BOUND_WITHOUT_PREDICTION",
            "blocking_markers": "MISSING_DELTA_W_TiPt;MISSING_TAU_WEP;NO_UNITY_SHORTCUT",
        },
        {
            "case_id": "DRY2510_2_R10_review_curve_only",
            "case_description": "nonclaim review candidate curve exists, but source-weight product and live promotion are missing",
            "arena": "R10",
            "result_status": "REFUSED_NONCLAIM_CURVE_AND_MISSING_PRODUCT",
            "blocking_markers": "CURVE_VALID_FOR_CLAIM_FALSE;MISSING_K_R10;MISSING_TAU_R10",
        },
        {
            "case_id": "DRY2510_3_PPN_bounds_only",
            "case_description": "PPN comparator bounds exist, but response from source weights into PPN vector is missing",
            "arena": "PPN",
            "result_status": "REFUSED_COMPARATOR_WITHOUT_RESPONSE_KERNEL",
            "blocking_markers": "MISSING_SOURCE_PREFACTOR_ZERO_OR_KERNEL;NO_GM_ABSORPTION",
        },
        {
            "case_id": "DRY2510_4_unsigned_theorem_zero",
            "case_description": "pretend Delta_w_eff=0 without parent signature",
            "arena": "all",
            "result_status": "REFUSED_UNSIGNED_ZERO_THEOREM",
            "blocking_markers": "THEOREM_ZERO_REQUIRES_PARENT_SIGNATURE;NO_CLOSURE_ONLY_PROMOTION",
        },
        {
            "case_id": "DRY2510_5_signed_cancellation",
            "case_description": "allow cancellation between components without a parent identity",
            "arena": "all",
            "result_status": "REFUSED_UNSOURCED_CANCELLATION",
            "blocking_markers": "ABSOLUTE_ENVELOPE_REQUIRED;NO_PAIR_CANCELLATION_SHORTCUT",
        },
    ]
    return [
        base_row(
            predicted_value="NOT_COMPUTED",
            comparator_bound="NOT_USED",
            pass_fail="BLOCKED_NONCLAIM",
            score_ready=False,
            valid_prediction_row=False,
            claim_pass=False,
            **case,
        )
        for case in cases
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        {
            "decision_id": "DEC2510_0_result",
            "decision": "SOURCE_WEIGHT_RESIDUAL_BOUND_PACK_STAGED_NONCLAIM",
            "rationale": "2509 rejected another constructor-exhaustion loop; 2510 now gives the exact finite-residual scoring contract.",
            "status": "selected",
        },
        {
            "decision_id": "DEC2510_1_scoring_rule",
            "decision": "ABSOLUTE_ENVELOPE_NO_CANCELLATION",
            "rationale": "Without a parent identity, arena residuals are bounded by sum of absolute transferred components, not by tuned cancellations.",
            "status": "enforced",
        },
        {
            "decision_id": "DEC2510_2_measured_G",
            "decision": "COMMON_NORMALIZATION_ONLY_CAN_BE_ABSORBED",
            "rationale": "A universal constant normalization may define measured G only after universality is proved; relative species/source weights remain physical residuals.",
            "status": "enforced",
        },
        {
            "decision_id": "DEC2510_3_best_next",
            "decision": "FIRST_SOURCE_WEIGHT_INPUT_ROW",
            "rationale": "The shortest route to a real test is the WEP Delta_w_TiPt * tau_WEP product, while PPN source kernels remain the local-GR bridge.",
            "status": "selected",
        },
        {
            "decision_id": "DEC2510_4_claim_ceiling",
            "decision": "NO_WEP_R10_PPN_CLOCK_ORBIT_CLAIM",
            "rationale": "Every arena still has either missing source-weight values, missing transfer kernels, or nonclaim bound data.",
            "status": "enforced",
        },
    ]
    return [
        base_row(
            **decision,
        )
        for decision in decisions
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2510_0_selected",
            selection_status="selected",
            target_file="2511-Y5-R2FR-first-source-weight-input-row-WEP-product-or-PPN-source-kernel.md",
            target_script="scripts/Y5_R2FR_first_source_weight_input_row_WEP_product_or_PPN_source_kernel_2511.py",
            objective=(
                "attempt the nearest real source-weight input: either derive Delta_w_TiPt=0/tau_WEP from parent source-label "
                "forgetting, or stage one strict numeric WEP product row; in parallel keep the PPN source-kernel requirement visible"
            ),
            success_condition=(
                "one row becomes score-ready only if Delta_w_TiPt, tau_WEP, units, source paths, and eta bound are real, or a parent-signed theorem-zero is present"
            ),
            do_not_do=(
                "do not set tau_WEP=1 by convention; do not absorb relative source weights into measured G; do not use the R10 review curve as claim-grade; "
                "do not claim local GR"
            ),
        ),
        base_row(
            route_id="NEXT2510_1_parallel_local_GR",
            selection_status="parallel_after_WEP_input",
            target_file="2511b-Y5-R2FR-PPN-source-weight-response-kernel-and-measured-GM-transfer.md",
            target_script="scripts/Y5_R2FR_PPN_source_weight_response_kernel_and_measured_GM_transfer_2511b.py",
            objective="derive or bound the response from Delta_w_eff into gamma,beta,alpha_i,xi in a fixed measured-GM convention",
            success_condition="PPN source-kernel matrix has units, source path, and no hidden fitted-G absorption",
            do_not_do="do not let WEP cleanliness imply PPN silence; do not re-import GR beta/gamma as proof",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("bound_pack", OUTPUTS["arena_requirements"], BRANCH_COPIES["bound_pack"]),
        ("no_cancellation_policy", OUTPUTS["dryrun_results"], BRANCH_COPIES["no_cancellation_policy"]),
        ("acquisition_queue", OUTPUTS["acquisition_ledger"], BRANCH_COPIES["acquisition_queue"]),
        ("next_source_input", OUTPUTS["next_target"], BRANCH_COPIES["next_source_input"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, src, dst in copies:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        ok, count, message = csv_rows_parse(dst)
        rows.append(
            base_row(
                copy_id=copy_id,
                source=str(src.relative_to(ROOT)),
                destination=str(dst.relative_to(ROOT)),
                copied=dst.exists(),
                parse_ok=ok,
                row_count=count,
                parse_message=message,
            )
        )
    return rows


def falsey(value: Any) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "not_computed", ""}


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name in {"source_register", "validation"}:
            continue
        for row in rows:
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "valid_prediction_row", "claim_pass"):
                if key in row and not falsey(row[key]):
                    return False
    return True


def all_missing_markers_nonclaim(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            has_missing = any("MISSING_" in str(value) for value in row.values())
            if has_missing and (
                not falsey(row.get("valid_for_claim", False))
                or not falsey(row.get("claim_allowed", False))
                or not falsey(row.get("score_ready", False))
            ):
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, detail: str = "") -> None:
        checks.append(
            base_row(
                check_id=check_id,
                status="PASS" if status else "FAIL",
                detail=detail,
                valid_for_claim=False,
                claim_allowed=False,
            )
        )

    source_rows = rows_by_name["source_register"]
    add("VAL2510_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2510_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2510_02_component_schema",
        any(row["component_id"] == "DWC2510_6_total_abs_envelope" for row in rows_by_name["component_schema"]),
        "absolute envelope row present",
    )
    add(
        "VAL2510_03_arena_coverage",
        {"ARENA2510_0_WEP", "ARENA2510_1_R10", "ARENA2510_2_PPN", "ARENA2510_3_clock", "ARENA2510_4_orbital"}.issubset(
            {row["arena_id"] for row in rows_by_name["arena_requirements"]}
        )
        and any(row["arena"] == "cross_arena_consistency" for row in rows_by_name["arena_requirements"]),
        "WEP/R10/PPN/clock/orbital/cross-arena rows present",
    )
    add(
        "VAL2510_04_acquisition_blocks",
        all(
            str(row["status"]) == "ACQUISITION_REQUIRED_NONCLAIM"
            and str(row["score_ready"]) == "False"
            and str(row["valid_prediction_row"]) == "False"
            for row in rows_by_name["acquisition_ledger"]
        ),
        "all acquisition rows remain blocked/nonclaim",
    )
    add(
        "VAL2510_05_dryrun_refuses",
        all(str(row["pass_fail"]) == "BLOCKED_NONCLAIM" and str(row["claim_pass"]) == "False" for row in rows_by_name["dryrun_results"]),
        "no dry-run produces a claim",
    )
    add(
        "VAL2510_06_decision",
        any(row["decision"] == "FIRST_SOURCE_WEIGHT_INPUT_ROW" for row in rows_by_name["decision_ledger"]),
        "next concrete input decision present",
    )
    add(
        "VAL2510_07_next_target",
        any(row["route_id"] == "NEXT2510_0_selected" for row in rows_by_name["next_target"]),
        "selected 2511 route present",
    )
    add("VAL2510_08_no_claim_flags", no_claim_flags(rows_by_name))
    add("VAL2510_09_missing_markers_nonclaim", all_missing_markers_nonclaim(rows_by_name))
    add(
        "VAL2510_10_branch_copies",
        all(str(row["copied"]) == "True" and str(row["parse_ok"]) == "True" for row in rows_by_name["branch_copies"]),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = list(formalization.rglob("*2510*")) if formalization.exists() else []
    add(
        "VAL2510_11_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2510_12_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2510_CSV_{path.stem}", ok, f"{message}; rows={count}")
    for key, path in BRANCH_COPIES.items():
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2510_COPY_CSV_{key}", ok, f"{message}; rows={count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2510_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2510 stages finite source-weight residual bound pack with no claim rows",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2510 — Source-Weight Residual Bound Pack for WEP/R10/PPN/Clocks/Orbit",
                "",
                "**Current verdict:** the coupling wound is now in a proper scoring cage. `2509` says the constructor-exhaustion derivation route is exhausted for the current corpus, so `2510` turns the surviving `Delta_w_eff` source-weight residual into a strict nonclaim bound pack.",
                "",
                "**Not a local-GR claim:** no WEP, R10, PPN, clock, orbital, Newton, or local-GR pass is made here. Every arena still needs either a parent-signed zero theorem or real numeric component values plus arena transfer kernels.",
                "",
                "**Core law:** for each arena `A`, the only allowed finite-residual comparison is",
                "",
                "`|R_A| <= sum_i |T_Ai Delta_w_eff_i| <= B_A`,",
                "",
                "unless a parent-signed identity proves an exact cancellation. A fitted `G` can absorb only a universal common normalization after universality is proved; relative source/species weights remain physical residuals.",
                "",
                "## Source Register",
                md_table(
                    rows_by_name["source_register"],
                    ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"],
                ),
                "",
                "## Delta-w Component Schema",
                md_table(
                    rows_by_name["component_schema"],
                    [
                        "component_id",
                        "symbol",
                        "definition",
                        "units",
                        "enters_arenas",
                        "current_status",
                        "score_ready",
                    ],
                ),
                "",
                "## Arena Bound Requirements",
                md_table(
                    rows_by_name["arena_requirements"],
                    [
                        "arena_id",
                        "arena",
                        "observable",
                        "residual_law",
                        "available_evidence",
                        "missing_inputs",
                        "acceptance_gate",
                    ],
                ),
                "",
                "## Input Acquisition Ledger",
                md_table(
                    rows_by_name["acquisition_ledger"],
                    [
                        "input_id",
                        "quantity",
                        "arena",
                        "units",
                        "source_path",
                        "source_row",
                        "current_value_or_status",
                        "needed_for",
                    ],
                ),
                "",
                "## Nonclaim Dry Run",
                md_table(
                    rows_by_name["dryrun_results"],
                    [
                        "case_id",
                        "arena",
                        "case_description",
                        "result_status",
                        "blocking_markers",
                        "pass_fail",
                        "claim_pass",
                    ],
                ),
                "",
                "## Decision Ledger",
                md_table(
                    rows_by_name["decision_ledger"],
                    ["decision_id", "decision", "rationale", "status"],
                ),
                "",
                "## Next Target",
                md_table(
                    rows_by_name["next_target"],
                    ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"],
                ),
                "",
                "## Validation",
                md_table(rows_by_name["validation"], ["check_id", "status", "detail"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "component_schema": component_schema_rows(),
        "arena_requirements": arena_requirement_rows(),
        "acquisition_ledger": acquisition_ledger_rows(),
        "dryrun_results": dryrun_result_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
