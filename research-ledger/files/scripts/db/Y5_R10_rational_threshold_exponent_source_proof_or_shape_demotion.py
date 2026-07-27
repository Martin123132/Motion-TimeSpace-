from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "815-Y5-R10-rational-threshold-exponent-source-proof-or-shape-demotion.md"
NEXT_TARGET = "816-Y5-R10-C1-shape-demotion-and-branch-replacement-contract.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_815_SOURCE_REGISTER.csv"
PROOF_ROUTE_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_815_PROOF_ROUTE_AUDIT.csv"
RATIONAL_CANDIDATE_STATUS_PATH = RESIDUALS / "P8_Y5_R10_815_RATIONAL_CANDIDATE_STATUS.csv"
SHAPE_DEMOTION_PATH = RESIDUALS / "P8_Y5_R10_815_SHAPE_DEMOTION.csv"
NEXT_DECISION_PATH = RESIDUALS / "P8_Y5_R10_815_NEXT_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_815_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_815_VALIDATION.csv"

STATUS = "Y5_R10_815_rational_threshold_proof_failed_shape_demoted_stress_only_nonclaim"
CLAIM_CEILING = "rational_shape_clue_stress_only_no_C1_data_run_no_parent_shape_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    PROOF_ROUTE_AUDIT_PATH,
    RATIONAL_CANDIDATE_STATUS_PATH,
    SHAPE_DEMOTION_PATH,
    NEXT_DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "814_doc",
        "path": POST_CHECKPOINT / "814-Y5-R10-threshold-distribution-parent-law-attempt.md",
        "needles": [
            "the fitted shape constants are not yet parent-derived",
            "C1_shape_7over4_3over5",
            "815-Y5-R10-rational-threshold-exponent-source-proof-or-shape-demotion.md",
        ],
        "role": "immediate rational-shape proof target",
    },
    {
        "source_id": "814_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_814_VALIDATION.csv",
        "needles": [
            "V814_5_exact_shape_not_parent_locked,pass",
            "V814_6_rational_clue_recorded,pass",
            "V814_8_next_target_selected,pass,815-Y5-R10-rational-threshold-exponent-source-proof-or-shape-demotion.md",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "formal_117_shape",
        "path": FORMALIZATION / "117-memory-shape-source-gate.md",
        "needles": [
            "Weibull F can be constructed as an expansion-clock threshold/survival law,",
            "alpha_act and nu_act are not parent-derived.",
            "derive the threshold distribution from microscopic/coarse-grained MTS dynamics",
        ],
        "role": "shape source gate",
    },
    {
        "source_id": "formal_118_status",
        "path": FORMALIZATION / "118-cosmology-memory-status-decision.md",
        "needles": [
            "cosmology_memory_branch_demoted_to_constraint_clue",
            "alpha_act is not parent-derived;",
            "nu_act is not parent-derived;",
        ],
        "role": "cosmology memory demotion source",
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
            "proof_verdict": "rational_shape_source_proof_failed",
            "shape_status": "C1_shape_7over4_3over5_demoted_to_stress_only",
            "what_survives": "conditional Weibull theorem and rational numerical clue",
            "what_failed": "independent parent source for nu=7/4 or F(u_eq)=3/5",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def proof_route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "R815_0_corpus_direct_source",
            "route": "Search corpus for independent parent statements fixing 7/4 or 3/5.",
            "result": "fail",
            "reason": "No independent source theorem for these constants was found; they first appear as numeric clues in 814.",
            "what_it_would_need": "pre-existing parent action, symmetry, dimensional, or fixed-point result selecting the constants",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "R815_1_dimension_codimension_ratio",
            "route": "Explain nu=7/4 as d/p from activation-measure dimension over response power.",
            "result": "fail_conditional_only",
            "reason": "d/p=7/4 would require a sourced seven-over-four structure; the corpus has no parent derivation of d=7 and p=4 for FLRW activation thresholds.",
            "what_it_would_need": "identified parent threshold manifold dimension and response power, both independent of cosmology data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "R815_2_hazard_regularitiy",
            "route": "Use regularity of h(N) near N=0 to force the exponent.",
            "result": "fail_bounds_only",
            "reason": "Regularity can motivate broad constraints such as positive hazard and finite source, but it does not select 7/4.",
            "what_it_would_need": "a precise differentiability/vanishing-order theorem that uniquely fixes nu=7/4",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "R815_3_equality_partition",
            "route": "Derive F(u_eq)=3/5 from matter-memory equality.",
            "result": "fail_clue_only",
            "reason": "Equality supplies a natural clock but not a partition rule giving exactly 3/5 activation.",
            "what_it_would_need": "parent conservation or counting law forcing 3 activated weights out of 5 at equality",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "R815_4_max_entropy_weibull",
            "route": "Use maximum-entropy or survival-process arguments to select Weibull constants.",
            "result": "fail_form_only",
            "reason": "Survival arguments select a family once constraints are chosen; they do not supply the parent constraints that fix 7/4 or 3/5.",
            "what_it_would_need": "parent-derived moment/scale constraints before data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def rational_candidate_status_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "candidate_id": "C1_shape_7over4_3over5",
            "status_before_815": "interesting_rational_source_target_not_parent_derived",
            "status_after_815": "stress_only_candidate",
            "reason": "the constants are numerically sharp but source-unsourced",
            "allowed_use": "future no-claim stress test or theorem target",
            "forbidden_use": "C1 parent lock, data-run permission, support claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def shape_demotion_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "item": "Weibull functional form",
            "new_status": "conditional_skeleton_retained",
            "reason": "derived from Poisson/power-law activation measure if parent supplies the measure",
            "blocks_data_run": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "item": "nu=7/4",
            "new_status": "stress_only",
            "reason": "no parent source proof",
            "blocks_data_run": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "item": "F(u_eq)=3/5",
            "new_status": "stress_only",
            "reason": "no parent equality-partition law",
            "blocks_data_run": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "item": "alpha_act derived from rational candidate",
            "new_status": "stress_only",
            "reason": "depends on unsourced 3/5 equality activation rule",
            "blocks_data_run": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D815_0",
            "decision": "demote rational C1 shape to stress-only and write branch-replacement contract",
            "reason": "exact shape constants are not parent-derived after proof-route audit",
            "next_target": NEXT_TARGET,
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
    proof_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    demotion_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V815_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )

    prior_clean, prior_detail = validation_file_clean(814)
    add("V815_1_prior_814_clean", prior_clean, prior_detail)

    add(
        "V815_2_outputs_scoped",
        all(inside_post_checkpoint(path) for path in OUTPUT_PATHS),
        str(POST_CHECKPOINT),
    )

    generated = all_generated_rows(source_rows, nonclaim_rows, proof_rows, candidate_rows, demotion_rows_, next_rows)
    add(
        "V815_3_all_rows_nonclaim",
        all(str(row.get("valid_for_claim", "")).lower() == "false" for row in generated),
        "all generated rows valid_for_claim=false",
    )

    add(
        "V815_4_no_successful_exact_proof",
        all(not row["result"].startswith("pass") for row in proof_rows),
        "no proof route fixed 7/4 or 3/5",
    )

    add(
        "V815_5_rational_candidate_demoted",
        any(row["candidate_id"] == "C1_shape_7over4_3over5" and row["status_after_815"] == "stress_only_candidate" for row in candidate_rows),
        "rational shape demoted to stress-only",
    )

    add(
        "V815_6_shape_blocks_data_run",
        sum(1 for row in demotion_rows_ if row["blocks_data_run"] == "true") >= 3,
        "unsourced exact shape constants block C1 data",
    )

    add(
        "V815_7_no_data_run_selected",
        all(row["run_now"] == "false" for row in next_rows),
        "no data run selected",
    )

    add(
        "V815_8_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )

    formalization_changed = formalization_change_count()
    add(
        "V815_9_formalization_workbench_untouched",
        formalization_changed == 0,
        f"formalization_changed_after_cutoff={formalization_changed}",
    )

    add("V815_10_validation_rows_ready", True, "validation table constructed")
    return rows


def render_document(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    proof_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    demotion_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 815 - Y5 R10 Rational Threshold Exponent Source Proof Or Shape Demotion",
            (
                "Current result: **the rational shape clue fails as a parent proof**. "
                "`nu=7/4` and `F(u_eq)=3/5` remain interesting, but without an independent source theorem they are not locks; "
                "the C1 shape is demoted to stress-only."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Non-Claim Summary\n\n"
            + markdown_table(
                nonclaim_rows,
                ["status", "claim_ceiling", "proof_verdict", "shape_status", "what_survives", "what_failed", "next_target", "valid_for_claim"],
            ),
            "## Proof Route Audit\n\n"
            + markdown_table(
                proof_rows,
                ["route_id", "route", "result", "reason", "what_it_would_need", "valid_for_claim"],
            ),
            "## Rational Candidate Status\n\n"
            + markdown_table(
                candidate_rows,
                ["candidate_id", "status_before_815", "status_after_815", "reason", "allowed_use", "forbidden_use", "valid_for_claim"],
            ),
            "## Shape Demotion\n\n"
            + markdown_table(demotion_rows_, ["item", "new_status", "reason", "blocks_data_run", "valid_for_claim"]),
            "## Next Decision\n\n"
            + markdown_table(next_rows, ["decision_id", "decision", "reason", "next_target", "run_now", "valid_for_claim"]),
            "## Source Register\n\n"
            + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "This is a useful failure. The theory has earned the Weibull form conditionally, but not the numbers. "
            "So the next branch must not pretend `7/4` and `3/5` are derived; it must either replace the shape with a parent-sourced law or keep the rational shape as a no-claim stress test.",
            "## Next Target\n\n`" + NEXT_TARGET + "`",
        ]
    ) + "\n"


def main() -> None:
    generated_utc = utc_stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(generated_utc)
    nonclaim_rows = nonclaim_summary_rows(generated_utc)
    proof_rows = proof_route_rows(generated_utc)
    candidate_rows = rational_candidate_status_rows(generated_utc)
    demotion_rows_ = shape_demotion_rows(generated_utc)
    next_rows = next_decision_rows(generated_utc)
    validation = validation_rows(source_rows, nonclaim_rows, proof_rows, candidate_rows, demotion_rows_, next_rows)

    write_csv(
        SOURCE_REGISTER_PATH,
        source_rows,
        ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NONCLAIM_SUMMARY_PATH,
        nonclaim_rows,
        ["status", "claim_ceiling", "proof_verdict", "shape_status", "what_survives", "what_failed", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        PROOF_ROUTE_AUDIT_PATH,
        proof_rows,
        ["route_id", "route", "result", "reason", "what_it_would_need", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RATIONAL_CANDIDATE_STATUS_PATH,
        candidate_rows,
        ["candidate_id", "status_before_815", "status_after_815", "reason", "allowed_use", "forbidden_use", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SHAPE_DEMOTION_PATH,
        demotion_rows_,
        ["item", "new_status", "reason", "blocks_data_run", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NEXT_DECISION_PATH,
        next_rows,
        ["decision_id", "decision", "reason", "next_target", "run_now", "valid_for_claim", "generated_utc"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(generated_utc, source_rows, nonclaim_rows, proof_rows, candidate_rows, demotion_rows_, next_rows, validation),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"815 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
