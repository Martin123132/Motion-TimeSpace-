from __future__ import annotations

import csv
import hashlib
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import brentq


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE = POST / "source-intake" / "functional_rg" / "4929"
SCRIPTS = POST / "scripts"

MARKER = "MTS_MATTER_COMPLETED_C3_FLOW_4929"
VALIDATION_MARKER = "MTS_MATTER_COMPLETED_C3_FLOW_VALIDATION_4929"
FORMAL_MARKER = "PPC4161_MATTER_COMPLETED_C3_FLOW_4929"
NEXT_TARGET = "4930-Y5-R2FR-six-derivative-MTS-matter-essential-operator-basis-and-block-triangular-stability-or-Wilson-retention.md"

RESEARCH = SCRIPTS / "Y5_R2FR_4929_matter_completed_C3_flow.py"
CHECKPOINT = POST / "4929-Y5-R2FR-MTS-matter-completed-C3-essential-flow-and-fixed-point-survival-or-one-Wilson-retention.md"
FORMAL_NOTE = FORMAL / "945-PPC4161-matter-completed-C3-leading-flow-and-closure-boundary.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
VALIDATION_OUTPUT = OUTPUT / "P8_Y5_BRR545_4929_VALIDATION.csv"

EXPECTED_OUTPUTS = [
    "P8_Y5_R2FR_4929_MATTER_FIELD_INVENTORY.csv",
    "P8_Y5_R2FR_4929_C3_SPIN_WEIGHT_DERIVATION.csv",
    "P8_Y5_R2FR_4929_NATURAL_QMINUS1_GATE.csv",
    "P8_Y5_R2FR_4929_PROPER_TIME_SHIFT_DIAGNOSTIC.csv",
    "P8_Y5_R2FR_4929_BENCHMARK_FIXED_POINTS.csv",
    "P8_Y5_R2FR_4929_FIXED_POINT_ROBUSTNESS_SCAN.csv",
    "P8_Y5_R2FR_4929_CONDITIONAL_COMPACT_MAP.csv",
    "P8_Y5_R2FR_4929_ESSENTIAL_OPERATOR_CLOSURE.csv",
    "P8_Y5_R2FR_4929_PARENT_INHERITANCE_GATE.csv",
    "P8_Y5_R2FR_4929_SOURCE_REGISTER.csv",
    "P8_Y5_R2FR_4929_GATE_DECISION.csv",
]

