from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4318"
CLAIM_ID = "L-159"
BRANCH = "MTS_R2FR_Y5_NONHILBERT_SUPPORT_DRIFT_HISTORY_BOUND_PRIORITIZER_4318"
DECISION = "NREST_NONEM_CANONICAL_SINGLE_COUNT_BUDGET_AND_PRIORITY_ORDER_DERIVED_NONCLAIM"
MARKER = "PPC4161_NONHILBERT_SUPPORT_DRIFT_HISTORY_BOUND_PRIORITIZER_4318"
PACKET_MARKER = "PPC4161_PACKET_NONHILBERT_SUPPORT_DRIFT_HISTORY_BOUND_PRIORITIZER_4318"
NEXT_TARGET = "4319-Y5-R2FR-nonHilbert-Hperp-source-support-zero-or-bound-row.md"

FORMAL_PATH = FORMAL / "334-PPC4161-nonHilbert-support-drift-history-bound-prioritizer.md"
DOC_PATH = POST / "4318-Y5-R2FR-nonHilbert-support-drift-history-bound-prioritizer.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4318_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4318_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4317_NEXT_TARGET.csv",
        "N_rest_nonEM",
        "4317 handoff selecting the residual non-EM budget.",
    ),
    "SRC4318_01_components": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "N_src <= ||U_B||_inf ||S_cg_nonHilbert||_{E*}",
        "4303 source-support row.",
    ),
    "SRC4318_02_drift": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "N_drift_selector <= N_drift_mL+N_drift_Lcg+N_selector",
        "4303 drift/selector row.",
    ),
    "SRC4318_03_history": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "N_history_transition <= N_history+N_transition+N_mass_current",
        "4303 history/transition row.",
    ),
    "SRC4318_04_boundary": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "N_boundary_domain <= N_no_flux+N_zero_mode+N_outer+N_history_boundary+N_domain",
        "4303 boundary/domain row.",
    ),
    "SRC4318_05_NN": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "Delta_m <= (N_J_4303+N_B_4303+N_N)/lambda_m",
        "4303 nonlinear/noise handoff row.",
    ),
    "SRC4318_06_Nrest": (
        FORMAL / "332-PPC4161-visible-Hilbert-source-silence-integration-or-nonEM-residual-budget.md",
        "N_rest_nonEM =",
        "4316 canonical residual sum before inner-charge sharpening.",
    ),
    "SRC4318_07_4317_reduction": (
        FORMAL / "333-PPC4161-nonEM-inner-charge-domain-zero-or-QmH-bound-values.md",
        "N_pair <= N_rest_nonEM",
        "4317 handoff after visible/EM/inner source reductions.",
    ),
    "SRC4318_08_standard_Nsrc": (
        FORMAL / "321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md",
        "N_src,strong_standard = 0.",
        "4305 standard Dq/Hperp-closed source-support zero branch.",
    ),
    "SRC4318_09_source_anchor": (
        FORMAL / "320-PPC4161-first-source-norms-or-visible-Hilbert-m-lock-signature.md",
        "N_src,strong <= U_B^2 A_src",
        "4304 private source-support scale anchor.",
    ),
    "SRC4318_10_collar_split": (
        FORMAL / "327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md",
        "S_U <= R_visible + R_EM_Poynting + R_transition + R_boundary + R_nonHilbert + R_N",
        "4311 collar residual split into physical rows.",
    ),
    "SRC4318_11_Hperp_bound": (
        FORMAL / "260-PPC4161-Dq-component-zero-adoption-or-Hperp-bound-input-fill.md",
        "|S_A Hperp^A| <= C_S C_perp E_Dq,H.",
        "4244 Hperp/Dq fallback bound feeding non-Hilbert source support.",
    ),
}


