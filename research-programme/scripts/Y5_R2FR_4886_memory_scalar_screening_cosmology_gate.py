from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

from Y5_R2FR_4886_memory_scalar_screening_cosmology import (
    BETA_ANCHOR,
    CASSINI_TWO_SIGMA_ABS_CEILING,
    NEXT_TARGET,
    result,
)


CHECKPOINT = "4886"
TIMESTAMP = "2026-07-11T00:45:41+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
EOS_ROOT = POST / "source-intake" / "microphysical_eos" / "4883" / "lalsuite"
PDF_ROOT = POST / "source-intake" / "memory_uv" / "4886"


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
    return digest.hexdigest().upper()


def source_rows() -> list[dict[str, Any]]:
    local_text = [
        (
            "SRC4886_00_checkpoint",
            POST
            / "4886-Y5-R2FR-canonical-memory-scalar-local-screening-scalarization-and-same-parent-cosmology-compatibility-gate.md",
            "MTS_MEMORY_SCALAR_SCREENING_COSMOLOGY_4886",
        ),
        (
            "SRC4886_01_research_script",
            POST
            / "scripts"
            / "Y5_R2FR_4886_memory_scalar_screening_cosmology.py",
            "MTS_MEMORY_SCALAR_SCREENING_COSMOLOGY_4886",
        ),
        (
            "SRC4886_02_gate_script",
            POST
            / "scripts"
            / "Y5_R2FR_4886_memory_scalar_screening_cosmology_gate.py",
            "P8_Y5_BRR545_4886_VALIDATION_PASS",
        ),
        (
            "SRC4886_03_formal_note",
            FORMAL
            / "902-PPC4161-memory-scalar-screening-and-cosmology-compatibility.md",
            "PPC4161_MEMORY_SCALAR_COMPATIBILITY_4886",
        ),
        (
            "SRC4886_04_claims",
            FORMAL / "02-claims-register.csv",
            "L-728",
        ),
        (
            "SRC4886_05_variables",
            FORMAL / "04-variable-audit.csv",
            "active_M_compatibility_4886_MTS",
        ),
        (
            "SRC4886_06_equations",
            FORMAL / "05-equation-register.md",
            "1.179 Memory-scalar charge and PPN--cosmology compatibility",
        ),
        (
            "SRC4886_07_redteam",
            FORMAL / "06-consistency-red-team.md",
            "130. A negative local Hessian is not a global scalarization proof",
        ),
        (
            "SRC4886_08_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4886",
        ),
        (
            "SRC4886_09_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_MEMORY_SCALAR_COMPATIBILITY_4886",
        ),
        (
            "SRC4886_10_prior_checkpoint",
            POST
            / "4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-from-closed-bath-or-three-boson-branch-demotion-gate.md",
            "MTS_GAMMA_MEMORY_UV_OPERATOR_AND_BRANCH_ARBITRATION_4885",
        ),
        (
            "SRC4886_11_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4885_VALIDATION.csv",
            "VAL4885_OVERALL,PASS",
        ),
        (
            "SRC4886_12_memory_action",
            ROOT
            / "cosmology"
            / "activation-cosmology"
            / "frw-background-and-linear-perturbations-for-the-curvature-memory-field-with-interaction-b-t-m-2.md",
            "b T M^2",
        ),
        (
            "SRC4886_13_memory_minimum",
            ROOT
            / "cosmology"
            / "activation-cosmology"
            / "cosmology-branch-of-the-curvature-memory-theory-derived-from-the-action-with-interaction-term-b-t-m-2.md",
            "M_*^2 = 2",
        ),
        (
            "SRC4886_14_sign_branch",
            ROOT
            / "cosmology"
            / "activation-cosmology"
            / "sign-of-the-coupling-b.md",
            "b < 0",
        ),
        (
            "SRC4886_15_EOS_targets",
            OUTPUT / "P8_Y5_R2FR_4883_TARGET_LOCATIONS.csv",
            "canonical_1p4",
        ),
        (
            "SRC4886_16_EOS_validation",
            OUTPUT / "P8_Y5_BRR545_4883_VALIDATION.csv",
            "VAL4883_OVERALL,PASS",
        ),
        (
            "SRC4886_17_EOS_script",
            POST / "scripts" / "Y5_R2FR_4883_multi_eos_tov_love_response.py",
            "class TabulatedEOS",
        ),
        (
            "SRC4886_18_Cassini_source_pack",
            POST
            / "1181-Y5-R10-PPN-KS-residual-vector-source-pack-or-parent-Q-identity-proof.md",
            "gamma = 1 + (2.1 +/- 2.3) x 10^-5",
        ),
        (
            "SRC4886_19_local_GR_certificate",
            POST
            / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
            "gamma_{\\rm classical}=1",
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

    hashed_files = [
        (
            "SRC4886_20_DEF_primary_pdf",
            PDF_ROOT / "Damour_Esposito_Farese_gr-qc_9602056.pdf",
            "134CDC406BBC5E03A65251FED0E4A703C2842CFEB0E4E9471E0F0034EB301DFA",
            "local_primary_pdf",
        ),
        (
            "SRC4886_21_BSK24_table",
            EOS_ROOT / "BSK24.dat",
            "78E6047B0A7724B350692B816F0D6181C49341847351E2A9A5E26B940F62AA1D",
            "local_EOS_table",
        ),
        (
            "SRC4886_22_SLY4_table",
            EOS_ROOT / "SLY4.dat",
            "475B77304C6DA7253699C3CF48AD5A06BB637178F9615267CC0C6E6B41CC0B75",
            "local_EOS_table",
        ),
        (
            "SRC4886_23_DD2_table",
            EOS_ROOT / "DD2.dat",
            "7C9B5B5B3B50219D35E8A302D596B2B08DF193CB62C17386CDD969174390D1FE",
            "local_EOS_table",
        ),
    ]
    for source_id, path, expected_hash, source_type in hashed_files:
        exists = path.exists()
        digest = sha256(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_type": source_type,
                "source_path": str(path),
                "source_exists": exists,
                "marker": "sha256",
                "marker_found": digest == expected_hash,
                "verification_method": "sha256",
                "sha256": digest,
                "expected_sha256": expected_hash,
            }
        )

    for source_id, url, marker in (
        (
            "SRC4886_24_Cassini_web",
            "https://doi.org/10.1038/nature01997",
            "primary Cassini gamma measurement",
        ),
        (
            "SRC4886_25_DEF_web",
            "https://arxiv.org/abs/gr-qc/9602056",
            "primary tensor-scalar and scalarization formalism",
        ),
    ):
        rows.append(
            {
                "source_id": source_id,
                "source_type": "web_primary",
                "source_path": url,
                "source_exists": True,
                "marker": marker,
                "marker_found": True,
                "verification_method": "primary_source_recorded",
            }
        )
    return tagged(rows)


def summary_row(section: dict[str, Any], excluded: set[str]) -> dict[str, Any]:
    return {key: value for key, value in section.items() if key not in excluded}


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    return {
        "PARENT_COMPLETION": tagged([sections["parent_completion"]]),
        "STELLAR_PROFILES": tagged(sections["stellar_profiles"]["rows"]),
        "STELLAR_SUMMARY": tagged(
            [summary_row(sections["stellar_profiles"], {"rows"})]
        ),
        "WEAK_SOURCE_RANGE": tagged([sections["weak_source_range"]]),
        "PPN_COSMOLOGY_SCENARIOS": tagged(
            sections["PPN_cosmology_link"]["scenarios"]
        ),
        "PPN_COSMOLOGY_SUMMARY": tagged(
            [summary_row(sections["PPN_cosmology_link"], {"scenarios"})]
        ),
        "FLRW_MODES": tagged(sections["FLRW_dynamics"]["mode_rows"]),
        "FLRW_SUMMARY": tagged(
            [summary_row(sections["FLRW_dynamics"], {"mode_rows"})]
        ),
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
    parent = sections["parent_completion"]
    stars = sections["stellar_profiles"]
    weak = sections["weak_source_range"]
    link = sections["PPN_cosmology_link"]
    flrw = sections["FLRW_dynamics"]
    arbitration = sections["arbitration"]
    prior_4885 = read_csv(OUTPUT / "P8_Y5_BRR545_4885_VALIDATION.csv")
    prior_4883 = read_csv(OUTPUT / "P8_Y5_BRR545_4883_VALIDATION.csv")

    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-728"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    expected_statuses = {
        "beta_trace_MTS": (
            "dimensionless_anchor_minus_1_over_18_covariant_owner_tested"
        ),
        "A_trace_owner_MTS": (
            "minimal_universal_conformal_completion_selected_for_gate"
        ),
        "Q_M_NS_4886_MTS": "nine_EOS_scalar_charge_profiles_derived",
        "beta_scalarization_crit_MTS": (
            "first_global_zero_mode_threshold_derived"
        ),
        "B0_memory_growth_MTS": "Cassini_linked_below_7p54e_minus5",
        "lambdaM_ambient_MTS": (
            "cosmological_range_no_local_Yukawa_screening"
        ),
        "active_M_compatibility_4886_MTS": (
            "significant_trace_driven_cosmology_rejected_minimal_owner"
        ),
    }
    variables = {row["symbol"]: row for row in variable_rows}
    variable_counts = {
        symbol: sum(row["symbol"] == symbol for row in variable_rows)
        for symbol in expected_statuses
    }

    checkpoint = (
        POST
        / "4886-Y5-R2FR-canonical-memory-scalar-local-screening-scalarization-and-same-parent-cosmology-compatibility-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL
        / "902-PPC4161-memory-scalar-screening-and-cosmology-compatibility.md"
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
        OUTPUT / f"P8_Y5_R2FR_4886_{name}.csv" for name in groups
    ]
    scenario_by_name = {
        row["scenario"]: row for row in link["scenarios"]
    }

    rows = [
        check(
            "VAL4886_00_calculation",
            calculation["all_checks_pass"],
            "parent stellar weak-source PPN and FLRW sections pass",
        ),
        check(
            "VAL4886_01_sources",
            len(sources) == 26
            and all(row["source_exists"] and row["marker_found"] for row in sources),
            f"sources={len(sources)}",
        ),
        check(
            "VAL4886_02_hashes",
            all(
                row.get("sha256") == row.get("expected_sha256")
                for row in sources
                if row["source_type"] in {"local_primary_pdf", "local_EOS_table"}
            ),
            "DEF PDF and three EOS tables hash locked",
        ),
        check(
            "VAL4886_03_prior",
            bool(prior_4885)
            and bool(prior_4883)
            and all(row["status"] == "PASS" for row in prior_4885)
            and all(row["status"] == "PASS" for row in prior_4883),
            "4885 memory ownership and 4883 EOS validation remain green",
        ),
        check(
            "VAL4886_04_parent_completion",
            parent["passed"]
            and parent["conformal_factor"] == "A(phi)=exp(beta*phi^2)"
            and parent["alpha_DEF"] == "2*sqrt(2)*beta*phi"
            and "-8*pi" in parent["scalar_equation"],
            "minimal covariant owner and field normalization",
        ),
        check(
            "VAL4886_05_matter_exchange",
            "nabla_mu" in parent["matter_exchange"]
            and "rho_m_dot" in parent["dust_continuity"],
            "trace interaction does not silently retain separate dust conservation",
        ),
        check(
            "VAL4886_06_spherical_equation",
            "rho-3p" in stars["equation"]
            and "Schwarzschild exterior" in stars["boundary_conditions"]
            and "4*beta*M" in stars["charge_definition"],
            "regular-center equation exact exterior and charge map",
        ),
        check(
            "VAL4886_07_nine_models",
            len(stars["rows"]) == 9
            and {row["eos_id"] for row in stars["rows"]}
            == {"BSK24", "SLY4", "DD2"}
            and all(
                abs(row["computed_mass_Msun"] / row["reference_mass_Msun"] - 1)
                < 1.0e-8
                and abs(row["computed_radius_km"] / row["reference_radius_km"] - 1)
                < 2.0e-8
                for row in stars["rows"]
            ),
            "three masses across each of three microphysical EOS families",
        ),
        check(
            "VAL4886_08_charge_range",
            all(0.32 < row["scalar_charge_ratio"] < 0.76 for row in stars["rows"])
            and min(row["field_center_over_infinity"] for row in stars["rows"])
            > 1,
            "finite scalar charges without anchor divergence",
        ),
        check(
            "VAL4886_09_zero_modes",
            all(row["zero_branch_globally_stable_at_anchor"] for row in stars["rows"])
            and -1.44 < min(row["first_beta_scalarization"] for row in stars["rows"])
            and max(row["first_beta_scalarization"] for row in stars["rows"])
            < -1.08
            and stars["minimum_threshold_margin"] > 19.5,
            "anchor lies at least nineteen-fold below first zero modes",
        ),
        check(
            "VAL4886_10_DEF_thresholds",
            all(
                abs(row["first_beta_DEF_scalarization"] - 4 * row["first_beta_scalarization"])
                < 1.0e-12
                for row in stars["rows"]
            )
            and min(row["first_beta_DEF_scalarization"] for row in stars["rows"])
            < -5.7,
            "canonical-to-DEF normalization remains exact",
        ),
        check(
            "VAL4886_11_trace_profiles",
            any(row["minimum_trace_Lsun_minus2"] < 0 for row in stars["rows"])
            and all(
                row["trace_positive_volume_fraction"] > 0.94
                for row in stars["rows"]
            ),
            "sign-changing high-mass traces retained rather than dust substituted",
        ),
        check(
            "VAL4886_12_convergence",
            stars["maximum_charge_convergence_error"] < 1.3e-6,
            "coarse/fine scalar charges converge",
        ),
        check(
            "VAL4886_13_ambient_quartic",
            max(
                row["ambient_quartic_to_central_trace_ratio"]
                for row in stars["rows"]
            )
            < 1.0e-40,
            "ambient quartic does not alter stellar-core onset solutions",
        ),
        check(
            "VAL4886_14_solar",
            weak["passed"]
            and abs(weak["solar_charge_ratio"] - 1) < 1.0e-6
            and weak["ambient_mass_times_AU"] < 1.0e-14,
            "Sun unscreened and no Solar-System Yukawa attenuation",
        ),
        check(
            "VAL4886_15_range",
            weak["ambient_compton_Mpc"] > 2.4e4
            and weak["AU_screening_to_cosmological_mass_ratio"] > 5.0e15,
            "cosmological range and one-AU mass incompatibility",
        ),
        check(
            "VAL4886_16_PPN_identity",
            link["passed"]
            and link["standard_scalar_coupling"]
            == "alpha_DEF^2=8*abs(beta)*B0"
            and link["conservative_two_sigma_abs_ceiling"]
            == CASSINI_TWO_SIGMA_ABS_CEILING,
            "same B0 fixes cosmological growth and PPN coupling",
        ),
        check(
            "VAL4886_17_Cassini_bound",
            7.5e-5 < link["B0_max"] < 7.6e-5
            and link["maximum_large_scale_growth_suppression"] == link["B0_max"],
            "conservative same-branch B0 ceiling",
        ),
        check(
            "VAL4886_18_growth_scenarios",
            scenario_by_name["one_percent_growth_target"]["Cassini_ceiling_ratio"]
            > 132
            and scenario_by_name["five_percent_growth_target"]["Cassini_ceiling_ratio"]
            > 648
            and not scenario_by_name["one_percent_growth_target"]["Cassini_allowed"],
            "percent-level direct-trace growth rejected",
        ),
        check(
            "VAL4886_19_FLRW_modes",
            flrw["passed"]
            and len(flrw["mode_rows"]) == 2
            and flrw["mode_rows"][0]["growing_exponent"] < 0.04
            and flrw["mode_rows"][1]["growing_exponent"] < 0.2,
            "small-field matter-era evolution derived",
        ),
        check(
            "VAL4886_20_recombination",
            flrw["B_at_recombination_if_tracking"] > 1.0e5
            and flrw["B0_for_abs_lnA_recombination_below_0p01"] < 7.5e-12
            and flrw["Cassini_B0_over_recombination_perturbative_ceiling"]
            > 1.0e7,
            "minimum-tracking truncation failure exposed",
        ),
        check(
            "VAL4886_21_arbitration",
            arbitration["passed"]
            and not arbitration["anchor_neutron_star_scalarization"]
            and not arbitration["anchor_solar_screening"]
            and "REJECTED" in arbitration["significant_active_M_growth_branch"]
            and arbitration["canonical_M_UV_determinant"] == "RETAINED"
            and arbitration["Gamma_overdamped_readout"] == "RETAINED",
            "direct-trace cosmology rejected without discarding memory operator",
        ),
        check(
            "VAL4886_22_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4886_23_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all checkpoint evidence remains private and nonclaim",
        ),
        check(
            "VAL4886_24_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4886_25_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "nine_EOS_global_scalarization_absent_anchor_unscreened_solar_long_range_PPN_B0_bound_significant_bTM2_cosmology_rejected_minimal_owner_private_nonclaim",
            "L-728 unique and scope locked",
        ),
        check(
            "VAL4886_26_variables",
            all(
                variable_counts[symbol] == 1
                and variables[symbol]["status"] == status
                for symbol, status in expected_statuses.items()
            ),
            "seven compatibility variables unique and status locked",
        ),
        check(
            "VAL4886_27_documents",
            "MTS_MEMORY_SCALAR_SCREENING_COSMOLOGY_4886" in checkpoint
            and "PPC4161_MEMORY_SCALAR_COMPATIBILITY_4886" in formal_note,
            "checkpoint and formal-note markers",
        ),
        check(
            "VAL4886_28_registers",
            "1.179 Memory-scalar charge and PPN--cosmology compatibility"
            in equations
            and "130. A negative local Hessian is not a global scalarization proof"
            in redteam
            and "PPC4161 checkpoint 4886" in spine,
            "equation red-team and spine updates",
        ),
        check(
            "VAL4886_29_resume",
            "PPC4161_MEMORY_SCALAR_COMPATIBILITY_4886" in resume
            and NEXT_TARGET in resume,
            "resume handoff",
        ),
        check(
            "VAL4886_30_scripts",
            compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4886_memory_scalar_screening_cosmology.py"
            )
            and compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4886_memory_scalar_screening_cosmology_gate.py"
            ),
            "research and gate scripts compile without bytecode",
        ),
        check(
            "VAL4886_31_pycache",
            not (POST / "scripts" / "__pycache__").exists(),
            "no pycache",
        ),
        check(
            "VAL4886_32_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4887 target selected",
        ),
        check(
            "VAL4886_33_anchor",
            abs(BETA_ANCHOR + 1 / 18) < 1.0e-15,
            "diagnostic anchor locked",
        ),
    ]
    rows.append(
        check(
            "VAL4886_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_MEMORY_SCALAR_SCREENING_COSMOLOGY_4886_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4886_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4886_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4886_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4886_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4886_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
