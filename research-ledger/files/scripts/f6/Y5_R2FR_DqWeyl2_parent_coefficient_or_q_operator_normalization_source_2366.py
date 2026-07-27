from __future__ import annotations

import csv
import subprocess
from pathlib import Path
from typing import Iterable


BRANCH_ID = "MTS_R2FR_DQWEYL2_PARENT_COEFFICIENT_OR_Q_OPERATOR_NORMALIZATION_SOURCE_2366"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2366-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md"
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
        ("SRC2366_2365_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2365_NEXT_TARGET.csv", "NEXT2365_0_selected", "2365 selected DqWeyl2 coefficient/operator target"),
        ("SRC2366_2365_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2365_VALIDATION.csv", "VAL2365_OVERALL", "2365 validation"),
        ("SRC2366_2308_coeff", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2308_DQWEYL2_PARENT_COEFFICIENT_AUDIT.csv", "DCO2308_3_verdict", "DqWeyl2 coefficient unsourced"),
        ("SRC2366_2308_operator", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2308_Q_OPERATOR_X_BRIDGE_AUDIT.csv", "QOP2308_4_verdict", "q operator/q-X bridge unsourced"),
        ("SRC2366_2308_action", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2308_Q_LOCAL_ACTION_NORMAL_FORM_CONTRACT.csv", "NF2308_1_variation", "q local action variation contract"),
        ("SRC2366_2309_trichotomy", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2309_QX_TRICHOTOMY_THEOREM.csv", "TRI2309_4_verdict", "q-X/independent/auxiliary branch not selected claim-grade"),
        ("SRC2366_2310_branch", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2310_BRANCH_SELECTION_SCORECARD.csv", "BSEL2310_4_verdict", "no-pole primary, independent q fallback staged"),
        ("SRC2366_2313_bound", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2313_INDEPENDENT_Q_BOUND_RUNNER_ACTIVATION.csv", "RUN2313_6_score_gate", "independent q bound runner active nonclaim"),
        ("SRC2366_2314_hessian", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2314_HESSIAN_SOURCE_HUNT.csv", "HUNT2314_5_verdict", "conditional operator fill imported but not claim-grade"),
        ("SRC2366_2314_green", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2314_GREEN_FUNCTION_NORMALIZATION_CONTRACT.csv", "GF2314_1_covariance_range", "conditional lambda_q=xi_q range result"),
        ("SRC2366_2315_domain", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2315_GREEN_DOMAIN_SECOND_FILL.csv", "GD2315_2_algebraic_limit", "finite residual formulas after conditional operator fill"),
        ("SRC2366_2315_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2315_NEXT_TARGET.csv", "NEXT2315_0", "j_q source-leg target selected in old chain"),
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


def dqweyl2_coefficient_audit() -> list[dict[str, object]]:
    rows = [
        ("DQC2366_0_definition", "D_qWeyl2", "coefficient of q C_abcd C^abcd in the local parent/effective q equation or action", "DEFINED_REQUIRED_INPUT", "no parent action coefficient yet"),
        ("DQC2366_1_zero_route", "D_qWeyl2=0", "no bare Weyl2/qWeyl2 operator and no induced tower after eliminating hidden/projector/memory sectors", "ZERO_ROUTE_NOT_DERIVED", "no-higher-curvature/no-regeneration theorem unsigned"),
        ("DQC2366_2_numeric_route", "finite D_qWeyl2", "source-backed sign, units, uncertainty, q normalization, and no-cancellation convention", "NO_NUMERIC_SOURCE_FOUND", "no inspected source supplies a value"),
        ("DQC2366_3_kernel", "C2 exterior source kernel", "C_abcd C^abcd = 48 mu^2/r^6 and integral_D C^2 dV = 64*pi*mu^2/R_body^3 outside a compact body", "ANALYTIC_KERNEL_READY_NONCLAIM", "kernel is plumbing only without D_qWeyl2 and L_q"),
        ("DQC2366_4_verdict", "DqWeyl2 coefficient status", "the quadratic Weyl source is not zeroed or numerically sourced", "COEFFICIENT_UNSOURCED", "cannot score R10/PPN/orbital/clock/local-GR branch"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "target": target,
            "definition_or_formula": definition,
            "status": status,
            "effect": effect,
        }
        for row_id, target, definition, status, effect in rows
    ]


def q_operator_normalization_audit() -> list[dict[str, object]]:
    rows = [
        ("QON2366_0_qX_bridge", "q=aX identity bridge", "if q=aX+O(X^2), then Z_q=Z_X/a^2, M_q^2=M_X^2/a^2, D_qWeyl2=D_XWeyl2/a", "BRIDGE_FORMULA_EXACT_IF_SIGNED_NOT_SIGNED", "scale a, shared domain, and X coefficients missing"),
        ("QON2366_1_independent_q", "independent physical q Hessian", "L_q=-Z_q Delta+M_q^2 with source vector S_q", "FALLBACK_BRANCH_ACTIVE_NONCLAIM", "needs its own Z_q, M_q^2, D_qWeyl2, J_q and boundary/source rows"),
        ("QON2366_2_conditional_mass", "M_q^2", "M_q^2=n_q^A H_AB n_q^B if q=0 is a parent-selected covariance equilibrium and H is positive transverse to quotient", "CONDITIONAL_FORMULA_IMPORTED", "selector/parent Hessian not signed or numeric"),
        ("QON2366_3_conditional_stiffness", "Z_q", "Z_q=xi_q^2 n_q^A H_AB n_q^B from finite smoothing/correlation length", "CONDITIONAL_FORMULA_IMPORTED", "xi_q and domain are not source-backed"),
        ("QON2366_4_range", "lambda_q", "lambda_q=sqrt(Z_q/M_q^2)=xi_q in the 2281 covariance-Hessian branch", "EXACT_CONDITIONAL_RATIO_NONCLAIM", "range not free, but xi_q is not yet sourced"),
        ("QON2366_5_verdict", "q operator normalization", "operator shape is no longer blank, but it is conditional and not score-ready", "PARTIAL_CONDITIONAL_OPERATOR_NOT_CLAIM_GRADE", "next bottleneck is source numerator/coupling vector"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "object": obj,
            "formula_or_statement": formula,
            "status": status,
            "missing_or_effect": effect,
        }
        for row_id, obj, formula, status, effect in rows
    ]


def finite_residual_formula_ledger() -> list[dict[str, object]]:
    rows = [
        ("FRF2366_0_dynamic_kernel", "dynamic massive q branch", "G_q(r)=exp(-r/xi_q)/(4*pi*Z_q*r) when Z_q=xi_q^2 M_q^2", "FORMAL_KERNEL_CONDITIONAL", "needs xi_q, Z_q normalization, boundary/domain, source vector, P_obs"),
        ("FRF2366_1_source_vector", "quadratic Weyl plus source legs", "S_q = D_qWeyl2 C^2 + D_qWeylDual C*C + J_q + Q_q_body + Pi_q + tail_q", "SOURCE_VECTOR_SYMBOLIC", "every source component must be zero-proved or bounded absolutely"),
        ("FRF2366_2_compact_source_response", "compact source far field", "q(r) ~ Q_q_eff exp(-r/xi_q)/(4*pi Z_q r)", "PROFILE_SHAPE_READY_INPUTS_MISSING", "Q_q_eff is not sourced because D_qWeyl2 and J_q are missing"),
        ("FRF2366_3_algebraic_limit", "auxiliary/algebraic q branch", "if Z_q=0, q=S_q/M_q^2 and q_R=j_q/(n_q^A H_AB n_q^B)", "EXACT_CONDITIONAL_FORMULA_INPUTS_MISSING", "j_q and Hessian denominator are not source-backed"),
        ("FRF2366_4_closure_control", "q=0 benchmark", "q=0 remains a labelled closure/control branch only", "BENCHMARK_ONLY", "not a derivation of GR/Newton"),
        ("FRF2366_5_verdict", "local residual formula status", "denominator shape is conditionally improved; numerator/source vector is now the highest-value missing object", "SELECT_NUMERATOR_SOURCE_LEG_NEXT", "j_q controls whether finite q branch is harmless or testable"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "branch_or_object": obj,
            "formula": formula,
            "status": status,
            "blocking_input": block,
        }
        for row_id, obj, formula, status, block in rows
    ]


def branch_decision() -> list[dict[str, object]]:
    rows = [
        ("BRD2366_0_no_pole", "q quotient/first-class/no-pole removal", 1, "KEEP_AS_BEST_GR_ROUTE_UNSIGNED", "cleanest local GR/Newton route, but Omega/momentum map/descent/boundary clauses are missing"),
        ("BRD2366_1_qX_bridge", "copy X operator by q=aX", 4, "REJECT_CURRENT_COPYING", "formula exists, but q=aX and scale/domain/source convention are not signed"),
        ("BRD2366_2_independent_q", "independent q Hessian/bound runner", 2, "ACTIVE_FALLBACK_NONCLAIM", "symplectic/no-pole source hunt was negative, so finite bound lane stays active"),
        ("BRD2366_3_DqWeyl2", "quadratic Weyl coefficient scoring", 4, "BLOCKED_INPUTS_MISSING", "D_qWeyl2 and operator/projection rows are not source-backed"),
        ("BRD2366_4_jq", "j_q numerator/source-leg theorem or finite pack", 1, "SELECT_NEXT_TARGET", "after the conditional denominator fill, numerator silence is the highest leverage local-GR target"),
        ("BRD2366_5_empirical", "R10/PPN/clock/orbital scoring", 5, "DEFER", "no claim-grade prediction vector exists yet"),
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
        ("CG2366_0_DqWeyl2_zero", "D_qWeyl2 theorem-zero derived", "BLOCKED", "no-tower/no-regeneration theorem unsigned"),
        ("CG2366_1_DqWeyl2_numeric", "D_qWeyl2 numeric coefficient sourced", "BLOCKED", "coefficient, units, sign, uncertainty missing"),
        ("CG2366_2_q_operator", "q operator/range score-ready", "BLOCKED", "Z_q/M_q^2/xi_q are conditional, not source-backed"),
        ("CG2366_3_q_source", "q source numerator and tails zero/bounded", "BLOCKED", "j_q, body, boundary, readout tails are open"),
        ("CG2366_4_projection", "P_arena projection ready", "BLOCKED", "R10/PPN/clock/orbital maps not normalized to q branch"),
        ("CG2366_5_local_GR_Newton", "local GR/Newton reduction derived", "BLOCKED", "q no-pole and finite residual gates remain open"),
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
        ("REF2366_0_score_DqWeyl2", "score D_qWeyl2 branch now", "needs D_qWeyl2, Z_q/M_q^2/xi_q, source vector, and P_arena", "REFUSED"),
        ("REF2366_1_copy_X", "borrow X operator values for q", "needs q=aX bridge, scale a, shared domain, and X coefficients", "REFUSED"),
        ("REF2366_2_claim_lambda", "treat lambda_q=xi_q as numeric evidence", "xi_q is not source-backed and the parent selector is unsigned", "REFUSED"),
        ("REF2366_3_GR", "claim local GR/Newton", "no-pole certificate and finite residual source pack remain open", "REFUSED"),
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
            "row_id": "NEXT2366_0_selected",
            "next_file": "2367-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack.md",
            "next_script": "scripts/Y5_R2FR_jq_source_leg_zero_theorem_or_finite_source_pack_2367.py",
            "selected_reason": "DqWeyl2 coefficient is unsourced and the q operator is only conditionally filled; with the denominator shape improved, the source numerator j_q is the highest-value route to local GR/Newton",
            "success_condition": "derive j_q=0 from parent matter/source/current descent in the same observed coframe, or stage finite j_q/body/boundary/tail rows with units and arena projections",
            "fallback_condition": "if j_q zero theorem fails, keep independent q bound runner nonclaim and fill finite source-coupling priors rather than claiming local GR",
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
    add("VAL2366_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2366_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2366_02_outputs_exist", all(path.exists() for path in generated), "all 2366 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2366_03_csv_parse", parse_ok, parse_detail)

    coeff = {row["row_id"]: row["status"] for row in read_csv(outputs["coeff"])}
    add("VAL2366_04_coeff_unsourced", coeff.get("DQC2366_4_verdict") == "COEFFICIENT_UNSOURCED", "DqWeyl2 coefficient remains unsourced")
    add("VAL2366_05_kernel_nonclaim", coeff.get("DQC2366_3_kernel") == "ANALYTIC_KERNEL_READY_NONCLAIM", "analytic Weyl2 kernel retained as nonclaim")

    operator = {row["row_id"]: row["status"] for row in read_csv(outputs["operator"])}
    add("VAL2366_06_operator_conditional", operator.get("QON2366_5_verdict") == "PARTIAL_CONDITIONAL_OPERATOR_NOT_CLAIM_GRADE", "q operator only conditionally filled")
    add("VAL2366_07_lambda_ratio", operator.get("QON2366_4_range") == "EXACT_CONDITIONAL_RATIO_NONCLAIM", "lambda_q=xi_q recorded as conditional ratio")

    formulas = {row["row_id"]: row["status"] for row in read_csv(outputs["formulas"])}
    add("VAL2366_08_numerator_selected", formulas.get("FRF2366_5_verdict") == "SELECT_NUMERATOR_SOURCE_LEG_NEXT", "j_q numerator/source leg selected next")

    decisions = {row["row_id"]: row["decision"] for row in read_csv(outputs["decision"])}
    add("VAL2366_09_next_decision", decisions.get("BRD2366_4_jq") == "SELECT_NEXT_TARGET", "decision ledger selects j_q target")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2366_10_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2366_11_formalization_untouched", formal_ok, formal_detail)
    add("VAL2366_12_next_selected", read_csv(outputs["next"])[0].get("row_id") == "NEXT2366_0_selected", "2367 j_q source-leg target selected")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2366_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2366 valid: DqWeyl2 coefficient unsourced, q operator conditionally filled, j_q numerator/source-leg route selected next" if overall else "one or more validation gates failed",
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

    coeff = read_csv(outputs["coeff"])
    operator = read_csv(outputs["operator"])
    formulas = read_csv(outputs["formulas"])
    decisions = read_csv(outputs["decision"])
    next_rows = read_csv(outputs["next"])

    md = f"""# 2366 - DqWeyl2 Parent Coefficient Or q Operator Normalization Source

## Result

The quadratic Weyl branch has been consolidated.  The coefficient `D_qWeyl2` is still not sourced and is not theorem-zero.  The useful nonclaim plumbing is the exterior Weyl-squared kernel:

`C_abcd C^abcd = 48 mu^2/r^6`, with compact exterior integral `64*pi*mu^2/R_body^3`.

The q operator is no longer completely blank, but it is only conditional.  In the covariance-Hessian branch:

`M_q^2 = n_q^A H_AB n_q^B`, `Z_q = xi_q^2 n_q^A H_AB n_q^B`, so `lambda_q = sqrt(Z_q/M_q^2) = xi_q`.

That is progress, not evidence.  `xi_q`, `Z_q`, `M_q^2`, `D_qWeyl2`, source terms, boundary tails, and arena projections are still not source-backed.  Since the denominator shape is now conditionally sharper, the next high-value target is the numerator/source leg `j_q`: either prove `j_q=0` from parent matter/source/current descent, or stage it as a finite source pack.

## DqWeyl2 Coefficient Audit

{table(["row_id", "target", "status", "effect"], coeff)}

## q Operator Normalization Audit

{table(["row_id", "object", "status", "missing_or_effect"], operator)}

## Finite Residual Formula Ledger

{table(["row_id", "branch_or_object", "status", "blocking_input"], formulas)}

## Branch Decision

{table(["row_id", "route", "rank", "decision", "reason"], decisions)}

## Next Target

{table(["row_id", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["coeff"])}`
- `{rel(outputs["operator"])}`
- `{rel(outputs["formulas"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This narrows the GR/Newton route.  The project has not proved local GR yet, but it has stopped smuggling the q denominator.  The remaining finite branch now looks like `q_R=j_q/(n_q H n_q)` in the algebraic/weak-field limit, with curvature and boundary source terms still live.  So the next useful fight is the coupling numerator, not another lap around the denominator.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def main() -> int:
    sources = source_register()
    outputs = {
        "source": RESIDUALS / "P8_Y5_PARENT_QLOC_2366_SOURCE_REGISTER.csv",
        "coeff": RESIDUALS / "P8_Y5_PARENT_QLOC_2366_DQWEYL2_COEFFICIENT_AUDIT.csv",
        "operator": RESIDUALS / "P8_Y5_PARENT_QLOC_2366_Q_OPERATOR_NORMALIZATION_AUDIT.csv",
        "formulas": RESIDUALS / "P8_Y5_PARENT_QLOC_2366_FINITE_RESIDUAL_FORMULA_LEDGER.csv",
        "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_2366_BRANCH_DECISION.csv",
        "claims": RESIDUALS / "P8_Y5_PARENT_QLOC_2366_CLAIM_GATES.csv",
        "refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_2366_REFUSAL_RUNNER.csv",
        "next": RESIDUALS / "P8_Y5_PARENT_QLOC_2366_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2366_VALIDATION.csv",
    }

    write_csv(outputs["source"], sources)
    write_csv(outputs["coeff"], dqweyl2_coefficient_audit())
    write_csv(outputs["operator"], q_operator_normalization_audit())
    write_csv(outputs["formulas"], finite_residual_formula_ledger())
    write_csv(outputs["decision"], branch_decision())
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
