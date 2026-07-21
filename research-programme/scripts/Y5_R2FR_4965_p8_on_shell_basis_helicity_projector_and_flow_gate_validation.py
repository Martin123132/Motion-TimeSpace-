from __future__ import annotations

import ast
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
SOURCE = POST / "source-intake" / "functional_rg" / "4965"
OUTPUT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_4965_VALIDATION.csv"
)

MAIN_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_4965_p8_on_shell_basis_helicity_projector_and_flow_gate.py"
)
RESULT_JSON = SOURCE / "p8_basis_projector_and_partial_flow_results.json"
BASIS_CSV = SOURCE / "p8_on_shell_basis.csv"
PROJECTOR_CSV = SOURCE / "p8_helicity_projector.csv"
MOTION_SOURCE_CSV = SOURCE / "p8_minimal_motion_scalar_source.csv"
POWER_COUNT_CSV = SOURCE / "p8_parent_source_power_count.csv"
DISPERSIVE_CSV = SOURCE / "p8_C3_dispersive_cone.csv"
COMPACT_CSV = SOURCE / "p8_two_coordinate_compact_domain.csv"
DECISION_CSV = SOURCE / "p8_flow_decision.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"

CHECKPOINT = (
    POST
    / "4965-Y5-R2FR-minimal-Ricci-flat-p8-on-shell-basis-helicity-projector-and-parent-flow-source-or-order-by-order-EFT-boundary.md"
)
FORMAL_NOTE = (
    FORMAL
    / "981-PPC4161-Ricci-flat-p8-basis-helicity-projector-and-motion-source-boundary.md"
)
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
LOCAL_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

MARKER = "MTS_4965_P8_BASIS_HELICITY_PARTIAL_FLOW"
FORMAL_MARKER = "PPC4161_P8_BASIS_HELICITY_MOTION_SOURCE_4965"

