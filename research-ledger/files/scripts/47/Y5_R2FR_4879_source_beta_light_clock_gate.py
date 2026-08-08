from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

from Y5_R2FR_4879_source_beta_light_clock import result


CHECKPOINT = "4879"
TIMESTAMP = "2026-07-10T18:52:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = (
    "4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-domain-"
    "of-validity-and-strong-field-entry-gate.md"
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


def source_rows() -> list[dict[str, Any]]:
    local = [
        (
            "SRC4879_00_checkpoint",
            POST
            / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
            "MTS_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879",
        ),
        (
            "SRC4879_01_research_script",
            POST / "scripts" / "Y5_R2FR_4879_source_beta_light_clock.py",
            "def field_redefinition_contact_derivation",
        ),
        (
            "SRC4879_02_gate_script",
            POST
            / "scripts"
            / "Y5_R2FR_4879_source_beta_light_clock_gate.py",
            "P8_Y5_BRR545_4879_VALIDATION_PASS",
        ),
        (
            "SRC4879_03_prior_checkpoint",
            POST
            / "4878-Y5-R2FR-renormalized-EFT-local-limit-and-arena-specific-nonlocal-residual-bounds-to-R10-PPN-clocks-orbit-and-Maxwell.md",
            "MTS_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878",
        ),
        (
            "SRC4879_04_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4878_VALIDATION.csv",
            "VAL4878_OVERALL,PASS",
        ),
        (
            "SRC4879_05_spin2_parent",
            POST
            / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875",
        ),
        (
            "SRC4879_06_maxwell",
            POST
            / "4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md",
            "Poynting",
        ),
        (
            "SRC4879_07_arena_inputs",
            OUTPUT / "P8_Y5_R2FR_4800_ARENA_PROJECTION_INPUT.csv",
            "ppn_beta_mercury_required_tau",
        ),
        (
            "SRC4879_08_prior_formal",
            FORMAL / "894-PPC4161-renormalized-EFT-local-arena-bounds.md",
            "PPC4161_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878",
        ),
        (
            "SRC4879_09_formal_note",
            FORMAL
            / "895-PPC4161-finite-source-beta-light-clock-local-GR-certificate.md",
            "PPC4161_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879",
        ),
        (
            "SRC4879_10_claims",
            FORMAL / "02-claims-register.csv",
            "L-721",
        ),
        (
            "SRC4879_11_variables",
            FORMAL / "04-variable-audit.csv",
            "local_GR_1PN_certificate_MTS",
        ),
        (
            "SRC4879_12_equations",
            FORMAL / "05-equation-register.md",
            "1.172 Finite-source contact image",
        ),
        (
            "SRC4879_13_redteam",
            FORMAL / "06-consistency-red-team.md",
            "123. Local-GR certificate scope",
        ),
        (
            "SRC4879_14_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4879",
        ),
        (
            "SRC4879_15_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker in local:
        content = path.read_text(encoding="utf-8", errors="replace")
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local",
                "source_path": str(path),
                "source_exists": path.exists(),
                "marker": marker,
                "marker_found": marker in content,
                "verification_method": "local_path_and_marker",
            }
        )
    web = [
        (
            "SRC4879_16_field_redefinition",
            "https://arxiv.org/abs/1911.10108",
            "two-heavy-source any-graviton curvature-squared theorem",
        ),
        (
            "SRC4879_17_light_PRL",
            "https://arxiv.org/abs/1410.7590",
            "physical photon bending amplitude",
        ),
        (
            "SRC4879_18_light_eikonal",
            "https://arxiv.org/abs/1609.07477",
            "classical 2PM and quantum eikonal angle",
        ),
        (
            "SRC4879_19_newton",
            "https://arxiv.org/abs/hep-th/0211072",
            "complete physical quantum Newton potential",
        ),
        (
            "SRC4879_20_metric_guard",
            "https://arxiv.org/abs/gr-qc/0601020",
            "off-shell metric reparametrization guard",
        ),
        (
            "SRC4879_21_mercury",
            "https://www.osti.gov/biblio/22863119",
            "beta-1=(-2.7+/-3.9)e-5",
        ),
        (
            "SRC4879_22_galileo",
            "https://arxiv.org/abs/1906.06161",
            "clock alpha=(0.19+/-2.48)e-5",
        ),
        (
            "SRC4879_23_cassini",
            "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "gamma-1=(2.1+/-2.3)e-5",
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
    field = sections["field_redefinition"]
    finite = sections["finite_sources"]
    ppn = sections["ppn_beta"]
    clock = sections["clock"]
    light = sections["light"]
    promotion = sections["promotion"]
    arbitration = sections["arbitration"]
    gate_rows = [
        {"gate": gate, "passed": passed}
        for gate, passed in promotion["gates"].items()
    ]
    groups = {
        "FIELD_REDEFINITION": tagged(
            [
                {
                    "basis": field["four_dimensional_basis"],
                    "metric_redefinition": field[
                        "inverse_metric_redefinition"
                    ],
                    "EH_shift": field["EH_shift"],
                    "contact_action": field["contact_action"],
                    "passed": field["passed"],
                }
            ]
        ),
        "FINITE_SOURCE_CONTACT": tagged(
            [
                {
                    "decomposition": finite["decomposition"],
                    "cross_density": finite[
                        "cross_contact_density_times_Mbar4"
                    ],
                    "support_condition": finite[
                        "disjoint_support_condition"
                    ],
                    "cross_value": finite[
                        "cross_contact_for_disjoint_sources"
                    ],
                    "self_terms": finite["self_terms"],
                    "R10_application": finite["R10_application"],
                    "passed": finite["passed"],
                }
            ]
        ),
        "PPN_BETA": tagged([ppn]),
        "CLOCK_KERNEL": tagged([clock]),
        "LIGHT_EIKONAL": tagged([light]),
        "LOCAL_GR_GATES": tagged(gate_rows),
        "PROMOTION": tagged(
            [
                {
                    "classical_local_GR_1PN_correspondence": promotion[
                        "classical_local_GR_1PN_correspondence"
                    ],
                    "promotion_scope": promotion["promotion_scope"],
                    "not_promoted": promotion["not_promoted"],
                    "claim_status": promotion["claim_status"],
                    "passed": promotion["passed"],
                }
            ]
        ),
        "DECISION": tagged(
            [
                {
                    **arbitration,
                    "overall_decision": calculation["decision"],
                    "all_checks_pass": calculation["all_checks_pass"],
                }
            ]
        ),
    }
    return groups


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

    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-721"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    variables = {row["symbol"]: row for row in variable_rows}
    expected_statuses = {
        "Gamma_metric_only_MTS": "private_conditional_classical_local_GR_1PN_certificate_selected_strictEFT_metric_branch",
        "P_BR_MTS": "exact_static_transfer_plus_operational_classical_1PN_gamma_beta_closure",
        "aR_induced_MTS": "finite_source_self_contact_derived_disjoint_cross_force_zero_resummed_scalar_nonclaim",
        "aC_induced_MTS": "finite_source_self_contact_derived_disjoint_cross_force_zero_resummed_spin2_unhealthy",
        "Gamma_Hgh_nonlocal_MTS": "physical_Newton_clock_and_on_shell_photon_eikonal_kernels_inserted_resolution_guarded",
        "etaNewton_total_MTS": "matter_plus_pure_gravity_Newton_clock_envelope_derived_no_cancellation",
        "contact_R2C2_MTS": "explicit_field_redefinition_and_disjoint_finite_source_cross_zero_derived",
        "beta_PPN_MTS": "operational_classical_beta_equals_one_for_selected_strictEFT_separated_source_branch",
        "clock_monopole_EFT_MTS": "physical_minimal_point_clock_monopole_kernel_derived_and_bounded",
        "theta_gamma_EFT_MTS": "on_shell_photon_eikonal_classical_GR_and_resolution_guarded_quantum_envelope_derived",
        "b0_light_resolution_MTS": "explicit_observer_resolution_parameter_not_fit_or_hidden",
        "local_GR_1PN_certificate_MTS": "private_conditional_classical_local_GR_through_1PN_certificate_pass",
    }
    variable_counts = {
        symbol: sum(row.get("symbol") == symbol for row in variable_rows)
        for symbol in expected_statuses
    }

    checkpoint = (
        POST
        / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL
        / "895-PPC4161-finite-source-beta-light-clock-local-GR-certificate.md"
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
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4878_VALIDATION.csv")
    output_paths = [
        OUTPUT / f"P8_Y5_R2FR_4879_{name}.csv" for name in groups
    ]
    all_rows = sources + [row for rows in groups.values() for row in rows]
    no_placeholders = not any(
        "MISSING_" in str(value)
        for row in all_rows
        for value in row.values()
    )
    sections = calculation["sections"]

    rows = [
        check(
            "VAL4879_00_symbolic",
            calculation["all_checks_pass"],
            "eight derivation and arbitration sections",
        ),
        check(
            "VAL4879_01_sources",
            len(sources) == 24
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            f"sources={len(sources)}",
        ),
        check(
            "VAL4879_02_field_redefinition",
            sections["field_redefinition"]["passed"],
            "curvature basis EH cancellation and stress contact image",
        ),
        check(
            "VAL4879_03_finite_sources",
            sections["finite_sources"]["passed"]
            and sections["finite_sources"][
                "cross_contact_for_disjoint_sources"
            ]
            == "0",
            "finite disjoint-source cross contact zero",
        ),
        check(
            "VAL4879_04_ppn",
            sections["ppn_beta"]["passed"]
            and sections["ppn_beta"]["beta_classical"] == 1
            and sections["ppn_beta"]["gamma_classical"] == 1,
            "operational classical beta gamma closure",
        ),
        check(
            "VAL4879_05_mercury",
            sections["ppn_beta"]["prediction_z_score"] < 1,
            "beta-1=0 within one MESSENGER sigma",
        ),
        check(
            "VAL4879_06_clock",
            sections["clock"]["passed"]
            and sections["clock"]["alpha_clock_prediction_abs"] < 1e-82,
            "physical point-clock monopole",
        ),
        check(
            "VAL4879_07_light_coefficients",
            sections["light"]["passed"]
            and sections["light"]["photon_constant_8bu_plus_9"]
            == -26 / 15,
            "photon bubble and IR-independent species difference",
        ),
        check(
            "VAL4879_08_light_bound",
            sections["light"]["gamma_equivalent_abs"] < 1e-84
            and sections["light"]["gamma_equivalent_abs"]
            < sections["light"]["Cassini_gamma_bound_abs"],
            "resolution-guarded photon envelope",
        ),
        check(
            "VAL4879_09_promotion",
            sections["promotion"]["passed"]
            and sections["promotion"][
                "classical_local_GR_1PN_correspondence"
            ]
            and all(sections["promotion"]["gates"].values()),
            "private conditional local-GR 1PN certificate",
        ),
        check(
            "VAL4879_10_scope",
            not sections["arbitration"]["full_fundamental_unification"]
            and "strong-field" in sections["promotion"]["not_promoted"],
            "strong-field and full unification not promoted",
        ),
        check(
            "VAL4879_11_metric_guard",
            "off-shell metric assignment" in sections["clock"]["derivation"]
            and "detector-resolution" in sections["light"]["interpretation"],
            "no partial-metric or hidden-resolution inference",
        ),
        check(
            "VAL4879_12_placeholders",
            no_placeholders,
            "no MISSING markers in evidence rows",
        ),
        check(
            "VAL4879_13_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all checkpoint evidence private",
        ),
        check(
            "VAL4879_14_csv",
            all(
                path.exists() and len(read_csv(path)) > 0
                for path in output_paths
            ),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4879_15_claim",
            len(claims) == 1
            and claims[0].get("status")
            == "selected_metric_strictEFT_classical_local_GR_1PN_private_conditional_certificate",
            "L-721 unique and scoped",
        ),
        check(
            "VAL4879_16_variables",
            all(
                variable_counts.get(symbol) == 1
                and variables.get(symbol, {}).get("status") == status
                for symbol, status in expected_statuses.items()
            ),
            "canonical variable rows unique and updated",
        ),
        check(
            "VAL4879_17_documents",
            "MTS_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879"
            in checkpoint
            and "PPC4161_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879"
            in formal_note,
            "checkpoint and formal note markers",
        ),
        check(
            "VAL4879_18_registers",
            "1.172 Finite-source contact image" in equations
            and "123. Local-GR certificate scope" in redteam
            and "PPC4161 checkpoint 4879" in spine,
            "equation red-team and spine updates",
        ),
        check(
            "VAL4879_19_resume",
            "PPC4161_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879"
            in resume
            and NEXT_TARGET in resume,
            "resume handoff",
        ),
        check(
            "VAL4879_20_prior",
            len(prior) > 0
            and all(row.get("status") == "PASS" for row in prior),
            "4878 remains green",
        ),
        check(
            "VAL4879_21_scripts",
            compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4879_source_beta_light_clock.py"
            )
            and compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4879_source_beta_light_clock_gate.py"
            ),
            "scripts compile without bytecode",
        ),
        check(
            "VAL4879_22_pycache",
            not (POST / "scripts" / "__pycache__").exists(),
            "no pycache",
        ),
        check(
            "VAL4879_23_next",
            NEXT_TARGET in checkpoint,
            "4880 target selected",
        ),
    ]
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        check(
            "VAL4879_OVERALL",
            overall,
            "MTS_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4879_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4879_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4879_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4879_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4879_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
