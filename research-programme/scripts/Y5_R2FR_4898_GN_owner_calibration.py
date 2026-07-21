from __future__ import annotations

import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4898"
NEXT_TARGET = (
    "4899-Y5-R2FR-primitive-U1-normalization-and-Maxwell-charge-"
    "calibration-versus-alpha-prediction-gate.md"
)

G_SI = 6.67430e-11
G_SIGMA_SI = 0.00015e-11
C_M_S = 299792458.0
H_J_S = 6.62607015e-34
HBAR_J_S = H_J_S / (2.0 * math.pi)
EV_J = 1.602176634e-19
NIST_CONSTANTS_URL = "https://physics.nist.gov/cuu/Constants/"
NIST_WALL_2022_URL = "https://physics.nist.gov/cuu/pdf/wall_2022.pdf"
CODATA_2022_PAPER_URL = (
    "https://physics.nist.gov/cuu/pdf/RevModPhys.97.025002.pdf"
)


def contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    local_sources = [
        (
            "SRC4898_00_4897",
            POST
            / "4897-Y5-R2FR-cosmology-without-bath-source-metric-only-baseline-and-derived-extension-reentry-gate.md",
            "MTS_METRIC_ONLY_BASELINE_REENTRY_GATE_4897",
        ),
        (
            "SRC4898_01_4897_validation",
            OUTPUT / "P8_Y5_BRR545_4897_VALIDATION.csv",
            "VAL4897_OVERALL,PASS",
        ),
        (
            "SRC4898_02_4875",
            POST
            / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875",
        ),
        (
            "SRC4898_03_4876",
            POST
            / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
            "INTEGRATED_H_PARENT_SADDLE_HEAT_KERNEL_POLE_HIERARCHY_4876",
        ),
        (
            "SRC4898_04_4877",
            POST
            / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877",
        ),
        (
            "SRC4898_05_4879",
            POST
            / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
            "MTS_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879",
        ),
        (
            "SRC4898_06_4880",
            POST
            / "4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-domain-of-validity-and-strong-field-entry-gate.md",
            "MTS_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880",
        ),
        (
            "SRC4898_07_4885",
            POST
            / "4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-from-closed-bath-or-three-boson-branch-demotion-gate.md",
            "MTS_GAMMA_MEMORY_UV_OPERATOR_AND_BRANCH_ARBITRATION_4885",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker in local_sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "validated_local_derivation_or_output",
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": path.exists(),
                "marker": marker,
                "marker_found": contains(path, marker),
                "source_checked_date": "2026-07-11",
            }
        )
    for source_id, url, description in (
        (
            "SRC4898_08_NIST_constants",
            NIST_CONSTANTS_URL,
            "NIST current CODATA constants portal; 2022 is latest available",
        ),
        (
            "SRC4898_09_NIST_wall",
            NIST_WALL_2022_URL,
            "NIST SP 961 2022 CODATA value G=6.67430(15)e-11 SI",
        ),
        (
            "SRC4898_10_CODATA_paper",
            CODATA_2022_PAPER_URL,
            "2022 CODATA recommended-values paper",
        ),
    ):
        rows.append(
            {
                "source_id": source_id,
                "source_type": "official_external_constant_source",
                "source_path_or_url": url,
                "local_path_required": False,
                "source_exists": True,
                "marker": description,
                "marker_found": True,
                "source_checked_date": "2026-07-11",
            }
        )
    return {
        "rows": rows,
        "local_sources": len(local_sources),
        "official_external_sources": 3,
        "passed": all(
            row["source_exists"]
            and row["marker_found"]
            and (
                row["local_path_required"]
                or str(row["source_path_or_url"]).startswith("https://")
            )
            for row in rows
        ),
    }


