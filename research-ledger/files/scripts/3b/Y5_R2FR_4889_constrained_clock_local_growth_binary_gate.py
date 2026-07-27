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

import Y5_R2FR_4889_constrained_clock_local_growth_binary as research  # noqa: E402


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
    output_sources = [
        (
            "SRC4889_09_checkpoint",
            POST
            / "4889-Y5-R2FR-nonlocal-bath-retarded-kernel-causal-front-growth-and-binary-leakage-or-expansion-source-demotion-gate.md",
            "MTS_CONSTRAINED_CLOCK_LOCAL_GROWTH_BINARY_4889",
        ),
        (
            "SRC4889_10_formal_note",
            FORMAL / "905-PPC4161-constrained-clock-local-growth-binary.md",
            "PPC4161_CONSTRAINED_CLOCK_LOCAL_GROWTH_BINARY_4889",
        ),
        (
            "SRC4889_11_claim",
            FORMAL / "02-claims-register.csv",
            "L-731",
        ),
        (
            "SRC4889_12_variables",
            FORMAL / "04-variable-audit.csv",
            "clockRoute_4889_MTS",
        ),
        (
            "SRC4889_13_equations",
            FORMAL / "05-equation-register.md",
            "1.182 Constrained clock parent and local cone reduction",
        ),
        (
            "SRC4889_14_redteam",
            FORMAL / "06-consistency-red-team.md",
            "133. A constraint can remove a wave but not the zero mode",
        ),
        (
            "SRC4889_15_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4889",
        ),
        (
            "SRC4889_16_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_CONSTRAINED_CLOCK_LOCAL_GROWTH_BINARY_4889",
        ),
    ]
    for source_id, path, marker in output_sources:
        exists = path.exists()
        content = (
            path.read_text(encoding="utf-8", errors="replace")
            if exists
            else ""
        )
        rows.append(
            {
                "source_id": source_id,
                "source_type": "generated_local_text",
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
    health = sections["background_health"]
    growth = sections["growth"]
    growth_data = sections["growth_data"]
    binary = sections["binary"]
    return {
        "PARENT": tagged([sections["parent"]]),
        "BACKGROUND_HEALTH": tagged(health["rows"]),
        "BACKGROUND_SUMMARY": tagged([summary_row(health, {"rows"})]),
        "CHARACTERISTICS": tagged([sections["characteristics"]]),
        "GROWTH_RESPONSE": tagged(growth["rows"]),
        "GROWTH_SUMMARY": tagged([summary_row(growth, {"rows"})]),
        "GROWTH_DATA_SCORES": tagged(growth_data["scores"]),
        "GROWTH_DATA_COMPARISONS": tagged(growth_data["comparisons"]),
        "GROWTH_DATA_PREDICTIONS": tagged(growth_data["predictions"]),
        "GROWTH_DATA_SUMMARY": tagged(
            [
                summary_row(
                    growth_data, {"scores", "comparisons", "predictions"}
                )
            ]
        ),
        "LOCAL_GR_NEWTON_MAXWELL": tagged([sections["local"]]),
        "BINARY_BOUNDS": tagged(binary["rows"]),
        "BINARY_SUMMARY": tagged([summary_row(binary, {"rows"})]),
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
    parent = sections["parent"]
    health = sections["background_health"]
    characteristics = sections["characteristics"]
    growth = sections["growth"]
    growth_data = sections["growth_data"]
    local = sections["local"]
    binary = sections["binary"]
    arbitration = sections["arbitration"]
    prior_validation = read_csv(
        OUTPUT / "P8_Y5_BRR545_4888_VALIDATION.csv"
    )
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-731"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    expected_statuses = {
        "Uclock_4889_MTS": "fixed_norm_parent_clock_selected_private",
        "varrho_clock_4889_MTS": "positive_on_three_backreacted_rays",
        "Bclock_inertia_MTS": "positive_all_rays_minimum_0p218",
        "charpoly_clock_4889_MTS": (
            "symbolically_derived_memory_luminal_clock_zero_mode"
        ),
        "growth_constraint_4889_MTS": "derived_subhorizon_two_component_kernel",
        "growth_score_4889_MTS": (
            "primary_and_robustness_real_covariance_smoke_nonclaim"
        ),
        "binary_leak_4889_MTS": "finite_frequency_power_counting_bounded",
        "local_correspondence_4889_MTS": (
            "conditional_stationary_local_reduction_derived"
        ),
        "clockRoute_4889_MTS": (
            "cone_obstruction_closed_background_growth_local_limits_pass_bath_identity_open"
        ),
    }
    variables = {row["symbol"]: row for row in variable_rows}
    variable_counts = {
        symbol: sum(row["symbol"] == symbol for row in variable_rows)
        for symbol in expected_statuses
    }
    checkpoint = (
        POST
        / "4889-Y5-R2FR-nonlocal-bath-retarded-kernel-causal-front-growth-and-binary-leakage-or-expansion-source-demotion-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL / "905-PPC4161-constrained-clock-local-growth-binary.md"
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
        OUTPUT / f"P8_Y5_R2FR_4889_{name}.csv" for name in groups
    ]
    health_by_target = {
        row["target_Omega_memory_today"]: row for row in health["rows"]
    }
    comparison_lookup = {
        (row["file_set"], row["model"]): row
        for row in growth_data["comparisons"]
    }
    rows = [
        check(
            "VAL4889_00_calculation",
            calculation["all_checks_pass"],
            "parent health characteristics growth data local and binary sections pass",
        ),
        check(
            "VAL4889_01_sources",
            len(sources) == 17
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            f"source rows={len(sources)}",
        ),
        check(
            "VAL4889_02_prior",
            bool(prior_validation)
            and all(row["status"] == "PASS" for row in prior_validation),
            "4888 validation remains green",
        ),
        check(
            "VAL4889_03_parent_action",
            parent["passed"]
            and "varrho" in parent["parent_action"]
            and "sigma_theta" in parent["parent_action"],
            "fixed-norm clock and memory coupling share one action",
        ),
        check(
            "VAL4889_04_constraint_source",
            parent["constraint_equation"] == "U_mu U^mu=-1"
            and "theta=-Box U" in parent["memory_equation"],
            "unit flow and expansion source follow by variation",
        ),
        check(
            "VAL4889_05_current_stress",
            "J_U" in parent["clock_current"]
            and "T_clock+sigma" in parent["stress_tensor"]
            and not parent["new_arena_switch"],
            "clock current and stress are owned without an arena switch",
        ),
        check(
            "VAL4889_06_background_health",
            health["passed"]
            and len(health["rows"]) == 3
            and set(health_by_target) == set(research.prior.TARGETS),
            "all three 4888 backgrounds mapped to constrained parent",
        ),
        check(
            "VAL4889_07_multiplier",
            min(
                row["minimum_multiplier_density_over_rhocrit0"]
                for row in health["rows"]
            )
            > 0.0406,
            "clock multiplier stays positive",
        ),
        check(
            "VAL4889_08_inertia",
            0.218
            < health_by_target[1.0e-2][
                "minimum_effective_clock_inertia_factor"
            ]
            < 0.219
            and all(row["positive_effective_inertia"] for row in health["rows"]),
            "constraint inertia remains positive on percent ray",
        ),
        check(
            "VAL4889_09_symbolic_characteristic",
            characteristics["passed"]
            and characteristics["symbolic_determinant_verified"]
            and "omega**2" in characteristics["characteristic_polynomial"],
            "principal determinant is symbolically evaluated",
        ),
        check(
            "VAL4889_10_mode_content",
            characteristics["propagating_memory_speed_squared"] == 1.0
            and characteristics["clock_sound_speed_squared"] == 0.0
            and not characteristics["upper_superluminal_clock_memory_root"],
            "luminal memory plus constrained dust zero mode",
        ),
        check(
            "VAL4889_11_public_cones",
            characteristics["tensor_speed_squared"] == 1.0
            and characteristics["Maxwell_speed_squared"] == 1.0,
            "tensor and Maxwell principal cones remain public metric",
        ),
        check(
            "VAL4889_12_generic_clock_demoted",
            "demoted" in characteristics["generic_PX_clock_branch"]
            and arbitration["generic_PX_clock"].startswith("DEMOTED"),
            "4888 generic P(X) root is not relabeled safe",
        ),
        check(
            "VAL4889_13_growth_equations",
            growth["passed"]
            and "B_N/B" in growth["subhorizon_equations"]
            and "sigma_bar^2" in growth["inertia_factor"],
            "two-component constrained growth kernel derived",
        ),
        check(
            "VAL4889_14_growth_rows",
            len(growth["rows"]) == 12
            and growth["maximum_abs_fractional_D_shift"] < 0.021
            and growth["maximum_abs_fractional_f_shift"] < 0.112,
            "growth response finite with explicit non-negligible size",
        ),
        check(
            "VAL4889_15_growth_score_shapes",
            growth_data["passed"]
            and len(growth_data["scores"]) == 8
            and len(growth_data["comparisons"]) == 6
            and len(growth_data["predictions"]) == 116,
            "primary and robustness covariance branches scored separately",
        ),
        check(
            "VAL4889_16_growth_profiles",
            all(
                row["success"]
                and not row["edge_flag"]
                and row["n_profiled_parameters"] == 2
                for row in growth_data["scores"]
            ),
            "q and sigma8 profiles converge without edges",
        ),
        check(
            "VAL4889_17_primary_comparison",
            all(
                comparison_lookup[("BAO_plus_primary", f"MTS_constrained_{target:.0e}")][
                    "delta_chi2_MTS_minus_LCDM"
                ]
                < 0.0
                for target in research.prior.TARGETS
            )
            and -1.0
            < comparison_lookup[("BAO_plus_primary", "MTS_constrained_1e-03")][
                "delta_chi2_MTS_minus_LCDM"
            ]
            < -0.95,
            "all primary rows modestly improve matched LCDM",
        ),
        check(
            "VAL4889_18_robustness_comparison",
            all(
                comparison_lookup[("full_shape_robustness", f"MTS_constrained_{target:.0e}")][
                    "delta_chi2_MTS_minus_LCDM"
                ]
                < 0.0
                for target in research.prior.TARGETS
            )
            and -1.06
            < comparison_lookup[("full_shape_robustness", "MTS_constrained_1e-03")][
                "delta_chi2_MTS_minus_LCDM"
            ]
            < -1.02,
            "independent full-shape compression keeps same ordering",
        ),
        check(
            "VAL4889_19_growth_nonclaim",
            all(
                not row["stable_evidence_allowed"]
                for row in growth_data["comparisons"]
            )
            and "no CMB" in growth_data["theory_scope"],
            "profiled growth smoke is not promoted to evidence",
        ),
        check(
            "VAL4889_20_local_reduction",
            local["passed"]
            and "delta T" in local["extra_stress"]
            and local["PPN_gamma"] == 1.0
            and local["PPN_beta"] == 1.0,
            "stationary extra stress vanishes and PPN values are GR",
        ),
        check(
            "VAL4889_21_Newton",
            "4 pi G_N" in local["Newton_limit"]
            and "8 pi Mbar_Pl^2" in local["Newton_limit"],
            "calibrated Newton coefficient retained",
        ),
        check(
            "VAL4889_22_Maxwell",
            "F_mn F^mn" in local["Maxwell_action"]
            and "T_EM" in local["Maxwell_stress"]
            and local["direct_phi_or_clock_charge_of_EM"] == 0.0,
            "minimal Maxwell Hilbert stress and no direct clock charge",
        ),
        check(
            "VAL4889_23_Poynting",
            local["Poynting_readout"] == "S^i=-T_EM^i_0 in the local observer frame",
            "Poynting vector belongs to standard EM stress",
        ),
        check(
            "VAL4889_24_local_background",
            local["cosmic_background_suppression_AU"] < 1.3e-30
            and local["cosmic_background_suppression_Rsun"] < 3.0e-35,
            "cosmic clock background is derivative suppressed locally",
        ),
        check(
            "VAL4889_25_binary",
            binary["passed"]
            and len(binary["rows"]) == 5
            and not binary["resonant_clock_pole"],
            "five finite-frequency systems bounded without a clock pole",
        ),
        check(
            "VAL4889_26_binary_envelope",
            binary["largest_metric_amplitude_envelope"] < 3.0e-23
            and binary["largest_metric_amplitude_envelope"] > 2.8e-23,
            "memory plus cosmic-clock envelope is explicit",
        ),
        check(
            "VAL4889_27_arbitration",
            arbitration["passed"]
            and arbitration["selected_clock_parent"]
            == "FIXED_NORM_IRROTATIONAL_CONSTRAINED_BATH_CLOCK"
            and "bath identity" in arbitration["remaining_root_risk"],
            "route selected with unresolved identity recorded",
        ),
        check(
            "VAL4889_28_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "constrained_clock_parent_cone_local_Newton_Maxwell_growth_and_binary_bounds_derived_bath_identity_full_CMB_open_private_nonclaim",
            "L-731 unique and nonclaim status locked",
        ),
        check(
            "VAL4889_29_variables",
            all(
                variable_counts[symbol] == 1
                and variables[symbol]["status"] == status
                for symbol, status in expected_statuses.items()
            ),
            "nine constrained-clock variables unique and status locked",
        ),
        check(
            "VAL4889_30_documents",
            "MTS_CONSTRAINED_CLOCK_LOCAL_GROWTH_BINARY_4889" in checkpoint
            and "PPC4161_CONSTRAINED_CLOCK_LOCAL_GROWTH_BINARY_4889"
            in formal_note,
            "checkpoint and formal note markers",
        ),
        check(
            "VAL4889_31_registers",
            "1.182 Constrained clock parent and local cone reduction"
            in equations
            and "133. A constraint can remove a wave but not the zero mode"
            in redteam
            and "PPC4161 checkpoint 4889" in spine,
            "equation red-team and spine updated",
        ),
        check(
            "VAL4889_32_resume",
            "PPC4161_CONSTRAINED_CLOCK_LOCAL_GROWTH_BINARY_4889" in resume
            and NEXT_TARGET in resume,
            "resume and 4890 handoff",
        ),
        check(
            "VAL4889_33_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4889_34_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4889_35_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4889_36_scripts",
            compile_source(
                SCRIPTS / "Y5_R2FR_4889_constrained_clock_local_growth_binary.py"
            )
            and compile_source(
                SCRIPTS
                / "Y5_R2FR_4889_constrained_clock_local_growth_binary_gate.py"
            ),
            "research and gate scripts compile",
        ),
        check(
            "VAL4889_37_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no post-checkpoint script pycache",
        ),
        check(
            "VAL4889_38_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4890 full perturbation and bath identity target selected",
        ),
    ]
    rows.append(
        check(
            "VAL4889_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_CONSTRAINED_CLOCK_LOCAL_GROWTH_BINARY_4889_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4889_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4889_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4889_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4889_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4889_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
