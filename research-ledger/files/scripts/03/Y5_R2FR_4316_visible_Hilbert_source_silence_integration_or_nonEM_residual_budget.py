from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4316"
CLAIM_ID = "L-157"
BRANCH = "MTS_R2FR_Y5_VISIBLE_HILBERT_SOURCE_SILENCE_INTEGRATION_OR_NONEM_RESIDUAL_BUDGET_4316"
DECISION = "VISIBLE_HILBERT_AND_EM_ZERO_BRANCHES_INTEGRATED_NONEM_RESIDUAL_BUDGET_ISOLATED_NONCLAIM"
MARKER = "PPC4161_VISIBLE_HILBERT_SOURCE_SILENCE_INTEGRATION_OR_NONEM_RESIDUAL_BUDGET_4316"
PACKET_MARKER = "PPC4161_PACKET_VISIBLE_HILBERT_SOURCE_SILENCE_INTEGRATION_OR_NONEM_RESIDUAL_BUDGET_4316"
NEXT_TARGET = "4317-Y5-R2FR-nonEM-inner-charge-domain-zero-or-QmH-bound-values.md"

FORMAL_PATH = FORMAL / "332-PPC4161-visible-Hilbert-source-silence-integration-or-nonEM-residual-budget.md"
DOC_PATH = POST / "4316-Y5-R2FR-visible-Hilbert-source-silence-integration-or-nonEM-residual-budget.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4316_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4316_00_4315_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4315_NEXT_TARGET.csv",
        "4316-Y5-R2FR-visible-Hilbert-source-silence-integration-or-nonEM-residual-budget.md",
        "4315 handoff selecting visible Hilbert source silence integration.",
    ),
    "SRC4316_01_4303_silence": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "delta S_vis/delta m = 0",
        "4303 visible Hilbert source-silence theorem.",
    ),
    "SRC4316_02_4303_nonHilbert": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "J_eff+B_m = R_nonHilbert + R_hidden_EM + R_transition + R_history + R_boundary",
        "4303 residual survivor decomposition.",
    ),
    "SRC4316_03_4305_pair": (
        FORMAL / "321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md",
        "N_pair <= N_inner + N_EM + N_rest",
        "4305 source-pair reduced runner.",
    ),
    "SRC4316_04_4305_NEM": (
        FORMAL / "321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md",
        "NEM4305_1_residual_envelope",
        "4305 EM residual envelope before 4312-4315 refinement.",
    ),
    "SRC4316_05_4312_EM": (
        FORMAL / "328-PPC4161-Zmin-M2min-EtaH-source-or-Poynting-residual-cancellation.md",
        "R_EM_Poynting <= C_H dH",
        "4312 Poynting/EM residual bound.",
    ),
    "SRC4316_06_4313_current": (
        FORMAL / "329-PPC4161-EM-Ward-current-normalization-or-collar-residual-bound-values.md",
        "Delta_internal_exchange=0",
        "4313 current/Ward exchange zero-or-bound gate.",
    ),
    "SRC4316_07_4314_radiation": (
        FORMAL / "330-PPC4161-radiative-Poynting-no-flux-or-boundary-flux-row.md",
        "Delta_rad_Poynting = 0.",
        "4314 radiative Poynting zero-or-bound gate.",
    ),
    "SRC4316_08_4315_Hodge": (
        FORMAL / "331-PPC4161-Hodge-constitutive-owner-zero-or-DeltaHodge-bound.md",
        "Delta_Hodge_EM=0",
        "4315 Hodge/constitutive zero-or-bound gate.",
    ),
    "SRC4316_09_4311_SU": (
        FORMAL / "327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md",
        "S_U := R_U + N_N + N_boundary",
        "4311 collar residual numerator feeding lambda-floor route.",
    ),
    "SRC4316_10_4306_inner": (
        FORMAL / "322-PPC4161-inner-domain-certificate-or-QmH-bound.md",
        "Q_m^H",
        "4306 inner-domain/source-charge blocker.",
    ),
    "SRC4316_11_precision": (
        FORMAL / "309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md",
        "order-one projection of epsilon_AJ_seed into local observables fails",
        "local precision guard for residual budgets.",
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
            "4316 integrates the visible Hilbert source-silence theorem with the refined EM zero-or-bound ledger. "
            "On the calibrated visible branch, ordinary matter and Maxwell-Hodge/Poynting do not source the m-lock "
            "equation directly because S_vis has no direct m slot before readout. If the EM subgates from 4312-4315 "
            "also close, N_visible=0 and N_EM=0, so the source-pair budget reduces to N_pair <= N_inner + N_rest_nonEM. "
            "If any visible/EM clause fails, the residual is retained as an absolute no-cancellation row. The remaining "
            "live non-EM budget is inner charge/source-domain, non-Hilbert support, drift/selector, history/transition, "
            "boundary/domain and nonlinear/noise terms, feeding S_U, Eta_H and the lambda-floor route. No local GR/Newton "
            "claim fires."
        ),
        (
            "4316 source register, visible silence integration, EM closure matrix, reduced non-EM residual budget, "
            "collar/lambda update, runner, firewall, status, next-target and validation CSV."
        ),
        "private_visible_Hilbert_EM_zero_branch_integrated_nonEM_residual_budget_nonclaim",
        (
            "Parent-sign or source-bound N_inner/Q_m^H, non-Hilbert support, drift/selector, history/transition, "
            "boundary/domain and N_N residual rows; then feed them into the lambda-floor criterion."
        ),
        (
            "Treating visible Hilbert silence as a global source theorem, hiding non-Hilbert support inside calibrated "
            "matter, cancelling EM residual terms against non-EM terms, or claiming local GR/Newton while lambda/source "
            "equality and projection gates remain open."
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


def visible_integration_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "VI4316_0_action_split",
            "visible Hilbert action split",
            "S_parent = S_lock[m,q] + S_vis[g_obs(q),psi,A,lambda0] + S_boundary",
            "if S_vis has no direct m slot, delta S_vis/delta m=0",
            "EXACT_CONDITIONAL_THEOREM",
        ),
        (
            "VI4316_1_matter_zero",
            "ordinary visible matter",
            "S_matter varies through g_obs(q), psi and fixed visible data only",
            "J_visible_matter_to_m=0 on signed branch",
            "CONDITIONAL_ZERO_ROUTE",
        ),
        (
            "VI4316_2_EM_zero",
            "visible EM/Poynting",
            "same-Hodge, fixed-current, no extra Poynting source, no radiative collar flux and no constitutive residual",
            "N_EM=0 on full EM zero branch",
            "CONDITIONAL_ZERO_ROUTE_REFINED_BY_4312_4315",
        ),
        (
            "VI4316_3_boundary_routing",
            "visible boundary/radiative flux",
            "visible flux is Hilbert bookkeeping or routed boundary/Hamiltonian flux, not an m-boundary charge",
            "does not enter hidden bulk source; open flux remains N_boundary",
            "ZERO_OR_BOUND_ROUTE",
        ),
        (
            "VI4316_4_failure",
            "visible theorem failure",
            "source-only weights, non-Hilbert currents, direct m slot or prevariation readout enter S_parent",
            "visible residual is retained as absolute source norm",
            "BOUND_ROUTE_IF_NOT_SIGNED",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, component, premise, result, status in specs:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "component": component,
                "premise": premise,
                "result": result,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def em_matrix_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "EM4316_0_Poynting_once",
            "c_Poynt_extra",
            "zero if Poynting is counted once as Maxwell-Hodge Hilbert stress",
            "standalone Poynting source retained if not",
            "4312",
        ),
        (
            "EM4316_1_current",
            "C_JQ/Delta_internal_exchange",
            "zero if same Maxwell/matter current and calibrated q-basic current branch",
            "F deltaJ bound if not",
            "4313",
        ),
        (
            "EM4316_2_radiation",
            "Delta_rad_Poynting",
            "zero if closed collar has pointwise no-through EM flux",
            "P_rad/E_rad boundary row if not",
            "4314",
        ),
        (
            "EM4316_3_Hodge",
            "Delta_Hodge_EM",
            "zero if same observed Hodge and no independent constitutive terms",
            "no-cancellation constitutive envelope if not",
            "4315",
        ),
        (
            "EM4316_4_weights",
            "delta_w_EM/b_alpha/C_XF2",
            "zero if calibrated visible constants and no hidden F2/source weights",
            "normalization/source-weight residual if not",
            "4262/4305",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for gate_id, symbol, zero_route, fallback, source_checkpoint in specs:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "symbol": symbol,
                "zero_route": zero_route,
                "fallback": fallback,
                "source_checkpoint": source_checkpoint,
                "status": "ZERO_OR_BOUND_GATE",
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def nonem_budget_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "NB4316_0_Ninner",
            "N_inner",
            "inner charge/source-domain or excision boundary residual",
            "N_inner <= C_inner |Q_m^H| or zero on smooth/no-excision/signed no-inner-charge branch",
            "PRIMARY_LIVE_BLOCKER",
        ),
        (
            "NB4316_1_Nsrc_nonHilbert",
            "N_src_nonHilbert",
            "source support outside Hilbert/q-kernel branch or U_B projection survives",
            "N_src <= ||U_B||_inf ||S_cg_nonHilbert||",
            "RETAINED_BOUND_ROW",
        ),
        (
            "NB4316_2_Ndrift_selector",
            "N_drift_selector",
            "drift in m, L_cg or local selector not fixed/q-basic",
            "N_drift_selector <= N_drift_mL + N_drift_Lcg + N_selector",
            "RETAINED_BOUND_ROW",
        ),
        (
            "NB4316_3_Nhistory_transition",
            "N_history_transition",
            "history/memory/transition shell membership or causal silence not signed",
            "N_history_transition <= N_history + N_transition + N_mass_current",
            "RETAINED_BOUND_ROW",
        ),
        (
            "NB4316_4_Nboundary_domain",
            "N_boundary_domain",
            "boundary/domain/zero-mode/outer/history boundary flux survives",
            "N_boundary_domain <= N_no_flux + N_zero_mode + N_outer + N_history_boundary + N_domain",
            "RETAINED_BOUND_ROW",
        ),
        (
            "NB4316_5_NN",
            "N_N",
            "nonlinear/noise/remainder forcing in collar m-lock equation",
            "must be zero or bounded before lambda-floor scoring",
            "RETAINED_BOUND_ROW",
        ),
        (
            "NB4316_6_projection_source",
            "projection/source-equality gates",
            "R_eq, I_commutator, projection/tomography and calibration constants remain open",
            "cannot be removed by visible Hilbert silence",
            "DOWNSTREAM_GATE",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for budget_id, symbol, meaning, law_or_bound, status in specs:
        row = base_row()
        row.update(
            {
                "budget_id": budget_id,
                "symbol": symbol,
                "meaning": meaning,
                "law_or_bound": law_or_bound,
                "status": status,
                "source_path": "",
                "numeric_value": "",
                "units": "collar/source-normalized norm or explicit declared units",
                "next_action": "parent-sign zero route or fill sourced bound row",
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def reduced_formula_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RF4316_0_full",
            "full source-pair budget",
            "N_pair <= N_inner + N_EM + N_rest_nonEM",
            "4305 with EM and non-EM split",
            "FORMULA_READY",
        ),
        (
            "RF4316_1_visible_EM_zero",
            "visible+EM zero branch",
            "if N_visible=0 and N_EM=0 then N_pair <= N_inner + N_rest_nonEM",
            "main reduction achieved by 4316",
            "CONDITIONAL_REDUCTION",
        ),
        (
            "RF4316_2_all_source_zero",
            "source-pair zero branch",
            "if N_inner=0 and N_rest_nonEM=0 then N_pair=0",
            "not live until non-EM rows close",
            "EXACT_ZERO_CONDITIONAL_NOT_LIVE",
        ),
        (
            "RF4316_3_SU",
            "collar numerator",
            "S_U <= S_U_visible_silent + N_inner + N_EM + N_rest_nonEM + N_N + N_boundary_extra",
            "feeds 4311 lambda-floor trace bound",
            "FORMULA_READY_VALUES_MISSING",
        ),
        (
            "RF4316_4_lambda",
            "lambda route",
            "N_inner <= C_N[K_U C_col S_U/lambda_* + R_U] + ||B_src^A|| with S_U now reduced by visible/EM zero branches",
            "same 4311 trace criterion, cleaner numerator",
            "GUARDED_BY_LAMBDA_AND_NONEM_INPUTS",
        ),
        (
            "RF4316_5_local_claim",
            "local GR/Newton",
            "no claim until lambda_*, non-EM budget, source equality, commutator and projection gates close",
            "claim firewall",
            "BLOCKED",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for formula_id, name, formula, role, status in specs:
        row = base_row()
        row.update(
            {
                "formula_id": formula_id,
                "name": name,
                "formula": formula,
                "role": role,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RUN4316_0_current_corpus",
            "current corpus",
            "REDUCED_BUDGET_NOT_CLAIM",
            "visible Hilbert and EM zero routes are branch-clean; non-EM residuals and lambda/source-equality gates remain open",
            "work the non-EM primary blocker next",
        ),
        (
            "RUN4316_1_standard_visible_EM",
            "calibrated visible branch plus all EM subgates closed",
            "ALLOW_N_VISIBLE_N_EM_ZERO_CONDITIONAL",
            "N_pair reduces to N_inner + N_rest_nonEM",
            "score only after non-EM rows and lambda floor are real",
        ),
        (
            "RUN4316_2_EM_deformation",
            "any EM subgate survives",
            "KEEP_N_EM_ENVELOPE",
            "N_EM remains an absolute no-cancellation residual envelope",
            "source every surviving EM term before local tests",
        ),
        (
            "RUN4316_3_nonEM_zero",
            "N_inner and all N_rest_nonEM rows zero",
            "ALLOW_N_PAIR_ZERO_CONDITIONAL",
            "source-pair forcing vanishes before lambda trace scoring",
            "still needs lambda, R_eq, I_commutator and projection gates",
        ),
        (
            "RUN4316_4_local_claim",
            "claim local GR/Newton/R10/PPN now",
            "REJECT",
            "N_inner/nonEM rows, lambda_* and source-equality/projection gates are not closed",
            "no public or empirical claim from 4316",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, case, result, reason, next_action in specs:
        row = base_row()
        row.update(
            {
                "runner_id": runner_id,
                "case": case,
                "result": result,
                "reason": reason,
                "next_action": next_action,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DEC4316_0_integration",
            "VISIBLE_AND_EM_ZERO_BRANCHES_INTEGRATED",
            "Visible Hilbert source silence and the refined EM gates now combine into N_visible=0 and N_EM=0 conditions.",
            "use only inside the calibrated/same-owner branch",
        ),
        (
            "DEC4316_1_reduction",
            "SOURCE_BUDGET_REDUCED_TO_NONEM",
            "When the visible+EM branch closes, N_pair <= N_inner + N_rest_nonEM.",
            "attack N_inner/Q_m^H and non-Hilbert residuals next",
        ),
        (
            "DEC4316_2_firewall",
            "NO_CROSS_CANCELLATION",
            "EM residuals, non-EM residuals and lambda terms are absolute rows; no cancellation credit is allowed.",
            "keep component ledger discipline",
        ),
        (
            "DEC4316_3_next",
            "NINNER_QMH_NEXT",
            "The sharpest remaining source blocker is inner/domain charge or its bound.",
            NEXT_TARGET,
        ),
        (
            "DEC4316_4_claim",
            "NO_LOCAL_CLAIM",
            "This is a major budget reduction, not a complete local-GR/Newton proof.",
            "keep all claim flags false",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for decision_id, result, reason, next_action in specs:
        row = base_row()
        row.update({"decision_id": decision_id, "result": result, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    rules = [
        "Do not treat visible Hilbert silence as a global source theorem outside the calibrated branch.",
        "Do not cancel EM residuals against non-EM residuals or lambda-floor terms.",
        "Do not hide non-Hilbert support, inner charge, transition/history or boundary/domain rows inside visible matter.",
        "Do not claim N_pair=0 until N_inner and every non-EM residual row is zero or sourced below bound.",
        "Do not claim local GR/Newton/R10/PPN until lambda, source-equality, commutator and projection gates close.",
    ]
    rows: List[Dict[str, str]] = []
    for index, rule in enumerate(rules):
        row = base_row()
        row.update({"firewall_id": f"FW4316_{index}", "rule": rule, "status": "ACTIVE"})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4316_0_visible", "N_visible", "ZERO_OR_BOUND", "zero on visible Hilbert no-direct-m branch"),
        ("STAT4316_1_EM", "N_EM", "ZERO_OR_BOUND", "zero only if 4312-4315 EM gates close"),
        ("STAT4316_2_Npair", "N_pair", "REDUCED", "standard branch now N_inner + N_rest_nonEM"),
        ("STAT4316_3_Ninner", "N_inner/Q_m^H", "PRIMARY_NEXT_BLOCKER", "inner/domain source charge remains live"),
        ("STAT4316_4_lambda", "lambda_* and S_U", "STILL_GATED", "cleaner numerator but missing positive floor/input values"),
        ("STAT4316_5_local", "local GR/Newton", "BLOCKED", "reduction improved but proof remains incomplete"),
    ]
    rows: List[Dict[str, str]] = []
    for status_id, item, status, note in specs:
        row = base_row()
        row.update({"status_id": status_id, "item": item, "status": status, "note": note})
        rows.append(row)
    return rows


def next_rows() -> List[Dict[str, str]]:
    row = base_row()
    row.update(
        {
            "next_target_id": "NT4316_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can N_inner be theorem-zeroed by the smooth/domain/Hilbert-charge branch, or must Q_m^H and C_inner be source-bounded?",
            "preferred_route": "derive N_inner=0 from smooth no-excision plus no independent m-charge/source-kernel ownership",
            "fallback_route": "fill nonclaim C_inner and Q_m^H bound rows with domain convention and units",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal_text = f"""# 332 PPC4161 visible Hilbert source silence integration or nonEM residual budget

Marker: `{MARKER}`

## Decision

`{DECISION}`

4316 integrates the visible theorem with the EM zero-or-bound ladder:

```text
S_parent = S_lock[m,q] + S_vis[g_obs(q),psi,A,lambda0] + S_boundary,
delta S_vis/delta m = 0
```

on the signed visible Hilbert branch.

With the EM gates from 4312-4315 closed:

```text
N_visible = 0,
N_EM = 0,
N_pair <= N_inner + N_rest_nonEM.
```

Without those gates:

```text
N_pair <= N_inner + N_EM_envelope + N_rest_nonEM.
```

The remaining non-EM budget is:

```text
N_rest_nonEM =
  N_src_nonHilbert
 + N_drift_selector
 + N_history_transition
 + N_boundary_domain
 + N_N
 + downstream source-equality/projection gates.
```

No cross-cancellation is allowed.

## Visible Silence Integration

{md_table(tables["visible"], ["row_id", "component", "premise", "result", "status"])}

## EM Closure Matrix

{md_table(tables["em_matrix"], ["gate_id", "symbol", "zero_route", "fallback", "source_checkpoint"])}

## Non-EM Residual Budget

{md_table(tables["nonem"], ["budget_id", "symbol", "meaning", "law_or_bound", "status"])}

## Reduced Formulas

{md_table(tables["formulas"], ["formula_id", "name", "formula", "role", "status"])}

## Runner

{md_table(tables["runner"], ["runner_id", "case", "result", "reason"])}

## Result

The source problem is now narrower: visible/EM can be silent on a disciplined branch, leaving inner/domain charge and non-Hilbert residuals as the real live budget.

Next target: `{NEXT_TARGET}`.
"""
    doc_text = f"""# 4316 - visible Hilbert source silence integration or nonEM residual budget

## Verdict
- Integrated visible Hilbert no-direct-`m` silence with the refined EM zero-or-bound ladder.
- Conditional reduction: if visible+EM gates close, `N_pair <= N_inner + N_rest_nonEM`.
- Retained fallback: any EM deformation stays in `N_EM_envelope`; no cancellation with non-EM terms.
- Isolated the remaining non-EM budget: `N_inner`, non-Hilbert support, drift/selector, history/transition, boundary/domain, `N_N`, and downstream source-equality/projection gates.
- No local-GR/Newton/R10/PPN claim fires.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Visible Silence Integration
{md_table(tables["visible"], ["row_id", "component", "premise", "result", "status"])}

## EM Closure Matrix
{md_table(tables["em_matrix"], ["gate_id", "symbol", "zero_route", "fallback", "source_checkpoint", "status"])}

## Non-EM Residual Budget
{md_table(tables["nonem"], ["budget_id", "symbol", "meaning", "law_or_bound", "status", "next_action"])}

## Reduced Formulas
{md_table(tables["formulas"], ["formula_id", "name", "formula", "role", "status"])}

## Runner
{md_table(tables["runner"], ["runner_id", "case", "result", "reason", "next_action"])}

## Claim Firewall
{md_table(tables["firewall"], ["firewall_id", "rule", "status"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Status
{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal_text, encoding="utf-8")
    DOC_PATH.write_text(doc_text, encoding="utf-8")


def validate_csv(path: Path) -> Tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), f"{path.name} parses with {len(rows)} rows"
    except Exception as exc:
        return False, f"{path.name} parse failure: {exc}"


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        row = base_row()
        row.update({"check_id": check_id, "description": description, "passed": str(passed), "evidence": evidence})
        rows.append(row)

    add("VAL4316_0_sources_exist", "all cited local source paths exist", all(Path(row["source_path"]).exists() for row in tables["sources"]), "source_register")
    add("VAL4316_1_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4316_2_visible_zero", "visible Hilbert zero row exists", any(row["row_id"] == "VI4316_1_matter_zero" for row in tables["visible"]), "visible")
    add("VAL4316_3_em_matrix", "EM closure matrix has five gates", len(tables["em_matrix"]) == 5, "em_matrix")
    add("VAL4316_4_nonem_budget", "non-EM budget rows include N_inner", any(row["budget_id"] == "NB4316_0_Ninner" for row in tables["nonem"]), "nonem")
    add("VAL4316_5_reduced_formula", "reduced N_pair formula exists", any(row["formula_id"] == "RF4316_1_visible_EM_zero" for row in tables["formulas"]), "formulas")
    add("VAL4316_6_no_claim_runner", "runner rejects local claim", any(row["runner_id"] == "RUN4316_4_local_claim" and row["result"] == "REJECT" for row in tables["runner"]), "runner")
    add("VAL4316_7_next_selected", f"next target is {NEXT_TARGET}", tables["next"][0]["next_target"] == NEXT_TARGET, "next")
    add(
        "VAL4316_8_claim_flags_false",
        "all generated rows keep claim flags false",
        all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for table in tables.values() for row in table),
        "generated_tables",
    )
    add(
        "VAL4316_9_score_flags_false",
        "all score rows remain unscored/nonclaim",
        all(row.get("score_ready", "False") == "False" for table in tables.values() for row in table),
        "generated_tables",
    )
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4316_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4316_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "generated_docs")
    add("VAL4316_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims_register")
    add("VAL4316_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "unification_spine")
    add("VAL4316_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "private_packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4316_SOURCE_REGISTER.csv",
        "visible": SOURCE_DIR / "P8_Y5_R2FR_4316_VISIBLE_SILENCE_INTEGRATION.csv",
        "em_matrix": SOURCE_DIR / "P8_Y5_R2FR_4316_EM_CLOSURE_MATRIX.csv",
        "nonem": SOURCE_DIR / "P8_Y5_R2FR_4316_NONEM_RESIDUAL_BUDGET.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4316_REDUCED_SOURCE_FORMULAS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4316_COLLAR_ROUTE_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4316_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4316_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4316_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4316_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "visible": visible_integration_rows(),
        "em_matrix": em_matrix_rows(),
        "nonem": nonem_budget_rows(),
        "formulas": reduced_formula_rows(),
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
## PPC4161 4316 visible Hilbert source silence integration or nonEM residual budget

Marker: `{MARKER}`

4316 integrates visible Hilbert source silence with the refined EM zero-or-bound ladder. On the calibrated visible branch with all EM subgates closed, `N_visible=0` and `N_EM=0`, so `N_pair <= N_inner + N_rest_nonEM`. The remaining live budget is inner/domain charge, non-Hilbert support, drift/selector, history/transition, boundary/domain, nonlinear/noise and downstream source-equality/projection gates. No cross-cancellation or local-GR/Newton claim is allowed.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4316 packet visible Hilbert and nonEM residual budget

Marker: `{PACKET_MARKER}`

Packet update: the visible/EM source branch now has a clean reduction. If the branch closes, the source-pair budget narrows to `N_inner + N_rest_nonEM`; if not, every visible or EM deformation stays in an explicit absolute residual row.
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
