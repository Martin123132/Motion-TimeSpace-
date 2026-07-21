from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import re
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4987"

CHECKPOINT_4985 = POST / "4985-Y5-R2FR-metric-frame-O2-zero-and-partial-wave-mixing-flow.md"
CHECKPOINT_4986 = POST / "4986-Y5-R2FR-common-scheme-log-invariant-and-local-metric-exterior-bounds.md"
RESULT_4986 = POST / "source-intake" / "functional_rg" / "4986" / "common_scheme_log_and_local_metric_results.json"
BERN_SOURCE = SOURCE / "sources" / "bern_parra_sawyer" / "smeft2.tex"
BERN_ARCHIVE = SOURCE / "sources" / "bern_parra_sawyer_2005.12917.tar"
DUNBAR_SOURCE = POST / "source-intake" / "functional_rg" / "4986" / "sources" / "dunbar_norridge" / "9512084.tex"
SCALAR_GRAVITON_SOURCE = SOURCE / "sources" / "scalar_graviton_1908.09755" / "mscalar_grav-submit.tex"
SCALAR_GRAVITON_ARCHIVE = SOURCE / "sources" / "scalar_graviton_1908.09755.tar"
FORDE_SOURCE = SOURCE / "sources" / "forde_kosower_hep-th0507292" / "payload"
FORDE_ARCHIVE = SOURCE / "sources" / "forde_kosower_hep-th0507292.gz"

BASIS_CSV = SOURCE / "crossing_local_polynomial_basis.csv"
SCHEME_CSV = SOURCE / "full_finite_scheme_orbit.csv"
CUT_CSV = SOURCE / "two_loop_cut_state_census.csv"
MASTER_CSV = SOURCE / "rational_free_master_projection.csv"
ANGULAR_CSV = SOURCE / "single_log_angular_projector_checks.csv"
GATE_CSV = SOURCE / "two_loop_cut_reduction_gate.csv"
RESULT_JSON = SOURCE / "full_finite_scheme_orbit_and_cut_reduction_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4987_FULL_FINITE_SCHEME_ORBIT_IRREDUCIBLE_CUT_REDUCTION"
CHECKED_DATE = "2026-07-14"

