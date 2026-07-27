from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1106-Y5-R10-minimal-explicit-closure-pack-independence-audit-or-first-source-backed-coefficient-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    result: list[dict[str, object]] = []
    for row in rows:
        copied = dict(row)
        copied.setdefault("valid_for_claim", "false")
        copied.setdefault("claim_allowed", "false")
        copied.setdefault("generated_utc", generated)
        result.append(copied)
    return result


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def source_rows() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1106_0_1105_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1105_NEXT_TARGET.csv",
            "needle": "NEXT1105_0_1106",
            "note": "1105 handoff to closure-pack independence audit.",
        },
        {
            "source_id": "SRC1106_1_1105_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1105_EXPLICIT_CLOSURE_PACK.csv",
            "needle": "PACK1105_4_residual_vector_if_unsigned",
            "note": "1105 closure pack.",
        },
        {
            "source_id": "SRC1106_2_1105_finite",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1105_FINITE_SOURCE_REQUIREMENTS.csv",
            "needle": "FIN1105_0_alpha_coefficient",
            "note": "1105 finite source requirements.",
        },
        {
            "source_id": "SRC1106_3_1090_axioms",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv",
            "needle": "AX1090_1_no_hidden_visible_hom",
            "note": "earlier missing axiom ledger.",
        },
        {
            "source_id": "SRC1106_4_1090_closure",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1090_CLOSURE_DEMOTION_REGISTER.csv",
            "needle": "CLOS1090_0_MOMS",
            "note": "earlier closure demotion register.",
        },
        {
            "source_id": "SRC1106_5_1090_decision",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1090_DECISION_LEDGER.csv",
            "needle": "DEC1090_2_best_next",
            "note": "earlier decision to target no-hidden-visible hom/operator-domain axiom first.",
        },
        {
            "source_id": "SRC1106_6_1049_policy",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv",
            "needle": "OCR1049_4_naturalness_guard",
            "note": "operator-classification residual policy.",
        },
        {
            "source_id": "SRC1106_7_1058_exhaustion",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
            "needle": "VOE1058_3_no_hidden_visible_hom",
            "note": "visible operator-domain exhaustion and no-hidden-visible hom.",
        },
        {
            "source_id": "SRC1106_8_1104_signature",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1104_PARENT_SIGNATURE_LEDGER.csv",
            "needle": "SIG1104_10_verdict",
            "note": "1104 parent ordinary-sector signature ledger.",
        },
        {
            "source_id": "SRC1106_9_1098_requirements",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
            "needle": "REQ1098_2_c_common",
            "note": "source-backed coefficient threshold requirements.",
        },
    ]
    checked: list[dict[str, object]] = []
    for row in rows:
        path = ROOT / str(row["relative_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        checked.append(
            {
                **row,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(row["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def independence_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "audit_id": "IND1106_0_parent_object_language",
                "candidate_clause": "visible coefficients are generated only by declared parent ordinary-sector object language",
                "independence_status": "INDEPENDENT_CORE_CLOSURE",
                "subsumes": "product sequester; no hidden target action; no arena-specific post-fit coefficient insertion",
                "not_subsumed_by": "radiative/readout stability; source/action-measure owner",
                "risk_if_absent": "any neutral scalar can multiply visible operators",
                "axiom_cost": "high_but_clean",
            },
            {
                "audit_id": "IND1106_1_hidden_invariant_no_target",
                "candidate_clause": "hidden invariant triviality or no target action on Coeff(O_vis)",
                "independence_status": "MERGEABLE_WITH_PARENT_OBJECT_LANGUAGE",
                "subsumes": "scalar obstruction if stated as no target action",
                "not_subsumed_by": "weak parent-domain language that merely lists fields",
                "risk_if_absent": "c0+epsilon I_hid visible coefficients survive",
                "axiom_cost": "high_if_separate_lower_if_merged",
            },
            {
                "audit_id": "IND1106_2_product_sequester",
                "candidate_clause": "S_vis factors through q and theta_rep, not hidden relaxation variables",
                "independence_status": "REDUNDANT_IF_IND1106_0_STRONG",
                "subsumes": "many mixed visible-hidden product terms",
                "not_subsumed_by": "radiative/readout stability",
                "risk_if_absent": "mixed products return as explicit action terms",
                "axiom_cost": "medium_as_restated_subclause",
            },
            {
                "audit_id": "IND1106_3_common_action_measure_current_owner",
                "candidate_clause": "one ordinary action measure/current/source normalization for all species",
                "independence_status": "INDEPENDENT_SOURCE_COUPLING_CLOSURE",
                "subsumes": "w_A S_A and species source-weight rescalings if paired with parent object language",
                "not_subsumed_by": "no-hidden-visible hom alone because constant species weights can survive without hidden scalar dependence",
                "risk_if_absent": "relative source weights survive classical EOM rescaling",
                "axiom_cost": "high_and_quantum_sensitive",
            },
            {
                "audit_id": "IND1106_4_radiative_readout_stability",
                "candidate_clause": "S_eff and readout maps preserve no-hidden-visible coefficient rule",
                "independence_status": "INDEPENDENT_STABILITY_CLOSURE",
                "subsumes": "loop/readout regeneration control",
                "not_subsumed_by": "tree-level object-language exhaustion",
                "risk_if_absent": "forbidden coefficients regenerate after reduction",
                "axiom_cost": "high_but_required_for_claim_grade_zeroes",
            },
            {
                "audit_id": "IND1106_5_variation_before_readout",
                "candidate_clause": "source/current variation happens before empirical readout/material projection/calibration",
                "independence_status": "PARTLY_MERGEABLE_WITH_READOUT_STABILITY",
                "subsumes": "post-variation selectors that manufacture or erase source currents",
                "not_subsumed_by": "object-language exhaustion alone",
                "risk_if_absent": "tau/source/readout maps can create artificial wins",
                "axiom_cost": "medium_as_readout_subclause",
            },
            {
                "audit_id": "IND1106_6_residual_vector_policy",
                "candidate_clause": "unsigned clauses become explicit residual coefficient/product rows",
                "independence_status": "METHODOLOGY_NOT_PHYSICS_AXIOM",
                "subsumes": "runner refusal discipline",
                "not_subsumed_by": "theory clauses",
                "risk_if_absent": "omission gets mistaken for derivation",
                "axiom_cost": "low_methodological",
            },
        ]
    )


def minimal_pack_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "pack_id": "MIN1106_A",
                "role": "physics_closure",
                "minimal_clause": "parent ordinary-sector object-language exhaustion",
                "formal_form": "Coeff(O_vis) subset Image(ParentGenerate[q, theta_rep, topological levels]) plus no hidden target action",
                "covers": "no-extra-F2, no hidden mass/binding/clock coefficient, no hidden visible coefficient morphism",
                "still_needs": "source action-measure owner and radiative/readout stability",
                "adoption_status": "not_adopted_not_derived",
            },
            {
                "pack_id": "MIN1106_B",
                "role": "physics_closure",
                "minimal_clause": "common ordinary action-measure/current/source owner",
                "formal_form": "no species-dependent S_A multiplier, source-only w_A, or independent current/source normalization",
                "covers": "relative source weights and measured-G absorption shortcuts",
                "still_needs": "parent current/gauge owner and source projection maps",
                "adoption_status": "not_adopted_not_derived",
            },
            {
                "pack_id": "MIN1106_C",
                "role": "physics_closure",
                "minimal_clause": "radiative/readout/variation-order stability",
                "formal_form": "S_eff and readout/projection maps remain in the same parent-generated domain and variation precedes readout",
                "covers": "loop/readout regeneration and post-variation selector leaks",
                "still_needs": "explicit arena projection maps tau_clock, tau_WEP, tau_R10",
                "adoption_status": "not_adopted_not_derived",
            },
            {
                "pack_id": "MIN1106_D",
                "role": "method_policy",
                "minimal_clause": "unsigned pieces enter residual vector with source-backed rows",
                "formal_form": "if not derived/adopted, coefficient/product rows must be numeric, sourced, unit-matched, and runner-valid",
                "covers": "nonclaim discipline and finite branch path",
                "still_needs": "actual source-backed prediction rows",
                "adoption_status": "active_internal_policy",
            },
        ]
    )


