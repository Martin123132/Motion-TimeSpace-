from __future__ import annotations

import csv
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

CHECKPOINT = "4897"
NEXT_TARGET = (
    "4898-Y5-R2FR-microscopic-Planck-stiffness-owner-and-GN-calibration-"
    "versus-prediction-gate.md"
)
H0_KM_S_MPC = 67.4
MPC_M = 3.085677581491367e22
C_M_S = 299792458.0
H0_PER_SECOND = H0_KM_S_MPC * 1000.0 / MPC_M
OMEGA_R = 9.0e-5
OMEGA_M = 0.315
OMEGA_LAMBDA = 1.0 - OMEGA_R - OMEGA_M


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    sources = [
        (
            "SRC4897_00_4896",
            POST
            / "4896-Y5-R2FR-full-matrix-nonlocal-FLRW-reshoot-covariant-bath-stress-and-constraint-gate.md",
            "MTS_FULL_MATRIX_FLRW_STRESS_RETIREMENT_GATE_4896",
        ),
        (
            "SRC4897_01_4896_validation",
            OUTPUT / "P8_Y5_BRR545_4896_VALIDATION.csv",
            "VAL4896_OVERALL,PASS",
        ),
        (
            "SRC4897_02_4875",
            POST
            / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875",
        ),
        (
            "SRC4897_03_4877",
            POST
            / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877",
        ),
        (
            "SRC4897_04_4879",
            POST
            / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
            "MTS_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879",
        ),
        (
            "SRC4897_05_4880",
            POST
            / "4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-domain-of-validity-and-strong-field-entry-gate.md",
            "MTS_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880",
        ),
    ]
    rows = [
        {
            "source_id": source_id,
            "source_type": "validated_parent_derivation_or_output",
            "source_path": str(path),
            "source_exists": path.exists(),
            "marker": marker,
            "marker_found": contains(path, marker),
        }
        for source_id, path, marker in sources
    ]
    return {
        "rows": rows,
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


@lru_cache(maxsize=None)
def metric_only_baseline() -> dict[str, Any]:
    lambda_cal = 3.0 * OMEGA_LAMBDA * H0_PER_SECOND**2 / C_M_S**2
    rows: list[dict[str, Any]] = []
    for redshift in (1.0e6, 1100.0, 100.0, 10.0, 3.0, 2.0, 1.0, 0.5, 0.0):
        scale_factor = 1.0 / (1.0 + redshift)
        radiation = OMEGA_R * scale_factor**-4
        matter = OMEGA_M * scale_factor**-3
        e_squared = radiation + matter + OMEGA_LAMBDA
        e_value = math.sqrt(e_squared)
        h_value = -(4.0 * radiation + 3.0 * matter) / (2.0 * e_squared)
        q_total = 0.0
        rows.append(
            {
                "redshift": redshift,
                "scale_factor": scale_factor,
                "E": e_value,
                "dlnH_dN": h_value,
                "Omega_r_of_z": radiation / e_squared,
                "Omega_m_of_z": matter / e_squared,
                "Omega_Lambda_of_z": OMEGA_LAMBDA / e_squared,
                "Q_total": q_total,
                "Friedmann_fraction_sum": (
                    radiation + matter + OMEGA_LAMBDA
                )
                / e_squared,
            }
        )
    return {
        "rows": rows,
        "baseline_action": (
            "Gamma_base=int sqrt(-g)[M_R^2(R-2Lambda_cal)/2]+"
            "S_matter[g]+S_EM[g]+Gamma_EFT_residual"
        ),
        "Friedmann_equation": (
            "E^2=Omega_r a^-4+Omega_m a^-3+Omega_Lambda"
        ),
        "matter_conservation": "nabla_mu T_matter^munu=0",
        "exchange_current": "Q^nu=0",
        "Newton_constant": "G_N=1/(8 pi M_R^2)",
        "PPN_gamma": 1.0,
        "PPN_beta": 1.0,
        "Maxwell_stress": (
            "T_EM_mn=F_ma F_n^a-g_mn F_ab F^ab/4 including Poynting flux"
        ),
        "Lambda_cal_per_square_metre": lambda_cal,
        "Lambda_status": (
            "single_renormalized_matching_condition_not_MTS_prediction"
        ),
        "GN_status": (
            "measured_calibration_of_M_R_until_Ns_xi_LambdaUV_are_independent"
        ),
        "novel_cosmology_prediction": False,
        "known_limit_baseline": True,
        "passed": bool(
            abs(rows[-1]["E"] - 1.0) < 1.0e-14
            and all(
                abs(row["Friedmann_fraction_sum"] - 1.0) < 1.0e-14
                and row["Q_total"] == 0.0
                for row in rows
            )
            and 1.08e-52 < lambda_cal < 1.10e-52
        ),
    }


@lru_cache(maxsize=None)
def cosmology_quarantine() -> dict[str, Any]:
    claims = {
        row["claim_id"]: row
        for row in read_csv(FORMAL / "02-claims-register.csv")
    }
    claim_ids = tuple(f"L-{number}" for number in range(729, 739))
    rows: list[dict[str, Any]] = []
    for claim_id in claim_ids:
        claim = claims[claim_id]
        number = int(claim_id.split("-")[1])
        if number <= 735:
            status = (
                "historical_conditional_diagnostic_superseded_by_4896_parent_retirement"
            )
            retained_asset = (
                "data_pipeline_standard_species_or_response_method_only"
            )
        elif number == 736:
            status = "demotion_step_confirmed_by_later_full_parent_test"
            retained_asset = "causal_auto_kernel_and_reciprocity_obstruction"
        elif number == 737:
            status = (
                "spectral_and_stationary_local_theorems_retained_cosmology_application_retired"
            )
            retained_asset = "positive_matrix_FDT_and_stationary_local_decoupling"
        else:
            status = "authoritative_selected_bath_cosmology_retirement"
            retained_asset = "covariant_stress_UV_no_go_and_reshoot_rejection"
        rows.append(
            {
                "claim_id": claim_id,
                "claim": claim["claim"],
                "historical_status": claim["status"],
                "current_cosmology_status": status,
                "retained_asset": retained_asset,
                "eligible_for_current_parent_cosmology_claim": False,
                "eligible_for_method_reuse": True,
                "authoritative_decision_claim": claim_id == "L-738",
            }
        )
    return {
        "rows": rows,
        "quarantined_claims": len(rows),
        "claimable_parent_cosmology_rows": sum(
            row["eligible_for_current_parent_cosmology_claim"] for row in rows
        ),
        "authoritative_retirement_rows": sum(
            row["authoritative_decision_claim"] for row in rows
        ),
        "rule": (
            "retired bath outputs may test code or preserve methods but may not "
            "be cited as current MTS parent cosmology predictions"
        ),
        "passed": bool(
            len(rows) == 10
            and not any(
                row["eligible_for_current_parent_cosmology_claim"]
                for row in rows
            )
            and sum(row["authoritative_decision_claim"] for row in rows) == 1
        ),
    }


@lru_cache(maxsize=None)
def extension_reentry_gate() -> dict[str, Any]:
    clauses = [
        (
            "parent_operator_predeclared",
            "covariant operator and coefficients derived before cosmology residual inspection",
        ),
        (
            "same_parent_stress",
            "Hilbert or SK stress varied from the same action/kernel as the response",
        ),
        (
            "Ward_and_constraint_closure",
            "Friedmann momentum clock and finite-k identities close together",
        ),
        (
            "stationary_local_decoupling",
            "Newton PPN clocks Maxwell and source coupling retain their certified limit",
        ),
        (
            "early_gravity_limit",
            "physical radiation and locally calibrated G give an acceptable early expansion",
        ),
        (
            "no_arena_specific_G_or_Lambda_reset",
            "G_N and the single Lambda matching condition are not retuned for cosmology",
        ),
        (
            "derived_activation_amplitude",
            "target amplitude and activation history follow from parent inputs rather than fit-only switches",
        ),
        (
            "state_and_FDT_owner",
            "dissipative response and stochastic covariance share one physical state",
        ),
        (
            "finite_k_species_completion",
            "metric memory matter photon baryon and neutrino perturbations use one constraint system",
        ),
        (
            "fair_empirical_score",
            "fixed predeclared prediction is compared with refitted GR wCDM and CPL baselines and split data",
        ),
    ]
    bath_values = {
        "parent_operator_predeclared": True,
        "same_parent_stress": True,
        "Ward_and_constraint_closure": True,
        "stationary_local_decoupling": True,
        "early_gravity_limit": False,
        "no_arena_specific_G_or_Lambda_reset": True,
        "derived_activation_amplitude": False,
        "state_and_FDT_owner": True,
        "finite_k_species_completion": False,
        "fair_empirical_score": False,
    }
    rows: list[dict[str, Any]] = []
    for clause, evidence_required in clauses:
        rows.append(
            {
                "candidate": "retired_gamma1_sigma0p3_diagonal_bath",
                "clause": clause,
                "evidence_required": evidence_required,
                "passes": bath_values[clause],
                "blocking_if_false": True,
            }
        )
        rows.append(
            {
                "candidate": "future_derived_extension",
                "clause": clause,
                "evidence_required": evidence_required,
                "passes": False,
                "blocking_if_false": True,
            }
        )
    bath_rows = [
        row
        for row in rows
        if row["candidate"] == "retired_gamma1_sigma0p3_diagonal_bath"
    ]
    future_rows = [
        row for row in rows if row["candidate"] == "future_derived_extension"
    ]
    return {
        "rows": rows,
        "clauses_per_candidate": len(clauses),
        "retired_bath_passed_clauses": sum(row["passes"] for row in bath_rows),
        "retired_bath_reentry_allowed": all(row["passes"] for row in bath_rows),
        "future_extension_reentry_allowed": all(
            row["passes"] for row in future_rows
        ),
        "gate_logic": "reentry=AND(all ten clauses); no score averaging",
        "passed": bool(
            len(clauses) == 10
            and sum(row["passes"] for row in bath_rows) == 6
            and not all(row["passes"] for row in bath_rows)
            and not all(row["passes"] for row in future_rows)
        ),
    }


@lru_cache(maxsize=None)
def priority_redirect() -> dict[str, Any]:
    rows = [
        {
            "rank": 1,
            "target": "microscopic_Planck_stiffness_and_GN_owner",
            "current_status": (
                "G_N=12pi/[Ns(1-6xi)LambdaUV^2] derived but all three microscopic inputs are not independently fixed"
            ),
            "direct_goal_value": "closes calibration-versus-prediction boundary in Newton/source coupling",
            "selected_next": True,
        },
        {
            "rank": 2,
            "target": "primitive_matter_and_EM_normalization",
            "current_status": (
                "universal Hilbert and Poynting coupling derived conditionally; U1 normalization and alpha are not predicted"
            ),
            "direct_goal_value": "strengthens Maxwell and calibrated source descent",
            "selected_next": False,
        },
        {
            "rank": 3,
            "target": "vacuum_relevant_coupling_selection",
            "current_status": (
                "C0_R=-M_R^2 Lambda_cal is one honest renormalization condition rather than a prediction"
            ),
            "direct_goal_value": "addresses cosmological constant ownership",
            "selected_next": False,
        },
        {
            "rank": 4,
            "target": "strong_matter_and_curvature_cubed_owner",
            "current_status": (
                "Einstein vacuum exact; compact matter response calculated conditionally; first nonredundant vacuum Wilson coefficient open"
            ),
            "direct_goal_value": "extends local GR certificate beyond retained EFT domain",
            "selected_next": False,
        },
        {
            "rank": 5,
            "target": "new_cosmological_extension",
            "current_status": "no active derived extension after 4896 retirement",
            "direct_goal_value": "potential future novelty but lower priority than Newton ownership",
            "selected_next": False,
        },
    ]
    return {
        "rows": rows,
        "selected_target": rows[0]["target"],
        "next_target": NEXT_TARGET,
        "reason": (
            "the local metric pole and universal coupling are already conditional theorems; "
            "the largest direct objective gap is whether Newton stiffness is predicted or only calibrated"
        ),
        "passed": bool(
            [row["rank"] for row in rows] == [1, 2, 3, 4, 5]
            and sum(row["selected_next"] for row in rows) == 1
            and rows[0]["selected_next"]
        ),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    baseline = metric_only_baseline()
    quarantine = cosmology_quarantine()
    reentry = extension_reentry_gate()
    priority = priority_redirect()
    return {
        "metric_only_cosmology_status": (
            "ACTIVE_KNOWN_LIMIT_BASELINE_NOT_NOVEL_MTS_COSMOLOGY_PREDICTION"
        ),
        "retired_bath_outputs_status": (
            "QUARANTINED_FROM_CURRENT_PARENT_CLAIMS_METHODS_RETAINED"
        ),
        "new_extension_status": (
            "NO_ACTIVE_EXTENSION_REENTRY_REQUIRES_ALL_TEN_GATES"
        ),
        "local_GR_Newton_Maxwell_status": (
            "RETAIN_4875_4879_4880_CONDITIONAL_CERTIFICATES"
        ),
        "GN_prediction_status": baseline["GN_status"],
        "selected_next_target": priority["selected_target"],
        "next_target": NEXT_TARGET,
        "passed": bool(
            baseline["passed"]
            and quarantine["passed"]
            and reentry["passed"]
            and priority["passed"]
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "baseline": metric_only_baseline(),
        "quarantine": cosmology_quarantine(),
        "reentry": extension_reentry_gate(),
        "priority": priority_redirect(),
        "arbitration": arbitration(),
    }
    return {
        "checkpoint": CHECKPOINT,
        "sections": sections,
        "decision": sections["arbitration"]["metric_only_cosmology_status"],
        "all_checks_pass": all(
            section.get("passed", True) for section in sections.values()
        ),
    }


def main() -> int:
    calculation = result()
    baseline = calculation["sections"]["baseline"]
    quarantine = calculation["sections"]["quarantine"]
    reentry = calculation["sections"]["reentry"]
    priority = calculation["sections"]["priority"]
    print(
        "Lambda_cal={:.9e} quarantined={} bath_reentry={} next={}".format(
            baseline["Lambda_cal_per_square_metre"],
            quarantine["quarantined_claims"],
            reentry["retired_bath_reentry_allowed"],
            priority["selected_target"],
        )
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
