from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3888"
BRANCH = "MTS_R2FR_Y5_NO_LINEAR_SOURCE_AND_RESIDUAL_LOCK_OR_FIRST_COEFFICIENT_FILL_3888"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3888-Y5-R2FR-no-linear-source-and-residual-lock-or-first-coefficient-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3887_NEXT = OUT / "P8_Y5_R2FR_3887_NEXT_TARGET.csv"
CSV_3887_THEOREM = OUT / "P8_Y5_R2FR_3887_YLOC_EULER_ZERO_THEOREM_ATTEMPT.csv"
CSV_3887_CLAUSES = OUT / "P8_Y5_R2FR_3887_PARENT_ACTION_CLAUSE_REQUIREMENTS.csv"
CSV_3887_FILL = OUT / "P8_Y5_R2FR_3887_R11_PPN_COEFFICIENT_FILL_PIVOT.csv"
CSV_3887_VALIDATION = OUT / "P8_Y5_BRR545_3887_VALIDATION.csv"
CSV_3883_HILBERT = OUT / "P8_Y5_R2FR_3883_SAME_HILBERT_SOURCE_LOCK.csv"
CSV_2570_MATTER_DESCENT = OUT / "P8_Y5_FIELD_QUOTIENT_2570_MATTER_DESCENT_GATE.csv"
CSV_2570_DQ = OUT / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv"
CSV_2611_MATTER = OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_MATTER_WORLDTUBE_DESCENT_ATTEMPT.csv"
CSV_2611_SOURCE_ZERO = OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_SOURCE_ZERO_STATUS.csv"
CSV_2612_GRAMMAR = OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv"
CSV_2612_SOURCE_ZERO = OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_ZERO_STATUS.csv"
CSV_2612_GATES = OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_CLAIM_GATES.csv"
CSV_3886_FAMILY = OUT / "P8_Y5_R2FR_3886_R11_FAMILY_SELECTOR_OR_FILL_MATRIX.csv"
CSV_LOCAL_LOCK = OUT / "P8_Y5_BRR545_LOCAL_LOCK_MAP.csv"
CSV_BOUNDARY_FILL = OUT / "P8_R11_BOUNDARY_STRESS_CLOSURE_FILL_PACK.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3888_SOURCE_REGISTER.csv",
    "derivation": OUT / "P8_Y5_R2FR_3888_QUOTIENT_NO_LINEAR_SOURCE_DERIVATION.csv",
    "channels": OUT / "P8_Y5_R2FR_3888_SOURCE_CHANNEL_SPLIT.csv",
    "residual_lock": OUT / "P8_Y5_R2FR_3888_RESIDUAL_LOCK_ATTEMPT.csv",
    "bounds": OUT / "P8_Y5_R2FR_3888_FIRST_COEFFICIENT_BOUND_INTERFACE.csv",
    "gate": OUT / "P8_Y5_R2FR_3888_LOCAL_GR_DECISION_GATE.csv",
    "runner": OUT / "P8_Y5_R2FR_3888_RUNNER_UPDATE.csv",
    "next": OUT / "P8_Y5_R2FR_3888_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3888_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3888_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3888_00_next", CSV_3887_NEXT, "NEXT3887_0", "3887 selected no-linear-source/residual-lock target"),
    ("SRC3888_01_theorem", CSV_3887_THEOREM, "YZT3887_3_zero_result", "Yloc no-hair theorem requiring J_A=0"),
    ("SRC3888_02_clauses", CSV_3887_CLAUSES, "PAC3887_2_matter_neutrality", "matter neutrality clause"),
    ("SRC3888_03_fill", CSV_3887_FILL, "FILL3887_0_boundary_alpha3", "first coefficient fallback rows"),
    ("SRC3888_04_valid", CSV_3887_VALIDATION, "VAL3887_15_next_target", "3887 validation"),
    ("SRC3888_05_hilbert", CSV_3883_HILBERT, "HSL3883_0_action", "same Hilbert source matter action"),
    ("SRC3888_06_2570_matter", CSV_2570_MATTER_DESCENT, "MD2570_0_chain_rule", "quotient matter descent chain rule"),
    ("SRC3888_07_2570_dq", CSV_2570_DQ, "DQ2570_0_chain_rule_template", "vertical generator template"),
    ("SRC3888_08_2611_matter", CSV_2611_MATTER, "MWD2611_1_conditional_theorem", "matter worldtube descent theorem"),
    ("SRC3888_09_2611_source", CSV_2611_SOURCE_ZERO, "SZ2611_0_matter", "matter source-zero status"),
    ("SRC3888_10_2612_grammar", CSV_2612_GRAMMAR, "NDV2612_1_allowed_syntax", "allowed matter syntax"),
    ("SRC3888_11_2612_source", CSV_2612_SOURCE_ZERO, "SZ2612_0_no_direct_vertex", "direct matter grammar source status"),
    ("SRC3888_12_2612_gates", CSV_2612_GATES, "GATE2612_0_no_direct_vertex", "direct matter grammar gates"),
    ("SRC3888_13_R11_family", CSV_3886_FAMILY, "R11F3886_09_projector_domain_stress", "R11 family selector/fill matrix"),
    ("SRC3888_14_local_lock", CSV_LOCAL_LOCK, "BRL547_0_boundary_alpha3", "source-backed local bound interface"),
    ("SRC3888_15_boundary_fill", CSV_BOUNDARY_FILL, "F6_projector_stress", "projector stress fill row"),
]

