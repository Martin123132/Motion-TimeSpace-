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
SOURCE = POST / "source-intake" / "functional_rg" / "4993"
DUNBAR_SOURCE = POST / "source-intake" / "functional_rg" / "4986" / "sources" / "dunbar_norridge" / "9512084.tex"
CHI_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4991"
    / "sources"
    / "chi_1903.07944"
    / "GravitonBending.tex"
)
BOX_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4992"
    / "mixed_hphi_cut_and_full_box_completion_results.json"
)
SOURCE_LOCK_CSV = SOURCE / "soft_operator_source_lock.csv"
POLE_BASIS_CSV = SOURCE / "one_loop_integral_pole_basis.csv"
TRIANGLE_CSV = SOURCE / "full_phi2h2_triangle_completion.csv"
IR_CSV = SOURCE / "infrared_pole_reconstruction.csv"
GATE_CSV = SOURCE / "triangle_completion_gate.csv"
RESULT_JSON = SOURCE / "universal_soft_operator_and_triangle_completion_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4993_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

MARKER = "MTS_4993_UNIVERSAL_SOFT_OPERATOR_AND_TRIANGLE_COMPLETION"
VALIDATION_MARKER = "P8_Y5_BRR545_4993_VALIDATION"

t, u = sp.symbols("t u", nonzero=True)
s = -t - u
L_s, L_t, L_u, epsilon = sp.symbols("L_s L_t L_u epsilon")


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
    return sp.sympify(
        expression,
        locals={
            "s": s,
            "t": t,
            "u": u,
            "L_s": L_s,
            "L_t": L_t,
            "L_u": L_u,
            "pi": sp.pi,
        },
    )


def zero(expression: sp.Expr) -> bool:
    return sp.factor(sp.cancel(sp.together(sp.simplify(expression)))) == 0


def add(checks: list[dict[str, Any]], check_id: str, passed: bool, evidence: str) -> None:
    checks.append(
        {
            "validation_id": f"VAL4993_{len(checks) + 1:04d}_{check_id}",
            "check": check_id,
            "passed": bool(passed),
            "evidence": evidence,
            "validation_marker": VALIDATION_MARKER,
        }
    )


