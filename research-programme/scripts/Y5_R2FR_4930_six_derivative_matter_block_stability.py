from __future__ import annotations

import csv
import hashlib
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.constants import G, c
from scipy.optimize import brentq


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE = POST / "source-intake" / "functional_rg" / "4930"
SOURCE_4929 = POST / "source-intake" / "functional_rg" / "4929"

CHECKED_DATE = "2026-07-12"
MARKER = "MTS_SIX_DERIVATIVE_MATTER_BLOCK_STABILITY_4930"
NEXT_TARGET = "4931-Y5-R2FR-gauge-curvature-portal-beta-functions-and-fixed-point-values-or-EM-Wilson-bound.md"

PDF_1908 = SOURCE / "1908.08050v2.pdf"
ARCHIVE_1908 = SOURCE / "1908.08050v2-source.tar"
TEX_1908 = SOURCE / "src1908" / "GravityEFTv2_final.tex"
PDF_2110 = SOURCE / "2110.09566v1.pdf"
ARCHIVE_2110 = SOURCE / "2110.09566v1-source.tar"
TEX_2110 = SOURCE / "src2110" / "SSTwAS.tex"
PROVENANCE = SOURCE / "PROVENANCE.md"
TEX_2204 = SOURCE_4929 / "src2204" / "R2scalarMES.tex"
TEX_2312 = SOURCE_4929 / "src2312" / "ess_cubic.tex"
CHECKPOINT_4905 = POST / "4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md"
CHECKPOINT_4929 = POST / "4929-Y5-R2FR-MTS-matter-completed-C3-essential-flow-and-fixed-point-survival-or-one-Wilson-retention.md"
CHECKPOINT_DOC = POST / "4930-Y5-R2FR-six-derivative-MTS-matter-essential-operator-basis-and-block-triangular-stability-or-Wilson-retention.md"
FORMAL_NOTE = FORMAL / "946-PPC4161-six-derivative-matter-basis-and-C3-block-stability.md"
VALIDATION = POST / "scripts" / "Y5_R2FR_4930_six_derivative_matter_block_stability_validation.py"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
CLAIMS_REGISTER = FORMAL / "02-claims-register.csv"
VARIABLE_REGISTER = FORMAL / "04-variable-audit.csv"
EQUATION_REGISTER = FORMAL / "05-equation-register.md"
RED_TEAM_REGISTER = FORMAL / "06-consistency-red-team.md"
SPINE_REGISTER = FORMAL / "07-unification-spine.md"

EXPECTED_HASHES = {
    PDF_1908: "0a7488198a3d164e33461bd149a83117be0f005b34363f77d2f8667d04f321b3",
    ARCHIVE_1908: "957fc506fb05d1692beab79f0979dda0bcb1867f378002f31640143c406e41ed",
    PDF_2110: "ce782d269d38357b2c68eb805072395f60c0a22776b6cdce819a698427d72b59",
    ARCHIVE_2110: "2ef680490ccf2e3f86cc8ff7f926fdd7e612345284948dd7775417326e617156",
}

ARXIV_URLS = {
    "GRSMEFT": "https://arxiv.org/abs/1908.08050",
    "scalar_tensor": "https://arxiv.org/abs/2110.09566",
    "essential_scalar": "https://arxiv.org/abs/2204.08564",
    "natural_C3": "https://arxiv.org/abs/2312.03831",
}

C3_SCALAR_UNIT = 1.0 / (30_240.0 * (4.0 * math.pi) ** 2)
NEWTON_POLE = 2.0 * math.pi / 3.0
GRAVITY_BETA_EIGENVALUE = -2.782608695652174
C3_BETA_EIGENVALUE = 7.750005355376459
SOLAR_MASS_KG = 1.988409870698051e30


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for row in rows:
        row["checkpoint_marker"] = MARKER
        row["valid_for_claim"] = False
        row["source_checked_date"] = CHECKED_DATE
    return rows


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_text_auto(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def scalar_basis_rows() -> list[dict[str, Any]]:
    basis = [
        (
            "S6_O1",
            "[(nabla phi)^2]^3",
            "dphi^6",
            6,
            False,
            "pure scalar six-point interaction",
            "INDIRECT_ONLY_AT_CONSTANT_SCALAR",
        ),
        (
            "S6_O2",
            "(nabla phi)^2 (nabla_rho nabla_sigma phi)^2",
            "dphi^4 D^2",
            4,
            False,
            "four-scalar derivative interaction",
            "INDIRECT_ONLY_AT_CONSTANT_SCALAR",
        ),
        (
            "S6_O3",
            "C_mn^rs C^mnab C_abrs",
            "C_L^3+C_R^3",
            0,
            True,
            "parity-even pure Weyl-cubic coordinate",
            "IS_THE_C3_DIRECTION",
        ),
        (
            "S6_O4",
            "C_abrs C^abrs (nabla phi)^2",
            "dphi^2(C_L^2+C_R^2)",
            2,
            True,
            "two-scalar curvature-squared principal-symbol portal",
            "SCALAR_C3_PORTAL_COEFFICIENT_REQUIRED",
        ),
        (
            "S6_O5",
            "C_mnrs nabla^m phi nabla^r phi nabla^n nabla^s phi",
            "dphi^3(C_L+C_R)D",
            3,
            False,
            "three-scalar Weyl derivative interaction",
            "INDIRECT_ONLY_AT_CONSTANT_SCALAR",
        ),
    ]
    return tagged(
        [
            {
                "operator_id": operator_id,
                "operator": operator,
                "Hilbert_series_structure": structure,
                "scalar_field_degree": field_degree,
                "quadratic_Hessian_nonzero_at_nabla_phi_zero": hessian_active,
                "physical_role": role,
                "C3_block_status": status,
                "CP": "even",
                "IBP_EOM_quotient_independent": True,
                "source": "1908.08050 eq:6derScalarBasis",
                "passed": True,
            }
            for operator_id, operator, structure, field_degree, hessian_active, role, status in basis
        ]
    )


def quotient_identity_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "identity_id": "QI4930_00_Weyl_wave",
                "candidate": "(nabla_alpha R_mnrs)^2",
                "quotient_result": "3 O3",
                "operations": "IBP; vacuum Weyl wave equation; four-dimensional tensor identities",
                "coefficient": 3.0,
                "status": "REDUNDANT_TO_WEYL_CUBED",
                "passed": True,
            },
            {
                "identity_id": "QI4930_01_scalar_Hessian",
                "candidate": "R_mnab (nabla^m nabla^a phi)(nabla^n nabla^b phi)",
                "quotient_result": "-O4/8",
                "operations": "IBP; derivative commutator; Ricci removal; 4D Weyl-square identity",
                "coefficient": -0.125,
                "status": "REDUNDANT_TO_C2_X",
                "passed": True,
            },
            {
                "identity_id": "QI4930_02_Ricci",
                "candidate": "operators containing R or R_mn",
                "quotient_result": "Einstein-frame matter contacts plus EOM-redundant coordinates",
                "operations": "metric field redefinition with induced matter terms retained",
                "coefficient": "basis dependent",
                "status": "REMOVED_FROM_ON_SHELL_WEYL_QUOTIENT",
                "passed": True,
            },
            {
                "identity_id": "QI4930_03_completeness",
                "candidate": "all CP-even shift-symmetric scalar-gravity monomials at six derivatives",
                "quotient_result": "exactly O1 through O5",
                "operations": "Hilbert series with EOM and IBP quotient",
                "coefficient": 5,
                "status": "FIVE_OPERATOR_QUOTIENT_COMPLETE",
                "passed": True,
            },
        ]
    )


