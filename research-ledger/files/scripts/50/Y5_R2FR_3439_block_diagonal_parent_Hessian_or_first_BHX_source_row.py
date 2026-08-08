from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3439-Y5-R2FR-block-diagonal-parent-Hessian-or-first-BHX-source-row-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3438": ROOT / "3438-Y5-R2FR-metric-mixing-to-alpha-numerator-or-nonmetric-decoupling-proof-under-AX1090.md",
    "next_3438": OUT / "P8_Y5_R2FR_3438_NEXT_TARGET.csv",
    "schur_3438": OUT / "P8_Y5_R2FR_3438_METRIC_MIXING_SCHUR_THEOREM.csv",
    "decoupling_3438": OUT / "P8_Y5_R2FR_3438_NONMETRIC_DECOUPLING_CONDITIONS.csv",
    "operator_inputs_3438": OUT / "P8_Y5_R2FR_3438_OPERATOR_INPUT_ROWS.csv",
    "alpha_template_3438": OUT / "P8_Y5_R2FR_3438_METRIC_MIXING_ALPHA_TEMPLATE.csv",
    "direct_current_3437": OUT / "P8_Y5_R2FR_3437_DIRECT_MATTER_SOURCE_CURRENT_THEOREM.csv",
    "coupling_fork_3437": OUT / "P8_Y5_R2FR_3437_COUPLING_BRANCH_FORK.csv",
    "positive_x_nohair_1042": OUT / "P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv",
    "extra_silence_energy": OUT / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
    "field_silence_queue": OUT / "P8_FIELD_SPECIFIC_SILENCE_QUEUE.csv",
    "source_owner_contract": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "eh_selection_1512": ROOT / "1512-Y5-parent-EH-operator-selection-theorem-or-nonEH-residual-vector.md",
    "minimality_1513": ROOT / "1513-Y5-parent-primitive-minimality-no-higher-derivative-theorem-or-R11-vector-lock.md",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3439_SOURCE_REGISTER.csv",
    "block_diagonal_hessian_theorem": OUT / "P8_Y5_R2FR_3439_BLOCK_DIAGONAL_HESSIAN_THEOREM.csv",
    "bhx_obstruction_audit": OUT / "P8_Y5_R2FR_3439_BHX_OBSTRUCTION_AUDIT.csv",
    "bhx_input_row": OUT / "P8_Y5_R2FR_3439_BHX_INPUT_ROW.csv",
    "alpha_template_update": OUT / "P8_Y5_R2FR_3439_ALPHA_TEMPLATE_UPDATE.csv",
    "local_gr_impact": OUT / "P8_Y5_R2FR_3439_LOCAL_GR_IMPACT.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3439_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3439_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3439_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3439_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3439_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3438": "Schur law handoff",
        "next_3438": "3439 target declaration",
        "schur_3438": "metric-mixing Schur theorem",
        "decoupling_3438": "nonmetric decoupling conditions",
        "operator_inputs_3438": "B_i input blocker",
        "alpha_template_3438": "metric-mixing alpha template",
        "direct_current_3437": "direct matter current zero theorem",
        "coupling_fork_3437": "identity/class/metric-mixing fork",
        "positive_x_nohair_1042": "positive-X nohair identity",
        "extra_silence_energy": "extra-sector positive operator identities",
        "field_silence_queue": "motion/time/flow no-linear-source queue",
        "source_owner_contract": "parent action blocks",
        "eh_selection_1512": "EH selection and nonEH residual vector",
        "minimality_1513": "minimality/no-higher-derivative lock",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def block_diagonal_hessian_theorem() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "BDH3439_0_define_BHX",
            "statement": "The metric/X mixing block is the mixed Hessian of the local parent action at the local vacuum.",
            "formula": "B_i := delta^2 S_parent / (delta h_H delta X_i)|_{g0,X0}",
            "status": "DEFINITION_FROM_3438",
            "condition_or_missing": "requires gauge-fixed h_H and finite-mode variable X_i",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BDH3439_1_even_X_vacuum_zero",
            "statement": "If the parent X-sector is even in X_i and expanded about X_i=0 with no background gradient, no linear source, and no linear curvature/readout term, then the h-X mixed Hessian vanishes.",
            "formula": "S_X=sqrt(-g)[1/2 Z_i(g)(nabla X_i)^2+1/2 M_i^2(g)X_i^2+O(X_i^4)] => delta_h delta_X S_X|_{X=0,nabla X=0}=0",
            "status": "EXACT_CONDITIONAL_BLOCK_DIAGONAL_THEOREM",
            "condition_or_missing": "needs parent-signed even/no-linear-X/local-vacuum premises",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BDH3439_2_metric_dependence_not_enough",
            "statement": "Metric dependence of the X kinetic/mass coefficients does not itself create linear h-X mixing at X=0.",
            "formula": "delta_g[Z(g)(nabla X)^2] is h X^2 or h (nabla X)^2, not h X, at the zero background",
            "status": "DERIVED_GUARDRAIL_NONCLAIM",
            "condition_or_missing": "fails if background X0 or nabla X0 is nonzero",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BDH3439_3_linear_curvature_obstruction",
            "statement": "A term linear in X_i times curvature or a source-normalization scalar creates B_i and defeats block diagonalization.",
            "formula": "S_mix=int sqrt(-g) c_i X_i R[g] or c_i X_i U_source[g] => B_i ~ c_i delta R/delta h_H",
            "status": "NO_GO_IF_LINEAR_XR_OR_TADPOLE_ALLOWED",
            "condition_or_missing": "parent must forbid linear X_i R, X_i T, X_i U_source, boundary X_i charge and readout X_i terms",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BDH3439_4_current_status",
            "statement": "The theorem gives the least-scrutiny route for B_i=0, but current MTS has not parent-signed the even/no-linear-X grammar for every finite channel.",
            "formula": "B_i=0 is theorem-ready for the clean branch; B_i row remains retained until parent grammar signs it",
            "status": "BRANCH_THEOREM_CANDIDATE_NOT_CLAIM",
            "condition_or_missing": "no parent-signed no-linear-X/no-XR/no-boundary-X clause yet",
            "valid_for_claim": False,
        },
    ]


