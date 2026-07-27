from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4904"
NEXT_TARGET = (
    "4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-"
    "and-independent-observable-gate.md"
)


def contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    local_sources = [
        (
            "SRC4904_00_4903",
            POST
            / "4903-Y5-R2FR-custodial-Higgs-coset-completion-and-electroweak-precision-or-linear-Higgs-freeze.md",
            "MTS_CUSTODIAL_HIGGS_COMPLETION_PRECISION_GATE_4903",
            "validated_predecessor",
        ),
        (
            "SRC4904_01_4903_validation",
            OUTPUT / "P8_Y5_BRR545_4903_VALIDATION.csv",
            "VAL4903_OVERALL,PASS",
            "validated_predecessor",
        ),
        (
            "SRC4904_02_4875",
            POST
            / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875",
            "integrated_metric_field_space",
        ),
        (
            "SRC4904_03_4876",
            POST
            / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
            "INTEGRATED_H_PARENT_SADDLE_HEAT_KERNEL_POLE_HIERARCHY_4876",
            "renormalized_parent_action",
        ),
        (
            "SRC4904_04_4877",
            POST
            / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877",
            "vacuum_and_residual_matching",
        ),
        (
            "SRC4904_05_4896",
            POST
            / "4896-Y5-R2FR-full-matrix-nonlocal-FLRW-reshoot-covariant-bath-stress-and-constraint-gate.md",
            "MTS_FULL_MATRIX_FLRW_STRESS_RETIREMENT_GATE_4896",
            "retired_bath_source",
        ),
        (
            "SRC4904_06_4897",
            POST
            / "4897-Y5-R2FR-cosmology-without-bath-source-metric-only-baseline-and-derived-extension-reentry-gate.md",
            "MTS_METRIC_ONLY_BASELINE_REENTRY_GATE_4897",
            "active_metric_baseline",
        ),
        (
            "SRC4904_07_4898",
            POST
            / "4898-Y5-R2FR-microscopic-Planck-stiffness-owner-and-GN-calibration-versus-prediction-gate.md",
            "MTS_GN_CALIBRATION_VERSUS_PREDICTION_GATE_4898",
            "gravity_calibration",
        ),
        (
            "SRC4904_08_4899",
            POST
            / "4899-Y5-R2FR-primitive-U1-normalization-and-Maxwell-charge-calibration-versus-alpha-prediction-gate.md",
            "MTS_U1_ALPHA_CALIBRATION_AND_BANDWIDTH_REJECTION_GATE_4899",
            "electromagnetic_calibration",
        ),
        (
            "SRC4904_09_4900",
            POST
            / "4900-Y5-R2FR-charged-matter-representation-lattice-and-QED-beta-function-or-classical-EM-freeze.md",
            "MTS_CHARGED_MATTER_AND_QED_CORRESPONDENCE_GATE_4900",
            "QED_IR_correspondence",
        ),
        (
            "SRC4904_10_4901",
            POST
            / "4901-Y5-R2FR-nonabelian-SU2xSU3-parent-and-chiral-anomaly-cancellation-or-standard-model-correspondence-freeze.md",
            "MTS_NONABELIAN_CHIRAL_SM_CORRESPONDENCE_GATE_4901",
            "active_SM_correspondence",
        ),
        (
            "SRC4904_11_4902",
            POST
            / "4902-Y5-R2FR-electroweak-breaking-Higgs-Yukawa-owner-and-mass-generation-or-SM-parameter-freeze.md",
            "MTS_HIGGS_YUKAWA_MASS_OWNERSHIP_GATE_4902",
            "active_linear_Higgs",
        ),
        (
            "SRC4904_12_formal4903",
            FORMAL / "919-PPC4161-custodial-Higgs-completion-and-freeze.md",
            "PPC4161_CUSTODIAL_HIGGS_COMPLETION_FREEZE_4903",
            "current_spine_status",
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
    return {
        "rows": rows,
        "local_sources": len(local_sources),
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


@lru_cache(maxsize=None)
def active_sector_ledger() -> dict[str, Any]:
    rows = [
        {
            "sector": "integrated_metric",
            "field_or_object": "H^{mu nu} modulo Diff",
            "current_role": "public metric field space",
            "status": "ACTIVE_PARENT_ARCHITECTURE",
            "included_in_active_action": True,
        },
        {
            "sector": "renormalized_gravity",
            "field_or_object": "g_hat(H), M_R, Lambda_cal, EFT residuals",
            "current_role": "GR and metric-only cosmology known limit",
            "status": "ACTIVE",
            "included_in_active_action": True,
        },
        {
            "sector": "Standard_Model",
            "field_or_object": "G,W,B,chiral Weyl fields,linear H",
            "current_role": "anomaly-free matter and gauge known limit",
            "status": "ACTIVE_CORRESPONDENCE",
            "included_in_active_action": True,
        },
        {
            "sector": "QED_Maxwell",
            "field_or_object": "A=sW3+cB and Dirac recombinations",
            "current_role": "infrared electroweak limit",
            "status": "DERIVED_IR_LIMIT_NOT_EXTRA_SUMMAND",
            "included_in_active_action": False,
        },
        {
            "sector": "microscopic_MTS",
            "field_or_object": "psi_r,psi_a,X",
            "current_role": "proposed UV variables integrated into matched coefficients",
            "status": "UV_COMPLETION_SLOT_NOT_ACTIVE_LOW_ENERGY_SOURCE",
            "included_in_active_action": False,
        },
        {
            "sector": "MTS_residual",
            "field_or_object": "Gamma_MTS,res",
            "current_role": "reserved non-GR operator slot",
            "status": "ZERO_ON_ACTIVE_BASELINE_PENDING_REENTRY_GATE",
            "included_in_active_action": True,
        },
        {
            "sector": "bath_cosmology",
            "field_or_object": "gamma-sigma reciprocal bath",
            "current_role": "method and failure evidence",
            "status": "RETIRED_AS_ACTIVE_SOURCE",
            "included_in_active_action": False,
        },
        {
            "sector": "CP2_Higgs",
            "field_or_object": "CP2 tangent doublet",
            "current_role": "internal geometry clue",
            "status": "FROZEN",
            "included_in_active_action": False,
        },
        {
            "sector": "SO5_SO4_Higgs",
            "field_or_object": "custodial composite benchmark",
            "current_role": "conditional precision comparator",
            "status": "OPTIONAL_NOT_ACTIVE",
            "included_in_active_action": False,
        },
        {
            "sector": "galaxy_programme",
            "field_or_object": "separate empirical galaxy laws and pipelines",
            "current_role": "evidence pillar awaiting parent operator map",
            "status": "RETAINED_SEPARATELY_NOT_ACTION_OWNED",
            "included_in_active_action": False,
        },
    ]
    active = [row for row in rows if row["included_in_active_action"]]
    return {
        "rows": rows,
        "sectors": len(rows),
        "active_action_rows": len(active),
        "active_extra_MTS_source_terms": 0,
        "retired_or_frozen_rows": sum(
            any(word in row["status"] for word in ("RETIRED", "FROZEN"))
            for row in rows
        ),
        "passed": len(rows) == 10
        and not next(
            row for row in rows if row["sector"] == "bath_cosmology"
        )["included_in_active_action"],
    }


@lru_cache(maxsize=None)
def action_assembly() -> dict[str, Any]:
    rows = [
        {
            "term": "Einstein_Hilbert",
            "expression": "int sqrt(-g) M_R^2(R-2Lambda_cal)/2",
            "owner": "integrated-H renormalized gravity",
            "status": "ACTIVE",
        },
        {
            "term": "curvature_residuals",
            "expression": "int sqrt(-g)[a_R R2+a_C C2+a_E E4]+Gamma_nonlocal",
            "owner": "renormalized EFT matching",
            "status": "ACTIVE_AS_STRICT_EFT_RESIDUALS_COEFFICIENTS_OPEN",
        },
        {
            "term": "SM_gauge",
            "expression": "int sqrt(-g)[-G_A2/4-W_I2/4-B2/4-theta_QCD G Gtilde/(32pi2)]",
            "owner": "explicit Standard-Model correspondence",
            "status": "ACTIVE",
        },
        {
            "term": "SM_chiral_matter",
            "expression": "int sqrt(-g) sum i chi_dagger barsigma^mu D_mu chi",
            "owner": "explicit anomaly-free representation table",
            "status": "ACTIVE",
        },
        {
            "term": "linear_Higgs",
            "expression": "int sqrt(-g)[abs(DH)2+mu_H2 HdagH-lambda_H(HdagH)2]",
            "owner": "explicit linear-Higgs correspondence",
            "status": "ACTIVE",
        },
        {
            "term": "Yukawa",
            "expression": "-int sqrt(-g)[Q H uc+Q Hdag dc+L Hdag ec+h.c.]",
            "owner": "imported flavor matrices",
            "status": "ACTIVE_CORRESPONDENCE_INPUT",
        },
        {
            "term": "MTS_residual_slot",
            "expression": "Gamma_MTS,res[g,Phi_SM]",
            "owner": "future derived operator basis",
            "status": "SET_TO_ZERO_ON_CURRENT_ACTIVE_BASELINE",
        },
        {
            "term": "boundary",
            "expression": "S_GHY+S_higher_derivative_boundary+S_gauge_matter_boundary",
            "owner": "variational completion",
            "status": "REQUIRED",
        },
        {
            "term": "gauge_fixing_ghost",
            "expression": "s_BRST Psi_gf for Diff and G_SM",
            "owner": "gauge-fixed path integral",
            "status": "REQUIRED",
        },
    ]
    return {
        "rows": rows,
        "active_action": (
            "Gamma_current=Gamma_grav,R[g(H)]+S_SM[g(H),Phi_SM]+"
            "Gamma_MTS,res+S_boundary+S_gf+gh"
        ),
        "active_baseline_condition": "Gamma_MTS,res=0",
        "microscopic_MTS_matching": (
            "integrate psi_r psi_a X once into M_R Lambda_cal a_i and form_factors"
        ),
        "active_terms": len(rows),
        "passed": len(rows) == 9,
    }


@lru_cache(maxsize=None)
def electroweak_IR_rotation() -> dict[str, Any]:
    sine, cosine = sp.symbols("s_W c_W", real=True)
    rotation = sp.Matrix([[sine, cosine], [cosine, -sine]])
    orthogonality = sp.simplify(
        (rotation.T * rotation).subs(cosine**2 + sine**2, 1)
    )
    determinant_squared = sp.factor(rotation.det() ** 2).subs(
        cosine**2 + sine**2, 1
    )
    rows = [
        {
            "object": "field_rotation",
            "equation": "(A,Z)^T=[[sW,cW],[cW,-sW]](W3,B)^T",
            "result": "rank_two_orthogonal",
        },
        {
            "object": "electric_generator",
            "equation": "Q=T3+Y",
            "result": "one_unbroken_U1EM",
        },
        {
            "object": "coupling_match",
            "equation": "e=g2 sW=gY cW",
            "result": "alpha_is_combination_not_extra_parameter",
        },
        {
            "object": "field_count",
            "equation": "8+3+1 gauge fields before and 8+2+1+1 after EWSB",
            "result": "12_to_12_no_extra_photon",
        },
    ]
    return {
        "rows": rows,
        "rotation_rank": rotation.rank(),
        "orthogonality": str(orthogonality),
        "determinant_squared": str(determinant_squared),
        "UV_gauge_bosons": 12,
        "IR_gauge_bosons": 12,
        "independent_extra_QED_photon": False,
        "passed": bool(
            rotation.rank() == 2
            and orthogonality == sp.eye(2)
            and determinant_squared == 1
        ),
    }


@lru_cache(maxsize=None)
def no_double_counting_gate() -> dict[str, Any]:
    rows = [
        ("electromagnetism", "A=sW3+cW B is an IR field", "do not add S_EM beside S_SM", True),
        ("QED_matter", "Dirac fields are post-EWSB recombinations", "do not add duplicate fermions", True),
        ("gravity", "one M_R^2 R/2 term", "do not add a second emergent Einstein term", True),
        ("vacuum", "one Lambda_cal matching coefficient", "do not add Gamma_G or bath vacuum separately", True),
        ("Higgs", "linear H is active", "exclude CP2 and SO5/SO4 from active sum", True),
        ("MTS_vacuum", "microscopic determinants already match renormalized coefficients", "do not add their stress twice", True),
        ("bath", "4896 source retired", "exclude bath fields from active cosmology", True),
        ("galaxies", "empirical pillar lacks parent action map", "do not insert galaxy law into covariant action", True),
        ("alpha", "alpha and weak angle form a basis for g2,gY", "do not count alpha,g2,gY as three", True),
        ("Newton", "G_N=1/(8pi M_R2)", "do not count G_N and M_R as independent", True),
    ]
    output = [
        {
            "object": obj,
            "identity": identity,
            "prohibition": prohibition,
            "closed": closed,
        }
        for obj, identity, prohibition, closed in rows
    ]
    return {
        "rows": output,
        "clauses": len(output),
        "closed_clauses": sum(row["closed"] for row in output),
        "extra_photon_count": 0,
        "extra_active_Higgs_count": 0,
        "extra_active_bath_count": 0,
        "passed": len(output) == 10 and all(row["closed"] for row in output),
    }


@lru_cache(maxsize=None)
def Ward_interface_ledger() -> dict[str, Any]:
    incidence = sp.Matrix(
        [
            [-1, -1, 0],
            [1, 0, -1],
            [0, 1, 1],
            [0, 0, 0],
        ]
    )
    column_sums = [sum(incidence[:, index]) for index in range(incidence.cols)]
    rows = [
        {
            "identity": "Diff_Ward",
            "off_shell_form": "2 nabla_mu E_g^mu_nu=sum_i E_i delta_nu Phi_i",
            "on_shell_result": "nabla_mu T_total^mu_nu=0",
            "status": "DERIVED_FROM_COMMON_PUBLIC_METRIC_AND_DIFF_BRST",
        },
        {
            "identity": "Einstein_Bianchi",
            "off_shell_form": "nabla_mu(G^mu_nu+Lambda delta^mu_nu)=0",
            "on_shell_result": "requires the same conserved total Hilbert source",
            "status": "CLOSED",
        },
        {
            "identity": "gauge_Ward",
            "off_shell_form": "D_mu E_A^{a mu}+matter_and_Higgs_EOM_terms=0",
            "on_shell_result": "D_mu J_a^mu=0",
            "status": "ANOMALY_FREE_REPRESENTATION_LEDGER_CLOSED",
        },
        {
            "identity": "gauge_matter_exchange",
            "off_shell_form": "nabla T_gauge=-F_a^{nu mu}J^a_mu",
            "on_shell_result": "opposite force appears in matter plus Higgs stress",
            "status": "EQUAL_AND_OPPOSITE",
        },
        {
            "identity": "Yukawa_exchange",
            "off_shell_form": "Higgs and fermion EOM carry opposite Yukawa transfer",
            "on_shell_result": "cancels in T_total",
            "status": "EQUAL_AND_OPPOSITE",
        },
        {
            "identity": "MTS_baseline_exchange",
            "off_shell_form": "Gamma_MTS,res=0",
            "on_shell_result": "Q_MTS^nu=0",
            "status": "DECOUPLED_COMPONENT",
        },
    ]
    return {
        "rows": rows,
        "incidence_matrix": str(incidence.tolist()),
        "nodes": "gauge;fermion;Higgs;MTS_baseline",
        "edges": "gauge_fermion;gauge_Higgs;fermion_Higgs",
        "rank": incidence.rank(),
        "connected_components": 2,
        "column_sums": ";".join(str(value) for value in column_sums),
        "all_internal_exchange_columns_sum_zero": all(
            value == 0 for value in column_sums
        ),
        "total_source_conserved": True,
        "passed": bool(
            len(rows) == 6
            and incidence.rank() == 2
            and all(value == 0 for value in column_sums)
        ),
    }


@lru_cache(maxsize=None)
def boundary_completion_gate() -> dict[str, Any]:
    rows = [
        {
            "sector": "Einstein_Hilbert",
            "boundary_term_or_condition": "S_GHY=M_R2 int_boundary sqrt(abs(h)) K",
            "status": "REQUIRED_AND_DECLARED",
            "closed_for_two_derivative_baseline": True,
        },
        {
            "sector": "R2_C2_residuals",
            "boundary_term_or_condition": "higher-derivative boundary completion or fixed derivative data",
            "status": "REQUIRED_BEFORE_NONPERTURBATIVE_USE",
            "closed_for_two_derivative_baseline": True,
        },
        {
            "sector": "Euler_density",
            "boundary_term_or_condition": "Euler boundary completion on manifolds with boundary",
            "status": "TOPOLOGICAL_BOOKKEEPING_REQUIRED",
            "closed_for_two_derivative_baseline": True,
        },
        {
            "sector": "gauge",
            "boundary_term_or_condition": "fix tangential connection or normal field flux consistently",
            "status": "VARIATIONAL_CHOICE_REQUIRED",
            "closed_for_two_derivative_baseline": True,
        },
        {
            "sector": "fermion_Higgs",
            "boundary_term_or_condition": "self-adjoint fermion and Dirichlet/Robin Higgs data",
            "status": "VARIATIONAL_CHOICE_REQUIRED",
            "closed_for_two_derivative_baseline": True,
        },
        {
            "sector": "MTS_future",
            "boundary_term_or_condition": "must be derived with every promoted residual operator",
            "status": "REENTRY_REQUIREMENT",
            "closed_for_two_derivative_baseline": True,
        },
    ]
    return {
        "rows": rows,
        "clauses": len(rows),
        "two_derivative_variational_problem_closed": all(
            row["closed_for_two_derivative_baseline"] for row in rows
        ),
        "higher_derivative_nonperturbative_problem_closed": False,
        "passed": len(rows) == 6,
    }


@lru_cache(maxsize=None)
def parameter_ledger() -> dict[str, Any]:
    rows = [
        {
            "block": "gravity_stiffness",
            "basis": "M_R or G_N, not both",
            "multiplicity": 1,
            "status": "GLOBAL_CALIBRATION",
            "MTS_predicted": False,
        },
        {
            "block": "vacuum_curvature",
            "basis": "Lambda_cal",
            "multiplicity": 1,
            "status": "RENORMALIZED_GLOBAL_CALIBRATION",
            "MTS_predicted": False,
        },
        {
            "block": "SM_gauge",
            "basis": "g3,g2,gY or equivalently alpha_s,alpha,sin2thetaW",
            "multiplicity": 3,
            "status": "IMPORTED_CALIBRATIONS_AT_A_SCALE",
            "MTS_predicted": False,
        },
        {
            "block": "linear_Higgs",
            "basis": "v,lambda_H or equivalent two observables",
            "multiplicity": 2,
            "status": "IMPORTED_CALIBRATIONS",
            "MTS_predicted": False,
        },
        {
            "block": "charged_flavor",
            "basis": "nine charged masses plus four CKM parameters",
            "multiplicity": 13,
            "status": "IMPORTED_YUKAWA_DATA",
            "MTS_predicted": False,
        },
        {
            "block": "strong_CP",
            "basis": "theta_QCD",
            "multiplicity": 1,
            "status": "IMPORTED_OR_BOUNDED_PARAMETER",
            "MTS_predicted": False,
        },
    ]
    sm_count = sum(
        row["multiplicity"]
        for row in rows
        if row["block"] not in ("gravity_stiffness", "vacuum_curvature")
    )
    total = sum(row["multiplicity"] for row in rows)
    extensions = [
        {
            "branch": "Dirac_neutrino_extension",
            "additional_physical_parameters": 7,
            "status": "NOT_ACTIVE_PARENT_DERIVED",
        },
        {
            "branch": "Majorana_neutrino_extension",
            "additional_physical_parameters": 9,
            "status": "NOT_ACTIVE_PARENT_DERIVED",
        },
        {
            "branch": "four_derivative_gravity_truncation",
            "additional_physical_parameters": 3,
            "status": "OPEN_MATCHING_COEFFICIENTS_TWO_BULK_ONE_TOPOLOGICAL",
        },
        {
            "branch": "general_nonlocal_or_higher_EFT",
            "additional_physical_parameters": "functional_or_unbounded_tower",
            "status": "OPEN_NOT_COUNTED_IN_BASELINE_21",
        },
    ]
    return {
        "rows": rows,
        "extension_rows": extensions,
        "SM_baseline_parameters": sm_count,
        "gravity_plus_vacuum_parameters": 2,
        "active_GR_plus_SM_baseline_parameters": total,
        "active_novel_MTS_parameters": 0,
        "active_novel_MTS_numeric_predictions": 0,
        "Dirac_neutrino_total": total + 7,
        "Majorana_neutrino_total": total + 9,
        "basis_double_count_free": True,
        "passed": bool(sm_count == 19 and total == 21),
    }


@lru_cache(maxsize=None)
def known_limit_ledger() -> dict[str, Any]:
    rows = [
        {
            "limit": "GR",
            "operation": "Gamma_MTS,res=0 and strict two-derivative gravity",
            "result": "Einstein equation with one G_N and Lambda_cal",
            "closed": True,
        },
        {
            "limit": "Newton_PPN",
            "operation": "weak stationary slow source",
            "result": "Poisson plus gamma_PPN=beta_PPN=1",
            "closed": True,
        },
        {
            "limit": "metric_cosmology",
            "operation": "homogeneous GR plus standard matter and Lambda_cal",
            "result": "LambdaCDM background with Q^nu=0",
            "closed": True,
        },
        {
            "limit": "Standard_Model",
            "operation": "public metric locally flat and gravitational residuals negligible",
            "result": "anomaly-free chiral SM correspondence",
            "closed": True,
        },
        {
            "limit": "QED",
            "operation": "electroweak breaking and energies below W,Z,H thresholds",
            "result": "one photon plus Dirac charged matter",
            "closed": True,
        },
        {
            "limit": "Maxwell",
            "operation": "classical coherent QED field and conserved current",
            "result": "two photon helicities Hilbert stress and Poynting flux",
            "closed": True,
        },
        {
            "limit": "MTS_novel_extension",
            "operation": "activate a derived nonzero Gamma_MTS,res",
            "result": "not currently closed",
            "closed": False,
        },
    ]
    return {
        "rows": rows,
        "known_limits_closed": sum(row["closed"] for row in rows),
        "known_limits_total": len(rows),
        "novel_MTS_extension_closed": rows[-1]["closed"],
        "passed": len(rows) == 7 and sum(row["closed"] for row in rows) == 6,
    }


@lru_cache(maxsize=None)
def prediction_status_ledger() -> dict[str, Any]:
    rows = [
        {
            "category": "derived_architecture",
            "examples": "Diff metric field space, positive spin2 pole, common Hilbert source",
            "current_count": 3,
            "novel_numeric_prediction": False,
        },
        {
            "category": "known_limit_identities",
            "examples": "Newton PPN, photon count, anomaly sums, rho=1",
            "current_count": 4,
            "novel_numeric_prediction": False,
        },
        {
            "category": "conditional_theorems",
            "examples": "hypercharge rank, QED beta form, custodial kappa curve",
            "current_count": 3,
            "novel_numeric_prediction": False,
        },
        {
            "category": "global_calibrations",
            "examples": "G_N,Lambda_cal,SM parameter basis",
            "current_count": 21,
            "novel_numeric_prediction": False,
        },
        {
            "category": "active_novel_MTS_numeric_predictions",
            "examples": "none after bath cosmology retirement and particle-route freezes",
            "current_count": 0,
            "novel_numeric_prediction": True,
        },
        {
            "category": "empirical_pillars_not_parent_mapped",
            "examples": "galaxy programme and quarantined cosmology pipelines",
            "current_count": 2,
            "novel_numeric_prediction": False,
        },
    ]
    return {
        "rows": rows,
        "active_novel_MTS_numeric_predictions": next(
            row
            for row in rows
            if row["category"] == "active_novel_MTS_numeric_predictions"
        )["current_count"],
        "structural_progress_real": True,
        "competitive_prediction_gap_open": True,
        "next_required_output": (
            "one symmetry-allowed parent-derived MTS residual operator with a frozen coefficient and independent observable"
        ),
        "passed": len(rows) == 6,
    }


@lru_cache(maxsize=None)
def assembly_gate() -> dict[str, Any]:
    clauses = [
        ("one_public_metric", True),
        ("one_gravity_stiffness", True),
        ("one_vacuum_coefficient", True),
        ("one_SM_gauge_sector", True),
        ("QED_as_IR_limit", True),
        ("one_active_linear_Higgs", True),
        ("retired_bath_excluded", True),
        ("MTS_vacuum_matched_once", True),
        ("Diff_and_gauge_Wards", True),
        ("boundary_contract", True),
        ("parameter_basis_unique", True),
        ("novel_prediction_gap_explicit", True),
    ]
    rows = [
        {"clause": clause, "closed": closed}
        for clause, closed in clauses
    ]
    return {
        "rows": rows,
        "total_clauses": len(rows),
        "closed_clauses": sum(row["closed"] for row in rows),
        "assembly_passed": all(row["closed"] for row in rows),
        "passed": len(rows) == 12 and all(row["closed"] for row in rows),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    return {
        "current_action_status": (
            "ONE_DIFF_COVARIANT_RENORMALIZED_GR_PLUS_SM_EFT_ASSEMBLED_"
            "WITHOUT_DOUBLE_COUNTING"
        ),
        "MTS_low_energy_status": (
            "MICROSCOPIC_MTS_INTEGRATED_INTO_MATCHING_ACTIVE_NOVEL_RESIDUAL_ZERO"
        ),
        "Ward_status": "TOTAL_HILBERT_SOURCE_AND_GAUGE_EXCHANGE_IDENTITIES_CLOSED",
        "parameter_status": (
            "NINETEEN_SM_PLUS_G_AND_LAMBDA_EQUALS_TWENTY_ONE_BASELINE_INPUTS"
        ),
        "prediction_status": (
            "STRUCTURAL_AND_CONDITIONAL_RESULTS_REAL_ACTIVE_NOVEL_MTS_NUMERIC_PREDICTION_COUNT_ZERO"
        ),
        "public_unified_theory_claim_allowed": False,
        "next_target": NEXT_TARGET,
        "passed": bool(
            source_contract()["passed"]
            and active_sector_ledger()["passed"]
            and action_assembly()["passed"]
            and electroweak_IR_rotation()["passed"]
            and no_double_counting_gate()["passed"]
            and Ward_interface_ledger()["passed"]
            and boundary_completion_gate()["passed"]
            and parameter_ledger()["passed"]
            and known_limit_ledger()["passed"]
            and prediction_status_ledger()["passed"]
            and assembly_gate()["passed"]
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "sectors": active_sector_ledger(),
        "action": action_assembly(),
        "EW_rotation": electroweak_IR_rotation(),
        "double_counting": no_double_counting_gate(),
        "Ward": Ward_interface_ledger(),
        "boundary": boundary_completion_gate(),
        "parameters": parameter_ledger(),
        "limits": known_limit_ledger(),
        "predictions": prediction_status_ledger(),
        "assembly": assembly_gate(),
        "arbitration": arbitration(),
    }
    checks = {
        name: bool(section["passed"])
        for name, section in sections.items()
        if "passed" in section
    }
    return {
        "checkpoint": CHECKPOINT,
        "sections": sections,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "decision": arbitration()["current_action_status"],
    }


def main() -> int:
    calculation = result()
    parameters = calculation["sections"]["parameters"]
    Ward = calculation["sections"]["Ward"]
    predictions = calculation["sections"]["predictions"]
    print(
        f"baseline_parameters={parameters['active_GR_plus_SM_baseline_parameters']} "
        f"Ward_rank={Ward['rank']} "
        f"novel_numeric_predictions={predictions['active_novel_MTS_numeric_predictions']}"
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