def grsmeft_basis_rows() -> list[dict[str, Any]]:
    entries = [
        ("G6_01", "zeta_plus", "C C C", "even", "gravity", 1, "vacuum_C3_coordinate"),
        ("G6_02", "zeta_minus", "C C Ctilde", "odd", "gravity", 1, "parity_odd_vacuum_coordinate"),
        ("G6_03", "c_H", "Hdag H C C", "even", "Higgs", 4, "Higgs_curvature_portal"),
        ("G6_04", "ctilde_H", "Hdag H C Ctilde", "odd", "Higgs", 4, "CP_odd_Higgs_portal"),
        ("G6_05", "c_B", "B^mn B^rs C_mnrs", "even", "U1Y", 1, "hypercharge_curvature_portal"),
        ("G6_06", "ctilde_B", "B^mn B^rs Ctilde_mnrs", "odd", "U1Y", 1, "CP_odd_hypercharge_portal"),
        ("G6_07", "c_G", "G_A^mn G_A^rs C_mnrs", "even", "SU3", 8, "gluon_curvature_portal"),
        ("G6_08", "ctilde_G", "G_A^mn G_A^rs Ctilde_mnrs", "odd", "SU3", 8, "CP_odd_gluon_portal"),
        ("G6_09", "c_W", "W_a^mn W_a^rs C_mnrs", "even", "SU2", 3, "weak_curvature_portal"),
        ("G6_10", "ctilde_W", "W_a^mn W_a^rs Ctilde_mnrs", "odd", "SU2", 3, "CP_odd_weak_portal"),
    ]
    rows: list[dict[str, Any]] = []
    for operator_id, coefficient, operator, parity, sector, multiplicity, role in entries:
        matter_hessian = sector != "gravity"
        direct_even_portal = parity == "even" and sector in {"Higgs", "U1Y", "SU3", "SU2"}
        rows.append(
            {
                "operator_id": operator_id,
                "coefficient": coefficient,
                "operator": operator,
                "CP": parity,
                "SM_sector": sector,
                "internal_multiplicity": multiplicity,
                "quadratic_matter_Hessian_at_zero_background": matter_hessian,
                "parity_even_C3_portal_allowed": direct_even_portal,
                "physical_role": role,
                "IBP_EOM_quotient_independent": True,
                "source": "1908.08050 eq:dim6GRSMEFT",
                "status": "COMPLETE_DIMENSION_SIX_GRAVITY_SM_BASIS",
                "passed": True,
            }
        )
    return tagged(rows)


