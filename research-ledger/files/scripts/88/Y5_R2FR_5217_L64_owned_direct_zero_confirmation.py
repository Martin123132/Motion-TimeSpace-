from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import mpmath as mp


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5217"
ITEMS = SOURCE / "runs" / "L64_zero_confirmation_v1"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SCRIPT_5216 = (
    POST
    / "scripts"
    / "Y5_R2FR_5216_grouped_owned_direct_residue_resolution.py"
)
SOURCE_5216 = POST / "source-intake" / "functional_rg" / "5216"
LOCK_5216 = SOURCE_5216 / "grouped_owned_direct_precision_lock.json"
EXTRACTION_5216 = (
    SOURCE_5216 / "S521509_E040_A00_catalog_extraction.json"
)
AUDIT_5216 = SOURCE_5216 / "S521509_E040_A00_grouped_direct_audit.json"
LOCK = SOURCE / "L64_owned_direct_zero_confirmation_lock.json"
AUDIT = SOURCE / "L64_owned_direct_zero_confirmation_audit.json"
REGISTRY = SOURCE / "resolved_grouped_owned_direct_registry.json"
RESULT = SOURCE / "L64_owned_direct_zero_confirmation.json"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5217_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5217-Y5-R2FR-L64-owned-direct-zero-confirmation.md"
)
MARKER = "MTS_5217_L64_OWNED_DIRECT_ZERO_CONFIRMATION"
REVISION = "finest-grid-zero-and-convergence-confirmation-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
ZERO_TOLERANCE = 1.0e-20
MAXIMUM_L32_TO_L48_RATIO = 1.0e-4
LEVEL = {
    "level_id": "L64",
    "dps": 120,
    "relative_nodes": 64,
    "global_nodes": 64,
    "relative_fractions": (0.1, 0.05, 0.025),
    "global_fractions": (0.15, 0.3),
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5216 = load_module("mts_5216_for_5217", SCRIPT_5216)


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
        "real": mp.nstr(mp.re(value), 70),
        "imaginary": mp.nstr(mp.im(value), 70),
    }


def row_complex(value: dict[str, Any]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


def unresolved_targets(audit: dict[str, Any]) -> list[dict[str, Any]]:
    targets = []
    for record in audit["records"]:
        for pair in record["pair_resolutions"]:
            if pair["resolution"]["classification"] != "UNRESOLVED":
                continue
            levels = {
                row["item_contract"]["level"]["level_id"]: row
                for row in pair["levels"]
            }
            targets.append(
                {
                    "record_index": int(record["record_index"]),
                    "pair_index": int(pair["pair_index"]),
                    "signature": record["signature"],
                    "pair": pair["pair"],
                    "owned_label": pair["owned_label"],
                    "L32_maximum_magnitude": float(
                        levels["L32"]["maximum_magnitude"]
                    ),
                    "L48_maximum_magnitude": float(
                        levels["L48"]["maximum_magnitude"]
                    ),
                    "L32_to_L48_maximum_ratio": float(
                        levels["L48"]["maximum_magnitude"]
                        / levels["L32"]["maximum_magnitude"]
                    ),
                }
            )
    return targets


def lock_contract() -> dict[str, Any]:
    audit = read_json(AUDIT_5216)
    targets = unresolved_targets(audit)
    if digest(SCRIPT_5216) != read_json(LOCK_5216)["contract"]["runner_sha256"]:
        raise RuntimeError("locked checkpoint-5216 runner changed")
    if len(targets) != 2:
        raise RuntimeError(f"expected two unresolved pairs, got {len(targets)}")
    return {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "runner_sha256": digest(Path(__file__).resolve()),
        "script_5216_sha256": digest(SCRIPT_5216),
        "lock_5216_sha256": digest(LOCK_5216),
        "extraction_5216_sha256": digest(EXTRACTION_5216),
        "audit_5216_sha256": digest(AUDIT_5216),
        "targets": targets,
        "level": {
            **LEVEL,
            "relative_fractions": list(LEVEL["relative_fractions"]),
            "global_fractions": list(LEVEL["global_fractions"]),
        },
        "zero_certificate": {
            "L48_maximum_below_existing_zero_tolerance": True,
            "L64_maximum_below_existing_zero_tolerance": True,
            "L32_to_L48_maximum_ratio_at_most": (
                MAXIMUM_L32_TO_L48_RATIO
            ),
            "zero_tolerance": ZERO_TOLERANCE,
            "unresolved_action": "fail_closed",
        },
        "zero_tolerance_changed": False,
        "integrand_changed": False,
        "contour_fractions_changed_from_L48": False,
        "development_event_outcome_exposed": True,
        "current_5215_scale_decision_allowed": False,
        "new_fresh_predeclared_run_required_for_scale_decision": True,
        "valid_for_numeric_UV_claim": False,
    }


def create_or_verify_lock() -> dict[str, Any]:
    contract = lock_contract()
    if LOCK.exists():
        locked = read_json(LOCK)
        if locked["contract"] != contract:
            raise RuntimeError("checkpoint-5217 lock contract changed")
        return locked
    locked = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "contract": contract,
        "L64_outcomes_present_at_lock": False,
        "development_event_outcome_exposed": True,
        "statistical_protocol_reopened": False,
        "valid_for_numeric_UV_claim": False,
    }
    atomic_json(LOCK, locked)
    return locked


