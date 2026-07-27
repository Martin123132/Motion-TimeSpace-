from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4311"
CLAIM_ID = "L-152"
BRANCH = "MTS_R2FR_Y5_LAMBDA_FLOOR_SOURCE_ROW_OR_COLLAR_RESIDUAL_FIRST_BOUND_4311"
DECISION = "LAMBDA_FLOOR_POSITIVITY_LAW_DERIVED_COMPONENTS_UNSOURCED_FIRST_COLLAR_RESIDUAL_BOUND_STAGED_NONCLAIM"
MARKER = "PPC4161_LAMBDA_FLOOR_SOURCE_ROW_OR_COLLAR_RESIDUAL_FIRST_BOUND_4311"
PACKET_MARKER = "PPC4161_PACKET_LAMBDA_FLOOR_SOURCE_ROW_OR_COLLAR_RESIDUAL_FIRST_BOUND_4311"
NEXT_TARGET = "4312-Y5-R2FR-Zmin-M2min-EtaH-source-or-Poynting-residual-cancellation.md"

FORMAL_PATH = FORMAL / "327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md"
DOC_PATH = POST / "4311-Y5-R2FR-lambda-floor-source-row-or-collar-residual-first-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4311_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4311_00_4310_formal": (
        FORMAL / "326-PPC4161-collar-no-concentration-signature-or-trace-bound-inputs.md",
        "A_U <= C_col (R_U + N_N + N_boundary) / lambda_*.",
        "4310 reduced the trace defect to lambda floor plus collar residual numerator.",
    ),
    "SRC4311_01_4310_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4310_NEXT_TARGET.csv",
        "4311-Y5-R2FR-lambda-floor-source-row-or-collar-residual-first-bound.md",
        "4310 handoff selecting lambda floor or first residual row.",
    ),
    "SRC4311_02_4302_lambda_formula": (
        FORMAL / "318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md",
        "lambda_m = Z_min lambda_1(D_loc) + M2_min - Eta_H",
        "parent m-lock coercive gap formula.",
    ),
    "SRC4311_03_4302_component_gaps": (
        FORMAL / "318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md",
        "IP4302_0_Zmin",
        "component ledger showing Z_min is still missing.",
    ),
    "SRC4311_04_4302_eta": (
        FORMAL / "318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md",
        "IP4302_4_EtaH",
        "component ledger showing Eta_H correction bound is still missing.",
    ),
    "SRC4311_05_4268_fixed_collar": (
        FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md",
        "fixed compact no-flux local collar/worldtube branch",
        "fixed collar/q-basic boundary projector branch.",
    ),
    "SRC4311_06_4176_no_flux": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "supp(T_local) subset int(W_loc)",
        "local no-flux/support-separation selector.",
    ),
    "SRC4311_07_319_no_m_slot": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "with no direct m slot in S_vis",
        "visible Hilbert matter no-direct-m source clause.",
    ),
    "SRC4311_08_321_source_split": (
        FORMAL / "321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md",
        "N_pair <= N_inner + N_EM + N_rest",
        "source-pair residual split entering collar forcing.",
    ),
    "SRC4311_09_223_poynting": (
        FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md",
        "Poynting vector is real physical flow",
        "Poynting/Hilbert stress owner rule for EM residual handling.",
    ),
    "SRC4311_10_309_precision": (
        FORMAL / "309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md",
        "order-one projection of epsilon_AJ_seed into local observables fails",
        "local tests require zero/suppression, not raw leakage.",
    ),
    "SRC4311_11_1714_guard": (
        POST / "1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md",
        "R_eq",
        "source-to-Newton equality guard still open.",
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
            "4311 derives the exact lambda-floor positivity law for the fixed-collar branch. With "
            "a_U[u,u] bounded below by Z_min||grad u||^2 + M2_min||u||^2 - Eta_H||u||^2 and "
            "the collar Poincare/eigenvalue relation ||grad u||^2 >= lambda_1(D_loc)||u||^2, "
            "the sufficient floor is lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H. Thus the "
            "local trace-defect route has three honest closure branches: Poincare/Dirichlet gap, "
            "mass-only zero-mode gap, or mixed positive margin. The current corpus does not source "
            "Z_min, M2_min, lambda_1(D_loc) or Eta_H as parent-owned positive/numeric rows, so 4311 "
            "stages the first collar residual bound and keeps local-GR/Newton/R10/PPN claims blocked."
        ),
        (
            "4311 source register, lambda floor component ledger, positivity route audit, collar residual "
            "first bound, lambda budget runner, claim firewall, status, next-target and validation CSV."
        ),
        "private_lambda_floor_positivity_law_derived_components_unsourced_residual_bound_nonclaim",
        (
            "Parent-source Z_min, M2_min, lambda_1(D_loc) and Eta_H, or prove EM/Poynting and visible "
            "Hilbert residual cancellation in the collar so the numerator vanishes before scoring local tests."
        ),
        (
            "Claiming lambda_*>0 from formula shape alone, treating a conditional no-flux selector as a "
            "numeric residual zero, hiding Poynting/open-boundary flux inside R_U, or claiming local GR/Newton "
            "while source equality, commutator and projection gates remain open."
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


def lambda_component_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "LC4311_0_Zmin",
            "Z_min",
            "elliptic kinetic lower bound for the m-lock fluctuation on the collar",
            "Z_m >= Z_min > 0",
            "MISSING_SOURCE_VALUE_OR_THEOREM",
            "needed for Poincare/mixed positive gap",
            "source parent kinetic sign/normalization or demote to fitted closure",
        ),
        (
            "LC4311_1_lambda1",
            "lambda_1(D_loc)",
            "first positive eigenvalue/Poincare gap of the fixed collar domain",
            "||grad u||^2 >= lambda_1(D_loc)||u||^2 after zero-mode/gauge branch is fixed",
            "MISSING_DOMAIN_SPECTRUM_OR_ZERO_MODE_SELECTOR",
            "needed unless mass-only gap controls zero mode",
            "source fixed collar geometry or prove zero-mode is removed by boundary/gauge condition",
        ),
        (
            "LC4311_2_M2min",
            "M2_min",
            "lower Hessian/memory mass curvature in the m direction",
            "M_m^2 >= M2_min",
            "MISSING_SOURCE_VALUE_OR_THEOREM",
            "needed for mass-only and mixed positive gaps",
            "derive from parent potential Hessian or source an empirical/theorem lower bound",
        ),
        (
            "LC4311_3_EtaH",
            "Eta_H",
            "absolute negative correction from hidden/source/boundary/operator terms",
            "|negative correction| <= Eta_H||u||^2",
            "MISSING_CORRECTION_BOUND",
            "must be smaller than the positive kinetic+mass margin",
            "bound EM/Poynting, non-Hilbert and boundary corrections separately",
        ),
        (
            "LC4311_4_lambda_star",
            "lambda_*",
            "positive lower floor used by 4310 trace-defect bound",
            "lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H",
            "FORMULA_DERIVED_VALUE_UNSOURCED",
            "turns A_U into residual/lambda bound",
            "only score after every component row is parent-owned and positive-margin checked",
        ),
        (
            "LC4311_5_zero_mode_mass_branch",
            "lambda_*_mass",
            "zero-mode-safe floor if Poincare gap is unavailable",
            "lambda_*_mass = M2_min-Eta_H",
            "ALTERNATE_ROUTE_FORMULA_READY_VALUE_UNSOURCED",
            "avoids depending on lambda_1 if M2_min dominates",
            "try this if collar boundary conditions leave a constant mode",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for component_id, symbol, definition, required_law, status, role, next_action in specs:
        row = base_row()
        row.update(
            {
                "component_id": component_id,
                "symbol": symbol,
                "definition": definition,
                "required_law": required_law,
                "status": status,
                "role": role,
                "source_path": "",
                "numeric_value": "",
                "units": "operator-normalized spectral/Hessian units",
                "next_action": next_action,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def positivity_route_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "PR4311_0_poincare_dirichlet",
            "Poincare/Dirichlet collar gap",
            "Z_min > 0, lambda_1(D_loc) > 0, and Eta_H < Z_min lambda_1(D_loc)+M2_min",
            "lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H > 0",
            "VALID_THEOREM_ROUTE_IF_COMPONENTS_SIGNED",
            "not live because all component values/theorems are unsourced",
        ),
        (
            "PR4311_1_mass_only",
            "mass-only zero-mode gap",
            "M2_min > Eta_H",
            "lambda_* >= M2_min-Eta_H > 0 even if lambda_1(D_loc)=0",
            "VALID_THEOREM_ROUTE_IF_COMPONENTS_SIGNED",
            "best route if local collar has Neumann/constant zero mode",
        ),
        (
            "PR4311_2_mixed_margin",
            "mixed kinetic plus memory margin",
            "margin := Z_min lambda_1(D_loc)+M2_min-Eta_H, margin >= lambda_floor_candidate > 0",
            "use lambda_floor_candidate in 4310 reduced trace bound",
            "VALID_THEOREM_ROUTE_IF_MARGIN_SOURCED",
            "turns qualitative positivity into an auditable numeric/theorem row",
        ),
        (
            "PR4311_3_failure",
            "negative or unsourced correction dominance",
            "Eta_H >= Z_min lambda_1(D_loc)+M2_min or any component is placeholder",
            "no lambda floor; only unscored residual ledger survives",
            "CLAIM_BLOCKED",
            "do not proceed to local-GR/R10/PPN scoring",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for route_id, route, conditions, result, status, implication in specs:
        row = base_row()
        row.update(
            {
                "route_id": route_id,
                "route": route,
                "conditions": conditions,
                "result": result,
                "status": status,
                "implication": implication,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def residual_bound_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RB4311_0_sum",
            "S_U",
            "S_U := R_U + N_N + N_boundary",
            "collar forcing numerator entering A_U",
            "FORMULA_READY_VALUES_MISSING",
            "source each part; do not collapse physical boundary flux into a single fudge factor",
        ),
        (
            "RB4311_1_AU",
            "A_U",
            "A_U <= C_col S_U / lambda_*",
            "collar amplitude bound from 4310 once lambda_* > 0",
            "GUARDED_BOUND_READY",
            "requires positive lambda_floor_candidate before numerical use",
        ),
        (
            "RB4311_2_Ninner",
            "N_inner",
            "N_inner <= C_N[K_U C_col S_U/lambda_* + R_U] + ||B_src^A||",
            "first reduced trace-defect bound",
            "GUARDED_BOUND_READY_VALUES_MISSING",
            "score only after lambda_*, C_N, K_U, C_col, R_U, S_U and B_src^A are sourced",
        ),
        (
            "RB4311_3_budget",
            "lambda_required",
            "lambda_* >= C_N K_U C_col S_U/(B_inner - C_N R_U - ||B_src^A||) if denominator > 0",
            "minimum lambda floor needed for a chosen trace-defect budget",
            "DERIVED_REQUIREMENT_NO_NUMERIC_BUDGET",
            "use once a local precision budget B_inner is selected",
        ),
        (
            "RB4311_4_residual_split",
            "S_U decomposition",
            "S_U <= R_visible + R_EM_Poynting + R_transition + R_boundary + R_nonHilbert + R_N",
            "honest place to test Poynting/wave/source terms",
            "DECOMPOSITION_READY_VALUES_MISSING",
            "next step can attack EM/Poynting cancellation or source each residual row",
        ),
        (
            "RB4311_5_zero_case",
            "mu_tr",
            "lambda_* > 0 and S_U,R_U,B_src^A -> 0 imply A_U->0, N_inner->0 and mu_tr=0",
            "exact zero law conditional on signed inputs",
            "CONDITIONAL_ZERO_NOT_LIVE",
            "this is the local vacuum plateau route without smuggling a plateau axiom",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for bound_id, symbol, law, role, status, next_action in specs:
        row = base_row()
        row.update(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "law": law,
                "role": role,
                "status": status,
                "next_action": next_action,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RUN4311_0_live_corpus",
            "current corpus rows",
            "BLOCK_CLAIM",
            "lambda formula is derived but Z_min, M2_min, lambda_1(D_loc), Eta_H and residual numerator are unsourced",
            "keep reduced bound as nonclaim scaffold",
        ),
        (
            "RUN4311_1_component_signed",
            "all lambda components source-signed with positive margin",
            "ALLOW_LAMBDA_FLOOR_CONDITIONAL",
            "lambda_floor_candidate can replace lambda_* in the 4310 trace-bound formula",
            "then source residual numerator and constants before local arena scoring",
        ),
        (
            "RUN4311_2_residual_zero",
            "lambda floor positive and S_U,R_U,B_src^A theorem-zero",
            "ALLOW_MU_TR_ZERO_CONDITIONAL",
            "A_U,N_inner,mu_tr vanish on the fixed-collar branch",
            "still must pass R_eq, I_commutator, EM/rest and projection gates for local GR",
        ),
        (
            "RUN4311_3_poynting_open",
            "Poynting/wave flux not proven Hilbert-owned/cancelled in collar",
            "KEEP_RESIDUAL",
            "R_EM_Poynting contributes to S_U or boundary residual rather than disappearing",
            "attack Poynting owner/cancellation next if lambda components stay unsourced",
        ),
        (
            "RUN4311_4_precision",
            "attempt to score WEP/PPN/R10 with placeholder lambda/residual rows",
            "REJECT",
            "order-one local leakage fails precision and no claim-valid source rows exist",
            "no local test pass from 4311",
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


def firewall_rows() -> List[Dict[str, str]]:
    rules = [
        "Do not claim lambda_*>0 merely because the formula has positive-looking terms.",
        "Do not use a Poincare gap unless the collar domain and zero-mode/boundary condition are fixed.",
        "Do not use the mass-only branch unless M2_min and Eta_H are parent-signed in the same normalization.",
        "Do not set EM/Poynting residuals to zero unless they are Hilbert-owned or boundary-cancelled in the collar.",
        "Do not score local GR/Newton/R10/PPN until lambda, residual, source-equality, commutator and projection gates are all closed.",
    ]
    rows: List[Dict[str, str]] = []
    for index, rule in enumerate(rules):
        row = base_row()
        row.update({"firewall_id": f"FW4311_{index}", "rule": rule, "status": "ACTIVE"})
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DEC4311_0_derivation",
            "LAMBDA_POSITIVITY_LAW_DERIVED",
            "lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H follows from the coercive m-lock form plus the collar Poincare/eigenvalue relation.",
            "turn the abstract missing lambda into four concrete source rows",
        ),
        (
            "DEC4311_1_routes",
            "THREE_CLOSURE_ROUTES_IDENTIFIED",
            "Poincare/Dirichlet, mass-only zero-mode, and mixed margin branches are the only honest positivity routes currently available.",
            "try mass-only if the collar has a zero mode; otherwise source domain spectrum",
        ),
        (
            "DEC4311_2_bound",
            "FIRST_COLLAR_RESIDUAL_BOUND_STAGED",
            "The reduced N_inner bound and required-lambda budget are now explicit.",
            "future numeric local tests can use the formula only after sourced rows exist",
        ),
        (
            "DEC4311_3_poynting",
            "POYNTING_IS_NEXT_REAL_RESIDUAL_TARGET_IF_LAMBDA_STALLS",
            "EM/wave flow is not dismissed; it belongs in R_EM_Poynting or boundary flux until Hilbert ownership/cancellation is proven.",
            NEXT_TARGET,
        ),
        (
            "DEC4311_4_claim",
            "NO_LOCAL_CLAIM",
            "This checkpoint improves the derivation ladder but does not close local GR/Newton/R10/PPN.",
            "keep all claim flags false",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for decision_id, result, reason, next_action in specs:
        row = base_row()
        row.update({"decision_id": decision_id, "result": result, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4311_0_lambda_formula", "lambda_* formula", "DERIVED", "exact positivity law is now explicit"),
        ("STAT4311_1_components", "Z_min/M2_min/lambda_1/Eta_H", "UNSOURCED", "no live parent-owned numeric/theorem rows yet"),
        ("STAT4311_2_zero_route", "mu_tr zero", "CONDITIONAL_ONLY", "valid if lambda positive and residual numerator vanishes"),
        ("STAT4311_3_residual_bound", "N_inner bound", "STAGED", "ready as guarded formula, not score-ready"),
        ("STAT4311_4_poynting", "EM/Poynting/wave flow", "OPEN_RESIDUAL_TARGET", "must be owned/cancelled or bounded"),
        ("STAT4311_5_local_GR", "local GR/Newton", "BLOCKED", "stronger ladder, but not a pass"),
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
            "next_target_id": "NT4311_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can Z_min/M2_min/Eta_H be parent-signed, or can the Poynting/EM residual be cancelled or bounded in the collar?",
            "preferred_route": "source/derive the lambda components in one normalization and prove a positive margin",
            "fallback_route": "attack R_EM_Poynting and boundary flux as explicit collar residual terms instead of hiding them",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal_text = f"""# 327 PPC4161 lambda-floor source row or collar residual first bound

Marker: `{MARKER}`

## Decision

`{DECISION}`

4311 turns the missing `lambda_*` into an exact local positivity law rather than another open word.

Start from the collar quadratic form:

```text
a_U[u,u] >= Z_min ||grad u||^2 + M2_min ||u||^2 - Eta_H ||u||^2.
```

On a fixed collar branch with the relevant zero mode removed or controlled:

```text
||grad u||^2 >= lambda_1(D_loc) ||u||^2.
```

Therefore:

```text
a_U[u,u] >= (Z_min lambda_1(D_loc) + M2_min - Eta_H) ||u||^2,
lambda_* := Z_min lambda_1(D_loc) + M2_min - Eta_H.
```

The positivity condition is exactly:

```text
Z_min lambda_1(D_loc) + M2_min > Eta_H.
```

This gives three honest branches: a Poincare/Dirichlet gap, a mass-only zero-mode gap, or a mixed positive margin. The current corpus has the formula, not the sourced component rows.

## Lambda Component Ledger

{md_table(tables["lambda_components"], ["component_id", "symbol", "required_law", "status", "next_action"])}

## Positivity Route Audit

{md_table(tables["positivity"], ["route_id", "route", "conditions", "result", "status"])}

## Collar Residual First Bound

{md_table(tables["residual_bounds"], ["bound_id", "symbol", "law", "status", "next_action"])}

## Runner

{md_table(tables["runner"], ["runner_id", "case", "result", "reason"])}

## Result

The leap forward is narrow but real: `lambda_*` is no longer vague. It is a four-input positivity contract plus a guarded trace-defect bound. No local-GR claim fires until those rows are parent-signed.

Next target: `{NEXT_TARGET}`.
"""
    doc_text = f"""# 4311 - lambda-floor source row or collar residual first bound

## Verdict
- Derived the exact local lambda-floor law: `lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H`.
- Split positivity into three honest routes: Poincare/Dirichlet gap, mass-only zero-mode gap, or mixed margin.
- Staged the first residual/budget bound: `N_inner <= C_N[K_U C_col S_U/lambda_* + R_U] + ||B_src^A||`.
- Kept Poynting/wave flow explicit as `R_EM_Poynting` or boundary flux, not a hidden zero.
- No local-GR/Newton/R10/PPN claim fires.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Lambda Component Ledger
{md_table(tables["lambda_components"], ["component_id", "symbol", "definition", "required_law", "status", "role", "next_action"])}

## Positivity Route Audit
{md_table(tables["positivity"], ["route_id", "route", "conditions", "result", "status", "implication"])}

## Collar Residual First Bound
{md_table(tables["residual_bounds"], ["bound_id", "symbol", "law", "role", "status", "next_action"])}

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

    add("VAL4311_0_sources_exist", "all cited local source paths exist", all(Path(row["source_path"]).exists() for row in tables["sources"]), "source_register")
    add("VAL4311_1_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4311_2_lambda_formula", "lambda_* formula row exists", any(row["component_id"] == "LC4311_4_lambda_star" for row in tables["lambda_components"]), "lambda_components")
    add("VAL4311_3_components_unsourced", "lambda component rows remain unsourced/nonclaim", all(row["score_ready"] == "False" for row in tables["lambda_components"]), "lambda_components")
    add("VAL4311_4_three_routes", "three positivity closure routes plus failure route exist", len(tables["positivity"]) == 4, "positivity")
    add("VAL4311_5_budget_bound", "required lambda budget formula staged", any(row["bound_id"] == "RB4311_3_budget" for row in tables["residual_bounds"]), "residual_bounds")
    add("VAL4311_6_poynting_explicit", "Poynting residual is explicit, not hidden", any("Poynting" in row["law"] for row in tables["residual_bounds"]), "residual_bounds")
    add("VAL4311_7_runner_blocks_live_claim", "live corpus runner blocks claim", any(row["runner_id"] == "RUN4311_0_live_corpus" and row["result"] == "BLOCK_CLAIM" for row in tables["runner"]), "runner")
    add("VAL4311_8_next_selected", f"next target is {NEXT_TARGET}", tables["next"][0]["next_target"] == NEXT_TARGET, "next")
    add(
        "VAL4311_9_claim_flags_false",
        "all generated rows keep claim flags false",
        all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for table in tables.values() for row in table),
        "generated_tables",
    )
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4311_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4311_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "generated_docs")
    add("VAL4311_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims_register")
    add("VAL4311_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "unification_spine")
    add("VAL4311_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "private_packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4311_SOURCE_REGISTER.csv",
        "lambda_components": SOURCE_DIR / "P8_Y5_R2FR_4311_LAMBDA_COMPONENT_LEDGER.csv",
        "positivity": SOURCE_DIR / "P8_Y5_R2FR_4311_POSITIVITY_ROUTE_AUDIT.csv",
        "residual_bounds": SOURCE_DIR / "P8_Y5_R2FR_4311_COLLAR_RESIDUAL_FIRST_BOUND.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4311_LAMBDA_BUDGET_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4311_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4311_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4311_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4311_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "lambda_components": lambda_component_rows(),
        "positivity": positivity_route_rows(),
        "residual_bounds": residual_bound_rows(),
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
## PPC4161 4311 lambda-floor source row or collar residual first bound

Marker: `{MARKER}`

4311 derives the local positivity contract for the collar trace-defect route: `lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H`, with Poincare/Dirichlet, mass-only and mixed-margin closure branches. The formula is now exact, but the component rows remain unsourced; therefore the first honest local bound is guarded: `N_inner <= C_N[K_U*C_col*S_U/lambda_* + R_U]+||B_src^A||`, with `S_U` retaining visible, EM/Poynting, transition, boundary, non-Hilbert and nonlinear residual pieces.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4311 packet lambda-floor contract

Marker: `{PACKET_MARKER}`

Packet update: the local branch has a sharper contract, not a plateau axiom. Close `Z_min`, `lambda_1(D_loc)`, `M2_min` and `Eta_H`, or explicitly bound/cancel the collar residual numerator including EM/Poynting flow. No local arena claim is allowed from placeholder lambda or residual rows.
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
