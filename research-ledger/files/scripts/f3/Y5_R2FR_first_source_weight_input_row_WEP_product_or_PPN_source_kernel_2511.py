from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_FIRST_SOURCE_WEIGHT_INPUT_ROW_2511"
CHECKPOINT_ID = "2511"
DOC = ROOT / "2511-Y5-R2FR-first-source-weight-input-row-WEP-product-or-PPN-source-kernel.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2511_SOURCE_REGISTER.csv",
    "zero_attempt": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2511_DELTAW_ZERO_ATTEMPT.csv",
    "wep_product_bound": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2511_WEP_PRODUCT_BOUND_LAW.csv",
    "tau_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2511_TAU_WEP_GATE.csv",
    "ppn_handoff": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2511_PPN_SOURCE_KERNEL_HANDOFF.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2511_NONCLAIM_DRYRUN_RESULTS.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2511_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2511_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2511_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2511_VALIDATION.csv",
}

BRANCH_COPIES = {
    "wep_product_bound": ROOT
    / "source-intake"
    / "local_bounds"
    / "WEP_source_weight_product_bound_2511_NONCLAIM.csv",
    "tau_requirement": ROOT
    / "source-intake"
    / "microscope"
    / "branch_locked_wep"
    / "source"
    / "WEP_tau_lower_bound_requirement_2511_NONCLAIM.csv",
    "ppn_handoff": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "PPN_source_weight_kernel_handoff_2511_NONCLAIM.csv",
    "next_tau": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2511_NEXT_TAU_WEP_OR_PARENT_ZERO_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2511_0_2510_next",
        "path": "2510-Y5-R2FR-source-weight-residual-bound-pack-WEP-R10-PPN-clock-orbit.md",
        "needles": ["NEXT2510_0_selected", "FIRST_SOURCE_WEIGHT_INPUT_ROW"],
        "role": "authoritative 2510 selection of WEP product / PPN kernel route",
    },
    {
        "source_id": "SRC2511_1_local_bound_claims",
        "path": "source-intake/local_bounds/local_bound_claims.csv",
        "needles": ["R1_WEP_source_charge", "2.8e-15"],
        "role": "MICROSCOPE Ti/Pt WEP source-charge proxy bound anchor",
    },
    {
        "source_id": "SRC2511_2_1065_product_schema",
        "path": "source-intake/mts_residuals/P8_Y5_R10_1065_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv",
        "needles": ["WEP1065_2_delta_w", "WEP1065_4_product"],
        "role": "existing WEP Delta_w times tau_WEP product schema",
    },
    {
        "source_id": "SRC2511_3_1065_zero_clauses",
        "path": "source-intake/mts_residuals/P8_Y5_R10_1065_WA_THEOREM_ZERO_CLAUSES.csv",
        "needles": ["WTZ1065_0_strict_no_slot", "WTZ1065_4_verdict"],
        "role": "zero-theorem clauses for relative source weights",
    },
    {
        "source_id": "SRC2511_4_1061_tau_input",
        "path": "source-intake/mts_residuals/P8_Y5_R10_1061_INPUT_FILL_LEDGER.csv",
        "needles": ["INF1061_4_tau_WEP", "MISSING_LAB_SOURCE_ORBIT_PROJECTION"],
        "role": "tau_WEP still missing and cannot be set to one",
    },
    {
        "source_id": "SRC2511_5_1061_material_convention",
        "path": "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv",
        "needles": ["MCON1061_0_test_pair", "MCON1061_2_eta_bound"],
        "role": "Ti/Pt material convention and eta bound anchor",
    },
    {
        "source_id": "SRC2511_6_1608_tau_contract",
        "path": "source-intake/microscope/quarantine/1608/TAU_WEP_READOUT_CONTRACT_NONCLAIM.csv",
        "needles": ["TAU1608_1_amplitude_law", "TAU1608_3_no_unity"],
        "role": "conditional amplitude law and anti-unity tau guard",
    },
    {
        "source_id": "SRC2511_7_2121_tau_min_request",
        "path": "source-intake/source-weight/docs/AFRAME_CMSM_EXPORT_2121_NONCLAIM.csv",
        "needles": ["CMSM2121_6_tau_min", "VR2121_6_no_tau_shortcut"],
        "role": "tau_min lower-bound acquisition requirement",
    },
    {
        "source_id": "SRC2511_8_2489_ppn_source",
        "path": "source-intake/local_bounds/PPN_residual_vector_interface_2489_NONCLAIM.csv",
        "needles": ["PPNV2489_4_wR", "PPNV2489_7_total_abs"],
        "role": "parallel local-GR bridge: PPN source-weight response kernel still missing",
    },
    {
        "source_id": "SRC2511_9_2510_bound_pack",
        "path": "source-intake/local_bounds/Source_weight_residual_bound_pack_2510_NONCLAIM.csv",
        "needles": ["ARENA2510_0_WEP", "ARENA2510_2_PPN"],
        "role": "2510 branch copy of WEP and PPN arena requirements",
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
    except Exception as exc:  # pragma: no cover
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


def zero_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "zero_id": "ZERO2511_0_no_w_slot",
            "target": "Delta_w_TiPt",
            "theorem_attempt": "if parent matter/source language has no inert source-only species scalar w_A, then relative source weights vanish",
            "formal_status": "EXACT_IF_PARENT_SYNTAX_SIGNED",
            "current_gap": "parent syntax/no-source-only-slot not derived from deeper MTS primitives",
            "verdict": "NOT_PROMOTED",
        },
        {
            "zero_id": "ZERO2511_1_common_mode",
            "target": "Delta_w_TiPt",
            "theorem_attempt": "if w_A=w_common for all species and is range/time/frame independent, common normalization may be calibrated into G",
            "formal_status": "EXACT_CONDITIONAL_COMMON_MODE",
            "current_gap": "universality is the missing theorem; relative pieces cannot be absorbed into measured G",
            "verdict": "NOT_PROMOTED",
        },
        {
            "zero_id": "ZERO2511_2_field_redefinition",
            "target": "Delta_w_TiPt",
            "theorem_attempt": "classify apparent w_A as field normalization after canonical kinetic and measured coupling quotient",
            "formal_status": "LOOPHOLE_AUDITED",
            "current_gap": "interactions, composite matter, quantum normalization, and source-action scale can leave a residual source-only factor",
            "verdict": "NOT_PROMOTED",
        },
        {
            "zero_id": "ZERO2511_3_tau_zero",
            "target": "P_WEP=Delta_w_TiPt*tau_WEP",
            "theorem_attempt": "tau_WEP=0 would make WEP blind to this component",
            "formal_status": "NOT_A_LOCAL_GR_ZERO",
            "current_gap": "tau_WEP=0 would not remove PPN/R10/clock/orbital source-weight residuals",
            "verdict": "HELD_AS_WEP_ONLY_BLINDNESS_NOT_THEORY_ZERO",
        },
        {
            "zero_id": "ZERO2511_4_verdict",
            "target": "P_WEP_relative_source_weight",
            "theorem_attempt": "Delta_w_TiPt=0 or tau_WEP=0 from parent-signed geometry/source grammar",
            "formal_status": "THEOREM_ZERO_NOT_PARENT_SIGNED",
            "current_gap": "WEP route must use a product-bound law until source-label forgetting or tau nondegeneracy is sourced",
            "verdict": "PRODUCT_BOUND_ROUTE_SELECTED_NONCLAIM",
        },
    ]
    return [
        base_row(
            score_ready=False,
            valid_prediction_row=False,
            **row,
        )
        for row in rows
    ]


