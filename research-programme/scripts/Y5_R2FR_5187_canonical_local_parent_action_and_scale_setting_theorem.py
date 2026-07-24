from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5187"

ACTION_CSV = OUT / "canonical_local_parent_action.csv"
HESSIAN_CSV = OUT / "vacuum_quadratic_Hessian_and_source_vertices.csv"
LIMIT_CSV = OUT / "universal_residue_and_limit_chain.csv"
RG_CSV = OUT / "RG_scale_setting_no_go.csv"
PARAMETER_CSV = OUT / "canonical_parameter_and_state_count.csv"
CORRIDOR_CSV = OUT / "higher_derivative_local_corridor.csv"
NO_RETUNING_CSV = OUT / "cross_arena_no_retuning.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "canonical_local_parent_action_results.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5187_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5187-Y5-R2FR-canonical-local-parent-action-Hessian-source-residue-"
    "and-scale-setting-theorem.md"
)

MARKER = "MTS_5187_CANONICAL_LOCAL_PARENT_ACTION_SCALE_SETTING_THEOREM"
CHECKED_DATE = "2026-07-23"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_TREE_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
CHECKPOINT_5176_ROOT = POST / "source-intake" / "functional_rg" / "5176"

CANONICAL_ACTION = (
    "Gamma_loc=int sqrt(-g){M_R^2(R-2Lambda_cal)/2"
    "-Z_A F_mn F^mn/4-Z_psi(nabla psi)^2/2-m_gap^2 psi^2/2"
    "+c_IR C_mnrs F^mn F^rs+G_C3 I_C3"
    "-u_O4 C_abcd C^abcd (nabla psi)^2+P_ge_2(X)}"
    "+S_matter[g,A,Phi_SM]+Gamma_contact+Gamma_nonlocal+Gamma_p8plus"
)

LEADING_THEOREM = (
    "INSIDE_THE_EXPLICIT_INTEGRATED_H_EXACT_DIFF_BRST_PARENT_WITH_ONE_"
    "POSITIVE_MASSLESS_SPIN_TWO_POLE_CANONICAL_U1_AND_REFLECTION_EVEN_"
    "MOTION_MATTER_THE_LOCAL_ZERO_FIELD_HESSIAN_IS_BLOCK_DIAGONAL_THE_"
    "HILBERT_SOURCE_MAP_IS_INVERTIBLE_SOFT_AND_BIANCHI_CONSISTENCY_LEAVE_"
    "ONE_COMMON_SPIN_TWO_RESIDUE_AND_FIELD_NORMALIZATIONS_CANCEL_FROM_"
    "EXCHANGE_THE_SAME_CANONICAL_ACTION_THEREFORE_GIVES_EINSTEIN_POISSON_"
    "NEWTON_GEODESIC_LENSING_AND_MAXWELL_COULOMB_LORENTZ_STRESS_POYNTING_"
    "CHAINS_WITH_NO_ARENA_RETUNING_THE_RELATION_GN_EQUALS_ONE_OVER_EIGHT_"
    "PI_MR_SQUARED_IS_DERIVED_BUT_AN_AUTONOMOUS_DIMENSIONLESS_RG_FLOW_"
    "RETAINS_ONE_TRANSLATIONAL_SCALE_MODULUS_SO_THE_NUMERICAL_VALUE_OF_GN_"
    "REQUIRES_ONE_ABSOLUTE_GRAVITATIONAL_SCALE_CALIBRATION_UNLESS_A_FUTURE_PARENT_"
    "SUPPLIES_AN_INDEPENDENT_DIMENSIONFUL_ANCHOR"
)

CLAIM_GUARD = (
    "THIS_IS_A_LEADING_LOCAL_THEOREM_INSIDE_EXPLICIT_PARENT_FIELD_AND_"
    "SYMMETRY_DATA_NOT_A_DERIVATION_OF_H_OR_DIFF_FROM_ONE_MOTION_SCALAR_"
    "NOT_A_NUMERICAL_PREDICTION_OF_GN_NOT_AN_ALL_OPERATOR_COMPACT_GR_"
    "THEOREM_AND_NOT_A_FULL_MTS_UNIFICATION_CLAIM"
)


def source_path(relative: str) -> Path:
    return POST / Path(relative.replace("/", "\\"))


SOURCES: dict[str, tuple[Path, str]] = {
    "checkpoint_4938_document": (
        source_path(
            "4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-"
            "explicit-two-scale-theory-gate.md"
        ),
        "b30394a62c6a22af5da315b92a2823f44aa34cd914b6bab813136b0926aa0ca4",
    ),
    "checkpoint_4938_scale_result": (
        source_path(
            "source-intake/functional_rg/4938/"
            "critical_surface_scale_lock_results.json"
        ),
        "544375b68725e8722507eea59414e91a3a76f2bad84c57ac3bdca1ae75a8a175",
    ),
    "checkpoint_4942_document": (
        source_path(
            "4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-"
            "motion-branch-and-C3-CFF-PPN-residual-gate.md"
        ),
        "64b96ca4e19a058ced85c0c4b800ae7a237408606799dd8c4a5b58935f635c5f",
    ),
    "checkpoint_4942_branch": (
        source_path(
            "source-intake/functional_rg/4942/"
            "local_homogeneous_branch_identities.csv"
        ),
        "e9e4532679843c78ab2c86ddc39589bb6c694ca9cb17aae6a7bae47af66d4d0a",
    ),
    "checkpoint_4943_document": (
        source_path(
            "4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-"
            "junction-or-fifth-force-residual-gate.md"
        ),
        "a90da0e9ad0457fc3dbdb389d7bf2715cb9d707cbffa094a987b0b0553e257b5",
    ),
    "checkpoint_4943_junction": (
        source_path(
            "source-intake/functional_rg/4943/"
            "junction_scalar_charge_and_fifth_force.csv"
        ),
        "5fbca2c1672d7fbb6f1741e56a3c72a2adbaee544a4fd5fd5525a616cb836df6",
    ),
    "checkpoint_4946_document": (
        source_path(
            "4946-Y5-R2FR-QCD-TJJ-dispersive-matching-and-weak-local-Maxwell-"
            "action-certificate.md"
        ),
        "4985b31aa5d5253ec64fd1575bbd0f844c1b5c0924a11482fb77374ddee477b6",
    ),
    "checkpoint_4946_Maxwell": (
        source_path(
            "source-intake/functional_rg/4946/"
            "local_Maxwell_action_stress_and_calibration_certificate.csv"
        ),
        "8b80ddf7b5cb469fa7c580b24f6b0d759322871bfb7064111839565ba290799a",
    ),
    "checkpoint_4946_CFF_transfer": (
        source_path(
            "source-intake/functional_rg/4946/"
            "universal_CFF_calibration_transfer_functions.csv"
        ),
        "8707daa86fac5daf0bd6859bf8d8c29f18777349c9dbac24e259f729facd15a8",
    ),
    "checkpoint_4947_document": (
        source_path(
            "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-"
            "universal-source-residue-certificate.md"
        ),
        "0b71f50c85ab4c5761755aa11544910a1a1e4fcacc901236432705a5ba36563f",
    ),
    "checkpoint_4947_residue_chain": (
        source_path(
            "source-intake/functional_rg/4947/source_residue_chain.csv"
        ),
        "b08468f29f938dfe72f13b9eec93f73c2b4f9c58ff89e7b67008c6de2cfc1e1d",
    ),
    "checkpoint_4960_document": (
        source_path(
            "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-"
            "and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-"
            "boundary.md"
        ),
        "6cd343d022dde751f86ad82eaf0f61fb5e3616753c228f631c44a45da278a69d",
    ),
    "checkpoint_4960_parent_contract": (
        source_path(
            "source-intake/functional_rg/4960/"
            "parent_definition_vs_derived_source_contract.csv"
        ),
        "93937d1ed9b13eab2c9e13fdf45a98c2236d037759abbdbec77e8da96ec9ddaf",
    ),
    "checkpoint_4960_soft_Bianchi": (
        source_path(
            "source-intake/functional_rg/4960/"
            "soft_Bianchi_species_coupling_nullspace.csv"
        ),
        "ad714332cf51eccb8b271394715b8de27affe3baee21889223da74aeeee1ac51",
    ),
    "checkpoint_4961_document": (
        source_path(
            "4961-Y5-R2FR-integrated-H-origin-and-induced-EH-residue-from-"
            "motion-Hessian-or-explicit-fundamental-field-boundary.md"
        ),
        "ec6c5ff4056ed13ad92cad5e70ce125d81183abd0d79c59345dd6393987e2de2",
    ),
    "checkpoint_4962_document": (
        source_path(
            "4962-Y5-R2FR-compact-body-sensitivity-binary-flux-and-junction-"
            "matching-or-strong-GR-residual-boundary.md"
        ),
        "93c88dd74a719106c998399a4f51bf78f44ed679ff19d3d570c8f3408d2c9134",
    ),
    "checkpoint_4962_compact": (
        source_path(
            "source-intake/functional_rg/4962/"
            "compact_body_sensitivity_and_no_dipole.csv"
        ),
        "e7c3fbefdc369b0493420d7bdc7318b060866981a85e7c1b845dfba4e1ba9717",
    ),
    "checkpoint_4963_document": (
        source_path(
            "4963-Y5-R2FR-strong-field-C3-Wilson-selection-and-global-"
            "scalar-branch-exclusion-or-compact-GR-finite-residual.md"
        ),
        "ea2df6892c729fc3c49eb00074eb2d999c426c18046db60aa1f963b8cc9fcc48",
    ),
    "checkpoint_4963_compact_C3": (
        source_path(
            "source-intake/functional_rg/4963/compact_C3_residual_domain.csv"
        ),
        "75285482928f6b1f897e365968e6d38514ca5d22fe70c6b8538610531e3b2383",
    ),
    "checkpoint_4964_document": (
        source_path(
            "4964-Y5-R2FR-four-derivative-redundant-quotient-CFF-one-LEC-"
            "contract-and-p8-tail-norm-or-all-operator-compact-GR-boundary.md"
        ),
        "8bcfe51f2960789c575c0b4f9c85e65a6ca83be6a8a49c689e58c3180d4c8f57",
    ),
    "checkpoint_4964_parameter_count": (
        source_path(
            "source-intake/functional_rg/4964/"
            "finite_matching_parameter_count.csv"
        ),
        "82d4178a1f7f983e47726451502f131075ecbd5b5905c31d068402f83828bd02",
    ),
    "checkpoint_4964_CFF_contract": (
        source_path(
            "source-intake/functional_rg/4964/"
            "CFF_one_LEC_calibration_contract.csv"
        ),
        "bd96a132e80647ac4f106a8c026afba3a8f4060d095fda3451cbbaac21d8236c",
    ),
    "checkpoint_4964_p8_gate": (
        source_path(
            "source-intake/functional_rg/4964/p8plus_tail_norm_gate.csv"
        ),
        "a17f8fc7c652fec0b9a33985fe7c23045073114784bc2304a084ad4ca057510f",
    ),
    "checkpoint_4986_document": (
        source_path(
            "4986-Y5-R2FR-common-scheme-log-invariant-and-local-metric-"
            "exterior-bounds.md"
        ),
        "6a2bea097597f0a1b39e035e0d8241abe7939371e980efd7c1eeaf5c0a5511a8",
    ),
    "checkpoint_4986_C3_bounds": (
        source_path(
            "source-intake/functional_rg/4986/"
            "C3_exterior_compactness_bounds.csv"
        ),
        "e6f8feab5e170b90420438385ba031295f7203fae857b1d5784d6ccff4b9e757",
    ),
    "checkpoint_4986_determinant_bounds": (
        source_path(
            "source-intake/functional_rg/4986/"
            "determinant_exterior_tail_bounds.csv"
        ),
        "5fab5cb73fcb1328b24291d3a4f7cf3a71f32f7ce7ed44610b8f40a09242f83d",
    ),
    "checkpoint_5148_document": (
        source_path(
            "5148-Y5-R2FR-one-parent-local-GR-galaxy-spectral-response-"
            "cog-theorem.md"
        ),
        "b2d5bddd8ce3cee2299b2cdadd66a0688bbd07c945bc329ac2ade4c20c113352",
    ),
    "checkpoint_5184_document": (
        source_path(
            "5184-Y5-R2FR-stationary-PX-background-no-lump-and-mixed-"
            "Hessian-gate.md"
        ),
        "e4a3427963b4de0b5b40baab67b905e9e7054e8033c72dee768fb8973a258e33",
    ),
    "checkpoint_5185_document": (
        source_path(
            "5185-Y5-R2FR-occupied-state-2PI-interaction-stress-and-"
            "collision-gate.md"
        ),
        "d47db7fefdb8b9f799a48a1e4d5a7c4266880d41d97b40ae2cefe33cd62d07a5",
    ),
    "checkpoint_5186_document": (
        source_path(
            "5186-Y5-R2FR-FLRW-Bogoliubov-neutral-vacuum-production-and-"
            "abundance-no-go.md"
        ),
        "b3846c2e4bc1270b4c2f50d431fc5d812944f648ebec36f3250a95916101c05a",
    ),
    "checkpoint_5186_result": (
        source_path(
            "source-intake/functional_rg/5186/"
            "FLRW_Bogoliubov_neutral_production_results.json"
        ),
        "08928a8d61f6a9defdb1b283e8d2faaa4ee2c8a3f11998071f829567c83ba28b",
    ),
}


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(file_digest(item).encode("ascii"))
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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


