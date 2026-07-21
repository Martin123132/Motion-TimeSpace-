from __future__ import annotations

import csv
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4960"

RESULT_JSON = SOURCE / "integrated_H_universal_source_results.json"
CONTRACT_CSV = SOURCE / "parent_definition_vs_derived_source_contract.csv"
H_SOURCE_CSV = SOURCE / "H_Hilbert_source_invertibility.csv"
UNIVERSALITY_CSV = SOURCE / "soft_Bianchi_species_coupling_nullspace.csv"
LOCAL_CHAIN_CSV = SOURCE / "local_limit_chain_and_calibrations.csv"
RESIDUAL_CSV = SOURCE / "local_residual_quarantine.csv"
DECISION_CSV = SOURCE / "universal_source_decision.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4960_INTEGRATED_H_UNIVERSAL_SOURCE_THEOREM"
CHECKED_DATE = "2026-07-13"

SOURCE_PATHS = {
    "soft_parent_4874": POST / "4874-Y5-R2FR-metric-only-quotient-background-independence-and-universal-principal-symbol-proof-or-equivalence-axiom-freeze.md",
    "integrated_parent_4875": POST / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
    "residue_4915": POST / "4915-Y5-R2FR-parent-EH-residue-universal-source-coupling-and-measured-G-calibration-or-closure-demotion.md",
    "covariantization_4916": POST / "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md",
    "higgs_bound_4920": POST / "4920-Y5-R2FR-graviton-mediated-curvature-Higgs-running-and-current-Higgs-coupling-bound-or-vacuum-local-GR-promotion-gate.md",
    "local_residual_4942": POST / "4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-branch-and-C3-CFF-PPN-residual-gate.md",
    "matter_source_4943": POST / "4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md",
    "maxwell_4946": POST / "4946-Y5-R2FR-QCD-TJJ-dispersive-matching-and-weak-local-Maxwell-action-certificate.md",
    "local_chain_4947": POST / "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md",
    "residue_chain_4947": POST / "source-intake" / "functional_rg" / "4947" / "source_residue_chain.csv",
    "limits_4947": POST / "source-intake" / "functional_rg" / "4947" / "Newton_geodesic_Lorentz_limit_gate.csv",
    "calibrations_4947": POST / "source-intake" / "functional_rg" / "4947" / "parent_low_energy_calibration_ledger.csv",
    "arenas_4947": POST / "source-intake" / "functional_rg" / "4947" / "cross_arena_no_retuning_matrix.csv",
    "matter_rules_4943": POST / "source-intake" / "functional_rg" / "4943" / "matter_source_selection_rules.csv",
    "fifth_force_4943": POST / "source-intake" / "functional_rg" / "4943" / "junction_scalar_charge_and_fifth_force.csv",
    "maxwell_certificate_4946": POST / "source-intake" / "functional_rg" / "4946" / "local_Maxwell_action_stress_and_calibration_certificate.csv",
    "local_residual_vector_4942": POST / "source-intake" / "functional_rg" / "4942" / "local_O4_C3_CFF_residual_vector.csv",
}

EXPECTED_HASHES = {
    "soft_parent_4874": "4eac48d7c90262bc0856d70eac8b25c0eed6b75bae1a11c16f5d1cdbf6ba81bb",
    "integrated_parent_4875": "83b20a1314e40e5fa9c30dcff5d47254f21cb47cfd8f2d1df4f14728f71fa484",
    "residue_4915": "3e0c0ac26e7541ce8b4e5fbfcb16549ce3361b970bc98860b5a3f4342ab57e9f",
    "covariantization_4916": "4c20db8f8f75d81bab3c2a6d334cbcefeb2f2c1d66266be0ec412947c705b636",
    "higgs_bound_4920": "9cb87e2761820c6a9d28828d90a13ff2cd2f5f6f77f9dec9e5cd28970e44ea44",
    "local_residual_4942": "64b96ca4e19a058ced85c0c4b800ae7a237408606799dd8c4a5b58935f635c5f",
    "matter_source_4943": "a90da0e9ad0457fc3dbdb389d7bf2715cb9d707cbffa094a987b0b0553e257b5",
    "maxwell_4946": "4985b31aa5d5253ec64fd1575bbd0f844c1b5c0924a11482fb77374ddee477b6",
    "local_chain_4947": "0b71f50c85ab4c5761755aa11544910a1a1e4fcacc901236432705a5ba36563f",
    "residue_chain_4947": "b08468f29f938dfe72f13b9eec93f73c2b4f9c58ff89e7b67008c6de2cfc1e1d",
    "limits_4947": "a412b326de7867064968a66caed955039b466e9e230acf5ee0b6952b6f5f006a",
    "calibrations_4947": "e68c78e9c4e1c05df056e441db9a06869b723bb5ca5c9fd06933965737766020",
    "arenas_4947": "8c060a129155d84ebc40412e50a2acc11ea5043a9825afd24e5486065c194cc7",
    "matter_rules_4943": "2e9308c2d88336aeeab957fe78ce3d3a1d912809fc9a20afc416031394fb7a1b",
    "fifth_force_4943": "5fbca2c1672d7fbb6f1741e56a3c72a2adbaee544a4fd5fd5525a616cb836df6",
    "maxwell_certificate_4946": "8b80ddf7b5cb469fa7c580b24f6b0d759322871bfb7064111839565ba290799a",
    "local_residual_vector_4942": "51f034326f02684491743d6b12fed9d54854885dae07e7894e77423f435a14a5",
}

