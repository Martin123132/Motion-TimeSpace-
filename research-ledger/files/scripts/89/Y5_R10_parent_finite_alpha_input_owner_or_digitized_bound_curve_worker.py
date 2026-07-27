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

STATUS = "Y5_R10_905_parent_finite_alpha_input_owner_audit_built_Ptr_Htr_selected_no_claim"
CLAIM_CEILING = "parent_alpha_input_owner_audit_only_no_numeric_alpha_no_digitized_bound_curve_no_R10_or_local_GR_claim"
NEXT_TARGET = "906-Y5-R10-trace-projector-Htr-parent-domain-or-closure-only.md"
ANCHOR_BOUND_FILE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_904_SOURCE_BACKED_ANCHORS_NONCLAIM.csv"
R10_DRY_RUN_DIR = OUT / "P8_Y5_R10_905_R10_OWNER_DRY_RUNNER_RESULTS"

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
        "source_id": "904_doc",
        "path": ROOT / "904-Y5-R10-finite-alpha-source-provenance-and-real-bound-curve-gate.md",
        "needle": "MTS must source `Z_tr`, `lambda_tr`, `Q_tr/m`",
        "role": "immediate finite-alpha provenance handoff",
    },
    {
        "source_id": "904_validation",
        "path": OUT / "P8_Y5_BRR545_904_VALIDATION.csv",
        "needle": "V904_12_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "904_finite_alpha_gate",
        "path": OUT / "P8_Y5_R10_904_FINITE_ALPHA_PROVENANCE_GATE.csv",
        "needle": "FAP904_6",
        "role": "current finite-alpha missing input ledger",
    },
    {
        "source_id": "876_parent_input_ledger",
        "path": OUT / "P8_Y5_R10_876_PARENT_INPUT_LEDGER.csv",
        "needle": "PI876_0_P_T",
        "role": "earlier parent trace input ledger",
    },
    {
        "source_id": "892_trace_hessian_source_rows",
        "path": OUT / "P8_Y5_R10_892_TRACE_HESSIAN_SOURCE_ROWS.csv",
        "needle": "THS892_0_Htr_definition",
        "role": "trace Hessian source-row contract",
    },
    {
        "source_id": "892_no_pole_theorem",
        "path": OUT / "P8_Y5_R10_892_NO_POLE_THEOREM_ATTEMPT.csv",
        "needle": "NPT892_4_verdict",
        "role": "no-pole theorem alternative",
    },
    {
        "source_id": "895_quadratic_trace_contract",
        "path": OUT / "P8_Y5_R10_895_QUADRATIC_TRACE_ACTION_CONTRACT.csv",
        "needle": "QTC895_8_parent_adoption_verdict",
        "role": "finite trace action contract and adoption verdict",
    },
    {
        "source_id": "896_adoption_clause_audit",
        "path": OUT / "P8_Y5_R10_896_ADOPTION_CLAUSE_AUDIT.csv",
        "needle": "ACA896_0_parent_field_domain",
        "role": "parent adoption failure audit",
    },
    {
        "source_id": "896_coupling_bottleneck",
        "path": OUT / "P8_Y5_R10_896_COUPLING_BOTTLENECK_REGISTER.csv",
        "needle": "CB896_3_numeric_alpha_fallback",
        "role": "coupling bottleneck and numeric fallback rule",
    },
    {
        "source_id": "r10_runner",
        "path": ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py",
        "needle": "MTS_REQUIRED_COLUMNS",
        "role": "existing R10 comparator refusal gate",
    },
    {
        "source_id": "r10_anchor_bound_file",
        "path": ANCHOR_BOUND_FILE,
        "needle": "R10_904_LEE2020_ALPHA1_38P6UM_ANCHOR",
        "role": "source-backed anchor-only nonclaim bound file",
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
            "what_changed": "chose the parent finite-alpha input route over bound-curve digitization and ranked the missing MTS alpha inputs by dependency",
            "best_partial_result": "all R10-primary finite-alpha inputs reduce to the same upstream owner: P_tr/H_tr must be parent-owned or the trace branch must be closure/no-pole",
            "hard_blockers": "P_tr parent field domain, H_tr second variation, reduced local source-coupled domain, Z_tr principal symbol, mu_tr^2/lambda_tr mass gap, and J_tr source projection",
            "what_is_not_claimed": "finite trace carrier, numeric alpha_tr(lambda), R10 pass, Q_tr zero, no-pole local trace theorem, or local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def parent_alpha_owner_matrix_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "PAO905_0_Ptr_Htr",
            "P_tr,H_tr",
            "root_owner",
            "H_tr=P_tr^dagger Hess(S_parent) P_tr on reduced quotient tangent space",
            "MISSING_PARENT_PROJECTOR_HESSIAN",
            "without P_tr/H_tr no trace local degree/operator exists",
            "906 trace projector-Htr parent domain",
        ),
        (
            "PAO905_1_Ztr",
            "Z_tr",
            "depends_on_Ptr_Htr",
            "Z_tr is the coefficient of g_obs^{mu nu}k_mu k_nu in sigma_2(H_tr)",
            "MISSING_PRINCIPAL_SYMBOL",
            "kinetic sign and alpha normalization are unknowable",
            "derive only after PAO905_0",
        ),
        (
            "PAO905_2_mutr_lambdatr",
            "mu_tr^2,m_tr,lambda_tr",
            "depends_on_Ztr_and_Htr_zeroth_symbol",
            "m_tr^2=mu_tr^2/Z_tr and lambda_tr=1/m_tr or hbar/(m_tr c)",
            "MISSING_MASS_GAP_OR_NOPOLE",
            "range cannot be compared to R10/orbital bounds",
            "derive only after PAO905_1 or no-pole theorem",
        ),
        (
            "PAO905_3_Jtr_Qtr",
            "J_tr,Q_tr/m",
            "depends_on_Ptr_and_matter_descent_or_source_functional",
            "J_tr=P_tr^dagger J_parent; Q_tr^A/m_A from body response or zero by source-cokernel",
            "MISSING_SOURCE_PROJECTION_OR_ZERO_THEOREM",
            "coupling cannot be set to zero or scored",
            "source-cokernel branch remains conditional; finite branch needs parent charges",
        ),
        (
            "PAO905_4_response_vector",
            "C_tr_gamma,C_tr_beta,C_tr_source,C_tr_clock,Delta_AB_Qtr",
            "depends_on_Ptr_Htr_Jtr_and_metric_map",
            "arena response operators induced by trace branch after local metric/source normalization",
            "MISSING_RESPONSE_OPERATOR",
            "PPN/WEP/clock/orbital tests cannot be run honestly",
            "after trace branch classification",
        ),
        (
            "PAO905_5_alpha_row",
            "alpha_tr_AB(lambda_tr)",
            "depends_on_Ztr_lambdatr_Qtr_and_bound_curve",
            "alpha_tr_AB=(Q_tr^A/m_A)(Q_tr^B/m_B)/(4*pi Z_tr G_obs)",
            "MISSING_Z_LAMBDA_Q_INPUTS_AND_FULL_BOUND_CURVE",
            "R10 runner must keep rejecting",
            "only after parent inputs and full bound curve exist",
        ),
    ]
    return [
        {
            "owner_id": owner_id,
            "quantity": quantity,
            "dependency_rank": rank,
            "definition": definition,
            "current_status": status,
            "why_it_blocks": why,
            "next_action": action,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for owner_id, quantity, rank, definition, status, why, action in rows
    ]


def derive_or_demote_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "DOD905_0_parent_finite_field",
            "derive finite local trace field",
            "parent action names P_tr, H_tr, Z_tr, mu_tr^2, J_tr, units, and boundary conditions",
            "not_available",
            "can build alpha_tr(lambda) source rows",
            "if unavailable, finite trace field is closure-only",
        ),
        (
            "DOD905_1_no_pole_trace_constraint",
            "derive no local source-coupled trace pole",
            "rank-zero/readout-only/constraint-null/source-cokernel/no-tail premises all parent-signed",
            "not_available",
            "lambda_tr absent locally and alpha_tr branch dies structurally",
            "if unavailable, no-pole cannot be claimed",
        ),
        (
            "DOD905_2_source_cokernel_zero",
            "derive J_tr=0/Q_tr=0",
            "matter descends through q_loc and v_tr is local-vertical with no marker constants",
            "conditional_not_signed",
            "local matter coupling vanishes even if formal trace variable exists",
            "if unavailable, Q_tr/m must be sourced",
        ),
        (
            "DOD905_3_bound_digitization",
            "digitize/source R10 alpha(lambda) curve",
            "full curve or supplemental numeric table with provenance and uncertainty",
            "useful_but_not_first",
            "enables scoring once alpha_tr(lambda) exists",
            "does not help while MTS alpha row is missing",
        ),
        (
            "DOD905_4_selected_route",
            "attack P_tr/H_tr parent domain first",
            "without it every finite coefficient is unowned and every zero theorem is under-specified",
            "selected",
            "decides whether the whole trace sector is finite field, no-pole theorem, or closure-only",
            "next target 906",
        ),
    ]
    return [
        {
            "route_id": route_id,
            "route": route,
            "requirement": requirement,
            "current_status": status,
            "if_success": success,
            "if_failure": failure,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for route_id, route, requirement, status, success, failure in rows
    ]


def bound_digitization_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "BDD905_0_bound_curve_worker",
            "option": "digitize/source R10 bound curve now",
            "current_value": "source-backed anchors exist; full curve missing",
            "decision": "defer_one_checkpoint",
            "reason": "MTS alpha_tr(lambda_tr) has zero valid parent rows, so curve work cannot produce a theory comparison yet",
            "safe_to_do_later": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "BDD905_1_parent_input_worker",
            "option": "derive parent finite-alpha inputs",
            "current_value": "P_tr/H_tr root owner missing",
            "decision": "selected_now",
            "reason": "this is the unique upstream dependency for Z_tr, lambda_tr, Q_tr/m, and no-pole classification",
            "safe_to_do_later": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def r10_alpha_dry_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "model_id": "MTS_trace_parent_alpha_owner_audit",
            "branch_id": "Ptr_Htr_missing_root_owner",
            "curve_id": "FT905_R10_0_parent_inputs_missing",
            "lambda_value": "MISSING_LAMBDA_TR_BECAUSE_PTR_HTR_MISSING",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_ALPHA_TR_BECAUSE_ZTR_QTR_MISSING",
            "alpha_bound": "MISSING_BOUND_LOOKUP",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_904_SOURCE_BACKED_ANCHORS_NONCLAIM.csv",
            "force_law_form": "Yukawa alpha_tr_AB exp(-r/lambda_tr) only after parent finite branch exists",
            "derivation_status": "PARENT_ALPHA_INPUT_OWNER_MISSING",
            "formula_reference": "P8_Y5_R10_905_PARENT_ALPHA_INPUT_OWNER_MATRIX.csv",
            "source_file": "source-intake/mts_residuals/P8_Y5_R10_905_PARENT_ALPHA_INPUT_OWNER_MATRIX.csv",
            "assumptions": "owner audit row only; no numeric parent coefficient",
            "valid_for_claim": False,
            "notes": "runner must reject until P_tr/H_tr and downstream quantities are real",
            "generated_utc": generated_utc,
        }
    ]


