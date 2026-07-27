from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
PILOT_V6 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v6"
)
CERTIFICATE_5088 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5088"
    / "exact_same_source_double_zero_collision_certificate.json"
)
GATE_5088 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5088"
    / "E020_A07_primary24_exact_collision_gate.json"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5089"
RUN = SOURCE / "exact_double_zero_runner_integration_smoke"
RESULT_JSON = SOURCE / "exact_double_zero_runner_integration_smoke.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5089_VALIDATION.csv"
)
MARKER = "MTS_5089_EXACT_DOUBLE_ZERO_RUNNER_INTEGRATION_SMOKE"
REVISION = "targeted-new-config-carry-forward-topology-smoke-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EVENT_ID = "S507603_N0000"
ARGUMENT_ID = "E020_A07"
JOB_KEY = "E020__S507603_N0000__A07__primary24"
RUN_ID = "5089_exact_double_zero_runner_integration_smoke"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


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


def main() -> None:
    source_topology = (
        PILOT_V6 / "topologies" / f"{EVENT_ID}__{ARGUMENT_ID}.json"
    )
    required = [
        SCRIPT_5077,
        PILOT_V6 / "config.json",
        source_topology,
        CERTIFICATE_5088,
        GATE_5088,
        FORMAL,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5089 inputs: {missing}")
    module_5077 = load_module("mts_5077_for_5089", SCRIPT_5077)
    manifest = json.loads(module_5077.MANIFEST.read_text(encoding="utf-8"))
    config = module_5077.make_config(manifest, RUN_ID)
    RUN.mkdir(parents=True, exist_ok=True)
    atomic_json(RUN / "config.json", config)
    carried_topology = json.loads(source_topology.read_text(encoding="utf-8"))
    source_topology_config_digest = carried_topology["config_digest"]
    carried_topology["config_digest"] = config["config_digest"]
    carried_topology["checkpoint_marker"] = MARKER
    carried_topology["5089_topology_carry_forward"] = {
        "source_path": str(source_topology),
        "source_sha256": digest(source_topology),
        "source_config_digest": source_topology_config_digest,
        "target_config_digest": config["config_digest"],
        "reason": (
            "5088 changes only the global collision-value extension; the saved "
            "causal topology and target roots are unchanged"
        ),
        "valid_for_full_MTS_claim": False,
    }
    topology_output = module_5077.M5036.M5035.M5034.topology_path(
        RUN, EVENT_ID, ARGUMENT_ID
    )
    atomic_json(topology_output, carried_topology)
    module_5077.install_history_invariant_breakpoints(module_5077.M5036.N5030)
    module_5077.install_history_invariant_breakpoints(module_5077.M5043.N5030)
    manager = module_5077.CentralTopologyManager(RUN, config)
    job = {
        "job_key": JOB_KEY,
        "profile": "primary24",
        "epsilon_id": "E020",
        "event_id": EVENT_ID,
        "base_argument_id": "A07",
    }
    job_path = RUN / "jobs" / f"{JOB_KEY}.json"
    first = (
        json.loads(job_path.read_text(encoding="utf-8"))
        if job_path.exists()
        else module_5077.execute_kernel(RUN, config, manager, job)
    )
    second = module_5077.execute_kernel(RUN, config, manager, job)
    kernel_path = RUN / "kernels" / f"{JOB_KEY}.json"
    kernel = (
        json.loads(kernel_path.read_text(encoding="utf-8"))
        if kernel_path.exists()
        else None
    )
    gate_5088 = json.loads(GATE_5088.read_text(encoding="utf-8"))
    certificate_5088 = json.loads(CERTIFICATE_5088.read_text(encoding="utf-8"))
    fixed_gate = kernel["fixed_event_integral_gate"] if kernel is not None else None
    exact_count = (
        int(
            kernel["profile_audit"][
                "exact_double_zero_collision_extension_count"
            ]
        )
        if kernel is not None
        else 0
    )
    numerical_limit_count = (
        int(
            kernel["profile_audit"][
                "removable_global_collision_extension_count"
            ]
        )
        if kernel is not None
        else 0
    )
    highest = (
        module_5077.M5036.M5035.M5034.highest_value(fixed_gate)
        if fixed_gate is not None
        else None
    )
    reference_highest = (
        module_5077.M5036.complex_from_row(gate_5088["highest_value"])
        if gate_5088["highest_value"] is not None
        else None
    )
    highest_relative_residual = (
        abs(highest - reference_highest) / max(1.0, abs(reference_highest))
        if highest is not None and reference_highest is not None
        else None
    )
    event_residual_relative_residual = abs(
        float(fixed_gate["highest_two_order_relative_residual"])
        - float(gate_5088["highest_two_order_relative_residual"])
    ) / max(
        abs(float(gate_5088["highest_two_order_relative_residual"])),
        1.0e-30,
    )
    reference_calls = {
        row["ownership_digest"]: complex(
            row["returned_value"]["real"],
            row["returned_value"]["imaginary"],
        )
        for row in gate_5088["double_zero_extension_calls"]
    }
    integrated_calls = {
        row["ownership_digest"]: complex(
            row["returned_value"]["real"],
            row["returned_value"]["imaginary"],
        )
        for row in kernel["profile_audit"][
            "exact_double_zero_collision_extensions"
        ]
    }
    extension_value_maximum_relative_residual = max(
        abs(integrated_calls[key] - reference_calls[key])
        / max(1.0, abs(reference_calls[key]))
        for key in reference_calls
    )
    formal_digest = tree_digest(FORMAL)
    accepted = bool(
        first["status"] == "COMPLETED_CONVERGED"
        and not first["resumed_from_cache"]
        and second["status"] == "COMPLETED_CONVERGED"
        and second["resumed_from_cache"]
        and fixed_gate is not None
        and fixed_gate["fixed_event_crossed_integral_converged"]
        and fixed_gate["all_residues_stable"]
        and exact_count == 2
        and numerical_limit_count == 0
        and set(integrated_calls) == set(reference_calls)
        and extension_value_maximum_relative_residual < 1.0e-12
        and event_residual_relative_residual < 1.0e-12
        and certificate_5088["runner_integration_authorized"]
        and formal_digest == FORMAL_BASELINE
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run_directory": str(RUN),
        "config_digest": config["config_digest"],
        "job_key": JOB_KEY,
        "source_topology": str(source_topology),
        "source_topology_sha256": digest(source_topology),
        "carried_topology": str(topology_output),
        "carried_topology_sha256": digest(topology_output),
        "first_execution": first,
        "second_execution": second,
        "kernel_path": str(kernel_path),
        "kernel_sha256": digest(kernel_path) if kernel_path.exists() else None,
        "fixed_event_converged": bool(
            fixed_gate
            and fixed_gate["fixed_event_crossed_integral_converged"]
        ),
        "all_residues_stable": bool(
            fixed_gate and fixed_gate["all_residues_stable"]
        ),
        "highest_two_order_relative_residual": (
            float(fixed_gate["highest_two_order_relative_residual"])
            if fixed_gate is not None
            else None
        ),
        "highest_value": (
            module_5077.M5036.complex_row(highest)
            if highest is not None
            else None
        ),
        "reference_5088_highest_value": gate_5088["highest_value"],
        "highest_value_relative_residual": highest_relative_residual,
        "highest_value_difference_source": (
            "production history-invariant breakpoint filter is installed in "
            "5089 but was absent from the standalone 5088 event gate"
        ),
        "event_convergence_residual_relative_residual": (
            event_residual_relative_residual
        ),
        "extension_value_maximum_relative_residual": (
            extension_value_maximum_relative_residual
        ),
        "exact_double_zero_extension_count": exact_count,
        "numerical_limit_extension_count": numerical_limit_count,
        "runner_exact_guard_integration_accepted": accepted,
        "pilot_resume_authorized": accepted,
        "full_pilot_result_claimed": False,
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", not missing, "all integration-smoke inputs exist"),
        (
            "topology_carry_forward_exact",
            carried_topology["5089_topology_carry_forward"]["source_sha256"]
            == digest(source_topology),
            str(source_topology),
        ),
        (
            "fresh_execution_converged",
            first["status"] == "COMPLETED_CONVERGED"
            and not first["resumed_from_cache"],
            first["status"],
        ),
        (
            "cache_resume_exercised",
            second["status"] == "COMPLETED_CONVERGED"
            and second["resumed_from_cache"],
            f"status={second['status']}; resumed={second['resumed_from_cache']}",
        ),
        (
            "event_gate_converged_and_stable",
            result["fixed_event_converged"] and result["all_residues_stable"],
            f"residual={result['highest_two_order_relative_residual']}",
        ),
        (
            "exact_guard_exercised_only",
            exact_count == 2 and numerical_limit_count == 0,
            f"exact={exact_count}; numerical_limit={numerical_limit_count}",
        ),
        (
            "local_extension_and_convergence_reproduced",
            set(integrated_calls) == set(reference_calls)
            and extension_value_maximum_relative_residual < 1.0e-12
            and event_residual_relative_residual < 1.0e-12,
            (
                f"extension={extension_value_maximum_relative_residual}; "
                f"event_residual={event_residual_relative_residual}; "
                f"final_value_diagnostic={highest_relative_residual}"
            ),
        ),
        (
            "resume_authorization_consistent",
            result["pilot_resume_authorized"] == accepted,
            f"accepted={accepted}",
        ),
        (
            "formalization_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "claim_discipline",
            not result["full_pilot_result_claimed"]
            and not result["valid_for_full_MTS_claim"],
            "runner integration is not amplitude or MTS evidence",
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
                    "check_id": f"V5089_{index:02d}_{name}",
                    "passed": bool(passed),
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5089 validation failed: {failed}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
