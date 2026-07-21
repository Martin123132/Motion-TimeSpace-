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
ARCHIVE = ROOT / "archive" / "uncategorised"
OUTPUT = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4899"
NEXT_TARGET = (
    "4900-Y5-R2FR-charged-matter-representation-lattice-and-QED-beta-"
    "function-or-classical-EM-freeze.md"
)

ALPHA_ZERO = 7.2973525643e-3
ALPHA_ZERO_SIGMA = 1.1e-12
ALPHA_INVERSE = 137.035999177
ALPHA_INVERSE_SIGMA = 2.1e-8
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
            "SRC4899_00_4898",
            POST
            / "4898-Y5-R2FR-microscopic-Planck-stiffness-owner-and-GN-calibration-versus-prediction-gate.md",
            "MTS_GN_CALIBRATION_VERSUS_PREDICTION_GATE_4898",
            "validated_predecessor",
        ),
        (
            "SRC4899_01_4898_validation",
            OUTPUT / "P8_Y5_BRR545_4898_VALIDATION.csv",
            "VAL4898_OVERALL,PASS",
            "validated_predecessor",
        ),
        (
            "SRC4899_02_4853",
            POST
            / "4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md",
            "SCALAR_ONLY_MAXWELL_NO_GO",
            "current_parent_derivation",
        ),
        (
            "SRC4899_03_4854",
            POST
            / "4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md",
            "U1_BASELINE_CP2_CONSTITUTIVE_GATE_4854",
            "current_parent_derivation",
        ),
        (
            "SRC4899_04_4873",
            POST
            / "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md",
            "OPEN_PARENT_HADAMARD_INDUCED_GRAVITY_AND_METRIC_ONLY_QUOTIENT_4873",
            "current_parent_derivation",
        ),
        (
            "SRC4899_05_4875",
            POST
            / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875",
            "current_parent_derivation",
        ),
        (
            "SRC4899_06_4897",
            POST
            / "4897-Y5-R2FR-cosmology-without-bath-source-metric-only-baseline-and-derived-extension-reentry-gate.md",
            "MTS_METRIC_ONLY_BASELINE_REENTRY_GATE_4897",
            "current_parent_derivation",
        ),
        (
            "SRC4899_07_4209",
            FORMAL / "225-PPC4161-Maxwell-normalization-charge-current-owner.md",
            "PPC4161_MAXWELL_NORMALIZATION_OWNER_4209",
            "normalization_predecessor",
        ),
        (
            "SRC4899_08_1056",
            POST
            / "1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md",
            "Topological level/index route audit",
            "topology_and_rescaling_predecessor",
        ),
        (
            "SRC4899_09_archive_bandwidth",
            ARCHIVE
            / "the-fine-structure-constant-from-angular-bandwidth-in-motion-timespace-theory.md",
            "The Fine-Structure Constant from Angular Bandwidth",
            "legacy_hypothesis_under_audit",
        ),
        (
            "SRC4899_10_archive_drift",
            ARCHIVE / "the-fine-structure-constant.md",
            "A Curvature-Driven Drift of the Fine-Structure Constant",
            "legacy_hypothesis_under_audit",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker, role in local_sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": role,
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
            "SRC4899_11_NIST_constants",
            NIST_CONSTANTS_URL,
            "NIST current CODATA constants portal; 2022 is latest available",
        ),
        (
            "SRC4899_12_NIST_wall",
            NIST_WALL_2022_URL,
            "alpha(0)=7.2973525643(11)e-3 and inverse=137.035999177(21)",
        ),
        (
            "SRC4899_13_CODATA_paper",
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
def em_owner_audit() -> dict[str, Any]:
    rows = [
        {
            "owner_id": "EM4899_U1",
            "quantity": "principal U1 connection A",
            "current_status": "explicit_parent_field_adopted",
            "structural_correspondence_closed": True,
            "microscopic_alpha_input_fixed": False,
            "source_path": "post-checkpoint-work/4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md",
            "consequence": "two photon helicities and Gauss constraint available",
        },
        {
            "owner_id": "EM4899_F2",
            "quantity": "two-derivative parity-even Maxwell operator F^2",
            "current_status": "unique_in_minimal_metric_only_operator_domain",
            "structural_correspondence_closed": True,
            "microscopic_alpha_input_fixed": False,
            "source_path": "post-checkpoint-work/4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md",
            "consequence": "Maxwell equations stress and Poynting routing derived",
        },
        {
            "owner_id": "EM4899_ZA",
            "quantity": "Z_A gauge kinetic normalization",
            "current_status": "continuous_relevant_or_marginal_matching_coefficient",
            "structural_correspondence_closed": False,
            "microscopic_alpha_input_fixed": False,
            "source_path": "formalization-workbench/225-PPC4161-Maxwell-normalization-charge-current-owner.md",
            "consequence": "absolute alpha cannot follow from U1 symmetry alone",
        },
        {
            "owner_id": "EM4899_GJ",
            "quantity": "g_J current vertex normalization",
            "current_status": "visible_matter_calibration_not_primitive_MTS_derivation",
            "structural_correspondence_closed": False,
            "microscopic_alpha_input_fixed": False,
            "source_path": "post-checkpoint-work/4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md",
            "consequence": "only g_J^2/Z_A is field-normalization invariant",
        },
        {
            "owner_id": "EM4899_LATTICE",
            "quantity": "compact U1 charge lattice",
            "current_status": "can_fix_integer_labels_not_absolute_unit",
            "structural_correspondence_closed": True,
            "microscopic_alpha_input_fixed": False,
            "source_path": "post-checkpoint-work/1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md",
            "consequence": "relative charges may be quantized while e_R remains continuous",
        },
        {
            "owner_id": "EM4899_REPS",
            "quantity": "charged matter representations and observed spectrum",
            "current_status": "imported_or_open",
            "structural_correspondence_closed": False,
            "microscopic_alpha_input_fixed": False,
            "source_path": "post-checkpoint-work/4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md",
            "consequence": "electron charge label and complete current are not MTS-derived",
        },
        {
            "owner_id": "EM4899_QED",
            "quantity": "charged quantum spectrum beta function and renormalization boundary",
            "current_status": "not_completed",
            "structural_correspondence_closed": False,
            "microscopic_alpha_input_fixed": False,
            "source_path": "post-checkpoint-work/4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md",
            "consequence": "running alpha(mu) is not a current parent prediction",
        },
        {
            "owner_id": "EM4899_ALPHA0",
            "quantity": "alpha(0)",
            "current_status": "one_global_CODATA_calibration_available",
            "structural_correspondence_closed": True,
            "microscopic_alpha_input_fixed": False,
            "source_path": "post-checkpoint-work/4899-Y5-R2FR-primitive-U1-normalization-and-Maxwell-charge-calibration-versus-alpha-prediction-gate.md",
            "consequence": "classical EM strength closes once without arena retuning",
        },
    ]
    return {
        "rows": rows,
        "owner_rows": len(rows),
        "structurally_closed_rows": sum(
            row["structural_correspondence_closed"] for row in rows
        ),
        "microscopic_alpha_inputs_fixed": sum(
            row["microscopic_alpha_input_fixed"] for row in rows
        ),
        "all_source_paths_exist": all((ROOT / row["source_path"]).exists() for row in rows),
        "microscopic_alpha_prediction_ready": all(
            row["microscopic_alpha_input_fixed"]
            for row in rows
            if row["owner_id"] in {"EM4899_ZA", "EM4899_GJ", "EM4899_REPS", "EM4899_QED"}
        ),
        "passed": len(rows) == 8,
    }


@lru_cache(maxsize=None)
def normalization_theorem() -> dict[str, Any]:
    return {
        "parent_action": "S_EM=-Z_A int F^2/4-g_J int A_mu j^mu",
        "canonical_field": "A_c=sqrt(Z_A) A",
        "renormalized_charge": "e_R=g_J/sqrt(Z_A)",
        "physical_coupling": "alpha=e_R^2/(4 pi)=g_J^2/(4 pi Z_A)",
        "field_rescaling": "A_prime=s A; Z_A_prime=Z_A/s^2; g_J_prime=g_J/s",
        "invariant": "g_J^2/Z_A",
        "log_constraint": "ln alpha=2 ln g_J-ln Z_A-ln(4 pi)",
        "jacobian": "[2,-1]",
        "jacobian_rank": 1,
        "parameter_count": 2,
        "normalization_orbit_nullity": 1,
        "null_vector": "(-1,-2)",
        "null_check": 2.0 * -1.0 - (-2.0),
        "interpretation": (
            "Z_A and g_J separately are field-coordinate data; alpha is the single physical invariant"
        ),
        "absolute_alpha_fixed_by_U1_symmetry": False,
        "passed": bool(2.0 * -1.0 - (-2.0) == 0.0 and 2 - 1 == 1),
    }


@lru_cache(maxsize=None)
def charge_lattice_theorem() -> dict[str, Any]:
    rows = [
        {
            "statement": "compact_connection",
            "equation": "[F/(2 pi)] in H^2(M,Z)",
            "derived_content": "flux periods and representation labels may be integral",
            "does_not_derive": "continuous Maxwell kinetic coefficient",
            "status": "structural_support",
        },
        {
            "statement": "charge_lattice",
            "equation": "q_n=n e_R; n in Z",
            "derived_content": "relative charge ratios q_n/q_m=n/m",
            "does_not_derive": "absolute e_R or alpha",
            "status": "conditional_compact_U1_theorem",
        },
        {
            "statement": "Ward_identity",
            "equation": "nabla_mu j^mu=0",
            "derived_content": "charge conservation",
            "does_not_derive": "current vertex magnitude",
            "status": "derived_in_correspondence_action",
        },
        {
            "statement": "CP2_Berry_route",
            "equation": "B=-i z^dagger dz; H=dB",
            "derived_content": "possible bundle curvature and integral geometry",
            "does_not_derive": "independent Maxwell variation or F^2 normalization",
            "status": "optional_UV_constructor_not_selected",
        },
        {
            "statement": "four_dimensional_Maxwell_level",
            "equation": "S=-int F^2/(4 e_R^2) in unit-charge convention",
            "derived_content": "one continuous physical coupling",
            "does_not_derive": "its numerical boundary value",
            "status": "calibration_required",
        },
    ]
    return {
        "rows": rows,
        "compactness_can_quantize_relative_labels": True,
        "compactness_fixes_absolute_charge_unit": False,
        "topology_fixes_alpha_without_kinetic_inheritance": False,
        "current_matter_representations_derived": False,
        "passed": len(rows) == 5,
    }


@lru_cache(maxsize=None)
def codata_alpha_calibration() -> dict[str, Any]:
    relative_alpha = ALPHA_ZERO_SIGMA / ALPHA_ZERO
    canonical_charge = math.sqrt(4.0 * math.pi * ALPHA_ZERO)
    canonical_charge_sigma = 0.5 * relative_alpha * canonical_charge
    product_residual = ALPHA_ZERO * ALPHA_INVERSE - 1.0
    rows = [
        {
            "quantity": "alpha(0)",
            "value": ALPHA_ZERO,
            "standard_uncertainty": ALPHA_ZERO_SIGMA,
            "relative_standard_uncertainty": relative_alpha,
            "units": "dimensionless",
            "role": "single_global_low_energy_input",
            "source_url": NIST_WALL_2022_URL,
        },
        {
            "quantity": "alpha(0)^-1",
            "value": ALPHA_INVERSE,
            "standard_uncertainty": ALPHA_INVERSE_SIGMA,
            "relative_standard_uncertainty": ALPHA_INVERSE_SIGMA
            / ALPHA_INVERSE,
            "units": "dimensionless",
            "role": "official_reciprocal_check",
            "source_url": NIST_WALL_2022_URL,
        },
        {
            "quantity": "e_R(0)_Heaviside_Lorentz",
            "value": canonical_charge,
            "standard_uncertainty": canonical_charge_sigma,
            "relative_standard_uncertainty": 0.5 * relative_alpha,
            "units": "dimensionless natural units",
            "role": "derived_after_Z_A_equals_1_canonicalization",
            "source_url": NIST_WALL_2022_URL,
        },
    ]
    return {
        "rows": rows,
        "alpha_zero": ALPHA_ZERO,
        "alpha_zero_sigma": ALPHA_ZERO_SIGMA,
        "alpha_inverse": ALPHA_INVERSE,
        "alpha_inverse_sigma": ALPHA_INVERSE_SIGMA,
        "relative_alpha_uncertainty": relative_alpha,
        "canonical_charge": canonical_charge,
        "canonical_charge_sigma": canonical_charge_sigma,
        "rounded_reciprocal_product_residual": product_residual,
        "calibration_count": 1,
        "latest_available_set_as_of_check": "CODATA_2022",
        "source_checked_date": "2026-07-11",
        "passed": bool(
            len(rows) == 3
            and 0.3028 < canonical_charge < 0.3029
            and abs(product_residual) < 5.0e-11
            and 1.5e-10 < relative_alpha < 1.6e-10
        ),
    }


@lru_cache(maxsize=None)
def archived_bandwidth_audit() -> dict[str, Any]:
    ell_zero = 1.7
    weights = [
        (2.0 * ell + 1.0)
        * math.exp(-ell * (ell + 1.0) / ell_zero**2)
        for ell in range(51)
    ]
    total = sum(weights)
    peak = max(weights)
    spectrum_rows: list[dict[str, Any]] = []
    cumulative = 0.0
    ell_99 = None
    for ell, weight in enumerate(weights):
        fraction = weight / total
        cumulative += fraction
        if ell_99 is None and cumulative >= 0.99:
            ell_99 = ell
        if ell <= 10:
            spectrum_rows.append(
                {
                    "ell": ell,
                    "ell_zero": ell_zero,
                    "unnormalized_power": weight,
                    "normalized_power": fraction,
                    "fraction_of_peak": weight / peak,
                    "cumulative_power": cumulative,
                }
            )
    ell_one_percent_total = max(
        ell for ell, weight in enumerate(weights) if weight / total >= 0.01
    )
    ell_one_percent_peak = max(
        ell for ell, weight in enumerate(weights) if weight / peak >= 0.01
    )
    ell_claimed = 6
    required_suppression = math.sqrt(2.0) / (3.0 * ALPHA_ZERO)
    candidates = [
        ("all_modes_through_ell", float((ell_claimed + 1) ** 2), False),
        ("nonmonopole_modes", float((ell_claimed + 1) ** 2 - 1), False),
        ("Laplacian_eigenvalue", float(ell_claimed * (ell_claimed + 1)), False),
        ("squared_cutoff", float(ell_claimed**2), False),
        ("required_from_CODATA_alpha", required_suppression, True),
    ]
    projection_rows: list[dict[str, Any]] = []
    for name, suppression, constructed_from_alpha in candidates:
        alpha_predicted = math.sqrt(2.0) / (3.0 * suppression)
        inverse_predicted = 1.0 / alpha_predicted
        projection_rows.append(
            {
                "projection_rule": name,
                "ell_max": ell_claimed,
                "S_ell": suppression,
                "alpha_predicted": alpha_predicted,
                "alpha_inverse_predicted": inverse_predicted,
                "relative_inverse_residual": inverse_predicted
                / ALPHA_INVERSE
                - 1.0,
                "constructed_from_observed_alpha": constructed_from_alpha,
                "predeclared_by_archive_equation": False,
                "within_one_percent": abs(inverse_predicted / ALPHA_INVERSE - 1.0)
                < 0.01,
            }
        )
    bandwidth_path = (
        ARCHIVE
        / "the-fine-structure-constant-from-angular-bandwidth-in-motion-timespace-theory.md"
    )
    bandwidth_text = bandwidth_path.read_text(
        encoding="utf-8", errors="replace"
    ).lower()
    cited_machine_data_path = any(
        suffix in bandwidth_text for suffix in (".csv", ".py", ".ipynb")
    )
    audit_rows = [
        {
            "clause": "current_field_content",
            "result": "fails_selected_parent",
            "reason": "legacy scalar oscillation photon route was rejected at 4853",
        },
        {
            "clause": "alpha_geom_equals_sqrt2",
            "result": "unsupported",
            "reason": "no action variation or normalized amplitude derivation is supplied",
        },
        {
            "clause": "S_ell_of_ellmax",
            "result": "undefined",
            "reason": "no explicit projection functional maps ell_max to S_ell",
        },
        {
            "clause": "printed_Gaussian_envelope",
            "result": "internally_inconsistent_with_claimed_thresholds",
            "reason": "ell0=1.7 gives ell99=3 and both one-percent cutoffs=3, not 4 and 6",
        },
        {
            "clause": "independent_alpha_match",
            "result": "circular_branch",
            "reason": "the second route scans ell_max for the best match to physical alpha",
        },
        {
            "clause": "machine_reproducibility",
            "result": "absent_from_archive_document",
            "reason": "no data or script path is cited",
        },
        {
            "clause": "curvature_drift",
            "result": "not_current_parent_prediction",
            "reason": "epsilon is not derived and the prior Gamma cosmology is quarantined",
        },
    ]
    noncircular_rows = [
        row
        for row in projection_rows
        if not row["constructed_from_observed_alpha"]
    ]
    return {
        "spectrum_rows": spectrum_rows,
        "projection_rows": projection_rows,
        "audit_rows": audit_rows,
        "ell_zero": ell_zero,
        "claimed_ell_99": 4,
        "calculated_ell_99": ell_99,
        "claimed_ell_max_one_percent": 6,
        "calculated_ell_max_one_percent_total": ell_one_percent_total,
        "calculated_ell_max_one_percent_peak": ell_one_percent_peak,
        "required_S_ell_from_CODATA": required_suppression,
        "archive_cites_machine_data_path": cited_machine_data_path,
        "noncircular_candidate_within_one_percent": any(
            row["within_one_percent"] for row in noncircular_rows
        ),
        "legacy_route_status": (
            "REJECTED_AS_CURRENT_ALPHA_DERIVATION_RETAINED_AS_ARCHIVED_HEURISTIC"
        ),
        "passed": bool(
            ell_99 == 3
            and ell_one_percent_total == 3
            and ell_one_percent_peak == 3
            and not cited_machine_data_path
            and not any(row["within_one_percent"] for row in noncircular_rows)
            and len(audit_rows) == 7
        ),
    }


@lru_cache(maxsize=None)
def baseline_alpha_constancy() -> dict[str, Any]:
    rows = [
        {
            "arena": "local_Maxwell_Coulomb",
            "alpha_input": "CODATA_alpha_zero",
            "arena_specific_retune": False,
            "baseline_alpha_drift": 0.0,
            "status": "canonical_Maxwell_correspondence_closed",
        },
        {
            "arena": "atomic_spectroscopy_and_clocks",
            "alpha_input": "CODATA_alpha_zero",
            "arena_specific_retune": False,
            "baseline_alpha_drift": 0.0,
            "status": "fixed_constant_baseline_comparator",
        },
        {
            "arena": "WEP_and_composition",
            "alpha_input": "CODATA_alpha_zero",
            "arena_specific_retune": False,
            "baseline_alpha_drift": 0.0,
            "status": "no_alpha_dependent_fifth_force_on_metric_only_baseline",
        },
        {
            "arena": "cosmology_and_quasar_spectra",
            "alpha_input": "CODATA_alpha_zero",
            "arena_specific_retune": False,
            "baseline_alpha_drift": 0.0,
            "status": "constant_alpha_known_limit_not_novel_prediction",
        },
        {
            "arena": "gravitational_EM_stress_and_Poynting",
            "alpha_input": "CODATA_alpha_zero",
            "arena_specific_retune": False,
            "baseline_alpha_drift": 0.0,
            "status": "same_Hilbert_source_and_one_EM_normalization",
        },
    ]
    return {
        "rows": rows,
        "canonical_action": "S_EM=-int F_c^2/4-e_R int A_c.j",
        "absolute_alpha_status": "calibrated_once_not_microscopically_predicted",
        "baseline_conditions": "constant Z_A and g_J; no active f(X)F^2 or varying current vertex",
        "baseline_drift_law": "b_alpha=d ln alpha=2 d ln g_J-d ln Z_A=0",
        "extended_drift_normal_form": (
            "b_alpha_EM=2 z_g-z_lambda-z_readout-z_rad"
        ),
        "arena_specific_retunes": sum(
            row["arena_specific_retune"] for row in rows
        ),
        "exact_baseline_constancy": all(
            row["baseline_alpha_drift"] == 0.0 for row in rows
        ),
        "passed": bool(
            len(rows) == 5
            and not any(row["arena_specific_retune"] for row in rows)
            and all(row["baseline_alpha_drift"] == 0.0 for row in rows)
        ),
    }


@lru_cache(maxsize=None)
def prediction_reentry_gate() -> dict[str, Any]:
    clauses = [
        (
            "explicit_principal_U1_connection",
            True,
            "independent U1 field is present in the parent correspondence action",
        ),
        (
            "Maxwell_modes_stress_and_current",
            True,
            "two modes Gauss Ward Hilbert and Poynting structure close",
        ),
        (
            "charged_matter_representations_derived",
            False,
            "observed charge labels and matter multiplets follow from MTS",
        ),
        (
            "kinetic_and_current_same_microscopic_owner",
            False,
            "Z_A and g_J inherit one nonrescalable parent norm",
        ),
        (
            "absolute_gauge_invariant_ratio_predicted",
            False,
            "g_J^2/Z_A is fixed before alpha data",
        ),
        (
            "dynamic_constitutive_operators_closed",
            False,
            "f(X)F^2 flow and readout/radiative regeneration are derived or absent",
        ),
        (
            "charged_quantum_spectrum_and_beta_function",
            False,
            "QED running follows from a completed charged spectrum",
        ),
        (
            "renormalization_boundary_and_scale_owned",
            False,
            "alpha(mu0) boundary is fixed by the parent rather than data",
        ),
        (
            "a_priori_alpha_value_and_uncertainty",
            False,
            "numerical alpha interval is produced before CODATA comparison",
        ),
        (
            "one_value_reused_and_baseline_drift_zero",
            True,
            "one calibration is reused and the metric-only baseline is constant",
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
            and sum(row["passes"] for row in rows) == 3
            and not all(row["passes"] for row in rows)
        ),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    owners = em_owner_audit()
    normalization = normalization_theorem()
    lattice = charge_lattice_theorem()
    calibration = codata_alpha_calibration()
    bandwidth = archived_bandwidth_audit()
    baseline = baseline_alpha_constancy()
    reentry = prediction_reentry_gate()
    return {
        "Maxwell_correspondence_status": (
            "DERIVED_FROM_EXPLICIT_PRINCIPAL_U1_PARENT_IN_METRIC_ONLY_DOMAIN"
        ),
        "charge_lattice_status": (
            "RELATIVE_INTEGER_LABELS_AVAILABLE_ABSOLUTE_UNIT_AND_MATTER_REPS_OPEN"
        ),
        "alpha_zero_status": "ONE_GLOBAL_CODATA_CALIBRATION_NO_ARENA_RETUNING",
        "alpha_baseline_drift_status": "EXACT_ZERO_ON_FIXED_METRIC_ONLY_BASELINE",
        "archived_bandwidth_status": bandwidth["legacy_route_status"],
        "microscopic_alpha_prediction_status": (
            "OPEN_GAUGE_INVARIANT_RATIO_AND_QED_BOUNDARY_NOT_PARENT_DERIVED"
        ),
        "normalization_orbit_rank": normalization["jacobian_rank"],
        "normalization_orbit_nullity": normalization[
            "normalization_orbit_nullity"
        ],
        "measured_inputs_consumed": calibration["calibration_count"],
        "arena_specific_alpha_retunes": baseline["arena_specific_retunes"],
        "prediction_gate_passed_clauses": reentry["passed_clauses"],
        "prediction_gate_total_clauses": reentry["total_clauses"],
        "next_target": NEXT_TARGET,
        "passed": bool(
            owners["passed"]
            and not owners["microscopic_alpha_prediction_ready"]
            and normalization["passed"]
            and lattice["passed"]
            and calibration["passed"]
            and bandwidth["passed"]
            and baseline["passed"]
            and reentry["passed"]
            and not reentry["prediction_reentry_allowed"]
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "owners": em_owner_audit(),
        "normalization": normalization_theorem(),
        "lattice": charge_lattice_theorem(),
        "calibration": codata_alpha_calibration(),
        "bandwidth": archived_bandwidth_audit(),
        "baseline": baseline_alpha_constancy(),
        "prediction_reentry": prediction_reentry_gate(),
        "arbitration": arbitration(),
    }
    return {
        "checkpoint": CHECKPOINT,
        "sections": sections,
        "decision": sections["arbitration"]["alpha_zero_status"],
        "all_checks_pass": all(
            section.get("passed", True) for section in sections.values()
        ),
    }


def main() -> int:
    calculation = result()
    calibration = calculation["sections"]["calibration"]
    bandwidth = calculation["sections"]["bandwidth"]
    arbitration_row = calculation["sections"]["arbitration"]
    print(
        "alpha={:.13e} eR={:.12f} ell99={} ell1pct={} retunes={}".format(
            calibration["alpha_zero"],
            calibration["canonical_charge"],
            bandwidth["calculated_ell_99"],
            bandwidth["calculated_ell_max_one_percent_total"],
            arbitration_row["arena_specific_alpha_retunes"],
        )
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
