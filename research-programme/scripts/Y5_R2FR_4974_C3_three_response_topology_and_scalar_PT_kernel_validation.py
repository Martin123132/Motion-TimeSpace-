from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from scipy.integrate import quad


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4974"
OUTPUT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_4974_VALIDATION.csv"
)

SCHEME_LOCK = SOURCE / "C3_parent_scheme_lock.csv"
TOPOLOGY = SOURCE / "C3_three_response_topology.csv"
SCALAR_KERNEL = SOURCE / "C3_scalar_PT_m3_local_kernel.csv"
HELICITY = SOURCE / "C3_scalar_PT_m3_helicity_projection.csv"
COVERAGE = SOURCE / "C3_kernel_sector_coverage.csv"
RESULT = SOURCE / "C3_three_response_topology_and_scalar_PT_kernel_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

CHECKPOINT = (
    POST
    / "4974-Y5-R2FR-C3-third-response-topology-correction-and-free-scalar-proper-time-kernel.md"
)
PREDECESSOR = (
    POST
    / "4973-Y5-R2FR-C3-fixed-point-form-factor-characteristics-kernel-null-family-and-finite-anchor-verdict.md"
)
FORMAL_NOTE = (
    FORMAL
    / "990-PPC4161-C3-third-response-topology-and-free-scalar-proper-time-kernel.md"
)
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION = FORMAL / "07-unification-spine.md"

MARKER = "VAL4974"
SCIENTIFIC_MARKER = "MTS_4974_C3_THREE_RESPONSE_AND_SCALAR_PT_KERNEL"
FORMAL_MARKER = "PPC4161_C3_THREE_RESPONSE_AND_SCALAR_PT_KERNEL_4974"
CHECKED_DATE = "2026-07-13"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def rectangular_csv(path: Path, expected_width: int) -> tuple[bool, int]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    widths = {len(row) for row in rows}
    return widths == {expected_width}, len(rows)


def validation_row(
    index: int,
    test: str,
    observed: Any,
    expected: Any,
    passed: bool,
) -> dict[str, Any]:
    def render(value: Any) -> str:
        if isinstance(value, str):
            return value
        return json.dumps(value, sort_keys=True)

    return {
        "check_id": f"{MARKER}_{index:02d}",
        "test": test,
        "observed": render(observed),
        "expected": render(expected),
        "passed": bool(passed),
        "checkpoint_marker": SCIENTIFIC_MARKER,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
    }


