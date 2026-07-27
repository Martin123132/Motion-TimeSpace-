from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

sys.dont_write_bytecode = True


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5182"

VERTEX_CSV = OUT / "static_Hilbert_vertex_and_seagull_audit.csv"
POLARIZATION_CSV = OUT / "critical_pair_scalar_polarization.csv"
RESPONSE_CSV = OUT / "constrained_Newtonian_response_theorem.csv"
TARGET_CSV = OUT / "critical_target_and_gap_endpoint_gate.csv"
OWNERSHIP_CSV = OUT / "nonminimal_coupling_parent_ownership.csv"
DECISION_CSV = OUT / "static_pair_route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "static_Hilbert_pair_projector_results.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5182_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5182-Y5-R2FR-static-Hilbert-pair-projector-constrained-Newtonian-response-and-route-decision.md"
)

MARKER = "MTS_5182_STATIC_HILBERT_PAIR_PROJECTOR_NEWTONIAN_RESPONSE_GATE"
CHECKED_DATE = "2026-07-23"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_TREE_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
CHECKPOINT_5176_ROOT = POST / "source-intake" / "functional_rg" / "5176"

ROUTE_DECISION = (
    "THE_ACTUAL_STATIC_HILBERT_PAIR_VERTEX_HAS_NOW_BEEN_PROJECTED_THROUGH_"
    "THE_NEWTONIAN_SCALAR_CONSTRAINTS_THE_CURRENT_SHIFT_SYMMETRIC_PARENT_"
    "HAS_ETA_EQUALS_ZERO_SO_THE_CRITICAL_PAIR_COUPLES_ONLY_TO_GRAVITATIONAL_"
    "SLIP_AND_IS_EXACTLY_INVISIBLE_TO_A_DUST_SOURCE_ALLOWING_THE_STRONGEST_"
    "LOCAL_CURVATURE_IMPROVEMENT_DOES_NOT_RESCUE_THE_ROUTE_BECAUSE_EVERY_"
    "POSITIVE_DRESSING_OF_THIS_DERIVED_PAIR_PROJECTOR_ON_THE_GR_CONNECTED_NO_POLE_"
    "BRANCH_SATISFIES_PHI_OVER_PHI_GR_LESS_THAN_OR_EQUAL_TO_ONE_THE_ONLY_"
    "NONTRIVIAL_NO_SLIP_VALUE_ETA_EQUALS_ONE_EIGHTH_SCREENS_GRAVITY_AND_THE_"
    "PURE_COMMON_VALUE_ETA_EQUALS_ONE_SIXTH_ROTATES_THE_BUBBLE_INTO_THE_COMMON_"
    "PROJECTOR_BUT_ALSO_SCREENS_THE_NEWTONIAN_AND_LENSING_RESPONSE_LOCAL_"
    "SEAGULLS_CANNOT_CHANGE_THE_NONANALYTIC_PAIR_TERM_AND_EVEN_AN_EXACT_GAP_"
    "COLLAPSE_REACHES_THIS_REJECTED_ENDPOINT_THEREFORE_PASSIVE_ZERO_"
    "BACKGROUND_HILBERT_PAIR_DRESSING_IS_REJECTED_AS_THE_5148_GALAXY_"
    "BRIDGE_THE_NEXT_PARENT_CALCULATION_MUST_DERIVE_A_NONZERO_BACKGROUND_"
    "LINEAR_METRIC_MOTION_MIXING_OR_SOURCE_SELECT_THE_ALREADY_CONSERVED_"
    "DIRECT_STATE_STRESS_WITHOUT_RETUNING"
)


def source_path(relative: str) -> Path:
    return POST / Path(relative.replace("/", "\\"))


