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
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate key: {key}")
            result[key] = value
        return result

    def invalid(value):
        raise ValueError(f"Invalid JSON constant: {value}")

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique, parse_constant=invalid)


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to overwrite sealed evidence.")
    stages = ["ward-remainder-20261003", "tensor-ward-20261003",
              "collective-operator-20261003", "tensor-response-20261003"]
    paths = [BRANCH / stage / "results/stage-integrity.json" for stage in stages]
    paths.append(BRANCH / "results/stage-integrity.json")
    bases = [BRANCH / stage for stage in stages] + [POST]
    chain_keys = ["parent_seal_sha256", "previous_seal_sha256", "previous_seal_sha256", "parent_seal_sha256"]
    previous_reports = []
    for path, base in zip(paths, bases):
        report = read_json(path)
        assert report["state"] == "complete"
        for relative, expected in report["file_hashes"].items():
            source = base / relative
            assert source.is_file() and digest(source) == expected, str(source)
        previous_reports.append(report)
    for index, key in enumerate(chain_keys):
        assert previous_reports[index][key] == digest(paths[index + 1])
    manifest = POST / "_checkpoints/20261003-pre-condensate-origin/manifest.json"
    assert digest(manifest) == previous_reports[0]["checkpoint_manifest_sha256"]

    derived_path = ROOT / "results/derivation/status.json"
    derived = read_json(derived_path)
    curved = read_json(ROOT / "results/curved-validation/status.json")
    coexistence = read_json(ROOT / "results/charge-coexistence/status.json")
    assert all(report["state"] == "complete" for report in [derived, curved, coexistence])
    assert derived["parent_seal_sha256"] == digest(paths[0])
    assert curved["derivation_sha256"] == coexistence["derivation_sha256"] == digest(derived_path)
    assert derived["exact_check_count"] == len(derived["checks"]) == 16
    assert coexistence["exact_check_count"] == len(coexistence["checks"]) == 7
    assert all(row["passed"] for row in derived["checks"] + coexistence["checks"])
    assert len(curved["curved_off_shell_Noether_fixtures"]) == 2
    assert curved["finite_action_variation_count"] == len(curved["finite_action_variations"]) == 14
    assert all(row["passed"] for row in curved["finite_action_variations"])
    assert sum(row["kind"] == "inverse_metric" for row in curved["finite_action_variations"]) == 10
    assert sum(row["kind"] == "phase" for row in curved["finite_action_variations"]) == 1
    assert sum(row["kind"] == "parent_density_metric" for row in curved["finite_action_variations"]) == 3
    for row in curved["curved_off_shell_Noether_fixtures"]:
        assert row["relative_error"] < 1e-8
        assert row["omitted_Q_terms_negative_control_error"] > 1000 * row["absolute_error"]
    estimates = coexistence["quadrature_estimates"]
    assert len(estimates) == 2
    assert [row["digits"] for row in estimates] == [50, 80]
    assert all(float(row["independent_variable_quadrature_relative_error"]) < 1e-40 for row in estimates)
    last = estimates[-1]
    coupling = 10**(2 / 3) / 3
    quartic = 1 / 150
    amplitude = (coupling / quartic)**(3 / 8)
    chemical = math.sqrt(2 * coupling * amplitude**(-2 / 3))
    charge = chemical * amplitude**2
    assert math.isclose(amplitude, float(last["critical_amplitude"]), rel_tol=1e-13)
    assert math.isclose(chemical, float(last["critical_chemical_potential"]), rel_tol=1e-13)
    assert math.isclose(charge, float(last["critical_charge_density"]), rel_tol=1e-13)
    assert math.isclose((100 / charge)**(1 / 3), derived["homogeneous_example"]["a_at_y1_from_y2_a1"], rel_tol=1e-13)
    assert math.isclose(float(last["critical_bulk_energy_density"]), chemical * charge, rel_tol=1e-13)

    source_map = []
    source_specifications = [
        ("4876", "Integrated-H gravitational saddle and retained renormalized normalization",
         [r"M_R^2\widehat G_{\mu\nu}", r"C_{0,R}"]),
        ("4916", "Local metric map, Hilbert source chain and non-unique covariantization boundary",
         [r"\mathcal H^{\mu\nu}=\sqrt{-g}", "not uniquely forced", r"S_{\psi X}"]),
        ("4960", "Declared independent-H/Diff parent and source normalization boundary",
         ["integrated nondegenerate Lorentzian H", "R4(T)", "one positive massless spin-2 pole"]),
    ]
    for prefix, role, anchors in source_specifications:
        matches = list(POST.glob(f"{prefix}-*.md"))
        assert len(matches) == 1
        path = matches[0]
        lines = path.read_text(encoding="utf-8").splitlines()
        text = "\n".join(lines)
        assert all(anchor in text for anchor in anchors), (prefix, anchors)
        source_map.append({"checkpoint": prefix, "role": role, "path": str(path.resolve()), "sha256": digest(path),
                           "anchor_lines": [{"text": anchor, "line": next(index + 1 for index, line in enumerate(lines) if anchor in line)}
                                            for anchor in anchors],
                           "all_historical_claims_reproved_this_turn": False})

    required = [
        ROOT / "06-conserved-stress-and-parent-source.md",
        ROOT / "07-fixed-charge-bulk-continuation.md",
        ROOT / "RESULTS.md", ROOT / "RESUME.md",
        BRANCH / "ward-remainder-20261003/05-Ward-remainder-and-derivative-interaction-bound.md",
        derived_path, ROOT / "results/curved-validation/status.json", ROOT / "results/charge-coexistence/status.json",
        manifest, *paths, *[Path(row["path"]) for row in source_map],
    ]
    assert all(path.is_file() for path in required)
    sources = ["https://arxiv.org/abs/1710.01562", "https://arxiv.org/abs/1709.09695",
               "https://doi.org/10.1016/0550-3213(85)90286-X"]
    prose = "\n".join(path.read_text(encoding="utf-8") for path in ROOT.glob("*.md"))
    assert all(url in prose for url in sources)
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
    protected = POST.parent / "formalization-workbench"
    start = datetime(2026, 10, 3, 16, 31, 57, tzinfo=timezone.utc)
    assert protected.is_dir()
    changed = [str(path) for path in protected.rglob("*")
               if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob("*"))
              if path.is_file() and path != OUTPUT}
    report = {
        "state": "complete", "sealed_at": datetime.now(timezone.utc).isoformat(), "file_hashes": hashes,
        "parent_seal_sha256": digest(paths[0]), "prior_sealed_entries_unchanged": sum(len(row["file_hashes"]) for row in previous_reports),
        "checkpoint_manifest_sha256": digest(manifest), "full_checkpoint_payload_rehashed": False,
        "exact_check_count": 23, "curved_identity_fixture_count": 2, "finite_action_variation_count": 14,
        "surface_tension_quadrature_precisions": [50, 80], "independent_coefficient_replay": True,
        "parent_source_map": source_map, "required_local_paths": [str(path.resolve()) for path in required],
        "web_context_sources": sources, "compiled_scripts": compiled, "parsed_json_files": parsed,
        "protected_workbench_recent_modified_file_count": len(changed),
        "protected_check_scope": "Modification-time scan since turn start; not a full content-hash baseline.",
        "closed_candidate_current_and_stress_derived": True,
        "offshell_Noether_identity_proved_for_displayed_action": True,
        "parent_H_source_chain_checked": True,
        "original_parent_replaced_or_modified": False,
        "full_original_bath_embedding_completed": False,
        "quadratic_order_reduction_checked": True,
        "general_nonlinear_order_reduction_completed": False,
        "nongravitating_bulk_coexistence_energy_bound_proved": True,
        "finite_charge_profile_solved": False, "cosmological_formation_predicted": False,
        "github_action": False, "subagents": 0,
    }
    OUTPUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", "sealed_files": len(hashes), "previous_unchanged": report["prior_sealed_entries_unchanged"],
                      "exact_checks": 23, "curved_checks": 2, "action_variations": 14,
                      "source_documents": len(source_map), "scripts_compiled": len(compiled), "protected_changes": len(changed)}))


if __name__ == "__main__":
    main()