PRIMARY_SOURCES = {
    "Weinberg_1964_soft_graviton": "https://doi.org/10.1103/PhysRev.135.B1049",
    "Weinberg_1965_Einstein_completion": "https://doi.org/10.1103/PhysRev.138.B988",
    "Deser_1970_self_coupling": "https://doi.org/10.1007/BF00759198",
    "Deser_author_source": "https://arxiv.org/abs/gr-qc/0411023",
    "Weinberg_Witten_1980": "https://doi.org/10.1016/0370-2693(80)90212-9",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def trace_reversal_matrix() -> tuple[sp.Matrix, list[tuple[int, int]]]:
    metric = sp.diag(-1, 1, 1, 1)
    inverse_metric = metric.inv()
    components = [(row, column) for row in range(4) for column in range(row, 4)]
    columns: list[sp.Matrix] = []
    for source_row, source_column in components:
        stress = sp.zeros(4)
        stress[source_row, source_column] = 1
        stress[source_column, source_row] = 1
        trace = sp.simplify(
            sum(
                inverse_metric[row, column] * stress[row, column]
                for row in range(4)
                for column in range(4)
            )
        )
        reversed_stress = stress - sp.Rational(1, 2) * metric * trace
        columns.append(
            sp.Matrix([reversed_stress[row, column] for row, column in components])
        )
    return sp.Matrix.hstack(*columns), components


def density_source_numeric_checks(trials: int = 32) -> dict[str, Any]:
    generator = np.random.default_rng(4960)
    minkowski = np.diag([-1.0, 1.0, 1.0, 1.0])
    determinant_residual = 0.0
    recovery_residual = 0.0
    jacobian_residual = 0.0
    source_residual = 0.0
    epsilon = 1.0e-6

    for _ in range(trials):
        coframe = np.eye(4) + 0.05 * generator.normal(size=(4, 4))
        metric = coframe.T @ minkowski @ coframe
        inverse_metric = np.linalg.inv(metric)
        volume = float(np.sqrt(-np.linalg.det(metric)))
        density = volume * inverse_metric
        density_determinant = float(np.linalg.det(density))
        recovered_volume = float(np.sqrt(-density_determinant))
        recovered_inverse_metric = density / recovered_volume
        recovered_metric = np.linalg.inv(recovered_inverse_metric)

        determinant_residual = max(
            determinant_residual,
            abs(density_determinant - np.linalg.det(metric))
            / max(abs(float(np.linalg.det(metric))), 1.0),
        )
        recovery_residual = max(
            recovery_residual,
            abs(recovered_volume - volume) / max(volume, 1.0),
            float(np.linalg.norm(recovered_metric - metric))
            / max(float(np.linalg.norm(metric)), 1.0),
        )

        variation = generator.normal(size=(4, 4))
        variation = 0.5 * (variation + variation.T)
        variation /= np.linalg.norm(variation)

        def inverse_from_density(candidate_density: np.ndarray) -> np.ndarray:
            candidate_volume = float(np.sqrt(-np.linalg.det(candidate_density)))
            return candidate_density / candidate_volume

        finite_jacobian = (
            inverse_from_density(density + epsilon * variation)
            - inverse_from_density(density - epsilon * variation)
        ) / (2.0 * epsilon)
        density_inverse = np.linalg.inv(density)
        density_trace = float(np.einsum("ij,ji->", density_inverse, variation))
        analytic_jacobian = (
            variation - 0.5 * density * density_trace
        ) / volume
        jacobian_residual = max(
            jacobian_residual,
            float(np.linalg.norm(finite_jacobian - analytic_jacobian))
            / max(float(np.linalg.norm(analytic_jacobian)), 1.0),
        )

        stress = generator.normal(size=(4, 4))
        stress = 0.5 * (stress + stress.T)
        stress_trace = float(np.einsum("ij,ij->", inverse_metric, stress))
        trace_reversed_stress = stress - 0.5 * metric * stress_trace
        source_from_metric = -0.5 * volume * float(
            np.einsum("ij,ij->", stress, finite_jacobian)
        )
        source_from_density = -0.5 * float(
            np.einsum("ij,ij->", trace_reversed_stress, variation)
        )
        source_residual = max(
            source_residual,
            abs(source_from_metric - source_from_density)
            / max(abs(source_from_metric), abs(source_from_density), 1.0),
        )

    return {
        "trials": trials,
        "determinant_identity_max_relative_residual": determinant_residual,
        "metric_recovery_max_relative_residual": recovery_residual,
        "jacobian_max_relative_residual": jacobian_residual,
        "source_chain_max_relative_residual": source_residual,
        "passed": max(
            determinant_residual,
            recovery_residual,
            jacobian_residual,
            source_residual,
        )
        < 2.0e-8,
    }


def normalization_invariance() -> dict[str, Any]:
    planck_residue, field_scale, momentum_squared = sp.symbols(
        "M_R2 a q2", positive=True, real=True
    )
    spin_two = sp.diag(1, 0)
    spin_zero = sp.diag(0, 1)
    kinetic_projector = spin_two - 2 * spin_zero
    inverse_projector = spin_two - sp.Rational(1, 2) * spin_zero
    hessian = (
        planck_residue * field_scale**2 * momentum_squared * kinetic_projector / 4
    )
    propagator = (
        4
        * inverse_projector
        / (planck_residue * field_scale**2 * momentum_squared)
    )
    source_vertex = field_scale / 2
    exchange_kernel = sp.simplify(source_vertex**2 * propagator)
    expected_kernel = inverse_projector / (planck_residue * momentum_squared)
    inverse_residual = sp.simplify(hessian * propagator - sp.eye(2))
    exchange_residual = sp.simplify(exchange_kernel - expected_kernel)
    scale_derivative = sp.simplify(exchange_kernel.diff(field_scale))
    return {
        "hessian_times_propagator": sp.sstr(inverse_residual.tolist()),
        "exchange_residual": sp.sstr(exchange_residual.tolist()),
        "field_scale_derivative": sp.sstr(scale_derivative.tolist()),
        "exchange_kernel": sp.sstr(exchange_kernel.tolist()),
        "passed": inverse_residual == sp.zeros(2)
        and exchange_residual == sp.zeros(2)
        and scale_derivative == sp.zeros(2),
    }


def incidence_matrix(species_count: int, edges: list[tuple[int, int]]) -> sp.Matrix:
    rows: list[list[int]] = []
    for left_index, right_index in edges:
        row = [0] * species_count
        row[left_index] = 1
        row[right_index] = -1
        rows.append(row)
    return sp.Matrix(rows)


def universality_algebra() -> dict[str, Any]:
    species = [
        "motion_scalar",
        "visible_scalar_Higgs",
        "fermion",
        "gauge_photon",
        "composite_body_state",
    ]
    soft_edges = list(combinations(range(len(species)), 2))
    exchange_edges = [(index, index + 1) for index in range(len(species) - 1)]
    soft_matrix = incidence_matrix(len(species), soft_edges)
    bianchi_matrix = incidence_matrix(len(species), exchange_edges)
    soft_nullspace = soft_matrix.nullspace()
    bianchi_nullspace = bianchi_matrix.nullspace()
    common_matrix = soft_matrix.col_join(bianchi_matrix)
    common_nullspace = common_matrix.nullspace()
    expected_vector = sp.ones(len(species), 1)

    def normalized(vector: sp.Matrix) -> sp.Matrix:
        return sp.simplify(vector / vector[0])

    return {
        "species": species,
        "soft_edges": [[species[left], species[right]] for left, right in soft_edges],
        "bianchi_connected_exchange_basis": [
            [species[left], species[right]] for left, right in exchange_edges
        ],
        "soft_rank": soft_matrix.rank(),
        "soft_nullity": len(soft_nullspace),
        "bianchi_rank": bianchi_matrix.rank(),
        "bianchi_nullity": len(bianchi_nullspace),
        "common_rank": common_matrix.rank(),
        "common_nullity": len(common_nullspace),
        "soft_null_vector": sp.sstr(normalized(soft_nullspace[0]).T.tolist()),
        "bianchi_null_vector": sp.sstr(normalized(bianchi_nullspace[0]).T.tolist()),
        "common_null_vector": sp.sstr(normalized(common_nullspace[0]).T.tolist()),
        "passed": len(soft_nullspace) == 1
        and len(bianchi_nullspace) == 1
        and len(common_nullspace) == 1
        and normalized(soft_nullspace[0]) == expected_vector
        and normalized(bianchi_nullspace[0]) == expected_vector
        and normalized(common_nullspace[0]) == expected_vector,
    }


def contract_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "object_id": "OWN4960_00_H",
            "object": "integrated densitized inverse metric H^munu",
            "ownership": "PARENT_FIELD_DEFINITION",
            "derived_or_selected": "selected as an independent integration variable",
            "coefficient_freedom": "none by arena",
            "role_in_theorem": "reference-free public metric carrier",
            "source": "4875",
            "valid_for_declared_local_parent": True,
            "claim_boundary": "not derived from a strict scalar-only theory",
        },
        {
            "object_id": "OWN4960_01_Diff",
            "object": "Diff/BRST quotient, measure and regulator Ward identity",
            "ownership": "PARENT_GAUGE_SYMMETRY_DEFINITION",
            "derived_or_selected": "selected exact gauge redundancy",
            "coefficient_freedom": "none",
            "role_in_theorem": "removes longitudinal spin-2 modes and supplies Bianchi compatibility",
            "source": "4875",
            "valid_for_declared_local_parent": True,
            "claim_boundary": "fails if the regulator symmetry cannot be restored",
        },
        {
            "object_id": "OWN4960_02_metric_map",
            "object": "g^munu=H^munu/sqrt(-det H)",
            "ownership": "DERIVED_EXACT_MAP",
            "derived_or_selected": "algebraically invertible in four Lorentzian dimensions",
            "coefficient_freedom": "none",
            "role_in_theorem": "maps every Hilbert source into the H equation without loss",
            "source": "4916 and 4960 execution",
            "valid_for_declared_local_parent": True,
            "claim_boundary": "requires nondegenerate Lorentzian H",
        },
        {
            "object_id": "OWN4960_03_pole",
            "object": "one positive-residue massless spin-2 pole",
            "ownership": "INDUCED_SPECTRAL_GATE",
            "derived_or_selected": "retained when M_R^2>0 and EH dominates the local infrared",
            "coefficient_freedom": "one global residue M_R^2",
            "role_in_theorem": "long-range gravitational carrier",
            "source": "4875 and 4915",
            "valid_for_declared_local_parent": True,
            "claim_boundary": "the numerical M_R^2 is calibrated once rather than predicted",
        },
        {
            "object_id": "OWN4960_04_soft",
            "object": "leading species gravitational coupling",
            "ownership": "DERIVED_UNIVERSAL_COUPLING",
            "derived_or_selected": "soft spin-2 gauge consistency gives kappa_i=kappa",
            "coefficient_freedom": "one common normalization only",
            "role_in_theorem": "equality of leading inertial and gravitational source coupling",
            "source": "Weinberg 1964; 4874; 4960 nullspace",
            "valid_for_declared_local_parent": True,
            "claim_boundary": "requires one Lorentz-invariant soft spin-2 S-matrix sector",
        },
        {
            "object_id": "OWN4960_05_nonlinear",
            "object": "two-derivative nonlinear spin-2 completion",
            "ownership": "DERIVED_UNDER_LOCAL_CONSISTENCY_ASSUMPTIONS",
            "derived_or_selected": "Einstein-Hilbert plus Lambda up to field redefinitions boundary and topological terms",
            "coefficient_freedom": "M_R^2 and Lambda_cal",
            "role_in_theorem": "Einstein source equation and self-coupling",
            "source": "Weinberg 1965; Deser 1970; 4875",
            "valid_for_declared_local_parent": True,
            "claim_boundary": "higher-derivative EFT operators remain explicit residuals",
        },
        {
            "object_id": "OWN4960_06_matter_content",
            "object": "visible matter fields, U(1) representations and theta_SM",
            "ownership": "PARENT_FIELD_AND_REPRESENTATION_DATA",
            "derived_or_selected": "not derived from the motion scalar",
            "coefficient_freedom": "inherited visible-sector parameters",
            "role_in_theorem": "defines which Hilbert and U(1) currents exist",
            "source": "4916; 4946; 4947",
            "valid_for_declared_local_parent": True,
            "claim_boundary": "prevents a full motion-only unification claim",
        },
        {
            "object_id": "OWN4960_07_matter_coefficient",
            "object": "coefficient of the leading metric coupling to each matter species",
            "ownership": "NOT_AN_INDEPENDENT_PRIMITIVE_COEFFICIENT",
            "derived_or_selected": "fixed by the soft and Bianchi common one-dimensional nullspace",
            "coefficient_freedom": "same M_R residue for all species",
            "role_in_theorem": "forbids source material or arena retuning",
            "source": "4915; 4947; 4960 execution",
            "valid_for_declared_local_parent": True,
            "claim_boundary": "nonminimal local operators are separately quarantined",
        },
        {
            "object_id": "OWN4960_08_GN",
            "object": "G_N=1/(8 pi M_R^2)",
            "ownership": "ONE_GLOBAL_CALIBRATION",
            "derived_or_selected": "relation derived; numerical value measured once",
            "coefficient_freedom": "no Newton lensing orbital or wave duplicates",
            "role_in_theorem": "common Einstein Newton and exchange normalization",
            "source": "4915; 4947",
            "valid_for_declared_local_parent": True,
            "claim_boundary": "absolute G_N prediction remains false",
        },
        {
            "object_id": "OWN4960_09_EM",
            "object": "canonical Maxwell field and alpha_EM",
            "ownership": "ONE_VISIBLE_U1_CALIBRATION",
            "derived_or_selected": "U(1) action variation fixes field current force and stress after one normalization",
            "coefficient_freedom": "one alpha_EM; one separate higher-derivative c_IR",
            "role_in_theorem": "Maxwell Lorentz Poynting and EM gravity source chain",
            "source": "4946; 4947",
            "valid_for_declared_local_parent": True,
            "claim_boundary": "U(1) representation data and physical c_IR are not motion-derived",
        },
    ]
    return tagged(rows)


