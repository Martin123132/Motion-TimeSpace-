from __future__ import annotations

import csv
import json
import math
import subprocess
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

import Y5_R2FR_4906_galaxy_kernel_no_slip_lensing_gate as research  # noqa: E402


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
        if key not in {"rows", "density_rows", "summary_rows"}
    }


def source_rows() -> list[dict[str, Any]]:
    rows = [dict(row) for row in research.source_contract()["rows"]]
    generated = [
        (
            "SRC4906_14_provenance",
            POST / "source-intake" / "galaxy_kernel" / "4906" / "PROVENANCE.md",
            "MTS_GALAXY_KERNEL_SOURCE_PROVENANCE_4906",
        ),
        (
            "SRC4906_15_checkpoint",
            POST
            / "4906-Y5-R2FR-galaxy-response-to-no-slip-covariant-form-factor-and-independent-lensing-gate.md",
            research.MARKER,
        ),
        (
            "SRC4906_16_formal",
            FORMAL / "922-PPC4161-galaxy-kernel-no-slip-arbitration.md",
            research.FORMAL_MARKER,
        ),
        (
            "SRC4906_17_claim",
            FORMAL / "02-claims-register.csv",
            "L-748",
        ),
        (
            "SRC4906_18_variables",
            FORMAL / "04-variable-audit.csv",
            "GalaxyArbitration4906_MTS",
        ),
        (
            "SRC4906_19_equations",
            FORMAL / "05-equation-register.md",
            "1.199 Galaxy-kernel linearity theorem",
        ),
        (
            "SRC4906_20_redteam",
            FORMAL / "06-consistency-red-team.md",
            "150. A reproducible galaxy response cache",
        ),
        (
            "SRC4906_21_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4906",
        ),
        (
            "SRC4906_22_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            research.FORMAL_MARKER,
        ),
        (
            "SRC4906_23_research",
            SCRIPTS / "Y5_R2FR_4906_galaxy_kernel_no_slip_lensing_gate.py",
            "def linearity_and_equivalent_density",
        ),
        (
            "SRC4906_24_validation",
            SCRIPTS
            / "Y5_R2FR_4906_galaxy_kernel_no_slip_lensing_gate_validation.py",
            "VAL4906_OVERALL",
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
                "access_mode": "generated_or_updated",
                "source_checked_date": "2026-07-11",
            }
        )
    return tagged(rows)


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    groups = {
        "ARTIFACT_AUDIT": tagged(sections["artifacts"]["rows"]),
        "ARTIFACT_AUDIT_SUMMARY": tagged(
            [scalar_summary(sections["artifacts"])]
        ),
        "LINEARITY_THEOREM": tagged(sections["linearity"]["rows"]),
        "LINEARITY_THEOREM_SUMMARY": tagged(
            [scalar_summary(sections["linearity"])]
        ),
        "EQUIVALENT_DENSITY": tagged(
            sections["linearity"]["density_rows"]
        ),
        "RESPONSE_PER_GALAXY": tagged(sections["spread"]["rows"]),
        "RESPONSE_SPREAD": tagged(sections["spread"]["summary_rows"]),
        "RESPONSE_SPREAD_SUMMARY": tagged(
            [scalar_summary(sections["spread"])]
        ),
        "CONFORMAL_LENSING": tagged(sections["conformal"]["rows"]),
        "CONFORMAL_LENSING_SUMMARY": tagged(
            [scalar_summary(sections["conformal"])]
        ),
        "BI_RESPONSE_INVERSE": tagged(sections["inverse"]["rows"]),
        "BI_RESPONSE_INVERSE_SUMMARY": tagged(
            [scalar_summary(sections["inverse"])]
        ),
        "V19_ARBITRATION": tagged(sections["v19"]["rows"]),
        "V19_ARBITRATION_SUMMARY": tagged(
            [scalar_summary(sections["v19"])]
        ),
        "ARBITRATION": tagged(sections["arbitration"]["rows"]),
        "ARBITRATION_SUMMARY": tagged(
            [scalar_summary(sections["arbitration"])]
        ),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "direct_no_slip_mapping_status": sections[
                        "arbitration"
                    ]["direct_no_slip_mapping_status"],
                    "galaxy_evidence_status": sections["arbitration"][
                        "galaxy_evidence_status"
                    ],
                    "conformal_route_status": sections["arbitration"][
                        "conformal_route_status"
                    ],
                    "active_residual_status": sections["arbitration"][
                        "active_residual_status"
                    ],
                    "active_novel_MTS_numeric_predictions": sections[
                        "arbitration"
                    ]["active_novel_MTS_numeric_predictions"],
                    "independent_lensing_score_run": sections[
                        "arbitration"
                    ]["independent_lensing_score_run"],
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
    artifacts = sections["artifacts"]
    linearity = sections["linearity"]
    spread = sections["spread"]
    conformal = sections["conformal"]
    inverse = sections["inverse"]
    v19 = sections["v19"]
    arbitration = sections["arbitration"]

    previous = read_csv(OUTPUT / "P8_Y5_BRR545_4905_VALIDATION.csv")
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-748"
    ]
    symbols = (
        "GalaxyArtifact4906_MTS",
        "GalaxySupport4906_MTS",
        "GalaxyLinearity4906_MTS",
        "EquivalentDensity4906_MTS",
        "MuPoint4906_MTS",
        "ConformalShift4906_MTS",
        "ConformalLensing4906_MTS",
        "BiResponseA04906_MTS",
        "BiResponseA24906_MTS",
        "BiResponseFR4906_MTS",
        "BiResponseFC4906_MTS",
        "GalaxyArbitration4906_MTS",
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
        / "4906-Y5-R2FR-galaxy-response-to-no-slip-covariant-form-factor-and-independent-lensing-gate.md"
    )
    formal_path = FORMAL / "922-PPC4161-galaxy-kernel-no-slip-arbitration.md"
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

    galaxy_status_result = subprocess.run(
        ["git", "status", "--short"],
        cwd=research.GALAXY_REPO,
        text=True,
        capture_output=True,
        check=False,
    )
    galaxy_status = [
        line for line in galaxy_status_result.stdout.splitlines() if line
    ]
    galaxy_changed_paths = [line[3:].strip() for line in galaxy_status]
    external_hashes_unchanged = all(
        (not row["local_path_required"])
        or row["access_mode"] != "read_only"
        or research.sha256(Path(str(row["source_path_or_url"])))
        == row["sha256"]
        for row in sources
    )

    all_rows = sources + [row for rows in groups.values() for row in rows]
    output_paths = [
        OUTPUT / "P8_Y5_R2FR_4906_SOURCE_REGISTER.csv",
        *[
            OUTPUT / f"P8_Y5_R2FR_4906_{name}.csv"
            for name in groups
        ],
    ]
    scripts = [
        SCRIPTS / "Y5_R2FR_4906_galaxy_kernel_no_slip_lensing_gate.py",
        SCRIPTS
        / "Y5_R2FR_4906_galaxy_kernel_no_slip_lensing_gate_validation.py",
    ]
    density_rows = linearity["density_rows"]
    spread_rows = spread["summary_rows"]

    rows = [
        check(
            "VAL4906_00_prior",
            bool(previous)
            and previous[-1]["check_id"] == "VAL4905_OVERALL"
            and previous[-1]["status"] == "PASS",
            "4905 validation inherited",
        ),
        check(
            "VAL4906_01_sources",
            sections["sources"]["passed"]
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            "all read-only and generated source markers exist",
        ),
        check(
            "VAL4906_02_external_hashes",
            external_hashes_unchanged,
            "all read-only galaxy source hashes remained unchanged during validation",
        ),
        check(
            "VAL4906_03_galaxy_git_scope",
            galaxy_status_result.returncode == 0
            and set(galaxy_changed_paths).issubset({"scripts/mts-failure-lab.py"}),
            f"galaxy repo has no new changed path; inherited status={galaxy_status}",
        ),
        check(
            "VAL4906_04_artifact_counts",
            artifacts["passed"]
            and artifacts["v1809_curve_count"] == 175
            and artifacts["v1809_unique_amp_count"] == 40
            and artifacts["v1809_unique_q_count"] == 30,
            "v18.09 state-response multiplicity reproduced",
        ),
        check(
            "VAL4906_05_active_artifact",
            artifacts["active_priority_verified"]
            and artifacts["active_browser_artifact"]
            == "v18.21_active_browser_release"
            and artifacts["v1821_exact_cache"]
            and not artifacts["v1821_native_formula"],
            "active browser response is the exact v18.21 cache",
        ),
        check(
            "VAL4906_06_no_fixed_artifact",
            artifacts["fixed_linear_kernel_artifact_count"] == 0,
            "no audited artifact is a fixed source-independent linear kernel",
        ),
        check(
            "VAL4906_07_linearity",
            linearity["passed"]
            and not linearity["fixed_linear_convolution_exists"]
            and linearity["nonlinear_parent_action_still_possible"],
            "fixed-kernel no-go and nonlinear-parent scope both retained",
        ),
        check(
            "VAL4906_08_density_symbolic",
            linearity["density_symbolic_residual"] == "0"
            and linearity["equivalent_density_positive"],
            "spherical-equivalent density differentiates exactly and remains positive",
        ),
        check(
            "VAL4906_09_density_slopes",
            math.isclose(
                linearity["inner_density_slope_q077"], -1.23, abs_tol=1e-12
            )
            and linearity["outer_density_slope"] == -2.0
            and all(row["positive"] for row in density_rows),
            "inner and outer asymptotic slopes reproduce",
        ),
        check(
            "VAL4906_10_curve_join",
            spread["passed"]
            and spread["galaxy_count"] == 175
            and spread["all_support_lengths_match"],
            "all 175 v18.21 support arrays join their SPARC curves",
        ),
        check(
            "VAL4906_11_canonical_split",
            spread["canonical_match_count"] == 87
            and spread["noncanonical_support_count"] == 88,
            "canonical versus redistributed support split reproduces",
        ),
        check(
            "VAL4906_12_response_spread",
            len(spread_rows) == 4
            and all(row["galaxy_count"] >= 172 for row in spread_rows)
            and all(row["mu_pointwise_p16"] > 1.0 for row in spread_rows)
            and all(
                row["fraction_mu_greater_than_4_over_3"] > 0.88
                for row in spread_rows
            ),
            "pointwise population spread and scalar-warning fraction reproduce",
        ),
        check(
            "VAL4906_13_pointwise_scope",
            not spread["pointwise_ratio_is_fourier_kernel"],
            "real-space ratios are not relabelled as momentum responses",
        ),
        check(
            "VAL4906_14_conformal_cancellation",
            conformal["passed"]
            and conformal["lensing_sum_residual"] == "0"
            and conformal["mu_lensing"] == "1",
            "leading conformal lensing cancellation closes",
        ),
        check(
            "VAL4906_15_conformal_slip",
            conformal["mu_dynamic"] == "epsilon + 1"
            and conformal["eta"] == "(1 - epsilon)/(epsilon + 1)"
            and conformal["no_slip_requires_zero_scalar_response"],
            "conformal scalar relation intersects no-slip only at zero response",
        ),
        check(
            "VAL4906_16_inverse_map",
            inverse["passed"]
            and inverse["A0"] == "1/(4*mu_L - 3*mu_d)"
            and inverse["A2"] == "1/mu_L"
            and inverse["dynamic_reconstruction_residual"] == "0"
            and inverse["lensing_reconstruction_residual"] == "0",
            "general two-observable inverse map reconstructs both responses",
        ),
        check(
            "VAL4906_17_underdetermination",
            not inverse["kinematics_alone_determines_both_functions"],
            "kinematics alone is not used to invent both form factors",
        ),
        check(
            "VAL4906_18_v19_disk",
            v19["passed"]
            and v19["disk_verdict"] == "missing physical source variable"
            and v19["sink_target_mean_gain_km_s"] < 0.0
            and v19["negative_field_target_count"] == 0
            and not v19["boundary_direction_consistent"],
            "current v19 source and boundary route is rejected",
        ),
        check(
            "VAL4906_19_v19_control",
            v19["protected_max_regression_km_s"] > 88.0
            and not v19["candidate_promoted"]
            and not v19["parent_owned"],
            "protected regression and ownership block promotion",
        ),
        check(
            "VAL4906_20_arbitration",
            arbitration["passed"]
            and arbitration["direct_no_slip_mapping_status"]
            == "REJECTED_FOR_CURRENT_GALAXY_ARTIFACTS"
            and arbitration["active_residual_status"]
            == "Gamma_MTS_res_equals_zero",
            "route arbitration preserves the active zero residual",
        ),
        check(
            "VAL4906_21_lensing_gate",
            not arbitration["independent_lensing_score_run"]
            and not arbitration["public_claim_allowed"],
            "undefined kernel is not assigned a misleading lensing score",
        ),
        check(
            "VAL4906_22_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "current_galaxy_response_not_fixed_linear_convolution_no_slip_import_rejected_environmental_parent_open_v19_conformal_not_no_slip_disk_pilot_rejected_private_nonclaim",
            "L-748 unique and scoped",
        ),
        check(
            "VAL4906_23_variables",
            len(selected) == len(symbols)
            and all(counts[symbol] == 1 for symbol in symbols),
            "twelve checkpoint variables are unique",
        ),
        check(
            "VAL4906_24_variable_sources",
            variable_sources_exist,
            "all variable source paths exist",
        ),
        check(
            "VAL4906_25_documents",
            research.MARKER in checkpoint
            and research.FORMAL_MARKER in formal_note,
            "checkpoint and formal note markers exist",
        ),
        check(
            "VAL4906_26_registers",
            "1.199 Galaxy-kernel linearity theorem" in equations
            and "150. A reproducible galaxy response cache" in redteam
            and "PPC4161 checkpoint 4906" in spine,
            "formal registers updated",
        ),
        check(
            "VAL4906_27_resume",
            research.FORMAL_MARKER in resume and NEXT_TARGET in resume,
            "resume handoff updated",
        ),
        check(
            "VAL4906_28_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder markers",
        ),
        check(
            "VAL4906_29_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4906_30_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4906_31_scripts",
            all(compile_source(path) for path in scripts),
            "scripts compile",
        ),
        check(
            "VAL4906_32_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no pycache",
        ),
        check(
            "VAL4906_33_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET
            and not (POST / NEXT_TARGET).exists(),
            "4907 handoff selected but not pre-created",
        ),
        check(
            "VAL4906_34_internal",
            calculation["all_checks_pass"],
            "calculation internally passes",
        ),
    ]
    rows.append(
        check(
            "VAL4906_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_GALAXY_KERNEL_NO_SLIP_LENSING_ARBITRATION_4906_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4906_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4906_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4906_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4906_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4906_VALIDATION_FAIL"
    )
    if not passed:
        for row in validation:
            if row["status"] != "PASS":
                print(row["check_id"], row["detail"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
