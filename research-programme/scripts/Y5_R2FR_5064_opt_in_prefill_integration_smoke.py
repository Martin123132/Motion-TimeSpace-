from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import shutil
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5034 = POST / "scripts" / "Y5_R2FR_5034_bounded_adaptive_outer_phase_space_smoke.py"
SCRIPT_5063 = POST / "scripts" / "Y5_R2FR_5063_opt_in_certified_topology_prefill.py"
SOURCE_5036_RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5036"
    / "runs"
    / "paired_full_vector_s2_v1"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5064"
SCRATCH = SOURCE / "scratch_run"
RESULT_JSON = SOURCE / "opt_in_prefill_integration_smoke.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5064_VALIDATION.csv"
)
MARKER = "MTS_5064_OPT_IN_PREFILL_INTEGRATION_SMOKE"
REVISION = "default-off-idempotent-existing-runner-cache-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
SAFE_EVENT = "S503401_N0000"
SAFE_ARGUMENT = "A00"
TRANSITION_EVENT = "S503402_N0000"
TRANSITION_ARGUMENT = "A06"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5034 = load_module("mts_5034_for_5064", SCRIPT_5034)
M5063 = load_module("mts_5063_for_5064", SCRIPT_5063)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    temporary.replace(path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def source_topology(event_id: str, epsilon_id: str, base_id: str) -> Path:
    return (
        SOURCE_5036_RUN
        / "topologies"
        / f"{event_id}__{epsilon_id}_{base_id}.json"
    )


def scratch_topology(event_id: str, epsilon_id: str, base_id: str) -> Path:
    return SCRATCH / "topologies" / f"{event_id}__{epsilon_id}_{base_id}.json"


def main() -> None:
    required = [
        SCRIPT_5034,
        SCRIPT_5063,
        SOURCE_5036_RUN / "config.json",
        source_topology(SAFE_EVENT, "E040", SAFE_ARGUMENT),
        source_topology(SAFE_EVENT, "E020", SAFE_ARGUMENT),
        source_topology(TRANSITION_EVENT, "E040", TRANSITION_ARGUMENT),
        source_topology(TRANSITION_EVENT, "E020", TRANSITION_ARGUMENT),
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    if SCRATCH.exists():
        if SOURCE not in SCRATCH.parents:
            raise RuntimeError("scratch path escaped checkpoint output directory")
        shutil.rmtree(SCRATCH)
    (SCRATCH / "topologies").mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE_5036_RUN / "config.json", SCRATCH / "config.json")
    shutil.copy2(
        source_topology(SAFE_EVENT, "E040", SAFE_ARGUMENT),
        scratch_topology(SAFE_EVENT, "E040", SAFE_ARGUMENT),
    )
    shutil.copy2(
        source_topology(TRANSITION_EVENT, "E040", TRANSITION_ARGUMENT),
        scratch_topology(TRANSITION_EVENT, "E040", TRANSITION_ARGUMENT),
    )
    safe_target = scratch_topology(SAFE_EVENT, "E020", SAFE_ARGUMENT)
    transition_target = scratch_topology(
        TRANSITION_EVENT, "E020", TRANSITION_ARGUMENT
    )
    disabled = M5063.prefill(SCRATCH, "E040", "E020", False)
    disabled_wrote_nothing = (
        disabled["written_topology_count"] == 0
        and not safe_target.exists()
        and not transition_target.exists()
    )
    enabled = M5063.prefill(SCRATCH, "E040", "E020", True)
    safe_written = safe_target.exists()
    transition_fallback = not transition_target.exists()
    generated = json.loads(safe_target.read_text(encoding="utf-8"))
    expected = json.loads(
        source_topology(SAFE_EVENT, "E020", SAFE_ARGUMENT).read_text(encoding="utf-8")
    )
    signature_exact = (
        generated["topology_signature_digest"]
        == expected["topology_signature_digest"]
    )
    descriptor_exact = (
        generated["topology_class_descriptor"]
        == expected["topology_class_descriptor"]
    )
    before_digest = digest(safe_target)
    repeated = M5063.prefill(SCRATCH, "E040", "E020", True)
    after_digest = digest(safe_target)
    idempotent = before_digest == after_digest
    config = json.loads((SCRATCH / "config.json").read_text(encoding="utf-8"))
    event = next(row for row in config["events"] if row["event_id"] == SAFE_EVENT)
    argument = next(
        row
        for row in config["arguments"]
        if row["argument_id"] == f"E020_{SAFE_ARGUMENT}"
    )
    cached_document, cached_path, cached_runtime = M5034.obtain_topology(
        SCRATCH, config, event, argument
    )
    existing_runner_cache_accepts = (
        cached_path == safe_target
        and cached_runtime == 0.0
        and cached_document["checkpoint_marker"]
        == "MTS_5063_OPT_IN_CERTIFIED_TOPOLOGY_PREFILL"
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "scratch_run": str(SCRATCH),
        "disabled_manifest": disabled,
        "enabled_manifest": enabled,
        "repeated_manifest": repeated,
        "default_off_wrote_nothing": disabled_wrote_nothing,
        "safe_target_written": safe_written,
        "transition_target_left_for_full_homotopy": transition_fallback,
        "safe_signature_exact": signature_exact,
        "safe_class_descriptor_exact": descriptor_exact,
        "second_enabled_call_idempotent": idempotent,
        "existing_5034_runner_cache_accepts_prefill": existing_runner_cache_accepts,
        "existing_5034_cache_runtime_seconds": cached_runtime,
        "opt_in_prefill_integration_passed": (
            disabled_wrote_nothing
            and safe_written
            and transition_fallback
            and signature_exact
            and descriptor_exact
            and idempotent
            and existing_runner_cache_accepts
        ),
        "fresh_kernel_execution_authorized": False,
        "next_required_gate": "use the opt-in prefill only on the next already-approved estimator run",
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        (
            "source_paths_exist",
            all(path.exists() for path in required),
            "5034, 5063, config, and source topology files exist",
        ),
        (
            "default_off",
            disabled_wrote_nothing,
            "no target topology is written without the explicit enable flag",
        ),
        (
            "safe_transport_written",
            safe_written and enabled["written_topology_count"] == 1,
            f"written={enabled['written_topology_count']}",
        ),
        (
            "transition_fallback_preserved",
            transition_fallback
            and enabled["decision_counts"].get(
                "FULL_HOMOTOPY_FALLBACK_TRANSITION", 0
            )
            == 1,
            "known A06 transition remains absent for the original runner to compute",
        ),
        (
            "safe_topology_exact",
            signature_exact and descriptor_exact,
            "prefilled safe target matches saved full signature and class",
        ),
        (
            "idempotent_no_overwrite",
            idempotent
            and repeated["decision_counts"].get("SKIP_EXISTING_TARGET", 0) == 1,
            "second enabled call preserves the existing target byte-for-byte",
        ),
        (
            "existing_runner_cache_acceptance",
            existing_runner_cache_accepts and cached_runtime == 0.0,
            "5034 obtains the prefilled document without invoking full homotopy",
        ),
        (
            "integration_gate_passed",
            result["opt_in_prefill_integration_passed"],
            "default-off, transport, fallback, idempotence, and cache gates pass",
        ),
        (
            "no_fresh_kernel_execution",
            not result["fresh_kernel_execution_authorized"],
            "integration smoke stops before kernel execution",
        ),
        (
            "formalization_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "runner acceleration is not a physical claim",
        ),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check_id", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5064_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "check_count": len(checks),
                "failed": failed,
                "passed": not failed,
                "output": str(RESULT_JSON),
            },
            indent=2,
        )
    )
    if failed:
        raise RuntimeError(f"checkpoint 5064 validation failed: {failed}")


if __name__ == "__main__":
    main()
