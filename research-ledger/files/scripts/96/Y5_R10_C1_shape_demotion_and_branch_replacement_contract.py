from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "816-Y5-R10-C1-shape-demotion-and-branch-replacement-contract.md"
NEXT_TARGET = "817-Y5-R10-C2-parent-source-memory-law-theorem-attempt.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_816_SOURCE_REGISTER.csv"
DEMOTION_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_816_C1_DEMOTION_CONTRACT.csv"
REPLACEMENT_REQUIREMENTS_PATH = RESIDUALS / "P8_Y5_R10_816_REPLACEMENT_REQUIREMENTS.csv"
BRANCH_STATUS_PATH = RESIDUALS / "P8_Y5_R10_816_BRANCH_STATUS.csv"
BENCHMARK_RULES_PATH = RESIDUALS / "P8_Y5_R10_816_BENCHMARK_RULES.csv"
NEXT_DECISION_PATH = RESIDUALS / "P8_Y5_R10_816_NEXT_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_816_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_816_VALIDATION.csv"

STATUS = "Y5_R10_816_C1_shape_demoted_C2_parent_source_replacement_contract_locked_nonclaim"
CLAIM_CEILING = "replacement_contract_only_no_data_run_no_parent_shape_claim_no_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    DEMOTION_CONTRACT_PATH,
    REPLACEMENT_REQUIREMENTS_PATH,
    BRANCH_STATUS_PATH,
    BENCHMARK_RULES_PATH,
    NEXT_DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "815_doc",
        "path": POST_CHECKPOINT / "815-Y5-R10-rational-threshold-exponent-source-proof-or-shape-demotion.md",
        "needles": [
            "the rational shape clue fails as a parent proof",
            "C1_shape_7over4_3over5_demoted_to_stress_only",
            "816-Y5-R10-C1-shape-demotion-and-branch-replacement-contract.md",
        ],
        "role": "immediate C1 shape demotion source",
    },
    {
        "source_id": "815_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_815_VALIDATION.csv",
        "needles": [
            "V815_4_no_successful_exact_proof,pass",
            "V815_5_rational_candidate_demoted,pass",
            "V815_8_next_target_selected,pass,816-Y5-R10-C1-shape-demotion-and-branch-replacement-contract.md",
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
        "role": "shape mechanism and parameter gap",
    },
    {
        "source_id": "formal_118_status",
        "path": FORMALIZATION / "118-cosmology-memory-status-decision.md",
        "needles": [
            "cosmology_memory_branch_demoted_to_constraint_clue",
            "alpha_act is not parent-derived;",
            "fit more BAO/SN branches and then rename the best shape as derived.",
        ],
        "role": "no fit-renaming status",
    },
    {
        "source_id": "formal_120_promotion",
        "path": FORMALIZATION / "120-derivability-promotion-gate.md",
        "needles": [
            "fit success does not promote a branch above Level 1 unless the rule was predeclared or independently derived.",
            "alpha_act, nu_act, b_mem, and DH residual pattern are not parent-derived",
            "derive or independently predeclare the memory source shape before new fits",
        ],
        "role": "derivability promotion gate",
    },
    {
        "source_id": "formal_155_Hz",
        "path": FORMALIZATION / "155-cosmology-status-after-Hz-covariance.md",
        "needles": [
            "derive the growth/CMB consistency contract before any more cosmology data fits.",
            "growth/CMB require the memory component to say how it perturbs, clusters, or",
            "the branch cannot say how Omega_Gamma perturbs or affects growth/CMB without",
        ],
        "role": "perturbation-before-data rule",
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
            "C1_result": "rational_shape_demoted_to_stress_only",
            "replacement_branch": "C2_parent_source_memory_law",
            "replacement_status": "contract_only_not_runnable",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def demotion_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "DC816_0_C1_shape_status",
            "branch": "C1_shape_7over4_3over5",
            "locked_status": "stress_only",
            "allowed_use": "future no-claim sensitivity/stress comparison after baselines are defined",
            "forbidden_use": "parent lock, support claim, data-run permission, or replacement for a derived source law",
            "revival_condition": "independent parent theorem fixes nu=7/4 and equality activation before data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "DC816_1_Weibull_skeleton_status",
            "branch": "Weibull_threshold_family",
            "locked_status": "conditional_skeleton_only",
            "allowed_use": "template for deriving a parent activation measure",
            "forbidden_use": "treating fitted alpha_act/nu_act as derived",
            "revival_condition": "parent dynamics generate the measure dmu=h(N)dN with sourced parameters",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "DC816_2_no_fit_renaming",
            "branch": "all_future_cosmology_shapes",
            "locked_status": "no_fit_renaming",
            "allowed_use": "predeclared stress tests and source-derived branch attempts",
            "forbidden_use": "fit more data and rename the winning function as derived",
            "revival_condition": "none; this is a permanent hygiene rule",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def replacement_requirement_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "requirement_id": "RR816_0_parent_source_law",
            "replacement_branch": "C2_parent_source_memory_law",
            "must_provide": "a source law S_Gamma(N; I_parent) from parent/coarse-grained invariants, not SN/BAO/growth/CMB residuals",
            "acceptance_gate": "S_Gamma is finite, nonnegative or sign-controlled, normalized, and pre-data",
            "if_missing": "C2 is not runnable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "RR816_1_shape_from_source",
            "replacement_branch": "C2_parent_source_memory_law",
            "must_provide": "F(N)=integral_0^N S_Gamma(s)ds / integral_0^infinity S_Gamma(s)ds with F(0)=0, F(infinity)=1, and 0<=F<=1",
            "acceptance_gate": "shape parameters, if any, are fixed by I_parent or bounded before data",
            "if_missing": "shape is stress-only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "RR816_2_amplitude_from_parent",
            "replacement_branch": "C2_parent_source_memory_law",
            "must_provide": "b_mem or a narrow b_mem corridor from eta=H0 L_cg/c, a_F, and DeltaR",
            "acceptance_gate": "amplitude cannot be freely fit after seeing target residuals",
            "if_missing": "background branch remains phenomenological benchmark",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "RR816_3_perturbation_closure",
            "replacement_branch": "C2_parent_source_memory_law",
            "must_provide": "c_s^2, pi_Gamma, Q_m^nu, early-time limit, and growth-sign prediction for the same memory source",
            "acceptance_gate": "growth/CMB closure is declared before any growth/CMB data run",
            "if_missing": "background-only constraint clue",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "RR816_4_baseline_parity",
            "replacement_branch": "C2_parent_source_memory_law",
            "must_provide": "same LCDM, wCDM, CPL, and C0/C1 benchmark scorecard with honest AIC/BIC and residual anatomy",
            "acceptance_gate": "no MTS-only prosecution and no hidden baseline immunity",
            "if_missing": "run invalid",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "RR816_5_local_GR_firewall",
            "replacement_branch": "C2_parent_source_memory_law",
            "must_provide": "explicit statement that cosmology cannot upgrade local GR/PPN status",
            "acceptance_gate": "MTS -> GR -> Newton remains separate hard gate",
            "if_missing": "claim language invalid",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def branch_status_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch": "C0_frozen_smooth_memory",
            "status": "closure_benchmark_retained",
            "runnable_status": "benchmark_only",
            "reason": "has a tested closure skeleton but not parent-derived shape/amplitude",
            "next_action": "retain for fair comparison only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch": "C1_shape_7over4_3over5",
            "status": "stress_only",
            "runnable_status": "not_support_runnable",
            "reason": "rational constants lack source proof",
            "next_action": "do not use as strict candidate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch": "C2_parent_source_memory_law",
            "status": "replacement_contract_defined",
            "runnable_status": "not_runnable_until_parent_source_law",
            "reason": "must derive shape/amplitude/perturbations before data",
            "next_action": "attempt parent source law theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def benchmark_rule_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "benchmark": "C0_frozen_smooth_memory",
            "allowed": "compare against C2 to see whether derived source loses the old residual anatomy",
            "forbidden": "present C0 as parent-derived or local-GR support",
            "required_label": "closure_benchmark",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "benchmark": "C1_shape_7over4_3over5",
            "allowed": "stress-only comparison of the rational clue",
            "forbidden": "call 7/4 or 3/5 derived without a new theorem",
            "required_label": "stress_only_rational_clue",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "benchmark": "LCDM_wCDM_CPL",
            "allowed": "full fair baseline ring for every future C2 diagnostic",
            "forbidden": "MTS-only residual/jackknife tests when baselines can face the same test",
            "required_label": "required_baseline_parity",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D816_0",
            "decision": "define C2 replacement branch and attempt parent source law next",
            "reason": "C1 shape constants are stress-only, so the next honest branch must derive S_Gamma from parent invariants before data",
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
    demotion_rows: list[dict[str, object]],
    replacement_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    benchmark_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V816_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )

    prior_clean, prior_detail = validation_file_clean(815)
    add("V816_1_prior_815_clean", prior_clean, prior_detail)

    add(
        "V816_2_outputs_scoped",
        all(inside_post_checkpoint(path) for path in OUTPUT_PATHS),
        str(POST_CHECKPOINT),
    )

    generated = all_generated_rows(source_rows, nonclaim_rows, demotion_rows, replacement_rows, branch_rows, benchmark_rows, next_rows)
    add(
        "V816_3_all_rows_nonclaim",
        all(str(row.get("valid_for_claim", "")).lower() == "false" for row in generated),
        "all generated rows valid_for_claim=false",
    )

    add(
        "V816_4_C1_stress_only_locked",
        any(row["branch"] == "C1_shape_7over4_3over5" and row["status"] == "stress_only" for row in branch_rows),
        "C1 rational shape locked as stress-only",
    )

    add(
        "V816_5_C2_replacement_defined",
        any(row["branch"] == "C2_parent_source_memory_law" and row["status"] == "replacement_contract_defined" for row in branch_rows),
        "C2 replacement branch defined",
    )

    required = {
        "RR816_0_parent_source_law",
        "RR816_1_shape_from_source",
        "RR816_2_amplitude_from_parent",
        "RR816_3_perturbation_closure",
        "RR816_4_baseline_parity",
        "RR816_5_local_GR_firewall",
    }
    add(
        "V816_6_replacement_requirements_complete",
        required.issubset({row["requirement_id"] for row in replacement_rows}),
        "shape, amplitude, perturbation, baseline, and local-GR requirements present",
    )

    add(
        "V816_7_no_data_run_selected",
        all(row["run_now"] == "false" for row in next_rows),
        "no data run selected",
    )

    add(
        "V816_8_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )

    formalization_changed = formalization_change_count()
    add(
        "V816_9_formalization_workbench_untouched",
        formalization_changed == 0,
        f"formalization_changed_after_cutoff={formalization_changed}",
    )

    add("V816_10_validation_rows_ready", True, "validation table constructed")
    return rows


def render_document(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    demotion_rows: list[dict[str, object]],
    replacement_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    benchmark_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 816 - Y5 R10 C1 Shape Demotion And Branch Replacement Contract",
            (
                "Current result: **C1 is no longer a strict cosmology candidate; it is a stress-only rational-shape clue**. "
                "The replacement path is `C2_parent_source_memory_law`: derive the source law first, then shape, amplitude, perturbations, and only then data."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Non-Claim Summary\n\n"
            + markdown_table(
                nonclaim_rows,
                ["status", "claim_ceiling", "C1_result", "replacement_branch", "replacement_status", "next_target", "valid_for_claim"],
            ),
            "## C1 Demotion Contract\n\n"
            + markdown_table(
                demotion_rows,
                ["contract_id", "branch", "locked_status", "allowed_use", "forbidden_use", "revival_condition", "valid_for_claim"],
            ),
            "## Replacement Requirements\n\n"
            + markdown_table(
                replacement_rows,
                ["requirement_id", "replacement_branch", "must_provide", "acceptance_gate", "if_missing", "valid_for_claim"],
            ),
            "## Branch Status\n\n"
            + markdown_table(branch_rows, ["branch", "status", "runnable_status", "reason", "next_action", "valid_for_claim"]),
            "## Benchmark Rules\n\n"
            + markdown_table(benchmark_rows, ["benchmark", "allowed", "forbidden", "required_label", "valid_for_claim"]),
            "## Next Decision\n\n"
            + markdown_table(next_rows, ["decision_id", "decision", "reason", "next_target", "run_now", "valid_for_claim"]),
            "## Source Register\n\n"
            + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "This keeps the work honest. C1 is useful only as a stress test. C2 is the real replacement route, but it is not runnable until `S_Gamma` is derived from parent invariants and carries its amplitude and perturbation rules with it.",
            "## Next Target\n\n`" + NEXT_TARGET + "`",
        ]
    ) + "\n"


def main() -> None:
    generated_utc = utc_stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(generated_utc)
    nonclaim_rows = nonclaim_summary_rows(generated_utc)
    demotion_rows = demotion_contract_rows(generated_utc)
    replacement_rows = replacement_requirement_rows(generated_utc)
    branch_rows = branch_status_rows(generated_utc)
    benchmark_rows = benchmark_rule_rows(generated_utc)
    next_rows = next_decision_rows(generated_utc)
    validation = validation_rows(source_rows, nonclaim_rows, demotion_rows, replacement_rows, branch_rows, benchmark_rows, next_rows)

    write_csv(
        SOURCE_REGISTER_PATH,
        source_rows,
        ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NONCLAIM_SUMMARY_PATH,
        nonclaim_rows,
        ["status", "claim_ceiling", "C1_result", "replacement_branch", "replacement_status", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        DEMOTION_CONTRACT_PATH,
        demotion_rows,
        ["contract_id", "branch", "locked_status", "allowed_use", "forbidden_use", "revival_condition", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        REPLACEMENT_REQUIREMENTS_PATH,
        replacement_rows,
        ["requirement_id", "replacement_branch", "must_provide", "acceptance_gate", "if_missing", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        BRANCH_STATUS_PATH,
        branch_rows,
        ["branch", "status", "runnable_status", "reason", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        BENCHMARK_RULES_PATH,
        benchmark_rows,
        ["benchmark", "allowed", "forbidden", "required_label", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NEXT_DECISION_PATH,
        next_rows,
        ["decision_id", "decision", "reason", "next_target", "run_now", "valid_for_claim", "generated_utc"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(generated_utc, source_rows, nonclaim_rows, demotion_rows, replacement_rows, branch_rows, benchmark_rows, next_rows, validation),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"816 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
