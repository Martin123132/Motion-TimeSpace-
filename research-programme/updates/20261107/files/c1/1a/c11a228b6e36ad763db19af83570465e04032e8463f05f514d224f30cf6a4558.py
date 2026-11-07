from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

import psutil


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
OUTPUT = ROOT / "results/stage-integrity.json"


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate key: {key}")
            result[key] = value
        return result

    def invalid(value):
        raise ValueError(f"Nonfinite JSON value: {value}")

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique, parse_constant=invalid)


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to overwrite a completed seal.")
    seals = [
        (BRANCH / "tensor-ward-20261003/results/stage-integrity.json", BRANCH / "tensor-ward-20261003"),
        (BRANCH / "collective-operator-20261003/results/stage-integrity.json", BRANCH / "collective-operator-20261003"),
        (BRANCH / "tensor-response-20261003/results/stage-integrity.json", BRANCH / "tensor-response-20261003"),
        (BRANCH / "results/stage-integrity.json", POST),
    ]
    prior = []
    for path, base in seals:
        report = read_json(path)
        assert report["state"] == "complete"
        for relative, expected in report["file_hashes"].items():
            source = base / relative
            assert source.is_file() and digest(source) == expected, str(source)
        prior.append(report)
    assert prior[0]["previous_seal_sha256"] == digest(seals[1][0])
    assert prior[1]["previous_seal_sha256"] == digest(seals[2][0])
    assert prior[2]["parent_seal_sha256"] == digest(seals[3][0])
    manifest = POST / "_checkpoints/20261003-pre-condensate-origin/manifest.json"
    assert digest(manifest) == prior[0]["checkpoint_manifest_sha256"]

    derived = read_json(ROOT / "results/derivation/status.json")
    validation = read_json(ROOT / "results/validation/status.json")
    assert derived["state"] == validation["state"] == "complete"
    assert derived["parent_seal_sha256"] == digest(seals[0][0])
    assert validation["derivation_sha256"] == digest(ROOT / "results/derivation/status.json")
    assert derived["exact_check_count"] == len(derived["checks"]) == 23
    assert validation["exact_check_count"] == len(validation["exact_checks"]) == 8
    assert validation["kernel_check_count"] == len(validation["kernel_checks"]) == 96
    assert validation["vertex_fixture_count"] == len(validation["vertex_fixtures"]) == 256
    assert all(row["passed"] for group in [derived["checks"], validation["exact_checks"],
                                         validation["kernel_checks"], validation["vertex_fixtures"]] for row in group)
    pressure = [100., 360., -1728 / 5, 487296 / 125]
    kinetic = pressure[0] + pressure[1]
    sound = math.sqrt(pressure[0] / kinetic)
    coefficients = {
        "cubic_time": (pressure[1] / 2 + pressure[2] / 6) / kinetic**1.5,
        "cubic_mixed": -pressure[1] / (2 * kinetic**1.5),
        "quartic_time": (pressure[1] / 8 + pressure[2] / 4 + pressure[3] / 24) / kinetic**2,
        "quartic_mixed": -(pressure[1] + pressure[2]) / (4 * kinetic**2),
        "quartic_spatial": pressure[1] / (8 * kinetic**2),
    }
    for key, value in coefficients.items():
        assert math.isclose(value, derived["canonical_coefficients"][key]["numeric"], rel_tol=1e-13)
    cubic_bound = 6 * (abs(coefficients["cubic_time"]) * sound**3 + abs(coefficients["cubic_mixed"]) * sound)
    quartic_bound = 24 * (abs(coefficients["quartic_time"]) * sound**4
                          + abs(coefficients["quartic_mixed"]) * sound**2
                          + abs(coefficients["quartic_spatial"]))
    tree_bound = quartic_bound + 3 * cubic_bound**2 / sound**2
    norm_prefactor = tree_bound / (64 * math.pi**2 * sound**3)
    for key, value in [("C3", cubic_bound), ("C4", quartic_bound), ("C_tree", tree_bound), ("norm_prefactor", norm_prefactor)]:
        assert math.isclose(value, derived["vertex_bounds"][key], rel_tol=1e-13)
    cutoffs = []
    for row in derived["cutoff_rows"]:
        cutoff = row["acoustic_cutoff_over_mu"]
        expected = norm_prefactor * cutoff**4
        assert math.isclose(row["leading_tree_EFT_continuum_norm_bound"], expected, rel_tol=1e-13)
        assert expected < 1
        cutoffs.append({**row, "maximum_exchanged_momentum_expansion_ratio": 4 * cutoff**2 / (10 / 9)})
    infrared = (1 / 9)**2 * sound / (32 * math.pi**2)
    assert math.isclose(2 * infrared**2 / (3 * (10 / 9)**2),
                        derived["isolated_second_rung_phase_log_coefficient"], rel_tol=1e-13)
    for key in ["cubic", "quartic", "tree"]:
        maximum = max(row[f"{key}_ratio"] for row in validation["vertex_fixtures"])
        assert math.isclose(maximum, validation[f"maximum_{key}_bound_ratio"], rel_tol=1e-13)
        assert maximum < 1
    source = validation["source_and_NLO_coefficients"]
    assert math.isclose(source["quadratic_gradient_shear"], sound**2, rel_tol=1e-13)
    assert math.isclose(source["cubic_time_gradient_shear"], pressure[1] / kinetic**1.5, rel_tol=1e-13)
    assert math.isclose(source["quartic_time_squared_gradient_shear"], (pressure[1] + pressure[2]) / (2 * kinetic**2), rel_tol=1e-13)
    assert math.isclose(source["quartic_gradient_squared_gradient_shear"], -pressure[1] / (2 * kinetic**2), rel_tol=1e-13)
    assert math.isclose(2 * source["NLO_quadratic_canonical_beta"] * sound**2 * (1 - sound**2),
                        source["NLO_k4_coefficient"], rel_tol=1e-13)
    parsed = []
    for path in sorted(ROOT.rglob("*.json")):
        read_json(path)
        parsed.append(path.relative_to(ROOT).as_posix())
    compiled = []
    for path in sorted(ROOT.glob("*.py")):
        compile(path.read_bytes(), str(path), "exec")
        compiled.append(path.name)
    assert not list(ROOT.rglob("__pycache__"))
    assert not list(ROOT.rglob("FAILED.json"))
    source_paths = [ROOT / "RESULTS.md", ROOT / "RESUME.md",
                    ROOT / "05-Ward-remainder-and-derivative-interaction-bound.md",
                    BRANCH / "01-first-condensate-derivation.md",
                    BRANCH / "tensor-response-20261003/02-full-tensor-response-and-collective-kernel.md",
                    BRANCH / "collective-operator-20261003/03-normalized-static-collective-operator.md",
                    BRANCH / "tensor-ward-20261003/04-tensor-Ward-identity-and-soft-response.md",
                    ROOT / "results/derivation/status.json", ROOT / "results/validation/status.json",
                    manifest, *[pair[0] for pair in seals]]
    assert all(path.is_file() for path in source_paths)
    urls = ["https://arxiv.org/abs/hep-ph/0204199", "https://arxiv.org/abs/1011.3324"]
    document = (ROOT / "05-Ward-remainder-and-derivative-interaction-bound.md").read_text(encoding="utf-8")
    assert all(url in document for url in urls)
    protected = POST.parent / "formalization-workbench"
    started = datetime(2026, 10, 3, 15, 47, 41, tzinfo=timezone.utc)
    assert protected.is_dir()
    modified = [str(path) for path in protected.rglob("*")
                if path.is_file() and path.stat().st_mtime > started.timestamp()]
    assert not modified, modified
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob("*"))
              if path.is_file() and path != OUTPUT}
    report = {
        "state": "complete", "sealed_at": datetime.now(timezone.utc).isoformat(), "file_hashes": hashes,
        "parent_seal_sha256": digest(seals[0][0]),
        "prior_stages_reverified": [{"path": str(path), "file_count": len(report["file_hashes"])}
                                    for (path, _), report in zip(seals, prior)],
        "prior_sealed_file_count_unchanged": sum(len(report["file_hashes"]) for report in prior),
        "checkpoint_manifest_sha256": digest(manifest), "full_checkpoint_payload_rehashed": False,
        "exact_check_count": 31, "transformed_kernel_check_count": 96, "vertex_fixture_count": 256,
        "independent_coefficient_replay": True, "compiled_scripts": compiled, "parsed_json_files": parsed,
        "cutoff_rows_with_exchange_domain": cutoffs,
        "required_local_paths": [str(path.resolve()) for path in source_paths], "web_sources": urls,
        "protected_workbench_recent_modified_file_count": len(modified),
        "protected_check_scope": "Modification-time scan since turn start, not a full content-hash baseline.",
        "leading_tree_phase_EFT_continuum_bound_proved": True,
        "proof_scope": derived["continuum_bound_scope"],
        "full_microscopic_continuum_bound_proved": False,
        "complete_two_loop_log_cancellation_proved": False,
        "new_tensor_mode_claimed": False, "independent_metric_dynamics_derived": False,
        "NLO_dispersion_matching_checked": True, "full_NLO_stress_variation_completed": False,
        "github_action": False, "subagents": 0,
    }
    OUTPUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", "sealed_files": len(hashes), "exact_checks": 31,
                      "kernel_checks": 96, "vertex_fixtures": 256,
                      "previous_unchanged": report["prior_sealed_file_count_unchanged"],
                      "compiled": len(compiled), "protected_changes": len(modified),
                      "conservative_domain_bound": cutoffs[0]["leading_tree_EFT_continuum_norm_bound"]}))


if __name__ == "__main__":
    main()

