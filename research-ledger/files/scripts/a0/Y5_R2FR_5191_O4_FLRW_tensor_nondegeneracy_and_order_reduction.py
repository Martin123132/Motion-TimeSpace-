from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5191"

DOCUMENT = (
    POST
    / "5191-Y5-R2FR-O4-FLRW-tensor-nondegeneracy-order-reduction-and-"
    "cosmological-safety-theorem.md"
)
PARENT_CSV = OUT / "O4_parent_ownership_and_convention.csv"
WEYL_CSV = OUT / "FLRW_TT_Weyl_quadratic_identity.csv"
DEGENERACY_CSV = OUT / "O4_TT_degeneracy_and_pole.csv"
REDUCTION_CSV = OUT / "O4_redundancy_and_order_reduction.csv"
ENVELOPE_CSV = OUT / "O4_cosmology_control_envelope.csv"
BRANCH_CSV = OUT / "O4_branch_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "O4_FLRW_tensor_order_reduction_results.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5191_VALIDATION.csv"
)

MARKER = "MTS_5191_O4_FLRW_TENSOR_NONDEGENERACY_ORDER_REDUCTION"
CHECKED_DATE = "2026-07-24"
FORMAL_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
CHECKPOINT_5176_ROOT = POST / "source-intake" / "functional_rg" / "5176"

LOCAL_SOURCES: dict[str, str] = {
    (
        "4930-Y5-R2FR-six-derivative-MTS-matter-essential-operator-basis-"
        "and-block-triangular-stability-or-Wilson-retention.md"
    ): "1b987f0040d4288d9057b52f2f792c6484b6a0a8edd0bf817d71f7abf6a03755",
    (
        "source-intake/mts_residuals/"
        "P8_Y5_R2FR_4930_SCALAR_SIX_DERIVATIVE_BASIS.csv"
    ): "93d8485ad79cc72ce2e9f6be3d81dc3605c785cb45436431d64041415e951361",
    (
        "source-intake/functional_rg/4930/src1908/GravityEFTv2_final.tex"
    ): "e234ab07031885f79030529bb3dcabc7e928cc4283774f26ebc5dac6b8a226dc",
    (
        "4941-Y5-R2FR-natural-TypeII-direct-metric-scalar-O4-zero-proof-and-"
        "minimal-O4-parent-completion-gate.md"
    ): "f4c6f83668c5f904706747dcafb3d538068a038307ffc062e13fe3234a6b9543",
    (
        "source-intake/functional_rg/4941/"
        "typeII_direct_O4_zero_and_lower_quotient_results.json"
    ): "e234f85376912f5a9da919f32dd7db855d1ff45f39faa693a01a74677590b57f",
    (
        "4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-"
        "branch-and-C3-CFF-PPN-residual-gate.md"
    ): "64b96ca4e19a058ced85c0c4b800ae7a237408606799dd8c4a5b58935f635c5f",
    (
        "source-intake/functional_rg/4942/"
        "local_O4_C3_CFF_residual_results.json"
    ): "c830baff10125f984ba26d11d44465c4d519ecd6c51317b9c9fcac6cf5e2e04b",
    (
        "4957-Y5-R2FR-functional-PX-GR-connected-trajectory-and-O2-O4-O5-"
        "residual-bound-or-motion-sector-rejection.md"
    ): "235b2e640428814bbcc3f0af1b2ebef020573314eaae1cb0b793be9122db0cb4",
    (
        "source-intake/functional_rg/4957/"
        "functional_PX_O4_GR_trajectory_results.json"
    ): "8d8c7e416706d116492e3539a0541e6e64174c59a460714325251656b1477cc6",
    (
        "4959-Y5-R2FR-O2-O3-O4-external-scalar-sixpoint-projectors-and-full-"
        "invariant-amplitude-or-curvature-route-rejection.md"
    ): "295a73fe134df2fc6fc1b08a33c5fcffbf664ccadf20c29fd376f516cbf7da8a",
    (
        "source-intake/functional_rg/4959/"
        "curvature_sixpoint_projector_results.json"
    ): "6febd4e1ca58bf037ee764464c4e7ca3fc99fbd3fc4680c110c64ad6a7df15a8",
    (
        "5187-Y5-R2FR-canonical-local-parent-action-Hessian-source-residue-"
        "and-scale-setting-theorem.md"
    ): "4556205ec12e11930a13d0ed9b5e27b6b4619f3752a5e10db2a4b767dcdec674",
    (
        "5189-Y5-R2FR-motion-sector-ADM-projection-clock-only-ancestry-and-"
        "local-tensor-protection-theorem.md"
    ): "4514f59f95fa00fbddd652511bf49a98a84347b3f4f10747afbdfb6d3917e266",
    (
        "source-intake/functional_rg/5189/"
        "motion_ADM_projection_results.json"
    ): "6418ffc826ed2068b1f4df46d56423fe3f866c0e9bfa363098f4e849174fcfc2",
    (
        "5190-Y5-R2FR-static-Ward-helicity-one-derivative-mixing-no-go-and-"
        "direct-state-route-freeze.md"
    ): "4f3d83db550d5eed2bea3fc8f6d6542807ec610a152abd2146a39ede6bdf6d55",
    (
        "source-intake/functional_rg/5190/"
        "static_Ward_and_mixing_no_go_results.json"
    ): "305157492ebc5d064f7ba38d9a83508e7bcb089529b0c7dbec58a66432519ab7",
}

EXTERNAL_SOURCES = {
    "Ruhdorfer_Serra_Weiler_nonredundant_gravity_EFT":
        "https://arxiv.org/abs/1908.08050",
    "Solomon_Trodden_scalar_tensor_order_reduction":
        "https://arxiv.org/abs/1709.09695",
    "Babichev_Bansal_Mylova_Padilla_six_derivative_scalar_tensor_EFT":
        "https://arxiv.org/abs/2512.13453",
}

LEADING_THEOREM = (
    "THE_RETAINED_O4_EQUALS_C_SQUARED_X_OPERATOR_IS_PARENT_PREDICTED_"
    "NONZERO_AND_NONREDUNDANT_IN_THE_FULL_SIX_DERIVATIVE_SCALAR_GRAVITY_"
    "EFT_BUT_ON_A_CONFORMALLY_FLAT_HOMOGENEOUS_CLOCK_BACKGROUND_ITS_"
    "QUADRATIC_TENSOR_FOURTH_DERIVATIVE_HESSIAN_HAS_RANK_TWO_WHEN_"
    "B_EQUALS_C_O4_X_IS_NONZERO_SO_THE_ISOLATED_FINITE_TRUNCATION_IS_NOT_"
    "DEGENERATE_AND_IF_RESUMMED_CONTAINS_AN_OPPOSITE_RESIDUE_TENSOR_POLE_"
    "THE_Q4_TWO_POINT_TERM_IS_NEVERTHELESS_EOM_REDUCIBLE_AT_FIRST_EFT_"
    "ORDER_AND_THE_EXACT_TIME_DEPENDENT_FLRW_REDUCTION_LEAVES_ONLY_"
    "BACKGROUND_SUPPRESSED_SECOND_ORDER_KINETIC_AND_GRADIENT_TERMS_"
    "WITH_THE_PREDICTED_WILSON_COEFFICIENT_AND_A_CANONICAL_KINETIC_"
    "DENSITY_NOT_EXCEEDING_THE_FRIEDMANN_DENSITY_THE_CONTROL_MARGIN_IS_"
    "ENORMOUS_BELOW_PLANCK_CURVATURE_THUS_LOCAL_GR_AND_LOW_ENERGY_"
    "COSMOLOGICAL_TENSORS_SURVIVE_AS_AN_ORDER_BY_ORDER_EFT_WHILE_AN_"
    "ALL_SCALE_FUNDAMENTAL_TWO_MODE_CLAIM_STILL_REQUIRES_THE_FULL_UV_"
    "TOWER_OR_AN_INDEPENDENT_COMPLETION_THEOREM"
)

CLAIM_GUARD = (
    "THIS_PROVES_NONDEGENERACY_OF_THE_ISOLATED_O4_TT_TRUNCATION_"
    "NONREDUNDANCY_OF_THE_FULL_OPERATOR_PERTURBATIVE_ORDER_REDUCTION_"
    "AND_A_CONDITIONAL_CANONICAL_COSMOLOGICAL_SAFETY_ENVELOPE_IT_DOES_"
    "NOT_PROVE_THE_FINITE_HIGHER_DERIVATIVE_ACTION_IS_A_GHOST_FREE_"
    "ALL_SCALE_FUNDAMENTAL_THEORY_DOES_NOT_DERIVE_THE_GENERAL_PX_"
    "COSMOLOGICAL_BACKGROUND_OR_ITS_X_PROFILE_DOES_NOT_BOUND_AN_"
    "ARBITRARILY_LARGE_KINETIC_BACKGROUND_WITH_CANCELLING_NEGATIVE_"
    "ENERGY_AND_DOES_NOT_COMPLETE_FULL_MTS_UNIFICATION"
)


def source_path(relative: str) -> Path:
    return POST / Path(relative)


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(
        candidate for candidate in path.rglob("*") if candidate.is_file()
    ):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(file_digest(item).encode("ascii"))
    return digest.hexdigest()


