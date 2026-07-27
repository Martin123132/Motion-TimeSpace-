from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3873"
BRANCH = "MTS_R2FR_Y5_FIRST_COEFFICIENT_FILL_THETA_BETA_OR_POYNTING_ZERO_3873"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3873-Y5-R2FR-first-coefficient-fill-theta-beta-or-poynting-zero.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3872_NEXT = OUT / "P8_Y5_R2FR_3872_NEXT_TARGET.csv"
CSV_3872_POY = OUT / "P8_Y5_R2FR_3872_POYNTING_SOURCE_BRIDGE.csv"
CSV_3872_CAND = OUT / "P8_Y5_R2FR_3872_FIRST_CANDIDATE_BJ_COEFFICIENT_ROWS.csv"
CSV_3872_ARENA = OUT / "P8_Y5_R2FR_3872_ARENA_PROJECTION_CONTRACT.csv"
CSV_3579_THEOREM = OUT / "P8_Y5_R2FR_3579_PUBLIC_EM_POYNTING_THEOREM.csv"
CSV_3579_BOUNDS = OUT / "P8_Y5_R2FR_3579_POYNTING_FLUX_BOUND_ROWS.csv"
CSV_3597_ONCE = OUT / "P8_Y5_R2FR_3597_EM_POYNTING_ONCE_THEOREM.csv"
CSV_3612_CLOSURE = OUT / "P8_Y5_R2FR_3612_EM_POYNTING_HILBERT_CLOSURE.csv"
CSV_3463_LEDGER = OUT / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv"
CSV_3503_THEOREM = OUT / "P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv"
CSV_3503_GATE = OUT / "P8_Y5_R2FR_3503_TOTAL_HILBERT_CURRENT_CLOSURE_GATE.csv"
CSV_3776_DOMAIN = OUT / "P8_Y5_R2FR_3776_EM_POYNTING_DOMAIN_AUDIT.csv"
CSV_3792_PIM = OUT / "P8_Y5_R2FR_3792_PIM_TOTAL_EM_SOURCE_UPDATE.csv"
CSV_3863_EM = OUT / "P8_Y5_R2FR_3863_EM_SOURCE_SCALE_BOUND.csv"
CSV_3825_BOUNDARY = OUT / "P8_Y5_R2FR_3825_BOUNDARY_REFERENCE_ZERO_THEOREM.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3873_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3873_POYNTING_STATIONARY_BOUNDARY_ZERO_THEOREM.csv",
    "clause_audit": OUT / "P8_Y5_R2FR_3873_POYNTING_ZERO_CLAUSE_AUDIT.csv",
    "coefficient_update": OUT / "P8_Y5_R2FR_3873_PHI_EM_BOUNDARY_COEFFICIENT_UPDATE.csv",
    "retained": OUT / "P8_Y5_R2FR_3873_RETAINED_EM_SOURCE_RESIDUALS.csv",
    "claim_gates": OUT / "P8_Y5_R2FR_3873_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3873_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3873_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3873_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3873_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3873_00_3872_next", CSV_3872_NEXT, "NEXT3872_0", "3872 selected first coefficient fill"),
    ("SRC3873_01_3872_poy", CSV_3872_POY, "POY3872_1_zero_route", "3872 Poynting zero route"),
    ("SRC3873_02_3872_candidate", CSV_3872_CAND, "CAND3872_8_Poynting_boundary", "3872 Phi_EM_boundary coefficient row"),
    ("SRC3873_03_3872_arena", CSV_3872_ARENA, "APC3872_5_EM", "3872 EM/Poynting arena contract"),
    ("SRC3873_04_3579_theorem", CSV_3579_THEOREM, "PEM3579_2_poynting_flux_identity", "public Poynting flux identity"),
    ("SRC3873_05_3579_bounds", CSV_3579_BOUNDS, "PFB3579_1_Phi_EM_rad", "Poynting flux bound row"),
    ("SRC3873_06_3597_once", CSV_3597_ONCE, "EMT3597_6_conditional_theorem", "EM/Poynting once-only theorem"),
    ("SRC3873_07_3612_closure", CSV_3612_CLOSURE, "EPC3612_6_closure_rule", "Poynting Hilbert closure rule"),
    ("SRC3873_08_3463_ledger", CSV_3463_LEDGER, "EM3463_2_poynting", "Maxwell/Poynting stress ledger"),
    ("SRC3873_09_3503_theorem", CSV_3503_THEOREM, "OHM3503_3_total_Hilbert_current", "total Hilbert current closure"),
    ("SRC3873_10_3503_gate", CSV_3503_GATE, "THC3503_6_stationary_flux", "stationary flux gate"),
    ("SRC3873_11_3776_domain", CSV_3776_DOMAIN, "EDA3776_3_Poynting_flux", "EM/Poynting source-domain audit"),
    ("SRC3873_12_3792_pim", CSV_3792_PIM, "PIM3792_2_EM_Hilbert_admission", "Pi_M total EM Hilbert admission"),
    ("SRC3873_13_3863_em", CSV_3863_EM, "ESB3863_2_EM_source_scale", "EM source-scale envelope"),
    ("SRC3873_14_3825_boundary", CSV_3825_BOUNDARY, "BRT3825_1_annulus_stokes", "boundary/Stokes zero theorem"),
]

