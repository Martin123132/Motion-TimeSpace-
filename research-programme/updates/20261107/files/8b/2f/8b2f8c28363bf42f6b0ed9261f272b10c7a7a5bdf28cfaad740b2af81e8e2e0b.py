import csv
import math
from common import ROOT, POST, PARENT, SECOND, PARENT_SEAL, ALGEBRA, GATE, modest, guard, require, read, write, digest


def main():
    modest()
    checks = {}
    def check(name, condition):
        checks[name] = bool(condition)
        require(condition, name)
    result = read(ROOT / "result.json")
    check("completed", result["passed"] and result["state"] == "complete")
    check("retained scope", result["scalar_gravity_hamiltonian_constructed"] and result["frozen_phase_mean_derived"]
          and not result["averaged_forward_qualification_claimed"] and not result["collision_species_hamiltonian_invented"])
    check("no new evolutions", result["new_evolutions"] == 0 and result["reused_histories"] == 42)
    check("parent seal", digest(PARENT / "closeout.json") == PARENT_SEAL)
    for path, checksum in result["source_hashes"].items():
        check("frozen:" + path, digest(path) == checksum)
    expected = {(family["model"] + "-" + family["label"], case["tag"]): case["sha256"]
                for family in read(SECOND / "prediction-result.json")["reports"] for case in family["cases"]}
    seen = set()
    for row in result["records"]:
        guard()
        key = (row["family"], row["tag"])
        check("unique:" + str(key), key not in seen)
        seen.add(key)
        check("packet:" + str(key), digest(row["packet"]) == expected[key] == row["sha256"])
        check("record:" + str(key), read(ROOT / "records" / (row["family"] + "-" + row["tag"] + ".json")) == row)
        for name, value in row["checks"].items():
            check(str(key) + name, math.isfinite(value) and 0 <= value < ALGEBRA)
        raw = row["diagnostics"]["raw_flow_errors"]
        check("raw fixed gate:" + str(key), row["diagnostics"]["raw_flow_within_retained_gate"] == (max(raw) < GATE))
        check("raw passes:" + str(key), max(raw) < GATE)
        check("finite accounted:" + str(key), max(row["diagnostics"]["accounted_flow_errors"]) < ALGEBRA)
        if row["tag"].endswith("zero"):
            check("zero flow:" + str(key), max(raw) == 0 and row["checks"]["zero_state_flow"] == 0)
    check("coverage", seen == set(expected))
    symbolic = read(ROOT / "symbolic-result.json")
    check("13 identities", symbolic["passed"] and len(symbolic["identities"]) == 13 and all(symbolic["identities"].values()))
    with (ROOT / "summary.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    check("CSV rows", len(rows) == 42 and all(None not in row and None not in row.values() for row in rows))
    check("CSV coverage", {(row["family"], row["case"]) for row in rows} == seen)
    canonical = read(ROOT / "canonical/result.json")
    check("canonical scope", canonical["passed"] and canonical["exact_frozen_canonical_map"]
          and canonical["actual_background_derivative_pending"] and canonical["new_evolutions"] == 0)
    for path, checksum in canonical["source_hashes"].items():
        check("canonical source:" + path, digest(path) == checksum)
    check("six canonical controls", len(canonical["reports"]) == 6)
    for row in canonical["reports"]:
        check("canonical packet:" + row["family"], digest(row["packet"]) == row["sha256"])
        if row["family"].startswith("cold"):
            check("cold identity:" + row["family"], row["identity_control"] and row["passed"])
            continue
        check("canonical no overclaim:" + row["family"], not row["full_time_derivative_included"] and not row["forward_qualified"])
        check("33 canonical probes:" + row["family"], row["probes"] == 33)
        for name in ("fourier_reconstruction", "coefficient_refinement", "symplectic", "inverse", "transformed_symmetry", "full_chain"):
            check(row["family"] + name, math.isfinite(row["maxima"][name]) and row["maxima"][name] < ALGEBRA)
        check("metric really transformed:" + row["family"], row["maxima"]["metric_mixing"] > 0)
        check("finite transformation:" + row["family"], math.isfinite(row["maxima"]["near_identity"]))
    for label in ("joint-01", "canonical-01"):
        receipt = read(ROOT / (label + ".end.json"))
        script = "derive_and_test.py" if label == "joint-01" else "canonical_generator.py"
        check("worker:" + label, receipt["exit_code"] == 0 and digest(ROOT / script) == receipt["source_sha256"])
    compiled = {}
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        compiled[str(path)] = digest(path)
    check("no bytecode", not list(ROOT.rglob("__pycache__")))
    authorities = [
        PARENT / "DERIVATION.md", PARENT / "METRIC-VARIATION.md",
        POST / "condensate-origin-20261003/native-two-field-transfer-20261007/54-native-canonical-fields-and-radiation.md",
        POST / "mts-derived-wavelength-test-20261107/build-full-momentum/camb_python.f90",
        POST / "mts-metric-feedback-20261107/observer.f90"]
    sources = {str(path): digest(path) for path in authorities}
    write(ROOT / "validation.json", dict(passed=all(checks.values()), count=len(checks), checks=checks,
          compiled_sources=compiled, authority_sources=sources, result_sha256=digest(ROOT / "result.json"),
          canonical_sha256=digest(ROOT / "canonical/result.json"), symbolic_sha256=digest(ROOT / "symbolic-result.json"),
          csv_sha256=digest(ROOT / "summary.csv")))
    print("Validated", len(checks), "checks;", len(compiled), "sources compiled without bytecode", flush=True)


if __name__ == "__main__":
    main()

