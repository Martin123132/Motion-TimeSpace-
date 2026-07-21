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
SOURCE = POST / "source-intake" / "functional_rg" / "4944"
OUTPUT = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4944_VALIDATION.csv"

MAIN_SCRIPT = POST / "scripts" / "Y5_R2FR_4944_visible_CFF_threshold_and_total_bound.py"
RESULT_JSON = SOURCE / "visible_CFF_threshold_and_total_bound_results.json"
SPIN1_CSV = SOURCE / "spin1_heat_kernel_envelope.csv"
COMPONENT_CSV = SOURCE / "visible_CFF_matching_components.csv"
HADRONIC_CSV = SOURCE / "hadronic_matching_and_total_bound_gate.csv"
LOCAL_CSV = SOURCE / "conditional_total_CFF_local_residual_bound.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = POST / "4944-Y5-R2FR-complete-electroweak-spin1-and-hadronic-CFF-matching-or-total-photon-residual-bound.md"
FORMAL_NOTE = FORMAL / "960-PPC4161-visible-CFF-threshold-and-total-residual-bound.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

RESULT_MARKER = "MTS_4944_VISIBLE_CFF_THRESHOLD_AND_TOTAL_BOUND"
CHECKPOINT_MARKER = "MTS_VISIBLE_CFF_THRESHOLD_TOTAL_RESIDUAL_BOUND_4944"
FORMAL_MARKER = "PPC4161_VISIBLE_CFF_THRESHOLD_TOTAL_BOUND_4944"
PROVENANCE_MARKER = "MTS_VISIBLE_CFF_THRESHOLD_TOTAL_BOUND_PROVENANCE_4944"
NEXT_TARGET = "4945-Y5-R2FR-primary-two-sided-CFF-likelihood-or-QCD-TJJ-dispersion-bound-and-local-Maxwell-certificate.md"

