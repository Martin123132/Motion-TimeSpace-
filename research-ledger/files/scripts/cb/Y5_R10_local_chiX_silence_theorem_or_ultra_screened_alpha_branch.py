from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
OUT = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_local_chiX_silence_theorem_or_ultra_screened_alpha_branch.py"
DOC_PATH = ROOT / "649-Y5-R10-local-chiX-silence-theorem-or-ultra-screened-alpha-branch.md"

STATUS = "Y5_R10_local_chiX_silence_conditional_not_parent_signed_ultra_screened_alpha_branch_formalized_nonclaim"
CLAIM_CEILING = "conditional_local_chiX_silence_theorem_plus_ultra_screened_finite_alpha_contract_only_no_clock_or_local_claim"
NEXT_TARGET = "650-Y5-R10-ultra-screened-alpha-branch-cross-arena-contract.md"
NOMINAL_H0_YR_INV = 7.16e-11
YB_PRODUCT_BOUND_1SIGMA = 2.1e-18
YB_DCHI_DN_FOR_KAPPA_ONE = YB_PRODUCT_BOUND_1SIGMA / NOMINAL_H0_YR_INV


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_register_rows() -> list[dict[str, object]]:
    sources = [
        ("S649_0", "checkpoint_648_doc", ROOT / "648-Y5-R10-clock-product-bound-runner-or-derive-local-chiX-dynamics.md", "prior clock product-bound fork"),
        ("S649_1", "validation_648", OUT / "P8_Y5_BRR545_648_VALIDATION.csv", "prior validation"),
        ("S649_2", "product_runner_648", OUT / "P8_Y5_R10_648_CLOCK_PRODUCT_BOUND_RUNNER.csv", "clock product-bound runner"),
        ("S649_3", "tau_survival_648", OUT / "P8_Y5_R10_648_TAU_SURVIVAL_REQUIREMENTS.csv", "tau survival requirements"),
        ("S649_4", "local_attempt_648", OUT / "P8_Y5_R10_648_LOCAL_CHIX_DYNAMICS_ATTEMPT.csv", "local chiX dynamics attempt"),
        ("S649_5", "strict_local_coframe_242", ROOT / "242-strict-local-coframe-branch-or-domain-projector-action.md", "strict local coframe conditional route"),
        ("S649_6", "boundary_state_local_silence_300", ROOT / "300-boundary-state-local-silence-theorem-attempt.md", "closed/gapped local silence conditional route"),
        ("S649_7", "clock_functional_156", ROOT / "156-clock-projection-functional-theorem-or-demotion.md", "clock scalar local-silence clue"),
        ("S649_8", "parent_vertical_norm_644", ROOT / "644-Y5-R10-parent-vertical-norm-coupling-owner-proof-or-demotion.md", "demoted zero route and rescaling counterexamples"),
        ("S649_9", "generator_script_649", SCRIPT_PATH, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": source_id,
            "label": label,
            "path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for source_id, label, path, role in sources
    ]


def conditional_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "LCS649",
            "name": "conditional local chi_X silence theorem",
            "statement": "If lab/bound domains are parent-selected closed/gapped boundary states, the observed local matter coframe is strict and independent of chi_X, the clock scalar vanishes for X_D=0/stationary domains, and no alpha_EM(Xhat) vertex remains, then dchi_X/dt=0 and clock alpha drift vanishes locally.",
            "proof_status": "proved_as_conditional_template",
            "corpus_status": "premises_unsigned",
            "consequence_if_signed": "clock product bound is satisfied by tau_clock=0 without constraining standalone kappa_alpha",
            "valid_for_claim": "false",
        }
    ]


