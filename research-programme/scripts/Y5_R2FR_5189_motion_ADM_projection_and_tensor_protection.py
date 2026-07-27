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
OUT = POST / "source-intake" / "functional_rg" / "5189"

ANCESTRY_CSV = OUT / "motion_ancestry_and_field_ownership.csv"
ADM_STRESS_CSV = OUT / "scalar_ADM_stress_and_current_projection.csv"
IRREP_CSV = OUT / "branch_Hessian_irrep_projection.csv"
O4_TT_CSV = OUT / "O4_TT_principal_symbol_and_EFT_gate.csv"
CONSTRAINT_CSV = OUT / "ADM_constraint_and_mode_count.csv"
UNIT_FLOW_CSV = OUT / "unit_flow_correspondence_compatibility.csv"
BRANCH_CSV = OUT / "local_cosmology_galaxy_branch_matrix.csv"
RESPONSE_CSV = OUT / "occupied_state_response_target.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "motion_ADM_projection_results.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5189_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5189-Y5-R2FR-motion-sector-ADM-projection-clock-only-ancestry-"
    "and-local-tensor-protection-theorem.md"
)

MARKER = "MTS_5189_MOTION_ADM_CLOCK_ONLY_AND_TENSOR_PROTECTION_THEOREM"
CHECKED_DATE = "2026-07-24"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_TREE_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
CHECKPOINT_5176_ROOT = POST / "source-intake" / "functional_rg" / "5176"

LEADING_THEOREM = (
    "THE_SURVIVING_MTS_MOTION_SCALAR_HAS_AN_EXACT_ADM_INTERPRETATION_AS_"
    "A_HYPERSURFACE_ORTHOGONAL_CLOCK_AND_MATTER_DEGREE_OF_FREEDOM_BUT_"
    "DOES_NOT_DETERMINE_THE_SIX_COMPONENT_SPATIAL_METRIC_OR_THE_THREE_"
    "SPATIAL_COFRAME_LEGS_MINIMAL_PX_COUPLING_PRESERVES_THE_DIFF_"
    "CONSTRAINTS_AND_CARRIES_ONE_SCALAR_MODE_IN_ADDITION_TO_THE_TWO_"
    "GRAVITON_MODES_THE_LOCAL_PSI_ZERO_BRANCH_HAS_ZERO_METRIC_SCALAR_"
    "MIXING_AND_EXACTLY_PROTECTS_THE_QUADRATIC_TWO_TENSOR_GRAVITY_"
    "SECTOR_THE_HOMOGENEOUS_CLOCK_BRANCH_HAS_ZERO_PX_TT_HESSIAN_BUT_"
    "THE_C_SQUARED_GRADIENT_PSI_SQUARED_OPERATOR_HAS_A_NONZERO_TT_"
    "HESSIAN_EVEN_WHEN_BACKGROUND_WEYL_IS_ZERO_SO_IT_REQUIRES_EFT_"
    "SMALLNESS_OR_A_PARENT_DEGENERACY_THEOREM_THE_REQUIRED_GALAXY_"
    "KERNEL_IS_STATICALLY_POSITIVE_AND_SLIP_COMPATIBLE_BUT_IS_"
    "NONANALYTIC_AND_CANNOT_BE_GENERATED_BY_A_LOCAL_GAPPED_VACUUM_"
    "POLARIZATION_AFTER_EINSTEIN_RESIDUE_MATCHING"
)

CLAIM_GUARD = (
    "THIS_DERIVES_THE_ADM_STRESS_CURRENT_ANCESTRY_MODE_COUNT_LOCAL_"
    "TENSOR_PROTECTION_O4_QUADRATIC_OBSTRUCTION_AND_THE_REQUIRED_"
    "OCCUPIED_STATE_PROJECTOR_CONDITIONS_IT_DOES_NOT_DERIVE_THE_"
    "SPATIAL_COFRAME_FROM_THE_OLD_SCALAR_DOES_NOT_DERIVE_THE_"
    "OCCUPIED_STATE_CTP_SPECTRAL_DENSITY_OR_ITS_MU_LAW_DOES_NOT_"
    "PREDICT_THE_ABSOLUTE_NEWTON_SCALE_AND_IS_NOT_A_FULL_MTS_"
    "UNIFICATION_OR_GALAXY_CLAIM"
)

PARENT_ACTION = (
    "Gamma_parent=Gamma_EH[e]+Gamma_Maxwell[e,A]+S_visible[e,A,Phi_SM]"
    "+int sqrt(-g) P(X,psi)+c_O4 int sqrt(-g) C^2 X"
    "+Gamma_contact+Gamma_nonlocal+Gamma_p8plus;"
    " X=g^munu nabla_mu psi nabla_nu psi;"
    " c_O4 is the signed coefficient actually multiplying C^2 X"
)


def source_path(relative: str) -> Path:
    return POST / Path(relative.replace("/", "\\"))


