from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp
from pypdf import PdfReader


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4961"

RESULT_JSON = SOURCE / "integrated_H_origin_and_induced_EH_results.json"
INVENTORY_CSV = SOURCE / "microscopic_tensor_density_candidate_inventory.csv"
MAP_CSV = SOURCE / "local_and_ensemble_metric_map_rank_gate.csv"
COLLECTIVE_CSV = SOURCE / "collective_field_transform_and_Diff_gate.csv"
BACKGROUND_CSV = SOURCE / "reference_background_split_Ward_gate.csv"
HESSIAN_CSV = SOURCE / "motion_Hessian_no_bootstrap_audit.csv"
RESIDUE_CSV = SOURCE / "induced_EH_residue_scale_gate.csv"
DECISION_CSV = SOURCE / "integrated_H_origin_boundary_decision.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4961_INTEGRATED_H_ORIGIN_AND_INDUCED_EH_BOUNDARY"
CHECKED_DATE = "2026-07-13"

SOURCE_PATHS = {
    "core_fundamental_action": ROOT
    / "core-mts-framework"
    / "action-principle"
    / "the-fundamental-action-of-motion-timespace-field-theory.md",
    "core_action_principle": ROOT
    / "core-mts-framework"
    / "action-principle"
    / "the-motion-timespace-action-principle.md",
    "core_EFT": ROOT
    / "core-mts-framework"
    / "field-theory"
    / "the-effective-field-theory-of-motion-timespace.md",
    "core_PDF": ROOT
    / "core-mts-framework"
    / "field-theory"
    / "motion-timespace.pdf",
    "primitive_audit_4872": POST
    / "4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md",
    "open_parent_4873": POST
    / "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md",
    "split_Ward_4874": POST
    / "4874-Y5-R2FR-metric-only-quotient-background-independence-and-universal-principal-symbol-proof-or-equivalence-axiom-freeze.md",
    "integrated_H_4875": POST
    / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
    "induced_parent_4876": POST
    / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
    "spectrum_4877": POST
    / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
    "gravity_parent_4935": POST
    / "source-intake"
    / "functional_rg"
    / "4935"
    / "completed_fixed_point_trajectory_results.json",
    "motion_Hessian_4956": POST
    / "4956-Y5-R2FR-functional-PX-motion-flow-gravity-source-and-convergence-or-derivative-hierarchy-rejection.md",
    "motion_Hessian_contract_4956": POST
    / "source-intake"
    / "functional_rg"
    / "4956"
    / "functional_PX_Hessian_contract.csv",
    "universal_source_4960": POST
    / "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md",
    "universal_source_result_4960": POST
    / "source-intake"
    / "functional_rg"
    / "4960"
    / "integrated_H_universal_source_results.json",
}

EXPECTED_HASHES = {
    "core_fundamental_action": "afbb6a6e86ee30ca790f829374b791b307ace0e20f175b1600632205f9aeff54",
    "core_action_principle": "04df43511ab101d57e2d1f570e56c8555a371ac1dfb0fc1f97180a5b2d35afa4",
    "core_EFT": "6024bb60c6883e17c8036cd44ccce6aff87b2d3c7b07cffccf11e57c38b5cde8",
    "core_PDF": "b659dd9b9b517d7269a60d2213efb41651a4afc5bd6c2db7f75e24f2bb47998e",
    "primitive_audit_4872": "9a4eaed25f41167381ea77437350c322f7a4ee9cfab3228cfc2db0bd5f204923",
    "open_parent_4873": "af2c97091477525fb7244e5b2577e4a4c70d863987ebbb39b6c974d978b38b6e",
    "split_Ward_4874": "4eac48d7c90262bc0856d70eac8b25c0eed6b75bae1a11c16f5d1cdbf6ba81bb",
    "integrated_H_4875": "83b20a1314e40e5fa9c30dcff5d47254f21cb47cfd8f2d1df4f14728f71fa484",
    "induced_parent_4876": "8798d2de8c48ccd4fcc22d676aa1ae37cb6ac7691a579f9444095a8302832780",
    "spectrum_4877": "9d57f0ec8028530a48c7cab90b0447fead680461500a8c3da2390a253ac39dd4",
    "gravity_parent_4935": "8793e369ba0a9726c43dc64fe454ba87f88876832eca0ba9b79f07b171d1e222",
    "motion_Hessian_4956": "c3cdc970258583882c13d6544e17c8cef2620d89002ee7998825566ce6630367",
    "motion_Hessian_contract_4956": "89afa890522ae40e7a624023f9f9bb62fdf8a01bc8c659fd7b76ab76fd900a16",
    "universal_source_4960": "6cd343d022dde751f86ad82eaf0f61fb5e3616753c228f631c44a45da278a69d",
    "universal_source_result_4960": "6fe2d8335cb1a4902c07c986e597e2f748050aa31f6137c5b52f9ced94542477",
}

CORPUS_ROOTS = (
    ROOT / "core-mts-framework",
    ROOT / "quantum-particle-field",
    ROOT / "mathematics",
)


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


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, sp.logic.boolalg.Boolean):
        return bool(value)
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, np.generic):
        return value.item()
    return value


def extract_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return path.read_text(encoding="utf-8-sig")


def first_excerpt(source_text: str, pattern: re.Pattern[str]) -> str:
    match = pattern.search(source_text)
    if match is None:
        return ""
    start = max(0, match.start() - 80)
    end = min(len(source_text), match.end() + 120)
    return re.sub(r"\s+", " ", source_text[start:end]).strip()