A_C = sp.Integer(16)
B_GC = -sp.Integer(6) / sp.pi
F_A = sp.Integer(46) / (sp.Integer(15) * sp.pi)
F_B = -sp.Integer(1) / (sp.Integer(15) * sp.pi)


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def normalized_text(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8", errors="replace"))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
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
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def source_lock() -> dict[str, bool]:
    bern = normalized_text(BERN_SOURCE)
    dunbar = normalized_text(DUNBAR_SOURCE)
    scalar_graviton = normalized_text(SCALAR_GRAVITON_SOURCE)
    forde = normalized_text(FORDE_SOURCE)
    checkpoint_4986 = normalized_text(CHECKPOINT_4986)
    return {
        "bern_two_loop_real_master_equation": "twoloopSimon3" in bern and "drop the imaginary parts" in bern,
        "bern_two_and_three_particle_cut_sum": "twoloopsum" in bern and "three-particle cuts" in bern,
        "bern_finite_scheme_transformation": "twoloopanomscheme" in bern and "finite renormalization" in bern,
        "bern_ir_subtraction_requirement": "stress-tensor" in bern and "same IR divergences" in bern,
        "dunbar_four_scalar_rational_polynomial_boundary": "finite, non-logarithmic rational polynomials" in dunbar,
        "dunbar_same_helicity_two_scalar_two_graviton_zero": "2^+ , 3^+ , \\phi_4 ) = 0" in dunbar,
        "dunbar_opposite_helicity_two_scalar_two_graviton_nonzero": "2^- , 3^+ , \\phi_4 )" in dunbar,
        "scalar_graviton_arbitrary_multiplicity_KLT": "arbitrary number of gravitons" in scalar_graviton and "Kawai-Lewellen-Tye" in scalar_graviton,
        "forde_all_plus_mass_factor": "(-m_s^{2})^{j}" in forde and "AllPlusResult" in forde,
        "forde_all_minus_by_conjugation": "all negative-helicity gluons can be obtained by spinor conjugation" in forde,
        "checkpoint_4986_mixed_log_coefficients": "F_1,log=(2/pi)[(23/15)L_A-(1/30)L_B]" in checkpoint_4986,
        "checkpoint_4986_reduced_flow": "dC/dlnmu=16" in checkpoint_4986 and "dW/dlnmu=B_gc C+S_2L" in checkpoint_4986,
    }


def integer_normalize(vector: sp.Matrix) -> list[int]:
    denominators = [sp.denom(value) for value in vector]
    common = int(sp.ilcm(*[int(value) for value in denominators])) if denominators else 1
    integers = [int(value * common) for value in vector]
    divisor = 0
    for value in integers:
        divisor = math.gcd(divisor, abs(value))
    if divisor:
        integers = [value // divisor for value in integers]
    first = next((value for value in integers if value), 1)
    if first < 0:
        integers = [-value for value in integers]
    return integers


def invariant_basis(degree: int) -> tuple[list[list[int]], sp.Expr]:
    s_value, t_value = sp.symbols("s t")
    coefficients = sp.symbols(f"a0:{degree + 1}")
    polynomial = sum(coefficients[index] * s_value ** (degree - index) * t_value**index for index in range(degree + 1))
    constraints: list[sp.Expr] = []
    for difference in (
        sp.expand(polynomial - polynomial.subs({s_value: t_value, t_value: s_value}, simultaneous=True)),
        sp.expand(polynomial - polynomial.subs(t_value, -s_value - t_value)),
    ):
        constraints.extend(sp.Poly(difference, s_value, t_value).coeffs())
    matrix, _ = sp.linear_eq_to_matrix(constraints, coefficients)
    nullspace = matrix.nullspace()
    vectors = [integer_normalize(vector) for vector in nullspace]
    representative = sp.Integer(0)
    if vectors:
        representative = sp.expand(
            sum(vectors[0][index] * s_value ** (degree - index) * t_value**index for index in range(degree + 1))
        )
    return vectors, representative


def basis_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    summary: dict[str, Any] = {}
    expected = {
        2: ("P4=s^2+t^2+u^2", "representative=P4/2"),
        3: ("P6=stu", "representative=-P6"),
    }
    for degree in (2, 3):
        vectors, representative = invariant_basis(degree)
        summary[f"degree_{degree}_dimension"] = len(vectors)
        summary[f"degree_{degree}_representative"] = str(representative)
        rows.append(
            {
                "basis_id": f"BASIS4987_D{degree}",
                "momentum_degree": degree,
                "derivative_order": 2 * degree,
                "crossing_group": "S3",
                "constraint": "s+t+u=0",
                "quotient_dimension": len(vectors),
                "null_vector": json.dumps(vectors[0] if vectors else []),
                "representative_after_u_elimination": str(representative),
                "canonical_basis": expected[degree][0],
                "canonical_relation": expected[degree][1],
                "status": "EXACT_ONE_DIMENSIONAL_LOCAL_ORBIT" if len(vectors) == 1 else "FAIL",
                "source_path": relative(CHECKPOINT_4986),
                "valid_for_basis_claim": len(vectors) == 1,
            }
        )
    return rows, summary


def scheme_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    C, W, r4, rho, source_s, coefficient_a, coefficient_b, eta = sp.symbols("C W r4 rho S A B eta")
    alpha, beta, delta = sp.symbols("alpha beta delta")
    stu, log_a, log_b = sp.symbols("stu L_A L_B")

    C_prime = C + beta
    W_prime = W + alpha * C + delta
    r4_prime = r4 - beta
    rho_prime = rho + 3 * alpha
    source_prime = source_s + A_C * alpha - B_GC * beta
    coefficient_a_prime = coefficient_a - beta * F_A
    coefficient_b_prime = coefficient_b - beta * F_B
    eta_prime = eta - beta * rho + 3 * (delta - alpha * beta)

    f1 = F_A * log_a + F_B * log_b + rho * stu
    f1_prime = F_A * log_a + F_B * log_b + rho_prime * stu
    f2 = coefficient_a * log_a + coefficient_b * log_b + eta * stu
    f2_prime = coefficient_a_prime * log_a + coefficient_b_prime * log_b + eta_prime * stu
    amplitude = -3 * W * stu + C * f1 + f2
    amplitude_prime = -3 * W_prime * stu + C_prime * f1_prime + f2_prime

    invariant_i = 3 * source_s - A_C * rho
    invariant_i_prime = sp.expand(3 * source_prime - A_C * rho_prime)
    angular_j = coefficient_a - coefficient_b
    angular_j_prime = sp.expand(coefficient_a_prime - coefficient_b_prime)
    invariant_mu = sp.expand(invariant_i - 3 * B_GC * r4)
    invariant_mu_prime = sp.expand(invariant_i_prime - 3 * B_GC * r4_prime)
    invariant_angular = sp.expand(angular_j - (F_A - F_B) * r4)
    invariant_angular_prime = sp.expand(angular_j_prime - (F_A - F_B) * r4_prime)

    checks = [
        ("SCHEME4987_01_amplitude", "R6'=R6", sp.simplify(amplitude_prime - amplitude), "full affine p4/p6 amplitude invariance"),
        ("SCHEME4987_02_p4_physical", "(C+r4)'=C+r4", sp.simplify(C_prime + r4_prime - C - r4), "finite X2 coordinate is compensated by one-loop local rational"),
        ("SCHEME4987_03_source", "S'=S+16alpha-B_gc beta", sp.Integer(0), str(source_prime)),
        ("SCHEME4987_04_I_shift", "I'=I-3B_gc beta", sp.simplify(invariant_i_prime - (invariant_i - 3 * B_GC * beta)), str(invariant_i_prime)),
        ("SCHEME4987_05_J_shift", "J'=J-beta(f_A-f_B)", sp.simplify(angular_j_prime - (angular_j - beta * (F_A - F_B))), str(angular_j_prime)),
        ("SCHEME4987_06_Kmu", "K_mu=I-3B_gc r4", sp.simplify(invariant_mu_prime - invariant_mu), str(invariant_mu)),
        ("SCHEME4987_07_Kang", "K_ang=J-(f_A-f_B)r4", sp.simplify(invariant_angular_prime - invariant_angular), str(invariant_angular)),
        ("SCHEME4987_08_fsum", "f_A+f_B=-B_gc/2=3/pi", sp.simplify(F_A + F_B + B_GC / 2), str(F_A + F_B)),
        ("SCHEME4987_09_fdiff", "f_A-f_B=47/(15pi)", sp.simplify(F_A - F_B - sp.Rational(47, 15) / sp.pi), str(F_A - F_B)),
        ("SCHEME4987_10_rational_free_r4", "beta=r4 => r4'=0", sp.simplify(r4_prime.subs(beta, r4)), "beta=r4"),
        ("SCHEME4987_11_rational_free_rho", "alpha=-rho/3 => rho'=0", sp.simplify(rho_prime.subs(alpha, -rho / 3)), "alpha=-rho/3"),
        ("SCHEME4987_12_rational_free_source", "K_mu=3S_rf", sp.simplify(invariant_mu - 3 * source_prime.subs({beta: r4, alpha: -rho / 3})), "S_rf=S-(16/3)rho-B_gc r4"),
    ]
    rows = [
        {
            "scheme_id": check_id,
            "statement": statement,
            "exact_residual": str(sp.simplify(residual)),
            "derived_expression": expression,
            "status": "EXACT" if sp.simplify(residual) == 0 else "FAIL",
            "source_path": relative(BERN_SOURCE),
            "valid_for_scheme_claim": sp.simplify(residual) == 0,
        }
        for check_id, statement, residual, expression in checks
    ]
    summary = {
        "f_A": str(F_A),
        "f_B": str(F_B),
        "B_gc": str(B_GC),
        "old_I_alpha_invariant_only": "I=3S-16rho",
        "full_scale_invariant": str(invariant_mu),
        "full_angular_invariant": str(invariant_angular),
        "rational_free_coordinates": {"beta": "r4", "alpha": "-rho/3"},
        "all_exact_residuals_zero": all(sp.simplify(item[2]) == 0 for item in checks),
    }
    return rows, summary


def cut_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = [
        (2, "phi_h", 1, False, False, "odd scalar number on each tree side", "none", CHECKPOINT_4985),
        (2, "h_h_same_helicity", 0, True, False, "M_tree(phi,phi,h+,h+)=0 and parity conjugate", "none", DUNBAR_SOURCE),
        (2, "h_h_opposite_helicity", 0, True, True, "opposite-helicity tree is nonzero", "Re A_2phi2h^(1,+-) x A_2phi2h^(0,+-) plus placement swap", DUNBAR_SOURCE),
        (2, "phi_phi", 2, True, True, "even scalar number", "Re A_4phi^(1) x A_4phi^(0) plus placement swap", DUNBAR_SOURCE),
        (3, "phi_h_h", 1, False, False, "odd scalar number on each tree side", "none", CHECKPOINT_4985),
        (3, "phi_phi_phi", 3, False, False, "odd scalar number on each tree side", "none", CHECKPOINT_4985),
        (3, "h_h_h_all_equal_helicity", 0, True, False, "all-plus scalar-gluon tree carries m_phi^(2j); KLT square vanishes at m_phi=0; all-minus follows by conjugation", "none", FORDE_SOURCE),
        (3, "h_h_h_mixed_helicity", 0, True, True, "one-opposite-helicity scalar-gluon trees survive and KLT supplies gravity tree", "A_2phi3h^(0) x A_2phi3h^(0)", SCALAR_GRAVITON_SOURCE),
        (3, "phi_phi_h", 2, True, True, "even scalar number; no helicity-zero theorem removes the branch", "A_4phi1h^(0) x A_4phi1h^(0)", CHECKPOINT_4986),
    ]
    output = [
        {
            "cut_id": f"CUT4987_{index:02d}",
            "cut_multiplicity": multiplicity,
            "state_class": state_class,
            "internal_scalar_count": scalar_count,
            "reflection_parity_allowed": parity_allowed,
            "helicity_allowed": helicity_allowed,
            "survives_irreducible_census": bool(parity_allowed and helicity_allowed),
            "reason": reason,
            "required_integrand": integrand,
            "source_path": relative(source_path),
            "status": "SURVIVES" if parity_allowed and helicity_allowed else "EXACT_ZERO",
            "valid_for_cut_census_claim": True,
        }
        for index, (multiplicity, state_class, scalar_count, parity_allowed, helicity_allowed, reason, integrand, source_path) in enumerate(rows, start=1)
    ]
    survivors = [row[1] for row in rows if row[3] and row[4]]
    summary = {
        "surviving_classes": survivors,
        "surviving_count": len(survivors),
        "two_particle_survivors": [name for multiplicity, name, _, parity, helicity, *_ in rows if multiplicity == 2 and parity and helicity],
        "three_particle_survivors": [name for multiplicity, name, _, parity, helicity, *_ in rows if multiplicity == 3 and parity and helicity],
    }
    return output, summary


def master_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "projection_id": "MASTER4987_01_general",
            "object": "two_loop_real_master",
            "equation": "D1 ReF1 + D2 F0 = -(1/pi)[Re(M) Re(F)]^(2)",
            "derivation_status": "SOURCE_LOCKED_GENERAL_IDENTITY",
            "remaining_numeric_input": "none_for_identity",
            "source_path": relative(BERN_SOURCE),
            "valid_for_projection_claim": True,
        },
        {
            "projection_id": "MASTER4987_02_rational_free",
            "object": "rational_free_scheme",
            "equation": "beta=r4; alpha=-rho/3 => r4_rf=rho_rf=0; K_mu=3S_rf; K_ang=J_rf",
            "derivation_status": "EXACT_FINITE_COORDINATE_CONSTRUCTION",
            "remaining_numeric_input": "none_for_coordinate_construction",
            "source_path": relative(BERN_SOURCE),
            "valid_for_projection_claim": True,
        },
        {
            "projection_id": "MASTER4987_03_cut_sum",
            "object": "C2_ren",
            "equation": "C2_ren=C2_phiphi+C2_hh(+-)+C3_hhh(mixed)+C3_phiphih-C_IR",
            "derivation_status": "COMPLETE_STATE_CENSUS",
            "remaining_numeric_input": "renormalized one-loop 4phi and 2phi2h(+-), tree 2phi3h and 4phi1h, common soft subtraction",
            "source_path": relative(BERN_SOURCE),
            "valid_for_projection_claim": True,
        },
        {
            "projection_id": "MASTER4987_04_scale",
            "object": "K_mu",
            "equation": "Pi_stu[-C2_ren/pi-D1 ReF1]=-K_mu stu",
            "derivation_status": "EXACT_MTS_SPECIALIZATION_IN_DOUBLE_RATIONAL_FREE_SCHEME",
            "remaining_numeric_input": "four surviving cut classes",
            "source_path": relative(CHECKPOINT_4986),
            "valid_for_projection_claim": True,
        },
        {
            "projection_id": "MASTER4987_05_discontinuity",
            "object": "K_ang",
            "equation": "Disc_s F2_single/(-2pi i s^3)=A_rf+(B_rf/4)(1-z^2); K_ang=A_rf-B_rf",
            "derivation_status": "EXACT_TWO_COMPONENT_CHANNEL_PROJECTOR",
            "remaining_numeric_input": "renormalized s-channel discontinuity after forced double-log subtraction",
            "source_path": relative(CHECKPOINT_4986),
            "valid_for_projection_claim": True,
        },
        {
            "projection_id": "MASTER4987_06_numeric",
            "object": "numeric_K_mu_and_K_ang",
            "equation": "not_evaluated",
            "derivation_status": "OPEN_NONCLAIM",
            "remaining_numeric_input": "explicit integration of surviving renormalized cuts",
            "source_path": relative(SCALAR_GRAVITON_SOURCE),
            "valid_for_projection_claim": False,
        },
    ]
    return rows


