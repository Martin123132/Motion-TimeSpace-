from __future__ import annotations

import csv
import math
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3995"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3995-Y5-R2FR-current-normalization-zg-zero-or-joint-alpha-F2-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3995_SOURCE_REGISTER.csv",
    "trichotomy": SRC / "P8_Y5_R2FR_3995_CURRENT_NORMALIZATION_GAUGE_TRICHOTOMY.csv",
    "decomposition": SRC / "P8_Y5_R2FR_3995_ZG_ZERO_THEOREM_OR_RESIDUAL_DECOMP.csv",
    "bounds": SRC / "P8_Y5_R2FR_3995_JOINT_ALPHA_F2_CURRENT_BOUND_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_3995_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_3995_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_3995_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3995_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3995_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3995_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3995_VALIDATION.csv",
}

NEXT_DOC = "3996-Y5-R2FR-prevariation-EM-source-slot-exclusion-or-balpha-source-product-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3996_prevariation_EM_source_slot_exclusion_or_balpha_source_product_bound.py"


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
        ("SRC3995_00_3994_next", SRC / "P8_Y5_R2FR_3994_NEXT_TARGET.csv", "NEXT3994_0", "3994 handoff"),
        ("SRC3995_01_3994_bounds", SRC / "P8_Y5_R2FR_3994_FINITE_EM_DD_COEFFICIENT_BOUNDS.csv", "FEB3994_2_sXF2_joint", "joint alpha/F2/current bound"),
        ("SRC3995_02_3994_calpha", SRC / "P8_Y5_R2FR_3994_FINITE_EM_DD_COEFFICIENT_BOUNDS.csv", "FEB3994_1_eta_at_C_alpha_bound", "EM DD alpha comparator"),
        ("SRC3995_03_3994_gate", SRC / "P8_Y5_R2FR_3994_OPERATOR_DOMAIN_GATE.csv", "ODG3994_2_current_owner", "same-current gate"),
        ("SRC3995_04_3865_joint", SRC / "P8_Y5_R2FR_3865_SXF2_ZG_BALPHA_JOINT_BOUND.csv", "JHB3865_0_linear_constraint", "b_alpha z_g sXF2 identity"),
        ("SRC3995_05_3865_zg_zero", SRC / "P8_Y5_R2FR_3865_SXF2_ZG_BALPHA_JOINT_BOUND.csv", "JHB3865_3_zg_zero_branch", "z_g zero branch"),
        ("SRC3995_06_3863_rescale", SRC / "P8_Y5_R2FR_3863_MAXWELL_NORMALIZATION_OWNER_THEOREM.csv", "MNO3863_0_rescaling_normal_form", "Maxwell rescaling normal form"),
        ("SRC3995_07_3863_owner", SRC / "P8_Y5_R2FR_3863_MAXWELL_NORMALIZATION_OWNER_THEOREM.csv", "MNO3863_2_normalization_owner_theorem", "source-scale zero theorem"),
        ("SRC3995_08_3809_counter", SRC / "P8_Y5_R2FR_3809_MAXWELL_NORMALIZATION_THEOREM.csv", "MNT3809_2_rescaling_countermodel", "normalization countermodel"),
        ("SRC3995_09_3507_zg", SRC / "P8_Y5_R2FR_3507_ALPHA_RESIDUAL_VECTOR.csv", "ARE3507_2_z_g", "z_g residual definition"),
        ("SRC3995_10_3507_balpha", SRC / "P8_Y5_R2FR_3507_ALPHA_RESIDUAL_VECTOR.csv", "ARE3507_0_b_alpha_X", "b_alpha residual definition"),
        ("SRC3995_11_3868_law", SRC / "P8_Y5_R2FR_3868_ZG_COMPONENT_LAW.csv", "ZC3868_0_product_decomposition", "z_g component law"),
        ("SRC3995_12_3868_audit", SRC / "P8_Y5_R2FR_3868_ZG_ZERO_PROOF_AUDIT.csv", "ZP3868_5_verdict", "z_g zero proof verdict"),
        ("SRC3995_13_3875_theorem", SRC / "P8_Y5_R2FR_3875_CJQ_CURRENT_OWNER_ZERO_THEOREM.csv", "CJT3875_0_target", "current-owner zero theorem"),
        ("SRC3995_14_3875_reduction", SRC / "P8_Y5_R2FR_3875_ZG_ACTIVE_REDUCTION_ROWS.csv", "ZGR3875_0_reduced_law", "active z_g reduction"),
        ("SRC3995_15_3508_ward", SRC / "P8_Y5_R2FR_3508_CURRENT_SOURCE_WARD_IDENTITY.csv", "WARD3508_2_vertical_current_normalization", "Ward current normalization"),
        ("SRC3995_16_3143_same_current", SRC / "P8_Y5_R2FR_3143_SAME_CURRENT_OWNER_THEOREM.csv", "SCOT3143_3_same_current_owner", "same current owner"),
        ("SRC3995_17_3792_same_source", SRC / "P8_Y5_R2FR_3792_SAME_CURRENT_WARD_HILBERT_THEOREM.csv", "SCW3792_1_same_current_definition", "same source current definition"),
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


