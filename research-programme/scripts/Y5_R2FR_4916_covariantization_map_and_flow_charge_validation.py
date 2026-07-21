from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import Y5_R2FR_4916_covariantization_map_and_flow_charge as research


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
    "explicit_integrated_H_covariantization_and_density_source_chain_derived_"
    "tree_flow_current_zero_selected_parent_minimal_map_not_symmetry_unique_"
    "radiative_reentry_open_private_nonclaim"
)
VARIABLES = (
    "CovariantizationFunctor4916_MTS",
    "DensityMetricMap4916_MTS",
    "HSourceChain4916_MTS",
    "TraceReverse4916_MTS",
    "ClosedBathLift4916_MTS",
    "GRParityMatterFunctor4916_MTS",
    "TreeFlowCurrent4916_MTS",
    "FlowReentryBasis4916_MTS",
    "MatterMapUniquenessGate4916_MTS",
    "PrimitiveBridgeOwnership4916_MTS",
)
EVIDENCE = (
    "P8_Y5_R2FR_4916_COVARIANTIZATION_MAP.csv",
    "P8_Y5_R2FR_4916_H_SOURCE_CHAIN.csv",
    "P8_Y5_R2FR_4916_OPERATOR_CLASSIFICATION.csv",
    "P8_Y5_R2FR_4916_FLOW_SILENCE_GATE.csv",
    "P8_Y5_R2FR_4916_OWNERSHIP.csv",
    "P8_Y5_R2FR_4916_GATE_DECISION.csv",
    "P8_Y5_R2FR_4916_SOURCE_REGISTER.csv",
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

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4915_VALIDATION.csv")
    covariantization = read_csv(
        OUTPUT / "P8_Y5_R2FR_4916_COVARIANTIZATION_MAP.csv"
    )
    h_source = read_csv(OUTPUT / "P8_Y5_R2FR_4916_H_SOURCE_CHAIN.csv")
    operators = read_csv(
        OUTPUT / "P8_Y5_R2FR_4916_OPERATOR_CLASSIFICATION.csv"
    )
    flow = read_csv(OUTPUT / "P8_Y5_R2FR_4916_FLOW_SILENCE_GATE.csv")
    ownership = read_csv(OUTPUT / "P8_Y5_R2FR_4916_OWNERSHIP.csv")
    decisions = read_csv(OUTPUT / "P8_Y5_R2FR_4916_GATE_DECISION.csv")
    sources = read_csv(OUTPUT / "P8_Y5_R2FR_4916_SOURCE_REGISTER.csv")
    decision_map = {row["gate"]: row for row in decisions}
    ownership_map = {row["object"]: row for row in ownership}

    checkpoint_path = (
        POST
        / "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md"
    )
    formal_path = (
        FORMAL / "932-PPC4161-covariantization-map-and-flow-charge-ownership.md"
    )
    provenance_path = (
        POST / "source-intake" / "parent_coupling" / "4916" / "PROVENANCE.md"
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
        if row.get("claim_id") == "L-758"
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
    all_evidence_rows = [
        row for path in evidence_paths for row in read_csv(path)
    ]
    scripts = [
        SCRIPTS / "Y5_R2FR_4916_covariantization_map_and_flow_charge.py",
        SCRIPTS
        / "Y5_R2FR_4916_covariantization_map_and_flow_charge_validation.py",
    ]
    numeric_cells: list[float] = []
    for row in all_evidence_rows:
        for value in row.values():
            try:
                numeric_cells.append(float(value))
            except (TypeError, ValueError):
                pass

    max_h_residual = max(float(row["residual"]) for row in h_source)
    rows = [
        check(
            "VAL4916_00_prior",
            prior[-1]["check_id"] == "VAL4915_OVERALL"
            and prior[-1]["status"] == "PASS",
            "4915 predecessor validation passes",
        ),
        check(
            "VAL4916_01_covariantization",
            len(covariantization) == 9
            and all(bool_cell(row["passed"]) for row in covariantization),
            "motion bath Higgs gauge fermion and coframe maps pass",
        ),
        check(
            "VAL4916_02_H_source",
            len(h_source) == 5
            and all(bool_cell(row["passed"]) for row in h_source)
            and max_h_residual < 2.0e-9,
            "density reconstruction Jacobian source chain and involution pass",
        ),
        check(
            "VAL4916_03_operators",
            len(operators) == 9
            and all(bool_cell(row["classification_passed"]) for row in operators)
            and all(not bool_cell(row["symmetry_unique_minimal_lift"]) for row in operators)
            and min(int(row["allowed_counterexample_count"]) for row in operators) >= 8,
            "symmetry-allowed counteroperator classification proves nonuniqueness",
        ),
        check(
            "VAL4916_04_flow",
            len(flow) == 8
            and all(bool_cell(row["passed"]) for row in flow)
            and all(not bool_cell(row["all_orders_claim"]) for row in flow),
            "tree flow silence is derived without an all-orders overclaim",
        ),
        check(
            "VAL4916_05_map_decision",
            decision_map["explicit_covariantization_map"]["status"]
            == "PASS_CONSTRUCTED",
            "explicit parent map is constructed",
        ),
        check(
            "VAL4916_06_source_decision",
            decision_map["H_source_chain"]["status"] == "PASS_EXACT",
            "H source chain is exact",
        ),
        check(
            "VAL4916_07_nonunique",
            decision_map["minimal_map_symmetry_uniqueness"]["status"]
            == "FAIL_COUNTEROPERATORS_EXIST",
            "minimal map is not falsely labelled symmetry-unique",
        ),
        check(
            "VAL4916_08_tree_zero",
            decision_map["tree_direct_flow_charge"]["status"]
            == "ZERO_DERIVED_SELECTED_PARENT"
            and ownership_map["tree direct-flow matter current"]["status"]
            == "DERIVED_ZERO_ON_SELECTED_PARENT",
            "tree direct-flow current is exactly scoped",
        ),
        check(
            "VAL4916_09_all_orders_open",
            decision_map["all_orders_direct_flow_charge"]["status"]
            == "OPEN_CALCULATE_OR_BOUND"
            and ownership_map["all-orders direct-flow current"]["status"]
            == "OPEN_REENTRY_BASIS_RETAINED",
            "radiative and state re-entry remains open",
        ),
        check(
            "VAL4916_10_primitive_owner",
            decision_map["matter_pullback_ownership"]["status"]
            == "PRIMITIVE_GR_PARITY_FUNCTOR_FROZEN"
            and ownership_map["GR-parity Standard-Model covariantization"]["status"]
            == "PRIMITIVE_PARENT_COUPLING_ARCHITECTURE",
            "matter pullback is owned explicitly rather than smuggled as derived",
        ),
        check(
            "VAL4916_11_scalar_only_rejected",
            ownership_map["strict scalar-only emergence claim"]["status"]
            == "REJECTED",
            "rejected scalar-only route is not revived",
        ),
        check(
            "VAL4916_12_sources",
            len(sources) == 21
            and all(
                bool_cell(row["source_exists"])
                and bool_cell(row["marker_found"])
                and row["sha256"]
                for row in sources
            ),
            "all local source paths markers and hashes resolve",
        ),
        check(
            "VAL4916_13_documents",
            MARKER in checkpoint
            and research.FORMAL_MARKER in formal_note
            and "MTS_COVARIANTIZATION_PROVENANCE_4916" in provenance,
            "checkpoint formal note and provenance markers exist",
        ),
        check(
            "VAL4916_14_document_integrity",
            "After choosing a bath state and integrating the bath" in checkpoint
            and "delta\\mathcal Hmu" not in checkpoint
            and "## 4. Exact `H`-source chain" in checkpoint,
            "checkpoint contains the complete bath and source derivations",
        ),
        check(
            "VAL4916_15_claim",
            len(claims) == 1 and claims[0]["status"] == CLAIM_STATUS,
            "L-758 is unique and accurately scoped",
        ),
        check(
            "VAL4916_16_variables",
            len(variable_rows) == len(VARIABLES)
            and {row["symbol"] for row in variable_rows} == set(VARIABLES),
            "ten checkpoint variables are unique",
        ),
        check(
            "VAL4916_17_variable_sources",
            variable_sources_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4916_18_registers",
            "1.209 Integrated-H covariantization and density-source chain"
            in equations
            and "160. Minimal covariantization is a construction, not a uniqueness theorem"
            in redteam
            and "PPC4161 checkpoint 4916" in spine,
            "equation red-team and spine registers are updated",
        ),
        check(
            "VAL4916_19_resume",
            "4916-Y5-R2FR-covariantization-map" in resume
            and research.FORMAL_MARKER in resume
            and NEXT_TARGET in resume,
            "resume points from 4916 to radiative matching or bounds",
        ),
        check(
            "VAL4916_20_csv",
            len(evidence_paths) == 7
            and all(path.exists() and read_csv(path) for path in evidence_paths),
            "seven generated evidence CSVs parse",
        ),
        check(
            "VAL4916_21_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_evidence_rows
                for value in row.values()
            ),
            "generated evidence has no placeholder markers",
        ),
        check(
            "VAL4916_22_finite",
            all(math.isfinite(value) for value in numeric_cells),
            "all parsed numeric evidence cells are finite",
        ),
        check(
            "VAL4916_23_nonclaim",
            all(row.get("valid_for_claim") == "False" for row in all_evidence_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4916_24_scripts",
            all(compile_source(path) for path in scripts),
            "research and validation scripts compile",
        ),
        check(
            "VAL4916_25_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no scripts pycache exists",
        ),
        check(
            "VAL4916_26_next",
            NEXT_TARGET in checkpoint and not (POST / NEXT_TARGET).exists(),
            "4917 radiative matching target is selected but not pre-created",
        ),
        check(
            "VAL4916_27_no_public_action",
            "No GitHub action or public claim is authorized." in checkpoint,
            "checkpoint remains local and private",
        ),
    ]
    rows.append(
        check(
            "VAL4916_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_COVARIANTIZATION_MAP_FLOW_CHARGE_4916_VALIDATED",
        )
    )
    return rows


def main() -> int:
    validation = validation_rows()
    write_csv(OUTPUT / "P8_Y5_BRR545_4916_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4916_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4916_VALIDATION_FAIL"
    )
    if not passed:
        for row in validation:
            if row["status"] != "PASS":
                print(row["check_id"], row["detail"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