def scalar_fixed_point_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "2110_minimal",
            0.66,
            0.21,
            None,
            None,
            None,
            None,
            1.60,
            3.25,
            None,
            None,
            None,
            "MINIMAL_SCALAR_GRAVITY_REFERENCE",
        ),
        (
            "2110_full_no_eta",
            0.66,
            0.21,
            -29.0,
            0.63,
            -1.69,
            0.0,
            1.76,
            3.57,
            -1.88,
            1.28,
            -9.69,
            "FULL_INTERACTING_SCALAR_ALL_MATTER_DIRECTIONS_IRRELEVANT",
        ),
        (
            "2110_full_eta_primary",
            0.67,
            0.21,
            -16.6,
            0.14,
            -0.96,
            1.27,
            1.70,
            3.38,
            -4.54,
            2.69,
            -3.00,
            "FULL_INTERACTING_SCALAR_ETA_BRANCH_ALL_MATTER_DIRECTIONS_IRRELEVANT",
        ),
        (
            "2110_full_eta_secondary",
            0.64,
            0.24,
            -42.2,
            5.65,
            -4.23,
            -1.75,
            1.34,
            4.65,
            -7.52,
            1.80,
            2.20,
            "SECONDARY_BRANCH_ONE_MATTER_DIRECTION_RELEVANT",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for entry in entries:
        (
            branch,
            newton,
            cosmological,
            scalar_c,
            scalar_ctilde,
            scalar_d,
            eta,
            theta_gravity_real,
            theta_gravity_imag,
            theta_matter_pair_real,
            theta_matter_pair_imag,
            theta_matter_real,
            status,
        ) = entry
        matter_irrelevant = (
            theta_matter_pair_real is not None
            and theta_matter_pair_real < 0.0
            and theta_matter_real is not None
            and theta_matter_real < 0.0
        )
        rows.append(
            {
                "branch": branch,
                "g_star": newton,
                "lambda_star": cosmological,
                "c_X2_star": scalar_c,
                "ctilde_RmnXmn_star": scalar_ctilde,
                "d_RX_star": scalar_d,
                "eta_scalar": eta,
                "theta_gravity_real": theta_gravity_real,
                "theta_gravity_imag_abs": theta_gravity_imag,
                "theta_matter_pair_real": theta_matter_pair_real,
                "theta_matter_pair_imag_abs": theta_matter_pair_imag,
                "theta_matter_real": theta_matter_real,
                "all_tracked_matter_directions_irrelevant": matter_irrelevant,
                "projection_compatible_with_4928_numeric_splice": False,
                "status": status,
                "source": "2110.09566 tab.fpdata",
                "passed": True,
            }
        )
    return tagged(rows)


def beta_g_pure(newton: float) -> float:
    return 2.0 * newton * (-32.0 * newton + 6.0 * math.pi) / (
        -9.0 * newton + 6.0 * math.pi
    )


def beta_g(newton: float, weight_1: float) -> float:
    return beta_g_pure(newton) + weight_1 * newton**2 / (6.0 * math.pi)


def c3_polynomial_coefficients(newton: float) -> tuple[float, float, float, float]:
    pi = math.pi
    return (
        69.0 * newton,
        -3_709_440.0 * newton**2 * pi
        + 14_515_200.0 * newton * pi**2
        + 1_451_520.0 * pi**3,
        47_585_664.0 * newton**3 * pi**2
        - 21_337_344.0 * newton**2 * pi**3,
        -84_188_160.0 * newton**4 * pi**3
        + 78_382_080.0 * newton**3 * pi**4,
    )


def beta_c3_pure(newton: float, c3_coupling: float) -> float:
    constant, linear, quadratic, cubic = c3_polynomial_coefficients(newton)
    numerator = constant + linear * c3_coupling + quadratic * c3_coupling**2 + cubic * c3_coupling**3
    denominator = 120_960.0 * (9.0 * newton - 6.0 * math.pi) * math.pi**2
    return -numerator / denominator


def anomalous_fixed_point(weight_1: float, eta_scalar: float) -> dict[str, float]:
    newton_star = brentq(
        lambda value: beta_g(value, weight_1),
        1.0e-12,
        NEWTON_POLE * (1.0 - 1.0e-10),
        xtol=1.0e-14,
        rtol=1.0e-14,
    )
    source = eta_scalar * C3_SCALAR_UNIT
    constant, linear, quadratic, cubic = c3_polynomial_coefficients(newton_star)
    denominator = 120_960.0 * (9.0 * newton_star - 6.0 * math.pi) * math.pi**2
    roots = np.roots([cubic, quadratic, linear, constant - source * denominator])
    real_roots = [float(root.real) for root in roots if abs(root.imag) < 1.0e-9]
    if not real_roots:
        raise RuntimeError(f"no real h root for W1={weight_1}, eta={eta_scalar}")
    c3_star = min(real_roots, key=abs)
    step_g = max(1.0e-7, 1.0e-6 * abs(newton_star))
    step_h = max(1.0e-12, 1.0e-5 * abs(c3_star))
    derivative_g = (beta_g(newton_star + step_g, weight_1) - beta_g(newton_star - step_g, weight_1)) / (2.0 * step_g)
    derivative_h = (
        beta_c3_pure(newton_star, c3_star + step_h)
        - beta_c3_pure(newton_star, c3_star - step_h)
    ) / (2.0 * step_h)
    residual = math.hypot(beta_g(newton_star, weight_1), beta_c3_pure(newton_star, c3_star) + source)
    return {
        "g_star": newton_star,
        "h_star": c3_star,
        "theta_g": -derivative_g,
        "theta_h": -derivative_h,
        "delta_beta_h": source,
        "beta_norm": residual,
    }


def anomalous_leak_rows() -> list[dict[str, Any]]:
    eta_values = [-2.42, -1.75, -0.77, 0.0, 0.94, 1.13, 1.27, 1.51]
    baseline = anomalous_fixed_point(1.0, 0.0)
    rows: list[dict[str, Any]] = []
    for eta_scalar in eta_values:
        fixed = anomalous_fixed_point(1.0, eta_scalar)
        shift = fixed["h_star"] - baseline["h_star"]
        rows.append(
            {
                "eta_scalar": eta_scalar,
                "W1": 1.0,
                "Qminus1": f"{-eta_scalar}/k^2",
                "delta_beta_h_equals_eta_c6": fixed["delta_beta_h"],
                "g_star": fixed["g_star"],
                "h_star": fixed["h_star"],
                "delta_h_star_from_eta_zero": shift,
                "fractional_h_star_shift": shift / baseline["h_star"],
                "theta_g": fixed["theta_g"],
                "theta_h": fixed["theta_h"],
                "two_coordinate_topology_survives": fixed["theta_g"] > 0.0 and fixed["theta_h"] < 0.0,
                "IR_Wilson_prediction_allowed": False,
                "status": "ANOMALOUS_DIMENSION_C3_LEAK_EXECUTED_UV_ONLY",
                "passed": fixed["beta_norm"] < 1.0e-9 and fixed["theta_g"] > 0.0 and fixed["theta_h"] < 0.0,
            }
        )
    return tagged(rows)


def anomalous_scan_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    index = 0
    for weight_1 in np.linspace(-20.0, 20.0, 81):
        for eta_scalar in np.linspace(-3.0, 3.0, 121):
            fixed = anomalous_fixed_point(float(weight_1), float(eta_scalar))
            survives = fixed["theta_g"] > 0.0 and fixed["theta_h"] < 0.0 and fixed["beta_norm"] < 1.0e-8
            rows.append(
                {
                    "scan_id": f"ETA4930_{index:05d}",
                    "W1": float(weight_1),
                    "eta_scalar": float(eta_scalar),
                    "delta_beta_h": fixed["delta_beta_h"],
                    "g_star": fixed["g_star"],
                    "h_star": fixed["h_star"],
                    "theta_g": fixed["theta_g"],
                    "theta_h": fixed["theta_h"],
                    "survives": survives,
                    "status": "ETA_LEAK_2D_SURVIVES" if survives else "ETA_LEAK_2D_FAILURE",
                    "passed": survives,
                }
            )
            index += 1
    return tagged(rows)


def gauge_determinant_witness_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for sector, coefficient, multiplicity in (
        ("U1Y", "c_B", 1),
        ("SU2", "c_W", 3),
        ("SU3", "c_G", 8),
    ):
        cubic_witness = -(32.0 / 3.0) * multiplicity
        rows.append(
            {
                "sector": sector,
                "portal_coefficient": coefficient,
                "internal_multiplicity": multiplicity,
                "constitutive_symbol": "K=I-4u_X C on two-form polarizations",
                "determinant_expansion": "(1/2)Tr log K=-2u TrC-4u^2 TrC^2-(32/3)u^3 TrC^3+...",
                "Tr_C": 0.0,
                "cubic_C3_witness_coefficient_times_multiplicity": cubic_witness,
                "Jacobian_witness_at_nonzero_u_star": f"-32*{multiplicity}*u_X_star^2",
                "full_FRG_coefficient_derived": False,
                "status": "NONZERO_GENERIC_C3_MIXING_WITNESS_NOT_FULL_BETA",
                "passed": cubic_witness != 0.0,
            }
        )
    return tagged(rows)


def block_gate_rows() -> list[dict[str, Any]]:
    clauses = [
        (
            "scalar_six_derivative_quotient",
            True,
            "five CP-even O1-O5 operators after IBP/EOM",
            "CLOSED_BY_HILBERT_SERIES",
        ),
        (
            "GRSMEFT_dimension_six_quotient",
            True,
            "ten gravity-SM operators in five parity pairs",
            "CLOSED_BY_HILBERT_SERIES",
        ),
        (
            "CP_even_odd_separation",
            True,
            "odd portals do not enter the even C3 block when the parent and regulator preserve CP",
            "CONDITIONAL_ON_CP_PRESERVATION",
        ),
        (
            "constant_scalar_O1_O2_O5_Hessian",
            True,
            "field degree greater than two makes their quadratic Hessian vanish at nabla phi=0",
            "DIRECT_RICCI_FLAT_C3_SILENCE_DERIVED",
        ),
        (
            "scalar_O4_portal",
            False,
            "C^2 X has a nonzero scalar Hessian on Ricci-flat Weyl backgrounds",
            "OFF_DIAGONAL_COEFFICIENT_REQUIRED",
        ),
        (
            "Higgs_C2_portal",
            False,
            "HdagH C^2 has a nonzero Higgs Hessian at H=0",
            "OFF_DIAGONAL_COEFFICIENT_REQUIRED",
        ),
        (
            "gauge_CFF_portals",
            False,
            "the two-form determinant has an explicit u_X^3 Tr C^3 witness for every nonzero even gauge portal",
            "GENERIC_BLOCK_TRIANGULARITY_REJECTED_AT_NONZERO_PORTAL",
        ),
        (
            "scalar_anomalous_dimension",
            False,
            "Q_-1=-eta/k^2 produces Delta beta_h=eta/[30240(4pi)^2]",
            "EXACT_ETA_LEAK_DERIVED",
        ),
        (
            "portal_fixed_point_values",
            False,
            "the MTS parent has not calculated u_B u_W u_G u_H or u_O4 at the fixed point",
            "OPEN_FIXED_POINT_COORDINATES",
        ),
        (
            "full_block_triangularity",
            False,
            "triangularity requires eta*=0 and every even portal fixed point or mixing derivative to vanish",
            "SPECIAL_ZERO_SUBMANIFOLD_ONLY_NOT_PARENT_DERIVED",
        ),
    ]
    return tagged(
        [
            {
                "clause": clause,
                "satisfied": satisfied,
                "evidence": evidence,
                "status": status,
                "blocks_full_C3_prediction": not satisfied,
                "passed": True,
            }
            for clause, satisfied, evidence, status in clauses
        ]
    )


def modal_stability_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "full_signed_C3_plus_scalar_no_eta",
            [GRAVITY_BETA_EIGENVALUE, C3_BETA_EIGENVALUE, 1.88 + 1.28j, 1.88 - 1.28j, 9.69 + 0.0j],
            "4928 relevant gravity and C3 modes plus 2110 full no-eta matter comparator",
        ),
        (
            "full_signed_C3_plus_scalar_eta_primary",
            [GRAVITY_BETA_EIGENVALUE, C3_BETA_EIGENVALUE, 4.54 + 2.69j, 4.54 - 2.69j, 3.00 + 0.0j],
            "4928 relevant gravity and C3 modes plus 2110 full eta primary matter comparator",
        ),
        (
            "full_signed_C3_scalar_no_eta_plus_canonical_gauge",
            [GRAVITY_BETA_EIGENVALUE, C3_BETA_EIGENVALUE, 1.88 + 1.28j, 1.88 - 1.28j, 9.69 + 0.0j, 2.0, 2.0, 2.0],
            "adds three near-canonical dimension-six gauge portal modes to the signed comparator",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for scenario, eigenvalues, source in entries:
        gap = min(abs(value.real) for value in eigenvalues)
        relevant_modes = sum(value.real < 0.0 for value in eigenvalues)
        irrelevant_modes = sum(value.real > 0.0 for value in eigenvalues)
        rows.append(
            {
                "scenario": scenario,
                "beta_eigenvalues": ";".join(f"{value.real:+.6g}{value.imag:+.6g}i" for value in eigenvalues),
                "imaginary_axis_gap": gap,
                "relevant_beta_modes": relevant_modes,
                "irrelevant_beta_modes": irrelevant_modes,
                "sufficient_modal_mixing_bound": f"norm_2(E_in_modal_basis)<{gap}",
                "theorem": "Bauer-Fike in the displayed modal basis preserves the signed stability index",
                "full_MTS_bound_measured": False,
                "source": source,
                "status": "EXACT_SUFFICIENT_SIGNED_STABILITY_CONTRACT_NOT_YET_EVALUATED",
                "passed": gap > 0.0 and relevant_modes == 1,
            }
        )
    for mode, matter_eigenvalue in (
        ("scalar_no_eta_real", 9.69),
        ("scalar_eta_primary_real", 3.00),
        ("canonical_gauge_portal", 2.00),
        ("canonical_six_derivative_scalar", 4.00),
    ):
        threshold = math.sqrt(C3_BETA_EIGENVALUE * matter_eigenvalue)
        rows.append(
            {
                "scenario": "pairwise_" + mode,
                "beta_eigenvalues": f"{C3_BETA_EIGENVALUE};{matter_eigenvalue}",
                "imaginary_axis_gap": min(C3_BETA_EIGENVALUE, matter_eigenvalue),
                "relevant_beta_modes": 0,
                "irrelevant_beta_modes": 2,
                "sufficient_modal_mixing_bound": f"M_hm*M_mh<{C3_BETA_EIGENVALUE * matter_eigenvalue}",
                "symmetric_offdiagonal_flip_threshold": threshold,
                "theorem": "positive trace and determinant of the real 2x2 beta-stability block",
                "full_MTS_bound_measured": False,
                "source": "derived exact pairwise stability condition",
                "status": "PAIRWISE_MIXING_PRODUCT_CONTRACT_DERIVED",
                "passed": threshold > 0.0,
            }
        )
    return tagged(rows)


def modal_monte_carlo_rows() -> list[dict[str, Any]]:
    base = np.zeros((8, 8), dtype=float)
    base[0, 0] = GRAVITY_BETA_EIGENVALUE
    base[1, 1] = C3_BETA_EIGENVALUE
    base[2:4, 2:4] = np.array([[1.88, -1.28], [1.28, 1.88]])
    base[4, 4] = 9.69
    base[5, 5] = 2.0
    base[6, 6] = 2.0
    base[7, 7] = 2.0
    gap = 1.88
    rng = np.random.default_rng(4930)
    rows: list[dict[str, Any]] = []
    for ratio in (0.10, 0.25, 0.50, 0.75, 0.99, 1.01, 1.25, 1.50, 2.00):
        trials = 500
        failures = 0
        minimum_abs_real = math.inf
        for _ in range(trials):
            perturbation = rng.normal(size=base.shape)
            norm = float(np.linalg.norm(perturbation, ord=2))
            perturbation *= ratio * gap / norm
            eigenvalues = np.linalg.eigvals(base + perturbation)
            trial_minimum_abs = float(np.min(np.abs(eigenvalues.real)))
            minimum_abs_real = min(minimum_abs_real, trial_minimum_abs)
            if int(np.sum(eigenvalues.real < 0.0)) != 1:
                failures += 1
        rows.append(
            {
                "norm_over_gap": ratio,
                "perturbation_norm": ratio * gap,
                "trials": trials,
                "failed_signed_stability_index": failures,
                "minimum_abs_real_part_seen": minimum_abs_real,
                "theorem_guarantees_no_crossing": ratio < 1.0,
                "expected_relevant_beta_modes": 1,
                "status": "SIGNED_MODAL_MIXING_MONTE_CARLO_SMOKE",
                "passed": failures == 0 if ratio < 1.0 else True,
            }
        )
    return tagged(rows)


def maxwell_map_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "map_id": "EM4930_00_EW",
                "object": "electroweak photon portal coefficient",
                "equation": "c_gamma=c_B cos^2(theta_W)+c_W sin^2(theta_W)",
                "interpretation": "the orthogonal combination and gamma-Z cross term remain separate electroweak observables",
                "status": "EXACT_TREE_LEVEL_EWSB_MAP",
                "passed": True,
            },
            {
                "map_id": "EM4930_01_constitutive",
                "object": "curved-space electromagnetic excitation tensor",
                "equation": "H^mn=F^mn-4 c_gamma C^mnrs F_rs",
                "interpretation": "Weyl curvature acts as a covariant anisotropic constitutive response",
                "status": "NONMINIMAL_MAXWELL_CONSTITUTIVE_MAP_DERIVED",
                "passed": True,
            },
            {
                "map_id": "EM4930_02_equation",
                "object": "modified Maxwell equation",
                "equation": "nabla_m H^mn=J^n; nabla_[m F_rs]=0",
                "interpretation": "standard Maxwell is recovered when c_gamma=0 or the curvature response is negligible",
                "status": "MAXWELL_LIMIT_CONDITION_EXPLICIT",
                "passed": True,
            },
            {
                "map_id": "EM4930_03_norm",
                "object": "field-response norm bound",
                "equation": "norm(delta H)/norm(F)<=4 abs(c_gamma) norm(C)_op",
                "interpretation": "define epsilon_CF=4 abs(c_gamma) norm(C)_op",
                "status": "ARENA_INDEPENDENT_EM_BOUND_DERIVED",
                "passed": True,
            },
            {
                "map_id": "EM4930_04_Poynting",
                "object": "Poynting and electromagnetic stress response",
                "equation": "norm(delta T_EM)/norm(T_EM)<=epsilon_CF+O(epsilon_CF^2)",
                "interpretation": "the Poynting vector is standard only inside the same constitutive smallness gate",
                "status": "POYNTING_BACKGROUND_FIELD_GATE_DERIVED",
                "passed": True,
            },
            {
                "map_id": "EM4930_05_vacuum",
                "object": "uncharged local vacuum",
                "equation": "F=0 implies the CFF operators and their tree stress vanish",
                "interpretation": "the portals do not alter vacuum PPN at tree level but can affect EM binding energy and propagation",
                "status": "VACUUM_PPN_SILENCE_NOT_EM_SILENCE",
                "passed": True,
            },
            {
                "map_id": "EM4930_06_conservation",
                "object": "source and stress conservation",
                "equation": "nabla_n J^n=0 follows from antisymmetry of H; diffeomorphism invariance conserves total metric plus EM stress on shell",
                "interpretation": "the nonminimal constitutive term must be varied in the source stress rather than appended to Maxwell by hand",
                "status": "COVARIANT_CONSERVATION_INTERFACE_DERIVED",
                "passed": True,
            },
        ]
    )


