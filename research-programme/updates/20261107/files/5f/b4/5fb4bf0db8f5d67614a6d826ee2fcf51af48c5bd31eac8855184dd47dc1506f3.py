import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
import run_temperature_validation
from hybrid_reference_common import *
import stage168_common as parent_module


def main():
    modest()
    folder = ROOT / "results/validation-final"
    folder.mkdir(parents=True, exist_ok=False)
    checks, hashes, packets, retained = [], {}, {}, []
    expected_failed = {"results/comparison": 6, "results/legacy-replay/heavy-m20": 1, "results/validation": 60}
    for path in sorted(ROOT.rglob("status.json")):
        if path.parent == folder:
            continue
        packet = json.loads(path.read_text())
        assert packet["state"] == "complete" and (path.parent / "COMPLETE").exists()
        label = path.parent.relative_to(ROOT).as_posix()
        failures = [dict(row, packet=str(path)) for row in packet["checks"] if not row["passed"]]
        assert len(failures) == expected_failed.get(label, 0), (label, failures)
        retained.extend(failures)
        retained.extend(dict(row, packet=str(path)) for row in packet.get("retained_failed_checks", []))
        for filename, checksum in packet["input_hashes"].items():
            assert filename not in hashes or hashes[filename] == checksum, filename
            hashes[filename] = checksum
        checks.append(dict(name="Packet scope and retained failures:" + label, passed=True))
        packets[label] = packet
    for filename, checksum in hashes.items():
        assert digest(filename) == checksum, filename
    checks.append(dict(name="Every unique consumed file hash", count=len(hashes), passed=True))
    comparison = packets["results/comparison-hybrid"]
    equations = packets["results/original-step-audit"]
    assert comparison["all_checks_passed"] and equations["all_checks_passed"]
    assert equations["sampled_one_step_check_only"] and not equations["saved_forecast_changed"]
    old = packets["results/validation"]
    assert sum(not row["passed"] for row in old["checks"]) == 60
    checks.extend(dict(row, name="Retained successful independent audit:" + row["name"]) for row in old["checks"] if row["passed"])
    checks.extend(dict(row, name="Direct original-variable sample:" + row["name"]) for row in equations["checks"])
    parent = json.loads((PARENT / "results/stage-integrity.json").read_text())
    assert digest(PARENT / "results/stage-integrity.json") == PARENT_SEAL
    chain = {PARENT / "results/stage-integrity.json": parent, **parent_module.ancestors()}
    paths = {PARENT / name for name in parent["file_hashes"]}
    paths.update(Path(filename) for filename in hashes if not Path(filename).is_relative_to(ROOT))
    authenticated = authenticate(paths, chain)
    checks.append(dict(name="Immediate parent and consumed ancestry authenticated", count=len(authenticated), passed=True))
    scripts = list(ROOT.glob("*.py"))
    for path in scripts:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    assert not list(ROOT.rglob("__pycache__"))
    checks.append(dict(name="Every script compiles without cache", count=len(scripts), passed=True))
    protected = POST.parent / "formalization-workbench"
    changed = [str(path) for path in protected.rglob("*") if path.is_file() and path.stat().st_mtime > STARTED.timestamp()]
    checks.append(dict(name="Protected workbench mtime guard", count=len(changed), passed=not changed))
    report = finish(folder, checks, [*map(Path, hashes), *[ROOT / name / "status.json" for name in packets]],
                    consumed_and_immediate_rehashed=authenticated, rehashed_prior_files=len(authenticated),
                    compiled_scripts=len(scripts), retained_failed_checks=retained,
                    failed_reconstruction_checks_retained=60, original_equations_passed_in_direct_sample=True,
                    original_equations_verified_at_every_step=False,
                    accepted_scope="Conditional forecast agreement plus directly solved high-precision original-variable sample; not certification of float derivative reconstruction or every step.",
                    conditional_resolved_prediction_only=True, microscopic_source_prediction_complete=False,
                    unresolved_carrier_forecast=False, raw_source_failures_inherited=40,
                    protected_check_scope="Mtime guard since 17:20:03 UTC, not a pre-turn content snapshot")
    print(json.dumps(dict(count=report["count"], all_passed=report["all_checks_passed"],
                          scripts=len(scripts), prior_files=len(authenticated), retained_failure_records=len(retained))), flush=True)


if __name__ == "__main__":
    main()