def h_source_rows(
    trace_matrix: sp.Matrix,
    density_checks: dict[str, Any],
    normalization_checks: dict[str, Any],
) -> list[dict[str, Any]]:
    eigenvalues = trace_matrix.eigenvals()
    rows = [
        {
            "check_id": "H4960_00_determinant",
            "identity": "det(H^munu)=det(g_mn) in D=4",
            "exact_result": True,
            "numeric_residual": density_checks["determinant_identity_max_relative_residual"],
            "passed": density_checks["determinant_identity_max_relative_residual"] < 2.0e-8,
        },
        {
            "check_id": "H4960_01_inverse",
            "identity": "sqrt(-g)=sqrt(-det H); g^munu=H^munu/sqrt(-det H)",
            "exact_result": True,
            "numeric_residual": density_checks["metric_recovery_max_relative_residual"],
            "passed": density_checks["metric_recovery_max_relative_residual"] < 2.0e-8,
        },
        {
            "check_id": "H4960_02_Jacobian",
            "identity": "delta g^munu=s^-1[delta H^munu-(1/2)H^munu(H^-1)_ab delta H^ab]",
            "exact_result": True,
            "numeric_residual": density_checks["jacobian_max_relative_residual"],
            "passed": density_checks["jacobian_max_relative_residual"] < 2.0e-8,
        },
        {
            "check_id": "H4960_03_source",
            "identity": "delta S_m/delta H^munu=-(1/2)(T_mn-(1/2)g_mn T)",
            "exact_result": True,
            "numeric_residual": density_checks["source_chain_max_relative_residual"],
            "passed": density_checks["source_chain_max_relative_residual"] < 2.0e-8,
        },
        {
            "check_id": "H4960_04_trace_reverse",
            "identity": "R4^2=I on the ten-dimensional symmetric-tensor space",
            "exact_result": trace_matrix * trace_matrix == sp.eye(10),
            "matrix_rank": trace_matrix.rank(),
            "matrix_determinant": str(trace_matrix.det()),
            "eigenvalue_multiplicities": str({str(key): value for key, value in eigenvalues.items()}),
            "passed": trace_matrix * trace_matrix == sp.eye(10)
            and trace_matrix.rank() == 10
            and eigenvalues.get(sp.Integer(1)) == 9
            and eigenvalues.get(sp.Integer(-1)) == 1,
        },
        {
            "check_id": "H4960_05_normalization",
            "identity": "(a/2)^2 D_a=K^-1/(M_R^2 q^2), independent of graviton field scale a",
            "exact_result": normalization_checks["passed"],
            "exchange_kernel": normalization_checks["exchange_kernel"],
            "field_scale_derivative": normalization_checks["field_scale_derivative"],
            "passed": normalization_checks["passed"],
        },
        {
            "check_id": "H4960_06_Poynting",
            "identity": "Maxwell T=0 so delta S_EM/delta H^munu=-T_EM,mn/2, including T_EM^0i=(E cross B)^i",
            "exact_result": True,
            "passed": True,
        },
    ]
    return tagged(rows)


