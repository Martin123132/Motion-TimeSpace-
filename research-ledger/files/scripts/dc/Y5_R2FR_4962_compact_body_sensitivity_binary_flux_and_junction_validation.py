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
SOURCE = POST / "source-intake" / "functional_rg" / "4962"
OUTPUT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_4962_VALIDATION.csv"
)

MAIN_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_4962_compact_body_sensitivity_binary_flux_and_junction.py"
)
RESULT_JSON = SOURCE / "compact_body_matching_results.json"
SENSITIVITY_CSV = SOURCE / "compact_body_sensitivity_and_no_dipole.csv"
JUNCTION_CSV = SOURCE / "junction_and_worldline_matching.csv"
RESIDUE_CSV = SOURCE / "conservative_radiative_residue_match.csv"
EOS_CSV = SOURCE / "realistic_EOS_scalar_stability_transfer.csv"
BOUNDARY_CSV = SOURCE / "strong_field_residual_boundary.csv"
DECISION_CSV = SOURCE / "compact_body_strong_GR_decision.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"

CHECKPOINT = (
    POST
    / "4962-Y5-R2FR-compact-body-sensitivity-binary-flux-and-junction-matching-or-strong-GR-residual-boundary.md"
)
FORMAL_NOTE = (
    FORMAL
    / "978-PPC4161-compact-body-sensitivity-binary-flux-and-strong-GR-boundary.md"
)
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
LOCAL_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

MARKER = "MTS_4962_COMPACT_BODY_SENSITIVITY_FLUX_JUNCTION"
FORMAL_MARKER = "PPC4161_COMPACT_BODY_FLUX_JUNCTION_4962"

HASH_LOCKS = {
    MAIN_SCRIPT: "b468ac172ea5f9eed7dd5c3d40ad381f12a8519983c7cbc514e77475fcf73fff",
    RESULT_JSON: "89e121d767673699ff8c6a34590f40c2b819274952992e1712b5c1ffe2eb3a5e",
    SENSITIVITY_CSV: "e7c3fbefdc369b0493420d7bdc7318b060866981a85e7c1b845dfba4e1ba9717",
    JUNCTION_CSV: "09e7c7c2a3d2212558f1484bc7545efa80df38db5ad28b44f7736a230196d9e8",
    RESIDUE_CSV: "bf5bd28bcaf97be0a53bc9c93cd9cb7c60a0d76eb86a7cb22d3234a14a710664",
    EOS_CSV: "df86b26581b523dcbfa0936c2af65f5d6e10ca4c5d75ac0bbc1b1196fa26a179",
    BOUNDARY_CSV: "ae9b0ff97a521745ae56b7425235a843e38e41d9d796a5e7adbed12f650d446e",
    DECISION_CSV: "6aecadfd090dad8cc09394998a5dfc69d9fbf5d9011f2c214a48f33c053535b9",
    PROVENANCE: "0cdfb608cffcbe4c633f2010e6d504ac1a12c750d336fb7d90c05295e864ed0b",
    CHECKPOINT: "93c88dd74a719106c998399a4f51bf78f44ed679ff19d3d570c8f3408d2c9134",
    FORMAL_NOTE: "6ee19d3caabc6c63c8b87e82e1b123ec9f18e41edc31714d937a15255437b864",
    CLAIMS: "9f2182725fdd7b4f27b434ed3ca5d4e780ce8d86e57fba0bfd88f160e1012b4d",
    VARIABLES: "6f0aaa9e6e2fe9e6252a33cfa95378e4405a5edc00774150a4cee38acc395975",
    EQUATIONS: "07688cceeea5692175d5f6f08bb016b307c0a142079f2fdce2cb56a42013d6cd",
    RED_TEAM: "c93b6dcf24cadc25442dea19e754fbcf34980580b7385b2a94c3db634ee6a6c6",
    SPINE: "61035bf8fef27c5910bc79f3f3b1d5d2d20401fffc06cfdca455814f02cce34c",
    RESUME: "4f77237cc1a13f0ec5223f15de6a6193318cc0662be884de2e6ea01b9cbb9aad",
    LOCAL_SPINE: "46fd99fc5d6b430d373b24a19db096c667a43756b3e5ec13e63af07504eda646",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def truth(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def close(actual: float, expected: float, tolerance: float = 1.0e-12) -> bool:
    return math.isclose(
        actual, expected, rel_tol=tolerance, abs_tol=1.0e-300
    )


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
            "checkpoint_marker": MARKER,
        }
    )


