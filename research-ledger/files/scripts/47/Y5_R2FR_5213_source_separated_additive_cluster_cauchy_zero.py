from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
SCRIPT_5124 = POST / "scripts" / "Y5_R2FR_5124_crossed_hhh_two_stratum_derivation.py"
RUN_5212 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5212"
    / "runs"
    / "fresh_two_stratum_pilot_v2"
)
TOPOLOGY_5212 = (
    RUN_5212 / "topologies" / "S521213_N0000__E040_A00.json"
)
HISTORICAL_FALSIFICATION = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5084"
    / "stable_nonzero_falsification_audit.csv"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5213"
RESULT_JSON = SOURCE / "source_separated_additive_cluster_cauchy_zero.json"
AUDIT_CSV = SOURCE / "source_separated_cluster_rows.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5213_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5213-Y5-R2FR-source-separated-additive-cluster-Cauchy-zero-theorem.md"
)

MARKER = "MTS_5213_SOURCE_SEPARATED_ADDITIVE_CLUSTER_CAUCHY_ZERO"
REVISION = "parameter-dependent-component-cycle-holomorphy-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
JOB_KEY = "TOP__E040__S521213_N0000__A00__primary24"
EVENT_ID = "S521213_N0000"
ARGUMENT_ID = "E040_A00"
BOUNDARY_NODES = 64
GROUP_ROOT_TOLERANCE = 2.0e-5
MINIMUM_MARGIN_RATIO = 100.0
MINIMUM_BOUNDARY_SEPARATION = 1.0e-8
MINIMUM_KINEMATIC_MAGNITUDE = 1.0e-8


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5077 = load_module(SCRIPT_5077, "mts_5077_for_5213")
M5124 = load_module(SCRIPT_5124, "mts_5124_for_5213")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def finite_complex(value: complex) -> bool:
    return math.isfinite(value.real) and math.isfinite(value.imag)


def additive_components(label: str) -> frozenset[str]:
    if label.startswith(("direct:g1:", "direct:g2:")):
        return frozenset(("direct",))
    if label.startswith(("direct:g3:", "subtraction:soft:")):
        return frozenset(("direct", "subtraction"))
    if label.startswith("subtraction:decay:"):
        return frozenset(("subtraction",))
    return frozenset()


def strict_cross_additive_pair(pair: tuple[str, str]) -> bool:
    first, second = pair
    return bool(
        (
            first.startswith(("direct:g1:", "direct:g2:"))
            and second.startswith("subtraction:decay:")
        )
        or (
            second.startswith(("direct:g1:", "direct:g2:"))
            and first.startswith("subtraction:decay:")
        )
    )


def historical_falsification_audit() -> dict[str, Any]:
    rows: list[dict[str, str]] = []
    strict_counterexamples: list[dict[str, Any]] = []
    with HISTORICAL_FALSIFICATION.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append(row)
            pairs = [
                tuple(str(label) for label in pair)
                for pair in json.loads(row["pairs"])
            ]
            if pairs and all(strict_cross_additive_pair(pair) for pair in pairs):
                strict_counterexamples.append(
                    {
                        "job_key": row["job_key"],
                        "chamber_index": int(row["chamber_index"]),
                        "pairs": [list(pair) for pair in pairs],
                        "residue_magnitude": float(row["residue_magnitude"]),
                    }
                )
    return {
        "source": str(HISTORICAL_FALSIFICATION),
        "source_sha256": digest(HISTORICAL_FALSIFICATION),
        "stable_nonzero_row_count": len(rows),
        "strict_cross_additive_counterexample_count": len(strict_counterexamples),
        "strict_cross_additive_counterexamples": strict_counterexamples,
        "passed": bool(rows) and not strict_counterexamples,
    }


