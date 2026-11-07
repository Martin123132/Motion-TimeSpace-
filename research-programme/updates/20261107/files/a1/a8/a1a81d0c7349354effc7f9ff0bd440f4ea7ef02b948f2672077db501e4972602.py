import ast
import sys
from common import ROOT, PRIOR, BRANCH, modest, guard, check_prior, require, read, write, digest, load
import numpy as np


def main():
    modest()
    check_prior()
    package = PRIOR / "build-corrected/native"
    sys.path.insert(0, str(package))
    import camb
    from camb.mts import MTSTwoField
    sys.path.append(str(BRANCH / "radiation-and-slow-field-transfer-20261007"))
    import radiation_common
    owner = BRANCH / "native-heavy-matching-20261007/matching_common.py"
    factory = next(node for node in ast.parse(owner.read_text()).body if isinstance(node, ast.FunctionDef) and node.name == "params_for")
    namespace = dict(np=np, previous=radiation_common, MTSTwoField=MTSTwoField)
    exec(compile(ast.Module(body=[factory], type_ignores=[]), str(owner), "exec"), namespace)
    destination = ROOT / "inputs"
    destination.mkdir(exist_ok=False)
    reports = []
    for model in ("heavy", "cold"):
        guard()
        folder = PRIOR / "runs-balanced" / model
        reference, audit = load(folder / "native-reference.npz"), load(folder / "operator-audit.npz")
        table = BRANCH / f"native-two-field-transfer-20261007/runs/backgrounds/{model}.npz"
        params = namespace["params_for"](table)
        native = camb.get_background(params)
        require(params.omk == 0, "flat-tail identity requires flat retained background")
        times = np.unique(np.r_[reference["times"], audit["times"]])
        opacity = native.get_background_time_evolution(times, ["opacity"])["opacity"]
        scale_factor = 1 / (1 + native.redshift_at_conformal_time(times))
        require(np.isfinite(opacity).all() and np.min(opacity) >= 0 and np.min(scale_factor) > 0, "physical background")
        original = np.searchsorted(times, reference["times"])
        observed_scale = reference["observer"][:, reference["observer_names"].tolist().index("a_native")]
        relative = float(np.max(abs(scale_factor[original] - observed_scale) / observed_scale))
        require(relative < 2e-5, "background representation changed")
        path = destination / (model + ".npz")
        np.savez_compressed(path, times=times, opacity=opacity, scale_factor=scale_factor, reference_indices=original, audit_indices=np.searchsorted(times, audit["times"]))
        reports.append(dict(model=model, file=str(path), sha256=digest(path), reference_sha256=digest(folder / "native-reference.npz"), operator_sha256=digest(folder / "operator-audit.npz"), table_sha256=digest(table), scale_factor_error=relative, minimum_opacity=float(np.min(opacity)), maximum_opacity=float(np.max(opacity)), flat=True))
        print(reports[-1], flush=True)
        del native
    write(ROOT / "input-result.json", dict(passed=True, reports=reports, source_sha256=digest(__file__), factory_sha256=digest(owner), dll_sha256=digest(package / "camb/cambdll.dll"), protocol_sha256=digest(ROOT / "PROTOCOL.md"), perturbation_evolution_rerun=False))


if __name__ == "__main__":
    main()
