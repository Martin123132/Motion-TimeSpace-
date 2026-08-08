from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "803-Y5-R10-transition-shell-exact-cancellation-projector-or-quarantine.md"
NEXT_TARGET = "804-Y5-R10-conservation-owned-quarantine-equations-or-parent-projector-origin.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_803_SOURCE_REGISTER.csv"
ANTI_CHEAT_PATH = RESIDUALS / "P8_Y5_R10_803_TRANSITION_SHELL_ANTI_CHEAT_BOUND.csv"
EXACT_CANCELLATION_PATH = RESIDUALS / "P8_Y5_R10_803_EXACT_CANCELLATION_AUDIT.csv"
PROJECTOR_PATH = RESIDUALS / "P8_Y5_R10_803_PROJECTOR_SUPPRESSION_AUDIT.csv"
QUARANTINE_PATH = RESIDUALS / "P8_Y5_R10_803_QUARANTINE_ROUTE_LEDGER.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_803_DERIVATION_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_803_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_803_VALIDATION.csv"

STATUS = "Y5_R10_803_transition_shell_exact_cancellation_projector_not_parent_derived_quarantine_only_nonclaim"
CLAIM_CEILING = "transition_shell_gate_only_no_exact_cancellation_no_projector_suppression_no_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    ANTI_CHEAT_PATH,
    EXACT_CANCELLATION_PATH,
    PROJECTOR_PATH,
    QUARANTINE_PATH,
    DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "802_doc",
        "path": POST_CHECKPOINT / "802-Y5-R10-parent-ZL-evenness-and-gradient-signature-gate.md",
        "needles": ["transition shells with `U_B=O(1)`", "TS802_1_exact_cancellation", "D802_3_next_route"],
        "role": "immediate 802 transition-shell obstruction and selected route",
    },
    {
        "source_id": "802_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_802_VALIDATION.csv",
        "needles": ["V802_8_transition_shell_blocks_claim,pass", "V802_11_no_local_GR_claim,pass"],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "spine_transition_shell_bound",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["transition_shell_direct_bound_fails_only_exact_or_quarantine_route_open", "direct local transition projection, U_B^2 suppression, width scaling, and"],
        "role": "transition-shell anti-cheat result and failed suppression routes",
    },
    {
        "source_id": "spine_exact_projector_status",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["exact_transition_cancellation_projector_not_derived_quarantine_only", "Derived local GR is blocked at the transition shell"],
        "role": "exact cancellation/projector theorem status",
    },
    {
        "source_id": "red_transition_bound",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["transition_shell_direct_bound_fails_only_exact_or_quarantine_route_open", "required suppression is about 4.2e-17"],
        "role": "red-team transition shell bound and survival routes",
    },
    {
        "source_id": "red_exact_projector_status",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["exact_transition_cancellation_projector_not_derived_quarantine_only", "the required transition suppression is ~4.2e-17", "exact theorem absent; quarantine or demotion"],
        "role": "red-team exact theorem absence",
    },
    {
        "source_id": "equation_register_routed_current",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": ["q_loc^nu = P_loc q_tr^nu", "nabla_mu K_tr,loc^{mu nu} = -q_loc^nu", "Kbar_MTS,00 ="],
        "role": "routed transition-current local branch equations",
    },
    {
        "source_id": "equation_register_stress_row",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": ["Solar transition shell:", "P_loc = 1", "epsilon_N,loc = 48.57583895725583", "gate_status = stress_fail_if_projected_locally"],
        "role": "local stress-test row showing direct projection failure",
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


def anti_cheat_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "AC803_0_required_shell_suppression",
            "test": "Can a generic small coefficient or U_B^2 factor hide the local shell?",
            "known_scale": "required local transition suppression ~4.2e-17; stress row epsilon_N,loc=48.57583895725583",
            "result": "fail_for_generic_suppression",
            "reason": "transition shells have U_B=O(1), so far-local U_B^2 suppression disappears",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "AC803_1_width_scaling",
            "test": "Can L_tr width scaling alone pass the local PPN shell?",
            "known_scale": "L_tr=4 Delta_B L_B and q_tr contains L_tr^-1 and L_tr^-3 terms",
            "result": "fail_or_unclaimed",
            "reason": "width scaling is not an exact zero and was already rejected by the shell bound gate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "AC803_2_direct_metric_projection",
            "test": "Can direct local metric projection be treated as safe?",
            "known_scale": "q_loc^nu=P_loc q_tr^nu with Solar/shell rows P_loc=1 or open_ppn_required",
            "result": "rejected",
            "reason": "equation register explicitly marks direct local transition projection unsafe/open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def exact_cancellation_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "EC803_0_Khat_trace_cancellation",
            "candidate_theorem": "nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}=0 inside local transition shell",
            "needed_identity": "parent variation forces K_hat gradient to cancel Gamma_eff gradient pointwise or as a local metric-response kernel",
            "audit_result": "not_derived",
            "why": "F1 trace locking helps scalar amplitude but does not cancel transition gradients or K_hat projector response",
            "claim_effect": "blocks_exact_local_zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "EC803_1_Bianchi_exactness",
            "candidate_theorem": "q_tr is an exact/internal exchange current whose local metric response is identically zero",
            "needed_identity": "P_metric,loc q_tr=0 follows from Bianchi-safe parent decomposition, not from bookkeeping labels",
            "audit_result": "not_derived",
            "why": "current conservation can route exchange, but does not by itself set the local metric kernel to zero",
            "claim_effect": "blocks_parent_projector_claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "EC803_2_boundary_cancellation",
            "candidate_theorem": "transition-shell local response integrates to a pure boundary term with zero PPN multipoles",
            "needed_identity": "worldtube boundary data and multipole moments vanish or cancel by parent theorem",
            "audit_result": "not_derived",
            "why": "no boundary/multipole cancellation theorem is present for the shell",
            "claim_effect": "blocks_solar_transition_pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def projector_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "projector_id": "PR803_0_existing_Ploc",
            "candidate": "existing routing projector P_loc",
            "required_behavior": "P_loc <= O(4.2e-17) on local transition shell or exact metric kernel zero",
            "audit_result": "fails_direct_suppression",
            "why": "equation register has Solar transition P_loc=1 and toy rows where local projection remains PPN-required/failing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "projector_id": "PR803_1_scalar_smallness_projector",
            "candidate": "projector chosen by small U_B or scalar smoothness",
            "required_behavior": "must suppress shell where U_B=O(1)",
            "audit_result": "fails_shell",
            "why": "the small parameter is not small at the transition shell",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "projector_id": "PR803_2_parent_metric_kernel",
            "candidate": "new parent-derived metric response kernel P_metric,loc",
            "required_behavior": "P_metric,loc q_tr=0 for transition exchange currents while preserving GR matter response",
            "audit_result": "open_not_derived",
            "why": "this is the only clean projector route, but no parent kernel theorem exists yet",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def quarantine_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "quarantine_id": "Q803_0_conservation_owned_quarantine",
            "route": "split q_tr into owned exchange channels with a compensating owner tensor K_own",
            "status": "only_surviving_nonclaim_route",
            "equation_target": "nabla_mu K_own^{mu nu}=-(q_gal^nu+q_cos^nu+q_shell^nu), P_metric,loc K_own=0",
            "why_not_claim": "clean bookkeeping is not a parent derivation until K_own and P_metric,loc descend from the action",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "quarantine_id": "Q803_1_demote_if_no_parent_origin",
            "route": "explicitly demote local transition branch to closure/quarantine",
            "status": "required_if_804_fails",
            "equation_target": "no local GR claim from transition shell; only far-local scalar closure remains",
            "why_not_claim": "without parent owner equations, quarantine is an accounting rule",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D803_0_direct_bound",
            "question": "Can direct local shell projection pass by amplitude/width/coefficient suppression?",
            "answer": "No. The required suppression is ~4.2e-17 and existing direct rows fail/open.",
            "status": "direct_projection_rejected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D803_1_exact_theorem",
            "question": "Is exact cancellation or local metric projector suppression parent-derived?",
            "answer": "No. Parent v1 does not derive K_hat cancellation, P_metric,loc suppression, or a boundary zero theorem.",
            "status": "exact_projector_not_derived",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D803_2_survival_route",
            "question": "What remains open?",
            "answer": "Only conservation-owned quarantine or a genuinely new parent metric-kernel theorem.",
            "status": "quarantine_only_nonclaim_route",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D803_3_local_GR_status",
            "question": "Can local GR/Newton be claimed after 803?",
            "answer": "No. The transition shell blocks derived local GR; Kperp also remains open.",
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
            "what_improved": "The transition-shell survival routes are now narrowed to exact cancellation/projector theorem or conservation-owned quarantine.",
            "what_blocks_claim": "No parent identity supplies the needed ~4.2e-17 shell suppression; quarantine is not a derived local-GR proof.",
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
    anti_cheat: list[dict[str, object]],
    exact: list[dict[str, object]],
    projectors: list[dict[str, object]],
    quarantines: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in sources)
    prior_ok, prior_detail = validation_file_clean(802)
    row_groups = [sources, anti_cheat, exact, projectors, quarantines, decisions, summary]
    nonclaim_ok = all_rows_nonclaim(row_groups)
    formalization_count = formalization_change_count()
    direct_rejected = any(row["gate_id"] == "AC803_2_direct_metric_projection" and row["result"] == "rejected" for row in anti_cheat)
    exact_not_derived = all(row["audit_result"] == "not_derived" for row in exact)
    projector_not_derived = any(row["projector_id"] == "PR803_2_parent_metric_kernel" and row["audit_result"] == "open_not_derived" for row in projectors)
    quarantine_only = any(row["quarantine_id"] == "Q803_0_conservation_owned_quarantine" and row["status"] == "only_surviving_nonclaim_route" for row in quarantines)
    return [
        {"check_id": "V803_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V803_1_prior_802_clean", "result": "pass" if prior_ok else "fail", "detail": prior_detail},
        {"check_id": "V803_2_outputs_scoped", "result": "pass" if all_outputs_scoped() else "fail", "detail": str(POST_CHECKPOINT)},
        {"check_id": "V803_3_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V803_4_required_suppression_recorded", "result": "pass" if any("4.2e-17" in row["known_scale"] for row in anti_cheat) else "fail", "detail": "transition anti-cheat suppression recorded"},
        {"check_id": "V803_5_direct_projection_rejected", "result": "pass" if direct_rejected else "fail", "detail": "direct local transition projection remains rejected"},
        {"check_id": "V803_6_exact_cancellation_not_derived", "result": "pass" if exact_not_derived else "fail", "detail": "no exact cancellation theorem promoted"},
        {"check_id": "V803_7_projector_suppression_not_derived", "result": "pass" if projector_not_derived else "fail", "detail": "parent metric kernel route open only"},
        {"check_id": "V803_8_quarantine_only_nonclaim", "result": "pass" if quarantine_only else "fail", "detail": "conservation-owned quarantine is nonclaim route"},
        {"check_id": "V803_9_next_target_selected", "result": "pass" if decisions[-1]["next_target"] == NEXT_TARGET else "fail", "detail": NEXT_TARGET},
        {"check_id": "V803_10_no_local_GR_claim", "result": "pass" if any(row["status"] == "local_GR_claim_false" for row in decisions) else "fail", "detail": "derived GR/Newton remains blocked"},
        {"check_id": "V803_11_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V803_12_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def build_doc(
    generated_utc: str,
    sources: list[dict[str, object]],
    anti_cheat: list[dict[str, object]],
    exact: list[dict[str, object]],
    projectors: list[dict[str, object]],
    quarantines: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return f"""# 803 - Y5 R10 Transition-Shell Exact Cancellation Projector Or Quarantine

Current result: **the transition shell still blocks derived local GR**. The shell is too severe for generic suppression: the required suppression is about `4.2e-17`, while the old stress row has `epsilon_N,loc=48.57583895725583` if projected locally. Since `U_B=O(1)` in the shell, the far-local `U_B^2` repair from 802 does not save it. Direct projection, width scaling, and coefficient tuning remain rejected. Exact cancellation/projector suppression is not parent-derived. The only route left standing is conservation-owned quarantine, and that is still non-claim until its owner tensor and metric kernel descend from the parent action.

Generated UTC: `{generated_utc}`

## Non-Claim Summary

{markdown_table(summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim"])}

## Anti-Cheat Bound

{markdown_table(anti_cheat, ["gate_id", "test", "known_scale", "result", "reason", "valid_for_claim"])}

## Exact Cancellation Audit

{markdown_table(exact, ["route_id", "candidate_theorem", "needed_identity", "audit_result", "why", "claim_effect", "valid_for_claim"])}

## Projector Suppression Audit

{markdown_table(projectors, ["projector_id", "candidate", "required_behavior", "audit_result", "why", "valid_for_claim"])}

## Quarantine Route Ledger

{markdown_table(quarantines, ["quarantine_id", "route", "status", "equation_target", "why_not_claim", "next_target", "valid_for_claim"])}

## Decision

{markdown_table(decisions, ["decision_id", "question", "answer", "status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## Verdict

No derived local-GR pass. The transition shell cannot be hidden by a merely small scalar closure:

```text
q_loc^nu = P_loc q_tr^nu
U_B(shell) = O(1)
required suppression ~= 4.2e-17
```

The only acceptable derivation route would be an exact parent identity:

```text
P_metric,loc q_tr = 0
```

or an exact cancellation:

```text
nabla^nu Gamma_eff - nabla_mu K_hat^{{mu nu}} = 0
```

on the local transition shell. Current parent v1 does not supply either. Therefore the honest next route is to formulate conservation-owned quarantine equations and then try to derive their projector/owner tensors from the parent action. If that cannot be parent-signed, the shell remains closure-only.

## Next Target

`{NEXT_TARGET}`
"""


def write_outputs() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    anti_cheat = anti_cheat_rows(generated_utc)
    exact = exact_cancellation_rows(generated_utc)
    projectors = projector_rows(generated_utc)
    quarantines = quarantine_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validations = validation_rows(sources, anti_cheat, exact, projectors, quarantines, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(ANTI_CHEAT_PATH, anti_cheat, ["gate_id", "test", "known_scale", "result", "reason", "valid_for_claim", "generated_utc"])
    write_csv(EXACT_CANCELLATION_PATH, exact, ["route_id", "candidate_theorem", "needed_identity", "audit_result", "why", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(PROJECTOR_PATH, projectors, ["projector_id", "candidate", "required_behavior", "audit_result", "why", "valid_for_claim", "generated_utc"])
    write_csv(QUARANTINE_PATH, quarantines, ["quarantine_id", "route", "status", "equation_target", "why_not_claim", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "question", "answer", "status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validations, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        build_doc(generated_utc, sources, anti_cheat, exact, projectors, quarantines, decisions, summary, validations),
        encoding="utf-8",
    )

    failed_checks = [row for row in validations if row["result"] != "pass"]
    if failed_checks:
        failed_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed_checks)
        raise SystemExit(f"803 validation failed: {failed_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    write_outputs()