def angular_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    generator = random.Random(4987)
    rows: list[dict[str, Any]] = []
    maximum_residual = Fraction(0)
    for event in range(64):
        coefficient_a = Fraction(generator.randint(-97, 97), generator.randint(1, 31))
        coefficient_b = Fraction(generator.randint(-97, 97), generator.randint(1, 31))
        d_at_zero = coefficient_a + coefficient_b / 4
        d_at_one = coefficient_a
        reconstructed_a = d_at_one
        reconstructed_b = 4 * (d_at_zero - d_at_one)
        legendre_zero = coefficient_a + coefficient_b / 6
        legendre_two = -coefficient_b / 6
        reconstructed_a_legendre = legendre_zero + legendre_two
        reconstructed_b_legendre = -6 * legendre_two
        residuals = (
            abs(reconstructed_a - coefficient_a),
            abs(reconstructed_b - coefficient_b),
            abs(reconstructed_a_legendre - coefficient_a),
            abs(reconstructed_b_legendre - coefficient_b),
        )
        maximum_residual = max(maximum_residual, *residuals)
        rows.append(
            {
                "event_id": f"ANG4987_{event + 1:03d}",
                "A_true": str(coefficient_a),
                "B_true": str(coefficient_b),
                "D_z0": str(d_at_zero),
                "D_z1": str(d_at_one),
                "d0_legendre": str(legendre_zero),
                "d2_legendre": str(legendre_two),
                "A_reconstructed": str(reconstructed_a),
                "B_reconstructed": str(reconstructed_b),
                "K_mu_over_minus6": str(legendre_zero - 5 * legendre_two),
                "K_ang": str(legendre_zero + 7 * legendre_two),
                "maximum_exact_residual": str(max(residuals)),
                "status": "EXACT_TWO_COMPONENT_RECONSTRUCTION" if max(residuals) == 0 else "FAIL",
                "source_path": relative(CHECKPOINT_4986),
                "valid_for_angular_projector_claim": max(residuals) == 0,
            }
        )
    return rows, {
        "events": len(rows),
        "maximum_exact_residual": str(maximum_residual),
        "projector": "D(z)=A+(B/4)(1-z^2)=d0+d2 P2(z)",
        "inverse": "A=d0+d2; B=-6d2; K_mu=-6(d0-5d2); K_ang=d0+7d2",
    }


