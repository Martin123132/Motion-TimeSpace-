from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "842-Y5-R10-doubled-open-system-metric-null-theorem-or-closure-demotion.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_842_SOURCE_REGISTER.csv"
ROUTE_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_842_METRIC_NULL_ROUTE_AUDIT.csv"
STATUS_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_842_DERIVATION_STATUS_LEDGER.csv"
CLOSURE_GATE_PATH = RESIDUALS / "P8_Y5_R10_842_CLOSURE_DEMOTION_GATE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_842_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_842_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_842_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_842_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_842_VALIDATION.csv"

STATUS = "Y5_R10_842_doubled_metric_null_and_backups_fail_local_transition_closure_only_nonclaim"
CLAIM_CEILING = "local_transition_closure_only_no_derived_local_GR_or_PPN_pass"
NEXT_TARGET = "843-Y5-R10-testing-readiness-and-GR-limit-map.md"

SOURCE_SPECS = [
    {
        "source_id": "841_doc",
        "path": POST_CHECKPOINT / "841-Y5-R10-quarantine-projector-parent-origin-or-far-local-closure-label.md",
        "needles": [
            "The selected next route is a doubled open-system metric-null theorem",
            "far_local_conditional_plus_quarantine_contract_only",
            "842-Y5-R10-doubled-open-system-metric-null-theorem-or-closure-demotion.md",
        ],
        "role": "immediate doubled-route handoff and closure label",
    },
    {
        "source_id": "841_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_841_VALIDATION.csv",
        "needles": [
            "V841_5_doubled_route_selected,pass",
            "V841_7_all_rows_nonclaim,pass",
            "V841_9_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "140_doubled_open_system",
        "path": FORMALIZATION / "140-doubled-open-system-metric-null-theorem.md",
        "needles": [
            "Private ruthless status: pure doubled route fails. A hybrid route remains open.",
            "pure doubled route failed D2 and D5;",
            "hybrid owner-connection route is the next test.",
        ],
        "role": "pure doubled/open-system metric-null theorem gate",
    },
    {
        "source_id": "141_owner_current_primitive",
        "path": FORMALIZATION / "141-doubled-owner-connection-current-primitive.md",
        "needles": [
            "Private ruthless status: primitive candidate exists; projection theorem missing.",
            "metric-independent primitive exists formally;",
            "spacetime projection without metric variation = not derived;",
        ],
        "role": "owner-connection current primitive gate",
    },
    {
        "source_id": "142_solder_map",
        "path": FORMALIZATION / "142-owner-spacetime-solder-map-theorem.md",
        "needles": [
            "Private ruthless status: bulk hybrid route fails as a derivation.",
            "the bulk hybrid route fails; only boundary/topological backup remains before",
            "143-boundary-topological-backup-gate.md",
        ],
        "role": "owner-spacetime solder map gate",
    },
    {
        "source_id": "143_boundary_topological_backup",
        "path": FORMALIZATION / "143-boundary-topological-backup-gate.md",
        "needles": [
            "Private ruthless status: the backup fails as a derivation.",
            "local GR recovery is an explicit closure/guardrail, not a derived theorem",
            "144-local-transition-closure-contract.md",
        ],
        "role": "boundary/topological backup gate",
    },
    {
        "source_id": "144_local_transition_closure_contract",
        "path": FORMALIZATION / "144-local-transition-closure-contract.md",
        "needles": [
            "Private ruthless status: local transition safety is closure-only unless a future",
            "MTS local-GR derivation = not achieved;",
            "145-testing-readiness-and-gr-limit-map.md",
        ],
        "role": "local transition closure contract and testing-readiness handoff",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def route_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "R842_0_pure_doubled",
            "route": "pure doubled open-system action",
            "attempted_proof": "derive Sigma_metric[q_tr]=0 from doubled exchange-current structure",
            "result": "fail",
            "blocking_clause": "D2 hidden metric dependence and D5 owner-stress guard fail",
            "surviving_value": "useful open-system bookkeeping and exchange-current language",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "R842_1_owner_current_primitive",
            "route": "owner-connection current primitive",
            "attempted_proof": "write transition balance in owner geometry without local metric covariant derivative",
            "result": "candidate_only",
            "blocking_clause": "metric-independent primitive exists formally but projection back to spacetime is not derived",
            "surviving_value": "moves the obstruction from q_tr itself to the owner-spacetime solder map",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "R842_2_solder_map",
            "route": "owner-spacetime solder/projection theorem",
            "attempted_proof": "project owner-current primitive into spacetime without reintroducing metric variation",
            "result": "fail",
            "blocking_clause": "metric tetrad solder reintroduces Sigma_metric; independent/fixed solder needs new geometry or breaks covariance",
            "surviving_value": "identifies boundary/topological backup as the only remaining metric-null route",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "R842_3_boundary_topological_backup",
            "route": "boundary/topological backup",
            "attempted_proof": "make transition ownership a boundary, superpotential, topological, or Ward-inflow term with zero local bulk metric response",
            "result": "fail",
            "blocking_clause": "nontrivial q_tr ownership, finite boundary terms, support/locality, and matter-response silence are not derived",
            "surviving_value": "true topological/exact blocks can be metric-null in form language, but do not currently own generic q_tr",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "R842_4_closure_contract",
            "route": "local transition closure contract",
            "attempted_proof": "replace the failed route with an explicit guardrail while preserving testability",
            "result": "closure_only",
            "blocking_clause": "local transition safety remains imposed unless a future parent theorem replaces the closure",
            "surviving_value": "MTS as fundamental theory candidate remains open; empirical testing allowed but cannot substitute for GR-limit derivation",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def status_ledger_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "S842_0_sigma_metric",
            "object": "Sigma_metric[q_tr]=0",
            "current_status": "not_derived",
            "reason": "pure doubled route fails and projection/backups do not eliminate the local metric response",
            "allowed_use": "theorem target or explicit closure assumption only",
            "forbidden_use": "derived local PPN safety",
            "exit_condition": "parent action proves zero metric response while matter still produces GR/Newton",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "status_id": "S842_1_Rloc_kernel",
            "object": "R_loc q_tr=0",
            "current_status": "not_derived",
            "reason": "R_loc depends on source lift/action block that no current route signs",
            "allowed_use": "response-kernel notation and nonclaim smoke tests",
            "forbidden_use": "claim projector parent origin",
            "exit_condition": "derive R_loc and source lift from parent variation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "status_id": "S842_2_local_transition_branch",
            "object": "local transition branch",
            "current_status": "explicit_closure_only",
            "reason": "pure doubled, owner-current, solder-map, and boundary/topological derivation routes all fail in the current corpus",
            "allowed_use": "guardrail for testing and bookkeeping with the closure label attached",
            "forbidden_use": "fundamental local-GR derivation claim",
            "exit_condition": "future parent theorem replaces the closure with a derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "status_id": "S842_3_empirical_work",
            "object": "galaxy/cosmology/EM/local tests",
            "current_status": "allowed_non_substitutive",
            "reason": "empirical viability can be tested, but it does not prove local GR reduction",
            "allowed_use": "robustness gates and baseline comparisons",
            "forbidden_use": "letting fits stand in for the missing theorem",
            "exit_condition": "testing-readiness map separates empirical pillars from GR-limit obligations",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def closure_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CD842_0_demote_transition_shell",
            "gate": "transition shell local-GR status",
            "condition": "all current metric-null derivation routes fail or remain unsigned",
            "result": "demote_to_explicit_closure_only",
            "closure_label": "local_transition_closure_only",
            "what_remains_open": "future parent action could still derive the same guardrail",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CD842_1_keep_far_local",
            "gate": "far-local conditional branch",
            "condition": "far-local U_B^2 suppression plumbing is separate from transition shell derivation",
            "result": "retain_as_conditional_nonclaim",
            "closure_label": "conditional_U_B2_suppression_plumbing_only",
            "what_remains_open": "coefficient sourcing and local bound data can still be tested",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CD842_2_testing_path",
            "gate": "testing readiness",
            "condition": "local-GR derivation missing but empirical branches are testable",
            "result": "move_to_testing_readiness_and_GR_limit_map",
            "closure_label": "empirical_tests_allowed_not_derivation",
            "what_remains_open": "define which tests are allowed now and which require the future parent theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG842_0_no_sigma_metric_claim",
            "claim": "Sigma_metric[q_tr]=0 is derived",
            "status": "forbidden",
            "reason": "the pure doubled route fails and neither owner-current nor backup routes close the projection problem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG842_1_no_local_GR_claim",
            "claim": "MTS locally reduces to GR/Newton through the transition-shell route",
            "status": "forbidden",
            "reason": "local transition safety is explicit closure-only in the current corpus",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG842_2_no_empirical_substitution",
            "claim": "successful galaxy/cosmology/EM fits prove the missing local-GR theorem",
            "status": "forbidden",
            "reason": "empirical testing is allowed but cannot substitute for the parent reduction proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG842_3_allowed_private_result",
            "claim": "current local transition branch is closure-only and must be tested separately from the future GR-limit theorem",
            "status": "allowed_private_nonclaim",
            "reason": "this is a discipline label and next-step map, not a public physics claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D842_0",
            "finding": "pure doubled metric-null theorem fails",
            "reason": "D2/D5 failures prevent deriving Sigma_metric[q_tr]=0",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D842_1",
            "finding": "hybrid owner-current route fails as a bulk derivation",
            "reason": "metric-independent current primitive cannot be projected to spacetime without an unsigned solder map",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D842_2",
            "finding": "boundary/topological backup fails as a derivation",
            "reason": "generic q_tr ownership and finite boundary/support control are not derived",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D842_3",
            "finding": "local transition branch is closure-only",
            "reason": "the current parent corpus does not derive local transition safety",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "separate what can be tested now from what still needs a parent GR-limit theorem",
            "include": "empirical branch list, GR-limit obligations, local closure label propagation, baseline comparisons, nonclaim status",
            "exclude": "public local-GR claim, hiding q_tr closure, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "collapsed the doubled, owner-current, solder-map, and boundary/topological routes into an explicit closure-only status for the local transition branch",
            "what_is_not_claimed": "derived Sigma_metric[q_tr]=0, R_loc q_tr=0, local PPN safety, local GR/Newton recovery",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_valid_for_claim_false(row_groups: list[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if row.get("valid_for_claim") != "false":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    status_rows: list[dict[str, object]],
    closure_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_841_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    route_ids = {row["route_id"] for row in route_rows}
    route_complete = route_ids == {
        "R842_0_pure_doubled",
        "R842_1_owner_current_primitive",
        "R842_2_solder_map",
        "R842_3_boundary_topological_backup",
        "R842_4_closure_contract",
    }
    pure_fail = any(row["route_id"] == "R842_0_pure_doubled" and row["result"] == "fail" for row in route_rows)
    hybrid_fail = any(row["route_id"] == "R842_2_solder_map" and row["result"] == "fail" for row in route_rows)
    backup_fail = any(row["route_id"] == "R842_3_boundary_topological_backup" and row["result"] == "fail" for row in route_rows)
    closure_only = any(row["current_status"] == "explicit_closure_only" for row in status_rows)
    demotion_gate = any(row["result"] == "demote_to_explicit_closure_only" for row in closure_rows)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    guard_forbidden = all(row["status"] != "allowed_public_claim" for row in guard_rows)
    nonclaim_ok = all_valid_for_claim_false([source_rows, route_rows, status_rows, closure_rows, guard_rows, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V842_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V842_1_prior_841_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V842_2_route_audit_complete",
            "result": "pass" if route_complete else "fail",
            "detail": "pure doubled, owner primitive, solder map, boundary backup, and closure contract recorded",
        },
        {
            "check_id": "V842_3_pure_doubled_fail_recorded",
            "result": "pass" if pure_fail else "fail",
            "detail": "pure doubled route fails D2/D5 and does not derive Sigma_metric[q_tr]=0",
        },
        {
            "check_id": "V842_4_hybrid_solder_fail_recorded",
            "result": "pass" if hybrid_fail else "fail",
            "detail": "bulk owner-current/solder-map hybrid fails as a derivation",
        },
        {
            "check_id": "V842_5_boundary_backup_fail_recorded",
            "result": "pass" if backup_fail else "fail",
            "detail": "boundary/topological backup fails as a derivation",
        },
        {
            "check_id": "V842_6_closure_only_installed",
            "result": "pass" if closure_only and demotion_gate else "fail",
            "detail": "local transition branch demoted to explicit closure-only",
        },
        {
            "check_id": "V842_7_no_local_GR_claim",
            "result": "pass" if no_claim and guard_forbidden else "fail",
            "detail": "no local-GR, PPN, Sigma_metric, or empirical-substitution claim allowed",
        },
        {
            "check_id": "V842_8_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V842_9_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V842_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V842_11_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]


def csv_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_document(
    source_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    status_rows: list[dict[str, object]],
    closure_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 842 - Y5 R10 Doubled Open-System Metric-Null Theorem Or Closure Demotion",
        "",
        "Current result: **the doubled/open-system metric-null route does not derive local transition safety in the current corpus**. The pure doubled route fails, the owner-current primitive remains projection-limited, the owner-spacetime solder map fails as a bulk derivation, and the boundary/topological backup also fails as a derivation. The honest status is now `local_transition_closure_only_no_derived_local_GR_or_PPN_pass`: usable as a private guardrail and testing discipline, not as a GR-limit theorem.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Metric-Null Route Audit",
        "",
        csv_table(route_rows, ["route_id", "route", "attempted_proof", "result", "blocking_clause", "surviving_value", "claim_allowed", "valid_for_claim"]),
        "",
        "## Derivation Status Ledger",
        "",
        csv_table(status_rows, ["status_id", "object", "current_status", "reason", "allowed_use", "forbidden_use", "exit_condition", "valid_for_claim"]),
        "",
        "## Closure Demotion Gate",
        "",
        csv_table(closure_rows, ["gate_id", "gate", "condition", "result", "closure_label", "what_remains_open", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        csv_table(guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim"]),
        "",
        "## Decision",
        "",
        csv_table(decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        csv_table(next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        csv_table(validation, ["check_id", "result", "detail"]),
        "",
    ]
    OUTPUT_DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    source_rows = source_register_rows(generated_utc)
    route_rows = route_audit_rows(generated_utc)
    status_rows = status_ledger_rows(generated_utc)
    closure_rows = closure_gate_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, route_rows, status_rows, closure_rows, guard_rows, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_AUDIT_PATH, route_rows, ["route_id", "route", "attempted_proof", "result", "blocking_clause", "surviving_value", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(STATUS_LEDGER_PATH, status_rows, ["status_id", "object", "current_status", "reason", "allowed_use", "forbidden_use", "exit_condition", "valid_for_claim", "generated_utc"])
    write_csv(CLOSURE_GATE_PATH, closure_rows, ["gate_id", "gate", "condition", "result", "closure_label", "what_remains_open", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, route_rows, status_rows, closure_rows, guard_rows, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
