from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "819-Y5-R10-C2A-minimal-source-axiom-candidate-manifest.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_819_SOURCE_REGISTER.csv"
MANIFEST_PATH = RESIDUALS / "P8_Y5_R10_819_AXIOM_CANDIDATE_MANIFEST.csv"
ALGEBRA_PATH = RESIDUALS / "P8_Y5_R10_819_ALGEBRAIC_CHECKS.csv"
INPUT_LOCKS_PATH = RESIDUALS / "P8_Y5_R10_819_INPUT_LOCKS.csv"
FIREWALL_PATH = RESIDUALS / "P8_Y5_R10_819_FIREWALL.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_819_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_819_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_819_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_819_VALIDATION.csv"

NEXT_TARGET = "820-Y5-R10-C2A-source-axiom-algebraic-stress-test.md"
AXIOM_ID = "C2A_TS1_threshold_survival_source_closure"
CLAIM_CEILING = "Level_2_effective_closure_candidate_only_no_parent_derivation_no_data_run"

GENERATED_FILES = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    MANIFEST_PATH,
    ALGEBRA_PATH,
    INPUT_LOCKS_PATH,
    FIREWALL_PATH,
    DECISION_PATH,
    NEXT_TARGET_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "818_doc",
        "path": POST_CHECKPOINT / "818-Y5-R10-C2-source-law-minimal-axiom-or-demotion-gate.md",
        "needles": [
            "C2 is demoted as a parent-derived branch",
            "C2A minimal source axiom is allowed as labelled closure grammar",
            "819-Y5-R10-C2A-minimal-source-axiom-candidate-manifest.md",
        ],
        "role": "immediate gate selecting this manifest target",
    },
    {
        "source_id": "818_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_818_VALIDATION.csv",
        "needles": [
            "V818_5_C2A_closure_allowed,pass",
            "V818_6_parent_claim_forbidden,pass",
            "V818_8_no_data_run_selected,pass",
            "V818_9_next_target_selected,pass,819-Y5-R10-C2A-minimal-source-axiom-candidate-manifest.md",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "818_manifest_requirements",
        "path": RESIDUALS / "P8_Y5_R10_818_AXIOM_MANIFEST_REQUIREMENTS.csv",
        "needles": [
            "S_Gamma_expression",
            "I_parent_inputs",
            "normalization_proof",
            "perturbation_policy",
        ],
        "role": "required fields for a source-axiom manifest",
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


def manifest_rows(generated_utc: str) -> list[dict[str, object]]:
    expression = (
        "Let X(N)>=0 be a parent/coarse-grained monotone control scalar. "
        "F_X(N)=1-exp[-(X(N)/X_star)^p_source]. "
        "S_Gamma(N;I_parent)=B_mem*dF_X/dN "
        "=B_mem*p_source*(X/X_star)^(p_source-1)*(dX/dN)/X_star*exp[-(X/X_star)^p_source]."
    )
    return [
        {
            "axiom_id": AXIOM_ID,
            "manifest_field": "S_Gamma_expression",
            "entry": expression,
            "status": "explicit_symbolic_closure_candidate",
            "blocking_gap": "X(N), X_star, p_source, B_mem, and perturbations are not parent-derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "axiom_id": AXIOM_ID,
            "manifest_field": "I_parent_inputs",
            "entry": "I_parent={X(N), dX/dN, X_star, p_source, B_mem, background branch, perturbation branch}",
            "status": "listed_but_not_sourced",
            "blocking_gap": "must map X to parent invariants and source paths before any run",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "axiom_id": AXIOM_ID,
            "manifest_field": "normalization_proof",
            "entry": "If p_source>0, X_star>0, X is nondecreasing, X(N_i)=0, and X(N_f)->infinity, then integral dF_X = 1 and integral S_Gamma dN = B_mem.",
            "status": "conditional_algebraic_identity",
            "blocking_gap": "endpoint and monotonicity conditions are not yet derived from the parent branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "axiom_id": AXIOM_ID,
            "manifest_field": "shape_parameters",
            "entry": "p_source remains a symbolic closure-shape exponent; it is not assigned from the old C1 fit or tuned to SN/BAO residuals.",
            "status": "locked_against_fit_smuggling",
            "blocking_gap": "derive p_source from parent threshold geometry or demote to stress parameter",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "axiom_id": AXIOM_ID,
            "manifest_field": "amplitude_policy",
            "entry": "B_mem is a total source budget, not evidence; it must be derived, bounded, or explicitly labelled phenomenological before any comparator.",
            "status": "amplitude_not_claimable",
            "blocking_gap": "no parent amplitude lock",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "axiom_id": AXIOM_ID,
            "manifest_field": "perturbation_policy",
            "entry": "No growth/CMB interpretation until c_s^2, pi_Gamma, Q_m^nu, early-time behaviour, and growth-sign response are specified.",
            "status": "perturbations_block_data_use",
            "blocking_gap": "background-only source law is insufficient",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def algebra_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "check_id": "A819_0_explicit_source",
            "condition": "S_Gamma is written as B_mem*dF_X/dN with a visible formula for F_X.",
            "result": "pass_symbolic",
            "blocker": "symbolic is not parent-derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "check_id": "A819_1_positivity",
            "condition": "S_Gamma>=0 follows only if B_mem>=0, p_source>0, X_star>0, X>=0, and dX/dN>=0.",
            "result": "conditional",
            "blocker": "must derive or bound dX/dN sign",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "check_id": "A819_2_normalization",
            "condition": "Integral S_Gamma dN = B_mem[F_X(N_f)-F_X(N_i)]. Full budget requires F_X(N_i)=0 and F_X(N_f)=1.",
            "result": "conditional",
            "blocker": "endpoint behaviour of X is not signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "check_id": "A819_3_units",
            "condition": "If N is dimensionless, S_Gamma has units of B_mem per e-fold; X/X_star must be dimensionless.",
            "result": "pass_if_X_star_matches_X",
            "blocker": "units of X must be fixed by parent invariant definition",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "check_id": "A819_4_no_fit_reuse",
            "condition": "Old C1 values such as nu_act=7/4 or F_eq=3/5 are not inserted.",
            "result": "pass",
            "blocker": "p_source remains symbolic until derived or separately stress-labelled",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def input_lock_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "lock_id": "L819_X_control",
            "required_input": "definition of X(N) from parent/coarse-grained invariants",
            "current_status": "missing_parent_map",
            "why_it_matters": "the source cannot be more than closure grammar without a real control scalar",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "L819_X_monotonicity",
            "required_input": "proof or bound for X>=0 and dX/dN>=0 over the intended branch",
            "current_status": "missing_sign_proof",
            "why_it_matters": "positivity and normalization fail without it",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "L819_shape",
            "required_input": "derive or predeclare p_source without target-data tuning",
            "current_status": "symbolic_only",
            "why_it_matters": "prevents old C1 fit-smuggling",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "L819_amplitude",
            "required_input": "derive, bound, or quarantine B_mem",
            "current_status": "missing_parent_budget",
            "why_it_matters": "background distances are too easy to fit with a free amplitude",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "L819_perturbations",
            "required_input": "c_s^2, pi_Gamma, Q_m^nu, early-limit, and growth response",
            "current_status": "missing_perturbation_contract",
            "why_it_matters": "no CMB/growth statement is interpretable without this",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "L819_local_firewall",
            "required_input": "proof that this cosmology source does not leak into local PPN/local-GR claims",
            "current_status": "local_firewall_required",
            "why_it_matters": "cosmology closure must not smuggle a local-GR pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def firewall_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "firewall_id": "FW819_no_data_run",
            "statement": "Do not run SN/BAO/CMB/growth fitting from this manifest.",
            "reason": "manifest is algebraic closure grammar only",
            "status": "active_block",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "firewall_id": "FW819_no_parent_claim",
            "statement": "Do not call C2A parent-derived.",
            "reason": "X, p_source, and B_mem are not derived from the parent action/equations",
            "status": "active_block",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "firewall_id": "FW819_no_local_GR_upgrade",
            "statement": "Do not upgrade R10, PPN, clocks, or local-GR status from this cosmology source law.",
            "reason": "local projection and coupling suppression remain separate gates",
            "status": "active_block",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D819_0",
            "decision": "accept C2A_TS1 as an explicit candidate closure manifest, not as evidence",
            "reason": "the threshold-survival form gives a normalized source law if its sign and endpoint hypotheses hold",
            "runnable": "false",
            "claim_ceiling": CLAIM_CEILING,
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D819_1",
            "decision": "stress-test the algebra before any data work",
            "reason": "the next useful move is to try to break positivity, normalization, endpoint, and units assumptions",
            "runnable": "false",
            "claim_ceiling": CLAIM_CEILING,
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "prove or break the C2A_TS1 algebraic conditions before any data comparator",
            "priority": "high",
            "allowed_work": "symbolic stress test, unit audit, endpoint and monotonicity gates",
            "forbidden_work": "SN/BAO/CMB/growth fitting or support claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": "Y5_R10_819_C2A_candidate_manifest_written_nonclaim",
            "axiom_id": AXIOM_ID,
            "claim_ceiling": CLAIM_CEILING,
            "what_is_new": "explicit threshold-survival source law template with normalization conditions",
            "what_is_missing": "parent map for X, sign proof, p_source derivation, B_mem budget, perturbation closure, local firewall",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in [
        SOURCE_REGISTER_PATH,
        MANIFEST_PATH,
        ALGEBRA_PATH,
        INPUT_LOCKS_PATH,
        FIREWALL_PATH,
        DECISION_PATH,
        NEXT_TARGET_PATH,
        NONCLAIM_SUMMARY_PATH,
    ]:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows.extend(csv.DictReader(handle))
    return rows


def validation_rows(
    source_rows: list[dict[str, object]],
    manifest: list[dict[str, object]],
    algebra: list[dict[str, object]],
    locks: list[dict[str, object]],
    firewall: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V819_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )
    clean_818, clean_818_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_818_VALIDATION.csv")
    add("V819_1_prior_818_clean", clean_818, clean_818_detail)
    expression_rows = [row for row in manifest if row["manifest_field"] == "S_Gamma_expression"]
    add(
        "V819_2_explicit_expression_present",
        bool(expression_rows) and "S_Gamma(N;I_parent)" in expression_rows[0]["entry"] and "dF_X/dN" in expression_rows[0]["entry"],
        "manifest writes S_Gamma explicitly",
    )
    required_fields = {
        "S_Gamma_expression",
        "I_parent_inputs",
        "normalization_proof",
        "shape_parameters",
        "amplitude_policy",
        "perturbation_policy",
    }
    add(
        "V819_3_manifest_fields_complete",
        required_fields.issubset({row["manifest_field"] for row in manifest}),
        "required manifest fields present",
    )
    add(
        "V819_4_algebra_blocks_data",
        any(row["check_id"] == "A819_2_normalization" and row["result"] == "conditional" for row in algebra),
        "normalization remains conditional, so no data run",
    )
    required_locks = {"L819_X_control", "L819_X_monotonicity", "L819_shape", "L819_amplitude", "L819_perturbations", "L819_local_firewall"}
    add(
        "V819_5_input_locks_complete",
        required_locks.issubset({row["lock_id"] for row in locks}),
        "all source-law locks listed",
    )
    add(
        "V819_6_firewalls_active",
        all(row["status"] == "active_block" for row in firewall) and len(firewall) >= 3,
        "data, parent-claim, and local-GR firewalls active",
    )
    add(
        "V819_7_decision_nonrunnable",
        all(row["runnable"] == "false" for row in decisions),
        "candidate accepted only as non-runnable closure manifest",
    )
    add(
        "V819_8_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )
    add(
        "V819_9_all_rows_nonclaim",
        all(row.get("valid_for_claim") == "false" for row in source_rows + manifest + algebra + locks + firewall + decisions + next_rows),
        "all generated rows valid_for_claim=false",
    )
    changed = formalization_workbench_modified_count()
    add(
        "V819_10_formalization_workbench_untouched",
        changed == 0,
        f"formalization_changed_after_cutoff={changed}",
    )
    add("V819_11_validation_rows_ready", True, "validation table constructed")
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
    manifest: list[dict[str, object]],
    algebra: list[dict[str, object]],
    locks: list[dict[str, object]],
    firewall: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 819 - Y5 R10 C2A Minimal Source-Axiom Candidate Manifest",
            (
                "Current result: **C2A now has one explicit candidate source-law manifest, but it is still non-runnable and non-claim**. "
                "The useful move is that the source is no longer hidden prose: it is a threshold-survival law with visible normalization, sign, unit, amplitude, perturbation, and local-firewall obligations."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Nonclaim Summary\n\n" + markdown_table(summary, ["status", "axiom_id", "claim_ceiling", "what_is_new", "what_is_missing", "valid_for_claim"]),
            "## Candidate Manifest\n\n" + markdown_table(manifest, ["manifest_field", "entry", "status", "blocking_gap", "valid_for_claim"]),
            "## Algebraic Checks\n\n" + markdown_table(algebra, ["check_id", "condition", "result", "blocker", "valid_for_claim"]),
            "## Input Locks\n\n" + markdown_table(locks, ["lock_id", "required_input", "current_status", "why_it_matters", "valid_for_claim"]),
            "## Firewalls\n\n" + markdown_table(firewall, ["firewall_id", "statement", "reason", "status", "valid_for_claim"]),
            "## Decision\n\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "runnable", "claim_ceiling", "next_target", "valid_for_claim"]),
            "## Next Target\n\n" + markdown_table(next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "valid_for_claim"]),
            "## Source Register\n\n" + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "This keeps the route alive without cheating. The C2A threshold-survival law is a clean thing to attack next: if the monotonic control scalar, endpoint behaviour, source exponent, amplitude budget, perturbation closure, or local firewall cannot be signed, it stays closure-only or gets demoted.",
        ]
    )


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")

    source_rows = source_register_rows(generated_utc)
    manifest = manifest_rows(generated_utc)
    algebra = algebra_rows(generated_utc)
    locks = input_lock_rows(generated_utc)
    firewall = firewall_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, manifest, algebra, locks, firewall, decisions, next_rows)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(MANIFEST_PATH, manifest, ["axiom_id", "manifest_field", "entry", "status", "blocking_gap", "valid_for_claim", "generated_utc"])
    write_csv(ALGEBRA_PATH, algebra, ["check_id", "condition", "result", "blocker", "valid_for_claim", "generated_utc"])
    write_csv(INPUT_LOCKS_PATH, locks, ["lock_id", "required_input", "current_status", "why_it_matters", "valid_for_claim", "generated_utc"])
    write_csv(FIREWALL_PATH, firewall, ["firewall_id", "statement", "reason", "status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "runnable", "claim_ceiling", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "priority", "allowed_work", "forbidden_work", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "axiom_id", "claim_ceiling", "what_is_new", "what_is_missing", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(generated_utc, source_rows, manifest, algebra, locks, firewall, decisions, next_rows, summary, validation),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"819 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
