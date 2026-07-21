from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import Y5_R2FR_4897_metric_baseline_reentry as research  # noqa: E402


TIMESTAMP = datetime.now(timezone.utc).isoformat()
NEXT_TARGET = research.NEXT_TARGET


def serializable(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(
            value, sort_keys=True, separators=(",", ":"), default=str
        )
    if hasattr(value, "item"):
        return value.item()
    return value


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows:
        normalized = {key: serializable(value) for key, value in row.items()}
        normalized["valid_for_claim"] = False
        normalized["timestamp_utc"] = TIMESTAMP
        output.append(normalized)
    return output


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def compile_source(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except SyntaxError:
        return False
    return True


def scalar_summary(section: dict[str, Any], excluded: set[str]) -> dict[str, Any]:
    return {key: value for key, value in section.items() if key not in excluded}


def source_rows() -> list[dict[str, Any]]:
    rows = [dict(row) for row in research.source_contract()["rows"]]
    outputs = [
        (
            "SRC4897_06_checkpoint",
            POST
            / "4897-Y5-R2FR-cosmology-without-bath-source-metric-only-baseline-and-derived-extension-reentry-gate.md",
            "MTS_METRIC_ONLY_BASELINE_REENTRY_GATE_4897",
        ),
        (
            "SRC4897_07_formal",
            FORMAL
            / "913-PPC4161-metric-only-cosmology-baseline-and-extension-reentry.md",
            "PPC4161_METRIC_BASELINE_REENTRY_4897",
        ),
        (
            "SRC4897_08_claim",
            FORMAL / "02-claims-register.csv",
            "L-739",
        ),
        (
            "SRC4897_09_variables",
            FORMAL / "04-variable-audit.csv",
            "Priority4897_MTS",
        ),
        (
            "SRC4897_10_equations",
            FORMAL / "05-equation-register.md",
            "1.190 Metric-only baseline",
        ),
        (
            "SRC4897_11_redteam",
            FORMAL / "06-consistency-red-team.md",
            "141. A known-limit fallback",
        ),
        (
            "SRC4897_12_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4897",
        ),
        (
            "SRC4897_13_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_METRIC_BASELINE_REENTRY_4897",
        ),
        (
            "SRC4897_14_research",
            SCRIPTS / "Y5_R2FR_4897_metric_baseline_reentry.py",
            "def metric_only_baseline",
        ),
        (
            "SRC4897_15_gate",
            SCRIPTS / "Y5_R2FR_4897_metric_baseline_reentry_gate.py",
            "VAL4897_OVERALL",
        ),
    ]
    for source_id, path, marker in outputs:
        exists = path.exists()
        content = (
            path.read_text(encoding="utf-8", errors="replace")
            if exists
            else ""
        )
        rows.append(
            {
                "source_id": source_id,
                "source_type": "generated_local_text_or_code",
                "source_path": str(path),
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker in content,
            }
        )
    return tagged(rows)


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    baseline = sections["baseline"]
    quarantine = sections["quarantine"]
    reentry = sections["reentry"]
    priority = sections["priority"]
    arbitration = sections["arbitration"]
    return {
        "BASELINE_EVOLUTION": tagged(baseline["rows"]),
        "BASELINE_SUMMARY": tagged([scalar_summary(baseline, {"rows"})]),
        "COSMOLOGY_QUARANTINE": tagged(quarantine["rows"]),
        "QUARANTINE_SUMMARY": tagged(
            [scalar_summary(quarantine, {"rows"})]
        ),
        "REENTRY_CLAUSES": tagged(reentry["rows"]),
        "REENTRY_SUMMARY": tagged([scalar_summary(reentry, {"rows"})]),
        "PRIORITY_REDIRECT": tagged(priority["rows"]),
        "PRIORITY_SUMMARY": tagged([scalar_summary(priority, {"rows"})]),
        "ARBITRATION": tagged([arbitration]),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "retired_bath_outputs_status": arbitration[
                        "retired_bath_outputs_status"
                    ],
                    "local_GR_Newton_Maxwell_status": arbitration[
                        "local_GR_Newton_Maxwell_status"
                    ],
                    "selected_next_target": arbitration[
                        "selected_next_target"
                    ],
                    "next_target": arbitration["next_target"],
                    "all_checks_pass": calculation["all_checks_pass"],
                }
            ]
        ),
    }


