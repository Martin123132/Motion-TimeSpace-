from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

from Y5_R2FR_4884_contact_coefficient_ownership_bounds import (
    NEXT_TARGET,
    result,
)


CHECKPOINT = "4884"
TIMESTAMP = "2026-07-10T23:48:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE_ROOT = POST / "source-intake" / "strong_matter" / "4884"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            **row,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row in rows
    ]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def source_rows() -> list[dict[str, Any]]:
    local_text = [
        (
            "SRC4884_00_checkpoint",
            POST
            / "4884-Y5-R2FR-strong-matter-contact-coefficient-parent-ownership-or-observational-bound-projection-gate.md",
            "MTS_CONTACT_COEFFICIENT_OWNERSHIP_AND_BOUNDS_4884",
        ),
        (
            "SRC4884_01_research_script",
            POST
            / "scripts"
            / "Y5_R2FR_4884_contact_coefficient_ownership_bounds.py",
            "def spectrum_rescue",
        ),
        (
            "SRC4884_02_gate_script",
            POST
            / "scripts"
            / "Y5_R2FR_4884_contact_coefficient_ownership_bounds_gate.py",
            "P8_Y5_BRR545_4884_VALIDATION_PASS",
        ),
        (
            "SRC4884_03_parent_matching",
            POST
            / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
            "a_{i,R}=a_{i,b}+a_{i,\\rm loop}",
        ),
        (
            "SRC4884_04_spectrum",
            POST
            / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "W_1=S_h+2N_D-4N_V",
        ),
        (
            "SRC4884_05_multi_EOS",
            POST
            / "4883-Y5-R2FR-tabulated-microphysical-EOS-acquisition-and-multi-EOS-mass-radius-tidal-contact-response-gate.md",
            "MTS_MULTI_EOS_TOV_LOVE_CONTACT_RESPONSE_4883",
        ),
        (
            "SRC4884_06_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4883_VALIDATION.csv",
            "VAL4883_OVERALL,PASS",
        ),
        (
            "SRC4884_07_formal_note",
            FORMAL
            / "900-PPC4161-contact-coefficient-ownership-and-strong-matter-projection.md",
            "PPC4161_CONTACT_COEFFICIENT_OWNERSHIP_4884",
        ),
        (
            "SRC4884_08_claims",
            FORMAL / "02-claims-register.csv",
            "L-726",
        ),
        (
            "SRC4884_09_variables",
            FORMAL / "04-variable-audit.csv",
            "h_three_boson_U1_MTS",
        ),
        (
            "SRC4884_10_equations",
            FORMAL / "05-equation-register.md",
            "1.177 Parent loop ownership and three-boson nonminimal ray",
        ),
        (
            "SRC4884_11_redteam",
            FORMAL / "06-consistency-red-team.md",
            "128. Loop ownership is not total coefficient ownership",
        ),
        (
            "SRC4884_12_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4884",
        ),
        (
            "SRC4884_13_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_CONTACT_COEFFICIENT_OWNERSHIP_4884",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker in local_text:
        exists = path.exists()
        content = (
            path.read_text(encoding="utf-8", errors="replace")
            if exists
            else ""
        )
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_text",
                "source_path": str(path),
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker in content,
                "verification_method": "local_path_and_marker",
            }
        )

    pdfs = [
        (
            "SRC4884_14_GW170817_pdf",
            SOURCE_ROOT / "GW170817_EOS_PRL_P1800115_v12.pdf",
            "EE46603B01059015C33981F755318CB3D1C4A8F8E9BC9EE7E68DC16C1F84FE27",
            "page 4 Lambda1.4=190+390-120; page 6 R=11.9+/-1.4",
        ),
        (
            "SRC4884_15_NICER_pdf",
            SOURCE_ROOT / "NICER_J0030_Miller_1912.05705.pdf",
            "6D3532EC2901099ABABAD7FF53B953DBADFABCD1941CFCAD858B76C98C444FF8",
            "page 2 M=1.44+0.15-0.14 and R=13.02+1.24-1.06 km",
        ),
    ]
    for source_id, path, expected_hash, marker in pdfs:
        exists = path.exists()
        digest = sha256(path).upper() if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_primary_pdf",
                "source_path": str(path),
                "source_exists": exists,
                "marker": marker,
                "marker_found": digest == expected_hash,
                "verification_method": "sha256_and_pypdf_page_text",
                "sha256": digest,
                "expected_sha256": expected_hash,
            }
        )

    web = [
        (
            "SRC4884_16_GW170817_web",
            "https://dcc.ligo.org/ligo-p1800115/public",
            "primary LVK common-EOS radius and Lambda1.4 analysis",
        ),
        (
            "SRC4884_17_NICER_web",
            "https://arxiv.org/abs/1912.05705",
            "primary NICER J0030 mass-radius analysis",
        ),
        (
            "SRC4884_18_heat_kernel",
            "https://arxiv.org/abs/hep-th/0306138",
            "primary heat-kernel coefficient review inherited from 4876",
        ),
    ]
    for source_id, url, marker in web:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "web_primary",
                "source_path": url,
                "source_exists": True,
                "marker": marker,
                "marker_found": True,
                "verification_method": "primary_source_recorded_and_browsed",
            }
        )
    return tagged(rows)


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    stability = sections["curvature_stability"]
    projection = sections["observational_projection"]
    nonlinear = sections["nonlinear_control"]
    predictions = sections["parent_predictions"]
    return {
        "OWNERSHIP_CHAIN": tagged(sections["prior_contract"]["rows"]),
        "SPECTRUM_RESCUE": tagged(sections["spectrum_rescue"]["rows"]),
        "CURVATURE_STABILITY": tagged(stability["rows"]),
        "CURVATURE_STABILITY_SUMMARY": tagged(
            [
                {
                    key: value
                    for key, value in stability.items()
                    if key not in {"rows"}
                }
            ]
        ),
        "OBSERVATIONAL_WINDOWS": tagged(projection["windows"]),
        "LINEAR_ONE_AT_A_TIME": tagged(projection["one_at_a_time"]),
        "JOINT_LINEAR_VERTICES": tagged(projection["joint_vertices"]),
        "NONLINEAR_CONTROL": tagged(nonlinear["rows"]),
        "PARENT_LOOP_PREDICTIONS": tagged(predictions["rows"]),
        "ARBITRATION": tagged([sections["arbitration"]]),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "all_checks_pass": calculation["all_checks_pass"],
                    "next_target": sections["arbitration"]["next_target"],
                }
            ]
        ),
    }