def boundary_regularity(
    row: dict[str, Any],
    ownership: dict[str, bool],
    module: Any,
    selected_labels: set[str],
    certificate_radius: float,
) -> dict[str, Any]:
    root = complex(row["root"])
    minimum_energy = math.inf
    minimum_inverse_energy_square_sum = math.inf
    minimum_selected_root_modulus = math.inf
    maximum_selected_root_modulus = 0.0
    minimum_same_component_separation = math.inf
    finite = True
    for index in range(BOUNDARY_NODES):
        phase = np.exp(2.0j * np.pi * (index + 0.317) / BOUNDARY_NODES)
        relative_circle = root + certificate_radius * phase
        soft_direction, decay_direction, internal = module.M5028.event_geometry(
            module.SOFT_ENERGY,
            complex(module.SOFT_COSINE, 0.0),
            complex(module.DECAY_COSINE, 0.0),
            relative_circle,
        )
        energies = [complex(momentum[0]) for momentum in internal]
        inverse_energy_square_sum = sum(1.0 / energy**2 for energy in energies)
        minimum_energy = min(minimum_energy, *(abs(value) for value in energies))
        minimum_inverse_energy_square_sum = min(
            minimum_inverse_energy_square_sum,
            abs(inverse_energy_square_sum),
        )
        sources = module.M5028.source_directions(
            internal, soft_direction, decay_direction
        )
        factor_roots: dict[str, complex] = {}
        for source, direction in sources.items():
            for suffix, value in module.M5028.M5026.M5024.all_factor_roots(
                direction, module.TARGET_COSINE
            ).items():
                factor_roots[f"{source}:{suffix}"] = complex(value)
        for label in selected_labels:
            selected_root = factor_roots[label]
            minimum_selected_root_modulus = min(
                minimum_selected_root_modulus, abs(selected_root)
            )
            maximum_selected_root_modulus = max(
                maximum_selected_root_modulus, abs(selected_root)
            )
            finite = finite and finite_complex(selected_root)
            for other_label, other_root in factor_roots.items():
                if other_label == label:
                    continue
                if not (
                    additive_components(label)
                    & additive_components(other_label)
                ):
                    continue
                separation = abs(selected_root - other_root) / max(
                    1.0, abs(selected_root), abs(other_root)
                )
                minimum_same_component_separation = min(
                    minimum_same_component_separation, separation
                )
        finite = finite and all(finite_complex(value) for value in energies)
        finite = finite and finite_complex(inverse_energy_square_sum)
    return {
        "boundary_nodes": BOUNDARY_NODES,
        "certificate_radius": certificate_radius,
        "minimum_internal_energy_magnitude": minimum_energy,
        "minimum_inverse_energy_square_sum_magnitude": (
            minimum_inverse_energy_square_sum
        ),
        "minimum_selected_global_root_modulus": minimum_selected_root_modulus,
        "maximum_selected_global_root_modulus": maximum_selected_root_modulus,
        "minimum_same_component_global_root_separation": (
            minimum_same_component_separation
        ),
        "all_boundary_values_finite": finite,
    }


