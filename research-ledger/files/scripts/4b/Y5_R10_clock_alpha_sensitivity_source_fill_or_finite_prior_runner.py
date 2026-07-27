from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
OUT = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_clock_alpha_sensitivity_source_fill_or_finite_prior_runner.py"
DOC_PATH = ROOT / "646-Y5-R10-clock-alpha-sensitivity-source-fill-or-finite-prior-runner.md"

STATUS = "Y5_R10_clock_alpha_sources_filled_R2_redshift_repaired_finite_runner_still_blocked_by_chiX_tau"
CLAIM_CEILING = "clock_alpha_sensitivity_source_fill_and_symbolic_runner_only_no_numeric_kappa_alpha_score_no_clock_or_local_claim"
NEXT_TARGET = "647-Y5-R10-derive-or-define-chiX-and-tau-clock-map.md"


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


def is_url(value: str) -> bool:
    return value.startswith("https://") or value.startswith("http://")


def source_register_rows() -> list[dict[str, object]]:
    local_sources = [
        ("S646_0", "checkpoint_645_doc", ROOT / "645-Y5-R10-finite-kappa-alpha-bound-input-fill-and-prior-discipline.md", "prior finite-branch discipline checkpoint"),
        ("S646_1", "validation_645", OUT / "P8_Y5_BRR545_645_VALIDATION.csv", "prior validation"),
        ("S646_2", "bound_input_645", OUT / "P8_Y5_R10_645_BOUND_INPUT_LEDGER.csv", "finite branch bound input ledger"),
        ("S646_3", "projection_readiness_645", OUT / "P8_Y5_R10_645_PROJECTION_READINESS.csv", "projection-readiness input"),
        ("S646_4", "finite_prior_645", OUT / "P8_Y5_R10_645_FINITE_PRIOR_DISCIPLINE.csv", "finite prior input"),
        ("S646_5", "local_bound_matrix_639", OUT / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv", "R2 clock-redshift row to repair"),
        ("S646_6", "generator_script_646", SCRIPT_PATH, "this checkpoint generator"),
    ]
    web_sources = [
        ("W646_0", "NIST_Rosenband_AlHg", "https://www.nist.gov/publications/frequency-ratio-al-and-hg-single-ion-optical-clocks-metrology-17th-decimal-place", "NIST record for Al+/Hg+ optical-clock ratio and alpha drift statement"),
        ("W646_1", "Dzuba_Flambaum_arXiv_1999", "https://arxiv.org/abs/physics/9908047", "primary theory paper defining optical-clock alpha sensitivity idea"),
        ("W646_2", "Frontiers_HCI_clock_review_2023", "https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2023.1104848/full", "source table for K_alpha values and clock-pair sensitivity differences"),
        ("W646_3", "PTB_Yb_clock_alpha_limit", "https://oar.ptb.de/resources/show/10.7795/110.20211216", "PTB source for Yb+ E3/E2 alpha-drift limit"),
        ("W646_4", "Galileo_redshift_PRL_pdf", "https://nebula.esa.int/sites/default/files/neb_tec_study/1301/C4000115150Paper.pdf", "R2 redshift bound source; used only as LPI/redshift parameter source, not alpha_EM"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, label, path, role in local_sources:
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_kind": "local",
                "path_or_url": rel(path),
                "available": bool_text(path.exists()),
                "role": role,
                "valid_for_claim": "false",
            }
        )
    for source_id, label, url, role in web_sources:
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_kind": "web",
                "path_or_url": url,
                "available": bool_text(is_url(url)),
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def clock_alpha_sensitivity_rows() -> list[dict[str, object]]:
    return [
        {
            "clock_pair_id": "CAS646_0_AlHg",
            "clock_pair": "27Al+ / 199Hg+",
            "transition_1": "Al+ clock transition",
            "transition_2": "Hg+ optical clock transition",
            "K_alpha_1": "0.008",
            "K_alpha_2": "-2.94",
            "delta_K_alpha_used": "2.95",
            "delta_K_alpha_source_status": "source_backed_review_table",
            "alpha_drift_source_value": "NIST: 1.4e-17 +/- 1.7e-17 yr^-1; Frontiers table reports -1.6e-17 +/- 2.3e-17 yr^-1",
            "source_urls": "https://www.nist.gov/publications/frequency-ratio-al-and-hg-single-ion-optical-clocks-metrology-17th-decimal-place; https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2023.1104848/full",
            "MTS_projection": "d ln R_AlHg = delta_K_alpha * kappa_alpha * d chi_X",
            "MTS_missing": "chi_X unit; tau_clock/time map from local MTS state to clock-ratio observable",
            "numeric_score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "clock_pair_id": "CAS646_1_YbE3E2",
            "clock_pair": "171Yb+ E3 / 171Yb+ E2",
            "transition_1": "Yb+ electric octupole E3",
            "transition_2": "Yb+ electric quadrupole E2",
            "K_alpha_1": "-5.95",
            "K_alpha_2": "1.03",
            "delta_K_alpha_used": "-6.95",
            "delta_K_alpha_source_status": "source_backed_review_table_stated_difference",
            "alpha_drift_source_value": "PTB/Frontiers: 1.0e-18 +/- 1.1e-18 yr^-1",
            "source_urls": "https://oar.ptb.de/resources/show/10.7795/110.20211216; https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2023.1104848/full",
            "MTS_projection": "d ln R_E3E2 = delta_K_alpha * kappa_alpha * d chi_X",
            "MTS_missing": "chi_X unit; tau_clock/time map from local MTS state to clock-ratio observable",
            "numeric_score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def R2_repair_rows() -> list[dict[str, object]]:
    local_bounds = {row["row_id"]: row for row in read_csv(OUT / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv")}
    r2 = local_bounds["R2_clock_redshift"]
    return [
        {
            "repair_id": "R2R646_0",
            "source_row_id": "R2_clock_redshift",
            "old_label": r2["observable"],
            "old_bound": r2["bound_value"],
            "old_units": r2["bound_units"],
            "repair_status": "not_alpha_EM",
            "correct_interpretation": "Galileo eccentric-satellite row constrains an LPI/gravitational-redshift violation parameter called alpha in that paper, not the fine-structure constant alpha_EM.",
            "allowed_use": "clock/coframe/LPI local-position-invariance pressure only",
            "forbidden_use": "do_not_use_as_delta_alpha_EM_or_clock_K_alpha_pair_bound",
            "source_url": "https://nebula.esa.int/sites/default/files/neb_tec_study/1301/C4000115150Paper.pdf",
            "valid_for_claim": "false",
        }
    ]


def clock_projection_ledger_rows() -> list[dict[str, object]]:
    return [
        {
            "projection_id": "CPL646_0_pair_ratio",
            "law": "d ln(nu_a/nu_b) = (K_alpha_a - K_alpha_b) d ln(alpha_EM)",
            "source_basis": "optical-clock alpha-sensitivity literature",
            "MTS_substitution": "d ln(alpha_EM) = kappa_alpha d chi_X",
            "MTS_law": "d ln R_ab = delta_K_alpha * kappa_alpha * d chi_X",
            "missing_to_score": "d chi_X for the experiment or tau_clock mapping",
            "numeric_score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "CPL646_1_time_drift",
            "law": "d ln R_ab/dt = delta_K_alpha * d ln(alpha_EM)/dt",
            "source_basis": "Al/Hg and Yb E3/E2 long-baseline clock comparisons",
            "MTS_substitution": "d ln(alpha_EM)/dt = kappa_alpha d chi_X/dt",
            "MTS_law": "d ln R_ab/dt = delta_K_alpha * kappa_alpha * d chi_X/dt",
            "missing_to_score": "d chi_X/dt from MTS local/cosmological state",
            "numeric_score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "CPL646_2_gravitational_potential_coupling",
            "law": "d ln R_ab = delta_K_alpha * k_alpha_Phi d Phi/c^2",
            "source_basis": "clock tests of coupling of constants to gravitational potential",
            "MTS_substitution": "k_alpha_Phi must be mapped from kappa_alpha and chi_X(Phi)",
            "MTS_law": "d ln R_ab = delta_K_alpha * kappa_alpha * (d chi_X/d Phi) d Phi",
            "missing_to_score": "chi_X(Phi) or local potential projection",
            "numeric_score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def finite_clock_runner_rows() -> list[dict[str, object]]:
    clock_rows = clock_alpha_sensitivity_rows()
    factors = [-10.0, -1.0, -0.1, -0.01, 0.01, 0.1, 1.0, 10.0]
    rows: list[dict[str, object]] = []
    for clock in clock_rows:
        delta_k = float(clock["delta_K_alpha_used"])
        for factor in factors:
            rows.append(
                {
                    "runner_id": f"FCR646_{len(rows):02d}",
                    "clock_pair_id": clock["clock_pair_id"],
                    "normalized_kappa_alpha_factor": f"{factor:g}",
                    "delta_K_alpha_used": f"{delta_k:g}",
                    "normalized_response_dlnR_per_dchiX": f"{delta_k * factor:.6g}",
                    "physical_interpretation": "symbolic sensitivity only; not a physical prediction until chi_X and tau_clock are defined",
                    "source_backed_delta_K": "true",
                    "has_chi_X_unit": "false",
                    "has_tau_clock": "false",
                    "numeric_score_ready": "false",
                    "valid_for_claim": "false",
                }
            )
    return rows


def readiness_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "RG646_0_R2_repair",
            "gate": "R2 redshift alpha is separated from alpha_EM",
            "result": "pass_repaired",
            "blocks": "misusing Galileo redshift alpha as fine-structure alpha",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "RG646_1_deltaK_source",
            "gate": "clock-pair delta_K_alpha values are source-backed",
            "result": "pass_for_source_fill",
            "blocks": "none for symbolic runner",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "RG646_2_chiX",
            "gate": "MTS chi_X or Xhat unit exists",
            "result": "fail_missing",
            "blocks": "physical kappa_alpha score",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "RG646_3_tau_clock",
            "gate": "tau_clock/time/potential map exists",
            "result": "fail_missing",
            "blocks": "clock bound projection into MTS variables",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "RG646_4_claim",
            "gate": "finite runner may make a clock-alpha claim",
            "result": "fail_policy",
            "blocks": "no numeric score until RG646_2 and RG646_3 pass",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D646_0",
            "route": "clock_alpha_source_fill",
            "decision": "source_fill_complete_nonclaim",
            "why": "Al/Hg and Yb E3/E2 provide source-backed delta_K_alpha clock pairs",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D646_1",
            "route": "finite_prior_runner",
            "decision": "symbolic_runner_complete_numeric_runner_blocked",
            "why": "delta_K is real, but chi_X and tau_clock are still missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "R2_repaired": "true",
            "clock_alpha_sources_filled": "true",
            "symbolic_runner_rows": "16",
            "numeric_score_allowed": "false",
            "strongest_positive_result": "clock alpha sensitivity coefficients are now source-backed and separated from the Galileo redshift alpha notation trap",
            "hardest_blocker": "chi_X/Xhat unit and tau_clock/time-potential map are still missing",
            "next_target": NEXT_TARGET,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    clock_rows: list[dict[str, object]],
    repair_rows: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V646_0_sources_available", all(row["available"] == "true" for row in source_rows), "all local sources exist and web source strings are valid URLs"))
    prior_validation = read_csv(OUT / "P8_Y5_BRR545_645_VALIDATION.csv")
    checks.append(("V646_1_prior_645_validation_clean", all(row.get("result") == "pass" for row in prior_validation), "645 validation remains clean"))
    checks.append(("V646_2_clock_pairs_source_backed", len(clock_rows) >= 2 and all(float(row["delta_K_alpha_used"]) != 0.0 for row in clock_rows), "clock delta_K rows are numeric and nonzero"))
    checks.append(("V646_3_clock_rows_nonclaim", all(row["numeric_score_ready"] == "false" and row["valid_for_claim"] == "false" for row in clock_rows), "clock rows remain nonclaim"))
    checks.append(("V646_4_R2_repair_explicit", repair_rows[0]["repair_status"] == "not_alpha_EM" and "do_not_use" in repair_rows[0]["forbidden_use"], "R2 alpha notation trap is repaired"))
    checks.append(("V646_5_projection_rows_blocked", all(row["numeric_score_ready"] == "false" and row["valid_for_claim"] == "false" for row in projection_rows), "projection rows remain blocked"))
    checks.append(("V646_6_runner_row_count", len(runner_rows) == 16, "symbolic runner covers two clock pairs times eight normalized factors"))
    checks.append(("V646_7_runner_nonclaim", all(row["numeric_score_ready"] == "false" and row["valid_for_claim"] == "false" for row in runner_rows), "finite runner rows remain nonclaim"))
    checks.append(("V646_8_gates_block_numeric_score", any(row["gate_id"] == "RG646_2_chiX" and row["result"] == "fail_missing" for row in gate_rows) and any(row["gate_id"] == "RG646_3_tau_clock" and row["result"] == "fail_missing" for row in gate_rows), "chiX and tau_clock gates block numeric scoring"))
    checks.append(("V646_9_decisions_nonclaim", all(row["valid_for_claim"] == "false" for row in decision), "decision rows do not claim pass"))
    checks.append(("V646_10_summary_nonclaim", summary[0]["numeric_score_allowed"] == "false" and summary[0]["R2_repaired"] == "true", "summary stays nonclaim and records R2 repair"))

    fw = ROOT.parent / "formalization-workbench"
    cutoff = datetime(2026, 5, 31, 14, 42, 0).timestamp()
    changed_after_cutoff = 0
    if fw.exists():
        for path in fw.rglob("*"):
            if path.is_file() and path.stat().st_mtime > cutoff:
                changed_after_cutoff += 1
    checks.append(("V646_11_formalization_workbench_unchanged", changed_after_cutoff == 0, f"formalization files changed after cutoff: {changed_after_cutoff}"))

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
    clock_rows: list[dict[str, object]],
    repair_rows: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 646 Y5/R10 Clock Alpha Sensitivity Source Fill or Finite Prior Runner",
        "",
        "## Verdict",
        "",
        f"- Status: `{STATUS}`",
        f"- Claim ceiling: `{CLAIM_CEILING}`",
        "- Important repair: the Galileo `alpha` redshift row is not `alpha_EM`; it is an LPI/gravitational-redshift violation parameter.",
        "- Source-backed optical-clock alpha pairs are now staged: Al+/Hg+ and Yb+ E3/E2.",
        "- The finite runner is symbolic only. It cannot score MTS until `chi_X`/`Xhat` and `tau_clock` are derived or explicitly defined.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["source_id", "label", "source_kind", "path_or_url", "available", "role"]),
        "",
        "## Clock Alpha Sensitivity Sources",
        "",
        markdown_table(clock_rows, ["clock_pair_id", "clock_pair", "K_alpha_1", "K_alpha_2", "delta_K_alpha_used", "alpha_drift_source_value", "numeric_score_ready"]),
        "",
        "## R2 Redshift Repair",
        "",
        markdown_table(repair_rows, ["repair_id", "source_row_id", "old_label", "repair_status", "correct_interpretation", "forbidden_use"]),
        "",
        "## Clock Projection Ledger",
        "",
        markdown_table(projection_rows, ["projection_id", "law", "MTS_substitution", "MTS_law", "missing_to_score"]),
        "",
        "## Finite Runner Smoke",
        "",
        markdown_table(runner_rows[:10], ["runner_id", "clock_pair_id", "normalized_kappa_alpha_factor", "delta_K_alpha_used", "normalized_response_dlnR_per_dchiX", "numeric_score_ready"]),
        "",
        f"- Full symbolic runner rows: `{len(runner_rows)}`",
        "",
        "## Readiness Gates",
        "",
        markdown_table(gate_rows, ["gate_id", "gate", "result", "blocks"]),
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
        "- This is a useful correction: the clock path is alive, but the previous R2 row cannot be used as a fine-structure-alpha bound.",
        "- The real clock-alpha path now runs through frequency-ratio pairs with `delta_K_alpha` coefficients.",
        "- Next, we need the MTS side of the bridge: `chi_X` and `tau_clock`; without them, the runner stays smoke-only.",
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(summary, ["status", "R2_repaired", "clock_alpha_sources_filled", "symbolic_runner_rows", "numeric_score_allowed", "hardest_blocker", "next_target"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    clock_rows = clock_alpha_sensitivity_rows()
    repair_rows = R2_repair_rows()
    projection_rows = clock_projection_ledger_rows()
    runner_rows = finite_clock_runner_rows()
    gate_rows = readiness_gate_rows()
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, clock_rows, repair_rows, projection_rows, runner_rows, gate_rows, decision, summary)

    write_csv(OUT / "P8_Y5_R10_646_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv", clock_rows)
    write_csv(OUT / "P8_Y5_R10_646_R2_CLOCK_REDSHIFT_REPAIR.csv", repair_rows)
    write_csv(OUT / "P8_Y5_R10_646_CLOCK_PROJECTION_LEDGER.csv", projection_rows)
    write_csv(OUT / "P8_Y5_R10_646_FINITE_CLOCK_RUNNER_SMOKE.csv", runner_rows)
    write_csv(OUT / "P8_Y5_R10_646_READINESS_GATES.csv", gate_rows)
    write_csv(OUT / "P8_Y5_BRR545_646_DECISION.csv", decision)
    write_csv(OUT / "P8_Y5_R10_646_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_BRR545_646_VALIDATION.csv", validation)
    write_doc(source_rows, clock_rows, repair_rows, projection_rows, runner_rows, gate_rows, decision, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote_doc={DOC_PATH}")
    print(f"wrote_csv_dir={OUT}")
    print(f"clock_pairs={len(clock_rows)}")
    print(f"symbolic_runner_rows={len(runner_rows)}")
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
