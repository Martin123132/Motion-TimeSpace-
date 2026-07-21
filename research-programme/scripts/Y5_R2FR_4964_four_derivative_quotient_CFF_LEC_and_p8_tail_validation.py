from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4964"
OUTPUT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_4964_VALIDATION.csv"
)

MAIN_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_4964_four_derivative_quotient_CFF_LEC_and_p8_tail.py"
)
RESULT_JSON = SOURCE / "four_derivative_quotient_CFF_p8_results.json"
QUOTIENT_CSV = SOURCE / "four_derivative_field_redefinition_quotient.csv"
PARAMETER_CSV = SOURCE / "finite_matching_parameter_count.csv"
CFF_CSV = SOURCE / "CFF_one_LEC_calibration_contract.csv"
P8_CSV = SOURCE / "p8plus_tail_norm_gate.csv"
DECISION_CSV = SOURCE / "compact_all_operator_decision.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"

CHECKPOINT = (
    POST
    / "4964-Y5-R2FR-four-derivative-redundant-quotient-CFF-one-LEC-contract-and-p8-tail-norm-or-all-operator-compact-GR-boundary.md"
)
FORMAL_NOTE = (
    FORMAL
    / "980-PPC4161-four-derivative-quotient-CFF-one-LEC-and-p8-tail-boundary.md"
)
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
LOCAL_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

MARKER = "MTS_4964_R2C2_QUOTIENT_CFF_LEC_P8_TAIL"
FORMAL_MARKER = "PPC4161_R2C2_QUOTIENT_CFF_LEC_P8_TAIL_4964"

C_LIGHT = 299_792_458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054_571_817e-34
M_SUN_KG = 1.98847e30
PLANCK_LENGTH_M = math.sqrt(HBAR * G_NEWTON / C_LIGHT**3)
SOLAR_MASS_LENGTH_M = G_NEWTON * M_SUN_KG / C_LIGHT**2

