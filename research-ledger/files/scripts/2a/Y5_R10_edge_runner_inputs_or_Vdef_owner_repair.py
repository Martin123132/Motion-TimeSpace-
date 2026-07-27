from __future__ import annotations

import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = POST_CHECKPOINT / "source-intake" / "local_bounds"
RUNS = POST_CHECKPOINT / "runs"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "725-Y5-R10-edge-runner-inputs-or-Vdef-owner-repair.md"
RUNNER = POST_CHECKPOINT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py"
EDGE_SMOKE_PATH = RESIDUALS / "R10_alpha_lambda_curve_MTS_edge_residual_smoke_725.csv"
LIVE_BOUND_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
REVIEW_BOUND_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv"
NEXT_TARGET = "726-Y5-R10-Vdef-parent-owner-map-or-edge-coefficient-source-contract.md"
GENERATED_UTC = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
RUN_STAMP = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
RUN_ROOT = RUNS / f"{RUN_STAMP}-Y5-R10-edge-runner-inputs-or-Vdef-owner-repair"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

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

SOURCES = {
    "724_doc": {
        "path": POST_CHECKPOINT / "724-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
        "note": "immediate handoff: runner inputs or Vdef owner repair",
        "needles": ["725-Y5-R10-edge-runner-inputs-or-Vdef-owner-repair.md", "Verdict: **nonclaim**", "alpha_edge(lambda)"],
    },
    "724_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_724_VALIDATION.csv",
        "note": "prior validation gate",
        "needles": ["V724_10_decision_selects_725", "pass", "V724_13_formalization_workbench_untouched"],
    },
    "724_edge_law": {
        "path": RESIDUALS / "P8_Y5_R10_724_EDGE_ENVELOPE_LAW.csv",
        "note": "current edge alpha envelope law",
        "needles": ["EEL724_3_edge_alpha", "alpha_edge(lambda)=K_edge(lambda)*Qbar_edge_XH(lambda)*qbar_XT", "false"],
    },
    "724_claim_contract": {
        "path": RESIDUALS / "P8_Y5_R10_724_EDGE_CLAIM_INPUT_CONTRACT.csv",
        "note": "current missing-input contract",
        "needles": ["ECIC724_0_lambda_edge", "ECIC724_1_K_edge", "ECIC724_5_no_double_count"],
    },
    "724_owner_gate": {
        "path": RESIDUALS / "P8_Y5_R10_724_OWNER_REPAIR_GATE.csv",
        "note": "current owner repair blockers",
        "needles": ["ORG724_1_Vdef_owner", "conditional_contract_not_parent_sourced", "ORG724_5_verdict"],
    },
    "724_runner_readiness": {
        "path": RESIDUALS / "P8_Y5_R10_724_RUNNER_READINESS.csv",
        "note": "runner readiness and claim blockers",
        "needles": ["RR724_0_existing_R10_runner", "claim_allowed", "false"],
    },
    "724_pressure_matrix": {
        "path": RESIDUALS / "P8_Y5_R10_724_EDGE_PRESSURE_MATRIX.csv",
        "note": "private review-candidate pressure matrix",
        "needles": ["EPM724_0", "private_review_candidate_nonclaim", "false"],
    },
    "724_decision": {
        "path": RESIDUALS / "P8_Y5_R10_724_DECISION_MATRIX.csv",
        "note": "current decision matrix",
        "needles": ["DM724_3_next_best_target", "build edge runner inputs or repair Vdef owner", "725-Y5-R10-edge-runner-inputs-or-Vdef-owner-repair.md"],
    },
    "586_doc": {
        "path": POST_CHECKPOINT / "586-Y5-R10-Vdef-owner-action-sketch-or-edge-runner-numeric-priors.md",
        "note": "older affine Vdef action sketch",
        "needles": ["affine block derives", "conditional_mechanism_found_but_P_J_A_not_parent_sourced", "edge-prior grid"],
    },
    "586_theorem": {
        "path": RESIDUALS / "P8_Y5_R10_586_CONDITIONAL_NO_POLE_THEOREM.csv",
        "note": "conditional no-pole theorem clauses",
        "needles": ["CNT586_0_affine_defect_block", "CNT586_4_no_double_count", "false"],
    },
    "586_boundary": {
        "path": RESIDUALS / "P8_Y5_R10_586_BOUNDARY_EXACTNESS_TEST.csv",
        "note": "boundary exactness fallback",
        "needles": ["BET586_3_improper_edge_mode", "fallback_live", "false"],
    },
    "live_bound_curve": {
        "path": LIVE_BOUND_CURVE,
        "note": "live claim curve placeholder",
        "needles": ["MISSING_DIGITIZED_ALPHA_BOUND", "valid_for_claim", "false"],
    },
    "review_bound_curve": {
        "path": REVIEW_BOUND_CURVE,
        "note": "private review-candidate curve",
        "needles": ["R10_VECTOR_2020_REVIEW_0000", "Review candidate only", "false"],
    },
    "runner": {
        "path": RUNNER,
        "note": "existing R10 comparator",
        "needles": ["MTS_REQUIRED_COLUMNS", "claim_allowed", "valid_for_claim"],
    },
}


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(POST_CHECKPOINT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_path_string(*keys: str) -> str:
    return ";".join(str(SOURCES[key]["path"]) for key in keys)


def text_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def csv_contains(path: Path, *needles: str) -> bool:
    return text_contains(path, list(needles))


def prior_validation_clean(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def all_valid_false(paths: list[Path]) -> bool:
    for path in paths:
        rows = read_csv(path)
        if not rows:
            continue
        if "valid_for_claim" not in rows[0]:
            continue
        if any(row.get("valid_for_claim", "").lower() != "false" for row in rows):
            return False
    return True


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime)
        if modified > CUTOFF:
            count += 1
    return count


def under_post_checkpoint(paths: list[Path]) -> bool:
    root = POST_CHECKPOINT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root)
        except ValueError:
            return False
    return True


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def make_source_register() -> list[dict[str, object]]:
    return [
        {
            "source_id": key,
            "path": str(info["path"]),
            "exists": bool_text(info["path"].exists()),
            "needle_check": bool_text(text_contains(info["path"], info["needles"])),
            "role": info["note"],
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        }
        for key, info in SOURCES.items()
    ]


