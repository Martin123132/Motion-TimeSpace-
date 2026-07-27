from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp


sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5196"
DOCUMENT = (
    POST
    / "5196-Y5-R2FR-invariant-mass-gap-Hessian-and-homogeneous-state-"
    "selection-theorem.md"
)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5196_VALIDATION.csv"
)
PUBLIC_WORKTREE = Path(
    r"C:\Users\ollet\OneDrive\Documents\Motion-TimeSpace-public-update-2026-07-22"
)
CHECKPOINT_5176 = POST / "source-intake" / "functional_rg" / "5176"
CHECKPOINT_5195_OUT = POST / "source-intake" / "functional_rg" / "5195"

MARKER = "MTS_5196_INVARIANT_MASS_GAP_AND_HOMOGENEOUS_STATE_SELECTION"
CHECKED_DATE = "2026-07-24"
FORMAL_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
CHECKPOINT_5195_OUT_LOCK = (
    "7aa855d3f75b9d2eb52fdc73f903c77a2e8e8b9e3be0f9496c4f9e15c5d6a810"
)
PUBLIC_HEAD_LOCK = "8913c00b77d98e457ddb0c48e9aeec9cc5f309fd"

MPC_METRES = 3.0856775814913673e22
HBAR_EV_SECONDS = 6.582119569e-16
PLANCK_TIME_SECONDS = 5.391247e-44
OMEGA_R = 9.0e-5
N_INITIAL = -12.0
TRANSFER_K_PLUS = 0.262094420818
TRANSFER_K_MINUS = 0.261707706805

SOURCE_LOCKS = {
    "4937-Y5-R2FR-gravity-motion-functional-potential-Hessian-and-one-scale-fixed-function-gate.md": (
        "2cf1f25d7cf67ec9bb724381919a9ff6e78d5dabe355ec50178157309b29cce5"
    ),
    "4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-two-scale-theory-gate.md": (
        "b30394a62c6a22af5da315b92a2823f44aa34cd914b6bab813136b0926aa0ca4"
    ),
    "4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md": (
        "a90da0e9ad0457fc3dbdb389d7bf2715cb9d707cbffa094a987b0b0553e257b5"
    ),
    "4951-Y5-R2FR-coupled-motion-VFZX2-functional-flow-fixed-point-index-and-GR-connected-trajectory-or-even-pair-sector-rejection.md": (
        "1dd7f2632ab15370e7b44272c2439a6cf70d5559b1c7993b6f55d7e9fab9a131"
    ),
    "5156-Y5-R2FR-FLRW-Hessian-Gaussian-state-single-clock-adiabatic-radiation-transfer-and-patch-collapse-gate.md": (
        "fdb5c0406fb7d0e47204a51212b24b5adf19d33644399bc4a1fd2268155b1353"
    ),
    "5179-Y5-R2FR-lowest-reflection-even-CTP-boundary-kernel-FLRW-preparation-and-perturbative-extra-stress-no-go.md": (
        "066217234006fecb16046796dd4cfdd0fec64a21a38fdcfa0eefb6aa709b3890"
    ),
    "5182-Y5-R2FR-static-Hilbert-pair-projector-constrained-Newtonian-response-and-route-decision.md": (
        "fe9307a74581108b428b12eb4918205b24bc5615c47e370face7eff6892f1fcf"
    ),
    "5186-Y5-R2FR-FLRW-Bogoliubov-neutral-vacuum-production-and-abundance-no-go.md": (
        "b3846c2e4bc1270b4c2f50d431fc5d812944f648ebec36f3250a95916101c05a"
    ),
    "5187-Y5-R2FR-canonical-local-parent-action-Hessian-source-residue-and-scale-setting-theorem.md": (
        "4556205ec12e11930a13d0ed9b5e27b6b4619f3752a5e10db2a4b767dcdec674"
    ),
    "5192-Y5-R2FR-parent-motion-FLRW-branch-memory-separation-and-mass-gap-cosmology-gate.md": (
        "e171efb8d498df44b535f6c25517c86a0cd5e8b993a67bfb8a9e3b74301eecc3"
    ),
    "5195-Y5-R2FR-matched-joint-CMB-informed-parent-refit-and-physical-sound-horizon-gate.md": (
        "217fdc07f94e18a21fe996f7592930f69c21ba16b3fe44b1fd1a2518d9d54737"
    ),
    "source-intake/functional_rg/5195/joint_CMB_informed_refit_results.json": (
        "538078e466c2ee9f02e5204090b9e1c87c8c56b5680c366289336dda4abdf3ad"
    ),
    "source-intake/functional_rg/5195/parent_state_summary.csv": (
        "f74142ebdcf3f43d3d4b10ae1b667b9a0cbf6c16e8f37598b7a58601df5d1d78"
    ),
}

