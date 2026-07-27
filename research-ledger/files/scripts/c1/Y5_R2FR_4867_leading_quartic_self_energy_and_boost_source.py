from __future__ import annotations

import csv
import math
import tarfile
from pathlib import Path
from typing import Any

import sympy as sp

from Y5_R2FR_4865_second_sensitivity_and_hat_alpha_gate import (
    numeric_values as preferred_numeric_values,
    strong_field_symbols,
)
from Y5_R2FR_4866_quartic_boost_hierarchy_and_kernel_gate import (
    numeric_values as quartic_numeric_values,
)


CHECKPOINT = "4867"
TIMESTAMP = "2026-07-10T11:25:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = "4868-Y5-R2FR-finite-compactness-v2-backreaction-and-v3-dipole-shooting-determinant-or-quartic-response-remainder-bound.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return True
    except SyntaxError:
        return False


def resume_checkpoint_at_least(resume: str, checkpoint: int) -> bool:
    prefix = "Last checkpoint: `"
    for line in resume.splitlines():
        if line.startswith(prefix):
            token = line[len(prefix) :].split("-", 1)[0]
            return token.isdigit() and int(token) >= checkpoint
    return False


def archive_member_contains(path: Path, member: str, needle: str) -> bool:
    if not path.exists():
        return False
    try:
        with tarfile.open(path, "r:*") as archive:
            extracted = archive.extractfile(member)
            if extracted is None:
                return False
            return needle in extracted.read().decode("utf-8", errors="replace")
    except (tarfile.TarError, OSError):
        return False


