from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5327"

SCRIPT_5326 = SCRIPTS / "Y5_R2FR_5326_D2_midpoint_event_aligned_E0025_refinement.py"
SCRIPT_5330 = SCRIPTS / "Y5_R2FR_5330_E040_adaptive_owner_channel_divisor.py"
RESULT_5330 = FUNCTIONAL_RG / "5330" / "E040_adaptive_divisor_result.json"
VALIDATION_5330 = FUNCTIONAL_RG / "5330" / "E040_adaptive_divisor_validation.csv"
CERTIFICATES_5330 = FUNCTIONAL_RG / "5330" / "E040_adaptive_divisor_certificates.csv"
FITS_5330 = FUNCTIONAL_RG / "5330" / "E040_adaptive_divisor_fits.csv"
ADAPTIVE_DIVISOR_RUNTIME = SOURCE / "E040" / "adaptive-divisor-runtime"
RESULT_5326 = FUNCTIONAL_RG / "5326" / "D2_midpoint_event_aligned_E0025_refinement_result.json"
VALIDATION_5326 = FUNCTIONAL_RG / "5326" / "D2_midpoint_event_aligned_E0025_refinement_validation.csv"
FINITE_5326 = FUNCTIONAL_RG / "5326" / "D2_midpoint_event_aligned_E0025_finite_value.csv"

LADDER = SOURCE / "D2_midpoint_finite_regulator_ladder.csv"
PAIRWISE = SOURCE / "D2_midpoint_finite_regulator_pairwise_convergence.csv"
TRENDS = SOURCE / "D2_midpoint_finite_regulator_three_point_trends.csv"
RESULT = SOURCE / "D2_midpoint_regulator_ladder_controller_result.json"
VALIDATION = SOURCE / "D2_midpoint_regulator_ladder_controller_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5327_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5327-Y5-R2FR-D2-midpoint-regulator-ladder-controller.md"

CHECKPOINT = 5327
PARENT_CHECKPOINT = 5326
MARKER = "MTS_5327_D2_MIDPOINT_REGULATOR_LADDER_CONTROLLER"
REVISION = "D2-midpoint-regulator-ladder-controller-v5"
EPSILON_VALUES = {
    "E000625": 0.000625,
    "E00125": 0.00125,
    "E0025": 0.0025,
    "E005": 0.005,
    "E010": 0.01,
    "E020": 0.02,
    "E040": 0.04,
}
EXPECTED_IDS = tuple(EPSILON_VALUES)
RUN_IDS = tuple(value for value in EXPECTED_IDS if value != "E0025")
GLOBAL_ERROR_BUDGET_LIMIT = 1.0e-2
SELECTOR_RECIPROCAL_RESIDUAL_TRIGGER = 1.0e-6
SELECTOR_CANDIDATE_SEED_COLLISION_RESIDUAL_LIMIT = 1.0e-6
SELECTOR_RECIPROCAL_PAIR_SEED_RESIDUAL_LIMIT = 1.0e-8
SELECTOR_REFINEMENT_CHORDAL_DISTANCE_LIMIT = 1.0e-6
SELECTOR_REFINED_COLLISION_RESIDUAL_LIMIT = 1.0e-20
SELECTOR_REFINED_RECIPROCAL_PAIR_RESIDUAL_LIMIT = 1.0e-20
E000625_NEAR_SUPPORT_DISTANCE_CORE_LIMIT = 32.0
E000625_INTERIOR_FIT_IMAGINARY_CORE_MULTIPLIER = 32.0
E000625_INTERIOR_FIT_SUPPORT_SAFETY = 0.8
E000625_REPAIR_REVISION = "E000625-one-sided-plus-symmetric-interior-laurent-v3"
TOPOLOGY_SAFE_REPAIR_REVISION = "D2-topology-safe-symmetric-interior-laurent-v4"
INTERIOR_TOPOLOGY_MAXIMUM_RADIUS_HALVINGS = 8
INTERIOR_TOPOLOGY_MINIMUM_IMAGINARY_CORE_MULTIPLIER = 1.0
INTERIOR_TOPOLOGY_LINEAR_GUARD_COUNT = 64
INTERIOR_TOPOLOGY_GEOMETRIC_GUARD_DEPTH = 12
E020_EXTENDED_ENERGY_NODE_IDS = (
    "P01_P01S01_Q08_N01",
    "P10_P10S02LLL_Q08_N01",
)
E020_EXTENDED_ENERGY_SUBDIVISIONS = (256, 512)
E020_EXTENDED_ENERGY_REPAIR_REVISION = "E020-energy-256-512-v1"
E020_DIRECT_CONTOUR_FALLBACK_NODE_IDS = (
    "P10_P10S02LLL_Q08_N01",
)
E020_DIRECT_CONTOUR_FALLBACK_REASON = (
    "OFF_AXIS_POLE_RESIDUE_UNRESOLVED__DIRECT_REAL_CONTOUR_REFINEMENT"
)
OFF_SUPPORT_ENERGY_SUBDIVISIONS = (64, 128, 256, 512)
OFF_SUPPORT_ENERGY_REPAIR_REVISION = "D2-off-support-real-axis-quadrature-v1"
OFF_SUPPORT_ENERGY_FALLBACK_REASON = (
    "TOPOLOGY_SAFE_NEAR_SUPPORT_FIT_UNAVAILABLE__NO_IN_SUPPORT_POLE"
)
E020_TOPOLOGY_REPAIR_NODE_IDS = (
    "P08_P08S03_Q04_N01",
    "P08_P08S03_Q04_N02",
    "P08_P08S03_Q04_N03",
    "P08_P08S03_Q04_N04",
    "P08_P08S03_Q08_N01",
    "P08_P08S03_Q08_N02",
    "P08_P08S03_Q08_N03",
    "P08_P08S03_Q08_N04",
    "P08_P08S03_Q08_N05",
    "P08_P08S03_Q08_N06",
    "P08_P08S03_Q08_N07",
    "P08_P08S04_Q04_N01",
    "P08_P08S04_Q04_N02",
    "P08_P08S04_Q04_N03",
    "P08_P08S04_Q04_N04",
    "P08_P08S04_Q08_N01",
    "P08_P08S04_Q08_N02",
)
E000625_REQUIRED_LOCAL_REPAIR_MODES = {
    "P01_P01S01_Q08_N01": "ONE_SIDED_ACTIVE_SUPPORT",
    "P08_P08S01_Q08_N05": "SYMMETRIC_INTERIOR_COMPLEX_POLE",
}
REQUIRED_LOCAL_REPAIR_MODES_BY_EPSILON = {
    "E000625": E000625_REQUIRED_LOCAL_REPAIR_MODES,
    "E010": {
        "P08_P08S02_Q04_N02": "SYMMETRIC_INTERIOR_COMPLEX_POLE",
    },
    "E020": {
        node_id: "SYMMETRIC_INTERIOR_COMPLEX_POLE"
        for node_id in E020_TOPOLOGY_REPAIR_NODE_IDS
    },
}
REQUIRED_LOCAL_REPAIR_REVISION_BY_EPSILON = {
    "E000625": E000625_REPAIR_REVISION,
    "E010": E000625_REPAIR_REVISION,
    "E020": TOPOLOGY_SAFE_REPAIR_REVISION,
}
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
CLAIM_FIELDS = (
    "valid_for_D2_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5326 = load_module("mts_5326_for_5327", SCRIPT_5326)
M5283 = M5326.M5283
M5279 = M5326.M5312.M5280.M5279
M5275 = M5326.M5312.M5280.M5275
ORIGINAL_ALGEBRAIC_COMPONENT_SELECTOR = M5279.algebraic_component_selector
ORIGINAL_SYNTHETIC_CONTEXT = M5326.M5312.M5303.synthetic_context
ORIGINAL_NEAR_SUPPORT_LAURENT_FIT = M5326.near_support_laurent_fit
ORIGINAL_REFINE_NEAR_SUPPORT_SIMPLE_POLE = M5326.refine_near_support_simple_pole
ORIGINAL_NEAR_SUPPORT_DISTANCE_CORE_LIMIT = M5326.NEAR_SUPPORT_DISTANCE_CORE_LIMIT
ORIGINAL_NEAR_SUPPORT_REPAIR_REVISION = M5326.NEAR_SUPPORT_REPAIR_REVISION
ORIGINAL_REPAIR_NODE_ENERGY_RESOLUTION = M5326.repair_node_energy_resolution
ORIGINAL_FIT_NODE_POLES = M5326.M5312.fit_node_poles
ACTIVE_SELECTOR_EPSILON_ID: str | None = None
ACTIVE_TARGET_EPSILON_ID: str | None = None
SELECTOR_REPAIR_ROWS: dict[tuple[str, ...], dict[str, Any]] = {}
INTERIOR_FIT_DIAGNOSTICS: dict[tuple[float, ...], dict[str, Any]] = {}
OWNER_CHANNEL_CERTIFICATE_BYPASS = False
OWNER_CHANNEL_CERTIFICATE_ROWS: dict[tuple[str, str, str], dict[str, str]] = {}
OWNER_CHANNEL_CERTIFICATE_FIT_ROWS: dict[tuple[str, str, str], list[dict[str, str]]] = {}
OWNER_CHANNEL_CERTIFICATE_SHA256 = ""
ADAPTIVE_DIVISOR_MODULE: Any | None = None
ADAPTIVE_DIVISOR_EVALUATE: Any | None = None
ADAPTIVE_DIVISOR_RUNTIME_CERTIFICATES: dict[
    tuple[str, str, str], dict[str, Any]
] = {}


def read_csv(path: Path) -> list[dict[str, str]]:
    return M5326.read_csv(path)


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    leading_fields: list[str] | None = None,
) -> None:
    M5326.write_csv(path, rows, leading_fields)


def read_json(path: Path) -> dict[str, Any]:
    return M5326.read_json(path)


def atomic_json(path: Path, value: Any) -> None:
    M5326.atomic_json(path, value)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_bool(value: Any) -> bool:
    return M5326.parse_bool(value)


def owner_channel_certificate_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return str(row["node_id"]), str(row["term_id"]), str(row["pole_id"])


def load_validated_owner_channel_certificate() -> tuple[
    dict[tuple[str, str, str], dict[str, str]],
    dict[tuple[str, str, str], list[dict[str, str]]],
    str,
]:
    required = (RESULT_5330, VALIDATION_5330, CERTIFICATES_5330, FITS_5330)
    if not all(path.exists() for path in required):
        raise RuntimeError("checkpoint 5330 adaptive-divisor certificate is missing")
    result = read_json(RESULT_5330)
    validation = read_csv(VALIDATION_5330)
    certificates = read_csv(CERTIFICATES_5330)
    fits = read_csv(FITS_5330)
    source_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    if not (
        bool(result["acceptance_passed"])
        and validation
        and all(parse_bool(row["passed"]) for row in validation)
        and source_current
        and len(certificates) == 30
        and bool(result["all_families_agree_with_resolved_history"])
        and all(
            parse_bool(row["adaptive_divisor_controls_pass"])
            and parse_bool(row["pole_classification_resolved"])
            and parse_bool(row["valid_for_E040_node_rerun"])
            for row in certificates
        )
    ):
        raise RuntimeError("checkpoint 5330 adaptive-divisor certificate is not valid")
    certificate_lookup = {
        owner_channel_certificate_key(row): row for row in certificates
    }
    all_fit_rows: dict[tuple[str, str, str], list[dict[str, str]]] = {}
    for row in fits:
        all_fit_rows.setdefault(owner_channel_certificate_key(row), []).append(row)
    fit_lookup: dict[tuple[str, str, str], list[dict[str, str]]] = {}
    for key, rows in all_fit_rows.items():
        maximum_degree = max(int(row["background_polynomial_degree"]) for row in rows)
        fit_lookup[key] = [
            row
            for row in rows
            if int(row["background_polynomial_degree"]) == maximum_degree
        ]
    if set(fit_lookup) != set(certificate_lookup):
        raise RuntimeError("checkpoint 5330 fit and certificate keys differ")
    return certificate_lookup, fit_lookup, digest(CERTIFICATES_5330)


def adaptive_divisor_component_evaluator(
    base_context: dict[str, Any],
) -> Any:
    cache: dict[tuple[float, float, int, int], dict[str, Any]] = {}
    contexts: dict[tuple[float, int, int], dict[str, Any]] = {}

    def evaluate(
        energy: float,
        coordinate: float,
        soft_sign: int,
        decay_sign: int,
    ) -> dict[str, Any]:
        key = (float(energy), float(coordinate), soft_sign, decay_sign)
        if key in cache:
            return cache[key]
        context_key = (float(coordinate), soft_sign, decay_sign)
        if context_key not in contexts:
            contexts[context_key] = M5326.M5312.M5308.M5302.local_context(
                base_context,
                coordinate,
                soft_sign,
                decay_sign,
            )
        context = contexts[context_key]
        event = dict(context["source_event"])
        event["soft_energy"] = energy
        target = context["inventories"]["E040"]["target"]
        rationals = M5326.M5312.M5280.M5274.M5231.root_rationals(
            event,
            target,
        )
        cache[key] = M5326.M5312.M5280.evaluate_component(
            event,
            "E040",
            "MC04",
            context,
            rationals=rationals,
            convergence_audit=True,
        )
        return cache[key]

    return evaluate


