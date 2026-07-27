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
SOURCE = POST / "source-intake" / "functional_rg" / "4947"
OUTPUT = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4947_VALIDATION.csv"

MAIN_SCRIPT = POST / "scripts" / "Y5_R2FR_4947_local_calibration_count_and_source_residues.py"
RESULT_JSON = SOURCE / "local_calibration_count_results.json"
CALIBRATION_CSV = SOURCE / "parent_low_energy_calibration_ledger.csv"
RESIDUE_CSV = SOURCE / "source_residue_chain.csv"
LIMIT_CSV = SOURCE / "Newton_geodesic_Lorentz_limit_gate.csv"
ARENA_CSV = SOURCE / "cross_arena_no_retuning_matrix.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = POST / "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md"
FORMAL_NOTE = FORMAL / "963-PPC4161-local-calibration-count-and-source-residue.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

RESULT_MARKER = "MTS_4947_LOCAL_CALIBRATION_COUNT_SOURCE_RESIDUES"
CHECKPOINT_MARKER = "MTS_LOCAL_GR_NEWTON_MAXWELL_SOURCE_RESIDUE_CALIBRATION_COUNT_4947"
FORMAL_MARKER = "PPC4161_LOCAL_CALIBRATION_COUNT_SOURCE_RESIDUE_4947"
PROVENANCE_MARKER = "MTS_LOCAL_CALIBRATION_COUNT_SOURCE_RESIDUE_PROVENANCE_4947"
NEXT_TARGET = "4948-Y5-R2FR-single-parent-motion-Hessian-to-galaxy-phase-flow-and-universal-Jgap-interface.md"

