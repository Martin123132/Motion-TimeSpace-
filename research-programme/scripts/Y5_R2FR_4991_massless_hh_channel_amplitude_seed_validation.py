from __future__ import annotations

import csv
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Any

import sympy as sp
from sympy.parsing.mathematica import parse_mathematica


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4991"
CHI_SOURCE = SOURCE / "sources" / "chi_1903.07944" / "GravitonBending.tex"
CHI_COEFFICIENTS = SOURCE / "sources" / "chi_1903.07944" / "Coeff-of-Integrals.txt"
DUNBAR_SOURCE = POST / "source-intake" / "functional_rg" / "4986" / "sources" / "dunbar_norridge" / "9512084.tex"
COEFFICIENTS = SOURCE / "massless_hh_channel_integral_coefficients.csv"
IDENTITIES = SOURCE / "massless_hh_channel_identity_checks.csv"
SCOPES = SOURCE / "one_loop_amplitude_scope_and_IR_test.csv"
GATES = SOURCE / "massless_hh_channel_amplitude_gate.csv"
RESULT = SOURCE / "massless_hh_channel_amplitude_seed_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4991_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

MARKER = "MTS_4991_MASSLESS_HH_CHANNEL_AMPLITUDE_SEED"
VALIDATION_MARKER = "P8_Y5_BRR545_4991_VALIDATION"

s, t, u, D = sp.symbols("s t u D", nonzero=True)
Q, Qbar, kappa, F_hh = sp.symbols("Q Qbar kappa F_hh", nonzero=True)


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
    return sp.sympify(expression, locals={"s": s, "t": t, "u": u, "pi": sp.pi})


def zero(expression: sp.Expr) -> bool:
    return sp.factor(sp.together(sp.simplify(expression))) == 0


def add(checks: list[dict[str, Any]], check_id: str, passed: bool, evidence: str) -> None:
    checks.append(
        {
            "validation_id": f"VAL4991_{len(checks) + 1:04d}_{check_id}",
            "check": check_id,
            "passed": bool(passed),
            "evidence": evidence,
            "validation_marker": VALIDATION_MARKER,
        }
    )


def independently_parse_ancillary() -> tuple[sp.Expr, ...]:
    source = "\n".join(
        line for line in CHI_COEFFICIENTS.read_text(encoding="utf-8").splitlines() if not line.startswith("##")
    ).strip()
    if not source.startswith("(1/4)*"):
        raise ValueError("unrecognized ancillary normalization")
    parsed = parse_mathematica(source[len("(1/4)*") :])
    if not isinstance(parsed, sp.Tuple) or len(parsed) != 5:
        raise ValueError("expected five integral coefficients")
    return tuple(sp.Rational(1, 4) * coefficient for coefficient in parsed)