def bhx_obstruction_audit() -> list[dict[str, Any]]:
    return [
        {
            "obstruction_id": "BHXO3439_0_linear_XR",
            "obstruction": "linear nonminimal curvature coupling",
            "term": "int sqrt(-g) c_XR X_i R",
            "effect_on_BHX": "B_i nonzero in scalar metric channel",
            "current_status": "NOT_FORBIDDEN_BY_PARENT_GRAMMAR",
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "BHXO3439_1_tadpole",
            "obstruction": "local vacuum not stationary in X_i",
            "term": "int sqrt(-g) J_0(g) X_i",
            "effect_on_BHX": "metric variation of J_0 drives X_i",
            "current_status": "STATIONARY_X0_PREMISE_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "BHXO3439_2_background_gradient",
            "obstruction": "nonzero background X_i or gradient in compact exterior",
            "term": "X0 != 0 or nabla X0 != 0",
            "effect_on_BHX": "metric variation of kinetic/mass terms can be linear in delta X",
            "current_status": "LOCAL_VACUUM_BACKGROUND_ZERO_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "BHXO3439_3_boundary_X",
            "obstruction": "boundary/projector/readout term linear in X_i",
            "term": "int_boundary B_i(g,P,domain) X_i",
            "effect_on_BHX": "bulk B_i may vanish while source-visible tail survives",
            "current_status": "BOUNDARY_PROJECTOR_TAIL_OPEN",
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "BHXO3439_4_class_metric",
            "obstruction": "matter metric or source-normalization readout depends on X_i",
            "term": "g_hat=exp(F(X_i))g or mu_obs=mu_obs(X_i)",
            "effect_on_BHX": "reintroduces effective metric/source coupling outside direct S_X",
            "current_status": "CLASS_METRIC_BRANCH_RETAINED",
            "valid_for_claim": False,
        },
    ]