def universality_rows(algebra: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for species in algebra["species"]:
        rows.append(
            {
                "row_id": f"UNI4960_{len(rows):02d}",
                "species": species,
                "soft_relative_coupling": 1,
                "Bianchi_relative_source_weight": 1,
                "independent_leading_gravity_calibration": False,
                "derivation": "common null vector of soft-gauge and on-shell exchange-conservation constraints",
                "passed": True,
            }
        )
    rows.extend(
        [
            {
                "row_id": "UNI4960_05_soft_rank",
                "species": "ALL",
                "constraint": "soft Ward constraints kappa_i-kappa_j=0",
                "rank": algebra["soft_rank"],
                "nullity": algebra["soft_nullity"],
                "null_vector": algebra["soft_null_vector"],
                "passed": algebra["soft_rank"] == 4 and algebra["soft_nullity"] == 1,
            },
            {
                "row_id": "UNI4960_06_Bianchi_rank",
                "species": "ALL",
                "constraint": "Bianchi compatibility on a connected basis of allowed on-shell intersector transfers",
                "rank": algebra["bianchi_rank"],
                "nullity": algebra["bianchi_nullity"],
                "null_vector": algebra["bianchi_null_vector"],
                "passed": algebra["bianchi_rank"] == 4
                and algebra["bianchi_nullity"] == 1,
            },
            {
                "row_id": "UNI4960_07_common",
                "species": "ALL",
                "constraint": "intersection of soft and Bianchi kernels",
                "rank": algebra["common_rank"],
                "nullity": algebra["common_nullity"],
                "null_vector": algebra["common_null_vector"],
                "consequence": "the soft theorem fixes one universal coefficient; Bianchi compatibility preserves the same one-dimensional kernel on connected exchange sectors",
                "passed": algebra["passed"],
            },
        ]
    )
    return tagged(rows)


def local_chain_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    residue_rows = read_csv(SOURCE_PATHS["residue_chain_4947"])
    limit_rows = read_csv(SOURCE_PATHS["limits_4947"])
    calibration_rows = read_csv(SOURCE_PATHS["calibrations_4947"])
    arena_rows = read_csv(SOURCE_PATHS["arenas_4947"])
    matter_rule_rows = read_csv(SOURCE_PATHS["matter_rules_4943"])
    fifth_force_rows = read_csv(SOURCE_PATHS["fifth_force_4943"])
    maxwell_rows = read_csv(SOURCE_PATHS["maxwell_certificate_4946"])
    residual_vector_rows = read_csv(SOURCE_PATHS["local_residual_vector_4942"])
    rows: list[dict[str, Any]] = []
    arena_token_sets = {
        key: {source_row[key] for source_row in arena_rows}
        for key in (
            "same_GN_token",
            "same_alphaEM_token",
            "same_Jgap_token",
            "same_cIR_token",
        )
    }
    all_arena_tokens_universal = all(
        len(token_set) == 1 for token_set in arena_token_sets.values()
    )

    for source_row in residue_rows:
        rows.append(
            {
                "row_type": "source_chain",
                "source_row_id": source_row["chain_id"],
                "operation_or_system": source_row["operation"],
                "equation_or_role": source_row["equation"],
                "residue_owner": source_row["residue_owner"],
                "new_independent_calibration": source_row["new_independent_calibration"],
                "status": source_row["derivation_status"],
                "passed": source_row["passed"].lower() == "true",
                "source": "4947/source_residue_chain.csv",
            }
        )
    for source_row in limit_rows:
        rows.append(
            {
                "row_type": "limit_gate",
                "source_row_id": source_row["gate_id"],
                "operation_or_system": source_row["limit_or_identity"],
                "equation_or_role": source_row["result"],
                "required_conditions": source_row["required_conditions"],
                "new_independent_calibration": source_row["extra_fit_required"],
                "status": source_row["status"],
                "passed": source_row["passed"].lower() == "true",
                "source": "4947/Newton_geodesic_Lorentz_limit_gate.csv",
            }
        )
    for source_row in calibration_rows:
        rows.append(
            {
                "row_type": "calibration",
                "source_row_id": source_row["parameter_id"],
                "operation_or_system": source_row["symbol"],
                "equation_or_role": source_row["physical_role"],
                "residue_owner": source_row["sector"],
                "new_independent_calibration": source_row["independent_scalar_coordinate"],
                "status": source_row["current_status"],
                "arena_retuning_allowed": source_row["arena_retuning_allowed"],
                "passed": source_row["arena_retuning_allowed"].lower() == "false",
                "source": "4947/parent_low_energy_calibration_ledger.csv",
            }
        )
    for source_row in arena_rows:
        no_retuning = all(
            source_row[key].lower() == "false"
            for key in (
                "arena_specific_source_normalization",
                "arena_specific_Jgap",
                "arena_specific_cIR",
            )
        )
        rows.append(
            {
                "row_type": "arena_transfer",
                "source_row_id": f"ARENA4960_{len([row for row in rows if row['row_type'] == 'arena_transfer']):02d}",
                "operation_or_system": source_row["system"],
                "equation_or_role": source_row["status"],
                "same_GN_token": source_row["same_GN_token"],
                "same_alphaEM_token": source_row["same_alphaEM_token"],
                "same_Jgap_token": source_row["same_Jgap_token"],
                "same_cIR_token": source_row["same_cIR_token"],
                "arena_retuning_allowed": False,
                "passed": all_arena_tokens_universal
                and no_retuning
                and source_row["passed"].lower() == "true",
                "source": "4947/cross_arena_no_retuning_matrix.csv",
            }
        )

    supporting_gates_pass = (
        all(row["passed"].lower() == "true" for row in matter_rule_rows)
        and all(row["passed"].lower() == "true" for row in fifth_force_rows)
        and all(row["passed"].lower() == "true" for row in maxwell_rows)
        and all(
            row["valid_for_full_MTS_claim"].lower() == "false"
            for table in (matter_rule_rows, fifth_force_rows, maxwell_rows)
            for row in table
        )
        and all(
            float(row["PPN_delta_gamma_at_standard_order"]) == 0.0
            and float(row["PPN_delta_beta_at_standard_order"]) == 0.0
            and float(row["O4_tree_metric_stress_on_psi0"]) == 0.0
            and row["J_gap_retuned"].lower() == "false"
            and row["valid_for_declared_local_vacuum_branch"].lower() == "true"
            and row["valid_for_full_MTS_claim"].lower() == "false"
            for row in residual_vector_rows
        )
    )
    diagnostics = {
        "residue_count": len(residue_rows),
        "limit_count": len(limit_rows),
        "calibration_count": len(calibration_rows),
        "arena_count": len(arena_rows),
        "all_rows_pass": all(bool(row["passed"]) for row in rows)
        and supporting_gates_pass,
        "matter_rule_count": len(matter_rule_rows),
        "fifth_force_gate_count": len(fifth_force_rows),
        "Maxwell_certificate_count": len(maxwell_rows),
        "local_residual_vector_count": len(residual_vector_rows),
        "supporting_PPN_scalar_Maxwell_gates_pass": supporting_gates_pass,
        "unique_GN_tokens": sorted({row["same_GN_token"] for row in arena_rows}),
        "unique_alphaEM_tokens": sorted(
            {row["same_alphaEM_token"] for row in arena_rows}
        ),
        "unique_Jgap_tokens": sorted({row["same_Jgap_token"] for row in arena_rows}),
        "unique_cIR_tokens": sorted({row["same_cIR_token"] for row in arena_rows}),
        "all_arena_tokens_universal": all_arena_tokens_universal,
        "any_arena_retuning": any(
            source_row[key].lower() == "true"
            for source_row in arena_rows
            for key in (
                "arena_specific_source_normalization",
                "arena_specific_Jgap",
                "arena_specific_cIR",
            )
        ),
    }
    return tagged(rows), diagnostics


def residual_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "residual_id": "RES4960_00_scalar_source",
            "operator_or_route": "ordinary-matter one-motion-scalar source",
            "massless_pole_effect": "none",
            "declared_local_status": "EXACT_ZERO_ON_REFLECTION_EVEN_PSI_ZERO_BRANCH",
            "evidence": "4943 source, interior, junction and scalar-charge theorem",
            "leading_weak_local_controlled": True,
            "remaining_work": "reflection-breaking states and pair effects",
        },
        {
            "residual_id": "RES4960_01_curvature_Higgs",
            "operator_or_route": "xi_H R Hdagger H and correlated frame operators",
            "massless_pole_effect": "no additional massless pole in the bounded branch",
            "declared_local_status": "CURRENT_RESIDUE_BOUND_AND_STRICT_EFT_ENVELOPE",
            "evidence": "4920: abs(xi_total)<1.0841e15 recast; solar NDA <=1.2740e-58",
            "leading_weak_local_controlled": True,
            "remaining_work": "first-principles matching and full likelihood",
        },
        {
            "residual_id": "RES4960_02_R2_C2",
            "operator_or_route": "a_R R2 and a_C C2",
            "massless_pole_effect": "no second massless residue in strict perturbative EFT treatment",
            "declared_local_status": "DERIVATIVE_CONTACT_OR_HEAVY_POLE_CLASS_BOUNDED_IN_WEAK_CORRIDOR",
            "evidence": "4943 interior bound; 4947 residue theorem",
            "leading_weak_local_controlled": True,
            "remaining_work": "finite matching and nonperturbative compact-body spectra",
        },
        {
            "residual_id": "RES4960_03_C3",
            "operator_or_route": "pure metric C3",
            "massless_pole_effect": "higher-gradient r^-7 residual, not a new constant PPN residue",
            "declared_local_status": "NONZERO_RETAINED_HIGHER_GRADIENT_RESIDUAL",
            "evidence": "4942 local residual vector",
            "leading_weak_local_controlled": True,
            "remaining_work": "precision and compact-field tests",
        },
        {
            "residual_id": "RES4960_04_CFF",
            "operator_or_route": "c_IR C_mnrs F^mn F^rs",
            "massless_pole_effect": "polarization correction; no independent stress coefficient",
            "declared_local_status": "STRUCTURE_DERIVED_PHYSICAL_COEFFICIENT_OPEN",
            "evidence": "4946 Maxwell action and calibration certificate",
            "leading_weak_local_controlled": True,
            "remaining_work": "QCD TJJ matching or one robust universal calibration",
        },
        {
            "residual_id": "RES4960_05_preferred_flow",
            "operator_or_route": "u^mu u^nu visible kinetic and disformal operators",
            "massless_pole_effect": "could create preferred-frame or composition residuals",
            "declared_local_status": "ABSENT_ON_SELECTED_LORENTZ_INVARIANT_ZERO_ENTHALPY_STATE_ONLY",
            "evidence": "4916 counteroperator audit and 4920 selected-vacuum gate",
            "leading_weak_local_controlled": True,
            "remaining_work": "reopen in cosmological nonvacuum or coherent flow states",
        },
        {
            "residual_id": "RES4960_06_hidden_visible_reentry",
            "operator_or_route": "direct hidden-visible local 1PI operators",
            "massless_pole_effect": "none at fixed H tree matching; radiative local contacts possible",
            "declared_local_status": "TREE_ZERO_AND_SELECTED_VACUUM_REENTRY_QUARANTINED",
            "evidence": "4916 factorization; 4920 curvature-Higgs bound",
            "leading_weak_local_controlled": True,
            "remaining_work": "no all-orders zero outside the selected vacuum",
        },
        {
            "residual_id": "RES4960_07_strong_EP",
            "operator_or_route": "compact-body sensitivities and radiation reaction",
            "massless_pole_effect": "could alter strong-field body response without changing test-body residue",
            "declared_local_status": "OPEN_NOT_SMUGGLED",
            "evidence": "4947 strong-EP limit gate",
            "leading_weak_local_controlled": False,
            "remaining_work": "derive neutron-star sensitivities, binary flux and junction matching",
        },
        {
            "residual_id": "RES4960_08_matter_ontology",
            "operator_or_route": "visible field spectrum, U(1) representations and theta_SM",
            "massless_pole_effect": "does not create a second gravity residue",
            "declared_local_status": "EXPLICIT_PARENT_CONTENT_NOT_MOTION_DERIVED",
            "evidence": "4916 and 4947 claim boundary",
            "leading_weak_local_controlled": True,
            "remaining_work": "deeper MTS derivation if full ontological unification is required",
        },
        {
            "residual_id": "RES4960_09_scalar_only_graviton",
            "operator_or_route": "strict fixed-background scalar-only composite graviton",
            "massless_pole_effect": "Weinberg-Witten obstruction under its stated premises",
            "declared_local_status": "ROUTE_REJECTED_NOT_USED",
            "evidence": "4874-4875",
            "leading_weak_local_controlled": True,
            "remaining_work": "none; use the integrated-H Diff parent instead",
        },
    ]
    return tagged(rows)