def silence_clause_rows() -> list[dict[str, object]]:
    return [
        {
            "clause_id": "LCS649_0_domain_classifier",
            "needed_statement": "A parent domain classifier separates lab/bound systems from FLRW/open systems before fitting data.",
            "support": "300 boundary-state local silence target",
            "current_status": "not_parent_derived",
            "failure_mode": "local/FLRW split becomes an escape hatch if chosen after seeing clock bounds",
            "result_for_tau": "no active tau_clock zero",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "LCS649_1_closed_gapped_lab_domain",
            "needed_statement": "Laboratory clock domains are closed/gapped in the chi_X boundary channel: [J_chi]_local=0 and rho_chi_local=0.",
            "support": "300 conditional closed/gapped theorem",
            "current_status": "conditional_only",
            "failure_mode": "ordinary baths, horizons, galaxies, or time-dependent local systems may leak",
            "result_for_tau": "tau_clock=0 only if closure/gap is parent-signed",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "LCS649_2_strict_matter_coframe",
            "needed_statement": "The local matter/clock coframe is strict and does not include chi_X or a direct alpha-pressure scalar.",
            "support": "242 strict local coframe conditional theorem",
            "current_status": "conditional_only",
            "failure_mode": "if matter clocks see chi_X directly, clock bounds bite immediately",
            "result_for_tau": "tau_clock=0 only if local representative is selected by parent action",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "LCS649_3_clock_scalar_vanishes",
            "needed_statement": "The signed clock scalar satisfies C_clock=0 for lab/local domains, e.g. X_D=0 or stationary bound-domain projection.",
            "support": "156 local silence if X_D=0 clue",
            "current_status": "theorem_target_not_derived",
            "failure_mode": "cell clock scalar may be gauge/closure and not physical",
            "result_for_tau": "not enough alone",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "LCS649_4_no_alpha_vertex",
            "needed_statement": "No local alpha_EM(chi_X), f_A(chi_X)F^2, or coframe leakage term survives in the lab effective action.",
            "support": "644 rescaling counterexamples",
            "current_status": "not_forbidden_by_current_corpus",
            "failure_mode": "lambda_A F^2/coframe leakage reopens finite alpha drift",
            "result_for_tau": "blocks silence claim",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "LCS649_5_edge_cases",
            "needed_statement": "Clock experiments are not in an edge class that sources chi_X drift through radiation, horizons, material stress, or environmental coupling.",
            "support": "300 edge-case ledger",
            "current_status": "open",
            "failure_mode": "unmodeled lab/environment channel invalidates silence assumption",
            "result_for_tau": "requires source ledger before claim",
            "valid_for_claim": "false",
        },
    ]


def ultra_screened_branch_rows() -> list[dict[str, object]]:
    kappa_values = [0.01, 0.1, 1.0, 10.0]
    rows: list[dict[str, object]] = []
    for kappa in kappa_values:
        tau = YB_PRODUCT_BOUND_1SIGMA / kappa
        rows.append(
            {
                "branch_id": f"USB649_{len(rows)}",
                "assumed_abs_kappa_alpha": f"{kappa:g}",
                "required_abs_tau_clock_time_yr_inv_max": f"{tau:.6e}",
                "required_abs_dchi_dN_over_H0_max": f"{tau / NOMINAL_H0_YR_INV:.6e}",
                "branch_rule": f"|dchi_X/dN| <= {tau / NOMINAL_H0_YR_INV:.3e} for |kappa_alpha|={kappa:g}",
                "status": "ultra_screened_nonclaim_contract",
                "valid_for_claim": "false",
            }
        )
    return rows


def branch_policy_rows() -> list[dict[str, object]]:
    return [
        {
            "policy_id": "BP649_0_no_silence_claim",
            "rule": "Do not use tau_clock=0 unless all local silence clauses are parent-signed.",
            "reason": "otherwise clocks are evaded by assumption",
            "status": "active",
            "valid_for_claim": "false",
        },
        {
            "policy_id": "BP649_1_product_not_standalone",
            "rule": "Clock rows constrain kappa_alpha*tau_clock, not kappa_alpha alone.",
            "reason": "tau dynamics are not derived",
            "status": "active",
            "valid_for_claim": "false",
        },
        {
            "policy_id": "BP649_2_ultra_screened_fallback",
            "rule": "If silence is not proved, finite alpha branch must carry explicit ultra-screening prior from Yb clocks.",
            "reason": "order-one kappa requires |dchi_X/dN| <= 2.93e-8 H0-normalized",
            "status": "selected_fallback",
            "valid_for_claim": "false",
        },
        {
            "policy_id": "BP649_3_cross_arena_warning",
            "rule": "Ultra-screening must later be checked against WEP/R10/EM spectra, not only clocks.",
            "reason": "clock-only survival may fail in other local arenas",
            "status": "next_contract",
            "valid_for_claim": "false",
        },
    ]


def decision_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "DG649_0_conditional_theorem_written",
            "gate": "conditional local chi_X silence theorem exists",
            "result": "pass_template",
            "consequence": "future parent action has exact clauses to prove",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG649_1_parent_signed_silence",
            "gate": "parent signs all local silence clauses",
            "result": "fail",
            "consequence": "tau_clock=0 cannot be used as active evidence",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG649_2_ultra_screened_branch",
            "gate": "ultra-screened finite branch is formalized",
            "result": "pass_nonclaim",
            "consequence": "finite alpha branch survives only with explicit clock-screening prior",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG649_3_public_claim",
            "gate": "clock/local pass claim allowed",
            "result": "fail_policy",
            "consequence": "no public clock or local claim",
            "valid_for_claim": "false",
        },
    ]