def wep_product_bound_rows() -> list[dict[str, Any]]:
    eta_bound = 2.8e-15
    one_sigma = 2.74590604355e-15
    rows = [
        {
            "product_id": "WPROD2511_0_observed_bound",
            "quantity": "eta_TiPt_source_charge_bound",
            "law": "abs(eta_TiPt_source_charge) <= 2.8e-15",
            "numeric_value": eta_bound,
            "one_sigma": one_sigma,
            "units": "dimensionless",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R1_WEP_source_charge",
            "status": "SOURCE_BACKED_BOUND_ANCHOR_NOT_MTS_PREDICTION",
            "score_ready": False,
        },
        {
            "product_id": "WPROD2511_1_direct_product_law",
            "quantity": "P_WEP_relative_source_weight",
            "law": "P_WEP = abs(Delta_w_TiPt * tau_WEP)",
            "numeric_value": "MISSING_DELTA_W_TiPt_AND_TAU_WEP",
            "one_sigma": "not_applicable",
            "units": "dimensionless",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1065_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv",
            "source_row": "WEP1065_4_product",
            "status": "PRODUCT_DEFINITION_READY_VALUES_MISSING",
            "score_ready": False,
        },
        {
            "product_id": "WPROD2511_2_exact_component_bound",
            "quantity": "component_product_ceiling",
            "law": "abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15 for the isolated WEP source-weight leg",
            "numeric_value": eta_bound,
            "one_sigma": one_sigma,
            "units": "dimensionless product ceiling",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv;source-intake/mts_residuals/P8_Y5_R10_1065_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv",
            "source_row": "R1_WEP_source_charge;WEP1065_4_product",
            "status": "EXACT_PRODUCT_BOUND_LAW_NONCLAIM",
            "score_ready": False,
        },
        {
            "product_id": "WPROD2511_3_amplitude_inversion",
            "quantity": "Delta_w_TiPt_width",
            "law": "if abs(tau_WEP) >= tau_min > 0 then abs(Delta_w_TiPt) <= 2.8e-15/tau_min",
            "numeric_value": "MISSING_TAU_MIN",
            "one_sigma": "not_applicable",
            "units": "dimensionless source-weight width",
            "source_path": "source-intake/microscope/quarantine/1608/TAU_WEP_READOUT_CONTRACT_NONCLAIM.csv",
            "source_row": "TAU1608_1_amplitude_law",
            "status": "EXACT_CONDITIONAL_LAW_TAU_MIN_MISSING",
            "score_ready": False,
        },
        {
            "product_id": "WPROD2511_4_total_envelope_guard",
            "quantity": "WEP_absolute_envelope",
            "law": "abs(Delta_w_TiPt*tau_WEP)+sum_other_abs_WEP_legs <= eta_bound; no cancellation between legs",
            "numeric_value": "MISSING_OTHER_LEG_BOUNDS",
            "one_sigma": "not_applicable",
            "units": "dimensionless eta envelope",
            "source_path": "source-intake/local_bounds/Source_weight_residual_bound_pack_2510_NONCLAIM.csv",
            "source_row": "ARENA2510_0_WEP",
            "status": "TOTAL_WEP_CLAIM_BLOCKED_OTHER_LEGS_RETAINED",
            "score_ready": False,
        },
    ]
    return [
        base_row(
            valid_prediction_row=False,
            claim_pass=False,
            **row,
        )
        for row in rows
    ]


