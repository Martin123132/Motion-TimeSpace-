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
SOURCE = POST / "source-intake" / "functional_rg" / "4943"
OUTPUT = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4943_VALIDATION.csv"

MAIN_SCRIPT = POST / "scripts" / "Y5_R2FR_4943_matter_source_junction_stability.py"
RESULT_JSON = SOURCE / "matter_source_junction_stability_results.json"
SELECTION_CSV = SOURCE / "matter_source_selection_rules.csv"
CONTACT_CSV = SOURCE / "interior_quadratic_contact_derivation.csv"
STABILITY_CSV = SOURCE / "interior_stability_benchmarks.csv"
JUNCTION_CSV = SOURCE / "junction_scalar_charge_and_fifth_force.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = POST / "4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md"
FORMAL_NOTE = FORMAL / "959-PPC4161-matter-source-interior-junction-no-fifth-force.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

RESULT_MARKER = "MTS_4943_MATTER_SOURCE_JUNCTION_STABILITY"
CHECKPOINT_MARKER = "MTS_MATTER_SOURCE_INTERIOR_JUNCTION_NO_FIFTH_FORCE_4943"
FORMAL_MARKER = "PPC4161_MATTER_SOURCE_INTERIOR_JUNCTION_NO_FIFTH_FORCE_4943"
PROVENANCE_MARKER = "MTS_MATTER_SOURCE_JUNCTION_STABILITY_PROVENANCE_4943"
NEXT_TARGET = "4944-Y5-R2FR-complete-electroweak-spin1-and-hadronic-CFF-matching-or-total-photon-residual-bound.md"

