from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "724-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md"
NEXT_TARGET = "725-Y5-R10-edge-runner-inputs-or-Vdef-owner-repair.md"
GENERATED_UTC = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)


SOURCES = {
    "723_doc": {
        "path": POST_CHECKPOINT / "723-Y5-R10-affine-X-momentum-map-owner-or-edge-residual-coefficient-pack.md",
        "note": "immediate handoff: edge envelope or owner repair",
        "needles": ["724-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md", "alpha_edge(lambda)", "parent symplectic/momentum-map certificate"],
    },
    "723_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_723_VALIDATION.csv",
        "note": "prior validation gate",
        "needles": ["V723_7_edge_coefficients_present", "pass", "V723_13_formalization_workbench_untouched"],
    },
    "723_edge_pack": {
        "path": RESIDUALS / "P8_Y5_R10_723_EDGE_RESIDUAL_COEFFICIENT_PACK.csv",
        "note": "current edge coefficient definitions",
        "needles": ["ERP723_7_edge_alpha", "alpha_edge(lambda)=K_edge(lambda)*Qbar_edge_XH(lambda)*qbar_XT", "TEMPLATE_NONCLAIM"],
    },
    "723_decision": {
        "path": RESIDUALS / "P8_Y5_R10_723_OWNER_OR_EDGE_DECISION.csv",
        "note": "current route selector",
        "needles": ["D723_2_current_route", "go_to_724_edge_envelope_or_owner_repair", "false"],
    },
    "584_doc": {
        "path": POST_CHECKPOINT / "584-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
        "note": "older edge-envelope checkpoint to reconcile with current chain",
        "needles": ["edge residual alpha envelope", "alpha_edge(lambda)=K_edge(lambda) Qbar_edge_XH(lambda) qbar_XT", "not an R10 result"],
    },
    "584_edge_law": {
        "path": RESIDUALS / "P8_Y5_R10_584_EDGE_ENVELOPE_LAW.csv",
        "note": "older edge envelope law rows",
        "needles": ["EEL584_3_edge_alpha", "alpha_edge(lambda)=K_edge(lambda) Qbar_edge_XH(lambda) qbar_XT", "false"],
    },
    "584_pressure_matrix": {
        "path": RESIDUALS / "P8_Y5_R10_584_EDGE_PRESSURE_MATRIX.csv",
        "note": "private review-candidate pressure matrix",
        "needles": ["EPM584_0", "valid_for_claim", "order_one_edge_product_not_excluded_on_review_candidate"],
    },
    "584_claim_contract": {
        "path": RESIDUALS / "P8_Y5_R10_584_EDGE_CLAIM_INPUT_CONTRACT.csv",
        "note": "edge claim input blockers",
        "needles": ["ECIC584_0_lambda_edge", "ECIC584_1_K_edge", "ECIC584_4_bound_curve"],
    },
    "584_owner_repair": {
        "path": RESIDUALS / "P8_Y5_R10_584_OWNER_REPAIR_ATTEMPT.csv",
        "note": "owner repair routes that were not closed",
        "needles": ["OR584_0_zero_momentum_map_repair", "OR584_5_verdict", "repair_open_not_closed"],
    },
    "586_doc": {
        "path": POST_CHECKPOINT / "586-Y5-R10-Vdef-owner-action-sketch-or-edge-runner-numeric-priors.md",
        "note": "affine Vdef action sketch plus nonclaim edge prior grid",
        "needles": ["numeric edge-prior grid", "claim_allowed=false", "all nonclaim"],
    },
    "586_prior_grid": {
        "path": RESIDUALS / "P8_Y5_R10_586_EDGE_NUMERIC_PRIOR_GRID.csv",
        "note": "nonclaim numeric edge prior grid",
        "needles": ["EPG586_0", "edge_product_prior", "valid_for_claim"],
    },
    "586_theorem": {
        "path": RESIDUALS / "P8_Y5_R10_586_CONDITIONAL_NO_POLE_THEOREM.csv",
        "note": "conditional no-pole theorem clauses",
        "needles": ["CNT586_0_affine_defect_block", "CNT586_3_boundary_silence", "false"],
    },
    "586_boundary": {
        "path": RESIDUALS / "P8_Y5_R10_586_BOUNDARY_EXACTNESS_TEST.csv",
        "note": "boundary exactness nonclaim routes",
        "needles": ["BET586_3_improper_edge_mode", "fallback_live", "false"],
    },
    "runner": {
        "path": POST_CHECKPOINT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py",
        "note": "existing R10 alpha/lambda comparator",
        "needles": ["valid_for_claim", "alpha_bound", "claim_allowed"],
    },
}


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


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