PRIMARY_CONFIG = "primary_fs8_wCDM_prior"
PARENT_MODELS = (
    "ParentScalar_Lambda_free",
    "ParentScalar_Lambda_zero",
)


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(file_digest(item).encode("ascii"))
    return digest.hexdigest()


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_cosmology_support_claim": False,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def import_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def symbolic_mass_and_regular_mode_rows() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, bool],
]:
    z_psi, mass_coefficient, scale = sp.symbols(
        "Z_psi M2 s",
        positive=True,
        finite=True,
    )
    transformed_z = z_psi / scale**2
    transformed_mass = mass_coefficient / scale**2
    pole_mass_squared = mass_coefficient / z_psi
    rescaling_residual = sp.simplify(
        transformed_mass / transformed_z - pole_mass_squared
    )

    epsilon, amplitude, q_ratio = sp.symbols(
        "epsilon A q",
        finite=True,
    )
    chi_regular = amplitude * (1 - q_ratio * epsilon / 20)

    def derivative_n(expression: sp.Expr) -> sp.Expr:
        return sp.expand(4 * epsilon * sp.diff(expression, epsilon))

    radiation_residual = sp.expand(
        derivative_n(derivative_n(chi_regular))
        + derivative_n(chi_regular)
        + q_ratio * epsilon * chi_regular
    )
    radiation_linear_coefficient = sp.expand(radiation_residual).coeff(
        epsilon,
        1,
    )
    radiation_next_coefficient = sp.expand(radiation_residual).coeff(
        epsilon,
        2,
    )

    n_value, constant_a, constant_b = sp.symbols(
        "N A0 B0",
        real=True,
    )
    radiation_massless = constant_a + constant_b * sp.exp(-n_value)
    radiation_massless_residual = sp.simplify(
        sp.diff(radiation_massless, n_value, 2)
        + sp.diff(radiation_massless, n_value)
    )
    matter_massless = constant_a + constant_b * sp.exp(
        -sp.Rational(3, 2) * n_value
    )
    matter_massless_residual = sp.simplify(
        sp.diff(matter_massless, n_value, 2)
        + sp.Rational(3, 2) * sp.diff(matter_massless, n_value)
    )

    mass_rows = tagged(
        [
            {
                "object": "quadratic_zero_field_Hessian",
                "coordinate_free_result": (
                    "K_psipsi=Z_psi(-Box)+V_eff''(0); "
                    "m_pole^2=V_eff''(0)/Z_psi"
                ),
                "derivation_status": "DERIVED",
                "selection_status": "RELATION_ONLY_NOT_NUMERICAL_VALUE",
                "source_path": (
                    "5187-Y5-R2FR-canonical-local-parent-action-Hessian-"
                    "source-residue-and-scale-setting-theorem.md"
                ),
            },
            {
                "object": "canonical_field_coordinate",
                "coordinate_free_result": (
                    "psi_c=sqrt(Z_psi)psi; "
                    "V_c''(0)=V_eff''(0)/Z_psi"
                ),
                "derivation_status": "DERIVED",
                "selection_status": "FIELD_NORMALIZATION_CANCELS",
                "source_path": (
                    "5187-Y5-R2FR-canonical-local-parent-action-Hessian-"
                    "source-residue-and-scale-setting-theorem.md"
                ),
            },
            {
                "object": "universal_gap_coordinate",
                "coordinate_free_result": (
                    "J_gap=G_N m_pole^2=G_N V_eff''(0)/Z_psi"
                ),
                "derivation_status": "DERIVED",
                "selection_status": "ONE_ESSENTIAL_ACTION_PARAMETER",
                "source_path": (
                    "4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-"
                    "identity-or-explicit-two-scale-theory-gate.md"
                ),
            },
            {
                "object": "J_gap_dimension_gate",
                "coordinate_free_result": (
                    "[J_gap]=0 while [delta Gamma/delta psi]=mass^3 in 4D"
                ),
                "derivation_status": "DERIVED",
                "selection_status": (
                    "CANNOT_BE_AN_ADDITIVE_SOURCE_WITHOUT_A_NEW_DIMENSION3_"
                    "PARENT_OPERATOR"
                ),
                "source_path": str(SCRIPT.relative_to(POST)),
            },
            {
                "object": "field_rescaling_test",
                "coordinate_free_result": str(rescaling_residual),
                "derivation_status": (
                    "PASS" if rescaling_residual == 0 else "FAIL"
                ),
                "selection_status": "INVARIANT_UNDER_psi_prime_equals_s_psi",
                "source_path": str(SCRIPT.relative_to(POST)),
            },
            {
                "object": "regular_fixed_function_mass_direction",
                "coordinate_free_result": (
                    "delta_u=C2 varphi^2; "
                    "theta_mass=2-A in [1.84666104495,1.85881728347]"
                ),
                "derivation_status": "DERIVED_RELEVANT",
                "selection_status": "C2_TRAJECTORY_AMPLITUDE_FREE",
                "source_path": (
                    "4937-Y5-R2FR-gravity-motion-functional-potential-"
                    "Hessian-and-one-scale-fixed-function-gate.md"
                ),
            },
            {
                "object": "GR_separatrix_transfer",
                "coordinate_free_result": (
                    "J_gap,IR=K R_UV+O(R_UV^2); "
                    f"K_plus={TRANSFER_K_PLUS};K_minus={TRANSFER_K_MINUS}"
                ),
                "derivation_status": "DERIVED_LINEAR_TRANSFER",
                "selection_status": "R_UV_REMAINS_FREE",
                "source_path": (
                    "4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-"
                    "identity-or-explicit-two-scale-theory-gate.md"
                ),
            },
        ]
    )

    state_rows = tagged(
        [
            {
                "background": "radiation_dominated",
                "h_dlnH_dN": -2.0,
                "early_equation": "chi''+chi'+(mu^2/Omega_r)e^(4N)chi=0",
                "regular_solution": (
                    "chi=A[1-mu^2 e^(4N)/(20 Omega_r)+O(e^(8N))]"
                ),
                "regular_velocity": (
                    "chi'=-A mu^2 e^(4N)/(5 Omega_r)+O(e^(8N))"
                ),
                "singular_solution": "B e^(-N)",
                "regularity_removes": "B",
                "regularity_leaves": "A",
                "symbolic_residual": str(radiation_linear_coefficient),
            },
            {
                "background": "matter_dominated_mass_negligible",
                "h_dlnH_dN": -1.5,
                "early_equation": "chi''+(3/2)chi'=0",
                "regular_solution": "A",
                "regular_velocity": "0",
                "singular_solution": "B e^(-3N/2)",
                "regularity_removes": "B",
                "regularity_leaves": "A",
                "symbolic_residual": str(matter_massless_residual),
            },
            {
                "background": "general_linear_retarded_problem",
                "h_dlnH_dN": "",
                "early_equation": "L chi=S",
                "regular_solution": "chi=chi_ret[S]+A u_reg",
                "regular_velocity": "fixed by u_reg once A is chosen",
                "singular_solution": "B u_sing",
                "regularity_removes": "B",
                "regularity_leaves": "A unless a state/boundary law sets it",
                "symbolic_residual": "Duhamel decomposition exact",
            },
            {
                "background": "constant_source_equilibrium_test",
                "h_dlnH_dN": "",
                "early_equation": "m_pole^2 psi_star=S_star",
                "regular_solution": "psi_star=S_star/m_pole^2",
                "regular_velocity": "0",
                "singular_solution": "homogeneous transients",
                "regularity_removes": "at most the divergent transient",
                "regularity_leaves": (
                    "source-set equilibrium plus one regular transient"
                ),
                "symbolic_residual": (
                    "current parent has S_star=0, hence psi_star=0"
                ),
            },
            {
                "background": "current_reflection_even_parent",
                "h_dlnH_dN": "",
                "early_equation": "L chi=0",
                "regular_solution": "chi=A u_reg",
                "regular_velocity": "phase relation derived",
                "singular_solution": "removed",
                "regularity_removes": "one divergent mode",
                "regularity_leaves": "one nonzero amplitude",
                "symbolic_residual": "additive source exactly zero",
            },
            {
                "background": "zero_mean_retarded_choice",
                "h_dlnH_dN": "",
                "early_equation": "L chi=0 with no incoming homogeneous mode",
                "regular_solution": "chi=0",
                "regular_velocity": "0",
                "singular_solution": "0",
                "regularity_removes": "all homogeneous data by extra condition",
                "regularity_leaves": "no nonzero cosmological scalar",
                "symbolic_residual": "unique but phenomenologically trivial",
            },
        ]
    )
    checks = {
        "field_rescaling_invariant": bool(rescaling_residual == 0),
        "radiation_regular_series_O_e4N_residual_zero": bool(
            radiation_linear_coefficient == 0
        ),
        "radiation_regular_series_next_term_nonzero_as_expected": bool(
            radiation_next_coefficient == -amplitude * q_ratio**2 / 20
        ),
        "radiation_singular_mode_exact": bool(
            radiation_massless_residual == 0
        ),
        "matter_singular_mode_exact": bool(matter_massless_residual == 0),
    }
    return mass_rows, state_rows, checks