def tau_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "tau_id": "TAUG2511_0_definition",
            "quantity": "tau_WEP",
            "requirement": "branch-locked lab/source/orbit/readout projection converting Delta_w_TiPt into eta_TiPt",
            "current_status": "FORMAL_DEFINITION_ONLY",
            "required_source": "official readout arrays or parent geometry/source nondegeneracy theorem",
            "blocks": "WEP product cannot become a Delta_w width",
        },
        {
            "tau_id": "TAUG2511_1_tau_min",
            "quantity": "tau_min",
            "requirement": "strictly positive lower bound abs(tau_WEP)>=tau_min>0",
            "current_status": "MISSING_TAU_MIN",
            "required_source": "P_WEP_tau_min_lower_bound.csv or parent nondegeneracy proof",
            "blocks": "abs(Delta_w_TiPt)<=2.8e-15/tau_min cannot be evaluated",
        },
        {
            "tau_id": "TAUG2511_2_no_unity",
            "quantity": "tau_WEP=1 shortcut",
            "requirement": "forbidden unless derived from the actual readout normalization",
            "current_status": "SHORTCUT_FORBIDDEN",
            "required_source": "source/readout normalization calculation",
            "blocks": "fake WEP pass and fake Delta_w bound",
        },
        {
            "tau_id": "TAUG2511_3_tau_zero",
            "quantity": "tau_WEP=0",
            "requirement": "can only mean WEP blindness, not universal source-weight safety",
            "current_status": "NOT_A_CROSS_ARENA_ZERO",
            "required_source": "PPN/R10/clock/orbit kernels still required",
            "blocks": "local-GR claim from WEP alone",
        },
        {
            "tau_id": "TAUG2511_4_verdict",
            "quantity": "tau_WEP gate",
            "requirement": "derive tau map or acquire tau_min before any Delta_w numeric width",
            "current_status": "TAU_GATE_BLOCKS_NUMERIC_DELTAW_WIDTH",
            "required_source": "2512 target",
            "blocks": "score_ready remains false",
        },
    ]
    return [
        base_row(
            score_ready=False,
            valid_prediction_row=False,
            **row,
        )
        for row in rows
    ]


