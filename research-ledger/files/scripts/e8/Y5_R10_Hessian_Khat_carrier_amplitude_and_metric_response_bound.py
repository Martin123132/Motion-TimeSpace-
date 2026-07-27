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

OUTPUT_DOC = POST_CHECKPOINT / "833-Y5-R10-Hessian-Khat-carrier-amplitude-and-metric-response-bound.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_833_SOURCE_REGISTER.csv"
AMPLITUDE_LAW_PATH = RESIDUALS / "P8_Y5_R10_833_HESSIAN_KHAT_AMPLITUDE_LAW.csv"
METRIC_GATE_PATH = RESIDUALS / "P8_Y5_R10_833_METRIC_RESPONSE_GATE.csv"
RUNNER_INPUT_PATH = RESIDUALS / "P8_Y5_R10_833_AMPLITUDE_RUNNER_INPUT_TEMPLATE.csv"
RUNNER_OUTPUT_PATH = RESIDUALS / "P8_Y5_R10_833_AMPLITUDE_RUNNER_OUTPUT.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_833_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_833_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_833_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_833_VALIDATION.csv"

STATUS = "Y5_R10_833_Hessian_Khat_carrier_amplitude_order_Gamma_metric_response_open_nonclaim"
CLAIM_CEILING = "Khat_carrier_amplitude_law_only_no_metric_safety_no_local_GR_pass"
NEXT_TARGET = "834-Y5-R10-metric-null-Khat-carrier-or-Gamma-local-suppression-law.md"

SOURCE_SPECS = [
    {
        "source_id": "832_doc",
        "path": POST_CHECKPOINT / "832-Y5-R10-tracefree-divergence-range-theorem-or-cokernel-bound.md",
        "needles": [
            "flat bulk trace-free `K_hat` carrier exists explicitly",
            "CB832_4_amplitude_warning",
            "833-Y5-R10-Hessian-Khat-carrier-amplitude-and-metric-response-bound.md",
        ],
        "role": "immediate Hessian Khat amplitude handoff",
    },
    {
        "source_id": "832_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_832_VALIDATION.csv",
        "needles": [
            "V832_2_flat_right_inverse_proved,pass",
            "V832_3_curved_obstruction_bound_recorded,pass",
            "V832_10_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "795_amplitude_warning",
        "path": POST_CHECKPOINT / "795-Y5-R10-parent-origin-of-tracefree-Khat-solver-or-amplitude-bound.md",
        "needles": [
            "KAB795_1_Newton_fraction",
            "KAB795_2_PPN_vector",
            "The solver is not dead, but it has changed job title",
        ],
        "role": "older Khat carrier amplitude/PPN warning",
    },
    {
        "source_id": "830_observable_gate",
        "path": POST_CHECKPOINT / "830-Y5-R10-Khat-boundary-owner-or-residual-vector-runner.md",
        "needles": [
            "OG830_1_PPN",
            "OG830_2_R10",
            "OG830_5_WEP",
        ],
        "role": "observable response gate",
    },
    {
        "source_id": "equation_register_local_ppn",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "Kbar_tr,loc,00",
            "delta_phi_fraction",
            "The real Solar branch remains open until `q_loc(x)`, boundary data, and amplitude bounds are supplied.",
        ],
        "role": "local PPN variables and amplitude warning",
    },
]