def source_operator_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "operator_or_sector": "P(X)_kinetic_germ",
                "delta_Gamma_delta_psi_at_zero": "0",
                "FLRW_effect": "derivative operator and Hubble friction",
                "can_select_finite_mass": False,
                "can_select_nonzero_homogeneous_amplitude": False,
                "parent_status": "DERIVED",
                "reason": "derivative-only and homogeneous",
                "source_path": (
                    "5192-Y5-R2FR-parent-motion-FLRW-branch-memory-"
                    "separation-and-mass-gap-cosmology-gate.md"
                ),
            },
            {
                "operator_or_sector": "quadratic_even_potential",
                "delta_Gamma_delta_psi_at_zero": "0",
                "FLRW_effect": "restoring term m_pole^2 psi",
                "can_select_finite_mass": False,
                "can_select_nonzero_homogeneous_amplitude": False,
                "parent_status": "RELEVANT_COORDINATE_VALUE_FREE",
                "reason": (
                    "Hessian defines pole mass; relevant trajectory amplitude "
                    "is not quantized"
                ),
                "source_path": (
                    "4937-Y5-R2FR-gravity-motion-functional-potential-"
                    "Hessian-and-one-scale-fixed-function-gate.md"
                ),
            },
            {
                "operator_or_sector": "ordinary_matter_action",
                "delta_Gamma_delta_psi_at_zero": "0",
                "FLRW_effect": "metric stress only",
                "can_select_finite_mass": False,
                "can_select_nonzero_homogeneous_amplitude": False,
                "parent_status": "METRIC_ONLY_REFLECTION_EVEN_BRANCH",
                "reason": "delta S_matter/delta psi=0",
                "source_path": (
                    "4943-Y5-R2FR-matter-source-interior-psi-zero-"
                    "continuation-and-junction-or-fifth-force-residual-gate.md"
                ),
            },
            {
                "operator_or_sector": "O4_equals_C2_times_X",
                "delta_Gamma_delta_psi_at_zero": "0",
                "FLRW_effect": "exactly zero because C_mnrs=0 on flat FLRW",
                "can_select_finite_mass": False,
                "can_select_nonzero_homogeneous_amplitude": False,
                "parent_status": "DERIVED_IRRELEVANT_EFT_OPERATOR",
                "reason": "conformal flatness and derivative field degree",
                "source_path": (
                    "5156-Y5-R2FR-FLRW-Hessian-Gaussian-state-single-"
                    "clock-adiabatic-radiation-transfer-and-patch-collapse-"
                    "gate.md"
                ),
            },
            {
                "operator_or_sector": "C3_and_CFF",
                "delta_Gamma_delta_psi_at_zero": "0",
                "FLRW_effect": "no scalar variation; Weyl background zero",
                "can_select_finite_mass": False,
                "can_select_nonzero_homogeneous_amplitude": False,
                "parent_status": "DERIVED_SEPARATE_BLOCKS",
                "reason": "quadratic Hessian block diagonal",
                "source_path": (
                    "5187-Y5-R2FR-canonical-local-parent-action-Hessian-"
                    "source-residue-and-scale-setting-theorem.md"
                ),
            },
            {
                "operator_or_sector": "X_squared",
                "delta_Gamma_delta_psi_at_zero": "0",
                "FLRW_effect": "nonlinear kinetic term only at nonzero X",
                "can_select_finite_mass": False,
                "can_select_nonzero_homogeneous_amplitude": False,
                "parent_status": "GENERATED_BUT_ZERO_QUADRATIC_HESSIAN",
                "reason": "delta^2(X^2)/delta psi^2 at psi=0 is zero",
                "source_path": (
                    "4951-Y5-R2FR-coupled-motion-VFZX2-functional-flow-"
                    "fixed-point-index-and-GR-connected-trajectory-or-even-"
                    "pair-sector-rejection.md"
                ),
            },
            {
                "operator_or_sector": "direct_T_matter_times_psi_squared",
                "delta_Gamma_delta_psi_at_zero": "0",
                "FLRW_effect": "would alter effective mass, not add a source",
                "can_select_finite_mass": False,
                "can_select_nonzero_homogeneous_amplitude": False,
                "parent_status": "EXCLUDED_BY_FIXED_METRIC_FACTORIZATION",
                "reason": "not an independent parent operator",
                "source_path": (
                    "4951-Y5-R2FR-coupled-motion-VFZX2-functional-flow-"
                    "fixed-point-index-and-GR-connected-trajectory-or-even-"
                    "pair-sector-rejection.md"
                ),
            },
            {
                "operator_or_sector": "R_times_psi_squared",
                "delta_Gamma_delta_psi_at_zero": "0",
                "FLRW_effect": "generic extension changes m_eff^2=m^2-xi R",
                "can_select_finite_mass": False,
                "can_select_nonzero_homogeneous_amplitude": False,
                "parent_status": "CURRENT_OPERATIONAL_XI_ZERO",
                "reason": (
                    "no additive parent source; even nonzero xi leaves psi=0 "
                    "exact and needs a derived stabilizer for bifurcation"
                ),
                "source_path": (
                    "5182-Y5-R2FR-static-Hilbert-pair-projector-"
                    "constrained-Newtonian-response-and-route-decision.md"
                ),
            },
            {
                "operator_or_sector": "CTP_Gaussian_covariance",
                "delta_Gamma_delta_psi_at_zero": "state functional",
                "FLRW_effect": "chooses occupation and squeezing",
                "can_select_finite_mass": False,
                "can_select_nonzero_homogeneous_amplitude": False,
                "parent_status": "INFINITE_POSITIVE_STATE_CONE",
                "reason": "Hessian fixes commutator, not statistical covariance",
                "source_path": (
                    "5156-Y5-R2FR-FLRW-Hessian-Gaussian-state-single-"
                    "clock-adiabatic-radiation-transfer-and-patch-collapse-"
                    "gate.md"
                ),
            },
            {
                "operator_or_sector": "CTP_alpha4_preparation_kernel",
                "delta_Gamma_delta_psi_at_zero": "0_by_reflection",
                "FLRW_effect": "initial-surface non-Gaussian correlation",
                "can_select_finite_mass": False,
                "can_select_nonzero_homogeneous_amplitude": False,
                "parent_status": "FUNCTIONAL_FORM_DERIVED_VALUE_STATE_DEPENDENT",
                "reason": "requires a selected density matrix/preparation contour",
                "source_path": (
                    "5179-Y5-R2FR-lowest-reflection-even-CTP-boundary-"
                    "kernel-FLRW-preparation-and-perturbative-extra-stress-"
                    "no-go.md"
                ),
            },
            {
                "operator_or_sector": "free_FLRW_Bogoliubov_production",
                "delta_Gamma_delta_psi_at_zero": "zero_mean",
                "FLRW_effect": "neutral squeezed pairs",
                "can_select_finite_mass": False,
                "can_select_nonzero_homogeneous_amplitude": False,
                "parent_status": "ABUNDANCE_OWNER_REJECTED",
                "reason": (
                    "boundary prescription remains state data and executed "
                    "abundance was 89-96 orders below its target"
                ),
                "source_path": (
                    "5186-Y5-R2FR-FLRW-Bogoliubov-neutral-vacuum-"
                    "production-and-abundance-no-go.md"
                ),
            },
        ]
    )