SOURCES: dict[str, tuple[Path, str]] = {
    "checkpoint_2048_motion_load_coframe": (
        source_path(
            "2048-Y5-R2FR-motion-load-coframe-construction-or-CMTS-"
            "provenance.md"
        ),
        "010b77e9fe7cabdaab18d1d3667d7772225278d3715fb3d1ee15493771411a0d",
    ),
    "checkpoint_4857_unit_flow": (
        source_path(
            "4857-Y5-R2FR-parent-time-coframe-kinetic-owner-or-PPN-safe-"
            "coefficient-surface-and-mode-stability-gate.md"
        ),
        "28f35d701e2df3a0ca3b2b6e1a69cbee0aec2d08b73742cdd487c82f22e8eb54",
    ),
    "checkpoint_4872_primitive_flow_rank": (
        source_path(
            "4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-"
            "universal-source-coupling-or-correspondence-demotion.md"
        ),
        "9a4eaed25f41167381ea77437350c322f7a4ee9cfab3228cfc2db0bd5f204923",
    ),
    "checkpoint_4873_metric_only_quotient": (
        source_path(
            "4873-Y5-R2FR-covariant-open-parent-action-and-connected-"
            "covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-"
            "EFT-freeze.md"
        ),
        "af2c97091477525fb7244e5b2577e4a4c70d863987ebbb39b6c974d978b38b6e",
    ),
    "checkpoint_4916_covariant_motion": (
        source_path(
            "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-"
            "action-to-integrated-H-parent-and-no-direct-flow-charge-or-"
            "primitive-freeze.md"
        ),
        "4c20db8f8f75d81bab3c2a6d334cbcefeb2f2c1d66266be0ec412947c705b636",
    ),
    "checkpoint_4935_motion_entry": (
        source_path(
            "4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-"
            "and-motion-sector-entry.md"
        ),
        "649da892ba5c256b7670206e837604dbbe04358fcd3705b5871906805e00c1df",
    ),
    "checkpoint_4935_result": (
        source_path(
            "source-intake/functional_rg/4935/motion_sector_entry_results.json"
        ),
        "ba3dfdaacfb1e3d00282d82c4b4656a937e033cb9145e94c71b81e9c42a54240",
    ),
    "checkpoint_4956_functional_PX": (
        source_path(
            "4956-Y5-R2FR-functional-PX-motion-flow-gravity-source-and-"
            "convergence-or-derivative-hierarchy-rejection.md"
        ),
        "c3cdc970258583882c13d6544e17c8cef2620d89002ee7998825566ce6630367",
    ),
    "checkpoint_4956_result": (
        source_path(
            "source-intake/functional_rg/4956/"
            "functional_PX_fixed_function_results.json"
        ),
        "06ee62bfba50e5b1411e59e5cc707110a52f893c556331ba178032748d7563fb",
    ),
    "checkpoint_5148_spectral_response": (
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
    "checkpoint_5184_stationary_PX": (
        source_path(
            "5184-Y5-R2FR-stationary-PX-background-no-lump-and-mixed-"
            "Hessian-gate.md"
        ),
        "e4a3427963b4de0b5b40baab67b905e9e7054e8033c72dee768fb8973a258e33",
    ),
    "checkpoint_5184_result": (
        source_path(
            "source-intake/functional_rg/5184/"
            "stationary_PX_background_results.json"
        ),
        "203549387a9c8f22721dfe8925c91aa2614a2adbcb3281f487cefb89d849e63b",
    ),
    "checkpoint_5187_canonical_parent": (
        source_path(
            "5187-Y5-R2FR-canonical-local-parent-action-Hessian-source-"
            "residue-and-scale-setting-theorem.md"
        ),
        "4556205ec12e11930a13d0ed9b5e27b6b4619f3752a5e10db2a4b767dcdec674",
    ),
    "checkpoint_5187_result": (
        source_path(
            "source-intake/functional_rg/5187/"
            "canonical_local_parent_action_results.json"
        ),
        "05d9e06edf88c219a6d21f49303b7e98dd82f3d1ecee5c9d445da385d4fa4e6d",
    ),
    "checkpoint_5188_coframe_parent": (
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
}

EXTERNAL_SOURCES = {
    "ADM_reprint": "https://arxiv.org/abs/gr-qc/0405109",
    "Einstein_aether_PPN": "https://arxiv.org/abs/gr-qc/0509083",
    "Einstein_aether_modes": "https://arxiv.org/abs/gr-qc/0402005",
    "Schwinger_Keldysh_EFT": "https://arxiv.org/abs/1511.03646",
}


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    files = sorted(candidate for candidate in path.rglob("*") if candidate.is_file())
    for item in files:
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


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def build_scalar_adm_projection() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    Pi, s1, s2, s3, P, PX = sp.symbols(
        "Pi s1 s2 s3 P P_X",
        real=True,
    )
    eta = sp.diag(-1, 1, 1, 1)
    n_up = sp.Matrix([1, 0, 0, 0])
    v_down = sp.Matrix([Pi, s1, s2, s3])
    v_up = eta * v_down
    stress = sp.simplify(2 * PX * v_down * v_down.T - P * eta)
    rho = sp.simplify((n_up.T * stress * n_up)[0])
    momentum = sp.Matrix(
        [sp.simplify(-stress[index, 0]) for index in range(1, 4)]
    )
    spatial_stress = stress[1:4, 1:4]
    s_squared = sp.expand(s1**2 + s2**2 + s3**2)
    pressure = sp.simplify(sp.trace(spatial_stress) / 3)
    anisotropic = sp.simplify(spatial_stress - pressure * sp.eye(3))
    anisotropic_trace = sp.simplify(sp.trace(anisotropic))
    X = sp.simplify((v_down.T * v_up)[0])
    current = sp.simplify(2 * PX * v_up)

    timelike_anisotropic = sp.simplify(
        anisotropic.subs({s1: 0, s2: 0, s3: 0})
    )
    spacelike_witness = sp.simplify(
        anisotropic.subs({Pi: 0, s1: 1, s2: 0, s3: 0, PX: 1})
    )

    h11, h22, h33, h12, h13, h23 = sp.symbols(
        "h11 h22 h33 h12 h13 h23"
    )
    spatial_metric = sp.Matrix(
        [
            [h11, h12, h13],
            [h12, h22, h23],
            [h13, h23, h33],
        ]
    )
    spatial_components = sp.Matrix(
        [
            spatial_metric[0, 0],
            spatial_metric[1, 1],
            spatial_metric[2, 2],
            spatial_metric[0, 1],
            spatial_metric[0, 2],
            spatial_metric[1, 2],
        ]
    )
    spatial_variables = (h11, h22, h33, h12, h13, h23)
    fixed_clock_spatial_rank = spatial_components.jacobian(
        spatial_variables
    ).rank()

    f = sp.symbols("f")
    dpsi = sp.symbols("p0:4")
    df = sp.symbols("f0:4")
    frobenius_components: list[sp.Expr] = []
    for a in range(4):
        for b in range(a + 1, 4):
            for c in range(b + 1, 4):
                component = (
                    f * dpsi[a] * (df[b] * dpsi[c] - df[c] * dpsi[b])
                    + f * dpsi[b] * (df[c] * dpsi[a] - df[a] * dpsi[c])
                    + f * dpsi[c] * (df[a] * dpsi[b] - df[b] * dpsi[a])
                )
                frobenius_components.append(sp.expand(component))
    frobenius_zero = all(value == 0 for value in frobenius_components)

    metrics = {
        "signature": "(-,+,+,+)",
        "gradient_decomposition": "nabla_mu psi=-Pi n_mu+s_mu",
        "X": str(X),
        "rho": str(rho),
        "momentum_density": [str(value) for value in momentum],
        "spatial_stress": [
            [str(spatial_stress[row, column]) for column in range(3)]
            for row in range(3)
        ],
        "isotropic_pressure": str(pressure),
        "anisotropic_stress": [
            [str(anisotropic[row, column]) for column in range(3)]
            for row in range(3)
        ],
        "anisotropic_trace": str(anisotropic_trace),
        "current": [str(value) for value in current],
        "timelike_anisotropic_zero": matrix_is_zero(timelike_anisotropic),
        "spacelike_anisotropic_nonzero": not matrix_is_zero(spacelike_witness),
        "fixed_clock_spatial_metric_rank": fixed_clock_spatial_rank,
        "frobenius_components": [str(value) for value in frobenius_components],
        "frobenius_zero": frobenius_zero,
        "conservation_identity": (
            "nabla_mu T^mu_nu=(nabla_mu J^mu-P_psi)nabla_nu psi"
        ),
    }

    rows = tagged(
        [
            {
                "projection_id": "ADM5189_00_gradient_split",
                "object": "motion gradient",
                "exact_formula": "nabla_mu psi=-Pi n_mu+s_mu; n.s=0",
                "derived_result": f"X={X}",
                "status": "EXACT_ADM_DECOMPOSITION",
                "implication": "timelike motion can define a clock congruence",
                "valid_for_local_statement": True,
            },
            {
                "projection_id": "ADM5189_01_energy",
                "object": "normal energy density",
                "exact_formula": "rho=n^mu n^nu T_mu_nu",
                "derived_result": str(rho),
                "status": "EXACT_IN_INHERITED_STRESS_CONVENTION",
                "implication": "homogeneous clock carries background energy",
                "valid_for_local_statement": True,
            },
            {
                "projection_id": "ADM5189_02_momentum",
                "object": "ADM momentum density",
                "exact_formula": "j_i=-h_i^mu n^nu T_mu_nu",
                "derived_result": str(list(momentum)),
                "status": "EXACT_IN_INHERITED_STRESS_CONVENTION",
                "implication": "j_i vanishes on a homogeneous timelike clock",
                "valid_for_local_statement": True,
            },
            {
                "projection_id": "ADM5189_03_spatial_stress",
                "object": "spatial stress",
                "exact_formula": "S_ij=h_i^mu h_j^nu T_mu_nu",
                "derived_result": "S_ij=2 P_X s_i s_j-P h_ij",
                "status": "EXACT",
                "implication": "a spatial gradient is intrinsically anisotropic",
                "valid_for_local_statement": True,
            },
            {
                "projection_id": "ADM5189_04_pressure",
                "object": "isotropic pressure",
                "exact_formula": "p_iso=S^i_i/3",
                "derived_result": str(pressure),
                "status": "EXACT",
                "implication": "timelike branch is perfect-fluid-like at one point",
                "valid_for_local_statement": True,
            },
            {
                "projection_id": "ADM5189_05_anisotropic",
                "object": "anisotropic stress",
                "exact_formula": "pi_ij=S_ij-p_iso h_ij",
                "derived_result": (
                    "pi_ij=2 P_X(s_i s_j-s^2 h_ij/3); trace=0"
                ),
                "status": "EXACT",
                "implication": (
                    "homogeneous timelike branch has pi_ij=0; spacelike branch does not"
                ),
                "valid_for_local_statement": True,
            },
            {
                "projection_id": "ADM5189_06_current",
                "object": "shift current",
                "exact_formula": "J^mu=2 P_X nabla^mu psi",
                "derived_result": str(list(current)),
                "status": "EXACT",
                "implication": "source-free P(X) obeys the inherited no-lump current theorem",
                "valid_for_local_statement": True,
            },
            {
                "projection_id": "ADM5189_07_conservation",
                "object": "stress conservation",
                "exact_formula": (
                    "nabla_mu T^mu_nu=(nabla_mu J^mu-P_psi)nabla_nu psi"
                ),
                "derived_result": "zero on the scalar Euler equation",
                "status": "EXACT_NOETHER_IDENTITY",
                "implication": "the scalar matter block is compatible with Bianchi",
                "valid_for_local_statement": True,
            },
        ]
    )
    return rows, metrics


def build_ancestry_rows(
    adm_metrics: dict[str, Any],
) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "ancestry_id": "ANC5189_00_scalar_clock",
                "candidate_parent_object": "timelike motion scalar gradient",
                "map": "u_mu=-nabla_mu psi/sqrt(-X), X<0",
                "rank_or_identity": "one normalized timelike direction",
                "verdict": "INHERITED_CLOCK_CONGRUENCE",
                "reason": "the current scalar action owns psi and its gradient",
                "what_it_does_not_own": "six-component h_ij or spatial coframe",
            },
            {
                "ancestry_id": "ANC5189_01_frobenius",
                "candidate_parent_object": "normalized scalar-gradient flow",
                "map": "u=f dpsi",
                "rank_or_identity": (
                    f"u wedge du=0; executed={adm_metrics['frobenius_zero']}"
                ),
                "verdict": "HYPERSURFACE_ORTHOGONAL_ONLY",
                "reason": "dpsi wedge df wedge dpsi vanishes identically",
                "what_it_does_not_own": "independent vortical spin-one flow",
            },
            {
                "ancestry_id": "ANC5189_02_spatial_ambiguity",
                "candidate_parent_object": "fixed unit clock u",
                "map": "g_mu_nu=-u_mu u_nu+h_mu_nu",
                "rank_or_identity": (
                    "fixed-u spatial family rank="
                    f"{adm_metrics['fixed_clock_spatial_metric_rank']}"
                ),
                "verdict": "CLOCK_DOES_NOT_DETERMINE_SPACE",
                "reason": "six independent positive spatial-metric directions remain",
                "what_it_does_not_own": "h_ij curvature, shear geometry, or triad orientation",
            },
            {
                "ancestry_id": "ANC5189_03_old_motion_load",
                "candidate_parent_object": "2048 spherical motion-load coframe",
                "map": (
                    "theta0=T c dt; theta1=sqrt(S)dr; theta2=r dtheta;"
                    " theta3=r sin(theta)dphi"
                ),
                "rank_or_identity": "special static spherical chart",
                "verdict": "SPECIAL_CONSTRUCTION_NOT_GENERAL_PARENT",
                "reason": (
                    "the independent radial function S and the law T^2 S=1 were not"
                    " derived from the old scalar"
                ),
                "what_it_does_not_own": "generic curved spatial coframe or parent field equation",
            },
            {
                "ancestry_id": "ANC5189_04_relational_coframe",
                "candidate_parent_object": "5188 e^a_mu=E^a_A partial_mu X^A",
                "map": "g=e^T eta e; H=sqrt(-g)g^-1",
                "rank_or_identity": "e->g rank 10; Lorentz nullity 6",
                "verdict": "MINIMAL_SURVIVING_GEOMETRIC_PARENT",
                "reason": "the map is exactly surjective on nondegenerate coframes",
                "what_it_does_not_own": "an old-scalar derivation of non-scalar E",
            },
            {
                "ancestry_id": "ANC5189_05_composite_space_projector",
                "candidate_parent_object": "h_mu_nu=g_mu_nu+u_mu u_nu",
                "map": "requires g before h can be formed",
                "rank_or_identity": "derived projector after geometry exists",
                "verdict": "READOUT_NOT_GEOMETRY_ORIGIN",
                "reason": "u plus an already existing metric defines a foliation",
                "what_it_does_not_own": "the metric it projects",
            },
            {
                "ancestry_id": "ANC5189_06_final",
                "candidate_parent_object": "old MTS motion/time/space ancestry",
                "map": "psi -> clock; e/E -> geometry; K_ij=(1/2)L_u h_ij",
                "rank_or_identity": "time-flow half inherited; spatial half independent",
                "verdict": "PARTIAL_ANCESTRY_EXACTLY_LOCATED",
                "reason": (
                    "motion can describe evolution of space once h exists but does not"
                    " create all spatial metric data"
                ),
                "what_it_does_not_own": "a scalar-only derivation of curved local GR",
            },
        ]
    )


