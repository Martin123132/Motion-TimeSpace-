from __future__ import annotations

import csv
import math
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3994"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3994-Y5-R2FR-no-extra-F2-operator-domain-or-finite-EM-DD-coefficient-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3994_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3994_NO_EXTRA_F2_OPERATOR_DOMAIN_THEOREM.csv",
    "gate": SRC / "P8_Y5_R2FR_3994_OPERATOR_DOMAIN_GATE.csv",
    "bounds": SRC / "P8_Y5_R2FR_3994_FINITE_EM_DD_COEFFICIENT_BOUNDS.csv",
    "poynting": SRC / "P8_Y5_R2FR_3994_POYNTING_FLUX_ZERO_OR_BOUND_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_3994_EM_DD_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_3994_EM_DD_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_3994_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3994_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3994_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3994_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3994_VALIDATION.csv",
}

NEXT_DOC = "3995-Y5-R2FR-current-normalization-zg-zero-or-joint-alpha-F2-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3995_current_normalization_zg_zero_or_joint_alpha_F2_bound.py"


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
        ("SRC3994_00_3993_next", SRC / "P8_Y5_R2FR_3993_NEXT_TARGET.csv", "NEXT3993_0", "3993 handoff"),
        ("SRC3994_01_3993_components", SRC / "P8_Y5_R2FR_3993_PARENT_TO_DD_COMPONENT_BASIS.csv", "PDM3993_4_C_alpha_EM", "C_alpha DD component"),
        ("SRC3994_02_3993_em", SRC / "P8_Y5_R2FR_3993_EM_POYNTING_MAP_LEDGER.csv", "EMDD3993_1_independent_F2_or_alpha", "EM F2/Poynting handoff"),
        ("SRC3994_03_3864_theorem", SRC / "P8_Y5_R2FR_3864_NO_EXTRA_F2_THEOREM.csv", "NEF3864_1_no_extra_F2_theorem", "no-extra-F2 theorem"),
        ("SRC3994_04_3864_operator", SRC / "P8_Y5_R2FR_3864_OPERATOR_DOMAIN_AUDIT.csv", "ODA3864_0_parent_image", "operator-domain audit"),
        ("SRC3994_05_3864_lambda_bound", SRC / "P8_Y5_R2FR_3864_LAMBDAF2_BOUND.csv", "LFB3864_0_canonical_identity", "lambda F2 bound identity"),
        ("SRC3994_06_3865_joint", SRC / "P8_Y5_R2FR_3865_SXF2_ZG_BALPHA_JOINT_BOUND.csv", "JHB3865_0_linear_constraint", "sXF2 zg balpha joint bound"),
        ("SRC3994_07_3874_active", SRC / "P8_Y5_R2FR_3874_ACTIVE_F2_RESIDUAL_DEFINITION.csv", "AR3874_2_sXF2_active", "active F2 residual definition"),
        ("SRC3994_08_3863_owner", SRC / "P8_Y5_R2FR_3863_MAXWELL_NORMALIZATION_OWNER_THEOREM.csv", "MNO3863_2_normalization_owner_theorem", "Maxwell normalization owner"),
        ("SRC3994_09_3809_norm", SRC / "P8_Y5_R2FR_3809_MAXWELL_NORMALIZATION_THEOREM.csv", "MNT3809_3_no_extra_F2_countermodel", "Maxwell normalization countermodel"),
        ("SRC3994_10_3528_domain", SRC / "P8_Y5_R2FR_3528_OPERATOR_DOMAIN_RESULT.csv", "OP3528_2_hidden_scalar_lambda", "operator-domain result"),
        ("SRC3994_11_3507_alpha", SRC / "P8_Y5_R2FR_3507_ALPHA_RESIDUAL_VECTOR.csv", "ARE3507_1_C_XF2", "alpha/F2 residual vector"),
        ("SRC3994_12_3883_poynting", SRC / "P8_Y5_R2FR_3883_MAXWELL_STRESS_POYNTING_DERIVATION.csv", "MX3883_4_poynting", "Poynting accounting"),
        ("SRC3994_13_3961_flux", SRC / "P8_Y5_R2FR_3961_POYNTING_NO_FLUX_THEOREM_OR_BOUND.csv", "PNF3961_2_flux_bound", "Poynting flux bound"),
        ("SRC3994_14_3981_controlled", SRC / "P8_Y5_R2FR_3981_CONTROLLED_POYNTING_SILENCE_THEOREM.csv", "CPS3981_0_branch", "controlled Poynting silence"),
        ("SRC3994_15_3579_flux_rows", SRC / "P8_Y5_R2FR_3579_POYNTING_FLUX_BOUND_ROWS.csv", "PFB3579_1_Phi_EM_rad", "Poynting finite flux row"),
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


