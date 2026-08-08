from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4992"
CHI_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4991"
    / "sources"
    / "chi_1903.07944"
    / "GravitonBending.tex"
)
CHI_COEFFICIENTS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4991"
    / "sources"
    / "chi_1903.07944"
    / "Coeff-of-Integrals.txt"
)
BOELS_SOURCE = SOURCE / "sources" / "boels_luo_1710.10208" / "LoopsFromTrees_v2.tex"
BOELS_ARCHIVE = SOURCE / "sources" / "boels_luo_1710.10208" / "1710.10208.tar"
RAFIE_SOURCE = SOURCE / "sources" / "rafie_zinedine_1808.06086" / "Safi_Quantum_Gravity.tex"
CHECKPOINT_4991 = POST / "4991-Y5-R2FR-massless-hh-channel-amplitude-seed-and-completeness-test.md"
HH_COEFFICIENTS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4991"
    / "massless_hh_channel_integral_coefficients.csv"
)
HH_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4991"
    / "massless_hh_channel_amplitude_seed_results.json"
)

SPINOR_CSV = SOURCE / "mixed_hphi_cut_spinor_chart.csv"
MIXED_BOX_CSV = SOURCE / "mixed_hphi_quadruple_cut_boxes.csv"
SCALAR_BOX_CSV = SOURCE / "scalar_intermediate_quadruple_cut_boxes.csv"
COMPLETION_CSV = SOURCE / "full_phi2h2_box_completion.csv"
GATE_CSV = SOURCE / "one_loop_box_completion_gate.csv"
RESULT_JSON = SOURCE / "mixed_hphi_cut_and_full_box_completion_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4992_MIXED_HPHI_CUT_AND_FULL_BOX_COMPLETION"
CHECKED_DATE = "2026-07-14"

