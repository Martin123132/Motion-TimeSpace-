from __future__ import annotations

import csv
import hashlib
import json
import random
import sys
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
BOELS_SOURCE = SOURCE / "sources" / "boels_luo_1710.10208" / "LoopsFromTrees_v2.tex"
HH_COEFFICIENTS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4991"
    / "massless_hh_channel_integral_coefficients.csv"
)
SPINOR_CSV = SOURCE / "mixed_hphi_cut_spinor_chart.csv"
MIXED_BOX_CSV = SOURCE / "mixed_hphi_quadruple_cut_boxes.csv"
SCALAR_BOX_CSV = SOURCE / "scalar_intermediate_quadruple_cut_boxes.csv"
COMPLETION_CSV = SOURCE / "full_phi2h2_box_completion.csv"
GATE_CSV = SOURCE / "one_loop_box_completion_gate.csv"
RESULT_JSON = SOURCE / "mixed_hphi_cut_and_full_box_completion_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4992_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

MARKER = "MTS_4992_MIXED_HPHI_CUT_AND_FULL_BOX_COMPLETION"
VALIDATION_MARKER = "P8_Y5_BRR545_4992_VALIDATION"

t, u, z, w = sp.symbols("t u z w", nonzero=True)
s = -t - u


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def parse(expression: str) -> sp.Expr:
    return sp.sympify(expression, locals={"s": s, "t": t, "u": u, "z": z, "w": w, "pi": sp.pi})


def zero(expression: sp.Expr) -> bool:
    return sp.factor(sp.cancel(sp.together(sp.simplify(expression)))) == 0


def add(checks: list[dict[str, Any]], check_id: str, passed: bool, evidence: str) -> None:
    checks.append(
        {
            "validation_id": f"VAL4992_{len(checks) + 1:04d}_{check_id}",
            "check": check_id,
            "passed": bool(passed),
            "evidence": evidence,
            "validation_marker": VALIDATION_MARKER,
        }
    )