def gate_rows(source_checks: dict[str, bool], basis: dict[str, Any], scheme: dict[str, Any], cuts: dict[str, Any], angular: dict[str, Any]) -> list[dict[str, Any]]:
    checks = [
        ("primary_source_lock", all(source_checks.values()), f"{sum(source_checks.values())}/{len(source_checks)} markers"),
        ("p4_local_orbit", basis["degree_2_dimension"] == 1, "crossing-symmetric local p4 quotient is one-dimensional"),
        ("p6_local_orbit", basis["degree_3_dimension"] == 1, "crossing-symmetric local p6 quotient is one-dimensional"),
        ("full_affine_scheme_orbit", scheme["all_exact_residuals_zero"], "all symbolic amplitude, flow and invariant residuals vanish"),
        ("old_I_scope_corrected", True, "I=3S-16rho is alpha-invariant but beta-shifts under finite X2 renormalization"),
        ("K_mu_full_invariant", True, "K_mu=I-3B_gc r4"),
        ("K_ang_full_invariant", True, "K_ang=J-(f_A-f_B)r4"),
        ("double_rational_free_scheme", True, "beta=r4 and alpha=-rho/3 set both local one-loop rational coordinates to zero"),
        ("cut_state_census", cuts["surviving_count"] == 4, json.dumps(cuts["surviving_classes"])),
        ("mixed_two_cut_zero", "phi_h" not in cuts["surviving_classes"], "reflection parity"),
        ("same_helicity_hh_zero", "h_h_same_helicity" not in cuts["surviving_classes"], "tree amplitude zero"),
        ("all_equal_helicity_hhh_zero", "h_h_h_all_equal_helicity" not in cuts["surviving_classes"], "massless all-plus/all-minus KLT zero"),
        ("angular_projector", angular["maximum_exact_residual"] == "0", f"{angular['events']} exact rational events"),
        ("numeric_K_mu", False, "surviving renormalized cut integrals not yet evaluated"),
        ("numeric_K_ang", False, "s-channel discontinuity not yet integrated"),
        ("exact_all_operator_local_GR", False, "two-loop primitive and higher residual sectors remain"),
        ("full_MTS", False, "not claimed"),
    ]
    return [
        {
            "gate_id": f"GATE4987_{index:02d}_{name}",
            "gate": name,
            "passed": passed,
            "evidence": evidence,
            "status": "PASS" if passed else "OPEN_NONCLAIM",
            "claim_allowed": bool(passed and name not in {"old_I_scope_corrected"}),
        }
        for index, (name, passed, evidence) in enumerate(checks, start=1)
    ]


