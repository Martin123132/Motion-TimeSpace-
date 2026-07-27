from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_PATH = Path(__file__)

CHECKPOINT = "4197"
BRANCH_ID = "MTS_R2FR_Y5_NORMALIZED_JRES_PROFILE_SMOKE_4197"
DECISION = (
    "NORMALIZED_JRES_SMOKE_FINDS_STRONG_LOCAL_WINDOW_PLAUSIBLE_ONLY_WITH_SMALL_AMPLITUDE_OR_"
    "RELAXATION_PRODUCT_WEAK_LOCAL_WINDOW_HARD_NONCLAIM"
)
DOC_PATH = POST / "4197-Y5-R2FR-normalized-Jres-profile-smoke-with-4194-budgets.md"
FORMAL_PATH = FORMAL / "213-PPC4161-normalized-Jres-profile-smoke.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-038"
SPINE_MARKER = "PPC4161_NORMALIZED_JRES_PROFILE_SMOKE_4197"
PACKET_MARKER = "PPC4161_PACKET_NORMALIZED_JRES_PROFILE_SMOKE_4197"
NEXT_TARGET = "4198-Y5-R2FR-parent-amplitude-owner-for-AJ-muXiTres-cGamma.md"

BUDGET_PATH = SOURCE_DIR / "P8_Y5_R2FR_4194_NORMALIZED_BUDGET_REQUIREMENTS.csv"

AJ_VALUES = [1e-6, 1e-4, 1e-2, 1e-1, 1.0, 10.0]
SCALE_VALUES = [1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0]
BOUNDARY_AJ_EQUIV_VALUES = [0.0, 1e-6, 1e-4, 1e-2, 1.0]

SOURCES = {
    "SRC4197_00_4194_formal": (
        FORMAL / "210-PPC4161-source-support-powers-for-Jres.md",
        "A_J <= 0.1678939074330212",
        "4194 formal budget reality check.",
    ),
    "SRC4197_01_4194_budget_csv": (
        BUDGET_PATH,
        "NB4194_strong_local_Gdot_cGamma_1e+00",
        "4194 machine-readable normalized budget rows.",
    ),
    "SRC4197_02_4196_formal": (
        FORMAL / "212-PPC4161-scalar-leakage-reference-nulling.md",
        "Stationary local values are not enough.",
        "4196 scalar leakage nulling result and next target.",
    ),
    "SRC4197_03_4196_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4196_NEXT_TARGET.csv",
        "A_J grid",
        "4196 machine-readable request for profile smoke inputs.",
    ),
    "SRC4197_04_4193_budget": (
        SOURCE_DIR / "P8_Y5_R2FR_4193_FINITE_PROFILE_BUDGET.csv",
        "BUD4193_SYMBOLIC_DTXI",
        "4193 finite profile budget source.",
    ),
    "SRC4197_05_4196_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4196_DECISION.csv",
        "Jres_profile_smoke_recommended_next",
        "4196 decision row pointing to this smoke.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def common() -> Dict[str, str]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def append_unique_line(path: Path, marker: str, line: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if text and not text.endswith("\n"):
            handle.write("\n")
        handle.write(line)


def append_unique_csv_row(path: Path, key_column: str, key_value: str, row: Dict[str, str]) -> None:
    rows = parse_csv(path)
    if any(existing.get(key_column) == key_value for existing in rows):
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writerow(row)


