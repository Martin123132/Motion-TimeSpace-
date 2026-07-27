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
SOURCE = POST / "source-intake" / "functional_rg" / "4945"
OUTPUT = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4945_VALIDATION.csv"

MAIN_SCRIPT = POST / "scripts" / "Y5_R2FR_4945_primary_CFF_two_sign_geometry_and_local_certificate.py"
RESULT_JSON = SOURCE / "primary_CFF_two_sign_geometry_results.json"
SIGN_CSV = SOURCE / "polarization_sign_symmetry_and_bound_gate.csv"
GEOMETRY_CSV = SOURCE / "PSR_B1534_geometry_reconstruction.csv"
OPERATORS_CSV = SOURCE / "CFF_competing_operator_audit.csv"
LOCAL_CSV = SOURCE / "geometry_corrected_local_CFF_projection.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = POST / "4945-Y5-R2FR-primary-two-sided-CFF-likelihood-or-QCD-TJJ-dispersion-bound-and-local-Maxwell-certificate.md"
FORMAL_NOTE = FORMAL / "961-PPC4161-primary-CFF-sign-geometry-and-weak-local-certificate.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

RESULT_MARKER = "MTS_4945_PRIMARY_CFF_TWO_SIGN_GEOMETRY_LOCAL_CERTIFICATE"
CHECKPOINT_MARKER = "MTS_PRIMARY_CFF_TWO_SIGN_GEOMETRY_LOCAL_CERTIFICATE_4945"
FORMAL_MARKER = "PPC4161_PRIMARY_CFF_SIGN_GEOMETRY_LOCAL_CERTIFICATE_4945"
PROVENANCE_MARKER = "MTS_PRIMARY_CFF_SIGN_GEOMETRY_PROVENANCE_4945"
NEXT_TARGET = "4946-Y5-R2FR-QCD-TJJ-dispersive-matching-and-weak-local-Maxwell-action-certificate.md"

HASH_LOCKS = {
    MAIN_SCRIPT: "554605947ce4bb43b70369157fef879bbc6b89e735bc013a90a367d54088949a",
    RESULT_JSON: "41304044091f953cddbb7c95c6034fbdbe5df836a4156c4f762180cfb0247edc",
    SIGN_CSV: "8e77fbbee1264cb7e51f64f277587204805b03d02f6d2f0a843b1cee336c7b49",
    GEOMETRY_CSV: "3a06ece4500454765d8b43883941bd48047722a84677aa3f5c445ed67d0204fc",
    OPERATORS_CSV: "00c2002521524a14c4d762bce75e1250d49be0c703c05fc646f39c732e357a4c",
    LOCAL_CSV: "89d425abb47dbfda188f8fdb470a205bb46a00518a1ea48c01822f0ade67825a",
    PROVENANCE: "0f2d310d625ea00ba9d19247486522e83e3ce273312efa9b910b2ba986dc1e17",
    CHECKPOINT: "296c5567169674d953dd44782cf2b21ce7f2bae9f9651cef6e7ced7d483e961e",
    FORMAL_NOTE: "ef88d7c1a381f9ea9bd122839f49b7994a32035e5773283b0d12689e9da3b0ea",
}

SPEED_OF_LIGHT_M_PER_S = 299_792_458.0
SOLAR_MASS_TIME_S = 4.925490947e-6
SOURCE_ALLOWANCE_S = 1.0e-6
SOURCE_RADIUS_M = 10_000.0
SOURCE_PRINTED_BOUND_M2 = 6.0e6


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


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
            "expected": json.dumps(expected, sort_keys=True, default=str),
            "actual": json.dumps(actual, sort_keys=True, default=str),
            "passed": bool(passed),
            "checkpoint_marker": RESULT_MARKER,
        }
    )


