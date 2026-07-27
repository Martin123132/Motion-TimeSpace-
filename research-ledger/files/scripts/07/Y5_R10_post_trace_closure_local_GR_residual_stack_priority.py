from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_907_post_trace_closure_local_GR_residual_stack_ranked_projector_Bianchi_gate_selected_nonclaim"
CLAIM_CEILING = "local_GR_residual_priority_only_no_EH_no_Newton_no_PPN_no_R10_claim"
NEXT_TARGET = "908-Y5-R10-projector-stress-Bianchi-fate-or-retained-PPN-vector.md"

SOURCE_SPECS = [
    {
        "source_id": "906_doc",
        "path": ROOT / "906-Y5-R10-trace-projector-Htr-parent-domain-or-closure-only.md",
        "needle": "finite trace `alpha_tr(lambda_tr)` branch is demoted to explicit closure-only",
        "role": "post-trace closure handoff",
    },
    {
        "source_id": "906_validation",
        "path": OUT / "P8_Y5_BRR545_906_VALIDATION.csv",
        "needle": "V906_12_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "906_closure_register",
        "path": OUT / "P8_Y5_R10_906_CLOSURE_ONLY_DEMOTION_REGISTER.csv",
        "needle": "CDR906_4_local_GR_policy",
        "role": "trace branch no longer claimable local-GR evidence",
    },
    {
        "source_id": "654_local_gr_spine",
        "path": OUT / "P8_Y5_R10_654_LOCAL_GR_SPINE.csv",
        "needle": "LGS654_1_EH_operator_selection",
        "role": "broad local-GR spine and EH/source/PPN blockers",
    },
    {
        "source_id": "654_promotion_gates",
        "path": OUT / "P8_Y5_R10_654_PROMOTION_GATES.csv",
        "needle": "PG654_1_EH_operator_selected",
        "role": "local-GR promotion gates remain failed",
    },
    {
        "source_id": "868_reduction_chain",
        "path": OUT / "P8_Y5_R10_868_LOCAL_GR_REDUCTION_CHAIN.csv",
        "needle": "GR868_3_projector_stress",
        "role": "post-endpoint local-GR reduction chain",
    },
    {
        "source_id": "868_blocker_audit",
        "path": OUT / "P8_Y5_R10_868_LOCAL_GR_BLOCKER_AUDIT.csv",
        "needle": "BL868_2_projector_stress",
        "role": "local-GR blocker audit",
    },
    {
        "source_id": "868_newton_source",
        "path": OUT / "P8_Y5_R10_868_NEWTON_SOURCE_NORMALIZATION_CONTRACT.csv",
        "needle": "NS868_1_measured_GM",
        "role": "Newton/source-normalization blocker",
    },
    {
        "source_id": "868_ppn_vector",
        "path": OUT / "P8_Y5_R10_868_PPN_VECTOR_LEDGER.csv",
        "needle": "PV868_3_q_loc",
        "role": "PPN/q_loc residual ledger",
    },
    {
        "source_id": "869_qloc_decomposition",
        "path": OUT / "P8_Y5_R10_869_QLOC_IDENTITY_DECOMPOSITION.csv",
        "needle": "QI869_3_projector_channel",
        "role": "q_loc residual channel decomposition",
    },
    {
        "source_id": "869_zero_theorem",
        "path": OUT / "P8_Y5_R10_869_ZERO_THEOREM_ATTEMPT.csv",
        "needle": "ZT869_4_projector_stress_fate",
        "role": "q_loc zero theorem blockers",
    },
    {
        "source_id": "870_nohair",
        "path": OUT / "P8_Y5_R10_870_JTRACE_NOHAIR_PROOF_ATTEMPT.csv",
        "needle": "NH870_5_nohair_verdict",
        "role": "trace no-hair branch now quarantined rather than promoted",
    },
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def stringify(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return "" if value is None else str(value)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: stringify(row.get(field, "")) for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needle(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [stringify(row.get(field, "")).replace("\n", " ").replace("|", "/") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": path,
                "exists": path.exists(),
                "needle_check": "pass" if has_needle(path, str(spec["needle"])) else "fail",
                "role": spec["role"],
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "ranked the post-trace local-GR residual stack and selected projector-stress/Bianchi fate as the next derivable gate",
            "best_partial_result": "finite trace alpha is quarantined; the next root local-GR blocker is whether projector/N5 stress is zero, gauge, boundary-conserved, or a retained PPN residual",
            "hard_blockers": "EH operator selection, projector stress fate, Bianchi conservation, source-normalized GM, matter descent/no-marker, boundary no-flux, and full PPN vector",
            "what_is_not_claimed": "local GR, Newtonian limit, PPN pass, source-normalization pass, R10 pass, or trace-zero theorem",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def post_trace_status_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "PTS907_0_trace_alpha",
            "finite trace alpha",
            "closure_only",
            "906 demoted it because P_tr/H_tr was not parent-owned",
            "do not use as local-GR or R10 evidence",
        ),
        (
            "PTS907_1_trace_no_pole",
            "trace no-pole/Q_tr-zero route",
            "conditional_watch_only",
            "rank-zero/source-cokernel/no-tail premises remain unsigned",
            "may reopen only with parent signatures",
        ),
        (
            "PTS907_2_R10",
            "R10 short-range test",
            "blocked_downstream",
            "no valid MTS alpha(lambda) row exists",
            "defer scoring; keep runner refusal rows only",
        ),
        (
            "PTS907_3_local_GR_policy",
            "local GR/Newton",
            "still_open",
            "trace quarantine removes one contaminating branch but does not prove EH/source/PPN",
            "continue residual stack derivation",
        ),
    ]
    return [
        {
            "status_id": status_id,
            "item": item,
            "post_906_status": status,
            "basis": basis,
            "policy": policy,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for status_id, item, status, basis, policy in rows
    ]


def residual_stack_rollup_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "LGR907_0_EH_operator",
            "EH operator selection",
            "local metric variation must reduce to EH plus allowed Lambda/boundary terms",
            "not_derived",
            "highest",
            "without this the exterior field equation may simply not be GR",
        ),
        (
            "LGR907_1_projector_Bianchi",
            "projector/N5 stress fate",
            "T_projector must be zero, pure gauge, boundary-only conserved, or retained explicitly",
            "open_hard",
            "highest",
            "dropping this would fake an EH exterior and break Bianchi safety",
        ),
        (
            "LGR907_2_source_GM",
            "source normalization / measured GM",
            "G_eff M_eff must be constant, universal, range-independent, species-independent",
            "not_parent_derived",
            "high",
            "Newtonian mechanics needs source normalization, not just EH-shaped algebra",
        ),
        (
            "LGR907_3_matter_descent",
            "matter/coframe/no-marker descent",
            "ordinary matter/clocks/rulers factor through one observed local quotient/coframe",
            "conditional_chain_rule_only",
            "high",
            "WEP/clock/source charge silence remains closure otherwise",
        ),
        (
            "LGR907_4_boundary_no_flux",
            "boundary/no-flux/no-tail",
            "worldtube/linking-sphere/boundary terms have no local mass/PPN flux",
            "open",
            "medium_high",
            "hidden boundary charge can contaminate GM and PPN",
        ),
        (
            "LGR907_5_PPN_vector",
            "PPN residual vector",
            "gamma-1, beta-1, alpha_i, xi, Gdot/G, clock/WEP residuals are zero or bounded",
            "not_ready",
            "medium_high",
            "requires EH/source/projector gates first to avoid meaningless coefficients",
        ),
        (
            "LGR907_6_R10",
            "R10 finite-range branch",
            "finite trace alpha has no valid theory row; other finite modes require source rows",
            "blocked",
            "lower_now",
            "important empirically, but not the next derivation gate",
        ),
    ]
    return [
        {
            "rollup_id": rollup_id,
            "residual_channel": channel,
            "required_condition": condition,
            "current_status": status,
            "local_GR_priority": priority,
            "why_it_matters": why,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for rollup_id, channel, condition, status, priority, why in rows
    ]


def qloc_channel_rerank_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            1,
            "q_P^nu projector/Bianchi channel",
            "P_loc(F_P^nu) or P_loc(nabla_mu T_projector^{mu nu})",
            "open_hard",
            "derive zero/gauge/boundary-conserved fate or retain c_P PPN vector",
            "selected_now",
        ),
        (
            2,
            "q_S^nu source-normalization channel",
            "source-normalization drift in Gamma_eff/K_hat and measured GM map",
            "open",
            "derive universal constant GM theorem or retain c_S delta_G/Gdot/WEP/fifth-force rows",
            "next_after_projector",
        ),
        (
            3,
            "q_e^nu matter/coframe channel",
            "P_loc Pi_I^matter",
            "conditional_shape_unsigned",
            "prove matter descent/no-marker or retain c_e WEP/clock rows",
            "parallel_after_projector",
        ),
        (
            4,
            "q_T^nu trace endpoint channel",
            "P_loc J_trace or boundary exact trace current",
            "closure_only_after_906",
            "do not use as evidence unless reopened by parent signatures",
            "quarantined",
        ),
    ]
    return [
        {
            "rank": rank,
            "channel": channel,
            "schematic_source": source,
            "current_status": status,
            "next_action": action,
            "decision": decision,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for rank, channel, source, status, action, decision in rows
    ]


def priority_stack_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "PRI907_0_projector_Bianchi",
            1,
            "projector-stress/Bianchi fate",
            "this is the least-cheaty route to EH exterior: either T_projector is zero/gauge/boundary-conserved or it becomes an explicit PPN residual",
            10,
            10,
            NEXT_TARGET,
            True,
        ),
        (
            "PRI907_1_source_GM",
            2,
            "source-normalized Newtonian limit",
            "after EH/projector fate, Newton requires constant universal measured GM and no hidden source drift",
            10,
            9,
            "909-Y5-R10-source-normalized-GM-theorem-or-deltaG-residual-vector.md",
            False,
        ),
        (
            "PRI907_2_matter_descent",
            3,
            "matter/coframe/no-marker descent",
            "needed for WEP/clock/source universality and one observed local matter frame",
            9,
            8,
            "910-Y5-R10-matter-coframe-descent-or-WEP-clock-residual-vector.md",
            False,
        ),
        (
            "PRI907_3_boundary_no_flux",
            4,
            "boundary no-flux/no-tail",
            "prevents hidden boundary charge from contaminating GM/PPN after the projector route",
            8,
            7,
            "after projector/source gates",
            False,
        ),
        (
            "PRI907_4_PPN_vector",
            5,
            "PPN residual vector scoring",
            "necessary for claims but should not be run before EH/source/projector coefficients are defined",
            9,
            5,
            "after operator/source gates",
            False,
        ),
        (
            "PRI907_5_R10_bound_curve",
            6,
            "R10/digitized short-range curve",
            "empirical plumbing is useful but cannot replace missing local-GR operator/source derivations",
            6,
            3,
            "defer until a valid theory row exists",
            False,
        ),
    ]
    return [
        {
            "priority_id": priority_id,
            "rank": rank,
            "target": target,
            "why_this_order": why,
            "local_GR_impact_0_10": impact,
            "dependency_weight_0_10": dep,
            "next_target": next_target,
            "selected_now": selected,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for priority_id, rank, target, why, impact, dep, next_target, selected in rows
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    gates = [
        ("CGATE907_0_trace_alpha", "finite trace alpha/R10 branch", "blocked: closure-only after 906"),
        ("CGATE907_1_EH_operator", "local EH/GR field equation", "blocked: operator/projector stress fate not derived"),
        ("CGATE907_2_Newton", "Newtonian mechanics/source normalization", "blocked: measured GM universality not parent-derived"),
        ("CGATE907_3_WEP_clock", "WEP/clock matter-frame pass", "blocked: matter/coframe/no-marker descent not signed"),
        ("CGATE907_4_PPN", "PPN local-GR pass", "blocked: residual vector not defined by source-backed coefficients"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "claim_allowed": False,
            "blocker": blocker,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for gate_id, claim, blocker in gates
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "decide the local projector/N5 stress fate: zero, gauge, boundary-conserved, or retained as an explicit PPN/source residual vector",
            "include": "parent variation, Bianchi identity, T_projector conservation, EH exterior compatibility, retained c_P residual rows, PPN gamma/beta/slip links",
            "exclude": "trace finite-alpha evidence, R10 curve scoring, local-GR claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_906_clean() -> bool:
    rows = read_csv(OUT / "P8_Y5_BRR545_906_VALIDATION.csv")
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > CUTOFF:
            count += 1
    return count


def all_generated_rows_nonclaim(row_groups: list[list[dict[str, object]]]) -> bool:
    for group in row_groups:
        for row in group:
            if "valid_for_claim" in row and stringify(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and stringify(row["claim_allowed"]).lower() != "false":
                return False
    return True


def validation_rows(
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    trace_rows_: list[dict[str, object]],
    rollup_rows_: list[dict[str, object]],
    qloc_rows_: list[dict[str, object]],
    priority_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        summary_rows_,
        trace_rows_,
        rollup_rows_,
        qloc_rows_,
        priority_rows_,
        claim_rows_,
        next_rows_,
    ]
    checks = [
        {
            "check_id": "V907_0_sources_exist_and_needles",
            "result": "pass"
            if all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows_)
            else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V907_1_prior_906_clean",
            "result": "pass" if prior_906_clean() else "fail",
            "detail": "P8_Y5_BRR545_906_VALIDATION.csv clean",
        },
        {
            "check_id": "V907_2_trace_quarantined",
            "result": "pass"
            if any(row["item"] == "finite trace alpha" and row["post_906_status"] == "closure_only" for row in trace_rows_)
            else "fail",
            "detail": "finite trace alpha not used as evidence",
        },
        {
            "check_id": "V907_3_projector_selected_top_priority",
            "result": "pass"
            if any(row["rank"] == 1 and row["selected_now"] is True and "projector" in stringify(row["target"]) for row in priority_rows_)
            else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V907_4_qloc_trace_not_selected",
            "result": "pass"
            if any(row["channel"].startswith("q_T") and row["decision"] == "quarantined" for row in qloc_rows_)
            else "fail",
            "detail": "trace q_loc channel quarantined after 906",
        },
        {
            "check_id": "V907_5_claim_gates_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in claim_rows_) else "fail",
            "detail": "all local-GR/Newton/PPN claims blocked",
        },
        {
            "check_id": "V907_6_all_generated_rows_nonclaim",
            "result": "pass" if all_generated_rows_nonclaim(row_groups) else "fail",
            "detail": "all generated rows keep valid_for_claim/claim_allowed false",
        },
        {
            "check_id": "V907_7_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V907_8_next_target_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V907_9_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    for row in checks:
        row["generated_utc"] = generated_utc
    return checks


def write_markdown(
    path: Path,
    generated_utc: str,
    summary_rows_: list[dict[str, object]],
    source_rows_: list[dict[str, object]],
    trace_rows_: list[dict[str, object]],
    rollup_rows_: list[dict[str, object]],
    qloc_rows_: list[dict[str, object]],
    priority_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 907 - Y5/R10 Post Trace Closure Local GR Residual Stack Priority

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **after quarantining finite trace alpha, the next derivable local-GR gate is projector/N5 stress fate under Bianchi safety.** The selected target is not a claim that local GR is derived. It is the least-cheaty next door: either the projector stress is zero/gauge/boundary-conserved, or it becomes an explicit retained PPN/source residual.

## Exact 907 Finding
The trace coupling branch was absorbing attention because it had a clean R10 shape. After 906, that shape is closure-only. The remaining GR/Newton problem is upstream of R10: the local exterior operator and source exchange must be fixed. The `q_loc^nu` rerank therefore puts the projector/Bianchi channel first, then source-normalized GM, then matter/coframe descent.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## Post-Trace Status
{md_table(trace_rows_)}

## Local-GR Residual Stack Rollup
{md_table(rollup_rows_)}

## q_loc Channel Rerank
{md_table(qloc_rows_)}

## Priority Stack
{md_table(priority_rows_)}

## Claim Gate
{md_table(claim_rows_)}

## Next Target
{md_table(next_rows_)}

## Validation
{md_table(validation_rows_)}
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    source_rows_ = source_register_rows(generated_utc)
    summary_rows_ = nonclaim_summary_rows(generated_utc)
    trace_rows_ = post_trace_status_rows(generated_utc)
    rollup_rows_ = residual_stack_rollup_rows(generated_utc)
    qloc_rows_ = qloc_channel_rerank_rows(generated_utc)
    priority_rows_ = priority_stack_rows(generated_utc)
    claim_rows_ = claim_gate_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        trace_rows_,
        rollup_rows_,
        qloc_rows_,
        priority_rows_,
        claim_rows_,
        next_rows_,
    )

    outputs = {
        "P8_Y5_R10_907_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_907_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_R10_907_POST_TRACE_STATUS.csv": trace_rows_,
        "P8_Y5_R10_907_LOCAL_GR_RESIDUAL_STACK_ROLLUP.csv": rollup_rows_,
        "P8_Y5_R10_907_QLOC_CHANNEL_RERANK.csv": qloc_rows_,
        "P8_Y5_R10_907_PRIORITY_STACK.csv": priority_rows_,
        "P8_Y5_R10_907_CLAIM_GATE.csv": claim_rows_,
        "P8_Y5_R10_907_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_BRR545_907_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "907-Y5-R10-post-trace-closure-local-GR-residual-stack-priority.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows_,
        source_rows_,
        trace_rows_,
        rollup_rows_,
        qloc_rows_,
        priority_rows_,
        claim_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_907_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