def c_alpha_bound() -> float:
    rows = read_csv(SRC / "P8_Y5_R2FR_3993_PARENT_TO_DD_COMPONENT_BASIS.csv")
    for row in rows:
        if row.get("parent_symbol") == "C_alpha_EM":
            return float(row["single_channel_bound_if_only_component"])
    raise RuntimeError("3993 C_alpha_EM bound row missing")


def c_alpha_dd_weight() -> float:
    rows = read_csv(SRC / "P8_Y5_R2FR_3993_PARENT_TO_DD_COMPONENT_BASIS.csv")
    for row in rows:
        if row.get("parent_symbol") == "C_alpha_EM":
            return abs(float(row["coefficient_weight_TA6V_PtRh10_Earth"]))
    raise RuntimeError("3993 C_alpha_EM DD weight row missing")


def c_alpha_readout_floor() -> float:
    c_alpha = c_alpha_bound()
    weight = c_alpha_dd_weight()
    if c_alpha <= 0.0 or weight <= 0.0:
        raise RuntimeError("cannot reconstruct readout floor from 3993 C_alpha_EM row")
    return eta_bound() / (c_alpha * weight)


def tau_proxy_low() -> float:
    rows = read_csv(SRC / "P8_Y5_R2FR_3993_DD_PROXY_BOUND_EVALUATOR_RESULTS.csv")
    for row in rows:
        if row.get("case_id") == "CASE3993_1_DD_proxy_unit_map_bound":
            return float(row["tau_proxy_low"])
    raise RuntimeError("3993 tau proxy row missing")


