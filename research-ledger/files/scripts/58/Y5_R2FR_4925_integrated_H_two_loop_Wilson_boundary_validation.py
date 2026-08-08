from __future__ import annotations

import csv
import importlib.util
import math
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"
TIMESTAMP = "2026-07-12T00:00:00Z"
MARKER = "MTS_INTEGRATED_H_TWO_LOOP_WILSON_BOUNDARY_4925"
FORMAL_MARKER = "PPC4161_INTEGRATED_H_TWO_LOOP_WILSON_BOUNDARY_4925"
NEXT_TARGET = (
    "4926-Y5-R2FR-known-massive-threshold-spectrum-and-motion-scale-"
    "normalization-or-low-energy-Wilson-posterior.md"
)
VARIABLES = {
    "HMetricJacobian4925_MTS",
    "WeylC3RenormalizedWilson4925_MTS",
    "WeylC3RGInvariant4925_MTS",
    "WeylC3SchemeShift4925_MTS",
    "WeylC3IRCoefficient4925_MTS",
    "WeylC3GWBound4925_MTS",
    "WeylC3InducedScale4925_MTS",
    "HeavyFieldC3ThresholdBasis4925_MTS",
    "WeylC3BoundaryRoutes4925_MTS",
    "VacuumGRWilsonStatus4925_MTS",
}
EVIDENCE = (
    "P8_Y5_R2FR_4925_PARENT_UV_OWNERSHIP.csv",
    "P8_Y5_R2FR_4925_H_TO_G_JACOBIAN.csv",
    "P8_Y5_R2FR_4925_RENORMALIZED_COEFFICIENT_COLLAPSE.csv",
    "P8_Y5_R2FR_4925_TWO_LOOP_RG_TRANSFER.csv",
    "P8_Y5_R2FR_4925_BOUNDARY_ROUTE_AUDIT.csv",
    "P8_Y5_R2FR_4925_HEAVY_FIELD_THRESHOLD_BASIS.csv",
    "P8_Y5_R2FR_4925_WILSON_BOUND.csv",
    "P8_Y5_R2FR_4925_INDUCED_SCALE_ENVELOPE.csv",
    "P8_Y5_R2FR_4925_GATE_DECISION.csv",
    "P8_Y5_R2FR_4925_SOURCE_REGISTER.csv",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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


def load_research() -> Any:
    path = SCRIPTS / "Y5_R2FR_4925_integrated_H_two_loop_Wilson_boundary.py"
    specification = importlib.util.spec_from_file_location("research_4925", path)
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load checkpoint 4925 research module")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def validation_rows() -> list[dict[str, Any]]:
    research = load_research()
    rows: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )

    evidence_paths = [OUTPUT / filename for filename in EVIDENCE]
    tables = {filename: read_csv(OUTPUT / filename) for filename in EVIDENCE}
    parent = tables[EVIDENCE[0]]
    jacobian = tables[EVIDENCE[1]]
    collapse = tables[EVIDENCE[2]]
    running = tables[EVIDENCE[3]]
    routes = tables[EVIDENCE[4]]
    thresholds = tables[EVIDENCE[5]]
    bounds = tables[EVIDENCE[6]]
    induced = tables[EVIDENCE[7]]
    decisions = tables[EVIDENCE[8]]
    sources = tables[EVIDENCE[9]]

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4924_VALIDATION.csv")
    check(
        "VAL4925_00_prior",
        prior[-1]["check_id"] == "VAL4924_OVERALL"
        and prior[-1]["status"] == "PASS",
        "checkpoint 4924 validation passed",
    )
    check(
        "VAL4925_01_evidence",
        all(path.exists() and read_csv(path) for path in evidence_paths),
        "all ten evidence files exist and parse",
    )
    parent_map = {row["audit_id"]: row for row in parent}
    check(
        "VAL4925_02_parent",
        len(parent) == 8
        and all(bool_cell(row["passed"]) for row in parent)
        and parent_map["UV4925_03_H_to_g_measure"]["status"]
        == "H_COORDINATE_JACOBIAN_C3_ZERO_DERIVED"
        and parent_map["UV4925_07_current_verdict"]["status"]
        == "ONE_WILSON_INPUT_SELECTED",
        "the UV audit closes the coordinate Jacobian and selects one Wilson input",
    )

    four_dimensional = [row for row in jacobian if int(row["dimension"]) == 4]
    controls = [row for row in jacobian if int(row["dimension"]) != 4]
    check(
        "VAL4925_03_jacobian_rows",
        len(jacobian) == 24
        and len(four_dimensional) == 16
        and len(controls) == 8
        and all(bool_cell(row["passed"]) for row in jacobian),
        "sixteen four-dimensional metrics and eight dimension controls pass",
    )
    check(
        "VAL4925_04_jacobian_unit",
        all(
            abs(abs(float(row["numeric_det_dH_dg"])) - 1.0) < 2.0e-8
            and float(row["four_dimensional_abs_det_minus_one"]) < 2.0e-8
            for row in four_dimensional
        ),
        "the full symmetric-component H-to-g Jacobian has unit magnitude in 4D",
    )
    check(
        "VAL4925_05_jacobian_formula",
        all(
            abs(
                float(row["numeric_det_dH_dg"])
                - float(row["theory_det_dH_dg"])
            )
            < 2.0e-8
            for row in jacobian
        ),
        "the general determinant formula reproduces every numerical control",
    )

    scheme_rows = [
        row for row in collapse if row["representation"] == "finite renormalization test"
    ]
    check(
        "VAL4925_06_collapse",
        len(collapse) == 8
        and len(scheme_rows) == 5
        and all(int(row["independent_local_I1_inputs"]) == 1 for row in collapse)
        and all(bool_cell(row["passed"]) for row in collapse),
        "bare and metric-ghost finite labels collapse to one renormalized input",
    )
    check(
        "VAL4925_07_scheme_invariance",
        all(float(row["invariance_error"]) < 1.0e-13 for row in scheme_rows),
        "five finite counterterm shifts leave the renormalized coefficient invariant",
    )

    inputs = research.physical_inputs()
    check(
        "VAL4925_08_physical_inputs",
        math.isclose(inputs["robust_abs_alpha"], 0.05390797991220972, rel_tol=1.0e-14)
        and math.isclose(
            inputs["robust_positive_alpha"], 0.0354924453877024, rel_tol=1.0e-14
        )
        and math.isclose(inputs["mass_q95_solar"], 69.18905836812272, rel_tol=1.0e-14),
        "the archived robustness and remnant-mass inputs reproduce",
    )
    check(
        "VAL4925_09_lengths",
        math.isclose(inputs["robust_abs_ell_m"], 49228.988526505666, rel_tol=2.0e-13)
        and math.isclose(
            inputs["robust_positive_ell_m"], 44344.69058379586, rel_tol=2.0e-13
        )
        and math.isclose(
            inputs["neutron_star_ell_m"], 3473.408489247101, rel_tol=2.0e-13
        ),
        "the signed, positive and compact-target length coordinates reproduce",
    )

    running_map = {row["row_id"]: row for row in running}
    check(
        "VAL4925_10_running",
        len(running) == 4
        and all(bool_cell(row["passed"]) for row in running)
        and math.isclose(
            float(running_map["RG4925_GW250114"]["ln_q_over_mu"]),
            -90.03263789832708,
            rel_tol=2.0e-13,
        )
        and math.isclose(
            float(running_map["RG4925_GW250114"]["delta_a_plus_over_lP4"]),
            -1.323987922642225,
            rel_tol=2.0e-13,
        ),
        "the Planck-reference GS transfer reproduces in all four arenas",
    )
    check(
        "VAL4925_11_running_small",
        max(float(row["absolute_running_length_m"]) for row in running) < 1.8e-35
        and max(float(row["a_ratio_to_robust_GW_envelope"]) for row in running)
        < 2.0e-158,
        "the universal running is negligible relative to the observational envelope",
    )

    route_map = {row["route_id"]: row for row in routes}
    selected_routes = [row for row in routes if bool_cell(row["selected"])]
    check(
        "VAL4925_12_routes",
        len(routes) == 7
        and len(selected_routes) == 1
        and selected_routes[0]["route_id"] == "ROUTE4925_06_IR_Wilson"
        and route_map["ROUTE4925_03_asymptotic_safety"]["status"]
        == "RETAINED_RESEARCH_ROUTE_NOT_ADOPTED_BOUNDARY"
        and all(bool_cell(row["passed"]) for row in routes),
        "six boundary mechanisms are arbitrated and the one-Wilson EFT route is selected",
    )

    threshold_map = {row["species"]: row for row in thresholds}
    check(
        "VAL4925_13_threshold_basis",
        len(thresholds) == 3
        and [
            float(threshold_map[name]["I1_coefficient_ratio_to_real_scalar"])
            for name in ("real_scalar", "Dirac_fermion", "massive_vector")
        ]
        == [1.0, -4.0, 3.0]
        and all(float(row["parity_odd_threshold"]) == 0.0 for row in thresholds)
        and all(bool_cell(row["passed"]) for row in thresholds),
        "the spin-zero, Dirac and Proca Ricci-flat threshold ratios close",
    )
    check(
        "VAL4925_14_threshold_floors",
        math.isclose(
            float(
                threshold_map["real_scalar"][
                    "one_species_NS_one_percent_mass_floor_eV_no_cancellation"
                ]
            ),
            8.576671952007384e-52,
            rel_tol=2.0e-12,
        )
        and math.isclose(
            float(
                threshold_map["Dirac_fermion"][
                    "one_species_NS_one_percent_mass_floor_eV_no_cancellation"
                ]
            ),
            1.7153343904014768e-51,
            rel_tol=2.0e-12,
        ),
        "the no-cancellation compact mass floors scale with the threshold ratios",
    )

    bound_map = {row["bound_id"]: row for row in bounds}
    check(
        "VAL4925_15_bounds",
        len(bounds) == 4
        and all(bool_cell(row["passed"]) for row in bounds)
        and math.isclose(
            float(bound_map["WBOUND4925_00_robust_abs"]["ell_bound_m"]),
            49228.988526505666,
            rel_tol=2.0e-13,
        )
        and math.isclose(
            float(bound_map["WBOUND4925_01_positive"]["ell_bound_m"]),
            44344.69058379586,
            rel_tol=2.0e-13,
        ),
        "the signed and positive low-energy Wilson envelopes reproduce",
    )
    check(
        "VAL4925_16_compact_gap",
        math.isclose(
            float(bound_map["WBOUND4925_03_gap"]["coefficient_room_factor"]),
            40351.54847808737,
            rel_tol=2.0e-13,
        )
        and float(bound_map["WBOUND4925_03_gap"]["length_room_factor"]) > 14.0,
        "the current data-to-compact one-percent gap is explicit",
    )

    check(
        "VAL4925_17_induced",
        len(induced) == 5
        and all(bool_cell(row["passed"]) for row in induced)
        and all(bool_cell(row["natural_cW_equal_one_is_assumption"]) for row in induced)
        and all(not bool_cell(row["branch_is_parent_selected"]) for row in induced)
        and min(float(row["abs_cW_at_NS_one_percent_target"]) for row in induced)
        > 1.0e155,
        "the Newton-matched induced hierarchy is exact but remains conditional",
    )

    decision_map = {row["gate"]: row for row in decisions}
    expected_decisions = {
        "H_to_g_jacobian": "UNIT_MAGNITUDE_DERIVED_IN_4D",
        "Hghost_finite_split": "COLLAPSED_INTO_RENORMALIZED_WILSON",
        "two_loop_running": "DERIVED_RG_INVARIANT_TRANSFER",
        "boundary_zero_proof": "NOT_DERIVED",
        "asymptotic_safety_route": "EXTERNAL_CANDIDATE_NOT_ADOPTED",
        "heavy_threshold_basis": "SPIN_0_HALF_1_COEFFICIENTS_DERIVED",
        "I1_parameter_count": "ONE_SIGNED_IR_WILSON_INPUT",
        "current_Wilson_bound": "ROBUST_NONCLAIM_ENVELOPE_ACQUIRED",
        "induced_scale": "PLANCK_NATURAL_SAFETY_CONDITIONAL_NOT_PROOF",
        "weak_invariant_vacuum_GR": "RETAINED",
        "compact_vacuum_GR": "NOT_PROMOTED",
        "full_MTS_to_GR": "NOT_PROMOTED",
        "next_target": "THRESHOLD_SPECTRUM_AND_MOTION_SCALE",
    }
    check(
        "VAL4925_18_decisions",
        len(decisions) == len(expected_decisions)
        and all(bool_cell(row["passed"]) for row in decisions)
        and all(
            decision_map[gate]["status"] == status
            for gate, status in expected_decisions.items()
        )
        and decision_map["next_target"]["decision"] == NEXT_TARGET,
        "all theory gates and the next target agree",
    )

    checkpoint_path = POST / (
        "4925-Y5-R2FR-integrated-H-two-loop-renormalization-condition-"
        "and-finite-zeta-plus-boundary-owner-or-explicit-Wilson-input.md"
    )
    formal_path = FORMAL / "941-PPC4161-integrated-H-two-loop-Wilson-boundary.md"
    provenance_path = (
        POST / "source-intake" / "parent_coupling" / "4925" / "PROVENANCE.md"
    )
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    formal_note = formal_path.read_text(encoding="utf-8")
    provenance = provenance_path.read_text(encoding="utf-8")
    check(
        "VAL4925_19_documents",
        MARKER in checkpoint
        and "abs det[dH/dg]=1" in checkpoint
        and "49.228989 km" in checkpoint
        and "one signed parameter" in checkpoint
        and "No GitHub action" in checkpoint
        and FORMAL_MARKER in formal_note
        and "MTS_INTEGRATED_H_TWO_LOOP_WILSON_BOUNDARY_PROVENANCE_4925"
        in provenance
        and "valid_for_claim=false" in provenance,
        "checkpoint, formal summary and provenance are synchronized",
    )

    claims = read_csv(FORMAL / "02-claims-register.csv")
    claim_rows = [row for row in claims if row.get("claim_id") == "L-767"]
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    variable_rows = [row for row in variables if row.get("symbol") in VARIABLES]
    variable_sources_exist = all(
        all((ROOT / source).exists() for source in row["source_files"].split(";"))
        for row in variable_rows
    )
    equations = (FORMAL / "05-equation-register.md").read_text(encoding="utf-8")
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8")
    spine = (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    check(
        "VAL4925_20_registers",
        len(claim_rows) == 1
        and "one_signed_IR_Wilson_input" in claim_rows[0]["status"]
        and len(variable_rows) == len(VARIABLES)
        and {row["symbol"] for row in variable_rows} == VARIABLES
        and variable_sources_exist
        and "1.218 Integrated-H measure and one-Wilson matching" in equations
        and "169. A scheme split is not two physical Weyl-cubic parameters"
        in redteam
        and "PPC4161 checkpoint 4925" in spine
        and "Last checkpoint:" in resume
        and "4925-Y5-R2FR-integrated-H-two-loop" in resume
        and FORMAL_MARKER in resume,
        "claim, variables, equations, red-team, spine and resume agree",
    )

    local_sources = [row for row in sources if bool_cell(row["local_path_required"])]
    external_sources = [
        row for row in sources if not bool_cell(row["local_path_required"])
    ]
    check(
        "VAL4925_21_sources",
        len(sources) == 33
        and len(local_sources) == 28
        and len(external_sources) == 5
        and all(
            bool_cell(row["source_exists"])
            and bool_cell(row["marker_found"])
            and bool_cell(row["passed"])
            and len(row["sha256"]) == 64
            for row in local_sources
        )
        and all(
            row["source_path_or_url"].startswith("https://")
            and bool_cell(row["passed"])
            for row in external_sources
        ),
        "all local and external source records pass",
    )

    all_rows = [row for table in tables.values() for row in table]
    all_text = "\n".join(value for row in all_rows for value in row.values() if value)
    numeric_values: list[float] = []
    for row in all_rows:
        for value in row.values():
            try:
                numeric_values.append(float(value))
            except (TypeError, ValueError):
                pass
    check(
        "VAL4925_22_hygiene",
        all(not bool_cell(row["valid_for_claim"]) for row in all_rows)
        and "MISSING_" not in all_text
        and numeric_values
        and all(math.isfinite(value) for value in numeric_values)
        and all(
            compile_source(path)
            for path in (
                SCRIPTS / "Y5_R2FR_4925_integrated_H_two_loop_Wilson_boundary.py",
                SCRIPTS
                / "Y5_R2FR_4925_integrated_H_two_loop_Wilson_boundary_validation.py",
            )
        )
        and not (SCRIPTS / "__pycache__").exists(),
        "nonclaim, finite-number, compilation and cache hygiene pass",
    )

    rows.append(
        {
            "check_id": "VAL4925_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "all 4925 measure, one-Wilson, RG, threshold and bound checks pass",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def main() -> int:
    rows = validation_rows()
    write_csv(OUTPUT / "P8_Y5_BRR545_4925_VALIDATION.csv", rows)
    passed = all(row["status"] == "PASS" for row in rows)
    print(f"P8_Y5_BRR545_4925_VALIDATION_{'PASS' if passed else 'FAIL'}")
    print(f"checks={len(rows)} passed={sum(row['status'] == 'PASS' for row in rows)}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
