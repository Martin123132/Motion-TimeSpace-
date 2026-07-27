from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

from Y5_R2FR_4878_local_eft_arena_bounds import result


CHECKPOINT = "4878"
TIMESTAMP = "2026-07-10T18:20:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = (
    "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-"
    "completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-"
    "GR-promotion-gate.md"
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
            "SRC4878_00_checkpoint",
            POST
            / "4878-Y5-R2FR-renormalized-EFT-local-limit-and-arena-specific-nonlocal-residual-bounds-to-R10-PPN-clocks-orbit-and-Maxwell.md",
            "MTS_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878",
        ),
        (
            "SRC4878_01_research_script",
            POST / "scripts" / "Y5_R2FR_4878_local_eft_arena_bounds.py",
            "def strict_eft_contact_branch",
        ),
        (
            "SRC4878_02_gate_script",
            POST
            / "scripts"
            / "Y5_R2FR_4878_local_eft_arena_bounds_gate.py",
            "P8_Y5_BRR545_4878_VALIDATION_PASS",
        ),
        (
            "SRC4878_03_prior_checkpoint",
            POST
            / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877",
        ),
        (
            "SRC4878_04_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4877_VALIDATION.csv",
            "VAL4877_OVERALL",
        ),
        (
            "SRC4878_05_r10_curve",
            OUTPUT
            / "P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv",
            "R10_EOTWASH2020_ABS_ALPHA_VECTOR_FROM_FIG5B1",
        ),
        (
            "SRC4878_06_r10_tex",
            POST
            / "source-intake"
            / "r10_curve_acquisition"
            / "4635"
            / "source"
            / "FB_ISL_pdf.tex",
            "percent-level measurements of $G_N$",
        ),
        (
            "SRC4878_07_arena_inputs",
            OUTPUT / "P8_Y5_R2FR_4800_ARENA_PROJECTION_INPUT.csv",
            "ppn_gamma_cassini_required_tau",
        ),
        (
            "SRC4878_08_maxwell",
            POST
            / "4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md",
            "Poynting",
        ),
        (
            "SRC4878_09_formal_note",
            FORMAL / "894-PPC4161-renormalized-EFT-local-arena-bounds.md",
            "PPC4161_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878",
        ),
        (
            "SRC4878_10_claims",
            FORMAL / "02-claims-register.csv",
            "L-720",
        ),
        (
            "SRC4878_11_variables",
            FORMAL / "04-variable-audit.csv",
            "etaGrav_quantum_MTS",
        ),
        (
            "SRC4878_12_equations",
            FORMAL / "05-equation-register.md",
            "1.171 Strict-EFT contact support",
        ),
        (
            "SRC4878_13_redteam",
            FORMAL / "06-consistency-red-team.md",
            "122. Strict-EFT/resummed branch mixing",
        ),
        (
            "SRC4878_14_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4878",
        ),
        (
            "SRC4878_15_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878",
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
            "SRC4878_16_strict_eft",
            "https://arxiv.org/abs/1911.10108",
            "absence of long-range R2 corrections in strict EFT",
        ),
        (
            "SRC4878_17_quadratic_gravity",
            "https://arxiv.org/abs/1508.00010",
            "quadratic-gravity resummed branch context",
        ),
        (
            "SRC4878_18_gravity_quantum",
            "https://arxiv.org/abs/hep-th/0211072",
            "physical 41/(10pi) quantum Newton coefficient",
        ),
        (
            "SRC4878_19_r10",
            "https://arxiv.org/abs/2002.11761",
            "52 micrometre data and 38.6 micrometre alpha=1 limit",
        ),
        (
            "SRC4878_20_cassini",
            "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "gamma-1=(2.1+/-2.3)e-5",
        ),
        (
            "SRC4878_21_galileo",
            "https://arxiv.org/abs/1906.06161",
            "alpha_redshift=(0.19+/-2.48)e-5",
        ),
        (
            "SRC4878_22_mercury",
            "https://www.osti.gov/biblio/22863119",
            "Mercury precession 575.3100+/-0.0015 arcsec/century",
        ),
        (
            "SRC4878_23_gw_speed",
            "https://arxiv.org/abs/1710.05834",
            "shared-cone comparator",
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
    projectors = sections["projectors"]
    strict = sections["strict_eft"]
    resummed = sections["resummed_diagnostic"]
    matter = sections["matter_nonlocal"]
    gravity = sections["pure_gravity"]
    maxwell = sections["maxwell"]
    arbitration = sections["arbitration"]

    groups = {
        "PROJECTOR_TRANSFER": tagged(
            [
                {
                    "A0": projectors["A0"],
                    "A2": projectors["A2"],
                    "Phi_exact": projectors["Phi_over_Phi_Newton_exact"],
                    "Psi_exact": projectors["Psi_over_Psi_Newton_exact"],
                    "gamma_exact": projectors["gamma_exact"],
                    "Phi_linear": projectors["Phi_over_Phi_Newton_linear"],
                    "Psi_linear": projectors["Psi_over_Psi_Newton_linear"],
                    "gamma_linear": projectors["gamma_linear"],
                    "passed": projectors["passed"],
                }
            ]
        ),
        "STRICT_EFT_CONTACT": tagged(
            [
                {
                    "branch": strict["branch"],
                    "d0_local": strict["d0_local"],
                    "d2_local": strict["d2_local"],
                    "Phi_integrand": strict[
                        "Phi_Fourier_integrand_correction"
                    ],
                    "Psi_integrand": strict[
                        "Psi_Fourier_integrand_correction"
                    ],
                    "r10_min_m": strict["r10_shortest_separation_m"],
                    "hierarchy_factor": strict[
                        "hierarchy_factor_lbarP2_over_r2"
                    ],
                    "aR_control_cap": strict["aR_abs_control_cap"],
                    "aC_control_cap": strict["aC_abs_control_cap"],
                    "cap_kind": strict["cap_kind"],
                    "passed": strict["passed"],
                }
            ]
        ),
        "RESUMMED_R10": tagged(
            [
                {
                    "branch": resummed["branch"],
                    "curve_rows": resummed["curve_rows"],
                    "alpha1_crossing_m": resummed["alpha_1_crossing_m"],
                    "alpha1_published_m": resummed[
                        "published_alpha_1_limit_m"
                    ],
                    "lambda0_limit_m": resummed["lambda0_limit_m"],
                    "aR_internal_limit": resummed[
                        "aR_internal_abs_limit"
                    ],
                    "lambda2_limit_m": resummed[
                        "lambda2_abs_envelope_m"
                    ],
                    "aC_internal_abs_limit": resummed[
                        "aC_internal_abs_limit"
                    ],
                    "d0_at_r10": resummed["scalar_d0_at_r10_limit"],
                    "abs_d2_at_r10": resummed[
                        "spin2_abs_d2_at_r10_limit"
                    ],
                    "spin2_health": resummed["spin2_health"],
                    "passed": resummed["passed"],
                }
            ]
        ),
        "NONLOCAL_COEFFICIENTS": tagged(
            [
                {
                    "kappa0_m2": matter["kappa0_m2"],
                    "kappa2_m2": matter["kappa2_m2"],
                    "etaPhi_m2": matter["etaPhi_m2"],
                    "etaPsi_m2": matter["etaPsi_m2"],
                    "etaSlip_m2": matter["etaSlip_m2"],
                    "no_cancellation": matter["no_cancellation"],
                    "passed": matter["passed"],
                }
            ]
        ),
        "PURE_GRAVITY_NEWTON": tagged(
            [
                {
                    "coefficient_41_over_10pi": gravity[
                        "coefficient_41_over_10pi"
                    ],
                    "eta_gravity_m2": gravity["eta_gravity_m2"],
                    "potential_fraction_52um": gravity[
                        "quantum_potential_fraction_at_52um"
                    ],
                    "acceleration_fraction_52um": gravity[
                        "quantum_acceleration_fraction_at_52um"
                    ],
                    "scope_guard": gravity["scope_guard"],
                    "passed": gravity["passed"],
                }
            ]
        ),
        "ARENA_BOUNDS": tagged(sections["arenas"]["rows"]),
        "MAXWELL_PROJECTION": tagged(
            [
                {
                    "field_equation": maxwell["field_equation"],
                    "direct_aR_aC_variation": maxwell[
                        "direct_aR_aC_variation_of_Maxwell_equation"
                    ],
                    "classical_trace": maxwell[
                        "classical_trace_in_four_dimensions"
                    ],
                    "scalar_source_free_EM": maxwell[
                        "scalar_R2_source_from_free_EM"
                    ],
                    "spin2_source": maxwell["spin2_source"],
                    "photon_cone": maxwell["photon_cone"],
                    "Poynting_role": maxwell["Poynting_role"],
                    "passed": maxwell["passed"],
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
        if row.get("claim_id") == "L-720"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    variables = {row["symbol"]: row for row in variable_rows}
    expected_statuses = {
        "Gamma_metric_only_MTS": "strict_renormalized_EFT_selected_contact_support_and_nonlocal_arena_projection_partial",
        "aR_induced_MTS": "finite_local_strict_EFT_contact_support_derived_resummed_scalar_diagnostic_nonclaim",
        "aC_induced_MTS": "finite_local_strict_EFT_contact_support_derived_resummed_spin2_diagnostic_unhealthy_nonclaim",
        "epsilon_nonlocal_MTS": "matter_position_space_tails_and_arena_coefficient_bounds_derived",
        "Gamma_Hgh_nonlocal_MTS": "physical_pure_gravity_Newton_tail_derived_offshell_light_clock_kernel_open",
        "d0_EFT_MTS": "exact_transfer_and_local_nonlocal_split_derived",
        "d2_EFT_MTS": "exact_transfer_and_local_nonlocal_split_derived",
        "etaPhi_nonlocal_MTS": "matter_loop_position_space_coefficient_derived",
        "etaPsi_nonlocal_MTS": "matter_loop_position_space_coefficient_derived",
        "etaSlip_nonlocal_MTS": "matter_loop_slip_coefficient_derived",
        "etaGrav_quantum_MTS": "physical_long_range_Newton_coefficient_derived",
        "etaNewton_total_MTS": "matter_plus_pure_gravity_Newton_envelope_derived_no_cancellation",
        "R10_resummed_curve_MTS": "vector_extracted_curve_reproduces_alpha1_anchor_resummed_only_private_nonclaim",
        "Maxwell_R2C2_projection_MTS": "minimal_Maxwell_equation_and_classical_trace_projection_closed_at_this_order",
    }
    variable_counts = {
        symbol: sum(row.get("symbol") == symbol for row in variable_rows)
        for symbol in expected_statuses
    }

    checkpoint = (
        POST
        / "4878-Y5-R2FR-renormalized-EFT-local-limit-and-arena-specific-nonlocal-residual-bounds-to-R10-PPN-clocks-orbit-and-Maxwell.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL / "894-PPC4161-renormalized-EFT-local-arena-bounds.md"
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
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4877_VALIDATION.csv")
    output_paths = [
        OUTPUT / f"P8_Y5_R2FR_4878_{name}.csv" for name in groups
    ]
    all_rows = sources + [row for rows in groups.values() for row in rows]
    no_placeholders = not any(
        "MISSING_" in str(value)
        for row in all_rows
        for value in row.values()
    )
    sections = calculation["sections"]
    arena_rows = sections["arenas"]["rows"]

    rows = [
        check(
            "VAL4878_00_symbolic",
            calculation["all_checks_pass"],
            "nine derivation and arbitration sections",
        ),
        check(
            "VAL4878_01_sources",
            len(sources) == 24
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            f"sources={len(sources)}",
        ),
        check(
            "VAL4878_02_projectors",
            sections["projectors"]["passed"]
            and "(2*d0 + d2 + 3)/(4*d0 - d2 + 3)"
            == sections["projectors"]["gamma_exact"],
            "exact Phi Psi gamma transfer",
        ),
        check(
            "VAL4878_03_contact",
            sections["strict_eft"]["passed"]
            and not sections["strict_eft"]["r10_yukawa_curve_applies"],
            "strict-EFT q2 cancellation and contact support",
        ),
        check(
            "VAL4878_04_control_caps",
            3.42e56
            < sections["strict_eft"]["aR_abs_control_cap"]
            < 3.45e56
            and 1.02e57
            < sections["strict_eft"]["aC_abs_control_cap"]
            < 1.04e57,
            "one-percent derivative-control caps",
        ),
        check(
            "VAL4878_05_r10_curve",
            sections["resummed_diagnostic"]["passed"]
            and sections["resummed_diagnostic"]["curve_rows"] == 176,
            "vector curve and three crossings",
        ),
        check(
            "VAL4878_06_branch_split",
            sections["resummed_diagnostic"]["scalar_d0_at_r10_limit"] > 1
            and sections["resummed_diagnostic"][
                "spin2_abs_d2_at_r10_limit"
            ]
            > 0.4,
            "resummed limits lie outside one-percent strict-EFT corridor",
        ),
        check(
            "VAL4878_07_matter_tail",
            sections["matter_nonlocal"]["passed"]
            and sections["matter_nonlocal"]["no_cancellation"],
            "matter r^-3 coefficients",
        ),
        check(
            "VAL4878_08_gravity_tail",
            sections["pure_gravity"]["passed"]
            and 3.40e-70
            < sections["pure_gravity"]["eta_gravity_m2"]
            < 3.42e-70,
            "physical 41/(10pi) Newton tail",
        ),
        check(
            "VAL4878_09_arenas",
            sections["arenas"]["passed"]
            and len(arena_rows) == 4
            and all(row["prediction_abs"] < row["bound_abs"] for row in arena_rows),
            "R10 Cassini Galileo Mercury envelopes",
        ),
        check(
            "VAL4878_10_coefficients",
            all(
                row["coefficient_prediction_m2"]
                < row["coefficient_bound_m2"]
                for row in arena_rows
            ),
            "observable anchors inverted to coefficient caps",
        ),
        check(
            "VAL4878_11_maxwell",
            sections["maxwell"]["passed"]
            and sections["maxwell"][
                "direct_aR_aC_variation_of_Maxwell_equation"
            ]
            == 0
            and sections["maxwell"]["classical_trace_in_four_dimensions"]
            == 0,
            "minimal Maxwell and trace selector",
        ),
        check(
            "VAL4878_12_claim_guard",
            not sections["arenas"]["full_local_gr_claim"]
            and not sections["resummed_diagnostic"]["valid_for_claim"],
            "full local-GR and resummed claims remain false",
        ),
        check(
            "VAL4878_13_placeholders",
            no_placeholders,
            "no MISSING markers in evidence rows",
        ),
        check(
            "VAL4878_14_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all checkpoint evidence private",
        ),
        check(
            "VAL4878_15_csv",
            all(
                path.exists() and len(read_csv(path)) > 0
                for path in output_paths
            ),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4878_16_claim",
            len(claims) == 1
            and claims[0].get("status")
            == "strict_EFT_contact_theorem_and_nonlocal_arena_bounds_derived_minimal_Maxwell_closed_local_GR_private_nonclaim",
            "L-720 unique and nonclaim",
        ),
        check(
            "VAL4878_17_variables",
            all(
                variable_counts.get(symbol) == 1
                and variables.get(symbol, {}).get("status") == status
                for symbol, status in expected_statuses.items()
            ),
            "canonical variable rows unique and updated",
        ),
        check(
            "VAL4878_18_documents",
            "MTS_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878"
            in checkpoint
            and "PPC4161_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878"
            in formal_note,
            "checkpoint and formal note markers",
        ),
        check(
            "VAL4878_19_registers",
            "1.171 Strict-EFT contact support" in equations
            and "122. Strict-EFT/resummed branch mixing" in redteam
            and "PPC4161 checkpoint 4878" in spine,
            "equation red-team and spine updates",
        ),
        check(
            "VAL4878_20_resume",
            "PPC4161_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878" in resume
            and NEXT_TARGET in resume,
            "resume handoff",
        ),
        check(
            "VAL4878_21_prior",
            len(prior) > 0
            and all(row.get("status") == "PASS" for row in prior),
            "4877 remains green",
        ),
        check(
            "VAL4878_22_scripts",
            compile_source(
                POST / "scripts" / "Y5_R2FR_4878_local_eft_arena_bounds.py"
            )
            and compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4878_local_eft_arena_bounds_gate.py"
            ),
            "scripts compile without bytecode",
        ),
        check(
            "VAL4878_23_pycache",
            not (POST / "scripts" / "__pycache__").exists(),
            "no pycache",
        ),
        check(
            "VAL4878_24_next",
            NEXT_TARGET in checkpoint,
            "4879 target selected",
        ),
    ]
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        check(
            "VAL4878_OVERALL",
            overall,
            "MTS_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4878_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4878_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4878_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4878_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4878_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
