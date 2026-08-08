from __future__ import annotations

import csv
import json
import math
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

import Y5_R2FR_4907_parent_environmental_bi_response_or_freeze as research  # noqa: E402


TIMESTAMP = datetime.now(timezone.utc).isoformat()
NEXT_TARGET = research.NEXT_TARGET


def serializable(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
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


def scalar_summary(section: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in section.items()
        if key not in {"rows", "scalar_rows"}
    }


def source_rows() -> list[dict[str, Any]]:
    rows = [dict(row) for row in research.source_contract()["rows"]]
    generated = [
        (
            "SRC4907_13_provenance",
            POST
            / "source-intake"
            / "environmental_response"
            / "4907"
            / "PROVENANCE.md",
            "MTS_ENVIRONMENTAL_BIRESPONSE_SOURCE_PROVENANCE_4907",
        ),
        (
            "SRC4907_14_checkpoint",
            POST
            / "4907-Y5-R2FR-parent-derived-environmental-bi-response-action-or-galaxy-residual-freeze.md",
            research.MARKER,
        ),
        (
            "SRC4907_15_formal",
            FORMAL / "923-PPC4161-environmental-bi-response-galaxy-freeze.md",
            research.FORMAL_MARKER,
        ),
        (
            "SRC4907_16_claim",
            FORMAL / "02-claims-register.csv",
            "L-749",
        ),
        (
            "SRC4907_17_variables",
            FORMAL / "04-variable-audit.csv",
            "ResidualStatus4907_MTS",
        ),
        (
            "SRC4907_18_equations",
            FORMAL / "05-equation-register.md",
            "1.200 Environmental bi-response no-go",
        ),
        (
            "SRC4907_19_redteam",
            FORMAL / "06-consistency-red-team.md",
            "151. A logical environmental escape",
        ),
        (
            "SRC4907_20_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4907",
        ),
        (
            "SRC4907_21_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            research.FORMAL_MARKER,
        ),
        (
            "SRC4907_22_research",
            SCRIPTS / "Y5_R2FR_4907_parent_environmental_bi_response_or_freeze.py",
            "def analytic_metric_scaling_theorem",
        ),
        (
            "SRC4907_23_validation",
            SCRIPTS
            / "Y5_R2FR_4907_parent_environmental_bi_response_or_freeze_validation.py",
            "VAL4907_OVERALL",
        ),
    ]
    for source_id, path, marker in generated:
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
                "sha256": research.sha256(path) if exists else "",
                "source_checked_date": "2026-07-12",
            }
        )
    return tagged(rows)


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    groups = {
        "PARENT_CARRIERS": tagged(sections["carriers"]["rows"]),
        "PARENT_CARRIERS_SUMMARY": tagged(
            [scalar_summary(sections["carriers"])]
        ),
        "ANALYTIC_METRIC_SCALING": tagged(sections["metric"]["rows"]),
        "ANALYTIC_METRIC_SCALING_SUMMARY": tagged(
            [scalar_summary(sections["metric"])]
        ),
        "SCALAR_GALAXY_LOCAL": tagged(sections["scalar"]["rows"]),
        "SCALAR_SCREENING_RANGE": tagged(
            sections["scalar"]["scalar_rows"]
        ),
        "SCALAR_GALAXY_LOCAL_SUMMARY": tagged(
            [scalar_summary(sections["scalar"])]
        ),
        "STATIONARY_FLOW": tagged(sections["flow"]["rows"]),
        "STATIONARY_FLOW_SUMMARY": tagged(
            [scalar_summary(sections["flow"])]
        ),
        "MAXWELL_POYNTING": tagged(sections["Maxwell"]["rows"]),
        "MAXWELL_POYNTING_SUMMARY": tagged(
            [scalar_summary(sections["Maxwell"])]
        ),
        "REENTRY_GATE": tagged(sections["gate"]["rows"]),
        "REENTRY_GATE_SUMMARY": tagged(
            [scalar_summary(sections["gate"])]
        ),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "galaxy_empirical_pillar_retained": sections["gate"][
                        "galaxy_empirical_pillar_retained"
                    ],
                    "galaxy_residual_active": sections["gate"][
                        "galaxy_residual_active"
                    ],
                    "Gamma_MTS_res": sections["gate"]["Gamma_MTS_res"],
                    "new_parent_field_added": sections["gate"][
                        "new_parent_field_added"
                    ],
                    "new_free_coefficient_added": sections["gate"][
                        "new_free_coefficient_added"
                    ],
                    "active_novel_MTS_numeric_predictions": sections["gate"][
                        "active_novel_MTS_numeric_predictions"
                    ],
                    "next_target": calculation["next_target"],
                    "all_checks_pass": calculation["all_checks_pass"],
                }
            ]
        ),
    }
    return groups


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
    carriers = sections["carriers"]
    metric = sections["metric"]
    scalar = sections["scalar"]
    flow = sections["flow"]
    Maxwell = sections["Maxwell"]
    gate = sections["gate"]

    previous = read_csv(OUTPUT / "P8_Y5_BRR545_4906_VALIDATION.csv")
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-749"
    ]
    symbols = (
        "ParentCarrier4907_MTS",
        "AnalyticScaling4907_MTS",
        "GalaxyLambdaZero4907_MTS",
        "ScalarEnvelope4907_MTS",
        "ScalarCharge4907_MTS",
        "ScalarRange4907_MTS",
        "ConformalBiResponse4907_MTS",
        "StationaryTheta4907_MTS",
        "MaxwellConformal4907_MTS",
        "PoyntingProjection4907_MTS",
        "GalaxyFreeze4907_MTS",
        "ResidualStatus4907_MTS",
    )
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    selected = [row for row in variables if row["symbol"] in symbols]
    counts = {
        symbol: sum(row["symbol"] == symbol for row in variables)
        for symbol in symbols
    }
    variable_sources_exist = all(
        (ROOT / path).exists()
        for row in selected
        for path in row["source_files"].split(";")
    )

    checkpoint_path = (
        POST
        / "4907-Y5-R2FR-parent-derived-environmental-bi-response-action-or-galaxy-residual-freeze.md"
    )
    formal_path = FORMAL / "923-PPC4161-environmental-bi-response-galaxy-freeze.md"
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    formal_note = formal_path.read_text(encoding="utf-8")
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
        OUTPUT / "P8_Y5_R2FR_4907_SOURCE_REGISTER.csv",
        *[
            OUTPUT / f"P8_Y5_R2FR_4907_{name}.csv"
            for name in groups
        ],
    ]
    scripts = [
        SCRIPTS / "Y5_R2FR_4907_parent_environmental_bi_response_or_freeze.py",
        SCRIPTS
        / "Y5_R2FR_4907_parent_environmental_bi_response_or_freeze_validation.py",
    ]
    scalar_rows = scalar["rows"]
    screening_rows = scalar["scalar_rows"]
    gate_statuses = {row["gate"]: row["status"] for row in gate["rows"]}

    rows = [
        check(
            "VAL4907_00_prior",
            bool(previous)
            and previous[-1]["check_id"] == "VAL4906_OVERALL"
            and previous[-1]["status"] == "PASS",
            "4906 validation inherited",
        ),
        check(
            "VAL4907_01_sources",
            sections["sources"]["passed"]
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            "all local source and generated markers exist",
        ),
        check(
            "VAL4907_02_carriers",
            carriers["passed"]
            and carriers["active_extra_light_MTS_fields"] == 0
            and carriers["active_direct_MTS_matter_vertices"] == 0
            and carriers["eligible_environmental_MTS_carriers"] == 0,
            "surviving parent has no hidden environmental carrier",
        ),
        check(
            "VAL4907_03_metric_identity",
            metric["passed"]
            and metric["identity_solution"]
            == "[{S_0: 0, c_1: 0, c_2: 0, c_3: 0, c_4: 0, c_5: 0}]",
            "analytic polynomial identity forces only the zero support solution",
        ),
        check(
            "VAL4907_04_metric_limits",
            metric["source_zero_limit"] == "0"
            and metric["galaxy_zero_limit"] == "S_0"
            and not metric["analytic_metric_route_closes_current_galaxy_law"],
            "source-zero limit distinguishes analytic metric and canonical galaxy laws",
        ),
        check(
            "VAL4907_05_nonanalytic_scope",
            not metric["nonanalytic_escape_parent_owned"],
            "logical nonanalytic escape is not mislabelled as a parent result",
        ),
        check(
            "VAL4907_06_scalar_PPN",
            scalar["passed"]
            and math.isclose(
                scalar["Cassini_alpha_DEF_squared_max"],
                3.350112228759664e-5,
                rel_tol=1e-13,
            )
            and math.isclose(
                scalar["generous_force_envelope"],
                6.700224457519328e-5,
                rel_tol=1e-13,
            ),
            "validated Cassini scalar ceiling and doubled envelope reproduce",
        ),
        check(
            "VAL4907_07_scalar_magnitude",
            len(scalar_rows) == 4
            and all(not row["same_branch_magnitude_pass"] for row in scalar_rows)
            and scalar["minimum_required_to_envelope_ratio"] > 5800.0,
            "all four radial galaxy targets exceed the generous scalar envelope",
        ),
        check(
            "VAL4907_08_scalar_outer",
            scalar_rows[-1]["p16_over_generous_scalar_envelope"] > 18400.0
            and scalar_rows[-1]["median_over_generous_scalar_envelope"]
            > 44200.0,
            "outer radial magnitude shortfall reproduces",
        ),
        check(
            "VAL4907_09_scalar_charge",
            scalar["anchor_solar_charge_reproduced"]
            and screening_rows[0]["solar_charge_ratio"] > 1.0
            and screening_rows[1]["solar_charge_ratio"] > 1.0
            and not screening_rows[0]["screened"]
            and not screening_rows[1]["screened"],
            "both negative-beta weak-source branches are unscreened",
        ),
        check(
            "VAL4907_10_scalar_range",
            math.isclose(
                scalar["minimum_empirical_L_eff_kpc"],
                0.6988015608918949,
                rel_tol=1e-13,
            )
            and scalar["minimum_range_AU_attenuation"] > 0.99999999
            and not screening_rows[2]["screened"],
            "galaxy-range scalar remains unsuppressed over one AU",
        ),
        check(
            "VAL4907_11_scalar_lensing",
            scalar["pure_conformal_lensing_response"] == 1.0
            and not scalar["same_branch_galaxy_route_passes"],
            "conformal branch fails the bi-response gate",
        ),
        check(
            "VAL4907_12_flow_stationary",
            flow["passed"]
            and flow["stationary_disk_source"] == 0
            and not flow["derivative_route_galaxy_passes"],
            "stationary circular flow has exact zero derivative source",
        ),
        check(
            "VAL4907_13_flow_retired",
            not flow["bath_source_currently_active"],
            "bath carrier remains retired",
        ),
        check(
            "VAL4907_14_Maxwell_conformal",
            Maxwell["passed"]
            and Maxwell["conformal_weight"] == "1"
            and Maxwell["Maxwell_trace"] == "0",
            "four-dimensional Maxwell conformal and trace identities close",
        ),
        check(
            "VAL4907_15_Poynting",
            Maxwell["Poynting_gravitates_in_baseline"]
            and not Maxwell["Poynting_sources_trace_memory_scalar"]
            and not Maxwell["Maxwell_creates_missing_bi_response"],
            "Poynting remains baseline Hilbert stress without becoming a scalar closure",
        ),
        check(
            "VAL4907_16_gate_failures",
            gate_statuses["parent_owned_carrier"] == "FAIL"
            and gate_statuses["galaxy_dynamics"] == "FAIL"
            and gate_statuses["lensing_relation"] == "FAIL"
            and gate_statuses["stationary_source"] == "FAIL"
            and gate_statuses["local_GR"] == "FAIL",
            "all substantive environmental entry gates fail explicitly",
        ),
        check(
            "VAL4907_17_baseline_gates",
            gate_statuses["Maxwell_EM_stress"] == "PASS_BASELINE_ONLY"
            and gate_statuses["Ward_conservation"] == "NO_NEW_EDGE",
            "Maxwell and Ward baselines remain intact without candidate insertion",
        ),
        check(
            "VAL4907_18_freeze",
            gate["passed"]
            and gate_statuses["action_entry_decision"]
            == "FREEZE_GALAXY_RESIDUAL_OUTSIDE_ACTIVE_ACTION"
            and gate["galaxy_empirical_pillar_retained"]
            and not gate["galaxy_residual_active"],
            "galaxy evidence retained while action residual freezes",
        ),
        check(
            "VAL4907_19_residual",
            gate["Gamma_MTS_res"] == 0
            and not gate["new_parent_field_added"]
            and not gate["new_free_coefficient_added"]
            and gate["active_novel_MTS_numeric_predictions"] == 0,
            "active residual and parameter count remain unchanged",
        ),
        check(
            "VAL4907_20_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "no_current_parent_environmental_bi_response_analytic_metric_conformal_scalar_derivative_flow_and_Poynting_routes_rejected_galaxy_residual_frozen_private_nonclaim",
            "L-749 unique and scoped",
        ),
        check(
            "VAL4907_21_variables",
            len(selected) == len(symbols)
            and all(counts[symbol] == 1 for symbol in symbols),
            "twelve checkpoint variables are unique",
        ),
        check(
            "VAL4907_22_variable_sources",
            variable_sources_exist,
            "all variable source paths exist",
        ),
        check(
            "VAL4907_23_documents",
            research.MARKER in checkpoint
            and research.FORMAL_MARKER in formal_note,
            "checkpoint and formal note markers exist",
        ),
        check(
            "VAL4907_24_registers",
            "1.200 Environmental bi-response no-go" in equations
            and "151. A logical environmental escape" in redteam
            and "PPC4161 checkpoint 4907" in spine,
            "formal registers updated",
        ),
        check(
            "VAL4907_25_resume",
            research.FORMAL_MARKER in resume and NEXT_TARGET in resume,
            "resume handoff updated",
        ),
        check(
            "VAL4907_26_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder markers",
        ),
        check(
            "VAL4907_27_finite",
            not any(
                str(value).lower() in {"nan", "inf", "-inf"}
                for row in all_rows
                for value in row.values()
            ),
            "generated evidence contains no nonfinite numeric cells",
        ),
        check(
            "VAL4907_28_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4907_29_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4907_30_scripts",
            all(compile_source(path) for path in scripts),
            "scripts compile",
        ),
        check(
            "VAL4907_31_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no pycache",
        ),
        check(
            "VAL4907_32_next",
            NEXT_TARGET in checkpoint
            and gate["next_target"] == NEXT_TARGET
            and not (POST / NEXT_TARGET).exists(),
            "4908 handoff selected but not pre-created",
        ),
        check(
            "VAL4907_33_internal",
            calculation["all_checks_pass"],
            "calculation internally passes",
        ),
    ]
    rows.append(
        check(
            "VAL4907_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_PARENT_ENVIRONMENTAL_BIRESPONSE_OR_GALAXY_FREEZE_4907_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4907_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4907_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4907_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4907_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4907_VALIDATION_FAIL"
    )
    if not passed:
        for row in validation:
            if row["status"] != "PASS":
                print(row["check_id"], row["detail"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