def source_separated_cluster_certificate(
    row: dict[str, Any],
    ownership: dict[str, bool],
    module: Any,
    job_key: str,
    historical: dict[str, Any] | None = None,
) -> dict[str, Any]:
    history = historical_falsification_audit() if historical is None else historical
    root = complex(row["root"])
    pairs = [tuple(str(label) for label in pair) for pair in row["pairs"]]
    labels = {label for pair in pairs for label in pair}
    selected_labels = {
        label for label in labels if bool(ownership.get(label, False))
    }
    _, collision_rows = module.M5029.all_collision_rows(
        module.SOFT_ENERGY,
        module.SOFT_COSINE,
        module.DECAY_COSINE,
        module.TARGET_COSINE,
    )
    pair_root_rows: list[dict[str, Any]] = []
    for pair in pairs:
        matches = [
            candidate
            for candidate in collision_rows
            if set(candidate["pair"]) == set(pair)
        ]
        if not matches:
            pair_root_rows.append(
                {
                    "pair": list(pair),
                    "matched": False,
                    "root_relative_residual": math.inf,
                }
            )
            continue
        match = min(
            matches, key=lambda candidate: abs(complex(candidate["root"]) - root)
        )
        matched_root = complex(match["root"])
        pair_root_rows.append(
            {
                "pair": list(pair),
                "matched": True,
                "matched_root": complex_row(matched_root),
                "root_relative_residual": abs(matched_root - root)
                / max(1.0, abs(root), abs(matched_root)),
            }
        )

    same_component_collisions: list[dict[str, Any]] = []
    for candidate in collision_rows:
        first, second = tuple(str(label) for label in candidate["pair"])
        if not ({first, second} & selected_labels):
            continue
        if not (additive_components(first) & additive_components(second)):
            continue
        candidate_root = complex(candidate["root"])
        same_component_collisions.append(
            {
                "pair": [first, second],
                "root": complex_row(candidate_root),
                "distance": abs(candidate_root - root),
            }
        )
    nearest_same_component = min(
        same_component_collisions,
        key=lambda candidate: float(candidate["distance"]),
        default=None,
    )
    nearest_same_component_distance = (
        float(nearest_same_component["distance"])
        if nearest_same_component is not None
        else math.inf
    )
    analytic_margin = min(abs(root), nearest_same_component_distance)
    outer_radius = float(row["outer_radius"])
    certificate_radius = min(
        0.05 * analytic_margin,
        max(4.0 * outer_radius, 1.0e-6 * analytic_margin),
    )
    regularity = boundary_regularity(
        row,
        ownership,
        module,
        selected_labels,
        certificate_radius,
    )
    maximum_pair_root_residual = max(
        (
            float(candidate["root_relative_residual"])
            for candidate in pair_root_rows
        ),
        default=math.inf,
    )
    margin_ratio = analytic_margin / max(outer_radius, 1.0e-300)
    guards = {
        "job_key_present": bool(job_key),
        "pairs_present": bool(pairs),
        "all_pairs_are_direct_g1_g2_vs_subtraction_decay": all(
            strict_cross_additive_pair(pair) for pair in pairs
        ),
        "every_pair_has_exactly_one_owned_label": all(
            sum(bool(ownership.get(label, False)) for label in pair) == 1
            for pair in pairs
        ),
        "selected_labels_present": bool(selected_labels),
        "relative_collision_is_not_chart_origin": abs(root) > 1.0e-8,
        "all_grouped_pair_roots_matched": all(
            bool(candidate["matched"]) for candidate in pair_root_rows
        ),
        "grouped_pair_root_residual_within_transport_tolerance": (
            maximum_pair_root_residual < GROUP_ROOT_TOLERANCE
        ),
        "same_summand_collision_catalogue_nonempty": bool(
            same_component_collisions
        ),
        "same_summand_singularities_outside_local_disk": (
            margin_ratio > MINIMUM_MARGIN_RATIO
            and certificate_radius > outer_radius
            and certificate_radius < analytic_margin
        ),
        "boundary_kinematics_regular": (
            float(regularity["minimum_internal_energy_magnitude"])
            > MINIMUM_KINEMATIC_MAGNITUDE
            and float(
                regularity[
                    "minimum_inverse_energy_square_sum_magnitude"
                ]
            )
            > MINIMUM_KINEMATIC_MAGNITUDE
        ),
        "selected_global_roots_finite_nonzero": (
            bool(regularity["all_boundary_values_finite"])
            and float(regularity["minimum_selected_global_root_modulus"])
            > 1.0e-10
            and float(regularity["maximum_selected_global_root_modulus"])
            < 1.0e8
        ),
        "same_summand_global_poles_separated_on_boundary": (
            float(
                regularity[
                    "minimum_same_component_global_root_separation"
                ]
            )
            > MINIMUM_BOUNDARY_SEPARATION
        ),
        "historical_stable_nonzero_falsification_has_no_in_scope_row": bool(
            history["passed"]
        ),
    }
    return {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "job_key": job_key,
        "root": complex_row(root),
        "pairs": [list(pair) for pair in pairs],
        "selected_owned_labels": sorted(selected_labels),
        "pair_root_rows": pair_root_rows,
        "maximum_grouped_pair_root_relative_residual": (
            maximum_pair_root_residual
        ),
        "nearest_same_summand_collision": nearest_same_component,
        "nearest_same_summand_collision_distance": (
            nearest_same_component_distance
        ),
        "analytic_margin": analytic_margin,
        "production_outer_radius": outer_radius,
        "analytic_margin_to_production_radius": margin_ratio,
        "boundary_regularity": regularity,
        "guards": guards,
        "passed": all(guards.values()),
        "analytic_identity": (
            "Write the finite integrand as I(z,q)=D(z,q)-S(z,q). "
            "For each additive summand, the selected global residue sum is a "
            "fixed parameter-dependent Cauchy cycle while no same-summand pole "
            "collision or kinematic singularity enters the certified q disk. "
            "It is therefore holomorphic in q. Cross-additive D/S pole "
            "coincidences cannot singularize either summand. Since q0 is "
            "nonzero, the selected sum divided by q is holomorphic at q0, so "
            "Res_q[(sum Res_z I/z)/q] at q0 equals zero."
        ),
        "catalogue_completeness_assumption": (
            "the finite-z Laurent factor catalogue exhausts the singularities "
            "of each source-separated additive summand in the certified disk"
        ),
        "historical_falsification_source": history["source"],
        "historical_falsification_source_sha256": history["source_sha256"],
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def apply_source_separated_cluster_zero(
    catalog: list[dict[str, Any]],
    ownership: dict[str, bool],
    module: Any,
    job_key: str,
    audit_log: list[dict[str, Any]],
    historical: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], bool]:
    history = historical_falsification_audit() if historical is None else historical
    for row in catalog:
        if bool(row["stable"]):
            continue
        certificate = source_separated_cluster_certificate(
            row, ownership, module, job_key, history
        )
        if not certificate["passed"]:
            continue
        original = {
            "residue_method": str(row["residue_method"]),
            "outer_residue": complex_row(complex(row["outer_residue"])),
            "inner_residue": complex_row(complex(row["inner_residue"])),
            "residue": complex_row(complex(row["residue"])),
            "residue_stability": float(row["residue_stability"]),
            "numerically_zero": bool(row["numerically_zero"]),
            "stable": bool(row["stable"]),
        }
        row.update(
            {
                "residue_method": REVISION,
                "outer_residue": 0.0j,
                "inner_residue": 0.0j,
                "residue": 0.0j,
                "residue_stability": 0.0,
                "numerically_zero": True,
                "stable": True,
                "included_as_pole_model": False,
                "source_separated_cluster_zero_certificate": certificate,
            }
        )
        audit_log.append(
            {
                "job_key": job_key,
                "resolution_classification": (
                    "SOURCE_SEPARATED_ADDITIVE_CLUSTER_CAUCHY_ZERO"
                ),
                "root": certificate["root"],
                "pairs": certificate["pairs"],
                "original_numeric_probe": original,
                "certificate": certificate,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return catalog, all(bool(row["stable"]) for row in catalog)


def configured_problem() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], Any]:
    config = json.loads((RUN_5212 / "config.json").read_text(encoding="utf-8"))
    event = next(row for row in config["events"] if row["event_id"] == EVENT_ID)
    argument = next(
        row for row in config["arguments"] if row["argument_id"] == ARGUMENT_ID
    )
    topology = json.loads(TOPOLOGY_5212.read_text(encoding="utf-8"))
    target = M5077.M5036.complex_from_row(argument["target_cosine"])
    M5077.CURRENT_EVENT = event
    M5077.CURRENT_ARGUMENT = argument
    M5077.M5036.M5035.M5034.configure(event, target)
    return config, event, argument, topology


