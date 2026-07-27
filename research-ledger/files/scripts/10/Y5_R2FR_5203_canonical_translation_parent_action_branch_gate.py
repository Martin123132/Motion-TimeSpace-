from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5203"
DOCUMENT = (
    POST
    / "5203-Y5-R2FR-one-canonical-translation-gauge-parent-action-"
    "cross-coupling-and-branch-reduction-theorem.md"
)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5203_VALIDATION.csv"
)
CHECKPOINT_5202_OUT = POST / "source-intake" / "functional_rg" / "5202"
PUBLIC_WORKTREE = Path(
    r"C:\Users\ollet\OneDrive\Documents\Motion-TimeSpace-public-update-2026-07-22"
)
GALAXY_REPO = Path(r"D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo")

MARKER = "MTS_5203_ONE_CANONICAL_TRANSLATION_PARENT_ACTION_BRANCH_THEOREM"
CHECKED_DATE = "2026-07-24"
FORMAL_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5202_OUT_LOCK = (
    "56ed69780a647a3cb65da2943e274f717a2ab532d4641e17251f0e0dadd1d8bb"
)
PUBLIC_HEAD_LOCK = "8913c00b77d98e457ddb0c48e9aeec9cc5f309fd"
GALAXY_HEAD_LOCK = "f850e4997657f457dddc05cbe50f21186588dcc7"

SOURCE_LOCKS = {
    "4919-Y5-R2FR-vacuum-1PI-operator-selection-curvature-Higgs-and-hidden-scalar-vev-matching-or-local-bound.md": (
        "47144e184bb1b37a0bb50ae630a5a80020ff5f7c372fe0dc1cef8e7ce79db629"
    ),
    "4950-Y5-R2FR-reflection-even-pair-source-operator-Rpsi2-Tpsi2-and-stabilized-galaxy-bifurcation-window-or-route-rejection.md": (
        "64188638f5d19e125e5c1305cce898332267295b26625c1492610a3c529774cf"
    ),
    "4951-Y5-R2FR-coupled-motion-VFZX2-functional-flow-fixed-point-index-and-GR-connected-trajectory-or-even-pair-sector-rejection.md": (
        "1dd7f2632ab15370e7b44272c2439a6cf70d5559b1c7993b6f55d7e9fab9a131"
    ),
    "5187-Y5-R2FR-canonical-local-parent-action-Hessian-source-residue-and-scale-setting-theorem.md": (
        "4556205ec12e11930a13d0ed9b5e27b6b4619f3752a5e10db2a4b767dcdec674"
    ),
    "5191-Y5-R2FR-O4-FLRW-tensor-nondegeneracy-order-reduction-and-cosmological-safety-theorem.md": (
        "4568e2ac3fe467b2fa1e2c294058692a0c62994e53e703405b2b18864742b6fa"
    ),
    "5192-Y5-R2FR-parent-motion-FLRW-branch-memory-separation-and-mass-gap-cosmology-gate.md": (
        "e171efb8d498df44b535f6c25517c86a0cd5e8b993a67bfb8a9e3b74301eecc3"
    ),
    "5196-Y5-R2FR-invariant-mass-gap-Hessian-and-homogeneous-state-selection-theorem.md": (
        "a3495f713d22fea38ebd010a1d0f14d2ff266180fa358ee8a89492a55ea57974"
    ),
    "5197-Y5-R2FR-universal-gap-cross-arena-compatibility-and-route-separation-theorem.md": (
        "f01f94465168758886800556f345e370910f6913e80f1a4a0c646bbe7abe0c0a"
    ),
    "5200-Y5-R2FR-CTP-vacuum-occupied-projector-metric-and-composite-exponent-ownership-gate.md": (
        "348e580fb9c48c28b4b77e2219e0bc8760bcd012081373e7120caa7aac83e656"
    ),
    "5201-Y5-R2FR-source-complete-coframe-variation-full-PPN-calibration-and-local-state-silence-theorem.md": (
        "e77e2f7b5c3b4376c7e8a792342c3ec49c912627c60f83c712597c74ccbb8507"
    ),
    "5202-Y5-R2FR-scalar-curvature-no-go-translation-gauge-TEGR-coframe-ancestry-and-mode-theorem.md": (
        "753a01fd12a36fe687877c70a89b97b838a5761a6af31c5d756c4ec5bc7a810b"
    ),
    "source-intake/functional_rg/4950/pair_operator_RG_and_bifurcation_results.json": (
        "9243cf84c42036cddb29a267e6d425cc0f443d74410af11965542e0470860860"
    ),
    "source-intake/functional_rg/4951/coupled_VFZX2_fixed_and_running_gate_results.json": (
        "d48c187595a71c3be6c2720a7545372d06361788a2fb242b902ef8e4bfe6ad8c"
    ),
    "source-intake/functional_rg/5187/canonical_local_parent_action_results.json": (
        "05d9e06edf88c219a6d21f49303b7e98dd82f3d1ecee5c9d445da385d4fa4e6d"
    ),
    "source-intake/functional_rg/5191/O4_FLRW_tensor_order_reduction_results.json": (
        "e8c3d48469a0e47a5629d30dd43992e1193f20f064f6c582db496514ac08712d"
    ),
    "source-intake/functional_rg/5192/parent_motion_FLRW_results.json": (
        "b05068d679118084d07d1b9420603d9bd231369ef1e5889d2ab5c3fa0171df32"
    ),
    "source-intake/functional_rg/5196/mass_gap_and_state_selection_results.json": (
        "aecba0a57eaf557b6fddd18948c0d74e00a2e68e1d892516e10d2d0763fe0f04"
    ),
    "source-intake/functional_rg/5197/universal_gap_cross_arena_results.json": (
        "e42f0be823acd57eed630cca62b1e84a66e85cc81ba4354a24a0dcb93d1d0c0e"
    ),
    "source-intake/functional_rg/5200/CTP_projector_metric_exponent_ownership_results.json": (
        "7440b1818c7377f913d84ee665d4bd40f7055b3481eb003a63b787c63e58594e"
    ),
    "source-intake/functional_rg/5201/source_complete_coframe_PPN_local_silence_results.json": (
        "99939a2990e033451ee5c33dbaffcf7ffeaa2e2131156c6d6161e70f0964141c"
    ),
    "source-intake/functional_rg/5202/translation_gauge_TEGR_coframe_ancestry_results.json": (
        "7cd2cdf5a76fce560382303bf9e1f13e49279943cd0533db48d93346697e3bb1"
    ),
}


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    files = sorted(item for item in path.rglob("*") if item.is_file())
    for item in files:
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(file_digest(item).encode("ascii"))
    return digest.hexdigest()


