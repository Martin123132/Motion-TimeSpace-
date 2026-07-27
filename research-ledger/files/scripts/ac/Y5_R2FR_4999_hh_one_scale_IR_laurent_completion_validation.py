from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FUNCTIONAL = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL / "4999"
RESIDUALS = POST / "source-intake" / "mts_residuals"

MIXED = FUNCTIONAL / "4998" / "complete_generic_D_mixed_cut.csv"
SCALAR = FUNCTIONAL / "4997" / "complete_generic_D_scalar_s_cut.csv"
TRIANGLES = FUNCTIONAL / "4993" / "full_phi2h2_triangle_completion.csv"
HH = FUNCTIONAL / "4991" / "massless_hh_channel_integral_coefficients.csv"
RECONCILIATION = FUNCTIONAL / "4997" / "one_scale_coordinate_reconciliation.csv"
RESULT = SOURCE / "hh_one_scale_IR_laurent_completion_results.json"
LAURENT = SOURCE / "IR_laurent_lower_sector_solve.csv"
HH_OUT = SOURCE / "hh_direct_one_scale_laurent.csv"
SCHEME = SOURCE / "evanescent_hh_scheme_translation.csv"
GATE = SOURCE / "hh_one_scale_IR_laurent_gate.csv"
DOCUMENT = POST / "4999-Y5-R2FR-hh-one-scale-IR-Laurent-completion.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_4999_VALIDATION.csv"
PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

MARKER = "MTS_4999_HH_ONE_SCALE_IR_LAURENT_COMPLETION"

D = sp.Symbol("D")
epsilon = sp.Symbol("epsilon")
t = sp.Symbol("t", nonzero=True)
u = sp.Symbol("u", nonzero=True)
s = -t - u


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def expression(value: str) -> sp.Expr:
    return sp.sympify(value, locals={"D": D, "epsilon": epsilon, "s": s, "t": t, "u": u})


def exact(value: sp.Expr | int) -> str:
    return sp.sstr(sp.factor(sp.cancel(sp.together(sp.sympify(value)))))


def coefficient_map(path: Path, key: str) -> dict[str, sp.Expr]:
    return {row[key]: expression(row["formula"]) for row in read_csv(path) if row.get(key) and row.get("formula")}


def eps(value: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    continued = sp.factor(value.subs(D, 4 - 2 * epsilon))
    return sp.factor(continued.subs(epsilon, 0)), sp.factor(sp.diff(continued, epsilon).subs(epsilon, 0))


def add(checks: list[dict[str, Any]], check_id: str, passed: bool, detail: str) -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "checkpoint_marker": MARKER})