def make_edge_runner_schema() -> list[dict[str, object]]:
    purposes = {
        "model_id": "names the theory branch",
        "branch_id": "names the residual/zero route",
        "curve_id": "groups rows into a sampled alpha(lambda) curve",
        "lambda_value": "edge support/range ordinate",
        "lambda_units": "units convertible to meters",
        "alpha_predicted": "numeric alpha for runner validation; symbolic rows must stay nonclaim",
        "alpha_bound": "row-level bound annotation copied from private pressure matrix only",
        "alpha_bound_source": "bound provenance",
        "force_law_form": "Yukawa/edge/envelope form",
        "derivation_status": "must distinguish source-backed from smoke/template",
        "formula_reference": "checkpoint formula source",
        "source_file": "local source for coefficients",
        "assumptions": "same-frame and no-double-count assumptions",
        "valid_for_claim": "must be true only after all inputs are numeric/source-backed",
        "notes": "blockers and provenance caveats",
    }
    return [
        {
            "column": column,
            "purpose": purposes[column],
            "edge_branch_status": "required",
            "valid_for_claim": "false",
            "source_paths": source_path_string("runner", "724_edge_law"),
            "generated_utc": GENERATED_UTC,
        }
        for column in MTS_REQUIRED_COLUMNS
    ]