def linearized_tt_weyl_metrics() -> dict[str, Any]:
    omega, wave_number, plus, cross = sp.symbols(
        "omega k gamma_plus gamma_cross",
        real=True,
    )
    eta = sp.diag(-1, 1, 1, 1)
    wave_covector = [-omega, 0, 0, wave_number]
    perturbation = sp.MutableDenseNDimArray.zeros(4, 4)
    perturbation[1, 1] = plus
    perturbation[2, 2] = -plus
    perturbation[1, 2] = cross
    perturbation[2, 1] = cross

    riemann = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    riemann[a, b, c, d] = sp.expand(
                        sp.Rational(1, 2)
                        * (
                            -wave_covector[c]
                            * wave_covector[b]
                            * perturbation[a, d]
                            - wave_covector[d]
                            * wave_covector[a]
                            * perturbation[b, c]
                            + wave_covector[d]
                            * wave_covector[b]
                            * perturbation[a, c]
                            + wave_covector[c]
                            * wave_covector[a]
                            * perturbation[b, d]
                        )
                    )

    ricci = sp.MutableDenseNDimArray.zeros(4, 4)
    for b in range(4):
        for d in range(4):
            ricci[b, d] = sp.expand(
                sum(
                    eta[a, c] * riemann[a, b, c, d]
                    for a in range(4)
                    for c in range(4)
                )
            )
    ricci_scalar = sp.expand(
        sum(
            eta[b, d] * ricci[b, d]
            for b in range(4)
            for d in range(4)
        )
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
                            eta[a, c] * ricci[d, b]
                            - eta[a, d] * ricci[c, b]
                            - eta[b, c] * ricci[d, a]
                            + eta[b, d] * ricci[c, a]
                        )
                        + ricci_scalar
                        * sp.Rational(1, 6)
                        * (
                            eta[a, c] * eta[d, b]
                            - eta[a, d] * eta[c, b]
                        )
                    )

    def contract_four(tensor: sp.MutableDenseNDimArray) -> sp.Expr:
        return sp.expand(
            sum(
                eta[a, a]
                * eta[b, b]
                * eta[c, c]
                * eta[d, d]
                * tensor[a, b, c, d] ** 2
                for a in range(4)
                for b in range(4)
                for c in range(4)
                for d in range(4)
            )
        )

    riemann_squared = contract_four(riemann)
    ricci_squared = sp.expand(
        sum(
            eta[a, a] * eta[b, b] * ricci[a, b] ** 2
            for a in range(4)
            for b in range(4)
        )
    )
    weyl_squared = contract_four(weyl)
    expected = sp.expand(
        (plus**2 + cross**2) * (omega**2 - wave_number**2) ** 2
    )
    identity_residual = sp.simplify(
        weyl_squared
        - (
            riemann_squared
            - 2 * ricci_squared
            + ricci_scalar**2 / 3
        )
    )
    return {
        "ricci_scalar": str(sp.factor(ricci_scalar)),
        "riemann_squared": str(sp.factor(riemann_squared)),
        "ricci_squared": str(sp.factor(ricci_squared)),
        "weyl_squared": str(sp.factor(weyl_squared)),
        "expected_weyl_squared": str(sp.factor(expected)),
        "weyl_squared_exact": sp.simplify(weyl_squared - expected) == 0,
        "weyl_identity_residual": str(identity_residual),
        "weyl_identity_exact": identity_residual == 0,
    }


def build_tt_and_irrep_rows() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    epsilon, scale, gamma1, gamma2, lapse, psi_dot = sp.symbols(
        "epsilon a gamma1 gamma2 N psi_dot",
        nonzero=True,
        real=True,
    )
    h_tt = scale**2 * sp.diag(
        sp.exp(epsilon * gamma1),
        sp.exp(epsilon * gamma2),
        sp.exp(-epsilon * (gamma1 + gamma2)),
    )
    det_h = sp.simplify(h_tt.det())
    X_homogeneous = sp.simplify(-psi_dot**2 / lapse**2)
    P_background = sp.symbols("P_background")
    px_density = sp.simplify(lapse * sp.sqrt(det_h) * P_background)
    px_tt_first = sp.simplify(sp.diff(px_density, epsilon))
    px_tt_second = sp.simplify(sp.diff(px_density, epsilon, 2))

    weyl_metrics = linearized_tt_weyl_metrics()
    q2, M2, cO4, X = sp.symbols("q2 M_R2 c_O4 X", nonzero=True)
    total_kernel = sp.factor(q2 * (M2 / 4 + cO4 * X * q2))
    extra_pole = sp.solve(sp.Eq(M2 / 4 + cO4 * X * q2, 0), q2)[0]
    massless_residue_factor = sp.simplify(
        sp.diff(total_kernel, q2).subs(q2, 0)
    )

    metrics = {
        "TT_spatial_determinant": str(det_h),
        "TT_determinant_exact": sp.simplify(det_h - scale**6) == 0,
        "homogeneous_X": str(X_homogeneous),
        "PX_TT_first_variation": str(px_tt_first),
        "PX_TT_second_variation": str(px_tt_second),
        "PX_TT_Hessian_zero": px_tt_second == 0,
        **weyl_metrics,
        "signed_O4_convention": (
            "c_O4 is the coefficient multiplying +sqrt(-g) C^2 X;"
            " c_O4=+u_O4 in 4935 and c_O4=-u_O4 in the 5187 display"
        ),
        "TT_total_principal_kernel": str(total_kernel),
        "massless_pole": "q2=omega^2-k^2=0",
        "massless_residue_factor": str(massless_residue_factor),
        "extra_pole_q2": str(extra_pole),
        "EFT_smallness": "epsilon_O4=abs(4 c_O4 X q2/M_R^2)<<1",
        "local_zero_background_exact": True,
        "cosmological_clock_O4_exactly_zero": False,
    }

    o4_rows = tagged(
        [
            {
                "gate_id": "O4TT5189_00_background",
                "object": "FLRW background Weyl",
                "calculation": "Cbar_abcd=0",
                "result": "background Cbar^2 X and first metric variation vanish",
                "status": "BACKGROUND_AND_LINEAR_SILENCE",
                "consequence": "this alone does not determine the Hessian",
            },
            {
                "gate_id": "O4TT5189_01_quadratic",
                "object": "TT Weyl Hessian",
                "calculation": (
                    "gamma_xx=gamma_plus; gamma_yy=-gamma_plus;"
                    " gamma_xy=gamma_cross; wave=(omega,0,0,k)"
                ),
                "result": (
                    "C1_abcd C1^abcd=(gamma_plus^2+gamma_cross^2)"
                    "(omega^2-k^2)^2"
                ),
                "status": "EXACT_NONZERO_OFF_SHELL",
                "consequence": (
                    "zero background Weyl cannot be used to delete the O4 TT Hessian"
                ),
            },
            {
                "gate_id": "O4TT5189_02_kernel",
                "object": "EH plus signed O4 TT principal kernel",
                "calculation": "q2=omega^2-k^2",
                "result": str(total_kernel),
                "status": "EXACT_FLAT_PRINCIPAL_SYMBOL",
                "consequence": "the GR massless pole remains a factor",
            },
            {
                "gate_id": "O4TT5189_03_massless",
                "object": "massless tensor pole",
                "calculation": "K_TT(q2=0)=0; derivative at zero",
                "result": f"residue factor={massless_residue_factor}",
                "status": "GR_POLE_AND_LOW_ENERGY_SPEED_RETAINED",
                "consequence": "c_T=1 at the massless principal root",
            },
            {
                "gate_id": "O4TT5189_04_extra_pole",
                "object": "nonperturbative higher-derivative pole",
                "calculation": "M_R^2/4+c_O4 X q2=0",
                "result": f"q2={extra_pole}",
                "status": "EXTRA_POLE_IF_cO4_X_NONZERO",
                "consequence": (
                    "an exact two-mode cosmological parent needs degeneracy/cancellation;"
                    " an EFT treatment needs this pole above cutoff"
                ),
            },
            {
                "gate_id": "O4TT5189_05_local",
                "object": "local psi=0 branch",
                "calculation": "Xbar=0 and nabla psi_bar=0",
                "result": "O4 pure-metric and mixed quadratic Hessians vanish",
                "status": "EXACT_LOCAL_TENSOR_PROTECTION",
                "consequence": "local vacuum gravity retains the 5188 two tensor modes",
            },
            {
                "gate_id": "O4TT5189_06_cosmology",
                "object": "homogeneous cosmological clock",
                "calculation": "Xbar=-Pi^2 generally nonzero",
                "result": "O4 TT Hessian is nonzero off shell",
                "status": "EFT_BOUND_OR_DEGENERACY_THEOREM_REQUIRED",
                "consequence": (
                    "do not claim an exact two-mode cosmological tensor sector yet"
                ),
            },
            {
                "gate_id": "O4TT5189_07_EFT",
                "object": "resolved low-energy corridor",
                "calculation": "epsilon_O4(q)=abs(4 c_O4 X q2/M_R^2)",
                "result": "require epsilon_O4<<1 throughout the claimed band",
                "status": "DERIVED_DIMENSIONLESS_CONTROL_PARAMETER",
                "consequence": (
                    "order reduction then retains the massless mode without resolving"
                    " the higher-derivative pole"
                ),
            },
            {
                "gate_id": "O4TT5189_08_sign_alias",
                "object": "O4 coefficient convention",
                "calculation": (
                    "4935 displays +u_O4 C^2 X; 5187 displays -u_O4 C^2 X"
                ),
                "result": "use signed c_O4 in all physical pole/bound formulas",
                "status": "ALIAS_CANONICALIZED",
                "consequence": "no sign conclusion is imported from a symbol alias",
            },
        ]
    )

    irrep_rows = tagged(
        [
            {
                "branch_id": "IRR5189_00_local_zero",
                "background": "psi_bar=0; Xbar=0; unoccupied local branch",
                "scalar_sector": "renormalized Z_psi(-Box+m_gap^2)",
                "vector_sector": "no scalar-gradient vector irrep",
                "tensor_sector": "EH/Fierz-Pauli only at quadratic order",
                "mixed_metric_scalar": "zero by field degree/reflection-even branch",
                "status": "EXACT_QUADRATIC_BLOCK_DIAGONAL",
            },
            {
                "branch_id": "IRR5189_01_timelike_PX",
                "background": "s_i=0; Pi nonzero; homogeneous clock",
                "scalar_sector": "dynamic P_X/P_XX sound and background stress",
                "vector_sector": "j_i=0 at one point",
                "tensor_sector": "pure P(X) TT Hessian exactly zero",
                "mixed_metric_scalar": "proportional to frequency; static limit zero",
                "status": "PX_TENSOR_SAFE_O4_SEPARATE",
            },
            {
                "branch_id": "IRR5189_02_timelike_O4",
                "background": "Cbar=0; Xbar=-Pi^2 nonzero",
                "scalar_sector": "O4 scalar Hessian background-silent when Cbar=0",
                "vector_sector": "not selected here",
                "tensor_sector": "c_O4 Xbar (omega^2-k^2)^2",
                "mixed_metric_scalar": "linear Cbar factor makes first mixed term zero",
                "status": "TT_HIGHER_DERIVATIVE_HESSIAN_NONZERO",
            },
            {
                "branch_id": "IRR5189_03_spacelike",
                "background": "Pi=0; s_i nonzero",
                "scalar_sector": "anisotropic principal cone",
                "vector_sector": "preferred spatial direction",
                "tensor_sector": "anisotropic stress can project into TT",
                "mixed_metric_scalar": "static k^0 Schur response",
                "status": "NONLOCALIZED_NO_LUMP_BRANCH_REJECTED",
            },
            {
                "branch_id": "IRR5189_04_occupied_isotropic",
                "background": "one-point isotropic; connected two-point state nonzero",
                "scalar_sector": "retarded stress susceptibility may be nonlocal",
                "vector_sector": "Poynting/momentum flux enters T0i",
                "tensor_sector": "must independently satisfy Pi_TT Sigma Pi_TT bound",
                "mixed_metric_scalar": "candidate common-mode Schur response",
                "status": "CONSTRUCTIVE_ROUTE_TARGET_NOT_DERIVED",
            },
        ]
    )
    return o4_rows, irrep_rows, metrics