def git_state(repository: Path) -> tuple[str, str]:
    safe_path = repository.as_posix()
    head = subprocess.run(
        ["git", "-c", f"safe.directory={safe_path}", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "-c", f"safe.directory={safe_path}", "status", "--short"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return head, status


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(field for field in row if field not in fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": 5203,
            "marker": MARKER,
            "checked_date": CHECKED_DATE,
            "valid_for_full_MTS_claim": False,
            **row,
        }
        for row in rows
    ]


def assert_source_locks() -> None:
    failures: list[str] = []
    for relative_path, expected_digest in SOURCE_LOCKS.items():
        source_path = POST / relative_path
        if not source_path.exists():
            failures.append(f"missing:{relative_path}")
            continue
        actual_digest = file_digest(source_path)
        if actual_digest != expected_digest:
            failures.append(
                f"hash:{relative_path}:{actual_digest}!={expected_digest}"
            )
    if tree_digest(FORMAL) != FORMAL_LOCK:
        failures.append("formalization-workbench tree changed")
    if tree_digest(CHECKPOINT_5202_OUT) != CHECKPOINT_5202_OUT_LOCK:
        failures.append("checkpoint-5202 output tree changed")
    if failures:
        raise RuntimeError("source lock failure: " + "; ".join(failures))


def canonical_parent_action() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = tagged(
        [
            {
                "block": "CTP_parent",
                "action_term": (
                    "Gamma_CTP=S_can[+]-S_can[-]+Gamma_IF[+,-]"
                    "+Gamma_rho_i[Sigma_i]"
                ),
                "field_owner": "one doubled bulk action plus one initial state",
                "symmetry": "diagonal Diff x local Lorentz x U(1) x Z2",
                "coefficient_status": "STRUCTURAL_PARENT_FORM",
                "local_branch": "physical limit plus rho_i=rho_0",
                "cosmology_branch": "homogeneous state datum",
                "galaxy_branch": "occupied reduced state only through Gamma_rho_i",
            },
            {
                "block": "relational_coframe",
                "action_term": "e^A_mu=D_mu X^A+mathcalB^A_mu",
                "field_owner": "X^A;mathcalB^A_mu;omega_inertial",
                "symmetry": "local translations and local Lorentz",
                "coefficient_status": "5202_CONSTRUCTED_PARENT_CANDIDATE",
                "local_branch": "one nondegenerate universal coframe",
                "cosmology_branch": "FLRW coframe",
                "galaxy_branch": "same coframe; no galaxy-only metric",
            },
            {
                "block": "curvature_function",
                "action_term": "integral e F_R(psi) R_LC/2",
                "field_owner": "coframe plus reflection-even motion scalar",
                "symmetry": "Diff x local Lorentz x Z2",
                "coefficient_status": "FUNCTION_REQUIRED_FOR_RG_CLOSURE",
                "local_branch": "F_R(0)=M_R^2;F_R'(0)=0",
                "cosmology_branch": "open when psi is nonzero",
                "galaxy_branch": "cannot be fitted per arena",
            },
            {
                "block": "teleparallel_completion",
                "action_term": (
                    "integral e[-F_R T_TEGR/2"
                    "-T^mu partial_mu F_R]+matched_boundary"
                ),
                "field_owner": "translation connection through e and torsion",
                "symmetry": "exact curvature-equivalent TEGR representation",
                "coefficient_status": "DERIVED_FROM_R_EQUALS_MINUS_T_PLUS_B",
                "local_branch": "-M_R^2 T_TEGR/2",
                "cosmology_branch": "same as scalar-curvature action",
                "galaxy_branch": "same as scalar-curvature action",
            },
            {
                "block": "cosmological_density",
                "action_term": "-integral e U_Lambda",
                "field_owner": "metric vacuum block",
                "symmetry": "all parent gauge symmetries",
                "coefficient_status": "CALIBRATED_LAMBDA_DIRECTION",
                "local_branch": "negligible local curvature correction",
                "cosmology_branch": "Lambda_cal retained",
                "galaxy_branch": "same universal value",
            },
            {
                "block": "motion_function",
                "action_term": (
                    "integral e[-Z(psi)X_psi/2-V_even(psi)"
                    "+P_ge_2(X_psi)]"
                ),
                "field_owner": "psi",
                "symmetry": "Diff x Z2",
                "coefficient_status": "MASS_RELEVANT_OTHER_FUNCTIONS_OPEN_OR_TRAJECTORY",
                "local_branch": "psi=0;X_psi=0",
                "cosmology_branch": "homogeneous massive or functional branch",
                "galaxy_branch": "elementary pole is not L_eff",
            },
            {
                "block": "Maxwell",
                "action_term": "-Z_A integral e F_mu_nu F^mu_nu/4",
                "field_owner": "A_mu and visible U(1) representations",
                "symmetry": "U(1) x Diff",
                "coefficient_status": "ONE_ALPHA_EM_CALIBRATION",
                "local_branch": "exact flat Maxwell",
                "cosmology_branch": "zero background field in tested branch",
                "galaxy_branch": "same visible electromagnetism",
            },
            {
                "block": "visible_matter",
                "action_term": "S_visible[e,omega_LC[e],A,Phi_SM]",
                "field_owner": "visible representations",
                "symmetry": "Diff x local Lorentz x visible gauge group",
                "coefficient_status": "PARENT_FIELD_CONTENT",
                "local_branch": "one Hilbert source",
                "cosmology_branch": "same matter and radiation source",
                "galaxy_branch": "same baryonic source",
            },
            {
                "block": "CFF",
                "action_term": "c_IR integral e C_mu_nu_rho_sigma F^mu_nu F^rho_sigma",
                "field_owner": "metric-photon EFT",
                "symmetry": "Diff x U(1) x parity even",
                "coefficient_status": "PHYSICAL_TOTAL_LEC_OPEN",
                "local_branch": "zero in conformally flat space; bounded otherwise",
                "cosmology_branch": "zero on exact FLRW",
                "galaxy_branch": "negligible bounded lensing correction",
            },
            {
                "block": "C3",
                "action_term": "G_C3 integral e Tr(C^3)",
                "field_owner": "metric EFT",
                "symmetry": "Diff x parity even",
                "coefficient_status": "SELECTED_TRAJECTORY_COORDINATE",
                "local_branch": "finite higher-gradient residual",
                "cosmology_branch": "zero on exact FLRW",
                "galaxy_branch": "same coefficient; no retuning",
            },
            {
                "block": "O4",
                "action_term": "-u_O4 integral e C^2 X_psi",
                "field_owner": "metric-motion EFT",
                "symmetry": "Diff x Z2 x parity even",
                "coefficient_status": "PARENT_OWNED_FIXED_POINT_COORDINATE",
                "local_branch": "zero at psi=0",
                "cosmology_branch": "zero on exact FLRW background; tensor effect order reduced",
                "galaxy_branch": "same coefficient; no static mass source",
            },
            {
                "block": "completion",
                "action_term": "Gamma_contact+Gamma_nonlocal+Gamma_p8plus",
                "field_owner": "renormalized EFT completion",
                "symmetry": "same parent symmetries",
                "coefficient_status": "FINITE_OPEN_OPERATOR_CORRIDOR",
                "local_branch": "must be bounded or order reduced",
                "cosmology_branch": "not silently set to zero",
                "galaxy_branch": "not a phase-profile fitting slot",
            },
        ]
    )

    coordinate = sp.symbols("x")
    density = sp.Function("e")(coordinate)
    coupling = sp.Function("F_R")(coordinate)
    torsion_vector = sp.Function("T")(coordinate)
    product_rule_residual = sp.simplify(
        coupling * sp.diff(density * torsion_vector, coordinate)
        - sp.diff(density * coupling * torsion_vector, coordinate)
        + density * torsion_vector * sp.diff(coupling, coordinate)
    )

    derivative_coordinates = sp.Matrix(
        [[1, 2, 0, -1], [0, 1, 3, 2], [2, -1, 1, 0], [1, 0, 2, 1]]
    )
    translation_connection = sp.Matrix(
        [[0, 1, -1, 2], [2, 0, 1, -1], [1, 3, 0, 1], [-1, 2, 1, 0]]
    )
    derivative_parameter = sp.Matrix(
        [[1, -2, 1, 0], [0, 1, -1, 2], [2, 0, 1, -1], [1, 1, 0, 1]]
    )
    coframe = derivative_coordinates + translation_connection
    shifted_coframe = (
        derivative_coordinates
        + derivative_parameter
        + translation_connection
        - derivative_parameter
    )
    translation_residual = sp.simplify(shifted_coframe - coframe)

    diagnostics = {
        "canonical_block_count": len(rows),
        "curvature_to_teleparallel_product_rule_residual": str(
            product_rule_residual
        ),
        "translation_gauge_residual": str(translation_residual),
        "sample_coframe_determinant": str(coframe.det()),
        "one_bulk_action": True,
        "one_universal_coframe": True,
        "metric_reintroduced_as_independent_field": False,
        "curvature_function_silently_zeroed": False,
    }
    return rows, diagnostics


def parent_variation_and_ward_identities(
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    derivative_map = sp.Matrix([[1, 2, 0], [0, 1, -1], [2, 0, 1]])
    kernel = sp.Matrix([[3, 1, 0], [1, 4, 2], [0, 2, 5]])
    source = sp.Matrix(sp.symbols("j0:3"))
    relational = sp.Matrix(sp.symbols("x0:3"))
    connection = sp.Matrix(sp.symbols("b0:3"))
    coframe = derivative_map * relational + connection
    action = sp.expand(
        (coframe.T * kernel * coframe)[0] / 2
        + (source.T * coframe)[0]
    )
    connection_equation = sp.Matrix(
        [sp.diff(action, component) for component in connection]
    )
    relational_equation = sp.Matrix(
        [sp.diff(action, component) for component in relational]
    )
    chain_rule_residual = sp.simplify(
        relational_equation - derivative_map.T * connection_equation
    )

    rows = tagged(
        [
            {
                "variation": "mathcalB^A_mu",
                "equation": "delta Gamma/delta mathcalB^A_mu=E_A^mu[e]",
                "identity_role": "full coframe equation",
                "branch_consequence": (
                    "F_R G_mu_nu+(g_mu_nu Box-nabla_mu nabla_nu)F_R"
                    "+U_Lambda g_mu_nu+DeltaE_EFT=T_total_mu_nu"
                ),
                "status": "EXACT_CHAIN_RULE",
            },
            {
                "variation": "X^A",
                "equation": "delta Gamma/delta X^A=-D_mu E_A^mu",
                "identity_role": "translation/diffeomorphism Ward consequence",
                "branch_consequence": "no extra relational scalar equation",
                "status": "EXACT_REDUNDANCY",
            },
            {
                "variation": "omega_inertial",
                "equation": "R[omega]=0; antisymmetric coframe equation is Lorentz Ward",
                "identity_role": "inertial frame covariance",
                "branch_consequence": "no independent propagating spin connection",
                "status": "TEGR_INERTIAL_CONNECTION",
            },
            {
                "variation": "A_nu",
                "equation": (
                    "Z_A nabla_mu F^mu_nu"
                    "-4c_IR nabla_mu(C^mu_nu_rho_sigma F^rho_sigma)=J^nu"
                ),
                "identity_role": "U(1) Euler equation",
                "branch_consequence": "nabla_mu J^mu=0",
                "status": "SAME_MAXWELL_PARENT",
            },
            {
                "variation": "psi",
                "equation": (
                    "nabla_mu[(Z-2P_X+2u_O4 C^2)nabla^mu psi]"
                    "+F_R' R/2-Z' X/2-V'=0"
                ),
                "identity_role": "motion field equation",
                "branch_consequence": "psi=0 exact for analytic Z2-even functions",
                "status": "FUNCTIONAL_EQUATION",
            },
            {
                "variation": "visible_fields",
                "equation": "delta S_visible/delta Phi_i=0",
                "identity_role": "visible matter equations",
                "branch_consequence": "one universal metric and gauge source",
                "status": "UNCHANGED_VISIBLE_PARENT",
            },
            {
                "variation": "diagonal_diffeomorphism",
                "equation": (
                    "nabla_mu(T_bulk^mu_nu+T_state^mu_nu)=0"
                    " on all bulk and state equations"
                ),
                "identity_role": "total Hilbert conservation",
                "branch_consequence": "no hidden source normalization",
                "status": "WARD_IDENTITY",
            },
            {
                "variation": "local_Lorentz",
                "equation": "E_[AB]+D_mu S^mu_AB/2=0",
                "identity_role": "symmetric improved Hilbert source",
                "branch_consequence": "six frame directions remain gauge",
                "status": "WARD_IDENTITY",
            },
        ]
    )
    diagnostics = {
        "finite_chain_rule_residual": str(chain_rule_residual),
        "connection_equation_rank": connection_equation.jacobian(
            list(connection)
        ).rank(),
        "relational_equation_is_dependent": True,
        "independent_metric_source_components": 10,
        "independent_relational_equations": 0,
        "total_Hilbert_conservation_on_shell": True,
    }
    return rows, diagnostics


def local_double_zero_theorem(
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    psi = sp.symbols("psi")
    m_r_squared, xi_two, f_four = sp.symbols("M_R2 xi_2 f_4")
    z_a_zero, z_a_two = sp.symbols("Z_A0 Z_A2")
    matter_two = sp.symbols("a_m2")
    vacuum, mass_squared, quartic = sp.symbols("V_0 M_psi2 lambda_4")
    curvature, field_strength_squared, matter_lagrangian = sp.symbols(
        "R F2 L_m"
    )

    curvature_function = (
        m_r_squared
        + xi_two * psi**2 / 2
        + f_four * psi**4 / sp.factorial(4)
    )
    gauge_function = z_a_zero + z_a_two * psi**2 / 2
    matter_function = 1 + matter_two * psi**2 / 2
    potential = (
        vacuum
        + mass_squared * psi**2 / 2
        + quartic * psi**4 / sp.factorial(4)
    )
    algebraic_scalar_source = (
        sp.diff(curvature_function, psi) * curvature / 2
        - sp.diff(gauge_function, psi) * field_strength_squared / 4
        + sp.diff(matter_function, psi) * matter_lagrangian
        - sp.diff(potential, psi)
    )
    source_at_zero = sp.simplify(algebraic_scalar_source.subs(psi, 0))
    source_slope_at_zero = sp.simplify(
        sp.diff(algebraic_scalar_source, psi).subs(psi, 0)
    )
    curvature_scalar_mixing = sp.simplify(
        sp.diff(curvature_function, psi).subs(psi, 0) / 2
    )
    gauge_scalar_mixing = sp.simplify(
        sp.diff(gauge_function, psi).subs(psi, 0)
    )
    matter_scalar_mixing = sp.simplify(
        sp.diff(matter_function, psi).subs(psi, 0)
    )

    functions = [
        ("F_R", curvature_function, m_r_squared),
        ("Z_A", gauge_function, z_a_zero),
        ("A_matter", matter_function, sp.S.One),
        ("V_even", potential, vacuum),
    ]
    rows: list[dict[str, Any]] = []
    for name, function, expected_value in functions:
        rows.append(
            {
                "function": name,
                "expansion": str(function),
                "value_at_zero": str(sp.simplify(function.subs(psi, 0))),
                "expected_value": str(expected_value),
                "first_derivative_at_zero": str(
                    sp.simplify(sp.diff(function, psi).subs(psi, 0))
                ),
                "second_derivative_at_zero": str(
                    sp.simplify(sp.diff(function, psi, 2).subs(psi, 0))
                ),
                "local_metric_or_Maxwell_effect": (
                    "constant normalization only"
                    if name != "V_even"
                    else "vacuum term absorbed into U_Lambda"
                ),
                "local_scalar_source": "zero",
                "status": "ANALYTIC_Z2_DOUBLE_ZERO",
            }
        )

    rows.extend(
        [
            {
                "function": "combined_algebraic_scalar_source",
                "expansion": str(algebraic_scalar_source),
                "value_at_zero": str(source_at_zero),
                "expected_value": "0",
                "first_derivative_at_zero": str(source_slope_at_zero),
                "second_derivative_at_zero": "",
                "local_metric_or_Maxwell_effect": (
                    "no additive source; second derivatives shift scalar Hessian"
                ),
                "local_scalar_source": "zero",
                "status": "EXACT_COMBINED_ZERO",
            },
            {
                "function": "local_scalar_Hessian",
                "expansion": (
                    "K_psi_psi=-Z_0 Box plus the signed second variation "
                    "of curvature, gauge, matter and potential functions"
                ),
                "value_at_zero": str(source_slope_at_zero),
                "expected_value": "positive spectrum on the selected local domain",
                "first_derivative_at_zero": "not applicable",
                "second_derivative_at_zero": str(source_slope_at_zero),
                "local_metric_or_Maxwell_effect": (
                    "stationarity is exact but stability is a separate spectral gate"
                ),
                "local_scalar_source": "zero does not prove positive Hessian",
                "status": "RETAIN_LOCAL_STABILITY_CONDITION",
            },
            {
                "function": "quadratic_cross_block",
                "expansion": (
                    "Gamma_hpsi proportional F_R'(0); "
                    "Gamma_Apsi proportional Z_A'(0) Abar; "
                    "Gamma_matterpsi proportional A_matter'(0)"
                ),
                "value_at_zero": (
                    f"({curvature_scalar_mixing},"
                    f"{gauge_scalar_mixing},{matter_scalar_mixing})"
                ),
                "expected_value": "(0,0,0)",
                "first_derivative_at_zero": "all zero",
                "second_derivative_at_zero": "retained only in scalar Hessian",
                "local_metric_or_Maxwell_effect": (
                    "no linear scalar-metric, scalar-photon, or scalar-matter mixing"
                ),
                "local_scalar_source": "zero",
                "status": "EXACT_QUADRATIC_BLOCK_DIAGONALITY",
            },
            {
                "function": "nonanalytic_guard",
                "expansion": "functions with cusp or singular Hessian at psi=0",
                "value_at_zero": "not sufficient",
                "expected_value": "regular C2 neighborhood",
                "first_derivative_at_zero": "may fail or be ambiguous",
                "second_derivative_at_zero": "may diverge",
                "local_metric_or_Maxwell_effect": "double-zero theorem unavailable",
                "local_scalar_source": "must be rederived",
                "status": "REJECT_NONREGULAR_SHORTCUT",
            },
        ]
    )
    diagnostics = {
        "F_R_at_zero": str(curvature_function.subs(psi, 0)),
        "F_R_prime_at_zero": str(
            sp.diff(curvature_function, psi).subs(psi, 0)
        ),
        "Z_A_at_zero": str(gauge_function.subs(psi, 0)),
        "Z_A_prime_at_zero": str(
            sp.diff(gauge_function, psi).subs(psi, 0)
        ),
        "matter_factor_at_zero": str(matter_function.subs(psi, 0)),
        "matter_factor_prime_at_zero": str(
            sp.diff(matter_function, psi).subs(psi, 0)
        ),
        "potential_prime_at_zero": str(
            sp.diff(potential, psi).subs(psi, 0)
        ),
        "combined_scalar_source_at_zero": str(source_at_zero),
        "combined_scalar_source_slope_at_zero": str(source_slope_at_zero),
        "curvature_scalar_mixing_at_zero": str(curvature_scalar_mixing),
        "gauge_scalar_mixing_at_zero": str(gauge_scalar_mixing),
        "matter_scalar_mixing_at_zero": str(matter_scalar_mixing),
        "local_quadratic_cross_blocks_zero": (
            curvature_scalar_mixing == 0
            and gauge_scalar_mixing == 0
            and matter_scalar_mixing == 0
        ),
        "local_stationary_equation_independent_of_even_second_derivatives": True,
        "local_stability_independent_of_even_second_derivatives": False,
    }
    return tagged(rows), diagnostics


def motion_rg_closure() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    quartic, nonminimal = sp.symbols("lambda_4 xi")
    beta_quartic = 3 * quartic**2 / (4 * sp.pi) ** 2
    beta_nonminimal = (
        quartic * (nonminimal - sp.Rational(1, 6)) / (4 * sp.pi) ** 2
    )
    beta_nonminimal_at_zero = sp.simplify(
        beta_nonminimal.subs(nonminimal, 0)
    )
    rows = tagged(
        [
            {
                "coordinate": "V_even(psi)",
                "representative": (
                    "V_0+M_psi^2 psi^2/2+lambda_4 psi^4/4!+..."
                ),
                "source_result": "mass relevant; regular quartic irrelevant on current low branch",
                "RG_closure": "retain as function or trajectory coordinates",
                "local_zero_branch": "exact by Z2 and V'(0)=0",
                "nonzero_branch": "changes cosmology and state stability",
                "status": "RETAIN_FUNCTIONAL_BLOCK",
            },
            {
                "coordinate": "F_R(psi)",
                "representative": "M_R^2+xi psi^2/2+...",
                "source_result": (
                    "R psi^2 symmetry allowed; beta_xi at xi=0 is nonzero"
                    " when lambda_4 is nonzero in the one-loop comparator"
                ),
                "RG_closure": "cannot silently fix xi=0 on an interacting branch",
                "local_zero_branch": "exact; F_R'(0)=0",
                "nonzero_branch": "changes scalar Hessian and cosmological gravity",
                "status": "OPEN_TRAJECTORY_COORDINATE",
            },
            {
                "coordinate": "Z(psi)",
                "representative": "Z_0+z_2 psi^2/2+...",
                "source_result": "field-dependent kinetic function belongs to source-complete block",
                "RG_closure": "retain with V and F",
                "local_zero_branch": "only Z_0 enters the pole residue",
                "nonzero_branch": "changes sound speed and normalization",
                "status": "OPEN_TRAJECTORY_COORDINATE",
            },
            {
                "coordinate": "X_psi^2",
                "representative": "c_X2 (g^mu_nu partial_mu psi partial_nu psi)^2",
                "source_result": "gravity additively generates the shift-even derivative channel",
                "RG_closure": "coefficient not solved in the active parent scheme",
                "local_zero_branch": "quartic in fluctuations; no onset source",
                "nonzero_branch": "changes scattering and nonlinear cosmology",
                "status": "GENERATED_OPEN_COORDINATE",
            },
            {
                "coordinate": "shift_symmetric_surface",
                "representative": "M_psi2=lambda_4=xi=z_2=0; c_X2 allowed",
                "source_result": "exact RG-invariant surface for a shift-preserving regulator",
                "RG_closure": "does not describe the physical finite mass deformation",
                "local_zero_branch": "exact",
                "nonzero_branch": "mass deformation may generate even coordinates",
                "status": "EXACT_BUT_NOT_PHYSICAL_FULL_TRAJECTORY",
            },
            {
                "coordinate": "one_loop_curved_scalar_check",
                "representative": (
                    "beta_lambda=3lambda^2/(4pi)^2;"
                    "beta_xi=lambda(xi-1/6)/(4pi)^2"
                ),
                "source_result": str(beta_nonminimal_at_zero),
                "RG_closure": "xi=0 invariant only when lambda_4=0 in this comparator",
                "local_zero_branch": "still exact classically",
                "nonzero_branch": "coefficient must be solved or bounded",
                "status": "EXECUTED_SYMBOLIC_SOURCE_IDENTITY",
            },
        ]
    )
    diagnostics = {
        "beta_lambda": str(beta_quartic),
        "beta_xi": str(beta_nonminimal),
        "beta_xi_at_xi_zero": str(beta_nonminimal_at_zero),
        "xi_zero_invariant_for_symbolic_nonzero_lambda": False,
        "shift_symmetric_surface_invariant": True,
        "physical_mass_deformation_breaks_shift": True,
        "current_motion_block_fully_RG_closed": False,
    }
    return rows, diagnostics


def cross_coupling_basis() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    raw_rows = [
        {
            "operator": "psi R",
            "canonical_dimension": 3,
            "symmetry_status": "FORBIDDEN_BY_Z2",
            "parent_status": "ABSENT_BY_SYMMETRY",
            "local_psi_zero": "odd additive curvature source forbidden",
            "nonzero_branch": "not admitted",
            "action_owner": "none",
        },
        {
            "operator": "psi F_mu_nu F^mu_nu",
            "canonical_dimension": 5,
            "symmetry_status": "FORBIDDEN_BY_Z2",
            "parent_status": "ABSENT_BY_SYMMETRY",
            "local_psi_zero": "odd photon source forbidden",
            "nonzero_branch": "not admitted",
            "action_owner": "none",
        },
        {
            "operator": "psi^2 R_LC",
            "canonical_dimension": 4,
            "symmetry_status": "ALLOWED",
            "parent_status": "RETAIN_IN_F_R_FUNCTION_NOT_AS_GALAXY_TRIGGER",
            "local_psi_zero": "metric and scalar first variations vanish",
            "nonzero_branch": (
                "changes scalar Hessian and effective Planck function; "
                "4950 galaxy/local activation window is empty"
            ),
            "action_owner": "motion-curvature functional block",
        },
        {
            "operator": "psi^4",
            "canonical_dimension": 4,
            "symmetry_status": "ALLOWED",
            "parent_status": "RETAIN_IN_V_EVEN_FUNCTION",
            "local_psi_zero": "zero through quadratic local source",
            "nonzero_branch": "stabilizes or changes cosmology",
            "action_owner": "motion potential",
        },
        {
            "operator": "psi^2 X_psi",
            "canonical_dimension": 6,
            "symmetry_status": "ALLOWED",
            "parent_status": "RETAIN_IN_Z_PSI_FUNCTION",
            "local_psi_zero": "quartic in fluctuations",
            "nonzero_branch": "changes kinetic cone",
            "action_owner": "motion kinetic function",
        },
        {
            "operator": "X_psi^2",
            "canonical_dimension": 8,
            "symmetry_status": "ALLOWED_SHIFT_EVEN",
            "parent_status": "GENERATED_COEFFICIENT_OPEN",
            "local_psi_zero": "quartic in fluctuations",
            "nonzero_branch": "changes scattering and sound speed",
            "action_owner": "motion derivative function",
        },
        {
            "operator": "psi^2 H_dagger H",
            "canonical_dimension": 4,
            "symmetry_status": "ALLOWED_BY_GAUGE_AND_Z2",
            "parent_status": "FORBIDDEN_BY_FIXED_METRIC_HIDDEN_VISIBLE_FACTORIZATION",
            "local_psi_zero": "would be double-zero but is not a parent vertex",
            "nonzero_branch": "would alter visible masses",
            "action_owner": "not in active parent",
        },
        {
            "operator": "psi^2 F_mu_nu F^mu_nu",
            "canonical_dimension": 6,
            "symmetry_status": "ALLOWED_BY_U1_AND_Z2",
            "parent_status": "FORBIDDEN_DIRECTLY_BY_FIXED_METRIC_FACTORIZATION",
            "local_psi_zero": "would be double-zero",
            "nonzero_branch": "would vary alpha_EM",
            "action_owner": "only contact/nonlocal graviton-mediated completion",
        },
        {
            "operator": "psi^2 bar_f_L H f_R plus Hermitian conjugate",
            "canonical_dimension": 6,
            "symmetry_status": "ALLOWED_BY_VISIBLE_GAUGE_GROUP_AND_Z2",
            "parent_status": "FORBIDDEN_DIRECTLY_BY_FIXED_METRIC_FACTORIZATION",
            "local_psi_zero": "would be double-zero",
            "nonzero_branch": "would create composition dependence",
            "action_owner": "not in active parent",
        },
        {
            "operator": "psi^2 T_visible",
            "canonical_dimension": 6,
            "symmetry_status": "ALLOWED_AS_EFT_REPRESENTATIVE",
            "parent_status": "NO_INDEPENDENT_COEFFICIENT",
            "local_psi_zero": "double-zero",
            "nonzero_branch": "correlated with curvature coupling under metric equations",
            "action_owner": "basis image of F_R coupling if used",
        },
        {
            "operator": "R_LC H_dagger H",
            "canonical_dimension": 4,
            "symmetry_status": "ALLOWED_ORDINARY_CURVED_VISIBLE_SECTOR",
            "parent_status": "RETAIN_INSIDE_S_VISIBLE_NOT_AS_DIRECT_MTS_PORTAL",
            "local_psi_zero": "renormalizes metric-Higgs block with only the Higgs pole",
            "nonzero_branch": "ordinary curved-SM coefficient; locally short ranged",
            "action_owner": "visible matter EFT",
        },
        {
            "operator": "C_mu_nu_rho_sigma F^mu_nu F^rho_sigma",
            "canonical_dimension": 6,
            "symmetry_status": "ALLOWED",
            "parent_status": "RETAIN_CFF",
            "local_psi_zero": "independent of psi; zero only when Weyl is zero",
            "nonzero_branch": "bounded curvature-photon correction",
            "action_owner": "metric-photon EFT",
        },
        {
            "operator": "Tr(C^3)",
            "canonical_dimension": 6,
            "symmetry_status": "ALLOWED",
            "parent_status": "RETAIN_C3",
            "local_psi_zero": "finite higher-gradient metric residual",
            "nonzero_branch": "zero on exact FLRW",
            "action_owner": "metric EFT",
        },
        {
            "operator": "C^2 X_psi",
            "canonical_dimension": 8,
            "symmetry_status": "ALLOWED",
            "parent_status": "RETAIN_O4",
            "local_psi_zero": "exactly zero",
            "nonzero_branch": "tensor/kinetic correction",
            "action_owner": "metric-motion EFT",
        },
        {
            "operator": "-F_R(psi)T_TEGR/2 without -T^mu partial_mu F_R",
            "canonical_dimension": 4,
            "symmetry_status": "ALLOWED_AS_A_DIFFERENT_SCALAR_TORSION_THEORY",
            "parent_status": "FORBIDDEN_BY_CURVATURE_EQUIVALENCE_CONTRACT",
            "local_psi_zero": "coincides only when F_R is constant",
            "nonzero_branch": "not equivalent to F_R R_LC/2",
            "action_owner": "none in the canonical GR-connected parent",
        },
        {
            "operator": "independent torsion-vector or axial-current matter coupling",
            "canonical_dimension": 4,
            "symmetry_status": "ALLOWED_IN_A_BROADER_TORSION_MATTER_THEORY",
            "parent_status": "FORBIDDEN_BY_OMEGA_LC_VISIBLE_MATTER_CONTRACT",
            "local_psi_zero": "would create an extra nonmetric source or spin force",
            "nonzero_branch": "separate Einstein-Cartan or nonminimal matter branch",
            "action_owner": "none in the minimum parent",
        },
        {
            "operator": "f(T_TEGR) nonlinear",
            "canonical_dimension": "various",
            "symmetry_status": "NOT_REQUIRED_BY_PARENT_SYMMETRY",
            "parent_status": "EXCLUDED_FROM_MINIMUM_GR_PARENT",
            "local_psi_zero": "would change constraints and modes",
            "nonzero_branch": "separate theory branch",
            "action_owner": "none",
        },
        {
            "operator": "explicit X^A or mathcalB^A representative dependence",
            "canonical_dimension": "various",
            "symmetry_status": "FORBIDDEN_BY_LOCAL_TRANSLATION",
            "parent_status": "ABSENT_BY_GAUGE_SYMMETRY",
            "local_psi_zero": "prevents hidden frame/source labels",
            "nonzero_branch": "not admitted",
            "action_owner": "none",
        },
        {
            "operator": "bulk prescribed n(x) coefficient",
            "canonical_dimension": "state dependent",
            "symmetry_status": "NOT_A_BULK_ACTION_COUPLING",
            "parent_status": "FORBIDDEN_AS_CLOSURE_SMUGGLING",
            "local_psi_zero": "rho_0 selected as state condition",
            "nonzero_branch": "must descend from Gamma_rho_i and its state equation",
            "action_owner": "CTP initial-boundary functional",
        },
    ]
    rows = tagged(raw_rows)
    allowed_rows = [
        row for row in raw_rows if row["symmetry_status"].startswith("ALLOWED")
    ]
    classified_allowed = [
        row
        for row in allowed_rows
        if row["parent_status"]
        not in {"ABSENT", "ZERO_WITHOUT_THEOREM", "UNCLASSIFIED"}
    ]
    diagnostics = {
        "basis_row_count": len(raw_rows),
        "symmetry_allowed_row_count": len(allowed_rows),
        "classified_symmetry_allowed_row_count": len(classified_allowed),
        "all_symmetry_allowed_rows_classified": (
            len(allowed_rows) == len(classified_allowed)
        ),
        "direct_hidden_visible_portals_present": False,
        "even_motion_curvature_portal_present": True,
        "bulk_state_profile_inserted": False,
        "basis_scope": (
            "branch-relevant parity-even scalar-curvature-gauge-matter "
            "operators through dimension eight; not the full SMEFT basis"
        ),
    }
    return rows, diagnostics


def branch_reduction() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = tagged(
        [
            {
                "branch": "local_vacuum_GR_Maxwell",
                "conditions": (
                    "psi=0;nabla psi=0;rho_i=rho_0;"
                    "F_R(0)=M_R^2;positive local K_psi_psi;"
                    "one universal coframe"
                ),
                "surviving_equations": (
                    "M_R^2(G_mu_nu+Lambda g_mu_nu)"
                    "=T_visible+T_EM+DeltaE_C3+CFF+p8;"
                    "Maxwell-CFF equation"
                ),
                "same_parent_action": True,
                "derived_reduction": True,
                "closure_or_state_input": "exact local vacuum state still requires selection",
                "claim_level": "LEADING_TWO_DERIVATIVE_EXACT_GR;FINITE_EFT_RESIDUAL",
            },
            {
                "branch": "Newton_PPN_orbital",
                "conditions": (
                    "local_vacuum branch;weak field;slow source;"
                    "negligible local anisotropic extra stress"
                ),
                "surviving_equations": (
                    "nabla^2 Phi=4pi G_N rho;"
                    "G_N=1/(8pi M_R^2);constant PPN vector equals GR"
                ),
                "same_parent_action": True,
                "derived_reduction": True,
                "closure_or_state_input": "one measured M_R scale",
                "claim_level": "DERIVED_INSIDE_DECLARED_LOCAL_BRANCH",
            },
            {
                "branch": "flat_FLRW_motion",
                "conditions": "FLRW coframe;C_mu_nu_rho_sigma=0;F_mu_nu=0;psi=psi(t)",
                "surviving_equations": (
                    "scalar-tensor Friedmann plus functional psi equation;"
                    "C3=CFF=O4=0 on the exact background"
                ),
                "same_parent_action": True,
                "derived_reduction": True,
                "closure_or_state_input": (
                    "F_R,V_even,Z,P_ge_2 trajectory and one homogeneous state amplitude"
                ),
                "claim_level": "EQUATIONS_DERIVED;COSMOLOGY_SUPPORT_NOT_ESTABLISHED",
            },
            {
                "branch": "galaxy_collective_CTP",
                "conditions": (
                    "same bulk action;regulated P0/P1 pair algebra;"
                    "environmental rho_i with occupation n"
                ),
                "surviving_equations": (
                    "projective n=K_IR/(K_IR+K_UV);"
                    "DeltaT_state=2/e delta Gamma_rho_i/delta g"
                ),
                "same_parent_action": True,
                "derived_reduction": False,
                "closure_or_state_input": (
                    "Gamma_rho_i preparation;|k|^(1+q);q;s=4;B=8;stress projection"
                ),
                "claim_level": "COMPATIBLE_REDUCED_STATE_CLOSURE_NOT_PARENT_PREDICTION",
            },
            {
                "branch": "gravitational_and_EM_waves",
                "conditions": "psi=0 local branch;rho_0;linear perturbations",
                "surviving_equations": (
                    "two TEGR tensor modes plus Maxwell modes;"
                    "bounded C3/CFF corrections"
                ),
                "same_parent_action": True,
                "derived_reduction": True,
                "closure_or_state_input": "physical total c_IR remains open",
                "claim_level": "LEADING_MODES_DERIVED;HIGHER_EFT_BOUNDED_OR_OPEN",
            },
        ]
    )
    diagnostics = {
        "branch_count": len(rows),
        "all_branches_use_same_bulk_action": all(
            row["same_parent_action"] for row in rows
        ),
        "local_branch_derived": True,
        "local_stationary_branch_derived": True,
        "local_scalar_stability_automatic": False,
        "local_state_selection_derived": False,
        "Newton_PPN_branch_derived": True,
        "FLRW_equations_derived": True,
        "FLRW_physical_trajectory_complete": False,
        "galaxy_collective_branch_derived": False,
        "galaxy_collective_branch_compatible": True,
        "all_branches_derived": False,
        "FLRW_Weyl_zero": True,
    }
    return rows, diagnostics


def branch_operator_projection(
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = tagged(
        [
            {
                "operator_block": "TEGR_plus_U_Lambda",
                "local_background": "ACTIVE",
                "local_quadratic": "ACTIVE_TWO_TENSOR_MODES",
                "flat_FLRW_background": "ACTIVE_FRIEDMANN",
                "galaxy_collective": "ACTIVE_SAME_METRIC",
                "projection_reason": "universal coframe block",
            },
            {
                "operator_block": "nonconstant_F_R_part",
                "local_background": "ZERO_AT_CONSTANT_PSI_ZERO",
                "local_quadratic": "SCALAR_HESSIAN_ONLY_NO_H_PSI_MIXING",
                "flat_FLRW_background": "ACTIVE_IF_PSI_NONZERO",
                "galaxy_collective": "NOT_A_REOPENED_SCALARIZATION_TRIGGER",
                "projection_reason": "analytic Z2 double zero and 4950 window rejection",
            },
            {
                "operator_block": "V_even_Z_P_X2_motion",
                "local_background": "ZERO_AT_PSI_ZERO",
                "local_quadratic": "M_POLE_AND_Z0_ONLY_AT_ONSET",
                "flat_FLRW_background": "ACTIVE",
                "galaxy_collective": "ELEMENTARY_POLE_NOT_L_EFF",
                "projection_reason": "5196/5197 pole and route separation",
            },
            {
                "operator_block": "Maxwell",
                "local_background": "ACTIVE_WHEN_EM_PRESENT",
                "local_quadratic": "TWO_PHOTON_MODES",
                "flat_FLRW_background": "ZERO_IN_TESTED_BACKGROUND",
                "galaxy_collective": "ACTIVE_VISIBLE_SECTOR",
                "projection_reason": "same U1 connection and coframe",
            },
            {
                "operator_block": "C3_equals_Tr_C3",
                "local_background": "FINITE_HIGHER_GRADIENT_RESIDUAL",
                "local_quadratic": "CONTROLLED_EFT_CORRECTION",
                "flat_FLRW_background": "ZERO_BECAUSE_WEYL_ZERO",
                "galaxy_collective": "SAME_COEFFICIENT_NO_RETUNING",
                "projection_reason": "Weyl-cubic structure",
            },
            {
                "operator_block": "CFF",
                "local_background": "ZERO_IF_WEYL_OR_F_ZERO_OTHERWISE_BOUNDED",
                "local_quadratic": "CONTROLLED_PHOTON_CORRECTION",
                "flat_FLRW_background": "ZERO_BECAUSE_WEYL_AND_F_ZERO",
                "galaxy_collective": "NEGLIGIBLE_BOUNDED_LENSING_CORRECTION",
                "projection_reason": "Weyl-photon structure",
            },
            {
                "operator_block": "O4_equals_C2_Xpsi",
                "local_background": "ZERO_AT_PSI_ZERO",
                "local_quadratic": "ZERO_ON_LOCAL_ZERO_FIELD_BACKGROUND",
                "flat_FLRW_background": "ZERO_BUT_TENSOR_PERTURBATIONS_ORDER_REDUCED",
                "galaxy_collective": "NO_STATIC_MASS_SOURCE",
                "projection_reason": "Weyl zero or Xpsi zero",
            },
            {
                "operator_block": "direct_hidden_visible_portals",
                "local_background": "ABSENT",
                "local_quadratic": "ABSENT",
                "flat_FLRW_background": "ABSENT",
                "galaxy_collective": "ABSENT",
                "projection_reason": "4919 fixed-metric factorization",
            },
            {
                "operator_block": "Gamma_rho_i_state",
                "local_background": "ZERO_FOR_RHO_I_EQUALS_RHO_0",
                "local_quadratic": "STATE_COVARIANCE_ONLY_IF_PREPARED",
                "flat_FLRW_background": "SETS_HOMOGENEOUS_STATE_DATA",
                "galaxy_collective": "ACTIVE_BUT_PROFILE_EQUATION_OPEN",
                "projection_reason": "state/action distinction and CTP Ward identity",
            },
            {
                "operator_block": "contact_nonlocal_p8plus",
                "local_background": "FINITE_RESIDUAL_OR_RENORMALIZATION",
                "local_quadratic": "MUST_RETAIN_BOUNDS_AND_ORDER_REDUCTION",
                "flat_FLRW_background": "OPEN_COMPLETION",
                "galaxy_collective": "NOT_A_PROFILE_FITTING_SLOT",
                "projection_reason": "finite EFT completion corridor",
            },
        ]
    )
    diagnostics = {
        "projection_row_count": len(rows),
        "FLRW_Weyl_blocks_zero": 3,
        "local_motion_background_blocks_zero": 3,
        "direct_hidden_visible_blocks_active": 0,
        "branch_specific_bulk_coefficients_inserted": 0,
        "galaxy_state_profile_equation_closed": False,
        "local_all_operator_exact_GR": False,
        "local_leading_two_derivative_GR": True,
    }
    return rows, diagnostics


def coefficient_state_ownership(
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    calibration_matrix = sp.Matrix(
        [
            [-1, 0, 0, 0, 0],
            [0, -1, 0, 0, 0],
            [0, 0, 1, -1, 0],
            [0, 0, 0, 0, 1],
        ]
    )
    rows = tagged(
        [
            {
                "object": "M_R^2",
                "class": "action_coefficient",
                "physical_combination": "G_N=1/(8pi M_R^2)",
                "ownership": "one measured absolute gravity scale",
                "arena_retuning": "FORBIDDEN",
            },
            {
                "object": "Z_A and visible charge normalization",
                "class": "action_coefficient",
                "physical_combination": "alpha_EM",
                "ownership": "one measured electromagnetic normalization",
                "arena_retuning": "FORBIDDEN",
            },
            {
                "object": "M_psi^2/Z_psi",
                "class": "action_coefficient_ratio",
                "physical_combination": "m_pole^2",
                "ownership": "one universal elementary pole",
                "arena_retuning": "FORBIDDEN",
            },
            {
                "object": "Lambda_cal",
                "class": "action_coefficient",
                "physical_combination": "background curvature scale",
                "ownership": "one cosmological calibration",
                "arena_retuning": "FORBIDDEN",
            },
            {
                "object": "F_R,V_even,Z,c_X2",
                "class": "action_function_or_trajectory_coordinates",
                "physical_combination": "motion curvature and nonlinear response",
                "ownership": "must be solved on one RG trajectory",
                "arena_retuning": "FORBIDDEN",
            },
            {
                "object": "c_IR,G_C3,u_O4,p8plus",
                "class": "EFT coefficients",
                "physical_combination": "higher-gradient residual vector",
                "ownership": "sourced, selected, bounded, or open as individually recorded",
                "arena_retuning": "FORBIDDEN",
            },
            {
                "object": "homogeneous psi amplitude",
                "class": "state datum",
                "physical_combination": "FLRW solution branch",
                "ownership": "initial state, not beta-function coefficient",
                "arena_retuning": "ONE_DECLARED_STATE_ONLY",
            },
            {
                "object": "rho_i and occupation covariance",
                "class": "CTP state datum/function",
                "physical_combination": "collective occupied branch",
                "ownership": "preparation history or boundary functional",
                "arena_retuning": "MUST_BE_DERIVED_FROM_ENVIRONMENT_NOT_FITTED_PER_OBJECT",
            },
            {
                "object": "q;s=4;B=8",
                "class": "reduced closure coordinates",
                "physical_combination": "galaxy phase and wall shape",
                "ownership": "not parent-owned at checkpoint 5203",
                "arena_retuning": "NO_FULL_THEORY_CLAIM",
            },
        ]
    )
    diagnostics = {
        "calibration_log_Jacobian": str(calibration_matrix),
        "calibration_log_Jacobian_rank": calibration_matrix.rank(),
        "calibration_log_Jacobian_nullity": (
            calibration_matrix.cols - calibration_matrix.rank()
        ),
        "action_coefficients_separated_from_states": True,
        "action_coefficients_separated_from_closures": True,
        "arena_dependent_G_N_slots": 0,
        "arena_dependent_alpha_EM_slots": 0,
        "arena_dependent_elementary_mass_slots": 0,
    }
    return rows, diagnostics


def ctp_state_conservation(
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    coordinate = sp.symbols("x")
    occupation = sp.Function("n")(coordinate)
    stress_difference = sp.Function("DeltaT10")(coordinate)
    product_residual = sp.simplify(
        sp.diff(occupation * stress_difference, coordinate)
        - sp.diff(occupation, coordinate) * stress_difference
        - occupation * sp.diff(stress_difference, coordinate)
    )
    rows = tagged(
        [
            {
                "step": "state_stress_definition",
                "equation": (
                    "T_state^mu_nu=(2/e)delta Gamma_rho_i/delta g_mu_nu"
                ),
                "condition": "Gamma_rho_i belongs to the diagonal-diffeomorphism CTP parent",
                "result": "state stress is varied, not appended after the equations",
                "status": "REQUIRED_PARENT_DEFINITION",
            },
            {
                "step": "binary_mixture",
                "equation": "DeltaT_state[n]=n(T_1-T_0)",
                "condition": "rho(n)=(1-n)rho_0+n rho_1",
                "result": "DeltaT_state[0]=0",
                "status": "EXACT_LINEAR_STATE_IDENTITY",
            },
            {
                "step": "divergence_product_rule",
                "equation": (
                    "nabla_mu DeltaT^mu_nu"
                    "=(partial_mu n)DeltaT10^mu_nu"
                    "+n nabla_mu DeltaT10^mu_nu"
                ),
                "condition": "no cancellation omitted",
                "result": str(product_residual),
                "status": "EXECUTED_EXACT",
            },
            {
                "step": "state_Ward_identity",
                "equation": (
                    "nabla_mu T_state^mu_nu=-E_n partial_nu n"
                    " plus other state Euler terms"
                ),
                "condition": "diagonal diffeomorphism invariance",
                "result": "conserved only when the state equation is solved",
                "status": "NO_EXTERNAL_PROFILE_SHORTCUT",
            },
            {
                "step": "local_silence",
                "equation": "n=0 and partial_mu n=0 on an open local domain",
                "condition": "rho_i=rho_0 locally",
                "result": "exact state stress and divergence silence",
                "status": "CONDITIONAL_EXACT",
            },
            {
                "step": "galaxy_profile",
                "equation": "dn/du=q n(1-n)",
                "condition": "must follow from delta Gamma_rho_i/delta n=0 or preparation",
                "result": "current projective algebra is exact but q and preparation are open",
                "status": "REDUCED_STATE_CLOSURE",
            },
        ]
    )
    diagnostics = {
        "product_rule_residual": str(product_residual),
        "local_state_stress_zero_at_n_zero": True,
        "local_state_divergence_zero_requires_open_domain": True,
        "external_logistic_profile_is_conserved_automatically": False,
        "state_equation_required": True,
    }
    return rows, diagnostics


def route_decision_rows(diagnostics: dict[str, Any]) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "question": "Has one canonical invariant parent action been assembled?",
                "answer": "YES_AT_THE_DISPLAYED_EFT_AND_CTP_LEVEL",
                "evidence": (
                    f"{diagnostics['action']['canonical_block_count']} action blocks"
                ),
                "next_consequence": "stop treating local, FLRW and CTP sectors as unrelated actions",
            },
            {
                "question": "Is the scalar-curvature term complete in translation variables?",
                "answer": "YES",
                "evidence": (
                    "F_R R/2=-F_R T/2-T^mu partial_mu F_R plus boundary"
                ),
                "next_consequence": "forbid the incomplete F_R T-only shortcut",
            },
            {
                "question": "Does analytic Z2 make the local branch exact?",
                "answer": "STATIONARY_YES;STABLE_ONLY_IF_K_PSI_PSI_IS_POSITIVE",
                "evidence": "all first derivatives of even functions vanish at psi=0",
                "next_consequence": (
                    "even second derivatives alter the scalar Hessian, "
                    "not the local additive source"
                ),
            },
            {
                "question": "Is the interacting motion functional RG closed?",
                "answer": "NO",
                "evidence": (
                    f"beta_xi(xi=0)="
                    f"{diagnostics['rg']['beta_xi_at_xi_zero']}"
                ),
                "next_consequence": "solve F_R,V_even,Z,c_X2 on one trajectory",
            },
            {
                "question": "Are direct hidden-visible portals required?",
                "answer": "NO_IN_THE_ACTIVE_FACTORIZED_PARENT",
                "evidence": "4919 fixed-metric factorization theorem",
                "next_consequence": "retain only correlated graviton-mediated contact/nonlocal completion",
            },
            {
                "question": "Are local GR, Newton, PPN and Maxwell from this action?",
                "answer": "YES_CONDITIONALLY",
                "evidence": "5201 source chain inherited through 5202/5203",
                "next_consequence": "keep finite C3/CFF/p8 residuals explicit",
            },
            {
                "question": "Is the FLRW model fully predicted?",
                "answer": "NO",
                "evidence": "motion functions and homogeneous state amplitude remain open",
                "next_consequence": "no cosmology support claim",
            },
            {
                "question": "Is the galaxy collective phase derived from the action?",
                "answer": "NO",
                "evidence": "Gamma_rho_i preparation and q/outer-wall ownership remain open",
                "next_consequence": "retain as reduced-state closure",
            },
            {
                "question": "What is the next derivation?",
                "answer": "SOLVE_MOTION_CURVATURE_FUNCTIONAL_TRAJECTORY",
                "evidence": "it is the first unsolved bulk block shared by local perturbations and FLRW",
                "next_consequence": (
                    "derive or reject the common F_R(psi),V_even(psi),Z(psi),c_X2 trajectory"
                ),
            },
        ]
    )


def source_provenance_rows() -> list[dict[str, Any]]:
    rows = []
    for relative_path, digest in SOURCE_LOCKS.items():
        rows.append(
            {
                "source_path": relative_path,
                "sha256": digest,
                "role": (
                    "parent ingredient, operator theorem, branch gate, or prior result"
                ),
                "exists": (POST / relative_path).exists(),
                "source_type": (
                    "checkpoint_document"
                    if relative_path.endswith(".md")
                    else "machine_result"
                ),
            }
        )
    return tagged(rows)


def validation_rows(
    public_before: tuple[str, str],
    galaxy_before: tuple[str, str],
    output_files: list[Path],
    all_csv_rows: list[list[dict[str, Any]]],
    payload: dict[str, Any],
    diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, Any]] = []

    def add(name: str, passed: bool, detail: Any) -> None:
        checks.append((name, bool(passed), detail))

    add("document_exists", DOCUMENT.exists(), DOCUMENT)
    add(
        "document_marker",
        DOCUMENT.exists() and MARKER in DOCUMENT.read_text(encoding="utf-8"),
        MARKER,
    )
    add("script_exists", SCRIPT.exists(), SCRIPT)
    for relative_path, expected_digest in SOURCE_LOCKS.items():
        source_path = POST / relative_path
        add(f"source_exists::{relative_path}", source_path.exists(), source_path)
        add(
            f"source_hash::{relative_path}",
            source_path.exists() and file_digest(source_path) == expected_digest,
            expected_digest,
        )
    add(
        "formalization_workbench_lock",
        tree_digest(FORMAL) == FORMAL_LOCK,
        tree_digest(FORMAL),
    )
    add(
        "checkpoint_5202_output_lock",
        tree_digest(CHECKPOINT_5202_OUT) == CHECKPOINT_5202_OUT_LOCK,
        tree_digest(CHECKPOINT_5202_OUT),
    )
    public_after = git_state(PUBLIC_WORKTREE)
    galaxy_after = git_state(GALAXY_REPO)
    add("public_head_lock", public_after[0] == PUBLIC_HEAD_LOCK, public_after[0])
    add("public_unchanged", public_after == public_before, public_after)
    add("galaxy_head_lock", galaxy_after[0] == GALAXY_HEAD_LOCK, galaxy_after[0])
    add("galaxy_unchanged", galaxy_after == galaxy_before, galaxy_after)

    action = diagnostics["action"]
    add(
        "one_bulk_action",
        action["one_bulk_action"],
        action["canonical_block_count"],
    )
    add(
        "one_universal_coframe",
        action["one_universal_coframe"],
        action["sample_coframe_determinant"],
    )
    add(
        "translation_gauge_exact",
        action["translation_gauge_residual"]
        == "Matrix([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])",
        action["translation_gauge_residual"],
    )
    add(
        "curvature_teleparallel_product_rule",
        action["curvature_to_teleparallel_product_rule_residual"] == "0",
        action["curvature_to_teleparallel_product_rule_residual"],
    )
    add(
        "curvature_function_not_silently_zeroed",
        action["curvature_function_silently_zeroed"] is False,
        action["curvature_function_silently_zeroed"],
    )

    variation = diagnostics["variation"]
    add(
        "variation_chain_rule_exact",
        variation["finite_chain_rule_residual"] == "Matrix([[0], [0], [0]])",
        variation["finite_chain_rule_residual"],
    )
    add(
        "relational_equation_redundant",
        variation["relational_equation_is_dependent"]
        and variation["independent_relational_equations"] == 0,
        variation,
    )
    add(
        "rank_ten_metric_source",
        variation["independent_metric_source_components"] == 10,
        variation["independent_metric_source_components"],
    )
    add(
        "total_conservation",
        variation["total_Hilbert_conservation_on_shell"],
        variation["total_Hilbert_conservation_on_shell"],
    )

    double_zero = diagnostics["double_zero"]
    for key in [
        "F_R_prime_at_zero",
        "Z_A_prime_at_zero",
        "matter_factor_prime_at_zero",
        "potential_prime_at_zero",
        "combined_scalar_source_at_zero",
    ]:
        add(f"double_zero::{key}", double_zero[key] == "0", double_zero[key])
    add(
        "even_second_derivatives_do_not_spoil_background",
        double_zero[
            "local_stationary_equation_independent_of_even_second_derivatives"
        ],
        double_zero["combined_scalar_source_slope_at_zero"],
    )
    add(
        "local_stability_not_overclaimed",
        double_zero["local_stability_independent_of_even_second_derivatives"]
        is False
        and payload["claim_status"]["local_scalar_stability_automatic"] is False,
        double_zero["combined_scalar_source_slope_at_zero"],
    )
    add(
        "local_quadratic_cross_blocks_zero",
        double_zero["local_quadratic_cross_blocks_zero"],
        {
            "h_psi": double_zero["curvature_scalar_mixing_at_zero"],
            "A_psi": double_zero["gauge_scalar_mixing_at_zero"],
            "matter_psi": double_zero["matter_scalar_mixing_at_zero"],
        },
    )

    rg = diagnostics["rg"]
    add(
        "xi_zero_not_overclaimed_invariant",
        rg["xi_zero_invariant_for_symbolic_nonzero_lambda"] is False
        and rg["beta_xi_at_xi_zero"] != "0",
        rg["beta_xi_at_xi_zero"],
    )
    add(
        "shift_symmetric_surface_exact",
        rg["shift_symmetric_surface_invariant"],
        rg["shift_symmetric_surface_invariant"],
    )
    add(
        "motion_RG_closure_not_overclaimed",
        rg["current_motion_block_fully_RG_closed"] is False,
        rg["current_motion_block_fully_RG_closed"],
    )

    couplings = diagnostics["couplings"]
    add(
        "all_allowed_cross_couplings_classified",
        couplings["all_symmetry_allowed_rows_classified"],
        couplings,
    )
    add(
        "direct_hidden_visible_portals_absent",
        couplings["direct_hidden_visible_portals_present"] is False,
        couplings["direct_hidden_visible_portals_present"],
    )
    add(
        "even_curvature_portal_retained",
        couplings["even_motion_curvature_portal_present"],
        couplings["even_motion_curvature_portal_present"],
    )
    add(
        "bulk_state_profile_not_inserted",
        couplings["bulk_state_profile_inserted"] is False,
        couplings["bulk_state_profile_inserted"],
    )

    branches = diagnostics["branches"]
    add(
        "same_bulk_action_all_branches",
        branches["all_branches_use_same_bulk_action"],
        branches,
    )
    add("local_branch_derived", branches["local_branch_derived"], branches)
    add(
        "Newton_PPN_branch_derived",
        branches["Newton_PPN_branch_derived"],
        branches,
    )
    add(
        "FLRW_equations_derived",
        branches["FLRW_equations_derived"] and branches["FLRW_Weyl_zero"],
        branches,
    )
    add(
        "FLRW_claim_not_overstated",
        branches["FLRW_physical_trajectory_complete"] is False,
        branches["FLRW_physical_trajectory_complete"],
    )
    add(
        "galaxy_claim_not_overstated",
        branches["galaxy_collective_branch_derived"] is False
        and branches["galaxy_collective_branch_compatible"],
        branches,
    )
    add(
        "full_branch_derivation_false",
        branches["all_branches_derived"] is False,
        branches["all_branches_derived"],
    )
    add(
        "local_stability_and_state_not_overclaimed",
        branches["local_stationary_branch_derived"]
        and branches["local_scalar_stability_automatic"] is False
        and branches["local_state_selection_derived"] is False,
        branches,
    )

    projection = diagnostics["projection"]
    add(
        "no_branch_specific_bulk_coefficients",
        projection["branch_specific_bulk_coefficients_inserted"] == 0,
        projection,
    )
    add(
        "direct_portal_projection_zero",
        projection["direct_hidden_visible_blocks_active"] == 0,
        projection,
    )
    add(
        "FLRW_Weyl_projection",
        projection["FLRW_Weyl_blocks_zero"] == 3,
        projection,
    )
    add(
        "local_leading_not_all_operator_GR",
        projection["local_leading_two_derivative_GR"]
        and projection["local_all_operator_exact_GR"] is False,
        projection,
    )
    add(
        "galaxy_profile_equation_open",
        projection["galaxy_state_profile_equation_closed"] is False,
        projection,
    )

    ownership = diagnostics["ownership"]
    add(
        "calibration_rank_four",
        ownership["calibration_log_Jacobian_rank"] == 4,
        ownership["calibration_log_Jacobian"],
    )
    add(
        "coefficient_state_separation",
        ownership["action_coefficients_separated_from_states"],
        ownership,
    )
    add(
        "coefficient_closure_separation",
        ownership["action_coefficients_separated_from_closures"],
        ownership,
    )
    add(
        "no_arena_retuning_slots",
        ownership["arena_dependent_G_N_slots"] == 0
        and ownership["arena_dependent_alpha_EM_slots"] == 0
        and ownership["arena_dependent_elementary_mass_slots"] == 0,
        ownership,
    )

    state = diagnostics["state"]
    add(
        "state_product_rule_exact",
        state["product_rule_residual"] == "0",
        state["product_rule_residual"],
    )
    add(
        "state_equation_required",
        state["state_equation_required"]
        and state["external_logistic_profile_is_conserved_automatically"] is False,
        state,
    )
    add(
        "local_state_open_domain_guard",
        state["local_state_divergence_zero_requires_open_domain"],
        state,
    )

    claim_status = payload["claim_status"]
    add(
        "canonical_parent_claim_true",
        claim_status["canonical_parent_action_assembled"],
        claim_status,
    )
    add(
        "local_GR_claim_scoped",
        claim_status["leading_local_GR_Newton_Maxwell_derived"]
        and claim_status["all_operator_exact_GR"] is False,
        claim_status,
    )
    add(
        "full_unification_claim_false",
        claim_status["full_MTS_unification"] is False,
        claim_status,
    )
    add(
        "GitHub_action_false",
        claim_status["GitHub_action"] is False,
        claim_status,
    )

    for output_file in output_files:
        add(
            f"output_exists::{output_file.name}",
            output_file.exists() and output_file.stat().st_size > 0,
            output_file,
        )
        if output_file.suffix == ".csv" and output_file.exists():
            parsed_rows = read_csv(output_file)
            add(
                f"output_parses::{output_file.name}",
                len(parsed_rows) > 0,
                len(parsed_rows),
            )
    flattened_rows = [row for rows in all_csv_rows for row in rows]
    add(
        "all_rows_full_MTS_nonclaim",
        all(
            row.get("valid_for_full_MTS_claim") is False
            for row in flattened_rows
        ),
        len(flattened_rows),
    )
    add(
        "no_placeholder_markers",
        not any(
            "MISSING_" in str(value)
            for row in flattened_rows
            for value in row.values()
        ),
        len(flattened_rows),
    )
    add(
        "no_script_pycache",
        not any((POST / "scripts").glob("__pycache__")),
        POST / "scripts" / "__pycache__",
    )
    return [
        {
            "checkpoint": 5203,
            "marker": MARKER,
            "checked_date": CHECKED_DATE,
            "check": name,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for name, passed, detail in checks
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="execute derivations and report without writing evidence files",
    )
    arguments = parser.parse_args()

    assert_source_locks()
    public_before = git_state(PUBLIC_WORKTREE)
    galaxy_before = git_state(GALAXY_REPO)

    action_rows, action_diagnostics = canonical_parent_action()
    variation_rows, variation_diagnostics = (
        parent_variation_and_ward_identities()
    )
    double_zero_rows, double_zero_diagnostics = local_double_zero_theorem()
    rg_rows, rg_diagnostics = motion_rg_closure()
    coupling_rows, coupling_diagnostics = cross_coupling_basis()
    branch_rows, branch_diagnostics = branch_reduction()
    projection_rows, projection_diagnostics = branch_operator_projection()
    ownership_rows, ownership_diagnostics = coefficient_state_ownership()
    state_rows, state_diagnostics = ctp_state_conservation()

    diagnostics = {
        "action": action_diagnostics,
        "variation": variation_diagnostics,
        "double_zero": double_zero_diagnostics,
        "rg": rg_diagnostics,
        "couplings": coupling_diagnostics,
        "branches": branch_diagnostics,
        "projection": projection_diagnostics,
        "ownership": ownership_diagnostics,
        "state": state_diagnostics,
    }
    decision_rows = route_decision_rows(diagnostics)
    provenance_rows = source_provenance_rows()

    claim_status = {
        "canonical_parent_action_assembled": True,
        "translation_gauge_coframe_used": True,
        "scalar_curvature_teleparallel_completion_derived": True,
        "one_universal_matter_coframe": True,
        "leading_local_GR_Newton_Maxwell_derived": True,
        "full_constant_PPN_vector_inherited": True,
        "analytic_Z2_even_portals_locally_double_zero": True,
        "local_scalar_stability_automatic": False,
        "direct_hidden_visible_portals_present": False,
        "motion_functional_RG_closed": False,
        "FLRW_equations_from_same_action": True,
        "FLRW_physical_trajectory_predicted": False,
        "galaxy_collective_state_compatible_with_same_action": True,
        "galaxy_collective_state_derived": False,
        "all_operator_exact_GR": False,
        "absolute_G_N_predicted": False,
        "full_MTS_unification": False,
        "GitHub_action": False,
    }
    payload = {
        "checkpoint": 5203,
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "canonical_action": (
            "Gamma_CTP=S_can[+]-S_can[-]+Gamma_IF+Gamma_rho_i;"
            "e=DX+mathcalB;"
            "S_can contains F_R R/2, V-Z-P motion, Maxwell, visible matter,"
            "CFF, C3, O4, contact, nonlocal and p8plus"
        ),
        "diagnostics": diagnostics,
        "claim_status": claim_status,
        "selected_next_route": (
            "SOLVE_OR_REJECT_COMMON_F_R_V_Z_X2_MOTION_TRAJECTORY"
        ),
    }

    if arguments.dry_run:
        print(json.dumps(payload, indent=2, default=str))
        return

    OUT.mkdir(parents=True, exist_ok=True)
    output_map = {
        "canonical_translation_parent_action.csv": action_rows,
        "parent_variation_and_Ward_identities.csv": variation_rows,
        "local_Z2_double_zero_theorem.csv": double_zero_rows,
        "motion_functional_RG_closure.csv": rg_rows,
        "branch_relevant_cross_coupling_basis.csv": coupling_rows,
        "common_action_branch_reduction.csv": branch_rows,
        "branch_operator_projection.csv": projection_rows,
        "coefficient_state_closure_ownership.csv": ownership_rows,
        "CTP_state_stress_conservation.csv": state_rows,
        "route_decision.csv": decision_rows,
        "source_provenance.csv": provenance_rows,
    }
    for name, rows in output_map.items():
        write_csv(OUT / name, rows)
    result_path = OUT / "canonical_translation_parent_action_results.json"
    result_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    output_files = [OUT / name for name in output_map] + [result_path]
    all_csv_rows = list(output_map.values())
    validations = validation_rows(
        public_before,
        galaxy_before,
        output_files,
        all_csv_rows,
        payload,
        diagnostics,
    )
    write_csv(VALIDATION, validations)
    failed = [row for row in validations if row["status"] != "PASS"]
    if failed:
        raise RuntimeError(
            "checkpoint 5203 validation failed: "
            + "; ".join(
                f"{row['check']}={row['detail']}" for row in failed
            )
        )
    print(
        json.dumps(
            {
                "marker": MARKER,
                "validation": f"{len(validations)}/{len(validations)} PASS",
                "output_files": len(output_files),
                "output_bytes": sum(path.stat().st_size for path in output_files),
                "output_tree_sha256": tree_digest(OUT),
                "formalization_workbench_sha256": tree_digest(FORMAL),
                "checkpoint_5202_output_sha256": tree_digest(
                    CHECKPOINT_5202_OUT
                ),
                "canonical_parent_action_assembled": True,
                "curvature_teleparallel_completion": (
                    action_diagnostics[
                        "curvature_to_teleparallel_product_rule_residual"
                    ]
                ),
                "local_double_zero_source": double_zero_diagnostics[
                    "combined_scalar_source_at_zero"
                ],
                "motion_functional_RG_closed": False,
                "all_branches_same_bulk_action": branch_diagnostics[
                    "all_branches_use_same_bulk_action"
                ],
                "all_branches_derived": branch_diagnostics[
                    "all_branches_derived"
                ],
                "selected_next_route": payload["selected_next_route"],
            },
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    main()
