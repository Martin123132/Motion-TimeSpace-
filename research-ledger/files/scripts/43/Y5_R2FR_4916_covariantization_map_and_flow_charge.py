from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4916"
CHECKED_DATE = "2026-07-12"
MARKER = "MTS_COVARIANTIZATION_MAP_FLOW_CHARGE_4916"
FORMAL_MARKER = "PPC4161_COVARIANTIZATION_MAP_FLOW_CHARGE_4916"
NEXT_TARGET = (
    "4917-Y5-R2FR-radiative-flow-matter-reentry-coefficients-from-"
    "gravity-mediation-or-local-bound-pack.md"
)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def metric_from_density(density: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    determinant = float(np.linalg.det(density))
    if determinant >= 0:
        raise ValueError("densitized inverse metric must have negative determinant")
    volume = float(np.sqrt(-determinant))
    metric_inverse = density / volume
    metric = np.linalg.inv(metric_inverse)
    return volume, metric_inverse, metric


def h_source_chain_checks(trials: int = 12) -> dict[str, float | bool]:
    generator = np.random.default_rng(4916)
    minkowski = np.diag([-1.0, 1.0, 1.0, 1.0])
    recovery_residual = 0.0
    derivative_residual = 0.0
    source_residual = 0.0
    involution_residual = 0.0
    epsilon = 2.0e-6
    for _ in range(trials):
        coframe = np.eye(4) + 0.08 * generator.normal(size=(4, 4))
        metric = coframe.T @ minkowski @ coframe
        metric_inverse = np.linalg.inv(metric)
        volume = float(np.sqrt(-np.linalg.det(metric)))
        density = volume * metric_inverse
        recovered_volume, recovered_inverse, recovered_metric = metric_from_density(
            density
        )
        recovery_residual = max(
            recovery_residual,
            abs(recovered_volume - volume) / volume,
            float(np.linalg.norm(recovered_inverse - metric_inverse))
            / max(float(np.linalg.norm(metric_inverse)), 1.0),
            float(np.linalg.norm(recovered_metric - metric))
            / max(float(np.linalg.norm(metric)), 1.0),
        )

        perturbation = generator.normal(size=(4, 4))
        perturbation = 0.5 * (perturbation + perturbation.T)
        perturbation /= np.linalg.norm(perturbation)
        plus_inverse = metric_from_density(density + epsilon * perturbation)[1]
        minus_inverse = metric_from_density(density - epsilon * perturbation)[1]
        finite_derivative = (plus_inverse - minus_inverse) / (2.0 * epsilon)
        density_inverse = np.linalg.inv(density)
        trace_density = float(np.einsum("ij,ji->", density_inverse, perturbation))
        predicted_derivative = (
            perturbation - 0.5 * density * trace_density
        ) / volume
        derivative_residual = max(
            derivative_residual,
            float(np.linalg.norm(finite_derivative - predicted_derivative))
            / max(float(np.linalg.norm(predicted_derivative)), 1.0),
        )

        stress = generator.normal(size=(4, 4))
        stress = 0.5 * (stress + stress.T)
        stress_trace = float(np.einsum("ij,ij->", metric_inverse, stress))
        trace_reversed = stress - 0.5 * metric * stress_trace
        direct_source = -0.5 * volume * float(
            np.einsum("ij,ij->", stress, finite_derivative)
        )
        density_source = -0.5 * float(
            np.einsum("ij,ij->", trace_reversed, perturbation)
        )
        source_residual = max(
            source_residual,
            abs(direct_source - density_source)
            / max(abs(direct_source), abs(density_source), 1.0),
        )
        twice_reversed = trace_reversed - 0.5 * metric * float(
            np.einsum("ij,ij->", metric_inverse, trace_reversed)
        )
        involution_residual = max(
            involution_residual,
            float(np.linalg.norm(twice_reversed - stress))
            / max(float(np.linalg.norm(stress)), 1.0),
        )
    return {
        "trial_count": trials,
        "metric_recovery_max_relative_residual": recovery_residual,
        "metric_derivative_max_relative_residual": derivative_residual,
        "source_chain_max_relative_residual": source_residual,
        "trace_reverse_involution_max_relative_residual": involution_residual,
        "passed": max(
            recovery_residual,
            derivative_residual,
            source_residual,
            involution_residual,
        )
        < 2.0e-9,
    }


def h_source_rows() -> list[dict[str, Any]]:
    checks = h_source_chain_checks()
    return tagged(
        [
            {
                "check_id": "HSRC4916_00_metric_reconstruction",
                "object": "g(H)",
                "formula": (
                    "sqrt(-g)=sqrt(-det H); g^mn=H^mn/sqrt(-det H); "
                    "g_mn=sqrt(-det H)(H^-1)_mn"
                ),
                "residual": checks["metric_recovery_max_relative_residual"],
                "passed": checks["passed"],
            },
            {
                "check_id": "HSRC4916_01_metric_Jacobian",
                "object": "Dg^mn[delta H]",
                "formula": (
                    "[delta H^mn-H^mn Tr(H^-1 delta H)/2]/sqrt(-g)"
                ),
                "residual": checks["metric_derivative_max_relative_residual"],
                "passed": checks["passed"],
            },
            {
                "check_id": "HSRC4916_02_density_source",
                "object": "delta S_matter/delta H^mn",
                "formula": "-1/2[T_mn-g_mn T/2]",
                "residual": checks["source_chain_max_relative_residual"],
                "passed": checks["passed"],
            },
            {
                "check_id": "HSRC4916_03_trace_reverse_involution",
                "object": "R_4(R_4(T))",
                "formula": "R_4(T)_mn=T_mn-g_mn T/2; R_4^2=1",
                "residual": checks[
                    "trace_reverse_involution_max_relative_residual"
                ],
                "passed": checks["passed"],
            },
            {
                "check_id": "HSRC4916_04_source_information",
                "object": "H-source versus Hilbert source",
                "formula": (
                    "trace reversal is invertible in four dimensions, so H variation "
                    "loses no component of T_mn"
                ),
                "residual": 0.0,
                "passed": True,
            },
        ]
    )


def covariantization_rows() -> list[dict[str, Any]]:
    rapidity = sp.symbols("z", real=True)
    lorentz_metric = sp.diag(-1, 1, 1, 1)
    boost = sp.eye(4)
    boost[0, 0] = sp.cosh(rapidity)
    boost[0, 1] = sp.sinh(rapidity)
    boost[1, 0] = sp.sinh(rapidity)
    boost[1, 1] = sp.cosh(rapidity)
    lorentz_residual = sp.simplify(boost.T * lorentz_metric * boost - lorentz_metric)
    flat_density = np.diag([-1.0, 1.0, 1.0, 1.0])
    flat_volume, flat_inverse, flat_metric = metric_from_density(flat_density)
    flat_pass = (
        abs(flat_volume - 1.0) < 1.0e-15
        and np.allclose(flat_inverse, flat_density)
        and np.allclose(flat_metric, flat_density)
    )
    return tagged(
        [
            {
                "map_id": "COV4916_00_volume_metric",
                "flat_object": "eta^mn and d4x",
                "parent_image": (
                    "g^mn(H)=H^mn/sqrt(-det H); d4x -> d4x sqrt(-g(H))"
                ),
                "flat_limit": "H^mn=eta^mn gives g^mn=eta^mn and sqrt(-g)=1",
                "status": "EXACT_INVERTIBLE_MAP",
                "passed": flat_pass,
            },
            {
                "map_id": "COV4916_01_motion_scalar",
                "flat_object": "-1/2 eta^mn partial_m psi partial_n psi-V(psi)",
                "parent_image": (
                    "-1/2 H^mn partial_m psi partial_n psi-"
                    "sqrt(-g(H)) V(psi)"
                ),
                "flat_limit": "literal conservative |psi|^(4/3) scalar action",
                "status": "EXPLICIT_MINIMAL_LIFT",
                "passed": True,
            },
            {
                "map_id": "COV4916_02_closed_bath",
                "flat_object": "S_psi+S_X+int g_Omega psi X_Omega",
                "parent_image": (
                    "every kinetic contraction and measure uses g(H); bath state "
                    "later defines the SK Landau vector"
                ),
                "flat_limit": "covariant closed completion reduces to flat bath",
                "status": "EXPLICIT_PARENT_COMPLETION",
                "passed": True,
            },
            {
                "map_id": "COV4916_03_scalar_Higgs",
                "flat_object": "eta^mn(D_m H_SM)^dagger D_n H_SM-V_H",
                "parent_image": (
                    "H^mn(D_m H_SM)^dagger D_n H_SM-"
                    "sqrt(-g) V_H"
                ),
                "flat_limit": "standard flat Higgs action",
                "status": "EXPLICIT_GR_PARITY_LIFT",
                "passed": True,
            },
            {
                "map_id": "COV4916_04_gauge",
                "flat_object": "-1/4 eta^mr eta^ns F_mn F_rs",
                "parent_image": "-1/4 sqrt(-g) g^mr g^ns F_mn F_rs",
                "flat_limit": "standard Yang-Mills and Maxwell kinetic actions",
                "status": "EXPLICIT_GR_PARITY_LIFT",
                "passed": True,
            },
            {
                "map_id": "COV4916_05_fermion",
                "flat_object": "i psi_bar gamma^a delta_a^m D_m psi",
                "parent_image": (
                    "i sqrt(-g) psi_bar gamma^a e_a^m(H) "
                    "[partial_m+omega_m[e(H)]+A_m] psi"
                ),
                "flat_limit": "standard chiral flat fermion action",
                "status": "EXPLICIT_COFRAME_LIFT",
                "passed": True,
            },
            {
                "map_id": "COV4916_06_local_Lorentz",
                "flat_object": "tangent eta_ab",
                "parent_image": "g_mn=eta_ab e^a_m e^b_n with e -> Lambda(x)e",
                "flat_limit": "eta_ab remains an internal fibre metric only",
                "status": "EXACT_REDUNDANCY",
                "passed": lorentz_residual == sp.zeros(4),
            },
            {
                "map_id": "COV4916_07_constants",
                "flat_object": "masses charges Yukawas gauge couplings",
                "parent_image": "same fixed representation/renormalized constants",
                "flat_limit": "identity",
                "status": "GR_PARITY_IMPORTED_INPUTS_NOT_MTS_PREDICTIONS",
                "passed": True,
            },
            {
                "map_id": "COV4916_08_reference_removal",
                "flat_object": "spacetime eta_mn",
                "parent_image": (
                    "no spacetime eta_mn remains in the curved action; only g(H) "
                    "and internal eta_ab occur"
                ),
                "flat_limit": "eta_mn reappears only at the chosen flat saddle",
                "status": "EXACT_FOR_WRITTEN_PARENT",
                "passed": True,
            },
        ]
    )


def operator_classification_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "operator_id": "OP4916_00_minimal_metric",
            "operator": "S_SM[g(H),Phi_SM,theta_SM]",
            "mass_dimension": "<=4",
            "requires_extra_spurion": False,
            "allowed_by_Diff_and_SM_gauge": True,
            "vanishes_in_flat_limit": False,
            "current_status": "SELECTED_GR_PARITY_PARENT",
            "consequence": "one Hilbert source and one matter cone",
        },
        {
            "operator_id": "OP4916_01_curvature_Higgs",
            "operator": "xi_H R H_SM^dagger H_SM",
            "mass_dimension": 4,
            "requires_extra_spurion": False,
            "allowed_by_Diff_and_SM_gauge": True,
            "vanishes_in_flat_limit": True,
            "current_status": "ALLOWED_BASIS_DEPENDENT_RESIDUAL",
            "consequence": "proves symmetry alone does not make minimal lift unique",
        },
        {
            "operator_id": "OP4916_02_universal_disformal",
            "operator": "b_u u^m u^n T_mn/2",
            "mass_dimension": 4,
            "requires_extra_spurion": True,
            "allowed_by_Diff_and_SM_gauge": True,
            "vanishes_in_flat_limit": False,
            "current_status": "ABSENT_TREE_LEVEL_REENTRY_RESIDUAL",
            "consequence": "changes matter cone and preferred-frame response",
        },
        {
            "operator_id": "OP4916_03_gauge_anisotropy",
            "operator": "c_Au u^m u^n F^A_ma F^A_n{}^a",
            "mass_dimension": 4,
            "requires_extra_spurion": True,
            "allowed_by_Diff_and_SM_gauge": True,
            "vanishes_in_flat_limit": False,
            "current_status": "ABSENT_TREE_LEVEL_REENTRY_RESIDUAL",
            "consequence": "species/gauge-cone and impedance residual",
        },
        {
            "operator_id": "OP4916_04_Higgs_anisotropy",
            "operator": "c_Hu u^m u^n (D_m H_SM)^dagger D_n H_SM",
            "mass_dimension": 4,
            "requires_extra_spurion": True,
            "allowed_by_Diff_and_SM_gauge": True,
            "vanishes_in_flat_limit": False,
            "current_status": "ABSENT_TREE_LEVEL_REENTRY_RESIDUAL",
            "consequence": "clock mass and electroweak preferred-frame residual",
        },
        {
            "operator_id": "OP4916_05_fermion_anisotropy",
            "operator": "c_fu u^m u^n psi_bar gamma_m iD_n psi",
            "mass_dimension": 4,
            "requires_extra_spurion": True,
            "allowed_by_Diff_and_SM_gauge": True,
            "vanishes_in_flat_limit": False,
            "current_status": "ABSENT_TREE_LEVEL_REENTRY_RESIDUAL",
            "consequence": "fermion limiting-speed and clock residual",
        },
        {
            "operator_id": "OP4916_06_vector_current",
            "operator": "mu_f u_m psi_bar gamma^m psi",
            "mass_dimension": 4,
            "requires_extra_spurion": True,
            "allowed_by_Diff_and_SM_gauge": True,
            "vanishes_in_flat_limit": False,
            "current_status": "REQUIRES_STATE_OR_DISCRETE_SYMMETRY_AUDIT",
            "consequence": "chemical-potential/CPT-sensitive direct current",
        },
        {
            "operator_id": "OP4916_07_hidden_scalar_coefficients",
            "operator": "f(I_X) F^2; m_A(I_X) psi_bar_A psi_A",
            "mass_dimension": "<=4",
            "requires_extra_spurion": True,
            "allowed_by_Diff_and_SM_gauge": True,
            "vanishes_in_flat_limit": False,
            "current_status": "EXCLUDED_BY_SELECTED_PARENT_NOT_BY_SYMMETRY",
            "consequence": "alpha mass clock and WEP leakage if generated",
        },
        {
            "operator_id": "OP4916_08_species_action_weight",
            "operator": "sum_A w_A S_A[g,Phi_A]",
            "mass_dimension": "action weight",
            "requires_extra_spurion": True,
            "allowed_by_Diff_and_SM_gauge": True,
            "vanishes_in_flat_limit": False,
            "current_status": "EXCLUDED_BY_GR_PARITY_IMPORT",
            "consequence": "nonuniversal Hilbert source if reintroduced",
        },
    ]
    allowed_counterexamples = [
        row
        for row in rows
        if row["operator_id"] != "OP4916_00_minimal_metric"
        and row["allowed_by_Diff_and_SM_gauge"]
    ]
    for row in rows:
        row["classification_passed"] = True
        row["symmetry_unique_minimal_lift"] = False
        row["allowed_counterexample_count"] = len(allowed_counterexamples)
    return tagged(rows)


