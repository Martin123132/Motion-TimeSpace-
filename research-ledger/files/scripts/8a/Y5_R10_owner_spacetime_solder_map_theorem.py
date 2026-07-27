from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "807-Y5-R10-owner-spacetime-solder-map-theorem.md"
NEXT_TARGET = "808-Y5-R10-boundary-topological-backup-or-local-transition-demotion.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_807_SOURCE_REGISTER.csv"
SOLDER_CANDIDATES_PATH = RESIDUALS / "P8_Y5_R10_807_SOLDER_CANDIDATES.csv"
THEOREM_CONDITIONS_PATH = RESIDUALS / "P8_Y5_R10_807_THEOREM_CONDITIONS.csv"
BACKUP_ROUTES_PATH = RESIDUALS / "P8_Y5_R10_807_BACKUP_ROUTES.csv"
DECISION_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_807_DECISION_LEDGER.csv"
CLAIM_STATUS_PATH = RESIDUALS / "P8_Y5_R10_807_CLAIM_STATUS.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_807_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_807_VALIDATION.csv"

STATUS = "Y5_R10_807_owner_spacetime_solder_bulk_hybrid_fails_boundary_topological_backup_open_nonclaim"
CLAIM_CEILING = "bulk_solder_theorem_rejected_backup_open_no_derived_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