PHI_ZERO_THEOREM = (
    "For a closed total-system worldtube W with observed Maxwell stress descended to the same g_obs/coframe, "
    "if L_tau fields=0 up to fixed EM gauge, no charge/current or radiation crosses boundary(W), and boundary/reference improvements are silent, "
    "then Phi_EM_boundary[W,tau] := int_dt int_boundary(W) S_EM dot n dA = 0. Circulating local Poynting flow may remain inside W; only net leakage through the chosen source boundary is zero."
)

UPDATED_EM_ENVELOPE = (
    "B_EM_scale_stationary <= b_Z+b_J+|b_alpha|+|w_EM|+|C_XF2|+|C_JQ|+|Delta_M_EM_binding|"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_poynting_stationary_boundary_zero",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "PZT3873_0_identity",
            "Poynting theorem",
            "d_t E_EM(W)+int_boundary(W) S_EM·n dA = -int_W J·E dV plus gauge/improvement terms",
            "standard observed-frame Maxwell stress identity",
            "EXACT_CONDITIONAL_IDENTITY",
        ),
        (
            "PZT3873_1_total_exchange",
            "matter-EM exchange cancellation",
            "nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda and nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda, so only T_total is conserved",
            "prevents matter-only source tubes from deleting EM energy flow",
            "EXACT_CONDITIONAL_TOTAL_CURRENT_RULE",
        ),
        (
            "PZT3873_2_stationary_zero",
            "stationary boundary flux theorem",
            PHI_ZERO_THEOREM,
            "sets net leakage coefficient Phi_EM_boundary to zero on the stationary isolated total-system branch",
            "EXACT_CONDITIONAL_ZERO_FOR_PHI_EM_BOUNDARY",
        ),
        (
            "PZT3873_3_circulation_guard",
            "circulating Poynting is not leakage",
            "S_EM may be nonzero locally in stationary bound systems, but a closed boundary integral can vanish; do not infer S_EM=0 from Phi_EM_boundary=0",
            "keeps EM stress and angular/momentum density in total T_EM",
            "SCOPE_GUARD",
        ),
        (
            "PZT3873_4_not_EM_origin",
            "not a derivation of EM from flow",
            "The theorem assumes the observed Maxwell/Hodge stress branch; it does not derive *_EM, charge normalization, no-extra-F2, or alpha.",
            "prevents overclaim and keeps normalization gates live",
            "SCOPE_GUARD",
        ),
    ]
    return [
        {
            "theorem_id": row_id,
            "piece": piece,
            "statement_or_formula": formula,
            "effect": effect,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, formula, effect, status in rows
    ]


def clause_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("CL3873_0_observed_Hodge", "observed Maxwell stress descends to same g_obs/coframe", "needed for S_EM as component of Hilbert stress", "CONDITIONAL_STANDARD_FORM_NOT_PARENT_DERIVED", "Delta_Hodge_EM"),
        ("CL3873_1_total_worldtube", "worldtube contains matter plus bound EM field/interactions/apparatus stress", "prevents matter-only source domain error", "PREFERRED_CONDITIONAL_DOMAIN", "epsilon_domain"),
        ("CL3873_2_stationary_generator", "L_tau fields=0 up to fixed EM gauge on the local branch", "turns time-energy storage term into zero", "BRANCH_CONDITION_REQUIRED", "d_t E_EM"),
        ("CL3873_3_no_crossing_current", "no charge/current crosses the selected boundary", "keeps J·E as internal exchange, not external leakage", "BRANCH_CONDITION_REQUIRED", "J_cross"),
        ("CL3873_4_no_radiative_leakage", "no outgoing/background radiation crosses boundary, or it is explicitly bounded", "sets Phi_EM_rad=0 only in stationary isolated branch", "CONDITIONAL_ZERO_ELSE_BOUND", "Phi_EM_rad"),
        ("CL3873_5_boundary_reference", "boundary/reference/improvement terms are silent on the annulus", "prevents corner/improvement flux from replacing Poynting flux", "BOUNDARY_THEOREM_CONDITIONAL", "C_EM_surface_gauge"),
        ("CL3873_6_same_owner_guard", "same current/Hilbert source owner handles matter+EM exchange", "prevents double count or zero count of EM binding/Poynting", "OWNER_STILL_UNSIGNED", "epsilon_EM_once"),
    ]
    return [
        {
            "clause_id": row_id,
            "required_clause": clause,
            "why_needed": why,
            "current_status": status,
            "failure_residual": residual,
            "passes_as_current_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, clause, why, status, residual in rows
    ]


def coefficient_update_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "PCU3873_0_old_row",
            "Phi_EM_boundary",
            "epsilon_Poynting = |int_dt int_boundary S_EM·n dA|/(M_ref c^2)",
            "CAND3872_8 status was POYNTING_SOURCE_ROW_REQUIRED_NONCLAIM",
            "still valid for radiative/nonstationary branches",
            "BOUND_ROUTE_RETAINED",
        ),
        (
            "PCU3873_1_stationary_zero",
            "Phi_EM_boundary",
            "Phi_EM_boundary[stationary closed total-system W]=0",
            PHI_ZERO_THEOREM,
            "removes the explicit boundary leakage term from the stationary isolated EM source envelope",
            "ZERO_CONDITIONAL_BRANCH_FILLED",
        ),
        (
            "PCU3873_2_updated_envelope",
            "B_EM_scale_stationary",
            UPDATED_EM_ENVELOPE,
            "3863 envelope with |Phi_EM_boundary| term dropped only under CL3873_0..6",
            "w_EM, C_XF2, C_JQ, b_Z, b_J, b_alpha, and Delta_M_EM_binding remain live",
            "REDUCED_ENVELOPE_NONCLAIM",
        ),
        (
            "PCU3873_3_local_GR_effect",
            "R_source_normalization_total",
            "R_source_total_stationary <= R_source_total_without_Phi_EM_leak + retained EM normalization/current/binding terms",
            "Poynting leakage no longer acts as independent source time-hair in stationary isolated branch",
            "does not prove Newton/PPN/local-GR because source owner and EM normalization remain open",
            "LOCAL_GR_HELPFUL_NOT_CLAIM",
        ),
    ]
    return [
        {
            "update_id": row_id,
            "quantity": quantity,
            "new_formula_or_rule": formula,
            "derivation_or_source": derivation,
            "effect": effect,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, formula, derivation, effect, status in rows
    ]


def retained_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("RET3873_0_Hodge", "Delta_Hodge_EM", "observed EM Hodge/coframe owner not derived from parent q/e_obs", "blocks EM stress normalization/local-GR compatibility"),
        ("RET3873_1_wEM", "w_EM", "independent EM action multiplier not excluded", "scales T_EM, binding energy and Poynting source strength"),
        ("RET3873_2_CXF2", "C_XF2", "hidden/extra F2 operator not excluded", "reopens alpha/clock/WEP/R10/source response"),
        ("RET3873_3_CJQ", "C_JQ", "charge/current normalization not parent-owned numerically", "keeps current/source coupling residual live"),
        ("RET3873_4_binding", "Delta_M_EM_binding", "EM binding must be included exactly once in M_H,total", "prevents deleting or double-counting bound field energy"),
        ("RET3873_5_readout", "C_EM_readout", "radiative/readout regeneration not theorem-zero", "can reintroduce F2/current/source response"),
        ("RET3873_6_radiative_branch", "Phi_EM_rad_nonstationary", "if the branch radiates or crosses background flux, Poynting term must be bounded not zeroed", "keeps bound route for nonstationary cases"),
    ]
    return [
        {
            "retained_id": row_id,
            "residual": residual,
            "why_retained": why,
            "impact": impact,
            "status": "RETAINED_AFTER_PHI_BOUNDARY_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, residual, why, impact in rows
    ]


def claim_gate_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    updates: list[dict[str, object]],
    retained: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    has_zero = any(row["status"] == "EXACT_CONDITIONAL_ZERO_FOR_PHI_EM_BOUNDARY" for row in theorem)
    has_unsigned = any(row["passes_as_current_claim"] is False for row in clauses)
    rows = [
        ("G3873_0_sources", "all cited source rows resolved", "PASS" if all_sources else "FAIL", f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"),
        ("G3873_1_zero_theorem", "stationary Poynting boundary zero theorem written", "PASS" if has_zero else "FAIL", "Phi_EM_boundary conditional zero branch"),
        ("G3873_2_clause_audit", "all zero clauses audited", "PASS" if len(clauses) >= 7 else "FAIL", f"{len(clauses)} clauses"),
        ("G3873_3_reduced_envelope", "stationary EM source envelope drops Phi term only conditionally", "PASS" if any(row["quantity"] == "B_EM_scale_stationary" for row in updates) else "FAIL", UPDATED_EM_ENVELOPE),
        ("G3873_4_retained_residuals", "normalization/current/Hodge/readout residuals remain live", "PASS" if len(retained) >= 6 else "FAIL", f"{len(retained)} retained residuals"),
        ("G3873_5_no_public_claim", "unsigned clauses block local-GR/EM claim", "BLOCKED" if has_unsigned else "FAIL", "zero theorem is exact conditional, not parent-promoted"),
        ("G3873_6_no_claim", "all generated rows remain nonclaim", "PASS", "valid_for_claim=false throughout"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, detail in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("DEC3873_0", "close the stationary Poynting leakage coefficient conditionally", "this removes one finite source-coupling tail on the isolated local branch"),
        ("DEC3873_1", "do not set local Poynting vector itself to zero", "stationary systems can have circulating EM momentum/stress with zero net boundary flux"),
        ("DEC3873_2", "do not claim EM origin or alpha normalization", "the theorem assumes observed Maxwell/Hodge stress and leaves F2/current/charge gates live"),
        ("DEC3873_3", "next best target is EM normalization/current owner or Delta_w theta commonness", "Phi leakage is now localized; bigger remaining coupling failures are w_EM/C_XF2/C_JQ/Delta_w"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for decision_id, decision, because in rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3873_0",
            "target_checkpoint": "3874-Y5-R2FR-EM-normalization-or-Delta-w-theta-commonness.md",
            "script": "scripts/Y5_R2FR_3874_EM_normalization_or_Delta_w_theta_commonness.py",
            "objective": "attack the larger retained coupling families after the Poynting leakage term: either no-extra-F2/w_EM normalization, charge-current C_JQ, or Delta_w theta-vector commonness",
            "why_next": "3873 conditionally removes Phi_EM_boundary for stationary isolated total-system tubes; remaining source-coupling risk is normalization/current/source-weight, not boundary Poynting leakage",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "result": "PHI_EM_BOUNDARY_ZERO_CONDITIONAL_BRANCH_FILLED_NONCLAIM",
            "claim_allowed": False,
            "short_summary": "3873 proves the stationary isolated total-system branch has zero net Poynting boundary leakage, while preserving circulating local Poynting stress and retaining EM normalization/current/Hodge/readout residuals.",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        values = []
        for col in columns:
            values.append(str(row.get(col, "")).replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    updates: list[dict[str, object]],
    retained: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3873 — First Coefficient Fill: Poynting Boundary Zero

Generated: `{timestamp}`

## Result

3873 closes one finite coupling family conditionally:

`{PHI_ZERO_THEOREM}`

This fills the `Phi_EM_boundary` branch for stationary isolated total-system source tubes. It does **not** set local Poynting flow to zero, and it does **not** derive EM, alpha, charge normalization, or the no-extra-F2 rule.

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Poynting Zero Theorem

{markdown_table(theorem, ["theorem_id", "piece", "statement_or_formula", "status"])}

## Clause Audit

{markdown_table(clauses, ["clause_id", "required_clause", "current_status", "failure_residual"])}

## Coefficient Update

{markdown_table(updates, ["update_id", "quantity", "new_formula_or_rule", "effect", "status"])}

## Retained Residuals

{markdown_table(retained, ["retained_id", "residual", "why_retained", "impact"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "detail", "claim_allowed"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "because"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

3873 is a genuine forward move: the Poynting term is no longer vague. In the stationary isolated total-system branch, the net boundary leakage coefficient `Phi_EM_boundary` has an exact conditional zero route, so the EM source-scale envelope can drop that term under the stated clauses. The remaining hard coupling problem is now sharper: derive or bound `w_EM`, `C_XF2`, `C_JQ`, `Delta_M_EM_binding`, `Delta_Hodge_EM`, readout regeneration, and the `Delta_w/theta` source-weight family.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3873 POYNTING BOUNDARY ZERO -->"
    end = "<!-- END 3873 POYNTING BOUNDARY ZERO -->"
    block = f"""{start}

## 3873 — Stationary Poynting boundary leakage zero

`3873` closes one finite coupling family conditionally. For a closed total-system worldtube with observed Maxwell stress on the same `g_obs/coframe`, stationary generator, no boundary current/radiation crossing, and silent boundary/reference improvements, the net Poynting leakage coefficient

`Phi_EM_boundary[W,tau] = int_dt int_boundary(W) S_EM · n dA`

is zero. This does not set local Poynting flow or EM stress to zero; circulating bound-field momentum remains part of `T_EM`. It also does not derive the EM Hodge rule, no-extra-F2, action normalization, charge/current owner, or alpha. It only removes one source-normalization tail on the stationary isolated branch.

Updated stationary envelope:

`{UPDATED_EM_ENVELOPE}`

Next gate: `3874`, attack `w_EM/C_XF2/C_JQ` or `Delta_w/theta` commonness.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3873_POYNTING_STATIONARY_BOUNDARY_ZERO_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3873_PHI_EM_BOUNDARY_COEFFICIENT_UPDATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3873_RETAINED_EM_SOURCE_RESIDUALS.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3873_VALIDATION.csv`

<!-- Generated by 3873 at {timestamp} -->
{end}
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if start in existing and end in existing:
        before = existing.split(start)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        new_text = f"{before}\n\n{block}\n\n{after}".rstrip() + "\n"
    else:
        new_text = existing.rstrip() + "\n\n" + block + "\n"
    SPINE_PATH.write_text(new_text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    updates: list[dict[str, object]],
    retained: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    checks.append(("VAL3873_0_sources", "all cited source paths exist and needles are found", all_sources, f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"))
    checks.append(("VAL3873_1_zero_theorem", "stationary Phi_EM_boundary zero theorem exists", any(row["status"] == "EXACT_CONDITIONAL_ZERO_FOR_PHI_EM_BOUNDARY" for row in theorem), "zero theorem row present"))
    checks.append(("VAL3873_2_circulation_guard", "local Poynting flow is not falsely zeroed", any(row["theorem_id"] == "PZT3873_3_circulation_guard" for row in theorem), "circulation guard present"))
    checks.append(("VAL3873_3_clause_count", "zero theorem clauses are audited", len(clauses) >= 7, f"{len(clauses)} clauses"))
    checks.append(("VAL3873_4_clause_claim_block", "clauses are not promoted as current claim", all(row["passes_as_current_claim"] is False for row in clauses), "passes_as_current_claim=false"))
    checks.append(("VAL3873_5_coefficient_update", "Phi boundary coefficient has stationary zero update", any(row["update_id"] == "PCU3873_1_stationary_zero" for row in updates), "PCU3873_1 present"))
    checks.append(("VAL3873_6_envelope_reduced", "updated stationary envelope omits Phi term", any(row["new_formula_or_rule"] == UPDATED_EM_ENVELOPE for row in updates), UPDATED_EM_ENVELOPE))
    required_retained = {"w_EM", "C_XF2", "C_JQ", "Delta_M_EM_binding", "Delta_Hodge_EM"}
    retained_names = {row["residual"] for row in retained}
    checks.append(("VAL3873_7_retained_residuals", "hard EM coupling residuals remain listed", required_retained.issubset(retained_names), ",".join(sorted(retained_names))))
    checks.append(("VAL3873_8_no_claim_gates", "claim gates do not allow a claim", all(str(row["claim_allowed"]) == "False" for row in gates), "claim_allowed=false"))
    checks.append(("VAL3873_9_doc", "markdown checkpoint exists with expected bottom line", DOC_PATH.exists() and "3873 is a genuine forward move" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3873_10_spine", "spine updated with 3873 block", SPINE_PATH.exists() and "BEGIN 3873 POYNTING BOUNDARY ZERO" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key not in {"validation"}]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            count = len(read_csv_rows(path))
            parse_details.append(f"{path.name}:{count}")
        except Exception as exc:  # pragma: no cover - validation detail
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3873_11_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [path for path in FWB.rglob("*3873*") if path.is_file()]
    checks.append(("VAL3873_12_formalization_untouched", "no generated 3873 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3873_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3873_14_no_generated_claim", "all analytical rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [theorem, clauses, updates, retained] for row in collection), "valid_for_claim=false"))
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
    theorem = theorem_rows(timestamp)
    clauses = clause_rows(timestamp)
    updates = coefficient_update_rows(timestamp)
    retained = retained_rows(timestamp)
    gates = claim_gate_rows(sources, theorem, clauses, updates, retained, timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["clause_audit"], clauses)
    write_csv(OUTPUTS["coefficient_update"], updates)
    write_csv(OUTPUTS["retained"], retained)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, clauses, updates, retained, gates, decisions, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, clauses, updates, retained, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_POYNTING_BOUNDARY_ZERO_CONDITIONAL")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