def main() -> int:
    checks: list[dict[str, Any]] = []

    missing = [str(path) for path in HASH_LOCKS if not path.exists()]
    add(
        checks,
        "VAL4962_01_paths",
        "all hash-locked artifacts exist",
        [],
        missing,
        not missing,
    )

    bad_hashes = {
        str(path): {"expected": expected, "actual": digest(path)}
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(
        checks,
        "VAL4962_02_hashes",
        "research and documentation hashes match",
        {},
        bad_hashes,
        not bad_hashes,
    )

    compile_errors: list[str] = []
    for path in (MAIN_SCRIPT, Path(__file__).resolve()):
        try:
            compile(text(path), str(path), "exec")
        except Exception as error:
            compile_errors.append(f"{path.name}: {error}")
    add(
        checks,
        "VAL4962_03_compile",
        "research and validation scripts compile in memory",
        [],
        compile_errors,
        not compile_errors,
    )

    result = json.loads(text(RESULT_JSON))
    add(
        checks,
        "VAL4962_04_marker",
        "result marker",
        MARKER,
        result.get("marker"),
        result.get("marker") == MARKER,
    )

    failed_internal = [
        name for name, passed in result["checks"].items() if not passed
    ]
    add(
        checks,
        "VAL4962_05_internal",
        "all 15 research checks pass",
        {"count": 15, "failed": []},
        {"count": len(result["checks"]), "failed": failed_internal},
        len(result["checks"]) == 15 and not failed_internal,
    )

    source_hashes = result["source_hashes"]
    failed_clauses = [
        name
        for name, passed in result["source_clause_checks"].items()
        if not passed
    ]
    add(
        checks,
        "VAL4962_06_sources",
        "18 source hashes and seven source clauses pass",
        {"hashes": 18, "clauses": 7, "failed": []},
        {
            "hashes": len(source_hashes),
            "clauses": len(result["source_clause_checks"]),
            "failed": failed_clauses,
        },
        len(source_hashes) == 18
        and len(result["source_clause_checks"]) == 7
        and not failed_clauses
        and all(
            len(value) == 64
            and all(character in "0123456789abcdef" for character in value)
            for value in source_hashes.values()
        ),
    )

    tables = {
        "sensitivity": read_csv(SENSITIVITY_CSV),
        "junction": read_csv(JUNCTION_CSV),
        "residue": read_csv(RESIDUE_CSV),
        "EOS": read_csv(EOS_CSV),
        "boundary": read_csv(BOUNDARY_CSV),
        "decision": read_csv(DECISION_CSV),
    }
    counts = {name: len(rows) for name, rows in tables.items()}
    expected_counts = {
        "sensitivity": 7,
        "junction": 6,
        "residue": 7,
        "EOS": 9,
        "boundary": 7,
        "decision": 6,
    }
    add(
        checks,
        "VAL4962_07_counts",
        "generated table row counts",
        expected_counts,
        counts,
        counts == expected_counts,
    )

    malformed = {
        f"{table_name}:{row_index}": row
        for table_name, rows in tables.items()
        for row_index, row in enumerate(rows)
        if None in row or any(value is None for value in row.values())
    }
    add(
        checks,
        "VAL4962_08_csv_shape",
        "all generated CSV rows parse without overflow",
        {},
        malformed,
        not malformed,
    )

    claim_errors = [
        f"{table_name}:{row_index}"
        for table_name, rows in tables.items()
        for row_index, row in enumerate(rows)
        if row.get("checkpoint_marker") != MARKER
        or truth(row.get("valid_for_full_MTS_claim"))
    ]
    add(
        checks,
        "VAL4962_09_claim_flags",
        "all rows carry marker and full-MTS false",
        [],
        claim_errors,
        not claim_errors,
    )

    sensitivity = {row["gate_id"]: row for row in tables["sensitivity"]}
    sensitivity_expected = {
        "SENS4962_01_first_sensitivity": "alpha_A=0",
        "SENS4962_02_scalar_charge": "Q_A=0",
        "SENS4962_03_binary_dipole": "(alpha_A-alpha_B)^2=0",
        "SENS4962_04_vector_charge": "no independent vector field or vector pole",
    }
    sensitivity_bad = {
        gate_id: sensitivity.get(gate_id, {}).get("equation")
        for gate_id, fragment in sensitivity_expected.items()
        if gate_id not in sensitivity
        or fragment not in sensitivity[gate_id]["equation"]
        or not truth(sensitivity[gate_id]["passed"])
    }
    add(
        checks,
        "VAL4962_10_sensitivity",
        "zero scalar sensitivity charge dipole and vector-pole gates",
        {},
        sensitivity_bad,
        not sensitivity_bad,
    )

    eos = tables["EOS"]
    max_density = max(float(row["central_density_kg_m3"]) for row in eos)
    max_ratio = max(float(row["central_to_critical_ratio"]) for row in eos)
    min_orders = min(float(row["orders_below_instability"]) for row in eos)
    eos_ids = sorted({row["eos_id"] for row in eos})
    eos_pass = all(
        truth(row["passed"])
        and truth(row["stable_branch"])
        and truth(row["valid_for_declared_parent_branch"])
        for row in eos
    )
    add(
        checks,
        "VAL4962_11_EOS",
        "nine realistic EOS rows reproduce the stability margin",
        {
            "eos": ["BSK24", "DD2", "SLY4"],
            "max_density": 2.2800188119234442e18,
            "max_ratio": 5.3697748471940454e-18,
            "min_orders_gt": 17.0,
            "pass": True,
        },
        {
            "eos": eos_ids,
            "max_density": max_density,
            "max_ratio": max_ratio,
            "min_orders": min_orders,
            "pass": eos_pass,
        },
        eos_ids == ["BSK24", "DD2", "SLY4"]
        and close(max_density, 2.2800188119234442e18)
        and close(max_ratio, 5.3697748471940454e-18)
        and min_orders > 17.0
        and eos_pass,
    )

    residue = {row["gate_id"]: row for row in tables["residue"]}
    residue_bad = [
        gate_id
        for gate_id, row in residue.items()
        if truth(row["new_independent_calibration"])
        or not truth(row["passed"])
    ]
    required_residue = {
        "RAD4962_00_conservative",
        "RAD4962_02_wave_flux",
        "RAD4962_03_quadrupole",
        "RAD4962_06_normalization",
    }
    add(
        checks,
        "VAL4962_12_residue",
        "same conservative-radiative residue and no new calibration",
        {"required": sorted(required_residue), "bad": []},
        {"required": sorted(residue), "bad": residue_bad},
        required_residue.issubset(residue) and not residue_bad,
    )

    junction = {row["gate_id"]: row for row in tables["junction"]}
    required_junction = {
        "MATCH4962_01_metric_shell",
        "MATCH4962_02_metric_no_shell",
        "MATCH4962_03_scalar",
        "MATCH4962_04_EM",
    }
    junction_bad = [
        gate_id
        for gate_id in required_junction
        if gate_id not in junction or not truth(junction[gate_id]["passed"])
    ]
    add(
        checks,
        "VAL4962_13_junction",
        "metric scalar and electromagnetic junction gates pass",
        [],
        junction_bad,
        not junction_bad,
    )

    boundary_ids = {row["residual_id"] for row in tables["boundary"]}
    expected_boundary = {
        "STRONG4962_00_C3",
        "STRONG4962_01_R2_C2",
        "STRONG4962_02_scalar_nonlinear",
        "STRONG4962_03_tidal",
        "STRONG4962_04_CFF",
        "STRONG4962_05_state",
        "STRONG4962_06_parent",
    }
    add(
        checks,
        "VAL4962_14_boundary",
        "finite strong-field residual classes are complete",
        sorted(expected_boundary),
        sorted(boundary_ids),
        boundary_ids == expected_boundary,
    )

    decisions = {
        row["decision_id"]: row["decision"] for row in tables["decision"]
    }
    expected_decisions = {
        "DEC4962_00_two_derivative_compact": "YES_CONDITIONALLY",
        "DEC4962_01_scalar_dipole": "NO_ON_SELECTED_BRANCH",
        "DEC4962_02_radiative_G": "NO",
        "DEC4962_03_realistic_matter": "NO_PERTURBATIVE_ZERO_MODE_IN_TESTED_CORRIDOR",
        "DEC4962_04_full_compact_GR": "NO",
        "DEC4962_05_full_MTS": "NO",
    }
    add(
        checks,
        "VAL4962_15_decision",
        "compact promotion and claim boundaries",
        expected_decisions,
        decisions,
        decisions == expected_decisions,
    )

    promotions = result["promotions"]
    expected_promotions = {
        "selected_two_derivative_compact_point_particle_GR": True,
        "zero_leading_scalar_dipole_on_selected_branch": True,
        "same_conservative_and_radiative_GN": True,
        "realistic_EOS_perturbative_zero_mode_excluded": True,
        "all_operator_compact_GR": False,
        "full_MTS": False,
    }
    add(
        checks,
        "VAL4962_16_promotions",
        "result promotion map",
        expected_promotions,
        promotions,
        promotions == expected_promotions,
    )

    claim_rows = read_csv(CLAIMS)
    l804 = [row for row in claim_rows if row.get("claim_id") == "L-804"]
    add(
        checks,
        "VAL4962_17_claim_register",
        "one L-804 claim row",
        1,
        len(l804),
        len(l804) == 1
        and "all_operator_compact_GR_open" in l804[0]["status"],
    )

    variable_rows = read_csv(VARIABLES)
    required_symbols = {
        "CompactSensitivity4962_MTS",
        "ScalarZeroMode4962_MTS",
        "CompactJunction4962_MTS",
        "ConservativeRadiativeResidue4962_MTS",
        "StrongResidualBoundary4962_MTS",
        "PredictivityStatus4962_MTS",
    }
    symbol_counts = {
        symbol: sum(row.get("symbol") == symbol for row in variable_rows)
        for symbol in required_symbols
    }
    add(
        checks,
        "VAL4962_18_variables",
        "six unique variable-audit rows",
        {symbol: 1 for symbol in required_symbols},
        symbol_counts,
        all(count == 1 for count in symbol_counts.values()),
    )

    resume_text = text(RESUME)
    documentation_checks = {
        "checkpoint": MARKER in text(CHECKPOINT),
        "formal_note": FORMAL_MARKER in text(FORMAL_NOTE),
        "equations": "## 1.255 Compact-body sensitivity" in text(EQUATIONS),
        "red_team": "## 206. Leading compact GR" in text(RED_TEAM),
        "spine": FORMAL_MARKER in text(SPINE),
        "resume": (
            "Last checkpoint:" in resume_text and "4962-Y5-R2FR" in resume_text
        ),
        "local_spine": "Current State Through 4962" in text(LOCAL_SPINE),
    }
    add(
        checks,
        "VAL4962_19_documentation",
        "all current-state documents carry checkpoint 4962",
        {name: True for name in documentation_checks},
        documentation_checks,
        all(documentation_checks.values()),
    )

    expected_next = (
        "4963-Y5-R2FR-strong-field-C3-Wilson-selection-and-global-"
        "scalar-branch-exclusion-or-compact-GR-finite-residual.md"
    )
    add(
        checks,
        "VAL4962_20_next",
        "next target is finite compact residual closure",
        expected_next,
        result.get("next_target"),
        result.get("next_target") == expected_next,
    )

    pycache = [
        str(path)
        for path in (POST / "scripts").rglob("__pycache__")
        if path.is_dir()
    ]
    add(
        checks,
        "VAL4962_21_pycache",
        "no scripts pycache directories",
        [],
        pycache,
        not pycache,
    )

    failed = [row["validation_id"] for row in checks if not row["passed"]]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    print(
        json.dumps(
            {
                "marker": MARKER,
                "passed": len(checks) - len(failed),
                "total": len(checks),
                "failed": failed,
                "validation_path": str(OUTPUT),
            },
            indent=2,
        )
    )
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
