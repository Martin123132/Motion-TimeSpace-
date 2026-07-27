from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "805-Y5-R10-metric-response-kernel-theorem-or-source-lift-action-block-gate.md"
NEXT_TARGET = "806-Y5-R10-transition-source-lift-action-block-gate.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_805_SOURCE_REGISTER.csv"
KERNEL_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_805_KERNEL_THEOREM_CONTRACT.csv"
DERIVATION_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_805_KERNEL_DERIVATION_AUDIT.csv"
SOURCE_LIFT_REQUIREMENTS_PATH = RESIDUALS / "P8_Y5_R10_805_SOURCE_LIFT_ACTION_BLOCK_REQUIREMENTS.csv"
LOCAL_RESPONSE_DECISION_PATH = RESIDUALS / "P8_Y5_R10_805_LOCAL_RESPONSE_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_805_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_805_VALIDATION.csv"

STATUS = "Y5_R10_805_metric_response_kernel_conditional_theorem_source_lift_missing_nonclaim"
CLAIM_CEILING = "conditional_kernel_contract_only_no_parent_Sigma_metric_no_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    KERNEL_CONTRACT_PATH,
    DERIVATION_AUDIT_PATH,
    SOURCE_LIFT_REQUIREMENTS_PATH,
    LOCAL_RESPONSE_DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "804_doc",
        "path": POST_CHECKPOINT / "804-Y5-R10-conservation-owned-quarantine-equations-or-parent-projector-origin.md",
        "needles": ["RK804_1_orthogonality", "RK804_2_matter_preservation", "D804_2_next_route"],
        "role": "immediate kernel requirements inherited from 804",
    },
    {
        "source_id": "804_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_804_VALIDATION.csv",
        "needles": ["V804_4_quarantine_equations_explicit,pass", "V804_8_next_target_selected,pass"],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "spine_metric_kernel",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": [
            "metric_response_kernel_formal_only_source_lift_missing_parent_theorem_not_derived",
            "Sigma_metric[q_tr]",
            "P_metric,loc remains closure-only",
        ],
        "role": "spine metric-kernel result",
    },
    {
        "source_id": "spine_transition_source_lift",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": [
            "transition_source_lift_action_block_not_derived_minimal_contract_required",
            "delta S_tr/delta g_loc",
            "metric-null transition action/source-lift block",
        ],
        "role": "spine source-lift/action-block target",
    },
    {
        "source_id": "red_metric_kernel",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": [
            "metric_response_kernel_formal_only_source_lift_missing_parent_theorem_not_derived.",
            "Sigma_metric[q_tr]",
            "source-lift missing; kernel theorem not derived.",
        ],
        "role": "red-team metric-kernel exposure",
    },
    {
        "source_id": "red_transition_source_lift",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": [
            "transition_source_lift_action_block_not_derived_minimal_contract_required.",
            "Sigma_metric[q_tr]=0 cannot be set",
            "action block missing; contract required.",
        ],
        "role": "red-team action-block exposure",
    },
    {
        "source_id": "equation_register_local_current",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": ["q_loc^nu = P_loc q_tr^nu", "nabla_mu K_tr,loc^{mu nu} = -q_loc^nu", "Kbar_MTS,00 ="],
        "role": "registered local current and PPN-risk equations",
    },
]


def utc_stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def needle_status(path: Path, needles: list[str]) -> str:
    if not path.exists():
        return "missing_file"
    source_text = read_text(path)
    missing_needles = [needle for needle in needles if needle not in source_text]
    if missing_needles:
        return "missing_needles:" + ";".join(missing_needles)
    return "pass"


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def validation_file_clean(check_number: int) -> tuple[bool, str]:
    validation_file = RESIDUALS / f"P8_Y5_BRR545_{check_number}_VALIDATION.csv"
    if not validation_file.exists():
        return False, f"missing={validation_file}"
    failures: list[str] = []
    with validation_file.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{validation_file.name} clean"


