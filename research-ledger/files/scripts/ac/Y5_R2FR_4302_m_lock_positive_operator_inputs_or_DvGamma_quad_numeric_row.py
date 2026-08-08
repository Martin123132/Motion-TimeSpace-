from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4302"
CLAIM_ID = "L-143"
BRANCH = "MTS_R2FR_Y5_M_LOCK_COERCIVITY_GAP_AND_DVGAMMA_QUAD_INPUT_PACK_4302"
DECISION = "M_LOCK_COERCIVITY_GAP_DERIVED_QUADRATIC_DVGAMMA_PACK_READY_VALUES_MISSING_NONCLAIM"
MARKER = "PPC4161_M_LOCK_COERCIVITY_GAP_AND_DVGAMMA_QUAD_INPUT_PACK_4302"
PACKET_MARKER = "PPC4161_PACKET_M_LOCK_COERCIVITY_GAP_AND_DVGAMMA_QUAD_INPUT_PACK_4302"
NEXT_TARGET = "4303-Y5-R2FR-source-boundary-component-norms-or-exact-silence-for-m-lock.md"

FORMAL_PATH = FORMAL / "318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md"
DOC_PATH = POST / "4302-Y5-R2FR-m-lock-positive-operator-inputs-or-DvGamma-quad-numeric-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4302_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4302_00_4301_formal": (
        FORMAL / "317-PPC4161-parent-double-zero-lock-or-second-order-DvGamma-bound-row.md",
        "Next target: `4302-Y5-R2FR-m-lock-positive-operator-inputs-or-DvGamma-quad-numeric-row.md`.",
        "4301 handoff to m-lock positive operator inputs or quadratic DvGamma row.",
    ),
    "SRC4302_01_4301_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4301_PARENT_LOCK_CONTRACT.csv",
        "PLC4301_4_gap_and_boundary",
        "4301 positive-gap/source-boundary clause.",
    ),
    "SRC4302_02_4301_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4301_SECOND_ORDER_DVGAMMA_BOUND_ROWS.csv",
        "BQ4301_3_DvGamma_quad",
        "4301 quadratic DvGamma bound template.",
    ),
    "SRC4302_03_1534_nohair": (
        POST / "1534-Y5-local-memory-locking-nohair-or-leakage-bound.md",
        "NH1534_3_exact_nohair",
        "Earlier local memory no-hair energy identity.",
    ),
    "SRC4302_04_1536_nlock": (
        POST / "1536-Y5-Jeff-Bm-source-boundary-silence-or-bound.md",
        "NLOCK1536_5_lock_norm",
        "J_eff/B_m absolute-sum leakage envelope.",
    ),
    "SRC4302_05_1978_gap": (
        POST / "1978-Y5-R2FR-memory-mass-gap-and-mL-derivative-bound-pack.md",
        "G_m := Z_min lambda_1(D_loc)+M2_min-Eta_H > 0",
        "Memory Hessian inverse and coercive mass-gap formula.",
    ),
    "SRC4302_06_1978_values": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1978_MEMORY_MASS_GAP_PACK.csv",
        "MG1978_5_inverse_bound",
        "Executable H_m inverse formula with missing values.",
    ),
    "SRC4302_07_3339_em": (
        POST / "3339-Y5-R2FR-parent-source-coupling-decomposition-under-AX1090.md",
        "EM3339_3_poynting_stress_readout",
        "Poynting/EM stress is a Hilbert-source readout only inside the Maxwell-Hodge route.",
    ),
    "SRC4302_08_3340_hilbert": (
        POST / "3340-Y5-R2FR-parent-Hilbert-source-clause-or-finite-residual-vector-under-AX1090.md",
        "HSC3340_4_public_Maxwell_Hodge",
        "Parent Hilbert source clause and EM/Hodge side-channel guard.",
    ),
    "SRC4302_09_4293_thresholds": (
        SOURCE_DIR / "P8_Y5_R2FR_4293_REQUIRED_SUPPRESSION_ROWS.csv",
        "REQ4293_WEP",
        "Shared local suppression thresholds imported from the transition residual runner.",
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
        for row in rows:
            writer.writerow(row)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


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
            "4302 derives the m-lock coercivity gate rather than merely naming missing inputs. "
            "For L_m u=-nabla_i(Z_m h^{ij}nabla_j u)+M_m^2u+Delta_H[u], the local branch has "
            "lambda_m=Z_min lambda_1(D_loc)+M2_min-Eta_H when the domain/zero-mode class is parent-owned. "
            "If lambda_m>0 and J_eff=B_m=0, the 4301 exact no-hair branch fires; otherwise the fallback is "
            "a quadratic D_v Gamma_eff bound with Delta_m, Delta_Dv_m, F_2, Lmin, projector norm and "
            "source/boundary terms carried as explicit rows."
        ),
        (
            "4302 source register, coercivity-gap derivation, source-boundary input pack, F2/DvGamma "
            "quadratic row, local arena suppression map, decision, firewall, status, next-target and validation CSV."
        ),
        "private_m_lock_coercivity_gap_formula_nonclaim_values_missing",
        (
            "Source or derive Z_min, M2_min/M2_bar, lambda_1(D_loc), Eta_H, J_eff/B_m component norms or "
            "silence, F_2, Lmin, projector norm, a_ref and EM/Poynting side-channel ownership before scoring."
        ),
        (
            "Treating lambda_m formula as a numeric value, claiming exact no-hair while J_eff/B_m remain open, "
            "double-counting Poynting outside Hilbert EM stress, or promoting Gamma trace silence to full local GR."
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


def coercivity_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "CG4302_0_operator_form",
            "m-lock Hessian operator",
            "L_m u=-nabla_i(Z_m h^{ij}nabla_j u)+M_m^2 u+Delta_H[u]",
            "Imports the 1978 H_m operator into the 4301 m-lock notation.",
            "OPERATOR_FORM_ALIGNED",
        ),
        (
            "CG4302_1_coercive_gap",
            "lambda_m theorem",
            "lambda_m := Z_min*lambda_1(D_loc)+M2_min-Eta_H",
            "If Z_m>=Z_min>0, M_m^2>=M2_min, <u,Delta_H u> >= -Eta_H||u||^2, and ||grad u||^2>=lambda_1||u||^2, then <u,L_m u> >= lambda_m||u||^2.",
            "COERCIVITY_FORMULA_DERIVED",
        ),
        (
            "CG4302_2_mass_only_gap",
            "zero-mode-safe mass branch",
            "lambda_m := M2_min-Eta_H when the mass term controls the zero mode",
            "A strictly positive memory Hessian can lock constant modes even when the Poincare gap is unavailable.",
            "ALTERNATE_COERCIVITY_ROUTE",
        ),
        (
            "CG4302_3_exact_nohair",
            "exact m-lock",
            "lambda_m>0 and J_eff=0 and B_m=0 and N(u) nonpositive/silent => u=0",
            "This is the exact branch that would fire the 4300/4301 Gamma double-zero theorem.",
            "CONDITIONAL_EXACT_ZERO_THEOREM",
        ),
        (
            "CG4302_4_finite_field_bound",
            "Delta_m fallback",
            "Delta_m <= (N_J2+N_B2+N_N2)/lambda_m, or Delta_m <= C_emb*N_lock in the 1536 energy norm",
            "If source/boundary terms survive, the route becomes a finite leakage bound rather than no-hair.",
            "BOUND_FORMULA_READY_VALUES_MISSING",
        ),
        (
            "CG4302_5_vertical_bound",
            "Delta_Dv_m fallback",
            "Delta_Dv_m <= (N_DvJ+N_DvB+N_DvN+N_DvL*Delta_m)/lambda_m",
            "Differentiating L_m u=J_eff+B_m+N(u) gives the vertical profile needed by D_v Gamma_eff.",
            "VERTICAL_BOUND_FORMULA_READY_VALUES_MISSING",
        ),
        (
            "CG4302_6_failure_mode",
            "claim gate",
            "lambda_m<=0 or unsourced J_eff/B_m leaves the m-lock branch unproved",
            "This prevents positivity language from becoming a hidden closure axiom.",
            "NO_CLAIM_IF_VALUES_MISSING",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, object_name, formula, result, status in specs:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object": object_name,
                "formula": formula,
                "result": result,
                "status": status,
                "parent_signed": "False" if "CONDITIONAL" in status or "MISSING" in status or "NO_CLAIM" in status else "conditional",
            }
        )
        rows.append(row)
    return rows


