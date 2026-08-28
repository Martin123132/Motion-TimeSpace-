from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
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


POST = Path(__file__).resolve().parents[1]
GATE_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5370_D4_six_rung_complete_family_outer_limit_gate.py"
)
ADAPTER_REVISION = "D4-six-rung-gate-numpy-scalar-serialization-adapter-v1"
ADAPTER_GATE = "postmeasurement_serialization_adapter_preserves_scientific_payload"


def load_gate_module() -> Any:
    specification = importlib.util.spec_from_file_location("mts_5370_frozen_gate", GATE_SCRIPT)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import frozen gate {GATE_SCRIPT}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def normalize_scalars(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: normalize_scalars(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize_scalars(item) for item in value]
    value_type = type(value)
    if value_type.__module__.startswith("numpy") and hasattr(value, "item"):
        return value.item()
    return value


def serialized_hash(value: Any) -> str:
    normalized = normalize_scalars(value)
    return hashlib.sha256(
        json.dumps(
            normalized,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


def frozen_source_certificate(module: Any) -> dict[str, Any]:
    contract = module.read_json(module.GATE_CONTRACT)
    rows = module.read_csv(module.GATE_CONTRACT_SOURCES)
    matches = [
        row
        for row in rows
        if Path(row["path"]).name == GATE_SCRIPT.name
    ]
    current_hash = digest(GATE_SCRIPT)
    checks = {
        "exactly_one_frozen_gate_source_row": len(matches) == 1,
        "frozen_gate_source_hash_is_current": len(matches) == 1
        and matches[0]["sha256"] == current_hash,
        "gate_contract_passed_before_measurement": contract.get("validation_passed")
        is True
        and contract.get("measurement_absent_at_freeze") is True
        and contract.get("gate_executed") is False,
        "adapter_revision_is_serialization_only": ADAPTER_REVISION
        == "D4-six-rung-gate-numpy-scalar-serialization-adapter-v1",
    }
    if not all(checks.values()):
        raise RuntimeError(f"frozen gate source certificate failed: {checks}")
    return {
        "checks": checks,
        "frozen_gate_script_sha256": current_hash,
        "contract_sha256": digest(module.GATE_CONTRACT),
    }


def append_adapter_evidence(
    module: Any,
    result: dict[str, Any],
    certificate: dict[str, Any],
    scientific_payload_hash: str,
) -> dict[str, Any]:
    adapter_path = Path(__file__).resolve()
    adapter_hash = digest(adapter_path)
    claims = normalize_scalars(result["claim_boundary"])
    source_rows = [
        row
        for row in module.read_csv(module.SOURCE_REGISTER)
        if Path(row["path"]).name != adapter_path.name
    ]
    source_rows.append(
        {
            "path": str(adapter_path),
            "sha256": adapter_hash,
            "exists": True,
            "role": "POSTMEASUREMENT_SERIALIZATION_ONLY__NO_SCIENTIFIC_BRANCH_OR_THRESHOLD_CHANGE",
            **claims,
        }
    )
    module.atomic_csv(module.SOURCE_REGISTER, source_rows)

    validation_detail = {
        "adapter_revision": ADAPTER_REVISION,
        "adapter_sha256": adapter_hash,
        "frozen_gate_script_sha256": certificate["frozen_gate_script_sha256"],
        "scientific_payload_sha256_before_metadata": scientific_payload_hash,
        "conversion_rule": "numpy scalar -> Python scalar via item(); containers recurse; all other values unchanged",
        "scientific_branch_or_threshold_changed": False,
    }
    for validation_path in (module.VALIDATION, module.RESIDUAL_VALIDATION):
        rows = [
            row
            for row in module.read_csv(validation_path)
            if row.get("gate") != ADAPTER_GATE
        ]
        rows.append(module.validation_row(ADAPTER_GATE, True, validation_detail))
        module.atomic_csv(validation_path, rows)

    updated = dict(result)
    updated["serialization_adapter"] = {
        "revision": ADAPTER_REVISION,
        "path": str(adapter_path),
        "sha256": adapter_hash,
        "frozen_gate_script_sha256": certificate["frozen_gate_script_sha256"],
        "frozen_gate_contract_sha256": certificate["contract_sha256"],
        "scientific_payload_sha256_before_metadata": scientific_payload_hash,
        "scientific_branch_or_threshold_changed": False,
    }
    module.atomic_json(module.RESULT, updated)
    module.render_document(updated)
    with module.DOCUMENT.open("a", encoding="utf-8") as handle:
        handle.write(
            "\nThe frozen gate first completed its mathematics but exposed NumPy boolean scalars to the standard JSON writer. The recorded adapter verifies the preregistered script hash and converts only scalar representation; no fit, threshold, gate, or claim rule changed.\n"
        )
    return updated


def run() -> dict[str, Any]:
    module = load_gate_module()
    module.set_below_normal_priority()
    certificate = frozen_source_certificate(module)
    original_atomic_json = module.atomic_json

    def scalar_safe_atomic_json(path: Path, payload: dict[str, Any]) -> None:
        original_atomic_json(path, normalize_scalars(payload))

    module.atomic_json = scalar_safe_atomic_json
    raw_result = module.execute_gate()
    normalized_result = normalize_scalars(raw_result)
    saved_result = module.read_json(module.RESULT)
    scientific_payload_hash = serialized_hash(normalized_result)
    if serialized_hash(saved_result) != scientific_payload_hash:
        raise RuntimeError("serialization adapter changed the scientific payload")
    return append_adapter_evidence(
        module,
        normalized_result,
        certificate,
        scientific_payload_hash,
    )


def main() -> int:
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return 0 if result.get("validation_passed") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
