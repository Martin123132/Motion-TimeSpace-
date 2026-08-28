from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import sys
from types import SimpleNamespace
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
PRIMARY_PATH = SCRIPTS / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
INPUT = FUNCTIONAL_RG / "5396"
OUTPUT = FUNCTIONAL_RG / "5397"
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5397_VALIDATION.csv"
)


def load_primary() -> Any:
    specification = importlib.util.spec_from_file_location(
        "mts_5397_primary", PRIMARY_PATH
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {PRIMARY_PATH}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def relative_error(left: complex, right: complex) -> float:
    return abs(left - right) / max(1.0e-30, abs(left), abs(right))


def state_key(configuration: dict[str, Any]) -> tuple[str, str, int, int]:
    return (
        str(configuration["role"]),
        "|".join(configuration["labels"]),
        int(configuration["trace_orientation"]),
        int(configuration["winding_delta"]),
    )


def observed_state_key(row: dict[str, str]) -> tuple[str, str, int, int]:
    return (
        row["selected_role"],
        row["selected_labels"],
        int(row["orientation"]),
        int(row["winding_delta"]),
    )


def transition_chart_rows(
    primary: Any, transition_rows: list[dict[str, str]]
) -> list[dict[str, Any]]:
    context = primary.M5308.M5303.synthetic_context()
    rows: list[dict[str, Any]] = []
    for probe_index, probe in enumerate(transition_rows):
        term_id = probe["term_id"]
        coordinate = float(probe["coordinate"])
        energy = float(probe["energy"])
        parent = primary.parent_point_component(
            context, term_id, coordinate, energy
        )
        parent_value = complex(parent["residue"])
        configurations = primary.configuration_variants(term_id)
        observed = observed_state_key(probe)
        for configuration in configurations:
            chart_value = primary.finite_displacement_residue_midpoint(
                configuration,
                coordinate,
                energy,
                0.0025,
            )
            rows.append(
                {
                    "probe_index": probe_index,
                    "mapped_cell_id": probe["mapped_cell_id"],
                    "term_id": term_id,
                    "x_fraction": float(probe["x_fraction"]),
                    "energy_fraction": float(probe["energy_fraction"]),
                    "coordinate": coordinate,
                    "energy": energy,
                    "parent_selected_role": parent["selected_role"],
                    "observed_state_is_this_chart": (
                        state_key(configuration) == observed
                    ),
                    "chart_role": configuration["role"],
                    "chart_labels": "|".join(configuration["labels"]),
                    "chart_orientation": int(
                        configuration["trace_orientation"]
                    ),
                    "chart_winding_delta": int(
                        configuration["winding_delta"]
                    ),
                    "parent_residue_real": parent_value.real,
                    "parent_residue_imaginary": parent_value.imag,
                    "chart_residue_real": chart_value.real,
                    "chart_residue_imaginary": chart_value.imag,
                    "chart_to_parent_relative_error": relative_error(
                        chart_value, parent_value
                    ),
                    "chart_equivalent_to_parent": relative_error(
                        chart_value, parent_value
                    )
                    <= 1.0e-7,
                    "selected_unit_margin": float(
                        probe["selected_unit_margin"]
                    ),
                    "reciprocal_residual": float(
                        probe["reciprocal_residual"]
                    ),
                }
            )
    return rows


def closed_union_smoke_rows(
    primary: Any,
    transition_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    mapped = {
        row["mapped_cell_id"]: row
        for row in primary.read_csv(primary.MAPPED_5393)
    }
    supports = {
        (row["atlas_cell_id"], row["reduced_MC04_term_ids"]): row
        for row in primary.away_term_support_cells()
    }
    support_segments = primary.material_support_segments()
    branches = primary.material_branch_data()
    epsilon_row = primary.epsilon_boxes(
        SimpleNamespace(
            combined_regulator_box=True,
            combined_regulator_slab_count=2,
            epsilon_subdivisions=1,
        )
    )[0]
    selected: dict[tuple[str, str], dict[str, str]] = {}
    for row in transition_rows:
        selected.setdefault((row["mapped_cell_id"], row["term_id"]), row)
    passed: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    for (mapped_cell_id, term_id), probe in sorted(selected.items()):
        source_cell = mapped[mapped_cell_id]
        support = supports[(source_cell["atlas_cell_id"], term_id)]
        coordinate = float(probe["coordinate"])
        source_width = float(source_cell["upper_absolute_soft_cosine"]) - float(
            source_cell["lower_absolute_soft_cosine"]
        )
        half_x_width = max(1.0e-12, source_width * 1.0e-7)
        x_lower = max(
            float(support["lower_absolute_soft_cosine"]),
            coordinate - half_x_width,
        )
        x_upper = min(
            float(support["upper_absolute_soft_cosine"]),
            coordinate + half_x_width,
        )
        t_midpoint = float(probe["energy_fraction"])
        t_lower = max(0.0, t_midpoint - 1.0e-6)
        t_upper = min(1.0, t_midpoint + 1.0e-6)
        try:
            enclosure = primary.evaluate_path_box(
                support,
                term_id,
                primary.configuration_variants(term_id),
                epsilon_row,
                "TOP",
                x_lower,
                x_upper,
                t_lower,
                t_upper,
                0,
                f"SELECTOR_UNION_{mapped_cell_id}",
                support_segments,
                branches,
                4,
                False,
            )
            passed.append(
                {
                    "mapped_cell_id": mapped_cell_id,
                    "atlas_cell_id": source_cell["atlas_cell_id"],
                    "term_id": term_id,
                    "x_lower": x_lower,
                    "x_upper": x_upper,
                    "t_lower": t_lower,
                    "t_upper": t_upper,
                    "chart_count": int(enclosure["chart_count"]),
                    "chart_roles": enclosure["chart_roles"],
                    "selected_role": enclosure["selected_role"],
                    "regular_integrand_abs_upper": float(
                        enclosure["regular_integrand_abs_upper"]
                    ),
                    "integrated_regular_path_abs_upper": float(
                        enclosure["integrated_regular_path_abs_upper"]
                    ),
                    "minimum_amplitude_denominator_abs_lower": float(
                        enclosure[
                            "minimum_amplitude_denominator_abs_lower"
                        ]
                    ),
                    "collision_jacobian_abs_lower": float(
                        enclosure["collision_jacobian_abs_lower"]
                    ),
                    "closed_two_chart_smoke_passed": (
                        int(enclosure["chart_count"]) == 2
                        and enclosure["selected_role"] == "CHART_UNION"
                    ),
                }
            )
        except Exception as error:
            failed.append(
                {
                    "mapped_cell_id": mapped_cell_id,
                    "atlas_cell_id": source_cell["atlas_cell_id"],
                    "term_id": term_id,
                    "x_lower": x_lower,
                    "x_upper": x_upper,
                    "t_lower": t_lower,
                    "t_upper": t_upper,
                    "error_type": type(error).__name__,
                    "error": str(error),
                    "closed_two_chart_smoke_passed": False,
                }
            )
    return passed, failed


def validation_row(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": 5397,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def run() -> dict[str, Any]:
    primary = load_primary()
    primary.set_below_normal_priority()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    selector_rows = primary.read_csv(INPUT / "selector_stability_crosschecks.csv")
    transition_rows = [
        row
        for row in selector_rows
        if row["selector_state_matches_cell_midpoint"] != "True"
    ]
    chart_rows = transition_chart_rows(primary, transition_rows)
    closed_rows, failed_rows = closed_union_smoke_rows(
        primary, transition_rows
    )
    source_rows = [
        {
            "path": str(path.relative_to(POST)).replace("\\", "/"),
            "sha256": primary.digest(path),
            "source_exists": path.is_file(),
        }
        for path in (
            Path(__file__).resolve(),
            PRIMARY_PATH,
            INPUT / "selector_stability_crosschecks.csv",
            INPUT / "selector_stability_result.json",
            primary.MAPPED_5393,
        )
    ]
    maximum_chart_error = max(
        float(row["chart_to_parent_relative_error"]) for row in chart_rows
    )
    observed_chart_count = {
        int(row["probe_index"]): sum(
            1
            for candidate in chart_rows
            if int(candidate["probe_index"]) == int(row["probe_index"])
        )
        for row in chart_rows
    }
    all_point_chart_unions_complete = all(
        observed_chart_count[index]
        == len(primary.configuration_variants(row["term_id"]))
        for index, row in enumerate(transition_rows)
    )
    closed_smoke_passed = (
        not failed_rows
        and len(closed_rows)
        == len({(row["mapped_cell_id"], row["term_id"]) for row in transition_rows})
        and all(row["closed_two_chart_smoke_passed"] for row in closed_rows)
    )
    atlas_migration_authorized = False
    validations = [
        validation_row(
            "all_sources_exist_and_are_hashed",
            all(row["source_exists"] and row["sha256"] for row in source_rows),
            len(source_rows),
        ),
        validation_row(
            "historical_selector_transition_count_is_reproduced",
            len(transition_rows) == 15,
            len(transition_rows),
        ),
        validation_row(
            "every_transition_state_is_a_declared_chart_variant",
            all(
                row["observed_state_is_declared_chart_variant"] == "True"
                for row in transition_rows
            ),
            len(transition_rows),
        ),
        validation_row(
            "every_transition_probe_evaluates_the_complete_chart_union",
            all_point_chart_unions_complete,
            len(chart_rows),
        ),
        validation_row(
            "both_chart_representatives_match_the_parent_at_transitions",
            all(row["chart_equivalent_to_parent"] for row in chart_rows),
            maximum_chart_error,
        ),
        validation_row(
            "closed_two_chart_smokes_are_finite",
            closed_smoke_passed,
            f"passed={len(closed_rows)};failed={len(failed_rows)}",
        ),
        validation_row(
            "atlas_migration_remains_blocked_until_closed_backfill",
            not atlas_migration_authorized,
            "v39 completed rows have not been silently promoted to two-chart rows",
        ),
    ]
    payload = {
        "checkpoint": 5397,
        "parent_checkpoint": 5396,
        "transition_probe_count": len(transition_rows),
        "transition_state_count": len(
            {
                observed_state_key(row)
                for row in transition_rows
            }
        ),
        "chart_probe_row_count": len(chart_rows),
        "maximum_chart_to_parent_relative_error": maximum_chart_error,
        "all_point_chart_unions_complete": all_point_chart_unions_complete,
        "closed_union_smoke_count": len(closed_rows),
        "closed_union_smoke_failure_count": len(failed_rows),
        "closed_union_smoke_passed": closed_smoke_passed,
        "selector_transition_union_lemma": (
            "If sigma(p) lies in the finite declared chart set C and each "
            "closed chart enclosure supplies |I_c(p)|<=B_c on the box, then "
            "|I_sigma(p)(p)|<=max_{c in C} B_c without a midpoint selector."
        ),
        "valid_for_selector_transition_chart_union_algorithm": (
            all_point_chart_unions_complete
            and all(row["chart_equivalent_to_parent"] for row in chart_rows)
            and closed_smoke_passed
        ),
        "valid_for_atlas_migration": atlas_migration_authorized,
        "claim_boundary": (
            "The finite-union algorithm is tested on transition probes and "
            "small closed boxes. Existing v39 one-chart path rows are not "
            "upgraded until a closed backfill or a closed pre-transition "
            "unit-margin certificate is completed."
        ),
    }
    primary.atomic_csv(OUTPUT / "source_register.csv", source_rows)
    primary.atomic_csv(
        OUTPUT / "selector_transition_chart_equivalence.csv", chart_rows
    )
    if closed_rows:
        primary.atomic_csv(OUTPUT / "closed_chart_union_smokes.csv", closed_rows)
    if failed_rows:
        primary.atomic_csv(
            OUTPUT / "closed_chart_union_smoke_failures.csv", failed_rows
        )
    primary.atomic_csv(VALIDATION, validations)
    primary.atomic_json(OUTPUT / "selector_transition_chart_union_result.json", payload)
    return {**payload, "all_validation_gates_passed": all(row["passed"] for row in validations)}


def main() -> int:
    print(json.dumps(run(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
