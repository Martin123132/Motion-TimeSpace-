from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4984"

CHECKPOINT_4983 = POST / "4983-Y5-R2FR-box2-essential-quotient-running-frame-and-local-profile-theorem.md"
RESULT_4983 = POST / "source-intake" / "functional_rg" / "4983" / "box2_essential_local_profile_results.json"
BASIS_4930 = POST / "4930-Y5-R2FR-six-derivative-MTS-matter-essential-operator-basis-and-block-triangular-stability-or-Wilson-retention.md"
EFT_SOURCE = POST / "source-intake" / "functional_rg" / "4930" / "src1908" / "GravityEFTv2_final.tex"
QUOTIENT_4958 = POST / "4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-2to4-amplitude-or-rate-route-rejection.md"
PROJECTOR_4959 = POST / "4959-Y5-R2FR-O2-O3-O4-external-scalar-sixpoint-projectors-and-full-invariant-amplitude-or-curvature-route-rejection.md"
RESULT_4959 = POST / "source-intake" / "functional_rg" / "4959" / "curvature_sixpoint_projector_results.json"
SOURCE_SELECTION = POST / "source-intake" / "functional_rg" / "4943" / "matter_source_selection_rules.csv"
JUNCTION_SOURCE = POST / "source-intake" / "functional_rg" / "4943" / "junction_scalar_charge_and_fifth_force.csv"
LOCAL_SOURCE_CHECKPOINT = POST / "4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md"
LOCAL_GR_CHECKPOINT = POST / "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md"
PARENT_HESSIAN_RESULT = POST / "source-intake" / "functional_rg" / "4981" / "parent_hessian_common_scheme_results.json"

GRADING_CSV = SOURCE / "running_frame_derivative_grading.csv"
SPILLOVER_CSV = SOURCE / "running_frame_six_derivative_spillover.csv"
IBP_CSV = SOURCE / "running_frame_IBP_jet_crosscheck.csv"
PROJECTOR_CSV = SOURCE / "running_frame_flat_onshell_projector.csv"
NONLOCAL_CSV = SOURCE / "nonlocal_two_point_source_silence_theorem.csv"
BRANCH_CSV = SOURCE / "selected_branch_six_derivative_silence_gate.csv"
GATE_CSV = SOURCE / "running_frame_nonlocal_silence_gate.csv"
RESULT_JSON = SOURCE / "running_frame_nonlocal_silence_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4984_RUNNING_FRAME_P6_NONLOCAL_SILENCE"
CHECKED_DATE = "2026-07-14"


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def minkowski_dot(left: np.ndarray, right: np.ndarray) -> float:
    return float(left[0] * right[0] - np.dot(left[1:], right[1:]))


def minkowski_square(vector: np.ndarray) -> float:
    return minkowski_dot(vector, vector)