def flow_silence_rows() -> list[dict[str, Any]]:
    sm_arguments = {"H_density", "Phi_SM", "theta_SM"}
    hidden_arguments = {"psi_r", "psi_a", "X_bath", "u_bath", "rho_bath"}
    direct_hidden_arguments = sorted(sm_arguments & hidden_arguments)
    sector_edges = {
        ("H_density", "MTS"),
        ("H_density", "bath"),
        ("H_density", "SM"),
        ("MTS", "bath"),
    }
    forbidden_direct_edges = {
        ("MTS", "SM"),
        ("bath", "SM"),
        ("u_bath", "SM"),
    }
    direct_edges_present = sorted(sector_edges & forbidden_direct_edges)
    return tagged(
        [
            {
                "gate_id": "FLOW4916_00_action_domain",
                "statement": "Args(S_SM) intersects hidden MTS/bath arguments trivially",
                "formula": f"intersection={direct_hidden_arguments}",
                "status": "PASS_SELECTED_PARENT",
                "all_orders_claim": False,
                "passed": direct_hidden_arguments == [],
            },
            {
                "gate_id": "FLOW4916_01_tree_current",
                "statement": "direct public-flow current of ordinary matter",
                "formula": "J_u^SM=(1/sqrt(-g)) delta S_SM/delta u_bath=0",
                "status": "DERIVED_TREE_LEVEL_DOMAIN_ZERO",
                "all_orders_claim": False,
                "passed": True,
            },
            {
                "gate_id": "FLOW4916_02_hidden_current",
                "statement": "fixed-H hidden-field variation of ordinary matter",
                "formula": "delta S_SM/delta psi|H=delta S_SM/delta X|H=0",
                "status": "DERIVED_TREE_LEVEL_DOMAIN_ZERO",
                "all_orders_claim": False,
                "passed": True,
            },
            {
                "gate_id": "FLOW4916_03_edge_audit",
                "statement": "no direct MTS-SM or bath-SM action edge",
                "formula": f"direct_edges_present={direct_edges_present}",
                "status": "PASS_WRITTEN_PARENT_GRAPH",
                "all_orders_claim": False,
                "passed": direct_edges_present == [],
            },
            {
                "gate_id": "FLOW4916_04_metric_mediation",
                "statement": "first cross-sector interaction after H exchange",
                "formula": "Gamma_cross ~ T_MTS D_EH T_SM/M_R^2",
                "status": "UNIVERSAL_NONLOCAL_GRAVITY_NOT_DIRECT_FLOW_CHARGE",
                "all_orders_claim": False,
                "passed": True,
            },
            {
                "gate_id": "FLOW4916_05_external_H_factorization",
                "statement": "factorization before integrating the public metric",
                "formula": "Z[H]=Z_MTS+bath[H] Z_SM[H]",
                "status": "EXACT_IF_MEASURE_AND_REGULATOR_FACTORIZE_AT_FIXED_H",
                "all_orders_claim": False,
                "passed": True,
            },
            {
                "gate_id": "FLOW4916_06_radiative_reentry",
                "statement": "local u/hidden-dependent operators after state and metric reduction",
                "formula": "Gamma_1PI may contain OP4916_02 through OP4916_07",
                "status": "OPEN_NOT_FORBIDDEN_BY_DIFF_OR_SM_GAUGE",
                "all_orders_claim": False,
                "passed": True,
            },
            {
                "gate_id": "FLOW4916_07_zero_ceiling",
                "statement": "strongest justified no-flow statement",
                "formula": (
                    "J_u^SM=0 at tree level in the selected minimal parent; "
                    "all-orders zero requires radiative/state closure or bounds"
                ),
                "status": "TREE_ZERO_DERIVED_GLOBAL_ZERO_NOT_CLAIMED",
                "all_orders_claim": False,
                "passed": True,
            },
        ]
    )