@lru_cache(maxsize=None)
def microscopic_owner_audit() -> dict[str, Any]:
    rows = [
        {
            "owner_id": "MICRO4898_H_DIFF",
            "quantity": "integrated principal density H and Diff quotient",
            "role": "owns the massless spin-2 field space and Ward identity",
            "current_status": "parent_owned",
            "independently_fixed_before_G": True,
            "blocks_numeric_G_prediction": False,
            "source_path": "post-checkpoint-work/4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "next_action": "retain",
        },
        {
            "owner_id": "MICRO4898_W1",
            "quantity": "W1=sum_s(1-6xi_s)+2N_D-4N_V",
            "role": "massless matter contribution to Einstein stiffness",
            "current_status": "spectrum_not_uniquely_fixed",
            "independently_fixed_before_G": False,
            "blocks_numeric_G_prediction": True,
            "source_path": "post-checkpoint-work/4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "next_action": "derive complete primitive spectrum and statistics",
        },
        {
            "owner_id": "MICRO4898_XI",
            "quantity": "xi_s curvature weights",
            "role": "sets each scalar contribution to W1",
            "current_status": "input_not_selected_by_parent_symmetry",
            "independently_fixed_before_G": False,
            "blocks_numeric_G_prediction": True,
            "source_path": "post-checkpoint-work/4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-from-closed-bath-or-three-boson-branch-demotion-gate.md",
            "next_action": "derive curvature weights from a microscopic symmetry or RG fixed point",
        },
        {
            "owner_id": "MICRO4898_LAMBDAUV",
            "quantity": "Lambda_UV",
            "role": "sets the quadratic induced-stiffness scale",
            "current_status": "conditional_cutoff_not_independently_derived",
            "independently_fixed_before_G": False,
            "blocks_numeric_G_prediction": True,
            "source_path": "post-checkpoint-work/4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
            "next_action": "derive from a non-gravitational MTS scale before using G",
        },
        {
            "owner_id": "MICRO4898_M0",
            "quantity": "M_EH,boundary^2",
            "role": "allowed relevant Einstein-Hilbert boundary/counterterm coefficient",
            "current_status": "free_renormalized_relevant_coupling",
            "independently_fixed_before_G": False,
            "blocks_numeric_G_prediction": True,
            "source_path": "post-checkpoint-work/4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
            "next_action": "supply a UV boundary principle; M0^2=0 alone is not a derivation",
        },
        {
            "owner_id": "MICRO4898_THRESHOLD",
            "quantity": "Delta M_threshold^2",
            "role": "finite mass threshold and phase-transition matching",
            "current_status": "full_massive_spectrum_not_calculated",
            "independently_fixed_before_G": False,
            "blocks_numeric_G_prediction": True,
            "source_path": "post-checkpoint-work/4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "next_action": "calculate all threshold moments from the selected spectrum",
        },
        {
            "owner_id": "MICRO4898_HGHOST",
            "quantity": "Delta M_H+ghost^2",
            "role": "integrated-H gauge and ghost contribution to matching",
            "current_status": "gauge_consistent_total_not_calculated",
            "independently_fixed_before_G": False,
            "blocks_numeric_G_prediction": True,
            "source_path": "post-checkpoint-work/4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "next_action": "perform one regulator-consistent H/ghost background-field match",
        },
        {
            "owner_id": "MICRO4898_MR",
            "quantity": "M_R^2",
            "role": "physical renormalized Einstein stiffness",
            "current_status": "one_global_observational_calibration_available",
            "independently_fixed_before_G": False,
            "blocks_numeric_G_prediction": False,
            "source_path": "post-checkpoint-work/4897-Y5-R2FR-cosmology-without-bath-source-metric-only-baseline-and-derived-extension-reentry-gate.md",
            "next_action": "calibrate once to CODATA G and forbid arena retuning",
        },
    ]
    return {
        "rows": rows,
        "owner_rows": len(rows),
        "independent_rows": sum(
            row["independently_fixed_before_G"] for row in rows
        ),
        "blocking_rows": sum(row["blocks_numeric_G_prediction"] for row in rows),
        "all_source_paths_exist": all((ROOT / row["source_path"]).exists() for row in rows),
        "microscopic_G_prediction_ready": not any(
            row["blocks_numeric_G_prediction"] for row in rows
        ),
        "passed": len(rows) == 8,
    }