def bracket(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    return sp.expand(left[0] * right[1] - left[1] * right[0])


def momentum(lam: sp.Matrix, tilde: sp.Matrix) -> sp.Matrix:
    return lam * tilde.T


def mass_squared(matrix: sp.Matrix) -> sp.Expr:
    return sp.factor(-matrix.det())


def matrix_zero(matrix: sp.Matrix) -> bool:
    return all(zero(entry) for entry in matrix)


def branch(
    expression: sp.Expr,
    substitutions: dict[sp.Symbol, sp.Expr],
    infinity_variable: sp.Symbol | None = None,
) -> sp.Expr:
    value = expression.subs(substitutions)
    if infinity_variable is not None:
        value = sp.limit(value, infinity_variable, sp.oo)
    return sp.factor(sp.cancel(sp.together(value)))


def write_validation(rows: list[dict[str, Any]]) -> None:
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    checks: list[dict[str, Any]] = []
    required_files = [
        CHI_SOURCE,
        BOELS_SOURCE,
        HH_COEFFICIENTS,
        SPINOR_CSV,
        MIXED_BOX_CSV,
        SCALAR_BOX_CSV,
        COMPLETION_CSV,
        GATE_CSV,
        RESULT_JSON,
        PROVENANCE,
    ]
    for path in required_files:
        add(checks, f"file_exists_{path.stem}", path.exists(), str(path))
        add(
            checks,
            f"file_nonempty_{path.stem}",
            path.exists() and path.stat().st_size > 0,
            str(path.stat().st_size if path.exists() else 0),
        )

    spinor_rows = read_csv(SPINOR_CSV)
    mixed_rows = read_csv(MIXED_BOX_CSV)
    scalar_rows = read_csv(SCALAR_BOX_CSV)
    completion_rows = read_csv(COMPLETION_CSV)
    gate_rows = read_csv(GATE_CSV)
    result = json.loads(RESULT_JSON.read_text(encoding="utf-8"))
    tables = {
        "spinor": (spinor_rows, 21),
        "mixed": (mixed_rows, 4),
        "scalar": (scalar_rows, 4),
        "completion": (completion_rows, 8),
        "gate": (gate_rows, 29),
    }
    for name, (rows, expected_count) in tables.items():
        add(checks, f"row_count_{name}", len(rows) == expected_count, str(len(rows)))
        add(checks, f"csv_shape_{name}", all(None not in row for row in rows), "no surplus columns")
        add(checks, f"marker_{name}", all(row["checkpoint_marker"] == MARKER for row in rows), MARKER)
        add(
            checks,
            f"full_MTS_false_{name}",
            all(not truth(row["valid_for_full_MTS_claim"]) for row in rows),
            "all rows guarded",
        )
        joined = "\n".join(str(value) for row in rows for value in row.values())
        add(checks, f"no_missing_marker_{name}", "MISSING_" not in joined, "no placeholders")

    add(checks, "result_marker", result["checkpoint_marker"] == MARKER, result["checkpoint_marker"])
    add(checks, "result_box_complete", truth(result["four_dimensional_box_sector_complete"]), "4D box sector")
    for key in (
        "complete_one_loop_phi2h2",
        "crossing_complete_outer_hh_cut",
        "numeric_full_K_mu",
        "numeric_full_K_ang",
        "exact_all_operator_local_GR",
        "full_MTS",
    ):
        add(checks, f"result_nonclaim_{key}", not truth(result[key]), str(result[key]))

    for source_path, expected_hash in result["source_hashes"].items():
        path = ROOT / source_path
        add(checks, f"source_exists_{len(checks)}", path.exists(), source_path)
        if path.exists():
            add(checks, f"source_hash_{len(checks)}", digest(path) == expected_hash, source_path)

    chi = " ".join(CHI_SOURCE.read_text(encoding="utf-8", errors="replace").split())
    boels = " ".join(BOELS_SOURCE.read_text(encoding="utf-8", errors="replace").split())
    source_markers = {
        "chi_compton": "Taking all particles incoming" in chi and "opposite graviton helicities" in chi,
        "chi_compton_formula": "M_{[\\Phi(k_4) \\Phi(k_3)]}^{[h^{+}(l_2)h^{-}(l_1)]}" in chi,
        "chi_scalar_formula": "(s^2+s t+t^2)^2" in chi,
        "boels_unitarity": "discontinuities across branch cuts are given by products of lower-loop amplitudes" in boels,
        "boels_quadruple": "For a quadruple cut, one should simply take a double residue" in boels,
        "boels_channel_match": "such as the scalar box, must match between channels" in boels,
    }
    for name, passed in source_markers.items():
        add(checks, f"independent_source_{name}", passed, name)

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
    Q = bracket(lambdas[2], lambdas[3]) * bracket(tildes[3], tildes[1])
    Qbar = bracket(lambdas[1], lambdas[3]) * bracket(tildes[3], tildes[2])
    chart_checks = {
        "momentum": matrix_zero(total),
        "massless": all(zero(mass_squared(momenta[index])) for index in range(1, 5)),
        "s": zero(mass_squared(momenta[1] + momenta[2]) - s),
        "t": zero(mass_squared(momenta[2] + momenta[3]) - t),
        "u": zero(mass_squared(momenta[1] + momenta[3]) - u),
        "Q": zero(Q - 1),
        "Qbar": zero(Qbar - t * u),
        "phase": zero(Q * Qbar - t * u),
    }
    for name, passed in chart_checks.items():
        add(checks, f"independent_chart_{name}", passed, name)

    denominator = 1 + z * w
    lambda_l_mixed = lambdas[1] - w * lambdas[3]
    tilde_l_mixed = (tildes[1] - z * tildes[3]) / denominator
    lambda_q_mixed = lambdas[3] + z * lambdas[1]
    tilde_q_mixed = (tildes[3] + w * tildes[1]) / denominator
    p_l_mixed = momentum(lambda_l_mixed, tilde_l_mixed)
    p_q_mixed = momentum(lambda_q_mixed, tilde_q_mixed)
    mixed_expected = {
        "A": -u * z * w / denominator,
        "B": -u / denominator,
        "C": (1 - w) * (s - t * z) / denominator,
        "D": (t + s * w) * (1 + z) / denominator,
    }
    mixed_derived = {
        "A": mass_squared(p_l_mixed - momenta[1]),
        "B": mass_squared(p_l_mixed - momenta[3]),
        "C": mass_squared(p_l_mixed + momenta[2]),
        "D": mass_squared(p_l_mixed + momenta[4]),
    }
    add(checks, "mixed_l_massless", zero(mass_squared(p_l_mixed)), str(mass_squared(p_l_mixed)))
    add(checks, "mixed_q_massless", zero(mass_squared(p_q_mixed)), str(mass_squared(p_q_mixed)))
    add(
        checks,
        "mixed_cut_sum",
        matrix_zero(sp.simplify(p_l_mixed + p_q_mixed - momenta[1] - momenta[3])),
        "l+q=p1+p3",
    )
    for name in mixed_expected:
        add(
            checks,
            f"mixed_propagator_{name}",
            zero(mixed_derived[name] - mixed_expected[name]),
            sp.sstr(sp.factor(mixed_derived[name])),
        )
    A, B, C, D = (mixed_derived[name] for name in ("A", "B", "C", "D"))
    add(checks, "mixed_AB_sum", zero(A + B + u), sp.sstr(sp.factor(A + B)))
    add(checks, "mixed_CD_sum", zero(C + D + u), sp.sstr(sp.factor(C + D)))
    mixed_pf = 1 / (u**2 * A * B * C * D) - (1 / A + 1 / B) * (1 / C + 1 / D) / u**4
    add(checks, "mixed_partial_fraction", zero(mixed_pf), sp.sstr(sp.factor(mixed_pf)))
    internal_spinor = bracket(lambda_l_mixed, lambdas[3]) * bracket(tildes[4], tilde_l_mixed)
    r = (1 + z) / denominator
    add(checks, "mixed_numerator", zero(internal_spinor**4 / u**4 - r**4), sp.sstr(sp.factor(internal_spinor)))

    mixed_branches = {
        "MIX4992_AC": [
            branch(r**4, {z: 0, w: 1}),
            branch(r**4, {w: 0, z: s / t}),
        ],
        "MIX4992_AD": [
            branch(r**4, {z: 0, w: -t / s}),
            branch(r**4, {w: 0, z: -1}),
        ],
        "MIX4992_BC": [
            branch(r**4, {w: 1}, z),
            branch(r**4, {z: s / t}, w),
        ],
        "MIX4992_BD": [
            branch(r**4, {w: -t / s}, z),
            branch(r**4, {z: -1}, w),
        ],
    }
    expected_mixed_coefficients = {
        topology_id: sp.factor((t * u) ** 4 * sum(values) / 32)
        for topology_id, values in mixed_branches.items()
    }
    mixed_by_id = {row["topology_id"]: row for row in mixed_rows}
    for topology_id, values in mixed_branches.items():
        row = mixed_by_id[topology_id]
        add(checks, f"{topology_id}_branch_1", zero(parse(row["r4_branch_1"]) - values[0]), row["r4_branch_1"])
        add(checks, f"{topology_id}_branch_2", zero(parse(row["r4_branch_2"]) - values[1]), row["r4_branch_2"])
        add(
            checks,
            f"{topology_id}_coefficient",
            zero(parse(row["box_coefficient"]) - expected_mixed_coefficients[topology_id]),
            row["box_coefficient"],
        )
        add(checks, f"{topology_id}_state_count", "distinguishable" in row["cut_state_factor"], row["cut_state_factor"])

    lambda_l_scalar = lambdas[1] - w * lambdas[2]
    tilde_l_scalar = (tildes[1] - z * tildes[2]) / denominator
    lambda_q_scalar = lambdas[2] + z * lambdas[1]
    tilde_q_scalar = (tildes[2] + w * tildes[1]) / denominator
    p_l_scalar = momentum(lambda_l_scalar, tilde_l_scalar)
    p_q_scalar = momentum(lambda_q_scalar, tilde_q_scalar)
    scalar_expected = {
        "L1": -s / denominator,
        "L2": -s * z * w / denominator,
        "R1": (w + t) * (1 + z * u) / denominator,
        "R2": (u - w) * (1 - z * t) / denominator,
    }
    scalar_derived = {
        "L1": mass_squared(momenta[2] - p_l_scalar),
        "L2": mass_squared(p_l_scalar - momenta[1]),
        "R1": mass_squared(momenta[4] + p_l_scalar),
        "R2": mass_squared(momenta[3] + p_l_scalar),
    }
    add(checks, "scalar_l_massless", zero(mass_squared(p_l_scalar)), str(mass_squared(p_l_scalar)))
    add(checks, "scalar_q_massless", zero(mass_squared(p_q_scalar)), str(mass_squared(p_q_scalar)))
    add(
        checks,
        "scalar_cut_sum",
        matrix_zero(sp.simplify(p_l_scalar + p_q_scalar - momenta[1] - momenta[2])),
        "l+q=p1+p2",
    )
    for name in scalar_expected:
        add(
            checks,
            f"scalar_propagator_{name}",
            zero(scalar_derived[name] - scalar_expected[name]),
            sp.sstr(sp.factor(scalar_derived[name])),
        )
    L1, L2, R1, R2 = (scalar_derived[name] for name in ("L1", "L2", "R1", "R2"))
    add(checks, "scalar_L_sum", zero(L1 + L2 + s), sp.sstr(sp.factor(L1 + L2)))
    add(checks, "scalar_R_sum", zero(R1 + R2 + s), sp.sstr(sp.factor(R1 + R2)))
    scalar_pf = 1 / (s**2 * L1 * L2 * R1 * R2) - (1 / L1 + 1 / L2) * (1 / R1 + 1 / R2) / s**4
    add(checks, "scalar_partial_fraction", zero(scalar_pf), sp.sstr(sp.factor(scalar_pf)))
    Q_l = bracket(lambdas[2], lambda_l_scalar) * bracket(tilde_l_scalar, tildes[1])
    rho = z / denominator
    add(checks, "scalar_phase", zero(Q_l / Q - s * rho), sp.sstr(sp.factor(Q_l / Q)))
    H1 = (s**2 + s * R1 + R1**2) ** 2
    H2 = (s**2 + s * R2 + R2**2) ** 2
    add(checks, "scalar_H_crossing", zero(H1 - H2), sp.sstr(sp.factor(H1 - H2)))

    scalar_branches = {
        "SCAL4992_L2R1": [
            (t * u) ** 4 * branch(rho**4, {z: 0, w: -t}),
            (t * u) ** 4 * branch(rho**4, {w: 0, z: -1 / u}),
        ],
        "SCAL4992_L1R2": [
            (t * u) ** 4 * branch(rho**4, {w: u}, z),
            (t * u) ** 4 * branch(rho**4, {z: 1 / t}, w),
        ],
        "SCAL4992_L2R2": [
            (t * u) ** 4 * branch(rho**4, {z: 0, w: u}),
            (t * u) ** 4 * branch(rho**4, {w: 0, z: 1 / t}),
        ],
        "SCAL4992_L1R1": [
            (t * u) ** 4 * branch(rho**4, {w: -t}, z),
            (t * u) ** 4 * branch(rho**4, {z: -1 / u}, w),
        ],
    }
    expected_scalar_coefficients = {
        topology_id: sp.factor(s**4 * sum(values) / 32)
        for topology_id, values in scalar_branches.items()
    }
    scalar_by_id = {row["topology_id"]: row for row in scalar_rows}
    for topology_id, values in scalar_branches.items():
        row = scalar_by_id[topology_id]
        add(
            checks,
            f"{topology_id}_branch_1",
            zero(parse(row["phase_weight_branch_1"]) - values[0]),
            row["phase_weight_branch_1"],
        )
        add(
            checks,
            f"{topology_id}_branch_2",
            zero(parse(row["phase_weight_branch_2"]) - values[1]),
            row["phase_weight_branch_2"],
        )
        add(
            checks,
            f"{topology_id}_coefficient",
            zero(parse(row["coefficient_before_identical_state_factor"]) - expected_scalar_coefficients[topology_id]),
            row["coefficient_before_identical_state_factor"],
        )
        add(checks, f"{topology_id}_state_factor", "1/2" in row["identical_scalar_state_factor"], row["identical_scalar_state_factor"])

    hh_rows = read_csv(HH_COEFFICIENTS)
    hh_by_integral = {row["integral"]: parse(row["coefficient_D4"]) for row in hh_rows}
    expected_hh_st = t**4 * (t**4 + u**4) / 32
    expected_hh_su = u**4 * (t**4 + u**4) / 32
    add(checks, "hh_st_source", zero(hh_by_integral["I4(s,t)"] - expected_hh_st), sp.sstr(hh_by_integral["I4(s,t)"]))
    add(checks, "hh_su_source", zero(hh_by_integral["I4(s,u)"] - expected_hh_su), sp.sstr(hh_by_integral["I4(s,u)"]))

    scalar_st = sp.Rational(1, 2) * (
        expected_scalar_coefficients["SCAL4992_L2R1"]
        + expected_scalar_coefficients["SCAL4992_L1R2"]
    )
    scalar_su = sp.Rational(1, 2) * (
        expected_scalar_coefficients["SCAL4992_L2R2"]
        + expected_scalar_coefficients["SCAL4992_L1R1"]
    )
    mixed_su = expected_mixed_coefficients["MIX4992_AC"] + expected_mixed_coefficients["MIX4992_BD"]
    mixed_tu = expected_mixed_coefficients["MIX4992_AD"] + expected_mixed_coefficients["MIX4992_BC"]
    B_st = sp.factor(expected_hh_st + scalar_st)
    B_su = sp.factor(expected_hh_su + scalar_su)
    B_tu = sp.factor(mixed_tu)
    expected_boxes = {
        "I4(s,t)": t**4 * (s**4 + t**4 + u**4) / 32,
        "I4(s,u)": u**4 * (s**4 + t**4 + u**4) / 32,
        "I4(t,u)": t**4 * u**4 / 16,
    }
    add(checks, "full_Bst", zero(B_st - expected_boxes["I4(s,t)"]), sp.sstr(B_st))
    add(checks, "full_Bsu", zero(B_su - expected_boxes["I4(s,u)"]), sp.sstr(B_su))
    add(checks, "full_Btu", zero(B_tu - expected_boxes["I4(t,u)"]), sp.sstr(B_tu))
    add(checks, "shared_su_match", zero(B_su - mixed_su), sp.sstr(B_su - mixed_su))
    add(checks, "crossed_st_match", zero(B_st - mixed_su.xreplace({t: u, u: t})), sp.sstr(B_st))
    add(checks, "identical_scalar_crossing", zero(B_st.xreplace({t: u, u: t}) - B_su), "t<->u")

    completion_by_id = {row["completion_id"]: row for row in completion_rows}
    recorded_boxes = {
        "BOX4992_03_scut_st": B_st,
        "BOX4992_06_scut_su": B_su,
        "BOX4992_07_mixed_tu": B_tu,
    }
    for row_id, expected in recorded_boxes.items():
        add(
            checks,
            f"recorded_{row_id}",
            zero(parse(completion_by_id[row_id]["coefficient"]) - expected),
            completion_by_id[row_id]["coefficient"],
        )
    for integral, expected in expected_boxes.items():
        add(
            checks,
            f"result_{integral}",
            zero(parse(result["full_four_dimensional_box_sector"][integral]) - expected),
            result["full_four_dimensional_box_sector"][integral],
        )

    passed_gates = [row for row in gate_rows if truth(row["passed"])]
    open_gates = [row for row in gate_rows if not truth(row["passed"])]
    add(checks, "gate_pass_count", len(passed_gates) == 20, str(len(passed_gates)))
    add(checks, "gate_open_count", len(open_gates) == 9, str(len(open_gates)))
    add(checks, "gate_pass_status", all(row["status"] == "PASS" for row in passed_gates), "closed gates")
    add(checks, "gate_open_status", all(row["status"] == "OPEN_NONCLAIM" for row in open_gates), "open gates")
    required_open = {
        "D_dimensional_mu2_rational_terms",
        "triangle_coefficients_all_channels",
        "bubble_coefficients_all_channels",
        "complete_one_loop_phi2h2",
        "universal_IR_normalization",
        "crossing_complete_outer_hh_cut",
        "numeric_full_K_mu_K_ang",
        "exact_all_operator_local_GR",
        "full_MTS",
    }
    add(checks, "required_nonclaim_set", {row["gate"] for row in open_gates} == required_open, ",".join(sorted(required_open)))

    symbolic_residuals = [
        B_st - expected_boxes["I4(s,t)"],
        B_su - expected_boxes["I4(s,u)"],
        B_tu - expected_boxes["I4(t,u)"],
        B_su - mixed_su,
        B_st - mixed_su.xreplace({t: u, u: t}),
        B_st.xreplace({t: u, u: t}) - B_su,
    ]
    randomizer = random.Random(4992)
    for event in range(32):
        t_value = -sp.Rational(randomizer.randint(1, 97), randomizer.randint(1, 43))
        u_value = -sp.Rational(randomizer.randint(1, 89), randomizer.randint(1, 47))
        values = {t: t_value, u: u_value}
        for residual_index, residual in enumerate(symbolic_residuals):
            evaluated = sp.factor(residual.subs(values))
            add(
                checks,
                f"random_{event:02d}_{residual_index:02d}",
                evaluated == 0,
                f"t={t_value},u={u_value},residual={evaluated}",
            )

    failed = [row for row in checks if not row["passed"]]
    write_validation(checks)
    VALIDATION_PROVENANCE.write_text(
        "\n".join(
            [
                "# 4992 independent validation provenance",
                "",
                f"Marker: {VALIDATION_MARKER}.",
                "",
                "The validator does not import the 4992 generator. It reconstructs both cut charts from rank-one spinors, derives every propagator, evaluates finite and projective-infinity quadruple-cut branches, reapplies distinguishable and identical-state factors, reloads the 4991 source coefficients, and compares all three shared box coefficients symbolically and at exact random rational kinematics.",
                "",
                f"Checks: {len(checks)}.",
                f"Passed: {len(checks) - len(failed)}.",
                f"Failed: {len(failed)}.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "validation_marker": VALIDATION_MARKER,
                "checks": len(checks),
                "passed": len(checks) - len(failed),
                "failed": len(failed),
                "validation": str(VALIDATION),
            },
            indent=2,
            sort_keys=True,
        )
    )
    if failed:
        for row in failed[:20]:
            print(json.dumps(row, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
