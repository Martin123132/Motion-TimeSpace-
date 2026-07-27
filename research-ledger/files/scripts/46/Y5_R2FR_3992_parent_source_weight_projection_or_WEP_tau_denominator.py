from __future__ import annotations

import csv
import math
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3992"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3992-Y5-R2FR-parent-source-weight-projection-or-WEP-tau-denominator.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3992_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3992_WEP_EFFECTIVE_NORMALIZATION_THEOREM.csv",
    "factors": SRC / "P8_Y5_R2FR_3992_TAU_DENOMINATOR_FACTOR_ROWS.csv",
    "material": SRC / "P8_Y5_R2FR_3992_MATERIAL_EARTH_DD_PROXY_DENOMINATOR.csv",
    "cases": SRC / "P8_Y5_R2FR_3992_DENOMINATOR_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_3992_DENOMINATOR_EVALUATOR_RESULTS.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3992_PROJECTION_CLAIM_GATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3992_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3992_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3992_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3992_VALIDATION.csv",
}

NEXT_DOC = "3993-Y5-R2FR-DD-proxy-to-parent-basis-map-or-source-weight-zero.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3993_DD_proxy_to_parent_basis_map_or_source_weight_zero.py"

DD_COMPONENTS = ["Q_hatm_full", "Q_delta_m", "Q_m_e", "Q_e_full"]
EARTH_COMPONENTS = ["Q_hatm_full_Earth", "Q_delta_m_Earth", "Q_m_e_Earth", "Q_e_full_Earth"]


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
        ("SRC3992_00_3991_next", SRC / "P8_Y5_R2FR_3991_NEXT_TARGET.csv", "NEXT3991_0", "3991 handoff"),
        ("SRC3992_01_3991_anchor", SRC / "P8_Y5_R2FR_3991_REAL_SOURCE_WEIGHT_BOUND_ANCHORS.csv", "ANCH3991_0_WEP_MICROSCOPE_product", "real WEP anchor"),
        ("SRC3992_02_3463_tau_derivation", SRC / "P8_Y5_R2FR_3463_WEP_TAU_PROJECTION_DERIVATION.csv", "TAU3463_1_direct_linear_limit", "effective Eotvos normalization"),
        ("SRC3992_03_3366_packet", SRC / "P8_Y5_R2FR_3366_TAU_WEP_EXECUTION_PACKET.csv", "TAU3366_0_executable_formula", "tau WEP execution packet"),
        ("SRC3992_04_3262_factor", SRC / "P8_Y5_R2FR_3262_TAU_WEP_FACTORIZATION.csv", "TAU3262_1_readout_X", "readout factor evidence"),
        ("SRC3992_05_3262_readout_lines", SRC / "P8_Y5_R2FR_3262_MICROSCOPE_READOUT_FACTOR_EVIDENCE.csv", "MRF3262_1_x_readout", "MICROSCOPE readout evidence"),
        ("SRC3992_06_3263_channel", SRC / "P8_Y5_R2FR_3263_MICROSCOPE_EP_CHANNEL_EVIDENCE.csv", "MCH3263_5_eta_identification", "EP channel eta identification"),
        ("SRC3992_07_3260_bound_inputs", SRC / "P8_Y5_R2FR_3260_MICROSCOPE_DD_BOUND_INPUTS.csv", "BIN3260_4_eta_reported_level", "MICROSCOPE DD bound inputs"),
        ("SRC3992_08_3473_material", SRC / "P8_Y5_R2FR_3473_FULL_DD_MATERIAL_ROWS.csv", "MAT3473_MICROSCOPE_TA6V", "MICROSCOPE material DD rows"),
        ("SRC3992_09_3482_earth", SRC / "P8_Y5_R2FR_3482_EARTH_FULL_DD_SOURCE_VECTOR_NONCLAIM.csv", "EARTH3482_0_bulk_full_DD_four_charge", "Earth DD source vector"),
        ("SRC3992_10_3481_normalizer", SRC / "P8_Y5_R2FR_3481_WEP_SHARED_EARTH_NORMALIZER_ROWS_NONCLAIM.csv", "WEN3481_0_MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10", "shared Earth/material normalizer"),
        ("SRC3992_11_3544_source_leg", SRC / "P8_Y5_R2FR_3544_MICROSCOPE_SOURCE_LEG_INTAKE.csv", "SL3544_0_compressed_D_definition", "compressed source-leg intake"),
        ("SRC3992_12_3364_owner", SRC / "P8_Y5_R2FR_3364_WEP_PROJECTION_OWNER_AUDIT.csv", "WEP3364_4_tau_product", "WEP projection owner audit"),
        ("SRC3992_13_1420_checklist", SRC / "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv", "WAC1420_0_source_worldtube_profile", "WEP source acquisition checklist"),
        ("SRC3992_14_3991_results", SRC / "P8_Y5_R2FR_3991_PPN_BETA_SOURCE_EVALUATOR_RESULTS.csv", "CASE3991_1_real_WEP_anchor_projection_blocked", "3991 projection block result"),
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


