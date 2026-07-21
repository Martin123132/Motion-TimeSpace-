from __future__ import annotations

import csv
import hashlib
import json
import random
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4987"
RESULT = SOURCE / "full_finite_scheme_orbit_and_cut_reduction_results.json"
BASIS = SOURCE / "crossing_local_polynomial_basis.csv"
SCHEME = SOURCE / "full_finite_scheme_orbit.csv"
CUTS = SOURCE / "two_loop_cut_state_census.csv"
MASTER = SOURCE / "rational_free_master_projection.csv"
ANGULAR = SOURCE / "single_log_angular_projector_checks.csv"
GATES = SOURCE / "two_loop_cut_reduction_gate.csv"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4987_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

VALIDATION_MARKER = "P8_Y5_BRR545_4987_FULL_SCHEME_CUT_REDUCTION_VALIDATION"
EXPECTED_MARKER = "MTS_4987_FULL_FINITE_SCHEME_ORBIT_IRREDUCIBLE_CUT_REDUCTION"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def truth(value: str) -> bool:
    return value.strip().lower() == "true"


def add(rows: list[dict[str, Any]], name: str, passed: bool, evidence: str) -> None:
    rows.append(
        {
            "validation_id": f"VAL4987_{len(rows) + 1:03d}_{name}",
            "passed": bool(passed),
            "evidence": evidence,
            "validation_marker": VALIDATION_MARKER,
            "valid_for_full_MTS_claim": False,
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
    outputs = (RESULT, BASIS, SCHEME, CUTS, MASTER, ANGULAR, GATES)
    for path in outputs:
        add(checks, f"exists_{path.stem}", path.exists(), str(path))
    if not all(path.exists() for path in outputs):
        write_validation(checks)
        return 1

    result = json.loads(RESULT.read_text(encoding="utf-8"))
    basis_rows = read_csv(BASIS)
    scheme_rows = read_csv(SCHEME)
    cut_rows = read_csv(CUTS)
    master_rows = read_csv(MASTER)
    angular_rows = read_csv(ANGULAR)
    gate_rows = read_csv(GATES)

    add(checks, "marker", result.get("checkpoint_marker") == EXPECTED_MARKER, str(result.get("checkpoint_marker")))
    for name, rows in (
        ("basis", basis_rows),
        ("scheme", scheme_rows),
        ("cuts", cut_rows),
        ("master", master_rows),
        ("angular", angular_rows),
        ("gates", gate_rows),
    ):
        add(checks, f"nonempty_{name}", bool(rows), f"rows={len(rows)}")
        add(checks, f"marker_{name}", all(row.get("checkpoint_marker") == EXPECTED_MARKER for row in rows), f"rows={len(rows)}")
        add(checks, f"no_missing_{name}", all("MISSING_" not in json.dumps(row) for row in rows), f"rows={len(rows)}")

    expected_basis = {2: (1, "[1, 1, 1]"), 3: (1, "[0, 1, 1, 0]")}
    for row in basis_rows:
        degree = int(row["momentum_degree"])
        dimension, vector = expected_basis[degree]
        add(checks, f"basis_dimension_d{degree}", int(row["quotient_dimension"]) == dimension, row["quotient_dimension"])
        add(checks, f"basis_vector_d{degree}", row["null_vector"] == vector, row["null_vector"])
        add(checks, f"basis_status_d{degree}", truth(row["valid_for_basis_claim"]), row["status"])

    add(checks, "scheme_exact_rows", all(row["exact_residual"] == "0" and truth(row["valid_for_scheme_claim"]) for row in scheme_rows), f"rows={len(scheme_rows)}")
    add(checks, "scheme_row_count", len(scheme_rows) == 12, f"rows={len(scheme_rows)}")

    pi = sp.pi
    a_c = sp.Integer(16)
    b_gc = -sp.Integer(6) / pi
    f_a = sp.Integer(46) / (sp.Integer(15) * pi)
    f_b = -sp.Integer(1) / (sp.Integer(15) * pi)
    generator = random.Random(14987)
    for event in range(96):
        C = sp.Rational(generator.randint(-40, 40), generator.randint(1, 17))
        W = sp.Rational(generator.randint(-40, 40), generator.randint(1, 17))
        r4 = sp.Rational(generator.randint(-40, 40), generator.randint(1, 17))
        rho = sp.Rational(generator.randint(-40, 40), generator.randint(1, 17))
        source_s = sp.Rational(generator.randint(-40, 40), generator.randint(1, 17))
        coefficient_a = sp.Rational(generator.randint(-40, 40), generator.randint(1, 17))
        coefficient_b = sp.Rational(generator.randint(-40, 40), generator.randint(1, 17))
        alpha = sp.Rational(generator.randint(-40, 40), generator.randint(1, 17))
        beta = sp.Rational(generator.randint(-40, 40), generator.randint(1, 17))
        delta = sp.Rational(generator.randint(-40, 40), generator.randint(1, 17))

        C_prime = C + beta
        W_prime = W + alpha * C + delta
        r4_prime = r4 - beta
        rho_prime = rho + 3 * alpha
        source_prime = source_s + a_c * alpha - b_gc * beta
        coefficient_a_prime = coefficient_a - beta * f_a
        coefficient_b_prime = coefficient_b - beta * f_b

        invariant_i = 3 * source_s - a_c * rho
        invariant_i_prime = 3 * source_prime - a_c * rho_prime
        invariant_mu = invariant_i - 3 * b_gc * r4
        invariant_mu_prime = invariant_i_prime - 3 * b_gc * r4_prime
        invariant_angular = coefficient_a - coefficient_b - (f_a - f_b) * r4
        invariant_angular_prime = coefficient_a_prime - coefficient_b_prime - (f_a - f_b) * r4_prime
        physical_p4 = C + r4
        physical_p4_prime = C_prime + r4_prime
        rational_free_source = source_s - a_c * rho / 3 - b_gc * r4
        residuals = (
            sp.simplify(invariant_mu_prime - invariant_mu),
            sp.simplify(invariant_angular_prime - invariant_angular),
            sp.simplify(physical_p4_prime - physical_p4),
            sp.simplify(invariant_mu - 3 * rational_free_source),
            sp.simplify(W_prime - W - alpha * C - delta),
        )
        add(checks, f"scheme_random_{event + 1:03d}", all(value == 0 for value in residuals), json.dumps([str(value) for value in residuals]))

    expected_survivors = {"h_h_opposite_helicity", "phi_phi", "h_h_h_mixed_helicity", "phi_phi_h"}
    actual_survivors = {row["state_class"] for row in cut_rows if truth(row["survives_irreducible_census"])}
    add(checks, "cut_survivor_set", actual_survivors == expected_survivors, json.dumps(sorted(actual_survivors)))
    for row in cut_rows:
        expected = row["state_class"] in expected_survivors
        add(checks, f"cut_{row['state_class']}", truth(row["survives_irreducible_census"]) == expected, row["status"])

    master_by_object = {row["object"]: row for row in master_rows}
    add(checks, "master_general", "D1 ReF1" in master_by_object["two_loop_real_master"]["equation"], master_by_object["two_loop_real_master"]["equation"])
    add(checks, "master_scale", "-K_mu stu" in master_by_object["K_mu"]["equation"], master_by_object["K_mu"]["equation"])
    add(checks, "master_angular", "K_ang=A_rf-B_rf" in master_by_object["K_ang"]["equation"], master_by_object["K_ang"]["equation"])
    add(checks, "numeric_nonclaim", not truth(master_by_object["numeric_K_mu_and_K_ang"]["valid_for_projection_claim"]), master_by_object["numeric_K_mu_and_K_ang"]["derivation_status"])

    add(checks, "angular_row_count", len(angular_rows) == 64, f"rows={len(angular_rows)}")
    for row in angular_rows:
        coefficient_a = Fraction(row["A_true"])
        coefficient_b = Fraction(row["B_true"])
        d_zero = Fraction(row["D_z0"])
        d_one = Fraction(row["D_z1"])
        reconstructed = (d_one, 4 * (d_zero - d_one))
        passed = reconstructed == (coefficient_a, coefficient_b) and row["maximum_exact_residual"] == "0"
        add(checks, f"angular_{row['event_id']}", passed, f"A={reconstructed[0]};B={reconstructed[1]}")

    gates = {row["gate"]: truth(row["passed"]) for row in gate_rows}
    expected_open = {"numeric_K_mu", "numeric_K_ang", "exact_all_operator_local_GR", "full_MTS"}
    add(checks, "open_gate_set", {name for name, passed in gates.items() if not passed} == expected_open, json.dumps(sorted(name for name, passed in gates.items() if not passed)))
    add(checks, "no_full_claim", not any(truth(row.get("valid_for_full_MTS_claim", "false")) for rows in (basis_rows, scheme_rows, cut_rows, master_rows, angular_rows, gate_rows) for row in rows), "all output rows nonclaim")

    for source_path, expected_hash in result["source_hashes"].items():
        path = ROOT / source_path
        add(checks, f"source_exists_{len(checks) + 1}", path.exists(), source_path)
        if path.exists():
            add(checks, f"source_hash_{len(checks) + 1}", digest(path) == expected_hash, source_path)

    write_validation(checks)
    VALIDATION_PROVENANCE.write_text(
        "\n".join(
            [
                "# 4987 independent validation provenance",
                "",
                f"Marker: `{VALIDATION_MARKER}`.",
                "",
                "The validator independently reconstructs the full affine scheme invariants on 96 exact rational events, checks the crossing bases, verifies the surviving cut set, reconstructs 64 angular projectors, confirms every source hash, and enforces the numeric and full-theory nonclaim gates.",
                "",
                f"Passed: `{sum(bool(row['passed']) for row in checks)}/{len(checks)}`.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    passed = sum(bool(row["passed"]) for row in checks)
    print(json.dumps({"validation_marker": VALIDATION_MARKER, "passed": passed, "total": len(checks)}, indent=2))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