def build_unit_flow_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    p, d, ratio, epsilon = sp.symbols(
        "p d r epsilon",
        positive=True,
    )
    c1 = sp.simplify((p + d) / 2)
    c3 = sp.simplify((p - d) / 2)
    c4 = sp.simplify(-(p - d) ** 2 / (2 * (p + d)))
    c2 = sp.simplify(-p * (3 * d + p) / (3 * (d + p)))
    c13 = sp.simplify(c1 + c3)
    c14 = sp.simplify(c1 + c4)
    c123 = sp.simplify(c1 + c2 + c3)
    ctheta = sp.simplify(c13 + 3 * c2)
    ppn_c4_residual = sp.simplify(c4 + c3**2 / c1)
    ppn_c2_residual = sp.simplify(
        c2 - (-2 * c1**2 - c1 * c3 + c3**2) / (3 * c1)
    )
    cosmology_newton_residual = sp.simplify(ctheta + c14)

    qS = sp.simplify(3 * (1 - p) * (d + p - d * p) / p**2)
    qV = sp.simplify(2 * d * p / (d + p))
    qT = sp.simplify(1 - p)
    speedS2 = sp.simplify(p / (3 * d * (1 - p)))
    speedV2 = sp.simplify(
        (d + p) * (d + p - d * p) / (4 * d * p * (1 - p))
    )
    speedT2 = sp.simplify(1 / (1 - p))
    endpoint = {
        "c1_over_epsilon": sp.simplify(
            (c1 / epsilon).subs({p: epsilon, d: ratio * epsilon})
        ),
        "c2_over_epsilon": sp.simplify(
            (c2 / epsilon).subs({p: epsilon, d: ratio * epsilon})
        ),
        "c3_over_epsilon": sp.simplify(
            (c3 / epsilon).subs({p: epsilon, d: ratio * epsilon})
        ),
        "c4_over_epsilon": sp.simplify(
            (c4 / epsilon).subs({p: epsilon, d: ratio * epsilon})
        ),
        "c14_over_epsilon": sp.simplify(
            (c14 / epsilon).subs({p: epsilon, d: ratio * epsilon})
        ),
        "c123_over_epsilon": sp.simplify(
            (c123 / epsilon).subs({p: epsilon, d: ratio * epsilon})
        ),
        "qS_scaled": sp.simplify(
            (epsilon * qS).subs({p: epsilon, d: ratio * epsilon})
        ),
    }
    endpoint_limits = {
        key: str(sp.simplify(sp.limit(value, epsilon, 0, dir="+")))
        for key, value in endpoint.items()
    }

    metrics = {
        "c1": str(c1),
        "c2": str(c2),
        "c3": str(c3),
        "c4": str(c4),
        "c13": str(c13),
        "c14": str(c14),
        "c123": str(c123),
        "c_theta": str(ctheta),
        "PPN_c4_residual": str(ppn_c4_residual),
        "PPN_c2_residual": str(ppn_c2_residual),
        "Gcos_GN_denominator_residual": str(cosmology_newton_residual),
        "qS": str(qS),
        "qV": str(qV),
        "qT": str(qT),
        "speedS2": str(speedS2),
        "speedV2": str(speedV2),
        "speedT2": str(speedT2),
        "endpoint_limits": endpoint_limits,
        "exact_zero_endpoint_chart_singular": True,
    }

    rows = tagged(
        [
            {
                "flow_id": "UF5189_00_gradient",
                "flow_object": "u_mu proportional to nabla_mu psi",
                "field_status": "composite scalar-gradient clock",
                "mode_content": "no independent vector mode; Frobenius vorticity zero",
                "local_GR_compatibility": "compatible when used only as readout",
                "verdict": "PRIMITIVE_CLOCK_ONLY",
            },
            {
                "flow_id": "UF5189_01_landau",
                "flow_object": "Landau eigenvector of connected state stress/covariance",
                "field_status": "composite diagnostic if not independently varied",
                "mode_content": "adds zero independent local field modes",
                "local_GR_compatibility": "compatible with metric-only local quotient",
                "verdict": "STATE_READOUT_ALLOWED",
            },
            {
                "flow_id": "UF5189_02_aether",
                "flow_object": "independently varied unit timelike vector",
                "field_status": "four-operator correspondence EFT",
                "mode_content": "2 tensor + 2 vector + 1 scalar gravitational/aether modes",
                "local_GR_compatibility": (
                    "not the exact two-mode local parent while u remains in field space"
                ),
                "verdict": "CORRESPONDENCE_EXTENSION_ONLY",
            },
            {
                "flow_id": "UF5189_03_PPN_surface",
                "flow_object": "p=c13; d=c1-c3",
                "field_status": (
                    "c4=-c3^2/c1; "
                    "c2=(-2c1^2-c1c3+c3^2)/(3c1)"
                ),
                "mode_content": f"qT={qT}; qV={qV}; qS={qS}",
                "local_GR_compatibility": (
                    "finite 0<p<=1e-15, 0<d<=p/3 is approximate safe corridor"
                ),
                "verdict": "EXACT_PPN_SAFE_SURFACE_REPRODUCED",
            },
            {
                "flow_id": "UF5189_04_calibration",
                "flow_object": "Newton/cosmology gravitational constants",
                "field_status": f"c_theta={ctheta}; c14={c14}",
                "mode_content": "c_theta=-c14",
                "local_GR_compatibility": "G_cos=G_N on the PPN-safe surface",
                "verdict": "EXACT_DENOMINATOR_LOCK",
            },
            {
                "flow_id": "UF5189_05_endpoint",
                "flow_object": "p->0 with d=r p",
                "field_status": (
                    "all c_i vanish linearly but c14,c123 vanish and scalar/vector"
                    " canonical chart is nonuniform"
                ),
                "mode_content": (
                    "qS diverges as 1/p in this variable chart while qV->0;"
                    " speed formulae are endpoint-indeterminate"
                ),
                "local_GR_compatibility": (
                    "exact GR requires removing u from field space, not coefficient zero"
                ),
                "verdict": "SINGULAR_ENDPOINT_NOT_GR_PROOF",
            },
        ]
    )
    return rows, metrics