def eta_bound() -> float:
    rows = read_csv(SRC / "P8_Y5_R2FR_3991_REAL_SOURCE_WEIGHT_BOUND_ANCHORS.csv")
    for row in rows:
        if row.get("anchor_id") == "ANCH3991_0_WEP_MICROSCOPE_product":
            return float(row["real_observable_bound"])
    raise RuntimeError("3991 WEP anchor missing")


def readout_interval() -> tuple[float, float]:
    rows = read_csv(SRC / "P8_Y5_R2FR_3262_TAU_WEP_FACTORIZATION.csv")
    for row in rows:
        if row.get("tau_id") == "TAU3262_1_readout_X":
            text = row["numeric_status"]
            # Stored as "9.800...e-01 <= tau_readout_X <= 1.020...e+00"
            left, _, right = text.partition("<= tau_readout_X <=")
            return float(left.strip()), float(right.strip())
    raise RuntimeError("TAU3262_1_readout_X row missing")


def material_rows() -> dict[str, dict[str, str]]:
    rows = read_csv(SRC / "P8_Y5_R2FR_3473_FULL_DD_MATERIAL_ROWS.csv")
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        if row.get("material_id") in {"PtRh10", "TA6V"} and row.get("arena") == "MICROSCOPE_TIPT_EARTH_FIELD":
            out[row["material_id"]] = row
    if set(out) != {"PtRh10", "TA6V"}:
        raise RuntimeError("MICROSCOPE PtRh10/TA6V material rows missing")
    return out


def earth_row() -> dict[str, str]:
    rows = read_csv(SRC / "P8_Y5_R2FR_3482_EARTH_FULL_DD_SOURCE_VECTOR_NONCLAIM.csv")
    for row in rows:
        if row.get("source_vector_id") == "EARTH3482_0_bulk_full_DD_four_charge":
            return row
    raise RuntimeError("Earth DD source vector row missing")