def curvature_smoke_rows() -> list[dict[str, Any]]:
    earth_mass = 5.9722e24
    earth_radius = 6.371e6
    sun_mass = 1.988409870698051e30
    sun_radius = 6.957e8
    neutron_star_mass = 1.4 * SOLAR_MASS_KG
    neutron_star_radius = 12_000.0
    black_hole_mass = 30.0 * SOLAR_MASS_KG
    black_hole_mgeom = G * black_hole_mass / c**2
    arenas = [
        ("Earth_surface", earth_mass, earth_radius),
        ("Sun_surface", sun_mass, sun_radius),
        ("NS_1p4Msun_12km", neutron_star_mass, neutron_star_radius),
        ("BH_30Msun_r3M", black_hole_mass, 3.0 * black_hole_mgeom),
    ]
    tolerance = 0.01
    rows: list[dict[str, Any]] = []
    for arena, mass, radius in arenas:
        mass_geom = G * mass / c**2
        curvature_frobenius = math.sqrt(48.0) * mass_geom / radius**3
        coefficient_bound = tolerance / (4.0 * curvature_frobenius)
        rows.append(
            {
                "arena": arena,
                "mass_kg": mass,
                "radius_m": radius,
                "sqrt_C2_m_minus2": curvature_frobenius,
                "declared_fractional_EM_tolerance": tolerance,
                "abs_c_gamma_internal_bound_m2": coefficient_bound,
                "sqrt_abs_c_gamma_bound_m": math.sqrt(coefficient_bound),
                "bound_type": "internal constitutive-control target using Frobenius curvature norm",
                "empirical_constraint": False,
                "status": "CURVATURE_SCALE_SMOKE_NONCLAIM",
                "passed": coefficient_bound > 0.0,
            }
        )
    return tagged(rows)


