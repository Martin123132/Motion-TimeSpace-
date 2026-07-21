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

import Y5_R2FR_4891_species_hierarchy_camb_FDT_bound as research  # noqa: E402


TIMESTAMP = datetime.now(timezone.utc).isoformat()
NEXT_TARGET = research.NEXT_TARGET


def serializable(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
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


def source_rows() -> list[dict[str, Any]]:
    rows = [dict(row) for row in research.source_contract()["rows"]]
    outputs = [
        (
            "SRC4891_06_checkpoint",
            POST
            / "4891-Y5-R2FR-composite-clock-neutrino-photon-baryon-hierarchy-and-FDT-state-normalization-or-CMB-source-demotion-gate.md",
            "MTS_SPECIES_HIERARCHY_CAMB_FDT_BOUND_4891",
        ),
        (
            "SRC4891_07_formal",
            FORMAL / "907-PPC4161-species-hierarchy-CAMB-FDT-bound.md",
            "PPC4161_SPECIES_HIERARCHY_CAMB_FDT_BOUND_4891",
        ),
        (
            "SRC4891_08_claim",
            FORMAL / "02-claims-register.csv",
            "L-733",
        ),
        (
            "SRC4891_09_variables",
            FORMAL / "04-variable-audit.csv",
            "clockRoute4891_MTS",
        ),
        (
            "SRC4891_10_equations",
            FORMAL / "05-equation-register.md",
            "1.184 Standard-species source interface",
        ),
        (
            "SRC4891_11_redteam",
            FORMAL / "06-consistency-red-team.md",
            "135. An exact source interface is not a compiled parent likelihood",
        ),
        (
            "SRC4891_12_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4891",
        ),
        (
            "SRC4891_13_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_SPECIES_HIERARCHY_CAMB_FDT_BOUND_4891",
        ),
        (
            "SRC4891_14_research_script",
            SCRIPTS / "Y5_R2FR_4891_species_hierarchy_camb_FDT_bound.py",
            "def species_hierarchy_derivation",
        ),
        (
            "SRC4891_15_gate_script",
            SCRIPTS
            / "Y5_R2FR_4891_species_hierarchy_camb_FDT_bound_gate.py",
            "VAL4891_OVERALL",
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


def summary_row(section: dict[str, Any], excluded: set[str]) -> dict[str, Any]:
    return {key: value for key, value in section.items() if key not in excluded}


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    hierarchy = sections["hierarchy"]
    bridge = sections["CAMB_bridge"]
    engine = sections["hierarchy_engine"]
    response = sections["parent_response"]
    lensing = sections["lensing"]
    fdt = sections["FDT_bound"]
    hierarchy_equations = [
        {"equation_name": name, "equation": equation}
        for name, equation in hierarchy["equations"].items()
    ]
    return {
        "HIERARCHY_EQUATIONS": tagged(hierarchy_equations),
        "HIERARCHY_SUMMARY": tagged(
            [summary_row(hierarchy, {"equations"})]
        ),
        "BACKGROUND_MAPPING": tagged(sections["background_mapping"]["rows"]),
        "CAMB_BRANCHES": tagged(bridge["branch_rows"]),
        "CAMB_SPECTRA_RESIDUALS": tagged(bridge["spectra_residual_rows"]),
        "CAMB_BACKGROUND_RESIDUALS": tagged(bridge["background_rows"]),
        "CAMB_BRIDGE_SUMMARY": tagged(
            [
                summary_row(
                    bridge,
                    {"branch_rows", "spectra_residual_rows", "background_rows"},
                )
            ]
        ),
        "HIERARCHY_ENGINE": tagged(engine["rows"]),
        "HIERARCHY_ENGINE_SUMMARY": tagged(
            [summary_row(engine, {"rows", "variable_names"})]
        ),
        "PARENT_RESPONSE": tagged(response["rows"]),
        "PARENT_RESPONSE_SUMMARY": tagged(
            [summary_row(response, {"rows"})]
        ),
        "LENSING_RESPONSE": tagged(lensing["rows"]),
        "LENSING_SUMMARY": tagged([summary_row(lensing, {"rows"})]),
        "FDT_BOUNDS": tagged(fdt["rows"]),
        "FDT_SUMMARY": tagged([summary_row(fdt, {"rows"})]),
        "CMB_REQUIREMENTS": tagged(sections["arbitration"]["requirements"]),
        "ARBITRATION": tagged([sections["arbitration"]]),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "all_checks_pass": calculation["all_checks_pass"],
                    "CMB_likelihood_allowed": sections["arbitration"][
                        "CMB_likelihood_allowed"
                    ],
                    "next_target": sections["arbitration"]["next_target"],
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
    hierarchy = sections["hierarchy"]
    mappings = sections["background_mapping"]["rows"]
    bridge = sections["CAMB_bridge"]
    engine = sections["hierarchy_engine"]
    response = sections["parent_response"]
    lensing = sections["lensing"]
    fdt = sections["FDT_bound"]
    arbitration = sections["arbitration"]
    prior_validation = read_csv(
        OUTPUT / "P8_Y5_BRR545_4890_VALIDATION.csv"
    )
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-733"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    expected_statuses = {
        "Hierarchy4891_MTS": "CAMB_standard_species_hierarchy_operational",
        "PiParent4891_MTS": "parent_linear_anisotropic_stress_zero_derived",
        "OmegaEarly4891_MTS": "early_matter_calibrated_three_rays",
        "wEff4891_MTS": "positive_effective_density_PPF_background_map",
        "thetaStar4891_MTS": "three_ray_geometry_smoke_worst_shift_6p833e-4",
        "RWeyl4891_MTS": "early_silent_late_max_1p921_percent",
        "Clens4891_MTS": "Limber_lensing_suppression_0p2_to_1p24_percent",
        "XiFDT4891_MTS": (
            "one_percent_metric_budget_bound_ThetaDeltaN_lt_0p01413"
        ),
        "CMBgate4891_MTS": "five_of_eight_requirements_closed_no_CMB_claim",
        "clockRoute4891_MTS": (
            "species_background_response_bound_pass_full_LOS_state_open"
        ),
    }
    variables = {row["symbol"]: row for row in variable_rows}
    variable_counts = {
        symbol: sum(row["symbol"] == symbol for row in variable_rows)
        for symbol in expected_statuses
    }
    checkpoint = (
        POST
        / "4891-Y5-R2FR-composite-clock-neutrino-photon-baryon-hierarchy-and-FDT-state-normalization-or-CMB-source-demotion-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL / "907-PPC4161-species-hierarchy-CAMB-FDT-bound.md"
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
    all_rows = sources + [row for rows in groups.values() for row in rows]
    output_paths = [
        OUTPUT / f"P8_Y5_R2FR_4891_{name}.csv" for name in groups
    ]
    mapping_lookup = {row["target"]: row for row in mappings}
    spectra_lookup = {
        (row["target"], row["channel"]): row
        for row in bridge["spectra_residual_rows"]
    }
    response_lookup = {
        (row["k_h_per_Mpc"], row["redshift"]): row
        for row in response["rows"]
    }
    lensing_lookup = {row["ell"]: row for row in lensing["rows"]}
    requirements = {
        row["requirement"]: row for row in arbitration["requirements"]
    }
    rows = [
        check(
            "VAL4891_00_calculation",
            calculation["all_checks_pass"],
            "hierarchy CAMB bridge response lensing FDT and arbitration pass",
        ),
        check(
            "VAL4891_01_sources",
            len(sources) == 16
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            f"source rows={len(sources)}",
        ),
        check(
            "VAL4891_02_prior",
            bool(prior_validation)
            and all(row["status"] == "PASS" for row in prior_validation),
            "4890 validation remains green",
        ),
        check(
            "VAL4891_03_engine",
            sections["sources"]["CAMB_version"] == "1.6.6"
            and ".venv-score" in sections["sources"]["CAMB_python"],
            "declared local CAMB engine and interpreter",
        ),
        check(
            "VAL4891_04_hierarchy_equations",
            hierarchy["passed"] and len(hierarchy["equations"]) == 11,
            "eleven symbolic standard-species equations exported",
        ),
        check(
            "VAL4891_05_photon_baryon",
            "opacity" in hierarchy["equations"]["photon_velocity"]
            and "opacity" in hierarchy["equations"]["baryon_velocity"]
            and "polter" in hierarchy["equations"]["photon_quadrupole"],
            "Thomson drag and polarization source present",
        ),
        check(
            "VAL4891_06_neutrinos",
            "pi_r" in hierarchy["equations"]["massless_neutrino_velocity"]
            and "compiled momentum-bin" in hierarchy["massive_neutrino_owner"],
            "massless shear and massive momentum-bin owner retained",
        ),
        check(
            "VAL4891_07_parent_slots",
            "delta rho_parent" in hierarchy["parent_sources"]["density"]
            and "delta q_parent" in hierarchy["parent_sources"]["momentum"]
            and "delta p_parent" in hierarchy["parent_sources"]["pressure"],
            "parent density momentum and pressure source slots explicit",
        ),
        check(
            "VAL4891_08_parent_shear",
            not hierarchy["new_parent_anisotropic_stress"]
            and hierarchy["parent_sources"]["anisotropic_stress"]
            == "Pi_parent=0 at linear order",
            "standard species exclusively own linear slip",
        ),
        check(
            "VAL4891_09_mapping_rows",
            sections["background_mapping"]["passed"]
            and len(mappings) == 3
            and set(mapping_lookup) == set(research.prior.background.TARGETS),
            "three early-density parent mappings",
        ),
        check(
            "VAL4891_10_early_density",
            0.31496
            < mapping_lookup[1.0e-3]["early_matter_Omega"]
            < 0.31497
            and 3.45e-5
            < mapping_lookup[1.0e-3]["matter_creation_delta_Omega"]
            < 3.46e-5,
            "central early matter and bath-heating shift locked",
        ),
        check(
            "VAL4891_11_positive_residual",
            all(
                row["minimum_effective_density"] > 0.684
                and row["crosses_minus_one"]
                and row["CAMB_dark_energy_model"] == "DarkEnergyPPF"
                for row in mappings
            ),
            "positive residual with mild crossing uses PPF geometry comparator",
        ),
        check(
            "VAL4891_12_CAMB_branches",
            bridge["passed"]
            and len(bridge["branch_rows"]) == 6
            and len(bridge["spectra_residual_rows"]) == 9
            and len(bridge["background_rows"]) == 21,
            "six branches nine channel summaries and 21 H checks",
        ),
        check(
            "VAL4891_13_theta_central",
            1.24e-4
            < spectra_lookup[(1.0e-3, "TT")][
                "fractional_thetastar_shift"
            ]
            < 1.26e-4,
            "central parent acoustic shift reproduced",
        ),
        check(
            "VAL4891_14_theta_percent",
            6.82e-4
            < spectra_lookup[(1.0e-2, "TT")][
                "fractional_thetastar_shift"
            ]
            < 6.84e-4,
            "percent parent worst acoustic shift reproduced",
        ),
        check(
            "VAL4891_15_TT",
            0.0044
            < spectra_lookup[(1.0e-2, "TT")][
                "maximum_abs_fractional_residual"
            ]
            < 0.0045,
            "percent parent TT smoke residual locked",
        ),
        check(
            "VAL4891_16_EE",
            0.0058
            < spectra_lookup[(1.0e-2, "EE")][
                "maximum_abs_fractional_residual"
            ]
            < 0.0059,
            "percent parent EE smoke residual locked",
        ),
        check(
            "VAL4891_17_background_H",
            bridge["maximum_abs_fractional_H_residual"] < 4.1e-4,
            "CAMB geometry tracks parent H to 4.1e-4",
        ),
        check(
            "VAL4891_18_no_likelihood",
            not bridge["official_likelihood_run"]
            and "PPF_not_parent" in bridge["spectra_residual_rows"][0][
                "closure_label"
            ],
            "spectra remain geometry/standard-hierarchy smoke",
        ),
        check(
            "VAL4891_19_engine_rows",
            engine["passed"]
            and len(engine["rows"]) == 21
            and engine["all_finite"],
            "three k by seven redshift hierarchy transfer rows finite",
        ),
        check(
            "VAL4891_20_visibility",
            1089.0 < engine["visibility_peak_redshift"] < 1090.0
            and engine["opacity_at_z30"] < 8.4e-8,
            "recombination visibility and late opacity checked",
        ),
        check(
            "VAL4891_21_hierarchy_activity",
            engine["maximum_abs_photon_quadrupole"] > 0.24
            and engine["massless_neutrino_transfer_nonzero"]
            and engine["massive_neutrino_transfer_nonzero"],
            "photon shear and both neutrino sectors active",
        ),
        check(
            "VAL4891_22_response_rows",
            response["passed"] and len(response["rows"]) == 50,
            "five k by ten redshift parent response rows",
        ),
        check(
            "VAL4891_23_early_silence",
            response["maximum_early_abs_response"] < 2.7e-7,
            "parent Weyl response silent at z>=30",
        ),
        check(
            "VAL4891_24_late_response",
            0.0192
            < response["maximum_late_abs_response"]
            < 0.0193
            and -0.0193
            < response_lookup[(1.0e-1, 0.0)][
                "fractional_Weyl_response"
            ]
            < -0.0191,
            "late scale-dependent Weyl suppression locked",
        ),
        check(
            "VAL4891_25_response_constraint",
            response["maximum_sampled_momentum_residual"] < 2.1e-4,
            "sampled parent response preserves momentum constraint",
        ),
        check(
            "VAL4891_26_lensing_rows",
            lensing["passed"] and len(lensing["rows"]) == 8,
            "eight positive Limber parent lensing rows",
        ),
        check(
            "VAL4891_27_lensing_sign",
            all(row["fractional_lensing_shift"] < 0.0 for row in lensing["rows"])
            and -0.0125
            < lensing_lookup[10]["fractional_lensing_shift"]
            < -0.0123
            and -0.0021
            < lensing_lookup[200]["fractional_lensing_shift"]
            < -0.0020,
            "parent predicts signed lensing suppression",
        ),
        check(
            "VAL4891_28_lensing_coverage",
            lensing["minimum_parent_response_weight_fraction"] > 0.85
            and not lensing["official_lensing_likelihood"],
            "minimum kernel coverage exceeds 85 percent without likelihood claim",
        ),
        check(
            "VAL4891_29_FDT_rows",
            fdt["passed"] and len(fdt["rows"]) == 4,
            "four unit-response covariance bounds",
        ),
        check(
            "VAL4891_30_FDT_variance",
            0.0282
            < fdt["combined_equal_variance_bound"]
            < 0.0283
            and 0.1680
            < fdt["combined_equal_rms_bound"]
            < 0.1681,
            "combined normalized impulse variance and RMS bound",
        ),
        check(
            "VAL4891_31_FDT_theta",
            0.0141
            < fdt["combined_Theta_times_DeltaN_bound"]
            < 0.0142,
            "normalized Markov state bound",
        ),
        check(
            "VAL4891_32_no_fake_temperature",
            not fdt["parent_state_realized"]
            and not fdt["noise_likelihood_allowed"]
            and fdt["physical_temperature_conversion"].startswith("not allowed"),
            "physical state and temperature are not fabricated",
        ),
        check(
            "VAL4891_33_requirements",
            len(arbitration["requirements"]) == 8
            and sum(row["closed"] for row in arbitration["requirements"])
            == 5,
            "five of eight CMB promotion requirements closed",
        ),
        check(
            "VAL4891_34_open_gates",
            not requirements["late_parent_Weyl_lensing_projection"]["closed"]
            and not requirements["FDT_state_normalization"]["closed"]
            and not requirements["official_CMB_likelihood"]["closed"],
            "line of sight state and official likelihood remain open",
        ),
        check(
            "VAL4891_35_arbitration",
            arbitration["passed"]
            and not arbitration["CMB_likelihood_allowed"]
            and arbitration["local_GR_Newton_Maxwell"]
            == "4889_STATIONARY_CORRESPONDENCE_RETAINED_UNCHANGED",
            "CMB claim blocked and local correspondence retained",
        ),
        check(
            "VAL4891_36_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "standard_species_hierarchy_parent_background_geometry_and_Weyl_FDT_bounds_derived_full_LOS_state_likelihood_open_private_nonclaim",
            "L-733 unique private nonclaim status",
        ),
        check(
            "VAL4891_37_variables",
            all(
                variable_counts[symbol] == 1
                and variables[symbol]["status"] == status
                for symbol, status in expected_statuses.items()
            ),
            "ten checkpoint variables unique and status locked",
        ),
        check(
            "VAL4891_38_documents",
            "MTS_SPECIES_HIERARCHY_CAMB_FDT_BOUND_4891" in checkpoint
            and "PPC4161_SPECIES_HIERARCHY_CAMB_FDT_BOUND_4891"
            in formal_note,
            "checkpoint and formal markers",
        ),
        check(
            "VAL4891_39_registers",
            "1.184 Standard-species source interface" in equations
            and "135. An exact source interface is not a compiled parent likelihood"
            in redteam
            and "PPC4161 checkpoint 4891" in spine,
            "equation red-team and spine registers updated",
        ),
        check(
            "VAL4891_40_resume",
            "PPC4161_SPECIES_HIERARCHY_CAMB_FDT_BOUND_4891" in resume
            and NEXT_TARGET in resume,
            "resume and 4892 handoff",
        ),
        check(
            "VAL4891_41_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4891_42_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4891_43_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4891_44_scripts",
            compile_source(
                SCRIPTS / "Y5_R2FR_4891_species_hierarchy_camb_FDT_bound.py"
            )
            and compile_source(
                SCRIPTS
                / "Y5_R2FR_4891_species_hierarchy_camb_FDT_bound_gate.py"
            ),
            "research and gate scripts compile",
        ),
        check(
            "VAL4891_45_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no post-checkpoint script pycache",
        ),
        check(
            "VAL4891_46_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4892 line-of-sight and state-realization target selected",
        ),
    ]
    rows.append(
        check(
            "VAL4891_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_SPECIES_HIERARCHY_CAMB_FDT_BOUND_4891_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4891_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4891_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4891_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4891_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4891_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