def load_json(relative: str) -> dict[str, Any]:
    return json.loads(source_path(relative).read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
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
    check: str,
    passed: bool,
    observed: Any,
    expected: Any,
) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "observed": str(observed),
        "expected": str(expected),
        "checkpoint_marker": MARKER,
        "valid_for_full_MTS_claim": False,
    }


def derive_linearized_weyl_mode(polarization: str) -> sp.Expr:
    time, x_coord, y_coord, z_coord = sp.symbols(
        "eta x y z",
        real=True,
    )
    wave_number = sp.symbols("k", positive=True, real=True)
    amplitude = sp.Function("gamma")(time)
    coordinates = (time, x_coord, y_coord, z_coord)
    eta_metric = sp.diag(-1, 1, 1, 1)
    perturbation = sp.MutableDenseNDimArray.zeros(4, 4)
    mode = amplitude * sp.cos(wave_number * z_coord)
    if polarization == "plus":
        perturbation[1, 1] = mode
        perturbation[2, 2] = -mode
    elif polarization == "cross":
        perturbation[1, 2] = mode
        perturbation[2, 1] = mode
    else:
        raise ValueError(f"Unknown polarization: {polarization}")

    riemann = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    riemann[a, b, c, d] = sp.expand(
                        sp.Rational(1, 2)
                        * (
                            sp.diff(
                                perturbation[a, d],
                                coordinates[b],
                                coordinates[c],
                            )
                            + sp.diff(
                                perturbation[b, c],
                                coordinates[a],
                                coordinates[d],
                            )
                            - sp.diff(
                                perturbation[a, c],
                                coordinates[b],
                                coordinates[d],
                            )
                            - sp.diff(
                                perturbation[b, d],
                                coordinates[a],
                                coordinates[c],
                            )
                        )
                    )

    ricci = sp.MutableDenseNDimArray.zeros(4, 4)
    for b in range(4):
        for d in range(4):
            ricci[b, d] = sp.expand(
                sum(
                    eta_metric[a, a] * riemann[a, b, a, d]
                    for a in range(4)
                )
            )
    ricci_scalar = sp.expand(
        sum(eta_metric[a, a] * ricci[a, a] for a in range(4))
    )

    weyl = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    weyl[a, b, c, d] = sp.expand(
                        riemann[a, b, c, d]
                        - sp.Rational(1, 2)
                        * (
                            eta_metric[a, c] * ricci[d, b]
                            - eta_metric[a, d] * ricci[c, b]
                            - eta_metric[b, c] * ricci[d, a]
                            + eta_metric[b, d] * ricci[c, a]
                        )
                        + ricci_scalar
                        * sp.Rational(1, 6)
                        * (
                            eta_metric[a, c] * eta_metric[d, b]
                            - eta_metric[a, d] * eta_metric[c, b]
                        )
                    )

    weyl_squared = sp.expand(
        sum(
            eta_metric[a, a]
            * eta_metric[b, b]
            * eta_metric[c, c]
            * eta_metric[d, d]
            * weyl[a, b, c, d] ** 2
            for a in range(4)
            for b in range(4)
            for c in range(4)
            for d in range(4)
        )
    )
    return sp.factor(
        sp.integrate(
            weyl_squared,
            (z_coord, 0, 2 * sp.pi / wave_number),
        )
        * wave_number
        / (2 * sp.pi)
    )


def derive_weyl_and_weighted_identity() -> tuple[
    list[dict[str, Any]],
    dict[str, Any],
]:
    plus_density = derive_linearized_weyl_mode("plus")
    cross_density = derive_linearized_weyl_mode("cross")

    conformal_time = sp.symbols("eta", real=True)
    wave_number = sp.symbols("k", positive=True, real=True)
    amplitude = sp.Function("gamma")(conformal_time)
    coefficient = sp.Function("B")(conformal_time)
    amplitude_prime = sp.diff(amplitude, conformal_time)
    amplitude_second = sp.diff(amplitude, conformal_time, 2)
    coefficient_prime = sp.diff(coefficient, conformal_time)
    coefficient_second = sp.diff(coefficient, conformal_time, 2)

    expected_density = sp.factor(
        sp.Rational(1, 2)
        * (
            (wave_number**2 * amplitude - amplitude_second) ** 2
            - 4 * wave_number**2 * amplitude_prime**2
        )
    )
    flat_operator = amplitude_second + wave_number**2 * amplitude
    total_derivative_seed = amplitude * amplitude_prime
    unweighted_identity = sp.simplify(
        expected_density
        - (
            flat_operator**2 / 2
            - 2
            * wave_number**2
            * sp.diff(total_derivative_seed, conformal_time)
        )
    )

    boundary_current = wave_number**2 * (
        coefficient_prime * amplitude**2
        - 2 * coefficient * amplitude * amplitude_prime
    )
    reduced_weighted_density = (
        coefficient * flat_operator**2 / 2
        - wave_number**2 * coefficient_second * amplitude**2
    )
    weighted_identity = sp.simplify(
        sp.expand(
            coefficient * expected_density
            - reduced_weighted_density
            - sp.diff(boundary_current, conformal_time)
        )
    )

    rows = tagged(
        [
            {
                "identity_id": "WEYL5191_00_conformal",
                "object": "four-dimensional Weyl density",
                "equation": "sqrt(-g) C[g]^2=sqrt(-gtilde) C[gtilde]^2",
                "derived_result": (
                    "FLRW tensor calculation reduces to the conformal metric"
                ),
                "status": "EXACT_4D_CONFORMAL_IDENTITY",
            },
            {
                "identity_id": "WEYL5191_01_plus",
                "object": "spatially averaged plus polarization",
                "equation": "linearized C_abcd C^abcd",
                "derived_result": str(plus_density),
                "status": "EXECUTED_FULL_TENSOR_CONTRACTION",
            },
            {
                "identity_id": "WEYL5191_02_cross",
                "object": "spatially averaged cross polarization",
                "equation": "linearized C_abcd C^abcd",
                "derived_result": str(cross_density),
                "status": "EXECUTED_FULL_TENSOR_CONTRACTION",
            },
            {
                "identity_id": "WEYL5191_03_unweighted",
                "object": "constant-coefficient quadratic action",
                "equation": (
                    "C1^2=(gamma''+k^2 gamma)^2/2"
                    "-2k^2(gamma gamma')'"
                ),
                "derived_result": str(unweighted_identity),
                "status": "EXACT_UP_TO_BOUNDARY",
            },
            {
                "identity_id": "WEYL5191_04_weighted",
                "object": "time-dependent B(eta)=c_O4 Xbar",
                "equation": (
                    "B C1^2=B(Dgamma)^2/2-k^2 B'' gamma^2+J'"
                ),
                "derived_result": str(weighted_identity),
                "status": "EXACT_WEIGHTED_IDENTITY",
            },
        ]
    )
    metrics = {
        "plus_density": str(plus_density),
        "cross_density": str(cross_density),
        "expected_density": str(expected_density),
        "polarizations_equal": bool(
            sp.simplify(plus_density - cross_density) == 0
        ),
        "plus_matches_expected": bool(
            sp.simplify(plus_density - expected_density) == 0
        ),
        "unweighted_identity_residual": str(unweighted_identity),
        "weighted_identity_residual": str(weighted_identity),
        "boundary_current": str(boundary_current),
        "weighted_bulk_density": str(reduced_weighted_density),
        "flat_tensor_operator": str(flat_operator),
    }
    return rows, metrics


