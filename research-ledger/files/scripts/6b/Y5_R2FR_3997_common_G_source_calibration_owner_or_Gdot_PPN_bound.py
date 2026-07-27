from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3997"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3997-Y5-R2FR-common-G-source-calibration-owner-or-Gdot-PPN-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3997_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3997_COMMON_G_CALIBRATION_THEOREM.csv",
    "newton": SRC / "P8_Y5_R2FR_3997_G_PRODUCT_AND_NEWTON_MAP.csv",
    "bounds": SRC / "P8_Y5_R2FR_3997_GDOT_PPN_BOUND_VECTOR.csv",
    "cases": SRC / "P8_Y5_R2FR_3997_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_3997_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_3997_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3997_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3997_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3997_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3997_VALIDATION.csv",
}

NEXT_DOC = "3998-Y5-R2FR-Hilbert-mass-projector-and-GM-source-denominator-lock.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3998_Hilbert_mass_projector_and_GM_source_denominator_lock.py"


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
        ("SRC3997_00_3996_next", SRC / "P8_Y5_R2FR_3996_NEXT_TARGET.csv", "NEXT3996_0", "3996 handoff"),
        ("SRC3997_01_3996_common", SRC / "P8_Y5_R2FR_3996_PREVARIATION_SOURCE_SLOT_EXCLUSION_THEOREM.csv", "PSS3996_1_common_scalar_reclassification", "common scalar split"),
        ("SRC3997_02_3996_product", SRC / "P8_Y5_R2FR_3996_BALPHA_SOURCE_PRODUCT_VECTOR.csv", "BSP3996_3_common_scalar_branch", "common scalar branch"),
        ("SRC3997_03_3879_common", SRC / "P8_Y5_R2FR_3879_COMMON_GN_CALIBRATION_THEOREM.csv", "CGT3879_1_anchor_calibration", "anchor calibration identity"),
        ("SRC3997_04_3879_const", SRC / "P8_Y5_R2FR_3879_COMMON_GN_CALIBRATION_THEOREM.csv", "CGT3879_2_local_constancy", "local constancy theorem"),
        ("SRC3997_05_3879_newton", SRC / "P8_Y5_R2FR_3879_NEWTON_POISSON_COMMON_TAIL_CHAIN.csv", "NPC3879_2_weak_field", "Newton weak-field algebra"),
        ("SRC3997_06_3880_silence", SRC / "P8_Y5_R2FR_3880_GEFF_DERIVATIVE_SILENCE_THEOREM.csv", "GST3880_0_target", "G derivative silence"),
        ("SRC3997_07_3880_bianchi", SRC / "P8_Y5_R2FR_3880_GEFF_DERIVATIVE_SILENCE_THEOREM.csv", "GST3880_3_Bianchi_guard", "Bianchi guard"),
        ("SRC3997_08_3881_gdot", SRC / "P8_Y5_R2FR_3881_GDOT_FALLBACK_BOUND_ROWS.csv", "GDOT3881_1_fallback_absolute_sum", "Gdot fallback bound"),
        ("SRC3997_09_3882_map", SRC / "P8_Y5_R2FR_3882_LOCAL_NEWTON_GR_REDUCTION_MAP.csv", "RED3882_1_Newton_Poisson", "local Newton map"),
        ("SRC3997_10_3511_kappa", SRC / "P8_Y5_R2FR_3511_KAPPA_GREF_ACTION_LINE_LOCK_THEOREM.csv", "KGL3511_6_verdict", "kappa/G product lock"),
        ("SRC3997_11_3530_contract", SRC / "P8_Y5_R2FR_3530_KAPPA_G_CONTRACT.csv", "KG3530_2_calibrated_GN", "calibrated G contract"),
        ("SRC3997_12_3963_identity", SRC / "P8_Y5_R2FR_3963_NEWTON_G_PRODUCT_IDENTITY.csv", "NGI3963_2_log_derivative", "Newton product log derivative"),
        ("SRC3997_13_3963_vector", SRC / "P8_Y5_R2FR_3963_NEWTON_SOURCE_RESIDUAL_VECTOR.csv", "NSV3963_0_time", "Newton source residual vector"),
        ("SRC3997_14_3967_ppn", SRC / "P8_Y5_R2FR_3967_PPN_RESIDUAL_VECTOR.csv", "DPPN3967_14_total_abs", "PPN residual vector"),
        ("SRC3997_15_3902_gdot", SRC / "P8_Y5_R2FR_3902_GDOT_STATIONARY_CALIBRATION_GATE.csv", "GD3902_2_bound", "Gdot executable bound"),
        ("SRC3997_16_3911_numeric", SRC / "P8_Y5_R2FR_3911_FIRST_GDOT_NUMERIC_NONCLAIM_ROW.csv", "GDN3911_1_acceptance_budget", "Gdot numeric target"),
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