def source_boundary_rows() -> List[Dict[str, str]]:
    specs = [
        ("IP4302_0_Zmin", "Z_min", "kinetic ellipticity lower bound", "MISSING_SOURCE_VALUE_OR_THEOREM", "needed for lambda_m and stress normalization"),
        ("IP4302_1_M2min", "M2_min", "memory Hessian lower bound", "MISSING_SOURCE_VALUE_OR_THEOREM", "needed for lambda_m and zero-mode control"),
        ("IP4302_2_M2bar", "M2_bar", "memory Hessian upper bound", "MISSING_SOURCE_VALUE_OR_THEOREM", "needed for F_2/V_mA and quadratic leakage size"),
        ("IP4302_3_lambda1", "lambda_1(D_loc)", "first positive eigenvalue/Poincare gap", "MISSING_DOMAIN_SPECTRUM", "needed for coercivity on the parent local collar"),
        ("IP4302_4_EtaH", "Eta_H", "negative source/boundary/operator correction norm", "MISSING_CORRECTION_BOUND", "subtracts from the coercive gap"),
        ("IP4302_5_NJ", "N_J", "absolute dual norm for J_eff components", "MISSING_COMPONENT_NORMS", "needed for Delta_m leakage"),
        ("IP4302_6_NB", "N_B", "absolute boundary norm for B_m components", "MISSING_COMPONENT_NORMS", "needed for Delta_m leakage"),
        ("IP4302_7_NDv", "N_DvJ,N_DvB,N_DvL,N_DvN", "vertical source/operator variation norms", "MISSING_VERTICAL_COMPONENT_NORMS", "needed for Delta_Dv_m"),
        ("IP4302_8_EM", "N_EM_or_zero", "EM/Poynting contribution to source forcing", "ZERO_ONLY_IF_MAXWELL_HODGE_HILBERT_OWNED_OTHERWISE_BOUND", "keeps Poynting as Hilbert stress, not a second background force"),
        ("IP4302_9_projection", "N_P,a_ref,Lmin,C_proj", "observable projection and Gamma normalization constants", "MISSING_PROJECTION_CONSTANTS", "needed to compare C4302_DVGAMMA_QUAD to local arenas"),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, symbol, role, status, needed_for in specs:
        row = base_row()
        row.update(
            {
                "input_id": row_id,
                "symbol": symbol,
                "role": role,
                "status": status,
                "needed_for": needed_for,
                "current_value": "MISSING_NUMERIC_OR_PARENT_SIGNED_ZERO",
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def f2_quad_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DQ4302_0_F2_identity",
            "F_2",
            "If F_vac(m)=V(m)-V(m_*), then F_2=partial_m^2F_vac(m_*)=V''(m_*)=M2_* in the same normalization.",
            "IDENTITY_DERIVED_NUMERIC_VALUE_MISSING",
            "M2_* or bounded M2_bar with units",
        ),
        (
            "DQ4302_1_Delta_m",
            "Delta_m",
            "Delta_m <= (N_J2+N_B2+N_N2)/lambda_m or C_emb*N_lock.",
            "FORMULA_READY_VALUES_MISSING",
            "lambda_m plus source/boundary norms",
        ),
        (
            "DQ4302_2_Delta_Dv_m",
            "Delta_Dv_m",
            "Delta_Dv_m <= (N_DvJ+N_DvB+N_DvN+N_DvL*Delta_m)/lambda_m.",
            "FORMULA_READY_VALUES_MISSING",
            "vertical component norms",
        ),
        (
            "DQ4302_3_Dv_ln_Lcg",
            "Delta_Dv_ln_Lcg",
            "zero if L_cg is fixed/q-basic on the branch; otherwise source-bound it separately.",
            "ZERO_OR_BOUND_GATE_RETAINED",
            "fixed-Lcg theorem or finite row",
        ),
        (
            "DQ4302_4_Cquad",
            "C4302_DVGAMMA_QUAD",
            "C_quad <= N_P/a_ref * Lmin^-2*|F_2|*(Delta_m*Delta_Dv_m + Delta_m^2*Delta_Dv_ln_Lcg)+C_proj_derivative.",
            "RUNNER_ROW_READY_NOT_SCORE_READY",
            "all input rows source-backed and units consistent",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, symbol, formula, status, required in specs:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "formula": formula,
                "status": status,
                "required_inputs": required,
                "current_value": "MISSING_NUMERIC_OR_PARENT_SIGNED_ZERO",
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def arena_rows() -> List[Dict[str, str]]:
    arenas = [
        ("ARENA4302_WEP", "WEP/composition", "C4302_DVGAMMA_QUAD projected through Y_WEP must meet the 4293 WEP suppression row", "REQ4293_WEP"),
        ("ARENA4302_PPN_GAMMA", "PPN gamma", "projected Gamma trace leakage must fit gamma residual budget", "REQ4293_gamma"),
        ("ARENA4302_PPN_BETA", "PPN beta", "quadratic Gamma leakage must not mimic beta source nonlinearity", "REQ4293_beta"),
        ("ARENA4302_CLOCK", "clock/time", "vertical m/Lcg drift must stay below clock redshift/frequency residual row", "REQ4293_clock"),
        ("ARENA4302_ORBIT", "orbital/Newton", "residual source-coupling or range hair must not exceed calibrated-G orbital budget", "REQ4293_orbit"),
        ("ARENA4302_GDOT", "Gdot/time drift", "static-degenerate or time-drift branch must be separated before Gdot scoring", "REQ4293_Gdot"),
        ("ARENA4302_R10", "R10/fifth-force", "finite-range mapping from Gamma leakage to alpha(lambda) is still required", "REQ4293_R10"),
        ("ARENA4302_EM", "Maxwell/EM stress", "EM/Poynting is safe only as same Hilbert Maxwell-Hodge stress; hidden Hodge/current/F2 residuals enter N_J", "HSC3340_4_public_Maxwell_Hodge"),
    ]
    rows: List[Dict[str, str]] = []
    for arena_id, arena, rule, source_ref in arenas:
        row = base_row()
        row.update(
            {
                "arena_id": arena_id,
                "arena": arena,
                "suppression_rule": rule,
                "source_ref": source_ref,
                "status": "MISSING_PROJECTION_AND_INPUT_VALUES",
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DEC4302_0_gain",
            "COERCIVE_GAP_FORMULA_DERIVED",
            "The missing lambda_m is no longer abstract: lambda_m=Z_min lambda_1(D_loc)+M2_min-Eta_H, with a mass-only variant.",
            "Use this as the exact acceptance contract for m-lock.",
        ),
        (
            "DEC4302_1_limit",
            "VALUES_MISSING_NO_EXACT_LOCK",
            "The corpus still lacks parent-signed Z/M/domain/source/boundary values, so exact no-hair is not claimable.",
            "Keep local-GR and Gamma trace claims blocked.",
        ),
        (
            "DEC4302_2_bound_route",
            "QUADRATIC_DVGAMMA_ROW_READY_NOT_SCORE_READY",
            "F_2 is tied to the memory Hessian identity and Delta_m/Delta_Dv_m have formulas, but no numerical/source-backed row exists.",
            "Fill component norms and projection constants before any arena comparison.",
        ),
        (
            "DEC4302_3_next",
            "SOURCE_BOUNDARY_COMPONENT_NORMS_FIRST",
            "J_eff/B_m decide both exact no-hair and the fallback leakage size; EM/Poynting is retained as a Hilbert-source side-channel gate.",
            NEXT_TARGET,
        ),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, decision, reason, next_action in specs:
        row = base_row()
        row.update({"decision_id": row_id, "decision_result": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    rules = [
        "Do not treat lambda_m=Z_min*lambda_1+M2_min-Eta_H as a sourced positive number until every term has a source/domain row.",
        "Do not claim exact no-hair unless J_eff and B_m are zero componentwise or bounded to zero by a parent theorem.",
        "Do not double-count Poynting: inside the clean branch it is Hilbert EM stress; outside it is a source residual norm.",
        "Do not score C4302_DVGAMMA_QUAD while F_2, Delta_m, Delta_Dv_m, Lmin, N_P/a_ref and projection constants are missing.",
        "Do not use Gamma trace locking to erase D_v K_hat, connection, boundary, transition-shell or matter/source residuals.",
    ]
    rows: List[Dict[str, str]] = []
    for index, rule in enumerate(rules):
        row = base_row()
        row.update({"firewall_id": f"FW4302_{index}", "rule": rule, "status": "ACTIVE"})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4302_0_lambda_formula", "lambda_m formula", "FORMULA_DERIVED_VALUES_MISSING", "real progress: coercivity criterion is exact but not numeric"),
        ("STAT4302_1_exact_lock", "m=m_* exact lock", "BLOCKED_NONCLAIM", "source/boundary/component silence is not parent-signed"),
        ("STAT4302_2_quadratic_bound", "D_v Gamma quadratic fallback", "ROW_READY_NOT_SCORE_READY", "inputs and projection constants missing"),
        ("STAT4302_3_EM", "EM/Poynting side channel", "RETAINED_AS_HILBERT_OR_BOUND_GATE", "prevents Poynting intuition becoming a double-counted source"),
        ("STAT4302_4_local_GR", "local GR/Newton/PPN/R10", "BLOCKED_NONCLAIM", "Khat/connection/boundary/matter gates remain open"),
    ]
    rows: List[Dict[str, str]] = []
    for status_id, item, status, note in specs:
        row = base_row()
        row.update({"status_id": status_id, "item": item, "status": status, "note": note})
        rows.append(row)
    return rows


def next_target_rows() -> List[Dict[str, str]]:
    row = base_row()
    row.update(
        {
            "next_target_id": "NT4302_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can J_eff/B_m be made zero by the parent source/Hilbert/Maxwell-Hodge branch, or filled as finite component norms for Delta_m?",
            "preferred_route": "prove componentwise source-boundary silence for the m-lock equation",
            "fallback_route": "source finite absolute component norms N_J,N_B,N_DvJ,N_DvB and run C4302_DVGAMMA_QUAD against 4293 arenas",
        }
    )
    return [row]


def write_docs(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal_text = f"""# 318 PPC4161 m-lock coercivity gap and DvGamma quadratic input pack

Marker: `{MARKER}`

## Decision

`{DECISION}`

4302 does not merely repeat that `lambda_m` is missing. It derives the exact coercive object that a future parent action must sign:

```text
L_m u = -nabla_i(Z_m h^ij nabla_j u) + M_m^2 u + Delta_H[u],
lambda_m = Z_min lambda_1(D_loc) + M2_min - Eta_H.
```

If `lambda_m>0` and the source/boundary forcing is silent, then the 4301 no-hair branch locks `u=delta m=0`. If the forcing survives, the route is a finite quadratic `D_v Gamma_eff` bound, not a local-GR claim.

## Coercivity Gap Derivation

{md_table(tables["coercivity"], ["row_id", "object", "formula", "status"])}

## Source/Boundary Input Pack

{md_table(tables["inputs"], ["input_id", "symbol", "role", "status", "needed_for"])}

## F2 and Quadratic DvGamma Row

{md_table(tables["quad"], ["row_id", "symbol", "formula", "status"])}

## Local Arena Suppression Map

{md_table(tables["arena"], ["arena_id", "arena", "suppression_rule", "status"])}

## Result

The strongest private result is now:

```text
<u,L_m u> >= lambda_m ||u||^2,
lambda_m = Z_min lambda_1(D_loc)+M2_min-Eta_H.
```

This is enough to make the lock theorem mathematically exact once the parent signs the operator/domain/source terms. It is not enough to claim local GR because the values and source/boundary silence are not signed.

Next target: `{NEXT_TARGET}`.
"""

    doc_text = f"""# 4302 - m-lock positive operator inputs or DvGamma quadratic numeric row

## Verdict
- The `m`-lock bottleneck moved forward: `lambda_m` now has an exact coercive formula rather than a vague missing slot.
- Exact no-hair remains nonclaim because `J_eff`, `B_m`, domain/zero-mode and numeric/source values are still unsigned.
- The fallback route is now runner-shaped: `F_2`, `Delta_m`, `Delta_Dv_m`, `Delta_Dv_ln_Lcg`, projection constants, and EM/Poynting side-channel ownership are explicit.
- Poynting is not ignored: in the clean route it is Maxwell-Hodge Hilbert stress; otherwise it enters the source residual norm.
- No local-GR/Newton/PPN/R10/Maxwell claim follows from this checkpoint.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Coercivity Gap
{md_table(tables["coercivity"], ["row_id", "object", "formula", "result", "status"])}

## Source/Boundary Inputs
{md_table(tables["inputs"], ["input_id", "symbol", "role", "status", "needed_for"])}

## F2 and DvGamma Quadratic Row
{md_table(tables["quad"], ["row_id", "symbol", "formula", "status", "required_inputs"])}

## Arena Map
{md_table(tables["arena"], ["arena_id", "arena", "suppression_rule", "source_ref", "status"])}

## Decision
{md_table(tables["decision"], ["decision_id", "decision_result", "reason", "next_action"])}

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
    except Exception as exc:  # pragma: no cover - validation report path
        return False, f"{path.name} failed to parse: {exc}"


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        row = base_row()
        row.update({"check_id": check_id, "description": description, "passed": str(passed), "evidence": evidence})
        rows.append(row)

    source_ok = all(Path(row["source_path"]).exists() for row in tables["sources"])
    needles_ok = all(row["needle_found"] == "True" for row in tables["sources"])
    add("VAL4302_0_sources_exist", "all cited local source paths exist", source_ok, "source_register")
    add("VAL4302_1_needles_found", "all cited source needles are present", needles_ok, "source_register")
    add(
        "VAL4302_2_lambda_formula",
        "coercivity gap formula row exists",
        any(row["row_id"] == "CG4302_1_coercive_gap" for row in tables["coercivity"]),
        "P8_Y5_R2FR_4302_COERCIVITY_GAP_DERIVATION.csv",
    )
    add(
        "VAL4302_3_exact_lock_blocked",
        "exact lock remains conditional/nonclaim",
        any(row["status"] == "CONDITIONAL_EXACT_ZERO_THEOREM" for row in tables["coercivity"]),
        "coercivity_rows",
    )
    add(
        "VAL4302_4_F2_identity",
        "F2 identity row exists",
        any(row["row_id"] == "DQ4302_0_F2_identity" for row in tables["quad"]),
        "P8_Y5_R2FR_4302_F2_AND_DVGAMMA_QUAD_ROW.csv",
    )
    add(
        "VAL4302_5_EM_guard",
        "EM/Poynting side channel retained",
        any(row.get("symbol") == "N_EM_or_zero" for row in tables["inputs"])
        and any(row.get("arena") == "Maxwell/EM stress" for row in tables["arena"]),
        "input_pack_and_arena_map",
    )
    add(
        "VAL4302_6_claim_flags_false",
        "all generated rows keep claim flags false",
        all(
            row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False"
            for table in tables.values()
            for row in table
        ),
        "generated_tables",
    )
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4302_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4302_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "generated_docs")
    add("VAL4302_claim_row", f"{CLAIM_ID} claim-register row is present", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims_register")
    add("VAL4302_spine_marker", "spine marker is present", MARKER in read_text(FORMAL / "07-unification-spine.md"), "unification_spine")
    add("VAL4302_packet_marker", "packet marker is present", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "private_packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4302_SOURCE_REGISTER.csv",
        "coercivity": SOURCE_DIR / "P8_Y5_R2FR_4302_COERCIVITY_GAP_DERIVATION.csv",
        "inputs": SOURCE_DIR / "P8_Y5_R2FR_4302_SOURCE_BOUNDARY_INPUT_PACK.csv",
        "quad": SOURCE_DIR / "P8_Y5_R2FR_4302_F2_AND_DVGAMMA_QUAD_ROW.csv",
        "arena": SOURCE_DIR / "P8_Y5_R2FR_4302_LOCAL_ARENA_SUPPRESSION_MAP.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4302_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4302_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4302_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4302_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }

    tables = {
        "sources": source_rows(),
        "coercivity": coercivity_rows(),
        "inputs": source_boundary_rows(),
        "quad": f2_quad_rows(),
        "arena": arena_rows(),
        "decision": decision_rows(),
        "firewall": firewall_rows(),
        "status": status_rows(),
        "next": next_target_rows(),
    }

    for key, rows in tables.items():
        write_csv(paths[key], rows)

    write_docs(paths, tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4302 m-lock coercivity gap and DvGamma quadratic input pack

Marker: `{MARKER}`

4302 turns `lambda_m` from a missing word into the exact coercive gate `lambda_m=Z_min lambda_1(D_loc)+M2_min-Eta_H`. Exact Gamma trace silence follows only if this gap is positive and `J_eff/B_m` are silent; otherwise the fallback is the explicit `C4302_DVGAMMA_QUAD` row. EM/Poynting is kept as Hilbert Maxwell-Hodge stress or as a source residual, not double-counted.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4302 packet m-lock coercivity gap

Marker: `{PACKET_MARKER}`

Packet update: the next proof target is no longer vague positivity. The local m-lock requires `lambda_m=Z_min lambda_1(D_loc)+M2_min-Eta_H>0` plus source/boundary silence. If that fails, the Gamma trace branch must be scored through the quadratic `D_v Gamma_eff` input pack.
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