def fmt(value: float) -> str:
    return f"{value:.12g}"


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, required_text, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": required_text,
                "required_text_found": str(required_text in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def budget_import_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for budget in parse_csv(BUDGET_PATH):
        rows.append(
            {
                **common(),
                "budget_id": budget["budget_id"],
                "window": budget["window"],
                "channel": budget["channel"],
                "U_B": budget["U_B"],
                "U_B_squared": budget["U_B_squared"],
                "assumed_abs_cGamma": budget["assumed_abs_cGamma"],
                "profile_limit": budget["profile_limit"],
                "required_AJ_multiplier": budget["required_AJ_multiplier"],
                "multiplier_units": budget["multiplier_units"],
                "source_budget_path": str(BUDGET_PATH),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def assumption_grid_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for a_j in AJ_VALUES:
        for scale in SCALE_VALUES:
            for boundary in BOUNDARY_AJ_EQUIV_VALUES:
                rows.append(
                    {
                        **common(),
                        "assumption_id": f"AJ{a_j:g}_S{scale:g}_B{boundary:g}",
                        "A_J_bulk": fmt(a_j),
                        "normalized_relaxation_or_length_scale": fmt(scale),
                        "boundary_AJ_equivalent": fmt(boundary),
                        "effective_AJ": fmt(a_j + boundary),
                        "basis": "declared_assumption_grid_not_parent_sourced",
                        "claim_allowed": "False",
                        "valid_for_claim": "False",
                    }
                )
    return rows


def grid_result_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    budgets = budget_import_rows()
    for budget in budgets:
        multiplier = float(budget["required_AJ_multiplier"])
        for a_j in AJ_VALUES:
            for scale in SCALE_VALUES:
                for boundary in BOUNDARY_AJ_EQUIV_VALUES:
                    effective_aj = a_j + boundary
                    allowed_aj = multiplier * scale
                    margin = allowed_aj / effective_aj if effective_aj > 0 else float("inf")
                    rows.append(
                        {
                            **common(),
                            "result_id": f"{budget['budget_id']}_AJ{a_j:g}_S{scale:g}_B{boundary:g}",
                            "budget_id": budget["budget_id"],
                            "window": budget["window"],
                            "channel": budget["channel"],
                            "assumed_abs_cGamma": budget["assumed_abs_cGamma"],
                            "multiplier_units": budget["multiplier_units"],
                            "A_J_bulk": fmt(a_j),
                            "boundary_AJ_equivalent": fmt(boundary),
                            "effective_AJ": fmt(effective_aj),
                            "normalized_relaxation_or_length_scale": fmt(scale),
                            "allowed_AJ_for_row": fmt(allowed_aj),
                            "pass_budget": str(effective_aj <= allowed_aj),
                            "margin_allowed_over_effective": fmt(margin),
                            "claim_allowed": "False",
                            "valid_for_claim": "False",
                        }
                    )
    return rows


def required_scale_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for budget in budget_import_rows():
        multiplier = float(budget["required_AJ_multiplier"])
        for effective_aj in [1e-4, 1e-2, 1e-1, 1.0]:
            required_scale = effective_aj / multiplier
            rows.append(
                {
                    **common(),
                    "requirement_id": f"{budget['budget_id']}_EFFAJ{effective_aj:g}",
                    "budget_id": budget["budget_id"],
                    "window": budget["window"],
                    "channel": budget["channel"],
                    "assumed_abs_cGamma": budget["assumed_abs_cGamma"],
                    "effective_AJ": fmt(effective_aj),
                    "required_normalized_scale": fmt(required_scale),
                    "scale_units": budget["multiplier_units"],
                    "interpretation": "scale must be at least this large for the chosen effective_AJ to satisfy this budget row",
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
    return rows


def summary_rows(grid: List[Dict[str, str]], requirements: List[Dict[str, str]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    groups = sorted({(r["window"], r["channel"], r["assumed_abs_cGamma"]) for r in grid})
    for window, channel, c_gamma in groups:
        subset = [r for r in grid if r["window"] == window and r["channel"] == channel and r["assumed_abs_cGamma"] == c_gamma]
        passes = [r for r in subset if r["pass_budget"] == "True"]
        best_margin = max(float(r["margin_allowed_over_effective"]) for r in subset)
        hardest_req_a1 = next(
            float(r["required_normalized_scale"])
            for r in requirements
            if r["window"] == window and r["channel"] == channel and r["assumed_abs_cGamma"] == c_gamma and r["effective_AJ"] == "1"
        )
        rows.append(
            {
                **common(),
                "summary_id": f"SUM4197_{window}_{channel.replace(' ', '_')}_cGamma_{c_gamma}",
                "window": window,
                "channel": channel,
                "assumed_abs_cGamma": c_gamma,
                "grid_rows": str(len(subset)),
                "pass_rows": str(len(passes)),
                "pass_fraction": fmt(len(passes) / len(subset)),
                "best_margin_allowed_over_effective": fmt(best_margin),
                "required_scale_for_effective_AJ_1": fmt(hardest_req_a1),
                "verdict": profile_verdict(window, channel, float(c_gamma), hardest_req_a1),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def profile_verdict(window: str, channel: str, c_gamma: float, required_scale_for_a1: float) -> str:
    if channel == "D_t Xi_0":
        if window == "strong_local" and required_scale_for_a1 <= 10:
            return "plausible_if_effective_AJ_not_large_or_muXiT_res_order_10"
        if window == "strong_local":
            return "plausible_only_with_small_cGamma_or_large_muXiT_res"
        if required_scale_for_a1 <= 10:
            return "weak_window_possible_only_with_small_cGamma_or_tiny_AJ"
        return "hard_fails_generic_effective_AJ_order_1"
    if required_scale_for_a1 <= 1:
        return "gradient_budget_loose_if_length_scale_order_1"
    if required_scale_for_a1 <= 100:
        return "gradient_budget_moderate_length_scale_needed"
    return "gradient_budget_hard_if_length_scale_small"


def decision_rows(summaries: List[Dict[str, str]], requirements: List[Dict[str, str]]) -> List[Dict[str, str]]:
    strong_gdot_a1 = next(
        r for r in requirements if r["budget_id"] == "NB4194_strong_local_Gdot_cGamma_1e+00" and r["effective_AJ"] == "1"
    )
    weak_gdot_a1 = next(
        r for r in requirements if r["budget_id"] == "NB4194_weaker_local_Gdot_cGamma_1e+00" and r["effective_AJ"] == "1"
    )
    strong_grad_a1 = next(
        r for r in requirements if r["budget_id"] == "NB4194_strong_local_gradXi_cGamma_1e+00" and r["effective_AJ"] == "1"
    )
    return [
        {
            **common(),
            "decision": DECISION,
            "strong_local_cGamma1_required_muXiT_for_effective_AJ1": strong_gdot_a1["required_normalized_scale"],
            "strong_local_cGamma1_required_length_scale_for_effective_AJ1": strong_grad_a1["required_normalized_scale"],
            "weaker_local_cGamma1_required_muXiT_for_effective_AJ1": weak_gdot_a1["required_normalized_scale"],
            "dominant_channel": "D_t Xi_0 / Gdot",
            "profile_smoke_result": "strong_local_window_not_dead_if_AJ_small_or_muXiT_res_above_order_few; weak_local_window_hard_for_cGamma_order_1",
            "parent_amplitude_owner_exists": "False",
            "numeric_values_are_assumption_grid": "True",
            "public_local_GR_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "FW4197_0_grid_not_parent",
            "The grid values for A_J, mu_Xi*T_res, L_res/L_loc, c_Gamma and boundary amplitude are assumption rows, not parent derivations.",
        ),
        (
            "FW4197_1_no_local_GR_pass",
            "Passing a smoke row is not a local GR/PPN pass because parent signatures and source-backed bounds remain unsigned.",
        ),
        (
            "FW4197_2_boundary_not_free",
            "Boundary_AJ_equivalent cannot be silently set to zero in a claim; it must be derived/routed or bounded.",
        ),
        (
            "FW4197_3_weak_window_warning",
            "The weak U_B=1e-4 local window with c_Gamma order 1 is hard and cannot be advertised as plausible without tiny A_J or huge relaxation product.",
        ),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in entries
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4197 turns the symbolic branch into explicit numeric pressure. The missing object is now an amplitude owner for A_J, mu_Xi*T_res, c_Gamma, and boundary routing.",
            "route_A": "derive A_J from the parent scalar/source operator and fixed-point Hessian",
            "route_B": "derive or bound mu_Xi*T_res and c_Gamma from the Xi relaxation operator",
            "route_C": "if parent derivation stalls, choose source-backed local bound priors and keep branch as explicit phenomenological closure",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "summary": "4197 finds that the strong local window can be numerically plausible only if effective A_J is small or mu_Xi*T_res is above order few; the weak local window is hard for c_Gamma order 1; Gdot dominates.",
            "local_GR_claim": "False",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_docs(decision: Dict[str, str]) -> None:
    formal = f"""# 213 - PPC4161 Normalized Jres Profile Smoke

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint is a numeric pressure test of the clean-closure `J_res=U_B^2 A_J` branch against the 4194 local `Gdot/G` and gradient budgets. It does not prove local GR or PPN safety.

## Imported Budget Form

4194 gave:

```text
||J_res|| = U_B^2 A_J
A_J <= required_AJ_multiplier * scale
```

where the scale is either:

```text
mu_Xi T_res
```

for the `Gdot/G` channel, or:

```text
mu_Xi (L_res/L_loc)
```

for the gradient channel.

4197 adds a boundary-equivalent amplitude:

```text
A_J,eff = A_J,bulk + A_J,boundary.
```

## Key Numeric Readout

For `effective_AJ = 1` and `|c_Gamma|=1`:

```text
strong local Gdot needs     mu_Xi T_res >= {decision['strong_local_cGamma1_required_muXiT_for_effective_AJ1']}
strong local gradient needs mu_Xi L_res/L_loc >= {decision['strong_local_cGamma1_required_length_scale_for_effective_AJ1']}
weak local Gdot needs       mu_Xi T_res >= {decision['weaker_local_cGamma1_required_muXiT_for_effective_AJ1']}
```

So the hard channel is `Gdot/G`, not the gradient budget.

## Interpretation

The strong local window is not numerically dead:

```text
U_B = 3.796559535779445e-07
```

If `A_J,eff` is around `0.1`, `mu_Xi T_res` of order unity can pass the `|c_Gamma|=1` Gdot budget. If `A_J,eff` is order unity, the relaxation product must be order several.

The weak local window is hard:

```text
U_B = 1e-4
```

For `|c_Gamma|=1` and `A_J,eff=1`, the required `mu_Xi T_res` is enormous. It only becomes plausible if `A_J,eff` is tiny, `|c_Gamma|` is much smaller, or the relaxation product is very large.

## Verdict

This moves the branch from vague symbolic worry to a concrete amplitude problem:

```text
derive A_J,eff,
derive or bound mu_Xi T_res,
derive or bound c_Gamma,
derive/rout boundary_AJ.
```

No public claim is allowed from 4197 because every profile number is an assumption-grid row.

## Next Gate

`{NEXT_TARGET}` should derive the parent amplitude owner for `A_J`, `mu_Xi T_res`, `c_Gamma`, and boundary routing, or demote the branch to an explicit phenomenological local closure with source-backed priors.
"""
    checkpoint = f"""# 4197 - Y5 R2FR Normalized Jres Profile Smoke With 4194 Budgets

Decision: `{DECISION}`

## Summary

4197 runs the numeric smoke test requested by 4196.

It imports the 4194 normalized budgets and scans:

```text
A_J in {AJ_VALUES}
scale in {SCALE_VALUES}
boundary_AJ_equiv in {BOUNDARY_AJ_EQUIV_VALUES}
```

against strong/weak local windows, `|c_Gamma|` rows, `Gdot/G`, and gradient constraints.

## Main Result

The branch is not killed, but it is not free.

- Strong local window: plausible if `A_J,eff` is small or `mu_Xi T_res` is order several for `A_J,eff~1`.
- Weak local window: hard for `|c_Gamma|~1`; it needs tiny `A_J,eff`, small `|c_Gamma|`, or very large relaxation product.
- Dominant constraint: `Gdot/G`.
- No claim: all numbers are assumption-grid rows.

## Next

`{NEXT_TARGET}` should stop treating `A_J` as a mystery box and try to derive or bound it from the parent source/operator normalization.
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(checkpoint, encoding="utf-8")


def write_register_updates(decision: Dict[str, str]) -> None:
    append_unique_csv_row(
        CLAIMS_PATH,
        "claim_id",
        CLAIM_ID,
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "The normalized J_res profile smoke shows the clean-closure local branch is numerically plausible only in the strong local window with small effective A_J or relaxation product above order few; the weak local window is hard for c_Gamma order 1.",
            "current_evidence": "4197 budget import, assumption grid, grid results, requirement table, scenario summary, decision row and nonclaim firewall.",
            "status": "private_numeric_smoke_nonclaim_parent_amplitude_owner_missing",
            "next_test": "Derive or source the parent amplitude owner for A_J, mu_Xi*T_res, c_Gamma and boundary routing.",
            "key_risk": "A passing assumption-grid row could be mistaken for an empirical local-GR pass even though A_J and relaxation scales are not parent-owned.",
        },
    )
    append_unique_line(
        SPINE_PATH,
        SPINE_MARKER,
        f"""

### PPC4161 Normalized Jres Profile Smoke - 4197

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4197 runs the numeric smoke test for the clean-closure branch against the 4194 budgets. For `effective_AJ=1` and `|c_Gamma|=1`:

```text
strong local Gdot requires     mu_Xi T_res >= {decision['strong_local_cGamma1_required_muXiT_for_effective_AJ1']}
strong local gradient requires mu_Xi L_res/L_loc >= {decision['strong_local_cGamma1_required_length_scale_for_effective_AJ1']}
weak local Gdot requires       mu_Xi T_res >= {decision['weaker_local_cGamma1_required_muXiT_for_effective_AJ1']}
```

Verdict: strong local window is plausible only with small effective amplitude or relaxation product above order few; weak local window is hard for `|c_Gamma|~1`. No claim is allowed because the amplitude owner is missing.
""",
    )
    append_unique_line(
        PACKET_180_PATH,
        PACKET_MARKER,
        f"""

## PPC4161 Packet Normalized Jres Profile Smoke - 4197

Marker: `{PACKET_MARKER}`

Inside the private packet, `J_res=U_B^2 A_J` is now numerically pressure-tested. The hard constraint is the `Gdot/G` channel. Strong local suppression survives only if `A_J,eff` is small or `mu_Xi T_res` is sufficiently large; weak local suppression is hard at `|c_Gamma|=1`. The packet remains nonclaim until parent action owns `A_J`, `mu_Xi T_res`, `c_Gamma`, and boundary routing.
""",
    )


def all_rows() -> Dict[str, List[Dict[str, str]]]:
    grid = grid_result_rows()
    requirements = required_scale_rows()
    summaries = summary_rows(grid, requirements)
    decision = decision_rows(summaries, requirements)
    return {
        "P8_Y5_R2FR_4197_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4197_BUDGET_IMPORT.csv": budget_import_rows(),
        "P8_Y5_R2FR_4197_ASSUMPTION_GRID.csv": assumption_grid_rows(),
        "P8_Y5_R2FR_4197_GRID_RESULTS.csv": grid,
        "P8_Y5_R2FR_4197_REQUIRED_SCALE_TABLE.csv": requirements,
        "P8_Y5_R2FR_4197_SCENARIO_SUMMARY.csv": summaries,
        "P8_Y5_R2FR_4197_DECISION.csv": decision,
        "P8_Y5_R2FR_4197_CLAIM_FIREWALL.csv": claim_firewall_rows(),
        "P8_Y5_R2FR_4197_NEXT_TARGET.csv": next_target_rows(),
        "P8_Y5_R2FR_4197_STATUS.csv": status_rows(),
    }


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4197_SOURCE_REGISTER.csv"]
    budgets = rows_by_file["P8_Y5_R2FR_4197_BUDGET_IMPORT.csv"]
    grid = rows_by_file["P8_Y5_R2FR_4197_GRID_RESULTS.csv"]
    requirements = rows_by_file["P8_Y5_R2FR_4197_REQUIRED_SCALE_TABLE.csv"]
    summaries = rows_by_file["P8_Y5_R2FR_4197_SCENARIO_SUMMARY.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4197_DECISION.csv"][0]
    firewall = rows_by_file["P8_Y5_R2FR_4197_CLAIM_FIREWALL.csv"]
    strong_req = float(decision["strong_local_cGamma1_required_muXiT_for_effective_AJ1"])
    weak_req = float(decision["weaker_local_cGamma1_required_muXiT_for_effective_AJ1"])

    checks = [
        ("VAL4197_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4197_1_source_tokens", "all source required text markers found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4197_2_budget_import_count", "4194 budget import has 12 rows", len(budgets) == 12),
        ("VAL4197_3_grid_nonempty", "grid result table has expected rows", len(grid) == len(budgets) * len(AJ_VALUES) * len(SCALE_VALUES) * len(BOUNDARY_AJ_EQUIV_VALUES)),
        ("VAL4197_4_required_scales", "required scale table has expected rows", len(requirements) == len(budgets) * 4),
        ("VAL4197_5_summary_count", "summary has one row per budget", len(summaries) == len(budgets)),
        ("VAL4197_6_gdot_dominates", "strong Gdot A_J=1 scale is harder than strong gradient", strong_req > float(decision["strong_local_cGamma1_required_length_scale_for_effective_AJ1"])),
        ("VAL4197_7_weak_window_hard", "weak cGamma=1 A_J=1 scale is much harder than strong", weak_req > strong_req * 1000),
        ("VAL4197_8_pass_and_fail_rows", "grid contains both pass and fail rows", any(r["pass_budget"] == "True" for r in grid) and any(r["pass_budget"] == "False" for r in grid)),
        ("VAL4197_9_parent_missing", "decision records parent amplitude owner missing", decision["parent_amplitude_owner_exists"] == "False"),
        (
            "VAL4197_10_no_claim_flags",
            "no 4197 row has claim_allowed or valid_for_claim true",
            all(
                row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False"
                for table in rows_by_file.values()
                for row in table
            ),
        ),
        ("VAL4197_11_firewall_rows", "firewall has four anti-claim rules", len(firewall) == 4),
        ("VAL4197_12_docs_written", "formal and checkpoint docs contain decision", DECISION in read_text(FORMAL_PATH) and DECISION in read_text(DOC_PATH)),
        ("VAL4197_13_claim_register", "claim register has L-038", CLAIM_ID in read_text(CLAIMS_PATH)),
        ("VAL4197_14_spine_marker", "spine marker appended", SPINE_MARKER in read_text(SPINE_PATH)),
        ("VAL4197_15_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_180_PATH)),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "check": check,
            "passed": str(bool(passed)),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, check, passed in checks
    ]


def write_all() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    rows_by_file = all_rows()
    decision = rows_by_file["P8_Y5_R2FR_4197_DECISION.csv"][0]
    write_docs(decision)
    write_register_updates(decision)
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4197_VALIDATION.csv", validation)
    if not all(row["passed"] == "True" for row in validation):
        failed = [row for row in validation if row["passed"] != "True"]
        raise RuntimeError(f"4197 validation failed: {failed}")
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4197_VALIDATION.csv'}")
    print("rows=16 validation checks")


if __name__ == "__main__":
    main()
