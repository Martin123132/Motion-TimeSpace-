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
SOURCE = POST / "source-intake" / "functional_rg" / "4937"
OUTPUT_DIR = POST / "source-intake" / "mts_residuals"
OUTPUT = OUTPUT_DIR / "P8_Y5_BRR545_4937_VALIDATION.csv"

HESSIAN_SCRIPT = POST / "scripts" / "Y5_R2FR_4937_gravity_motion_block_hessian.py"
FIXED_SCRIPT = POST / "scripts" / "Y5_R2FR_4937_functional_potential_fixed_gate.py"
CHECKPOINT = POST / "4937-Y5-R2FR-gravity-motion-functional-potential-Hessian-and-one-scale-fixed-function-gate.md"
FORMAL_NOTE = FORMAL / "953-PPC4161-gravity-motion-functional-Hessian-and-one-scale-gate.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

PARENT_ACTION = POST / "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md"
TRAJECTORY = POST / "source-intake" / "functional_rg" / "4935" / "completed_fixed_point_trajectory_results.json"
ARCHIVE_1911 = SOURCE / "1911.06100v3.tar"
ARCHIVE_2111 = SOURCE / "2111.04696v2.tar"
ARCHIVE_2110 = SOURCE / "2110.09566v1.tar"
SOURCE_1911 = SOURCE / "src-1911.06100v3" / "Eff_Scalar_Pot_ASQG.tex"
SOURCE_2111 = SOURCE / "src-2111.04696v2" / "Rsquared.tex"
SOURCE_2110 = SOURCE / "src-2110.09566v1" / "SSTwAS.tex"
SOURCE_2204 = POST / "source-intake" / "functional_rg" / "4929" / "src2204" / "R2scalarMES.tex"

HESSIAN_JSON = SOURCE / "gravity_motion_block_hessian_results.json"
SERIES_CSV = SOURCE / "fractional_mixing_power_series.csv"
FIXED_JSON = SOURCE / "functional_potential_fixed_gate_results.json"
ROOTS_CSV = SOURCE / "constant_potential_root_spectrum.csv"
MES_CSV = SOURCE / "minimal_essential_motion_spectrum.csv"
SHOOTING_CSV = SOURCE / "fixed_function_shooting_scan.csv"
COMPATIBILITY_CSV = SOURCE / "fixed_function_compatibility_brackets.csv"

MARKER = "MTS_GRAVITY_MOTION_FUNCTIONAL_HESSIAN_ONE_SCALE_GATE_4937"
FORMAL_MARKER = "PPC4161_GRAVITY_MOTION_FUNCTIONAL_HESSIAN_ONE_SCALE_GATE_4937"
VALIDATION_MARKER = "MTS_GRAVITY_MOTION_FUNCTIONAL_HESSIAN_VALIDATION_4937"
NEXT_TARGET = "4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-two-scale-theory-gate.md"
CHECKED_DATE = "2026-07-12"

