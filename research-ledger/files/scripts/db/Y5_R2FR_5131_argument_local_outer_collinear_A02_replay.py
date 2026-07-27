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


M5128 = load_module("mts_5128_for_5131", SCRIPT_5128)

CHECKPOINT_ID = "5131"
MARKER = "MTS_5131_ARGUMENT_LOCAL_OUTER_COLLINEAR_A02"
REVISION = "argument-local-log-cauchy-chart-v3"
CHECKED_DATE = "2026-07-20"
JOB_KEY = "E040__S512503_N0000__A02__primary24"
BASE_ARGUMENT_ID = "A02"
SOURCE = POST / "source-intake" / "functional_rg" / CHECKPOINT_ID
INITIAL_REJECTED_GATE = SOURCE / "A02_initial_rejected_chart_gate.json"

M5128.CHECKPOINT_ID = CHECKPOINT_ID
M5128.MARKER = MARKER
M5128.REVISION = REVISION
M5128.CHECKED_DATE = CHECKED_DATE
M5128.JOB_KEY = JOB_KEY
M5128.BASE_ARGUMENT_ID = BASE_ARGUMENT_ID
M5128.SOURCE = SOURCE
M5128.PREFLIGHT_JSON = SOURCE / "A02_argument_local_outer_collinear_preflight.json"
M5128.GATE_JSON = SOURCE / "A02_argument_local_outer_collinear_chart_gate.json"
M5128.CATALOG_CSV = SOURCE / "A02_argument_local_outer_collinear_catalog.csv"
M5128.RESULT_JSON = SOURCE / "A02_argument_local_outer_collinear_replay_result.json"
M5128.STATUS_JSON = SOURCE / "A02_argument_local_outer_collinear_replay_status.json"
M5128.VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5131_VALIDATION.csv"
)
M5128.DOCUMENT = (
    POST
    / "5131-Y5-R2FR-argument-local-outer-collinear-A02-replay.md"
)
M5128.INITIAL_REJECTED_GATE = INITIAL_REJECTED_GATE
M5128.EXPECTED_COUNTS_AFTER = {
    "completed_converged": 47,
    "completed_unconverged": 0,
    "failed": 0,
    "missing": 513,
}
M5128.M5127.JOB_KEY = JOB_KEY
M5128.M5127.MARKER = MARKER
M5128.M5127.REVISION = REVISION
M5128.M5127.CHECKED_DATE = CHECKED_DATE


if __name__ == "__main__":
    if M5128.GATE_JSON.exists() and not INITIAL_REJECTED_GATE.exists():
        rejected = M5128.read_json(M5128.GATE_JSON)
        if not bool(rejected.get("gate_accepted")):
            M5128.atomic_json(INITIAL_REJECTED_GATE, rejected)
    M5128.main()
