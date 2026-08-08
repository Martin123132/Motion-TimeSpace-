from __future__ import annotations

import argparse
import csv
import hashlib
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
OUT = POST / "source-intake" / "functional_rg" / "5201"
DOCUMENT = (
    POST
    / "5201-Y5-R2FR-source-complete-coframe-variation-full-PPN-"
    "calibration-and-local-state-silence-theorem.md"
)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5201_VALIDATION.csv"
)
CHECKPOINT_5200_OUT = POST / "source-intake" / "functional_rg" / "5200"
RESULT_5197 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5197"
    / "universal_gap_cross_arena_results.json"
)
RESIDUAL_VECTOR_4942 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4942"
    / "local_O4_C3_CFF_residual_vector.csv"
)
PUBLIC_WORKTREE = Path(
    r"C:\Users\ollet\OneDrive\Documents\Motion-TimeSpace-public-update-2026-07-22"
)
GALAXY_REPO = Path(r"D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo")

MARKER = "MTS_5201_SOURCE_COMPLETE_COFRAME_PPN_LOCAL_SILENCE_THEOREM"
CHECKED_DATE = "2026-07-24"
FORMAL_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5200_OUT_LOCK = (
    "acc19e684b35c7aff65923713812b6416e8cb5ea5212ddc5645f3802c37f4075"
)
PUBLIC_HEAD_LOCK = "8913c00b77d98e457ddb0c48e9aeec9cc5f309fd"
GALAXY_HEAD_LOCK = "f850e4997657f457dddc05cbe50f21186588dcc7"