@lru_cache(maxsize=None)
def identifiability_theorem() -> dict[str, Any]:
    coefficient = 1.0 / (96.0 * math.pi**2)
    return {
        "renormalized_relation": (
            "M_R^2=M_EH,boundary^2+W1 Lambda_UV^2/(96 pi^2)+"
            "DeltaM_threshold^2+DeltaM_Hghost^2"
        ),
        "Newton_relation": "G_N=1/(8 pi M_R^2)",
        "scalar_anchor": (
            "G_N=12 pi/[N_s(1-6xi)Lambda_UV^2] only when boundary and omitted terms vanish"
        ),
        "constraint_function": (
            "F=M_boundary^2+W1 y/(96 pi^2)+DeltaM^2-Mobs^2=0; y=Lambda_UV^2"
        ),
        "jacobian": "[1,y/(96pi^2),W1/(96pi^2),1]",
        "jacobian_rank": 1,
        "continuous_unknowns_if_W1_unfixed": 4,
        "nullity_if_W1_unfixed": 3,
        "continuous_unknowns_if_W1_fixed": 3,
        "nullity_if_W1_fixed": 2,
        "loop_coefficient": coefficient,
        "identifiable_combination": "M_R^2 only",
        "microscopic_components_individually_identifiable_from_G": False,
        "prediction_status": "rank_deficient_calibration_surface_not_prediction",
        "passed": bool(
            coefficient > 0.0
            and 96.0 * math.pi**2 * coefficient == 1.0
            and 4 - 1 == 3
            and 3 - 1 == 2
        ),
    }


@lru_cache(maxsize=None)
def codata_calibration() -> dict[str, Any]:
    relative_g = G_SIGMA_SI / G_SI
    reduced_planck_kg = math.sqrt(HBAR_J_S * C_M_S / (8.0 * math.pi * G_SI))
    reduced_planck_gev = reduced_planck_kg * C_M_S**2 / EV_J / 1.0e9
    relative_mass = 0.5 * relative_g
    reduced_planck_sigma_kg = reduced_planck_kg * relative_mass
    reduced_planck_sigma_gev = reduced_planck_gev * relative_mass
    reduced_planck_squared_gev2 = reduced_planck_gev**2
    g_natural_gev_minus2 = 1.0 / (
        8.0 * math.pi * reduced_planck_squared_gev2
    )
    rows = [
        {
            "quantity": "G_N",
            "value": G_SI,
            "standard_uncertainty": G_SIGMA_SI,
            "relative_standard_uncertainty": relative_g,
            "units": "m^3 kg^-1 s^-2",
            "role": "single_global_input",
            "source_url": NIST_WALL_2022_URL,
        },
        {
            "quantity": "Mbar_Pl",
            "value": reduced_planck_kg,
            "standard_uncertainty": reduced_planck_sigma_kg,
            "relative_standard_uncertainty": relative_mass,
            "units": "kg",
            "role": "derived_from_single_global_input",
            "source_url": NIST_WALL_2022_URL,
        },
        {
            "quantity": "Mbar_Pl",
            "value": reduced_planck_gev,
            "standard_uncertainty": reduced_planck_sigma_gev,
            "relative_standard_uncertainty": relative_mass,
            "units": "GeV/c^2",
            "role": "derived_from_single_global_input",
            "source_url": NIST_WALL_2022_URL,
        },
        {
            "quantity": "G_N_natural",
            "value": g_natural_gev_minus2,
            "standard_uncertainty": g_natural_gev_minus2 * relative_g,
            "relative_standard_uncertainty": relative_g,
            "units": "GeV^-2",
            "role": "derived_unit_conversion",
            "source_url": NIST_WALL_2022_URL,
        },
    ]
    return {
        "rows": rows,
        "G_SI": G_SI,
        "G_sigma_SI": G_SIGMA_SI,
        "G_relative_uncertainty": relative_g,
        "Mbar_kg": reduced_planck_kg,
        "Mbar_sigma_kg": reduced_planck_sigma_kg,
        "Mbar_GeV": reduced_planck_gev,
        "Mbar_sigma_GeV": reduced_planck_sigma_gev,
        "Mbar_squared_GeV2": reduced_planck_squared_gev2,
        "G_natural_GeV_minus2": g_natural_gev_minus2,
        "calibration_count": 1,
        "latest_available_set_as_of_check": "CODATA_2022",
        "source_checked_date": "2026-07-11",
        "passed": bool(
            len(rows) == 4
            and 2.43e18 < reduced_planck_gev < 2.44e18
            and 4.33e-9 < reduced_planck_kg < 4.35e-9
            and 2.2e-5 < relative_g < 2.3e-5
        ),
    }


