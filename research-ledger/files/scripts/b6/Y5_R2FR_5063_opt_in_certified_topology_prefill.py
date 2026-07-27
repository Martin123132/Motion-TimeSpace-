from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5059 = POST / "scripts" / "Y5_R2FR_5059_short_epsilon_segment_transition_certificate.py"
SCRIPT_5061 = POST / "scripts" / "Y5_R2FR_5061_serialized_transport_topology_constructor_dry_run.py"
MARKER = "MTS_5063_OPT_IN_CERTIFIED_TOPOLOGY_PREFILL"
REVISION = "default-off-certified-transport-prefill-v1"
PROJECTIVE_LIMIT = 0.1


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5059 = load_module("mts_5059_for_5063", SCRIPT_5059)
M5061 = load_module("mts_5061_for_5063", SCRIPT_5061)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def argument_map(config: dict[str, Any], epsilon_id: str) -> dict[str, dict[str, Any]]:
    return {
        str(row["base_argument_id"]): row
        for row in config["arguments"]
        if str(row["epsilon_id"]) == epsilon_id
    }


def target_epsilon(argument: dict[str, Any]) -> float:
    return float(argument["target_cosine"]["imaginary"])


def topology_path(
    run_directory: Path, event_id: str, argument_id: str
) -> Path:
    return run_directory / "topologies" / f"{event_id}__{argument_id}.json"


def prefill(
    run_directory: Path,
    source_epsilon_id: str,
    target_epsilon_id: str,
    enabled: bool,
) -> dict[str, Any]:
    config_path = run_directory / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(config_path)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    source_arguments = argument_map(config, source_epsilon_id)
    target_arguments = argument_map(config, target_epsilon_id)
    common_base_ids = sorted(set(source_arguments) & set(target_arguments))
    if not common_base_ids:
        raise RuntimeError("source and target epsilon layers have no common arguments")
    rows = []
    for event in config["events"]:
        event_id = str(event["event_id"])
        for base_argument_id in common_base_ids:
            source_argument = source_arguments[base_argument_id]
            target_argument = target_arguments[base_argument_id]
            source_path = topology_path(
                run_directory, event_id, str(source_argument["argument_id"])
            )
            target_path = topology_path(
                run_directory, event_id, str(target_argument["argument_id"])
            )
            if not source_path.exists():
                continue
            if target_path.exists():
                rows.append(
                    {
                        "event_id": event_id,
                        "base_argument_id": base_argument_id,
                        "source_path": str(source_path),
                        "target_path": str(target_path),
                        "decision": "SKIP_EXISTING_TARGET",
                        "transition_detected": None,
                        "certificate_converged": None,
                        "written": False,
                    }
                )
                continue
            source_document = json.loads(source_path.read_text(encoding="utf-8"))
            expected_real = float(target_argument["target_cosine"]["real"])
            source_target = complex(str(source_document["target_cosine"]))
            if abs(source_target.real - expected_real) > 1.0e-12:
                raise RuntimeError(
                    f"argument real-part mismatch for {event_id}/{base_argument_id}"
                )
            epsilon = target_epsilon(target_argument)
            level8 = M5059.segment_gate(source_document, 8, epsilon)
            level16 = M5059.segment_gate(source_document, 16, epsilon)
            converged = (
                level8["transition_signature"] == level16["transition_signature"]
                and level8["groups_consistent"]
                and level16["groups_consistent"]
                and max(
                    level8["maximum_projective_assignment_step"],
                    level16["maximum_projective_assignment_step"],
                    level8["maximum_boundary_projective_step"],
                    level16["maximum_boundary_projective_step"],
                )
                < PROJECTIVE_LIMIT
            )
            transition_detected = bool(level16["transition_detected"])
            if not converged:
                decision = "FULL_HOMOTOPY_FALLBACK_UNCERTIFIED"
            elif transition_detected:
                decision = "FULL_HOMOTOPY_FALLBACK_TRANSITION"
            elif not enabled:
                decision = "TRANSPORT_AVAILABLE_DEFAULT_OFF"
            else:
                decision = "CERTIFIED_DIRECT_ROOT_TRANSPORT"
            written = False
            if decision == "CERTIFIED_DIRECT_ROOT_TRANSPORT":
                document = M5061.construct_document(
                    source_document,
                    epsilon,
                    source_path,
                    f"{source_epsilon_id}_TO_{target_epsilon_id}",
                )
                document.update(
                    {
                        "checkpoint_marker": MARKER,
                        "revision": REVISION,
                        "config_digest": config["config_digest"],
                        "event_id": event_id,
                        "argument_id": str(target_argument["argument_id"]),
                        "known_5032_class_at_z1p5": None,
                        "certified_transport_prefill_enabled": True,
                        "certificate_step_levels": [8, 16],
                        "certificate_transition_signature": level16[
                            "transition_signature_json"
                        ],
                        "certificate_maximum_projective_step": max(
                            level8["maximum_projective_assignment_step"],
                            level16["maximum_projective_assignment_step"],
                            level8["maximum_boundary_projective_step"],
                            level16["maximum_boundary_projective_step"],
                        ),
                        "valid_for_full_MTS_claim": False,
                    }
                )
                atomic_json(target_path, document)
                written = True
            rows.append(
                {
                    "event_id": event_id,
                    "base_argument_id": base_argument_id,
                    "source_path": str(source_path),
                    "target_path": str(target_path),
                    "decision": decision,
                    "transition_detected": transition_detected,
                    "certificate_converged": converged,
                    "written": written,
                }
            )
    decision_counts: dict[str, int] = {}
    for row in rows:
        decision_counts[row["decision"]] = decision_counts.get(row["decision"], 0) + 1
    return {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run_directory": str(run_directory),
        "source_epsilon_id": source_epsilon_id,
        "target_epsilon_id": target_epsilon_id,
        "certified_transport_enabled": enabled,
        "default_off": not enabled,
        "source_topology_count": len(rows),
        "written_topology_count": sum(bool(row["written"]) for row in rows),
        "decision_counts": decision_counts,
        "rows": rows,
        "fresh_kernel_execution_authorized": False,
        "valid_for_full_MTS_claim": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-directory", type=Path, required=True)
    parser.add_argument("--source-epsilon-id", default="E040")
    parser.add_argument("--target-epsilon-id", default="E020")
    parser.add_argument("--enable-certified-transport", action="store_true")
    parser.add_argument("--manifest", type=Path)
    arguments = parser.parse_args()
    result = prefill(
        arguments.run_directory.resolve(),
        str(arguments.source_epsilon_id),
        str(arguments.target_epsilon_id),
        bool(arguments.enable_certified_transport),
    )
    if arguments.manifest is not None:
        atomic_json(arguments.manifest.resolve(), result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