HASH_LOCKS = {
    MAIN_SCRIPT: "d47b3cbc8481b89cc1da5c28142daecfa60409be6afce2ef17b64f846aa0f40b",
    RESULT_JSON: "752b62cf5f236860739d4200c3c3fbaa52952187a8db06e71fa98051b2fa2b04",
    QUOTIENT_CSV: "c318f963778a37e56b3c68d250f32a55b3abe83ebb5f0f4134c36f5073da9551",
    PARAMETER_CSV: "82d4178a1f7f983e47726451502f131075ecbd5b5905c31d068402f83828bd02",
    CFF_CSV: "bd96a132e80647ac4f106a8c026afba3a8f4060d095fda3451cbbaac21d8236c",
    P8_CSV: "a17f8fc7c652fec0b9a33985fe7c23045073114784bc2304a084ad4ca057510f",
    DECISION_CSV: "b49701343c9865d2e8bc899c05ac2c8ca3ad7e837aedac40fc8f46a7654b00b9",
    PROVENANCE: "9789d6f90d27c05628adc6e4812fdde7905e77d884ca900ce524fd68d65df356",
    CHECKPOINT: "8bcfe51f2960789c575c0b4f9c85e65a6ca83be6a8a49c689e58c3180d4c8f57",
    FORMAL_NOTE: "52457851a4e3c66449ad7a8427f62737979fcea30f9afbd24f3412c7ce984631",
    CLAIMS: "8e28a99b29b20c33a9913f5e2c677faf5571ec48ee69428a05780b157b07112a",
    VARIABLES: "1863f6faad8b96322d0af3b3f8a1ab52f23e801391c2eca9c4ee46b9c067311d",
    EQUATIONS: "8a82466daaba0d752504a868035e245860c7f4260531b3d43506ce47e88c61d8",
    RED_TEAM: "abf171c9813848498e71a899fb144bdae0b88b7d07ba12467af87ef67b600e7d",
    SPINE: "602048dbf6582971aeaefb378a41107a941b88bdb5e247628523d8c83546fd9b",
    RESUME: "1e976a66d59dfbcce31edb158f636f666bad05ca51e610220950f864d95e5a8e",
    LOCAL_SPINE: "627132b8d32e2310cec5951999021b95c5796d4f0168d8bf0c692432be5d9c82",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def truth(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def close(actual: float, expected: float, tolerance: float = 1.0e-12) -> bool:
    return math.isclose(actual, expected, rel_tol=tolerance, abs_tol=1.0e-300)


def add(
    rows: list[dict[str, Any]],
    check_id: str,
    test: str,
    expected: Any,
    actual: Any,
    passed: bool,
) -> None:
    rows.append(
        {
            "validation_id": check_id,
            "test": test,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "status": "PASS" if passed else "FAIL",
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
        }
    )


def malformed(rows: list[dict[str, str]]) -> bool:
    return any(None in row or any(value is None for value in row.values()) for row in rows)


def main() -> int:
    checks: list[dict[str, Any]] = []

    missing = [str(path) for path in HASH_LOCKS if not path.exists()]
    add(checks, "V4964_00", "all locked files exist", [], missing, not missing)

    bad_hashes = {
        str(path.relative_to(ROOT)): {
            "expected": expected,
            "actual": digest(path),
        }
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "V4964_01", "all locked hashes match", {}, bad_hashes, not bad_hashes)

    result = json.loads(text(RESULT_JSON))
    quotient_rows = read_csv(QUOTIENT_CSV)
    parameter_rows = read_csv(PARAMETER_CSV)
    CFF_rows = read_csv(CFF_CSV)
    p8_rows = read_csv(P8_CSV)
    decision_rows = read_csv(DECISION_CSV)
    generated_tables = [
        quotient_rows,
        parameter_rows,
        CFF_rows,
        p8_rows,
        decision_rows,
    ]
    add(
        checks,
        "V4964_02",
        "generated CSVs parse without malformed rows",
        True,
        not any(malformed(rows) for rows in generated_tables),
        not any(malformed(rows) for rows in generated_tables),
    )

    all_generated_rows = [row for rows in generated_tables for row in rows]
    tags_ok = all(
        row.get("checkpoint_marker") == MARKER
        and not truth(row.get("valid_for_full_MTS_claim", ""))
        for row in all_generated_rows
    )
    add(checks, "V4964_03", "all generated rows retain nonclaim tags", True, tags_ok, tags_ok)

    missing_tokens = [
        token
        for token in ("MISSING_", "PLACEHOLDER", "TODO_NUMERIC")
        if any(token in " ".join(row.values()) for row in all_generated_rows)
    ]
    add(checks, "V4964_04", "no placeholder tokens in generated evidence", [], missing_tokens, not missing_tokens)

    a_R, a_C = sp.symbols("a_R a_C")
    ricci_squared, scalar_squared = sp.symbols("Ricci2 R2")
    local_four = 2 * a_C * ricci_squared + (a_R - sp.Rational(2, 3) * a_C) * scalar_squared
    alpha = -2 * a_C
    beta = a_R + sp.Rational(1, 3) * a_C
    delta_eh = alpha * (ricci_squared - scalar_squared / 2) - beta * scalar_squared
    cancellation = sp.simplify(local_four + delta_eh)
    add(checks, "V4964_05", "independent symbolic R2/C2 cancellation", 0, cancellation, cancellation == 0)

    M_R2 = sp.symbols("M_R2", nonzero=True)
    stress_squared, trace_squared = sp.symbols("Tmn2 T2")
    direct_contact = (
        -alpha * (stress_squared - trace_squared / 2) + beta * trace_squared
    ) / M_R2**2
    expected_contact = (
        2 * a_C * stress_squared
        + (a_R - sp.Rational(2, 3) * a_C) * trace_squared
    ) / M_R2**2
    contact_remainder = sp.simplify(direct_contact - expected_contact)
    add(checks, "V4964_06", "independent matter-contact identity", 0, contact_remainder, contact_remainder == 0)

    quotient_by_id = {row["quotient_id"]: row for row in quotient_rows}
    quotient_pass = len(quotient_rows) == 7 and all(truth(row["passed"]) for row in quotient_rows)
    add(checks, "V4964_07", "seven quotient theorem rows pass", "7/7", f"{sum(truth(row['passed']) for row in quotient_rows)}/{len(quotient_rows)}", quotient_pass)
    add(
        checks,
        "V4964_08",
        "vacuum p4 parameter count reduced to zero",
        0,
        result["four_derivative_quotient"]["independent_neutral_vacuum_p4_parameters"],
        result["four_derivative_quotient"]["independent_neutral_vacuum_p4_parameters"] == 0
        and quotient_by_id["Q4964_04_vacuum_observable_count"]["status"]
        == "PURE_VACUUM_PARAMETER_COUNT_REDUCED_2_TO_0",
    )

    parameters = {row["parameter_id"]: row for row in parameter_rows}
    W_status = parameters["PAR4964_06_Wplus_Wminus"]["current_status"]
    add(checks, "V4964_09", "Wplus/Wminus are not gravitational R2/C2", "NOT_GRAVITATIONAL_AR_AC", W_status, W_status == "NOT_GRAVITATIONAL_AR_AC")

    CFF_by_id = {row["contract_id"]: row for row in CFF_rows}
    add(
        checks,
        "V4964_10",
        "CFF action equation and stress retain one coefficient",
        1,
        result["CFF_one_LEC_contract"]["retained_independent_CFF_LECs"],
        result["CFF_one_LEC_contract"]["retained_independent_CFF_LECs"] == 1
        and truth(CFF_by_id["CFF4964_03_equation_stress"]["valid_for_declared_structure"]),
    )
    add(
        checks,
        "V4964_11",
        "physical CFF numeric calibration remains open",
        False,
        result["CFF_one_LEC_contract"]["physical_cIR_calibrated"],
        not result["CFF_one_LEC_contract"]["physical_cIR_calibrated"]
        and not truth(CFF_by_id["CFF4964_05_calibration"]["valid_for_numeric_CFF_claim"]),
    )
    add(
        checks,
        "V4964_12",
        "flat Maxwell remains exact for arbitrary cIR",
        True,
        result["CFF_one_LEC_contract"]["flat_Maxwell_exact"],
        result["CFF_one_LEC_contract"]["flat_Maxwell_exact"]
        and truth(CFF_by_id["CFF4964_04_flat_Maxwell"]["valid_for_numeric_CFF_claim"]),
    )

    compact_rows = [row for row in p8_rows if row["row_type"] == "compact_object_gate"]
    add(checks, "V4964_13", "eleven compact p8 rows", 11, len(compact_rows), len(compact_rows) == 11)

    recomputation_failures: list[str] = []
    for row in compact_rows:
        mass_length = float(row["mass_Msun"]) * SOLAR_MASS_LENGTH_M
        chi = PLANCK_LENGTH_M**2 * mass_length / float(row["radius_m"]) ** 3
        budget = 0.01 * (1.0 - chi) / chi**3
        equivalent_length = PLANCK_LENGTH_M * budget ** (1.0 / 6.0)
        if not (
            close(float(row["mass_length_m"]), mass_length)
            and close(float(row["chi_lP2_curvature"]), chi)
            and close(float(row["C8_max_if_R_equals_1"]), budget)
            and close(float(row["response_equivalent_length_at_R1_m"]), equivalent_length)
        ):
            recomputation_failures.append(row["object_id"])
    add(checks, "V4964_14", "independent compact chi and C8 recomputation", [], recomputation_failures, not recomputation_failures)

    tightest = min(compact_rows, key=lambda row: float(row["C8_max_if_R_equals_1"]))
    tightest_budget = float(tightest["C8_max_if_R_equals_1"])
    add(
        checks,
        "V4964_15",
        "tightest p8 budget and owner",
        "SLY4_near_turning_0p99_Mmax;3.027551244686395e232",
        f"{tightest['object_id']};{tightest_budget:.16e}",
        tightest["object_id"] == "SLY4_near_turning_0p99_Mmax"
        and close(tightest_budget, 3.027551244686395e232),
    )

    tail_statuses = {row["row_type"]: row["status"] for row in p8_rows if row["row_type"] != "compact_object_gate"}
    add(
        checks,
        "V4964_16",
        "tail theorem and finite-truncation firewall present",
        {"tail_theorem", "nonidentifiability_theorem"},
        set(tail_statuses),
        tail_statuses.get("tail_theorem") == "EXACT_CONDITIONAL_GEOMETRIC_SERIES_BOUND"
        and tail_statuses.get("nonidentifiability_theorem") == "P6_DATA_CANNOT_PROVE_P8_TAIL_WITHOUT_UV_INPUT",
    )
    add(
        checks,
        "V4964_17",
        "parent C8 and radius remain unclaimed",
        "False;False",
        f"{result['p8plus_tail_gate']['parent_C8_bound_available']};{result['p8plus_tail_gate']['parent_R_bound_available']}",
        not result["p8plus_tail_gate"]["parent_C8_bound_available"]
        and not result["p8plus_tail_gate"]["parent_R_bound_available"],
    )

    decisions = {row["decision_id"]: row for row in decision_rows}
    expected_decisions = {
        "DEC4964_00_R2C2_quotient": "NO",
        "DEC4964_01_R2C2_vacuum_obstruction": "NO_AT_FIRST_EFT_ORDER",
        "DEC4964_02_matter_contact_matching": "NO",
        "DEC4964_03_CFF_count": "YES",
        "DEC4964_04_CFF_numeric": "NO",
        "DEC4964_05_p8_tail_formula": "YES_CONDITIONAL",
        "DEC4964_06_p8_parent_bound": "NO",
        "DEC4964_07_order_by_order_compact_GR": "YES_WITHIN_DECLARED_STATIC_P6_DOMAIN",
        "DEC4964_08_all_operator_compact_GR": "NO",
        "DEC4964_09_full_MTS": "NO",
    }
    decision_failures = {
        key: decisions.get(key, {}).get("decision")
        for key, expected in expected_decisions.items()
        if decisions.get(key, {}).get("decision") != expected
    }
    add(checks, "V4964_18", "decision matrix matches scoped verdicts", {}, decision_failures, not decision_failures)

    result_checks = result["checks"]
    add(
        checks,
        "V4964_19",
        "generator internal checks all pass",
        f"{len(result_checks)}/{len(result_checks)}",
        f"{sum(result_checks.values())}/{len(result_checks)}",
        all(result_checks.values()),
    )

    source_path_failures: list[str] = []
    for row in p8_rows + CFF_rows:
        source_path = row.get("source_path", "")
        if source_path and not (ROOT / Path(source_path)).exists():
            source_path_failures.append(source_path)
    add(checks, "V4964_20", "every emitted source path exists", [], source_path_failures, not source_path_failures)

    claims = read_csv(CLAIMS)
    claim_rows = [row for row in claims if row["claim_id"] == "L-806"]
    add(
        checks,
        "V4964_21",
        "claim register contains exactly one scoped L-806",
        1,
        len(claim_rows),
        len(claim_rows) == 1
        and "all-operator" in claim_rows[0]["risk"]
        and "full MTS" in claim_rows[0]["risk"],
    )

    variables = read_csv(VARIABLES)
    required_symbols = {
        "R2C2VacuumQuotient4964_MTS",
        "StressContactInvariant4964_MTS",
        "CFFOneLEC4964_MTS",
        "chi_p8_4964",
        "C8Tail4964_MTS",
        "PredictivityStatus4964_MTS",
    }
    present_symbols = {row["symbol"] for row in variables}
    add(checks, "V4964_22", "six canonical 4964 variable rows present", required_symbols, required_symbols & present_symbols, required_symbols <= present_symbols)

    marker_files = [CHECKPOINT, FORMAL_NOTE, EQUATIONS, RED_TEAM, SPINE, RESUME, LOCAL_SPINE]
    marker_failures = [str(path.relative_to(ROOT)) for path in marker_files if FORMAL_MARKER not in text(path)]
    add(checks, "V4964_23", "formal marker propagated to all handoff files", [], marker_failures, not marker_failures)

    resume_text = text(RESUME)
    add(
        checks,
        "V4964_24",
        "resume points to checkpoint 4964 and next p8 target",
        True,
        "Last checkpoint: `4964" in resume_text and "checkpoint 4965" in resume_text,
        "Last checkpoint: `4964" in resume_text and "checkpoint 4965" in resume_text,
    )

    claim_scope = result["claim_scope"]
    scope_ok = (
        not claim_scope["R2C2_independent_vacuum_p4_obstruction"]
        and not claim_scope["R2C2_full_matter_contact_matching"]
        and claim_scope["CFF_one_LEC_structure"]
        and not claim_scope["CFF_numeric_calibration"]
        and claim_scope["compact_GR_through_declared_static_p6_domain"]
        and not claim_scope["p8plus_parent_bound"]
        and not claim_scope["all_operator_compact_GR"]
        and not claim_scope["full_MTS"]
    )
    add(checks, "V4964_25", "claim scope retains every required boundary", True, scope_ok, scope_ok)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    passed = sum(truth(row["passed"]) for row in checks)
    print(f"{FORMAL_MARKER}_VALIDATION={passed}/{len(checks)}", flush=True)
    print(f"{FORMAL_MARKER}_OUTPUT={OUTPUT}", flush=True)
    if passed != len(checks):
        failures = [row["validation_id"] for row in checks if not truth(row["passed"])]
        print(f"{FORMAL_MARKER}_FAILURES={failures}", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
