from __future__ import annotations

import csv
import hashlib
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE = POST / "source-intake" / "functional_rg" / "4928"
SCRIPTS = POST / "scripts"

MARKER = "MTS_INTEGRATED_H_C3_FUNCTIONAL_FLOW_4928"
FORMAL_MARKER = "PPC4161_INTEGRATED_H_C3_FUNCTIONAL_FLOW_4928"
VALIDATION_MARKER = "MTS_INTEGRATED_H_C3_FUNCTIONAL_FLOW_VALIDATION_4928"
RESEARCH = SCRIPTS / "Y5_R2FR_4928_integrated_H_C3_functional_flow.py"
CHECKPOINT = POST / "4928-Y5-R2FR-integrated-H-C3-functional-flow-boundary-or-observational-Wilson-freeze.md"
FORMAL_NOTE = FORMAL / "944-PPC4161-integrated-H-C3-functional-flow-and-Wilson-freeze.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
NEXT_TARGET = "4929-Y5-R2FR-MTS-matter-completed-C3-essential-flow-and-fixed-point-survival-or-one-Wilson-retention.md"

EXPECTED_OUTPUTS = [
    "P8_Y5_R2FR_4928_NATURAL_BETA_FUNCTION.csv",
    "P8_Y5_R2FR_4928_FIXED_POINT.csv",
    "P8_Y5_R2FR_4928_SEPARATRIX.csv",
    "P8_Y5_R2FR_4928_LOG_SIGN_AUDIT.csv",
    "P8_Y5_R2FR_4928_OPERATOR_MAP.csv",
    "P8_Y5_R2FR_4928_REFERENCE_SCALE_SCAN.csv",
    "P8_Y5_R2FR_4928_CONDITIONAL_PREDICTION.csv",
    "P8_Y5_R2FR_4928_PARENT_INHERITANCE_GATE.csv",
    "P8_Y5_R2FR_4928_OBSERVATIONAL_WILSON_FREEZE.csv",
    "P8_Y5_R2FR_4928_SOURCE_REGISTER.csv",
    "P8_Y5_R2FR_4928_GATE_DECISION.csv",
]