EXPECTED_HASHES = {
    SOURCE / "2104.11336v2.pdf": "9c59217b0653e44e5b93ad612ae6ced26cbf7e04275e3523c7aa1a5fbf6156b8",
    SOURCE / "2104.11336v2-source.tar": "79b7e2f8de41e3c7a4fa5028311eeff7d8efc1228d0db7c1b69c1a9f79916af4",
    SOURCE / "2204.08564v2.pdf": "11970922381681435f29a135f823bf8840a2f41f323f8253f3331062d0734744",
    SOURCE / "2204.08564v2-source.tar": "7e4504e7bea553db51f01ed23860cb7309432a863df124c881668c60f21c5afe",
    SOURCE / "2312.03831v1.pdf": "86b424e0c309d06444c110841e23751b4edcb44548fbcb50fddac6d8c1fb700f",
    SOURCE / "2312.03831v1-source.tar": "830678a191f7bed7fe0f0050e2dc86207ece3044719ec475130e4427a36a8956",
    SOURCE / "1311.2898v2.pdf": "f2adcbd636ed7e662d54769ca6a20cd6ca20564e3c9a8bbe079eae5cc113cd0b",
    SOURCE / "1311.2898v2-source.tar": "e0d90aac0e92ec05fabb67b824969148e8e49a870566f49844f46e2a58f3d5f2",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    if not reader.fieldnames or any(None in row for row in rows):
        raise ValueError(f"malformed CSV: {path}")
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def source_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def add_check(
    rows: list[dict[str, Any]],
    validation_id: str,
    description: str,
    expected: Any,
    actual: Any,
    passed: bool,
) -> None:
    rows.append(
        {
            "validation_id": validation_id,
            "description": description,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "checkpoint_marker": VALIDATION_MARKER,
            "valid_for_claim": False,
            "source_checked_date": "2026-07-12",
        }
    )


def beta_g(newton: float, weight_1: float) -> float:
    pure = 2.0 * newton * (-32.0 * newton + 6.0 * math.pi) / (
        -9.0 * newton + 6.0 * math.pi
    )
    return pure + weight_1 * newton**2 / (6.0 * math.pi)


def beta_c3(newton: float, c3_coupling: float) -> float:
    pi = math.pi
    numerator = (
        69.0 * newton
        + (
            -3_709_440.0 * newton**2 * pi
            + 14_515_200.0 * newton * pi**2
            + 1_451_520.0 * pi**3
        )
        * c3_coupling
        + (
            47_585_664.0 * newton**3 * pi**2
            - 21_337_344.0 * newton**2 * pi**3
        )
        * c3_coupling**2
        + (
            -84_188_160.0 * newton**4 * pi**3
            + 78_382_080.0 * newton**3 * pi**4
        )
        * c3_coupling**3
    )
    return -numerator / (120_960.0 * (9.0 * newton - 6.0 * pi) * pi**2)


def independent_fixed_point(weight_1: float) -> tuple[float, float]:
    newton_star = brentq(
        lambda value: beta_g(value, weight_1),
        1.0e-12,
        (2.0 * math.pi / 3.0) * (1.0 - 1.0e-10),
    )
    pi = math.pi
    coefficients = [
        -84_188_160.0 * newton_star**4 * pi**3
        + 78_382_080.0 * newton_star**3 * pi**4,
        47_585_664.0 * newton_star**3 * pi**2
        - 21_337_344.0 * newton_star**2 * pi**3,
        -3_709_440.0 * newton_star**2 * pi
        + 14_515_200.0 * newton_star * pi**2
        + 1_451_520.0 * pi**3,
        69.0 * newton_star,
    ]
    roots = np.roots(coefficients)
    real_roots = [float(root.real) for root in roots if abs(root.imag) < 1.0e-9]
    return newton_star, min(real_roots, key=abs)


def main() -> int:
    checks: list[dict[str, Any]] = []
    compile_failures: list[str] = []
    for path in (RESEARCH, Path(__file__).resolve()):
        try:
            compile(source_text(path), str(path), "exec")
        except SyntaxError as error:
            compile_failures.append(f"{path.name}:{error}")
    add_check(
        checks,
        "VAL4929_00_compile",
        "research and validation scripts compile in memory",
        "no syntax errors",
        ";".join(compile_failures) or "no syntax errors",
        not compile_failures,
    )

    run = subprocess.run(
        [sys.executable, "-B", str(RESEARCH)],
        cwd=POST,
        text=True,
        capture_output=True,
        timeout=180,
        check=False,
    )
    add_check(
        checks,
        "VAL4929_01_research_run",
        "research generator reruns successfully",
        "return 0 and PASS marker",
        f"return={run.returncode}; stdout={run.stdout.strip()}",
        run.returncode == 0
        and "P8_Y5_R2FR_4929_MATTER_COMPLETED_C3_FLOW_PASS" in run.stdout,
    )

    missing_outputs = [name for name in EXPECTED_OUTPUTS if not (OUTPUT / name).exists()]
    add_check(
        checks,
        "VAL4929_02_outputs",
        "all expected evidence tables exist",
        len(EXPECTED_OUTPUTS),
        len(EXPECTED_OUTPUTS) - len(missing_outputs),
        not missing_outputs,
    )

    parsed: dict[str, list[dict[str, str]]] = {}
    parse_failures: list[str] = []
    for name in EXPECTED_OUTPUTS:
        try:
            parsed[name] = read_csv(OUTPUT / name)
        except (OSError, ValueError) as error:
            parse_failures.append(f"{name}:{error}")
    add_check(
        checks,
        "VAL4929_03_csv_shape",
        "all evidence CSVs parse without malformed rows",
        "no malformed rows",
        ";".join(parse_failures) or "no malformed rows",
        not parse_failures,
    )

    all_rows = [row for rows in parsed.values() for row in rows]
    marker_failures = [row for row in all_rows if row.get("checkpoint_marker") != MARKER]
    add_check(
        checks,
        "VAL4929_04_markers",
        "all generated evidence rows carry the checkpoint marker",
        0,
        len(marker_failures),
        not marker_failures,
    )
    claimable = [row for row in all_rows if as_bool(row.get("valid_for_claim"))]
    add_check(
        checks,
        "VAL4929_05_nonclaim",
        "all checkpoint evidence remains private nonclaim",
        0,
        len(claimable),
        not claimable,
    )
    placeholders = [
        row
        for row in all_rows
        if "MISSING_" in " ".join(str(value) for value in row.values())
    ]
    add_check(
        checks,
        "VAL4929_06_no_placeholders",
        "no generated row contains a placeholder token",
        0,
        len(placeholders),
        not placeholders,
    )

    hash_failures = [
        path.name
        for path, expected_hash in EXPECTED_HASHES.items()
        if not path.exists() or digest(path) != expected_hash
    ]
    add_check(
        checks,
        "VAL4929_07_hashes",
        "all eight primary PDF/source archives match locked hashes",
        0,
        len(hash_failures),
        not hash_failures,
    )

    source_rows = parsed["P8_Y5_R2FR_4929_SOURCE_REGISTER.csv"]
    source_failures = [row["source_id"] for row in source_rows if not as_bool(row["passed"])]
    add_check(
        checks,
        "VAL4929_08_sources",
        "primary archives TeX markers internal coefficients and URLs verify",
        "31 rows; zero failures",
        f"{len(source_rows)} rows; failures={source_failures}",
        len(source_rows) == 31 and not source_failures,
    )

    spin_rows = parsed["P8_Y5_R2FR_4929_C3_SPIN_WEIGHT_DERIVATION.csv"]
    spin = {row["field"]: row for row in spin_rows}
    maxwell_weight = float(spin["massive Proca"]["Ricci_flat_C3_weight"]) - float(
        spin["real scalar"]["Ricci_flat_C3_weight"]
    )
    add_check(
        checks,
        "VAL4929_09_spin_identity",
        "Proca determinant identity gives Maxwell weight two and W3=W0",
        "Maxwell=2; combined identity present",
        f"Maxwell={maxwell_weight}; combined={spin['combined free matter']['Ricci_flat_C3_weight']}",
        len(spin_rows) == 5
        and math.isclose(maxwell_weight, 2.0)
        and "W0" in spin["combined free matter"]["Ricci_flat_C3_weight"],
    )

    q_rows = parsed["P8_Y5_R2FR_4929_NATURAL_QMINUS1_GATE.csv"]
    q_c3 = next(row for row in q_rows if row["gate_id"] == "QG4929_03_C3")
    q_newton = next(row for row in q_rows if row["gate_id"] == "QG4929_02_Newton")
    add_check(
        checks,
        "VAL4929_10_qminus1",
        "optimized free-spectator trace has Q_-1 zero and W1/(6pi) Newton increment",
        "0 and 1/(6pi)",
        f"{q_c3['derived_value']}; {q_newton['derived_value']}",
        float(q_c3["derived_value"]) == 0.0
        and math.isclose(float(q_newton["derived_value"]), 1.0 / (6.0 * math.pi), rel_tol=1.0e-15),
    )

    inventory = parsed["P8_Y5_R2FR_4929_MATTER_FIELD_INVENTORY.csv"]
    inventory_by_name = {row["scenario"]: row for row in inventory}
    add_check(
        checks,
        "VAL4929_11_inventory",
        "SM45 SM48 and conditional one-motion-mode weights reproduce source inventory",
        "(-62,1),(-68,4),(-61,2),(-67,5)",
        ";".join(
            f"{name}=({inventory_by_name[name]['W0_equals_W3']},{inventory_by_name[name]['W1']})"
            for name in (
                "SM45_minimal_Higgs",
                "SM48_minimal_Higgs",
                "SM45_minimal_Higgs_plus_motion",
                "SM48_minimal_Higgs_plus_motion",
            )
        ),
        len(inventory) == 9
        and float(inventory_by_name["SM45_minimal_Higgs"]["W0_equals_W3"]) == -62.0
        and float(inventory_by_name["SM45_minimal_Higgs"]["W1"]) == 1.0
        and float(inventory_by_name["SM48_minimal_Higgs"]["W0_equals_W3"]) == -68.0
        and float(inventory_by_name["SM48_minimal_Higgs"]["W1"]) == 4.0
        and float(inventory_by_name["SM45_minimal_Higgs_plus_motion"]["W1"]) == 2.0
        and float(inventory_by_name["SM48_minimal_Higgs_plus_motion"]["W1"]) == 5.0,
    )

    fixed_rows = parsed["P8_Y5_R2FR_4929_BENCHMARK_FIXED_POINTS.csv"]
    optimized = [row for row in fixed_rows if row["projection"] == "optimized_spectral_free_spectator"]
    hybrid = [row for row in fixed_rows if row["projection"] == "proper_time_hybrid_diagnostic"]
    fixed_failures = [
        row["scenario"] + ":" + row["projection"]
        for row in fixed_rows
        if not as_bool(row["passed"])
        or not (float(row["g_star"]) > 0.0)
        or not (float(row["theta_relevant_g"]) > 0.0)
        or not (float(row["theta_irrelevant_C3"]) < 0.0)
    ]
    add_check(
        checks,
        "VAL4929_12_benchmarks",
        "all optimized and proper-time benchmark fixed points survive in two dimensions",
        "9 optimized; 9 hybrid; zero failures",
        f"{len(optimized)} optimized; {len(hybrid)} hybrid; failures={fixed_failures}",
        len(optimized) == 9 and len(hybrid) == 9 and not fixed_failures,
    )

    independent_failures: list[str] = []
    for scenario, weight_1 in (("pure_gravity", 0.0), ("SM45_minimal_Higgs", 1.0), ("SM48_minimal_Higgs", 4.0)):
        expected = next(row for row in optimized if row["scenario"] == scenario)
        newton_star, c3_star = independent_fixed_point(weight_1)
        if not math.isclose(newton_star, float(expected["g_star"]), rel_tol=2.0e-12):
            independent_failures.append(scenario + ":g")
        if not math.isclose(c3_star, float(expected["h_star"]), rel_tol=2.0e-10):
            independent_failures.append(scenario + ":h")
        if math.hypot(beta_g(newton_star, weight_1), beta_c3(newton_star, c3_star)) > 1.0e-10:
            independent_failures.append(scenario + ":beta")
    add_check(
        checks,
        "VAL4929_13_independent_fixed",
        "independent solver reproduces pure SM45 and SM48 optimized fixed points",
        0,
        len(independent_failures),
        not independent_failures,
    )

    scan = parsed["P8_Y5_R2FR_4929_FIXED_POINT_ROBUSTNESS_SCAN.csv"]
    natural_scan = [row for row in scan if row["projection"] == "optimized_spectral_free_spectator"]
    hybrid_scan = [row for row in scan if row["projection"] == "proper_time_hybrid_diagnostic"]
    scan_failures = [row["scan_id"] for row in scan if not as_bool(row["passed"])]
    add_check(
        checks,
        "VAL4929_14_scan",
        "wide two-coordinate stress scan retains fixed-point topology",
        "81 optimized + 6561 hybrid; zero failures",
        f"{len(natural_scan)} optimized + {len(hybrid_scan)} hybrid; failures={len(scan_failures)}",
        len(scan) == 6642
        and len(natural_scan) == 81
        and len(hybrid_scan) == 6561
        and not scan_failures,
    )

    scan_theta_g = [float(row["theta_g"]) for row in scan]
    scan_theta_h = [float(row["theta_h"]) for row in scan]
    add_check(
        checks,
        "VAL4929_15_scan_ranges",
        "wide scan critical exponents remain bounded away from zero",
        "theta_g>2.4 and theta_h<-6.3",
        f"theta_g=[{min(scan_theta_g)},{max(scan_theta_g)}]; theta_h=[{min(scan_theta_h)},{max(scan_theta_h)}]",
        min(scan_theta_g) > 2.4 and max(scan_theta_h) < -6.3,
    )

    proper = parsed["P8_Y5_R2FR_4929_PROPER_TIME_SHIFT_DIAGNOSTIC.csv"]
    shifted = [row for row in proper if abs(float(row["C_m_equals_W0_c6"])) > 0.0]
    add_check(
        checks,
        "VAL4929_16_shift_firewall",
        "proper-time matter branches are explicitly shifted-Gaussian diagnostics",
        "8 nonzero shifts; all quarantined",
        f"{len(shifted)} nonzero; statuses={sorted(set(row['status'] for row in proper))}",
        len(proper) == 9
        and len(shifted) == 8
        and all(row["status"] == "SHIFTED_GAUSSIAN_QUARANTINED" for row in proper),
    )

    conditional = parsed["P8_Y5_R2FR_4929_CONDITIONAL_COMPACT_MAP.csv"]
    amplitudes = [float(row["A_C3_equals_GC3_over_GN_at_k0"]) for row in conditional]
    lengths = [float(row["ell_plus_m"]) for row in conditional]
    add_check(
        checks,
        "VAL4929_17_conditional_map",
        "all optimized benchmark separatrices remain positive and compact-safe",
        "9 rows; A around 3e-6; ell around 1.8e-36 m",
        f"rows={len(conditional)}; A=[{min(amplitudes)},{max(amplitudes)}]; ell=[{min(lengths)},{max(lengths)}]",
        len(conditional) == 9
        and min(amplitudes) > 2.9e-6
        and max(amplitudes) < 3.1e-6
        and all(as_bool(row["compact_safe_within_leading_projection"]) for row in conditional)
        and all(not as_bool(row["MTS_prediction"]) for row in conditional),
    )

    pure_map = next(row for row in conditional if row["scenario"] == "pure_gravity")
    add_check(
        checks,
        "VAL4929_18_pure_recovery",
        "zero-matter spectator branch recovers checkpoint 4928 infrared constant",
        3.024098389340624e-6,
        pure_map["A_C3_equals_GC3_over_GN_at_k0"],
        math.isclose(
            float(pure_map["A_C3_equals_GC3_over_GN_at_k0"]),
            3.024098389340624e-6,
            rel_tol=2.0e-9,
        ),
    )

    closure = parsed["P8_Y5_R2FR_4929_ESSENTIAL_OPERATOR_CLOSURE.csv"]
    open_blocks = [row["block"] for row in closure if not as_bool(row["closed"])]
    add_check(
        checks,
        "VAL4929_19_closure",
        "free traces close while interacting six-derivative essential blocks remain explicit",
        "9 rows; 6 open",
        f"{len(closure)} rows; open={open_blocks}",
        len(closure) == 9 and len(open_blocks) == 6,
    )

    inheritance = parsed["P8_Y5_R2FR_4929_PARENT_INHERITANCE_GATE.csv"]
    all_dynamic = next(row for row in inheritance if row["clause"] == "all_dynamic_inheritance")
    add_check(
        checks,
        "VAL4929_20_inheritance",
        "full MTS dynamic inheritance remains false despite leading survival",
        False,
        all_dynamic["satisfied"],
        not as_bool(all_dynamic["satisfied"])
        and as_bool(all_dynamic["blocks_numeric_MTS_prediction"]),
    )

    gates = {row["gate"]: row for row in parsed["P8_Y5_R2FR_4929_GATE_DECISION.csv"]}
    add_check(
        checks,
        "VAL4929_21_decision",
        "final gate retains one Wilson and refuses compact/full promotion",
        "one Wilson retained; full closure not derived; next 4930",
        f"Wilson={gates['one_observational_Wilson']['status']}; closure={gates['full_matter_essential_closure']['status']}; next={gates['next_target']['decision']}",
        gates["one_observational_Wilson"]["status"] == "RETAINED"
        and gates["full_matter_essential_closure"]["status"] == "NOT_DERIVED"
        and gates["compact_and_full_MTS_to_GR"]["status"] == "NOT_PROMOTED"
        and gates["next_target"]["decision"] == NEXT_TARGET,
    )

    marker_paths = [
        (CHECKPOINT, MARKER),
        (FORMAL_NOTE, FORMAL_MARKER),
        (PROVENANCE, "MTS_MATTER_COMPLETED_C3_FLOW_PROVENANCE_4929"),
        (CLAIMS, "L-771"),
        (VARIABLES, "C3MatterFlowStatus4929_MTS"),
        (EQUATIONS, "1.222 Matter-completed C3 leading flow and closure boundary"),
        (RED_TEAM, "173. Leading free-spectator survival is not the complete matter critical surface"),
        (SPINE, "PPC4161 checkpoint 4929"),
        (RESUME, NEXT_TARGET),
    ]
    marker_path_failures = [
        path.name
        for path, marker in marker_paths
        if not path.exists() or marker not in source_text(path)
    ]
    add_check(
        checks,
        "VAL4929_22_registers",
        "checkpoint formal note provenance registers and resume markers exist",
        0,
        len(marker_path_failures),
        not marker_path_failures,
    )

    claims_rows = read_csv(CLAIMS)
    variable_rows = read_csv(VARIABLES)
    add_check(
        checks,
        "VAL4929_23_register_csv",
        "claims and variable registers remain parseable with unique new identifiers",
        "one L-771 and fourteen 4929 variables",
        f"L-771={sum(row['claim_id'] == 'L-771' for row in claims_rows)}; vars={sum('4929_MTS' in row['symbol'] for row in variable_rows)}",
        sum(row["claim_id"] == "L-771" for row in claims_rows) == 1
        and sum("4929_MTS" in row["symbol"] for row in variable_rows) == 14,
    )

    pycache = list(POST.rglob("__pycache__"))
    new_pycache = [path for path in pycache if "scripts" in path.parts and any("4929" in item.name for item in path.glob("*"))]
    add_check(
        checks,
        "VAL4929_24_pycache",
        "checkpoint execution creates no 4929 bytecode cache",
        0,
        len(new_pycache),
        not new_pycache,
    )

    write_csv(VALIDATION_OUTPUT, checks)
    passed_count = sum(as_bool(row["passed"]) for row in checks)
    all_passed = passed_count == len(checks)
    print("P8_Y5_BRR545_4929_VALIDATION_PASS" if all_passed else "P8_Y5_BRR545_4929_VALIDATION_FAIL")
    print(f"checks_passed={passed_count}/{len(checks)}")
    if not all_passed:
        print("failed=" + ",".join(row["validation_id"] for row in checks if not as_bool(row["passed"])))
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
