from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import Y5_R2FR_4915_single_functional_EH_source_residue as research


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
    "single_functional_metric_variation_and_normalization_invariant_source_"
    "residue_derived_G_calibrated_once_microscopic_matter_pullback_open_"
    "private_nonclaim"
)
VARIABLES = (
    "ParentFunctional4915_MTS",
    "PerturbationScale4915_MTS",
    "SourceResidueInvariant4915_MTS",
    "CanonicalGraviton4915_MTS",
    "HilbertSource4915_MTS",
    "SourceCoefficientGate4915_MTS",
    "PoyntingHilbert4915_MTS",
    "GOwnership4915_MTS",
    "MatterPullbackBridge4915_MTS",
)
EVIDENCE = (
    "P8_Y5_R2FR_4915_NORMALIZATION_INVARIANCE.csv",
    "P8_Y5_R2FR_4915_PARENT_VARIATION.csv",
    "P8_Y5_R2FR_4915_LIMIT_LADDER.csv",
    "P8_Y5_R2FR_4915_OWNERSHIP.csv",
    "P8_Y5_R2FR_4915_GATE_DECISION.csv",
    "P8_Y5_R2FR_4915_SOURCE_REGISTER.csv",
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


def compile_source(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except (OSError, SyntaxError, UnicodeError):
        return False
    return True


def bool_cell(value: str) -> bool:
    return value.strip().lower() == "true"


def validation_rows() -> list[dict[str, Any]]:
    def check(check_id: str, condition: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4914_VALIDATION.csv")
    normalization = read_csv(
        OUTPUT / "P8_Y5_R2FR_4915_NORMALIZATION_INVARIANCE.csv"
    )
    variation = read_csv(OUTPUT / "P8_Y5_R2FR_4915_PARENT_VARIATION.csv")
    limits = read_csv(OUTPUT / "P8_Y5_R2FR_4915_LIMIT_LADDER.csv")
    ownership = read_csv(OUTPUT / "P8_Y5_R2FR_4915_OWNERSHIP.csv")
    decisions = read_csv(OUTPUT / "P8_Y5_R2FR_4915_GATE_DECISION.csv")
    sources = read_csv(OUTPUT / "P8_Y5_R2FR_4915_SOURCE_REGISTER.csv")
    decision_map = {row["gate"]: row for row in decisions}
    ownership_map = {row["quantity"]: row for row in ownership}

    checkpoint_path = (
        POST
        / "4915-Y5-R2FR-parent-EH-residue-universal-source-coupling-and-measured-G-calibration-or-closure-demotion.md"
    )
    formal_path = (
        FORMAL
        / "931-PPC4161-single-functional-EH-source-residue-and-G-ownership.md"
    )
    provenance_path = (
        POST / "source-intake" / "parent_coupling" / "4915" / "PROVENANCE.md"
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
        if row.get("claim_id") == "L-757"
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
        SCRIPTS / "Y5_R2FR_4915_single_functional_EH_source_residue.py",
        SCRIPTS
        / "Y5_R2FR_4915_single_functional_EH_source_residue_validation.py",
    ]
    numeric_cells: list[float] = []
    for row in all_evidence_rows:
        for value in row.values():
            try:
                numeric_cells.append(float(value))
            except (TypeError, ValueError):
                pass

    rows = [
        check(
            "VAL4915_00_prior",
            prior[-1]["check_id"] == "VAL4914_OVERALL"
            and prior[-1]["status"] == "PASS",
            "4914 predecessor validation passes",
        ),
        check(
            "VAL4915_01_normalization",
            len(normalization) == 7
            and all(bool_cell(row["passed"]) for row in normalization),
            "arbitrary-scale projector vertex and propagator identities pass",
        ),
        check(
            "VAL4915_02_variation",
            len(variation) == 7
            and all(bool_cell(row["passed"]) for row in variation),
            "single-functional variation and soft universality pass",
        ),
        check(
            "VAL4915_03_limits",
            len(limits) == 8 and all(bool_cell(row["passed"]) for row in limits),
            "Newton exchange Bianchi Maxwell Poynting and PPN ladder passes",
        ),
        check(
            "VAL4915_04_single_parent",
            decision_map["single_parent_variation"]["status"] == "PASS",
            "metric equation and source come from one parent variation",
        ),
        check(
            "VAL4915_05_source_residue",
            decision_map["kinetic_source_normalization"]["status"] == "PASS",
            "kinetic residue and source vertices have one invariant coefficient",
        ),
        check(
            "VAL4915_06_no_extra_source",
            decision_map["independent_source_coefficient"]["status"] == "ABSENT",
            "no hidden source normalization is admitted",
        ),
        check(
            "VAL4915_07_G_owner",
            decision_map["measured_G_ownership"]["status"]
            == "ONE_GLOBAL_CALIBRATION"
            and ownership_map["renormalized M_R^2"]["status"]
            == "one_global_calibration",
            "4898 one-calibration ownership is preserved",
        ),
        check(
            "VAL4915_08_pullback_open",
            decision_map["microscopic_matter_pullback"]["status"]
            == "OPEN_PRIMITIVE_BRIDGE"
            and ownership_map["matter pullback S_matter[g(H),Phi]"]["status"]
            == "explicit_parent_clause_not_derived_from_strict_scalar_only_corpus",
            "microscopic matter pullback is not falsely promoted",
        ),
        check(
            "VAL4915_09_no_G_prediction",
            ownership_map["microscopic numerical prediction of G_N"]["status"]
            == "rank_deficient_open_not_claimed",
            "numerical G prediction remains open",
        ),
        check(
            "VAL4915_10_residual_zero",
            ownership_map["Gamma_MTS_res"]["status"]
            == "zero_preserved_after_4914",
            "failed C-cubed residual remains absent",
        ),
        check(
            "VAL4915_11_sources",
            len(sources) == 17
            and all(
                bool_cell(row["source_exists"])
                and bool_cell(row["marker_found"])
                and row["sha256"]
                for row in sources
            ),
            "all local source paths markers and hashes resolve",
        ),
        check(
            "VAL4915_12_documents",
            MARKER in checkpoint
            and research.FORMAL_MARKER in formal_note
            and "MTS_PARENT_COUPLING_PROVENANCE_4915" in provenance,
            "checkpoint formal note and provenance markers exist",
        ),
        check(
            "VAL4915_13_4875_repair",
            "Repair of the checkpoint-4875 notation" in checkpoint
            and "supersedes only its intermediate" in checkpoint
            and "NORM4915_06_4875_notation_repair"
            in {row["check_id"] for row in normalization},
            "historical mixed normalization is repaired without changing invariants",
        ),
        check(
            "VAL4915_14_claim",
            len(claims) == 1 and claims[0]["status"] == CLAIM_STATUS,
            "L-757 is unique and accurately scoped",
        ),
        check(
            "VAL4915_15_variables",
            len(variable_rows) == len(VARIABLES)
            and {row["symbol"] for row in variable_rows} == set(VARIABLES),
            "nine checkpoint variables are unique",
        ),
        check(
            "VAL4915_16_variable_sources",
            variable_sources_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4915_17_registers",
            "1.208 Single-functional EH source-residue theorem" in equations
            and "159. A correct exchange amplitude can hide a mixed graviton normalization"
            in redteam
            and "PPC4161 checkpoint 4915" in spine,
            "equation red-team and spine registers are updated",
        ),
        check(
            "VAL4915_18_resume",
            "4915-Y5-R2FR-parent-EH-residue" in resume
            and research.FORMAL_MARKER in resume
            and NEXT_TARGET in resume,
            "resume points from 4915 to the microscopic covariantization bridge",
        ),
        check(
            "VAL4915_19_csv",
            len(evidence_paths) == 6
            and all(path.exists() and read_csv(path) for path in evidence_paths),
            "six generated evidence CSVs parse",
        ),
        check(
            "VAL4915_20_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_evidence_rows
                for value in row.values()
            ),
            "generated evidence has no placeholder markers",
        ),
        check(
            "VAL4915_21_finite",
            all(math.isfinite(value) for value in numeric_cells),
            "all parsed numeric evidence cells are finite",
        ),
        check(
            "VAL4915_22_nonclaim",
            all(row.get("valid_for_claim") == "False" for row in all_evidence_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4915_23_scripts",
            all(compile_source(path) for path in scripts),
            "research and validation scripts compile",
        ),
        check(
            "VAL4915_24_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no scripts pycache exists",
        ),
        check(
            "VAL4915_25_next",
            NEXT_TARGET in checkpoint and not (POST / NEXT_TARGET).exists(),
            "4916 microscopic covariantization target is selected but not pre-created",
        ),
        check(
            "VAL4915_26_no_public_action",
            "No GitHub action or public claim is authorized." in checkpoint,
            "checkpoint remains local and private",
        ),
    ]
    rows.append(
        check(
            "VAL4915_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_SINGLE_FUNCTIONAL_EH_SOURCE_RESIDUE_4915_VALIDATED",
        )
    )
    return rows


def main() -> int:
    validation = validation_rows()
    write_csv(OUTPUT / "P8_Y5_BRR545_4915_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4915_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4915_VALIDATION_FAIL"
    )
    if not passed:
        for row in validation:
            if row["status"] != "PASS":
                print(row["check_id"], row["detail"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
