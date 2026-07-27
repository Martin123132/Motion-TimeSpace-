from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
OUT = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_derive_or_define_chiX_and_tau_clock_map.py"
DOC_PATH = ROOT / "647-Y5-R10-derive-or-define-chiX-and-tau-clock-map.md"

STATUS = "Y5_R10_chiX_tau_clock_defined_as_product_bound_contract_not_parent_derived_clock_product_bound_ready_nonclaim"
CLAIM_CEILING = "clock_product_bound_on_kappa_alpha_times_tau_clock_only_no_standalone_kappa_alpha_score_no_clock_or_local_claim"
NEXT_TARGET = "648-Y5-R10-clock-product-bound-runner-or-derive-local-chiX-dynamics.md"
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
        ("S647_0", "checkpoint_646_doc", ROOT / "646-Y5-R10-clock-alpha-sensitivity-source-fill-or-finite-prior-runner.md", "clock-alpha source fill and R2 repair"),
        ("S647_1", "validation_646", OUT / "P8_Y5_BRR545_646_VALIDATION.csv", "prior validation"),
        ("S647_2", "clock_alpha_sources_646", OUT / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv", "source-backed delta K alpha pairs"),
        ("S647_3", "clock_projection_646", OUT / "P8_Y5_R10_646_CLOCK_PROJECTION_LEDGER.csv", "clock projection laws"),
        ("S647_4", "R2_repair_646", OUT / "P8_Y5_R10_646_R2_CLOCK_REDSHIFT_REPAIR.csv", "R2 redshift alpha notation repair"),
        ("S647_5", "finite_coordinate_645", OUT / "P8_Y5_R10_645_FINITE_COORDINATE_REQUIREMENT.csv", "chi_X coordinate requirement"),
        ("S647_6", "clock_map_155", ROOT / "155-redshift-projection-clock-map-owner.md", "older observer/coframe clock-map owner target"),
        ("S647_7", "clock_functional_156", ROOT / "156-clock-projection-functional-theorem-or-demotion.md", "cell-balanced clock functional target"),
        ("S647_8", "strict_local_coframe_242", ROOT / "242-strict-local-coframe-branch-or-domain-projector-action.md", "strict local coframe conditional silence"),
        ("S647_9", "local_silence_300", ROOT / "300-boundary-state-local-silence-theorem-attempt.md", "local-bound silence conditional theorem"),
        ("S647_10", "generator_script_647", SCRIPT_PATH, "this checkpoint generator"),
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


def chiX_definition_rows() -> list[dict[str, object]]:
    return [
        {
            "chi_id": "CHX647_0_parent_vertical_norm",
            "candidate_definition": "chi_X = ln[(C_P N_Q hbar c)/(C_P N_Q hbar c)_ref] from the parent vertical norm formula",
            "status": "not_derived",
            "what_it_would_do": "turn kappa_alpha into a parent-owned response coefficient",
            "problem": "644 showed C_P, N_Q, coframe descent, and no-extra-F2 are unsigned",
            "allowed_use_now": "dormant theorem contract only",
            "valid_for_claim": "false",
        },
        {
            "chi_id": "CHX647_1_finite_alpha_pressure_coordinate",
            "candidate_definition": "chi_X is a dimensionless local alpha-pressure coordinate satisfying d ln(alpha_EM)=kappa_alpha d chi_X",
            "status": "defined_as_closure_coordinate",
            "what_it_would_do": "lets clock data bound the product kappa_alpha * dchi_X/dt",
            "problem": "does not identify the parent state variable; standalone kappa_alpha remains unbounded",
            "allowed_use_now": "internal finite-runner product-bound coordinate",
            "valid_for_claim": "false",
        },
        {
            "chi_id": "CHX647_2_clock_coframe_candidate",
            "candidate_definition": "chi_X may be a local/coframe projection of the signed clock scalar C_clock[Q_coh,D] from the 155/156 clock-map route",
            "status": "theorem_target_not_derived",
            "what_it_would_do": "connect alpha pressure to the same observer/coframe language used in redshift work",
            "problem": "C_clock is not parent-derived and may be gauge/closure if not varied from an action",
            "allowed_use_now": "candidate for 648 derivation only",
            "valid_for_claim": "false",
        },
        {
            "chi_id": "CHX647_3_strict_local_silence",
            "candidate_definition": "chi_X_local = constant in closed/gapped local bound domains",
            "status": "conditional_only",
            "what_it_would_do": "tau_clock=0 locally and no clock-alpha drift",
            "problem": "242/300 local silence conditions are not parent-derived",
            "allowed_use_now": "not an evidence branch; only a sufficient-condition target",
            "valid_for_claim": "false",
        },
    ]


def tau_clock_map_rows() -> list[dict[str, object]]:
    return [
        {
            "tau_id": "TAU647_0_time_drift",
            "definition": "tau_clock_time = d chi_X / dt",
            "units": "yr^-1",
            "projection_law": "d ln(alpha_EM)/dt = kappa_alpha * tau_clock_time",
            "status": "defined_product_map",
            "what_clocks_bound": "|kappa_alpha * tau_clock_time|",
            "standalone_kappa_bound_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "tau_id": "TAU647_1_H0_normalized_drift",
            "definition": "tau_clock_time = H0 * d chi_X/dN with nominal H0=7.16e-11 yr^-1",
            "units": "yr^-1",
            "projection_law": "d ln(alpha_EM)/dt = kappa_alpha * H0 * dchi_X/dN",
            "status": "diagnostic_only",
            "what_clocks_bound": "|kappa_alpha * dchi_X/dN| after dividing by nominal H0",
            "standalone_kappa_bound_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "tau_id": "TAU647_2_potential_map",
            "definition": "tau_clock_Phi = d chi_X / d(Phi/c^2)",
            "units": "dimensionless",
            "projection_law": "d ln(alpha_EM) = kappa_alpha * tau_clock_Phi * d(Phi/c^2)",
            "status": "source_missing",
            "what_clocks_bound": "potential-coupled alpha variation if annual/potential source rows are added",
            "standalone_kappa_bound_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "tau_id": "TAU647_3_local_silence",
            "definition": "tau_clock_local = 0 in a parent-proved closed/gapped strict-local coframe domain",
            "units": "yr^-1_or_dimensionless_depending_on_probe",
            "projection_law": "d ln(alpha_EM)=0 locally if local silence theorem is parent-signed",
            "status": "conditional_not_active",
            "what_clocks_bound": "nothing until local silence is proved; cannot be used to evade clock bounds",
            "standalone_kappa_bound_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def clock_product_bound_rows() -> list[dict[str, object]]:
    return [
        {
            "bound_id": "CPB647_0_AlHg",
            "clock_pair_id": "CAS646_0_AlHg",
            "clock_pair": "27Al+ / 199Hg+",
            "source_measurements": "NIST 1.4e-17 +/- 1.7e-17 yr^-1; Frontiers table -1.6e-17 +/- 2.3e-17 yr^-1",
            "conservative_abs_product_bound_1sigma_yr_inv": "3.9e-17",
            "conservative_abs_product_bound_2sigma_yr_inv": "6.2e-17",
            "product_bound_statement": "|kappa_alpha * tau_clock_time| <= 3.9e-17 yr^-1 at conservative 1sigma bookkeeping level",
            "standalone_kappa_bound_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CPB647_1_YbE3E2",
            "clock_pair_id": "CAS646_1_YbE3E2",
            "clock_pair": "171Yb+ E3 / 171Yb+ E2",
            "source_measurements": "PTB/Frontiers 1.0e-18 +/- 1.1e-18 yr^-1",
            "conservative_abs_product_bound_1sigma_yr_inv": "2.1e-18",
            "conservative_abs_product_bound_2sigma_yr_inv": "3.2e-18",
            "product_bound_statement": "|kappa_alpha * tau_clock_time| <= 2.1e-18 yr^-1 at conservative 1sigma bookkeeping level",
            "standalone_kappa_bound_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def h0_normalized_diagnostic_rows() -> list[dict[str, object]]:
    rows = []
    for bound in clock_product_bound_rows():
        one_sigma = float(bound["conservative_abs_product_bound_1sigma_yr_inv"])
        two_sigma = float(bound["conservative_abs_product_bound_2sigma_yr_inv"])
        rows.append(
            {
                "diagnostic_id": bound["bound_id"].replace("CPB", "H0D"),
                "clock_pair_id": bound["clock_pair_id"],
                "nominal_H0_yr_inv": f"{NOMINAL_H0_YR_INV:.3e}",
                "bound_on_abs_kappa_times_dchi_dN_1sigma": f"{one_sigma / NOMINAL_H0_YR_INV:.6g}",
                "bound_on_abs_kappa_times_dchi_dN_2sigma": f"{two_sigma / NOMINAL_H0_YR_INV:.6g}",
                "interpretation": "diagnostic only: assumes tau_clock_time = H0 dchi_X/dN; not a derived MTS clock map",
                "standalone_kappa_bound_ready": "false",
                "valid_for_claim": "false",
            }
        )
    return rows


def tau_requirement_rows() -> list[dict[str, object]]:
    factors = [0.01, 0.1, 1.0, 10.0]
    rows = []
    for bound in clock_product_bound_rows():
        one_sigma = float(bound["conservative_abs_product_bound_1sigma_yr_inv"])
        for factor in factors:
            rows.append(
                {
                    "requirement_id": f"TR647_{len(rows):02d}",
                    "clock_pair_id": bound["clock_pair_id"],
                    "assumed_abs_kappa_alpha": f"{factor:g}",
                    "max_abs_tau_clock_time_yr_inv_1sigma": f"{one_sigma / factor:.6e}",
                    "equivalent_tau_over_H0_nominal": f"{(one_sigma / factor) / NOMINAL_H0_YR_INV:.6e}",
                    "interpretation": "if this kappa factor is physical, tau_clock must be below this value; diagnostic only",
                    "valid_for_claim": "false",
                }
            )
    return rows


def readiness_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "RG647_0_chiX_defined",
            "gate": "dimensionless chi_X exists as finite closure coordinate",
            "result": "pass_definition_only",
            "blocks": "parent derivation and standalone kappa claim",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "RG647_1_tau_product_map",
            "gate": "tau_clock_time=dchi_X/dt product map exists",
            "result": "pass_product_bound_only",
            "blocks": "standalone kappa bound without tau dynamics",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "RG647_2_clock_product_bound",
            "gate": "source-backed product bounds can be written",
            "result": "pass_nonclaim_internal",
            "blocks": "public clock-alpha claim",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "RG647_3_parent_chiX",
            "gate": "chi_X is derived from the parent action",
            "result": "fail_missing",
            "blocks": "theory promotion",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "RG647_4_tau_dynamics",
            "gate": "dchi_X/dt or dchi_X/dN is derived for local clocks",
            "result": "fail_missing",
            "blocks": "standalone kappa_alpha score",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D647_0",
            "route": "clock_product_bound",
            "decision": "selected_next_runner",
            "why": "clock data already constrain kappa_alpha*tau_clock_time even without standalone tau dynamics",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D647_1",
            "route": "derive_local_chiX_dynamics",
            "decision": "parallel_theory_target",
            "why": "only a parent/local chi_X dynamics theorem can turn product bounds into kappa_alpha bounds",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "chiX_defined": "closure_coordinate_only",
            "tau_clock_defined": "product_map_only",
            "product_bound_ready": "true_nonclaim",
            "standalone_kappa_bound_ready": "false",
            "strongest_bound_product_1sigma_yr_inv": "2.1e-18",
            "hardest_blocker": "no derived dchi_X/dt or dchi_X/dN for local clock experiments",
            "next_target": NEXT_TARGET,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    chi_rows: list[dict[str, object]],
    tau_rows: list[dict[str, object]],
    product_rows: list[dict[str, object]],
    h0_rows: list[dict[str, object]],
    tau_req_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V647_0_source_paths_exist", all(row["exists"] == "true" for row in source_rows), "all cited local source paths exist"))
    prior_validation = read_csv(OUT / "P8_Y5_BRR545_646_VALIDATION.csv")
    checks.append(("V647_1_prior_646_validation_clean", all(row.get("result") == "pass" for row in prior_validation), "646 validation remains clean"))
    r2_repair = read_csv(OUT / "P8_Y5_R10_646_R2_CLOCK_REDSHIFT_REPAIR.csv")[0]
    checks.append(("V647_2_R2_repair_imported", r2_repair.get("repair_status") == "not_alpha_EM", "R2 repair is imported"))
    checks.append(("V647_3_chiX_closure_not_claim", any(row["status"] == "defined_as_closure_coordinate" for row in chi_rows) and all(row["valid_for_claim"] == "false" for row in chi_rows), "chiX closure coordinate exists but is nonclaim"))
    checks.append(("V647_4_tau_time_product_map", any(row["tau_id"] == "TAU647_0_time_drift" and row["status"] == "defined_product_map" for row in tau_rows), "tau_clock time product map exists"))
    checks.append(("V647_5_product_bounds_positive", all(float(row["conservative_abs_product_bound_1sigma_yr_inv"]) > 0.0 and row["standalone_kappa_bound_ready"] == "false" for row in product_rows), "product bounds are positive and not standalone kappa bounds"))
    strongest = min(float(row["conservative_abs_product_bound_1sigma_yr_inv"]) for row in product_rows)
    checks.append(("V647_6_strongest_bound_is_Yb_scale", strongest <= 2.1e-18 + 1e-30, "strongest clock product bound is at Yb E3/E2 scale"))
    checks.append(("V647_7_h0_diagnostic_nonclaim", all(row["standalone_kappa_bound_ready"] == "false" and row["valid_for_claim"] == "false" for row in h0_rows), "H0 diagnostic rows are nonclaim"))
    checks.append(("V647_8_tau_requirements_nonclaim", len(tau_req_rows) == 8 and all(row["valid_for_claim"] == "false" for row in tau_req_rows), "tau requirements cover two clocks times four kappa factors"))
    checks.append(("V647_9_gates_block_standalone_score", any(row["gate_id"] == "RG647_4_tau_dynamics" and row["result"] == "fail_missing" for row in gate_rows), "tau dynamics gate blocks standalone kappa score"))
    checks.append(("V647_10_decisions_nonclaim", all(row["valid_for_claim"] == "false" for row in decision), "decision rows do not claim pass"))
    checks.append(("V647_11_summary_product_only", summary[0]["product_bound_ready"] == "true_nonclaim" and summary[0]["standalone_kappa_bound_ready"] == "false", "summary marks product-only bound"))

    fw = ROOT.parent / "formalization-workbench"
    cutoff = datetime(2026, 5, 31, 14, 42, 0).timestamp()
    changed_after_cutoff = 0
    if fw.exists():
        for path in fw.rglob("*"):
            if path.is_file() and path.stat().st_mtime > cutoff:
                changed_after_cutoff += 1
    checks.append(("V647_12_formalization_workbench_unchanged", changed_after_cutoff == 0, f"formalization files changed after cutoff: {changed_after_cutoff}"))

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
    chi_rows: list[dict[str, object]],
    tau_rows: list[dict[str, object]],
    product_rows: list[dict[str, object]],
    h0_rows: list[dict[str, object]],
    tau_req_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 647 Y5/R10 Derive or Define chi_X and tau_clock Map",
        "",
        "## Verdict",
        "",
        f"- Status: `{STATUS}`",
        f"- Claim ceiling: `{CLAIM_CEILING}`",
        "- `chi_X` can be defined as a finite alpha-pressure coordinate, but it is not parent-derived.",
        "- `tau_clock_time = d chi_X/dt` gives a clean product map. Clocks now bound `kappa_alpha * tau_clock_time`, not `kappa_alpha` alone.",
        "- Strongest staged product bound is the Yb+ E3/E2 row: `|kappa_alpha * tau_clock_time| <= 2.1e-18 yr^-1` at conservative 1-sigma bookkeeping level.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["source_id", "label", "path", "exists", "role"]),
        "",
        "## chi_X Definition Attempt",
        "",
        markdown_table(chi_rows, ["chi_id", "candidate_definition", "status", "what_it_would_do", "problem", "allowed_use_now"]),
        "",
        "## tau_clock Map",
        "",
        markdown_table(tau_rows, ["tau_id", "definition", "units", "projection_law", "status", "what_clocks_bound"]),
        "",
        "## Clock Product Bound",
        "",
        markdown_table(product_rows, ["bound_id", "clock_pair", "conservative_abs_product_bound_1sigma_yr_inv", "conservative_abs_product_bound_2sigma_yr_inv", "product_bound_statement", "standalone_kappa_bound_ready"]),
        "",
        "## H0 Diagnostic",
        "",
        markdown_table(h0_rows, ["diagnostic_id", "clock_pair_id", "nominal_H0_yr_inv", "bound_on_abs_kappa_times_dchi_dN_1sigma", "interpretation"]),
        "",
        "## tau Requirement Diagnostic",
        "",
        markdown_table(tau_req_rows, ["requirement_id", "clock_pair_id", "assumed_abs_kappa_alpha", "max_abs_tau_clock_time_yr_inv_1sigma", "equivalent_tau_over_H0_nominal"]),
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
        "- This is a real step: clocks now give a sharp product constraint on the finite alpha branch.",
        "- It is also a hard warning: unless `dchi_X/dt` is tiny or zero in lab domains, finite alpha response is brutally constrained.",
        "- The next target is either run the product-bound ledger cleanly or derive local `chi_X` dynamics/silence so the product has a theory value.",
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(summary, ["status", "chiX_defined", "tau_clock_defined", "product_bound_ready", "standalone_kappa_bound_ready", "strongest_bound_product_1sigma_yr_inv", "hardest_blocker", "next_target"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    chi_rows = chiX_definition_rows()
    tau_rows = tau_clock_map_rows()
    product_rows = clock_product_bound_rows()
    h0_rows = h0_normalized_diagnostic_rows()
    tau_req_rows = tau_requirement_rows()
    gate_rows = readiness_gate_rows()
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, chi_rows, tau_rows, product_rows, h0_rows, tau_req_rows, gate_rows, decision, summary)

    write_csv(OUT / "P8_Y5_R10_647_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_647_CHIX_DEFINITION_ATTEMPT.csv", chi_rows)
    write_csv(OUT / "P8_Y5_R10_647_TAU_CLOCK_MAP.csv", tau_rows)
    write_csv(OUT / "P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv", product_rows)
    write_csv(OUT / "P8_Y5_R10_647_H0_NORMALIZED_DIAGNOSTIC.csv", h0_rows)
    write_csv(OUT / "P8_Y5_R10_647_TAU_REQUIREMENT_DIAGNOSTIC.csv", tau_req_rows)
    write_csv(OUT / "P8_Y5_R10_647_READINESS_GATES.csv", gate_rows)
    write_csv(OUT / "P8_Y5_BRR545_647_DECISION.csv", decision)
    write_csv(OUT / "P8_Y5_R10_647_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_BRR545_647_VALIDATION.csv", validation)
    write_doc(source_rows, chi_rows, tau_rows, product_rows, h0_rows, tau_req_rows, gate_rows, decision, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote_doc={DOC_PATH}")
    print(f"wrote_csv_dir={OUT}")
    print(f"product_bound_rows={len(product_rows)}")
    print("strongest_bound_product_1sigma_yr_inv=2.1e-18")
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
