from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4317"
CLAIM_ID = "L-158"
BRANCH = "MTS_R2FR_Y5_NONEM_INNER_CHARGE_DOMAIN_ZERO_OR_QMH_BOUND_VALUES_4317"
DECISION = "INNER_CHARGE_ZERO_BRANCH_SHARPENED_TRACE_DEFECT_BOUND_VALUES_STAGED_NONCLAIM"
MARKER = "PPC4161_NONEM_INNER_CHARGE_DOMAIN_ZERO_OR_QMH_BOUND_VALUES_4317"
PACKET_MARKER = "PPC4161_PACKET_NONEM_INNER_CHARGE_DOMAIN_ZERO_OR_QMH_BOUND_VALUES_4317"
NEXT_TARGET = "4318-Y5-R2FR-nonHilbert-support-drift-history-bound-prioritizer.md"

FORMAL_PATH = FORMAL / "333-PPC4161-nonEM-inner-charge-domain-zero-or-QmH-bound-values.md"
DOC_PATH = POST / "4317-Y5-R2FR-nonEM-inner-charge-domain-zero-or-QmH-bound-values.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4317_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4317_00_4316_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4316_NEXT_TARGET.csv",
        "Can N_inner be theorem-zeroed",
        "4316 handoff selecting the inner/domain charge branch.",
    ),
    "SRC4317_01_4303_component": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "N_inner <= C_inner |Q_m^H_nonHilbert|",
        "4303 component ledger naming inner charge as primary boundary blocker.",
    ),
    "SRC4317_02_4305_reduction": (
        FORMAL / "321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md",
        "N_pair <= N_inner + N_EM + N_rest",
        "4305 source-pair branch before visible/EM reduction.",
    ),
    "SRC4317_03_4306_weak_law": (
        FORMAL / "322-PPC4161-inner-domain-certificate-or-QmH-bound.md",
        "B_inner[phi] = int_partialD_in phi Z_m n.grad u dSigma + B_src[phi]",
        "4306 derived inner-boundary functional.",
    ),
    "SRC4317_04_4306_trace_bound": (
        FORMAL / "322-PPC4161-inner-domain-certificate-or-QmH-bound.md",
        "N_inner <= C_0 |Q_m^H| + C_perp ||g_perp|| + ||B_src||",
        "4306 monopole/multipole/source-boundary split.",
    ),
    "SRC4317_05_4307_domain_split": (
        FORMAL / "323-PPC4161-source-domain-owner-or-inner-flux-profile-fill.md",
        "partialD_in = empty set  =>  N_inner = 0",
        "4307 smooth-domain identity branch.",
    ),
    "SRC4317_06_4308_trace_defect": (
        FORMAL / "324-PPC4161-smooth-Hilbert-volume-domain-parent-signature-or-worldtube-flux-profile-row.md",
        "mu_tr := weak-lim",
        "4308 exterior readout trace-defect object.",
    ),
    "SRC4317_07_4309_conormal": (
        FORMAL / "325-PPC4161-source-domain-limit-defect-zero-or-first-numeric-flux-bound.md",
        "gamma_N",
        "4309 weak conormal trace bound route.",
    ),
    "SRC4317_08_4310_collar": (
        FORMAL / "326-PPC4161-collar-no-concentration-signature-or-trace-bound-inputs.md",
        "A_U <= C_col",
        "4310 collar amplitude bound replacing a free trace amplitude.",
    ),
    "SRC4317_09_4311_lambda": (
        FORMAL / "327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md",
        "lambda_* := Z_min lambda_1(D_loc) + M2_min - Eta_H",
        "4311 exact lambda-floor law.",
    ),
    "SRC4317_10_4316_budget": (
        FORMAL / "332-PPC4161-visible-Hilbert-source-silence-integration-or-nonEM-residual-budget.md",
        "N_pair <= N_inner + N_rest_nonEM",
        "4316 visible/EM source budget reduction.",
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
            "4317 sharpens the remaining inner/domain charge blocker after the 4316 visible/EM reduction. "
            "The exact theorem branch is now explicit: if the local m-lock problem is posed on the full smooth "
            "Hilbert source domain, no source hole is removed, no independent m-boundary/source charge exists, "
            "and any later worldtube surface is only an internal bookkeeping interface, then partialD_in is empty "
            "or its two oriented traces cancel, so B_inner=0 and N_inner=0. In that branch the 4316 source budget "
            "reduces further to N_pair <= N_rest_nonEM. If the calculation is instead an exterior/worldtube or "
            "point/excision branch, N_inner is not erased: it is bounded by the trace-defect and source-injection "
            "envelope N_inner <= ||mu_tr|| + ||B_src^A|| <= C_N[K_U C_col S_U_not_inner/lambda_* + R_U] + ||B_src^A||, "
            "or equivalently by C_0|Q_m^H|+C_perp||g_perp||+||B_src||. This is a source-coupling advance, not a "
            "local GR/Newton claim."
        ),
        (
            "4317 source register, zero theorem audit, branch selector, QmH/trace bound input schema, reduced "
            "source formulas, runner, firewall, status, next-target and validation CSV."
        ),
        "private_inner_charge_zero_branch_or_trace_defect_bound_values_nonclaim",
        (
            "Parent-sign the smooth source-domain/no-independent-m-charge branch, or source C_N, K_U, C_col, "
            "lambda_*, S_U_not_inner, R_U, B_src^A, C_0, Q_m^H, C_perp and g_perp as real arena inputs."
        ),
        (
            "Using smooth-domain N_inner=0 inside an exterior/excision solve, reducing a worldtube trace to a "
            "scalar Q_m^H without multipole/source-injection rows, claiming lambda_* positivity from its formula "
            "shape, or promoting N_inner silence to local GR/Newton while N_rest_nonEM/source-equality/projection "
            "gates remain open."
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


def zero_theorem_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "ZT4317_0_full_domain",
            "m-lock operator domain contains compact Hilbert source volume",
            "D_m = W_H union A_ext and W_H is not removed before variation",
            "partialD_in = empty set; B_inner=0; N_inner=0",
            "EXACT_DOMAIN_IDENTITY_IF_PARENT_SIGNED",
        ),
        (
            "ZT4317_1_no_direct_m_charge",
            "matter/source action carries no independent m-boundary charge",
            "source factors through q/Hilbert variables already owned by S_vis and source kernel",
            "B_src^A=0 and Q_m^H=0",
            "EXACT_ZERO_CLAUSE_IF_PARENT_SIGNED",
        ),
        (
            "ZT4317_2_interface_cancellation",
            "worldtube surface is only a split of a full-domain weak form",
            "oriented inner and outer interface terms are equal and opposite",
            "interface flux is bookkeeping, not a physical inner source",
            "DERIVED_BOOKKEEPING_ZERO",
        ),
        (
            "ZT4317_3_smooth_to_exterior_limit",
            "exterior readout is taken as a limit of smooth full-domain sources",
            "mu_tr=0 and B_src^A=0",
            "N_inner=0 survives exterior readout",
            "CONDITIONAL_LIMIT_ZERO_NOT_PARENT_SIGNED",
        ),
        (
            "ZT4317_4_failure_branch",
            "source is solved as exterior/worldtube or point/excision problem",
            "partialD_in nonempty or trace-defect/source injection survives",
            "N_inner must be bounded, not erased",
            "BOUND_BRANCH_REQUIRED",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for theorem_id, clause, condition, consequence, status in specs:
        row = base_row()
        row.update(
            {
                "theorem_id": theorem_id,
                "clause": clause,
                "condition": condition,
                "consequence": consequence,
                "status": status,
            }
        )
        rows.append(row)
    return rows


def branch_selector_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "BR4317_0_standard_smooth",
            "visible+EM zero branch from 4316 plus full smooth Hilbert source domain",
            "N_visible=0; N_EM=0; N_inner=0",
            "N_pair <= N_rest_nonEM",
            "BEST_LOCAL_SOURCE_BRANCH_CONDITIONAL",
            "use for derivation work only after parent/domain signature exists",
        ),
        (
            "BR4317_1_full_domain_internal_split",
            "worldtube surface introduced only after solving full-domain weak problem",
            "opposite oriented traces cancel on the artificial interface",
            "no physical Q_m^H row is charged to N_inner",
            "BOOKKEEPING_ZERO_ROUTE",
            "must not be mixed with exterior-only boundary data",
        ),
        (
            "BR4317_2_exterior_trace_defect",
            "exterior/worldtube branch with surviving trace-defect",
            "mu_tr or B_src^A nonzero/unsigned",
            "N_pair <= N_rest_nonEM + ||mu_tr|| + ||B_src^A||",
            "TRACE_DEFECT_BOUND_ROUTE",
            "requires trace/collar/lambda inputs before local tests",
        ),
        (
            "BR4317_3_QmH_profile",
            "monopole/multipole profile branch",
            "g_in decomposed into Q_m^H and g_perp with B_src retained",
            "N_pair <= N_rest_nonEM + C_0|Q_m^H| + C_perp||g_perp|| + ||B_src||",
            "PROFILE_BOUND_ROUTE",
            "scalar Q_m^H alone is insufficient unless g_perp and B_src are zero/bounded",
        ),
        (
            "BR4317_4_invalid_mix",
            "borrowing smooth zero inside exterior/excision calculation",
            "partialD_in nonempty while N_inner is set to zero by smooth-domain language",
            "reject branch",
            "INVALID_BRANCH_MIX",
            "prevents smuggled local-GR closure",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for selector_id, branch_condition, inputs, output_formula, status, guard in specs:
        row = base_row()
        row.update(
            {
                "selector_id": selector_id,
                "branch_condition": branch_condition,
                "inputs_or_certificates": inputs,
                "output_formula": output_formula,
                "status": status,
                "guard": guard,
            }
        )
        rows.append(row)
    return rows


def bound_input_rows() -> List[Dict[str, str]]:
    specs = [
        ("BI4317_0_mu_tr", "mu_tr", "weak exterior trace-defect measure", "H^{-1/2}(partialW_H)", "zero or finite norm", "MISSING_ZERO_THEOREM_OR_VALUE", "False"),
        ("BI4317_1_BsrcA", "B_src^A", "exterior source-boundary injection", "H^{-1/2}(partialW_H)", "zero or finite norm", "MISSING_ZERO_THEOREM_OR_VALUE", "False"),
        ("BI4317_2_CN", "C_N", "weak conormal trace extension constant", "dimensionless/operator norm", "positive finite constant", "MISSING_ARENA_PROJECTION", "False"),
        ("BI4317_3_KU", "K_U", "collar coefficient ceiling Zbar+Mbar+EtaH_U or equivalent", "operator/collar norm", "positive finite ceiling", "MISSING_COMPONENT_VALUES", "False"),
        ("BI4317_4_Ccol", "C_col", "collar coercive amplitude constant", "dimensionless/operator norm", "positive finite constant", "MISSING_ARENA_PROJECTION", "False"),
        ("BI4317_5_lambda_star", "lambda_*", "local positivity floor", "same as m-lock quadratic form floor", "lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H > 0", "FORMULA_READY_VALUE_UNSOURCED", "False"),
        ("BI4317_6_SU_not_inner", "S_U_not_inner", "collar numerator excluding N_inner itself", "same dual/source norm as collar forcing", "sum of non-inner residual rows", "FORMULA_READY_COMPONENT_VALUES_MISSING", "False"),
        ("BI4317_7_RU", "R_U", "local m-lock residual on collar", "H^{-1}(U_W)", "zero theorem or finite norm", "MISSING_ZERO_THEOREM_OR_VALUE", "False"),
        ("BI4317_8_QmH", "Q_m^H", "monopole part of exterior normal memory flux", "flux integral over partialW_H", "zero theorem or finite value", "MISSING_ZERO_THEOREM_OR_VALUE", "False"),
        ("BI4317_9_gperp", "g_perp", "multipole/tidal part of exterior normal memory flux", "H^{-1/2}(partialW_H)", "zero theorem or finite norm", "MISSING_ZERO_THEOREM_OR_VALUE", "False"),
        ("BI4317_10_C0", "C_0", "monopole trace conversion constant", "operator/domain constant", "positive finite constant", "MISSING_ARENA_PROJECTION", "False"),
        ("BI4317_11_Cperp", "C_perp", "multipole trace conversion constant", "operator/domain constant", "positive finite constant", "MISSING_ARENA_PROJECTION", "False"),
        ("BI4317_12_Bsrc", "B_src", "profile-branch source-boundary injection", "boundary dual norm", "zero theorem or finite norm", "MISSING_ZERO_THEOREM_OR_VALUE", "False"),
    ]
    rows: List[Dict[str, str]] = []
    for input_id, symbol, meaning, units, required_value, status, value_valid in specs:
        row = base_row()
        row.update(
            {
                "input_id": input_id,
                "symbol": symbol,
                "meaning": meaning,
                "units_or_norm": units,
                "required_value": required_value,
                "status": status,
                "value_valid_for_claim": value_valid,
            }
        )
        rows.append(row)
    return rows


def formula_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "F4317_0_inner_functional",
            "inner boundary functional",
            "B_inner[phi] = int_partialD_in phi Z_m n.grad u dSigma + B_src[phi]",
            "from 4306 weak form",
            "DERIVED",
        ),
        (
            "F4317_1_smooth_zero",
            "smooth full-domain zero",
            "partialD_in=empty and B_src=0 => N_inner=0",
            "domain identity, not a fit",
            "EXACT_IF_BRANCH_SIGNED",
        ),
        (
            "F4317_2_interface_zero",
            "internal interface cancellation",
            "int_partialW phi Z_m n_A.grad u + int_partialW phi Z_m n_W.grad u = 0",
            "valid only for a split of the full-domain weak form",
            "DERIVED_BOOKKEEPING_IDENTITY",
        ),
        (
            "F4317_3_trace_defect_bound",
            "exterior trace-defect bound",
            "N_inner <= ||mu_tr|| + ||B_src^A||",
            "fallback when exterior readout has a surviving defect",
            "BOUND_FORMULA_READY_VALUES_MISSING",
        ),
        (
            "F4317_4_collar_bound",
            "lambda-floor trace bound",
            "N_inner <= C_N[K_U C_col S_U_not_inner/lambda_* + R_U] + ||B_src^A||",
            "4310/4311 bound with self-dependence removed from numerator",
            "GUARDED_BOUND_READY_VALUES_MISSING",
        ),
        (
            "F4317_5_profile_bound",
            "QmH profile envelope",
            "N_inner <= C_0|Q_m^H| + C_perp||g_perp|| + ||B_src||",
            "safe scalar-plus-multipole fallback",
            "BOUND_FORMULA_READY_VALUES_MISSING",
        ),
        (
            "F4317_6_reduced_source_pair",
            "4316 plus inner zero",
            "if N_visible=N_EM=N_inner=0 then N_pair <= N_rest_nonEM",
            "this is the main 4317 gain",
            "CONDITIONAL_REDUCTION",
        ),
        (
            "F4317_7_all_source_zero",
            "exact local source silence",
            "if N_rest_nonEM=0 also, then N_pair=0",
            "still needs non-Hilbert/drift/history/boundary/nonlinear rows",
            "NOT_LIVE",
        ),
        (
            "F4317_8_m_lock_handoff",
            "m-lock amplitude",
            "Delta_m <= (N_rest_nonEM + N_N)/lambda_m on full zero branch",
            "requires lambda_m positive and remaining components sourced",
            "HANDOFF_READY_NOT_SCORE_READY",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for formula_id, name, formula, derivation_basis, status in specs:
        row = base_row()
        row.update(
            {
                "formula_id": formula_id,
                "name": name,
                "formula": formula,
                "derivation_basis": derivation_basis,
                "status": status,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RUN4317_0_current_safe",
            "current corpus, no new parent domain signature",
            "USE_TRACE_OR_PROFILE_BOUND",
            "N_pair <= N_rest_nonEM + N_inner_bound",
            "local GR/Newton blocked",
        ),
        (
            "RUN4317_1_best_if_signed",
            "visible+EM zero and smooth full-domain N_inner=0 signed",
            "ALLOW_NPAIR_TO_NONEM",
            "N_pair <= N_rest_nonEM",
            "next attack N_rest_nonEM and lambda/source equality",
        ),
        (
            "RUN4317_2_all_nonEM_zero",
            "N_rest_nonEM also zero or finitely below local precision budget",
            "ALLOW_SOURCE_PAIR_ZERO_OR_SMALL",
            "N_pair=0 or bounded below arena tolerance",
            "still needs lambda_m, R_eq, I_commutator, projection",
        ),
        (
            "RUN4317_3_invalid_excision_zero",
            "exterior/excision branch but N_inner set to zero without trace/no-flux theorem",
            "REJECT",
            "no score",
            "branch-mixing firewall",
        ),
        (
            "RUN4317_4_numeric_fallback",
            "Q_m^H/g_perp/B_src/C constants sourced",
            "ALLOW_NONCLAIM_LOCAL_BOUND",
            "N_inner finite bound feeds R10/PPN/clocks/orbital residual tests",
            "claim only after all rows valid and within arena budgets",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, scenario, action, output, reason in specs:
        row = base_row()
        row.update(
            {
                "runner_id": runner_id,
                "scenario": scenario,
                "action": action,
                "output": output,
                "reason": reason,
            }
        )
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    specs = [
        ("FW4317_0", "Do not use smooth-domain N_inner=0 inside an exterior/worldtube/excision solve.", "ACTIVE"),
        ("FW4317_1", "Do not collapse the trace profile to scalar Q_m^H unless g_perp and B_src are independently zero or bounded.", "ACTIVE"),
        ("FW4317_2", "Do not let N_inner appear on both sides of the collar numerator; use S_U_not_inner.", "ACTIVE"),
        ("FW4317_3", "Do not treat lambda_* as positive until Z_min, lambda_1, M2_min and Eta_H are parent-owned or numerically sourced.", "ACTIVE"),
        ("FW4317_4", "Do not claim local GR/Newton from N_inner silence alone; N_rest_nonEM, lambda_m, source equality, commutator and projection gates remain live.", "ACTIVE"),
    ]
    rows: List[Dict[str, str]] = []
    for firewall_id, rule, status in specs:
        row = base_row()
        row.update({"firewall_id": firewall_id, "rule": rule, "status": status})
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DEC4317_0_gain",
            "NINNER_ZERO_CONDITIONS_EXACT",
            "The smooth full-domain route is now an exact domain/source theorem rather than a vague hope.",
            "try to parent-sign full-domain source ownership before choosing exterior fallback",
        ),
        (
            "DEC4317_1_reduction",
            "SOURCE_PAIR_CAN_REDUCE_TO_NREST_NONEM",
            "4316 plus N_inner=0 gives N_pair <= N_rest_nonEM.",
            "attack non-Hilbert support, drift/selector, history/transition, boundary/domain and nonlinear rows next",
        ),
        (
            "DEC4317_2_fallback",
            "TRACE_PROFILE_BOUND_RETAINED",
            "If exterior/worldtube language survives, Q_m^H alone is not enough; multipoles and source injection remain.",
            "source or theorem-zero C_0, Q_m^H, C_perp, g_perp and B_src",
        ),
        (
            "DEC4317_3_claim",
            "NO_LOCAL_CLAIM",
            "This closes or bounds one source component only; it does not derive the full GR/Newton limit.",
            "keep all claim flags false",
        ),
        (
            "DEC4317_4_next",
            "NONEM_REST_NEXT",
            "After visible/EM and possible N_inner zero, the dominant budget is N_rest_nonEM.",
            NEXT_TARGET,
        ),
    ]
    rows: List[Dict[str, str]] = []
    for decision_id, result, reason, next_action in specs:
        row = base_row()
        row.update(
            {
                "decision_id": decision_id,
                "result": result,
                "reason": reason,
                "next_action": next_action,
            }
        )
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4317_0_Ninner_smooth", "N_inner smooth branch", "EXACT_ZERO_IF_PARENT_SIGNED", "full source domain/no independent m-charge"),
        ("STAT4317_1_Ninner_exterior", "N_inner exterior branch", "BOUND_REQUIRED", "trace-defect/profile rows required"),
        ("STAT4317_2_QmH", "Q_m^H scalar", "INSUFFICIENT_ALONE", "must pair with g_perp and B_src rows"),
        ("STAT4317_3_Npair", "N_pair", "CAN_REDUCE_TO_NREST_NONEM", "only on visible+EM+Ninner zero branch"),
        ("STAT4317_4_lambda", "lambda_*", "STILL_GATED", "positivity formula derived but values not sourced"),
        ("STAT4317_5_local", "local GR/Newton", "BLOCKED", "N_rest_nonEM/source equality/projection gates remain"),
    ]
    rows: List[Dict[str, str]] = []
    for status_id, object_name, status, note in specs:
        row = base_row()
        row.update({"status_id": status_id, "object": object_name, "status": status, "note": note})
        rows.append(row)
    return rows


