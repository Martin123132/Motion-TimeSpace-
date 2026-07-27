from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
OUT = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_clock_product_bound_runner_or_derive_local_chiX_dynamics.py"
DOC_PATH = ROOT / "648-Y5-R10-clock-product-bound-runner-or-derive-local-chiX-dynamics.md"

STATUS = "Y5_R10_clock_product_bound_runner_quantifies_ultra_silence_requirement_local_chiX_dynamics_not_derived_nonclaim"
CLAIM_CEILING = "clock_product_bound_runner_and_local_silence_audit_only_no_standalone_kappa_alpha_score_no_clock_or_local_claim"
NEXT_TARGET = "649-Y5-R10-local-chiX-silence-theorem-or-ultra-screened-alpha-branch.md"
NOMINAL_H0_YR_INV = 7.16e-11


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
        ("S648_0", "checkpoint_647_doc", ROOT / "647-Y5-R10-derive-or-define-chiX-and-tau-clock-map.md", "prior product-bound checkpoint"),
        ("S648_1", "validation_647", OUT / "P8_Y5_BRR545_647_VALIDATION.csv", "prior validation"),
        ("S648_2", "clock_product_bound_647", OUT / "P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv", "clock product bounds"),
        ("S648_3", "H0_diagnostic_647", OUT / "P8_Y5_R10_647_H0_NORMALIZED_DIAGNOSTIC.csv", "H0-normalized product diagnostic"),
        ("S648_4", "tau_requirement_647", OUT / "P8_Y5_R10_647_TAU_REQUIREMENT_DIAGNOSTIC.csv", "tau requirements imported"),
        ("S648_5", "chiX_attempt_647", OUT / "P8_Y5_R10_647_CHIX_DEFINITION_ATTEMPT.csv", "chi_X definition attempt"),
        ("S648_6", "tau_map_647", OUT / "P8_Y5_R10_647_TAU_CLOCK_MAP.csv", "tau_clock map attempt"),
        ("S648_7", "strict_local_coframe_242", ROOT / "242-strict-local-coframe-branch-or-domain-projector-action.md", "strict local coframe conditional route"),
        ("S648_8", "boundary_state_local_silence_300", ROOT / "300-boundary-state-local-silence-theorem-attempt.md", "closed/gapped local silence conditional route"),
        ("S648_9", "clock_functional_156", ROOT / "156-clock-projection-functional-theorem-or-demotion.md", "clock scalar local-silence clue"),
        ("S648_10", "generator_script_648", SCRIPT_PATH, "this checkpoint generator"),
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


def local_chiX_dynamics_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "LCD648_0_strict_local_coframe",
            "route": "strict local matter coframe",
            "candidate_statement": "If the parent action selects a strict local matter coframe independent of the open alpha-pressure coordinate, then dchi_X/dt=0 for lab clocks.",
            "support_source": "242-strict-local-coframe-branch-or-domain-projector-action.md",
            "current_status": "conditional_only",
            "blocking_gap": "parent selection of the strict local representative is still missing",
            "tau_clock_result": "tau_clock_time=0 only if parent representative-selection theorem closes",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "LCD648_1_closed_gapped_boundary_state",
            "route": "closed/gapped local boundary-bath state",
            "candidate_statement": "If local bound domains are closed/gapped in the MTS boundary-bath channel, then the open sector is locally silent.",
            "support_source": "300-boundary-state-local-silence-theorem-attempt.md",
            "current_status": "conditional_only",
            "blocking_gap": "local/FLRW boundary-state split is not parent-derived and edge cases remain open",
            "tau_clock_result": "tau_clock_time=0 only if closed/gapped local split is proved",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "LCD648_2_cell_clock_scalar",
            "route": "cell-balanced clock scalar",
            "candidate_statement": "If chi_X is tied to the cell clock scalar, then lab silence would require X_D=0 or stationary local domain projection.",
            "support_source": "156-clock-projection-functional-theorem-or-demotion.md",
            "current_status": "theorem_target_not_derived",
            "blocking_gap": "Theta_clock and matter-clock coupling are not derived from a parent action and may be gauge/closure",
            "tau_clock_result": "not enough for lab alpha silence",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "LCD648_3_parent_vertical_norm",
            "route": "parent vertical norm alpha silence",
            "candidate_statement": "If alpha_EM is quotient-fixed by the vertical norm, then chi_X has no local alpha meaning and kappa_alpha=0.",
            "support_source": "644-Y5-R10-parent-vertical-norm-coupling-owner-proof-or-demotion.md",
            "current_status": "demoted_closure_contract",
            "blocking_gap": "independent lambda_A F_Q^2, generator rescaling, and coframe leakage are not forbidden",
            "tau_clock_result": "not active; zero route demoted",
            "valid_for_claim": "false",
        },
    ]


