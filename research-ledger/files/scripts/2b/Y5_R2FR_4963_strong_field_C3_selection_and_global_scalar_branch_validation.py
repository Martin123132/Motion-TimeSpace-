from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4963"
OUTPUT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_4963_VALIDATION.csv"
)

MAIN_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_4963_strong_field_C3_selection_and_global_scalar_branch.py"
)
RESULT_JSON = SOURCE / "strong_field_C3_and_scalar_branch_results.json"
OWNERSHIP_CSV = SOURCE / "C3_source_ownership_audit.csv"
SELECTION_CSV = SOURCE / "C3_Wilson_selection_and_running.csv"
COMPACT_CSV = SOURCE / "compact_C3_residual_domain.csv"
SCALAR_CSV = SOURCE / "nonlinear_scalar_branch_theorem.csv"
DECISION_CSV = SOURCE / "strong_field_compact_GR_decision.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"

CHECKPOINT = (
    POST
    / "4963-Y5-R2FR-strong-field-C3-Wilson-selection-and-global-scalar-branch-exclusion-or-compact-GR-finite-residual.md"
)
FORMAL_NOTE = (
    FORMAL
    / "979-PPC4161-C3-Wilson-selection-nonlinear-scalar-exclusion-and-compact-residual.md"
)
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
LOCAL_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

TRAJECTORY_4958 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4958"
    / "essential_functional_GR_trajectory.csv"
)
MASS_FAMILY_4942 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4942"
    / "completed_O4_endpoint_Wilson_family.csv"
)
CONVEXITY_4956 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4956"
    / "functional_regular_convexity_gate.csv"
)
REGULARITY_4957 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4957"
    / "trajectory_functional_regularity_gate.csv"
)
EOS_4962 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4962"
    / "realistic_EOS_scalar_stability_transfer.csv"
)

MARKER = "MTS_4963_C3_SELECTION_GLOBAL_SCALAR_BRANCH"
FORMAL_MARKER = "PPC4161_C3_SCALAR_STRONG_FIELD_4963"

C_LIGHT = 299_792_458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054_571_817e-34
M_SUN_KG = 1.98847e30
PLANCK_LENGTH_M = math.sqrt(HBAR * G_NEWTON / C_LIGHT**3)
SOLAR_MASS_LENGTH_M = G_NEWTON * M_SUN_KG / C_LIGHT**2