REQUIRED_NUMERIC_FIELDS = [
    "dimension_n",
    "Gamma_norm",
    "K00_projection_fraction",
    "matter_curvature_norm",
    "metric_response_coeff",
    "observable_limit",
]
REQUIRED_SOURCE_FIELDS = [
    "Gamma_source_path",
    "Khat_projection_source_path",
    "metric_response_source_path",
    "local_bound_source_path",
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


def amplitude_law_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "law_id": "AL833_0_flat_carrier_symbol",
            "statement": "For the flat Hessian carrier, K_ij(k)=((n P_ij(k)-delta_ij)/(n-1)) Gamma(k), where P_ij=k_i k_j/k^2.",
            "derivation": "Fourier transform K_ij=(n/(n-1))partial_i partial_j Delta^-1 Gamma-(1/(n-1))delta_ij Gamma.",
            "result": "carrier_symbol_defined",
            "physical_impact": "Khat is not an independent tiny correction unless Gamma is tiny or metric-null",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "AL833_1_exact_L2_norm",
            "statement": "The flat Frobenius/L2 norm of the carrier is exactly order Gamma.",
            "derivation": "||nP-I||_F^2=n^2 tr(P^2)-2n tr(P)+tr(I)=n^2-2n+n=n(n-1), so ||K||^2=(n/(n-1))||Gamma||^2.",
            "result": "||K||_L2=sqrt(n/(n-1))*||Gamma||_L2",
            "physical_impact": "q cancellation does not itself suppress the metric source carried by Khat",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "AL833_2_dimension_examples",
            "statement": "The carrier-amplitude factor is close to one in relevant dimensions.",
            "derivation": "sqrt(3/2)=1.224744871 for spatial n=3; sqrt(4/3)=1.154700538 for spacetime-like n=4.",
            "result": "no_parametric_amplitude_suppression",
            "physical_impact": "local safety must come from metric-nullity, local Gamma suppression, or response bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "AL833_3_Newton_fraction_gate",
            "statement": "If Khat enters the local metric source, its Newton/PPN fraction must be bounded.",
            "derivation": "epsilon_K ~= metric_response_coeff * |Kbar_00| / |4 pi G rho/c^2|, with |Kbar_00| <= f_00 sqrt(n/(n-1)) ||Gamma||.",
            "result": "epsilon_K_bound_formula",
            "physical_impact": "source-backed Gamma_loc, f_00, matter curvature, and response coefficient are required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def metric_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "MG833_0_metric_null_route",
            "route": "metric-null carrier",
            "pass_condition": "parent action proves delta S_Khat/delta g_obs=0 or exact improvement/boundary-only stress in local matter frame",
            "current_status": "not_derived",
            "failure_effect": "Khat carrier can gravitate despite q cancellation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MG833_1_local_Gamma_suppression_route",
            "route": "local Gamma suppression",
            "pass_condition": "Gamma_loc is source-supported/locally suppressed enough that sqrt(n/(n-1)) Gamma_loc is below Newton/PPN limits",
            "current_status": "not_sourced",
            "failure_effect": "carrier amplitude is generically order Gamma",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MG833_2_response_matrix_route",
            "route": "observable response bound",
            "pass_condition": "PPN/R10/clock/orbital/WEP response matrix maps Khat carrier below all local bounds",
            "current_status": "missing_response_matrix",
            "failure_effect": "no local-GR or local-test pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MG833_3_parent_action_route",
            "route": "parent owner",
            "pass_condition": "S_bal or equivalent Khat equation is derived from MTS parent action and shares the same matter-frame readout",
            "current_status": "not_derived",
            "failure_effect": "Hessian carrier remains a mathematical repair, not a derived mechanism",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def runner_input_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "template_missing_amplitude_inputs",
            "row_status": "blocked_missing_parent_and_response_inputs",
            "dimension_n": "MISSING_DIMENSION_CHOICE",
            "Gamma_norm": "MISSING_GAMMA_PROFILE",
            "K00_projection_fraction": "MISSING_KHAT_COMPONENT_MAP",
            "matter_curvature_norm": "MISSING_LOCAL_MATTER_CURVATURE",
            "metric_response_coeff": "MISSING_ARENA_PROJECTION",
            "observable_limit": "MISSING_ARENA_BOUND",
            "Gamma_source_path": "MISSING_SOURCE_PATH",
            "Khat_projection_source_path": "MISSING_SOURCE_PATH",
            "metric_response_source_path": "MISSING_SOURCE_PATH",
            "local_bound_source_path": "MISSING_SOURCE_PATH",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "notes": "a claim row needs sourced Gamma_loc, K00 projection, local matter curvature, metric response, and arena limit",
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


def run_amplitude_row(row: dict[str, object], generated_utc: str) -> dict[str, object]:
    missing_numeric = [field for field in REQUIRED_NUMERIC_FIELDS if as_float(row.get(field)) is None]
    missing_sources = [field for field in REQUIRED_SOURCE_FIELDS if is_missing(row.get(field))]
    missing = missing_numeric + missing_sources
    valid_for_claim = str(row.get("valid_for_claim")).lower() == "true"

    if missing:
        return {
            "row_id": row["row_id"],
            "runner_status": "blocked_missing_inputs",
            "carrier_factor": "MISSING_INPUT",
            "Khat_norm_bound": "MISSING_INPUT",
            "K00_bound": "MISSING_INPUT",
            "newton_ppn_fraction_bound": "MISSING_INPUT",
            "observable_pass": "false",
            "block_reason": "missing_fields:" + ";".join(missing),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }

    values = {field: as_float(row[field]) for field in REQUIRED_NUMERIC_FIELDS}
    assert all(value is not None for value in values.values())
    n = values["dimension_n"]
    if n <= 1:
        carrier_factor = math.inf
    else:
        carrier_factor = math.sqrt(n / (n - 1.0))
    khat_norm = carrier_factor * values["Gamma_norm"]
    k00_bound = abs(values["K00_projection_fraction"]) * khat_norm
    newton_ppn_fraction = abs(values["metric_response_coeff"]) * k00_bound / abs(values["matter_curvature_norm"])
    passes = valid_for_claim and newton_ppn_fraction <= values["observable_limit"]
    block_reason = "none" if passes else ("row_valid_for_claim_false" if not valid_for_claim else "observable_bound_exceeds_or_unvalidated")
    return {
        "row_id": row["row_id"],
        "runner_status": "computed_nonclaim" if not valid_for_claim else "computed",
        "carrier_factor": f"{carrier_factor:.16e}",
        "Khat_norm_bound": f"{khat_norm:.16e}",
        "K00_bound": f"{k00_bound:.16e}",
        "newton_ppn_fraction_bound": f"{newton_ppn_fraction:.16e}",
        "observable_pass": str(passes).lower(),
        "block_reason": block_reason,
        "valid_for_claim": "false",
        "generated_utc": generated_utc,
    }


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D833_0",
            "finding": "Hessian Khat carrier is not parametrically small",
            "reason": "flat amplitude law gives ||K||=sqrt(n/(n-1))||Gamma||",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D833_1",
            "finding": "local branch needs metric-nullity, Gamma suppression, or response bound",
            "reason": "q cancellation alone can leave an order-Gamma carrier in the metric source",
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
            "objective": "derive either metric-null Khat carrier ownership or a local Gamma suppression law strong enough to satisfy local tests",
            "include": "metric-null variation, local Gamma profile, source-support scaling, matter-frame readout, PPN/R10/clock/orbital/WEP gates",
            "exclude": "claiming q cancellation as local GR, placeholder response rows, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "derived the exact flat Hessian Khat carrier amplitude law and installed metric-response safety gates",
            "what_is_not_claimed": "metric-null carrier, local Gamma suppression, local GR, PPN, R10, clocks, orbital, WEP, or parent action adoption",
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
    amplitude_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    runner_outputs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_832_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    amplitude_ok = any(row["result"] == "||K||_L2=sqrt(n/(n-1))*||Gamma||_L2" for row in amplitude_rows) and any(
        row["result"] == "no_parametric_amplitude_suppression" for row in amplitude_rows
    )
    gates_ok = {"MG833_0_metric_null_route", "MG833_1_local_Gamma_suppression_route", "MG833_2_response_matrix_route", "MG833_3_parent_action_route"}.issubset(
        {row["gate_id"] for row in gate_rows}
    )
    runner_blocks = any(row["row_id"] == "template_missing_amplitude_inputs" and row["observable_pass"] == "false" for row in runner_outputs)
    no_missing_passes = not any(row["observable_pass"] == "true" and "missing_fields" in row["block_reason"] for row in runner_outputs)
    no_claim = (
        not any(row["observable_pass"] == "true" for row in runner_outputs)
        and not any(row["claim_allowed"] == "true" for row in decisions)
    )
    nonclaim_ok = all_valid_for_claim_false(
        [source_rows, amplitude_rows, gate_rows, runner_inputs, runner_outputs, decisions, next_targets, nonclaim]
    )
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V833_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V833_1_prior_832_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V833_2_amplitude_law_derived",
            "result": "pass" if amplitude_ok else "fail",
            "detail": "exact sqrt(n/(n-1)) amplitude law and no-suppression warning present",
        },
        {
            "check_id": "V833_3_metric_safety_gates_complete",
            "result": "pass" if gates_ok else "fail",
            "detail": "metric-null, local-Gamma, response-matrix, and parent-action routes listed",
        },
        {
            "check_id": "V833_4_runner_template_blocks_missing",
            "result": "pass" if runner_blocks else "fail",
            "detail": "template_missing_amplitude_inputs is blocked before numeric use",
        },
        {
            "check_id": "V833_5_no_missing_input_passes",
            "result": "pass" if no_missing_passes else "fail",
            "detail": "no row with missing fields passes",
        },
        {
            "check_id": "V833_6_no_data_or_local_GR_claim",
            "result": "pass" if no_claim else "fail",
            "detail": "no data, local-GR, PPN, R10, clock, orbital, or WEP pass selected",
        },
        {
            "check_id": "V833_7_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V833_8_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V833_9_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V833_10_validation_rows_ready",
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
    amplitude_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    runner_outputs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 833 - Y5 R10 Hessian Khat Carrier Amplitude And Metric Response Bound",
        "",
        "Current result: **the explicit Hessian `K_hat` carrier that cancels flat-bulk `q` is generically order `Gamma_eff`, not parametrically small**. In flat Fourier/L2 form, `K_ij=((nP_ij-I_ij)/(n-1)) Gamma_eff`, so `||K||=sqrt(n/(n-1)) ||Gamma_eff||`. Therefore q-cancellation is mathematically real but physically insufficient unless the carrier is metric-null, `Gamma_eff` is locally suppressed, or the metric-response vector is bounded below local-test limits.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Hessian Carrier Amplitude Law",
        "",
        csv_table(amplitude_rows, ["law_id", "statement", "derivation", "result", "physical_impact", "valid_for_claim"]),
        "",
        "## Metric Response Gate",
        "",
        csv_table(gate_rows, ["gate_id", "route", "pass_condition", "current_status", "failure_effect", "valid_for_claim"]),
        "",
        "## Amplitude Runner Input Template",
        "",
        csv_table(runner_inputs, ["row_id", "row_status", "dimension_n", "Gamma_norm", "K00_projection_fraction", "matter_curvature_norm", "metric_response_coeff", "numeric_ready", "valid_for_claim", "notes"]),
        "",
        "## Amplitude Runner Output",
        "",
        csv_table(runner_outputs, ["row_id", "runner_status", "carrier_factor", "Khat_norm_bound", "K00_bound", "newton_ppn_fraction_bound", "observable_pass", "block_reason", "valid_for_claim"]),
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
    amplitude_rows = amplitude_law_rows(generated_utc)
    gate_rows = metric_gate_rows(generated_utc)
    runner_inputs = runner_input_rows(generated_utc)
    runner_outputs = [run_amplitude_row(row, generated_utc) for row in runner_inputs]
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, amplitude_rows, gate_rows, runner_inputs, runner_outputs, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(AMPLITUDE_LAW_PATH, amplitude_rows, ["law_id", "statement", "derivation", "result", "physical_impact", "valid_for_claim", "generated_utc"])
    write_csv(METRIC_GATE_PATH, gate_rows, ["gate_id", "route", "pass_condition", "current_status", "failure_effect", "valid_for_claim", "generated_utc"])
    write_csv(
        RUNNER_INPUT_PATH,
        runner_inputs,
        [
            "row_id",
            "row_status",
            "dimension_n",
            "Gamma_norm",
            "K00_projection_fraction",
            "matter_curvature_norm",
            "metric_response_coeff",
            "observable_limit",
            "Gamma_source_path",
            "Khat_projection_source_path",
            "metric_response_source_path",
            "local_bound_source_path",
            "numeric_ready",
            "valid_for_claim",
            "notes",
            "generated_utc",
        ],
    )
    write_csv(
        RUNNER_OUTPUT_PATH,
        runner_outputs,
        ["row_id", "runner_status", "carrier_factor", "Khat_norm_bound", "K00_bound", "newton_ppn_fraction_bound", "observable_pass", "block_reason", "valid_for_claim", "generated_utc"],
    )
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, amplitude_rows, gate_rows, runner_inputs, runner_outputs, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