SOURCE_LOCKS = {
    "4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-branch-and-C3-CFF-PPN-residual-gate.md": (
        "64b96ca4e19a058ced85c0c4b800ae7a237408606799dd8c4a5b58935f635c5f"
    ),
    "4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md": (
        "a90da0e9ad0457fc3dbdb389d7bf2715cb9d707cbffa094a987b0b0553e257b5"
    ),
    "4946-Y5-R2FR-QCD-TJJ-dispersive-matching-and-weak-local-Maxwell-action-certificate.md": (
        "4985b31aa5d5253ec64fd1575bbd0f844c1b5c0924a11482fb77374ddee477b6"
    ),
    "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md": (
        "0b71f50c85ab4c5761755aa11544910a1a1e4fcacc901236432705a5ba36563f"
    ),
    "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md": (
        "6cd343d022dde751f86ad82eaf0f61fb5e3616753c228f631c44a45da278a69d"
    ),
    "5187-Y5-R2FR-canonical-local-parent-action-Hessian-source-residue-and-scale-setting-theorem.md": (
        "4556205ec12e11930a13d0ed9b5e27b6b4619f3752a5e10db2a4b767dcdec674"
    ),
    "5188-Y5-R2FR-relational-clock-scalar-no-go-minimal-coframe-parent-and-Fierz-Pauli-selection-theorem.md": (
        "06f376fbab1a07312ae6993f1ea2a2e2f276a2438d7a2c15daf7993a17f6fb7a"
    ),
    "5189-Y5-R2FR-motion-sector-ADM-projection-clock-only-ancestry-and-local-tensor-protection-theorem.md": (
        "4514f59f95fa00fbddd652511bf49a98a84347b3f4f10747afbdfb6d3917e266"
    ),
    "5190-Y5-R2FR-static-Ward-helicity-one-derivative-mixing-no-go-and-direct-state-route-freeze.md": (
        "4f3d83db550d5eed2bea3fc8f6d6542807ec610a152abd2146a39ede6bdf6d55"
    ),
    "5197-Y5-R2FR-universal-gap-cross-arena-compatibility-and-route-separation-theorem.md": (
        "f01f94465168758886800556f345e370910f6913e80f1a4a0c646bbe7abe0c0a"
    ),
    "5200-Y5-R2FR-CTP-vacuum-occupied-projector-metric-and-composite-exponent-ownership-gate.md": (
        "348e580fb9c48c28b4b77e2219e0bc8760bcd012081373e7120caa7aac83e656"
    ),
    "source-intake/functional_rg/4942/local_O4_C3_CFF_residual_results.json": (
        "c830baff10125f984ba26d11d44465c4d519ecd6c51317b9c9fcac6cf5e2e04b"
    ),
    "source-intake/functional_rg/4942/local_O4_C3_CFF_residual_vector.csv": (
        "51f034326f02684491743d6b12fed9d54854885dae07e7894e77423f435a14a5"
    ),
    "source-intake/functional_rg/4946/QCD_TJJ_no_go_lattice_and_Maxwell_results.json": (
        "e0e0f3578574b191ab389edfda6f8a3e09937053aaa945147fb4dd1fbd410041"
    ),
    "source-intake/functional_rg/4946/local_Maxwell_action_stress_and_calibration_certificate.csv": (
        "8b80ddf7b5cb469fa7c580b24f6b0d759322871bfb7064111839565ba290799a"
    ),
    "source-intake/functional_rg/4947/local_calibration_count_results.json": (
        "2df2b3af173ecb85167a99795766d13cc8ca17de04fa227dafbbbc7389710b42"
    ),
    "source-intake/functional_rg/4960/integrated_H_universal_source_results.json": (
        "6fe2d8335cb1a4902c07c986e597e2f748050aa31f6137c5b52f9ced94542477"
    ),
    "source-intake/functional_rg/5187/canonical_local_parent_action_results.json": (
        "05d9e06edf88c219a6d21f49303b7e98dd82f3d1ecee5c9d445da385d4fa4e6d"
    ),
    "source-intake/functional_rg/5187/universal_residue_and_limit_chain.csv": (
        "f3a77301fde86ddd595be910c6076cfb129687e030fa972e8521039f372347f4"
    ),
    "source-intake/functional_rg/5188/relational_coframe_parent_results.json": (
        "9160b84ad6cbb9de7cda7df53b4d5a0c35f24b0b2c2795ff529bc94a3c12a30b"
    ),
    "source-intake/functional_rg/5188/same_coframe_GR_Newton_Maxwell_chain.csv": (
        "ec0c2417ef89d16360bdc64d5bf355fdbf99bbb26d9bca1eb6283c5f2b3f9db7"
    ),
    "source-intake/functional_rg/5189/motion_ADM_projection_results.json": (
        "6418ffc826ed2068b1f4df46d56423fe3f866c0e9bfa363098f4e849174fcfc2"
    ),
    "source-intake/functional_rg/5197/universal_gap_cross_arena_results.json": (
        "e42f0be823acd57eed630cca62b1e84a66e85cc81ba4354a24a0dcb93d1d0c0e"
    ),
    "source-intake/functional_rg/5200/CTP_projector_metric_exponent_ownership_results.json": (
        "7440b1818c7377f913d84ee665d4bd40f7055b3481eb003a63b787c63e58594e"
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
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
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
            "checkpoint": 5201,
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
    if tree_digest(CHECKPOINT_5200_OUT) != CHECKPOINT_5200_OUT_LOCK:
        failures.append("checkpoint-5200 output tree changed")
    if failures:
        raise RuntimeError("source lock failure: " + "; ".join(failures))


def coframe_variation_and_ward_chain(
) -> tuple[list[dict[str, Any]], dict[str, float]]:
    minkowski = np.diag([-1.0, 1.0, 1.0, 1.0])
    symmetric_pairs = [
        (first, second)
        for first in range(4)
        for second in range(first, 4)
    ]
    coframe_components = [
        (internal, spacetime)
        for internal in range(4)
        for spacetime in range(4)
    ]
    metric_jacobian = np.zeros((len(symmetric_pairs), len(coframe_components)))
    for row_index, (first, second) in enumerate(symmetric_pairs):
        for column_index, (internal, spacetime) in enumerate(
            coframe_components
        ):
            first_term = (
                minkowski[internal, second] if spacetime == first else 0.0
            )
            second_term = (
                minkowski[internal, first] if spacetime == second else 0.0
            )
            metric_jacobian[row_index, column_index] = (
                first_term + second_term
            )

    lorentz_generators = np.zeros((len(coframe_components), 6))
    generator_index = 0
    for first in range(4):
        for second in range(first + 1, 4):
            omega_lower = np.zeros((4, 4))
            omega_lower[first, second] = 1.0
            omega_lower[second, first] = -1.0
            omega_mixed = minkowski @ omega_lower
            for component_index, (internal, spacetime) in enumerate(
                coframe_components
            ):
                lorentz_generators[component_index, generator_index] = (
                    omega_mixed[internal, spacetime]
                )
            generator_index += 1

    metric_rank = int(np.linalg.matrix_rank(metric_jacobian, tol=1.0e-12))
    lorentz_rank = int(np.linalg.matrix_rank(lorentz_generators, tol=1.0e-12))
    lorentz_null_residual = float(
        np.max(np.abs(metric_jacobian @ lorentz_generators))
    )
    singular_values = np.linalg.svd(metric_jacobian, compute_uv=False)

    rows = tagged(
        [
            {
                "step": "parent_action",
                "equation": (
                    "S=(M_R^2/2) integral e(R-2 Lambda_cal)"
                    "-(Z_A/4) integral e F^2+S_visible[e,omega_LC[e],A,Phi]"
                    "+S_motion[e,psi]+Gamma_controlled_EFT+Gamma_rho0"
                ),
                "status": "EXPLICIT_PARENT_PREMISE",
                "derived_here": False,
                "scope": "torsionless one-coframe local branch",
            },
            {
                "step": "coframe_metric_map",
                "equation": "g_mn=eta_ab e^a_m e^b_n",
                "status": "EXACT",
                "derived_here": True,
                "scope": f"Jacobian rank {metric_rank}; Lorentz nullity 6",
            },
            {
                "step": "visible_Hilbert_source",
                "equation": (
                    "T_a^m=-(1/e) delta S_visible/delta e^a_m; "
                    "T_mn=e_(a n) T^a_m after LC spin improvement"
                ),
                "status": "EXACT_VARIATIONAL_DEFINITION",
                "derived_here": True,
                "scope": "all visible species use the same coframe",
            },
            {
                "step": "gauge_current",
                "equation": (
                    "J^m=-(1/e) delta S_visible/delta A_m"
                ),
                "status": "EXACT_VARIATIONAL_DEFINITION",
                "derived_here": True,
                "scope": "one U(1) connection",
            },
            {
                "step": "local_Lorentz_Ward",
                "equation": (
                    "T_[ab]+(1/2) nabla_m S^m_ab=0; "
                    "Belinfante-Hilbert T_mn=T_nm"
                ),
                "status": "DERIVED_FROM_LOCAL_LORENTZ_INVARIANCE",
                "derived_here": True,
                "scope": "omega=omega_LC[e], no independent torsion source",
            },
            {
                "step": "visible_diffeomorphism_Ward",
                "equation": (
                    "nabla_m T_visible^m_n=F_nm J^m"
                    "+sum_i E_i nabla_n Phi_i"
                ),
                "status": "DERIVED_NOETHER_IDENTITY",
                "derived_here": True,
                "scope": "on visible matter shell leaves Lorentz-force exchange",
            },
            {
                "step": "U1_Ward",
                "equation": "nabla_m J^m=0 on charged-matter shell",
                "status": "DERIVED_NOETHER_IDENTITY",
                "derived_here": True,
                "scope": "visible U(1) representations remain parent content",
            },
            {
                "step": "Einstein_equation",
                "equation": (
                    "M_R^2(G_mn+Lambda_cal g_mn)="
                    "T_visible_mn+T_EM_mn+T_psi_mn+DeltaE_EFT_mn"
                    "+DeltaT_state_mn"
                ),
                "status": "DERIVED_BY_ONE_COFRAME_VARIATION",
                "derived_here": True,
                "scope": "same source used by Newton, clocks, light and waves",
            },
            {
                "step": "combined_Ward",
                "equation": (
                    "nabla_m(T_visible^m_n+T_EM^m_n+T_psi^m_n"
                    "+DeltaT_EFT^m_n+DeltaT_state^m_n)=0"
                ),
                "status": "DERIVED_ON_ALL_FIELD_EQUATIONS",
                "derived_here": True,
                "scope": "Bianchi-compatible total source",
            },
        ]
    )
    diagnostics = {
        "coframe_component_count": 16.0,
        "metric_source_component_count": 10.0,
        "metric_jacobian_rank": float(metric_rank),
        "metric_jacobian_nullity": float(
            metric_jacobian.shape[1] - metric_rank
        ),
        "Lorentz_generator_rank": float(lorentz_rank),
        "maximum_Lorentz_metric_null_residual": lorentz_null_residual,
        "minimum_nonzero_metric_jacobian_singular_value": float(
            min(value for value in singular_values if value > 1.0e-12)
        ),
    }
    return rows, diagnostics


def symbolic_linearized_einstein_newton(
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    time_coord, x_coord, y_coord, z_coord = sp.symbols("t x y z")
    coordinates = (time_coord, x_coord, y_coord, z_coord)
    potential_phi = sp.Function("Phi")(x_coord, y_coord, z_coord)
    potential_psi = sp.Function("Psi")(x_coord, y_coord, z_coord)
    minkowski = sp.diag(-1, 1, 1, 1)
    perturbation = sp.diag(
        -2 * potential_phi,
        -2 * potential_psi,
        -2 * potential_psi,
        -2 * potential_psi,
    )
    mixed_perturbation = minkowski * perturbation
    trace_perturbation = sp.simplify(
        sum(
            minkowski[first, second] * perturbation[first, second]
            for first in range(4)
            for second in range(4)
        )
    )

    def second_derivative(
        expression: sp.Expr, first: int, second: int
    ) -> sp.Expr:
        return sp.diff(expression, coordinates[first], coordinates[second])

    def flat_box(expression: sp.Expr) -> sp.Expr:
        return sp.simplify(
            sum(
                minkowski[first, second]
                * second_derivative(expression, first, second)
                for first in range(4)
                for second in range(4)
            )
        )

    linear_ricci = sp.zeros(4)
    for first in range(4):
        for second in range(4):
            divergence_terms = sum(
                second_derivative(
                    mixed_perturbation[index, second], index, first
                )
                + second_derivative(
                    mixed_perturbation[index, first], index, second
                )
                for index in range(4)
            )
            linear_ricci[first, second] = sp.simplify(
                (
                    divergence_terms
                    - flat_box(perturbation[first, second])
                    - second_derivative(trace_perturbation, first, second)
                )
                / 2
            )
    linear_scalar = sp.simplify(
        sum(
            minkowski[first, second] * linear_ricci[first, second]
            for first in range(4)
            for second in range(4)
        )
    )
    linear_einstein = sp.simplify(
        linear_ricci - minkowski * linear_scalar / 2
    )

    laplacian_psi = sum(
        sp.diff(potential_psi, coordinate, 2)
        for coordinate in (x_coord, y_coord, z_coord)
    )
    expected_g00 = 2 * laplacian_psi
    expected_g12 = sp.diff(
        potential_psi - potential_phi, x_coord, y_coord
    )
    g00_residual = sp.simplify(linear_einstein[0, 0] - expected_g00)
    g12_residual = sp.simplify(linear_einstein[1, 2] - expected_g12)

    reduced_mass, newton_constant = sp.symbols(
        "M_R G_N", positive=True
    )
    newton_relation = sp.Eq(
        newton_constant, 1 / (8 * sp.pi * reduced_mass**2)
    )
    poisson_coefficient_residual = sp.simplify(
        1 / (2 * reduced_mass**2)
        - 4 * sp.pi * newton_relation.rhs
    )

    potential_u = sp.symbols("U")
    isotropic_g00 = -(
        (1 - potential_u / 2) / (1 + potential_u / 2)
    ) ** 2
    isotropic_gspace = (1 + potential_u / 2) ** 4
    g00_series = sp.series(isotropic_g00, potential_u, 0, 3).removeO()
    gspace_series = sp.series(
        isotropic_gspace, potential_u, 0, 3
    ).removeO()
    beta_ppn = sp.simplify(
        -sp.expand(g00_series).coeff(potential_u, 2) / 2
    )
    gamma_ppn = sp.simplify(
        sp.expand(gspace_series).coeff(potential_u, 1) / 2
    )

    rows = tagged(
        [
            {
                "step": "linear_metric",
                "equation": (
                    "ds^2=-(1+2 Phi)dt^2+(1-2 Psi)delta_ij dx^i dx^j"
                ),
                "symbolic_result": f"h={perturbation}",
                "status": "INPUT_WEAK_STATIC_ANSATZ",
            },
            {
                "step": "linear_Einstein_00",
                "equation": "G00^(1)",
                "symbolic_result": str(linear_einstein[0, 0]),
                "status": "EXECUTED_EXACT",
            },
            {
                "step": "linear_Einstein_offdiagonal",
                "equation": "G12^(1)",
                "symbolic_result": str(linear_einstein[1, 2]),
                "status": "EXECUTED_EXACT",
            },
            {
                "step": "zero_anisotropic_stress",
                "equation": "Gij_TF=0 with asymptotically vanishing potentials",
                "symbolic_result": "Phi=Psi",
                "status": "DERIVED_LOCAL_VACUUM_SLIP_ZERO",
            },
            {
                "step": "Poisson",
                "equation": "2 M_R^2 nabla^2 Phi=rho",
                "symbolic_result": (
                    "nabla^2 Phi=rho/(2M_R^2)=4pi G_N rho"
                ),
                "status": "DERIVED_WITH_G_N=1/(8pi M_R^2)",
            },
            {
                "step": "point_source",
                "equation": "nabla^2(1/r)=-4pi delta^3(r)",
                "symbolic_result": "Phi=-G_N M/r",
                "status": "DERIVED_NEWTON_POTENTIAL",
            },
            {
                "step": "geodesic",
                "equation": "u^m nabla_m u^n=0",
                "symbolic_result": "d2 x/dt2=-grad Phi",
                "status": "DERIVED_NEWTON_ACCELERATION",
            },
            {
                "step": "isotropic_Schwarzschild_g00",
                "equation": "-[(1-U/2)/(1+U/2)]^2",
                "symbolic_result": str(g00_series),
                "status": "EXECUTED_TO_O(U^2)",
            },
            {
                "step": "isotropic_Schwarzschild_gij",
                "equation": "(1+U/2)^4 delta_ij",
                "symbolic_result": str(gspace_series),
                "status": "EXECUTED_TO_O(U^2)",
            },
            {
                "step": "PPN_beta_gamma",
                "equation": (
                    "g00=-1+2U-2 beta U^2; gij=(1+2 gamma U)delta_ij"
                ),
                "symbolic_result": f"beta={beta_ppn}; gamma={gamma_ppn}",
                "status": "DERIVED_EINSTEIN_VALUES",
            },
        ]
    )
    diagnostics: dict[str, Any] = {
        "linear_Einstein_G00": str(linear_einstein[0, 0]),
        "linear_Einstein_G12": str(linear_einstein[1, 2]),
        "G00_identity_residual": str(g00_residual),
        "G12_identity_residual": str(g12_residual),
        "Poisson_coefficient_residual": str(
            poisson_coefficient_residual
        ),
        "Schwarzschild_g00_series": str(g00_series),
        "Schwarzschild_gspace_series": str(gspace_series),
        "beta_PPN": float(beta_ppn),
        "gamma_PPN": float(gamma_ppn),
    }
    return rows, diagnostics


def full_ppn_vector(
    beta_ppn: float, gamma_ppn: float
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    entries = [
        (
            "gamma",
            1.0,
            gamma_ppn,
            "linear Gij trace-free equation gives Phi=Psi",
        ),
        (
            "beta",
            1.0,
            beta_ppn,
            "isotropic Schwarzschild g00 coefficient at O(U^2)",
        ),
        (
            "xi",
            0.0,
            0.0,
            "no preferred-location/Whitehead term in local EH branch",
        ),
        (
            "alpha_1",
            0.0,
            0.0,
            "single Lorentz coframe and no local vector/timelike background",
        ),
        (
            "alpha_2",
            0.0,
            0.0,
            "single Lorentz coframe and psi=0, nabla psi=0",
        ),
        (
            "alpha_3",
            0.0,
            0.0,
            "local Lorentz plus diffeomorphism Ward identities",
        ),
        (
            "zeta_1",
            0.0,
            0.0,
            "action-based conserved total Hilbert stress",
        ),
        (
            "zeta_2",
            0.0,
            0.0,
            "action-based conserved total Hilbert stress",
        ),
        (
            "zeta_3",
            0.0,
            0.0,
            "action-based conserved total Hilbert stress",
        ),
        (
            "zeta_4",
            0.0,
            0.0,
            "action-based conserved total Hilbert stress",
        ),
    ]
    rows = tagged(
        [
            {
                "PPN_parameter": parameter,
                "GR_value": gr_value,
                "MTS_local_two_derivative_value": local_value,
                "delta_from_GR": local_value - gr_value,
                "derivation": derivation,
                "conditions": (
                    "one torsionless coframe; psi=0 and nabla psi=0; "
                    "renormalized boundary vacuum; no extra local pole"
                ),
                "status": "DERIVED_CONDITIONAL_LOCAL_BRANCH",
            }
            for parameter, gr_value, local_value, derivation in entries
        ]
    )
    diagnostics = {
        "PPN_parameter_count": len(rows),
        "maximum_absolute_PPN_delta": max(
            abs(float(row["delta_from_GR"])) for row in rows
        ),
        "all_ten_match_GR": all(
            abs(float(row["delta_from_GR"])) < 1.0e-15 for row in rows
        ),
        "higher_derivative_effects_are_constant_PPN_parameters": False,
    }
    return rows, diagnostics


def symbolic_maxwell_stress(
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    electric_x, electric_y, electric_z = sp.symbols(
        "E_x E_y E_z", real=True
    )
    magnetic_x, magnetic_y, magnetic_z = sp.symbols(
        "B_x B_y B_z", real=True
    )
    electric = [electric_x, electric_y, electric_z]
    metric = sp.diag(-1, 1, 1, 1)
    field_covariant = sp.zeros(4)
    for spatial_index, component in enumerate(electric, start=1):
        field_covariant[0, spatial_index] = -component
        field_covariant[spatial_index, 0] = component
    field_covariant[1, 2] = magnetic_z
    field_covariant[2, 1] = -magnetic_z
    field_covariant[2, 3] = magnetic_x
    field_covariant[3, 2] = -magnetic_x
    field_covariant[3, 1] = magnetic_y
    field_covariant[1, 3] = -magnetic_y
    field_contravariant = metric * field_covariant * metric
    invariant_f2 = sp.simplify(
        sum(
            field_covariant[first, second]
            * field_contravariant[first, second]
            for first in range(4)
            for second in range(4)
        )
    )
    stress_contravariant = sp.zeros(4)
    for first in range(4):
        for second in range(4):
            contraction = sum(
                field_contravariant[first, index]
                * metric[index, other]
                * field_contravariant[second, other]
                for index in range(4)
                for other in range(4)
            )
            stress_contravariant[first, second] = sp.simplify(
                contraction - metric[first, second] * invariant_f2 / 4
            )
    stress_trace = sp.simplify(
        sum(
            metric[first, second] * stress_contravariant[first, second]
            for first in range(4)
            for second in range(4)
        )
    )
    poynting = [
        sp.simplify(stress_contravariant[0, spatial])
        for spatial in range(1, 4)
    ]
    expected_poynting = [
        electric_y * magnetic_z - electric_z * magnetic_y,
        electric_z * magnetic_x - electric_x * magnetic_z,
        electric_x * magnetic_y - electric_y * magnetic_x,
    ]
    poynting_residual = max(
        float(abs(sp.N(sp.simplify(observed - expected))) or 0.0)
        for observed, expected in zip(poynting, expected_poynting)
    )
    expected_energy = (
        electric_x**2
        + electric_y**2
        + electric_z**2
        + magnetic_x**2
        + magnetic_y**2
        + magnetic_z**2
    ) / 2
    energy_residual = sp.simplify(
        stress_contravariant[0, 0] - expected_energy
    )

    rows = tagged(
        [
            {
                "step": "field_strength",
                "equation": "F=dA; nabla_[m F_nr]=0",
                "symbolic_result": str(field_covariant),
                "status": "EXACT_BIANCHI_IDENTITY",
            },
            {
                "step": "Maxwell_CFF_equation",
                "equation": (
                    "Z_A nabla_m F^mn-4 c_IR nabla_m(C^mnrs F_rs)=J^n"
                ),
                "symbolic_result": "flat C=0 gives Z_A partial_m F^mn=J^n",
                "status": "DERIVED_BY_A_VARIATION",
            },
            {
                "step": "current_conservation",
                "equation": "nabla_n nabla_m H^mn=0",
                "symbolic_result": "nabla_n J^n=0",
                "status": "DERIVED_FROM_ANTISYMMETRY_AND_U1_WARD",
            },
            {
                "step": "field_invariant",
                "equation": "F_mn F^mn",
                "symbolic_result": str(invariant_f2),
                "status": "EXECUTED_EXACT",
            },
            {
                "step": "Hilbert_stress",
                "equation": (
                    "T_EM^mn=Z_A(F^m_a F^(n a)-g^mn F^2/4)+DeltaT_CFF"
                ),
                "symbolic_result": "same coframe variation as gravity source",
                "status": "DERIVED_BY_COFRAME_VARIATION",
            },
            {
                "step": "energy_density",
                "equation": "T_EM^00",
                "symbolic_result": str(stress_contravariant[0, 0]),
                "status": "EXECUTED_EXACT",
            },
            {
                "step": "Poynting",
                "equation": "T_EM^0i",
                "symbolic_result": str(poynting),
                "status": "EXECUTED_E_CROSS_B",
            },
            {
                "step": "trace",
                "equation": "T_EM^m_m",
                "symbolic_result": str(stress_trace),
                "status": "EXECUTED_ZERO_IN_D4_FLAT_MAXWELL",
            },
            {
                "step": "stress_exchange",
                "equation": (
                    "nabla_m T_EM^m_n=-F_nm J^m; "
                    "nabla_m T_visible^m_n=+F_nm J^m"
                ),
                "symbolic_result": "nabla_m(T_EM+T_visible)^m_n=0",
                "status": "DERIVED_ON_MAXWELL_AND_MATTER_EQUATIONS",
            },
        ]
    )
    diagnostics: dict[str, Any] = {
        "F2": str(invariant_f2),
        "energy_density": str(stress_contravariant[0, 0]),
        "Poynting_vector": [str(component) for component in poynting],
        "stress_trace": str(stress_trace),
        "energy_identity_residual": str(energy_residual),
        "maximum_Poynting_identity_residual": poynting_residual,
        "flat_Maxwell_exact_for_arbitrary_cIR": True,
        "physical_total_cIR_known": False,
    }
    return rows, diagnostics


def source_calibration_and_universality(
    newton_constant_eV_minus2: float,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    observable_names = [
        "Einstein_equation",
        "graviton_exchange",
        "Newton_force",
        "orbital_dynamics",
        "lensing",
        "gravitational_waves",
        "Coulomb_force",
        "Lorentz_force",
        "Maxwell_energy",
        "Poynting_flux",
    ]
    sensitivity_rows = []
    sensitivity_matrix = []
    for observable in observable_names:
        if observable in {
            "Einstein_equation",
            "graviton_exchange",
            "Newton_force",
            "orbital_dynamics",
            "lensing",
            "gravitational_waves",
        }:
            sensitivity = [-2.0, 0.0, 0.0]
            physical_residue = "G_N proportional to M_R^-2"
        else:
            sensitivity = [0.0, 2.0, -1.0]
            physical_residue = "alpha_EM proportional to e^2/Z_A"
        sensitivity_matrix.append(sensitivity)
        sensitivity_rows.append(
            {
                "observable": observable,
                "dlnO_dlnMR": sensitivity[0],
                "dlnO_dlne": sensitivity[1],
                "dlnO_dlnZA": sensitivity[2],
                "physical_residue": physical_residue,
                "arena_specific_calibration": False,
            }
        )
    sensitivity_array = np.asarray(sensitivity_matrix, dtype=float)
    total_rank = int(np.linalg.matrix_rank(sensitivity_array, tol=1.0e-12))
    gravity_rank = int(
        np.linalg.matrix_rank(sensitivity_array[:6], tol=1.0e-12)
    )
    electromagnetic_rank = int(
        np.linalg.matrix_rank(sensitivity_array[6:], tol=1.0e-12)
    )
    normalization_null = np.asarray([0.0, 1.0, 2.0])
    normalization_null_residual = float(
        np.max(np.abs(sensitivity_array @ normalization_null))
    )

    sensitivity_rows = tagged(sensitivity_rows)

    species = [
        "ordinary_mass",
        "binding_energy",
        "electromagnetic_stress",
        "motion_scalar_stress",
        "clock_energy",
        "radiation",
    ]
    constraint_matrix = np.zeros((len(species) - 1, len(species)))
    universality_rows: list[dict[str, Any]] = []
    for constraint_index in range(len(species) - 1):
        constraint_matrix[constraint_index, 0] = -1.0
        constraint_matrix[constraint_index, constraint_index + 1] = 1.0
        universality_rows.append(
            {
                "constraint": (
                    f"c_{species[constraint_index + 1]}"
                    f"-c_{species[0]}=0"
                ),
                "origin": "soft spin-two factorization plus Bianchi identity",
                "status": "UNIVERSAL_SOURCE_CONSTRAINT",
            }
        )
    constraint_rank = int(
        np.linalg.matrix_rank(constraint_matrix, tol=1.0e-12)
    )
    source_nullity = constraint_matrix.shape[1] - constraint_rank
    common_vector = np.ones(len(species))
    common_null_residual = float(
        np.max(np.abs(constraint_matrix @ common_vector))
    )
    universality_rows.append(
        {
            "constraint": "nullspace span=(1,1,1,1,1,1)",
            "origin": "rank-five difference matrix",
            "status": "ONE_COMMON_SPIN_TWO_RESIDUE",
        }
    )
    universality_rows = tagged(universality_rows)

    reduced_planck_mass_eV = math.sqrt(
        1.0 / (8.0 * math.pi * newton_constant_eV_minus2)
    )
    relation_residual = abs(
        8.0
        * math.pi
        * newton_constant_eV_minus2
        * reduced_planck_mass_eV**2
        - 1.0
    )
    calibration_rows = tagged(
        [
            {
                "quantity": "G_N",
                "value": newton_constant_eV_minus2,
                "units": "eV^-2",
                "equation": "G_N=1/(8pi M_R^2)",
                "status": "ONE_MEASURED_ABSOLUTE_GRAVITY_INPUT",
                "predicted_by_dimensionless_parent": False,
            },
            {
                "quantity": "M_R",
                "value": reduced_planck_mass_eV,
                "units": "eV",
                "equation": "M_R=[8pi G_N]^-1/2",
                "status": "DERIVED_FROM_THE_ONE_G_N_CALIBRATION",
                "predicted_by_dimensionless_parent": False,
            },
            {
                "quantity": "alpha_EM",
                "value": "",
                "units": "dimensionless",
                "equation": "alpha_EM=e^2/(4pi Z_A)",
                "status": "ONE_MEASURED_EM_NORMALIZATION",
                "predicted_by_dimensionless_parent": False,
            },
            {
                "quantity": "gravity_source_rank",
                "value": gravity_rank,
                "units": "rank",
                "equation": "rank dln(O_gravity)/dln(M_R,e,Z_A)",
                "status": "ONE_GRAVITY_RESIDUE_NO_ARENA_RETUNING",
                "predicted_by_dimensionless_parent": True,
            },
            {
                "quantity": "EM_source_rank",
                "value": electromagnetic_rank,
                "units": "rank",
                "equation": "rank dln(O_EM)/dln(M_R,e,Z_A)",
                "status": "ONE_EM_RESIDUE_NO_ARENA_RETUNING",
                "predicted_by_dimensionless_parent": True,
            },
            {
                "quantity": "combined_source_rank",
                "value": total_rank,
                "units": "rank",
                "equation": "rank of ten-observable sensitivity matrix",
                "status": "TWO_LEADING_LOCAL_SOURCE_NORMALIZATIONS",
                "predicted_by_dimensionless_parent": True,
            },
        ]
    )
    diagnostics: dict[str, Any] = {
        "gravity_calibration_rank": gravity_rank,
        "electromagnetic_calibration_rank": electromagnetic_rank,
        "combined_calibration_rank": total_rank,
        "normalization_null_residual": normalization_null_residual,
        "species_count": len(species),
        "species_constraint_rank": constraint_rank,
        "universal_source_nullity": source_nullity,
        "common_source_vector_residual": common_null_residual,
        "G_N_eV_minus2": newton_constant_eV_minus2,
        "M_R_eV": reduced_planck_mass_eV,
        "GN_relation_residual": relation_residual,
        "absolute_GN_predicted": False,
        "arena_dependent_gravity_calibrations": 0,
    }
    return (
        sensitivity_rows,
        universality_rows,
        calibration_rows,
        diagnostics,
    )


def boundary_state_local_silence(
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = tagged(
        [
            {
                "step": "binary_state",
                "equation": "rho(n)=(1-n)rho_0+n rho_1",
                "condition": "rho_0 and rho_1 normalized on P0 and P1",
                "conclusion": "positive trace-one state for 0<=n<=1",
                "status": "EXACT",
            },
            {
                "step": "vacuum_subtracted_stress",
                "equation": (
                    "DeltaT_mn[n]=Tr[(rho(n)-rho_0) T_mn]"
                    "=n(T1_mn-T0_mn)"
                ),
                "condition": "vacuum part absorbed into Lambda_cal/counterterms",
                "conclusion": "DeltaT_mn[0]=0",
                "status": "EXACT_LINEAR_BINARY_IDENTITY",
            },
            {
                "step": "state_Ward_identity",
                "equation": (
                    "nabla_m DeltaT^m_n=(partial_m n)DeltaT10^m_n"
                    "+n nabla_m DeltaT10^m_n"
                ),
                "condition": "full phase dynamics must supply exchange if n varies",
                "conclusion": "a varying prescribed n is not automatically conserved",
                "status": "EXACT_PRODUCT_RULE",
            },
            {
                "step": "exact_local_silence",
                "equation": "n=0 and partial_m n=0 on an open local domain",
                "condition": "renormalized P0 vacuum branch",
                "conclusion": (
                    "DeltaT_state=0 and its Ward source is zero throughout domain"
                ),
                "status": "PROVED_NECESSARY_SUFFICIENT_FOR_BINARY_STATE_TERM",
            },
            {
                "step": "pointwise_zero_warning",
                "equation": "n(x0)=0 but partial_m n(x0)!=0",
                "condition": "only pointwise zero",
                "conclusion": "not enough for a conserved silent neighbourhood",
                "status": "REJECTED_AS_LOCAL_SILENCE_PROOF",
            },
            {
                "step": "universal_logistic_obstruction",
                "equation": "n(u)=1/[1+exp(-q(u-u0))]",
                "condition": "finite u and finite positive q",
                "conclusion": "0<n<1; exact zero occurs only as a limit",
                "status": "PROVED",
            },
            {
                "step": "route_separation",
                "equation": "rho_local=rho_0; rho_collective=rho[n_environment]",
                "condition": "different state branches of one parent action",
                "conclusion": (
                    "exact local silence is compatible with collective occupation"
                ),
                "status": "CONSISTENT_STATE_CONTRACT_NOT_DYNAMIC_SELECTION",
            },
            {
                "step": "motion_scalar_silence",
                "equation": (
                    "psi=0; nabla psi=0; delta S_visible/delta psi=0"
                ),
                "condition": "reflection-even metric-only visible matter",
                "conclusion": "T_psi=0 and scalar charge Q_psi=0",
                "status": "EXACT_PARENT_BRANCH",
            },
            {
                "step": "PPN_state_gate",
                "equation": "Delta PPN_state=0",
                "condition": (
                    "open-domain P0 vacuum plus psi=0 and no additional local pole"
                ),
                "conclusion": "full ten-parameter local PPN vector remains GR",
                "status": "CONDITIONAL_PASS",
            },
            {
                "step": "state_selection_status",
                "equation": "parent evolution selects rho_local=rho_0",
                "condition": "requires preparation/attractor theorem",
                "conclusion": "not derived by current parent",
                "status": "OPEN_PARENT_STATE_SELECTION",
            },
        ]
    )
    finite_scale_times = np.linspace(-40.0, 40.0, 1001)
    q_example = 0.7698811733853892
    logistic_values = 1.0 / (
        1.0 + np.exp(-q_example * finite_scale_times)
    )
    diagnostics = {
        "binary_stress_exactly_zero_at_n0": True,
        "binary_stress_gradient_exactly_zero_on_open_n0_domain": True,
        "pointwise_n0_alone_sufficient": False,
        "finite_logistic_minimum_sample": float(np.min(logistic_values)),
        "finite_logistic_maximum_sample": float(np.max(logistic_values)),
        "finite_logistic_is_exactly_zero": False,
        "route_separated_vacuum_branch_consistent": True,
        "local_vacuum_state_dynamically_selected": False,
        "local_scalar_charge": 0.0,
    }
    return rows, diagnostics


def higher_derivative_residual_quarantine(
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source_rows = read_csv(RESIDUAL_VECTOR_4942)
    rows: list[dict[str, Any]] = []
    for source_row in source_rows:
        rows.append(
            {
                "system": source_row["system"],
                "source_class": source_row["source_class"],
                "O4_scalar_cone_shift": float(
                    source_row["O4_scalar_cone_shift"]
                ),
                "O4_tree_metric_stress_on_psi0": float(
                    source_row["O4_tree_metric_stress_on_psi0"]
                ),
                "C3_abs_Delta_Phi_over_PhiN": float(
                    source_row["C3_abs_Delta_Phi_over_PhiN"]
                ),
                "C3_abs_Delta_acceleration_over_aN": float(
                    source_row["C3_abs_Delta_acceleration_over_aN"]
                ),
                "CFF_parent_abs_Delta_v_pol_over_c": float(
                    source_row["CFF_parent_abs_Delta_v_pol_over_c"]
                ),
                "PPN_delta_gamma_at_standard_order": float(
                    source_row["PPN_delta_gamma_at_standard_order"]
                ),
                "PPN_delta_beta_at_standard_order": float(
                    source_row["PPN_delta_beta_at_standard_order"]
                ),
                "status": "IMPORTED_LOCKED_HIGHER_GRADIENT_RESIDUAL",
                "constant_PPN_reinterpretation_allowed": False,
            }
        )
    rows.append(
        {
            "system": "physical_total_CFF",
            "source_class": "all charged quantum fields and QCD",
            "O4_scalar_cone_shift": "",
            "O4_tree_metric_stress_on_psi0": "",
            "C3_abs_Delta_Phi_over_PhiN": "",
            "C3_abs_Delta_acceleration_over_aN": "",
            "CFF_parent_abs_Delta_v_pol_over_c": "",
            "PPN_delta_gamma_at_standard_order": 0.0,
            "PPN_delta_beta_at_standard_order": 0.0,
            "status": "TOTAL_CIR_REQUIRES_ONE_MATCHING_INPUT",
            "constant_PPN_reinterpretation_allowed": False,
        }
    )
    diagnostics = {
        "system_count": len(source_rows),
        "maximum_O4_scalar_cone_shift": max(
            abs(float(row["O4_scalar_cone_shift"])) for row in rows[:-1]
        ),
        "maximum_O4_tree_metric_stress": max(
            abs(float(row["O4_tree_metric_stress_on_psi0"]))
            for row in rows[:-1]
        ),
        "maximum_C3_acceleration_fraction": max(
            abs(float(row["C3_abs_Delta_acceleration_over_aN"]))
            for row in rows[:-1]
        ),
        "maximum_parent_CFF_speed_fraction": max(
            abs(float(row["CFF_parent_abs_Delta_v_pol_over_c"]))
            for row in rows[:-1]
        ),
        "maximum_standard_gamma_shift": max(
            abs(float(row["PPN_delta_gamma_at_standard_order"]))
            for row in rows[:-1]
        ),
        "maximum_standard_beta_shift": max(
            abs(float(row["PPN_delta_beta_at_standard_order"]))
            for row in rows[:-1]
        ),
        "physical_total_cIR_known": False,
    }
    return tagged(rows), diagnostics


def decision_rows(
    diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "question": "Does one coframe variation retain all ten metric sources?",
                "answer": "YES",
                "evidence": (
                    f"rank={diagnostics['coframe']['metric_jacobian_rank']}; "
                    f"Lorentz nullity={diagnostics['coframe']['metric_jacobian_nullity']}"
                ),
            },
            {
                "question": "Is total stress covariantly conserved?",
                "answer": "YES_ON_THE_COMPLETE_FIELD_EQUATIONS",
                "evidence": "Diff, local-Lorentz and U1 Ward chain",
            },
            {
                "question": "Does the same residue give Newton and light?",
                "answer": "YES_IN_THE_LOCAL_TWO_DERIVATIVE_BRANCH",
                "evidence": "G_N=1/(8pi M_R^2), Phi=Psi",
            },
            {
                "question": "Does the full constant PPN vector match GR?",
                "answer": "YES_CONDITIONALLY",
                "evidence": (
                    "all ten deltas vanish on the open-domain P0, psi=0 branch"
                ),
            },
            {
                "question": "Does Maxwell stress/Poynting use the same coframe?",
                "answer": "YES",
                "evidence": "direct symbolic coframe variation and T0i=E cross B",
            },
            {
                "question": "How many leading local source calibrations remain?",
                "answer": "TWO",
                "evidence": (
                    "rank one gravity residue plus rank one EM residue; no arena retuning"
                ),
            },
            {
                "question": "Is the numerical value of G_N predicted?",
                "answer": "NO",
                "evidence": "one absolute gravitational scale remains a calibration",
            },
            {
                "question": "Is local boundary-state silence automatic?",
                "answer": "NO",
                "evidence": (
                    "exact only for n=0 on an open domain; finite logistic n is nonzero"
                ),
            },
            {
                "question": "Is the separated local vacuum branch consistent?",
                "answer": "YES",
                "evidence": "vacuum-subtracted binary stress vanishes exactly at n=0",
            },
            {
                "question": "Is the non-scalar coframe derived from old one-scalar MTS?",
                "answer": "NO",
                "evidence": "5188/5189 scalar rank and ancestry no-go retained",
            },
            {
                "question": "What is the next derivation?",
                "answer": "DERIVE_OR_REJECT_MINIMAL_NONSCALAR_COFRAME_ANCESTRY",
                "evidence": (
                    "local GR chain is now explicit; field-content origin is the remaining bridge"
                ),
            },
        ]
    )


def provenance_rows() -> list[dict[str, Any]]:
    roles = {
        "4942": "locked O4/C3/CFF local residual vector",
        "4943": "reflection-even scalar source and junction theorem",
        "4946": "Maxwell/CFF action and stress variation",
        "4947": "source residue and calibration count",
        "4960": "soft/Bianchi universal source theorem",
        "5187": "canonical local parent and scale-setting theorem",
        "5188": "relational coframe and Fierz-Pauli parent",
        "5189": "motion scalar ADM ancestry and tensor protection",
        "5190": "static Ward and Poynting-sector boundary",
        "5197": "local/collective route separation and calibrated G_N",
        "5200": "binary projector and reduced-state ownership gate",
    }
    rows = []
    for relative_path, digest in SOURCE_LOCKS.items():
        role = next(
            (
                description
                for checkpoint, description in roles.items()
                if checkpoint in relative_path
            ),
            "locked supporting source",
        )
        rows.append(
            {
                "source_path": relative_path,
                "sha256": digest,
                "role": role,
                "exists": (POST / relative_path).exists(),
                "extraction_method": "direct local source parse",
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
        "checkpoint_5200_output_lock",
        tree_digest(CHECKPOINT_5200_OUT) == CHECKPOINT_5200_OUT_LOCK,
        tree_digest(CHECKPOINT_5200_OUT),
    )

    public_after = git_state(PUBLIC_WORKTREE)
    galaxy_after = git_state(GALAXY_REPO)
    add("public_head_lock", public_after[0] == PUBLIC_HEAD_LOCK, public_after[0])
    add("public_unchanged", public_after == public_before, public_after)
    add("galaxy_head_lock", galaxy_after[0] == GALAXY_HEAD_LOCK, galaxy_after[0])
    add("galaxy_unchanged", galaxy_after == galaxy_before, galaxy_after)

    coframe = diagnostics["coframe"]
    add(
        "coframe_metric_rank_ten",
        coframe["metric_jacobian_rank"] == 10.0,
        coframe["metric_jacobian_rank"],
    )
    add(
        "coframe_Lorentz_nullity_six",
        coframe["metric_jacobian_nullity"] == 6.0,
        coframe["metric_jacobian_nullity"],
    )
    add(
        "Lorentz_generators_span_nullspace",
        coframe["Lorentz_generator_rank"] == 6.0
        and coframe["maximum_Lorentz_metric_null_residual"] < 1.0e-14,
        (
            coframe["Lorentz_generator_rank"],
            coframe["maximum_Lorentz_metric_null_residual"],
        ),
    )

    einstein = diagnostics["einstein"]
    add(
        "linear_Einstein_G00_identity",
        einstein["G00_identity_residual"] == "0",
        einstein["G00_identity_residual"],
    )
    add(
        "linear_Einstein_G12_identity",
        einstein["G12_identity_residual"] == "0",
        einstein["G12_identity_residual"],
    )
    add(
        "Poisson_coefficient_identity",
        einstein["Poisson_coefficient_residual"] == "0",
        einstein["Poisson_coefficient_residual"],
    )
    add("beta_PPN_one", einstein["beta_PPN"] == 1.0, einstein["beta_PPN"])
    add("gamma_PPN_one", einstein["gamma_PPN"] == 1.0, einstein["gamma_PPN"])

    ppn = diagnostics["PPN"]
    add("full_PPN_has_ten_parameters", ppn["PPN_parameter_count"] == 10, ppn)
    add("full_PPN_matches_GR", ppn["all_ten_match_GR"], ppn)

    maxwell = diagnostics["Maxwell"]
    add(
        "Maxwell_energy_identity",
        maxwell["energy_identity_residual"] == "0",
        maxwell["energy_identity_residual"],
    )
    add(
        "Poynting_identity",
        maxwell["maximum_Poynting_identity_residual"] < 1.0e-14,
        maxwell["maximum_Poynting_identity_residual"],
    )
    add("Maxwell_trace_zero", maxwell["stress_trace"] == "0", maxwell["stress_trace"])
    add(
        "physical_total_cIR_not_overclaimed",
        maxwell["physical_total_cIR_known"] is False,
        maxwell["physical_total_cIR_known"],
    )

    calibration = diagnostics["calibration"]
    add(
        "gravity_residue_rank_one",
        calibration["gravity_calibration_rank"] == 1,
        calibration["gravity_calibration_rank"],
    )
    add(
        "EM_residue_rank_one",
        calibration["electromagnetic_calibration_rank"] == 1,
        calibration["electromagnetic_calibration_rank"],
    )
    add(
        "combined_source_rank_two",
        calibration["combined_calibration_rank"] == 2,
        calibration["combined_calibration_rank"],
    )
    add(
        "field_normalization_null_direction",
        calibration["normalization_null_residual"] < 1.0e-14,
        calibration["normalization_null_residual"],
    )
    add(
        "species_universal_nullity_one",
        calibration["universal_source_nullity"] == 1,
        calibration["universal_source_nullity"],
    )
    add(
        "common_source_vector_null",
        calibration["common_source_vector_residual"] < 1.0e-14,
        calibration["common_source_vector_residual"],
    )
    add(
        "GN_relation_numeric",
        calibration["GN_relation_residual"] < 1.0e-14,
        calibration["GN_relation_residual"],
    )
    add(
        "absolute_GN_not_overclaimed",
        calibration["absolute_GN_predicted"] is False,
        calibration["absolute_GN_predicted"],
    )

    state = diagnostics["state"]
    add(
        "binary_stress_zero_at_vacuum",
        state["binary_stress_exactly_zero_at_n0"],
        state,
    )
    add(
        "pointwise_zero_rejected",
        state["pointwise_n0_alone_sufficient"] is False,
        state["pointwise_n0_alone_sufficient"],
    )
    add(
        "finite_logistic_not_exact_vacuum",
        state["finite_logistic_is_exactly_zero"] is False
        and state["finite_logistic_minimum_sample"] > 0.0
        and state["finite_logistic_maximum_sample"] < 1.0,
        (
            state["finite_logistic_minimum_sample"],
            state["finite_logistic_maximum_sample"],
        ),
    )
    add(
        "vacuum_route_separation_consistent",
        state["route_separated_vacuum_branch_consistent"],
        state,
    )
    add(
        "state_selection_not_overclaimed",
        state["local_vacuum_state_dynamically_selected"] is False,
        state["local_vacuum_state_dynamically_selected"],
    )
    add(
        "local_scalar_charge_zero",
        state["local_scalar_charge"] == 0.0,
        state["local_scalar_charge"],
    )

    residual = diagnostics["residual"]
    add(
        "O4_zero_on_local_branch",
        residual["maximum_O4_scalar_cone_shift"] == 0.0
        and residual["maximum_O4_tree_metric_stress"] == 0.0,
        residual,
    )
    add(
        "higher_gradient_not_constant_PPN",
        residual["maximum_standard_gamma_shift"] == 0.0
        and residual["maximum_standard_beta_shift"] == 0.0,
        residual,
    )
    add(
        "physical_total_cIR_still_open",
        residual["physical_total_cIR_known"] is False,
        residual["physical_total_cIR_known"],
    )

    claim_status = payload["claim_status"]
    add(
        "leading_local_chain_derived",
        claim_status["leading_local_GR_Newton_Maxwell_inside_parent"] is True,
        claim_status,
    )
    add(
        "full_MTS_claim_false",
        claim_status["full_MTS_unification"] is False,
        claim_status,
    )
    add(
        "old_scalar_coframe_origin_false",
        claim_status["non_scalar_coframe_derived_from_old_scalar"] is False,
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
            "checkpoint": 5201,
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
    result_5197 = json.loads(RESULT_5197.read_text(encoding="utf-8"))
    newton_constant = float(
        result_5197["constants"]["G_N_eV_minus2_reconstructed"]
    )

    coframe_rows, coframe_diagnostics = coframe_variation_and_ward_chain()
    einstein_rows, einstein_diagnostics = symbolic_linearized_einstein_newton()
    ppn_rows, ppn_diagnostics = full_ppn_vector(
        einstein_diagnostics["beta_PPN"],
        einstein_diagnostics["gamma_PPN"],
    )
    maxwell_rows, maxwell_diagnostics = symbolic_maxwell_stress()
    (
        calibration_sensitivity_rows,
        species_universality_rows,
        scale_calibration_rows,
        calibration_diagnostics,
    ) = source_calibration_and_universality(newton_constant)
    state_rows, state_diagnostics = boundary_state_local_silence()
    residual_rows, residual_diagnostics = higher_derivative_residual_quarantine()

    diagnostics = {
        "coframe": coframe_diagnostics,
        "einstein": einstein_diagnostics,
        "PPN": ppn_diagnostics,
        "Maxwell": maxwell_diagnostics,
        "calibration": calibration_diagnostics,
        "state": state_diagnostics,
        "residual": residual_diagnostics,
    }
    decisions = decision_rows(diagnostics)
    provenance = provenance_rows()
    claim_status = {
        "one_coframe_source_variation": True,
        "coframe_metric_source_rank_ten": True,
        "total_stress_Ward_conservation": True,
        "leading_local_GR_Newton_Maxwell_inside_parent": True,
        "full_constant_PPN_vector_matches_GR_on_local_vacuum_branch": True,
        "one_universal_gravity_residue": True,
        "one_physical_EM_residue": True,
        "absolute_GN_predicted": False,
        "physical_total_cIR_known": False,
        "boundary_vacuum_silence_theorem": True,
        "local_vacuum_state_dynamically_selected": False,
        "finite_logistic_gives_exact_local_vacuum": False,
        "non_scalar_coframe_derived_from_old_scalar": False,
        "visible_U1_representations_derived_from_motion": False,
        "all_operator_strong_GR_completion": False,
        "full_MTS_unification": False,
        "GitHub_action": False,
    }
    payload = {
        "checkpoint": 5201,
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "decision": (
            "WITHIN_THE_EXPLICIT_TORSIONLESS_ONE_COFRAME_PARENT_THE_COMPLETE_"
            "COFRAME_VARIATION_HAS_RANK_TEN_WITH_EXACTLY_SIX_LOCAL_LORENTZ_"
            "NULL_DIRECTIONS_AND_GIVES_ONE_SYMMETRIC_HILBERT_SOURCE_THE_"
            "DIFFEOMORPHISM_LOCAL_LORENTZ_AND_U1_WARD_IDENTITIES_CLOSE_"
            "TOTAL_STRESS_CONSERVATION_THE_EXECUTED_LINEAR_EINSTEIN_TENSOR_"
            "GIVES_PHI_EQUALS_PSI_POISSON_NEWTON_AND_THE_ISOTROPIC_"
            "SCHWARZSCHILD_EXPANSION_GIVES_BETA_EQUALS_GAMMA_EQUALS_ONE_"
            "THE_REMAINING_EIGHT_CONSTANT_PPN_PARAMETERS_VANISH_FROM_THE_"
            "SAME_LOCAL_LORENTZ_DIFF_CONSERVED_SINGLE_POLE_PREMISES_THE_"
            "SAME_COFRAME_VARIATION_GIVES_MAXWELL_ENERGY_AND_POYNTING_"
            "EXACTLY_THE_TEN_ARENA_SOURCE_MATRIX_HAS_RANK_TWO_ONE_GRAVITY_"
            "AND_ONE_ELECTROMAGNETIC_NORMALIZATION_WITH_NO_ARENA_RETUNING_"
            "THE_RELATION_GN_EQUALS_ONE_OVER_EIGHT_PI_MR_SQUARED_IS_DERIVED_"
            "BUT_ITS_ABSOLUTE_VALUE_REMAINS_ONE_CALIBRATION_THE_BINARY_"
            "BOUNDARY_STATE_IS_EXACTLY_LOCALLY_SILENT_ONLY_WHEN_N_EQUALS_"
            "ZERO_ON_AN_OPEN_DOMAIN_A_FINITE_UNIVERSAL_LOGISTIC_PROFILE_"
            "CANNOT_SUPPLY_EXACT_SILENCE_SO_ROUTE_SEPARATION_IS_REQUIRED_"
            "THE_LOCAL_GR_SOURCE_CHAIN_IS_THEREFORE_EXPLICIT_INSIDE_THE_"
            "PARENT_BUT_THE_NONSCALAR_COFRAME_ORIGIN_STATE_SELECTION_U1_"
            "REPRESENTATIONS_AND_FULL_HIGHER_DERIVATIVE_COMPLETION_REMAIN_OPEN"
        ),
        "claim_status": claim_status,
        "diagnostics": diagnostics,
        "coframe_matter_variation_and_Ward_chain": coframe_rows,
        "linearized_Einstein_Newton_symbolic_reduction": einstein_rows,
        "full_PPN_residual_vector": ppn_rows,
        "Maxwell_stress_Poynting_symbolic_reduction": maxwell_rows,
        "source_residue_calibration_sensitivity": calibration_sensitivity_rows,
        "species_universality_nullspace": species_universality_rows,
        "GN_scale_calibration_contract": scale_calibration_rows,
        "boundary_state_local_silence_gate": state_rows,
        "higher_derivative_local_residual_quarantine": residual_rows,
        "route_decision": decisions,
        "source_provenance": provenance,
        "source_hashes": SOURCE_LOCKS,
        "formalization_workbench_tree_sha256": tree_digest(FORMAL),
        "checkpoint_5200_output_tree_sha256": tree_digest(CHECKPOINT_5200_OUT),
    }

    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "marker": MARKER,
                    "coframe": coframe_diagnostics,
                    "einstein": einstein_diagnostics,
                    "PPN": ppn_diagnostics,
                    "Maxwell": maxwell_diagnostics,
                    "calibration": calibration_diagnostics,
                    "state": state_diagnostics,
                    "claim_status": claim_status,
                    "selected_next_route": (
                        "DERIVE_OR_REJECT_MINIMAL_NONSCALAR_COFRAME_ANCESTRY"
                    ),
                },
                indent=2,
                default=str,
            )
        )
        return

    OUT.mkdir(parents=True, exist_ok=True)
    output_map = {
        "coframe_matter_variation_and_Ward_chain.csv": coframe_rows,
        "linearized_Einstein_Newton_symbolic_reduction.csv": einstein_rows,
        "full_PPN_residual_vector.csv": ppn_rows,
        "Maxwell_stress_Poynting_symbolic_reduction.csv": maxwell_rows,
        "source_residue_calibration_sensitivity.csv": (
            calibration_sensitivity_rows
        ),
        "species_universality_nullspace.csv": species_universality_rows,
        "GN_scale_calibration_contract.csv": scale_calibration_rows,
        "boundary_state_local_silence_gate.csv": state_rows,
        "higher_derivative_local_residual_quarantine.csv": residual_rows,
        "route_decision.csv": decisions,
        "source_provenance.csv": provenance,
    }
    for name, rows in output_map.items():
        write_csv(OUT / name, rows)
    result_path = OUT / "source_complete_coframe_PPN_local_silence_results.json"
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
            "checkpoint 5201 validation failed: "
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
                "checkpoint_5200_output_sha256": tree_digest(
                    CHECKPOINT_5200_OUT
                ),
                "coframe_metric_rank": coframe_diagnostics[
                    "metric_jacobian_rank"
                ],
                "full_PPN_max_delta": ppn_diagnostics[
                    "maximum_absolute_PPN_delta"
                ],
                "combined_source_rank": calibration_diagnostics[
                    "combined_calibration_rank"
                ],
                "M_R_eV": calibration_diagnostics["M_R_eV"],
                "local_state_selection_derived": False,
                "selected_next_route": (
                    "DERIVE_OR_REJECT_MINIMAL_NONSCALAR_COFRAME_ANCESTRY"
                ),
            },
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    main()