def formalization_change_count() -> int:
    if not FORMALIZATION.exists():
        return -1
    return sum(
        1
        for candidate_path in FORMALIZATION.rglob("*")
        if candidate_path.is_file() and datetime.fromtimestamp(candidate_path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        source_path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(source_path),
                "exists": str(source_path.exists()).lower(),
                "needle_check": needle_status(source_path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def kernel_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "KC805_0_parent_lift",
            "statement": "A parent-derived tensor source lift Sigma_metric[q] must map transition currents into the metric variation channel.",
            "equation": "delta S_tr / delta g_loc^{mu nu} := -1/2 sqrt(-g) Sigma_metric[q_tr]_{mu nu}",
            "claim_status": "missing_parent_object",
            "why_it_matters": "q_tr^nu is a vector current; the metric responds to tensor source classes, not to labels.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "KC805_1_response_kernel",
            "statement": "If the metric Hessian E_g and physical projection Pi_phys are defined, the local response is R_loc q = Pi_phys E_g^{-1} Sigma_metric[q].",
            "equation": "R_loc q := Pi_phys E_g^{-1} Sigma_metric[q]",
            "claim_status": "conditional_definition_only",
            "why_it_matters": "This makes the kernel a theorem target rather than a hand-picked projector.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "KC805_2_transition_nullity",
            "statement": "The transition branch is locally safe only if the parent lift sends q_tr into the metric-null class.",
            "equation": "Pi_phys E_g^{-1} Sigma_metric[q_tr] = 0",
            "claim_status": "not_proven",
            "why_it_matters": "This is the exact replacement for smuggling in P_metric,loc[K_own]=0.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "KC805_3_matter_preservation",
            "statement": "Ordinary matter must remain visible to the same metric Hessian.",
            "equation": "Pi_phys E_g^{-1} Sigma_metric[q_matter] = Pi_phys E_g^{-1} T_matter",
            "claim_status": "required_not_proven",
            "why_it_matters": "A kernel that kills all sources also kills Newton/GR, so it is not a GR limit.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "KC805_4_bianchi_compatibility",
            "statement": "The lift must be divergence-compatible with the owned exchange tensor and the metric equations.",
            "equation": "nabla_mu Sigma_metric[q]^{mu nu} + q_own^nu = 0 modulo parent Noether identities",
            "claim_status": "required_not_proven",
            "why_it_matters": "Conservation bookkeeping alone does not prove metric invisibility.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def derivation_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "DA805_0_formal_kernel_possible",
            "attempt": "Define R_loc from a metric Hessian and a source lift rather than a sector label.",
            "result": "conditional_pass",
            "obstruction": "E_g and Sigma_metric[q_tr] are not parent-signed in the current local branch.",
            "decision": "keep_as_theorem_contract",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "DA805_1_direct_label_projector",
            "attempt": "Set R_loc q_tr=0 because q_tr is the transition current.",
            "result": "rejected",
            "obstruction": "label routing is not a covariant parent theorem and does not preserve ordinary matter by itself.",
            "decision": "do_not_use_for_claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "DA805_2_conservation_only",
            "attempt": "Use nabla_mu K_own^{mu nu}=-q_own^nu to infer metric invisibility.",
            "result": "rejected",
            "obstruction": "a conserved or owned stress can still gravitate unless its metric variation is zero or pure gauge.",
            "decision": "requires_source_lift_action_block",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "DA805_3_null_source_condition",
            "attempt": "Prove Sigma_metric[q_tr]=0 or Pi_phys E_g^{-1} Sigma_metric[q_tr]=0 from parent symmetry.",
            "result": "not_derived",
            "obstruction": "no action block, Ward identity, boundary/topological theorem, doubled/open-system cancellation, or Palatini split is signed here.",
            "decision": "move_to_806_source_lift_action_block_gate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "DA805_4_matter_response",
            "attempt": "Verify ordinary matter remains GR/Newton while transition current is null.",
            "result": "not_derived",
            "obstruction": "the same parent kernel must kill q_tr but not T_matter; that separation is not proven.",
            "decision": "local_GR_claim_false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def source_lift_requirement_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "requirement_id": "SL805_0_action_block",
            "required_object": "S_tr[g_loc, Phi_tr, auxiliaries]",
            "must_show": "variation with respect to g_loc gives Sigma_metric[q_tr], and the claimed nullity follows from the parent structure",
            "allowed_routes": "boundary/topological term; internal metric-null sector; doubled/open-system cancellation; Palatini split; Ward identity",
            "status": "missing",
            "blocks": "derived_metric_kernel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "SL805_1_metric_nullity",
            "required_object": "Sigma_metric[q_tr] in ker(Pi_phys E_g^{-1})",
            "must_show": "transition source has no PPN/Newton metric response on local shells without deleting q_tr",
            "allowed_routes": "exact symmetry, pure gauge source, total derivative, canceling doubled partner, auxiliary constraint",
            "status": "missing",
            "blocks": "R_loc q_tr equals zero claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "SL805_2_matter_visibility",
            "required_object": "ordinary matter lift Sigma_metric[q_matter]=T_matter",
            "must_show": "the local source sector still reproduces Newton/GR and does not get projected away",
            "allowed_routes": "minimal coupling to g_loc plus parent theorem separating matter from transition exchange",
            "status": "missing",
            "blocks": "GR_limit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "SL805_3_noether_identity",
            "required_object": "parent Noether/Bianchi identity tying Sigma_metric and K_own",
            "must_show": "nabla_mu Sigma_metric^{mu nu} plus owned exchange closes without post-hoc current erasure",
            "allowed_routes": "diffeomorphism Ward identity, constrained auxiliary transport, covariant open-system balance",
            "status": "missing",
            "blocks": "conservation_to_metric_response_bridge",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def local_response_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D805_0_kernel_theorem",
            "question": "Can the metric-response kernel theorem be written exactly?",
            "answer": "Yes, conditionally: R_loc q = Pi_phys E_g^{-1} Sigma_metric[q].",
            "status": "conditional_contract_written",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D805_1_source_lift",
            "question": "Is Sigma_metric[q_tr] derived from the current parent route?",
            "answer": "No. The exact tensor lift and action block are missing.",
            "status": "source_lift_missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D805_2_matter_preservation",
            "question": "Can the kernel kill transition exchange while preserving ordinary matter GR/Newton?",
            "answer": "Not yet. This must be derived from the same parent action or Ward identity.",
            "status": "matter_response_not_proven",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D805_3_claim_status",
            "question": "Can local GR/Newton be claimed from 805?",
            "answer": "No. 805 identifies the exact missing object; it does not derive it.",
            "status": "local_GR_claim_false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_improved": "The metric-response kernel is now an exact conditional theorem target, not a vague projector.",
            "what_blocks_claim": "The parent source lift Sigma_metric[q_tr], metric-null action block, and matter-response preservation theorem are missing.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_outputs_scoped() -> bool:
    post_root = POST_CHECKPOINT.resolve()
    return all(path.resolve().is_relative_to(post_root) for path in OUTPUT_PATHS)


def all_rows_nonclaim(row_groups: list[list[dict[str, object]]]) -> bool:
    for row_group in row_groups:
        for row in row_group:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                return False
    return True


def validation_rows(
    sources: list[dict[str, object]],
    contracts: list[dict[str, object]],
    audits: list[dict[str, object]],
    requirements: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in sources)
    prior_ok, prior_detail = validation_file_clean(804)
    row_groups = [sources, contracts, audits, requirements, decisions, summary]
    nonclaim_ok = all_rows_nonclaim(row_groups)
    formalization_count = formalization_change_count()
    contract_explicit = any("Sigma_metric[q]" in row["statement"] or "R_loc q" in row["statement"] for row in contracts)
    conditional_only = any(row["result"] == "conditional_pass" for row in audits) and any(row["result"] == "not_derived" for row in audits)
    source_missing = any(row["status"] == "source_lift_missing" for row in decisions)
    matter_required = any(row["requirement_id"] == "SL805_2_matter_visibility" for row in requirements)
    local_false = any(row["status"] == "local_GR_claim_false" for row in decisions)
    next_selected = all(row["next_target"] == NEXT_TARGET for row in decisions)
    return [
        {"check_id": "V805_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V805_1_prior_804_clean", "result": "pass" if prior_ok else "fail", "detail": prior_detail},
        {"check_id": "V805_2_outputs_scoped", "result": "pass" if all_outputs_scoped() else "fail", "detail": str(POST_CHECKPOINT)},
        {"check_id": "V805_3_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V805_4_kernel_contract_explicit", "result": "pass" if contract_explicit else "fail", "detail": "R_loc q and Sigma_metric[q] contract written"},
        {"check_id": "V805_5_conditional_only_not_derived", "result": "pass" if conditional_only else "fail", "detail": "formal theorem target exists but source lift remains missing"},
        {"check_id": "V805_6_source_lift_missing_recorded", "result": "pass" if source_missing else "fail", "detail": "Sigma_metric[q_tr] is not parent-derived"},
        {"check_id": "V805_7_matter_response_required", "result": "pass" if matter_required else "fail", "detail": "ordinary matter visibility gate present"},
        {"check_id": "V805_8_no_local_GR_claim", "result": "pass" if local_false else "fail", "detail": "derived GR/Newton remains blocked"},
        {"check_id": "V805_9_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V805_10_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V805_11_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def build_doc(
    generated_utc: str,
    sources: list[dict[str, object]],
    contracts: list[dict[str, object]],
    audits: list[dict[str, object]],
    requirements: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return f"""# 805 - Y5 R10 Metric-Response Kernel Theorem Or Source-Lift Action-Block Gate

Current result: **the metric-response kernel can be stated as a clean conditional theorem, but it is not derived**. The exact missing object is the parent tensor source lift `Sigma_metric[q_tr]`. Without it, `R_loc q_tr=0` is only notation. With it, the local-GR gate becomes sharp: prove the transition source is metric-null while ordinary matter still sources the usual Newton/GR response.

Generated UTC: `{generated_utc}`

## Non-Claim Summary

{markdown_table(summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim"])}

## Conditional Kernel Theorem

{markdown_table(contracts, ["contract_id", "statement", "equation", "claim_status", "why_it_matters", "valid_for_claim"])}

## Derivation Audit

{markdown_table(audits, ["audit_id", "attempt", "result", "obstruction", "decision", "valid_for_claim"])}

## Source-Lift Action-Block Requirements

{markdown_table(requirements, ["requirement_id", "required_object", "must_show", "allowed_routes", "status", "blocks", "valid_for_claim"])}

## Local Response Decision

{markdown_table(decisions, ["decision_id", "question", "answer", "status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## The Actual Kernel Law

If the parent theory supplies a metric Hessian `E_g`, physical projection `Pi_phys`, and tensor source lift `Sigma_metric[q]`, then:

```text
delta S_tr / delta g_loc^{{mu nu}} := -1/2 sqrt(-g) Sigma_metric[q_tr]_{{mu nu}}
R_loc q := Pi_phys E_g^{-1} Sigma_metric[q]
```

The transition branch is locally safe only if:

```text
Pi_phys E_g^{-1} Sigma_metric[q_tr] = 0
```

and ordinary matter remains visible only if:

```text
Pi_phys E_g^{-1} Sigma_metric[q_matter] = Pi_phys E_g^{-1} T_matter
```

That is the whole fight now. A label projector can always be written; a parent-derived metric-null source lift has to be earned.

## Verdict

805 improves the theory because it tells us exactly what must be derived. It also refuses the shortcut. `K_own` conservation and `P_metric,loc[K_own]=0` are not enough unless they descend from an action/source-lift theorem. The local branch therefore remains **closure-only**, not a derived GR/Newton reduction.

## Next Target

`{NEXT_TARGET}`
"""


def write_outputs() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    contracts = kernel_contract_rows(generated_utc)
    audits = derivation_audit_rows(generated_utc)
    requirements = source_lift_requirement_rows(generated_utc)
    decisions = local_response_decision_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validations = validation_rows(sources, contracts, audits, requirements, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(KERNEL_CONTRACT_PATH, contracts, ["contract_id", "statement", "equation", "claim_status", "why_it_matters", "valid_for_claim", "generated_utc"])
    write_csv(DERIVATION_AUDIT_PATH, audits, ["audit_id", "attempt", "result", "obstruction", "decision", "valid_for_claim", "generated_utc"])
    write_csv(SOURCE_LIFT_REQUIREMENTS_PATH, requirements, ["requirement_id", "required_object", "must_show", "allowed_routes", "status", "blocks", "valid_for_claim", "generated_utc"])
    write_csv(LOCAL_RESPONSE_DECISION_PATH, decisions, ["decision_id", "question", "answer", "status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validations, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        build_doc(generated_utc, sources, contracts, audits, requirements, decisions, summary, validations),
        encoding="utf-8",
    )

    failed_checks = [row for row in validations if row["result"] != "pass"]
    if failed_checks:
        failed_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed_checks)
        raise SystemExit(f"805 validation failed: {failed_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    write_outputs()