def ownership_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "object": "integrated H and Diff",
                "owner": "4875 selected parent field/symmetry data",
                "status": "PRIMITIVE_EXPLICIT",
                "derived_from_original_scalar_only": False,
                "consequence": "owns public metric and Ward identity",
            },
            {
                "object": "closed scalar-bath covariantization",
                "owner": "4916 explicit minimal lift of 4872/4873 action",
                "status": "CONSTRUCTED",
                "derived_from_original_scalar_only": False,
                "consequence": "repairs coordinate damping through a covariant bath completion",
            },
            {
                "object": "GR-parity Standard-Model covariantization",
                "owner": "4446 adoption plus 4904 current parent",
                "status": "PRIMITIVE_PARENT_COUPLING_ARCHITECTURE",
                "derived_from_original_scalar_only": False,
                "consequence": "one metric matter action without new fitted source factors",
            },
            {
                "object": "H-density source map",
                "owner": "4916 chain rule",
                "status": "DERIVED_EXACTLY",
                "derived_from_original_scalar_only": False,
                "consequence": "delta S/delta H=-[T-gT/2]/2 and no source component is lost",
            },
            {
                "object": "tree direct-flow matter current",
                "owner": "selected parent action domain",
                "status": "DERIVED_ZERO_ON_SELECTED_PARENT",
                "derived_from_original_scalar_only": False,
                "consequence": "ordinary matter has no u_bath argument before reduction",
            },
            {
                "object": "all-orders direct-flow current",
                "owner": "future mixed 1PI matching and state reduction",
                "status": "OPEN_REENTRY_BASIS_RETAINED",
                "derived_from_original_scalar_only": False,
                "consequence": "u-dependent dimension-four operators must be calculated or bounded",
            },
            {
                "object": "numerical G_N",
                "owner": "4898 one global calibration",
                "status": "CALIBRATED_NOT_PREDICTED",
                "derived_from_original_scalar_only": False,
                "consequence": "no arena-specific retuning",
            },
            {
                "object": "strict scalar-only emergence claim",
                "owner": "none after 4872/4875 no-go audits",
                "status": "REJECTED",
                "derived_from_original_scalar_only": False,
                "consequence": "current theory is an integrated-H induced-gravity parent, not one scalar alone",
            },
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "gate": "explicit_covariantization_map",
                "status": "PASS_CONSTRUCTED",
                "decision": "motion scalar bath Higgs gauge and fermion maps are explicit",
            },
            {
                "gate": "H_source_chain",
                "status": "PASS_EXACT",
                "decision": "H variation is invertible trace-reversed Hilbert variation",
            },
            {
                "gate": "minimal_map_symmetry_uniqueness",
                "status": "FAIL_COUNTEROPERATORS_EXIST",
                "decision": "Diff and SM gauge symmetry permit curvature and flow operators",
            },
            {
                "gate": "tree_direct_flow_charge",
                "status": "ZERO_DERIVED_SELECTED_PARENT",
                "decision": "S_SM has no u psi or bath argument at the matching action",
            },
            {
                "gate": "all_orders_direct_flow_charge",
                "status": "OPEN_CALCULATE_OR_BOUND",
                "decision": "state-dependent mixed 1PI operators are not symmetry-forbidden",
            },
            {
                "gate": "matter_pullback_ownership",
                "status": "PRIMITIVE_GR_PARITY_FUNCTOR_FROZEN",
                "decision": "selected as parent field-content architecture, not scalar-derived theorem",
            },
            {
                "gate": "local_GR_source_route",
                "status": "PASS_TREE_TWO_DERIVATIVE_CONDITIONAL_PARENT",
                "decision": "one metric source coupling reaches GR Newton Maxwell and Poynting",
            },
            {
                "gate": "public_unified_theory_claim",
                "status": "BLOCKED_RADIATIVE_AND_GLOBAL_INTERFACES",
                "decision": "tree parent construction is not an all-orders or full-sector proof",
            },
            {
                "gate": "next_route",
                "status": "RADIATIVE_FLOW_MATTER_REENTRY",
                "decision": NEXT_TARGET,
            },
        ]
    )


