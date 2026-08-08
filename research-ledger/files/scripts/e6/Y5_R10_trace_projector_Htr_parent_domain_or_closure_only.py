from __future__ import annotations

import csv
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_906_trace_projector_Htr_parent_domain_attempt_failed_finite_trace_alpha_demoted_closure_only_nonclaim"
CLAIM_CEILING = "Ptr_Htr_parent_domain_audit_and_closure_only_demotion_no_numeric_alpha_no_R10_no_local_GR_claim"
NEXT_TARGET = "907-Y5-R10-post-trace-closure-local-GR-residual-stack-priority.md"
ANCHOR_BOUND_FILE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_904_SOURCE_BACKED_ANCHORS_NONCLAIM.csv"
R10_DRY_RUN_DIR = OUT / "P8_Y5_R10_906_R10_CLOSURE_DRY_RUNNER_RESULTS"

MTS_REQUIRED_COLUMNS = [
    "model_id",
    "branch_id",
    "curve_id",
    "lambda_value",
    "lambda_units",
    "alpha_predicted",
    "alpha_bound",
    "alpha_bound_source",
    "force_law_form",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]

SOURCE_SPECS = [
    {
        "source_id": "905_doc",
        "path": ROOT / "905-Y5-R10-parent-finite-alpha-input-owner-or-digitized-bound-curve-worker.md",
        "needle": "P_tr/H_tr -> Z_tr",
        "role": "immediate parent-alpha root-owner handoff",
    },
    {
        "source_id": "905_validation",
        "path": OUT / "P8_Y5_BRR545_905_VALIDATION.csv",
        "needle": "V905_12_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "878_projector_construction",
        "path": OUT / "P8_Y5_R10_878_FORMAL_PROJECTOR_CONSTRUCTION.csv",
        "needle": "PC878_3_projector",
        "role": "formal P_tr construction and missing-owner status",
    },
    {
        "source_id": "878_rank_test",
        "path": OUT / "P8_Y5_R10_878_CONSTRAINT_RANK_TEST.csv",
        "needle": "RT878_4_rank_verdict",
        "role": "rank-zero/no-pole/source-cokernel gate",
    },
    {
        "source_id": "879_covector_audit",
        "path": OUT / "P8_Y5_R10_879_COVECTOR_SOURCE_AUDIT.csv",
        "needle": "CV879_4_covector_verdict",
        "role": "ell_tr parent covector audit",
    },
    {
        "source_id": "879_pairing_audit",
        "path": OUT / "P8_Y5_R10_879_PAIRING_SOURCE_AUDIT.csv",
        "needle": "KP879_4_pairing_verdict",
        "role": "K_parent/pseudo-inverse pairing audit",
    },
    {
        "source_id": "880_action_contract",
        "path": OUT / "P8_Y5_R10_880_MINIMAL_ACTION_CONTRACT.csv",
        "needle": "MAC880_4_parent_pairing_extension",
        "role": "endpoint action contract and missing K_parent extension",
    },
    {
        "source_id": "886_zero_pole_theorem",
        "path": OUT / "P8_Y5_R10_886_ZERO_POLE_IMPLICATION_THEOREM.csv",
        "needle": "ZP886_6_verdict",
        "role": "conditional zero-pole implication theorem",
    },
    {
        "source_id": "887_readout_boundary",
        "path": OUT / "P8_Y5_R10_887_READOUT_BOUNDARY_CLAUSE.csv",
        "needle": "RO887_6_clause_verdict",
        "role": "readout-only/boundary support clause",
    },
    {
        "source_id": "888_parent_spine_integration",
        "path": OUT / "P8_Y5_R10_888_PARENT_SPINE_INTEGRATION.csv",
        "needle": "PSI888_5_integration_verdict",
        "role": "parent-spine integration failure",
    },
    {
        "source_id": "890_no_tail",
        "path": OUT / "P8_Y5_R10_890_BOUNDARY_NO_TAIL_THEOREM_ATTEMPT.csv",
        "needle": "NT890_5_no_tail_corollary",
        "role": "boundary no-tail theorem attempt",
    },
    {
        "source_id": "891_source_rows",
        "path": OUT / "P8_Y5_R10_891_TRACE_COEFFICIENT_SOURCE_ROWS.csv",
        "needle": "TCSR891_0_Ztr",
        "role": "finite trace coefficient source rows",
    },
    {
        "source_id": "r10_runner",
        "path": ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py",
        "needle": "MTS_REQUIRED_COLUMNS",
        "role": "R10 comparator refusal gate",
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
            "what_changed": "attempted the P_tr/H_tr parent-domain route and demoted the finite trace alpha branch to closure-only because the root owner is still missing",
            "best_partial_result": "the exact failure is now isolated: ell_tr is not a parent covector, K_parent is not a parent pairing, and the readout/no-pole route is not parent-integrated",
            "hard_blockers": "Q_trace/Q_* ownership, K_parent constrained pseudo-inverse, P_tr local support class, H_tr second variation, rank-zero/no-pole signatures, matter/source-cokernel, and boundary no-tail",
            "what_is_not_claimed": "P_tr/H_tr ownership, no local trace pole, Q_tr=0, finite alpha_tr(lambda), R10 pass, or local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def ptr_htr_parent_domain_test_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "PHD906_0_elltr_covector",
            "ell_tr=DQ_trace",
            "Q_trace/Q_* must be a parent readout/coordinate before local scoring",
            "fail_for_claim",
            "879 says Q_trace is named but not parent-owned and Q_* remains missing",
            "P_tr cannot be defined canonically",
        ),
        (
            "PHD906_1_Kparent_pairing",
            "K_parent or constrained pseudo-inverse",
            "parent action must supply a nondegenerate quotient pairing to raise ell_tr",
            "fail_for_claim",
            "879/880 provide endpoint/formal candidates but no full parent K_parent extension",
            "v_tr cannot be normalized without arbitrary choice",
        ),
        (
            "PHD906_2_projector",
            "P_tr=v_tr tensor ell_tr",
            "ell_tr, v_tr, gauge degeneracies, and local support class must be parent-owned",
            "fail_for_claim",
            "878 gives a conditional idempotent formula only",
            "H_tr=P_tr^dagger Hess(S_parent)P_tr is undefined",
        ),
        (
            "PHD906_3_Htr_operator",
            "H_tr=P_tr^dagger Hess(S_parent)P_tr",
            "actual second variation of S_parent must be projected after gauge/constraint reduction",
            "fail_for_claim",
            "877/892/895 give skeletons/templates but no computed parent Hessian",
            "Z_tr, mu_tr^2, and lambda_tr cannot be extracted",
        ),
        (
            "PHD906_4_local_source_domain",
            "rank(P_loc P_tr P_loc^dagger) and source-coupled inverse",
            "compact-local domain and reduced Green-function pole must be tested on the same q_loc/P_loc convention",
            "fail_for_claim",
            "878/886 rank-zero and no-pole tests remain conditional",
            "cannot claim no local trace pole",
        ),
        (
            "PHD906_5_readout_no_tail",
            "readout-only boundary support and no local tail",
            "trace endpoint/readout must be post-variation/source-at-zero and have no compact local tail",
            "fail_for_claim",
            "887/888/890 support the policy shape but do not parent-integrate it",
            "cannot theorem-zero the branch",
        ),
        (
            "PHD906_6_verdict",
            "P_tr/H_tr parent-domain ownership",
            "all PHD906_0 through PHD906_5 must pass",
            "not_parent_owned",
            "multiple upstream failures remain",
            "finite trace alpha must be closure-only until new parent action material exists",
        ),
    ]
    return [
        {
            "test_id": test_id,
            "object": obj,
            "required_parent_signature": requirement,
            "result": result,
            "evidence": evidence,
            "consequence": consequence,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for test_id, obj, requirement, result, evidence, consequence in rows
    ]


def zero_pole_or_finite_field_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "ZPF906_0_finite_field",
            "finite local trace field",
            "requires parent-owned P_tr/H_tr plus Z_tr, mu_tr^2, J_tr, units, boundary conditions",
            "failed_for_now",
            "no numeric alpha branch",
            "closure_only",
        ),
        (
            "ZPF906_1_no_pole",
            "no local source-coupled trace pole",
            "requires rank-zero/readout-only/constraint-null/source-cokernel/no-tail signatures",
            "not_promoted",
            "cannot set lambda_tr absent as a theorem",
            "conditional_watch",
        ),
        (
            "ZPF906_2_source_cokernel",
            "J_tr=0/Q_tr=0",
            "requires matter descent through q_loc, v_tr local verticality, and no-marker constants",
            "not_promoted",
            "cannot set alpha_tr=0",
            "conditional_watch",
        ),
        (
            "ZPF906_3_closure_demotion",
            "finite trace alpha branch",
            "if neither finite field nor no-pole theorem is parent-signed, finite alpha is not a theory output",
            "selected",
            "remove finite trace alpha from claimable empirical branches",
            "closure_only",
        ),
    ]
    return [
        {
            "fork_id": fork_id,
            "branch": branch,
            "promotion_requirement": requirement,
            "current_status": status,
            "empirical_effect": effect,
            "classification": classification,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for fork_id, branch, requirement, status, effect, classification in rows
    ]


def closure_demotion_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "CDR906_0_branch_label",
            "finite_trace_alpha",
            "closure_only_until_parent_Ptr_Htr_or_no_pole_theorem",
            "not part of claimable MTS field theory spine",
            "prevents treating missing coupling as hidden small alpha",
        ),
        (
            "CDR906_1_allowed_use",
            "private diagnostic scaffold",
            "may appear as a blocked source-row schema or future derivation target",
            "must not be used as evidence, fit parameter, or R10 pass",
            "keeps future work recoverable without contaminating claims",
        ),
        (
            "CDR906_2_reopen_condition",
            "reopen finite branch",
            "requires parent-owned P_tr/H_tr plus Z_tr, lambda_tr, Q_tr/m and units, or signed no-pole/Q_tr-zero theorem",
            "new checkpoint must cite source paths and remove MISSING markers",
            "sets exact path back from closure to theory",
        ),
        (
            "CDR906_3_R10_policy",
            "R10 testing",
            "skip finite trace alpha as a claim branch until reopen condition is met",
            "R10 runner may only be used as refusal/smoke while rows are closure-only",
            "protects empirical robustness work from phantom alpha rows",
        ),
        (
            "CDR906_4_local_GR_policy",
            "local GR/Newton",
            "trace branch does not prove local GR; it is simply removed from claimable finite-alpha use",
            "remaining local-GR residual stack must be audited separately",
            "moves next work to nontrace residual priority",
        ),
    ]
    return [
        {
            "demotion_id": demotion_id,
            "item": item,
            "new_status": status,
            "rule": rule,
            "why": why,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for demotion_id, item, status, rule, why in rows
    ]


def downstream_alpha_status_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "DAS906_0_Ztr",
            "Z_tr",
            "blocked_by_closure_only",
            "principal symbol cannot be read because H_tr is not parent-owned",
        ),
        (
            "DAS906_1_lambdatr",
            "lambda_tr",
            "blocked_by_closure_only",
            "range cannot be physical because no finite local trace operator/no-pole theorem is signed",
        ),
        (
            "DAS906_2_Qtr",
            "Q_tr/m",
            "blocked_by_closure_only",
            "source projection cannot be computed because P_tr/v_tr and matter descent are unsigned",
        ),
        (
            "DAS906_3_alpha_tr",
            "alpha_tr(lambda_tr)",
            "not_a_claimable_row",
            "depends on Z_tr, lambda_tr, Q_tr/m and a real R10 bound curve",
        ),
        (
            "DAS906_4_R10",
            "R10 comparison",
            "not_runnable_for_claim",
            "no valid MTS alpha row exists and the branch is closure-only",
        ),
    ]
    return [
        {
            "status_id": status_id,
            "quantity": quantity,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for status_id, quantity, status, reason in rows
    ]


def r10_alpha_dry_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "model_id": "MTS_trace_closure_only_after_906",
            "branch_id": "finite_trace_alpha_closure_only",
            "curve_id": "FT906_R10_0_closure_only_no_alpha",
            "lambda_value": "MISSING_CLOSURE_ONLY_NO_LAMBDA_TR",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_CLOSURE_ONLY_NO_ALPHA_TR",
            "alpha_bound": "MISSING_BOUND_LOOKUP",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_904_SOURCE_BACKED_ANCHORS_NONCLAIM.csv",
            "force_law_form": "none_for_claim; finite trace alpha is closure-only after failed P_tr/H_tr ownership",
            "derivation_status": "FINITE_TRACE_ALPHA_CLOSURE_ONLY_AFTER_906",
            "formula_reference": "P8_Y5_R10_906_CLOSURE_ONLY_DEMOTION_REGISTER.csv",
            "source_file": "source-intake/mts_residuals/P8_Y5_R10_906_CLOSURE_ONLY_DEMOTION_REGISTER.csv",
            "assumptions": "no parent-owned trace projector/Hessian; row exists only to prove runner refusal",
            "valid_for_claim": False,
            "notes": "do not score R10 from this branch until reopen condition is met",
            "generated_utc": generated_utc,
        }
    ]