HASH_LOCKS = {
    MAIN_SCRIPT: "08f57edfcb138f3521e5f64d0ba1155e24f8b844f131a78f8058bdcb19f3bc08",
    RESULT_JSON: "74ca1417cd82738e3e46af0f2e0525cd1084646917a01876ffd2bd19371dd989",
    BASIS_CSV: "46a99a91812cbc7af7ce6a5fcd0bc67b90112f0731c1c54631c0526eee392a61",
    PROJECTOR_CSV: "d87515661b135507302dc9b3dc8a4fb4888c36f264f1f5385c7ad687a2ad6a3f",
    MOTION_SOURCE_CSV: "617a4decd95b17e4b111a6d3ae0f21fa87844a3027ea45ff34f1d60e9e324dc0",
    POWER_COUNT_CSV: "6a386fc1e022d1aeaeeb64f0804de8755d66e5eb2f36b9f609e70b863a83f8d6",
    DISPERSIVE_CSV: "4c2ecf2ab4d44ea3fbd33cc76eddec321648029b249e1f3f49ecbe9247f559fe",
    COMPACT_CSV: "25e8e5ac5b60c134863e0f8615aaadfb99456c9aa4bdb086ea742623351a32da",
    DECISION_CSV: "379522bb88a7267ba0e3aef8c80da6c65eda4b8c4e3fae2ac7b879f36ad0f601",
    PROVENANCE: "a25769f17ae95adf02012479d551c69c9fd3308b2417dcc481da86ad8c0bcdab",
    CHECKPOINT: "8816046146a785b34938f7386df924b2d318098cb6413430798cffc6da021774",
    FORMAL_NOTE: "a0838137c98b027912c0849215f9bfa526ffad75931caf6906ddb4312d12ccd8",
    CLAIMS: "02bcd5582f95947a8ed493c6e6b3a1ce337280e0ef0a4ab745709e781946a316",
    VARIABLES: "e6ab72642b161edb5b736b7186ad8e4eee08126169f729a318ededfac8bcb773",
    EQUATIONS: "7b20f2676482db4700d8c75726113f5c868a74653acbbb98cdc8b8e4c80afb5f",
    RED_TEAM: "61f9f51090f5d3c44b0ede1ed2061977c21356c05fb522b79c1f261dbd24116a",
    SPINE: "12813bcfb67bf08a972e11372e9c609fc6455fc99aea53db12e32df32fba5241",
    RESUME: "199ed7010a6efa4a2f2c247b19b096f493a45577d67a352bab1ce0d355df73dc",
    LOCAL_SPINE: "112a1cd1bda82e48a147084a60612ffc451bf1f370c5ad298919b270adac86ca",
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


def malformed(rows: list[dict[str, str]]) -> bool:
    return any(None in row or any(value is None for value in row.values()) for row in rows)


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


def write_output(rows: list[dict[str, Any]]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    checks: list[dict[str, Any]] = []

    missing = [str(path) for path in HASH_LOCKS if not path.exists()]
    add(checks, "V4965_00", "all locked files exist", [], missing, not missing)

    bad_hashes = {
        str(path.relative_to(ROOT)): {"expected": expected, "actual": digest(path)}
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "V4965_01", "all locked hashes match", {}, bad_hashes, not bad_hashes)

    syntax_errors: dict[str, str] = {}
    for path in (MAIN_SCRIPT, Path(__file__)):
        try:
            ast.parse(text(path), filename=str(path))
        except SyntaxError as error:
            syntax_errors[str(path)] = str(error)
    add(checks, "V4965_02", "generator and validator parse", {}, syntax_errors, not syntax_errors)

    result = json.loads(text(RESULT_JSON))
    basis_rows = read_csv(BASIS_CSV)
    projector_rows = read_csv(PROJECTOR_CSV)
    motion_rows = read_csv(MOTION_SOURCE_CSV)
    power_rows = read_csv(POWER_COUNT_CSV)
    dispersive_rows = read_csv(DISPERSIVE_CSV)
    compact_rows = read_csv(COMPACT_CSV)
    decision_rows = read_csv(DECISION_CSV)
    generated_tables = [
        basis_rows,
        projector_rows,
        motion_rows,
        power_rows,
        dispersive_rows,
        compact_rows,
        decision_rows,
    ]
    add(
        checks,
        "V4965_03",
        "all generated CSVs parse without malformed rows",
        True,
        not any(malformed(rows) for rows in generated_tables),
        not any(malformed(rows) for rows in generated_tables),
    )

    all_generated = [row for rows in generated_tables for row in rows]
    tags_ok = all(
        row.get("checkpoint_marker") == MARKER
        and not truth(row.get("valid_for_full_MTS_claim", ""))
        for row in all_generated
    )
    add(checks, "V4965_04", "all rows retain private nonclaim tags", True, tags_ok, tags_ok)

    bad_tokens = [
        token
        for token in ("MISSING_", "PLACEHOLDER", "TODO_NUMERIC")
        if any(token in " ".join(row.values()) for row in all_generated)
    ]
    add(checks, "V4965_05", "no placeholder tokens in evidence rows", [], bad_tokens, not bad_tokens)

    result_checks = result["checks"]
    failed_result_checks = [name for name, passed in result_checks.items() if not passed]
    add(checks, "V4965_06", "all generator checks pass", [], failed_result_checks, not failed_result_checks)

    C_L2, C_R2 = sp.symbols("C_L2 C_R2")
    X = C_L2 + C_R2
    Y = -sp.I * (C_L2 - C_R2)
    same = C_L2**2 + C_R2**2
    mixed = C_L2 * C_R2
    invariant_map_ok = (
        sp.simplify(X**2 - same - 2 * mixed) == 0
        and sp.simplify(Y**2 + same - 2 * mixed) == 0
        and sp.simplify(X * Y + sp.I * (C_L2**2 - C_R2**2)) == 0
    )
    add(checks, "V4965_07", "independent chiral-real invariant map", True, invariant_map_ok, invariant_map_ok)

    basis_summary = result["p8_basis"]
    basis_count_ok = (
        len(basis_rows) == 8
        and basis_summary["raw_chiral_monomial_count"] == 3
        and basis_summary["real_parity_even_rank"] == 2
        and basis_summary["real_parity_odd_rank_excluded"] == 1
        and basis_summary["derivative_p8_rank"] == 0
    )
    add(checks, "V4965_08", "complete p8 quotient count", "3 raw -> 2 even; D rank 0", basis_summary, basis_count_ok)

    even_rows = [row for row in basis_rows if truth(row["independent_parity_even_coordinate"])]
    add(checks, "V4965_09", "basis table marks exactly four representations of two even coordinates", 4, len(even_rows), len(even_rows) == 4)

    projector = sp.Matrix([[1, -1], [1, 1]])
    projector_ok = projector.rank() == 2 and projector.det() == 2 and projector.inv() * projector == sp.eye(2)
    add(checks, "V4965_10", "independent helicity projector rank and inverse", "rank 2 det 2", f"rank {projector.rank()} det {projector.det()}", projector_ok)

    channel_rows = [row for row in projector_rows if row["channel_id"] in {"H4965_00_all_plus", "H4965_01_double_minus"}]
    channel_matrix = sp.Matrix(
        [
            [int(row["coefficient_beta_C"]), int(row["coefficient_beta_tildeC"])]
            for row in channel_rows
        ]
    )
    add(checks, "V4965_11", "CSV helicity rows reproduce projector", projector.tolist(), channel_matrix.tolist(), channel_matrix == projector)

    mu = sp.symbols("mu", positive=True)
    A_scalar = 1 / (483840 * sp.pi**2 * mu**2)
    B_minus = 1 / (60480 * sp.pi * mu**4)
    B_plus = 1 / (50400 * sp.pi * mu**4)
    B_C = sp.simplify((B_minus + B_plus) / 2)
    B_tilde = sp.simplify((B_plus - B_minus) / 2)
    scalar_algebra_ok = (
        sp.simplify(B_plus / B_minus) == sp.Rational(6, 5)
        and sp.simplify(B_C / B_tilde) == 11
        and sp.simplify(B_minus / A_scalar**2) == 3870720 * sp.pi**3
        and sp.simplify(B_plus / A_scalar**2) == 4644864 * sp.pi**3
    )
    add(checks, "V4965_12", "independent minimal-scalar p8 algebra", True, scalar_algebra_ok, scalar_algebra_ok)

    motion_by_id = {row["source_id"]: row for row in motion_rows}
    scalar_rows_ok = (
        len(motion_rows) == 9
        and motion_by_id["S4965_02_scalar_Bminus"]["exact_formula"] == "1/(60480*pi*mu_psi^4)"
        and motion_by_id["S4965_03_scalar_Bplus"]["exact_formula"] == "1/(50400*pi*mu_psi^4)"
        and motion_by_id["S4965_08_scalar_internal_consistency_curve"]["status"] == "MINIMAL_SCALAR_C3_P8_SOURCE_RELATION_DERIVED"
        and all(not truth(row["valid_for_total_parent_prediction"]) for row in motion_rows)
    )
    add(checks, "V4965_13", "nine motion source rows preserve partial-source scope", True, scalar_rows_ok, scalar_rows_ok)

    c6_value = float(motion_by_id["S4965_06_c6_crosscheck"]["numeric_prefactor"])
    c6_expected = 1 / (483840 * math.pi**2)
    c6_ok = math.isclose(c6_value, c6_expected, rel_tol=1.0e-15)
    add(checks, "V4965_14", "independent C3 heat-kernel prefactor match", c6_expected, c6_value, c6_ok)

    sign_guardrail = motion_by_id["S4965_07_scalar_only_test"]
    sign_scope_ok = (
        sign_guardrail["status"] == "DIRECT_SCALAR_THRESHOLD_IDENTIFICATION_REJECTED_SCHEME_INVARIANT_ORIGIN_OPEN"
        and "physical-origin_no_go_not_implied" in sign_guardrail["sign_or_ratio"]
    )
    add(checks, "V4965_15", "sign mismatch is not promoted to physical origin no-go", True, sign_scope_ok, sign_scope_ok)

    power_count_ok = len(power_rows) == 8 and all(int(row["computed_D"]) == 8 for row in power_rows)
    add(checks, "V4965_16", "all p8 power-count rows evaluate to D=8", "8/8", f"{sum(int(row['computed_D']) == 8 for row in power_rows)}/{len(power_rows)}", power_count_ok)

    p4_relocated = [row for row in power_rows if row["status"] == "P4_DEPENDENT_CLASS_RELOCATED_BY_EQUIVALENCE_QUOTIENT"]
    add(checks, "V4965_17", "four p4-dependent partitions are quotient-relocated", 4, len(p4_relocated), len(p4_relocated) == 4)

    flow_summary = result["parent_power_count_and_flow_gate"]
    flow_rank_ok = (
        flow_summary["target_p8_rank"] == 2
        and flow_summary["current_4935_p8_projection_rank"] == 0
        and flow_summary["minimal_motion_scalar_source_rank"] == 1
        and not flow_summary["total_parent_p8_values_identified"]
    )
    add(checks, "V4965_18", "parent p8 rank accounting is 2 target 0 current 1 partial", "2/0/1 total open", flow_summary, flow_rank_ok)

    dispersive_by_id = {row["cone_id"]: row for row in dispersive_rows}
    cone = dispersive_by_id["D4965_00_primary_bound"]
    cone_ok = (
        cone["MTS_coordinate_form"] == "B_plus >= 576*pi^2*A_C3_phys^2*mu_gap^2"
        and truth(cone["valid_for_physical_bound"])
        and not truth(cone["valid_for_current_MTS_numeric_bound"])
        and not any(truth(row["valid_for_current_MTS_numeric_bound"]) for row in dispersive_rows)
    )
    add(checks, "V4965_19", "dispersive cone derived but numeric MTS activation blocked", True, cone_ok, cone_ok)

    C3_result = json.loads(
        text(POST / "source-intake" / "functional_rg" / "4963" / "strong_field_C3_and_scalar_branch_results.json")
    )
    A_values = [
        float(C3_result["C3_selection"]["selected_A_C3_min"]),
        float(C3_result["C3_selection"]["selected_A_C3_max"]),
    ]
    expected_factors = sorted(576 * math.pi**2 * value**2 for value in A_values)
    source_scheme_row = dispersive_by_id["D4965_01_source_scheme_transfer"]
    actual_factors = [float(source_scheme_row["coefficient_min"]), float(source_scheme_row["coefficient_max"])]
    cone_numbers_ok = all(math.isclose(a, b, rel_tol=1.0e-15) for a, b in zip(actual_factors, expected_factors))
    add(checks, "V4965_20", "source-scheme cone factors independently recomputed", expected_factors, actual_factors, cone_numbers_ok)

    compact_ok = (
        len(compact_rows) == 11
        and all(truth(row["valid_for_conditional_coefficient_domain"]) for row in compact_rows)
        and all(not truth(row["valid_for_compact_p8_claim"]) for row in compact_rows)
        and all(row["minimal_scalar_direction"] == "B_plus=(6/5)B_minus" for row in compact_rows)
    )
    add(checks, "V4965_21", "eleven compact two-coordinate gates retain nonclaim status", True, compact_ok, compact_ok)

    tightest = min(compact_rows, key=lambda row: float(row["unit_response_l1_budget"]))
    tightest_ok = (
        tightest["object_id"] == "SLY4_near_turning_0p99_Mmax"
        and math.isclose(float(tightest["unit_response_l1_budget"]), 3.027551244686395e232, rel_tol=1.0e-15)
    )
    add(checks, "V4965_22", "tightest inherited compact unit-response budget retained", "SLY4 3.027551244686395e232", f"{tightest['object_id']} {tightest['unit_response_l1_budget']}", tightest_ok)

    decisions = {row["decision_id"]: row for row in decision_rows}
    decisions_ok = (
        len(decision_rows) == 7
        and decisions["DEC4965_00_p8_basis"]["answer"] == "2"
        and decisions["DEC4965_04_total_parent_flow"]["answer"].lower() == "false"
        and decisions["DEC4965_05_compact_GR"]["answer"].lower() == "false"
    )
    add(checks, "V4965_23", "decision table retains total and all-operator false", True, decisions_ok, decisions_ok)

    claims = read_csv(CLAIMS)
    variables = read_csv(VARIABLES)
    claim_rows = [row for row in claims if row["claim_id"] == "L-807"]
    required_variables = {
        "P8Basis4965_MTS",
        "P8HelicityProjector4965_MTS",
        "mu_psi4965",
        "BminusPsi4965",
        "BplusPsi4965",
        "P8DispersiveCone4965",
        "PredictivityStatus4965_MTS",
    }
    variable_ids = {row["symbol"] for row in variables}
    registers_ok = len(claim_rows) == 1 and required_variables.issubset(variable_ids)
    add(checks, "V4965_24", "claims and variable registers contain 4965 rows", True, registers_ok, registers_ok)

    marker_files = [CHECKPOINT, FORMAL_NOTE, EQUATIONS, RED_TEAM, SPINE, RESUME, LOCAL_SPINE]
    missing_markers = [str(path.relative_to(ROOT)) for path in marker_files if FORMAL_MARKER not in text(path)]
    add(checks, "V4965_25", "formal marker appears in every narrative handoff", [], missing_markers, not missing_markers)

    forbidden_claims = [
        phrase
        for phrase in (
            "exact all-operator compact GR = true",
            "full MTS = true",
            "total parent p8 vector = derived",
        )
        if phrase in text(CHECKPOINT)
    ]
    add(checks, "V4965_26", "checkpoint contains no forbidden promotion language", [], forbidden_claims, not forbidden_claims)

    source_refs = [
        SOURCE / "src-1908.08050" / "GravityEFTv2_final.tex",
        SOURCE / "src-2305.10481" / "main.tex",
        SOURCE / "src-2103.12728" / "GravScatt.tex",
        POST / "source-intake" / "functional_rg" / "4935" / "motion_sector_entry_results.json",
        POST / "source-intake" / "functional_rg" / "4963" / "strong_field_C3_and_scalar_branch_results.json",
        POST / "source-intake" / "functional_rg" / "4964" / "p8plus_tail_norm_gate.csv",
    ]
    missing_sources = [str(path) for path in source_refs if not path.exists()]
    add(checks, "V4965_27", "all cited local source paths exist", [], missing_sources, not missing_sources)

    pycache = [str(path) for path in (POST / "scripts").rglob("__pycache__")]
    add(checks, "V4965_28", "scripts tree contains no pycache", [], pycache, not pycache)

    all_passed = all(row["passed"] for row in checks)
    add(checks, "V4965_29", "aggregate validation", True, all_passed, all_passed)
    write_output(checks)
    print(f"{sum(row['passed'] for row in checks)}/{len(checks)} validation checks passed")
    return 0 if all(row["passed"] for row in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
