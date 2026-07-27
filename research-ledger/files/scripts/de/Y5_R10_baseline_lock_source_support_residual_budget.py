from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "829-Y5-R10-baseline-lock-source-support-residual-budget.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_829_SOURCE_REGISTER.csv"
RESIDUAL_BUDGET_PATH = RESIDUALS / "P8_Y5_R10_829_RESIDUAL_BUDGET_FORMULAS.csv"
SUPPORT_INPUT_PATH = RESIDUALS / "P8_Y5_R10_829_SUPPORT_INPUT_LEDGER.csv"
OBSERVABLE_VECTOR_PATH = RESIDUALS / "P8_Y5_R10_829_OBSERVABLE_RESIDUAL_VECTOR.csv"
PROMOTION_GATE_PATH = RESIDUALS / "P8_Y5_R10_829_PROMOTION_GATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_829_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_829_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_829_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_829_VALIDATION.csv"

STATUS = "Y5_R10_829_baseline_lock_residual_budget_defined_inputs_unsourced_nonclaim"
CLAIM_CEILING = "symbolic_local_residual_budget_only_no_numeric_local_GR_pass"
NEXT_TARGET = "830-Y5-R10-Khat-boundary-owner-or-residual-vector-runner.md"

SOURCE_SPECS = [
    {
        "source_id": "828_doc",
        "path": POST_CHECKPOINT / "828-Y5-R10-XB-Lcg-local-constancy-or-Khat-owner-theorem.md",
        "needles": [
            "BL828_3_post_lock_q",
            "QB828_1_support_power_bound",
            "829-Y5-R10-baseline-lock-source-support-residual-budget.md",
        ],
        "role": "immediate baseline-lock residual budget handoff",
    },
    {
        "source_id": "828_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_828_VALIDATION.csv",
        "needles": [
            "V828_3_baseline_lock_condition,pass",
            "V828_7_promotion_still_blocked,pass",
            "V828_12_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "799_transition_calculator",
        "path": POST_CHECKPOINT / "799-Y5-R10-transition-current-bound-calculator-and-source-support-powers.md",
        "needles": [
            "TBF799_1_q_gamma_quad",
            "TBF799_4_epsilon_q",
            "TCP799_1_compare_all_local_arenas",
        ],
        "role": "older transition-current calculator formulas and all-arena gate",
    },
    {
        "source_id": "800_support_powers",
        "path": POST_CHECKPOINT / "800-Y5-R10-universal-XB-PiB-support-powers-or-Kperp-boundary-zero-lemma.md",
        "needles": [
            "SPD800_0_pS_source",
            "SPD800_5_verdict",
            "KBL800_3_failure",
        ],
        "role": "support-power and Kperp obstruction source",
    },
    {
        "source_id": "equation_register_local_ppn",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "local_ppn_branch_framework_defined",
            "q_loc^nu nonzero -> K_tr,loc^{mu nu} required -> metric solution required -> PPN observables required.",
            "Source-support / boundary-amplitude law",
        ],
        "role": "local PPN vector and source-support obligations",
    },
    {
        "source_id": "equation_register_qbound",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "Local `q_loc` source-profile bound",
            "The real Solar branch remains open until `q_loc(x)`, boundary data, and amplitude bounds are supplied.",
            "Strong support can pass; weak source support",
        ],
        "role": "q_loc profile and residual-bound warning",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def check_needles(path: Path, needles: list[str]) -> str:
    if not path.exists():
        return "missing_path"
    text = path.read_text(encoding="utf-8", errors="replace")
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


def residual_budget_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "term_id": "RB829_0_exact_removed_linear_trace",
            "residual_term": "baseline trace drift",
            "formula": "q_baseline = 0 after parent-derived baseline lock Gamma_L=Lambda_loc",
            "dimension": "L^-3",
            "status": "exact_zero_conditional",
            "needed_source": "derive Gamma_L=Lambda_loc from parent local branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "term_id": "RB829_1_quadratic_memory",
            "residual_term": "quadratic memory source",
            "formula": "q_quad <= abs(a_F R_mm) U_B^(2 pS)/(L_cg^2 L_tr)",
            "dimension": "L^-3",
            "status": "conditional_scaling",
            "needed_source": "U_B profile, pS, a_F, R_mm, L_cg, L_tr",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "term_id": "RB829_2_second_order_XB",
            "residual_term": "second-order X_B drift",
            "formula": "q_X2 <= C_X U_B^(2 pS)/(L_cg^2 L_X)",
            "dimension": "L^-3",
            "status": "conditional_scaling",
            "needed_source": "C_X, L_X, U_B profile, pS, moving-extremum theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "term_id": "RB829_3_boundary_measure",
            "residual_term": "boundary/source-measure residue",
            "formula": "q_boundary <= A_B U_B^pB/(L_cg^2 L_tr)",
            "dimension": "L^-3",
            "status": "open",
            "needed_source": "pB, A_B, boundary silence theorem or local response bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "term_id": "RB829_4_Khat_divergence",
            "residual_term": "K_hat response",
            "formula": "q_K = -P_loc div K_hat, bounded by parent tensor operator and boundary data",
            "dimension": "L^-3",
            "status": "open",
            "needed_source": "K_hat owner, tensor boundary data, no-zero-mode or residual response bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "term_id": "RB829_5_total_source_scale",
            "residual_term": "total local exchange source",
            "formula": "q_total <= q_quad + q_X2 + q_boundary + q_K",
            "dimension": "L^-3",
            "status": "budget_formula_only",
            "needed_source": "all prior terms plus observable response matrices",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def support_input_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "input_id": "SI829_0_U_B",
            "symbol": "U_B",
            "role": "local screened small parameter",
            "current_status": "missing_source_backed_local_profile",
            "minimum_acceptance": "one universal X_B to Pi_B rule for lab, Solar, clock, orbital, and R10 environments",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "SI829_1_pS",
            "symbol": "pS",
            "role": "quadratic memory source support power",
            "current_status": "pS=1 conditional from U_B S_cg source factor",
            "minimum_acceptance": "prove bounded S_cg and no hidden unscreened source channel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "SI829_2_baseline_lock",
            "symbol": "Gamma_L=Lambda_loc",
            "role": "kills pT trace-baseline drift exactly",
            "current_status": "conditional_theorem_not_parent_derived",
            "minimum_acceptance": "derive from parent local vacuum branch rather than impose as closure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "SI829_3_lengths",
            "symbol": "L_cg, L_tr, L_X, L_sys",
            "role": "convert source scaling into local residual amplitudes",
            "current_status": "missing_source_backed_values",
            "minimum_acceptance": "local-system-specific but parent-derived or observationally sourced length rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "SI829_4_coefficients",
            "symbol": "a_F, R_mm, C_X, A_B",
            "role": "amplitude coefficients in q residual budget",
            "current_status": "missing_parent_values",
            "minimum_acceptance": "derive or bound before any residual-vector run is treated as evidence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "SI829_5_Khat",
            "symbol": "K_hat operator and boundary data",
            "role": "owns or bounds tensor divergence contribution",
            "current_status": "open",
            "minimum_acceptance": "parent tensor equation, boundary theorem, or explicit response-vector residual bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def observable_vector_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "observable_id": "OV829_0_exchange",
            "arena": "Bianchi/exchange",
            "residual_component": "epsilon_q = L_sys q_total / K_matter_00",
            "required_response": "K_matter_00 and local source profile",
            "claim_status": "missing_numeric_inputs",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "OV829_1_PPN",
            "arena": "PPN",
            "residual_component": "delta_gamma, delta_beta, alpha1, alpha2, xi from metric response to q_total and K_hat",
            "required_response": "solve or bound local metric/tensor response, not just Poisson source size",
            "claim_status": "missing_response_matrix",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "OV829_2_R10",
            "arena": "short-range R10",
            "residual_component": "alpha(lambda) induced by local memory/tensor exchange",
            "required_response": "map q_total and K_hat to Yukawa-like alpha(lambda) with sourced lambda",
            "claim_status": "missing_response_matrix",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "OV829_3_clocks",
            "arena": "clock/redshift",
            "residual_component": "clock_delta_z and possible Gdot/G proxy",
            "required_response": "matter-frame descent and time-dependent local baseline residual",
            "claim_status": "missing_matter_descent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "OV829_4_orbital",
            "arena": "orbital/ephemeris",
            "residual_component": "extra acceleration, precession, range residual",
            "required_response": "stationary weak-field metric solution and boundary conditions",
            "claim_status": "missing_response_matrix",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "OV829_5_WEP",
            "arena": "WEP/matter readout",
            "residual_component": "eta_AB or species-dependent coupling",
            "required_response": "species-independent matter action descent or direct bound",
            "claim_status": "missing_matter_descent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G829_0_linear_terms",
            "gate": "Are linear trace-gradient channels removed?",
            "result": "pass_conditional",
            "consequence": "F1 zero, moving-extremum cancellation, and baseline lock leave only quadratic/boundary/Khat terms",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G829_1_budget_schema",
            "gate": "Is the local residual budget formula explicit?",
            "result": "pass_symbolic",
            "consequence": "q_total formula is ready for sourced inputs, but not evidence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G829_2_numeric_sources",
            "gate": "Are U_B, support powers, lengths, amplitudes, and Khat owner sourced?",
            "result": "fail_missing_inputs",
            "consequence": "no numeric local pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G829_3_observable_response",
            "gate": "Is there a PPN/R10/clock/orbital/WEP residual vector with response matrices?",
            "result": "fail_missing_response",
            "consequence": "no local-GR/Newton claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D829_0",
            "decision": "residual budget is symbolically defined after baseline lock",
            "reason": "linear trace channels are conditionally removed, leaving q_quad, q_X2, q_boundary, and q_Khat",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D829_1",
            "decision": "do not run numeric local evidence yet",
            "reason": "inputs and response matrices are not source-backed; a numeric run now would be toy closure only",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "either derive the K_hat/boundary owner needed by the residual budget or build a nonclaim residual-vector runner that refuses to pass without sourced local inputs",
            "allowed_work": "Khat tensor equation attempt, boundary/no-zero-mode theorem, response-vector schema, missing-input runner",
            "forbidden_work": "local-GR claim, sourced-pass claim with placeholders, data fitting, C2A closure promotion",
            "priority": "high",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_survived": "symbolic q_loc residual budget after conditional removal of all linear trace channels",
            "what_failed": "source-backed numeric inputs and observable response matrices are still missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    support_rows: list[dict[str, object]],
    observable_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V829_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )
    clean_828, clean_828_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_828_VALIDATION.csv")
    add("V829_1_prior_828_clean", clean_828, clean_828_detail)
    add(
        "V829_2_residual_terms_complete",
        {"RB829_0_exact_removed_linear_trace", "RB829_1_quadratic_memory", "RB829_2_second_order_XB", "RB829_3_boundary_measure", "RB829_4_Khat_divergence", "RB829_5_total_source_scale"}.issubset({row["term_id"] for row in residual_rows}),
        "linear removed, quadratic, X2, boundary, Khat, and total terms present",
    )
    add(
        "V829_3_dimensions_are_Lminus3",
        all(row["dimension"] == "L^-3" for row in residual_rows),
        "all q residual terms have L^-3 dimension",
    )
    add(
        "V829_4_missing_inputs_explicit",
        {"SI829_0_U_B", "SI829_3_lengths", "SI829_4_coefficients", "SI829_5_Khat"}.issubset({row["input_id"] for row in support_rows}),
        "missing source-backed inputs listed",
    )
    add(
        "V829_5_observable_vector_complete",
        {"Bianchi/exchange", "PPN", "short-range R10", "clock/redshift", "orbital/ephemeris", "WEP/matter readout"}.issubset({row["arena"] for row in observable_rows}),
        "observable residual vector covers local arenas",
    )
    add(
        "V829_6_promotion_blocked",
        any(row["gate_id"] == "G829_2_numeric_sources" and row["result"] == "fail_missing_inputs" for row in gates)
        and any(row["gate_id"] == "G829_3_observable_response" and row["result"] == "fail_missing_response" for row in gates),
        "numeric and response gates block promotion",
    )
    add(
        "V829_7_decision_nonrunnable",
        all(row["runnable"] == "false" for row in decisions),
        "branch remains non-runnable",
    )
    add(
        "V829_8_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )
    all_rows = source_rows + residual_rows + support_rows + observable_rows + gates + decisions + next_rows + summary
    add(
        "V829_9_all_rows_nonclaim",
        all(row.get("valid_for_claim") == "false" for row in all_rows),
        "all generated rows valid_for_claim=false",
    )
    add(
        "V829_10_no_data_or_local_GR_claim",
        all("local-GR claim" in row["forbidden_work"] and "placeholders" in row["forbidden_work"] for row in next_rows),
        "no data or local-GR claim selected",
    )
    changed = formalization_workbench_modified_count()
    add(
        "V829_11_formalization_workbench_untouched",
        changed == 0,
        f"formalization_changed_after_cutoff={changed}",
    )
    add("V829_12_validation_rows_ready", True, "validation table constructed")
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def render_document(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    support_rows: list[dict[str, object]],
    observable_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 829 - Y5 R10 Baseline-Lock Source-Support Residual Budget",
            (
                "Current result: **the post-baseline-lock local branch now has an explicit symbolic residual budget**. "
                "The linear trace channels are conditionally gone; the remaining local source is `q_total <= q_quad + q_X2 + q_boundary + q_K`. "
                "This is calculator-ready structure, not evidence: the input rows and response matrices are still unsourced."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Nonclaim Summary\n\n" + markdown_table(summary, ["status", "claim_ceiling", "what_survived", "what_failed", "next_target", "valid_for_claim"]),
            "## Residual Budget Formulas\n\n" + markdown_table(residual_rows, ["term_id", "residual_term", "formula", "dimension", "status", "needed_source", "valid_for_claim"]),
            "## Support Input Ledger\n\n" + markdown_table(support_rows, ["input_id", "symbol", "role", "current_status", "minimum_acceptance", "valid_for_claim"]),
            "## Observable Residual Vector\n\n" + markdown_table(observable_rows, ["observable_id", "arena", "residual_component", "required_response", "claim_status", "valid_for_claim"]),
            "## Promotion Gate\n\n" + markdown_table(gates, ["gate_id", "gate", "result", "consequence", "valid_for_claim"]),
            "## Decision\n\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim"]),
            "## Next Target\n\n" + markdown_table(next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "valid_for_claim"]),
            "## Source Register\n\n" + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "This is useful because it turns the local-GR problem into a finite checklist instead of a fog bank. "
            "The branch is not promoted: a real pass needs sourced `U_B`, lengths, amplitudes, a `K_hat`/boundary owner, matter descent, and observable response matrices.",
        ]
    )


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")

    source_rows = source_register_rows(generated_utc)
    residual_rows = residual_budget_rows(generated_utc)
    support_rows = support_input_rows(generated_utc)
    observable_rows = observable_vector_rows(generated_utc)
    gates = promotion_gate_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, residual_rows, support_rows, observable_rows, gates, decisions, next_rows, summary)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUAL_BUDGET_PATH, residual_rows, ["term_id", "residual_term", "formula", "dimension", "status", "needed_source", "valid_for_claim", "generated_utc"])
    write_csv(SUPPORT_INPUT_PATH, support_rows, ["input_id", "symbol", "role", "current_status", "minimum_acceptance", "valid_for_claim", "generated_utc"])
    write_csv(OBSERVABLE_VECTOR_PATH, observable_rows, ["observable_id", "arena", "residual_component", "required_response", "claim_status", "valid_for_claim", "generated_utc"])
    write_csv(PROMOTION_GATE_PATH, gates, ["gate_id", "gate", "result", "consequence", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "priority", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_survived", "what_failed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(generated_utc, source_rows, residual_rows, support_rows, observable_rows, gates, decisions, next_rows, summary, validation),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"829 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
