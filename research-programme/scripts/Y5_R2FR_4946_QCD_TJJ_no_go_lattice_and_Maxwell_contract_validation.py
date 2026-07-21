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
SOURCE = POST / "source-intake" / "functional_rg" / "4946"
OUTPUT = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4946_VALIDATION.csv"

MAIN_SCRIPT = POST / "scripts" / "Y5_R2FR_4946_QCD_TJJ_no_go_lattice_and_Maxwell_contract.py"
RESULT_JSON = SOURCE / "QCD_TJJ_no_go_lattice_and_Maxwell_results.json"
NO_GO_CSV = SOURCE / "QCD_TJJ_observable_nonidentifiability_gate.csv"
DISPERSION_CSV = SOURCE / "QCD_TJJ_dispersion_and_lattice_contract.csv"
NDA_CSV = SOURCE / "QCD_CFF_NDA_sensitivity_nonclaim.csv"
MAXWELL_CSV = SOURCE / "local_Maxwell_action_stress_and_calibration_certificate.csv"
TRANSFER_CSV = SOURCE / "universal_CFF_calibration_transfer_functions.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = POST / "4946-Y5-R2FR-QCD-TJJ-dispersive-matching-and-weak-local-Maxwell-action-certificate.md"
FORMAL_NOTE = FORMAL / "962-PPC4161-QCD-TJJ-no-go-lattice-and-Maxwell-contract.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

RESULT_MARKER = "MTS_4946_QCD_TJJ_NO_GO_LATTICE_MAXWELL_CONTRACT"
CHECKPOINT_MARKER = "MTS_QCD_TJJ_NO_GO_LATTICE_MAXWELL_CONTRACT_4946"
FORMAL_MARKER = "PPC4161_QCD_TJJ_NO_GO_LATTICE_MAXWELL_CONTRACT_4946"
PROVENANCE_MARKER = "MTS_QCD_TJJ_NO_GO_LATTICE_MAXWELL_PROVENANCE_4946"
NEXT_TARGET = "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md"