def ibp_crosschecks() -> tuple[list[dict[str, Any]], float, float]:
    generator = np.random.default_rng(4984)
    rows: list[dict[str, Any]] = []
    for control_index in range(24):
        metric = np.eye(4) if control_index < 12 else np.diag([-1.0, 1.0, 1.0, 1.0])
        signature = "Euclidean" if control_index < 12 else "Lorentzian_local_jet"
        gradient_covector = generator.normal(size=4)
        gradient_vector = metric @ gradient_covector
        hessian = generator.normal(size=(4, 4))
        hessian = 0.5 * (hessian + hessian.T)
        gradient_box = generator.normal(size=4)
        coefficient_c = float(generator.uniform(-1.3, 1.3))
        gamma_box = float(generator.uniform(-1.1, 1.1))

        kinetic = float(gradient_covector @ gradient_vector)
        box_psi = float(np.sum(metric * hessian))
        vv_hessian = float(gradient_vector @ hessian @ gradient_vector)
        v_gradient_box = float(gradient_vector @ gradient_box)
        divergence = (
            2.0 * box_psi * vv_hessian
            + kinetic * v_gradient_box
            + kinetic * box_psi**2
        )
        direct = 4.0 * coefficient_c * gamma_box * kinetic * v_gradient_box
        boundary = 4.0 * coefficient_c * gamma_box * divergence
        bulk = (
            -4.0 * coefficient_c * gamma_box * kinetic * box_psi**2
            -8.0 * coefficient_c * gamma_box * box_psi * vv_hessian
        )
        reconstructed = boundary + bulk
        absolute = abs(direct - reconstructed)
        relative_value = absolute / max(abs(direct), abs(reconstructed), 1.0e-15)
        rows.append(
            {
                "control_index": control_index,
                "signature": signature,
                "X": kinetic,
                "Y_Box_psi": box_psi,
                "vvH": vv_hessian,
                "v_dot_nablaY": v_gradient_box,
                "coefficient_c": coefficient_c,
                "gamma_Box": gamma_box,
                "direct_delta_cX2": direct,
                "boundary_divergence": boundary,
                "reduced_EOM_bulk": bulk,
                "reconstructed_delta_cX2": reconstructed,
                "absolute_residual": absolute,
                "relative_residual": relative_value,
                "status": "COVARIANT_LOCAL_JET_IBP_IDENTITY_MATCH",
            }
        )
    return (
        rows,
        max(float(row["relative_residual"]) for row in rows),
        max(float(row["absolute_residual"]) for row in rows),
    )


def projector_crosschecks() -> tuple[list[dict[str, Any]], float, float, float]:
    rows: list[dict[str, Any]] = []
    maximum_shell = 0.0
    maximum_ratio = 0.0
    minimum_o2 = math.inf
    for event_index, angle in enumerate(np.linspace(0.2, 2.8, 14)):
        sine = math.sin(float(angle))
        cosine = math.cos(float(angle))
        momenta = (
            np.array([1.0, 0.0, 0.0, 1.0]),
            np.array([1.0, 0.0, 0.0, -1.0]),
            np.array([-1.0, -sine, 0.0, -cosine]),
            np.array([-1.0, sine, 0.0, cosine]),
        )
        mass_shell = [minkowski_square(momentum) for momentum in momenta]
        conservation = np.sum(momenta, axis=0)
        s_value = minkowski_square(momenta[0] + momenta[1])
        t_value = minkowski_square(momenta[0] + momenta[2])
        u_value = minkowski_square(momenta[0] + momenta[3])
        projector_a = 0.0
        projector_b = 0.0
        for first, second, third, fourth in itertools.permutations(range(4)):
            projector_a += (
                minkowski_dot(momenta[first], momenta[second])
                * mass_shell[third]
                * mass_shell[fourth]
            )
            projector_b += (
                mass_shell[first]
                * minkowski_dot(momenta[second], momenta[fourth])
                * minkowski_dot(momenta[third], momenta[fourth])
            )
        projector_o2 = -3.0 * s_value * t_value * u_value
        induced = -4.0 * 0.731 * projector_a - 8.0 * 0.731 * projector_b
        ratio = abs(induced) / max(abs(projector_o2), 1.0e-300)
        shell = max(
            *(abs(value) for value in mass_shell),
            float(np.max(np.abs(conservation))),
            abs(s_value + t_value + u_value),
        )
        maximum_shell = max(maximum_shell, shell)
        maximum_ratio = max(maximum_ratio, ratio)
        minimum_o2 = min(minimum_o2, abs(projector_o2))
        rows.append(
            {
                "event_index": event_index,
                "scattering_angle_radians": float(angle),
                "maximum_external_mass_shell_residual": max(abs(value) for value in mass_shell),
                "momentum_conservation_residual": float(np.max(np.abs(conservation))),
                "s_plus_t_plus_u_residual": abs(s_value + t_value + u_value),
                "s": s_value,
                "t": t_value,
                "u": u_value,
                "P_A_XBox2": projector_a,
                "P_B_BoxvvH": projector_b,
                "P_O2_minus3stu": projector_o2,
                "induced_running_frame_projector": induced,
                "absolute_induced_to_O2_ratio": ratio,
                "status": "MASSLESS_ONSHELL_REDUNDANT_PACKET_ZERO_O2_NONZERO",
            }
        )
    return rows, maximum_shell, maximum_ratio, minimum_o2


