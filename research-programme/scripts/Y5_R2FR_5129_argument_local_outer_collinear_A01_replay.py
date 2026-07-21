from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5128 = (
    POST
    / "scripts"
    / "Y5_R2FR_5128_argument_local_outer_collinear_preflight_and_A11_replay.py"
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5128 = load_module("mts_5128_for_5129", SCRIPT_5128)

CHECKPOINT_ID = "5129"
MARKER = "MTS_5129_ARGUMENT_LOCAL_OUTER_COLLINEAR_A01"
REVISION = "argument-local-log-cauchy-chart-v2"
CHECKED_DATE = "2026-07-20"
JOB_KEY = "E040__S512503_N0000__A01__primary24"
BASE_ARGUMENT_ID = "A01"
SOURCE = POST / "source-intake" / "functional_rg" / CHECKPOINT_ID
INITIAL_REJECTED_GATE = SOURCE / "A01_initial_rejected_chart_gate.json"

M5128.CHECKPOINT_ID = CHECKPOINT_ID
M5128.MARKER = MARKER
M5128.REVISION = REVISION
M5128.CHECKED_DATE = CHECKED_DATE
M5128.JOB_KEY = JOB_KEY
M5128.BASE_ARGUMENT_ID = BASE_ARGUMENT_ID
M5128.SOURCE = SOURCE
M5128.PREFLIGHT_JSON = SOURCE / "A01_argument_local_outer_collinear_preflight.json"
M5128.GATE_JSON = SOURCE / "A01_argument_local_outer_collinear_chart_gate.json"
M5128.CATALOG_CSV = SOURCE / "A01_argument_local_outer_collinear_catalog.csv"
M5128.RESULT_JSON = SOURCE / "A01_argument_local_outer_collinear_replay_result.json"
M5128.STATUS_JSON = SOURCE / "A01_argument_local_outer_collinear_replay_status.json"
M5128.VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5129_VALIDATION.csv"
)
M5128.DOCUMENT = (
    POST
    / "5129-Y5-R2FR-argument-local-outer-collinear-A01-replay.md"
)
M5128.INITIAL_REJECTED_GATE = INITIAL_REJECTED_GATE
M5128.PRECISION_POLICY = {
    "low_boundary_nodes": 48,
    "low_global_nodes": 64,
    "low_global_residue_nodes": 96,
    "high_boundary_nodes": 64,
    "high_global_nodes": 96,
    "high_global_residue_nodes": 128,
    "selection": (
        "nested precision refinement after the default boundary pair failed; "
        "acceptance thresholds and chart radii unchanged"
    ),
    "acceptance_threshold_changed": False,
}
M5128.EXPECTED_COUNTS_AFTER = {
    "completed_converged": 45,
    "completed_unconverged": 0,
    "failed": 0,
    "missing": 515,
}
M5128.M5127.JOB_KEY = JOB_KEY
M5128.M5127.MARKER = MARKER
M5128.M5127.REVISION = REVISION
M5128.M5127.CHECKED_DATE = CHECKED_DATE
M5128.M5127.LOW_BOUNDARY_NODES = 48
M5128.M5127.LOW_GLOBAL_NODES = 64
M5128.M5127.LOW_RESIDUE_NODES = 96
M5128.M5127.HIGH_BOUNDARY_NODES = 64
M5128.M5127.HIGH_GLOBAL_NODES = 96
M5128.M5127.HIGH_RESIDUE_NODES = 128


if __name__ == "__main__":
    if M5128.GATE_JSON.exists() and not INITIAL_REJECTED_GATE.exists():
        rejected = M5128.read_json(M5128.GATE_JSON)
        if not bool(rejected.get("gate_accepted")):
            M5128.atomic_json(INITIAL_REJECTED_GATE, rejected)
    M5128.main()