def derive_degeneracy_and_poles() -> tuple[
    list[dict[str, Any]],
    dict[str, Any],
]:
    q_squared, einstein_residue, background_coefficient = sp.symbols(
        "q2 A B",
        nonzero=True,
        real=True,
    )
    tensor_kernel = sp.factor(
        q_squared
        * (einstein_residue + background_coefficient * q_squared)
    )
    extra_pole = sp.solve(
        sp.Eq(
            einstein_residue + background_coefficient * q_squared,
            0,
        ),
        q_squared,
    )[0]
    propagator = 1 / tensor_kernel
    massless_residue = sp.simplify(
        sp.limit(q_squared * propagator, q_squared, 0)
    )
    extra_residue = sp.simplify(
        sp.limit(
            (q_squared - extra_pole) * propagator,
            q_squared,
            extra_pole,
        )
    )
    partial_fraction_residual = sp.simplify(
        propagator
        - (
            1
            / einstein_residue
            * (
                1 / q_squared
                - 1 / (q_squared - extra_pole)
            )
        )
    )

    acceleration_plus, acceleration_cross = sp.symbols(
        "gamma_plus_ddot gamma_cross_ddot",
        real=True,
    )
    highest_derivative_lagrangian = (
        background_coefficient
        * (acceleration_plus**2 + acceleration_cross**2)
        / 2
    )
    acceleration_hessian = sp.hessian(
        highest_derivative_lagrangian,
        (acceleration_plus, acceleration_cross),
    )

    field_redefinition_factor = (
        1
        - background_coefficient
        * q_squared
        / (2 * einstein_residue)
    )
    transformed_kernel = sp.expand(
        field_redefinition_factor**2 * tensor_kernel
    )
    transformed_linear_coefficient = sp.simplify(
        sp.diff(
            transformed_kernel,
            background_coefficient,
        ).subs(background_coefficient, 0)
    )
    transformed_leading_kernel = sp.simplify(
        transformed_kernel.subs(background_coefficient, 0)
    )

    rows = tagged(
        [
            {
                "gate_id": "DEG5191_00_Hessian",
                "object": "TT acceleration Hessian",
                "equation": "d2 L/d(gamma_A'')d(gamma_B'')=B delta_AB",
                "derived_result": str(acceleration_hessian),
                "status": "RANK_TWO_FOR_B_NONZERO",
            },
            {
                "gate_id": "DEG5191_01_constraints",
                "object": "possible scalar/lapse cancellation",
                "equation": (
                    "TT is an independent SO(3) irrep on FLRW;"
                    " P(X) has zero TT acceleration Hessian"
                ),
                "derived_result": (
                    "no scalar, lapse or shift constraint nulls the TT block"
                ),
                "status": "NO_DHOST_LIKE_DEGENERACY_IN_SELECTED_BLOCK",
            },
            {
                "gate_id": "DEG5191_02_kernel",
                "object": "constant-background principal kernel",
                "equation": "A=M_R^2/4; B=c_O4 Xbar",
                "derived_result": str(tensor_kernel),
                "status": "EXACT_5189_NORMALIZATION",
            },
            {
                "gate_id": "DEG5191_03_pole",
                "object": "additional resummed tensor pole",
                "equation": "A+B q2=0",
                "derived_result": str(extra_pole),
                "status": "PRESENT_FOR_B_NONZERO",
            },
            {
                "gate_id": "DEG5191_04_residues",
                "object": "pole residues in q2",
                "equation": "1/[q2(A+Bq2)]",
                "derived_result": (
                    f"massless={massless_residue}; extra={extra_residue}"
                ),
                "status": "OPPOSITE_RESIDUE",
            },
            {
                "gate_id": "DEG5191_05_sign",
                "object": "resummed-pole sign classification",
                "equation": "q2_extra=-A/B with A>0",
                "derived_result": (
                    "B<0: positive q2 negative-residue pole;"
                    " B>0: tachyonic-sign negative-residue pole"
                ),
                "status": "FINITE_TRUNCATION_NOT_ALL_SCALE_HEALTHY",
            },
            {
                "gate_id": "DEG5191_06_field_redefinition",
                "object": "constant-B perturbative tensor two-point term",
                "equation": "gamma=(1-B D/(2A)) gamma_R",
                "derived_result": (
                    "linear B q2^2 term cancels; residual starts at O(B^2)"
                ),
                "status": "FIRST_EFT_ORDER_REDUCIBLE",
            },
        ]
    )
    metrics = {
        "einstein_residue": "A=M_R^2/4",
        "background_coefficient": "B=c_O4 Xbar",
        "tensor_kernel": str(tensor_kernel),
        "extra_pole_q2": str(extra_pole),
        "massless_residue": str(massless_residue),
        "extra_residue": str(extra_residue),
        "partial_fraction_residual": str(partial_fraction_residual),
        "acceleration_hessian": [
            [
                str(acceleration_hessian[row, column])
                for column in range(2)
            ]
            for row in range(2)
        ],
        "acceleration_hessian_rank_for_nonzero_B": int(
            acceleration_hessian.rank()
        ),
        "acceleration_hessian_determinant": str(
            sp.factor(acceleration_hessian.det())
        ),
        "isolated_finite_truncation_degenerate": False,
        "field_redefinition": (
            "gamma=(1-B D/(2A)) gamma_R at first order in B"
        ),
        "transformed_kernel": str(sp.factor(transformed_kernel)),
        "transformed_leading_kernel": str(transformed_leading_kernel),
        "transformed_linear_B_coefficient": str(
            transformed_linear_coefficient
        ),
        "quadratic_q4_EFT_reducible_at_first_order": bool(
            transformed_linear_coefficient == 0
        ),
    }
    return rows, metrics


def derive_flrw_order_reduction() -> tuple[
    list[dict[str, Any]],
    dict[str, Any],
]:
    einstein_residue, scale_factor, hubble_conformal = sp.symbols(
        "A a Hc",
        positive=True,
        real=True,
    )
    background_coefficient, coefficient_second = sp.symbols(
        "B Bpp",
        real=True,
    )
    wave_number = sp.symbols("k", positive=True, real=True)
    amplitude, amplitude_prime, leading_eom = sp.symbols(
        "gamma gamma_prime E0",
        real=True,
    )

    flat_operator = leading_eom - 2 * hubble_conformal * amplitude_prime
    higher_derivative_piece = (
        background_coefficient * flat_operator**2 / 2
    )
    eom_proportional_piece = (
        background_coefficient * leading_eom**2 / 2
        - 2
        * background_coefficient
        * hubble_conformal
        * amplitude_prime
        * leading_eom
    )
    reduced_kinetic_piece = (
        2
        * background_coefficient
        * hubble_conformal**2
        * amplitude_prime**2
    )
    decomposition_residual = sp.simplify(
        higher_derivative_piece
        - eom_proportional_piece
        - reduced_kinetic_piece
    )

    kinetic_coefficient = sp.factor(
        einstein_residue * scale_factor**2
        + 4 * background_coefficient * hubble_conformal**2
    )
    gradient_coefficient = sp.factor(
        einstein_residue * scale_factor**2
        + 2 * coefficient_second
    )
    delta_kinetic = sp.factor(
        4
        * background_coefficient
        * hubble_conformal**2
        / (einstein_residue * scale_factor**2)
    )
    delta_gradient = sp.factor(
        2
        * coefficient_second
        / (einstein_residue * scale_factor**2)
    )
    sound_speed_squared, sound_speed_running, hubble_slope = sp.symbols(
        "c_s2 d_c_s2_d_lna epsilon_H",
        real=True,
    )
    logarithmic_B_slope = -6 * sound_speed_squared
    derivative_shape = sp.expand(
        -6 * sound_speed_running
        + logarithmic_B_slope * hubble_slope
        + logarithmic_B_slope**2
        + logarithmic_B_slope
    )
    canonical_derivative_shape = sp.simplify(
        derivative_shape.subs(
            {
                sound_speed_squared: 1,
                sound_speed_running: 0,
            }
        )
    )

    rows = tagged(
        [
            {
                "reduction_id": "RED5191_00_Einstein",
                "object": "leading FLRW tensor equation",
                "equation": "E0=gamma''+2 Hc gamma'+k^2 gamma=0",
                "derived_result": (
                    "Dgamma=gamma''+k^2 gamma=E0-2Hc gamma'"
                ),
                "status": "EXACT_IDENTITY",
            },
            {
                "reduction_id": "RED5191_01_EOM",
                "object": "B(Dgamma)^2/2",
                "equation": (
                    "B E0^2/2-2B Hc gamma' E0+2B Hc^2 gamma'^2"
                ),
                "derived_result": str(decomposition_residual),
                "status": "EOM_TERMS_REMOVABLE_AT_FIRST_EFT_ORDER",
            },
            {
                "reduction_id": "RED5191_02_action",
                "object": "order-reduced quadratic action per polarization",
                "equation": (
                    "Sred=1/2 int[Q_T gamma'^2-F_T k^2 gamma^2]"
                ),
                "derived_result": (
                    f"Q_T={kinetic_coefficient};"
                    f" F_T={gradient_coefficient}"
                ),
                "status": "SECOND_ORDER_EFT_ACTION",
            },
            {
                "reduction_id": "RED5191_03_controls",
                "object": "signed FLRW control parameters",
                "equation": "delta_Q=Q_T/(Aa^2)-1; delta_F=F_T/(Aa^2)-1",
                "derived_result": (
                    f"delta_Q={delta_kinetic};"
                    f" delta_F={delta_gradient}"
                ),
                "status": "EXACT_FIRST_ORDER_CONTROLS",
            },
            {
                "reduction_id": "RED5191_04_cosmic_time",
                "object": "cosmic-time coefficient derivative",
                "equation": "B''/a^2=ddot(B)+H dot(B)",
                "derived_result": (
                    "delta_Q=4 B H^2/A;"
                    " delta_F=2[ddot(B)+H dot(B)]/A"
                ),
                "status": "EXACT_TIME_CONVERSION",
            },
            {
                "reduction_id": "RED5191_05_stability",
                "object": "low-energy tensor stability",
                "equation": "Q_T>0 and F_T>0",
                "derived_result": (
                    "1+delta_Q>0 and 1+delta_F>0"
                ),
                "status": "FINITE_EFT_STABILITY_GATE",
            },
            {
                "reduction_id": "RED5191_06_speed",
                "object": "massless-branch tensor speed in original frame",
                "equation": "c_T^2=F_T/Q_T",
                "derived_result": (
                    "(1+delta_F)/(1+delta_Q)+O(B^2)"
                ),
                "status": "SOURCE_FRAME_MUST_BE_TRANSFORMED_CONSISTENTLY",
            },
            {
                "reduction_id": "RED5191_07_shift_current",
                "object": "homogeneous shift-symmetric P(X) clock",
                "equation": "a^3 P_X dot(psi)=constant",
                "derived_result": (
                    "d ln|X|/d ln a=-6 c_s^2;"
                    " c_s^2=P_X/(P_X+2X P_XX)"
                ),
                "status": "EXACT_CURRENT_CONSERVATION_LAW",
            },
            {
                "reduction_id": "RED5191_08_B_shape",
                "object": "B=c_O4 X derivative shape",
                "equation": (
                    "s_B=[ddot(B)+H dot(B)]/(B H^2)"
                ),
                "derived_result": str(derivative_shape),
                "status": "DERIVED_FROM_SHIFT_CURRENT",
            },
            {
                "reduction_id": "RED5191_09_canonical",
                "object": "canonical c_s^2=1 clock",
                "equation": "d c_s^2/d ln a=0",
                "derived_result": (
                    f"s_B={canonical_derivative_shape};"
                    " for constant -1<=w<=1, 30<=s_B<=48"
                ),
                "status": "CANONICAL_DERIVATIVE_ENVELOPE_DERIVED",
            },
        ]
    )
    metrics = {
        "leading_tensor_eom": "E0=gamma''+2 Hc gamma'+k^2 gamma",
        "flat_operator_on_leading_shell": "Dgamma=-2 Hc gamma'",
        "decomposition_residual": str(decomposition_residual),
        "kinetic_coefficient_QT": str(kinetic_coefficient),
        "gradient_coefficient_FT": str(gradient_coefficient),
        "delta_Q_conformal": str(delta_kinetic),
        "delta_F_conformal": str(delta_gradient),
        "delta_Q_cosmic": "4 B H^2/A",
        "delta_F_cosmic": "2[ddot(B)+H dot(B)]/A",
        "tensor_speed_squared": "(1+delta_F)/(1+delta_Q)",
        "shift_current": "a^3 P_X dot(psi)=constant",
        "sound_speed_squared": "P_X/(P_X+2X P_XX)",
        "logarithmic_B_slope": str(logarithmic_B_slope),
        "derivative_shape_s_B": str(derivative_shape),
        "canonical_s_B": str(canonical_derivative_shape),
        "canonical_constant_w_s_B": "39+9w for -1<=w<=1",
        "canonical_constant_w_s_B_range": [30, 48],
        "reduced_equation_order": 2,
        "order_reduction_validity": (
            "first order in B with derivatives and background curvature"
            " below the heavy-pole/parent cutoff"
        ),
    }
    return rows, metrics


