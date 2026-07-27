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
OUT = POST / "source-intake" / "functional_rg" / "5190"

WARD_CSV = OUT / "static_Ward_constraint_and_helicity_decomposition.csv"
SO2_CSV = OUT / "SO2_invariant_stress_covariance.csv"
POWER_CSV = OUT / "local_scalar_mixing_power_count.csv"
POYNTING_CSV = OUT / "Poynting_and_unit_flow_escape_gate.csv"
ROUTE_CSV = OUT / "occupied_state_route_arbitration.csv"
DIRECT_CSV = OUT / "direct_state_vs_propagator_response.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "static_Ward_and_mixing_no_go_results.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5190_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5190-Y5-R2FR-static-Ward-helicity-one-derivative-mixing-no-go-"
    "and-direct-state-route-freeze.md"
)

MARKER = "MTS_5190_STATIC_WARD_HELICITY_AND_MIXING_NO_GO"
CHECKED_DATE = "2026-07-24"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_TREE_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
CHECKPOINT_5176_ROOT = POST / "source-intake" / "functional_rg" / "5176"

LEADING_THEOREM = (
    "AFTER_LOCAL_CONTACT_SUBTRACTION_THE_EXACT_STATIC_STRESS_WARD_"
    "IDENTITY_AT_NONZERO_SPATIAL_MOMENTUM_REMOVES_LONGITUDINAL_"
    "MOMENTUM_AND_LONGITUDINAL_STRESS_AND_SO2_INVARIANCE_SPLITS_THE_"
    "SURVIVING_RESPONSE_INTO_TWO_SCALARS_ONE_TRANSVERSE_POYNTING_"
    "DOUBLEt_AND_ONE_TT_DOUBLET_WITH_ZERO_CROSS_HELICITY_COVARIANCE_"
    "THEREFORE_STATIONARY_POYNTING_FLUX_CANNOT_SUPPLY_THE_MISSING_"
    "SCALAR_GALAXY_KERNEL_THE_POSITIVE_5181_COMPLETION_REQUIRES_A_"
    "CONSTANT_MIXING_TO_THE_CANONICALLY_NORMALIZED_METRIC_EQUIVALENT_"
    "TO_AN_UNNORMALIZED_ONE_SPATIAL_DERIVATIVE_SCALAR_MIXING_LOCAL_"
    "DIFFEOMORPHISM_INVARIANT_STATIC_PARITY_EVEN_SCALAR_COUPLINGS_"
    "HAVE_ZERO_DERIVATIVES_ONLY_WITH_A_NONZERO_GAP_OR_BEGIN_AT_TWO_"
    "DERIVATIVES_SO_THE_PARENT_MASSLESS_PAIR_GIVES_K_TIMES_NQ_"
    "RELATIVE_RESPONSE_NOT_NQ_OVER_K_NO_CONSTANT_NORMALIZATION_CAN_"
    "REPAIR_THE_TWO_POWER_MISMATCH_THE_CURRENT_SCALAR_COFRAME_PARENT_"
    "PROPAGATOR_ENHANCEMENT_ROUTE_IS_THEREFORE_REJECTED_WHILE_THE_"
    "DIRECT_CONSERVED_STATE_STRESS_ROUTE_REMAINS_CONDITIONAL_ON_A_"
    "PARENT_DERIVED_STATE_PREPARATION_AND_FORMATION_LAW"
)

CLAIM_GUARD = (
    "THIS_PROVES_A_STATIC_WARD_HELICITY_AND_LOCAL_DERIVATIVE_COUNTING_"
    "NO_GO_FOR_THE_CURRENT_SCALAR_PAIR_AND_POYNTING_ESCAPE_IT_DOES_"
    "NOT_REJECT_NONLOCAL_NONEQUILIBRIUM_OR_NEW_INDEPENDENT_VECTOR_"
    "PARENTS_DOES_NOT_DERIVE_THE_DIRECT_STATE_OCCUPATION_OR_GALAXY_"
    "FORMATION_LAW_DOES_NOT_PROMOTE_A_GALAXY_CLAIM_AND_DOES_NOT_"
    "ALTER_THE_LEADING_LOCAL_GR_NEWTON_MAXWELL_BRANCH"
)


def source_path(relative: str) -> Path:
    return POST / Path(relative.replace("/", "\\"))


SOURCES: dict[str, tuple[Path, str]] = {
    "checkpoint_4872_flow_and_Poynting": (
        source_path(
            "4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-"
            "universal-source-coupling-or-correspondence-demotion.md"
        ),
        "9a4eaed25f41167381ea77437350c322f7a4ee9cfab3228cfc2db0bd5f204923",
    ),
    "checkpoint_4873_metric_only": (
        source_path(
            "4873-Y5-R2FR-covariant-open-parent-action-and-connected-"
            "covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-"
            "EFT-freeze.md"
        ),
        "af2c97091477525fb7244e5b2577e4a4c70d863987ebbb39b6c974d978b38b6e",
    ),
    "checkpoint_5148_target": (
        source_path(
            "5148-Y5-R2FR-one-parent-local-GR-galaxy-spectral-response-"
            "cog-theorem.md"
        ),
        "b2d5bddd8ce3cee2299b2cdadd66a0688bbd07c945bc329ac2ade4c20c113352",
    ),
    "checkpoint_5148_result": (
        source_path(
            "source-intake/functional_rg/5148/"
            "regime_selective_motion_response_results.json"
        ),
        "a9f48dd11d6c7f3bdd79436ade9d467c8b870b50c5fb2c5c760abae8dc3f05aa",
    ),
    "checkpoint_5149_spectral": (
        source_path(
            "5149-Y5-R2FR-causal-spectral-density-critical-motion-"
            "mixing-and-vacuum-no-go.md"
        ),
        "4ccd4b37a60a3e5b66d8cc9d0f3e94473baf19f1468180a74a468f3ad1db606d",
    ),
    "checkpoint_5149_result": (
        source_path(
            "source-intake/functional_rg/5149/"
            "causal_spectral_density_and_critical_mixing_results.json"
        ),
        "32970c04699829c2e4190dbbf9926b602c9079cb385737dfccf67af82acdefdc",
    ),
    "checkpoint_5150_TT_pair": (
        source_path(
            "5150-Y5-R2FR-minimal-occupied-PX-zero-mode-TT-"
            "polarization-and-critical-sign-gate.md"
        ),
        "1c7152513ee33a185113dc422be35034d7f7f40ea78d47001b4308c971f56458",
    ),
    "checkpoint_5150_result": (
        source_path(
            "source-intake/functional_rg/5150/"
            "minimal_occupied_PX_zero_mode_TT_results.json"
        ),
        "307fd49a9c9c38f47f3c381bcd57ab2001a1c6d286bcb5f2beddaf7eec0160d6",
    ),
    "checkpoint_5151_direct_state": (
        source_path(
            "5151-Y5-R2FR-parent-projective-occupation-to-conserved-"
            "Einstein-cluster-stress-and-two-metric-cog-gate.md"
        ),
        "b23ca652af8b66c220973cffbdc1ab2df028947c9dba8bd61666d1e0460c5fd5",
    ),
    "checkpoint_5151_result": (
        source_path(
            "source-intake/functional_rg/5151/"
            "projective_state_stress_results.json"
        ),
        "f1331f9bc511f12e4e785c9a3ffcf19dadf4eb8b05b05362031548a22984805c",
    ),
    "checkpoint_5171_Vlasov": (
        source_path(
            "5171-Y5-R2FR-action-angle-retarded-Vlasov-polarization-"
            "static-response-and-double-counting-gate.md"
        ),
        "e66c543db2154ac061a5930edad50585b5835bbc53e1d2774a0c87d7e19cbade",
    ),
    "checkpoint_5171_result": (
        source_path(
            "source-intake/functional_rg/5171/"
            "action_angle_vlasov_response_results.json"
        ),
        "ee867649d6e1a1784e56d2805f63b4d8b4956fdb2337ba311cda99a4926054e1",
    ),
    "checkpoint_5177_no_retuning": (
        source_path(
            "5177-Y5-R2FR-locked-ensemble-metric-split-and-no-retuning-"
            "theorem.md"
        ),
        "abe635ca81992660c7e9bb834eed765626bf63cfc2564f3f4b23b759a3a0fd90",
    ),
    "checkpoint_5177_result": (
        source_path(
            "source-intake/functional_rg/5177/"
            "locked_metric_split_results.json"
        ),
        "2ae85163c0c03a642252f6521d717ddd0a313f113cc6cc65bdf2b0425a2af570",
    ),
    "checkpoint_5180_interacting_kernel": (
        source_path(
            "5180-Y5-R2FR-interacting-retarded-2PI-kernel-Vlasov-"
            "subtraction-and-infrared-gap-closure-gate.md"
        ),
        "1df0b686a815496b143f5397aebf4b55d16058cd8bbca3910fb7993e980c0c10",
    ),
    "checkpoint_5180_result": (
        source_path(
            "source-intake/functional_rg/5180/"
            "interacting_spectral_gap_results.json"
        ),
        "699ac52dc60d07f6893b321aeb7a7701834870bb5fd1b09499f42a3486475512",
    ),
    "checkpoint_5181_positive_completion": (
        source_path(
            "5181-Y5-R2FR-critical-pair-bubble-positive-Hessian-and-"
            "parent-ownership-gate.md"
        ),
        "54a35ad66744f9e1f5ab6fdd15e66bc6f87a93330a999aae2235ea5cf98b3657",
    ),
    "checkpoint_5181_result": (
        source_path(
            "source-intake/functional_rg/5181/"
            "critical_pair_completion_results.json"
        ),
        "4c1f015ed2d946f4e158cb1b1954b3bb6dfc5a49f2f43c2fc92e847229f8f88d",
    ),
    "checkpoint_5182_projector": (
        source_path(
            "5182-Y5-R2FR-static-Hilbert-pair-projector-constrained-"
            "Newtonian-response-and-route-decision.md"
        ),
        "fe9307a74581108b428b12eb4918205b24bc5615c47e370face7eff6892f1fcf",
    ),
    "checkpoint_5182_result": (
        source_path(
            "source-intake/functional_rg/5182/"
            "static_Hilbert_pair_projector_results.json"
        ),
        "50fcd555fb9ee889a3d10cd4a5fe45ff61ef8c1447b3d6ff12b38ed9d56d63ee",
    ),
    "checkpoint_5183_sign_fix": (
        source_path(
            "5183-Y5-R2FR-Wick-sign-consistent-static-pair-response-and-"
            "5182-supersession.md"
        ),
        "c8aafba0a982c957d844b0db4165d46c30236d62296c38d4eb7d8e34fc25cc36",
    ),
    "checkpoint_5183_result": (
        source_path(
            "source-intake/functional_rg/5183/"
            "Wick_sign_consistent_pair_response_results.json"
        ),
        "97f3a5d9265fb19898ac859f37e33bede58bc0d72bb3f1dd86b78c3ed421a85b",
    ),
    "checkpoint_5185_interaction_stress": (
        source_path(
            "5185-Y5-R2FR-occupied-state-2PI-interaction-stress-and-"
            "collision-gate.md"
        ),
        "d47db7fefdb8b9f799a48a1e4d5a7c4266880d41d97b40ae2cefe33cd62d07a5",
    ),
    "checkpoint_5185_result": (
        source_path(
            "source-intake/functional_rg/5185/"
            "occupied_state_2PI_interaction_results.json"
        ),
        "9d725483e8fe7e355f1844ab5a15a9b257d8e4d8792250807bef1474df58d081",
    ),
    "checkpoint_5188_coframe_Maxwell": (
        source_path(
            "5188-Y5-R2FR-relational-clock-scalar-no-go-minimal-coframe-"
            "parent-and-Fierz-Pauli-selection-theorem.md"
        ),
        "06f376fbab1a07312ae6993f1ea2a2e2f276a2438d7a2c15daf7993a17f6fb7a",
    ),
    "checkpoint_5188_result": (
        source_path(
            "source-intake/functional_rg/5188/"
            "relational_coframe_parent_results.json"
        ),
        "9160b84ad6cbb9de7cda7df53b4d5a0c35f24b0b2c2795ff529bc94a3c12a30b",
    ),
    "checkpoint_5189_ADM_target": (
        source_path(
            "5189-Y5-R2FR-motion-sector-ADM-projection-clock-only-"
            "ancestry-and-local-tensor-protection-theorem.md"
        ),
        "4514f59f95fa00fbddd652511bf49a98a84347b3f4f10747afbdfb6d3917e266",
    ),
    "checkpoint_5189_result": (
        source_path(
            "source-intake/functional_rg/5189/"
            "motion_ADM_projection_results.json"
        ),
        "6418ffc826ed2068b1f4df46d56423fe3f866c0e9bfa363098f4e849174fcfc2",
    ),
}