def write_validation(rows: list[dict[str, Any]]) -> None:
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    checks: list[dict[str, Any]] = []
    files = [CHI_SOURCE, CHI_COEFFICIENTS, DUNBAR_SOURCE, COEFFICIENTS, IDENTITIES, SCOPES, GATES, RESULT, PROVENANCE]
    for path in files:
        add(checks, f"file_exists_{path.stem}", path.exists(), str(path))
        add(
            checks,
            f"file_nonempty_{path.stem}",
            path.exists() and path.stat().st_size > 0,
            str(path.stat().st_size if path.exists() else 0),
        )

    coefficient_rows = read_csv(COEFFICIENTS)
    identity_rows = read_csv(IDENTITIES)
    scope_rows = read_csv(SCOPES)
    gate_rows = read_csv(GATES)
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    tables = {
        "coefficients": (coefficient_rows, 4),
        "identities": (identity_rows, 8),
        "scopes": (scope_rows, 4),
        "gates": (gate_rows, 16),
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
        add(checks, f"no_missing_marker_{name}", "MISSING_" not in joined, "no placeholder markers")

    add(checks, "result_marker", result["checkpoint_marker"] == MARKER, result["checkpoint_marker"])
    add(checks, "source_marker_count", len(result["source_checks"]) == 8, str(len(result["source_checks"])))
    add(checks, "all_source_markers", all(result["source_checks"].values()), json.dumps(result["source_checks"], sort_keys=True))
    for source_path, expected_hash in result["source_hashes"].items():
        path = ROOT / source_path
        add(checks, f"source_exists_{len(checks)}", path.exists(), source_path)
        if path.exists():
            add(checks, f"source_hash_{len(checks)}", digest(path) == expected_hash, source_path)

    chi = " ".join(CHI_SOURCE.read_text(encoding="utf-8", errors="replace").split())
    dunbar = " ".join(DUNBAR_SOURCE.read_text(encoding="utf-8", errors="replace").split())
    source_checks = {
        "chi_s_channel": "Focusing on terms with an $s$-channel cut" in chi,
        "chi_basis": "b_1 I_4(s,t) + b_2 I_4(s,u)" in chi and "b I_2(s)" in chi,
        "chi_reduction_scope": "scalar massive triangle integral and two scalar box integrals" in chi,
        "dunbar_box": "I^{}_4 (s,t)" in dunbar,
        "dunbar_triangle": "I_{3}(s)" in dunbar,
        "dunbar_bubble": "I_2(s)" in dunbar,
    }
    for name, passed in source_checks.items():
        add(checks, f"independent_source_{name}", passed, name)

    coefficients = independently_parse_ancillary()
    M = sp.Symbol("M")
    parser_s = sp.Symbol("s")
    parser_t = sp.Symbol("t")
    parser_D = sp.Symbol("D")
    substitution = {M: 0, parser_s: -t - u, parser_t: t, parser_D: D}
    bubble_D, triangle_1, triangle_2, box_st, box_su = [sp.factor(value.subs(substitution)) for value in coefficients]
    bubble_4 = sp.factor(bubble_D.subs(D, 4))
    bubble_epsilon_1 = sp.factor(-2 * sp.diff(bubble_D, D).subs(D, 4))
    triangle_sum = sp.factor(triangle_1 + triangle_2)
    expected_bubble_4 = sp.factor(t * u * (2 * (t**4 + u**4) - 3 * t * u * (t**2 + u**2)) / 32)
    expected_bubble_epsilon_1 = sp.factor(
        -t * u * (180 * (t**4 + u**4) - 333 * t * u * (t**2 + u**2) + 605 * t**2 * u**2) / 2880
    )
    expected_triangle = -sp.Rational(1, 16) * (t**7 + u**7)
    expected_box_st = sp.Rational(1, 32) * t**4 * (t**4 + u**4)
    expected_box_su = sp.Rational(1, 32) * u**4 * (t**4 + u**4)
    double_pole = sp.factor(
        4 * box_st / ((-t - u) * t) + 4 * box_su / ((-t - u) * u) - triangle_sum / (-t - u)
    )
    expected_double_pole = -(
        3 * t**6
        - 3 * t**5 * u
        + 3 * t**4 * u**2
        - t**3 * u**3
        + 3 * t**2 * u**4
        - 3 * t * u**5
        + 3 * u**6
    ) / 16
    derived = {
        "bubble_D4": bubble_4 - expected_bubble_4,
        "bubble_epsilon_1": bubble_epsilon_1 - expected_bubble_epsilon_1,
        "triangle_sum": triangle_sum - expected_triangle,
        "box_st": box_st - expected_box_st,
        "box_su": box_su - expected_box_su,
        "double_pole": double_pole - expected_double_pole,
        "bubble_crossing": bubble_4 - bubble_4.xreplace({t: u, u: t}),
        "triangle_crossing": triangle_sum - triangle_sum.xreplace({t: u, u: t}),
    }
    for name, residual in derived.items():
        add(checks, f"symbolic_{name}", zero(residual), sp.sstr(sp.factor(residual)))

    by_integral = {row["integral"]: row for row in coefficient_rows}
    recorded = {
        "recorded_bubble_D4": parse(by_integral["I2(s)"]["coefficient_D4"]) - bubble_4,
        "recorded_bubble_epsilon": parse(by_integral["I2(s)"]["coefficient_epsilon_1"]) - bubble_epsilon_1,
        "recorded_triangle": parse(by_integral["I3(s)"]["coefficient_D4"]) - triangle_sum,
        "recorded_box_st": parse(by_integral["I4(s,t)"]["coefficient_D4"]) - box_st,
        "recorded_box_su": parse(by_integral["I4(s,u)"]["coefficient_D4"]) - box_su,
    }
    for name, residual in recorded.items():
        add(checks, name, zero(residual), sp.sstr(sp.factor(residual)))

    add(
        checks,
        "recorded_identity_residuals",
        all(zero(parse(row["exact_residual"])) for row in identity_rows),
        ",".join(row["identity_id"] for row in identity_rows),
    )
    scope_by_id = {row["scope_id"]: row for row in scope_rows}
    add(checks, "seed_scope_true", truth(scope_by_id["HHSCOPE4991_01_derived_seed"]["valid"]), scope_by_id["HHSCOPE4991_01_derived_seed"]["status"])
    add(checks, "partial_pole_scope_true", truth(scope_by_id["HHSCOPE4991_02_double_pole"]["valid"]), scope_by_id["HHSCOPE4991_02_double_pole"]["status"])
    add(checks, "full_amplitude_scope_false", not truth(scope_by_id["HHSCOPE4991_03_full_amplitude"]["valid"]), scope_by_id["HHSCOPE4991_03_full_amplitude"]["status"])
    add(checks, "outer_cut_scope_false", not truth(scope_by_id["HHSCOPE4991_04_outer_cut"]["valid"]), scope_by_id["HHSCOPE4991_04_outer_cut"]["status"])
    add(
        checks,
        "recorded_double_pole",
        zero(parse(scope_by_id["HHSCOPE4991_02_double_pole"]["evidence"]) - double_pole),
        scope_by_id["HHSCOPE4991_02_double_pole"]["evidence"],
    )

    amplitude_1 = kappa**4 * F_hh / Q**4
    amplitude_0_conjugate = kappa**2 * Q**4 / (4 * s * t * u)
    interference = sp.factor(amplitude_1 * amplitude_0_conjugate)
    add(
        checks,
        "independent_phase_cancellation",
        zero(interference - kappa**6 * F_hh / (4 * s * t * u)),
        sp.sstr(interference),
    )

    randomizer = random.Random(4991)
    for event in range(24):
        t_value = -sp.Rational(randomizer.randint(1, 83), randomizer.randint(1, 37))
        u_value = -sp.Rational(randomizer.randint(1, 79), randomizer.randint(1, 41))
        event_values = {t: t_value, u: u_value}
        for name, residual in derived.items():
            value = sp.factor(residual.subs(event_values))
            add(checks, f"rational_{event:02d}_{name}", value == 0, str(value))

    gates_by_name = {row["gate"]: row for row in gate_rows}
    closed_gates = {
        "primary_source_lock",
        "five_coefficient_parse",
        "massless_bubble_reduction",
        "bubble_epsilon_term",
        "triangle_degeneracy",
        "box_st_reduction",
        "box_su_reduction",
        "identical_scalar_crossing",
        "physical_phase_cancellation",
    }
    open_gates = set(gates_by_name) - closed_gates
    add(checks, "closed_gate_count", len(closed_gates) == 9, str(len(closed_gates)))
    add(checks, "open_gate_count", len(open_gates) == 7, str(len(open_gates)))
    for gate in sorted(closed_gates):
        row = gates_by_name[gate]
        add(checks, f"closed_gate_{gate}", truth(row["passed"]) and truth(row["valid_for_checkpoint_claim"]), row["status"])
    for gate in sorted(open_gates):
        row = gates_by_name[gate]
        add(checks, f"open_gate_{gate}", not truth(row["passed"]) and not truth(row["valid_for_checkpoint_claim"]), row["status"])

    result_expressions = {
        "I2_s": bubble_4,
        "I2_s_epsilon_1": bubble_epsilon_1,
        "I3_s": triangle_sum,
        "I4_st": box_st,
        "I4_su": box_su,
        "partial_double_pole": double_pole,
    }
    for name, expected in result_expressions.items():
        residual = parse(result["massless_hh_s_channel"][name]) - expected
        add(checks, f"result_{name}", zero(residual), result["massless_hh_s_channel"][name])
    add(checks, "result_complete_false", result["complete_one_loop_phi2h2"] is False, str(result["complete_one_loop_phi2h2"]))
    add(checks, "result_outer_cut_false", result["crossing_complete_outer_hh_cut"] is False, str(result["crossing_complete_outer_hh_cut"]))
    add(checks, "result_full_Kmu_false", result["numeric_full_K_mu"] is False, str(result["numeric_full_K_mu"]))
    add(checks, "result_full_Kang_false", result["numeric_full_K_ang"] is False, str(result["numeric_full_K_ang"]))
    add(checks, "result_local_GR_false", result["exact_all_operator_local_GR"] is False, str(result["exact_all_operator_local_GR"]))
    add(checks, "result_full_MTS_false", result["full_MTS"] is False, str(result["full_MTS"]))

    write_validation(checks)
    passed = sum(bool(row["passed"]) for row in checks)
    VALIDATION_PROVENANCE.write_text(
        "\n".join(
            [
                "# 4991 independent validation provenance",
                "",
                f"Marker: `{VALIDATION_MARKER}`.",
                "",
                "The validator does not import the generator. It reparses Chi's D-dimensional ancillary coefficients, independently takes the M=0 and D=4-2 epsilon limits, reconstructs all four integral coefficients and the partial double pole, checks exact t-u symmetry and 24 rational kinematic events, verifies source hashes and table scope, and enforces seven explicit nonclaim gates.",
                "",
                f"Checks passed: `{passed}/{len(checks)}`.",
                f"Validation CSV: `{VALIDATION.relative_to(ROOT).as_posix()}`.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "validation_marker": VALIDATION_MARKER,
                "passed": passed,
                "total": len(checks),
                "output": str(VALIDATION),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