HASH_LOCKS = {
    MAIN_SCRIPT: "9adaefe7fb06b0db30d0b6e13b1376fed78b20f6f63f1313dc36dbf08e61c01d",
    RESULT_JSON: "059b52fe849ea13082f5ad86221c85009a7595637e0ad0415b3ea59cbb37a791",
    OWNERSHIP_CSV: "5b0fd4d9df891073f1fbbc86aadf77ec2ae3b1efbd73ddc4e73843476c377102",
    SELECTION_CSV: "c130ad2c49cce89682726377d459d3af7119a330c82af10a6c18bed770f7dfa0",
    COMPACT_CSV: "75285482928f6b1f897e365968e6d38514ca5d22fe70c6b8538610531e3b2383",
    SCALAR_CSV: "fc066534b1e6a0317eabe2724a747bf49c9834c0e18543b7d7f582d46126d1fb",
    DECISION_CSV: "1d805fe878e18236d15e352a37a646a1249681bd8ed562bc5ebf67c6e6b5fafe",
    PROVENANCE: "dce7be5c78f6892ed2a08f06412984028e27999c9063f57c0c5dadefacd28025",
    CHECKPOINT: "ea2df6892c729fc3c49eb00074eb2d999c426c18046db60aa1f963b8cc9fcc48",
    FORMAL_NOTE: "dd265f0e8fd6244faff60027ae4cb8dc27b16028c7adeffbcb744e411e8ad71a",
    CLAIMS: "1a4f943c94d54f6ec1b72274c3538e8b82b9d2460b288a5c627cf825d8028989",
    VARIABLES: "9948bb7c909a4df301a84badf94e483cc66e8efd423e288b57313ee542e32489",
    EQUATIONS: "d39fbf27955b3dcf8308f336bf34f44046a93984f975ae06af9064476c38c3c6",
    RED_TEAM: "480bcd16b8e8f4c0a7d79be4af7cb21bb77571419a7e7d3bc6600d549e47597c",
    SPINE: "a079faf2b5a115f34349bec395af9718ef16e63a7160668d2f17e72f87499d29",
    RESUME: "d8c1fe84121ec7be79c84b3d9c3f7657bb9c516f8668dfd3292d2b2901755c91",
    LOCAL_SPINE: "b5a214736069b092020ff88c896a22cf7e7a5ee890254f6c26cb2a65c0dff7fd",
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
    return math.isclose(actual, expected, rel_tol=tolerance, abs_tol=1.0e-300)


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


def independent_C3_fit() -> dict[str, float]:
    trajectory = read_csv(TRAJECTORY_4958)
    groups: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(list)
    for row in trajectory:
        groups[(row["scheme"], int(row["polynomial_order"]))].append(row)

    estimates: list[float] = []
    slopes: list[float] = []
    maximum_residual = 0.0
    maximum_slope_error = 0.0
    base_source = -3.669491731602941e-5
    denominator = 483_840.0 * math.pi**2
    for group in groups.values():
        group.sort(key=lambda row: int(row["sample_index"]))
        eta_over_g = float(
            np.mean(
                [
                    float(row["eta_psi"]) / float(row["g"])
                    for row in group[-10:]
                ]
            )
        )
        source_slope = 0.5 * (base_source + eta_over_g / denominator)
        slopes.append(source_slope)
        analytic = [
            float(row["h_C3"]) / float(row["g"])
            - source_slope * math.log(float(row["g"]))
            for row in group[-10:]
        ]
        estimates.append(float(np.median(analytic)))
        for row_count in (10, 20):
            selected = group[-row_count:]
            g = np.asarray([float(row["g"]) for row in selected])
            y = np.asarray(
                [float(row["h_C3"]) / float(row["g"]) for row in selected]
            )
            log_g = np.log(g)
            matrix = np.column_stack(
                [np.ones(row_count), log_g, g, g * log_g]
            )
            coefficients = np.linalg.lstsq(matrix, y, rcond=None)[0]
            estimates.append(float(coefficients[0]))
            maximum_residual = max(
                maximum_residual,
                float(np.max(np.abs(matrix @ coefficients - y))),
            )
            maximum_slope_error = max(
                maximum_slope_error,
                abs(float(coefficients[1]) - source_slope),
            )

    family = read_csv(MASS_FAMILY_4942)
    family_groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in family:
        family_groups[(row["mapping"], row["relative_gravity_seed"])].append(row)
    displacements: list[float] = []
    for group in family_groups.values():
        baseline = min(group, key=lambda row: float(row["J_gap_endpoint"]))
        baseline_A = float(baseline["A_C3"])
        displacements.extend(
            abs(float(row["A_C3"]) - baseline_A) for row in group
        )
    displacement = max(displacements)
    selected_min = min(estimates) - displacement
    selected_max = max(estimates) + displacement
    selected_abs = max(abs(selected_min), abs(selected_max))
    return {
        "group_count": float(len(groups)),
        "selected_min": selected_min,
        "selected_max": selected_max,
        "B_min": min(slopes),
        "B_max": max(slopes),
        "displacement": displacement,
        "maximum_residual": maximum_residual,
        "maximum_slope_error": maximum_slope_error,
        "a_plus": 16.0 * math.pi * selected_abs * PLANCK_LENGTH_M**4,
    }


def main() -> int:
    checks: list[dict[str, Any]] = []

    missing = [str(path) for path in HASH_LOCKS if not path.exists()]
    add(
        checks,
        "VAL4963_01_paths",
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
        "VAL4963_02_hashes",
        "research, data and documentation hashes match",
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
        "VAL4963_03_compile",
        "research and validation scripts compile in memory",
        [],
        compile_errors,
        not compile_errors,
    )

    result = json.loads(text(RESULT_JSON))
    add(
        checks,
        "VAL4963_04_marker",
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
        "VAL4963_05_internal",
        "all 19 research checks pass",
        {"count": 19, "failed": []},
        {"count": len(result["checks"]), "failed": failed_internal},
        len(result["checks"]) == 19 and not failed_internal,
    )

    source_hashes = result["source_hashes"]
    failed_clauses = [
        name
        for name, passed in result["source_clause_checks"].items()
        if not passed
    ]
    add(
        checks,
        "VAL4963_06_sources",
        "13 source hashes and six source clauses pass",
        {"hashes": 13, "clauses": 6, "failed": []},
        {
            "hashes": len(source_hashes),
            "clauses": len(result["source_clause_checks"]),
            "failed": failed_clauses,
        },
        len(source_hashes) == 13
        and len(result["source_clause_checks"]) == 6
        and not failed_clauses,
    )

    tables = {
        "ownership": read_csv(OWNERSHIP_CSV),
        "selection": read_csv(SELECTION_CSV),
        "compact": read_csv(COMPACT_CSV),
        "scalar": read_csv(SCALAR_CSV),
        "decision": read_csv(DECISION_CSV),
    }
    counts = {name: len(rows) for name, rows in tables.items()}
    expected_counts = {
        "ownership": 8,
        "selection": 10,
        "compact": 11,
        "scalar": 11,
        "decision": 7,
    }
    add(
        checks,
        "VAL4963_07_counts",
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
        "VAL4963_08_csv_shape",
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
        "VAL4963_09_claim_flags",
        "all generated rows carry the marker and full-MTS false",
        [],
        claim_errors,
        not claim_errors,
    )

    ownership = {row["operator_id"]: row for row in tables["ownership"]}
    p6_ids = {
        "C3OWN4963_O1",
        "C3OWN4963_O2",
        "C3OWN4963_O3",
        "C3OWN4963_O4",
        "C3OWN4963_O5",
        "C3OWN4963_PX",
        "C3OWN4963_JGAP",
    }
    p6_bad = [
        item
        for item in p6_ids
        if item not in ownership
        or not truth(ownership[item]["passed"])
        or not truth(ownership[item]["valid_for_declared_p6_zero_state"])
    ]
    tail = ownership.get("C3OWN4963_P8PLUS", {})
    add(
        checks,
        "VAL4963_10_ownership",
        "declared p6 sources close and p>=8 remains open",
        {"p6_bad": [], "p8_status": "FULL_PARENT_TAIL_OPEN", "p8_valid": False},
        {
            "p6_bad": p6_bad,
            "p8_status": tail.get("status"),
            "p8_valid": truth(tail.get("valid_for_declared_p6_zero_state")),
        },
        not p6_bad
        and tail.get("status") == "FULL_PARENT_TAIL_OPEN"
        and not truth(tail.get("valid_for_declared_p6_zero_state")),
    )

    independent = independent_C3_fit()
    C3 = result["C3_selection"]
    C3_differences = {
        "selected_min": abs(independent["selected_min"] - C3["selected_A_C3_min"]),
        "selected_max": abs(independent["selected_max"] - C3["selected_A_C3_max"]),
        "B_min": abs(independent["B_min"] - C3["source_B_C3_min"]),
        "B_max": abs(independent["B_max"] - C3["source_B_C3_max"]),
        "displacement": abs(
            independent["displacement"] - C3["finite_gap_A_C3_displacement"]
        ),
        "a_plus": abs(independent["a_plus"] - C3["selected_a_plus_abs_m4"]),
    }
    add(
        checks,
        "VAL4963_11_C3_independent",
        "independent source fit reproduces the C3 selection",
        {"max_normalized_difference": 0.0},
        C3_differences,
        close(independent["selected_min"], C3["selected_A_C3_min"])
        and close(independent["selected_max"], C3["selected_A_C3_max"])
        and close(independent["B_min"], C3["source_B_C3_min"])
        and close(independent["B_max"], C3["source_B_C3_max"])
        and close(
            independent["displacement"],
            C3["finite_gap_A_C3_displacement"],
        )
        and close(independent["a_plus"], C3["selected_a_plus_abs_m4"]),
    )

    add(
        checks,
        "VAL4963_12_C3_quality",
        "fit, source-slope, finite-gap and sign gates",
        {
            "fits": 8,
            "fit_residual_lt": 2.0e-10,
            "slope_error_lt": 5.0e-10,
            "gap": 8.08875617759326e-8,
            "selected_max_lt": 0.0,
        },
        {
            "fits": C3["fit_count"],
            "fit_residual": C3["maximum_fit_residual"],
            "slope_error": C3["maximum_slope_error"],
            "gap": C3["finite_gap_A_C3_displacement"],
            "selected_max": C3["selected_A_C3_max"],
        },
        C3["fit_count"] == 8
        and C3["maximum_fit_residual"] < 2.0e-10
        and C3["maximum_slope_error"] < 5.0e-10
        and close(C3["finite_gap_A_C3_displacement"], 8.08875617759326e-8)
        and C3["selected_A_C3_max"] < 0.0,
    )

    compact = tables["compact"]
    failed_compact = [row["object_id"] for row in compact if not truth(row["passed"])]
    finite_values = [
        float(row.get("finite_abs_Deltaa_over_aN") or row.get("finite_epsilon_h"))
        for row in compact
    ]
    running_values = [
        float(row.get("running_abs_Deltaa_over_aN") or row.get("running_epsilon_h"))
        for row in compact
    ]
    add(
        checks,
        "VAL4963_13_compact",
        "eleven compact rows pass and reproduce maxima",
        {
            "failed": [],
            "finite_max": 7.415086500522157e-158,
            "running_max": 1.1065178572529907e-155,
        },
        {
            "failed": failed_compact,
            "finite_max": max(finite_values),
            "running_max": max(running_values),
        },
        not failed_compact
        and close(max(finite_values), 7.415086500522157e-158)
        and close(max(running_values), 1.1065178572529907e-155),
    )

    benchmark = next(
        row
        for row in compact
        if row["object_id"] == "canonical_1p4_12km_benchmark"
    )
    benchmark_mass = 1.4 * SOLAR_MASS_LENGTH_M
    benchmark_expected = (
        140.0
        * float(benchmark["a_plus_finite_abs_max_m4"])
        * benchmark_mass**2
        / 12_000.0**6
    )
    add(
        checks,
        "VAL4963_14_benchmark",
        "independent 1.4-Msun 12-km finite residual",
        benchmark_expected,
        float(benchmark["finite_abs_Deltaa_over_aN"]),
        close(
            float(benchmark["finite_abs_Deltaa_over_aN"]),
            benchmark_expected,
        ),
    )

    black_hole = next(
        row for row in compact if row["object_id"] == "Schwarzschild_10Msun"
    )
    black_hole_mass = 10.0 * SOLAR_MASS_LENGTH_M
    black_hole_expected = (
        0.75
        * float(black_hole["a_plus_finite_abs_max_m4"])
        / black_hole_mass**4
    )
    add(
        checks,
        "VAL4963_15_black_hole",
        "independent ten-solar-mass horizon proxy",
        black_hole_expected,
        float(black_hole["finite_epsilon_h"]),
        close(float(black_hole["finite_epsilon_h"]), black_hole_expected),
    )

    scalar = {row["theorem_id"]: row for row in tables["scalar"]}
    required_scalar = {
        "SCALAR4963_00_equation",
        "SCALAR4963_01_multiplier",
        "SCALAR4963_02_junction",
        "SCALAR4963_03_outer_boundary",
        "SCALAR4963_04_kinetic_sign",
        "SCALAR4963_05_potential_sign",
        "SCALAR4963_06_no_odd_source",
        "SCALAR4963_07_conclusion",
        "SCALAR4963_08_failure_surface",
    }
    scalar_bad = [
        item
        for item in required_scalar
        if item not in scalar
        or not truth(scalar[item]["passed"])
        or not truth(scalar[item]["valid_for_certified_x_le_0p1"])
    ]
    add(
        checks,
        "VAL4963_16_scalar_theorem",
        "all static multiplier theorem clauses pass in the certified chart",
        [],
        scalar_bad,
        not scalar_bad
        and scalar["SCALAR4963_07_conclusion"]["status"]
        == "NO_HEALTHY_DISCONNECTED_STATIC_SCALAR_BRANCH_IN_CERTIFIED_DOMAIN",
    )

    convexity = read_csv(CONVEXITY_4956)
    regularity = read_csv(REGULARITY_4957)
    local_fixed = [
        row for row in convexity if math.isclose(float(row["x_domain_max"]), 0.1)
    ]
    extended_fixed = [
        row for row in convexity if math.isclose(float(row["x_domain_max"]), 0.25)
    ]
    minimum_singular = min(
        [float(row["minimum_singular_value"]) for row in local_fixed]
        + [float(row["minimum_singular_value"]) for row in regularity]
    )
    add(
        checks,
        "VAL4963_17_scalar_domain",
        "source scans certify x<=0.1 and reject an all-X claim",
        {
            "local_all_convex": True,
            "extended_all_convex": False,
            "minimum": 0.33637208449902206,
        },
        {
            "local_all_convex": all(
                truth(row["scalar_convex"]) for row in local_fixed + regularity
            ),
            "extended_all_convex": all(
                truth(row["scalar_convex"]) for row in extended_fixed
            ),
            "minimum": minimum_singular,
        },
        all(truth(row["scalar_convex"]) for row in local_fixed + regularity)
        and not all(truth(row["scalar_convex"]) for row in extended_fixed)
        and close(minimum_singular, 0.33637208449902206),
    )

    EOS = read_csv(EOS_4962)
    maximum_density_ratio = max(
        float(row["central_to_critical_ratio"]) for row in EOS
    )
    add(
        checks,
        "VAL4963_18_EOS",
        "nine source-backed EOS rows remain stable",
        {
            "count": 9,
            "all_pass": True,
            "max_ratio": 5.3697748471940454e-18,
        },
        {
            "count": len(EOS),
            "all_pass": all(truth(row["passed"]) for row in EOS),
            "max_ratio": maximum_density_ratio,
        },
        len(EOS) == 9
        and all(truth(row["passed"]) for row in EOS)
        and close(maximum_density_ratio, 5.3697748471940454e-18),
    )

    decisions = {row["decision_id"]: row["decision"] for row in tables["decision"]}
    expected_decisions = {
        "DEC4963_00_C3_p6_selection": "YES_IN_LOCKED_SOURCE_SCHEME",
        "DEC4963_01_C3_compact": "NO_WITHIN_DECLARED_LOCAL_AND_RUNNING_ENVELOPES",
        "DEC4963_02_scalar_nonlinear": "NO",
        "DEC4963_03_scalar_all_X": "NO",
        "DEC4963_04_all_operator_compact_GR": "NO",
        "DEC4963_05_full_MTS": "NO",
        "DEC4963_06_next_target": "FINITE_R2_C2_CFF_MATCHING_AND_P8PLUS_TAIL",
    }
    add(
        checks,
        "VAL4963_19_decisions",
        "decision matrix preserves exact scope",
        expected_decisions,
        decisions,
        decisions == expected_decisions,
    )

    document_text = {
        "checkpoint": text(CHECKPOINT),
        "formal_note": text(FORMAL_NOTE),
        "equations": text(EQUATIONS),
        "red_team": text(RED_TEAM),
        "spine": text(SPINE),
        "resume": text(RESUME),
        "local_spine": text(LOCAL_SPINE),
    }
    missing_markers = [
        name
        for name, content in document_text.items()
        if FORMAL_MARKER not in content and MARKER not in content
    ]
    add(
        checks,
        "VAL4963_20_docs",
        "all documentation surfaces carry a 4963 marker",
        [],
        missing_markers,
        not missing_markers,
    )

    claim_rows = read_csv(CLAIMS)
    variable_rows = read_csv(VARIABLES)
    claim = [row for row in claim_rows if row.get("claim_id") == "L-805"]
    variable_symbols = {
        row.get("symbol")
        for row in variable_rows
        if row.get("symbol")
        in {
            "A_C3^S",
            "B_C3",
            "a_plus4963",
            "I_scalar4963",
            "D_healthy4963",
            "PredictivityStatus4963_MTS",
        }
    }
    add(
        checks,
        "VAL4963_21_registers",
        "claim L-805 and six canonical variables are registered",
        {"claims": 1, "variables": 6},
        {"claims": len(claim), "variables": len(variable_symbols)},
        len(claim) == 1 and len(variable_symbols) == 6,
    )

    scope = result["claim_scope"]
    add(
        checks,
        "VAL4963_22_scope",
        "conditional p6 result true while broad claims remain false",
        {
            "p6_C3": True,
            "static_scalar_x_le_0p1": True,
            "all_X": False,
            "all_operator_compact_GR": False,
            "full_MTS": False,
        },
        {
            "p6_C3": scope["declared_p6_zero_state_C3_selected"],
            "static_scalar_x_le_0p1": scope[
                "healthy_static_scalar_branch_x_le_0p1_excluded"
            ],
            "all_X": scope["all_X_scalar_branch_excluded"],
            "all_operator_compact_GR": scope["all_operator_compact_GR"],
            "full_MTS": scope["full_MTS"],
        },
        scope["declared_p6_zero_state_C3_selected"]
        and scope["healthy_static_scalar_branch_x_le_0p1_excluded"]
        and not scope["all_X_scalar_branch_excluded"]
        and not scope["all_operator_compact_GR"]
        and not scope["full_MTS"],
    )

    pycache = sorted(
        str(path.relative_to(ROOT))
        for path in (POST / "scripts").rglob("__pycache__")
    )
    add(
        checks,
        "VAL4963_23_pycache",
        "scripts tree contains no __pycache__",
        [],
        pycache,
        not pycache,
    )

    all_passed = all(row["passed"] for row in checks)
    add(
        checks,
        "VAL4963_24_all",
        "all preceding validation checks pass",
        True,
        all_passed,
        all_passed,
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    failed = [row["validation_id"] for row in checks if not row["passed"]]
    print(f"{MARKER}_VALIDATION={len(checks)-len(failed)}/{len(checks)}", flush=True)
    print(f"{MARKER}_FAILED={failed}", flush=True)
    print(f"{MARKER}_OUTPUT={OUTPUT}", flush=True)
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