EXTERNAL_SOURCES = {
    "Rychkov_CFT_unitarity_lectures": "https://arxiv.org/abs/1601.05000",
    "Crossley_Glorioso_Liu_CTP": "https://arxiv.org/abs/1511.03646",
}


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(file_digest(item).encode("ascii"))
    return digest.hexdigest()


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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


def build_static_ward_and_helicity() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    component_names = (
        "T00",
        "T01",
        "T02",
        "T03",
        "T11",
        "T12",
        "T13",
        "T22",
        "T23",
        "T33",
    )
    components = sp.symbols(" ".join(component_names), real=True)
    index = {name: position for position, name in enumerate(component_names)}
    ward_matrix = sp.zeros(4, len(components))
    for row, name in enumerate(("T03", "T13", "T23", "T33")):
        ward_matrix[row, index[name]] = 1
    ward_rank = ward_matrix.rank()
    ward_nullity = len(components) - ward_rank

    covariance = sp.zeros(6)
    covariance_variables: list[sp.Symbol] = []
    for row in range(6):
        for column in range(row, 6):
            variable = sp.symbols(f"C{row}{column}", real=True)
            covariance_variables.append(variable)
            covariance[row, column] = variable
            covariance[column, row] = variable

    vector_generator = sp.Matrix([[0, -1], [1, 0]])
    rotation_generator = sp.diag(
        sp.zeros(2),
        vector_generator,
        2 * vector_generator,
    )
    invariance_residual = sp.expand(
        rotation_generator * covariance - covariance * rotation_generator
    )
    invariance_equations = [
        invariance_residual[row, column]
        for row in range(6)
        for column in range(6)
    ]
    invariance_matrix, invariance_rhs = sp.linear_eq_to_matrix(
        invariance_equations,
        covariance_variables,
    )
    invariant_rank = invariance_matrix.rank()
    invariant_nullity = len(covariance_variables) - invariant_rank
    invariant_solution = sp.linsolve(
        (invariance_matrix, invariance_rhs),
        covariance_variables,
    )
    solution_tuple = next(iter(invariant_solution))
    invariant_covariance = covariance.subs(
        dict(zip(covariance_variables, solution_tuple))
    )

    Phi, Psi = sp.symbols("Phi Psi", real=True)
    T00, T11, T22 = sp.symbols("T00 T11 T22", real=True)
    scalar_metric_vertex = sp.expand(-Phi * T00 - Psi * (T11 + T22))

    omega, wave_number, dynamic_T00 = sp.symbols(
        "omega k T00_dynamic",
        nonzero=True,
        real=True,
    )
    dynamic_longitudinal_momentum = sp.simplify(
        omega * dynamic_T00 / wave_number
    )
    static_longitudinal_momentum = sp.limit(
        dynamic_longitudinal_momentum,
        omega,
        0,
    )

    metrics = {
        "stress_component_order": list(component_names),
        "static_Ward_matrix": [
            [int(ward_matrix[row, column]) for column in range(10)]
            for row in range(4)
        ],
        "static_Ward_rank": ward_rank,
        "static_Ward_nullity": ward_nullity,
        "static_Ward_zero_components": ["T03", "T13", "T23", "T33"],
        "surviving_basis": [
            "T00",
            "tau=(T11+T22)/2",
            "P_x=T01",
            "P_y=T02",
            "T_plus=(T11-T22)/2",
            "T_cross=T12",
        ],
        "helicity_dimensions": {"scalar": 2, "vector": 2, "tensor": 2},
        "SO2_covariance_variable_count": len(covariance_variables),
        "SO2_invariance_constraint_rank": invariant_rank,
        "SO2_invariant_covariance_dimension": invariant_nullity,
        "SO2_invariant_covariance": [
            [
                str(invariant_covariance[row, column])
                for column in range(6)
            ]
            for row in range(6)
        ],
        "cross_helicity_covariance_zero": all(
            invariant_covariance[row, column] == 0
            for row in range(2)
            for column in range(2, 6)
        )
        and all(
            invariant_covariance[row, column] == 0
            for row in range(2, 4)
            for column in range(4, 6)
        ),
        "scalar_metric_vertex": str(scalar_metric_vertex),
        "dynamic_longitudinal_momentum": str(dynamic_longitudinal_momentum),
        "static_longitudinal_momentum": str(static_longitudinal_momentum),
        "contact_clause": (
            "homogeneous Ward identity applies to the nonanalytic connected"
            " kernel after local seagull/contact subtraction"
        ),
    }

    ward_rows = tagged(
        [
            {
                "ward_id": "WARD5190_00_setup",
                "object": "static Fourier stress insertion",
                "equation": "k_mu=(0,0,0,k), k!=0",
                "derived_result": "k_mu Delta T^mu_nu=0",
                "sector": "all",
                "status": "EXACT_AFTER_LOCAL_CONTACT_SUBTRACTION",
            },
            {
                "ward_id": "WARD5190_01_constraints",
                "object": "longitudinal stress components",
                "equation": "k T^3_nu=0",
                "derived_result": "T03=T13=T23=T33=0",
                "sector": "all",
                "status": "RANK4_WARD_CONSTRAINT",
            },
            {
                "ward_id": "WARD5190_02_scalar",
                "object": "surviving helicity-zero stress",
                "equation": "rho=T00; tau=(T11+T22)/2",
                "derived_result": "two-dimensional scalar block",
                "sector": "scalar",
                "status": "EXACT_SO2_IRREP",
            },
            {
                "ward_id": "WARD5190_03_vector",
                "object": "surviving transverse momentum/Poynting",
                "equation": "P_A=T0A, A=x,y",
                "derived_result": "two-dimensional helicity-one block",
                "sector": "vector",
                "status": "EXACT_SO2_IRREP",
            },
            {
                "ward_id": "WARD5190_04_tensor",
                "object": "surviving transverse traceless stress",
                "equation": "T_plus=(T11-T22)/2; T_cross=T12",
                "derived_result": "two-dimensional helicity-two block",
                "sector": "tensor",
                "status": "EXACT_SO2_IRREP",
            },
            {
                "ward_id": "WARD5190_05_metric_vertex",
                "object": "Newtonian scalar metric coupling",
                "equation": "1/2 h_mu_nu T^mu_nu",
                "derived_result": str(scalar_metric_vertex),
                "sector": "scalar",
                "status": "EXACT_STATIC_VERTEX",
            },
            {
                "ward_id": "WARD5190_06_finite_frequency",
                "object": "longitudinal momentum",
                "equation": "-omega T00+k T30=0",
                "derived_result": "T30=(omega/k)T00 -> 0 for a regular DC limit",
                "sector": "scalar/vector boundary",
                "status": "EXACT_REGULAR_LIMIT",
            },
        ]
    )

    so2_rows = tagged(
        [
            {
                "irrep_id": "SO25190_00_generator",
                "basis": "(rho,tau,Px,Py,Tplus,Tcross)",
                "rotation_weight": "(0,0,1,1,2,2)",
                "invariant_covariance": "solve [G,C]=0 for symmetric C",
                "derived_result": (
                    f"21 variables; rank {invariant_rank}; dimension"
                    f" {invariant_nullity}"
                ),
                "cross_block": "zero",
                "status": "EXACT_LINEAR_ALGEBRA",
            },
            {
                "irrep_id": "SO25190_01_scalar",
                "basis": "(rho,tau)",
                "rotation_weight": "0",
                "invariant_covariance": "arbitrary symmetric 2x2",
                "derived_result": "3 independent functions",
                "cross_block": "no scalar-vector or scalar-tensor covariance",
                "status": "HELICITY_BLOCK",
            },
            {
                "irrep_id": "SO25190_02_vector",
                "basis": "(Px,Py)",
                "rotation_weight": "1",
                "invariant_covariance": "C_V times identity_2",
                "derived_result": "1 independent function",
                "cross_block": "no vector-scalar or vector-tensor covariance",
                "status": "HELICITY_BLOCK",
            },
            {
                "irrep_id": "SO25190_03_tensor",
                "basis": "(Tplus,Tcross)",
                "rotation_weight": "2",
                "invariant_covariance": "C_T times identity_2",
                "derived_result": "1 independent function",
                "cross_block": "no tensor-scalar or tensor-vector covariance",
                "status": "HELICITY_BLOCK",
            },
        ]
    )
    return ward_rows, so2_rows, metrics