SCRIPTS = (HESSIAN_SCRIPT, FIXED_SCRIPT, Path(__file__))
EVIDENCE_CSV = (
    SERIES_CSV,
    ROOTS_CSV,
    MES_CSV,
    SHOOTING_CSV,
    COMPATIBILITY_CSV,
)
HASH_LOCKS = {
    PARENT_ACTION: "4c20db8f8f75d81bab3c2a6d334cbcefeb2f2c1d66266be0ec412947c705b636",
    TRAJECTORY: "8793e369ba0a9726c43dc64fe454ba87f88876832eca0ba9b79f07b171d1e222",
    ARCHIVE_1911: "def9f823cadc2ab5a23c064784ecfe877fa4ddbcc28fd4ccaf318887030e45e6",
    ARCHIVE_2111: "f3e291cf0b62efb513b18116b034ba3ddbf59e7aa6b051aec2fdd48a9fd2c0d9",
    ARCHIVE_2110: "2ef680490ccf2e3f86cc8ff7f926fdd7e612345284948dd7775417326e617156",
    SOURCE_1911: "5d742ca63e93e1715adfba01f83c6c6cf2fcbbdb57407cb472eee5133914b9b9",
    SOURCE_2111: "7c857e1ccdd7569874ca8a439f62afee24994d4389c2c4bec772b4620b949bb0",
    SOURCE_2110: "09e4775df76bf3e2024be7f2ec655a125436dbb6042779bc71fe03f6f7e5d778",
    SOURCE_2204: "56a906bdfef4af8c1e7a337263636bd0b2d5c863b5d5c52382385b655da4bdd7",
    HESSIAN_SCRIPT: "7cffac9c37bcdcdee07ff5b35225021f303e44338a72b5864caa3955fbb2e650",
    FIXED_SCRIPT: "b4ed9269d6077f2d2ed96cfa93fde57ba8c835e83475fd37b5c0db129829af2c",
    HESSIAN_JSON: "48303c49eac3f41d0e3ba93e9fb82c8cd7f79fc1cc9717f006dba8cc4ecbed73",
    SERIES_CSV: "4207e169a81b27de911a2e8edb1d44dd7f096098a78f0fa3160471e7b5012e84",
    FIXED_JSON: "a965b75e5b5576e579bb4812b14a0e220a1b18b4e9653f4e83d714c4caf8a361",
    ROOTS_CSV: "fcc85c2120d5a6546352de7ef3433afb6fd45d74aa68c0e89b4c21c909366a79",
    MES_CSV: "054273203419412b4470e28b11de0a2ca3ac41be7f55118f7d2772f74e4bf9ec",
    SHOOTING_CSV: "617de46eec17595c0791401f175b453d44be252a009a9045f1f3ca6f5fe58f91",
    COMPATIBILITY_CSV: "9a5189a1090ec43667bfe9c4bb53a3cf23252437f724aecb5cad6c72ddded95b",
    CHECKPOINT: "2cf1f25d7cf67ec9bb724381919a9ff6e78d5dabe355ec50178157309b29cce5",
    FORMAL_NOTE: "5802cedcfe061e123e679b141aff0f48aded11bb3ae9fd66c8c4ad907b771cd2",
    PROVENANCE: "44aa6b41ea1cd470c4fbad94e21f66a4aea9cbb99a701ff37e771eb90f50473c",
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
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
    )