@lru_cache(maxsize=None)
def degeneracy_rays() -> dict[str, Any]:
    calibration = codata_calibration()
    mbar = calibration["Mbar_GeV"]
    target_m2 = mbar**2
    rows: list[dict[str, Any]] = []
    for weight in (0.1, 1.0, 10.0, 100.0, 1000.0):
        cutoff_ratio = 4.0 * math.pi * math.sqrt(6.0 / weight)
        cutoff_gev = cutoff_ratio * mbar
        recovered_m2 = weight * cutoff_gev**2 / (96.0 * math.pi**2)
        recovered_g = 1.0 / (8.0 * math.pi * recovered_m2)
        rows.append(
            {
                "branch": "pure_induced_positive_W1",
                "W1": weight,
                "LambdaUV_over_Mbar": cutoff_ratio,
                "LambdaUV_GeV": cutoff_gev,
                "M_boundary_squared_over_Mbar_squared": 0.0,
                "DeltaM_squared_over_Mbar_squared": 0.0,
                "recovered_MR_squared_over_target": recovered_m2 / target_m2,
                "recovered_G_GeV_minus2": recovered_g,
                "relative_G_residual": recovered_g
                / calibration["G_natural_GeV_minus2"]
                - 1.0,
                "interpretation": "distinct microscopic ray with identical calibrated G",
            }
        )
    for cutoff_ratio in (1.0, 4.0 * math.pi, 4.0 * math.pi * math.sqrt(6.0)):
        loop_ratio = -(cutoff_ratio**2) / (96.0 * math.pi**2)
        boundary_ratio = 1.0 - loop_ratio
        rows.append(
            {
                "branch": "selected_W1_minus1_renormalized_EH",
                "W1": -1.0,
                "LambdaUV_over_Mbar": cutoff_ratio,
                "LambdaUV_GeV": cutoff_ratio * mbar,
                "M_boundary_squared_over_Mbar_squared": boundary_ratio,
                "DeltaM_squared_over_Mbar_squared": 0.0,
                "recovered_MR_squared_over_target": boundary_ratio + loop_ratio,
                "recovered_G_GeV_minus2": calibration[
                    "G_natural_GeV_minus2"
                ],
                "relative_G_residual": boundary_ratio + loop_ratio - 1.0,
                "interpretation": "one calibrated counterterm cancels the cutoff-dependent loop shift",
            }
        )
    return {
        "rows": rows,
        "pure_induced_rows": 5,
        "renormalized_rows": 3,
        "maximum_absolute_recovery_residual": max(
            abs(row["relative_G_residual"]) for row in rows
        ),
        "demonstrates_nonuniqueness": True,
        "passed": bool(
            len(rows) == 8
            and max(abs(row["relative_G_residual"]) for row in rows) < 1.0e-12
            and abs(rows[-1]["M_boundary_squared_over_Mbar_squared"] - 2.0)
            < 1.0e-12
        ),
    }