def next_rows() -> List[Dict[str, str]]:
    row = base_row()
    row.update(
        {
            "next_target_id": "NT4317_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the remaining non-EM source budget N_rest_nonEM be split into zeroable theorem branches and finite bound rows without double-counting N_inner?",
            "preferred_route": "derive/source-kill non-Hilbert support, drift/selector, history/transition, boundary/domain and nonlinear rows componentwise",
            "fallback_route": "stage nonclaim numeric/budget schemas for each residual and route them into lambda-floor/local precision tests",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 333 PPC4161 nonEM inner charge domain zero or QmH bound values

Marker: `{MARKER}`

## Decision

`{DECISION}`

4317 takes the 4316 source budget

```text
N_pair <= N_inner + N_rest_nonEM
```

and sharpens the first remaining blocker. The exact zero branch is not a plateau axiom. It is a domain/source theorem:

```text
D_m = W_H union A_ext, W_H not removed before variation,
partialD_in = empty set, B_src=0
=> B_inner=0, N_inner=0.
```

If a worldtube surface is introduced only as a split of the full-domain weak form, the two oriented interface traces cancel. If the solve is exterior-only or point/excision based, the inner charge is physical boundary data and must be bounded:

```text
N_inner <= ||mu_tr|| + ||B_src^A||
N_inner <= C_N[K_U C_col S_U_not_inner/lambda_* + R_U] + ||B_src^A||
N_inner <= C_0|Q_m^H| + C_perp||g_perp|| + ||B_src||.
```

The self-dependence guard is explicit: `S_U_not_inner` excludes `N_inner` itself.

## Zero Theorem Audit
{md_table(tables["zero"], ["theorem_id", "clause", "condition", "consequence", "status"])}

## Branch Selector
{md_table(tables["branches"], ["selector_id", "branch_condition", "inputs_or_certificates", "output_formula", "status", "guard"])}

## Bound Input Schema
{md_table(tables["bounds"], ["input_id", "symbol", "meaning", "units_or_norm", "required_value", "status", "value_valid_for_claim"])}

## Reduced Formulas
{md_table(tables["formulas"], ["formula_id", "name", "formula", "derivation_basis", "status"])}

## Runner
{md_table(tables["runner"], ["runner_id", "scenario", "action", "output", "reason"])}

## Firewall
{md_table(tables["firewall"], ["firewall_id", "rule", "status"])}

## Result

4317 gives a genuine branch advance: on the signed smooth full-domain source branch, 4316 reduces further to `N_pair <= N_rest_nonEM`. On the exterior/worldtube branch, the price of not proving that theorem is now explicit and scoreable. No local GR/Newton claim fires.

Next target: `{NEXT_TARGET}`.
"""
    post = f"""# 4317 - nonEM inner charge domain zero or QmH bound values

## Verdict

- Real gain: `N_inner=0` now has exact domain/source conditions, not just a missing-label wish.
- Conditional reduction: if visible+EM gates close and the smooth full-domain source branch is signed, `N_pair <= N_rest_nonEM`.
- Exterior branch remains honest: `N_inner <= ||mu_tr||+||B_src^A||` or `C_0|Q_m^H|+C_perp||g_perp||+||B_src||`.
- No local GR/Newton claim fires; the next target is the remaining `N_rest_nonEM` budget.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Zero Theorem Audit
{md_table(tables["zero"], ["theorem_id", "clause", "condition", "consequence", "status"])}

## Branch Selector
{md_table(tables["branches"], ["selector_id", "branch_condition", "output_formula", "status", "guard"])}

## Bound Input Schema
{md_table(tables["bounds"], ["input_id", "symbol", "units_or_norm", "required_value", "status"])}

## Reduced Formulas
{md_table(tables["formulas"], ["formula_id", "name", "formula", "status"])}

## Runner
{md_table(tables["runner"], ["runner_id", "scenario", "action", "output", "reason"])}

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
        row.update(
            {
                "check_id": check_id,
                "description": description,
                "passed": str(passed),
                "evidence": evidence,
            }
        )
        rows.append(row)

    source_table = tables["sources"]
    add("VAL4317_sources_exist", "all cited source paths exist", all(r["exists"] == "True" for r in source_table), "source_register")
    add("VAL4317_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in source_table), "source_register")
    add("VAL4317_zero_branch", "smooth zero theorem row exists", any(r["theorem_id"] == "ZT4317_0_full_domain" and "N_inner=0" in r["consequence"] for r in tables["zero"]), "zero_theorem")
    add("VAL4317_failure_branch", "exterior failure branch retains bound", any(r["theorem_id"] == "ZT4317_4_failure_branch" and r["status"] == "BOUND_BRANCH_REQUIRED" for r in tables["zero"]), "zero_theorem")
    add("VAL4317_branch_reduction", "branch selector reduces N_pair to N_rest_nonEM only conditionally", any(r["selector_id"] == "BR4317_0_standard_smooth" and "N_pair <= N_rest_nonEM" in r["output_formula"] for r in tables["branches"]), "branch_selector")
    add("VAL4317_invalid_mix_rejected", "invalid branch mix is rejected", any(r["selector_id"] == "BR4317_4_invalid_mix" and r["status"] == "INVALID_BRANCH_MIX" for r in tables["branches"]), "branch_selector")
    add("VAL4317_bound_inputs_nonclaim", "all bound inputs are nonclaim", all(r["value_valid_for_claim"] == "False" for r in tables["bounds"]), "bound_schema")
    add("VAL4317_QmH_not_alone", "QmH row is marked insufficient without profile", any(r["symbol"] == "Q_m^H" and r["status"] == "MISSING_ZERO_THEOREM_OR_VALUE" for r in tables["bounds"]), "bound_schema")
    add("VAL4317_self_guard", "S_U_not_inner row prevents circular bound", any(r["symbol"] == "S_U_not_inner" for r in tables["bounds"]), "bound_schema")
    add("VAL4317_collar_formula", "collar bound formula includes S_U_not_inner/lambda_*", any("S_U_not_inner/lambda_*" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4317_profile_formula", "profile formula includes QmH, gperp, and Bsrc", any("Q_m^H" in r["formula"] and "g_perp" in r["formula"] and "B_src" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4317_runner_rejects_invalid", "runner rejects excision zero", any(r["runner_id"] == "RUN4317_3_invalid_excision_zero" and r["action"] == "REJECT" for r in tables["runner"]), "runner")
    add("VAL4317_claim_false", "all generated rows keep claim false", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for table in tables.values() for row in table), "all_tables")
    add("VAL4317_next_target", "next target is 4318", any("4318" in r["next_target"] for r in tables["next"]), "next")
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4317_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4317_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "generated_docs")
    add("VAL4317_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims_register")
    add("VAL4317_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "unification_spine")
    add("VAL4317_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "private_packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4317_SOURCE_REGISTER.csv",
        "zero": SOURCE_DIR / "P8_Y5_R2FR_4317_ZERO_THEOREM_AUDIT.csv",
        "branches": SOURCE_DIR / "P8_Y5_R2FR_4317_BRANCH_SELECTOR.csv",
        "bounds": SOURCE_DIR / "P8_Y5_R2FR_4317_QMH_TRACE_BOUND_INPUT_SCHEMA.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4317_REDUCED_SOURCE_FORMULAS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4317_LOCAL_ROUTE_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4317_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4317_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4317_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4317_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "zero": zero_theorem_rows(),
        "branches": branch_selector_rows(),
        "bounds": bound_input_rows(),
        "formulas": formula_rows(),
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
## PPC4161 4317 nonEM inner charge domain zero or QmH bound values

Marker: `{MARKER}`

4317 sharpens the first post-4316 non-EM source blocker. On the signed smooth full-domain Hilbert source branch, `partialD_in=empty`, no independent `m`-boundary charge exists, and artificial worldtube traces cancel as internal interfaces; hence `N_inner=0` and the source-pair budget reduces to `N_pair <= N_rest_nonEM`. On exterior/worldtube or point/excision branches, `N_inner` is retained as a trace/profile cost: `N_inner <= ||mu_tr||+||B_src^A|| <= C_N[K_U C_col S_U_not_inner/lambda_*+R_U]+||B_src^A||`, equivalently `C_0|Q_m^H|+C_perp||g_perp||+||B_src||`. No local GR/Newton claim fires.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4317 packet nonEM inner charge zero or bound

Marker: `{PACKET_MARKER}`

Packet update: the inner charge blocker is now a branch theorem or a trace-defect budget. If the local source is kept inside the smooth Hilbert volume domain, `N_inner=0`; if an exterior worldtube/excision solve is used, the trace profile must be paid through `mu_tr`, `Q_m^H`, `g_perp` and `B_src` rows.
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