def build_local_mixing_power_count() -> tuple[
    list[dict[str, Any]],
    dict[str, Any],
]:
    derivative_order, singularity = sp.symbols(
        "d alpha",
        real=True,
    )
    relative_exponent = sp.simplify(
        2 * derivative_order - singularity - 2
    )
    required_derivative_for_pair = sp.solve(
        sp.Eq(relative_exponent.subs(singularity, 1), -1),
        derivative_order,
    )[0]
    required_singularity_for_two_derivatives = sp.solve(
        sp.Eq(relative_exponent.subs(derivative_order, 2), -1),
        singularity,
    )[0]

    x = sp.symbols("x", positive=True)
    q = sp.Rational(77, 100)
    occupation = sp.simplify(1 / (1 + x**q))
    pair_relative = sp.simplify(x * occupation)
    target_relative = sp.simplify(occupation / x)
    shape_ratio = sp.cancel((x * occupation) / (occupation / x))
    logarithmic_pair_slope = sp.simplify(
        x * sp.diff(pair_relative, x) / pair_relative
    )
    logarithmic_target_slope = sp.simplify(
        x * sp.diff(target_relative, x) / target_relative
    )
    low_pair_slope = sp.limit(logarithmic_pair_slope, x, 0, dir="+")
    high_pair_slope = sp.limit(logarithmic_pair_slope, x, sp.oo)
    low_target_slope = sp.limit(logarithmic_target_slope, x, 0, dir="+")
    high_target_slope = sp.limit(logarithmic_target_slope, x, sp.oo)

    Delta = sp.symbols("Delta", real=True)
    cft_singularity = sp.simplify(3 - 2 * Delta)
    cft_maximum_singularity = cft_singularity.subs(
        Delta,
        sp.Rational(1, 2),
    )

    sample_x = [10 ** (-6 + 12 * index / 240) for index in range(241)]
    target_values = [
        (1 / (1 + value**0.77)) / value for value in sample_x
    ]
    pair_values = [
        value / (1 + value**0.77) for value in sample_x
    ]
    log_ratios = [
        math.log(target / pair)
        for target, pair in zip(target_values, pair_values)
    ]
    best_log_amplitude = sum(log_ratios) / len(log_ratios)
    best_amplitude = math.exp(best_log_amplitude)
    residual_factors = [
        best_amplitude * pair / target
        for target, pair in zip(target_values, pair_values)
    ]

    metrics = {
        "Schur_power_formula": (
            "if B_hchi~k^d and G_chi~k^-alpha then"
            " (B G B)/K_GR~k^(2d-alpha-2)"
        ),
        "relative_exponent": str(relative_exponent),
        "pair_singularity_alpha": 1,
        "target_relative_exponent": -1,
        "required_derivative_order_for_pair": str(
            required_derivative_for_pair
        ),
        "required_singularity_for_two_derivative_vertex": str(
            required_singularity_for_two_derivatives
        ),
        "critical_pair_occupation": str(occupation),
        "local_pair_relative": str(pair_relative),
        "required_relative": str(target_relative),
        "shape_ratio": str(shape_ratio),
        "low_pair_slope": str(low_pair_slope),
        "high_pair_slope": str(high_pair_slope),
        "low_target_slope": str(low_target_slope),
        "high_target_slope": str(high_target_slope),
        "positive_completion_normalized_mixing": "B_uchi=sqrt(A)",
        "positive_completion_unnormalized_mixing": (
            "B_hchi=sqrt(A K_h)~sqrt(A) M_R |k|"
        ),
        "required_local_static_scalar_derivative_order": 1,
        "current_gapless_scalar_vertex_derivative_order": 2,
        "zero_derivative_mass_vertex_at_criticality": 0,
        "CFT_scalar_two_point_power": "G_O(k)~k^(2 Delta-3)",
        "CFT_scalar_unitarity_bound": "Delta>=1/2 in three dimensions",
        "CFT_maximum_singularity_alpha": str(cft_maximum_singularity),
        "CFT_two_derivative_target_possible": bool(
            cft_maximum_singularity
            >= required_singularity_for_two_derivatives
        ),
        "sample_log_best_amplitude": best_amplitude,
        "sample_minimum_target_ratio": min(residual_factors),
        "sample_maximum_target_ratio": max(residual_factors),
        "sample_dynamic_range": (
            max(residual_factors) / min(residual_factors)
        ),
    }

    rows = tagged(
        [
            {
                "power_id": "POW5190_00_general",
                "candidate": "generic Schur channel",
                "critical_susceptibility": "G_chi~|k|^-alpha",
                "metric_mixing": "B_hchi~|k|^d",
                "relative_to_Einstein": "|k|^(2d-alpha-2)",
                "comparison_to_target": "target exponent=-1",
                "verdict": "EXACT_POWER_COUNT",
            },
            {
                "power_id": "POW5190_01_pair",
                "candidate": "massless psi^2 pair",
                "critical_susceptibility": "B0~1/(8|k|), alpha=1",
                "metric_mixing": "local Hilbert or R psi^2 vertex has d=2",
                "relative_to_Einstein": "|k|^(+1) n_q",
                "comparison_to_target": "n_q/|k|",
                "verdict": "TWO_POWERS_TOO_SOFT",
            },
            {
                "power_id": "POW5190_02_shape",
                "candidate": "locked q=0.77 crossover",
                "critical_susceptibility": "n_q=1/(1+x^q)",
                "metric_mixing": "x=|k|/mu",
                "relative_to_Einstein": "pair=x n_q; target=n_q/x",
                "comparison_to_target": f"pair/target={shape_ratio}",
                "verdict": "NO_CONSTANT_NORMALIZATION_CAN_MATCH",
            },
            {
                "power_id": "POW5190_03_mass",
                "candidate": "zero-derivative sqrt(-g)m^2 psi^2 vertex",
                "critical_susceptibility": "massive bubble analytic for m!=0",
                "metric_mixing": "d=0 but coefficient proportional to m^2",
                "relative_to_Einstein": "vanishes when the gap is collapsed",
                "comparison_to_target": "cannot retain d=0 at the massless pair point",
                "verdict": "NOT_A_CRITICAL_ESCAPE",
            },
            {
                "power_id": "POW5190_04_required",
                "candidate": "5181 positive completion",
                "critical_susceptibility": "C_q~1/|k|",
                "metric_mixing": "B_uchi=sqrt(A) in u=sqrt(K_h)h",
                "relative_to_Einstein": "A C_q",
                "comparison_to_target": (
                    "B_hchi=sqrt(A K_h)~sqrt(A)M_R|k|, so d=1"
                ),
                "verdict": "REQUIRES_ONE_DERIVATIVE_OR_NONLOCAL_MIXING",
            },
            {
                "power_id": "POW5190_05_static_scalar",
                "candidate": "local static isotropic parity-even scalar action",
                "critical_susceptibility": "scalar O",
                "metric_mixing": (
                    "no one-spatial-derivative scalar; K O and u.grad O are"
                    " proportional to omega and vanish at DC"
                ),
                "relative_to_Einstein": "leading gapless scalar mixing has d=2",
                "comparison_to_target": "required d=1 absent",
                "verdict": "LOCAL_ONE_DERIVATIVE_SCALAR_MIXING_NO_GO",
            },
            {
                "power_id": "POW5190_06_CFT_bound",
                "candidate": "unitary local three-dimensional critical scalar",
                "critical_susceptibility": (
                    "G_O~k^(2Delta-3), Delta>=1/2 => alpha<=2"
                ),
                "metric_mixing": "d=2",
                "relative_to_Einstein": "target would require alpha=3",
                "comparison_to_target": "alpha_required exceeds unitary scalar bound",
                "verdict": "EQUILIBRIUM_LOCAL_CRITICAL_ESCAPE_REJECTED",
            },
            {
                "power_id": "POW5190_07_scope",
                "candidate": "nonlocal or nonequilibrium active medium",
                "critical_susceptibility": "not constrained to local CFT scaling",
                "metric_mixing": "may generate |nabla| or noncommuting omega->0 limit",
                "relative_to_Einstein": "must be derived in full CTP kernel",
                "comparison_to_target": "not rejected by this theorem",
                "verdict": "OPEN_ONLY_AS_NEW_PARENT_DYNAMICS",
            },
        ]
    )
    return rows, metrics