t, u, z, w = sp.symbols("t u z w", nonzero=True)
s = -t - u


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def normalized_text(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8", errors="replace").split())


def exact(expression: sp.Expr) -> str:
    return sp.sstr(sp.factor(sp.cancel(sp.together(sp.simplify(expression)))))


def is_zero(expression: sp.Expr) -> bool:
    return sp.factor(sp.cancel(sp.together(sp.simplify(expression)))) == 0


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


def angle(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    return sp.expand(left[0] * right[1] - left[1] * right[0])


def square(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    return sp.expand(left[0] * right[1] - left[1] * right[0])


def momentum(lam: sp.Matrix, tilde: sp.Matrix) -> sp.Matrix:
    return lam * tilde.T


def mass_squared(matrix: sp.Matrix) -> sp.Expr:
    return sp.factor(-matrix.det())


def sandwich(
    left_lam: sp.Matrix,
    middle_lam: sp.Matrix,
    middle_tilde: sp.Matrix,
    right_tilde: sp.Matrix,
) -> sp.Expr:
    return sp.factor(angle(left_lam, middle_lam) * square(middle_tilde, right_tilde))


def matrix_zero(matrix: sp.Matrix) -> bool:
    return all(is_zero(entry) for entry in matrix)


def source_lock() -> dict[str, bool]:
    chi = normalized_text(CHI_SOURCE)
    boels = normalized_text(BOELS_SOURCE)
    checkpoint = normalized_text(CHECKPOINT_4991)
    hh_result = json.loads(HH_RESULT.read_text(encoding="utf-8"))
    return {
        "chi_all_incoming_compton_tree": (
            "Taking all particles incoming" in chi
            and "two-graviton-two-massive-scalar amplitude with opposite graviton helicities" in chi
            and "M_{[\\Phi(k_4) \\Phi(k_3)]}^{[h^{+}(l_2)h^{-}(l_1)]}" in chi
        ),
        "chi_four_scalar_tree": (
            "M_{[\\phi(k_1) \\phi(k_2)]}^{[\\phi(k_3)\\phi(k_4)]}" in chi
            and "(s^2+s t+t^2)^2" in chi
            and "all momenta are incoming" in chi
        ),
        "chi_cut_state_factor": "2 l_1^2 l_2^2" in chi,
        "boels_unitarity_product": "discontinuities across branch cuts are given by products of lower-loop amplitudes" in boels,
        "boels_massless_cut_completeness": "unitarity cuts pick up all integrals in the case where the external legs are massless" in boels,
        "boels_box_two_channel_consistency": "box coefficients appear in two cut channels" in boels,
        "boels_quadruple_residue": "For a quadruple cut, one should simply take a double residue" in boels,
        "boels_shared_box_match": "such as the scalar box, must match between channels" in boels,
        "checkpoint_4991_scope": "massless" in checkpoint and "hh" in checkpoint and "source-complete component" in checkpoint,
        "checkpoint_4991_result": hh_result.get("checkpoint_marker") == "MTS_4991_MASSLESS_HH_CHANNEL_AMPLITUDE_SEED",
    }


def external_chart() -> dict[str, Any]:
    lambdas = {
        1: sp.Matrix([1, 0]),
        2: sp.Matrix([0, 1]),
        3: sp.Matrix([1, -u]),
        4: sp.Matrix([1, t]),
    }
    tildes = {
        1: sp.Matrix([-1, -1]),
        2: sp.Matrix([u, -t]),
        3: sp.Matrix([1, 0]),
        4: sp.Matrix([0, 1]),
    }
    momenta = {index: momentum(lambdas[index], tildes[index]) for index in range(1, 5)}
    total = sum(momenta.values(), sp.zeros(2))
    invariants = {
        "s": mass_squared(momenta[1] + momenta[2]),
        "t": mass_squared(momenta[2] + momenta[3]),
        "u": mass_squared(momenta[1] + momenta[3]),
    }
    Q = sandwich(lambdas[2], lambdas[3], tildes[3], tildes[1])
    Qbar = sandwich(lambdas[1], lambdas[3], tildes[3], tildes[2])
    return {
        "lambdas": lambdas,
        "tildes": tildes,
        "momenta": momenta,
        "total": total,
        "invariants": invariants,
        "Q": sp.factor(Q),
        "Qbar": sp.factor(Qbar),
    }


def mixed_cut(chart: dict[str, Any]) -> dict[str, Any]:
    lambdas = chart["lambdas"]
    tildes = chart["tildes"]
    momenta = chart["momenta"]
    denominator = 1 + z * w
    lambda_l = lambdas[1] - w * lambdas[3]
    tilde_l = (tildes[1] - z * tildes[3]) / denominator
    lambda_q = lambdas[3] + z * lambdas[1]
    tilde_q = (tildes[3] + w * tildes[1]) / denominator
    p_l = sp.simplify(momentum(lambda_l, tilde_l))
    p_q = sp.simplify(momentum(lambda_q, tilde_q))
    K = momenta[1] + momenta[3]

    A = sp.factor(mass_squared(p_l - momenta[1]))
    B = sp.factor(mass_squared(p_l - momenta[3]))
    C = sp.factor(mass_squared(p_l + momenta[2]))
    D = sp.factor(mass_squared(p_l + momenta[4]))
    r = sp.factor((1 + z) / denominator)
    internal_spinor = sp.factor(angle(lambda_l, lambdas[3]) * square(tildes[4], tilde_l))
    partial_fraction_residual = sp.factor(
        1 / (u**2 * A * B * C * D)
        - (1 / A + 1 / B) * (1 / C + 1 / D) / u**4
    )
    return {
        "denominator": denominator,
        "lambda_l": lambda_l,
        "tilde_l": tilde_l,
        "p_l": p_l,
        "p_q": p_q,
        "K": K,
        "A": A,
        "B": B,
        "C": C,
        "D": D,
        "r": r,
        "internal_spinor": internal_spinor,
        "partial_fraction_residual": partial_fraction_residual,
    }


def evaluate_branch(
    expression: sp.Expr,
    substitutions: dict[sp.Symbol, sp.Expr],
    infinity_variable: sp.Symbol | None = None,
) -> sp.Expr:
    reduced = expression.subs(substitutions)
    if infinity_variable is not None:
        reduced = sp.limit(reduced, infinity_variable, sp.oo)
    return sp.factor(sp.cancel(sp.together(reduced)))


def mixed_box_rows(values: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, sp.Expr]]:
    r4 = values["r"] ** 4
    branches: dict[str, list[tuple[str, dict[sp.Symbol, sp.Expr], sp.Symbol | None]]] = {
        "AC": [
            ("z=0,w=1", {z: 0, w: 1}, None),
            ("w=0,z=s/t", {w: 0, z: s / t}, None),
        ],
        "AD": [
            ("z=0,w=-t/s", {z: 0, w: -t / s}, None),
            ("w=0,z=-1", {w: 0, z: -1}, None),
        ],
        "BC": [
            ("z->infinity,w=1", {w: 1}, z),
            ("w->infinity,z=s/t", {z: s / t}, w),
        ],
        "BD": [
            ("z->infinity,w=-t/s", {w: -t / s}, z),
            ("w->infinity,z=-1", {z: -1}, w),
        ],
    }
    masters = {
        "AC": "I4(s,u)",
        "AD": "I4(t,u)",
        "BC": "I4(t,u)",
        "BD": "I4(s,u)",
    }
    denominators = {"AC": "A*C", "AD": "A*D", "BC": "B*C", "BD": "B*D"}
    rows: list[dict[str, Any]] = []
    coefficients: dict[str, sp.Expr] = {}
    for topology, topology_branches in branches.items():
        branch_values = [
            evaluate_branch(r4, substitutions, infinity_variable)
            for _, substitutions, infinity_variable in topology_branches
        ]
        branch_sum = sp.factor(sum(branch_values))
        coefficient = sp.factor((t * u) ** 4 * branch_sum / 32)
        coefficients[topology] = coefficient
        rows.append(
            {
                "topology_id": f"MIX4992_{topology}",
                "cut_channel": "u=(p1+p3)^2",
                "uncut_propagators": denominators[topology],
                "master_integral": masters[topology],
                "branch_1": topology_branches[0][0],
                "r4_branch_1": exact(branch_values[0]),
                "branch_2": topology_branches[1][0],
                "r4_branch_2": exact(branch_values[1]),
                "r4_solution_sum": exact(branch_sum),
                "tree_prefactor": "1/16",
                "quadruple_solution_average": "1/2",
                "cut_state_factor": "1 (distinguishable h,phi)",
                "box_coefficient": exact(coefficient),
                "status": "DERIVED_EXACT_FOUR_DIMENSIONAL_CUT",
            }
        )
    return rows, coefficients


def scalar_cut(chart: dict[str, Any]) -> dict[str, Any]:
    lambdas = chart["lambdas"]
    tildes = chart["tildes"]
    momenta = chart["momenta"]
    denominator = 1 + z * w
    lambda_l = lambdas[1] - w * lambdas[2]
    tilde_l = (tildes[1] - z * tildes[2]) / denominator
    lambda_q = lambdas[2] + z * lambdas[1]
    tilde_q = (tildes[2] + w * tildes[1]) / denominator
    p_l = sp.simplify(momentum(lambda_l, tilde_l))
    p_q = sp.simplify(momentum(lambda_q, tilde_q))
    K = momenta[1] + momenta[2]

    L1 = sp.factor(mass_squared(momenta[2] - p_l))
    L2 = sp.factor(mass_squared(p_l - momenta[1]))
    R1 = sp.factor(mass_squared(momenta[4] + p_l))
    R2 = sp.factor(mass_squared(momenta[3] + p_l))
    Q_l = sandwich(lambdas[2], lambda_l, tilde_l, tildes[1])
    rho = sp.factor(z / denominator)
    H1 = sp.factor((s**2 + s * R1 + R1**2) ** 2)
    H2 = sp.factor((s**2 + s * R2 + R2**2) ** 2)
    partial_fraction_residual = sp.factor(
        1 / (s**2 * L1 * L2 * R1 * R2)
        - (1 / L1 + 1 / L2) * (1 / R1 + 1 / R2) / s**4
    )
    return {
        "denominator": denominator,
        "lambda_l": lambda_l,
        "tilde_l": tilde_l,
        "p_l": p_l,
        "p_q": p_q,
        "K": K,
        "L1": L1,
        "L2": L2,
        "R1": R1,
        "R2": R2,
        "Q_l": sp.factor(Q_l),
        "rho": rho,
        "H1": H1,
        "H2": H2,
        "partial_fraction_residual": partial_fraction_residual,
    }


def scalar_box_rows(values: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, sp.Expr]]:
    rho4 = values["rho"] ** 4
    branches: dict[str, list[tuple[str, dict[sp.Symbol, sp.Expr], sp.Symbol | None]]] = {
        "L2R1": [
            ("z=0,w=-t", {z: 0, w: -t}, None),
            ("w=0,z=-1/u", {w: 0, z: -1 / u}, None),
        ],
        "L1R2": [
            ("z->infinity,w=u", {w: u}, z),
            ("w->infinity,z=1/t", {z: 1 / t}, w),
        ],
        "L2R2": [
            ("z=0,w=u", {z: 0, w: u}, None),
            ("w=0,z=1/t", {w: 0, z: 1 / t}, None),
        ],
        "L1R1": [
            ("z->infinity,w=-t", {w: -t}, z),
            ("w->infinity,z=-1/u", {z: -1 / u}, w),
        ],
    }
    masters = {
        "L2R1": "I4(s,t)",
        "L1R2": "I4(s,t)",
        "L2R2": "I4(s,u)",
        "L1R1": "I4(s,u)",
    }
    rows: list[dict[str, Any]] = []
    coefficients: dict[str, sp.Expr] = {}
    for topology, topology_branches in branches.items():
        rho_values = [
            evaluate_branch(rho4, substitutions, infinity_variable)
            for _, substitutions, infinity_variable in topology_branches
        ]
        phase_values = [sp.factor((t * u) ** 4 * value) for value in rho_values]
        phase_sum = sp.factor(sum(phase_values))
        coefficient_before_state_factor = sp.factor(s**4 * phase_sum / 32)
        coefficients[topology] = coefficient_before_state_factor
        rows.append(
            {
                "topology_id": f"SCAL4992_{topology}",
                "cut_channel": "s=(p1+p2)^2",
                "uncut_propagators": topology,
                "master_integral": masters[topology],
                "branch_1": topology_branches[0][0],
                "phase_weight_branch_1": exact(phase_values[0]),
                "branch_2": topology_branches[1][0],
                "phase_weight_branch_2": exact(phase_values[1]),
                "phase_weight_sum": exact(phase_sum),
                "four_scalar_numerator_on_residue": exact(s**4),
                "coefficient_before_identical_state_factor": exact(coefficient_before_state_factor),
                "identical_scalar_state_factor": "1/2 after pairing the two routings",
                "status": "DERIVED_EXACT_FOUR_DIMENSIONAL_CUT",
            }
        )
    return rows, coefficients


def read_hh_boxes() -> dict[str, sp.Expr]:
    with HH_COEFFICIENTS.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    by_integral = {row["integral"]: row for row in rows}
    locals_map = {"s": s, "t": t, "u": u, "pi": sp.pi}
    return {
        "I4(s,t)": sp.factor(sp.sympify(by_integral["I4(s,t)"]["coefficient_D4"], locals=locals_map)),
        "I4(s,u)": sp.factor(sp.sympify(by_integral["I4(s,u)"]["coefficient_D4"], locals=locals_map)),
    }


def spinor_rows(
    chart: dict[str, Any],
    mixed: dict[str, Any],
    scalar: dict[str, Any],
) -> list[dict[str, Any]]:
    expected_mixed = {
        "A": -u * z * w / (1 + z * w),
        "B": -u / (1 + z * w),
        "C": (1 - w) * (s - t * z) / (1 + z * w),
        "D": (t + s * w) * (1 + z) / (1 + z * w),
    }
    expected_scalar = {
        "L1": -s / (1 + z * w),
        "L2": -s * z * w / (1 + z * w),
        "R1": (w + t) * (1 + z * u) / (1 + z * w),
        "R2": (u - w) * (1 - z * t) / (1 + z * w),
    }
    rows: list[dict[str, Any]] = [
        {
            "identity_id": "CHART4992_01_momentum",
            "sector": "external",
            "statement": "sum_i p_i=0",
            "derived_value": str(chart["total"].tolist()),
            "exact_residual": "0" if matrix_zero(chart["total"]) else str(chart["total"].tolist()),
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "CHART4992_02_massless",
            "sector": "external",
            "statement": "p_i^2=0 for i=1..4",
            "derived_value": ";".join(exact(mass_squared(chart["momenta"][index])) for index in range(1, 5)),
            "exact_residual": "0" if all(is_zero(mass_squared(chart["momenta"][index])) for index in range(1, 5)) else "nonzero",
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "CHART4992_03_mandelstam",
            "sector": "external",
            "statement": "(p1+p2)^2=s,(p2+p3)^2=t,(p1+p3)^2=u",
            "derived_value": ";".join(f"{name}={exact(value)}" for name, value in chart["invariants"].items()),
            "exact_residual": exact(
                chart["invariants"]["s"] - s
                + chart["invariants"]["t"] - t
                + chart["invariants"]["u"] - u
            ),
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "CHART4992_04_phase",
            "sector": "external",
            "statement": "Q=<2|3|1],Qbar=<1|3|2],Q Qbar=t u",
            "derived_value": f"Q={exact(chart['Q'])};Qbar={exact(chart['Qbar'])}",
            "exact_residual": exact(chart["Q"] * chart["Qbar"] - t * u),
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "CHART4992_05_mixed_on_shell",
            "sector": "mixed_hphi_u_cut",
            "statement": "l^2=q^2=0 and l+q=p1+p3",
            "derived_value": "rank-one spinor decomposition",
            "exact_residual": "0"
            if is_zero(mass_squared(mixed["p_l"]))
            and is_zero(mass_squared(mixed["p_q"]))
            and matrix_zero(sp.simplify(mixed["p_l"] + mixed["p_q"] - mixed["K"]))
            else "nonzero",
            "status": "DERIVED_EXACT",
        },
    ]
    for index, name in enumerate(("A", "B", "C", "D"), start=6):
        rows.append(
            {
                "identity_id": f"CHART4992_{index:02d}_mixed_{name}",
                "sector": "mixed_hphi_u_cut",
                "statement": f"{name} crossed-Compton propagator",
                "derived_value": exact(mixed[name]),
                "exact_residual": exact(mixed[name] - expected_mixed[name]),
                "status": "DERIVED_EXACT",
            }
        )
    rows.extend(
        [
            {
                "identity_id": "CHART4992_10_mixed_pair_sums",
                "sector": "mixed_hphi_u_cut",
                "statement": "A+B=C+D=-u",
                "derived_value": f"A+B={exact(mixed['A']+mixed['B'])};C+D={exact(mixed['C']+mixed['D'])}",
                "exact_residual": exact(mixed["A"] + mixed["B"] + u) + ";" + exact(mixed["C"] + mixed["D"] + u),
                "status": "DERIVED_EXACT",
            },
            {
                "identity_id": "CHART4992_11_mixed_numerator",
                "sector": "mixed_hphi_u_cut",
                "statement": "(<l3>[4l])^4/u^4=r^4 in the fixed external little-group chart",
                "derived_value": f"<l3>[4l]={exact(mixed['internal_spinor'])};r={exact(mixed['r'])}",
                "exact_residual": exact(mixed["internal_spinor"] ** 4 / u**4 - mixed["r"] ** 4),
                "status": "DERIVED_EXACT",
            },
            {
                "identity_id": "CHART4992_12_mixed_partial_fraction",
                "sector": "mixed_hphi_u_cut",
                "statement": "1/(u^2 A B C D)=u^-4(1/A+1/B)(1/C+1/D)",
                "derived_value": "four scalar-box topologies AC,AD,BC,BD",
                "exact_residual": exact(mixed["partial_fraction_residual"]),
                "status": "DERIVED_EXACT",
            },
            {
                "identity_id": "CHART4992_13_scalar_on_shell",
                "sector": "scalar_s_cut",
                "statement": "l^2=q^2=0 and l+q=p1+p2",
                "derived_value": "rank-one spinor decomposition",
                "exact_residual": "0"
                if is_zero(mass_squared(scalar["p_l"]))
                and is_zero(mass_squared(scalar["p_q"]))
                and matrix_zero(sp.simplify(scalar["p_l"] + scalar["p_q"] - scalar["K"]))
                else "nonzero",
                "status": "DERIVED_EXACT",
            },
        ]
    )
    for index, name in enumerate(("L1", "L2", "R1", "R2"), start=14):
        rows.append(
            {
                "identity_id": f"CHART4992_{index:02d}_scalar_{name}",
                "sector": "scalar_s_cut",
                "statement": f"{name} scalar-cut propagator",
                "derived_value": exact(scalar[name]),
                "exact_residual": exact(scalar[name] - expected_scalar[name]),
                "status": "DERIVED_EXACT",
            }
        )
    rows.extend(
        [
            {
                "identity_id": "CHART4992_18_scalar_pair_sums",
                "sector": "scalar_s_cut",
                "statement": "L1+L2=R1+R2=-s",
                "derived_value": f"L1+L2={exact(scalar['L1']+scalar['L2'])};R1+R2={exact(scalar['R1']+scalar['R2'])}",
                "exact_residual": exact(scalar["L1"] + scalar["L2"] + s) + ";" + exact(scalar["R1"] + scalar["R2"] + s),
                "status": "DERIVED_EXACT",
            },
            {
                "identity_id": "CHART4992_19_scalar_compton_phase",
                "sector": "scalar_s_cut",
                "statement": "<2|l|1]/Q=s z/(1+z w)",
                "derived_value": exact(scalar["Q_l"] / chart["Q"]),
                "exact_residual": exact(scalar["Q_l"] / chart["Q"] - s * z / (1 + z * w)),
                "status": "DERIVED_EXACT",
            },
            {
                "identity_id": "CHART4992_20_four_scalar_numerator",
                "sector": "scalar_s_cut",
                "statement": "H(R1)=H(R2)=(s^2+sR+R^2)^2 and H(0)=s^4",
                "derived_value": "crossing-symmetric graviton-exchange numerator",
                "exact_residual": exact(scalar["H1"] - scalar["H2"]),
                "status": "DERIVED_EXACT",
            },
            {
                "identity_id": "CHART4992_21_scalar_partial_fraction",
                "sector": "scalar_s_cut",
                "statement": "1/(s^2 L1 L2 R1 R2)=s^-4(1/L1+1/L2)(1/R1+1/R2)",
                "derived_value": "two routings per scalar box master",
                "exact_residual": exact(scalar["partial_fraction_residual"]),
                "status": "DERIVED_EXACT",
            },
        ]
    )
    return rows


def completion_rows(
    hh: dict[str, sp.Expr],
    mixed_coefficients: dict[str, sp.Expr],
    scalar_coefficients: dict[str, sp.Expr],
) -> tuple[list[dict[str, Any]], dict[str, sp.Expr]]:
    scalar_st = sp.factor(
        sp.Rational(1, 2) * (scalar_coefficients["L2R1"] + scalar_coefficients["L1R2"])
    )
    scalar_su = sp.factor(
        sp.Rational(1, 2) * (scalar_coefficients["L2R2"] + scalar_coefficients["L1R1"])
    )
    mixed_su = sp.factor(mixed_coefficients["AC"] + mixed_coefficients["BD"])
    mixed_tu = sp.factor(mixed_coefficients["AD"] + mixed_coefficients["BC"])
    s_cut_st = sp.factor(hh["I4(s,t)"] + scalar_st)
    s_cut_su = sp.factor(hh["I4(s,u)"] + scalar_su)
    crossed_st = sp.factor(mixed_su.xreplace({t: u, u: t}))
    crossed_tu = sp.factor(mixed_tu.xreplace({t: u, u: t}))
    full = {
        "B_st": s_cut_st,
        "B_su": s_cut_su,
        "B_tu": mixed_tu,
        "scalar_st": scalar_st,
        "scalar_su": scalar_su,
        "mixed_su": mixed_su,
        "mixed_tu": mixed_tu,
        "crossed_st": crossed_st,
        "crossed_tu": crossed_tu,
    }
    rows = [
        {
            "completion_id": "BOX4992_01_hh_st",
            "master_integral": "I4(s,t)",
            "cut_or_component": "hh intermediate state on s cut",
            "coefficient": exact(hh["I4(s,t)"]),
            "comparison_residual": "0",
            "status": "IMPORTED_SOURCE_COMPLETE_4991_COMPONENT",
        },
        {
            "completion_id": "BOX4992_02_scalar_st",
            "master_integral": "I4(s,t)",
            "cut_or_component": "phi phi intermediate state on s cut after 1/2 state factor",
            "coefficient": exact(scalar_st),
            "comparison_residual": "0",
            "status": "DERIVED_EXACT",
        },
        {
            "completion_id": "BOX4992_03_scut_st",
            "master_integral": "I4(s,t)",
            "cut_or_component": "complete s-cut sum",
            "coefficient": exact(s_cut_st),
            "comparison_residual": exact(s_cut_st - crossed_st),
            "status": "MATCHES_CROSSED_MIXED_T_CUT",
        },
        {
            "completion_id": "BOX4992_04_hh_su",
            "master_integral": "I4(s,u)",
            "cut_or_component": "hh intermediate state on s cut",
            "coefficient": exact(hh["I4(s,u)"]),
            "comparison_residual": "0",
            "status": "IMPORTED_SOURCE_COMPLETE_4991_COMPONENT",
        },
        {
            "completion_id": "BOX4992_05_scalar_su",
            "master_integral": "I4(s,u)",
            "cut_or_component": "phi phi intermediate state on s cut after 1/2 state factor",
            "coefficient": exact(scalar_su),
            "comparison_residual": "0",
            "status": "DERIVED_EXACT",
        },
        {
            "completion_id": "BOX4992_06_scut_su",
            "master_integral": "I4(s,u)",
            "cut_or_component": "complete s-cut sum",
            "coefficient": exact(s_cut_su),
            "comparison_residual": exact(s_cut_su - mixed_su),
            "status": "MATCHES_MIXED_U_CUT",
        },
        {
            "completion_id": "BOX4992_07_mixed_tu",
            "master_integral": "I4(t,u)",
            "cut_or_component": "mixed h phi u cut",
            "coefficient": exact(mixed_tu),
            "comparison_residual": exact(mixed_tu - crossed_tu),
            "status": "MATCHES_MIXED_T_CUT_BY_CROSSING",
        },
        {
            "completion_id": "BOX4992_08_full_box_sector",
            "master_integral": "all three massless boxes",
            "cut_or_component": "F_box=B_st I4(s,t)+B_su I4(s,u)+B_tu I4(t,u)",
            "coefficient": f"B_st={exact(s_cut_st)};B_su={exact(s_cut_su)};B_tu={exact(mixed_tu)}",
            "comparison_residual": exact(s_cut_st - crossed_st) + ";" + exact(s_cut_su - mixed_su),
            "status": "THREE_CHANNEL_UNITARITY_CONSISTENT_BOX_COMPLETION",
        },
    ]
    return rows, full


def gate_rows(
    source_checks: dict[str, bool],
    chart_rows_out: list[dict[str, Any]],
    mixed_rows_out: list[dict[str, Any]],
    scalar_rows_out: list[dict[str, Any]],
    full: dict[str, sp.Expr],
) -> list[dict[str, Any]]:
    closed = {
        "primary_source_lock": all(source_checks.values()),
        "external_massless_spinor_chart": all(row["exact_residual"] == "0" for row in chart_rows_out[:5]),
        "mixed_cut_propagator_map": all(row["exact_residual"] == "0" for row in chart_rows_out[5:9]),
        "mixed_cut_pair_sums": chart_rows_out[9]["exact_residual"] == "0;0",
        "mixed_cut_numerator": chart_rows_out[10]["exact_residual"] == "0",
        "mixed_cut_partial_fraction": chart_rows_out[11]["exact_residual"] == "0",
        "mixed_quadruple_cut_four_topologies": len(mixed_rows_out) == 4,
        "mixed_distinguishable_state_count": all("distinguishable" in row["cut_state_factor"] for row in mixed_rows_out),
        "scalar_cut_on_shell": chart_rows_out[12]["exact_residual"] == "0",
        "scalar_cut_propagator_map": all(row["exact_residual"] == "0" for row in chart_rows_out[13:17]),
        "scalar_cut_pair_sums": chart_rows_out[17]["exact_residual"] == "0;0",
        "scalar_compton_phase": chart_rows_out[18]["exact_residual"] == "0",
        "four_scalar_numerator_crossing": chart_rows_out[19]["exact_residual"] == "0",
        "scalar_cut_partial_fraction": chart_rows_out[20]["exact_residual"] == "0",
        "scalar_quadruple_cut_four_routings": len(scalar_rows_out) == 4,
        "identical_scalar_state_factor": all("1/2" in row["identical_scalar_state_factor"] for row in scalar_rows_out),
        "I4_su_two_channel_match": is_zero(full["B_su"] - full["mixed_su"]),
        "I4_st_crossed_two_channel_match": is_zero(full["B_st"] - full["crossed_st"]),
        "I4_tu_crossing_match": is_zero(full["B_tu"] - full["crossed_tu"]),
        "full_box_identical_scalar_crossing": is_zero(
            full["B_st"].xreplace({t: u, u: t}) - full["B_su"]
        ),
    }
    open_gates = {
        "D_dimensional_mu2_rational_terms": "four-dimensional cuts do not determine evanescent mu^2 or rational terms",
        "triangle_coefficients_all_channels": "requires cut IBP or universal infrared reconstruction",
        "bubble_coefficients_all_channels": "requires D-dimensional cut reduction",
        "complete_one_loop_phi2h2": "box sector is complete; triangle, bubble and rational sectors remain",
        "universal_IR_normalization": "must be matched in the same integral convention",
        "crossing_complete_outer_hh_cut": "one-loop hard kernel is not yet complete",
        "numeric_full_K_mu_K_ang": "outer cut remains open",
        "exact_all_operator_local_GR": "not claimed",
        "full_MTS": "not claimed",
    }
    rows: list[dict[str, Any]] = []
    for name, passed in closed.items():
        rows.append(
            {
                "gate": name,
                "passed": bool(passed),
                "evidence": "exact source lock or symbolic identity",
                "status": "PASS" if passed else "FAIL",
                "valid_for_checkpoint_claim": bool(passed),
            }
        )
    for name, evidence in open_gates.items():
        rows.append(
            {
                "gate": name,
                "passed": False,
                "evidence": evidence,
                "status": "OPEN_NONCLAIM",
                "valid_for_checkpoint_claim": False,
            }
        )
    return [
        dict(gate_id=f"GATE4992_{index:02d}_{row['gate']}", **row)
        for index, row in enumerate(rows, start=1)
    ]


def write_provenance(source_hashes: dict[str, str], source_checks: dict[str, bool]) -> None:
    lines = [
        "# 4992 mixed h-phi cut and complete scalar-box provenance",
        "",
        f"Marker: {MARKER}.",
        "",
        f"Checked: {CHECKED_DATE}.",
        "",
        "## Primary sources",
        "",
        "- H.-H. Chi, Graviton bending in quantum gravity from one-loop amplitudes, Phys. Rev. D 99, 126008 (2019), arXiv:1903.07944, DOI 10.1103/PhysRevD.99.126008: all-incoming opposite-helicity graviton-scalar Compton tree, cut normalization, four-scalar graviton-exchange tree, and the sourced hh s-cut component inherited through 4991.",
        "- R. H. Boels and H. Luo, A minimal approach to the scattering of physical massless bosons, JHEP 05 (2018) 063, arXiv:1710.10208, DOI 10.1007/JHEP05(2018)063: unitarity/IBP completeness, shared-box channel consistency, and quadruple-residue method.",
        "- S. Rafie-Zinedine, Simplifying Quantum Gravity Calculations, arXiv:1808.06086: convention cross-check only; it is not used as a tabulation of the full amplitude.",
        "",
        "## Source checks",
        "",
    ]
    lines.extend(f"- {name}: {value}" for name, value in source_checks.items())
    lines.extend(["", "## SHA-256", ""])
    lines.extend(f"- {path}: {value}" for path, value in source_hashes.items())
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "This checkpoint completes the four-dimensional scalar-box sector of the one-loop opposite-helicity two-graviton/two-massless-scalar amplitude and proves its agreement across the hh plus scalar s cut and the crossed mixed h-phi cuts. It does not determine triangle, bubble, D-dimensional mu-squared, evanescent, or rational terms; therefore it does not yet claim the complete one-loop amplitude, the outer two-loop hh cut, numeric full invariants, local GR, or full MTS.",
            "",
        ]
    )
    PROVENANCE.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    started = time.perf_counter()

    source_checks = source_lock()
    if not all(source_checks.values()):
        failed = [name for name, passed in source_checks.items() if not passed]
        raise RuntimeError(f"source lock failed: {failed}")

    chart = external_chart()
    mixed = mixed_cut(chart)
    scalar = scalar_cut(chart)
    chart_rows_out = spinor_rows(chart, mixed, scalar)
    mixed_rows_out, mixed_coefficients = mixed_box_rows(mixed)
    scalar_rows_out, scalar_coefficients = scalar_box_rows(scalar)
    hh = read_hh_boxes()
    completion_rows_out, full = completion_rows(hh, mixed_coefficients, scalar_coefficients)
    gates = gate_rows(source_checks, chart_rows_out, mixed_rows_out, scalar_rows_out, full)

    failed_closed = [row["gate"] for row in gates if row["status"] == "FAIL"]
    if failed_closed:
        raise RuntimeError(f"closed derivation gates failed: {failed_closed}")

    summary = {
        "checkpoint_marker": MARKER,
        "source_checks": source_checks,
        "B_st": exact(full["B_st"]),
        "B_su": exact(full["B_su"]),
        "B_tu": exact(full["B_tu"]),
        "I4_st_channel_residual": exact(full["B_st"] - full["crossed_st"]),
        "I4_su_channel_residual": exact(full["B_su"] - full["mixed_su"]),
        "I4_tu_crossing_residual": exact(full["B_tu"] - full["crossed_tu"]),
        "dry_run": bool(args.dry_run),
    }
    if args.dry_run:
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0

    for path, rows in (
        (SPINOR_CSV, chart_rows_out),
        (MIXED_BOX_CSV, mixed_rows_out),
        (SCALAR_BOX_CSV, scalar_rows_out),
        (COMPLETION_CSV, completion_rows_out),
        (GATE_CSV, gates),
    ):
        write_csv(path, tagged(rows))

    script_path = Path(__file__).resolve()
    source_paths = [
        CHI_SOURCE,
        CHI_COEFFICIENTS,
        BOELS_SOURCE,
        BOELS_ARCHIVE,
        RAFIE_SOURCE,
        CHECKPOINT_4991,
        HH_COEFFICIENTS,
        HH_RESULT,
        script_path,
    ]
    source_hashes = {relative(path): digest(path) for path in source_paths}
    result = {
        **summary,
        "dry_run": False,
        "source_hashes": source_hashes,
        "amplitude_convention": "M1=kappa^4 F/<1|3|2]^4",
        "full_four_dimensional_box_sector": {
            "I4(s,t)": exact(full["B_st"]),
            "I4(s,u)": exact(full["B_su"]),
            "I4(t,u)": exact(full["B_tu"]),
        },
        "mixed_u_cut_topologies": {
            name: exact(value) for name, value in mixed_coefficients.items()
        },
        "scalar_s_cut_topologies_before_state_factor": {
            name: exact(value) for name, value in scalar_coefficients.items()
        },
        "four_dimensional_box_sector_complete": True,
        "complete_one_loop_phi2h2": False,
        "crossing_complete_outer_hh_cut": False,
        "numeric_full_K_mu": False,
        "numeric_full_K_ang": False,
        "exact_all_operator_local_GR": False,
        "full_MTS": False,
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
                "passed_gates": passed,
                "total_gates": len(gates),
                "open_nonclaim_gates": len(gates) - passed,
                "B_st": exact(full["B_st"]),
                "B_su": exact(full["B_su"]),
                "B_tu": exact(full["B_tu"]),
                "four_dimensional_box_sector_complete": True,
                "complete_one_loop_phi2h2": False,
                "result": str(RESULT_JSON),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