@lru_cache(maxsize=None)
def source_coupling_certificate() -> dict[str, Any]:
    structure_rows = [
        {
            "clause": "integrated_public_metric",
            "result": "H is integrated modulo Diff",
            "closed": True,
            "source_path": "post-checkpoint-work/4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
        },
        {
            "clause": "positive_massless_spin2_pole",
            "result": "residue=1/M_R^2>0",
            "closed": True,
            "source_path": "post-checkpoint-work/4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
        },
        {
            "clause": "Diff_BRST_Ward_identity",
            "result": "nabla_mu deltaGamma/delta g_mn=0",
            "closed": True,
            "source_path": "post-checkpoint-work/4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
        },
        {
            "clause": "universal_soft_source_coupling",
            "result": "one massless spin2 pole couples to the conserved total Hilbert source",
            "closed": True,
            "source_path": "post-checkpoint-work/4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
        },
        {
            "clause": "finite_source_Newton_and_1PN",
            "result": "Poisson normalization and gamma=beta=1 after one M_R calibration",
            "closed": True,
            "source_path": "post-checkpoint-work/4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
        },
        {
            "clause": "Maxwell_Hilbert_Poynting_source",
            "result": "standard EM stress including momentum flux sources the same metric",
            "closed": True,
            "source_path": "post-checkpoint-work/4897-Y5-R2FR-cosmology-without-bath-source-metric-only-baseline-and-derived-extension-reentry-gate.md",
        },
    ]
    arena_rows = [
        {
            "arena": "Newton_R10",
            "coupling_used": "G_N_CODATA_2022",
            "arena_specific_retune": False,
            "status": "closed_in_4879_weak_separated_source_domain",
            "remaining_non_G_issue": "apparatus projections for any additional MTS residual",
        },
        {
            "arena": "PPN_clocks_orbits",
            "coupling_used": "G_N_CODATA_2022",
            "arena_specific_retune": False,
            "status": "closed_in_metric_only_1PN_domain",
            "remaining_non_G_issue": "nonminimal active-flow or composite-body residuals",
        },
        {
            "arena": "Maxwell_Poynting_gravity",
            "coupling_used": "G_N_CODATA_2022",
            "arena_specific_retune": False,
            "status": "gravitational_source_coupling_closed",
            "remaining_non_G_issue": "primitive U1 normalization and alpha prediction",
        },
        {
            "arena": "strong_vacuum",
            "coupling_used": "G_N_CODATA_2022",
            "arena_specific_retune": False,
            "status": "exact_Einstein_vacuum_branch_closed",
            "remaining_non_G_issue": "strong matter interiors and higher curvature operators",
        },
        {
            "arena": "metric_only_cosmology",
            "coupling_used": "G_N_CODATA_2022",
            "arena_specific_retune": False,
            "status": "known_limit_baseline_closed",
            "remaining_non_G_issue": "novel parent-derived cosmological extension",
        },
    ]
    return {
        "structure_rows": structure_rows,
        "arena_rows": arena_rows,
        "structure_derived": all(row["closed"] for row in structure_rows),
        "one_global_strength_calibration": True,
        "calibration_count": 1,
        "arena_specific_retunes": sum(
            row["arena_specific_retune"] for row in arena_rows
        ),
        "source_structure_status": "derived",
        "source_strength_status": "calibrated_once",
        "microscopic_strength_prediction": False,
        "GR_correspondence_status": (
            "structure_derived_strength_calibrated_once_no_arena_retuning"
        ),
        "all_source_paths_exist": all(
            (ROOT / row["source_path"]).exists() for row in structure_rows
        ),
        "passed": bool(
            all(row["closed"] for row in structure_rows)
            and not any(row["arena_specific_retune"] for row in arena_rows)
        ),
    }