def make_edge_smoke_rows() -> list[dict[str, object]]:
    return [
        {
            "model_id": "MTS_edge_residual_nonclaim_smoke_725",
            "branch_id": "edge_only_residual_smoke_pressure_safe",
            "curve_id": "R10_alpha_lambda_curve_MTS_edge_residual_smoke_725",
            "lambda_value": "6.080783e-04",
            "lambda_units": "m",
            "alpha_predicted": "0.001",
            "alpha_bound": "0.00234471960478",
            "alpha_bound_source": "source-intake/mts_residuals/P8_Y5_R10_724_EDGE_PRESSURE_MATRIX.csv::private_review_candidate_nonclaim",
            "force_law_form": "edge_alpha_envelope",
            "derivation_status": "numeric_smoke_placeholder_not_source_backed",
            "formula_reference": "724-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
            "source_file": "724-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
            "assumptions": "K_edge*Qbar_edge_XH*qbar_XT inserted for runner schema smoke only; no parent coefficients",
            "valid_for_claim": "false",
            "notes": "nonclaim smoke row below private review-candidate ceiling; must remain invalid until coefficients and bound curve are source-backed",
        },
        {
            "model_id": "MTS_edge_residual_nonclaim_smoke_725",
            "branch_id": "edge_only_residual_smoke_pressure_safe",
            "curve_id": "R10_alpha_lambda_curve_MTS_edge_residual_smoke_725",
            "lambda_value": "1.000000e-04",
            "lambda_units": "m",
            "alpha_predicted": "0.05",
            "alpha_bound": "0.0766587862265",
            "alpha_bound_source": "source-intake/mts_residuals/P8_Y5_R10_724_EDGE_PRESSURE_MATRIX.csv::private_review_candidate_nonclaim",
            "force_law_form": "edge_alpha_envelope",
            "derivation_status": "numeric_smoke_placeholder_not_source_backed",
            "formula_reference": "724-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
            "source_file": "724-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
            "assumptions": "K_edge*Qbar_edge_XH*qbar_XT inserted for runner schema smoke only; no parent coefficients",
            "valid_for_claim": "false",
            "notes": "nonclaim smoke row below private review-candidate ceiling; must remain invalid until coefficients and bound curve are source-backed",
        },
        {
            "model_id": "MTS_edge_residual_nonclaim_smoke_725",
            "branch_id": "edge_only_residual_smoke_pressure_fail",
            "curve_id": "R10_alpha_lambda_curve_MTS_edge_residual_smoke_725",
            "lambda_value": "1.000000e-03",
            "lambda_units": "m",
            "alpha_predicted": "0.1",
            "alpha_bound": "0.00998986313981",
            "alpha_bound_source": "source-intake/mts_residuals/P8_Y5_R10_724_EDGE_PRESSURE_MATRIX.csv::private_review_candidate_nonclaim",
            "force_law_form": "edge_alpha_envelope",
            "derivation_status": "numeric_smoke_placeholder_not_source_backed",
            "formula_reference": "724-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
            "source_file": "724-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
            "assumptions": "intentional pressure-fail smoke row; it must not become evidence",
            "valid_for_claim": "false",
            "notes": "nonclaim row above private pressure ceiling; verifies runner still blocks because valid_for_claim=false",
        },
        {
            "model_id": "MTS_edge_residual_nonclaim_smoke_725",
            "branch_id": "edge_missing_input_guard",
            "curve_id": "R10_alpha_lambda_curve_MTS_edge_residual_smoke_725",
            "lambda_value": "MISSING_PARENT_EDGE_RANGE_OR_ENVELOPE",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_K_EDGE_QBAR_EDGE_QBAR_XT",
            "alpha_bound": "MISSING_CLAIM_GRADE_BOUND",
            "alpha_bound_source": "source-intake/mts_residuals/P8_Y5_R10_724_EDGE_CLAIM_INPUT_CONTRACT.csv",
            "force_law_form": "edge_alpha_envelope",
            "derivation_status": "template_invalid_missing_edge_inputs",
            "formula_reference": "724-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
            "source_file": "source-intake/mts_residuals/P8_Y5_R10_724_EDGE_CLAIM_INPUT_CONTRACT.csv",
            "assumptions": "explicit missing-input guard row",
            "valid_for_claim": "false",
            "notes": "runner must reject this row",
        },
    ]