MATTER_ACTION = "S_matter = S_bar[Psi, e_obs(q(Phi)), omega[e_obs(q(Phi))], theta_obs(q(Phi))]"
CHAIN_RULE = "delta_y S_matter = (delta S/d e_obs) D e_obs[Dq[y]] + (delta S/d theta_obs) D theta_obs[Dq[y]] + direct_hidden_terms"
NO_SOURCE_RESULT = "If y in ker(Dq), e_obs and theta_obs are q-basic, and direct_hidden_terms=0, then J_A^obs := delta S_matter/delta y^A|_0 = 0"


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


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        cells = [str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


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
                "claim_use": "nonclaim_no_linear_source_residual_lock_or_bounds",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def derivation_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("NLS3888_0_action", "ordinary matter descends through observed variables", MATTER_ACTION, "CANDIDATE_FROM_3883_AND_2570", "matter action itself is candidate/adopted locally but parent object language remains unsigned"),
        ("NLS3888_1_vertical", "define source-neutral directions as quotient-vertical", "y^A vertical iff Dq[y^A]=0 and y^A is not a public metric/coframe variation", "EXACT_DEFINITION", "some current residuals are not proven vertical, especially projector, boundary, memory and source-normalization directions"),
        ("NLS3888_2_chain_rule", "vary observed matter along y", CHAIN_RULE, "EXACT_CHAIN_RULE", "direct hidden terms and source-only prefactors survive unless grammar forbids them"),
        ("NLS3888_3_observed_zero", "observed ordinary matter gives no linear source along true vertical directions", NO_SOURCE_RESULT, "DERIVED_CONDITIONAL_JOBS_ZERO", "this only zeros J_A^obs, not boundary/worldtube/direct-hidden/projector channels"),
        ("NLS3888_4_same_Hilbert", "same Hilbert source prevents a second source definition from reintroducing J_A^obs", "T_H is varied from the same S_matter before Pi_M/readout; no post-fit GM source slot is allowed in J_A^obs", "DERIVED_CONDITIONAL_SAME_SOURCE_SUPPORT", "Pi_M/source-normalization and worldtube support still need residual-lock"),
        ("NLS3888_5_verdict", "no-linear-source route status", "J_A = J_A^obs + J_A^direct + J_A^worldtube + J_A^boundary + J_A^memory + J_A^projector; 3888 derives J_A^obs=0 conditionally only", "PARTIAL_SOURCE_NEUTRALITY_ADVANCED", "local GR remains blocked until every non-observed channel is zeroed or bounded"),
    ]
    return [
        {
            "derivation_id": row_id,
            "step": step,
            "math": math,
            "result": result,
            "remaining_failure": failure,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, step, math, result, failure in raw_rows
    ]


def channel_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("SRCCH3888_0_observed_matter", "J_A^obs", "ordinary matter/EM through e_obs(q), theta_obs(q)", "J_A^obs=0 if y in ker(Dq) and readouts are q-basic", "CONDITIONAL_ZERO_DERIVED", "needs parent q/readout ownership"),
        ("SRCCH3888_1_direct_hidden", "J_A^direct", "direct V_m[X], hidden frame, marker, alpha/mass or source-prefactor slot", "zero only if object-language grammar forbids the slot", "OPEN_COUNTERMODEL_SURVIVES", "2612 grammar not parent-signed"),
        ("SRCCH3888_2_relative_weight", "delta_w_A", "species/source relative prefactor", "common prefactor calibrates away; relative prefactor does not", "OPEN_WEP_SOURCE_RISK", "Hom/no-marker theorem or bounds needed"),
        ("SRCCH3888_3_worldtube", "J_A^worldtube", "source support/worldtube/readout boundary dependence", "zero if Hilbert support and tau/readout descend through q", "OPEN_SUPPORT_OWNER", "worldtube owner unsigned"),
        ("SRCCH3888_4_boundary", "J_A^boundary", "inner/outer collar, reference, corner or flux term", "zero only by no-flux/topological theorem or retained bound", "OPEN_BOUNDARY_CHANNEL", "alpha3/xi/Gdot rows live"),
        ("SRCCH3888_5_memory", "J_A^memory", "history/nonlocal/private clock-frame response", "zero if compact local memory kernel becomes q-basic/local silent", "OPEN_NONLOCAL_CHANNEL", "Gdot/clock/orbital hysteresis risk"),
        ("SRCCH3888_6_projector", "J_A^projector", "Pi_M/readout/projector variation or stress", "zero if projector is fixed before variation, q-basic, or topological; otherwise retained stress", "OPEN_PROJECTOR_STRESS", "zeta/gamma/beta/alpha_i risk"),
        ("SRCCH3888_7_R11_factor", "J_A^R11", "non-EH operator coefficient dependence on y", "zero if every c_A(y)=cbar_A Sigma_loc+O(Sigma_loc^2) or topological", "OPEN_UNIVERSAL_FACTORIZATION", "R11/PPN/R10 risk"),
    ]
    return [
        {
            "channel_id": row_id,
            "source_piece": piece,
            "meaning": meaning,
            "zero_or_bound_rule": rule,
            "3888_status": status,
            "residual_risk": risk,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, meaning, rule, status, risk in raw_rows
    ]


def residual_lock_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("RL3888_0_normal_coordinates", "Use y^A as normal coordinates to the quotient fiber: Phi=(q,y) locally.", "If the parent field space admits this split and y directions are in ker(Dq), source neutrality has a real object.", "CONDITIONAL_GEOMETRIC_LOCK", "field-space split and gauge fixing unsigned"),
        ("RL3888_1_physical_residuals", "Identify Y_loc^A with actual residual functionals R^A[Phi] used in PPN/R10/R11 ledgers.", "Prevents a decoy auxiliary zero from replacing physical alpha/gamma/beta/R10 residuals.", "REQUIRED_UNSIGNED", "residual map not proven invertible or complete"),
        ("RL3888_2_metric_readout", "Public g_obs/e_obs must be independent of y to first order on the compact local branch.", "Makes delta_y S_matter vanish rather than produce T_H delta_y g_obs.", "CONDITIONAL_FROM_Q_BASIC_READOUT", "q-basic readout functor not globally parent-signed"),
        ("RL3888_3_projector_readout", "Pi_M and measured mass support must be fixed before variation or descend through q.", "Stops source-normalization/projector stress from reentering as J_A.", "OPEN", "Pi_M/readout order remains live"),
        ("RL3888_4_boundary_worldtube", "Worldtube support and boundary/corner classes must descend through q or be retained as coefficients.", "Closes inner-boundary charge and alpha3/Gdot leakage.", "OPEN", "support and boundary owner unsigned"),
        ("RL3888_5_lock_verdict", "3888 signs a conditional route for J_A^obs=0 but not full residual-lock.", "Useful progress: ordinary matter is not the enemy if it truly sees only q-basic geometry; the enemy is hidden/direct/readout/boundary slots.", "PARTIAL_LOCK_ONLY", "local GR no-claim remains"),
    ]
    return [
        {
            "lock_id": row_id,
            "lock_clause": clause,
            "effect": effect,
            "status": status,
            "remaining_failure": failure,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, clause, effect, status, failure in raw_rows
    ]


def bound_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("BND3888_0_boundary_alpha3", "epsilon_B_flux_abs", "alpha3", "4e-20", "dimensionless", "source-intake\\mts_residuals\\P8_Y5_BRR545_LOCAL_LOCK_MAP.csv:BRL547_0_boundary_alpha3", "prediction coefficient/input missing; bound side filled"),
        ("BND3888_1_boundary_xi", "epsilon_B_flux_abs", "xi", "4e-09", "dimensionless", "source-intake\\mts_residuals\\P8_Y5_BRR545_LOCAL_LOCK_MAP.csv:BRL547_1_boundary_xi", "prediction coefficient/input missing; bound side filled"),
        ("BND3888_2_beta_source", "delta_beta_source", "beta_minus_1", "7.8e-05", "dimensionless", "source-intake\\mts_residuals\\P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv:COEF3886_03_delta_beta_source", "A_source and B_source missing"),
        ("BND3888_3_gamma_R11", "delta_gamma_R11", "gamma_minus_1", "2.3e-05", "dimensionless", "source-intake\\mts_residuals\\P8_Y5_BRR545_LOCAL_LOCK_MAP.csv:BRL547_6_reference_gamma", "weak-field map missing"),
        ("BND3888_4_Gdot", "partial_t K_history_or_boundary", "Gdot_over_G", "9.6e-15", "yr^-1", "source-intake\\mts_residuals\\P8_Y5_BRR545_LOCAL_LOCK_MAP.csv:BRL547_3_boundary_Gdot", "time profile missing"),
        ("BND3888_5_R10_alpha_lambda", "alpha(lambda)", "fifth_force", "alpha(lambda)", "range-dependent", "source-intake\\mts_residuals\\P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv:COEF3886_11_alpha_lambda", "real prediction curve and source charge missing"),
        ("BND3888_6_projector_stress", "T_extra_munu_or_c_projector_domain_stress", "zeta_i;gamma;beta;alpha_i", "component-specific", "stress_or_dimensionless", "source-intake\\mts_residuals\\P8_R11_BOUNDARY_STRESS_CLOSURE_FILL_PACK.csv:F6_projector_stress", "stress vector not yet decomposed"),
    ]
    return [
        {
            "bound_id": row_id,
            "symbol": symbol,
            "observable": observable,
            "bound_value": value,
            "units": units,
            "source_anchor": anchor,
            "prediction_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, observable, value, units, anchor, status in raw_rows
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("LGG3888_0_Yloc_Euler", "3887 positive no-hair identity", "Yloc zero follows if positive/no-source/no-flux/residual-lock hold", "PASS_CONDITIONAL"),
        ("LGG3888_1_observed_matter_source", "J_A^obs", NO_SOURCE_RESULT, "PASS_CONDITIONAL"),
        ("LGG3888_2_direct_hidden_source", "J_A^direct and delta_w_A", "object language forbids direct hidden/source-prefactor slots", "FAIL_UNSIGNED"),
        ("LGG3888_3_worldtube_boundary", "J_A^worldtube + J_A^boundary", "support and boundary descend through q or retained coefficients pass bounds", "FAIL_UNSIGNED"),
        ("LGG3888_4_residual_lock", "Yloc physical residual-lock", "normal coordinates y^A equal actual PPN/R10/R11 residuals", "FAIL_UNSIGNED"),
        ("LGG3888_5_R11_factorization", "universal R11 factorization", "all non-EH operators are Sigma_loc-selected/topological or bounded", "FAIL_UNSIGNED"),
        ("LGG3888_6_bound_interface", "first coefficient bound side", "alpha3/xi/beta/gamma/Gdot/R10/projector bound interface exists", "PASS_BOUND_SIDE_NONCLAIM"),
        ("LGG3888_7_local_GR", "local-GR promotion", "all source, lock, boundary, R11 and coefficient gates close", "BLOCKED_NO_CLAIM"),
    ]
    return [
        {
            "gate_id": row_id,
            "gate": gate,
            "requirement": req,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, req, status in raw_rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("RUNU3888_0_no_source", "J_A_split", "J_A=J_obs+J_direct+J_worldtube+J_boundary+J_memory+J_projector+J_R11; only J_obs has a conditional quotient zero", "IMPLEMENTED_SPLIT"),
        ("RUNU3888_1_vertical_guard", "verticality_guard", "do not apply J_obs=0 unless y in ker(Dq) and readouts are q-basic", "NO_FALSE_VERTICALS"),
        ("RUNU3888_2_direct_guard", "direct_slot_guard", "if direct hidden/source-prefactor slot remains legal, keep A_direct/delta_w rows live", "NO_GRAMMAR_SHORTCUT"),
        ("RUNU3888_3_bound_interface", "bound_side_ready", "bound side exists for alpha3 xi beta gamma Gdot R10 and projector stress; prediction side remains missing", "NONCLAIM_INTERFACE"),
        ("RUNU3888_4_next", "next_attack", "derive parent object-language Hom/no-marker exclusion for direct slots or build prediction-side coefficient rows", "NEXT_3889"),
    ]
    return [
        {
            "update_id": row_id,
            "runner_field": field,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, rule, status in raw_rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3888_0",
            "target_checkpoint": "3889-Y5-R2FR-parent-object-language-no-direct-source-or-prediction-coefficient-fill.md",
            "script": "scripts/Y5_R2FR_3889_parent_object_language_no_direct_source_or_prediction_coefficient_fill.py",
            "objective": "derive a parent object-language/Hom/no-marker exclusion for direct hidden matter/source prefactors; if that fails, fill prediction-side coefficient rows for boundary alpha3, gamma_R11, beta_source, R10 alpha(lambda), Gdot memory and projector stress",
            "why_next": "3888 conditionally zeros ordinary observed matter along true quotient-vertical directions; the remaining live source is direct hidden/source-prefactor/worldtube/boundary/projector structure",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3888_0",
            "branch": BRANCH,
            "summary": "quotient chain-rule derives conditional J_A^obs=0 for ordinary observed matter along true vertical directions; direct hidden/source-prefactor/worldtube/boundary/memory/projector/R11 channels remain live; first bound-side coefficient interface filled as nonclaim",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    derivation: list[dict[str, object]],
    channels: list[dict[str, object]],
    residual_lock: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3888 - No-Linear-Source and Residual-Lock or First Coefficient Fill

Generated: `{timestamp}`

## Result

3888 attacks the actual source term in the `Y_loc` Euler equation.

Matter action form:

`{MATTER_ACTION}`

Chain rule:

`{CHAIN_RULE}`

Conditional source-neutrality result:

`{NO_SOURCE_RESULT}`

This is a real narrowing: ordinary observed matter/EM does not linearly source true quotient-vertical local silence fields. But that is not the whole `J_A`. Direct hidden matter slots, relative source prefactors, worldtube support, boundary flux, memory, projector stress and R11 coefficient dependence remain live unless separately forbidden or bounded.

## Quotient No-Linear-Source Derivation

{markdown_table(derivation, ["derivation_id", "step", "math", "result", "remaining_failure"])}

## Source Channel Split

{markdown_table(channels, ["channel_id", "source_piece", "meaning", "zero_or_bound_rule", "3888_status", "residual_risk"])}

## Residual Lock Attempt

{markdown_table(residual_lock, ["lock_id", "lock_clause", "effect", "status", "remaining_failure"])}

## First Coefficient Bound Interface

{markdown_table(bounds, ["bound_id", "symbol", "observable", "bound_value", "units", "prediction_status"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "requirement", "status", "claim_allowed"])}

## Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This moves the work forward in the right place. The theory can now say: if matter only sees q-basic observed geometry, then ordinary matter is not the linear-source obstruction. The live obstruction is narrower and nastier: parent grammar must forbid direct hidden/source-prefactor slots, and residual-lock must prove the vertical variables are the same physical residuals that enter the PPN/R10/R11 ledgers.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3888 NO LINEAR SOURCE -->"
    end = "<!-- END 3888 NO LINEAR SOURCE -->"
    block = f"""{start}

## 3888 - Quotient no-linear-source split

Matter chain rule:

`{CHAIN_RULE}`

Conditional result:

`{NO_SOURCE_RESULT}`

Status: ordinary observed matter/EM is conditionally source-neutral along true quotient-vertical directions. This helps the 3887 Euler-zero theorem because it attacks `J_A=0` rather than merely naming it. Still nonclaim: direct hidden/source-prefactor slots, worldtube support, boundary flux, memory, projector stress, residual-lock and universal R11 factorization remain live.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3888_QUOTIENT_NO_LINEAR_SOURCE_DERIVATION.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3888_SOURCE_CHANNEL_SPLIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3888_RESIDUAL_LOCK_ATTEMPT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3888_FIRST_COEFFICIENT_BOUND_INTERFACE.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3888_VALIDATION.csv`

Next gate: `3889`, parent object-language no-direct-source exclusion or prediction-side coefficient fill.

<!-- Generated by 3888 at {timestamp} -->
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
    derivation: list[dict[str, object]],
    channels: list[dict[str, object]],
    residual_lock: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    checks.append(("VAL3888_0_sources", "all cited source paths exist and needles are found", resolved == len(sources), f"{resolved}/{len(sources)} sources resolved"))
    checks.append(("VAL3888_1_chain_rule", "quotient chain rule is explicit", any("delta_y S_matter" in str(row["math"]) for row in derivation), "NLS3888_2"))
    checks.append(("VAL3888_2_jobs_zero", "observed matter source-neutrality result is explicit", any("J_A^obs" in str(row["math"]) and "= 0" in str(row["math"]) for row in derivation), "NLS3888_3"))
    required_channels = {"J_A^obs", "J_A^direct", "delta_w_A", "J_A^worldtube", "J_A^boundary", "J_A^memory", "J_A^projector", "J_A^R11"}
    found_channels = {str(row["source_piece"]) for row in channels}
    checks.append(("VAL3888_3_channel_split", "source channel split covers observed/direct/worldtube/boundary/memory/projector/R11", required_channels.issubset(found_channels), f"{len(found_channels)} channels"))
    checks.append(("VAL3888_4_residual_lock", "residual lock remains explicit and nonclaim", any(row["lock_id"] == "RL3888_5_lock_verdict" and "PARTIAL" in str(row["status"]) for row in residual_lock), "RL3888_5"))
    required_bounds = {"alpha3", "xi", "beta_minus_1", "gamma_minus_1", "Gdot_over_G", "fifth_force", "zeta_i;gamma;beta;alpha_i"}
    found_bounds = {str(row["observable"]) for row in bounds}
    checks.append(("VAL3888_5_bound_interface", "first bound-side coefficient interface covers key local arenas", required_bounds.issubset(found_bounds), f"{len(found_bounds)} bounds"))
    checks.append(("VAL3888_6_local_gr_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3888_7_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3888_7"))
    checks.append(("VAL3888_7_all_nonclaim", "all generated analytic rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [derivation, channels, residual_lock, bounds, gate, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3888_8_runner_split", "runner keeps only observed matter zeroed", any(row["runner_field"] == "J_A_split" and "only J_obs" in str(row["rule"]) for row in runner), "RUNU3888_0"))
    checks.append(("VAL3888_9_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "ordinary matter is not the linear-source obstruction" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3888_10_spine", "spine updated with 3888 block", SPINE_PATH.exists() and "BEGIN 3888 NO LINEAR SOURCE" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3888_11_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [path for path in FWB.rglob("*3888*") if path.is_file() and ("3888-Y5" in path.name or "P8_Y5_R2FR_3888" in path.name or "P8_Y5_BRR545_3888" in path.name)]
    checks.append(("VAL3888_12_formalization_untouched", "no generated 3888 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3888_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3888_14_next_target", "next target attacks object-language source exclusion or prediction fill", any("no-direct-source" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3889 no-direct-source"))
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
    derivation = derivation_rows(timestamp)
    channels = channel_rows(timestamp)
    residual_lock = residual_lock_rows(timestamp)
    bounds = bound_rows(timestamp)
    gate = gate_rows(timestamp)
    runner = runner_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["derivation"], derivation)
    write_csv(OUTPUTS["channels"], channels)
    write_csv(OUTPUTS["residual_lock"], residual_lock)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, derivation, channels, residual_lock, bounds, gate, runner, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, derivation, channels, residual_lock, bounds, gate, runner, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_QUOTIENT_NO_LINEAR_SOURCE_SPLIT")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