def base_row() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
        "claim_allowed": "False",
        "valid_for_claim": "False",
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: List[Dict[str, str]], columns: List[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(col, "")).replace("\n", "<br>").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + content.strip() + "\n")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path) if path.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr",
        (
            "4318 converts the post-4317 residual phrase N_rest_nonEM into a canonical single-count budget: "
            "N_rest_nonEM^canon = N_src_nonHilbert + N_drift_selector + N_history_transition + "
            "N_boundary_domain + N_N. This repairs the handoff convention by requiring N_N to be included "
            "exactly once; when this canonical symbol is used, Delta_m <= N_rest_nonEM^canon/lambda_m rather "
            "than adding another +N_N. It also derives the nonlinear absorption branch: if "
            "N_N <= kappa_N lambda_m Delta_m with 0<=kappa_N<1, then "
            "Delta_m <= (N_src_nonHilbert+N_drift_selector+N_history_transition+N_boundary_domain)/((1-kappa_N)lambda_m). "
            "The priority order selects N_src_nonHilbert/Hperp first because it has an existing standard zero route "
            "and a finite Dq/Hperp bound route; drift, history, boundary/domain and nonlinear rows remain explicit "
            "absolute components. No local GR/Newton claim fires."
        ),
        (
            "4318 source register, canonical N_rest budget, zero-or-bound matrix, priority order, single-count repair, "
            "runner, firewall, status, next-target and validation CSV."
        ),
        "private_Nrest_nonEM_single_count_budget_and_priority_order_nonclaim",
        (
            "Parent-sign or source-bound N_src_nonHilbert through Hperp/Dq, then repeat componentwise for drift/selector, "
            "history/transition, boundary/domain and nonlinear absorption rows."
        ),
        (
            "Double-counting N_N, cancelling residual rows against each other, claiming U_B^2 suppression in transition "
            "shells without Hperp/Dq ownership, or promoting source-pair silence to local GR/Newton while lambda, "
            "source-equality, commutator and projection gates remain open."
        ),
    ]
    with path.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, purpose) in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(needle in text),
                "purpose": purpose,
            }
        )
        rows.append(row)
    return rows


def budget_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "NR4318_0_Nsrc",
            "N_src_nonHilbert",
            "source support outside Hilbert/q-kernel branch",
            "zero if standard Dq/Hperp branch gives S_A Hperp^A=0 or projected source support vanishes",
            "N_src <= ||U_B||_inf ||S_cg_nonHilbert|| <= U_B^2 A_src_general or C_S C_perp E_Dq,H",
            "PRIORITY_1",
        ),
        (
            "NR4318_1_Ndrift",
            "N_drift_selector",
            "drift in m, L_cg or local selector",
            "zero if branch selector is fixed/q-basic and m_L/L_cg do not move under local variation",
            "N_drift_selector <= N_drift_mL + N_drift_Lcg + N_selector",
            "PRIORITY_2",
        ),
        (
            "NR4318_2_Nhistory",
            "N_history_transition",
            "history/memory/transition shell or mass-current leakage",
            "zero if local causal silence and transition-kernel membership are parent-signed",
            "N_history_transition <= N_history + N_transition + N_mass_current",
            "PRIORITY_3",
        ),
        (
            "NR4318_3_Nboundary",
            "N_boundary_domain",
            "outer/no-flux/zero-mode/history-boundary/domain-motion row",
            "zero if no-flux, zero-mode removal, fixed domain and outer boundary routing are all signed",
            "N_boundary_domain <= N_no_flux + N_zero_mode + N_outer + N_history_boundary + N_domain",
            "PRIORITY_4",
        ),
        (
            "NR4318_4_NN",
            "N_N",
            "nonlinear/noise/remainder forcing",
            "zero if nonlinear remainder vanishes; absorbable if N_N <= kappa_N lambda_m Delta_m with kappa_N<1",
            "otherwise retain N_N as a finite absolute row",
            "PRIORITY_5_DEPENDS_ON_LAMBDA",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for residual_id, symbol, meaning, zero_route, bound_route, priority in specs:
        row = base_row()
        row.update(
            {
                "residual_id": residual_id,
                "symbol": symbol,
                "meaning": meaning,
                "zero_route": zero_route,
                "bound_route": bound_route,
                "priority": priority,
                "double_count_guard": "included_once_in_N_rest_nonEM_canon",
            }
        )
        rows.append(row)
    return rows


def zero_bound_rows() -> List[Dict[str, str]]:
    specs = [
        ("ZB4318_0_Nsrc_standard", "N_src_nonHilbert", "Dq/Hperp-closed standard source branch", "N_src_nonHilbert=0", "CONDITIONAL_ZERO_ROUTE"),
        ("ZB4318_1_Nsrc_Hperp", "N_src_nonHilbert", "Hperp not zero but Dq component budget finite", "N_src_nonHilbert <= C_S C_perp E_Dq,H or U_B^2 A_src_general", "BOUND_ROUTE_READY_INPUTS_MISSING"),
        ("ZB4318_2_Ndrift_zero", "N_drift_selector", "fixed local branch and q-basic selector", "N_drift_selector=0", "CONDITIONAL_ZERO_ROUTE"),
        ("ZB4318_3_Ndrift_bound", "N_drift_selector", "m_L/L_cg/selector drift survives", "N_drift_mL + N_drift_Lcg + N_selector", "BOUND_ROUTE_REQUIRED"),
        ("ZB4318_4_Nhistory_zero", "N_history_transition", "local causal silence plus transition-kernel membership", "N_history_transition=0", "CONDITIONAL_ZERO_ROUTE"),
        ("ZB4318_5_Nhistory_bound", "N_history_transition", "history/transition/mass-current survives", "N_history + N_transition + N_mass_current", "BOUND_ROUTE_REQUIRED"),
        ("ZB4318_6_Nboundary_zero", "N_boundary_domain", "no-flux, zero-mode and fixed-domain certificates signed", "N_boundary_domain=0", "CONDITIONAL_ZERO_ROUTE"),
        ("ZB4318_7_Nboundary_bound", "N_boundary_domain", "boundary/domain/zero-mode survives", "N_no_flux + N_zero_mode + N_outer + N_history_boundary + N_domain", "BOUND_ROUTE_REQUIRED"),
        ("ZB4318_8_NN_absorb", "N_N", "small nonlinear Lipschitz remainder", "Delta_m <= N_linear/((1-kappa_N)lambda_m)", "DERIVED_ABSORPTION_ROUTE_VALUES_MISSING"),
        ("ZB4318_9_NN_bound", "N_N", "nonlinear/noise not absorbable", "retain N_N in N_rest_nonEM^canon", "BOUND_ROUTE_REQUIRED"),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, symbol, condition, output, status in specs:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "condition": condition,
                "output": output,
                "status": status,
            }
        )
        rows.append(row)
    return rows