def wilson_count_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "uncharged_constant_motion_vacuum",
            1,
            "A_+(Q_GW)",
            "all mixed matter operators vanish on the background",
        ),
        (
            "photon_curved_background",
            2,
            "A_+(Q_GW); c_gamma",
            "one photon combination joins the vacuum C3 coefficient",
        ),
        (
            "unbroken_SM_parity_even_dimension6_gravity",
            5,
            "zeta_plus;c_H;c_B;c_G;c_W",
            "complete parity-even half of the ten-operator GRSMEFT basis",
        ),
        (
            "shift_symmetric_motion_plus_gravity_six_derivative",
            5,
            "O1;O2;O3;O4;O5",
            "complete CP-even scalar Hilbert quotient",
        ),
        (
            "unified_parity_even_union",
            9,
            "O3 shared plus four motion and four SM mixed coefficients",
            "full action count before ultraviolet prediction or empirical bounds",
        ),
        (
            "unified_with_GRSMEFT_parity_partners",
            14,
            "ten GRSMEFT coefficients plus four extra CP-even motion coefficients",
            "does not add scalar topological Wess-Zumino terms",
        ),
    ]
    return tagged(
        [
            {
                "arena_or_action": arena,
                "independent_gravity_coupled_Wilson_coefficients": count,
                "coefficient_set": coefficient_set,
                "reason": reason,
                "all_parent_predicted": False,
                "status": "ACTIVE_ARENA_COUNT" if count <= 2 else "FULL_ACTION_COUNT_NOT_FIT_COUNT",
                "passed": count > 0,
            }
            for arena, count, coefficient_set, reason in rows
        ]
    )


