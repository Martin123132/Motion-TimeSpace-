from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "832-Y5-R10-tracefree-divergence-range-theorem-or-cokernel-bound.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_832_SOURCE_REGISTER.csv"
FLAT_PROOF_PATH = RESIDUALS / "P8_Y5_R10_832_FLAT_RIGHT_INVERSE_PROOF.csv"
CURVED_BOUND_PATH = RESIDUALS / "P8_Y5_R10_832_CURVED_OBSTRUCTION_BOUND.csv"
PHYSICAL_GAP_PATH = RESIDUALS / "P8_Y5_R10_832_PHYSICAL_GAP_LEDGER.csv"
RUNNER_INPUT_PATH = RESIDUALS / "P8_Y5_R10_832_BOUND_RUNNER_INPUT_TEMPLATE.csv"
RUNNER_OUTPUT_PATH = RESIDUALS / "P8_Y5_R10_832_BOUND_RUNNER_OUTPUT.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_832_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_832_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_832_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_832_VALIDATION.csv"

STATUS = "Y5_R10_832_flat_tracefree_divergence_right_inverse_derived_curved_boundary_amplitude_open_nonclaim"
CLAIM_CEILING = "flat_bulk_Khat_cancellation_theorem_only_no_parent_action_no_PPN_or_local_GR_pass"
NEXT_TARGET = "833-Y5-R10-Hessian-Khat-carrier-amplitude-and-metric-response-bound.md"

SOURCE_SPECS = [
    {
        "source_id": "831_doc",
        "path": POST_CHECKPOINT / "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md",
        "needles": [
            "P_coker(D_T)G=0",
            "RT831_2_exact_zero",
            "832-Y5-R10-tracefree-divergence-range-theorem-or-cokernel-bound.md",
        ],
        "role": "immediate range/cokernel handoff",
    },
    {
        "source_id": "831_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_831_VALIDATION.csv",
        "needles": [
            "V831_3_range_cokernel_theorem_recorded,pass",
            "V831_4_parent_adoption_blocked,pass",
            "V831_11_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "794_tracefree_solver",
        "path": POST_CHECKPOINT / "794-Y5-R10-tracefree-longitudinal-Khat-solver-or-PPN-bound.md",
        "needles": [
            "V794_5_flat_cancel",
            "trace-free condition does not kill the cancellation route",
            "solver not adopted as proof",
        ],
        "role": "earlier flat trace-free cancellation clue",
    },
    {
        "source_id": "795_parent_origin",
        "path": POST_CHECKPOINT / "795-Y5-R10-parent-origin-of-tracefree-Khat-solver-or-amplitude-bound.md",
        "needles": [
            "KAB795_1_Newton_fraction",
            "KAB795_2_PPN_vector",
            "parent_origin_missing",
        ],
        "role": "amplitude and parent-origin warning",
    },
    {
        "source_id": "830_runner_gate",
        "path": POST_CHECKPOINT / "830-Y5-R10-Khat-boundary-owner-or-residual-vector-runner.md",
        "needles": [
            "missing_parent_operator",
            "missing_response_matrix",
            "no_local_GR_claim",
        ],
        "role": "nonclaim Khat owner and response-matrix gate",
    },
    {
        "source_id": "equation_register_q",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "q^nu = nabla^nu Gamma_eff - nabla_mu K_hat",
            "The real Solar branch remains open until `q_loc(x)`, boundary data, and amplitude bounds are supplied.",
            "Source-support / boundary-amplitude law",
        ],
        "role": "equation register q/Khat and boundary-amplitude obligations",
    },
]