RUN_142 = FORMALIZATION / "runs" / "20260528-192230-owner-spacetime-solder-map-theorem"

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    SOLDER_CANDIDATES_PATH,
    THEOREM_CONDITIONS_PATH,
    BACKUP_ROUTES_PATH,
    DECISION_LEDGER_PATH,
    CLAIM_STATUS_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "806_doc",
        "path": POST_CHECKPOINT / "806-Y5-R10-transition-source-lift-action-block-gate.md",
        "needles": ["owner_spacetime_solder_map", "metric_null_solder_variation", "807-Y5-R10-owner-spacetime-solder-map-theorem.md"],
        "role": "immediate 806 solder-map target",
    },
    {
        "source_id": "806_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_806_VALIDATION.csv",
        "needles": ["V806_7_owner_solder_route_selected,pass", "V806_9_no_local_GR_claim,pass"],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "formal_142_doc",
        "path": FORMALIZATION / "142-owner-spacetime-solder-map-theorem.md",
        "needles": [
            "owner_spacetime_solder_map_bulk_hybrid_fails_boundary_topological_backup_open",
            "metric tetrad route = reintroduces metric",
            "boundary/topological backup remains open",
        ],
        "role": "earlier owner-spacetime solder-map gate",
    },
    {
        "source_id": "run_142_summary",
        "path": RUN_142 / "summary.csv",
        "needles": ["owner_spacetime_solder_map_bulk_hybrid_fails_boundary_topological_backup_open", "next_test_boundary_topological_backup_or_demote", "False,False,True"],
        "role": "solder-map machine summary",
    },
    {
        "source_id": "run_142_solder_candidates",
        "path": RUN_142 / "results" / "solder_candidates.csv",
        "needles": ["metric_tetrad_solder", "fixed_background_solder", "boundary_superpotential_solder", "Ward_gauge_solder"],
        "role": "solder candidate table",
    },
    {
        "source_id": "run_142_gate_criteria",
        "path": RUN_142 / "results" / "gate_criteria.csv",
        "needles": ["metric_tetrad_route,fail_reintroduces_metric", "boundary_topological_backup,open_next_backup", "derived_local_GR,fail"],
        "role": "solder theorem gate criteria",
    },
    {
        "source_id": "run_142_claim_status",
        "path": RUN_142 / "results" / "claim_status_after_gate.csv",
        "needles": ["Owner-spacetime solder map is derived.,false", "Boundary/topological backup remains open.,true", "Derived local GR through transition shells.,false"],
        "role": "claim status after solder gate",
    },
    {
        "source_id": "spine_142",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["owner_spacetime_solder_map_bulk_hybrid_fails_boundary_topological_backup_open", "backup is the only remaining route", "143-boundary-topological-backup-gate.md"],
        "role": "spine result and next branch",
    },
    {
        "source_id": "red_142",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["owner_spacetime_solder_map_bulk_hybrid_fails_boundary_topological_backup_open.", "bulk hybrid fails; boundary/topological backup only."],
        "role": "red-team result",
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


def solder_candidate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "candidate": "metric_tetrad_solder",
            "map": "q_A^nu=e_I^nu(g_loc)s_A^I; K_A^{mu nu}=e_I^mu e_J^nu k_A^{IJ}",
            "covariance": "strong",
            "metric_nullity": "fail",
            "decision": "reject_bulk_route",
            "reason": "A solder tied to g_loc varies with the local metric and reintroduces Sigma_metric.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate": "independent_coframe_solder",
            "map": "q_A^nu=E_I^nu s_A^I with E independent of g_loc",
            "covariance": "possible",
            "metric_nullity": "formal_candidate_not_sufficient",
            "decision": "requires_new_stress_null_theorem",
            "reason": "The coframe becomes extra geometry whose stress and relation to g_loc must be controlled.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate": "fixed_background_solder",
            "map": "q_A^nu=E0_I^nu s_A^I",
            "covariance": "fail",
            "metric_nullity": "formal_but_cheating",
            "decision": "reject_covariance_cheat",
            "reason": "It avoids variation by introducing fixed background structure.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate": "density_projection",
            "map": "mathcal{q}_A^nu=mathcal{E}_I^nu s_A^I as a vector density",
            "covariance": "partial",
            "metric_nullity": "incomplete",
            "decision": "insufficient",
            "reason": "It still needs conversion to tensor balance or observable spacetime conservation.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate": "boundary_superpotential_solder",
            "map": "K_A^{mu nu}=nabla_rho U_A^{rho mu nu} or exterior-form boundary projection",
            "covariance": "strong_if_derived",
            "metric_nullity": "backup_open",
            "decision": "send_to_next_backup_gate",
            "reason": "Can be locally bulk-null if exact, but support and finite boundary terms must be controlled.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate": "Ward_gauge_solder",
            "map": "metric variation of solder projection is pure gauge by identity",
            "covariance": "strong_if_symmetry_exists",
            "metric_nullity": "open_no_symmetry",
            "decision": "backup_inside_next_gate",
            "reason": "Would solve the issue if a transition Ward identity existed; none is currently derived.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def theorem_condition_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "condition": "spacetime_vector_projection",
            "required_statement": "q_A^nu=E_I^nu s_A^I transforms as a spacetime vector.",
            "status": "requires_solder",
            "gap": "Metric-independent solder is extra geometric structure.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition": "metric_null_variation",
            "required_statement": "delta E_I^nu/delta g_loc=0 or variation is boundary/gauge/PPN-null.",
            "status": "not_derived",
            "gap": "Tetrad route fails; independent route needs a new stress/null theorem.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition": "spacetime_conservation_recovery",
            "required_statement": "D_A J_A+s_A=0 projects to nabla_mu K_A^{mu nu}+q_A^nu=0.",
            "status": "not_derived",
            "gap": "Using nabla_mu(g_loc) in projection can reintroduce the metric.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition": "no_fixed_background_cheat",
            "required_statement": "Solder map is dynamical/covariant or gauge-fixed from parent variables, not absolute background.",
            "status": "required",
            "gap": "Fixed solder avoids variation by sacrificing covariance.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition": "owner_solder_stress_control",
            "required_statement": "E/Pi owner-solder sector has zero, boundary/gauge, or PPN-null stress.",
            "status": "not_derived",
            "gap": "Independent coframe can itself gravitate locally.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition": "exact_or_hard_bound",
            "required_statement": "local metric response from solder <=4.212667126774669e-17 if not exactly zero.",
            "status": "not_met",
            "gap": "No estimate or identity supplies the transition-shell bound.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def backup_route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "backup": "boundary_superpotential",
            "target": "owner current projects only through local-boundary/superpotential terms with zero bulk PPN source",
            "why_it_remains": "It can avoid bulk solder stress if exact.",
            "risk": "finite boundary terms and support conditions may fail",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "backup": "topological_density",
            "target": "transition ownership is an exact/topological identity with no metric variation",
            "why_it_remains": "Topological terms can be metric-null.",
            "risk": "may not generate nontrivial owner equations or observable constraints",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "backup": "Ward_gauge_null",
            "target": "symmetry makes solder variation pure gauge",
            "why_it_remains": "Would be strongest if found.",
            "risk": "no such symmetry currently exists",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_ledger_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D807_0_bulk_tetrad",
            "question": "Can the metric/tetrad solder derive metric-nullity?",
            "answer": "No. It reintroduces g_loc variation and Sigma_metric.",
            "status": "bulk_route_fail",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D807_1_fixed_solder",
            "question": "Can a fixed solder avoid metric variation?",
            "answer": "Only by breaking field-theory covariance.",
            "status": "covariance_cheat_rejected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D807_2_independent_coframe",
            "question": "Can independent coframe solder save the bulk hybrid?",
            "answer": "Not yet. It becomes new geometry needing its own stress-null theorem.",
            "status": "insufficient_without_new_theorem",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D807_3_backup",
            "question": "What route remains?",
            "answer": "Boundary/topological/Ward backup: exact local bulk-null ownership or demote the branch.",
            "status": "boundary_topological_backup_open",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_status_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "claim": "Owner-spacetime solder map is derived",
            "status_after_gate": "false",
            "reason": "Every bulk solder candidate either reintroduces metric variation, breaks covariance, or requires another theorem.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "claim": "Bulk doubled owner-connection hybrid derives local safety",
            "status_after_gate": "false",
            "reason": "It stalls at the solder/projection map.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "claim": "Boundary/topological backup remains open",
            "status_after_gate": "true_backup",
            "reason": "A boundary/topological projection could avoid bulk metric stress if exact.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "claim": "Derived local GR through transition shells",
            "status_after_gate": "false",
            "reason": "No solder theorem or backup theorem has passed.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_improved": "807 closes the bulk owner-solder route as a derivation and leaves only boundary/topological/Ward backup.",
            "what_blocks_claim": "No owner-spacetime solder map is parent-derived; Sigma_metric[q_tr]=0 is not derived; local GR remains false.",
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
    backups: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in sources)
    prior_ok, prior_detail = validation_file_clean(806)
    row_groups = [sources, candidates, conditions, backups, decisions, claims, summary]
    nonclaim_ok = all_rows_nonclaim(row_groups)
    formalization_count = formalization_change_count()
    tetrad_fail = any(row["candidate"] == "metric_tetrad_solder" and row["metric_nullity"] == "fail" for row in candidates)
    fixed_fail = any(row["candidate"] == "fixed_background_solder" and row["decision"] == "reject_covariance_cheat" for row in candidates)
    independent_insufficient = any(row["candidate"] == "independent_coframe_solder" and row["decision"] == "requires_new_stress_null_theorem" for row in candidates)
    backup_open = any(row["backup"] == "boundary_superpotential" for row in backups) and any(row["status_after_gate"] == "true_backup" for row in claims)
    local_false = any(row["claim"] == "Derived local GR through transition shells" and row["status_after_gate"] == "false" for row in claims)
    return [
        {"check_id": "V807_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V807_1_prior_806_clean", "result": "pass" if prior_ok else "fail", "detail": prior_detail},
        {"check_id": "V807_2_outputs_scoped", "result": "pass" if all_outputs_scoped() else "fail", "detail": str(POST_CHECKPOINT)},
        {"check_id": "V807_3_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V807_4_tetrad_solder_rejected", "result": "pass" if tetrad_fail else "fail", "detail": "metric/tetrad solder reintroduces g_loc"},
        {"check_id": "V807_5_fixed_solder_rejected", "result": "pass" if fixed_fail else "fail", "detail": "fixed solder is covariance cheat"},
        {"check_id": "V807_6_independent_coframe_insufficient", "result": "pass" if independent_insufficient else "fail", "detail": "independent coframe needs stress-null theorem"},
        {"check_id": "V807_7_boundary_topological_backup_open", "result": "pass" if backup_open else "fail", "detail": NEXT_TARGET},
        {"check_id": "V807_8_no_local_GR_claim", "result": "pass" if local_false else "fail", "detail": "derived local GR remains false"},
        {"check_id": "V807_9_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V807_10_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def build_doc(
    generated_utc: str,
    sources: list[dict[str, object]],
    candidates: list[dict[str, object]],
    conditions: list[dict[str, object]],
    backups: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    summary: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return f"""# 807 - Y5 R10 Owner-Spacetime Solder Map Theorem

Current result: **bulk owner-solder does not derive local safety**. The metric/tetrad solder is covariant but reintroduces `g_loc`; the fixed solder avoids variation only by cheating covariance; the independent coframe is a new geometry that needs its own stress-null theorem. So the owner-connection hybrid fails as a derivation. The only route still open is a boundary/topological/Ward backup with exact local bulk-null response.

Generated UTC: `{generated_utc}`

## Non-Claim Summary

{markdown_table(summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim"])}

## Solder Candidates

{markdown_table(candidates, ["candidate", "map", "covariance", "metric_nullity", "decision", "reason", "valid_for_claim"])}

## Theorem Conditions

{markdown_table(conditions, ["condition", "required_statement", "status", "gap", "valid_for_claim"])}

## Backup Routes

{markdown_table(backups, ["backup", "target", "why_it_remains", "risk", "next_target", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decisions, ["decision_id", "question", "answer", "status", "next_target", "valid_for_claim"])}

## Claim Status

{markdown_table(claims, ["claim", "status_after_gate", "reason", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## Solder-Map Result

The owner primitive wanted:

```text
D_A J_A^I + s_A^I = 0
q_A^nu = E_I^nu s_A^I
K_A^{{mu nu}} = Pi^{{mu nu}}_I J_A^I
```

For this to solve the local branch, the solder/projection map had to satisfy:

```text
delta E_I^nu / delta g_loc = 0
projection(D_A J_A+s_A=0) -> nabla_mu K_A^{{mu nu}}+q_A^nu=0
no fixed-background covariance cheat
no new owner-solder stress above local PPN bounds
```

That exact package is not derived. The bulk hybrid route has therefore failed as a derivation.

## Verdict

This is not a collapse of the whole framework. It is the local transition route being forced into honesty. The surviving option is now very narrow: boundary/topological/Ward ownership with zero local bulk metric response, controlled finite boundary/support terms, nontrivial owner balance, and matter GR preserved. If that fails, the transition-shell local branch has to become explicit closure-only while testing continues elsewhere.

## Next Target

`{NEXT_TARGET}`
"""


def write_outputs() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    candidates = solder_candidate_rows(generated_utc)
    conditions = theorem_condition_rows(generated_utc)
    backups = backup_route_rows(generated_utc)
    decisions = decision_ledger_rows(generated_utc)
    claims = claim_status_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validations = validation_rows(sources, candidates, conditions, backups, decisions, claims, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(SOLDER_CANDIDATES_PATH, candidates, ["candidate", "map", "covariance", "metric_nullity", "decision", "reason", "valid_for_claim", "generated_utc"])
    write_csv(THEOREM_CONDITIONS_PATH, conditions, ["condition", "required_statement", "status", "gap", "valid_for_claim", "generated_utc"])
    write_csv(BACKUP_ROUTES_PATH, backups, ["backup", "target", "why_it_remains", "risk", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_LEDGER_PATH, decisions, ["decision_id", "question", "answer", "status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_STATUS_PATH, claims, ["claim", "status_after_gate", "reason", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validations, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        build_doc(generated_utc, sources, candidates, conditions, backups, decisions, claims, summary, validations),
        encoding="utf-8",
    )

    failed_checks = [row for row in validations if row["result"] != "pass"]
    if failed_checks:
        failed_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed_checks)
        raise SystemExit(f"807 validation failed: {failed_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    write_outputs()