def adaptive_owner_channel_function(
    row: dict[str, Any],
) -> Any:
    coordinate = float(row["absolute_soft_cosine"])
    soft_sign = int(row["soft_sign"])
    decay_sign = int(row["decay_sign"])
    problem = M5326.M5312.M5311.synthetic_energy_problem(
        "MC04",
        soft_sign * coordinate,
        decay_sign * M5326.M5312.M5308.M5302.EDGE_DECAY_ABSOLUTE,
    )
    surface_id = str(row["primary_surface_id"])
    return lambda energy: complex(
        M5326.M5312.M5291.M5267.M5239.owner_surface_values(
            problem,
            complex(energy),
        )[surface_id]
    )


def persist_adaptive_divisor_runtime_outcome(
    key: tuple[str, str, str],
    outcome: dict[str, Any],
) -> None:
    if ADAPTIVE_DIVISOR_MODULE is None:
        raise RuntimeError("adaptive divisor module is not configured")
    node_id, term_id, pole_id = key
    target = ADAPTIVE_DIVISOR_RUNTIME / node_id
    stem = f"{term_id}_{pole_id}"
    ADAPTIVE_DIVISOR_MODULE.write_csv(
        target / f"{stem}_root.csv",
        [outcome["root"]],
    )
    ADAPTIVE_DIVISOR_MODULE.write_csv(
        target / f"{stem}_samples.csv",
        outcome["samples"],
    )
    ADAPTIVE_DIVISOR_MODULE.write_csv(
        target / f"{stem}_fits.csv",
        outcome["fits"],
    )
    ADAPTIVE_DIVISOR_MODULE.write_csv(
        target / f"{stem}_certificate.csv",
        [outcome["certificate"]],
    )


