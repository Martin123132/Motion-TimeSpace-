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
SOURCE = POST / "source-intake" / "functional_rg" / "4940"
OUTPUT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_4940_VALIDATION.csv"
)

MAIN_SCRIPT = POST / "scripts" / "Y5_R2FR_4940_metric_kernel_O4_source_and_family.py"
RESULT_JSON = SOURCE / "metric_kernel_O4_source_and_family_results.json"
SPECTRUM_CSV = SOURCE / "O4_kernel_augmented_spectrum.csv"
FAMILY_CSV = SOURCE / "O4_kernel_GR_family.csv"
SOURCE_CSV = SOURCE / "O4_source_decomposition.csv"
GAUSSIAN_CSV = SOURCE / "gammaC2_gaussian_scaling.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = POST / "4940-Y5-R2FR-metric-kernel-O4-nonzero-source-self-backreacted-fixed-point-and-direct-trace-cancellation-gate.md"
FORMAL_NOTE = FORMAL / "956-PPC4161-metric-kernel-O4-source-and-direct-trace-gate.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
ESS_SOURCE = POST / "source-intake" / "functional_rg" / "4929" / "src2312" / "ess_cubic.tex"

RESULT_MARKER = "MTS_4940_METRIC_KERNEL_O4_SOURCE_AND_FAMILY"
CHECKPOINT_MARKER = "MTS_METRIC_KERNEL_O4_SOURCE_SELF_BACKREACTED_GATE_4940"
FORMAL_MARKER = "PPC4161_METRIC_KERNEL_O4_SOURCE_SELF_BACKREACTED_GATE_4940"
PROVENANCE_MARKER = "MTS_METRIC_KERNEL_O4_PROVENANCE_4940"
NEXT_TARGET = "4941-Y5-R2FR-direct-metric-scalar-C2p2-trace-and-O4-cancellation-or-shift-gate.md"