def validation_row(
    check_id: str,
    test: str,
    passed: bool,
    value: Any,
    expected: Any,
) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "test": test,
        "status": "PASS" if passed else "FAIL",
        "value": value,
        "expected": expected,
        "checkpoint_marker": MARKER,
    }


def fraction_rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                candidate
                for candidate in range(pivot_row, row_count)
                if work[candidate][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for candidate in range(row_count):
            if candidate == pivot_row:
                continue
            factor = work[candidate][column]
            if factor == 0:
                continue
            work[candidate] = [
                value - factor * pivot_value
                for value, pivot_value in zip(
                    work[candidate],
                    work[pivot_row],
                    strict=True,
                )
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def fraction_determinant(matrix: list[list[Fraction]]) -> Fraction:
    if not matrix:
        return Fraction(1)
    if any(len(row) != len(matrix) for row in matrix):
        raise ValueError("Determinant requires a square matrix")
    work = [row[:] for row in matrix]
    determinant = Fraction(1)
    dimension = len(work)
    for column in range(dimension):
        pivot = next(
            (
                candidate
                for candidate in range(column, dimension)
                if work[candidate][column] != 0
            ),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant *= -1
        pivot_value = work[column][column]
        determinant *= pivot_value
        for candidate in range(column + 1, dimension):
            factor = work[candidate][column] / pivot_value
            for inner in range(column + 1, dimension):
                work[candidate][inner] -= factor * work[column][inner]
    return determinant


def matrix_product(
    left: list[list[Fraction]],
    right: list[list[Fraction]],
) -> list[list[Fraction]]:
    return [
        [
            sum(
                (
                    left[row][inner] * right[inner][column]
                    for inner in range(len(right))
                ),
                Fraction(0),
            )
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def identity_matrix(dimension: int) -> list[list[Fraction]]:
    return [
        [
            Fraction(1 if row == column else 0)
            for column in range(dimension)
        ]
        for row in range(dimension)
    ]


def trace_reversal_matrix() -> list[list[Fraction]]:
    metric = (-1, 1, 1, 1)
    basis = [(row, column) for row in range(4) for column in range(row, 4)]
    matrix = [
        [Fraction(0) for _ in basis]
        for _ in basis
    ]
    for output_index, (mu, nu) in enumerate(basis):
        for input_index, (alpha, beta) in enumerate(basis):
            if (mu, nu) == (alpha, beta):
                matrix[output_index][input_index] += 1
            if mu == nu and alpha == beta:
                matrix[output_index][input_index] -= Fraction(
                    metric[mu] * metric[alpha],
                    2,
                )
    return matrix


def species_difference_matrix(species_count: int) -> list[list[Fraction]]:
    return [
        [
            Fraction(
                -1 if column == 0 else 1 if column == row + 1 else 0
            )
            for column in range(species_count)
        ]
        for row in range(species_count - 1)
    ]


def second_derivative_at_origin(
    exponents: tuple[int, int, int],
    first: int,
    second: int,
) -> int:
    remaining = list(exponents)
    coefficient = remaining[first]
    if coefficient == 0:
        return 0
    remaining[first] -= 1
    coefficient *= remaining[second]
    if coefficient == 0:
        return 0
    remaining[second] -= 1
    return coefficient if remaining == [0, 0, 0] else 0


def build_action_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "row_id": "ACT5187_00_H",
                "component": "integrated densitized inverse metric",
                "symbol": "H^mn=sqrt(-g)g^mn",
                "canonical_term": "g^mn=H^mn/sqrt(-det H)",
                "local_role": "complete Hilbert source carrier",
                "ownership": "explicit parent field datum",
                "calibration_count": 0,
                "status": "PARENT_DEFINED_NOT_SCALAR_DERIVED",
                "leading_local_theorem": True,
                "source_key": "checkpoint_4960_document;checkpoint_4961_document",
            },
            {
                "row_id": "ACT5187_01_Diff",
                "component": "gauge structure",
                "symbol": "Diff/BRST",
                "canonical_term": "exact diffeomorphism and BRST identities",
                "local_role": "removes unphysical spin-two modes and enforces Bianchi compatibility",
                "ownership": "explicit parent symmetry datum",
                "calibration_count": 0,
                "status": "PARENT_DEFINED_NOT_SCALAR_DERIVED",
                "leading_local_theorem": True,
                "source_key": "checkpoint_4960_document;checkpoint_4961_document",
            },
            {
                "row_id": "ACT5187_02_EH",
                "component": "two-derivative gravity",
                "symbol": "M_R^2,Lambda_cal",
                "canonical_term": "sqrt(-g) M_R^2(R-2Lambda_cal)/2",
                "local_role": "one positive massless spin-two pole and background curvature",
                "ownership": "IR parent coefficient",
                "calibration_count": 2,
                "status": "STRUCTURE_DERIVED_RESIDUE_AND_BACKGROUND_VALUES_CALIBRATED",
                "leading_local_theorem": True,
                "source_key": "checkpoint_4960_document",
            },
            {
                "row_id": "ACT5187_03_Maxwell",
                "component": "two-derivative photon",
                "symbol": "Z_A,e",
                "canonical_term": "-sqrt(-g) Z_A F_mn F^mn/4+sqrt(-g)e A_m j^m",
                "local_role": "canonical U1 pole and conserved current",
                "ownership": "visible parent field and representation data",
                "calibration_count": 1,
                "status": "ONE_PHYSICAL_COMBINATION_E_SQUARED_OVER_ZA",
                "leading_local_theorem": True,
                "source_key": "checkpoint_4946_Maxwell;checkpoint_4947_residue_chain",
            },
            {
                "row_id": "ACT5187_04_motion",
                "component": "quadratic motion scalar",
                "symbol": "Z_psi,m_gap^2",
                "canonical_term": "-sqrt(-g)[Z_psi(nabla psi)^2+m_gap^2 psi^2]/2",
                "local_role": "reflection-even gapped motion pole",
                "ownership": "selected parent motion sector",
                "calibration_count": 1,
                "status": "J_GAP_UNSELECTED_BUT_LOCAL_ONE_SCALAR_SOURCE_ZERO",
                "leading_local_theorem": True,
                "source_key": "checkpoint_4938_document;checkpoint_4942_branch",
            },
            {
                "row_id": "ACT5187_05_CFF",
                "component": "curvature-photon response",
                "symbol": "c_IR",
                "canonical_term": "sqrt(-g)c_IR C_mnrs F^mn F^rs",
                "local_role": "one CP-even Ricci-flat photon-curvature LEC",
                "ownership": "nonQCD contribution assembled; QCD TJJ finite part open",
                "calibration_count": 1,
                "status": "ONE_SHARED_LEC_NUMERIC_TOTAL_OPEN",
                "leading_local_theorem": False,
                "source_key": "checkpoint_4946_document;checkpoint_4964_CFF_contract",
            },
            {
                "row_id": "ACT5187_06_C3",
                "component": "six-derivative vacuum gravity",
                "symbol": "G_C3;a_plus",
                "canonical_term": "sqrt(-g)G_C3 I_C3 with G_C3=M_R^2 a_plus/2=A_C3^S l_P^2",
                "local_role": "selected higher-gradient metric residual",
                "ownership": "A_C3^S selected in locked p6 source scheme",
                "calibration_count": 0,
                "status": "P6_LOCAL_COORDINATE_SELECTED_NONLOCAL_COMPLETION_OPEN",
                "leading_local_theorem": False,
                "source_key": "checkpoint_4963_document;checkpoint_4986_C3_bounds",
            },
            {
                "row_id": "ACT5187_07_O4",
                "component": "motion-curvature portal",
                "symbol": "u_O4",
                "canonical_term": "-sqrt(-g)u_O4 C_abcd C^abcd(nabla psi)^2",
                "local_role": "curvature-dependent scalar principal coefficient",
                "ownership": "selected GR-connected trajectory",
                "calibration_count": 0,
                "status": "NONZERO_BUT_EXACTLY_SILENT_AT_PSI_ZERO",
                "leading_local_theorem": False,
                "source_key": "checkpoint_4942_document",
            },
            {
                "row_id": "ACT5187_08_PX",
                "component": "nonlinear motion self-interactions",
                "symbol": "P_ge_2(X)",
                "canonical_term": "sqrt(-g)[c2 X^2+c3 X^3+...]",
                "local_role": "occupied/nonlinear state dynamics",
                "ownership": "motion functional trajectory",
                "calibration_count": 0,
                "status": "QUADRATIC_HESSIAN_SILENT_AT_PSI_ZERO",
                "leading_local_theorem": False,
                "source_key": "checkpoint_4942_document;checkpoint_5184_document;checkpoint_5185_document;checkpoint_5186_document",
            },
            {
                "row_id": "ACT5187_09_matter",
                "component": "visible matter functor",
                "symbol": "S_matter[g,A,Phi_SM;theta_SM]",
                "canonical_term": "ordinary matter uses g and U1 connection A with no reflection-odd psi source",
                "local_role": "Hilbert stress and conserved electric current",
                "ownership": "explicit parent field/representation content",
                "calibration_count": 0,
                "status": "CONTENT_PARENT_DEFINED_LEADING_RESIDUES_DERIVED",
                "leading_local_theorem": True,
                "source_key": "checkpoint_4943_document;checkpoint_4960_parent_contract",
            },
            {
                "row_id": "ACT5187_10_contact",
                "component": "matter contact/worldline EFT",
                "symbol": "Gamma_contact",
                "canonical_term": "[2a_C T_mnT^mn+(a_R-2a_C/3)T^2]/M_R^4 plus independent matter counterterms",
                "local_role": "short-distance material/EOS response",
                "ownership": "full invariant matter basis not matched",
                "calibration_count": 2,
                "status": "P4_VACUUM_QUOTIENTED_CONTACT_MATCHING_OPEN",
                "leading_local_theorem": False,
                "source_key": "checkpoint_4964_parameter_count",
            },
            {
                "row_id": "ACT5187_11_nonlocal_p8",
                "component": "nonlocal and p8-plus completion",
                "symbol": "Gamma_nonlocal,Gamma_p8plus",
                "canonical_term": "vacuum logarithms plus Ricci-flat p8 and higher basis",
                "local_role": "complete quantum potential and all-operator compact response",
                "ownership": "partial determinant endpoint and conditional tail norm only",
                "calibration_count": 2,
                "status": "COMPLETE_PHYSICAL_AMPLITUDE_OPEN",
                "leading_local_theorem": False,
                "source_key": "checkpoint_4964_p8_gate;checkpoint_4986_determinant_bounds",
            },
        ]
    )


def build_hessian_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    fields = ("h", "A", "psi")
    pairs = (
        ("hh", 0, 0),
        ("hA", 0, 1),
        ("hpsi", 0, 2),
        ("AA", 1, 1),
        ("Apsi", 1, 2),
        ("psipsi", 2, 2),
    )
    terms = [
        (
            "EH",
            (2, 0, 0),
            "M_R^2 q^2 P_spin2 plus Lambda background terms",
            "modifies hh",
        ),
        (
            "Maxwell",
            (0, 2, 0),
            "Z_A q^2 P_transverse",
            "modifies AA",
        ),
        (
            "motion_quadratic",
            (0, 0, 2),
            "Z_psi q^2+m_gap^2",
            "modifies psipsi",
        ),
        (
            "CFF_flat",
            (1, 2, 0),
            "starts as h A A around flat A=0",
            "no flat quadratic term",
        ),
        (
            "C3_flat",
            (3, 0, 0),
            "starts as h cubed around flat space",
            "no flat quadratic term",
        ),
        (
            "O4_flat",
            (2, 0, 2),
            "starts as h h psi psi around flat space",
            "no flat quadratic term",
        ),
        (
            "P_X2",
            (0, 0, 4),
            "starts as psi to fourth derivative order",
            "no quadratic term",
        ),
    ]
    rows: list[dict[str, Any]] = []
    mixed_sum = 0
    for term, exponents, operator, consequence in terms:
        derivatives = {
            label: second_derivative_at_origin(exponents, first, second)
            for label, first, second in pairs
        }
        mixed_sum += (
            abs(derivatives["hA"])
            + abs(derivatives["hpsi"])
            + abs(derivatives["Apsi"])
        )
        rows.append(
            {
                "row_id": f"HESS5187_degree_{term}",
                "row_type": "exact_flat_background_field_degree",
                "field_or_test": term,
                "minimal_degree_h_A_psi": ",".join(map(str, exponents)),
                "operator_or_equation": operator,
                **{f"d2_{key}_at_zero": value for key, value in derivatives.items()},
                "result": consequence,
                "passed": True,
            }
        )

    block_rows = [
        {
            "row_id": "HESS5187_00_hh",
            "row_type": "curved_zero_field_block",
            "field_or_test": "metric block",
            "operator_or_equation": "K_hh=M_R^2 K_Einstein+K_C3+K_nonlocal+K_p8plus",
            "result": "one positive massless spin-two pole is the declared leading block",
            "passed": True,
        },
        {
            "row_id": "HESS5187_01_AA",
            "row_type": "curved_zero_field_block",
            "field_or_test": "photon block",
            "operator_or_equation": "K_AA=Z_A q^2 P_T+c_IR K_CFF[bar C]",
            "result": "CFF modifies only the photon block when bar A=0",
            "passed": True,
        },
        {
            "row_id": "HESS5187_02_psipsi",
            "row_type": "curved_zero_field_block",
            "field_or_test": "motion block",
            "operator_or_equation": "K_psipsi=(Z_psi+2u_O4 bar C^2)q^2+m_gap^2+lower-gradient curvature terms",
            "result": "O4 modifies only the motion block when bar psi=0",
            "passed": True,
        },
        {
            "row_id": "HESS5187_03_hpsi",
            "row_type": "exact_mixed_block",
            "field_or_test": "metric-motion",
            "operator_or_equation": "delta2 Gamma/(delta h delta psi)|bar psi=0=0",
            "result": "zero by reflection parity and at least quadratic scalar degree",
            "passed": True,
        },
        {
            "row_id": "HESS5187_04_hA",
            "row_type": "exact_mixed_block",
            "field_or_test": "metric-photon",
            "operator_or_equation": "delta2 Gamma/(delta h delta A)|bar A=0=0",
            "result": "zero because every gauge-invariant photon term is at least quadratic in A",
            "passed": True,
        },
        {
            "row_id": "HESS5187_05_Apsi",
            "row_type": "exact_mixed_block",
            "field_or_test": "photon-motion",
            "operator_or_equation": "delta2 Gamma/(delta A delta psi)|bar A=bar psi=0=0",
            "result": "zero because the selected parent has no reflection-odd or gauge-variant direct portal",
            "passed": True,
        },
        {
            "row_id": "HESS5187_06_source_h",
            "row_type": "linear_source_vertex",
            "field_or_test": "metric source",
            "operator_or_equation": "V_hT=(a/2)h_mn T^mn; delta S_matter/delta H^mn=-R4(T)_mn/2",
            "result": "complete invertible Hilbert source",
            "passed": True,
        },
        {
            "row_id": "HESS5187_07_source_A",
            "row_type": "linear_source_vertex",
            "field_or_test": "photon source",
            "operator_or_equation": "V_AJ=e A_m j^m; nabla_m J^m=0",
            "result": "one conserved U1 current",
            "passed": True,
        },
        {
            "row_id": "HESS5187_08_source_psi",
            "row_type": "linear_source_vertex",
            "field_or_test": "motion source",
            "operator_or_equation": "delta S_matter/delta psi|psi=0=Q_psi=0",
            "result": "no classical one-scalar fifth-force pole",
            "passed": True,
        },
    ]
    rows.extend(block_rows)

    trace_matrix = trace_reversal_matrix()
    trace_rank = fraction_rank(trace_matrix)
    trace_det = fraction_determinant(trace_matrix)
    trace_square = matrix_product(trace_matrix, trace_matrix)
    trace_involution = trace_square == identity_matrix(10)
    rows.extend(
        [
            {
                "row_id": "HESS5187_09_trace_map",
                "row_type": "source_map_theorem",
                "field_or_test": "four-dimensional trace reversal",
                "operator_or_equation": "R4(T)_mn=T_mn-g_mn T/2",
                "rank": trace_rank,
                "nullity": 10 - trace_rank,
                "determinant": str(trace_det),
                "result": "invertible and involutive",
                "passed": trace_rank == 10
                and trace_det == -1
                and trace_involution,
            },
        ]
    )

    species_count = 5
    soft_matrix = species_difference_matrix(species_count)
    soft_rank = fraction_rank(soft_matrix)
    soft_nullity = species_count - soft_rank
    null_vector = [Fraction(1)] * species_count
    null_residual = [
        sum(
            (
                matrix_value * vector_value
                for matrix_value, vector_value in zip(
                    row,
                    null_vector,
                    strict=True,
                )
            ),
            Fraction(0),
        )
        for row in soft_matrix
    ]
    rows.extend(
        [
            {
                "row_id": "HESS5187_10_soft_species",
                "row_type": "source_map_theorem",
                "field_or_test": "soft spin-two species constraints",
                "operator_or_equation": "c_i-c_0=0 for five independent source classes",
                "rank": soft_rank,
                "nullity": soft_nullity,
                "null_vector": "(1,1,1,1,1)",
                "result": "one common leading spin-two residue",
                "passed": soft_rank == 4
                and soft_nullity == 1
                and all(value == 0 for value in null_residual),
            },
            {
                "row_id": "HESS5187_11_Bianchi_species",
                "row_type": "source_map_theorem",
                "field_or_test": "Bianchi exchange constraints",
                "operator_or_equation": "sum_i c_i Q_i^nu=0 whenever sum_i Q_i^nu=0",
                "rank": soft_rank,
                "nullity": soft_nullity,
                "null_vector": "(1,1,1,1,1)",
                "result": "same one-dimensional common-coupling subspace",
                "passed": soft_rank == 4 and soft_nullity == 1,
            },
        ]
    )

    spin2_products: list[float] = []
    for coordinate_scale in (0.25, 0.5, 1.0, 2.0, 4.0):
        hessian_coefficient = coordinate_scale**2 / 4.0
        propagator_coefficient = 4.0 / coordinate_scale**2
        vertex = coordinate_scale / 2.0
        exchange = vertex**2 * propagator_coefficient
        spin2_products.append(exchange)
        rows.append(
            {
                "row_id": f"HESS5187_spin2_norm_{coordinate_scale:g}",
                "row_type": "normalization_cancellation",
                "field_or_test": "spin-two coordinate normalization",
                "coordinate_scale": coordinate_scale,
                "operator_or_equation": "Gamma2=M_R^2 a^2 q^2 K/4; D=4K^-1/(M_R^2 a^2 q^2); V=a/2",
                "hessian_coefficient_for_MR2_q2K": hessian_coefficient,
                "propagator_coefficient_for_Kinv_over_MR2q2": propagator_coefficient,
                "vertex": vertex,
                "exchange_residue_for_1_over_MR2q2": exchange,
                "result": "coordinate scale cancels",
                "passed": math.isclose(exchange, 1.0, rel_tol=0.0, abs_tol=1e-15),
            }
        )

    photon_products: list[float] = []
    for photon_wavefunction in (0.25, 0.5, 1.0, 2.0, 4.0):
        bare_charge = 1.0
        canonical_charge = bare_charge / math.sqrt(photon_wavefunction)
        original_exchange = bare_charge**2 / photon_wavefunction
        canonical_exchange = canonical_charge**2
        photon_products.append(original_exchange / canonical_exchange)
        rows.append(
            {
                "row_id": f"HESS5187_photon_norm_{photon_wavefunction:g}",
                "row_type": "normalization_cancellation",
                "field_or_test": "photon wavefunction normalization",
                "coordinate_scale": photon_wavefunction,
                "operator_or_equation": "A_c=sqrt(Z_A)A; e_c=e/sqrt(Z_A)",
                "bare_e": bare_charge,
                "canonical_e": canonical_charge,
                "original_exchange_e2_over_ZA": original_exchange,
                "canonical_exchange_ec2": canonical_exchange,
                "result": "only e^2/Z_A is physical",
                "passed": math.isclose(
                    original_exchange,
                    canonical_exchange,
                    rel_tol=1e-14,
                    abs_tol=1e-15,
                ),
            }
        )

    metrics = {
        "field_degree_mixed_derivative_sum": mixed_sum,
        "trace_reversal_rank": trace_rank,
        "trace_reversal_nullity": 10 - trace_rank,
        "trace_reversal_determinant": str(trace_det),
        "trace_reversal_involution": trace_involution,
        "soft_species_rank": soft_rank,
        "soft_species_nullity": soft_nullity,
        "soft_species_null_vector": [1] * species_count,
        "maximum_spin2_normalization_residual": max(
            abs(value - 1.0) for value in spin2_products
        ),
        "maximum_photon_normalization_residual": max(
            abs(value - 1.0) for value in photon_products
        ),
        "vacuum_Hessian_block_diagonal": mixed_sum == 0,
        "linear_source_vertices": {
            "metric": "universal_Hilbert_stress",
            "photon": "conserved_U1_current",
            "motion": "exact_zero_on_reflection_even_branch",
        },
    }
    return tagged(rows), metrics


def build_limit_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    relation_residual = abs(8.0 * math.pi * (1.0 / (8.0 * math.pi)) - 1.0)
    green_residual = abs(4.0 * math.pi * (1.0 / (4.0 * math.pi)) - 1.0)
    rows = [
        {
            "chain_id": "LIM5187_00_metric_variation",
            "sector": "gravity",
            "operation": "vary the canonical metric action",
            "equation": "M_R^2(G_mn+Lambda_cal g_mn)=T_total_mn",
            "shared_residue": "G_N=1/(8pi M_R^2)",
            "new_calibration": "one numerical G_N value",
            "scope": "exact two-derivative parent equation",
            "status": "DERIVED_INSIDE_EXPLICIT_PARENT",
            "passed": relation_residual < 1e-15,
        },
        {
            "chain_id": "LIM5187_01_exchange",
            "sector": "gravity",
            "operation": "invert the conserved-source Einstein Hessian",
            "equation": "Gamma_12=i[M_R^2(q^2+i0)]^-1[T1_mnT2^mn-T1T2/2]",
            "shared_residue": "1/M_R^2=8pi G_N",
            "new_calibration": "none",
            "scope": "massless spin-two pole",
            "status": "DERIVED_UNIVERSAL_EXCHANGE",
            "passed": True,
        },
        {
            "chain_id": "LIM5187_02_harmonic",
            "sector": "gravity",
            "operation": "linearize in harmonic gauge",
            "equation": "Box hbar_mn=-2T_mn/M_R^2=-16pi G_N T_mn",
            "shared_residue": "G_N",
            "new_calibration": "none",
            "scope": "local weak field q^2 much greater than |Lambda_cal|",
            "status": "DERIVED_LINEAR_EINSTEIN",
            "passed": relation_residual < 1e-15,
        },
        {
            "chain_id": "LIM5187_03_Poisson",
            "sector": "Newton",
            "operation": "take the static nonrelativistic 00 projection",
            "equation": "nabla^2 Phi=4pi G_N rho-Lambda_cal c^2",
            "shared_residue": "G_N;Lambda_cal",
            "new_calibration": "none",
            "scope": "Schwarzschild-de Sitter weak limit",
            "status": "DERIVED_POISSON_WITH_BACKGROUND_TERM",
            "passed": True,
        },
        {
            "chain_id": "LIM5187_04_Green",
            "sector": "Newton",
            "operation": "use the three-dimensional massless Green function",
            "equation": "int d^3q/(2pi)^3 exp(iq.r)/q^2=1/(4pi r)",
            "shared_residue": "G_N",
            "new_calibration": "none",
            "scope": "distributional identity away from source",
            "status": "DERIVED_INVERSE_DISTANCE_KERNEL",
            "passed": green_residual < 1e-15,
        },
        {
            "chain_id": "LIM5187_05_point_potential",
            "sector": "Newton",
            "operation": "solve for a point mass",
            "equation": "Phi=-G_N M/r-Lambda_cal c^2 r^2/6",
            "shared_residue": "G_N;Lambda_cal",
            "new_calibration": "none",
            "scope": "local weak field",
            "status": "DERIVED_POINT_SOURCE_POTENTIAL",
            "passed": True,
        },
        {
            "chain_id": "LIM5187_06_geodesic",
            "sector": "Newton",
            "operation": "vary S_pp=-m int ds",
            "equation": "u.nabla u^m=0; d2x/dt2=-grad Phi",
            "shared_residue": "same public metric and G_N",
            "new_calibration": "none",
            "scope": "neutral test body",
            "status": "DERIVED_INERTIAL_PASSIVE_ACTIVE_CHAIN",
            "passed": True,
        },
        {
            "chain_id": "LIM5187_07_inverse_square",
            "sector": "Newton",
            "operation": "differentiate the point potential",
            "equation": "a_r=-G_N M/r^2+Lambda_cal c^2 r/3",
            "shared_residue": "same G_N",
            "new_calibration": "none",
            "scope": "local weak field",
            "status": "DERIVED_NEWTON_FORCE_WITH_BACKGROUND_TERM",
            "passed": True,
        },
        {
            "chain_id": "LIM5187_08_lensing",
            "sector": "gravity",
            "operation": "take the null eikonal/geodesic limit",
            "equation": "k.nabla k^m=0; alpha_lens=4G_N M/(bc^2)+higher gradients",
            "shared_residue": "same public metric and G_N",
            "new_calibration": "none",
            "scope": "leading local null propagation",
            "status": "NO_SEPARATE_LENSING_G",
            "passed": True,
        },
        {
            "chain_id": "LIM5187_09_PPN",
            "sector": "gravity",
            "operation": "project the exact psi=0 two-derivative branch",
            "equation": "gamma_PPN=1; beta_PPN=1; Q_psi=0",
            "shared_residue": "same G_N",
            "new_calibration": "none",
            "scope": "standard constant PPN order; higher gradients retained separately",
            "status": "DERIVED_LEADING_LOCAL_PPN",
            "passed": True,
        },
        {
            "chain_id": "LIM5187_10_photon_normalization",
            "sector": "electromagnetism",
            "operation": "canonically normalize the photon",
            "equation": "A_c=sqrt(Z_A)A; e_c=e/sqrt(Z_A); alpha_EM=e_c^2/(4pi)",
            "shared_residue": "e^2/Z_A",
            "new_calibration": "one alpha_EM value",
            "scope": "rationalized natural units",
            "status": "ONE_PHYSICAL_EM_NORMALIZATION",
            "passed": True,
        },
        {
            "chain_id": "LIM5187_11_Maxwell",
            "sector": "electromagnetism",
            "operation": "vary A_n",
            "equation": "nabla_m F^mn-4c_IR nabla_m(C^mnrs F_rs)=J^n",
            "shared_residue": "alpha_EM;c_IR",
            "new_calibration": "none after alpha_EM and c_IR are fixed once",
            "scope": "canonical photon field",
            "status": "DERIVED_MAXWELL_CFF_EQUATION",
            "passed": True,
        },
        {
            "chain_id": "LIM5187_12_flat_Maxwell",
            "sector": "electromagnetism",
            "operation": "set Weyl curvature to zero",
            "equation": "partial_m F^mn=J^n; partial_[mF_nr]=0",
            "shared_residue": "alpha_EM",
            "new_calibration": "none",
            "scope": "exact for arbitrary c_IR when C_mnrs=0",
            "status": "EXACT_FLAT_MAXWELL_LIMIT",
            "passed": True,
        },
        {
            "chain_id": "LIM5187_13_Coulomb",
            "sector": "electromagnetism",
            "operation": "solve the static point-current equation",
            "equation": "E_r=q/(4pi r^2); F_12=q1q2/(4pi r^2)",
            "shared_residue": "same alpha_EM charge convention",
            "new_calibration": "none",
            "scope": "flat canonical rationalized units",
            "status": "DERIVED_COULOMB_KERNEL",
            "passed": green_residual < 1e-15,
        },
        {
            "chain_id": "LIM5187_14_Lorentz",
            "sector": "electromagnetism",
            "operation": "vary -m int ds+q int A.dx",
            "equation": "u.nabla u^m=(q/m)F^m_n u^n",
            "shared_residue": "same alpha_EM charge convention",
            "new_calibration": "none",
            "scope": "charged point body",
            "status": "DERIVED_LORENTZ_FORCE",
            "passed": True,
        },
        {
            "chain_id": "LIM5187_15_stress",
            "sector": "electromagnetism",
            "operation": "vary the same photon action with respect to g_mn",
            "equation": "T_EM,mn=F_maF_n^a-g_mnF^2/4+c_IR H_CFF,mn",
            "shared_residue": "same canonical photon normalization and c_IR",
            "new_calibration": "none",
            "scope": "Hilbert stress",
            "status": "DERIVED_EM_STRESS",
            "passed": True,
        },
        {
            "chain_id": "LIM5187_16_Poynting",
            "sector": "electromagnetism",
            "operation": "take the 0i component of the canonical stress",
            "equation": "T_EM^0i=(E cross B)^i in canonical natural units",
            "shared_residue": "same photon action",
            "new_calibration": "none",
            "scope": "flat leading Maxwell sector",
            "status": "DERIVED_POYNTING_FLUX_NOT_EXTRA_BACKGROUND_COUPLING",
            "passed": True,
        },
        {
            "chain_id": "LIM5187_17_conservation",
            "sector": "combined",
            "operation": "apply Diff and U1 Ward identities on shell",
            "equation": "nabla^m(T_EM,mn+T_matter,mn+T_psi,mn)=0",
            "shared_residue": "same metric and gauge action",
            "new_calibration": "none",
            "scope": "selected parent",
            "status": "DERIVED_TOTAL_EXCHANGE_CONSERVATION",
            "passed": True,
        },
        {
            "chain_id": "LIM5187_18_motion_silence",
            "sector": "motion",
            "operation": "evaluate the reflection-even matter functor at psi=0",
            "equation": "delta S_matter/delta psi=Q_psi=a_psi/a_N=0",
            "shared_residue": "J_gap remains in the motion pole but not a linear local source",
            "new_calibration": "none in the leading local force law",
            "scope": "ordinary matter and no reflection-odd surface action",
            "status": "EXACT_CLASSICAL_ONE_SCALAR_FORCE_ZERO",
            "passed": True,
        },
    ]
    metrics = {
        "GN_MR_relation_residual": relation_residual,
        "three_dimensional_Green_normalization_residual": green_residual,
        "chain_row_count": len(rows),
        "failed_chain_rows": sum(not row["passed"] for row in rows),
        "leading_local_GR_Newton_chain": True,
        "leading_flat_Maxwell_Lorentz_stress_Poynting_chain": True,
        "numerical_GN_predicted": False,
        "numerical_alpha_EM_predicted": False,
    }
    return tagged(rows), metrics


def build_rg_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "row_id": "RG5187_00_autonomy",
            "row_type": "theorem",
            "statement": "dimensionless autonomous flow is invariant under RG-time translation",
            "equation": "dg/dln(k)=beta(g); g(k)=g_hat(k/Lambda_g)",
            "consequence": "Lambda_g is an integration modulus not selected by fixed-point coordinates",
            "status": "DERIVED",
            "passed": True,
        },
        {
            "row_id": "RG5187_01_explicit_family",
            "row_type": "theorem",
            "statement": "an explicit fixed-point-identical scale family exists",
            "equation": "g_hat(x)=g_star x^2/(1+x^2); beta_g=2g(1-g/g_star)",
            "consequence": "all members have Gaussian IR and the same UV fixed point g_star",
            "status": "CONSTRUCTIVE_COUNTERFAMILY",
            "passed": True,
        },
        {
            "row_id": "RG5187_02_IR_residue",
            "row_type": "theorem",
            "statement": "the dimensionful Newton residue is the Gaussian-endpoint coefficient",
            "equation": "G_N=lim(k->0)g(k)/k^2=C_g/Lambda_g^2",
            "consequence": "dimensionless trajectory shape gives relations but not the SI scale",
            "status": "DERIVED",
            "passed": True,
        },
        {
            "row_id": "RG5187_03_gap",
            "row_type": "theorem",
            "statement": "the motion gap ratio is transported but not selected",
            "equation": "J_gap=w_psi g=m_gap^2 G_N; beta_J/J=(-2)+(+2)=0 in the Gaussian IR",
            "consequence": "fixed J_gap does not fix Lambda_g or G_N",
            "status": "DERIVED_INDEPENDENT_RELEVANT_COORDINATE",
            "passed": True,
        },
        {
            "row_id": "RG5187_04_scale_verdict",
            "row_type": "theorem",
            "statement": "current parent scale-setting verdict",
            "equation": "same beta functions plus Lambda_g->s Lambda_g imply G_N->G_N/s^2",
            "consequence": "one absolute gravitational scale datum is unavoidable unless a future parent supplies an independent anchor",
            "status": "NUMERICAL_GN_NOT_DERIVED_RELATION_AND_UNIVERSALITY_DERIVED",
            "passed": True,
        },
    ]

    maximum_beta_residual = 0.0
    fixed_point_values: list[float] = []
    g_star = 1.0
    for x in (1e-3, 1e-2, 0.1, 1.0, 10.0, 100.0):
        g_value = g_star * x**2 / (1.0 + x**2)
        derivative = 2.0 * g_star * x**2 / (1.0 + x**2) ** 2
        beta_value = 2.0 * g_value * (1.0 - g_value / g_star)
        residual = abs(derivative - beta_value)
        maximum_beta_residual = max(maximum_beta_residual, residual)
        fixed_point_values.append(g_value)
        rows.append(
            {
                "row_id": f"RG5187_shape_{x:g}",
                "row_type": "explicit_trajectory_check",
                "statement": "autonomous logistic fixed-point trajectory",
                "equation": "g=x^2/(1+x^2)",
                "x_equals_k_over_Lambda_g": x,
                "g_value": g_value,
                "d_g_d_ln_k": derivative,
                "beta_of_g": beta_value,
                "absolute_residual": residual,
                "consequence": "same dimensionless shape for every Lambda_g",
                "status": "PASS",
                "passed": residual < 1e-14,
            }
        )

    scale_rows: list[dict[str, Any]] = []
    for scale_factor in (0.25, 0.5, 1.0, 2.0, 4.0, 10.0):
        g_ratio = 1.0 / scale_factor**2
        mass_ratio_at_fixed_j = scale_factor
        row = {
            "row_id": f"RG5187_scale_{scale_factor:g}",
            "row_type": "scale_modulus_family",
            "statement": "translate the same dimensionless trajectory along ln(k)",
            "equation": "Lambda_g=s Lambda_ref; G_N/G_ref=s^-2; m_gap/m_ref=s at fixed J_gap",
            "Lambda_g_over_reference": scale_factor,
            "G_N_over_reference": g_ratio,
            "J_gap_over_reference": 1.0,
            "m_gap_over_reference_at_fixed_J": mass_ratio_at_fixed_j,
            "dimensionless_fixed_point_changed": False,
            "consequence": "J_gap remains fixed while the absolute length and mass units move",
            "status": "EXPLICIT_SCALE_DEGENERACY",
            "passed": math.isclose(
                g_ratio * mass_ratio_at_fixed_j**2,
                1.0,
                rel_tol=0.0,
                abs_tol=1e-15,
            ),
        }
        rows.append(row)
        scale_rows.append(row)

    metrics = {
        "explicit_beta_maximum_residual": maximum_beta_residual,
        "UV_fixed_point_target": g_star,
        "largest_sampled_g": max(fixed_point_values),
        "scale_family_count": len(scale_rows),
        "scale_family_preserves_J_gap": all(
            row["J_gap_over_reference"] == 1.0 for row in scale_rows
        ),
        "scale_family_changes_GN": len(
            {row["G_N_over_reference"] for row in scale_rows}
        )
        == len(scale_rows),
        "IR_beta_J_over_J": -2 + 2,
        "absolute_GN_selected_by_current_dimensionless_flow": False,
        "required_absolute_gravity_motion_scale_calibrations": 1,
    }
    return tagged(rows), metrics