def run_runner(bound_curve: Path, output_dir: Path) -> dict[str, object]:
    completed = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--mts-curve",
            str(EDGE_SMOKE_PATH),
            "--bound-curve",
            str(bound_curve),
            "--output-dir",
            str(output_dir),
        ],
        cwd=str(POST_CHECKPOINT),
        check=True,
        capture_output=True,
        text=True,
    )
    status_path = output_dir / "R10_runner_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    status["stdout"] = completed.stdout.strip()
    status["stderr"] = completed.stderr.strip()
    return status


def make_vdef_owner_repair_attempt() -> list[dict[str, object]]:
    return [
        {
            "repair_id": "VOR725_0_affine_action_variation",
            "target": "derive the X equation from one affine parent block",
            "candidate_statement": "S_X=int sqrt(-g)[P^{mu nu}[Y](nabla_mu X_nu-A_{mu nu}[Y])+X_nu J_eff^nu[Y]]+S_boundary",
            "derived_if_signed": "delta_X S_X gives C_X^nu=-nabla_mu P^{mu nu}+J_eff^nu plus boundary n_mu P^{mu nu}",
            "current_status": "conditional_variation_written_not_parent_sourced",
            "failure_mode": "P,J,A,boundary counterterm are still allowed as inserted coefficients",
            "claim_effect": "no theorem-zero credit",
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_doc", "586_theorem", "724_owner_gate"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "repair_id": "VOR725_1_parent_symplectic_owner",
            "target": "own the generator by parent symplectic geometry",
            "candidate_statement": "i_{v_epsilon} Omega_Y = delta G[epsilon]",
            "derived_if_signed": "C_X and Q_boundary become a momentum map rather than a fitted field equation",
            "current_status": "missing_theta_Y_Omega_Y_vertical_generator",
            "failure_mode": "cannot prove first-class local gauge silence",
            "claim_effect": "edge residual remains live",
            "valid_for_claim": "false",
            "source_paths": source_path_string("724_owner_gate", "586_theorem"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "repair_id": "VOR725_2_boundary_silence",
            "target": "zero the edge charge",
            "candidate_statement": "Q_edge[epsilon]=int_boundary epsilon_nu(n_mu P^{mu nu}+B_ct^nu)=0",
            "derived_if_signed": "Qbar_edge_XH(lambda)=0 and the edge alpha branch collapses",
            "current_status": "not_derived",
            "failure_mode": "improper/finite edge mode remains possible",
            "claim_effect": "must keep alpha_edge(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_boundary", "724_owner_gate"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "repair_id": "VOR725_3_matter_and_projector_descent",
            "target": "zero ordinary test/source charges",
            "candidate_statement": "S_matter=Sbar_matter[q(Y),psi] and Pi_M^H[Q_edge]=0",
            "derived_if_signed": "qbar_XT=0 or Qbar_edge_XH=0 without source-by-source tuning",
            "current_status": "not_signed",
            "failure_mode": "ordinary matter can still carry finite retained edge response",
            "claim_effect": "local arenas stay blocked",
            "valid_for_claim": "false",
            "source_paths": source_path_string("724_owner_gate", "724_claim_contract"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "repair_id": "VOR725_4_verdict",
            "target": "choose owner repair or edge runner",
            "candidate_statement": "one parent-owned zero route is needed before no-pole/local-GR credit",
            "derived_if_signed": "edge runner branch can be replaced by theorem-zero rows",
            "current_status": "repair_not_closed_runner_inputs_required",
            "failure_mode": "continue with nonclaim runner-shaped edge rows",
            "claim_effect": "blocked_for_claim",
            "valid_for_claim": "false",
            "source_paths": source_path_string("724_doc", "724_runner_readiness"),
            "generated_utc": GENERATED_UTC,
        },
    ]


def make_claim_blockers(runner_status_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blockers = [
        {
            "blocker_id": "CB725_0_edge_coefficients",
            "blocker": "K_edge, Qbar_edge_XH, and qbar_XT are not parent-derived or source-backed",
            "required_repair": "derive owner zero or fill numeric/source-backed coefficient rows",
            "claim_blocked": "true",
            "valid_for_claim": "false",
            "source_paths": source_path_string("724_claim_contract", "724_edge_law"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "blocker_id": "CB725_1_edge_support",
            "blocker": "lambda_edge/support envelope is not parent-derived",
            "required_repair": "derive edge kernel support or bounded range grid",
            "claim_blocked": "true",
            "valid_for_claim": "false",
            "source_paths": source_path_string("724_claim_contract", "586_boundary"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "blocker_id": "CB725_2_bound_curve",
            "blocker": "live bound file is placeholder and review curve is private nonclaim",
            "required_repair": "QA-promote/source alpha_bound(lambda) before any R10 statement",
            "claim_blocked": "true",
            "valid_for_claim": "false",
            "source_paths": source_path_string("live_bound_curve", "review_bound_curve"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "blocker_id": "CB725_3_no_double_count",
            "blocker": "bulk-edge source split is not orthogonalized",
            "required_repair": "derive Q_X=Q_bulk+Q_edge decomposition and projection rules",
            "claim_blocked": "true",
            "valid_for_claim": "false",
            "source_paths": source_path_string("724_claim_contract", "586_theorem"),
            "generated_utc": GENERATED_UTC,
        },
    ]
    for status in runner_status_rows:
        blockers.append(
            {
                "blocker_id": f"CB725_runner_{status['runner_id']}",
                "blocker": f"runner claim_allowed={status['claim_allowed']} valid_mts_rows={status['valid_mts_rows']} valid_bound_rows={status['valid_bound_rows']}",
                "required_repair": "all MTS and bound rows must be valid_for_claim=true, numeric, sourced, and non-placeholder",
                "claim_blocked": "true",
                "valid_for_claim": "false",
                "source_paths": status["source_paths"],
                "generated_utc": GENERATED_UTC,
            }
        )
    return blockers


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    RUN_ROOT.mkdir(parents=True, exist_ok=True)

    source_register = make_source_register()
    edge_runner_schema = make_edge_runner_schema()
    edge_smoke_rows = make_edge_smoke_rows()
    write_csv(EDGE_SMOKE_PATH, edge_smoke_rows, MTS_REQUIRED_COLUMNS)

    runner_statuses: list[dict[str, object]] = []
    for runner_id, bound_curve, run_subdir in [
        ("R10_EDGE_SMOKE_725_LIVE_PLACEHOLDER", LIVE_BOUND_CURVE, "live_placeholder_bound"),
        ("R10_EDGE_SMOKE_725_REVIEW_CANDIDATE", REVIEW_BOUND_CURVE, "review_candidate_bound"),
    ]:
        output_dir = RUN_ROOT / run_subdir / "results"
        status = run_runner(bound_curve, output_dir)
        runner_statuses.append(
            {
                "runner_id": runner_id,
                "bound_curve": rel(bound_curve),
                "output_dir": rel(output_dir),
                "mts_rows": str(status["mts_rows"]),
                "valid_mts_rows": str(status["valid_mts_rows"]),
                "bound_rows": str(status["bound_rows"]),
                "valid_bound_rows": str(status["valid_bound_rows"]),
                "comparison_rows": str(status["comparison_rows"]),
                "passed_rows": str(status["passed_rows"]),
                "blocked_or_failed_rows": str(status["blocked_or_failed_rows"]),
                "claim_allowed": bool_text(bool(status["claim_allowed"])),
                "valid_for_claim": "false",
                "source_paths": source_path_string("runner", "724_runner_readiness"),
                "generated_utc": GENERATED_UTC,
            }
        )

    vdef_owner_repair_attempt = make_vdef_owner_repair_attempt()
    claim_blockers = make_claim_blockers(runner_statuses)
    decision_matrix = [
        {
            "decision_id": "D725_0_Vdef_owner_attempt",
            "decision": "do_not_promote_Vdef_owner",
            "meaning": "affine variation is useful, but P,J,A,boundary, symplectic owner, and matter descent remain unsigned",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("724_owner_gate", "586_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D725_1_edge_runner_inputs_written",
            "decision": "write runner-shaped edge smoke rows",
            "meaning": "edge branch can be passed through the existing R10 comparator without becoming evidence",
            "status": "progress_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": str(EDGE_SMOKE_PATH),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D725_2_runner_blocks_claim",
            "decision": "runner correctly refuses claim status",
            "meaning": "valid_mts_rows=0 and valid_bound_rows=0 keep live and review runs blocked",
            "status": "guardrail_pass",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("runner", "live_bound_curve", "review_bound_curve"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D725_3_next_best_target",
            "decision": "map parent owner or source edge coefficients",
            "meaning": "the next move should either close theorem-zero or turn lambda/K/Qbar/qbar into sourced rows",
            "status": "next_derivation_target",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("724_claim_contract", "724_owner_gate"),
            "generated_utc": GENERATED_UTC,
        },
    ]
    route_update = [
        {
            "route_id": "RU725_0_allowed",
            "allowed_after_725": "use R10_alpha_lambda_curve_MTS_edge_residual_smoke_725.csv for schema/runnable smoke tests only",
            "forbidden_after_725": "copy smoke rows into live claim files or set valid_for_claim=true",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": str(EDGE_SMOKE_PATH),
            "generated_utc": GENERATED_UTC,
        },
        {
            "route_id": "RU725_1_allowed",
            "allowed_after_725": "keep Vdef owner repair as the preferred theorem-zero path",
            "forbidden_after_725": "claim no-pole/local-GR from the affine skeleton alone",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_doc", "724_owner_gate"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "route_id": "RU725_2_allowed",
            "allowed_after_725": "use runner status to verify guardrails and failure modes",
            "forbidden_after_725": "interpret nonclaim runner smoke as empirical support",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("runner", "724_runner_readiness"),
            "generated_utc": GENERATED_UTC,
        },
    ]
    nonclaim_summary = [
        {
            "status": "Y5_R10_725_edge_runner_inputs_written_runner_blocks_nonclaim_rows_Vdef_owner_repair_open",
            "claim_ceiling": "edge_runner_smoke_and_Vdef_owner_attempt_only_no_R10_WEP_PPN_Newton_or_local_GR_pass",
            "main_result": "runner-shaped edge residual rows now exist for the current 724 chain and both runner branches block claims",
            "hard_blocker": "Vdef owner remains conditional; edge coefficients and bound curve are not source-backed",
            "run_root": str(RUN_ROOT),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("724_doc", "runner"),
            "generated_utc": GENERATED_UTC,
        }
    ]

    outputs = {
        "source_register": (
            RESIDUALS / "P8_Y5_R10_725_SOURCE_REGISTER.csv",
            source_register,
            ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
        ),
        "edge_runner_schema": (
            RESIDUALS / "P8_Y5_R10_725_EDGE_RUNNER_INPUT_SCHEMA.csv",
            edge_runner_schema,
            ["column", "purpose", "edge_branch_status", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "vdef_owner_repair_attempt": (
            RESIDUALS / "P8_Y5_R10_725_VDEF_OWNER_REPAIR_ATTEMPT.csv",
            vdef_owner_repair_attempt,
            [
                "repair_id",
                "target",
                "candidate_statement",
                "derived_if_signed",
                "current_status",
                "failure_mode",
                "claim_effect",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "runner_status_summary": (
            RESIDUALS / "P8_Y5_R10_725_RUNNER_STATUS_SUMMARY.csv",
            runner_statuses,
            [
                "runner_id",
                "bound_curve",
                "output_dir",
                "mts_rows",
                "valid_mts_rows",
                "bound_rows",
                "valid_bound_rows",
                "comparison_rows",
                "passed_rows",
                "blocked_or_failed_rows",
                "claim_allowed",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "claim_blockers": (
            RESIDUALS / "P8_Y5_R10_725_EDGE_CLAIM_BLOCKER_LEDGER.csv",
            claim_blockers,
            [
                "blocker_id",
                "blocker",
                "required_repair",
                "claim_blocked",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "decision_matrix": (
            RESIDUALS / "P8_Y5_R10_725_DECISION_MATRIX.csv",
            decision_matrix,
            ["decision_id", "decision", "meaning", "status", "next_target", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "route_update": (
            RESIDUALS / "P8_Y5_R10_725_ROUTE_UPDATE.csv",
            route_update,
            ["route_id", "allowed_after_725", "forbidden_after_725", "next_action", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "nonclaim_summary": (
            RESIDUALS / "P8_Y5_R10_725_NONCLAIM_SUMMARY.csv",
            nonclaim_summary,
            ["status", "claim_ceiling", "main_result", "hard_blocker", "run_root", "next_target", "valid_for_claim", "source_paths", "generated_utc"],
        ),
    }

    for path, rows, fields in outputs.values():
        write_csv(path, rows, fields)

    generated_paths = [path for path, _, _ in outputs.values()] + [EDGE_SMOKE_PATH]
    formalization_count = formalization_changed_after_cutoff()
    schema_columns = {row["column"] for row in edge_runner_schema}
    runner_claims_blocked = all(row["claim_allowed"] == "false" and row["valid_mts_rows"] == "0" for row in runner_statuses)
    runner_outputs_exist = all((POST_CHECKPOINT / row["output_dir"] / "R10_runner_status.json").exists() for row in runner_statuses)
    validations = [
        {
            "check_id": "V725_0_source_paths_exist",
            "result": "pass" if all(info["path"].exists() for info in SOURCES.values()) else "fail",
            "detail": "all cited source paths exist",
        },
        {
            "check_id": "V725_1_source_needles_present",
            "result": "pass" if all(text_contains(info["path"], info["needles"]) for info in SOURCES.values()) else "fail",
            "detail": "all source files contain expected evidence needles",
        },
        {
            "check_id": "V725_2_prior_724_clean",
            "result": "pass" if prior_validation_clean(SOURCES["724_validation"]["path"]) else "fail",
            "detail": "724 validation has no failures",
        },
        {
            "check_id": "V725_3_724_selected_725",
            "result": "pass" if csv_contains(SOURCES["724_decision"]["path"], "725-Y5-R10-edge-runner-inputs-or-Vdef-owner-repair.md") else "fail",
            "detail": "724 decision matrix selected this checkpoint",
        },
        {
            "check_id": "V725_4_Vdef_repair_not_promoted",
            "result": "pass" if all(row["valid_for_claim"] == "false" for row in vdef_owner_repair_attempt) and any(row["current_status"] == "repair_not_closed_runner_inputs_required" for row in vdef_owner_repair_attempt) else "fail",
            "detail": "Vdef owner remains conditional and unclaimed",
        },
        {
            "check_id": "V725_5_edge_runner_schema_complete",
            "result": "pass" if set(MTS_REQUIRED_COLUMNS).issubset(schema_columns) else "fail",
            "detail": f"schema_columns={len(schema_columns)}",
        },
        {
            "check_id": "V725_6_edge_smoke_rows_nonclaim",
            "result": "pass" if len(edge_smoke_rows) == 4 and all(row["valid_for_claim"] == "false" for row in edge_smoke_rows) else "fail",
            "detail": f"smoke_rows={len(edge_smoke_rows)};valid_for_claim_true=0",
        },
        {
            "check_id": "V725_7_existing_runner_blocks_claim",
            "result": "pass" if runner_claims_blocked else "fail",
            "detail": ";".join(f"{row['runner_id']}:claim_allowed={row['claim_allowed']};valid_mts_rows={row['valid_mts_rows']};valid_bound_rows={row['valid_bound_rows']}" for row in runner_statuses),
        },
        {
            "check_id": "V725_8_runner_outputs_exist",
            "result": "pass" if runner_outputs_exist else "fail",
            "detail": f"run_root={RUN_ROOT}",
        },
        {
            "check_id": "V725_9_claim_blockers_all_true",
            "result": "pass" if all(row["claim_blocked"] == "true" for row in claim_blockers) else "fail",
            "detail": f"blocker_rows={len(claim_blockers)}",
        },
        {
            "check_id": "V725_10_next_target_selected",
            "result": "pass" if all(row["next_target"] == NEXT_TARGET for row in decision_matrix) else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V725_11_no_claim_rows_promoted",
            "result": "pass" if all_valid_false(generated_paths) else "fail",
            "detail": "all generated rows with valid_for_claim remain false",
        },
        {
            "check_id": "V725_12_outputs_scoped",
            "result": "pass" if under_post_checkpoint([OUTPUT_DOC, *generated_paths, RUN_ROOT]) else "fail",
            "detail": "all outputs under post-checkpoint-work",
        },
        {
            "check_id": "V725_13_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V725_14_no_local_arena_claim",
            "result": "pass" if "no_R10_WEP_PPN_Newton_or_local_GR_pass" in nonclaim_summary[0]["claim_ceiling"] else "fail",
            "detail": "R10/WEP/PPN/Newton/local-GR claims remain blocked",
        },
        {
            "check_id": "V725_15_source_register_written",
            "result": "pass" if len(source_register) >= 12 else "fail",
            "detail": f"source_rows={len(source_register)}",
        },
        {
            "check_id": "V725_16_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]

    validation_path = RESIDUALS / "P8_Y5_BRR545_725_VALIDATION.csv"
    write_csv(validation_path, validations, ["check_id", "result", "detail"])

    doc = f"""# 725 - Y5 R10 Edge Runner Inputs Or Vdef Owner Repair

## Summary

This checkpoint tries the clean route first: repair the affine/topological `V_def` owner so the local edge branch dies by theorem.

Current verdict: **not closed**. The affine variation is still a useful skeleton, but the parent-owned `P[Y]`, `J_eff[Y]`, `A[Y]`, boundary counterterm, symplectic generator, projector descent, and matter descent are not signed.

So the fallback is made executable without becoming a claim: current 725 runner-shaped edge rows are written to:

`source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_edge_residual_smoke_725.csv`

Both R10 runner branches correctly block claim status.

| Field | Value |
| --- | --- |
| Generated UTC | `{GENERATED_UTC}` |
| Claim status | private/nonclaim checkpoint |
| Run root | `{RUN_ROOT}` |
| Next target | `{NEXT_TARGET}` |

## Vdef Owner Repair Attempt

{markdown_table(vdef_owner_repair_attempt, ["repair_id", "target", "current_status", "failure_mode", "claim_effect", "valid_for_claim"])}

## Edge Runner Schema

{markdown_table(edge_runner_schema, ["column", "purpose", "edge_branch_status", "valid_for_claim"])}

## Edge Smoke Rows

{markdown_table(edge_smoke_rows, ["model_id", "branch_id", "lambda_value", "alpha_predicted", "alpha_bound", "derivation_status", "valid_for_claim"])}

## Runner Status Summary

{markdown_table(runner_statuses, ["runner_id", "bound_curve", "mts_rows", "valid_mts_rows", "bound_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "valid_for_claim"])}

## Claim Blocker Ledger

{markdown_table(claim_blockers, ["blocker_id", "blocker", "required_repair", "claim_blocked", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decision_matrix, ["decision_id", "decision", "status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(route_update, ["route_id", "allowed_after_725", "forbidden_after_725", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(nonclaim_summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## Practical Read

This is exactly the guardrail we wanted. The edge residual can now enter the existing R10 machinery, but the machinery refuses to score it because the physics ingredients are not claim-grade. The next serious route is still derivation-first: either map the affine `V_def` owner to the actual parent variables, or admit the edge branch needs real sourced `lambda_edge`, `K_edge`, `Qbar_edge_XH`, and `qbar_XT` rows before it can face local bounds.
"""

    OUTPUT_DOC.write_text(doc, encoding="utf-8")
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {validation_path}")
    print(f"wrote {EDGE_SMOKE_PATH}")
    print(f"validation_passes={sum(row['result'] == 'pass' for row in validations)}/{len(validations)}")
    print(";".join(f"{row['runner_id']}:claim_allowed={row['claim_allowed']}" for row in runner_statuses))
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
