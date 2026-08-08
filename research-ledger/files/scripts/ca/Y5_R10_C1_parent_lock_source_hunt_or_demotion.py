from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "813-Y5-R10-C1-parent-lock-source-hunt-or-demotion.md"
NEXT_TARGET = "814-Y5-R10-threshold-distribution-parent-law-attempt.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_813_SOURCE_REGISTER.csv"
LOCK_SOURCE_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_813_LOCK_SOURCE_AUDIT.csv"
C1_DEMOTION_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_813_C1_DEMOTION_LEDGER.csv"
SOURCE_HUNT_PATHS_PATH = RESIDUALS / "P8_Y5_R10_813_SOURCE_HUNT_PATHS.csv"
NEXT_DERIVATION_TARGET_PATH = RESIDUALS / "P8_Y5_R10_813_NEXT_DERIVATION_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_813_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_813_VALIDATION.csv"

STATUS = "Y5_R10_813_C1_demoted_to_parent_lock_source_hunt_threshold_law_next_nonclaim"
CLAIM_CEILING = "C1_source_hunt_only_no_data_run_no_cosmology_support_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    LOCK_SOURCE_AUDIT_PATH,
    C1_DEMOTION_LEDGER_PATH,
    SOURCE_HUNT_PATHS_PATH,
    NEXT_DERIVATION_TARGET_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "812_doc",
        "path": POST_CHECKPOINT / "812-Y5-R10-parent-locked-memory-branch-preflight.md",
        "needles": [
            "C1 is defined but not yet runnable as an honest data branch",
            "critical C1 locks are missing",
            "813-Y5-R10-C1-parent-lock-source-hunt-or-demotion.md",
        ],
        "role": "immediate C1 preflight blocker source",
    },
    {
        "source_id": "812_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_812_VALIDATION.csv",
        "needles": [
            "V812_4_critical_locks_block_run,pass",
            "V812_5_preflight_blocks_data,pass",
            "V812_9_next_target_selected,pass,813-Y5-R10-C1-parent-lock-source-hunt-or-demotion.md",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "formal_117_shape",
        "path": FORMALIZATION / "117-memory-shape-source-gate.md",
        "needles": [
            "partly: a threshold/survival mechanism exists, but the parameters are not parent-derived.",
            "alpha_act is still fitted, not derived.",
            "derive the threshold distribution from microscopic/coarse-grained MTS dynamics",
        ],
        "role": "shape and threshold source-gate",
    },
    {
        "source_id": "formal_118_status",
        "path": FORMALIZATION / "118-cosmology-memory-status-decision.md",
        "needles": [
            "alpha_act is not parent-derived;",
            "nu_act is not parent-derived;",
            "R2: derive the threshold distribution N_th from microscopic/coarse-grained MTS dynamics;",
        ],
        "role": "cosmology memory status lock",
    },
    {
        "source_id": "formal_174_bmem",
        "path": FORMALIZATION / "174-bmem-parent-boundary-law.md",
        "needles": [
            "b_mem = Omega_Gamma,inf - Omega_Gamma0;",
            "b_mem = integral_0^infinity S_Gamma(N) dN.",
            "b_mem magnitude is demoted to calibrated phenomenological amplitude.",
        ],
        "role": "b_mem identity and amplitude gap",
    },
    {
        "source_id": "formal_178_amplitude",
        "path": FORMALIZATION / "178-parent-amplitude-theorem-attempt.md",
        "needles": [
            "only a corridor derives, not a prediction.",
            "amplitude corridor derived = true",
            "a unique no-fit b_mem prediction.",
        ],
        "role": "amplitude corridor-only result",
    },
    {
        "source_id": "spine_Lcg",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": [
            "L_cg_coherence_rule_candidate_not_derived",
            "the curvature/source coherence rule passes conditionally",
            "memory-diffusion L_cg remains open until its fixed point is solved",
        ],
        "role": "L_cg source-hunt status",
    },
    {
        "source_id": "formal_156_perturbation",
        "path": FORMALIZATION / "156-growth-CMB-consistency-preflight.md",
        "needles": [
            "c_s,Gamma^2 = 1",
            "pi_Gamma = 0",
            "Q_m^nu = 0",
            "testable_closure_not_parent_derived",
        ],
        "role": "C0 perturbation closure source",
    },
    {
        "source_id": "formal_157_growth_contract",
        "path": FORMALIZATION / "157-minimal-smooth-memory-growth-CMB-test-contract.md",
        "needles": [
            "closure_only_not_parent_derivation",
            "growth suppression.",
            "do not prosecute MTS alone with a diagnostic that baselines can also face.",
        ],
        "role": "growth/CMB closure-only contract",
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
            "C1_fate": "demoted_from_data_candidate_to_parent_lock_source_hunt",
            "what_survives": "radflat skeleton, b_mem identity, Weibull threshold mechanism, C0 smooth perturbation closure as benchmark",
            "what_blocks": "alpha_act, nu_act, eta/L_cg, a_F DeltaR, unique b_mem prediction, parent perturbation closure",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def lock_source_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "lock_id": "LS813_0_radflat_background",
            "lock_item": "radiation-consistent background equation",
            "candidate_source": "formal_172_radflat; 812_doc",
            "source_verdict": "source_locked_for_skeleton",
            "data_status": "usable_for_algebraic_preflight_only",
            "blocks_C1_data_run": "false",
            "next_action": "carry forward",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "LS813_1_bmem_identity",
            "lock_item": "b_mem identity/source integral",
            "candidate_source": "formal_174_bmem",
            "source_verdict": "meaning_locked_not_prediction",
            "data_status": "usable_for_parameter_meaning_only",
            "blocks_C1_data_run": "false",
            "next_action": "carry forward but do not treat as amplitude prediction",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "LS813_2_alpha_act",
            "lock_item": "alpha_act equality-clock placement",
            "candidate_source": "formal_117_shape; formal_118_status",
            "source_verdict": "clue_only_not_parent_locked",
            "data_status": "blocks_C1",
            "blocks_C1_data_run": "true",
            "next_action": "derive threshold distribution or demote shape to stress-only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "LS813_3_nu_act",
            "lock_item": "nu_act hazard exponent",
            "candidate_source": "formal_117_shape; formal_118_status",
            "source_verdict": "hazard_form_constructed_exponent_not_parent_locked",
            "data_status": "blocks_C1",
            "blocks_C1_data_run": "true",
            "next_action": "derive microscopic/coarse-grained threshold distribution",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "LS813_4_eta_Lcg",
            "lock_item": "eta=H0 L_cg/c",
            "candidate_source": "spine_Lcg; formal_178_amplitude",
            "source_verdict": "candidate_rule_conditional_not_fixed_point_derived",
            "data_status": "blocks_C1",
            "blocks_C1_data_run": "true",
            "next_action": "derive L_cg fixed point or finite source-backed corridor",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "LS813_5_aF_DeltaR",
            "lock_item": "a_F DeltaR trace-coupling contrast",
            "candidate_source": "formal_174_bmem; formal_178_amplitude",
            "source_verdict": "positive_sign_conditional_magnitude_not_locked",
            "data_status": "blocks_C1",
            "blocks_C1_data_run": "true",
            "next_action": "derive endpoint ordering and trace-coupling normalization",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "LS813_6_bmem_prediction",
            "lock_item": "unique or tight b_mem prediction",
            "candidate_source": "formal_174_bmem; formal_178_amplitude",
            "source_verdict": "corridor_only_not_prediction",
            "data_status": "blocks_C1_support",
            "blocks_C1_data_run": "true",
            "next_action": "do not fit b_mem until eta,a_F,DeltaR are sourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "LS813_7_perturbation_closure",
            "lock_item": "c_s^2, pi_Gamma, Q_m^nu, early fraction, growth sign",
            "candidate_source": "formal_156_perturbation; formal_157_growth_contract",
            "source_verdict": "C0_closure_locked_not_parent_derivation",
            "data_status": "benchmark_only",
            "blocks_C1_data_run": "true",
            "next_action": "derive smooth-memory closure from parent or keep growth/CMB closure-only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def demotion_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch": "C1_parent_locked_memory",
            "old_status": "strict_MTS_candidate_pending_preflight",
            "new_status": "parent_lock_source_hunt_only",
            "reason": "critical locks remain clue-only, conditional, or closure-only",
            "allowed_use": "organize derivation targets; compare to C0 only after locks are sourced",
            "forbidden_use": "run on cosmology data as support or claim C1 evidence",
            "revival_condition": "alpha_act, nu_act, eta/L_cg, a_F DeltaR, b_mem corridor, and perturbation closure become parent-sourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch": "C0_frozen_smooth_memory",
            "old_status": "closure_benchmark",
            "new_status": "closure_benchmark_retained",
            "reason": "C0 supplies the fair comparison skeleton but not a parent-derived theory",
            "allowed_use": "benchmark residual anatomy and perturbation closure behavior",
            "forbidden_use": "C0 evidence or local-GR support",
            "revival_condition": "parent amplitude and perturbation derivations succeed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def source_hunt_path_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "path_id": "P813_A_threshold_distribution",
            "target": "alpha_act and nu_act",
            "source_basis": "117 constructs a Weibull threshold mechanism but leaves N_th distribution underived",
            "rank": "first",
            "reason": "without shape locks C1 is stress-only before amplitude even matters",
            "success_condition": "derive or bound the threshold distribution from parent/coarse-grained dynamics without cosmology-fit input",
            "failure_action": "demote C1 shape to stress-only and move to branch replacement",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "path_id": "P813_B_amplitude_coupling",
            "target": "eta, a_F, DeltaR, b_mem",
            "source_basis": "174/178 give identity and order-one corridor, not prediction",
            "rank": "second_parallel",
            "reason": "amplitude remains the C0/C1 choke point",
            "success_condition": "derive a finite parent corridor narrow enough to be predeclared",
            "failure_action": "keep b_mem phenomenological and C1 blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "path_id": "P813_C_Lcg_fixed_point",
            "target": "L_cg/eta",
            "source_basis": "spine has candidate universal coherence rule, conditionally passing but not fixed-point derived",
            "rank": "second_parallel",
            "reason": "eta controls whether amplitude corridor is meaningful",
            "success_condition": "derive L_cg from universal source/coherence rule without sector tuning",
            "failure_action": "no parent b_mem prediction",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "path_id": "P813_D_perturbation_parent_closure",
            "target": "smooth-memory perturbation closure",
            "source_basis": "156/157 define C0 closure c_s^2=1, pi=0, Q=0 but label it closure-only",
            "rank": "third",
            "reason": "needed before growth/CMB can become physics rather than benchmark testing",
            "success_condition": "derive closure from parent action or a signed effective stress-energy theorem",
            "failure_action": "growth/CMB remains closure-only holdout",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_derivation_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "priority": "1",
            "next_target": NEXT_TARGET,
            "derivation_question": "Can the Weibull threshold distribution N_th be derived or bounded from parent/coarse-grained MTS dynamics?",
            "why_first": "alpha_act and nu_act block C1 before amplitude fitting; 117 already gives a concrete partial mechanism to attack",
            "acceptance_gate": "derive alpha_act/nu_act or a finite pre-data corridor without using SN/BAO/growth/CMB best fits",
            "if_fails": "C1 shape is demoted to stress-only and strict branch replacement becomes the honest route",
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
    audit_rows: list[dict[str, object]],
    demotion: list[dict[str, object]],
    paths: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V813_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )

    prior_clean, prior_detail = validation_file_clean(812)
    add("V813_1_prior_812_clean", prior_clean, prior_detail)

    add(
        "V813_2_outputs_scoped",
        all(inside_post_checkpoint(path) for path in OUTPUT_PATHS),
        str(POST_CHECKPOINT),
    )

    generated = all_generated_rows(source_rows, nonclaim_rows, audit_rows, demotion, paths, next_rows)
    add(
        "V813_3_all_rows_nonclaim",
        all(str(row.get("valid_for_claim", "")).lower() == "false" for row in generated),
        "all generated rows valid_for_claim=false",
    )

    blockers = [row for row in audit_rows if row["blocks_C1_data_run"] == "true"]
    add(
        "V813_4_C1_blockers_retained",
        len(blockers) >= 5,
        f"C1_lock_blockers={len(blockers)}",
    )

    add(
        "V813_5_C1_demoted_to_source_hunt",
        any(row["branch"] == "C1_parent_locked_memory" and row["new_status"] == "parent_lock_source_hunt_only" for row in demotion),
        "C1 demoted from data candidate to source hunt",
    )

    add(
        "V813_6_threshold_path_selected_first",
        any(row["path_id"] == "P813_A_threshold_distribution" and row["rank"] == "first" for row in paths),
        "threshold distribution derivation selected first",
    )

    add(
        "V813_7_no_data_run_selected",
        all(row["run_now"] == "false" for row in next_rows),
        "no data run selected",
    )

    add(
        "V813_8_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )

    formalization_changed = formalization_change_count()
    add(
        "V813_9_formalization_workbench_untouched",
        formalization_changed == 0,
        f"formalization_changed_after_cutoff={formalization_changed}",
    )

    add("V813_10_validation_rows_ready", True, "validation table constructed")
    return rows


def render_document(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    audit_rows: list[dict[str, object]],
    demotion: list[dict[str, object]],
    paths: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 813 - Y5 R10 C1 Parent-Lock Source Hunt Or Demotion",
            (
                "Current result: **C1 is not dead, but it is demoted out of the data ring**. "
                "The source hunt found real partial structures — Weibull threshold mechanism, b_mem identity, "
                "conditional L_cg/amplitude corridors, and C0 smooth closure — but none are strong enough to make C1 runnable."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Non-Claim Summary\n\n"
            + markdown_table(
                nonclaim_rows,
                ["status", "claim_ceiling", "C1_fate", "what_survives", "what_blocks", "next_target", "valid_for_claim"],
            ),
            "## Lock Source Audit\n\n"
            + markdown_table(
                audit_rows,
                [
                    "lock_id",
                    "lock_item",
                    "candidate_source",
                    "source_verdict",
                    "data_status",
                    "blocks_C1_data_run",
                    "next_action",
                    "valid_for_claim",
                ],
            ),
            "## C1 Demotion Ledger\n\n"
            + markdown_table(
                demotion,
                [
                    "branch",
                    "old_status",
                    "new_status",
                    "reason",
                    "allowed_use",
                    "forbidden_use",
                    "revival_condition",
                    "valid_for_claim",
                ],
            ),
            "## Source-Hunt Paths\n\n"
            + markdown_table(
                paths,
                [
                    "path_id",
                    "target",
                    "source_basis",
                    "rank",
                    "reason",
                    "success_condition",
                    "failure_action",
                    "valid_for_claim",
                ],
            ),
            "## Next Derivation Target\n\n"
            + markdown_table(
                next_rows,
                ["priority", "next_target", "derivation_question", "why_first", "acceptance_gate", "if_fails", "run_now", "valid_for_claim"],
            ),
            "## Source Register\n\n"
            + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "C1 does not get to fight yet. The first real derivation attack is the threshold distribution: "
            "if `N_th` can be derived, `alpha_act` and `nu_act` stop being dressed-up fit memories. "
            "If it cannot, C1's shape is stress-only and the branch should be replaced rather than rescued.",
            "## Next Target\n\n`" + NEXT_TARGET + "`",
        ]
    ) + "\n"


def main() -> None:
    generated_utc = utc_stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(generated_utc)
    nonclaim_rows = nonclaim_summary_rows(generated_utc)
    audit_rows = lock_source_audit_rows(generated_utc)
    demotion = demotion_rows(generated_utc)
    paths = source_hunt_path_rows(generated_utc)
    next_rows = next_derivation_rows(generated_utc)
    validation = validation_rows(source_rows, nonclaim_rows, audit_rows, demotion, paths, next_rows)

    write_csv(
        SOURCE_REGISTER_PATH,
        source_rows,
        ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NONCLAIM_SUMMARY_PATH,
        nonclaim_rows,
        ["status", "claim_ceiling", "C1_fate", "what_survives", "what_blocks", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        LOCK_SOURCE_AUDIT_PATH,
        audit_rows,
        [
            "lock_id",
            "lock_item",
            "candidate_source",
            "source_verdict",
            "data_status",
            "blocks_C1_data_run",
            "next_action",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        C1_DEMOTION_LEDGER_PATH,
        demotion,
        [
            "branch",
            "old_status",
            "new_status",
            "reason",
            "allowed_use",
            "forbidden_use",
            "revival_condition",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        SOURCE_HUNT_PATHS_PATH,
        paths,
        [
            "path_id",
            "target",
            "source_basis",
            "rank",
            "reason",
            "success_condition",
            "failure_action",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        NEXT_DERIVATION_TARGET_PATH,
        next_rows,
        ["priority", "next_target", "derivation_question", "why_first", "acceptance_gate", "if_fails", "run_now", "valid_for_claim", "generated_utc"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(generated_utc, source_rows, nonclaim_rows, audit_rows, demotion, paths, next_rows, validation),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"813 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