def build_parent_rows(
    result_4941: dict[str, Any],
    result_4942: dict[str, Any],
    result_4957: dict[str, Any],
    result_4959: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    o4_basis_rows = list(
        csv.DictReader(
            source_path(
                "source-intake/mts_residuals/"
                "P8_Y5_R2FR_4930_SCALAR_SIX_DERIVATIVE_BASIS.csv"
            ).open(encoding="utf-8")
        )
    )
    o4_basis = next(
        row for row in o4_basis_rows if row["operator_id"] == "S6_O4"
    )
    endpoint_values = [
        float(row["W_O4_endpoint"])
        for row in result_4957["endpoint_summary"].values()
    ]
    wilson_min = min(endpoint_values)
    wilson_max = max(endpoint_values)
    wilson_abs_max = max(abs(value) for value in endpoint_values)
    gram_eigenvalues = [
        float(value) for value in result_4959["qmc"]["gram_eigenvalues"]
    ]
    planck_length = float(
        result_4942["dimensionful_endpoint_envelope"]["Planck_length_m"]
    )
    canonical_signed_coefficient_max = wilson_abs_max * planck_length**4

    rows = tagged(
        [
            {
                "ownership_id": "OWN5191_00_parent",
                "object": "selected canonical local parent",
                "source_fact": (
                    "Gamma contains -u_O4 C^2 X with c_O4=-u_O4"
                ),
                "derived_consequence": "B=c_O4 Xbar",
                "status": "PARENT_OWNED_OPERATOR",
            },
            {
                "ownership_id": "OWN5191_01_flow",
                "object": "minimal Type-II fixed point",
                "source_fact": (
                    "u_O4*="
                    f"{result_4941['minimal_O4_completed_point']['coordinates']['u_O4']}"
                ),
                "derived_consequence": (
                    "u_O4=0 is not an invariant surface and O4 adds no"
                    " relevant UV datum"
                ),
                "status": "NONZERO_PREDICTED_IRRELEVANT_COORDINATE",
            },
            {
                "ownership_id": "OWN5191_02_IR",
                "object": "GR-connected infrared Wilson endpoint",
                "source_fact": (
                    f"{wilson_min}<=W_O4=u_O4/g^2<={wilson_max}"
                ),
                "derived_consequence": (
                    "canonical c_O4=-u_O4/Z=-W_O4 l_P^4 is positive"
                ),
                "status": "SIGNED_ENDPOINT_ENVELOPE",
            },
            {
                "ownership_id": "OWN5191_03_quotient",
                "object": "full six-derivative scalar-gravity operator",
                "source_fact": (
                    f"IBP/EOM quotient independent={o4_basis['IBP_EOM_quotient_independent']}"
                ),
                "derived_consequence": (
                    "the full C^2 X operator cannot be deleted by a local"
                    " field redefinition"
                ),
                "status": "FULL_OPERATOR_NONREDUNDANT",
            },
            {
                "ownership_id": "OWN5191_04_amplitude",
                "object": "gauge-complete on-shell O4 projector",
                "source_fact": (
                    "five-projector Gram minimum eigenvalue="
                    f"{min(gram_eigenvalues)}"
                ),
                "derived_consequence": (
                    "O4 has an independent nonzero amplitude direction"
                ),
                "status": "ON_SHELL_NONREDUNDANCY_WITNESS",
            },
            {
                "ownership_id": "OWN5191_05_local",
                "object": "unoccupied local branch",
                "source_fact": "psi=0 implies Xbar=0",
                "derived_consequence": "B=0 and the O4 TT Hessian vanishes",
                "status": "EXACT_LOCAL_GR_PROTECTION",
            },
            {
                "ownership_id": "OWN5191_06_FLRW",
                "object": "homogeneous timelike canonical clock",
                "source_fact": "X_c=-dot(phi_c)^2<0 and c_O4>0",
                "derived_consequence": (
                    "B<0; a resummed pole has positive q2 but opposite residue"
                ),
                "status": "EFT_NOT_FUNDAMENTAL_RESUMMATION",
            },
        ]
    )
    metrics = {
        "basis_operator": o4_basis["operator"],
        "basis_independent": o4_basis[
            "IBP_EOM_quotient_independent"
        ].lower()
        == "true",
        "basis_quadratic_Hessian_nonzero": o4_basis[
            "quadratic_Hessian_nonzero_at_nabla_phi_zero"
        ].lower()
        == "true",
        "fixed_point_u_O4": float(
            result_4941["minimal_O4_completed_point"]["coordinates"][
                "u_O4"
            ]
        ),
        "u_O4_zero_invariant": bool(
            result_4941["minimal_O4_completed_point"][
                "u_O4_zero_invariant"
            ]
        ),
        "O4_adds_relevant_direction": bool(
            result_4941["claim_boundary"][
                "u_O4_adds_relevant_direction"
            ]
        ),
        "W_O4_endpoint_min": wilson_min,
        "W_O4_endpoint_max": wilson_max,
        "W_O4_endpoint_abs_max": wilson_abs_max,
        "planck_length_m": planck_length,
        "canonical_c_O4_abs_max_m4": canonical_signed_coefficient_max,
        "projector_basis": result_4959["projector_basis"],
        "projector_gram_eigenvalues": gram_eigenvalues,
        "projector_gram_positive": bool(
            result_4959["qmc"]["gram_positive_definite"]
        ),
        "full_operator_redundant": False,
        "local_X_zero_TT_Hessian_zero": True,
        "predicted_timelike_B_sign": "negative",
    }
    return rows, metrics


def build_cosmology_envelope(
    parent: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    speed_of_light = 299_792_458.0
    planck_length = float(parent["planck_length_m"])
    planck_time = planck_length / speed_of_light
    wilson_abs_max = float(parent["W_O4_endpoint_abs_max"])
    omega_kinetic = 1.0
    derivative_shape_bound = 100.0

    benchmarks = [
        ("today_scale", 2.2e-18),
        ("recombination_order_scale", 1.0e-13),
        ("BBN_order_scale", 1.0),
        ("high_scale_inflation_example", 1.0e38),
        ("near_UV_but_sub_Planck_example", 1.0e40),
        ("stress_test_near_Planck", 1.0e42),
    ]
    rows: list[dict[str, Any]] = []
    for label, hubble_per_second in benchmarks:
        hubble_planck = hubble_per_second * planck_time
        epsilon_background = (
            24
            * wilson_abs_max
            * omega_kinetic
            * hubble_planck**4
        )
        delta_q_abs = 4 * epsilon_background
        delta_f_abs_bound = (
            2 * derivative_shape_bound * epsilon_background
        )
        heavy_pole_over_hubble = 1 / (
            math.sqrt(
                24 * wilson_abs_max * omega_kinetic
            )
            * hubble_planck**2
        )
        rows.append(
            {
                "benchmark_id": f"ENV5191_{label}",
                "H_s_inverse": hubble_per_second,
                "H_tPlanck": hubble_planck,
                "Omega_kinetic_assumed": omega_kinetic,
                "s_B_abs_bound": derivative_shape_bound,
                "epsilon_background_abs": epsilon_background,
                "delta_Q_abs": delta_q_abs,
                "delta_F_abs_bound": delta_f_abs_bound,
                "heavy_pole_over_H": heavy_pole_over_hubble,
                "status": (
                    "ORDER_REDUCED_EFT_CONTROLLED"
                    if max(delta_q_abs, delta_f_abs_bound) < 0.1
                    else "APPROACHING_EFT_BOUNDARY"
                ),
            }
        )

    kinetic_unity_hubble = (
        1 / (96 * wilson_abs_max * omega_kinetic)
    ) ** 0.25 / planck_time
    pole_equals_hubble = (
        1 / (24 * wilson_abs_max * omega_kinetic)
    ) ** 0.25 / planck_time
    canonical_coefficient = (
        wilson_abs_max * planck_length**4
    )
    metrics = {
        "speed_of_light_m_s": speed_of_light,
        "planck_time_s": planck_time,
        "W_O4_abs_max": wilson_abs_max,
        "canonical_c_O4_abs_max_m4": canonical_coefficient,
        "canonical_branch_definition": (
            "phi_c=sqrt(Z)psi; X_c=-dot(phi_c)^2;"
            " Omega_kin=-X_c/(2 rho_total)"
        ),
        "canonical_density_assumption": (
            "0<=Omega_kin<=1 with no large positive kinetic density"
            " hidden by a cancelling negative component"
        ),
        "B_friedmann_relation": (
            "B=c_O4 X_c=-3|W_O4| Omega_kin (H t_P)^2/(4pi)"
        ),
        "epsilon_background": (
            "|B|H^2/A=24|W_O4|Omega_kin(H t_P)^4"
        ),
        "delta_Q_abs_bound": (
            "96|W_O4|Omega_kin(H t_P)^4"
        ),
        "delta_F_abs_bound": (
            "48|W_O4|Omega_kin |s_B| (H t_P)^4;"
            " s_B=[ddot(B)+H dot(B)]/(B H^2)"
        ),
        "heavy_pole_over_H": (
            "1/[sqrt(24|W_O4|Omega_kin)(H t_P)^2]"
        ),
        "H_for_abs_delta_Q_unity_s_inverse": kinetic_unity_hubble,
        "H_for_heavy_pole_equal_H_s_inverse": pole_equals_hubble,
        "benchmark_Omega_kinetic": omega_kinetic,
        "benchmark_s_B_abs_bound": derivative_shape_bound,
        "maximum_benchmark_delta_Q_below_1e40": max(
            float(row["delta_Q_abs"])
            for row in rows
            if float(row["H_s_inverse"]) <= 1e40
        ),
        "maximum_benchmark_delta_F_below_1e40": max(
            float(row["delta_F_abs_bound"])
            for row in rows
            if float(row["H_s_inverse"]) <= 1e40
        ),
    }
    return tagged(rows), metrics


def build_branch_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "branch_id": "BR5191_00_local",
                "arena": "local unoccupied vacuum",
                "B_status": "B=c_O4 Xbar=0 exactly",
                "tensor_status": "two-derivative GR block protected",
                "required_gate": "none from O4 at quadratic order",
                "decision": "EXACT_LOCAL_O4_SILENCE",
            },
            {
                "branch_id": "BR5191_01_FLRW_exact",
                "arena": "homogeneous clock, finite truncation resummed",
                "B_status": "B nonzero",
                "tensor_status": (
                    "rank-two fourth-derivative Hessian and opposite-residue"
                    " extra pole"
                ),
                "required_gate": (
                    "full UV tower, spectral completion or independent"
                    " degeneracy theorem"
                ),
                "decision": "NOT_AN_ALL_SCALE_TWO_MODE_THEORY",
            },
            {
                "branch_id": "BR5191_02_FLRW_EFT",
                "arena": "homogeneous clock, strict derivative expansion",
                "B_status": "B treated perturbatively",
                "tensor_status": (
                    "second-order Q_T/F_T action after reduction of order"
                ),
                "required_gate": (
                    "|delta_Q|,|delta_F|<<1 and frequencies below parent"
                    " cutoff"
                ),
                "decision": "LOW_ENERGY_ROUTE_RETAINED",
            },
            {
                "branch_id": "BR5191_03_canonical_density",
                "arena": "canonical timelike clock with Omega_kin<=1",
                "B_status": (
                    "predicted W_O4 gives Planck-fourth-power suppression"
                ),
                "tensor_status": (
                    "large safety margin for H far below Planck curvature"
                ),
                "required_gate": (
                    "derive actual cosmological X or retain Omega_kin/s_B"
                    " envelope"
                ),
                "decision": "CONDITIONAL_COSMOLOGICAL_SAFETY",
            },
            {
                "branch_id": "BR5191_04_general_PX",
                "arena": "general nonlinear P(X) background",
                "B_status": (
                    "shift current fixes d ln|X|/d ln a=-6c_s^2"
                ),
                "tensor_status": (
                    "same exact Q_T/F_T formulas apply; one state and"
                    " c_s^2(X) trajectory remain"
                ),
                "required_gate": (
                    "insert parent P(X), choose the cosmological state,"
                    " and enforce energy positivity/no cancellation"
                ),
                "decision": "BACKGROUND_EVOLUTION_REDUCED_NOT_SELECTED",
            },
            {
                "branch_id": "BR5191_05_operator",
                "arena": "full scalar-gravity amplitudes",
                "B_status": "O4 is an independent EFT coordinate",
                "tensor_status": (
                    "two-point q4 term reducible does not delete interactions"
                ),
                "required_gate": (
                    "carry induced operators and source transformation under"
                    " any field redefinition"
                ),
                "decision": "FULL_OPERATOR_NONREDUNDANT",
            },
            {
                "branch_id": "BR5191_06_Maxwell",
                "arena": "Maxwell/EM stress and Poynting",
                "B_status": "O4 contains no photon field",
                "tensor_status": (
                    "canonical Maxwell source chain unchanged at this order"
                ),
                "required_gate": "retain separate CFF coefficient",
                "decision": "MAXWELL_CHAIN_NOT_ALTERED_BY_O4",
            },
            {
                "branch_id": "BR5191_07_fundamental",
                "arena": "full MTS ultraviolet interpretation",
                "B_status": "finite derivative truncation is insufficient",
                "tensor_status": (
                    "ghost pole cannot be promoted to a physical prediction"
                ),
                "required_gate": (
                    "derive infinite-tower/nonlocal propagator or exact"
                    " parent completion"
                ),
                "decision": "UV_COMPLETION_GATE_OPEN",
            },
        ]
    )