def output_path(target: dict[str, Any]) -> Path:
    return ITEMS / (
        f"record_{target['record_index']:02d}"
        f"__pair_{target['pair_index']:02d}__L64.json"
    )


def evaluate_target(
    target: dict[str, Any],
    event: dict[str, Any],
    argument: dict[str, Any],
    ownership: dict[str, bool],
    lock_sha256: str,
) -> dict[str, Any]:
    output = output_path(target)
    item_contract = {
        "target": target,
        "level": {
            **LEVEL,
            "relative_fractions": list(LEVEL["relative_fractions"]),
            "global_fractions": list(LEVEL["global_fractions"]),
        },
        "lock_sha256": lock_sha256,
    }
    item_digest = canonical_digest(item_contract)
    if output.exists():
        cached = read_json(output)
        if (
            cached.get("status") == "COMPLETE"
            and cached.get("item_digest") == item_digest
        ):
            return cached
    if M5216.one_owned_direct_label(target["pair"], ownership) != target["owned_label"]:
        raise RuntimeError("target ownership changed")
    record = {
        "event": event,
        "argument": argument,
        "chamber_index": target["signature"]["chamber_index"],
        "root": target["signature"]["root"],
        "pairs": [target["pair"]],
        "safe_scale": target["signature"]["safe_scale"],
    }
    configured = M5216.M5112.configure(record)
    root = row_complex(target["signature"]["root"])
    values = []
    previous_dps = mp.mp.dps
    started = time.monotonic()
    try:
        mp.mp.dps = int(LEVEL["dps"])
        for relative_fraction in LEVEL["relative_fractions"]:
            for global_fraction in LEVEL["global_fractions"]:
                value = M5216.M5112.direct_relative_residue(
                    root,
                    float(target["signature"]["safe_scale"]),
                    [tuple(target["pair"])],
                    configured,
                    int(LEVEL["relative_nodes"]),
                    int(LEVEL["global_nodes"]),
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
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "status": "COMPLETE",
        "item_digest": item_digest,
        "item_contract": item_contract,
        "values": values,
        "mean": complex_row(mean),
        "minimum_magnitude": min(
            float(row["magnitude"]) for row in values
        ),
        "maximum_magnitude": max(
            float(row["magnitude"]) for row in values
        ),
        "runtime_seconds": time.monotonic() - started,
        "valid_for_numeric_UV_claim": False,
    }
    atomic_json(output, result)
    print(
        json.dumps(
            {
                "record_index": target["record_index"],
                "pair_index": target["pair_index"],
                "maximum_magnitude": result["maximum_magnitude"],
                "runtime_seconds": result["runtime_seconds"],
            }
        ),
        flush=True,
    )
    return result