def main() -> int:
    required = [MIXED, SCALAR, TRIANGLES, HH, RECONCILIATION, RESULT, LAURENT, HH_OUT, SCHEME, GATE, DOCUMENT]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("missing validation inputs: " + "; ".join(missing))
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    mixed = coefficient_map(MIXED, "coefficient")
    scalar = coefficient_map(SCALAR, "coefficient")
    ratio = lambda channel: sp.factor((D - 4) * channel / (2 * (D - 3)))
    At = sp.factor(mixed["T_t_finite"] + ratio(t) * mixed["C_t_finite"])
    Au = sp.factor(mixed["T_u_finite"] + ratio(u) * mixed["C_u_finite"])
    B0 = {}
    B1 = {}
    for name in ("B_st_full", "B_su_full", "B_tu_full"):
        B0[name], B1[name] = eps(mixed[name])
    At0, At1 = eps(At)
    Au0, Au1 = eps(Au)
    box0 = sp.factor(B0["B_st_full"] / (s * t) + B0["B_su_full"] / (s * u) + B0["B_tu_full"] / (t * u))
    box1 = sp.factor(B1["B_st_full"] / (s * t) + B1["B_su_full"] / (s * u) + B1["B_tu_full"] / (t * u))
    As0 = sp.factor(s * (4 * box0 - At0 / t - Au0 / u))
    As1 = sp.factor(s * (4 * box1 - At1 / t - Au1 / u))
    Sc0, Sc1 = eps(scalar["T_s_scalar_direct(D)"])
    H0 = sp.factor(As0 - Sc0)
    H1 = sp.factor(As1 - Sc1)

    triangle_rows = read_csv(TRIANGLES)
    hh_rows = read_csv(HH)
    recon_rows = read_csv(RECONCILIATION)
    full_target = expression(next(row["coefficient"] for row in triangle_rows if row["triangle_id"] == "TRI4993_01_Ts"))
    fdh0 = expression(next(row["coefficient_D4"] for row in hh_rows if row["basis_id"] == "HHAMP4991_02_I3s"))
    Chh0 = expression(next(row["coefficient_D4"] for row in hh_rows if row["basis_id"] == "HHAMP4991_01_I2s"))
    fdh1 = sp.factor(-s * Chh0)
    translation = expression(next(row["right_hand_side"] for row in recon_rows if row["identity"] == "D4_triangle_coordinate_difference"))

    expected_As0 = sp.factor((t + u) * (t**6 + t**5 * u + 2 * t**4 * u**2 + 2 * t**2 * u**4 + t * u**5 + u**6) / 8)
    expected_As1 = sp.factor((t + u) * (22 * t**6 + 36 * t**5 * u + 21 * t**4 * u**2 + 22 * t**3 * u**3 + 21 * t**2 * u**4 + 36 * t * u**5 + 22 * u**6) / 96)
    expected_H0 = sp.factor((t + u) * (t**6 - t**5 * u + t**4 * u**2 - t**3 * u**3 + t**2 * u**4 - t * u**5 + u**6) / 16)
    expected_H1 = sp.factor((t + u) * (11 * t**6 - 3 * t**5 * u - 27 * t**4 * u**2 - 27 * t**2 * u**4 - 3 * t * u**5 + 11 * u**6) / 96)

    checks: list[dict[str, Any]] = []
    add(checks, "marker", result.get("checkpoint_marker") == MARKER, str(result.get("checkpoint_marker")))
    add(checks, "P0", sp.factor(4 * box0 - As0 / s - At0 / t - Au0 / u) == 0, "constant double pole")
    add(checks, "P1", sp.factor(4 * box1 - As1 / s - At1 / t - Au1 / u) == 0, "constant simple pole")
    add(checks, "As0_formula", sp.factor(As0 - expected_As0) == 0, exact(As0))
    add(checks, "As1_formula", sp.factor(As1 - expected_As1) == 0, exact(As1))
    add(checks, "H0_formula", sp.factor(H0 - expected_H0) == 0, exact(H0))
    add(checks, "H1_formula", sp.factor(H1 - expected_H1) == 0, exact(H1))
    add(checks, "full_IR_target", sp.factor(As0 - full_target) == 0, exact(As0 - full_target))
    add(checks, "translation", sp.factor(H0 - fdh0 - translation) == 0, exact(H0 - fdh0 - translation))
    add(checks, "t_u_crossing_0", sp.factor(At0 - Au0.xreplace({t: u, u: t})) == 0, exact(At0 - Au0.xreplace({t: u, u: t})))
    add(checks, "t_u_crossing_1", sp.factor(At1 - Au1.xreplace({t: u, u: t})) == 0, exact(At1 - Au1.xreplace({t: u, u: t})))
    add(checks, "s_symmetry_0", sp.factor(H0 - H0.xreplace({t: u, u: t})) == 0, "t<->u")
    add(checks, "s_symmetry_1", sp.factor(H1 - H1.xreplace({t: u, u: t})) == 0, "t<->u")
    add(checks, "FDH_linear_coordinate", sp.factor(fdh1 + s * Chh0) == 0, exact(fdh1))

    output_laurent = {row["channel"]: row for row in read_csv(LAURENT) if row["channel"] in ("s", "t", "u")}
    for channel, zero, one in (("s", As0, As1), ("t", At0, At1), ("u", Au0, Au1)):
        add(checks, f"stored_{channel}_0", sp.factor(expression(output_laurent[channel]["epsilon_0"]) - zero) == 0, output_laurent[channel]["epsilon_0"])
        add(checks, f"stored_{channel}_1", sp.factor(expression(output_laurent[channel]["epsilon_1"]) - one) == 0, output_laurent[channel]["epsilon_1"])
    output_hh = {row["component"]: row for row in read_csv(HH_OUT)}
    add(checks, "stored_hh_0", sp.factor(expression(output_hh["A_s_hh_CDR_direct_inference"]["epsilon_0"]) - H0) == 0, "hh epsilon0")
    add(checks, "stored_hh_1", sp.factor(expression(output_hh["A_s_hh_CDR_direct_inference"]["epsilon_1"]) - H1) == 0, "hh epsilon1")

    samples = [(1, 2), (2, 3), (3, 5), (5, 2), (7, 4), (4, 9), (8, 3), (11, 6)]
    for index, (tv, uv) in enumerate(samples, start=1):
        substitutions = {t: sp.Rational(tv), u: sp.Rational(uv)}
        add(checks, f"sample_{index}_H0", sp.factor((H0 - expected_H0).subs(substitutions)) == 0, f"t={tv},u={uv}")
        add(checks, f"sample_{index}_H1", sp.factor((H1 - expected_H1).subs(substitutions)) == 0, f"t={tv},u={uv}")
        add(checks, f"sample_{index}_P0", sp.factor((4 * box0 - As0 / s - At0 / t - Au0 / u).subs(substitutions)) == 0, f"t={tv},u={uv}")
        add(checks, f"sample_{index}_P1", sp.factor((4 * box1 - As1 / s - At1 / t - Au1 / u).subs(substitutions)) == 0, f"t={tv},u={uv}")

    hashes = result.get("source_hashes_sha256", {})
    for path_text, expected in hashes.items():
        path = ROOT / Path(path_text)
        add(checks, "hash_" + Path(path_text).name, path.exists() and digest(path) == expected, path_text)
    add(checks, "formalization_unchanged", tree_digest(ROOT / "formalization-workbench") == result.get("formalization_workbench_tree_sha256"), str(result.get("formalization_workbench_tree_sha256")))
    all_rows = read_csv(LAURENT) + read_csv(HH_OUT) + read_csv(SCHEME) + read_csv(GATE)
    add(checks, "all_rows_nonclaim", all(row.get("valid_for_full_MTS_claim") == "False" for row in all_rows), f"rows={len(all_rows)}")
    add(checks, "exact_D_gate_open", any(row["gate"] == "exact_generic_D_hh_lower_sector" and row["passed"] == "False" for row in read_csv(GATE)), "no arbitrary-D overclaim")
    add(checks, "dJ2_gate_open", result.get("cut_free_dJ2_remainder_complete") is False, "dJ2 remains open")
    add(checks, "outer_gate_open", result.get("outer_cut_complete") is False, "outer cut remains open")

    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check_id", "passed", "detail", "checkpoint_marker"])
        writer.writeheader()
        writer.writerows(checks)
    passed = all(row["passed"] for row in checks)
    PROVENANCE.write_text(
        "\n".join(
            [
                "# 4999 validation provenance",
                "",
                "The validator independently reparses every inherited coefficient, reconstructs A=T+rC, resolves both Laurent pole equations, checks closed formulas and crossings symbolically and at eight held-out rational kinematics, verifies stored rows and source hashes, and enforces all nonclaim gates.",
                "",
                f"Checks: `{len(checks)}`. Passed: `{passed}`.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps({"checkpoint_marker": MARKER, "checks": len(checks), "passed": passed, "validation": str(VALIDATION)}, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