def product_bound_runner_rows() -> list[dict[str, object]]:
    product_rows = read_csv(OUT / "P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv")
    drift_fractions = [1.0, 1e-2, 1e-4, 1e-6, 1e-8, 0.0]
    rows: list[dict[str, object]] = []
    for bound in product_rows:
        one_sigma = float(bound["conservative_abs_product_bound_1sigma_yr_inv"])
        two_sigma = float(bound["conservative_abs_product_bound_2sigma_yr_inv"])
        for fraction in drift_fractions:
            if fraction == 0.0:
                kappa_1 = "unbounded_if_parent_silence_proved"
                kappa_2 = "unbounded_if_parent_silence_proved"
                verdict = "conditional_silence_branch_only"
            else:
                tau = NOMINAL_H0_YR_INV * fraction
                kappa_1 = f"{one_sigma / tau:.6g}"
                kappa_2 = f"{two_sigma / tau:.6g}"
                if one_sigma / tau < 1e-4:
                    verdict = "catastrophic_for_order_one_kappa"
                elif one_sigma / tau < 1e-1:
                    verdict = "order_one_kappa_excluded_if_drift_assumption_valid"
                else:
                    verdict = "order_one_kappa_possible_only_with_ultra_slow_drift"
            rows.append(
                {
                    "runner_id": f"PBR648_{len(rows):02d}",
                    "clock_pair_id": bound["clock_pair_id"],
                    "clock_pair": bound["clock_pair"],
                    "assumed_abs_dchi_dN": f"{fraction:g}",
                    "assumed_tau_clock_time_yr_inv": "0" if fraction == 0.0 else f"{NOMINAL_H0_YR_INV * fraction:.6e}",
                    "max_abs_kappa_alpha_1sigma": kappa_1,
                    "max_abs_kappa_alpha_2sigma": kappa_2,
                    "verdict_if_assumption_true": verdict,
                    "standalone_kappa_bound_ready": "false",
                    "valid_for_claim": "false",
                }
            )
    return rows


def tau_survival_rows() -> list[dict[str, object]]:
    product_rows = read_csv(OUT / "P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv")
    kappa_values = [0.01, 0.1, 1.0, 10.0]
    rows: list[dict[str, object]] = []
    for bound in product_rows:
        one_sigma = float(bound["conservative_abs_product_bound_1sigma_yr_inv"])
        for kappa in kappa_values:
            tau_max = one_sigma / kappa
            rows.append(
                {
                    "survival_id": f"TS648_{len(rows):02d}",
                    "clock_pair_id": bound["clock_pair_id"],
                    "assumed_abs_kappa_alpha": f"{kappa:g}",
                    "max_abs_tau_clock_time_yr_inv_1sigma": f"{tau_max:.6e}",
                    "max_abs_dchi_dN_against_H0": f"{tau_max / NOMINAL_H0_YR_INV:.6e}",
                    "plain_english": f"for |kappa_alpha|={kappa:g}, lab chi_X drift must be <= {tau_max / NOMINAL_H0_YR_INV:.3e} H0 using this clock pair",
                    "valid_for_claim": "false",
                }
            )
    return rows


def local_silence_decision_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "LSD648_0_product_bound_runner",
            "gate": "clock product-bound runner gives finite pressure numbers",
            "result": "pass_nonclaim",
            "meaning": "finite alpha branch is now quantitatively pressured",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "LSD648_1_local_silence_theorem",
            "gate": "local dchi_X/dt=0 is parent-derived",
            "result": "fail_missing",
            "meaning": "cannot use silence branch as evidence or pass",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "LSD648_2_order_one_survival",
            "gate": "order-one finite kappa survives Hubble-scale local drift",
            "result": "fail_if_assumed_dchi_dN_order_one",
            "meaning": "Yb bound requires |kappa_alpha*dchi_X/dN| <= about 2.9e-8 for H0-normalized drift",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "LSD648_3_ultra_screening_requirement",
            "gate": "if |kappa_alpha|~1, local chi_X drift must be ultra-screened",
            "result": "pass_diagnostic",
            "meaning": "requires |dchi_X/dN| <= 2.93e-8 relative to H0 from Yb row",
            "valid_for_claim": "false",
        },
    ]