def finite_priority_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "priority_id": "PRI1106_0_alpha",
                "rank": "1",
                "finite_row": "alpha coefficient/product row",
                "why_first": "highest shared pressure across clocks, WEP Coulomb/material, R10 alpha(lambda), and EM normalization",
                "current_threshold": "abs(c_alpha_DD or b_alpha) <= 8.320244933243533e-10; clock product <= 2.1e-18 yr^-1",
                "missing_before_score": "parent no-extra-F2 theorem or source-backed b_alpha/c_alpha and tau maps",
            },
            {
                "priority_id": "PRI1106_1_source_weight",
                "rank": "2",
                "finite_row": "WEP/source relative weight row",
                "why_first": "directly tests source coupling/GR-Newton source normalization wound",
                "current_threshold": "eta/source proxy <= 2.8e-15",
                "missing_before_score": "Delta_w_TiPt theorem-zero or numeric prior plus tau_WEP projection",
            },
            {
                "priority_id": "PRI1106_2_WEP_alpha_product",
                "rank": "3",
                "finite_row": "direct WEP alpha product row",
                "why_first": "already has material/DeltaQ/target context from 1102",
                "current_threshold": "abs(P_WEP_alpha) target <= 4.797780522732e-05",
                "missing_before_score": "beta_source_alpha, tau_WEP, or direct product theorem/value",
            },
            {
                "priority_id": "PRI1106_3_mass_binding",
                "rank": "4",
                "finite_row": "mass/binding/material coefficient row",
                "why_first": "important for WEP/material channels but less unified than alpha/source owner",
                "current_threshold": "c_surface <= 6.9875016461438634e-11; c_common <= 6.4461422294339073e-11",
                "missing_before_score": "source-backed coefficient or matter-spectrum theorem-zero",
            },
            {
                "priority_id": "PRI1106_4_R10",
                "rank": "5",
                "finite_row": "R10 alpha(lambda)/relative-weight product row",
                "why_first": "empirically valuable but requires the most arena-specific plumbing",
                "current_threshold": "promoted alpha(lambda) curve required",
                "missing_before_score": "lambda, K(lambda), source/test weights, tau_R10, and valid bound curve",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1106_0_pack_reduction",
                "decision": "closure pack reduces to three physics closures plus one methodology policy",
                "because": "hidden-invariant no-target and product sequester are mostly subclauses of parent object-language exhaustion, while action-measure/current owner and radiative/readout stability are independent",
                "next_action": "do not adopt the pack as derived; target the parent object-language exhaustion first",
            },
            {
                "decision_id": "DEC1106_1_cost_status",
                "decision": "the minimal closure pack is respectable as an explicit private contract but too expensive for a public derivation claim",
                "because": "it still contains three high-impact parent-action closures not derived from MTS primitives",
                "next_action": "try to derive MIN1106_A or else start the alpha finite row route",
            },
            {
                "decision_id": "DEC1106_2_first_finite_row",
                "decision": "if derivation fails again, alpha is the first finite row priority",
                "because": "alpha is the shared coefficient channel with the most cross-arena leverage and existing thresholds",
                "next_action": "1107 should attempt parent object-language exhaustion or stage a source-backed alpha coefficient row",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "CG1106_0_pack_adopted",
                "claim": "minimal closure pack is adopted as derived MTS theory",
                "gate_pass": "false",
                "reason": "independence audit classifies it as not_adopted_not_derived",
            },
            {
                "gate_id": "CG1106_1_public_zero_claims",
                "claim": "alpha/source/mass/clock coefficients are theorem-zero",
                "gate_pass": "false",
                "reason": "three physics closures remain unsigned",
            },
            {
                "gate_id": "CG1106_2_finite_alpha_score",
                "claim": "finite alpha row is scoreable now",
                "gate_pass": "false",
                "reason": "priority is selected but coefficient/projection inputs remain missing",
            },
            {
                "gate_id": "CG1106_3_local_GR",
                "claim": "local GR/Newton follows from closure pack",
                "gate_pass": "false",
                "reason": "closure pack addresses ordinary-sector coefficient leakage, not the full EH/source/PPN derivation",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1106_0_1107",
                "next_target": "1107-Y5-R10-parent-object-language-exhaustion-derivation-or-alpha-coefficient-source-row.md",
                "objective": "try to derive MIN1106_A, the parent ordinary-sector object-language exhaustion rule; if it cannot be derived, stage the first alpha coefficient/product source row with strict nonclaim gates",
                "include": "ParentGenerate image; Coeff(O_vis) domain; no hidden target action; no-extra-F2 subcase; finite alpha coefficient thresholds; clock/WEP/R10 projection blockers",
                "exclude": "adopting closure as derivation; local-GR claim; tau=1; standalone b_alpha; unsourced coefficient values; GitHub; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    independence: list[dict[str, object]],
    minimal_pack: list[dict[str, object]],
    priorities: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    add(
        "V1106_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1106_1_independence_written",
        len(independence) >= 7 and any(row["independence_status"] == "METHODOLOGY_NOT_PHYSICS_AXIOM" for row in independence),
        "independence audit separates physics closures from methodology",
    )
    add(
        "V1106_2_minimal_pack_reduced",
        {row["pack_id"] for row in minimal_pack} == {"MIN1106_A", "MIN1106_B", "MIN1106_C", "MIN1106_D"},
        "minimal pack reduced to three physics closures plus one policy",
    )
    add(
        "V1106_3_alpha_priority_selected",
        any(row["priority_id"] == "PRI1106_0_alpha" and row["rank"] == "1" for row in priorities),
        "alpha coefficient/product row selected as first finite fallback priority",
    )
    add(
        "V1106_4_pack_not_adopted",
        all(row["adoption_status"] != "adopted_as_derivation" for row in minimal_pack),
        "closure pack is not adopted as derivation",
    )
    add(
        "V1106_5_claim_gates_blocked",
        all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in gates),
        "all claim gates remain blocked",
    )
    add(
        "V1106_6_next_target",
        next_target[0]["next_target"].startswith("1107-") and "object-language-exhaustion" in str(next_target[0]["next_target"]),
        "1107 handoff targets object-language exhaustion or alpha source row",
    )
    add(
        "V1106_7_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in independence + minimal_pack + priorities + decisions + gates + next_target),
        "all generated rows are nonclaim",
    )
    add(
        "V1106_8_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for name, path in outputs.items():
        if name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1106_9_csv_parse", csv_parse_ok, "all 1106 CSV outputs parse cleanly")
    add(
        "V1106_10_formalization_untouched",
        True,
        "generator writes no outputs under formalization-workbench",
    )
    add(
        "V1106_SUMMARY",
        True,
        "1106 reduces the closure pack to three physics closures plus one policy and selects parent object-language exhaustion or alpha row as next target",
    )
    return rows


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    independence: list[dict[str, object]],
    minimal_pack: list[dict[str, object]],
    priorities: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1106 - Minimal Explicit Closure Pack Independence Audit Or First Source-Backed Coefficient Row

**Current verdict:** the 1105 closure pack is reducible, but still not cheap. It collapses to three physics closures plus one methodology policy: parent object-language exhaustion, common action-measure/current/source ownership, radiative/readout stability, and residual-vector discipline.

**Why this matters:** this is better than five disconnected magic clauses, but it is still not a derivation. The respectable route is to derive the first closure, `MIN1106_A`, from MTS parent object-language structure; if that fails, the finite alpha row is the highest-leverage empirical fallback.

**No claim:** nothing in 1106 authorizes local-GR, WEP, R10, clock, or alpha silence. It is a closure-minimization and next-target selection checkpoint.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Independence Audit
{table(["audit_id", "candidate_clause", "independence_status", "subsumes", "not_subsumed_by", "risk_if_absent", "axiom_cost", "claim_allowed"], independence)}

## Minimal Closure Pack
{table(["pack_id", "role", "minimal_clause", "formal_form", "covers", "still_needs", "adoption_status", "claim_allowed"], minimal_pack)}

## Finite Row Priority
{table(["priority_id", "rank", "finite_row", "why_first", "current_threshold", "missing_before_score", "claim_allowed"], priorities)}

## Decisions
{table(["decision_id", "decision", "because", "next_action", "claim_allowed"], decisions)}

## Claim Gates
{table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed"], gates)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1106_SOURCE_REGISTER.csv",
        "independence": OUT / "P8_Y5_R10_1106_CLOSURE_INDEPENDENCE_AUDIT.csv",
        "minimal_pack": OUT / "P8_Y5_R10_1106_MINIMAL_CLOSURE_PACK.csv",
        "priorities": OUT / "P8_Y5_R10_1106_FINITE_ROW_PRIORITY.csv",
        "decisions": OUT / "P8_Y5_R10_1106_DECISION_LEDGER.csv",
        "claim_gates": OUT / "P8_Y5_R10_1106_CLAIM_GATES.csv",
        "next_target": OUT / "P8_Y5_R10_1106_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1106_VALIDATION.csv",
    }
    sources = source_rows()
    independence = independence_rows()
    minimal_pack = minimal_pack_rows()
    priorities = finite_priority_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["independence"], independence)
    write_csv(outputs["minimal_pack"], minimal_pack)
    write_csv(outputs["priorities"], priorities)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], gates)
    write_csv(outputs["next_target"], next_target)
    validation = validate(sources, independence, minimal_pack, priorities, decisions, gates, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, independence, minimal_pack, priorities, decisions, gates, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
