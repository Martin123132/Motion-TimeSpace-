from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE = POST / "source-intake" / "functional_rg" / "4933"
CHECKPOINT = POST / "4933-Y5-R2FR-C3-CFF-F4-minimal-combined-natural-flow-and-0p239-stability-gate.md"
FORMAL_NOTE = FORMAL / "949-PPC4161-C3-CFF-F4-combined-natural-flow.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_C3_CFF_F4_COMBINED_NATURAL_FLOW_4933"
VALIDATION_MARKER = "MTS_C3_CFF_F4_COMBINED_NATURAL_FLOW_VALIDATION_4933"
CHECKED_DATE = "2026-07-12"
NEXT_TARGET = "4934-Y5-R2FR-portal-a6-completion-and-direct-C3-photon-Hessian-gate.md"

SCRIPTS = (
    POST / "scripts" / "Y5_R2FR_4933_wolfram_notebook_box_extractor.py",
    POST / "scripts" / "Y5_R2FR_4933_c3_notebook_box_extractor.py",
    POST / "scripts" / "Y5_R2FR_4933_c3_direct_threshold_solver.py",
    POST / "scripts" / "Y5_R2FR_4933_photon_flow_reproduction.py",
    POST / "scripts" / "Y5_R2FR_4933_combined_c3_photon_stability.py",
    POST / "scripts" / "Y5_R2FR_4933_combined_natural_flow_evidence.py",
    Path(__file__),
)