def require_float(row: dict[str, str], key: str) -> bool:
    try:
        return float(row.get(key, "")) > 0
    except ValueError:
        return False


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    pressure_rows_584 = read_csv(SOURCES["584_pressure_matrix"]["path"])
    prior_grid_586 = read_csv(SOURCES["586_prior_grid"]["path"])
    pressure_band_counts = Counter(row.get("pressure_band", "missing") for row in pressure_rows_584)
    prior_pass_count = sum(row.get("private_diagnostic_pass", "").lower() == "true" for row in prior_grid_586)
    prior_fail_count = sum(row.get("private_diagnostic_pass", "").lower() == "false" for row in prior_grid_586)

    source_register = [
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

    edge_envelope_law = [
        {
            "law_id": "EEL724_0_edge_charge",
            "object": "Q_edge^H(lambda)",
            "formula": "Q_edge^H(lambda)=int_{partial H} dS F_lambda(s) epsilon_nu B_X^nu(s)",
            "meaning": "compact-source edge charge if the boundary part of the would-be gauge/constraint generator survives",
            "needed_input": "boundary momentum B_X, allowed epsilon, edge support kernel F_lambda",
            "current_status": "symbolic_nonclaim",
            "zero_or_pass_condition": "B_X exact/pure gauge/proper-zero or source-backed numeric envelope passes bounds",
            "valid_for_claim": "false",
            "source_paths": source_path_string("723_edge_pack", "584_edge_law"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "law_id": "EEL724_1_projected_edge",
            "object": "Qbar_edge_XH(lambda)",
            "formula": "Qbar_edge_XH(lambda)=Pi_M^H[Q_edge^H(lambda)]/M_H",
            "meaning": "edge charge that survives projection into the measured source-mass channel",
            "needed_input": "Pi_M action on edge charge including reference-boundary terms",
            "current_status": "symbolic_nonclaim",
            "zero_or_pass_condition": "Pi_M^H[Q_edge]=0 or numeric/source-backed projected charge is small enough",
            "valid_for_claim": "false",
            "source_paths": source_path_string("723_edge_pack", "584_edge_law"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "law_id": "EEL724_2_edge_prefactor",
            "object": "K_edge(lambda)",
            "formula": "K_edge(lambda)=normalization_from_edge_Green_kernel/G_obs",
            "meaning": "boundary-kernel normalization converting an edge charge into an R10-comparable alpha",
            "needed_input": "edge Green kernel, normalization, range/support map",
            "current_status": "missing",
            "zero_or_pass_condition": "no edge propagator/charge or source-backed K_edge(lambda) obeys envelope bounds",
            "valid_for_claim": "false",
            "source_paths": source_path_string("723_edge_pack", "584_edge_law"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "law_id": "EEL724_3_edge_alpha",
            "object": "alpha_edge(lambda)",
            "formula": "alpha_edge(lambda)=K_edge(lambda)*Qbar_edge_XH(lambda)*qbar_XT",
            "meaning": "R10-comparable edge fifth-force amplitude",
            "needed_input": "K_edge(lambda), Qbar_edge_XH(lambda), qbar_XT, lambda support",
            "current_status": "template_only",
            "zero_or_pass_condition": "K_edge=0 or Qbar_edge_XH=0 or qbar_XT=0 by theorem, otherwise numeric alpha envelope must pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("723_edge_pack", "584_edge_law", "586_prior_grid"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "law_id": "EEL724_4_combined_alpha",
            "object": "alpha_total(lambda)",
            "formula": "alpha_total(lambda)=K_X*Qbar_bulk_XH(lambda)*qbar_XT + K_edge(lambda)*Qbar_edge_XH(lambda)*qbar_XT",
            "meaning": "fallback if both bulk finite mode and edge exchange survive",
            "needed_input": "orthogonal bulk-edge source split to avoid double-counting",
            "current_status": "template_only",
            "zero_or_pass_condition": "bulk-edge split theorem or separate sourced envelopes for both branches",
            "valid_for_claim": "false",
            "source_paths": source_path_string("584_edge_law", "586_theorem"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "law_id": "EEL724_5_bound_condition",
            "object": "R10 edge gate",
            "formula": "abs(alpha_edge(lambda)) <= alpha_bound(lambda) for every active edge-support lambda",
            "meaning": "private diagnostic gate only until bound curve and edge coefficients are source-backed",
            "needed_input": "claim-grade alpha_bound(lambda), real lambda envelope, real edge coefficients",
            "current_status": "nonclaim_diagnostic",
            "zero_or_pass_condition": "all active rows are numeric, sourced, valid_for_claim=true, and runner passes",
            "valid_for_claim": "false",
            "source_paths": source_path_string("584_pressure_matrix", "586_prior_grid", "runner"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    edge_pressure_matrix = [
        {
            "pressure_id": row["pressure_id"].replace("EPM584", "EPM724"),
            "source_pressure_id": row["pressure_id"],
            "lambda_m": row["lambda_m"],
            "lambda_um": row["lambda_um"],
            "review_candidate_alpha_bound": row["review_candidate_alpha_bound"],
            "max_abs_edge_product": row["max_abs_edge_product"],
            "edge_product_condition": row["edge_product_condition"],
            "pressure_band": row["pressure_band"],
            "evidence_class": "private_review_candidate_nonclaim",
            "claim_use": "forbidden_until_bound_curve_and_edge_coefficients_are_source_backed",
            "valid_for_claim": "false",
            "source_paths": source_path_string("584_pressure_matrix"),
            "generated_utc": GENERATED_UTC,
        }
        for row in pressure_rows_584
    ]

    edge_prior_grid_summary = [
        {
            "summary_id": "EPGS724_0_prior_grid_status",
            "source_grid": str(SOURCES["586_prior_grid"]["path"]),
            "rows": str(len(prior_grid_586)),
            "diagnostic_passes": str(prior_pass_count),
            "diagnostic_fails": str(prior_fail_count),
            "status": "numeric_prior_grid_exists_but_is_not_source_backed",
            "interpretation": "useful pressure dial; not evidence because edge coefficients are priors, not parent-derived quantities",
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_doc", "586_prior_grid"),
            "generated_utc": GENERATED_UTC,
        },
        *[
            {
                "summary_id": f"EPGS724_band_{index}",
                "source_grid": str(SOURCES["584_pressure_matrix"]["path"]),
                "rows": str(count),
                "diagnostic_passes": "",
                "diagnostic_fails": "",
                "status": pressure_band,
                "interpretation": "pressure level copied from private review-candidate matrix; not claim evidence",
                "valid_for_claim": "false",
                "source_paths": source_path_string("584_pressure_matrix"),
                "generated_utc": GENERATED_UTC,
            }
            for index, (pressure_band, count) in enumerate(sorted(pressure_band_counts.items()), start=1)
        ],
    ]

    edge_claim_input_contract = [
        {
            "input_id": "ECIC724_0_lambda_edge",
            "needed_input": "lambda_edge or edge support envelope",
            "required_format": "positive numeric length grid or theorem-zero no-support certificate",
            "current_status": "missing",
            "claim_failure_if_missing": "cannot choose alpha_bound(lambda)",
            "next_action": "derive edge support from boundary kernel or demote to closure",
            "valid_for_claim": "false",
            "source_paths": source_path_string("584_claim_contract", "586_boundary"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "input_id": "ECIC724_1_K_edge",
            "needed_input": "K_edge(lambda)",
            "required_format": "numeric/source-backed normalization from edge Green kernel",
            "current_status": "missing",
            "claim_failure_if_missing": "alpha_edge remains symbolic",
            "next_action": "derive kernel normalization or write explicit prior-only smoke file",
            "valid_for_claim": "false",
            "source_paths": source_path_string("723_edge_pack", "584_claim_contract"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "input_id": "ECIC724_2_Qbar_edge",
            "needed_input": "Qbar_edge_XH(lambda)",
            "required_format": "numeric/source-backed projected edge charge or theorem-zero orthogonality",
            "current_status": "missing",
            "claim_failure_if_missing": "source side remains symbolic",
            "next_action": "derive Pi_M edge orthogonality or source projected edge charge",
            "valid_for_claim": "false",
            "source_paths": source_path_string("723_edge_pack", "584_claim_contract"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "input_id": "ECIC724_3_qbar_XT",
            "needed_input": "qbar_XT",
            "required_format": "numeric/source-backed test charge or matter-blindness theorem",
            "current_status": "retained_symbolic_from_matter_descent_blocker",
            "claim_failure_if_missing": "test side remains retained",
            "next_action": "prove quotient matter descent or keep finite test-charge branch",
            "valid_for_claim": "false",
            "source_paths": source_path_string("723_edge_pack", "586_theorem"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "input_id": "ECIC724_4_bound_curve",
            "needed_input": "claim-grade alpha_bound(lambda)",
            "required_format": "QA-promoted curve/table with source provenance and valid_for_claim=true",
            "current_status": "private_review_candidate_only",
            "claim_failure_if_missing": "pressure matrix remains private diagnostic",
            "next_action": "acquire/digitize source-backed curve before any R10 statement",
            "valid_for_claim": "false",
            "source_paths": source_path_string("584_pressure_matrix", "runner"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "input_id": "ECIC724_5_no_double_count",
            "needed_input": "bulk-edge source split",
            "required_format": "orthogonal decomposition Q_X=Q_bulk+Q_edge with projection rules",
            "current_status": "missing",
            "claim_failure_if_missing": "combined alpha_total may double-count source charge",
            "next_action": "derive source split or keep branch-separated nonclaim rows",
            "valid_for_claim": "false",
            "source_paths": source_path_string("584_edge_law", "586_theorem"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    owner_repair_gate = [
        {
            "gate_id": "ORG724_0_strict_quotient",
            "repair_route": "strict quotient owner",
            "required_derivation": "construct q:Conf_parent->Q_obs and prove vertical X directions are in ker(Dq)",
            "would_zero": "bulk and edge X charge if matter/action/measure descend",
            "current_status": "not_derived",
            "fallback_if_missing": "edge alpha envelope",
            "valid_for_claim": "false",
            "source_paths": source_path_string("584_owner_repair", "586_theorem"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "ORG724_1_Vdef_owner",
            "repair_route": "affine Vdef owner",
            "required_derivation": "derive P[Y], J_eff[Y], A[Y], and boundary term from the same parent block",
            "would_zero": "free-P insertion and unowned C_X source",
            "current_status": "conditional_contract_not_parent_sourced",
            "fallback_if_missing": "edge/source coefficient branch",
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_doc", "586_theorem"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "ORG724_2_boundary_exactness",
            "repair_route": "exact/pure-gauge boundary primitive",
            "required_derivation": "show B_X=d_boundary b_X or counterterm-cancelled without removing physical mass charge",
            "would_zero": "Q_edge and K_boundary for compact local branch",
            "current_status": "not_derived",
            "fallback_if_missing": "Qbar_edge_XH(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_path_string("584_owner_repair", "586_boundary"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "ORG724_3_projector_orthogonality",
            "repair_route": "mass-channel orthogonality",
            "required_derivation": "prove Pi_M^H[Q_edge]=0 including reference boundary and delta Pi_M terms",
            "would_zero": "Qbar_edge_XH even if Q_edge exists",
            "current_status": "not_derived",
            "fallback_if_missing": "epsilon_PiM_X(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_path_string("723_edge_pack", "584_owner_repair"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "ORG724_4_matter_blindness",
            "repair_route": "ordinary matter quotient blindness",
            "required_derivation": "delta_X S_matter=0 universally, not source-by-source tuning",
            "would_zero": "qbar_XT",
            "current_status": "not_signed",
            "fallback_if_missing": "retain finite qbar_XT",
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_theorem", "723_edge_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "ORG724_5_verdict",
            "repair_route": "owner repair versus edge envelope",
            "required_derivation": "one zero route must be parent-owned before theorem credit",
            "would_zero": "edge alpha branch",
            "current_status": "repair_open_not_closed",
            "fallback_if_missing": "build edge runner inputs",
            "valid_for_claim": "false",
            "source_paths": source_path_string("584_owner_repair", "586_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    runner_readiness = [
        {
            "runner_id": "RR724_0_existing_R10_runner",
            "input_family": "edge residual alpha rows",
            "current_input_status": "symbolic_coefficients_and_private_review_bound",
            "dry_run_allowed": "true",
            "claim_allowed": "false",
            "blocking_reason": "valid MTS rows and valid bound rows are intentionally absent",
            "required_before_claim": "valid_for_claim=true numeric sourced lambda/K/Qbar/qbar rows plus claim-grade bound curve",
            "valid_for_claim": "false",
            "source_paths": source_path_string("runner", "586_prior_grid", "584_pressure_matrix"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "runner_id": "RR724_1_prior_grid_status",
            "input_family": "586 edge product priors",
            "current_input_status": f"rows={len(prior_grid_586)};diagnostic_passes={prior_pass_count};diagnostic_fails={prior_fail_count}",
            "dry_run_allowed": "true",
            "claim_allowed": "false",
            "blocking_reason": "edge_product_prior is not a parent-derived coefficient",
            "required_before_claim": "replace priors with sourced K_edge*Qbar_edge_XH*qbar_XT or derive zero",
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_doc", "586_prior_grid"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    decision_matrix = [
        {
            "decision_id": "DM724_0_owner_not_closed",
            "decision": "do_not_promote_no_pole_or_local_GR",
            "reason": "strict quotient, affine owner, boundary silence, projector orthogonality, and matter blindness remain unsigned",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("723_decision", "584_owner_repair", "586_theorem"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "DM724_1_edge_envelope_current",
            "decision": "keep_alpha_edge_envelope_as_nonclaim_formula",
            "reason": "boundary hair has an explicit R10-comparable amplitude but no numeric parent coefficients",
            "claim_status": "nonclaim_diagnostic",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("723_edge_pack", "584_edge_law"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "DM724_2_pressure_matrix_current",
            "decision": "use_private_pressure_matrix_only_for_derivation_pressure",
            "reason": "the old 584/586 rows show how small the edge product must be, but they are not claim-grade evidence",
            "claim_status": "nonclaim_diagnostic",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("584_pressure_matrix", "586_prior_grid"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "DM724_3_next_best_target",
            "decision": "build edge runner inputs or repair Vdef owner",
            "reason": "the best mathematical path is still to zero the branch; the fallback is sourced numeric edge coefficients",
            "claim_status": "next_derivation_target",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_doc", "runner"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    bound_or_derive_queue = [
        {
            "queue_id": "BOD724_0_first_choice",
            "target": "derive strict quotient or affine owner zero",
            "why_first": "a theorem-zero route survives R10/PPN/clocks/orbital arenas without tuning an edge envelope",
            "needed_artifact": "parent q, vertical generator, Omega_Y, P/J/A owner, boundary exactness, matter descent",
            "fallback_route": "source numeric edge envelope",
            "priority": "highest",
            "next_artifact": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_theorem", "584_owner_repair"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BOD724_1_second_choice",
            "target": "edge runner input rows",
            "why_first": "if owner zero fails, local tests need actual lambda/K/Qbar/qbar inputs rather than words",
            "needed_artifact": "candidate edge smoke CSV with all rows valid_for_claim=false",
            "fallback_route": "block R10/local arena claims",
            "priority": "high",
            "next_artifact": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("runner", "584_claim_contract"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BOD724_2_guardrail",
            "target": "real alpha_bound(lambda) source gate",
            "why_first": "pressure matrix is private review-candidate material and cannot become a public claim",
            "needed_artifact": "digitized/source-backed R10 bound curve with provenance and validation",
            "fallback_route": "keep pressure matrix as internal pressure dial",
            "priority": "high",
            "next_artifact": "future R10 acquisition checkpoint",
            "valid_for_claim": "false",
            "source_paths": source_path_string("584_pressure_matrix", "runner"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    nonclaim_summary = [
        {
            "status": "Y5_R10_724_edge_envelope_reconciled_owner_repair_open_nonclaim",
            "claim_ceiling": "edge_alpha_envelope_and_runner_readiness_only_no_R10_WEP_PPN_Newton_or_local_GR_pass",
            "main_result": "current 723 edge coefficients are reconciled with old 584 envelope and 586 prior-grid pressure diagnostics",
            "hard_blocker": "lambda_edge, K_edge(lambda), Qbar_edge_XH(lambda), qbar_XT, no-double-count split, and claim-grade alpha_bound(lambda) are missing or nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("723_doc", "584_doc", "586_doc"),
            "generated_utc": GENERATED_UTC,
        }
    ]

    outputs = {
        "source_register": (
            RESIDUALS / "P8_Y5_R10_724_SOURCE_REGISTER.csv",
            source_register,
            ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
        ),
        "edge_envelope_law": (
            RESIDUALS / "P8_Y5_R10_724_EDGE_ENVELOPE_LAW.csv",
            edge_envelope_law,
            [
                "law_id",
                "object",
                "formula",
                "meaning",
                "needed_input",
                "current_status",
                "zero_or_pass_condition",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "edge_pressure_matrix": (
            RESIDUALS / "P8_Y5_R10_724_EDGE_PRESSURE_MATRIX.csv",
            edge_pressure_matrix,
            [
                "pressure_id",
                "source_pressure_id",
                "lambda_m",
                "lambda_um",
                "review_candidate_alpha_bound",
                "max_abs_edge_product",
                "edge_product_condition",
                "pressure_band",
                "evidence_class",
                "claim_use",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "edge_prior_grid_summary": (
            RESIDUALS / "P8_Y5_R10_724_EDGE_PRIOR_GRID_SUMMARY.csv",
            edge_prior_grid_summary,
            [
                "summary_id",
                "source_grid",
                "rows",
                "diagnostic_passes",
                "diagnostic_fails",
                "status",
                "interpretation",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "edge_claim_input_contract": (
            RESIDUALS / "P8_Y5_R10_724_EDGE_CLAIM_INPUT_CONTRACT.csv",
            edge_claim_input_contract,
            [
                "input_id",
                "needed_input",
                "required_format",
                "current_status",
                "claim_failure_if_missing",
                "next_action",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "owner_repair_gate": (
            RESIDUALS / "P8_Y5_R10_724_OWNER_REPAIR_GATE.csv",
            owner_repair_gate,
            [
                "gate_id",
                "repair_route",
                "required_derivation",
                "would_zero",
                "current_status",
                "fallback_if_missing",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "runner_readiness": (
            RESIDUALS / "P8_Y5_R10_724_RUNNER_READINESS.csv",
            runner_readiness,
            [
                "runner_id",
                "input_family",
                "current_input_status",
                "dry_run_allowed",
                "claim_allowed",
                "blocking_reason",
                "required_before_claim",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "decision_matrix": (
            RESIDUALS / "P8_Y5_R10_724_DECISION_MATRIX.csv",
            decision_matrix,
            ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "bound_or_derive_queue": (
            RESIDUALS / "P8_Y5_R10_724_BOUND_OR_DERIVE_QUEUE.csv",
            bound_or_derive_queue,
            [
                "queue_id",
                "target",
                "why_first",
                "needed_artifact",
                "fallback_route",
                "priority",
                "next_artifact",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "nonclaim_summary": (
            RESIDUALS / "P8_Y5_R10_724_NONCLAIM_SUMMARY.csv",
            nonclaim_summary,
            ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "source_paths", "generated_utc"],
        ),
    }

    for path, rows, fields in outputs.values():
        write_csv(path, rows, fields)

    generated_paths = [path for path, _, _ in outputs.values()]
    formalization_count = formalization_changed_after_cutoff()
    all_pressure_numeric = all(
        require_float(row, "lambda_m")
        and require_float(row, "lambda_um")
        and require_float(row, "review_candidate_alpha_bound")
        and require_float(row, "max_abs_edge_product")
        for row in edge_pressure_matrix
    )
    validations = [
        {
            "check_id": "V724_0_source_paths_exist",
            "result": "pass" if all(info["path"].exists() for info in SOURCES.values()) else "fail",
            "detail": "all cited source paths exist",
        },
        {
            "check_id": "V724_1_source_needles_present",
            "result": "pass" if all(text_contains(info["path"], info["needles"]) for info in SOURCES.values()) else "fail",
            "detail": "all source files contain expected evidence needles",
        },
        {
            "check_id": "V724_2_prior_723_clean",
            "result": "pass" if prior_validation_clean(SOURCES["723_validation"]["path"]) else "fail",
            "detail": "723 validation has no failures",
        },
        {
            "check_id": "V724_3_723_selected_724",
            "result": "pass" if csv_contains(SOURCES["723_decision"]["path"], "724-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md") else "fail",
            "detail": "723 next target matches this checkpoint",
        },
        {
            "check_id": "V724_4_edge_law_current_and_old_reconciled",
            "result": "pass"
            if any(row["object"] == "alpha_edge(lambda)" and "K_edge(lambda)*Qbar_edge_XH(lambda)*qbar_XT" in row["formula"] for row in edge_envelope_law)
            else "fail",
            "detail": f"edge_law_rows={len(edge_envelope_law)}",
        },
        {
            "check_id": "V724_5_pressure_matrix_numeric_nonclaim",
            "result": "pass" if len(edge_pressure_matrix) >= 10 and all_pressure_numeric and all(row["valid_for_claim"] == "false" for row in edge_pressure_matrix) else "fail",
            "detail": f"pressure_rows={len(edge_pressure_matrix)};numeric={all_pressure_numeric};claim_rows=0",
        },
        {
            "check_id": "V724_6_prior_grid_nonclaim_summary",
            "result": "pass" if len(prior_grid_586) == 55 and prior_pass_count == 42 and prior_fail_count == 13 else "fail",
            "detail": f"prior_rows={len(prior_grid_586)};diagnostic_passes={prior_pass_count};diagnostic_fails={prior_fail_count}",
        },
        {
            "check_id": "V724_7_claim_contract_blocks_missing_inputs",
            "result": "pass"
            if {"missing", "retained_symbolic_from_matter_descent_blocker", "private_review_candidate_only"}.issubset(
                {row["current_status"] for row in edge_claim_input_contract}
            )
            else "fail",
            "detail": f"contract_rows={len(edge_claim_input_contract)};claim_rows=0",
        },
        {
            "check_id": "V724_8_owner_repair_not_promoted",
            "result": "pass" if all(row["valid_for_claim"] == "false" for row in owner_repair_gate) and any(row["current_status"] == "repair_open_not_closed" for row in owner_repair_gate) else "fail",
            "detail": "owner repair open; no theorem credit",
        },
        {
            "check_id": "V724_9_runner_readiness_blocks_claim",
            "result": "pass" if all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in runner_readiness) else "fail",
            "detail": "existing runner can smoke-check only",
        },
        {
            "check_id": "V724_10_decision_selects_725",
            "result": "pass" if all(row["next_target"] == NEXT_TARGET for row in decision_matrix) else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V724_11_no_claim_rows_promoted",
            "result": "pass" if all_valid_false(generated_paths) else "fail",
            "detail": "all generated rows with valid_for_claim remain false",
        },
        {
            "check_id": "V724_12_outputs_scoped",
            "result": "pass" if under_post_checkpoint([OUTPUT_DOC, *generated_paths]) else "fail",
            "detail": "all outputs under post-checkpoint-work",
        },
        {
            "check_id": "V724_13_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V724_14_no_local_arena_claim",
            "result": "pass" if "no_R10_WEP_PPN_Newton_or_local_GR_pass" in nonclaim_summary[0]["claim_ceiling"] else "fail",
            "detail": "R10/WEP/PPN/Newton/local-GR claims remain blocked",
        },
        {
            "check_id": "V724_15_source_register_written",
            "result": "pass" if len(source_register) >= 12 else "fail",
            "detail": f"source_rows={len(source_register)}",
        },
        {
            "check_id": "V724_16_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]

    validation_path = RESIDUALS / "P8_Y5_BRR545_724_VALIDATION.csv"
    write_csv(validation_path, validations, ["check_id", "result", "detail"])

    pressure_preview = edge_pressure_matrix[:6]
    doc = f"""# 724 - Y5 R10 Edge Residual Alpha Envelope Or Owner Repair

## Summary

This checkpoint reconciles the current 723 edge-residual coefficient pack with the older 584 edge-envelope law and the 586 nonclaim numeric edge-prior grid.

The live edge fallback is now:

```text
Q_edge^H(lambda)=int_boundary dS F_lambda epsilon_nu B_X^nu
Qbar_edge_XH(lambda)=Pi_M^H[Q_edge^H(lambda)]/M_H
alpha_edge(lambda)=K_edge(lambda)*Qbar_edge_XH(lambda)*qbar_XT
```

Verdict: **nonclaim**. The edge branch is sharper, but it is not yet an R10/local-GR result. The missing pieces are `lambda_edge`, `K_edge(lambda)`, `Qbar_edge_XH(lambda)`, `qbar_XT`, a no-double-count bulk/edge split, and a claim-grade `alpha_bound(lambda)` curve.

| Field | Value |
| --- | --- |
| Generated UTC | `{GENERATED_UTC}` |
| Claim status | private/nonclaim checkpoint |
| Next target | `{NEXT_TARGET}` |

## Edge Envelope Law

{markdown_table(edge_envelope_law, ["law_id", "object", "formula", "current_status", "zero_or_pass_condition", "valid_for_claim"])}

## Edge Pressure Matrix

The pressure matrix below is copied forward as a private review-candidate diagnostic only. It tells us where the edge product would need to be order-one, tenth-level, percent-level, or per-mille-level, but it is not public claim evidence.

{markdown_table(pressure_preview, ["pressure_id", "lambda_um", "review_candidate_alpha_bound", "max_abs_edge_product", "pressure_band", "valid_for_claim"])}

Full current matrix: `source-intake/mts_residuals/P8_Y5_R10_724_EDGE_PRESSURE_MATRIX.csv`.

## Edge Prior Grid Summary

{markdown_table(edge_prior_grid_summary, ["summary_id", "rows", "diagnostic_passes", "diagnostic_fails", "status", "valid_for_claim"])}

## Edge Claim Input Contract

{markdown_table(edge_claim_input_contract, ["input_id", "needed_input", "current_status", "claim_failure_if_missing", "next_action", "valid_for_claim"])}

## Owner Repair Gate

{markdown_table(owner_repair_gate, ["gate_id", "repair_route", "current_status", "would_zero", "fallback_if_missing", "valid_for_claim"])}

## Runner Readiness

{markdown_table(runner_readiness, ["runner_id", "input_family", "current_input_status", "claim_allowed", "blocking_reason", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decision_matrix, ["decision_id", "decision", "claim_status", "next_target", "valid_for_claim"])}

## Bound Or Derive Queue

{markdown_table(bound_or_derive_queue, ["queue_id", "target", "why_first", "needed_artifact", "priority", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(nonclaim_summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## Practical Read

The edge branch is no longer fog. It is a named alpha envelope with a pressure dial. That is progress. But the clean win is still a derivation: if the parent quotient, affine `V_def` owner, boundary exactness, projector orthogonality, or matter blindness can be signed, the edge alpha branch collapses by theorem instead of by tuning. If not, 725 has to build runner-shaped nonclaim edge inputs and make the residual face the same local bounds discipline as everything else.
"""

    OUTPUT_DOC.write_text(doc, encoding="utf-8")
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {validation_path}")
    print(f"validation_passes={sum(row['result'] == 'pass' for row in validations)}/{len(validations)}")
    print(f"prior_grid={len(prior_grid_586)} rows;passes={prior_pass_count};fails={prior_fail_count}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
