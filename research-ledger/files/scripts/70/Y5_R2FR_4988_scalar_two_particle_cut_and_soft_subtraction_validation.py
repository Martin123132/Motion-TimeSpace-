from __future__ import annotations

import csv
import hashlib
import json
import random
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp
import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4988"
RESULT = SOURCE / "scalar_cut_soft_subtraction_results.json"
NORMALIZATION = SOURCE / "canonical_tree_normalization_checks.csv"
KERNEL = SOURCE / "one_loop_hard_kernel_decomposition.csv"
SOFT = SOURCE / "two_loop_soft_endpoint_subtraction.csv"
PARTIAL = SOURCE / "scalar_cut_partial_wave_integrals.csv"
PROJECTION = SOURCE / "scalar_cut_channel_projection.csv"
GATE = SOURCE / "scalar_cut_master_subtraction_gate.csv"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4988_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

MARKER = "MTS_4988_SCALAR_TWO_PARTICLE_CUT_SOFT_SUBTRACTION"
VALIDATION_MARKER = "P8_Y5_BRR545_4988_VALIDATION"


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


def add(checks: list[dict[str, Any]], check_id: str, passed: bool, evidence: str) -> None:
    checks.append(
        {
            "validation_id": f"VAL4988_{len(checks) + 1:04d}_{check_id}",
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


def hard_direct(value: mp.mpf, scale_log: mp.mpf) -> mp.mpf:
    t = -value
    u = value - 1
    log_x = mp.log(value)
    log_one_minus = mp.log1p(-value)
    log_s_real = scale_log
    log_t = scale_log + log_x
    log_u = scale_log + log_one_minus
    result = (1 + t**4) / (8 * t) * log_s_real * log_t
    result += (1 + u**4) / (8 * u) * log_s_real * log_u
    result += (u**4 + t**4) / (8 * t * u) * log_t * log_u
    result += (1 + 2 * t**2 + 2 * u**2) / 16 * (scale_log**2 - mp.pi**2)
    result += (t**2 + 2 + 2 * u**2) / 16 * log_t**2
    result += (u**2 + 2 * t**2 + 2) / 16 * log_u**2
    result += (t / u + t * u + u / t) / 16 * ((scale_log**2 - mp.pi**2) + t * log_t**2 + u * log_u**2)
    result -= (163 * u**2 + 163 * t**2 + 43 * t * u) / 960 * log_s_real
    result -= (163 * u**2 + 163 + 43 * u) / 960 * log_t
    result -= (163 + 163 * t**2 + 43 * t) / 960 * log_u
    return result + mp.pi**2 / (16 * value * (1 - value))


def hard_decomposed(value: mp.mpf, scale_log: mp.mpf) -> mp.mpf:
    log_x = mp.log(value)
    log_one_minus = mp.log1p(-value)
    result = (value**4 + value**3 - 4 * value**2 + 6 * value - 3) * log_x**2 / (16 * (value - 1))
    result -= (2 * value**4 - 4 * value**3 + 6 * value**2 - 4 * value + 1) * log_x * log_one_minus / (8 * value * (value - 1))
    result -= (value**4 - 5 * value**3 + 5 * value**2 - 5 * value + 1) * log_one_minus**2 / (16 * value)
    result -= (163 * value**2 - 283 * value + 283) * log_x / 960
    result -= (163 * value**2 - 43 * value + 163) * log_one_minus / 960
    result -= mp.pi**2 * (3 * value**2 - 3 * value + 1) / 16
    result -= mp.mpf(203) * (value**2 - value + 1) * scale_log / 320
    return result


def quadrature(spin: int, scale_log: mp.mpf) -> mp.mpf:
    delta = mp.mpf("0.0125")

    def weight(value: mp.mpf) -> mp.mpf:
        return mp.mpf(1) if spin == 0 else 1 - 6 * value + 6 * value**2

    def left(variable: mp.mpf) -> mp.mpf:
        if variable == 0:
            return mp.mpf(0)
        value = delta * variable**2
        return 2 * delta * variable * weight(value) * hard_decomposed(value, scale_log)

    middle = mp.quad(lambda value: weight(value) * hard_decomposed(value, scale_log), [delta, mp.mpf("0.4"), mp.mpf("0.6"), 1 - delta])
    return 2 * mp.quad(left, [0, 1]) + middle


def main() -> int:
    required = (RESULT, NORMALIZATION, KERNEL, SOFT, PARTIAL, PROJECTION, GATE)
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("\n".join(missing))

    result = json.loads(RESULT.read_text(encoding="utf-8"))
    normalization_rows = read_csv(NORMALIZATION)
    kernel_rows = read_csv(KERNEL)
    soft_rows = read_csv(SOFT)
    partial_rows = read_csv(PARTIAL)
    projection_rows = read_csv(PROJECTION)
    gate_rows = read_csv(GATE)
    all_rows = normalization_rows + kernel_rows + soft_rows + partial_rows + projection_rows + gate_rows
    checks: list[dict[str, Any]] = []

    add(checks, "marker", result["checkpoint_marker"] == MARKER, result["checkpoint_marker"])
    add(checks, "source_locks", all(result["source_checks"].values()), json.dumps(result["source_checks"], sort_keys=True))
    for path in required:
        add(checks, f"output_exists_{path.stem}", path.exists() and path.stat().st_size > 0, str(path))
    for row in all_rows:
        add(checks, f"row_marker_{len(checks)}", row.get("checkpoint_marker") == MARKER, row.get("checkpoint_marker", ""))
        add(checks, f"row_nonclaim_{len(checks)}", not truth(row.get("valid_for_full_MTS_claim", "false")), row.get("valid_for_full_MTS_claim", ""))
        add(checks, f"row_no_missing_{len(checks)}", "MISSING_" not in json.dumps(row), row.get(next(iter(row)), ""))

    for row in normalization_rows:
        add(checks, f"normalization_{row['normalization_id']}", sp.sympify(row["exact_residual"]) == 0 and row["status"] == "EXACT", row["derived_value"])
    for row in soft_rows:
        add(checks, f"soft_{row['soft_id']}", sp.sympify(row["exact_residual"]) == 0 and truth(row["valid_for_soft_subtraction_claim"]), row["derived_value"])

    kernel_by_id = {row["kernel_id"]: row for row in kernel_rows}
    add(checks, "kernel_scale", kernel_by_id["KERNEL4988_07_scale_linear"]["coefficient"] == "-203(x^2-x+1)/320", kernel_by_id["KERNEL4988_07_scale_linear"]["coefficient"])
    add(checks, "kernel_no_L2", kernel_by_id["KERNEL4988_08_scale_quadratic"]["coefficient"] == "0", kernel_by_id["KERNEL4988_08_scale_quadratic"]["coefficient"])
    add(checks, "kernel_identity", kernel_by_id["KERNEL4988_09_full_identity"]["coefficient"] == "0", kernel_by_id["KERNEL4988_09_full_identity"]["coefficient"])

    generator = random.Random(4988)
    for event in range(48):
        s_value = Fraction(generator.randint(1, 101), generator.randint(1, 37))
        t_value = Fraction(-generator.randint(1, 101), generator.randint(1, 37))
        u_value = -s_value - t_value
        if u_value == 0:
            t_value -= Fraction(1, 113)
            u_value = -s_value - t_value
        old = Fraction(1, 2) * ((t_value**2 + u_value**2) / s_value + (s_value**2 + u_value**2) / t_value + (s_value**2 + t_value**2) / u_value)
        canonical = t_value * u_value / s_value + s_value * u_value / t_value + s_value * t_value / u_value
        add(checks, f"tree_identity_{event:03d}", old + canonical == 0, f"residual={old + canonical}")

    mp.mp.dps = 80
    maximum_kernel_residual = mp.mpf(0)
    for event in range(96):
        value = mp.mpf(generator.randint(5, 995)) / 1000
        scale_log = mp.mpf(generator.randint(-800, 800)) / 137
        direct = hard_direct(value, scale_log)
        decomposed = hard_decomposed(value, scale_log)
        residual = abs(direct - decomposed)
        maximum_kernel_residual = max(maximum_kernel_residual, residual)
        add(checks, f"kernel_point_{event:03d}", residual < mp.mpf("1e-68"), mp.nstr(residual, 10))

    for exponent in (8, 12, 16, 20):
        epsilon = mp.mpf(10) ** (-exponent)
        for side, value, factor in (("left", epsilon, epsilon), ("right", 1 - epsilon, epsilon)):
            raw = hard_decomposed(value, mp.mpf("1.75")) - mp.pi**2 / (16 * value * (1 - value))
            raw_residual = abs(factor * raw + mp.pi**2 / 16)
            regular_residue = abs(factor * hard_decomposed(value, mp.mpf("1.75")))
            tolerance = mp.mpf(10) ** (-exponent + 2) * exponent**2
            add(checks, f"endpoint_raw_{side}_{exponent}", raw_residual < tolerance, mp.nstr(raw_residual, 10))
            add(checks, f"endpoint_reg_{side}_{exponent}", regular_residue < tolerance, mp.nstr(regular_residue, 10))

    expected_partial = {
        "PW4988_J0_TOTAL": sp.Rational(18161, 34560) + 13 * sp.pi**2 / 288,
        "PW4988_J2_TOTAL": -sp.Rational(621877, 864000) + 173 * sp.pi**2 / 1440,
    }
    partial_by_id = {row["integral_id"]: row for row in partial_rows}
    for row_id, expected in expected_partial.items():
        recorded_expression = sp.sympify(partial_by_id[row_id]["exact_integral"])
        recorded_constant = recorded_expression.subs(sp.Symbol("L"), 0)
        add(checks, f"partial_exact_{row_id}", sp.simplify(recorded_constant - expected) == 0, str(recorded_constant))
        add(checks, f"partial_zeta_{row_id}", partial_by_id[row_id]["zeta3_coefficient"] == "0", partial_by_id[row_id]["zeta3_coefficient"])

    exact_h = {
        0: (sp.Rational(18161, 34560) + 13 * sp.pi**2 / 288, -sp.Rational(203, 384)),
        2: (-sp.Rational(621877, 864000) + 173 * sp.pi**2 / 1440, -sp.Rational(203, 9600)),
    }
    for scale_text in ("-2.75", "0.625", "4.0"):
        scale_log = mp.mpf(scale_text)
        for spin in (0, 2):
            numeric = quadrature(spin, scale_log)
            exact_expr = exact_h[spin][0] + exact_h[spin][1] * sp.Rational(scale_text)
            exact = mp.mpf(str(sp.N(exact_expr, 85)))
            residual = abs(numeric - exact)
            add(checks, f"quadrature_J{spin}_L{scale_text}", residual < mp.mpf("1e-55"), mp.nstr(residual, 12))

    projection_by_quantity = {row["quantity"]: row for row in projection_rows}
    expected_projection = {
        "d0_phi(L)": 143 * (120 * sp.pi**2 + 1397) / (6480 * sp.pi),
        "d2_phi(L)": (-621877 + 103800 * sp.pi**2) / (162000 * sp.pi),
        "A_phi(L=0)": (242911 + 29600 * sp.pi**2) / (9000 * sp.pi),
        "B_phi(L=0)": (621877 - 103800 * sp.pi**2) / (27000 * sp.pi),
        "Delta K_mu_phi(L)": (-135061 + 1500 * sp.pi**2) / (450 * sp.pi),
        "Delta K_ang_phi(L)": (13357 + 24075 * sp.pi**2) / (3375 * sp.pi),
    }
    for quantity, expected in expected_projection.items():
        recorded = sp.sympify(projection_by_quantity[quantity]["constant_L0"])
        add(checks, f"projection_{quantity}", sp.simplify(recorded - expected) == 0, str(recorded))
        add(checks, f"projection_partial_only_{quantity}", not truth(projection_by_quantity[quantity]["valid_for_full_K_claim"]), projection_by_quantity[quantity]["valid_for_full_K_claim"])

    gates = {row["gate"]: truth(row["passed"]) for row in gate_rows}
    expected_open = {
        "global_D1F1_subtraction",
        "opposite_helicity_hh_cut",
        "mixed_hhh_cut",
        "phiphih_cut",
        "numeric_full_K_mu",
        "numeric_full_K_ang",
        "exact_all_operator_local_GR",
        "full_MTS",
    }
    add(checks, "open_gate_set", {name for name, passed in gates.items() if not passed} == expected_open, json.dumps(sorted(name for name, passed in gates.items() if not passed)))
    add(checks, "scalar_subtotal_checkpoint_claim", truth(next(row for row in gate_rows if row["gate"] == "scalar_cut_invariant_subtotal")["claim_allowed"]), "scalar-cut subtotal derived but full invariant remains guarded")
    add(checks, "master_cut_factor_two", result["projection"]["master_cut_weight"] == "-U_phiphi/(pi s^3)=2 D_phiphi", result["projection"]["master_cut_weight"])
    add(checks, "result_full_K_mu_false", result["projection"]["numeric_full_K_mu"] is False, str(result["projection"]["numeric_full_K_mu"]))
    add(checks, "result_full_K_ang_false", result["projection"]["numeric_full_K_ang"] is False, str(result["projection"]["numeric_full_K_ang"]))

    for source_path, expected_hash in result["source_hashes"].items():
        path = ROOT / source_path
        add(checks, f"source_exists_{len(checks)}", path.exists(), source_path)
        if path.exists():
            add(checks, f"source_hash_{len(checks)}", digest(path) == expected_hash, source_path)

    add(checks, "maximum_kernel_residual", maximum_kernel_residual < mp.mpf("1e-68"), mp.nstr(maximum_kernel_residual, 12))
    write_validation(checks)
    passed = sum(bool(row["passed"]) for row in checks)
    VALIDATION_PROVENANCE.write_text(
        "\n".join(
            [
                "# 4988 independent validation provenance",
                "",
                f"Marker: `{VALIDATION_MARKER}`.",
                "",
                "The validator does not import the generator. It rebuilds the canonical crossing identity on 48 rational events, compares the direct and decomposed hard kernels on 96 high-precision points, tests both endpoint residues at four scales, repeats transformed endpoint quadrature at six unseen `(J,L)` points, checks exact partial waves and raw `-U/(2pi)` scalar-cut projector coordinates, verifies the master factor of two, verifies every source hash, and enforces all full-invariant nonclaim gates.",
                "",
                f"Passed: `{passed}/{len(checks)}`.",
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
                "maximum_kernel_residual": mp.nstr(maximum_kernel_residual, 12),
                "output": str(VALIDATION),
            },
            indent=2,
        )
    )
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
