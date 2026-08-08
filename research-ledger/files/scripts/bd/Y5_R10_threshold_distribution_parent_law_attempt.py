from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "814-Y5-R10-threshold-distribution-parent-law-attempt.md"
NEXT_TARGET = "815-Y5-R10-rational-threshold-exponent-source-proof-or-shape-demotion.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_814_SOURCE_REGISTER.csv"
THEOREM_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_814_THRESHOLD_THEOREM_ATTEMPT.csv"
NUMERIC_DIAGNOSTICS_PATH = RESIDUALS / "P8_Y5_R10_814_RATIONAL_DIAGNOSTICS.csv"
SHAPE_LOCK_VERDICT_PATH = RESIDUALS / "P8_Y5_R10_814_SHAPE_LOCK_VERDICT.csv"
CANDIDATE_SHAPE_PATH = RESIDUALS / "P8_Y5_R10_814_CANDIDATE_SHAPE_CONTRACT.csv"
NEXT_DECISION_PATH = RESIDUALS / "P8_Y5_R10_814_NEXT_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_814_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_814_VALIDATION.csv"

STATUS = "Y5_R10_814_threshold_distribution_conditional_theorem_rational_clue_not_parent_lock_nonclaim"
CLAIM_CEILING = "conditional_shape_theorem_only_no_C1_data_run_no_cosmology_support_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

NU_FIT = 1.7500073382761008
ALPHA_FIT = 1.0543379145228584
NU_RATIONAL = 7.0 / 4.0
F_EQ_TARGET = 3.0 / 5.0

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    THEOREM_ATTEMPT_PATH,
    NUMERIC_DIAGNOSTICS_PATH,
    SHAPE_LOCK_VERDICT_PATH,
    CANDIDATE_SHAPE_PATH,
    NEXT_DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "813_doc",
        "path": POST_CHECKPOINT / "813-Y5-R10-C1-parent-lock-source-hunt-or-demotion.md",
        "needles": [
            "C1 is not dead, but it is demoted out of the data ring",
            "threshold distribution derivation selected first",
            "814-Y5-R10-threshold-distribution-parent-law-attempt.md",
        ],
        "role": "immediate source-hunt selector",
    },
    {
        "source_id": "813_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_813_VALIDATION.csv",
        "needles": [
            "V813_5_C1_demoted_to_source_hunt,pass",
            "V813_6_threshold_path_selected_first,pass",
            "V813_8_next_target_selected,pass,814-Y5-R10-threshold-distribution-parent-law-attempt.md",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "formal_117_shape",
        "path": FORMALIZATION / "117-memory-shape-source-gate.md",
        "needles": [
            "dF/dN = h(N)[1 - F]",
            "F(N) = 1 - exp[-(N/u_s)^nu_act].",
            "The parent theory must explain that distribution.",
            "alpha_act is still fitted, not derived.",
        ],
        "role": "threshold/survival mechanism source",
    },
    {
        "source_id": "formal_118_status",
        "path": FORMALIZATION / "118-cosmology-memory-status-decision.md",
        "needles": [
            "alpha_act is not parent-derived;",
            "nu_act is not parent-derived;",
            "R2: derive the threshold distribution N_th from microscopic/coarse-grained MTS dynamics;",
        ],
        "role": "frozen cosmology-memory status",
    },
]


def utc_stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def needle_status(path: Path, needles: list[str]) -> str:
    if not path.exists():
        return "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
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