def ppn_handoff_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "ppn_id": "PPNH2511_0_source_weight_gamma",
            "observable": "gamma_minus_1",
            "needed_kernel": "C_gamma_source_weight",
            "current_status": "MISSING_SOURCE_PREFACTOR_ZERO_OR_KERNEL",
            "why_parallel": "WEP can bind a product, but local GR needs the PPN response of the same source-weight vector",
        },
        {
            "ppn_id": "PPNH2511_1_source_weight_beta",
            "observable": "beta_minus_1",
            "needed_kernel": "C_beta_source_weight",
            "current_status": "MISSING_SECOND_ORDER_SOURCE_RESPONSE_KERNEL",
            "why_parallel": "beta is the second-order local-GR gate and cannot be inferred from WEP",
        },
        {
            "ppn_id": "PPNH2511_2_preferred_frame_exchange",
            "observable": "alpha1,alpha2,alpha3,xi",
            "needed_kernel": "preferred-frame/source-exchange/endpoint kernel",
            "current_status": "MISSING_VECTOR_DOMAIN_SOURCE_KERNEL",
            "why_parallel": "relative weights can hide in WEP but show in source exchange, endpoint, or momentum-flux channels",
        },
        {
            "ppn_id": "PPNH2511_3_measured_GM",
            "observable": "source-normalized Newton/PPN comparison",
            "needed_kernel": "fixed measured-GM transfer map",
            "current_status": "MISSING_NO_ABSORB_RELATIVE_WEIGHT_PROOF",
            "why_parallel": "common normalization can define G only after universality; relative weights must remain observable residuals",
        },
    ]
    return [
        base_row(
            score_ready=False,
            valid_prediction_row=False,
            **row,
        )
        for row in rows
    ]