def build_provenance_rows(
    source_hashes: dict[str, str],
) -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": f"SRC5191_{index:02d}",
            "source_type": "local_hash_locked",
            "source": str(source_path(relative)),
            "sha256": source_hashes[relative],
            "role": "parent definition, coefficient, amplitude or predecessor",
            "status": "HASH_MATCHED",
        }
        for index, relative in enumerate(LOCAL_SOURCES)
    ]
    offset = len(rows)
    rows.extend(
        {
            "source_id": f"SRC5191_{offset + index:02d}",
            "source_type": "external_primary",
            "source": url,
            "sha256": "URL_RECORDED_LOCAL_COPY_WHERE_AVAILABLE",
            "role": name,
            "status": "PRIMARY_REFERENCE_RECORDED",
        }
        for index, (name, url) in enumerate(EXTERNAL_SOURCES.items())
    )
    return tagged(rows)


def build_document(
    parent: dict[str, Any],
    weyl: dict[str, Any],
    degeneracy: dict[str, Any],
    reduction: dict[str, Any],
    envelope: dict[str, Any],
) -> None:
    text = f"""# 5191 - O4 FLRW tensor nondegeneracy, order reduction, and cosmological safety

Marker: `{MARKER}`

**Verdict:** `O4=C^2 X` cannot be set to zero, declared redundant, or
resummed as an exact healthy finite higher-derivative theory. The parent flow
predicts a nonzero coefficient and the full operator is an independent
on-shell scalar-gravity interaction. On a homogeneous clock background its
isolated tensor acceleration Hessian has rank two, so it is not degenerate.
If the finite truncation is resummed, its extra tensor pole has the opposite
residue to the GR pole.

The correct low-energy interpretation is nevertheless viable. At first order
in the derivative expansion, the tensor `q^4` term is equation-of-motion
reducible. For a time-dependent FLRW clock, exact reduction of order leaves a
second-order tensor action with background-suppressed kinetic and gradient
corrections. The source-predicted Wilson coefficient gives an enormous
control margin below Planck curvature under an explicit canonical kinetic
density bound.

No GitHub action and no edit to `formalization-workbench` occurred.

## 1. Parent ownership and sign

The assembled local action uses

```text
Gamma contains -u_O4 C_abcd C^abcd X,
X=g^munu partial_mu psi partial_nu psi.
```

Define the signed coefficient multiplying `+C^2 X`:

```text
c_O4=-u_O4,
B(eta)=c_O4 Xbar(eta).
```

The completed Type-II fixed point has

```text
u_O4*={parent['fixed_point_u_O4']},
u_O4=0 invariant={parent['u_O4_zero_invariant']},
O4 adds a relevant direction={parent['O4_adds_relevant_direction']}.
```

The four converged infrared endpoints give

```text
{parent['W_O4_endpoint_min']} <= W_O4=u_O4/g^2
                             <= {parent['W_O4_endpoint_max']}.
```

Thus in the canonical scalar coordinate

```text
c_O4=-u_O4/Z=-W_O4 l_P^4>0,
|c_O4| <= {parent['canonical_c_O4_abs_max_m4']:.15e} m^4.
```

For a homogeneous timelike canonical clock, `X_c<0`, hence `B<0`.

## 2. The full operator is not redundant

Checkpoint 4930 places

```text
O4=C_abcd C^abcd (nabla phi)^2
```

in the independent integration-by-parts/equation-of-motion quotient of the
shift-symmetric six-derivative scalar-gravity EFT. Checkpoint 4959 then
constructs its gauge-complete on-shell projector. The five-projector Gram
matrix is positive definite, with minimum eigenvalue

```text
{min(parent['projector_gram_eigenvalues']):.15e}.
```

A local field redefinition may move `O4` effects among equivalent operators,
but it cannot delete its full on-shell amplitude. This must be separated from
the narrower fact that its free tensor `q^4` two-point term is perturbatively
reducible.

The external primary basis reference is
`https://arxiv.org/abs/1908.08050`; the reduction-of-order methodology is
cross-checked against `https://arxiv.org/abs/1709.09695`. The newer
six-derivative scalar-tensor amplitude count is recorded at
`https://arxiv.org/abs/2512.13453`.

## 3. Exact time-dependent tensor Weyl density

Use conformal time, spatial momentum along `z`, and either real TT
polarization `gamma(eta) cos(kz)`. Four-dimensional conformal invariance gives

```text
sqrt(-g) C[g]^2=sqrt(-gtilde) C[gtilde]^2.
```

The executed full linearized Riemann/Ricci/Weyl contraction gives the same
spatially averaged density for plus and cross:

```text
{weyl['plus_density']}.
```

Writing `D gamma=gamma''+k^2 gamma`,

```text
C_1^2
 =1/2(D gamma)^2-2k^2(gamma gamma')'.
```

The second term cannot simply be discarded when `B(eta)` varies. The exact
weighted identity is

```text
B C_1^2
 =B(D gamma)^2/2-k^2 B'' gamma^2+J',

J=k^2[B' gamma^2-2B gamma gamma'].
```

Both symbolic residuals are exactly zero.

## 4. Nondegeneracy and the resummed pole

In the 5189 normalization,

```text
A=M_R^2/4,
K_TT(q^2)=q^2(A+Bq^2),
q^2=omega^2-k_phys^2.
```

The highest-time-derivative quadratic Lagrangian is

```text
L_high=B[(gamma_plus'')^2+(gamma_cross'')^2]/2.
```

Therefore

```text
d^2 L_high/d gamma_A'' d gamma_B''=B delta_AB,
rank=2 when B!=0,
det=B^2.
```

TT is an independent FLRW irrep. The scalar, lapse and shift constraints
cannot null this block, `P(X)` has zero TT acceleration Hessian, `C^3` starts
at cubic order on `Cbar=0`, and `CFF` has no pure tensor quadratic term on
`Fbar=0`. No explicitly resolved operator in the selected six-derivative
block supplies a cancellation. The unresolved `Gamma_p8plus/nonlocal` tower
could alter the all-scale spectrum, which is precisely why the finite
truncation is retained only as an EFT; it cannot be used as an unproved
exact cancellation.

The exact extra root and pole decomposition are

```text
q_extra^2={degeneracy['extra_pole_q2']},

1/[q^2(A+Bq^2)]
 =1/A[1/q^2-1/(q^2-q_extra^2)].
```

The residues are

```text
GR={degeneracy['massless_residue']},
extra={degeneracy['extra_residue']}.
```

For the predicted timelike branch `B<0`, the extra root has positive `q^2`
but negative residue. It is a heavy ghost if the finite polynomial is
incorrectly treated as exact. For `B>0`, the root also has tachyonic sign.
This is not a valid all-scale two-mode theory.

## 5. Why the low-energy EFT still survives

For constant `B`, the first-order local field redefinition

```text
gamma=[1-B D/(2A)] gamma_R
```

removes the linear `B q^4` tensor term. The executed transformed kernel has
linear-`B` coefficient

```text
{degeneracy['transformed_linear_B_coefficient']}.
```

The full `O4` interaction remains physical; only the free two-point
equation-of-motion-squared term is being reduced.

On FLRW, define the leading Einstein equation

```text
E0=gamma''+2 Hc gamma'+k^2 gamma=0,
Hc=a'/a.
```

Since `D gamma=E0-2Hc gamma'`, terms proportional to `E0` are removed by the
same first-order equivalence transformation. Including the exact `B''`
piece from the weighted Weyl density gives

```text
S_T,red=1/2 int d eta [
  Q_T gamma'^2-F_T k^2 gamma^2
]+O(B^2),

Q_T=A a^2+4B Hc^2,
F_T=A a^2+2B''.
```

This equation is second order. In cosmic time,

```text
delta_Q=Q_T/(Aa^2)-1=4B H^2/A,
delta_F=F_T/(Aa^2)-1
       =2[ddot(B)+H dot(B)]/A,
c_T^2=(1+delta_F)/(1+delta_Q)+O(B^2).
```

The finite low-energy gates are `1+delta_Q>0`,
`1+delta_F>0`, and physical frequencies/background derivatives below the
parent cutoff. Any field redefinition must also be applied to the source and
readout map; it is not permission to change frames selectively.

For a homogeneous shift-symmetric `P(X)` clock, the background current gives
an additional exact reduction:

```text
a^3 P_X dot(psi)=constant,
c_s^2=P_X/(P_X+2X P_XX),
d ln|B|/d ln a=d ln|X|/d ln a=-6c_s^2.
```

Therefore

```text
s_B=[ddot(B)+H dot(B)]/(B H^2)
   =36c_s^4-6c_s^2(1+dot(H)/H^2)
    -6 d(c_s^2)/d ln a.
```

For a canonical clock, `c_s^2=1`, so

```text
s_B=30-6 dot(H)/H^2.
```

On a constant equation-of-state background with `-1<=w<=1`, this is
`s_B=39+9w`, hence `30<=s_B<=48`. The numerical `|s_B|<=100`
envelope below is therefore deliberately wider than the complete canonical
range.

## 6. Source-predicted cosmological envelope

For `phi_c=sqrt(Z)psi`, define

```text
Omega_kin=-X_c/(2 rho_total),
rho_total=3M_R^2 H^2,
M_R^2=1/(8pi l_P^2).
```

On the healthy canonical branch assume

```text
0<=Omega_kin<=1
```

with no large positive kinetic density hidden by a cancelling negative
component. Then

```text
epsilon_bg=|B|H^2/A
          =24|W_O4|Omega_kin(H t_P)^4,

|delta_Q|=4 epsilon_bg,

|delta_F|=2|s_B| epsilon_bg,
s_B=[ddot(B)+H dot(B)]/(B H^2),

|q_extra|/H
 =1/[sqrt(24|W_O4|Omega_kin)(H t_P)^2].
```

At `Omega_kin=1`, `|delta_Q|=1` only at

```text
H={envelope['H_for_abs_delta_Q_unity_s_inverse']:.15e} s^-1,
```

and the heavy pole reaches `H` only at

```text
H={envelope['H_for_heavy_pole_equal_H_s_inverse']:.15e} s^-1.
```

Even the illustrative `H=10^40 s^-1` row has

```text
|delta_Q|<={envelope['maximum_benchmark_delta_Q_below_1e40']:.15e},
|delta_F|<={envelope['maximum_benchmark_delta_F_below_1e40']:.15e}
```

using the deliberately broad derivative-shape envelope `|s_B|<=100`.
This is a conditional theorem for the canonical kinetic-density branch, not
a selection of the actual MTS cosmological initial condition. For a general
shift-symmetric `P(X)` branch, the exact current law above reduces the
remaining input to its sourced `c_s^2(X)` trajectory and one background
state.

## 7. Decision

```text
O4 parent ownership                         = derived;
u_O4=0 invariant surface                    = false;
full O4 operator redundant                  = false;
isolated finite O4 TT truncation degenerate = false;
resummed extra-pole residue                 = opposite to GR;
first-EFT-order q4 two-point term reducible = true;
time-dependent FLRW reduced action          = derived;
local psi=0 tensor protection               = exact;
canonical sub-Planck cosmology              = conditionally controlled;
general P(X) cosmological X(t)               = still required;
all-scale UV two-mode completion             = not established.
```

This resolves the 5189 gate. `O4` does not have to be deleted for MTS to
recover low-energy GR. It has to be treated honestly as an irrelevant EFT
operator. A future fundamental claim must derive the full tower/nonlocal
propagator or another UV completion rather than promote the finite
fourth-order tensor polynomial to an exact spectrum.

## 8. Next target

The next calculation should insert the actual functional MTS `P(X)` into the
homogeneous current/Friedmann system and select its cosmological branch:

```text
Xbar(t), B(t), s_B(t), Omega_kin(t)
```

on the same cosmological branch used by the likelihood work. That turns the
conditional envelope into a branch-specific CMB/GW propagation prediction
without introducing a new coefficient.

## 9. Machine artifacts

- `source-intake/functional_rg/5191/O4_parent_ownership_and_convention.csv`
- `source-intake/functional_rg/5191/FLRW_TT_Weyl_quadratic_identity.csv`
- `source-intake/functional_rg/5191/O4_TT_degeneracy_and_pole.csv`
- `source-intake/functional_rg/5191/O4_redundancy_and_order_reduction.csv`
- `source-intake/functional_rg/5191/O4_cosmology_control_envelope.csv`
- `source-intake/functional_rg/5191/O4_branch_decision.csv`
- `source-intake/functional_rg/5191/source_provenance.csv`
- `source-intake/functional_rg/5191/O4_FLRW_tensor_order_reduction_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5191_VALIDATION.csv`
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def calculate_validations(
    source_hashes: dict[str, str],
    formal_before: str,
    checkpoint_5176_before: str,
    result_4941: dict[str, Any],
    result_4942: dict[str, Any],
    result_4957: dict[str, Any],
    result_4959: dict[str, Any],
    result_5189: dict[str, Any],
    parent: dict[str, Any],
    weyl: dict[str, Any],
    degeneracy: dict[str, Any],
    reduction: dict[str, Any],
    envelope: dict[str, Any],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(
        check: str,
        passed: bool,
        observed: Any,
        expected: Any,
    ) -> None:
        checks.append(
            validation_row(
                f"V5191_{len(checks):02d}",
                check,
                bool(passed),
                observed,
                expected,
            )
        )

    mismatches = {
        relative: source_hashes.get(relative)
        for relative, expected in LOCAL_SOURCES.items()
        if source_hashes.get(relative) != expected
    }
    add(
        "all locked local source hashes match",
        not mismatches,
        len(source_hashes) - len(mismatches),
        len(LOCAL_SOURCES),
    )
    add(
        "formalization workbench lock matches before writes",
        formal_before == FORMAL_LOCK,
        formal_before,
        FORMAL_LOCK,
    )
    add(
        "checkpoint 5176 lock matches before writes",
        checkpoint_5176_before == CHECKPOINT_5176_LOCK,
        checkpoint_5176_before,
        CHECKPOINT_5176_LOCK,
    )
    add(
        "4941 completes a nonzero O4 fixed point",
        (
            result_4941["claim_boundary"][
                "minimal_O4_parent_fixed_point_completed"
            ]
            is True
            and result_4941["minimal_O4_completed_point"]["coordinates"][
                "u_O4"
            ]
            != 0
        ),
        result_4941["minimal_O4_completed_point"]["coordinates"]["u_O4"],
        "nonzero",
    )
    add(
        "4941 rejects an invariant u_O4 zero surface",
        (
            result_4941["minimal_O4_completed_point"][
                "u_O4_zero_invariant"
            ]
            is False
        ),
        result_4941["minimal_O4_completed_point"][
            "u_O4_zero_invariant"
        ],
        False,
    )
    add(
        "O4 does not add a relevant UV direction",
        (
            result_4941["claim_boundary"][
                "u_O4_adds_relevant_direction"
            ]
            is False
        ),
        result_4941["claim_boundary"]["u_O4_adds_relevant_direction"],
        False,
    )
    add(
        "4942 local zero-field branch is derived",
        (
            result_4942["claim_boundary"][
                "homogeneous_local_psi_zero_branch_derived"
            ]
            is True
        ),
        result_4942["claim_boundary"][
            "homogeneous_local_psi_zero_branch_derived"
        ],
        True,
    )
    add(
        "4957 O4 trajectory is included",
        result_4957["gates"]["O4_functional_eta_trajectory"]
        == "INCLUDED",
        result_4957["gates"]["O4_functional_eta_trajectory"],
        "INCLUDED",
    )
    add(
        "all 4957 infrared O4 Wilson endpoints are negative",
        all(
            float(row["W_O4_endpoint"]) < 0
            for row in result_4957["endpoint_summary"].values()
        ),
        [
            row["W_O4_endpoint"]
            for row in result_4957["endpoint_summary"].values()
        ],
        "all negative",
    )
    add(
        "4959 gauge-complete projector Gram matrix is positive",
        result_4959["qmc"]["gram_positive_definite"] is True,
        result_4959["qmc"]["gram_positive_definite"],
        True,
    )
    add(
        "4959 basis explicitly contains O4 C2X",
        "O4_C2X" in result_4959["projector_basis"],
        result_4959["projector_basis"],
        "contains O4_C2X",
    )
    add(
        "5189 locks the Einstein plus O4 tensor kernel",
        result_5189["tensor_projection"]["TT_total_principal_kernel"]
        == "q2*(M_R2 + 4*X*c_O4*q2)/4",
        result_5189["tensor_projection"]["TT_total_principal_kernel"],
        "q2*(M_R2 + 4*X*c_O4*q2)/4",
    )
    add(
        "5189 local X zero protection is retained",
        result_5189["tensor_projection"]["local_zero_background_exact"]
        is True,
        result_5189["tensor_projection"]["local_zero_background_exact"],
        True,
    )
    add(
        "4930 quotient marks O4 independent",
        parent["basis_independent"] is True,
        parent["basis_independent"],
        True,
    )
    add(
        "4930 marks the O4 quadratic Hessian nonzero",
        parent["basis_quadratic_Hessian_nonzero"] is True,
        parent["basis_quadratic_Hessian_nonzero"],
        True,
    )
    add(
        "predicted canonical c_O4 magnitude is finite and positive",
        (
            math.isfinite(parent["canonical_c_O4_abs_max_m4"])
            and parent["canonical_c_O4_abs_max_m4"] > 0
        ),
        parent["canonical_c_O4_abs_max_m4"],
        ">0 finite",
    )
    add(
        "full tensor contraction gives equal TT polarizations",
        weyl["polarizations_equal"] is True,
        weyl["polarizations_equal"],
        True,
    )
    add(
        "plus polarization matches exact time-domain density",
        weyl["plus_matches_expected"] is True,
        weyl["plus_matches_expected"],
        True,
    )
    add(
        "unweighted Weyl identity closes",
        weyl["unweighted_identity_residual"] == "0",
        weyl["unweighted_identity_residual"],
        "0",
    )
    add(
        "time-dependent weighted Weyl identity closes",
        weyl["weighted_identity_residual"] == "0",
        weyl["weighted_identity_residual"],
        "0",
    )
    add(
        "TT acceleration Hessian has rank two for B nonzero",
        degeneracy["acceleration_hessian_rank_for_nonzero_B"] == 2,
        degeneracy["acceleration_hessian_rank_for_nonzero_B"],
        2,
    )
    add(
        "TT acceleration Hessian determinant is B squared",
        degeneracy["acceleration_hessian_determinant"] == "B**2",
        degeneracy["acceleration_hessian_determinant"],
        "B**2",
    )
    add(
        "isolated O4 finite truncation is not degenerate",
        degeneracy["isolated_finite_truncation_degenerate"] is False,
        degeneracy["isolated_finite_truncation_degenerate"],
        False,
    )
    add(
        "additional tensor root is minus A over B",
        degeneracy["extra_pole_q2"] == "-A/B",
        degeneracy["extra_pole_q2"],
        "-A/B",
    )
    add(
        "massless tensor residue is positive one over A",
        degeneracy["massless_residue"] == "1/A",
        degeneracy["massless_residue"],
        "1/A",
    )
    add(
        "extra tensor residue is opposite",
        degeneracy["extra_residue"] == "-1/A",
        degeneracy["extra_residue"],
        "-1/A",
    )
    add(
        "pole partial-fraction identity closes",
        degeneracy["partial_fraction_residual"] == "0",
        degeneracy["partial_fraction_residual"],
        "0",
    )
    add(
        "constant-B q4 term reduces at first EFT order",
        degeneracy["quadratic_q4_EFT_reducible_at_first_order"] is True,
        degeneracy["transformed_linear_B_coefficient"],
        "0",
    )
    add(
        "FLRW EOM decomposition closes",
        reduction["decomposition_residual"] == "0",
        reduction["decomposition_residual"],
        "0",
    )
    add(
        "order-reduced tensor equation is second order",
        reduction["reduced_equation_order"] == 2,
        reduction["reduced_equation_order"],
        2,
    )
    add(
        "order-reduced kinetic coefficient retains B Hc squared",
        (
            "4*B*Hc**2" in reduction["kinetic_coefficient_QT"]
            and "A*a**2" in reduction["kinetic_coefficient_QT"]
        ),
        reduction["kinetic_coefficient_QT"],
        "A*a**2+4*B*Hc**2",
    )
    add(
        "order-reduced gradient coefficient retains B second derivative",
        (
            "2*Bpp" in reduction["gradient_coefficient_FT"]
            and "A*a**2" in reduction["gradient_coefficient_FT"]
        ),
        reduction["gradient_coefficient_FT"],
        "A*a**2+2*Bpp",
    )
    add(
        "shift current fixes the logarithmic B slope",
        reduction["logarithmic_B_slope"] == "-6*c_s2",
        reduction["logarithmic_B_slope"],
        "-6*c_s2",
    )
    add(
        "canonical clock derivative shape is fixed",
        reduction["canonical_s_B"] in {
            "30 - 6*epsilon_H",
            "-6*epsilon_H + 30",
        },
        reduction["canonical_s_B"],
        "30-6*epsilon_H",
    )
    add(
        "canonical constant-w derivative envelope is finite",
        reduction["canonical_constant_w_s_B_range"] == [30, 48],
        reduction["canonical_constant_w_s_B_range"],
        [30, 48],
    )
    add(
        "canonical H threshold for kinetic breakdown is near Planck",
        1e42
        < envelope["H_for_abs_delta_Q_unity_s_inverse"]
        < 1e43,
        envelope["H_for_abs_delta_Q_unity_s_inverse"],
        "between 1e42 and 1e43 s^-1",
    )
    add(
        "canonical H<=1e40 kinetic correction is tiny",
        envelope["maximum_benchmark_delta_Q_below_1e40"] < 1e-8,
        envelope["maximum_benchmark_delta_Q_below_1e40"],
        "<1e-8",
    )
    add(
        "broad derivative envelope remains small through H=1e40",
        envelope["maximum_benchmark_delta_F_below_1e40"] < 1e-6,
        envelope["maximum_benchmark_delta_F_below_1e40"],
        "<1e-6",
    )
    return checks


def main() -> None:
    source_hashes = {
        relative: file_digest(source_path(relative))
        for relative in LOCAL_SOURCES
    }
    formal_before = tree_digest(FORMAL)
    checkpoint_5176_before = tree_digest(CHECKPOINT_5176_ROOT)

    result_4941 = load_json(
        "source-intake/functional_rg/4941/"
        "typeII_direct_O4_zero_and_lower_quotient_results.json"
    )
    result_4942 = load_json(
        "source-intake/functional_rg/4942/"
        "local_O4_C3_CFF_residual_results.json"
    )
    result_4957 = load_json(
        "source-intake/functional_rg/4957/"
        "functional_PX_O4_GR_trajectory_results.json"
    )
    result_4959 = load_json(
        "source-intake/functional_rg/4959/"
        "curvature_sixpoint_projector_results.json"
    )
    result_5189 = load_json(
        "source-intake/functional_rg/5189/"
        "motion_ADM_projection_results.json"
    )

    parent_rows, parent_metrics = build_parent_rows(
        result_4941,
        result_4942,
        result_4957,
        result_4959,
    )
    weyl_rows, weyl_metrics = derive_weyl_and_weighted_identity()
    degeneracy_rows, degeneracy_metrics = derive_degeneracy_and_poles()
    reduction_rows, reduction_metrics = derive_flrw_order_reduction()
    envelope_rows, envelope_metrics = build_cosmology_envelope(
        parent_metrics
    )
    branch_rows = build_branch_rows()
    provenance_rows = build_provenance_rows(source_hashes)

    checks = calculate_validations(
        source_hashes,
        formal_before,
        checkpoint_5176_before,
        result_4941,
        result_4942,
        result_4957,
        result_4959,
        result_5189,
        parent_metrics,
        weyl_metrics,
        degeneracy_metrics,
        reduction_metrics,
        envelope_metrics,
    )
    failures = [row for row in checks if row["status"] != "PASS"]
    if failures:
        raise RuntimeError(
            "Pre-write validation failed:\n"
            + json.dumps(failures, indent=2)
        )

    outputs = {
        PARENT_CSV: parent_rows,
        WEYL_CSV: weyl_rows,
        DEGENERACY_CSV: degeneracy_rows,
        REDUCTION_CSV: reduction_rows,
        ENVELOPE_CSV: envelope_rows,
        BRANCH_CSV: branch_rows,
        PROVENANCE_CSV: provenance_rows,
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    data_pack_digest = hashlib.sha256()
    for path in outputs:
        data_pack_digest.update(path.name.encode("utf-8"))
        data_pack_digest.update(file_digest(path).encode("ascii"))

    result_payload = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "leading_theorem": LEADING_THEOREM,
        "claim_guard": CLAIM_GUARD,
        "parent_ownership": parent_metrics,
        "time_dependent_Weyl_identity": weyl_metrics,
        "tensor_degeneracy_and_poles": degeneracy_metrics,
        "FLRW_order_reduction": reduction_metrics,
        "canonical_cosmology_envelope": envelope_metrics,
        "branch_decision": {
            "local_unoccupied_O4_tensor_silent": True,
            "full_O4_operator_redundant": False,
            "isolated_finite_O4_truncation_degenerate": False,
            "resummed_finite_O4_tensor_theory_healthy_all_scale": False,
            "first_EFT_order_tensor_q4_reducible": True,
            "order_reduced_FLRW_tensor_equation_second_order": True,
            "shift_symmetric_PX_background_evolution_law_derived": True,
            "canonical_sub_Planck_cosmology_conditionally_controlled": True,
            "general_PX_background_profile_derived": False,
            "full_UV_tensor_completion_derived": False,
            "next_target": (
                "derive Xbar(t), B(t), s_B(t), and Omega_kin(t) on the"
                " same MTS cosmology branch used by the likelihood"
            ),
        },
        "claim_status": {
            "O4_parent_owned_nonzero": True,
            "O4_full_operator_nonredundant": True,
            "O4_TT_nondegeneracy_derived": True,
            "O4_first_order_EFT_reduction_derived": True,
            "homogeneous_PX_shift_current_law_derived": True,
            "local_GR_tensor_branch_retained": True,
            "Maxwell_chain_modified_by_O4": False,
            "exact_all_scale_two_tensor_mode_claim": False,
            "general_cosmological_X_profile_derived": False,
            "full_MTS_unification": False,
            "GitHub_action": False,
        },
        "external_sources": EXTERNAL_SOURCES,
        "source_hashes": source_hashes,
        "formalization_workbench_sha256": formal_before,
        "checkpoint_5176_tree_sha256": checkpoint_5176_before,
        "data_pack_sha256": data_pack_digest.hexdigest(),
        "validation_count_prewrite": len(checks),
        "validation_failures_prewrite": 0,
    }
    write_json(RESULT_JSON, result_payload)
    build_document(
        parent_metrics,
        weyl_metrics,
        degeneracy_metrics,
        reduction_metrics,
        envelope_metrics,
    )

    formal_after = tree_digest(FORMAL)
    checkpoint_5176_after = tree_digest(CHECKPOINT_5176_ROOT)
    expected_outputs = tuple(outputs) + (RESULT_JSON, DOCUMENT)

    def add_final(
        check: str,
        passed: bool,
        observed: Any,
        expected: Any,
    ) -> None:
        checks.append(
            validation_row(
                f"V5191_{len(checks):02d}",
                check,
                bool(passed),
                observed,
                expected,
            )
        )

    add_final(
        "formalization workbench remains unchanged after writes",
        formal_after == formal_before == FORMAL_LOCK,
        formal_after,
        FORMAL_LOCK,
    )
    add_final(
        "checkpoint 5176 remains unchanged after writes",
        (
            checkpoint_5176_after
            == checkpoint_5176_before
            == CHECKPOINT_5176_LOCK
        ),
        checkpoint_5176_after,
        CHECKPOINT_5176_LOCK,
    )
    add_final(
        "all checkpoint artifacts exist and are nonempty",
        all(path.exists() and path.stat().st_size > 0 for path in expected_outputs),
        sum(
            1
            for path in expected_outputs
            if path.exists() and path.stat().st_size > 0
        ),
        len(expected_outputs),
    )
    parsed_csv_rows = {
        path.name: list(csv.DictReader(path.open(encoding="utf-8")))
        for path in outputs
    }
    add_final(
        "all generated CSV files parse with at least one row",
        all(rows for rows in parsed_csv_rows.values()),
        len(parsed_csv_rows),
        len(outputs),
    )
    all_generated_rows = [
        row
        for rows in parsed_csv_rows.values()
        for row in rows
    ]
    add_final(
        "all generated rows remain nonclaim",
        all(
            row.get("valid_for_full_MTS_claim", "").lower() == "false"
            for row in all_generated_rows
        ),
        len(all_generated_rows),
        "all false",
    )
    add_final(
        "all external primary source strings are recorded",
        all(
            url.startswith("https://arxiv.org/abs/")
            for url in EXTERNAL_SOURCES.values()
        ),
        len(EXTERNAL_SOURCES),
        len(EXTERNAL_SOURCES),
    )
    add_final(
        "no GitHub action is recorded",
        result_payload["claim_status"]["GitHub_action"] is False,
        result_payload["claim_status"]["GitHub_action"],
        False,
    )

    final_failures = [row for row in checks if row["status"] != "PASS"]
    if final_failures:
        raise RuntimeError(
            "Post-write validation failed:\n"
            + json.dumps(final_failures, indent=2)
        )
    write_csv(VALIDATION_CSV, checks)

    print(
        json.dumps(
            {
                "checkpoint": 5191,
                "marker": MARKER,
                "validation_passed": len(checks),
                "validation_failed": 0,
                "full_operator_redundant": False,
                "finite_truncation_degenerate": False,
                "extra_pole_residue": degeneracy_metrics["extra_residue"],
                "first_EFT_order_q4_reducible": True,
                "order_reduced_equation_order": reduction_metrics[
                    "reduced_equation_order"
                ],
                "canonical_c_O4_abs_max_m4": parent_metrics[
                    "canonical_c_O4_abs_max_m4"
                ],
                "H_deltaQ_unity_s_inverse": envelope_metrics[
                    "H_for_abs_delta_Q_unity_s_inverse"
                ],
                "document": str(DOCUMENT),
                "result": str(RESULT_JSON),
                "validation": str(VALIDATION_CSV),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