TABLES = {
    "sources": ("P8_Y5_R2FR_4933_SOURCE_REGISTER.csv", 13),
    "compatibility": ("P8_Y5_R2FR_4933_SOURCE_COMPATIBILITY.csv", 8),
    "c3": ("P8_Y5_R2FR_4933_C3_SOURCE_REPRODUCTION.csv", 4),
    "photon": ("P8_Y5_R2FR_4933_PHOTON_FLOW_RECONSTRUCTION.csv", 5),
    "combined": ("P8_Y5_R2FR_4933_PARTIAL_COMBINED_COMMON_ZERO.csv", 8),
    "responses": ("P8_Y5_R2FR_4933_OPEN_PROJECTION_RESPONSE.csv", 8),
    "stability": ("P8_Y5_R2FR_4933_SIGNED_STABILITY.csv", 6),
    "gates": ("P8_Y5_R2FR_4933_GATE_DECISION.csv", 10),
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def is_true(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def is_false(value: Any) -> bool:
    return str(value).strip().lower() == "false"


def add_check(
    checks: list[dict[str, Any]],
    check_id: str,
    requirement: str,
    expected: str,
    actual: str,
    passed: bool,
) -> None:
    checks.append(
        {
            "validation_id": check_id,
            "requirement": requirement,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "checkpoint_marker": VALIDATION_MARKER,
            "valid_for_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
    )


def main() -> int:
    checks: list[dict[str, Any]] = []
    c3_json_path = SOURCE / "C3_direct_threshold_results.json"
    photon_json_path = SOURCE / "photon_flow_reproduction_results.json"
    combined_json_path = SOURCE / "combined_c3_photon_stability_results.json"
    required_paths = [
        *SCRIPTS,
        c3_json_path,
        photon_json_path,
        combined_json_path,
        CHECKPOINT,
        FORMAL_NOTE,
        CLAIMS,
        VARIABLES,
        EQUATIONS,
        RED_TEAM,
        SPINE,
        RESUME,
        PROVENANCE,
    ]
    missing_paths = [str(path) for path in required_paths if not path.exists()]
    add_check(
        checks,
        "VAL4933_00_paths",
        "all scripts results authored documents and registers exist",
        "0 missing paths",
        str(missing_paths),
        not missing_paths,
    )

    syntax_errors = []
    for path in SCRIPTS:
        try:
            compile(read_text(path), str(path), "exec")
        except SyntaxError as error:
            syntax_errors.append(f"{path.name}:{error}")
    add_check(
        checks,
        "VAL4933_01_compile",
        "all seven checkpoint scripts compile without writing bytecode",
        "0 syntax errors",
        str(syntax_errors),
        not syntax_errors,
    )

    rows_by_name: dict[str, list[dict[str, str]]] = {}
    table_failures = []
    for name, (filename, expected_rows) in TABLES.items():
        path = OUTPUT / filename
        if not path.exists():
            rows_by_name[name] = []
            table_failures.append(f"{name}:missing")
            continue
        rows = read_csv(path)
        rows_by_name[name] = rows
        if len(rows) != expected_rows:
            table_failures.append(f"{name}:{len(rows)}!={expected_rows}")
    add_check(
        checks,
        "VAL4933_02_tables",
        "all eight evidence tables parse with declared row counts",
        ";".join(f"{name}:{count}" for name, (_, count) in TABLES.items()),
        "OK" if not table_failures else ";".join(table_failures),
        not table_failures,
    )

    all_rows = [row for rows in rows_by_name.values() for row in rows]
    marker_failures = sum(row.get("checkpoint_marker") != MARKER for row in all_rows)
    claim_failures = sum(not is_false(row.get("valid_for_claim")) for row in all_rows)
    pass_failures = sum(not is_true(row.get("passed")) for row in all_rows)
    missing_tokens = sum("MISSING_" in str(value) for row in all_rows for value in row.values())
    add_check(
        checks,
        "VAL4933_03_row_policy",
        "all evidence rows are marked nonclaim pass internal checks and contain no placeholder tokens",
        "marker=0; claim=0; pass=0; MISSING=0",
        f"marker={marker_failures}; claim={claim_failures}; pass={pass_failures}; MISSING={missing_tokens}",
        marker_failures == claim_failures == pass_failures == missing_tokens == 0,
    )

    source_failures = []
    hash_failures = []
    hash_rows = 0
    for row in rows_by_name["sources"]:
        source_ref = row["source_path_or_url"]
        if source_ref.startswith("http"):
            continue
        path = ROOT / Path(source_ref)
        if not path.exists():
            source_failures.append(source_ref)
            continue
        if row.get("expected_sha256"):
            hash_rows += 1
            if digest(path) != row["expected_sha256"] or row["actual_sha256"] != row["expected_sha256"]:
                hash_failures.append(source_ref)
    add_check(
        checks,
        "VAL4933_04_sources",
        "all eight local primary artifacts exist and match locked hashes",
        "missing=0; hash_rows=8; mismatches=0",
        f"missing={source_failures}; hash_rows={hash_rows}; mismatches={hash_failures}",
        not source_failures and hash_rows == 8 and not hash_failures,
    )

    c3_result = load_json(c3_json_path)
    reproduction = c3_result["source_reproduction"]
    source_root = reproduction["roots"][0]
    source_errors = [
        abs(actual - expected)
        for actual, expected in zip(source_root["fixed_point"], reproduction["expected_fixed_point"])
    ]
    source_exponents = sorted(row["real"] for row in source_root["critical_exponents"])
    expected_exponents = sorted(reproduction["expected_critical_exponents"])
    exponent_error = max(abs(actual - expected) for actual, expected in zip(source_exponents, expected_exponents))
    c3_ok = (
        reproduction["pass"]
        and max(source_errors) < 1e-14
        and exponent_error < 2e-9
        and c3_result["stats"]["q_count"] == 2272
        and c3_result["stats"]["q_distribution_higher_power_zeroed_by_source_rule"] == 0
    )
    add_check(
        checks,
        "VAL4933_05_c3_reproduction",
        "direct threshold evaluator reproduces the C3 source point and exponents",
        "coordinate error<1e-14; exponent error<2e-9; Q=2272",
        f"coordinate={source_errors}; exponent={exponent_error}; Q={c3_result['stats']['q_count']}",
        c3_ok,
    )

    photon_result = load_json(photon_json_path)
    photon_root = photon_result["reconstructed_root"]
    published = photon_result["published_fp1"]["coordinates"]
    tolerances = (1e-3, 5e-3, 5e-2, 1e-5)
    coordinate_differences = [abs(actual - expected) for actual, expected in zip(photon_root["coordinates"], published)]
    reconstructed_leading = max(row["real"] for row in photon_root["critical_exponents"])
    photon_ok = (
        photon_root["success"]
        and max(abs(value) for value in photon_root["beta_residual"]) < 1e-10
        and all(difference < tolerance for difference, tolerance in zip(coordinate_differences, tolerances))
        and 0.04 < abs(reconstructed_leading - 1.845) < 0.06
    )
    add_check(
        checks,
        "VAL4933_06_photon_reconstruction",
        "photon root is reconstructed within published rounding while the leading-exponent offset remains explicit",
        "coordinate tolerances pass; residual<1e-10; leading offset 0.04--0.06",
        f"differences={coordinate_differences}; residual={photon_root['beta_residual']}; leading={reconstructed_leading}",
        photon_ok,
    )

    combined_result = load_json(combined_json_path)
    partial = combined_result["partial_combined_common_zero"]
    expected_point = [
        0.13056045261536448,
        0.347004250660221,
        3.2444364236742977,
        0.003729942575813481,
        4.273038337287102e-6,
    ]
    point_error = max(
        abs(actual - expected) for actual, expected in zip(partial["coordinates_g_gplus_gminus_gCFF_h"], expected_point)
    )
    common_ok = (
        partial["success"]
        and partial["beta_residual_infinity_norm"] < 2e-12
        and point_error < 1e-12
        and math.isfinite(partial["linear_system_condition_number"])
        and partial["linear_system_condition_number"] > 1e5
    )
    add_check(
        checks,
        "VAL4933_07_common_zero",
        "shared 20-equation partial flow converges at the recorded five-coordinate common zero",
        "point error<1e-12; beta_inf<2e-12; finite declared condition>1e5",
        f"point_error={point_error}; beta_inf={partial['beta_residual_infinity_norm']}; condition={partial['linear_system_condition_number']}",
        common_ok,
    )

    index = partial["signed_index"]
    gap = partial["signed_imaginary_axis_gap"]
    coordinate_gate = partial["coordinate_basis_stability_matrix_2norm_gate"]
    stability_ok = (
        index == {"negative_real_parts": 1, "positive_real_parts": 4}
        and math.isclose(gap, 0.24207516460574788, rel_tol=1e-10)
        and math.isclose(coordinate_gate, 0.0016084042284096303, rel_tol=1e-10)
        and not combined_result["stability_contract"]["full_combined_index_proved"]
    )
    add_check(
        checks,
        "VAL4933_08_stability",
        "partial matrix has one relevant direction and full index remains unclaimed",
        "index=1/4; gap=0.2420751646; coordinate gate=0.00160840423; full=False",
        f"index={index}; gap={gap}; gate={coordinate_gate}; full={combined_result['stability_contract']['full_combined_index_proved']}",
        stability_ok,
    )

    frozen = combined_result["frozen_photon_lower_curvature_combined_solve"]
    maxwell = frozen["minimal_Maxwell_a6"]
    principal = combined_result["principal_cff_to_c3"]
    a6_ok = (
        math.isclose(maxwell["massless_Maxwell_c6_difference"], 1 / (15120 * (4 * math.pi) ** 2), rel_tol=1e-14)
        and math.isclose(maxwell["C3_RHS_projection"], -6.247079790476585e-8, rel_tol=1e-12)
        and math.isclose(principal["principal_C3_RHS_projection_term"], 1.0713723290526187e-9, rel_tol=1e-12)
        and principal["status"] == "EXACT_WITHIN_CONSTANT_WEYL_PRINCIPAL_SYMBOL_NOT_COMPLETE_A6"
    )
    add_check(
        checks,
        "VAL4933_09_derived_a6",
        "minimal Maxwell a6 and principal CFF cubed terms match their derived formulas",
        "c6=1/[15120(4pi)^2]; Maxwell=-6.24708e-8; principal=1.07137e-9",
        f"{maxwell}; principal={principal}",
        a6_ok,
    )

    response = partial["open_projection_linear_response"]
    a6_threshold = response["unknown_portal_a6_C3_row"][
        "linear_projection_magnitude_for_all_coordinate_shifts_below_one_percent"
    ]
    photon_responses = response["direct_C3_Hessian_photon_rows"]
    response_ok = (
        math.isclose(a6_threshold, 4.674459778947013e-8, rel_tol=1e-10)
        and set(photon_responses) == {"F2", "FDeltaF", "RFF", "SFF", "F2sq", "F4", "CFF"}
        and all(
            row["linear_projection_magnitude_for_all_coordinate_shifts_below_one_percent"] > 0
            for row in photon_responses.values()
        )
        and response["scope"] == "first-order source and fixed-point displacement map; not a nonlinear enclosure"
    )
    add_check(
        checks,
        "VAL4933_10_response",
        "all eight omitted-source linear response columns are explicit and firewalled from nonlinear interpretation",
        "a6 threshold=4.67445978e-8; seven named photon rows; first-order scope",
        f"a6={a6_threshold}; photon_rows={sorted(photon_responses)}; scope={response['scope']}",
        response_ok,
    )

    expected_open = [
        "linear and quadratic CFF-curvature a6 contributions to beta_h",
        "direct C3 Hessian contribution to the seven photon-background projection rows",
    ]
    boundary_ok = (
        combined_result["open_exact_terms"] == expected_open
        and not partial["is_full_combined_fixed_point"]
        and len(partial["omitted"]) == 2
    )
    add_check(
        checks,
        "VAL4933_11_claim_boundary",
        "the two exact source omissions are enumerated and the full fixed point remains false",
        str(expected_open),
        f"open={combined_result['open_exact_terms']}; full={partial['is_full_combined_fixed_point']}",
        boundary_ok,
    )

    checkpoint_text = read_text(CHECKPOINT)
    formal_text = read_text(FORMAL_NOTE)
    provenance_text = read_text(PROVENANCE)
    docs_ok = all(
        token in checkpoint_text
        for token in (
            MARKER,
            "0.130560452615",
            "0.00160840422841",
            "4.67445977895e-8",
            "not the complete MTS point",
            NEXT_TARGET,
        )
    ) and all(
        token in formal_text
        for token in ("PPC4161_C3_CFF_F4_COMBINED_NATURAL_FLOW_4933", "1.44518e-13", "full minimal combined point")
    ) and all(
        token in provenance_text
        for token in ("MTS_C3_CFF_F4_COMBINED_NATURAL_FLOW_PROVENANCE_4933", "2272", "valid_for_claim=false")
    )
    add_check(
        checks,
        "VAL4933_12_docs",
        "checkpoint formal note and provenance contain numeric results and claim firewalls",
        "all required markers present",
        f"checkpoint_chars={len(checkpoint_text)}; formal_chars={len(formal_text)}; provenance_chars={len(provenance_text)}",
        docs_ok,
    )

    claim_rows = read_csv(CLAIMS)
    variable_rows = read_csv(VARIABLES)
    claim_count = sum(row.get("claim_id") == "L-775" for row in claim_rows)
    variable_symbols = [row.get("symbol", "") for row in variable_rows if "4933_MTS" in row.get("symbol", "")]
    add_check(
        checks,
        "VAL4933_13_register_csv",
        "claim and variable registers contain unique checkpoint identifiers",
        "L-775=1; 4933 variables=12",
        f"L-775={claim_count}; variables={len(variable_symbols)}; symbols={variable_symbols}",
        claim_count == 1 and len(variable_symbols) == 12 and len(set(variable_symbols)) == 12,
    )

    register_markers = {
        EQUATIONS: "## 1.226 Combined `C3-CFF-F4` natural flow",
        RED_TEAM: "## 177. A partial common zero is not the complete MTS fixed point",
        SPINE: "PPC4161_C3_CFF_F4_COMBINED_NATURAL_FLOW_4933",
        RESUME: "Last checkpoint:\n`4933-Y5-R2FR-C3-CFF-F4-minimal-combined-natural-flow-and-0p239-stability-gate.md`",
    }
    register_missing = [f"{path.name}:{marker}" for path, marker in register_markers.items() if marker not in read_text(path)]
    add_check(
        checks,
        "VAL4933_14_register_md",
        "equation red-team spine and resume registers are synchronized",
        "0 missing markers",
        str(register_missing),
        not register_missing,
    )

    gate_rows = {row["gate"]: row for row in rows_by_name["gates"]}
    next_ok = (
        gate_rows.get("next_target", {}).get("decision") == NEXT_TARGET
        and NEXT_TARGET in checkpoint_text
        and NEXT_TARGET in read_text(RESUME)
        and gate_rows.get("full_combined_fixed_point", {}).get("status") == "BLOCKED_BY_TWO_EXACT_TERMS"
        and is_false(gate_rows.get("full_combined_fixed_point", {}).get("claim_promoted"))
    )
    add_check(
        checks,
        "VAL4933_15_next_target",
        "documents and executable gate agree on exact-term completion as the next target",
        NEXT_TARGET,
        str(gate_rows.get("next_target", {})),
        next_ok,
    )

    project_pycache = list((POST / "scripts").glob("__pycache__")) + list(SOURCE.rglob("__pycache__"))
    add_check(
        checks,
        "VAL4933_16_pycache",
        "checkpoint scripts and source packet contain no bytecode caches",
        "0 project __pycache__ directories",
        str([str(path) for path in project_pycache]),
        not project_pycache,
    )

    result_hashes = {
        path.name: digest(path) for path in (c3_json_path, photon_json_path, combined_json_path)
    }
    add_check(
        checks,
        "VAL4933_17_result_hashes",
        "all three executable result JSON files have nonempty stable hash records",
        "3 unique SHA256 values",
        str(result_hashes),
        len(result_hashes) == 3 and len(set(result_hashes.values())) == 3 and all(len(value) == 64 for value in result_hashes.values()),
    )

    output_path = OUTPUT / "P8_Y5_BRR545_4933_VALIDATION.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    passed_count = sum(bool(row["passed"]) for row in checks)
    print(f"P8_Y5_BRR545_4933_VALIDATION_{'PASS' if passed_count == len(checks) else 'FAIL'}")
    print(f"checks={passed_count}/{len(checks)}")
    for row in checks:
        if not row["passed"]:
            print(f"FAILED {row['validation_id']}: {row['actual']}")
    return 0 if passed_count == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
