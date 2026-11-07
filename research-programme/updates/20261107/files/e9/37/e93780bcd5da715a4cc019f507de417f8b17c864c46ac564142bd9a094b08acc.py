import os

from common import ROOT, PAIRED, modest, require, read, write, digest
from probe_analysis import packet, physical, norm_error, algebraic
import numpy as np


def main():
    modest()
    native = read(ROOT / "tangent-native-result.json")
    require(native["state"] == "complete" and len(native["reports"]) == 14, "incomplete tangent runs")
    old = read(PAIRED / "probe-check-result.json")
    require(digest(PAIRED / "probe-check-result.json") == native["paired_result_sha256"] and not old["passed"], "paired evidence changed")
    for row in native["reports"]:
        require(digest(ROOT / "packets" / row["file"]) == row["sha256"], "changed tangent packet")
    reports = []
    for model in ("heavy", "cold"):
        packets = {tag: packet(model, 3, tag) for tag in ("zero", "one", "negative", "half", "negativehalf")}
        data = {tag: physical(value, model) for tag, value in packets.items()}
        source = next(row for row in old["reports"] if row["model"] == model and row["k"] == 5.)
        require(digest(PAIRED / source["response_file"]) == source["response_sha256"], "changed paired estimate")
        with np.load(PAIRED / source["response_file"]) as saved:
            old_names = saved["names"].tolist()
            old_values, old_half = saved["values"].copy(), saved["half_values"].copy()
        checks = []
        for name, reference in data["one"].items():
            parity = norm_error(data["negative"][name] + reference, reference)
            half = norm_error(2 * data["half"][name] - reference, reference)
            negative_half = norm_error(-2 * data["negativehalf"][name] - reference, reference)
            zero = float(np.max(abs(data["zero"][name])))
            paired = old_values[:, old_names.index(name)]
            paired_half = old_half[:, old_names.index(name)]
            checks.append(dict(variable=name, zero_max=zero, response_scale=float(np.max(abs(reference))),
                parity=parity, half_error=half, negative_half_error=negative_half,
                paired_error=norm_error(paired - reference, reference), paired_half_error=norm_error(paired_half - reference, reference),
                initial_pair_difference=float(abs(paired[0] - reference[0]) / max(float(np.max(abs(reference))), 1e-30)),
                passed=bool(zero == 0 and max(parity, half, negative_half) < 2e-5)))
        max_constraint = max(algebraic(value) for value in packets.values())
        names = list(data["one"])
        filename = f"direct-response-{model}.npz"
        np.savez_compressed(ROOT / filename, names=np.array(names), times=packets["one"]["times"],
            values=np.column_stack([data["one"][name] for name in names]),
            half_values=np.column_stack([2 * data["half"][name] for name in names]),
            paired_values=old_values, paired_half_values=old_half, paired_names=np.array(old_names), k=5.)
        reports.append(dict(model=model, k=5., passed=all(row["passed"] for row in checks) and max_constraint < 1e-10,
            checks=checks, max_constraint=max_constraint, file=filename, sha256=digest(ROOT / filename),
            original_paired_passed=source["passed"]))
    result = dict(passed=all(row["passed"] for row in reports), pid=os.getpid(), reports=reports,
        native_result_sha256=digest(ROOT / "tangent-native-result.json"), paired_result_sha256=digest(PAIRED / "probe-check-result.json"),
        source_sha256=digest(__file__), analysis_source_sha256=digest(ROOT / "probe_analysis.py"),
        response_gate=2e-5, constraint_gate=1e-10,
        scope="Direct response normalization/parity and old-pair comparison, not continuum discretization accuracy.")
    write(ROOT / "tangent-check-result.json", result)
    print(dict(passed=result["passed"], cases=[dict(model=row["model"], constraint=row["max_constraint"],
        max_homogeneity=max(max(item["parity"], item["half_error"], item["negative_half_error"]) for item in row["checks"]),
        max_old_pair=max(item["paired_error"] for item in row["checks"]),
        max_old_half_pair=max(item["paired_half_error"] for item in row["checks"]),
        failed=[item for item in row["checks"] if not item["passed"]]) for row in reports]), flush=True)
    require(result["passed"], "direct response gate failed; preserve and inspect")


if __name__ == "__main__":
    main()