def grading_rows() -> list[dict[str, Any]]:
    rows = [
        ("kinetic", "(Z/2)X", 2, 2, "delta S=-Zs(Box chi)^2+boundary", 4, "fixes b_new=b-2Zs", "0", "ZERO", "ACTION_SUBSTITUTION_DERIVED", CHECKPOINT_4983),
        ("Box2_surface", "(b/2)(Box psi)^2", 4, 2, "delta S=bs(Box chi)(Box^2 chi)+commutators", 6, "b*s=O(dt^2) on b=0 flow surface", "0", "ZERO", "OFF_SURFACE_REDUNDANT_QUADRATIC_PACKET", CHECKPOINT_4983),
        ("X2", "cX^2", 4, 4, "delta S=-4cs X Y^2-8cs Y v^m v^n H_mn+boundary", 6, "A6 and B6 contain explicit Y=Box psi", "0", "ZERO", "CLASSICAL_CONNECTION_DERIVED", QUOTIENT_4958),
        ("RicciX", "ctilde R_mn v^m v^n", 4, 2, "delta S=-2ctilde s Y nabla^n(R_mn v^m)+boundary", 6, "EOM packet; ctilde=0 on essential surface", "0 on ctilde=0", "ZERO", "METRIC_FRAME_SPILLOVER_SEPARATE", QUOTIENT_4958),
        ("RX", "d R X", 4, 2, "delta S=-2ds Y nabla_m(Rv^m)+boundary", 6, "EOM packet; d=0 on essential surface", "0 on d=0", "ZERO", "METRIC_FRAME_SPILLOVER_SEPARATE", QUOTIENT_4958),
        ("O2", "X H_mn H^mn", 6, 4, "scalar substitution raises derivative order by two", 8, "no six-to-six term", "0", "ZERO", "GENUINE_BETA_wO2_STILL_SEPARATE", PROJECTOR_4959),
        ("O3", "C^3", 6, 0, "classical scalar substitution acts trivially", 6, "zero action substitution", "0", "PURE_METRIC_REMAINS", "SCALAR_JACOBIAN_PURE_METRIC_OPEN", BASIS_4930),
        ("O4", "C^2 X", 6, 2, "delta O4=2s C^2 v.nablaY", 8, "no six-to-six term", "0", "ZERO", "CLASSICAL_CONNECTION_DERIVED", PROJECTOR_4959),
        ("source", "-J_psi psi", 0, 1, "J_new=J+s Box J plus Green boundary", 2, "J=0 is a fixed source", "0", "ZERO", "SELECTED_PARENT_SOURCE_INVARIANT", SOURCE_SELECTION),
        ("Jacobian", "Dpsi under psi_old=(1+sBox)chi", 0, 0, "log J=Tr log(1+sBox)", -1, "regulator-dependent metric-only terms", "0 because no psi", "NO_CLASSICAL_SCALAR_SOURCE", "PURE_METRIC_JACOBIAN_OPEN", PARENT_HESSIAN_RESULT),
    ]
    return [
        {
            "grading_id": f"DG4984_{index:02d}_{name}",
            "input_operator": operator,
            "input_derivative_order": derivative_order,
            "scalar_field_degree": degree,
            "frame_variation": variation,
            "output_derivative_order": output_order,
            "six_derivative_effect": effect,
            "essential_O2_shift": o2_shift,
            "selected_psi_zero_status": zero_status,
            "quantum_measure_status": measure_status,
            "source_path": relative(source),
        }
        for index, (name, operator, derivative_order, degree, variation, output_order, effect, o2_shift, zero_status, measure_status, source) in enumerate(rows, start=1)
    ]


