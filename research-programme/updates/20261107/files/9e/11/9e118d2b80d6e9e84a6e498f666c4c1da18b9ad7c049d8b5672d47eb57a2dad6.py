import os

from common import ROOT, modest, require, read, write, digest
from probe_analysis import packet, physical, norm_error, algebraic
import numpy as np


def main():
    modest()
    native = read(ROOT / "native-probe-result.json")
    require(native["state"] == "complete" and len(native["reports"]) == 48, "incomplete probes")
    for row in native["reports"]:
        require(digest(ROOT / "packets" / row["file"]) == row["sha256"], "changed packet")
    reports = []
    for model in ("heavy", "cold"):
        for index, wave in enumerate((.03, .1, 1., 5.)):
            packets = {tag: packet(model, index, tag) for tag in ("zero", "plus", "minus", "halfplus", "halfminus")}
            data = {tag: physical(value, model) for tag, value in packets.items()}
            checks, response, half_response = [], {}, {}
            for key in data["zero"]:
                response[key] = (data["plus"][key] - data["minus"][key]) / .2
                half_response[key] = (data["halfplus"][key] - data["halfminus"][key]) / .1
                symmetry = (data["plus"][key] + data["minus"][key] - 2 * data["zero"][key]) / .2
                symmetry_error = norm_error(symmetry, response[key])
                step_error = norm_error(half_response[key] - response[key], response[key])
                checks.append(dict(variable=key, response_scale=float(np.max(abs(response[key]))),
                    response_to_original=norm_error(response[key], data["zero"][key]), symmetry_error=symmetry_error,
                    step_error=step_error, passed=bool(max(symmetry_error, step_error) < 2e-5)))
            constraint_error = max(algebraic(value) for value in packets.values())
            passed = all(row["passed"] for row in checks) and constraint_error < 1e-10
            names = list(response)
            target = ROOT / f"response-{model}-{index}.npz"
            np.savez_compressed(target, values=np.column_stack([response[key] for key in names]),
                half_values=np.column_stack([half_response[key] for key in names]), names=np.array(names),
                times=packets["zero"]["times"], k=wave)
            reports.append(dict(model=model, index=index, k=wave, checks=checks, constraint_error=constraint_error,
                passed=passed, response_file=target.name, response_sha256=digest(target)))
    result = dict(passed=all(row["passed"] for row in reports), pid=os.getpid(), reports=reports,
        native_result_sha256=digest(ROOT / "native-probe-result.json"), source_sha256=digest(__file__),
        analysis_source_sha256=digest(ROOT / "probe_analysis.py"), response_gate=2e-5, constraint_gate=1e-10)
    write(ROOT / "probe-check-result.json", result)
    print(dict(passed=result["passed"], max_constraint=max(row["constraint_error"] for row in reports),
        max_symmetry=max(check["symmetry_error"] for row in reports for check in row["checks"]),
        max_step=max(check["step_error"] for row in reports for check in row["checks"]),
        failures=[dict(model=row["model"], k=row["k"], checks=[check for check in row["checks"] if not check["passed"]]) for row in reports if not row["passed"]]), flush=True)
    require(result["passed"], "response gate failed; inspect rather than retune")


if __name__ == "__main__":
    main()