HASH_LOCKS = {
    MAIN_SCRIPT: "6d429945ec2b96b385f4fe30e00506be88c73bcc90c934ab3f7963644cc547a2",
    RESULT_JSON: "2df2b3af173ecb85167a99795766d13cc8ca17de04fa227dafbbbc7389710b42",
    CALIBRATION_CSV: "e68c78e9c4e1c05df056e441db9a06869b723bb5ca5c9fd06933965737766020",
    RESIDUE_CSV: "b08468f29f938dfe72f13b9eec93f73c2b4f9c58ff89e7b67008c6de2cfc1e1d",
    LIMIT_CSV: "a412b326de7867064968a66caed955039b466e9e230acf5ee0b6952b6f5f006a",
    ARENA_CSV: "8c060a129155d84ebc40412e50a2acc11ea5043a9825afd24e5486065c194cc7",
    PROVENANCE: "bd67171d34042dbdc593eed6203975577d062a12aa8ed6e844ec1ef7518a77c1",
    CHECKPOINT: "0b71f50c85ab4c5761755aa11544910a1a1e4fcacc901236432705a5ba36563f",
    FORMAL_NOTE: "93ec3d2bfb50873cfe10001d2c43381233587e93fe22f31b8a7ded54423d4eef",
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
    add(checks, "VAL4947_01_paths", "locked paths exist", [], missing, not missing)
    bad_hashes = {
        str(path): (expected, digest(path))
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "VAL4947_02_hashes", "locked hashes match", {}, bad_hashes, not bad_hashes)

    compile_errors: list[str] = []
    for path in (MAIN_SCRIPT, Path(__file__).resolve()):
        try:
            compile(text(path), str(path), "exec")
        except Exception as exc:
            compile_errors.append(f"{path.name}:{exc}")
    add(checks, "VAL4947_03_compile", "scripts compile in memory", [], compile_errors, not compile_errors)

    result = json.loads(text(RESULT_JSON))
    add(checks, "VAL4947_04_marker", "result marker", RESULT_MARKER, result.get("marker"), result.get("marker") == RESULT_MARKER)
    failed_internal = [name for name, passed in result["checks"].items() if not passed]
    add(checks, "VAL4947_05_internal", "research checks pass", [], failed_internal, not failed_internal)
    source_errors = [
        key
        for key, expected in result["source_hashes"].items()
        if not (ROOT / Path(key)).exists() or digest(ROOT / Path(key)) != expected
    ]
    add(checks, "VAL4947_06_sources", "result source paths and hashes", [], source_errors, not source_errors)
    source_clause_failures = [name for name, passed in result["source_clause_checks"].items() if not passed]
    add(checks, "VAL4947_07_source_clauses", "authoritative parent clauses found", [], source_clause_failures, not source_clause_failures)

    tables = {
        "calibration": read_csv(CALIBRATION_CSV),
        "residue": read_csv(RESIDUE_CSV),
        "limit": read_csv(LIMIT_CSV),
        "arena": read_csv(ARENA_CSV),
    }
    malformed = {
        name: index
        for name, rows in tables.items()
        for index, row in enumerate(rows)
        if None in row or any(value is None for value in row.values())
    }
    add(checks, "VAL4947_08_csv_shape", "all generated CSV rows parse without overflow", {}, malformed, not malformed)

    calibration = tables["calibration"]
    expected_calibration_ids = {f"CAL4947_{index:02d}_{suffix}" for index, suffix in enumerate((
        "GN", "Lambda", "alphaEM", "Jgap", "cIR", "aR", "aC", "thetaSM", "RGWilson"
    ))}
    calibration_ids = {row["parameter_id"] for row in calibration}
    calibration_structure = (
        len(calibration) == 9
        and calibration_ids == expected_calibration_ids
        and all(row["arena_retuning_allowed"] == "False" for row in calibration)
    )
    add(checks, "VAL4947_09_calibration_rows", "nine scoped calibration rows", sorted(expected_calibration_ids), sorted(calibration_ids), calibration_structure)
    counted = [row for row in calibration if row["count_in_declared_truncation"] == "True"]
    add(checks, "VAL4947_10_counted_coordinates", "seven counted scalar coordinates", 7, [row["symbol"] for row in counted], len(counted) == 7)
    leading = [row for row in calibration if row["leading_local_source_residue"] == "True"]
    expected_leading = {"G_N <-> M_R^2", "alpha_EM (or e in a fixed charge convention)"}
    add(checks, "VAL4947_11_leading", "two leading source normalizations", sorted(expected_leading), sorted(row["symbol"] for row in leading), {row["symbol"] for row in leading} == expected_leading)
    open_statuses = {"UNIVERSAL_VALUE_NOT_SELECTED", "QCD_TJJ_OR_ONE_CALIBRATION_OPEN", "FINITE_MATCHING_SUM_OPEN"}
    unresolved = {row["symbol"] for row in counted if row["current_status"] in open_statuses}
    expected_unresolved = {"J_gap=m_gap^2 G_N", "c_IR=c_nonQCD+c_QCD^r", "a_R^r", "a_C^r"}
    add(checks, "VAL4947_12_unresolved", "four universal unresolved coordinates", sorted(expected_unresolved), sorted(unresolved), unresolved == expected_unresolved)
    calibration_map = {row["parameter_id"]: row for row in calibration}
    inherited_ok = (
        calibration_map["CAL4947_07_thetaSM"]["count_in_declared_truncation"] == "False"
        and calibration_map["CAL4947_07_thetaSM"]["current_status"] == "EXPLICIT_INHERITED_PARAMETER_SET"
        and calibration_map["CAL4947_08_RGWilson"]["independent_scalar_coordinate"] == "False"
    )
    add(checks, "VAL4947_13_inherited", "thetaSM excluded and RG Wilsons conditional", True, inherited_ok, inherited_ok)

    residues = tables["residue"]
    expected_residue_ids = {f"SRC4947_{index:02d}_{suffix}" for index, suffix in enumerate((
        "parent_action", "metric_variation", "exchange", "linearized_Einstein", "Poisson", "point_source",
        "neutral_worldline", "null_worldline", "gauge_normalization", "Maxwell", "charged_worldline",
        "EM_stress", "total_conservation", "motion_silence"
    ))}
    residue_ids = {row["chain_id"] for row in residues}
    residue_structure = len(residues) == 14 and residue_ids == expected_residue_ids and all(row["passed"] == "True" for row in residues)
    add(checks, "VAL4947_14_residue_rows", "fourteen source-residue rows", sorted(expected_residue_ids), sorted(residue_ids), residue_structure)
    residue_map = {row["chain_id"]: row for row in residues}
    metric_rank_ok = (
        "G_N=1/(8 pi M_R^2)" in residue_map["SRC4947_01_metric_variation"]["equation"]
        and "1/M_R^2=8 pi G_N" in residue_map["SRC4947_02_exchange"]["residue_owner"]
        and residue_map["SRC4947_03_linearized_Einstein"]["residue_owner"] == "same G_N"
        and residue_map["SRC4947_07_null_worldline"]["new_independent_calibration"] == "False"
    )
    add(checks, "VAL4947_15_metric_rank", "one metric residue through lensing", True, metric_rank_ok, metric_rank_ok)
    Newton_ok = (
        "nabla2 Phi=4 pi G_N rho" in residue_map["SRC4947_04_Poisson"]["equation"]
        and "Phi=-G_N M/r" in residue_map["SRC4947_05_point_source"]["equation"]
        and residue_map["SRC4947_06_neutral_worldline"]["derivation_status"] == "UNIVERSAL_GEODESIC_LIMIT_DERIVED"
    )
    add(checks, "VAL4947_16_Newton", "Poisson point force geodesic chain", True, Newton_ok, Newton_ok)
    Maxwell_ok = (
        "-4c_IR" in residue_map["SRC4947_09_Maxwell"]["equation"]
        and "(q/m)F" in residue_map["SRC4947_10_charged_worldline"]["equation"]
        and "T_EM^0i=(E cross B)^i" in residue_map["SRC4947_11_EM_stress"]["equation"]
        and residue_map["SRC4947_12_total_conservation"]["derivation_status"] == "SOURCE_EXCHANGE_CONSERVATION_DERIVED"
    )
    add(checks, "VAL4947_17_Maxwell", "Maxwell Lorentz stress Poynting chain", True, Maxwell_ok, Maxwell_ok)
    motion_ok = (
        residue_map["SRC4947_13_motion_silence"]["derivation_status"] == "CLASSICAL_ONE_SCALAR_FIFTH_FORCE_ZERO"
        and "Q_psi=0" in residue_map["SRC4947_13_motion_silence"]["equation"]
    )
    add(checks, "VAL4947_18_motion", "local motion source silence", True, motion_ok, motion_ok)

    limits = tables["limit"]
    expected_limit_ids = {f"LIM4947_{index:02d}_{suffix}" for index, suffix in enumerate((
        "action_to_Einstein", "Einstein_to_Poisson", "Poisson_to_Newton", "metric_to_geodesic", "null_lensing",
        "Maxwell_flat", "Lorentz", "EM_gravity_source", "standard_PPN", "strong_EP"
    ))}
    limit_ids = {row["gate_id"] for row in limits}
    limit_structure = len(limits) == 10 and limit_ids == expected_limit_ids and all(row["passed"] == "True" for row in limits)
    add(checks, "VAL4947_19_limit_rows", "ten correspondence gates", sorted(expected_limit_ids), sorted(limit_ids), limit_structure)
    limit_map = {row["gate_id"]: row for row in limits}
    boundary_gates = (
        limit_map["LIM4947_04_null_lensing"]["status"] == "SAME_GN_DERIVED_CFF_NUMERIC_OPEN"
        and "physical coefficient is open" in limit_map["LIM4947_04_null_lensing"]["result"]
        and limit_map["LIM4947_09_strong_EP"]["status"] == "OPEN_NOT_SMUGGLED"
    )
    add(checks, "VAL4947_20_gate_boundaries", "CFF numeric and strong EP remain open", True, boundary_gates, boundary_gates)

    arenas = tables["arena"]
    expected_systems = {
        "Earth", "Sun", "one_solar_mass_white_dwarf", "1.4_solar_mass_12km_neutron_star", "10_solar_mass_Schwarzschild_horizon"
    }
    systems = {row["system"] for row in arenas}
    add(checks, "VAL4947_21_arenas", "five fixed systems", sorted(expected_systems), sorted(systems), len(arenas) == 5 and systems == expected_systems)
    arena_map = {row["system"]: row for row in arenas}
    weak_systems = {row["system"] for row in arenas if row["weak_field_Newton_gate"] == "True"}
    expected_weak = {"Earth", "Sun", "one_solar_mass_white_dwarf"}
    add(checks, "VAL4947_22_weak_domain", "only three weak-Newton systems", sorted(expected_weak), sorted(weak_systems), weak_systems == expected_weak)
    acceleration_ok = (
        math.isclose(float(arena_map["Earth"]["Newton_surface_acceleration_m_s2"]), 9.820302293385646, rel_tol=1e-14)
        and math.isclose(float(arena_map["Sun"]["Newton_surface_acceleration_m_s2"]), 274.2084034394405, rel_tol=1e-14)
        and math.isclose(float(arena_map["one_solar_mass_white_dwarf"]["Newton_surface_acceleration_m_s2"]), 2708499.0451020403, rel_tol=1e-14)
    )
    add(checks, "VAL4947_23_acceleration", "weak-system Newton accelerations", "locked", [arena_map[name]["Newton_surface_acceleration_m_s2"] for name in sorted(expected_weak)], acceleration_ok)
    cff_ok = all(
        math.isclose(float(row["CFF_factor_m_minus_2"]), 12.0 * float(row["mass_length_m"]) / float(row["radius_m"]) ** 3, rel_tol=2e-15)
        and row["CFF_factor_matches"] == "True"
        for row in arenas
    )
    add(checks, "VAL4947_24_CFF", "all CFF transfer factors reproduced", True, cff_ok, cff_ok)
    token_columns = ("same_GN_token", "same_alphaEM_token", "same_Jgap_token", "same_cIR_token")
    universal_tokens = all(len({row[column] for row in arenas}) == 1 for column in token_columns)
    no_retune = all(
        row["arena_specific_source_normalization"] == "False"
        and row["arena_specific_Jgap"] == "False"
        and row["arena_specific_cIR"] == "False"
        for row in arenas
    )
    add(checks, "VAL4947_25_no_retuning", "four universal tokens and no arena retuning", True, [universal_tokens, no_retune], universal_tokens and no_retune)
    ppn_ok = all(float(row["PPN_delta_gamma"]) == 0.0 and float(row["PPN_delta_beta"]) == 0.0 for row in arenas)
    strong_not_Newton = all(arena_map[name]["status"] == "GR_SOURCE_CHAIN_RETAINED_NEWTON_APPROXIMATION_NOT_APPLICABLE" for name in expected_systems - expected_weak)
    add(checks, "VAL4947_26_PPN_domain", "standard PPN zero and strong rows not Newtonian", True, [ppn_ok, strong_not_Newton], ppn_ok and strong_not_Newton)

    count = result["calibration_count"]
    count_ok = (
        count["leading_local_source_normalizations"] == 2
        and count["declared_scalar_coordinates_in_current_truncation"] == 7
        and len(count["currently_unselected_or_unmatched_coordinates"]) == 4
        and count["arena_dependent_calibrations"] == 0
        and not count["full_untruncated_EFT_parameter_count_closed"]
    )
    add(checks, "VAL4947_27_result_count", "result calibration count", True, count, count_ok)
    boundary = result["claim_boundary"]
    boundary_ok = (
        boundary["single_metric_pole_owns_GR_Newton_orbital_and_lensing_residue"]
        and boundary["Poisson_point_force_and_geodesic_limits_derived"]
        and boundary["Maxwell_Lorentz_stress_and_Poynting_share_one_action"]
        and boundary["classical_one_scalar_fifth_force_zero_on_selected_branch"]
        and not boundary["strong_equivalence_principle_for_compact_bodies_proved"]
        and not boundary["G_N_predicted_from_dimensionless_MTS_data"]
        and not boundary["J_gap_selected_without_calibration"]
        and not boundary["physical_c_IR_calculated_or_calibrated"]
        and not boundary["a_R_a_C_finite_matching_completed"]
        and not boundary["visible_U1_and_matter_functor_derived_from_motion_alone"]
        and not boundary["full_untruncated_parameter_count_closed"]
        and not boundary["full_MTS_fixed_point_and_empirical_unification"]
    )
    add(checks, "VAL4947_28_boundary", "claim boundary", True, boundary, boundary_ok)

    claim_rows = read_csv(CLAIMS)
    claim = next((row for row in claim_rows if row["claim_id"] == "L-789"), None)
    claim_ok = claim is not None and "MASSLESS_METRIC_SOURCE_RANK_ONE" in claim["notes"] and claim["next_test"] == NEXT_TARGET
    add(checks, "VAL4947_29_claim", "claim L-789 registered", True, claim, claim_ok)
    variable_rows = read_csv(VARIABLES)
    expected_variables = {
        "LocalParentAction4947_MTS", "MetricPoleRank4947_MTS", "NewtonLimit4947_MTS", "GeodesicLensing4947_MTS",
        "MaxwellLorentzStress4947_MTS", "CalibrationCount4947_MTS", "NoRetuningMatrix4947_MTS", "PredictivityStatus4947_MTS"
    }
    found_variables = {row["symbol"] for row in variable_rows if row["symbol"] in expected_variables}
    add(checks, "VAL4947_30_variables", "eight variables registered", sorted(expected_variables), sorted(found_variables), found_variables == expected_variables)
    document_checks = {
        "equation": "## 1.240 Rank-one metric residue, Newton limit and one-action Lorentz chain" in text(EQUATIONS),
        "red_team": "## 191. A correspondence derivation is not a parameter prediction" in text(RED_TEAM),
        "spine": FORMAL_MARKER in text(SPINE),
        "resume": FORMAL_MARKER in text(RESUME) and NEXT_TARGET in text(RESUME),
        "checkpoint": CHECKPOINT_MARKER in text(CHECKPOINT),
        "formal": FORMAL_MARKER in text(FORMAL_NOTE),
        "provenance": PROVENANCE_MARKER in text(PROVENANCE),
    }
    add(checks, "VAL4947_31_documents", "all document markers", {key: True for key in document_checks}, document_checks, all(document_checks.values()))

    generated_text = "\n".join(text(path) for path in (RESULT_JSON, CALIBRATION_CSV, RESIDUE_CSV, LIMIT_CSV, ARENA_CSV))
    missing_markers = [token for token in ("MISSING_", "TODO_NUMERIC", "PLACEHOLDER") if token in generated_text]
    add(checks, "VAL4947_32_no_placeholders", "no generated placeholders", [], missing_markers, not missing_markers)
    all_nonclaim = all(
        row["valid_for_full_MTS_claim"] == "False"
        for rows in tables.values()
        for row in rows
    )
    add(checks, "VAL4947_33_nonclaim", "all evidence rows retain full-MTS firewall", True, all_nonclaim, all_nonclaim)
    all_pass = all(row["passed"] == "True" for name, rows in tables.items() if name != "calibration" for row in rows)
    add(checks, "VAL4947_34_row_pass", "all applicable generated gate rows pass", True, all_pass, all_pass)
    pycache = list((POST / "scripts").glob("__pycache__"))
    add(checks, "VAL4947_35_no_pycache", "no scripts pycache", [], [str(path) for path in pycache], not pycache)

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