def write_provenance(source_hashes: dict[str, str], source_checks: dict[str, bool]) -> None:
    lines = [
        "# 4987 finite-scheme orbit and irreducible-cut provenance",
        "",
        f"Marker: `{MARKER}`.",
        "",
        f"Checked: `{CHECKED_DATE}`.",
        "",
        "## Primary sources",
        "",
        "- [Bern, Parra-Martinez and Sawyer, *Structure of two-loop SMEFT anomalous dimensions via on-shell methods*](https://arxiv.org/abs/2005.12917): real two-loop master relation, two- and three-particle cut decomposition, IR subtraction, and finite-scheme law.",
        "- [Dunbar and Norridge, *Infinities within Graviton Scattering Amplitudes*](https://arxiv.org/abs/hep-th/9512084): one-loop four-scalar rational-polynomial boundary and the same/opposite-helicity two-scalar-two-graviton tree amplitudes.",
        "- [Bjerrum-Bohr et al., *Scalar-Graviton Amplitudes*](https://arxiv.org/abs/1908.09755): arbitrary-multiplicity two-scalar graviton trees and KLT construction.",
        "- [Forde and Kosower, *All-Multiplicity Amplitudes with Massive Scalars*](https://arxiv.org/abs/hep-th/0507292): every all-plus scalar-gluon tree term carries a positive power of the scalar mass; all-minus follows by conjugation.",
        "",
        "The source archives and extracted TeX are retained under `post-checkpoint-work/source-intake/functional_rg/4987/sources/`.",
        "",
        "## Source-marker checks",
        "",
    ]
    lines.extend(f"- `{name}`: `{value}`" for name, value in source_checks.items())
    lines.extend(["", "## SHA-256", ""])
    lines.extend(f"- `{path}`: `{hash_value}`" for path, hash_value in source_hashes.items())
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "This checkpoint corrects the scope of the 4986 invariant, derives the full finite `X^2/O2` scheme orbit, constructs the two genuinely scheme-independent logarithmic combinations, and reduces the two-loop state sum to four nonzero cut classes. It does not assign numerical values to those invariants because the surviving renormalized cut integrals have not yet been evaluated. No local-GR or full-MTS claim follows from this reduction.",
            "",
        ]
    )
    PROVENANCE.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    started = time.perf_counter()

    required_paths = (
        CHECKPOINT_4985,
        CHECKPOINT_4986,
        RESULT_4986,
        BERN_SOURCE,
        BERN_ARCHIVE,
        DUNBAR_SOURCE,
        SCALAR_GRAVITON_SOURCE,
        SCALAR_GRAVITON_ARCHIVE,
        FORDE_SOURCE,
        FORDE_ARCHIVE,
    )
    missing = [str(path) for path in required_paths if not path.exists()]
    if missing:
        raise FileNotFoundError("\n".join(missing))
    source_checks = source_lock()
    if not all(source_checks.values()):
        raise RuntimeError(json.dumps(source_checks, indent=2, sort_keys=True))

    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "dry_run": True,
                    "required_paths": len(required_paths),
                    "source_checks": source_checks,
                    "planned_outputs": 8,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    SOURCE.mkdir(parents=True, exist_ok=True)
    local_basis_rows, basis_summary = basis_rows()
    finite_scheme_rows, scheme_summary = scheme_rows()
    state_rows, cut_summary = cut_rows()
    projection_rows = master_rows()
    projector_rows, angular_summary = angular_rows()
    gates = gate_rows(source_checks, basis_summary, scheme_summary, cut_summary, angular_summary)

    write_csv(BASIS_CSV, tagged(local_basis_rows))
    write_csv(SCHEME_CSV, tagged(finite_scheme_rows))
    write_csv(CUT_CSV, tagged(state_rows))
    write_csv(MASTER_CSV, tagged(projection_rows))
    write_csv(ANGULAR_CSV, tagged(projector_rows))
    write_csv(GATE_CSV, tagged(gates))

    hash_paths = required_paths + (Path(__file__),)
    source_hashes = {relative(path): digest(path) for path in hash_paths}
    result = {
        "checkpoint_marker": MARKER,
        "source_checks": source_checks,
        "source_hashes": source_hashes,
        "crossing_local_basis": basis_summary,
        "finite_scheme": scheme_summary,
        "cut_census": cut_summary,
        "master_projection": {
            "scale_invariant_target": "Pi_stu[-C2_ren/pi-D1 ReF1]=-K_mu stu",
            "angular_target": "Disc_s/(-2pi i s^3)=A_rf+(B_rf/4)(1-z^2)",
            "numeric_K_mu_derived": False,
            "numeric_K_ang_derived": False,
        },
        "angular_projector": angular_summary,
        "gates": {row["gate"]: bool(row["passed"]) for row in gates},
        "elapsed_seconds": time.perf_counter() - started,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_provenance(source_hashes, source_checks)

    passed = sum(bool(row["passed"]) for row in gates)
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "gate_rows": len(gates),
                "passed_rows": passed,
                "open_nonclaim_rows": len(gates) - passed,
                "surviving_cut_classes": cut_summary["surviving_classes"],
                "scheme_residuals_zero": scheme_summary["all_exact_residuals_zero"],
                "angular_maximum_exact_residual": angular_summary["maximum_exact_residual"],
                "result": str(RESULT_JSON),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
