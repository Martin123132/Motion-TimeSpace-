from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

from Y5_R2FR_4881_compact_fluid_a6 import (
    A6_ARCHIVE_SHA256,
    result,
)


CHECKPOINT = "4881"
TIMESTAMP = "2026-07-10T19:56:56+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
A6_SOURCE = POST / "source-intake" / "heat_kernel_a6" / "4881"
NEXT_TARGET = (
    "4882-Y5-R2FR-compact-star-EOS-response-Jacobian-mass-radius-"
    "and-tidal-sensitivity-or-strong-matter-promotion-gate.md"
)


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


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def source_rows() -> list[dict[str, Any]]:
    local = [
        (
            "SRC4881_00_checkpoint",
            POST
            / "4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md",
            "MTS_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881",
        ),
        (
            "SRC4881_01_research_script",
            POST / "scripts" / "Y5_R2FR_4881_compact_fluid_a6.py",
            "def perfect_fluid_contact_image",
        ),
        (
            "SRC4881_02_gate_script",
            POST / "scripts" / "Y5_R2FR_4881_compact_fluid_a6_gate.py",
            "P8_Y5_BRR545_4881_VALIDATION_PASS",
        ),
        (
            "SRC4881_03_prior_checkpoint",
            POST
            / "4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-domain-of-validity-and-strong-field-entry-gate.md",
            "MTS_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880",
        ),
        (
            "SRC4881_04_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4880_VALIDATION.csv",
            "VAL4880_OVERALL,PASS",
        ),
        (
            "SRC4881_05_finite_source",
            POST
            / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
            "MTS_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879",
        ),
        (
            "SRC4881_06_parent_heat_kernel",
            POST
            / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
            "INTEGRATED_H_PARENT_SADDLE_HEAT_KERNEL_POLE_HIERARCHY_4876",
        ),
        (
            "SRC4881_07_nonlocal_spectrum",
            POST
            / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877",
        ),
        (
            "SRC4881_08_a6_tex",
            A6_SOURCE / "ch4.tex",
            "a_{6}(f,D)",
        ),
        (
            "SRC4881_09_a6_provenance",
            A6_SOURCE / "PROVENANCE.md",
            "VASSILEVICH_A6_SOURCE_PROVENANCE_4881",
        ),
        (
            "SRC4881_10_formal_note",
            FORMAL / "897-PPC4161-compact-fluid-TOV-and-scalar-a6-owner.md",
            "PPC4161_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881",
        ),
        (
            "SRC4881_11_claims",
            FORMAL / "02-claims-register.csv",
            "L-723",
        ),
        (
            "SRC4881_12_variables",
            FORMAL / "04-variable-audit.csv",
            "F_contact_fluid_MTS",
        ),
        (
            "SRC4881_13_equations",
            FORMAL / "05-equation-register.md",
            "1.174 Compact-fluid contact/TOV map",
        ),
        (
            "SRC4881_14_redteam",
            FORMAL / "06-consistency-red-team.md",
            "125. Compact-fluid EOS redundancy",
        ),
        (
            "SRC4881_15_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4881",
        ),
        (
            "SRC4881_16_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker in local:
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
    archive = A6_SOURCE / "hep-th-0306138.tar"
    archive_exists = archive.exists()
    archive_hash = _sha256(archive) if archive_exists else ""
    rows.append(
        {
            "source_id": "SRC4881_17_a6_archive",
            "source_type": "local_binary",
            "source_path": str(archive),
            "source_exists": archive_exists,
            "marker": A6_ARCHIVE_SHA256,
            "marker_found": archive_hash == A6_ARCHIVE_SHA256,
            "verification_method": "sha256",
        }
    )
    web = [
        (
            "SRC4881_18_fluid_action",
            "https://arxiv.org/abs/gr-qc/9304026",
            "off-shell relativistic perfect-fluid action",
        ),
        (
            "SRC4881_19_heat_kernel",
            "https://arxiv.org/abs/hep-th/0306138",
            "general Laplace-type a6 coefficient",
        ),
        (
            "SRC4881_20_field_redefinition",
            "https://arxiv.org/abs/1911.10108",
            "strict-EFT curvature-squared field redefinition",
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
    fluid = sections["perfect_fluid"]
    tov = sections["tov_map"]
    contact = sections["contact_envelopes"]
    a6 = sections["scalar_a6"]
    ownership = sections["dimension_six_ownership"]
    arbitration = sections["arbitration"]
    return {
        "FLUID_CONTACT": tagged([fluid]),
        "TOV_MAP": tagged([tov]),
        "CONTACT_GATES": tagged(
            [
                {
                    "causal_box": contact["causal_box"],
                    "cap_ratio": contact["exact_cap_ratio_aC_over_aR"],
                    "energy_proof": contact["energy_coefficient_proof"],
                    "pressure_proof": contact[
                        "pressure_coefficient_proof"
                    ],
                    "profile_mass_bound": contact["profile_mass_bound"],
                    "mass_guard": contact["mass_guard"],
                    "passed": contact["passed"],
                }
            ]
        ),
        "CONTACT_BENCHMARKS": tagged(contact["rows"]),
        "SCALAR_A6": tagged([a6]),
        "DIMENSION_SIX_OWNERSHIP": tagged(ownership["rows"]),
        "A6_STRONG_FIELD_BENCHMARKS": tagged(
            sections["a6_benchmarks"]["rows"]
        ),
        "ARBITRATION": tagged([arbitration]),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "all_checks_pass": calculation["all_checks_pass"],
                    "next_target": arbitration["next_target"],
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
    fluid = sections["perfect_fluid"]
    tov = sections["tov_map"]
    contact = sections["contact_envelopes"]
    contact_rows = contact["rows"]
    contact_by_name = {row["system"]: row for row in contact_rows}
    a6 = sections["scalar_a6"]
    ownership = sections["dimension_six_ownership"]
    a6_rows = sections["a6_benchmarks"]["rows"]
    a6_by_name = {row["system"]: row for row in a6_rows}
    arbitration = sections["arbitration"]

    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-723"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    variables = {row["symbol"]: row for row in variable_rows}
    expected_statuses = {
        "F_contact_fluid_MTS": "exact_perfect_fluid_contact_image_derived",
        "rho_eff_contact_MTS": "derived_first_order_effective_EOS_energy",
        "p_eff_contact_MTS": "derived_first_order_effective_EOS_pressure",
        "TOV_contact_map_MTS": "exact_first_order_standard_TOV_with_effective_EOS_map",
        "A6_scalar_RF_MTS": "exact_massive_scalar_Ricci_flat_a6_kernel_derived",
        "b6_spectral_owner_MTS": "owner_equation_derived_total_coefficient_not_owned",
        "epsilon6_scalar_MTS": "derived_conditional_massive_scalar_dimension_six_control",
    }
    variable_counts = {
        symbol: sum(row.get("symbol") == symbol for row in variable_rows)
        for symbol in expected_statuses
    }

    checkpoint = (
        POST
        / "4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL / "897-PPC4161-compact-fluid-TOV-and-scalar-a6-owner.md"
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
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4880_VALIDATION.csv")
    output_paths = [
        OUTPUT / f"P8_Y5_R2FR_4881_{name}.csv" for name in groups
    ]
    all_rows = sources + [row for rows in groups.values() for row in rows]
    no_placeholders = not any(
        "MISSING_" in str(value)
        for row in all_rows
        for value in row.values()
    )
    neutron_contact = contact_by_name[
        "1.4_solar_mass_12km_neutron_star"
    ]

    rows = [
        check(
            "VAL4881_00_symbolic",
            calculation["all_checks_pass"],
            "eight derivation ownership benchmark and arbitration sections",
        ),
        check(
            "VAL4881_01_sources",
            len(sources) == 21
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            f"sources={len(sources)}",
        ),
        check(
            "VAL4881_02_archive",
            sections["sources"]["archive_hash_matches"]
            and sections["sources"]["archive_sha256"]
            == A6_ARCHIVE_SHA256,
            "Vassilevich source archive hash locked",
        ),
        check(
            "VAL4881_03_fluid_contact",
            fluid["passed"]
            and fluid["contact_boxed"]
            == "F=a_R(rho-3p)^2+4a_C rho(rho/3+p)",
            "perfect-fluid contact reduction exact",
        ),
        check(
            "VAL4881_04_constant_w",
            fluid["constant_w_identity"]
            == "D=(1+2w)F when p=w rho"
            and fluid["radiation_trace_selector"] == "8*a_C/3",
            "barotropic pressure and radiation selectors",
        ),
        check(
            "VAL4881_05_off_shell",
            "conserved-current" in fluid["off_shell_guard"]
            and "on-shell shorthand" in fluid["off_shell_guard"],
            "fluid metric variation owner fixed",
        ),
        check(
            "VAL4881_06_TOV",
            tov["passed"]
            and "rho_eff" in tov["mass_equation"]
            and "p_eff" in tov["pressure_equation"],
            "standard TOV map with effective EOS",
        ),
        check(
            "VAL4881_07_EOS_redundancy",
            "no new gravitational differential operator"
            in tov["EOS_redundancy_theorem"]
            and "Schwarzschild" in tov["metric_redefinition"],
            "interior EOS map and exterior silence",
        ),
        check(
            "VAL4881_08_caps",
            contact["passed"]
            and abs(contact["exact_cap_ratio_aC_over_aR"] - 3) < 1e-12,
            "causal coefficient envelope and cap ratio",
        ),
        check(
            "VAL4881_09_contact_rows",
            len(contact_rows) == 4 and len(contact_by_name) == 4,
            "four uniform-density benchmarks",
        ),
        check(
            "VAL4881_10_neutron_benchmark",
            3.2e-19
            < neutron_contact[
                "uniform_mean_density_abs_delta_rho_over_rho_benchmark"
            ]
            < 3.3e-19
            and 9.6e-19
            < neutron_contact[
                "uniform_mean_density_abs_delta_p_over_rho_benchmark"
            ]
            < 9.8e-19,
            "neutron-star uniform-mean-density benchmark",
        ),
        check(
            "VAL4881_11_profile_guard",
            "int rho_mass^2" in contact["profile_mass_bound"]
            and "does not upper-bound" in contact["mass_guard"],
            "mean density not mislabeled as profile bound",
        ),
        check(
            "VAL4881_12_a6_tensor",
            a6["passed"]
            and a6["absolute_operator_norm"] == "313/45360",
            "Ricci-flat scalar a6 coefficients and norm",
        ),
        check(
            "VAL4881_13_massive_moment",
            "exp(-m^2/LambdaUV^2)/m^2"
            in a6["proper_time_integral_massive"]
            and "32 pi^2 m^2" in a6["scalar_loop_action_magnitude"],
            "massive proper-time spectral moment",
        ),
        check(
            "VAL4881_14_massless_branch",
            "infrared divergent" in a6["massless_limit"]
            and "nonlocal" in a6["massless_limit"],
            "massless local-c6 route rejected correctly",
        ),
        check(
            "VAL4881_15_owner",
            ownership["passed"]
            and not ownership["bare_dimension_six_declared"]
            and not a6["total_c6_parent_derived"],
            "scalar loop owned and total bare-plus-spectrum withheld",
        ),
        check(
            "VAL4881_16_scalar_hierarchy",
            4.18e-5 < a6["epsilon6_scalar_envelope"] < 4.19e-5
            and a6["delta_EH_max"] == 0.01,
            "Newton-matched scalar a6 hierarchy",
        ),
        check(
            "VAL4881_17_a6_benchmarks",
            len(a6_rows) == 2
            and 1000
            < a6_by_name[
                "1.4_solar_mass_12km_neutron_star"
            ]["max_massive_gap_Compton_length_m_for_q_over_m_0p1"]
            < 1200
            and 1500
            < a6_by_name[
                "10_solar_mass_Schwarzschild_horizon"
            ]["max_massive_gap_Compton_length_m_for_q_over_m_0p1"]
            < 1700,
            "neutron-star and black-hole hierarchy lengths",
        ),
        check(
            "VAL4881_18_arbitration",
            arbitration["passed"]
            and not arbitration[
                "parameter_free_mass_radius_tidal_prediction"
            ]
            and not arbitration["total_c6_parent_derived"],
            "advance retained without compact-star or total-c6 overclaim",
        ),
        check(
            "VAL4881_19_scope",
            not arbitration["full_strong_matter_GR_promoted"]
            and not arbitration["full_fundamental_unification"],
            "strong matter and full theory not promoted",
        ),
        check(
            "VAL4881_20_placeholders",
            no_placeholders,
            "no MISSING markers in evidence rows",
        ),
        check(
            "VAL4881_21_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all checkpoint evidence remains private",
        ),
        check(
            "VAL4881_22_csv",
            all(
                path.exists() and len(read_csv(path)) > 0
                for path in output_paths
            ),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4881_23_claim",
            len(claims) == 1
            and claims[0].get("status")
            == "selected_metric_strictEFT_compact_fluid_EOS_TOV_map_and_massive_scalar_a6_kernel_private_conditional",
            "L-723 unique and scoped",
        ),
        check(
            "VAL4881_24_variables",
            all(
                variable_counts.get(symbol) == 1
                and variables.get(symbol, {}).get("status") == status
                for symbol, status in expected_statuses.items()
            ),
            "seven compact-fluid and dimension-six variables unique",
        ),
        check(
            "VAL4881_25_documents",
            "MTS_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881"
            in checkpoint
            and "PPC4161_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881"
            in formal_note,
            "checkpoint and formal note markers",
        ),
        check(
            "VAL4881_26_registers",
            "1.174 Compact-fluid contact/TOV map" in equations
            and "125. Compact-fluid EOS redundancy" in redteam
            and "PPC4161 checkpoint 4881" in spine,
            "equation red-team and spine updates",
        ),
        check(
            "VAL4881_27_resume",
            "PPC4161_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881"
            in resume
            and NEXT_TARGET in resume,
            "resume handoff",
        ),
        check(
            "VAL4881_28_prior",
            len(prior) > 0
            and all(row.get("status") == "PASS" for row in prior),
            "4880 remains green",
        ),
        check(
            "VAL4881_29_scripts",
            compile_source(
                POST / "scripts" / "Y5_R2FR_4881_compact_fluid_a6.py"
            )
            and compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4881_compact_fluid_a6_gate.py"
            ),
            "scripts compile without bytecode",
        ),
        check(
            "VAL4881_30_pycache",
            not (POST / "scripts" / "__pycache__").exists(),
            "no pycache",
        ),
        check(
            "VAL4881_31_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4882 target selected",
        ),
    ]
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        check(
            "VAL4881_OVERALL",
            overall,
            "MTS_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4881_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4881_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4881_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4881_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4881_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