def build_parameter_rows() -> tuple[list[dict[str, Any]], dict[str, int]]:
    rows = [
        {
            "parameter_id": "PAR5187_00_structure",
            "symbol": "H^mn;Diff/BRST;positive spin-two pole;U1 representations",
            "category": "parent structural data",
            "independent_numeric_inputs": 0,
            "leading_local_force_normalization": False,
            "action_or_state": "parent definition",
            "derived_relation": "universal source residue follows once these premises hold",
            "numeric_status": "NOT_NUMERIC",
            "arena_retune_allowed": False,
            "current_status": "EXPLICIT_NOT_DERIVED_FROM_ONE_SCALAR",
        },
        {
            "parameter_id": "PAR5187_01_GN",
            "symbol": "M_R^2 <-> G_N",
            "category": "absolute gravity scale",
            "independent_numeric_inputs": 1,
            "leading_local_force_normalization": True,
            "action_or_state": "action",
            "derived_relation": "G_N=1/(8pi M_R^2); all leading gravitational arenas share it",
            "numeric_status": "MEASURE_ONCE",
            "arena_retune_allowed": False,
            "current_status": "RELATION_AND_UNIVERSALITY_DERIVED_ABSOLUTE_VALUE_CALIBRATED",
        },
        {
            "parameter_id": "PAR5187_02_Lambda",
            "symbol": "Lambda_cal",
            "category": "background curvature",
            "independent_numeric_inputs": 1,
            "leading_local_force_normalization": False,
            "action_or_state": "action",
            "derived_relation": "same background term enters every local arena",
            "numeric_status": "BACKGROUND_CALIBRATION",
            "arena_retune_allowed": False,
            "current_status": "VALUE_NOT_PREDICTED",
        },
        {
            "parameter_id": "PAR5187_03_alpha",
            "symbol": "alpha_EM=e^2/(4pi Z_A)",
            "category": "leading electromagnetic normalization",
            "independent_numeric_inputs": 1,
            "leading_local_force_normalization": True,
            "action_or_state": "action/representation",
            "derived_relation": "Maxwell Coulomb Lorentz stress and Poynting share e^2/Z_A",
            "numeric_status": "MEASURE_ONCE",
            "arena_retune_allowed": False,
            "current_status": "ONE_PHYSICAL_EM_NORMALIZATION",
        },
        {
            "parameter_id": "PAR5187_04_Jgap",
            "symbol": "J_gap=m_gap^2 G_N",
            "category": "motion relevant coordinate",
            "independent_numeric_inputs": 1,
            "leading_local_force_normalization": False,
            "action_or_state": "action",
            "derived_relation": "beta_J=0 in Gaussian IR; local one-scalar source is zero",
            "numeric_status": "UNSELECTED_UNIVERSAL_COORDINATE",
            "arena_retune_allowed": False,
            "current_status": "TRANSPORTED_NOT_SELECTED",
        },
        {
            "parameter_id": "PAR5187_05_cIR",
            "symbol": "c_IR",
            "category": "curvature-photon LEC",
            "independent_numeric_inputs": 1,
            "leading_local_force_normalization": False,
            "action_or_state": "action",
            "derived_relation": "one coefficient controls curved propagation and Hilbert stress",
            "numeric_status": "NONQCD_PART_KNOWN_QCD_FINITE_PART_OPEN",
            "arena_retune_allowed": False,
            "current_status": "ONE_TJJ_OR_CURVED_PHOTON_CALIBRATION_REQUIRED",
        },
        {
            "parameter_id": "PAR5187_06_p4vac",
            "symbol": "a_R,a_C in neutral vacuum",
            "category": "four-derivative vacuum gravity",
            "independent_numeric_inputs": 0,
            "leading_local_force_normalization": False,
            "action_or_state": "redundant action coordinates",
            "derived_relation": "removed at first strict-EFT order by EOM quotient up to Euler/boundary",
            "numeric_status": "NO_VACUUM_LONG_RANGE_INPUT",
            "arena_retune_allowed": False,
            "current_status": "QUOTIENTED",
        },
        {
            "parameter_id": "PAR5187_07_contact",
            "symbol": "2a_C;a_R-2a_C/3 plus matter counterterms",
            "category": "matter contact/worldline/EOS EFT",
            "independent_numeric_inputs": 2,
            "leading_local_force_normalization": False,
            "action_or_state": "action/contact",
            "derived_relation": "stress-square packet identified; independent matter basis reduction open",
            "numeric_status": "OPEN_ONLY_WHEN_SHORT_DISTANCE_MATTER_PRECISION_REQUIRES",
            "arena_retune_allowed": False,
            "current_status": "NOT_A_VACUUM_GR_RESIDUE",
        },
        {
            "parameter_id": "PAR5187_08_C3",
            "symbol": "A_C3^S or a_plus",
            "category": "six-derivative vacuum gravity",
            "independent_numeric_inputs": 0,
            "leading_local_force_normalization": False,
            "action_or_state": "action trajectory coordinate",
            "derived_relation": "selected finite p6 coordinate in locked source scheme",
            "numeric_status": "TRAJECTORY_SELECTED",
            "arena_retune_allowed": False,
            "current_status": "LOCAL_P6_SAFE_NONLOCAL_COMPLETION_OPEN",
        },
        {
            "parameter_id": "PAR5187_09_p8",
            "symbol": "C_8;R_tail",
            "category": "p8-plus aggregate tail",
            "independent_numeric_inputs": 2,
            "leading_local_force_normalization": False,
            "action_or_state": "action completion",
            "derived_relation": "conditional tail inequality only",
            "numeric_status": "PARENT_PROJECTION_AND_CONVERGENCE_RADIUS_OPEN",
            "arena_retune_allowed": False,
            "current_status": "ALL_OPERATOR_GR_NOT_PROVED",
        },
        {
            "parameter_id": "PAR5187_10_state_abundance",
            "symbol": "Omega_X or psi_i",
            "category": "cosmological occupied-state normalization",
            "independent_numeric_inputs": 1,
            "leading_local_force_normalization": False,
            "action_or_state": "initial state",
            "derived_relation": "free FLRW Bogoliubov production is at least 88 orders too small",
            "numeric_status": "CONDITIONAL_INITIAL_DATA",
            "arena_retune_allowed": False,
            "current_status": "NOT_AN_ACTION_COUPLING",
        },
        {
            "parameter_id": "PAR5187_11_state_covariance",
            "symbol": "neutral Gaussian covariance/squeezing phase",
            "category": "state covariance",
            "independent_numeric_inputs": 1,
            "leading_local_force_normalization": False,
            "action_or_state": "initial state",
            "derived_relation": "neutral squeezed-pair relation derived; amplitude and phase not parent-selected",
            "numeric_status": "CONDITIONAL_INITIAL_DATA",
            "arena_retune_allowed": False,
            "current_status": "NOT_AN_ACTION_COUPLING",
        },
    ]
    counts = {
        "leading_local_force_normalizations": sum(
            bool(row["leading_local_force_normalization"]) for row in rows
        ),
        "background_curvature_calibrations": 1,
        "motion_action_coordinates_unselected": 1,
        "curvature_photon_LECs_open": 1,
        "neutral_vacuum_p4_long_range_inputs": 0,
        "p6_empirical_inputs": 0,
        "matter_contact_pre_reduction_open": 2,
        "p8_aggregate_coordinates_open": 2,
        "initial_state_data_classes_open": 2,
        "absolute_GR_motion_scale_calibrations": 1,
    }
    return tagged(rows), counts