def next_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "NC648_0",
            "next_target": NEXT_TARGET,
            "work_item": "Try to derive local chi_X silence from strict coframe plus closed/gapped boundary-state selection.",
            "acceptance_condition": "parent action selects local representative and proves dchi_X/dt=0 for lab clock domains",
        },
        {
            "contract_id": "NC648_1",
            "next_target": NEXT_TARGET,
            "work_item": "If silence fails, formalize ultra-screened finite branch with |dchi_X/dN| bounded by clock data.",
            "acceptance_condition": "finite alpha branch carries explicit ultra-screening prior and remains nonclaim",
        },
        {
            "contract_id": "NC648_2",
            "next_target": NEXT_TARGET,
            "work_item": "Do not convert product bounds into standalone kappa bounds without tau_clock dynamics.",
            "acceptance_condition": "validation rejects any standalone kappa claim unless tau dynamics are sourced",
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D648_0",
            "route": "local_chiX_silence",
            "decision": "best_theory_route_but_not_proved",
            "why": "it would evade clock alpha drift cleanly, but all available silence routes are conditional",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D648_1",
            "route": "ultra_screened_finite_branch",
            "decision": "fallback_required_if_silence_fails",
            "why": "clock product bounds force |dchi_X/dN| to be far below H0 for order-one kappa_alpha",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "product_runner_ready": "true_nonclaim",
            "local_chiX_silence_proved": "false",
            "strongest_H0_normalized_product_bound": "2.93e-8",
            "order_one_kappa_requires_dchi_dN_below": "2.93e-8",
            "standalone_kappa_bound_ready": "false",
            "hardest_blocker": "local chi_X dynamics or silence theorem is not parent-derived",
            "next_target": NEXT_TARGET,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    local_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    survival_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V648_0_source_paths_exist", all(row["exists"] == "true" for row in source_rows), "all cited local source paths exist"))
    prior = read_csv(OUT / "P8_Y5_BRR545_647_VALIDATION.csv")
    checks.append(("V648_1_prior_647_validation_clean", all(row.get("result") == "pass" for row in prior), "647 validation remains clean"))
    checks.append(("V648_2_local_silence_not_proved", all(row["valid_for_claim"] == "false" for row in local_rows) and any(row["current_status"] == "conditional_only" for row in local_rows), "local silence routes remain conditional/nonclaim"))
    checks.append(("V648_3_product_runner_row_count", len(runner_rows) == 12, "product runner covers two clock pairs times six drift assumptions"))
    checks.append(("V648_4_runner_no_standalone_claim", all(row["standalone_kappa_bound_ready"] == "false" and row["valid_for_claim"] == "false" for row in runner_rows), "runner rows do not claim standalone kappa bounds"))
    yb_h0 = [row for row in runner_rows if row["clock_pair_id"] == "CAS646_1_YbE3E2" and row["assumed_abs_dchi_dN"] == "1"]
    checks.append(("V648_5_yb_H0_bound_is_brutal", len(yb_h0) == 1 and float(yb_h0[0]["max_abs_kappa_alpha_1sigma"]) < 3e-8, "Yb H0-normalized row forces kappa below 3e-8 if dchi/dN=1"))
    checks.append(("V648_6_survival_rows_cover_assumptions", len(survival_rows) == 8 and all(row["valid_for_claim"] == "false" for row in survival_rows), "survival rows cover two clocks times four kappa assumptions"))
    checks.append(("V648_7_order_one_tau_requirement", any(row["clock_pair_id"] == "CAS646_1_YbE3E2" and row["assumed_abs_kappa_alpha"] == "1" and float(row["max_abs_dchi_dN_against_H0"]) < 3e-8 for row in survival_rows), "order-one kappa requires Yb tau/H0 below 3e-8"))
    checks.append(("V648_8_gates_nonclaim", all(row["valid_for_claim"] == "false" for row in gate_rows) and any(row["gate_id"] == "LSD648_1_local_silence_theorem" and row["result"] == "fail_missing" for row in gate_rows), "gates keep local silence unproved"))
    checks.append(("V648_9_next_contract_points_to_649", all(row["next_target"] == NEXT_TARGET for row in next_rows), "next contract points to 649"))
    checks.append(("V648_10_decisions_nonclaim", all(row["valid_for_claim"] == "false" for row in decision), "decision rows are nonclaim"))
    checks.append(("V648_11_summary_nonclaim", summary[0]["standalone_kappa_bound_ready"] == "false" and summary[0]["local_chiX_silence_proved"] == "false", "summary blocks standalone claim"))

    fw = ROOT.parent / "formalization-workbench"
    cutoff = datetime(2026, 5, 31, 14, 42, 0).timestamp()
    changed_after_cutoff = 0
    if fw.exists():
        for path in fw.rglob("*"):
            if path.is_file() and path.stat().st_mtime > cutoff:
                changed_after_cutoff += 1
    checks.append(("V648_12_formalization_workbench_unchanged", changed_after_cutoff == 0, f"formalization files changed after cutoff: {changed_after_cutoff}"))

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
    local_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    survival_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 648 Y5/R10 Clock Product-Bound Runner or Derive Local chi_X Dynamics",
        "",
        "## Verdict",
        "",
        f"- Status: `{STATUS}`",
        f"- Claim ceiling: `{CLAIM_CEILING}`",
        "- Local `chi_X` silence is the clean theory route, but it is not parent-derived in the current corpus.",
        "- The product-bound runner quantifies the fallback: if local `dchi_X/dN` is order unity, Yb+ clocks force `|kappa_alpha| < 3e-8`.",
        "- For `|kappa_alpha| ~ 1`, lab `chi_X` drift must be below about `2.93e-8 H0` from the Yb+ E3/E2 product bound.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["source_id", "label", "path", "exists", "role"]),
        "",
        "## Local chi_X Dynamics Attempt",
        "",
        markdown_table(local_rows, ["attempt_id", "route", "current_status", "blocking_gap", "tau_clock_result"]),
        "",
        "## Product Bound Runner",
        "",
        markdown_table(runner_rows, ["runner_id", "clock_pair_id", "assumed_abs_dchi_dN", "assumed_tau_clock_time_yr_inv", "max_abs_kappa_alpha_1sigma", "verdict_if_assumption_true"]),
        "",
        "## Tau Survival Requirements",
        "",
        markdown_table(survival_rows, ["survival_id", "clock_pair_id", "assumed_abs_kappa_alpha", "max_abs_tau_clock_time_yr_inv_1sigma", "max_abs_dchi_dN_against_H0", "plain_english"]),
        "",
        "## Decision Gates",
        "",
        markdown_table(gate_rows, ["gate_id", "gate", "result", "meaning"]),
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
        "- This is one of the sharpest local constraints so far: finite alpha response survives only with local silence or ultra-screening.",
        "- That is not a defeat by itself; it is a clean fork. Either prove `dchi_X/dt=0` in lab domains, or make the finite branch explicitly ultra-screened.",
        "- No standalone `kappa_alpha` bound is claimed here because `tau_clock` dynamics are still not derived.",
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(summary, ["status", "product_runner_ready", "local_chiX_silence_proved", "strongest_H0_normalized_product_bound", "order_one_kappa_requires_dchi_dN_below", "standalone_kappa_bound_ready", "hardest_blocker", "next_target"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    local_rows = local_chiX_dynamics_attempt_rows()
    runner_rows = product_bound_runner_rows()
    survival_rows = tau_survival_rows()
    gate_rows = local_silence_decision_gate_rows()
    next_rows = next_contract_rows()
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, local_rows, runner_rows, survival_rows, gate_rows, next_rows, decision, summary)

    write_csv(OUT / "P8_Y5_R10_648_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_648_LOCAL_CHIX_DYNAMICS_ATTEMPT.csv", local_rows)
    write_csv(OUT / "P8_Y5_R10_648_CLOCK_PRODUCT_BOUND_RUNNER.csv", runner_rows)
    write_csv(OUT / "P8_Y5_R10_648_TAU_SURVIVAL_REQUIREMENTS.csv", survival_rows)
    write_csv(OUT / "P8_Y5_R10_648_LOCAL_SILENCE_DECISION_GATES.csv", gate_rows)
    write_csv(OUT / "P8_Y5_R10_648_NEXT_CONTRACT.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_648_DECISION.csv", decision)
    write_csv(OUT / "P8_Y5_R10_648_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_BRR545_648_VALIDATION.csv", validation)
    write_doc(source_rows, local_rows, runner_rows, survival_rows, gate_rows, next_rows, decision, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote_doc={DOC_PATH}")
    print(f"wrote_csv_dir={OUT}")
    print(f"runner_rows={len(runner_rows)}")
    print("Yb_H0_order_one_dchi_bound_on_abs_kappa_alpha=2.93e-8")
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
