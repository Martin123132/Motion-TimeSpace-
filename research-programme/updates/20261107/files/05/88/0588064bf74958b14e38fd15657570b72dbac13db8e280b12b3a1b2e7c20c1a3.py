from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import mpmath as mp
import numpy as np
import psutil

from operator_core import Candidate, q2, q2_derivative


ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / "tensor-response-20261003"
POST = ROOT.parent.parent
OUTPUT = ROOT / "results" / "stage-integrity.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to overwrite a sealed stage.")
    previous_path = PREVIOUS / "results/stage-integrity.json"
    previous = json.loads(previous_path.read_text(encoding="utf-8"))
    for relative, expected in previous["file_hashes"].items():
        path = PREVIOUS / relative
        assert path.is_file() and digest(path) == expected, str(path)
    older_path = ROOT.parent / "results/stage-integrity.json"
    assert digest(older_path) == previous["parent_seal_sha256"]
    older = json.loads(older_path.read_text(encoding="utf-8"))
    for relative, expected in older["file_hashes"].items():
        path = POST / relative
        assert path.is_file() and digest(path) == expected, str(path)
    manifest = POST / "_checkpoints/20261003-pre-condensate-origin/manifest.json"
    assert digest(manifest) == previous["checkpoint_manifest_sha256"]

    normalization = json.loads((ROOT / "results/normalization/status.json").read_text(encoding="utf-8"))
    soft = json.loads((ROOT / "results/soft-identities/status.json").read_text(encoding="utf-8"))
    first_pass = json.loads((ROOT / "results/static-operator/status.json").read_text(encoding="utf-8"))
    refinement = json.loads((ROOT / "results/fixed-infrared-refinement/status.json").read_text(encoding="utf-8"))
    assert all(report["state"] == "complete" for report in [normalization, soft, first_pass, refinement])
    assert len(normalization["exact_checks"]) == 16
    assert len(normalization["numerical_checks"]) == 116
    assert soft["exact_checks"] == 8
    assert all(item["passed"] for item in normalization["exact_checks"] + normalization["numerical_checks"] + soft["checks"])
    for report in [normalization, first_pass, refinement]:
        assert report["core_sha256"] == digest(ROOT / "operator_core.py")
    assert refinement["explicit_mesh_sha256"] == digest(ROOT / "operator_explicit_mesh.py")
    assert first_pass["normalization_sha256"] == digest(ROOT / "results/normalization/status.json")
    assert soft["parent_sha256"] == digest(previous_path)
    assert len(first_pass["rows"]) == 11 and len(refinement["rows"]) == 5

    replay = []
    for group, report in [("static-operator", first_pass), ("fixed-infrared-refinement", refinement)]:
        for row in report["rows"]:
            folder = ROOT / "results" / group / row["name"]
            matrix = np.load(folder / "operator.npy", allow_pickle=False)
            saved = np.load(folder / "diagnostics.npz", allow_pickle=False)
            assert matrix.shape == (row["matrix_dimension"], row["matrix_dimension"])
            assert np.all(np.isfinite(matrix))
            eigenvalues = saved["eigenvalues"]
            assert abs(float(np.max(np.abs(eigenvalues))) - row["spectral_radius"]) < 1e-15
            real_index = int(np.argmax(eigenvalues.real))
            assert abs(eigenvalues[real_index].imag) < 1e-12
            if group == "fixed-infrared-refinement":
                weights = saved["positive_norm_weights"]
                assert np.all(np.isfinite(weights)) and np.all(weights > 0)
                bound = float(np.max((np.abs(matrix) @ weights) / weights))
                assert abs(bound - row["positive_weight_comparison_bound"]) < 1e-14
                assert np.max(np.abs(eigenvalues)) < bound < 1
                replay.append({"name": row["name"], "weighted_bound": bound, "passed": True})
            else:
                bound = float(np.max(np.sum(np.abs(matrix), axis=1)))
                assert abs(bound - row["infinity_norm"]) < 1e-14
                source, vertex = saved["source"], saved["stress_vertex"]
                residual = float(np.max(np.abs(vertex - source - matrix @ vertex)))
                assert residual < 1e-10
                replay.append({"name": row["name"], "vertex_residual": residual, "passed": True})
    assert len({row["first_center"] for row in refinement["rows"][:3]}) == 1
    cutoff_change = refinement["rows"][2]["largest_positive_eigenvalue"] / refinement["rows"][0]["largest_positive_eigenvalue"] - 1
    infrared_change = refinement["rows"][3]["largest_positive_eigenvalue"] / refinement["rows"][1]["largest_positive_eigenvalue"] - 1
    quadrature_change = refinement["rows"][4]["largest_positive_eigenvalue"] / refinement["rows"][3]["largest_positive_eigenvalue"] - 1

    mp.mp.dps = 100
    Q2 = lambda value: (3 * value**2 - 1) * mp.log((value + 1) / (value - 1)) / 4 - 3 * value / 2
    accuracy = []
    for value in [mp.mpf("1.0001"), mp.mpf(2), mp.mpf("3.0001"), mp.mpf(10), mp.mpf("1000000"), mp.mpc(1, 2), mp.mpc(3, 5)]:
        for name, actual, expected in [
            ("Q2", q2(np.array([complex(value)]))[0], Q2(value)),
            ("Q2_derivative", q2_derivative(np.array([complex(value)]))[0], mp.diff(Q2, value))
        ]:
            relative = abs(complex(actual) - expected) / abs(expected)
            assert relative < mp.mpf("1e-8"), (name, value, relative)
            accuracy.append({"name": f"{name}_{value}", "relative_error": str(relative), "passed": True})
    model = Candidate()
    mass = mp.mpf(10) / 9
    for frequency, first, second in [(mp.mpf(8), mp.mpf(".01"), mp.mpf(".03")),
                                    (mp.mpf(".2"), mp.mpf(".7"), mp.mpf(".7"))]:
        actual = model.exchange_l2(np.array([float(frequency)]), np.array([float(first)]), np.array([float(second)]))[0]
        for row in range(2):
            for column in range(2):
                def integrand(angle):
                    squared = frequency**2 + first**2 + second**2 - 2 * first * second * angle
                    determinant = squared * (squared + mass) + 4 * frequency**2
                    entry = [[squared, 2 * frequency], [-2 * frequency, squared + mass]][row][column]
                    return (3 * angle**2 - 1) * entry / (4 * determinant)
                expected = mp.quad(integrand, [-1, 0, 1])
                relative = abs(float(actual[row, column]) - expected) / abs(expected)
                assert relative < mp.mpf("1e-8"), (frequency, row, column, relative)
                accuracy.append({"name": f"relative_projected_entry_{frequency}_{row}_{column}", "relative_error": str(relative), "passed": True})
    assert not list(ROOT.rglob("FAILED.json"))
    assert not list(ROOT.rglob("__pycache__"))
    compiled = []
    for path in sorted(ROOT.glob("*.py")):
        compile(path.read_bytes(), str(path), "exec")
        compiled.append(path.name)
    source_paths = [ROOT / "RESULTS.md", ROOT / "RESUME.md", ROOT / "03-normalized-static-collective-operator.md",
                    previous_path, PREVIOUS / "02-full-tensor-response-and-collective-kernel.md"]
    assert all(path.is_file() for path in source_paths)
    urls = ["https://arxiv.org/abs/1310.3295", "https://doi.org/10.1103/PhysRevD.88.085024", "https://doi.org/10.1103/PhysRevD.109.096024"]
    document = (ROOT / "03-normalized-static-collective-operator.md").read_text(encoding="utf-8")
    assert all(url in document for url in urls)
    protected = POST.parent / "formalization-workbench"
    assert protected.is_dir()
    start = datetime(2026, 10, 3, 14, 34, 22, tzinfo=timezone.utc)
    recent = [str(path) for path in protected.rglob("*") if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert not recent, recent
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob("*")) if path.is_file() and path != OUTPUT}
    report = {
        "state": "complete", "sealed_at": datetime.now(timezone.utc).isoformat(), "file_hashes": hashes,
        "previous_seal_sha256": digest(previous_path), "previous_files_reverified": len(previous["file_hashes"]),
        "older_sealed_files_reverified": len(older["file_hashes"]), "checkpoint_manifest_sha256": digest(manifest),
        "full_checkpoint_payload_rehashed": False,
        "exact_identities": 24, "normalization_numerical_checks": 116,
        "supplementary_strict_relative_accuracy_checks": accuracy,
        "saved_matrix_replays": replay, "matrix_runs": 16, "self_cell_fixtures": 2,
        "fixed_ir_cutoff_relative_change": cutoff_change, "infrared_grid_relative_change": infrared_change,
        "cell_quadrature_relative_change": quadrature_change,
        "finest_maximum_real_eigenvalue": refinement["rows"][-1]["largest_positive_eigenvalue"],
        "finest_positive_weight_comparison_bound": refinement["rows"][-1]["positive_weight_comparison_bound"],
        "compiled_scripts": compiled, "required_local_paths": [str(path) for path in source_paths], "web_sources": urls,
        "protected_workbench_recent_modified_file_count": len(recent),
        "protected_check_scope": "Modification-time scan since turn start, not a full content-hash baseline.",
        "scope": "Chosen weak point, bare leading cubic-exchange static pair operator; finite numerical matrices.",
        "continuum_operator_theorem": False, "finite_frequency_pole_search": False,
        "symmetry_preserving_dressed_truncation_implemented": False,
        "github_action": False, "subagents": 0, "candidate_adopted_into_original_framework": False
    }
    OUTPUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", "exact_identities": 24, "normalization_checks": 116,
                      "strict_relative_checks": len(accuracy), "matrix_replays": len(replay),
                      "scripts_compiled": len(compiled), "protected_changes": len(recent),
                      "cutoff_change": cutoff_change, "infrared_change": infrared_change,
                      "quadrature_change": quadrature_change}))


if __name__ == "__main__":
    main()