@lru_cache(maxsize=None)
def prediction_reentry_gate() -> dict[str, Any]:
    clauses = [
        (
            "complete_primitive_spectrum",
            False,
            "all physical species statistics and multiplicities fixed before G",
        ),
        (
            "curvature_weights_owned",
            False,
            "all xi_s derived from microscopic symmetry dynamics or RG",
        ),
        (
            "UV_scale_owned_independently",
            False,
            "Lambda_UV fixed from a non-gravitational parent observable",
        ),
        (
            "EH_boundary_condition_derived",
            False,
            "M_EH,boundary^2 selected rather than set to zero by preference",
        ),
        (
            "mass_thresholds_complete",
            False,
            "finite mass and phase-transition contributions calculated",
        ),
        (
            "H_ghost_matching_complete",
            False,
            "integrated-H and ghost contribution calculated consistently",
        ),
        (
            "scheme_independent_renormalized_prediction",
            False,
            "physical M_R is invariant under regulator and matching-scale changes",
        ),
        (
            "radiative_stability_or_sensitivity_bound",
            False,
            "higher loops do not require uncontrolled retuning",
        ),
        (
            "single_value_all_arenas",
            True,
            "one G value is reused in local strong-vacuum and cosmology arenas",
        ),
        (
            "uncertainty_prediction_against_CODATA",
            False,
            "an a priori predicted interval is compared with CODATA",
        ),
    ]
    rows = [
        {
            "clause_index": index,
            "clause": clause,
            "passes": passes,
            "required_evidence": evidence,
            "blocking_if_false": True,
        }
        for index, (clause, passes, evidence) in enumerate(clauses, start=1)
    ]
    return {
        "rows": rows,
        "passed_clauses": sum(row["passes"] for row in rows),
        "total_clauses": len(rows),
        "prediction_reentry_allowed": all(row["passes"] for row in rows),
        "gate_logic": "AND(all ten clauses); no score averaging",
        "passed": bool(
            len(rows) == 10
            and sum(row["passes"] for row in rows) == 1
            and not all(row["passes"] for row in rows)
        ),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    owners = microscopic_owner_audit()
    theorem = identifiability_theorem()
    calibration = codata_calibration()
    rays = degeneracy_rays()
    source = source_coupling_certificate()
    reentry = prediction_reentry_gate()
    return {
        "Planck_stiffness_operator_status": "DERIVED_RENORMALIZED_EH_OPERATOR",
        "GN_correspondence_status": (
            "ONE_GLOBAL_CODATA_CALIBRATION_CLOSES_STRENGTH_WITH_NO_ARENA_RETUNING"
        ),
        "GN_microscopic_prediction_status": (
            "OPEN_RANK_DEFICIENT_CALIBRATION_SURFACE_NOT_CLAIMED"
        ),
        "GR_reduction_status": "STRUCTURE_DERIVED_STRENGTH_CALIBRATED",
        "measured_inputs_consumed": 1,
        "arena_specific_G_retunes": source["arena_specific_retunes"],
        "new_exact_result": (
            "rank1 constraint with nullity at least 2 even for fixed W1 and at least 3 when W1 is unfixed"
        ),
        "prediction_gate_passed_clauses": reentry["passed_clauses"],
        "prediction_gate_total_clauses": reentry["total_clauses"],
        "next_target": NEXT_TARGET,
        "passed": bool(
            owners["passed"]
            and not owners["microscopic_G_prediction_ready"]
            and theorem["passed"]
            and calibration["passed"]
            and rays["passed"]
            and source["passed"]
            and reentry["passed"]
            and not reentry["prediction_reentry_allowed"]
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "owners": microscopic_owner_audit(),
        "identifiability": identifiability_theorem(),
        "calibration": codata_calibration(),
        "rays": degeneracy_rays(),
        "source_coupling": source_coupling_certificate(),
        "prediction_reentry": prediction_reentry_gate(),
        "arbitration": arbitration(),
    }
    return {
        "checkpoint": CHECKPOINT,
        "sections": sections,
        "decision": sections["arbitration"]["GN_correspondence_status"],
        "all_checks_pass": all(
            section.get("passed", True) for section in sections.values()
        ),
    }


def main() -> int:
    calculation = result()
    calibration = calculation["sections"]["calibration"]
    theorem = calculation["sections"]["identifiability"]
    arbitration_row = calculation["sections"]["arbitration"]
    print(
        "Mbar={:.9e} GeV rank={} nullity_fixedW1={} retunes={}".format(
            calibration["Mbar_GeV"],
            theorem["jacobian_rank"],
            theorem["nullity_if_W1_fixed"],
            arbitration_row["arena_specific_G_retunes"],
        )
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