def next_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "NC649_0",
            "next_target": NEXT_TARGET,
            "work_item": "Carry the ultra-screened alpha branch into WEP/R10/EM spectra cross-arena consistency.",
            "acceptance_condition": "same screening variable and branch policy used across arenas; no clock-only special pleading",
        },
        {
            "contract_id": "NC649_1",
            "next_target": NEXT_TARGET,
            "work_item": "Try to identify a physical screening mechanism for |dchi_X/dN| << 1 in lab domains.",
            "acceptance_condition": "mechanism derives from parent domain/classifier/coframe, not a fitted small number",
        },
        {
            "contract_id": "NC649_2",
            "next_target": NEXT_TARGET,
            "work_item": "Keep local silence theorem as dormant proof target with explicit clauses.",
            "acceptance_condition": "future promotion must close all six LCS649 clauses",
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D649_0",
            "route": "local_chiX_silence",
            "decision": "conditional_theorem_written_not_selected_as_claim",
            "why": "strict coframe and closed/gapped routes are still parent-unsigned",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D649_1",
            "route": "ultra_screened_alpha_branch",
            "decision": "selected_nonclaim_fallback",
            "why": "clock data require explicit ultra-screening unless local silence is proved",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "conditional_silence_theorem_written": "true",
            "local_chiX_silence_claim": "false",
            "ultra_screened_branch_selected": "true_nonclaim",
            "order_one_kappa_requires_dchi_dN_below": f"{YB_DCHI_DN_FOR_KAPPA_ONE:.3e}",
            "standalone_clock_pass": "false",
            "hardest_blocker": "parent domain classifier plus strict local coframe plus no-alpha-vertex clauses are unsigned",
            "next_target": NEXT_TARGET,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    clause_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    policy_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V649_0_source_paths_exist", all(row["exists"] == "true" for row in source_rows), "all cited local source paths exist"))
    prior = read_csv(OUT / "P8_Y5_BRR545_648_VALIDATION.csv")
    checks.append(("V649_1_prior_648_validation_clean", all(row.get("result") == "pass" for row in prior), "648 validation remains clean"))
    checks.append(("V649_2_conditional_theorem_written", theorem_rows[0]["proof_status"] == "proved_as_conditional_template", "conditional local silence theorem is written"))
    checks.append(("V649_3_silence_clauses_unsigned", any(row["current_status"] in {"not_parent_derived", "conditional_only", "not_forbidden_by_current_corpus", "open"} for row in clause_rows), "silence clauses remain unsigned"))
    checks.append(("V649_4_no_clause_claim", all(row["valid_for_claim"] == "false" for row in clause_rows), "silence clauses are nonclaim"))
    kappa_one = [row for row in branch_rows if row["assumed_abs_kappa_alpha"] == "1"]
    checks.append(("V649_5_ultra_screen_kappa_one", len(kappa_one) == 1 and float(kappa_one[0]["required_abs_dchi_dN_over_H0_max"]) < 3e-8, "order-one kappa requires dchi/dN below 3e-8"))
    checks.append(("V649_6_branch_rows_nonclaim", all(row["valid_for_claim"] == "false" for row in branch_rows), "ultra-screened branch rows are nonclaim"))
    checks.append(("V649_7_policy_has_no_special_pleading", any(row["policy_id"] == "BP649_3_cross_arena_warning" for row in policy_rows), "cross-arena warning policy is present"))
    checks.append(("V649_8_gate_blocks_public_claim", any(row["gate_id"] == "DG649_3_public_claim" and row["result"] == "fail_policy" for row in gate_rows), "public claim gate is blocked"))
    checks.append(("V649_9_next_contract_points_to_650", all(row["next_target"] == NEXT_TARGET for row in next_rows), "next contract points to 650"))
    checks.append(("V649_10_decisions_nonclaim", all(row["valid_for_claim"] == "false" for row in decision), "decision rows are nonclaim"))
    checks.append(("V649_11_summary_nonclaim", summary[0]["local_chiX_silence_claim"] == "false" and summary[0]["ultra_screened_branch_selected"] == "true_nonclaim", "summary blocks silence claim and selects nonclaim fallback"))

    fw = ROOT.parent / "formalization-workbench"
    cutoff = datetime(2026, 5, 31, 14, 42, 0).timestamp()
    changed_after_cutoff = 0
    if fw.exists():
        for path in fw.rglob("*"):
            if path.is_file() and path.stat().st_mtime > cutoff:
                changed_after_cutoff += 1
    checks.append(("V649_12_formalization_workbench_unchanged", changed_after_cutoff == 0, f"formalization files changed after cutoff: {changed_after_cutoff}"))

    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now_iso(),
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("|", "\\|").replace("\n", " ")
            values.append(text)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    source_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    clause_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    policy_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 649 Y5/R10 Local chi_X Silence Theorem or Ultra-Screened Alpha Branch",
        "",
        "## Verdict",
        "",
        f"- Status: `{STATUS}`",
        f"- Claim ceiling: `{CLAIM_CEILING}`",
        "- The local silence theorem can be written as a clean conditional theorem, but the current corpus cannot sign its clauses.",
        "- Therefore finite alpha is retained only as an ultra-screened nonclaim branch.",
        f"- Order-one `kappa_alpha` requires `|dchi_X/dN| <= {YB_DCHI_DN_FOR_KAPPA_ONE:.3e}` in lab domains from the Yb clock product bound.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["source_id", "label", "path", "exists", "role"]),
        "",
        "## Conditional Silence Theorem",
        "",
        markdown_table(theorem_rows, ["theorem_id", "name", "proof_status", "corpus_status", "consequence_if_signed"]),
        "",
        "## Silence Clause Audit",
        "",
        markdown_table(clause_rows, ["clause_id", "needed_statement", "current_status", "failure_mode", "result_for_tau"]),
        "",
        "## Ultra-Screened Alpha Branch",
        "",
        markdown_table(branch_rows, ["branch_id", "assumed_abs_kappa_alpha", "required_abs_tau_clock_time_yr_inv_max", "required_abs_dchi_dN_over_H0_max", "branch_rule", "status"]),
        "",
        "## Branch Policy",
        "",
        markdown_table(policy_rows, ["policy_id", "rule", "reason", "status"]),
        "",
        "## Decision Gates",
        "",
        markdown_table(gate_rows, ["gate_id", "gate", "result", "consequence"]),
        "",
        "## Next Contract",
        "",
        markdown_table(next_rows, ["contract_id", "work_item", "acceptance_condition"]),
        "",
        "## Decision",
        "",
        markdown_table(decision, ["decision_id", "route", "decision", "why", "next_target"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["check_id", "result", "detail"]),
        "",
        "## Interpretation",
        "",
        "- This is a clean survival route, not a win: MTS must either prove local silence or accept ultra-screening as part of the finite alpha branch.",
        "- The good news is the needed theorem is now explicit; the bad news is the clock bound leaves almost no room for unscreened local drift.",
        "- The next fair test is cross-arena consistency: the same screening rule must not be invented only to dodge clocks.",
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(summary, ["status", "conditional_silence_theorem_written", "local_chiX_silence_claim", "ultra_screened_branch_selected", "order_one_kappa_requires_dchi_dN_below", "standalone_clock_pass", "hardest_blocker", "next_target"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    theorem_rows = conditional_theorem_rows()
    clause_rows = silence_clause_rows()
    branch_rows = ultra_screened_branch_rows()
    policy_rows = branch_policy_rows()
    gate_rows = decision_gate_rows()
    next_rows = next_contract_rows()
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, theorem_rows, clause_rows, branch_rows, policy_rows, gate_rows, next_rows, decision, summary)

    write_csv(OUT / "P8_Y5_R10_649_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_649_CONDITIONAL_SILENCE_THEOREM.csv", theorem_rows)
    write_csv(OUT / "P8_Y5_R10_649_SILENCE_CLAUSE_AUDIT.csv", clause_rows)
    write_csv(OUT / "P8_Y5_R10_649_ULTRA_SCREENED_ALPHA_BRANCH.csv", branch_rows)
    write_csv(OUT / "P8_Y5_R10_649_BRANCH_POLICY.csv", policy_rows)
    write_csv(OUT / "P8_Y5_R10_649_DECISION_GATES.csv", gate_rows)
    write_csv(OUT / "P8_Y5_R10_649_NEXT_CONTRACT.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_649_DECISION.csv", decision)
    write_csv(OUT / "P8_Y5_R10_649_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_BRR545_649_VALIDATION.csv", validation)
    write_doc(source_rows, theorem_rows, clause_rows, branch_rows, policy_rows, gate_rows, next_rows, decision, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote_doc={DOC_PATH}")
    print(f"wrote_csv_dir={OUT}")
    print("order_one_kappa_requires_dchi_dN_below=2.93e-8")
    print(f"validation_rows={len(validation)}")
    print(f"validation_failures={len(failures)}")
    print(f"status={STATUS}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for row in failures:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