EXPECTED_HASHES = {
    SOURCE / "1601.01800v1.pdf": "8e1b524465a2b6b112ea63ca339ccc84da216bdd0b25d6665b2931e9135cc822",
    SOURCE / "1601.01800v1-source.tar": "016ffc070fc1d10d798eb3b8ae37b82abe07897137c722691e2de96f70f6ec89",
    SOURCE / "2509.07058v1.pdf": "e203ead85ebdf37a94c03d52c1a6e68c4d45ab72a90415e1ff165adc42d712ec",
    SOURCE / "2509.07058v1-source.tar": "11cf0a348b5413e7daf896dcf59b560698780b3a21b3670f54664eeb5c9b7c1d",
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


def beta_g(newton: float) -> float:
    return 2.0 * newton * (-32.0 * newton + 6.0 * math.pi) / (
        -9.0 * newton + 6.0 * math.pi
    )


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
    return -numerator / (
        120_960.0 * (9.0 * newton - 6.0 * pi) * pi**2
    )


def independent_separatrix() -> tuple[float, float, float, float]:
    newton_star = 3.0 * math.pi / 16.0
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
    c3_star = next(float(root.real) for root in roots if abs(root.imag) < 1.0e-11)
    delta_g = 1.0e-7
    delta_h = 1.0e-11
    derivative_g = -64.0 / 23.0
    derivative_h_g = (
        beta_c3(newton_star + delta_g, c3_star)
        - beta_c3(newton_star - delta_g, c3_star)
    ) / (2.0 * delta_g)
    derivative_h_h = (
        beta_c3(newton_star, c3_star + delta_h)
        - beta_c3(newton_star, c3_star - delta_h)
    ) / (2.0 * delta_h)
    slope = -derivative_h_g / (derivative_h_h - derivative_g)

    epsilon = 1.0e-4
    g_initial = newton_star - epsilon
    h_initial = c3_star + slope * (g_initial - newton_star)
    x_initial = math.log(g_initial)
    ratio_initial = h_initial / g_initial

    def ratio_flow(log_newton: float, state: np.ndarray) -> list[float]:
        newton = math.exp(log_newton)
        ratio = float(state[0])
        return [beta_c3(newton, ratio * newton) / beta_g(newton) - ratio]

    solution = solve_ivp(
        ratio_flow,
        (x_initial, -40.0),
        [ratio_initial],
        rtol=1.0e-11,
        atol=1.0e-14,
        max_step=0.03,
    )
    log_coefficient = 69.0 / (725_760.0 * math.pi**3)
    ratio_final = float(solution.y[0, -1])
    infrared_constant = ratio_final - 0.5 * log_coefficient * -40.0
    return c3_star, -derivative_h_h, log_coefficient, infrared_constant


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
        "VAL4928_00_compile",
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
        "VAL4928_01_research_run",
        "research generator reruns successfully",
        "return 0 and PASS marker",
        f"return={run.returncode}; stdout={run.stdout.strip()}",
        run.returncode == 0
        and "P8_Y5_R2FR_4928_INTEGRATED_H_C3_FUNCTIONAL_FLOW_PASS" in run.stdout,
    )

    missing_outputs = [name for name in EXPECTED_OUTPUTS if not (OUTPUT / name).exists()]
    add_check(
        checks,
        "VAL4928_02_outputs",
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
        "VAL4928_03_csv_shape",
        "all evidence CSVs parse without malformed rows",
        "no malformed rows",
        ";".join(parse_failures) or "no malformed rows",
        not parse_failures,
    )

    all_rows = [row for rows in parsed.values() for row in rows]
    marker_failures = [row for row in all_rows if row.get("checkpoint_marker") != MARKER]
    add_check(
        checks,
        "VAL4928_04_markers",
        "all generated evidence rows carry the checkpoint marker",
        0,
        len(marker_failures),
        not marker_failures,
    )
    claimable_rows = [row for row in all_rows if as_bool(row.get("valid_for_claim"))]
    add_check(
        checks,
        "VAL4928_05_nonclaim",
        "all checkpoint evidence remains private nonclaim",
        0,
        len(claimable_rows),
        not claimable_rows,
    )
    placeholder_rows = [
        row
        for row in all_rows
        if "MISSING_" in " ".join(str(value) for value in row.values())
    ]
    add_check(
        checks,
        "VAL4928_06_no_placeholders",
        "no generated row contains a MISSING placeholder token",
        0,
        len(placeholder_rows),
        not placeholder_rows,
    )

    hash_failures = [
        path.name
        for path, expected_hash in EXPECTED_HASHES.items()
        if not path.exists() or digest(path) != expected_hash
    ]
    add_check(
        checks,
        "VAL4928_07_source_hashes",
        "all four primary PDF and source archives match locked SHA-256 values",
        0,
        len(hash_failures),
        not hash_failures,
    )

    source_rows = parsed["P8_Y5_R2FR_4928_SOURCE_REGISTER.csv"]
    source_failures = [row["source_id"] for row in source_rows if not as_bool(row["passed"])]
    add_check(
        checks,
        "VAL4928_08_source_register",
        "primary archives extracted equations prior checkpoints registers and URLs are verified",
        "26 rows; zero failures",
        f"{len(source_rows)} rows; failures={source_failures}",
        len(source_rows) == 26 and not source_failures,
    )

    beta_rows = parsed["P8_Y5_R2FR_4928_NATURAL_BETA_FUNCTION.csv"]
    log_row = next(row for row in beta_rows if row["object"] == "massless logarithmic slope")
    exact_log = 69.0 / (725_760.0 * math.pi**3)
    add_check(
        checks,
        "VAL4928_09_beta_expansion",
        "natural beta system has the canonical IR terms and exact positive log coefficient",
        exact_log,
        log_row["derived_value"],
        len(beta_rows) == 3
        and math.isclose(float(log_row["derived_value"]), exact_log, rel_tol=2.0e-15)
        and exact_log > 0.0,
    )

    fixed_rows = parsed["P8_Y5_R2FR_4928_FIXED_POINT.csv"]
    fixed = next(row for row in fixed_rows if row["fixed_point"] == "natural-scheme non-Gaussian")
    add_check(
        checks,
        "VAL4928_10_fixed_point",
        "natural non-Gaussian fixed point solves both beta functions",
        "g*=3pi/16; h*=-3.242484275319408e-7; beta norm near zero",
        f"g={fixed['g_star']}; h={fixed['g_C3_star']}; norm={fixed['beta_norm']}",
        len(fixed_rows) == 2
        and math.isclose(float(fixed["g_star"]), 3.0 * math.pi / 16.0, rel_tol=2.0e-15)
        and math.isclose(float(fixed["g_C3_star"]), -3.242484275319408e-7, rel_tol=2.0e-12)
        and float(fixed["beta_norm"]) < 1.0e-12,
    )
    add_check(
        checks,
        "VAL4928_11_critical_exponents",
        "stability matrix has one relevant and one irrelevant direction",
        "theta=(64/23,-7.75000535537)",
        f"theta=({fixed['theta_1']},{fixed['theta_2']})",
        math.isclose(float(fixed["theta_1"]), 64.0 / 23.0, rel_tol=2.0e-14)
        and math.isclose(float(fixed["theta_2"]), -7.75000535537, rel_tol=2.0e-11)
        and fixed["relevant_directions"] == "1",
    )

    independent_h_star, independent_theta_h, independent_log, independent_ir = independent_separatrix()
    add_check(
        checks,
        "VAL4928_12_independent_flow",
        "alternate-start independent integration reproduces the fixed point log slope and IR constant",
        "h*=-3.24248e-7; theta_h=-7.75001; c=3.06624e-6; A=3.02410e-6",
        f"h={independent_h_star}; theta={independent_theta_h}; c={independent_log}; A={independent_ir}",
        math.isclose(independent_h_star, -3.242484275319408e-7, rel_tol=2.0e-12)
        and math.isclose(independent_theta_h, -7.75000535537, rel_tol=3.0e-10)
        and math.isclose(independent_log, exact_log, rel_tol=2.0e-15)
        and math.isclose(independent_ir, 3.024098389340624e-6, rel_tol=2.0e-9),
    )

    separatrix_rows = parsed["P8_Y5_R2FR_4928_SEPARATRIX.csv"]
    infrared_rows = [row for row in separatrix_rows if as_bool(row["IR_sample"])]
    final_constant = float(separatrix_rows[-1]["log_subtracted_ratio"])
    ir_spread = max(float(row["log_subtracted_ratio"]) for row in infrared_rows) - min(
        float(row["log_subtracted_ratio"]) for row in infrared_rows
    )
    add_check(
        checks,
        "VAL4928_13_separatrix_convergence",
        "121-row unique separatrix converges to a stable log-subtracted infrared constant",
        "A=3.02409838934e-6 and IR spread below 1e-12",
        f"rows={len(separatrix_rows)}; A={final_constant}; spread={ir_spread}",
        len(separatrix_rows) == 121
        and math.isclose(final_constant, 3.024098389340624e-6, rel_tol=2.0e-13)
        and ir_spread < 1.0e-12,
    )

    log_sign_rows = parsed["P8_Y5_R2FR_4928_LOG_SIGN_AUDIT.csv"]
    log_sign = {row["audit_id"]: row for row in log_sign_rows}
    add_check(
        checks,
        "VAL4928_14_log_sign_audit",
        "attached beta sign article-text sign and reference-scale crossing are kept distinct",
        "notebook positive; prose negative; xi zero near 0.373",
        f"notebook={log_sign['LOG4928_00_notebook']['sign']}; prose={log_sign['LOG4928_01_article_text']['sign']}; xi={log_sign['LOG4928_03_reference_crossing']['result']}",
        len(log_sign_rows) == 4
        and log_sign["LOG4928_00_notebook"]["sign"] == "positive"
        and log_sign["LOG4928_01_article_text"]["sign"] == "negative"
        and math.isclose(
            float(log_sign["LOG4928_03_reference_crossing"]["result"]),
            0.3729706388575977,
            rel_tol=2.0e-13,
        ),
    )

    operator_rows = parsed["P8_Y5_R2FR_4928_OPERATOR_MAP.csv"]
    add_check(
        checks,
        "VAL4928_15_operator_map",
        "external G_C3 and MTS zeta_plus map to a_plus without a normalization gap",
        "zeta_+=G_C3 and a_+/lP^4=16pi r_C3",
        [row["result"] for row in operator_rows],
        len(operator_rows) == 3
        and all(as_bool(row["passed"]) for row in operator_rows)
        and "zeta_+=G_C3" in operator_rows[0]["relation"],
    )

    scale_rows = parsed["P8_Y5_R2FR_4928_REFERENCE_SCALE_SCAN.csv"]
    zero_row = min(scale_rows, key=lambda row: abs(float(row["r_C3_at_reference"])))
    add_check(
        checks,
        "VAL4928_16_reference_scale",
        "reference-scale scan reproduces the sign crossing and keeps it conditional",
        "eight rows and zero at xi=0.372970638857598",
        f"rows={len(scale_rows)}; xi={zero_row['xi_k0_over_MPl']}; r={zero_row['r_C3_at_reference']}",
        len(scale_rows) == 8
        and math.isclose(float(zero_row["xi_k0_over_MPl"]), 0.3729706388575977, rel_tol=2.0e-13)
        and abs(float(zero_row["r_C3_at_reference"])) < 1.0e-18,
    )

    conditional_rows = parsed["P8_Y5_R2FR_4928_CONDITIONAL_PREDICTION.csv"]
    natural = next(row for row in conditional_rows if row["branch"] == "natural_regulator_reproduced")
    add_check(
        checks,
        "VAL4928_17_conditional_prediction",
        "natural pure-gravity branch maps to the calculated sub-Planckian MTS cubic length",
        "ell=1.794635816842645e-36 m and compact ratio below 1e-150",
        f"ell={natural['ell_plus_m']}; ratio={natural['ratio_to_NS_one_percent_target']}",
        len(conditional_rows) == 2
        and math.isclose(float(natural["ell_plus_m"]), 1.794635816842645e-36, rel_tol=2.0e-14)
        and float(natural["ratio_to_NS_one_percent_target"]) < 1.0e-150
        and natural["status"] == "CONDITIONAL_PURE_GRAVITY_TRUNCATION",
    )

    inheritance_rows = parsed["P8_Y5_R2FR_4928_PARENT_INHERITANCE_GATE.csv"]
    inheritance = {row["clause"]: row for row in inheritance_rows}
    satisfied_count = sum(as_bool(row["MTS_clause_satisfied"]) for row in inheritance_rows[:-1])
    add_check(
        checks,
        "VAL4928_18_inheritance_gate",
        "three kinematic clauses close while six dynamic or scale clauses block an MTS prediction",
        "3 of 9 base clauses satisfied; all_dynamic false",
        f"satisfied={satisfied_count}; all={inheritance['all_dynamic_inheritance']['MTS_clause_satisfied']}",
        len(inheritance_rows) == 10
        and satisfied_count == 3
        and not as_bool(inheritance["all_dynamic_inheritance"]["MTS_clause_satisfied"])
        and as_bool(inheritance["all_dynamic_inheritance"]["blocks_MTS_numeric_prediction"]),
    )

    freeze_rows = parsed["P8_Y5_R2FR_4928_OBSERVATIONAL_WILSON_FREEZE.csv"]
    freeze = {row["freeze_id"]: row for row in freeze_rows}
    add_check(
        checks,
        "VAL4928_19_Wilson_freeze",
        "one signed RG-invariant observational parameter is retained with separate QNM branches",
        "six rows; robust bound +/-5.873319830123418e18 m^4; one parameter",
        f"rows={len(freeze_rows)}; interval=({freeze['WF4928_00_parameter']['lower']},{freeze['WF4928_00_parameter']['upper']})",
        len(freeze_rows) == 6
        and math.isclose(float(freeze["WF4928_00_parameter"]["upper"]), 5.873319830123418e18, rel_tol=2.0e-14)
        and math.isclose(float(freeze["WF4928_00_parameter"]["lower"]), -5.873319830123418e18, rel_tol=2.0e-14)
        and all(row["independent_IR_test_parameters"] in {"0", "1"} for row in freeze_rows)
        and freeze["WF4928_00_parameter"]["independent_IR_test_parameters"] == "1",
    )

    gate_rows = parsed["P8_Y5_R2FR_4928_GATE_DECISION.csv"]
    gate = {row["gate"]: row for row in gate_rows}
    add_check(
        checks,
        "VAL4928_20_gate_state",
        "conditional flow is calculated but MTS inheritance and compact/full promotion remain false",
        "kinematic derived; dynamic not derived; one Wilson; weak retained; compact/full false",
        f"kinematic={gate['integrated_H_kinematic_compatibility']['status']}; dynamic={gate['MTS_dynamic_flow_inheritance']['status']}; compact={gate['compact_GR']['status']}",
        gate["integrated_H_kinematic_compatibility"]["status"] == "DERIVED"
        and gate["MTS_dynamic_flow_inheritance"]["status"] == "NOT_DERIVED"
        and gate["observational_Wilson_freeze"]["status"] == "ONE_SIGNED_PARAMETER_SELECTED"
        and gate["weak_GR_Newton_Maxwell"]["status"] == "RETAINED"
        and gate["compact_GR"]["status"] == "NOT_PROMOTED"
        and gate["full_MTS_to_GR"]["status"] == "NOT_PROMOTED"
        and gate["next_target"]["decision"] == NEXT_TARGET
        and all(not as_bool(row["claim_promoted"]) for row in gate_rows),
    )

    required_markers = {
        CHECKPOINT: MARKER,
        FORMAL_NOTE: FORMAL_MARKER,
        SOURCE / "PROVENANCE.md": "MTS_INTEGRATED_H_C3_FUNCTIONAL_FLOW_PROVENANCE_4928",
        RESUME: NEXT_TARGET,
        FORMAL / "02-claims-register.csv": "L-770",
        FORMAL / "04-variable-audit.csv": "C3FunctionalFlowStatus4928_MTS",
        FORMAL / "05-equation-register.md": "1.221 Integrated-H C3 functional flow and observational Wilson freeze",
        FORMAL / "06-consistency-red-team.md": "172. A pure-gravity fixed-point trajectory is not automatically the MTS ultraviolet trajectory",
        FORMAL / "07-unification-spine.md": "PPC4161 checkpoint 4928",
    }
    marker_problems = [
        path.name
        for path, marker in required_markers.items()
        if not path.exists() or marker not in source_text(path)
    ]
    add_check(
        checks,
        "VAL4928_21_registers",
        "checkpoint formal note provenance resume and five registers carry their markers",
        0,
        len(marker_problems),
        not marker_problems,
    )

    required_variables = {
        "NaturalNewtonCoupling4928_MTS",
        "NaturalC3Coupling4928_MTS",
        "C3NaturalBetaFlow4928_MTS",
        "C3NaturalFixedPoint4928_MTS",
        "C3CriticalExponents4928_MTS",
        "C3MasslessLogSlope4928_MTS",
        "C3SeparatrixConstant4928_MTS",
        "C3ReferenceScale4928_MTS",
        "IntegratedHFlowInheritance4928_MTS",
        "C3ObservationalWilson4928_MTS",
        "C3ConditionalLength4928_MTS",
        "C3FunctionalFlowStatus4928_MTS",
        "VacuumGRWeylC3Status4928_MTS",
    }
    variable_symbols = {row["symbol"] for row in read_csv(FORMAL / "04-variable-audit.csv")}
    add_check(
        checks,
        "VAL4928_22_variables",
        "all thirteen canonical checkpoint variables are registered",
        13,
        len(required_variables & variable_symbols),
        required_variables <= variable_symbols,
    )

    pycache_paths = list(SCRIPTS.rglob("__pycache__"))
    add_check(
        checks,
        "VAL4928_23_pycache",
        "scripts tree contains no Python bytecode cache directories",
        0,
        len(pycache_paths),
        not pycache_paths,
    )

    all_passed = all(as_bool(row["passed"]) for row in checks)
    add_check(
        checks,
        "VAL4928_OVERALL",
        "checkpoint 4928 functional-flow derivation and claim-discipline validation",
        "all checks pass",
        f"{sum(as_bool(row['passed']) for row in checks)}/{len(checks)} pre-overall checks pass",
        all_passed,
    )
    write_csv(OUTPUT / "P8_Y5_BRR545_4928_VALIDATION.csv", checks)
    print(
        "P8_Y5_BRR545_4928_VALIDATION_PASS"
        if all_passed
        else "P8_Y5_BRR545_4928_VALIDATION_FAIL"
    )
    print(f"checks_passed={sum(as_bool(row['passed']) for row in checks)}/{len(checks)}")
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
