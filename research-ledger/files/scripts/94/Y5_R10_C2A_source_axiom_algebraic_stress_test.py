from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "820-Y5-R10-C2A-source-axiom-algebraic-stress-test.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_820_SOURCE_REGISTER.csv"
STRESS_TESTS_PATH = RESIDUALS / "P8_Y5_R10_820_STRESS_TESTS.csv"
ENDPOINT_LAWS_PATH = RESIDUALS / "P8_Y5_R10_820_ENDPOINT_LAWS.csv"
COUNTEREXAMPLES_PATH = RESIDUALS / "P8_Y5_R10_820_COUNTEREXAMPLES.csv"
SURVIVAL_CONDITIONS_PATH = RESIDUALS / "P8_Y5_R10_820_SURVIVAL_CONDITIONS.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_820_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_820_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_820_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_820_VALIDATION.csv"

AXIOM_ID = "C2A_TS1_threshold_survival_source_closure"
STATUS = "Y5_R10_820_C2A_algebra_survives_only_as_parent_locked_closure_nonclaim"
CLAIM_CEILING = "Level_2_effective_closure_candidate_only_no_parent_derivation_no_data_run"
NEXT_TARGET = "821-Y5-R10-C2A-parent-control-scalar-candidate-hunt.md"

SOURCE_SPECS = [
    {
        "source_id": "819_doc",
        "path": POST_CHECKPOINT / "819-Y5-R10-C2A-minimal-source-axiom-candidate-manifest.md",
        "needles": [
            "C2A now has one explicit candidate source-law manifest",
            "S_Gamma(N;I_parent)=B_mem*dF_X/dN",
            "820-Y5-R10-C2A-source-axiom-algebraic-stress-test.md",
        ],
        "role": "immediate source-axiom manifest",
    },
    {
        "source_id": "819_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_819_VALIDATION.csv",
        "needles": [
            "V819_2_explicit_expression_present,pass",
            "V819_4_algebra_blocks_data,pass",
            "V819_6_firewalls_active,pass",
            "V819_8_next_target_selected,pass,820-Y5-R10-C2A-source-axiom-algebraic-stress-test.md",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "819_manifest",
        "path": RESIDUALS / "P8_Y5_R10_819_AXIOM_CANDIDATE_MANIFEST.csv",
        "needles": [
            "S_Gamma_expression",
            "S_Gamma(N;I_parent)=B_mem*dF_X/dN",
            "p_source remains a symbolic closure-shape exponent",
        ],
        "role": "machine-readable candidate source law",
    },
    {
        "source_id": "formal_120_promotion",
        "path": FORMALIZATION / "120-derivability-promotion-gate.md",
        "needles": [
            "fit success does not promote a branch above Level 1 unless the rule was predeclared or independently derived.",
            "effective_model",
            "derive source terms and parameters from parent invariants or symmetry",
        ],
        "role": "promotion standard and anti-fit-smuggling gate",
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


def stress_test_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "test_id": "T820_0_exact_derivative",
            "question": "Is S_Gamma exactly the derivative of a bounded cumulative source?",
            "result": "survives_conditionally",
            "derivation": "For F_X=1-exp[-(X/X_star)^p], dF_X/dN=p*(X/X_star)^(p-1)*(dX/dN)/X_star*exp[-(X/X_star)^p]. Thus S_Gamma=B_mem*dF_X/dN.",
            "required_condition": "X differentiable or absolutely continuous; p>0; X_star>0",
            "failure_mode": "without a defined parent X(N), the derivative identity is algebraic closure only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "T820_1_positivity",
            "question": "When is the source nonnegative?",
            "result": "survives_only_with_sign_locks",
            "derivation": "The exponential and power factor are nonnegative for X>=0. The sign is sign(B_mem*dX/dN) when p>0 and X_star>0.",
            "required_condition": "B_mem>=0 and dX/dN>=0 on the branch, or an explicit signed-source policy",
            "failure_mode": "any interval with dX/dN<0 creates a sink/negative source",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "T820_2_normalization",
            "question": "When does the total source equal B_mem?",
            "result": "survives_only_with_endpoint_locks",
            "derivation": "Integral S_Gamma dN=B_mem[F_X(N_f)-F_X(N_i)]. Full normalization needs F_X(N_i)=0 and F_X(N_f)=1.",
            "required_condition": "X(N_i)=0 and X(N_f)->infinity, or a declared finite-budget fraction",
            "failure_mode": "finite terminal X gives only B_mem*(1-exp[-(X_f/X_star)^p])",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "T820_3_onset_regularity",
            "question": "Can the source diverge at activation?",
            "result": "regularity_requires_rp_ge_1",
            "derivation": "If X~C*(N-N_i)^r with r>0, then S_Gamma~B_mem*p*r*(C/X_star)^p*(N-N_i)^(r*p-1).",
            "required_condition": "integrable for r*p>0; finite at onset only if r*p>=1; zero onset only if r*p>1",
            "failure_mode": "0<r*p<1 gives an integrable but divergent activation spike",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "T820_4_shape_identifiability",
            "question": "Does p_source determine the source history by itself?",
            "result": "fails_without_parent_X",
            "derivation": "The N-profile is multiplied by dX/dN; therefore p_source fixes only the density with respect to X, not with respect to N.",
            "required_condition": "derive or predeclare X(N) independently of target cosmology residuals",
            "failure_mode": "a free monotone X(N) can reshape the source in N almost arbitrarily",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "T820_5_arbitrary_fit_inversion",
            "question": "Can the closure encode any desired monotone memory history if X(N) is free?",
            "result": "hard_fail_for_claims",
            "derivation": "For any desired monotone F_fit(N) in [0,1), choose X(N)=X_star*(-ln(1-F_fit(N)))^(1/p). Then F_X(N)=F_fit(N).",
            "required_condition": "X(N) must be parent-derived or predeclared before data; otherwise this is a universal monotone-history parametrizer",
            "failure_mode": "target-data leakage and fit-renaming",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def endpoint_law_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "law_id": "E820_0_total_budget",
            "statement": "Delta_Gamma = integral_{N_i}^{N_f} S_Gamma dN = B_mem*(F_f-F_i).",
            "status": "exact_if_absolute_continuity_holds",
            "implication": "amplitude budget cannot be interpreted without endpoint values",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "E820_1_full_activation",
            "statement": "Full activation Delta_Gamma=B_mem requires X_i=0 and X_f->infinity.",
            "status": "conditional",
            "implication": "finite X_f leaves unactivated memory fraction exp[-(X_f/X_star)^p]",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "E820_2_finite_endpoint",
            "statement": "If X_i=0 and X_f=X_star, then Delta_Gamma=B_mem*(1-exp[-1])~0.632 B_mem.",
            "status": "counterexample_anchor",
            "implication": "normalization to B_mem is false unless endpoints are locked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "E820_3_onset_power_law",
            "statement": "For X~C tau^r near activation, S_Gamma~tau^(r*p-1).",
            "status": "regularity_gate",
            "implication": "finite source onset requires r*p>=1",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "E820_4_X_density_peak",
            "statement": "The density dF/dX peaks at (X/X_star)^p=(p-1)/p only for p>1; p=1 peaks at X=0; 0<p<1 is singular at X=0.",
            "status": "shape_warning",
            "implication": "a smooth source onset prefers p>1 or an X onset with r*p>=1, but the N-peak still depends on dX/dN",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def counterexample_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "counterexample_id": "CE820_0_nonmonotone_X",
            "construction": "Choose X(N)=1+0.1*sin(N) on an interval where cos(N)<0.",
            "breaks": "positivity",
            "lesson": "X>=0 is not enough; dX/dN sign must be controlled.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "CE820_1_finite_terminal_X",
            "construction": "Choose X(N_i)=0 and X(N_f)=X_star.",
            "breaks": "full_budget_normalization",
            "lesson": "integral is only 1-exp[-1] of B_mem, not B_mem.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "CE820_2_activation_spike",
            "construction": "Choose p=1/2 and X~C*(N-N_i).",
            "breaks": "finite_onset_regularness",
            "lesson": "source is integrable but diverges like (N-N_i)^(-1/2).",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "CE820_3_arbitrary_monotone_fit",
            "construction": "Given any monotone target F_fit(N), set X=X_star*(-ln(1-F_fit))^(1/p).",
            "breaks": "independent_predictivity",
            "lesson": "without parent X, C2A can become a dressed fit function.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def survival_condition_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "condition_id": "SC820_0_parent_X",
            "requirement": "Define X(N) from parent/coarse-grained invariants before target-data comparison.",
            "reason": "blocks arbitrary monotone-history inversion",
            "status": "missing",
            "next_action": "hunt candidate X from Gamma_mem, flow, curvature, matter, or coarse-graining variables",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition_id": "SC820_1_sign",
            "requirement": "Prove X>=0 and dX/dN>=0, or explicitly choose a signed-source branch.",
            "reason": "needed for nonnegative memory activation",
            "status": "missing",
            "next_action": "derive monotonicity or demote to signed stress closure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition_id": "SC820_2_endpoints",
            "requirement": "State and prove X_i=0 and X_f->infinity, or carry the finite activation fraction.",
            "reason": "needed for honest B_mem interpretation",
            "status": "missing",
            "next_action": "treat B_mem as total budget only after endpoint law is signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition_id": "SC820_3_regular_onset",
            "requirement": "If X~C tau^r, require r*p>=1 for finite onset source.",
            "reason": "avoids an unphysical activation spike unless explicitly allowed",
            "status": "new_gate",
            "next_action": "derive onset power r from candidate X dynamics",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition_id": "SC820_4_shape",
            "requirement": "Derive or predeclare p_source independent of SN/BAO/CMB/growth data.",
            "reason": "prevents reusing C1 fit clues as derivation",
            "status": "missing",
            "next_action": "source p_source from threshold geometry or keep it stress-only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "condition_id": "SC820_5_perturbations",
            "requirement": "Specify c_s^2, pi_Gamma, Q_m^nu, early limit, and growth sign response.",
            "reason": "background source law alone cannot support growth/CMB claims",
            "status": "missing",
            "next_action": "defer until parent X is chosen",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D820_0",
            "decision": "C2A_TS1 survives as a conditional algebraic closure only",
            "reason": "exact derivative and normalization identities hold, but only with unsourced sign, endpoint, and parent-X conditions",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D820_1",
            "decision": "parent-lock X(N) before any data or support claim",
            "reason": "free X(N) can reproduce any monotone F_fit(N), so independent predictivity is otherwise zero",
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
            "objective": "hunt a parent-derived or predeclared control scalar X(N) and test monotonicity/endpoints before data",
            "allowed_work": "source audit, symbolic candidate ranking, sign/endpoints/units proof",
            "forbidden_work": "SN/BAO/CMB/growth fitting or evidence claim",
            "priority": "high",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "axiom_id": AXIOM_ID,
            "claim_ceiling": CLAIM_CEILING,
            "verdict": "algebra useful but not predictive until X(N) is parent-locked",
            "sharpest_failure": "free X(N) can encode any monotone target F_fit(N)",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    stress_rows: list[dict[str, object]],
    endpoint_rows: list[dict[str, object]],
    counterexamples: list[dict[str, object]],
    survival_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V820_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )
    clean_819, clean_819_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_819_VALIDATION.csv")
    add("V820_1_prior_819_clean", clean_819, clean_819_detail)
    add(
        "V820_2_exact_derivative_test_present",
        any(row["test_id"] == "T820_0_exact_derivative" and row["result"] == "survives_conditionally" for row in stress_rows),
        "exact derivative identity tested",
    )
    add(
        "V820_3_arbitrary_fit_inversion_flagged",
        any(row["test_id"] == "T820_5_arbitrary_fit_inversion" and row["result"] == "hard_fail_for_claims" for row in stress_rows),
        "free X(N) arbitrary-fit inversion flagged",
    )
    add(
        "V820_4_endpoint_laws_present",
        {"E820_0_total_budget", "E820_1_full_activation", "E820_3_onset_power_law"}.issubset({row["law_id"] for row in endpoint_rows}),
        "budget, full activation, and onset laws present",
    )
    add(
        "V820_5_counterexamples_present",
        {"CE820_0_nonmonotone_X", "CE820_1_finite_terminal_X", "CE820_2_activation_spike", "CE820_3_arbitrary_monotone_fit"}.issubset({row["counterexample_id"] for row in counterexamples}),
        "counterexamples cover sign, endpoint, regularity, and predictivity",
    )
    add(
        "V820_6_survival_conditions_complete",
        {"SC820_0_parent_X", "SC820_1_sign", "SC820_2_endpoints", "SC820_3_regular_onset", "SC820_4_shape", "SC820_5_perturbations"}.issubset({row["condition_id"] for row in survival_rows}),
        "survival conditions complete",
    )
    add(
        "V820_7_decision_nonrunnable",
        all(row["runnable"] == "false" for row in decisions),
        "C2A remains non-runnable",
    )
    add(
        "V820_8_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )
    all_rows = source_rows + stress_rows + endpoint_rows + counterexamples + survival_rows + decisions + next_rows + summary
    add(
        "V820_9_all_rows_nonclaim",
        all(row.get("valid_for_claim") == "false" for row in all_rows),
        "all generated rows valid_for_claim=false",
    )
    changed = formalization_workbench_modified_count()
    add(
        "V820_10_formalization_workbench_untouched",
        changed == 0,
        f"formalization_changed_after_cutoff={changed}",
    )
    add("V820_11_validation_rows_ready", True, "validation table constructed")
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
    stress_rows: list[dict[str, object]],
    endpoint_rows: list[dict[str, object]],
    counterexamples: list[dict[str, object]],
    survival_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 820 - Y5 R10 C2A Source-Axiom Algebraic Stress Test",
            (
                "Current result: **C2A_TS1 survives as useful algebra but fails as a claimable/predictive branch until X(N) is parent-locked**. "
                "The exact derivative and budget identities are real. The killer caveat is also real: if X(N) is free, the closure can reproduce any monotone target history."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Nonclaim Summary\n\n" + markdown_table(summary, ["status", "axiom_id", "claim_ceiling", "verdict", "sharpest_failure", "next_target", "valid_for_claim"]),
            "## Stress Tests\n\n" + markdown_table(stress_rows, ["test_id", "question", "result", "derivation", "required_condition", "failure_mode", "valid_for_claim"]),
            "## Endpoint And Regularity Laws\n\n" + markdown_table(endpoint_rows, ["law_id", "statement", "status", "implication", "valid_for_claim"]),
            "## Counterexamples\n\n" + markdown_table(counterexamples, ["counterexample_id", "construction", "breaks", "lesson", "valid_for_claim"]),
            "## Survival Conditions\n\n" + markdown_table(survival_rows, ["condition_id", "requirement", "reason", "status", "next_action", "valid_for_claim"]),
            "## Decision\n\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim"]),
            "## Next Target\n\n" + markdown_table(next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "valid_for_claim"]),
            "## Source Register\n\n" + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "This is a good sharpening, not a loss. We now know exactly where the theory has to become real: the control scalar X(N). Without that, C2A is too flexible. With a parent-derived X and signed endpoints, the same algebra becomes a disciplined branch rather than a fitted costume.",
        ]
    )


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")

    source_rows = source_register_rows(generated_utc)
    stress_rows = stress_test_rows(generated_utc)
    endpoint_rows = endpoint_law_rows(generated_utc)
    counterexamples = counterexample_rows(generated_utc)
    survival_rows = survival_condition_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, stress_rows, endpoint_rows, counterexamples, survival_rows, decisions, next_rows, summary)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(STRESS_TESTS_PATH, stress_rows, ["test_id", "question", "result", "derivation", "required_condition", "failure_mode", "valid_for_claim", "generated_utc"])
    write_csv(ENDPOINT_LAWS_PATH, endpoint_rows, ["law_id", "statement", "status", "implication", "valid_for_claim", "generated_utc"])
    write_csv(COUNTEREXAMPLES_PATH, counterexamples, ["counterexample_id", "construction", "breaks", "lesson", "valid_for_claim", "generated_utc"])
    write_csv(SURVIVAL_CONDITIONS_PATH, survival_rows, ["condition_id", "requirement", "reason", "status", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "priority", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "axiom_id", "claim_ceiling", "verdict", "sharpest_failure", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(generated_utc, source_rows, stress_rows, endpoint_rows, counterexamples, survival_rows, decisions, next_rows, summary, validation),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"820 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