def dryrun_result_rows() -> list[dict[str, Any]]:
    cases = [
        {
            "case_id": "DRY2511_0_bound_anchor_only",
            "case_description": "use eta_bound=2.8e-15 without Delta_w or tau_WEP",
            "result_status": "REFUSED_BOUND_ANCHOR_NOT_PREDICTION",
            "blocking_markers": "MISSING_DELTA_W_TiPt;MISSING_TAU_WEP",
        },
        {
            "case_id": "DRY2511_1_product_law",
            "case_description": "derive product ceiling abs(Delta_w_TiPt*tau_WEP)<=2.8e-15",
            "result_status": "ACCEPT_PRODUCT_BOUND_LAW_NONCLAIM",
            "blocking_markers": "PRODUCT_BOUND_NOT_MTS_PREDICTION;VALID_FOR_CLAIM_FALSE",
        },
        {
            "case_id": "DRY2511_2_invert_without_tau_min",
            "case_description": "attempt Delta_w width from product ceiling with tau_min missing",
            "result_status": "REFUSED_MISSING_TAU_MIN",
            "blocking_markers": "MISSING_TAU_MIN;NO_TAU_UNITY_SHORTCUT",
        },
        {
            "case_id": "DRY2511_3_unsigned_zero",
            "case_description": "promote Delta_w_TiPt=0 from the no-source-only-slot grammar without parent signature",
            "result_status": "REFUSED_UNSIGNED_THEOREM_ZERO",
            "blocking_markers": "THEOREM_ZERO_NOT_PARENT_SIGNED",
        },
        {
            "case_id": "DRY2511_4_wep_to_local_gr",
            "case_description": "infer PPN/local-GR safety from WEP product bound",
            "result_status": "REFUSED_WRONG_ARENA_INFERENCE",
            "blocking_markers": "MISSING_PPN_SOURCE_KERNEL;WEP_NOT_LOCAL_GR",
        },
    ]
    return [
        base_row(
            predicted_value="NOT_COMPUTED",
            comparator_bound="2.8e-15 for WEP product only",
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
            "decision_id": "DEC2511_0_gain",
            "decision": "WEP_PRODUCT_AMPLITUDE_LAW_DERIVED",
            "rationale": "The exact component law is now explicit: abs(Delta_w_TiPt*tau_WEP)<=2.8e-15 for the isolated WEP source-weight leg.",
            "status": "selected_nonclaim",
        },
        {
            "decision_id": "DEC2511_1_limit",
            "decision": "DELTAW_WIDTH_NOT_NUMERIC",
            "rationale": "A standalone Delta_w_TiPt width requires tau_min>0 or parent zero; tau_WEP cannot be set to one.",
            "status": "blocked_by_tau_min",
        },
        {
            "decision_id": "DEC2511_2_theorem",
            "decision": "NO_SOURCE_ONLY_SLOT_NOT_SIGNED",
            "rationale": "The desired zero theorem remains conditional; relative weights survive as finite coupling debt.",
            "status": "retained",
        },
        {
            "decision_id": "DEC2511_3_ppn",
            "decision": "PPN_SOURCE_KERNEL_REMAINS_PARALLEL_LOCAL_GR_GATE",
            "rationale": "WEP product bounds cannot prove beta/gamma/preferred-frame closure or Newton/GR reduction.",
            "status": "retained",
        },
        {
            "decision_id": "DEC2511_4_best_next",
            "decision": "TAU_WEP_LOWER_BOUND_OR_PARENT_NONDEGENERACY",
            "rationale": "The next real unlock is tau_min or a parent proof that the WEP projection is nondegenerate/zero in the right way.",
            "status": "selected",
        },
    ]
    return [base_row(**decision) for decision in decisions]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2511_0_selected",
            selection_status="selected",
            target_file="2512-Y5-R2FR-tau-WEP-lower-bound-or-parent-nondegeneracy-proof.md",
            target_script="scripts/Y5_R2FR_tau_WEP_lower_bound_or_parent_nondegeneracy_proof_2512.py",
            objective="derive tau_WEP=0/nonzero from parent geometry or acquire a source-backed tau_min lower bound; then convert the WEP product ceiling into a Delta_w_TiPt width only if legitimate",
            success_condition="tau_WEP has parent-signed zero/nonzero theorem or tau_min>0 with source path, units, sign/absolute convention, and no unity shortcut",
            do_not_do="do not assume tau_WEP=1; do not treat WEP blindness as PPN/R10 silence; do not claim local GR",
        ),
        base_row(
            route_id="NEXT2511_1_parallel_ppn",
            selection_status="parallel_after_tau",
            target_file="2512b-Y5-R2FR-source-weight-PPN-response-kernel-fixed-GM-map.md",
            target_script="scripts/Y5_R2FR_source_weight_PPN_response_kernel_fixed_GM_map_2512b.py",
            objective="derive or bound how the same Delta_w_eff vector enters gamma,beta,alpha_i,xi under a fixed measured-GM convention",
            success_condition="PPN response kernel has units and source path and cannot absorb relative source weights into fitted G",
            do_not_do="do not infer local GR from WEP; do not import GR as the response kernel",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("wep_product_bound", OUTPUTS["wep_product_bound"], BRANCH_COPIES["wep_product_bound"]),
        ("tau_requirement", OUTPUTS["tau_gate"], BRANCH_COPIES["tau_requirement"]),
        ("ppn_handoff", OUTPUTS["ppn_handoff"], BRANCH_COPIES["ppn_handoff"]),
        ("next_tau", OUTPUTS["next_target"], BRANCH_COPIES["next_tau"]),
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
    add("VAL2511_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2511_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2511_02_zero_not_promoted",
        any(row["zero_id"] == "ZERO2511_4_verdict" and row["verdict"] == "PRODUCT_BOUND_ROUTE_SELECTED_NONCLAIM" for row in rows_by_name["zero_attempt"]),
        "zero theorem remains unsigned",
    )
    add(
        "VAL2511_03_product_law",
        any(row["product_id"] == "WPROD2511_2_exact_component_bound" and str(row["numeric_value"]) == "2.8e-15" for row in rows_by_name["wep_product_bound"]),
        "component product ceiling present",
    )
    add(
        "VAL2511_04_tau_blocks_width",
        any(row["tau_id"] == "TAUG2511_1_tau_min" and row["current_status"] == "MISSING_TAU_MIN" for row in rows_by_name["tau_gate"])
        and any(row["product_id"] == "WPROD2511_3_amplitude_inversion" and row["numeric_value"] == "MISSING_TAU_MIN" for row in rows_by_name["wep_product_bound"]),
        "tau_min missing blocks Delta_w width",
    )
    add(
        "VAL2511_05_ppn_handoff",
        any(row["ppn_id"] == "PPNH2511_0_source_weight_gamma" for row in rows_by_name["ppn_handoff"])
        and any(row["ppn_id"] == "PPNH2511_3_measured_GM" for row in rows_by_name["ppn_handoff"]),
        "PPN local-GR handoff rows present",
    )
    add(
        "VAL2511_06_dryruns_block_claims",
        all(str(row["pass_fail"]) == "BLOCKED_NONCLAIM" and str(row["claim_pass"]) == "False" for row in rows_by_name["dryrun_results"]),
        "dry runs remain nonclaim",
    )
    add(
        "VAL2511_07_next_target",
        any(row["route_id"] == "NEXT2511_0_selected" for row in rows_by_name["next_target"]),
        "tau lower-bound route selected",
    )
    add("VAL2511_08_no_claim_flags", no_claim_flags(rows_by_name))
    add(
        "VAL2511_09_branch_copies",
        all(str(row["copied"]) == "True" and str(row["parse_ok"]) == "True" for row in rows_by_name["branch_copies"]),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = list(formalization.rglob("*2511*")) if formalization.exists() else []
    add(
        "VAL2511_10_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2511_11_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2511_CSV_{path.stem}", ok, f"{message}; rows={count}")
    for key, path in BRANCH_COPIES.items():
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2511_COPY_CSV_{key}", ok, f"{message}; rows={count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2511_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2511 derives WEP source-weight product amplitude law and blocks standalone Delta_w claim without tau_min",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2511 — First Source-Weight Input Row: WEP Product Law or PPN Source Kernel",
                "",
                "**Current verdict:** one real thing is derived: the isolated WEP source-weight product must obey `|Delta_w_TiPt tau_WEP| <= 2.8e-15`. That is a product/amplitude law, not a standalone MTS prediction and not a local-GR pass.",
                "",
                "**Key limit:** `|Delta_w_TiPt| <= 2.8e-15/tau_min` only follows if `|tau_WEP| >= tau_min > 0` is sourced or parent-derived. `tau_WEP=1` is explicitly forbidden as a shortcut.",
                "",
                "**PPN warning:** even a clean WEP product does not prove `gamma=beta=1`; the same source-weight vector still needs a PPN response kernel in a fixed measured-GM convention.",
                "",
                "## Source Register",
                md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"]),
                "",
                "## Delta-w Zero Attempt",
                md_table(rows_by_name["zero_attempt"], ["zero_id", "target", "theorem_attempt", "formal_status", "current_gap", "verdict"]),
                "",
                "## WEP Product Bound Law",
                md_table(rows_by_name["wep_product_bound"], ["product_id", "quantity", "law", "numeric_value", "units", "status", "score_ready"]),
                "",
                "## Tau Gate",
                md_table(rows_by_name["tau_gate"], ["tau_id", "quantity", "requirement", "current_status", "required_source", "blocks"]),
                "",
                "## PPN Handoff",
                md_table(rows_by_name["ppn_handoff"], ["ppn_id", "observable", "needed_kernel", "current_status", "why_parallel"]),
                "",
                "## Nonclaim Dry Run",
                md_table(rows_by_name["dryrun_results"], ["case_id", "case_description", "result_status", "blocking_markers", "pass_fail", "claim_pass"]),
                "",
                "## Decision Ledger",
                md_table(rows_by_name["decision_ledger"], ["decision_id", "decision", "rationale", "status"]),
                "",
                "## Next Target",
                md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"]),
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
        "zero_attempt": zero_attempt_rows(),
        "wep_product_bound": wep_product_bound_rows(),
        "tau_gate": tau_gate_rows(),
        "ppn_handoff": ppn_handoff_rows(),
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