def branch_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "BD905_0_parent_inputs",
            "branch": "derive parent finite-alpha inputs",
            "decision": "selected",
            "reason": "P_tr/H_tr is the root owner for every missing alpha input and for the no-pole alternative",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD905_1_digitized_bound_curve",
            "branch": "R10 curve digitization/source table",
            "decision": "deferred_one_checkpoint",
            "reason": "important but downstream; no MTS alpha row exists to compare against it",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD905_2_selected_next",
            "branch": "trace projector-Htr parent domain or closure-only",
            "decision": NEXT_TARGET,
            "reason": "if 906 cannot parent-own P_tr/H_tr, finite trace alpha must be explicitly closure-only until new parent action material appears",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    gates = [
        ("CGATE905_0_Ptr_Htr", "parent trace field/operator exists", "P_tr/H_tr are missing"),
        ("CGATE905_1_Z_lambda", "Z_tr/lambda_tr numeric", "principal symbol and mass gap depend on missing H_tr"),
        ("CGATE905_2_Qtr", "Q_tr/m sourced or zero", "source-cokernel/matter descent remains unsigned"),
        ("CGATE905_3_R10", "R10 comparison pass", "MTS alpha row invalid and bound curve anchor-only"),
        ("CGATE905_4_local_GR", "local GR/Newton reduction", "trace sector not finite-owned, no-pole, or closure-demoted"),
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
            "objective": "try to parent-own the trace projector and projected Hessian domain; if it cannot be derived, demote finite trace alpha to explicit closure-only",
            "include": "P_tr field domain, H_tr=P_tr^dagger Hess(S_parent)P_tr, gauge/constraint reduction, source-coupled domain, no-pole fork",
            "exclude": "R10 curve digitization as main path, fitted alpha, local-GR pass, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_904_clean() -> bool:
    rows = read_csv(OUT / "P8_Y5_BRR545_904_VALIDATION.csv")
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
    spec = importlib.util.spec_from_file_location("r10_runner_905", runner_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {runner_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_r10_dry_runner() -> dict[str, Any]:
    module = import_r10_runner()
    result = module.run_runner(
        OUT / "P8_Y5_R10_905_R10_ALPHA_DRY_ROWS.csv",
        ANCHOR_BOUND_FILE,
        R10_DRY_RUN_DIR,
    )
    return result["status"]


def validation_rows(
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    owner_rows_: list[dict[str, object]],
    derive_rows_: list[dict[str, object]],
    bound_decision_rows_: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    runner_status: dict[str, Any],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        summary_rows_,
        owner_rows_,
        derive_rows_,
        bound_decision_rows_,
        dry_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
    ]
    missing_schema_columns = [column for column in MTS_REQUIRED_COLUMNS if column not in dry_rows_[0]]
    checks = [
        {
            "check_id": "V905_0_sources_exist_and_needles",
            "result": "pass"
            if all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows_)
            else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V905_1_prior_904_clean",
            "result": "pass" if prior_904_clean() else "fail",
            "detail": "P8_Y5_BRR545_904_VALIDATION.csv clean",
        },
        {
            "check_id": "V905_2_root_owner_selected",
            "result": "pass"
            if any(row["owner_id"] == "PAO905_0_Ptr_Htr" and row["dependency_rank"] == "root_owner" for row in owner_rows_)
            else "fail",
            "detail": "P_tr/H_tr selected as root owner",
        },
        {
            "check_id": "V905_3_all_owner_rows_blocked",
            "result": "pass" if all("MISSING" in stringify(row["current_status"]) for row in owner_rows_) else "fail",
            "detail": f"owner_rows={len(owner_rows_)}",
        },
        {
            "check_id": "V905_4_derive_or_demote_selects_906",
            "result": "pass"
            if any(row["route_id"] == "DOD905_4_selected_route" and row["current_status"] == "selected" for row in derive_rows_)
            else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V905_5_bound_digitization_deferred",
            "result": "pass"
            if any(row["decision_id"] == "BDD905_0_bound_curve_worker" and row["decision"] == "defer_one_checkpoint" for row in bound_decision_rows_)
            else "fail",
            "detail": "bound curve worker deferred because MTS alpha row missing",
        },
        {
            "check_id": "V905_6_R10_dry_schema_ok",
            "result": "pass" if not missing_schema_columns else "fail",
            "detail": "schema ok" if not missing_schema_columns else "missing=" + ",".join(missing_schema_columns),
        },
        {
            "check_id": "V905_7_R10_runner_blocks_claim",
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
            "check_id": "V905_8_claim_gates_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in claim_rows_) else "fail",
            "detail": "all parent-alpha/R10/local claims blocked",
        },
        {
            "check_id": "V905_9_all_generated_rows_nonclaim",
            "result": "pass" if all_generated_rows_nonclaim(row_groups) else "fail",
            "detail": "all generated rows keep valid_for_claim/claim_allowed false",
        },
        {
            "check_id": "V905_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V905_11_next_target_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V905_12_validation_rows_ready",
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
    owner_rows_: list[dict[str, object]],
    derive_rows_: list[dict[str, object]],
    bound_decision_rows_: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 905 - Y5/R10 Parent Finite Alpha Input Owner Or Digitized Bound Curve Worker

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the next useful move is parent input ownership, not R10 curve digitization.** The finite trace `alpha_tr(lambda_tr)` row cannot exist until the parent owns `P_tr/H_tr`. That single upstream object decides whether `Z_tr`, `lambda_tr`, and `Q_tr/m` can be derived, whether the local trace branch has no pole, or whether the finite trace branch must be demoted to closure-only.

## Exact 905 Finding
The hierarchy is now sharp:

`P_tr/H_tr -> Z_tr and mu_tr^2 -> lambda_tr -> J_tr/Q_tr/m -> alpha_tr(lambda_tr) -> R10 comparison`.

The current corpus does not parent-own the root `P_tr/H_tr` object. So `Z_tr`, `lambda_tr`, and `Q_tr/m` remain blocked, and digitizing a perfect R10 bound curve would still leave the theory unscorable. The next derivation target is therefore `906`: parent-own `P_tr/H_tr`, prove no local trace pole, or explicitly mark the finite trace alpha branch as closure-only.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## Parent Alpha Input Owner Matrix
{md_table(owner_rows_)}

## Derive Or Demote Audit
{md_table(derive_rows_)}

## Bound Digitization Decision
{md_table(bound_decision_rows_)}

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
    owner_rows_ = parent_alpha_owner_matrix_rows(generated_utc)
    derive_rows_ = derive_or_demote_rows(generated_utc)
    bound_decision_rows_ = bound_digitization_decision_rows(generated_utc)
    dry_rows_ = r10_alpha_dry_rows(generated_utc)
    branch_rows_ = branch_decision_rows(generated_utc)
    claim_rows_ = claim_gate_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)

    initial_outputs = {
        "P8_Y5_R10_905_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_905_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_R10_905_PARENT_ALPHA_INPUT_OWNER_MATRIX.csv": owner_rows_,
        "P8_Y5_R10_905_DERIVE_OR_DEMOTE_AUDIT.csv": derive_rows_,
        "P8_Y5_R10_905_BOUND_DIGITIZATION_DECISION.csv": bound_decision_rows_,
        "P8_Y5_R10_905_R10_ALPHA_DRY_ROWS.csv": dry_rows_,
        "P8_Y5_R10_905_BRANCH_DECISION.csv": branch_rows_,
        "P8_Y5_R10_905_CLAIM_GATE.csv": claim_rows_,
        "P8_Y5_R10_905_NEXT_TARGET.csv": next_rows_,
    }
    for filename, rows in initial_outputs.items():
        write_csv(OUT / filename, rows)

    runner_status = run_r10_dry_runner()
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        owner_rows_,
        derive_rows_,
        bound_decision_rows_,
        dry_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
        runner_status,
    )
    write_csv(OUT / "P8_Y5_BRR545_905_VALIDATION.csv", validation_rows_)

    doc_path = ROOT / "905-Y5-R10-parent-finite-alpha-input-owner-or-digitized-bound-curve-worker.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows_,
        source_rows_,
        owner_rows_,
        derive_rows_,
        bound_decision_rows_,
        dry_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_905_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
