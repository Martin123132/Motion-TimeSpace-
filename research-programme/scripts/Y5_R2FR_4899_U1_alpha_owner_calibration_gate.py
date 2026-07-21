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

import Y5_R2FR_4899_U1_alpha_owner_calibration as research  # noqa: E402


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
            "SRC4899_14_checkpoint",
            POST
            / "4899-Y5-R2FR-primitive-U1-normalization-and-Maxwell-charge-calibration-versus-alpha-prediction-gate.md",
            "MTS_U1_ALPHA_CALIBRATION_AND_BANDWIDTH_REJECTION_GATE_4899",
        ),
        (
            "SRC4899_15_formal",
            FORMAL
            / "915-PPC4161-U1-normalization-alpha-calibration-and-bandwidth-rejection.md",
            "PPC4161_U1_ALPHA_CALIBRATION_AND_BANDWIDTH_REJECTION_4899",
        ),
        (
            "SRC4899_16_claim",
            FORMAL / "02-claims-register.csv",
            "L-741",
        ),
        (
            "SRC4899_17_variables",
            FORMAL / "04-variable-audit.csv",
            "AlphaPredict4899_MTS",
        ),
        (
            "SRC4899_18_equations",
            FORMAL / "05-equation-register.md",
            "1.192 U1 normalization orbit",
        ),
        (
            "SRC4899_19_redteam",
            FORMAL / "06-consistency-red-team.md",
            "143. Charge quantization is not coupling quantization",
        ),
        (
            "SRC4899_20_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4899",
        ),
        (
            "SRC4899_21_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_U1_ALPHA_CALIBRATION_AND_BANDWIDTH_REJECTION_4899",
        ),
        (
            "SRC4899_22_research",
            SCRIPTS / "Y5_R2FR_4899_U1_alpha_owner_calibration.py",
            "def normalization_theorem",
        ),
        (
            "SRC4899_23_gate",
            SCRIPTS / "Y5_R2FR_4899_U1_alpha_owner_calibration_gate.py",
            "VAL4899_OVERALL",
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
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker in content,
                "source_checked_date": "2026-07-11",
            }
        )
    return tagged(rows)


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    owners = sections["owners"]
    normalization = sections["normalization"]
    lattice = sections["lattice"]
    calibration = sections["calibration"]
    bandwidth = sections["bandwidth"]
    baseline = sections["baseline"]
    reentry = sections["prediction_reentry"]
    arbitration = sections["arbitration"]
    return {
        "EM_OWNER_AUDIT": tagged(owners["rows"]),
        "EM_OWNER_SUMMARY": tagged([scalar_summary(owners, {"rows"})]),
        "NORMALIZATION_THEOREM": tagged([normalization]),
        "CHARGE_LATTICE": tagged(lattice["rows"]),
        "CHARGE_LATTICE_SUMMARY": tagged(
            [scalar_summary(lattice, {"rows"})]
        ),
        "CODATA_ALPHA": tagged(calibration["rows"]),
        "CODATA_ALPHA_SUMMARY": tagged(
            [scalar_summary(calibration, {"rows"})]
        ),
        "BANDWIDTH_SPECTRUM": tagged(bandwidth["spectrum_rows"]),
        "BANDWIDTH_PROJECTIONS": tagged(bandwidth["projection_rows"]),
        "BANDWIDTH_AUDIT": tagged(bandwidth["audit_rows"]),
        "BANDWIDTH_SUMMARY": tagged(
            [
                scalar_summary(
                    bandwidth,
                    {"spectrum_rows", "projection_rows", "audit_rows"},
                )
            ]
        ),
        "BASELINE_ARENA_REUSE": tagged(baseline["rows"]),
        "BASELINE_CONSTANCY": tagged([scalar_summary(baseline, {"rows"})]),
        "PREDICTION_REENTRY": tagged(reentry["rows"]),
        "PREDICTION_REENTRY_SUMMARY": tagged(
            [scalar_summary(reentry, {"rows"})]
        ),
        "ARBITRATION": tagged([arbitration]),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "Maxwell_correspondence_status": arbitration[
                        "Maxwell_correspondence_status"
                    ],
                    "microscopic_alpha_prediction_status": arbitration[
                        "microscopic_alpha_prediction_status"
                    ],
                    "archived_bandwidth_status": arbitration[
                        "archived_bandwidth_status"
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
    owners = sections["owners"]
    normalization = sections["normalization"]
    lattice = sections["lattice"]
    calibration = sections["calibration"]
    bandwidth = sections["bandwidth"]
    baseline = sections["baseline"]
    reentry = sections["prediction_reentry"]
    arbitration = sections["arbitration"]
    previous_validation = read_csv(
        OUTPUT / "P8_Y5_BRR545_4898_VALIDATION.csv"
    )
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-741"
    ]
    variable_symbols = (
        "ZA4899_MTS",
        "gJ4899_MTS",
        "eR4899_MTS",
        "alphaCal4899_MTS",
        "NormOrbit4899_MTS",
        "ChargeLattice4899_MTS",
        "bAlpha4899_MTS",
        "Bandwidth4899_MTS",
        "AlphaPredict4899_MTS",
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
        / "4899-Y5-R2FR-primitive-U1-normalization-and-Maxwell-charge-calibration-versus-alpha-prediction-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL
        / "915-PPC4161-U1-normalization-alpha-calibration-and-bandwidth-rejection.md"
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
        OUTPUT / "P8_Y5_R2FR_4899_SOURCE_REGISTER.csv",
        *[OUTPUT / f"P8_Y5_R2FR_4899_{name}.csv" for name in groups],
    ]
    noncircular_projection_rows = [
        row
        for row in bandwidth["projection_rows"]
        if not row["constructed_from_observed_alpha"]
    ]
    rows = [
        check(
            "VAL4899_00_prior",
            bool(previous_validation)
            and previous_validation[-1]["check_id"] == "VAL4898_OVERALL"
            and previous_validation[-1]["status"] == "PASS",
            "4898 validation inherited",
        ),
        check(
            "VAL4899_01_sources",
            sections["sources"]["passed"]
            and all(
                row["source_exists"] and row["marker_found"] for row in sources
            ),
            "all parent legacy and official source markers exist",
        ),
        check(
            "VAL4899_02_owner_rows",
            owners["passed"]
            and owners["owner_rows"] == 8
            and owners["structurally_closed_rows"] == 4,
            "eight EM owner rows separate four structural closures",
        ),
        check(
            "VAL4899_03_owner_paths",
            owners["all_source_paths_exist"],
            "all owner source paths exist",
        ),
        check(
            "VAL4899_04_prediction_not_ready",
            not owners["microscopic_alpha_prediction_ready"],
            "microscopic alpha prediction remains blocked",
        ),
        check(
            "VAL4899_05_normalization",
            normalization["passed"]
            and normalization["invariant"] == "g_J^2/Z_A"
            and "4 pi" in normalization["physical_coupling"],
            "canonical U1 normalization theorem closes",
        ),
        check(
            "VAL4899_06_orbit",
            normalization["jacobian_rank"] == 1
            and normalization["normalization_orbit_nullity"] == 1
            and normalization["null_check"] == 0.0,
            "field-rescaling orbit is the exact null direction",
        ),
        check(
            "VAL4899_07_topology",
            lattice["passed"]
            and lattice["compactness_can_quantize_relative_labels"]
            and not lattice["compactness_fixes_absolute_charge_unit"]
            and not lattice["topology_fixes_alpha_without_kinetic_inheritance"],
            "charge quantization is separated from coupling quantization",
        ),
        check(
            "VAL4899_08_CODATA",
            calibration["passed"]
            and calibration["latest_available_set_as_of_check"]
            == "CODATA_2022"
            and calibration["calibration_count"] == 1,
            "one current official alpha calibration recorded",
        ),
        check(
            "VAL4899_09_canonical_charge",
            0.3028 < calibration["canonical_charge"] < 0.3029
            and abs(calibration["rounded_reciprocal_product_residual"])
            < 5.0e-11,
            "canonical charge and inverse-alpha crosscheck close",
        ),
        check(
            "VAL4899_10_bandwidth_envelope",
            bandwidth["passed"]
            and bandwidth["calculated_ell_99"] == 3
            and bandwidth["calculated_ell_max_one_percent_total"] == 3
            and bandwidth["calculated_ell_max_one_percent_peak"] == 3,
            "printed ell0=1.7 envelope contradicts claimed ell99 and ellmax",
        ),
        check(
            "VAL4899_11_bandwidth_projection",
            not bandwidth["noncircular_candidate_within_one_percent"]
            and not any(
                row["within_one_percent"]
                for row in noncircular_projection_rows
            ),
            "common ellmax=6 projections miss alpha by more than one percent",
        ),
        check(
            "VAL4899_12_bandwidth_circular",
            sum(
                row["constructed_from_observed_alpha"]
                for row in bandwidth["projection_rows"]
            )
            == 1
            and next(
                row
                for row in bandwidth["projection_rows"]
                if row["constructed_from_observed_alpha"]
            )["within_one_percent"],
            "only the observed-alpha-constructed suppression matches",
        ),
        check(
            "VAL4899_13_bandwidth_reproducibility",
            not bandwidth["archive_cites_machine_data_path"]
            and len(bandwidth["audit_rows"]) == 7,
            "legacy document supplies no machine data path and fails seven clauses",
        ),
        check(
            "VAL4899_14_bandwidth_status",
            bandwidth["legacy_route_status"]
            == "REJECTED_AS_CURRENT_ALPHA_DERIVATION_RETAINED_AS_ARCHIVED_HEURISTIC",
            "archived bandwidth route is classified decisively",
        ),
        check(
            "VAL4899_15_baseline",
            baseline["passed"]
            and baseline["exact_baseline_constancy"]
            and baseline["arena_specific_retunes"] == 0,
            "fixed metric-only alpha baseline is exact and unretuned",
        ),
        check(
            "VAL4899_16_baseline_drift",
            "=0" in baseline["baseline_drift_law"]
            and "2 z_g" in baseline["extended_drift_normal_form"],
            "zero baseline and live extension drift law are distinct",
        ),
        check(
            "VAL4899_17_prediction_gate",
            reentry["passed"]
            and reentry["total_clauses"] == 10
            and reentry["passed_clauses"] == 3
            and not reentry["prediction_reentry_allowed"],
            "microscopic alpha prediction gate remains closed",
        ),
        check(
            "VAL4899_18_arbitration",
            arbitration["passed"]
            and arbitration["alpha_zero_status"]
            == "ONE_GLOBAL_CODATA_CALIBRATION_NO_ARENA_RETUNING",
            "one-calibration arbitration passes",
        ),
        check(
            "VAL4899_19_Maxwell",
            arbitration["Maxwell_correspondence_status"]
            == "DERIVED_FROM_EXPLICIT_PRINCIPAL_U1_PARENT_IN_METRIC_ONLY_DOMAIN",
            "Maxwell correspondence remains derived",
        ),
        check(
            "VAL4899_20_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "U1_Maxwell_structure_derived_alpha_calibrated_once_baseline_drift_zero_bandwidth_derivation_rejected_microscopic_charge_QED_open_private_nonclaim",
            "L-741 unique private nonclaim status",
        ),
        check(
            "VAL4899_21_variables",
            len(new_variables) == 9
            and all(variable_counts[symbol] == 1 for symbol in variable_symbols),
            "nine checkpoint variables are unique",
        ),
        check(
            "VAL4899_22_variable_sources",
            variable_sources_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4899_23_documents",
            "MTS_U1_ALPHA_CALIBRATION_AND_BANDWIDTH_REJECTION_GATE_4899"
            in checkpoint
            and "PPC4161_U1_ALPHA_CALIBRATION_AND_BANDWIDTH_REJECTION_4899"
            in formal_note,
            "checkpoint and formal markers exist",
        ),
        check(
            "VAL4899_24_registers",
            "1.192 U1 normalization orbit" in equations
            and "143. Charge quantization is not coupling quantization"
            in redteam
            and "PPC4161 checkpoint 4899" in spine,
            "equation red-team and spine registers updated",
        ),
        check(
            "VAL4899_25_resume",
            "PPC4161_U1_ALPHA_CALIBRATION_AND_BANDWIDTH_REJECTION_4899"
            in resume
            and NEXT_TARGET in resume,
            "resume and 4900 handoff updated",
        ),
        check(
            "VAL4899_26_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4899_27_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4899_28_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4899_29_scripts",
            compile_source(
                SCRIPTS / "Y5_R2FR_4899_U1_alpha_owner_calibration.py"
            )
            and compile_source(
                SCRIPTS / "Y5_R2FR_4899_U1_alpha_owner_calibration_gate.py"
            ),
            "research and gate scripts compile",
        ),
        check(
            "VAL4899_30_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no post-checkpoint script pycache",
        ),
        check(
            "VAL4899_31_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4900 charged matter and QED target selected",
        ),
        check(
            "VAL4899_32_internal",
            calculation["all_checks_pass"],
            "4899 calculation internally passes",
        ),
    ]
    rows.append(
        check(
            "VAL4899_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_U1_ALPHA_CALIBRATION_AND_BANDWIDTH_REJECTION_GATE_4899_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4899_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4899_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4899_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4899_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4899_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