HASH_LOCKS = {
    MAIN_SCRIPT: "64c21710778a0298a2a6e770986bfce0bc5e372e95d5aae58a9aeb780f5b6989",
    RESULT_JSON: "4c4900dfe18f638801b1a0998ac40f9aa7d6eed9737c8c0a053b2cd2fa9d536a",
    SPECTRUM_CSV: "92493e8ecb238fd718a1928d01b7f5e788124f8e255a72beed1f0a8f2a7cae3a",
    FAMILY_CSV: "d6f6fd98c06cdf29ef842a8ab99aea1642ceb3e0a188d3c449b4d66ff6a97723",
    SOURCE_CSV: "9f3d33756600b0861d38c80a3f760795bf17c7c815a8d724a5477c4ba384150b",
    GAUSSIAN_CSV: "a76287f6de250d588e45f831230f3f69766169ed4534250a84ec811ae70cef58",
    CHECKPOINT: "3fac7373e840f707d855758ca3053e4315411058264782bcf51f49643d99dfef",
    FORMAL_NOTE: "73646172c3ec995a754a4235c010ac9b6615911d7b68ea81b5c5af5301ebbcc2",
    PROVENANCE: "b2d1a705b51b0814587d9deecb3577a15e7eacf30252179db95fdb58609b260d",
    ESS_SOURCE: "b23b0974509278be22c8917f531a2963d415184d9052e27860c65fad80943a1d",
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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def add(
    rows: list[dict[str, Any]],
    validation_id: str,
    test: str,
    expected: Any,
    actual: Any,
    passed: bool,
) -> None:
    rows.append(
        {
            "validation_id": validation_id,
            "test": test,
            "expected": json.dumps(expected, sort_keys=True, default=str),
            "actual": json.dumps(actual, sort_keys=True, default=str),
            "passed": bool(passed),
            "checkpoint_marker": RESULT_MARKER,
        }
    )


def main() -> int:
    checks: list[dict[str, Any]] = []

    missing_paths = [str(path) for path in HASH_LOCKS if not path.exists()]
    add(checks, "VAL4940_01_paths", "all locked source and artifact paths exist", [], missing_paths, not missing_paths)

    hash_failures = {
        str(path): {"expected": expected, "actual": digest(path)}
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "VAL4940_02_hashes", "all source and artifact hashes match", {}, hash_failures, not hash_failures)

    compile_failures: list[str] = []
    for path in (MAIN_SCRIPT, Path(__file__).resolve()):
        try:
            compile(read_text(path), str(path), "exec")
        except Exception as exc:  # pragma: no cover - recorded in ledger
            compile_failures.append(f"{path.name}:{type(exc).__name__}:{exc}")
    add(checks, "VAL4940_03_compile", "main and validation scripts compile without bytecode", [], compile_failures, not compile_failures)

    result = json.loads(read_text(RESULT_JSON))
    add(checks, "VAL4940_04_marker", "result marker is exact", RESULT_MARKER, result.get("marker"), result.get("marker") == RESULT_MARKER)

    internal_checks = result["checks"]
    failed_internal = [name for name, passed in internal_checks.items() if not passed]
    add(checks, "VAL4940_05_internal", "all calculation checks pass", [], failed_internal, not failed_internal)

    fixed = result["O4_completed_known_source_fixed_point"]
    coordinates = fixed["coordinates"]
    expected_coordinates = {
        "g": 0.13087813612487986,
        "g_plus": 0.3714660799104595,
        "g_minus": 3.4532084880347265,
        "g_CFF": 0.004095333544140413,
        "h_C3": 3.916801605590217e-06,
        "u_O4": -0.0018050754086485139,
    }
    coordinate_error = max(
        abs(float(coordinates[name]) - value)
        for name, value in expected_coordinates.items()
    )
    fixed_ok = (
        fixed["success"]
        and float(fixed["beta_residual_infinity_norm"]) < 1.0e-12
        and coordinate_error < 1.0e-13
    )
    add(checks, "VAL4940_06_fixed", "six-coordinate fixed point is reproduced", expected_coordinates, {"coordinates": coordinates, "residual": fixed["beta_residual_infinity_norm"], "max_error": coordinate_error}, fixed_ok)

    source_numeric_ok = (
        math.isclose(float(fixed["gamma_C2_at_fixed_point"]), -0.014440603269187884, rel_tol=0.0, abs_tol=1.0e-13)
        and math.isclose(float(fixed["metric_kernel_source_at_u_zero"]), 0.0072128143216457575, rel_tol=0.0, abs_tol=1.0e-13)
        and math.isclose(float(fixed["direct_trace_required_for_u_zero"]), -0.0072128143216457575, rel_tol=0.0, abs_tol=1.0e-13)
        and not fixed["u_zero_invariant_in_known_source_system"]
    )
    add(checks, "VAL4940_07_source_numeric", "kernel source and signed cancellation target are fixed", {"gamma_C2": -0.014440603269187884, "kernel": 0.0072128143216457575, "direct": -0.0072128143216457575, "u0_invariant": False}, {"gamma_C2": fixed["gamma_C2_at_fixed_point"], "kernel": fixed["metric_kernel_source_at_u_zero"], "direct": fixed["direct_trace_required_for_u_zero"], "u0_invariant": fixed["u_zero_invariant_in_known_source_system"]}, source_numeric_ok)

    six_values = sorted(float(row["real"]) for row in fixed["beta_eigenvalues"])
    six_ok = (
        len(six_values) == 6
        and sum(value < 0.0 for value in six_values) == 1
        and any(abs(value - 3.9960254522943828) < 1.0e-10 for value in six_values)
        and fixed["relevant_directions"] == 1
    )
    add(checks, "VAL4940_08_six_spectrum", "six-coordinate spectrum has one relevant and one irrelevant O4 mode", "6 modes; 1 negative; O4 about 3.99602545", six_values, six_ok)

    mass_blocks = result["mass_augmented_blocks"]
    mass_ok = (
        set(mass_blocks) == {"Wetterich_v_equals_plus_2lambda", "Wetterich_v_equals_minus_2lambda"}
        and all(block["relevant_directions"] == 2 for block in mass_blocks.values())
        and math.isclose(float(mass_blocks["Wetterich_v_equals_plus_2lambda"]["theta_mass"]), 1.8496934455116607, abs_tol=1.0e-11)
        and math.isclose(float(mass_blocks["Wetterich_v_equals_minus_2lambda"]["theta_mass"]), 1.858483853942984, abs_tol=1.0e-11)
    )
    add(checks, "VAL4940_09_mass_blocks", "both mass blocks retain exactly two relevant directions", "two mappings and theta_mass values", {name: {"theta_mass": block["theta_mass"], "relevant": block["relevant_directions"]} for name, block in mass_blocks.items()}, mass_ok)

    source_rows = read_csv(SOURCE_CSV)
    source_status = {row["source_id"]: row["status"] for row in source_rows}
    source_rows_ok = (
        len(source_rows) == 6
        and source_status.get("O4S4940_0_metric_kernel") == "DERIVED_NONZERO_COMPONENT"
        and source_status.get("O4S4940_1_scalar_C2_feedback") == "DERIVED_AND_INCLUDED"
        and source_status.get("O4S4940_2_scalar_RC2_feedback") == "DERIVED_AND_INCLUDED"
        and source_status.get("O4S4940_3_quadratic_scalar_external") == "EXACT_ZERO"
        and source_status.get("O4S4940_4_neutral_photon_external") == "EXACT_ZERO"
        and source_status.get("O4S4940_5_direct_gravity_mixed") == "OPEN_CANCELLATION_OR_SHIFT_TERM"
    )
    add(checks, "VAL4940_10_source_split", "source decomposition closes five components and leaves only direct mixed trace open", "six exact statuses", source_status, source_rows_ok)

    direct_row = next(row for row in source_rows if row["source_id"] == "O4S4940_5_direct_gravity_mixed")
    direct_open_ok = direct_row["fixed_numeric"] == "" and direct_row["beta_contribution"] == "not included"
    add(checks, "VAL4940_11_direct_open", "direct RHS trace is not silently zeroed or inserted", {"fixed_numeric": "", "beta_contribution": "not included"}, direct_row, direct_open_ok)

    spectrum_rows = read_csv(SPECTRUM_CSV)
    spectrum_ok = (
        len(spectrum_rows) == 14
        and sum(row["relevant"] == "True" for row in spectrum_rows) == 4
        and all(row["valid_for_full_MTS_claim"] == "False" for row in spectrum_rows)
        and all(row["checkpoint_marker"] == RESULT_MARKER for row in spectrum_rows)
    )
    add(checks, "VAL4940_12_spectrum_csv", "two seven-mode spectra are complete and firewalled", "14 rows; 4 relevant entries; all nonclaim", {"rows": len(spectrum_rows), "relevant": sum(row["relevant"] == "True" for row in spectrum_rows)}, spectrum_ok)

    gaussian_rows = read_csv(GAUSSIAN_CSV)
    gaussian_power = float(result["Gaussian_gammaC2_scaling"]["fit_power"])
    gaussian_ok = (
        len(gaussian_rows) >= 5
        and abs(gaussian_power - 2.0) < 5.0e-5
        and all(math.isfinite(float(row["gamma_C2_over_g2"])) for row in gaussian_rows)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in gaussian_rows)
    )
    add(checks, "VAL4940_13_gaussian", "gamma_C2 scales quadratically and W_O4 has a finite endpoint", "power 2 within 5e-5 and finite ratios", {"rows": len(gaussian_rows), "power": gaussian_power}, gaussian_ok)

    family_rows = read_csv(FAMILY_CSV)
    mapping_counts = {
        mapping: sum(row["mapping"] == mapping for row in family_rows)
        for mapping in {row["mapping"] for row in family_rows}
    }
    family_shape_ok = mapping_counts == {
        "massless_shared": 3,
        "Wetterich_v_equals_plus_2lambda": 21,
        "Wetterich_v_equals_minus_2lambda": 21,
    }
    add(checks, "VAL4940_14_family_shape", "family contains 3 controls and 42 positive-mass runs", {"massless_shared": 3, "Wetterich_v_equals_plus_2lambda": 21, "Wetterich_v_equals_minus_2lambda": 21}, mapping_counts, family_shape_ok)

    w_values = [float(row["W_O4_equals_u_over_g2"]) for row in family_rows]
    family_ir_ok = (
        all(row["termination"] == "IR_G_TARGET" for row in family_rows)
        and all(math.isclose(float(row["g_endpoint"]), 1.0e-10, rel_tol=1.0e-8, abs_tol=1.0e-20) for row in family_rows)
        and all(math.isfinite(value) for value in w_values)
        and min(w_values) > -3.320
        and max(w_values) < -3.318
    )
    add(checks, "VAL4940_15_family_IR", "all runs reach the IR with finite bounded W_O4", "45 IR targets and -3.320<W<-3.318", {"terminations": sorted({row["termination"] for row in family_rows}), "min_W": min(w_values), "max_W": max(w_values)}, family_ir_ok)

    positive_rows = [row for row in family_rows if row["mapping"] != "massless_shared"]
    finite_shift = max(abs(float(row["delta_W_O4_from_massless"])) for row in positive_rows)
    j_values = [float(row["J_gap_endpoint"]) for row in positive_rows]
    family_response_ok = all(value > 0.0 for value in j_values) and finite_shift < 7.5e-4
    add(checks, "VAL4940_16_family_response", "positive mass family keeps positive J_gap and bounded O4 displacement", "all J positive and max |Delta W|<7.5e-4", {"min_J": min(j_values), "max_J": max(j_values), "max_delta_W": finite_shift}, family_response_ok)

    convergence = result["trajectory_grid"]["O4_Wilson_seed_convergence"]
    max_drift = max(
        float(entry["max_relative_difference"])
        for mapping in convergence.values()
        for entry in mapping.values()
    )
    add(checks, "VAL4940_17_convergence", "three-seed W_O4 drift remains below 2e-6", 2.0e-6, max_drift, max_drift < 2.0e-6)

    boundary = result["claim_boundary"]
    boundary_ok = (
        boundary["metric_kernel_O4_source_derived"]
        and boundary["scalar_O4_C2_and_RC2_feedback_derived"]
        and boundary["known_source_O4_fixed_point_solved"]
        and boundary["known_source_O4_finite_family_integrated"]
        and not boundary["u_O4_zero_invariant_in_known_source_system"]
        and not boundary["direct_gravity_mixed_RHS_trace_derived"]
        and not boundary["full_O4_parent_fixed_point"]
        and not boundary["physical_PPN_Maxwell_residual_derived"]
        and not boundary["full_MTS_fixed_point"]
        and not boundary["local_GR_Newton_Maxwell_promoted"]
    )
    add(checks, "VAL4940_18_boundary", "derived O4 branch remains separated from full-parent and local claims", "known-source true; direct/full/local false", boundary, boundary_ok)

    checkpoint_text = read_text(CHECKPOINT)
    checkpoint_ok = (
        CHECKPOINT_MARKER in checkpoint_text
        and NEXT_TARGET in checkpoint_text
        and "direct metric-scalar/mixed RHS trace            = open;" in checkpoint_text
        and "local GR/Newton/Maxwell promotion               = false." in checkpoint_text
    )
    add(checks, "VAL4940_19_checkpoint", "checkpoint records exact source boundary and next target", "marker direct open local false next 4941", "OK" if checkpoint_ok else "missing", checkpoint_ok)

    formal_text = read_text(FORMAL_NOTE)
    formal_ok = FORMAL_MARKER in formal_text and "direct RHS mixed trace          = open;" in formal_text and "full MTS/local-GR promotion     = false." in formal_text
    add(checks, "VAL4940_20_formal", "formal note preserves direct and local nonclaims", "marker and two false/open rows", "OK" if formal_ok else "missing", formal_ok)

    claim_rows = [row for row in read_csv(CLAIMS) if row["claim_id"] == "L-782"]
    claim_ok = len(claim_rows) == 1 and NEXT_TARGET in claim_rows[0]["next_test"] and "DIRECT_RHS_TRACE_OPEN" in claim_rows[0]["notes"] and "LOCAL_GR_FALSE" in claim_rows[0]["notes"]
    add(checks, "VAL4940_21_claim", "claim L-782 is unique and firewalled", "one row with next target and open/local markers", claim_rows, claim_ok)

    expected_variables = {
        "gammaC24940_MTS",
        "MetricKernelO4Source4940_MTS",
        "O4ScalarFeedback4940_MTS",
        "uO4star4940_MTS",
        "O4FixedPoint4940_MTS",
        "O4Spectrum4940_MTS",
        "WO4IR4940_MTS",
        "DirectMixedO4Source4940_MTS",
        "PredictivityStatus4940_MTS",
    }
    found_variables = {row["symbol"] for row in read_csv(VARIABLES) if row["symbol"] in expected_variables}
    add(checks, "VAL4940_22_variables", "all nine 4940 variables are registered", sorted(expected_variables), sorted(found_variables), found_variables == expected_variables)

    equation_text = read_text(EQUATIONS)
    equation_ok = "## 1.233 Metric-kernel O4 source and self-backreacted fixed family" in equation_text and "beta_uO4" in equation_text and "-0.00721281432165" in equation_text
    add(checks, "VAL4940_23_equations", "equation 1.233 records source beta and cancellation value", "section beta and signed target", "OK" if equation_ok else "missing", equation_ok)

    red_text = read_text(RED_TEAM)
    red_ok = "## 184. A field-redefinition kernel acts on the matter action" in red_text and "do not set the remaining direct RHS trace to zero" in red_text and "do not call W_O4 a PPN" in red_text
    add(checks, "VAL4940_24_red_team", "red-team 184 blocks source erasure and observable overclaim", "section and two prohibitions", "OK" if red_ok else "missing", red_ok)

    spine_text = read_text(SPINE)
    spine_ok = "## PPC4161 checkpoint 4940 - parent-kernel O4 source and backreacted family" in spine_text and FORMAL_MARKER in spine_text and "full MTS/local-GR promotion                    = false;" in spine_text
    add(checks, "VAL4940_25_spine", "spine records O4 result and local boundary", "4940 marker and local false", "OK" if spine_ok else "missing", spine_ok)

    resume_text = read_text(RESUME)
    resume_ok = CHECKPOINT.name in resume_text and FORMAL_MARKER in resume_text and NEXT_TARGET in resume_text and "S_O4,direct,*=-0.00721281432165" in resume_text
    add(checks, "VAL4940_26_resume", "resume points to 4940 and exact 4941 calculation", "checkpoint marker target and signed value", "OK" if resume_ok else "missing", resume_ok)

    provenance_text = read_text(PROVENANCE)
    provenance_ok = PROVENANCE_MARKER in provenance_text and all(hash_value in provenance_text for path, hash_value in HASH_LOCKS.items() if path not in (PROVENANCE,)) and "valid_for_full_MTS_claim=False" in provenance_text
    add(checks, "VAL4940_27_provenance", "provenance records input and output hashes plus firewall", "all hashes and nonclaim token", "OK" if provenance_ok else "missing", provenance_ok)

    evidence_failures: list[str] = []
    for path in (SPECTRUM_CSV, FAMILY_CSV, SOURCE_CSV, GAUSSIAN_CSV):
        for index, row in enumerate(read_csv(path), start=2):
            claim_fields = [value for key, value in row.items() if key.startswith("valid_for")]
            if not claim_fields or any(value != "False" for value in claim_fields):
                evidence_failures.append(f"{path.name}:{index}:claim")
            if any("MISSING_" in value for value in row.values() if value):
                evidence_failures.append(f"{path.name}:{index}:missing")
    add(checks, "VAL4940_28_firewall", "all generated evidence rows remain complete private nonclaims", [], evidence_failures, not evidence_failures)

    malformed: list[str] = []
    for path in (CLAIMS, VARIABLES, SPECTRUM_CSV, FAMILY_CSV, SOURCE_CSV, GAUSSIAN_CSV):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.reader(handle))
        width = len(rows[0]) if rows else 0
        malformed.extend(
            f"{path.name}:{index}:{len(row)}!={width}"
            for index, row in enumerate(rows[1:], start=2)
            if len(row) != width
        )
    add(checks, "VAL4940_29_csv_shape", "register and evidence CSV rows have uniform widths", [], malformed, not malformed)

    pycache = sorted(str(path) for path in (POST / "scripts").glob("__pycache__") if path.exists())
    add(checks, "VAL4940_30_pycache", "no scripts pycache remains", [], pycache, not pycache)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    failures = [row for row in checks if not row["passed"]]
    print(f"{RESULT_MARKER}_VALIDATION_CHECKS={len(checks)}", flush=True)
    print(f"{RESULT_MARKER}_VALIDATION_FAILURES={len(failures)}", flush=True)
    print(f"{RESULT_MARKER}_VALIDATION_SHA256={digest(OUTPUT)}", flush=True)
    for failure in failures:
        print(f"{RESULT_MARKER}_VALIDATION_FAIL={failure['validation_id']}:{failure['actual']}", flush=True)
    if failures:
        return 1
    print(f"{RESULT_MARKER}_VALIDATION_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