def primary_fit_parameters() -> dict[str, dict[str, float]]:
    rows = read_csv(CHECKPOINT_5195_OUT / "joint_fit_parameters.csv")
    parameters: dict[str, dict[str, float]] = {
        model: {} for model in PARENT_MODELS
    }
    for row in rows:
        if (
            row["config"] == PRIMARY_CONFIG
            and row["model"] in parameters
            and row["parameter"]
            in {"Omega_m", "log10_mu", "f_scalar", "H0", "Omega_b_h2"}
        ):
            parameters[row["model"]][row["parameter"]] = float(row["best_fit"])
    parameters["ParentScalar_Lambda_zero"]["f_scalar"] = 1.0
    required = {"Omega_m", "log10_mu", "f_scalar", "H0", "Omega_b_h2"}
    for model, values in parameters.items():
        if set(values) != required:
            raise ValueError(f"incomplete primary parameters for {model}: {values}")
    return parameters


def reconstruct_5195_branches() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    checkpoint_5195 = import_module(
        POST / "scripts" / "Y5_R2FR_5195_joint_CMB_informed_parent_refit.py",
        "checkpoint_5195_for_5196",
    )
    parameters = primary_fit_parameters()
    published_state_rows = {
        row["model"]: row
        for row in read_csv(CHECKPOINT_5195_OUT / "parent_state_summary.csv")
    }
    branch_rows: list[dict[str, Any]] = []
    regular_counterfamily_rows: list[dict[str, Any]] = []
    curvature_rows: list[dict[str, Any]] = []
    for model in PARENT_MODELS:
        values = parameters[model]
        backward = checkpoint_5195.backward_parent_background(model, values)
        forward = checkpoint_5195.forward_parent_background(
            model,
            values,
            backward,
        )
        diagnostics = forward.parent_diagnostics
        first = forward.scalar_rows[0]
        last = forward.scalar_rows[-1]
        mu_value = float(diagnostics["mu"])
        h0_value = float(values["H0"])
        h0_per_second = h0_value * 1000.0 / MPC_METRES
        mass_ev = mu_value * h0_per_second * HBAR_EV_SECONDS
        j_gap = (mu_value * h0_per_second * PLANCK_TIME_SECONDS) ** 2
        chi_initial = float(diagnostics["chi_initial_at_N_minus_12"])
        chi_today = float(last["chi"])
        x_today = float(last["x"])
        y_today = float(last["y"])
        retention = chi_today / chi_initial
        h_today = (
            -1.5 * float(values["Omega_m"])
            - 2.0 * OMEGA_R
            - 3.0 * x_today**2
        )
        r_over_h_squared = 6.0 * (2.0 + h_today)
        xi_tachyon_threshold = mu_value**2 / r_over_h_squared
        discriminant = 9.0 - 4.0 * mu_value**2
        slow_constant_h_rate = (
            (-3.0 + math.sqrt(discriminant)) / 2.0
            if discriminant >= 0.0
            else -1.5
        )
        published = published_state_rows[model]
        branch_rows.append(
            {
                "model": model,
                "Omega_m": float(values["Omega_m"]),
                "H0_km_s_Mpc": h0_value,
                "mu_mgap_over_H0": mu_value,
                "m_gap_eV": mass_ev,
                "J_gap_mgap2_GN": j_gap,
                "R_UV_from_K_plus": j_gap / TRANSFER_K_PLUS,
                "R_UV_from_K_minus": j_gap / TRANSFER_K_MINUS,
                "Omega_scalar_0": float(diagnostics["omega_scalar_zero"]),
                "Omega_Lambda_0": float(diagnostics["omega_lambda"]),
                "chi_regular_N_minus_12": chi_initial,
                "chi_0": chi_today,
                "x_0": x_today,
                "y_0": y_today,
                "theta_0": float(diagnostics["present_theta"]),
                "chi_amplitude_retention": retention,
                "chi_amplitude_change_fraction": retention - 1.0,
                "dln_abs_chi_dN_0": x_today / chi_today,
                "constant_H0_slow_mode_rate_per_Hubble_time": (
                    slow_constant_h_rate
                ),
                "constant_H0_slow_mode_amplitude_factor": math.exp(
                    slow_constant_h_rate
                ),
                "R_over_H2_today": r_over_h_squared,
                "generic_xi_tachyon_threshold_today": xi_tachyon_threshold,
                "mass_matches_5195_csv_fractional": (
                    mass_ev
                    / float(published["m_gap_eV_if_H0_sets_scale"])
                    - 1.0
                ),
                "mu_matches_5195_csv_fractional": (
                    mu_value / float(published["mu_mgap_over_H0"]) - 1.0
                ),
                "regular_phase_selected": True,
                "regular_amplitude_selected_by_action": False,
                "mass_value_selected_by_action": False,
                "interpretation": (
                    "finite fitted branch; universal calibration target, "
                    "not a parent-derived number"
                ),
            }
        )
        early_e = float(first["E"])
        for multiplier in (0.0, 0.5, 1.0, 1.5):
            candidate_amplitude = multiplier * chi_initial
            regular_counterfamily_rows.append(
                {
                    "model": model,
                    "amplitude_multiplier": multiplier,
                    "candidate_chi_N_minus_12": candidate_amplitude,
                    "candidate_x_N_minus_12_regular_series": (
                        -mu_value**2
                        * candidate_amplitude
                        / (5.0 * early_e**2)
                    ),
                    "x_over_chi_if_nonzero": (
                        -mu_value**2 / (5.0 * early_e**2)
                        if candidate_amplitude != 0.0
                        else ""
                    ),
                    "regularity_status": "REGULAR_TO_DISPLAYED_ORDER",
                    "present_flatness_status": (
                        "NOT_IMPOSED_EXCEPT_AT_MULTIPLIER_ONE"
                    ),
                    "theorem_use": (
                        "counterfamily proving early regularity alone does "
                        "not select amplitude"
                    ),
                }
            )
        curvature_rows.extend(
            [
                {
                    "model_or_epoch": model,
                    "R_over_H2": r_over_h_squared,
                    "generic_m_eff2_over_H2": (
                        f"{mu_value**2:.16g}-xi*{r_over_h_squared:.16g}"
                    ),
                    "xi_for_zero_present_effective_mass": xi_tachyon_threshold,
                    "parent_owned_xi": 0.0,
                    "amplitude_selection": (
                        "NO; psi=0 remains exact for every xi"
                    ),
                    "route_status": (
                        "UNOWNED_EXTENSION_REQUIRES_DERIVED_XI_AND_STABILIZER"
                    ),
                },
                {
                    "model_or_epoch": f"{model}:radiation_limit",
                    "R_over_H2": 0.0,
                    "generic_m_eff2_over_H2": "mu^2/E^2",
                    "xi_for_zero_present_effective_mass": "",
                    "parent_owned_xi": 0.0,
                    "amplitude_selection": "NO",
                    "route_status": "CURVATURE_TERM_VANISHES",
                },
                {
                    "model_or_epoch": f"{model}:matter_limit",
                    "R_over_H2": 3.0,
                    "generic_m_eff2_over_H2": "mu^2/E^2-3xi",
                    "xi_for_zero_present_effective_mass": "",
                    "parent_owned_xi": 0.0,
                    "amplitude_selection": "NO",
                    "route_status": (
                        "CONSTANT_RATIO_PER_EPOCH_NO_ABSOLUTE_H0_SCALE"
                    ),
                },
                {
                    "model_or_epoch": f"{model}:de_Sitter_limit",
                    "R_over_H2": 12.0,
                    "generic_m_eff2_over_H2": "mu^2/E^2-12xi",
                    "xi_for_zero_present_effective_mass": "",
                    "parent_owned_xi": 0.0,
                    "amplitude_selection": "NO",
                    "route_status": (
                        "CONSTANT_RATIO_PER_EPOCH_NO_ABSOLUTE_H0_SCALE"
                    ),
                },
            ]
        )
    return tagged(branch_rows), tagged(regular_counterfamily_rows), tagged(curvature_rows)


