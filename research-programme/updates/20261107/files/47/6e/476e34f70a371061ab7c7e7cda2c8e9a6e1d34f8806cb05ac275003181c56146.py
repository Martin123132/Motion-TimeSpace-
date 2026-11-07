from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import psutil
from scipy.linalg import eigvals


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
PREVIOUS = BRANCH / "collective-operator-20261003"
OUTPUT = ROOT / "results/stage-integrity.json"


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"Non-finite JSON value: {value}")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def verify_seal(path, base):
    report = read_json(path)
    assert report["state"] == "complete"
    for relative, expected in report["file_hashes"].items():
        source = base / relative
        assert source.is_file() and digest(source) == expected, str(source)
    return report


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to overwrite a sealed stage.")
    previous_path = PREVIOUS / "results/stage-integrity.json"
    previous = verify_seal(previous_path, PREVIOUS)
    tensor_path = BRANCH / "tensor-response-20261003/results/stage-integrity.json"
    assert digest(tensor_path) == previous["previous_seal_sha256"]
    tensor = verify_seal(tensor_path, tensor_path.parent.parent)
    origin_path = BRANCH / "results/stage-integrity.json"
    assert digest(origin_path) == tensor["parent_seal_sha256"]
    origin = verify_seal(origin_path, POST)
    manifest = POST / "_checkpoints/20261003-pre-condensate-origin/manifest.json"
    assert digest(manifest) == previous["checkpoint_manifest_sha256"]

    parsed = [path.relative_to(ROOT).as_posix() for path in sorted(ROOT.rglob("*.json"))
              if read_json(path) is not None]
    algebra = read_json(ROOT / "results/algebra/status.json")
    ward = read_json(ROOT / "results/ward-validation/status.json")
    operator = read_json(ROOT / "results/regulated-operator/status.json")
    soft = read_json(ROOT / "results/soft-response/status.json")
    assert all(report["state"] == "complete" for report in [algebra, ward, operator, soft])
    assert algebra["exact_checks"] == len(algebra["checks"]) == 19
    assert soft["exact_check_count"] == len(soft["exact_checks"]) == 12
    assert ward["checks_passed"] == len(ward["checks"]) == 56
    assert len(operator["projection_checks"]) == 12
    assert all(check["passed"] for check in algebra["checks"] + soft["exact_checks"]
               + ward["checks"] + operator["projection_checks"])
    assert algebra["parent_sha256"] == digest(previous_path)
    assert ward["core_sha256"] == digest(ROOT / "ward_core.py")
    assert ward["algebra_sha256"] == digest(ROOT / "results/algebra/status.json")
    assert operator["parent_sha256"] == digest(previous_path)
    assert operator["operator_sha256"] == digest(ROOT / "regulated_operator.py")
    assert operator["ward_core_sha256"] == digest(ROOT / "ward_core.py")
    assert operator["bare_replay_error"] < 1e-16

    source_rows = operator["rows"]
    assert len(source_rows) == 5
    replay_rows = []
    for row in source_rows:
        folder = ROOT / "results/regulated-operator" / row["name"]
        assert read_json(folder / "status.json") == row
        matrix = np.load(folder / "operator.npy", allow_pickle=False)
        saved = np.load(folder / "diagnostics.npz", allow_pickle=False)
        assert matrix.shape == (row["matrix_dimension"], row["matrix_dimension"])
        assert np.isfinite(matrix).all()
        centers = saved["centers"]
        frequency, momentum = np.meshgrid(centers, centers, indexing="ij")
        soft_squared = momentum**2 + frequency**2 / (5 / 23)
        weights = np.stack([1 + 1 / soft_squared, np.ones_like(soft_squared),
                            1 + 1 / np.sqrt(soft_squared), 1 + 1 / np.sqrt(soft_squared)], axis=-1).ravel()
        assert np.array_equal(weights, saved["soft_weights"])
        bound = float(np.max((np.abs(matrix) @ weights) / weights))
        assert abs(bound - row["analytic_soft_weight_matrix_bound"]) < 1e-15
        source = np.tile([1., 1., 0., 0.], len(matrix) // 4)
        assert np.array_equal(source, saved["source"])
        response = matrix @ source
        assert np.max(np.abs(response - saved["first_rung"])) < 1e-15
        assert np.max(np.abs(response[:4] - np.asarray(row["first_rung_at_lowest_node"]))) < 1e-15
        eigenvalues = eigvals(matrix)
        radius = float(np.max(np.abs(eigenvalues)))
        maximum_real = float(np.max(eigenvalues.real))
        assert abs(radius - row["spectral_radius"]) < 1e-15
        assert abs(maximum_real - row["largest_positive_eigenvalue"]) < 1e-15
        assert abs(float(np.max(np.abs(saved["eigenvalues"]))) - radius) < 1e-15
        assert radius < bound < 1
        prediction = soft["infrared_coefficient"] / float(soft_squared[0, 0])
        assert abs(prediction - row["parameter_free_radial_soft_prediction"]) < 1e-15
        assert abs(response[0] / prediction - row["radial_soft_ratio"]) < 1e-13
        replay_rows.append({"name": row["name"], "independently_recomputed_spectral_radius": radius,
                            "maximum_real_eigenvalue": maximum_real, "soft_weight_bound": bound,
                            "source_first_rung_replayed": True, "passed": True})

    parent_report_path = PREVIOUS / "results/fixed-infrared-refinement/status.json"
    assert digest(parent_report_path) == soft["parent_report_sha256"]
    assert len(soft["parent_rows"]) == 5
    parent_replays = []
    for row in soft["parent_rows"]:
        folder = PREVIOUS / "results/fixed-infrared-refinement" / row["name"]
        assert digest(folder / "operator.npy") == row["parent_matrix_sha256"]
        matrix = np.load(folder / "operator.npy", allow_pickle=False)
        saved = np.load(folder / "diagnostics.npz", allow_pickle=False)
        centers = saved["centers"]
        frequency, momentum = np.meshgrid(centers, centers, indexing="ij")
        soft_squared = momentum**2 + frequency**2 / (5 / 23)
        weights = np.stack([1 + 1 / soft_squared, np.ones_like(soft_squared),
                            1 + 1 / np.sqrt(soft_squared), 1 + 1 / np.sqrt(soft_squared)], axis=-1).ravel()
        bound = float(np.max((np.abs(matrix) @ weights) / weights))
        assert abs(bound - row["analytic_weight_matrix_bound"]) < 1e-15
        response = matrix @ np.tile([1., 1., 0., 0.], len(matrix) // 4)
        prediction = soft["infrared_coefficient"] / float(soft_squared[0, 0])
        mixed_prediction = -math.sqrt(2) * 2 / (10 / 9) * centers[0] * prediction
        assert abs(response[0] / prediction - row["radial_ratio"]) < 1e-13
        assert abs(response[3] / mixed_prediction - row["antisymmetric_ratio"]) < 1e-13
        parent_replays.append({"name": row["name"], "weighted_bound": bound,
                               "radial_ratio": row["radial_ratio"],
                               "mixed_ratio": row["antisymmetric_ratio"], "passed": True})

    assert len(ward["hard_boundary_fixtures"]) == 9
    assert len(ward["infinite_spatial_paired_fixtures"]) == 4
    assert len(ward["metric_variations"]) == 4
    assert len(ward["tadpole_rows"]) == 3
    for row in ward["hard_boundary_fixtures"]:
        direct = np.asarray(row["direct_spatial_derivative"])
        first = np.asarray(row["first_leg_half"])
        second = np.asarray(row["second_leg_half"])
        boundary = np.asarray(row["boundary"])
        error = float(np.max(np.abs(direct - first - second - boundary)))
        assert error < 1e-12
        assert row["omitted_surface_error"] > 100 * error + 1e-14
    for row in ward["tadpole_rows"]:
        fine = row["orders"]["96"]
        assert abs(fine["phase_self_energy"] - fine["tadpole"] / 10) < 1e-14
        assert abs(fine["background_shift"] + fine["tadpole"] / (10 / 9)) < 1e-14
        assert abs(fine["phase_self_energy"] + fine["background_shift"] / 9) < 2e-14

    compiled = []
    for path in sorted(ROOT.glob("*.py")):
        compile(path.read_bytes(), str(path), "exec")
        compiled.append(path.name)
    assert not list(ROOT.rglob("__pycache__"))
    assert not list(ROOT.rglob("FAILED.json"))
    source_paths = [
        ROOT / "04-tensor-Ward-identity-and-soft-response.md", ROOT / "RESULTS.md", ROOT / "RESUME.md",
        BRANCH / "01-first-condensate-derivation.md",
        BRANCH / "tensor-response-20261003/02-full-tensor-response-and-collective-kernel.md",
        PREVIOUS / "03-normalized-static-collective-operator.md",
        previous_path, tensor_path, origin_path, manifest,
        ROOT / "results/algebra/status.json", ROOT / "results/ward-validation/status.json",
        ROOT / "results/regulated-operator/status.json", ROOT / "results/soft-response/status.json",
    ]
    assert all(path.is_file() for path in source_paths)
    urls = ["https://arxiv.org/abs/1108.5207", "https://arxiv.org/abs/1011.3324"]
    document = (ROOT / "04-tensor-Ward-identity-and-soft-response.md").read_text(encoding="utf-8")
    assert all(url in document for url in urls)
    protected = POST.parent / "formalization-workbench"
    assert protected.is_dir()
    started = datetime(2026, 10, 3, 15, 5, 9, tzinfo=timezone.utc)
    recent = [str(path) for path in protected.rglob("*")
              if path.is_file() and path.stat().st_mtime > started.timestamp()]
    assert not recent, recent
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob("*"))
              if path.is_file() and path != OUTPUT}
    report = {
        "state": "complete", "sealed_at": datetime.now(timezone.utc).isoformat(), "file_hashes": hashes,
        "previous_seal_sha256": digest(previous_path),
        "previous_files_reverified": len(previous["file_hashes"]),
        "tensor_stage_files_reverified": len(tensor["file_hashes"]),
        "origin_stage_files_reverified": len(origin["file_hashes"]),
        "checkpoint_manifest_sha256": digest(manifest), "full_checkpoint_payload_rehashed": False,
        "exact_identity_count": 31, "Ward_numerical_check_count": 56, "angular_high_precision_count": 12,
        "parsed_json_files": parsed, "compiled_scripts": compiled,
        "new_matrix_replays": replay_rows, "parent_matrix_replays": parent_replays,
        "regulator_relative_change_matched_mesh": source_rows[1]["largest_positive_eigenvalue"] / source_rows[0]["largest_positive_eigenvalue"] - 1,
        "quadrature_relative_change": source_rows[2]["largest_positive_eigenvalue"] / source_rows[1]["largest_positive_eigenvalue"] - 1,
        "infrared_refinement_relative_change": source_rows[3]["largest_positive_eigenvalue"] / source_rows[2]["largest_positive_eigenvalue"] - 1,
        "box_extension_relative_change_fixed_ir": source_rows[4]["largest_positive_eigenvalue"] / source_rows[1]["largest_positive_eigenvalue"] - 1,
        "required_local_paths": [str(path.resolve()) for path in source_paths], "web_context_sources": urls,
        "protected_workbench_recent_modified_file_count": len(recent),
        "protected_check_scope": "Modification-time scan since turn start, not a full content-hash baseline.",
        "soft_cancellation_scope": "Specific leading nonanalytic propagated shear insertion, not full response.",
        "operator_scope": "Regulator/source-completed bare static cubic ladder at the selected weak point.",
        "continuum_operator_norm_theorem": False, "full_dressed_symmetry_consistency_proved": False,
        "regulator_removal_and_renormalized_parameter_matching_performed": False,
        "new_regulator_adopted_as_physical_term": False, "new_tensor_mode_claimed": False,
        "github_action": False, "subagents": 0, "new_science_outside_isolated_branch": False,
    }
    OUTPUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", "sealed_files": len(hashes), "exact_identities": 31,
                      "Ward_checks": 56, "angular_checks": 12, "new_matrices_replayed": len(replay_rows),
                      "old_matrices_replayed": len(parent_replays), "scripts_compiled": len(compiled),
                      "previous_files_unchanged": sum(len(item["file_hashes"]) for item in [previous, tensor, origin]),
                      "protected_recent_changes": len(recent)}))


if __name__ == "__main__":
    main()