def alpha_channel_inputs() -> dict[str, float]:
    bounds = read_csv(SRC / "P8_Y5_R2FR_3994_FINITE_EM_DD_COEFFICIENT_BOUNDS.csv")
    results = read_csv(SRC / "P8_Y5_R2FR_3994_EM_DD_EVALUATOR_RESULTS.csv")
    c_alpha = None
    eta = None
    readout = None
    weight = None
    for row in bounds:
        if row.get("bound_id") == "FEB3994_0_C_alpha_EM_DD":
            c_alpha = float(row["numeric_value"])
    for row in results:
        if row.get("case_id") == "CASE3994_1_C_alpha_at_DD_proxy_bound":
            eta = float(row["eta_bound_abs"])
            readout = float(row["readout_floor"])
            weight = float(row["DD_weight_abs"])
    if c_alpha is None or eta is None or readout is None or weight is None:
        raise RuntimeError("3994 alpha channel inputs missing")
    return {
        "c_alpha_bound": c_alpha,
        "eta_bound": eta,
        "readout_floor": readout,
        "dd_weight_abs": weight,
    }


def trichotomy_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "TRI3995_0_rescaling_covariance",
            "branch": "normalization_gauge",
            "statement": "Under A_Q -> exp(sigma) A_Q, lambda_A -> exp(-2 sigma) lambda_A and g_J -> exp(-sigma) g_J, so z_g -> z_g-Dsigma and s_XF2 -> s_XF2-2Dsigma while b_alpha=2z_g-s_XF2 is invariant.",
            "derived_result": "z_g alone is not an observable before the EM/current normalization gauge is fixed",
            "status": "EXACT_FIELD_REDEFINITION_IDENTITY",
            "source_path": str(SRC / "P8_Y5_R2FR_3863_MAXWELL_NORMALIZATION_OWNER_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "TRI3995_1_Ward_current_gauge",
            "branch": "same_current_owner",
            "statement": "If J_Q is the Noether current varied before readout from the same q-basic matter action with fixed charge labels, choose the Ward-current gauge Dsigma=z_g; then z_g'=0 and s_XF2'=-b_alpha.",
            "derived_result": "the same-current route does not need a separate physical z_g proof; it needs source-slot exclusion plus the invariant b_alpha/F2 branch",
            "status": "EXACT_CONDITIONAL_GAUGE_FIX",
            "source_path": str(SRC / "P8_Y5_R2FR_3508_CURRENT_SOURCE_WARD_IDENTITY.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "TRI3995_2_physical_source_slot",
            "branch": "prevariation_source_slot",
            "statement": "If kappa_A(X), w_A(X), q_A(X), readout R_A(X), or radiative current regeneration enters before variation or before arena projection, it is not a pure z_g gauge artifact and must remain as a finite source residual.",
            "derived_result": "Ward conservation cannot remove source prefactors already inserted into the action",
            "status": "COUNTERMODEL_BRANCH_RETAINED",
            "source_path": str(SRC / "P8_Y5_R2FR_3868_ZG_ZERO_PROOF_AUDIT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "TRI3995_3_absolute_constant_guard",
            "branch": "constant_value_vs_local_drift",
            "statement": "This branch can silence local vertical drift without deriving the absolute value of alpha_EM, just as GR uses Newton's constant as an empirical coupling while still deriving the Newtonian limit.",
            "derived_result": "do not overclaim absolute alpha/G prediction; local tests require drift/source-product closure",
            "status": "OVERCLAIM_GUARD_ACTIVE",
            "source_path": str(SRC / "P8_Y5_R2FR_3809_MAXWELL_NORMALIZATION_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decomposition_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "component_id": "ZGD3995_0_reduced_law",
            "quantity": "z_g_active",
            "formula": "z_g_active = z_Qstar + z_Noether + z_readout + z_measure/source_slot + z_rad",
            "result": "active current-normalization residue after fixed-lattice and post-variation reductions",
            "zero_status": "REDUCED_NOT_GLOBALLY_ZERO",
            "next_action": "fix Ward-current gauge for convention leg; bound or exclude source-slot terms",
            "source_path": str(SRC / "P8_Y5_R2FR_3875_ZG_ACTIVE_REDUCTION_ROWS.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "ZGD3995_1_fixed_lattice",
            "quantity": "z_lattice",
            "formula": "D_X ln n_A = 0 on a connected fixed representation sector",
            "result": "derived subzero",
            "zero_status": "ZERO_IF_FIXED_SECTOR",
            "next_action": "keep as signed sublemma, not as full z_g proof",
            "source_path": str(SRC / "P8_Y5_R2FR_3868_ZG_ZERO_PROOF_AUDIT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "ZGD3995_2_noether_current",
            "quantity": "z_Noether",
            "formula": "D_v J_Q=0 if J_Q=(1/mu_obs) delta S_matter/delta A_Q and S_matter descends through q",
            "result": "exact conditional Ward/chain-rule subzero",
            "zero_status": "ZERO_IF_SAME_CURRENT_OWNER_SIGNED",
            "next_action": "need parent current certificate or keep finite residual",
            "source_path": str(SRC / "P8_Y5_R2FR_3143_SAME_CURRENT_OWNER_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "ZGD3995_3_base_unit",
            "quantity": "z_Qstar",
            "formula": "D_X ln Qstar",
            "result": "constant charge unit/generator norm is gauge-fixable locally but not an absolute alpha prediction",
            "zero_status": "GAUGE_OR_PARENT_NORM_REQUIRED",
            "next_action": "work with invariant b_alpha unless parent norm value is derived",
            "source_path": str(SRC / "P8_Y5_R2FR_3868_ZG_COMPONENT_LAW.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "ZGD3995_4_source_slot_tail",
            "quantity": "z_source_tail",
            "formula": "D_X ln kappa_A + D_X ln w_A + D_X ln R_A + z_rad",
            "result": "physical if inserted before variation or before arena/source projection",
            "zero_status": "LIVE_UNTIL_SOURCE_SLOT_EXCLUSION_OR_BOUND",
            "next_action": "3996 source-slot exclusion or product-bound rows",
            "source_path": str(SRC / "P8_Y5_R2FR_3508_CURRENT_SOURCE_WARD_IDENTITY.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    alpha = alpha_channel_inputs()
    return [
        {
            "bound_id": "JAB3995_0_invariant_identity",
            "target": "b_alpha,z_g,s_XF2",
            "formula": "b_alpha = 2 z_g - s_XF2",
            "numeric_value": "identity",
            "derived_result": "b_alpha is invariant under EM current/field rescaling while z_g and s_XF2 separately move",
            "status": "EXACT_INVARIANT_IDENTITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "JAB3995_1_Ward_current_gauge",
            "target": "z_g,s_XF2",
            "formula": "choose Dsigma=z_g => z_g'=0, s_XF2'=-b_alpha",
            "numeric_value": "gauge_fixed_identity",
            "derived_result": "same-current branch can score the invariant b_alpha/F2 channel without treating z_g as independent evidence",
            "status": "EXACT_CONDITIONAL_GAUGE_REDUCTION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "JAB3995_2_arbitrary_gauge_bound",
            "target": "s_XF2",
            "formula": "|s_XF2| <= |b_alpha| + 2|z_g|",
            "numeric_value": "symbolic_until_zg_bound",
            "derived_result": "fallback if the current normalization gauge cannot be fixed or source slots are physical",
            "status": "SYMBOLIC_NONCLAIM_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "JAB3995_3_alpha_channel_proxy",
            "target": "b_alpha_or_C_alpha_EM",
            "formula": "|b_alpha_channel| <= eta_bound/(readout_floor*|Qe_Earth DeltaQe|)",
            "numeric_value": f"{alpha['c_alpha_bound']:.12e}",
            "derived_result": "imports 3994 single-channel EM/DD proxy comparator, not a parent MTS coefficient claim",
            "status": "NUMERIC_PROXY_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "JAB3995_4_source_slot_envelope",
            "target": "B_zg_source_tail",
            "formula": "B_zg_source_tail <= |D ln kappa_A|+|D ln w_A|+|D ln R_A|+|z_rad|",
            "numeric_value": "MISSING_SOURCE_SLOT_ROWS",
            "derived_result": "source-slot tail is the real physical obstruction after current-gauge reduction",
            "status": "NEXT_BOUND_VECTOR_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    alpha = alpha_channel_inputs()
    c_alpha = alpha["c_alpha_bound"]
    return [
        {
            "case_id": "CASE3995_0_Ward_current_gauge_zero",
            "route": "same_current_gauge_zero",
            "b_alpha": 0.0,
            "z_g": 0.0,
            "s_XF2": 0.0,
            "source_tail": 0.0,
            "input_status": "CONDITIONAL_ZERO_GAUGE_NOT_PARENT_CLAIM",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3995_1_pure_rescaling_countermodel",
            "route": "normalization_gauge_artifact",
            "b_alpha": 0.0,
            "z_g": 1.0e-8,
            "s_XF2": 2.0e-8,
            "source_tail": 0.0,
            "input_status": "PURE_ZG_NOT_OBSERVABLE_IF_BALPHA_ZERO",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3995_2_alpha_bound_current_gauge",
            "route": "Ward_current_gauge_alpha_proxy",
            "b_alpha": c_alpha,
            "z_g": 0.0,
            "s_XF2": -c_alpha,
            "source_tail": 0.0,
            "input_status": "DD_ALPHA_PROXY_NONCLAIM",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3995_3_live_zg_source_tail",
            "route": "finite_source_tail",
            "b_alpha": c_alpha,
            "z_g": "",
            "s_XF2": "",
            "source_tail": "MISSING_kappa_w_R_zrad",
            "input_status": "MISSING_SOURCE_SLOT_BOUND",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3995_4_readout_radiative_reentry",
            "route": "readout_radiative_tail",
            "b_alpha": "",
            "z_g": "",
            "s_XF2": "",
            "source_tail": "MISSING_READOUT_RADIOUT_KERNEL",
            "input_status": "MISSING_READOUT_RADIOUT_CLOSURE",
            "timestamp_utc": timestamp,
        },
    ]


def optional_float(value: Any) -> float | None:
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING"):
        return None
    return float(text)


def evaluate_case(row: dict[str, Any]) -> dict[str, Any]:
    alpha = alpha_channel_inputs()
    b_alpha = optional_float(row.get("b_alpha"))
    z_g = optional_float(row.get("z_g"))
    sxf2 = optional_float(row.get("s_XF2"))
    source_tail = optional_float(row.get("source_tail"))
    result: dict[str, Any] = {
        "case_id": row["case_id"],
        "route": row["route"],
        "input_status": row["input_status"],
        "eta_bound_abs": alpha["eta_bound"],
        "readout_floor": f"{alpha['readout_floor']:.12e}",
        "DD_weight_abs": f"{alpha['dd_weight_abs']:.12e}",
        "b_alpha": "MISSING",
        "z_g": "MISSING",
        "s_XF2": "MISSING",
        "identity_residual_abs": "MISSING",
        "eta_alpha_proxy_abs": "MISSING",
        "B_source_tail_abs": "MISSING",
        "passes_identity": False,
        "passes_alpha_proxy": False,
        "score_ready": False,
        "claim_allowed": False,
        "valid_for_claim": False,
    }
    if b_alpha is None or z_g is None or sxf2 is None or source_tail is None:
        return result
    identity = abs(b_alpha - (2.0 * z_g - sxf2))
    eta_proxy = alpha["readout_floor"] * alpha["dd_weight_abs"] * abs(b_alpha)
    source_tail_abs = abs(source_tail)
    result.update(
        {
            "b_alpha": f"{b_alpha:.12e}",
            "z_g": f"{z_g:.12e}",
            "s_XF2": f"{sxf2:.12e}",
            "identity_residual_abs": f"{identity:.12e}",
            "eta_alpha_proxy_abs": f"{eta_proxy:.12e}",
            "B_source_tail_abs": f"{source_tail_abs:.12e}",
            "passes_identity": identity <= 1.0e-20,
            "passes_alpha_proxy": eta_proxy <= alpha["eta_bound"] * (1.0 + 1.0e-12),
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
            "decision_id": "DEC3995_0",
            "finding": "z_g is not a standalone physical obstruction before EM/current normalization is fixed",
            "evidence": "field rescaling moves z_g and s_XF2 while preserving b_alpha=2z_g-s_XF2",
            "limitation": "pre-variation source slots, readout, and radiative current re-entry are physical if present",
            "next_action": "attack source-slot exclusion or build source-backed b_alpha/source-tail product rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3995_1",
            "finding": "current-gauge route is less scrutiny-prone than a naked z_g=0 claim",
            "evidence": "same-current Ward gauge gives z_g'=0 and s_XF2'=-b_alpha without asserting an absolute alpha value",
            "limitation": "does not prove local GR; it only removes one coordinate artifact from the EM coupling branch",
            "next_action": "3996 prevariation EM source-slot exclusion or finite product vector",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM3995_0_local_GR_EM",
            "claim": "local GR/EM source branch passes",
            "allowed": False,
            "reason": "source-slot/readout/radiative tails not parent-signed or source-bounded",
            "required_exit": "source-tail zero theorem or numeric source-backed product rows",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3995_1_zg_zero",
            "claim": "physical z_g=0 is proven",
            "allowed": False,
            "reason": "3995 proves gauge reduction and conditional same-current zero, not absolute physical z_g zero",
            "required_exit": "parent current certificate plus source-slot exclusion",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3995_2_alpha_bound",
            "claim": "MTS alpha coefficient is bounded/predicted",
            "allowed": False,
            "reason": "numeric alpha row is comparator/proxy only; parent coefficient remains unsourced",
            "required_exit": "parent-owned b_alpha or source product map",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3995_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "exclude prevariation EM/source slots from the parent grammar or build a finite b_alpha/source-tail product vector",
            "success_condition": "either source_tail=0 by object-language theorem, or b_alpha/source/readout/radiative products are numeric, sourced, same-domain, and nonclaim-evaluated",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "ZG_COORDINATE_SPLIT_DERIVED_SOURCE_SLOT_REMAINS_PHYSICAL",
            "headline": "z_g by itself is a normalization-gauge coordinate; b_alpha is the invariant coupling, while prevariation source slots/readout/radiative tails remain the real local-EM obstruction",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(bool(row["needle_found"]) for row in sources)
    alpha = alpha_channel_inputs()
    lines = [
        "# 3995 - Current Normalization z_g Zero Or Joint Alpha/F2 Bound",
        "",
        f"Timestamp: `{timestamp}`",
        "",
        "## Result",
        "",
        "`z_g` is now split into a normalization-gauge leg and a physical source-slot leg.",
        "",
        "The invariant coupling is not naked `z_g`; it is",
        "",
        "`b_alpha = 2 z_g - s_XF2`.",
        "",
        "Under `A_Q -> exp(sigma) A_Q`, `z_g -> z_g-Dsigma` and `s_XF2 -> s_XF2-2Dsigma`, so `b_alpha` is unchanged. That means a pure `z_g` drift can be bookkeeping, not physics.",
        "",
        "## Ward-Current Gauge",
        "",
        "If the visible charge current is varied before readout from the same q-basic matter action, choose `Dsigma=z_g`. Then `z_g'=0` and `s_XF2'=-b_alpha`.",
        "",
        "This is better than claiming a mystical standalone `z_g=0`: it says the same-current branch should score the invariant alpha/F2 coupling, while source-slot/readout/radiative tails remain explicit residuals.",
        "",
        "## Finite Bound",
        "",
        f"The 3994 EM/DD proxy gives `|b_alpha_channel| <= {alpha['c_alpha_bound']:.12e}` in the single `Q_e` route, with readout floor `{alpha['readout_floor']:.12e}` and DD weight `{alpha['dd_weight_abs']:.12e}`.",
        "",
        "In arbitrary normalization gauge we still keep",
        "",
        "`|s_XF2| <= |b_alpha| + 2|z_g|`.",
        "",
        "In Ward-current gauge this tightens to",
        "",
        "`|s_XF2'| = |b_alpha|`.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: status `{row['input_status']}`, identity `{row['identity_residual_abs']}`, eta `{row['eta_alpha_proxy_abs']}`, claim={row['claim_allowed']}"
        )
    lines.extend(
        [
            "",
            "## Current Closure Gate",
            "",
            "This moves the problem forward: the next hard thing is not a vague `z_g` hunt. It is the explicit physical tail",
            "",
            "`B_zg_source_tail <= |D ln kappa_A|+|D ln w_A|+|D ln R_A|+|z_rad|`.",
            "",
            "Those terms are real only if they enter before variation/readout projection. If the parent grammar excludes them, the EM source branch gets much cleaner. If not, they become numeric product rows.",
            "",
            "## Guard",
            "",
            "This does not derive the absolute value of `alpha_EM`, just as local GR recovery does not require deriving the numerical value of Newton's constant. The live target is local drift/source-product silence or bounded residuals.",
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
    marker = "## 3995 - Current Normalization Gauge Split"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: `z_g` alone is not an invariant obstruction; under EM field/current normalization rescaling, `z_g` and `s_XF2` move but `b_alpha=2z_g-s_XF2` is invariant.
- Derived branch: in Ward-current gauge, same-current owner gives `z_g'=0` and `s_XF2'=-b_alpha`; this avoids a naked physical `z_g=0` overclaim.
- Remaining blocker: prevariation EM/source slots, readout transfer, and radiative current regeneration are still physical unless excluded or bounded.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    trichotomy: list[dict[str, Any]],
    decomp: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    source_paths = [Path(row["path"]) for row in sources]
    add("VAL3995_00_sources_exist", all(path.exists() for path in source_paths), "every cited source path exists")
    add("VAL3995_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL3995_02_rescaling_row", any(row["row_id"] == "TRI3995_0_rescaling_covariance" for row in trichotomy), "rescaling covariance row present")
    add("VAL3995_03_current_gauge_row", any(row["row_id"] == "TRI3995_1_Ward_current_gauge" for row in trichotomy), "Ward-current gauge row present")
    add("VAL3995_04_source_slot_row", any(row["row_id"] == "TRI3995_2_physical_source_slot" for row in trichotomy), "source-slot countermodel row present")
    add("VAL3995_05_decomposition_rows", len(decomp) >= 5 and any(row["component_id"] == "ZGD3995_4_source_slot_tail" for row in decomp), "z_g decomposition rows present")
    add("VAL3995_06_bound_identity", any(row["bound_id"] == "JAB3995_0_invariant_identity" for row in bounds), "invariant identity bound row present")
    add("VAL3995_07_bound_current_gauge", any(row["bound_id"] == "JAB3995_1_Ward_current_gauge" for row in bounds), "current-gauge bound row present")
    alpha_bound = next(row for row in bounds if row["bound_id"] == "JAB3995_3_alpha_channel_proxy")
    add("VAL3995_08_alpha_bound_numeric", float(alpha_bound["numeric_value"]) > 0.0, "alpha proxy bound positive")
    zero = next(row for row in results if row["case_id"] == "CASE3995_0_Ward_current_gauge_zero")
    pure = next(row for row in results if row["case_id"] == "CASE3995_1_pure_rescaling_countermodel")
    alpha_case = next(row for row in results if row["case_id"] == "CASE3995_2_alpha_bound_current_gauge")
    missing = next(row for row in results if row["case_id"] == "CASE3995_3_live_zg_source_tail")
    rad = next(row for row in results if row["case_id"] == "CASE3995_4_readout_radiative_reentry")
    add("VAL3995_09_zero_case", float(zero["eta_alpha_proxy_abs"]) == 0.0 and str(zero["passes_identity"]).lower() == "true", "zero case evaluates cleanly")
    add("VAL3995_10_pure_rescaling_case", float(pure["eta_alpha_proxy_abs"]) == 0.0 and str(pure["passes_identity"]).lower() == "true", "pure z_g rescaling has zero invariant alpha signal")
    add("VAL3995_11_alpha_case", str(alpha_case["passes_alpha_proxy"]).lower() == "true" and str(alpha_case["valid_for_claim"]).lower() == "false", "alpha proxy case passes nonclaim")
    add("VAL3995_12_missing_source_blocks", missing["eta_alpha_proxy_abs"] == "MISSING" and str(missing["passes_alpha_proxy"]).lower() == "false", "missing source-slot branch blocks")
    add("VAL3995_13_radout_blocks", rad["eta_alpha_proxy_abs"] == "MISSING" and str(rad["passes_alpha_proxy"]).lower() == "false", "missing readout/radiative branch blocks")
    add("VAL3995_14_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL3995_15_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL3995_16_doc_exists", DOC_PATH.exists() and "Ward-current gauge" in read_text(DOC_PATH), "document written")
    add("VAL3995_17_spine_updated", SPINE_PATH.exists() and "## 3995 - Current Normalization Gauge Split" in read_text(SPINE_PATH), "spine updated")
    add("VAL3995_18_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL3995_19_compile", compile_ok, "script compiles")
    add("VAL3995_20_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL3995_21_status_exists", OUTPUTS["status"].exists(), "status file exists")
    add("VAL3995_22_results_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for row in results), "all evaluator results remain nonclaim")
    add("VAL3995_23_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL3995_24_guard_mentions_G", DOC_PATH.exists() and "Newton's constant" in read_text(DOC_PATH), "absolute constant guard recorded")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    trichotomy = trichotomy_rows(timestamp)
    decomp = decomposition_rows(timestamp)
    bounds = bound_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["trichotomy"], trichotomy)
    write_csv(OUTPUTS["decomposition"], decomp)
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

    validation = build_validation_rows(timestamp, sources, trichotomy, decomp, bounds, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"3995 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