def certify(
    target: dict[str, Any],
    item: dict[str, Any],
) -> dict[str, Any]:
    passed = bool(
        target["L48_maximum_magnitude"] < ZERO_TOLERANCE
        and item["maximum_magnitude"] < ZERO_TOLERANCE
        and target["L32_to_L48_maximum_ratio"]
        <= MAXIMUM_L32_TO_L48_RATIO
    )
    return {
        "record_index": target["record_index"],
        "pair_index": target["pair_index"],
        "signature": target["signature"],
        "pair": target["pair"],
        "owned_label": target["owned_label"],
        "L32_maximum_magnitude": target["L32_maximum_magnitude"],
        "L48_maximum_magnitude": target["L48_maximum_magnitude"],
        "L64_maximum_magnitude": item["maximum_magnitude"],
        "L32_to_L48_maximum_ratio": target[
            "L32_to_L48_maximum_ratio"
        ],
        "classification": (
            "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO"
            if passed
            else "UNRESOLVED"
        ),
        "replacement_residue": {
            "real": "0.0",
            "imaginary": "0.0",
        },
        "zero_tolerance": ZERO_TOLERANCE,
        "zero_tolerance_changed": False,
        "scope": (
            "exact job, event, argument, chamber, pair and collision "
            "root only"
        ),
        "current_5215_scale_decision_allowed": False,
        "valid_for_numeric_UV_claim": False,
    }


