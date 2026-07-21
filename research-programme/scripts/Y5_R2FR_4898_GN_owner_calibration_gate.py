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

import Y5_R2FR_4898_GN_owner_calibration as research  # noqa: E402


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
            "SRC4898_11_checkpoint",
            POST
            / "4898-Y5-R2FR-microscopic-Planck-stiffness-owner-and-GN-calibration-versus-prediction-gate.md",
            "MTS_GN_CALIBRATION_VERSUS_PREDICTION_GATE_4898",
        ),
        (
            "SRC4898_12_formal",
            FORMAL
            / "914-PPC4161-Planck-stiffness-identifiability-and-one-calibration-certificate.md",
            "PPC4161_GN_IDENTIFIABILITY_AND_CALIBRATION_4898",
        ),
        (
            "SRC4898_13_claim",
            FORMAL / "02-claims-register.csv",
            "L-740",
        ),
        (
            "SRC4898_14_variables",
            FORMAL / "04-variable-audit.csv",
            "GNpredict4898_MTS",
        ),
        (
            "SRC4898_15_equations",
            FORMAL / "05-equation-register.md",
            "1.191 Newton-stiffness identifiability",
        ),
        (
            "SRC4898_16_redteam",
            FORMAL / "06-consistency-red-team.md",
            "142. A calibration surface is not a prediction",
        ),
        (
            "SRC4898_17_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4898",
        ),
        (
            "SRC4898_18_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_GN_IDENTIFIABILITY_AND_CALIBRATION_4898",
        ),
        (
            "SRC4898_19_research",
            SCRIPTS / "Y5_R2FR_4898_GN_owner_calibration.py",
            "def identifiability_theorem",
        ),
        (
            "SRC4898_20_gate",
            SCRIPTS / "Y5_R2FR_4898_GN_owner_calibration_gate.py",
            "VAL4898_OVERALL",
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
    theorem = sections["identifiability"]
    calibration = sections["calibration"]
    rays = sections["rays"]
    source = sections["source_coupling"]
    reentry = sections["prediction_reentry"]
    arbitration = sections["arbitration"]
    return {
        "MICRO_OWNER_AUDIT": tagged(owners["rows"]),
        "MICRO_OWNER_SUMMARY": tagged([scalar_summary(owners, {"rows"})]),
        "IDENTIFIABILITY": tagged([theorem]),
        "CODATA_CALIBRATION": tagged(calibration["rows"]),
        "CODATA_SUMMARY": tagged([scalar_summary(calibration, {"rows"})]),
        "DEGENERACY_RAYS": tagged(rays["rows"]),
        "DEGENERACY_SUMMARY": tagged([scalar_summary(rays, {"rows"})]),
        "SOURCE_STRUCTURE": tagged(source["structure_rows"]),
        "ARENA_REUSE": tagged(source["arena_rows"]),
        "SOURCE_CERTIFICATE": tagged(
            [scalar_summary(source, {"structure_rows", "arena_rows"})]
        ),
        "PREDICTION_REENTRY": tagged(reentry["rows"]),
        "PREDICTION_REENTRY_SUMMARY": tagged(
            [scalar_summary(reentry, {"rows"})]
        ),
        "ARBITRATION": tagged([arbitration]),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "GN_microscopic_prediction_status": arbitration[
                        "GN_microscopic_prediction_status"
                    ],
                    "GR_reduction_status": arbitration["GR_reduction_status"],
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
    theorem = sections["identifiability"]
    calibration = sections["calibration"]
    rays = sections["rays"]
    source = sections["source_coupling"]
    reentry = sections["prediction_reentry"]
    arbitration = sections["arbitration"]
    previous_validation = read_csv(
        OUTPUT / "P8_Y5_BRR545_4897_VALIDATION.csv"
    )
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-740"
    ]
    variable_symbols = (
        "MR4898_MTS",
        "W1eff4898_MTS",
        "M0EH4898_MTS",
        "DeltaM4898_MTS",
        "GNcal4898_MTS",
        "GNrank4898_MTS",
        "SourceCert4898_MTS",
        "GNpredict4898_MTS",
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
        / "4898-Y5-R2FR-microscopic-Planck-stiffness-owner-and-GN-calibration-versus-prediction-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL
        / "914-PPC4161-Planck-stiffness-identifiability-and-one-calibration-certificate.md"
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
        OUTPUT / "P8_Y5_R2FR_4898_SOURCE_REGISTER.csv",
        *[OUTPUT / f"P8_Y5_R2FR_4898_{name}.csv" for name in groups],
    ]
    rows = [
        check(
            "VAL4898_00_prior",
            bool(previous_validation)
            and previous_validation[-1]["check_id"] == "VAL4897_OVERALL"
            and previous_validation[-1]["status"] == "PASS",
            "4897 validation inherited",
        ),
        check(
            "VAL4898_01_sources",
            sections["sources"]["passed"]
            and all(
                row["source_exists"] and row["marker_found"] for row in sources
            ),
            "all local markers and official source records exist",
        ),
        check(
            "VAL4898_02_owner_rows",
            owners["passed"]
            and owners["owner_rows"] == 8
            and owners["blocking_rows"] == 6,
            "eight microscopic owner rows classify six prediction blockers",
        ),
        check(
            "VAL4898_03_owner_paths",
            owners["all_source_paths_exist"],
            "all owner evidence paths exist",
        ),
        check(
            "VAL4898_04_prediction_not_ready",
            not owners["microscopic_G_prediction_ready"],
            "numeric microscopic G prediction remains blocked",
        ),
        check(
            "VAL4898_05_total_relation",
            theorem["passed"]
            and "M_EH,boundary" in theorem["renormalized_relation"]
            and "DeltaM_Hghost" in theorem["renormalized_relation"],
            "counterterm-complete stiffness relation retained",
        ),
        check(
            "VAL4898_06_rank",
            theorem["jacobian_rank"] == 1
            and theorem["nullity_if_W1_fixed"] == 2
            and theorem["nullity_if_W1_unfixed"] == 3,
            "rank-one identifiability theorem closes",
        ),
        check(
            "VAL4898_07_scalar_condition",
            "only when boundary and omitted terms vanish"
            in theorem["scalar_anchor"],
            "scalar G formula is explicitly conditional",
        ),
        check(
            "VAL4898_08_CODATA",
            calibration["passed"]
            and calibration["latest_available_set_as_of_check"]
            == "CODATA_2022"
            and calibration["calibration_count"] == 1,
            "one current official G calibration is recorded",
        ),
        check(
            "VAL4898_09_Mbar",
            2.43e18 < calibration["Mbar_GeV"] < 2.44e18
            and 4.33e-9 < calibration["Mbar_kg"] < 4.35e-9,
            "reduced Planck mass conversion is numerical",
        ),
        check(
            "VAL4898_10_uncertainty",
            abs(
                calibration["Mbar_sigma_GeV"] / calibration["Mbar_GeV"]
                - 0.5 * calibration["G_relative_uncertainty"]
            )
            < 1.0e-16,
            "G uncertainty propagation follows Mbar proportional to G^-1/2",
        ),
        check(
            "VAL4898_11_degeneracy_rows",
            rays["passed"]
            and rays["pure_induced_rows"] == 5
            and rays["renormalized_rows"] == 3,
            "eight exact calibration rays generated",
        ),
        check(
            "VAL4898_12_degeneracy_recovery",
            rays["maximum_absolute_recovery_residual"] < 1.0e-12
            and rays["demonstrates_nonuniqueness"],
            "distinct microscopic rows recover identical G",
        ),
        check(
            "VAL4898_13_structure",
            source["passed"]
            and source["structure_derived"]
            and source["all_source_paths_exist"],
            "metric pole Ward Hilbert and Poynting source structure closes",
        ),
        check(
            "VAL4898_14_one_calibration",
            source["one_global_strength_calibration"]
            and source["calibration_count"] == 1
            and source["arena_specific_retunes"] == 0,
            "one G input is reused without arena retuning",
        ),
        check(
            "VAL4898_15_arenas",
            len(source["arena_rows"]) == 5
            and all(
                row["coupling_used"] == "G_N_CODATA_2022"
                and not row["arena_specific_retune"]
                for row in source["arena_rows"]
            ),
            "five correspondence arenas reuse one coupling",
        ),
        check(
            "VAL4898_16_prediction_gate",
            reentry["passed"]
            and reentry["total_clauses"] == 10
            and reentry["passed_clauses"] == 1
            and not reentry["prediction_reentry_allowed"],
            "microscopic prediction gate remains all-or-nothing and closed",
        ),
        check(
            "VAL4898_17_arbitration",
            arbitration["passed"]
            and arbitration["GN_correspondence_status"]
            == "ONE_GLOBAL_CODATA_CALIBRATION_CLOSES_STRENGTH_WITH_NO_ARENA_RETUNING",
            "calibrated correspondence arbitration passes",
        ),
        check(
            "VAL4898_18_prediction_status",
            arbitration["GN_microscopic_prediction_status"]
            == "OPEN_RANK_DEFICIENT_CALIBRATION_SURFACE_NOT_CLAIMED",
            "microscopic G prediction is not smuggled in",
        ),
        check(
            "VAL4898_19_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "GN_one_global_calibration_accepted_universal_source_strength_closed_microscopic_prediction_rank_deficient_and_open_private_nonclaim",
            "L-740 unique private nonclaim status",
        ),
        check(
            "VAL4898_20_variables",
            len(new_variables) == 8
            and all(variable_counts[symbol] == 1 for symbol in variable_symbols),
            "eight checkpoint variables are unique",
        ),
        check(
            "VAL4898_21_variable_sources",
            variable_sources_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4898_22_documents",
            "MTS_GN_CALIBRATION_VERSUS_PREDICTION_GATE_4898" in checkpoint
            and "PPC4161_GN_IDENTIFIABILITY_AND_CALIBRATION_4898"
            in formal_note,
            "checkpoint and formal markers exist",
        ),
        check(
            "VAL4898_23_registers",
            "1.191 Newton-stiffness identifiability" in equations
            and "142. A calibration surface is not a prediction" in redteam
            and "PPC4161 checkpoint 4898" in spine,
            "equation red-team and spine registers updated",
        ),
        check(
            "VAL4898_24_resume",
            "PPC4161_GN_IDENTIFIABILITY_AND_CALIBRATION_4898" in resume
            and NEXT_TARGET in resume,
            "resume and 4899 handoff updated",
        ),
        check(
            "VAL4898_25_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4898_26_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4898_27_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4898_28_scripts",
            compile_source(SCRIPTS / "Y5_R2FR_4898_GN_owner_calibration.py")
            and compile_source(
                SCRIPTS / "Y5_R2FR_4898_GN_owner_calibration_gate.py"
            ),
            "research and gate scripts compile",
        ),
        check(
            "VAL4898_29_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no post-checkpoint script pycache",
        ),
        check(
            "VAL4898_30_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4899 primitive U1 normalization target selected",
        ),
        check(
            "VAL4898_31_internal",
            calculation["all_checks_pass"],
            "4898 calculation internally passes",
        ),
    ]
    rows.append(
        check(
            "VAL4898_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_GN_CALIBRATION_VERSUS_PREDICTION_GATE_4898_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4898_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4898_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4898_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4898_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4898_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