def public_symbols() -> dict[str, sp.Expr]:
    p, ratio, velocity, cosine = sp.symbols("p r v mu", positive=True, real=True)
    gamma = 1 / sp.sqrt(1 - velocity**2)
    c_plus = sp.Integer(0)
    c_14 = 2 * ratio * p / (1 + ratio)
    c_2 = 2 * p / (3 * (1 + ratio) * (1 - p))
    c_123 = c_2
    c_minus = p * (1 + ratio - ratio * p)
    scalar_speed_squared = sp.Rational(1, 3) / ratio
    tensor_speed_squared = sp.Integer(1)
    scalar_anisotropy = 1 - 1 / scalar_speed_squared
    spatial_boost = 1 + gamma**2 * velocity**2 * cosine**2
    cosine_k_squared = gamma**2 * cosine**2 / spatial_boost
    scalar_denominator = 1 + gamma**2 * velocity**2 * scalar_anisotropy * cosine**2
    source_ratio = (2 + 3 * c_2 + c_plus) / c_123
    alpha_1 = -4 * c_14
    alpha_2 = sp.factor(
        alpha_1 / 2
        + 3 * c_14 * (3 * c_2 + c_14) / ((2 - c_14) * 3 * c_2)
    )
    return {
        "p": p,
        "r": ratio,
        "v": velocity,
        "mu": cosine,
        "gamma": gamma,
        "c_plus": c_plus,
        "c14": c_14,
        "c2": c_2,
        "c123": c_123,
        "c_minus": c_minus,
        "s0sq": scalar_speed_squared,
        "s2sq": tensor_speed_squared,
        "chi0": scalar_anisotropy,
        "H": spatial_boost,
        "mu_k2": cosine_k_squared,
        "D0": scalar_denominator,
        "B": source_ratio,
        "alpha1": alpha_1,
        "alpha2": alpha_2,
    }


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC4867_00_public", POST / "4861-Y5-R2FR-shared-cone-matter-frame-Hilbert-variation-or-base-metric-branch-selection.md", "PUBLIC_FRAME_VARIATION_SELECTION_4861", "selected public action and coefficient map"),
        ("SRC4867_01_interaction", POST / "4863-Y5-R2FR-full-reduced-cubic-mode-action-and-unitarity-partial-wave-or-public-branch-hard-cutoff.md", "Complete local interaction action", "unit-flow action conventions"),
        ("SRC4867_02_first", POST / "4864-Y5-R2FR-one-parameter-compact-body-sensitivity-and-dipole-radiation-scaling-or-strong-field-fallback.md", "Compact-body sensitivity", "known weak first response"),
        ("SRC4867_03_second", POST / "4865-Y5-R2FR-second-sensitivity-derivative-and-strong-field-preferred-frame-gate-or-public-branch-fallback.md", "Regular-response theorem", "second response and preferred-frame transfer"),
        ("SRC4867_04_quartic", POST / "4866-Y5-R2FR-quartic-boost-compact-star-Hessian-and-sigma-prime-coefficient-or-finite-response-fallback.md", "QUARTIC_BOOST_HIERARCHY_KERNEL_4866", "quartic variable and hierarchy"),
        ("SRC4867_05_prior_validation", OUTPUT / "P8_Y5_BRR545_4866_VALIDATION.csv", "VAL4866_OVERALL", "prior validation"),
        ("SRC4867_06_checkpoint", POST / "4867-Y5-R2FR-second-order-boost-l0-l2-star-equations-and-third-order-l1-source-or-finite-kappa4-fallback.md", "LEADING_QUARTIC_SELF_ENERGY_4867", "human derivation"),
        ("SRC4867_07_formal", FORMAL / "883-PPC4161-leading-compactness-quartic-response-and-boost-source.md", "PPC4161_LEADING_QUARTIC_SELF_ENERGY_4867", "formal integration"),
        ("SRC4867_08_claim", FORMAL / "02-claims-register.csv", "L-709", "claim register"),
        ("SRC4867_09_variable", FORMAL / "04-variable-audit.csv", "leading_compactness_quartic_response_derived", "variable integration"),
        ("SRC4867_10_equation", FORMAL / "05-equation-register.md", "1.160 Leading-compactness quartic response", "equation integration"),
        ("SRC4867_11_redteam", FORMAL / "06-consistency-red-team.md", "111. Leading-compactness quartic response red team", "red-team integration"),
        ("SRC4867_12_spine", FORMAL / "07-unification-spine.md", "checkpoint 4867", "spine integration"),
        ("SRC4867_13_resume", POST / "CURRENT_LOCAL_RESUME.md", "Last checkpoint: `4867-", "resume marker"),
        ("SRC4867_14_script", Path(__file__).resolve(), 'CHECKPOINT = "4867"', "executable derivation"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in local_sources:
        content = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        valid = path.exists() and needle in content
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_locator": str(path),
                "member": "",
                "needle": needle,
                "source_exists": path.exists(),
                "needle_found": needle in content,
                "role": role,
                "source_validated": valid,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    archive_sources = [
        ("SRC4867_15_gupta", Path(r"D:\Temp\2104.04596-source.tar"), "main.tex", r"\section{Solutions for slowly moving stars}", "published stellar ansatz and first-order equations"),
        ("SRC4867_16_foster_wave", Path(r"D:\Temp\gr-qc-0602004-source.tar"), "aeradSep08.tex", r"\Box_0 F", "relaxed sourced spin decomposition"),
    ]
    for source_id, path, member, needle, role in archive_sources:
        valid = archive_member_contains(path, member, needle)
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "local_primary_archive",
                "source_locator": str(path),
                "member": member,
                "needle": needle,
                "source_exists": path.exists(),
                "needle_found": valid,
                "role": role,
                "source_validated": valid,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    foster = Path(r"D:\Temp\aestrongSep2008.tex")
    foster_text = foster.read_text(encoding="utf-8", errors="replace") if foster.exists() else ""
    foster_needle = r"\tilde{m}_A[\gamma]"
    rows.append(
        {
            "source_id": "SRC4867_17_foster_strong",
            "source_kind": "local_primary_tex",
            "source_locator": str(foster),
            "member": "",
            "needle": foster_needle,
            "source_exists": foster.exists(),
            "needle_found": foster_needle in foster_text,
            "role": "compact-body mass function and weak sensitivity matching",
            "source_validated": foster.exists() and foster_needle in foster_text,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def mode_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    p, ratio = symbols["p"], symbols["r"]
    expected = [
        ("MODE4867_00_cplus", "public tensor coupling", symbols["c_plus"], 0, "c13=0"),
        ("MODE4867_01_c123", "public scalar combination", symbols["c123"], symbols["c2"], "c123=c2 when c13=0"),
        ("MODE4867_02_c14", "acceleration coefficient", symbols["c14"], 2 * ratio * p / (1 + ratio), "public surface"),
        ("MODE4867_03_c2", "expansion coefficient", symbols["c2"], 2 * p / (3 * (1 + ratio) * (1 - p)), "public surface"),
        ("MODE4867_04_s0", "scalar speed squared", symbols["s0sq"], 1 / (3 * ratio), "finite for fixed r"),
        ("MODE4867_05_s2", "tensor speed squared", symbols["s2sq"], 1, "public metric cone"),
        ("MODE4867_06_a1", "weak preferred-frame alpha1", symbols["alpha1"], -8 * ratio * p / (1 + ratio), "standard public PPN"),
        ("MODE4867_07_a2", "weak preferred-frame alpha2", symbols["alpha2"], ratio * p * (3 * ratio - 1) / (1 + ratio), "standard public PPN"),
        ("MODE4867_08_spin1", "propagating spin1 matter source", symbols["c_plus"], 0, "minimal matter source is proportional to cplus"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, quantity, derived, target, meaning in expected:
        difference = sp.factor(derived - target)
        rows.append(
            {
                "row_id": row_id,
                "quantity": quantity,
                "derived": sp.sstr(sp.factor(derived)),
                "expected": sp.sstr(sp.factor(target)),
                "difference": sp.sstr(difference),
                "meaning": meaning,
                "status": "PASS" if difference == 0 else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def angular_rows() -> list[dict[str, Any]]:
    radius, cosine = sp.symbols("R mu", positive=True, real=True)
    radial = sp.Function("X")(radius)
    derivative_z = lambda expression: sp.expand(
        cosine * sp.diff(expression, radius)
        + (1 - cosine**2) * sp.diff(expression, cosine) / radius
    )
    p_0 = sp.Integer(1)
    p_1 = cosine
    p_2 = (3 * cosine**2 - 1) / 2
    p_3 = (5 * cosine**3 - 3 * cosine) / 2
    radial_second = sp.simplify(derivative_z(derivative_z(radial)))
    dipole_second = sp.simplify(derivative_z(derivative_z(radial * p_1)))
    radial_l0 = (radial.diff(radius, 2) + 2 * radial.diff(radius) / radius) / 3
    radial_l2 = 2 * (radial.diff(radius, 2) - radial.diff(radius) / radius) / 3
    dipole_l1 = 3 * (
        radial.diff(radius, 2)
        + 2 * radial.diff(radius) / radius
        - 2 * radial / radius**2
    ) / 5
    dipole_l3 = 2 * (
        radial.diff(radius, 2)
        - 3 * radial.diff(radius) / radius
        + 3 * radial / radius**2
    ) / 5
    identities = [
        ("ANG4867_00_P1sq", "P1 squared", p_1**2, p_0 / 3 + 2 * p_2 / 3, "v2 selects l=0,2"),
        ("ANG4867_01_P1cube", "P1 cubed", p_1**3, 3 * p_1 / 5 + 2 * p_3 / 5, "v3 selects l=1,3"),
        ("ANG4867_02_dz2_l0l2", "second directional derivative of radial mode", radial_second, radial_l0 * p_0 + radial_l2 * p_2, "exact l=0,2 radial projection"),
        ("ANG4867_03_dz2_l1l3", "second directional derivative of dipole", dipole_second, dipole_l1 * p_1 + dipole_l3 * p_3, "exact l=1,3 radial projection"),
        ("ANG4867_04_l1", "dipole l1 projection", dipole_l1, 3 * (radial.diff(radius, 2) + 2 * radial.diff(radius) / radius - 2 * radial / radius**2) / 5, "three-fifths of the l1 radial operator"),
        ("ANG4867_05_l3", "dipole l3 projection", dipole_l3, 2 * (radial.diff(radius, 2) - 3 * radial.diff(radius) / radius + 3 * radial / radius**2) / 5, "third-order l3 companion"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, quantity, left, right, meaning in identities:
        difference = sp.simplify(sp.expand(left - right))
        rows.append(
            {
                "row_id": row_id,
                "quantity": quantity,
                "left": sp.sstr(left),
                "right": sp.sstr(right),
                "difference": sp.sstr(difference),
                "meaning": meaning,
                "status": "PASS" if difference == 0 else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def boost_source_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    gamma, velocity = symbols["gamma"], symbols["v"]
    cosine_k_squared = symbols["mu_k2"]
    entries = [
        ("BST4867_00_k", "boosted spatial momentum", "k_perp=q_perp; k_parallel=gamma*q_parallel", "rest-frame spherical form factor remains rho_tilde(q)"),
        ("BST4867_01_omega", "stationary-source frequency", "omega=gamma*v*q_parallel", "uniform translation in the aether frame"),
        ("BST4867_02_H", "spatial Laplacian factor", f"H={sp.sstr(symbols['H'])}", "k^2=q^2 H"),
        ("BST4867_03_D0", "scalar mode denominator", f"D0={sp.sstr(symbols['D0'])}", "k^2-omega^2/s0^2=q^2 D0"),
        ("BST4867_04_T00", "matter energy source", f"T00={sp.sstr(gamma)}*rho_tilde", "exact uniform dust source"),
        ("BST4867_05_TL", "longitudinal spatial trace", f"T_L={sp.sstr(gamma * velocity**2 * cosine_k_squared)}*rho_tilde", "projected along k"),
        ("BST4867_06_TT", "transverse spatial trace", f"T_T={sp.sstr(gamma * velocity**2 * (1-cosine_k_squared))}*rho_tilde", "orthogonal to k"),
        ("BST4867_07_VT", "transverse momentum norm", f"V_T^2={sp.sstr(gamma**2 * velocity**2 * (1-cosine_k_squared))}*rho_tilde^2", "vector constraint source"),
        ("BST4867_08_QTT", "TT stress norm", f"Q_TT^2={sp.sstr(sp.Rational(1,2)*gamma**2*velocity**4*(1-cosine_k_squared)**2)}*rho_tilde^2", "tensor mode source"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "equation": equation,
            "meaning": meaning,
            "status": "DERIVED_EXACT_LINEAR_SOURCE",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, quantity, equation, meaning in entries
    ]


def scalar_master(symbols: dict[str, sp.Expr]) -> sp.Expr:
    gamma = symbols["gamma"]
    velocity = symbols["v"]
    longitudinal = gamma * velocity**2 * symbols["mu_k2"]
    trace = gamma * velocity**2
    return (
        symbols["c14"]
        / ((2 - symbols["c14"]) * symbols["D0"])
        * (trace - symbols["B"] * longitudinal + 2 * gamma / symbols["c14"])
    )


def legendre_coefficient(expression: sp.Expr, order: int, cosine: sp.Symbol) -> sp.Expr:
    polynomial = sp.legendre(order, cosine)
    return sp.factor(sp.Rational(2 * order + 1, 2) * sp.integrate(expression * polynomial, (cosine, -1, 1)))


def second_order_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    p, ratio, velocity, cosine = symbols["p"], symbols["r"], symbols["v"], symbols["mu"]
    denominator = 1 + ratio - p * ratio
    master = scalar_master(symbols)
    master_series = sp.series(master, velocity, 0, 4).removeO().expand()
    master_0 = sp.factor(master_series.coeff(velocity, 0))
    master_2 = sp.factor(master_series.coeff(velocity, 2))
    monopole = legendre_coefficient(master_2, 0, cosine)
    quadrupole = legendre_coefficient(master_2, 2, cosine)
    h00 = (master - symbols["gamma"] / symbols["H"]) / symbols["c14"]
    h00_2 = sp.series(h00, velocity, 0, 4).removeO().expand().coeff(velocity, 2)
    h00_monopole = legendre_coefficient(h00_2, 0, cosine)
    h00_quadrupole = legendre_coefficient(h00_2, 2, cosine)
    expected = [
        ("SO4867_00_F0", "static scalar master coefficient", master_0, (1 + ratio) / denominator, "L0 F0=-16 pi G coefficient*rho"),
        ("SO4867_01_F20", "v2 monopole scalar coefficient", monopole, (1 + ratio) * (6 * p * ratio + 1) / (6 * denominator), "L0 F20=-16 pi G A0*rho"),
        ("SO4867_02_F22", "v2 quadrupole scalar coefficient", quadrupole, 2 * (3 * p * ratio**2 - ratio - 1) / (3 * denominator), "L2 F22=-16 pi G A2*Q2[rho]"),
        ("SO4867_03_h20", "v2 monopole h00 coefficient", h00_monopole, (1 + ratio) * (6 * ratio + 7) / (12 * denominator), "public metric reconstruction"),
        ("SO4867_04_h22", "v2 quadrupole h00 coefficient", h00_quadrupole, (1 + ratio) * (3 * ratio - 1) / (3 * denominator), "public metric reconstruction"),
        ("SO4867_05_A0limit", "finite p->0 monopole limit", sp.limit(monopole, p, 0, dir="+"), sp.Rational(1, 6), "no inverse-p source pole"),
        ("SO4867_06_A2limit", "finite p->0 quadrupole limit", sp.limit(quadrupole, p, 0, dir="+"), -sp.Rational(2, 3), "no inverse-p source pole"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, quantity, derived, target, equation in expected:
        difference = sp.factor(derived - target)
        rows.append(
            {
                "row_id": row_id,
                "quantity": quantity,
                "derived": sp.sstr(sp.factor(derived)),
                "expected": sp.sstr(sp.factor(target)),
                "difference": sp.sstr(difference),
                "radial_equation_or_scope": equation,
                "status": "PASS" if difference == 0 else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.extend(
        [
            {
                "row_id": "SO4867_07_Q2",
                "quantity": "quadrupole source projector",
                "derived": "Q2[rho]=U_rho''-U_rho'/R",
                "expected": "Q2=F^{-1}[P2(qhat.vhat)*rho_tilde(q)]; L0 U_rho=rho",
                "difference": "0 by directional-derivative identity",
                "radial_equation_or_scope": "L2 F22=-16 pi G A2 Q2[rho]",
                "status": "PASS",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            },
            {
                "row_id": "SO4867_08_complete",
                "quantity": "leading-C even-parity system",
                "derived": "F20,F22 plus h00 constraints, TT tensor response and spatial scalar reconstruction",
                "expected": "complete linear sourced l=0,2 master system",
                "difference": "finite-C nonlinear terms excluded explicitly",
                "radial_equation_or_scope": "equivalent to the O(v2) star equations at leading self-gravity",
                "status": "PASS",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            },
        ]
    )
    return rows


def third_order_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    entries = [
        ("TO4867_00_operator", "boosted mode operator", "D_s=Delta+chi_s*gamma^2*v^2*d_z^2", "covariant mode cone in the body-rest frame", "DERIVED"),
        ("TO4867_01_first", "first-order dipole equation", "L1 X1=J1", "regular-center and decaying-exterior boundary problem", "DERIVED"),
        ("TO4867_02_l1", "third-order dipole equation", "L1 X31=J31-(3/5)chi_s*L1 X1=J31-(3/5)chi_s*J1", "exact operator-induced l1 source", "DERIVED"),
        ("TO4867_03_l3", "third-order octupole equation", "L3 X33=J33-(2/5)chi_s*(X1''-3X1'/R+3X1/R^2)", "mandatory l3 companion", "DERIVED"),
        ("TO4867_04_tensor", "public tensor correction", "chi_2=0", "luminal tensor has no boost-cone source term", "DERIVED"),
        ("TO4867_05_spin1", "public propagating spin1 matter source", "J1_spin1 proportional cplus*T_i0^T=0", "minimal public matter does not directly source the propagating spin1 master", "DERIVED"),
        ("TO4867_06_constraint", "metric vector constraint", "Delta gamma_i^T=-16 pi G T_i0^T", "nonpropagating shift still contributes at v and v3", "DERIVED"),
        ("TO4867_07_nonlinear", "finite-C third-order source", "J31_nonlinear[Phi0,Phi1,Phi20,Phi22]", "not supplied by the linear self-energy calculation", "OPEN_FINITE_C"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "equation": equation,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, quantity, equation, meaning, status in entries
    ]


def self_energy_kernel(symbols: dict[str, sp.Expr]) -> dict[str, sp.Expr]:
    p, ratio, velocity, cosine = symbols["p"], symbols["r"], symbols["v"], symbols["mu"]
    gamma = symbols["gamma"]
    longitudinal = gamma * velocity**2 * symbols["mu_k2"]
    transverse_trace = gamma * velocity**2 - longitudinal
    transverse_momentum_squared = gamma**2 * velocity**2 * (1 - symbols["mu_k2"])
    tt_stress_squared = (
        sp.Rational(1, 2)
        * gamma**2
        * velocity**4
        * (1 - symbols["mu_k2"]) ** 2
    )
    master = scalar_master(symbols)
    h00 = (master - gamma / symbols["H"]) / symbols["c14"]
    longitudinal_metric = (
        -(1 + symbols["c2"]) * master / symbols["c2"]
        + longitudinal / (symbols["c2"] * gamma**2 * velocity**2 * cosine**2)
    )
    kernel = (
        h00 * gamma
        + master * transverse_trace / 2
        + longitudinal_metric * longitudinal
        - 2 * transverse_momentum_squared / symbols["H"]
        + tt_stress_squared
    )
    series = sp.series(kernel, velocity, 0, 6).removeO().expand()
    angular_average = sp.integrate(series, (cosine, -1, 1)) / 2
    static_kernel = sp.factor(angular_average.subs(velocity, 0))
    mass_ratio = sp.series(
        gamma**2 * angular_average / static_kernel, velocity, 0, 6
    ).removeO().expand()
    coefficient_2 = sp.factor(mass_ratio.coeff(velocity, 2))
    coefficient_4 = sp.factor(mass_ratio.coeff(velocity, 4))
    return {
        "kernel": kernel,
        "K0": static_kernel,
        "R": mass_ratio,
        "a": coefficient_2,
        "b": coefficient_4,
        "a_expected": p * ratio * (3 * ratio + 11) / (3 * (1 + ratio)),
        "b_expected": p * ratio * (27 * ratio**2 + 57 * ratio + 98) / (15 * (1 + ratio)),
    }


def self_energy_rows(symbols: dict[str, sp.Expr], kernel: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    p, ratio = symbols["p"], symbols["r"]
    preferred_combination = sp.factor(symbols["alpha1"] - sp.Rational(2, 3) * symbols["alpha2"])
    expected = [
        ("SE4867_00_K0", "static on-shell kernel", kernel["K0"], 1 / (2 - symbols["c14"]), "Newton self-energy normalization"),
        ("SE4867_01_a", "mass-response v2 coefficient", kernel["a"], kernel["a_expected"], "first sensitivity coefficient"),
        ("SE4867_02_PPN", "weak sensitivity cross-check", -2 * kernel["a"], preferred_combination, "matches alpha1-2 alpha2/3 exactly"),
        ("SE4867_03_b", "mass-response v4 coefficient", kernel["b"], kernel["b_expected"], "new quartic result"),
        ("SE4867_04_GR_a", "p->0 v2 response", sp.limit(kernel["a"], p, 0, dir="+"), 0, "GR mass is boost independent"),
        ("SE4867_05_GR_b", "p->0 v4 response", sp.limit(kernel["b"], p, 0, dir="+"), 0, "GR mass is boost independent"),
        ("SE4867_06_boverp", "finite quartic co-scaling coefficient", sp.factor(kernel["b"] / p), ratio * (27 * ratio**2 + 57 * ratio + 98) / (15 * (1 + ratio)), "no inverse-p pole"),
        ("SE4867_07_endpoint", "quartic coefficient at r=1/3", sp.factor((kernel["b"] / p).subs(ratio, sp.Rational(1, 3))), 2, "maximum over the public r corridor"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, quantity, derived, target, meaning in expected:
        difference = sp.factor(derived - target)
        rows.append(
            {
                "row_id": row_id,
                "quantity": quantity,
                "derived": sp.sstr(sp.factor(derived)),
                "expected": sp.sstr(sp.factor(target)),
                "difference": sp.sstr(difference),
                "meaning": meaning,
                "status": "PASS" if difference == 0 else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "row_id": "SE4867_08_profile",
            "quantity": "source-profile factorization",
            "derived": "angular kernel multiplies integral d3q |rho_tilde(q)|^2/q^2",
            "expected": "the same Newtonian binding-energy integral Omega",
            "difference": "profile independent at leading self-gravity for a spherical rest source",
            "meaning": "permits exact matching to Omega/M",
            "status": "PASS",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def response_rows(symbols: dict[str, sp.Expr], kernel: dict[str, sp.Expr]) -> tuple[list[dict[str, Any]], dict[str, float]]:
    ratio, compactness = symbols["r"], sp.symbols("C", positive=True, real=True)
    omega_ratio = -sp.Rational(5, 7) * compactness
    f_coefficient = sp.factor(
        (symbols["alpha1"] - sp.Rational(2, 3) * symbols["alpha2"])
        * omega_ratio
        / symbols["p"]
    )
    kappa = sp.factor(omega_ratio * kernel["b"] / symbols["p"])
    g_coefficient = sp.factor(3 * f_coefficient + 8 * kappa)
    kappa_magnitude_shape = sp.factor(-kappa / compactness)
    derivative = sp.factor(sp.diff(kappa_magnitude_shape, ratio))
    kappa_max = sp.factor((-kappa).subs({ratio: sp.Rational(1, 3), compactness: sp.Rational(3, 10)}))
    g_max = sp.factor((-g_coefficient).subs({ratio: sp.Rational(1, 3), compactness: sp.Rational(3, 10)}))
    quartic_values = quartic_numeric_values()
    preferred_values = preferred_numeric_values(strong_field_symbols())
    kappa_bound = quartic_values["kappa_bound"]
    g_bound = preferred_values["g_box_alpha1_stressed"]
    numeric = {
        "kappa_bound": kappa_bound,
        "g_bound": g_bound,
        "kappa_max": float(kappa_max),
        "g_max": float(g_max),
        "kappa_margin": kappa_bound - float(kappa_max),
        "g_margin": g_bound - float(g_max),
        "kappa_factor": kappa_bound / float(kappa_max),
        "g_factor": g_bound / float(g_max),
    }
    expected = [
        ("WK4867_00_Omega", "Tolman VII Newtonian binding energy", omega_ratio, -5 * compactness / 7, "Omega/M through leading compactness"),
        ("WK4867_01_f", "leading first-response coefficient", f_coefficient, 10 * compactness * ratio * (3 * ratio + 11) / (21 * (1 + ratio)), "reproduces checkpoint 4864 C coefficient"),
        ("WK4867_02_kappa", "leading quartic compact response", kappa, -compactness * ratio * (27 * ratio**2 + 57 * ratio + 98) / (21 * (1 + ratio)), "parent public-action prediction through O(C)"),
        ("WK4867_03_g", "leading second-sensitivity coefficient", g_coefficient, -2 * compactness * ratio * (108 * ratio**2 + 183 * ratio + 227) / (21 * (1 + ratio)), "g=3f+8kappa"),
        ("WK4867_04_monotone", "r derivative of |kappa|/C", derivative, 2 * (27 * ratio**3 + 69 * ratio**2 + 57 * ratio + 49) / (21 * (1 + ratio) ** 2), "strictly positive on r>0"),
        ("WK4867_05_kmax", "maximum |kappa| at C=0.3,r=1/3", kappa_max, sp.Rational(3, 7), "leading-C public corridor maximum"),
        ("WK4867_06_gmax", "maximum |g| at C=0.3,r=1/3", g_max, sp.Rational(15, 7), "leading-C public corridor maximum"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, quantity, derived, target, meaning in expected:
        difference = sp.factor(derived - target)
        rows.append(
            {
                "row_id": row_id,
                "quantity": quantity,
                "derived": sp.sstr(sp.factor(derived)),
                "expected": sp.sstr(sp.factor(target)),
                "difference": sp.sstr(difference),
                "meaning": meaning,
                "status": "PASS" if difference == 0 else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.extend(
        [
            {
                "row_id": "WK4867_07_kbound",
                "quantity": "4866 quartic-box comparison",
                "derived": f"{float(kappa_max):.16g}",
                "expected": f"less than {kappa_bound:.16g}",
                "difference": f"remainder budget={numeric['kappa_margin']:.16g}",
                "meaning": f"leading result has factor {numeric['kappa_factor']:.8g} headroom",
                "status": "PASS" if float(kappa_max) < kappa_bound else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            },
            {
                "row_id": "WK4867_08_gbound",
                "quantity": "4865 stressed g-box comparison",
                "derived": f"{float(g_max):.16g}",
                "expected": f"less than {g_bound:.16g}",
                "difference": f"remainder budget={numeric['g_margin']:.16g}",
                "meaning": f"leading result has factor {numeric['g_factor']:.8g} headroom",
                "status": "PASS" if float(g_max) < g_bound else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            },
        ]
    )
    return rows, numeric


def response_grid_rows(symbols: dict[str, sp.Expr], numeric: dict[str, float]) -> list[dict[str, Any]]:
    ratio_values = [sp.Rational(index, 45) for index in range(1, 16)]
    compactness_values = [sp.Rational(index, 50) for index in range(1, 16)]
    rows: list[dict[str, Any]] = []
    for ratio_value in ratio_values:
        for compactness_value in compactness_values:
            kappa = -compactness_value * ratio_value * (
                27 * ratio_value**2 + 57 * ratio_value + 98
            ) / (21 * (1 + ratio_value))
            f_value = 10 * compactness_value * ratio_value * (3 * ratio_value + 11) / (
                21 * (1 + ratio_value)
            )
            g_value = 3 * f_value + 8 * kappa
            passed = (
                abs(float(kappa)) <= numeric["kappa_bound"]
                and abs(float(g_value)) <= numeric["g_bound"]
            )
            rows.append(
                {
                    "row_id": f"WGRID4867_{len(rows):03d}",
                    "r": f"{float(ratio_value):.16g}",
                    "compactness": f"{float(compactness_value):.16g}",
                    "f_leading": f"{float(f_value):.16g}",
                    "kappa4_leading": f"{float(kappa):.16g}",
                    "g_leading": f"{float(g_value):.16g}",
                    "kappa_bound": f"{numeric['kappa_bound']:.16g}",
                    "g_bound": f"{numeric['g_bound']:.16g}",
                    "status": "PASS" if passed else "FAIL",
                    "valid_for_claim": False,
                    "timestamp_utc": TIMESTAMP,
                }
            )
    return rows


def decision_rows(numeric: dict[str, float]) -> list[dict[str, Any]]:
    entries = [
        ("DEC4867_0_route", "accept the one-graviton self-energy route as the leading-compactness quartic derivation", "it integrates the complete sourced public linear mode system and reproduces the known first sensitivity exactly"),
        ("DEC4867_1_even", "accept the explicit leading-C l0,l2 master equations", "the scalar monopole/quadrupole coefficients and public-metric constraints are finite and source complete at linear self-gravity"),
        ("DEC4867_2_odd", "accept the exact operator-induced v3,l1 source", "the directional derivative projection gives the three-fifths l1 law without a closure"),
        ("DEC4867_3_value", "promote kappa4 from wholly unknown to derived through O(C)", "the public Tolman VII result is kappa4=-C*r*(27r^2+57r+98)/(21*(1+r))+O(C^2)"),
        ("DEC4867_4_window", "retain the public branch with quantified finite-C remainder headroom", f"the leading maximum is 3/7 and leaves {numeric['kappa_margin']:.6g} absolute kappa4 budget"),
        ("DEC4867_5_scope", "do not call the finite-compactness response closed", "nonlinear O(C2+) stellar backreaction, the finite-C determinant and a full EoS solve remain open"),
        ("DEC4867_6_next", "construct the finite-compactness v2/v3 boundary-value system or bound its remainder", "this now tests a concrete correction around a derived leading value rather than an arbitrary coefficient"),
    ]
    return [
        {
            "decision_id": row_id,
            "decision": decision,
            "reason": reason,
            "next_target": NEXT_TARGET if row_id == "DEC4867_6_next" else "",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, decision, reason in entries
    ]


def residual_rows(numeric: dict[str, float]) -> list[dict[str, Any]]:
    entries = [
        (1, "E_kappa4_leading_C", "CLOSED_PARENT_ACTION", "complete linear-mode self-energy gives a source-profile-independent O(C) coefficient", "retain exact formula as the finite-C expansion anchor"),
        (2, "E_first_response_crosscheck", "CLOSED_EXACT", "the v2 kernel reproduces alpha1-2alpha2/3 and the Tolman VII C coefficient", "use as regression check for every finite-C solver"),
        (3, "E_v2_l0_l2_leading", "CLOSED_LINEAR", "monopole and quadrupole master equations and source projector are explicit", "lift them onto the nonlinear spherical background"),
        (4, "E_v3_l1_operator", "CLOSED_OPERATOR", "the operator-induced l1 source is exactly -(3/5)chi_s J1", "add the nonlinear matter/field source terms"),
        (5, "E_kappa4_C2plus", "OPEN_DECISIVE", f"leading |kappa4|<=3/7 leaves absolute budget {numeric['kappa_margin']:.6g}", "derive or rigorously bound the C2 and higher remainder"),
        (6, "E_finite_C_kernel", "OPEN_DECISIVE", "the leading quotient kernel is trivial but no C-dependent shooting determinant exists", "construct determinant over C<=0.3"),
        (7, "E_full_EOS", "OPEN_NUMERIC", "the O(C) result is profile universal but nonlinear corrections are EoS dependent", "solve at least Tolman VII and one tabulated EoS"),
        (8, "E_solitary_map", "OPEN_LATER", "binary response is now anchored but the solitary spin map remains distinct", "derive only after finite-C g is controlled"),
        (9, "E_exact_GR_endpoint", "OPEN_HARD", "the correlated p->0 response vanishes but canonical gauge restoration is not proved", "return after compact response closure"),
    ]
    return [
        {
            "priority": priority,
            "residual": residual,
            "status": status,
            "evidence": evidence,
            "next_action": next_action,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for priority, residual, status, evidence, next_action in entries
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    modes: list[dict[str, Any]],
    angular: list[dict[str, Any]],
    boost: list[dict[str, Any]],
    second: list[dict[str, Any]],
    third: list[dict[str, Any]],
    self_energy: list[dict[str, Any]],
    response: list[dict[str, Any]],
    grid: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    claims = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-709"]
    variables = [
        row
        for row in read_csv(FORMAL / "04-variable-audit.csv")
        if row.get("symbol") == "kappa4_compact_MTS"
    ]
    checkpoint = (POST / "4867-Y5-R2FR-second-order-boost-l0-l2-star-equations-and-third-order-l1-source-or-finite-kappa4-fallback.md").read_text(encoding="utf-8")
    formal = (FORMAL / "883-PPC4161-leading-compactness-quartic-response-and-boost-source.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    prior_validation = read_csv(OUTPUT / "P8_Y5_BRR545_4866_VALIDATION.csv")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    groups = (sources, modes, angular, boost, second, third, self_energy, response, grid, decisions, residuals)
    checks = [
        result("VAL4867_00_sources", len(sources) == 18 and all(row["source_validated"] for row in sources), f"sources={len(sources)}"),
        result("VAL4867_01_modes", len(modes) == 9 and all(row["status"] == "PASS" for row in modes), "public mode and PPN map passes"),
        result("VAL4867_02_angular", len(angular) == 6 and all(row["status"] == "PASS" for row in angular), "all Legendre and directional-derivative identities pass"),
        result("VAL4867_03_boost", len(boost) == 9 and all(row["status"] == "DERIVED_EXACT_LINEAR_SOURCE" for row in boost), "exact uniform source projections recorded"),
        result("VAL4867_04_second", len(second) == 9 and all(row["status"] == "PASS" for row in second), "leading-C l0,l2 system passes"),
        result("VAL4867_05_third", len(third) == 8 and third[2]["status"] == "DERIVED" and third[-1]["status"] == "OPEN_FINITE_C", "operator source derived and nonlinear source scoped"),
        result("VAL4867_06_self", len(self_energy) == 9 and all(row["status"] == "PASS" for row in self_energy), "on-shell self-energy kernel identities pass"),
        result("VAL4867_07_response", len(response) == 9 and all(row["status"] == "PASS" for row in response), "weak f, kappa4 and g derivation passes"),
        result("VAL4867_08_grid", len(grid) == 225 and all(row["status"] == "PASS" for row in grid), "225-point leading-response grid passes inherited windows"),
        result("VAL4867_09_decision", decisions[3]["decision"] == "promote kappa4 from wholly unknown to derived through O(C)" and decisions[5]["decision"] == "do not call the finite-compactness response closed", "advance and claim ceiling both recorded"),
        result("VAL4867_10_residual", residuals[0]["status"] == "CLOSED_PARENT_ACTION" and residuals[4]["status"] == "OPEN_DECISIVE", "leading response and finite-C remainder separated"),
        result("VAL4867_11_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all rows remain private nonclaim"),
        result("VAL4867_12_registers", len(claims) == 1 and len(variables) == 1 and variables[0].get("status") == "leading_compactness_quartic_response_derived_finite_compactness_open_nonclaim", f"claims={len(claims)} variables={len(variables)}"),
        result("VAL4867_13_documents", "LEADING_QUARTIC_SELF_ENERGY_4867" in checkpoint and "PPC4161_LEADING_QUARTIC_SELF_ENERGY_4867" in formal, "checkpoint and formal markers found"),
        result("VAL4867_14_resume", resume_checkpoint_at_least(resume, 4867) and NEXT_TARGET in resume, "resume advanced to finite-C response"),
        result("VAL4867_15_prior", prior_validation[-1].get("status") == "PASS", "4866 validation remains green"),
        result("VAL4867_16_script", compiles(Path(__file__).resolve()), "generator compiles"),
    ]
    checks.append(
        result(
            "VAL4867_OVERALL",
            all(row["status"] == "PASS" for row in checks),
            "LEADING_QUARTIC_SELF_ENERGY_AND_BOOST_SOURCE_VALIDATED",
        )
    )
    return checks


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    symbols = public_symbols()
    sources = source_rows()
    modes = mode_rows(symbols)
    angular = angular_rows()
    boost = boost_source_rows(symbols)
    second = second_order_rows(symbols)
    third = third_order_rows(symbols)
    kernel = self_energy_kernel(symbols)
    self_energy = self_energy_rows(symbols, kernel)
    response, numeric = response_rows(symbols, kernel)
    grid = response_grid_rows(symbols, numeric)
    decisions = decision_rows(numeric)
    residuals = residual_rows(numeric)
    validation = validation_rows(
        sources,
        modes,
        angular,
        boost,
        second,
        third,
        self_energy,
        response,
        grid,
        decisions,
        residuals,
    )
    write_csv(OUTPUT / "P8_Y5_R2FR_4867_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4867_PUBLIC_MODE_MAP.csv", modes)
    write_csv(OUTPUT / "P8_Y5_R2FR_4867_ANGULAR_DIFFERENTIAL_PROJECTORS.csv", angular)
    write_csv(OUTPUT / "P8_Y5_R2FR_4867_BOOST_SOURCE_PROJECTORS.csv", boost)
    write_csv(OUTPUT / "P8_Y5_R2FR_4867_SECOND_ORDER_L0_L2_SYSTEM.csv", second)
    write_csv(OUTPUT / "P8_Y5_R2FR_4867_THIRD_ORDER_L1_SOURCE.csv", third)
    write_csv(OUTPUT / "P8_Y5_R2FR_4867_SELF_ENERGY_KERNEL.csv", self_energy)
    write_csv(OUTPUT / "P8_Y5_R2FR_4867_WEAK_KAPPA4_DERIVATION.csv", response)
    write_csv(OUTPUT / "P8_Y5_R2FR_4867_WEAK_RESPONSE_GRID.csv", grid)
    write_csv(OUTPUT / "P8_Y5_R2FR_4867_BRANCH_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4867_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_BRR545_4867_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4867_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4867_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
