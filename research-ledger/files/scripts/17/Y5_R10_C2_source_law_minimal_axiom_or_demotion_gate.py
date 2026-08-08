from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "818-Y5-R10-C2-source-law-minimal-axiom-or-demotion-gate.md"
NEXT_TARGET = "819-Y5-R10-C2A-minimal-source-axiom-candidate-manifest.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_818_SOURCE_REGISTER.csv"
AXIOM_GATE_PATH = RESIDUALS / "P8_Y5_R10_818_MINIMAL_AXIOM_GATE.csv"
BRANCH_DECISION_PATH = RESIDUALS / "P8_Y5_R10_818_BRANCH_DECISION.csv"
AXIOM_MANIFEST_REQUIREMENTS_PATH = RESIDUALS / "P8_Y5_R10_818_AXIOM_MANIFEST_REQUIREMENTS.csv"
CLAIM_FIREWALL_PATH = RESIDUALS / "P8_Y5_R10_818_CLAIM_FIREWALL.csv"
NEXT_DECISION_PATH = RESIDUALS / "P8_Y5_R10_818_NEXT_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_818_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_818_VALIDATION.csv"

STATUS = "Y5_R10_818_C2_demoted_to_C2A_minimal_source_axiom_closure_nonclaim"
CLAIM_CEILING = "minimal_source_axiom_closure_only_no_parent_derivation_no_data_run"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    AXIOM_GATE_PATH,
    BRANCH_DECISION_PATH,
    AXIOM_MANIFEST_REQUIREMENTS_PATH,
    CLAIM_FIREWALL_PATH,
    NEXT_DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "817_doc",
        "path": POST_CHECKPOINT / "817-Y5-R10-C2-parent-source-memory-law-theorem-attempt.md",
        "needles": [
            "C2 earns a normalized-source theorem, but not a parent source law",
            "C2 is not runnable",
            "818-Y5-R10-C2-source-law-minimal-axiom-or-demotion-gate.md",
        ],
        "role": "immediate C2 theorem-attempt source",
    },
    {
        "source_id": "817_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_817_VALIDATION.csv",
        "needles": [
            "V817_5_parent_source_law_not_derived,pass",
            "V817_6_C2_not_runnable,pass",
            "V817_9_next_target_selected,pass,818-Y5-R10-C2-source-law-minimal-axiom-or-demotion-gate.md",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "formal_120_promotion",
        "path": FORMALIZATION / "120-derivability-promotion-gate.md",
        "needles": [
            "fit success does not promote a branch above Level 1 unless the rule was predeclared or independently derived.",
            "effective_model",
            "derive source terms and parameters from parent invariants or symmetry",
        ],
        "role": "promotion standard for closure versus derivation",
    },
    {
        "source_id": "formal_118_status",
        "path": FORMALIZATION / "118-cosmology-memory-status-decision.md",
        "needles": [
            "without a parent-derived source law, it is too easy to fit background distances.",
            "fit more BAO/SN branches and then rename the best shape as derived.",
            "the source hazard h(N) from microscopic/coarse-grained MTS dynamics.",
        ],
        "role": "cosmology no-fit-renaming warning",
    },
    {
        "source_id": "formal_155_Hz",
        "path": FORMALIZATION / "155-cosmology-status-after-Hz-covariance.md",
        "needles": [
            "background distances are too easy to fit phenomenologically;",
            "given Omega_Gamma(z) and w_Gamma(z), what perturbation contract is required?",
            "derive the growth/CMB consistency contract before any more cosmology data fits.",
        ],
        "role": "background-only and perturbation-contract warning",
    },
    {
        "source_id": "formal_12_parent_skeleton",
        "path": FORMALIZATION / "12-minimal-parent-theory-sketch.md",
        "needles": [
            "□Γ_mem + dV/dΓ_mem = source(invariants of ψ, T_matter, curvature)",
            "phenomenological_success until derived from Γ_mem/M dynamics",
            "all exponents are derived if they differ by sector.",
        ],
        "role": "parent skeleton and exponent discipline",
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
            "decision": "minimal source axiom is allowed only as explicit closure grammar",
            "C2_result": "parent_source_branch_demoted_until_source_law_exists",
            "C2A_result": "minimal_source_axiom_closure_contract_allowed_not_runnable",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def axiom_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "AG818_0_explicit_source_density",
            "rule": "A minimal axiom must write S_Gamma(N;I_parent) explicitly before data.",
            "allowed": "labelled closure grammar",
            "forbidden": "hidden fitted residual function",
            "gate_status": "required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "AG818_1_parent_input_list",
            "rule": "The axiom must list its parent/coarse-grained inputs I_parent and exclude target-data residuals.",
            "allowed": "Gamma_mem, X_B, Pi_B, L_cg, curvature/matter scalars, endpoint functionals",
            "forbidden": "SN/BAO/growth/CMB best-fit quantities as source inputs",
            "gate_status": "required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "AG818_2_normalization_and_bounds",
            "rule": "The axiom must prove integrability, normalization, F(0)=0, F(infinity)=1, and bounded/sign-controlled source behaviour.",
            "allowed": "monotone nonnegative source or signed source with explicit control",
            "forbidden": "unbounded or unnormalizable source law",
            "gate_status": "required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "AG818_3_no_promotion",
            "rule": "A source axiom cannot be called parent-derived until derived from parent equations/action.",
            "allowed": "Level-2 effective closure if units/conservation/known limits work",
            "forbidden": "Level-4 parent-derived component language",
            "gate_status": "permanent_firewall",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "AG818_4_no_data_run",
            "rule": "No C2A data run is allowed until an axiom manifest exists and passes the gates.",
            "allowed": "manifest writing and algebraic validation",
            "forbidden": "cosmology fit or support run",
            "gate_status": "active_block",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def branch_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch": "C2_parent_source_memory_law",
            "old_status": "conditional_source_identity_only",
            "new_status": "demoted_until_parent_source_law_exists",
            "runnable": "false",
            "reason": "source normalization theorem exists but actual parent source law is missing",
            "revival_condition": "derive S_Gamma from parent action/equations and same source perturbation closure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch": "C2A_minimal_source_axiom_closure",
            "old_status": "not_defined",
            "new_status": "closure_contract_allowed",
            "runnable": "false",
            "reason": "a minimal explicit source axiom may be useful as disciplined closure grammar, not derivation",
            "revival_condition": "write candidate axiom manifest and pass AG818 gates",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch": "C0_C1_benchmarks",
            "old_status": "benchmark_or_stress_only",
            "new_status": "retained_for_comparison_only",
            "runnable": "false",
            "reason": "benchmarks cannot replace C2A source axiom or parent derivation",
            "revival_condition": "benchmark use only after C2A manifest exists",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def axiom_manifest_requirement_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "field": "axiom_id",
            "requirement": "stable name for the candidate source law",
            "why_needed": "prevents silent mutation after results",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "S_Gamma_expression",
            "requirement": "explicit formula for S_Gamma(N;I_parent)",
            "why_needed": "source law must be inspectable before data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "I_parent_inputs",
            "requirement": "complete list of parent/coarse-grained inputs and their source paths",
            "why_needed": "blocks target-data leakage",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "normalization_proof",
            "requirement": "proof or calculation that total source budget is finite and nonzero",
            "why_needed": "needed to define F(N)",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "shape_parameters",
            "requirement": "all source parameters fixed, bounded, or explicitly labelled stress-only",
            "why_needed": "prevents C1-style fit-smuggling",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "amplitude_policy",
            "requirement": "b_mem derived, bounded, or labelled phenomenological with no support claim",
            "why_needed": "amplitude remains a known choke point",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "perturbation_policy",
            "requirement": "c_s^2, pi_Gamma, Q_m^nu, early limit, and growth-sign status",
            "why_needed": "growth/CMB cannot be interpreted without it",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_firewall_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "claim": "C2A is parent-derived",
            "status": "forbidden",
            "reason": "minimal axiom is an axiom until derived from parent equations",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "claim": "C2A can run on cosmology data now",
            "status": "forbidden",
            "reason": "candidate axiom manifest does not exist yet",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "claim": "C2A upgrades local GR/PPN",
            "status": "forbidden",
            "reason": "cosmology cannot replace MTS -> GR -> Newton derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "claim": "C2A may be a Level-2 effective closure if manifest passes",
            "status": "allowed_later",
            "reason": "effective closure is allowed if units, conservation, source normalization, and known-limit behaviour are explicit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D818_0",
            "decision": "write C2A minimal source axiom candidate manifest next",
            "reason": "C2 parent source is missing, but a labelled closure axiom may be useful if fully fenced",
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
    gate_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    manifest_rows: list[dict[str, object]],
    firewall_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V818_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )

    prior_clean, prior_detail = validation_file_clean(817)
    add("V818_1_prior_817_clean", prior_clean, prior_detail)

    add(
        "V818_2_outputs_scoped",
        all(inside_post_checkpoint(path) for path in OUTPUT_PATHS),
        str(POST_CHECKPOINT),
    )

    generated = all_generated_rows(source_rows, nonclaim_rows, gate_rows, branch_rows, manifest_rows, firewall_rows, next_rows)
    add(
        "V818_3_all_rows_nonclaim",
        all(str(row.get("valid_for_claim", "")).lower() == "false" for row in generated),
        "all generated rows valid_for_claim=false",
    )

    add(
        "V818_4_C2_demoted",
        any(row["branch"] == "C2_parent_source_memory_law" and row["new_status"] == "demoted_until_parent_source_law_exists" for row in branch_rows),
        "C2 parent-source branch demoted until source law exists",
    )

    add(
        "V818_5_C2A_closure_allowed",
        any(row["branch"] == "C2A_minimal_source_axiom_closure" and row["new_status"] == "closure_contract_allowed" for row in branch_rows),
        "C2A closure contract allowed",
    )

    add(
        "V818_6_parent_claim_forbidden",
        any(row["claim"] == "C2A is parent-derived" and row["status"] == "forbidden" for row in firewall_rows),
        "parent-derived language forbidden",
    )

    add(
        "V818_7_manifest_requirements_complete",
        {"axiom_id", "S_Gamma_expression", "I_parent_inputs", "normalization_proof", "shape_parameters", "amplitude_policy", "perturbation_policy"}.issubset(
            {row["field"] for row in manifest_rows}
        ),
        "candidate manifest fields complete",
    )

    add(
        "V818_8_no_data_run_selected",
        all(row["run_now"] == "false" for row in next_rows),
        "no data run selected",
    )

    add(
        "V818_9_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )

    formalization_changed = formalization_change_count()
    add(
        "V818_10_formalization_workbench_untouched",
        formalization_changed == 0,
        f"formalization_changed_after_cutoff={formalization_changed}",
    )

    add("V818_11_validation_rows_ready", True, "validation table constructed")
    return rows


def render_document(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    manifest_rows: list[dict[str, object]],
    firewall_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 818 - Y5 R10 C2 Source-Law Minimal Axiom Or Demotion Gate",
            (
                "Current result: **C2 is demoted as a parent-derived branch, but a C2A minimal source axiom is allowed as labelled closure grammar**. "
                "That is not a win-by-words move: C2A cannot run data, cannot claim parent derivation, and must first write a full source-axiom manifest."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Non-Claim Summary\n\n"
            + markdown_table(
                nonclaim_rows,
                ["status", "claim_ceiling", "decision", "C2_result", "C2A_result", "next_target", "valid_for_claim"],
            ),
            "## Minimal Axiom Gate\n\n"
            + markdown_table(gate_rows, ["gate_id", "rule", "allowed", "forbidden", "gate_status", "valid_for_claim"]),
            "## Branch Decision\n\n"
            + markdown_table(branch_rows, ["branch", "old_status", "new_status", "runnable", "reason", "revival_condition", "valid_for_claim"]),
            "## Axiom Manifest Requirements\n\n"
            + markdown_table(manifest_rows, ["field", "requirement", "why_needed", "valid_for_claim"]),
            "## Claim Firewall\n\n"
            + markdown_table(firewall_rows, ["claim", "status", "reason", "valid_for_claim"]),
            "## Next Decision\n\n"
            + markdown_table(next_rows, ["decision_id", "decision", "reason", "next_target", "run_now", "valid_for_claim"]),
            "## Source Register\n\n"
            + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "This is the safe compromise. We do not pretend the parent law has been derived. We also do not throw away the normalized-source machinery. C2A may become a disciplined effective closure only after its axiom manifest exists and passes the no-fit, no-overclaim gates.",
            "## Next Target\n\n`" + NEXT_TARGET + "`",
        ]
    ) + "\n"


def main() -> None:
    generated_utc = utc_stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(generated_utc)
    nonclaim_rows = nonclaim_summary_rows(generated_utc)
    gate_rows = axiom_gate_rows(generated_utc)
    branch_rows = branch_decision_rows(generated_utc)
    manifest_rows = axiom_manifest_requirement_rows(generated_utc)
    firewall_rows = claim_firewall_rows(generated_utc)
    next_rows = next_decision_rows(generated_utc)
    validation = validation_rows(source_rows, nonclaim_rows, gate_rows, branch_rows, manifest_rows, firewall_rows, next_rows)

    write_csv(
        SOURCE_REGISTER_PATH,
        source_rows,
        ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NONCLAIM_SUMMARY_PATH,
        nonclaim_rows,
        ["status", "claim_ceiling", "decision", "C2_result", "C2A_result", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        AXIOM_GATE_PATH,
        gate_rows,
        ["gate_id", "rule", "allowed", "forbidden", "gate_status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        BRANCH_DECISION_PATH,
        branch_rows,
        ["branch", "old_status", "new_status", "runnable", "reason", "revival_condition", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        AXIOM_MANIFEST_REQUIREMENTS_PATH,
        manifest_rows,
        ["field", "requirement", "why_needed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        CLAIM_FIREWALL_PATH,
        firewall_rows,
        ["claim", "status", "reason", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NEXT_DECISION_PATH,
        next_rows,
        ["decision_id", "decision", "reason", "next_target", "run_now", "valid_for_claim", "generated_utc"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(generated_utc, source_rows, nonclaim_rows, gate_rows, branch_rows, manifest_rows, firewall_rows, next_rows, validation),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"818 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