def main() -> int:
    checks: list[dict[str, Any]] = []
    required = [
        *SCRIPTS,
        *HASH_LOCKS,
        CHECKPOINT,
        FORMAL_NOTE,
        PROVENANCE,
        CLAIMS,
        VARIABLES,
        EQUATIONS,
        RED_TEAM,
        SPINE,
        RESUME,
    ]
    missing = sorted(str(path) for path in set(required) if not path.exists())
    add_check(
        checks,
        "VAL4937_00_paths",
        "all parent primary-source script evidence document and register paths exist",
        "0 missing paths",
        str(missing),
        not missing,
    )

    syntax_errors = []
    for path in SCRIPTS:
        try:
            compile(read_text(path), str(path), "exec")
        except SyntaxError as error:
            syntax_errors.append(f"{path.name}:{error}")
    add_check(
        checks,
        "VAL4937_01_compile",
        "all three checkpoint scripts compile without bytecode",
        "0 syntax errors",
        str(syntax_errors),
        not syntax_errors,
    )

    hash_failures = []
    for path, expected in HASH_LOCKS.items():
        actual = digest(path) if path.exists() else "MISSING"
        if actual != expected:
            hash_failures.append(f"{path.name}:{actual}")
    add_check(
        checks,
        "VAL4937_02_hashes",
        "all parent primary sources scripts artifacts and checkpoint documents match locked hashes",
        f"{len(HASH_LOCKS)} matches",
        "OK" if not hash_failures else str(hash_failures),
        not hash_failures,
    )

    hessian = load_json(HESSIAN_JSON)
    add_check(
        checks,
        "VAL4937_03_hessian_internal",
        "all direct variation canonical normalization inverse and series checks pass",
        "all true",
        str(hessian["checks"]),
        all(hessian["checks"].values()),
    )
    hessian_boundary = hessian["claim_boundary"]
    hessian_boundary_ok = (
        hessian_boundary["off_shell_gravity_motion_Hessian_derived"]
        and hessian_boundary["optimized_mixed_potential_trace_derived"]
        and not hessian_boundary["fractional_q_cancellation_found"]
        and not hessian_boundary["regulator_independent_no_go_claimed"]
        and not hessian_boundary["full_MTS_fixed_function_derived"]
        and not hessian_boundary["local_GR_Newton_Maxwell_promoted"]
    )
    add_check(
        checks,
        "VAL4937_04_hessian_boundary",
        "the Hessian and declared trace are derived without a universal no-go or local promotion",
        "Hessian=true; trace=true; cancellation=false; universal=false; local=false",
        str(hessian_boundary),
        hessian_boundary_ok,
    )

    series_rows = read_csv(SERIES_CSV)
    q_rows = [row for row in series_rows if row["q_power"] == "1"]
    series_ok = (
        len(series_rows) == 8
        and len(q_rows) == 2
        and all(row["mixing_only_coefficient"] == "0" for row in q_rows)
        and all(
            row["full_flow_coefficient"] == "3/(32*pi**2*g_tilde)"
            for row in q_rows
        )
        and {row["r_sigma"] for row in q_rows} == {"1", "4/3"}
    )
    add_check(
        checks,
        "VAL4937_05_fractional_series",
        "both regulator normalizations retain the scalar q source and have zero mixed q coefficient",
        "8 rows; two q rows; mixed q=0; full q=3/(32pi^2gtilde)",
        str(q_rows),
        series_ok,
    )

    fixed = load_json(FIXED_JSON)
    add_check(
        checks,
        "VAL4937_06_fixed_internal",
        "all constant-root spectrum MES shooting and scale-lock checks pass",
        "all true",
        str(fixed["checks"]),
        all(fixed["checks"].values()),
    )

    root_rows = read_csv(ROOTS_CSV)
    low_roots = [row for row in root_rows if row["branch"] == "low"]
    high_roots = [row for row in root_rows if row["branch"] == "high_near_barrier"]
    roots_ok = (
        len(root_rows) == 4
        and len(low_roots) == 2
        and len(high_roots) == 2
        and all(float(row["theta_mass_n2"]) > 1.84 for row in low_roots)
        and all(row["compatible_with_current_MES_v_branch"] == "True" for row in low_roots)
        and all(float(row["TT_pole_margin_1_minus_v"]) < 0.04 for row in high_roots)
        and all(row["compatible_with_current_MES_v_branch"] == "False" for row in high_roots)
    )
    add_check(
        checks,
        "VAL4937_07_roots",
        "four roots parse; low roots have relevant mass and MES compatibility; high roots are near-pole and incompatible",
        "4 rows; low theta_mass>1.84 and MES=true; high margin<0.04 and MES=false",
        str(root_rows),
        roots_ok,
    )

    mes_rows = read_csv(MES_CSV)
    mes_ok = (
        len(mes_rows) == 2
        and {row["mapping"] for row in mes_rows}
        == {
            "Wetterich_v_equals_plus_2lambda",
            "Wetterich_v_equals_minus_2lambda",
        }
        and all(row["mass_direction_relevant"] == "True" for row in mes_rows)
        and all(float(row["theta_mass_n2"]) > 1.84 for row in mes_rows)
        and all(row["fractional_is_regular_eigenoperator"] == "False" for row in mes_rows)
    )
    add_check(
        checks,
        "VAL4937_08_MES_signs",
        "both action-sign maps retain a relevant regular mass and reject the fractional power as a regular eigenoperator",
        "2 maps; mass relevant; theta_mass>1.84; fractional regular=false",
        str(mes_rows),
        mes_ok,
    )

    shooting_rows = read_csv(SHOOTING_CSV)
    nonconstant_rows = [row for row in shooting_rows if float(row["mass_squared"]) != 0.0]
    analytic_rows = [row for row in shooting_rows if row["termination"] == "ANALYTIC_CONSTANT_GLOBAL"]
    shooting_ok = (
        len(shooting_rows) == 72
        and len(nonconstant_rows) == 68
        and len(analytic_rows) == 4
        and all(row["termination"] != "PHI_MAX_REACHED" for row in nonconstant_rows)
        and all(abs(float(row["boundary_residual"])) < 1.0e-9 for row in shooting_rows)
    )
    add_check(
        checks,
        "VAL4937_09_shooting",
        "the 72-row scan has four analytic constants and no generic nonconstant target reach",
        "72 rows; 68 nonconstant; 4 analytic; 0 nonconstant PHI_MAX; boundary residual<1e-9",
        str(
            {
                "rows": len(shooting_rows),
                "nonconstant": len(nonconstant_rows),
                "analytic": len(analytic_rows),
                "nonconstant_target": sum(
                    row["termination"] == "PHI_MAX_REACHED"
                    for row in nonconstant_rows
                ),
            }
        ),
        shooting_ok,
    )

    compatibility_rows = read_csv(COMPATIBILITY_CSV)
    compatibility_ok = (
        len(compatibility_rows) == 4
        and all(
            row["status"]
            == "FINITE_FIELD_TERMINATION_TRANSITION_NOT_GLOBAL_SOLUTION"
            for row in compatibility_rows
        )
        and all(float(row["mass_bracket_width"]) > 0.0 for row in compatibility_rows)
    )
    add_check(
        checks,
        "VAL4937_10_termination_transitions",
        "all four narrow transition brackets remain finite-field non-global diagnostics",
        "4 rows; finite-field termination status; positive bracket width",
        str(compatibility_rows),
        compatibility_ok,
    )

    scale_lock = fixed["scale_lock_contract"]
    scale_lock_ok = (
        scale_lock["dimensionless_invariant"]
        == "I_M=gtilde_psi g^(4/3)=g_psi G_N^(4/3)"
        and scale_lock["canonical_Gaussian_value"] == "0"
        and "c_m I_M^(3/8)" in scale_lock["mass_ratio"]
    )
    add_check(
        checks,
        "VAL4937_11_scale_lock",
        "the unique Newton-motion invariant and zero canonical logarithmic beta are recorded without selecting a value",
        "I_M exact; canonical beta=0; mass ratio contains c_m I_M^(3/8)",
        str(scale_lock),
        scale_lock_ok,
    )

    fixed_boundary = fixed["claim_boundary"]
    fixed_boundary_ok = (
        fixed_boundary["declared_functional_flow_solved_at_constant_roots"]
        and fixed_boundary["regular_linear_spectrum_derived"]
        and fixed_boundary["MES_sign_robust_mass_relevance_derived"]
        and not fixed_boundary["global_nonconstant_no_go_theorem"]
        and not fixed_boundary["one_scale_MTS_fixed_function_derived"]
        and not fixed_boundary["O4_beta_frozen_to_zero"]
        and not fixed_boundary["full_MTS_fixed_point_and_trajectory"]
        and not fixed_boundary["local_GR_Newton_Maxwell_promoted"]
    )
    add_check(
        checks,
        "VAL4937_12_claim_boundary",
        "solved roots and spectrum remain firewalled from universal no-go one-scale O4 full-MTS and local claims",
        "roots/spectrum/MES=true; no-go/one-scale/O4-freeze/full/local=false",
        str(fixed_boundary),
        fixed_boundary_ok,
    )

    checkpoint_text = read_text(CHECKPOINT)
    checkpoint_ok = (
        MARKER in checkpoint_text
        and NEXT_TARGET in checkpoint_text
        and "global nonconstant no-go theorem                  = false" in checkpoint_text
        and "local GR/Newton/Maxwell promotion                  = false" in checkpoint_text
    )
    add_check(
        checks,
        "VAL4937_13_checkpoint",
        "the checkpoint states the marker next target and explicit nonclaim boundaries",
        "marker; next target; global no-go=false; local=false",
        "OK" if checkpoint_ok else "missing checkpoint boundary text",
        checkpoint_ok,
    )

    formal_text = read_text(FORMAL_NOTE)
    formal_ok = (
        FORMAL_MARKER in formal_text
        and "one-scale unchanged-parent branch       = false" in formal_text
        and "full MTS/local-GR promotion             = false" in formal_text
    )
    add_check(
        checks,
        "VAL4937_14_formal_note",
        "the formal note records one-scale and local-GR failure boundaries",
        "formal marker; one-scale=false; local=false",
        "OK" if formal_ok else "missing formal boundary text",
        formal_ok,
    )

    claim_rows = read_csv(CLAIMS)
    claim_matches = [row for row in claim_rows if row["claim_id"] == "L-779"]
    claim_ok = (
        len(claim_matches) == 1
        and "one_scale_branch_rejected" in claim_matches[0]["status"]
        and NEXT_TARGET in claim_matches[0]["next_test"]
        and "LOCAL_GR_FALSE" in claim_matches[0]["notes"]
    )
    add_check(
        checks,
        "VAL4937_15_claim_register",
        "claim L-779 records the rejected one-scale branch next test and local boundary",
        "one row; status contains rejection; next=4938; LOCAL_GR_FALSE",
        str(claim_matches),
        claim_ok,
    )

    expected_variables = {
        "GravityMotionHessian4937_MTS",
        "PhysicalTrace4937_MTS",
        "MixedTrace4937_MTS",
        "FractionalCancellation4937_MTS",
        "ConstantRoots4937_MTS",
        "GravityAnomalousA4937_MTS",
        "MotionSpectrum4937_MTS",
        "MESMotionMass4937_MTS",
        "FixedFunctionShooting4937_MTS",
        "MotionNewtonInvariant4937_MTS",
        "O4FlatBoundary4937_MTS",
        "PredictivityStatus4937_MTS",
    }
    variable_rows = read_csv(VARIABLES)
    found_variables = {
        row["symbol"] for row in variable_rows if row["symbol"] in expected_variables
    }
    variable_ok = found_variables == expected_variables
    add_check(
        checks,
        "VAL4937_16_variables",
        "all twelve checkpoint variables are registered",
        str(sorted(expected_variables)),
        str(sorted(found_variables)),
        variable_ok,
    )

    equation_text = read_text(EQUATIONS)
    equation_ok = (
        "## 1.230 Gravity-motion functional Hessian and scale-lock gate" in equation_text
        and "I_M=gtilde_psi g^(4/3)=g_psi G_N^(4/3)" in equation_text
        and "partial_tu=3/(32pi^2gtilde)" in equation_text
    )
    add_check(
        checks,
        "VAL4937_17_equations",
        "equation section 1.230 records the mixed source and scale-lock invariant",
        "section 1.230; q source; I_M invariant",
        "OK" if equation_ok else "missing equation register content",
        equation_ok,
    )

    red_text = read_text(RED_TEAM)
    red_ok = (
        "## 181. Mixed gravity does not automatically remove an independently relevant motion scale"
        in red_text
        and "do not claim canonical invariance fixes the value of I_M" in red_text
        and "do not promote full MTS local GR Newton Maxwell or galaxy exponents" in red_text
    )
    add_check(
        checks,
        "VAL4937_18_red_team",
        "red-team 181 prohibits invariant-value and broad-physics overclaims",
        "section 181; I_M prohibition; full/local prohibition",
        "OK" if red_ok else "missing red-team boundaries",
        red_ok,
    )

    spine_text = read_text(SPINE)
    spine_ok = (
        "## PPC4161 checkpoint 4937 - gravity-motion functional Hessian and scale lock"
        in spine_text
        and FORMAL_MARKER in spine_text
        and "full MTS/local-GR promotion                    = false" in spine_text
    )
    add_check(
        checks,
        "VAL4937_19_spine",
        "the unification spine records checkpoint 4937 and keeps local promotion false",
        "4937 section; formal marker; local=false",
        "OK" if spine_ok else "missing spine handoff",
        spine_ok,
    )

    resume_text = read_text(RESUME)
    resume_ok = (
        f"Last checkpoint: `{CHECKPOINT.name}`" in resume_text
        and FORMAL_MARKER in resume_text
        and NEXT_TARGET in resume_text
        and "Canonical Gaussian scaling preserves `I_M`" in resume_text
    )
    add_check(
        checks,
        "VAL4937_20_resume",
        "the resume points to 4937 and the exact 4938 scale-lock target",
        "last=4937; marker; next=4938; canonical invariant boundary",
        "OK" if resume_ok else "missing resume handoff",
        resume_ok,
    )

    evidence_failures = []
    for path in EVIDENCE_CSV:
        rows = read_csv(path)
        for index, row in enumerate(rows, start=2):
            claim_fields = [
                value
                for key, value in row.items()
                if key.startswith("valid_for")
            ]
            if not claim_fields or any(value != "False" for value in claim_fields):
                evidence_failures.append(f"{path.name}:{index}:claim flag")
            if any("MISSING_" in value for value in row.values() if value):
                evidence_failures.append(f"{path.name}:{index}:MISSING marker")
    add_check(
        checks,
        "VAL4937_21_evidence_firewall",
        "every generated CSV row remains private and contains no missing placeholder marker",
        "all valid_for*=False; zero MISSING_ markers",
        str(evidence_failures),
        not evidence_failures,
    )

    malformed = []
    for path in (CLAIMS, VARIABLES, *EVIDENCE_CSV):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            rows = list(reader)
        width = len(rows[0]) if rows else 0
        for index, row in enumerate(rows[1:], start=2):
            if len(row) != width:
                malformed.append(f"{path.name}:{index}:{len(row)}!={width}")
    add_check(
        checks,
        "VAL4937_22_csv_shape",
        "claim variable and generated CSV files have uniform row widths",
        "0 malformed rows",
        str(malformed),
        not malformed,
    )

    provenance_text = read_text(PROVENANCE)
    provenance_ok = all(
        expected in provenance_text
        for expected in (
            HASH_LOCKS[ARCHIVE_1911],
            HASH_LOCKS[ARCHIVE_2111],
            HASH_LOCKS[ARCHIVE_2110],
            HASH_LOCKS[SOURCE_1911],
            HASH_LOCKS[SOURCE_2111],
            HASH_LOCKS[SOURCE_2110],
            HASH_LOCKS[SOURCE_2204],
            "All CSV rows remain `valid_for_full_MTS_claim=false`",
        )
    )
    add_check(
        checks,
        "VAL4937_23_provenance",
        "provenance records all primary archive and TeX hashes plus the private firewall",
        "seven source hashes and valid_for_full_MTS_claim=false",
        "OK" if provenance_ok else "missing provenance string",
        provenance_ok,
    )

    pycache_paths = sorted(
        str(path) for path in (POST / "scripts").glob("__pycache__") if path.exists()
    )
    add_check(
        checks,
        "VAL4937_24_pycache",
        "checkpoint execution leaves no scripts __pycache__ directory",
        "[]",
        str(pycache_paths),
        not pycache_paths,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    failures = [row for row in checks if not row["passed"]]
    print(f"{VALIDATION_MARKER}_CHECKS={len(checks)}", flush=True)
    print(f"{VALIDATION_MARKER}_FAILURES={len(failures)}", flush=True)
    print(f"{VALIDATION_MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    if failures:
        for failure in failures:
            print(
                f"{VALIDATION_MARKER}_FAIL={failure['validation_id']}:{failure['actual']}",
                flush=True,
            )
        return 1
    print(f"{VALIDATION_MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