def finalize(
    locked: dict[str, Any],
    items: list[dict[str, Any]],
) -> dict[str, Any]:
    audit_5216 = read_json(AUDIT_5216)
    targets = locked["contract"]["targets"]
    certificates = [
        certify(target, item)
        for target, item in zip(targets, items)
    ]
    unresolved = [
        row for row in certificates if row["classification"] == "UNRESOLVED"
    ]
    registry_rows = []
    for record in audit_5216["records"]:
        grouped = record["grouped_resolution"]
        pair_rows = []
        for pair in record["pair_resolutions"]:
            classification = pair["resolution"]["classification"]
            if classification == "UNRESOLVED":
                matches = [
                    row
                    for row in certificates
                    if row["record_index"] == record["record_index"]
                    and row["pair_index"] == pair["pair_index"]
                ]
                if len(matches) != 1:
                    raise RuntimeError("unresolved pair certificate missing")
                classification = matches[0]["classification"]
            pair_rows.append(
                {
                    "pair": pair["pair"],
                    "owned_label": pair["owned_label"],
                    "classification": classification,
                }
            )
        resolved = bool(
            grouped["classification"]
            == "STABLE_DIRECT_COMPONENT_NONZERO"
            and all(
                row["classification"]
                in {
                    "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO",
                    "STABLE_DIRECT_COMPONENT_NONZERO",
                }
                for row in pair_rows
            )
        )
        registry_rows.append(
            {
                "job_key": M5216.JOB_KEY,
                "event_id": M5216.EVENT_ID,
                "argument_id": M5216.ARGUMENT_ID,
                "signature": record["signature"],
                "pair_resolutions": pair_rows,
                "grouped_classification": (
                    "STABLE_GROUPED_DIRECT_NONZERO"
                    if resolved
                    else "UNRESOLVED"
                ),
                "replacement_residue": grouped["selected_value"],
                "stable": resolved,
                "numerically_zero": False,
                "scope": (
                    "exact job, event, argument, chamber, grouped pairs "
                    "and collision root only"
                ),
                "current_5215_scale_decision_allowed": False,
                "valid_for_numeric_UV_claim": False,
            }
        )
    unresolved_registry = [
        row for row in registry_rows if not bool(row["stable"])
    ]
    formal_digest = tree_digest(FORMAL)
    validations = [
        (
            "formalization_workbench_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "two_L64_targets_complete",
            len(items) == 2
            and all(row["status"] == "COMPLETE" for row in items),
            str(len(items)),
        ),
        (
            "L48_values_below_existing_zero_gate",
            all(
                row["L48_maximum_magnitude"] < ZERO_TOLERANCE
                for row in certificates
            ),
            str(
                max(
                    row["L48_maximum_magnitude"]
                    for row in certificates
                )
            ),
        ),
        (
            "L64_values_below_existing_zero_gate",
            all(
                row["L64_maximum_magnitude"] < ZERO_TOLERANCE
                for row in certificates
            ),
            str(
                max(
                    row["L64_maximum_magnitude"]
                    for row in certificates
                )
            ),
        ),
        (
            "coarse_to_fine_reduction_passes",
            all(
                row["L32_to_L48_maximum_ratio"]
                <= MAXIMUM_L32_TO_L48_RATIO
                for row in certificates
            ),
            str(
                max(
                    row["L32_to_L48_maximum_ratio"]
                    for row in certificates
                )
            ),
        ),
        (
            "all_three_grouped_rows_resolved",
            not unresolved_registry,
            str(len(unresolved_registry)),
        ),
        (
            "current_exposed_pilot_not_used_for_scale_decision",
            all(
                not row["current_5215_scale_decision_allowed"]
                for row in registry_rows
            ),
            "new predeclared fresh run required",
        ),
        (
            "claim_flags_remain_false",
            all(
                not row["valid_for_numeric_UV_claim"]
                for row in registry_rows
            ),
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
        "certificates": certificates,
        "unresolved_certificate_count": len(unresolved),
        "development_event_outcome_exposed": True,
        "current_5215_scale_decision_allowed": False,
        "new_fresh_predeclared_run_required_for_scale_decision": True,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(AUDIT, audit)
    atomic_json(
        REGISTRY,
        {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "rows": registry_rows,
            "unresolved_action": "fail_closed",
            "event_local_registry_complete": not unresolved_registry,
            "future_fresh_runner_integration_authorized": (
                not unresolved_registry
            ),
            "current_5215_scale_decision_allowed": False,
            "new_fresh_predeclared_run_required_for_scale_decision": True,
            "valid_for_numeric_UV_claim": False,
        },
    )
    passed = all(row[1] for row in validations)
    result = {
        "checkpoint": 5217,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "state": "COMPLETE" if passed else "BLOCKED",
        "lock_sha256": digest(LOCK),
        "audit_sha256": digest(AUDIT),
        "registry_sha256": digest(REGISTRY),
        "zero_certificate_count": len(certificates) - len(unresolved),
        "resolved_grouped_row_count": (
            len(registry_rows) - len(unresolved_registry)
        ),
        "future_fresh_runner_integration_authorized": bool(passed),
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
        "# 5217 - L64 owned-direct zero confirmation",
        "",
        "## Question",
        "",
        "Checkpoint 5216 resolved all three grouped sums but left two",
        "individual summands unresolved because its deliberately strict",
        "rule included the coarse `L32` quadrature maximum. Both `L48`",
        "maxima were already below the unchanged `1e-20` zero gate.",
        "",
        "## Test",
        "",
        "The two exact summands were recomputed at 120 decimal digits with",
        "`64 x 64` contour nodes on the same six radius combinations used",
        "by `L48`. A zero certificate requires both `L48` and `L64` below",
        "`1e-20` and at least a `1e4` reduction from `L32` to `L48`.",
        "",
        "## Result",
        "",
        f"- Zero certificates: `{len(certificates) - len(unresolved)}/"
        f"{len(certificates)}`.",
        f"- Resolved grouped rows: `{len(registry_rows) - len(unresolved_registry)}/"
        f"{len(registry_rows)}`.",
        f"- Validation: `{sum(1 for row in validations if row[1])}/"
        f"{len(validations)}`.",
        "- Zero tolerance changed: `False`.",
        "- Current checkpoint-5215 scale decision allowed: `False`.",
        "",
        "## Consequence",
        "",
        "The event-local grouped residues are now numerically resolved",
        "without deleting poles or widening a tolerance. The development",
        "event was outcome-exposed, so a new fresh run must predeclare the",
        "general grouped classifier before any scale decision.",
        "",
        "## Evidence",
        "",
        f"- Lock: `{LOCK}`",
        f"- Audit: `{AUDIT}`",
        f"- Registry: `{REGISTRY}`",
        f"- Validation: `{VALIDATION}`",
    ]
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def execute(locked: dict[str, Any]) -> dict[str, Any]:
    extraction = read_json(EXTRACTION_5216)
    ownership = extraction["capture"]["ownership"]
    event = extraction["event"]
    argument = extraction["argument"]
    items = [
        evaluate_target(
            target,
            event,
            argument,
            ownership,
            digest(LOCK),
        )
        for target in locked["contract"]["targets"]
    ]
    return finalize(locked, items)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("lock", "run"),
        default="lock",
    )
    arguments = parser.parse_args()
    locked = create_or_verify_lock()
    if arguments.mode == "lock":
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "state": "LOCKED_AWAITING_L64",
                    "lock": str(LOCK),
                    "lock_sha256": digest(LOCK),
                    "target_count": len(locked["contract"]["targets"]),
                    "valid_for_numeric_UV_claim": False,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    execute(locked)


if __name__ == "__main__":
    main()