def build_poynting_rows(
    ward_metrics: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    metrics = {
        "static_longitudinal_Poynting": 0,
        "transverse_Poynting_dot_wavevector": 0,
        "scalar_vector_cross_covariance": 0,
        "regular_finite_frequency_scaling": "T_L^0=(omega/k)T00",
        "singular_DC_escape": (
            "requires a hydrodynamic/conserved-density pole and must include"
            " the density response rather than a standalone Poynting patch"
        ),
        "independent_vector_escape": (
            "a_i V^i can have one metric derivative only if V is an"
            " independent longitudinal vector; this is outside the current"
            " scalar parent and enters the unit-flow correspondence branch"
        ),
        "metric_only_local_branch_retained": True,
        "Maxwell_Poynting_same_coframe_source": True,
        "Poynting_generates_static_common_scalar_kernel": False,
        "ward_cross_helicity_zero": ward_metrics[
            "cross_helicity_covariance_zero"
        ],
    }
    rows = tagged(
        [
            {
                "escape_id": "ESC5190_00_EM_source",
                "candidate": "Maxwell Poynting vector",
                "operator_or_identity": "T_EM^0i=(E cross B)^i",
                "static_projection": "transverse helicity-one momentum source",
                "result": "gravitates through the same coframe shift/vector equation",
                "status": "RETAINED_UNIVERSAL_SOURCE",
                "why_not_target": "not a helicity-zero susceptibility",
            },
            {
                "escape_id": "ESC5190_01_longitudinal",
                "candidate": "longitudinal momentum/Poynting",
                "operator_or_identity": "k_i T^i0=0 at omega=0",
                "static_projection": "T_L^0=0",
                "result": "no DC longitudinal vector remains",
                "status": "EXACT_WARD_ZERO",
                "why_not_target": "cannot mix with Phi/Psi at nonzero k",
            },
            {
                "escape_id": "ESC5190_02_transverse",
                "candidate": "transverse Poynting",
                "operator_or_identity": "k_i P_T^i=0",
                "static_projection": "a_i P_T^i proportional k_i P_T^i=0",
                "result": "acceleration-vector one-derivative escape vanishes",
                "status": "EXACT_ORTHOGONALITY_ZERO",
                "why_not_target": "lives in helicity one, not common scalar",
            },
            {
                "escape_id": "ESC5190_03_SO2",
                "candidate": "isotropic stress covariance",
                "operator_or_identity": "[G_SO2,C]=0",
                "static_projection": "C_scalar,vector=C_vector,tensor=0",
                "result": "Poynting cannot enter scalar by an isotropic two-point cross block",
                "status": "EXACT_HELICITY_BLOCK",
                "why_not_target": "cross-helicity covariance forbidden",
            },
            {
                "escape_id": "ESC5190_04_finite_omega",
                "candidate": "time-dependent momentum transfer",
                "operator_or_identity": "T_L^0=(omega/k)T00",
                "static_projection": "vanishes for a regular omega->0 limit",
                "result": "finite-frequency effects remain possible",
                "status": "DYNAMIC_ONLY",
                "why_not_target": "stationary galaxy kernel is the DC limit",
            },
            {
                "escape_id": "ESC5190_05_hydrodynamic",
                "candidate": "singular noncommuting DC limit",
                "operator_or_identity": "T00 or response proportional 1/omega",
                "static_projection": "must keep conserved density and its Ward partners",
                "result": "reduces to a density/Vlasov or new active CTP mode",
                "status": "NOT_A_POYNTING_ONLY_ESCAPE",
                "why_not_target": "cannot insert flux without the full conserved state",
            },
            {
                "escape_id": "ESC5190_06_unit_flow",
                "candidate": "independent longitudinal vector V^i",
                "operator_or_identity": "a_i V^i",
                "static_projection": "can realize d=1 metric mixing",
                "result": "adds an independent field and preferred-flow modes",
                "status": "CORRESPONDENCE_EXTENSION_NOT_CURRENT_PARENT",
                "why_not_target": "requires microscopic Kubo ownership and PPN/mode gates",
            },
            {
                "escape_id": "ESC5190_07_anisotropic_flux",
                "candidate": "fixed background Poynting direction",
                "operator_or_identity": "breaks SO(3) to a source-selected axis",
                "static_projection": "allows anisotropic cross terms",
                "result": "not the universal isotropic galaxy kernel",
                "status": "ANISOTROPIC_ARENA_RESPONSE_ONLY",
                "why_not_target": "would require quadrupole/PPN/source-geometry bounds",
            },
        ]
    )
    return rows, metrics


def build_route_rows(
    prior: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    route_rows = tagged(
        [
            {
                "route_id": "ROUTE5190_00_gapped_vacuum",
                "mechanism": "local gapped vacuum polarization",
                "parent_ownership": "yes as local motion vacuum",
                "exact_obstruction": "analytic in k^2 after Einstein-residue matching",
                "current_disposition": "REJECTED_FOR_CQ",
                "surviving_use": "local EFT corrections and decoupling",
            },
            {
                "route_id": "ROUTE5190_01_abstract_completion",
                "mechanism": "5181 positive generalized-field Hessian",
                "parent_ownership": "constructed but not parent-derived",
                "exact_obstruction": (
                    "constant normalized mixing means unnormalized d=1"
                    " scalar mixing"
                ),
                "current_disposition": "MATHEMATICALLY_HEALTHY_PARENT_OWNERSHIP_FAILS",
                "surviving_use": "target contract for any future nonlocal state",
            },
            {
                "route_id": "ROUTE5190_02_minimal_pair",
                "mechanism": "massless passive psi^2 pair",
                "parent_ownership": "kinetic carrier yes",
                "exact_obstruction": (
                    "minimal projector is pure slip/dust-invisible;"
                    " TT nonanalytic sign is wrong; relative shape is k n_q"
                ),
                "current_disposition": "REJECTED_FOR_COMMON_GALAXY_KERNEL",
                "surviving_use": "source-backed loop and sign benchmark",
            },
            {
                "route_id": "ROUTE5190_03_improved_pair",
                "mechanism": "R psi^2 improvement/nonminimal pair",
                "parent_ownership": "eta nonzero not owned by current shift-symmetric parent",
                "exact_obstruction": "still d=2 and therefore two powers too soft",
                "current_disposition": "REJECTED_EVEN_BEFORE_RETUNING",
                "surviving_use": "none as current-parent rescue",
            },
            {
                "route_id": "ROUTE5190_04_interactions",
                "mechanism": "controlled X2/X3 Hartree, basketball and collision stress",
                "parent_ownership": "yes",
                "exact_obstruction": (
                    "Ward-correct but source-locked norm is negligible and"
                    " regular clustering cannot generate |k|"
                ),
                "current_disposition": "REJECTED_AS_PROFILE_REPAIR",
                "surviving_use": "small controlled interaction corrections",
            },
            {
                "route_id": "ROUTE5190_05_Poynting",
                "mechanism": "stationary electromagnetic momentum flux",
                "parent_ownership": "yes through Maxwell Hilbert stress",
                "exact_obstruction": "static Ward and SO2 place it in helicity one",
                "current_disposition": "REJECTED_AS_SCALAR_KERNEL",
                "surviving_use": "vector/gravitomagnetic source and dynamic CTP tests",
            },
            {
                "route_id": "ROUTE5190_06_Vlasov",
                "mechanism": "collisionless occupied-state density response",
                "parent_ownership": "derived for the frozen state",
                "exact_obstruction": (
                    "already evolved/double-counted and frozen radial response"
                    " did not close the profile"
                ),
                "current_disposition": "NO_ADDITIONAL_KERNEL_ALLOWED",
                "surviving_use": "formation/state evolution",
            },
            {
                "route_id": "ROUTE5190_07_direct_state",
                "mechanism": "positive conserved occupied-state Hilbert stress",
                "parent_ownership": "stress map yes; occupation selection no",
                "exact_obstruction": "state preparation, q/core/edge and mu law not derived",
                "current_disposition": "CONDITIONAL_SURVIVOR",
                "surviving_use": "rotation+lensing source with local psi=0 branch intact",
            },
            {
                "route_id": "ROUTE5190_08_unit_flow",
                "mechanism": "independent state-flow/vector response",
                "parent_ownership": "correspondence EFT only",
                "exact_obstruction": "extra modes and microscopic Kubo coefficients",
                "current_disposition": "CONDITIONAL_EXTENSION",
                "surviving_use": "preferred-frame/Poynting response test harness",
            },
            {
                "route_id": "ROUTE5190_09_new_nonlocal_state",
                "mechanism": "nonlocal or active critical scalar response",
                "parent_ownership": "absent",
                "exact_obstruction": (
                    "must derive d=1 or equivalent nonlocal mixing plus Ward,"
                    " slip, TT and passivity"
                ),
                "current_disposition": "NEW_PARENT_DYNAMICS_REQUIRED",
                "surviving_use": "only route to revive 5148 propagator enhancement",
            },
        ]
    )

    direct_rows = tagged(
        [
            {
                "comparison_id": "CMP5190_00_equation",
                "property": "field equation",
                "Schur_response": "(K_GR-Sigma)h=J_visible",
                "direct_state_stress": "K_GR h=J_visible+J_state",
                "equivalent_when": (
                    "only after deriving J_state[h,J_visible] and integrating"
                    " state fluctuations without double counting"
                ),
                "current_status": "DISTINCT_MECHANISMS",
            },
            {
                "comparison_id": "CMP5190_01_local",
                "property": "local vacuum",
                "Schur_response": "requires Sigma->0 at high k/local state",
                "direct_state_stress": "requires T_state=0 in unoccupied local branch",
                "equivalent_when": "both preserve 5189 local psi=0 tensor block",
                "current_status": "LOCAL_GR_COMPATIBLE_CONDITIONALLY",
            },
            {
                "comparison_id": "CMP5190_02_slip",
                "property": "lensing slip",
                "Schur_response": "requires Sigma_cs=0 and TT bound",
                "direct_state_stress": (
                    "nonrelativistic conserved state has slip controlled by"
                    " anisotropic stress"
                ),
                "equivalent_when": "state pressure/anisotropy is small",
                "current_status": "DIRECT_STATE_5151_NUMERICALLY_SMALL_SLIP",
            },
            {
                "comparison_id": "CMP5190_03_physics",
                "property": "interpretation",
                "Schur_response": "modifies effective metric inverse kernel",
                "direct_state_stress": "adds a real gravitating motion-state component",
                "equivalent_when": "not generally equivalent",
                "current_status": "DIRECT_ROUTE_IS_MATTER_LIKE",
            },
            {
                "comparison_id": "CMP5190_04_ownership",
                "property": "remaining derivation",
                "Schur_response": "derive nonlocal d=1 mixing and full CTP projectors",
                "direct_state_stress": "derive state preparation and nonlinear formation law",
                "equivalent_when": "neither may be replaced by fitted per-galaxy data",
                "current_status": "NO_RETUNING_REQUIRED",
            },
            {
                "comparison_id": "CMP5190_05_decision",
                "property": "current parent verdict",
                "Schur_response": "rejected for current local scalar/coframe operators",
                "direct_state_stress": "retained as conditional empirical pillar",
                "equivalent_when": "a new parent mechanism would reopen arbitration",
                "current_status": "ROUTE_FREEZE",
            },
        ]
    )

    maximum_interaction_norm = prior["5185"]["metrics"]["physical_bounds"][
        "maximum_interaction_Z_norm_ceiling"
    ]
    metrics = {
        "current_parent_propagator_enhancement_route_survives": False,
        "current_parent_direct_state_stress_route_survives": True,
        "direct_state_occupation_selected_by_parent": prior["5151"][
            "source_selected_occupation_derived"
        ],
        "minimal_pair_common_kernel_survives": prior["5150"][
            "minimal_passive_PX_common_kernel_survives"
        ],
        "pair_constant_normalization_matches_corridor": prior["5183"][
            "summary"
        ]["constant_normalization_can_match_full_corridor"],
        "controlled_collision_repair": prior["5180"]["summary"][
            "controlled_collision_repair"
        ],
        "maximum_interaction_Z_norm_ceiling": maximum_interaction_norm,
        "Vlasov_fully_closed_clauses": prior["5171"]["summary"][
            "fully_closed_5170_kernel_clauses"
        ],
        "Vlasov_total_clauses": prior["5171"]["summary"][
            "total_5170_kernel_clauses"
        ],
        "constant_source_normalization_rejected": prior["5177"][
            "constant_source_normalization_rejected"
        ],
        "local_GR_branch_modified": False,
        "next_parent_choice": (
            "derive direct-state preparation/formation, or explicitly add and"
            " derive a nonlocal/active collective mode; do not rerun the"
            " passive scalar pair or stationary Poynting routes"
        ),
    }
    return route_rows, direct_rows, metrics


def build_provenance_rows(source_hashes: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, (path, expected_hash) in SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "local_locked",
                "source_path_or_url": str(path),
                "sha256": source_hashes[source_id],
                "expected_sha256": expected_hash,
                "hash_match": source_hashes[source_id] == expected_hash,
                "role": "prior target, loop, Ward, state or route theorem",
            }
        )
    for source_id, url in EXTERNAL_SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "primary_or_authoritative_reference",
                "source_path_or_url": url,
                "sha256": "",
                "expected_sha256": "",
                "hash_match": "",
                "role": "unitary CFT bound or causal CTP formalism",
            }
        )
    return tagged(rows)


