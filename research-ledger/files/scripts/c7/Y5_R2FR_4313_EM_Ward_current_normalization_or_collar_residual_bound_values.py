from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4313"
CLAIM_ID = "L-154"
BRANCH = "MTS_R2FR_Y5_EM_WARD_CURRENT_NORMALIZATION_OR_COLLAR_RESIDUAL_BOUND_VALUES_4313"
DECISION = "EM_WARD_CURRENT_OWNER_THEOREM_DERIVED_CURRENT_MISMATCH_BOUND_STAGED_NONCLAIM"
MARKER = "PPC4161_EM_WARD_CURRENT_NORMALIZATION_OR_COLLAR_RESIDUAL_BOUND_VALUES_4313"
PACKET_MARKER = "PPC4161_PACKET_EM_WARD_CURRENT_NORMALIZATION_OR_COLLAR_RESIDUAL_BOUND_VALUES_4313"
NEXT_TARGET = "4314-Y5-R2FR-radiative-Poynting-no-flux-or-boundary-flux-row.md"

FORMAL_PATH = FORMAL / "329-PPC4161-EM-Ward-current-normalization-or-collar-residual-bound-values.md"
DOC_PATH = POST / "4313-Y5-R2FR-EM-Ward-current-normalization-or-collar-residual-bound-values.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4313_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4313_00_4312_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4312_NEXT_TARGET.csv",
        "4313-Y5-R2FR-EM-Ward-current-normalization-or-collar-residual-bound-values.md",
        "4312 handoff selecting EM current/Ward normalization.",
    ),
    "SRC4313_01_4312_defects": (
        SOURCE_DIR / "P8_Y5_R2FR_4312_EM_DEFECT_LEDGER.csv",
        "Delta_internal_exchange",
        "4312 defect row for unmatched matter-EM exchange.",
    ),
    "SRC4313_02_4312_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4312_COLLAR_EM_RESIDUAL_BOUND.csv",
        "R_EM_Poynting <=",
        "4312 EM/Poynting residual bound receiving current/Ward terms.",
    ),
    "SRC4313_03_191_ward": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "nabla_mu T_EM^mu_nu = -F_nu_lambda J^lambda",
        "Maxwell-Hodge stress owner Ward exchange identity.",
    ),
    "SRC4313_04_4207_owner": (
        SOURCE_DIR / "P8_Y5_R2FR_4207_POYNTING_OWNER_CHAIN.csv",
        "nabla_mu T_EM",
        "4207 source-backed owner-chain Ward exchange row.",
    ),
    "SRC4313_05_225_norm": (
        FORMAL / "225-PPC4161-Maxwell-normalization-charge-current-owner.md",
        "b_alpha = D_X ln alpha_eff",
        "Maxwell normalization identity and no fake alpha derivation.",
    ),
    "SRC4313_06_278_readout": (
        FORMAL / "278-PPC4161-visible-EM-readout-guard-or-charge-normalization-bound.md",
        "C_JQ = 0",
        "calibrated q-basic visible-EM branch kills current/readout drift conditionally.",
    ),
    "SRC4313_07_3508_current": (
        SOURCE_DIR / "P8_EM_current_source_Ward_alpha_source_residual.csv",
        "z_g=D_X ln g_J",
        "current/source Ward alpha-source residual ledger.",
    ),
    "SRC4313_08_319_silence": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "J_EM_to_m=0",
        "visible Hilbert EM current silence in m equation if owner branch is signed.",
    ),
    "SRC4313_09_309_precision": (
        FORMAL / "309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md",
        "order-one projection of epsilon_AJ_seed into local observables fails",
        "local precision forbids unbounded current-normalization leakage.",
    ),
    "SRC4313_10_newton_guard": (
        POST / "1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md",
        "R_eq",
        "source-to-Newton equality guard remains open.",
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
        "em_local_gr",
        (
            "4313 derives the EM Ward/current-owner gate needed after the 4312 Poynting split. If the matter "
            "action and Maxwell-Hodge action use the same observed Hodge structure and the same normalized current, "
            "then div T_EM=-FJ and div T_matter=+FJ cancel in the total Hilbert source, giving "
            "Delta_internal_exchange=0 and C_JQ=0 on the calibrated q-basic visible branch. If the currents differ, "
            "the surviving force is not handwaved: Delta_Ward^nu = F^{nu lambda}(J_matter-J_Maxwell)_lambda plus "
            "Hodge, charge-normalization and boundary terms, with a collar dual bound feeding R_EM_Poynting, Eta_H "
            "and S_U. This is a source-coupling derivation step only; local GR/Newton/R10/PPN claims remain blocked."
        ),
        (
            "4313 source register, Ward current theorem, current normalization contract, internal exchange bound, "
            "defect reduction, collar update, runner, firewall, status, next-target and validation CSV."
        ),
        "private_EM_Ward_current_owner_theorem_mismatch_bound_nonclaim",
        (
            "Parent-sign one matter+EM current before readout, or fill numeric bounds for delta_J, C_JQ, b_alpha, "
            "Delta_internal_exchange and radiative boundary flux."
        ),
        (
            "Using Ward conservation to prove absence of source channels without current equality, deriving alpha_EM "
            "from field normalization, moving current drift into readout after variation, or claiming local GR/Newton "
            "while lambda, boundary flux and source-equality gates remain open."
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


def ward_theorem_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "WT4313_0_parent_action",
            "single matter+EM action",
            "S_vis = S_MH[A,g_obs;lambda_A] + S_matter[psi,A,g_obs;theta_Q]",
            "one variational source owner before readout",
            "CONTRACT_FORM_READY_NOT_GLOBAL_PARENT_SIGNED",
        ),
        (
            "WT4313_1_maxwell_current",
            "Maxwell current",
            "J_Maxwell^nu := nabla_mu(lambda_A F^{mu nu}) in the same Hodge/normalization",
            "current appearing in div T_EM",
            "DEFINITION_READY",
        ),
        (
            "WT4313_2_matter_current",
            "matter current",
            "J_matter^nu := (1/sqrt(-g)) delta S_matter / delta A_nu",
            "current appearing in Lorentz force on matter",
            "DEFINITION_READY",
        ),
        (
            "WT4313_3_exchange_identity",
            "Ward exchange",
            "nabla_mu T_EM^{mu nu} = -F^{nu lambda}J_Maxwell_lambda and nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_matter_lambda",
            "total exchange cancels if J_matter=J_Maxwell",
            "STANDARD_IDENTITY_IMPORTED_CONDITIONALLY",
        ),
        (
            "WT4313_4_zero_theorem",
            "internal exchange zero",
            "J_matter=J_Maxwell, same Hodge, fixed calibrated charge/current and no boundary current leakage imply Delta_internal_exchange=0",
            "R_EM_Poynting loses the Ward/current mismatch term",
            "EXACT_ZERO_IF_CLAUSES_PARENT_SIGNED",
        ),
        (
            "WT4313_5_failure_theorem",
            "mismatch residual",
            "Delta_Ward^nu = F^{nu lambda}(J_matter-J_Maxwell)_lambda + R_Hodge^nu + R_Q^nu + B_J^nu",
            "current mismatch becomes explicit collar residual",
            "BOUND_ROUTE_IF_NOT_SIGNED",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for theorem_id, clause, statement, result, status in specs:
        row = base_row()
        row.update(
            {
                "theorem_id": theorem_id,
                "clause": clause,
                "statement": statement,
                "result": result,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def normalization_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "CN4313_0_alpha_identity",
            "alpha_eff",
            "alpha_eff proportional to g_J^2/lambda_A",
            "b_alpha = 2 D_X ln g_J - D_X ln lambda_A",
            "identity only; not an alpha_EM prediction",
            "EXACT_IDENTITY_NONCLAIM",
        ),
        (
            "CN4313_1_fixed_visible_branch",
            "calibrated q-basic EM constants",
            "D_X ln g_J=0 and D_X ln lambda_A=0 when g_J, lambda_A, charges and readout labels are fixed before variation",
            "b_alpha=0, C_JQ=0 on this branch",
            "safe calibrated visible local-GR branch",
            "CONDITIONAL_ZERO_ROUTE",
        ),
        (
            "CN4313_2_current_multiplier",
            "C_JQ",
            "J_matter=(1+C_JQ)J_Maxwell + delta J_perp",
            "current mismatch contribution is F(C_JQ J_Maxwell + delta J_perp)",
            "enters R_EM_Poynting, WEP/source and clock residuals",
            "BOUND_IF_NOT_ZERO",
        ),
        (
            "CN4313_3_dynamic_EM_branch",
            "dynamic g_J/lambda_A",
            "g_J(Phi), lambda_A(Phi) or charge labels before variation make b_alpha and C_JQ physical",
            "no readout convention may remove the residual",
            "global MTS EM derivation remains open",
            "DEFORMATION_TAX_RETAINED",
        ),
        (
            "CN4313_4_no_fake_alpha",
            "absolute alpha_EM",
            "classical U(1)/Noether owns conservation and relative labels but not the numerical value of alpha_EM",
            "visible EM may be calibrated; deviations must be bounded",
            "prevents false precision claim",
            "NO_GO_RETAINED",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for contract_id, item, condition, formula, implication, status in specs:
        row = base_row()
        row.update(
            {
                "contract_id": contract_id,
                "item": item,
                "condition": condition,
                "formula": formula,
                "implication": implication,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def exchange_bound_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "EB4313_0_deltaJ",
            "delta J",
            "delta J := J_matter - J_Maxwell",
            "||Delta_Ward||_dual <= ||F||_inf ||delta J||_dual + ||R_Hodge|| + ||R_Q|| + ||B_J||",
            "primary internal-exchange bound",
        ),
        (
            "EB4313_1_CJQ",
            "C_JQ",
            "if delta J = C_JQ J_Maxwell + delta J_perp",
            "||Delta_Ward||_dual <= ||F||_inf(|C_JQ| ||J_Maxwell||_dual + ||delta J_perp||_dual)+...",
            "charge/current multiplier bound",
        ),
        (
            "EB4313_2_balpha",
            "b_alpha",
            "b_alpha = 2D ln g_J - D ln lambda_A",
            "|b_alpha| contributes to source normalization/clock/EM residual if dynamic",
            "normalization drift bound",
        ),
        (
            "EB4313_3_zero",
            "Delta_internal_exchange",
            "same current plus same Hodge plus calibrated constants plus no boundary current leakage",
            "Delta_internal_exchange=0",
            "exact conditional cancellation",
        ),
        (
            "EB4313_4_R_EM_update",
            "R_EM_Poynting",
            "substitute the Ward/current mismatch into the 4312 EM residual",
            "R_EM_Poynting <= R_EM_noWard + ||F||_inf(|C_JQ| ||J|| + ||delta J_perp||) + ||R_Q|| + ||B_J||",
            "feeds 4312 residual bound",
        ),
        (
            "EB4313_5_EtaH_update",
            "Eta_H",
            "current mismatch contributes to the negative/correction budget in the lambda floor",
            "Eta_H >= Eta_H_noWard + C_Ward[||F||_inf(|C_JQ| ||J||+||delta J_perp||)+||R_Q||+||B_J||]",
            "weakens lambda_* unless the current gate closes",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for bound_id, symbol, premise, bound, role in specs:
        row = base_row()
        row.update(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "premise": premise,
                "bound": bound,
                "role": role,
                "status": "FORMULA_READY_VALUES_MISSING",
                "source_path": "",
                "numeric_value": "",
                "units": "collar dual/source-normalized units",
                "next_action": "parent-sign the zero route or fill this bound with sourced collar units",
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def defect_reduction_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DR4313_0_C_JQ",
            "C_JQ",
            "zero if g_J/charge/current lattice is fixed q-basic before variation",
            "current mismatch bound if not fixed",
            "PARTLY_REDUCED_TO_BRANCH_THEOREM",
        ),
        (
            "DR4313_1_Delta_internal_exchange",
            "Delta_internal_exchange",
            "zero if J_matter=J_Maxwell and Ward exchange is one-action owned",
            "F deltaJ plus Hodge/charge/boundary terms if not",
            "PARTLY_REDUCED_TO_CURRENT_EQUALITY",
        ),
        (
            "DR4313_2_delta_w_EM",
            "delta_w_EM",
            "zero on source-label-forgetting Hilbert branch",
            "species/readout weight residual if prevariation source weights exist",
            "RETAINED",
        ),
        (
            "DR4313_3_Delta_rad_Poynting",
            "Delta_rad_Poynting",
            "not solved by Ward current equality",
            "must route to no-flux/boundary row next",
            "NEXT_FRONTIER",
        ),
        (
            "DR4313_4_Delta_Hodge_EM",
            "Delta_Hodge_EM",
            "not solved by current equality unless same-Hodge owner also signed",
            "stays in R_Hodge/Eta_H",
            "RETAINED",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for reduction_id, defect, zero_route, fallback, status in specs:
        row = base_row()
        row.update(
            {
                "reduction_id": reduction_id,
                "defect": defect,
                "zero_route": zero_route,
                "fallback": fallback,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RUN4313_0_current_corpus",
            "current corpus",
            "BOUND_ROUTE_ONLY",
            "Ward identity exists and current-zero branch is clean, but global parent current equality is not signed for every branch",
            "retain deltaJ/C_JQ/Delta_internal_exchange bound rows",
        ),
        (
            "RUN4313_1_calibrated_visible",
            "4210/4262 calibrated q-basic visible EM branch",
            "ALLOW_CJQ_ZERO_CONDITIONAL",
            "fixed charges, g_J, lambda_A and readout labels give C_JQ=0 and b_alpha=0 inside that branch",
            "still needs boundary radiative flux and lambda gates before local tests",
        ),
        (
            "RUN4313_2_same_action_current",
            "same matter+EM action and same current",
            "ALLOW_DELTA_INTERNAL_EXCHANGE_ZERO_CONDITIONAL",
            "Lorentz force exchange cancels in total Hilbert stress",
            "then R_EM_Poynting can drop Ward/current mismatch term",
        ),
        (
            "RUN4313_3_dynamic_or_mismatch",
            "dynamic current/coupling or mismatched current",
            "KEEP_RESIDUAL",
            "deltaJ, C_JQ and b_alpha are physical residuals",
            "source numeric bounds before scoring local arenas",
        ),
        (
            "RUN4313_4_local_claim",
            "claim local GR/Newton/R10/PPN now",
            "REJECT",
            "lambda components, radiative boundary flux, source equality, I_commutator and projection gates remain open",
            "continue source-coupling derivation",
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
            "DEC4313_0_ward",
            "WARD_EXCHANGE_CAN_CANCEL_EXACTLY",
            "If the same current appears in Maxwell and matter variations, EM/matter Lorentz exchange is internal and Delta_internal_exchange=0.",
            "use the zero route only when current equality is parent-signed",
        ),
        (
            "DEC4313_1_current",
            "CURRENT_MISMATCH_HAS_A_BOUND",
            "If currents differ, the surviving residual is F deltaJ plus Hodge, charge and boundary terms.",
            "feed the bound into R_EM_Poynting, Eta_H and S_U",
        ),
        (
            "DEC4313_2_normalization",
            "NO_FAKE_ALPHA_OR_CHARGE_DERIVATION",
            "alpha_eff is g_J^2/lambda_A; calibrated visible EM is allowed, but absolute alpha_EM is not predicted here.",
            "keep dynamic current/coupling deviations as residuals",
        ),
        (
            "DEC4313_3_frontier",
            "RADIATIVE_BOUNDARY_FLUX_NOW_SHARPEST_EM_GATE",
            "After current equality, the remaining EM gate with teeth is net Poynting flux through the collar.",
            NEXT_TARGET,
        ),
        (
            "DEC4313_4_claim",
            "NO_LOCAL_CLAIM",
            "4313 improves source coupling but does not close the full local-GR reduction.",
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
        "Do not use Ward conservation to prove EM residual absence unless J_matter equals J_Maxwell in one normalization.",
        "Do not derive the numerical fine-structure constant from field normalization.",
        "Do not move a prevariation current/coupling drift into harmless postvariation readout.",
        "Do not set radiative Poynting flux to zero from current equality alone.",
        "Do not claim local GR/Newton/R10/PPN from current-owner cancellation alone.",
    ]
    rows: List[Dict[str, str]] = []
    for index, rule in enumerate(rules):
        row = base_row()
        row.update({"firewall_id": f"FW4313_{index}", "rule": rule, "status": "ACTIVE"})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4313_0_Ward", "Ward exchange", "EXACT_CONDITIONAL", "cancels only with same current and same Hodge owner"),
        ("STAT4313_1_CJQ", "C_JQ", "ZERO_OR_BOUND", "zero in calibrated q-basic branch; bound if dynamic/mismatched"),
        ("STAT4313_2_deltaJ", "delta J", "NEW_BOUND_OBJECT", "direct current mismatch norm feeding EM residual"),
        ("STAT4313_3_balpha", "b_alpha", "IDENTITY_NOT_PREDICTION", "no fake alpha derivation"),
        ("STAT4313_4_RadFlux", "Delta_rad_Poynting", "NEXT_OPEN_GATE", "not solved by current equality"),
        ("STAT4313_5_local", "local GR/Newton", "BLOCKED", "source coupling narrowed, full reduction still open"),
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
            "next_target_id": "NT4313_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can net radiative Poynting flux through the local collar be zeroed by no-flux/compact support, or must it be bounded as N_boundary?",
            "preferred_route": "derive closed-collar/no-through-EM-flux theorem in the same Hilbert owner branch",
            "fallback_route": "fill a nonclaim boundary-flux row Phi_rad = int_boundary S_Poynting dot n dA with units and source path",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal_text = f"""# 329 PPC4161 EM Ward current normalization or collar residual bound values

Marker: `{MARKER}`

## Decision

`{DECISION}`

4313 closes the logical gap between "Poynting is Hilbert-owned" and "the EM current does not leak as a source." The exact theorem target is:

```text
J_matter = J_Maxwell
same Hodge owner
fixed calibrated charge/current normalization
=> Delta_internal_exchange = 0.
```

The failure branch is equally exact:

```text
Delta_Ward^nu =
  F^(nu lambda)(J_matter-J_Maxwell)_lambda
  + R_Hodge^nu + R_Q^nu + B_J^nu.
```

So the collar dual bound is:

```text
||Delta_Ward|| <= ||F||_inf ||delta J|| + ||R_Hodge|| + ||R_Q|| + ||B_J||.
```

If `delta J = C_JQ J_Maxwell + delta J_perp`, then:

```text
||Delta_Ward|| <= ||F||_inf(|C_JQ| ||J_Maxwell|| + ||delta J_perp||)
               + ||R_Hodge|| + ||R_Q|| + ||B_J||.
```

This feeds `R_EM_Poynting`, `Eta_H`, and `S_U`.

## Ward Current Theorem

{md_table(tables["ward"], ["theorem_id", "clause", "statement", "result", "status"])}

## Current Normalization Contract

{md_table(tables["normalization"], ["contract_id", "item", "condition", "formula", "status"])}

## Internal Exchange Bound

{md_table(tables["bounds"], ["bound_id", "symbol", "premise", "bound", "role"])}

## Defect Reduction

{md_table(tables["defect_reduction"], ["reduction_id", "defect", "zero_route", "fallback", "status"])}

## Runner

{md_table(tables["runner"], ["runner_id", "case", "result", "reason"])}

## Result

The Ward/current gate is now an exact zero-or-bound object. Current equality can remove `Delta_internal_exchange`; it cannot remove radiative collar flux or replace the missing lambda/source-equality gates.

Next target: `{NEXT_TARGET}`.
"""
    doc_text = f"""# 4313 - EM Ward current normalization or collar residual bound values

## Verdict
- Derived the exact Ward/current cancellation condition: same current in Maxwell and matter variations gives `Delta_internal_exchange=0`.
- Derived the fallback bound: `Delta_Ward = F deltaJ + R_Hodge + R_Q + B_J`.
- Split `deltaJ` into `C_JQ J_Maxwell + deltaJ_perp`, so charge/current drift has a concrete collar bound.
- Preserved the no-fake-alpha rule: `alpha_eff` is controlled by `g_J^2/lambda_A`, but this does not predict numerical `alpha_EM`.
- No local-GR/Newton/R10/PPN claim fires.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Ward Current Theorem
{md_table(tables["ward"], ["theorem_id", "clause", "statement", "result", "status"])}

## Current Normalization Contract
{md_table(tables["normalization"], ["contract_id", "item", "condition", "formula", "implication", "status"])}

## Internal Exchange Bound
{md_table(tables["bounds"], ["bound_id", "symbol", "premise", "bound", "role", "status", "next_action"])}

## Defect Reduction
{md_table(tables["defect_reduction"], ["reduction_id", "defect", "zero_route", "fallback", "status"])}

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

    add("VAL4313_0_sources_exist", "all cited local source paths exist", all(Path(row["source_path"]).exists() for row in tables["sources"]), "source_register")
    add("VAL4313_1_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4313_2_zero_theorem", "Ward current zero theorem exists", any(row["theorem_id"] == "WT4313_4_zero_theorem" for row in tables["ward"]), "ward")
    add("VAL4313_3_failure_bound", "Ward failure residual formula exists", any(row["theorem_id"] == "WT4313_5_failure_theorem" for row in tables["ward"]), "ward")
    add("VAL4313_4_CJQ_bound", "C_JQ current multiplier bound exists", any(row["bound_id"] == "EB4313_1_CJQ" for row in tables["bounds"]), "bounds")
    add("VAL4313_5_no_fake_alpha", "no fake alpha clause retained", any(row["contract_id"] == "CN4313_4_no_fake_alpha" for row in tables["normalization"]), "normalization")
    add("VAL4313_6_radiative_next", "radiative flux selected as next frontier", tables["next"][0]["next_target"] == NEXT_TARGET, "next")
    add("VAL4313_7_runner_rejects_claim", "runner rejects local claim from current gate alone", any(row["runner_id"] == "RUN4313_4_local_claim" and row["result"] == "REJECT" for row in tables["runner"]), "runner")
    add(
        "VAL4313_8_claim_flags_false",
        "all generated rows keep claim flags false",
        all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for table in tables.values() for row in table),
        "generated_tables",
    )
    add(
        "VAL4313_9_score_flags_false",
        "all score rows remain unscored/nonclaim",
        all(row.get("score_ready", "False") == "False" for table in tables.values() for row in table),
        "generated_tables",
    )
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4313_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4313_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "generated_docs")
    add("VAL4313_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims_register")
    add("VAL4313_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "unification_spine")
    add("VAL4313_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "private_packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4313_SOURCE_REGISTER.csv",
        "ward": SOURCE_DIR / "P8_Y5_R2FR_4313_EM_WARD_CURRENT_THEOREM.csv",
        "normalization": SOURCE_DIR / "P8_Y5_R2FR_4313_CURRENT_NORMALIZATION_CONTRACT.csv",
        "bounds": SOURCE_DIR / "P8_Y5_R2FR_4313_INTERNAL_EXCHANGE_BOUND.csv",
        "defect_reduction": SOURCE_DIR / "P8_Y5_R2FR_4313_DEFECT_REDUCTION.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4313_LOCAL_ROUTE_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4313_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4313_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4313_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4313_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "ward": ward_theorem_rows(),
        "normalization": normalization_rows(),
        "bounds": exchange_bound_rows(),
        "defect_reduction": defect_reduction_rows(),
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
## PPC4161 4313 EM Ward current normalization or collar residual bound values

Marker: `{MARKER}`

4313 turns EM current ownership into an exact zero-or-bound gate. If the Maxwell and matter variations share the same normalized current in the same Hodge geometry, the Lorentz exchange cancels internally and `Delta_internal_exchange=0`. If not, the residual is `Delta_Ward^nu = F^(nu lambda)(J_matter-J_Maxwell)_lambda + R_Hodge^nu + R_Q^nu + B_J^nu`, bounded in the collar and fed to `R_EM_Poynting`, `Eta_H`, and `S_U`. The calibrated visible branch may set `C_JQ=b_alpha=0`, but this is not a prediction of `alpha_EM`.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4313 packet EM Ward/current owner

Marker: `{PACKET_MARKER}`

Packet update: EM current normalization is now a concrete gate. Same current plus same Hodge owner gives zero internal exchange; otherwise `deltaJ`, `C_JQ`, `b_alpha`, Hodge drift and boundary-current leakage are retained as collar residual terms.
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