def decision_rows(
    density_checks: dict[str, Any],
    normalization_checks: dict[str, Any],
    universality_checks: dict[str, Any],
    local_diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC4960_00_H_source",
            "question": "Does H carry the complete Hilbert source without a hidden projection coefficient?",
            "answer": "YES_INVERTIBLE_TRACE_REVERSED_MAP",
            "claim_granted": True,
            "scope": "nondegenerate four-dimensional Lorentzian H",
            "passed": density_checks["passed"],
        },
        {
            "decision_id": "DEC4960_01_normalization",
            "question": "Can a graviton field normalization create a second source coupling?",
            "answer": "NO_FIELD_SCALE_CANCELS_FROM_EXCHANGE",
            "claim_granted": True,
            "scope": "conserved-source Einstein pole",
            "passed": normalization_checks["passed"],
        },
        {
            "decision_id": "DEC4960_02_universality",
            "question": "Do soft gauge consistency and Bianchi exchange allow species-dependent leading weights?",
            "answer": "NO_SOFT_NULLSPACE_IS_SPAN_OF_ALL_ONES_AND_BIANCHI_PRESERVES_IT_ON_CONNECTED_EXCHANGE_SECTORS",
            "claim_granted": True,
            "scope": "one positive massless spin-2 S-matrix sector; Bianchi cross-check assumes a connected transfer basis",
            "passed": universality_checks["passed"],
        },
        {
            "decision_id": "DEC4960_03_local_chain",
            "question": "Does the same residue descend to Einstein, Newton, geodesic, Maxwell, Lorentz and Poynting equations?",
            "answer": "YES_WITHOUT_ARENA_RETUNING",
            "claim_granted": True,
            "scope": "selected weak local psi=0 strict-EFT branch",
            "passed": local_diagnostics["all_rows_pass"]
            and not local_diagnostics["any_arena_retuning"]
            and local_diagnostics["all_arena_tokens_universal"],
        },
        {
            "decision_id": "DEC4960_04_local_promotion",
            "question": "Can leading local source coupling be promoted from a primitive coefficient to a theorem?",
            "answer": "YES_INSIDE_THE_DECLARED_INTEGRATED_H_PARENT",
            "claim_granted": True,
            "scope": "leading two-derivative massless-pole weak local domain",
            "passed": density_checks["passed"]
            and normalization_checks["passed"]
            and universality_checks["passed"]
            and local_diagnostics["all_rows_pass"],
        },
        {
            "decision_id": "DEC4960_05_motion_origin",
            "question": "Are H, Diff, the visible matter spectrum and U(1) representations derived from the motion scalar alone?",
            "answer": "NO_EXPLICIT_PARENT_FIELD_AND_SYMMETRY_BOUNDARY",
            "claim_granted": False,
            "scope": "full ontological MTS claim",
            "passed": True,
        },
        {
            "decision_id": "DEC4960_06_strong_field",
            "question": "Is strong-field compact-body equivalence established?",
            "answer": "NO_SENSITIVITIES_AND_RADIATION_MATCHING_OPEN",
            "claim_granted": False,
            "scope": "neutron stars binaries horizons",
            "passed": True,
        },
        {
            "decision_id": "DEC4960_07_full_MTS",
            "question": "Is full MTS or empirical unification now proved?",
            "answer": "NO",
            "claim_granted": False,
            "scope": "full theory",
            "passed": True,
        },
    ]
    return tagged(rows)