def run_gate() -> dict[str, Any]:
    config, event, argument, topology = configured_problem()
    del event, argument
    module = M5077.M5036.N5030
    profile = config["tiers"]["primary24"]
    historical = historical_falsification_audit()
    captured: list[tuple[dict[str, bool], list[dict[str, Any]]]] = []
    previous_catalog = module.chamber_residue_catalog
    previous_job = M5077.M5036.MREPAIR.CURRENT_JOB

    def capture_catalog(
        ownership: dict[str, bool],
        start: complex,
        end: complex,
        required_roots: list[complex],
        global_nodes: int,
        global_residue_nodes: int,
        relative_residue_nodes: int,
        model_distance: float,
    ) -> tuple[list[dict[str, Any]], bool]:
        catalog, stable = M5077.certified_primary_catalog(
            ownership,
            start,
            end,
            required_roots,
            global_nodes,
            global_residue_nodes,
            relative_residue_nodes,
            model_distance,
        )
        captured.append((ownership, catalog))
        return catalog, stable

    module.chamber_residue_catalog = capture_catalog
    M5077.M5036.MREPAIR.CURRENT_JOB = JOB_KEY
    M5077.M5036.MREPAIR.RADIUS_AUDIT.clear()
    M5077.LOCAL_RESIDUE_RESOLUTION_AUDIT.clear()
    M5077.OUTWARD_CONTOUR_AUDIT.clear()
    M5077.PROJECTIVE_CLUSTER_ZERO_AUDIT.clear()
    try:
        (
            original_topological,
            original_stable,
            original_catalog_rows,
            safe_pair_count,
            unsafe_pair_count,
        ) = M5124.reciprocal_reduced_topological_value(
            module, topology, profile
        )
    finally:
        module.chamber_residue_catalog = previous_catalog
        M5077.M5036.MREPAIR.CURRENT_JOB = previous_job

    unstable: list[dict[str, Any]] = []
    for ownership, catalog in captured:
        for row in catalog:
            if bool(row["stable"]):
                continue
            certificate = source_separated_cluster_certificate(
                row, ownership, module, JOB_KEY, historical
            )
            unstable.append(
                {
                    "root": complex_row(complex(row["root"])),
                    "pairs": [list(pair) for pair in row["pairs"]],
                    "outer_residue": complex_row(complex(row["outer_residue"])),
                    "inner_residue": complex_row(complex(row["inner_residue"])),
                    "residue_stability": float(row["residue_stability"]),
                    "certificate": certificate,
                }
            )

    repair_audit: list[dict[str, Any]] = []

    def repaired_catalog(
        ownership: dict[str, bool],
        start: complex,
        end: complex,
        required_roots: list[complex],
        global_nodes: int,
        global_residue_nodes: int,
        relative_residue_nodes: int,
        model_distance: float,
    ) -> tuple[list[dict[str, Any]], bool]:
        catalog, _ = M5077.certified_primary_catalog(
            ownership,
            start,
            end,
            required_roots,
            global_nodes,
            global_residue_nodes,
            relative_residue_nodes,
            model_distance,
        )
        return apply_source_separated_cluster_zero(
            catalog,
            ownership,
            module,
            JOB_KEY,
            repair_audit,
            historical,
        )

    module.chamber_residue_catalog = repaired_catalog
    M5077.M5036.MREPAIR.CURRENT_JOB = JOB_KEY
    M5077.M5036.MREPAIR.RADIUS_AUDIT.clear()
    M5077.LOCAL_RESIDUE_RESOLUTION_AUDIT.clear()
    M5077.OUTWARD_CONTOUR_AUDIT.clear()
    M5077.PROJECTIVE_CLUSTER_ZERO_AUDIT.clear()
    try:
        (
            repaired_topological,
            repaired_stable,
            repaired_catalog_rows,
            repaired_safe_pair_count,
            repaired_unsafe_pair_count,
        ) = M5124.reciprocal_reduced_topological_value(
            module, topology, profile
        )
    finally:
        module.chamber_residue_catalog = previous_catalog
        M5077.M5036.MREPAIR.CURRENT_JOB = previous_job

    formal_hash = tree_digest(FORMAL)
    maximum_group_residual = max(
        float(row["certificate"]["maximum_grouped_pair_root_relative_residual"])
        for row in unstable
    )
    minimum_margin_ratio = min(
        float(row["certificate"]["analytic_margin_to_production_radius"])
        for row in unstable
    )
    checks = [
        (
            "formalization_workbench_unchanged",
            formal_hash == FORMAL_BASELINE,
            formal_hash,
        ),
        (
            "failed_pilot_job_reproduced_as_residue_unstable",
            not original_stable,
            str(original_topological),
        ),
        (
            "exactly_four_unstable_rows_exposed",
            len(unstable) == 4,
            str(len(unstable)),
        ),
        (
            "all_unstable_rows_source_separated_and_certified",
            all(row["certificate"]["passed"] for row in unstable),
            str(sum(row["certificate"]["passed"] for row in unstable)),
        ),
        (
            "grouped_pair_roots_within_transport_tolerance",
            maximum_group_residual < GROUP_ROOT_TOLERANCE,
            str(maximum_group_residual),
        ),
        (
            "same_summand_margin_exceeds_one_hundred_radii",
            minimum_margin_ratio > MINIMUM_MARGIN_RATIO,
            str(minimum_margin_ratio),
        ),
        (
            "historical_601_row_nonzero_corpus_has_no_in_scope_counterexample",
            historical["passed"]
            and historical["stable_nonzero_row_count"] == 601,
            json.dumps(
                {
                    "rows": historical["stable_nonzero_row_count"],
                    "counterexamples": historical[
                        "strict_cross_additive_counterexample_count"
                    ],
                }
            ),
        ),
        (
            "four_exact_zero_replacements_applied",
            len(repair_audit) == 4,
            str(len(repair_audit)),
        ),
        (
            "repaired_reciprocal_reduced_topological_gate_converges",
            repaired_stable,
            str(repaired_topological),
        ),
        (
            "pair_accounting_unchanged",
            (
                original_catalog_rows == repaired_catalog_rows
                and safe_pair_count == repaired_safe_pair_count
                and unsafe_pair_count == repaired_unsafe_pair_count
            ),
            json.dumps(
                {
                    "original_catalog_rows": original_catalog_rows,
                    "repaired_catalog_rows": repaired_catalog_rows,
                    "safe_pairs": repaired_safe_pair_count,
                    "unsafe_pairs": repaired_unsafe_pair_count,
                }
            ),
        ),
        (
            "checkpoint_remains_nonclaim",
            True,
            "numeric_UV=false; local_GR=false; full_MTS=false",
        ),
    ]
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "job_key": JOB_KEY,
        "source_run": str(RUN_5212),
        "source_run_config_sha256": digest(RUN_5212 / "config.json"),
        "source_topology": str(TOPOLOGY_5212),
        "source_topology_sha256": digest(TOPOLOGY_5212),
        "historical_falsification": historical,
        "theorem": (
            "For I=D-S, a selected sum of componentwise global Cauchy "
            "residues is holomorphic in q on any disk excluding same-summand "
            "collisions and kinematic singularities. Cross-additive pole "
            "coincidences are harmless. At nonzero q0 its relative residue "
            "after division by q is exactly zero."
        ),
        "raw_unstable_rows": unstable,
        "source_separated_zero_repair_audit": repair_audit,
        "original_reciprocal_reduced_topological_value": complex_row(
            original_topological
        ),
        "repaired_reciprocal_reduced_topological_value": complex_row(
            repaired_topological
        ),
        "original_residues_stable": original_stable,
        "repaired_residues_stable": repaired_stable,
        "catalog_row_count": repaired_catalog_rows,
        "safe_pair_count": repaired_safe_pair_count,
        "unsafe_pair_count": repaired_unsafe_pair_count,
        "maximum_grouped_pair_root_relative_residual": maximum_group_residual,
        "minimum_same_summand_margin_to_production_radius": (
            minimum_margin_ratio
        ),
        "formalization_workbench_tree_sha256": formal_hash,
        "runner_integration_authorized": all(passed for _, passed, _ in checks),
        "authorized_scope": (
            "on-demand unstable rows whose complete guard set passes; "
            "no same-summand, direct:g3/soft-alias, chart-origin, or "
            "uncatalogued row is promoted"
        ),
        "checks": [
            {"check": name, "passed": bool(passed), "detail": detail}
            for name, passed, detail in checks
        ],
        "passed": all(passed for _, passed, _ in checks),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    return result