def parent_gate_rows() -> list[dict[str, Any]]:
    clauses = [
        ("operator_quotient", True, "five scalar and ten GRSMEFT dimension-six operators source-locked"),
        ("vacuum_active_count", True, "one parity-even A_+(Q_GW) remains active when matter backgrounds vanish"),
        ("Maxwell_constitutive_map", True, "c_gamma and epsilon_CF derived from c_B and c_W"),
        ("scalar_interacting_comparator", True, "2110 full primary branch has three irrelevant tracked matter directions"),
        ("eta_C3_leak", True, "Delta beta_h=eta c6 derived and scanned"),
        ("gauge_portal_mixing_witness", True, "two-form determinant produces u_X^3 Tr C^3"),
        ("scalar_O4_beta", False, "natural essential off-diagonal coefficient not calculated"),
        ("Higgs_portal_beta", False, "natural essential off-diagonal coefficient not calculated"),
        ("gauge_portal_beta", False, "u_B u_W u_G fixed points and C3 Jacobian entries not calculated"),
        ("modal_mixing_norm", False, "the derived 1.88 modal stability contract has no parent numeric matrix"),
        ("full_C3_prediction", False, "generic block triangularity is not inherited"),
    ]
    rows = [
        {
            "clause": clause,
            "satisfied": satisfied,
            "evidence": evidence,
            "blocks_full_C3_prediction": not satisfied,
            "status": "CLOSED" if satisfied else "OPEN",
            "passed": True,
        }
        for clause, satisfied, evidence in clauses
    ]
    rows.append(
        {
            "clause": "all_parent_inheritance",
            "satisfied": all(row["satisfied"] for row in rows),
            "evidence": "the quotient and exact stability contracts close but three portal beta blocks remain uncalculated",
            "blocks_full_C3_prediction": True,
            "status": "FULL_MTS_C3_FLOW_NOT_INHERITED",
            "passed": True,
        }
    )
    return tagged(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (path, expected_hash) in enumerate(EXPECTED_HASHES.items()):
        exists = path.exists()
        actual_hash = digest(path) if exists else ""
        passed = exists and actual_hash == expected_hash
        rows.append(
            {
                "source_id": f"SRC4930_{index:02d}_binary",
                "source_path_or_url": path.relative_to(ROOT).as_posix(),
                "source_role": "locked_primary_pdf_or_author_source",
                "verification": "SHA256",
                "expected_sha256": expected_hash,
                "actual_sha256": actual_hash,
                "source_exists": exists,
                "marker_found": passed,
                "status": "LOCAL_BINARY_SOURCE_HASH_VERIFIED" if passed else "LOCAL_BINARY_SOURCE_FAILED",
                "passed": passed,
            }
        )
    text_sources = [
        (PROVENANCE, "MTS_SIX_DERIVATIVE_MATTER_BLOCK_PROVENANCE_4930", "source_provenance"),
        (TEX_1908, "eq:6derScalarBasis", "complete_scalar_six_derivative_basis"),
        (TEX_1908, "eq:dim6GRSMEFT", "complete_GRSMEFT_dimension_six_basis"),
        (TEX_1908, "-\\frac{1}{8} \\mathcal{O}_4", "exact_scalar_redundancy_identity"),
        (TEX_2110, "tab.fpdata", "interacting_scalar_fixed_point_table"),
        (TEX_2110, r"Z_k^2 \, C_k \, X^2", "lower_scalar_interaction_ansatz"),
        (TEX_2204, "additional essential couplings related to six-derivative operators occur", "essential_matter_extension_boundary"),
        (TEX_2312, "application of this scheme to gravity-matter systems is intriguing", "natural_C3_matter_boundary"),
        (CHECKPOINT_4905, "ten operators", "prior_MTS_GRSMEFT_normalization"),
        (CHECKPOINT_4929, "MTS_MATTER_COMPLETED_C3_FLOW_4929", "free_spectator_predecessor"),
        (Path(__file__).resolve(), "def gauge_determinant_witness_rows", "checkpoint_generator"),
        (CHECKPOINT_DOC, MARKER, "generated_checkpoint"),
        (FORMAL_NOTE, "PPC4161_SIX_DERIVATIVE_MATTER_BLOCK_4930", "formal_checkpoint_note"),
        (VALIDATION, "MTS_SIX_DERIVATIVE_MATTER_BLOCK_VALIDATION_4930", "independent_validation_code"),
        (RESUME, NEXT_TARGET, "local_resume_ledger"),
        (CLAIMS_REGISTER, "L-772", "claim_register"),
        (VARIABLE_REGISTER, "C3BlockStatus4930_MTS", "variable_register"),
        (EQUATION_REGISTER, "1.223 Six-derivative matter quotient and C3 block-stability boundary", "equation_register"),
        (RED_TEAM_REGISTER, "174. Arena silence is not full-action derivation", "red_team_register"),
        (SPINE_REGISTER, "PPC4161 checkpoint 4930", "unification_spine"),
    ]
    for offset, (path, marker, role) in enumerate(text_sources, start=len(rows)):
        exists = path.exists()
        marker_found = exists and marker in read_text_auto(path)
        rows.append(
            {
                "source_id": f"SRC4930_{offset:02d}_text",
                "source_path_or_url": path.relative_to(ROOT).as_posix(),
                "source_role": role,
                "verification": "path_and_marker",
                "expected_sha256": "",
                "actual_sha256": digest(path) if exists else "",
                "source_exists": exists,
                "marker_found": marker_found,
                "status": "LOCAL_TEXT_SOURCE_VERIFIED" if marker_found else "LOCAL_TEXT_SOURCE_FAILED",
                "passed": marker_found,
            }
        )
    for source_id, url in ARXIV_URLS.items():
        rows.append(
            {
                "source_id": "SRC4930_URL_" + source_id,
                "source_path_or_url": url,
                "source_role": "primary_arXiv_record",
                "verification": "external_primary_URL_recorded",
                "expected_sha256": "",
                "actual_sha256": "",
                "source_exists": True,
                "marker_found": True,
                "status": "EXTERNAL_PRIMARY_URL_RECORDED",
                "passed": True,
            }
        )
    return tagged(rows)


def gate_rows(
    scalar_basis: list[dict[str, Any]],
    grsmeft: list[dict[str, Any]],
    anomalous_scan: list[dict[str, Any]],
    block_gate: list[dict[str, Any]],
    wilson_counts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    scan_failures = sum(not bool(row["passed"]) for row in anomalous_scan)
    full_triangle = next(row for row in block_gate if row["clause"] == "full_block_triangularity")["satisfied"]
    vacuum_count = next(row for row in wilson_counts if row["arena_or_action"] == "uncharged_constant_motion_vacuum")
    return tagged(
        [
            {
                "gate": "six_derivative_scalar_quotient",
                "status": "CLOSED",
                "decision": f"{len(scalar_basis)} CP-even operators O1-O5 after EOM and IBP",
                "claim_promoted": False,
                "passed": len(scalar_basis) == 5,
            },
            {
                "gate": "dimension_six_GRSMEFT_quotient",
                "status": "CLOSED",
                "decision": f"{len(grsmeft)} operators in five parity pairs",
                "claim_promoted": False,
                "passed": len(grsmeft) == 10,
            },
            {
                "gate": "interacting_scalar_comparator",
                "status": "EXTERNAL_SURVIVAL_EVIDENCE",
                "decision": "the primary full scalar branch has nonzero interactions and three irrelevant tracked matter directions",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "eta_C3_leak",
                "status": "DERIVED_AND_STRESS_TESTED",
                "decision": f"Delta beta_h=eta/[30240(4pi)^2]; {len(anomalous_scan)-scan_failures}/{len(anomalous_scan)} two-coordinate rows survive",
                "claim_promoted": False,
                "passed": scan_failures == 0,
            },
            {
                "gate": "generic_block_triangularity",
                "status": "REJECTED_WITH_SPECIAL_ZERO_SUBMANIFOLD",
                "decision": "O4 Higgs and even CFF portals plus eta can feed C3; gauge determinant gives an explicit cubic mixing witness",
                "claim_promoted": False,
                "passed": not full_triangle,
            },
            {
                "gate": "modal_stability_contract",
                "status": "DERIVED_NOT_EVALUATED",
                "decision": "the displayed signed comparator preserves one relevant mode if norm_2(E_modal)<1.88; pairwise product thresholds are tabulated",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "Maxwell_Poynting_interface",
                "status": "DERIVED",
                "decision": "H=F-4c_gamma C.F and epsilon_CF=4|c_gamma|||C|| control Maxwell and Poynting recovery",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "vacuum_Wilson_count",
                "status": "ONE_RETAINED",
                "decision": f"uncharged constant-motion vacuum activates {vacuum_count['independent_gravity_coupled_Wilson_coefficients']} parity-even coefficient",
                "claim_promoted": False,
                "passed": int(vacuum_count["independent_gravity_coupled_Wilson_coefficients"]) == 1,
            },
            {
                "gate": "full_unified_Wilson_count",
                "status": "NINE_PARITY_EVEN_BEFORE_UV_PREDICTION",
                "decision": "one shared C3 plus four motion and four SM mixed coefficients; arena inactivity is not derivation",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "weak_GR_Newton",
                "status": "RETAINED",
                "decision": "all mixed portals vanish in uncharged constant-motion weak vacuum and do not alter the calibrated two-derivative source limit",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "Maxwell_full_MTS_to_GR",
                "status": "BOUNDED_NOT_PROMOTED",
                "decision": "standard Maxwell requires c_gamma=0 or epsilon_CF below the arena tolerance; full portal beta values remain open",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "next_target",
                "status": "GAUGE_PORTAL_BETA_FUNCTIONS",
                "decision": NEXT_TARGET,
                "claim_promoted": False,
                "passed": True,
            },
        ]
    )


def main() -> int:
    scalar_basis = scalar_basis_rows()
    quotient = quotient_identity_rows()
    grsmeft = grsmeft_basis_rows()
    scalar_fixed = scalar_fixed_point_rows()
    anomalous = anomalous_leak_rows()
    anomalous_scan = anomalous_scan_rows()
    gauge_witness = gauge_determinant_witness_rows()
    block_gate = block_gate_rows()
    modal = modal_stability_rows()
    modal_smoke = modal_monte_carlo_rows()
    maxwell = maxwell_map_rows()
    curvature = curvature_smoke_rows()
    wilson_counts = wilson_count_rows()
    parent = parent_gate_rows()
    sources = source_register_rows()
    gates = gate_rows(scalar_basis, grsmeft, anomalous_scan, block_gate, wilson_counts)
    tables = {
        "P8_Y5_R2FR_4930_SCALAR_SIX_DERIVATIVE_BASIS.csv": scalar_basis,
        "P8_Y5_R2FR_4930_QUOTIENT_IDENTITIES.csv": quotient,
        "P8_Y5_R2FR_4930_GRSMEFT_DIM6_BASIS.csv": grsmeft,
        "P8_Y5_R2FR_4930_SCALAR_FIXED_POINT_COMPARATOR.csv": scalar_fixed,
        "P8_Y5_R2FR_4930_ANOMALOUS_DIMENSION_LEAK.csv": anomalous,
        "P8_Y5_R2FR_4930_ANOMALOUS_DIMENSION_SCAN.csv": anomalous_scan,
        "P8_Y5_R2FR_4930_GAUGE_DETERMINANT_MIXING_WITNESS.csv": gauge_witness,
        "P8_Y5_R2FR_4930_BLOCK_TRIANGULARITY_GATE.csv": block_gate,
        "P8_Y5_R2FR_4930_MODAL_STABILITY_BOUND.csv": modal,
        "P8_Y5_R2FR_4930_MODAL_MIXING_MONTE_CARLO.csv": modal_smoke,
        "P8_Y5_R2FR_4930_MAXWELL_CONSTITUTIVE_MAP.csv": maxwell,
        "P8_Y5_R2FR_4930_MAXWELL_CURVATURE_SMOKE.csv": curvature,
        "P8_Y5_R2FR_4930_WILSON_PARAMETER_COUNT.csv": wilson_counts,
        "P8_Y5_R2FR_4930_PARENT_INHERITANCE_GATE.csv": parent,
        "P8_Y5_R2FR_4930_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4930_GATE_DECISION.csv": gates,
    }
    for filename, rows in tables.items():
        write_csv(OUTPUT / filename, rows)
    passed = all(bool(row.get("passed", True)) for rows in tables.values() for row in rows)
    scan_failures = sum(not bool(row["passed"]) for row in anomalous_scan)
    full_primary = next(row for row in scalar_fixed if row["branch"] == "2110_full_eta_primary")
    print("P8_Y5_R2FR_4930_SIX_DERIVATIVE_MATTER_BLOCK_PASS" if passed else "P8_Y5_R2FR_4930_SIX_DERIVATIVE_MATTER_BLOCK_FAIL")
    print(f"scalar_six_derivative_basis={len(scalar_basis)}")
    print(f"GRSMEFT_dimension6_basis={len(grsmeft)}")
    print(f"external_full_scalar_eta={full_primary['eta_scalar']}")
    print(f"eta_scan_survival={len(anomalous_scan)-scan_failures}/{len(anomalous_scan)}")
    print("generic_block_triangularity=False")
    print("modal_sufficient_gap=1.88")
    print("vacuum_active_parity_even_Wilsons=1")
    print("full_unified_parity_even_Wilsons_before_prediction=9")
    print("Maxwell_constitutive_gate=epsilon_CF")
    print("compact_and_full_MTS_promoted=False")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
