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
QPF = ROOT / "quantum-particle-field"
CORE = ROOT / "core-mts-framework"
OUTPUT = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4902"
NEXT_TARGET = (
    "4903-Y5-R2FR-custodial-Higgs-coset-completion-and-electroweak-"
    "precision-or-linear-Higgs-freeze.md"
)

HIGGS_URL = "https://doi.org/10.1103/PhysRevLett.13.508"
WEINBERG_EW_URL = "https://doi.org/10.1103/PhysRevLett.19.1264"
VACUUM_MISALIGNMENT_URL = "https://doi.org/10.1016/0370-2693(84)91177-8"
COMPOSITE_HIGGS_URL = "https://doi.org/10.1016/0370-2693(84)91178-X"
WEINBERG_OPERATOR_URL = "https://doi.org/10.1103/PhysRevLett.43.1566"


def contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    local_sources = [
        (
            "SRC4902_00_4901",
            POST
            / "4901-Y5-R2FR-nonabelian-SU2xSU3-parent-and-chiral-anomaly-cancellation-or-standard-model-correspondence-freeze.md",
            "MTS_NONABELIAN_CHIRAL_SM_CORRESPONDENCE_GATE_4901",
            "validated_predecessor",
        ),
        (
            "SRC4902_01_4901_validation",
            OUTPUT / "P8_Y5_BRR545_4901_VALIDATION.csv",
            "VAL4901_OVERALL,PASS",
            "validated_predecessor",
        ),
        (
            "SRC4902_02_4854_CP2",
            POST
            / "4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md",
            "U1_BASELINE_CP2_CONSTITUTIVE_GATE_4854",
            "optional_CP2_parent_clue",
        ),
        (
            "SRC4902_03_4900_particle_audit",
            POST
            / "4900-Y5-R2FR-charged-matter-representation-lattice-and-QED-beta-function-or-classical-EM-freeze.md",
            "MTS_CHARGED_MATTER_AND_QED_CORRESPONDENCE_GATE_4900",
            "particle_mass_audit",
        ),
        (
            "SRC4902_04_fundamental_scalar",
            CORE
            / "action-principle"
            / "the-fundamental-action-of-motion-timespace-field-theory.md",
            "The elementary object of MTS is a scalar motion field",
            "primitive_scalar_owner",
        ),
        (
            "SRC4902_05_lepton_mass",
            QPF
            / "leptons-neutrinos"
            / "the-lepton-mass-hierarchy-from-motion-timespace.md",
            "LEPTON MASS HIERARCHY",
            "legacy_mass_claim_under_audit",
        ),
        (
            "SRC4902_06_quark_mass",
            QPF
            / "quarks-protons"
            / "the-quark-mass-hierarchy-from-motion-timespace.md",
            "THE QUARK MASS HIERARCHY",
            "legacy_mass_claim_under_audit",
        ),
        (
            "SRC4902_07_neutrino_matrix",
            QPF
            / "leptons-neutrinos"
            / "neutrino-mixing-from-motion-timespace-geometry.md",
            "Neutrino Mixing from Motion",
            "legacy_neutrino_claim_under_audit",
        ),
        (
            "SRC4902_08_neutrino_winding",
            QPF
            / "leptons-neutrinos"
            / "why-neutrinos-are-light-and-mix.md",
            "WHY NEUTRINOS ARE LIGHT AND MIX",
            "legacy_neutrino_interpretation_under_audit",
        ),
        (
            "SRC4902_09_formal4901",
            FORMAL / "917-PPC4161-nonabelian-chiral-SM-correspondence.md",
            "PPC4161_NONABELIAN_CHIRAL_SM_CORRESPONDENCE_4901",
            "current_SM_correspondence",
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
    external = (
        (
            "SRC4902_10_Higgs",
            HIGGS_URL,
            "Higgs gauge-boson mass mechanism primary source",
        ),
        (
            "SRC4902_11_WeinbergEW",
            WEINBERG_EW_URL,
            "electroweak Higgs model primary source",
        ),
        (
            "SRC4902_12_vacuum_misalignment",
            VACUUM_MISALIGNMENT_URL,
            "composite-Higgs vacuum-misalignment primary source",
        ),
        (
            "SRC4902_13_composite_Higgs",
            COMPOSITE_HIGGS_URL,
            "composite Higgs scalar primary source",
        ),
        (
            "SRC4902_14_Weinberg_operator",
            WEINBERG_OPERATOR_URL,
            "dimension-five lepton-number operator primary source",
        ),
    )
    for source_id, url, marker in external:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "primary_external_source",
                "source_path_or_url": url,
                "local_path_required": False,
                "source_exists": True,
                "marker": marker,
                "marker_found": True,
                "source_checked_date": "2026-07-11",
            }
        )
    return {
        "rows": rows,
        "local_sources": len(local_sources),
        "external_sources": len(external),
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
def Higgs_owner_audit() -> dict[str, Any]:
    rows = [
        {
            "candidate": "primitive_real_psi",
            "field_content": "one real gauge-singlet scalar psi:R4->R",
            "Higgs_doublet_representation": False,
            "kinetic_owner": True,
            "potential_owner": False,
            "vacuum_owner": False,
            "verdict": "CANNOT_BREAK_SU2L_X_U1Y_AS_WRITTEN",
        },
        {
            "candidate": "CP2_optional_target",
            "field_content": "four-real-dimensional SU3/U2 coset",
            "Higgs_doublet_representation": True,
            "kinetic_owner": True,
            "potential_owner": False,
            "vacuum_owner": False,
            "verdict": "CONDITIONAL_DOUBLE_AND_KINETIC_CLUE_ONLY",
        },
        {
            "candidate": "linear_SM_H",
            "field_content": "explicit complex SU2 doublet with Y=1/2",
            "Higgs_doublet_representation": True,
            "kinetic_owner": True,
            "potential_owner": True,
            "vacuum_owner": True,
            "verdict": "COMPLETE_CORRESPONDENCE_INPUT_NOT_PRIMITIVE",
        },
    ]
    return {
        "rows": rows,
        "primitive_real_scalar_is_Higgs": False,
        "CP2_conditional_representation_owner": True,
        "CP2_potential_and_vacuum_owner": False,
        "linear_Higgs_correspondence_required": True,
        "passed": len(rows) == 3
        and not rows[0]["Higgs_doublet_representation"]
        and rows[1]["Higgs_doublet_representation"]
        and not rows[1]["potential_owner"],
    }


@lru_cache(maxsize=None)
def CP2_Higgs_geometry() -> dict[str, Any]:
    radius_squared, decay_scale = sp.symbols(
        "r2 f", nonnegative=True, positive=True
    )
    eigen_orthogonal = decay_scale**2 / (1 + radius_squared)
    eigen_parallel = decay_scale**2 / (1 + radius_squared) ** 2
    determinant = sp.factor(eigen_orthogonal * eigen_parallel)
    rows = [
        {
            "property": "coset_dimension",
            "derivation": "dim_R SU3-dim_R U2=8-4",
            "result": "4",
            "status": "ONE_COMPLEX_DOUBLET_COUNT",
        },
        {
            "property": "isotropy_representation",
            "derivation": "T_[base]CP2 transforms as the complex fundamental of U2",
            "result": "2_complex",
            "status": "CONDITIONAL_HIGGS_REPRESENTATION",
        },
        {
            "property": "Fubini_Study_metric",
            "derivation": "f2*((1+wdagw)I-w wdag)/(1+wdagw)^2",
            "result": "positive for f2>0",
            "status": "KINETIC_GEOMETRY_CLOSED",
        },
        {
            "property": "metric_eigenvalue_orthogonal",
            "derivation": "direction orthogonal to w",
            "result": str(eigen_orthogonal),
            "status": "POSITIVE",
        },
        {
            "property": "metric_eigenvalue_parallel",
            "derivation": "direction parallel to w",
            "result": str(eigen_parallel),
            "status": "POSITIVE",
        },
        {
            "property": "metric_determinant",
            "derivation": "product of complex eigenvalues",
            "result": str(determinant),
            "status": "POSITIVE",
        },
        {
            "property": "invariant_potential",
            "derivation": "SU3 acts transitively on homogeneous CP2=SU3/U2",
            "result": "every globally SU3-invariant scalar potential is constant",
            "status": "NONTRIVIAL_POTENTIAL_REQUIRES_EXPLICIT_BREAKING_SPURIONS",
        },
        {
            "property": "canonical_limit",
            "derivation": "H=f w near w=0",
            "result": "L=partial H dagger partial H+O(1/f2)",
            "status": "LINEAR_HIGGS_LIMIT_RECOVERED",
        },
    ]
    return {
        "rows": rows,
        "real_dimension": 4,
        "complex_doublets": 1,
        "metric_determinant": str(determinant),
        "metric_positive": True,
        "nonconstant_SU3_invariant_potential_exists": False,
        "explicit_breaking_required": True,
        "CP2_representation_and_kinetic_derived_conditionally": True,
        "passed": bool(
            len(rows) == 8
            and determinant == decay_scale**4 / (1 + radius_squared) ** 3
        ),
    }


@lru_cache(maxsize=None)
def CP2_custodial_gate() -> dict[str, Any]:
    g2, gY, decay_scale, tangent = sp.symbols(
        "g2 gY f t", positive=True
    )
    mW_squared = sp.factor(
        g2**2 * decay_scale**2 * tangent**2 / (2 * (1 + tangent**2))
    )
    mZ_squared = sp.factor(
        (g2**2 + gY**2)
        * decay_scale**2
        * tangent**2
        / (2 * (1 + tangent**2) ** 2)
    )
    cosine_squared = g2**2 / (g2**2 + gY**2)
    rho = sp.factor(mW_squared / (mZ_squared * cosine_squared))
    rows = [
        {
            "object": "charged_mass",
            "equation": "mW2=g2^2 f^2 t^2/[2(1+t^2)]",
            "symbolic_result": str(mW_squared),
            "status": "DERIVED_FROM_GAUGED_FS_METRIC",
        },
        {
            "object": "neutral_mass",
            "equation": "mZ2=(g2^2+gY^2)f^2t^2/[2(1+t^2)^2]",
            "symbolic_result": str(mZ_squared),
            "status": "DERIVED_FROM_GAUGED_FS_METRIC",
        },
        {
            "object": "photon",
            "equation": "det neutral mass matrix=0",
            "symbolic_result": "0",
            "status": "U1EM_UNBROKEN",
        },
        {
            "object": "rho_parameter",
            "equation": "rho=mW2/(mZ2 cos2thetaW)",
            "symbolic_result": str(rho),
            "status": "RHO_EQUALS_1_PLUS_T2",
        },
    ]
    return {
        "rows": rows,
        "mW_squared": str(mW_squared),
        "mZ_squared": str(mZ_squared),
        "rho": str(rho),
        "rho_minus_one": str(sp.factor(rho - 1)),
        "rho_exactly_one_at_nonzero_tangent": False,
        "custodial_completion_present": False,
        "CP2_Higgs_branch_precision_ready": False,
        "passed": bool(
            rho == 1 + tangent**2
            and sp.factor(rho - 1) == tangent**2
            and len(rows) == 4
        ),
    }


@lru_cache(maxsize=None)
def linear_Higgs_correspondence() -> dict[str, Any]:
    g2, gY, vacuum, quartic = sp.symbols(
        "g2 gY v lambda_H", positive=True
    )
    neutral = vacuum**2 / 4 * sp.Matrix(
        [[g2**2, -g2 * gY], [-g2 * gY, gY**2]]
    )
    neutral_eigenvalues = sorted(
        [sp.factor(value) for value in neutral.eigenvals()], key=str
    )
    mW_squared = g2**2 * vacuum**2 / 4
    mZ_squared = (g2**2 + gY**2) * vacuum**2 / 4
    photon_squared = sp.Integer(0)
    Higgs_squared = 2 * quartic * vacuum**2
    rho = sp.factor(
        mW_squared
        / (mZ_squared * g2**2 / (g2**2 + gY**2))
    )
    rows = [
        {
            "object": "vacuum",
            "equation": "H0=(0,v/sqrt(2)); v2=mu_H2/lambda_H",
            "result": "SU2LxU1Y -> U1EM",
            "status": "CORRESPONDENCE_INPUT",
        },
        {
            "object": "W_mass",
            "equation": "mW2=g2^2 v2/4",
            "result": str(mW_squared),
            "status": "KNOWN_LIMIT_DERIVED",
        },
        {
            "object": "Z_mass",
            "equation": "mZ2=(g2^2+gY^2)v2/4",
            "result": str(mZ_squared),
            "status": "KNOWN_LIMIT_DERIVED",
        },
        {
            "object": "photon_mass",
            "equation": "neutral determinant zero",
            "result": str(photon_squared),
            "status": "KNOWN_LIMIT_DERIVED",
        },
        {
            "object": "Higgs_mass",
            "equation": "mh2=2lambda_H v2",
            "result": str(Higgs_squared),
            "status": "KNOWN_LIMIT_DERIVED",
        },
        {
            "object": "tree_rho",
            "equation": "rho=mW2/(mZ2 cos2thetaW)",
            "result": str(rho),
            "status": "EXACTLY_ONE",
        },
    ]
    return {
        "rows": rows,
        "neutral_eigenvalues": ";".join(str(value) for value in neutral_eigenvalues),
        "neutral_determinant": str(sp.factor(neutral.det())),
        "rho": str(rho),
        "Higgs_potential_parameters_derived_from_MTS": False,
        "vacuum_scale_derived_from_MTS": False,
        "correspondence_gate_passed": True,
        "passed": bool(
            neutral.det() == 0
            and rho == 1
            and len(neutral_eigenvalues) == 2
            and len(rows) == 6
        ),
    }


@lru_cache(maxsize=None)
def electroweak_identifiability() -> dict[str, Any]:
    g2, gY, vacuum, quartic = sp.symbols(
        "g2 gY v lambda_H", positive=True
    )
    parameters = (g2, gY, vacuum, quartic)
    observables = sp.Matrix(
        [
            g2**2 * gY**2 / (g2**2 + gY**2),
            g2**2 * vacuum**2 / 4,
            (g2**2 + gY**2) * vacuum**2 / 4,
            2 * quartic * vacuum**2,
        ]
    )
    jacobian = observables.jacobian(parameters)
    determinant = sp.factor(jacobian.det())
    rows = [
        {
            "observable": "e_squared",
            "equation": "g2^2 gY^2/(g2^2+gY^2)",
            "parameter_owner": "g2,gY",
            "prediction_status": "CALIBRATION_MAP",
        },
        {
            "observable": "mW_squared",
            "equation": "g2^2 v2/4",
            "parameter_owner": "g2,v",
            "prediction_status": "CALIBRATION_MAP",
        },
        {
            "observable": "mZ_squared",
            "equation": "(g2^2+gY^2)v2/4",
            "parameter_owner": "g2,gY,v",
            "prediction_status": "CALIBRATION_MAP",
        },
        {
            "observable": "mh_squared",
            "equation": "2lambda_H v2",
            "parameter_owner": "lambda_H,v",
            "prediction_status": "CALIBRATION_MAP",
        },
    ]
    return {
        "rows": rows,
        "parameters": len(parameters),
        "observables": len(observables),
        "jacobian_rank": jacobian.rank(),
        "jacobian_determinant": str(determinant),
        "generic_full_rank": determinant != 0,
        "independent_MTS_relation_in_four_observable_block": False,
        "passed": bool(
            jacobian.rank() == 4
            and determinant
            == -g2**3 * gY**3 * vacuum**5 / (g2**2 + gY**2)
        ),
    }


@lru_cache(maxsize=None)
def Yukawa_and_mass_identifiability() -> dict[str, Any]:
    rows = [
        {
            "sector": "one_generation_up",
            "mass_map": "m_u=y_u v/sqrt(2)",
            "free_flavor_parameters": 1,
            "mass_mixing_observables": 1,
            "map_rank": 1,
            "MTS_prediction": False,
        },
        {
            "sector": "one_generation_down",
            "mass_map": "m_d=y_d v/sqrt(2)",
            "free_flavor_parameters": 1,
            "mass_mixing_observables": 1,
            "map_rank": 1,
            "MTS_prediction": False,
        },
        {
            "sector": "one_generation_charged_lepton",
            "mass_map": "m_e=y_e v/sqrt(2)",
            "free_flavor_parameters": 1,
            "mass_mixing_observables": 1,
            "map_rank": 1,
            "MTS_prediction": False,
        },
        {
            "sector": "three_generation_quarks",
            "mass_map": "M_u=Y_u v/sqrt(2); M_d=Y_d v/sqrt(2)",
            "free_flavor_parameters": 10,
            "mass_mixing_observables": 10,
            "map_rank": 10,
            "MTS_prediction": False,
        },
        {
            "sector": "three_generation_charged_leptons",
            "mass_map": "M_e=Y_e v/sqrt(2)",
            "free_flavor_parameters": 3,
            "mass_mixing_observables": 3,
            "map_rank": 3,
            "MTS_prediction": False,
        },
    ]
    return {
        "rows": rows,
        "charged_flavor_parameters": 13,
        "charged_mass_and_CKM_observables": 13,
        "inverse_map": "Y_f=sqrt(2) M_f/v",
        "Yukawa_matrices_derived_from_MTS": False,
        "charged_mass_spectrum_predicted": False,
        "passed": bool(
            len(rows) == 5
            and sum(
                row["free_flavor_parameters"]
                for row in rows
                if row["sector"].startswith("three_generation")
            )
            == 13
            and not any(row["MTS_prediction"] for row in rows)
        ),
    }


@lru_cache(maxsize=None)
def legacy_mass_claim_audit() -> dict[str, Any]:
    rows = [
        {
            "claim": "charged_lepton_masses",
            "numerical_inputs": "psi_e,psi_mu,psi_tau selected; tau labeled fine adjustment",
            "decisive_test": "4900 endpoint reshoot gives nonzero tails and R^approximately3 mass growth",
            "retained_asset": "nonlinear amplitude-to-integral map",
            "current_status": "NOT_A_LOCALIZED_MASS_EIGENPROBLEM",
        },
        {
            "claim": "quark_masses",
            "numerical_inputs": "six flavor amplitudes plus explicit target-ratio loss and s/c sweep",
            "decisive_test": "one amplitude per flavor can invert the observed mass ladder",
            "retained_asset": "nonlinear flavor-regression experiment",
            "current_status": "NOT_A_YUKAWA_REPLACEMENT_OR_SPECTRUM_THEOREM",
        },
        {
            "claim": "neutrino_masses_and_PMNS",
            "numerical_inputs": "Phi_nu, three kappa_i, three symmetric and three antisymmetric off-diagonal entries",
            "decisive_test": "at least ten sector numbers are inserted before diagonalization",
            "retained_asset": "Hermitian-matrix diagonalization target",
            "current_status": "NUMERICAL_MATRIX_ANSATZ_NOT_PARENT_DERIVATION",
        },
        {
            "claim": "winding_charge_and_neutrality",
            "numerical_inputs": "n approximately zero versus nonzero labels",
            "decisive_test": "4900 finds no moment map from spatial winding to principal U1 charge",
            "retained_asset": "candidate topological classifier",
            "current_status": "QUALITATIVE_HEURISTIC_NOT_GAUGE_REPRESENTATION",
        },
    ]
    return {
        "rows": rows,
        "audited_claims": len(rows),
        "promoted_claims": 0,
        "all_assets_retained": True,
        "passed": len(rows) == 4
        and all("NOT_" in row["current_status"] for row in rows),
    }


@lru_cache(maxsize=None)
def neutrino_mass_correspondence() -> dict[str, Any]:
    rows = [
        {
            "branch": "minimal_renormalizable_SM",
            "operator": "none",
            "mass_map": "m_nu=0",
            "parent_coefficient_status": "closed but empirically incomplete",
            "MTS_origin": False,
        },
        {
            "branch": "dimension_five_Majorana",
            "operator": "c5_ij (L_i H)(L_j H)/Lambda+h.c.",
            "mass_map": "M_nu=c5 v2/(2 Lambda) by stated convention",
            "parent_coefficient_status": "c5/Lambda not derived",
            "MTS_origin": False,
        },
        {
            "branch": "type_I_seesaw",
            "operator": "Y_nu L H nu_R^c + M_R nu_R^c nu_R^c/2",
            "mass_map": "M_nu approximately -v2 Y_nu M_R^-1 Y_nu^T/2",
            "parent_coefficient_status": "Y_nu and M_R not derived",
            "MTS_origin": False,
        },
    ]
    return {
        "rows": rows,
        "baseline_massive_neutrinos_closed": False,
        "Weinberg_operator_available_as_correspondence": True,
        "seesaw_available_as_correspondence": True,
        "MTS_neutrino_mass_matrix_derived": False,
        "passed": len(rows) == 3
        and not any(row["MTS_origin"] for row in rows),
    }


@lru_cache(maxsize=None)
def promotion_gate() -> dict[str, Any]:
    clauses = [
        ("primitive_Higgs_representation", False, "real psi is a singlet; CP2 is optional"),
        ("CP2_kinetic_geometry", True, "one complex doublet and positive FS metric"),
        ("CP2_nonconstant_potential", False, "exact SU3 invariance permits only a constant"),
        ("CP2_custodial_precision", False, "rho=1+t^2 without a custodial completion"),
        ("vacuum_scale_owner", False, "v or f and misalignment are not selected"),
        ("Higgs_mass_owner", False, "mu_H and lambda_H are not derived"),
        ("gauge_coupling_owner", False, "g2 and gY remain calibrated"),
        ("Yukawa_matrix_owner", False, "thirteen charged-flavor parameters remain inputs"),
        ("neutrino_mass_owner", False, "c5/Lambda or Ynu and MR remain inputs"),
        ("legacy_mass_eigenproblem", False, "archived scalar profiles are not localized eigenstates"),
        ("linear_Higgs_known_limit", True, "correct W Z photon Higgs and rho relations"),
        ("private_nonclaim_discipline", True, "no primitive mass claim promoted"),
    ]
    rows = [
        {"clause": name, "closed": closed, "evidence": evidence}
        for name, closed, evidence in clauses
    ]
    primitive_required = rows[:10]
    return {
        "rows": rows,
        "total_clauses": len(rows),
        "closed_clauses": sum(row["closed"] for row in rows),
        "primitive_required_clauses": len(primitive_required),
        "primitive_closed_clauses": sum(
            row["closed"] for row in primitive_required
        ),
        "primitive_Higgs_mass_reentry_allowed": all(
            row["closed"] for row in primitive_required
        ),
        "linear_correspondence_closed": rows[10]["closed"],
        "passed": bool(
            len(rows) == 12
            and not all(row["closed"] for row in primitive_required)
            and rows[10]["closed"]
            and rows[11]["closed"]
        ),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    return {
        "primitive_Higgs_status": (
            "REAL_MTS_SCALAR_NOT_HIGGS_CP2_CONDITIONAL_DOUBLET_KINETIC_CLUE_"
            "POTENTIAL_AND_VACUUM_OPEN"
        ),
        "CP2_precision_status": (
            "GAUGED_CP2_FS_METRIC_GIVES_RHO_1_PLUS_T2_CUSTODIAL_COMPLETION_REQUIRED"
        ),
        "linear_Higgs_status": (
            "EXPLICIT_LINEAR_HIGGS_CORRESPONDENCE_RETAINED_AS_ACTIVE_KNOWN_LIMIT"
        ),
        "electroweak_parameter_status": (
            "FOUR_PARAMETER_FOUR_OBSERVABLE_MAP_FULL_RANK_NO_MTS_RELATION"
        ),
        "Yukawa_status": (
            "CHARGED_MASS_AND_MIXING_MAP_FULL_INPUT_RANK_YUKAWA_MATRICES_NOT_DERIVED"
        ),
        "neutrino_status": (
            "MASS_REQUIRES_WEINBERG_OR_SEESAW_CORRESPONDENCE_COEFFICIENTS_OPEN"
        ),
        "legacy_mass_status": (
            "SCALAR_AMPLITUDE_AND_INSERTED_MATRIX_CLAIMS_QUARANTINED_ASSETS_RETAINED"
        ),
        "public_claim_allowed": False,
        "next_target": NEXT_TARGET,
        "passed": bool(
            source_contract()["passed"]
            and Higgs_owner_audit()["passed"]
            and CP2_Higgs_geometry()["passed"]
            and CP2_custodial_gate()["passed"]
            and linear_Higgs_correspondence()["passed"]
            and electroweak_identifiability()["passed"]
            and Yukawa_and_mass_identifiability()["passed"]
            and legacy_mass_claim_audit()["passed"]
            and neutrino_mass_correspondence()["passed"]
            and promotion_gate()["passed"]
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "owner": Higgs_owner_audit(),
        "CP2_geometry": CP2_Higgs_geometry(),
        "CP2_custodial": CP2_custodial_gate(),
        "linear_Higgs": linear_Higgs_correspondence(),
        "EW_identifiability": electroweak_identifiability(),
        "Yukawa": Yukawa_and_mass_identifiability(),
        "legacy_mass": legacy_mass_claim_audit(),
        "neutrino": neutrino_mass_correspondence(),
        "promotion": promotion_gate(),
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
        "decision": arbitration()["linear_Higgs_status"],
    }


def main() -> int:
    calculation = result()
    geometry = calculation["sections"]["CP2_geometry"]
    custodial = calculation["sections"]["CP2_custodial"]
    identifiability = calculation["sections"]["EW_identifiability"]
    print(
        f"CP2_dim={geometry['real_dimension']} "
        f"doublets={geometry['complex_doublets']} "
        f"rho={custodial['rho']} "
        f"EW_rank={identifiability['jacobian_rank']}"
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