def configure_owner_channel_certificate(epsilon_id: str) -> None:
    global OWNER_CHANNEL_CERTIFICATE_ROWS
    global OWNER_CHANNEL_CERTIFICATE_FIT_ROWS
    global OWNER_CHANNEL_CERTIFICATE_SHA256
    global ADAPTIVE_DIVISOR_MODULE
    global ADAPTIVE_DIVISOR_EVALUATE
    global ADAPTIVE_DIVISOR_RUNTIME_CERTIFICATES
    M5326.M5312.fit_node_poles = ORIGINAL_FIT_NODE_POLES
    OWNER_CHANNEL_CERTIFICATE_ROWS = {}
    OWNER_CHANNEL_CERTIFICATE_FIT_ROWS = {}
    OWNER_CHANNEL_CERTIFICATE_SHA256 = ""
    ADAPTIVE_DIVISOR_EVALUATE = None
    ADAPTIVE_DIVISOR_RUNTIME_CERTIFICATES = {}
    if epsilon_id != "E040" or OWNER_CHANNEL_CERTIFICATE_BYPASS:
        return
    if ADAPTIVE_DIVISOR_MODULE is None:
        ADAPTIVE_DIVISOR_MODULE = load_module(
            "mts_5330_adaptive_divisor_for_5327",
            SCRIPT_5330,
        )
    ADAPTIVE_DIVISOR_EVALUATE = adaptive_divisor_component_evaluator(
        M5326.M5312.M5303.synthetic_context()
    )
    (
        OWNER_CHANNEL_CERTIFICATE_ROWS,
        OWNER_CHANNEL_CERTIFICATE_FIT_ROWS,
        OWNER_CHANNEL_CERTIFICATE_SHA256,
    ) = load_validated_owner_channel_certificate()

    def fit_node_poles_with_owner_channel_certificate(
        node: dict[str, Any],
        poles: list[dict[str, Any]],
        evaluate: Any,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        fit_rows, classifications = ORIGINAL_FIT_NODE_POLES(node, poles, evaluate)
        node_id = str(node["node_id"])
        pole_lookup = {owner_channel_certificate_key(row): row for row in poles}
        active_certificates: dict[tuple[str, str, str], dict[str, Any]] = {
            key: row
            for key, row in OWNER_CHANNEL_CERTIFICATE_ROWS.items()
            if key[0] == node_id
        }
        active_fits: dict[tuple[str, str, str], list[dict[str, Any]]] = {
            key: list(OWNER_CHANNEL_CERTIFICATE_FIT_ROWS[key])
            for key in active_certificates
        }
        for row in classifications:
            key = owner_channel_certificate_key(row)
            if (
                key in active_certificates
                or parse_bool(row.get("pole_classification_resolved", False))
                or key not in pole_lookup
            ):
                continue
            outcome = ADAPTIVE_DIVISOR_MODULE.classify_adaptive_pole(
                row,
                pole_lookup[key],
                poles,
                adaptive_owner_channel_function(pole_lookup[key]),
                ADAPTIVE_DIVISOR_EVALUATE,
            )
            persist_adaptive_divisor_runtime_outcome(key, outcome)
            certificate = outcome["certificate"]
            ADAPTIVE_DIVISOR_RUNTIME_CERTIFICATES[key] = certificate
            if not parse_bool(certificate["adaptive_divisor_controls_pass"]):
                continue
            active_certificates[key] = certificate
            maximum_degree = max(
                int(fit["background_polynomial_degree"])
                for fit in outcome["fits"]
            )
            active_fits[key] = [
                fit
                for fit in outcome["fits"]
                if int(fit["background_polynomial_degree"]) == maximum_degree
            ]
        replacement_keys = set(active_certificates)
        if not replacement_keys:
            return fit_rows, classifications
        fit_rows = [
            row
            for row in fit_rows
            if owner_channel_certificate_key(row) not in replacement_keys
        ]
        output_classifications: list[dict[str, Any]] = []
        for row in classifications:
            key = owner_channel_certificate_key(row)
            if key not in replacement_keys:
                output_classifications.append(row)
                continue
            certificate = active_certificates[key]
            runtime_evaluated = key not in OWNER_CHANNEL_CERTIFICATE_ROWS
            certificate_sha256 = (
                digest(SCRIPT_5330)
                if runtime_evaluated
                else OWNER_CHANNEL_CERTIFICATE_SHA256
            )
            residue = complex(
                float(certificate["certified_residue_real"]),
                float(certificate["certified_residue_imaginary"]),
            )
            output_classifications.append(
                {
                    **row,
                    "primary_surface_id": certificate["primary_surface_id"],
                    "pole_real": certificate["refined_pole_real"],
                    "pole_imaginary": certificate["refined_pole_imaginary"],
                    **M5326.complex_fields("selected_residue", residue),
                    "maximum_fit_relative_residual": certificate[
                        "maximum_fit_relative_residual"
                    ],
                    "fit_residue_relative_change": certificate[
                        "certified_residue_relative_spread"
                    ],
                    "all_fit_samples_mask_active": True,
                    "material_simple_pole": parse_bool(
                        certificate["material_simple_pole"]
                    ),
                    "removable_zero_residue_pole": parse_bool(
                        certificate["removable_zero_residue_pole"]
                    ),
                    "pole_classification_resolved": True,
                    "failure_reason": "",
                    "valid_for_pole_subtracted_outer_soft_node": True,
                    "owner_channel_certificate_applied": True,
                    "owner_channel_certificate_checkpoint": 5330,
                    "owner_channel_certificate_sha256": certificate_sha256,
                    "owner_channel_pole_classification": certificate[
                        "pole_classification"
                    ],
                    "adaptive_divisor_runtime_evaluated": runtime_evaluated,
                }
            )
            for fit in active_fits[key]:
                fitted_residue = complex(
                    float(fit["fitted_residue_real"]),
                    float(fit["fitted_residue_imaginary"]),
                )
                fit_rows.append(
                    {
                        "node_id": node_id,
                        "term_id": certificate["term_id"],
                        "support_id": certificate["support_id"],
                        "pole_id": certificate["pole_id"],
                        "fit_scale": fit["fit_scale"],
                        "fit_radius": fit["fit_radius"],
                        "fit_sample_count": fit["fit_sample_count"],
                        "background_polynomial_degree": fit[
                            "background_polynomial_degree"
                        ],
                        **M5326.complex_fields("fitted_residue", fitted_residue),
                        "fit_relative_residual": fit["fit_relative_residual"],
                        "all_fit_samples_mask_active": True,
                        "residue_derivation_method": (
                            "ADAPTIVE_OWNER_CHANNEL_ANALYTIC_DIVISOR"
                        ),
                        "owner_channel_certificate_applied": True,
                        "owner_channel_certificate_checkpoint": 5330,
                        "owner_channel_certificate_sha256": certificate_sha256,
                        "adaptive_divisor_runtime_evaluated": runtime_evaluated,
                        **{field: False for field in M5326.CLAIM_FIELDS},
                    }
                )
        if not replacement_keys.issubset(
            {
                owner_channel_certificate_key(row)
                for row in output_classifications
                if parse_bool(row.get("owner_channel_certificate_applied", False))
            }
        ):
            raise RuntimeError(f"adaptive-divisor replacement incomplete for {node_id}")
        return fit_rows, output_classifications

    M5326.M5312.fit_node_poles = fit_node_poles_with_owner_channel_certificate


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return M5326.validation_gate(gate, passed, detail)


def target_source(epsilon_id: str) -> Path:
    return SOURCE / epsilon_id


def target_paths(epsilon_id: str) -> dict[str, Path]:
    source = target_source(epsilon_id)
    stem = f"D2_midpoint_event_aligned_{epsilon_id}"
    return {
        "source": source,
        "shards": source / "shards",
        "event_candidates": source / "support_event_candidates.csv",
        "event_cache": source / "support_event_state_cache.json",
        "event_states": source / "support_event_state_scan.csv",
        "events": source / "refined_support_events.csv",
        "initial_plan": source / "event_aligned_initial_plan.csv",
        "dry_run": source / f"{stem}_dry_run.json",
        "node_manifest": source / f"{stem}_node_manifest.csv",
        "adaptive_panels": source / f"{stem}_adaptive_panels.csv",
        "poles": source / f"{stem}_geometric_poles.csv",
        "fits": source / f"{stem}_pole_residue_fits.csv",
        "classifications": source / f"{stem}_pole_classification.csv",
        "cell_integrals": source / f"{stem}_cell_integrals.csv",
        "energy_repairs": source / "targeted_energy_partition_repairs.csv",
        "near_repairs": source / "active_support_pole_subtraction_repairs.csv",
        "near_fits": source / "active_support_pole_fits.csv",
        "near_identities": source / "active_support_masked_identity.csv",
        "selector_repairs": source / "algebraic_selector_repairs.csv",
        "inventory_audit": source / "synthetic_regulator_inventory_extension_audit.csv",
        "finite": source / f"{stem}_finite_value.csv",
        "result": source / f"{stem}_result.json",
        "validation": source / f"{stem}_validation.csv",
        "residual_validation": RESIDUALS / f"P8_Y5_BRR545_5327_{epsilon_id}_VALIDATION.csv",
        "status": source / "status.json",
        "document": source / f"{stem}.md",
    }


def stable_value_digest(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def extended_synthetic_context() -> dict[str, Any]:
    context = ORIGINAL_SYNTHETIC_CONTEXT()
    inventories = dict(context["inventories"])
    component_map = inventories["E020"]["components"]
    for epsilon_id, epsilon in EPSILON_VALUES.items():
        if epsilon_id in inventories:
            continue
        target = complex(-9.0, epsilon)
        inventories[epsilon_id] = {
            "target": target,
            "high_precision_target": M5275.target_as_mp(target),
            "components": component_map,
        }
    context["inventories"] = inventories
    return context


def install_synthetic_context_extension() -> None:
    current = M5326.M5312.M5303.synthetic_context
    if getattr(current, "_mts_5327_regulator_extension", False):
        return
    extended_synthetic_context._mts_5327_regulator_extension = True
    M5326.M5312.M5303.synthetic_context = extended_synthetic_context


def write_inventory_extension_audit(
    requested_epsilon_id: str,
    path: Path,
) -> None:
    native = ORIGINAL_SYNTHETIC_CONTEXT()["inventories"]
    extended = extended_synthetic_context()["inventories"]
    source_components = native["E020"]["components"]
    source_digest = stable_value_digest(source_components)
    rows: list[dict[str, Any]] = []
    for epsilon_id, epsilon in EPSILON_VALUES.items():
        inventory = extended[epsilon_id]
        target = complex(inventory["target"])
        component_digest = stable_value_digest(inventory["components"])
        native_target_match = (
            epsilon_id not in native
            or complex(native[epsilon_id]["target"]) == target
        )
        native_component_match = (
            epsilon_id not in native
            or stable_value_digest(native[epsilon_id]["components"])
            == component_digest
        )
        target_passes = (
            target.real == -9.0
            and target.imag == epsilon
        )
        map_passes = component_digest == source_digest
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "requested_epsilon_id": requested_epsilon_id,
                "epsilon_id": epsilon_id,
                "epsilon": epsilon,
                "inventory_origin": (
                    "parent_5303_native"
                    if epsilon_id in native
                    else "checkpoint_5327_exact_target_extension"
                ),
                "target_real": target.real,
                "target_imaginary": target.imag,
                "component_count": len(inventory["components"]),
                "component_map_source_epsilon_id": "E020",
                "component_map_sha256": component_digest,
                "source_component_map_sha256": source_digest,
                "native_target_identity_passes": native_target_match,
                "native_component_identity_passes": native_component_match,
                "target_contract_passes": target_passes,
                "component_map_identity_passes": map_passes,
                "valid_for_regulator_inventory": (
                    native_target_match
                    and native_component_match
                    and target_passes
                    and map_passes
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    write_csv(path, rows, ["requested_epsilon_id", "epsilon_id"])


def selector_repair_key(row: dict[str, Any]) -> tuple[str, ...]:
    return (
        str(row["epsilon_id"]),
        str(row["component_id"]),
        format(float(row["soft_energy"]), ".17g"),
        format(float(row["soft_cosine"]), ".17g"),
        format(float(row["decay_cosine"]), ".17g"),
    )


def initialize_selector_repair_rows(epsilon_id: str) -> None:
    global ACTIVE_SELECTOR_EPSILON_ID
    global SELECTOR_REPAIR_ROWS
    if ACTIVE_SELECTOR_EPSILON_ID == epsilon_id:
        return
    path = target_paths(epsilon_id)["selector_repairs"]
    rows = read_csv(path) if path.exists() else []
    SELECTOR_REPAIR_ROWS = {selector_repair_key(row): dict(row) for row in rows}
    ACTIVE_SELECTOR_EPSILON_ID = epsilon_id


def flush_selector_repair_rows() -> None:
    if ACTIVE_SELECTOR_EPSILON_ID is None or not SELECTOR_REPAIR_ROWS:
        return
    path = target_paths(ACTIVE_SELECTOR_EPSILON_ID)["selector_repairs"]
    rows = sorted(
        SELECTOR_REPAIR_ROWS.values(),
        key=lambda row: (
            float(row["soft_cosine"]),
            float(row["soft_energy"]),
            str(row["component_id"]),
            float(row["decay_cosine"]),
        ),
    )
    write_csv(
        path,
        rows,
        ["epsilon_id", "component_id", "soft_energy", "soft_cosine", "decay_cosine"],
    )


def collision_candidate_residual(
    event: dict[str, Any],
    target: complex,
    labels: tuple[str, str],
    candidate: complex,
) -> tuple[float, float]:
    mp = M5275.mp
    with mp.workdps(M5326.M5312.M5280.MP_DECIMAL_DIGITS):
        high_precision_event = M5275.event_as_mp(event)
        high_precision_target = M5275.target_as_mp(target)
        root = mp.mpc(
            mp.mpf(repr(float(candidate.real))),
            mp.mpf(repr(float(candidate.imag))),
        )
        *_, global_roots = M5275.local_root_data(
            high_precision_event,
            high_precision_target,
            labels,
            root,
        )
        absolute = abs(global_roots[0] - global_roots[1])
        relative = absolute / max(abs(global_roots[0]), abs(global_roots[1]), mp.mpf(1))
    return float(absolute), float(relative)


def refine_collision_candidate(
    event: dict[str, Any],
    target: complex,
    labels: tuple[str, str],
    candidate: complex,
) -> dict[str, Any]:
    mp = M5275.mp
    with mp.workdps(M5326.M5312.M5280.MP_DECIMAL_DIGITS):
        high_precision_event = M5275.event_as_mp(event)
        high_precision_target = M5275.target_as_mp(target)
        refined, reported_residual, distance = M5275.refine_relative_root(
            high_precision_event,
            high_precision_target,
            labels,
            candidate,
        )
        *_, global_roots = M5275.local_root_data(
            high_precision_event,
            high_precision_target,
            labels,
            refined,
        )
        absolute = abs(global_roots[0] - global_roots[1])
        relative = absolute / max(abs(global_roots[0]), abs(global_roots[1]), mp.mpf(1))
    return {
        "root_mp": refined,
        "root": complex(refined),
        "absolute_residual": float(absolute),
        "relative_residual": float(relative),
        "reported_residual": float(reported_residual),
        "refinement_chordal_distance": float(distance),
    }


def record_selector_repair(row: dict[str, Any]) -> None:
    key = selector_repair_key(row)
    if SELECTOR_REPAIR_ROWS.get(key) == row:
        return
    SELECTOR_REPAIR_ROWS[key] = row
    flush_selector_repair_rows()


def selector_repair_passes(row: dict[str, Any]) -> bool:
    try:
        return (
            parse_bool(row["valid_for_selector_repair"])
            and float(row["original_reciprocal_pair_residual"])
            > SELECTOR_RECIPROCAL_RESIDUAL_TRIGGER
            and float(row["corrected_representative_seed_collision_residual_relative"])
            <= SELECTOR_CANDIDATE_SEED_COLLISION_RESIDUAL_LIMIT
            and float(row["corrected_reciprocal_seed_collision_residual_relative"])
            <= SELECTOR_CANDIDATE_SEED_COLLISION_RESIDUAL_LIMIT
            and float(row["corrected_reciprocal_pair_seed_residual"])
            <= SELECTOR_RECIPROCAL_PAIR_SEED_RESIDUAL_LIMIT
            and float(row["corrected_representative_refinement_chordal_distance"])
            <= SELECTOR_REFINEMENT_CHORDAL_DISTANCE_LIMIT
            and float(row["corrected_reciprocal_refinement_chordal_distance"])
            <= SELECTOR_REFINEMENT_CHORDAL_DISTANCE_LIMIT
            and float(row["corrected_selected_collision_residual_relative"])
            <= SELECTOR_REFINED_COLLISION_RESIDUAL_LIMIT
            and float(row["corrected_reciprocal_pair_residual"])
            <= SELECTOR_REFINED_RECIPROCAL_PAIR_RESIDUAL_LIMIT
            and int(row["independently_refined_candidate_pair_count"]) >= 1
        )
    except (KeyError, TypeError, ValueError):
        return False


def guarded_algebraic_component_selector(
    event: dict[str, Any],
    scattering_target: complex,
    component: dict[str, Any],
    rationals: dict[str, Any] | None = None,
) -> dict[str, Any]:
    selection = ORIGINAL_ALGEBRAIC_COMPONENT_SELECTOR(
        event,
        scattering_target,
        component,
        rationals,
    )
    original_pair_residual = float(selection["reciprocal_residual"])
    if original_pair_residual <= SELECTOR_RECIPROCAL_RESIDUAL_TRIGGER:
        return selection
    representative_scores = [
        {
            "root": complex(root),
            "absolute_residual": residual[0],
            "relative_residual": residual[1],
        }
        for root in selection["representative_roots"]
        for residual in [
            collision_candidate_residual(
                event,
                scattering_target,
                selection["representative_labels"],
                complex(root),
            )
        ]
    ]
    reciprocal_scores = [
        {
            "root": complex(root),
            "absolute_residual": residual[0],
            "relative_residual": residual[1],
        }
        for root in selection["reciprocal_roots"]
        for residual in [
            collision_candidate_residual(
                event,
                scattering_target,
                selection["reciprocal_labels"],
                complex(root),
            )
        ]
    ]
    valid_representatives = [
        row
        for row in representative_scores
        if math.isfinite(row["relative_residual"])
        and row["relative_residual"]
        <= SELECTOR_CANDIDATE_SEED_COLLISION_RESIDUAL_LIMIT
    ]
    valid_reciprocals = [
        row
        for row in reciprocal_scores
        if math.isfinite(row["relative_residual"])
        and row["relative_residual"]
        <= SELECTOR_CANDIDATE_SEED_COLLISION_RESIDUAL_LIMIT
    ]
    seed_pairs = [
        {
            "representative_seed": representative,
            "reciprocal_seed": reciprocal,
            "pair_seed_residual": abs(
                representative["root"] * reciprocal["root"] - 1.0
            ),
        }
        for representative in valid_representatives
        for reciprocal in valid_reciprocals
        if abs(representative["root"] * reciprocal["root"] - 1.0)
        <= SELECTOR_RECIPROCAL_PAIR_SEED_RESIDUAL_LIMIT
    ]
    if not seed_pairs:
        raise RuntimeError(
            "5327 selector guard found no refinement-eligible reciprocal seed pair for "
            f"{component['component_id']} at soft_energy={event['soft_energy']!r}, "
            f"soft_cosine={event['soft_cosine']!r}, decay_cosine={event['decay_cosine']!r}"
        )
    refined_pairs: list[dict[str, Any]] = []
    refinement_failures: list[str] = []
    for seed_pair in sorted(
        seed_pairs,
        key=lambda row: (
            row["pair_seed_residual"],
            max(
                row["representative_seed"]["relative_residual"],
                row["reciprocal_seed"]["relative_residual"],
            ),
        ),
    ):
        try:
            representative = refine_collision_candidate(
                event,
                scattering_target,
                selection["representative_labels"],
                seed_pair["representative_seed"]["root"],
            )
            reciprocal = refine_collision_candidate(
                event,
                scattering_target,
                selection["reciprocal_labels"],
                seed_pair["reciprocal_seed"]["root"],
            )
        except Exception as error:
            refinement_failures.append(f"{type(error).__name__}:{error}")
            continue
        refined_pair_residual = float(
            abs(representative["root_mp"] * reciprocal["root_mp"] - 1)
        )
        if (
            representative["relative_residual"]
            <= SELECTOR_REFINED_COLLISION_RESIDUAL_LIMIT
            and reciprocal["relative_residual"]
            <= SELECTOR_REFINED_COLLISION_RESIDUAL_LIMIT
            and representative["refinement_chordal_distance"]
            <= SELECTOR_REFINEMENT_CHORDAL_DISTANCE_LIMIT
            and reciprocal["refinement_chordal_distance"]
            <= SELECTOR_REFINEMENT_CHORDAL_DISTANCE_LIMIT
            and refined_pair_residual
            <= SELECTOR_REFINED_RECIPROCAL_PAIR_RESIDUAL_LIMIT
        ):
            refined_pairs.append(
                {
                    **seed_pair,
                    "representative": representative,
                    "reciprocal": reciprocal,
                    "refined_pair_residual": refined_pair_residual,
                }
            )
    if not refined_pairs:
        raise RuntimeError(
            "5327 selector guard found no independently refined reciprocal pair for "
            f"{component['component_id']} at soft_energy={event['soft_energy']!r}, "
            f"soft_cosine={event['soft_cosine']!r}, decay_cosine={event['decay_cosine']!r}; "
            f"seed_pairs={len(seed_pairs)}; failures={'|'.join(refinement_failures)}"
        )
    selected_pair = min(
        refined_pairs,
        key=lambda row: (
            row["refined_pair_residual"],
            max(
                row["representative"]["relative_residual"],
                row["reciprocal"]["relative_residual"],
            ),
            max(
                row["representative"]["refinement_chordal_distance"],
                row["reciprocal"]["refinement_chordal_distance"],
            ),
        ),
    )
    representative_seed = selected_pair["representative_seed"]
    reciprocal_seed = selected_pair["reciprocal_seed"]
    representative = selected_pair["representative"]
    reciprocal = selected_pair["reciprocal"]
    corrected = dict(selection)
    corrected["representative_root"] = representative["root"]
    corrected["reciprocal_root"] = reciprocal["root"]
    corrected["reciprocal_residual"] = float(selected_pair["refined_pair_residual"])
    corrected["representative_alternate_separation"] = M5279.alternate_separation(
        representative["root"],
        selection["representative_roots"],
    )
    corrected["reciprocal_alternate_separation"] = M5279.alternate_separation(
        reciprocal["root"],
        selection["reciprocal_roots"],
    )
    if abs(representative["root"]) >= 1.0:
        selected = representative
        corrected["selected_role"] = "representative"
        corrected["selected_entry"] = component["representative"]
        corrected["selected_labels"] = selection["representative_labels"]
        corrected["selected_root"] = representative["root"]
        corrected["partner_root"] = reciprocal["root"]
    else:
        selected = reciprocal
        corrected["selected_role"] = "reciprocal"
        corrected["selected_entry"] = component["reciprocal"]
        corrected["selected_labels"] = selection["reciprocal_labels"]
        corrected["selected_root"] = reciprocal["root"]
        corrected["partner_root"] = representative["root"]
    corrected["selected_unit_margin"] = abs(
        math.log(max(abs(corrected["selected_root"]), 1.0e-300))
    )
    original_absolute, original_relative = collision_candidate_residual(
        event,
        scattering_target,
        selection["selected_labels"],
        complex(selection["selected_root"]),
    )
    row = {
        "checkpoint": CHECKPOINT,
        "epsilon_id": ACTIVE_SELECTOR_EPSILON_ID or "UNCONFIGURED",
        "component_id": component["component_id"],
        "soft_energy": float(event["soft_energy"]),
        "soft_cosine": float(event["soft_cosine"]),
        "decay_cosine": float(event["decay_cosine"]),
        "original_selected_role": selection["selected_role"],
        "original_selected_root_real": complex(selection["selected_root"]).real,
        "original_selected_root_imaginary": complex(selection["selected_root"]).imag,
        "original_selected_collision_residual_absolute": original_absolute,
        "original_selected_collision_residual_relative": original_relative,
        "original_reciprocal_pair_residual": original_pair_residual,
        "corrected_representative_seed_collision_residual_relative": representative_seed[
            "relative_residual"
        ],
        "corrected_reciprocal_seed_collision_residual_relative": reciprocal_seed[
            "relative_residual"
        ],
        "corrected_reciprocal_pair_seed_residual": selected_pair[
            "pair_seed_residual"
        ],
        "corrected_representative_root_real": representative["root"].real,
        "corrected_representative_root_imaginary": representative["root"].imag,
        "corrected_representative_collision_residual_relative": representative[
            "relative_residual"
        ],
        "corrected_representative_refinement_chordal_distance": representative[
            "refinement_chordal_distance"
        ],
        "corrected_reciprocal_root_real": reciprocal["root"].real,
        "corrected_reciprocal_root_imaginary": reciprocal["root"].imag,
        "corrected_reciprocal_collision_residual_relative": reciprocal[
            "relative_residual"
        ],
        "corrected_reciprocal_refinement_chordal_distance": reciprocal[
            "refinement_chordal_distance"
        ],
        "corrected_selected_role": corrected["selected_role"],
        "corrected_selected_root_real": complex(corrected["selected_root"]).real,
        "corrected_selected_root_imaginary": complex(corrected["selected_root"]).imag,
        "corrected_selected_collision_residual_absolute": selected[
            "absolute_residual"
        ],
        "corrected_selected_collision_residual_relative": selected[
            "relative_residual"
        ],
        "corrected_reciprocal_pair_residual": float(
            selected_pair["refined_pair_residual"]
        ),
        "collision_valid_candidate_pair_count": len(seed_pairs),
        "independently_refined_candidate_pair_count": len(refined_pairs),
        "valid_for_selector_repair": True,
        **{field: False for field in CLAIM_FIELDS},
    }
    record_selector_repair(row)
    corrected["checkpoint_5327_selector_repair_applied"] = True
    return corrected


def install_selector_guard() -> None:
    current = M5279.algebraic_component_selector
    if getattr(current, "_mts_5327_selector_guard", False):
        return
    guarded_algebraic_component_selector._mts_5327_selector_guard = True
    M5279.algebraic_component_selector = guarded_algebraic_component_selector


def interior_fit_diagnostic_key(
    coordinate: float,
    pole: complex,
    fit_scale: float,
) -> tuple[float, ...]:
    return (
        round(float(coordinate), 15),
        round(float(pole.real), 15),
        round(float(pole.imag), 15),
        round(float(fit_scale), 12),
    )


def interior_topology_guard(
    coordinate: float,
    pole: complex,
    lower: float,
    upper: float,
    radius: float,
    evaluate_unmasked: Any,
) -> dict[str, Any]:
    maximum_unit = max(abs(value) for value in M5326.NEAR_SUPPORT_FIT_UNITS)
    maximum_scale = max(
        1.0,
        *(abs(value) for value in M5326.NEAR_SUPPORT_FIT_SCALES),
    )
    maximum_offset = maximum_unit * maximum_scale * radius
    normalized_offsets = {
        abs(unit * scale) / (maximum_unit * maximum_scale)
        for scale in (1.0, *M5326.NEAR_SUPPORT_FIT_SCALES)
        for unit in M5326.NEAR_SUPPORT_FIT_UNITS
    }
    normalized_offsets.update(
        index / INTERIOR_TOPOLOGY_LINEAR_GUARD_COUNT
        for index in range(1, INTERIOR_TOPOLOGY_LINEAR_GUARD_COUNT + 1)
    )
    normalized_offsets.update(
        2.0 ** (-depth)
        for depth in range(1, INTERIOR_TOPOLOGY_GEOMETRIC_GUARD_DEPTH + 1)
    )
    metadata: list[dict[str, Any]] = []
    for sign in (-1.0, 1.0):
        for normalized_offset in sorted(normalized_offsets):
            energy = pole.real + sign * normalized_offset * maximum_offset
            if not lower < energy < upper:
                return {
                    "interior_topology_preflight_passes": False,
                    "interior_topology_preflight_failure": "GUARD_LEFT_ACTIVE_SUPPORT",
                    "interior_topology_preflight_sample_count": len(metadata),
                }
            metadata.append(evaluate_unmasked(energy, coordinate))
    mask_states = {bool(row["mask_active"]) for row in metadata}
    orientations = {int(row["orientation"]) for row in metadata}
    labels = {str(row["selected_labels"]) for row in metadata}
    roles = {str(row["selected_role"]) for row in metadata}
    passes = (
        mask_states == {True}
        and len(orientations) == 1
        and len(labels) == 1
        and len(roles) == 1
    )
    return {
        "interior_topology_preflight_passes": passes,
        "interior_topology_preflight_failure": (
            "" if passes else "SELECTOR_ORBIT_CHANGES_INSIDE_FIT_NEIGHBOURHOOD"
        ),
        "interior_topology_preflight_sample_count": len(metadata),
        "interior_topology_preflight_mask_state_count": len(mask_states),
        "interior_topology_preflight_orientation_count": len(orientations),
        "interior_topology_preflight_label_count": len(labels),
        "interior_topology_preflight_role_count": len(roles),
    }


def E000625_interior_laurent_fit(
    coordinate: float,
    pole: complex,
    lower: float,
    upper: float,
    fit_scale: float,
    evaluate_unmasked: Any,
) -> dict[str, Any]:
    if M5326.near_support_pole_side(pole, lower, upper) != "INSIDE_SUPPORT":
        return ORIGINAL_NEAR_SUPPORT_LAURENT_FIT(
            coordinate,
            pole,
            lower,
            upper,
            fit_scale,
            evaluate_unmasked,
        )
    boundary_distance = min(pole.real - lower, upper - pole.real)
    if boundary_distance <= 0.0:
        raise RuntimeError("interior Laurent pole is not strictly inside support")
    maximum_unit = max(abs(value) for value in M5326.NEAR_SUPPORT_FIT_UNITS)
    maximum_scale = max(abs(value) for value in M5326.NEAR_SUPPORT_FIT_SCALES)
    support_safe_radius = (
        E000625_INTERIOR_FIT_SUPPORT_SAFETY
        * boundary_distance
        / (maximum_unit * maximum_scale)
    )
    imaginary_core_radius = max(
        E000625_INTERIOR_FIT_IMAGINARY_CORE_MULTIPLIER * abs(pole.imag),
        1.0e-8 * (upper - lower),
        1.0e-12,
    )
    radius = min(imaginary_core_radius, support_safe_radius)
    if radius <= 0.0:
        raise RuntimeError("nonpositive symmetric interior Laurent radius")
    initial_radius = radius
    minimum_radius = max(
        INTERIOR_TOPOLOGY_MINIMUM_IMAGINARY_CORE_MULTIPLIER * abs(pole.imag),
        1.0e-12 * (upper - lower),
        1.0e-15,
    )
    topology_guard: dict[str, Any] = {}
    radius_halving_count = 0
    for radius_halving_count in range(
        INTERIOR_TOPOLOGY_MAXIMUM_RADIUS_HALVINGS + 1
    ):
        topology_guard = interior_topology_guard(
            coordinate,
            pole,
            lower,
            upper,
            radius,
            evaluate_unmasked,
        )
        if bool(topology_guard["interior_topology_preflight_passes"]):
            break
        next_radius = 0.5 * radius
        if next_radius < minimum_radius:
            break
        radius = next_radius
    if not bool(topology_guard.get("interior_topology_preflight_passes", False)):
        raise RuntimeError(
            "no branch-pure symmetric Laurent neighbourhood above the imaginary core"
        )
    matrix_rows: list[list[complex]] = []
    values: list[complex] = []
    metadata: list[dict[str, Any]] = []
    for sign in (-1.0, 1.0):
        for unit in M5326.NEAR_SUPPORT_FIT_UNITS:
            offset = sign * unit * fit_scale * radius
            energy = pole.real + offset
            if not lower < energy < upper:
                raise RuntimeError("symmetric Laurent sample left active support")
            evaluation = evaluate_unmasked(energy, coordinate)
            background_coordinate = offset / radius
            matrix_rows.append(
                [
                    (radius / (energy - pole)) ** 2,
                    radius / (energy - pole),
                    *[
                        complex(background_coordinate**power)
                        for power in range(
                            M5326.NEAR_SUPPORT_FIT_BACKGROUND_DEGREE + 1
                        )
                    ],
                ]
            )
            values.append(evaluation["value"])
            metadata.append(evaluation)
    matrix = M5326.M5312.np.asarray(matrix_rows, dtype=M5326.M5312.np.complex128)
    vector = M5326.M5312.np.asarray(values, dtype=M5326.M5312.np.complex128)
    coefficients, _, _, _ = M5326.M5312.np.linalg.lstsq(
        matrix,
        vector,
        rcond=None,
    )
    predicted = matrix @ coefficients
    residual = float(
        M5326.M5312.np.linalg.norm(predicted - vector)
        / max(M5326.M5312.np.linalg.norm(vector), 1.0)
    )
    diagnostics = {
        "interior_topology_initial_radius": initial_radius,
        "interior_topology_safe_radius": radius,
        "interior_topology_minimum_radius": minimum_radius,
        "interior_topology_radius_halving_count": radius_halving_count,
        **topology_guard,
    }
    INTERIOR_FIT_DIAGNOSTICS[
        interior_fit_diagnostic_key(coordinate, pole, fit_scale)
    ] = diagnostics
    return {
        "fit_scale": fit_scale,
        "fit_radius": radius,
        "fit_sample_count": len(metadata),
        "fit_relative_residual": residual,
        "second_order_coefficient": complex(coefficients[0]) * radius**2,
        "simple_residue": complex(coefficients[1]) * radius,
        "all_fit_samples_mask_active": all(
            bool(row["mask_active"]) for row in metadata
        ),
        "fit_mask_state_count": len(
            {bool(row["mask_active"]) for row in metadata}
        ),
        "fit_mask_states": "|".join(
            sorted({str(bool(row["mask_active"])) for row in metadata})
        ),
        "fit_orientation_count": len(
            {int(row["orientation"]) for row in metadata}
        ),
        "fit_label_count": len(
            {str(row["selected_labels"]) for row in metadata}
        ),
        "fit_role_count": len(
            {str(row["selected_role"]) for row in metadata}
        ),
        "maximum_root_equation_residual": max(
            float(row["root_equation_residual"]) for row in metadata
        ),
        "maximum_root_refinement_chordal_distance": max(
            float(row["root_refinement_chordal_distance"])
            for row in metadata
        ),
        **diagnostics,
    }


def E000625_refine_near_support_simple_pole(
    coordinate: float,
    source: dict[str, Any],
    evaluate_unmasked: Any,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    geometric = complex(float(source["pole_real"]), float(source["pole_imaginary"]))
    fit_geometry_mode = (
        "SYMMETRIC_INTERIOR_COMPLEX_POLE"
        if M5326.near_support_pole_side(
            geometric,
            float(source["support_energy_lower"]),
            float(source["support_energy_upper"]),
        )
        == "INSIDE_SUPPORT"
        else "ONE_SIDED_ACTIVE_SUPPORT"
    )
    selected, rows = ORIGINAL_REFINE_NEAR_SUPPORT_SIMPLE_POLE(
        coordinate,
        source,
        evaluate_unmasked,
    )
    selected["fit_geometry_mode"] = fit_geometry_mode
    for row in rows:
        row["fit_geometry_mode"] = fit_geometry_mode
        row["interior_fit_imaginary_core_multiplier"] = (
            E000625_INTERIOR_FIT_IMAGINARY_CORE_MULTIPLIER
            if fit_geometry_mode == "SYMMETRIC_INTERIOR_COMPLEX_POLE"
            else ""
        )
        row["interior_fit_support_safety"] = (
            E000625_INTERIOR_FIT_SUPPORT_SAFETY
            if fit_geometry_mode == "SYMMETRIC_INTERIOR_COMPLEX_POLE"
            else ""
        )
        if (
            fit_geometry_mode == "SYMMETRIC_INTERIOR_COMPLEX_POLE"
            and row.get("fit_row_type", "")
            == "NEAR_SUPPORT_FINAL_SIMPLE_POLE_FIT"
        ):
            refined_pole = complex(
                float(row["refined_pole_real"]),
                float(row["refined_pole_imaginary"]),
            )
            diagnostic_key = interior_fit_diagnostic_key(
                coordinate,
                refined_pole,
                float(row["fit_scale"]),
            )
            if diagnostic_key not in INTERIOR_FIT_DIAGNOSTICS:
                raise RuntimeError("missing interior topology-radius diagnostic")
            row.update(INTERIOR_FIT_DIAGNOSTICS[diagnostic_key])
    if fit_geometry_mode == "SYMMETRIC_INTERIOR_COMPLEX_POLE":
        final_rows = [
            row
            for row in rows
            if row.get("fit_row_type", "")
            == "NEAR_SUPPORT_FINAL_SIMPLE_POLE_FIT"
        ]
        selected["interior_topology_preflight_passes"] = bool(final_rows) and all(
            bool(row["interior_topology_preflight_passes"])
            for row in final_rows
        )
    return selected, rows


def configure_local_pole_repair(epsilon_id: str) -> None:
    M5326.near_support_laurent_fit = ORIGINAL_NEAR_SUPPORT_LAURENT_FIT
    M5326.refine_near_support_simple_pole = ORIGINAL_REFINE_NEAR_SUPPORT_SIMPLE_POLE
    M5326.NEAR_SUPPORT_DISTANCE_CORE_LIMIT = ORIGINAL_NEAR_SUPPORT_DISTANCE_CORE_LIMIT
    M5326.NEAR_SUPPORT_REPAIR_REVISION = ORIGINAL_NEAR_SUPPORT_REPAIR_REVISION
    M5326.near_support_laurent_fit = E000625_interior_laurent_fit
    M5326.refine_near_support_simple_pole = E000625_refine_near_support_simple_pole
    M5326.NEAR_SUPPORT_DISTANCE_CORE_LIMIT = E000625_NEAR_SUPPORT_DISTANCE_CORE_LIMIT
    M5326.NEAR_SUPPORT_REPAIR_REVISION = TOPOLOGY_SAFE_REPAIR_REVISION


def D2_extended_energy_partition_repair(
    node: dict[str, Any],
    contract: list[dict[str, str]],
    expected_plan_sha256: str,
    base_context: dict[str, Any],
    multiplier: float,
    result: dict[str, Any],
) -> dict[str, Any]:
    is_extended_target = (
        ACTIVE_TARGET_EPSILON_ID == "E020"
        and str(node["node_id"]) in E020_EXTENDED_ENERGY_NODE_IDS
    )
    already_has_inherited_ladder = (
        bool(result.get("targeted_energy_partition_repair_applied", False))
        and int(result.get("targeted_energy_panel_subdivisions", 0)) >= 128
    )
    final = (
        result
        if is_extended_target and already_has_inherited_ladder
        else ORIGINAL_REPAIR_NODE_ENERGY_RESOLUTION(
            node,
            contract,
            expected_plan_sha256,
            base_context,
            multiplier,
            result,
        )
    )
    if bool(final["acceptance_passed"]):
        return final
    off_support_fallback = (
        int(final["inactive_selected_term_count"]) == 0
        and int(final["unresolved_pole_count"]) == 0
        and int(final["geometric_pole_count"]) > 0
        and int(final["in_support_pole_count"]) == 0
    )
    if not is_extended_target and not off_support_fallback:
        return final
    if (
        int(final["inactive_selected_term_count"]) != 0
        or int(final["unresolved_pole_count"]) != 0
    ):
        return final
    baseline_change = float(
        final.get(
            "pre_repair_inner_Q4_Q8_relative_change",
            result["inner_Q4_Q8_relative_change"],
        )
    )
    baseline_budget = float(
        final.get(
            "pre_repair_inner_energy_error_budget_relative",
            result["inner_energy_error_budget_relative"],
        )
    )
    if is_extended_target:
        subdivision_ladder = E020_EXTENDED_ENERGY_SUBDIVISIONS
        repair_revision = E020_EXTENDED_ENERGY_REPAIR_REVISION
        fallback_reason = (
            E020_DIRECT_CONTOUR_FALLBACK_REASON
            if str(node["node_id"]) in E020_DIRECT_CONTOUR_FALLBACK_NODE_IDS
            else ""
        )
    else:
        completed_subdivisions = int(
            final.get("targeted_energy_panel_subdivisions", 0)
        )
        subdivision_ladder = tuple(
            count
            for count in OFF_SUPPORT_ENERGY_SUBDIVISIONS
            if count > completed_subdivisions
        )
        repair_revision = OFF_SUPPORT_ENERGY_REPAIR_REVISION
        fallback_reason = OFF_SUPPORT_ENERGY_FALLBACK_REASON
    old_energy_panel_rows = M5326.M5312.energy_panel_rows
    try:
        for subdivisions in subdivision_ladder:
            M5326.M5312.energy_panel_rows = (
                lambda local_node, cell, supports, classifications, count=subdivisions: M5326.refined_energy_panel_rows(
                    local_node,
                    cell,
                    supports,
                    classifications,
                    count,
                )
            )
            final = M5326.M5312.run_node(
                node,
                contract,
                expected_plan_sha256,
                base_context,
                multiplier,
            )
            final["targeted_energy_partition_repair_applied"] = True
            final["targeted_energy_panel_subdivisions"] = subdivisions
            final["extended_energy_partition_repair_revision"] = (
                repair_revision
            )
            final["extended_energy_partition_fallback_reason"] = fallback_reason
            final["pre_repair_inner_Q4_Q8_relative_change"] = baseline_change
            final["pre_repair_inner_energy_error_budget_relative"] = baseline_budget
            M5326.atomic_json(
                M5326.M5312.shard_paths(str(node["node_id"]))["result"],
                final,
            )
            M5326.record_energy_repair(
                {
                    "node_id": node["node_id"],
                    "x_panel_index": node["x_panel_index"],
                    "absolute_soft_cosine": node["absolute_soft_cosine"],
                    "energy_panel_subdivisions": subdivisions,
                    "energy_partition_repair_revision": (
                        repair_revision
                    ),
                    "energy_partition_fallback_reason": fallback_reason,
                    "pre_repair_inner_Q4_Q8_relative_change": baseline_change,
                    "post_repair_inner_Q4_Q8_relative_change": final[
                        "inner_Q4_Q8_relative_change"
                    ],
                    "pre_repair_inner_energy_error_budget_relative": baseline_budget,
                    "post_repair_inner_energy_error_budget_relative": final[
                        "inner_energy_error_budget_relative"
                    ],
                    "repair_acceptance_passed": final["acceptance_passed"],
                    **{field: False for field in M5326.CLAIM_FIELDS},
                }
            )
            if bool(final["acceptance_passed"]):
                break
    finally:
        M5326.M5312.energy_panel_rows = old_energy_panel_rows
    return final


def configure_target(epsilon_id: str) -> dict[str, Path]:
    global ACTIVE_TARGET_EPSILON_ID
    if epsilon_id not in RUN_IDS:
        raise ValueError(f"unsupported generated epsilon id: {epsilon_id}")
    ACTIVE_TARGET_EPSILON_ID = epsilon_id
    INTERIOR_FIT_DIAGNOSTICS.clear()
    paths = target_paths(epsilon_id)
    epsilon = EPSILON_VALUES[epsilon_id]
    M5326.SOURCE = paths["source"]
    M5326.SHARDS = paths["shards"]
    M5326.EVENT_CANDIDATES = paths["event_candidates"]
    M5326.EVENT_CACHE = paths["event_cache"]
    M5326.EVENT_STATES = paths["event_states"]
    M5326.EVENTS = paths["events"]
    M5326.INITIAL_PLAN = paths["initial_plan"]
    M5326.DRY_RUN = paths["dry_run"]
    M5326.NODE_MANIFEST = paths["node_manifest"]
    M5326.ADAPTIVE_PANELS = paths["adaptive_panels"]
    M5326.OFF_AXIS_POLES = paths["poles"]
    M5326.OFF_AXIS_FITS = paths["fits"]
    M5326.OFF_AXIS_CLASSIFICATIONS = paths["classifications"]
    M5326.CELL_INTEGRALS = paths["cell_integrals"]
    M5326.ENERGY_REPAIRS = paths["energy_repairs"]
    M5326.NEAR_SUPPORT_REPAIRS = paths["near_repairs"]
    M5326.NEAR_SUPPORT_FITS = paths["near_fits"]
    M5326.NEAR_SUPPORT_IDENTITIES = paths["near_identities"]
    M5326.FINITE_VALUE = paths["finite"]
    M5326.RESULT = paths["result"]
    M5326.VALIDATION = paths["validation"]
    M5326.RESIDUAL_VALIDATION = paths["residual_validation"]
    M5326.STATUS = paths["status"]
    M5326.DOCUMENT = paths["document"]
    M5326.CHECKPOINT = CHECKPOINT
    M5326.PARENT_CHECKPOINT = PARENT_CHECKPOINT
    M5326.MARKER = f"{MARKER}_{epsilon_id}"
    M5326.REVISION = f"{REVISION}-{epsilon_id}"
    M5326.NODE_REVISION = f"D2-midpoint-{epsilon_id}-node-v2"
    M5326.EPSILON_ID = epsilon_id
    M5326.EPSILON = epsilon
    M5326.M5325.EPSILON_ID = epsilon_id
    M5326.M5325.EPSILON = epsilon
    install_synthetic_context_extension()
    write_inventory_extension_audit(epsilon_id, paths["inventory_audit"])
    initialize_selector_repair_rows(epsilon_id)
    install_selector_guard()
    configure_local_pole_repair(epsilon_id)
    configure_owner_channel_certificate(epsilon_id)
    M5326.repair_node_energy_resolution = D2_extended_energy_partition_repair
    return paths


def normalize_target_result(epsilon_id: str) -> dict[str, Any]:
    paths = target_paths(epsilon_id)
    result = read_json(paths["result"])
    accepted = bool(result["acceptance_passed"])
    state = "ACCEPTED" if accepted else (
        "PAUSED_RESUMABLE"
        if "PAUSED" in result["decision"]
        else "REQUIRES_REFINEMENT"
    )
    result["mode"] = f"D2-midpoint-event-aligned-{epsilon_id}-refinement"
    result["epsilon_id"] = epsilon_id
    result["epsilon"] = EPSILON_VALUES[epsilon_id]
    result["topology_transfer_source_epsilon_id"] = "E0025"
    result["decision"] = (
        f"D2_EVENT_ALIGNED_{epsilon_id}_ACCEPTED__CONTINUE_REGULATOR_LADDER"
        if accepted
        else f"D2_EVENT_ALIGNED_{epsilon_id}_{state}"
    )
    result["claim_boundary"] = {
        "valid_for_D2_finite_regulator_integral": accepted,
        **{field: False for field in CLAIM_FIELDS},
        "reason": (
            f"This closes only epsilon={EPSILON_VALUES[epsilon_id]:.8g} at D2_MID. "
            "The D2 regulator-zero and decay-angle limits remain separate."
        ),
    }
    sources = list(result.get("source_files", []))
    additional_sources = [Path(__file__).resolve(), paths["inventory_audit"]]
    if paths["selector_repairs"].exists():
        additional_sources.append(paths["selector_repairs"])
    additional_sources.extend(
        paths[key]
        for key in ("energy_repairs", "near_repairs", "near_fits", "near_identities")
        if paths[key].exists()
    )
    if epsilon_id == "E040":
        additional_sources.extend(
            (
                SCRIPT_5330,
                RESULT_5330,
                VALIDATION_5330,
                CERTIFICATES_5330,
                FITS_5330,
            )
        )
    additional_paths = {str(path) for path in additional_sources}
    sources = [row for row in sources if row["path"] not in additional_paths]
    sources.extend(
        {"path": str(path), "sha256": digest(path)} for path in additional_sources
    )
    result["source_files"] = sources
    atomic_json(paths["result"], result)
    if paths["finite"].exists():
        rows = read_csv(paths["finite"])
        for row in rows:
            row["valid_for_D2_E0025_fixed_decay_integral"] = False
            row["valid_for_D2_finite_regulator_integral"] = accepted
            for field in CLAIM_FIELDS:
                row[field] = False
        write_csv(paths["finite"], rows, ["decay_node_id", "epsilon_id"])
    atomic_json(
        paths["status"],
        {
            "checkpoint": CHECKPOINT,
            "epsilon_id": epsilon_id,
            "epsilon": EPSILON_VALUES[epsilon_id],
            "state": state,
            "decision": result["decision"],
            "encountered_node_count": result["encountered_node_count"],
            "completed_node_count": result["completed_node_count"],
        },
    )
    return result


def normalize_target_dry_run(epsilon_id: str) -> dict[str, Any]:
    paths = target_paths(epsilon_id)
    result = read_json(paths["dry_run"])
    result["checkpoint"] = CHECKPOINT
    result["parent_checkpoint"] = PARENT_CHECKPOINT
    result["epsilon_id"] = epsilon_id
    result["epsilon"] = EPSILON_VALUES[epsilon_id]
    result["topology_transfer_source_epsilon_id"] = "E0025"
    result["decision"] = (
        f"DRY_RUN_ACCEPTED__RUN_D2_EVENT_ALIGNED_{epsilon_id}_REFINEMENT"
        if bool(result["acceptance_passed"])
        else f"D2_EVENT_ALIGNED_{epsilon_id}_DRY_RUN_BLOCKED"
    )
    atomic_json(paths["dry_run"], result)
    return result


def validate_target(epsilon_id: str) -> dict[str, Any]:
    started = time.perf_counter()
    paths = configure_target(epsilon_id)
    result = normalize_target_result(epsilon_id)
    dry = read_json(paths["dry_run"])
    events = read_csv(paths["events"])
    manifest = read_csv(paths["node_manifest"])
    panels = read_csv(paths["adaptive_panels"])
    finite = read_csv(paths["finite"])
    classifications = read_csv(paths["classifications"])
    selector_repairs = (
        read_csv(paths["selector_repairs"])
        if paths["selector_repairs"].exists()
        else []
    )
    near_repairs = (
        read_csv(paths["near_repairs"])
        if paths["near_repairs"].exists()
        else []
    )
    near_fits = (
        read_csv(paths["near_fits"])
        if paths["near_fits"].exists()
        else []
    )
    energy_repairs = (
        read_csv(paths["energy_repairs"])
        if paths["energy_repairs"].exists()
        else []
    )
    inventory_audit = read_csv(paths["inventory_audit"])
    certificate_rows = (
        list(OWNER_CHANNEL_CERTIFICATE_ROWS.values())
        if epsilon_id == "E040"
        else []
    )
    adaptive_divisor_node_ids = {
        row["node_id"]
        for row in classifications
        if parse_bool(row.get("owner_channel_certificate_applied", False))
        and parse_bool(row.get("pole_classification_resolved", False))
        and not row.get("failure_reason", "")
    }
    effective_near_repairs = [
        row
        for row in near_repairs
        if not (
            epsilon_id == "E040"
            and row["node_id"] in adaptive_divisor_node_ids
        )
    ]
    applied_certificate_rows = [
        row
        for row in classifications
        if parse_bool(row.get("owner_channel_certificate_applied", False))
    ]
    leaves = [row for row in panels if parse_bool(row["adaptive_leaf"])]
    source_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    gates = [
        validation_gate(
            "E0025_topology_transfers_with_seven_resolved_events",
            bool(dry["acceptance_passed"])
            and len(events) == M5326.EXPECTED_EVENT_COUNT
            and all(parse_bool(row["event_contract_passes"]) for row in events),
            f"epsilon={epsilon_id};events={len(events)}",
        ),
        validation_gate(
            "all_target_nodes_pass",
            bool(manifest)
            and all(row["shard_state"] == "COMPLETE_PASS" for row in manifest)
            and int(result["failed_inner_node_count"]) == 0,
            f"nodes={len(manifest)}",
        ),
        validation_gate(
            "all_target_adaptive_leaves_pass",
            bool(leaves)
            and all(parse_bool(row["adaptive_gate_passes"]) for row in leaves)
            and bool(result["all_adaptive_leaf_gates_pass"]),
            f"leaves={len(leaves)}",
        ),
        validation_gate(
            "finite_regulator_error_budget_passes",
            len(finite) == 1
            and parse_bool(finite[0]["finite_regulator_fixed_decay_integral_accepted"])
            and float(finite[0]["total_error_relative_conservative"])
            <= GLOBAL_ERROR_BUDGET_LIMIT
            and bool(result["acceptance_passed"]),
            str(result["total_error_relative_conservative"]),
        ),
        validation_gate(
            "synthetic_regulator_inventory_is_exact_and_parent_map_preserving",
            len(inventory_audit) == len(EXPECTED_IDS)
            and all(
                row["requested_epsilon_id"] == epsilon_id
                and parse_bool(row["valid_for_regulator_inventory"])
                and parse_bool(row["native_target_identity_passes"])
                and parse_bool(row["native_component_identity_passes"])
                and parse_bool(row["target_contract_passes"])
                and parse_bool(row["component_map_identity_passes"])
                for row in inventory_audit
            )
            and {
                row["epsilon_id"]
                for row in inventory_audit
                if row["inventory_origin"]
                == "checkpoint_5327_exact_target_extension"
            }
            == {"E00125", "E000625"},
            f"rows={len(inventory_audit)}",
        ),
        validation_gate(
            "algebraic_selector_repairs_are_collision_and_reciprocal_gated",
            all(selector_repair_passes(row) for row in selector_repairs),
            f"repairs={len(selector_repairs)}",
        ),
        validation_gate(
            "E040_adaptive_owner_channel_divisor_is_complete_and_applied",
            epsilon_id != "E040"
            or (
                len(certificate_rows) == 30
                and len(applied_certificate_rows) >= 30
                and {
                    owner_channel_certificate_key(row)
                    for row in certificate_rows
                }.issubset(
                    {
                        owner_channel_certificate_key(row)
                        for row in applied_certificate_rows
                    }
                )
                and all(
                    parse_bool(row["pole_classification_resolved"])
                    and not row.get("failure_reason", "")
                    and int(row.get("owner_channel_certificate_checkpoint", 0))
                    == 5330
                    for row in applied_certificate_rows
                )
                and all(
                    row.get("owner_channel_certificate_sha256", "")
                    == OWNER_CHANNEL_CERTIFICATE_SHA256
                    for row in applied_certificate_rows
                    if owner_channel_certificate_key(row)
                    in OWNER_CHANNEL_CERTIFICATE_ROWS
                )
            ),
            (
                f"certificates={len(certificate_rows)};"
                f"applied={len(applied_certificate_rows)}"
            ),
        ),
        validation_gate(
            "local_pole_repairs_are_strictly_fitted_masked_and_source_owned",
            all(
                (
                    parse_bool(row["near_support_subtraction_contract_passes"])
                    and parse_bool(row["repair_acceptance_passed"])
                    and not row.get("failure_reason", "")
                )
                or (
                    epsilon_id == "E020"
                    and row["node_id"] in E020_DIRECT_CONTOUR_FALLBACK_NODE_IDS
                    and row.get("failure_reason", "")
                    == "NEAR_SUPPORT_SUBTRACTION_GATE_FAILED"
                    and any(
                        energy_row["node_id"] == row["node_id"]
                        and energy_row.get("energy_partition_repair_revision", "")
                        == E020_EXTENDED_ENERGY_REPAIR_REVISION
                        and energy_row.get("energy_partition_fallback_reason", "")
                        == E020_DIRECT_CONTOUR_FALLBACK_REASON
                        and parse_bool(energy_row["repair_acceptance_passed"])
                        for energy_row in energy_repairs
                    )
                )
                or (
                    row.get("failure_reason", "")
                    == "NEAR_SUPPORT_SUBTRACTION_GATE_FAILED"
                    and any(
                        energy_row["node_id"] == row["node_id"]
                        and energy_row.get("energy_partition_repair_revision", "")
                        == OFF_SUPPORT_ENERGY_REPAIR_REVISION
                        and energy_row.get("energy_partition_fallback_reason", "")
                        == OFF_SUPPORT_ENERGY_FALLBACK_REASON
                        and parse_bool(energy_row["repair_acceptance_passed"])
                        for energy_row in energy_repairs
                    )
                )
                for row in effective_near_repairs
            )
            and all(
                    any(
                        row["node_id"] == node_id
                        and row.get("near_support_repair_revision", "")
                        == REQUIRED_LOCAL_REPAIR_REVISION_BY_EPSILON.get(
                            epsilon_id,
                            TOPOLOGY_SAFE_REPAIR_REVISION,
                        )
                        and parse_bool(
                            row["near_support_subtraction_contract_passes"]
                        )
                        and parse_bool(row["repair_acceptance_passed"])
                        for row in effective_near_repairs
                    )
                    and any(
                        row["node_id"] == node_id
                        and row.get("fit_row_type", "")
                        == "NEAR_SUPPORT_FINAL_SIMPLE_POLE_FIT"
                        and row.get("fit_geometry_mode", "") == fit_mode
                        and parse_bool(row["near_support_simple_pole_fit_passes"])
                        and (
                            epsilon_id != "E020"
                            or (
                                parse_bool(
                                    row.get(
                                        "interior_topology_preflight_passes",
                                        "False",
                                    )
                                )
                                and int(
                                    row.get(
                                        "interior_topology_radius_halving_count",
                                        -1,
                                    )
                                )
                                >= 1
                            )
                        )
                        for row in near_fits
                    )
                    for node_id, fit_mode in REQUIRED_LOCAL_REPAIR_MODES_BY_EPSILON.get(
                        epsilon_id,
                        {},
                    ).items()
            ),
            (
                f"effective_repairs={len(effective_near_repairs)};"
                f"superseded={len(near_repairs)-len(effective_near_repairs)};"
                f"fits={len(near_fits)}"
            ),
        ),
        validation_gate(
            "extended_energy_partition_repair_is_converged_and_source_owned",
            (
                epsilon_id != "E020"
                or all(
                    any(
                        row["node_id"] == node_id
                        and int(row["energy_panel_subdivisions"])
                        in E020_EXTENDED_ENERGY_SUBDIVISIONS
                        and row.get("energy_partition_repair_revision", "")
                        == E020_EXTENDED_ENERGY_REPAIR_REVISION
                        and parse_bool(row["repair_acceptance_passed"])
                        for row in energy_repairs
                    )
                    for node_id in E020_EXTENDED_ENERGY_NODE_IDS
                )
            )
            and (
                epsilon_id == "E020"
                or all(
                    any(
                        energy_row["node_id"] == near_row["node_id"]
                        and int(energy_row["energy_panel_subdivisions"])
                        in OFF_SUPPORT_ENERGY_SUBDIVISIONS
                        and energy_row.get("energy_partition_repair_revision", "")
                        == OFF_SUPPORT_ENERGY_REPAIR_REVISION
                        and energy_row.get("energy_partition_fallback_reason", "")
                        == OFF_SUPPORT_ENERGY_FALLBACK_REASON
                        and parse_bool(energy_row["repair_acceptance_passed"])
                        for energy_row in energy_repairs
                    )
                    for near_row in effective_near_repairs
                    if near_row.get("failure_reason", "")
                    == "NEAR_SUPPORT_SUBTRACTION_GATE_FAILED"
                )
            ),
            f"repairs={len(energy_repairs)}",
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest()
            == result["formalization_workbench_end_digest"]
            == result["formalization_workbench_reference_digest"]
            == FORMAL_DIGEST
            and int(result["formalization_workbench_modified_file_count"]) == 0,
            result["formalization_workbench_end_digest"],
        ),
        validation_gate(
            "source_paths_and_hashes_current",
            source_current,
            f"rows={len(result['source_files'])}",
        ),
        validation_gate(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
        validation_gate(
            "regulator_zero_and_broader_claims_locked_false",
            all(not bool(result["claim_boundary"][field]) for field in CLAIM_FIELDS),
            epsilon_id,
        ),
    ]
    passed = all(bool(row["passed"]) for row in gates)
    write_csv(paths["validation"], gates, ["gate"])
    write_csv(paths["residual_validation"], gates, ["gate"])
    return {
        "checkpoint": CHECKPOINT,
        "mode": "target-validation",
        "epsilon_id": epsilon_id,
        "acceptance_passed": passed,
        "decision": (
            f"VALIDATED_D2_MIDPOINT_{epsilon_id}_FINITE_REGULATOR"
            if passed
            else f"D2_MIDPOINT_{epsilon_id}_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def runtime_owner_channel_shard_passes(node_id: str) -> bool:
    paths = M5326.M5312.shard_paths(node_id)
    if not paths["result"].exists() or not paths["classifications"].exists():
        return False
    result = read_json(paths["result"])
    classifications = read_csv(paths["classifications"])
    runtime_rows = [
        row
        for row in classifications
        if parse_bool(row.get("owner_channel_certificate_applied", False))
        and parse_bool(row.get("adaptive_divisor_runtime_evaluated", False))
        and row.get("owner_channel_certificate_sha256", "") == digest(SCRIPT_5330)
    ]
    return (
        bool(result.get("acceptance_passed"))
        and int(result.get("unresolved_pole_count", -1)) == 0
        and bool(runtime_rows)
        and all(parse_bool(row["pole_classification_resolved"]) for row in classifications)
    )


def unresolved_runtime_divisor_target(node: dict[str, Any]) -> bool:
    if str(node.get("shard_state", "")) != "COMPLETE_FAIL":
        return False
    paths = M5326.M5312.shard_paths(str(node["node_id"]))
    if not paths["result"].exists() or not paths["classifications"].exists():
        return False
    result = read_json(paths["result"])
    classifications = read_csv(paths["classifications"])
    return (
        not bool(result.get("acceptance_passed"))
        and any(
            not parse_bool(row.get("pole_classification_resolved", False))
            for row in classifications
        )
    )


def rerun_owner_channel_certificate_nodes(
    runtime_limit_seconds: float,
) -> dict[str, Any]:
    started = time.perf_counter()
    if ACTIVE_TARGET_EPSILON_ID != "E040":
        raise RuntimeError("owner-channel rerun is E040-only")
    if len(OWNER_CHANNEL_CERTIFICATE_ROWS) != 30:
        raise RuntimeError("owner-channel certificate is not configured")
    dry = M5326.load_validated_dry_run()
    contract = read_csv(M5326.CONTRACT_5325)
    expected = str(dry["node_plan_sha256"])
    base_context = M5326.M5312.M5303.synthetic_context()
    multiplier = M5326.M5312.M5309.physical_multiplier()
    manifest = read_csv(M5326.NODE_MANIFEST)
    previous_shards = M5326.M5312.SHARDS
    M5326.M5312.SHARDS = M5326.SHARDS
    try:
        targets = [
            dict(row) for row in manifest if unresolved_runtime_divisor_target(row)
        ]
    finally:
        M5326.M5312.SHARDS = previous_shards
    target_node_ids = {str(row["node_id"]) for row in targets}
    if not targets:
        raise RuntimeError("E040 manifest has no unresolved runtime-divisor targets")
    old = M5326.configure_kernel()
    completed: list[dict[str, Any]] = []
    paused = False
    accepted_count = 0
    try:
        for node in targets:
            node_id = str(node["node_id"])
            if runtime_owner_channel_shard_passes(node_id):
                final = read_json(M5326.M5312.shard_paths(node_id)["result"])
            else:
                if time.perf_counter() - started >= runtime_limit_seconds:
                    paused = True
                    break
                final = M5326.M5312.run_node(
                    node,
                    contract,
                    expected,
                    base_context,
                    multiplier,
                )
                if (
                    not bool(final["acceptance_passed"])
                    and int(final["unresolved_pole_count"]) == 0
                ):
                    final = M5326.repair_node_energy_resolution(
                        node,
                        contract,
                        expected,
                        base_context,
                        multiplier,
                        final,
                    )
            completed.append(
                {
                    "node_id": node_id,
                    "acceptance_passed": bool(final["acceptance_passed"]),
                    "unresolved_pole_count": int(final["unresolved_pole_count"]),
                    "runtime_divisor_certificate_count": sum(
                        1
                        for row in read_csv(
                            M5326.M5312.shard_paths(node_id)["classifications"]
                        )
                        if parse_bool(
                            row.get("adaptive_divisor_runtime_evaluated", False)
                        )
                    ),
                    "runtime_seconds": float(final["runtime_seconds"]),
                }
            )
            atomic_json(
                M5326.SOURCE / "owner_channel_runtime_divisor_rerun_status.json",
                {
                    "checkpoint": CHECKPOINT,
                    "epsilon_id": "E040",
                    "state": "RUNNING",
                    "completed_node_count": len(completed),
                    "target_node_count": len(targets),
                    "last_node_id": node_id,
                },
            )
        accepted_count = sum(
            runtime_owner_channel_shard_passes(node_id)
            for node_id in target_node_ids
        )
    finally:
        M5326.restore_kernel(old)
    accepted = not paused and accepted_count == len(target_node_ids)
    decision = (
        "E040_RUNTIME_DIVISOR_NODES_ACCEPTED__RESUME_OUTER_RUN"
        if accepted
        else "E040_RUNTIME_DIVISOR_NODE_RERUN_PAUSED__RESUME"
        if paused
        else "E040_RUNTIME_DIVISOR_NODES_REQUIRE_REFINEMENT"
    )
    result = {
        "checkpoint": CHECKPOINT,
        "mode": "owner-channel-runtime-divisor-rerun",
        "epsilon_id": "E040",
        "acceptance_passed": accepted,
        "decision": decision,
        "target_node_count": len(targets),
        "accepted_node_count": accepted_count,
        "encountered_node_count": len(completed),
        "paused_resumable": paused,
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(
        M5326.SOURCE / "owner_channel_runtime_divisor_rerun_result.json",
        result,
    )
    atomic_json(
        M5326.SOURCE / "owner_channel_runtime_divisor_rerun_status.json",
        {
            "checkpoint": CHECKPOINT,
            "epsilon_id": "E040",
            "state": (
                "ACCEPTED"
                if accepted
                else "PAUSED_RESUMABLE"
                if paused
                else "REQUIRES_REFINEMENT"
            ),
            "decision": decision,
            "accepted_node_count": accepted_count,
            "target_node_count": len(targets),
        },
    )
    return result


def finite_row(
    epsilon_id: str,
    finite_path: Path,
    result_path: Path,
    validation_path: Path,
) -> dict[str, Any] | None:
    if not all(path.exists() for path in (finite_path, result_path, validation_path)):
        return None
    result = read_json(result_path)
    validation = read_csv(validation_path)
    rows = read_csv(finite_path)
    if (
        len(rows) != 1
        or not bool(result["acceptance_passed"])
        or not all(parse_bool(row["passed"]) for row in validation)
        or not parse_bool(rows[0]["finite_regulator_fixed_decay_integral_accepted"])
    ):
        return None
    row = rows[0]
    value = complex(
        float(row["fixed_decay_integral_real"]),
        float(row["fixed_decay_integral_imaginary"]),
    )
    relative = float(row["total_error_relative_conservative"])
    return {
        "decay_node_id": "D2_MID",
        "epsilon_id": epsilon_id,
        "epsilon": EPSILON_VALUES[epsilon_id],
        "method": row["method"],
        "fixed_decay_integral_real": value.real,
        "fixed_decay_integral_imaginary": value.imag,
        "fixed_decay_integral_magnitude": abs(value),
        "fixed_decay_error_absolute_conservative": relative * abs(value),
        "fixed_decay_error_relative_conservative": relative,
        "finite_regulator_fixed_decay_integral_accepted": True,
        "finite_source_path": str(finite_path),
        "result_source_path": str(result_path),
        "validation_source_path": str(validation_path),
        "valid_for_D2_regulator_zero_fit_input": True,
        **{field: False for field in CLAIM_FIELDS},
    }


def pairwise_convergence_rows(
    finite_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lower, upper in zip(finite_rows[:-1], finite_rows[1:]):
        lower_value = complex(
            float(lower["fixed_decay_integral_real"]),
            float(lower["fixed_decay_integral_imaginary"]),
        )
        upper_value = complex(
            float(upper["fixed_decay_integral_real"]),
            float(upper["fixed_decay_integral_imaginary"]),
        )
        difference = upper_value - lower_value
        combined_error = (
            float(lower["fixed_decay_error_absolute_conservative"])
            + float(upper["fixed_decay_error_absolute_conservative"])
        )
        difference_magnitude = abs(difference)
        rows.append(
            {
                "lower_epsilon_id": lower["epsilon_id"],
                "upper_epsilon_id": upper["epsilon_id"],
                "lower_epsilon": float(lower["epsilon"]),
                "upper_epsilon": float(upper["epsilon"]),
                "epsilon_ratio": float(upper["epsilon"]) / float(lower["epsilon"]),
                "difference_real": difference.real,
                "difference_imaginary": difference.imag,
                "difference_magnitude": difference_magnitude,
                "relative_complex_change": difference_magnitude
                / max(abs(lower_value), abs(upper_value), 1.0e-300),
                "combined_conservative_error_absolute": combined_error,
                "difference_to_combined_error_ratio": difference_magnitude
                / max(combined_error, 1.0e-300),
                "difference_within_combined_conservative_error": (
                    difference_magnitude <= combined_error
                ),
                "valid_for_D2_regulator_zero_fit_input_pair": True,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def three_point_trend_rows(
    finite_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lower, middle, upper in zip(
        finite_rows[:-2],
        finite_rows[1:-1],
        finite_rows[2:],
    ):
        lower_value = complex(
            float(lower["fixed_decay_integral_real"]),
            float(lower["fixed_decay_integral_imaginary"]),
        )
        middle_value = complex(
            float(middle["fixed_decay_integral_real"]),
            float(middle["fixed_decay_integral_imaginary"]),
        )
        upper_value = complex(
            float(upper["fixed_decay_integral_real"]),
            float(upper["fixed_decay_integral_imaginary"]),
        )
        lower_difference = middle_value - lower_value
        upper_difference = upper_value - middle_value
        ratio = lower_difference / upper_difference
        ratio_magnitude = abs(ratio)
        ratio_phase = math.atan2(ratio.imag, ratio.real)
        nominal_order = (
            -math.log(ratio_magnitude, 2.0)
            if 0.0 < ratio_magnitude < 1.0
            else math.nan
        )
        denominator = (
            2.0**nominal_order - 1.0
            if math.isfinite(nominal_order)
            else math.nan
        )
        nominal_limit = (
            lower_value - lower_difference / denominator
            if math.isfinite(denominator) and abs(denominator) > 1.0e-15
            else complex(math.nan, math.nan)
        )
        lower_error = (
            float(lower["fixed_decay_error_absolute_conservative"])
            + float(middle["fixed_decay_error_absolute_conservative"])
        )
        upper_error = (
            float(middle["fixed_decay_error_absolute_conservative"])
            + float(upper["fixed_decay_error_absolute_conservative"])
        )
        central_contracts = (
            0.0 < ratio_magnitude < 1.0
            and abs(ratio_phase) <= 0.1
            and math.isfinite(nominal_order)
            and nominal_order > 0.0
        )
        resolved = (
            abs(lower_difference) > lower_error
            and abs(upper_difference) > upper_error
        )
        rows.append(
            {
                "lower_epsilon_id": lower["epsilon_id"],
                "middle_epsilon_id": middle["epsilon_id"],
                "upper_epsilon_id": upper["epsilon_id"],
                "lower_epsilon": float(lower["epsilon"]),
                "middle_epsilon": float(middle["epsilon"]),
                "upper_epsilon": float(upper["epsilon"]),
                "lower_to_middle_epsilon_ratio": float(middle["epsilon"])
                / float(lower["epsilon"]),
                "middle_to_upper_epsilon_ratio": float(upper["epsilon"])
                / float(middle["epsilon"]),
                "successive_difference_ratio_real": ratio.real,
                "successive_difference_ratio_imaginary": ratio.imag,
                "successive_difference_ratio_magnitude": ratio_magnitude,
                "successive_difference_ratio_phase_radians": ratio_phase,
                "nominal_effective_convergence_order": nominal_order,
                "nominal_zero_limit_real": nominal_limit.real,
                "nominal_zero_limit_imaginary": nominal_limit.imag,
                "nominal_zero_limit_magnitude": abs(nominal_limit),
                "lower_difference_to_error_ratio": abs(lower_difference)
                / max(lower_error, 1.0e-300),
                "upper_difference_to_error_ratio": abs(upper_difference)
                / max(upper_error, 1.0e-300),
                "central_values_contract_with_nearly_collinear_differences": central_contracts,
                "power_law_order_resolved_above_conservative_numerical_error": resolved,
                "valid_for_preliminary_regulator_trend_diagnostic": True,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def collect_ladder() -> dict[str, Any]:
    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    inherited = finite_row("E0025", FINITE_5326, RESULT_5326, VALIDATION_5326)
    if inherited is None:
        raise RuntimeError("validated 5326 E0025 finite row is unavailable")
    rows.append(inherited)
    for epsilon_id in RUN_IDS:
        paths = target_paths(epsilon_id)
        row = finite_row(
            epsilon_id,
            paths["finite"],
            paths["result"],
            paths["validation"],
        )
        if row is not None:
            rows.append(row)
    rows.sort(key=lambda row: float(row["epsilon"]))
    write_csv(LADDER, rows, ["epsilon_id"])
    pairwise = pairwise_convergence_rows(rows)
    if pairwise:
        write_csv(PAIRWISE, pairwise, ["lower_epsilon_id", "upper_epsilon_id"])
    trends = three_point_trend_rows(rows)
    if trends:
        write_csv(
            TRENDS,
            trends,
            ["lower_epsilon_id", "middle_epsilon_id", "upper_epsilon_id"],
        )
    completed_ids = tuple(row["epsilon_id"] for row in rows)
    missing_ids = tuple(value for value in EXPECTED_IDS if value not in completed_ids)
    complete = not missing_ids
    formal_end = M5283.formal_inventory_digest()
    source_paths = {Path(__file__).resolve(), LADDER}
    if pairwise:
        source_paths.add(PAIRWISE)
    if trends:
        source_paths.add(TRENDS)
    selector_repairs: list[dict[str, str]] = []
    inventory_audits: list[dict[str, str]] = []
    for epsilon_id in RUN_IDS:
        selector_path = target_paths(epsilon_id)["selector_repairs"]
        if selector_path.exists():
            source_paths.add(selector_path)
            selector_repairs.extend(read_csv(selector_path))
        inventory_path = target_paths(epsilon_id)["inventory_audit"]
        if inventory_path.exists():
            source_paths.add(inventory_path)
            inventory_audits.extend(read_csv(inventory_path))
    for row in rows:
        source_paths.update(
            {
                Path(row["finite_source_path"]),
                Path(row["result_source_path"]),
                Path(row["validation_source_path"]),
            }
        )
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D2-midpoint-regulator-ladder-controller",
        "acceptance_passed": complete,
        "checkpoint_execution_passed": True,
        "decision": (
            "D2_SEVEN_POINT_FINITE_REGULATOR_LADDER_COMPLETE__FIT_ZERO_LIMIT"
            if complete
            else "D2_REGULATOR_LADDER_PARTIAL__RUN_MISSING_EPSILONS"
        ),
        "completed_regulator_count": len(rows),
        "expected_regulator_count": len(EXPECTED_IDS),
        "completed_regulator_ids": list(completed_ids),
        "missing_regulator_ids": list(missing_ids),
        "adjacent_regulator_pair_count": len(pairwise),
        "maximum_adjacent_relative_complex_change": max(
            (float(row["relative_complex_change"]) for row in pairwise),
            default=0.0,
        ),
        "maximum_adjacent_difference_to_combined_error_ratio": max(
            (
                float(row["difference_to_combined_error_ratio"])
                for row in pairwise
            ),
            default=0.0,
        ),
        "all_adjacent_differences_within_combined_conservative_errors": all(
            bool(row["difference_within_combined_conservative_error"])
            for row in pairwise
        ),
        "three_point_trend_count": len(trends),
        "smallest_epsilon_nominal_effective_convergence_order": (
            float(trends[0]["nominal_effective_convergence_order"])
            if trends
            else None
        ),
        "smallest_epsilon_successive_difference_ratio_phase_radians": (
            float(trends[0]["successive_difference_ratio_phase_radians"])
            if trends
            else None
        ),
        "resolved_power_law_trend_count": sum(
            bool(
                row[
                    "power_law_order_resolved_above_conservative_numerical_error"
                ]
            )
            for row in trends
        ),
        "algebraic_selector_repair_count": len(selector_repairs),
        "synthetic_regulator_inventory_audit_row_count": len(inventory_audits),
        "maximum_original_reciprocal_pair_residual": max(
            (
                float(row["original_reciprocal_pair_residual"])
                for row in selector_repairs
            ),
            default=0.0,
        ),
        "maximum_corrected_selected_collision_residual_relative": max(
            (
                float(row["corrected_selected_collision_residual_relative"])
                for row in selector_repairs
            ),
            default=0.0,
        ),
        "maximum_corrected_reciprocal_pair_residual": max(
            (
                float(row["corrected_reciprocal_pair_residual"])
                for row in selector_repairs
            ),
            default=0.0,
        ),
        "formalization_workbench_reference_digest": FORMAL_DIGEST,
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": 0 if formal_end == FORMAL_DIGEST else -1,
        "claim_boundary": {
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "Finite-regulator rows are inputs only. The D2 regulator-zero fit "
                "is not attempted until all seven validated rows exist."
            ),
        },
        "source_files": [
            {"path": str(path), "sha256": digest(path)}
            for path in sorted(source_paths, key=str)
        ],
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETE_INPUT_LADDER" if complete else "PARTIAL_RESUMABLE",
            "completed_regulator_count": len(rows),
            "missing_regulator_ids": list(missing_ids),
            "decision": result["decision"],
        },
    )
    render_document(result)
    return result


def validate_controller() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    rows = read_csv(LADDER)
    pairwise = read_csv(PAIRWISE) if PAIRWISE.exists() else []
    trends = read_csv(TRENDS) if TRENDS.exists() else []
    ids = tuple(row["epsilon_id"] for row in rows)
    expected_present = tuple(
        value for value in EXPECTED_IDS if value in set(ids)
    )
    sources_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    selector_repairs = [
        row
        for epsilon_id in RUN_IDS
        for path in [target_paths(epsilon_id)["selector_repairs"]]
        if path.exists()
        for row in read_csv(path)
    ]
    inventory_audits = [
        row
        for epsilon_id in RUN_IDS
        for path in [target_paths(epsilon_id)["inventory_audit"]]
        if path.exists()
        for row in read_csv(path)
    ]
    gates = [
        validation_gate(
            "all_collected_rows_numeric_and_accepted",
            bool(rows)
            and all(
                float(row["epsilon"]) > 0.0
                and math.isfinite(float(row["fixed_decay_integral_real"]))
                and math.isfinite(float(row["fixed_decay_integral_imaginary"]))
                and 0.0 < float(row["fixed_decay_error_relative_conservative"])
                <= GLOBAL_ERROR_BUDGET_LIMIT
                and parse_bool(row["finite_regulator_fixed_decay_integral_accepted"])
                for row in rows
            ),
            f"rows={len(rows)}",
        ),
        validation_gate(
            "collected_ids_are_ordered_expected_subset",
            ids == expected_present,
            "|".join(ids),
        ),
        validation_gate(
            "adjacent_regulator_convergence_rows_are_complete_and_nonclaim",
            len(pairwise) == max(len(rows) - 1, 0)
            and all(
                float(row["epsilon_ratio"]) > 1.0
                and math.isfinite(float(row["difference_magnitude"]))
                and math.isfinite(float(row["relative_complex_change"]))
                and float(row["combined_conservative_error_absolute"]) > 0.0
                and math.isfinite(
                    float(row["difference_to_combined_error_ratio"])
                )
                and parse_bool(row["valid_for_D2_regulator_zero_fit_input_pair"])
                and all(not parse_bool(row[field]) for field in CLAIM_FIELDS)
                for row in pairwise
            ),
            f"pairs={len(pairwise)}",
        ),
        validation_gate(
            "three_point_trends_are_numeric_explicitly_preliminary_and_nonclaim",
            len(trends) == max(len(rows) - 2, 0)
            and all(
                float(row["lower_to_middle_epsilon_ratio"]) > 1.0
                and float(row["middle_to_upper_epsilon_ratio"]) > 1.0
                and math.isfinite(
                    float(row["successive_difference_ratio_magnitude"])
                )
                and math.isfinite(
                    float(row["successive_difference_ratio_phase_radians"])
                )
                and math.isfinite(
                    float(row["nominal_effective_convergence_order"])
                )
                and parse_bool(
                    row["valid_for_preliminary_regulator_trend_diagnostic"]
                )
                and all(not parse_bool(row[field]) for field in CLAIM_FIELDS)
                for row in trends
            ),
            f"trends={len(trends)}",
        ),
        validation_gate(
            "controller_decision_matches_completeness",
            bool(result["acceptance_passed"]) == (len(rows) == len(EXPECTED_IDS))
            and set(result["missing_regulator_ids"]) == set(EXPECTED_IDS) - set(ids),
            result["decision"],
        ),
        validation_gate(
            "all_checkpoint_inventory_extensions_are_exact_and_parent_map_preserving",
            len(inventory_audits)
            == int(result.get("synthetic_regulator_inventory_audit_row_count", -1))
            and all(
                parse_bool(row["valid_for_regulator_inventory"])
                and parse_bool(row["native_target_identity_passes"])
                and parse_bool(row["native_component_identity_passes"])
                and parse_bool(row["target_contract_passes"])
                and parse_bool(row["component_map_identity_passes"])
                for row in inventory_audits
            ),
            f"rows={len(inventory_audits)}",
        ),
        validation_gate(
            "all_checkpoint_selector_repairs_are_collision_and_reciprocal_gated",
            len(selector_repairs)
            == int(result.get("algebraic_selector_repair_count", -1))
            and all(selector_repair_passes(row) for row in selector_repairs),
            f"repairs={len(selector_repairs)}",
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest()
            == result["formalization_workbench_end_digest"]
            == result["formalization_workbench_reference_digest"]
            == FORMAL_DIGEST
            and int(result["formalization_workbench_modified_file_count"]) == 0,
            result["formalization_workbench_end_digest"],
        ),
        validation_gate(
            "source_paths_and_hashes_current",
            sources_current,
            f"rows={len(result['source_files'])}",
        ),
        validation_gate(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
        validation_gate(
            "zero_limit_and_broader_claims_locked_false",
            all(not bool(result["claim_boundary"][field]) for field in CLAIM_FIELDS),
            "finite rows only",
        ),
    ]
    passed = all(bool(row["passed"]) for row in gates)
    write_csv(VALIDATION, gates, ["gate"])
    write_csv(RESIDUAL_VALIDATION, gates, ["gate"])
    return {
        "checkpoint": CHECKPOINT,
        "mode": "controller-validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_D2_REGULATOR_LADDER_CONTROLLER"
            if passed
            else "D2_REGULATOR_LADDER_CONTROLLER_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def render_document(result: dict[str, Any]) -> None:
    missing = ", ".join(result["missing_regulator_ids"]) or "none"
    lines = [
        "# 5327 - D2 midpoint regulator ladder controller",
        "",
        "## Method",
        "",
        "Each regulator value receives isolated event caches, shards, pole fits,",
        "adaptive panels, and validation. The seven E0025 support events are used",
        "only as candidate topology; every target epsilon must re-solve all event",
        "coordinates and pass its own topology, inner, outer, and source gates.",
        "Reciprocal algebraic candidates are repaired only when the inherited pair",
        "residual is anomalous; both collision equations and the reciprocal-product",
        "identity must then pass explicit residual gates, with every repair audited.",
        "For every regulator, candidate detection extends to 32 imaginary-core widths",
        "without relaxing any fit gate. Outside-support poles retain one-sided active-",
        "support subtraction; inside-support poles use symmetric pole-centred Laurent samples",
        "whose full stencil stays inside one support branch. Fit residual, residue-scale",
        "stability, second-order suppression, and masked identity limits are unchanged.",
        "If the common two-scale stencil crosses an internal selector orbit, its radius",
        "is halved until a dense linear-plus-geometric guard is branch-pure; the radius",
        "may not shrink below one imaginary pole core and no acceptance limit is relaxed.",
        "The isolated E020 slow-energy nodes extend the inherited 64/128 partition",
        "ladder to independently audited 256/512 subdivisions, retaining the same",
        "Q4/Q8 and conservative error-budget gates. An outside-support pole whose",
        "strict residue fit fails is never subtracted: because it remains off the real",
        "contour, its failed fit is retained and direct real-contour refinement is used.",
        "",
        "## State",
        "",
        f"- validated finite rows: `{result['completed_regulator_count']}/7`;",
        f"- missing rows: `{missing}`;",
        f"- decision: **{result['decision']}**.",
        "- maximum adjacent regulator change: "
        f"`{result['maximum_adjacent_relative_complex_change']:.6e}`;",
        "- maximum difference/error-envelope ratio: "
        f"`{result['maximum_adjacent_difference_to_combined_error_ratio']:.6e}`;",
        "- preliminary three-point trends: "
        f"`{result['three_point_trend_count']}`; resolved above error: "
        f"`{result['resolved_power_law_trend_count']}`;",
        f"- audited algebraic-selector repairs: `{result['algebraic_selector_repair_count']}`;",
        "- synthetic regulator-inventory audit rows: "
        f"`{result['synthetic_regulator_inventory_audit_row_count']}`;",
        "- maximum corrected collision residual: "
        f"`{result['maximum_corrected_selected_collision_residual_relative']:.6e}`;",
        "- maximum corrected reciprocal-pair residual: "
        f"`{result['maximum_corrected_reciprocal_pair_residual']:.6e}`.",
        "",
        "## Claim boundary",
        "",
        "The E00125 and E000625 inventories extend the parent 5303 construction",
        "only by the exact target `-9+i epsilon`; they retain the parent E020",
        "component map byte-for-byte and do not assert a regulator-zero result.",
        "",
        "No regulator-zero or decay-angle claim is made by the controller. A",
        "zero-limit fit is allowed only after all seven finite rows validate.",
    ]
    DOCUMENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=(
            "dry-run",
            "run",
            "repair-nodes",
            "certificate-rerun",
            "validate-target",
            "collect",
            "validate",
        ),
        required=True,
    )
    parser.add_argument("--epsilon-id", choices=RUN_IDS)
    parser.add_argument("--max-runtime-hours", type=float, default=2.0)
    return parser.parse_args()


def main() -> int:
    M5326.M5312.set_below_normal_priority()
    arguments = parse_args()
    started = time.perf_counter()
    if arguments.mode in {
        "dry-run",
        "run",
        "repair-nodes",
        "certificate-rerun",
        "validate-target",
    }:
        if arguments.epsilon_id is None:
            raise RuntimeError("--epsilon-id is required for target modes")
        configure_target(arguments.epsilon_id)
        if arguments.mode == "dry-run":
            result = M5326.dry_run()
            result = normalize_target_dry_run(arguments.epsilon_id)
        elif arguments.mode == "run":
            result = M5326.execute(arguments.max_runtime_hours * 3600.0)
            flush_selector_repair_rows()
            result = normalize_target_result(arguments.epsilon_id)
            if bool(result["acceptance_passed"]):
                result = validate_target(arguments.epsilon_id)
        elif arguments.mode == "repair-nodes":
            result = M5326.repair_failed_nodes()
            flush_selector_repair_rows()
        elif arguments.mode == "certificate-rerun":
            result = rerun_owner_channel_certificate_nodes(
                arguments.max_runtime_hours * 3600.0
            )
            flush_selector_repair_rows()
        else:
            result = validate_target(arguments.epsilon_id)
    elif arguments.mode == "collect":
        result = collect_ladder()
    else:
        result = validate_controller()
    summary = {
        "checkpoint": CHECKPOINT,
        "mode": result["mode"],
        "epsilon_id": result.get("epsilon_id"),
        "acceptance_passed": bool(result["acceptance_passed"]),
        "decision": result["decision"],
        "runtime_seconds": result.get("runtime_seconds", time.perf_counter() - started),
    }
    print(json.dumps(summary, sort_keys=True))
    return 0 if bool(result["acceptance_passed"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
