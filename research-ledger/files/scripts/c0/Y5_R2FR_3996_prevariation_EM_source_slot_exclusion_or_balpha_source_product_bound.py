from __future__ import annotations

import csv
import math
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3996"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3996-Y5-R2FR-prevariation-EM-source-slot-exclusion-or-balpha-source-product-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3996_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3996_PREVARIATION_SOURCE_SLOT_EXCLUSION_THEOREM.csv",
    "types": SRC / "P8_Y5_R2FR_3996_SOURCE_SLOT_TYPE_DECISION_TABLE.csv",
    "products": SRC / "P8_Y5_R2FR_3996_BALPHA_SOURCE_PRODUCT_VECTOR.csv",
    "cases": SRC / "P8_Y5_R2FR_3996_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_3996_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_3996_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3996_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3996_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3996_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3996_VALIDATION.csv",
}

NEXT_DOC = "3997-Y5-R2FR-common-G-source-calibration-owner-or-Gdot-PPN-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3997_common_G_source_calibration_owner_or_Gdot_PPN_bound.py"


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
        ("SRC3996_00_3995_next", SRC / "P8_Y5_R2FR_3995_NEXT_TARGET.csv", "NEXT3995_0", "3995 handoff"),
        ("SRC3996_01_3995_trichotomy", SRC / "P8_Y5_R2FR_3995_CURRENT_NORMALIZATION_GAUGE_TRICHOTOMY.csv", "TRI3995_2_physical_source_slot", "physical source-slot fork"),
        ("SRC3996_02_3995_decomp", SRC / "P8_Y5_R2FR_3995_ZG_ZERO_THEOREM_OR_RESIDUAL_DECOMP.csv", "ZGD3995_4_source_slot_tail", "source-tail decomposition"),
        ("SRC3996_03_3995_bound", SRC / "P8_Y5_R2FR_3995_JOINT_ALPHA_F2_CURRENT_BOUND_ROWS.csv", "JAB3995_4_source_slot_envelope", "source-tail envelope"),
        ("SRC3996_04_3995_alpha", SRC / "P8_Y5_R2FR_3995_JOINT_ALPHA_F2_CURRENT_BOUND_ROWS.csv", "JAB3995_3_alpha_channel_proxy", "alpha channel proxy"),
        ("SRC3996_05_3989_theorem", SRC / "P8_Y5_R2FR_3989_MATTER_DESCENT_NO_SOURCE_PREFACTOR_THEOREM.csv", "NP3989_0_no_prefactor_criterion", "no-source-prefactor theorem"),
        ("SRC3996_06_3989_bound", SRC / "P8_Y5_R2FR_3989_DESCENT_PREFAC_PPN_BOUND_ROWS.csv", "NPB3989_1_descent_prefactor_total", "descent prefactor bound"),
        ("SRC3996_07_3990_nohom", SRC / "P8_Y5_R2FR_3990_NO_HOM_GRAMMAR_THEOREM.csv", "NHG3990_0_target", "no-Hom grammar theorem"),
        ("SRC3996_08_3562_nohom", SRC / "P8_Y5_R2FR_3562_NO_SOURCE_ONLY_HOM_THEOREM.csv", "NH3562_1_noHom_relative_weight_theorem", "source-only Hom theorem"),
        ("SRC3996_09_3509_functor", SRC / "P8_Y5_R2FR_3509_NO_SOURCE_ONLY_MATTER_FUNCTOR_THEOREM.csv", "NSF3509_6_verdict", "no-source-only matter functor"),
        ("SRC3996_10_3509_residuals", SRC / "P8_Y5_R2FR_3509_SOURCE_SLOT_RESIDUAL_VECTOR.csv", "NSSR3509_1_w_common", "source-slot residual vector"),
        ("SRC3996_11_3870_theorem", SRC / "P8_Y5_R2FR_3870_NO_SOURCE_SLOT_THEOREM.csv", "NST3870_1_forbidden_source_slots", "typed source-slot theorem"),
        ("SRC3996_12_3870_types", SRC / "P8_Y5_R2FR_3870_SOURCE_SLOT_CLASSIFICATION.csv", "CLS3870_5_kappa", "source-slot classification"),
        ("SRC3996_13_3877_tail", SRC / "P8_Y5_R2FR_3877_READOUT_SOURCE_SLOT_RAD_TAIL_CONTRACT.csv", "RTC3877_2_source_slot", "readout/source/radiative tail contract"),
        ("SRC3996_14_3960_grammar", SRC / "P8_Y5_R2FR_3960_SOURCE_CURRENT_ZERO_GRAMMAR.csv", "SCG3960_2_source_label_forgetting", "source-current zero grammar"),
        ("SRC3996_15_3988_ppn", SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_ORIGIN_AND_PPN_THEOREM.csv", "JPPN3988_3_PPN_envelope", "PPN source stability envelope"),
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


def alpha_inputs() -> dict[str, float]:
    bounds = read_csv(SRC / "P8_Y5_R2FR_3995_JOINT_ALPHA_F2_CURRENT_BOUND_ROWS.csv")
    results = read_csv(SRC / "P8_Y5_R2FR_3995_EVALUATOR_RESULTS.csv")
    alpha_bound = None
    eta_bound = None
    readout_floor = None
    dd_weight = None
    for row in bounds:
        if row.get("bound_id") == "JAB3995_3_alpha_channel_proxy":
            alpha_bound = float(row["numeric_value"])
    for row in results:
        if row.get("case_id") == "CASE3995_2_alpha_bound_current_gauge":
            eta_bound = float(row["eta_bound_abs"])
            readout_floor = float(row["readout_floor"])
            dd_weight = float(row["DD_weight_abs"])
    if alpha_bound is None or eta_bound is None or readout_floor is None or dd_weight is None:
        raise RuntimeError("3995 alpha source-product inputs missing")
    return {
        "alpha_bound": alpha_bound,
        "eta_bound": eta_bound,
        "readout_floor": readout_floor,
        "dd_weight_abs": dd_weight,
    }


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "PSS3996_0_target",
            "claim_piece": "prevariation source-slot exclusion theorem",
            "mathematical_form": "If Arg(S_matter)={q-basic observed geometry/coframe, parent gauge connection, matter fields, fixed representation labels, universal constants}, variation is before readout, ordinary matter lives on one connected action-density line, and Hom_parent(Species/Hidden/ReadoutWorldtube,ActiveSourcePrefactor)=CommonConst only, then D ln c_A_pre=D ln w_A^rel=D ln kappa_A=hidden_marker_source=0.",
            "derived_result": "relative prevariation EM/source slots are not legal action arguments under the typed parent grammar",
            "status": "EXACT_CONDITIONAL_SOURCE_SLOT_ZERO_THEOREM_NOT_PARENT_SIGNED",
            "source_path": str(SRC / "P8_Y5_R2FR_3990_NO_HOM_GRAMMAR_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PSS3996_1_common_scalar_reclassification",
            "claim_piece": "common source/action scalar",
            "mathematical_form": "w_A=w_* for all ordinary sectors gives T_source=w_* T_total; composition differences vanish, but D ln w_* is a universal G_ref/source-calibration residual until parent-fixed or bounded.",
            "derived_result": "the GR-like common coupling is separated from WEP/R10 composition poison",
            "status": "EXACT_CLASSIFICATION_COMMON_G_GATE_REMAINS",
            "source_path": str(SRC / "P8_Y5_R2FR_3562_NO_SOURCE_ONLY_HOM_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PSS3996_2_real_field_exception",
            "claim_piece": "real field/current exception",
            "mathematical_form": "If c_A,w_A,kappa_A are generated by a real parent field/current or by an arena kernel before variation, the term is not erased; it becomes an explicit finite source-product coefficient.",
            "derived_result": "the theorem forbids inert smuggled slots, not real dynamics",
            "status": "COUNTERMODEL_BRANCH_RETAINED_AS_FINITE_VECTOR",
            "source_path": str(SRC / "P8_Y5_R2FR_3870_NO_SOURCE_SLOT_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PSS3996_3_bound_law",
            "claim_piece": "b_alpha/source-tail product law",
            "mathematical_form": "B_EM_source = |b_alpha|+|D ln c_A_pre|+|D ln w_A^rel|+|D ln kappa_A|+|D ln R_A|+|z_rad| and eta_EM_source <= readout_floor |Qe_Earth DeltaQe| B_EM_source.",
            "derived_result": "the finite branch is now an executable no-cancellation source-product vector",
            "status": "EXACT_BOUND_SCHEMA_NUMERIC_PROXY_AVAILABLE",
            "source_path": str(SRC / "P8_Y5_R2FR_3877_READOUT_SOURCE_SLOT_RAD_TAIL_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PSS3996_4_verdict",
            "claim_piece": "current 3996 verdict",
            "mathematical_form": "Current corpus has the conditional zero theorem plus a finite product vector; it does not parent-sign the grammar strongly enough to claim local-GR source closure.",
            "derived_result": "relative source-slot poison is narrowed to typed parent grammar; the remaining universal scalar is the next G/source calibration gate",
            "status": "SOURCE_SLOT_ROUTE_REDUCED_NO_LOCAL_GR_CLAIM",
            "source_path": str(SRC / "P8_Y5_R2FR_3989_MATTER_DESCENT_NO_SOURCE_PREFACTOR_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def type_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "type_id": "TYPE3996_0_w_relative",
            "slot": "D ln w_A^rel",
            "classification": "FORBIDDEN_IF_CONNECTED_DENSITY_LINE_AND_NO_HOM",
            "zero_condition": "single parent ordinary-matter action-density line; no species-label to active-source prefactor Hom",
            "if_present": "finite WEP/R10/PPN source coefficient",
            "source_path": str(SRC / "P8_Y5_R2FR_3509_SOURCE_SLOT_RESIDUAL_VECTOR.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "type_id": "TYPE3996_1_w_common",
            "slot": "D ln w_*",
            "classification": "COMMON_G_SOURCE_CALIBRATION_NOT_COMPOSITION_SOURCE",
            "zero_condition": "parent action-scale/G_ref owner or observational Gdot/source-calibration bound",
            "if_present": "universal Newton/G calibration drift, not WEP relative source charge by itself",
            "source_path": str(SRC / "P8_Y5_R2FR_3509_SOURCE_SLOT_RESIDUAL_VECTOR.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "type_id": "TYPE3996_2_c_pre",
            "slot": "D ln c_A_pre",
            "classification": "FORBIDDEN_IF_VARIATION_BEFORE_READOUT_AND_NO_CURRENT_SLOT",
            "zero_condition": "same-current owner and no prevariation current multiplier in matter grammar",
            "if_present": "current/source normalization residual",
            "source_path": str(SRC / "P8_Y5_R2FR_3870_SOURCE_SLOT_CLASSIFICATION.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "type_id": "TYPE3996_3_kappa_A",
            "slot": "D ln kappa_A",
            "classification": "FORBIDDEN_IF_SOURCE_FUNCTOR_FORGETS_LABELS",
            "zero_condition": "active source functor factors through total Hilbert source plus declared improvements",
            "if_present": "active source selector residual",
            "source_path": str(SRC / "P8_Y5_R2FR_3960_SOURCE_CURRENT_ZERO_GRAMMAR.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "type_id": "TYPE3996_4_readout",
            "slot": "D ln R_A",
            "classification": "POST_VARIATION_OR_ARENA_TRANSFER_TAIL",
            "zero_condition": "readout naturality/domain lock after variation",
            "if_present": "finite readout transfer residual",
            "source_path": str(SRC / "P8_Y5_R2FR_3877_READOUT_SOURCE_SLOT_RAD_TAIL_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "type_id": "TYPE3996_5_radiative",
            "slot": "z_rad",
            "classification": "EFFECTIVE_ACTION_OR_RADIOUT_REGENERATION_TAIL",
            "zero_condition": "radiative/image stability and boundary flux closure",
            "if_present": "finite radiative/readout current residual",
            "source_path": str(SRC / "P8_Y5_R2FR_3877_READOUT_SOURCE_SLOT_RAD_TAIL_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def product_rows(timestamp: str) -> list[dict[str, Any]]:
    alpha = alpha_inputs()
    return [
        {
            "product_id": "BSP3996_0_invariant_source_product",
            "target": "B_EM_source",
            "formula": "|b_alpha|+|Dln c_pre|+|Dln w_rel|+|Dln kappa_A|+|Dln R_A|+|z_rad|",
            "numeric_value": "MISSING_PARENT_COEFFICIENT_VECTOR",
            "units": "dimensionless per normalized Xhat",
            "status": "EXECUTABLE_PRODUCT_VECTOR_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "product_id": "BSP3996_1_DD_proxy_projection",
            "target": "eta_EM_source_proxy",
            "formula": "eta_EM_source <= readout_floor*|Qe_Earth DeltaQe|*B_EM_source",
            "numeric_value": f"readout_floor={alpha['readout_floor']:.12e};DD_weight={alpha['dd_weight_abs']:.12e};eta_bound={alpha['eta_bound']:.12e}",
            "units": "dimensionless eta",
            "status": "NUMERIC_PROXY_PROJECTOR_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "product_id": "BSP3996_2_source_slot_zero_branch",
            "target": "B_EM_source",
            "formula": "B_EM_source=|b_alpha| if source-slot theorem and readout/radiative closure are signed",
            "numeric_value": "CONDITIONAL_ZERO_BRANCH_UNSIGNED",
            "units": "dimensionless",
            "status": "THEOREM_BRANCH_READY_NOT_CLAIMED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "product_id": "BSP3996_3_common_scalar_branch",
            "target": "Dln w_common",
            "formula": "w_common shifts universal source/G calibration and must be owned by G_ref/action-scale or bounded by Gdot/PPN/source calibration",
            "numeric_value": "MISSING_COMMON_G_OWNER_OR_GDOT_BOUND",
            "units": "dimensionless or time/range derivative depending domain",
            "status": "NEXT_GATE_COMMON_G_CALIBRATION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "product_id": "BSP3996_4_PPN_link",
            "target": "epsilon_descent_prefactor_3996",
            "formula": "epsilon_descent_prefactor_3996 <= B_source_slot_relative + B_readout + B_rad + R_matter_descent + R_nonHilbert",
            "numeric_value": "SYMBOLIC_PPN_LINK",
            "units": "absolute PPN/source residual",
            "status": "PPN_HANDOFF_REFINED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    alpha = alpha_inputs()
    a = alpha["alpha_bound"]
    return [
        {
            "case_id": "CASE3996_0_source_slot_theorem_zero",
            "route": "zero_theorem",
            "b_alpha": 0.0,
            "dln_c_pre": 0.0,
            "dln_w_relative": 0.0,
            "dln_kappa_A": 0.0,
            "dln_readout_R": 0.0,
            "z_rad": 0.0,
            "dln_w_common": 0.0,
            "input_status": "CONDITIONAL_ZERO_THEOREM_UNSIGNED",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3996_1_alpha_proxy_no_source_tail",
            "route": "Ward_gauge_alpha_proxy",
            "b_alpha": a,
            "dln_c_pre": 0.0,
            "dln_w_relative": 0.0,
            "dln_kappa_A": 0.0,
            "dln_readout_R": 0.0,
            "z_rad": 0.0,
            "dln_w_common": 0.0,
            "input_status": "DD_ALPHA_PROXY_NONCLAIM",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3996_2_small_finite_source_tail",
            "route": "finite_product_smoke",
            "b_alpha": 0.25 * a,
            "dln_c_pre": 0.10 * a,
            "dln_w_relative": 0.10 * a,
            "dln_kappa_A": 0.10 * a,
            "dln_readout_R": 0.05 * a,
            "z_rad": 0.05 * a,
            "dln_w_common": 0.0,
            "input_status": "NUMERIC_SMOKE_ONLY_NOT_EVIDENCE",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3996_3_common_scalar_only",
            "route": "common_G_calibration",
            "b_alpha": 0.0,
            "dln_c_pre": 0.0,
            "dln_w_relative": 0.0,
            "dln_kappa_A": 0.0,
            "dln_readout_R": 0.0,
            "z_rad": 0.0,
            "dln_w_common": 1.0e-8,
            "input_status": "COMMON_SCALAR_NOT_COMPOSITION_SOURCE_BUT_G_GATE_OPEN",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3996_4_missing_source_slot_inputs",
            "route": "missing_finite_vector",
            "b_alpha": a,
            "dln_c_pre": "",
            "dln_w_relative": "",
            "dln_kappa_A": "",
            "dln_readout_R": "",
            "z_rad": "",
            "dln_w_common": "",
            "input_status": "MISSING_SOURCE_SLOT_VECTOR",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3996_5_large_tail_fails_proxy",
            "route": "finite_product_bound_guard",
            "b_alpha": a,
            "dln_c_pre": a,
            "dln_w_relative": a,
            "dln_kappa_A": 0.5 * a,
            "dln_readout_R": 0.25 * a,
            "z_rad": 0.25 * a,
            "dln_w_common": 0.0,
            "input_status": "OVERSIZED_TAIL_SMOKE_BLOCKS",
            "timestamp_utc": timestamp,
        },
    ]


def optional_float(value: Any) -> float | None:
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING"):
        return None
    return float(text)


RELATIVE_FIELDS = ["b_alpha", "dln_c_pre", "dln_w_relative", "dln_kappa_A", "dln_readout_R", "z_rad"]


def evaluate_case(row: dict[str, Any]) -> dict[str, Any]:
    alpha = alpha_inputs()
    parsed = {field: optional_float(row.get(field)) for field in RELATIVE_FIELDS}
    w_common = optional_float(row.get("dln_w_common"))
    result: dict[str, Any] = {
        "case_id": row["case_id"],
        "route": row["route"],
        "input_status": row["input_status"],
        "eta_bound_abs": alpha["eta_bound"],
        "readout_floor": f"{alpha['readout_floor']:.12e}",
        "DD_weight_abs": f"{alpha['dd_weight_abs']:.12e}",
        "B_EM_source_abs": "MISSING",
        "B_source_tail_relative_abs": "MISSING",
        "B_common_calibration_abs": "MISSING",
        "eta_EM_source_proxy_abs": "MISSING",
        "composition_silent": False,
        "common_G_gate_open": False,
        "passes_DD_source_proxy": False,
        "score_ready": False,
        "claim_allowed": False,
        "valid_for_claim": False,
    }
    if any(value is None for value in parsed.values()) or w_common is None:
        return result
    b_alpha = abs(parsed["b_alpha"] or 0.0)
    tail = sum(abs(parsed[field] or 0.0) for field in RELATIVE_FIELDS if field != "b_alpha")
    total = b_alpha + tail
    eta_proxy = alpha["readout_floor"] * alpha["dd_weight_abs"] * total
    result.update(
        {
            "B_EM_source_abs": f"{total:.12e}",
            "B_source_tail_relative_abs": f"{tail:.12e}",
            "B_common_calibration_abs": f"{abs(w_common):.12e}",
            "eta_EM_source_proxy_abs": f"{eta_proxy:.12e}",
            "composition_silent": tail == 0.0 and b_alpha == 0.0,
            "common_G_gate_open": abs(w_common) > 0.0,
            "passes_DD_source_proxy": eta_proxy <= alpha["eta_bound"] * (1.0 + 1.0e-12),
            "score_ready": False,
        }
    )
    return result


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows = [evaluate_case(row) for row in cases]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3996_0",
            "finding": "prevariation relative EM/source slots are the real physical tail after current-gauge cleanup",
            "evidence": "typed parent grammar/no-Hom theorem kills inert relative source slots, while the finite product vector catches real fields/readout/radiative tails",
            "limitation": "the parent grammar is not yet signed strongly enough for a local-GR source claim",
            "next_action": "attack the common G/source calibration owner or bound universal drift/PPN source calibration",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3996_1",
            "finding": "common scalar is not embarrassing; it is the GR-style Newton/G calibration gate",
            "evidence": "w_common multiplies all Hilbert sources equally and drops out of relative WEP/source composition tests",
            "limitation": "common drift/range dependence still affects Newtonian mechanics, clocks, and PPN unless parent-owned or bounded",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM3996_0_source_slot_zero",
            "claim": "relative prevariation EM/source slots are zero in current MTS",
            "allowed": False,
            "reason": "zero theorem is exact but parent grammar/no-Hom/action-density signatures are not signed together",
            "required_exit": "parent primitive constructor list plus no-Hom source-prefactor certificate",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3996_1_local_GR_source",
            "claim": "local GR source coupling passes",
            "allowed": False,
            "reason": "common G/source calibration, non-Hilbert bypass, readout/radiative tails, and PPN rest remain",
            "required_exit": "3997 common-G calibration plus existing PPN/nonHilbert gates",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3996_2_numeric_bound",
            "claim": "finite b_alpha/source-tail vector is a sourced MTS prediction",
            "allowed": False,
            "reason": "numeric rows are smoke/proxy comparators unless parent coefficients are sourced",
            "required_exit": "numeric parent coefficient vector with source paths and same-domain projections",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3996_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive parent-owned common G/source calibration or build Gdot/PPN/Newton bound rows for the universal scalar branch",
            "success_condition": "common source scalar is either parent-fixed/calibrated without drift or bounded in Newton/PPN/Gdot arenas without being confused with WEP composition",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PREVARIATION_RELATIVE_SOURCE_SLOT_ZERO_THEOREM_PLUS_PRODUCT_VECTOR",
            "headline": "relative source-slot poison is narrowed to a typed no-Hom parent grammar; common scalar is reclassified as the Newton/G calibration gate",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    alpha = alpha_inputs()
    found = sum(bool(row["needle_found"]) for row in sources)
    lines = [
        "# 3996 - Prevariation EM Source-Slot Exclusion Or b_alpha Source Product Bound",
        "",
        f"Timestamp: `{timestamp}`",
        "",
        "## Result",
        "",
        "The source-slot problem is now split cleanly.",
        "",
        "Relative prevariation slots like `w_A^rel`, `c_A_pre`, `kappa_A`, and hidden/material source markers are ill-typed if the parent matter action has one typed density line, variation-before-readout, source-label forgetting, and no Hom into an active-source-prefactor object.",
        "",
        "That is not a public local-GR claim yet, because the parent grammar is not fully signed. But it is a real narrowing: if the theorem closes, these terms vanish by syntax, not by tuning.",
        "",
        "## Common Scalar",
        "",
        "A common multiplier `w_*` is different. It scales all Hilbert sources together:",
        "",
        "`T_source = w_* T_total`.",
        "",
        "That is not WEP/composition poison by itself. It is the GR-like common `G_ref` or source-calibration gate. This matters because GR also uses Newton's constant as a calibrated coupling; the danger is drift/range/source-domain dependence, not the mere existence of one common coupling.",
        "",
        "## Finite Product Vector",
        "",
        "The retained finite branch is",
        "",
        "`B_EM_source = |b_alpha|+|Dln c_pre|+|Dln w_rel|+|Dln kappa_A|+|Dln R_A|+|z_rad|`",
        "",
        "with proxy projection",
        "",
        "`eta_EM_source <= readout_floor |Qe_Earth DeltaQe| B_EM_source`.",
        "",
        f"For the current EM/DD proxy, `readout_floor={alpha['readout_floor']:.12e}`, `|Qe_Earth DeltaQe|={alpha['dd_weight_abs']:.12e}`, and `eta_bound={alpha['eta_bound']:.12e}`.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: status `{row['input_status']}`, B `{row['B_EM_source_abs']}`, eta `{row['eta_EM_source_proxy_abs']}`, pass={row['passes_DD_source_proxy']}, commonG={row['common_G_gate_open']}"
        )
    lines.extend(
        [
            "",
            "## Current Closure Gate",
            "",
            "3996 removes a major ambiguity: the next target is no longer the whole messy source-slot cloud. The next target is the universal common scalar: either derive the parent owner of `G_ref`/common source calibration, or bound its drift/range effect using Newton/PPN/Gdot-style rows.",
            "",
            "## Source Count",
            "",
            f"- source needles found: `{found}/{len(sources)}`",
            "",
            "## Next Target",
            "",
            f"- `{NEXT_DOC}`",
            f"- `{NEXT_SCRIPT}`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def append_spine(timestamp: str) -> None:
    marker = "## 3996 - Prevariation Source Slot Gate"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: relative prevariation source slots are ill-typed under the typed parent matter grammar/no-Hom/action-density theorem; if signed, `Dln c_A_pre`, `Dln w_A^rel`, `Dln kappa_A`, and hidden marker source terms vanish.
- Finite branch: `B_EM_source = |b_alpha|+|Dln c_pre|+|Dln w_rel|+|Dln kappa_A|+|Dln R_A|+|z_rad|`.
- Important split: a common scalar `w_*` is not WEP/composition poison; it becomes the Newton/`G_ref` source-calibration gate.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    types: list[dict[str, Any]],
    products: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    source_paths = [Path(row["path"]) for row in sources]
    add("VAL3996_00_sources_exist", all(path.exists() for path in source_paths), "every cited source path exists")
    add("VAL3996_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL3996_02_theorem_target", any(row["theorem_id"] == "PSS3996_0_target" for row in theorem), "source-slot exclusion theorem row present")
    add("VAL3996_03_common_scalar", any(row["theorem_id"] == "PSS3996_1_common_scalar_reclassification" for row in theorem), "common scalar row present")
    add("VAL3996_04_real_field_exception", any(row["theorem_id"] == "PSS3996_2_real_field_exception" for row in theorem), "real field exception retained")
    add("VAL3996_05_type_rows", len(types) >= 6 and any(row["type_id"] == "TYPE3996_3_kappa_A" for row in types), "source-slot type rows present")
    add("VAL3996_06_product_vector", any(row["product_id"] == "BSP3996_0_invariant_source_product" for row in products), "product vector row present")
    add("VAL3996_07_proxy_projection", any(row["product_id"] == "BSP3996_1_DD_proxy_projection" for row in products), "DD proxy projector row present")
    add("VAL3996_08_common_G_next", any(row["product_id"] == "BSP3996_3_common_scalar_branch" for row in products), "common G branch row present")
    zero = next(row for row in results if row["case_id"] == "CASE3996_0_source_slot_theorem_zero")
    alpha_case = next(row for row in results if row["case_id"] == "CASE3996_1_alpha_proxy_no_source_tail")
    small = next(row for row in results if row["case_id"] == "CASE3996_2_small_finite_source_tail")
    common = next(row for row in results if row["case_id"] == "CASE3996_3_common_scalar_only")
    missing = next(row for row in results if row["case_id"] == "CASE3996_4_missing_source_slot_inputs")
    large = next(row for row in results if row["case_id"] == "CASE3996_5_large_tail_fails_proxy")
    add("VAL3996_09_zero_case", float(zero["B_EM_source_abs"]) == 0.0 and str(zero["passes_DD_source_proxy"]).lower() == "true", "zero case evaluates cleanly")
    add("VAL3996_10_alpha_case", str(alpha_case["passes_DD_source_proxy"]).lower() == "true" and str(alpha_case["valid_for_claim"]).lower() == "false", "alpha proxy case passes nonclaim")
    add("VAL3996_11_small_tail_case", str(small["passes_DD_source_proxy"]).lower() == "true" and str(small["valid_for_claim"]).lower() == "false", "small source-tail smoke passes nonclaim")
    add("VAL3996_12_common_scalar_case", str(common["composition_silent"]).lower() == "true" and str(common["common_G_gate_open"]).lower() == "true", "common scalar separated from composition source")
    add("VAL3996_13_missing_blocks", missing["B_EM_source_abs"] == "MISSING" and str(missing["passes_DD_source_proxy"]).lower() == "false", "missing source-vector branch blocks")
    add("VAL3996_14_large_tail_fails", str(large["passes_DD_source_proxy"]).lower() == "false", "large finite tail fails proxy guard")
    add("VAL3996_15_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL3996_16_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL3996_17_doc_exists", DOC_PATH.exists() and "Common Scalar" in read_text(DOC_PATH), "document written")
    add("VAL3996_18_spine_updated", SPINE_PATH.exists() and "## 3996 - Prevariation Source Slot Gate" in read_text(SPINE_PATH), "spine updated")
    add("VAL3996_19_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL3996_20_compile", compile_ok, "script compiles")
    add("VAL3996_21_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL3996_22_status_exists", OUTPUTS["status"].exists(), "status file exists")
    add("VAL3996_23_results_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for row in results), "all evaluator results remain nonclaim")
    add("VAL3996_24_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL3996_25_G_guard_doc", DOC_PATH.exists() and "Newton's constant" in read_text(DOC_PATH), "Newton/G calibration guard recorded")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    types = type_rows(timestamp)
    products = product_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["types"], types)
    write_csv(OUTPUTS["products"], products)
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

    validation = build_validation_rows(timestamp, sources, theorem, types, products, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"3996 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