def write_validation(rows: list[dict[str, Any]]) -> None:
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    checks: list[dict[str, Any]] = []
    required_files = [
        DUNBAR_SOURCE,
        CHI_SOURCE,
        BOX_RESULT,
        SOURCE_LOCK_CSV,
        POLE_BASIS_CSV,
        TRIANGLE_CSV,
        IR_CSV,
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

    source_rows = read_csv(SOURCE_LOCK_CSV)
    pole_rows = read_csv(POLE_BASIS_CSV)
    triangle_rows = read_csv(TRIANGLE_CSV)
    ir_rows = read_csv(IR_CSV)
    gate_rows = read_csv(GATE_CSV)
    result = json.loads(RESULT_JSON.read_text(encoding="utf-8"))
    tables = {
        "sources": (source_rows, 9),
        "poles": (pole_rows, 3),
        "triangles": (triangle_rows, 5),
        "infrared": (ir_rows, 7),
        "gates": (gate_rows, 25),
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
    add(checks, "result_triangle_complete", truth(result["triangle_sector_complete_from_IR"]), "triangle sector")
    add(checks, "result_box_complete", truth(result["four_dimensional_box_sector_complete"]), "box sector")
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

    dunbar = " ".join(DUNBAR_SOURCE.read_text(encoding="utf-8", errors="replace").split())
    chi = " ".join(CHI_SOURCE.read_text(encoding="utf-8", errors="replace").split())
    source_markers = {
        "soft_pair": "summed over all pairs of external legs" in dunbar,
        "soft_formula": "s \\ln(-s) + t \\ln(-t) + u \\ln(-u)" in dunbar,
        "universal_matter": "external legs are gravitons or scalars" in dunbar,
        "box_poles": "{4\\over \\eps^2}" in dunbar and "2\\ln( -s)\\ln(-t)" in dunbar,
        "triangle_poles": "I_{3}(s)" in dunbar and "{ \\ln^2(-s) \\over 2}" in dunbar,
        "bubble_poles": "I_2(s)" in dunbar and "{1\\over \\eps } - \\ln(-s) + 2" in dunbar,
        "chi_kappa": "\\kappa^2=32 \\pi G" in chi,
        "chi_tree_quarter": "\\frac{\\kappa^2}{4}" in chi,
    }
    for name, passed in source_markers.items():
        add(checks, f"independent_source_{name}", passed, name)
    add(checks, "recorded_source_locks", all(truth(row["passed"]) for row in source_rows), "all source rows pass")

    box_data = json.loads(BOX_RESULT.read_text(encoding="utf-8"))
    boxes = {
        "B_st": parse(box_data["full_four_dimensional_box_sector"]["I4(s,t)"]),
        "B_su": parse(box_data["full_four_dimensional_box_sector"]["I4(s,u)"]),
        "B_tu": parse(box_data["full_four_dimensional_box_sector"]["I4(t,u)"]),
    }
    expected_boxes = {
        "B_st": t**4 * (s**4 + t**4 + u**4) / 32,
        "B_su": u**4 * (s**4 + t**4 + u**4) / 32,
        "B_tu": t**4 * u**4 / 16,
    }
    for name in boxes:
        add(checks, f"box_{name}", zero(boxes[name] - expected_boxes[name]), sp.sstr(sp.factor(boxes[name])))

    pair_sum = 2 * (
        -s * sp.exp(-epsilon * L_s)
        - t * sp.exp(-epsilon * L_t)
        - u * sp.exp(-epsilon * L_u)
    )
    pair_leading = sp.factor(pair_sum.subs(epsilon, 0))
    pair_first = sp.factor(sp.diff(pair_sum, epsilon).subs(epsilon, 0))
    add(checks, "pair_leading", zero(pair_leading), sp.sstr(pair_leading))
    add(
        checks,
        "pair_first",
        zero(pair_first - 2 * (s * L_s + t * L_t + u * L_u)),
        sp.sstr(pair_first),
    )

    Q, Qbar = sp.symbols("Q Qbar", nonzero=True)
    tree_original = Q**4 / (4 * s * t * u)
    tree_rephased = sp.factor(tree_original.subs(Q, t * u / Qbar) * Qbar**4)
    expected_tree_reduced = t**3 * u**3 / (4 * s)
    add(checks, "tree_phase_conversion", zero(tree_rephased - expected_tree_reduced), sp.sstr(tree_rephased))

    universal = {
        "s": sp.factor(expected_tree_reduced * s / 2),
        "t": sp.factor(expected_tree_reduced * t / 2),
        "u": sp.factor(expected_tree_reduced * u / 2),
    }
    box_logs = {
        "s": sp.factor(-2 * boxes["B_st"] / (s * t) - 2 * boxes["B_su"] / (s * u)),
        "t": sp.factor(-2 * boxes["B_st"] / (s * t) - 2 * boxes["B_tu"] / (t * u)),
        "u": sp.factor(-2 * boxes["B_su"] / (s * u) - 2 * boxes["B_tu"] / (t * u)),
    }
    T_s_symbol, T_t_symbol, T_u_symbol = sp.symbols("T_s_symbol T_t_symbol T_u_symbol")
    equations = [
        sp.Eq(box_logs["s"] + T_s_symbol / s, universal["s"]),
        sp.Eq(box_logs["t"] + T_t_symbol / t, universal["t"]),
        sp.Eq(box_logs["u"] + T_u_symbol / u, universal["u"]),
    ]
    solution = sp.solve(equations, (T_s_symbol, T_t_symbol, T_u_symbol), dict=True)
    add(checks, "triangle_linear_unique", len(solution) == 1, str(len(solution)))
    solved = {
        "T_s": sp.factor(solution[0][T_s_symbol]),
        "T_t": sp.factor(solution[0][T_t_symbol]),
        "T_u": sp.factor(solution[0][T_u_symbol]),
    }
    jacobian = sp.Matrix(
        [
            [sp.diff(equation.lhs - equation.rhs, symbol) for symbol in (T_s_symbol, T_t_symbol, T_u_symbol)]
            for equation in equations
        ]
    )
    add(
        checks,
        "triangle_system_determinant",
        zero(jacobian.det() - 1 / (s * t * u)),
        sp.sstr(sp.factor(jacobian.det())),
    )

    expected_triangles = {
        "T_s": sp.factor(
            (t + u)
            * (
                t**6
                + t**5 * u
                + 2 * t**4 * u**2
                + 2 * t**2 * u**4
                + t * u**5
                + u**6
            )
            / 8
        ),
        "T_t": sp.factor(-t**5 * (t**2 + t * u + 2 * u**2) / 8),
        "T_u": sp.factor(-u**5 * (2 * t**2 + t * u + u**2) / 8),
    }
    for name in solved:
        add(checks, f"solved_{name}", zero(solved[name] - expected_triangles[name]), sp.sstr(solved[name]))

    actual_logs = {
        "s": sp.factor(box_logs["s"] + solved["T_s"] / s),
        "t": sp.factor(box_logs["t"] + solved["T_t"] / t),
        "u": sp.factor(box_logs["u"] + solved["T_u"] / u),
    }
    for name in actual_logs:
        add(
            checks,
            f"soft_log_{name}",
            zero(actual_logs[name] - universal[name]),
            sp.sstr(sp.factor(actual_logs[name] - universal[name])),
        )

    double_pole = sp.factor(
        4 * boxes["B_st"] / (s * t)
        + 4 * boxes["B_su"] / (s * u)
        + 4 * boxes["B_tu"] / (t * u)
        - solved["T_s"] / s
        - solved["T_t"] / t
        - solved["T_u"] / u
    )
    add(checks, "double_pole_zero", zero(double_pole), sp.sstr(double_pole))
    add(
        checks,
        "triangle_crossing",
        zero(solved["T_t"] - solved["T_u"].xreplace({t: u, u: t})),
        "T_t(t,u)=T_u(u,t)",
    )
    add(
        checks,
        "triangle_s_symmetry",
        zero(solved["T_s"] - solved["T_s"].xreplace({t: u, u: t})),
        "T_s symmetric",
    )

    triangle_by_integral = {
        row["integral"]: row for row in triangle_rows if row["triangle_id"] in {"TRI4993_01_Ts", "TRI4993_02_Tt", "TRI4993_03_Tu"}
    }
    for integral, name in (("I3(s)", "T_s"), ("I3(t)", "T_t"), ("I3(u)", "T_u")):
        add(
            checks,
            f"recorded_{name}",
            zero(parse(triangle_by_integral[integral]["coefficient"]) - solved[name]),
            triangle_by_integral[integral]["coefficient"],
        )
        add(
            checks,
            f"recorded_log_residual_{name}",
            zero(parse(triangle_by_integral[integral]["log_pole_residual"])),
            triangle_by_integral[integral]["log_pole_residual"],
        )

    for integral, name in (("I3(s)", "T_s"), ("I3(t)", "T_t"), ("I3(u)", "T_u")):
        add(
            checks,
            f"result_{name}",
            zero(parse(result["full_triangle_sector"][integral]) - solved[name]),
            result["full_triangle_sector"][integral],
        )
    for name in ("s", "t", "u"):
        add(
            checks,
            f"result_soft_target_{name}",
            zero(parse(result["universal_log_targets"][f"L_{name}/epsilon"]) - universal[name]),
            result["universal_log_targets"][f"L_{name}/epsilon"],
        )
    add(checks, "result_double_pole", zero(parse(result["double_pole"])), result["double_pole"])

    pole_by_integral = {row["integral"]: row for row in pole_rows}
    add(checks, "pole_box_double", parse(pole_by_integral["I4(x,y)"]["double_pole"].replace("x", "t").replace("y", "u")) == 4 / (t * u), pole_by_integral["I4(x,y)"]["double_pole"])
    add(checks, "pole_triangle_log", pole_by_integral["I3(x)"]["log_x_over_epsilon"] == "1/x", pole_by_integral["I3(x)"]["log_x_over_epsilon"])
    add(checks, "pole_bubble_no_log_over_epsilon", pole_by_integral["I2(x)"]["log_x_over_epsilon"] == "0", pole_by_integral["I2(x)"]["log_x_over_epsilon"])

    add(checks, "ir_all_residuals", all(row["residual"] == "0" for row in ir_rows), ",".join(row["ir_id"] for row in ir_rows))
    passed_gates = [row for row in gate_rows if truth(row["passed"])]
    open_gates = [row for row in gate_rows if not truth(row["passed"])]
    add(checks, "gate_pass_count", len(passed_gates) == 16, str(len(passed_gates)))
    add(checks, "gate_open_count", len(open_gates) == 9, str(len(open_gates)))
    add(checks, "gate_pass_status", all(row["status"] == "PASS" for row in passed_gates), "closed")
    add(checks, "gate_open_status", all(row["status"] == "OPEN_NONCLAIM" for row in open_gates), "open")
    required_open = {
        "bubble_coefficients_all_channels",
        "UV_counterterm_separation",
        "D_dimensional_mu2_rational_terms",
        "complete_one_loop_phi2h2",
        "finite_common_IR_subtraction",
        "crossing_complete_outer_hh_cut",
        "numeric_full_K_mu_K_ang",
        "exact_all_operator_local_GR",
        "full_MTS",
    }
    add(checks, "required_open_set", {row["gate"] for row in open_gates} == required_open, ",".join(sorted(required_open)))

    residuals = [
        solved["T_s"] - expected_triangles["T_s"],
        solved["T_t"] - expected_triangles["T_t"],
        solved["T_u"] - expected_triangles["T_u"],
        actual_logs["s"] - universal["s"],
        actual_logs["t"] - universal["t"],
        actual_logs["u"] - universal["u"],
        double_pole,
        solved["T_t"] - solved["T_u"].xreplace({t: u, u: t}),
    ]
    randomizer = random.Random(4993)
    for event in range(36):
        t_value = -sp.Rational(randomizer.randint(1, 103), randomizer.randint(1, 47))
        u_value = -sp.Rational(randomizer.randint(1, 101), randomizer.randint(1, 43))
        values = {t: t_value, u: u_value}
        for residual_index, residual in enumerate(residuals):
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
                "# 4993 independent validation provenance",
                "",
                f"Marker: {VALIDATION_MARKER}.",
                "",
                "The validator does not import the generator. It reparses the primary soft and integral-basis sources, reloads the 4992 box coefficients, independently converts the tree helicity phase, expands the four-point pair sum, solves a fresh three-by-three symbolic system for the triangle coefficients, checks its nonzero determinant, reconstructs every logarithmic pole and the double pole, and evaluates exact random rational kinematics.",
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