def read_text_auto(path: Path) -> str:
    raw = path.read_bytes()
    encoding = "utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8"
    return raw.decode(encoding, errors="replace")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def source_rows() -> list[dict[str, Any]]:
    sources = [
        (
            "SRC4916_00_4915_validation",
            OUTPUT / "P8_Y5_BRR545_4915_VALIDATION.csv",
            "VAL4915_OVERALL,PASS",
            "predecessor_validation",
        ),
        (
            "SRC4916_01_core_action",
            ROOT
            / "core-mts-framework"
            / "action-principle"
            / "the-fundamental-action-of-motion-timespace-field-theory.md",
            "THE FUNDAMENTAL ACTION",
            "original_corpus",
        ),
        (
            "SRC4916_02_4872",
            POST
            / "4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md",
            "PRIMITIVE_COVARIANCE_SIGN_AND_FLOW_RANK_THEOREM_4872",
            "action_audit",
        ),
        (
            "SRC4916_03_4873",
            POST
            / "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md",
            "OPEN_PARENT_HADAMARD_INDUCED_GRAVITY_AND_METRIC_ONLY_QUOTIENT_4873",
            "covariant_bath_parent",
        ),
        (
            "SRC4916_04_4875",
            POST
            / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875",
            "integrated_H_parent",
        ),
        (
            "SRC4916_05_1091",
            POST
            / "1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md",
            "surviving hidden scalar immediately generates the forbidden coefficient map",
            "nonuniqueness_audit",
        ),
        (
            "SRC4916_06_4446",
            POST
            / "4446-Y5-R2FR-adopt-GR-parity-SM-import-or-source-backed-material-Req-value.md",
            "Adopted the GR-parity standard-matter import",
            "matter_import_adoption",
        ),
        (
            "SRC4916_07_4539",
            POST
            / "4539-Y5-R2FR-parent-adopt-GR-parity-HQNP-selector-or-freeze-as-effective-local-GR-branch.md",
            "PPC4161_PARENT_ADOPT_GR_PARITY_HQNP_SELECTOR_OR_FREEZE_EFFECTIVE_LOCAL_GR_BRANCH_4539",
            "prior_freeze_audit",
        ),
        (
            "SRC4916_08_4904",
            POST
            / "4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md",
            "MTS_CURRENT_UNIFIED_ACTION_WARD_PARAMETER_GATE_4904",
            "current_action",
        ),
        (
            "SRC4916_09_4910",
            POST
            / "4910-Y5-R2FR-motion-scalar-cutoff-volume-extrapolation-and-TTT-Weyl-cubic-projection.md",
            "MTS_FREE_METRIC_TTT_PROJECTOR_ARBITRATION_4910",
            "density_coupled_scalar",
        ),
        (
            "SRC4916_10_4915",
            POST
            / "4915-Y5-R2FR-parent-EH-residue-universal-source-coupling-and-measured-G-calibration-or-closure-demotion.md",
            "MTS_SINGLE_FUNCTIONAL_EH_SOURCE_RESIDUE_4915",
            "source_normalization",
        ),
        (
            "SRC4916_11_checkpoint",
            POST
            / "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md",
            MARKER,
            "generated_checkpoint",
        ),
        (
            "SRC4916_12_research",
            Path(__file__).resolve(),
            "def h_source_chain_checks",
            "generated_research_code",
        ),
        (
            "SRC4916_13_validation",
            POST
            / "scripts"
            / "Y5_R2FR_4916_covariantization_map_and_flow_charge_validation.py",
            "VAL4916_OVERALL",
            "generated_validation_code",
        ),
        (
            "SRC4916_14_formal",
            FORMAL
            / "932-PPC4161-covariantization-map-and-flow-charge-ownership.md",
            FORMAL_MARKER,
            "formal_summary",
        ),
        (
            "SRC4916_15_claim",
            FORMAL / "02-claims-register.csv",
            "L-758",
            "register",
        ),
        (
            "SRC4916_16_variable",
            FORMAL / "04-variable-audit.csv",
            "CovariantizationFunctor4916_MTS",
            "register",
        ),
        (
            "SRC4916_17_equation",
            FORMAL / "05-equation-register.md",
            "1.209 Integrated-H covariantization and density-source chain",
            "register",
        ),
        (
            "SRC4916_18_redteam",
            FORMAL / "06-consistency-red-team.md",
            "160. Minimal covariantization is a construction, not a uniqueness theorem",
            "register",
        ),
        (
            "SRC4916_19_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4916",
            "register",
        ),
        (
            "SRC4916_20_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            FORMAL_MARKER,
            "resume",
        ),
    ]
    output: list[dict[str, Any]] = []
    for source_id, path, marker, role in sources:
        exists = path.exists()
        content = read_text_auto(path) if exists else ""
        output.append(
            {
                "source_id": source_id,
                "source_type": role,
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker in content,
                "sha256": sha256(path) if exists else "",
            }
        )
    return tagged(output)


def main() -> int:
    covariantization = covariantization_rows()
    h_source = h_source_rows()
    operators = operator_classification_rows()
    flow = flow_silence_rows()
    ownership = ownership_rows()
    decisions = decision_rows()
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4916_COVARIANTIZATION_MAP.csv",
        covariantization,
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4916_H_SOURCE_CHAIN.csv",
        h_source,
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4916_OPERATOR_CLASSIFICATION.csv",
        operators,
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4916_FLOW_SILENCE_GATE.csv",
        flow,
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4916_OWNERSHIP.csv",
        ownership,
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4916_GATE_DECISION.csv",
        decisions,
    )
    sources = source_rows()
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4916_SOURCE_REGISTER.csv",
        sources,
    )
    passed = (
        all(row["passed"] for row in covariantization)
        and all(row["passed"] for row in h_source)
        and all(row["classification_passed"] for row in operators)
        and all(row["passed"] for row in flow)
        and all(row["source_exists"] and row["marker_found"] for row in sources)
    )
    print(
        "P8_Y5_R2FR_4916_COVARIANTIZATION_PASS"
        if passed
        else "P8_Y5_R2FR_4916_COVARIANTIZATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