def validation_rows(
    calculation: dict[str, Any],
    sources: list[dict[str, Any]],
    groups: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    def check(check_id: str, condition: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    sections = calculation["sections"]
    baseline = sections["baseline"]
    quarantine = sections["quarantine"]
    reentry = sections["reentry"]
    priority = sections["priority"]
    arbitration = sections["arbitration"]
    previous_validation = read_csv(
        OUTPUT / "P8_Y5_BRR545_4896_VALIDATION.csv"
    )
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-739"
    ]
    variable_symbols = (
        "GammaBase4897_MTS",
        "EBase4897_MTS",
        "QBase4897_MTS",
        "CosmoQuarantine4897_MTS",
        "Reentry4897_MTS",
        "GNstatus4897_MTS",
        "Priority4897_MTS",
    )
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    new_variables = [
        row for row in variable_rows if row["symbol"] in variable_symbols
    ]
    variable_counts = {
        symbol: sum(row["symbol"] == symbol for row in variable_rows)
        for symbol in variable_symbols
    }
    variable_sources_exist = True
    for row in new_variables:
        for source_path in row["source_files"].split(";"):
            variable_sources_exist = (
                variable_sources_exist and (ROOT / source_path).exists()
            )
    checkpoint = (
        POST
        / "4897-Y5-R2FR-cosmology-without-bath-source-metric-only-baseline-and-derived-extension-reentry-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL
        / "913-PPC4161-metric-only-cosmology-baseline-and-extension-reentry.md"
    ).read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(
        encoding="utf-8"
    )
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(
        encoding="utf-8"
    )
    spine = (FORMAL / "07-unification-spine.md").read_text(
        encoding="utf-8"
    )
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    all_rows = sources + [row for rows in groups.values() for row in rows]
    output_paths = [
        OUTPUT / "P8_Y5_R2FR_4897_SOURCE_REGISTER.csv",
        *[
            OUTPUT / f"P8_Y5_R2FR_4897_{name}.csv" for name in groups
        ],
    ]
    bath_rows = [
        row
        for row in reentry["rows"]
        if row["candidate"] == "retired_gamma1_sigma0p3_diagonal_bath"
    ]
    rows = [
        check(
            "VAL4897_00_prior",
            bool(previous_validation)
            and previous_validation[-1]["check_id"] == "VAL4896_OVERALL"
            and previous_validation[-1]["status"] == "PASS",
            "4896 validation inherited",
        ),
        check(
            "VAL4897_01_sources",
            sections["sources"]["passed"]
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            "all prior and generated source markers exist",
        ),
        check(
            "VAL4897_02_baseline",
            baseline["passed"]
            and baseline["known_limit_baseline"]
            and not baseline["novel_cosmology_prediction"],
            "metric-only branch is an active known-limit baseline",
        ),
        check(
            "VAL4897_03_baseline_rows",
            len(baseline["rows"]) == 9
            and abs(baseline["rows"][-1]["E"] - 1.0) < 1.0e-14,
            "nine conserved baseline epochs generated",
        ),
        check(
            "VAL4897_04_conservation",
            all(
                row["Q_total"] == 0.0
                and abs(row["Friedmann_fraction_sum"] - 1.0) < 1.0e-14
                for row in baseline["rows"]
            ),
            "baseline exchange and Friedmann residuals vanish",
        ),
        check(
            "VAL4897_05_lambda",
            1.08e-52 < baseline["Lambda_cal_per_square_metre"] < 1.10e-52
            and "not_MTS_prediction" in baseline["Lambda_status"],
            "single Lambda calibration is explicit",
        ),
        check(
            "VAL4897_06_GN",
            "measured_calibration" in baseline["GN_status"]
            and "8 pi" in baseline["Newton_constant"],
            "Newton strength remains calibrated",
        ),
        check(
            "VAL4897_07_local_values",
            baseline["PPN_gamma"] == 1.0
            and baseline["PPN_beta"] == 1.0
            and "Poynting" in baseline["Maxwell_stress"],
            "PPN and Maxwell/Poynting baseline retained",
        ),
        check(
            "VAL4897_08_quarantine",
            quarantine["passed"]
            and quarantine["quarantined_claims"] == 10
            and quarantine["claimable_parent_cosmology_rows"] == 0,
            "ten historical bath claims quarantined",
        ),
        check(
            "VAL4897_09_quarantine_ids",
            [row["claim_id"] for row in quarantine["rows"]]
            == [f"L-{number}" for number in range(729, 739)],
            "quarantine covers exactly L-729 through L-738",
        ),
        check(
            "VAL4897_10_authoritative",
            quarantine["authoritative_retirement_rows"] == 1
            and next(
                row
                for row in quarantine["rows"]
                if row["authoritative_decision_claim"]
            )["claim_id"]
            == "L-738",
            "L-738 is the unique authoritative retirement row",
        ),
        check(
            "VAL4897_11_method_reuse",
            all(row["eligible_for_method_reuse"] for row in quarantine["rows"]),
            "failed-route methods remain reusable",
        ),
        check(
            "VAL4897_12_reentry_rows",
            reentry["passed"]
            and len(reentry["rows"]) == 20
            and reentry["clauses_per_candidate"] == 10,
            "ten all-or-nothing clauses applied to two candidates",
        ),
        check(
            "VAL4897_13_bath_reentry",
            not reentry["retired_bath_reentry_allowed"]
            and reentry["retired_bath_passed_clauses"] == 6,
            "retired bath cannot re-enter",
        ),
        check(
            "VAL4897_14_bath_failures",
            {row["clause"] for row in bath_rows if not row["passes"]}
            == {
                "early_gravity_limit",
                "derived_activation_amplitude",
                "finite_k_species_completion",
                "fair_empirical_score",
            },
            "four bath re-entry failures are explicit",
        ),
        check(
            "VAL4897_15_future_reentry",
            not reentry["future_extension_reentry_allowed"]
            and "AND" in reentry["gate_logic"],
            "no unspecified future candidate is pre-approved",
        ),
        check(
            "VAL4897_16_priority_rows",
            priority["passed"]
            and len(priority["rows"]) == 5
            and [row["rank"] for row in priority["rows"]] == [1, 2, 3, 4, 5],
            "five post-retirement priorities ranked",
        ),
        check(
            "VAL4897_17_priority_selection",
            priority["selected_target"]
            == "microscopic_Planck_stiffness_and_GN_owner"
            and sum(row["selected_next"] for row in priority["rows"]) == 1,
            "Planck stiffness and G_N ownership selected",
        ),
        check(
            "VAL4897_18_arbitration",
            arbitration["passed"]
            and arbitration["metric_only_cosmology_status"]
            == "ACTIVE_KNOWN_LIMIT_BASELINE_NOT_NOVEL_MTS_COSMOLOGY_PREDICTION",
            "baseline arbitration passes",
        ),
        check(
            "VAL4897_19_local_chain",
            arbitration["local_GR_Newton_Maxwell_status"]
            == "RETAIN_4875_4879_4880_CONDITIONAL_CERTIFICATES",
            "local GR Newton Maxwell chain retained",
        ),
        check(
            "VAL4897_20_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "metric_only_known_limit_active_retired_bath_outputs_quarantined_extension_reentry_locked_GN_microscopic_owner_selected_private_nonclaim",
            "L-739 unique private nonclaim status",
        ),
        check(
            "VAL4897_21_variables",
            len(new_variables) == 7
            and all(variable_counts[symbol] == 1 for symbol in variable_symbols),
            "seven checkpoint variables are unique",
        ),
        check(
            "VAL4897_22_variable_sources",
            variable_sources_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4897_23_documents",
            "MTS_METRIC_ONLY_BASELINE_REENTRY_GATE_4897" in checkpoint
            and "PPC4161_METRIC_BASELINE_REENTRY_4897" in formal_note,
            "checkpoint and formal markers exist",
        ),
        check(
            "VAL4897_24_registers",
            "1.190 Metric-only baseline" in equations
            and "141. A known-limit fallback" in redteam
            and "PPC4161 checkpoint 4897" in spine,
            "equation red-team and spine registers updated",
        ),
        check(
            "VAL4897_25_resume",
            "PPC4161_METRIC_BASELINE_REENTRY_4897" in resume
            and NEXT_TARGET in resume,
            "resume and 4898 handoff updated",
        ),
        check(
            "VAL4897_26_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4897_27_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4897_28_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4897_29_scripts",
            compile_source(SCRIPTS / "Y5_R2FR_4897_metric_baseline_reentry.py")
            and compile_source(
                SCRIPTS / "Y5_R2FR_4897_metric_baseline_reentry_gate.py"
            ),
            "research and gate scripts compile",
        ),
        check(
            "VAL4897_30_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no post-checkpoint script pycache",
        ),
        check(
            "VAL4897_31_next",
            NEXT_TARGET in checkpoint
            and priority["next_target"] == NEXT_TARGET
            and arbitration["next_target"] == NEXT_TARGET,
            "4898 microscopic G_N owner target selected",
        ),
        check(
            "VAL4897_32_overall_internal",
            calculation["all_checks_pass"],
            "4897 calculation internally passes",
        ),
    ]
    rows.append(
        check(
            "VAL4897_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_METRIC_ONLY_BASELINE_REENTRY_GATE_4897_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4897_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4897_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4897_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4897_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4897_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