HASH_LOCKS = {
    MAIN_SCRIPT: "691529ad9bef1674fe82108169f18d5126c51d0b49ffb2c709ff109a848f1221",
    RESULT_JSON: "e0e0f3578574b191ab389edfda6f8a3e09937053aaa945147fb4dd1fbd410041",
    NO_GO_CSV: "c570dbef06650bfc04a80f5eb8ddb52b1832078cf58e68a5838b5a6e271f2f84",
    DISPERSION_CSV: "153b131d851fd4423b7e4677e8f4a68e4cf407b6d4cea76ba1ef0a1782933819",
    NDA_CSV: "780768dd1a0da09f4d45d1bdf6ee1f7822ea695a706abf2f72610752dbd1ef66",
    MAXWELL_CSV: "8b80ddf7b5cb469fa7c580b24f6b0d759322871bfb7064111839565ba290799a",
    TRANSFER_CSV: "8707daa86fac5daf0bd6859bf8d8c29f18777349c9dbac24e259f729facd15a8",
    PROVENANCE: "2985de8547e549bd1696fcfef1a35955bd07c003398f1a6a7c6794d27c6a5715",
    CHECKPOINT: "4985b31aa5d5253ec64fd1575bbd0f844c1b5c0924a11482fb77374ddee477b6",
    FORMAL_NOTE: "19b35cfb55ad4358bded8895f70b7af473f8f8b97822a8ee31ac6ed8fd760b58",
}


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
    add(checks, "VAL4946_01_paths", "locked paths exist", [], missing, not missing)
    bad_hashes = {
        str(path): (expected, digest(path))
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "VAL4946_02_hashes", "locked hashes match", {}, bad_hashes, not bad_hashes)

    compile_errors: list[str] = []
    for path in (MAIN_SCRIPT, Path(__file__).resolve()):
        try:
            compile(text(path), str(path), "exec")
        except Exception as exc:
            compile_errors.append(f"{path.name}:{exc}")
    add(checks, "VAL4946_03_compile", "scripts compile in memory", [], compile_errors, not compile_errors)

    result = json.loads(text(RESULT_JSON))
    add(checks, "VAL4946_04_marker", "result marker", RESULT_MARKER, result.get("marker"), result.get("marker") == RESULT_MARKER)
    failed_internal = [name for name, passed in result["checks"].items() if not passed]
    add(checks, "VAL4946_05_internal", "research checks pass", [], failed_internal, not failed_internal)
    source_errors = [
        key
        for key, expected in result["source_hashes"].items()
        if not (ROOT / Path(key)).exists() or digest(ROOT / Path(key)) != expected
    ]
    add(checks, "VAL4946_06_sources", "result source paths and hashes", [], source_errors, not source_errors)
    source_clause_failures = [name for name, passed in result["source_clause_checks"].items() if not passed]
    add(checks, "VAL4946_07_source_clauses", "primary source clauses found", [], source_clause_failures, not source_clause_failures)

    no_go = read_csv(NO_GO_CSV)
    expected_no_go_ids = {f"NG4946_{index:02d}_{suffix}" for index, suffix in enumerate((
        "local_shift",
        "flat_HVP",
        "hadron_EM_form_factors",
        "hadron_GFF",
        "flat_gamma_gamma",
        "trace_anomaly",
        "TJJ_TT",
        "no_go",
    ))}
    no_go_ids = {row["gate_id"] for row in no_go}
    no_go_structure = (
        len(no_go) == 8
        and no_go_ids == expected_no_go_ids
        and all(row["passed"] == "True" for row in no_go)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in no_go)
    )
    add(checks, "VAL4946_08_no_go_rows", "eight non-identifiability rows", sorted(expected_no_go_ids), sorted(no_go_ids), no_go_structure)
    no_go_map = {row["gate_id"]: row for row in no_go}
    lower_invariant = all(
        no_go_map[key]["identifies_c_QCD"] == "False"
        for key in (
            "NG4946_01_flat_HVP",
            "NG4946_02_hadron_EM_form_factors",
            "NG4946_03_hadron_GFF",
            "NG4946_04_flat_gamma_gamma",
            "NG4946_05_trace_anomaly",
        )
    )
    add(checks, "VAL4946_09_lower_invariant", "lower observables do not identify cQCD", True, lower_invariant, lower_invariant)
    identifying = (
        no_go_map["NG4946_06_TJJ_TT"]["identifies_c_QCD"] == "True"
        and "delta c V_CFF" in no_go_map["NG4946_06_TJJ_TT"]["response_to_delta_c"]
        and no_go_map["NG4946_07_no_go"]["status"] == "DATA_ONLY_DISPERSIVE_BOUND_NO_GO_PROVED"
    )
    add(checks, "VAL4946_10_identifying", "TJJ identifies contact and no-go closes", True, identifying, identifying)

    dispersion = read_csv(DISPERSION_CSV)
    expected_dispersion_ids = {f"TJJ4946_{index:02d}_{suffix}" for index, suffix in enumerate((
        "generating_functional",
        "vertex",
        "Weyl_projector",
        "low_momentum_match",
        "dispersion",
        "photon_Ward",
        "diffeomorphism_Ward",
        "trace_TT_split",
        "lattice_EMT",
        "matching_output",
    ))}
    dispersion_ids = {row["contract_id"] for row in dispersion}
    dispersion_structure = (
        len(dispersion) == 10
        and dispersion_ids == expected_dispersion_ids
        and all(row["passed"] == "True" for row in dispersion)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in dispersion)
    )
    add(checks, "VAL4946_11_dispersion_rows", "ten TJJ contract rows", sorted(expected_dispersion_ids), sorted(dispersion_ids), dispersion_structure)
    dispersion_map = {row["contract_id"]: row for row in dispersion}
    subtraction_ok = (
        "c_QCD^r(mu)+q2/pi" in dispersion_map["TJJ4946_04_dispersion"]["object"]
        and "no unsubtracted or positivity assumption" in dispersion_map["TJJ4946_04_dispersion"]["acceptance_gate"]
        and not result["dispersive_representation"]["subtraction_constant_fixed_by_spectral_density"]
        and not result["dispersive_representation"]["rigorous_data_only_bound_available"]
    )
    add(checks, "VAL4946_12_subtraction", "subtraction constant retained", True, subtraction_ok, subtraction_ok)
    Ward_ok = (
        "p_a Gamma" in dispersion_map["TJJ4946_05_photon_Ward"]["object"]
        and "HVP pinched/contact" in dispersion_map["TJJ4946_06_diffeomorphism_Ward"]["object"]
        and "trace anomaly" in dispersion_map["TJJ4946_07_trace_TT_split"]["required_operation"]
    )
    add(checks, "VAL4946_13_Ward", "photon diffeomorphism and trace gates", True, Ward_ok, Ward_ok)
    lattice_ok = (
        dispersion_map["TJJ4946_08_lattice_EMT"]["status"] == "LATTICE_READY_ESTIMATOR"
        and "continuum limit before zero-flow-time limit" in dispersion_map["TJJ4946_08_lattice_EMT"]["required_operation"]
        and result["matching"]["c_QCD_lattice_estimator_defined"]
        and not result["matching"]["c_QCD_numeric_value_available"]
    )
    add(checks, "VAL4946_14_lattice", "lattice estimator defined numeric absent", True, lattice_ok, lattice_ok)

    nda = read_csv(NDA_CSV)
    expected_nda_ids = {f"NDA4946_{index:02d}_{suffix}" for index, suffix in enumerate((
        "pointlike_pion",
        "pointlike_kaon",
        "unit_1GeV",
        "K_4pi_squared",
        "K_for_one_percent",
        "K_for_equal_leptons",
    ))}
    nda_ids = {row["sensitivity_id"] for row in nda}
    nda_structure = (
        len(nda) == 6
        and nda_ids == expected_nda_ids
        and all(row["passed"] == "True" for row in nda)
        and all(row["valid_for_QCD_bound"] == "False" for row in nda)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in nda)
    )
    add(checks, "VAL4946_15_NDA_rows", "six NDA nonclaim rows", sorted(expected_nda_ids), sorted(nda_ids), nda_structure)
    nda_map = {row["sensitivity_id"]: row for row in nda}
    nda_values = (
        math.isclose(float(nda_map["NDA4946_02_unit_1GeV"]["coefficient_m2"]), 2.261144961772855e-35, rel_tol=1e-14)
        and math.isclose(float(nda_map["NDA4946_04_K_for_one_percent"]["dimensionless_K"]), 425.5275352193915, rel_tol=1e-14)
        and math.isclose(float(nda_map["NDA4946_05_K_for_equal_leptons"]["dimensionless_K"]), 42552.75352193915, rel_tol=1e-14)
    )
    add(checks, "VAL4946_16_NDA_values", "NDA sensitivity values", "locked", [nda_map[key].get("dimensionless_K", nda_map[key]["coefficient_m2"]) for key in ("NDA4946_02_unit_1GeV", "NDA4946_04_K_for_one_percent", "NDA4946_05_K_for_equal_leptons")], nda_values)

    maxwell = read_csv(MAXWELL_CSV)
    expected_maxwell_ids = {f"MAX4946_{index:02d}_{suffix}" for index, suffix in enumerate((
        "action",
        "current",
        "field_equation",
        "Bianchi",
        "stress",
        "conservation",
        "flat_limit",
        "weak_local",
        "calibration",
    ))}
    maxwell_ids = {row["certificate_id"] for row in maxwell}
    maxwell_structure = (
        len(maxwell) == 9
        and maxwell_ids == expected_maxwell_ids
        and all(row["passed"] == "True" for row in maxwell)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in maxwell)
    )
    add(checks, "VAL4946_17_Maxwell_rows", "nine Maxwell rows", sorted(expected_maxwell_ids), sorted(maxwell_ids), maxwell_structure)
    maxwell_map = {row["certificate_id"]: row for row in maxwell}
    field_stress_ok = (
        "-4c_IR" in maxwell_map["MAX4946_02_field_equation"]["statement"]
        and "c_IR H_CFF" in maxwell_map["MAX4946_04_stress"]["statement"]
        and maxwell_map["MAX4946_05_conservation"]["status"] == "TOTAL_LOCAL_CONSERVATION_DERIVED"
    )
    add(checks, "VAL4946_18_field_stress", "field stress conservation from same action", True, field_stress_ok, field_stress_ok)
    flat_calibration_ok = (
        maxwell_map["MAX4946_06_flat_limit"]["status"] == "EXACT_MAXWELL_LIMIT_DERIVED"
        and maxwell_map["MAX4946_08_calibration"]["status"] == "CALIBRATION_CONTRACT_DEFINED_NOT_EXECUTED"
        and result["local_Maxwell"]["flat_Maxwell_limit_exact"]
        and not result["local_Maxwell"]["physical_CFF_coefficient_calibrated"]
    )
    add(checks, "VAL4946_19_flat_calibration", "flat exact calibration open", True, flat_calibration_ok, flat_calibration_ok)

    transfers = read_csv(TRANSFER_CSV)
    expected_systems = {
        "Earth",
        "Sun",
        "one_solar_mass_white_dwarf",
        "1.4_solar_mass_12km_neutron_star",
        "10_solar_mass_Schwarzschild_horizon",
    }
    systems = {row["system"] for row in transfers}
    transfer_structure = (
        len(transfers) == 5
        and systems == expected_systems
        and all(row["passed"] == "True" for row in transfers)
        and all(row["coefficient_retuned"] == "False" for row in transfers)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in transfers)
    )
    add(checks, "VAL4946_20_transfer_rows", "five no-retuning transfer rows", sorted(expected_systems), sorted(systems), transfer_structure)
    transfer_map = {row["system"]: row for row in transfers}
    transfer_formula = all(
        math.isclose(
            float(row["abs_cIR_for_1e_minus_6_split_m2"]),
            1e-6 / float(row["CFF_curvature_factor_m_minus_2"]),
            rel_tol=1e-14,
        )
        for row in transfers
    )
    add(checks, "VAL4946_21_transfer_formula", "one-micro residual sensitivity slopes", True, transfer_formula, transfer_formula)
    compact_values = (
        math.isclose(float(transfer_map["1.4_solar_mass_12km_neutron_star"]["abs_cIR_for_1e_minus_6_split_m2"]), 69.65480735584059, rel_tol=1e-14)
        and math.isclose(float(transfer_map["10_solar_mass_Schwarzschild_horizon"]["abs_cIR_for_1e_minus_6_split_m2"]), 145.37022509445288, rel_tol=1e-14)
    )
    add(checks, "VAL4946_22_transfer_values", "compact sensitivity values", "locked", [transfer_map[name]["abs_cIR_for_1e_minus_6_split_m2"] for name in ("1.4_solar_mass_12km_neutron_star", "10_solar_mass_Schwarzschild_horizon")], compact_values)

    matching = result["matching"]
    interval = matching["non_QCD_interval_m2"]
    interval_ok = (
        math.isclose(float(interval[0]), -9.621794773634824e-31, rel_tol=1e-14)
        and math.isclose(float(interval[1]), -9.621794073504142e-31, rel_tol=1e-14)
        and interval[0] < interval[1] < 0.0
        and "replaced, not added" in matching["formula"]
    )
    add(checks, "VAL4946_23_matching", "non-QCD interval and no double count", "locked and replacement", matching, interval_ok)

    boundary = result["claim_boundary"]
    boundary_ok = (
        boundary["QCD_TJJ_lower_observable_no_go_proved"]
        and boundary["QCD_TJJ_subtracted_dispersion_relation_derived"]
        and not boundary["QCD_TJJ_finite_rigorous_spectral_bound_derived"]
        and boundary["QCD_TJJ_lattice_matching_estimator_defined"]
        and not boundary["QCD_TJJ_numeric_matching_calculated"]
        and boundary["leading_local_Maxwell_action_equation_stress_derived"]
        and boundary["universal_CFF_calibration_contract_defined"]
        and not boundary["universal_CFF_calibration_executed"]
        and not boundary["general_local_Maxwell_promoted"]
        and not boundary["full_MTS_fixed_point"]
    )
    add(checks, "VAL4946_24_boundary", "claim boundary", True, boundary, boundary_ok)

    claim_rows = read_csv(CLAIMS)
    claim = next((row for row in claim_rows if row["claim_id"] == "L-788"), None)
    claim_ok = claim is not None and "FINITE_CFF_CONTACT_COUNTEREXAMPLE" in claim["notes"] and NEXT_TARGET in claim["next_test"]
    add(checks, "VAL4946_25_claim", "claim L-788 registered", True, claim, claim_ok)
    variable_rows = read_csv(VARIABLES)
    expected_variables = {
        "QCDCFFContactShift4946_MTS",
        "QCDTJJNoGo4946_MTS",
        "QCDTJJDispersion4946_MTS",
        "QCDTJJLatticeEstimator4946_MTS",
        "CFFNonQCDInterval4946_MTS",
        "LocalMaxwellStress4946_MTS",
        "CFFCalibrationTransfer4946_MTS",
        "PredictivityStatus4946_MTS",
    }
    found_variables = {row["symbol"] for row in variable_rows if row["symbol"] in expected_variables}
    add(checks, "VAL4946_26_variables", "eight variables registered", sorted(expected_variables), sorted(found_variables), found_variables == expected_variables)

    document_checks = {
        "equation": "## 1.239 QCD TJJ subtraction theorem and local Maxwell stress" in text(EQUATIONS),
        "red_team": "## 190. A subtraction constant cannot be bounded by data that never sees it" in text(RED_TEAM),
        "spine": FORMAL_MARKER in text(SPINE),
        "resume": FORMAL_MARKER in text(RESUME) and NEXT_TARGET in text(RESUME),
        "checkpoint": CHECKPOINT_MARKER in text(CHECKPOINT),
        "formal": FORMAL_MARKER in text(FORMAL_NOTE),
        "provenance": PROVENANCE_MARKER in text(PROVENANCE),
    }
    add(checks, "VAL4946_27_documents", "all document markers", {key: True for key in document_checks}, document_checks, all(document_checks.values()))
    generated_text = "\n".join(text(path) for path in (RESULT_JSON, NO_GO_CSV, DISPERSION_CSV, NDA_CSV, MAXWELL_CSV, TRANSFER_CSV))
    missing_markers = [token for token in ("MISSING_", "TODO_NUMERIC", "PLACEHOLDER") if token in generated_text]
    add(checks, "VAL4946_28_no_placeholders", "no generated placeholders", [], missing_markers, not missing_markers)
    all_nonclaim = all(
        row["valid_for_full_MTS_claim"] == "False"
        for table in (no_go, dispersion, nda, maxwell, transfers)
        for row in table
    )
    add(checks, "VAL4946_29_nonclaim", "all evidence rows retain full-MTS firewall", True, all_nonclaim, all_nonclaim)
    pycache = list((POST / "scripts").glob("__pycache__"))
    add(checks, "VAL4946_30_no_pycache", "no scripts pycache", [], [str(path) for path in pycache], not pycache)

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