REQUIRED_NUMERIC_FIELDS = [
    "Ricci_norm",
    "grad_laplace_inverse_Gamma_norm",
    "boundary_flux_norm",
    "regularizer_residual_norm",
    "Khat_amplitude_norm",
    "metric_response_norm",
    "observable_limit",
]
REQUIRED_SOURCE_FIELDS = [
    "Gamma_source_path",
    "boundary_condition_source_path",
    "curvature_bound_source_path",
    "metric_response_source_path",
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


def flat_proof_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "proof_id": "FRI832_0_domain",
            "claim": "For flat local dimension n>1, the divergence map from symmetric trace-free tensors to vectors is surjective on nonzero/compatible modes.",
            "derivation": "For Fourier k != 0, choose A_ij=(k_iG_j+k_jG_i)/k^2-((n-2)/(n-1))(k.G)k_ik_j/k^4-(1/(n-1))(k.G)delta_ij/k^2; then A_i^i=0 and k_iA_ij=G_j.",
            "result": "flat_symbol_surjective_except_zero_mode",
            "remaining_obstruction": "zero mode and boundary compatibility",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "FRI832_1_gradient_right_inverse",
            "claim": "For gradient source G_j=partial_j Gamma, an explicit trace-free tensor cancels q in flat bulk.",
            "derivation": "Let Delta u=Gamma and K_ij=(n/(n-1)) partial_i partial_j u -(1/(n-1)) delta_ij Gamma.",
            "result": "explicit_Khat_solution_defined",
            "remaining_obstruction": "Delta inverse requires boundary/zero-mode choice",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "FRI832_2_tracefree_check",
            "claim": "K_ij is trace-free.",
            "derivation": "delta^ij K_ij=(n/(n-1)) Delta u-(n/(n-1)) Gamma=0 because Delta u=Gamma.",
            "result": "tracefree_exact",
            "remaining_obstruction": "none in flat bulk after Delta inverse is valid",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "FRI832_3_divergence_check",
            "claim": "The divergence of K_ij equals partial_j Gamma.",
            "derivation": "partial^i K_ij=(n/(n-1))partial_j Delta u-(1/(n-1))partial_j Gamma=partial_j Gamma.",
            "result": "divergence_matches_gradient_exact",
            "remaining_obstruction": "boundary flux can still spoil global/local-domain use",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "FRI832_4_flat_q_zero",
            "claim": "Flat bulk q_j=partial_j Gamma-partial^iK_ij is exactly zero for the constructed K.",
            "derivation": "Substitute FRI832_3 into q_j definition.",
            "result": "flat_bulk_q_loc_zero_for_gradient_source",
            "remaining_obstruction": "not a parent-action proof and not a metric-response/PPN proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def curved_bound_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "CB832_0_covariant_carrier",
            "statement": "Use the same Hessian carrier on a curved local domain: K_ij=(n/(n-1)) nabla_i nabla_j u -(1/(n-1)) g_ij Gamma with Delta u=Gamma.",
            "formula": "tr_g K=0",
            "status": "covariant_candidate",
            "claim_impact": "trace-free survives curvature",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "CB832_1_curvature_residual",
            "statement": "Curvature prevents exact flat divergence cancellation unless Ricci gradient term is small or canceled.",
            "formula": "nabla^i K_ij = nabla_j Gamma + (n/(n-1)) Ric_j^k nabla_k u, so q_j=-(n/(n-1)) Ric_j^k nabla_k u",
            "status": "derived_curvature_obstruction",
            "claim_impact": "local GR needs Ricci/curvature correction theorem or bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "CB832_2_norm_bound",
            "statement": "A first bound follows from the Ricci norm and inverse-Laplacian gradient norm.",
            "formula": "||q_curv|| <= (n/(n-1)) ||Ric|| ||nabla Delta^-1 Gamma||",
            "status": "derived_bound_formula",
            "claim_impact": "calculator-ready once Ricci and Gamma source profiles are sourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "CB832_3_boundary_residual",
            "statement": "The inverse Laplacian and integration by parts introduce boundary/zero-mode conditions.",
            "formula": "q_total <= q_curv + q_boundary + q_regularizer",
            "status": "open_boundary_input",
            "claim_impact": "boundary/source-measure terms remain live until sourced or theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "CB832_4_amplitude_warning",
            "statement": "The constructed K is generally of order Gamma, so q cancellation can still leave a metric-source carrier.",
            "formula": "||K|| <= C_H ||Gamma|| plus boundary/curvature corrections",
            "status": "amplitude_bound_required",
            "claim_impact": "PPN/Newton/clock/orbital response must be bounded before local GR is claimed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def physical_gap_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gap_id": "PG832_0_parent_action",
            "gap": "The flat right inverse is mathematical, not yet a term derived from the MTS parent action.",
            "needed_to_close": "derive S_bal or equivalent Khat balance equation from parent variables",
            "status": "open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gap_id": "PG832_1_boundary_choice",
            "gap": "Delta^-1 Gamma requires a zero-mode and boundary condition choice.",
            "needed_to_close": "prove compact local vacuum boundary/no-flux conditions or source a boundary bound",
            "status": "open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gap_id": "PG832_2_curvature_correction",
            "gap": "Curved domains produce q_curv=-(n/(n-1)) Ric(nabla Delta^-1 Gamma).",
            "needed_to_close": "bound Ricci and inverse-Laplacian source profile or add a covariant correction term",
            "status": "open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gap_id": "PG832_3_metric_response",
            "gap": "Khat carrier can gravitate even when div Khat cancels grad Gamma.",
            "needed_to_close": "derive metric response and show PPN/R10/clock/orbital/WEP residuals are below sourced limits",
            "status": "open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def runner_input_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "template_missing_curved_bound_inputs",
            "row_status": "blocked_missing_parent_and_arena_inputs",
            "Ricci_norm": "MISSING_CURVATURE_INPUT",
            "grad_laplace_inverse_Gamma_norm": "MISSING_GAMMA_PROFILE",
            "boundary_flux_norm": "MISSING_BOUNDARY_INPUT",
            "regularizer_residual_norm": "MISSING_PARENT_INPUT",
            "Khat_amplitude_norm": "MISSING_AMPLITUDE_INPUT",
            "metric_response_norm": "MISSING_ARENA_PROJECTION",
            "observable_limit": "MISSING_ARENA_BOUND",
            "Gamma_source_path": "MISSING_SOURCE_PATH",
            "boundary_condition_source_path": "MISSING_SOURCE_PATH",
            "curvature_bound_source_path": "MISSING_SOURCE_PATH",
            "metric_response_source_path": "MISSING_SOURCE_PATH",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "notes": "a claim row needs sourced Gamma profile, curvature/boundary data, parent regularizer, and observable response",
            "generated_utc": generated_utc,
        }
    ]