def bhx_input_row() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "BHX3439_0_clean_branch_zero_candidate",
            "symbol": "B_i",
            "definition": "delta^2 S_parent/(delta h_H delta X_i)|local vacuum",
            "candidate_value": "0",
            "status": "EXACT_CONDITIONAL_ZERO_IF_EVEN_X_GRAMMAR_SIGNED",
            "required_source_path": "parent action grammar forbidding linear X_i R / X_i source / boundary X_i",
            "units": "operator_units_hX_declared_by_parent_normalization",
            "arena_projection": "R10;PPN;Newton/source-normalization",
            "valid_for_claim": False,
        },
        {
            "row_id": "BHX3439_1_fallback_source_row",
            "symbol": "B_i",
            "definition": "nonzero h-X Hessian entry if any obstruction survives",
            "candidate_value": "MISSING_NUMERIC_OR_SYMBOLIC_OPERATOR_VALUE",
            "status": "SOURCE_READY_TEMPLATE_NONCLAIM",
            "required_source_path": "parent Hessian expansion with gauge projector, source/test projector and units",
            "units": "MISSING_UNITS",
            "arena_projection": "alpha_i^{gX}; gamma_minus_1; beta_minus_1; epsilon_range",
            "valid_for_claim": False,
        },
    ]


def alpha_template_update() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "ATU3439_0_if_clean_branch_signed",
            "component": "alpha_i^{gX}",
            "before": "Xi_R10*tau_i*Qbar_i_S_gX*qbar_i_T_gX/(4*pi*G0*Z_i)",
            "after": "0 for the metric-mixing component only",
            "condition": "BDH3439_1 plus all BHX obstruction rows forbidden/zero",
            "valid_for_claim": False,
        },
        {
            "update_id": "ATU3439_1_if_linear_XR_allowed",
            "component": "alpha_i^{gX}",
            "before": "template-only metric mixing",
            "after": "Xi_R10*tau_i*(Qbar_i_S_gX*qbar_i_T_gX/(4*pi*G0*Z_i)+alpha_i_tail)",
            "condition": "B_i nonzero; must source B_i, Z_i, M_i^2, projections and tail",
            "valid_for_claim": False,
        },
        {
            "update_id": "ATU3439_2_total_alpha_guard",
            "component": "alpha_total",
            "before": "direct matter component zeroed conditionally at 3437",
            "after": "alpha_total still includes class metric, boundary/projector, q_loc and nonEH tails",
            "condition": "no cancellation credit between components",
            "valid_for_claim": False,
        },
    ]


