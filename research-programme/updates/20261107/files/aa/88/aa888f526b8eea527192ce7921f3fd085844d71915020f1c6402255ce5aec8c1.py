from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import platform

import mpmath
import numpy
import psutil
import scipy
import sympy


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
OUTPUT = ROOT / "results" / "stage-integrity.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to replace a sealed result.")
    parent_path = BRANCH / "results" / "stage-integrity.json"
    parent = json.loads(parent_path.read_text(encoding="utf-8"))
    assert parent["state"] == "complete"
    for relative, expected in parent["file_hashes"].items():
        source = POST / relative
        assert source.is_file(), source
        assert digest(source) == expected, source
    manifest = POST / "_checkpoints" / "20261003-pre-condensate-origin" / "manifest.json"
    assert digest(manifest) == parent["snapshot_manifest_sha256"]

    algebra = json.loads((ROOT / "results/algebra/status.json").read_text(encoding="utf-8"))
    spectrum = json.loads((ROOT / "results/full-spectrum-v4/status.json").read_text(encoding="utf-8"))
    kernel = json.loads((ROOT / "results/off-shell-kernel/status.json").read_text(encoding="utf-8"))
    assert all(report["state"] == "complete" for report in [algebra, spectrum, kernel])
    assert len(algebra["checks"]) == 46 and all(check["passed"] for check in algebra["checks"])
    assert len(spectrum["checks"]) == 174 and all(check["passed"] for check in spectrum["checks"])
    assert len(spectrum["full_spectrum_rows"]) == 21
    assert len(spectrum["partial_wave_rows"]) == 7
    for row in spectrum["full_spectrum_rows"]:
        assert row["total"] >= 0
        assert all(value >= 0 for value in row["channels"].values())
    for row in spectrum["partial_wave_rows"]:
        assert Decimal(row["relative_error"]) < Decimal("1e-35")
        assert Decimal(row["l2_projection"]) > 0
    assert len(kernel["exact_checks"]) == 9 and all(check["passed"] for check in kernel["exact_checks"])
    assert len(kernel["angular_checks"]) == 28 and all(check["passed"] for check in kernel["angular_checks"])
    for check in kernel["angular_checks"]:
        assert Decimal(check["absolute_error"]) <= Decimal(check["budget"])
    assert len(kernel["static_limit_checks"]) == 2 and all(check["passed"] for check in kernel["static_limit_checks"])
    assert not spectrum["full_resummed_interacting_collective_pole_test_performed"]
    assert not kernel["full_resummed_interacting_pole_test_performed"]
    assert algebra["parent_sha256"] == digest(parent_path)
    assert spectrum["algebra_sha256"] == digest(ROOT / "results/algebra/status.json")
    assert kernel["algebra_source_sha256"] == digest(ROOT / "results/algebra/status.json")
    failures = []
    for folder in ["full-spectrum", "full-spectrum-v2", "full-spectrum-v3"]:
        path = ROOT / "results" / folder / "FAILED.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["state"] == "failed"
        failures.append({"path": path.relative_to(ROOT).as_posix(), "error": data["error"]})

    required = [
        BRANCH / "01-first-condensate-derivation.md",
        parent_path,
        POST / "CHECKPOINT-20261003-BEFORE-CONDENSATE.md",
        ROOT / "02-full-tensor-response-and-collective-kernel.md",
        ROOT / "RESULTS.md",
        ROOT / "RESUME.md",
    ]
    assert all(path.is_file() for path in required)
    document = (ROOT / "02-full-tensor-response-and-collective-kernel.md").read_text(encoding="utf-8")
    web_sources = [
        "https://arxiv.org/abs/1001.1044",
        "https://doi.org/10.1088/1367-2630/12/9/095012",
        "https://arxiv.org/abs/1407.7896",
        "https://doi.org/10.1103/PhysRevD.90.104015",
    ]
    assert all(url in document for url in web_sources)
    scripts = sorted(ROOT.glob("*.py"))
    for path in scripts:
        compile(path.read_bytes(), str(path), "exec")
    assert not list(ROOT.rglob("__pycache__"))
    protected = POST.parent / "formalization-workbench"
    assert protected.is_dir()
    turn_start = datetime(2026, 10, 3, 13, 46, 28, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob("*")
               if path.is_file() and path.stat().st_mtime > turn_start.timestamp()]
    assert not changed, changed
    own_hashes = {path.relative_to(ROOT).as_posix(): digest(path)
                  for path in sorted(ROOT.rglob("*")) if path.is_file() and path != OUTPUT}
    report = {
        "state": "complete", "sealed_at": datetime.now(timezone.utc).isoformat(),
        "file_hashes": own_hashes, "parent_seal_sha256": digest(parent_path),
        "previous_sealed_files_reverified": len(parent["file_hashes"]),
        "checkpoint_manifest_sha256": digest(manifest),
        "checkpoint_payload_rehashed_this_stage": False,
        "checkpoint_note": "Previous stage validated the full payload; this stage verifies its manifest and all 26 parent seal entries, not a new 13GB payload replay.",
        "exact_identity_checks": 55, "numerical_checks": 174,
        "two_mode_spectrum_rows": 21, "on_shell_high_precision_angular_checks": 7,
        "independent_high_precision_energy_inversions": 12,
        "off_shell_high_precision_matrix_checks": 28, "static_limit_checks": 2,
        "scripts_compiled": len(scripts), "preserved_failures": failures,
        "required_local_sources": [str(path) for path in required],
        "web_source_strings": web_sources,
        "protected_workbench_recent_modified_file_count": len(changed),
        "protected_check_scope": "Modification-time scan since this turn started; not a full content-hash comparison of that directory.",
        "versions": {"python": platform.python_version(), "numpy": numpy.__version__,
                     "scipy": scipy.__version__, "sympy": sympy.__version__, "mpmath": mpmath.__version__},
        "new_writes_scope": "tensor-response-20261003, plus mutable navigation handoffs after sealing",
        "github_action": False, "subagents": 0,
        "full_interacting_collective_pole_equation_solved": False,
        "quadrature_refinements_are_interval_certificates": False,
        "candidate_adopted_into_original_framework": False,
    }
    OUTPUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({key: report[key] for key in [
        "state", "previous_sealed_files_reverified", "exact_identity_checks",
        "numerical_checks", "two_mode_spectrum_rows", "scripts_compiled",
        "off_shell_high_precision_matrix_checks", "protected_workbench_recent_modified_file_count"
    ]}))


if __name__ == "__main__":
    main()