HASH_LOCKS = {
    MAIN_SCRIPT: "38ac0bc9b4370671b3400e7f18feac99f9865eea501dc62fdd8a2104e4669a0e",
    RESULT_JSON: "733f057b78ee5c9848a5d25c019b2c993bf6faebb78f0a4653923e4b62cc357d",
    SPIN1_CSV: "02c69eaf1ccbcc3860f3ce5834f4498b8e3dbcdcc83f2e08aaa17a3828062bc1",
    COMPONENT_CSV: "96a8b2f3efe054681203516422e1f1133a725ce70cb1f36fb0a5ab3b863b7b2a",
    HADRONIC_CSV: "6eadda29996fc1ea217378c8e92b51869ddd3c218ab2f4c77de48f5e5121f963",
    LOCAL_CSV: "bc1700d28d660fb6e1d868ecc0a19ef6f472c6b832cb85e832dbed96e69b35f3",
    PROVENANCE: "da4cda35608a9117adf5fb3bd1c9c024d2bb0575f66e8a04e538134da718b3bd",
    CHECKPOINT: "0082f96830d4a3cdb75a27b55a8382ac4ba6bb75811eea655723629e4a523dd9",
    FORMAL_NOTE: "384bef251c6aba26dfdecc95c8fbb24f500728df7219ff26350cade9b31a70ff",
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
    add(checks, "VAL4944_01_paths", "locked paths exist", [], missing, not missing)
    bad_hashes = {
        str(path): (expected, digest(path))
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "VAL4944_02_hashes", "locked hashes match", {}, bad_hashes, not bad_hashes)

    compile_errors: list[str] = []
    for path in (MAIN_SCRIPT, Path(__file__).resolve()):
        try:
            compile(text(path), str(path), "exec")
        except Exception as exc:
            compile_errors.append(f"{path.name}:{exc}")
    add(checks, "VAL4944_03_compile", "scripts compile in memory", [], compile_errors, not compile_errors)

    result = json.loads(text(RESULT_JSON))
    add(checks, "VAL4944_04_marker", "result marker", RESULT_MARKER, result.get("marker"), result.get("marker") == RESULT_MARKER)
    failed_internal = [name for name, passed in result["checks"].items() if not passed]
    add(checks, "VAL4944_05_internal", "research checks pass", [], failed_internal, not failed_internal)
    source_errors = [
        key
        for key, expected in result["source_hashes"].items()
        if not (ROOT / Path(key)).exists() or digest(ROOT / Path(key)) != expected
    ]
    add(checks, "VAL4944_06_sources", "result source paths and hashes", [], source_errors, not source_errors)

    spin1 = read_csv(SPIN1_CSV)
    expected_spin1 = {
        "W4944_00_hessian",
        "W4944_01_explicit_Riemann_Omega2",
        "W4944_02_covariant_derivative_reduction",
        "W4944_03_U_box_U",
        "W4944_04_U_Omega2",
        "W4944_05_non_CFF_monomials",
        "W4944_06_total_envelope",
    }
    spin1_ids = {row["term_id"] for row in spin1}
    spin1_ok = (
        len(spin1) == 7
        and spin1_ids == expected_spin1
        and all(row["passed"] == "True" for row in spin1)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in spin1)
    )
    add(checks, "VAL4944_07_spin1_rows", "seven spin-one rows", sorted(expected_spin1), sorted(spin1_ids), spin1_ok)
    raw_weight = sum(
        float(row["absolute_dimensionless_CFF_weight"])
        for row in spin1
        if row["term_id"] != "W4944_06_total_envelope"
    )
    envelope_weight = float(next(row for row in spin1 if row["term_id"] == "W4944_06_total_envelope")["absolute_dimensionless_CFF_weight"])
    spin1_weight_ok = (
        math.isclose(raw_weight, 1.972222222222222, rel_tol=1e-14)
        and envelope_weight == 10.0
        and envelope_weight >= 5.0 * raw_weight
    )
    add(checks, "VAL4944_08_spin1_weight", "raw and adopted W weights", [1.972222222222222, 10.0], [raw_weight, envelope_weight], spin1_weight_ok)
    spin1_zero = next(row for row in spin1 if row["term_id"] == "W4944_05_non_CFF_monomials")
    zero_ok = float(spin1_zero["absolute_dimensionless_CFF_weight"]) == 0 and "vanishes" in spin1_zero["bound_derivation"]
    add(checks, "VAL4944_09_spin1_zero", "non-CFF monomials excluded", "zero with trace reason", spin1_zero, zero_ok)

    components = read_csv(COMPONENT_CSV)
    expected_components = {f"CFF4944_{index:02d}_{suffix}" for index, suffix in enumerate((
        "parent",
        "free_leptons",
        "W_spin1",
        "pion_pointlike_anchor",
        "kaon_pointlike_anchor",
        "QCD_local_remainder",
        "calculable_control_interval",
        "total_conditional_bound",
        "unmatched_remainder_bound",
    ))}
    component_ids = {row["component_id"] for row in components}
    components_ok = (
        len(components) == 9
        and component_ids == expected_components
        and all(row["passed"] == "True" for row in components)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in components)
    )
    add(checks, "VAL4944_10_components", "nine matching components", sorted(expected_components), sorted(component_ids), components_ok)
    component_map = {row["component_id"]: row for row in components}
    numeric_ok = (
        math.isclose(float(component_map["CFF4944_01_free_leptons"]["coefficient_or_bound_m2"]), -9.621794423569482e-31, rel_tol=1e-14)
        and math.isclose(float(component_map["CFF4944_02_W_spin1"]["coefficient_or_bound_m2"]), 3.500653413759824e-38, rel_tol=1e-14)
        and math.isclose(float(component_map["CFF4944_03_pion_pointlike_anchor"]["coefficient_or_bound_m2"]), 6.448656653294463e-36, rel_tol=1e-14)
        and math.isclose(float(component_map["CFF4944_04_kaon_pointlike_anchor"]["coefficient_or_bound_m2"]), 5.15430497960349e-37, rel_tol=1e-14)
    )
    add(checks, "VAL4944_11_threshold_values", "lepton W pion and kaon values", "locked", [component_map[key]["coefficient_or_bound_m2"] for key in ("CFF4944_01_free_leptons", "CFF4944_02_W_spin1", "CFF4944_03_pion_pointlike_anchor", "CFF4944_04_kaon_pointlike_anchor")], numeric_ok)
    qcd_ok = (
        "not separately bounded" in component_map["CFF4944_05_QCD_local_remainder"]["coefficient_or_bound_m2"]
        and "not assumed to cancel" in component_map["CFF4944_05_QCD_local_remainder"]["sign_or_interval"]
        and component_map["CFF4944_05_QCD_local_remainder"]["valid_for_total_physical_prediction"] == "False"
    )
    add(checks, "VAL4944_12_QCD", "QCD remainder retained", "not zero or predicted", component_map["CFF4944_05_QCD_local_remainder"], qcd_ok)
    control_ok = (
        math.isclose(float(component_map["CFF4944_06_calculable_control_interval"]["coefficient_or_bound_m2"]), 9.62172513276331e-31, rel_tol=1e-14)
        and "CALCULABLE_CONTROL_NOT_TOTAL_PHYSICAL_COEFFICIENT" == component_map["CFF4944_06_calculable_control_interval"]["matching_status"]
    )
    add(checks, "VAL4944_13_control", "calculable control envelope", 9.62172513276331e-31, component_map["CFF4944_06_calculable_control_interval"], control_ok)
    total_ok = (
        float(component_map["CFF4944_07_total_conditional_bound"]["coefficient_or_bound_m2"]) == 6002500.0
        and component_map["CFF4944_07_total_conditional_bound"]["matching_status"] == "TWO_SIDED_SECONDARY_MODEL_CONDITIONAL_TOTAL_BOUND"
        and "B_PSR+|c_control|" in component_map["CFF4944_08_unmatched_remainder_bound"]["formula"]
    )
    add(checks, "VAL4944_14_total_bound", "total and unmatched triangle bounds", "conditional and two-sided", [component_map["CFF4944_07_total_conditional_bound"], component_map["CFF4944_08_unmatched_remainder_bound"]], total_ok)

    hadronic = read_csv(HADRONIC_CSV)
    expected_hadronic = {f"HAD4944_{index:02d}_{suffix}" for index, suffix in enumerate((
        "no_free_current_quarks",
        "scalar_loop_anchors",
        "curved_chiral_LECs",
        "no_cancellation_assumption",
        "total_bound_bypass",
        "primary_likelihood",
    ))}
    hadronic_ids = {row["gate_id"] for row in hadronic}
    hadronic_ok = (
        len(hadronic) == 6
        and hadronic_ids == expected_hadronic
        and all(row["passed"] == "True" for row in hadronic)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in hadronic)
    )
    add(checks, "VAL4944_15_hadronic", "six hadronic and bound gates", sorted(expected_hadronic), sorted(hadronic_ids), hadronic_ok)
    hadronic_map = {row["gate_id"]: row for row in hadronic}
    no_closure_ok = (
        "not inserted" in hadronic_map["HAD4944_00_no_free_current_quarks"]["statement"]
        and "neither set to zero nor tuned" in hadronic_map["HAD4944_03_no_cancellation_assumption"]["statement"]
        and "secondary recast" in hadronic_map["HAD4944_05_primary_likelihood"]["statement"]
    )
    add(checks, "VAL4944_16_no_closure", "no quark or cancellation closure", "all clauses", no_closure_ok, no_closure_ok)

    local = read_csv(LOCAL_CSV)
    expected_systems = {
        "Earth",
        "Sun",
        "one_solar_mass_white_dwarf",
        "1.4_solar_mass_12km_neutron_star",
        "10_solar_mass_Schwarzschild_horizon",
    }
    systems = {row["system"] for row in local}
    local_structure_ok = (
        len(local) == 5
        and systems == expected_systems
        and all(row["passed"] == "True" for row in local)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in local)
    )
    add(checks, "VAL4944_17_local_structure", "five local systems", sorted(expected_systems), sorted(systems), local_structure_ok)
    local_map = {row["system"]: row for row in local}
    local_values_ok = (
        math.isclose(float(local_map["Sun"]["conditional_total_abs_Delta_v_pol_over_c"]), 3.158862816269501e-16, rel_tol=1e-14)
        and math.isclose(float(local_map["one_solar_mass_white_dwarf"]["conditional_total_abs_Delta_v_pol_over_c"]), 3.101006351170222e-10, rel_tol=1e-14)
        and math.isclose(float(local_map["1.4_solar_mass_12km_neutron_star"]["conditional_total_abs_Delta_v_pol_over_c"]), 0.08617495658749656, rel_tol=1e-14)
        and math.isclose(float(local_map["10_solar_mass_Schwarzschild_horizon"]["conditional_total_abs_Delta_v_pol_over_c"]), 0.04129112406684336, rel_tol=1e-14)
    )
    add(checks, "VAL4944_18_local_values", "locked local bound values", "Sun WD NS BH", [local_map[key]["conditional_total_abs_Delta_v_pol_over_c"] for key in ("Sun", "one_solar_mass_white_dwarf", "1.4_solar_mass_12km_neutron_star", "10_solar_mass_Schwarzschild_horizon")], local_values_ok)
    local_scope_ok = all(
        float(row["conditional_total_abs_Delta_v_pol_over_c"]) < 0.1
        and row["linearized_total_bound_below_ten_percent"] == "True"
        and row["constant_PPN_interpretation"] == "NOT_A_CONSTANT_PPN_COEFFICIENT"
        and row["valid_for_general_physical_CFF_claim"] == "False"
        for row in local
    )
    add(checks, "VAL4944_19_local_scope", "linear and PPN firewalls", "all pass", local_scope_ok, local_scope_ok)

    boundary = result["claim_boundary"]
    boundary_ok = (
        boundary["free_lepton_thresholds_calculated"]
        and boundary["scalar_QED_CFF_formula_calculated"]
        and boundary["pointlike_pion_kaon_anchors_calculated"]
        and boundary["electroweak_spin1_complete_dimension_six_envelope_bounded"]
        and not boundary["electroweak_spin1_exact_signed_matching_calculated"]
        and not boundary["QCD_hadronic_local_matching_calculated"]
        and not boundary["QCD_hadronic_remainder_assumed_zero"]
        and boundary["conditional_complete_total_CFF_bound_constructed"]
        and not boundary["primary_robust_two_sided_CFF_likelihood_available"]
        and not boundary["complete_physical_CFF_prediction"]
        and not boundary["local_Maxwell_promoted"]
        and not boundary["full_MTS_fixed_point"]
    )
    add(checks, "VAL4944_20_boundary", "claim boundary", "controls true promotion false", boundary, boundary_ok)

    checkpoint_text = text(CHECKPOINT)
    checkpoint_ok = (
        CHECKPOINT_MARKER in checkpoint_text
        and NEXT_TARGET in checkpoint_text
        and "local Maxwell promotion                        = false;" in checkpoint_text
        and "8.61750e-2" in checkpoint_text
    )
    add(checks, "VAL4944_21_checkpoint", "checkpoint marker boundary and target", "all present", checkpoint_ok, checkpoint_ok)
    formal_text = text(FORMAL_NOTE)
    formal_ok = FORMAL_MARKER in formal_text and NEXT_TARGET in formal_text and "local Maxwell/full MTS promotion               = false." in formal_text
    add(checks, "VAL4944_22_formal", "formal marker boundary and target", "all present", formal_ok, formal_ok)

    claim_rows = [row for row in read_csv(CLAIMS) if row["claim_id"] == "L-786"]
    claim_ok = (
        len(claim_rows) == 1
        and NEXT_TARGET in claim_rows[0]["next_test"]
        and "QCD_REMAINDER_NOT_ZERO" in claim_rows[0]["notes"]
        and "LOCAL_MAXWELL_FALSE" in claim_rows[0]["notes"]
    )
    add(checks, "VAL4944_23_claim", "claim L-786 unique and scoped", "one row", claim_rows, claim_ok)

    expected_variables = {
        "CFFScalarThreshold4944_MTS",
        "CFFPionKaonAnchor4944_MTS",
        "WSpin1Envelope4944_MTS",
        "CFFCalculableControl4944_MTS",
        "CFFTotalBound4944_MTS",
        "CFFUnmatchedBound4944_MTS",
        "CFFLocalResidualVector4944_MTS",
        "PredictivityStatus4944_MTS",
    }
    found_variables = {row["symbol"] for row in read_csv(VARIABLES) if row["symbol"] in expected_variables}
    add(checks, "VAL4944_24_variables", "eight variables registered", sorted(expected_variables), sorted(found_variables), found_variables == expected_variables)

    register_ok = (
        "## 1.237 Visible CFF threshold hierarchy and total residual bound" in text(EQUATIONS)
        and "## 188. A total bound can bypass split matching but cannot predict it" in text(RED_TEAM)
        and "## PPC4161 checkpoint 4944 - visible CFF thresholds and total bound" in text(SPINE)
        and "## Current checkpoint 4944 handoff" in text(RESUME)
        and NEXT_TARGET in text(RESUME)
    )
    add(checks, "VAL4944_25_registers", "equation red-team spine and resume updated", "all present", register_ok, register_ok)

    provenance_text = text(PROVENANCE)
    provenance_ok = (
        PROVENANCE_MARKER in provenance_text
        and all(expected in provenance_text for path, expected in HASH_LOCKS.items() if path not in {PROVENANCE, CHECKPOINT, FORMAL_NOTE})
        and "https://arxiv.org/abs/2512.12743" in provenance_text
        and "valid_for_full_MTS_claim=False" in provenance_text
        and "not cited as a calculation" in provenance_text
    )
    add(checks, "VAL4944_26_provenance", "provenance hashes sources and firewall", "all present", provenance_ok, provenance_ok)

    errors: list[str] = []
    csv_paths = (CLAIMS, VARIABLES, SPIN1_CSV, COMPONENT_CSV, HADRONIC_CSV, LOCAL_CSV)
    for path in csv_paths:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            raw_rows = list(csv.reader(handle))
        width = len(raw_rows[0])
        errors.extend(
            f"{path.name}:{index}:width"
            for index, row in enumerate(raw_rows[1:], start=2)
            if len(row) != width
        )
    for path in (SPIN1_CSV, COMPONENT_CSV, HADRONIC_CSV, LOCAL_CSV):
        for index, row in enumerate(read_csv(path), start=2):
            if row["valid_for_full_MTS_claim"] != "False":
                errors.append(f"{path.name}:{index}:claim")
            if any("MISSING_" in value or value == "MISSING" for value in row.values() if value):
                errors.append(f"{path.name}:{index}:missing")
    add(checks, "VAL4944_27_csv_firewall", "CSV shape and evidence firewall", [], errors, not errors)

    pycache = sorted(str(path) for path in (POST / "scripts").glob("__pycache__") if path.exists())
    add(checks, "VAL4944_28_pycache", "scripts pycache absent", [], pycache, not pycache)

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
