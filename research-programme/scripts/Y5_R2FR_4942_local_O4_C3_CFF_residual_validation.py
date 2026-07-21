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
SOURCE = POST / "source-intake" / "functional_rg" / "4942"
OUTPUT = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4942_VALIDATION.csv"

MAIN_SCRIPT = POST / "scripts" / "Y5_R2FR_4942_local_O4_C3_CFF_residual.py"
RESULT_JSON = SOURCE / "local_O4_C3_CFF_residual_results.json"
ENDPOINT_CSV = SOURCE / "completed_O4_endpoint_Wilson_family.csv"
BRANCH_CSV = SOURCE / "local_homogeneous_branch_identities.csv"
RESIDUAL_CSV = SOURCE / "local_O4_C3_CFF_residual_vector.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = POST / "4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-branch-and-C3-CFF-PPN-residual-gate.md"
FORMAL_NOTE = FORMAL / "958-PPC4161-completed-O4-local-branch-and-C3-CFF-residual.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

RESULT_MARKER = "MTS_4942_LOCAL_O4_C3_CFF_RESIDUAL"
CHECKPOINT_MARKER = "MTS_O4_COMPLETED_ENDPOINT_LOCAL_BRANCH_C3_CFF_RESIDUAL_4942"
FORMAL_MARKER = "PPC4161_COMPLETED_O4_LOCAL_BRANCH_C3_CFF_RESIDUAL_4942"
PROVENANCE_MARKER = "MTS_COMPLETED_O4_LOCAL_BRANCH_C3_CFF_PROVENANCE_4942"
NEXT_TARGET = "4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md"

