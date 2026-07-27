from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4304"
CLAIM_ID = "L-145"
BRANCH = "MTS_R2FR_Y5_FIRST_SOURCE_NORMS_OR_VISIBLE_HILBERT_M_LOCK_SIGNATURE_4304"
DECISION = "VISIBLE_HILBERT_SIGNATURE_CONDITIONAL_SOURCE_POWER_ANCHOR_IMPORTED_FIRST_NORM_ROWS_STAGED_NONCLAIM"
MARKER = "PPC4161_FIRST_SOURCE_NORMS_OR_VISIBLE_HILBERT_M_LOCK_SIGNATURE_4304"
PACKET_MARKER = "PPC4161_PACKET_FIRST_SOURCE_NORMS_OR_VISIBLE_HILBERT_M_LOCK_SIGNATURE_4304"
NEXT_TARGET = "4305-Y5-R2FR-source-power-amplitude-or-inner-charge-bound-runner.md"

FORMAL_PATH = FORMAL / "320-PPC4161-first-source-norms-or-visible-Hilbert-m-lock-signature.md"
DOC_PATH = POST / "4304-Y5-R2FR-fill-first-source-norms-or-parent-sign-visible-Hilbert-m-lock-silence.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4304_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
U_B_STRONG = "3.7965595357794454e-7"
U_B2_STRONG = "1.4413864308717837e-13"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4304_00_4303_formal": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "Next target: `4304-Y5-R2FR-fill-first-source-norms-or-parent-sign-visible-Hilbert-m-lock-silence.md`.",
        "4303 handoff: parent-sign visible Hilbert m-silence or fill first source norm rows.",
    ),
    "SRC4304_01_4303_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4303_VISIBLE_HILBERT_M_LOCK_SILENCE_THEOREM.csv",
        "VHS4303_0_action_split",
        "conditional visible-Hilbert source silence theorem.",
    ),
    "SRC4304_02_4303_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4303_COMPONENT_ZERO_NORM_MATRIX.csv",
        "CM4303_2_screened_source",
        "N_src, N_inner and N_EM component slots.",
    ),
    "SRC4304_03_1538_nsrc": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1538_N_SRC_THEOREM_OR_BOUND.csv",
        "NSRC1538_4_finite_bound",
        "first source-support theorem-or-bound row.",
    ),
    "SRC4304_04_1538_ninner": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1538_N_INNER_THEOREM_OR_BOUND.csv",
        "NINNER1538_4_finite_bound",
        "inner compact-source theorem-or-bound row.",
    ),
    "SRC4304_05_123_power": (
        FORMAL / "123-local-source-power-theorem.md",
        "U_B S_cg order = 1.4413864308717837e-13",
        "older local source-power anchor; explicitly not parent-derived.",
    ),
    "SRC4304_06_210_jres_power": (
        FORMAL / "210-PPC4161-source-support-powers-for-Jres.md",
        "U_B S_cg = O(U_B^2),",
        "newer J_res consolidation of source-support power.",
    ),
    "SRC4304_07_211_parity": (
        FORMAL / "211-PPC4161-parent-ZL-parity-signature.md",
        "J_res,bulk = O(U_B^2).",
        "parity/evenness route for quadratic bulk source scaling.",
    ),
    "SRC4304_08_214_amplitude_owner": (
        FORMAL / "214-PPC4161-parent-amplitude-owner-for-Jres.md",
        "A_J,eff = A_src + A_lap + A_drift + A_boundary/U_B^2.",
        "source amplitude owner decomposition.",
    ),
    "SRC4304_09_215_AJ_bound": (
        FORMAL / "215-PPC4161-source-operator-amplitude-AJ-bound.md",
        "A_J,eff <= C_D C_S",
        "source-operator amplitude bound contract.",
    ),
    "SRC4304_10_3340_hilbert": (
        POST / "3340-Y5-R2FR-parent-Hilbert-source-clause-or-finite-residual-vector-under-AX1090.md",
        "HSC3340_4_public_Maxwell_Hodge",
        "Maxwell/Hodge/Poynting Hilbert source clause.",
    ),
    "SRC4304_11_3523_poynting": (
        POST / "3523-Y5-R2FR-source-label-forgetting-functor-and-EM-Hodge-owner-or-marker-kernel-bound.md",
        "DER3523_2_public_Maxwell_Poynting_lock",
        "Poynting as Maxwell Hilbert stress when owner clauses close.",
    ),
    "SRC4304_12_3524_composite": (
        POST / "3524-Y5-R2FR-observed-stack-and-charge-lattice-parent-owner-or-local-source-kernel-values.md",
        "COT3524_0_shared_owner_theorem",
        "composite observed-stack source owner theorem.",
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
            "4304 tries the 4303 fork rather than only listing it. The visible Hilbert/m-lock silence "
            "signature remains conditional, not globally parent-signed, but it is now written as an explicit "
            "parent-action contract. The first source norm is also no longer empty: the existing source-power "
            "work gives a private nonclaim anchor N_src,strong <= U_B^2 A_src with U_B=3.7965595357794454e-7 "
            "and U_B^2=1.4413864308717837e-13. This anchor is useful only if A_src and the source covariance "
            "clauses are parent-owned; N_inner and N_EM remain separate nonnegative residual rows."
        ),
        (
            "4304 source register, visible-Hilbert signature audit, first norm value rows, source-power anchor "
            "import, Npair-to-Cquad runner, decision, firewall, status, next-target and validation CSV."
        ),
        "private_visible_Hilbert_signature_conditional_first_Nsrc_anchor_staged_nonclaim",
        (
            "Parent-sign the source-power amplitude A_src or source real finite values for A_src, C_inner, "
            "Q_m^H and N_EM; then feed N_pair into lambda_m and C4302_DVGAMMA_QUAD."
        ),
        (
            "Treating U_B^2 as a claimable local-GR pass, setting A_src=1 as physics rather than a smoke "
            "normalization, cancelling source and boundary norms, or using visible-Hilbert silence to erase "
            "non-Hilbert source support."
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


def visible_signature_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "VHSIG4304_0_parent_split",
            "S_parent splits into S_lock[m,q]+S_vis[g_obs(q),psi,A]+S_EM[g_obs(q),A]+S_boundary",
            "4303/3340/3524 give a conditional branch, not a global parent action signature.",
            "False",
            "BRANCH_CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "Need parent action where visible and Maxwell sectors have no direct m slot before readout.",
        ),
        (
            "VHSIG4304_1_variation_order",
            "m-lock variation is taken at fixed q/g_obs before calibration/readout",
            "Required by 4303 theorem; current corpus keeps it as conditional.",
            "False",
            "CONDITIONAL_THEOREM_INPUT",
            "Need parent-owned order of variation and observed-stack functor.",
        ),
        (
            "VHSIG4304_2_Maxwell_Poynting",
            "Poynting is S^a=-h^a_mu T_EM^{mu nu}u_nu from the same Maxwell Hilbert stress",
            "3523/3340 support the route if Hodge, current lattice and gauge normalization are q-owned.",
            "False",
            "CONDITIONAL_EM_SILENCE_ELSE_NEM",
            "Need hidden F2/Hodge/current closure or a numeric N_EM residual.",
        ),
        (
            "VHSIG4304_3_no_hidden_slots",
            "No independent f(m,X)F^2, source-label drift, hidden Hodge drift, or species marker coupling",
            "The corpus has guards and residual labels; it does not globally delete these slots.",
            "False",
            "RESIDUAL_ROWS_RETAINED",
            "Need no-hidden-slot theorem or bounds for b_alpha, delta_J, delta_star and Delta_Hodge_EM.",
        ),
        (
            "VHSIG4304_4_result",
            "delta S_visible/delta m = 0 is usable only inside the signed visible-Hilbert branch",
            "This can zero ordinary visible matter and EM/Poynting in the m equation, not non-Hilbert source support.",
            "False",
            "NO_GLOBAL_SOURCE_SILENCE_CLAIM",
            "Feed remaining source norms into N_pair and C4302 unless parent signature closes.",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for signature_id, required_clause, current_evidence, parent_signed, result, missing_input in specs:
        row = base_row()
        row.update(
            {
                "signature_id": signature_id,
                "required_clause": required_clause,
                "current_evidence": current_evidence,
                "parent_signed": parent_signed,
                "result": result,
                "missing_input": missing_input,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def first_norm_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "FN4304_0_Nvisible_zero",
            "N_visible_matter",
            "0",
            "",
            "dimensionless lock-dual norm",
            "visible Hilbert branch only",
            "CONDITIONAL_ZERO_NOT_GLOBAL",
            "Ordinary matter stress remains in T_munu for GR/Newton readout; it is only silent in the m-lock equation.",
        ),
        (
            "FN4304_1_NEM_zero_or_bound",
            "N_EM",
            "0 if Maxwell/Hodge/Poynting owner clauses close; otherwise |b_alpha|+|delta_J|+|delta_star|+||Delta_Hodge_EM||+|Phi_Poynting_unclosed|",
            "",
            "dimensionless lock-dual norm",
            "4303/3340/3523 conditional route",
            "ZERO_OR_RESIDUAL_BOUND_REQUIRED",
            "Do not double-count Poynting as a second force; either Hilbert EM stress or a boundary/source residual.",
        ),
        (
            "FN4304_2_Nsrc_power_anchor",
            "N_src,strong_anchor",
            "N_src <= U_B^2 A_src",
            U_B2_STRONG,
            "dimensionless lock-dual norm times A_src",
            "123/210/211 source-power route",
            "FIRST_NUMERIC_ANCHOR_NONCLAIM",
            "This is the first filled source-support scale, but A_src and source covariance are not parent-owned.",
        ),
        (
            "FN4304_3_Nsrc_formula",
            "N_src",
            "N_src <= U_B_max S_cg_norm; under parity/source-power branch S_cg_norm <= U_B A_src",
            "",
            "dimensionless lock-dual norm",
            "1538 finite row plus 210/211 power reduction",
            "FORMULA_PLUS_CONDITIONAL_ANCHOR",
            "Needs A_src or a theorem-zero for source support before it becomes claimable.",
        ),
        (
            "FN4304_4_Ninner_formula",
            "N_inner",
            "N_inner <= C_inner |Q_m^H|",
            "",
            "boundary-dual norm",
            "1538 inner charge row",
            "FORMULA_ONLY_INPUTS_MISSING",
            "Still needs C_inner and Q_m^H, or a parent no-inner-charge/no-flux theorem.",
        ),
        (
            "FN4304_5_Npair_anchor",
            "N_pair",
            "N_pair <= U_B^2 A_src + C_inner |Q_m^H| + N_EM + N_drift + N_history + N_boundary",
            "",
            "dimensionless lock-dual norm",
            "4303 absolute no-cancellation handoff",
            "RUNNER_READY_VALUES_MISSING",
            "The source side has a real scale anchor; the boundary/EM pieces still block a full number.",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, symbol, formula, value, units, source_basis, status, note in specs:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "formula": formula,
                "value_numeric": value,
                "units": units,
                "source_basis": source_basis,
                "status": status,
                "note": note,
                "parent_signed": "False",
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def source_power_anchor_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "SPA4304_0_UB",
            "U_B",
            U_B_STRONG,
            "strong local window leakage parameter imported from 123/210",
            "NUMERIC_ANCHOR_PRIVATE",
        ),
        (
            "SPA4304_1_UB2",
            "U_B^2",
            U_B2_STRONG,
            "quadratic source-support scale; equals window43/strong M_src anchor",
            "NUMERIC_ANCHOR_PRIVATE",
        ),
        (
            "SPA4304_2_power_law",
            "U_B S_cg",
            "O(U_B^2)",
            "if leakage parity/source covariance gives S_cg=O(U_B)",
            "DERIVED_POWER_CONDITIONAL",
        ),
        (
            "SPA4304_3_amplitude",
            "A_src",
            "MISSING_PARENT_INPUT",
            "dimensionless amplitude multiplying U_B^2 in N_src,strong_anchor",
            "BLOCKING_INPUT",
        ),
        (
            "SPA4304_4_claim_status",
            "claim_allowed",
            "False",
            "source-power theorem form is useful but explicitly not parent-derived in 123",
            "NONCLAIM_FIREWALL",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for anchor_id, quantity, value_or_status, role, status in specs:
        row = base_row()
        row.update(
            {
                "anchor_id": anchor_id,
                "quantity": quantity,
                "value_or_status": value_or_status,
                "role": role,
                "status": status,
                "source_paths": (
                    str(FORMAL / "123-local-source-power-theorem.md")
                    + "; "
                    + str(FORMAL / "210-PPC4161-source-support-powers-for-Jres.md")
                    + "; "
                    + str(FORMAL / "211-PPC4161-parent-ZL-parity-signature.md")
                ),
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def npair_runner_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RUN4304_0_source_pair",
            "N_pair_anchor",
            "N_pair_anchor <= U_B^2 A_src + C_inner |Q_m^H| + N_EM + N_rest",
            "Combines the new conditional N_src scale with unreduced inner/EM/rest norms.",
            "PARTIAL_RUNNER_READY",
        ),
        (
            "RUN4304_1_m_amplitude",
            "Delta_m",
            "Delta_m <= (N_pair_anchor + N_N)/lambda_m",
            "Feeds 4302/4301 m-lock amplitude once lambda_m and all source norms are sourced.",
            "FORMULA_READY_VALUES_MISSING",
        ),
        (
            "RUN4304_2_vertical_amplitude",
            "Delta_Dv_m",
            "Delta_Dv_m <= (D_v N_pair + N_DvL Delta_m + N_DvN)/lambda_m",
            "Feeds D_v Gamma_eff quadratic residual.",
            "FORMULA_READY_VALUES_MISSING",
        ),
        (
            "RUN4304_3_Cquad",
            "C4302_DVGAMMA_QUAD",
            "C_quad <= N_P/a_ref Lmin^-2 |F_2|(Delta_m Delta_Dv_m + Delta_m^2 Delta_Dv_ln_Lcg)+C_proj_derivative",
            "This remains the local-GR suppression runner; the source side now has one private anchor.",
            "HANDOFF_READY_NOT_SCORE_READY",
        ),
        (
            "RUN4304_4_exact_branch",
            "exact m-lock source silence",
            "N_pair=0 only if visible Hilbert silence closes and N_src=N_inner=N_EM=N_rest=0 componentwise",
            "No cancellations are allowed between source and boundary pieces.",
            "EXACT_ROUTE_NOT_CLOSED",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, quantity, formula, role, status in specs:
        row = base_row()
        row.update(
            {
                "runner_id": runner_id,
                "quantity": quantity,
                "formula": formula,
                "role": role,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DEC4304_0_gain",
            "FIRST_SOURCE_SCALE_ANCHOR_IMPORTED",
            "The source-support row is no longer empty: N_src,strong <= U_B^2 A_src with U_B^2=1.4413864308717837e-13.",
            "Use it as a private smoke/derivation anchor only, not a claim.",
        ),
        (
            "DEC4304_1_limit",
            "VISIBLE_HILBERT_SIGNATURE_NOT_GLOBAL",
            "The Hilbert/Poynting silence theorem is sharp but still branch-conditional; the parent action signature is not globally owned.",
            "Keep ordinary matter/EM zero only inside the signed visible-Hilbert branch.",
        ),
        (
            "DEC4304_2_blockers",
            "A_SRC_QMH_CINNER_NEM_REMAIN",
            "A_src, C_inner, Q_m^H and N_EM are the concrete remaining source/boundary inputs.",
            "Next checkpoint should hunt these amplitudes or prove exact zeros.",
        ),
        (
            "DEC4304_3_next",
            "SOURCE_POWER_AMPLITUDE_OR_INNER_CHARGE_BOUND_NEXT",
            "The best route is now not another abstract audit; it is the amplitude/inner-charge bound runner.",
            NEXT_TARGET,
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
        "Do not claim local GR/Newton/PPN/R10 from the U_B^2 source anchor.",
        "Do not set A_src=1 except as an explicitly marked smoke normalization.",
        "Do not cancel N_src, N_inner, N_EM, drift, history or boundary terms against each other.",
        "Do not count Poynting twice: it is Hilbert EM stress when owned, otherwise a residual flux norm.",
        "Do not promote visible-Hilbert branch silence to a global parent theorem until the parent action has no direct m slots.",
    ]
    rows: List[Dict[str, str]] = []
    for index, rule in enumerate(rules):
        row = base_row()
        row.update({"firewall_id": f"FW4304_{index}", "rule": rule, "status": "ACTIVE"})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4304_0_visible", "visible matter/EM/Poynting", "CONDITIONAL_ZERO_BRANCH", "useful branch; not global parent signature"),
        ("STAT4304_1_Nsrc", "N_src", "FIRST_CONDITIONAL_NUMERIC_SCALE", "U_B^2 anchor exists, A_src missing"),
        ("STAT4304_2_Ninner", "N_inner", "FORMULA_ONLY_INPUTS_MISSING", "C_inner and Q_m^H missing"),
        ("STAT4304_3_NEM", "N_EM", "ZERO_OR_BOUND_GATE", "Hodge/current/hidden F2 closure still needed"),
        ("STAT4304_4_Cquad", "C4302_DVGAMMA_QUAD", "PARTIAL_HANDOFF_READY_NOT_SCORE_READY", "needs complete N_pair, lambda_m and projector values"),
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
            "next_target_id": "NT4304_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can A_src be parent-derived/bounded, or can C_inner |Q_m^H| and N_EM be zeroed/bounded?",
            "preferred_route": "derive source covariance/parity amplitude A_src and no-inner-charge/no-hidden-EM clauses",
            "fallback_route": "source finite values for A_src, C_inner, Q_m^H, b_alpha, delta_J, delta_star, Delta_Hodge_EM and Phi_Poynting_unclosed",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal_text = f"""# 320 PPC4161 first source norms or visible-Hilbert m-lock signature

Marker: `{MARKER}`

## Decision

`{DECISION}`

4304 does two concrete things:

1. It tries to parent-sign the visible Hilbert/m-lock source silence branch. Result: the theorem is sharp, but the global parent signature remains conditional rather than owned.
2. It fills the first source-support scale instead of leaving `N_src` blank:

```text
N_src,strong <= U_B^2 A_src,
U_B = {U_B_STRONG},
U_B^2 = {U_B2_STRONG}.
```

That is progress, but not a claim: `A_src`, source covariance, `N_inner`, and `N_EM` still have to be derived or bounded.

## Visible-Hilbert Signature Audit

{md_table(tables["signature"], ["signature_id", "required_clause", "parent_signed", "result", "missing_input"])}

## First Norm Value Rows

{md_table(tables["norms"], ["row_id", "symbol", "formula", "value_numeric", "status", "note"])}

## Source-Power Anchor Import

{md_table(tables["anchors"], ["anchor_id", "quantity", "value_or_status", "status"])}

## Npair to Cquad Runner

{md_table(tables["runner"], ["runner_id", "quantity", "formula", "status"])}

## Result

The local branch has moved forward one notch: the source-support term now has a conditional quadratic scale, not just a missing label. The next hard work is the amplitude and boundary side: `A_src`, `C_inner |Q_m^H|`, and `N_EM`.

Next target: `{NEXT_TARGET}`.
"""
    doc_text = f"""# 4304 - fill first source norms or parent-sign visible Hilbert m-lock silence

## Verdict
- Visible matter/EM/Poynting silence remains a clean conditional theorem, not a global parent-signed result.
- The first source-support row is now staged with a real private anchor: `N_src,strong <= U_B^2 A_src`, using `U_B^2={U_B2_STRONG}` from the existing source-power chain.
- `A_src`, `N_inner`, and `N_EM` are still the live blockers, so no local-GR/Newton/PPN/R10 claim fires.
- The next checkpoint should attack the amplitude/inner-charge inputs directly, not circle the same fork again.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Visible-Hilbert Signature Audit
{md_table(tables["signature"], ["signature_id", "required_clause", "current_evidence", "parent_signed", "result", "missing_input"])}

## First Norm Value Rows
{md_table(tables["norms"], ["row_id", "symbol", "formula", "value_numeric", "units", "source_basis", "status", "note"])}

## Source-Power Anchor Import
{md_table(tables["anchors"], ["anchor_id", "quantity", "value_or_status", "role", "status"])}

## Npair to Cquad Runner
{md_table(tables["runner"], ["runner_id", "quantity", "formula", "role", "status"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Claim Firewall
{md_table(tables["firewall"], ["firewall_id", "rule", "status"])}

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

    add(
        "VAL4304_0_sources_exist",
        "all cited local source paths exist",
        all(Path(row["source_path"]).exists() for row in tables["sources"]),
        "source_register",
    )
    add(
        "VAL4304_1_needles_found",
        "all cited source needles found",
        all(row["needle_found"] == "True" for row in tables["sources"]),
        "source_register",
    )
    add(
        "VAL4304_2_visible_signature_not_claimed",
        "visible-Hilbert signature rows remain parent_signed false",
        all(row["parent_signed"] == "False" for row in tables["signature"]),
        "signature_audit",
    )
    add(
        "VAL4304_3_Nsrc_anchor_present",
        "N_src U_B^2 anchor row exists",
        any(row["row_id"] == "FN4304_2_Nsrc_power_anchor" and row["value_numeric"] == U_B2_STRONG for row in tables["norms"]),
        "first_norm_rows",
    )
    add(
        "VAL4304_4_anchor_nonclaim",
        "source-power anchor is explicitly nonclaim",
        all(row.get("valid_for_claim") == "False" for row in tables["anchors"]),
        "anchor_rows",
    )
    add(
        "VAL4304_5_runner_handoff",
        "Npair to C4302 handoff exists",
        any(row["quantity"] == "C4302_DVGAMMA_QUAD" for row in tables["runner"]),
        "runner_rows",
    )
    add(
        "VAL4304_6_claim_flags_false",
        "all generated rows keep claim flags false",
        all(
            row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False"
            for table in tables.values()
            for row in table
        ),
        "generated_tables",
    )
    add(
        "VAL4304_7_no_missing_marker_claim_rows",
        "norm rows do not mark missing inputs as claimable",
        all(
            not (
                "MISSING" in " ".join(str(value) for value in row.values())
                and row.get("valid_for_claim") == "True"
            )
            for row in tables["norms"] + tables["anchors"] + tables["runner"]
        ),
        "missing_input_firewall",
    )
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4304_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4304_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "generated_docs")
    add("VAL4304_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims_register")
    add("VAL4304_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "unification_spine")
    add("VAL4304_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "private_packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4304_SOURCE_REGISTER.csv",
        "signature": SOURCE_DIR / "P8_Y5_R2FR_4304_VISIBLE_HILBERT_SIGNATURE_AUDIT.csv",
        "norms": SOURCE_DIR / "P8_Y5_R2FR_4304_FIRST_NORM_VALUE_ROWS.csv",
        "anchors": SOURCE_DIR / "P8_Y5_R2FR_4304_SOURCE_POWER_ANCHOR_IMPORT.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4304_NPAIR_TO_CQUAD_RUNNER.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4304_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4304_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4304_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4304_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "signature": visible_signature_rows(),
        "norms": first_norm_rows(),
        "anchors": source_power_anchor_rows(),
        "runner": npair_runner_rows(),
        "decision": decision_rows(),
        "firewall": firewall_rows(),
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
## PPC4161 4304 first source norms or visible-Hilbert m-lock signature

Marker: `{MARKER}`

4304 converts the 4303 fork into a first filled source row. Visible Hilbert/m-lock silence remains conditional, but `N_src` now has a private nonclaim quadratic source-support anchor: `N_src,strong <= U_B^2 A_src` with `U_B^2={U_B2_STRONG}`. The remaining live inputs are `A_src`, `C_inner |Q_m^H|`, `N_EM`, and the usual `lambda_m`/projection constants before `C4302_DVGAMMA_QUAD` can be scored.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4304 packet first source norm anchor

Marker: `{PACKET_MARKER}`

Packet update: the local source fork is no longer blank. The source-support side can be carried as `U_B^2 A_src` on the private source-power branch, while inner charge and EM/Hodge/Poynting residuals stay separate absolute norms. No local-GR or R10 claim fires.
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