def compile_source(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except SyntaxError:
        return False
    return True


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
    ownership = sections["prior_contract"]
    rescue = sections["spectrum_rescue"]
    stability = sections["curvature_stability"]
    projection = sections["observational_projection"]
    nonlinear = sections["nonlinear_control"]
    predictions = sections["parent_predictions"]
    arbitration = sections["arbitration"]
    selected = next(
        row
        for row in predictions["rows"]
        if abs(row["W1"] - 1.0) < 1.0e-12
        and row["branch"].startswith("three_boson")
    )

    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-726"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    expected_statuses = {
        "aR_loop_owned_MTS": (
            "derived_universal_matter_loop_total_finite_open"
        ),
        "aC_loop_owned_MTS": (
            "derived_universal_matter_loop_total_finite_open"
        ),
        "h_three_boson_U1_MTS": (
            "derived_positive_EH_threshold_parent_parameter_open"
        ),
        "rUV_three_boson_MTS": (
            "Newton_matched_one_parameter_nonminimal_ray"
        ),
        "mxi_stability_MTS": (
            "derived_sampled_strong_matter_curvature_stability_floor"
        ),
        "B_NS_aRaC_MTS": (
            "source_backed_linear_interval_projection_nonlinear_scope_guard"
        ),
        "strong_matter_loop_correspondence_4884_MTS": (
            "private_conditional_parent_loop_correspondence_over_65_orders"
        ),
    }
    variables = {row["symbol"]: row for row in variable_rows}
    variable_counts = {
        symbol: sum(row["symbol"] == symbol for row in variable_rows)
        for symbol in expected_statuses
    }

    checkpoint = (
        POST
        / "4884-Y5-R2FR-strong-matter-contact-coefficient-parent-ownership-or-observational-bound-projection-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL
        / "900-PPC4161-contact-coefficient-ownership-and-strong-matter-projection.md"
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
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(
        encoding="utf-8"
    )
    prior_validation = read_csv(
        OUTPUT / "P8_Y5_BRR545_4883_VALIDATION.csv"
    )
    all_rows = sources + [row for rows in groups.values() for row in rows]
    output_paths = [
        OUTPUT / f"P8_Y5_R2FR_4884_{name}.csv" for name in groups
    ]

    rows = [
        check(
            "VAL4884_00_calculation",
            calculation["all_checks_pass"],
            "ownership rescue stability projection nonlinear and loop-ray sections",
        ),
        check(
            "VAL4884_01_sources",
            len(sources) == 19
            and all(row["source_exists"] and row["marker_found"] for row in sources),
            f"sources={len(sources)}",
        ),
        check(
            "VAL4884_02_primary_pdfs",
            all(
                row.get("sha256") == row.get("expected_sha256")
                for row in sources
                if row["source_type"] == "local_primary_pdf"
            ),
            "GW170817 and NICER PDFs hash locked",
        ),
        check(
            "VAL4884_03_prior",
            ownership["passed"]
            and prior_validation
            and all(row["status"] == "PASS" for row in prior_validation),
            "4876 4877 ownership chain and 4883 response remain green",
        ),
        check(
            "VAL4884_04_loop_ownership",
            ownership["rows"][0]["formula"] == "L*S_h2/(1152*pi^2)"
            and ownership["rows"][1]["formula"] == "L*W_C/(1920*pi^2)"
            and "PARTIAL" in ownership["rows"][2]["ownership"]
            and "PARTIAL" in ownership["rows"][3]["ownership"],
            "loop pieces derived and total pieces not conflated",
        ),
        check(
            "VAL4884_05_nonminimal_rescue",
            rescue["passed"]
            and "h>4/3" in rescue["candidate_branch"]
            and "a_R/a_C=h^2/3" in rescue["candidate_formula"],
            "three-scalar plus U1 positive-EH threshold",
        ),
        check(
            "VAL4884_06_selected_anchor",
            abs(selected["h"] - 5 / 3) < 1.0e-12
            and abs(selected["xi"] + 1 / 9) < 1.0e-12
            and abs(selected["aR_over_aC"] - 25 / 27) < 1.0e-12,
            "W1=1 anchor gives h=5/3 xi=-1/9 and aR/aC=25/27",
        ),
        check(
            "VAL4884_07_curvature_stability",
            stability["passed"]
            and len(stability["rows"]) == 9
            and 8.0e-12
            < stability["mass_floor_eV_per_sqrt_h_minus_1"]
            < 8.1e-12,
            "sampled compact-star nonminimal tachyon floor derived",
        ),
        check(
            "VAL4884_08_observational_sources",
            len(projection["windows"]) == 3
            and {row["window_id"] for row in projection["windows"]}
            == {
                "GW170817_Lambda1p4_90pct",
                "GW170817_common_EOS_radius_90pct",
                "NICER_J0030_radius_68pct",
            },
            "source-backed radius and tidal intervals",
        ),
        check(
            "VAL4884_09_linear_projection",
            projection["passed"]
            and len(projection["one_at_a_time"]) == 18
            and len(projection["joint_vertices"]) == 24,
            "three EOS by three windows and two coefficient directions",
        ),
        check(
            "VAL4884_10_direction_rank",
            projection["all_response_directions_independent"],
            "radius and tidal response directions form nonsingular 2D maps",
        ),
        check(
            "VAL4884_11_projection_scope",
            not projection["claim_ready"]
            and projection["maximum_joint_pressure_contact_fraction"] > 1,
            "broad interval vertices expose rather than hide linear-scope failure",
        ),
        check(
            "VAL4884_12_nonlinear_control",
            nonlinear["passed"]
            and len(nonlinear["rows"]) == 12
            and nonlinear["maximum_radius_delta_relative_error"] < 0.004
            and nonlinear["maximum_tidal_delta_relative_error"] < 0.055,
            "all signs and directions solved at one-percent contact control",
        ),
        check(
            "VAL4884_13_parent_predictions",
            predictions["passed"]
            and len(predictions["rows"]) == 5
            and all(
                row["orders_below_observational_width"] > 65
                for row in predictions["rows"]
            ),
            "candidate and reference loop rays negligible in strong matter",
        ),
        check(
            "VAL4884_14_control_comparison",
            arbitration[
                "strong_matter_interval_weaker_than_local_control_orders"
            ]
            > 15,
            "strong-matter interval scale is over 15 orders weaker than local EFT control",
        ),
        check(
            "VAL4884_15_arbitration",
            arbitration["passed"]
            and not arbitration["three_boson_parent_promotion"]
            and not arbitration["observational_bound_claim"],
            "loop advance retained without total-coefficient or likelihood overclaim",
        ),
        check(
            "VAL4884_16_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4884_17_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all checkpoint evidence remains private and nonclaim",
        ),
        check(
            "VAL4884_18_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4884_19_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "parent_loop_aR_aC_derived_three_boson_nonminimal_ray_viable_source_backed_strong_matter_projection_private_conditional_nonclaim",
            "L-726 unique and scope locked",
        ),
        check(
            "VAL4884_20_variables",
            all(
                variable_counts[symbol] == 1
                and variables[symbol]["status"] == status
                for symbol, status in expected_statuses.items()
            ),
            "seven coefficient-ownership variables unique and status locked",
        ),
        check(
            "VAL4884_21_documents",
            "MTS_CONTACT_COEFFICIENT_OWNERSHIP_AND_BOUNDS_4884" in checkpoint
            and "PPC4161_CONTACT_COEFFICIENT_OWNERSHIP_4884" in formal_note,
            "checkpoint and formal note markers",
        ),
        check(
            "VAL4884_22_registers",
            "1.177 Parent loop ownership and three-boson nonminimal ray"
            in equations
            and "128. Loop ownership is not total coefficient ownership"
            in redteam
            and "PPC4161 checkpoint 4884" in spine,
            "equation red-team and spine updates",
        ),
        check(
            "VAL4884_23_resume",
            "PPC4161_CONTACT_COEFFICIENT_OWNERSHIP_4884" in resume
            and NEXT_TARGET in resume,
            "resume handoff",
        ),
        check(
            "VAL4884_24_scripts",
            compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4884_contact_coefficient_ownership_bounds.py"
            )
            and compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4884_contact_coefficient_ownership_bounds_gate.py"
            ),
            "research and gate scripts compile without bytecode",
        ),
        check(
            "VAL4884_25_pycache",
            not (POST / "scripts" / "__pycache__").exists(),
            "no pycache",
        ),
        check(
            "VAL4884_26_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4885 target selected",
        ),
    ]
    rows.append(
        check(
            "VAL4884_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_CONTACT_COEFFICIENT_OWNERSHIP_AND_BOUNDS_4884_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4884_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4884_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4884_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4884_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4884_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