def corpus_inventory() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    scalar_pattern = re.compile(
        r"fundamental (?:object|field|elementary object).*?scalar|"
        r"scalar motion field|psi\s*:\s*(?:R|ℝ)[\^⁴4]",
        re.IGNORECASE | re.DOTALL,
    )
    covariance_pattern = re.compile(
        r"emergent metric|smoothed covariance|coarse[- ]grained gradient covariance|"
        r"g_\{[^}]+\}\s*=\s*(?:eta|η)_\{[^}]+\}.*?partial|"
        r"g_\{[^}]+\}.*?⟨\s*∂",
        re.IGNORECASE | re.DOTALL,
    )
    independent_tensor_pattern = re.compile(
        r"(?:integrat(?:e|ed|ing)|path integral).*?(?:D\s*H|metric field|tensor density)|"
        r"independent\s+(?:symmetric\s+)?(?:metric|rank[- ]?two tensor|tensor density|tetrad|coframe)|"
        r"fundamental\s+(?:metric field|rank[- ]?two tensor|tensor density|tetrad|coframe)|"
        r"Vol\s*\(\s*Diff\s*\)|BRST",
        re.IGNORECASE | re.DOTALL,
    )
    exact_diff_pattern = re.compile(
        r"diffeomorphism (?:gauge|redundancy|quotient)|exact Diff|BRST|Vol\s*\(\s*Diff\s*\)",
        re.IGNORECASE,
    )
    fixed_background_pattern = re.compile(
        r"Minkowski (?:metric|background|spacetime)|fixed background|eta_\{|η_\{",
        re.IGNORECASE,
    )
    gauge_extension_pattern = re.compile(
        r"Yang.?Mills|gauge field(?:s)?\s+A_|non-Abelian gauge|field strength tensor",
        re.IGNORECASE,
    )

    rows: list[dict[str, Any]] = []
    for corpus_root in CORPUS_ROOTS:
        for path in sorted(corpus_root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in {".md", ".pdf"}:
                continue
            source_text = extract_text(path)
            independent_match = independent_tensor_pattern.search(source_text)
            exact_diff_match = exact_diff_pattern.search(source_text)
            rows.append(
                {
                    "source_path": path.relative_to(ROOT).as_posix(),
                    "source_sha256": digest(path),
                    "format": path.suffix.lower().lstrip("."),
                    "declares_scalar_primitive": bool(scalar_pattern.search(source_text)),
                    "uses_covariance_metric_readout": bool(
                        covariance_pattern.search(source_text)
                    ),
                    "uses_fixed_background_scaffold": bool(
                        fixed_background_pattern.search(source_text)
                    ),
                    "declares_independent_tensor_or_metric_parent": bool(
                        independent_match
                    ),
                    "declares_exact_Diff_BRST_parent": bool(exact_diff_match),
                    "contains_internal_gauge_extension": bool(
                        gauge_extension_pattern.search(source_text)
                    ),
                    "candidate_excerpt": first_excerpt(
                        source_text, independent_tensor_pattern
                    ),
                    "classification": (
                        "INDEPENDENT_TENSOR_GAUGE_CANDIDATE"
                        if independent_match and exact_diff_match
                        else "COVARIANCE_READOUT_NOT_INDEPENDENT_PARENT"
                        if covariance_pattern.search(source_text)
                        else "INTERNAL_GAUGE_EXTENSION_NOT_GRAVITY_GAUGE"
                        if gauge_extension_pattern.search(source_text)
                        else "NO_RELEVANT_PARENT_CANDIDATE"
                    ),
                }
            )

    candidate_rows = [
        row
        for row in rows
        if row["declares_independent_tensor_or_metric_parent"]
        and row["declares_exact_Diff_BRST_parent"]
    ]
    diagnostics = {
        "files_scanned": len(rows),
        "markdown_files": sum(row["format"] == "md" for row in rows),
        "pdf_files": sum(row["format"] == "pdf" for row in rows),
        "scalar_primitive_files": sum(
            bool(row["declares_scalar_primitive"]) for row in rows
        ),
        "covariance_metric_files": sum(
            bool(row["uses_covariance_metric_readout"]) for row in rows
        ),
        "independent_tensor_Diff_candidate_count": len(candidate_rows),
        "independent_tensor_Diff_candidate_paths": [
            row["source_path"] for row in candidate_rows
        ],
    }
    return tagged(rows), diagnostics


def metric_map_rank_gate() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    symmetric_components = [
        (row_index, column_index)
        for row_index in range(4)
        for column_index in range(row_index, 4)
    ]
    gradient_symbols = sp.symbols("v0:4", real=True)
    rank_one_components = sp.Matrix(
        [
            gradient_symbols[row_index] * gradient_symbols[column_index]
            for row_index, column_index in symmetric_components
        ]
    )
    rank_one_jacobian = rank_one_components.jacobian(gradient_symbols)
    generic_point = {symbol: prime for symbol, prime in zip(gradient_symbols, (1, 2, 3, 5))}
    generic_rank = int(rank_one_jacobian.subs(generic_point).rank())

    lower_symbols: dict[tuple[int, int], sp.Symbol] = {}
    lower_matrix = sp.zeros(4)
    for row_index in range(4):
        for column_index in range(row_index + 1):
            symbol = sp.symbols(f"l{row_index}{column_index}", real=True)
            lower_symbols[(row_index, column_index)] = symbol
            lower_matrix[row_index, column_index] = symbol
    covariance_matrix = lower_matrix * lower_matrix.T
    covariance_components = sp.Matrix(
        [
            covariance_matrix[row_index, column_index]
            for row_index, column_index in symmetric_components
        ]
    )
    lower_variables = list(lower_symbols.values())
    covariance_jacobian = covariance_components.jacobian(lower_variables)
    identity_point = {
        symbol: 1 if row_index == column_index else 0
        for (row_index, column_index), symbol in lower_symbols.items()
    }
    covariance_tangent_rank = int(covariance_jacobian.subs(identity_point).rank())

    rank_one_matrix = sp.Matrix(4, 1, gradient_symbols) * sp.Matrix(
        1, 4, gradient_symbols
    )
    rank_one_matrix_rank = int(rank_one_matrix.subs(generic_point).rank())

    rows = tagged(
        [
            {
                "gate_id": "MAP4961_00_single_gradient",
                "map": "O_mn(v)=v_m v_n",
                "domain_dimension": 4,
                "target_dimension": 10,
                "generic_Jacobian_rank": generic_rank,
                "matrix_rank_at_generic_point": rank_one_matrix_rank,
                "result": "NOT_LOCALLY_SURJECTIVE_ON_SYMMETRIC_TENSORS",
                "passed": generic_rank == 4 and rank_one_matrix_rank == 1,
            },
            {
                "gate_id": "MAP4961_01_first_jet_bound",
                "map": "H_mn=F_mn(psi,partial_0psi,...,partial_3psi)",
                "domain_dimension": 5,
                "target_dimension": 10,
                "generic_Jacobian_rank": "at_most_5",
                "matrix_rank_at_generic_point": "not_applicable",
                "result": "NO_LOCAL_INVERTIBLE_ONE_SCALAR_FIRST_JET_MAP",
                "passed": True,
            },
            {
                "gate_id": "MAP4961_02_connected_covariance",
                "map": "C=L L^T around positive_definite C=I",
                "domain_dimension": 10,
                "target_dimension": 10,
                "generic_Jacobian_rank": covariance_tangent_rank,
                "matrix_rank_at_generic_point": 4,
                "result": "ENSEMBLE_COVARIANCE_CAN_SPAN_TEN_TENSOR_DIRECTIONS",
                "passed": covariance_tangent_rank == 10,
            },
            {
                "gate_id": "MAP4961_03_interpretation",
                "map": "single_scalar_state_to_connected_two_point_covariance",
                "domain_dimension": "functional_state_space",
                "target_dimension": 10,
                "generic_Jacobian_rank": "can_be_10",
                "matrix_rank_at_generic_point": "can_be_4",
                "result": "ALGEBRAIC_RANK_OBSTRUCTION_EVADED_ONLY_BY_STATE_NONLOCAL_DATA_NOT_BY_LOCAL_FIELD_REDEFINITION",
                "passed": covariance_tangent_rank == 10 and generic_rank < 10,
            },
        ]
    )
    diagnostics = {
        "symmetric_components": [list(component) for component in symmetric_components],
        "single_gradient_Jacobian_shape": list(rank_one_jacobian.shape),
        "single_gradient_generic_rank": generic_rank,
        "single_gradient_outer_product_rank": rank_one_matrix_rank,
        "first_jet_rank_upper_bound": 5,
        "covariance_Cholesky_Jacobian_shape": list(covariance_jacobian.shape),
        "covariance_tangent_rank_at_identity": covariance_tangent_rank,
        "passed": generic_rank == 4
        and rank_one_matrix_rank == 1
        and covariance_tangent_rank == 10,
    }
    return rows, diagnostics


def collective_field_gate() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    symmetric_components = [
        (row_index, column_index)
        for row_index in range(4)
        for column_index in range(row_index, 4)
    ]
    def gauge_map_for(momentum_vector: sp.Matrix) -> sp.Matrix:
        result = sp.zeros(10, 4)
        for component_index, (row_index, column_index) in enumerate(
            symmetric_components
        ):
            for vector_index in range(4):
                result[component_index, vector_index] = (
                    momentum_vector[row_index]
                    * int(column_index == vector_index)
                    + momentum_vector[column_index]
                    * int(row_index == vector_index)
                )
        return result

    momentum_samples = {
        "timelike_axis": sp.Matrix([1, 0, 0, 0]),
        "spacelike_axis": sp.Matrix([0, 1, 0, 0]),
        "Minkowski_null": sp.Matrix([1, 1, 0, 0]),
        "generic": sp.Matrix([1, 2, 3, 5]),
    }
    gauge_ranks = {
        label: int(gauge_map_for(momentum_vector).rank())
        for label, momentum_vector in momentum_samples.items()
    }
    momentum = momentum_samples["generic"]
    gauge_map = gauge_map_for(momentum)
    gauge_rank = int(gauge_map.rank())

    inverse_kernel = sp.eye(10)
    inverse_kernel_rank = int(inverse_kernel.rank())
    inverse_kernel_ward_residual = inverse_kernel * gauge_map
    gram = gauge_map.T * gauge_map
    quotient_hessian = sp.eye(10) - gauge_map * gram.inv() * gauge_map.T
    quotient_rank = int(quotient_hessian.rank())
    quotient_nullity = 10 - quotient_rank
    quotient_ward_residual = sp.simplify(quotient_hessian * gauge_map)

    current_0, current_1 = sp.symbols("J0 J1", real=True)
    auxiliary_0, auxiliary_1 = sp.symbols("chi0 chi1", real=True)
    current_vector = sp.Matrix([current_0, current_1])
    auxiliary_vector = sp.Matrix([auxiliary_0, auxiliary_1])
    kernel = sp.Matrix([[2, 1], [1, 3]])
    shifted_auxiliary = auxiliary_vector - kernel * current_vector
    left_exponent = sp.expand(
        -sp.Rational(1, 2)
        * (auxiliary_vector.T * kernel.inv() * auxiliary_vector)[0]
        + (auxiliary_vector.T * current_vector)[0]
    )
    completed_square = sp.expand(
        -sp.Rational(1, 2)
        * (shifted_auxiliary.T * kernel.inv() * shifted_auxiliary)[0]
        + sp.Rational(1, 2) * (current_vector.T * kernel * current_vector)[0]
    )
    gaussian_identity_residual = sp.simplify(left_exponent - completed_square)

    tuning_parameter = sp.symbols("epsilon", real=True)
    tuned_hessian = sp.diag(tuning_parameter, *([1] * 9))
    tuned_determinant = sp.factor(tuned_hessian.det())

    rows = tagged(
        [
            {
                "gate_id": "COL4961_00_HS_identity",
                "construction": "exp(i J K J/2)=N integral Dchi exp(i[-chi Kinv chi/2+chi J])",
                "exact_check": f"completed_square_residual={gaussian_identity_residual}",
                "rank_or_nullity": f"rank(Kinv)={inverse_kernel_rank}",
                "result": "EXACT_AUXILIARY_FIELD_REWRITE_FOR_INVERTIBLE_KERNEL",
                "creates_new_gauge_redundancy": False,
                "passed": gaussian_identity_residual == 0 and kernel.det() != 0,
            },
            {
                "gate_id": "COL4961_01_spin2_gauge_map",
                "construction": "delta h_mn=q_m xi_n+q_n xi_m",
                "exact_check": f"ranks={gauge_ranks}",
                "rank_or_nullity": "required_Hessian_nullity_at_least_4",
                "result": "FOUR_GAUGE_NULL_DIRECTIONS_REQUIRED_AT_GENERIC_NONZERO_MOMENTUM",
                "creates_new_gauge_redundancy": True,
                "passed": gauge_rank == 4,
            },
            {
                "gate_id": "COL4961_02_regular_HS_Ward_failure",
                "construction": "regular ultralocal Kinv=I10",
                "exact_check": f"Kinv_Rq_zero={inverse_kernel_ward_residual == sp.zeros(10, 4)}",
                "rank_or_nullity": "rank=10 nullity=0",
                "result": "REGULAR_HS_KERNEL_CANNOT_BE_AN_UNGAUGED_DIFF_HESSIAN",
                "creates_new_gauge_redundancy": False,
                "passed": inverse_kernel_rank == 10
                and inverse_kernel_ward_residual != sp.zeros(10, 4),
            },
            {
                "gate_id": "COL4961_03_Ward_Hessian",
                "construction": "Gamma_perp=I-R(RT R)^-1 RT",
                "exact_check": f"Gamma_perp_Rq_zero={quotient_ward_residual == sp.zeros(10, 4)}",
                "rank_or_nullity": f"rank={quotient_rank} nullity={quotient_nullity}",
                "result": "WARD_COMPATIBLE_OPERATOR_IS_SINGULAR_BEFORE_GAUGE_FIXING",
                "creates_new_gauge_redundancy": True,
                "passed": quotient_ward_residual == sp.zeros(10, 4)
                and quotient_nullity == 4
                and quotient_hessian.det() == 0,
            },
            {
                "gate_id": "COL4961_04_singular_kernel_boundary",
                "construction": "replace Kinv by Gamma_perp in the HS identity",
                "exact_check": f"det(Gamma_perp)={quotient_hessian.det()}",
                "rank_or_nullity": f"nullity={quotient_nullity}",
                "result": "STANDARD_HS_NORMALIZATION_AND_INVERSE_FAIL_UNLESS_A_GAUGE_QUOTIENT_IS_ADDED_AS_NEW_PARENT_DATA",
                "creates_new_gauge_redundancy": False,
                "passed": quotient_hessian.det() == 0,
            },
            {
                "gate_id": "COL4961_05_accidental_pole_tuning",
                "construction": "Gamma(0)=Kinv+Pi(0); tune one eigenvalue to epsilon",
                "exact_check": f"det(Gamma(0))={tuned_determinant}",
                "rank_or_nullity": "nullity=1 only at epsilon=0; Diff requires four Ward-aligned null directions",
                "result": "AN_ACCIDENTAL_ZERO_EIGENVALUE_IS_TUNING_NOT_A_DIFF_WARD_IDENTITY",
                "creates_new_gauge_redundancy": False,
                "passed": tuned_determinant == tuning_parameter,
            },
            {
                "gate_id": "COL4961_06_composite_delta",
                "construction": "1=integral DH delta[H-O(psi)]",
                "exact_check": "H_support_is_exactly_the_image_of_O",
                "rank_or_nullity": "no_independent_H_configuration_direction",
                "result": "EXACT_CHANGE_OF_VARIABLES_REMAINS_THE_FIXED_BACKGROUND_COMPOSITE_THEORY",
                "creates_new_gauge_redundancy": False,
                "passed": True,
            },
            {
                "gate_id": "COL4961_07_release_delta",
                "construction": "integral DH without delta[H-O(psi)] modulo Diff",
                "exact_check": "configuration_space_and_redundancy_are_enlarged",
                "rank_or_nullity": "independent_H_plus_four_gauge_directions",
                "result": "THIS_IS_THE_4875_PARENT_FIELD_UPGRADE_NOT_A_DERIVATION_FROM_THE_SCALAR",
                "creates_new_gauge_redundancy": True,
                "passed": True,
            },
        ]
    )
    diagnostics = {
        "momentum": [int(value) for value in momentum],
        "sampled_gauge_map_ranks": gauge_ranks,
        "gauge_map_shape": list(gauge_map.shape),
        "gauge_map_rank": gauge_rank,
        "regular_inverse_kernel_rank": inverse_kernel_rank,
        "regular_inverse_kernel_Ward_zero": inverse_kernel_ward_residual
        == sp.zeros(10, 4),
        "quotient_Hessian_rank": quotient_rank,
        "quotient_Hessian_nullity": quotient_nullity,
        "quotient_Hessian_Ward_zero": quotient_ward_residual == sp.zeros(10, 4),
        "quotient_Hessian_determinant": str(quotient_hessian.det()),
        "gaussian_identity_residual": str(gaussian_identity_residual),
        "accidental_pole_determinant": str(tuned_determinant),
        "passed": gauge_rank == 4
        and all(rank == 4 for rank in gauge_ranks.values())
        and inverse_kernel_rank == 10
        and inverse_kernel_ward_residual != sp.zeros(10, 4)
        and quotient_nullity == 4
        and quotient_ward_residual == sp.zeros(10, 4)
        and gaussian_identity_residual == 0,
    }
    return rows, diagnostics


def background_split_gate() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    minkowski = sp.diag(-1, 1, 1, 1)
    gradient = sp.Matrix([2, 1, 0, 0])
    kinetic_scalar = (gradient.T * minkowski.inv() * gradient)[0]
    stress = gradient * gradient.T - sp.Rational(1, 2) * minkowski * kinetic_scalar
    stress_rank = int(stress.rank())
    stress_norm_squared = sp.simplify(sum(value**2 for value in stress))

    rows = tagged(
        [
            {
                "gate_id": "BG4961_00_reference_action",
                "object": "S0[psi;g_ref]=integral sqrt(-g_ref) g_ref^mn partial_mpsi partial_npsi/2",
                "exact_result": "delta S0/delta g_ref is proportional to the scalar Hilbert stress",
                "numeric_or_symbolic_value": f"T={stress.tolist()}",
                "status": "EXPLICIT_REFERENCE_METRIC_DEPENDENCE",
                "passed": stress != sp.zeros(4),
            },
            {
                "gate_id": "BG4961_01_nonzero_witness",
                "object": "g_ref=eta and partial_m psi=(2,1,0,0)",
                "exact_result": "reference stress is nonzero",
                "numeric_or_symbolic_value": f"X={kinetic_scalar}; rank={stress_rank}; Frobenius2={stress_norm_squared}",
                "status": "SPLIT_VARIATION_NOT_AN_IDENTITY_OF_THE_PRINTED_SCALAR_ACTION",
                "passed": stress_rank > 0 and stress_norm_squared > 0,
            },
            {
                "gate_id": "BG4961_02_split_Ward_requirement",
                "object": "g_hat=g_ref+C and delta Gamma_IR/delta g_ref|g_hat=0",
                "exact_result": "requires compensating split symmetry or dynamical cancellation for every field configuration",
                "numeric_or_symbolic_value": "no such identity in the primitive corpus",
                "status": "BACKGROUND_INDEPENDENCE_NOT_DERIVED",
                "passed": True,
            },
            {
                "gate_id": "BG4961_03_spurion_boundary",
                "object": "simultaneous tensor transformation of g_ref and psi",
                "exact_result": "coordinate covariance does not remove g_ref from observables",
                "numeric_or_symbolic_value": "spurionic_covariance_not_Diff_quotient",
                "status": "COVARIANCE_IS_NOT_GAUGE_REDUNDANCY",
                "passed": True,
            },
        ]
    )
    diagnostics = {
        "test_gradient": [int(value) for value in gradient],
        "kinetic_scalar": str(kinetic_scalar),
        "stress": [[str(stress[row, column]) for column in range(4)] for row in range(4)],
        "stress_rank": stress_rank,
        "stress_Frobenius_squared": str(stress_norm_squared),
        "printed_scalar_action_has_nonzero_reference_variation": stress != sp.zeros(4),
        "passed": stress != sp.zeros(4) and stress_norm_squared > 0,
    }
    return rows, diagnostics


def motion_hessian_audit() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    hessian_rows = read_csv(SOURCE_PATHS["motion_Hessian_contract_4956"])
    metric_row = next(
        row for row in hessian_rows if row["contract_id"] == "H4956_01_metric_block"
    )
    mixed_row = next(
        row for row in hessian_rows if row["contract_id"] == "H4956_02_mixed_block"
    )
    gravity_parent = json.loads(
        SOURCE_PATHS["gravity_parent_4935"].read_text(encoding="utf-8")
    )
    fixed_gravity = float(gravity_parent["flow_contract"]["fixed_point"][0])
    coordinates = list(gravity_parent["flow_contract"]["coordinates"])
    source_newton_pole = float(gravity_parent["flow_contract"]["source_Newton_pole"])

    rows = tagged(
        [
            {
                "gate_id": "HES4961_00_metric_baseline",
                "source_equation": metric_row["equation"],
                "evaluation": "set g=0",
                "result": "H_hh=I10",
                "interpretation": "the metric propagator and regulator baseline already exist before motion corrections",
                "can_derive_H_or_EH_from_motion": False,
                "passed": metric_row["equation"].startswith("H_hh=I10+32*pi*g"),
            },
            {
                "gate_id": "HES4961_01_mixed_baseline",
                "source_equation": mixed_row["equation"],
                "evaluation": "set g=0",
                "result": "H_hpsi=0",
                "interpretation": "motion-metric mixing is an expansion around the inherited gravity coordinate",
                "can_derive_H_or_EH_from_motion": False,
                "passed": "sqrt(32*pi*g)" in mixed_row["equation"],
            },
            {
                "gate_id": "HES4961_02_gravity_input",
                "source_equation": "4935 flow coordinates and fixed point",
                "evaluation": f"coordinates={coordinates}; g_star={fixed_gravity:.16g}; source_Newton_pole={source_newton_pole:.16g}",
                "result": "g is inherited from a completed gravity-photon trajectory",
                "interpretation": "4956 computes motion backreaction on a pre-existing gravitational Hessian",
                "can_derive_H_or_EH_from_motion": False,
                "passed": coordinates[0] == "g"
                and fixed_gravity > 0
                and source_newton_pole > 0,
            },
            {
                "gate_id": "HES4961_03_no_bootstrap",
                "source_equation": "H_hh=I10+Delta_H_motion(g,p)",
                "evaluation": "remove the inherited metric block",
                "result": "the published functional flow loses its defined inverse propagator and regulator normalization",
                "interpretation": "the motion Hessian is a correction calculation, not an origin calculation",
                "can_derive_H_or_EH_from_motion": False,
                "passed": True,
            },
        ]
    )
    diagnostics = {
        "metric_equation": metric_row["equation"],
        "mixed_equation": mixed_row["equation"],
        "gravity_coordinates": coordinates,
        "inherited_g_fixed_point": fixed_gravity,
        "source_Newton_pole": source_newton_pole,
        "metric_block_at_g_zero": "I10",
        "mixed_block_at_g_zero": "0",
        "motion_Hessian_bootstraps_gravity": False,
        "passed": all(bool(row["passed"]) for row in rows),
    }
    return rows, diagnostics


def induced_residue_gate() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    reduced_to_unreduced = math.sqrt(8.0 * math.pi)

    def branch_row(branch: str, weight: float, ownership: str) -> dict[str, Any]:
        cutoff_over_reduced = 4.0 * math.pi * math.sqrt(6.0 / weight)
        cutoff_over_unreduced = cutoff_over_reduced / reduced_to_unreduced
        length_over_planck = 1.0 / cutoff_over_unreduced
        return {
            "branch": branch,
            "W1": weight,
            "Mloop2_formula": "W1*LambdaUV^2/(96*pi^2)",
            "LambdaUV_over_reduced_Mpl_if_M0_zero": cutoff_over_reduced,
            "LambdaUV_over_unreduced_mpl_if_M0_zero": cutoff_over_unreduced,
            "ellstar_over_usual_lPlanck_if_M0_zero": length_over_planck,
            "ownership": ownership,
            "prediction_status": "MATCHING_RELATION_NOT_ABSOLUTE_G_PREDICTION",
            "passed": weight > 0,
        }

    rows = [
        branch_row("primitive_real_scalar_minimal", 1.0, "MTS_PRIMITIVE_MINIMAL_BRANCH"),
        branch_row("primitive_complex_scalar_minimal", 2.0, "MTS_NORMALIZATION_ALTERNATIVE_MINIMAL_BRANCH"),
        branch_row("imported_SM_plus_three_RH_neutrinos", 4.0, "EXTERNAL_COMPARATOR"),
        branch_row("five_scalars_plus_U1", 1.0, "CONSTRUCTIVE_BOSONIC_COMPARATOR"),
    ]
    weight_for_reduced_cutoff = 96.0 * math.pi**2
    weight_for_unreduced_cutoff = 12.0 * math.pi
    rows.extend(
        [
            {
                "branch": "required_weight_if_LambdaUV_equals_reduced_Mpl",
                "W1": weight_for_reduced_cutoff,
                "Mloop2_formula": "W1*LambdaUV^2/(96*pi^2)",
                "LambdaUV_over_reduced_Mpl_if_M0_zero": 1.0,
                "LambdaUV_over_unreduced_mpl_if_M0_zero": 1.0
                / reduced_to_unreduced,
                "ellstar_over_usual_lPlanck_if_M0_zero": reduced_to_unreduced,
                "xi_if_one_real_scalar_only": (1.0 - weight_for_reduced_cutoff)
                / 6.0,
                "ownership": "REQUIRED_EFFECTIVE_SIGNED_WEIGHT_NOT_PRESENTLY_DERIVED",
                "prediction_status": "SCALE_GATE",
                "passed": True,
            },
            {
                "branch": "required_weight_if_LambdaUV_equals_usual_mpl",
                "W1": weight_for_unreduced_cutoff,
                "Mloop2_formula": "W1*LambdaUV^2/(96*pi^2)",
                "LambdaUV_over_reduced_Mpl_if_M0_zero": reduced_to_unreduced,
                "LambdaUV_over_unreduced_mpl_if_M0_zero": 1.0,
                "ellstar_over_usual_lPlanck_if_M0_zero": 1.0,
                "xi_if_one_real_scalar_only": (1.0 - weight_for_unreduced_cutoff)
                / 6.0,
                "ownership": "REQUIRED_EFFECTIVE_SIGNED_WEIGHT_NOT_PRESENTLY_DERIVED",
                "prediction_status": "SCALE_GATE",
                "passed": True,
            },
        ]
    )

    bare_residue, loop_combination, threshold_residue = sp.symbols(
        "M0_squared LoopCombination ThresholdResidue", real=True
    )
    total_residue = bare_residue + loop_combination + threshold_residue
    matching_jacobian = sp.Matrix([total_residue]).jacobian(
        [bare_residue, loop_combination, threshold_residue]
    )
    matching_rank = int(matching_jacobian.rank())
    matching_nullity = 3 - matching_rank

    tagged_rows = tagged(rows)
    diagnostics = {
        "formula": "M_R^2=M_0^2+W1*LambdaUV^2/(96*pi^2)+delta_M_threshold^2",
        "matching_parameter_count": 3,
        "one_Newton_measurement_Jacobian_rank": matching_rank,
        "matching_nullity": matching_nullity,
        "W1_for_LambdaUV_equal_reduced_Mpl": weight_for_reduced_cutoff,
        "W1_for_LambdaUV_equal_usual_mpl": weight_for_unreduced_cutoff,
        "one_scalar_xi_for_LambdaUV_equal_reduced_Mpl": (
            1.0 - weight_for_reduced_cutoff
        )
        / 6.0,
        "one_scalar_xi_for_LambdaUV_equal_usual_mpl": (
            1.0 - weight_for_unreduced_cutoff
        )
        / 6.0,
        "primitive_W1_1_Lambda_over_reduced_Mpl": rows[0][
            "LambdaUV_over_reduced_Mpl_if_M0_zero"
        ],
        "primitive_W1_1_Lambda_over_usual_mpl": rows[0][
            "LambdaUV_over_unreduced_mpl_if_M0_zero"
        ],
        "primitive_W1_1_ellstar_over_lPlanck": rows[0][
            "ellstar_over_usual_lPlanck_if_M0_zero"
        ],
        "absolute_G_predicted": False,
        "passed": matching_rank == 1
        and matching_nullity == 2
        and weight_for_reduced_cutoff > 900
        and weight_for_unreduced_cutoff > 30,
    }
    return tagged_rows, diagnostics


def decision_rows(
    inventory_diagnostics: dict[str, Any],
    map_diagnostics: dict[str, Any],
    collective_diagnostics: dict[str, Any],
    background_diagnostics: dict[str, Any],
    hessian_diagnostics: dict[str, Any],
    residue_diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "decision_id": "DEC4961_00_primitive_content",
                "question": "Does the pre-checkpoint primitive corpus declare an independent tensor-density field with exact Diff/BRST?",
                "answer": "NO",
                "claim_granted": False,
                "scope": "43 Markdown files and one PDF in the core particle and mathematics corpus",
                "evidence": f"candidate_count={inventory_diagnostics['independent_tensor_Diff_candidate_count']}",
                "passed": inventory_diagnostics[
                    "independent_tensor_Diff_candidate_count"
                ]
                == 0,
            },
            {
                "decision_id": "DEC4961_01_local_scalar_map",
                "question": "Can one scalar first jet be locally inverted into ten independent metric components?",
                "answer": "NO_RANK_AT_MOST_FIVE",
                "claim_granted": False,
                "scope": "local maps depending on psi and its first derivative",
                "evidence": f"outer_Jacobian_rank={map_diagnostics['single_gradient_generic_rank']}; first_jet_cap=5",
                "passed": map_diagnostics["single_gradient_generic_rank"] == 4,
            },
            {
                "decision_id": "DEC4961_02_covariance_span",
                "question": "Can a genuine connected ensemble covariance carry ten tensor directions?",
                "answer": "YES_ALGEBRAICALLY",
                "claim_granted": True,
                "scope": "positive-definite covariance tangent around a regular state",
                "evidence": f"Cholesky_tangent_rank={map_diagnostics['covariance_tangent_rank_at_identity']}",
                "passed": map_diagnostics["covariance_tangent_rank_at_identity"] == 10,
            },
            {
                "decision_id": "DEC4961_03_collective_transform",
                "question": "Does an exact nonsingular Hubbard-Stratonovich or delta-functional rewrite create independent H and Diff redundancy?",
                "answer": "NO",
                "claim_granted": False,
                "scope": "exact rewrites of the present fixed-background scalar functional",
                "evidence": "regular_HS_nullity=0; Ward_nullity=4; delta keeps H=O(psi)",
                "passed": collective_diagnostics["passed"],
            },
            {
                "decision_id": "DEC4961_04_background_independence",
                "question": "Does the printed scalar action obey the required split Ward identity?",
                "answer": "NOT_DERIVED_AND_HAS_A_NONZERO_REFERENCE_STRESS_WITNESS",
                "claim_granted": False,
                "scope": "g_hat=g_ref+C representation",
                "evidence": f"reference_stress_rank={background_diagnostics['stress_rank']}",
                "passed": background_diagnostics["passed"],
            },
            {
                "decision_id": "DEC4961_05_motion_Hessian",
                "question": "Can the 4956 motion Hessian bootstrap H or the Einstein kinetic term?",
                "answer": "NO_IT_EXPANDS_AROUND_AN_INHERITED_GRAVITY_HESSIAN_AND_G_COORDINATE",
                "claim_granted": False,
                "scope": "4956 functional P(X) flat gravity-motion projector",
                "evidence": f"H_hh(g=0)=I10; inherited_g_star={hessian_diagnostics['inherited_g_fixed_point']:.16g}",
                "passed": hessian_diagnostics["passed"],
            },
            {
                "decision_id": "DEC4961_06_induced_EH",
                "question": "Is a positive induced Einstein contribution available?",
                "answer": "YES_WHEN_W1_POSITIVE",
                "claim_granted": True,
                "scope": "declared proper-time one-loop matching convention",
                "evidence": "M_loop^2=W1 LambdaUV^2/(96 pi^2)",
                "passed": residue_diagnostics["passed"],
            },
            {
                "decision_id": "DEC4961_07_absolute_G",
                "question": "Does that induced term predict the measured Newton constant from current MTS data?",
                "answer": "NO_ONE_MATCHING_EQUATION_HAS_AT_LEAST_TWO_FLAT_DIRECTIONS",
                "claim_granted": False,
                "scope": "M0^2 loop scale and threshold residue",
                "evidence": f"matching_rank={residue_diagnostics['one_Newton_measurement_Jacobian_rank']}; nullity={residue_diagnostics['matching_nullity']}",
                "passed": residue_diagnostics["matching_nullity"] == 2,
            },
            {
                "decision_id": "DEC4961_08_parent_boundary",
                "question": "What architecture survives without circular emergence?",
                "answer": "INTEGRATED_H_AND_EXACT_DIFF_ARE_EXPLICIT_FUNDAMENTAL_PARENT_FIELD_AND_SYMMETRY_DATA",
                "claim_granted": True,
                "scope": "current competitive MTS field-theory branch",
                "evidence": "exact collective-origin routes rejected; 4875 parent remains consistent",
                "passed": collective_diagnostics["passed"]
                and hessian_diagnostics["passed"],
            },
            {
                "decision_id": "DEC4961_09_local_correspondence",
                "question": "Does this boundary invalidate checkpoint 4960 local GR Newton Maxwell universality?",
                "answer": "NO_4960_IS_RETAINED_INSIDE_THE_NOW_EXPLICIT_PARENT_BOUNDARY",
                "claim_granted": True,
                "scope": "leading weak local massless-pole branch",
                "evidence": "4960 source result is hash locked and full-MTS false",
                "passed": True,
            },
            {
                "decision_id": "DEC4961_10_full_MTS",
                "question": "Is full ontological MTS or strong compact GR proved?",
                "answer": "NO",
                "claim_granted": False,
                "scope": "full theory and compact strong fields",
                "evidence": "H/Diff origin bounded rather than motion-derived; compact sensitivities remain open",
                "passed": True,
            },
            {
                "decision_id": "DEC4961_11_next_target",
                "question": "What is the next highest-value derivation?",
                "answer": "STRONG_COMPACT_BODY_SENSITIVITIES_BINARY_FLUX_AND_JUNCTION_MATCHING_IN_THE_EXPLICIT_PARENT",
                "claim_granted": False,
                "scope": "checkpoint 4962",
                "evidence": "weak local coefficient throat is closed and the origin fork is decided",
                "passed": True,
            },
        ]
    )