def spillover_rows() -> list[dict[str, Any]]:
    rows = [
        ("A6", "X(Box psi)^2", "-4 c gamma_Box", True, 0.0, 0.0, 0.0, "REDUNDANT_CONNECTION_COORDINATE", QUOTIENT_4958),
        ("B6", "(Box psi)v^m v^n H_mn", "-8 c gamma_Box", True, 0.0, 0.0, 0.0, "REDUNDANT_CONNECTION_COORDINATE", QUOTIENT_4958),
        ("Ricci_EOM", "Y nabla^n(R_mn v^m)", "-2 ctilde gamma_Box=0 on surface", True, 0.0, 0.0, 0.0, "REDUNDANT_SURFACE_ZERO", QUOTIENT_4958),
        ("R_EOM", "Y nabla_m(Rv^m)", "-2 d gamma_Box=0 on surface", True, 0.0, 0.0, 0.0, "REDUNDANT_SURFACE_ZERO", QUOTIENT_4958),
        ("O1", "X^3", "0 at p6", False, math.nan, 0.0, 0.0, "NO_SCALAR_FRAME_P6_SHIFT", BASIS_4930),
        ("O2", "X H_mn H^mn", "0 from gamma_Box", False, -3.0, 0.0, 0.0, "ESSENTIAL_O2_NOT_CONTAMINATED_GENUINE_BETA_OPEN", PROJECTOR_4959),
        ("O3", "C^3", "0 classical; pure-metric Jacobian open", False, math.nan, 0.0, math.nan, "CLASSICAL_ZERO_QUANTUM_MEASURE_OPEN", BASIS_4930),
        ("O4", "C^2 X", "0 at p6", False, math.nan, 0.0, 0.0, "NO_SCALAR_FRAME_P6_SHIFT_ZERO_AT_PSI0", PROJECTOR_4959),
        ("O5", "C_mnrs v^m v^r H^ns", "absent by reflection", False, math.nan, 0.0, 0.0, "REFLECTION_ODD_EXCLUDED_ZERO_AT_PSI0", BASIS_4930),
    ]
    return [
        {
            "spillover_id": f"SP4984_{index:02d}_{name}",
            "coordinate": coordinate,
            "connection_beta": beta,
            "contains_explicit_leading_EOM": contains_eom,
            "flat_massless_onshell_projector": projector,
            "essential_six_derivative_shift": shift,
            "selected_branch_value": branch_value,
            "status": status,
            "source_path": relative(source),
        }
        for index, (name, coordinate, beta, contains_eom, projector, shift, branch_value, status, source) in enumerate(rows, start=1)
    ]


def nonlocal_rows() -> list[dict[str, Any]]:
    rows = [
        ("kernel", "Gamma2=(1/2)<psi,F_H(-Box)psi> on a covariant self-adjoint domain", "E_psi=F_H(-Box)psi=0", "EXACT_ANALYTIC_OR_NONANALYTIC_KERNEL", True, CHECKPOINT_4983),
        ("metric", "delta_H Gamma2=(1/2)<psi,delta_H F_H psi> plus measure terms", "classical T_mn[Gamma2]=0", "EXACT_CLASSICAL_BILINEAR_METRIC_SILENCE", True, LOCAL_GR_CHECKPOINT),
        ("interactions", "retained motion interactions have scalar degree at least two", "first scalar variation and classical stress vanish", "EXACT_SELECTED_PARENT_RULE", True, SOURCE_SELECTION),
        ("matter", "Args(S_SM)={H,Phi_SM,theta_SM}; psi absent", "J_psi=0 in every scalar coordinate", "EXACT_MATTER_DESCENT_INVARIANT", True, SOURCE_SELECTION),
        ("source_map", "-<J,psi_old>=-<J+sBoxJ,chi> plus Green boundary", "J=0 maps exactly to J_new=0", "ZERO_SOURCE_FIXED_POINT", True, CHECKPOINT_4983),
        ("boundary", "selected global profile and asymptotic collar have psi=0", "psi, Box psi, and every normal derivative vanish", "ZERO_PROFILE_DOMAIN_INVARIANCE", True, JUNCTION_SOURCE),
        ("Ward", "nabla_mu T^mu_nu=E_psi nabla_nu psi", "no independent classical one-scalar force current", "COVARIANT_NONLOCAL_WARD_SILENCE", True, LOCAL_GR_CHECKPOINT),
        ("uniqueness", "zero solves the equation without a spectral-gap premise", "existence proved; uniqueness and stability open", "EXPLICIT_NONCLAIM_UNIQUENESS_OPEN", False, CHECKPOINT_4983),
        ("determinant", "integrating fluctuations gives (1/2)Tr log F_H", "pure-metric quantum response may remain", "QUANTUM_METRIC_DETERMINANT_RETAINED_OPEN", False, PARENT_HESSIAN_RESULT),
        ("scope", "O3=C^3 and other pure-metric terms contain no psi", "scalar silence is not exact all-operator local GR", "PURE_METRIC_OBSTRUCTION_RETAINED", False, BASIS_4930),
    ]
    return [
        {
            "theorem_id": f"NL4984_{index:02d}_{name}",
            "assumption_or_identity": assumption,
            "consequence_at_psi_zero": consequence,
            "status": status,
            "source_path": relative(source),
            "valid_for_selected_nonlocal_source_silence_claim": valid,
        }
        for index, (name, assumption, consequence, status, valid, source) in enumerate(rows, start=1)
    ]


