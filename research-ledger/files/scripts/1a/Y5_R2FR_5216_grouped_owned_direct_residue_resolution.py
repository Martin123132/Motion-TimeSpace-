from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import mpmath as mp


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5216"
RUN = SOURCE / "runs" / "grouped_owned_direct_resolution_v1"
ITEMS = RUN / "items"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SCRIPT_5112 = (
    POST
    / "scripts"
    / "Y5_R2FR_5112_recoil_holomorphy_scope_correction.py"
)
SCRIPT_5215 = (
    POST
    / "scripts"
    / "Y5_R2FR_5215_fresh_A00_permutation_control_pilot.py"
)
SCRIPT_5215_TRANSPORT = (
    POST
    / "scripts"
    / "Y5_R2FR_5215_transport_invalid_full_homotopy_repair.py"
)
SOURCE_5215 = POST / "source-intake" / "functional_rg" / "5215"
PROTOCOL_LOCK_5215 = SOURCE_5215 / "frozen_A00_control_pilot_lock.json"
TRANSPORT_LOCK_5215 = SOURCE_5215 / "frozen_transport_repair_lock.json"
SOURCE_JOB = (
    SOURCE_5215
    / "runs"
    / "fresh_A00_control_pilot_v1"
    / "topological-jobs"
    / "TOP__E040__S521509_N0000__A00__primary24.json"
)
SOURCE_TOPOLOGY = (
    SOURCE_5215
    / "runs"
    / "fresh_A00_control_pilot_v1"
    / "topologies"
    / "S521509_N0000__E040_A00.json"
)
LOCK = SOURCE / "grouped_owned_direct_precision_lock.json"
EXTRACTION = SOURCE / "S521509_E040_A00_catalog_extraction.json"
AUDIT = SOURCE / "S521509_E040_A00_grouped_direct_audit.json"
AUDIT_CSV = SOURCE / "S521509_E040_A00_grouped_direct_audit.csv"
REPLACEMENTS = SOURCE / "event_local_grouped_direct_replacements.json"
RESULT = SOURCE / "grouped_owned_direct_residue_resolution.json"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5216_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5216-Y5-R2FR-grouped-owned-direct-residue-resolution.md"
)
MARKER = "MTS_5216_GROUPED_OWNED_DIRECT_RESIDUE_RESOLUTION"
REVISION = "event-local-linear-sum-arbitrary-precision-resolution-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
JOB_KEY = "TOP__E040__S521509_N0000__A00__primary24"
EVENT_ID = "S521509_N0000"
ARGUMENT_ID = "E040_A00"
ZERO_TOLERANCE = 1.0e-20
MINIMUM_NONZERO_MAGNITUDE = 1.0e-14
MAXIMUM_RELATIVE_SPREAD = 1.0e-8
MAXIMUM_CROSS_LEVEL_RELATIVE_CHANGE = 1.0e-8
LEVELS = (
    {
        "level_id": "L32",
        "dps": 80,
        "relative_nodes": 32,
        "global_nodes": 32,
        "relative_fractions": (0.1, 0.05, 0.025),
        "global_fractions": (0.1, 0.2, 0.3),
    },
    {
        "level_id": "L48",
        "dps": 100,
        "relative_nodes": 48,
        "global_nodes": 48,
        "relative_fractions": (0.1, 0.05, 0.025),
        "global_fractions": (0.15, 0.3),
    },
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5215 = load_module("mts_5215_for_5216", SCRIPT_5215)
M5112 = load_module("mts_5112_for_5216", SCRIPT_5112)


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


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def complex_row(value: complex | mp.mpc) -> dict[str, str]:
    return {
        "real": mp.nstr(mp.re(value), 60),
        "imaginary": mp.nstr(mp.im(value), 60),
    }


def row_complex(value: dict[str, Any]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


def json_ready(value: Any) -> Any:
    if isinstance(value, complex):
        return str(value)
    if isinstance(value, dict):
        return {
            str(key): json_ready(item)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    return value


def canonical_pairs(value: list[list[str]]) -> list[list[str]]:
    return [
        list(pair)
        for pair in sorted(
            tuple(sorted((str(pair[0]), str(pair[1])))) for pair in value
        )
    ]


def install_parent_runtime() -> tuple[dict[str, Any], Any]:
    config = M5215.read_json(M5215.FROZEN_CONFIG)
    run_directory = (
        SOURCE_5215 / "runs" / "fresh_A00_control_pilot_v1"
    )
    M5215.M5212.source_separated_cluster_gate()
    M5215.M5212.M5077.certified_primary_catalog = (
        M5215.M5212.certified_5212_catalog
    )
    M5215.M5212.M5077.M5085.CertifiedRemovableGlobalExtension = (
        M5215.M5212.AdaptiveRemovableGlobalExtension
    )
    M5215.M5212.M5077.install_history_invariant_breakpoints(
        M5215.M5212.M5077.M5036.N5030
    )
    manager = M5215.M5212.M5077.CentralTopologyManager(
        run_directory,
        config,
    )
    return config, manager


def extract_catalog() -> dict[str, Any]:
    config, manager = install_parent_runtime()
    event = manager.events[EVENT_ID]
    argument = manager.arguments[ARGUMENT_ID]
    topology = read_json(SOURCE_TOPOLOGY)
    target = M5215.M5212.M5077.M5036.complex_from_row(
        argument["target_cosine"]
    )
    module = M5215.M5212.M5077.M5036.N5030
    previous_event = M5215.M5212.M5077.CURRENT_EVENT
    previous_argument = M5215.M5212.M5077.CURRENT_ARGUMENT
    previous_catalog = module.chamber_residue_catalog
    previous_global_value = module.global_chamber_value
    previous_job = M5215.M5212.M5077.M5036.MREPAIR.CURRENT_JOB
    captures: list[dict[str, Any]] = []

    def capture(
        ownership: dict[str, bool],
        start: complex,
        end: complex,
        required_roots: list[complex],
        global_nodes: int,
        global_residue_nodes: int,
        relative_residue_nodes: int,
        model_distance: float,
    ) -> tuple[list[dict[str, Any]], bool]:
        rows, stable = M5215.M5212.certified_5212_catalog(
            ownership,
            start,
            end,
            required_roots,
            global_nodes,
            global_residue_nodes,
            relative_residue_nodes,
            model_distance,
        )
        ownerships = module.physical_chambers()[1]
        matches = [
            index
            for index, candidate in enumerate(ownerships)
            if candidate == ownership
        ]
        if len(matches) != 1:
            raise RuntimeError(
                f"ownership matched {len(matches)} physical chambers"
            )
        captures.append(
            {
                "chamber_index": matches[0],
                "ownership": ownership,
                "required_roots": [str(root) for root in required_roots],
                "stable": bool(stable),
                "rows": json_ready(rows),
            }
        )
        return rows, stable

    started = time.monotonic()
    try:
        M5215.M5212.M5077.CURRENT_EVENT = event
        M5215.M5212.M5077.CURRENT_ARGUMENT = argument
        M5215.M5212.M5077.M5036.M5035.M5034.configure(
            event,
            target,
        )
        module.chamber_residue_catalog = capture
        M5215.M5212.M5077.M5036.MREPAIR.CURRENT_JOB = JOB_KEY
        M5215.M5212.M5077.M5036.MREPAIR.RADIUS_AUDIT.clear()
        M5215.M5212.M5077.LOCAL_RESIDUE_RESOLUTION_AUDIT.clear()
        M5215.M5212.M5077.OUTWARD_CONTOUR_AUDIT.clear()
        M5215.M5212.M5077.PROJECTIVE_CLUSTER_ZERO_AUDIT.clear()
        M5215.M5212.SOURCE_SEPARATED_CLUSTER_ZERO_AUDIT.clear()
        M5215.M5212.M5077.removable_extension_gate()
        extension = M5215.M5212.AdaptiveRemovableGlobalExtension(
            previous_global_value
        )
        module.global_chamber_value = extension
        decomposition = M5215.M5214.decompose_topological_value(
            module,
            topology,
            config["tiers"]["primary24"],
        )
    finally:
        module.chamber_residue_catalog = previous_catalog
        module.global_chamber_value = previous_global_value
        M5215.M5212.M5077.M5036.MREPAIR.CURRENT_JOB = previous_job
        M5215.M5212.M5077.CURRENT_EVENT = previous_event
        M5215.M5212.M5077.CURRENT_ARGUMENT = previous_argument
    if len(captures) != 1:
        raise RuntimeError(f"expected one catalog capture, got {len(captures)}")
    capture_row = captures[0]
    unstable = [
        row for row in capture_row["rows"] if not bool(row["stable"])
    ]
    extraction = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "job_key": JOB_KEY,
        "event": event,
        "argument": argument,
        "source_job": str(SOURCE_JOB),
        "source_job_sha256": digest(SOURCE_JOB),
        "source_topology": str(SOURCE_TOPOLOGY),
        "source_topology_sha256": digest(SOURCE_TOPOLOGY),
        "catalog_runtime_seconds": time.monotonic() - started,
        "decomposition": {
            "residues_stable": bool(decomposition[1]),
            "catalog_row_count": int(decomposition[2]),
            "safe_pair_count": int(decomposition[3]),
            "unsafe_pair_count": int(decomposition[4]),
        },
        "capture": capture_row,
        "unstable_row_count": len(unstable),
        "unstable_rows": unstable,
        "valid_for_numeric_UV_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(EXTRACTION, extraction)
    return extraction


def row_signature(
    chamber_index: int,
    row: dict[str, Any],
) -> dict[str, Any]:
    root = complex(row["root"])
    return {
        "chamber_index": int(chamber_index),
        "root": {
            "real": format(root.real, ".17g"),
            "imaginary": format(root.imag, ".17g"),
        },
        "pairs": canonical_pairs(row["pairs"]),
        "safe_scale": float(
            float(row["outer_radius"])
            / float(row["residue_contour_fraction"])
        ),
    }


def lock_contract(extraction: dict[str, Any]) -> dict[str, Any]:
    protocol = read_json(PROTOCOL_LOCK_5215)
    transport = read_json(TRANSPORT_LOCK_5215)
    if protocol["contract"]["runner_sha256"] != digest(SCRIPT_5215):
        raise RuntimeError("locked checkpoint-5215 runner changed")
    if (
        transport["contract"]["repair_runner_sha256"]
        != digest(SCRIPT_5215_TRANSPORT)
    ):
        raise RuntimeError("locked transport-repair runner changed")
    capture = extraction["capture"]
    signatures = [
        row_signature(capture["chamber_index"], row)
        for row in extraction["unstable_rows"]
    ]
    return {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "runner_sha256": digest(Path(__file__).resolve()),
        "script_5112_sha256": digest(SCRIPT_5112),
        "script_5215_sha256": digest(SCRIPT_5215),
        "script_5215_transport_sha256": digest(
            SCRIPT_5215_TRANSPORT
        ),
        "protocol_lock_5215_sha256": digest(PROTOCOL_LOCK_5215),
        "transport_lock_5215_sha256": digest(TRANSPORT_LOCK_5215),
        "source_job_sha256": digest(SOURCE_JOB),
        "source_topology_sha256": digest(SOURCE_TOPOLOGY),
        "target_signatures": signatures,
        "linearity_rule": (
            "for a grouped collision row, evaluate each exactly-one-owned "
            "direct pair independently and sum the resulting iterated "
            "residues at each common contour point"
        ),
        "levels": [
            {
                **level,
                "relative_fractions": list(level["relative_fractions"]),
                "global_fractions": list(level["global_fractions"]),
            }
            for level in LEVELS
        ],
        "classification": {
            "zero_tolerance": ZERO_TOLERANCE,
            "minimum_nonzero_magnitude": MINIMUM_NONZERO_MAGNITUDE,
            "maximum_relative_spread": MAXIMUM_RELATIVE_SPREAD,
            "maximum_cross_level_relative_change": (
                MAXIMUM_CROSS_LEVEL_RELATIVE_CHANGE
            ),
            "unresolved_action": "fail_closed",
        },
        "development_event_outcome_exposed": True,
        "current_5215_scale_decision_allowed": False,
        "new_fresh_predeclared_run_required_for_scale_decision": True,
        "statistical_thresholds_changed": False,
        "integrand_changed": False,
        "contour_definition_changed": False,
        "valid_for_numeric_UV_claim": False,
    }


def create_or_verify_lock(extraction: dict[str, Any]) -> dict[str, Any]:
    contract = lock_contract(extraction)
    if LOCK.exists():
        locked = read_json(LOCK)
        if locked["contract"] != contract:
            raise RuntimeError("checkpoint-5216 precision contract changed")
        return locked
    locked = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "contract": contract,
        "high_precision_outcomes_present_at_lock": False,
        "development_event_outcome_exposed": True,
        "statistical_protocol_reopened": False,
        "valid_for_numeric_UV_claim": False,
    }
    atomic_json(LOCK, locked)
    return locked


def one_owned_direct_label(
    pair: list[str],
    ownership: dict[str, bool],
) -> str:
    labels = [
        label
        for label in pair
        if bool(ownership.get(label, False))
        and label.startswith(("direct:g1:", "direct:g2:"))
    ]
    if len(labels) != 1:
        raise RuntimeError(
            f"pair has {len(labels)} owned direct g1/g2 labels: {pair}"
        )
    if not all(label.startswith("direct:") for label in pair):
        raise RuntimeError(f"pair is not direct-only: {pair}")
    return labels[0]


def item_path(
    record_index: int,
    pair_index: int,
    level_id: str,
) -> Path:
    return ITEMS / (
        f"record_{record_index:02d}__pair_{pair_index:02d}"
        f"__{level_id}.json"
    )


def evaluate_item(
    record_index: int,
    pair_index: int,
    signature: dict[str, Any],
    pair: list[str],
    ownership: dict[str, bool],
    event: dict[str, Any],
    argument: dict[str, Any],
    level: dict[str, Any],
    lock_digest: str,
) -> dict[str, Any]:
    output = item_path(record_index, pair_index, level["level_id"])
    item_contract = {
        "record_index": record_index,
        "pair_index": pair_index,
        "signature": signature,
        "pair": pair,
        "owned_label": one_owned_direct_label(pair, ownership),
        "level": {
            **level,
            "relative_fractions": list(level["relative_fractions"]),
            "global_fractions": list(level["global_fractions"]),
        },
        "lock_sha256": lock_digest,
    }
    item_digest = canonical_digest(item_contract)
    if output.exists():
        cached = read_json(output)
        if (
            cached.get("status") == "COMPLETE"
            and cached.get("item_digest") == item_digest
        ):
            return cached
    record = {
        "event": event,
        "argument": argument,
        "chamber_index": signature["chamber_index"],
        "root": signature["root"],
        "pairs": [pair],
        "safe_scale": signature["safe_scale"],
    }
    configured = M5112.configure(record)
    root = row_complex(signature["root"])
    values: list[dict[str, Any]] = []
    previous_dps = mp.mp.dps
    started = time.monotonic()
    try:
        mp.mp.dps = int(level["dps"])
        for relative_fraction in level["relative_fractions"]:
            for global_fraction in level["global_fractions"]:
                value = M5112.direct_relative_residue(
                    root,
                    float(signature["safe_scale"]),
                    [tuple(pair)],
                    configured,
                    int(level["relative_nodes"]),
                    int(level["global_nodes"]),
                    float(relative_fraction),
                    float(global_fraction),
                )
                values.append(
                    {
                        "relative_fraction": float(relative_fraction),
                        "global_fraction": float(global_fraction),
                        "value": complex_row(value),
                        "magnitude": float(abs(value)),
                    }
                )
    finally:
        mp.mp.dps = previous_dps
    complex_values = [row_complex(row["value"]) for row in values]
    mean = sum(complex_values) / len(complex_values)
    spread = max(abs(value - mean) for value in complex_values)
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "status": "COMPLETE",
        "item_digest": item_digest,
        "item_contract": item_contract,
        "values": values,
        "mean": complex_row(mean),
        "maximum_spread": float(spread),
        "relative_spread": float(
            spread / max(abs(mean), 1.0e-300)
        ),
        "minimum_magnitude": float(
            min(abs(value) for value in complex_values)
        ),
        "maximum_magnitude": float(
            max(abs(value) for value in complex_values)
        ),
        "runtime_seconds": time.monotonic() - started,
        "valid_for_numeric_UV_claim": False,
    }
    atomic_json(output, result)
    print(
        json.dumps(
            {
                "record_index": record_index,
                "pair_index": pair_index,
                "level_id": level["level_id"],
                "mean": result["mean"],
                "relative_spread": result["relative_spread"],
                "runtime_seconds": result["runtime_seconds"],
            }
        ),
        flush=True,
    )
    return result


def classify_levels(level_rows: list[dict[str, Any]]) -> dict[str, Any]:
    means = [row_complex(row["mean"]) for row in level_rows]
    maximum_magnitude = max(
        float(row["maximum_magnitude"]) for row in level_rows
    )
    minimum_magnitude = min(
        float(row["minimum_magnitude"]) for row in level_rows
    )
    maximum_relative_spread = max(
        float(row["relative_spread"]) for row in level_rows
    )
    cross_level_change = abs(means[-1] - means[0]) / max(
        abs(means[-1]),
        abs(means[0]),
        1.0e-300,
    )
    if maximum_magnitude < ZERO_TOLERANCE:
        classification = "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO"
    elif (
        minimum_magnitude > MINIMUM_NONZERO_MAGNITUDE
        and maximum_relative_spread < MAXIMUM_RELATIVE_SPREAD
        and cross_level_change
        < MAXIMUM_CROSS_LEVEL_RELATIVE_CHANGE
    ):
        classification = "STABLE_DIRECT_COMPONENT_NONZERO"
    else:
        classification = "UNRESOLVED"
    return {
        "classification": classification,
        "selected_value": level_rows[-1]["mean"],
        "maximum_magnitude": maximum_magnitude,
        "minimum_magnitude": minimum_magnitude,
        "maximum_relative_spread": maximum_relative_spread,
        "cross_level_relative_change": float(cross_level_change),
    }


def grouped_level(
    level: dict[str, Any],
    pair_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    keyed: list[dict[tuple[float, float], complex]] = []
    for pair_row in pair_rows:
        keyed.append(
            {
                (
                    float(value["relative_fraction"]),
                    float(value["global_fraction"]),
                ): row_complex(value["value"])
                for value in pair_row["values"]
            }
        )
    keys = set(keyed[0])
    if any(set(values) != keys for values in keyed[1:]):
        raise RuntimeError("grouped pair grids differ")
    values: list[dict[str, Any]] = []
    for relative_fraction, global_fraction in sorted(keys):
        total = sum(
            (pair_values[(relative_fraction, global_fraction)]
             for pair_values in keyed),
            0.0j,
        )
        values.append(
            {
                "relative_fraction": relative_fraction,
                "global_fraction": global_fraction,
                "value": complex_row(total),
                "magnitude": abs(total),
            }
        )
    complex_values = [row_complex(row["value"]) for row in values]
    mean = sum(complex_values) / len(complex_values)
    spread = max(abs(value - mean) for value in complex_values)
    return {
        "level_id": level["level_id"],
        "values": values,
        "mean": complex_row(mean),
        "maximum_spread": float(spread),
        "relative_spread": float(
            spread / max(abs(mean), 1.0e-300)
        ),
        "minimum_magnitude": float(
            min(abs(value) for value in complex_values)
        ),
        "maximum_magnitude": float(
            max(abs(value) for value in complex_values)
        ),
    }


def write_audit_csv(records: list[dict[str, Any]]) -> None:
    AUDIT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            (
                "record_index",
                "root_real",
                "root_imaginary",
                "pair_count",
                "classification",
                "selected_real",
                "selected_imaginary",
                "maximum_relative_spread",
                "cross_level_relative_change",
                "valid_for_numeric_UV_claim",
            )
        )
        for record in records:
            signature = record["signature"]
            resolution = record["grouped_resolution"]
            writer.writerow(
                (
                    record["record_index"],
                    signature["root"]["real"],
                    signature["root"]["imaginary"],
                    len(signature["pairs"]),
                    resolution["classification"],
                    resolution["selected_value"]["real"],
                    resolution["selected_value"]["imaginary"],
                    resolution["maximum_relative_spread"],
                    resolution["cross_level_relative_change"],
                    "false",
                )
            )


def finalize(
    extraction: dict[str, Any],
    locked: dict[str, Any],
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    unresolved = [
        record
        for record in records
        if record["grouped_resolution"]["classification"] == "UNRESOLVED"
        or any(
            pair["resolution"]["classification"] == "UNRESOLVED"
            for pair in record["pair_resolutions"]
        )
    ]
    replacements = []
    for record in records:
        resolution = record["grouped_resolution"]
        if resolution["classification"] == "UNRESOLVED":
            continue
        selected = (
            {"real": "0.0", "imaginary": "0.0"}
            if resolution["classification"]
            == "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO"
            else resolution["selected_value"]
        )
        replacements.append(
            {
                "job_key": JOB_KEY,
                "event_id": EVENT_ID,
                "argument_id": ARGUMENT_ID,
                "signature": record["signature"],
                "replacement_residue": selected,
                "classification": resolution["classification"],
                "stable": True,
                "numerically_zero": (
                    resolution["classification"]
                    == "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO"
                ),
                "scope": (
                    "exact job, event, argument, chamber, grouped pairs "
                    "and collision root only"
                ),
                "current_5215_scale_decision_allowed": False,
                "valid_for_numeric_UV_claim": False,
            }
        )
    formal_digest = tree_digest(FORMAL)
    validations = [
        (
            "formalization_workbench_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "source_job_remains_unconverged",
            read_json(SOURCE_JOB)["status"] == "COMPLETED_UNCONVERGED",
            read_json(SOURCE_JOB)["status"],
        ),
        (
            "three_unstable_catalog_rows_extracted",
            extraction["unstable_row_count"] == 3,
            str(extraction["unstable_row_count"]),
        ),
        (
            "all_exact_pairs_have_one_owned_direct_label",
            all(
                pair["owned_label"].startswith(("direct:g1:", "direct:g2:"))
                for record in records
                for pair in record["pair_resolutions"]
            ),
            "exactly one owned direct g1/g2 label per pair",
        ),
        (
            "all_precision_items_complete",
            all(
                item["status"] == "COMPLETE"
                for record in records
                for pair in record["pair_resolutions"]
                for item in pair["levels"]
            ),
            str(
                sum(
                    len(pair["levels"])
                    for record in records
                    for pair in record["pair_resolutions"]
                )
            ),
        ),
        (
            "all_grouped_rows_resolved",
            not unresolved,
            str(len(unresolved)),
        ),
        (
            "current_exposed_pilot_not_used_for_scale_decision",
            all(
                not row["current_5215_scale_decision_allowed"]
                for row in replacements
            ),
            "new predeclared fresh run required",
        ),
        (
            "claim_flags_remain_false",
            all(not row["valid_for_numeric_UV_claim"] for row in replacements),
            "numeric UV, local GR and full MTS remain false",
        ),
    ]
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("check", "passed", "detail"))
        for name, passed, detail in validations:
            writer.writerow((name, str(bool(passed)).lower(), detail))
    audit = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "lock": str(LOCK),
        "lock_sha256": digest(LOCK),
        "extraction": str(EXTRACTION),
        "extraction_sha256": digest(EXTRACTION),
        "records": records,
        "unresolved_record_count": len(unresolved),
        "replacement_count": len(replacements),
        "development_event_outcome_exposed": True,
        "current_5215_scale_decision_allowed": False,
        "new_fresh_predeclared_run_required_for_scale_decision": True,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(AUDIT, audit)
    write_audit_csv(records)
    atomic_json(
        REPLACEMENTS,
        {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "rows": replacements,
            "unresolved_action": "fail_closed",
            "runner_integration_authorized": not unresolved,
            "current_5215_scale_decision_allowed": False,
            "new_fresh_predeclared_run_required_for_scale_decision": True,
            "valid_for_numeric_UV_claim": False,
        },
    )
    passed = all(row[1] for row in validations)
    result = {
        "checkpoint": 5216,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "state": "COMPLETE" if passed else "BLOCKED",
        "precision_lock_sha256": digest(LOCK),
        "audit_sha256": digest(AUDIT),
        "replacement_registry_sha256": digest(REPLACEMENTS),
        "resolved_record_count": len(records) - len(unresolved),
        "unresolved_record_count": len(unresolved),
        "runner_integration_authorized": bool(passed and not unresolved),
        "current_5215_scale_decision_allowed": False,
        "new_fresh_predeclared_run_required_for_scale_decision": True,
        "formalization_workbench_tree_sha256": formal_digest,
        "validation_all_passed": passed,
        "validation_check_count": len(validations),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT, result)
    lines = [
        "# 5216 - Grouped owned-direct residue resolution",
        "",
        "## Problem",
        "",
        "The transport-repaired `S521509/E040/A00` topology exposed three",
        "unstable direct-only catalog rows. Two rows contain two collision",
        "pairs at one relative root; the old on-demand classifier only",
        "accepted one pair.",
        "",
        "## Derived rule",
        "",
        "Linearity of the iterated contour integral permits each collision",
        "pair with exactly one chamber-owned direct pole to be evaluated",
        "separately. Their residues are then summed point-by-point on the",
        "same relative/global contour grid. No pole is deleted and no",
        "double-precision tolerance is widened.",
        "",
        "## Result",
        "",
        f"- Resolved grouped rows: `{len(records) - len(unresolved)}/"
        f"{len(records)}`.",
        f"- Event-local replacement rows: `{len(replacements)}`.",
        f"- Validation: `{sum(1 for row in validations if row[1])}/"
        f"{len(validations)}`.",
        "- Current checkpoint-5215 scale decision: `not allowed`.",
        "- A new fresh run with this classifier predeclared is required.",
        "",
        "## Claim boundary",
        "",
        "This is an event-local numerical resolution on an outcome-exposed",
        "development event. It does not determine the MTS two-loop",
        "coefficient and does not alter the exact checkpoint-5211",
        "GR+Lambda+SM+Maxwell truncation.",
        "",
        "## Evidence",
        "",
        f"- Precision lock: `{LOCK}`",
        f"- Extraction: `{EXTRACTION}`",
        f"- Audit: `{AUDIT}`",
        f"- Replacement registry: `{REPLACEMENTS}`",
        f"- Validation: `{VALIDATION}`",
    ]
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def execute() -> dict[str, Any]:
    extraction = extract_catalog()
    locked = create_or_verify_lock(extraction)
    lock_digest = digest(LOCK)
    capture = extraction["capture"]
    ownership = capture["ownership"]
    event = extraction["event"]
    argument = extraction["argument"]
    signatures = locked["contract"]["target_signatures"]
    records: list[dict[str, Any]] = []
    for record_index, signature in enumerate(signatures):
        pair_resolutions = []
        level_groups: dict[str, list[dict[str, Any]]] = {
            level["level_id"]: [] for level in LEVELS
        }
        for pair_index, pair in enumerate(signature["pairs"]):
            levels = [
                evaluate_item(
                    record_index,
                    pair_index,
                    signature,
                    pair,
                    ownership,
                    event,
                    argument,
                    level,
                    lock_digest,
                )
                for level in LEVELS
            ]
            for item in levels:
                level_groups[
                    item["item_contract"]["level"]["level_id"]
                ].append(item)
            pair_resolutions.append(
                {
                    "pair_index": pair_index,
                    "pair": pair,
                    "owned_label": one_owned_direct_label(
                        pair,
                        ownership,
                    ),
                    "levels": levels,
                    "resolution": classify_levels(levels),
                }
            )
        grouped_levels = [
            grouped_level(
                level,
                level_groups[level["level_id"]],
            )
            for level in LEVELS
        ]
        records.append(
            {
                "record_index": record_index,
                "signature": signature,
                "pair_resolutions": pair_resolutions,
                "grouped_levels": grouped_levels,
                "grouped_resolution": classify_levels(grouped_levels),
            }
        )
    return finalize(extraction, locked, records)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("lock", "run"),
        default="lock",
    )
    arguments = parser.parse_args()
    extraction = extract_catalog()
    locked = create_or_verify_lock(extraction)
    if arguments.mode == "lock":
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "state": "LOCKED_AWAITING_HIGH_PRECISION",
                    "lock": str(LOCK),
                    "lock_sha256": digest(LOCK),
                    "target_count": len(
                        locked["contract"]["target_signatures"]
                    ),
                    "development_event_outcome_exposed": True,
                    "valid_for_numeric_UV_claim": False,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    execute()


if __name__ == "__main__":
    main()