def eta_bound() -> float:
    rows = read_csv(SRC / "P8_Y5_R2FR_3993_DD_PROXY_BOUND_EVALUATOR_RESULTS.csv")
    for row in rows:
        if row.get("case_id") == "CASE3993_1_DD_proxy_unit_map_bound":
            return float(row["eta_bound_abs"])
    raise RuntimeError("3993 eta bound row missing")


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "F2G3994_0_ord_symmetry_countermodel",
            "claim_piece": "ordinary symmetry does not ban extra F2",
            "mathematical_form": "DeltaS_F2=-1/4 int sqrt(-g_obs) lambda(Phi,readout,hidden) F_Q^2 is diffeomorphism and U(1) gauge invariant.",
            "derived_result": "ordinary covariance/gauge symmetry alone cannot close EM source normalization",
            "status": "COUNTERMODEL_RETAINED_NO_SHORTCUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "F2G3994_1_no_extra_F2_zero",
            "claim_piece": "no-extra-F2 operator-domain theorem",
            "mathematical_form": "If Allowed[S_vis]=Image(ParentGenerate) and that image contains the Q-subblock only as C_P N_Q F_Q^2, with no separate Coeff(F_Q^2), no hidden/readout Hom into that coefficient, same-current owner, and radiative/readout closure in the same image, then D_v lambda_F2=D_v f_X=D_v delta_lambda_rad=0 for v in ker(Dq_obs).",
            "derived_result": "C_XF2, s_XF2, active alpha drift, and EM source-scale leakage vanish locally under the signed image theorem",
            "status": "EXACT_CONDITIONAL_ZERO_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "F2G3994_2_canonical_identity",
            "claim_piece": "finite F2/current identity",
            "mathematical_form": "For S_EM,J=-1/4 int lambda_A F_Q^2 + int g_J A_Q J_Q, define s_XF2=D_X ln lambda_A and z_g=D_X ln g_J. Then b_alpha_X=2 z_g-s_XF2.",
            "derived_result": "an alpha/F2 branch must be bounded jointly; alpha-only shortcuts cannot isolate s_XF2 while z_g is live",
            "status": "EXACT_LINEAR_IDENTITY_FOR_BOUND_BRANCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "F2G3994_3_constant_calibration_split",
            "claim_piece": "constant F2 calibration",
            "mathematical_form": "A universal hidden-independent constant lambda_0 F_Q^2 is an absolute alpha/mu0 calibration debt, not a local vertical residual by itself.",
            "derived_result": "do not claim alpha's value, but do not treat constant calibration as WEP/local drift pressure",
            "status": "CALIBRATION_NOT_LOCAL_RESIDUAL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "F2G3994_4_Poynting_flux_bound",
            "claim_piece": "Poynting zero-or-bound law",
            "mathematical_form": "dU_EM/dt + int_boundary S_Poynting.n dA = - int_D J.E dV, hence |Phi_EM_rad| <= |dU_EM/dt| + |W_matter| unless the stationary isolated no-flux branch sets it to zero.",
            "derived_result": "Poynting is either Hilbert-stress/internal exchange, controlled zero, or explicit flux residual",
            "status": "POYNTING_ZERO_OR_BOUND_LAW_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "ODG3994_0_parent_image",
            "slot": "visible operator-domain image",
            "required_for_zero": "Allowed[S_vis]=Image(ParentGenerate) with no free Coeff(F_Q^2)",
            "current_status": "UNSIGNED_PARENT_IMAGE_THEOREM",
            "if_fails": "retain C_XF2 and s_XF2 active residuals",
            "source_path": str(SRC / "P8_Y5_R2FR_3864_OPERATOR_DOMAIN_AUDIT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "ODG3994_1_hidden_hom",
            "slot": "hidden/readout Hom into Coeff(F_Q^2)",
            "required_for_zero": "no hidden, motion, time, material, or readout map can feed lambda_F2",
            "current_status": "CONDITIONAL_NO_HOM_UNSIGNED",
            "if_fails": "retain C_XF2_active and C_EM_readout",
            "source_path": str(SRC / "P8_Y5_R2FR_3528_OPERATOR_DOMAIN_RESULT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "ODG3994_2_current_owner",
            "slot": "same-current normalization z_g",
            "required_for_zero": "J_Q and A_Q current are extracted before readout from one parent current owner",
            "current_status": "z_g_LIVE",
            "if_fails": "bound s_XF2 jointly with z_g via b_alpha_X=2 z_g-s_XF2",
            "source_path": str(SRC / "P8_Y5_R2FR_3865_SXF2_ZG_BALPHA_JOINT_BOUND.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "ODG3994_3_radiative_readout",
            "slot": "radiative/readout regenerated F2",
            "required_for_zero": "effective action and readout maps remain q-basic/image-stable",
            "current_status": "UNSIGNED_RADIOUT_CLOSURE",
            "if_fails": "retain delta_lambda_rad and C_EM_readout",
            "source_path": str(SRC / "P8_Y5_R2FR_3864_OPERATOR_DOMAIN_AUDIT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "ODG3994_4_Poynting_flux",
            "slot": "boundary Poynting flux",
            "required_for_zero": "closed stationary source worldtube or finite flux bound",
            "current_status": "CONTROLLED_BRANCH_ZERO_AVAILABLE_GENERAL_BOUND_MISSING",
            "if_fails": "retain Phi_EM_rad/(G_ref M_H)",
            "source_path": str(SRC / "P8_Y5_R2FR_3961_POYNTING_NO_FLUX_THEOREM_OR_BOUND.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    c_alpha = c_alpha_bound()
    c_alpha_weight = c_alpha_dd_weight()
    c_alpha_readout = c_alpha_readout_floor()
    tau = tau_proxy_low()
    eta = eta_bound()
    return [
        {
            "bound_id": "FEB3994_0_C_alpha_EM_DD",
            "target": "C_alpha_EM",
            "formula": "|C_alpha_EM| <= eta_bound/(readout_floor*|Qe_Earth DeltaQe|) as a single-channel DD proxy comparator",
            "numeric_value": f"{c_alpha:.12e}",
            "units": "dimensionless per normalized parent coefficient",
            "derivation": "imports 3993 C_alpha_EM single-channel DD proxy bound",
            "status": "NUMERIC_PROXY_BOUND_NONCLAIM_PARENT_MAP_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "FEB3994_1_eta_at_C_alpha_bound",
            "target": "eta_alpha_proxy",
            "formula": "|eta_alpha_proxy| = readout_floor * |Qe_Earth DeltaQe| * |C_alpha_EM|",
            "numeric_value": f"{c_alpha_readout * c_alpha_weight * c_alpha:.12e}",
            "units": "dimensionless",
            "derivation": f"readout_floor={c_alpha_readout:.12e}, full_DD_tau_proxy={tau:.12e}, |Qe_Earth DeltaQe|={c_alpha_weight:.12e}, eta_bound={eta:.12e}",
            "status": "SATURATES_DD_PROXY_COMPARATOR_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "FEB3994_2_sXF2_joint",
            "target": "s_XF2",
            "formula": "|s_XF2| <= |b_alpha_X| + 2|z_g|",
            "numeric_value": "MISSING_b_alpha_X_AND_z_g",
            "units": "dimensionless per normalized Xhat",
            "derivation": "canonical identity b_alpha_X=2 z_g-s_XF2",
            "status": "JOINT_BOUND_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "FEB3994_3_active_F2_total",
            "target": "B_lambdaF2_3994",
            "formula": "B_lambdaF2_3994 <= |s_XF2| + |C_XF2| + |delta_lambda_rad| + |delta_lambda_readout|",
            "numeric_value": "SYMBOLIC_BOUND_INPUTS_MISSING",
            "units": "dimensionless/source-normalized",
            "derivation": "active F2 residual excludes pure constant calibration but retains hidden/radiative/readout derivatives",
            "status": "ACTIVE_F2_BOUND_VECTOR_READY_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "FEB3994_4_EM_source_scale_update",
            "target": "B_EM_scale_3994",
            "formula": "B_EM_scale_3994 <= B_lambdaF2_3994 + |z_g| + |Delta_Hodge_EM| + |Phi_EM_rad|/(G_ref M_H) + |C_EM_readout|",
            "numeric_value": "SYMBOLIC_BOUND_INPUTS_MISSING",
            "units": "dimensionless/source-normalized",
            "derivation": "combines F2/current/Hodge/Poynting residuals into EM source-scale branch",
            "status": "SOURCE_SCALE_BOUND_REFINED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def poynting_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PY3994_0_stationary_zero",
            "target": "Phi_EM_rad",
            "condition": "time_avg(dU_EM/dt)=0, time_avg(int_D J.E dV)=0, closed stationary isolated worldtube, no external radiation",
            "result": "time_avg(Phi_EM_rad)=0",
            "status": "CONDITIONAL_ZERO_BRANCH",
            "source_path": str(SRC / "P8_Y5_R2FR_3961_POYNTING_NO_FLUX_THEOREM_OR_BOUND.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PY3994_1_controlled_monopole",
            "target": "Phi_EM_rad",
            "condition": "controlled neutral/nonradiating EH-monopole branch",
            "result": "Poynting blocker closed only for that branch",
            "status": "BRANCH_SPECIFIC_ZERO_DERIVED_NONCLAIM",
            "source_path": str(SRC / "P8_Y5_R2FR_3981_CONTROLLED_POYNTING_SILENCE_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PY3994_2_flux_bound",
            "target": "Phi_EM_rad",
            "condition": "general nonstationary/radiative branch",
            "result": "|Phi_EM_rad| <= |dU_EM/dt| + |W_matter|",
            "status": "FINITE_FLUX_BOUND_TEMPLATE_VALUE_MISSING",
            "source_path": str(SRC / "P8_Y5_R2FR_3579_POYNTING_FLUX_BOUND_ROWS.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    c_alpha = c_alpha_bound()
    return [
        {
            "case_id": "CASE3994_0_no_extra_F2_zero",
            "route": "operator_domain_zero",
            "C_alpha_EM": 0.0,
            "s_XF2": 0.0,
            "z_g": 0.0,
            "Phi_EM_rad_norm": 0.0,
            "input_status": "CONDITIONAL_ZERO_PARENT_UNSIGNED",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3994_1_C_alpha_at_DD_proxy_bound",
            "route": "finite_C_alpha_proxy",
            "C_alpha_EM": c_alpha,
            "s_XF2": "",
            "z_g": "",
            "Phi_EM_rad_norm": 0.0,
            "input_status": "DD_PROXY_SINGLE_CHANNEL_NONCLAIM",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3994_2_small_joint_F2_smoke",
            "route": "joint_sXF2_zg_smoke",
            "C_alpha_EM": 0.25 * c_alpha,
            "s_XF2": 0.10 * c_alpha,
            "z_g": 0.05 * c_alpha,
            "Phi_EM_rad_norm": 0.0,
            "input_status": "NUMERIC_SMOKE_ONLY_NOT_EVIDENCE",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3994_3_missing_zg_alpha",
            "route": "joint_sXF2_zg",
            "C_alpha_EM": "",
            "s_XF2": "",
            "z_g": "",
            "Phi_EM_rad_norm": 0.0,
            "input_status": "MISSING_b_alpha_X_z_g_sXF2",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3994_4_Poynting_flux_open",
            "route": "Poynting_flux",
            "C_alpha_EM": "",
            "s_XF2": "",
            "z_g": "",
            "Phi_EM_rad_norm": "",
            "input_status": "MISSING_FLUX_OR_ZERO_THEOREM_GENERAL_BRANCH",
            "timestamp_utc": timestamp,
        },
    ]


def optional_float(value: Any) -> float | None:
    text = str(value).strip()
    if not text:
        return None
    return float(text)


def evaluate_case(row: dict[str, Any]) -> dict[str, Any]:
    tau = tau_proxy_low()
    eta = eta_bound()
    c_alpha_weight = c_alpha_dd_weight()
    c_alpha_readout = c_alpha_readout_floor()
    c_alpha = optional_float(row.get("C_alpha_EM"))
    sxf2 = optional_float(row.get("s_XF2"))
    zg = optional_float(row.get("z_g"))
    phi = optional_float(row.get("Phi_EM_rad_norm"))
    result: dict[str, Any] = {
        "case_id": row["case_id"],
        "route": row["route"],
        "input_status": row["input_status"],
        "eta_bound_abs": eta,
        "full_DD_tau_proxy": f"{tau:.12e}",
        "readout_floor": f"{c_alpha_readout:.12e}",
        "DD_weight_abs": f"{c_alpha_weight:.12e}",
        "eta_EM_proxy_abs": "MISSING",
        "sXF2_bound_lhs": "MISSING",
        "B_EM_scale_proxy": "MISSING",
        "passes_DD_proxy": False,
        "score_ready": False,
        "claim_allowed": False,
        "valid_for_claim": False,
    }
    if c_alpha is None:
        return result
    eta_proxy = c_alpha_readout * c_alpha_weight * abs(c_alpha)
    sxf2_lhs = abs(sxf2) if sxf2 is not None else 0.0
    zg_lhs = abs(zg) if zg is not None else 0.0
    phi_lhs = abs(phi) if phi is not None else 0.0
    b_em_scale = abs(c_alpha) + sxf2_lhs + zg_lhs + phi_lhs
    result.update(
        {
            "eta_EM_proxy_abs": f"{eta_proxy:.12e}",
            "sXF2_bound_lhs": f"{sxf2_lhs:.12e}",
            "B_EM_scale_proxy": f"{b_em_scale:.12e}",
            "passes_DD_proxy": eta_proxy <= eta * (1.0 + 1.0e-12),
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
            "decision_id": "DEC3994_0",
            "finding": "no-extra-F2 is an exact conditional theorem, not an ordinary-symmetry result",
            "evidence": "F_Q^2 counterterm is legal unless parent visible operator image/no-Hom/radiative clauses are signed",
            "limitation": "current corpus has not parent-signed those clauses",
            "next_action": "attack same-current z_g or build joint b_alpha/sXF2/z_g numeric branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3994_1",
            "finding": "first finite EM/DD proxy coefficient bound is executable",
            "evidence": f"|C_alpha_EM| <= {c_alpha_bound():.12e} in the single-channel DD proxy comparator",
            "limitation": "not a raw MTS claim until parent-to-DD map and same-current owner close",
            "next_action": "3995 should target z_g/current normalization because b_alpha=2z_g-sXF2 is the live degeneracy",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM3994_0_no_F2_zero_claim",
            "claim": "no-extra-F2 operator-domain theorem is parent-signed",
            "allowed": False,
            "reason": "visible operator-domain image, hidden/readout Hom exclusion, radiative closure, and same-current owner remain unsigned",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3994_1_no_EM_DD_claim",
            "claim": "finite EM/DD coefficient bound is an MTS prediction",
            "allowed": False,
            "reason": "C_alpha_EM bound is a DD proxy comparator and parent-to-DD map is not signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3994_2_no_Poynting_general_claim",
            "claim": "Poynting flux is zero generally",
            "allowed": False,
            "reason": "zero holds only on stationary/controlled no-flux branches; general branch needs finite flux data",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3994_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "prove same-current/current-normalization z_g=0 or build the joint alpha/F2/current finite-bound runner",
            "success_condition": "z_g is theorem-zero, or b_alpha_X, s_XF2, and z_g enter a shared source-backed no-cancellation bound row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "NO_EXTRA_F2_THEOREM_CONDITIONAL_FIRST_EM_DD_PROXY_BOUND_READY",
            "headline": "extra F2 is not killed by ordinary symmetry; it is theorem-zero only by parent operator-domain image, otherwise C_alpha_EM/sXF2/z_g/Poynting are finite residuals",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(bool(row["needle_found"]) for row in sources)
    lines = [
        "# 3994 - No-Extra-F2 Operator Domain Or Finite EM/DD Coefficient Bound",
        "",
        f"Timestamp: `{timestamp}`",
        "",
        "## Result",
        "",
        "This checkpoint attacks the EM gate directly.",
        "",
        "Ordinary diffeomorphism and U(1) gauge symmetry do **not** forbid an extra `lambda(Phi) F_Q^2` term. The zero route needs the stronger parent visible-operator-domain image theorem.",
        "",
        "## Zero Route",
        "",
        "If `Allowed[S_vis]=Image(ParentGenerate)` and there is no separate `Coeff(F_Q^2)` object, no hidden/readout Hom into it, same-current ownership, and radiative/readout closure, then",
        "",
        "`D_v lambda_F2 = D_v f_X = D_v delta_lambda_rad = 0`",
        "",
        "for local vertical `v in ker(Dq_obs)`. This kills `C_XF2`, `s_XF2`, active alpha drift, and EM source-scale leakage locally.",
        "",
        "## Finite Route",
        "",
        "`b_alpha_X = 2 z_g - s_XF2`, so the branch must be bounded jointly:",
        "",
        "`|s_XF2| <= |b_alpha_X| + 2|z_g|`.",
        "",
        f"The first EM/DD proxy comparator bound is `|C_alpha_EM| <= {c_alpha_bound():.12e}` for the single-channel `Q_e` route.",
        "",
        "## Poynting",
        "",
        "Poynting is now cleanly split:",
        "",
        "- stationary/controlled closed worldtube: `Phi_EM_rad=0` conditionally;",
        "- general radiative branch: `|Phi_EM_rad| <= |dU_EM/dt| + |W_matter|`;",
        "- internal circulating Poynting is not deleted; it belongs inside total Hilbert/Maxwell stress.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: status `{row['input_status']}`, eta_EM `{row['eta_EM_proxy_abs']}`, B_EM `{row['B_EM_scale_proxy']}`, claim={row['claim_allowed']}"
        )
    lines.extend(
        [
            "",
            "## Current Closure Gate",
            "",
            "The sharpest next gate is same-current/current-normalization `z_g`. Without `z_g=0`, alpha/F2 data cannot isolate `s_XF2`; with `z_g=0`, the `F^2` branch collapses onto alpha/source product rows.",
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
            "Prove same-current/current-normalization `z_g=0`, or build the joint alpha/F2/current finite-bound runner.",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def update_spine(timestamp: str) -> None:
    header = "## 3994 - No-Extra-F2 EM Gate"
    block = "\n".join(
        [
            "",
            header,
            "",
            f"- Timestamp: `{timestamp}`",
            "- Status: `NO_EXTRA_F2_THEOREM_CONDITIONAL_FIRST_EM_DD_PROXY_BOUND_READY`",
            "- Main theorem:",
            "  ordinary symmetry allows `lambda(Phi)F_Q^2`; zero needs parent visible-operator-domain image, no hidden/readout Hom, same-current owner, and radiative/readout closure.",
            "- Finite branch:",
            "  `b_alpha_X=2 z_g-s_XF2`, so `|s_XF2| <= |b_alpha_X|+2|z_g|` with no cancellation credit.",
            "- First EM/DD proxy comparator:",
            f"  `|C_alpha_EM| <= {c_alpha_bound():.12e}` in the single-channel DD proxy route, nonclaim until parent map closes.",
            "- Poynting:",
            "  stationary closed worldtube gives conditional zero; general branch keeps `|Phi_EM_rad| <= |dU_EM/dt|+|W_matter|`.",
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
    gate: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    poynting: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": timestamp})

    add("VAL3994_00_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3994_01_needles_found", all(row["needle_found"] for row in sources), "every cited source needle found")
    add("VAL3994_02_countermodel", any(row["theorem_id"] == "F2G3994_0_ord_symmetry_countermodel" for row in theorem), "ordinary-symmetry countermodel row present")
    add("VAL3994_03_zero_theorem", any(row["theorem_id"] == "F2G3994_1_no_extra_F2_zero" for row in theorem), "no-extra-F2 zero theorem row present")
    add("VAL3994_04_identity", any(row["theorem_id"] == "F2G3994_2_canonical_identity" for row in theorem), "canonical identity row present")
    add("VAL3994_05_gate_rows", len(gate) >= 5, "operator-domain gate rows present")
    add("VAL3994_06_bound_rows", len(bounds) >= 5, "finite EM/DD bound rows present")
    add("VAL3994_07_calpha_bound_positive", c_alpha_bound() > 0 and math.isfinite(c_alpha_bound()), "C_alpha_EM proxy bound finite positive")
    add("VAL3994_08_poynting_rows", len(poynting) >= 3, "Poynting zero-or-bound rows present")
    zero = next(row for row in results if row["case_id"] == "CASE3994_0_no_extra_F2_zero")
    calpha = next(row for row in results if row["case_id"] == "CASE3994_1_C_alpha_at_DD_proxy_bound")
    smoke = next(row for row in results if row["case_id"] == "CASE3994_2_small_joint_F2_smoke")
    missing = next(row for row in results if row["case_id"] == "CASE3994_3_missing_zg_alpha")
    flux = next(row for row in results if row["case_id"] == "CASE3994_4_Poynting_flux_open")
    add("VAL3994_09_zero_case", float(zero["eta_EM_proxy_abs"]) == 0.0 and str(zero["passes_DD_proxy"]).lower() == "true", "zero case evaluates to zero")
    add("VAL3994_10_calpha_case", str(calpha["passes_DD_proxy"]).lower() == "true" and str(calpha["valid_for_claim"]).lower() == "false", "C_alpha proxy case passes nonclaim")
    add("VAL3994_11_smoke_case", str(smoke["passes_DD_proxy"]).lower() == "true" and str(smoke["valid_for_claim"]).lower() == "false", "small joint smoke passes nonclaim")
    add("VAL3994_12_missing_blocks", missing["eta_EM_proxy_abs"] == "MISSING" and str(missing["passes_DD_proxy"]).lower() == "false", "missing alpha/F2/current rows block")
    add("VAL3994_13_flux_blocks", flux["eta_EM_proxy_abs"] == "MISSING" and str(flux["passes_DD_proxy"]).lower() == "false", "open Poynting flux branch blocks")
    add("VAL3994_14_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL3994_15_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL3994_16_doc_exists", DOC_PATH.exists() and "b_alpha_X = 2 z_g - s_XF2" in read_text(DOC_PATH), "document written")
    add("VAL3994_17_spine_updated", SPINE_PATH.exists() and "## 3994 - No-Extra-F2 EM Gate" in read_text(SPINE_PATH), "spine updated")
    add("VAL3994_18_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL3994_19_compile", compile_ok, "script compiles")
    add("VAL3994_20_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL3994_21_status_exists", OUTPUTS["status"].exists(), "status file exists")
    add("VAL3994_22_results_nonclaim", not any(str(row["valid_for_claim"]).lower() == "true" for row in results), "all evaluator results remain nonclaim")
    return rows


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    gate = gate_rows(timestamp)
    bounds = bound_rows(timestamp)
    poynting = poynting_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decision = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["poynting"], poynting)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["claim_gate"], claim_gate)
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

    validation = build_validation_rows(timestamp, sources, theorem, gate, bounds, poynting, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)

    failed = [row for row in validation if str(row["passed"]).lower() != "true"]
    print(f"3994 validation: {len(validation) - len(failed)}/{len(validation)} passed")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