HASH_LOCKS = {
    MAIN_SCRIPT: "1c539d7ce99780085b23b1324e9aeb18e33ad14a0b767e4eff1287b62e439d5e",
    RESULT_JSON: "c830baff10125f984ba26d11d44465c4d519ecd6c51317b9c9fcac6cf5e2e04b",
    ENDPOINT_CSV: "fc994f761ef08155b926fee675b5617c40aad2ef24b701e645e208fda19b3dea",
    BRANCH_CSV: "e9e4532679843c78ab2c86ddc39589bb6c694ca9cb17aae6a7bae47af66d4d0a",
    RESIDUAL_CSV: "51f034326f02684491743d6b12fed9d54854885dae07e7894e77423f435a14a5",
    PROVENANCE: "a1ed7424cac629d95f67ba2c5a412125b71f6d615c9cd9545e5f2d4a38ad0492",
    CHECKPOINT: "64b96ca4e19a058ced85c0c4b800ae7a237408606799dd8c4a5b58935f635c5f",
    FORMAL_NOTE: "a4cc0f9a93d62e65d1a9055bf0602eb447a30f4204db87e397d9a99386c44ad7",
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
    add(checks, "VAL4942_01_paths", "locked paths exist", [], missing, not missing)
    bad_hashes = {
        str(path): (expected, digest(path))
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "VAL4942_02_hashes", "locked hashes match", {}, bad_hashes, not bad_hashes)

    compile_errors: list[str] = []
    for path in (MAIN_SCRIPT, Path(__file__).resolve()):
        try:
            compile(text(path), str(path), "exec")
        except Exception as exc:
            compile_errors.append(f"{path.name}:{exc}")
    add(checks, "VAL4942_03_compile", "scripts compile in memory", [], compile_errors, not compile_errors)

    result = json.loads(text(RESULT_JSON))
    add(checks, "VAL4942_04_marker", "result marker", RESULT_MARKER, result.get("marker"), result.get("marker") == RESULT_MARKER)
    failed_internal = [name for name, passed in result["checks"].items() if not passed]
    add(checks, "VAL4942_05_internal", "research checks pass", [], failed_internal, not failed_internal)

    endpoints = read_csv(ENDPOINT_CSV)
    family = {
        "rows": len(endpoints),
        "massless": sum(row["mapping"] == "massless_shared" for row in endpoints),
        "positive": sum(float(row["R_UV"]) > 0 for row in endpoints),
    }
    add(checks, "VAL4942_06_family", "45-row family structure", {"rows": 45, "massless": 3, "positive": 42}, family, family == {"rows": 45, "massless": 3, "positive": 42})
    endpoint_scope = all(
        row["termination"] == "IR_G_TARGET"
        and row["direct_O4_trace_closed_zero"] == "True"
        and row["valid_for_full_MTS_claim"] == "False"
        for row in endpoints
    )
    add(checks, "VAL4942_07_family_scope", "family reaches IR with firewall", "all pass", endpoint_scope, endpoint_scope)

    envelope = result["completed_family"]["envelope"]
    envelope_ok = (
        math.isclose(float(envelope["W_O4"]["minimum"]), -3.3191818497655214, abs_tol=1e-12)
        and math.isclose(float(envelope["A_C3"]["minimum"]), -2.2004419554225998e-5, abs_tol=1e-16)
        and math.isclose(float(envelope["W_C"]["maximum"]), 0.0006033651459509288, abs_tol=1e-15)
        and float(result["completed_family"]["W_O4_reconstruction_max_abs_gap"]) < 5e-10
    )
    add(checks, "VAL4942_08_envelope", "Wilson envelope and reconstruction", "locked extrema", envelope, envelope_ok)

    branches = read_csv(BRANCH_CSV)
    expected_ids = {
        "LOCAL4942_00_EOM",
        "LOCAL4942_01_zero_branch",
        "LOCAL4942_02_stress",
        "LOCAL4942_03_characteristic",
        "LOCAL4942_04_endpoint_map",
        "LOCAL4942_05_gap_independence",
        "LOCAL4942_06_PPN_orders",
        "LOCAL4942_07_Maxwell",
    }
    branch_map = {row["identity_id"]: row for row in branches}
    branch_ok = (
        set(branch_map) == expected_ids
        and all(row["passed"] == "True" for row in branches)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in branches)
    )
    add(checks, "VAL4942_09_branches", "eight branch identities pass", sorted(expected_ids), sorted(branch_map), len(branches) == 8 and branch_ok)
    branch_content = (
        "Z+2u C2" in branch_map["LOCAL4942_00_EOM"]["statement"]
        and "arbitrary m2" in branch_map["LOCAL4942_01_zero_branch"]["result"]
        and "same metric null cone" in branch_map["LOCAL4942_03_characteristic"]["result"]
        and "J_gap=0" in branch_map["LOCAL4942_05_gap_independence"]["statement"]
    )
    add(checks, "VAL4942_10_branch_content", "EOM cone and gap clauses", "all present", branch_content, branch_content)

    residuals = read_csv(RESIDUAL_CSV)
    expected_systems = {
        "Earth",
        "Sun",
        "one_solar_mass_white_dwarf",
        "1.4_solar_mass_12km_neutron_star",
        "10_solar_mass_Schwarzschild_horizon",
    }
    systems = {row["system"] for row in residuals}
    add(checks, "VAL4942_11_systems", "five systems projected", sorted(expected_systems), sorted(systems), len(residuals) == 5 and systems == expected_systems)
    positivity = all(
        float(row["O4_abs_Delta_Z_over_Z"]) < 1e-150
        and float(row["O4_Zeff_over_Z_lower"]) > 0
        for row in residuals
    )
    add(checks, "VAL4942_12_positivity", "Zeff positive and tiny", "all below 1e-150", [row["O4_abs_Delta_Z_over_Z"] for row in residuals], positivity)
    zero_vector = all(
        float(row["O4_scalar_cone_shift"]) == 0
        and float(row["O4_tree_metric_stress_on_psi0"]) == 0
        and float(row["PPN_delta_gamma_at_standard_order"]) == 0
        and float(row["PPN_delta_beta_at_standard_order"]) == 0
        and row["J_gap_retuned"] == "False"
        for row in residuals
    )
    add(checks, "VAL4942_13_zero_vector", "cone stress PPN and retuning vector", "(0,0,0,0,false)", zero_vector, zero_vector)
    nonzero_vector = all(
        float(row["C3_abs_Delta_acceleration_over_aN"]) > 0
        and float(row["CFF_parent_abs_Delta_v_pol_over_c"]) > 0
        for row in residuals
    )
    add(checks, "VAL4942_14_nonzero_vector", "C3 and CFF residuals retained", "positive", nonzero_vector, nonzero_vector)

    horizon = next(row for row in residuals if row["system"] == "10_solar_mass_Schwarzschild_horizon")
    horizon_ok = (
        math.isclose(float(horizon["C3_abs_Delta_acceleration_over_aN"]), 3.4724335367210295e-159, rel_tol=1e-12)
        and math.isclose(float(horizon["CFF_parent_abs_Delta_v_pol_over_c"]), 5.4499734609854115e-80, rel_tol=1e-12)
        and math.isclose(float(horizon["O4_abs_Delta_Z_over_Z"]), 7.145430739978276e-156, rel_tol=1e-12)
    )
    add(checks, "VAL4942_15_horizon", "horizon residual triple", "locked values", horizon, horizon_ok)

    physical = result["dimensionful_endpoint_envelope"]
    physical_ok = (
        math.isclose(float(physical["abs_u_O4_over_Z_m4"]), 2.265012477923484e-139, rel_tol=1e-12)
        and math.isclose(float(physical["abs_a_plus_m4"]), 7.547781585001645e-143, rel_tol=1e-12)
        and math.isclose(float(physical["abs_c_gamma_parent_m2"]), 7.922638687822437e-72, rel_tol=1e-12)
        and float(physical["free_lepton_to_parent_abs_ratio"]) > 1e41
    )
    add(checks, "VAL4942_16_physical", "dimensionful endpoint map", "locked values and ratio", physical, physical_ok)

    threshold_ok = all(
        math.isclose(float(row["RG_threshold_abs_Delta_beta_g_over_g_at_g1e_minus10_max"]), 5.305164769729845e-12, rel_tol=1e-14)
        for row in residuals
    )
    add(checks, "VAL4942_17_threshold", "RG threshold envelope", 5.305164769729845e-12, residuals[0]["RG_threshold_abs_Delta_beta_g_over_g_at_g1e_minus10_max"], threshold_ok)

    boundary = result["claim_boundary"]
    boundary_ok = (
        boundary["homogeneous_local_psi_zero_branch_derived"]
        and boundary["O4_scalar_characteristic_derived"]
        and boundary["same_endpoint_C3_CFF_O4_residual_vector_derived"]
        and boundary["higher_gradient_C3_residual_nonzero"]
        and boundary["curved_photon_CFF_residual_nonzero"]
        and not boundary["interior_source_matching_completed"]
        and not boundary["full_MTS_fixed_point"]
        and not boundary["local_GR_Newton_Maxwell_promoted"]
    )
    add(checks, "VAL4942_18_boundary", "claim boundary", "vacuum true full false", boundary, boundary_ok)

    checkpoint_ok = CHECKPOINT_MARKER in text(CHECKPOINT) and NEXT_TARGET in text(CHECKPOINT) and "local GR/Newton/Maxwell promotion              = false." in text(CHECKPOINT)
    add(checks, "VAL4942_19_checkpoint", "checkpoint marker boundary and target", "all present", checkpoint_ok, checkpoint_ok)
    formal_ok = FORMAL_MARKER in text(FORMAL_NOTE) and NEXT_TARGET in text(FORMAL_NOTE) and "full MTS/local-GR promotion                    = false." in text(FORMAL_NOTE)
    add(checks, "VAL4942_20_formal", "formal marker boundary and target", "all present", formal_ok, formal_ok)

    claim_rows = [row for row in read_csv(CLAIMS) if row["claim_id"] == "L-784"]
    claim_ok = len(claim_rows) == 1 and NEXT_TARGET in claim_rows[0]["next_test"] and "PSI_ZERO_EXACT_SOURCE_FREE" in claim_rows[0]["notes"] and "LOCAL_GR_FALSE" in claim_rows[0]["notes"]
    add(checks, "VAL4942_21_claim", "claim L-784 unique and scoped", "one row", claim_rows, claim_ok)

    expected_variables = {
        "Zeff4942_MTS",
        "PsiZero4942_MTS",
        "WilsonEnvelope4942_MTS",
        "C3Residual4942_MTS",
        "CFFResidual4942_MTS",
        "PPNVector4942_MTS",
        "JGapIndependence4942_MTS",
        "PredictivityStatus4942_MTS",
    }
    found_variables = {row["symbol"] for row in read_csv(VARIABLES) if row["symbol"] in expected_variables}
    add(checks, "VAL4942_22_variables", "eight variables registered", sorted(expected_variables), sorted(found_variables), found_variables == expected_variables)

    register_ok = (
        "## 1.235 Completed O4 local branch and same-family C3-CFF residual" in text(EQUATIONS)
        and "## 186. A vacuum zero branch is not yet a matter-source theorem" in text(RED_TEAM)
        and "## PPC4161 checkpoint 4942 - completed O4 local branch and residual vector" in text(SPINE)
        and "## Current checkpoint 4942 handoff" in text(RESUME)
        and NEXT_TARGET in text(RESUME)
    )
    add(checks, "VAL4942_23_registers", "equation red-team spine and resume updated", "all present", register_ok, register_ok)

    provenance_ok = (
        PROVENANCE_MARKER in text(PROVENANCE)
        and all(expected in text(PROVENANCE) for path, expected in HASH_LOCKS.items() if path != PROVENANCE)
        and "valid_for_full_MTS_claim=False" in text(PROVENANCE)
    )
    add(checks, "VAL4942_24_provenance", "provenance hashes and firewall", "all present", provenance_ok, provenance_ok)

    errors: list[str] = []
    for path in (CLAIMS, VARIABLES, ENDPOINT_CSV, BRANCH_CSV, RESIDUAL_CSV):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            raw_rows = list(csv.reader(handle))
        width = len(raw_rows[0])
        errors.extend(
            f"{path.name}:{index}:width"
            for index, row in enumerate(raw_rows[1:], start=2)
            if len(row) != width
        )
    for path in (ENDPOINT_CSV, BRANCH_CSV, RESIDUAL_CSV):
        for index, row in enumerate(read_csv(path), start=2):
            if row["valid_for_full_MTS_claim"] != "False":
                errors.append(f"{path.name}:{index}:claim")
            if any("MISSING_" in value for value in row.values() if value):
                errors.append(f"{path.name}:{index}:missing")
    source_errors = [key for key in result["source_hashes"] if not (ROOT / Path(key)).exists()]
    pycache = sorted(str(path) for path in (POST / "scripts").glob("__pycache__") if path.exists())
    errors.extend(f"source:{value}" for value in source_errors)
    errors.extend(f"pycache:{value}" for value in pycache)
    add(checks, "VAL4942_25_firewall", "CSV sources firewall and pycache", [], errors, not errors)

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
