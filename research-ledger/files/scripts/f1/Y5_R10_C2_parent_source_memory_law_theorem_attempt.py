from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "817-Y5-R10-C2-parent-source-memory-law-theorem-attempt.md"
NEXT_TARGET = "818-Y5-R10-C2-source-law-minimal-axiom-or-demotion-gate.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_817_SOURCE_REGISTER.csv"
THEOREM_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_817_SOURCE_THEOREM_ATTEMPT.csv"
SOURCE_CANDIDATES_PATH = RESIDUALS / "P8_Y5_R10_817_SOURCE_CANDIDATE_AUDIT.csv"
C2_STATUS_PATH = RESIDUALS / "P8_Y5_R10_817_C2_STATUS.csv"
MINIMAL_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_817_MINIMAL_SOURCE_CONTRACT.csv"
NEXT_DECISION_PATH = RESIDUALS / "P8_Y5_R10_817_NEXT_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_817_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_817_VALIDATION.csv"

STATUS = "Y5_R10_817_C2_normalized_source_theorem_conditional_parent_source_law_not_derived_nonclaim"
CLAIM_CEILING = "conditional_source_identity_only_C2_not_runnable_no_cosmology_support_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    THEOREM_ATTEMPT_PATH,
    SOURCE_CANDIDATES_PATH,
    C2_STATUS_PATH,
    MINIMAL_CONTRACT_PATH,
    NEXT_DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "816_doc",
        "path": POST_CHECKPOINT / "816-Y5-R10-C1-shape-demotion-and-branch-replacement-contract.md",
        "needles": [
            "C2_parent_source_memory_law",
            "a source law S_Gamma(N; I_parent) from parent/coarse-grained invariants",
            "817-Y5-R10-C2-parent-source-memory-law-theorem-attempt.md",
        ],
        "role": "immediate C2 replacement contract",
    },
    {
        "source_id": "816_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_816_VALIDATION.csv",
        "needles": [
            "V816_5_C2_replacement_defined,pass",
            "V816_6_replacement_requirements_complete,pass",
            "V816_8_next_target_selected,pass,817-Y5-R10-C2-parent-source-memory-law-theorem-attempt.md",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "formal_116_FLRW",
        "path": FORMALIZATION / "116-FLRW-memory-projection-derivation.md",
        "needles": [
            "no at the parent-derived memory-shape level.",
            "derive F(z), or replace it with a parent-predicted memory source law.",
            "test whether the Weibull expansion-clock source can be derived from allowed FLRW parent invariants",
        ],
        "role": "FLRW projection and source-law target",
    },
    {
        "source_id": "formal_117_shape",
        "path": FORMALIZATION / "117-memory-shape-source-gate.md",
        "needles": [
            "The existing `X_B/Pi_B` machinery helps with:",
            "the FLRW source curve F(N).",
            "source parameters not derived;",
        ],
        "role": "shape mechanism and XB/PiB limitation",
    },
    {
        "source_id": "formal_174_bmem",
        "path": FORMALIZATION / "174-bmem-parent-boundary-law.md",
        "needles": [
            "S_Gamma(N) = dOmega_Gamma/dN = b_mem dF/dN.",
            "So the amplitude is the total integrated memory-source budget.",
            "But it is not derived.",
        ],
        "role": "source-integral identity and amplitude gap",
    },
    {
        "source_id": "formal_12_parent_skeleton",
        "path": FORMALIZATION / "12-minimal-parent-theory-sketch.md",
        "needles": [
            "□Γ_mem + dV/dΓ_mem = source(invariants of ψ, T_matter, curvature)",
            "phenomenological_success until derived from Γ_mem/M dynamics",
            "all exponents are derived if they differ by sector.",
        ],
        "role": "parent memory skeleton",
    },
    {
        "source_id": "formal_120_promotion",
        "path": FORMALIZATION / "120-derivability-promotion-gate.md",
        "needles": [
            "fit success does not promote a branch above Level 1 unless the rule was predeclared or independently derived.",
            "derive or independently predeclare the memory source shape before new fits",
            "derive perturbation equations for the same memory fluid",
        ],
        "role": "promotion and source-before-fit rules",
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
            "what_derives": "if a finite parent source S_Gamma is supplied, F(N) is normalized by source integration",
            "what_fails": "the corpus does not supply the actual FLRW parent source law S_Gamma(N; I_parent)",
            "C2_status": "not_runnable_parent_source_law_missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def theorem_attempt_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "step": "T817_0_normalized_source_identity",
            "statement": "If parent dynamics provide an integrable source S_Gamma(N;I_parent) with total budget B=int_0^infinity S_Gamma dN != 0, then F(N)=B^-1 int_0^N S_Gamma(s)ds gives F(0)=0 and F(infinity)=1.",
            "status": "conditional_theorem",
            "C2_consequence": "shape can be generated without fitting if S_Gamma is parent-sourced",
            "blocks_data_run": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step": "T817_1_Bianchi_background_closure",
            "statement": "Given Omega_Gamma(N)=Omega_Gamma0+b_mem F(N), Bianchi conservation fixes w_Gamma once F is chosen.",
            "status": "effective_closure_available",
            "C2_consequence": "background conservation is not the blocker",
            "blocks_data_run": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step": "T817_2_parent_memory_skeleton",
            "statement": "The parent sketch contains a Gamma_mem equation sourced by invariants of psi, matter, and curvature.",
            "status": "skeleton_exists",
            "C2_consequence": "possible source-law route exists in principle",
            "blocks_data_run": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step": "T817_3_FLRW_reduction_gap",
            "statement": "No inspected source derives the FLRW reduction from the Gamma_mem parent equation to a unique S_Gamma(N;I_parent).",
            "status": "not_derived",
            "C2_consequence": "C2 is not runnable",
            "blocks_data_run": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step": "T817_4_same_source_perturbation_gap",
            "statement": "The same parent source does not yet produce c_s^2, pi_Gamma, Q_m^nu, early-time limit, and growth sign.",
            "status": "not_derived",
            "C2_consequence": "no growth/CMB support language",
            "blocks_data_run": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def source_candidate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "candidate": "Gamma_mem_parent_equation",
            "source_basis": "formal_12_parent_skeleton",
            "verdict": "skeleton_only",
            "why_not_enough": "source(invariants) is named but not reduced to an FLRW ODE or source density",
            "next_requirement": "derive FLRW projection and source density from the parent equation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate": "expansion_clock_N",
            "source_basis": "formal_116_FLRW; formal_117_shape",
            "verdict": "allowed_clock_not_source_law",
            "why_not_enough": "N=ln(1+z) can parameterize source exposure but does not define the source density",
            "next_requirement": "derive dmu/dN from parent invariants",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate": "X_B_Pi_B_routing",
            "source_basis": "formal_117_shape; equation-register search",
            "verdict": "regime_selector_not_shape_generator",
            "why_not_enough": "X_B/Pi_B helps active-versus-screened routing, but does not derive F(N)",
            "next_requirement": "connect cosmological U_B/Pi_B evolution to S_Gamma with no sector tuning",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate": "b_mem_source_integral",
            "source_basis": "formal_174_bmem",
            "verdict": "amplitude_meaning_not_time_profile",
            "why_not_enough": "integral S_Gamma dN=b_mem fixes meaning after S_Gamma is known, not the shape of S_Gamma",
            "next_requirement": "derive S_Gamma(N) and endpoint contrast from the same parent law",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate": "Weibull_or_rational_template",
            "source_basis": "815 demotion",
            "verdict": "stress_template_only",
            "why_not_enough": "C1 shape constants are unsourced and cannot be reused as C2 locks",
            "next_requirement": "replace with parent-generated source or keep stress-only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def c2_status_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch": "C2_parent_source_memory_law",
            "status": "conditional_source_identity_only",
            "runnable": "false",
            "reason": "normalized-source theorem exists but parent source density is missing",
            "promotion_condition": "derive S_Gamma(N;I_parent), b_mem corridor, and perturbation closure from the same parent source",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def minimal_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "clause": "MC817_0_source_density",
            "minimum": "S_Gamma(N;I_parent) must be explicit, finite, pre-data, and not a fitted residual function",
            "if_missing": "C2 not runnable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause": "MC817_1_parent_inputs",
            "minimum": "I_parent must list only parent/coarse-grained invariants such as Gamma_mem, X_B, Pi_B, L_cg, curvature/matter scalars, or endpoint functionals",
            "if_missing": "source law is not parent-owned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause": "MC817_2_normalization",
            "minimum": "F(N)=int_0^N S/int_0^infinity S must satisfy F(0)=0, F(infinity)=1, and bounded monotonicity or signed-control rules",
            "if_missing": "background equation under-defined",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause": "MC817_3_amplitude",
            "minimum": "b_mem must be derived or narrowed from eta, a_F, DeltaR, endpoint contrast, or a source-budget theorem",
            "if_missing": "phenomenological amplitude only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause": "MC817_4_perturbations",
            "minimum": "same source must specify smooth/clustering/coupled perturbation behavior before growth/CMB data",
            "if_missing": "background-only clue",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D817_0",
            "decision": "C2 theorem attempt fails as runnable branch; move to minimal source axiom or demotion gate",
            "reason": "source normalization derives conditionally, but S_Gamma itself is not parent-derived",
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
    theorem_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    status_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V817_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )

    prior_clean, prior_detail = validation_file_clean(816)
    add("V817_1_prior_816_clean", prior_clean, prior_detail)

    add(
        "V817_2_outputs_scoped",
        all(inside_post_checkpoint(path) for path in OUTPUT_PATHS),
        str(POST_CHECKPOINT),
    )

    generated = all_generated_rows(source_rows, nonclaim_rows, theorem_rows, candidate_rows, status_rows, contract_rows, next_rows)
    add(
        "V817_3_all_rows_nonclaim",
        all(str(row.get("valid_for_claim", "")).lower() == "false" for row in generated),
        "all generated rows valid_for_claim=false",
    )

    add(
        "V817_4_normalized_source_identity_present",
        any(row["step"] == "T817_0_normalized_source_identity" and row["status"] == "conditional_theorem" for row in theorem_rows),
        "conditional normalized source theorem recorded",
    )

    add(
        "V817_5_parent_source_law_not_derived",
        any(row["step"] == "T817_3_FLRW_reduction_gap" and row["status"] == "not_derived" for row in theorem_rows),
        "FLRW parent source law remains missing",
    )

    add(
        "V817_6_C2_not_runnable",
        all(row["runnable"] == "false" for row in status_rows),
        "C2 not runnable",
    )

    add(
        "V817_7_minimal_contract_complete",
        {"MC817_0_source_density", "MC817_1_parent_inputs", "MC817_2_normalization", "MC817_3_amplitude", "MC817_4_perturbations"}.issubset(
            {row["clause"] for row in contract_rows}
        ),
        "minimal source contract includes source, inputs, normalization, amplitude, perturbations",
    )

    add(
        "V817_8_no_data_run_selected",
        all(row["run_now"] == "false" for row in next_rows),
        "no data run selected",
    )

    add(
        "V817_9_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )

    formalization_changed = formalization_change_count()
    add(
        "V817_10_formalization_workbench_untouched",
        formalization_changed == 0,
        f"formalization_changed_after_cutoff={formalization_changed}",
    )

    add("V817_11_validation_rows_ready", True, "validation table constructed")
    return rows


def render_document(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    status_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 817 - Y5 R10 C2 Parent-Source Memory Law Theorem Attempt",
            (
                "Current result: **C2 earns a normalized-source theorem, but not a parent source law**. "
                "If the parent gives `S_Gamma`, the background shape follows cleanly; the problem is that the inspected corpus still does not derive `S_Gamma(N; I_parent)` itself."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Non-Claim Summary\n\n"
            + markdown_table(
                nonclaim_rows,
                ["status", "claim_ceiling", "what_derives", "what_fails", "C2_status", "next_target", "valid_for_claim"],
            ),
            "## Source Theorem Attempt\n\n"
            + markdown_table(theorem_rows, ["step", "statement", "status", "C2_consequence", "blocks_data_run", "valid_for_claim"]),
            "## Source Candidate Audit\n\n"
            + markdown_table(candidate_rows, ["candidate", "source_basis", "verdict", "why_not_enough", "next_requirement", "valid_for_claim"]),
            "## C2 Status\n\n"
            + markdown_table(status_rows, ["branch", "status", "runnable", "reason", "promotion_condition", "valid_for_claim"]),
            "## Minimal Source Contract\n\n"
            + markdown_table(contract_rows, ["clause", "minimum", "if_missing", "valid_for_claim"]),
            "## Next Decision\n\n"
            + markdown_table(next_rows, ["decision_id", "decision", "reason", "next_target", "run_now", "valid_for_claim"]),
            "## Source Register\n\n"
            + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "C2 is closer to being a real field-theory branch than C1 because it asks for the right object: a parent source law. But right now it has a theorem shell, not a law. The next gate must decide whether a minimal explicit source axiom is acceptable as a labelled closure, or whether C2 is demoted until the parent action supplies it.",
            "## Next Target\n\n`" + NEXT_TARGET + "`",
        ]
    ) + "\n"


def main() -> None:
    generated_utc = utc_stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(generated_utc)
    nonclaim_rows = nonclaim_summary_rows(generated_utc)
    theorem_rows = theorem_attempt_rows(generated_utc)
    candidate_rows = source_candidate_rows(generated_utc)
    status_rows = c2_status_rows(generated_utc)
    contract_rows = minimal_contract_rows(generated_utc)
    next_rows = next_decision_rows(generated_utc)
    validation = validation_rows(source_rows, nonclaim_rows, theorem_rows, candidate_rows, status_rows, contract_rows, next_rows)

    write_csv(
        SOURCE_REGISTER_PATH,
        source_rows,
        ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NONCLAIM_SUMMARY_PATH,
        nonclaim_rows,
        ["status", "claim_ceiling", "what_derives", "what_fails", "C2_status", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        THEOREM_ATTEMPT_PATH,
        theorem_rows,
        ["step", "statement", "status", "C2_consequence", "blocks_data_run", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SOURCE_CANDIDATES_PATH,
        candidate_rows,
        ["candidate", "source_basis", "verdict", "why_not_enough", "next_requirement", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        C2_STATUS_PATH,
        status_rows,
        ["branch", "status", "runnable", "reason", "promotion_condition", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        MINIMAL_CONTRACT_PATH,
        contract_rows,
        ["clause", "minimum", "if_missing", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NEXT_DECISION_PATH,
        next_rows,
        ["decision_id", "decision", "reason", "next_target", "run_now", "valid_for_claim", "generated_utc"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(generated_utc, source_rows, nonclaim_rows, theorem_rows, candidate_rows, status_rows, contract_rows, next_rows, validation),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"817 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
