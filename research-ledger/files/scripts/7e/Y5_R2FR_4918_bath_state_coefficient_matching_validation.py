from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import Y5_R2FR_4918_bath_state_coefficient_matching as research


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
OUTPUT = POST / "source-intake" / "mts_residuals"
TIMESTAMP = datetime.now(timezone.utc).isoformat()
MARKER = research.MARKER
NEXT_TARGET = research.NEXT_TARGET
CLAIM_STATUS = (
    "active_IR_state_flow_contact_zero_by_Wilsonian_field_content_invariant_"
    "vacuum_enthalpy_zero_exact_bath_profile_and_loop_ray_derived_clock_"
    "profile_bound_and_universal_WEP_zero_full_vacuum_1PI_basis_open_private_"
    "nonclaim"
)
VARIABLES = (
    "BathLayerSplit4918_MTS",
    "InvariantVacuumStress4918_MTS",
    "BathEnthalpy4918_MTS",
    "BathTrace4918_MTS",
    "RetiredBathProfile4918_MTS",
    "CurvatureLoopRay4918_MTS",
    "CurvatureTotalMatching4918_MTS",
    "ClockKappa4918_MTS",
    "UniversalContactWEP4918_MTS",
    "StateFlowGate4918_MTS",
)
EVIDENCE = (
    "P8_Y5_R2FR_4918_ACTIVE_LAYER_SPLIT.csv",
    "P8_Y5_R2FR_4918_BATH_STRESS_IDENTITIES.csv",
    "P8_Y5_R2FR_4918_RETIRED_STATE_PROFILE.csv",
    "P8_Y5_R2FR_4918_CURVATURE_MATCHING.csv",
    "P8_Y5_R2FR_4918_LOOP_PROFILE_PROJECTION.csv",
    "P8_Y5_R2FR_4918_ARENA_PROJECTION.csv",
    "P8_Y5_R2FR_4918_GATE_DECISION.csv",
    "P8_Y5_R2FR_4918_SOURCE_REGISTER.csv",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bool_cell(value: str) -> bool:
    return value.strip().lower() == "true"


def compile_source(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except (OSError, SyntaxError, UnicodeError):
        return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    def check(check_id: str, condition: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4917_VALIDATION.csv")
    retired_validation = read_csv(OUTPUT / "P8_Y5_BRR545_4896_VALIDATION.csv")
    layers = read_csv(OUTPUT / EVIDENCE[0])
    stress = read_csv(OUTPUT / EVIDENCE[1])
    profiles = read_csv(OUTPUT / EVIDENCE[2])
    matching = read_csv(OUTPUT / EVIDENCE[3])
    loop_profiles = read_csv(OUTPUT / EVIDENCE[4])
    arenas = read_csv(OUTPUT / EVIDENCE[5])
    decisions = read_csv(OUTPUT / EVIDENCE[6])
    sources = read_csv(OUTPUT / EVIDENCE[7])
    layer_map = {row["layer_id"]: row for row in layers}
    stress_map = {row["identity_id"]: row for row in stress}
    matching_map = {row["matching_id"]: row for row in matching}
    arena_map = {row["arena_id"]: row for row in arenas}
    decision_map = {row["gate"]: row for row in decisions}
    profile_z0 = min(profiles, key=lambda row: abs(float(row["redshift"])))
    profile_early = max(profiles, key=lambda row: float(row["redshift"]))
    loop_z0 = min(loop_profiles, key=lambda row: abs(float(row["redshift"])))

    checkpoint_path = (
        POST
        / "4918-Y5-R2FR-closed-bath-state-enthalpy-trace-profile-and-renormalized-aC-aR-matching-or-multiarena-bound.md"
    )
    formal_path = (
        FORMAL / "934-PPC4161-bath-state-curvature-matching-local-gate.md"
    )
    provenance_path = (
        POST / "source-intake" / "parent_coupling" / "4918" / "PROVENANCE.md"
    )
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    formal_note = formal_path.read_text(encoding="utf-8")
    provenance = provenance_path.read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(encoding="utf-8")
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8")
    spine = (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-760"
    ]
    variable_rows = [
        row
        for row in read_csv(FORMAL / "04-variable-audit.csv")
        if row.get("symbol") in VARIABLES
    ]
    variable_sources_exist = all(
        all((ROOT / source).exists() for source in row["source_files"].split(";"))
        for row in variable_rows
    )
    evidence_paths = [OUTPUT / filename for filename in EVIDENCE]
    all_evidence_rows = [row for path in evidence_paths for row in read_csv(path)]
    numeric_cells: list[float] = []
    for row in all_evidence_rows:
        for value in row.values():
            try:
                numeric_cells.append(float(value))
            except (TypeError, ValueError):
                pass
    scripts = [
        SCRIPTS / "Y5_R2FR_4918_bath_state_coefficient_matching.py",
        SCRIPTS / "Y5_R2FR_4918_bath_state_coefficient_matching_validation.py",
    ]
    calibration = research.calibration_values()

    rows = [
        check(
            "VAL4918_00_prior",
            prior[-1]["check_id"] == "VAL4917_OVERALL"
            and prior[-1]["status"] == "PASS",
            "4917 predecessor validation passes",
        ),
        check(
            "VAL4918_01_retired_parent",
            retired_validation[-1]["check_id"] == "VAL4896_OVERALL"
            and retired_validation[-1]["status"] == "PASS",
            "4896 stress parent and retirement validation passes",
        ),
        check(
            "VAL4918_02_layers",
            len(layers) == 7 and all(bool_cell(row["passed"]) for row in layers),
            "seven microscopic matching active and extension layer rows pass",
        ),
        check(
            "VAL4918_03_active_field_content",
            layer_map["LAYER4918_02_active_IR"]["status"]
            == "ACTIVE_METRIC_ONLY_BASELINE"
            and not bool_cell(
                layer_map["LAYER4918_02_active_IR"]["independent_T_X_in_IR"]
            ),
            "active IR action contains no independent bath source",
        ),
        check(
            "VAL4918_04_invariant_vacuum",
            layer_map["LAYER4918_03_invariant_vacuum"]["status"]
            == "H_X_ZERO_NO_FLOW_SPURION",
            "invariant vacuum has zero enthalpy and no flow spurion",
        ),
        check(
            "VAL4918_05_extension_split",
            bool_cell(
                layer_map["LAYER4918_05_excited_state"]["independent_T_X_in_IR"]
            )
            and layer_map["LAYER4918_05_excited_state"]["status"]
            == "REENTRY_EXTENSION_REQUIRES_GATE",
            "nonvacuum state is kept as an explicit extension",
        ),
        check(
            "VAL4918_06_stress_rows",
            len(stress) == 6 and all(bool_cell(row["passed"]) for row in stress),
            "density enthalpy trace and stationary limits pass",
        ),
        check(
            "VAL4918_07_trace_identity",
            float(stress_map["STRESS4918_02_trace"]["symbolic_residual"]) == 0.0,
            "tau=3h-4rho expansion is exact",
        ),
        check(
            "VAL4918_08_vacuum_stress",
            float(
                stress_map["STRESS4918_03_invariant_vacuum"][
                    "symbolic_residual"
                ]
            )
            == 0.0
            and "h_X=0" in stress_map["STRESS4918_03_invariant_vacuum"]["formula"],
            "vacuum enthalpy zero is executable",
        ),
        check(
            "VAL4918_09_nonzero_current",
            "p_B=0" in stress_map["STRESS4918_05_nonzero_clock_current"]["formula"],
            "nonzero stationary clock current is correctly retained as dust",
        ),
        check(
            "VAL4918_10_profiles",
            len(profiles) == 8
            and all(bool_cell(row["passed"]) for row in profiles)
            and max(
                float(row["Raychaudhuri_reconstruction_residual"])
                for row in profiles
            )
            < 5.0e-16,
            "eight retired profile rows reconstruct Raychaudhuri",
        ),
        check(
            "VAL4918_11_present_profile",
            math.isclose(
                float(profile_z0["rho_B_over_3M2H2"]), 0.049, rel_tol=1e-12
            )
            and math.isclose(
                float(profile_z0["h_B_over_3M2H2"]),
                0.3989648914098004,
                rel_tol=1e-12,
            )
            and math.isclose(
                float(profile_z0["tau_B_over_3M2H2"]),
                1.0008946742294031,
                rel_tol=1e-12,
            ),
            "present retired bath density enthalpy and trace reproduce the parent output",
        ),
        check(
            "VAL4918_12_early_profile",
            math.isclose(
                float(profile_early["h_B_over_3M2H2"]),
                -1.3995433837714693,
                rel_tol=1e-12,
            )
            and float(profile_early["rho_B_over_3M2H2"]) < 0,
            "retired branch early pathology remains visible",
        ),
        check(
            "VAL4918_13_profile_scope",
            all(
                row["branch_status"] == "RETIRED_DIAGNOSTIC_NOT_ACTIVE_BASELINE"
                for row in profiles
            ),
            "retired profile cannot silently re-enter the active cosmology",
        ),
        check(
            "VAL4918_14_matching",
            len(matching) == 8
            and all(bool_cell(row["passed"]) for row in matching),
            "curvature matching decomposition and loop ray pass",
        ),
        check(
            "VAL4918_15_loop_prefactors",
            math.isclose(
                float(matching_map["MATCH4918_03_aC_loop"]["numeric_per_L"]),
                1.0 / (128.0 * math.pi**2),
                rel_tol=1e-14,
            )
            and math.isclose(
                float(matching_map["MATCH4918_04_aR_loop"]["numeric_per_L"]),
                1.0 / (384.0 * math.pi**2),
                rel_tol=1e-14,
            ),
            "selected a_C and a_R matter-loop prefactors are correct",
        ),
        check(
            "VAL4918_16_loop_ratio",
            math.isclose(
                float(matching_map["MATCH4918_05_loop_ray"]["numeric_per_L"]),
                1.0 / 3.0,
                rel_tol=1e-14,
            ),
            "selected loop ray has a_R/a_C=1/3",
        ),
        check(
            "VAL4918_17_total_open",
            matching_map["MATCH4918_00_aC_total"]["status"]
            == "TOTAL_OPEN_DECOMPOSITION_EXACT"
            and matching_map["MATCH4918_07_finite_boundary"]["status"]
            == "NOT_SELECTED_AS_DERIVATION",
            "finite and omitted total coefficients are not set to zero",
        ),
        check(
            "VAL4918_18_loop_profiles",
            len(loop_profiles) == 8
            and all(bool_cell(row["passed"]) for row in loop_profiles)
            and all(
                row["branch_status"] == "RETIRED_DIAGNOSTIC_NOT_ACTIVE_BASELINE"
                for row in loop_profiles
            ),
            "eight loop projections remain finite and quarantined",
        ),
        check(
            "VAL4918_19_present_loop",
            math.isclose(
                float(loop_z0["p_mix_per_L"]),
                -2.6416369999419466e-123,
                rel_tol=1e-12,
            )
            and math.isclose(
                float(loop_z0["clock_kappa_per_L"]),
                -7.14482601544383e-124,
                rel_tol=1e-12,
            ),
            "present retired loop projection has the derived Planck hierarchy",
        ),
        check(
            "VAL4918_20_calibration",
            math.isclose(
                calibration["critical_ratio_3H0sq_over_M2"],
                1.0455822142576514e-120,
                rel_tol=1e-12,
            ),
            "H0 and one calibrated Planck mass give the expected hierarchy",
        ),
        check(
            "VAL4918_21_arenas",
            len(arenas) == 8 and all(bool_cell(row["passed"]) for row in arenas),
            "active and extension arena projections pass",
        ),
        check(
            "VAL4918_22_clock_formula",
            "p_mix/2-sigma_mix"
            in arena_map["ARENA4918_05_clock_profile"]["profile_or_observable"],
            "clock projection uses p_mix/2-sigma_mix rather than sigma alone",
        ),
        check(
            "VAL4918_23_Galileo_bound",
            math.isclose(
                float(arena_map["ARENA4918_05_clock_profile"]["numeric_value"]),
                1.3548126671703264e-14,
                rel_tol=1e-12,
            ),
            "Galileo alpha interval is mapped to a profile-difference bound",
        ),
        check(
            "VAL4918_24_WEP_zero",
            arena_map["ARENA4918_02_active_WEP"]["status"]
            == "EXACT_UNIVERSAL_METRIC_ZERO"
            and float(arena_map["ARENA4918_02_active_WEP"]["numeric_value"])
            == 0.0,
            "universal stress contact gives zero test-body Eotvos residual",
        ),
        check(
            "VAL4918_25_Maxwell_zero",
            arena_map["ARENA4918_03_Maxwell_trace"]["status"]
            == "EXACT_CONFORMAL_ZERO",
            "trace shift does not change the classical Maxwell cone",
        ),
        check(
            "VAL4918_26_decisions",
            len(decisions) == 9
            and decision_map["active_IR_bath_source"]["status"]
            == "ZERO_BY_EXPLICIT_WILSONIAN_FIELD_CONTENT"
            and decision_map["invariant_vacuum_enthalpy"]["status"]
            == "ZERO_BY_STATE_SYMMETRY",
            "active and invariant-vacuum state decisions are explicit",
        ),
        check(
            "VAL4918_27_retired_decision",
            decision_map["nonvacuum_state_profile"]["status"]
            == "DERIVED_FOR_4896_BUT_BRANCH_RETIRED",
            "derived profile is not promoted",
        ),
        check(
            "VAL4918_28_total_decision",
            decision_map["curvature_total_matching"]["status"]
            == "OPEN_FINITE_HGHOST_THRESHOLD_TERMS",
            "total curvature matching remains honestly open",
        ),
        check(
            "VAL4918_29_next_decision",
            decision_map["full_vacuum_1PI_local_GR"]["decision"] == NEXT_TARGET,
            "next target advances to the surviving vacuum 1PI basis",
        ),
        check(
            "VAL4918_30_sources",
            len(sources) == 22
            and all(
                bool_cell(row["source_exists"])
                and bool_cell(row["marker_found"])
                and row["sha256"]
                for row in sources
            ),
            "all twenty-two source paths markers and hashes resolve",
        ),
        check(
            "VAL4918_31_documents",
            MARKER in checkpoint
            and research.FORMAL_MARKER in formal_note
            and "MTS_BATH_STATE_MATCHING_PROVENANCE_4918" in provenance,
            "checkpoint formal note and provenance markers exist",
        ),
        check(
            "VAL4918_32_document_integrity",
            "Integrating out a bath is not" not in checkpoint
            and "not the assertion that an active physical bath" in checkpoint
            and "kappa_{\\rm clock}" in checkpoint
            and "eta_{AB}=0" in checkpoint,
            "document distinguishes field content from stress cancellation and derives clock/WEP projections",
        ),
        check(
            "VAL4918_33_claim",
            len(claims) == 1 and claims[0]["status"] == CLAIM_STATUS,
            "L-760 is unique and accurately scoped",
        ),
        check(
            "VAL4918_34_variables",
            len(variable_rows) == len(VARIABLES)
            and {row["symbol"] for row in variable_rows} == set(VARIABLES),
            "ten checkpoint variables are unique",
        ),
        check(
            "VAL4918_35_variable_sources",
            variable_sources_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4918_36_registers",
            "1.211 Bath-state stress, loop ray and clock projection" in equations
            and "162. Integrating out a bath is not setting an active bath stress to zero"
            in redteam
            and "PPC4161 checkpoint 4918" in spine,
            "equation red-team and spine registers are updated",
        ),
        check(
            "VAL4918_37_resume",
            "4918-Y5-R2FR-closed-bath-state" in resume
            and research.FORMAL_MARKER in resume
            and NEXT_TARGET in resume,
            "resume points from state-flow closure to vacuum 1PI matching",
        ),
        check(
            "VAL4918_38_csv",
            len(evidence_paths) == 8
            and all(path.exists() and read_csv(path) for path in evidence_paths),
            "eight generated evidence CSVs parse",
        ),
        check(
            "VAL4918_39_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_evidence_rows
                for value in row.values()
            ),
            "generated evidence has no placeholder markers",
        ),
        check(
            "VAL4918_40_finite",
            all(math.isfinite(value) for value in numeric_cells),
            "all parsed numeric evidence cells are finite",
        ),
        check(
            "VAL4918_41_nonclaim",
            all(row.get("valid_for_claim") == "False" for row in all_evidence_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4918_42_scripts",
            all(compile_source(path) for path in scripts),
            "research and validation scripts compile",
        ),
        check(
            "VAL4918_43_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no scripts pycache exists",
        ),
        check(
            "VAL4918_44_next",
            NEXT_TARGET in checkpoint and not (POST / NEXT_TARGET).exists(),
            "4919 vacuum 1PI target is selected but not pre-created",
        ),
        check(
            "VAL4918_45_no_public_action",
            "No GitHub action or public claim is authorized." in checkpoint,
            "checkpoint remains local and private",
        ),
    ]
    rows.append(
        check(
            "VAL4918_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_BATH_STATE_CURVATURE_MATCHING_LOCAL_GATE_4918_VALIDATED",
        )
    )
    return rows


def main() -> int:
    validation = validation_rows()
    write_csv(OUTPUT / "P8_Y5_BRR545_4918_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4918_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4918_VALIDATION_FAIL"
    )
    if not passed:
        for row in validation:
            if row["status"] != "PASS":
                print(row["check_id"], row["detail"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