def write_csv(rows: list[dict[str, Any]]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    rows: list[dict[str, Any]] = []
    required_paths = (
        SCHEME_LOCK,
        TOPOLOGY,
        SCALAR_KERNEL,
        HELICITY,
        COVERAGE,
        RESULT,
        PROVENANCE,
        CHECKPOINT,
        PREDECESSOR,
        FORMAL_NOTE,
        RESUME,
        SPINE,
        CLAIMS,
        VARIABLES,
        EQUATIONS,
        RED_TEAM,
        UNIFICATION,
    )
    missing = [str(path) for path in required_paths if not path.exists()]
    rows.append(
        validation_row(
            len(rows),
            "all checkpoint products and handoff files exist",
            missing,
            [],
            not missing,
        )
    )

    result = json.loads(RESULT.read_text(encoding="utf-8"))
    failed_internal = [
        name for name, passed in result["checks"].items() if not passed
    ]
    rows.append(
        validation_row(
            len(rows),
            "runner reports all internal checks passing",
            {
                "count": result["check_count"],
                "failed": failed_internal,
            },
            {"count": 28, "failed": []},
            result["check_count"] == 28
            and not failed_internal
            and not result["failed_checks"],
        )
    )

    topology = read_csv(TOPOLOGY)
    determinant = [
        row for row in topology if row["flow_type"] == "one_loop_log_determinant"
    ]
    determinant_counts = Counter(row["topology_class"] for row in determinant)
    determinant_signs = Counter(
        (row["topology_class"], int(row["coefficient"])) for row in determinant
    )
    rows.append(
        validation_row(
            len(rows),
            "one-loop determinant has exact 1+3+2 C3 topology",
            {
                "terms": len(determinant),
                "classes": dict(determinant_counts),
                "signs": {str(key): value for key, value in determinant_signs.items()},
            },
            "one +Gamma5; three -mixed; two +triangles",
            len(determinant) == 6
            and determinant_counts
            == {
                "Gamma5_contact": 1,
                "Gamma3_Gamma4_mixed": 3,
                "Gamma3_cubed_triangle": 2,
            }
            and determinant_signs[("Gamma5_contact", 1)] == 1
            and determinant_signs[("Gamma3_Gamma4_mixed", -1)] == 3
            and determinant_signs[("Gamma3_cubed_triangle", 1)] == 2,
        )
    )

    wetterich = [
        row
        for row in topology
        if row["flow_type"] == "exact_Wetterich_field_independent_Rdot"
    ]
    wetterich_counts = Counter(row["topology_class"] for row in wetterich)
    rows.append(
        validation_row(
            len(rows),
            "exact Wetterich third response has ordered 1+6+6 topology",
            {"terms": len(wetterich), "classes": dict(wetterich_counts)},
            {
                "terms": 13,
                "classes": {
                    "Gamma5_contact": 1,
                    "Gamma3_Gamma4_mixed": 6,
                    "Gamma3_cubed_triangle": 6,
                },
            },
            len(wetterich) == 13
            and wetterich_counts
            == {
                "Gamma5_contact": 1,
                "Gamma3_Gamma4_mixed": 6,
                "Gamma3_cubed_triangle": 6,
            },
        )
    )

    erratum = [row for row in topology if row["term_id"] == "C3TOP4974_ERRATUM"]
    rows.append(
        validation_row(
            len(rows),
            "two-response Gamma4 plus Gamma3-squared target is explicitly superseded",
            erratum[0]["status"] if len(erratum) == 1 else "row_count_error",
            "SUPERSEDED_FOR_C3",
            len(erratum) == 1 and erratum[0]["status"] == "SUPERSEDED_FOR_C3",
        )
    )

    scheme = read_csv(SCHEME_LOCK)
    source_paths_missing: list[str] = []
    for row in scheme:
        for path_string in row["source_path"].split(";"):
            if not (ROOT / path_string).exists():
                source_paths_missing.append(path_string)
    rows.append(
        validation_row(
            len(rows),
            "all five scheme-lock rows have existing local sources",
            {"rows": len(scheme), "missing": source_paths_missing},
            {"rows": 5, "missing": []},
            len(scheme) == 5 and not source_paths_missing,
        )
    )

    scalar = read_csv(SCALAR_KERNEL)
    scalar_by_x = {float(row["x_equals_3k2_over_m2"]): row for row in scalar}
    rows.append(
        validation_row(
            len(rows),
            "scalar kernel grid contains both asymptotic tails and x=3 peak",
            {
                "rows": len(scalar),
                "minimum_x": min(scalar_by_x),
                "maximum_x": max(scalar_by_x),
                "x3": 3.0 in scalar_by_x,
            },
            {"rows": 13, "minimum_x": 1e-8, "maximum_x": 1e8, "x3": True},
            len(scalar) == 13
            and min(scalar_by_x) == 1e-8
            and max(scalar_by_x) == 1e8
            and 3.0 in scalar_by_x,
        )
    )

    x3_value = float(scalar_by_x[3.0]["m2_dzeta_dlnk_over_C0"])
    rows.append(
        validation_row(
            len(rows),
            "scalar flow magnitude peaks at x=3 with exact value -81/128",
            x3_value,
            -81.0 / 128.0,
            math.isclose(x3_value, -81.0 / 128.0, rel_tol=0.0, abs_tol=1e-15),
        )
    )

    integral, error = quad(
        lambda value: 3.0 * value**2 / (1.0 + value) ** 4,
        0.0,
        math.inf,
        epsabs=1e-13,
        epsrel=1e-13,
        limit=300,
    )
    rows.append(
        validation_row(
            len(rows),
            "independent scalar threshold integral equals one",
            {"integral": integral, "error": error},
            1.0,
            math.isclose(integral, 1.0, rel_tol=0.0, abs_tol=2e-13),
        )
    )

    rows.append(
        validation_row(
            len(rows),
            "cumulative scalar fractions match the exact cube law",
            {
                "x1": float(scalar_by_x[1.0]["cumulative_IR_to_x_fraction"]),
                "x3": float(scalar_by_x[3.0]["cumulative_IR_to_x_fraction"]),
                "x10": float(scalar_by_x[10.0]["cumulative_IR_to_x_fraction"]),
            },
            {"x1": 1 / 8, "x3": 27 / 64, "x10": (10 / 11) ** 3},
            math.isclose(
                float(scalar_by_x[1.0]["cumulative_IR_to_x_fraction"]),
                1 / 8,
                rel_tol=0.0,
                abs_tol=1e-15,
            )
            and math.isclose(
                float(scalar_by_x[3.0]["cumulative_IR_to_x_fraction"]),
                27 / 64,
                rel_tol=0.0,
                abs_tol=1e-15,
            )
            and math.isclose(
                float(scalar_by_x[10.0]["cumulative_IR_to_x_fraction"]),
                (10 / 11) ** 3,
                rel_tol=0.0,
                abs_tol=1e-15,
            ),
        )
    )

    low_tail = float(scalar_by_x[1e-8]["m2_dzeta_dlnk_over_C0"]) / (1e-8) ** 3
    high_tail = float(scalar_by_x[1e8]["m2_dzeta_dlnk_over_C0"]) * 1e8
    rows.append(
        validation_row(
            len(rows),
            "scalar kernel has the independently checked IR x-cubed and UV inverse-x tails",
            {"low_coefficient": low_tail, "high_coefficient": high_tail},
            {"low_coefficient": -6.0, "high_coefficient": -6.0},
            math.isclose(low_tail, -6.0, rel_tol=5e-8, abs_tol=0.0)
            and math.isclose(high_tail, -6.0, rel_tol=5e-8, abs_tol=0.0),
        )
    )

    helicity = read_csv(HELICITY)
    grouped: dict[float, dict[str, float]] = {}
    for row in helicity:
        grouped.setdefault(float(row["x_equals_3k2_over_m2"]), {})[
            row["helicity"]
        ] = float(row["projected_helicity_source"])
    ratios = [values["++++"] / values["-+++"] for values in grouped.values()]
    rows.append(
        validation_row(
            len(rows),
            "all eight local helicity rows preserve the exact factor-ten identity",
            {"x_rows": len(grouped), "maximum_residual": max(abs(value - 10) for value in ratios)},
            {"x_rows": 8, "maximum_residual": 0.0},
            len(grouped) == 8 and max(abs(value - 10) for value in ratios) == 0.0,
        )
    )

    coverage = {row["sector"]: row for row in read_csv(COVERAGE)}
    rows.append(
        validation_row(
            len(rows),
            "coverage matrix promotes only the free scalar local row",
            {
                sector: row["local_C3_kernel_status"] for sector, row in coverage.items()
            },
            "free scalar calculated; interacting motion, graviton, and ghost remain partial/open",
            coverage["free_massive_real_scalar"]["local_C3_kernel_status"]
            == "CALCULATED_AND_INTEGRATED"
            and coverage["interacting_motion_scalar"]["local_C3_kernel_status"]
            == "FREE_POLE_BENCHMARK_ONLY"
            and coverage["graviton"]["finite_momentum_status"] == "OPEN"
            and coverage["ghost"]["finite_momentum_status"] == "OPEN",
        )
    )

    scientific_rows = scheme + topology + scalar + helicity + list(coverage.values())
    rows.append(
        validation_row(
            len(rows),
            "all generated scientific rows remain private nonclaim",
            {"rows": len(scientific_rows)},
            {"all_valid_for_full_MTS_claim": False},
            all(
                row["checkpoint_marker"] == SCIENTIFIC_MARKER
                and row["valid_for_full_MTS_claim"] == "False"
                for row in scientific_rows
            )
            and result["valid_for_full_MTS_claim"] is False,
        )
    )

    generated_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (SCHEME_LOCK, TOPOLOGY, SCALAR_KERNEL, HELICITY, COVERAGE, RESULT)
    )
    rows.append(
        validation_row(
            len(rows),
            "generated products contain no placeholder sentinel",
            {"MISSING_": generated_text.count("MISSING_")},
            {"MISSING_": 0},
            "MISSING_" not in generated_text,
        )
    )

    handoffs = (
        CHECKPOINT,
        PROVENANCE,
        FORMAL_NOTE,
        RESUME,
        SPINE,
        EQUATIONS,
        RED_TEAM,
        UNIFICATION,
    )
    absent_markers = [
        str(path)
        for path in handoffs
        if FORMAL_MARKER not in path.read_text(encoding="utf-8")
    ]
    rows.append(
        validation_row(
            len(rows),
            "formal marker propagates through every current handoff",
            absent_markers,
            [],
            not absent_markers,
        )
    )

    predecessor_text = PREDECESSOR.read_text(encoding="utf-8")
    rows.append(
        validation_row(
            len(rows),
            "4973 historical checkpoint carries an explicit 4974 topology correction",
            "Checkpoint 4974 correction" in predecessor_text,
            True,
            "Checkpoint 4974 correction" in predecessor_text
            and "Gamma^(5)" in predecessor_text,
        )
    )

    resume_text = RESUME.read_text(encoding="utf-8")
    spine_text = SPINE.read_text(encoding="utf-8")
    rows.append(
        validation_row(
            len(rows),
            "resume and local coupling spine point to checkpoint 4974",
            {
                "resume": "Last checkpoint: `4974-" in resume_text,
                "spine": "Current State Through 4974" in spine_text,
            },
            {"resume": True, "spine": True},
            "Last checkpoint: `4974-" in resume_text
            and "Current State Through 4974" in spine_text,
        )
    )

    claims_rectangular, claims_count = rectangular_csv(CLAIMS, 13)
    claim_816 = [row for row in read_csv(CLAIMS) if row["claim_id"] == "L-816"]
    rows.append(
        validation_row(
            len(rows),
            "claims register is rectangular and contains one L-816 row",
            {"rows": claims_count, "L-816": len(claim_816)},
            {"L-816": 1},
            claims_rectangular
            and len(claim_816) == 1
            and FORMAL_MARKER in claim_816[0]["notes"],
        )
    )

    variables_rectangular, variables_count = rectangular_csv(VARIABLES, 11)
    expected_symbols = {
        "C3ThirdResponse4974_MTS",
        "Gamma5Contact4974_MTS",
        "ScalarPTKernel4974_MTS",
        "ScalarThresholdX4974_MTS",
        "ScalarCumulative4974_MTS",
        "C3KernelCoverage4974_MTS",
    }
    variable_rows = read_csv(VARIABLES)
    observed_symbols = {
        row["symbol"] for row in variable_rows if row["symbol"] in expected_symbols
    }
    rows.append(
        validation_row(
            len(rows),
            "variable audit is rectangular and contains all six 4974 symbols",
            {"rows": variables_count, "symbols": sorted(observed_symbols)},
            sorted(expected_symbols),
            variables_rectangular and observed_symbols == expected_symbols,
        )
    )

    h4973 = [row for row in variable_rows if row["symbol"] == "H_C34973_MTS"]
    rows.append(
        validation_row(
            len(rows),
            "stale H_C3 variable row is corrected to the third response",
            h4973[0]["status"] if len(h4973) == 1 else "row_count_error",
            "required_momentum_kernel_open_topology_corrected_4974",
            len(h4973) == 1
            and h4973[0]["status"]
            == "required_momentum_kernel_open_topology_corrected_4974"
            and "Gamma5" in h4973[0]["equations"],
        )
    )

    checkpoint_text = CHECKPOINT.read_text(encoding="utf-8")
    rows.append(
        validation_row(
            len(rows),
            "claim boundary keeps the physical logarithm and full parent kernel open",
            {
                "log_open": "physical logarithmic endpoint from 4974     = not claimed" in checkpoint_text,
                "full_open": "full delta_c_fin                            = open" in checkpoint_text,
            },
            {"log_open": True, "full_open": True},
            "physical logarithmic endpoint from 4974     = not claimed" in checkpoint_text
            and "full delta_c_fin                            = open" in checkpoint_text,
        )
    )

    write_csv(rows)
    failed = [row["check_id"] for row in rows if not row["passed"]]
    print(f"{MARKER}_CHECKS={len(rows)}", flush=True)
    print(f"{MARKER}_PASSED={len(rows) - len(failed)}", flush=True)
    print(f"{MARKER}_FAILED={len(failed)}", flush=True)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    if failed:
        print(f"{MARKER}_FAILED_IDS={','.join(failed)}", flush=True)
        return 1
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