def local_gr_impact() -> list[dict[str, Any]]:
    return [
        {
            "impact_id": "LGI3439_0_real_progress",
            "local_gr_gate": "metric-mixing leg",
            "status": "CLEAN_BRANCH_THEOREM_CANDIDATE",
            "impact": "B_i can be zero for an even/nonmetric X sector at X0=0 without assuming smallness",
            "remaining_blocker": "parent grammar has to forbid linear X curvature/source/boundary/readout terms",
            "valid_for_claim": False,
        },
        {
            "impact_id": "LGI3439_1_not_enough_for_GR",
            "local_gr_gate": "full local GR",
            "status": "STILL_BLOCKED",
            "impact": "even if B_i closes, source normalization, boundary/projector tails, EH selection, PPN beta/gamma and R10 curve gates remain",
            "remaining_blocker": "A3/A4/A5/A8/A10 and PPN residual stack",
            "valid_for_claim": False,
        },
        {
            "impact_id": "LGI3439_2_next_pressure",
            "local_gr_gate": "parent grammar",
            "status": "NEXT_ROOT_TARGET",
            "impact": "the next proof must decide whether no-linear-X is derived from MTS primitives or adopted as closure",
            "remaining_blocker": "parent object-language/no-linear-X theorem",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3439_0_block_diagonal_theorem",
            "gate": "conditional B_i=0 theorem exists",
            "result": "PASS_BRANCH_THEOREM_NONCLAIM",
            "evidence": "BDH3439_1",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3439_1_parent_signed_Bzero",
            "gate": "MTS parent signs B_i=0 for the finite channels",
            "result": "BLOCKED_PARENT_GRAMMAR_UNSIGNED",
            "evidence": "BHXO3439 obstruction clauses remain possible",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3439_2_first_BHX_row",
            "gate": "source-ready B_HX fallback row exists",
            "result": "PASS_TEMPLATE_NONCLAIM",
            "evidence": "BHX3439_1_fallback_source_row",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3439_3_R10_alpha",
            "gate": "R10 alpha(lambda) metric-mixing leg can be scored",
            "result": "BLOCKED",
            "evidence": "B_i zero not parent-signed and fallback B_i value missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3439_4_local_GR",
            "gate": "local GR/Newton branch is derived",
            "result": "BLOCKED",
            "evidence": "B_i progress is one leg; source normalization/EH/PPN/boundary remain open",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3439_0_progress",
            "decision": "Keep the even/nonmetric-X block-diagonal theorem as the clean B_i route.",
            "reason": "It proves B_i=0 from action parity/stationary vacuum rather than from empirical smallness.",
            "next_action": "derive parent no-linear-X/no-XR grammar from MTS primitives",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3439_1_guard",
            "decision": "Do not promote B_i=0 yet.",
            "reason": "Linear X R, tadpole, boundary X, class metric and background-gradient terms are not parent-forbidden.",
            "next_action": "turn obstruction audit into a parent object-language theorem or explicit closure ledger",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3439_2_best_next",
            "decision": "Attack the no-linear-X parent grammar next.",
            "reason": "This signs B_i=0, strengthens positive nohair, and closes a major R10/PPN leak without needing data first.",
            "next_action": "3440 no-linear-X parent grammar or closure demotion",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3440-Y5-R2FR-no-linear-X-parent-grammar-or-explicit-closure-demotion-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3440_no_linear_X_parent_grammar_or_explicit_closure_demotion.py",
            "objective": "derive whether the MTS parent object-language forbids linear X_i R, X_i source, X_i boundary/readout and nonzero local X backgrounds; if not, demote B_i=0 to explicit closure and keep B_HX source rows",
            "success_condition": "a parent grammar theorem that signs the even/nonmetric-X branch, or a closure ledger that marks B_i=0 as an assumption and routes nonzero B_i to R10/PPN source rows",
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3439_0",
            "status": "BLOCK_DIAGONAL_HESSIAN_THEOREM_CANDIDATE_WRITTEN_NONCLAIM",
            "claim_allowed": False,
            "reason": "B_i=0 is exact under even/no-linear-X local-vacuum grammar, but the grammar is not parent-signed",
            "next_safe_action": "derive no-linear-X grammar before treating metric mixing as closed",
            "valid_for_claim": False,
        }
    ]