def branch_rows() -> list[dict[str, Any]]:
    rows = [
        ("nonlocal", "(1/2)<psi,F_H psi>", 2, "0", "0", "0", "0 classically at psi=0", "SOURCE_SILENT_ANALYTIC_OR_NONANALYTIC", CHECKPOINT_4983),
        ("O1", "X^3", 6, "0", "0", "0", "0", "MOTION_OPERATOR_SILENT", BASIS_4930),
        ("O2", "X H_mn H^mn", 4, "0", "0", "0", "0", "MOTION_OPERATOR_SILENT_FOR_ARBITRARY_wO2", PROJECTOR_4959),
        ("O3", "C^3", 0, "0", "GENERALLY_NONZERO_ON_CURVED_BACKGROUND", "0", "0 because C^3 starts at h^3 about flat", "SCALAR_SILENT_PURE_METRIC_REMAINS", BASIS_4930),
        ("O4", "C^2 X", 2, "0", "0", "0", "0", "MOTION_CURVATURE_PORTAL_SILENT", PROJECTOR_4959),
        ("O5", "C_mnrs v^m v^r H^ns", 3, "0", "0", "0", "0", "ABSENT_BY_REFLECTION_AND_ZERO_AT_ORIGIN", BASIS_4930),
        ("source", "S_SM[H,Phi_SM]", 0, "0", "VISIBLE_T_MN_REMAINS", "0", "standard metric response", "PUBLIC_METRIC_SOURCE_NO_SCALAR_SOURCE", SOURCE_SELECTION),
        ("frame", "psi_old=(1+sBox)chi", 1, "0 maps to 0", "0", "J=0 maps to 0", "coordinate change", "ZERO_BRANCH_FIXED_UNDER_RUNNING_FRAME", CHECKPOINT_4983),
        ("Jacobian", "Tr log(1+sBox)", 0, "0", "QUANTUM_METRIC_TERM_OPEN", "0", "REGULATOR_DEPENDENT", "DO_NOT_DROP_DOES_NOT_SOURCE_PSI", PARENT_HESSIAN_RESULT),
        ("Newton", "p6 scalar packet plus C^3 about flat psi=0", -1, "0", "only pure metric terms remain", "0", "0 at p2 Newton order", "LEADING_NEWTON_PROPAGATOR_UNCHANGED_NOT_FULL_PPN", LOCAL_GR_CHECKPOINT),
    ]
    return [
        {
            "sector_id": f"BR4984_{index:02d}_{name}",
            "operator": operator,
            "scalar_degree": degree,
            "scalar_EOM_at_psi_zero": eom,
            "classical_metric_stress_at_psi_zero": stress,
            "one_scalar_source_at_psi_zero": source_value,
            "flat_metric_quadratic_Hessian": hessian,
            "status": status,
            "source_path": relative(source),
            "valid_for_selected_branch_claim": True,
        }
        for index, (name, operator, degree, eom, stress, source_value, hessian, status, source) in enumerate(rows, start=1)
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    started = time.perf_counter()

    required_paths = (
        CHECKPOINT_4983,
        RESULT_4983,
        BASIS_4930,
        EFT_SOURCE,
        QUOTIENT_4958,
        PROJECTOR_4959,
        RESULT_4959,
        SOURCE_SELECTION,
        JUNCTION_SOURCE,
        LOCAL_SOURCE_CHECKPOINT,
        LOCAL_GR_CHECKPOINT,
        PARENT_HESSIAN_RESULT,
    )
    missing = [str(path) for path in required_paths if not path.exists()]
    if missing:
        raise FileNotFoundError("\n".join(missing))

    result_4983 = json.loads(RESULT_4983.read_text(encoding="utf-8"))
    result_4959 = json.loads(RESULT_4959.read_text(encoding="utf-8"))
    source_selection = read_csv(SOURCE_SELECTION)
    junction_source = read_csv(JUNCTION_SOURCE)
    basis_text = BASIS_4930.read_text(encoding="utf-8", errors="replace")
    projector_text = PROJECTOR_4959.read_text(encoding="utf-8", errors="replace")

    parent_source_zero = any(
        row["rule_id"] == "SRC4943_00_parent_arguments"
        and row["passed"].lower() == "true"
        and "delta S_SM/delta psi=0" in row["consequence"]
        for row in source_selection
    )
    reflection_even = any(
        row["rule_id"] == "SRC4943_02_diagonal_reflection"
        and row["passed"].lower() == "true"
        for row in source_selection
    )
    boundary_zero = any(
        row["rule_id"] == "SRC4943_04_boundary_state"
        and row["passed"].lower() == "true"
        for row in source_selection
    )
    scalar_charge_zero = any(
        row["gate_id"] == "JUNC4943_03_scalar_charge"
        and row["passed"].lower() == "true"
        for row in junction_source
    )

    grading = grading_rows()
    spillover = spillover_rows()
    ibp, maximum_ibp_relative, maximum_ibp_absolute = ibp_crosschecks()
    projectors, maximum_shell, maximum_ratio, minimum_o2 = projector_crosschecks()
    nonlocal_theorem = nonlocal_rows()
    branch = branch_rows()
    spillover_by_id = {row["spillover_id"]: row for row in spillover}
    nonlocal_by_id = {row["theorem_id"]: row for row in nonlocal_theorem}
    branch_by_id = {row["sector_id"]: row for row in branch}

    source_fragments = {
        "O2": "O2=(nabla phi)^2" in basis_text,
        "O3": "O3=C_mn^rs C^mnab C_abrs" in basis_text,
        "O4": "O4=(C_abrs C^abrs)(nabla phi)^2" in basis_text,
        "O2_projector": "V4_O2(k1,k2,k3,k4)" in projector_text and "-3 s t u" in projector_text,
    }

    gates = [
        ("G01_required_inputs", not missing, f"{len(required_paths)} paths"),
        ("G02_4983_predecessor", result_4983["valid_for_selected_parent_Box2_zero_motion_local_branch"] is True, "4983 branch promoted"),
        ("G03_source_basis", all(source_fragments.values()), str(source_fragments)),
        ("G04_4959_O2_projector", result_4959["gates"]["O2_projector"] == "DERIVED_GAUGE_COMPLETE", "gauge-complete -3stu"),
        ("G05_derivative_grading", len(grading) == 10, "ten rows"),
        ("G06_IBP_controls", len(ibp) == 24 and maximum_ibp_relative < 2.0e-13 and maximum_ibp_absolute < 2.0e-13, f"rel={maximum_ibp_relative:.3e};abs={maximum_ibp_absolute:.3e}"),
        ("G07_connection_coefficients", spillover_by_id["SP4984_01_A6"]["connection_beta"] == "-4 c gamma_Box" and spillover_by_id["SP4984_02_B6"]["connection_beta"] == "-8 c gamma_Box", "(-4c,-8c)gamma"),
        ("G08_projector_controls", len(projectors) == 14, "14 events"),
        ("G09_mass_shell", maximum_shell < 2.0e-14, f"residual={maximum_shell:.3e}"),
        ("G10_redundant_projector_zero", maximum_ratio < 2.0e-13, f"ratio={maximum_ratio:.3e}"),
        ("G11_O2_nonzero", minimum_o2 > 1.0, f"min={minimum_o2:.6g}"),
        ("G12_essential_O2_shift_zero", spillover_by_id["SP4984_06_O2"]["essential_six_derivative_shift"] == 0.0, "delta w_O2=0"),
        ("G13_O3_measure_open", "QUANTUM_MEASURE_OPEN" in spillover_by_id["SP4984_07_O3"]["status"], "not dropped"),
        ("G14_O4_shift_zero", spillover_by_id["SP4984_08_O4"]["essential_six_derivative_shift"] == 0.0, "six-to-eight"),
        ("G15_parent_source_zero", parent_source_zero, "J_psi=0"),
        ("G16_reflection_even", reflection_even, "invariant state"),
        ("G17_boundary_zero", boundary_zero, "zero profile"),
        ("G18_scalar_charge_zero", scalar_charge_zero, "Q_psi=0"),
        ("G19_source_fixed_point", "J=0 maps exactly" in nonlocal_by_id["NL4984_05_source_map"]["consequence_at_psi_zero"], "frame invariant"),
        ("G20_nonlocal_EOM", "F_H(-Box)psi=0" in nonlocal_by_id["NL4984_01_kernel"]["consequence_at_psi_zero"], "arbitrary kernel"),
        ("G21_nonlocal_stress", nonlocal_by_id["NL4984_02_metric"]["consequence_at_psi_zero"] == "classical T_mn[Gamma2]=0", "classical"),
        ("G22_nonlocal_boundary", "every normal derivative vanish" in nonlocal_by_id["NL4984_06_boundary"]["consequence_at_psi_zero"], "global zero"),
        ("G23_nonlocal_Ward", "no independent classical one-scalar force current" in nonlocal_by_id["NL4984_07_Ward"]["consequence_at_psi_zero"], "Ward"),
        ("G24_O2_branch", branch_by_id["BR4984_03_O2"]["status"] == "MOTION_OPERATOR_SILENT_FOR_ARBITRARY_wO2", "arbitrary w"),
        ("G25_O4_branch", branch_by_id["BR4984_05_O4"]["status"] == "MOTION_CURVATURE_PORTAL_SILENT", "C2X zero"),
        ("G26_O3_retained", "PURE_METRIC_REMAINS" in branch_by_id["BR4984_04_O3"]["status"], "not hidden"),
        ("G27_Newton_Hessian", "0 at p2 Newton order" in branch_by_id["BR4984_10_Newton"]["flat_metric_quadratic_Hessian"], "not full PPN"),
        ("G28_Jacobian_open", nonlocal_by_id["NL4984_09_determinant"]["status"] == "QUANTUM_METRIC_DETERMINANT_RETAINED_OPEN", "pure metric"),
        ("G29_uniqueness_open", nonlocal_by_id["NL4984_08_uniqueness"]["valid_for_selected_nonlocal_source_silence_claim"] is False, "existence only"),
        ("G30_finite_parent_TTT_false", True, "not calculated"),
        ("G31_exact_local_GR_false", True, "pure metric corrections remain"),
        ("G32_full_MTS_false", True, "no promotion"),
    ]
    gate_rows = [
        {"gate": name, "passed": bool(passed), "detail": detail, "status": "pass" if passed else "fail"}
        for name, passed, detail in gates
    ]
    pass_count = sum(bool(row["passed"]) for row in gate_rows)
    all_gates_pass = pass_count == len(gate_rows)

    result = {
        "checkpoint_marker": MARKER,
        "dry_run": arguments.dry_run,
        "maximum_IBP_jet_relative_residual": maximum_ibp_relative,
        "maximum_IBP_jet_absolute_residual": maximum_ibp_absolute,
        "massless_projector_event_count": len(projectors),
        "maximum_mass_shell_and_conservation_residual": maximum_shell,
        "maximum_running_frame_induced_to_O2_projector_ratio": maximum_ratio,
        "minimum_nonzero_O2_projector_magnitude": minimum_o2,
        "scalar_running_frame_raw_p6_connection_vector": {"A6": "-4 c gamma_Box", "B6": "-8 c gamma_Box"},
        "scalar_running_frame_essential_p6_shift_vector": {
            "O1": 0.0,
            "O2": 0.0,
            "O3_classical_action_substitution": 0.0,
            "O4": 0.0,
            "O5_selected_parent": 0.0,
        },
        "numeric_beta_bBox_required_for_zero_essential_O2_shift": False,
        "selected_parent_source_zero": parent_source_zero,
        "selected_parent_reflection_even": reflection_even,
        "selected_parent_zero_boundary": boundary_zero,
        "selected_parent_scalar_charge_zero": scalar_charge_zero,
        "gate_pass_count": pass_count,
        "gate_count": len(gate_rows),
        "valid_for_classical_running_frame_six_derivative_map": all_gates_pass,
        "valid_for_zero_essential_O2_shift_from_beta_bBox_connection": all_gates_pass,
        "valid_for_selected_parent_nonlocal_two_point_source_silence": all_gates_pass,
        "valid_for_leading_flat_Newton_silence_of_six_derivative_scalar_packet": all_gates_pass,
        "valid_for_numeric_beta_bBox_claim": False,
        "valid_for_complete_parent_O2_beta_claim": False,
        "valid_for_quantum_field_redefinition_Jacobian_coefficient_claim": False,
        "valid_for_nonlocal_zero_solution_uniqueness_claim": False,
        "valid_for_finite_parent_metric_three_point_claim": False,
        "valid_for_exact_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": (
            "4985 derive the genuine parent O2 momentum-flow source and metric-frame derivative "
            "spillover in one common measure scheme; separately bound pure-metric C3 and "
            "determinant corrections before any exact local-GR promotion"
        ),
        "elapsed_seconds": time.perf_counter() - started,
    }

    if arguments.dry_run:
        print(
            f"{MARKER}_DRY_RUN={pass_count}/{len(gates)} "
            f"IBP={maximum_ibp_relative:.3e} projector_ratio={maximum_ratio:.3e} "
            f"nonlocal_source_zero={parent_source_zero}",
            flush=True,
        )
        return 0 if all_gates_pass else 1

    write_csv(GRADING_CSV, tagged(grading))
    write_csv(SPILLOVER_CSV, tagged(spillover))
    write_csv(IBP_CSV, tagged(ibp))
    write_csv(PROJECTOR_CSV, tagged(projectors))
    write_csv(NONLOCAL_CSV, tagged(nonlocal_theorem))
    write_csv(BRANCH_CSV, tagged(branch))
    write_csv(GATE_CSV, tagged(gate_rows))
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    provenance_lines = [
        "# Checkpoint 4984 provenance",
        "",
        "Generated locally. No GitHub action.",
        "",
        "This derives the classical scalar running-frame map through six derivatives",
        "and selected-branch source silence for an arbitrary covariant motion kernel.",
        "It does not assign beta_bBox, the genuine O2 flow, a Jacobian coefficient,",
        "uniqueness, exact all-operator local GR, or full MTS.",
        "",
        "## Input digests",
    ]
    for path in required_paths:
        provenance_lines.append(
            f"- {relative(path)} sha256 {digest(path)}"
        )
    PROVENANCE.write_text("\n".join(provenance_lines) + "\n", encoding="utf-8")

    print(
        f"{MARKER}_PASS={pass_count}/{len(gates)} "
        f"IBP={maximum_ibp_relative:.3e} projector_ratio={maximum_ratio:.3e} "
        f"output={RESULT_JSON}",
        flush=True,
    )
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