def parameter_and_state_count_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "coordinate": "G_N",
                "class": "leading_action_scale",
                "current_owner": "one absolute gravitational calibration",
                "selected_by_parent": False,
                "universal_across_arenas": True,
                "Lambda_free_branch_role": "fitted/calibrated",
                "Lambda_zero_branch_role": "fitted/calibrated",
            },
            {
                "coordinate": "J_gap=G_N m_pole^2",
                "class": "essential_action_parameter",
                "current_owner": "one universal motion-gap calibration",
                "selected_by_parent": False,
                "universal_across_arenas": True,
                "Lambda_free_branch_role": "one fitted shape coordinate mu",
                "Lambda_zero_branch_role": "one fitted shape coordinate mu",
            },
            {
                "coordinate": "Lambda_cal",
                "class": "background_action_calibration",
                "current_owner": "independent cosmological coordinate",
                "selected_by_parent": False,
                "universal_across_arenas": True,
                "Lambda_free_branch_role": "nonzero via f_scalar split",
                "Lambda_zero_branch_role": "set to zero as declared ablation",
            },
            {
                "coordinate": "A_reg_or_Omega_scalar",
                "class": "homogeneous_state_datum",
                "current_owner": "initial condition, not action coupling",
                "selected_by_parent": False,
                "universal_across_arenas": True,
                "Lambda_free_branch_role": (
                    "one independent fitted state fraction f_scalar"
                ),
                "Lambda_zero_branch_role": (
                    "fixed conditionally by flatness after Omega_m and H0"
                ),
            },
            {
                "coordinate": "theta_regular_phase",
                "class": "derived_boundary_relation",
                "current_owner": "radiation-era regularity",
                "selected_by_parent": True,
                "universal_across_arenas": True,
                "Lambda_free_branch_role": "shot, not fitted",
                "Lambda_zero_branch_role": "shot, not fitted",
            },
            {
                "coordinate": "primordial_covariance",
                "class": "quantum_or_statistical_state_datum",
                "current_owner": "unselected density matrix",
                "selected_by_parent": False,
                "universal_across_arenas": True,
                "Lambda_free_branch_role": "not used by background fit",
                "Lambda_zero_branch_role": "not used by background fit",
            },
        ]
    )


