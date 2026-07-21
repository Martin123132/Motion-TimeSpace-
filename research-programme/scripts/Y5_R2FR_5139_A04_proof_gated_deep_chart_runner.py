from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
GENERIC_RUNNER = POST / "scripts" / "Y5_R2FR_5132_locked_next_argument_gate_and_single_job_runner.py"
PROOF = POST / "source-intake" / "functional_rg" / "5138" / "A04_KLT_collinear_pole_order_proof.json"
DEFAULT_REJECTED_GATE = POST / "source-intake" / "functional_rg" / "5135" / "A04_argument_local_outer_collinear_chart_gate.json"

CHECKPOINT_ID = "5139"
CHECKED_DATE = "2026-07-20"
JOB_KEY = "E040__S512503_N0000__A04__primary24"
DEEP_PROFILE = {
    "low_boundary_nodes": 96,
    "low_global_nodes": 128,
    "low_global_residue_nodes": 192,
    "high_boundary_nodes": 128,
    "high_global_nodes": 192,
    "high_global_residue_nodes": 256,
    "selection": "authorized only by the 5138 exact KLT simple-pole proof after the preserved default Laurent-order rejection",
    "acceptance_threshold_changed": False,
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def configure(mode: str) -> tuple[Any, dict[str, Any]]:
    runner = load_module("mts_5132_for_5139", GENERIC_RUNNER)
    proof = runner.M5128.read_json(PROOF)
    default_gate = runner.M5128.read_json(DEFAULT_REJECTED_GATE)
    if not proof.get("simple_pole_order_proved_for_implemented_integrand"):
        raise RuntimeError("5139 deep precision requires the signed 5138 simple-pole proof")
    if default_gate.get("gate_accepted"):
        raise RuntimeError("5139 expected a preserved rejected default A04 gate")
    arguments = argparse.Namespace(
        checkpoint_id=CHECKPOINT_ID,
        checked_date=CHECKED_DATE,
        job_key=JOB_KEY,
        precision="default",
        mode=mode,
    )
    job, configuration = runner.configure(arguments)
    base = runner.M5128
    if job["job_key"] != JOB_KEY:
        raise RuntimeError(f"5139 selected the wrong locked job: {job['job_key']}")
    base.REVISION = "proof-gated-deep-argument-log-cauchy-chart-v1"
    base.M5127.REVISION = base.REVISION
    base.PRECISION_POLICY = dict(DEEP_PROFILE)
    base.M5127.LOW_BOUNDARY_NODES = DEEP_PROFILE["low_boundary_nodes"]
    base.M5127.LOW_GLOBAL_NODES = DEEP_PROFILE["low_global_nodes"]
    base.M5127.LOW_RESIDUE_NODES = DEEP_PROFILE["low_global_residue_nodes"]
    base.M5127.HIGH_BOUNDARY_NODES = DEEP_PROFILE["high_boundary_nodes"]
    base.M5127.HIGH_GLOBAL_NODES = DEEP_PROFILE["high_global_nodes"]
    base.M5127.HIGH_RESIDUE_NODES = DEEP_PROFILE["high_global_residue_nodes"]
    if base.INITIAL_REJECTED_GATE is None:
        raise RuntimeError("5139 missing rejected-gate destination")
    if not base.INITIAL_REJECTED_GATE.exists():
        base.atomic_json(base.INITIAL_REJECTED_GATE, default_gate)
    configuration.update(
        {
            "precision": "proof-gated-deep",
            "precision_profile": DEEP_PROFILE,
            "simple_pole_proof": base.relative(PROOF),
            "simple_pole_proof_sha256": base.M5127.digest(PROOF),
            "source_default_rejected_gate": base.relative(DEFAULT_REJECTED_GATE),
            "source_default_rejected_gate_sha256": base.M5127.digest(
                DEFAULT_REJECTED_GATE
            ),
            "acceptance_threshold_changed": False,
            "mode": mode,
        }
    )
    base.atomic_json(base.SOURCE / "locked_next_job_configuration.json", configuration)
    return runner, configuration


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("gate", "execute"), default="gate")
    arguments = parser.parse_args()
    runner, configuration = configure(arguments.mode)
    if arguments.mode == "gate":
        result = runner.M5128.gate_only()
    else:
        result = runner.M5128.execute()
    print(
        json.dumps(
            {"configuration": configuration, "result": result},
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
