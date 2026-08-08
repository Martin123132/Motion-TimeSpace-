from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "808-Y5-R10-boundary-topological-backup-or-local-transition-demotion.md"
NEXT_TARGET = "809-Y5-R10-local-transition-closure-contract-and-testing-shift.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_808_SOURCE_REGISTER.csv"
ROUTE_CANDIDATES_PATH = RESIDUALS / "P8_Y5_R10_808_ROUTE_CANDIDATES.csv"
THEOREM_CONDITIONS_PATH = RESIDUALS / "P8_Y5_R10_808_THEOREM_CONDITIONS.csv"
DEMOTION_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_808_DEMOTION_CONTRACT.csv"
NEXT_STEPS_PATH = RESIDUALS / "P8_Y5_R10_808_NEXT_STEPS.csv"
CLAIM_STATUS_PATH = RESIDUALS / "P8_Y5_R10_808_CLAIM_STATUS.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_808_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_808_VALIDATION.csv"

STATUS = "Y5_R10_808_boundary_topological_backup_fails_transition_branch_demoted_closure_only_nonclaim"
CLAIM_CEILING = "local_transition_route_explicit_closure_only_no_derived_GR_no_fundamental_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

RUN_143 = FORMALIZATION / "runs" / "20260528-195637-boundary-topological-backup-gate"

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    ROUTE_CANDIDATES_PATH,
    THEOREM_CONDITIONS_PATH,
    DEMOTION_CONTRACT_PATH,
    NEXT_STEPS_PATH,
    CLAIM_STATUS_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "807_doc",
        "path": POST_CHECKPOINT / "807-Y5-R10-owner-spacetime-solder-map-theorem.md",
        "needles": ["boundary_topological_backup_open", "808-Y5-R10-boundary-topological-backup-or-local-transition-demotion.md", "Derived local GR through transition shells"],
        "role": "immediate 807 backup target",
    },
    {
        "source_id": "807_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_807_VALIDATION.csv",
        "needles": ["V807_7_boundary_topological_backup_open,pass", "V807_8_no_local_GR_claim,pass"],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "formal_143_doc",
        "path": FORMALIZATION / "143-boundary-topological-backup-gate.md",
        "needles": [
            "boundary_topological_backup_fails_transition_branch_demoted_closure_only",
            "transition_route_current_status = explicit_closure_only",
            "write_explicit_local_transition_closure_contract_and_shift_to_testing",
        ],
        "role": "earlier boundary/topological backup gate",
    },
    {
        "source_id": "run_143_summary",
        "path": RUN_143 / "summary.csv",
        "needles": ["boundary_topological_backup_fails_transition_branch_demoted_closure_only", "explicit_closure_only", "False,False"],
        "role": "boundary/topological machine summary",
    },
    {
        "source_id": "run_143_route_candidates",
        "path": RUN_143 / "results" / "route_candidates.csv",
        "needles": ["exact_superpotential", "topological_density", "Ward_or_anomaly_inflow", "global_reservoir_ledger"],
        "role": "route candidate table",
    },
    {
        "source_id": "run_143_gate_criteria",
        "path": RUN_143 / "results" / "gate_criteria.csv",
        "needles": ["nontrivial_owner_balance,fail_not_derived", "transition_branch_status,demote_to_explicit_closure_only", "derived_local_GR,fail"],
        "role": "backup pass/fail criteria",
    },
    {
        "source_id": "run_143_closure_contract",
        "path": RUN_143 / "results" / "closure_contract.csv",
        "needles": ["local_metric_quarantine", "transition_current_visibility", "public_claim_guardrail"],
        "role": "closure contract machine output",
    },
    {
        "source_id": "formal_144_doc",
        "path": FORMALIZATION / "144-local-transition-closure-contract.md",
        "needles": ["local transition branch = explicit closure-only", "MTS empirical testing = allowed but cannot substitute for derivation", "145-testing-readiness-and-gr-limit-map.md"],
        "role": "next closure-contract source",
    },
    {
        "source_id": "spine_143_144",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["boundary_topological_backup_fails_transition_branch_demoted_closure_only", "local transition branch is therefore explicit closure-only", "145-testing-readiness-and-gr-limit-map.md"],
        "role": "spine demotion and testing transition",
    },
    {
        "source_id": "red_143_144",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["boundary_topological_backup_fails_transition_branch_demoted_closure_only.", "local transition branch = closure-only.", "disciplined closure, not derived reduction."],
        "role": "red-team demotion result",
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


def route_candidate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route": "exact_superpotential",
            "ansatz": "K_A^{mu nu}=nabla_rho U_A^{rho mu nu} with antisymmetry",
            "bulk_metric_response": "not_safe_as_written",
            "ownership": "fails_generic_q_tr",
            "decision": "fail_as_derivation",
            "reason": "A true superpotential is either identically conserved or needs metric covariant derivatives that reintroduce local response.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route": "exterior_exact_form",
            "ansatz": "J_A=dU_A and dJ_A=0 with transition exchange moved to boundary form",
            "bulk_metric_response": "possible_if_no_hodge_metric",
            "ownership": "too_restrictive",
            "decision": "fail_without_parent_cohomology_theorem",
            "reason": "Generic q_tr is not exact-boundary unless supplied by a parent cohomology/support theorem.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route": "topological_density",
            "ansatz": "S_tr includes metric-independent characteristic/topological density",
            "bulk_metric_response": "pass_formally",
            "ownership": "physically_empty_without_defects",
            "decision": "true_but_insufficient",
            "reason": "Bulk metric-nullity alone makes the term local identity/boundary-only and does not own generic q_tr.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route": "boundary_defect_or_domain_wall",
            "ansatz": "q_tr is supported on transition boundary/defect with surface ledger",
            "bulk_metric_response": "bulk_null_but_surface_live",
            "ownership": "possible_but_unbounded",
            "decision": "fail_without_boundary_bound",
            "reason": "Finite surface terms are exactly what the local PPN bound must suppress.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route": "Ward_or_anomaly_inflow",
            "ansatz": "metric variation cancelled by transition Ward identity or inflow current",
            "bulk_metric_response": "open_if_symmetry_exists",
            "ownership": "not_derived",
            "decision": "fail_current_parent",
            "reason": "No parent transition symmetry or anomaly equation is derived.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route": "global_reservoir_ledger",
            "ansatz": "q_tr conserved in nonlocal/global owner ledger and excluded from local metric response",
            "bulk_metric_response": "closure_only",
            "ownership": "closure_only",
            "decision": "allowed_as_bookkeeping_not_derivation",
            "reason": "Coherent ledger, not parent-derived local GR.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def theorem_condition_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "condition": "true_bulk_metric_nullity",
            "required_statement": "delta S_boundary_topological/delta g_loc = 0 in the local bulk.",
            "status": "partial_formal_only",
            "gap": "Topological/exact forms can satisfy bulk nullity only after avoiding Hodge, connection, and boundary metric dependence.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition": "nontrivial_qtr_ownership",
            "required_statement": "The same term yields nabla_mu K_A^{mu nu}=-q_A^nu for transition current.",
            "status": "fail_not_derived",
            "gap": "Metric-null topological terms tend to be identities/boundaries, not generic local source owners.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition": "finite_boundary_control",
            "required_statement": "Boundary/surface metric response is zero or <=4.212667126774669e-17.",
            "status": "fail_not_derived",
            "gap": "No theorem suppresses transition surface terms by the hard local factor.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition": "support_theorem",
            "required_statement": "Transition boundaries do not perturb local PPN domains except by controlled null terms.",
            "status": "fail_not_derived",
            "gap": "Boundary ownership can become real local force/stress without support control.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition": "no_current_erasure",
            "required_statement": "q_tr remains visible in owner equation rather than set to zero by exactness.",
            "status": "fail_risk",
            "gap": "Strong exact forms can trivialize the current unless a defect/source theorem is supplied.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition": "local_GR_derivation",
            "required_statement": "Matter still sources GR/Newton while transition exchange has zero local PPN response by theorem.",
            "status": "fail",
            "gap": "Backup does not satisfy ownership plus metric-null plus boundary-control together.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def demotion_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "closure_item": "local_metric_quarantine",
            "statement": "q_metric,loc^nu = 0 or is excluded by explicit closure rule, not parent derivation.",
            "claim_status": "closure_assumption",
            "promotion_condition": "derive parent action/symmetry/coarse-graining theorem for exact local metric nullity",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_item": "transition_current_visibility",
            "statement": "q_tr^nu remains in an owner/global ledger and is not erased.",
            "claim_status": "required_for_internal_consistency",
            "promotion_condition": "derive owner equations from parent dynamics",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_item": "local_GR_limit",
            "statement": "Solar-system/local predictions use GR plus matter response unless a future parent theorem replaces the closure.",
            "claim_status": "conditional_recovery",
            "promotion_condition": "prove MTS -> GR -> Newton from the parent action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_item": "empirical_pillars",
            "statement": "Galaxy/cosmology tests may proceed but do not prove parent-derived local GR.",
            "claim_status": "allowed_with_label",
            "promotion_condition": "both fit data and derive the relevant local limit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_item": "public_claim_guardrail",
            "statement": "Do not claim derived local GR from transition-shell machinery.",
            "claim_status": "hard_forbidden_until_new_theorem",
            "promotion_condition": "new theorem must explicitly close Sigma_metric[q_tr], matter response, boundary terms, and K_perp",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_step_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "priority": 1,
            "next_step": "write_local_transition_closure_contract",
            "purpose": "Make the local branch honest: closure-only, no derived-local-GR claim.",
            "target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "priority": 2,
            "next_step": "separate_empirical_testing_from_local_derivation",
            "purpose": "Proceed to SPARC/Pantheon/BAO/CMB tests without pretending they solve PPN closure.",
            "target": "testing_readiness_and_GR_limit_map",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "priority": 3,
            "next_step": "catalog_new_parent_mechanisms_only_if_available",
            "purpose": "Reopen local derivation only with genuinely new symmetry, constraint, action, or coarse-graining theorem.",
            "target": "future_parent_action_contract",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "priority": 4,
            "next_step": "keep_Kperp_as_independent_blocker",
            "purpose": "Do not let closure-only transition safety hide transverse leakage.",
            "target": "K_perp_guardrail",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_status_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "claim": "Boundary/topological backup derives transition-shell local safety",
            "status_after_gate": "false",
            "reason": "It cannot satisfy bulk metric-nullity, nontrivial q_tr ownership, and finite-boundary control together.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "claim": "Topological terms can be bulk metric-null",
            "status_after_gate": "true_but_insufficient",
            "reason": "Bulk metric-nullity alone tends to make the term locally empty or boundary-only.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "claim": "Local transition route is still an active derivation route",
            "status_after_gate": "false_for_current_routes",
            "reason": "Doubled, owner-connection, solder, and boundary/topological backups have failed as derivations.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "claim": "Local GR is derived",
            "status_after_gate": "false",
            "reason": "The branch must be labelled explicit closure-only until a new parent mechanism is found.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "claim": "The wider MTS programme is dead",
            "status_after_gate": "false",
            "reason": "This demotes one local transition-safety route; empirical and other parent routes remain separate pillars.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_improved": "808 tests the last backup and demotes the local transition route to explicit closure-only instead of vague hope.",
            "what_blocks_claim": "No route derives nontrivial q_tr ownership plus exact local metric-nullity plus finite boundary control plus K_perp.",
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
    routes: list[dict[str, object]],
    conditions: list[dict[str, object]],
    contract: list[dict[str, object]],
    next_steps: list[dict[str, object]],
    claims: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in sources)
    prior_ok, prior_detail = validation_file_clean(807)
    row_groups = [sources, routes, conditions, contract, next_steps, claims, summary]
    nonclaim_ok = all_rows_nonclaim(row_groups)
    formalization_count = formalization_change_count()
    backup_failed = any(row["claim"] == "Boundary/topological backup derives transition-shell local safety" and row["status_after_gate"] == "false" for row in claims)
    demotion_set = any(row["closure_item"] == "local_metric_quarantine" and row["claim_status"] == "closure_assumption" for row in contract)
    current_visible = any(row["closure_item"] == "transition_current_visibility" for row in contract)
    public_guard = any(row["closure_item"] == "public_claim_guardrail" for row in contract)
    next_selected = any(row["target"] == NEXT_TARGET for row in next_steps)
    local_false = any(row["claim"] == "Local GR is derived" and row["status_after_gate"] == "false" for row in claims)
    return [
        {"check_id": "V808_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V808_1_prior_807_clean", "result": "pass" if prior_ok else "fail", "detail": prior_detail},
        {"check_id": "V808_2_outputs_scoped", "result": "pass" if all_outputs_scoped() else "fail", "detail": str(POST_CHECKPOINT)},
        {"check_id": "V808_3_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V808_4_backup_failed_recorded", "result": "pass" if backup_failed else "fail", "detail": "boundary/topological backup does not derive local safety"},
        {"check_id": "V808_5_demotion_contract_set", "result": "pass" if demotion_set else "fail", "detail": "local metric branch closure-only"},
        {"check_id": "V808_6_current_visibility_guard", "result": "pass" if current_visible else "fail", "detail": "q_tr remains visible in owner ledger"},
        {"check_id": "V808_7_public_claim_guardrail", "result": "pass" if public_guard else "fail", "detail": "derived local GR claim forbidden"},
        {"check_id": "V808_8_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V808_9_no_local_GR_claim", "result": "pass" if local_false else "fail", "detail": "derived local GR remains false"},
        {"check_id": "V808_10_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V808_11_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def build_doc(
    generated_utc: str,
    sources: list[dict[str, object]],
    routes: list[dict[str, object]],
    conditions: list[dict[str, object]],
    contract: list[dict[str, object]],
    next_steps: list[dict[str, object]],
    claims: list[dict[str, object]],
    summary: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return f"""# 808 - Y5 R10 Boundary-Topological Backup Or Local Transition Demotion

Current result: **the final boundary/topological backup fails as a derivation, so the local transition route is demoted to explicit closure-only**. True topological/exact terms can be bulk metric-null, but this does not also derive generic `q_tr` ownership, finite local boundary/support control, matter GR preservation, and `K_perp` control. The honest status is therefore closure, not derived local GR.

Generated UTC: `{generated_utc}`

## Non-Claim Summary

{markdown_table(summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim"])}

## Route Candidates

{markdown_table(routes, ["route", "ansatz", "bulk_metric_response", "ownership", "decision", "reason", "valid_for_claim"])}

## Theorem Conditions

{markdown_table(conditions, ["condition", "required_statement", "status", "gap", "valid_for_claim"])}

## Demotion Contract

{markdown_table(contract, ["closure_item", "statement", "claim_status", "promotion_condition", "valid_for_claim"])}

## Next Steps

{markdown_table(next_steps, ["priority", "next_step", "purpose", "target", "valid_for_claim"])}

## Claim Status

{markdown_table(claims, ["claim", "status_after_gate", "reason", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## What Failed

The last backup needed all of:

```text
delta S_boundary_topological / delta g_loc = 0
nabla_mu K_A^{{mu nu}} = -q_A^nu for generic transition current
finite boundary/support response = 0 or <= 4.212667126774669e-17
matter remains GR/Newton
K_perp is absent, boundary/gauge, higher-order, or bounded
```

The backup can satisfy the first item formally in special exact/topological language, but not the full package. Once defects, surfaces, or support terms are added to own nonzero `q_tr`, the local boundary response must be controlled, and no such parent theorem exists.

## Closure Rule Now Installed

```text
q_metric,loc^nu = 0 is a closure assumption, not a parent theorem.
q_tr^nu remains visible in an owner/global ledger.
Solar/local predictions use GR plus ordinary matter response unless replaced by a future parent theorem.
Galaxy/cosmology tests remain allowed empirical pillars, but cannot prove the local GR reduction.
```

## Verdict

This is grim for this local transition route, but good for the programme discipline. We now stop spending derivation energy on a route that has failed every tested escape hatch. The next useful step is to write the local transition closure contract and testing-shift map so the framework can keep moving without overclaiming.

## Next Target

`{NEXT_TARGET}`
"""


def write_outputs() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    routes = route_candidate_rows(generated_utc)
    conditions = theorem_condition_rows(generated_utc)
    contract = demotion_contract_rows(generated_utc)
    next_steps = next_step_rows(generated_utc)
    claims = claim_status_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validations = validation_rows(sources, routes, conditions, contract, next_steps, claims, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CANDIDATES_PATH, routes, ["route", "ansatz", "bulk_metric_response", "ownership", "decision", "reason", "valid_for_claim", "generated_utc"])
    write_csv(THEOREM_CONDITIONS_PATH, conditions, ["condition", "required_statement", "status", "gap", "valid_for_claim", "generated_utc"])
    write_csv(DEMOTION_CONTRACT_PATH, contract, ["closure_item", "statement", "claim_status", "promotion_condition", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_STEPS_PATH, next_steps, ["priority", "next_step", "purpose", "target", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_STATUS_PATH, claims, ["claim", "status_after_gate", "reason", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validations, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        build_doc(generated_utc, sources, routes, conditions, contract, next_steps, claims, summary, validations),
        encoding="utf-8",
    )

    failed_checks = [row for row in validations if row["result"] != "pass"]
    if failed_checks:
        failed_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed_checks)
        raise SystemExit(f"808 validation failed: {failed_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    write_outputs()