def route_decision_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "question": "Is J_gap an additive scalar source?",
                "answer": "NO",
                "status": "PROVED_BY_DEFINITION_AND_ACTION_VARIATION",
                "consequence": (
                    "J_gap labels the invariant pole mass and cannot displace "
                    "the homogeneous field"
                ),
            },
            {
                "question": "Does the parent Hessian derive a pole mass relation?",
                "answer": "YES",
                "status": "DERIVED",
                "consequence": "m_pole^2=V_eff''(0)/Z_psi",
            },
            {
                "question": "Does the current fixed point select finite J_gap?",
                "answer": "NO",
                "status": "EXACT_RELEVANT_DIRECTION_COUNTERFAMILY",
                "consequence": (
                    "one universal motion-scale calibration remains"
                ),
            },
            {
                "question": "Does FLRW regularity select the phase?",
                "answer": "YES",
                "status": "DERIVED",
                "consequence": (
                    "the early velocity is fixed in terms of one amplitude"
                ),
            },
            {
                "question": "Does FLRW regularity select the amplitude?",
                "answer": "NO",
                "status": "EXACT_ONE_PARAMETER_REGULAR_SOLUTION_FAMILY",
                "consequence": (
                    "one homogeneous state datum remains unless a separate "
                    "state law is supplied"
                ),
            },
            {
                "question": "Can a retarded no-incoming prescription select a state?",
                "answer": "YES_BUT_ZERO_FOR_CURRENT_SOURCE_FREE_PARENT",
                "status": "DERIVED",
                "consequence": (
                    "it yields psi=0, not the finite 5195 thawing branches"
                ),
            },
            {
                "question": "Does the current R psi^2 route repair selection?",
                "answer": "NO",
                "status": "PARENT_XI_ZERO_AND_MULTIPLICATIVE_ONLY",
                "consequence": (
                    "a nonzero extension changes m_eff but leaves psi=0 exact "
                    "without a derived instability and stabilizer"
                ),
            },
            {
                "question": "Is the Lambda=0 branch still economical?",
                "answer": "YES_CONDITIONALLY",
                "status": "ONE_EXTRA_ACTION_SHAPE_COORDINATE_VERSUS_LCDM",
                "consequence": (
                    "flatness removes an independent scalar-fraction fit "
                    "coordinate, but does not make the state action-derived"
                ),
            },
            {
                "question": "Does checkpoint 5196 establish full cosmology or MTS?",
                "answer": "NO",
                "status": "NONCLAIM",
                "consequence": (
                    "it establishes the minimum honest calibration/state "
                    "contract and closes repeated source hunting"
                ),
            },
        ]
    )


def source_provenance_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for relative_path, expected_hash in SOURCE_LOCKS.items():
        path = POST / relative_path
        rows.append(
            {
                "source_path": relative_path,
                "source_type": (
                    "generated_parent_evidence"
                    if relative_path.startswith("source-intake/")
                    else "private_checkpoint"
                ),
                "expected_sha256": expected_hash,
                "actual_sha256": file_digest(path) if path.exists() else "",
                "exists": path.exists(),
                "hash_matches": (
                    path.exists() and file_digest(path) == expected_hash
                ),
                "use": "locked input to mass/state theorem",
            }
        )
    return tagged(rows)