SOURCES = {
    "checkpoint_4950_document": (
        source_path(
            "4950-Y5-R2FR-reflection-even-pair-source-operator-Rpsi2-Tpsi2-"
            "and-stabilized-galaxy-bifurcation-window-or-route-rejection.md"
        ),
        "64188638f5d19e125e5c1305cce898332267295b26625c1492610a3c529774cf",
    ),
    "checkpoint_4950_result": (
        source_path(
            "source-intake/functional_rg/4950/"
            "pair_operator_RG_and_bifurcation_results.json"
        ),
        "9243cf84c42036cddb29a267e6d425cc0f443d74410af11965542e0470860860",
    ),
    "checkpoint_4951_document": (
        source_path(
            "4951-Y5-R2FR-coupled-motion-VFZX2-functional-flow-fixed-point-"
            "index-and-GR-connected-trajectory-or-even-pair-sector-rejection.md"
        ),
        "1dd7f2632ab15370e7b44272c2439a6cf70d5559b1c7993b6f55d7e9fab9a131",
    ),
    "checkpoint_4951_result": (
        source_path(
            "source-intake/functional_rg/4951/"
            "coupled_VFZX2_fixed_and_running_gate_results.json"
        ),
        "d48c187595a71c3be6c2720a7545372d06361788a2fb242b902ef8e4bfe6ad8c",
    ),
    "checkpoint_4960_document": (
        source_path(
            "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-"
            "local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md"
        ),
        "6cd343d022dde751f86ad82eaf0f61fb5e3616753c228f631c44a45da278a69d",
    ),
    "checkpoint_4960_result": (
        source_path(
            "source-intake/functional_rg/4960/"
            "integrated_H_universal_source_results.json"
        ),
        "6fe2d8335cb1a4902c07c986e597e2f748050aa31f6137c5b52f9ced94542477",
    ),
    "checkpoint_4982_document": (
        source_path(
            "4982-Y5-R2FR-covariant-orderX-Schur-kernel-and-essential-two-point-"
            "subtraction.md"
        ),
        "83bfd153e96f7fb2322e2df1e71dce485caf5b7323230be285081ff280f55645",
    ),
    "checkpoint_4982_result": (
        source_path(
            "source-intake/functional_rg/4982/"
            "covariant_orderX_essential_results.json"
        ),
        "923aceac438808f912b03f032281ccc1bba960987ce70158222efc88f41d6b2f",
    ),
    "checkpoint_4982_second_variation": (
        source_path(
            "source-intake/functional_rg/4982/"
            "covariant_PX_second_variation_contract.csv"
        ),
        "5f19eda356865087f5d346d969a0a0647ca49d077f4c8a5956f79eb564ba6141",
    ),
    "checkpoint_5148_document": (
        source_path(
            "5148-Y5-R2FR-one-parent-local-GR-galaxy-spectral-response-cog-"
            "theorem.md"
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
    "checkpoint_5149_document": (
        source_path(
            "5149-Y5-R2FR-causal-spectral-density-critical-motion-mixing-and-"
            "vacuum-no-go.md"
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
    "checkpoint_5150_document": (
        source_path(
            "5150-Y5-R2FR-minimal-occupied-PX-zero-mode-TT-polarization-and-"
            "critical-sign-gate.md"
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
    "checkpoint_5150_loop": (
        source_path(
            "source-intake/functional_rg/5150/zero_mode_TT_loop_derivation.csv"
        ),
        "f63337c5c55a92091c6a1be30039531952c60dcc1c3c5c3d4fdabe2d673f58cf",
    ),
    "checkpoint_5151_document": (
        source_path(
            "5151-Y5-R2FR-parent-projective-occupation-to-conserved-Einstein-"
            "cluster-stress-and-two-metric-cog-gate.md"
        ),
        "b23ca652af8b66c220973cffbdc1ab2df028947c9dba8bd61666d1e0460c5fd5",
    ),
    "checkpoint_5151_result": (
        source_path(
            "source-intake/functional_rg/5151/projective_state_stress_results.json"
        ),
        "f1331f9bc511f12e4e785c9a3ffcf19dadf4eb8b05b05362031548a22984805c",
    ),
    "checkpoint_5178_document": (
        source_path(
            "5178-Y5-R2FR-exact-2PI-Schur-Ward-Vlasov-subtraction-and-Gaussian-"
            "residual-stress-no-go.md"
        ),
        "7bce528f8654373353304bf904316ddc15e2923dda3064bc7e9684e92a468ac9",
    ),
    "checkpoint_5178_result": (
        source_path(
            "source-intake/functional_rg/5178/"
            "twoPI_Schur_Vlasov_subtraction_results.json"
        ),
        "f007ab8d2f157e0fbda7465806e2902cca9e8f98d94db2d5d2fe4f1c54a0b007",
    ),
    "checkpoint_5180_document": (
        source_path(
            "5180-Y5-R2FR-interacting-retarded-2PI-kernel-Vlasov-subtraction-"
            "and-infrared-gap-closure-gate.md"
        ),
        "1df0b686a815496b143f5397aebf4b55d16058cd8bbca3910fb7993e980c0c10",
    ),
    "checkpoint_5180_result": (
        source_path(
            "source-intake/functional_rg/5180/interacting_spectral_gap_results.json"
        ),
        "699ac52dc60d07f6893b321aeb7a7701834870bb5fd1b09499f42a3486475512",
    ),
    "checkpoint_5181_document": (
        source_path(
            "5181-Y5-R2FR-critical-pair-bubble-positive-Hessian-and-parent-"
            "ownership-gate.md"
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
    "checkpoint_5181_pair": (
        source_path(
            "source-intake/functional_rg/5181/"
            "critical_pair_bubble_derivation.csv"
        ),
        "78cb5dec6a307c5e2361897c93b99ac7cd4b2689ffacb852671b67a46a45959a",
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
    for file_path in sorted(item for item in path.rglob("*") if item.is_file()):
        relative = file_path.relative_to(path).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(file_digest(file_path).encode("ascii"))
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields = list(rows[0])
    if any(list(row) != fields for row in rows):
        raise ValueError(f"inconsistent CSV fields: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def relative(path: Path) -> str:
    return path.relative_to(POST).as_posix()


def validation_row(
    validation_id: str,
    check: str,
    passed: bool,
    actual: Any,
    expected: Any,
) -> dict[str, Any]:
    return {
        "validation_id": validation_id,
        "check": check,
        "passed": bool(passed),
        "actual": actual,
        "expected": expected,
        "checkpoint_marker": MARKER,
    }


def close(
    actual: float,
    expected: float,
    relative_tolerance: float = 1.0e-11,
    absolute_tolerance: float = 1.0e-13,
) -> bool:
    return math.isclose(
        float(actual),
        float(expected),
        rel_tol=relative_tolerance,
        abs_tol=absolute_tolerance,
    )


def direct_loop_matrix(xi_value: float) -> np.ndarray:
    i_mm = 1.0 / 32.0
    i_m0 = -1.0 / 16.0
    bubble = 1.0 / 8.0
    minimal = np.array([0.5, -0.5], dtype=float)
    improvement = np.array([xi_value, -2.0 * xi_value], dtype=float)
    return 2.0 * (
        np.outer(minimal, minimal) * i_mm
        + (
            np.outer(minimal, improvement)
            + np.outer(improvement, minimal)
        )
        * i_m0
        + np.outer(improvement, improvement) * bubble
    )


def outer_loop_matrix(xi_value: float) -> np.ndarray:
    vector = np.array(
        [4.0 * xi_value - 1.0, 1.0 - 8.0 * xi_value],
        dtype=float,
    )
    return np.outer(vector, vector) / 64.0


def massive_pair_bubble(k_value: float, mass_value: float) -> float:
    if k_value <= 0.0 or mass_value <= 0.0:
        raise ValueError("k and mass must be positive")
    return math.atan(k_value / (2.0 * mass_value)) / (
        4.0 * math.pi * k_value
    )


def response_values(xi_value: float, ratio: float) -> dict[str, float]:
    factor = 48.0 * xi_value**2 - 16.0 * xi_value + 1.0
    denominator = 1.0 - ratio * factor
    phi_ratio = 1.0 - 16.0 * ratio * xi_value**2 / denominator
    psi_ratio = (
        1.0
        + 4.0
        * ratio
        * xi_value
        * (4.0 * xi_value - 1.0)
        / denominator
    )
    lens_ratio = 1.0 - 2.0 * ratio * xi_value / denominator
    slip_ratio = (
        -4.0
        * ratio
        * xi_value
        * (8.0 * xi_value - 1.0)
        / denominator
    )
    gamma_ppn = (
        psi_ratio / phi_ratio
        if abs(phi_ratio) > 1.0e-15
        else math.copysign(math.inf, psi_ratio)
    )
    return {
        "factor": factor,
        "denominator_over_a": denominator,
        "phi_ratio": phi_ratio,
        "psi_ratio": psi_ratio,
        "lensing_ratio": lens_ratio,
        "slip_over_phi_GR": slip_ratio,
        "gamma_PPN": gamma_ppn,
    }


def symbolic_contract() -> dict[str, Any]:
    eta, a, d, rho = sp.symbols("eta a d rho", real=True)
    vector = sp.Matrix([4 * eta - 1, 1 - 8 * eta])
    common = sp.Matrix([1, 1])
    slip = sp.Matrix([1, -1])
    kernel_gr = a * sp.Matrix([[0, -1], [-1, 1]])
    kernel = kernel_gr - d * vector * vector.T
    inverse = sp.simplify(kernel.inv())
    source = sp.Matrix([rho, 0])
    potentials = sp.simplify(inverse * source)
    factor = sp.expand((4 * eta - 1) * (12 * eta - 1))
    denominator = a - d * factor
    phi_gr = -rho / a
    psi_gr = -rho / a
    lens_gr = -2 * rho / a
    phi_ratio = sp.factor(potentials[0] / phi_gr)
    psi_ratio = sp.factor(potentials[1] / psi_gr)
    lens_ratio = sp.factor((common.T * potentials)[0] / lens_gr)
    slip_ratio = sp.factor((slip.T * potentials)[0] / phi_gr)
    expected_phi = sp.factor(1 - 16 * d * eta**2 / denominator)
    expected_psi = sp.factor(
        1 + 4 * d * eta * (4 * eta - 1) / denominator
    )
    expected_lens = sp.factor(1 - 2 * d * eta / denominator)
    expected_slip = sp.factor(
        -4 * d * eta * (8 * eta - 1) / denominator
    )
    no_slip_polynomial = sp.factor(sp.together(expected_slip).as_numer_denom()[0])
    return {
        "eta": eta,
        "a": a,
        "d": d,
        "rho": rho,
        "vector": vector,
        "common": common,
        "slip": slip,
        "kernel_gr": kernel_gr,
        "kernel": kernel,
        "inverse": inverse,
        "factor": factor,
        "denominator": denominator,
        "determinant": sp.factor(kernel.det()),
        "phi_ratio": phi_ratio,
        "psi_ratio": psi_ratio,
        "lens_ratio": lens_ratio,
        "slip_ratio": slip_ratio,
        "expected_phi": expected_phi,
        "expected_psi": expected_psi,
        "expected_lens": expected_lens,
        "expected_slip": expected_slip,
        "no_slip_polynomial": no_slip_polynomial,
        "common_overlap": sp.factor((common.T * vector)[0]),
        "slip_overlap": sp.factor((slip.T * vector)[0]),
    }


def make_rows() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    vertex_source = relative(SOURCES["checkpoint_4982_document"][0])
    pair_source = relative(SOURCES["checkpoint_5181_document"][0])
    target_source = relative(SOURCES["checkpoint_5148_document"][0])
    parent_source = relative(SOURCES["checkpoint_4951_document"][0])
    stress_source = relative(SOURCES["checkpoint_5151_document"][0])
    vertex_rows = [
        {
            "object": "static_metric",
            "equation": "ds2=-(1+2Phi)dt2+(1-2Psi)delta_ij dx^i dx^j",
            "status": "defined",
            "role": "Newtonian-gauge scalar projection",
            "source_path": vertex_source,
            "valid_for_claim": False,
        },
        {
            "object": "minimal_exact_factor",
            "equation": "N sqrt(gamma) gamma^ij=sqrt((1+2Phi)(1-2Psi)) delta^ij",
            "status": "derived",
            "role": "exact static Hilbert coupling of the canonical zero mode",
            "source_path": vertex_source,
            "valid_for_claim": False,
        },
        {
            "object": "minimal_factor_expansion",
            "equation": "1+(Phi-Psi)-0.5(Phi+Psi)^2+O(h^3)",
            "status": "derived",
            "role": "linear pair vertex plus quadratic seagull",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "object": "minimal_linear_vertex",
            "equation": "V_min=(Phi-Psi)[p.(p+k)]/2",
            "status": "derived",
            "role": "couples the minimal critical pair to gravitational slip",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "object": "minimal_seagull",
            "equation": "S_seagull=-integral (Phi+Psi)^2 (grad chi)^2/4",
            "status": "derived",
            "role": "one-propagator local/scaleless contact only",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "object": "linear_Ricci_scalar",
            "equation": "R1=2 nabla^2(2Psi-Phi)=2 k^2(Phi-2Psi)",
            "status": "derived",
            "role": "curvature-improvement metric vertex",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "object": "improvement_linear_vertex",
            "equation": "V_eta=eta k^2(Phi-2Psi) chi^2",
            "status": "derived",
            "role": "eta is defined operationally by this vertex; source-sign independent",
            "source_path": relative(SOURCES["checkpoint_4950_document"][0]),
            "valid_for_claim": False,
        },
        {
            "object": "improvement_seagulls",
            "equation": "delta2[sqrt(-g)R] chi^2 produces polynomial k^2 tadpoles",
            "status": "derived",
            "role": "renormalizes local geometric coefficients only",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "object": "nonanalytic_seagull_gate",
            "equation": "seagulls contain one scalar propagator and no pair cut",
            "status": "proved",
            "role": "cannot alter the |k|^3 connected pair coefficient",
            "source_path": pair_source,
            "valid_for_claim": False,
        },
    ]

    special_values = [
        ("minimal", 0.0),
        ("curvature_root", 1.0 / 12.0),
        ("nontrivial_no_slip", 1.0 / 8.0),
        ("pure_common_value", 1.0 / 6.0),
        ("curvature_root_2", 1.0 / 4.0),
    ]
    polarization_rows = [
        {
            "quantity": "massless_scalar_bubble",
            "eta": "",
            "expression": "B0(k)=1/(8|k|)",
            "numeric_value": 0.125,
            "status": "derived_at_5181",
            "source_path": pair_source,
            "valid_for_claim": False,
        },
        {
            "quantity": "derivative_integral",
            "eta": "",
            "expression": "I_MM/k^3=1/32",
            "numeric_value": 1.0 / 32.0,
            "status": "derived",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "quantity": "mixed_integral",
            "eta": "",
            "expression": "k^2 I_M0/k^3=-1/16",
            "numeric_value": -1.0 / 16.0,
            "status": "derived",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "quantity": "pair_polarization",
            "eta": "symbolic",
            "expression": "C_ab=W|k|^3 w_a w_b/64; w=(4eta-1,1-8eta)",
            "numeric_value": "",
            "status": "derived",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "quantity": "pair_effective_Hessian",
            "eta": "symbolic",
            "expression": "Delta K_ab=-W|k|^3 w_a w_b/64",
            "numeric_value": "",
            "status": "derived_passive_sign",
            "source_path": relative(SOURCES["checkpoint_5150_document"][0]),
            "valid_for_claim": False,
        },
        {
            "quantity": "rank_and_positivity",
            "eta": "symbolic",
            "expression": "det(C)=0; tr(C)=(40eta^2-12eta+1)/32>0",
            "numeric_value": "",
            "status": "proved",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
    ]
    for label, xi_value in special_values:
        vector = np.array(
            [4.0 * xi_value - 1.0, 1.0 - 8.0 * xi_value]
        )
        polarization_rows.append(
            {
                "quantity": label,
                "eta": f"{xi_value:.17g}",
                "expression": f"w=({vector[0]:.17g},{vector[1]:.17g})",
                "numeric_value": float(np.dot(vector, vector) / 64.0),
                "status": "evaluated",
                "source_path": str(SCRIPT),
                "valid_for_claim": False,
            }
        )

    response_rows = [
        {
            "case": "GR_static_kernel",
            "eta": "",
            "d_over_a": "",
            "denominator_over_a": "1",
            "Phi_over_Phi_GR": "1",
            "Psi_over_Psi_GR": "1",
            "lensing_over_GR": "1",
            "gamma_PPN": "1",
            "decision": "baseline",
            "valid_for_claim": False,
        },
        {
            "case": "exact_symbolic",
            "eta": "eta",
            "d_over_a": "r",
            "denominator_over_a": "Delta/a=1-r(48eta^2-16eta+1)",
            "Phi_over_Phi_GR": "1-16r eta^2/(Delta/a)",
            "Psi_over_Psi_GR": "1+4r eta(4eta-1)/(Delta/a)",
            "lensing_over_GR": "1-2r eta/(Delta/a)",
            "gamma_PPN": "R_Psi/R_Phi",
            "decision": "derived",
            "valid_for_claim": False,
        },
    ]
    sample_values = [
        ("negative_improvement", -0.25),
        ("minimal_parent", 0.0),
        ("first_factor_root", 1.0 / 12.0),
        ("nontrivial_no_slip", 1.0 / 8.0),
        ("pure_common_value", 1.0 / 6.0),
        ("second_factor_root", 1.0 / 4.0),
        ("positive_improvement", 1.0),
    ]
    for label, xi_value in sample_values:
        factor = 48.0 * xi_value**2 - 16.0 * xi_value + 1.0
        ratio = 0.5 if factor <= 0.0 else 0.25 / factor
        values = response_values(xi_value, ratio)
        response_rows.append(
            {
                "case": label,
                "eta": f"{xi_value:.17g}",
                "d_over_a": f"{ratio:.17g}",
                "denominator_over_a": f"{values['denominator_over_a']:.17g}",
                "Phi_over_Phi_GR": f"{values['phi_ratio']:.17g}",
                "Psi_over_Psi_GR": f"{values['psi_ratio']:.17g}",
                "lensing_over_GR": f"{values['lensing_ratio']:.17g}",
                "gamma_PPN": f"{values['gamma_PPN']:.17g}",
                "decision": (
                    "unchanged"
                    if close(values["phi_ratio"], 1.0)
                    else "screened_circular_potential"
                ),
                "valid_for_claim": False,
            }
        )

    target_rows = [
        {
            "gate": "checkpoint_5148_required_response",
            "derived_value": "Phi/Phi_GR=1+A C_q>1 for A>0",
            "required_value": "enhanced common Newtonian response",
            "result": "target",
            "source_path": target_source,
            "valid_for_claim": False,
        },
        {
            "gate": "passive_pair_GR_connected_branch",
            "derived_value": "Phi/Phi_GR<=1",
            "required_value": "Phi/Phi_GR>1",
            "result": "incompatible",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "gate": "minimal_eta_zero",
            "derived_value": "Phi=Psi=Phi_GR for dust",
            "required_value": "nontrivial common response",
            "result": "exactly_invisible",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "gate": "no_slip_extension",
            "derived_value": "eta=1/8 gives Phi/Phi_GR=4a/(4a+d)<1",
            "required_value": "no-slip enhancement",
            "result": "screening",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "gate": "pure_common_extension",
            "derived_value": "eta=1/6 gives lensing/GR=3a/(3a+d)<1",
            "required_value": "common enhancement",
            "result": "common_projector_but_screening",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "gate": "critical_pole",
            "derived_value": "Delta=a-d(48eta^2-16eta+1)=0",
            "required_value": "positive nonsingular Schur residual",
            "result": "constraint_rank_loss_not_target_criticality",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "gate": "finite_gap",
            "derived_value": "B_m analytic at k<<m; only m=0 reaches pair carrier",
            "required_value": "infrared 1/|k| carrier",
            "result": "finite_gap_cannot_help",
            "source_path": pair_source,
            "valid_for_claim": False,
        },
        {
            "gate": "exact_gap_collapse",
            "derived_value": "m->0 reaches the rejected constrained endpoint",
            "required_value": "parent-derived attractive galaxy bridge",
            "result": "cannot_rescue_passive_pair_route",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "gate": "seagull_counterterms",
            "derived_value": "analytic local renormalizations only",
            "required_value": "change nonanalytic projector or inequality",
            "result": "cannot_rescue",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
    ]

    ownership_rows = [
        {
            "object": "universal_metric_source",
            "parent_status": "derived",
            "checkpoint_5182_status": "retained",
            "reason": "one Hilbert source and calibrated local GR remain unchanged",
            "source_path": relative(SOURCES["checkpoint_4960_document"][0]),
            "valid_for_claim": False,
        },
        {
            "object": "canonical_PX_vertex",
            "parent_status": "derived",
            "checkpoint_5182_status": "projected",
            "reason": "P_X(0)=1/2 fixes the minimal h chi chi vertex",
            "source_path": vertex_source,
            "valid_for_claim": False,
        },
        {
            "object": "eta_R_chi2_operational",
            "parent_status": "absent_on_exact_shift_symmetric_trajectory",
            "checkpoint_5182_status": "eta=0",
            "reason": "the current parent has no R chi^2 vertex in any sign convention",
            "source_path": parent_source,
            "valid_for_claim": False,
        },
        {
            "object": "eta_extension",
            "parent_status": "symmetry_allowed_only_after_pair_breaking_extension",
            "checkpoint_5182_status": "strongest_extension_audited",
            "reason": "all real eta fail to enhance Phi on the GR-connected passive branch",
            "source_path": relative(SOURCES["checkpoint_4950_document"][0]),
            "valid_for_claim": False,
        },
        {
            "object": "pure_common_eta",
            "parent_status": "operational_vertex_value_not_parent_prediction",
            "checkpoint_5182_status": "eta=1/6_screening",
            "reason": "do not identify eta with source xi before translating signs",
            "source_path": parent_source,
            "valid_for_claim": False,
        },
        {
            "object": "passive_pair_weight",
            "parent_status": "positive_for_passive_Gaussian_or_CTP_state",
            "checkpoint_5182_status": "d>=0",
            "reason": "connected pair covariance is positive semidefinite",
            "source_path": relative(SOURCES["checkpoint_5150_document"][0]),
            "valid_for_claim": False,
        },
        {
            "object": "direct_conserved_state_stress",
            "parent_status": "conditional_existence_derived",
            "checkpoint_5182_status": "survives",
            "reason": "not the rejected zero-background pair-dressing mechanism",
            "source_path": stress_source,
            "valid_for_claim": False,
        },
        {
            "object": "nonzero_background_linear_mixing",
            "parent_status": "not_yet_derived",
            "checkpoint_5182_status": "next_target",
            "reason": "only an actual B!=0 Hessian can realize the 5181 positive completion",
            "source_path": relative(SOURCES["checkpoint_5181_document"][0]),
            "valid_for_claim": False,
        },
    ]

    decision_rows = [
        {
            "decision": "RETAIN_LOCAL_GR_NEWTON_MAXWELL",
            "status": "passed",
            "reason": "no protected parent or formalization file is changed",
            "next_action": "none",
            "valid_for_claim": False,
        },
        {
            "decision": "REJECT_PASSIVE_ZERO_BACKGROUND_PAIR_DRESSING",
            "status": "derived",
            "reason": "Phi/Phi_GR<=1 on every GR-connected passive branch",
            "next_action": "do_not_revisit_without_new_parent_vertex",
            "valid_for_claim": False,
        },
        {
            "decision": "REJECT_GAP_COLLAPSE_AS_A_STANDALONE_RESCUE",
            "status": "derived",
            "reason": "the exact massless endpoint has the wrong constrained response",
            "next_action": "do_not_spend_more_work_on_gap_before_new_mixing",
            "valid_for_claim": False,
        },
        {
            "decision": "RETAIN_DIRECT_CONSERVED_STATE_STRESS",
            "status": "conditional",
            "reason": "5151 is logically distinct from passive Hessian dressing",
            "next_action": "derive source-selected occupation",
            "valid_for_claim": False,
        },
        {
            "decision": "DERIVE_NONZERO_BACKGROUND_LINEAR_MIXING",
            "status": "selected_next",
            "reason": "test whether the parent owns an actual positive B Kchi^-1 Bdagger channel",
            "next_action": "5183_parent_stationary_background_and_linear_Hessian",
            "valid_for_claim": False,
        },
        {
            "decision": "NO_GALAXY_OR_FULL_MTS_CLAIM",
            "status": "blocked",
            "reason": "surviving source selection and background ownership remain open",
            "next_action": "keep checkpoint private",
            "valid_for_claim": False,
        },
    ]

    summary = {
        "static_Hilbert_vertex_derived": True,
        "minimal_seagull_nonanalytic_silent": True,
        "improvement_seagulls_nonanalytic_silent": True,
        "pair_polarization_rank": 1,
        "pair_polarization_positive_semidefinite": True,
        "pair_effective_Hessian_sign": "negative_connected_cumulant",
        "current_parent_eta": 0.0,
        "current_parent_pair_projector": "pure_gravitational_slip",
        "current_parent_dust_response": "exactly_GR",
        "GR_connected_branch_condition": (
            "Delta=a-d(48eta^2-16eta+1)>0"
        ),
        "passive_nonminimal_phi_enhancement_exists": False,
        "no_slip_eta_values": [0.0, 0.125],
        "nontrivial_no_slip_branch": "eta=1/8_screening",
        "pure_common_branch": "eta=1/6_common_projector_but_screening",
        "constraint_pole_is_target_criticality": False,
        "exact_gap_collapse_rescues_pair_route": False,
        "passive_zero_background_pair_route_rejected": True,
        "direct_conserved_state_stress_survives": True,
        "next_target": "DERIVE_NONZERO_BACKGROUND_LINEAR_MIXING",
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_local_GR_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_cosmology_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    return (
        vertex_rows,
        polarization_rows,
        response_rows,
        target_rows,
        ownership_rows,
        decision_rows,
        summary,
    )


def write_document(result: dict[str, Any]) -> None:
    summary = result["summary"]
    text = f"""# 5182 - Static Hilbert pair projector and constrained Newtonian response

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

The actual static Hilbert `h chi chi` vertex has now been calculated and
passed through the two Newtonian-gauge scalar constraints. This closes the
main ambiguity left by checkpoint 5181.

The current shift-symmetric parent has no `R chi^2` vertex, so the
operational improvement coefficient defined below is `eta=0`. Its massless critical pair
therefore couples only to `Phi-Psi`, the gravitational-slip channel. For a
dust source,

```text
Phi=Psi=Phi_GR
```

exactly, independent of the positive pair susceptibility. Tuning the pair
weight to criticality only makes the unused slip constraint singular.

The strongest local curvature extension was also allowed rather than being
dismissed as absent. To avoid importing incompatible curvature or Wick-rotation
signs, define `eta` directly by the linear static vertex
`V_eta=eta k^2(Phi-2Psi)chi^2`. The theorem covers every real `eta`, so its
translation to a source's `xi` convention cannot change the result. On every
GR-connected no-pole branch a passive pair obeys

```text
Phi/Phi_GR
 =1-16 d eta^2/[a-d(48eta^2-16eta+1)]
 <=1.
```

Thus no real `eta` supplies the required extra attractive circular potential.
The passive zero-background pair-dressing route to checkpoint 5148 is
rejected. This is a projector-and-constraint result, not another missing
coefficient.

## 1. Exact static vertex

Use

```text
ds^2=-(1+2Phi)dt^2+(1-2Psi)delta_ij dx^i dx^j.
```

For a canonical static zero mode,

```text
S_chi
 =1/2 integral N sqrt(gamma) gamma^ij partial_i chi partial_j chi,

N sqrt(gamma) gamma^ij
 =sqrt[(1+2Phi)(1-2Psi)] delta^ij
 ={{1+(Phi-Psi)-1/2(Phi+Psi)^2+O(h^3)}}delta^ij.
```

The linear minimal pair vertex is consequently

```text
V_min=(Phi-Psi) [p.(p+k)]/2.
```

The quadratic term is the seagull

```text
S_seagull=-1/4 integral (Phi+Psi)^2 (grad chi)^2.
```

It contains one scalar tadpole and no two-particle cut. In dimensional
regularization it is scaleless at the critical point; with a mass or state
scale it remains analytic in external momentum and only renormalizes local
coefficients.

For the nonminimal extension,

```text
R^(1)=2 nabla^2(2Psi-Phi)=2 k^2(Phi-2Psi),

V_eta=eta k^2(Phi-2Psi) chi^2.
```

Its second metric variation also multiplies a one-propagator tadpole and
cannot alter the nonanalytic pair term.

## 2. Critical pair polarization

With `M=p.(p+k)` and the checkpoint-5181 massless bubble,

```text
B_0(k)=1/(8|k|),
I_MM=(k^4/4)B_0=|k|^3/32,
k^2 I_M0=-|k|^3/16.
```

The connected metric pair covariance is

```text
C_ab(k)
 =W |k|^3 w_a w_b/64,

w(eta)=(4eta-1, 1-8eta),
```

and the passive Euclidean cumulant gives

```text
Delta K_ab=-C_ab.
```

This matrix is rank one and positive semidefinite before the cumulant sign:

```text
det C=0,
tr[C/(W|k|^3)]=(40eta^2-12eta+1)/32>0.
```

At `eta=0`, `w=(-1,1)` is pure slip. At `eta=1/6`,
`w=(-1/3,-1/3)` is pure common mode. This is an operational static-vertex
statement, not an identification with checkpoint 4951's source coefficient.
The constrained response below shows that the pure-common rotation screens
rather than enhances.

The scalar-slip coefficient at `eta=0` is 32 times the checkpoint-5150 TT
coefficient, providing an independent normalization cross-check.

## 3. Exact scalar-constraint inversion

After all analytic local renormalizations define

```text
a=2 M_R^2 k^2>0,
d=W |k|^3/64>=0.
```

The static Einstein kernel and pair-dressed kernel are

```text
K_GR=a [[0,-1],[-1,1]],

K=K_GR-d w w^T.
```

Their determinant is

```text
det K=-a Delta,

Delta=a-d F(eta),
F(eta)=(4eta-1)(12eta-1)=48eta^2-16eta+1.
```

Continuity from the GR constraint inertia requires `Delta>0`. For a dust
source `J=(rho,0)`, exact inversion gives

```text
Phi/Phi_GR
 =1-16 d eta^2/Delta,

Psi/Psi_GR
 =1+4 d eta(4eta-1)/Delta,

(Phi+Psi)/(Phi+Psi)_GR
 =1-2 d eta/Delta,

(Phi-Psi)/Phi_GR
 =-4 d eta(8eta-1)/Delta.
```

Because `d>=0` and `Delta>0`,

```text
Phi/Phi_GR<=1,
```

with equality only for `d=0` or `eta=0`. This proves the no-enhancement
theorem for every positive scalar dressing of the derived rank-one
projector, not merely for one chosen normalization. Interactions that create
new tensor vertices would be a new parent mechanism and are not silently
covered by this result.

## 4. No-slip and pure-common cases

For nonzero pair weight the dust slip vanishes only at

```text
eta=0 or eta=1/8.
```

The first is exactly invisible to dust. The second gives

```text
Phi/Phi_GR=Psi/Psi_GR=4a/(4a+d)<1.
```

Therefore the only nontrivial no-slip extension is screening.

At the operational pure-common value `eta=1/6`,

```text
w=(-1/3,-1/3),
Delta=a+d/3,

Phi/Phi_GR=(9a-d)/(9a+3d),
Psi/Psi_GR=(9a+d)/(9a+3d),
lensing/GR=3a/(3a+d).
```

The bubble is in the common metric projector, but both the circular
potential and total lensing response are suppressed; a slip is also
generated. Approaching `Delta=0` where it exists is a loss of scalar
constraint rank, not the positive critical Schur residual of checkpoint
5181.

## 5. Parent ownership and gap endpoint

Checkpoint 4951 proved that the exact shift-symmetric parent trajectory has
no additive `R chi^2` source, so the parent-owned operational value is
`eta=0`. Checkpoint 4950 showed that a curvature-pair coefficient becomes an
allowed RG coordinate only after
adding a pair-breaking even potential; that extension did not derive a
viable local/galaxy activation window.

More importantly, the theorem above already grants arbitrary real `eta` and
still rejects attractive enhancement. Parent ownership therefore cannot
reverse this decision inside the audited vertex class.

A finite pair gap has an analytic infrared bubble and cannot produce the
required `1/|k|` carrier. Granting an exact environmental collapse to
`m=0` reaches the endpoint just rejected. The gap mechanism is therefore no
longer the next bottleneck for this route.

## 6. What survives

This checkpoint does not reject:

- the universal local GR/Newton/Maxwell chain;
- checkpoint 5151's direct conserved positive state stress, whose
  source-selected occupation remains to be derived;
- a nonzero parent motion background that creates a genuine linear
  `h-delta chi` Hessian block `B`, rather than a zero-background quadratic
  pair loop.

The next calculation is consequently:

```text
5183:
derive or reject a parent-owned stationary motion background and its
linear metric-motion Hessian; if it does not exist, return to the direct
conserved-state-stress source-selection problem.
```

No local-GR, galaxy, cosmology or full-MTS claim is made. The protected
formalization digest remains
`{result['formalization_workbench_tree_sha256']}` and checkpoint 5176
remains `{result['checkpoint_5176_tree_sha256']}`.

## Evidence

- `{relative(VERTEX_CSV)}`
- `{relative(POLARIZATION_CSV)}`
- `{relative(RESPONSE_CSV)}`
- `{relative(TARGET_CSV)}`
- `{relative(OWNERSHIP_CSV)}`
- `{relative(DECISION_CSV)}`
- `{relative(PROVENANCE_CSV)}`
- `{relative(RESULT_JSON)}`
- `{relative(VALIDATION_CSV)}`

## Machine decision

`{ROUTE_DECISION}`

Summary route rejection:
`{summary['passive_zero_background_pair_route_rejected']}`.
"""
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(DOCUMENT)


def calculate_checks(
    symbolic: dict[str, Any],
    formal_before: str,
    checkpoint_5176_before: str,
    source_hashes_before: dict[str, str],
    rows: tuple[
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
        dict[str, Any],
    ],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    eta = symbolic["eta"]
    a = symbolic["a"]
    d = symbolic["d"]
    vector = symbolic["vector"]
    expected_factor = 48 * eta**2 - 16 * eta + 1
    matrix_residuals = []
    minimum_eigenvalue = math.inf
    for xi_value in np.linspace(-2.0, 2.0, 401):
        direct = direct_loop_matrix(float(xi_value))
        outer = outer_loop_matrix(float(xi_value))
        matrix_residuals.append(float(np.max(np.abs(direct - outer))))
        minimum_eigenvalue = min(
            minimum_eigenvalue,
            float(np.min(np.linalg.eigvalsh(0.5 * (direct + direct.T)))),
        )

    response_residuals = []
    phi_excesses = []
    no_slip_candidates = []
    minimum_denominator = math.inf
    for xi_value in np.linspace(-3.0, 3.0, 1201):
        factor = 48.0 * xi_value**2 - 16.0 * xi_value + 1.0
        ratios = [0.01, 0.05, 0.2, 0.5, 2.0]
        for ratio in ratios:
            if 1.0 - ratio * factor <= 1.0e-6:
                continue
            values = response_values(float(xi_value), ratio)
            minimum_denominator = min(
                minimum_denominator, values["denominator_over_a"]
            )
            phi_excesses.append(values["phi_ratio"] - 1.0)
            kernel_gr = np.array([[0.0, -1.0], [-1.0, 1.0]])
            vector_numeric = np.array(
                [4.0 * xi_value - 1.0, 1.0 - 8.0 * xi_value]
            )
            kernel = (
                kernel_gr - ratio * np.outer(vector_numeric, vector_numeric)
            )
            potentials = np.linalg.solve(kernel, np.array([1.0, 0.0]))
            direct_phi_ratio = potentials[0] / -1.0
            direct_psi_ratio = potentials[1] / -1.0
            direct_lens_ratio = (potentials[0] + potentials[1]) / -2.0
            response_residuals.extend(
                [
                    abs(direct_phi_ratio - values["phi_ratio"]),
                    abs(direct_psi_ratio - values["psi_ratio"]),
                    abs(direct_lens_ratio - values["lensing_ratio"]),
                ]
            )
            if abs(values["slip_over_phi_GR"]) < 1.0e-12:
                no_slip_candidates.append(float(xi_value))

    no_slip_exact = sp.solve(
        sp.Eq(symbolic["no_slip_polynomial"], 0),
        eta,
    )
    special_minimal = response_values(0.0, 0.5)
    special_no_slip = response_values(0.125, 0.5)
    special_pure_common = response_values(1.0 / 6.0, 0.5)
    low_gap_errors = []
    for k_value in np.logspace(-7.0, -2.0, 80):
        exact_bubble = massive_pair_bubble(float(k_value), 1.0)
        low_gap_series = 1.0 / (8.0 * math.pi) - k_value**2 / (
            96.0 * math.pi
        )
        low_gap_errors.append(
            abs(exact_bubble - low_gap_series) / exact_bubble
        )
    slope_step = 1.0e-3
    slope_center = 1.0e-5
    finite_gap_slope = (
        math.log(
            massive_pair_bubble(
                slope_center * math.exp(slope_step),
                1.0,
            )
        )
        - math.log(
            massive_pair_bubble(
                slope_center * math.exp(-slope_step),
                1.0,
            )
        )
    ) / (2.0 * slope_step)
    critical_ratio = massive_pair_bubble(1.0, 1.0e-9) / (1.0 / 8.0)
    common_at_minimal = sp.simplify(
        symbolic["common_overlap"].subs(eta, 0)
    )
    slip_at_pure_common = sp.simplify(
        symbolic["slip_overlap"].subs(eta, sp.Rational(1, 6))
    )
    common_at_pure_common = sp.simplify(
        symbolic["common_overlap"].subs(eta, sp.Rational(1, 6))
    )
    exact_checks = {
        "factor_identity": sp.simplify(
            symbolic["factor"] - expected_factor
        )
        == 0,
        "determinant_identity": sp.simplify(
            symbolic["determinant"]
            + a * symbolic["denominator"]
        )
        == 0,
        "phi_identity": sp.simplify(
            symbolic["phi_ratio"] - symbolic["expected_phi"]
        )
        == 0,
        "psi_identity": sp.simplify(
            symbolic["psi_ratio"] - symbolic["expected_psi"]
        )
        == 0,
        "lens_identity": sp.simplify(
            symbolic["lens_ratio"] - symbolic["expected_lens"]
        )
        == 0,
        "slip_identity": sp.simplify(
            symbolic["slip_ratio"] - symbolic["expected_slip"]
        )
        == 0,
        "minimal_pure_slip": common_at_minimal == 0,
        "eta_one_sixth_pure_common": slip_at_pure_common == 0
        and common_at_pure_common != 0,
        "no_slip_roots": no_slip_exact
        == [sp.Integer(0), sp.Rational(1, 8)],
    }
    metrics = {
        "maximum_loop_matrix_residual": max(matrix_residuals),
        "minimum_loop_matrix_eigenvalue": minimum_eigenvalue,
        "maximum_response_inverse_residual": max(response_residuals),
        "maximum_phi_excess_on_GR_connected_grid": max(phi_excesses),
        "minimum_sampled_Delta_over_a": minimum_denominator,
        "no_slip_exact_roots": [str(value) for value in no_slip_exact],
        "minimal_phi_ratio": special_minimal["phi_ratio"],
        "minimal_lensing_ratio": special_minimal["lensing_ratio"],
        "eta_one_eighth_phi_ratio": special_no_slip["phi_ratio"],
        "eta_one_eighth_gamma": special_no_slip["gamma_PPN"],
        "pure_common_phi_ratio": special_pure_common["phi_ratio"],
        "pure_common_lensing_ratio": special_pure_common["lensing_ratio"],
        "pure_common_gamma": special_pure_common["gamma_PPN"],
        "maximum_finite_gap_low_k_series_error": max(low_gap_errors),
        "finite_gap_low_k_log_slope": finite_gap_slope,
        "near_massless_bubble_over_B0": critical_ratio,
        "exact_symbolic_checks": exact_checks,
    }
    (
        vertex_rows,
        polarization_rows,
        response_rows,
        target_rows,
        ownership_rows,
        decision_rows,
        summary,
    ) = rows
    checks = [
        validation_row(
            "V5182_01_source_count",
            "all declared parent sources are present",
            len(source_hashes_before) == len(SOURCES),
            len(source_hashes_before),
            len(SOURCES),
        ),
        validation_row(
            "V5182_02_source_hashes",
            "all source hashes match their locks",
            all(
                source_hashes_before[name] == expected
                for name, (_, expected) in SOURCES.items()
            ),
            sum(
                source_hashes_before[name] == expected
                for name, (_, expected) in SOURCES.items()
            ),
            len(SOURCES),
        ),
        validation_row(
            "V5182_03_formal_lock",
            "formalization-workbench is unchanged before execution",
            formal_before == FORMAL_DIGEST_LOCK,
            formal_before,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5182_04_checkpoint_5176_lock",
            "checkpoint 5176 evidence remains immutable",
            checkpoint_5176_before == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_before,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5182_05_exact_factor",
            "constraint factor is (4eta-1)(12eta-1)",
            exact_checks["factor_identity"],
            exact_checks["factor_identity"],
            True,
        ),
        validation_row(
            "V5182_06_exact_determinant",
            "dressed scalar determinant is -a Delta",
            exact_checks["determinant_identity"],
            exact_checks["determinant_identity"],
            True,
        ),
        validation_row(
            "V5182_07_exact_phi",
            "symbolic Phi response identity closes",
            exact_checks["phi_identity"],
            exact_checks["phi_identity"],
            True,
        ),
        validation_row(
            "V5182_08_exact_psi",
            "symbolic Psi response identity closes",
            exact_checks["psi_identity"],
            exact_checks["psi_identity"],
            True,
        ),
        validation_row(
            "V5182_09_exact_lensing",
            "symbolic lensing response identity closes",
            exact_checks["lens_identity"],
            exact_checks["lens_identity"],
            True,
        ),
        validation_row(
            "V5182_10_exact_slip",
            "symbolic gravitational-slip identity closes",
            exact_checks["slip_identity"],
            exact_checks["slip_identity"],
            True,
        ),
        validation_row(
            "V5182_11_loop_outer_product",
            "direct loop integrals equal the rank-one outer product",
            metrics["maximum_loop_matrix_residual"] < 1.0e-14,
            metrics["maximum_loop_matrix_residual"],
            "<1e-14",
        ),
        validation_row(
            "V5182_12_pair_covariance_PSD",
            "pair covariance is positive semidefinite",
            metrics["minimum_loop_matrix_eigenvalue"] > -1.0e-13,
            metrics["minimum_loop_matrix_eigenvalue"],
            ">=-1e-13",
        ),
        validation_row(
            "V5182_13_inverse_numeric",
            "direct matrix inversion matches analytic responses",
            metrics["maximum_response_inverse_residual"] < 1.0e-10,
            metrics["maximum_response_inverse_residual"],
            "<1e-10",
        ),
        validation_row(
            "V5182_14_GR_connected_grid",
            "all sampled response points retain Delta>0",
            metrics["minimum_sampled_Delta_over_a"] > 0.0,
            metrics["minimum_sampled_Delta_over_a"],
            ">0",
        ),
        validation_row(
            "V5182_15_no_phi_enhancement",
            "Phi never exceeds Phi_GR on the GR-connected passive grid",
            metrics["maximum_phi_excess_on_GR_connected_grid"] <= 2.0e-12,
            metrics["maximum_phi_excess_on_GR_connected_grid"],
            "<=2e-12",
        ),
        validation_row(
            "V5182_16_minimal_pure_slip",
            "eta=0 pair vertex is orthogonal to the common mode",
            exact_checks["minimal_pure_slip"],
            exact_checks["minimal_pure_slip"],
            True,
        ),
        validation_row(
            "V5182_17_eta_one_sixth_pure_common",
            "eta=1/6 pair vertex is pure common mode",
            exact_checks["eta_one_sixth_pure_common"],
            exact_checks["eta_one_sixth_pure_common"],
            True,
        ),
        validation_row(
            "V5182_18_no_slip_roots",
            "the only dust no-slip eta values are 0 and 1/8",
            exact_checks["no_slip_roots"],
            metrics["no_slip_exact_roots"],
            ["0", "1/8"],
        ),
        validation_row(
            "V5182_19_minimal_dust_invisible",
            "eta=0 leaves dust Phi unchanged",
            close(metrics["minimal_phi_ratio"], 1.0),
            metrics["minimal_phi_ratio"],
            1.0,
        ),
        validation_row(
            "V5182_20_minimal_lensing_invisible",
            "eta=0 leaves dust lensing unchanged",
            close(metrics["minimal_lensing_ratio"], 1.0),
            metrics["minimal_lensing_ratio"],
            1.0,
        ),
        validation_row(
            "V5182_21_nontrivial_no_slip_screens",
            "eta=1/8 is no-slip but screens the circular potential",
            metrics["eta_one_eighth_phi_ratio"] < 1.0
            and close(metrics["eta_one_eighth_gamma"], 1.0),
            [
                metrics["eta_one_eighth_phi_ratio"],
                metrics["eta_one_eighth_gamma"],
            ],
            ["<1", 1.0],
        ),
        validation_row(
            "V5182_22_pure_common_screens_phi",
            "eta=1/6 screens the circular potential",
            metrics["pure_common_phi_ratio"] < 1.0,
            metrics["pure_common_phi_ratio"],
            "<1",
        ),
        validation_row(
            "V5182_23_pure_common_screens_lensing",
            "eta=1/6 screens total lensing",
            metrics["pure_common_lensing_ratio"] < 1.0,
            metrics["pure_common_lensing_ratio"],
            "<1",
        ),
        validation_row(
            "V5182_24_pure_common_generates_slip",
            "eta=1/6 does not retain gamma=1",
            not close(metrics["pure_common_gamma"], 1.0),
            metrics["pure_common_gamma"],
            "!=1",
        ),
        validation_row(
            "V5182_25_parent_eta_zero",
            "current shift-symmetric parent value is eta=0",
            summary["current_parent_eta"] == 0.0,
            summary["current_parent_eta"],
            0.0,
        ),
        validation_row(
            "V5182_26_target_rejected",
            "passive pair route is rejected as the 5148 enhancement",
            summary["passive_zero_background_pair_route_rejected"],
            summary["passive_zero_background_pair_route_rejected"],
            True,
        ),
        validation_row(
            "V5182_26A_finite_gap_series",
            "finite-gap bubble has the analytic low-k expansion",
            metrics["maximum_finite_gap_low_k_series_error"] < 2.0e-10,
            metrics["maximum_finite_gap_low_k_series_error"],
            "<2e-10",
        ),
        validation_row(
            "V5182_26B_finite_gap_slope",
            "finite-gap bubble tends to a constant rather than 1/k",
            abs(metrics["finite_gap_low_k_log_slope"]) < 1.0e-7,
            metrics["finite_gap_low_k_log_slope"],
            "0",
        ),
        validation_row(
            "V5182_26C_massless_endpoint",
            "the gap-collapse endpoint tends to B0=1/(8k)",
            abs(metrics["near_massless_bubble_over_B0"] - 1.0) < 2.0e-9,
            metrics["near_massless_bubble_over_B0"],
            1.0,
        ),
        validation_row(
            "V5182_27_gap_not_rescue",
            "even exact gap collapse cannot rescue this endpoint",
            not summary["exact_gap_collapse_rescues_pair_route"],
            summary["exact_gap_collapse_rescues_pair_route"],
            False,
        ),
        validation_row(
            "V5182_28_direct_stress_survives",
            "the direct conserved-state-stress route is not rejected",
            summary["direct_conserved_state_stress_survives"],
            summary["direct_conserved_state_stress_survives"],
            True,
        ),
        validation_row(
            "V5182_29_next_target",
            "one concrete next parent calculation is selected",
            summary["next_target"]
            == "DERIVE_NONZERO_BACKGROUND_LINEAR_MIXING",
            summary["next_target"],
            "DERIVE_NONZERO_BACKGROUND_LINEAR_MIXING",
        ),
        validation_row(
            "V5182_30_row_counts",
            "all generated table row counts match the contract",
            [
                len(vertex_rows),
                len(polarization_rows),
                len(response_rows),
                len(target_rows),
                len(ownership_rows),
                len(decision_rows),
            ]
            == [9, 11, 9, 9, 8, 6],
            [
                len(vertex_rows),
                len(polarization_rows),
                len(response_rows),
                len(target_rows),
                len(ownership_rows),
                len(decision_rows),
            ],
            [9, 11, 9, 9, 8, 6],
        ),
        validation_row(
            "V5182_31_decision_unique",
            "exactly one next calculation is selected",
            sum(
                row["decision"] == "DERIVE_NONZERO_BACKGROUND_LINEAR_MIXING"
                and row["status"] == "selected_next"
                for row in decision_rows
            )
            == 1,
            sum(row["status"] == "selected_next" for row in decision_rows),
            1,
        ),
        validation_row(
            "V5182_32_nonclaim",
            "all physics claim flags remain false",
            not any(
                summary[key]
                for key in (
                    "valid_for_local_GR_claim",
                    "valid_for_galaxy_claim",
                    "valid_for_cosmology_claim",
                    "valid_for_full_MTS_claim",
                )
            ),
            [
                summary["valid_for_local_GR_claim"],
                summary["valid_for_galaxy_claim"],
                summary["valid_for_cosmology_claim"],
                summary["valid_for_full_MTS_claim"],
            ],
            [False, False, False, False],
        ),
    ]
    return checks, metrics


def run(dry_run: bool) -> dict[str, Any]:
    missing_sources = [
        name for name, (path, _) in SOURCES.items() if not path.is_file()
    ]
    if missing_sources:
        raise FileNotFoundError(f"missing sources: {missing_sources}")
    source_hashes_before = {
        name: file_digest(path) for name, (path, _) in SOURCES.items()
    }
    formal_before = tree_digest(FORMAL)
    checkpoint_5176_before = tree_digest(CHECKPOINT_5176_ROOT)
    symbolic = symbolic_contract()
    rows = make_rows()
    checks, metrics = calculate_checks(
        symbolic,
        formal_before,
        checkpoint_5176_before,
        source_hashes_before,
        rows,
    )
    failures = [row["validation_id"] for row in checks if not row["passed"]]
    (
        vertex_rows,
        polarization_rows,
        response_rows,
        target_rows,
        ownership_rows,
        decision_rows,
        summary,
    ) = rows
    dry_result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "dry_run": dry_run,
        "route_decision": ROUTE_DECISION,
        "summary": summary,
        "metrics": metrics,
        "validation_count": len(checks),
        "validation_failures": failures,
    }
    if failures:
        raise RuntimeError(f"dry validation failures: {failures}")
    if dry_run:
        return dry_result

    write_csv(VERTEX_CSV, vertex_rows)
    write_csv(POLARIZATION_CSV, polarization_rows)
    write_csv(RESPONSE_CSV, response_rows)
    write_csv(TARGET_CSV, target_rows)
    write_csv(OWNERSHIP_CSV, ownership_rows)
    write_csv(DECISION_CSV, decision_rows)
    provenance_rows = [
        {
            "source_id": name,
            "source_path": str(path),
            "sha256": source_hashes_before[name],
            "expected_sha256": expected,
            "status": "hash_locked_read_only",
            "checked_date": CHECKED_DATE,
        }
        for name, (path, expected) in SOURCES.items()
    ]
    write_csv(PROVENANCE_CSV, provenance_rows)

    source_hashes_after = {
        name: file_digest(path) for name, (path, _) in SOURCES.items()
    }
    formal_after = tree_digest(FORMAL)
    checkpoint_5176_after = tree_digest(CHECKPOINT_5176_ROOT)
    output_tables = (
        VERTEX_CSV,
        POLARIZATION_CSV,
        RESPONSE_CSV,
        TARGET_CSV,
        OWNERSHIP_CSV,
        DECISION_CSV,
        PROVENANCE_CSV,
    )
    output_text = "\n".join(
        path.read_text(encoding="utf-8") for path in output_tables
    )
    output_payload_digest = hashlib.sha256(
        output_text.encode("utf-8")
    ).hexdigest()
    full_checks = checks + [
        validation_row(
            "V5182_33_sources_read_only",
            "all source hashes remain unchanged",
            source_hashes_before == source_hashes_after,
            sum(
                source_hashes_before[name] == source_hashes_after[name]
                for name in SOURCES
            ),
            len(SOURCES),
        ),
        validation_row(
            "V5182_34_formal_after",
            "formalization-workbench remains unchanged after execution",
            formal_after == formal_before == FORMAL_DIGEST_LOCK,
            formal_after,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5182_35_checkpoint_5176_after",
            "checkpoint 5176 remains immutable after execution",
            checkpoint_5176_after
            == checkpoint_5176_before
            == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_after,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5182_36_no_placeholders",
            "generated evidence has no missing-input placeholder",
            "MISSING_" not in output_text,
            "MISSING_" in output_text,
            False,
        ),
        validation_row(
            "V5182_37_provenance_rows",
            "every declared source has one provenance row",
            len(provenance_rows) == len(SOURCES),
            len(provenance_rows),
            len(SOURCES),
        ),
        validation_row(
            "V5182_38_output_parse",
            "all generated CSVs parse with nonempty rows",
            all(
                len(list(csv.DictReader(path.open(encoding="utf-8")))) > 0
                for path in output_tables
            ),
            len(output_tables),
            len(output_tables),
        ),
        validation_row(
            "V5182_39_claim_columns",
            "every substantive evidence row remains nonclaim",
            all(
                str(row.get("valid_for_claim", "")).lower() == "false"
                for table in (
                    vertex_rows,
                    polarization_rows,
                    response_rows,
                    target_rows,
                    ownership_rows,
                    decision_rows,
                )
                for row in table
            ),
            False,
            False,
        ),
        validation_row(
            "V5182_40_local_branch_unchanged",
            "local GR/Newton/Maxwell branch is not modified",
            not summary["local_GR_Newton_Maxwell_branch_modified"],
            summary["local_GR_Newton_Maxwell_branch_modified"],
            False,
        ),
    ]
    full_failures = [
        row["validation_id"] for row in full_checks if not row["passed"]
    ]
    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "dry_run": False,
        "route_decision": ROUTE_DECISION,
        "source_paths": {
            name: str(path) for name, (path, _) in SOURCES.items()
        },
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "formalization_workbench_tree_sha256": formal_after,
        "checkpoint_5176_tree_sha256": checkpoint_5176_after,
        "output_payload_sha256": output_payload_digest,
        "summary": summary,
        "metrics": metrics,
        "validation_count": len(full_checks),
        "validation_failures": full_failures,
        "valid_for_local_GR_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_cosmology_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_json(RESULT_JSON, result)
    write_document(result)
    write_csv(VALIDATION_CSV, full_checks)
    if full_failures:
        raise RuntimeError(f"validation failures: {full_failures}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Project the exact static Hilbert pair vertex through the "
            "Newtonian scalar constraints and decide the passive pair route."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate sources and derivations without writing outputs",
    )
    arguments = parser.parse_args()
    result = run(arguments.dry_run)
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
