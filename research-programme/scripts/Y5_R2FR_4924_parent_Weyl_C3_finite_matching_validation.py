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
MARKER = "MTS_PARENT_WEYL_C3_FINITE_MATCHING_4924"
FORMAL_MARKER = "PPC4161_PARENT_WEYL_C3_FINITE_MATCHING_4924"
NEXT_TARGET = (
    "4925-Y5-R2FR-integrated-H-two-loop-renormalization-condition-"
    "and-finite-zeta-plus-boundary-owner-or-explicit-Wilson-input.md"
)
VARIABLES = {
    "MotionScalarC3Threshold4924_MTS",
    "MotionScalarC3Sign4924_MTS",
    "MotionScalarC6Coefficient4924_MTS",
    "MotionScalarGapScale4924_MTS",
    "ScalarC3Multiplicity4924_MTS",
    "GSI1Running4924_MTS",
    "WeylC3Boundary4924_MTS",
    "WeylC3MatchingLedger4924_MTS",
    "ScalarCompactScaleGate4924_MTS",
    "MinimalC3MatchingBranch4924_MTS",
    "VacuumGRDomain4924_MTS",
}
EVIDENCE = (
    "P8_Y5_R2FR_4924_PARENT_ACTION_AUDIT.csv",
    "P8_Y5_R2FR_4924_MASS_GAP_COEFFICIENT.csv",
    "P8_Y5_R2FR_4924_SCALAR_THRESHOLD.csv",
    "P8_Y5_R2FR_4924_GS_CANONICAL_RUNNING.csv",
    "P8_Y5_R2FR_4924_PHYSICAL_SCALE_GATES.csv",
    "P8_Y5_R2FR_4924_TOTAL_MATCHING_LEDGER.csv",
    "P8_Y5_R2FR_4924_COUNTERTERM_THEOREM.csv",
    "P8_Y5_R2FR_4924_GATE_DECISION.csv",
    "P8_Y5_R2FR_4924_SOURCE_REGISTER.csv",
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
    path = SCRIPTS / "Y5_R2FR_4924_parent_Weyl_C3_finite_matching.py"
    specification = importlib.util.spec_from_file_location("research_4924", path)
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load checkpoint 4924 research module")
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
    mass_gap = tables[EVIDENCE[1]]
    scalar = tables[EVIDENCE[2]]
    gs = tables[EVIDENCE[3]]
    physical = tables[EVIDENCE[4]]
    ledger = tables[EVIDENCE[5]]
    counterterm = tables[EVIDENCE[6]]
    decisions = tables[EVIDENCE[7]]
    sources = tables[EVIDENCE[8]]
    mass_map = {row["profile"]: row for row in mass_gap}
    scalar_map = {row["threshold_id"]: row for row in scalar}
    gs_map = {row["running_id"]: row for row in gs}
    ledger_map = {row["term_id"]: row for row in ledger}
    counterterm_map = {row["clause_id"]: row for row in counterterm}
    decision_map = {row["gate"]: row for row in decisions}

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4923_VALIDATION.csv")
    check(
        "VAL4924_00_prior",
        prior[-1]["check_id"] == "VAL4923_OVERALL"
        and prior[-1]["status"] == "PASS",
        "checkpoint 4923 validation passed",
    )
    check(
        "VAL4924_01_evidence",
        all(path.exists() and read_csv(path) for path in evidence_paths),
        "all nine evidence files exist and parse",
    )
    check(
        "VAL4924_02_parent_audit",
        len(parent) == 6
        and all(bool_cell(row["passed"]) for row in parent)
        and {row["status"] for row in parent}
        >= {
            "DETERMINANT_THRESHOLD_OWNER_CLOSED_PER_REAL_POLE",
            "SIX_DERIVATIVE_COUNTERTERM_REQUIRED",
            "NO_DIMENSION_SIX_PREDICTION_FROM_G",
        },
        "determinant, counterterm and measured-G ownership are separated",
    )

    inputs = research.mass_gap_inputs()
    check(
        "VAL4924_03_mass_inputs",
        abs(inputs["central"] - 1.0212886943350583) < 1.0e-14
        and abs(inputs["union_min"] - 0.7278049207982136) < 1.0e-14
        and abs(inputs["union_max"] - 1.189451317368038) < 1.0e-14,
        "the archived c_m pilot and conservative union reproduce",
    )
    check(
        "VAL4924_04_mass_rows",
        len(mass_gap) == 5
        and all(bool_cell(row["passed"]) for row in mass_gap)
        and all(not bool_cell(row["coefficient_promoted"]) for row in mass_gap),
        "five c_m sensitivity rows remain explicitly nonpromoted",
    )
    central_c6 = research.scalar_c6_lambda(inputs["central"])
    low_c6 = research.scalar_c6_lambda(inputs["union_max"])
    high_c6 = research.scalar_c6_lambda(inputs["union_min"])
    check(
        "VAL4924_05_c6_transform",
        abs(central_c6 - 2.007712100686747e-7) < 1.0e-20
        and abs(low_c6 - 1.480147997106536e-7) < 1.0e-20
        and abs(high_c6 - 3.9533795365551735e-7) < 1.0e-20
        and abs(
            float(
                mass_map["central_constant_fit"][
                    "c6_lambda_coefficient_per_real_pole"
                ]
            )
            - central_c6
        )
        < 1.0e-20,
        "the exact c_m-to-c6 transformation reproduces",
    )
    check(
        "VAL4924_06_scalar_rows",
        len(scalar) == 3
        and all(bool_cell(row["passed"]) for row in scalar)
        and all(row["sign"] == "positive" for row in scalar)
        and all(float(row["parity_odd_threshold"]) == 0.0 for row in scalar),
        "one-, two- and three-pole scalar thresholds have positive even and zero odd signs",
    )
    check(
        "VAL4924_07_scalar_multiplicity",
        abs(
            float(scalar_map["SCALAR4924_N2"]["c6_lambda_central"])
            / float(scalar_map["SCALAR4924_N1"]["c6_lambda_central"])
            - 2.0
        )
        < 1.0e-13
        and abs(
            float(scalar_map["SCALAR4924_N3"]["c6_lambda_central"])
            / float(scalar_map["SCALAR4924_N1"]["c6_lambda_central"])
            - 3.0
        )
        < 1.0e-13,
        "threshold coefficients scale linearly with physical real-pole count",
    )
    check(
        "VAL4924_08_canonical_normalization",
        abs(
            research.scalar_a_mu2_over_G(inputs["central"])
            - 16.0 * math.pi * central_c6
        )
        < 1.0e-18,
        "a_plus=16 pi G zeta_plus normalization is exact",
    )

    expected_gs = 209.0 / (1440.0 * math.pi**2)
    expected_ell = expected_gs**0.25
    check(
        "VAL4924_09_GS_rows",
        len(gs) == 2
        and all(bool_cell(row["passed"]) for row in gs)
        and abs(float(gs_map["GS4924_log_1"]["delta_a_plus_over_lP4"]) - expected_gs)
        < 1.0e-15
        and abs(float(gs_map["GS4924_log_1"]["ell_plus_over_lP"]) - expected_ell)
        < 1.0e-15,
        "the GS pole is mapped directly into the canonical I1 coordinate",
    )
    check(
        "VAL4924_10_GS_correction",
        abs(expected_ell - 0.3482338723051975) < 1.0e-15
        and all(not bool_cell(row["old_4921_beta1_length_reused"]) for row in gs),
        "the superseded 0.603159 l_P beta1 length is not reused",
    )
    check(
        "VAL4924_11_GS_log_scaling",
        abs(
            float(gs_map["GS4924_log_100"]["delta_a_plus_over_lP4"])
            / float(gs_map["GS4924_log_1"]["delta_a_plus_over_lP4"])
            - 100.0
        )
        < 1.0e-12
        and abs(
            float(gs_map["GS4924_log_100"]["ell_plus_over_lP"])
            / float(gs_map["GS4924_log_1"]["ell_plus_over_lP"])
            - 100.0**0.25
        )
        < 1.0e-12,
        "the running coefficient and canonical length have the correct log scaling",
    )

    check(
        "VAL4924_12_physical_rows",
        len(physical) == 12
        and all(bool_cell(row["passed"]) for row in physical)
        and all(not bool_cell(row["current_mu_value_owned"]) for row in physical)
        and all(not bool_cell(row["gate_closed"]) for row in physical),
        "four arenas and three pole multiplicities produce twelve conditional rows",
    )
    one_pole = {
        row["gate_id"]: row
        for row in physical
        if int(row["real_scalar_poles"]) == 1
    }
    expected_floors = {
        "GW250114_positive_robust": 5.261956627570885e-54,
        "GW170608_positive_published": 7.827661629024919e-54,
        "BH10_one_percent": 4.1095515411299444e-52,
        "NS14_one_percent": 8.576671952007384e-52,
    }
    check(
        "VAL4924_13_mass_floors",
        all(
            math.isclose(
                float(one_pole[gate]["m_gap_floor_eV"]),
                expected,
                rel_tol=2.0e-12,
            )
            for gate, expected in expected_floors.items()
        ),
        "all four one-pole physical gap floors independently reproduce",
    )
    check(
        "VAL4924_14_mu_floor",
        math.isclose(
            float(
                one_pole["NS14_one_percent"][
                    "mu_floor_eV_guaranteed_over_cm_union"
                ]
            ),
            1.1784300582360717e-51,
            rel_tol=2.0e-12,
        ),
        "the conservative one-pole neutron-star motion-scale floor reproduces",
    )
    check(
        "VAL4924_15_floor_multiplicity",
        all(
            math.isclose(
                float(
                    next(
                        row
                        for row in physical
                        if row["gate_id"] == gate
                        and int(row["real_scalar_poles"]) == 3
                    )["m_gap_floor_eV"]
                )
                / float(one_pole[gate]["m_gap_floor_eV"]),
                math.sqrt(3.0),
                rel_tol=1.0e-12,
            )
            for gate in expected_floors
        ),
        "physical gap floors scale as sqrt(N_real)",
    )

    check(
        "VAL4924_16_ledger",
        len(ledger) == 7
        and all(bool_cell(row["passed"]) for row in ledger)
        and ledger_map["MATCH4924_00_boundary"]["status"]
        == "FINITE_BOUNDARY_NOT_OWNED"
        and ledger_map["MATCH4924_01_motion_scalar"]["status"]
        == "DERIVED_PER_POLE_CONDITIONAL_ON_GAP_AND_COUNT"
        and ledger_map["MATCH4924_06_total"]["status"]
        == "TOTAL_MAGNITUDE_AND_SIGN_NOT_DERIVED",
        "the matching ledger separates derived, selected and open terms",
    )
    check(
        "VAL4924_17_counterterm",
        len(counterterm) == 7
        and all(bool_cell(row["passed"]) for row in counterterm)
        and counterterm_map["CT4924_02_quantum_gravity"]["status"]
        == "COUNTERTERM_MANDATORY"
        and counterterm_map["CT4924_05_current_parent"]["status"]
        == "FINITE_BOUNDARY_OBSTRUCTION_PROVED"
        and counterterm_map["CT4924_06_minimal_branch"]["status"]
        == "EXPLICIT_CLOSURE_BRANCH_NOT_PARENT_THEOREM",
        "the finite-boundary obstruction and minimal closure distinction are explicit",
    )

    expected_decisions = {
        "motion_scalar_finite_threshold": "DERIVED_PER_HEALTHY_REAL_POLE",
        "motion_scalar_sign": "POSITIVE_DERIVED",
        "mass_gap_constant": "PILOT_NOT_PROMOTED",
        "interacting_residual": "NO_NONZERO_VALUE_PROMOTED",
        "GS_running": "DERIVED_CANONICAL_I1_AND_NEGLIGIBLE",
        "finite_boundary": "REQUIRED_NOT_OWNED",
        "scalar_compact_scale": "EXACT_CONDITIONAL_FLOOR",
        "total_zeta_plus": "NOT_DERIVED",
        "weak_invariant_vacuum_GR": "RETAINED",
        "compact_vacuum_and_matter_GR": "NOT_PROMOTED_TOTAL",
        "full_MTS_to_GR": "NOT_PROMOTED",
        "next_target": "UV_BOUNDARY_OWNER",
    }
    check(
        "VAL4924_18_decisions",
        len(decisions) == len(expected_decisions)
        and all(bool_cell(row["passed"]) for row in decisions)
        and all(
            decision_map[gate]["status"] == status
            for gate, status in expected_decisions.items()
        )
        and decision_map["next_target"]["decision"] == NEXT_TARGET,
        "all gate states and the UV-boundary next target agree",
    )

    checkpoint_path = POST / (
        "4924-Y5-R2FR-renormalized-parent-Weyl-cubic-finite-matching-"
        "sign-and-scale-from-motion-scalar-determinant-or-explicit-"
        "counterterm-boundary.md"
    )
    formal_path = FORMAL / "940-PPC4161-parent-Weyl-C3-finite-matching.md"
    provenance_path = (
        POST / "source-intake" / "parent_coupling" / "4924" / "PROVENANCE.md"
    )
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    formal_note = formal_path.read_text(encoding="utf-8")
    provenance = provenance_path.read_text(encoding="utf-8")
    check(
        "VAL4924_19_documents",
        MARKER in checkpoint
        and "2.0077121007e-7" in checkpoint
        and "0.3482338723 l_P" in checkpoint
        and "1.17843e-51 eV" in checkpoint
        and "No GitHub action" in checkpoint
        and FORMAL_MARKER in formal_note
        and "MTS_PARENT_WEYL_C3_FINITE_MATCHING_PROVENANCE_4924"
        in provenance
        and "Every generated CSV row is valid_for_claim=false" in provenance,
        "checkpoint, formal summary and provenance are synchronized",
    )

    claims = read_csv(FORMAL / "02-claims-register.csv")
    claim_rows = [row for row in claims if row.get("claim_id") == "L-766"]
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    variable_rows = [
        row for row in variables if row.get("symbol") in VARIABLES
    ]
    variable_sources_exist = all(
        all((ROOT / source).exists() for source in row["source_files"].split(";"))
        for row in variable_rows
    )
    equations = (FORMAL / "05-equation-register.md").read_text(encoding="utf-8")
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8")
    spine = (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    check(
        "VAL4924_20_registers",
        len(claim_rows) == 1
        and "total_zeta_plus_sign_and_value_not_derived" in claim_rows[0]["status"]
        and len(variable_rows) == len(VARIABLES)
        and {row["symbol"] for row in variable_rows} == VARIABLES
        and variable_sources_exist
        and "1.217 Parent Weyl-cubic finite matching" in equations
        and "168. A calculable scalar threshold is not the total finite Weyl-cubic coefficient"
        in redteam
        and "PPC4161 checkpoint 4924" in spine
        and "Last checkpoint:" in resume
        and "4924-Y5-R2FR-renormalized-parent-Weyl-cubic" in resume
        and FORMAL_MARKER in resume,
        "claim, variables, equations, red-team, spine and resume agree",
    )

    local_sources = [
        row for row in sources if bool_cell(row["local_path_required"])
    ]
    external_sources = [
        row for row in sources if not bool_cell(row["local_path_required"])
    ]
    check(
        "VAL4924_21_sources",
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
    all_text = "\n".join(
        value for row in all_rows for value in row.values() if value
    )
    numeric_values: list[float] = []
    for row in all_rows:
        for value in row.values():
            try:
                numeric_values.append(float(value))
            except (TypeError, ValueError):
                pass
    check(
        "VAL4924_22_hygiene",
        all(not bool_cell(row["valid_for_claim"]) for row in all_rows)
        and "MISSING_" not in all_text
        and numeric_values
        and all(math.isfinite(value) for value in numeric_values)
        and all(
            compile_source(path)
            for path in (
                SCRIPTS / "Y5_R2FR_4924_parent_Weyl_C3_finite_matching.py",
                SCRIPTS
                / "Y5_R2FR_4924_parent_Weyl_C3_finite_matching_validation.py",
            )
        )
        and not (SCRIPTS / "__pycache__").exists(),
        "nonclaim, finite-number, compilation and cache hygiene pass",
    )

    rows.append(
        {
            "check_id": "VAL4924_OVERALL",
            "status": (
                "PASS"
                if all(row["status"] == "PASS" for row in rows)
                else "FAIL"
            ),
            "detail": "all 4924 finite-threshold, running, scale and counterterm checks pass",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def main() -> int:
    rows = validation_rows()
    write_csv(OUTPUT / "P8_Y5_BRR545_4924_VALIDATION.csv", rows)
    passed = all(row["status"] == "PASS" for row in rows)
    print(f"P8_Y5_BRR545_4924_VALIDATION_{'PASS' if passed else 'FAIL'}")
    print(f"checks={len(rows)} passed={sum(row['status'] == 'PASS' for row in rows)}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
