import ast
import ctypes
import hashlib
import os
import sys
from datetime import datetime, timezone

from common import ROOT, PRIOR, NATIVE, BRANCH, EARLY, modest, guard, require, read, write, digest
import numpy as np


def relative(left, right):
    scale = np.maximum(np.max(abs(right), axis=0), 1e-30)
    return float(np.max(np.max(abs(left - right), axis=0) / scale))


def main():
    modest()
    build = read(ROOT / "build-result.json")
    require(build["state"] == "complete" and build["temporary_mappings_removed"], "unaccepted build")
    require(digest(ROOT / "native/camb/cambdll.dll") == build["dll_sha256"], "changed test DLL")
    prior = read(PRIOR / "full-cadence/native-result.json")
    for path, checksum in prior["protected_source_hashes"].items():
        require(digest(path) == checksum, "changed original input")
    require(digest(PRIOR / "observer.dll") == prior["observer_dll_sha256"], "changed observer")
    sys.path.insert(0, str(ROOT / "native"))
    import camb
    from camb.mts import MTSTwoField
    sys.path.append(str(BRANCH / "radiation-and-slow-field-transfer-20261007"))
    import radiation_common
    require(str(ROOT / "native").lower() in str(camb.__file__).lower(), "wrong native import")
    owner = NATIVE.parent / "matching_common.py"
    factory = next(node for node in ast.parse(owner.read_text()).body if isinstance(node, ast.FunctionDef) and node.name == "params_for")
    namespace = dict(np=np, previous=radiation_common, MTSTwoField=MTSTwoField)
    exec(compile(ast.Module(body=[factory], type_ignores=[]), str(owner), "exec"), namespace)
    params_for = namespace["params_for"]
    library = ctypes.CDLL(str(PRIOR / "observer.dll"))
    function = ctypes.cast(library.source_func_, ctypes.c_void_p)
    loaded = camb.baseconfig.camblib
    config = {name: ctypes.c_int.in_dll(loaded, "mts_probe_" + name) for name in ("step", "kind", "count")}
    epsilon_ref = ctypes.c_double.in_dll(loaded, "mts_probe_epsilon")
    before = (ctypes.c_double * 4).in_dll(loaded, "mts_probe_before")
    after = (ctypes.c_double * 4).in_dll(loaded, "mts_probe_after")
    untouched = ctypes.c_double.in_dll(loaded, "mts_probe_untouched")
    names = list(camb.model.evolve_names)
    with np.load(PRIOR / "full-cadence/observer-heavy-0.npz") as old:
        observer_names = old["observer_names"].tolist()
    count = len(names) + len(observer_names)
    folder = ROOT / "packets"
    folder.mkdir(exist_ok=False)
    reports = []
    state, error = "running", None
    try:
        for model in ("heavy", "cold"):
            with np.load(EARLY / f"runs/final-bg8-start/{model}.npz") as original:
                full_times = np.ascontiguousarray(original["conformal_time"])
                selected = np.concatenate([np.arange((center := int(np.argmin(abs(original["requested_scale"] - target)))) - 64, center + 65)
                    for target in (.0002, .000225, .00025)])
                modes = original["modes"].copy()
            params = params_for(EARLY / f"runs/backgrounds/{model}.npz")
            native = camb.get_background(params)
            native.Params.Accuracy.IntTolBoost = 6
            native.Params.Accuracy.lAccuracyBoost = 4
            for index, wave in enumerate(modes):
                entry = next(row for row in prior["reports"] if row["model"] == model and row["k"] == wave)
                require(digest(entry["full_schedule_source"]) == entry["full_schedule_sha256"], "changed full reference")
                with np.load(entry["full_schedule_source"]) as cached:
                    old_observer = cached["full_observer"][selected].copy()
                    old_standard = cached["full_standard"][selected].copy()
                reference = prefix = None
                for tag, epsilon in (("off", 0.), ("zero", 0.), ("plus", .1), ("minus", -.1), ("halfplus", .05), ("halfminus", -.05)):
                    guard()
                    config["step"].value = 0 if tag == "off" else int(selected[0] + 1)
                    config["kind"].value = 1 if model == "heavy" else 2
                    config["count"].value = 0
                    epsilon_ref.value = epsilon
                    for slot in range(4):
                        before[slot] = after[slot] = 0.
                    untouched.value = 0.
                    output = np.zeros((1, len(full_times), count))
                    code = camb.results.CAMB_TimeEvolution(ctypes.byref(native), ctypes.byref(ctypes.c_int(1)), np.array([wave]),
                        ctypes.byref(ctypes.c_int(len(full_times))), full_times, ctypes.byref(ctypes.c_int(count)), output,
                        ctypes.byref(ctypes.c_int(len(observer_names))), ctypes.byref(function))
                    require(code == 0 and np.isfinite(output).all(), "native probe failure")
                    panel = output[0, selected]
                    filename = f"{model}-{index}-{tag}.npz"
                    np.savez_compressed(folder / filename, standard=panel[:, :len(names)], observer=panel[:, len(names):],
                        names=np.array(names), observer_names=np.array(observer_names), times=full_times[selected],
                        k=float(wave), epsilon=epsilon, original_indices=selected)
                    prefix_hash = hashlib.sha256(output[0, :selected[0]].tobytes()).hexdigest()
                    hook = dict(count=config["count"].value, before=list(before), after=list(after), untouched=untouched.value)
                    row = dict(model=model, k=float(wave), index=index, tag=tag, epsilon=epsilon, file=filename,
                        sha256=digest(folder / filename), prefix_hash=prefix_hash, hook=hook)
                    if tag == "off":
                        reference, prefix = panel.copy(), prefix_hash
                        row["observer_original_error"] = relative(panel[:, len(names):], old_observer)
                        row["standard_original_error"] = relative(panel[:, :len(names)], old_standard)
                        require(max(row["observer_original_error"], row["standard_original_error"]) < 2e-5, "isolated build control failed")
                    else:
                        require(hook["count"] == 1 and hook["untouched"] == 0 and prefix_hash == prefix, "hook ownership failed")
                        selected_slots = (2, 3) if model == "heavy" else (0,)
                        for slot in range(4):
                            expected = hook["before"][slot] * (1 + epsilon) if slot in selected_slots else hook["before"][slot]
                            require(hook["after"][slot] == expected, "incorrect seed change")
                        if tag == "zero":
                            row["restart_observer_error"] = relative(panel[:, len(names):], reference[:, len(names):])
                            row["restart_standard_error"] = relative(panel[:, :len(names)], reference[:, :len(names)])
                            require(max(row["restart_observer_error"], row["restart_standard_error"]) < 2e-5, "zero restart failed")
                    reports.append(row)
                    write(folder / (filename + ".json"), row)
                    print(model, float(wave), tag, "saved", flush=True)
            del native
        state = "complete"
    except BaseException as exception:
        state, error = "failed", repr(exception)
        raise
    finally:
        config["step"].value = 0
        write(ROOT / "native-probe-result.json", dict(state=state, error=error, pid=os.getpid(),
            finished=datetime.now(timezone.utc).isoformat(), reports=reports, source_sha256=digest(__file__),
            build_sha256=digest(ROOT / "build-result.json"), original_source_hashes=prior["protected_source_hashes"],
            observer_sha256=digest(PRIOR / "observer.dll"), params_factory_sha256=digest(owner),
            inherited_parameters_sha256=digest(BRANCH / "cosmology-reconnection-20261006/results/comparison/status.json"),
            scope="Changed Cauchy data at the retained slice; all species subsequently coupled. No source-created impulse or new fitted occupation."))


if __name__ == "__main__":
    main()