def dd_proxy() -> dict[str, float]:
    mats = material_rows()
    earth = earth_row()
    deltas: dict[str, float] = {}
    products: dict[str, float] = {}
    dot = 0.0
    for material_key, earth_key in zip(DD_COMPONENTS, EARTH_COMPONENTS):
        delta = float(mats["TA6V"][material_key]) - float(mats["PtRh10"][material_key])
        source = float(earth[earth_key])
        product = delta * source
        deltas[material_key] = delta
        products[material_key] = product
        dot += product
    l1_delta = sum(abs(value) for value in deltas.values())
    l2_delta = math.sqrt(sum(value * value for value in deltas.values()))
    source_l2 = math.sqrt(sum(float(earth[key]) ** 2 for key in EARTH_COMPONENTS))
    readout_low, readout_high = readout_interval()
    abs_dot = abs(dot)
    return {
        "Delta_Q_hatm_full": deltas["Q_hatm_full"],
        "Delta_Q_delta_m": deltas["Q_delta_m"],
        "Delta_Q_m_e": deltas["Q_m_e"],
        "Delta_Q_e_full": deltas["Q_e_full"],
        "Earth_Q_hatm_full": float(earth["Q_hatm_full_Earth"]),
        "Earth_Q_delta_m": float(earth["Q_delta_m_Earth"]),
        "Earth_Q_m_e": float(earth["Q_m_e_Earth"]),
        "Earth_Q_e_full": float(earth["Q_e_full_Earth"]),
        "dot_Earth_DeltaQ_TA6V_minus_PtRh10": dot,
        "abs_dot_Earth_DeltaQ": abs_dot,
        "l1_material_delta": l1_delta,
        "l2_material_delta": l2_delta,
        "l2_earth_source": source_l2,
        "tau_readout_low": readout_low,
        "tau_readout_high": readout_high,
        "abs_tau_proxy_low": readout_low * abs_dot,
        "abs_tau_proxy_high": readout_high * abs_dot,
        "eta_bound_abs": eta_bound(),
        "dd_proxy_coeff_bound_using_tau_low": eta_bound() / (readout_low * abs_dot) if abs_dot > 0 else math.inf,
    }


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "WEN3992_0_exact_eotvos_identity",
            "claim_piece": "Eotvos effective contrast identity",
            "mathematical_form": "If a_A=g_N(1+epsilon_A) and a_B=g_N(1+epsilon_B), then eta_AB=2(epsilon_A-epsilon_B)/(2+epsilon_A+epsilon_B).",
            "derived_result": "the MICROSCOPE bound is directly a bound on the readout-normalized effective differential acceleration contrast",
            "status": "EXACT_EFFECTIVE_NORMALIZATION_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "WEN3992_1_effective_tau",
            "claim_piece": "effective contrast tau",
            "mathematical_form": "Define Delta_w_eff_TiPt := eta_source_component in the MICROSCOPE Eotvos readout convention. Then tau_eff=1 by definition and |Delta_w_eff_TiPt| <= eta_bound_abs.",
            "derived_result": "a real effective-contrast bound is available without setting raw MTS tau_WEP to one",
            "status": "EFFECTIVE_BOUND_READY_RAW_MTS_MAP_OPEN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "WEN3992_2_raw_tau_factorization",
            "claim_piece": "raw MTS tau factorization",
            "mathematical_form": "tau_MTS = tau_readout_X * <S_Earth, K_parent_to_response[DeltaQ_TiPt]> * tau_channel_projection * tau_branch_lock.",
            "derived_result": "the raw parent coefficient denominator is not tau_eff; it requires source/profile/material/parent-basis projection",
            "status": "RAW_TAU_FACTOR_LAW_DERIVED_INPUTS_PARTIAL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "WEN3992_3_no_hom_zero_route",
            "claim_piece": "source-weight zero bypass",
            "mathematical_form": "If the 3990 no-Hom grammar is parent-signed, Delta_w_TiPt=0 and the WEP product vanishes for any finite tau_WEP.",
            "derived_result": "the projection denominator is unnecessary only after the parent source-weight zero theorem is signed",
            "status": "CONDITIONAL_ZERO_ROUTE_PARENT_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def factor_rows(timestamp: str) -> list[dict[str, Any]]:
    proxy = dd_proxy()
    return [
        {
            "factor_id": "TAUF3992_0_effective_readout",
            "factor": "tau_eff",
            "formula": "Delta_w_eff_TiPt := eta_source_component",
            "value_or_interval": "1 by readout-normalized definition",
            "status": "EXACT_EFFECTIVE_NORMALIZATION_NOT_RAW_MTS_TAU",
            "source_path": str(SRC / "P8_Y5_R2FR_3463_WEP_TAU_PROJECTION_DERIVATION.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "factor_id": "TAUF3992_1_readout_X",
            "factor": "tau_readout_X",
            "formula": "tau_readout_X = tilde(a)_c11",
            "value_or_interval": f"{proxy['tau_readout_low']:.12g} <= tau_readout_X <= {proxy['tau_readout_high']:.12g}",
            "status": "PARTIAL_FACTOR_SOURCE_BACKED",
            "source_path": str(SRC / "P8_Y5_R2FR_3262_TAU_WEP_FACTORIZATION.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "factor_id": "TAUF3992_2_DD_proxy_denominator",
            "factor": "tau_DD_proxy",
            "formula": "tau_DD_proxy = tau_readout_X * dot(Q_Earth_DD, DeltaQ_TA6V_minus_PtRh10_DD)",
            "value_or_interval": f"{proxy['abs_tau_proxy_low']:.12e} <= |tau_DD_proxy| <= {proxy['abs_tau_proxy_high']:.12e}",
            "status": "NUMERIC_DD_PROXY_DENOMINATOR_NONCLAIM_PARENT_MAP_MISSING",
            "source_path": str(SRC / "P8_Y5_R2FR_3473_FULL_DD_MATERIAL_ROWS.csv") + ";" + str(SRC / "P8_Y5_R2FR_3482_EARTH_FULL_DD_SOURCE_VECTOR_NONCLAIM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "factor_id": "TAUF3992_3_parent_basis_map",
            "factor": "K_parent_to_DD_or_response",
            "formula": "maps MTS source-weight residual basis into the DD/material/source response basis",
            "value_or_interval": "MISSING_PARENT_BASIS_MAP",
            "status": "BLOCKS_RAW_MTS_COUPLING_BOUND",
            "source_path": str(SRC / "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "factor_id": "TAUF3992_4_official_orbit_profile",
            "factor": "tau_channel_projection",
            "formula": "official orbit/axis/mask/source-profile correction from parent response to fitted EP channel",
            "value_or_interval": "PARTIAL_READOUT_ONLY_OFFICIAL_ARRAYS_NOT_IMPORTED",
            "status": "BLOCKS_CLAIM_GRADE_TAU",
            "source_path": str(SRC / "P8_Y5_R2FR_3364_WEP_PROJECTION_OWNER_AUDIT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def material_proxy_rows(timestamp: str) -> list[dict[str, Any]]:
    proxy = dd_proxy()
    rows: list[dict[str, Any]] = []
    for component in DD_COMPONENTS:
        rows.append(
            {
                "row_id": f"DDP3992_{component}",
                "component": component,
                "DeltaQ_TA6V_minus_PtRh10": f"{proxy['Delta_' + component]:.12e}",
                "Q_Earth": f"{proxy['Earth_' + component]:.12e}",
                "product": f"{proxy['Delta_' + component] * proxy['Earth_' + component]:.12e}",
                "units": "dimensionless",
                "status": "DD_PROXY_COMPONENT_NONCLAIM",
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    rows.append(
        {
            "row_id": "DDP3992_total",
            "component": "DD_proxy_total",
            "DeltaQ_TA6V_minus_PtRh10": f"L1={proxy['l1_material_delta']:.12e}; L2={proxy['l2_material_delta']:.12e}",
            "Q_Earth": f"L2={proxy['l2_earth_source']:.12e}",
            "product": f"dot={proxy['dot_Earth_DeltaQ_TA6V_minus_PtRh10']:.12e}; abs_tau_proxy_low={proxy['abs_tau_proxy_low']:.12e}",
            "units": "dimensionless",
            "status": "NUMERIC_PROXY_DENOMINATOR_READY_PARENT_MAP_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    rows.append(
        {
            "row_id": "DDP3992_coeff_bound",
            "component": "DD_proxy_coefficient_bound",
            "DeltaQ_TA6V_minus_PtRh10": "single coefficient along DD proxy product",
            "Q_Earth": f"eta_bound={proxy['eta_bound_abs']:.12e}",
            "product": f"|C_DD_proxy| <= {proxy['dd_proxy_coeff_bound_using_tau_low']:.12e} if K_parent_to_DD=1 and lower readout bound is used",
            "units": "dimensionless coefficient proxy",
            "status": "DD_PROXY_SMOKE_BOUND_NOT_MTS_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    proxy = dd_proxy()
    return [
        {
            "case_id": "CASE3992_0_effective_contrast_bound",
            "route": "effective_readout_normalized",
            "eta_bound_abs": proxy["eta_bound_abs"],
            "tau_denominator": 1.0,
            "parent_basis_map_ready": False,
            "official_projection_ready": True,
            "theorem_zero": False,
            "status": "REAL_EFFECTIVE_CONTRAST_BOUND_NONCLAIM",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3992_1_DD_proxy_denominator",
            "route": "DD_proxy",
            "eta_bound_abs": proxy["eta_bound_abs"],
            "tau_denominator": proxy["abs_tau_proxy_low"],
            "parent_basis_map_ready": False,
            "official_projection_ready": False,
            "theorem_zero": False,
            "status": "NUMERIC_PROXY_ONLY_PARENT_MAP_MISSING",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3992_2_raw_MTS_projection_missing",
            "route": "raw_MTS",
            "eta_bound_abs": proxy["eta_bound_abs"],
            "tau_denominator": "",
            "parent_basis_map_ready": False,
            "official_projection_ready": False,
            "theorem_zero": False,
            "status": "MISSING_PARENT_BASIS_AND_OFFICIAL_PROJECTION",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3992_3_no_Hom_zero_conditional",
            "route": "parent_theorem_zero",
            "eta_bound_abs": proxy["eta_bound_abs"],
            "tau_denominator": "",
            "parent_basis_map_ready": False,
            "official_projection_ready": False,
            "theorem_zero": True,
            "status": "CONDITIONAL_ZERO_PARENT_UNSIGNED",
            "timestamp_utc": timestamp,
        },
    ]


def evaluate_case(row: dict[str, Any]) -> dict[str, Any]:
    eta = float(row["eta_bound_abs"])
    theorem_zero = str(row.get("theorem_zero", "")).lower() == "true"
    route = row["route"]
    result: dict[str, Any] = {
        "case_id": row["case_id"],
        "route": route,
        "input_status": row["status"],
        "eta_bound_abs": eta,
        "tau_used": "MISSING",
        "coefficient_bound": "MISSING",
        "passes_effective_or_proxy_bound": False,
        "score_ready": False,
        "claim_allowed": False,
        "valid_for_claim": False,
    }
    if theorem_zero:
        result.update(
            {
                "tau_used": "not_required_if_Delta_w_zero",
                "coefficient_bound": "0",
                "passes_effective_or_proxy_bound": True,
                "input_status": "CONDITIONAL_NO_HOM_ZERO_PARENT_UNSIGNED",
            }
        )
        return result
    tau = row.get("tau_denominator", "")
    if tau == "":
        return result
    tau_value = float(tau)
    if tau_value <= 0:
        result["input_status"] = "NONPOSITIVE_TAU_DENOMINATOR"
        return result
    coeff_bound = eta / tau_value
    result.update(
        {
            "tau_used": f"{tau_value:.12e}",
            "coefficient_bound": f"{coeff_bound:.12e}",
            "passes_effective_or_proxy_bound": True,
        }
    )
    return result


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows = [evaluate_case(row) for row in cases]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM3992_0_effective_bound_not_raw_claim",
            "claim": "MICROSCOPE bound constrains readout-normalized effective contrast",
            "allowed": True,
            "reason": "this is an observational/effective statement, not a raw MTS source-weight coefficient claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3992_1_no_raw_MTS_tau_claim",
            "claim": "raw MTS Delta_w_TiPt bound from MICROSCOPE",
            "allowed": False,
            "reason": "parent-to-DD/source response map and official projection are missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3992_2_no_local_GR_claim",
            "claim": "local GR/Newton source coupling closes",
            "allowed": False,
            "reason": "DD proxy denominator is not the parent MTS denominator and no-Hom zero remains unsigned",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    proxy = dd_proxy()
    return [
        {
            "decision_id": "DEC3992_0",
            "finding": "effective WEP contrast bound is derived",
            "evidence": f"|Delta_w_eff_TiPt| <= {proxy['eta_bound_abs']:.12e}",
            "limitation": "Delta_w_eff is the readout-normalized observable component, not raw MTS Delta_w",
            "next_action": "use as comparator/check target only",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3992_1",
            "finding": "DD proxy denominator is numeric",
            "evidence": f"dot(Q_Earth_DD,DeltaQ_TA6V_minus_PtRh10)={proxy['dot_Earth_DeltaQ_TA6V_minus_PtRh10']:.12e}; |tau_proxy|>={proxy['abs_tau_proxy_low']:.12e}",
            "limitation": "DD proxy requires parent-to-DD/source-response map before becoming an MTS coefficient bound",
            "next_action": "derive K_parent_to_DD or source-weight zero in 3993",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3992_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive the parent-to-DD/source-response basis map, or close the no-Hom source-weight zero",
            "success_condition": "DD proxy denominator is either promoted through a parent-owned map or explicitly demoted to comparator-only while no-Hom zero is attacked",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "EFFECTIVE_WEP_BOUND_DERIVED_DD_PROXY_DENOMINATOR_NUMERIC_RAW_PARENT_MAP_OPEN",
            "headline": "MICROSCOPE now gives an exact effective contrast bound and a numeric DD proxy denominator, but raw MTS coupling still needs parent basis ownership",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    proxy = dd_proxy()
    found = sum(bool(row["needle_found"]) for row in sources)
    lines = [
        "# 3992 - Parent Source-Weight Projection Or WEP Tau Denominator",
        "",
        f"Timestamp: `{timestamp}`",
        "",
        "## Result",
        "",
        "This checkpoint attacks the WEP denominator rather than relabelling it missing.",
        "",
        "Two things now separate cleanly:",
        "",
        "1. the readout-normalized effective WEP contrast; and",
        "2. the raw MTS parent source-weight coefficient.",
        "",
        "## Exact Effective Bound",
        "",
        "For `a_A=g_N(1+epsilon_A)` and `a_B=g_N(1+epsilon_B)`,",
        "",
        "`eta_AB = 2(epsilon_A-epsilon_B)/(2+epsilon_A+epsilon_B)`.",
        "",
        "Defining `Delta_w_eff_TiPt` as the source component already in the MICROSCOPE Eotvos readout convention gives",
        "",
        f"`|Delta_w_eff_TiPt| <= {proxy['eta_bound_abs']:.12e}`.",
        "",
        "This is a real effective-observable bound. It is not a raw MTS coupling claim.",
        "",
        "## Numeric DD Proxy Denominator",
        "",
        "Using the existing DD proxy Earth/source vector and MICROSCOPE material rows:",
        "",
        f"`dot(Q_Earth_DD, DeltaQ_TA6V_minus_PtRh10) = {proxy['dot_Earth_DeltaQ_TA6V_minus_PtRh10']:.12e}`.",
        "",
        f"With `0.98 <= tau_readout_X <= 1.02`, this gives `|tau_DD_proxy| >= {proxy['abs_tau_proxy_low']:.12e}`.",
        "",
        f"If, and only if, a future parent map proves `K_parent_to_DD=1` in this compressed channel, the proxy coefficient smoke bound would be `|C_DD_proxy| <= {proxy['dd_proxy_coeff_bound_using_tau_low']:.12e}`.",
        "",
        "That last line is deliberately nonclaim: the parent-to-DD/source-response map is the live missing object.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: status `{row['input_status']}`, tau `{row['tau_used']}`, coeff_bound `{row['coefficient_bound']}`, claim={row['claim_allowed']}"
        )
    lines.extend(
        [
            "",
            "## Current Closure Gate",
            "",
            "The WEP side is no longer just missing. It now has an exact effective observable bound and a numeric DD proxy denominator. The remaining hard gate is the parent map from MTS source-weight residuals into that response basis, or the no-Hom theorem-zero.",
            "",
            "## Source Register",
            "",
            f"`{found}/{len(sources)}` source needles found.",
        ]
    )
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
            "Derive the parent-to-DD/source-response map, or prove the no-Hom source-weight zero.",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def update_spine(timestamp: str) -> None:
    proxy = dd_proxy()
    header = "## 3992 - Effective WEP Bound And DD Proxy Denominator"
    block = "\n".join(
        [
            "",
            header,
            "",
            f"- Timestamp: `{timestamp}`",
            "- Status: `EFFECTIVE_WEP_BOUND_DERIVED_DD_PROXY_DENOMINATOR_NUMERIC_RAW_PARENT_MAP_OPEN`",
            "- Exact effective result:",
            f"  `|Delta_w_eff_TiPt| <= {proxy['eta_bound_abs']:.12e}` in the MICROSCOPE readout-normalized Eotvos convention.",
            "- Numeric proxy denominator:",
            f"  `dot(Q_Earth_DD,DeltaQ_TA6V_minus_PtRh10)={proxy['dot_Earth_DeltaQ_TA6V_minus_PtRh10']:.12e}` and `|tau_DD_proxy| >= {proxy['abs_tau_proxy_low']:.12e}` using the sourced readout interval.",
            "- Nonclaim guard:",
            "  the DD proxy denominator does not yet bind raw MTS `Delta_w` until a parent-to-DD/source-response basis map is derived.",
            "- Current bottleneck:",
            "  derive `K_parent_to_DD` or close the 3990 no-Hom source-weight zero.",
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
    factors: list[dict[str, Any]],
    material: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": timestamp})

    proxy = dd_proxy()
    add("VAL3992_00_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3992_01_needles_found", all(row["needle_found"] for row in sources), "every cited source needle found")
    add("VAL3992_02_effective_theorem", any(row["theorem_id"] == "WEN3992_1_effective_tau" for row in theorem), "effective tau theorem row present")
    add("VAL3992_03_raw_factor_law", any(row["theorem_id"] == "WEN3992_2_raw_tau_factorization" for row in theorem), "raw tau factorization row present")
    add("VAL3992_04_eta_positive", proxy["eta_bound_abs"] > 0.0, "eta bound positive")
    add("VAL3992_05_readout_interval", 0.0 < proxy["tau_readout_low"] < 1.0 < proxy["tau_readout_high"], "readout interval straddles unity")
    add("VAL3992_06_material_delta_nonzero", proxy["l2_material_delta"] > 0.0, "material DD contrast nonzero")
    add("VAL3992_07_earth_vector_nonzero", proxy["l2_earth_source"] > 0.0, "Earth DD source vector nonzero")
    add("VAL3992_08_dot_nonzero", proxy["abs_dot_Earth_DeltaQ"] > 0.0, "DD proxy dot product nonzero")
    add("VAL3992_09_proxy_bound_finite", math.isfinite(proxy["dd_proxy_coeff_bound_using_tau_low"]) and proxy["dd_proxy_coeff_bound_using_tau_low"] > 0.0, "proxy coefficient bound finite positive")
    add("VAL3992_10_factor_rows", len(factors) >= 5, "tau factor rows written")
    add("VAL3992_11_material_rows", len(material) >= 6, "material/Earth proxy rows written")
    effective = next(row for row in results if row["case_id"] == "CASE3992_0_effective_contrast_bound")
    proxy_case = next(row for row in results if row["case_id"] == "CASE3992_1_DD_proxy_denominator")
    raw = next(row for row in results if row["case_id"] == "CASE3992_2_raw_MTS_projection_missing")
    zero = next(row for row in results if row["case_id"] == "CASE3992_3_no_Hom_zero_conditional")
    add("VAL3992_12_effective_result", str(effective["passes_effective_or_proxy_bound"]).lower() == "true", "effective contrast result executes")
    add("VAL3992_13_proxy_result", str(proxy_case["passes_effective_or_proxy_bound"]).lower() == "true" and str(proxy_case["valid_for_claim"]).lower() == "false", "DD proxy executes as nonclaim")
    add("VAL3992_14_raw_blocks", raw["coefficient_bound"] == "MISSING" and str(raw["passes_effective_or_proxy_bound"]).lower() == "false", "raw MTS projection blocks")
    add("VAL3992_15_zero_conditional", zero["coefficient_bound"] == "0" and str(zero["valid_for_claim"]).lower() == "false", "no-Hom zero route conditional nonclaim")
    add("VAL3992_16_claim_gate_false_for_raw", "no raw MTS" in read_text(OUTPUTS["claim_gate"]) or "raw MTS" in read_text(OUTPUTS["claim_gate"]), "raw claim gate present")
    add("VAL3992_17_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL3992_18_doc_exists", DOC_PATH.exists() and "DD proxy denominator" in read_text(DOC_PATH), "document written")
    add("VAL3992_19_spine_updated", SPINE_PATH.exists() and "## 3992 - Effective WEP Bound And DD Proxy Denominator" in read_text(SPINE_PATH), "spine updated")
    add("VAL3992_20_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL3992_21_compile", compile_ok, "script compiles")
    add("VAL3992_22_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL3992_23_status_exists", OUTPUTS["status"].exists(), "status file exists")
    add("VAL3992_24_results_nonclaim", not any(str(row["valid_for_claim"]).lower() == "true" for row in results), "all evaluator results remain nonclaim")
    return rows


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    factors = factor_rows(timestamp)
    material = material_proxy_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    claim_gate = claim_gate_rows(timestamp)
    decision = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["factors"], factors)
    write_csv(OUTPUTS["material"], material)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["claim_gate"], claim_gate)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    update_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validation = build_validation_rows(timestamp, sources, theorem, factors, material, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)

    failed = [row for row in validation if str(row["passed"]).lower() != "true"]
    print(f"3992 validation: {len(validation) - len(failed)}/{len(validation)} passed")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