def is_missing(value: object) -> bool:
    text = str(value).strip()
    if text == "":
        return True
    upper = text.upper()
    return "MISSING" in upper or upper in {"UNSOURCED", "NONE", "N/A"}


def as_float(value: object) -> float | None:
    if is_missing(value):
        return None
    try:
        parsed = float(str(value))
    except ValueError:
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def run_bound_row(row: dict[str, object], generated_utc: str) -> dict[str, object]:
    missing_numeric = [field for field in REQUIRED_NUMERIC_FIELDS if as_float(row.get(field)) is None]
    missing_sources = [field for field in REQUIRED_SOURCE_FIELDS if is_missing(row.get(field))]
    missing = missing_numeric + missing_sources
    valid_for_claim = str(row.get("valid_for_claim")).lower() == "true"

    if missing:
        return {
            "row_id": row["row_id"],
            "runner_status": "blocked_missing_inputs",
            "q_curv_bound": "MISSING_INPUT",
            "q_total_bound": "MISSING_INPUT",
            "carrier_metric_bound": "MISSING_INPUT",
            "observable_pass": "false",
            "block_reason": "missing_fields:" + ";".join(missing),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }

    values = {field: as_float(row[field]) for field in REQUIRED_NUMERIC_FIELDS}
    assert all(value is not None for value in values.values())
    n = 4.0
    q_curv = (n / (n - 1.0)) * values["Ricci_norm"] * values["grad_laplace_inverse_Gamma_norm"]
    q_total = q_curv + values["boundary_flux_norm"] + values["regularizer_residual_norm"]
    carrier_metric = values["metric_response_norm"] * (q_total + values["Khat_amplitude_norm"])
    passes = valid_for_claim and carrier_metric <= values["observable_limit"]
    block_reason = "none" if passes else ("row_valid_for_claim_false" if not valid_for_claim else "observable_bound_exceeds_or_unvalidated")
    return {
        "row_id": row["row_id"],
        "runner_status": "computed_nonclaim" if not valid_for_claim else "computed",
        "q_curv_bound": f"{q_curv:.16e}",
        "q_total_bound": f"{q_total:.16e}",
        "carrier_metric_bound": f"{carrier_metric:.16e}",
        "observable_pass": str(passes).lower(),
        "block_reason": block_reason,
        "valid_for_claim": "false",
        "generated_utc": generated_utc,
    }


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D832_0",
            "finding": "flat bulk trace-free Khat right inverse is derived",
            "reason": "K_ij=(n/(n-1))partial_i partial_j Delta^-1 Gamma-(1/(n-1))delta_ij Gamma is trace-free and has divergence grad Gamma",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D832_1",
            "finding": "curved/local physical branch remains nonclaim",
            "reason": "curvature, boundary, parent-action origin, carrier amplitude, and observable response remain open",
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
            "objective": "use the explicit Hessian Khat carrier to bound its amplitude and metric response, or reject it as locally unsafe",
            "include": "Khat norm estimate, Newton fraction, PPN vector schema, curvature/boundary terms, parent-action adoption gate",
            "exclude": "local-GR claim, unsourced PPN/R10 pass, GitHub action, changing formalization-workbench",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "proved the flat trace-free Hessian Khat carrier cancels gradient q in bulk and derived curved Ricci obstruction",
            "what_is_not_claimed": "parent-derived Khat owner, boundary silence, local GR, PPN, R10, clocks, orbital, WEP, or metric safety",
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
    flat_rows: list[dict[str, object]],
    curved_rows: list[dict[str, object]],
    gap_rows: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    runner_outputs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_831_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    flat_ok = any(row["result"] == "tracefree_exact" for row in flat_rows) and any(
        row["result"] == "divergence_matches_gradient_exact" for row in flat_rows
    ) and any(row["result"] == "flat_bulk_q_loc_zero_for_gradient_source" for row in flat_rows)
    curved_ok = any(row["status"] == "derived_curvature_obstruction" for row in curved_rows) and any(
        row["status"] == "derived_bound_formula" for row in curved_rows
    )
    gaps_open = {"PG832_0_parent_action", "PG832_1_boundary_choice", "PG832_2_curvature_correction", "PG832_3_metric_response"}.issubset(
        {row["gap_id"] for row in gap_rows if row["status"] == "open"}
    )
    runner_blocks = any(row["row_id"] == "template_missing_curved_bound_inputs" and row["observable_pass"] == "false" for row in runner_outputs)
    no_missing_passes = not any(row["observable_pass"] == "true" and "missing_fields" in row["block_reason"] for row in runner_outputs)
    no_claim = (
        not any(row["observable_pass"] == "true" for row in runner_outputs)
        and not any(row["claim_allowed"] == "true" for row in decisions)
    )
    nonclaim_ok = all_valid_for_claim_false(
        [source_rows, flat_rows, curved_rows, gap_rows, runner_inputs, runner_outputs, decisions, next_targets, nonclaim]
    )
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V832_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V832_1_prior_831_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V832_2_flat_right_inverse_proved",
            "result": "pass" if flat_ok else "fail",
            "detail": "trace-free exact, divergence exact, and flat q zero rows present",
        },
        {
            "check_id": "V832_3_curved_obstruction_bound_recorded",
            "result": "pass" if curved_ok else "fail",
            "detail": "Ricci obstruction and norm bound recorded",
        },
        {
            "check_id": "V832_4_physical_gaps_open",
            "result": "pass" if gaps_open else "fail",
            "detail": "parent action, boundary, curvature, and metric response gaps remain explicit",
        },
        {
            "check_id": "V832_5_runner_template_blocks_missing",
            "result": "pass" if runner_blocks else "fail",
            "detail": "template_missing_curved_bound_inputs is blocked before numeric use",
        },
        {
            "check_id": "V832_6_no_missing_input_passes",
            "result": "pass" if no_missing_passes else "fail",
            "detail": "no row with missing fields passes",
        },
        {
            "check_id": "V832_7_no_data_or_local_GR_claim",
            "result": "pass" if no_claim else "fail",
            "detail": "no data, local-GR, PPN, R10, clock, orbital, or WEP pass selected",
        },
        {
            "check_id": "V832_8_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V832_9_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V832_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V832_11_validation_rows_ready",
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
    flat_rows: list[dict[str, object]],
    curved_rows: list[dict[str, object]],
    gap_rows: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    runner_outputs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 832 - Y5 R10 Trace-Free Divergence Range Theorem Or Cokernel Bound",
        "",
        "Current result: **the flat bulk trace-free `K_hat` carrier exists explicitly for gradient sources**. In flat dimension `n>1`, if `Delta u=Gamma_eff`, then `K_ij=(n/(n-1)) partial_i partial_j u-(1/(n-1)) delta_ij Gamma_eff` is trace-free and satisfies `partial^i K_ij=partial_j Gamma_eff`, so the bulk `q_j` channel cancels exactly. This is not yet local GR: curvature adds a Ricci obstruction, boundary data are still live, and the carrier amplitude/metric response still needs a PPN-style bound.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Flat Right-Inverse Proof",
        "",
        csv_table(flat_rows, ["proof_id", "claim", "derivation", "result", "remaining_obstruction", "valid_for_claim"]),
        "",
        "## Curved Obstruction Bound",
        "",
        csv_table(curved_rows, ["bound_id", "statement", "formula", "status", "claim_impact", "valid_for_claim"]),
        "",
        "## Physical Gap Ledger",
        "",
        csv_table(gap_rows, ["gap_id", "gap", "needed_to_close", "status", "valid_for_claim"]),
        "",
        "## Bound Runner Input Template",
        "",
        csv_table(runner_inputs, ["row_id", "row_status", "Ricci_norm", "grad_laplace_inverse_Gamma_norm", "boundary_flux_norm", "metric_response_norm", "numeric_ready", "valid_for_claim", "notes"]),
        "",
        "## Bound Runner Output",
        "",
        csv_table(runner_outputs, ["row_id", "runner_status", "q_curv_bound", "q_total_bound", "carrier_metric_bound", "observable_pass", "block_reason", "valid_for_claim"]),
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
    flat_rows = flat_proof_rows(generated_utc)
    curved_rows = curved_bound_rows(generated_utc)
    gap_rows = physical_gap_rows(generated_utc)
    runner_inputs = runner_input_rows(generated_utc)
    runner_outputs = [run_bound_row(row, generated_utc) for row in runner_inputs]
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, flat_rows, curved_rows, gap_rows, runner_inputs, runner_outputs, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(FLAT_PROOF_PATH, flat_rows, ["proof_id", "claim", "derivation", "result", "remaining_obstruction", "valid_for_claim", "generated_utc"])
    write_csv(CURVED_BOUND_PATH, curved_rows, ["bound_id", "statement", "formula", "status", "claim_impact", "valid_for_claim", "generated_utc"])
    write_csv(PHYSICAL_GAP_PATH, gap_rows, ["gap_id", "gap", "needed_to_close", "status", "valid_for_claim", "generated_utc"])
    write_csv(
        RUNNER_INPUT_PATH,
        runner_inputs,
        [
            "row_id",
            "row_status",
            "Ricci_norm",
            "grad_laplace_inverse_Gamma_norm",
            "boundary_flux_norm",
            "regularizer_residual_norm",
            "Khat_amplitude_norm",
            "metric_response_norm",
            "observable_limit",
            "Gamma_source_path",
            "boundary_condition_source_path",
            "curvature_bound_source_path",
            "metric_response_source_path",
            "numeric_ready",
            "valid_for_claim",
            "notes",
            "generated_utc",
        ],
    )
    write_csv(
        RUNNER_OUTPUT_PATH,
        runner_outputs,
        ["row_id", "runner_status", "q_curv_bound", "q_total_bound", "carrier_metric_bound", "observable_pass", "block_reason", "valid_for_claim", "generated_utc"],
    )
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, flat_rows, curved_rows, gap_rows, runner_inputs, runner_outputs, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
