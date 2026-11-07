import ast
import ctypes
import hashlib
import os
import sys
from datetime import datetime, timezone

from common import ROOT, PRIOR, PAIRED, NATIVE, BRANCH, EARLY, modest, guard, require, read, write, digest
import numpy as np


def relative(left, right):
    return float(np.max(np.max(abs(left - right), axis=0) / np.maximum(np.max(abs(right), axis=0), 1e-30)))


def main():
    modest()
    build = read(ROOT / "build-result.json")
    require(build["state"] == "complete" and digest(ROOT / "native/camb/cambdll.dll") == build["dll_sha256"], "unowned isolated build")
    prior = read(PRIOR / "full-cadence/native-result.json")
    for path, checksum in prior["protected_source_hashes"].items():
        require(digest(path) == checksum, "parent changed")
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
    observer_dll = ctypes.CDLL(str(PRIOR / "observer.dll"))
    function = ctypes.cast(observer_dll.source_func_, ctypes.c_void_p)
    loaded = camb.baseconfig.camblib
    config = {name: ctypes.c_int.in_dll(loaded, "mts_probe_" + name) for name in ("step", "kind", "count", "tangent")}
    epsilon_ref = ctypes.c_double.in_dll(loaded, "mts_probe_epsilon")
    before = (ctypes.c_double * 4).in_dll(loaded, "mts_probe_before")
    after = (ctypes.c_double * 4).in_dll(loaded, "mts_probe_after")
    flags = (ctypes.c_int * 4).in_dll(loaded, "mts_probe_flags")
    untouched = ctypes.c_double.in_dll(loaded, "mts_probe_untouched")
    cache = ctypes.c_double.in_dll(loaded, "mts_probe_cache_max")
    names = list(camb.model.evolve_names)
    growth_index = names.index("growth")
    with np.load(PRIOR / "full-cadence/observer-heavy-3.npz") as packet:
        observer_names = packet["observer_names"].tolist()
    count = len(names) + len(observer_names)
    folder = ROOT / "packets"
    folder.mkdir(exist_ok=False)
    reports = []
    state, error = "running", None
    try:
        for model in ("heavy", "cold"):
            with np.load(EARLY / f"runs/final-bg8-start/{model}.npz") as original:
                times = np.ascontiguousarray(original["conformal_time"])
                selected = np.concatenate([np.arange((center := int(np.argmin(abs(original["requested_scale"] - target)))) - 64, center + 65)
                    for target in (.0002, .000225, .00025)])
            params = namespace["params_for"](EARLY / f"runs/backgrounds/{model}.npz")
            native = camb.get_background(params)
            native.Params.Accuracy.IntTolBoost = 6
            native.Params.Accuracy.lAccuracyBoost = 4
            off = prefix = None
            entry = next(row for row in prior["reports"] if row["model"] == model and row["k"] == 5.)
            require(digest(entry["full_schedule_source"]) == entry["full_schedule_sha256"], "changed saved reference")
            with np.load(entry["full_schedule_source"]) as original:
                reference_observer = original["full_observer"][selected].copy()
                reference_standard = original["full_standard"][selected].copy()
            for tag, amplitude, direct in (("off", 0., False), ("restart", 0., False), ("zero", 0., True),
                    ("one", 1., True), ("negative", -1., True), ("half", .5, True), ("negativehalf", -.5, True)):
                guard()
                config["step"].value = 0 if tag == "off" else int(selected[0] + 1)
                config["kind"].value = 1 if model == "heavy" else 2
                config["count"].value = 0
                config["tangent"].value = int(direct)
                epsilon_ref.value = amplitude
                for slot in range(4):
                    before[slot] = after[slot] = flags[slot] = 0
                untouched.value = cache.value = 0.
                output = np.zeros((1, len(times), count))
                code = camb.results.CAMB_TimeEvolution(ctypes.byref(native), ctypes.byref(ctypes.c_int(1)), np.array([5.]),
                    ctypes.byref(ctypes.c_int(len(times))), times, ctypes.byref(ctypes.c_int(count)), output,
                    ctypes.byref(ctypes.c_int(len(observer_names))), ctypes.byref(function))
                physical_columns = np.arange(count) != growth_index
                require(code == 0 and np.isfinite(output[0, :, physical_columns]).all(), "native physical output failure")
                prefix_hash = hashlib.sha256(output[0, :selected[0]].tobytes()).hexdigest()
                standard = output[0, :, :len(names)]
                observer = output[0, :, len(names):]
                get = lambda name: observer[:, observer_names.index(name)]
                density = get("R_cdm") * get("delta_cdm64") + get("R_baryon") * get("delta_baryon64")
                growth_defined = np.isfinite(standard[:, growth_index]) & (density != 0)
                standard[~growth_defined, growth_index] = np.nan
                filename = f"{model}-3-{tag}.npz"
                np.savez_compressed(folder / filename, standard=standard[selected], observer=observer[selected],
                    full_standard=standard, full_observer=observer, full_times=times, times=times[selected],
                    names=np.array(names), observer_names=np.array(observer_names), original_indices=selected,
                    growth_defined=growth_defined, k=5., amplitude=amplitude)
                hook = dict(count=config["count"].value, before=list(before), after=list(after),
                    untouched=untouched.value, flags=list(flags), cache_max=cache.value)
                row = dict(model=model, tag=tag, amplitude=amplitude, direct=direct, file=filename,
                    sha256=digest(folder / filename), prefix_hash=prefix_hash, hook=hook,
                    undefined_growth_rows=int(np.sum(~growth_defined)))
                if tag == "off":
                    off, prefix = output[0, selected].copy(), prefix_hash
                    columns = np.arange(len(names)) != growth_index
                    row["original_observer_error"] = relative(observer[selected], reference_observer)
                    row["original_standard_error"] = relative(standard[selected][:, columns], reference_standard[:, columns])
                    require(max(row["original_observer_error"], row["original_standard_error"]) < 2e-5, "off control failed")
                else:
                    require(hook["count"] == 1 and prefix_hash == prefix and hook["untouched"] == 0, "hook ownership")
                    if direct:
                        require(hook["flags"][0] == 0 and hook["cache_max"] == 0, "unsupported memory or uncleared cache")
                        expected = np.zeros(4)
                        slots = [2, 3] if model == "heavy" else [0]
                        expected[slots] = amplitude * np.array(hook["before"])[slots]
                        require(np.array_equal(expected, hook["after"]), "incorrect tangent direction")
                    else:
                        row["restart_error"] = relative(observer[selected], off[:, len(names):])
                        require(row["restart_error"] < 2e-5, "ordinary zero restart failed")
                reports.append(row)
                write(folder / (filename + ".json"), row)
                print(model, tag, "saved", hook["flags"], flush=True)
            del native
        state = "complete"
    except BaseException as exception:
        state, error = "failed", repr(exception)
        raise
    finally:
        config["step"].value = config["tangent"].value = 0
        write(ROOT / "tangent-native-result.json", dict(state=state, error=error, pid=os.getpid(),
            finished=datetime.now(timezone.utc).isoformat(), reports=reports, source_sha256=digest(__file__),
            build_sha256=digest(ROOT / "build-result.json"), original_source_hashes=prior["protected_source_hashes"],
            observer_sha256=digest(PRIOR / "observer.dll"), paired_result_sha256=digest(PAIRED / "probe-check-result.json"),
            scope="Direct tangent initial state, including perturbative cache clearing; original full-species evolution.",
            growth_convention="NaN with explicit mask for undefined matter-density growth ratio; all physical output finite."))


if __name__ == "__main__":
    main()