def build_constraint_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    lapse, sqrt_h, Pi, PX, PXX = sp.symbols(
        "N sqrt_h Pi P_X P_XX",
        nonzero=True,
        real=True,
    )
    scalar_velocity_hessian = sp.simplify(
        -2 * sqrt_h * (PX - 2 * Pi**2 * PXX) / lapse
    )
    velocity_hessian = sp.diag(
        0,
        0,
        0,
        0,
        scalar_velocity_hessian,
    )
    lapse_shift_velocity_block = velocity_hessian[:4, :4]
    pure_metric_configuration_dof = (12 - 2 * 4) // 2
    metric_scalar_configuration_dof = (14 - 2 * 4) // 2
    metrics = {
        "velocity_order": [
            "dot_N",
            "dot_N1",
            "dot_N2",
            "dot_N3",
            "dot_psi",
        ],
        "PX_matter_velocity_Hessian": [
            [str(velocity_hessian[row, column]) for column in range(5)]
            for row in range(5)
        ],
        "lapse_shift_velocity_block_zero": matrix_is_zero(
            lapse_shift_velocity_block
        ),
        "regular_scalar_velocity_rank": velocity_hessian.rank(),
        "scalar_velocity_Hessian": str(scalar_velocity_hessian),
        "scalar_regularity_condition": "P_X-2 Pi^2 P_XX != 0",
        "pure_metric_reduced_phase_dimension": 12 - 2 * 4,
        "pure_metric_configuration_dof": pure_metric_configuration_dof,
        "metric_plus_PX_reduced_phase_dimension": 14 - 2 * 4,
        "metric_plus_PX_configuration_dof": metric_scalar_configuration_dof,
        "local_resolved_gravity_dof_below_gap": 2,
        "independent_aether_gravity_configuration_dof": 5,
        "O4_nonperturbative_extra_TT_pole_when_X_nonzero": True,
    }
    rows = tagged(
        [
            {
                "count_id": "CNT5189_00_EH",
                "action_branch": "Einstein-Hilbert coframe/metric",
                "velocity_statement": "no dot(N) or dot(N^i)",
                "constraint_statement": "one Hamiltonian plus three momentum first class",
                "configuration_dof": pure_metric_configuration_dof,
                "interpretation": "two tensor modes",
                "status": "EXACT_ADM_COUNT",
            },
            {
                "count_id": "CNT5189_01_EH_PX",
                "action_branch": "EH plus regular first-derivative P(X,psi)",
                "velocity_statement": (
                    "H_vel=diag(0,0,0,0,"
                    "-2 sqrt(h)(P_X-2 Pi^2 P_XX)/N)"
                ),
                "constraint_statement": "Diff constraints remain first class",
                "configuration_dof": metric_scalar_configuration_dof,
                "interpretation": "two tensor plus one physical scalar",
                "status": "EXACT_REGULAR_BRANCH_COUNT",
            },
            {
                "count_id": "CNT5189_02_local_IR",
                "action_branch": "psi=0 unoccupied local branch below m_gap",
                "velocity_statement": "scalar pole is unresolved/decoupled in the IR band",
                "constraint_statement": "metric quadratic block is the 5188 ADM block",
                "configuration_dof": 2,
                "interpretation": (
                    "two resolved gravitational modes; scalar still exists above its gap"
                ),
                "status": "EXACT_QUADRATIC_LOCAL_PROTECTION_NOT_FIELD_REMOVAL",
            },
            {
                "count_id": "CNT5189_03_O4_local",
                "action_branch": "c_O4 C^2 X at Xbar=0",
                "velocity_statement": "pure metric O4 Hessian vanishes",
                "constraint_statement": "no new quadratic local metric pole",
                "configuration_dof": 2,
                "interpretation": "local vacuum tensor count unchanged",
                "status": "EXACT_AT_SELECTED_BACKGROUND",
            },
            {
                "count_id": "CNT5189_04_O4_clock",
                "action_branch": "c_O4 C^2 X at homogeneous Xbar nonzero",
                "velocity_statement": "fourth-order TT principal kernel appears",
                "constraint_statement": (
                    "Diff remains but higher derivatives enlarge the nonperturbative"
                    " phase space"
                ),
                "configuration_dof": "2 low-energy tensors plus an extra TT pole if resolved",
                "interpretation": "order-reduced EFT or degeneracy theorem required",
                "status": "EXACT_TWO_MODE_COSMOLOGY_NOT_YET_PROVED",
            },
            {
                "count_id": "CNT5189_05_unit_flow",
                "action_branch": "independent Einstein-aether/unit-flow field",
                "velocity_statement": "independent vector kinetic operators",
                "constraint_statement": "unit constraint does not remove spin-1/spin-0 modes",
                "configuration_dof": 5,
                "interpretation": "2 tensor +2 vector +1 scalar before any separate psi",
                "status": "CORRESPONDENCE_NOT_PRIMITIVE_LOCAL_PARENT",
            },
            {
                "count_id": "CNT5189_06_composite_flow",
                "action_branch": "Landau/state flow used only as composite readout",
                "velocity_statement": "u is not independently varied",
                "constraint_statement": "no additional canonical pair",
                "configuration_dof": "unchanged",
                "interpretation": "compatible with metric-only local quotient",
                "status": "MODE_SAFE_BY_FIELD_ABSENCE",
            },
        ]
    )
    return rows, metrics


def build_response_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    y, amplitude = sp.symbols("y A", positive=True)
    q = sp.Rational(77, 100)
    support = sp.simplify(y ** (1 + q) / (1 + y**q))
    schur_fraction = sp.simplify(amplitude * support / (1 + amplitude * support))
    support_derivative = sp.factor(sp.diff(support, y))
    support_small_y = sp.limit(support / y ** (1 + q), y, 0, dir="+")
    support_large_y = sp.limit(support / y, y, sp.oo)
    fraction_small_y = sp.limit(schur_fraction, y, 0, dir="+")
    fraction_large_y = sp.limit(schur_fraction, y, sp.oo)
    effective_ratio = sp.simplify(1 - schur_fraction)

    locked_amplitude = 9.32299014212954
    sample_values: list[float] = []
    effective_values: list[float] = []
    for index in range(321):
        log_y = -12.0 + 24.0 * index / 320.0
        y_value = 10.0**log_y
        support_value = y_value ** (1.0 + 0.77) / (
            1.0 + y_value**0.77
        )
        fraction_value = locked_amplitude * support_value / (
            1.0 + locked_amplitude * support_value
        )
        sample_values.append(fraction_value)
        effective_values.append(1.0 - fraction_value)

    metrics = {
        "q": str(q),
        "support": str(support),
        "support_derivative": str(support_derivative),
        "support_small_y_coefficient": str(support_small_y),
        "support_large_y_coefficient": str(support_large_y),
        "schur_fraction": str(schur_fraction),
        "schur_fraction_small_y": str(fraction_small_y),
        "schur_fraction_large_y": str(fraction_large_y),
        "effective_kernel_ratio": str(effective_ratio),
        "sample_count": len(sample_values),
        "sample_fraction_minimum": min(sample_values),
        "sample_fraction_maximum": max(sample_values),
        "sample_effective_ratio_minimum": min(effective_values),
        "sample_effective_ratio_maximum": max(effective_values),
        "static_positive_for_A_positive": (
            min(sample_values) > 0
            and max(sample_values) < 1
            and min(effective_values) > 0
        ),
        "no_slip_condition": "Sigma_cs=Sigma_sc=0 with invertible slip block",
        "tensor_condition": "Pi_TT Sigma Pi_TT=0 or explicitly bounded",
        "gapped_vacuum_no_go": (
            "after local EH-residue matching a local gapped vacuum polarization"
            " is analytic in k^2 near k=0, whereas the target has"
            " K_eff/K_GR~|k|/(A mu) and an absolute |k|^3 term"
        ),
    }

    rows = tagged(
        [
            {
                "target_id": "RSP5189_00_basis",
                "object": "static scalar metric basis",
                "formula": "c=(Phi+Psi)/sqrt(2); s=(Phi-Psi)/sqrt(2)",
                "derived_condition": "ordinary no-anisotropic-stress source has J_s=0",
                "status": "EXACT_BASIS",
                "missing_parent_input": "",
            },
            {
                "target_id": "RSP5189_01_Schur",
                "object": "integrated motion-state susceptibility",
                "formula": "K_eff=K_GR-Sigma; Sigma=B K_chi^-1 B_dagger",
                "derived_condition": "Sigma is positive semidefinite in Euclidean static sector if K_chi>0",
                "status": "EXACT_SCHUR_SIGN_CONDITION",
                "missing_parent_input": "actual causal CTP B and K_chi",
            },
            {
                "target_id": "RSP5189_02_common",
                "object": "required common scalar channel",
                "formula": "Sigma_cc/K_GR,cc=A C_q/(1+A C_q)",
                "derived_condition": "K_eff,cc/K_GR,cc=1/(1+A C_q)>0 for A>=0",
                "status": "EXACT_TARGET_AND_STATIC_STABILITY",
                "missing_parent_input": "parent spectral density and amplitude law",
            },
            {
                "target_id": "RSP5189_03_support",
                "object": "spectral support shape",
                "formula": "C_q=y^(1+q)/(1+y^q); y=mu/|k|; q=0.77",
                "derived_condition": (
                    "dC/dy=y^q[(1+q)+y^q]/(1+y^q)^2>0"
                ),
                "status": "EXACT_MONOTONE_POSITIVE_SHAPE",
                "missing_parent_input": "derivation of q and mu from one state preparation law",
            },
            {
                "target_id": "RSP5189_04_limits",
                "object": "local and infrared limits",
                "formula": "C_q~(mu/|k|)^(1+q) at high k; C_q~mu/|k| at low k",
                "derived_condition": "Sigma/K_GR->0 locally and ->1 in the deep infrared",
                "status": "EXACT_ASYMPTOTICS",
                "missing_parent_input": "arena-independent scale-setting law",
            },
            {
                "target_id": "RSP5189_05_slip",
                "object": "PPN/lensing slip protection",
                "formula": (
                    "K_eff=[[Kc-Scc,-Scs],[-Scs,Ks-Sss]]; J=(Jc,0)"
                ),
                "derived_condition": "s=0 for arbitrary Jc iff Scs=0 with invertible slip block",
                "status": "EXACT_NO_SLIP_PROJECTOR_GATE",
                "missing_parent_input": "CTP proof that Sigma_cs=0",
            },
            {
                "target_id": "RSP5189_06_tensor",
                "object": "tensor protection",
                "formula": "Pi_TT Sigma Pi_TT",
                "derived_condition": "zero for exact GR tensors, or bounded in the claimed frequency band",
                "status": "INDEPENDENT_PROJECTOR_GATE",
                "missing_parent_input": "TT state susceptibility or symmetry zero",
            },
            {
                "target_id": "RSP5189_07_Ward",
                "object": "diffeomorphism Ward identity",
                "formula": "k_mu Sigma^mu_nu,rho_sigma=0 after contact terms",
                "derived_condition": "Hamiltonian/momentum constraints are not replaced by a fitted scalar kernel",
                "status": "REQUIRED_CTP_CONSERVATION_GATE",
                "missing_parent_input": "conserving 2PI/CTP approximation",
            },
            {
                "target_id": "RSP5189_08_gapped_no_go",
                "object": "local gapped vacuum polarization",
                "formula": "Sigma_vac/K_GR=a0+a2 k^2/m_gap^2+...",
                "derived_condition": (
                    "after matching a0 into M_R, it cannot generate |k| or fractional"
                    " powers required by C_q"
                ),
                "status": "REJECTED_AS_ORIGIN_OF_GALAXY_KERNEL",
                "missing_parent_input": "",
            },
            {
                "target_id": "RSP5189_09_required_state",
                "object": "viable origin of nonanalytic response",
                "formula": "gapless continuum or occupied-state retarded stress spectral density",
                "derived_condition": "must reproduce common channel while passing Ward, slip, TT and positivity gates",
                "status": "UNIQUE_NEXT_CONSTRUCTIVE_TARGET_CLASS",
                "missing_parent_input": "rho_TT/rho_cc spectral calculation and mu law",
            },
            {
                "target_id": "RSP5189_10_Poynting",
                "object": "electromagnetic Poynting flux",
                "formula": "T_EM^0i=(E cross B)^i",
                "derived_condition": (
                    "enters the universal vector/momentum source; it does not by itself"
                    " generate a stationary common scalar susceptibility"
                ),
                "status": "SAME_COFRAME_SOURCE_NOT_SEPARATE_FIELD",
                "missing_parent_input": "time-dependent CTP transfer if proposed",
            },
        ]
    )
    return rows, metrics