def main() -> int:
    checks: list[dict[str, Any]] = []
    missing = [str(path) for path in HASH_LOCKS if not path.exists()]
    add(checks, "VAL4945_01_paths", "locked paths exist", [], missing, not missing)
    bad_hashes = {
        str(path): (expected, digest(path))
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "VAL4945_02_hashes", "locked hashes match", {}, bad_hashes, not bad_hashes)

    compile_errors: list[str] = []
    for path in (MAIN_SCRIPT, Path(__file__).resolve()):
        try:
            compile(text(path), str(path), "exec")
        except Exception as exc:
            compile_errors.append(f"{path.name}:{exc}")
    add(checks, "VAL4945_03_compile", "scripts compile in memory", [], compile_errors, not compile_errors)

    result = json.loads(text(RESULT_JSON))
    add(checks, "VAL4945_04_marker", "result marker", RESULT_MARKER, result.get("marker"), result.get("marker") == RESULT_MARKER)
    failed_internal = [name for name, passed in result["checks"].items() if not passed]
    add(checks, "VAL4945_05_internal", "research checks pass", [], failed_internal, not failed_internal)
    source_errors = [
        key
        for key, expected in result["source_hashes"].items()
        if not (ROOT / Path(key)).exists() or digest(ROOT / Path(key)) != expected
    ]
    add(checks, "VAL4945_06_sources", "result source paths and hashes", [], source_errors, not source_errors)

    signs = read_csv(SIGN_CSV)
    expected_sign_ids = {f"SIGN4945_{index:02d}_{suffix}" for index, suffix in enumerate((
        "mode_law",
        "label_swap",
        "signed_lag",
        "observed_split",
        "top_hat",
        "printed_bound_reproduction",
        "measured_geometry_bound",
        "raw_likelihood",
    ))}
    sign_ids = {row["gate_id"] for row in signs}
    sign_structure = (
        len(signs) == 8
        and sign_ids == expected_sign_ids
        and all(row["passed"] == "True" for row in signs)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in signs)
    )
    add(checks, "VAL4945_07_sign_rows", "eight sign rows", sorted(expected_sign_ids), sorted(sign_ids), sign_structure)
    sign_map = {row["gate_id"]: row for row in signs}
    parity_ok = (
        sign_map["SIGN4945_02_signed_lag"]["lambda_parity"] == "odd"
        and sign_map["SIGN4945_03_observed_split"]["lambda_parity"] == "even"
        and "T_plus(-lambda)=T_minus(lambda)" in sign_map["SIGN4945_01_label_swap"]["statement"]
    )
    add(checks, "VAL4945_08_sign_parity", "signed lag odd split even", True, parity_ok, parity_ok)
    likelihood_firewall = all(row["valid_for_raw_likelihood"] == "False" for row in signs)
    add(checks, "VAL4945_09_likelihood_firewall", "no sign row is raw likelihood", True, likelihood_firewall, likelihood_firewall)

    geometry = read_csv(GEOMETRY_CSV)
    expected_geometry_ids = {
        "G4945_00_DD_central",
        "G4945_01_DD_plus_1sigma",
        "G4945_02_DD_minus_1sigma",
        "G4945_03_DD_minus_2sigma_conservative",
        "G4945_04_DDGR_crosscheck",
    }
    geometry_ids = {row["geometry_id"] for row in geometry}
    geometry_structure = (
        len(geometry) == 5
        and geometry_ids == expected_geometry_ids
        and all(row["passed"] == "True" for row in geometry)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in geometry)
    )
    add(checks, "VAL4945_10_geometry_rows", "five geometry rows", sorted(expected_geometry_ids), sorted(geometry_ids), geometry_structure)
    geometry_map = {row["geometry_id"]: row for row in geometry}
    central = geometry_map["G4945_00_DD_central"]
    conservative = geometry_map["G4945_03_DD_minus_2sigma_conservative"]
    central_values = (
        math.isclose(float(central["physical_impact_parameter_m"]), 6.110828535952203e8, rel_tol=1e-12)
        and math.isclose(float(central["one_microsecond_abs_lambda_bound_m2"]), 1.1874270830489058e15, rel_tol=1e-12)
        and math.isclose(float(conservative["one_microsecond_abs_lambda_bound_m2"]), 1.3544193104492175e15, rel_tol=1e-12)
    )
    add(checks, "VAL4945_11_geometry_values", "central and conservative values", "locked", [central["physical_impact_parameter_m"], central["one_microsecond_abs_lambda_bound_m2"], conservative["one_microsecond_abs_lambda_bound_m2"]], central_values)
    physical_geometry = all(
        1.0 <= float(row["source_formula_geometry_factor"]) <= 2.0
        and abs(float(row["stationarity_residual"])) < 1.0e-11
        and float(row["impact_to_stated_radius_ratio"]) > 1.0e4
        for row in geometry
    )
    add(checks, "VAL4945_12_geometry_physical", "geometry factor stationarity and impact", True, physical_geometry, physical_geometry)

    source_mass_length_m = 1.33 * SOLAR_MASS_TIME_S * SPEED_OF_LIGHT_M_PER_S
    inferred_geometry = (
        SPEED_OF_LIGHT_M_PER_S
        * SOURCE_ALLOWANCE_S
        * SOURCE_RADIUS_M**2
        / (24.0 * source_mass_length_m * SOURCE_PRINTED_BOUND_M2)
    )
    printed_audit = result["printed_bound_audit"]
    printed_reject = (
        math.isclose(inferred_geometry, float(printed_audit["inferred_geometry_factor"]), rel_tol=1e-14)
        and inferred_geometry < 1.0
        and printed_audit["status"].startswith("nonreproducible")
        and not result["claim_boundary"]["source_printed_6e6_m2_bound_reproducible"]
    )
    add(checks, "VAL4945_13_printed_reject", "printed source bound rejected", "S inferred below one", inferred_geometry, printed_reject)
    conservative_bound = float(conservative["one_microsecond_abs_lambda_bound_m2"])
    bound_formula = SOURCE_ALLOWANCE_S / float(conservative["lag_coefficient_s_per_m2"])
    formula_ok = math.isclose(conservative_bound, bound_formula, rel_tol=1e-14)
    add(checks, "VAL4945_14_bound_formula", "conservative bound equals tau over K", conservative_bound, bound_formula, formula_ok)
    pulsar_linear = float(conservative["linear_CFF_parameter_at_bound"])
    add(checks, "VAL4945_15_pulsar_linear", "actual pulsar leg remains linear", "<1e-5", pulsar_linear, pulsar_linear < 1e-5)

    operators = read_csv(OPERATORS_CSV)
    expected_operator_ids = {f"OP4945_{index:02d}_{suffix}" for index, suffix in enumerate((
        "CFF",
        "Ricci_photon",
        "derivative_photon",
        "metric_GR",
        "cold_plasma",
        "magnetized_plasma",
        "intrinsic_modes_jitter",
        "QED_magnetic_vacuum",
        "parity_odd",
    ))}
    operator_ids = {row["operator_id"] for row in operators}
    operator_structure = (
        len(operators) == 9
        and operator_ids == expected_operator_ids
        and all(row["passed"] == "True" for row in operators)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in operators)
    )
    add(checks, "VAL4945_16_operator_rows", "nine operator rows", sorted(expected_operator_ids), sorted(operator_ids), operator_structure)
    operator_map = {row["operator_id"]: row for row in operators}
    projection_ok = (
        operator_map["OP4945_01_Ricci_photon"]["numeric_delay_envelope_s"] == "0.0"
        and operator_map["OP4945_02_derivative_photon"]["degeneracy_status"] == "ON_SHELL_REDUCED_NOT_DOUBLE_COUNTED"
        and operator_map["OP4945_03_metric_GR"]["degeneracy_status"] == "CANCELS_IN_IDEAL_POLARIZATION_DIFFERENCE"
    )
    add(checks, "VAL4945_17_operator_projection", "vacuum competitor projection", True, projection_ok, projection_ok)
    nuisance_ok = all(
        operator_map[key]["requires_joint_raw_fit"] == "True"
        for key in ("OP4945_04_cold_plasma", "OP4945_05_magnetized_plasma", "OP4945_06_intrinsic_modes_jitter")
    )
    add(checks, "VAL4945_18_nuisances", "plasma and source nuisances retained", True, nuisance_ok, nuisance_ok)
    qed_delay = float(operator_map["OP4945_07_QED_magnetic_vacuum"]["numeric_delay_envelope_s"])
    add(checks, "VAL4945_19_QED", "extreme QED magnetic delay negligible", "<1e-26 s", qed_delay, qed_delay < 1e-26)

    local = read_csv(LOCAL_CSV)
    expected_systems = {
        "Earth",
        "Sun",
        "one_solar_mass_white_dwarf",
        "1.4_solar_mass_12km_neutron_star",
        "10_solar_mass_Schwarzschild_horizon",
    }
    systems = {row["system"] for row in local}
    local_structure = (
        len(local) == 5
        and systems == expected_systems
        and all(row["passed"] == "True" for row in local)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in local)
    )
    add(checks, "VAL4945_20_local_rows", "five corrected local rows", sorted(expected_systems), sorted(systems), local_structure)
    local_map = {row["system"]: row for row in local}
    local_values = (
        math.isclose(float(local_map["Earth"]["geometry_corrected_abs_Delta_v_pol_over_c"]), 2.7874701720068493e-7, rel_tol=1e-12)
        and math.isclose(float(local_map["Sun"]["geometry_corrected_abs_Delta_v_pol_over_c"]), 7.127738104815346e-8, rel_tol=1e-12)
        and math.isclose(float(local_map["one_solar_mass_white_dwarf"]["geometry_corrected_abs_Delta_v_pol_over_c"]), 0.06997189310871497, rel_tol=1e-12)
    )
    add(checks, "VAL4945_21_local_values", "Earth Sun WD corrected values", "locked", [local_map[name]["geometry_corrected_abs_Delta_v_pol_over_c"] for name in ("Earth", "Sun", "one_solar_mass_white_dwarf")], local_values)
    weak_certificate = all(
        local_map[name]["valid_for_conditional_weak_local_CFF_certificate"] == "True"
        and float(local_map[name]["geometry_corrected_abs_Delta_v_pol_over_c"]) < 1e-6
        for name in ("Earth", "Sun")
    )
    add(checks, "VAL4945_22_weak_certificate", "Earth and Sun conditional certificate", True, weak_certificate, weak_certificate)
    compact_firewall = all(
        local_map[name]["linearized_transfer_below_ten_percent"] == "False"
        and local_map[name]["valid_for_conditional_weak_local_CFF_certificate"] == "False"
        and local_map[name]["status"] == "TRANSFER_OUTSIDE_LINEAR_CONTROL_NO_CERTIFICATE"
        for name in ("1.4_solar_mass_12km_neutron_star", "10_solar_mass_Schwarzschild_horizon")
    )
    add(checks, "VAL4945_23_compact_firewall", "compact transfer not promoted", True, compact_firewall, compact_firewall)
    universal_bound = {row["geometry_corrected_historical_abs_cgamma_bound_m2"] for row in local}
    add(checks, "VAL4945_24_universal", "one coefficient across systems", 1, len(universal_bound), len(universal_bound) == 1)

    boundary = result["claim_boundary"]
    boundary_ok = (
        boundary["primary_formula_sign_symmetry_proved"]
        and boundary["primary_formula_two_sided_top_hat_constructed"]
        and boundary["geometry_corrected_historical_envelope_constructed"]
        and boundary["conditional_Earth_Sun_CFF_residual_certificate"]
        and not boundary["primary_raw_data_robust_likelihood_available"]
        and not boundary["compact_object_CFF_transfer_certified"]
        and not boundary["QCD_TJJ_matching_calculated"]
        and not boundary["general_local_Maxwell_promoted"]
        and not boundary["full_MTS_fixed_point"]
    )
    add(checks, "VAL4945_25_boundary", "claim boundary", True, boundary, boundary_ok)

    claim_rows = read_csv(CLAIMS)
    claim = next((row for row in claim_rows if row["claim_id"] == "L-787"), None)
    claim_ok = claim is not None and "PRINTED_PSR_BOUND_REJECTED" in claim["notes"] and NEXT_TARGET in claim["next_test"]
    add(checks, "VAL4945_26_claim", "claim L-787 registered", True, claim, claim_ok)
    variable_rows = read_csv(VARIABLES)
    expected_variables = {
        "CFFModeSwap4945_MTS",
        "CFFSplitGate4945_MTS",
        "CFFPrintedBoundAudit4945_MTS",
        "PSRB1534Impact4945_MTS",
        "CFFGeometryBound4945_MTS",
        "CFFNuisanceAudit4945_MTS",
        "CFFWeakLocalVector4945_MTS",
        "PredictivityStatus4945_MTS",
    }
    found_variables = {row["symbol"] for row in variable_rows if row["symbol"] in expected_variables}
    add(checks, "VAL4945_27_variables", "eight variables registered", sorted(expected_variables), sorted(found_variables), found_variables == expected_variables)

    document_checks = {
        "equation": "## 1.238 Primary CFF sign theorem and physical pulsar geometry" in text(EQUATIONS),
        "red_team": "## 189. A two-sided formula does not rescue a wrong impact parameter" in text(RED_TEAM),
        "spine": FORMAL_MARKER in text(SPINE),
        "resume": FORMAL_MARKER in text(RESUME) and NEXT_TARGET in text(RESUME),
        "checkpoint": CHECKPOINT_MARKER in text(CHECKPOINT),
        "formal": FORMAL_MARKER in text(FORMAL_NOTE),
        "provenance": PROVENANCE_MARKER in text(PROVENANCE),
    }
    add(checks, "VAL4945_28_documents", "all document markers", {key: True for key in document_checks}, document_checks, all(document_checks.values()))
    generated_text = "\n".join(text(path) for path in (RESULT_JSON, SIGN_CSV, GEOMETRY_CSV, OPERATORS_CSV, LOCAL_CSV))
    missing_markers = [token for token in ("MISSING_", "TODO_NUMERIC", "PLACEHOLDER") if token in generated_text]
    add(checks, "VAL4945_29_no_placeholders", "no generated placeholders", [], missing_markers, not missing_markers)
    pycache = list((POST / "scripts").glob("__pycache__"))
    add(checks, "VAL4945_30_no_pycache", "no scripts pycache", [], [str(path) for path in pycache], not pycache)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    failures = [row["validation_id"] for row in checks if not row["passed"]]
    print(f"{RESULT_MARKER}_VALIDATION_TOTAL={len(checks)}", flush=True)
    print(f"{RESULT_MARKER}_VALIDATION_FAILED={len(failures)}", flush=True)
    print(f"{RESULT_MARKER}_VALIDATION_SHA256={digest(OUTPUT)}", flush=True)
    if failures:
        for failure in failures:
            print(f"{RESULT_MARKER}_VALIDATION_FAIL={failure}", flush=True)
        return 1
    print(f"{RESULT_MARKER}_VALIDATION_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
