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
SOURCE = POST / "source-intake" / "functional_rg" / "4939"
OUTPUT_DIR = POST / "source-intake" / "mts_residuals"
OUTPUT = OUTPUT_DIR / "P8_Y5_BRR545_4939_VALIDATION.csv"

MAIN_SCRIPT = POST / "scripts" / "Y5_R2FR_4939_O4_known_source_backreacted_family.py"
CHECKPOINT = POST / "4939-Y5-R2FR-two-scale-motion-O4-curved-flow-and-backreacted-GR-family-gate.md"
FORMAL_NOTE = FORMAL / "955-PPC4161-two-scale-O4-known-source-backreacted-GR-family.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
RESULT_JSON = SOURCE / "known_source_O4_and_backreacted_family_results.json"
SPECTRUM_CSV = SOURCE / "augmented_motion_backreacted_spectrum.csv"
FAMILY_CSV = SOURCE / "two_scale_backreacted_GR_family.csv"
RESIDUAL_CSV = SOURCE / "local_threshold_residual_family.csv"

COMPLETED_SCRIPT = POST / "scripts" / "Y5_R2FR_4934_completed_combined_flow.py"
COMPLETED_RESULT = POST / "source-intake" / "functional_rg" / "4934" / "completed_combined_flow_results.json"
TRAJECTORY_RESULT = POST / "source-intake" / "functional_rg" / "4935" / "completed_fixed_point_trajectory_results.json"
MOTION_ENTRY = POST / "source-intake" / "functional_rg" / "4935" / "motion_sector_entry_results.json"
FUNCTIONAL_GATE = POST / "4936-Y5-R2FR-motion-1PI-mass-and-O4-functional-trace-projection-or-two-scale-predictivity-gate.md"
FIXED_GATE = POST / "source-intake" / "functional_rg" / "4937" / "functional_potential_fixed_gate_results.json"
TWO_SCALE_GATE = POST / "4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-two-scale-theory-gate.md"
CURVED_SCALAR_SOURCE = POST / "source-intake" / "functional_rg" / "4937" / "src-2110.09566v1" / "SSTwAS.tex"

CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

MARKER = "MTS_O4_BACKREACTED_FAMILY_VALIDATION_4939"
CHECKPOINT_MARKER = "MTS_TWO_SCALE_O4_KNOWN_SOURCE_BACKREACTED_GR_FAMILY_GATE_4939"
FORMAL_MARKER = "PPC4161_TWO_SCALE_O4_KNOWN_SOURCE_BACKREACTED_GR_FAMILY_GATE_4939"
NEXT_TARGET = "4940-Y5-R2FR-curved-gravity-motion-O4-additive-source-and-full-invariant-submanifold-gate.md"
CHECKED_DATE = "2026-07-12"