def build_branch_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "arena_id": "BR5189_00_local_vacuum",
                "arena": "local vacuum/compact exterior",
                "state": "psi=0; X=0; no scalar charge",
                "two_derivative_result": "EH plus gapped block-diagonal scalar",
                "higher_derivative_result": "O4 pure metric Hessian exactly zero",
                "mode_result": "two resolved gravity tensors below m_gap",
                "claim_status": "LEADING_LOCAL_GR_PROTECTED_INSIDE_PARENT",
                "next_requirement": "retain existing PPN/operator bounds; no new retuning",
            },
            {
                "arena_id": "BR5189_01_FLRW",
                "arena": "homogeneous cosmology",
                "state": "Pi nonzero; s_i=0",
                "two_derivative_result": "P(X) changes background/scalar constraints but not pure TT Hessian",
                "higher_derivative_result": "c_O4 X produces a q^4 TT Hessian",
                "mode_result": "massless GR pole plus possible resolved higher-derivative pole",
                "claim_status": "COSMOLOGY_TENSOR_GATE_OPEN",
                "next_requirement": "derive c_O4 X suppression or a degenerate completion",
            },
            {
                "arena_id": "BR5189_02_classical_galaxy",
                "arena": "stationary classical galaxy",
                "state": "attempted localized P(X) scalar profile",
                "two_derivative_result": "no-lump current theorem forces trivial regular profile",
                "higher_derivative_result": "spacelike escape is anisotropic and nonlocalized",
                "mode_result": "classical background route rejected in certified chart",
                "claim_status": "REJECTED_ROUTE",
                "next_requirement": "do not revive by retuning P_X or boundary flux",
            },
            {
                "arena_id": "BR5189_03_occupied_galaxy",
                "arena": "galaxy occupied motion state",
                "state": "isotropic one-point stress; nonzero connected two-point response",
                "two_derivative_result": "candidate Schur susceptibility can weaken common scalar kernel",
                "higher_derivative_result": "TT and slip projectors must remain silent/bounded",
                "mode_result": "state response, not a new classical background field",
                "claim_status": "PROMISING_INTERFACE_NOT_DERIVED",
                "next_requirement": "derive retarded spectral density, collision/state law and mu scaling",
            },
            {
                "arena_id": "BR5189_04_unit_flow",
                "arena": "preferred-flow correspondence tests",
                "state": "independently varied u only if microscopic Kubo response is nonzero",
                "two_derivative_result": "4857 PPN-safe finite corridor remains valid",
                "higher_derivative_result": "not part of primitive metric-only local branch",
                "mode_result": "adds spin-1/spin-0 modes when independent",
                "claim_status": "CORRESPONDENCE_BACKSTOP",
                "next_requirement": "promote only from a nonzero microscopic Kubo derivation",
            },
            {
                "arena_id": "BR5189_05_no_retuning",
                "arena": "cross-arena parent rule",
                "state": "one action; arena differences are states/boundaries, not new couplings",
                "two_derivative_result": "M_R,Z_A,Z_psi,m_gap,c_O4 fixed once",
                "higher_derivative_result": "same Wilson coefficients in every arena",
                "mode_result": "state occupation may vary only by a derived preparation law",
                "claim_status": "REQUIRED_DISCIPLINE",
                "next_requirement": "no per-galaxy or per-cosmology coefficient refits",
            },
        ]
    )


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
                "role": "parent ancestry, Hessian, branch or prior theorem",
            }
        )
    for source_id, url in EXTERNAL_SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "primary_external_reference",
                "source_path_or_url": url,
                "sha256": "",
                "expected_sha256": "",
                "hash_match": "",
                "role": "standard ADM, unit-flow mode or CTP formalism reference",
            }
        )
    return tagged(rows)


