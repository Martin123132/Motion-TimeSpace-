from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time
from typing import Any


for thread_variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[thread_variable] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SCRIPT_5364 = SCRIPTS / "Y5_R2FR_5364_D4_E000625_primary_blind_holdout_runner.py"
SCRIPT_5367 = SCRIPTS / "Y5_R2FR_5367_D4_E0003125_source_complete_event_geometry.py"

SOURCE_CANDIDATES = (
    FUNCTIONAL_RG / "5334" / "E0025" / "D4_outer_support_event_candidates.csv"
)
SOURCE_EVENTS = (
    FUNCTIONAL_RG / "5367" / "E0003125" / "D4_E0003125_refined_events.csv"
)
SOURCE_ANALYTIC_AUDIT = (
    FUNCTIONAL_RG
    / "5367"
    / "E0003125"
    / "D4_E0003125_finite_analytic_event_audit.csv"
)
SOURCE_GEOMETRY_RESULT = (
    FUNCTIONAL_RG / "5367" / "E0003125" / "D4_E0003125_event_geometry_result.json"
)
SOURCE_GEOMETRY_VALIDATION = (
    FUNCTIONAL_RG
    / "5367"
    / "E0003125"
    / "D4_E0003125_event_geometry_validation.csv"
)
FREEZE_ROWS = FUNCTIONAL_RG / "5365" / "D4_E0003125_premeasurement_freeze.csv"
FREEZE_RESULT = (
    FUNCTIONAL_RG / "5365" / "D4_E0003125_premeasurement_freeze_result.json"
)
FREEZE_VALIDATION = (
    FUNCTIONAL_RG / "5365" / "D4_E0003125_premeasurement_freeze_validation.csv"
)
FIVE_RUNG_RESULT = FUNCTIONAL_RG / "5366" / "D4_five_rung_intercept_envelope_result.json"
FIVE_RUNG_VALIDATION = (
    FUNCTIONAL_RG / "5366" / "D4_five_rung_intercept_envelope_validation.csv"
)

OUTPUT = FUNCTIONAL_RG / "5368" / "E0003125"
FROZEN_EVENTS = OUTPUT / "D4_E0003125_preintegration_frozen_events.csv"
POSTDEATH_CONTRACT = OUTPUT / "D4_E0003125_SP_DP_postdeath_absence_contract.csv"
POSTDEATH_SAMPLE = OUTPUT / "D4_E0003125_SP_DP_postdeath_pre_adapter_sample.csv"
POSTDEATH_USAGE = OUTPUT / "D4_E0003125_SP_DP_postdeath_adapter_usage.csv"
LOCAL_REPAIR_CONTRACT = OUTPUT / "D4_E0003125_precomparison_local_repair_contract.csv"
OWNER_SURFACE_FITS = OUTPUT / "D4_E0003125_owner_surface_factor_fits.csv"
OWNER_SURFACE_IDENTITIES = OUTPUT / "D4_E0003125_owner_surface_masked_identity.csv"
FROZEN_ENERGY_AUGMENTATION = OUTPUT / "D4_E0003125_frozen_energy_node_pole_augmentation.csv"
LOCAL_REPAIR_USAGE = OUTPUT / "D4_E0003125_precomparison_local_repair_usage.csv"
RESULT = OUTPUT / "D4_E0003125_blind_holdout_runner_result.json"
VALIDATION = OUTPUT / "D4_E0003125_blind_holdout_runner_validation.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
STATUS = OUTPUT / "status.json"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5368_VALIDATION.csv"
DOCUMENT = POST / "5368-Y5-R2FR-D4-E0003125-preregistered-blind-holdout-runner.md"

CHECKPOINT = 5368
MARKER = "MTS_5368_D4_E0003125_PREREGISTERED_BLIND_HOLDOUT_RUNNER"
REVISION = "D4-E0003125-preregistered-blind-holdout-runner-v2"
EPSILON_ID = "E0003125"
EPSILON = 0.0003125
MAXIMUM_ADAPTIVE_DEPTH = 6
EXPECTED_EVENT_COUNT = 8
EXPECTED_INITIAL_SEGMENT_COUNT = 26
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
EVENT_SOURCE_MODE = "CHECKPOINT_5367_FINITE_ANALYTIC_E0003125_EVENT_GEOMETRY"
OWNER_SURFACE_REPAIR_NODE_IDS = (
    "P08_P08S02_Q04_N01",
    "P10_P10S03_Q04_N01",
    "P10_P10S03_Q08_N02",
    "P10_P10S03_Q08_N03",
    "P10_P10S03_Q08_N04",
    "P10_P10S04_Q04_N01",
    "P10_P10S05_Q04_N02",
    "P10_P10S05_Q04_N03",
    "P10_P10S05_Q04_N04",
    "P10_P10S05_Q08_N03",
)
EXTENDED_ENERGY_REPAIR_NODE_IDS = ("P10_P10S01_Q08_N01",)
OWNER_SURFACE_TERM_ID = "MC04_SM_DM"
OWNER_SURFACE_PRIMARY_SURFACE_ID = "direct:L:s14"
OWNER_SURFACE_FIT_RADIUS_FRACTIONS = (0.1, 0.2)
OWNER_SURFACE_FIT_UNITS = (
    -1.0,
    -0.8,
    -0.65,
    -0.5,
    -0.35,
    -0.2,
    -0.1,
    0.1,
    0.2,
    0.35,
    0.5,
    0.65,
    0.8,
    1.0,
)
OWNER_SURFACE_POLYNOMIAL_DEGREE = 7
OWNER_SURFACE_FIT_RESIDUAL_LIMIT = 1.0e-5
OWNER_NUMERATOR_FIT_RESIDUAL_LIMIT = 1.0e-5
OWNER_SURFACE_ROOT_SCALED_LIMIT = 0.25
OWNER_SURFACE_ROOT_SCALE_CHANGE_LIMIT = 1.0e-2
OWNER_SURFACE_DERIVATIVE_FLOOR = 1.0e-8
OWNER_SURFACE_ENERGY_SUBDIVISIONS = (64, 128, 256)
EXTENDED_ENERGY_SUBDIVISIONS = (128, 256)
LOCAL_REPAIR_REVISION = "E0003125-owner-surface-factor-precomparison-v2"

