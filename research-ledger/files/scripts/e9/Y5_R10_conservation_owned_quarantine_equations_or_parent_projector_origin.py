from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "804-Y5-R10-conservation-owned-quarantine-equations-or-parent-projector-origin.md"
NEXT_TARGET = "805-Y5-R10-metric-response-kernel-theorem-or-source-lift-action-block-gate.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_804_SOURCE_REGISTER.csv"
QUARANTINE_EQUATIONS_PATH = RESIDUALS / "P8_Y5_R10_804_QUARANTINE_EQUATIONS.csv"
PARENT_ORIGIN_PATH = RESIDUALS / "P8_Y5_R10_804_PARENT_ORIGIN_AUDIT.csv"
RESPONSE_KERNEL_PATH = RESIDUALS / "P8_Y5_R10_804_RESPONSE_KERNEL_REQUIREMENTS.csv"
LOCAL_CLAIM_GATE_PATH = RESIDUALS / "P8_Y5_R10_804_LOCAL_CLAIM_GATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_804_DERIVATION_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_804_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_804_VALIDATION.csv"

STATUS = "Y5_R10_804_conservation_owned_quarantine_equations_clean_closure_parent_origin_missing_nonclaim"
CLAIM_CEILING = "quarantine_equations_only_no_parent_Rloc_no_Kown_action_no_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    QUARANTINE_EQUATIONS_PATH,
    PARENT_ORIGIN_PATH,
    RESPONSE_KERNEL_PATH,
    LOCAL_CLAIM_GATE_PATH,
    DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "803_doc",
        "path": POST_CHECKPOINT / "803-Y5-R10-transition-shell-exact-cancellation-projector-or-quarantine.md",
        "needles": ["Q803_0_conservation_owned_quarantine", "P_metric,loc K_own=0", "D803_2_survival_route"],
        "role": "immediate 803 quarantine-only route",
    },
    {
        "source_id": "803_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_803_VALIDATION.csv",
        "needles": ["V803_8_quarantine_only_nonclaim,pass", "V803_10_no_local_GR_claim,pass"],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "spine_quarantine_equations",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["conservation_owned_quarantine_equations_clean_closure_not_parent_derived", "q_tr can be split into owned channels and conserved by K_own", "owner tensors are derived from parent invariants"],
        "role": "spine quarantine equation status",
    },
    {
        "source_id": "spine_projector_origin",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["quarantine_projector_parent_origin_not_derived_kernel_route_identified", "R_loc q_tr = 0 while ordinary matter still has the GR/Newton response"],
        "role": "spine parent-origin/kernel route",
    },
    {
        "source_id": "red_quarantine_equations",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["conservation_owned_quarantine_equations_clean_closure_not_parent_derived", "q_metric,loc can be quarantined while q_tr remains visible in K_own", "sector-label routing and current erasure are explicitly forbidden"],
        "role": "red-team quarantine equation status",
    },
    {
        "source_id": "red_projector_origin",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["quarantine_projector_parent_origin_not_derived_kernel_route_identified", "R_loc is not defined from parent action/coarse-graining", "ordinary matter GR response must be preserved"],
        "role": "red-team projector parent-origin gap",
    },
    {
        "source_id": "equation_register_local_routing",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": ["q_loc^nu = P_loc q_tr^nu", "nabla_mu K_tr,loc^{mu nu} = -q_loc^nu", "Kbar_MTS,00 ="],
        "role": "existing local routed-current equation register",
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


def quarantine_equation_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "equation_id": "QE804_0_current_split",
            "equation": "q_tr^nu = q_metric,loc^nu + q_own^nu",
            "condition": "q_metric,loc^nu = R_loc q_tr^nu; q_own^nu = (I - R_loc) q_tr^nu",
            "role": "keeps the transition current visible while separating local metric response from owned exchange",
            "status": "clean_closure_equation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "equation_id": "QE804_1_owner_tensor",
            "equation": "nabla_mu K_own^{mu nu} = -q_own^nu",
            "condition": "K_own is an owned exchange tensor, not silently added to the local metric source",
            "role": "restores total conservation without erasing q_tr",
            "status": "clean_closure_equation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "equation_id": "QE804_2_local_metric_quarantine",
            "equation": "P_metric,loc[K_own] = 0 and R_loc q_tr = 0 on local transition shells",
            "condition": "ordinary matter remains in the GR/Newton response sector",
            "role": "the actual local-safety condition; without it quarantine is only accounting",
            "status": "required_not_parent_derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "equation_id": "QE804_3_total_bianchi_bookkeeping",
            "equation": "nabla_mu(K_safe^{mu nu}+K_metric,loc^{mu nu}+K_own^{mu nu}) = -(q_base^nu+q_metric,loc^nu+q_own^nu)",
            "condition": "the split must be Bianchi-safe and not selected per dataset",
            "role": "keeps total-source conservation explicit",
            "status": "algebraic_closure_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def parent_origin_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "origin_id": "PO804_0_action_owner",
            "required_parent_origin": "An action block S_own or constrained auxiliary sector whose variation yields K_own and q_own.",
            "current_evidence": "K_own equations can be written, but owner dynamics are not derived from an action or transport law.",
            "status": "missing_parent_action_block",
            "blocks": "quarantine_as_derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "origin_id": "PO804_1_metric_kernel",
            "required_parent_origin": "A covariant response kernel R_loc/P_metric,loc derived from parent action or coarse-graining.",
            "current_evidence": "R_loc is not defined from parent action/coarse-graining; P_metric,loc=0 is a quarantine condition.",
            "status": "missing_parent_kernel",
            "blocks": "local_transition_shell_pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "origin_id": "PO804_2_matter_GR_response",
            "required_parent_origin": "The kernel must kill transition exchange current while preserving ordinary matter's GR/Newton response.",
            "current_evidence": "ordinary matter GR response preservation is named as required but not proven.",
            "status": "missing_response_preservation_theorem",
            "blocks": "equivalence_to_GR",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "origin_id": "PO804_3_non_erasure",
            "required_parent_origin": "Quarantine must route q_tr into owned exchange, not delete it.",
            "current_evidence": "the clean closure keeps q_tr visible in K_own and forbids current erasure.",
            "status": "closure_requirement_satisfied_not_parent_derived",
            "blocks": "none_by_itself",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def response_kernel_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "kernel_id": "RK804_0_linearity",
            "requirement": "R_loc is a linear/covariant response map on source-current classes.",
            "test_form": "R_loc(a q_1 + b q_2)=a R_loc q_1+b R_loc q_2",
            "status": "required_for_805",
            "failure_mode": "nonlinear or label-selected kernels are not parent theorems",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "kernel_id": "RK804_1_orthogonality",
            "requirement": "R_loc annihilates transition exchange currents.",
            "test_form": "R_loc q_tr = 0 or P_metric,loc[K_own]=0",
            "status": "required_for_805",
            "failure_mode": "without exact kernel orthogonality, the ~4.2e-17 shell bound returns",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "kernel_id": "RK804_2_matter_preservation",
            "requirement": "R_loc preserves ordinary local matter response.",
            "test_form": "R_loc q_matter gives the usual GR/Newton source response, not zero",
            "status": "required_for_805",
            "failure_mode": "a kernel that kills everything also kills gravity",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "kernel_id": "RK804_3_parent_descent",
            "requirement": "R_loc descends from action block, quotient geometry, Hessian/kinetic metric, or Noether identity.",
            "test_form": "no sector labels, no dataset labels, no post-hoc P_loc override",
            "status": "required_for_805",
            "failure_mode": "bookkeeping projector remains closure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def local_claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "LC804_0_equations_clean",
            "gate": "Are conservation-owned quarantine equations explicit and non-erasing?",
            "result": "pass_closure_only",
            "detail": "q_tr is split and owned by K_own rather than hidden",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "LC804_1_parent_origin",
            "gate": "Are K_own and R_loc parent-derived?",
            "result": "fail_for_claim",
            "detail": "owner action/transport law and response kernel are missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "LC804_2_local_GR",
            "gate": "Can local GR/Newton be claimed?",
            "result": "fail_for_claim",
            "detail": "transition shell and K_perp remain blockers",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D804_0_quarantine_equations",
            "question": "Can the quarantine route be written without hiding the transition current?",
            "answer": "Yes. q_tr can be split into q_metric,loc and q_own, with K_own conserving the owned exchange.",
            "status": "clean_closure_equations_written",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D804_1_parent_derivation",
            "question": "Is quarantine parent-derived?",
            "answer": "No. R_loc/P_metric,loc and K_own owner dynamics are not derived from the parent action.",
            "status": "not_parent_derived",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D804_2_next_route",
            "question": "What must be tried next?",
            "answer": "Build the metric-response kernel theorem or source-lift action-block gate: R_loc q_tr=0 while ordinary matter still sources GR.",
            "status": "attempt_metric_response_kernel_theorem",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D804_3_claim_status",
            "question": "Can the shell/local branch be promoted?",
            "answer": "No. 804 improves bookkeeping only; derived local GR remains false.",
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
            "what_improved": "The quarantine route is now an explicit conserved closure with q_tr visible and owned by K_own.",
            "what_blocks_claim": "K_own, R_loc/P_metric,loc, and ordinary-matter response preservation are not parent-derived.",
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
    equations: list[dict[str, object]],
    origins: list[dict[str, object]],
    kernels: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in sources)
    prior_ok, prior_detail = validation_file_clean(803)
    row_groups = [sources, equations, origins, kernels, claim_gates, decisions, summary]
    nonclaim_ok = all_rows_nonclaim(row_groups)
    formalization_count = formalization_change_count()
    equations_clean = any(row["equation_id"] == "QE804_1_owner_tensor" for row in equations) and any(row["equation_id"] == "QE804_2_local_metric_quarantine" for row in equations)
    parent_missing = any(row["origin_id"] == "PO804_1_metric_kernel" and row["status"] == "missing_parent_kernel" for row in origins)
    matter_gate = any(row["kernel_id"] == "RK804_2_matter_preservation" for row in kernels)
    local_false = any(row["status"] == "local_GR_claim_false" for row in decisions)
    return [
        {"check_id": "V804_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V804_1_prior_803_clean", "result": "pass" if prior_ok else "fail", "detail": prior_detail},
        {"check_id": "V804_2_outputs_scoped", "result": "pass" if all_outputs_scoped() else "fail", "detail": str(POST_CHECKPOINT)},
        {"check_id": "V804_3_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V804_4_quarantine_equations_explicit", "result": "pass" if equations_clean else "fail", "detail": "K_own and P_metric quarantine equations written"},
        {"check_id": "V804_5_parent_kernel_missing", "result": "pass" if parent_missing else "fail", "detail": "R_loc/P_metric,loc not parent-derived"},
        {"check_id": "V804_6_matter_response_gate_present", "result": "pass" if matter_gate else "fail", "detail": "ordinary matter GR response preservation required"},
        {"check_id": "V804_7_no_local_GR_claim", "result": "pass" if local_false else "fail", "detail": "derived GR/Newton remains blocked"},
        {"check_id": "V804_8_next_target_selected", "result": "pass" if decisions[-1]["next_target"] == NEXT_TARGET else "fail", "detail": NEXT_TARGET},
        {"check_id": "V804_9_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V804_10_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def build_doc(
    generated_utc: str,
    sources: list[dict[str, object]],
    equations: list[dict[str, object]],
    origins: list[dict[str, object]],
    kernels: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return f"""# 804 - Y5 R10 Conservation-Owned Quarantine Equations Or Parent Projector Origin

Current result: **quarantine can be written cleanly, but it is still closure, not derived local GR**. The transition current is no longer hidden: it is split into a local metric-response channel and an owned exchange channel, with `K_own` carrying the quarantined current. This is algebraically and Bianchi-clean as a closure. It becomes physics only if `K_own`, `R_loc/P_metric,loc`, and ordinary-matter response preservation descend from the parent action/coarse-graining theorem. Current evidence does not derive those parent origins.

Generated UTC: `{generated_utc}`

## Non-Claim Summary

{markdown_table(summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim"])}

## Quarantine Equations

{markdown_table(equations, ["equation_id", "equation", "condition", "role", "status", "valid_for_claim"])}

## Parent Origin Audit

{markdown_table(origins, ["origin_id", "required_parent_origin", "current_evidence", "status", "blocks", "valid_for_claim"])}

## Response Kernel Requirements

{markdown_table(kernels, ["kernel_id", "requirement", "test_form", "status", "failure_mode", "valid_for_claim"])}

## Local Claim Gate

{markdown_table(claim_gates, ["gate_id", "gate", "result", "detail", "valid_for_claim"])}

## Decision

{markdown_table(decisions, ["decision_id", "question", "answer", "status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## Verdict

The clean closure is:

```text
q_tr^nu = q_metric,loc^nu + q_own^nu
q_metric,loc^nu = R_loc q_tr^nu
q_own^nu = (I - R_loc) q_tr^nu
nabla_mu K_own^{{mu nu}} = -q_own^nu
P_metric,loc[K_own] = 0
```

This is useful because it prevents cheating: the current is not erased, and conservation is explicit. But it is not a derivation. To become a real local-GR reduction, the parent theory must prove:

```text
R_loc q_tr = 0
R_loc ordinary matter -> GR/Newton response
K_own descends from an action/Noether/transport block
```

Without that, quarantine is honest bookkeeping and the local transition shell remains closure-only.

## Next Target

`{NEXT_TARGET}`
"""


def write_outputs() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    equations = quarantine_equation_rows(generated_utc)
    origins = parent_origin_rows(generated_utc)
    kernels = response_kernel_rows(generated_utc)
    claim_gates = local_claim_gate_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validations = validation_rows(sources, equations, origins, kernels, claim_gates, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(QUARANTINE_EQUATIONS_PATH, equations, ["equation_id", "equation", "condition", "role", "status", "valid_for_claim", "generated_utc"])
    write_csv(PARENT_ORIGIN_PATH, origins, ["origin_id", "required_parent_origin", "current_evidence", "status", "blocks", "valid_for_claim", "generated_utc"])
    write_csv(RESPONSE_KERNEL_PATH, kernels, ["kernel_id", "requirement", "test_form", "status", "failure_mode", "valid_for_claim", "generated_utc"])
    write_csv(LOCAL_CLAIM_GATE_PATH, claim_gates, ["gate_id", "gate", "result", "detail", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "question", "answer", "status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validations, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        build_doc(generated_utc, sources, equations, origins, kernels, claim_gates, decisions, summary, validations),
        encoding="utf-8",
    )

    failed_checks = [row for row in validations if row["result"] != "pass"]
    if failed_checks:
        failed_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed_checks)
        raise SystemExit(f"804 validation failed: {failed_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    write_outputs()