def build_document(result: dict[str, Any]) -> None:
    adm = result["ADM_projection"]
    tt = result["tensor_projection"]
    constraints = result["constraint_count"]
    response = result["occupied_state_target"]
    unit_flow = result["unit_flow"]
    text = f"""# 5189 — Motion-sector ADM projection, clock-only ancestry, and local tensor protection

Marker: `{MARKER}`

**Verdict:** This checkpoint makes a forward structural decision. The
surviving MTS motion scalar maps exactly into the coframe parent as a clock
and matter degree of freedom. It does **not** generate the spatial coframe.
The local `psi=0` branch protects the two GR tensor modes exactly at
quadratic order. A homogeneous cosmological clock is safe in the minimal
`P(X)` block, but the retained `C^2 X` operator is not automatically silent:
its background and first variation vanish on FLRW while its tensor Hessian
does not. The galaxy response therefore remains an occupied-state
susceptibility problem, not a classical scalar-profile problem.

No GitHub action and no edit to `formalization-workbench` occurred.

## 1. Parent and convention

```text
{PARENT_ACTION}
```

Signature is `(-,+,+,+)`. The signed coefficient `c_O4` is used because
checkpoint 4935 displayed `+u_O4 C^2 X`, whereas the assembled 5187 action
displayed `-u_O4 C^2 X`. Thus `c_O4=+u_O4` in the former notation and
`c_O4=-u_O4` in the latter. No physical sign is inferred from the alias.

## 2. Exact scalar-to-ADM map

Let `n^mu n_mu=-1`,

```text
nabla_mu psi=-Pi n_mu+s_mu,    n.s=0,
X=-Pi^2+s^2.
```

For the inherited convention

```text
J^mu=2 P_X nabla^mu psi,
T^mu_nu=2 P_X nabla^mu psi nabla_nu psi-delta^mu_nu P,
```

the exact projections are

```text
rho=2 P_X Pi^2+P,
j_i=-2 P_X Pi s_i,
S_ij=2 P_X s_i s_j-P h_ij,
p_iso=(2/3)P_X s^2-P,
pi_ij=2 P_X(s_i s_j-s^2 h_ij/3).
```

The executed anisotropic-stress trace is `{adm['anisotropic_trace']}`.
For `s_i=0`, `j_i=pi_ij=0`; a nonzero spatial gradient is anisotropic.
The exact identity

```text
nabla_mu T^mu_nu=(nabla_mu J^mu-P_psi)nabla_nu psi
```

then closes stress conservation on the scalar Euler equation.

## 3. What motion inherits — and what it cannot

If `X<0`,

```text
u_mu=-nabla_mu psi/sqrt(-X).
```

Since `u=f dpsi`, `u wedge du=0` identically. This is a
hypersurface-orthogonal clock congruence, not an independently vortical
spin-one field. Fixing that clock still leaves
`{adm['fixed_clock_spatial_metric_rank']}` independent spatial-metric
directions. Therefore

```text
old scalar motion -> clock/time-flow;
non-scalar E/e     -> spatial geometry;
K_ij=(1/2)L_u h_ij -> motion of already existing space.
```

The 2048 spherical coframe remains useful, but it supplied a separate radial
function `S(r)` and never derived the decisive `T^2 S=1` law. It is a special
construction, not a general scalar origin of the three spatial legs.

## 4. Constraint and mode count

Minimal `P(X,psi)` contains no `dot(N)` or `dot(N^i)`. Diffeomorphism
invariance retains one Hamiltonian and three momentum first-class
constraints. In velocity order
`(dot(N),dot(N^1),dot(N^2),dot(N^3),dot(psi))`, its matter Hessian is

```text
diag(0,0,0,0,
     -2 sqrt(h)[P_X-2 Pi^2 P_XX]/N).
```

The first four null directions are exact; the scalar direction is regular
when `P_X-2 Pi^2 P_XX != 0`. Thus

```text
metric only:       (12-2*4)/2 = {constraints['pure_metric_configuration_dof']};
metric plus scalar:(14-2*4)/2 = {constraints['metric_plus_PX_configuration_dof']}.
```

The full regular two-derivative parent has two tensors plus one scalar. On
the unoccupied local branch below `m_gap`, the scalar pole is unresolved and
the **resolved gravity sector** has two modes. This is decoupling, not a
claim that the scalar was removed from the full field space.

An independently varied unit-flow/aether field instead carries two tensor,
two vector and one scalar gravitational/aether modes. Its finite PPN-safe
corridor remains a correspondence test layer. Exact GR is obtained by
removing that independent field from the local quotient, not by taking its
singular zero-coefficient endpoint.

## 5. Minimal `P(X)` tensor protection

For a homogeneous clock and a trace-free tensor perturbation,

```text
h_ij=a^2 [exp(gamma)]_ij,    tr(gamma)=0,
det(h)=a^6,                  X=-dot(psi)^2/N^2.
```

Therefore `N sqrt(h) P(X,psi)` is independent of `gamma` at all orders.
The executed first and second TT variations are
`{tt['PX_TT_first_variation']}` and
`{tt['PX_TT_second_variation']}`. Dynamic scalar/metric mixing remains in
the scalar constraint sector and vanishes in the static limit found at
5184.

## 6. The `O4=C^2 X` correction that cannot be skipped

FLRW has `Cbar=0`; this kills the background contribution and first
variation. It does **not** kill the second variation. For a flat local TT
wave with plus/cross amplitudes,

```text
C1_abcd C1^abcd
 =(gamma_plus^2+gamma_cross^2)(omega^2-k^2)^2.
```

The executed Weyl identity residual is
`{tt['weyl_identity_residual']}`. With `q2=omega^2-k^2`, the principal
kernel per polarization pair is

```text
{tt['TT_total_principal_kernel']}.
```

It factorizes into the GR massless pole and, if `c_O4 X !=0`, a second pole

```text
q2={tt['extra_pole_q2']}.
```

Consequences:

1. `psi=0 -> X=0` protects the local vacuum tensor Hessian exactly.
2. A homogeneous cosmological clock generally activates the `q^4` term.
3. A low-energy order-reduced claim requires
   `epsilon_O4=|4 c_O4 X q2/M_R^2| << 1` over the whole tested band.
4. An exact all-scale two-mode claim requires a parent degeneracy,
   cancellation, or `c_O4 X=0` theorem.

This corrects the tempting but false shortcut “background Weyl is zero, so
the operator has no tensor Hessian.”

## 7. Local, cosmological, and galaxy branches

```text
local psi=0:
  exact quadratic metric/scalar block diagonal;
  O4 pure-metric Hessian zero;
  leading local GR/Newton/Maxwell chain retained.

homogeneous FLRW clock:
  P(X) changes background/scalar dynamics;
  P(X) pure TT Hessian zero;
  O4 tensor EFT gate open.

stationary classical galaxy profile:
  rejected by the healthy P(X) no-lump theorem.

occupied isotropic galaxy state:
  retained as the only current route to the required nonlocal
  common-scalar susceptibility.
```

The same action coefficients must be used in every branch. Arena dependence
may enter through a derived state/boundary preparation law, not by refitting
the parent Wilson coefficients.

## 8. Exact occupied-state target

Use common/slip variables

```text
c=(Phi+Psi)/sqrt(2),    s=(Phi-Psi)/sqrt(2).
```

For `K_eff=K_GR-Sigma`, the 5148 target is

```text
C_q(y)=y^(1+q)/(1+y^q),  y=mu/|k|, q=0.77,
Sigma_cc/K_GR,cc=A C_q/(1+A C_q),
K_eff,cc/K_GR,cc=1/(1+A C_q).
```

For `A>=0` this is positive, monotone and statically stable. The executed
sample gives

```text
min(Sigma_cc/K_GR)={response['sample_fraction_minimum']:.6e},
max(Sigma_cc/K_GR)={response['sample_fraction_maximum']:.6e},
min(K_eff/K_GR)={response['sample_effective_ratio_minimum']:.6e}.
```

No-slip for arbitrary ordinary scalar sources requires
`Sigma_cs=Sigma_sc=0` with an invertible slip block. Tensor protection
requires `Pi_TT Sigma Pi_TT=0` or an explicit frequency-dependent bound.
The full CTP kernel must also satisfy its diffeomorphism Ward identity and
retarded/noise positivity.

## 9. A real origin no-go and the remaining constructive target

After the local Einstein residue is matched, a local gapped vacuum
polarization is analytic in `k^2` near zero. The target instead has

```text
C_q~mu/|k|                    (deep infrared),
K_eff/K_GR~|k|/(A mu),
```

so the absolute inverse kernel contains a nonanalytic `|k|^3` term. A
gapped local vacuum loop cannot generate it. The viable origin class is
therefore narrowed to a gapless continuum or an occupied-state retarded
stress spectral density.

The next actual derivation is not another missing-variable ledger. It is:

```text
derive rho_cc(omega,k) from the parent occupied motion state;
prove the Ward identity;
project rho_cs and rho_TT;
recover or reject C_q and its mu law with one cross-arena parameter set.
```

The Poynting vector remains relevant as the universal `T^0i_EM` momentum
source. A stationary Poynting vector is not, by itself, the missing common
scalar susceptibility; any transfer must be derived dynamically in the
same CTP kernel.

## 10. Claim boundary

Established here:

```text
motion-scalar ADM map                 = exact;
clock-only ancestry                   = exact;
six spatial metric directions remain = exact;
EH+P(X) mode count                    = 2 tensor + 1 scalar;
local psi=0 tensor protection         = exact at quadratic order;
homogeneous P(X) TT Hessian           = zero;
O4 TT Hessian on Cbar=0               = nonzero off shell;
O4 low-energy control parameter       = derived;
galaxy common/slip/TT target          = exact;
gapped-vacuum origin                  = rejected under stated assumptions.
```

Not established:

```text
old-scalar derivation of spatial coframe;
numeric or symmetry proof for c_O4 X in cosmology;
occupied-state CTP spectral density;
derived q=0.77 or mu state law;
full MTS unification or galaxy claim;
numerical first-principles G_N.
```

## 11. Machine artifacts

- `source-intake/functional_rg/5189/motion_ancestry_and_field_ownership.csv`
- `source-intake/functional_rg/5189/scalar_ADM_stress_and_current_projection.csv`
- `source-intake/functional_rg/5189/branch_Hessian_irrep_projection.csv`
- `source-intake/functional_rg/5189/O4_TT_principal_symbol_and_EFT_gate.csv`
- `source-intake/functional_rg/5189/ADM_constraint_and_mode_count.csv`
- `source-intake/functional_rg/5189/unit_flow_correspondence_compatibility.csv`
- `source-intake/functional_rg/5189/local_cosmology_galaxy_branch_matrix.csv`
- `source-intake/functional_rg/5189/occupied_state_response_target.csv`
- `source-intake/functional_rg/5189/source_provenance.csv`
- `source-intake/functional_rg/5189/motion_ADM_projection_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5189_VALIDATION.csv`
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def calculate_validations(
    source_hashes: dict[str, str],
    formal_before: str,
    checkpoint_5176_before: str,
    result_4935: dict[str, Any],
    result_4956: dict[str, Any],
    result_5148: dict[str, Any],
    result_5184: dict[str, Any],
    result_5187: dict[str, Any],
    result_5188: dict[str, Any],
    adm: dict[str, Any],
    tt: dict[str, Any],
    unit_flow: dict[str, Any],
    constraints: dict[str, Any],
    response: dict[str, Any],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check: str, passed: bool, observed: Any, expected: Any) -> None:
        checks.append(
            validation_row(
                f"V5189_{len(checks):02d}",
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
        "4935 identifies O4 as unique quadratic motion portal",
        result_4935["six_derivative_entry"][
            "motion_rows_with_nonzero_quadratic_Hessian"
        ]
        == ["S6_O4"],
        result_4935["six_derivative_entry"][
            "motion_rows_with_nonzero_quadratic_Hessian"
        ],
        ["S6_O4"],
    )
    add(
        "4956 retains local fixed-function germ",
        result_4956["gates"]["local_x_le_0p1_fixed_function_germ"] is True,
        result_4956["gates"]["local_x_le_0p1_fixed_function_germ"],
        True,
    )
    add(
        "5148 q lock is 0.77",
        math.isclose(result_5148["kernel"]["q"], 0.77),
        result_5148["kernel"]["q"],
        0.77,
    )
    add(
        "5184 rejects regular localized stationary PX profile",
        result_5184["summary"]["regular_localized_static_PX_background_exists"]
        is False,
        result_5184["summary"]["regular_localized_static_PX_background_exists"],
        False,
    )
    add(
        "5187 vacuum Hessian is block diagonal",
        result_5187["Hessian"]["vacuum_Hessian_block_diagonal"] is True,
        result_5187["Hessian"]["vacuum_Hessian_block_diagonal"],
        True,
    )
    add(
        "5188 ADM metric mode count is two",
        result_5188["ADM"]["physical_spin2_configuration_dof"] == 2,
        result_5188["ADM"]["physical_spin2_configuration_dof"],
        2,
    )
    add("ADM X projection exact", adm["X"] == "-Pi**2 + s1**2 + s2**2 + s3**2", adm["X"], "-Pi**2 + s1**2 + s2**2 + s3**2")
    add("ADM rho projection exact", adm["rho"] == "P + 2*P_X*Pi**2", adm["rho"], "P + 2*P_X*Pi**2")
    add(
        "ADM anisotropic stress is traceless",
        adm["anisotropic_trace"] == "0",
        adm["anisotropic_trace"],
        "0",
    )
    add(
        "homogeneous timelike anisotropic stress vanishes",
        adm["timelike_anisotropic_zero"] is True,
        adm["timelike_anisotropic_zero"],
        True,
    )
    add(
        "spacelike gradient has anisotropic stress",
        adm["spacelike_anisotropic_nonzero"] is True,
        adm["spacelike_anisotropic_nonzero"],
        True,
    )
    add(
        "normalized scalar-gradient flow is Frobenius integrable",
        adm["frobenius_zero"] is True,
        adm["frobenius_components"],
        ["0", "0", "0", "0"],
    )
    add(
        "fixed clock leaves six spatial metric directions",
        adm["fixed_clock_spatial_metric_rank"] == 6,
        adm["fixed_clock_spatial_metric_rank"],
        6,
    )
    add(
        "tracefree tensor determinant is exactly a^6",
        tt["TT_determinant_exact"] is True,
        tt["TT_spatial_determinant"],
        "a**6",
    )
    add(
        "homogeneous PX pure TT Hessian vanishes",
        tt["PX_TT_Hessian_zero"] is True,
        tt["PX_TT_second_variation"],
        "0",
    )
    add(
        "linearized TT Ricci scalar vanishes",
        tt["ricci_scalar"] == "0",
        tt["ricci_scalar"],
        "0",
    )
    add(
        "linearized TT Weyl square matches exact q4 form",
        tt["weyl_squared_exact"] is True,
        tt["weyl_squared"],
        tt["expected_weyl_squared"],
    )
    add(
        "Weyl curvature identity closes",
        tt["weyl_identity_exact"] is True,
        tt["weyl_identity_residual"],
        "0",
    )
    add(
        "EH plus O4 principal kernel retains massless residue",
        tt["massless_residue_factor"] == "M_R2/4",
        tt["massless_residue_factor"],
        "M_R2/4",
    )
    add(
        "O4 cosmological clock is not falsely marked zero",
        tt["cosmological_clock_O4_exactly_zero"] is False,
        tt["cosmological_clock_O4_exactly_zero"],
        False,
    )
    add(
        "local X zero protects O4 tensor Hessian",
        tt["local_zero_background_exact"] is True,
        tt["local_zero_background_exact"],
        True,
    )
    add(
        "PX matter gives no lapse or shift velocity Hessian",
        constraints["lapse_shift_velocity_block_zero"] is True,
        constraints["lapse_shift_velocity_block_zero"],
        True,
    )
    add(
        "regular PX matter has one scalar velocity direction",
        constraints["regular_scalar_velocity_rank"] == 1,
        constraints["regular_scalar_velocity_rank"],
        1,
    )
    add(
        "pure metric ADM count is two",
        constraints["pure_metric_configuration_dof"] == 2,
        constraints["pure_metric_configuration_dof"],
        2,
    )
    add(
        "metric plus regular PX count is three",
        constraints["metric_plus_PX_configuration_dof"] == 3,
        constraints["metric_plus_PX_configuration_dof"],
        3,
    )
    add(
        "independent unit flow has five gravity/aether modes",
        constraints["independent_aether_gravity_configuration_dof"] == 5,
        constraints["independent_aether_gravity_configuration_dof"],
        5,
    )
    add(
        "PPN c4 surface identity closes",
        unit_flow["PPN_c4_residual"] == "0",
        unit_flow["PPN_c4_residual"],
        "0",
    )
    add(
        "PPN c2 surface identity closes",
        unit_flow["PPN_c2_residual"] == "0",
        unit_flow["PPN_c2_residual"],
        "0",
    )
    add(
        "Newton and cosmology denominators lock",
        unit_flow["Gcos_GN_denominator_residual"] == "0",
        unit_flow["Gcos_GN_denominator_residual"],
        "0",
    )
    add(
        "unit-flow exact-zero endpoint remains singular",
        unit_flow["exact_zero_endpoint_chart_singular"] is True,
        unit_flow["exact_zero_endpoint_chart_singular"],
        True,
    )
    add(
        "galaxy support small-y coefficient is one",
        response["support_small_y_coefficient"] == "1",
        response["support_small_y_coefficient"],
        "1",
    )
    add(
        "galaxy support large-y coefficient is one",
        response["support_large_y_coefficient"] == "1",
        response["support_large_y_coefficient"],
        "1",
    )
    add(
        "Schur fraction tends zero locally",
        response["schur_fraction_small_y"] == "0",
        response["schur_fraction_small_y"],
        "0",
    )
    add(
        "Schur fraction tends one in deep infrared",
        response["schur_fraction_large_y"] == "1",
        response["schur_fraction_large_y"],
        "1",
    )
    add(
        "sampled target is positive and stable",
        response["static_positive_for_A_positive"] is True,
        (
            response["sample_fraction_minimum"],
            response["sample_fraction_maximum"],
            response["sample_effective_ratio_minimum"],
        ),
        "0<f<1 and 0<Keff/K<1",
    )
    add(
        "no-slip projector condition is explicit",
        response["no_slip_condition"]
        == "Sigma_cs=Sigma_sc=0 with invertible slip block",
        response["no_slip_condition"],
        "Sigma_cs=Sigma_sc=0 with invertible slip block",
    )
    add(
        "tensor projector condition is explicit",
        response["tensor_condition"]
        == "Pi_TT Sigma Pi_TT=0 or explicitly bounded",
        response["tensor_condition"],
        "Pi_TT Sigma Pi_TT=0 or explicitly bounded",
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

    result_4935 = json.loads(
        SOURCES["checkpoint_4935_result"][0].read_text(encoding="utf-8")
    )
    result_4956 = json.loads(
        SOURCES["checkpoint_4956_result"][0].read_text(encoding="utf-8")
    )
    result_5148 = json.loads(
        SOURCES["checkpoint_5148_result"][0].read_text(encoding="utf-8")
    )
    result_5184 = json.loads(
        SOURCES["checkpoint_5184_result"][0].read_text(encoding="utf-8")
    )
    result_5187 = json.loads(
        SOURCES["checkpoint_5187_result"][0].read_text(encoding="utf-8")
    )
    result_5188 = json.loads(
        SOURCES["checkpoint_5188_result"][0].read_text(encoding="utf-8")
    )

    adm_rows, adm_metrics = build_scalar_adm_projection()
    ancestry_rows = build_ancestry_rows(adm_metrics)
    o4_rows, irrep_rows, tt_metrics = build_tt_and_irrep_rows()
    unit_flow_rows, unit_flow_metrics = build_unit_flow_rows()
    constraint_rows, constraint_metrics = build_constraint_rows()
    response_rows, response_metrics = build_response_rows()
    branch_rows = build_branch_rows()
    provenance_rows = build_provenance_rows(source_hashes)

    checks = calculate_validations(
        source_hashes,
        formal_before,
        checkpoint_5176_before,
        result_4935,
        result_4956,
        result_5148,
        result_5184,
        result_5187,
        result_5188,
        adm_metrics,
        tt_metrics,
        unit_flow_metrics,
        constraint_metrics,
        response_metrics,
    )
    failures = [row for row in checks if row["status"] != "PASS"]
    if failures:
        raise RuntimeError(
            "Pre-write validation failed:\n" + json.dumps(failures, indent=2)
        )

    outputs = {
        ANCESTRY_CSV: ancestry_rows,
        ADM_STRESS_CSV: adm_rows,
        IRREP_CSV: irrep_rows,
        O4_TT_CSV: o4_rows,
        CONSTRAINT_CSV: constraint_rows,
        UNIT_FLOW_CSV: unit_flow_rows,
        BRANCH_CSV: branch_rows,
        RESPONSE_CSV: response_rows,
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
        "parent_action": PARENT_ACTION,
        "ADM_projection": adm_metrics,
        "tensor_projection": tt_metrics,
        "constraint_count": constraint_metrics,
        "unit_flow": unit_flow_metrics,
        "occupied_state_target": response_metrics,
        "branch_decision": {
            "old_motion_scalar_owns_clock": True,
            "old_motion_scalar_owns_spatial_coframe": False,
            "local_psi_zero_two_tensor_sector_protected": True,
            "homogeneous_PX_TT_Hessian_zero": True,
            "homogeneous_O4_TT_Hessian_zero": False,
            "stationary_classical_PX_galaxy_route": False,
            "occupied_state_response_route_retained": True,
            "gapped_vacuum_can_generate_target_nonanalytic_kernel": False,
            "next_constructive_target": (
                "derive occupied-state retarded stress spectral density and"
                " project common/slip/TT channels with one mu law"
            ),
        },
        "claim_status": {
            "clock_only_motion_ancestry_derived": True,
            "spatial_coframe_derived_from_old_scalar": False,
            "leading_local_GR_quadratic_sector_retained": True,
            "exact_all_scale_cosmological_two_tensor_mode_claim": False,
            "galaxy_kernel_derived_from_parent_CTP": False,
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
            f"V5189_{len(checks):02d}",
            "formalization workbench remains unchanged after writes",
            formal_after == formal_before == FORMAL_DIGEST_LOCK,
            formal_after,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            f"V5189_{len(checks) + 1:02d}",
            "checkpoint 5176 remains unchanged after writes",
            checkpoint_5176_after
            == checkpoint_5176_before
            == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_after,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            f"V5189_{len(checks) + 2:02d}",
            "all checkpoint artifacts exist and are nonempty",
            all(path.is_file() and path.stat().st_size > 0 for path in expected_outputs),
            sum(path.is_file() and path.stat().st_size > 0 for path in expected_outputs),
            len(expected_outputs),
        ),
        validation_row(
            f"V5189_{len(checks) + 3:02d}",
            "all generated CSV files parse with at least one row",
            all(len(read_csv(path)) > 0 for path in outputs),
            sum(len(read_csv(path)) > 0 for path in outputs),
            len(outputs),
        ),
        validation_row(
            f"V5189_{len(checks) + 4:02d}",
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
            f"V5189_{len(checks) + 5:02d}",
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
                "checkpoint": 5189,
                "marker": MARKER,
                "validation_passed": len(final_checks),
                "validation_failed": 0,
                "clock_only_ancestry": True,
                "fixed_clock_spatial_rank": adm_metrics[
                    "fixed_clock_spatial_metric_rank"
                ],
                "metric_plus_scalar_dof": constraint_metrics[
                    "metric_plus_PX_configuration_dof"
                ],
                "local_tensor_dof": constraint_metrics[
                    "local_resolved_gravity_dof_below_gap"
                ],
                "PX_TT_Hessian_zero": tt_metrics["PX_TT_Hessian_zero"],
                "O4_TT_Hessian_zero_on_clock": tt_metrics[
                    "cosmological_clock_O4_exactly_zero"
                ],
                "O4_extra_pole": tt_metrics["extra_pole_q2"],
                "galaxy_target_static_positive": response_metrics[
                    "static_positive_for_A_positive"
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
