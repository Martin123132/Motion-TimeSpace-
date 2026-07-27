from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3908"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3908-Y5-R2FR-measured-Gstar-derivative-zero-gates-or-bound-runner.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3908_SOURCE_REGISTER.csv",
    "zero_routes": SRC / "P8_Y5_R2FR_3908_GSTAR_DERIVATIVE_ZERO_ROUTE_MATRIX.csv",
    "bound_runner": SRC / "P8_Y5_R2FR_3908_GSTAR_DERIVATIVE_BOUND_RUNNER.csv",
    "budgets": SRC / "P8_Y5_R2FR_3908_OBSERVABLE_BUDGET_TARGETS.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3908_LOCAL_GR_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3908_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3908_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3908_VALIDATION.csv",
}

ABS_SUM = "total_residual <= sum_i |component_i|; no fitted cancellation is credited unless a parent identity is signed"
GDOT_BOUND = "B_Gdot = |d_t ln C_*| + |d_t ln M_eff| + |d_t epsilon_mu/(1+epsilon_mu)| + |d_t ln Z_Poisson| + |d_t ln Z_frame| <= 9.6e-15 yr^-1"
WEP_BOUND = "B_WEP = |Delta_AB ln kappa_eff| + |Delta_AB ln Xi| + |Delta_AB ln Z_frame| + |Delta_AB exchange| <= 2.8e-15"
RANGE_BOUND = "B_R10(lambda) = alpha_predicted(lambda) <= alpha_bound(lambda) with sourced full-curve/arena projection rows"
PRODUCT_BOUND = "B_product = |z_G| + |z_w| + |z_ellJ| + |z_Rframe| + |z_extra| + |epsilon_Gref_match|"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    return str(path.relative_to(PCW)) if path.is_relative_to(PCW) else str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
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
        ("SRC3908_00_next", SRC / "P8_Y5_R2FR_3907_NEXT_TARGET.csv", "NEXT3907_0", "3907 selected derivative gate target"),
        ("SRC3908_01_policy", SRC / "P8_Y5_R2FR_3907_MEASURED_COUPLING_POLICY_RUNNER.csv", "POL3907_1_derivatives", "measured Gstar derivative policy"),
        ("SRC3908_02_gates", SRC / "P8_Y5_R2FR_3907_GSTAR_DERIVATIVE_ZERO_GATES.csv", "DG3907_5_product", "3907 derivative gates"),
        ("SRC3908_03_residuals", SRC / "P8_Y5_R2FR_3906_NON_EH_AND_GSTAR_RESIDUAL_ROWS.csv", "RES3906_6_exchange", "3906 residual vector"),
        ("SRC3908_04_silence", SRC / "P8_Y5_R2FR_3880_GEFF_DERIVATIVE_SILENCE_THEOREM.csv", "GST3880_5_verdict", "Geff derivative silence theorem"),
        ("SRC3908_05_gdot_fallback", SRC / "P8_Y5_R2FR_3881_GDOT_FALLBACK_BOUND_ROWS.csv", "GDOT3881_1_fallback_absolute_sum", "Gdot fallback absolute-sum bound"),
        ("SRC3908_06_gdot_eval", SRC / "P8_Y5_R2FR_3758_GDOT_BOUND_EVALUATION.csv", "GB3758_2_max_allowed_residual", "Gdot numeric target"),
        ("SRC3908_07_wep_eval", SRC / "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv", "WB3759_2_max_allowed_residual", "WEP/source coupling target"),
        ("SRC3908_08_rrf_locks", SRC / "P8_Y5_R2FR_3762_RANGE_RADIAL_FRAME_LOCKS.csv", "RRF3762_4_single_observed_frame", "range/radial/frame lock theorem routes"),
        ("SRC3908_09_rrf_budget", SRC / "P8_Y5_R2FR_3762_RANGE_RADIAL_FRAME_RESIDUAL_BUDGET.csv", "RRF_BUD3762_2_frame_split", "range/radial/frame residual budgets"),
        ("SRC3908_10_frame", SRC / "P8_Y5_R2FR_3764_FRAME_SOURCE_DESCENT_MATRIX.csv", "FSM3764_2_frame", "frame source descent matrix"),
        ("SRC3908_11_product_theorem", SRC / "P8_Y5_R2FR_3600_GEFF_PRODUCT_LOCK_THEOREM.csv", "GPL3600_8_conditional_product_lock_theorem", "G_eff product lock theorem"),
        ("SRC3908_12_product_bounds", SRC / "P8_Y5_R2FR_3600_GEFF_PRODUCT_BOUND_ROWS.csv", "GPB3600_11_product_lock_total", "G_eff product bound rows"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": found,
                "role": role,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def zero_route_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "ZR3908_0_time",
            "symbol": "dln_Gstar_dt",
            "zero_route": "G_* is a global/topological zero-form or q-global constant with no local time label",
            "source_theorem": "GST3880_0_target; GDOT3881_0_conditional_zero",
            "fallback_formula": GDOT_BOUND,
            "status": "ZERO_CONDITIONAL_BOUND_ROUTE_ACTIVE",
            "local_GR_effect": "blocks Gdot/clock if neither zero nor bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "ZR3908_1_radial",
            "symbol": "partial_r_ln_Gstar",
            "zero_route": "kappa/source charge/Poisson calibration/extra fields are constant outside compact source",
            "source_theorem": "RRF3762_2_no_radial_hair",
            "fallback_formula": "|partial_r ln kappa_eff| + |partial_r ln C_M| + |partial_r ln Z_Poisson| + |partial_r ln Z_extra|",
            "status": "ZERO_CONDITIONAL_PROFILE_ROUTE_ACTIVE",
            "local_GR_effect": "blocks pure inverse-square Newton/orbital branch if radial hair remains",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "ZR3908_2_species",
            "symbol": "partial_A_ln_Gstar",
            "zero_route": "source functor forgets material/species labels and universal kappa/source action is parent-owned",
            "source_theorem": "WB3759_0_conditional_zero; SC3/C5 contracts",
            "fallback_formula": WEP_BOUND,
            "status": "ZERO_CONDITIONAL_WEP_BOUND_ROUTE_ACTIVE",
            "local_GR_effect": "blocks WEP/source-universality if composition residual remains",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "ZR3908_3_range",
            "symbol": "alpha_Gstar_lambda",
            "zero_route": "no unscreened finite-range mediator outside the EH metric/coframe and same total source",
            "source_theorem": "RRF3762_0_no_range_mediator",
            "fallback_formula": RANGE_BOUND,
            "status": "ZERO_CONDITIONAL_R10_CURVE_ROUTE_ACTIVE",
            "local_GR_effect": "blocks inverse-square/local-GR branch if finite-range source coupling survives",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "ZR3908_4_frame",
            "symbol": "partial_frame_ln_Gstar",
            "zero_route": "same observed coframe/tau/source/orbit/clock branch is fixed before readout",
            "source_theorem": "RRF3762_4_single_observed_frame; FSM3764_2_frame",
            "fallback_formula": "|delta_clock_frame| + |delta_light_cone| + |delta_source_frame| + |delta_preferred_frame|",
            "status": "ZERO_CONDITIONAL_FRAME_BOUND_ROUTE_ACTIVE",
            "local_GR_effect": "blocks PPN/clock/orbital single-frame claims if frame drift remains",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "ZR3908_5_product",
            "symbol": "Dln_Z_product",
            "zero_route": "z_G=z_w=z_ellJ=z_Rframe=z_extra=0 independently or by parent identity",
            "source_theorem": "GPL3600_1_product_identity; GPL3600_8_conditional_product_lock_theorem",
            "fallback_formula": PRODUCT_BOUND,
            "status": "ZERO_CONDITIONAL_PRODUCT_BOUND_ROUTE_ACTIVE",
            "local_GR_effect": "blocks measured-coupling silence if product factors are unowned",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_runner_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3908_0_absolute_sum",
            "observable": "all derivative gates",
            "formula": ABS_SUM,
            "required_inputs": "component theorem-zero flags or source-backed numeric bounds",
            "runner_status": "EXECUTABLE_FORMULA_READY_INPUTS_MISSING",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "runner_id": "RUN3908_1_Gdot",
            "observable": "Gdot_over_G",
            "formula": GDOT_BOUND,
            "required_inputs": "d_t ln C_*, d_t ln M_eff, d_t epsilon_mu, d_t ln Z_Poisson, d_t ln Z_frame",
            "runner_status": "BOUND_READY_NUMERIC_COMPONENTS_MISSING",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "runner_id": "RUN3908_2_WEP",
            "observable": "eta_source_AB",
            "formula": WEP_BOUND,
            "required_inputs": "Delta_AB ln kappa_eff, Delta_AB ln Xi, Delta_AB ln Z_frame, Delta_AB exchange",
            "runner_status": "BOUND_READY_NUMERIC_COMPONENTS_MISSING",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "runner_id": "RUN3908_3_R10",
            "observable": "alpha(lambda)",
            "formula": RANGE_BOUND,
            "required_inputs": "source-backed alpha_predicted(lambda), lambda rows, real alpha_bound(lambda), projection provenance",
            "runner_status": "BOUND_CURVE_READY_PROJECTION_INPUTS_MISSING",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "runner_id": "RUN3908_4_radial_frame_product",
            "observable": "radial/frame/product residual vector",
            "formula": "|partial_r ln mu_obs| + |delta_frame_source| + " + PRODUCT_BOUND,
            "required_inputs": "radial profile, frame split, z_G/z_w/z_ellJ/z_Rframe/z_extra, Gref match",
            "runner_status": "VECTOR_BOUND_READY_INPUTS_MISSING",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def budget_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "budget_id": "BUD3908_0_Gdot",
            "observable": "Gdot_over_G",
            "target_or_bound": "9.6e-15",
            "units": "yr^-1",
            "source_basis": "GB3758_2_max_allowed_residual; GDOT3881 fallback",
            "acceptance_rule": "absolute component sum <= bound and all components sourced or theorem-zero",
            "status": "TARGET_READY_COMPONENTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "budget_id": "BUD3908_1_WEP",
            "observable": "eta_source_AB",
            "target_or_bound": "2.8e-15",
            "units": "dimensionless",
            "source_basis": "WB3759_2_max_allowed_residual",
            "acceptance_rule": "composition residual absolute sum <= bound and source material mapping exists",
            "status": "TARGET_READY_COMPONENTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "budget_id": "BUD3908_2_R10",
            "observable": "alpha(lambda)",
            "target_or_bound": "alpha_bound(lambda)",
            "units": "dimensionless curve",
            "source_basis": "RRF3762_1_alpha_curve_fallback",
            "acceptance_rule": "each alpha_predicted(lambda) row <= real sourced bound row without placeholder coefficients",
            "status": "CURVE_TARGET_READY_PROJECTION_ROWS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "budget_id": "BUD3908_3_frame",
            "observable": "delta_frame_source",
            "target_or_bound": "PPN/clock/orbital row locks",
            "units": "dimensionless or arena-specific",
            "source_basis": "RRF_BUD3762_2_frame_split; FSM3764_2_frame",
            "acceptance_rule": "single-frame theorem signed or every frame component has arena bound",
            "status": "TARGET_INTERFACE_READY_COMPONENTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "budget_id": "BUD3908_4_product",
            "observable": "Dln_Z_product",
            "target_or_bound": "zero or arena budget inherited from Gdot/WEP/R10/PPN",
            "units": "per-channel derivative units",
            "source_basis": "GPB3600_11_product_lock_total",
            "acceptance_rule": "every product factor independently zero-owned or numerically bounded; no cancellation",
            "status": "TARGET_INTERFACE_READY_COMPONENTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3908_0_zero_route",
            "gate": "all derivative zero routes parent-signed",
            "result": "not currently true; routes are conditional",
            "status": "BLOCKED_PARENT_SIGNATURES",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3908_1_bound_route",
            "gate": "fallback numeric bound route",
            "result": "formulas exist, but component values/provenance are missing",
            "status": "BLOCKED_NUMERIC_COMPONENTS",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3908_2_measured_G_policy",
            "gate": "measured G_* allowed",
            "result": "allowed only if derivative/source/range gates pass",
            "status": "POLICY_READY_NOT_CLAIM_READY",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3908_3_local_GR_Newton",
            "gate": "local GR/Newton promotion",
            "result": "blocked until zero or bound route closes for all six derivative gates",
            "status": "BLOCKED_NO_CLAIM",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3908_0",
            "target_checkpoint": "3909-Y5-R2FR-first-measured-Gstar-component-fill-Gdot-or-WEP.md",
            "script": "scripts/Y5_R2FR_3909_first_measured_Gstar_component_fill_Gdot_or_WEP.py",
            "objective": "fill the first real measured-Gstar component branch: either Gdot component rows from stationary/topological zero-form route, or WEP/source-species rows from source-label forgetting",
            "why_next": "3908 makes the derivative gates executable; the next real move is to close one component family rather than keep broad matrices open",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_MEASURED_GSTAR_DERIVATIVE_GATE_RUNNER_BUILT",
            "claim": "NO_LOCAL_GR_CLAIM",
            "summary": "six derivative gates for measured Gstar are now routed through zero theorems or explicit bound formulas; all remain nonclaim until parent signatures or numeric components close",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    zero_routes: list[dict[str, Any]],
    bound_runner: list[dict[str, Any]],
    budgets: list[dict[str, Any]],
    claim_gate: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    timestamp: str,
) -> None:
    doc = f"""# 3908 - Measured Gstar Derivative Zero Gates or Bound Runner

Generated: `{timestamp}`

## Result

3908 turns the measured-`G_*` policy into an executable derivative gate.

No-cancellation rule:

`{ABS_SUM}`

Core bound branches:

- `{GDOT_BOUND}`
- `{WEP_BOUND}`
- `{RANGE_BOUND}`
- `{PRODUCT_BOUND}`

Verdict: measured `G_*` is acceptable only if every derivative/source/range gate is theorem-zero or bounded. Current state is not claim-ready, but it is now scoreable: time, radial, species, range, frame and product-factor residuals have explicit zero routes and fallback formulas.

## Gstar Derivative Zero Route Matrix

{markdown_table(zero_routes, ["gate_id", "symbol", "zero_route", "source_theorem", "fallback_formula", "status"])}

## Gstar Derivative Bound Runner

{markdown_table(bound_runner, ["runner_id", "observable", "formula", "required_inputs", "runner_status"])}

## Observable Budget Targets

{markdown_table(budgets, ["budget_id", "observable", "target_or_bound", "units", "acceptance_rule", "status"])}

## Local-GR Claim Gate

{markdown_table(claim_gate, ["gate_id", "gate", "result", "status", "claim_allowed"])}

## Source Register

Resolved `{sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is the practical local-test interface for a measured `G_*` branch:

1. If all derivative gates are parent-zero, local `G_*` is clean.
2. If not, the gates become quantitative residual rows.
3. No local-GR/Newton claim is allowed until either route closes.

The next best move is not another broad audit. It is to close one component family first: `Gdot` or WEP/source-species.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3908 MEASURED GSTAR DERIVATIVE GATES -->
## 3908 Measured Gstar Derivative Gates

Timestamp: `{timestamp}`

No-cancellation rule:
`{ABS_SUM}`

Gdot:
`{GDOT_BOUND}`

WEP/source:
`{WEP_BOUND}`

Range:
`{RANGE_BOUND}`

Product:
`{PRODUCT_BOUND}`

Decision: measured `G_*` remains viable, but local GR/Newton is blocked until all derivative gates are theorem-zero or bounded.
<!-- END 3908 MEASURED GSTAR DERIVATIVE GATES -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3908 MEASURED GSTAR DERIVATIVE GATES -->"
    end = "<!-- END 3908 MEASURED GSTAR DERIVATIVE GATES -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    zero_routes: list[dict[str, Any]],
    bound_runner: list[dict[str, Any]],
    budgets: list[dict[str, Any]],
    claim_gate: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = [row for row in sources if row["exists"] and row["needle_found"]]
    checks.append(("VAL3908_0_sources", "all source paths and needles resolve", len(resolved) == len(sources), f"{len(resolved)}/{len(sources)} sources resolved"))
    required_symbols = {"dln_Gstar_dt", "partial_r_ln_Gstar", "partial_A_ln_Gstar", "alpha_Gstar_lambda", "partial_frame_ln_Gstar", "Dln_Z_product"}
    checks.append(("VAL3908_1_zero_routes", "zero-route matrix covers all six gates", required_symbols.issubset({str(row["symbol"]) for row in zero_routes}), f"{len(zero_routes)} rows"))
    required_runners = {"RUN3908_1_Gdot", "RUN3908_2_WEP", "RUN3908_3_R10", "RUN3908_4_radial_frame_product"}
    checks.append(("VAL3908_2_runner", "bound runner covers major observable families", required_runners.issubset({str(row["runner_id"]) for row in bound_runner}), f"{len(bound_runner)} rows"))
    required_budgets = {"Gdot_over_G", "eta_source_AB", "alpha(lambda)", "delta_frame_source", "Dln_Z_product"}
    checks.append(("VAL3908_3_budgets", "observable budget targets emitted", required_budgets.issubset({str(row["observable"]) for row in budgets}), f"{len(budgets)} budgets"))
    checks.append(("VAL3908_4_no_claim", "local GR remains blocked", any(row["gate_id"] == "GATE3908_3_local_GR_Newton" and "BLOCKED" in str(row["status"]) for row in claim_gate), "GATE3908_3"))
    checks.append(("VAL3908_5_all_nonclaim", "all generated rows are nonclaim", all(str(row.get("valid_for_claim", row.get("claim_allowed", False))) == "False" for collection in [zero_routes, budgets, claim_gate] for row in collection) and all(str(row.get("claim_allowed", False)) == "False" for row in bound_runner), "valid_for_claim=false"))
    checks.append(("VAL3908_6_doc", "markdown checkpoint exists with no-cancellation rule", DOC_PATH.exists() and ABS_SUM in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3908_7_spine", "spine updated with 3908 block", SPINE_PATH.exists() and "BEGIN 3908 MEASURED GSTAR DERIVATIVE GATES" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3908_8_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3908*")
            if path.is_file() and ("3908-Y5" in path.name or "P8_Y5_R2FR_3908" in path.name or "P8_Y5_BRR545_3908" in path.name)
        ]
    checks.append(("VAL3908_9_formalization_untouched", "no generated 3908 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3908_10_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3908_11_next_target", "next target fills a component family", any("first-measured-Gstar-component-fill" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3909 component fill"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    zero_routes = zero_route_rows(timestamp)
    bound_runner = bound_runner_rows(timestamp)
    budgets = budget_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["zero_routes"], zero_routes)
    write_csv(OUTPUTS["bound_runner"], bound_runner)
    write_csv(OUTPUTS["budgets"], budgets)
    write_csv(OUTPUTS["claim_gate"], claim_gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, zero_routes, bound_runner, budgets, claim_gate, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, zero_routes, bound_runner, budgets, claim_gate, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_MEASURED_GSTAR_DERIVATIVE_GATE_RUNNER_BUILT")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