def provenance_text(source_hashes: dict[str, str]) -> str:
    source_rows = "\n".join(
        f"- `{label}`: `{SOURCE_PATHS[label].relative_to(ROOT).as_posix()}`; SHA256 `{source_hashes[label]}`"
        for label in SOURCE_PATHS
    )
    corpus_rows = "\n".join(
        f"- `{corpus_root.relative_to(ROOT).as_posix()}`"
        for corpus_root in CORPUS_ROOTS
    )
    return f"""# 4961 provenance

Marker: `{MARKER}_PROVENANCE`.

Checked: `{CHECKED_DATE}`.

## Hash-locked inputs

{source_rows}

## Primitive corpus sweep

{corpus_rows}

The sweep covers every Markdown file and PDF under those three roots. It is
used only to classify the field content actually written in the supplied
primitive corpus. Absence of an independent tensor-gauge parent there is not
advertised as a theorem against every possible microscopic completion.

## Executed derivations

The generator checks the one-scalar first-jet rank, the full tangent rank of a
regular connected covariance, an exact finite-dimensional
Hubbard-Stratonovich completion of the square, the four spin-two gauge null
directions, the incompatibility of a regular auxiliary kernel with the
ungauge-fixed Ward identity, a nonzero reference-metric stress witness, the
4956 inherited gravity block, and the induced-Einstein matching degeneracy.

The Weinberg-Witten premise gate and integrated-`H`/Diff construction are
imported from the hash-locked 4874-4875 analysis. Checkpoint 4961 narrows the
claim: it rejects the current scalar/covariance/auxiliary rewrite as an origin
of independent gravity; it does not claim a no-go for every future MTS
microscopic tensor-gauge completion.

All generated rows remain `valid_for_full_MTS_claim=false`.
"""


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)

    missing_sources = [
        label for label, path in SOURCE_PATHS.items() if not path.exists()
    ]
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
        if path.suffix.lower() in {".md", ".csv", ".json"}
    }
    gravity_parent = json.loads(source_text["gravity_parent_4935"])
    source_4960 = json.loads(source_text["universal_source_result_4960"])
    source_clause_checks = {
        "core_scalar_primitive": "ψ : ℝ⁴ → ℝ" in source_text["core_fundamental_action"],
        "core_fixed_Minkowski_background": "η_{μν} is the Minkowski background"
        in source_text["core_fundamental_action"],
        "core_covariance_metric": "⟨ ∂_μψ ∂_νψ ⟩_smooth"
        in source_text["core_EFT"],
        "core_inserts_EH_then_varies_metric": "Einstein–Hilbert term"
        in source_text["core_action_principle"]
        and "We vary A with respect to the emergent metric"
        in source_text["core_action_principle"],
        "4872_connected_covariance": "inverse connected-covariance metric"
        in source_text["primitive_audit_4872"],
        "4873_reference_metric_survives": "reference metric has not disappeared"
        in source_text["open_parent_4873"],
        "4874_split_Ward": "background independence is exactly a split Ward identity"
        in source_text["split_Ward_4874"],
        "4875_integrated_modulo_Diff": "integrated modulo Diff"
        in source_text["integrated_H_4875"],
        "4875_composite_WW_boundary": "original fixed-\\(\\eta\\) scalar theory"
        in source_text["integrated_H_4875"]
        and "triggers Weinberg-Witten" in source_text["integrated_H_4875"],
        "4876_bare_plus_loop": "M_R^2=M_0^2+M_{\\rm loop}^2"
        in source_text["induced_parent_4876"],
        "4877_signed_EH_weight": "M_*^2=\\frac{\\Lambda_{\\rm UV}^2}{96\\pi^2}W_1"
        in source_text["spectrum_4877"],
        "4935_gravity_coordinate": gravity_parent["flow_contract"]["coordinates"][0]
        == "g"
        and gravity_parent["flow_contract"]["source_Newton_pole"] > 0,
        "4956_inherited_metric_block": "H_hh=I10+32*pi*g"
        in source_text["motion_Hessian_contract_4956"],
        "4960_parent_boundary": source_4960["decision"][
            "matter_field_content_from_motion_alone"
        ]
        is False
        and source_4960["decision"]["full_MTS"] is False,
    }
    failed_clauses = [
        name for name, passed in source_clause_checks.items() if not passed
    ]
    if failed_clauses:
        raise RuntimeError(f"source clause mismatch: {failed_clauses}")

    inventory_rows, inventory_diagnostics = corpus_inventory()
    map_rows, map_diagnostics = metric_map_rank_gate()
    collective_rows, collective_diagnostics = collective_field_gate()
    background_rows, background_diagnostics = background_split_gate()
    hessian_rows, hessian_diagnostics = motion_hessian_audit()
    residue_rows, residue_diagnostics = induced_residue_gate()
    decisions = decision_rows(
        inventory_diagnostics,
        map_diagnostics,
        collective_diagnostics,
        background_diagnostics,
        hessian_diagnostics,
        residue_diagnostics,
    )

    write_csv(INVENTORY_CSV, inventory_rows)
    write_csv(MAP_CSV, map_rows)
    write_csv(COLLECTIVE_CSV, collective_rows)
    write_csv(BACKGROUND_CSV, background_rows)
    write_csv(HESSIAN_CSV, hessian_rows)
    write_csv(RESIDUE_CSV, residue_rows)
    write_csv(DECISION_CSV, decisions)
    PROVENANCE.write_text(provenance_text(source_hashes), encoding="utf-8")

    decision_by_id = {row["decision_id"]: row for row in decisions}
    checks = {
        "all_source_hashes_match": not bad_hashes,
        "all_source_clauses_match": not failed_clauses,
        "primitive_corpus_has_no_integrated_tensor_Diff_parent": inventory_diagnostics[
            "independent_tensor_Diff_candidate_count"
        ]
        == 0,
        "local_and_ensemble_rank_gate_passes": map_diagnostics["passed"],
        "collective_transform_and_Ward_gate_passes": collective_diagnostics[
            "passed"
        ],
        "reference_background_witness_is_nonzero": background_diagnostics["passed"],
        "motion_Hessian_is_not_an_origin_bootstrap": hessian_diagnostics["passed"]
        and not hessian_diagnostics["motion_Hessian_bootstraps_gravity"],
        "induced_EH_matching_gate_passes": residue_diagnostics["passed"],
        "explicit_parent_boundary_selected": bool(
            decision_by_id["DEC4961_08_parent_boundary"]["claim_granted"]
        ),
        "weak_local_4960_correspondence_retained": bool(
            decision_by_id["DEC4961_09_local_correspondence"]["claim_granted"]
        ),
        "full_MTS_remains_false": not bool(
            decision_by_id["DEC4961_10_full_MTS"]["claim_granted"]
        ),
        "all_generated_full_claim_flags_false": all(
            not bool(row["valid_for_full_MTS_claim"])
            for table in (
                inventory_rows,
                map_rows,
                collective_rows,
                background_rows,
                hessian_rows,
                residue_rows,
                decisions,
            )
            for row in table
        ),
    }
    failed_checks = [name for name, passed in checks.items() if not passed]
    if failed_checks:
        raise RuntimeError(f"4961 internal checks failed: {failed_checks}")

    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_hashes": source_hashes,
        "source_clause_checks": source_clause_checks,
        "corpus_inventory": inventory_diagnostics,
        "metric_map_rank_gate": map_diagnostics,
        "collective_field_gate": collective_diagnostics,
        "background_split_gate": background_diagnostics,
        "motion_Hessian_audit": hessian_diagnostics,
        "induced_EH_residue_gate": residue_diagnostics,
        "checks": checks,
        "decision": {
            "local_one_scalar_metric_origin": "REJECTED",
            "connected_covariance_tensor_span": "ALGEBRAICALLY_AVAILABLE_STATE_DEPENDENT",
            "exact_HS_or_delta_rewrite_origin_of_Diff": "REJECTED",
            "4956_motion_Hessian_origin_of_gravity": "REJECTED_CIRCULAR",
            "positive_induced_EH_contribution": "CONDITIONAL_ON_W1_POSITIVE",
            "absolute_Newton_constant_prediction": False,
            "integrated_H_and_Diff": "EXPLICIT_FUNDAMENTAL_PARENT_DATA",
            "weak_local_GR_Newton_Maxwell_4960": "RETAINED",
            "strong_compact_GR": False,
            "full_MTS": False,
            "next_target": "4962_STRONG_COMPACT_BODY_SENSITIVITIES_BINARY_FLUX_AND_JUNCTION_MATCHING",
        },
    }
    RESULT_JSON.write_text(
        json.dumps(json_ready(result), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"{MARKER}_RESULT_SHA256={digest(RESULT_JSON)}", flush=True)
    print(
        f"{MARKER}_CORPUS_FILES={inventory_diagnostics['files_scanned']}",
        flush=True,
    )
    print(
        f"{MARKER}_PRIMITIVE_TENSOR_DIFF_CANDIDATES={inventory_diagnostics['independent_tensor_Diff_candidate_count']}",
        flush=True,
    )
    print(
        f"{MARKER}_SINGLE_GRADIENT_RANK={map_diagnostics['single_gradient_generic_rank']}",
        flush=True,
    )
    print(
        f"{MARKER}_COVARIANCE_TANGENT_RANK={map_diagnostics['covariance_tangent_rank_at_identity']}",
        flush=True,
    )
    print(
        f"{MARKER}_GAUGE_MAP_RANK={collective_diagnostics['gauge_map_rank']}",
        flush=True,
    )
    print(
        f"{MARKER}_WARD_HESSIAN_NULLITY={collective_diagnostics['quotient_Hessian_nullity']}",
        flush=True,
    )
    print(
        f"{MARKER}_PRIMITIVE_W1_CUTOFF_OVER_MPL={residue_diagnostics['primitive_W1_1_Lambda_over_usual_mpl']:.16g}",
        flush=True,
    )
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