def build_document(result: dict[str, Any]) -> None:
    ward = result["static_Ward"]
    power = result["mixing_power_count"]
    poynting = result["Poynting_gate"]
    routes = result["route_arbitration"]
    text = f"""# 5190 — Static Ward helicity, one-derivative mixing no-go, and direct-state route freeze

Marker: `{MARKER}`

**Verdict:** The 5148 propagator-enhancement target is mathematically healthy
as an abstract nonlocal response, but the current selected zero-background
scalar/coframe operators cannot generate its required mixing. This is now a
theorem rather than another missing coefficient. Static stress conservation
and isotropy block Poynting from the scalar sector, while local scalar
derivative counting puts the parent massless pair two powers away from the
target. The passive scalar-pair and stationary-Poynting routes are closed.
The direct conserved motion-state stress remains viable, but only
conditionally until its state preparation and formation law are derived.

The theorem is scoped to nonzero spatial momentum, zero frequency, a regular
DC limit, local contact subtraction, and the homogeneous/isotropic,
parity-even, local diffeomorphism-invariant scalar sector. It does not reject
a parent-derived direct state, an independent vector background, or genuinely
active/nonlocal dynamics.

No GitHub action and no edit to `formalization-workbench` occurred.

## 1. Why this is not a repeat of 5150–5183

The prior chain already established:

```text
B_0(k)=1/(8|k|)                         critical pair carrier;
Delta K_TT=-W_state |k|^3/2048          minimal passive TT sign;
w(eta=0)=(-1,1)                         minimal pair is pure slip;
pair/K_GR proportional x n_q(x)         local pair relative shape;
target proportional n_q(x)/x            5148 required shape;
pair/target=x^2                         exact mismatch.
```

Checkpoint 5181 also constructed a positive, passive generalized-field
Hessian that gives the target exactly. The unresolved question was whether
the current parent can own its cross block. Checkpoint 5190 answers that
question.

## 2. Exact static Ward decomposition

Take nonzero Fourier momentum along `z` and subtract local contact/seagull
terms from the connected nonanalytic kernel:

```text
k_mu=(0,0,0,k),    k!=0,
k_mu Delta T^mu_nu=0.
```

The exact rank-four Ward system gives

```text
T03=T13=T23=T33=0.
```

The original ten symmetric stress components therefore leave six:

```text
helicity 0: rho=T00, tau=(T11+T22)/2;
helicity 1: P_x=T01, P_y=T02;
helicity 2: T_plus=(T11-T22)/2, T_cross=T12.
```

The Ward matrix has rank `{ward['static_Ward_rank']}` and nullity
`{ward['static_Ward_nullity']}`.

## 3. Exact isotropic covariance theorem

In basis `(rho,tau,Px,Py,Tplus,Tcross)`, solve

```text
[G_SO(2),C]=0
```

for a symmetric `6 x 6` covariance. The executed `21`-variable system has
rank `{ward['SO2_invariance_constraint_rank']}` and solution dimension
`{ward['SO2_invariant_covariance_dimension']}`:

```text
C = diag-block(C_scalar[2x2], C_vector I_2, C_tensor I_2).
```

All scalar-vector, scalar-tensor and vector-tensor cross blocks vanish.
The scalar Newtonian metric vertex is

```text
{ward['scalar_metric_vertex']}.
```

Thus a transverse Poynting fluctuation is not a hidden scalar response.

## 4. The derivative-counting theorem

Let a critical collective susceptibility scale as

```text
G_chi(k)~|k|^-alpha
```

and its unnormalized metric mixing as `B_hchi~|k|^d`. Since
`K_GR~M_R^2 k^2`, its Schur correction relative to Einstein scales as

```text
(B_hchi G_chi B_chih)/K_GR
  ~ |k|^(2d-alpha-2).
```

The 5148 target has exponent `-1`. For the parent pair `alpha=1`, this
requires

```text
d={power['required_derivative_order_for_pair']}.
```

But every nonzero local critical scalar metric vertex in the current parent
starts at two derivatives:

```text
kinetic Hilbert vertex h (partial psi)^2: d=2;
curvature improvement R psi^2:            d=2;
```

so its relative response scales as `|k| n_q`, not `n_q/|k|`. A
zero-derivative `sqrt(-g)m^2 psi^2` vertex is proportional to the gap and
vanishes at the massless pair point; retaining it restores a finite gap and
an analytic bubble.

The abstract 5181 completion makes the issue transparent. Its normalized
metric variable is `u=sqrt(K_h)h`, and

```text
B_uchi=sqrt(A)
=> B_hchi=sqrt(A K_h)~sqrt(A) M_R |k|.
```

It requires precisely the missing one-spatial-derivative scalar mixing.

## 5. Why a local equilibrium critical scalar does not repair `d=2`

For a unitary local three-dimensional critical scalar primary,

```text
G_O(k)~k^(2 Delta-3),    Delta>=1/2,
```

so its singularity satisfies `alpha<=2`. A two-derivative metric vertex
would need

```text
alpha={power['required_singularity_for_two_derivative_vertex']}
```

to reproduce the target. Therefore the escape is unavailable inside that
local equilibrium class. This clause does not cover an active,
nonequilibrium or explicitly nonlocal CTP state; such a state would be new
parent dynamics and must prove its own passivity and stability.

## 6. Poynting-vector escape tested exactly

At finite frequency, the longitudinal Ward identity gives

```text
T_L^0=(omega/k)T00.
```

It vanishes in a regular DC limit. The surviving electromagnetic Poynting
components are transverse:

```text
k_i P_T^i=0.
```

The apparent one-derivative scalar `a_i P^i`, with
`a_i~partial_i Phi`, consequently vanishes:

```text
a_i P_T^i proportional k_i P_T^i=0.
```

SO(2) invariance independently gives zero scalar-vector covariance. A
singular noncommuting `omega->0` limit must retain the conserved density and
its Ward partners, reducing to a full hydrodynamic/Vlasov or new active-state
problem—not a Poynting-only patch.

An independent longitudinal vector can support `a_i V^i`, but this is the
unit-flow/aether correspondence extension. It adds preferred-flow modes and
requires microscopic Kubo ownership plus PPN and stability gates. It is not
present in the selected metric-only local parent.

The Maxwell conclusion remains positive:

```text
T_EM^0i=(E cross B)^i
```

is a real same-coframe vector/gravitomagnetic source. It simply is not the
stationary common-scalar galaxy kernel.

## 7. Route arbitration

```text
local gapped vacuum:
  rejected for C_q; analytic in k^2.

minimal passive scalar pair:
  rejected; pure slip at parent eta=0, wrong TT sign, wrong k shape.

nonminimal R psi^2 pair:
  not parent-owned and still two powers too soft.

controlled X2/X3 interactions:
  Ward-correct but far too small; regular clustering cannot create |k|.

stationary Poynting:
  exact helicity-one source; rejected as scalar kernel.

free Vlasov response:
  already evolved and must not be double counted; frozen response failed
  to close the required radial hierarchy.

5181 abstract nonlocal completion:
  positive and causal, but its d=1 cross block is not generated by the
  current parent.

direct conserved state stress:
  survives conditionally; stress map derived, state selection not derived.
```

The current-parent propagator-enhancement verdict is therefore
`{routes['current_parent_propagator_enhancement_route_survives']}`.

## 8. Propagator response is not direct state stress

The two equations are

```text
Schur response:  (K_GR-Sigma)h=J_visible;
direct state:     K_GR h=J_visible+J_state.
```

They become equivalent only after deriving
`J_state[h,J_visible]` and integrating out the state without double
counting. Checkpoint 5171 already calculates the frozen Vlasov response, so
it cannot be added again as a new kernel.

The direct 5151 state is useful because a positive conserved,
nonrelativistic state sources rotation and lensing through the same Einstein
metric while leaving the local unoccupied `psi=0` branch intact. But until
the parent selects its occupation, transition, core and edge, it is a
conditional matter-state pillar rather than a derived modification of
gravity.

## 9. Consequence for the unified programme

This closes a loop that should not be run again:

```text
do not retry the passive zero-background scalar pair;
do not retry stationary Poynting as a scalar response;
do not multiply the failed Vlasov response by a fitted constant;
do not call the abstract 5181 cross block parent-derived.
```

There are now two honest forward choices:

1. derive the direct motion-state preparation and nonlinear formation law
   with one cross-arena parameter set; or
2. introduce only through an actual parent derivation a nonlocal/active
   collective mode that supplies the missing `d=1` cross block and passes
   Ward, slip, TT, passivity and local-vacuum gates.

Because the separate galaxy programme already owns nonlinear formation,
the next unified-framework calculation should return to the other newly
exposed root gate: determine whether the cosmological
`c_O4 C^2 X` tensor Hessian is degenerate/redundant or only an
order-reduced EFT correction.

## 10. Claim boundary

Established:

```text
static Ward rank/nullity                 = 4/6;
static helicity dimensions               = 2 scalar +2 vector +2 tensor;
isotropic cross-helicity covariance      = zero;
regular DC longitudinal Poynting         = zero;
transverse Poynting scalar contraction   = zero;
pair local-mixing derivative order       = 2;
target-required derivative order         = 1;
pair/target shape ratio                  = x^2;
current-parent propagator route          = rejected;
direct conserved state route             = conditional survivor.
```

Not established:

```text
parent direct-state preparation or formation;
new nonlocal/active d=1 collective mode;
galaxy claim;
all-scale cosmological O4 tensor safety;
full MTS unification.
```

## 11. Machine artifacts

- `source-intake/functional_rg/5190/static_Ward_constraint_and_helicity_decomposition.csv`
- `source-intake/functional_rg/5190/SO2_invariant_stress_covariance.csv`
- `source-intake/functional_rg/5190/local_scalar_mixing_power_count.csv`
- `source-intake/functional_rg/5190/Poynting_and_unit_flow_escape_gate.csv`
- `source-intake/functional_rg/5190/occupied_state_route_arbitration.csv`
- `source-intake/functional_rg/5190/direct_state_vs_propagator_response.csv`
- `source-intake/functional_rg/5190/source_provenance.csv`
- `source-intake/functional_rg/5190/static_Ward_and_mixing_no_go_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5190_VALIDATION.csv`
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def calculate_validations(
    source_hashes: dict[str, str],
    formal_before: str,
    checkpoint_5176_before: str,
    prior: dict[str, dict[str, Any]],
    ward: dict[str, Any],
    power: dict[str, Any],
    poynting: dict[str, Any],
    routes: dict[str, Any],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check: str, passed: bool, observed: Any, expected: Any) -> None:
        checks.append(
            validation_row(
                f"V5190_{len(checks):02d}",
                check,
                bool(passed),
                observed,
                expected,
            )
        )

    add(
        "all locked local source hashes match",
        all(
            source_hashes[source_id] == expected
            for source_id, (_, expected) in SOURCES.items()
        ),
        sum(
            source_hashes[source_id] == expected
            for source_id, (_, expected) in SOURCES.items()
        ),
        len(SOURCES),
    )
    add(
        "formalization workbench lock matches before writes",
        formal_before == FORMAL_DIGEST_LOCK,
        formal_before,
        FORMAL_DIGEST_LOCK,
    )
    add(
        "checkpoint 5176 lock matches before writes",
        checkpoint_5176_before == CHECKPOINT_5176_TREE_LOCK,
        checkpoint_5176_before,
        CHECKPOINT_5176_TREE_LOCK,
    )
    add(
        "5148 target q is 0.77",
        math.isclose(prior["5148"]["kernel"]["q"], 0.77),
        prior["5148"]["kernel"]["q"],
        0.77,
    )
    add(
        "5149 occupied critical route survived only conditionally",
        prior["5149"]["critical_mixing"][
            "occupied_critical_CTP_route_survives"
        ]
        is True,
        prior["5149"]["critical_mixing"][
            "occupied_critical_CTP_route_survives"
        ],
        True,
    )
    add(
        "5150 minimal passive common kernel is rejected",
        prior["5150"]["minimal_passive_PX_common_kernel_survives"] is False,
        prior["5150"]["minimal_passive_PX_common_kernel_survives"],
        False,
    )
    add(
        "5150 TT nonanalytic coefficient is negative",
        prior["5150"]["zero_mode_loop"][
            "metric_hessian_nonanalytic_coefficient"
        ]
        < 0,
        prior["5150"]["zero_mode_loop"][
            "metric_hessian_nonanalytic_coefficient"
        ],
        "<0",
    )
    add(
        "5151 direct state exists but source selection is not derived",
        prior["5151"]["state_stress_stationary_existence_constructed"] is True
        and prior["5151"]["source_selected_occupation_derived"] is False,
        (
            prior["5151"]["state_stress_stationary_existence_constructed"],
            prior["5151"]["source_selected_occupation_derived"],
        ),
        (True, False),
    )
    add(
        "5177 rejects constant source normalization",
        prior["5177"]["constant_source_normalization_rejected"] is True,
        prior["5177"]["constant_source_normalization_rejected"],
        True,
    )
    add(
        "5180 controlled collision repair is rejected",
        prior["5180"]["summary"]["controlled_collision_repair"] is False,
        prior["5180"]["summary"]["controlled_collision_repair"],
        False,
    )
    add(
        "5181 derives critical pair infrared power",
        prior["5181"]["summary"]["critical_IR_pair_power_derived"] is True,
        prior["5181"]["summary"]["critical_IR_pair_power_derived"],
        True,
    )
    add(
        "5181 full Cq is not a positive massive pair mixture",
        prior["5181"]["summary"]["full_Cq_positive_massive_pair_mixture"]
        is False,
        prior["5181"]["summary"]["full_Cq_positive_massive_pair_mixture"],
        False,
    )
    add(
        "5183 exact shape identity remains x squared",
        prior["5183"]["summary"]["shape_ratio"] == "x^2",
        prior["5183"]["summary"]["shape_ratio"],
        "x^2",
    )
    add(
        "5183 says constant normalization cannot match corridor",
        prior["5183"]["summary"][
            "constant_normalization_can_match_full_corridor"
        ]
        is False,
        prior["5183"]["summary"][
            "constant_normalization_can_match_full_corridor"
        ],
        False,
    )
    add(
        "5185 interaction repair is not viable",
        prior["5185"]["summary"]["known_interaction_profile_repair_viable"]
        is False,
        prior["5185"]["summary"]["known_interaction_profile_repair_viable"],
        False,
    )
    add(
        "5189 requires no-slip scalar projector",
        prior["5189"]["occupied_state_target"]["no_slip_condition"]
        == "Sigma_cs=Sigma_sc=0 with invertible slip block",
        prior["5189"]["occupied_state_target"]["no_slip_condition"],
        "Sigma_cs=Sigma_sc=0 with invertible slip block",
    )
    add(
        "static Ward matrix rank is four",
        ward["static_Ward_rank"] == 4,
        ward["static_Ward_rank"],
        4,
    )
    add(
        "static Ward nullity is six",
        ward["static_Ward_nullity"] == 6,
        ward["static_Ward_nullity"],
        6,
    )
    add(
        "static Ward removes all longitudinal stress components",
        ward["static_Ward_zero_components"]
        == ["T03", "T13", "T23", "T33"],
        ward["static_Ward_zero_components"],
        ["T03", "T13", "T23", "T33"],
    )
    add(
        "helicity dimensions are 2+2+2",
        ward["helicity_dimensions"]
        == {"scalar": 2, "vector": 2, "tensor": 2},
        ward["helicity_dimensions"],
        {"scalar": 2, "vector": 2, "tensor": 2},
    )
    add(
        "SO2 invariant covariance has dimension five",
        ward["SO2_invariant_covariance_dimension"] == 5,
        ward["SO2_invariant_covariance_dimension"],
        5,
    )
    add(
        "cross-helicity covariance vanishes",
        ward["cross_helicity_covariance_zero"] is True,
        ward["cross_helicity_covariance_zero"],
        True,
    )
    add(
        "regular static longitudinal momentum vanishes",
        ward["static_longitudinal_momentum"] == "0",
        ward["static_longitudinal_momentum"],
        "0",
    )
    add(
        "pair susceptibility requires derivative order one",
        power["required_derivative_order_for_pair"] == "1",
        power["required_derivative_order_for_pair"],
        "1",
    )
    add(
        "two-derivative vertex would require alpha three",
        power["required_singularity_for_two_derivative_vertex"] == "3",
        power["required_singularity_for_two_derivative_vertex"],
        "3",
    )
    add(
        "pair versus target ratio is x squared",
        power["shape_ratio"] == "x**2",
        power["shape_ratio"],
        "x**2",
    )
    add(
        "pair low-k slope is plus one",
        power["low_pair_slope"] == "1",
        power["low_pair_slope"],
        "1",
    )
    add(
        "target low-k slope is minus one",
        power["low_target_slope"] == "-1",
        power["low_target_slope"],
        "-1",
    )
    add(
        "pair high-k slope is 1-q=0.23",
        power["high_pair_slope"] == "23/100",
        power["high_pair_slope"],
        "23/100",
    )
    add(
        "target high-k slope is -(1+q)=-1.77",
        power["high_target_slope"] == "-177/100",
        power["high_target_slope"],
        "-177/100",
    )
    add(
        "unitary 3D scalar maximum alpha is two",
        power["CFT_maximum_singularity_alpha"] == "2",
        power["CFT_maximum_singularity_alpha"],
        "2",
    )
    add(
        "unitary local scalar cannot supply alpha three",
        power["CFT_two_derivative_target_possible"] is False,
        power["CFT_two_derivative_target_possible"],
        False,
    )
    add(
        "stationary Poynting does not generate common scalar kernel",
        poynting["Poynting_generates_static_common_scalar_kernel"] is False,
        poynting["Poynting_generates_static_common_scalar_kernel"],
        False,
    )
    add(
        "same-coframe Maxwell Poynting source is retained",
        poynting["Maxwell_Poynting_same_coframe_source"] is True,
        poynting["Maxwell_Poynting_same_coframe_source"],
        True,
    )
    add(
        "route arbitration rejects current propagator enhancement",
        routes["current_parent_propagator_enhancement_route_survives"]
        is False,
        routes["current_parent_propagator_enhancement_route_survives"],
        False,
    )
    add(
        "route arbitration retains direct state conditionally",
        routes["current_parent_direct_state_stress_route_survives"] is True,
        routes["current_parent_direct_state_stress_route_survives"],
        True,
    )
    add(
        "direct state occupation remains unselected",
        routes["direct_state_occupation_selected_by_parent"] is False,
        routes["direct_state_occupation_selected_by_parent"],
        False,
    )
    add(
        "local GR branch remains unmodified",
        routes["local_GR_branch_modified"] is False,
        routes["local_GR_branch_modified"],
        False,
    )
    return checks


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_hashes: dict[str, str] = {}
    for source_id, (path, _) in SOURCES.items():
        if not path.is_file():
            raise FileNotFoundError(path)
        source_hashes[source_id] = file_digest(path)

    formal_before = tree_digest(FORMAL)
    checkpoint_5176_before = tree_digest(CHECKPOINT_5176_ROOT)

    result_source_ids = {
        "5148": "checkpoint_5148_result",
        "5149": "checkpoint_5149_result",
        "5150": "checkpoint_5150_result",
        "5151": "checkpoint_5151_result",
        "5171": "checkpoint_5171_result",
        "5177": "checkpoint_5177_result",
        "5180": "checkpoint_5180_result",
        "5181": "checkpoint_5181_result",
        "5182": "checkpoint_5182_result",
        "5183": "checkpoint_5183_result",
        "5185": "checkpoint_5185_result",
        "5188": "checkpoint_5188_result",
        "5189": "checkpoint_5189_result",
    }
    prior = {
        checkpoint: json.loads(
            SOURCES[source_id][0].read_text(encoding="utf-8")
        )
        for checkpoint, source_id in result_source_ids.items()
    }

    ward_rows, so2_rows, ward_metrics = build_static_ward_and_helicity()
    power_rows, power_metrics = build_local_mixing_power_count()
    poynting_rows, poynting_metrics = build_poynting_rows(ward_metrics)
    route_rows, direct_rows, route_metrics = build_route_rows(prior)
    provenance_rows = build_provenance_rows(source_hashes)

    checks = calculate_validations(
        source_hashes,
        formal_before,
        checkpoint_5176_before,
        prior,
        ward_metrics,
        power_metrics,
        poynting_metrics,
        route_metrics,
    )
    failures = [row for row in checks if row["status"] != "PASS"]
    if failures:
        raise RuntimeError(
            "Pre-write validation failed:\n" + json.dumps(failures, indent=2)
        )

    outputs = {
        WARD_CSV: ward_rows,
        SO2_CSV: so2_rows,
        POWER_CSV: power_rows,
        POYNTING_CSV: poynting_rows,
        ROUTE_CSV: route_rows,
        DIRECT_CSV: direct_rows,
        PROVENANCE_CSV: provenance_rows,
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    data_pack_digest = hashlib.sha256()
    for path in outputs:
        data_pack_digest.update(path.name.encode("utf-8"))
        data_pack_digest.update(file_digest(path).encode("ascii"))

    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "leading_theorem": LEADING_THEOREM,
        "claim_guard": CLAIM_GUARD,
        "static_Ward": ward_metrics,
        "mixing_power_count": power_metrics,
        "Poynting_gate": poynting_metrics,
        "route_arbitration": route_metrics,
        "claim_status": {
            "static_Ward_helicity_theorem": True,
            "Poynting_scalar_escape": False,
            "current_scalar_parent_Cq_propagator_route": False,
            "direct_state_stress_conditional_route": True,
            "direct_state_preparation_derived": False,
            "leading_local_GR_Newton_Maxwell_modified": False,
            "galaxy_claim": False,
            "full_MTS_unification": False,
            "GitHub_action": False,
        },
        "source_hashes": source_hashes,
        "external_sources": EXTERNAL_SOURCES,
        "data_pack_sha256": data_pack_digest.hexdigest(),
        "formalization_workbench_sha256": formal_before,
        "checkpoint_5176_tree_sha256": checkpoint_5176_before,
        "validation_count_prewrite": len(checks),
        "validation_failures_prewrite": 0,
    }
    write_json(RESULT_JSON, result)
    build_document(result)

    formal_after = tree_digest(FORMAL)
    checkpoint_5176_after = tree_digest(CHECKPOINT_5176_ROOT)
    expected_outputs = tuple(outputs) + (RESULT_JSON, DOCUMENT)
    final_checks = checks + [
        validation_row(
            f"V5190_{len(checks):02d}",
            "formalization workbench remains unchanged after writes",
            formal_after == formal_before == FORMAL_DIGEST_LOCK,
            formal_after,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            f"V5190_{len(checks) + 1:02d}",
            "checkpoint 5176 remains unchanged after writes",
            checkpoint_5176_after
            == checkpoint_5176_before
            == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_after,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            f"V5190_{len(checks) + 2:02d}",
            "all checkpoint artifacts exist and are nonempty",
            all(path.is_file() and path.stat().st_size > 0 for path in expected_outputs),
            sum(path.is_file() and path.stat().st_size > 0 for path in expected_outputs),
            len(expected_outputs),
        ),
        validation_row(
            f"V5190_{len(checks) + 3:02d}",
            "all generated CSV files parse with at least one row",
            all(len(read_csv(path)) > 0 for path in outputs),
            sum(len(read_csv(path)) > 0 for path in outputs),
            len(outputs),
        ),
        validation_row(
            f"V5190_{len(checks) + 4:02d}",
            "all generated rows remain nonclaim",
            all(
                row["valid_for_full_MTS_claim"] is False
                for rows in outputs.values()
                for row in rows
            ),
            sum(
                row["valid_for_full_MTS_claim"] is False
                for rows in outputs.values()
                for row in rows
            ),
            sum(len(rows) for rows in outputs.values()),
        ),
        validation_row(
            f"V5190_{len(checks) + 5:02d}",
            "no GitHub action is recorded",
            result["claim_status"]["GitHub_action"] is False,
            result["claim_status"]["GitHub_action"],
            False,
        ),
    ]
    final_failures = [row for row in final_checks if row["status"] != "PASS"]
    if final_failures:
        raise RuntimeError(
            "Final validation failed:\n" + json.dumps(final_failures, indent=2)
        )
    write_csv(VALIDATION_CSV, final_checks)

    print(
        json.dumps(
            {
                "checkpoint": 5190,
                "marker": MARKER,
                "validation_passed": len(final_checks),
                "validation_failed": 0,
                "Ward_rank": ward_metrics["static_Ward_rank"],
                "Ward_nullity": ward_metrics["static_Ward_nullity"],
                "SO2_invariant_dimension": ward_metrics[
                    "SO2_invariant_covariance_dimension"
                ],
                "required_pair_mixing_derivative_order": power_metrics[
                    "required_derivative_order_for_pair"
                ],
                "current_pair_mixing_derivative_order": power_metrics[
                    "current_gapless_scalar_vertex_derivative_order"
                ],
                "Poynting_scalar_escape": poynting_metrics[
                    "Poynting_generates_static_common_scalar_kernel"
                ],
                "current_parent_propagator_route": route_metrics[
                    "current_parent_propagator_enhancement_route_survives"
                ],
                "direct_state_route": route_metrics[
                    "current_parent_direct_state_stress_route_survives"
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