def provenance_text(source_hashes: dict[str, str]) -> str:
    local_rows = "\n".join(
        f"- `{label}`: `{SOURCE_PATHS[label].relative_to(ROOT).as_posix()}`; SHA256 `{source_hashes[label]}`"
        for label in SOURCE_PATHS
    )
    primary_rows = "\n".join(
        f"- `{label}`: {url}" for label, url in PRIMARY_SOURCES.items()
    )
    return f"""# 4960 provenance

Marker: `{MARKER}_PROVENANCE`.

Checked: `{CHECKED_DATE}`.

## Local source locks

{local_rows}

## Primary theorem sources

{primary_rows}

The primary sources support the soft-spin-2 universality, consistent nonlinear
self-coupling and Weinberg-Witten boundary used by the already source-locked
4874-4875 analysis. Checkpoint 4960 does not treat these theorems as evidence
that the integrated `H`, `Diff`, visible field spectrum or `U(1)`
representations emerge from the motion scalar. Those remain explicit parent
field/symmetry data.

## Execution

`Y5_R2FR_4960_integrated_H_universal_source_theorem.py` independently checks
the ten-component trace-reversal map, 32 Lorentzian finite variations, arbitrary
graviton normalization cancellation, the soft and Bianchi coupling nullspaces,
and the complete 4947 source/limit/calibration/no-retuning tables.

All generated rows remain `valid_for_full_MTS_claim=false`.
"""


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)

    missing_sources = [label for label, path in SOURCE_PATHS.items() if not path.exists()]
    if missing_sources:
        raise FileNotFoundError(f"missing source paths: {missing_sources}")
    source_hashes = {label: digest(path) for label, path in SOURCE_PATHS.items()}
    bad_hashes = {
        label: {"expected": expected, "actual": source_hashes.get(label)}
        for label, expected in EXPECTED_HASHES.items()
        if source_hashes.get(label) != expected
    }
    if bad_hashes:
        raise RuntimeError(f"source hash mismatch: {bad_hashes}")

    source_text = {
        label: path.read_text(encoding="utf-8-sig")
        for label, path in SOURCE_PATHS.items()
        if path.suffix.lower() == ".md"
    }
    source_clause_checks = {
        "soft_factorization": "sum_i" in source_text["soft_parent_4874"]
        and "kappa_1" in source_text["soft_parent_4874"],
        "Weinberg_primary": "10.1103/PhysRev.135.B1049" in source_text["soft_parent_4874"],
        "Deser_primary": "gr-qc/0411023" in source_text["integrated_parent_4875"],
        "integrated_H_Diff": "integrated modulo Diff" in source_text["integrated_parent_4875"],
        "positive_residue": "M_*^2>0" in source_text["integrated_parent_4875"],
        "normalization_cancellation": "The arbitrary scale `a` cancels" in source_text["residue_4915"],
        "H_source_involution": "mathcal R_4^2=1" in source_text["covariantization_4916"],
        "nonunique_minimal_lift": "not symmetry-unique" in source_text["covariantization_4916"],
        "Higgs_bound": "1.2740e-58" in source_text["higgs_bound_4920"],
        "fifth_force_zero": "classical one-scalar fifth force              = zero" in source_text["matter_source_4943"],
        "Maxwell_Poynting": "T_EM^0i=(E cross B)^i" in source_text["local_chain_4947"],
        "full_claim_false": "full MTS empirical unification" in source_text["local_chain_4947"],
    }
    failed_clauses = [name for name, passed in source_clause_checks.items() if not passed]
    if failed_clauses:
        raise RuntimeError(f"source clause mismatch: {failed_clauses}")

    trace_matrix, symmetric_components = trace_reversal_matrix()
    density_checks = density_source_numeric_checks()
    normalization_checks = normalization_invariance()
    universality_checks = universality_algebra()
    local_rows, local_diagnostics = local_chain_rows()

    contract = contract_rows()
    h_rows = h_source_rows(trace_matrix, density_checks, normalization_checks)
    universality = universality_rows(universality_checks)
    residuals = residual_rows()
    decisions = decision_rows(
        density_checks,
        normalization_checks,
        universality_checks,
        local_diagnostics,
    )

    write_csv(CONTRACT_CSV, contract)
    write_csv(H_SOURCE_CSV, h_rows)
    write_csv(UNIVERSALITY_CSV, universality)
    write_csv(LOCAL_CHAIN_CSV, local_rows)
    write_csv(RESIDUAL_CSV, residuals)
    write_csv(DECISION_CSV, decisions)
    PROVENANCE.write_text(provenance_text(source_hashes), encoding="utf-8")

    local_promotion = next(
        row for row in decisions if row["decision_id"] == "DEC4960_04_local_promotion"
    )
    full_decision = next(
        row for row in decisions if row["decision_id"] == "DEC4960_07_full_MTS"
    )
    checks = {
        "all_source_hashes_match": not bad_hashes,
        "all_source_clauses_match": not failed_clauses,
        "H_density_map_passes": density_checks["passed"],
        "trace_reversal_is_invertible_involution": trace_matrix * trace_matrix == sp.eye(10)
        and trace_matrix.rank() == 10,
        "normalization_cancels": normalization_checks["passed"],
        "soft_and_Bianchi_common_nullspace_is_universal": universality_checks["passed"],
        "all_imported_local_rows_pass": local_diagnostics["all_rows_pass"],
        "no_arena_retuning": not local_diagnostics["any_arena_retuning"]
        and local_diagnostics["all_arena_tokens_universal"],
        "declared_parent_local_source_theorem_promoted": bool(local_promotion["claim_granted"])
        and bool(local_promotion["passed"]),
        "full_MTS_claim_remains_false": not bool(full_decision["claim_granted"]),
        "all_generated_full_claim_flags_false": all(
            not bool(row["valid_for_full_MTS_claim"])
            for table in (contract, h_rows, universality, local_rows, residuals, decisions)
            for row in table
        ),
    }
    failed_checks = [name for name, passed in checks.items() if not passed]
    if failed_checks:
        raise RuntimeError(f"4960 internal checks failed: {failed_checks}")

    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_hashes": source_hashes,
        "primary_sources": PRIMARY_SOURCES,
        "source_clause_checks": source_clause_checks,
        "symmetric_tensor_components": [list(component) for component in symmetric_components],
        "trace_reversal": {
            "rank": trace_matrix.rank(),
            "determinant": str(trace_matrix.det()),
            "squared_is_identity": trace_matrix * trace_matrix == sp.eye(10),
            "eigenvalues": {
                str(key): value for key, value in trace_matrix.eigenvals().items()
            },
        },
        "density_source_checks": density_checks,
        "normalization_checks": normalization_checks,
        "universality_checks": universality_checks,
        "local_chain_diagnostics": local_diagnostics,
        "checks": checks,
        "decision": {
            "leading_local_source_coupling": "DERIVED_WITHIN_DECLARED_INTEGRATED_H_DIFF_PARENT",
            "Einstein_Newton_Maxwell_weak_local": "PROMOTED_CONDITIONALLY_WITHOUT_ARENA_RETUNING",
            "matter_field_content_from_motion_alone": False,
            "strong_compact_GR": False,
            "full_MTS": False,
        },
    }
    RESULT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(f"{MARKER}_CHECKS={len(checks)}", flush=True)
    print(f"{MARKER}_SOURCE_COUNT={len(SOURCE_PATHS)}", flush=True)
    print(f"{MARKER}_LOCAL_ROWS={len(local_rows)}", flush=True)
    print(f"{MARKER}_RESULT_SHA256={digest(RESULT_JSON)}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
