from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "812-Y5-R10-parent-locked-memory-branch-preflight.md"
NEXT_TARGET = "813-Y5-R10-C1-parent-lock-source-hunt-or-demotion.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_812_SOURCE_REGISTER.csv"
LOCK_MANIFEST_PATH = RESIDUALS / "P8_Y5_R10_812_C1_LOCK_MANIFEST.csv"
PREFLIGHT_CHECKS_PATH = RESIDUALS / "P8_Y5_R10_812_PREFLIGHT_CHECKS.csv"
PARENT_GAPS_PATH = RESIDUALS / "P8_Y5_R10_812_PARENT_INPUT_GAPS.csv"
BASELINE_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_812_BASELINE_RUN_MATRIX.csv"
DRY_RUN_MANIFEST_PATH = RESIDUALS / "P8_Y5_R10_812_DRY_RUN_MANIFEST.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_812_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_812_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_812_VALIDATION.csv"

STATUS = "Y5_R10_812_C1_parent_locked_memory_preflight_blocked_no_data_run_nonclaim"
CLAIM_CEILING = "preflight_blocked_parent_locks_missing_no_support_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    LOCK_MANIFEST_PATH,
    PREFLIGHT_CHECKS_PATH,
    PARENT_GAPS_PATH,
    BASELINE_MATRIX_PATH,
    DRY_RUN_MANIFEST_PATH,
    DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "811_doc",
        "path": POST_CHECKPOINT / "811-Y5-R10-strict-MTS-cosmology-branch-contract.md",
        "needles": [
            "C1_parent_locked_memory",
            "shape and amplitude locks predeclared before data",
            "812-Y5-R10-parent-locked-memory-branch-preflight.md",
        ],
        "role": "strict branch contract",
    },
    {
        "source_id": "811_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_811_VALIDATION.csv",
        "needles": [
            "V811_5_parameter_locks_complete,pass",
            "V811_6_perturbation_contract_present,pass",
            "V811_8_no_data_run_selected,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "formal_172_radflat",
        "path": FORMALIZATION / "172-radiation-consistent-CMB-calibration-branch.md",
        "needles": [
            "Omega_smooth0 = 1 - Omega_m0 - Omega_r0",
            "E(0)^2 = 1",
            "b_mem value/sign are not parent-derived",
        ],
        "role": "radflat equation source",
    },
    {
        "source_id": "formal_174_bmem",
        "path": FORMALIZATION / "174-bmem-parent-boundary-law.md",
        "needles": [
            "b_mem = Omega_Gamma,inf - Omega_Gamma0.",
            "integral_0^infinity S_Gamma(N) dN = b_mem.",
            "the magnitude is not parent-derived.",
        ],
        "role": "b_mem identity and magnitude gap",
    },
    {
        "source_id": "formal_177_contract",
        "path": FORMALIZATION / "177-parent-amplitude-repair-contract.md",
        "needles": [
            "derive the amplitude before fitting it.",
            "without using the full-joint best-fit `b_mem` as input.",
            "eta, a_F, or DeltaR are tuned after the fit",
        ],
        "role": "amplitude no-fit rule",
    },
    {
        "source_id": "formal_178_attempt",
        "path": FORMALIZATION / "178-parent-amplitude-theorem-attempt.md",
        "needles": [
            "only a corridor derives, not a prediction.",
            "amplitude corridor derived = true",
            "a unique no-fit b_mem prediction.",
        ],
        "role": "corridor-only theorem attempt",
    },
    {
        "source_id": "formal_155_Hz",
        "path": FORMALIZATION / "155-cosmology-status-after-Hz-covariance.md",
        "needles": [
            "direct H(z) should not be squeezed further as a support search.",
            "given Omega_Gamma(z) and w_Gamma(z), what perturbation contract is required?",
            "cosmology remains background-only phenomenology.",
        ],
        "role": "no-Hz-rescue and perturbation warning",
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
            "branch": "C1_parent_locked_memory",
            "preflight_verdict": "blocked_for_data_run",
            "reason": "radflat equations and b_mem identities exist, but shape, amplitude, and perturbation locks are not sourced strongly enough",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def lock_manifest_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "lock_id": "L812_0_radflat_background",
            "item": "radiation-consistent flat FLRW background",
            "status": "available",
            "evidence": "E(0)^2=1 with Omega_smooth0=1-Omega_m0-Omega_r0",
            "blocks_data_run": "false",
            "required_before_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "L812_1_bmem_identity",
            "item": "b_mem identity and source integral",
            "status": "available_as_identity",
            "evidence": "b_mem=Omega_Gamma,inf-Omega_Gamma0=integral S_Gamma dN",
            "blocks_data_run": "false",
            "required_before_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "L812_2_alpha_act",
            "item": "alpha_act shape lock",
            "status": "missing_parent_source",
            "evidence": "current value is clue/predeclared candidate, not parent-derived",
            "blocks_data_run": "true",
            "required_before_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "L812_3_nu_act",
            "item": "nu_act hazard exponent lock",
            "status": "missing_parent_source",
            "evidence": "hazard form exists but exponent is not derived from source distribution",
            "blocks_data_run": "true",
            "required_before_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "L812_4_bmem_amplitude",
            "item": "b_mem predicted or narrow parent corridor",
            "status": "corridor_only_not_prediction",
            "evidence": "eta,a_F,DeltaR corridor is plausible but not unique",
            "blocks_data_run": "true",
            "required_before_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "L812_5_eta",
            "item": "eta=H0 L_cg/c",
            "status": "missing_parent_scale",
            "evidence": "L_cg not derived from parent coarse-graining law",
            "blocks_data_run": "true",
            "required_before_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "L812_6_trace_contrast",
            "item": "a_F DeltaR",
            "status": "missing_endpoint_dynamics",
            "evidence": "sign route conditional, magnitude not derived",
            "blocks_data_run": "true",
            "required_before_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "L812_7_perturbation_contract",
            "item": "c_s^2, pi_Gamma, matter coupling, early-time limit, growth sign",
            "status": "missing_physical_contract",
            "evidence": "811 lists obligations but no parent-signed values",
            "blocks_data_run": "true",
            "required_before_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def preflight_check_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "check_id": "PF812_0_equation_defined",
            "result": "pass",
            "detail": "C1 background equation can be written in radflat form",
            "consequence": "algebraic branch skeleton allowed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "check_id": "PF812_1_shape_locked",
            "result": "fail",
            "detail": "alpha_act and nu_act lack parent-sourced locks",
            "consequence": "no C1 data run",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "check_id": "PF812_2_amplitude_locked",
            "result": "fail",
            "detail": "b_mem has identity/corridor but no unique prediction or tight prior",
            "consequence": "no C1 support fit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "check_id": "PF812_3_perturbations_locked",
            "result": "fail",
            "detail": "growth/CMB variables are obligations, not sourced values",
            "consequence": "no growth/CMB claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "check_id": "PF812_4_baseline_matrix_defined",
            "result": "pass",
            "detail": "LCDM/wCDM/CPL/C0/C1 comparison matrix can be specified",
            "consequence": "future dry-run design allowed after locks",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "check_id": "PF812_5_local_GR_firewall",
            "result": "pass",
            "detail": "no cosmology result is allowed to upgrade local GR",
            "consequence": "local GR remains closure guardrail",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def parent_gap_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gap_id": "G812_0_threshold_clock",
            "missing_input": "parent derivation of alpha_act/equality-clock placement",
            "minimum_accept": "non-cosmology source or predeclared theorem fixing u_s before data",
            "if_not_filled": "C1 shape becomes stress-only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gap_id": "G812_1_hazard_exponent",
            "missing_input": "parent derivation of nu_act from source/hazard distribution",
            "minimum_accept": "microscopic/coarse-grained survival law, not fit preference",
            "if_not_filled": "C1 shape becomes stress-only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gap_id": "G812_2_coarse_graining_scale",
            "missing_input": "L_cg or eta from parent coarse-graining",
            "minimum_accept": "finite source-backed range independent of target cosmology likelihood",
            "if_not_filled": "b_mem amplitude remains phenomenological",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gap_id": "G812_3_trace_coupling",
            "missing_input": "a_F and DeltaR sign/magnitude from trace-coupling endpoint dynamics",
            "minimum_accept": "signed endpoint theorem or bounded source row",
            "if_not_filled": "positive sign stays conditional and magnitude unclaimed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gap_id": "G812_4_perturbation_sector",
            "missing_input": "c_s^2, anisotropic stress, coupling, early-time limit, growth sign",
            "minimum_accept": "smooth-memory theorem or explicit sourced perturbation closure",
            "if_not_filled": "background-only phenomenology",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def baseline_matrix_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "model": "LCDM",
            "role": "baseline",
            "runnable_now": "future_yes",
            "condition": "same data/covariance as all branches",
            "free_parameters_policy": "standard fitted baseline parameters",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "model": "wCDM",
            "role": "flexible_baseline",
            "runnable_now": "future_yes",
            "condition": "same data/covariance as all branches",
            "free_parameters_policy": "w counted honestly",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "model": "CPL",
            "role": "two_parameter_DE_baseline",
            "runnable_now": "future_yes",
            "condition": "same data/covariance and optimizer diagnostics",
            "free_parameters_policy": "w0,wa counted honestly",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "model": "C0_frozen_benchmark",
            "role": "MTS_closure_benchmark",
            "runnable_now": "future_yes_benchmark_only",
            "condition": "never support language",
            "free_parameters_policy": "benchmark freedoms counted honestly",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "model": "C1_parent_locked_memory",
            "role": "strict_MTS_candidate",
            "runnable_now": "false",
            "condition": "requires parent locks before data",
            "free_parameters_policy": "no broad b_mem/alpha/nu fitting",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def dry_run_manifest_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "manifest_id": "DRY812_0",
            "command_status": "not_generated",
            "reason": "critical C1 locks are missing",
            "would_generate_after": "alpha_act,nu_act,b_mem corridor,perturbation closure are sourced",
            "long_run_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D812_0",
            "decision": "C1 preflight blocked for data run",
            "reason": "equation skeleton exists but parent locks are missing",
            "allowed_next": "source-hunt or theorem attempt for the missing locks",
            "forbidden_next": "run C1 on cosmology data as support",
            "next_target": NEXT_TARGET,
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
    locks: list[dict[str, object]],
    checks: list[dict[str, object]],
    gaps: list[dict[str, object]],
    matrix: list[dict[str, object]],
    dry_run: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V812_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )

    prior_clean, prior_detail = validation_file_clean(811)
    add("V812_1_prior_811_clean", prior_clean, prior_detail)

    add(
        "V812_2_outputs_scoped",
        all(inside_post_checkpoint(path) for path in OUTPUT_PATHS),
        str(POST_CHECKPOINT),
    )

    generated = all_generated_rows(source_rows, nonclaim_rows, locks, checks, gaps, matrix, dry_run, decisions)
    add(
        "V812_3_all_rows_nonclaim",
        all(str(row.get("valid_for_claim", "")).lower() == "false" for row in generated),
        "all generated rows valid_for_claim=false",
    )

    critical_blockers = [row for row in locks if row["blocks_data_run"] == "true"]
    add(
        "V812_4_critical_locks_block_run",
        len(critical_blockers) >= 5,
        f"critical_lock_blockers={len(critical_blockers)}",
    )

    add(
        "V812_5_preflight_blocks_data",
        any(row["preflight_verdict"] == "blocked_for_data_run" for row in nonclaim_rows)
        and any(row["decision"] == "C1 preflight blocked for data run" for row in decisions),
        "C1 data run blocked",
    )

    add(
        "V812_6_no_command_generated",
        all(row["command_status"] == "not_generated" and row["long_run_allowed"] == "false" for row in dry_run),
        "no executable long-run command emitted",
    )

    add(
        "V812_7_baseline_matrix_retained",
        {"LCDM", "wCDM", "CPL", "C0_frozen_benchmark", "C1_parent_locked_memory"}.issubset({row["model"] for row in matrix}),
        "full fair comparison matrix retained",
    )

    add(
        "V812_8_parent_gaps_named",
        {"G812_0_threshold_clock", "G812_1_hazard_exponent", "G812_2_coarse_graining_scale", "G812_3_trace_coupling", "G812_4_perturbation_sector"}.issubset({row["gap_id"] for row in gaps}),
        "shape, amplitude, and perturbation gaps named",
    )

    add(
        "V812_9_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in decisions),
        NEXT_TARGET,
    )

    formalization_changed = formalization_change_count()
    add(
        "V812_10_formalization_workbench_untouched",
        formalization_changed == 0,
        f"formalization_changed_after_cutoff={formalization_changed}",
    )

    add("V812_11_validation_rows_ready", True, "validation table constructed")
    return rows


def render_document(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    locks: list[dict[str, object]],
    checks: list[dict[str, object]],
    gaps: list[dict[str, object]],
    matrix: list[dict[str, object]],
    dry_run: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 812 - Y5 R10 Parent-Locked Memory Branch Preflight",
            (
                "Current result: **C1 is defined but not yet runnable as an honest data branch**. "
                "The radflat background and b_mem identities are real enough to specify the skeleton, "
                "but the parent locks that would stop C1 becoming C0-with-better-clothes are missing."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Non-Claim Summary\n\n"
            + markdown_table(
                nonclaim_rows,
                ["status", "claim_ceiling", "branch", "preflight_verdict", "reason", "next_target", "valid_for_claim"],
            ),
            "## C1 Lock Manifest\n\n"
            + markdown_table(
                locks,
                ["lock_id", "item", "status", "evidence", "blocks_data_run", "required_before_claim", "valid_for_claim"],
            ),
            "## Preflight Checks\n\n"
            + markdown_table(checks, ["check_id", "result", "detail", "consequence", "valid_for_claim"]),
            "## Parent Input Gaps\n\n"
            + markdown_table(gaps, ["gap_id", "missing_input", "minimum_accept", "if_not_filled", "valid_for_claim"]),
            "## Baseline Run Matrix\n\n"
            + markdown_table(matrix, ["model", "role", "runnable_now", "condition", "free_parameters_policy", "valid_for_claim"]),
            "## Dry-Run Manifest\n\n"
            + markdown_table(dry_run, ["manifest_id", "command_status", "reason", "would_generate_after", "long_run_allowed", "valid_for_claim"]),
            "## Decision\n\n"
            + markdown_table(decisions, ["decision_id", "decision", "reason", "allowed_next", "forbidden_next", "next_target", "valid_for_claim"]),
            "## Source Register\n\n"
            + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "The branch has a skeleton, not a licence. That is useful: it prevents us spending tokens and compute on a run "
            "whose knobs are not yet parent-locked. The next move is a focused source hunt/theorem attempt for the locks, "
            "especially `alpha_act`, `nu_act`, `eta`, `a_F DeltaR`, and the perturbation closure.",
            "## Next Target\n\n`" + NEXT_TARGET + "`",
        ]
    ) + "\n"


def main() -> None:
    generated_utc = utc_stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(generated_utc)
    nonclaim_rows = nonclaim_summary_rows(generated_utc)
    locks = lock_manifest_rows(generated_utc)
    checks = preflight_check_rows(generated_utc)
    gaps = parent_gap_rows(generated_utc)
    matrix = baseline_matrix_rows(generated_utc)
    dry_run = dry_run_manifest_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    validation = validation_rows(source_rows, nonclaim_rows, locks, checks, gaps, matrix, dry_run, decisions)

    write_csv(
        SOURCE_REGISTER_PATH,
        source_rows,
        ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NONCLAIM_SUMMARY_PATH,
        nonclaim_rows,
        ["status", "claim_ceiling", "branch", "preflight_verdict", "reason", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        LOCK_MANIFEST_PATH,
        locks,
        ["lock_id", "item", "status", "evidence", "blocks_data_run", "required_before_claim", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        PREFLIGHT_CHECKS_PATH,
        checks,
        ["check_id", "result", "detail", "consequence", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        PARENT_GAPS_PATH,
        gaps,
        ["gap_id", "missing_input", "minimum_accept", "if_not_filled", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        BASELINE_MATRIX_PATH,
        matrix,
        ["model", "role", "runnable_now", "condition", "free_parameters_policy", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        DRY_RUN_MANIFEST_PATH,
        dry_run,
        ["manifest_id", "command_status", "reason", "would_generate_after", "long_run_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        DECISION_PATH,
        decisions,
        ["decision_id", "decision", "reason", "allowed_next", "forbidden_next", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(
            generated_utc,
            source_rows,
            nonclaim_rows,
            locks,
            checks,
            gaps,
            matrix,
            dry_run,
            decisions,
            validation,
        ),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"812 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