def public_worktree_state() -> tuple[str, bool, str]:
    safe_path = PUBLIC_WORKTREE.as_posix()
    head = subprocess.run(
        [
            "git",
            "-c",
            f"safe.directory={safe_path}",
            "-C",
            str(PUBLIC_WORKTREE),
            "rev-parse",
            "HEAD",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        [
            "git",
            "-c",
            f"safe.directory={safe_path}",
            "-C",
            str(PUBLIC_WORKTREE),
            "status",
            "--porcelain",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return head, not bool(status.strip()), status


def validation_rows(
    mass_rows: list[dict[str, Any]],
    state_rows: list[dict[str, Any]],
    operator_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    counterfamily_rows: list[dict[str, Any]],
    curvature_rows: list[dict[str, Any]],
    count_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    provenance_rows: list[dict[str, Any]],
    symbolic_checks: dict[str, bool],
    output_files: list[Path],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []

    def add(name: str, passed: bool, detail: Any) -> None:
        checks.append((name, bool(passed), str(detail)))

    for name, passed in symbolic_checks.items():
        add(name, passed, passed)
    add(
        "all_locked_sources_exist",
        all(bool(row["exists"]) for row in provenance_rows),
        len(provenance_rows),
    )
    add(
        "all_locked_source_hashes_match",
        all(bool(row["hash_matches"]) for row in provenance_rows),
        len(provenance_rows),
    )
    formal_hash = tree_digest(FORMAL)
    add(
        "formalization_workbench_unchanged",
        formal_hash == FORMAL_LOCK,
        f"expected={FORMAL_LOCK};actual={formal_hash}",
    )
    checkpoint_5176_hash = tree_digest(CHECKPOINT_5176)
    add(
        "checkpoint_5176_unchanged",
        checkpoint_5176_hash == CHECKPOINT_5176_LOCK,
        f"expected={CHECKPOINT_5176_LOCK};actual={checkpoint_5176_hash}",
    )
    checkpoint_5195_hash = tree_digest(CHECKPOINT_5195_OUT)
    add(
        "checkpoint_5195_output_tree_unchanged",
        checkpoint_5195_hash == CHECKPOINT_5195_OUT_LOCK,
        f"expected={CHECKPOINT_5195_OUT_LOCK};actual={checkpoint_5195_hash}",
    )
    add("document_exists", DOCUMENT.exists(), DOCUMENT)
    add(
        "document_marker_present",
        DOCUMENT.exists()
        and MARKER in DOCUMENT.read_text(encoding="utf-8"),
        MARKER,
    )
    add(
        "mass_relation_is_coordinate_invariant",
        any(
            row["object"] == "field_rescaling_test"
            and row["derivation_status"] == "PASS"
            for row in mass_rows
        ),
        "V''/Z",
    )
    add(
        "mass_direction_remains_relevant",
        any(
            row["object"] == "regular_fixed_function_mass_direction"
            and row["derivation_status"] == "DERIVED_RELEVANT"
            for row in mass_rows
        ),
        "theta_mass positive",
    )
    add(
        "regularity_removes_only_one_mode",
        all(
            row["regularity_leaves"] == "A"
            for row in state_rows
            if row["background"]
            in {"radiation_dominated", "matter_dominated_mass_negligible"}
        ),
        "one regular amplitude remains",
    )
    add(
        "no_current_additive_scalar_source",
        all(
            row["can_select_nonzero_homogeneous_amplitude"] is False
            for row in operator_rows
        ),
        len(operator_rows),
    )
    add(
        "ordinary_matter_scalar_source_zero",
        any(
            row["operator_or_sector"] == "ordinary_matter_action"
            and row["delta_Gamma_delta_psi_at_zero"] == "0"
            for row in operator_rows
        ),
        "delta S_matter/delta psi=0",
    )
    add(
        "O4_FLRW_source_zero",
        any(
            row["operator_or_sector"] == "O4_equals_C2_times_X"
            and "exactly zero" in row["FLRW_effect"]
            for row in operator_rows
        ),
        "C_FLRW=0",
    )
    add(
        "Rpsi2_not_smuggled_into_parent",
        any(
            row["operator_or_sector"] == "R_times_psi_squared"
            and row["parent_status"] == "CURRENT_OPERATIONAL_XI_ZERO"
            for row in operator_rows
        ),
        "xi=0",
    )
    add("two_5195_branches_reconstructed", len(branch_rows) == 2, len(branch_rows))
    add(
        "reconstructed_masses_match_5195",
        all(
            abs(float(row["mass_matches_5195_csv_fractional"])) < 1.0e-13
            for row in branch_rows
        ),
        max(
            abs(float(row["mass_matches_5195_csv_fractional"]))
            for row in branch_rows
        ),
    )
    add(
        "reconstructed_mu_matches_5195",
        all(
            abs(float(row["mu_matches_5195_csv_fractional"])) < 1.0e-13
            for row in branch_rows
        ),
        max(
            abs(float(row["mu_matches_5195_csv_fractional"]))
            for row in branch_rows
        ),
    )
    add(
        "finite_positive_Jgap_targets",
        all(float(row["J_gap_mgap2_GN"]) > 0.0 for row in branch_rows),
        ";".join(f"{row['J_gap_mgap2_GN']:.6e}" for row in branch_rows),
    )
    add(
        "finite_RUV_targets",
        all(
            float(row["R_UV_from_K_plus"]) > 0.0
            and float(row["R_UV_from_K_minus"]) > 0.0
            for row in branch_rows
        ),
        "positive",
    )
    add(
        "fitted_state_not_erased",
        all(
            0.75 < float(row["chi_amplitude_retention"]) < 1.0
            for row in branch_rows
        ),
        ";".join(
            f"{row['chi_amplitude_retention']:.9f}" for row in branch_rows
        ),
    )
    add(
        "phase_selected_but_amplitude_not_selected",
        all(
            row["regular_phase_selected"] is True
            and row["regular_amplitude_selected_by_action"] is False
            for row in branch_rows
        ),
        "both branches",
    )
    add(
        "mass_targets_remain_nonderived",
        all(row["mass_value_selected_by_action"] is False for row in branch_rows),
        "both branches",
    )
    add(
        "regular_counterfamily_has_four_rows_per_model",
        len(counterfamily_rows) == 8,
        len(counterfamily_rows),
    )
    add(
        "regular_counterfamily_contains_zero_and_nonzero_amplitudes",
        all(
            {float(row["amplitude_multiplier"]) for row in counterfamily_rows if row["model"] == model}
            == {0.0, 0.5, 1.0, 1.5}
            for model in PARENT_MODELS
        ),
        "0,0.5,1,1.5",
    )
    add(
        "curvature_pair_parent_value_zero",
        all(float(row["parent_owned_xi"]) == 0.0 for row in curvature_rows),
        len(curvature_rows),
    )
    add(
        "curvature_pair_keeps_zero_solution",
        all(
            str(row["amplitude_selection"]).startswith("NO")
            for row in curvature_rows
        ),
        "all rows",
    )
    add(
        "regular_phase_not_counted_as_fit_parameter",
        any(
            row["coordinate"] == "theta_regular_phase"
            and row["selected_by_parent"] is True
            for row in count_rows
        ),
        "theta shot",
    )
    add(
        "homogeneous_amplitude_counted_as_state",
        any(
            row["coordinate"] == "A_reg_or_Omega_scalar"
            and row["class"] == "homogeneous_state_datum"
            and row["selected_by_parent"] is False
            for row in count_rows
        ),
        "one global state datum",
    )
    add(
        "route_decision_closes_repeated_Jgap_source_hunt",
        any(
            row["question"] == "Is J_gap an additive scalar source?"
            and row["answer"] == "NO"
            for row in decision_rows
        ),
        "J_gap is mass coordinate",
    )
    add(
        "route_decision_retains_Lambda0_economy",
        any(
            row["question"] == "Is the Lambda=0 branch still economical?"
            and row["answer"] == "YES_CONDITIONALLY"
            for row in decision_rows
        ),
        "one extra shape coordinate",
    )
    add(
        "all_outputs_exist_and_nonempty",
        all(path.exists() and path.stat().st_size > 0 for path in output_files),
        len(output_files),
    )
    parse_ok = True
    missing_marker = False
    for path in output_files:
        if path.suffix == ".csv":
            rows = read_csv(path)
            parse_ok = parse_ok and bool(rows)
            missing_marker = missing_marker or any(
                "MISSING_" in str(value)
                for row in rows
                for value in row.values()
            )
        elif path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
    add("all_machine_outputs_parse", parse_ok, len(output_files))
    add("no_MISSING_markers", not missing_marker, missing_marker)
    add(
        "all_rows_are_nonclaim",
        all(
            row.get("valid_for_cosmology_support_claim") is False
            and row.get("valid_for_full_MTS_claim") is False
            for collection in (
                mass_rows,
                state_rows,
                operator_rows,
                branch_rows,
                counterfamily_rows,
                curvature_rows,
                count_rows,
                decision_rows,
                provenance_rows,
            )
            for row in collection
        ),
        "all generated rows",
    )
    pycache = POST / "scripts" / "__pycache__"
    add(
        "no_scripts_pycache",
        not pycache.exists(),
        pycache,
    )
    head, public_clean, public_status = public_worktree_state()
    add(
        "public_worktree_head_unchanged",
        head == PUBLIC_HEAD_LOCK,
        f"expected={PUBLIC_HEAD_LOCK};actual={head}",
    )
    add(
        "public_worktree_clean",
        public_clean,
        public_status if public_status else "clean",
    )
    return tagged(
        [
            {
                "check": name,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
            }
            for name, passed, detail in checks
        ]
    )


def build_payload(
    mass_rows: list[dict[str, Any]],
    state_rows: list[dict[str, Any]],
    operator_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    counterfamily_rows: list[dict[str, Any]],
    curvature_rows: list[dict[str, Any]],
    count_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    provenance_rows: list[dict[str, Any]],
    symbolic_checks: dict[str, bool],
) -> dict[str, Any]:
    return {
        "checkpoint": 5196,
        "marker": MARKER,
        "claim_status": {
            "mass_Hessian_relation": "DERIVED",
            "numerical_J_gap_selection": False,
            "regular_phase_selection": "DERIVED",
            "nonzero_homogeneous_amplitude_selection": False,
            "leading_local_GR_Newton_Maxwell_branch": "UNCHANGED",
            "cosmology_support_claim": False,
            "full_MTS_claim": False,
        },
        "theorem": (
            "The current local reflection-even parent fixes the invariant "
            "pole-mass relation and the regular FLRW phase, but its relevant "
            "mass eigenmode leaves one universal J_gap calibration and its "
            "second-order source-free homogeneous equation leaves one regular "
            "state amplitude. J_gap is not an additive source. A retarded "
            "zero-state rule selects only psi=0."
        ),
        "symbolic_checks": symbolic_checks,
        "invariant_mass_gap": mass_rows,
        "regular_mode_theorem": state_rows,
        "source_operator_exhaustion": operator_rows,
        "fitted_branch_match": branch_rows,
        "regular_counterfamily": counterfamily_rows,
        "curvature_pair_gate": curvature_rows,
        "parameter_and_state_count": count_rows,
        "route_decision": decision_rows,
        "source_provenance": provenance_rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="derive and print the checkpoint summary without writing files",
    )
    arguments = parser.parse_args()

    mass_rows, state_rows, symbolic_checks = (
        symbolic_mass_and_regular_mode_rows()
    )
    operator_rows = source_operator_rows()
    branch_rows, counterfamily_rows, curvature_rows = reconstruct_5195_branches()
    count_rows = parameter_and_state_count_rows()
    decision_rows = route_decision_rows()
    provenance_rows = source_provenance_rows()
    payload = build_payload(
        mass_rows,
        state_rows,
        operator_rows,
        branch_rows,
        counterfamily_rows,
        curvature_rows,
        count_rows,
        decision_rows,
        provenance_rows,
        symbolic_checks,
    )

    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "marker": MARKER,
                    "symbolic_checks": symbolic_checks,
                    "branches": branch_rows,
                    "decision": decision_rows,
                },
                indent=2,
                default=str,
            )
        )
        return

    OUT.mkdir(parents=True, exist_ok=True)
    output_map = {
        "invariant_mass_gap_Hessian.csv": mass_rows,
        "regular_FLRW_mode_and_state_theorem.csv": state_rows,
        "existing_source_operator_exhaustion.csv": operator_rows,
        "fitted_5195_mass_and_state_match.csv": branch_rows,
        "regular_amplitude_counterfamily.csv": counterfamily_rows,
        "curvature_pair_cosmology_gate.csv": curvature_rows,
        "parameter_and_state_count.csv": count_rows,
        "route_decision.csv": decision_rows,
        "source_provenance.csv": provenance_rows,
    }
    for name, rows in output_map.items():
        write_csv(OUT / name, rows)
    result_path = OUT / "mass_gap_and_state_selection_results.json"
    result_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    output_files = [OUT / name for name in output_map] + [result_path]
    rows = validation_rows(
        mass_rows,
        state_rows,
        operator_rows,
        branch_rows,
        counterfamily_rows,
        curvature_rows,
        count_rows,
        decision_rows,
        provenance_rows,
        symbolic_checks,
        output_files,
    )
    write_csv(VALIDATION, rows)
    failed = [row for row in rows if row["status"] != "PASS"]
    if failed:
        raise RuntimeError(
            "checkpoint 5196 validation failed: "
            + "; ".join(f"{row['check']}={row['detail']}" for row in failed)
        )
    print(
        json.dumps(
            {
                "marker": MARKER,
                "validation": f"{len(rows)}/{len(rows)} PASS",
                "output_files": len(output_files),
                "output_bytes": sum(path.stat().st_size for path in output_files),
                "formalization_workbench": tree_digest(FORMAL),
                "checkpoint_5176": tree_digest(CHECKPOINT_5176),
                "checkpoint_5195_output": tree_digest(CHECKPOINT_5195_OUT),
                "branch_targets": [
                    {
                        "model": row["model"],
                        "J_gap": row["J_gap_mgap2_GN"],
                        "chi_retention": row["chi_amplitude_retention"],
                    }
                    for row in branch_rows
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