def all_generated_nonclaim(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for output_name, rows in rows_by_name.items():
        if output_name == "validation":
            continue
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    theorem_rows = rows_by_name["block_diagonal_hessian_theorem"]
    obstruction_rows = rows_by_name["bhx_obstruction_audit"]
    input_rows = rows_by_name["bhx_input_row"]
    promotion_rows = rows_by_name["promotion_gates"]
    next_rows = rows_by_name["next_target"]
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1 for checked_path in FORMALIZATION.rglob("*") if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )
    validations = [
        {
            "check_id": "VAL3439_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3439_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": all(str(path).startswith(str(ROOT)) for path in OUTPUTS.values()),
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3439_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": all_generated_nonclaim(rows_by_name),
            "detail": "valid_for_claim=false and claim_allowed=false throughout generated rows",
        },
        {
            "check_id": "VAL3439_3_Bzero_theorem",
            "condition": "conditional B_i=0 theorem exists",
            "passed": any(row["theorem_id"] == "BDH3439_1_even_X_vacuum_zero" and row["status"] == "EXACT_CONDITIONAL_BLOCK_DIAGONAL_THEOREM" for row in theorem_rows),
            "detail": "even/nonmetric-X local-vacuum branch gives B_i=0",
        },
        {
            "check_id": "VAL3439_4_obstructions_retained",
            "condition": "linear XR/tadpole/boundary/class obstructions are retained",
            "passed": len(obstruction_rows) >= 5 and all(str(row["current_status"]).endswith(("OPEN", "RETAINED", "UNSIGNED", "POSSIBLE")) or row["current_status"] in {"NOT_FORBIDDEN_BY_PARENT_GRAMMAR", "STATIONARY_X0_PREMISE_NOT_PARENT_SIGNED", "LOCAL_VACUUM_BACKGROUND_ZERO_NOT_PARENT_SIGNED", "BOUNDARY_PROJECTOR_TAIL_OPEN", "CLASS_METRIC_BRANCH_RETAINED"} for row in obstruction_rows),
            "detail": f"{len(obstruction_rows)} obstruction rows retained",
        },
        {
            "check_id": "VAL3439_5_BHX_source_row",
            "condition": "fallback B_HX source row exists",
            "passed": any(row["row_id"] == "BHX3439_1_fallback_source_row" and row["status"] == "SOURCE_READY_TEMPLATE_NONCLAIM" for row in input_rows),
            "detail": "nonzero B_i has a source-ready row shape",
        },
        {
            "check_id": "VAL3439_6_no_promotion",
            "condition": "B_i=0 and local GR are not promoted",
            "passed": any(row["gate_id"] == "PG3439_1_parent_signed_Bzero" and row["result"] == "BLOCKED_PARENT_GRAMMAR_UNSIGNED" for row in promotion_rows)
            and any(row["gate_id"] == "PG3439_4_local_GR" and row["result"] == "BLOCKED" for row in promotion_rows),
            "detail": "parent grammar unsigned and local GR blocked",
        },
        {
            "check_id": "VAL3439_7_next_target",
            "condition": "next target attacks no-linear-X parent grammar",
            "passed": "no-linear-X" in next_rows[0]["target_doc"],
            "detail": next_rows[0]["target_doc"],
        },
        {
            "check_id": "VAL3439_8_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3439_9_overall",
            "condition": "3439 B_HX checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3439 - Block-Diagonal Parent Hessian or First BHX Source Row

## Summary
- This checkpoint attacks the exact `B_i` object isolated in 3438.
- The useful theorem is simple and strong: if `X_i` is an even, nonmetric finite mode expanded about `X_i=0` with no local background gradient, no tadpole, no linear `X_i R`, and no boundary/readout `X_i` source, then `B_i = delta^2 S_parent/(delta h_H delta X_i)=0`.
- That means metric dependence of the `X_i` kinetic/mass terms is not automatically fatal; at a zero background it is at least quadratic in `X_i`, so it does not create an `h-X` Hessian entry.
- But the theorem is not yet a claim: the parent grammar has not forbidden linear `X_i R`, tadpoles, boundary/projector `X_i`, class-metric pullbacks, or nonzero local backgrounds.
- A fallback `B_HX` source row is now staged, so if the clean theorem fails, `B_i` becomes an explicit R10/PPN numerator input rather than a fog bank.

## Source Register
{md_table(rows_by_name["source_register"])}

## Block-Diagonal Hessian Theorem
{md_table(rows_by_name["block_diagonal_hessian_theorem"])}

## BHX Obstruction Audit
{md_table(rows_by_name["bhx_obstruction_audit"])}

## BHX Input Row
{md_table(rows_by_name["bhx_input_row"])}

## Alpha Template Update
{md_table(rows_by_name["alpha_template_update"])}

## Local GR Impact
{md_table(rows_by_name["local_gr_impact"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
This is a good rung. We now have a real conditional theorem for why metric/X mixing can vanish, and it is not just “because we want it to”. The next job is to prove the no-linear-X parent grammar; if that closes, the local-GR route gets significantly cleaner. If it does not, `B_i` is a named operator coefficient to source and bound.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "block_diagonal_hessian_theorem": block_diagonal_hessian_theorem(),
        "bhx_obstruction_audit": bhx_obstruction_audit(),
        "bhx_input_row": bhx_input_row(),
        "alpha_template_update": alpha_template_update(),
        "local_gr_impact": local_gr_impact(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3439 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