def write_outputs(result: dict[str, Any]) -> None:
    atomic_json(RESULT_JSON, result)
    rows = []
    for index, row in enumerate(result["raw_unstable_rows"], start=1):
        certificate = row["certificate"]
        regularity = certificate["boundary_regularity"]
        rows.append(
            {
                "row_index": index,
                "root_real": row["root"]["real"],
                "root_imaginary": row["root"]["imaginary"],
                "pair_count": len(row["pairs"]),
                "selected_owned_labels": json.dumps(
                    certificate["selected_owned_labels"],
                    separators=(",", ":"),
                ),
                "maximum_grouped_pair_root_relative_residual": certificate[
                    "maximum_grouped_pair_root_relative_residual"
                ],
                "nearest_same_summand_collision_distance": certificate[
                    "nearest_same_summand_collision_distance"
                ],
                "production_outer_radius": certificate[
                    "production_outer_radius"
                ],
                "analytic_margin_to_production_radius": certificate[
                    "analytic_margin_to_production_radius"
                ],
                "minimum_boundary_same_summand_root_separation": regularity[
                    "minimum_same_component_global_root_separation"
                ],
                "certificate_passed": certificate["passed"],
                "valid_for_numeric_UV_claim": False,
            }
        )
    AUDIT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=("check", "passed", "detail")
        )
        writer.writeheader()
        writer.writerows(result["checks"])
    document = f"""# 5213 — Source-separated additive-cluster Cauchy zero theorem

## Decision

The first fresh `5212` topological failure is **not** repaired by loosening
the residue-stability tolerance. Its four unstable rows satisfy an exact,
guarded zero theorem. The repaired reciprocal-reduced gate converges, but
this remains a non-claim support checkpoint.

## Derivation

Write the finite integrand as

`I(z,q) = D(z,q) - S(z,q)`.

For one additive summand `X in {{D,S}}`, let `C_X` be a fixed union of small
global contours enclosing the causally selected poles. On a relative
`q`-disk containing no same-summand pole collision, chart origin, or
kinematic singularity,

`R_X(q) = (1/(2 pi i)) integral_(C_X) X(z,q) dz/z`

is holomorphic in `q` by the parameter-dependent Cauchy theorem. A pole of
`D` may coincide with a pole of `S` without singularizing either additive
summand. Therefore `R_D(q)-R_S(q)` remains holomorphic through every guarded
cross-additive cluster. Since the collision centre `q0` is nonzero,

`Res_(q=q0) [(R_D(q)-R_S(q))/q] = 0`.

This is the exact zero inserted by the repair. It is not a fitted value and
does not use the failed double-precision contour estimate.

## Fresh failure audit

- Unstable rows: `{len(result['raw_unstable_rows'])}`.
- Certified exact-zero rows: `{len(result['source_separated_zero_repair_audit'])}`.
- Largest grouped-root residual: `{result['maximum_grouped_pair_root_relative_residual']:.6e}`.
- Smallest same-summand margin in production contour radii:
  `{result['minimum_same_summand_margin_to_production_radius']:.6e}`.
- Historical stable-nonzero rows checked:
  `{result['historical_falsification']['stable_nonzero_row_count']}`.
- In-scope historical counterexamples:
  `{result['historical_falsification']['strict_cross_additive_counterexample_count']}`.
- Raw topological value:
  `{result['original_reciprocal_reduced_topological_value']}`.
- Certified repaired topological value:
  `{result['repaired_reciprocal_reduced_topological_value']}`.
- Repaired residue gate converged: `{result['repaired_residues_stable']}`.

## Scope discipline

The theorem rejects same-summand pairs, the `direct:g3/subtraction:soft`
alias, chart-origin collisions, incomplete pair-root matches, insufficient
same-summand margins, irregular boundary kinematics, and any row outside
the finite-factor catalogue. The historical 601-row stable-nonzero corpus
contains no row in the authorized strict scope.

This proves only the four guarded local residue zeros and authorizes the
same complete on-demand guard set in the `5212` runner. It does **not**
complete the fresh coefficient pilot and does not support a numeric UV,
local-GR, or full-MTS claim.

## Machine-readable evidence

- `{RESULT_JSON}`
- `{AUDIT_CSV}`
- `{VALIDATION_CSV}`
- Source topology: `{TOPOLOGY_5212}`
- Historical falsification corpus: `{HISTORICAL_FALSIFICATION}`
"""
    atomic_text(DOCUMENT, document)


def main() -> None:
    required = (
        SCRIPT_5077,
        SCRIPT_5124,
        RUN_5212 / "config.json",
        TOPOLOGY_5212,
        HISTORICAL_FALSIFICATION,
        FORMAL,
    )
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    result = run_gate()
    write_outputs(result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["passed"]:
        raise RuntimeError("5213 source-separated Cauchy zero gate failed")


if __name__ == "__main__":
    main()
