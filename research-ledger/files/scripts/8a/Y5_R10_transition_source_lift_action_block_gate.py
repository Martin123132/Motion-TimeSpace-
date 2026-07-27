from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "806-Y5-R10-transition-source-lift-action-block-gate.md"
NEXT_TARGET = "807-Y5-R10-owner-spacetime-solder-map-theorem.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_806_SOURCE_REGISTER.csv"
SOURCE_LIFT_CANDIDATES_PATH = RESIDUALS / "P8_Y5_R10_806_SOURCE_LIFT_CANDIDATES.csv"
ACTION_BLOCK_CONDITIONS_PATH = RESIDUALS / "P8_Y5_R10_806_ACTION_BLOCK_CONDITIONS.csv"
ROUTE_SELECTION_PATH = RESIDUALS / "P8_Y5_R10_806_ROUTE_SELECTION.csv"
BLOCKER_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_806_BLOCKER_LEDGER.csv"
CLAIM_STATUS_PATH = RESIDUALS / "P8_Y5_R10_806_CLAIM_STATUS.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_806_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_806_VALIDATION.csv"

STATUS = "Y5_R10_806_source_lift_action_block_not_parent_derived_owner_solder_route_selected_nonclaim"
CLAIM_CEILING = "source_lift_contract_and_route_selection_only_no_derived_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

