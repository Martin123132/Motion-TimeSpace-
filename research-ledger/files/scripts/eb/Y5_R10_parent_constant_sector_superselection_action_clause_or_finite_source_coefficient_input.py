from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "949-Y5-R10-parent-constant-sector-superselection-action-clause-or-finite-source-coefficient-input.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def parse_float(value: str) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "948_doc",
            "path": "948-Y5-R10-clock-WEP-product-bound-runner-or-constant-superselection-no-marker-theorem.md",
            "role": "handoff: theorem clean but unsigned, runners executable nonclaim",
            "needle": "derive-zero route: clean but unsigned",
        },
        {
            "source_id": "948_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_948_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V948_14_validation_rows_ready",
        },
        {
            "source_id": "948_next_target",
            "path": "source-intake/mts_residuals/P8_Y5_R10_948_NEXT_TARGET.csv",
            "role": "949 target selection",
            "needle": "949-Y5-R10-parent-constant-sector-superselection-action-clause-or-finite-source-coefficient-input.md",
        },
        {
            "source_id": "948_theorem_attempt",
            "path": "source-intake/mts_residuals/P8_Y5_R10_948_CONSTANT_SUPERSELECTION_THEOREM_ATTEMPT.csv",
            "role": "constant-superselection theorem attempt and countermodel",
            "needle": "CST948_4_countermodel",
        },
        {
            "source_id": "948_clock_runner",
            "path": "source-intake/mts_residuals/P8_Y5_R10_948_CLOCK_PRODUCT_BOUND_RUNNER.csv",
            "role": "clock product-bound runner",
            "needle": "CLK948_1_CAS646_1_YbE3E2",
        },
        {
            "source_id": "948_WEP_runner",
            "path": "source-intake/mts_residuals/P8_Y5_R10_948_WEP_PRODUCT_BOUND_RUNNER.csv",
            "role": "WEP source-product runner",
            "needle": "WEP948_1_WAS651_1_surface_binding",
        },
        {
            "source_id": "948_scoreboard",
            "path": "source-intake/mts_residuals/P8_Y5_R10_948_PRODUCT_BOUND_SCOREBOARD.csv",
            "role": "product-bound scoreboard",
            "needle": "PBS948_2_zero_theorem",
        },
        {
            "source_id": "no_species_contract",
            "path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
            "role": "S0-S4 parent clause blockers",
            "needle": "S4_source_normalization_species_blind",
        },
        {
            "source_id": "763_no_marker_spurion",
            "path": "source-intake/mts_residuals/P8_Y5_R10_763_NO_MARKER_SPURION_THEOREM_ATTEMPT.csv",
            "role": "marker/source-weight blockers",
            "needle": "NMS763_6_verdict",
        },
    ]
    rows = []
    for spec in specs:
        path = source_path(spec["path"])
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def parent_clause_attempt() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "PCA949_0_variational_domain",
            "clause": "ordinary constants are external labels, not parent fields",
            "mathematical_contract": "delta theta_univ=0 for all parent variations; theta_univ notin Field(S_parent)",
            "would_close": "constant-sector vertical leakage",
            "current_status": "candidate_parent_clause_not_derived",
            "remaining_gap": "needs derivation from parent construction, not insertion by convenience",
            "adopt_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PCA949_1_matter_factorization",
            "clause": "ordinary matter sees only observed quotient geometry and universal constants",
            "mathematical_contract": "S_m=sum_A S_A[Psi_A, e_obs(q(Phi)), omega(e_obs), theta_univ]",
            "would_close": "direct marker/frame dependence in matter action",
            "current_status": "candidate_parent_clause_not_derived",
            "remaining_gap": "parent-selected e_obs functor and quotient-only matter frame still need proof",
            "adopt_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PCA949_2_source_universality",
            "clause": "source normalization has one universal Hilbert/coframe current",
            "mathematical_contract": "S_source=kappa_univ int e_obs J_univ with J_univ=sum_A T_A and delta kappa_univ=0",
            "would_close": "species-weighted WEP source charge",
            "current_status": "candidate_parent_clause_not_derived",
            "remaining_gap": "measured-GM/source-current universality must be parent-owned",
            "adopt_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PCA949_3_no_marker_extension",
            "clause": "no matter-visible marker may enter the parent matter/source/readout stack",
            "mathematical_contract": "partial_m S_parent=0 for every matter-visible marker m unless m is retained as explicit physical residual",
            "would_close": "countermodel theta_A=theta_0 exp(epsilon m_A)",
            "current_status": "candidate_parent_clause_not_derived",
            "remaining_gap": "must rule out co-moving/material markers without erasing legitimate physical residuals",
            "adopt_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PCA949_4_total_clause",
            "clause": "constant/source no-marker parent action clause closes clock and WEP zero route",
            "mathematical_contract": "PCA949_0..PCA949_3 imply b_A=0 and kappa_alpha*tau_clock_time=0",
            "would_close": "clock/WEP product leakage",
            "current_status": "not_parent_signed",
            "remaining_gap": "current evidence supports a clean clause candidate, not a derived theorem",
            "adopt_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def finite_coefficient_input_schema() -> list[dict[str, str]]:
    clock_rows = read_csv(OUT / "P8_Y5_R10_948_CLOCK_PRODUCT_BOUND_RUNNER.csv")
    wep_rows = read_csv(OUT / "P8_Y5_R10_948_WEP_PRODUCT_BOUND_RUNNER.csv")
    yb = next(row for row in clock_rows if row["run_id"].startswith("CLK948_1"))
    alhg = next(row for row in clock_rows if row["run_id"].startswith("CLK948_0"))
    surface = next(row for row in wep_rows if row["run_id"].startswith("WEP948_1"))
    coulomb = next(row for row in wep_rows if row["run_id"].startswith("WEP948_0"))
    specs = [
        (
            "FCI949_0_clock_yb_product",
            "kappa_alpha_tau_clock_time",
            "clock alpha drift / Yb E3-E2",
            "yr^-1",
            yb["bound_1sigma_abs"],
            "P8_Y5_R10_948_CLOCK_PRODUCT_BOUND_RUNNER.csv::CLK948_1_CAS646_1_YbE3E2",
        ),
        (
            "FCI949_1_clock_alhg_product",
            "kappa_alpha_tau_clock_time",
            "clock alpha drift / Al-Hg",
            "yr^-1",
            alhg["bound_1sigma_abs"],
            "P8_Y5_R10_948_CLOCK_PRODUCT_BOUND_RUNNER.csv::CLK948_0_CAS646_0_AlHg",
        ),
        (
            "FCI949_2_WEP_surface_beta_source",
            "beta_source_normalized",
            "MICROSCOPE WEP / surface-binding diagnostic",
            "dimensionless",
            surface["required_abs_product_max"],
            "P8_Y5_R10_948_WEP_PRODUCT_BOUND_RUNNER.csv::WEP948_1_WAS651_1_surface_binding",
        ),
        (
            "FCI949_3_WEP_coulomb_beta_source",
            "beta_source_normalized",
            "MICROSCOPE WEP / alpha-Coulomb diagnostic",
            "dimensionless",
            coulomb["required_abs_product_max"],
            "P8_Y5_R10_948_WEP_PRODUCT_BOUND_RUNNER.csv::WEP948_0_WAS651_0_alpha_Coulomb",
        ),
        (
            "FCI949_4_zero_theorem_switch",
            "constant_source_zero_theorem",
            "clock and WEP zero route",
            "boolean",
            "true_required_for_zero_claim",
            "P8_Y5_R10_948_CONSTANT_SUPERSELECTION_THEOREM_ATTEMPT.csv::CST948_5_total_verdict",
        ),
    ]
    rows = []
    for input_id, symbol, arena, units, bound, bound_source in specs:
        rows.append(
            {
                "input_id": input_id,
                "coefficient_symbol": symbol,
                "arena": arena,
                "units": units,
                "required_input_value": "MISSING_PARENT_INPUT",
                "comparison_bound": bound,
                "comparison_rule": "abs(required_input_value) <= comparison_bound" if units != "boolean" else "zero theorem must be parent-signed true",
                "bound_source": bound_source,
                "source_bound_ready": flag(bound not in {"", "MISSING", "not_applicable"}),
                "input_ready": "false",
                "score_ready": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def product_runner_readiness(input_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    clock_bounds = [parse_float(row["comparison_bound"]) for row in input_rows if row["coefficient_symbol"] == "kappa_alpha_tau_clock_time"]
    clock_bounds = [bound for bound in clock_bounds if bound is not None]
    wep_bounds = [parse_float(row["comparison_bound"]) for row in input_rows if row["coefficient_symbol"] == "beta_source_normalized"]
    wep_bounds = [bound for bound in wep_bounds if bound is not None]
    return [
        {
            "readiness_id": "PRR949_0_clock",
            "runner": "clock product-bound runner",
            "strongest_loaded_bound": "" if not clock_bounds else f"{min(clock_bounds):.12e}",
            "units": "yr^-1",
            "needed_to_score": "finite numeric kappa_alpha_tau_clock_time or parent-signed zero theorem",
            "current_status": "INPUT_SCHEMA_READY_SOURCE_BOUND_READY_MTS_INPUT_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "readiness_id": "PRR949_1_WEP",
            "runner": "WEP source-product runner",
            "strongest_loaded_bound": "" if not wep_bounds else f"{min(wep_bounds):.12e}",
            "units": "dimensionless",
            "needed_to_score": "finite numeric beta_source_normalized or parent-signed species/source zero theorem",
            "current_status": "INPUT_SCHEMA_READY_SOURCE_BOUND_READY_MTS_INPUT_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "readiness_id": "PRR949_2_zero_route",
            "runner": "constant/source zero theorem",
            "strongest_loaded_bound": "zero_if_parent_signed",
            "units": "coefficient",
            "needed_to_score": "parent derivation of PCA949_0..PCA949_3, not a closure insertion",
            "current_status": "CLAUSE_CANDIDATE_READY_NOT_PARENT_SIGNED",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC949_0_parent_clause",
            "topic": "constant/source parent action clause",
            "result": "clean_candidate_written_not_adopted",
            "reason": "the clause would close the clock/WEP zero route, but adopting it now would be an axiom insertion rather than a derivation from the parent action",
            "next_action": "try to derive source-normalization species blindness or mark finite coefficients as empirical inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC949_1_finite_input_schema",
            "topic": "finite coefficient input schema",
            "result": "schema_ready_nonclaim",
            "reason": "clock and WEP runners now have explicit fields for future MTS coefficients and comparison bounds",
            "next_action": "build first candidate-value smoke runner only after a parent coefficient or deliberately labelled closure value exists",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE949_0_parent_clause_adoption",
            "claim": "constant/source no-marker clause is part of the derived parent theory",
            "required_condition": "derive PCA949_0..PCA949_3 from the parent action, not add them as convenience constraints",
            "current_evidence": "candidate clause only",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE949_1_product_score",
            "claim": "clock/WEP product runners can score MTS predictions now",
            "required_condition": "replace MISSING_PARENT_INPUT with sourced numeric coefficient or parent-signed zero theorem",
            "current_evidence": "input schema ready, inputs missing",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "950-Y5-R10-source-normalization-species-blind-zero-lemma-or-first-finite-coefficient-smoke-run.md",
            "objective": "try to derive the species-blind source-normalization lemma that would close WEP beta_source, or run a first explicitly labelled finite-coefficient smoke test using the 949 schema if a candidate value is supplied",
            "include": "source current universality, measured-GM normalization, WEP beta_source schema, clock product schema, zero-vs-finite branch labels",
            "exclude": "unstated coefficient values, local-GR pass claim, WEP/clock claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            changed += 1
    return changed


def validation(
    sources: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    input_rows: list[dict[str, str]],
    readiness_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, passes: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passes else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_clean = all(row.get("result") == "pass" for row in read_csv(OUT / "P8_Y5_BRR545_948_VALIDATION.csv"))
    clause_not_adopted = all(row["adopt_now"] == "false" for row in clause_rows)
    total_clause_blocked = any(row["clause_id"] == "PCA949_4_total_clause" and row["current_status"] == "not_parent_signed" for row in clause_rows)
    schema_ready = len(input_rows) == 5 and all(row["source_bound_ready"] == "true" for row in input_rows)
    inputs_missing = all(row["input_ready"] == "false" and row["score_ready"] == "false" for row in input_rows)
    readiness_nonclaim = all(row["score_ready"] == "false" for row in readiness_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" for row in decision_rows)
    claim_gates_false = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    target_selected = target_rows and target_rows[0]["next_target"].startswith("950-")
    valid_for_claim_false = all(
        row.get("valid_for_claim") == "false"
        for table in [sources, clause_rows, input_rows, readiness_rows, decision_rows, claim_rows, target_rows]
        for row in table
    )
    formalization_changed = formalization_changed_after_start()

    add("V949_0_sources_exist_and_needles", sources_ok, "all 949 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V949_1_prior_948_clean", prior_clean, "P8_Y5_BRR545_948_VALIDATION.csv clean")
    add("V949_2_parent_clause_not_adopted", clause_not_adopted, "all parent clause rows remain candidate only")
    add("V949_3_total_clause_blocked", total_clause_blocked, "total constant/source clause remains not parent-signed")
    add("V949_4_input_schema_ready", schema_ready, "finite coefficient input schema has expected rows and source bounds")
    add("V949_5_inputs_missing_nonclaim", inputs_missing, "no placeholder input is score-ready")
    add("V949_6_readiness_nonclaim", readiness_nonclaim, "runner readiness rows remain nonclaim")
    add("V949_7_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V949_8_claim_gates_false", claim_gates_false, "all claim gates remain false")
    add("V949_9_next_target_selected", target_selected, "950 source-normalization or finite coefficient smoke target selected")
    add("V949_10_no_claims_promoted", valid_for_claim_false, "all generated rows are valid_for_claim=false")
    add("V949_11_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V949_12_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    input_rows: list[dict[str, str]],
    readiness_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 949 Y5 R10: Parent Constant-Sector Superselection Action Clause Or Finite Source-Coefficient Input

Status: `Y5_R10_949_parent_clause_candidate_and_finite_input_schema_written_nonclaim`

Claim ceiling: `candidate_clause_only_input_schema_only_no_product_score_no_local_GR_claim`

## Result

This checkpoint made the 948 fork explicit. There are now two honest routes:

1. **Zero route:** derive a parent-action clause saying ordinary constants/source weights are superselection labels, matter factors through observed quotient geometry, and no matter-visible marker enters the readout stack.
2. **Finite route:** keep `kappa_alpha*tau_clock_time` and `beta_source_normalized` as explicit finite coefficients and compare them to the clock/WEP product bounds.

The zero route is still not claimed. The parent clause is written as a candidate contract, not adopted as a derived part of the theory. The finite route now has a clean input schema, but every input remains `MISSING_PARENT_INPUT`.

```text
we now know exactly what number or theorem the next step must supply;
no hidden coefficient, no silent closure, no WEP/clock/local-GR claim.
```

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Parent Clause Attempt

{md_table(clause_rows, ["clause_id", "clause", "mathematical_contract", "current_status", "remaining_gap", "adopt_now"])}

## Finite Coefficient Input Schema

{md_table(input_rows, ["input_id", "coefficient_symbol", "arena", "required_input_value", "comparison_bound", "comparison_rule", "score_ready"])}

## Product Runner Readiness

{md_table(readiness_rows, ["readiness_id", "runner", "strongest_loaded_bound", "needed_to_score", "current_status", "score_ready"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    clause_rows = parent_clause_attempt()
    input_rows = finite_coefficient_input_schema()
    readiness_rows = product_runner_readiness(input_rows)
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, clause_rows, input_rows, readiness_rows, decision_rows, claim_rows, target_rows)

    write_csv(
        OUT / "P8_Y5_R10_949_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_949_PARENT_CLAUSE_ATTEMPT.csv",
        clause_rows,
        [
            "clause_id",
            "clause",
            "mathematical_contract",
            "would_close",
            "current_status",
            "remaining_gap",
            "adopt_now",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_949_FINITE_COEFFICIENT_INPUT_SCHEMA.csv",
        input_rows,
        [
            "input_id",
            "coefficient_symbol",
            "arena",
            "units",
            "required_input_value",
            "comparison_bound",
            "comparison_rule",
            "bound_source",
            "source_bound_ready",
            "input_ready",
            "score_ready",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_949_PRODUCT_RUNNER_READINESS.csv",
        readiness_rows,
        [
            "readiness_id",
            "runner",
            "strongest_loaded_bound",
            "units",
            "needed_to_score",
            "current_status",
            "score_ready",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_949_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_949_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_949_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_949_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, clause_rows, input_rows, readiness_rows, decision_rows, claim_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()
