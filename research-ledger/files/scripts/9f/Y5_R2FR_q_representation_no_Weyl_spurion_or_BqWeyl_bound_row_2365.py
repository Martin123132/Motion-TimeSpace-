from __future__ import annotations

import csv
import subprocess
from pathlib import Path
from typing import Iterable


BRANCH_ID = "MTS_R2FR_Q_REPRESENTATION_NO_WEYL_SPURION_OR_BQWEYL_BOUND_ROW_2365"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2365-Y5-R2FR-q-representation-no-Weyl-spurion-or-BqWeyl-bound-row.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_value_present": "false",
        "source_backed": "false",
        "operator_domain_ready": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    sources = [
        ("SRC2365_2364_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2364_NEXT_TARGET.csv", "NEXT2364_0_selected", "2364 selected no-spurion/BqWeyl route"),
        ("SRC2365_2364_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2364_VALIDATION.csv", "VAL2364_OVERALL", "2364 validation"),
        ("SRC2365_2304_index", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2304_OBJECT_LANGUAGE_INDEX_LEMMA.csv", "OLI2304_6_verdict", "linear BqWeyl index theorem conditional verdict"),
        ("SRC2365_2304_input", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2304_BQWEYL_FIRST_SOURCE_INPUT.csv", "BQI2304_4_acceptance_rule", "first BqWeyl source input acceptance rule"),
        ("SRC2365_2305_typed", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2305_TYPED_NO_SPURION_SIGNATURE_ATTEMPT.csv", "TGS2305_7_verdict", "typed no-spurion signature attempt verdict"),
        ("SRC2365_2305_demote", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2305_LINEAR_BQWEYL_DEMOTION_LEDGER.csv", "DEM2305_0_linear_route_status", "linear BqWeyl route demoted to closure-only"),
        ("SRC2365_2305_quadratic", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2305_QUADRATIC_WEYL_RESIDUAL_ROW.csv", "DQW2305_0_DqWeyl2", "quadratic Weyl residual survives linear theorem"),
        ("SRC2365_2306_zero", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2306_DQWEYL2_ZERO_THEOREM_ATTEMPT.csv", "ZERO2306_4_verdict", "DqWeyl2 zero theorem not derived"),
        ("SRC2365_2306_bound", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2306_DQWEYL2_FIRST_LOCAL_BOUND_ROW.csv", "BOUND2306_3_projection_kernel", "analytic quadratic Weyl exterior kernel"),
        ("SRC2365_2307_hunt", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2307_PARENT_COEFFICIENT_SOURCE_HUNT.csv", "HUNT2307_3_verdict", "DqWeyl2 coefficient/operator/projection source hunt blocked"),
        ("SRC2365_2307_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2307_NEXT_TARGET.csv", "NEXT2307_0", "next target after DqWeyl2 smoke contract"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in sources:
        path = POST_ROOT / source_path
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": source_path,
                "needle": needle,
                "role": role,
                "path_exists": str(path.exists()).lower(),
                "needle_found": str(contains(path, needle)).lower(),
                "valid_for_claim": "false",
            }
        )
    return rows


def linear_bqweyl_zero_audit() -> list[dict[str, object]]:
    rows = [
        (
            "LBZ2365_0_metric_trace",
            "metric-only one-Weyl contraction",
            "g-contractions of one C_abcd trace a Weyl index pair and vanish",
            "EXACT_INDEX_LEMMA",
            "safe only inside a metric/epsilon-only grammar",
        ),
        (
            "LBZ2365_1_epsilon_trace",
            "epsilon-only one-Weyl contraction",
            "epsilon^{abcd} C_abcd vanishes by Weyl symmetries and Bianchi identity",
            "EXACT_INDEX_LEMMA",
            "parity-odd nonzero terms start at C * C, not one Weyl",
        ),
        (
            "LBZ2365_2_spurion_countermodel",
            "q P^{abcd} C_abcd",
            "a hidden four-index projector/spurion/readout kernel makes a linear scalar legal",
            "COUNTERMODEL_SURVIVES",
            "this is the exact clause the parent action must forbid",
        ),
        (
            "LBZ2365_3_parent_signature",
            "typed no-Weyl-spurion grammar",
            "q must be scalar/quotient/pure density and the parent grammar must contain no Weyl-type P^{abcd}",
            "NOT_PARENT_SIGNED",
            "2305 says this is a schema/contract, not a primitive derivation",
        ),
        (
            "LBZ2365_4_linear_verdict",
            "linear B_qWeyl status",
            "linear B_qWeyl can be killed by a real parent no-spurion theorem, but cannot be claimed now",
            "DEMOTE_TO_CLOSURE_ONLY",
            "strong mathematical lever, weak parent-signature evidence",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "audit_target": target,
            "statement": statement,
            "status": status,
            "effect": effect,
        }
        for row_id, target, statement, status, effect in rows
    ]


def no_spurion_contract() -> list[dict[str, object]]:
    rows = [
        ("NSC2365_0_parent_sort", "parent q sort", "q is declared before variation as scalar, quotient coordinate, or pure density", "MISSING_PARENT_SORT_DERIVATION"),
        ("NSC2365_1_transform_law", "q transformation law", "q carries no Weyl/Riemann four-index bundle data under diffeo/local-frame/internal maps", "MISSING_TRANSFORM_LAW"),
        ("NSC2365_2_no_projector", "no Weyl projector/spurion", "no parent P^{abcd}, readout kernel, or hidden tensor contracts q with Weyl", "MISSING_NO_PROJECTOR_THEOREM"),
        ("NSC2365_3_no_extension", "object-language exhaustion", "no manually appended local scalar algebra outside Image(ParentGenerate)", "MISSING_EXHAUSTION_THEOREM"),
        ("NSC2365_4_no_readout_reentry", "variation-before-readout closure", "source/readout/projector maps cannot insert P^{abcd} after Euler variation", "MISSING_READOUT_CLOSURE"),
        ("NSC2365_5_radiative_stability", "radiative/loop/reduction closure", "integrating out sectors cannot regenerate q-Weyl coefficient maps", "MISSING_RADIATIVE_CLOSURE"),
        ("NSC2365_6_verdict", "no-spurion contract", "all clauses must close in one parent branch to activate B_qWeyl(linear)=0", "CONTRACT_READY_THEOREM_NOT_SIGNED"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "clause": clause,
            "required_statement": statement,
            "status": status,
        }
        for row_id, clause, statement, status in rows
    ]


def bqweyl_bound_row_status() -> list[dict[str, object]]:
    rows = [
        ("BQB2365_0_zero_switch", "Z_BqWeyl_linear", "true only if the no-spurion contract is parent-signed", "ZERO_SWITCH_FALSE", "dimensionless_bool"),
        ("BQB2365_1_parent_coefficient", "B_qWeyl", "source-backed coefficient with sign, uncertainty, and q normalization", "MISSING_PARENT_COEFFICIENT", "parent_normalized"),
        ("BQB2365_2_q_operator", "L_q_or_G_q", "q Green operator, mass/range, boundary class, and sign convention", "MISSING_Q_OPERATOR", "operator"),
        ("BQB2365_3_weyl_profile", "C_Weyl_local", "exterior Weyl/tidal profile on the selected domain", "MISSING_DOMAIN_PROFILE", "length^-2"),
        ("BQB2365_4_projection", "tau_BqWeyl_arena", "R10/PPN/clock/orbital projection from q_Weyl to observables", "MISSING_ARENA_PROJECTION", "arena_specific"),
        ("BQB2365_5_acceptance", "linear_BqWeyl_claim", "claim only if zero switch or all numeric rows are sourced and below arena limits", "CLAIM_BLOCKED", "boolean"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "symbol": symbol,
            "required_input": required,
            "status": status,
            "units": units,
        }
        for row_id, symbol, required, status, units in rows
    ]


def quadratic_weyl_reentry() -> list[dict[str, object]]:
    rows = [
        (
            "QWR2365_0_DqWeyl2",
            "D_qWeyl2",
            "q C_abcd C^abcd",
            "survives the linear one-Weyl index theorem",
            "LIVE_NONCLAIM_RESIDUAL",
        ),
        (
            "QWR2365_1_DqWeylDual",
            "D_qWeylDual",
            "q C_abcd *C^abcd",
            "parity/orientation branch also survives unless object-language forbids it",
            "LIVE_NONCLAIM_RESIDUAL",
        ),
        (
            "QWR2365_2_no_tower",
            "Z_DqWeyl2",
            "absence of bare/induced higher-curvature tower",
            "requires no bare Weyl2, no integrated-out regeneration, no hidden coefficient morphism",
            "ZERO_THEOREM_NOT_DERIVED",
        ),
        (
            "QWR2365_3_kernel",
            "K_C2_ext",
            "64*pi*(GM/c^2)^2/R_body^3",
            "analytic exterior Schwarzschild/Weyl2 source kernel is available as nonclaim plumbing",
            "ANALYTIC_KERNEL_READY_NONCLAIM",
        ),
        (
            "QWR2365_4_source_hunt",
            "D_qWeyl2, L_q, P_obs",
            "parent coefficient, q operator, and observable map",
            "2307 source hunt did not find these in the current corpus",
            "BLOCKED_INPUTS_MISSING",
        ),
        (
            "QWR2365_5_verdict",
            "quadratic Weyl branch",
            "linear route demoted; quadratic/tower branch is the next real obstruction",
            "not score-ready",
            "SELECT_NEXT_COEFFICIENT_OR_Q_OPERATOR_TARGET",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "symbol": symbol,
            "operator_or_formula": formula,
            "reason_retained": reason,
            "status": status,
        }
        for row_id, symbol, formula, reason, status in rows
    ]


def decision_ledger() -> list[dict[str, object]]:
    rows = [
        ("DEC2365_0_linear_index", "use the one-Weyl index theorem", 1, "KEEP_AS_CONDITIONAL_LEVER", "it is exact under the typed no-spurion grammar"),
        ("DEC2365_1_linear_claim", "claim B_qWeyl(linear)=0 now", 5, "REFUSE_AND_DEMOTE", "parent grammar/no-spurion/readout closure is not signed"),
        ("DEC2365_2_linear_bound", "fill numeric linear B_qWeyl row", 2, "BLOCKED_INPUTS_MISSING", "parent coefficient, q operator, Weyl profile, and projections are missing"),
        ("DEC2365_3_quadratic", "carry D_qWeyl2 branch", 1, "SELECT_NEXT_OBSTRUCTION", "quadratic Weyl is not killed by the linear theorem"),
        ("DEC2365_4_parent_action", "derive parent object language/no-tower action", 1, "BEST_THEORY_ROUTE", "this is the least hand-wavy way to reach local GR/Newton"),
        ("DEC2365_5_empirical", "run local tests", 5, "DEFER", "no source-backed prediction row exists yet"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "route": route,
            "rank": rank,
            "decision": decision,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, route, rank, decision, reason in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2365_0_linear_BqWeyl_zero", "linear B_qWeyl theorem-zero activated", "BLOCKED", "conditional theorem premises are not parent-signed"),
        ("CG2365_1_linear_BqWeyl_bound", "linear B_qWeyl finite row score-ready", "BLOCKED", "coefficient/operator/projection rows missing"),
        ("CG2365_2_no_spurion", "no-Weyl-spurion parent object language derived", "BLOCKED", "typed grammar is a contract, not a primitive theorem"),
        ("CG2365_3_DqWeyl2_zero", "quadratic Weyl/tower zero theorem derived", "BLOCKED", "no-tower/radiative/readout closure unsigned"),
        ("CG2365_4_DqWeyl2_bound", "quadratic Weyl finite bound score-ready", "BLOCKED", "D_qWeyl2, L_q/G_q, and P_obs missing"),
        ("CG2365_5_local_GR_Newton", "local GR/Newton reduction derived", "BLOCKED", "linear and quadratic q-curvature residuals not closed"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "gate_pass": "false",
            "passes_public_claim": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, claim, status, reason in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2365_0_BqWeyl_zero", "promote linear B_qWeyl=0", "needs parent-signed q sort, no projector, exhaustion, readout closure", "REFUSED"),
        ("REF2365_1_BqWeyl_bound", "run linear BqWeyl local comparator", "needs B_qWeyl, L_q/G_q, C_Weyl profile, tau projection", "REFUSED"),
        ("REF2365_2_ignore_DqWeyl2", "ignore quadratic Weyl after killing linear branch", "q C^2 is not killed by one-Weyl index algebra", "REFUSED"),
        ("REF2365_3_local_GR", "claim local GR/Newton branch passes", "curvature residual tower and source/body/tail gates remain open", "REFUSED"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "attempted_claim": claim,
            "missing_evidence": missing,
            "refusal_result": result,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, claim, missing, result in rows
    ]


def next_target() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2365_0_selected",
            "next_file": "2366-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md",
            "next_script": "scripts/Y5_R2FR_DqWeyl2_parent_coefficient_or_q_operator_normalization_source_2366.py",
            "selected_reason": "linear B_qWeyl is closure-only until parent no-spurion is signed; quadratic Weyl survives and now needs either no-tower proof or coefficient/operator normalization",
            "success_condition": "derive D_qWeyl2=0 from a parent no-higher-curvature/no-regeneration theorem, or source D_qWeyl2, L_q/G_q, and P_obs as nonclaim rows",
            "fallback_condition": "if coefficient/operator cannot be sourced, keep the analytic kernel as plumbing only and return to parent action object-language/no-tower derivation",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
    ]


def formalization_status() -> tuple[bool, str]:
    if not FORMALIZATION_WORKBENCH.exists():
        return True, "formalization-workbench path not found; generator has no write targets there"
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT_ROOT), "status", "--short", "--", "formalization-workbench"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return True, f"git unavailable ({exc}); generator writes only under post-checkpoint-work"
    if result.returncode == 0:
        changed = [line for line in result.stdout.splitlines() if line.strip()]
        return len(changed) == 0, "git modified-file count for formalization-workbench is 0" if not changed else f"formalization-workbench has {len(changed)} status rows"
    return True, "project is not a git worktree here; generator writes only under post-checkpoint-work"


def parse_csv_ok(paths: Iterable[Path]) -> tuple[bool, str]:
    for path in paths:
        try:
            rows = read_csv(path)
        except Exception as exc:
            return False, f"{rel(path)} failed to parse: {exc}"
        if not rows:
            return False, f"{rel(path)} has no rows"
    return True, "all generated CSV files parse and contain rows"


def no_positive_claim_flags(paths: Iterable[Path]) -> tuple[bool, str]:
    flag_columns = [
        "parent_signed",
        "theorem_zero",
        "numeric_value_present",
        "source_backed",
        "operator_domain_ready",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "passes_public_claim",
        "claim_gate_passed",
    ]
    offenders: list[str] = []
    for path in paths:
        for row in read_csv(path):
            row_name = row.get("row_id") or row.get("source_id") or "?"
            for column in flag_columns:
                if row.get(column, "").strip().lower() == "true":
                    offenders.append(f"{rel(path)}:{row_name}:{column}")
    if offenders:
        return False, "; ".join(offenders[:10])
    return True, "all generated claim/readiness flags remain negative"


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(row_id: str, ok: bool, detail: str) -> None:
        rows.append({"row_id": row_id, "status": "PASS" if ok else "FAIL", "detail": detail, "valid_for_claim": "false"})

    missing_sources = [str(row["source_path"]) for row in sources if row["path_exists"] != "true"]
    missing_needles = [str(row["source_id"]) for row in sources if row["needle_found"] != "true"]
    add("VAL2365_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2365_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2365_02_outputs_exist", all(path.exists() for path in generated), "all 2365 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2365_03_csv_parse", parse_ok, parse_detail)

    linear = {row["row_id"]: row["status"] for row in read_csv(outputs["linear"])}
    add("VAL2365_04_linear_index_kept", linear.get("LBZ2365_0_metric_trace") == "EXACT_INDEX_LEMMA", "linear one-Weyl index lemma retained")
    add("VAL2365_05_linear_demoted", linear.get("LBZ2365_4_linear_verdict") == "DEMOTE_TO_CLOSURE_ONLY", "linear BqWeyl route demoted to closure-only")

    contract = {row["row_id"]: row["status"] for row in read_csv(outputs["contract"])}
    add("VAL2365_06_no_spurion_unsigned", contract.get("NSC2365_6_verdict") == "CONTRACT_READY_THEOREM_NOT_SIGNED", "no-spurion contract ready but unsigned")

    bounds = {row["row_id"]: row["status"] for row in read_csv(outputs["bound"])}
    add("VAL2365_07_linear_bound_blocked", bounds.get("BQB2365_5_acceptance") == "CLAIM_BLOCKED", "linear BqWeyl finite row remains blocked")

    quadratic = {row["row_id"]: row["status"] for row in read_csv(outputs["quadratic"])}
    add("VAL2365_08_quadratic_survives", quadratic.get("QWR2365_0_DqWeyl2") == "LIVE_NONCLAIM_RESIDUAL", "DqWeyl2 survives the linear theorem")
    add("VAL2365_09_next_obstruction_selected", quadratic.get("QWR2365_5_verdict") == "SELECT_NEXT_COEFFICIENT_OR_Q_OPERATOR_TARGET", "quadratic Weyl coefficient/operator route selected")

    decisions = {row["row_id"]: row["decision"] for row in read_csv(outputs["decision"])}
    add("VAL2365_10_claim_refused", decisions.get("DEC2365_1_linear_claim") == "REFUSE_AND_DEMOTE", "premature linear zero claim refused")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2365_11_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2365_12_formalization_untouched", formal_ok, formal_detail)
    add("VAL2365_13_next_selected", read_csv(outputs["next"])[0].get("row_id") == "NEXT2365_0_selected", "2366 DqWeyl2 coefficient/operator target selected")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2365_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2365 valid: linear BqWeyl index route kept as closure-only, finite linear row blocked, quadratic Weyl branch selected next" if overall else "one or more validation gates failed",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(outputs: dict[str, Path]) -> None:
    def table(headers: list[str], rows: list[dict[str, str]]) -> str:
        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
        ]
        for row in rows:
            lines.append("| " + " | ".join(row.get(header, "").replace("|", "/") for header in headers) + " |")
        return "\n".join(lines)

    linear = read_csv(outputs["linear"])
    contract = read_csv(outputs["contract"])
    bound = read_csv(outputs["bound"])
    quadratic = read_csv(outputs["quadratic"])
    decisions = read_csv(outputs["decision"])
    next_rows = read_csv(outputs["next"])

    md = f"""# 2365 - q Representation No-Weyl-Spurion Or BqWeyl Bound Row

## Result

The good news is real but conditional: a single Weyl tensor cannot make a scalar linear source for scalar/quotient `q` using only the metric or epsilon tensor.  A nonzero linear term needs a four-index object like `P^{{abcd}}`, so the exact closure target is now sharp:

`B_qWeyl(linear)=0` if `q` is scalar/quotient/pure-density and the parent action has no Weyl-type spurion, projector, hidden tensor, or readout kernel.

The hard part is also clear: the current corpus does not parent-sign that object-language/no-spurion grammar.  Therefore the linear `B_qWeyl` route is demoted to closure-only, not claimed.  A numeric fallback is also blocked because `B_qWeyl`, `L_q/G_q`, the Weyl profile, and arena projection kernels are not sourced.

The next obstruction is quadratic Weyl: `q C_{{abcd}} C^{{abcd}}` and `q C_{{abcd}} *C^{{abcd}}` are not killed by the one-Weyl index theorem.  That branch needs a no-higher-curvature/no-regeneration proof or a sourced `D_qWeyl2` coefficient plus q-operator normalization.

## Linear BqWeyl Zero Audit

{table(["row_id", "audit_target", "status", "effect"], linear)}

## No-Spurion Contract

{table(["row_id", "clause", "status"], contract)}

## Linear BqWeyl Bound Row Status

{table(["row_id", "symbol", "status", "units"], bound)}

## Quadratic Weyl Re-entry

{table(["row_id", "symbol", "status", "reason_retained"], quadratic)}

## Decision Ledger

{table(["row_id", "route", "rank", "decision", "reason"], decisions)}

## Next Target

{table(["row_id", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["linear"])}`
- `{rel(outputs["contract"])}`
- `{rel(outputs["bound"])}`
- `{rel(outputs["quadratic"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is not circling; it is a narrowing strike.  The linear Weyl coupling now has a precise kill condition.  The project either derives that parent grammar, or it must carry a finite coefficient.  But even a successful linear kill does not finish local GR, because the quadratic Weyl/tower route remains live.  That is the next target.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def main() -> int:
    sources = source_register()
    outputs = {
        "source": RESIDUALS / "P8_Y5_PARENT_QLOC_2365_SOURCE_REGISTER.csv",
        "linear": RESIDUALS / "P8_Y5_PARENT_QLOC_2365_LINEAR_BQWEYL_ZERO_AUDIT.csv",
        "contract": RESIDUALS / "P8_Y5_PARENT_QLOC_2365_NO_SPURION_CONTRACT.csv",
        "bound": RESIDUALS / "P8_Y5_PARENT_QLOC_2365_BQWEYL_BOUND_ROW_STATUS.csv",
        "quadratic": RESIDUALS / "P8_Y5_PARENT_QLOC_2365_QUADRATIC_WEYL_REENTRY.csv",
        "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_2365_DECISION_LEDGER.csv",
        "claims": RESIDUALS / "P8_Y5_PARENT_QLOC_2365_CLAIM_GATES.csv",
        "refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_2365_REFUSAL_RUNNER.csv",
        "next": RESIDUALS / "P8_Y5_PARENT_QLOC_2365_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2365_VALIDATION.csv",
    }

    write_csv(outputs["source"], sources)
    write_csv(outputs["linear"], linear_bqweyl_zero_audit())
    write_csv(outputs["contract"], no_spurion_contract())
    write_csv(outputs["bound"], bqweyl_bound_row_status())
    write_csv(outputs["quadratic"], quadratic_weyl_reentry())
    write_csv(outputs["decision"], decision_ledger())
    write_csv(outputs["claims"], claim_gates())
    write_csv(outputs["refusal"], refusal_runner())
    write_csv(outputs["next"], next_target())
    validation = validation_rows(outputs, sources)
    write_csv(outputs["validation"], validation)
    write_markdown(outputs)

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