RUN_137 = FORMALIZATION / "runs" / "20260528-184357-transition-source-lift-action-block"
RUN_138 = FORMALIZATION / "runs" / "20260528-185851-metric-null-action-block-contract"
RUN_140 = FORMALIZATION / "runs" / "20260528-190949-doubled-open-system-metric-null-theorem"
RUN_141 = FORMALIZATION / "runs" / "20260528-191541-doubled-owner-connection-current-primitive"

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    SOURCE_LIFT_CANDIDATES_PATH,
    ACTION_BLOCK_CONDITIONS_PATH,
    ROUTE_SELECTION_PATH,
    BLOCKER_LEDGER_PATH,
    CLAIM_STATUS_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "805_doc",
        "path": POST_CHECKPOINT / "805-Y5-R10-metric-response-kernel-theorem-or-source-lift-action-block-gate.md",
        "needles": ["SL805_0_action_block", "D805_1_source_lift", "806-Y5-R10-transition-source-lift-action-block-gate.md"],
        "role": "immediate 805 source-lift target",
    },
    {
        "source_id": "805_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_805_VALIDATION.csv",
        "needles": ["V805_5_conditional_only_not_derived,pass", "V805_9_next_target_selected,pass,806-Y5-R10-transition-source-lift-action-block-gate.md"],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "formal_137_doc",
        "path": FORMALIZATION / "137-transition-source-lift-action-block.md",
        "needles": ["transition_source_lift_action_block_not_derived_minimal_contract_required", "next_build_metric_null_action_block_contract", "Sigma_metric[q_tr] = 0"],
        "role": "earlier source-lift action-block gate",
    },
    {
        "source_id": "run_137_summary",
        "path": RUN_137 / "summary.csv",
        "needles": ["transition_source_lift_action_block_not_derived_minimal_contract_required", "next_build_metric_null_action_block_contract", "4.212667126774669e-17"],
        "role": "source-lift gate machine result",
    },
    {
        "source_id": "run_137_gate_criteria",
        "path": RUN_137 / "results" / "gate_criteria.csv",
        "needles": ["Sigma_metric_source_lift_defined,fail_not_derived", "minimal_action_block_contract_identified,pass_next_target", "derived_local_GR,fail"],
        "role": "source-lift pass/fail criteria",
    },
    {
        "source_id": "run_138_contract",
        "path": RUN_138 / "results" / "contract_equations.csv",
        "needles": ["C2_transition_metric_null", "C7_covariance_escape", "C9_Kperp_separate"],
        "role": "metric-null action-block C0-C9 contract",
    },
    {
        "source_id": "run_140_summary",
        "path": RUN_140 / "summary.csv",
        "needles": ["doubled_open_system_metric_null_theorem_pure_route_fails_owner_connection_hybrid_required", "next_build_doubled_owner_connection_current_primitive"],
        "role": "pure doubled route failure and hybrid selection",
    },
    {
        "source_id": "formal_141_doc",
        "path": FORMALIZATION / "141-doubled-owner-connection-current-primitive.md",
        "needles": ["owner_connection_current_primitive_candidate_projection_solder_map_not_derived", "next_build_owner_spacetime_solder_map_theorem"],
        "role": "owner-connection primitive and solder-map target",
    },
    {
        "source_id": "run_141_gate_criteria",
        "path": RUN_141 / "results" / "gate_criteria.csv",
        "needles": ["best_next_theorem,solder_map_theorem_required", "derived_local_GR,fail"],
        "role": "owner-connection gate criteria",
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


def source_lift_candidate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "candidate": "zero_metric_lift",
            "definition": "Sigma_metric[q_tr]=0",
            "status": "imposed_closure_not_derivation",
            "reason": "It is the desired theorem, not an explanation.",
            "route_decision": "reject_as_claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate": "owner_tensor_lift",
            "definition": "Sigma_metric[q_tr]=K_own",
            "status": "fails_metric_invisibility",
            "reason": "A tensor that owns the current can still source the local metric.",
            "route_decision": "reject_without_metric_null_owner_theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate": "trace_residual_lift",
            "definition": "Sigma_metric[q_tr]=Gamma_eff g-K_hat",
            "status": "metric_visible_generically",
            "reason": "This is the dangerous local residual, not a quarantine proof.",
            "route_decision": "reject_for_local_GR",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate": "pure_gauge_or_Ward_lift",
            "definition": "Sigma_metric[q_tr]=E_loc[Lie_xi g] or Ward-null",
            "status": "open_not_derived",
            "reason": "No transition gauge symmetry or Ward identity has been derived.",
            "route_decision": "backup_route",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate": "boundary_superpotential_lift",
            "definition": "Sigma_metric[q_tr]=nabla_rho U^{rho mu nu} with controlled support",
            "status": "open_not_derived",
            "reason": "No superpotential, antisymmetry, or local boundary-support theorem is signed.",
            "route_decision": "backup_route",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate": "owner_connection_solder_lift",
            "definition": "q_tr is owned in metric-independent owner geometry and projected to spacetime by a solder/projection map",
            "status": "best_live_route_not_derived",
            "reason": "It avoids g_loc inside the primitive, but the solder map can reintroduce metric variation.",
            "route_decision": "select_for_next_theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def action_block_condition_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "condition_id": "AB806_0_action_exists",
            "required_statement": "S_parent includes a transition/owner action block separate from ordinary matter.",
            "current_status": "fail_not_in_parent_v1",
            "why_it_matters": "Without an action block, Sigma_metric is not derived.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition_id": "AB806_1_transition_metric_null_variation",
            "required_statement": "delta S_tr/delta g_loc = 0 or Pi_phys E_g^{-1} Sigma_metric[q_tr]=0.",
            "current_status": "fail_not_derived",
            "why_it_matters": "This is the exact local transition-shell safety condition.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition_id": "AB806_2_matter_response",
            "required_statement": "delta S_m/delta g_loc gives nonzero T_matter and ordinary GR/Newton response.",
            "current_status": "required_open",
            "why_it_matters": "The fix must not save local tests by turning off gravity.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition_id": "AB806_3_owner_equations",
            "required_statement": "owner Euler-Lagrange equations imply nabla_mu K_A^{mu nu}+q_A^nu=0.",
            "current_status": "fail_not_derived",
            "why_it_matters": "Prevents current erasure.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition_id": "AB806_4_covariance_without_metric_stress",
            "required_statement": "covariance is maintained without sqrt(-g), nabla, traces, contractions, or constraints regenerating metric stress.",
            "current_status": "tension_open",
            "why_it_matters": "This is where most elegant-looking routes secretly fail.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition_id": "AB806_5_exactness_or_bound",
            "required_statement": "metric-nullity is exact, or normalized local response is <=4.212667126774669e-17.",
            "current_status": "fail_without_exact_null",
            "why_it_matters": "The transition shell bound is too severe for smooth tuning.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition_id": "AB806_6_Kperp",
            "required_statement": "K_perp is absent, higher order, gauge/boundary, or independently PPN-bounded.",
            "current_status": "separate_required_open",
            "why_it_matters": "Nulling q_tr does not automatically remove transverse tensor leakage.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_selection_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route": "topological_density",
            "score": "backup",
            "status": "open_not_derived",
            "reason": "Can be metric-null if exact, but owner equations and local support are not derived.",
            "next_action": "keep_as_backup",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route": "boundary_superpotential",
            "score": "backup",
            "status": "open_not_derived",
            "reason": "Can silence bulk response, but finite local boundary terms are uncontrolled.",
            "next_action": "keep_as_backup",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route": "pure_doubled_open_system",
            "score": "rejected_as_sufficient",
            "status": "pure_route_fails",
            "reason": "Prior gate found nabla, traces, connections, and contractions still reintroduce metric dependence.",
            "next_action": "do_not_repeat_as_standalone",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route": "Palatini_or_independent_connection",
            "score": "backup_plus",
            "status": "open_not_derived",
            "reason": "Helps remove g_loc nabla, but compatibility constraints can bring metric dependence back.",
            "next_action": "fold_into_owner_connection_hybrid",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route": "Ward_identity",
            "score": "high_payoff_backup",
            "status": "no_symmetry_derived",
            "reason": "Would be decisive if found, but no parent gauge identity currently exists.",
            "next_action": "search_later",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route": "owner_connection_solder_map",
            "score": "best_next",
            "status": "selected_not_derived",
            "reason": "It defines transition balance before local metric projection and matches the owner/exchange scaffold.",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def blocker_ledger_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "rank": 1,
            "blocker": "owner_spacetime_solder_map",
            "needed_statement": "Define E_I^nu or Pi^{mu nu}_{I...} mapping owner primitives to q_A and K_A.",
            "why_it_matters": "Without it, internal owner current has no physical spacetime conservation meaning.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank": 2,
            "blocker": "metric_null_solder_variation",
            "needed_statement": "delta E_I^nu/delta g_loc=0 or pure boundary/gauge/PPN-null variation.",
            "why_it_matters": "Prevents Sigma_metric[q_tr] returning through projection.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank": 3,
            "blocker": "diffeomorphism_covariance",
            "needed_statement": "Projection is covariant without fixed-background cheating.",
            "why_it_matters": "The route must remain a serious field theory, not a coordinate device.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank": 4,
            "blocker": "spacetime_conservation_recovery",
            "needed_statement": "Projection of owner balance implies nabla_mu K_A^{mu nu}+q_A^nu=0.",
            "why_it_matters": "Keeps the quarantine conservation ledger real.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank": 5,
            "blocker": "matter_and_Kperp_guardrails",
            "needed_statement": "matter remains GR/Newton and K_perp is absent, higher order, boundary/gauge, or bounded.",
            "why_it_matters": "Even a good solder theorem cannot ignore known local tests.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_status_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "claim": "Sigma_metric[q_tr] is parent-derived",
            "status_after_gate": "false",
            "reason": "Current route identifies candidate lifts but derives none.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "claim": "A coherent metric-null action-block contract exists",
            "status_after_gate": "true_contract",
            "reason": "C0-C9 style conditions are coherent and route-checkable.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "claim": "Owner-connection/solder route is best next target",
            "status_after_gate": "true_route_selection",
            "reason": "Pure doubled is insufficient; owner primitive plus solder theorem is the sharpest remaining non-cheating route.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "claim": "Derived local GR through transition shells",
            "status_after_gate": "false",
            "reason": "Solder projection, metric-null variation, matter response, and K_perp remain unproved.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_improved": "806 rejects source-lift shortcuts and selects the owner-connection/solder-map theorem as the best live route.",
            "what_blocks_claim": "No parent action derives Sigma_metric[q_tr]=0, no solder/projection theorem is proven, and local GR remains closure-only.",
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
    candidates: list[dict[str, object]],
    conditions: list[dict[str, object]],
    routes: list[dict[str, object]],
    blockers: list[dict[str, object]],
    claims: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in sources)
    prior_ok, prior_detail = validation_file_clean(805)
    row_groups = [sources, candidates, conditions, routes, blockers, claims, summary]
    nonclaim_ok = all_rows_nonclaim(row_groups)
    formalization_count = formalization_change_count()
    rejects_shortcuts = any(row["candidate"] == "zero_metric_lift" and row["route_decision"] == "reject_as_claim" for row in candidates)
    action_missing = any(row["condition_id"] == "AB806_0_action_exists" and row["current_status"] == "fail_not_in_parent_v1" for row in conditions)
    matter_guard = any(row["condition_id"] == "AB806_2_matter_response" for row in conditions)
    route_selected = any(row["route"] == "owner_connection_solder_map" and row["score"] == "best_next" for row in routes)
    solder_blocker = any(row["blocker"] == "owner_spacetime_solder_map" for row in blockers)
    local_false = any(row["claim"] == "Derived local GR through transition shells" and row["status_after_gate"] == "false" for row in claims)
    return [
        {"check_id": "V806_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V806_1_prior_805_clean", "result": "pass" if prior_ok else "fail", "detail": prior_detail},
        {"check_id": "V806_2_outputs_scoped", "result": "pass" if all_outputs_scoped() else "fail", "detail": str(POST_CHECKPOINT)},
        {"check_id": "V806_3_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V806_4_shortcuts_rejected", "result": "pass" if rejects_shortcuts else "fail", "detail": "Sigma_metric[q_tr]=0 by definition rejected"},
        {"check_id": "V806_5_action_block_missing_recorded", "result": "pass" if action_missing else "fail", "detail": "parent v1 action block missing"},
        {"check_id": "V806_6_matter_response_guard_present", "result": "pass" if matter_guard else "fail", "detail": "ordinary matter GR/Newton guard retained"},
        {"check_id": "V806_7_owner_solder_route_selected", "result": "pass" if route_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V806_8_solder_blocker_recorded", "result": "pass" if solder_blocker else "fail", "detail": "owner-spacetime solder map is main blocker"},
        {"check_id": "V806_9_no_local_GR_claim", "result": "pass" if local_false else "fail", "detail": "derived local GR remains false"},
        {"check_id": "V806_10_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V806_11_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def build_doc(
    generated_utc: str,
    sources: list[dict[str, object]],
    candidates: list[dict[str, object]],
    conditions: list[dict[str, object]],
    routes: list[dict[str, object]],
    blockers: list[dict[str, object]],
    claims: list[dict[str, object]],
    summary: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return f"""# 806 - Y5 R10 Transition Source-Lift Action-Block Gate

Current result: **the source-lift/action-block route is still not derived, but the best live route is now sharper**. We reject the cheap move `Sigma_metric[q_tr]=0` by notation. A coherent metric-null contract exists, but parent v1 does not derive it. The strongest next path is an owner-connection/current primitive plus an owner-spacetime solder/projection theorem.

Generated UTC: `{generated_utc}`

## Non-Claim Summary

{markdown_table(summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim"])}

## Source-Lift Candidates

{markdown_table(candidates, ["candidate", "definition", "status", "reason", "route_decision", "valid_for_claim"])}

## Action-Block Conditions

{markdown_table(conditions, ["condition_id", "required_statement", "current_status", "why_it_matters", "valid_for_claim"])}

## Route Selection

{markdown_table(routes, ["route", "score", "status", "reason", "next_action", "valid_for_claim"])}

## Blocker Ledger

{markdown_table(blockers, ["rank", "blocker", "needed_statement", "why_it_matters", "next_target", "valid_for_claim"])}

## Claim Status

{markdown_table(claims, ["claim", "status_after_gate", "reason", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## Derivation Position

The source-lift route must satisfy:

```text
Sigma_metric[q_tr] := -2/sqrt(-g) delta S_tr/delta g_loc = 0
delta S_m/delta g_loc != 0
delta S_tr/delta A_A -> nabla_mu K_A^{{mu nu}} + q_A^nu = 0
```

The failed shortcuts are now explicit:

```text
Sigma_metric[q_tr]=0 by definition: rejected.
K_own owns q_tr, therefore K_own is invisible: rejected.
Pure doubled/open-system cancellation alone: insufficient.
```

The live route is:

```text
D_A J_A^I + s_A^I = 0
q_A^nu = E_I^nu s_A^I
K_A^{{mu nu}} = Pi^{{mu nu}}_I J_A^I
delta E_I^nu/delta g_loc = 0 or boundary/gauge/PPN-null
```

That shifts the hard problem from “make q_tr vanish” to “project owner current into spacetime without reintroducing metric variation.” That is a better problem. It is tighter, less cheat-prone, and closer to a derivable field-theory mechanism.

## Verdict

806 does **not** give local GR. It gives a cleaner hunt: prove the owner-spacetime solder/projection theorem, or demote the transition-shell local branch to explicit closure-only. The branch is not dead, but the next theorem has to carry real weight.

## Next Target

`{NEXT_TARGET}`
"""


def write_outputs() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    candidates = source_lift_candidate_rows(generated_utc)
    conditions = action_block_condition_rows(generated_utc)
    routes = route_selection_rows(generated_utc)
    blockers = blocker_ledger_rows(generated_utc)
    claims = claim_status_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validations = validation_rows(sources, candidates, conditions, routes, blockers, claims, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(SOURCE_LIFT_CANDIDATES_PATH, candidates, ["candidate", "definition", "status", "reason", "route_decision", "valid_for_claim", "generated_utc"])
    write_csv(ACTION_BLOCK_CONDITIONS_PATH, conditions, ["condition_id", "required_statement", "current_status", "why_it_matters", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_SELECTION_PATH, routes, ["route", "score", "status", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(BLOCKER_LEDGER_PATH, blockers, ["rank", "blocker", "needed_statement", "why_it_matters", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_STATUS_PATH, claims, ["claim", "status_after_gate", "reason", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validations, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        build_doc(generated_utc, sources, candidates, conditions, routes, blockers, claims, summary, validations),
        encoding="utf-8",
    )

    failed_checks = [row for row in validations if row["result"] != "pass"]
    if failed_checks:
        failed_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed_checks)
        raise SystemExit(f"806 validation failed: {failed_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    write_outputs()