def priority_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "P4318_1",
            "1",
            "N_src_nonHilbert / Hperp",
            "highest leverage direct source row; already has standard zero route and finite Dq/Hperp route",
            NEXT_TARGET,
        ),
        (
            "P4318_2",
            "2",
            "N_drift_selector",
            "can be killed by fixed selector/local branch theorem; otherwise easy absolute sum",
            "43120-Y5-R2FR-fixed-selector-drift-zero-or-bound-row.md",
        ),
        (
            "P4318_3",
            "3",
            "N_history_transition",
            "transition/history leakage is dangerous for local tests but should be separated from source support",
            "43121-Y5-R2FR-history-transition-causal-silence-or-bound-row.md",
        ),
        (
            "P4318_4",
            "4",
            "N_boundary_domain",
            "important but depends on no-flux/zero-mode/domain certificates already entangled with lambda/domain gates",
            "43122-Y5-R2FR-boundary-domain-no-flux-zero-mode-or-bound-row.md",
        ),
        (
            "P4318_5",
            "5",
            "N_N absorption",
            "should be handled once lambda_m and linear residual rows are clearer",
            "43123-Y5-R2FR-nonlinear-absorption-kappaN-or-remainder-bound.md",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for priority_id, rank, target, reason, proposed_target in specs:
        row = base_row()
        row.update(
            {
                "priority_id": priority_id,
                "rank": rank,
                "target": target,
                "reason": reason,
                "proposed_target": proposed_target,
            }
        )
        rows.append(row)
    return rows


def single_count_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "SC4318_0_canon",
            "canonical N_rest_nonEM",
            "N_rest_nonEM^canon := N_src_nonHilbert + N_drift_selector + N_history_transition + N_boundary_domain + N_N",
            "Use this symbol when quoting 4317/4318 source-pair reductions.",
            "REPAIR_APPLIED",
        ),
        (
            "SC4318_1_delta_m",
            "single-count m-lock handoff",
            "Delta_m <= N_rest_nonEM^canon/lambda_m",
            "Do not write Delta_m <= (N_rest_nonEM^canon + N_N)/lambda_m.",
            "DOUBLE_COUNT_BLOCKED",
        ),
        (
            "SC4318_2_linear_split",
            "linear/nonlinear split",
            "N_linear := N_src_nonHilbert + N_drift_selector + N_history_transition + N_boundary_domain",
            "Useful for nonlinear absorption.",
            "FORMULA_READY",
        ),
        (
            "SC4318_3_absorption",
            "nonlinear absorption law",
            "if N_N <= kappa_N lambda_m Delta_m and 0<=kappa_N<1, then Delta_m <= N_linear/((1-kappa_N)lambda_m)",
            "Moves small nonlinear remainder to the left side instead of double-counting it.",
            "DERIVED_CONDITIONAL",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for repair_id, name, formula, use_rule, status in specs:
        row = base_row()
        row.update(
            {
                "repair_id": repair_id,
                "name": name,
                "formula": formula,
                "use_rule": use_rule,
                "status": status,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        ("RUN4318_0_current", "current corpus", "USE_CANONICAL_BUDGET", "N_pair <= N_rest_nonEM^canon", "no local claim"),
        ("RUN4318_1_Nsrc_zero", "N_src_nonHilbert theorem-zeroed next", "REDUCE_BUDGET", "N_rest_nonEM^canon -> N_drift_selector+N_history_transition+N_boundary_domain+N_N", "best next move"),
        ("RUN4318_2_all_linear_zero", "source/drift/history/boundary zero", "CHECK_NONLINEAR", "Delta_m controlled by N_N/lambda_m or absorbed if kappa_N<1", "still needs lambda_m"),
        ("RUN4318_3_absorbed_NN", "N_N absorbable and lambda_m positive", "ALLOW_SOURCE_PAIR_ZERO_CONDITIONAL", "Delta_m=0 if N_linear=0", "not enough for local GR without downstream gates"),
        ("RUN4318_4_numeric_bound", "all residual rows sourced as finite values", "ALLOW_NONCLAIM_PRECISION_TEST", "feed R10/PPN/clocks/orbital residual budgets", "claim only after full gate coverage"),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, scenario, action, output, note in specs:
        row = base_row()
        row.update({"runner_id": runner_id, "scenario": scenario, "action": action, "output": output, "note": note})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    specs = [
        ("FW4318_0", "Do not double-count N_N after defining N_rest_nonEM^canon.", "ACTIVE"),
        ("FW4318_1", "Do not cancel N_src, drift, history, boundary and nonlinear rows against each other.", "ACTIVE"),
        ("FW4318_2", "Do not use U_B^2 source suppression in transition shells unless Hperp/Dq ownership is proved there.", "ACTIVE"),
        ("FW4318_3", "Do not claim local GR/Newton from N_pair=0 alone; source equality, commutator, projection and lambda gates remain.", "ACTIVE"),
        ("FW4318_4", "Do not absorb N_N unless a kappa_N<1 Lipschitz/smallness row is sourced or theorem-signed.", "ACTIVE"),
    ]
    rows: List[Dict[str, str]] = []
    for firewall_id, rule, status in specs:
        row = base_row()
        row.update({"firewall_id": firewall_id, "rule": rule, "status": status})
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        ("DEC4318_0_gain", "NREST_CANONICALIZED", "N_rest_nonEM is now a five-row single-count budget.", "use N_rest_nonEM^canon going forward"),
        ("DEC4318_1_repair", "NN_DOUBLE_COUNT_BLOCKED", "N_N is included exactly once in the canonical symbol.", "repair later formulas if they add +N_N to N_rest_nonEM^canon"),
        ("DEC4318_2_absorption", "NONLINEAR_ABSORPTION_ROUTE_DERIVED", "small N_N can move to the left side with a 1-kappa_N penalty.", "source kappa_N after linear rows are controlled"),
        ("DEC4318_3_priority", "NSRC_HPERP_FIRST", "N_src_nonHilbert has both a zero theorem route and an existing Hperp/Dq finite-bound route.", NEXT_TARGET),
        ("DEC4318_4_claim", "NO_LOCAL_CLAIM", "This is a budget/prioritization step, not a complete GR/Newton derivation.", "keep all claim flags false"),
    ]
    rows: List[Dict[str, str]] = []
    for decision_id, result, reason, next_action in specs:
        row = base_row()
        row.update({"decision_id": decision_id, "result": result, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4318_0_Nrest", "N_rest_nonEM^canon", "DEFINED_SINGLE_COUNT", "five residual rows, N_N included once"),
        ("STAT4318_1_Nsrc", "N_src_nonHilbert", "NEXT_PRIMARY_TARGET", "Hperp/Dq theorem-or-bound"),
        ("STAT4318_2_Ndrift", "N_drift_selector", "OPEN_ZERO_OR_BOUND", "fixed selector theorem needed"),
        ("STAT4318_3_Nhistory", "N_history_transition", "OPEN_ZERO_OR_BOUND", "causal/transition-kernel theorem needed"),
        ("STAT4318_4_Nboundary", "N_boundary_domain", "OPEN_ZERO_OR_BOUND", "no-flux/zero-mode/domain certificates needed"),
        ("STAT4318_5_NN", "N_N", "ABSORB_OR_BOUND", "requires kappa_N<1 or finite remainder row"),
        ("STAT4318_6_local", "local GR/Newton", "BLOCKED", "source equality, commutator, projection and lambda gates remain"),
    ]
    rows: List[Dict[str, str]] = []
    for status_id, obj, status, note in specs:
        row = base_row()
        row.update({"status_id": status_id, "object": obj, "status": status, "note": note})
        rows.append(row)
    return rows


def next_rows() -> List[Dict[str, str]]:
    row = base_row()
    row.update(
        {
            "next_target_id": "NT4318_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can N_src_nonHilbert be theorem-zeroed by the standard Dq/Hperp branch, or bounded by a real E_Dq,H / A_src row?",
            "preferred_route": "prove Hperp=0 or S_A Hperp^A=0 from parent source support and Dq ownership",
            "fallback_route": "fill nonclaim C_S, C_perp, E_Dq,H or U_B^2 A_src_general rows and feed them into N_rest_nonEM^canon",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 334 PPC4161 nonHilbert support drift history bound prioritizer

Marker: `{MARKER}`

## Decision

`{DECISION}`

4318 converts the post-4317 phrase `N_rest_nonEM` into a canonical, single-count object:

```text
N_rest_nonEM^canon :=
  N_src_nonHilbert
  + N_drift_selector
  + N_history_transition
  + N_boundary_domain
  + N_N.
```

This repairs the handoff convention: when `N_rest_nonEM^canon` is used, `N_N` is already inside it. Therefore

```text
Delta_m <= N_rest_nonEM^canon / lambda_m
```

not `Delta_m <= (N_rest_nonEM^canon + N_N)/lambda_m`.

The useful nonlinear route is also explicit. Let

```text
N_linear := N_src_nonHilbert + N_drift_selector + N_history_transition + N_boundary_domain.
```

If `N_N <= kappa_N lambda_m Delta_m` with `0 <= kappa_N < 1`, then

```text
Delta_m <= N_linear / ((1-kappa_N) lambda_m).
```

## Canonical Budget
{md_table(tables["budget"], ["residual_id", "symbol", "meaning", "zero_route", "bound_route", "priority", "double_count_guard"])}

## Zero Or Bound Matrix
{md_table(tables["zero_bound"], ["row_id", "symbol", "condition", "output", "status"])}

## Priority Order
{md_table(tables["priority"], ["priority_id", "rank", "target", "reason", "proposed_target"])}

## Single Count Repair
{md_table(tables["single_count"], ["repair_id", "name", "formula", "use_rule", "status"])}

## Runner
{md_table(tables["runner"], ["runner_id", "scenario", "action", "output", "note"])}

## Result

The next best attack is `N_src_nonHilbert/Hperp`: it is the highest-leverage direct source row and has both a clean zero theorem route and a finite Dq/Hperp bound route. Drift, history, boundary/domain and nonlinear rows remain absolute non-cancelling rows. No local GR/Newton claim fires.

Next target: `{NEXT_TARGET}`.
"""
    post = f"""# 4318 - nonHilbert support drift history bound prioritizer

## Verdict

- `N_rest_nonEM` is now canonical and single-count: `N_src_nonHilbert + N_drift_selector + N_history_transition + N_boundary_domain + N_N`.
- `N_N` is included once; do not add another `+N_N` after using `N_rest_nonEM^canon`.
- Nonlinear remainder has a real absorption route: if `N_N <= kappa_N lambda_m Delta_m`, then `Delta_m <= N_linear / ((1-kappa_N) lambda_m)`.
- Next target is `N_src_nonHilbert/Hperp`, because it has the best zero-or-bound machinery already built.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Canonical Budget
{md_table(tables["budget"], ["residual_id", "symbol", "zero_route", "bound_route", "priority"])}

## Priority Order
{md_table(tables["priority"], ["rank", "target", "reason", "proposed_target"])}

## Single Count Repair
{md_table(tables["single_count"], ["repair_id", "formula", "use_rule", "status"])}

## Runner
{md_table(tables["runner"], ["runner_id", "scenario", "action", "output", "note"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Status
{md_table(tables["status"], ["status_id", "object", "status", "note"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def validate_csv(path: Path) -> Tuple[bool, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    except Exception as exc:
        return False, f"csv parse failed: {exc}"
    if not rows:
        return False, "csv has no data rows"
    return True, f"csv parsed rows={len(rows)}"


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        row = base_row()
        row.update({"check_id": check_id, "description": description, "passed": str(passed), "evidence": evidence})
        rows.append(row)

    add("VAL4318_sources_exist", "all source paths exist", all(r["exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4318_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4318_budget_five", "canonical budget has five components", len(tables["budget"]) == 5, "budget")
    add("VAL4318_NN_once", "N_N appears as one canonical component", sum(1 for r in tables["budget"] if r["symbol"] == "N_N") == 1, "budget")
    add("VAL4318_Nsrc_priority", "Nsrc/Hperp selected as rank 1", any(r["rank"] == "1" and "N_src" in r["target"] for r in tables["priority"]), "priority")
    add("VAL4318_single_count", "single-count Delta_m formula exists", any("N_rest_nonEM^canon/lambda_m" in r["formula"] for r in tables["single_count"]), "single_count")
    add("VAL4318_no_double_count_rule", "double-count rule blocks +N_N", any("+ N_N" in r["use_rule"] and "Do not" in r["use_rule"] for r in tables["single_count"]), "single_count")
    add("VAL4318_absorption", "nonlinear absorption formula has 1-kappa_N", any("1-kappa_N" in r["formula"] for r in tables["single_count"]), "single_count")
    add("VAL4318_Hperp_bound", "Hperp/Dq bound route recorded", any("E_Dq,H" in r["bound_route"] for r in tables["budget"]), "budget")
    add("VAL4318_runner_next", "runner reduces budget after Nsrc zero", any(r["runner_id"] == "RUN4318_1_Nsrc_zero" for r in tables["runner"]), "runner")
    add("VAL4318_firewall_double_count", "firewall blocks N_N double counting", any("double-count N_N" in r["rule"] for r in tables["firewall"]), "firewall")
    add("VAL4318_claim_false", "all rows keep claim flags false", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for table in tables.values() for row in table), "all_tables")
    add("VAL4318_next_target", "next target is 4319 Hperp", any("4319" in r["next_target"] and "Hperp" in r["next_target"] for r in tables["next"]), "next")
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4318_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4318_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4318_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4318_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4318_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4318_SOURCE_REGISTER.csv",
        "budget": SOURCE_DIR / "P8_Y5_R2FR_4318_CANONICAL_NREST_BUDGET.csv",
        "zero_bound": SOURCE_DIR / "P8_Y5_R2FR_4318_ZERO_OR_BOUND_MATRIX.csv",
        "priority": SOURCE_DIR / "P8_Y5_R2FR_4318_PRIORITY_ORDER.csv",
        "single_count": SOURCE_DIR / "P8_Y5_R2FR_4318_SINGLE_COUNT_REPAIR.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4318_LOCAL_ROUTE_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4318_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4318_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4318_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4318_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "budget": budget_rows(),
        "zero_bound": zero_bound_rows(),
        "priority": priority_rows(),
        "single_count": single_count_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }
    for key, rows in tables.items():
        write_csv(paths[key], rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4318 nonHilbert support drift history bound prioritizer

Marker: `{MARKER}`

4318 canonicalizes the post-4317 residual budget as `N_rest_nonEM^canon = N_src_nonHilbert + N_drift_selector + N_history_transition + N_boundary_domain + N_N`, with `N_N` included exactly once. Thus the full source-silent branch uses `Delta_m <= N_rest_nonEM^canon/lambda_m`, not an extra `+N_N`. It also derives the nonlinear absorption option: if `N_N <= kappa_N lambda_m Delta_m` with `0<=kappa_N<1`, then `Delta_m <= N_linear/((1-kappa_N)lambda_m)`. The priority order selects `N_src_nonHilbert/Hperp` next, because it has the strongest existing zero-or-bound machinery.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4318 packet nonHilbert support drift history prioritizer

Marker: `{PACKET_MARKER}`

Packet update: the remaining non-EM budget is now a five-row single-count ledger. `N_N` is not to be added twice, and small nonlinear remainders can be absorbed with a `1-kappa_N` penalty. The next concrete attack is `N_src_nonHilbert/Hperp`.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} evidence={row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