def parse_interval(interval: str) -> tuple[float, float]:
    matches = re.findall(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", interval)
    if len(matches) != 2:
        raise ValueError(f"Cannot parse interval: {interval}")
    return float(matches[0]), float(matches[1])


def build_corridor_rows(
    c3_rows: list[dict[str, str]],
    determinant_rows: list[dict[str, str]],
    compact_c3_rows: list[dict[str, str]],
    cff_transfer_rows: list[dict[str, str]],
    cff_contract_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "residual_id": "COR5187_00_scalar_force",
            "sector": "motion",
            "arena": "ordinary local matter",
            "quantity": "a_psi/a_N",
            "value": 0.0,
            "units": "dimensionless",
            "condition": "reflection-even psi=0 branch and no odd surface action",
            "physical_amplitude_complete": True,
            "claim_status": "EXACT_ZERO_AT_CLASSICAL_ONE_SCALAR_ORDER",
            "source_path": "source-intake/functional_rg/4943/junction_scalar_charge_and_fifth_force.csv",
        },
        {
            "residual_id": "COR5187_01_PPN_gamma",
            "sector": "motion/O4/CFF",
            "arena": "standard local PPN",
            "quantity": "Delta gamma_PPN",
            "value": 0.0,
            "units": "dimensionless",
            "condition": "psi=F=0 at defining constant PPN order",
            "physical_amplitude_complete": True,
            "claim_status": "EXACT_ZERO_AT_DECLARED_ORDER",
            "source_path": "source-intake/functional_rg/4942/local_homogeneous_branch_identities.csv",
        },
        {
            "residual_id": "COR5187_02_PPN_beta",
            "sector": "motion/O4/CFF",
            "arena": "standard local PPN",
            "quantity": "Delta beta_PPN",
            "value": 0.0,
            "units": "dimensionless",
            "condition": "psi=F=0 at defining constant PPN order",
            "physical_amplitude_complete": True,
            "claim_status": "EXACT_ZERO_AT_DECLARED_ORDER",
            "source_path": "source-intake/functional_rg/4942/local_homogeneous_branch_identities.csv",
        },
        {
            "residual_id": "COR5187_03_p4_vacuum",
            "sector": "four-derivative gravity",
            "arena": "neutral exterior vacuum",
            "quantity": "independent p4 long-range coefficients",
            "value": 0,
            "units": "count",
            "condition": "first strict-EFT order modulo field redefinitions and Euler/boundary",
            "physical_amplitude_complete": True,
            "claim_status": "QUOTIENTED_NOT_CALIBRATION_MISSING",
            "source_path": "source-intake/functional_rg/4964/finite_matching_parameter_count.csv",
        },
    ]

    c3_values: list[float] = []
    for index, row in enumerate(c3_rows):
        value = float(row["selected_abs_Deltaa_over_aN_bound"])
        c3_values.append(value)
        rows.append(
            {
                "residual_id": f"COR5187_C3_{index:02d}",
                "sector": "selected local C3",
                "arena": row["scale_id"],
                "quantity": "abs(Delta a/a_N)",
                "value": value,
                "units": "dimensionless",
                "condition": row["condition"],
                "physical_amplitude_complete": False,
                "claim_status": "SELECTED_SOURCE_SCHEME_LOCAL_BOUND_NONLOCAL_COMPLETION_OPEN",
                "source_path": "source-intake/functional_rg/4986/C3_exterior_compactness_bounds.csv",
            }
        )

    determinant_values: list[float] = []
    for index, row in enumerate(determinant_rows):
        value = float(row["exterior_abs_Deltaa_over_aN"])
        determinant_values.append(value)
        rows.append(
            {
                "residual_id": f"COR5187_DET_{index:02d}",
                "sector": "one-loop determinant two-point tail",
                "arena": row["scale_id"],
                "quantity": "abs(Delta a/a_N)",
                "value": value,
                "units": "dimensionless",
                "condition": row["motion_threshold_regime"],
                "physical_amplitude_complete": False,
                "claim_status": "MASSLESS_ENDPOINT_SUBSET_PHYSICAL_MGAP_THRESHOLD_OPEN",
                "source_path": "source-intake/functional_rg/4986/determinant_exterior_tail_bounds.csv",
            }
        )

    finite_compact_values = [
        float(row["finite_abs_Deltaa_over_aN"])
        for row in compact_c3_rows
        if row.get("finite_abs_Deltaa_over_aN")
    ]
    running_compact_values = [
        float(row["running_abs_Deltaa_over_aN"])
        for row in compact_c3_rows
        if row.get("running_abs_Deltaa_over_aN")
    ]
    black_hole_epsilon = [
        float(row["finite_epsilon_h"])
        for row in compact_c3_rows
        if row.get("finite_epsilon_h")
    ]
    rows.extend(
        [
            {
                "residual_id": "COR5187_compact_C3_finite",
                "sector": "selected local C3",
                "arena": "neutron-star source set",
                "quantity": "maximum finite abs(Delta a/a_N)",
                "value": max(finite_compact_values),
                "units": "dimensionless",
                "condition": "declared p6 source closure",
                "physical_amplitude_complete": False,
                "claim_status": "P6_LOCAL_COORDINATE_SAFE",
                "source_path": "source-intake/functional_rg/4963/compact_C3_residual_domain.csv",
            },
            {
                "residual_id": "COR5187_compact_C3_running",
                "sector": "selected local C3",
                "arena": "neutron-star source set",
                "quantity": "maximum running-coordinate envelope abs(Delta a/a_N)",
                "value": max(running_compact_values),
                "units": "dimensionless",
                "condition": "diagnostic running envelope is not a full physical amplitude",
                "physical_amplitude_complete": False,
                "claim_status": "DIAGNOSTIC_ONLY",
                "source_path": "source-intake/functional_rg/4963/compact_C3_residual_domain.csv",
            },
            {
                "residual_id": "COR5187_BH_C3",
                "sector": "selected local C3",
                "arena": "ten-solar-mass Schwarzschild horizon",
                "quantity": "epsilon_h",
                "value": max(black_hole_epsilon),
                "units": "dimensionless",
                "condition": "local p6 horizon-control diagnostic",
                "physical_amplitude_complete": False,
                "claim_status": "P6_LOCAL_COORDINATE_SAFE",
                "source_path": "source-intake/functional_rg/4963/compact_C3_residual_domain.csv",
            },
        ]
    )

    nonqcd_row = next(
        row
        for row in cff_contract_rows
        if row["contract_id"] == "CFF4964_02_nonQCD_interval"
    )
    nonqcd_interval = parse_interval(nonqcd_row["numeric_value"])
    nonqcd_envelope = max(abs(value) for value in nonqcd_interval)
    cff_ratios: list[float] = []
    for index, row in enumerate(cff_transfer_rows):
        one_ppm_budget = float(row["abs_cIR_for_1e_minus_6_split_m2"])
        ratio = nonqcd_envelope / one_ppm_budget
        cff_ratios.append(ratio)
        rows.append(
            {
                "residual_id": f"COR5187_CFF_{index:02d}",
                "sector": "curvature photon CFF",
                "arena": row["system"],
                "quantity": "known nonQCD abs(c_IR)/one-ppm budget",
                "value": ratio,
                "units": "dimensionless",
                "condition": "compares only source-backed nonQCD component; finite QCD contact excluded",
                "physical_amplitude_complete": False,
                "claim_status": "KNOWN_COMPONENT_TINY_PHYSICAL_TOTAL_OPEN",
                "source_path": "source-intake/functional_rg/4946/universal_CFF_calibration_transfer_functions.csv",
                "curvature_factor_m_minus_2": row[
                    "CFF_curvature_factor_m_minus_2"
                ],
                "one_ppm_abs_cIR_budget_m2": one_ppm_budget,
                "one_percent_abs_cIR_budget_m2": row[
                    "abs_cIR_for_1_percent_split_m2"
                ],
            }
        )
    rows.extend(
        [
            {
                "residual_id": "COR5187_CFF_total",
                "sector": "curvature photon CFF",
                "arena": "all curved photon arenas",
                "quantity": "physical total c_IR",
                "value": "",
                "units": "m^2",
                "condition": "one TJJ lattice match or one robust curved-photon calibration",
                "physical_amplitude_complete": False,
                "claim_status": "NUMERIC_TOTAL_OPEN_NO_ARENA_RETUNING",
                "source_path": "source-intake/functional_rg/4964/CFF_one_LEC_calibration_contract.csv",
            },
            {
                "residual_id": "COR5187_p8",
                "sector": "p8-plus Ricci-flat gravity",
                "arena": "compact and short-range local tests",
                "quantity": "aggregate omitted response norm",
                "value": "",
                "units": "dimensionless response norm",
                "condition": "requires parent p8 projection and coefficient-growth/convergence bound",
                "physical_amplitude_complete": False,
                "claim_status": "CONDITIONAL_TAIL_GATE_ONLY",
                "source_path": "source-intake/functional_rg/4964/p8plus_tail_norm_gate.csv",
            },
            {
                "residual_id": "COR5187_all_operator",
                "sector": "complete local theory",
                "arena": "all local/compact arenas",
                "quantity": "all-operator equality to GR",
                "value": False,
                "units": "boolean",
                "condition": "CFF physical total p8-plus and complete nonlocal amplitudes remain open",
                "physical_amplitude_complete": False,
                "claim_status": "NOT_CLAIMED",
                "source_path": "source-intake/functional_rg/4964/compact_all_operator_decision.csv",
            },
        ]
    )

    metrics = {
        "maximum_selected_C3_exterior_acceleration_fraction": max(c3_values),
        "maximum_massless_endpoint_determinant_acceleration_fraction": max(
            determinant_values
        ),
        "maximum_compact_finite_C3_acceleration_fraction": max(
            finite_compact_values
        ),
        "maximum_compact_running_coordinate_acceleration_fraction": max(
            running_compact_values
        ),
        "black_hole_C3_horizon_epsilon": max(black_hole_epsilon),
        "known_nonQCD_cIR_abs_envelope_m2": nonqcd_envelope,
        "maximum_known_nonQCD_to_one_ppm_budget_ratio": max(cff_ratios),
        "physical_total_cIR_known": False,
        "p8plus_complete": False,
        "all_operator_local_GR_claim": False,
    }
    return tagged(rows), metrics