def inside_post_checkpoint(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def rational_diagnostics() -> dict[str, float]:
    f_eq_fit = 1.0 - math.exp(-((1.0 / ALPHA_FIT) ** NU_FIT))
    alpha_from_three_fifths = (1.0 / (-math.log(1.0 - F_EQ_TARGET))) ** (1.0 / NU_RATIONAL)
    f_eq_nu_rational_alpha_fit = 1.0 - math.exp(-((1.0 / ALPHA_FIT) ** NU_RATIONAL))
    f_eq_alpha_one = 1.0 - math.exp(-1.0)
    return {
        "nu_fit": NU_FIT,
        "nu_rational_7_4": NU_RATIONAL,
        "nu_abs_diff_from_7_4": abs(NU_FIT - NU_RATIONAL),
        "nu_rel_diff_from_7_4": abs(NU_FIT - NU_RATIONAL) / NU_RATIONAL,
        "alpha_fit": ALPHA_FIT,
        "F_eq_fit": f_eq_fit,
        "F_eq_diff_from_3_5": f_eq_fit - F_EQ_TARGET,
        "alpha_from_Feq_3_5_nu_7_4": alpha_from_three_fifths,
        "alpha_diff_from_3_5_7_4_candidate": ALPHA_FIT - alpha_from_three_fifths,
        "F_eq_nu_7_4_alpha_fit": f_eq_nu_rational_alpha_fit,
        "F_eq_alpha_1": f_eq_alpha_one,
    }


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


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_derived": "Weibull threshold law follows from a Poisson activation measure with power-law cumulative hazard.",
            "what_not_derived": "parent origin of nu=7/4, equality-clock normalization, F_eq=3/5, and exact alpha_act",
            "C1_status": "shape_lock_not_satisfied_data_run_blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def theorem_attempt_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "step": "T814_0_activation_survival_identity",
            "statement": "Let U(N)=1-F(N). If dF/dN=h(N)(1-F), then dU/dN=-h(N)U and U(N)=exp[-integral_0^N h(s)ds].",
            "status": "derived",
            "blocks_C1_data_run": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step": "T814_1_poisson_threshold_measure",
            "statement": "If activation thresholds form a Poisson process over expansion-load measure dmu=h(N)dN, then F(N)=P(N_th<N)=1-exp[-mu([0,N])].",
            "status": "derived",
            "blocks_C1_data_run": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step": "T814_2_weibull_condition",
            "statement": "If h(N)=(nu/u_s)(N/u_s)^(nu-1), then mu([0,N])=(N/u_s)^nu and F(N)=1-exp[-(N/u_s)^nu].",
            "status": "conditional_theorem",
            "blocks_C1_data_run": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step": "T814_3_parent_exponent_gap",
            "statement": "The parent action/corpus still does not derive why the activation measure density must scale as N^(nu-1), nor why nu equals 7/4.",
            "status": "not_derived",
            "blocks_C1_data_run": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step": "T814_4_parent_scale_gap",
            "statement": "The equality clock gives a natural scale u_eq, but the parent theory does not derive alpha_act or an exact F(u_eq) rule.",
            "status": "not_derived",
            "blocks_C1_data_run": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def numeric_diagnostic_rows(generated_utc: str) -> list[dict[str, object]]:
    diagnostics = rational_diagnostics()
    rows: list[dict[str, object]] = []
    for key, value in diagnostics.items():
        rows.append(
            {
                "diagnostic": key,
                "value": f"{value:.17g}",
                "interpretation": diagnostic_interpretation(key, value),
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def diagnostic_interpretation(key: str, value: float) -> str:
    if key == "nu_abs_diff_from_7_4":
        return "nu_fit is extremely close to 7/4; this is a derivation target, not proof"
    if key == "F_eq_diff_from_3_5":
        return "F at equality is close to 3/5; rational clue only"
    if key == "alpha_diff_from_3_5_7_4_candidate":
        return "alpha candidate from nu=7/4 and F_eq=3/5 is close but not exact"
    if key == "F_eq_alpha_1":
        return "alpha=1 would give 1-exp(-1), not the fitted equality activation"
    return "numeric diagnostic"


def shape_lock_verdict_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "shape_item": "Weibull functional form",
            "verdict": "conditionally_derived",
            "reason": "follows from Poisson activation measure with power-law cumulative hazard",
            "C1_consequence": "skeleton survives",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "shape_item": "nu_act exact value",
            "verdict": "rational_clue_not_parent_lock",
            "reason": "nu_fit is within 7.338276100776753e-06 of 7/4, but no corpus theorem derives 7/4",
            "C1_consequence": "blocks data run",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "shape_item": "alpha_act exact value",
            "verdict": "equality_scale_clue_not_parent_lock",
            "reason": "alpha is close to equality-clock normalization and F_eq is near 3/5, but no parent rule fixes either",
            "C1_consequence": "blocks data run",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "shape_item": "threshold distribution N_th",
            "verdict": "conditional_measure_only",
            "reason": "required density dmu=(nu/u_s^nu)N^(nu-1)dN is identified but not generated from parent dynamics",
            "C1_consequence": "C1 shape remains source-hunt only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def candidate_shape_rows(generated_utc: str) -> list[dict[str, object]]:
    diagnostics = rational_diagnostics()
    return [
        {
            "candidate_id": "C1_shape_7over4_3over5",
            "candidate_rule": "nu=7/4 and F(u_eq)=3/5, giving alpha=[1/ln(5/2)]^(4/7)",
            "alpha_candidate": f"{diagnostics['alpha_from_Feq_3_5_nu_7_4']:.17g}",
            "alpha_fit": f"{ALPHA_FIT:.17g}",
            "nu_candidate": f"{NU_RATIONAL:.17g}",
            "nu_fit": f"{NU_FIT:.17g}",
            "status": "interesting_rational_source_target_not_parent_derived",
            "allowed_use": "future theorem target or stress-only predeclared shape",
            "forbidden_use": "claim fitted shape is derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def next_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D814_0",
            "decision": "do not run C1 data branch",
            "reason": "functional form is conditionally derived but exact shape constants are not parent-locked",
            "next_target": NEXT_TARGET,
            "next_question": "Can nu=7/4 and/or F(u_eq)=3/5 be derived from parent source geometry rather than noticed after fitting?",
            "run_now": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_rows(*row_groups: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for group in row_groups:
        rows.extend(group)
    return rows


def validation_rows(
    source_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    diagnostic_rows: list[dict[str, object]],
    verdict_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V814_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )

    prior_clean, prior_detail = validation_file_clean(813)
    add("V814_1_prior_813_clean", prior_clean, prior_detail)

    add(
        "V814_2_outputs_scoped",
        all(inside_post_checkpoint(path) for path in OUTPUT_PATHS),
        str(POST_CHECKPOINT),
    )

    generated = all_generated_rows(source_rows, nonclaim_rows, theorem_rows, diagnostic_rows, verdict_rows, candidate_rows, next_rows)
    add(
        "V814_3_all_rows_nonclaim",
        all(str(row.get("valid_for_claim", "")).lower() == "false" for row in generated),
        "all generated rows valid_for_claim=false",
    )

    add(
        "V814_4_conditional_weibull_theorem_present",
        any(row["step"] == "T814_2_weibull_condition" and row["status"] == "conditional_theorem" for row in theorem_rows),
        "Weibull conditional theorem recorded",
    )

    add(
        "V814_5_exact_shape_not_parent_locked",
        any(row["shape_item"] == "nu_act exact value" and "not_parent_lock" in row["verdict"] for row in verdict_rows)
        and any(row["shape_item"] == "alpha_act exact value" and "not_parent_lock" in row["verdict"] for row in verdict_rows),
        "alpha_act and nu_act remain unpromoted",
    )

    add(
        "V814_6_rational_clue_recorded",
        any(row["candidate_id"] == "C1_shape_7over4_3over5" for row in candidate_rows),
        "7/4 and 3/5 candidate recorded as nonclaim target",
    )

    add(
        "V814_7_no_data_run_selected",
        all(row["run_now"] == "false" for row in next_rows),
        "no C1 data run selected",
    )

    add(
        "V814_8_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )

    formalization_changed = formalization_change_count()
    add(
        "V814_9_formalization_workbench_untouched",
        formalization_changed == 0,
        f"formalization_changed_after_cutoff={formalization_changed}",
    )

    add("V814_10_validation_rows_ready", True, "validation table constructed")
    return rows


def render_document(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    diagnostic_rows: list[dict[str, object]],
    verdict_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 814 - Y5 R10 Threshold Distribution Parent Law Attempt",
            (
                "Current result: **the Weibull threshold law can be derived conditionally, but the fitted shape constants are not yet parent-derived**. "
                "The useful surprise is that `nu_act` is essentially `7/4`, and the equality activation is close to `3/5`; "
                "that creates a sharper theorem target, not a claim."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Non-Claim Summary\n\n"
            + markdown_table(
                nonclaim_rows,
                ["status", "claim_ceiling", "what_derived", "what_not_derived", "C1_status", "next_target", "valid_for_claim"],
            ),
            "## Threshold Theorem Attempt\n\n"
            + markdown_table(theorem_rows, ["step", "statement", "status", "blocks_C1_data_run", "valid_for_claim"]),
            "## Rational Diagnostics\n\n"
            + markdown_table(diagnostic_rows, ["diagnostic", "value", "interpretation", "valid_for_claim"]),
            "## Shape Lock Verdict\n\n"
            + markdown_table(verdict_rows, ["shape_item", "verdict", "reason", "C1_consequence", "valid_for_claim"]),
            "## Candidate Shape Contract\n\n"
            + markdown_table(
                candidate_rows,
                ["candidate_id", "candidate_rule", "alpha_candidate", "alpha_fit", "nu_candidate", "nu_fit", "status", "allowed_use", "forbidden_use", "valid_for_claim"],
            ),
            "## Next Decision\n\n"
            + markdown_table(next_rows, ["decision_id", "decision", "reason", "next_target", "next_question", "run_now", "valid_for_claim"]),
            "## Source Register\n\n"
            + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "This is a partial derivation win and a promotion failure. The form `F=1-exp[-(N/u_s)^nu]` is not arbitrary if the parent supplies a power-law activation measure. "
            "But the parent has not supplied the exponent or equality normalization. The next move is therefore not data; it is a targeted proof attempt for `nu=7/4` and the `F(u_eq)≈3/5` equality rule.",
            "## Next Target\n\n`" + NEXT_TARGET + "`",
        ]
    ) + "\n"


def main() -> None:
    generated_utc = utc_stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(generated_utc)
    nonclaim_rows = nonclaim_summary_rows(generated_utc)
    theorem_rows = theorem_attempt_rows(generated_utc)
    diagnostic_rows = numeric_diagnostic_rows(generated_utc)
    verdict_rows = shape_lock_verdict_rows(generated_utc)
    candidate_rows = candidate_shape_rows(generated_utc)
    next_rows = next_decision_rows(generated_utc)
    validation = validation_rows(source_rows, nonclaim_rows, theorem_rows, diagnostic_rows, verdict_rows, candidate_rows, next_rows)

    write_csv(
        SOURCE_REGISTER_PATH,
        source_rows,
        ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NONCLAIM_SUMMARY_PATH,
        nonclaim_rows,
        ["status", "claim_ceiling", "what_derived", "what_not_derived", "C1_status", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        THEOREM_ATTEMPT_PATH,
        theorem_rows,
        ["step", "statement", "status", "blocks_C1_data_run", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NUMERIC_DIAGNOSTICS_PATH,
        diagnostic_rows,
        ["diagnostic", "value", "interpretation", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SHAPE_LOCK_VERDICT_PATH,
        verdict_rows,
        ["shape_item", "verdict", "reason", "C1_consequence", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        CANDIDATE_SHAPE_PATH,
        candidate_rows,
        ["candidate_id", "candidate_rule", "alpha_candidate", "alpha_fit", "nu_candidate", "nu_fit", "status", "allowed_use", "forbidden_use", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NEXT_DECISION_PATH,
        next_rows,
        ["decision_id", "decision", "reason", "next_target", "next_question", "run_now", "valid_for_claim", "generated_utc"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(
            generated_utc,
            source_rows,
            nonclaim_rows,
            theorem_rows,
            diagnostic_rows,
            verdict_rows,
            candidate_rows,
            next_rows,
            validation,
        ),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"814 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