CLAIM_FIELDS = (
    "valid_for_D4_outer_E0003125_fixed_decay_integral",
    "valid_for_D4_E0003125_complete_family_holdout_compatibility",
    "valid_for_D4_six_rung_complete_second_order_fit",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
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
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


B = load_module("mts_5364_for_5368", SCRIPT_5364)
M5334 = B.M5334
M5326 = B.M5326
M5283 = B.M5283


def no_claims() -> dict[str, bool]:
    return {field: False for field in CLAIM_FIELDS}


def csv_passes(path: Path) -> bool:
    rows = B.read_csv(path)
    return bool(rows) and all(B.parse_bool(row["passed"]) for row in rows)


def target_result_path() -> Path:
    return (
        FUNCTIONAL_RG
        / "5334"
        / EPSILON_ID
        / f"D4_outer_event_aligned_{EPSILON_ID}_result.json"
    )


def accepted_measurement_paths() -> list[str]:
    target = FUNCTIONAL_RG / "5334" / EPSILON_ID
    accepted: list[str] = []
    if target_result_path().is_file():
        result = B.read_json(target_result_path())
        if result.get("acceptance_passed") is True and result.get(
            "completed_full_run"
        ) is True:
            accepted.append(str(target_result_path().resolve()))
    for path in target.glob("*finite_value.csv"):
        if any(
            B.parse_bool(
                row.get("finite_regulator_fixed_decay_integral_accepted", False)
            )
            for row in B.read_csv(path)
        ):
            accepted.append(str(path.resolve()))
    return sorted(set(accepted))


def source_geometry_is_valid() -> tuple[bool, dict[str, Any]]:
    required = (
        Path(__file__).resolve(),
        SCRIPT_5364,
        SCRIPT_5367,
        SOURCE_CANDIDATES,
        SOURCE_EVENTS,
        SOURCE_ANALYTIC_AUDIT,
        SOURCE_GEOMETRY_RESULT,
        SOURCE_GEOMETRY_VALIDATION,
        FREEZE_ROWS,
        FREEZE_RESULT,
        FREEZE_VALIDATION,
        FIVE_RUNG_RESULT,
        FIVE_RUNG_VALIDATION,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        return False, {"missing": missing}
    events = B.read_csv(SOURCE_EVENTS)
    analytic = B.read_csv(SOURCE_ANALYTIC_AUDIT)
    freeze_rows = B.read_csv(FREEZE_ROWS)
    geometry = B.read_json(SOURCE_GEOMETRY_RESULT)
    freeze = B.read_json(FREEZE_RESULT)
    five = B.read_json(FIVE_RUNG_RESULT)
    expected_ids = [f"E{index:02d}" for index in range(1, 9)]
    topology = [row["event_type"] for row in events]
    checks = {
        "checkpoint_5367_geometry_passes": geometry.get("validation_passed") is True
        and geometry.get("claim_boundary", {}).get(
            "valid_for_D4_outer_E0003125_event_geometry"
        )
        is True
        and csv_passes(SOURCE_GEOMETRY_VALIDATION),
        "eight_analytic_events_are_source_owned": len(events)
        == len(analytic)
        == EXPECTED_EVENT_COUNT
        and [row["event_id"] for row in events] == expected_ids
        and [row["event_id"] for row in analytic] == expected_ids
        and all(B.parse_bool(row["event_contract_passes"]) for row in events)
        and all(
            B.parse_bool(row["analytic_finite_event_contract_passes"])
            for row in analytic
        ),
        "event_topology_is_three_entries_four_deaths_one_exit": topology.count(
            "SUPPORT_ENTRY"
        )
        == 3
        and topology.count("BRANCH_DEATH") == 4
        and topology.count("SUPPORT_EXIT") == 1,
        "checkpoint_5365_holdout_was_frozen_before_measurement": freeze.get(
            "validation_passed"
        )
        is True
        and freeze.get("decision")
        == "D4_E0003125_COMPLETE_FAMILY_HOLDOUT_FROZEN_BEFORE_E000625_RESULT"
        and len(freeze_rows) == 1
        and freeze_rows[0]["holdout_epsilon_id"] == EPSILON_ID
        and B.parse_bool(freeze_rows[0]["frozen_before_accepted_E0003125_value"])
        and not B.parse_bool(freeze_rows[0]["comparison_to_measured_holdout_performed"])
        and csv_passes(FREEZE_VALIDATION),
        "checkpoint_5366_five_rung_gate_precedes_sixth_measurement": five.get(
            "validation_passed"
        )
        is True
        and five.get("numerical_intercept_gate_passes") is True
        and five.get("claim_boundary", {}).get(
            "valid_for_D4_outer_regulator_zero_limit"
        )
        is False
        and csv_passes(FIVE_RUNG_VALIDATION),
        "formal_workbench_unchanged": M5283.formal_inventory_digest()
        == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return all(checks.values()), checks


def freeze_events() -> None:
    rows = B.read_csv(SOURCE_EVENTS)
    if FROZEN_EVENTS.is_file():
        if B.digest(FROZEN_EVENTS) != B.digest(SOURCE_EVENTS):
            raise RuntimeError("frozen E0003125 event geometry drifted from checkpoint 5367")
        return
    B.atomic_csv(FROZEN_EVENTS, rows)


def build_postdeath_absence_contract() -> None:
    if POSTDEATH_CONTRACT.is_file() and POSTDEATH_SAMPLE.is_file():
        return
    geometry = B.read_json(SOURCE_GEOMETRY_RESULT)
    events = B.read_csv(SOURCE_EVENTS)
    sp_dp_events = [row for row in events if row["term_id"] == "MC04_SP_DP"]
    expected = (
        ("E02", "SUPPORT_ENTRY", "direct:L:s01"),
        ("E03", "SUPPORT_ENTRY", "direct:shared:s13"),
        ("E05", "BRANCH_DEATH", "direct:L:s01"),
        ("E06", "BRANCH_DEATH", "direct:shared:s13"),
    )
    observed = tuple(
        (row["event_id"], row["event_type"], row["primary_surface_id"])
        for row in sp_dp_events
    )
    if (
        observed != expected
        or geometry.get("validation_passed") is not True
        or geometry.get("event_count") != EXPECTED_EVENT_COUNT
        or not all(B.parse_bool(row["event_contract_passes"]) for row in sp_dp_events)
    ):
        raise RuntimeError(f"SP_DP post-death topology is not source-complete: {observed}")
    death_rows = [row for row in sp_dp_events if row["event_type"] == "BRANCH_DEATH"]
    last_death_coordinate = max(float(row["event_coordinate"]) for row in death_rows)
    contract_rows = [
        {
            "epsilon_id": EPSILON_ID,
            "epsilon": EPSILON,
            "term_id": "MC04_SP_DP",
            "primary_surface_id": row["primary_surface_id"],
            "entry_event_id": "E02" if row["primary_surface_id"] == "direct:L:s01" else "E03",
            "death_event_id": row["event_id"],
            "death_coordinate": row["event_coordinate"],
            "last_term_death_coordinate": last_death_coordinate,
            "branch_active_side": "absolute_soft_cosine_below_death",
            "no_later_term_event_in_source_complete_eight_event_geometry": True,
            "finite_analytic_event_contract_passes": row["event_contract_passes"],
            "source_geometry_path": str(SOURCE_EVENTS.resolve()),
            "source_geometry_sha256": B.digest(SOURCE_EVENTS),
            "source_geometry_result_path": str(SOURCE_GEOMETRY_RESULT.resolve()),
            "source_geometry_result_sha256": B.digest(SOURCE_GEOMETRY_RESULT),
            "valid_for_E0003125_SP_DP_postdeath_branch_absence": True,
            **no_claims(),
        }
        for row in death_rows
    ]
    target_shards = FUNCTIONAL_RG / "5334" / EPSILON_ID / "refinement-shards"
    sample_rows: list[dict[str, Any]] = []
    for result_path in sorted(target_shards.glob("*/result.json")):
        result = B.read_json(result_path)
        coordinate = float(result.get("absolute_soft_cosine", math.nan))
        if (
            result.get("acceptance_passed") is not True
            or not math.isfinite(coordinate)
            or coordinate <= last_death_coordinate
        ):
            continue
        poles_path = result_path.with_name("geometric_poles.csv")
        poles = B.read_csv(poles_path)
        sp_dp_poles = [row for row in poles if row["term_id"] == "MC04_SP_DP"]
        sample_rows.append(
            {
                "node_id": result["node_id"],
                "absolute_soft_cosine": coordinate,
                "last_SP_DP_death_coordinate": last_death_coordinate,
                "node_acceptance_passed": result.get("acceptance_passed") is True,
                "SP_DP_geometric_pole_count": len(sp_dp_poles),
                "pre_adapter_sample": True,
                "node_result_path": str(result_path.resolve()),
                "node_result_sha256": B.digest(result_path),
                "geometric_poles_path": str(poles_path.resolve()),
                "geometric_poles_sha256": B.digest(poles_path),
                "valid_for_E0003125_SP_DP_postdeath_branch_absence_crosscheck": (
                    result.get("acceptance_passed") is True and not sp_dp_poles
                ),
                **no_claims(),
            }
        )
    if len(sample_rows) < 32 or not all(
        B.parse_bool(row["valid_for_E0003125_SP_DP_postdeath_branch_absence_crosscheck"])
        for row in sample_rows
    ):
        raise RuntimeError(
            f"insufficient pre-adapter SP_DP absence sample: {len(sample_rows)}"
        )
    OUTPUT.mkdir(parents=True, exist_ok=True)
    B.atomic_csv(POSTDEATH_CONTRACT, contract_rows)
    B.atomic_csv(POSTDEATH_SAMPLE, sample_rows)


def postdeath_absence_contract_is_valid() -> tuple[bool, dict[str, Any]]:
    if not POSTDEATH_CONTRACT.is_file() or not POSTDEATH_SAMPLE.is_file():
        return False, {"missing": [str(POSTDEATH_CONTRACT), str(POSTDEATH_SAMPLE)]}
    contract = B.read_csv(POSTDEATH_CONTRACT)
    sample = B.read_csv(POSTDEATH_SAMPLE)
    source_hash = B.digest(SOURCE_EVENTS)
    checks = {
        "two_SP_DP_deaths_are_analytic_and_source_complete": len(contract) == 2
        and {row["death_event_id"] for row in contract} == {"E05", "E06"}
        and {row["primary_surface_id"] for row in contract}
        == {"direct:L:s01", "direct:shared:s13"}
        and all(
            B.parse_bool(
                row["no_later_term_event_in_source_complete_eight_event_geometry"]
            )
            and B.parse_bool(row["finite_analytic_event_contract_passes"])
            and B.parse_bool(
                row["valid_for_E0003125_SP_DP_postdeath_branch_absence"]
            )
            and row["source_geometry_sha256"] == source_hash
            for row in contract
        ),
        "pre_adapter_parent_scan_crosscheck_has_no_SP_DP_poles": len(sample) >= 32
        and all(
            B.parse_bool(row["pre_adapter_sample"])
            and B.parse_bool(row["node_acceptance_passed"])
            and int(row["SP_DP_geometric_pole_count"]) == 0
            and B.parse_bool(
                row[
                    "valid_for_E0003125_SP_DP_postdeath_branch_absence_crosscheck"
                ]
            )
            and Path(row["node_result_path"]).is_file()
            and B.digest(Path(row["node_result_path"])) == row["node_result_sha256"]
            and Path(row["geometric_poles_path"]).is_file()
            and B.digest(Path(row["geometric_poles_path"]))
            == row["geometric_poles_sha256"]
            for row in sample
        ),
    }
    return all(checks.values()), checks


def record_postdeath_adapter_use(
    node: dict[str, Any], term_id: str, cutoff: float
) -> None:
    rows = B.read_csv(POSTDEATH_USAGE) if POSTDEATH_USAGE.is_file() else []
    key = (str(node["node_id"]), term_id)
    if any((row["node_id"], row["term_id"]) == key for row in rows):
        return
    rows.append(
        {
            "node_id": node["node_id"],
            "x_panel_index": node["x_panel_index"],
            "outer_order": node["outer_order"],
            "absolute_soft_cosine": node["absolute_soft_cosine"],
            "term_id": term_id,
            "last_SP_DP_death_coordinate": cutoff,
            "resolution": "DERIVED_POSTDEATH_BRANCH_ABSENCE__NO_GEOMETRIC_POLES",
            "contract_path": str(POSTDEATH_CONTRACT.resolve()),
            "contract_sha256": B.digest(POSTDEATH_CONTRACT),
            "valid_for_E0003125_SP_DP_postdeath_branch_absence": True,
            **no_claims(),
        }
    )
    B.atomic_csv(POSTDEATH_USAGE, rows)


def install_postdeath_absence_adapter() -> None:
    if getattr(M5334.M5312, "_mts_5368_postdeath_adapter_installed", False):
        return
    valid, detail = postdeath_absence_contract_is_valid()
    if not valid:
        raise RuntimeError(f"SP_DP post-death absence contract failed: {detail}")
    cutoff = max(
        float(row["last_term_death_coordinate"])
        for row in B.read_csv(POSTDEATH_CONTRACT)
    )
    original_scan = M5334.M5312.scan_term_poles

    def scan_term_poles(
        node: dict[str, Any], term_id: str, supports: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        coordinate = float(node["absolute_soft_cosine"])
        if term_id == "MC04_SP_DP" and coordinate > cutoff + 1.0e-11:
            record_postdeath_adapter_use(node, term_id, cutoff)
            return []
        return original_scan(node, term_id, supports)

    M5334.M5312.scan_term_poles = scan_term_poles
    M5334.M5312._mts_5368_postdeath_adapter_installed = True


def upsert_rows(
    path: Path,
    new_rows: list[dict[str, Any]],
    key_fields: tuple[str, ...],
) -> None:
    existing = B.read_csv(path) if path.is_file() else []
    new_keys = {
        tuple(str(row.get(field, "")) for field in key_fields)
        for row in new_rows
    }
    retained = [
        row
        for row in existing
        if tuple(str(row.get(field, "")) for field in key_fields) not in new_keys
    ]
    B.atomic_csv(path, retained + new_rows)


def build_local_repair_contract() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for node_id in OWNER_SURFACE_REPAIR_NODE_IDS:
        source = (
            FUNCTIONAL_RG
            / "5334"
            / EPSILON_ID
            / "refinement-shards"
            / node_id
            / "geometric_poles.csv"
        )
        if not source.is_file():
            raise RuntimeError(f"missing frozen owner-surface source shard: {source}")
        geometric = [
            row
            for row in B.read_csv(source)
            if row["term_id"] == OWNER_SURFACE_TERM_ID
            and row["primary_surface_id"] == OWNER_SURFACE_PRIMARY_SURFACE_ID
            and B.parse_bool(row["inside_reduced_term_support"])
        ]
        if len(geometric) != 1:
            raise RuntimeError(
                f"owner-surface repair source is not unique for {node_id}"
            )
        rows.append(
            {
                "node_id": node_id,
                "repair_mode": "EXACT_OWNER_SURFACE_FACTOR",
                "term_id": OWNER_SURFACE_TERM_ID,
                "pole_id": geometric[0]["pole_id"],
                "primary_surface_id": OWNER_SURFACE_PRIMARY_SURFACE_ID,
                "fit_radius_fractions": "|".join(
                    f"{value:.17g}" for value in OWNER_SURFACE_FIT_RADIUS_FRACTIONS
                ),
                "fit_units": "|".join(
                    f"{value:.17g}" for value in OWNER_SURFACE_FIT_UNITS
                ),
                "polynomial_degree": OWNER_SURFACE_POLYNOMIAL_DEGREE,
                "energy_subdivision_ladder": "|".join(
                    str(value) for value in OWNER_SURFACE_ENERGY_SUBDIVISIONS
                ),
                "source_path": str(source.resolve()),
                "source_sha256_at_freeze": B.digest(source),
                "repair_revision": LOCAL_REPAIR_REVISION,
                "selection_uses_frozen_prediction": False,
                "selection_uses_provisional_integral_value": False,
                **no_claims(),
            }
        )
    for node_id in EXTENDED_ENERGY_REPAIR_NODE_IDS:
        classification_source = (
            FUNCTIONAL_RG
            / "5334"
            / EPSILON_ID
            / "refinement-shards"
            / node_id
            / "pole_classification.csv"
        )
        fit_source = classification_source.with_name("pole_residue_fits.csv")
        if not classification_source.is_file() or not fit_source.is_file():
            raise RuntimeError(
                f"missing frozen energy-repair source shard: {classification_source}"
            )
        if not FROZEN_ENERGY_AUGMENTATION.is_file():
            classifications = [
                row
                for row in B.read_csv(classification_source)
                if row["term_id"] == OWNER_SURFACE_TERM_ID
                and row["pole_id"] == "MC04_P01"
                and B.parse_bool(row["pole_classification_resolved"])
                and B.parse_bool(row["material_simple_pole"])
            ]
            if len(classifications) != 1:
                raise RuntimeError("accepted energy-node pole augmentation is not unique")
            fit_rows = [
                row
                for row in B.read_csv(fit_source)
                if row["term_id"] == OWNER_SURFACE_TERM_ID
                and row["pole_id"] == "MC04_P01"
            ]
            if not fit_rows:
                raise RuntimeError("accepted energy-node pole fit rows are absent")
            frozen_rows = [
                {
                    "frozen_row_type": "CLASSIFICATION",
                    "frozen_node_id": node_id,
                    **classifications[0],
                },
                *[
                    {
                        "frozen_row_type": "FIT",
                        "frozen_node_id": node_id,
                        **row,
                    }
                    for row in fit_rows
                ],
            ]
            B.atomic_csv(FROZEN_ENERGY_AUGMENTATION, frozen_rows)
        source = FROZEN_ENERGY_AUGMENTATION
        rows.append(
            {
                "node_id": node_id,
                "repair_mode": "PRESERVE_ACCEPTED_POLE_FIT_EXTEND_ENERGY_PARTITION",
                "term_id": OWNER_SURFACE_TERM_ID,
                "pole_id": "MC04_P01",
                "primary_surface_id": OWNER_SURFACE_PRIMARY_SURFACE_ID,
                "fit_radius_fractions": "",
                "fit_units": "",
                "polynomial_degree": "",
                "energy_subdivision_ladder": "|".join(
                    str(value) for value in EXTENDED_ENERGY_SUBDIVISIONS
                ),
                "source_path": str(source.resolve()),
                "source_sha256_at_freeze": B.digest(source),
                "repair_revision": LOCAL_REPAIR_REVISION,
                "selection_uses_frozen_prediction": False,
                "selection_uses_provisional_integral_value": False,
                **no_claims(),
            }
        )
    OUTPUT.mkdir(parents=True, exist_ok=True)
    B.atomic_csv(LOCAL_REPAIR_CONTRACT, rows)
    return rows


def local_repair_contract_is_valid() -> tuple[bool, dict[str, Any]]:
    if not LOCAL_REPAIR_CONTRACT.is_file():
        return False, {"missing": str(LOCAL_REPAIR_CONTRACT)}
    rows = B.read_csv(LOCAL_REPAIR_CONTRACT)
    expected = set(OWNER_SURFACE_REPAIR_NODE_IDS) | set(
        EXTENDED_ENERGY_REPAIR_NODE_IDS
    )
    observed = {row["node_id"] for row in rows}
    sources_current = all(
        Path(row["source_path"]).is_file()
        and B.digest(Path(row["source_path"])) == row["source_sha256_at_freeze"]
        for row in rows
    )
    prediction_silent = all(
        not B.parse_bool(row["selection_uses_frozen_prediction"])
        and not B.parse_bool(row["selection_uses_provisional_integral_value"])
        for row in rows
    )
    valid = (
        len(rows) == len(expected)
        and observed == expected
        and sources_current
        and prediction_silent
        and all(row["repair_revision"] == LOCAL_REPAIR_REVISION for row in rows)
    )
    return valid, {
        "row_count": len(rows),
        "expected_node_count": len(expected),
        "sources_current": sources_current,
        "prediction_silent": prediction_silent,
    }


def owner_surface_source_problem(
    node: dict[str, Any],
    geometric: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    specification = M5326.M5312.M5308.SURFACE_LOOKUP[geometric["term_id"]]
    coordinate = float(node["absolute_soft_cosine"])
    problem = M5326.M5312.M5311.synthetic_energy_problem(
        "MC04",
        int(specification["soft_sign"]) * coordinate,
        int(specification["decay_sign"])
        * M5326.M5312.M5308.M5302.EDGE_DECAY_ABSOLUTE,
    )
    _, _, poles, _ = M5326.M5312.M5291.M5267.M5239.scan_problem(problem)
    matching = [
        row
        for row in poles
        if row["pole_id"] == geometric["pole_id"]
        and row["primary_surface_id"] == geometric["primary_surface_id"]
    ]
    if len(matching) != 1:
        raise RuntimeError(
            f"source owner surface is not unique for {node['node_id']}"
        )
    return problem, matching[0]


def owner_surface_factor_augmentation(
    node: dict[str, Any],
    base_context: dict[str, Any],
) -> dict[str, Any] | None:
    paths = M5326.M5312.shard_paths(str(node["node_id"]))
    if not paths["poles"].is_file():
        return None
    geometric_rows = [
        row
        for row in B.read_csv(paths["poles"])
        if row["term_id"] == OWNER_SURFACE_TERM_ID
        and row["primary_surface_id"] == OWNER_SURFACE_PRIMARY_SURFACE_ID
        and B.parse_bool(row["inside_reduced_term_support"])
    ]
    if len(geometric_rows) != 1:
        return None
    geometric = geometric_rows[0]
    problem, source_pole = owner_surface_source_problem(node, geometric)
    coordinate = float(node["absolute_soft_cosine"])
    lower = float(geometric["support_energy_lower"])
    upper = float(geometric["support_energy_upper"])
    initial_pole = complex(
        float(source_pole["pole_real"]),
        float(source_pole["pole_imaginary"]),
    )
    center = initial_pole.real
    boundary_distance = min(center - lower, upper - center)
    if boundary_distance <= 0.0:
        return None
    evaluate_unmasked = M5326.near_support_unmasked_evaluator(
        base_context,
        OWNER_SURFACE_TERM_ID,
    )
    owner_surface_values = (
        M5326.M5312.M5291.M5267.M5239.owner_surface_values
    )
    np = M5326.M5312.np
    unit_vector = np.asarray(OWNER_SURFACE_FIT_UNITS, dtype=np.complex128)
    matrix = np.column_stack(
        [
            unit_vector**power
            for power in range(OWNER_SURFACE_POLYNOMIAL_DEGREE + 1)
        ]
    )
    fits: list[dict[str, Any]] = []
    for radius_fraction in OWNER_SURFACE_FIT_RADIUS_FRACTIONS:
        radius = radius_fraction * boundary_distance
        surface_samples: list[complex] = []
        numerator_samples: list[complex] = []
        metadata: list[dict[str, Any]] = []
        for unit in OWNER_SURFACE_FIT_UNITS:
            energy = center + unit * radius
            evaluation = evaluate_unmasked(energy, coordinate)
            surface = complex(
                owner_surface_values(problem, complex(energy))[
                    source_pole["primary_surface_id"]
                ]
            )
            surface_samples.append(surface)
            numerator_samples.append(surface * complex(evaluation["value"]))
            metadata.append(evaluation)
        surface_vector = np.asarray(surface_samples, dtype=np.complex128)
        numerator_vector = np.asarray(numerator_samples, dtype=np.complex128)
        surface_coefficients, _, _, _ = np.linalg.lstsq(
            matrix,
            surface_vector,
            rcond=None,
        )
        numerator_coefficients, _, _, _ = np.linalg.lstsq(
            matrix,
            numerator_vector,
            rcond=None,
        )
        surface_residual = float(
            np.linalg.norm(matrix @ surface_coefficients - surface_vector)
            / max(np.linalg.norm(surface_vector), 1.0e-300)
        )
        numerator_residual = float(
            np.linalg.norm(matrix @ numerator_coefficients - numerator_vector)
            / max(np.linalg.norm(numerator_vector), 1.0)
        )
        candidate_roots = np.polynomial.polynomial.polyroots(surface_coefficients)
        scaled_initial = (initial_pole - center) / radius
        finite_roots = [
            complex(value)
            for value in candidate_roots
            if math.isfinite(float(value.real)) and math.isfinite(float(value.imag))
        ]
        if not finite_roots:
            raise RuntimeError("owner-surface polynomial has no finite root")
        scaled_root = min(finite_roots, key=lambda value: abs(value - scaled_initial))
        refined_pole = center + radius * scaled_root
        surface_derivative = sum(
            power
            * complex(surface_coefficients[power])
            * scaled_root ** (power - 1)
            for power in range(1, len(surface_coefficients))
        ) / radius
        numerator_at_pole = sum(
            complex(numerator_coefficients[power]) * scaled_root**power
            for power in range(len(numerator_coefficients))
        )
        residue = (
            numerator_at_pole / surface_derivative
            if abs(surface_derivative) > 0.0
            else complex(math.inf, math.inf)
        )
        topology_state_count = len(
            {
                (
                    bool(row["mask_active"]),
                    int(row["orientation"]),
                    str(row["selected_labels"]),
                    str(row["selected_role"]),
                )
                for row in metadata
            }
        )
        topology_passes = topology_state_count == 1 and all(
            bool(row["mask_active"]) for row in metadata
        )
        fits.append(
            {
                "node_id": str(node["node_id"]),
                "fit_row_type": "OWNER_SURFACE_FACTOR_POLYNOMIAL",
                "term_id": OWNER_SURFACE_TERM_ID,
                "support_id": geometric["support_id"],
                "pole_id": geometric["pole_id"],
                "primary_surface_id": source_pole["primary_surface_id"],
                "fit_scale": radius_fraction,
                "fit_radius": radius,
                "fit_sample_count": len(OWNER_SURFACE_FIT_UNITS),
                "polynomial_degree": OWNER_SURFACE_POLYNOMIAL_DEGREE,
                **M5326.complex_fields("geometric_pole", initial_pole),
                **M5326.complex_fields("refined_pole", refined_pole),
                **M5326.complex_fields("surface_derivative", surface_derivative),
                **M5326.complex_fields(
                    "regular_numerator_at_pole",
                    numerator_at_pole,
                ),
                **M5326.complex_fields("fitted_residue", residue),
                "surface_fit_relative_residual": surface_residual,
                "numerator_fit_relative_residual": numerator_residual,
                "scaled_root_magnitude": abs(scaled_root),
                "topology_state_count": topology_state_count,
                "topology_preflight_passes": topology_passes,
                "repair_revision": LOCAL_REPAIR_REVISION,
                **no_claims(),
            }
        )
    first, second = fits
    first_pole = complex(
        float(first["refined_pole_real"]),
        float(first["refined_pole_imaginary"]),
    )
    second_pole = complex(
        float(second["refined_pole_real"]),
        float(second["refined_pole_imaginary"]),
    )
    first_residue = complex(
        float(first["fitted_residue_real"]),
        float(first["fitted_residue_imaginary"]),
    )
    second_residue = complex(
        float(second["fitted_residue_real"]),
        float(second["fitted_residue_imaginary"]),
    )
    pole_core = max(abs(first_pole.imag), abs(second_pole.imag), 1.0e-12)
    pole_scale_change = abs(first_pole - second_pole) / pole_core
    residue_scale_change = M5326.M5312.relative_complex_change(
        first_residue,
        second_residue,
    )
    fit_contract_passes = (
        all(
            float(row["surface_fit_relative_residual"])
            <= OWNER_SURFACE_FIT_RESIDUAL_LIMIT
            and float(row["numerator_fit_relative_residual"])
            <= OWNER_NUMERATOR_FIT_RESIDUAL_LIMIT
            and float(row["scaled_root_magnitude"])
            <= OWNER_SURFACE_ROOT_SCALED_LIMIT
            and float(row["surface_derivative_magnitude"])
            >= OWNER_SURFACE_DERIVATIVE_FLOOR
            and B.parse_bool(row["topology_preflight_passes"])
            for row in fits
        )
        and pole_scale_change <= OWNER_SURFACE_ROOT_SCALE_CHANGE_LIMIT
        and residue_scale_change <= M5326.NEAR_SUPPORT_RESIDUE_SCALE_CHANGE_LIMIT
        and min(abs(first_residue), abs(second_residue))
        >= M5326.M5312.MATERIAL_RESIDUE_FLOOR
        and lower < first_pole.real < upper
        and lower < second_pole.real < upper
    )
    selected = {
        "refined_pole": second_pole,
        "selected_residue": second_residue,
        "support_energy_lower": lower,
        "support_energy_upper": upper,
        "active_support_boundary": M5326.active_support_fit_geometry(
            second_pole,
            lower,
            upper,
        )[2],
        "active_support_direction": M5326.active_support_fit_geometry(
            second_pole,
            lower,
            upper,
        )[1],
    }
    identity_rows, identity_passes = M5326.near_support_masked_identity_audit(
        coordinate,
        OWNER_SURFACE_TERM_ID,
        selected,
        evaluate_unmasked,
        M5326.M5312.M5305.component_evaluator(base_context),
    )
    contract_passes = fit_contract_passes and identity_passes
    for row in fits:
        row["pole_scale_change_in_core_units"] = pole_scale_change
        row["residue_fit_scale_relative_change"] = residue_scale_change
        row["masked_identity_passes"] = identity_passes
        row["owner_surface_factor_contract_passes"] = contract_passes
    identity_rows = [
        {
            "node_id": str(node["node_id"]),
            "term_id": OWNER_SURFACE_TERM_ID,
            "pole_id": geometric["pole_id"],
            "primary_surface_id": source_pole["primary_surface_id"],
            **row,
            "repair_revision": LOCAL_REPAIR_REVISION,
            **no_claims(),
        }
        for row in identity_rows
    ]
    upsert_rows(OWNER_SURFACE_FITS, fits, ("node_id", "fit_scale"))
    upsert_rows(
        OWNER_SURFACE_IDENTITIES,
        identity_rows,
        ("node_id", "sample_index"),
    )
    classification = {
        "node_id": str(node["node_id"]),
        "x_panel_index": int(node["x_panel_index"]),
        "outer_order": int(node["outer_order"]),
        "absolute_soft_cosine": coordinate,
        "term_id": OWNER_SURFACE_TERM_ID,
        "support_id": geometric["support_id"],
        "pole_id": geometric["pole_id"],
        "primary_surface_id": source_pole["primary_surface_id"],
        "pole_real": second_pole.real,
        "pole_imaginary": second_pole.imag,
        **M5326.complex_fields("selected_residue", second_residue),
        "maximum_fit_relative_residual": max(
            max(float(row["surface_fit_relative_residual"]) for row in fits),
            max(float(row["numerator_fit_relative_residual"]) for row in fits),
        ),
        "fit_residue_relative_change": residue_scale_change,
        "all_fit_samples_mask_active": contract_passes,
        "owner_surface_factor_fit_used": True,
        "owner_surface_root_scale_change_in_core_units": pole_scale_change,
        "owner_surface_masked_identity_passes": identity_passes,
        "material_simple_pole": contract_passes,
        "removable_zero_residue_pole": False,
        "pole_classification_resolved": contract_passes,
        "failure_reason": "" if contract_passes else "OWNER_SURFACE_FACTOR_GATE_FAILED",
        "valid_for_pole_subtracted_outer_soft_node": contract_passes,
        "repair_revision": LOCAL_REPAIR_REVISION,
        **no_claims(),
    }
    return {
        "fit_rows": fits,
        "classification": classification,
        "contract_passes": contract_passes,
        "selected": selected,
    }


def frozen_energy_augmentation(node: dict[str, Any]) -> dict[str, Any] | None:
    if not FROZEN_ENERGY_AUGMENTATION.is_file():
        return None
    rows = [
        row
        for row in B.read_csv(FROZEN_ENERGY_AUGMENTATION)
        if row["frozen_node_id"] == str(node["node_id"])
    ]
    classifications = [
        row for row in rows if row["frozen_row_type"] == "CLASSIFICATION"
    ]
    fits = [row for row in rows if row["frozen_row_type"] == "FIT"]
    if len(classifications) != 1 or not fits:
        return None
    classification = dict(classifications[0])
    for field in (
        "all_fit_samples_mask_active",
        "near_support_unmasked_fit_used",
        "near_support_masked_identity_passes",
        "material_simple_pole",
        "removable_zero_residue_pole",
        "pole_classification_resolved",
        "valid_for_pole_subtracted_outer_soft_node",
    ):
        if field in classification:
            classification[field] = B.parse_bool(classification[field])
    contract_passes = (
        B.parse_bool(classification["pole_classification_resolved"])
        and B.parse_bool(classification["material_simple_pole"])
        and B.parse_bool(classification["all_fit_samples_mask_active"])
        and B.parse_bool(classification["near_support_masked_identity_passes"])
    )
    return {
        "fit_rows": fits,
        "classification": classification,
        "contract_passes": contract_passes,
    }


def record_local_repair_usage(row: dict[str, Any]) -> None:
    upsert_rows(
        LOCAL_REPAIR_USAGE,
        [{**row, "repair_revision": LOCAL_REPAIR_REVISION, **no_claims()}],
        ("node_id", "energy_panel_subdivisions"),
    )


def run_node_with_augmentation(
    node: dict[str, Any],
    contract: list[dict[str, str]],
    expected_plan_sha256: str,
    base_context: dict[str, Any],
    multiplier: float,
    result: dict[str, Any],
    augmentation: dict[str, Any],
    repair_mode: str,
    subdivision_ladder: tuple[int, ...],
) -> dict[str, Any]:
    classification = dict(augmentation["classification"])
    fit_rows = [dict(row) for row in augmentation["fit_rows"]]
    replacement_key = (classification["term_id"], classification["pole_id"])
    old_fit_node_poles = M5326.M5312.fit_node_poles
    old_energy_panel_rows = M5326.M5312.energy_panel_rows
    baseline_change = float(result["inner_Q4_Q8_relative_change"])
    baseline_budget = float(result["inner_energy_error_budget_relative"])

    def fit_node_poles_with_augmentation(
        local_node: dict[str, Any],
        poles: list[dict[str, Any]],
        evaluate: Any,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        fits, classifications = old_fit_node_poles(local_node, poles, evaluate)
        if str(local_node["node_id"]) != str(node["node_id"]):
            return fits, classifications
        fits = [
            row
            for row in fits
            if (row["term_id"], row["pole_id"]) != replacement_key
        ]
        classifications = [
            row
            for row in classifications
            if (row["term_id"], row["pole_id"]) != replacement_key
        ]
        fits.extend(fit_rows)
        classifications.append(classification)
        return fits, classifications

    final = result
    try:
        M5326.M5312.fit_node_poles = fit_node_poles_with_augmentation
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
            final["precomparison_local_repair_applied"] = True
            final["precomparison_local_repair_mode"] = repair_mode
            final["precomparison_local_repair_revision"] = LOCAL_REPAIR_REVISION
            final["precomparison_energy_panel_subdivisions"] = subdivisions
            final["pre_repair_inner_Q4_Q8_relative_change"] = baseline_change
            final["pre_repair_inner_energy_error_budget_relative"] = baseline_budget
            M5326.atomic_json(
                M5326.M5312.shard_paths(str(node["node_id"]))["result"],
                final,
            )
            record_local_repair_usage(
                {
                    "node_id": str(node["node_id"]),
                    "x_panel_index": int(node["x_panel_index"]),
                    "outer_order": int(node["outer_order"]),
                    "absolute_soft_cosine": float(node["absolute_soft_cosine"]),
                    "repair_mode": repair_mode,
                    "term_id": classification["term_id"],
                    "pole_id": classification["pole_id"],
                    "primary_surface_id": classification.get(
                        "primary_surface_id",
                        OWNER_SURFACE_PRIMARY_SURFACE_ID,
                    ),
                    "energy_panel_subdivisions": subdivisions,
                    "pre_repair_inner_Q4_Q8_relative_change": baseline_change,
                    "post_repair_inner_Q4_Q8_relative_change": final[
                        "inner_Q4_Q8_relative_change"
                    ],
                    "pre_repair_inner_energy_error_budget_relative": baseline_budget,
                    "post_repair_inner_energy_error_budget_relative": final[
                        "inner_energy_error_budget_relative"
                    ],
                    "unresolved_pole_count": final["unresolved_pole_count"],
                    "repair_acceptance_passed": final["acceptance_passed"],
                }
            )
            if bool(final["acceptance_passed"]):
                break
    finally:
        M5326.M5312.fit_node_poles = old_fit_node_poles
        M5326.M5312.energy_panel_rows = old_energy_panel_rows
    return final


_BASE_REPAIR_NODE_ENERGY_RESOLUTION: Any = None


def install_precomparison_local_repair() -> None:
    global _BASE_REPAIR_NODE_ENERGY_RESOLUTION
    _BASE_REPAIR_NODE_ENERGY_RESOLUTION = M5326.repair_node_energy_resolution

    def repair_node_energy_resolution(
        node: dict[str, Any],
        contract: list[dict[str, str]],
        expected_plan_sha256: str,
        base_context: dict[str, Any],
        multiplier: float,
        result: dict[str, Any],
    ) -> dict[str, Any]:
        if bool(result["acceptance_passed"]):
            return result
        node_id = str(node["node_id"])
        if node_id in OWNER_SURFACE_REPAIR_NODE_IDS:
            augmentation = owner_surface_factor_augmentation(node, base_context)
            if augmentation is None or not bool(augmentation["contract_passes"]):
                record_local_repair_usage(
                    {
                        "node_id": node_id,
                        "x_panel_index": int(node["x_panel_index"]),
                        "outer_order": int(node["outer_order"]),
                        "absolute_soft_cosine": float(node["absolute_soft_cosine"]),
                        "repair_mode": "EXACT_OWNER_SURFACE_FACTOR",
                        "term_id": OWNER_SURFACE_TERM_ID,
                        "pole_id": "MC04_P01",
                        "primary_surface_id": OWNER_SURFACE_PRIMARY_SURFACE_ID,
                        "energy_panel_subdivisions": 0,
                        "pre_repair_inner_Q4_Q8_relative_change": result[
                            "inner_Q4_Q8_relative_change"
                        ],
                        "post_repair_inner_Q4_Q8_relative_change": result[
                            "inner_Q4_Q8_relative_change"
                        ],
                        "pre_repair_inner_energy_error_budget_relative": result[
                            "inner_energy_error_budget_relative"
                        ],
                        "post_repair_inner_energy_error_budget_relative": result[
                            "inner_energy_error_budget_relative"
                        ],
                        "unresolved_pole_count": result["unresolved_pole_count"],
                        "repair_acceptance_passed": False,
                    }
                )
                return result
            return run_node_with_augmentation(
                node,
                contract,
                expected_plan_sha256,
                base_context,
                multiplier,
                result,
                augmentation,
                "EXACT_OWNER_SURFACE_FACTOR",
                OWNER_SURFACE_ENERGY_SUBDIVISIONS,
            )
        if node_id in EXTENDED_ENERGY_REPAIR_NODE_IDS:
            augmentation = frozen_energy_augmentation(node)
            if augmentation is not None and bool(augmentation["contract_passes"]):
                return run_node_with_augmentation(
                    node,
                    contract,
                    expected_plan_sha256,
                    base_context,
                    multiplier,
                    result,
                    augmentation,
                    "PRESERVE_ACCEPTED_POLE_FIT_EXTEND_ENERGY_PARTITION",
                    EXTENDED_ENERGY_SUBDIVISIONS,
                )
        return _BASE_REPAIR_NODE_ENERGY_RESOLUTION(
            node,
            contract,
            expected_plan_sha256,
            base_context,
            multiplier,
            result,
        )

    M5326.repair_node_energy_resolution = repair_node_energy_resolution


def target_candidate_rows() -> list[dict[str, Any]]:
    rows = [dict(row) for row in B.read_csv(SOURCE_CANDIDATES)]
    M5334.write_csv(
        M5326.EVENT_CANDIDATES,
        rows,
        ["candidate_id", "x_panel_index", "term_id", "primary_surface_id"],
    )
    return rows


def target_events_only() -> list[dict[str, Any]]:
    valid, detail = source_geometry_is_valid()
    if not valid:
        raise RuntimeError(f"validated E0003125 geometry failed: {detail}")
    rows = [dict(row) for row in B.read_csv(FROZEN_EVENTS)]
    contract_hash = B.digest(M5326.CONTRACT_5325)
    pole_hash = B.digest(M5326.POLES_5325)
    for row in rows:
        row["contract_sha256"] = contract_hash
        row["parent_pole_sha256"] = pole_hash
        row["candidate_source"] = EVENT_SOURCE_MODE
        row["transfer_source_path"] = str(FROZEN_EVENTS.resolve())
        row["transfer_source_sha256"] = B.digest(FROZEN_EVENTS)
    M5334.write_csv(
        M5326.EVENTS,
        rows,
        ["event_id", "x_panel_index", "term_id", "primary_surface_id"],
    )
    return rows


def write_target_event_states() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for event in B.read_csv(FROZEN_EVENTS):
        rows.append(
            {
                "x_panel_index": int(event["x_panel_index"]),
                "term_id": event["term_id"],
                "primary_surface_id": event["primary_surface_id"],
                "absolute_soft_cosine": float(event["event_coordinate"]),
                "branch_exists": True,
                "pole_real": float(event["event_pole_real"]),
                "pole_imaginary": float(event["event_pole_imaginary"]),
                "support_id": f"TRANSFERRED_{event['term_id']}_SUPPORT",
                "support_energy_lower": float(event["event_support_lower"]),
                "support_energy_upper": float(event["event_support_upper"]),
                "signed_support_margin": float(event["event_signed_support_margin"]),
                "inside_reduced_term_support": event["event_type"]
                != "BRANCH_DEATH",
                "state_source": EVENT_SOURCE_MODE,
                **no_claims(),
            }
        )
    M5334.write_csv(
        M5326.EVENT_STATES,
        rows,
        [
            "x_panel_index",
            "term_id",
            "primary_surface_id",
            "absolute_soft_cosine",
        ],
    )
    return rows


def configure_target() -> dict[str, Path]:
    valid, detail = source_geometry_is_valid()
    if not valid:
        raise RuntimeError(f"E0003125 source geometry failed: {detail}")
    build_postdeath_absence_contract()
    M5334.M5327.EPSILON_VALUES[EPSILON_ID] = EPSILON
    M5334.M5327.EXPECTED_IDS = tuple(M5334.M5327.EPSILON_VALUES)
    M5334.M5327.RUN_IDS = tuple(
        value for value in M5334.M5327.EXPECTED_IDS if value != "E0025"
    )
    M5334.M5327.REQUIRED_LOCAL_REPAIR_MODES_BY_EPSILON[EPSILON_ID] = dict(
        M5334.M5327.E000625_REQUIRED_LOCAL_REPAIR_MODES
    )
    M5334.M5327.REQUIRED_LOCAL_REPAIR_REVISION_BY_EPSILON[EPSILON_ID] = (
        M5334.M5327.E000625_REPAIR_REVISION
    )
    M5334.configure_ladder()
    M5334.D4_TARGET_MAXIMUM_ADAPTIVE_DEPTH[EPSILON_ID] = MAXIMUM_ADAPTIVE_DEPTH
    paths = M5334.configure_D4_target(EPSILON_ID)
    expected_source = (FUNCTIONAL_RG / "5334" / EPSILON_ID).resolve()
    if paths["source"].resolve() != expected_source or M5326.SOURCE.resolve() != expected_source:
        raise RuntimeError("refusing cross-channel E0003125 target routing")
    M5334.M5312.shard_is_complete = M5334.d4_target_shard_is_complete
    M5326.EXPECTED_EVENT_COUNT = EXPECTED_EVENT_COUNT
    M5326.event_candidate_rows = target_candidate_rows
    M5326.derive_events = target_events_only
    install_postdeath_absence_adapter()
    build_local_repair_contract()
    install_precomparison_local_repair()
    return paths


def build_dry_run() -> dict[str, Any]:
    freeze_events()
    configure_target()
    dry = M5334.d4_refinement_dry_run()
    write_target_event_states()
    dry["event_source_mode"] = EVENT_SOURCE_MODE
    dry["event_source_path"] = str(FROZEN_EVENTS.resolve())
    dry["event_source_sha256"] = B.digest(FROZEN_EVENTS)
    dry["maximum_adaptive_depth"] = MAXIMUM_ADAPTIVE_DEPTH
    dry["checks"]["checkpoint_5367_E0003125_event_geometry_passes"] = (
        source_geometry_is_valid()[0]
    )
    dry["checks"]["checkpoint_5365_E0003125_holdout_was_frozen"] = True
    dry["acceptance_passed"] = all(dry["checks"].values())
    dry["decision"] = (
        "DRY_RUN_ACCEPTED__RUN_D4_OUTER_E0003125_BLIND_HOLDOUT"
        if dry["acceptance_passed"]
        else "D4_OUTER_E0003125_BLIND_HOLDOUT_DRY_RUN_BLOCKED"
    )
    M5334.atomic_json(M5326.DRY_RUN, dry)
    return dry


def direct_sources() -> tuple[Path, ...]:
    paths = [
        Path(__file__).resolve(),
        SCRIPT_5364,
        SCRIPT_5367,
        SOURCE_CANDIDATES,
        FROZEN_EVENTS,
        SOURCE_ANALYTIC_AUDIT,
        SOURCE_GEOMETRY_RESULT,
        SOURCE_GEOMETRY_VALIDATION,
        FREEZE_ROWS,
        FREEZE_RESULT,
        FREEZE_VALIDATION,
        FIVE_RUNG_RESULT,
        FIVE_RUNG_VALIDATION,
        POSTDEATH_CONTRACT,
        POSTDEATH_SAMPLE,
        LOCAL_REPAIR_CONTRACT,
        FROZEN_ENERGY_AUGMENTATION,
    ]
    paths.extend(
        path
        for path in (
            POSTDEATH_USAGE,
            OWNER_SURFACE_FITS,
            OWNER_SURFACE_IDENTITIES,
            LOCAL_REPAIR_USAGE,
        )
        if path.is_file()
    )
    return tuple(paths)


def write_checkpoint(dry: dict[str, Any]) -> dict[str, Any]:
    valid, source_checks = source_geometry_is_valid()
    validations = [
        B.validation_row("source_geometry_and_freeze_pass", valid, source_checks),
        B.validation_row(
            "SP_DP_postdeath_absence_contract_passes",
            postdeath_absence_contract_is_valid()[0],
            postdeath_absence_contract_is_valid()[1],
        ),
        B.validation_row(
            "precomparison_local_repair_contract_is_frozen_and_prediction_silent",
            local_repair_contract_is_valid()[0],
            local_repair_contract_is_valid()[1],
        ),
        B.validation_row(
            "dry_run_passes_with_eight_events",
            dry.get("acceptance_passed") is True
            and int(dry.get("refined_event_count", -1)) == EXPECTED_EVENT_COUNT
            and int(dry.get("initial_segment_count", -1))
            == EXPECTED_INITIAL_SEGMENT_COUNT,
            dry.get("decision"),
        ),
        B.validation_row(
            "depth_six_is_preregistered_before_E0003125_integration",
            int(dry.get("maximum_adaptive_depth", -1)) == MAXIMUM_ADAPTIVE_DEPTH,
            dry.get("node_plan_sha256"),
        ),
        B.validation_row(
            "E0003125_measurement_is_absent_at_runner_freeze",
            not accepted_measurement_paths(),
            accepted_measurement_paths(),
        ),
        B.validation_row(
            "D4_target_is_routed_only_to_5334_E0003125",
            M5326.SOURCE.resolve()
            == (FUNCTIONAL_RG / "5334" / EPSILON_ID).resolve(),
            M5326.SOURCE.resolve(),
        ),
        B.validation_row(
            "all_holdout_and_broad_claims_remain_false",
            all(value is False for value in no_claims().values()),
            no_claims(),
        ),
        B.validation_row(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest() == FORMAL_DIGEST,
            M5283.formal_inventory_digest(),
        ),
        B.validation_row(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            SCRIPTS / "__pycache__",
        ),
    ]
    passed = all(B.parse_bool(row["passed"]) for row in validations)
    source_rows = [
        {
            "path": str(path.resolve()),
            "sha256": B.digest(path),
            "exists": path.is_file(),
            **no_claims(),
        }
        for path in direct_sources()
    ]
    result = {
        "mode": "D4-E0003125-preregistered-blind-holdout-runner",
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "epsilon_id": EPSILON_ID,
        "epsilon": EPSILON,
        "validation_passed": passed,
        "decision": (
            "D4_E0003125_BLIND_HOLDOUT_DEPTH6_PREREGISTERED__RUN_RESUMABLE_INTEGRAL"
            if passed
            else "D4_E0003125_SOURCE_GEOMETRY_OR_DRY_RUN_BLOCKED"
        ),
        "event_count": dry.get("refined_event_count"),
        "initial_segment_count": dry.get("initial_segment_count"),
        "maximum_adaptive_depth": dry.get("maximum_adaptive_depth"),
        "node_plan_sha256": dry.get("node_plan_sha256"),
        "local_repair_revision": LOCAL_REPAIR_REVISION,
        "owner_surface_factor_node_count": len(OWNER_SURFACE_REPAIR_NODE_IDS),
        "extended_energy_partition_node_count": len(
            EXTENDED_ENERGY_REPAIR_NODE_IDS
        ),
        "frozen_prediction_source_path": str(FREEZE_ROWS.resolve()),
        "frozen_prediction_source_sha256": B.digest(FREEZE_ROWS),
        "event_source_path": str(FROZEN_EVENTS.resolve()),
        "event_source_sha256": B.digest(FROZEN_EVENTS),
        "claim_boundary": no_claims(),
        "formalization_workbench_modified_file_count": 0,
        "updated_utc": B.utc_now(),
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    B.atomic_csv(VALIDATION, validations)
    B.atomic_csv(RESIDUAL_VALIDATION, validations)
    B.atomic_csv(SOURCE_REGISTER, source_rows)
    B.atomic_json(RESULT, result)
    B.atomic_json(
        STATUS,
        {
            "state": "complete" if passed else "blocked",
            "decision": result["decision"],
            "updated_utc": result["updated_utc"],
        },
    )
    DOCUMENT.write_text(
        "\n".join(
            [
                "# 5368 - D4 E0003125 preregistered blind holdout runner",
                "",
                "## Decision",
                "",
                f"`{result['decision']}`",
                "",
                "Checkpoint 5365 froze this sixth-rung prediction before measurement. Checkpoint 5367 independently derived its finite-Q eight-event geometry. Depth six and the exact node plan are now frozen before integration.",
                "",
                f"- events: `{result['event_count']}`;",
                f"- initial segments: `{result['initial_segment_count']}`;",
                f"- maximum adaptive depth: `{result['maximum_adaptive_depth']}`;",
                f"- plan hash: `{result['node_plan_sha256']}`.",
                "",
                "The pre-comparison numerical repair is also frozen. Ten unresolved in-support poles are factored by their exact owner surface, the regular numerator and owner surface are fitted independently on two support-relative radii, and the residue is their ratio at the fitted simple zero. One already accepted pole fit is preserved while its energy partition is extended. Neither rule reads the frozen prediction or the provisional integral value.",
                "",
                "No measured holdout, six-rung fit, regulator-zero, angular, UV, local-GR, or full-MTS claim is made by this setup checkpoint.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return result


def run_integral(runtime_seconds: float) -> dict[str, Any]:
    configure_target()
    dry = M5334.d4_load_validated_refinement_dry_run()
    if dry.get("event_source_mode") != EVENT_SOURCE_MODE:
        dry = build_dry_run()
    write_target_event_states()
    raw = M5326.execute(runtime_seconds)
    source_paths = {
        Path(row["path"])
        for row in raw.get("source_files", [])
        if Path(row["path"]).is_file()
    }
    source_paths.update(direct_sources())
    raw["source_files"] = [
        {"path": str(path.resolve()), "sha256": B.digest(path)}
        for path in sorted(source_paths, key=lambda path: str(path).lower())
    ]
    result = M5334.canonicalize_refinement_result(raw)
    print(
        json.dumps(
            {
                "mode": "run",
                "epsilon_id": EPSILON_ID,
                "acceptance_passed": result["acceptance_passed"],
                "decision": result["decision"],
                "completed_full_run": result["completed_full_run"],
                "encountered_node_count": result["encountered_node_count"],
                "completed_node_count": result["completed_node_count"],
                "runtime_seconds": result["runtime_seconds"],
            },
            sort_keys=True,
        )
    )
    return result


def validate_integral() -> dict[str, Any]:
    configure_target()
    return M5334.validate_refinement_outputs()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "run", "validate"), required=True)
    parser.add_argument("--max-runtime-hours", type=float, default=4.0)
    arguments = parser.parse_args()
    M5334.M5312.set_below_normal_priority()
    started = time.perf_counter()
    if arguments.mode == "dry-run":
        dry = build_dry_run()
        payload = write_checkpoint(dry)
        payload["runtime_seconds"] = time.perf_counter() - started
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif arguments.mode == "run":
        payload = run_integral(max(arguments.max_runtime_hours, 0.0) * 3600.0)
    else:
        payload = validate_integral()
        print(json.dumps(payload, indent=2, sort_keys=True))
    accepted = payload.get("validation_passed", payload.get("acceptance_passed", False))
    paused = "PAUSED" in str(payload.get("decision", ""))
    return 0 if accepted or paused else 1


if __name__ == "__main__":
    raise SystemExit(main())