EVIDENCE_CSV = (SPECTRUM_CSV, FAMILY_CSV, RESIDUAL_CSV)
HASH_LOCKS = {
    COMPLETED_SCRIPT: "c5fded8ca210607972c5d12640cdfd3e88ea3de48f84d1b699a3b2a7e342e230",
    COMPLETED_RESULT: "c70583d03ec773fb31aca0cb0ac73e662c66c6146ee8bfcdeb07598ddfe43978",
    TRAJECTORY_RESULT: "8793e369ba0a9726c43dc64fe454ba87f88876832eca0ba9b79f07b171d1e222",
    MOTION_ENTRY: "ba3dfdaacfb1e3d00282d82c4b4656a937e033cb9145e94c71b81e9c42a54240",
    FUNCTIONAL_GATE: "d24db400f3fb2fec75883bb078a37eec15b101e09c119f2a6ff43063d604c971",
    FIXED_GATE: "a965b75e5b5576e579bb4812b14a0e220a1b18b4e9653f4e83d714c4caf8a361",
    TWO_SCALE_GATE: "b30394a62c6a22af5da315b92a2823f44aa34cd914b6bab813136b0926aa0ca4",
    CURVED_SCALAR_SOURCE: "09e4775df76bf3e2024be7f2ec655a125436dbb6042779bc71fe03f6f7e5d778",
    MAIN_SCRIPT: "52b5d4aa68b5f5fccf0d0cff8e17d269a8ddad818e61ad113d0a2055127fd08d",
    RESULT_JSON: "3859aded9146696080bd7c0209f5a2385ef68ee2dac43ee293a5b864305dd041",
    SPECTRUM_CSV: "2c8b863ce041a32dad039775ecd479253fcb98f7dec39e7ce519262c2524324f",
    FAMILY_CSV: "5505fa7be52a84f49e086f96ce23ca2a768c0f8c739e5cdadba2d4cc7c52dc9f",
    RESIDUAL_CSV: "87d6320b1ecc1347fa519a2beb33f3b3e61ab48a5c933686bfdabf4e87fe3852",
    CHECKPOINT: "9da47eb0232980ca743c50617645c0d02cfaaeca58793a0d244bc9450418fa9e",
    FORMAL_NOTE: "b0281e42ffe8f2e2db94d360e5e156efc63b69e80809811c12fb19984c70f0c0",
    PROVENANCE: "755f3a9795dc1f96b0c2646c90b304e72269f50679bcc7f4b3a299e2dd603e93",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def add(
    checks: list[dict[str, Any]],
    check_id: str,
    requirement: str,
    expected: str,
    actual: Any,
    passed: bool,
) -> None:
    checks.append(
        {
            "validation_id": check_id,
            "requirement": requirement,
            "expected": expected,
            "actual": str(actual),
            "passed": passed,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
    )


def main() -> int:
    checks: list[dict[str, Any]] = []
    required = set(
        (
            Path(__file__),
            *HASH_LOCKS,
            CLAIMS,
            VARIABLES,
            EQUATIONS,
            RED_TEAM,
            SPINE,
            RESUME,
        )
    )
    missing = sorted(str(path) for path in required if not path.exists())
    add(checks, "VAL4939_00_paths", "all source artifact document and register paths exist", "[]", missing, not missing)

    syntax_errors = []
    for path in (MAIN_SCRIPT, Path(__file__)):
        try:
            compile(read_text(path), str(path), "exec")
        except SyntaxError as error:
            syntax_errors.append(f"{path.name}:{error}")
    add(checks, "VAL4939_01_compile", "both checkpoint scripts compile", "[]", syntax_errors, not syntax_errors)

    hash_failures = []
    for path, expected in HASH_LOCKS.items():
        actual = digest(path) if path.exists() else "MISSING"
        if actual != expected:
            hash_failures.append(f"{path.name}:{actual}")
    add(checks, "VAL4939_02_hashes", "all locked hashes match", f"{len(HASH_LOCKS)} matches", hash_failures, not hash_failures)

    result = json.loads(read_text(RESULT_JSON))
    add(checks, "VAL4939_03_internal", "all executed internal checks pass", "all true", result["checks"], all(result["checks"].values()))

    fixed = result["massless_scalar_backreacted_fixed_point"]
    coordinates = fixed["coordinates"]
    fixed_ok = (
        fixed["success"]
        and fixed["beta_residual_infinity_norm"] < 1.0e-9
        and 0.13 < coordinates["g"] < 0.132
        and fixed["gravity_relevant_directions"] == 1
        and max(abs(value) for value in fixed["relative_shift_from_4934"].values()) > 0.09
    )
    add(checks, "VAL4939_04_fixed", "scalar-backreacted point converges and materially shifts", "residual below 1e-9; one relevant; max shift above 9 percent", fixed, fixed_ok)

    gravity_values = fixed["gravity_beta_eigenvalues"]
    gravity_ok = (
        sum(row["real"] < 0.0 for row in gravity_values) == 1
        and sum(row["real"] > 0.0 for row in gravity_values) == 4
        and min(row["real"] for row in gravity_values if row["real"] > 0.0) > 0.21
    )
    add(checks, "VAL4939_05_gravity_spectrum", "shifted gravity spectrum has one relevant and a positive gap", "1 negative 4 positive gap above 0.21", gravity_values, gravity_ok)

    blocks = result["augmented_motion_blocks"]
    blocks_ok = (
        len(blocks) == 2
        and all(row["relevant_directions"] == 2 for row in blocks.values())
        and all(1.84 < row["theta_mass"] < 1.87 for row in blocks.values())
        and all(row["response_residual"] < 2.0e-16 for row in blocks.values())
    )
    add(checks, "VAL4939_06_blocks", "both mass blocks retain two relevant modes", "2 blocks; theta in range; response below 2e-16", blocks, blocks_ok)

    spectrum = read_csv(SPECTRUM_CSV)
    mappings = {row["mapping"] for row in spectrum}
    spectrum_ok = len(spectrum) == 12 and len(mappings) == 2
    for mapping in mappings:
        rows = [row for row in spectrum if row["mapping"] == mapping]
        spectrum_ok = spectrum_ok and (
            len(rows) == 6
            and sum(row["relevant"] == "True" for row in rows) == 2
            and sum(row["motion_mass_mode"] == "True" for row in rows) == 1
        )
    add(checks, "VAL4939_07_spectrum_csv", "spectrum table has two six-mode blocks", "12 rows and two relevant per block", sorted(mappings), spectrum_ok)

    family = read_csv(FAMILY_CSV)
    massless = [row for row in family if row["mapping"] == "massless_shared"]
    positive = [row for row in family if row["mapping"] != "massless_shared"]
    seeds = {float(row["relative_gravity_seed"]) for row in positive}
    R_values = {float(row["R_UV"]) for row in positive}
    positive_mappings = {row["mapping"] for row in positive}
    family_ok = (
        len(family) == 45
        and len(massless) == 3
        and len(positive) == 42
        and len(seeds) == 3
        and len(R_values) == 7
        and len(positive_mappings) == 2
        and all(row["termination"] == "IR_G_TARGET" for row in family)
        and all(abs(float(row["g_endpoint"]) - 1.0e-10) < 1.0e-22 for row in family)
        and all(float(row["J_gap_endpoint"]) > 0.0 for row in positive)
    )
    add(checks, "VAL4939_08_family", "all 45 finite-family rows reach the GR endpoint", "3 massless plus 42 positive; 2 maps x 3 seeds x 7 R", {"rows": len(family), "seeds": seeds, "R": R_values}, family_ok)

    convergence = result["trajectory_grid"]["J_gap_seed_convergence"]
    drifts = [
        row["max_relative_difference"]
        for mapping in convergence.values()
        for row in mapping.values()
    ]
    convergence_ok = len(drifts) == 14 and max(drifts) < 7.1e-6
    add(checks, "VAL4939_09_convergence", "all finite J maps are three-seed converged", "14 rows and max drift below 7.1e-6", max(drifts), convergence_ok)

    smallest_seed = 1.0e-6
    small_rows = [
        row
        for row in positive
        if float(row["relative_gravity_seed"]) == smallest_seed
        and float(row["R_UV"]) == 1.0e-12
    ]
    large_rows = [
        row
        for row in positive
        if float(row["relative_gravity_seed"]) == smallest_seed
        and float(row["R_UV"]) == 1.0
    ]
    small_K = [float(row["J_gap_endpoint"]) / float(row["R_UV"]) for row in small_rows]
    large_J = [float(row["J_gap_endpoint"]) for row in large_rows]
    nonlinear_ok = (
        len(small_K) == 2
        and all(0.2620 < value < 0.2630 for value in small_K)
        and sorted(large_J)[0] > 0.18
        and sorted(large_J)[1] < 0.21
        and all(value < 0.8 * small for value, small in zip(sorted(large_J), sorted(small_K)))
    )
    add(checks, "VAL4939_10_nonlinear_map", "finite backreaction reproduces the linear limit and bends at R=1", "small K about 0.262; large J between 0.18 and 0.21", {"small_K": small_K, "large_J": large_J}, nonlinear_ok)

    shift_fields = (
        "delta_W_plus_from_massless",
        "delta_W_minus_from_massless",
        "delta_W_C_from_massless",
        "delta_A_C3_from_massless",
    )
    maxima = {
        field: max(abs(float(row[field])) for row in positive)
        for field in shift_fields
    }
    wilson_ok = (
        maxima["delta_W_plus_from_massless"] < 6.7e-5
        and maxima["delta_W_minus_from_massless"] < 6.4e-4
        and maxima["delta_W_C_from_massless"] < 3.1e-6
        and maxima["delta_A_C3_from_massless"] < 7.7e-8
    )
    add(checks, "VAL4939_11_Wilson", "finite Wilson shifts remain bounded on the executed family", "declared four maxima", maxima, wilson_ok)

    residuals = read_csv(RESIDUAL_CSV)
    residual_ok = (
        len(residuals) == 42
        and all(math.isfinite(float(row["Delta_beta_g_over_g_endpoint"])) for row in residuals)
        and max(float(row["Delta_beta_g_over_g_endpoint"]) for row in residuals) < 5.31e-12
        and all(row["PPN_beta_gamma_residual"] == "NOT_DERIVED_FROM_RG_THRESHOLD" for row in residuals)
        and all(row["Maxwell_observable_residual"] == "INDIRECT_WILSON_SHIFT_ONLY" for row in residuals)
    )
    add(checks, "VAL4939_12_residuals", "RG residual rows remain finite and are not mislabeled as PPN or Maxwell", "42 rows; max below 5.31e-12; explicit nonclaims", len(residuals), residual_ok)

    o4 = result["O4_curved_source_audit"]
    o4_ok = (
        all(o4["exact_zero_sources"].values())
        and o4["remaining_source"] == "off-shell curved gravity-motion and mixed Hessian trace at C^2 p^2"
        and not o4["u4_zero_is_full_invariant_submanifold"]
        and o4["known_source_u4_zero_trajectory_is_diagnostic"]
    )
    add(checks, "VAL4939_13_O4", "scalar and photon O4 sources close while gravity-mixed remains open", "all known zeros true and full invariant false", o4, o4_ok)

    boundary = result["claim_boundary"]
    boundary_ok = (
        boundary["massless_scalar_fixed_point_backreaction_calculated"]
        and boundary["finite_mass_threshold_family_backreacted"]
        and boundary["neutral_scalar_direct_Maxwell_source_zero"]
        and boundary["scalar_and_photon_O4_sources_zero"]
        and not boundary["gravity_mixed_O4_source_derived"]
        and not boundary["u4_zero_full_parent_invariant"]
        and not boundary["physical_PPN_residual_derived"]
        and not boundary["full_MTS_fixed_point"]
        and not boundary["local_GR_Newton_Maxwell_promoted"]
    )
    add(checks, "VAL4939_14_boundary", "derived family stays firewalled from O4 PPN full-MTS and local claims", "known results true and promotions false", boundary, boundary_ok)

    checkpoint_text = read_text(CHECKPOINT)
    checkpoint_ok = (
        CHECKPOINT_MARKER in checkpoint_text
        and NEXT_TARGET in checkpoint_text
        and "gravity-mixed O4 source                         = open;" in checkpoint_text
        and "local GR/Newton/Maxwell promotion               = false." in checkpoint_text
    )
    add(checks, "VAL4939_15_checkpoint", "checkpoint records marker next target and nonclaims", "marker next 4940 O4 open local false", "OK" if checkpoint_ok else "missing", checkpoint_ok)

    formal_text = read_text(FORMAL_NOTE)
    formal_ok = (
        FORMAL_MARKER in formal_text
        and "gravity-mixed O4 source           = open;" in formal_text
        and "full MTS/local-GR promotion       = false." in formal_text
    )
    add(checks, "VAL4939_16_formal", "formal note records the O4 and local boundaries", "marker O4 open local false", "OK" if formal_ok else "missing", formal_ok)

    claim_matches = [row for row in read_csv(CLAIMS) if row["claim_id"] == "L-781"]
    claim_ok = (
        len(claim_matches) == 1
        and "finite_two_scale_family_backreacted" in claim_matches[0]["status"]
        and NEXT_TARGET in claim_matches[0]["next_test"]
        and "LOCAL_GR_FALSE" in claim_matches[0]["notes"]
    )
    add(checks, "VAL4939_17_claim", "claim L-781 records the finite-family boundary", "one row next 4940 and local false", claim_matches, claim_ok)

    expected_variables = {
        "ScalarThreshold4939_MTS",
        "BackreactedFixedPoint4939_MTS",
        "BackreactedSpectrum4939_MTS",
        "FiniteRUVFamily4939_MTS",
        "O4KnownSource4939_MTS",
        "O4GravityMixed4939_MTS",
        "IRWilsonResponse4939_MTS",
        "LocalThresholdResidual4939_MTS",
        "PredictivityStatus4939_MTS",
    }
    found_variables = {row["symbol"] for row in read_csv(VARIABLES) if row["symbol"] in expected_variables}
    add(checks, "VAL4939_18_variables", "all nine variables are registered", sorted(expected_variables), sorted(found_variables), found_variables == expected_variables)

    equation_text = read_text(EQUATIONS)
    equation_ok = (
        "## 1.232 Scalar-baseline fixed point, finite two-scale flow and O4 source split" in equation_text
        and "beta_utilde_O4" in equation_text
        and "J_gap,IR={0.200597389473,0.188519777494}." in equation_text
    )
    add(checks, "VAL4939_19_equations", "equation 1.232 records the finite flow and O4 split", "section finite J and O4 beta", "OK" if equation_ok else "missing", equation_ok)

    red_text = read_text(RED_TEAM)
    red_ok = (
        "## 183. A threshold derivative is not the enlarged fixed point" in red_text
        and "do not call u_O4=0 a full invariant submanifold" in red_text
        and "do not call Delta beta_g/g a PPN beta or gamma residual" in red_text
    )
    add(checks, "VAL4939_20_red_team", "red-team 183 prohibits spectator O4 and PPN overclaims", "section and three prohibitions", "OK" if red_ok else "missing", red_ok)

    spine_text = read_text(SPINE)
    spine_ok = (
        "## PPC4161 checkpoint 4939 - finite two-scale GR family and O4 source split" in spine_text
        and FORMAL_MARKER in spine_text
        and "full MTS/local-GR promotion                    = false;" in spine_text
    )
    add(checks, "VAL4939_21_spine", "spine records finite family and local nonclaim", "4939 marker local false", "OK" if spine_ok else "missing", spine_ok)

    resume_text = read_text(RESUME)
    resume_ok = (
        CHECKPOINT.name in resume_text
        and FORMAL_MARKER in resume_text
        and NEXT_TARGET in resume_text
        and "known-source" in resume_text
        and "diagnostic" in resume_text
    )
    add(checks, "VAL4939_22_resume", "resume points to 4939 and exact 4940 target", "checkpoint marker target and diagnostic boundary", "OK" if resume_ok else "missing", resume_ok)

    evidence_failures = []
    for path in EVIDENCE_CSV:
        for index, row in enumerate(read_csv(path), start=2):
            claim_fields = [value for key, value in row.items() if key.startswith("valid_for")]
            if not claim_fields or any(value != "False" for value in claim_fields):
                evidence_failures.append(f"{path.name}:{index}:claim")
            if any("MISSING_" in value for value in row.values() if value):
                evidence_failures.append(f"{path.name}:{index}:missing")
    add(checks, "VAL4939_23_firewall", "all evidence rows remain private and complete", "[]", evidence_failures, not evidence_failures)

    malformed = []
    for path in (CLAIMS, VARIABLES, *EVIDENCE_CSV):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.reader(handle))
        width = len(rows[0]) if rows else 0
        malformed.extend(
            f"{path.name}:{index}:{len(row)}!={width}"
            for index, row in enumerate(rows[1:], start=2)
            if len(row) != width
        )
    add(checks, "VAL4939_24_csv_shape", "all register and evidence CSV rows have uniform width", "[]", malformed, not malformed)

    provenance_text = read_text(PROVENANCE)
    provenance_ok = all(
        value in provenance_text
        for value in (
            HASH_LOCKS[COMPLETED_SCRIPT],
            HASH_LOCKS[COMPLETED_RESULT],
            HASH_LOCKS[MAIN_SCRIPT],
            HASH_LOCKS[RESULT_JSON],
            "P8_Y5_BRR545_4939_VALIDATION.csv",
            "valid_for_full_MTS_claim=false",
        )
    )
    add(checks, "VAL4939_25_provenance", "provenance records hashes validation and firewall", "all provenance tokens", "OK" if provenance_ok else "missing", provenance_ok)

    pycache = sorted(str(path) for path in (POST / "scripts").glob("__pycache__") if path.exists())
    add(checks, "VAL4939_26_pycache", "no scripts pycache remains", "[]", pycache, not pycache)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    failures = [row for row in checks if not row["passed"]]
    print(f"{MARKER}_CHECKS={len(checks)}", flush=True)
    print(f"{MARKER}_FAILURES={len(failures)}", flush=True)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    for failure in failures:
        print(f"{MARKER}_FAIL={failure['validation_id']}:{failure['actual']}", flush=True)
    if failures:
        return 1
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