def gdot_bound() -> float:
    rows = read_csv(SRC / "P8_Y5_R2FR_3881_GDOT_FALLBACK_BOUND_ROWS.csv")
    for row in rows:
        if row.get("gdot_id") == "GDOT3881_1_fallback_absolute_sum":
            return float(row["bound_or_budget"])
    raise RuntimeError("GDOT3881 fallback bound missing")


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CG3997_0_anchor_policy",
            "claim_piece": "GR-style common calibration",
            "mathematical_form": "Choose one local calibration event p0 and define G0 := G_ref C_*(p0), kappa0 := 8*pi*G0/c^4.",
            "derived_result": "MTS does not need to derive the decimal SI value of G to reduce to GR/Newton; it must use one universal coupling product consistently",
            "status": "EXACT_CALIBRATION_IDENTITY_NO_ABSOLUTE_G_CLAIM",
            "source_path": str(SRC / "P8_Y5_R2FR_3879_COMMON_GN_CALIBRATION_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CG3997_1_local_constancy",
            "claim_piece": "common coupling derivative silence",
            "mathematical_form": "If G_ref and C_* are parent-owned/superselected/q-global and D ln C_*=0 in time, radius, range, frame, and domain on the branch, then G_eff=G0 locally.",
            "derived_result": "a common scalar becomes harmless local Newton calibration only when derivative-silent",
            "status": "EXACT_CONDITIONAL_ZERO_THEOREM_NOT_PARENT_SIGNED",
            "source_path": str(SRC / "P8_Y5_R2FR_3880_GEFF_DERIVATIVE_SILENCE_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CG3997_2_Newton_Poisson",
            "claim_piece": "Newtonian coefficient recovery",
            "mathematical_form": "With EH coefficient kappa0 and same Hilbert source T00=rho_H c^2, the weak-field 00 equation gives nabla^2 Phi = 4*pi*G0*rho_H.",
            "derived_result": "Newton's law coefficient follows algebraically after common coupling and Hilbert source are locked",
            "status": "EXACT_CONDITIONAL_WEAK_FIELD_DERIVATION",
            "source_path": str(SRC / "P8_Y5_R2FR_3879_NEWTON_POISSON_COMMON_TAIL_CHAIN.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CG3997_3_Bianchi_guard",
            "claim_piece": "no variable-kappa smuggling",
            "mathematical_form": "If kappa_eff varies in the field equations, Bianchi identities require compensating source-exchange terms; variation cannot be hidden inside calibration.",
            "derived_result": "common G drift must be zero by theorem or bounded as a real exchange/source residual",
            "status": "NO_SMUGGLING_GUARD",
            "source_path": str(SRC / "P8_Y5_R2FR_3880_GEFF_DERIVATIVE_SILENCE_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CG3997_4_PPN_scope",
            "claim_piece": "Newton is not full local GR",
            "mathematical_form": "Fixing first-order G0/U does not prove gamma=1, beta=1, alpha_i=0, xi=0, or zeta_i=0.",
            "derived_result": "PPN vector remains separate after Newton/G calibration",
            "status": "PPN_SCOPE_GUARD",
            "source_path": str(SRC / "P8_Y5_R2FR_3967_PPN_RESIDUAL_VECTOR.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def newton_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "map_id": "GN3997_0_product",
            "target": "G_eff product",
            "formula": "D_X ln G_eff = D_X ln G_ref + D_X ln C_* + D_X ln w_common + D_X ln ell_J + D_X ln R_frame + retained_source_terms",
            "meaning": "Newton/source tests see the product, not a naked kappa or naked matter prefactor",
            "status": "EXACT_LOG_PRODUCT_IDENTITY",
            "source_path": str(SRC / "P8_Y5_R2FR_3511_KAPPA_GREF_ACTION_LINE_LOCK_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "map_id": "GN3997_1_calibrated_branch",
            "target": "G0",
            "formula": "G0 := G_ref C_*(p0); kappa0=8*pi*G0/c^4",
            "meaning": "one measured constant is allowed as local branch calibration after anti-circular source-mass guard",
            "status": "CALIBRATION_ALLOWED_NO_DECIMAL_G_CLAIM",
            "source_path": str(SRC / "P8_Y5_R2FR_3530_KAPPA_G_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "map_id": "GN3997_2_Poisson",
            "target": "Newtonian limit",
            "formula": "G00^(1)=2 nabla^2 Phi/c^2 and kappa0 T00 = 8*pi*G0 rho_H/c^2 => nabla^2 Phi=4*pi*G0 rho_H",
            "meaning": "Newtonian mechanics follows once EH left side and same Hilbert source denominator are locked",
            "status": "EXACT_CONDITIONAL_ALGEBRA",
            "source_path": str(SRC / "P8_Y5_R2FR_3882_LOCAL_NEWTON_GR_REDUCTION_MAP.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "map_id": "GN3997_3_GM_guard",
            "target": "orbital GM",
            "formula": "mu_obs=G_eff M_eff(1+epsilon_mu)",
            "meaning": "orbital GM can verify after source lock; it cannot define both G and M_H_ref before the proof",
            "status": "ANTI_CIRCULAR_GUARD",
            "source_path": str(SRC / "P8_Y5_R2FR_3963_NEWTON_G_PRODUCT_IDENTITY.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    bound = gdot_bound()
    return [
        {
            "bound_id": "GB3997_0_Gdot_zero",
            "target": "Gdot/G",
            "formula": "D_t ln G_eff=0 if common coupling is superselected/topological/q-global and source/readout products are stationary",
            "numeric_value": "0",
            "bound_value": f"{bound:.12e}",
            "units": "yr^-1",
            "status": "CONDITIONAL_ZERO_BRANCH_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "GB3997_1_Gdot_absolute_sum",
            "target": "B_Gdot_common",
            "formula": "|D_t ln G_ref|+|D_t ln C_*|+|D_t ln w_common|+|D_t ln ell_J|+|D_t ln R_frame|+|D_t ln M_eff|+|D_t epsilon_mu|+|D_t ln Z_Poisson|+|D_t ln Z_frame|",
            "numeric_value": "MISSING_COMPONENT_VECTOR",
            "bound_value": f"{bound:.12e}",
            "units": "yr^-1",
            "status": "BOUND_FORMULA_READY_COMPONENTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "GB3997_2_Newton_amplitude",
            "target": "Newton/Poisson amplitude",
            "formula": "nabla^2 Phi=4*pi*G0 rho_H + residual_GM",
            "numeric_value": "G0_CALIBRATED_BRANCH_CONSTANT",
            "bound_value": "requires Hilbert mass/source denominator lock",
            "units": "Poisson coefficient",
            "status": "AMPLITUDE_ALLOWED_BUT_SOURCE_DENOMINATOR_OPEN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "GB3997_3_PPN_fixed_U",
            "target": "PPN source vector",
            "formula": "after fixed U=G0 M_H/r, Delta_PPN_abs=sum(|delta_gamma|,|delta_beta|,|alpha_i|,|xi|,|zeta_i|)",
            "numeric_value": "SYMBOLIC_PPN_VECTOR_RETAINED",
            "bound_value": "component comparators exist for some PPN rows; no total claim",
            "units": "dimensionless PPN",
            "status": "PPN_HANDOFF_NOT_CLOSED_BY_G_CALIBRATION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    bound = gdot_bound()
    return [
        {
            "case_id": "CASE3997_0_parent_superselection_zero",
            "route": "topological_or_superselected_G",
            "dt_ln_Gref": 0.0,
            "dt_ln_Cstar": 0.0,
            "dt_ln_w_common": 0.0,
            "dt_ln_ellJ": 0.0,
            "dt_ln_Rframe": 0.0,
            "dt_ln_Meff": 0.0,
            "dt_epsilon_mu": 0.0,
            "dt_ln_Zpoisson": 0.0,
            "dt_ln_Zframe": 0.0,
            "input_status": "CONDITIONAL_ZERO_PARENT_UNSIGNED",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3997_1_constant_calibrated_G0",
            "route": "GR_style_calibrated_constant",
            "dt_ln_Gref": 0.0,
            "dt_ln_Cstar": 0.0,
            "dt_ln_w_common": 0.0,
            "dt_ln_ellJ": 0.0,
            "dt_ln_Rframe": 0.0,
            "dt_ln_Meff": 0.0,
            "dt_epsilon_mu": 0.0,
            "dt_ln_Zpoisson": 0.0,
            "dt_ln_Zframe": 0.0,
            "input_status": "CALIBRATED_CONSTANT_NOT_DECIMAL_G_CLAIM",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3997_2_half_budget_common_drift",
            "route": "finite_Gdot_smoke",
            "dt_ln_Gref": 0.0,
            "dt_ln_Cstar": 0.10 * bound,
            "dt_ln_w_common": 0.15 * bound,
            "dt_ln_ellJ": 0.10 * bound,
            "dt_ln_Rframe": 0.05 * bound,
            "dt_ln_Meff": 0.05 * bound,
            "dt_epsilon_mu": 0.05 * bound,
            "dt_ln_Zpoisson": 0.0,
            "dt_ln_Zframe": 0.0,
            "input_status": "NUMERIC_SMOKE_ONLY_NOT_EVIDENCE",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3997_3_missing_components",
            "route": "missing_Gdot_vector",
            "dt_ln_Gref": "",
            "dt_ln_Cstar": "",
            "dt_ln_w_common": "",
            "dt_ln_ellJ": "",
            "dt_ln_Rframe": "",
            "dt_ln_Meff": "",
            "dt_epsilon_mu": "",
            "dt_ln_Zpoisson": "",
            "dt_ln_Zframe": "",
            "input_status": "MISSING_GDOT_COMPONENT_VECTOR",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3997_4_oversized_common_drift",
            "route": "Gdot_guard_failure",
            "dt_ln_Gref": 0.0,
            "dt_ln_Cstar": 0.75 * bound,
            "dt_ln_w_common": 0.75 * bound,
            "dt_ln_ellJ": 0.25 * bound,
            "dt_ln_Rframe": 0.25 * bound,
            "dt_ln_Meff": 0.0,
            "dt_epsilon_mu": 0.0,
            "dt_ln_Zpoisson": 0.0,
            "dt_ln_Zframe": 0.0,
            "input_status": "OVERSIZED_GDOT_SMOKE_BLOCKS",
            "timestamp_utc": timestamp,
        },
    ]


FIELDS = [
    "dt_ln_Gref",
    "dt_ln_Cstar",
    "dt_ln_w_common",
    "dt_ln_ellJ",
    "dt_ln_Rframe",
    "dt_ln_Meff",
    "dt_epsilon_mu",
    "dt_ln_Zpoisson",
    "dt_ln_Zframe",
]


def optional_float(value: Any) -> float | None:
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING"):
        return None
    return float(text)


def evaluate_case(row: dict[str, Any]) -> dict[str, Any]:
    bound = gdot_bound()
    values = {field: optional_float(row.get(field)) for field in FIELDS}
    result: dict[str, Any] = {
        "case_id": row["case_id"],
        "route": row["route"],
        "input_status": row["input_status"],
        "Gdot_bound_yr_inv": f"{bound:.12e}",
        "B_Gdot_abs_yr_inv": "MISSING",
        "Gdot_margin": "MISSING",
        "passes_Gdot_proxy": False,
        "calibrated_constant_ok": False,
        "score_ready": False,
        "claim_allowed": False,
        "valid_for_claim": False,
    }
    if any(value is None for value in values.values()):
        return result
    total = sum(abs(value or 0.0) for value in values.values())
    result.update(
        {
            "B_Gdot_abs_yr_inv": f"{total:.12e}",
            "Gdot_margin": f"{bound - total:.12e}",
            "passes_Gdot_proxy": total <= bound * (1.0 + 1.0e-12),
            "calibrated_constant_ok": total == 0.0,
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
            "decision_id": "DEC3997_0",
            "finding": "common G calibration is acceptable if it is one derivative-silent branch constant",
            "evidence": "GR-style calibration identity plus weak-field Poisson algebra",
            "limitation": "does not derive decimal G and does not close Hilbert mass/source denominator",
            "next_action": "lock M_H_ref / Hilbert mass projector so calibrated G0 multiplies the right source",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3997_1",
            "finding": "if common coupling is not derivative-silent, it becomes a Gdot/PPN/Newton residual",
            "evidence": "absolute no-cancellation Gdot vector with 9.6e-15 yr^-1 budget",
            "limitation": "prediction-side component values are not parent-sourced",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM3997_0_decimal_G",
            "claim": "MTS derives the numerical value of Newton's constant",
            "allowed": False,
            "reason": "3997 explicitly permits calibration but forbids claiming decimal G without a parent scale",
            "required_exit": "parent action scale/topological sector fixing the absolute coupling value",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3997_1_Newton_limit",
            "claim": "Newtonian mechanics is fully derived",
            "allowed": False,
            "reason": "Poisson algebra is derived conditionally, but Hilbert mass/source denominator and residual flux gates remain open",
            "required_exit": NEXT_DOC,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3997_2_local_GR",
            "claim": "local GR/PPN pass",
            "allowed": False,
            "reason": "G calibration does not close gamma, beta, preferred-frame, xi, zeta, non-Hilbert, or readout residuals",
            "required_exit": "componentwise PPN zero/bound vector",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3997_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "prove or bound the Hilbert mass projector/source denominator so calibrated G0 multiplies M_H rather than an orbital backfilled GM",
            "success_condition": "M_H_ref is parent-owned and flux/readout stable, or Newtonian GM residual components are numeric/source-backed and nonclaim-evaluated",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMMON_G_CALIBRATION_SPLIT_AND_GDOT_BOUND_GATE",
            "headline": "absolute G value is not claimed; local Newton recovery needs one calibrated derivative-silent coupling product plus the Hilbert mass/source denominator lock",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    bound = gdot_bound()
    found = sum(bool(row["needle_found"]) for row in sources)
    lines = [
        "# 3997 - Common G Source Calibration Owner Or Gdot/PPN Bound",
        "",
        f"Timestamp: `{timestamp}`",
        "",
        "## Result",
        "",
        "This checkpoint answers the Newton-constant issue cleanly.",
        "",
        "A serious local-GR/Newton reduction does **not** need MTS to derive the decimal SI value of `G`. GR itself uses one measured coupling. What MTS must derive or bound is stricter and more useful:",
        "",
        "- the coupling is one common branch constant;",
        "- it is derivative-silent over local tests;",
        "- it multiplies the same Hilbert source denominator;",
        "- it is not secretly backfilled from orbital `GM`.",
        "",
        "## Calibration Law",
        "",
        "`G0 := G_ref C_*(p0)`, and `kappa0 := 8*pi*G0/c^4`.",
        "",
        "If `D ln C_* = 0` in time/radius/range/frame/domain and the source denominator is locked, the weak-field equation gives",
        "",
        "`nabla^2 Phi = 4*pi*G0 rho_H`.",
        "",
        "That is the right comparison with GR: derive the reduction and constancy, not pretend the numerical value appears from nowhere.",
        "",
        "## Bound Branch",
        "",
        "If derivative silence is not proved, the retained absolute-sum budget is",
        "",
        "`B_Gdot = |D_t ln G_ref|+|D_t ln C_*|+|D_t ln w_common|+|D_t ln ell_J|+|D_t ln R_frame|+|D_t ln M_eff|+|D_t epsilon_mu|+|D_t ln Z_Poisson|+|D_t ln Z_frame|`.",
        "",
        f"The current nonclaim comparator budget is `{bound:.12e} yr^-1`.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: status `{row['input_status']}`, B_Gdot `{row['B_Gdot_abs_yr_inv']}`, pass={row['passes_Gdot_proxy']}, claim={row['claim_allowed']}"
        )
    lines.extend(
        [
            "",
            "## PPN Guard",
            "",
            "First-order `G0` calibration fixes the Newtonian potential convention. It does not prove `gamma=1`, `beta=1`, preferred-frame silence, or conservation-law PPN channels. Those remain component gates.",
            "",
            "## Next Target",
            "",
            "The next obstruction is the mass/source denominator: calibrated `G0` must multiply parent-owned `M_H`, not an orbital `GM` that already absorbed the residual.",
            "",
            f"- `{NEXT_DOC}`",
            f"- `{NEXT_SCRIPT}`",
            "",
            "## Source Count",
            "",
            f"- source needles found: `{found}/{len(sources)}`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def append_spine(timestamp: str) -> None:
    marker = "## 3997 - Common G Calibration Gate"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: MTS need not derive the decimal value of Newton's constant for local-GR/Newton recovery; it must supply one calibrated/common derivative-silent coupling product.
- Derived law: `G0 := G_ref C_*(p0)`, `kappa0=8*pi*G0/c^4`, and with same Hilbert source `nabla^2 Phi=4*pi*G0 rho_H`.
- Bound branch: if derivative silence fails, score the absolute `Gdot` product vector against the `9.6e-15 yr^-1` budget without cancellation.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    newton: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    source_paths = [Path(row["path"]) for row in sources]
    add("VAL3997_00_sources_exist", all(path.exists() for path in source_paths), "every cited source path exists")
    add("VAL3997_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL3997_02_anchor_policy", any(row["theorem_id"] == "CG3997_0_anchor_policy" for row in theorem), "anchor calibration theorem row present")
    add("VAL3997_03_constancy", any(row["theorem_id"] == "CG3997_1_local_constancy" for row in theorem), "local constancy row present")
    add("VAL3997_04_newton_theorem", any(row["theorem_id"] == "CG3997_2_Newton_Poisson" for row in theorem), "Newton Poisson theorem row present")
    add("VAL3997_05_bianchi_guard", any(row["theorem_id"] == "CG3997_3_Bianchi_guard" for row in theorem), "Bianchi guard row present")
    add("VAL3997_06_newton_map", len(newton) >= 4 and any(row["map_id"] == "GN3997_2_Poisson" for row in newton), "Newton map rows present")
    add("VAL3997_07_gdot_bound", any(row["bound_id"] == "GB3997_1_Gdot_absolute_sum" for row in bounds), "Gdot absolute-sum bound row present")
    add("VAL3997_08_ppn_guard", any(row["bound_id"] == "GB3997_3_PPN_fixed_U" for row in bounds), "PPN guard row present")
    zero = next(row for row in results if row["case_id"] == "CASE3997_0_parent_superselection_zero")
    cal = next(row for row in results if row["case_id"] == "CASE3997_1_constant_calibrated_G0")
    half = next(row for row in results if row["case_id"] == "CASE3997_2_half_budget_common_drift")
    missing = next(row for row in results if row["case_id"] == "CASE3997_3_missing_components")
    large = next(row for row in results if row["case_id"] == "CASE3997_4_oversized_common_drift")
    add("VAL3997_09_zero_case", float(zero["B_Gdot_abs_yr_inv"]) == 0.0 and str(zero["passes_Gdot_proxy"]).lower() == "true", "zero case evaluates cleanly")
    add("VAL3997_10_calibrated_case", str(cal["calibrated_constant_ok"]).lower() == "true" and str(cal["valid_for_claim"]).lower() == "false", "calibrated constant case nonclaim")
    add("VAL3997_11_half_budget_case", str(half["passes_Gdot_proxy"]).lower() == "true" and str(half["valid_for_claim"]).lower() == "false", "half budget smoke passes nonclaim")
    add("VAL3997_12_missing_blocks", missing["B_Gdot_abs_yr_inv"] == "MISSING" and str(missing["passes_Gdot_proxy"]).lower() == "false", "missing component branch blocks")
    add("VAL3997_13_large_fails", str(large["passes_Gdot_proxy"]).lower() == "false", "oversized drift fails")
    add("VAL3997_14_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL3997_15_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL3997_16_doc_exists", DOC_PATH.exists() and "Newton-constant issue" in read_text(DOC_PATH), "document written")
    add("VAL3997_17_spine_updated", SPINE_PATH.exists() and "## 3997 - Common G Calibration Gate" in read_text(SPINE_PATH), "spine updated")
    add("VAL3997_18_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL3997_19_compile", compile_ok, "script compiles")
    add("VAL3997_20_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL3997_21_status_exists", OUTPUTS["status"].exists(), "status file exists")
    add("VAL3997_22_results_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for row in results), "all evaluator results remain nonclaim")
    add("VAL3997_23_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL3997_24_no_decimal_G_claim", DOC_PATH.exists() and "derive the decimal SI value" in read_text(DOC_PATH), "no absolute G overclaim recorded")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    newton = newton_rows(timestamp)
    bounds = bound_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["newton"], newton)
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

    validation = build_validation_rows(timestamp, sources, theorem, newton, bounds, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"3997 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
