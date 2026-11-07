import csv
import math
from common import ROOT, POST, PARENT, PARENT_SEAL, ALGEBRA, GATE, modest, guard, digest, read, write, require

OUTPUT = ROOT / "verified"


def main():
    modest()
    result = read(OUTPUT / "result.json")
    checks = {}

    def check(name, passed):
        checks[name] = bool(passed)
        require(passed, name)

    check("completed source test", result["state"] == "complete" and result["passed"])
    check("42 reused histories, no new integration", result["reused_histories"] == 42 and result["new_evolutions"] == 0)
    check("unchanged tolerances", result["algebra_gate"] == ALGEBRA and result["numerical_gate"] == GATE)
    check("limited action claim", result["scalar_action_pullback_verified"] and not result["full_truncated_covariant_action_claimed"])
    check("parent seal", digest(PARENT / "closeout.json") == PARENT_SEAL == result["parent_closeout_sha256"])
    for path, checksum in result["source_hashes"].items():
        check("source:" + path, digest(path) == checksum)
    compiled = {}
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        compiled[str(path)] = digest(path)
    check("no bytecode", not list(ROOT.rglob("__pycache__")))
    parent = read(PARENT / "prediction-result.json")
    expected = {(family["model"] + "-" + family["label"], case["tag"]): case["sha256"]
                for family in parent["reports"] for case in family["cases"]}
    seen = set()
    for record in result["records"]:
        guard()
        key = (record["family"], record["tag"])
        check("unique:" + str(key), key not in seen)
        seen.add(key)
        check("owned packet:" + str(key), digest(record["packet"]) == record["sha256"] == expected[key])
        saved = read(OUTPUT / (record["family"] + "-" + record["tag"] + ".json"))
        check("separate record:" + str(key), saved == record and record["passed"])
        for name, value in record["checks"].items():
            check(str(key) + ":" + name, math.isfinite(value) and 0 <= value < ALGEBRA)
        if record["family"].startswith("heavy-"):
            check("positive two-form:" + str(key), record["diagnostics"]["area_min"] > 0)
            check("finite area:" + str(key), math.isfinite(record["diagnostics"]["area_max"]))
            if "-full-" in record["tag"] or "-zero" in record["tag"]:
                check("no invented exact-flow defect:" + str(key),
                      record["diagnostics"]["coordinate_Euler_residual_over_parent_rate"] == 0
                      and record["diagnostics"]["covariant_truncation_density_over_density"] == 0)
        if record["tag"].endswith("-zero"):
            check("zero sources:" + str(key), record["checks"]["zero_source"] == 0)
    check("full expected coverage", seen == set(expected))
    symbolic = read(OUTPUT / "symbolic-result.json")
    check("symbolic derivation", symbolic["passed"] and all(symbolic["identities"].values())
          and len(symbolic["identities"]) == result["symbolic_identity_count"] == 16)
    with (OUTPUT / "summary.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    check("CSV shape", len(rows) == 42 and all(None not in row and None not in row.values() for row in rows))
    check("CSV coverage", {(row["family"], row["case"]) for row in rows} == seen)
    for row in rows:
        check("CSV numeric:" + row["family"] + row["case"],
              all(math.isfinite(float(value)) for name, value in row.items() if name not in ("family", "case")))
    authorities = [
        POST / "condensate-origin-20261003/native-two-field-transfer-20261007/54-native-canonical-fields-and-radiation.md",
        POST / "mts-derived-wavelength-test-20261107/build-full-momentum/camb_python.f90",
        POST / "mts-background-operator-bridge-20261107/build/MTSTwoField.f90",
        PARENT / "DERIVATION.md", PARENT / "micromotion.py", PARENT / "near_identity_parent.py"]
    sources = {str(path): digest(path) for path in authorities}
    check("all local authority paths", all(path.is_file() for path in authorities))
    failed = read(ROOT / "action-01.end.json")
    check("failed checker preserved", failed["exit_code"] == 1
          and digest(ROOT / "test_action_sources.py") == failed["source_sha256"])
    repaired = read(ROOT / "action-02.end.json")
    check("repaired checker succeeded", repaired["exit_code"] == 0
          and digest(ROOT / "test_action_sources_repaired.py") == repaired["source_sha256"])
    evidence = dict(passed=all(checks.values()), count=len(checks), checks=checks, compiled_sources=compiled,
                    authority_sources=sources, result_sha256=digest(OUTPUT / "result.json"),
                    csv_sha256=digest(OUTPUT / "summary.csv"), symbolic_sha256=digest(OUTPUT / "symbolic-result.json"),
                    original_failed_checker_retained=True, no_changed_tolerances=True)
    write(OUTPUT / "validation.json", evidence)
    print("Validated", len(checks), "checks;", len(compiled), "sources compiled without bytecode", flush=True)


if __name__ == "__main__":
    main()

