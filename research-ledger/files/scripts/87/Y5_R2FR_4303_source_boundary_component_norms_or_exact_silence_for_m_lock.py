from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4303"
CLAIM_ID = "L-144"
BRANCH = "MTS_R2FR_Y5_SOURCE_BOUNDARY_SILENCE_OR_COMPONENT_NORMS_FOR_M_LOCK_4303"
DECISION = "VISIBLE_HILBERT_SOURCE_SILENCE_DERIVED_CONDITIONALLY_NONHILBERT_NORMS_RETAINED_NONCLAIM"
MARKER = "PPC4161_SOURCE_BOUNDARY_SILENCE_OR_COMPONENT_NORMS_FOR_M_LOCK_4303"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_BOUNDARY_SILENCE_OR_COMPONENT_NORMS_FOR_M_LOCK_4303"
NEXT_TARGET = "4304-Y5-R2FR-fill-first-source-norms-or-parent-sign-visible-Hilbert-m-lock-silence.md"

FORMAL_PATH = FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md"
DOC_PATH = POST / "4303-Y5-R2FR-source-boundary-component-norms-or-exact-silence-for-m-lock.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4303_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4303_00_4302_formal": (
        FORMAL / "318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md",
        "Next target: `4303-Y5-R2FR-source-boundary-component-norms-or-exact-silence-for-m-lock.md`.",
        "4302 handoff to source-boundary silence or finite component norms.",
    ),
    "SRC4303_01_4302_inputs": (
        SOURCE_DIR / "P8_Y5_R2FR_4302_SOURCE_BOUNDARY_INPUT_PACK.csv",
        "IP4302_8_EM",
        "4302 EM/Poynting source residual gate.",
    ),
    "SRC4303_02_4302_quad": (
        SOURCE_DIR / "P8_Y5_R2FR_4302_F2_AND_DVGAMMA_QUAD_ROW.csv",
        "DQ4302_4_Cquad",
        "4302 quadratic DvGamma row that needs J/B norms.",
    ),
    "SRC4303_03_1536_jeff": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1536_JEFF_COMPONENT_SPLIT.csv",
        "JEFF1536_0_screened_source",
        "J_eff component decomposition.",
    ),
    "SRC4303_04_1536_bm": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1536_BM_COMPONENT_SPLIT.csv",
        "BM1536_0_inner_charge",
        "B_m component decomposition.",
    ),
    "SRC4303_05_1537_norms": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1537_COMPONENT_NORM_INPUT_PACK.csv",
        "NORM1537_0_N_src",
        "Component norm slots for N_lock.",
    ),
    "SRC4303_06_1537_priority": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1537_FIRST_PRIORITY_NORM_ROWS.csv",
        "FP1537_2_N_inner_zero",
        "First-priority source/inner-boundary norm rows.",
    ),
    "SRC4303_07_3340_hilbert": (
        POST / "3340-Y5-R2FR-parent-Hilbert-source-clause-or-finite-residual-vector-under-AX1090.md",
        "HSC3340_0_parent_action_form",
        "Parent Hilbert source clause and finite residual fallback.",
    ),
    "SRC4303_08_3523_poynting": (
        POST / "3523-Y5-R2FR-source-label-forgetting-functor-and-EM-Hodge-owner-or-marker-kernel-bound.md",
        "DER3523_2_public_Maxwell_Poynting_lock",
        "Poynting as Maxwell Hilbert stress when EM owner closes.",
    ),
    "SRC4303_09_3524_composite": (
        POST / "3524-Y5-R2FR-observed-stack-and-charge-lattice-parent-owner-or-local-source-kernel-values.md",
        "COT3524_0_shared_owner_theorem",
        "Composite observed-stack Hilbert source theorem.",
    ),
    "SRC4303_10_4295_kernel": (
        FORMAL / "07-unification-spine.md",
        "4295 finds that the ordinary local source kernel is real inside the private PPC4161 selector",
        "Ordinary-source kernel exists privately, raw transition kernel not parent-signed.",
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
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("\n", "<br>") for col in columns) + " |")
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
            "4303 derives the exact conditional silence theorem for the m-lock source/boundary terms. "
            "If the visible matter and Maxwell sectors factor through the same observed Hilbert action before readout, "
            "and m appears only in the lock sector, then delta S_visible/delta m=0: ordinary matter, EM stress and "
            "Poynting do not source J_eff or B_m separately. Any non-Hilbert source support, inner charge, hidden "
            "EM/Hodge/current marker, transition shell, history or moving-boundary term is retained as an absolute "
            "component norm feeding N_J, N_B and C4302_DVGAMMA_QUAD."
        ),
        (
            "4303 source register, visible-Hilbert silence theorem, component zero/norm matrix, Nlock-to-DvGamma "
            "handoff, EM/Poynting guard, decision, firewall, status, next-target and validation CSV."
        ),
        "private_visible_Hilbert_m_lock_silence_conditional_nonclaim_component_norms_retained",
        (
            "Parent-sign the visible Hilbert/Maxwell source clauses and m-sector decoupling, or fill finite "
            "N_src, N_inner, N_EM, N_transition, N_history, N_boundary and vertical derivative norms."
        ),
        (
            "Claiming source silence without parent action-domain ownership, treating Poynting as a second force, "
            "cancelling component norms, or promoting m-lock Gamma trace silence to full local GR."
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


def silence_theorem_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "VHS4303_0_action_split",
            "visible Hilbert action split",
            "S_parent = S_lock[m,q] + S_vis[g_obs(q),psi,A,lambda0] + S_boundary with no direct m slot in S_vis",
            "delta S_vis/delta m = 0 at fixed q/g_obs if the split is parent-owned",
            "EXACT_CONDITIONAL_THEOREM",
        ),
        (
            "VHS4303_1_matter_silence",
            "ordinary matter source silence",
            "J_matter_to_m = delta S_matter[g_obs(q),psi]/delta m = 0",
            "Visible matter stress remains in Hilbert T_munu for GR/Newton readout, not in the memory lock equation.",
            "CONDITIONAL_ZERO_ROUTE",
        ),
        (
            "VHS4303_2_EM_Poynting_silence",
            "Maxwell-Hodge/Poynting silence",
            "J_EM_to_m=0 and B_EM_to_m=0 when S_EM=-lambda0/4 int sqrt(-g_obs)F^2 and lambda0,*_obs,current lattice are q-owned",
            "Poynting is T_EM^{0i}; it is not an extra background field force in J_eff.",
            "CONDITIONAL_ZERO_ROUTE",
        ),
        (
            "VHS4303_3_boundary_silence",
            "visible boundary/radiative flux routing",
            "B_visible_to_m=0 if visible flux is a Hilbert/source bookkeeping term or an explicitly routed exterior flux, not an m-boundary charge",
            "Radiation is routed, not erased.",
            "CONDITIONAL_ZERO_OR_BOUND_ROUTE",
        ),
        (
            "VHS4303_4_nonHilbert_residual",
            "non-Hilbert residual survives",
            "J_eff+B_m = R_nonHilbert + R_hidden_EM + R_transition + R_history + R_boundary",
            "Any channel not covered by VHS4303_0..3 must be an absolute component norm.",
            "BOUND_ROUTE_REQUIRED",
        ),
        (
            "VHS4303_5_verdict",
            "source-boundary exact silence",
            "J_eff=B_m=0 only if visible Hilbert silence plus all non-Hilbert residual components vanish componentwise",
            "Current corpus has conditional private source-kernel evidence but not a global parent signature.",
            "NOT_PARENT_SIGNED_NONCLAIM",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for theorem_id, theorem, formula, implication, status in specs:
        row = base_row()
        row.update(
            {
                "theorem_id": theorem_id,
                "theorem": theorem,
                "formula_or_condition": formula,
                "implication": implication,
                "status": status,
                "parent_signed": "False",
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def component_matrix_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "CM4303_0_visible_matter",
            "J_visible_matter",
            "ordinary matter Hilbert stress",
            "zero if S_matter has no direct m slot and varies only through g_obs(q)",
            "N_visible_matter=0 on signed visible-Hilbert branch; otherwise eta_species/xi_tensor source residual",
            "CONDITIONAL_ZERO_ELSE_SOURCE_RESIDUAL",
        ),
        (
            "CM4303_1_visible_EM",
            "J_EM_Poynting",
            "Maxwell-Hodge stress and Poynting flux",
            "zero in m equation if Hodge, gauge normalization and current lattice are q-owned/fixed",
            "N_EM <= |b_alpha|+|delta_J|+|delta_star|+||Delta_Hodge_EM||+|Phi_Poynting_unclosed|",
            "CONDITIONAL_ZERO_ELSE_EM_RESIDUAL",
        ),
        (
            "CM4303_2_screened_source",
            "N_src",
            "non-Hilbert screened source support U_B S_cg",
            "zero only if source support is Hilbert-owned/q-kernel or U_B projection vanishes",
            "N_src <= ||U_B||_inf ||S_cg_nonHilbert||_{E*}",
            "PRIMARY_BOUND_ROW",
        ),
        (
            "CM4303_3_inner_charge",
            "N_inner",
            "inner compact-source m-charge Q_m^H",
            "zero only if compact source has no independent m-charge or source kernel absorbs it before m-variation",
            "N_inner <= C_inner |Q_m^H_nonHilbert|",
            "PRIMARY_BOUND_ROW",
        ),
        (
            "CM4303_4_drift_selector",
            "N_drift_selector",
            "m_L/L_cg/Pi_B/mu_B/tau_L drift",
            "zero only on fixed local branch/selector theorem",
            "N_drift_selector <= N_drift_mL+N_drift_Lcg+N_selector",
            "BOUND_ROW_REQUIRED",
        ),
        (
            "CM4303_5_history_transition",
            "N_history_transition",
            "history memory and transition-current injection",
            "zero only under local causal silence plus transition-kernel membership",
            "N_history_transition <= N_history+N_transition+N_mass_current",
            "BOUND_ROW_REQUIRED",
        ),
        (
            "CM4303_6_boundary_domain",
            "N_boundary_domain",
            "no-flux violation, zero-mode, outer flux, history boundary, moving domain",
            "zero only with parent boundary/zero-mode/domain certificate",
            "N_boundary_domain <= N_no_flux+N_zero_mode+N_outer+N_history_boundary+N_domain",
            "BOUND_ROW_REQUIRED",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for component_id, symbol, channel, zero_rule, bound_rule, status in specs:
        row = base_row()
        row.update(
            {
                "component_id": component_id,
                "symbol": symbol,
                "channel": channel,
                "zero_rule": zero_rule,
                "bound_rule": bound_rule,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def handoff_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "HD4303_0_NJ",
            "N_J_4303",
            "N_J <= N_visible_matter + N_EM + N_src + N_drift_selector + N_history_transition",
            "absolute source-side sum; no cancellation",
            "FORMULA_READY_VALUES_MISSING",
        ),
        (
            "HD4303_1_NB",
            "N_B_4303",
            "N_B <= N_inner + N_boundary_domain + N_EM_boundary",
            "absolute boundary-side sum; no cancellation",
            "FORMULA_READY_VALUES_MISSING",
        ),
        (
            "HD4303_2_Delta_m",
            "Delta_m",
            "Delta_m <= (N_J_4303+N_B_4303+N_N)/lambda_m",
            "feeds DQ4302_1_Delta_m",
            "FORMULA_READY_VALUES_MISSING",
        ),
        (
            "HD4303_3_Delta_Dv_m",
            "Delta_Dv_m",
            "Delta_Dv_m <= (D_v N_J + D_v N_B + N_DvL Delta_m + N_DvN)/lambda_m",
            "feeds DQ4302_2_Delta_Dv_m",
            "FORMULA_READY_VALUES_MISSING",
        ),
        (
            "HD4303_4_Cquad",
            "C4302_DVGAMMA_QUAD",
            "insert Delta_m and Delta_Dv_m into C_quad <= N_P/a_ref Lmin^-2 |F_2|(Delta_m Delta_Dv_m + Delta_m^2 Delta_Dv_ln_Lcg)+C_proj_derivative",
            "ready for future numeric/source rows",
            "RUNNER_HANDOFF_READY_NOT_SCORE_READY",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for handoff_id, quantity, formula, role, status in specs:
        row = base_row()
        row.update(
            {
                "handoff_id": handoff_id,
                "quantity": quantity,
                "formula": formula,
                "role": role,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def em_guard_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "EMG4303_0_poynting_route",
            "Poynting is allowed only as S^i=T_EM^{0i} from the same Maxwell-Hodge Hilbert stress.",
            "zero contribution to m-lock forcing if EM owner and action-domain clauses are signed",
            "CONDITIONAL_ZERO_ROUTE",
        ),
        (
            "EMG4303_1_hidden_F2",
            "A hidden f(m,X)F^2 or non-q-owned gauge normalization creates a real source residual.",
            "enters N_EM through b_alpha or hidden F2 response",
            "BOUND_REQUIRED_IF_PRESENT",
        ),
        (
            "EMG4303_2_hodge_current",
            "Independent Hodge/constitutive/current-lattice drift is not killed by gauge covariance.",
            "enters N_EM through Delta_Hodge_EM, delta_J, delta_star",
            "BOUND_REQUIRED_IF_PRESENT",
        ),
        (
            "EMG4303_3_flux_boundary",
            "Radiative Poynting flux across the collar is a boundary/source bookkeeping term, not a silent deletion.",
            "zero only for closed/static collar; otherwise Phi_Poynting_unclosed is a boundary norm",
            "ZERO_OR_BOUND_ROUTE",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for guard_id, rule, consequence, status in specs:
        row = base_row()
        row.update({"guard_id": guard_id, "rule": rule, "consequence": consequence, "status": status})
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DEC4303_0_gain",
            "VISIBLE_HILBERT_SILENCE_THEOREM_EXTRACTED",
            "Ordinary visible matter plus Maxwell/Poynting do not source the m-lock equation if they factor only through the observed Hilbert action.",
            "Use this as the clean local-GR branch condition, not as a global claim.",
        ),
        (
            "DEC4303_1_limit",
            "NONHILBERT_COMPONENTS_REMAIN",
            "U_B S_cg, Q_m^H, hidden EM markers, transition/history and boundary/domain terms are not zeroed by the visible-Hilbert theorem.",
            "Retain absolute component norm rows.",
        ),
        (
            "DEC4303_2_runner",
            "NLOCK_TO_C4302_HANDOFF_READY",
            "N_J and N_B now have a 4302-compatible formula handoff into Delta_m, Delta_Dv_m and C4302_DVGAMMA_QUAD.",
            "Fill first source values or theorem-zero switches next.",
        ),
        (
            "DEC4303_3_next",
            "FIRST_VALUES_OR_PARENT_SIGNATURE_NEXT",
            "The highest leverage next step is either parent-sign visible Hilbert silence in the m equation or fill N_src/N_inner/N_EM component norms.",
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
        "Do not promote visible-Hilbert silence unless the parent action really has no direct m slot in S_vis/S_EM.",
        "Do not use Poynting as an extra hidden background source; it is Hilbert EM stress or a bounded residual.",
        "Do not cancel N_src against N_inner or source components against boundary components.",
        "Do not score C4302_DVGAMMA_QUAD until N_J, N_B, vertical norms, lambda_m and projection constants are source-backed.",
        "Do not claim local GR, Newton, Maxwell or R10 pass from 4303; Khat, connection, boundary and full source-coupling gates remain open.",
    ]
    rows: List[Dict[str, str]] = []
    for index, rule in enumerate(rules):
        row = base_row()
        row.update({"firewall_id": f"FW4303_{index}", "rule": rule, "status": "ACTIVE"})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4303_0_visible", "visible matter/EM/Poynting branch", "CONDITIONAL_ZERO_THEOREM", "clean if parent Hilbert action-domain is signed"),
        ("STAT4303_1_Nsrc", "N_src", "PRIMARY_VALUE_OR_ZERO_NEEDED", "source-support term remains first source blocker"),
        ("STAT4303_2_Ninner", "N_inner", "PRIMARY_VALUE_OR_ZERO_NEEDED", "inner compact-source charge remains first boundary blocker"),
        ("STAT4303_3_NEM", "N_EM", "ZERO_OR_BOUND_GATE", "Poynting/Hodge/current are routed but not globally parent-signed"),
        ("STAT4303_4_Cquad", "C4302_DVGAMMA_QUAD", "HANDOFF_READY_NOT_SCORE_READY", "component norms and projections missing"),
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
            "next_target_id": "NT4303_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can visible Hilbert m-silence be parent-signed, and can N_src/N_inner/N_EM get theorem-zero or finite values?",
            "preferred_route": "parent-sign action split S_lock[m]+S_vis[g_obs(q)]+S_EM[g_obs(q)] with no direct m source",
            "fallback_route": "fill N_src, N_inner, N_EM and vertical derivative norm rows with source paths, units and no-cancellation guards",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal_text = f"""# 319 PPC4161 source-boundary silence or component norms for m-lock

Marker: `{MARKER}`

## Decision

`{DECISION}`

4303 extracts the clean theorem fork for the m-lock source terms:

```text
S_parent = S_lock[m,q] + S_vis[g_obs(q),psi,A,lambda0] + S_boundary,
delta S_vis/delta m = 0
```

So visible matter, Maxwell stress and Poynting do not force `u=delta m` if they are Hilbert-owned before readout and have no direct `m` slot. Everything outside that branch becomes an absolute component norm.

## Visible-Hilbert Silence Theorem

{md_table(tables["theorem"], ["theorem_id", "theorem", "formula_or_condition", "status"])}

## Component Zero/Norm Matrix

{md_table(tables["components"], ["component_id", "symbol", "zero_rule", "bound_rule", "status"])}

## Nlock to DvGamma Handoff

{md_table(tables["handoff"], ["handoff_id", "quantity", "formula", "status"])}

## EM/Poynting Guard

{md_table(tables["em"], ["guard_id", "rule", "status"])}

## Result

Visible Hilbert ownership can make ordinary matter/EM/Poynting silent in the `m` equation, but it does not zero non-Hilbert source support, inner charge, transition/history or boundary/domain components. Those now feed the `4302` quadratic Gamma row by absolute sums.

Next target: `{NEXT_TARGET}`.
"""
    doc_text = f"""# 4303 - source-boundary component norms or exact silence for m-lock

## Verdict
- Derived the conditional visible-Hilbert silence theorem: if matter and Maxwell/Poynting factor only through `g_obs(q)` before readout, they do not directly source the `m`-lock equation.
- This is useful but not a full closure: non-Hilbert `U_B S_cg`, inner `Q_m^H`, hidden EM/Hodge/current markers, transition/history and boundary/domain terms remain as absolute norm rows.
- The `N_lock` handoff is now explicit for `4302`: component norms feed `Delta_m`, `Delta_Dv_m`, then `C4302_DVGAMMA_QUAD`.
- No cancellation and no public local-GR/Newton/Maxwell/R10 claim.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Visible-Hilbert Silence Theorem
{md_table(tables["theorem"], ["theorem_id", "theorem", "formula_or_condition", "implication", "status"])}

## Component Zero/Norm Matrix
{md_table(tables["components"], ["component_id", "symbol", "channel", "zero_rule", "bound_rule", "status"])}

## Nlock to DvGamma Handoff
{md_table(tables["handoff"], ["handoff_id", "quantity", "formula", "role", "status"])}

## EM/Poynting Guard
{md_table(tables["em"], ["guard_id", "rule", "consequence", "status"])}

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

    add("VAL4303_0_sources_exist", "all cited local source paths exist", all(Path(row["source_path"]).exists() for row in tables["sources"]), "source_register")
    add("VAL4303_1_needles_found", "all source needles found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4303_2_visible_theorem", "visible-Hilbert silence theorem row exists", any(row["theorem_id"] == "VHS4303_0_action_split" for row in tables["theorem"]), "theorem_rows")
    add("VAL4303_3_poynting_guard", "Poynting is routed as Hilbert or residual", any(row["guard_id"] == "EMG4303_0_poynting_route" for row in tables["em"]), "em_guard_rows")
    add("VAL4303_4_primary_norms", "N_src and N_inner component rows exist", all(any(row["symbol"] == symbol for row in tables["components"]) for symbol in ["N_src", "N_inner"]), "component_matrix")
    add("VAL4303_5_handoff", "C4302 handoff row exists", any(row["quantity"] == "C4302_DVGAMMA_QUAD" for row in tables["handoff"]), "handoff_rows")
    add(
        "VAL4303_6_claim_flags_false",
        "all generated rows keep claim flags false",
        all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for table in tables.values() for row in table),
        "generated_tables",
    )
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4303_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4303_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "generated_docs")
    add("VAL4303_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims_register")
    add("VAL4303_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "unification_spine")
    add("VAL4303_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "private_packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4303_SOURCE_REGISTER.csv",
        "theorem": SOURCE_DIR / "P8_Y5_R2FR_4303_VISIBLE_HILBERT_M_LOCK_SILENCE_THEOREM.csv",
        "components": SOURCE_DIR / "P8_Y5_R2FR_4303_COMPONENT_ZERO_NORM_MATRIX.csv",
        "handoff": SOURCE_DIR / "P8_Y5_R2FR_4303_NLOCK_TO_DVGAMMA_HANDOFF.csv",
        "em": SOURCE_DIR / "P8_Y5_R2FR_4303_EM_POYNTING_GUARD.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4303_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4303_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4303_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4303_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "theorem": silence_theorem_rows(),
        "components": component_matrix_rows(),
        "handoff": handoff_rows(),
        "em": em_guard_rows(),
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
## PPC4161 4303 source-boundary silence or component norms for m-lock

Marker: `{MARKER}`

4303 derives the clean conditional theorem for `J_eff/B_m`: visible matter plus Maxwell-Hodge/Poynting are silent in the `m`-lock equation when they factor only through the same observed Hilbert action before readout. Non-Hilbert source support, inner `m` charge, hidden EM/Hodge/current markers, transition/history and boundary/domain terms remain as absolute component norms feeding the 4302 quadratic Gamma row.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4303 packet source-boundary silence gate

Marker: `{PACKET_MARKER}`

Packet update: the source-boundary forcing is split into a conditional visible-Hilbert zero branch and retained non-Hilbert norm rows. Poynting is treated as Maxwell Hilbert stress when owned, otherwise as a residual norm; no double-counting is allowed.
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