HASH_LOCKS = {
    MAIN_SCRIPT: "61d117285443662dca15d4120a05e2c149bfc8db5f353e94295015f82058df0c",
    RESULT_JSON: "67ff98eb4e0bec17906e1515fef3d07f85a00480941d882cc31261639707eebb",
    SELECTION_CSV: "2e9308c2d88336aeeab957fe78ce3d3a1d912809fc9a20afc416031394fb7a1b",
    CONTACT_CSV: "334291e78d9c9efc38d9c9d5741004ca191906bc8d9243d5091d96c6e4a4eccd",
    STABILITY_CSV: "3c49fdc86490eb936c27fc954b420ab1205fa2e6211e87507cc33cec7f64e3af",
    JUNCTION_CSV: "5fbca2c1672d7fbb6f1741e56a3c72a2adbaee544a4fd5fd5525a616cb836df6",
    PROVENANCE: "70cadef15d608143e8e41a5cb3869e70fa7f3e180af3da793bf8c49f3c45f1fd",
    CHECKPOINT: "a90da0e9ad0457fc3dbdb389d7bf2715cb9d707cbffa094a987b0b0553e257b5",
    FORMAL_NOTE: "71b71425296c6b3023ee162a70d712c474fbb6c2bdc82cbd061289ff68488bf1",
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
    add(checks, "VAL4943_01_paths", "locked paths exist", [], missing, not missing)
    bad_hashes = {
        str(path): (expected, digest(path))
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "VAL4943_02_hashes", "locked hashes match", {}, bad_hashes, not bad_hashes)

    compile_errors: list[str] = []
    for path in (MAIN_SCRIPT, Path(__file__).resolve()):
        try:
            compile(text(path), str(path), "exec")
        except Exception as exc:
            compile_errors.append(f"{path.name}:{exc}")
    add(checks, "VAL4943_03_compile", "scripts compile in memory", [], compile_errors, not compile_errors)

    result = json.loads(text(RESULT_JSON))
    add(checks, "VAL4943_04_marker", "result marker", RESULT_MARKER, result.get("marker"), result.get("marker") == RESULT_MARKER)
    failed_internal = [name for name, passed in result["checks"].items() if not passed]
    add(checks, "VAL4943_05_internal", "research checks pass", [], failed_internal, not failed_internal)
    source_hash_errors = [
        key
        for key, expected in result["source_hashes"].items()
        if not (ROOT / Path(key)).exists() or digest(ROOT / Path(key)) != expected
    ]
    add(checks, "VAL4943_06_sources", "result source paths and hashes", [], source_hash_errors, not source_hash_errors)

    selection = read_csv(SELECTION_CSV)
    expected_selection = {f"SRC4943_{index:02d}_{suffix}" for index, suffix in enumerate((
        "parent_arguments",
        "fixed_metric_factorization",
        "diagonal_reflection",
        "gravity_mediation",
        "boundary_state",
        "S6_O1",
        "S6_O2",
        "S6_O3",
        "S6_O4",
        "S6_O5",
    ))}
    selection_ids = {row["rule_id"] for row in selection}
    selection_ok = (
        len(selection) == 10
        and selection_ids == expected_selection
        and all(row["passed"] == "True" for row in selection)
        and all(row["valid_for_declared_integrated_H_local_branch"] == "True" for row in selection)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in selection)
    )
    add(checks, "VAL4943_07_selection", "ten source and parity rules", sorted(expected_selection), sorted(selection_ids), selection_ok)
    selection_map = {row["rule_id"]: row for row in selection}
    source_rule_ok = (
        "delta S_SM/delta psi=0" in selection_map["SRC4943_00_parent_arguments"]["consequence"]
        and "all direct hidden-visible" in selection_map["SRC4943_01_fixed_metric_factorization"]["consequence"]
        and "Gamma_eff" in selection_map["SRC4943_02_diagonal_reflection"]["consequence"]
        and "no one-psi source" in selection_map["SRC4943_03_gravity_mediation"]["consequence"]
    )
    add(checks, "VAL4943_08_source_rule", "parent no-source chain", "all clauses", source_rule_ok, source_rule_ok)
    o5 = selection_map["SRC4943_09_S6_O5"]
    o5_ok = o5["status"] == "FORBIDDEN_BY_SELECTED_MOTION_REFLECTION" and "u_O5=0" in o5["consequence"]
    add(checks, "VAL4943_09_O5", "odd O5 forbidden", "reflection-forbidden", o5, o5_ok)

    contact = read_csv(CONTACT_CSV)
    contact_map = {row["quantity"]: row for row in contact}
    expected_contact = {"Delta_L_contact", "A_time", "B_space", "m_effective_squared", "linear_tadpole"}
    contact_ok = (
        len(contact) == 5
        and set(contact_map) == expected_contact
        and all(row["passed"] == "True" for row in contact)
        and all(row["symbolic_residual"] == "0" for row in contact)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in contact)
    )
    add(checks, "VAL4943_10_contact", "five exact contact rows", sorted(expected_contact), sorted(contact_map), contact_ok)
    contact_formula_ok = (
        "8*a_C*rho" in contact_map["A_time"]["expected"]
        and "-8*a_C*p" in contact_map["B_space"]["expected"]
        and "-a_C/3 + 2*a_R" in contact_map["m_effective_squared"]["expected"]
        and contact_map["linear_tadpole"]["expected"] == "0"
    )
    add(checks, "VAL4943_11_contact_formula", "kinetic mass and tadpole formulas", "all clauses", contact_formula_ok, contact_formula_ok)

    stability = read_csv(STABILITY_CSV)
    expected_systems = {"Earth", "Sun", "one_solar_mass_white_dwarf", "1.4_solar_mass_12km_neutron_star"}
    structure = {
        "rows": len(stability),
        "systems": sorted({row["system"] for row in stability}),
        "multipliers": sorted({float(row["density_multiplier_over_mean"]) for row in stability}),
    }
    structure_ok = structure == {"rows": 8, "systems": sorted(expected_systems), "multipliers": [1.0, 10.0]}
    add(checks, "VAL4943_12_stability_structure", "eight benchmark rows", {"rows": 8, "systems": sorted(expected_systems), "multipliers": [1.0, 10.0]}, structure, structure_ok)
    positivity = all(
        float(row["A_time_lower"]) > 0
        and float(row["B_space_lower"]) > 0
        and float(row["m_effective_squared_ratio_lower"]) > 0
        and row["scalarization_from_declared_quadratic_packet"] == "False"
        and row["status"] == "STRICT_EFT_DEC_STABILITY_BOUND"
        and row["valid_for_full_MTS_claim"] == "False"
        for row in stability
    )
    add(checks, "VAL4943_13_positivity", "all quadratic rows positive", "all pass", positivity, positivity)
    max_kinetic = max(float(row["DEC_abs_delta_A_or_B_bound"]) for row in stability)
    max_speed = max(float(row["abs_delta_cpsi_squared_bound"]) for row in stability)
    max_mass = max(float(row["abs_delta_m2_over_m2_bound"]) for row in stability)
    worst_ok = (
        math.isclose(max_kinetic, 9.058001273285048e-18, rel_tol=1e-14)
        and math.isclose(max_speed, 1.8116002546570096e-17, rel_tol=1e-14)
        and math.isclose(max_mass, 7.764001091390056e-18, rel_tol=1e-14)
    )
    add(checks, "VAL4943_14_worst", "locked worst stability triple", [9.058001273285048e-18, 1.8116002546570096e-17, 7.764001091390056e-18], [max_kinetic, max_speed, max_mass], worst_ok)
    critical_ricci = {float(row["critical_ricci_m_minus_2"]) for row in stability}
    critical_density = {float(row["critical_density_kg_m3"]) for row in stability}
    critical_ok = (
        len(critical_ricci) == 1
        and len(critical_density) == 1
        and math.isclose(next(iter(critical_ricci)), 7924767535.300136, rel_tol=1e-14)
        and math.isclose(next(iter(critical_density)), 4.246023114199768e35, rel_tol=1e-14)
    )
    add(checks, "VAL4943_15_critical", "critical proxy thresholds", "locked", [*critical_ricci, *critical_density], critical_ok)

    junction = read_csv(JUNCTION_CSV)
    expected_junction = {f"JUNC4943_{index:02d}_{suffix}" for index, suffix in enumerate((
        "bulk", "field", "flux", "scalar_charge", "single_exchange", "energy", "fifth_force"
    ))}
    junction_ids = {row["gate_id"] for row in junction}
    junction_ok = (
        len(junction) == 7
        and junction_ids == expected_junction
        and all(row["passed"] == "True" for row in junction)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in junction)
    )
    add(checks, "VAL4943_16_junction", "seven junction and force rows", sorted(expected_junction), sorted(junction_ids), junction_ok)
    junction_map = {row["gate_id"]: row for row in junction}
    flux_ok = (
        "[psi]_Sigma=0" in junction_map["JUNC4943_01_field"]["equation"]
        and "K_eff" in junction_map["JUNC4943_02_flux"]["equation"]
        and "Q_psi" in junction_map["JUNC4943_03_scalar_charge"]["equation"]
    )
    add(checks, "VAL4943_17_flux", "field flux and charge equations", "all present", flux_ok, flux_ok)
    force_ok = (
        junction_map["JUNC4943_03_scalar_charge"]["result"] == "ordinary source carries no one-scalar charge"
        and junction_map["JUNC4943_04_single_exchange"]["result"] == "no classical single-scalar fifth-force pole"
        and junction_map["JUNC4943_06_fifth_force"]["equation"] == "a_psi/a_N=0 at classical one-scalar order"
    )
    add(checks, "VAL4943_18_force", "scalar charge and force zero", "all exact", force_ok, force_ok)

    boundary = result["claim_boundary"]
    boundary_ok = (
        boundary["ordinary_matter_direct_motion_source_zero_in_selected_parent"]
        and boundary["reflection_even_effective_action_tadpole_zero"]
        and boundary["interior_zero_branch_continuation_derived"]
        and boundary["surface_flux_zero_branch_derived"]
        and boundary["ordinary_matter_scalar_charge_zero"]
        and boundary["classical_single_scalar_fifth_force_zero"]
        and boundary["strict_EFT_interior_quadratic_stability_bounded"]
        and not boundary["O5_present_on_reflection_even_branch"]
        and not boundary["nonvacuum_reflection_breaking_state_tested"]
        and not boundary["complete_visible_CFF_threshold_matching"]
        and not boundary["full_MTS_fixed_point"]
        and not boundary["local_GR_Newton_Maxwell_promoted"]
    )
    add(checks, "VAL4943_19_boundary", "claim boundary", "selected branch true full false", boundary, boundary_ok)

    checkpoint_text = text(CHECKPOINT)
    checkpoint_ok = (
        CHECKPOINT_MARKER in checkpoint_text
        and NEXT_TARGET in checkpoint_text
        and "local GR/Newton/Maxwell promotion              = false." in checkpoint_text
        and "a_psi/a_N=0" in checkpoint_text
    )
    add(checks, "VAL4943_20_checkpoint", "checkpoint marker boundary and target", "all present", checkpoint_ok, checkpoint_ok)
    formal_text = text(FORMAL_NOTE)
    formal_ok = FORMAL_MARKER in formal_text and NEXT_TARGET in formal_text and "full MTS/local-GR promotion                    = false." in formal_text
    add(checks, "VAL4943_21_formal", "formal marker boundary and target", "all present", formal_ok, formal_ok)

    claim_rows = [row for row in read_csv(CLAIMS) if row["claim_id"] == "L-785"]
    claim_ok = (
        len(claim_rows) == 1
        and NEXT_TARGET in claim_rows[0]["next_test"]
        and "SCALAR_CHARGE_ZERO" in claim_rows[0]["notes"]
        and "LOCAL_GR_FALSE" in claim_rows[0]["notes"]
    )
    add(checks, "VAL4943_22_claim", "claim L-785 unique and scoped", "one row", claim_rows, claim_ok)

    expected_variables = {
        "MatterSourceZero4943_MTS",
        "MotionReflection4943_MTS",
        "InteriorKineticA4943_MTS",
        "InteriorKineticB4943_MTS",
        "InteriorMass4943_MTS",
        "ScalarJunction4943_MTS",
        "ScalarCharge4943_MTS",
        "PredictivityStatus4943_MTS",
    }
    found_variables = {row["symbol"] for row in read_csv(VARIABLES) if row["symbol"] in expected_variables}
    add(checks, "VAL4943_23_variables", "eight variables registered", sorted(expected_variables), sorted(found_variables), found_variables == expected_variables)

    register_ok = (
        "## 1.236 Matter-source interior continuation, junction and no fifth force" in text(EQUATIONS)
        and "## 187. A selected no-source theorem is not a derivation of visible matter" in text(RED_TEAM)
        and "## PPC4161 checkpoint 4943 - matter-source continuation and no fifth force" in text(SPINE)
        and "## Current checkpoint 4943 handoff" in text(RESUME)
        and NEXT_TARGET in text(RESUME)
    )
    add(checks, "VAL4943_24_registers", "equation red-team spine and resume updated", "all present", register_ok, register_ok)

    provenance_text = text(PROVENANCE)
    provenance_ok = (
        PROVENANCE_MARKER in provenance_text
        and all(expected in provenance_text for path, expected in HASH_LOCKS.items() if path not in {PROVENANCE, CHECKPOINT, FORMAL_NOTE})
        and "valid_for_full_MTS_claim=False" in provenance_text
        and "does not derive the public matter functor" in provenance_text
    )
    add(checks, "VAL4943_25_provenance", "provenance hashes and firewall", "all present", provenance_ok, provenance_ok)

    errors: list[str] = []
    csv_paths = (CLAIMS, VARIABLES, SELECTION_CSV, CONTACT_CSV, STABILITY_CSV, JUNCTION_CSV)
    for path in csv_paths:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            raw_rows = list(csv.reader(handle))
        width = len(raw_rows[0])
        errors.extend(
            f"{path.name}:{index}:width"
            for index, row in enumerate(raw_rows[1:], start=2)
            if len(row) != width
        )
    for path in (SELECTION_CSV, CONTACT_CSV, STABILITY_CSV, JUNCTION_CSV):
        for index, row in enumerate(read_csv(path), start=2):
            if row["valid_for_full_MTS_claim"] != "False":
                errors.append(f"{path.name}:{index}:claim")
            if any("MISSING_" in value or value == "MISSING" for value in row.values() if value):
                errors.append(f"{path.name}:{index}:missing")
    add(checks, "VAL4943_26_csv_firewall", "CSV shape and evidence firewall", [], errors, not errors)

    pycache = sorted(str(path) for path in (POST / "scripts").glob("__pycache__") if path.exists())
    add(checks, "VAL4943_27_pycache", "scripts pycache absent", [], pycache, not pycache)

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