def branch_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "BD906_0_parent_domain",
            "branch": "parent-own P_tr/H_tr",
            "decision": "failed_for_now",
            "reason": "ell_tr, K_parent, projector domain, Hessian, rank/no-pole, and no-tail signatures remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD906_1_closure_only",
            "branch": "finite trace alpha",
            "decision": "demoted_to_closure_only",
            "reason": "without P_tr/H_tr the finite alpha branch is not a parent field-theory output",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD906_2_selected_next",
            "branch": "post-trace-closure local-GR residual stack",
            "decision": NEXT_TARGET,
            "reason": "trace finite alpha is quarantined; the next useful work is ranking remaining local-GR/Newton residual channels",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    gates = [
        ("CGATE906_0_Ptr_Htr", "P_tr/H_tr parent-owned", "ell_tr/K_parent/Hessian/readout/no-tail signatures fail"),
        ("CGATE906_1_no_pole", "no local trace pole", "rank-zero/readout-only/source-cokernel/no-tail premises not parent-signed"),
        ("CGATE906_2_finite_alpha", "finite alpha_tr(lambda_tr)", "branch demoted closure-only"),
        ("CGATE906_3_R10", "R10 comparison pass", "closure-only branch has no valid MTS alpha row"),
        ("CGATE906_4_local_GR", "local GR/Newton derivation", "trace branch quarantine is not a full EH/source/PPN derivation"),
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
            "objective": "after demoting finite trace alpha to closure-only, rank the remaining local-GR/Newton residual stack and choose the next derivable gate",
            "include": "EH operator selection, source normalization/GM absorption, q_loc residual vector, PPN coefficients, boundary no-flux, clock/WEP residuals, R10 branch status",
            "exclude": "using finite trace alpha as evidence, fitted alpha, GitHub action, formalization-workbench edits",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_905_clean() -> bool:
    rows = read_csv(OUT / "P8_Y5_BRR545_905_VALIDATION.csv")
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


def import_r10_runner() -> Any:
    runner_path = ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py"
    spec = importlib.util.spec_from_file_location("r10_runner_906", runner_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {runner_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_r10_dry_runner() -> dict[str, Any]:
    module = import_r10_runner()
    result = module.run_runner(
        OUT / "P8_Y5_R10_906_R10_ALPHA_DRY_ROWS.csv",
        ANCHOR_BOUND_FILE,
        R10_DRY_RUN_DIR,
    )
    return result["status"]


def validation_rows(
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    ptr_rows_: list[dict[str, object]],
    fork_rows_: list[dict[str, object]],
    demotion_rows_: list[dict[str, object]],
    downstream_rows_: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    runner_status: dict[str, Any],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        summary_rows_,
        ptr_rows_,
        fork_rows_,
        demotion_rows_,
        downstream_rows_,
        dry_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
    ]
    missing_schema_columns = [column for column in MTS_REQUIRED_COLUMNS if column not in dry_rows_[0]]
    checks = [
        {
            "check_id": "V906_0_sources_exist_and_needles",
            "result": "pass"
            if all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows_)
            else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V906_1_prior_905_clean",
            "result": "pass" if prior_905_clean() else "fail",
            "detail": "P8_Y5_BRR545_905_VALIDATION.csv clean",
        },
        {
            "check_id": "V906_2_Ptr_Htr_not_parent_owned",
            "result": "pass"
            if any(row["test_id"] == "PHD906_6_verdict" and row["result"] == "not_parent_owned" for row in ptr_rows_)
            else "fail",
            "detail": "P_tr/H_tr parent ownership failed",
        },
        {
            "check_id": "V906_3_closure_demotion_selected",
            "result": "pass"
            if any(row["fork_id"] == "ZPF906_3_closure_demotion" and row["current_status"] == "selected" for row in fork_rows_)
            else "fail",
            "detail": "finite trace alpha demoted closure-only",
        },
        {
            "check_id": "V906_4_closure_register_has_reopen_condition",
            "result": "pass"
            if any(row["demotion_id"] == "CDR906_2_reopen_condition" for row in demotion_rows_)
            else "fail",
            "detail": "closure-only branch has explicit reopen condition",
        },
        {
            "check_id": "V906_5_downstream_alpha_all_blocked",
            "result": "pass" if all(row["claim_allowed"] is False for row in downstream_rows_) else "fail",
            "detail": f"downstream_rows={len(downstream_rows_)}",
        },
        {
            "check_id": "V906_6_R10_dry_schema_ok",
            "result": "pass" if not missing_schema_columns else "fail",
            "detail": "schema ok" if not missing_schema_columns else "missing=" + ",".join(missing_schema_columns),
        },
        {
            "check_id": "V906_7_R10_runner_blocks_claim",
            "result": "pass"
            if runner_status.get("claim_allowed") is False and runner_status.get("valid_mts_rows") == 0
            else "fail",
            "detail": json.dumps(
                {
                    "claim_allowed": runner_status.get("claim_allowed"),
                    "valid_mts_rows": runner_status.get("valid_mts_rows"),
                    "valid_bound_rows": runner_status.get("valid_bound_rows"),
                    "blocked_or_failed_rows": runner_status.get("blocked_or_failed_rows"),
                },
                sort_keys=True,
            ),
        },
        {
            "check_id": "V906_8_claim_gates_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in claim_rows_) else "fail",
            "detail": "all trace/R10/local claims blocked",
        },
        {
            "check_id": "V906_9_all_generated_rows_nonclaim",
            "result": "pass" if all_generated_rows_nonclaim(row_groups) else "fail",
            "detail": "all generated rows keep valid_for_claim/claim_allowed false",
        },
        {
            "check_id": "V906_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V906_11_next_target_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V906_12_validation_rows_ready",
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
    ptr_rows_: list[dict[str, object]],
    fork_rows_: list[dict[str, object]],
    demotion_rows_: list[dict[str, object]],
    downstream_rows_: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 906 - Y5/R10 Trace Projector Htr Parent Domain Or Closure Only

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **`P_tr/H_tr` still cannot be parent-owned from the current corpus, so the finite trace `alpha_tr(lambda_tr)` branch is demoted to explicit closure-only.** This is not a local-GR win; it is a quarantine. It prevents missing trace coefficients from being laundered into a fifth-force pass while preserving a clean reopen path if a future parent action supplies the missing root object.

## Exact 906 Finding
The parent-domain test fails upstream:

`ell_tr` is not a parent covector, `K_parent` is not a parent pairing, `P_tr` is only a conditional formal projector, and `H_tr=P_tr^dagger Hess(S_parent)P_tr` is therefore not a computable parent Hessian.

The no-pole/readout route is mathematically plausible but also unsigned: rank-zero, source-cokernel, boundary no-tail, and matter no-marker premises are not parent-integrated. Therefore the finite trace alpha branch is neither a derived finite field nor a proved zero theorem. It is closure-only.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## P_tr/H_tr Parent Domain Test
{md_table(ptr_rows_)}

## Zero-Pole Or Finite Field Fork
{md_table(fork_rows_)}

## Closure-Only Demotion Register
{md_table(demotion_rows_)}

## Downstream Alpha Status
{md_table(downstream_rows_)}

## R10 Alpha Dry Rows
{md_table(dry_rows_)}

## Branch Decision
{md_table(branch_rows_)}

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
    ptr_rows_ = ptr_htr_parent_domain_test_rows(generated_utc)
    fork_rows_ = zero_pole_or_finite_field_rows(generated_utc)
    demotion_rows_ = closure_demotion_rows(generated_utc)
    downstream_rows_ = downstream_alpha_status_rows(generated_utc)
    dry_rows_ = r10_alpha_dry_rows(generated_utc)
    branch_rows_ = branch_decision_rows(generated_utc)
    claim_rows_ = claim_gate_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)

    initial_outputs = {
        "P8_Y5_R10_906_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_906_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_R10_906_PTR_HTR_PARENT_DOMAIN_TEST.csv": ptr_rows_,
        "P8_Y5_R10_906_ZERO_POLE_OR_FINITE_FIELD_FORK.csv": fork_rows_,
        "P8_Y5_R10_906_CLOSURE_ONLY_DEMOTION_REGISTER.csv": demotion_rows_,
        "P8_Y5_R10_906_DOWNSTREAM_ALPHA_STATUS.csv": downstream_rows_,
        "P8_Y5_R10_906_R10_ALPHA_DRY_ROWS.csv": dry_rows_,
        "P8_Y5_R10_906_BRANCH_DECISION.csv": branch_rows_,
        "P8_Y5_R10_906_CLAIM_GATE.csv": claim_rows_,
        "P8_Y5_R10_906_NEXT_TARGET.csv": next_rows_,
    }
    for filename, rows in initial_outputs.items():
        write_csv(OUT / filename, rows)

    runner_status = run_r10_dry_runner()
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        ptr_rows_,
        fork_rows_,
        demotion_rows_,
        downstream_rows_,
        dry_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
        runner_status,
    )
    write_csv(OUT / "P8_Y5_BRR545_906_VALIDATION.csv", validation_rows_)

    doc_path = ROOT / "906-Y5-R10-trace-projector-Htr-parent-domain-or-closure-only.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows_,
        source_rows_,
        ptr_rows_,
        fork_rows_,
        demotion_rows_,
        downstream_rows_,
        dry_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_906_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