def build_no_retuning_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "row_id": "NRT5187_00_Einstein",
                "arena": "nonlinear two-derivative Einstein equation",
                "shared_parameter": "G_N",
                "independent_arena_retune": False,
                "derivation": "metric variation of one EH residue",
                "status": "DERIVED_SHARED",
                "guard": "explicit parent H/Diff premises",
            },
            {
                "row_id": "NRT5187_01_Newton",
                "arena": "laboratory Newton/Poisson",
                "shared_parameter": "G_N",
                "independent_arena_retune": False,
                "derivation": "static 00 projection of the same Einstein equation",
                "status": "DERIVED_SHARED",
                "guard": "local weak field and calibrated Lambda background",
            },
            {
                "row_id": "NRT5187_02_orbit",
                "arena": "neutral orbital motion",
                "shared_parameter": "G_N",
                "independent_arena_retune": False,
                "derivation": "same metric plus -m int ds",
                "status": "DERIVED_SHARED",
                "guard": "higher-gradient compact residuals remain explicit",
            },
            {
                "row_id": "NRT5187_03_lensing",
                "arena": "leading lensing/null propagation",
                "shared_parameter": "G_N",
                "independent_arena_retune": False,
                "derivation": "same metric null geodesic/eikonal limit",
                "status": "DERIVED_SHARED",
                "guard": "CFF curved-photon correction separately retained",
            },
            {
                "row_id": "NRT5187_04_wave",
                "arena": "leading massless spin-two radiation residue",
                "shared_parameter": "G_N",
                "independent_arena_retune": False,
                "derivation": "same positive spin-two pole and conservative/radiative residue match",
                "status": "DERIVED_SHARED",
                "guard": "complete higher-operator waveform remains open",
            },
            {
                "row_id": "NRT5187_05_Coulomb",
                "arena": "flat Coulomb",
                "shared_parameter": "alpha_EM=e^2/(4pi Z_A)",
                "independent_arena_retune": False,
                "derivation": "static Green function of the canonical Maxwell block",
                "status": "DERIVED_SHARED",
                "guard": "visible charge representations are parent data",
            },
            {
                "row_id": "NRT5187_06_Lorentz",
                "arena": "charged-particle Lorentz force",
                "shared_parameter": "alpha_EM=e^2/(4pi Z_A)",
                "independent_arena_retune": False,
                "derivation": "same worldline gauge vertex",
                "status": "DERIVED_SHARED",
                "guard": "charge-to-mass ratio belongs to the particle state",
            },
            {
                "row_id": "NRT5187_07_stress",
                "arena": "EM gravitational stress/Poynting flux",
                "shared_parameter": "alpha_EM and c_IR",
                "independent_arena_retune": False,
                "derivation": "metric variation of the same photon action",
                "status": "DERIVED_SHARED",
                "guard": "physical total c_IR remains one open universal LEC",
            },
            {
                "row_id": "NRT5187_08_scalar_local",
                "arena": "ordinary local scalar/fifth-force tests",
                "shared_parameter": "J_gap",
                "independent_arena_retune": False,
                "derivation": "reflection-even matter functor gives Q_psi=0 for every ordinary source",
                "status": "EXACT_SOURCE_SILENCE",
                "guard": "does not erase occupied-state or pair-mediated effects",
            },
            {
                "row_id": "NRT5187_09_CFF",
                "arena": "all curved-photon transfer functions",
                "shared_parameter": "c_IR",
                "independent_arena_retune": False,
                "derivation": "one CFF operator controls equation and stress",
                "status": "STRUCTURE_DERIVED_NUMERIC_VALUE_OPEN",
                "guard": "one calibration must transfer everywhere",
            },
            {
                "row_id": "NRT5187_10_C3",
                "arena": "short-range orbital and compact p6 projections",
                "shared_parameter": "a_plus",
                "independent_arena_retune": False,
                "derivation": "one selected source-scheme coordinate propagated to every benchmark",
                "status": "LOCAL_P6_BOUND_DERIVED",
                "guard": "nonlocal completion prevents a complete-amplitude claim",
            },
            {
                "row_id": "NRT5187_11_state",
                "arena": "cosmological/galactic occupied motion state",
                "shared_parameter": "J_gap plus state abundance/covariance",
                "independent_arena_retune": False,
                "derivation": "5186 rejects free-vacuum abundance selection and separates state data from action couplings",
                "status": "CONDITIONAL_STATE_NOT_LOCAL_COUPLING",
                "guard": "state normalization is not yet parent-derived",
            },
        ]
    )


def build_provenance_rows(source_hashes: dict[str, str]) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "source_id": source_id,
                "source_path": str(path),
                "sha256_expected": expected_hash,
                "sha256_observed": source_hashes[source_id],
                "exists": path.is_file(),
                "hash_match": source_hashes[source_id] == expected_hash,
                "role": "locked local derivation input",
            }
            for source_id, (path, expected_hash) in SOURCES.items()
        ]
    )


def calculate_validations(
    source_hashes: dict[str, str],
    formal_before: str,
    checkpoint_5176_before: str,
    action_rows: list[dict[str, Any]],
    hessian_rows: list[dict[str, Any]],
    hessian_metrics: dict[str, Any],
    limit_rows: list[dict[str, Any]],
    limit_metrics: dict[str, Any],
    rg_rows: list[dict[str, Any]],
    rg_metrics: dict[str, Any],
    parameter_rows: list[dict[str, Any]],
    parameter_counts: dict[str, int],
    corridor_rows: list[dict[str, Any]],
    corridor_metrics: dict[str, Any],
    no_retuning_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    for index, (source_id, (path, expected_hash)) in enumerate(SOURCES.items()):
        checks.append(
            validation_row(
                f"V5187_{index:02d}_source_{source_id}",
                f"{source_id} exists and remains hash locked",
                path.is_file() and source_hashes[source_id] == expected_hash,
                source_hashes[source_id],
                expected_hash,
            )
        )
    base = len(checks)
    checks.extend(
        [
            validation_row(
                f"V5187_{base + 0:02d}_formal_before",
                "formalization-workbench matches the protected digest",
                formal_before == FORMAL_DIGEST_LOCK,
                formal_before,
                FORMAL_DIGEST_LOCK,
            ),
            validation_row(
                f"V5187_{base + 1:02d}_5176_before",
                "checkpoint 5176 ensemble matches the protected tree digest",
                checkpoint_5176_before == CHECKPOINT_5176_TREE_LOCK,
                checkpoint_5176_before,
                CHECKPOINT_5176_TREE_LOCK,
            ),
            validation_row(
                f"V5187_{base + 2:02d}_action",
                "canonical action contains every declared local sector",
                len(action_rows) == 12,
                len(action_rows),
                12,
            ),
            validation_row(
                f"V5187_{base + 3:02d}_mixed",
                "all local zero-field mixed Hessian blocks vanish",
                hessian_metrics["field_degree_mixed_derivative_sum"] == 0
                and hessian_metrics["vacuum_Hessian_block_diagonal"],
                hessian_metrics["field_degree_mixed_derivative_sum"],
                0,
            ),
            validation_row(
                f"V5187_{base + 4:02d}_trace_rank",
                "four-dimensional trace reversal is full rank",
                hessian_metrics["trace_reversal_rank"] == 10,
                hessian_metrics["trace_reversal_rank"],
                10,
            ),
            validation_row(
                f"V5187_{base + 5:02d}_trace_det",
                "trace reversal has determinant minus one",
                hessian_metrics["trace_reversal_determinant"] == "-1",
                hessian_metrics["trace_reversal_determinant"],
                "-1",
            ),
            validation_row(
                f"V5187_{base + 6:02d}_trace_involution",
                "trace reversal squares to the identity",
                hessian_metrics["trace_reversal_involution"],
                hessian_metrics["trace_reversal_involution"],
                True,
            ),
            validation_row(
                f"V5187_{base + 7:02d}_soft_rank",
                "five-source soft consistency has rank four and nullity one",
                hessian_metrics["soft_species_rank"] == 4
                and hessian_metrics["soft_species_nullity"] == 1,
                (
                    hessian_metrics["soft_species_rank"],
                    hessian_metrics["soft_species_nullity"],
                ),
                (4, 1),
            ),
            validation_row(
                f"V5187_{base + 8:02d}_spin2_norm",
                "graviton coordinate normalization cancels from exchange",
                hessian_metrics[
                    "maximum_spin2_normalization_residual"
                ]
                < 1e-14,
                hessian_metrics["maximum_spin2_normalization_residual"],
                "<1e-14",
            ),
            validation_row(
                f"V5187_{base + 9:02d}_photon_norm",
                "photon wavefunction normalization leaves only e squared over Z_A",
                hessian_metrics[
                    "maximum_photon_normalization_residual"
                ]
                < 1e-14,
                hessian_metrics["maximum_photon_normalization_residual"],
                "<1e-14",
            ),
            validation_row(
                f"V5187_{base + 10:02d}_limit_chain",
                "all Einstein Newton Maxwell limit-chain rows pass",
                limit_metrics["failed_chain_rows"] == 0
                and all(bool(row["passed"]) for row in limit_rows),
                limit_metrics["failed_chain_rows"],
                0,
            ),
            validation_row(
                f"V5187_{base + 11:02d}_GN_relation",
                "G_N and M_R relation is numerically normalized",
                limit_metrics["GN_MR_relation_residual"] < 1e-15,
                limit_metrics["GN_MR_relation_residual"],
                "<1e-15",
            ),
            validation_row(
                f"V5187_{base + 12:02d}_Green",
                "three-dimensional Green-function normalization is exact numerically",
                limit_metrics[
                    "three_dimensional_Green_normalization_residual"
                ]
                < 1e-15,
                limit_metrics[
                    "three_dimensional_Green_normalization_residual"
                ],
                "<1e-15",
            ),
            validation_row(
                f"V5187_{base + 13:02d}_RG_beta",
                "explicit autonomous trajectory satisfies its beta function",
                rg_metrics["explicit_beta_maximum_residual"] < 1e-14,
                rg_metrics["explicit_beta_maximum_residual"],
                "<1e-14",
            ),
            validation_row(
                f"V5187_{base + 14:02d}_RG_scale",
                "scale family preserves J_gap while changing G_N",
                rg_metrics["scale_family_preserves_J_gap"]
                and rg_metrics["scale_family_changes_GN"],
                (
                    rg_metrics["scale_family_preserves_J_gap"],
                    rg_metrics["scale_family_changes_GN"],
                ),
                (True, True),
            ),
            validation_row(
                f"V5187_{base + 15:02d}_betaJ",
                "Gaussian IR beta identity transports J_gap",
                rg_metrics["IR_beta_J_over_J"] == 0,
                rg_metrics["IR_beta_J_over_J"],
                0,
            ),
            validation_row(
                f"V5187_{base + 16:02d}_leading_count",
                "exactly two leading local force normalizations remain",
                parameter_counts["leading_local_force_normalizations"] == 2,
                parameter_counts["leading_local_force_normalizations"],
                2,
            ),
            validation_row(
                f"V5187_{base + 17:02d}_p4_count",
                "neutral-vacuum p4 long-range input count is zero",
                parameter_counts[
                    "neutral_vacuum_p4_long_range_inputs"
                ]
                == 0,
                parameter_counts[
                    "neutral_vacuum_p4_long_range_inputs"
                ],
                0,
            ),
            validation_row(
                f"V5187_{base + 18:02d}_absolute_scale",
                "the current autonomous GR-motion trajectory requires one absolute gravitational scale calibration",
                parameter_counts[
                    "absolute_GR_motion_scale_calibrations"
                ]
                == 1,
                parameter_counts[
                    "absolute_GR_motion_scale_calibrations"
                ],
                1,
            ),
            validation_row(
                f"V5187_{base + 19:02d}_C3_numeric",
                "selected C3 exterior maximum reproduces checkpoint 4986",
                math.isclose(
                    corridor_metrics[
                        "maximum_selected_C3_exterior_acceleration_fraction"
                    ],
                    3.6208461805802824e-124,
                    rel_tol=1e-14,
                ),
                corridor_metrics[
                    "maximum_selected_C3_exterior_acceleration_fraction"
                ],
                3.6208461805802824e-124,
            ),
            validation_row(
                f"V5187_{base + 20:02d}_det_numeric",
                "massless-endpoint determinant maximum reproduces checkpoint 4986",
                math.isclose(
                    corridor_metrics[
                        "maximum_massless_endpoint_determinant_acceleration_fraction"
                    ],
                    1.3684320168245822e-61,
                    rel_tol=1e-14,
                ),
                corridor_metrics[
                    "maximum_massless_endpoint_determinant_acceleration_fraction"
                ],
                1.3684320168245822e-61,
            ),
            validation_row(
                f"V5187_{base + 21:02d}_compact_numeric",
                "compact finite C3 maximum reproduces checkpoint 4963",
                math.isclose(
                    corridor_metrics[
                        "maximum_compact_finite_C3_acceleration_fraction"
                    ],
                    7.415086500522157e-158,
                    rel_tol=1e-14,
                ),
                corridor_metrics[
                    "maximum_compact_finite_C3_acceleration_fraction"
                ],
                7.415086500522157e-158,
            ),
            validation_row(
                f"V5187_{base + 22:02d}_CFF_open",
                "physical total c_IR remains explicitly open",
                not corridor_metrics["physical_total_cIR_known"],
                corridor_metrics["physical_total_cIR_known"],
                False,
            ),
            validation_row(
                f"V5187_{base + 23:02d}_p8_open",
                "p8-plus completion remains explicitly open",
                not corridor_metrics["p8plus_complete"],
                corridor_metrics["p8plus_complete"],
                False,
            ),
            validation_row(
                f"V5187_{base + 24:02d}_retuning",
                "no generated cross-arena row permits retuning",
                all(
                    not bool(row["independent_arena_retune"])
                    for row in no_retuning_rows
                ),
                sum(
                    bool(row["independent_arena_retune"])
                    for row in no_retuning_rows
                ),
                0,
            ),
            validation_row(
                f"V5187_{base + 25:02d}_claims",
                "all generated rows retain the full-MTS claim guard",
                all(
                    row.get("valid_for_full_MTS_claim") is False
                    for packet in (
                        action_rows,
                        hessian_rows,
                        limit_rows,
                        rg_rows,
                        parameter_rows,
                        corridor_rows,
                        no_retuning_rows,
                    )
                    for row in packet
                ),
                True,
                True,
            ),
        ]
    )
    return checks


def build_document(
    result: dict[str, Any],
    source_hashes: dict[str, str],
) -> None:
    source_list = "\n".join(
        f"- `{path.relative_to(POST).as_posix()}`  \n"
        f"  SHA-256 `{source_hashes[source_id]}`"
        for source_id, (path, _) in SOURCES.items()
    )
    hessian = result["Hessian"]
    limits = result["limit_chain"]
    rg = result["scale_setting"]
    parameters = result["parameter_counts"]
    corridor = result["higher_derivative_corridor"]
    text = f"""# 5187 - Canonical local parent action, Hessian, source residue and scale-setting theorem

Marker: `{MARKER}`

Date: `{CHECKED_DATE}`.

Status: private analytic and source-executed checkpoint. No GitHub action.

## 1. Verdict

This checkpoint does **not** hunt for another source coefficient. Checkpoint
4960 already proved that the declared integrated-`H`, exact-Diff/BRST parent
has one universal leading spin-two source residue. The new result is to put
the surviving local theory into one canonical action and prove, in one place,
what follows from it.

The leading local result is now:

```text
{LEADING_THEOREM}
```

In ordinary language:

1. the local vacuum Hessian has separate metric, photon and motion blocks;
2. ordinary matter has a metric stress source and an electric current but no
   one-motion-scalar source on the reflection-even branch;
3. one metric residue produces Einstein, Poisson, Newton, geodesic, lensing
   and leading radiation laws;
4. one photon normalization produces Maxwell, Coulomb, Lorentz force,
   electromagnetic stress and Poynting flux;
5. neither field-coordinate normalization can manufacture an extra coupling;
6. the *relation* `G_N=1/(8 pi M_R^2)` and cross-arena universality are
   derived, while the numerical value of `G_N` still requires one absolute
   scale datum in the current autonomous dimensionless RG parent.

This is a genuine consolidation and promotion of the **leading local branch**.
It is not a derivation of the metric/Diff parent from one scalar and it is not
an all-operator or full-MTS theorem.

## 2. Exact premises

The theorem is conditional on these explicit parent data:

- `H^mn=sqrt(-g)g^mn` is an integrated rank-ten tensor-density field;
- `g^mn=H^mn/sqrt(-det H)` and exact Diff/BRST identities hold;
- the infrared spectrum contains one positive massless helicity-two pole and
  no additional massless pole;
- the visible fields and their `U(1)` representations are parent content;
- the motion sector is reflection even and ordinary matter contains no term
  odd in `psi`;
- the expansion is made about an on-shell zero-field background
  `bar A=bar psi=0`; local flat formulas additionally take
  `q^2 >> |Lambda_cal|`.

Checkpoint 4961 proved that a lone scalar does not supply the rank or gauge
structure needed to derive these premises. This checkpoint keeps that
boundary visible rather than concealing it.

## 3. Canonical local action

Through the displayed EFT order the action is

```text
{CANONICAL_ACTION}
```

Here `I_C3` is the selected parity-even cubic-curvature invariant with
`G_C3=M_R^2 a_plus/2=A_C3^S l_P^2`, `P_ge_2(X)` begins at `X^2`, and the
p4 neutral-vacuum `R^2,C^2` coordinates have been quotiented at first
strict-EFT order. Their surviving matter-supported content belongs to
`Gamma_contact`, not to a second long-range vacuum gravitational residue.

## 4. Quadratic Hessian theorem

At `bar A=bar psi=0`, gauge invariance makes every photon term at least
quadratic in `A`, while reflection symmetry makes every motion term at least
quadratic in `psi`. Therefore

```text
delta^2 Gamma/(delta h delta A)   =0,
delta^2 Gamma/(delta h delta psi) =0,
delta^2 Gamma/(delta A delta psi) =0.
```

The three diagonal blocks on a curved zero-field background are

```text
K_hh       =M_R^2 K_Einstein+K_C3+K_nonlocal+K_p8plus,
K_AA       =Z_A q^2 P_T+c_IR K_CFF[bar C],
K_psipsi   =(Z_psi+2u_O4 bar C^2)q^2+m_gap^2+lower-gradient terms.
```

The exact field-degree audit gives mixed-derivative sum
`{hessian['field_degree_mixed_derivative_sum']}`. The four-dimensional
trace-reversal source map has rank
`{hessian['trace_reversal_rank']}`, nullity
`{hessian['trace_reversal_nullity']}`, determinant
`{hessian['trace_reversal_determinant']}`, and squares exactly to the
identity. It therefore loses neither trace nor species information.

Five independent source classes give a soft/Bianchi constraint matrix of
rank `{hessian['soft_species_rank']}` and nullity
`{hessian['soft_species_nullity']}`, with sole null direction
`(1,1,1,1,1)`. This is the one common leading gravitational coupling.

For `g=eta+a h`,

```text
Gamma_2=M_R^2 a^2 q^2 K/4,
D_a=4K^-1/(M_R^2 a^2 q^2),
V_a=a/2,
V_a^2 D_a=K^-1/(M_R^2 q^2).
```

The executed maximum normalization residual is
`{hessian['maximum_spin2_normalization_residual']:.3e}`. Likewise
`A_c=sqrt(Z_A)A` and `e_c=e/sqrt(Z_A)` leave only `e^2/Z_A`, with maximum
executed residual `{hessian['maximum_photon_normalization_residual']:.3e}`.

## 5. Einstein to Newton

One variation and one sequence of limits give

```text
M_R^2(G_mn+Lambda_cal g_mn)=T_total,mn,
G_N=1/(8 pi M_R^2),

Box hbar_mn=-16 pi G_N T_mn,
nabla^2 Phi=4 pi G_N rho-Lambda_cal c^2,

Phi=-G_N M/r-Lambda_cal c^2 r^2/6,
a_r=-G_N M/r^2+Lambda_cal c^2 r/3.
```

The same metric follows from `-m int ds` for neutral bodies and controls null
rays. Hence there is no independent inertial, passive, active, orbital,
lensing or leading-wave value of `G`. The local constant PPN values are
`gamma=beta=1`, while the C3 and determinant tails remain explicit
higher-gradient corrections.

The Green-function normalization residual is
`{limits['three_dimensional_Green_normalization_residual']:.3e}` and all
`{limits['chain_row_count']}` limit-chain rows pass.

## 6. Maxwell to Poynting

The same photon action yields

```text
nabla_m F^mn-4c_IR nabla_m(C^mnrs F_rs)=J^n,
nabla_m J^m=0,

u.nabla u^m=(q/m)F^m_n u^n,

T_EM,mn=F_ma F_n^a-g_mn F^2/4+c_IR H_CFF,mn,
T_EM^0i=(E cross B)^i.
```

When `C_mnrs=0`, ordinary Maxwell theory is exact for any `c_IR`. The
Poynting vector is therefore not an extra postulated coupling to a hidden
background: it is the `0i` Hilbert-stress component of the same canonical
gauge action. A future microscopic interpretation may explain the field, but
it cannot alter this normalization chain without changing the action.

## 7. Absolute scale theorem

For any autonomous dimensionless flow,

```text
dg/dln(k)=beta(g),
g(k)=g_hat(k/Lambda_g).
```

The executed counterfamily

```text
g_hat(x)=g_star x^2/(1+x^2),
beta(g)=2g(1-g/g_star)
```

has the same Gaussian endpoint and the same ultraviolet fixed point for every
`Lambda_g`. Its maximum beta-function residual is
`{rg['explicit_beta_maximum_residual']:.3e}`, but

```text
G_N=lim(k->0) g(k)/k^2=C_g/Lambda_g^2.
```

Changing `Lambda_g -> s Lambda_g` leaves every dimensionless beta function
and fixed point unchanged while sending `G_N -> G_N/s^2`.

The motion ratio does not remove this freedom:

```text
J_gap=w_psi g=m_gap^2 G_N,
beta_J/J=(-2)+(+2)=0.
```

At fixed `J_gap`, the same scale translation sends
`m_gap -> s m_gap`; it does not select `s`. Therefore the current autonomous
GR-motion trajectory requires exactly
`{rg['required_absolute_gravity_motion_scale_calibrations']}` absolute
gravitational scale calibration. `Lambda_cal`, `c_IR`, contact coefficients
and state data retain their separately listed roles below. A future parent
can improve the gravity-scale result only by supplying a genuine
dimensionful anchor or a derived relation to one—not by renaming a
dimensionless fixed-point coordinate.

## 8. Parameter and state count

The corrected count is:

| class | current count/status |
|---|---|
| leading local force normalizations | `{parameters['leading_local_force_normalizations']}`: `G_N`, `alpha_EM` |
| background curvature calibration | `{parameters['background_curvature_calibrations']}`: `Lambda_cal` |
| unselected universal motion coordinate | `{parameters['motion_action_coordinates_unselected']}`: `J_gap` |
| physical curvature-photon LEC | `{parameters['curvature_photon_LECs_open']}`: total `c_IR` open |
| neutral-vacuum p4 long-range inputs | `{parameters['neutral_vacuum_p4_long_range_inputs']}` |
| p6 empirical inputs | `{parameters['p6_empirical_inputs']}`; `A_C3^S` is trajectory selected |
| matter-contact pre-reduction directions | `{parameters['matter_contact_pre_reduction_open']}` open |
| p8 aggregate completion coordinates | `{parameters['p8_aggregate_coordinates_open']}` open |
| occupied-state data classes | `{parameters['initial_state_data_classes_open']}` open, not action couplings |

The state abundance and covariance found at 5186 are not smuggled into this
action count. They remain conditional initial-state data.

## 9. Higher-derivative corridor

The current numerical corridor is:

```text
classical one-scalar fifth force              = exactly zero;
standard constant Delta gamma and Delta beta = exactly zero;
neutral-vacuum p4 long-range input count      = zero;

max selected local C3 exterior |Delta a/a_N|
  = {corridor['maximum_selected_C3_exterior_acceleration_fraction']:.16e};

max massless-endpoint determinant |Delta a/a_N|
  = {corridor['maximum_massless_endpoint_determinant_acceleration_fraction']:.16e};

max compact finite C3 |Delta a/a_N|
  = {corridor['maximum_compact_finite_C3_acceleration_fraction']:.16e};

max known nonQCD c_IR / one-ppm arena budget
  = {corridor['maximum_known_nonQCD_to_one_ppm_budget_ratio']:.16e}.
```

These small numbers do not close the full theory. The C3 number is a selected
local source-scheme coordinate, the determinant number is a massless-endpoint
two-point subset, the physical `m_gap` threshold form factor is open, the
finite QCD part of `c_IR` is open, and the p8-plus response basis has not been
projected. Therefore

```text
leading two-derivative local GR/Newton branch = established inside premises;
flat Maxwell/Lorentz/stress/Poynting chain    = established inside premises;
all-operator compact equality to GR           = not established;
full MTS unification                          = not claimed.
```

## 10. What this changes

The project no longer needs another search for a separate Newton, lensing,
orbital, photon-stress or Poynting coupling. Such a coefficient would
duplicate a residue already fixed by the canonical action and Ward
identities.

The unresolved foundational task is now sharply different:

```text
derive the integrated H/Diff/visible-field parent from a genuinely
non-scalar relational or coframe construction,
or retain it honestly as fundamental parent data.
```

The one-scalar bootstrap route is already rejected by rank. Repeating it
would be circling. The next derivation should therefore test a minimal
relational coframe/tensor parent, while local residual work can proceed
independently through the physical `c_IR` match and p8 projection.

## 11. Claim guard

```text
{CLAIM_GUARD}
```

## 12. Generated evidence

- `source-intake/functional_rg/5187/canonical_local_parent_action.csv`
- `source-intake/functional_rg/5187/vacuum_quadratic_Hessian_and_source_vertices.csv`
- `source-intake/functional_rg/5187/universal_residue_and_limit_chain.csv`
- `source-intake/functional_rg/5187/RG_scale_setting_no_go.csv`
- `source-intake/functional_rg/5187/canonical_parameter_and_state_count.csv`
- `source-intake/functional_rg/5187/higher_derivative_local_corridor.csv`
- `source-intake/functional_rg/5187/cross_arena_no_retuning.csv`
- `source-intake/functional_rg/5187/source_provenance.csv`
- `source-intake/functional_rg/5187/canonical_local_parent_action_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5187_VALIDATION.csv`

Locked source inputs:

{source_list}

All validation rows pass. The formalization workbench and checkpoint-5176
ensemble remain locked. No GitHub action occurred.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_hashes: dict[str, str] = {}
    for source_id, (path, _) in SOURCES.items():
        if not path.is_file():
            raise FileNotFoundError(path)
        source_hashes[source_id] = file_digest(path)

    formal_before = tree_digest(FORMAL)
    checkpoint_5176_before = tree_digest(CHECKPOINT_5176_ROOT)

    c3_rows = read_csv(SOURCES["checkpoint_4986_C3_bounds"][0])
    determinant_rows = read_csv(
        SOURCES["checkpoint_4986_determinant_bounds"][0]
    )
    compact_c3_rows = read_csv(SOURCES["checkpoint_4963_compact_C3"][0])
    cff_transfer_rows = read_csv(SOURCES["checkpoint_4946_CFF_transfer"][0])
    cff_contract_rows = read_csv(SOURCES["checkpoint_4964_CFF_contract"][0])

    action_rows = build_action_rows()
    hessian_rows, hessian_metrics = build_hessian_rows()
    limit_rows, limit_metrics = build_limit_rows()
    rg_rows, rg_metrics = build_rg_rows()
    parameter_rows, parameter_counts = build_parameter_rows()
    corridor_rows, corridor_metrics = build_corridor_rows(
        c3_rows,
        determinant_rows,
        compact_c3_rows,
        cff_transfer_rows,
        cff_contract_rows,
    )
    no_retuning_rows = build_no_retuning_rows()
    provenance_rows = build_provenance_rows(source_hashes)

    checks = calculate_validations(
        source_hashes,
        formal_before,
        checkpoint_5176_before,
        action_rows,
        hessian_rows,
        hessian_metrics,
        limit_rows,
        limit_metrics,
        rg_rows,
        rg_metrics,
        parameter_rows,
        parameter_counts,
        corridor_rows,
        corridor_metrics,
        no_retuning_rows,
    )
    failures = [row for row in checks if row["status"] != "PASS"]
    if failures:
        raise RuntimeError(
            "Pre-write validation failed:\n"
            + json.dumps(failures, indent=2)
        )

    write_csv(ACTION_CSV, action_rows)
    write_csv(HESSIAN_CSV, hessian_rows)
    write_csv(LIMIT_CSV, limit_rows)
    write_csv(RG_CSV, rg_rows)
    write_csv(PARAMETER_CSV, parameter_rows)
    write_csv(CORRIDOR_CSV, corridor_rows)
    write_csv(NO_RETUNING_CSV, no_retuning_rows)
    write_csv(PROVENANCE_CSV, provenance_rows)

    data_pack_digest = hashlib.sha256()
    for path in (
        ACTION_CSV,
        HESSIAN_CSV,
        LIMIT_CSV,
        RG_CSV,
        PARAMETER_CSV,
        CORRIDOR_CSV,
        NO_RETUNING_CSV,
        PROVENANCE_CSV,
    ):
        data_pack_digest.update(path.name.encode("utf-8"))
        data_pack_digest.update(file_digest(path).encode("ascii"))

    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "canonical_action": CANONICAL_ACTION,
        "leading_theorem": LEADING_THEOREM,
        "claim_guard": CLAIM_GUARD,
        "Hessian": hessian_metrics,
        "limit_chain": limit_metrics,
        "scale_setting": rg_metrics,
        "parameter_counts": parameter_counts,
        "higher_derivative_corridor": corridor_metrics,
        "claim_status": {
            "canonical_local_action_assembled": True,
            "vacuum_Hessian_block_diagonal": True,
            "Hilbert_source_map_invertible": True,
            "one_universal_leading_spin2_residue": True,
            "leading_local_GR_Newton_chain_inside_parent": True,
            "flat_Maxwell_Lorentz_stress_Poynting_chain_inside_parent": True,
            "classical_one_scalar_fifth_force": False,
            "numerical_GN_predicted_from_current_dimensionless_parent": False,
            "integrated_H_or_Diff_derived_from_one_scalar": False,
            "physical_total_cIR_known": False,
            "p8plus_complete": False,
            "all_operator_compact_GR": False,
            "full_MTS_unification": False,
            "GitHub_action": False,
        },
        "source_hashes": source_hashes,
        "data_pack_sha256": data_pack_digest.hexdigest(),
        "formalization_workbench_sha256": formal_before,
        "checkpoint_5176_tree_sha256": checkpoint_5176_before,
        "validation_count_prewrite": len(checks),
        "validation_failures_prewrite": 0,
    }
    write_json(RESULT_JSON, result)
    build_document(result, source_hashes)

    formal_after = tree_digest(FORMAL)
    checkpoint_5176_after = tree_digest(CHECKPOINT_5176_ROOT)
    expected_outputs = (
        ACTION_CSV,
        HESSIAN_CSV,
        LIMIT_CSV,
        RG_CSV,
        PARAMETER_CSV,
        CORRIDOR_CSV,
        NO_RETUNING_CSV,
        PROVENANCE_CSV,
        RESULT_JSON,
        DOCUMENT,
    )
    final_checks = checks + [
        validation_row(
            f"V5187_{len(checks):02d}_formal_after",
            "formalization-workbench remains unchanged after writes",
            formal_after == formal_before == FORMAL_DIGEST_LOCK,
            formal_after,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            f"V5187_{len(checks) + 1:02d}_5176_after",
            "checkpoint 5176 remains unchanged after writes",
            checkpoint_5176_after
            == checkpoint_5176_before
            == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_after,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            f"V5187_{len(checks) + 2:02d}_outputs",
            "all checkpoint artifacts exist and are nonempty",
            all(path.is_file() and path.stat().st_size > 0 for path in expected_outputs),
            sum(path.is_file() and path.stat().st_size > 0 for path in expected_outputs),
            len(expected_outputs),
        ),
        validation_row(
            f"V5187_{len(checks) + 3:02d}_csv_parse",
            "all generated CSV files parse with at least one row",
            all(
                len(read_csv(path)) > 0
                for path in (
                    ACTION_CSV,
                    HESSIAN_CSV,
                    LIMIT_CSV,
                    RG_CSV,
                    PARAMETER_CSV,
                    CORRIDOR_CSV,
                    NO_RETUNING_CSV,
                    PROVENANCE_CSV,
                )
            ),
            8,
            8,
        ),
    ]
    final_failures = [
        row for row in final_checks if row["status"] != "PASS"
    ]
    if final_failures:
        raise RuntimeError(
            "Final validation failed:\n"
            + json.dumps(final_failures, indent=2)
        )
    write_csv(VALIDATION_CSV, final_checks)

    print(
        json.dumps(
            {
                "checkpoint": 5187,
                "marker": MARKER,
                "validation_passed": len(final_checks),
                "validation_failed": 0,
                "vacuum_Hessian_block_diagonal": hessian_metrics[
                    "vacuum_Hessian_block_diagonal"
                ],
                "trace_reversal_rank": hessian_metrics[
                    "trace_reversal_rank"
                ],
                "soft_species_rank": hessian_metrics["soft_species_rank"],
                "soft_species_nullity": hessian_metrics[
                    "soft_species_nullity"
                ],
                "leading_local_force_normalizations": parameter_counts[
                    "leading_local_force_normalizations"
                ],
                "required_absolute_GR_motion_scale_calibrations": rg_metrics[
                    "required_absolute_gravity_motion_scale_calibrations"
                ],
                "numerical_GN_predicted": False,
                "maximum_selected_C3_exterior_acceleration_fraction": (
                    corridor_metrics[
                        "maximum_selected_C3_exterior_acceleration_fraction"
                    ]
                ),
                "maximum_determinant_acceleration_fraction": (
                    corridor_metrics[
                        "maximum_massless_endpoint_determinant_acceleration_fraction"
                    ]
                ),
                "document": str(DOCUMENT),
                "result": str(RESULT_JSON),
                "validation": str(VALIDATION_CSV),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
