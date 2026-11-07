import ast
import ctypes
import os
import sys
import time
from datetime import datetime, timezone
from common import ROOT, PRIOR, PAIRED, SOURCE, HIERARCHY, CLOSURE, NATIVE, BRANCH, EARLY, WAVE, ALGEBRA, modest, guard, check_prior, require, read, write, digest, load
import numpy as np


POINTER = ctypes.POINTER(ctypes.c_double)
INTEGER_POINTER = ctypes.POINTER(ctypes.c_int)
TAGS = ("L16-base", "L64-base", "L64-fine", "L128-fine", "G192-fine", "L64-zero", "L64-negative")
STEPS = (1e-3, 5e-4, 2.5e-4, 1.25e-4)

def pointer(values):
    return values.ctypes.data_as(POINTER)


def row_error(left, right):
    return float(np.max(abs(left - right) / np.maximum(np.max(abs(right), axis=1, keepdims=True), 1e-80)))


def main():
    modest()
    check_prior()
    build = read(ROOT / "build/build-result.json")
    require(build["state"] == "complete" and build["dll_sha256"] == digest(ROOT / "build/native/camb/cambdll.dll"), "isolated build ownership")
    sys.path.insert(0, str(ROOT / "build/native"))
    import camb
    from camb.mts import MTSTwoField
    sys.path.append(str(BRANCH / "radiation-and-slow-field-transfer-20261007"))
    import radiation_common
    factory_owner = NATIVE.parent / "matching_common.py"
    factory = next(node for node in ast.parse(factory_owner.read_text()).body if isinstance(node, ast.FunctionDef) and node.name == "params_for")
    namespace = dict(np=np, previous=radiation_common, MTSTwoField=MTSTwoField)
    exec(compile(ast.Module(body=[factory], type_ignores=[]), str(factory_owner), "exec"), namespace)
    lib = camb.baseconfig.camblib
    observer_dll = ctypes.CDLL(str(PRIOR / "observer.dll"))
    source_function = ctypes.cast(observer_dll.source_func_, ctypes.c_void_p)
    flags = {name: ctypes.c_int.in_dll(lib, "mts_probe_" + name) for name in ("step", "kind", "count", "tangent")}
    capture = {name: ctypes.c_int.in_dll(lib, "mts_capture_" + name) for name in ("begin", "end", "count", "dimension", "native_dimension", "selector")}
    epsilon = ctypes.c_double.in_dll(lib, "mts_probe_epsilon")
    mapping = (ctypes.c_int * 512).in_dll(lib, "mts_capture_map")
    signature = (ctypes.c_int * 96).in_dll(lib, "mts_capture_signature")
    lib.mts_capture_reset.argtypes, lib.mts_capture_reset.restype = [], None
    lib.mts_capture_copy.argtypes = [ctypes.c_int, ctypes.c_int, POINTER, POINTER, POINTER]
    lib.mts_capture_copy.restype = None
    lib.mts_operator_window.argtypes, lib.mts_operator_window.restype = [ctypes.c_double, INTEGER_POINTER], None
    lib.mts_operator_rhs.argtypes, lib.mts_operator_rhs.restype = [ctypes.c_double, ctypes.c_int, POINTER, POINTER], None
    lib.mts_operator_observe.argtypes, lib.mts_operator_observe.restype = [ctypes.c_double, ctypes.c_int, POINTER, ctypes.c_int, POINTER], None
    lib.mts_operator_kinetic.argtypes, lib.mts_operator_kinetic.restype = [ctypes.c_double, ctypes.c_int, POINTER, POINTER], None
    lib.mts_operator_stress.argtypes, lib.mts_operator_stress.restype = [ctypes.c_double, ctypes.c_int, POINTER, POINTER, POINTER], None
    native_names = list(camb.model.evolve_names)
    owner_result = read(SOURCE / "phase-resolved/tangent-native-result.json")
    hierarchy_owner = read(HIERARCHY / "hierarchy-balanced-result.json")
    destination = ROOT / "runs"
    destination.mkdir(exist_ok=False)
    write(ROOT / "readout-config.json", dict(source_sha256=digest(__file__), protocol_sha256=digest(ROOT / "PROTOCOL.md"), tags=TAGS, difference_steps=STEPS, created_utc=datetime.now(timezone.utc).isoformat(), coupled_closeout_sha256=digest(CLOSURE / "closeout.json"), no_new_evolution=True))
    coupled_owner = read(CLOSURE / "prediction-result.json")
    reports, failure = [], None
    try:
        for model in ("heavy", "cold"):
            guard()
            old_folder = HIERARCHY / "runs-balanced" / model
            reference = load(old_folder / "native-reference.npz")
            audit = load(old_folder / "operator-audit.npz")
            normalization = load(old_folder / "balanced-scale.npz")["normalization"]
            old_report = next(row for row in hierarchy_owner["reports"] if row["model"] == model)
            require(digest(old_folder / "native-reference.npz") == old_report["captured_reference_sha256"], "initial state owner")
            require(digest(old_folder / "operator-audit.npz") == old_report["operator_audit_sha256"], "operator owner")
            source_row = next(row for row in owner_result["reports"] if row["model"] == model and row["tag"] == "one")
            source_path = SOURCE / "phase-resolved/packets" / source_row["file"]
            require(digest(source_path) == source_row["sha256"], "initial prefix owner")
            with np.load(source_path) as packet:
                first = int(packet["original_indices"][0])
                prefix = np.ascontiguousarray(packet["full_times"][:first + 1])
            times = reference["times"]
            require(prefix[-1] == times[0], "initial capture endpoint")
            names = reference["observer_names"].tolist()
            params = namespace["params_for"](EARLY / f"runs/backgrounds/{model}.npz")
            native = camb.get_background(params)
            native.Params.Accuracy.IntTolBoost = 6
            native.Params.Accuracy.lAccuracyBoost = 4
            lib.mts_capture_reset()
            flags["step"].value, flags["kind"].value = first + 1, 1 if model == "heavy" else 2
            flags["count"].value, flags["tangent"].value = 0, 1
            epsilon.value = 1.
            capture["begin"].value = capture["end"].value = first + 1
            count = len(native_names) + len(names)
            output = np.zeros((1, len(prefix), count))
            code = camb.results.CAMB_TimeEvolution(ctypes.byref(native), ctypes.byref(ctypes.c_int(1)), np.array([WAVE]), ctypes.byref(ctypes.c_int(len(prefix))), prefix, ctypes.byref(ctypes.c_int(count)), output, ctypes.byref(ctypes.c_int(len(names))), ctypes.byref(source_function))
            require(code == 0 and capture["count"].value == 1, "single initial capture")
            dimension = capture["dimension"].value
            initial, initial_rate = np.zeros((dimension, 1), order="F"), np.zeros((dimension, 1), order="F")
            initial_time = np.zeros(1)
            lib.mts_capture_copy(dimension, 1, pointer(initial), pointer(initial_rate), pointer(initial_time))
            require(np.array_equal(initial[:, 0], reference["initial"]), "initial perturbation changed")
            require(np.array_equal(initial_rate[:, 0], reference["derivative"][0]), "initial derivative changed")
            require(np.array_equal(output[0, -1, len(native_names):], reference["observer"][0]), "initial observer changed")
            require(np.array_equal(np.array(list(mapping)[:dimension]), reference["mapping"]), "state map changed")
            require(np.array_equal(np.array(list(signature)), reference["signature"]), "initial regime signature changed")
            saved_signature = np.ascontiguousarray(reference["signature"], dtype=np.int32)
            lib.mts_operator_window(float(times[-1]), saved_signature.ctypes.data_as(INTEGER_POINTER))
            signature_values = reference["signature"]
            require(signature_values[20] == 1 and signature_values[30] == 5 and signature_values[40] == 16, "expected retained massive-neutrino layout")
            def position(native_index):
                return int(np.flatnonzero(reference["mapping"] == native_index)[0])
            all_moments = np.column_stack([[position(int(signature_values[50]) + node * 17 + ell) for ell in range(17)] for node in range(5)])
            tail_slots, low_slots = all_moments[3:], all_moments[2]
            core = np.array([index for index in range(dimension) if index not in tail_slots])
            require(np.count_nonzero(reference["initial"][tail_slots]) == 0, "initial high-moment preparation not zero")
            tail_units = np.max(normalization[all_moments], axis=0)
            model_root = destination / model
            model_root.mkdir()
            np.savez_compressed(model_root / "initial-context.npz", initial=initial[:, 0], initial_rate=initial_rate[:, 0], mapping=reference["mapping"], signature=reference["signature"], core=core, tail_slots=tail_slots, low_slots=low_slots, old_normalization=normalization, tail_units=tail_units)
            write(model_root / "capture-check.json", dict(single_capture=True, prefix_points=len(prefix), captured_time=float(initial_time[0]), authorized_last_time=float(times[-1]), exact_state=True, exact_rate=True, exact_observer=True, exact_signature=True, future_reference_evolution_recomputed=False, source_sha256=digest(source_path), initial_owner_sha256=digest(old_folder / "native-reference.npz")))
            def original_rhs(stamp, vector):
                vector = np.ascontiguousarray(vector, dtype=np.float64)
                rate = np.empty(dimension)
                lib.mts_operator_rhs(float(stamp), dimension, pointer(vector), pointer(rate))
                return rate
            def observe(stamp, vector):
                vector = np.ascontiguousarray(vector, dtype=np.float64)
                values = np.empty(len(names))
                lib.mts_operator_observe(float(stamp), dimension, pointer(vector), len(names), pointer(values))
                return values
            def kinetic(stamp):
                scale = np.empty(1)
                speeds = np.empty(5)
                lib.mts_operator_kinetic(float(stamp), 5, pointer(scale), pointer(speeds))
                return float(scale[0]), speeds

            def stress(stamp, vector):
                vector = np.ascontiguousarray(vector, dtype=np.float64)
                terms = np.zeros((7, 7), order="F")
                metadata = np.zeros(25)
                lib.mts_operator_stress(float(stamp), dimension, pointer(vector), pointer(terms), pointer(metadata))
                return terms.T.copy(), metadata
            cases = []
            saved_owner = next(row for row in coupled_owner["reports"] if row["model"] == model)
            indices = np.unique(np.linspace(1, len(times) - 2, 9, dtype=int))
            indices = indices[(times[indices] - times[0] > max(STEPS)) & (times[-1] - times[indices] > max(STEPS))]
            require(len(indices) >= 7, "directional check coverage")
            for tag in TAGS:
                guard()
                case_owner = next(row for row in saved_owner["cases"] if row["tag"] == tag)
                source = CLOSURE / "runs" / model / case_owner["file"]
                require(digest(source) == case_owner["sha256"], "saved coupled state changed")
                packet = load(source)
                require(np.array_equal(packet["times"], times), "unchanged saved phase grid")
                terms_rows, meta_rows, base_rows = [], [], []
                for sample, (stamp, vector) in enumerate(zip(times, packet["projected_state"])):
                    if sample % 512 == 0:
                        guard()
                    terms, metadata = stress(stamp, vector)
                    terms_rows.append(terms)
                    meta_rows.append(metadata)
                    base_rows.append(observe(stamp, vector))
                base_rows = np.array(base_rows)
                observer_error = float(np.max(np.max(abs(base_rows - packet["observer"]), axis=0) / np.maximum(np.max(abs(packet["observer"]), axis=0), 1e-80)))
                require(observer_error < ALGEBRA, "original observer changed")
                directional, scale_rates = [], []
                for index in indices:
                    stamp, vector = times[index], packet["projected_state"][index]
                    derivative = original_rhs(stamp, vector)
                    derivatives, scale_derivatives = [], []
                    for step in STEPS:
                        plus, plus_meta = stress(stamp + step, vector + step * derivative)
                        minus, minus_meta = stress(stamp - step, vector - step * derivative)
                        derivatives.append((plus[:, :2] - minus[:, :2]) / (2 * step))
                        scale_derivatives.append((plus_meta[0] - minus_meta[0]) / (2 * step))
                    directional.append(derivatives)
                    scale_rates.append(scale_derivatives)
                path = model_root / (tag + "-stress.npz")
                np.savez_compressed(path, times=times, terms=np.array(terms_rows), metadata=np.array(meta_rows), observer=base_rows, observer_names=packet["observer_names"],
                                    derivative_indices=indices, difference_steps=STEPS, directional=np.array(directional), scale_rates=np.array(scale_rates),
                                    species=np.array(["cdm", "baryon", "photon", "massless", "massive_neutrino", "slow_scalar", "heavy_scalar"]),
                                    term_names=np.array(["D_sync", "Q_sync", "P_sync", "D_sync_rate", "Q_sync_rate", "enthalpy", "Pi"]))
                record = dict(tag=tag, file=path.name, sha256=digest(path), source_file=str(source), source_sha256=digest(source), points=len(times), derivative_probes=len(indices), old_observer_error=observer_error, original_solver=case_owner)
                cases.append(record)
                write(model_root / (tag + "-stress.json"), record)
                print(model, tag, "read", len(times), "states; observer error", observer_error, flush=True)
                del packet, terms_rows, meta_rows, base_rows
            report = dict(model=model, cases=cases, initial_context_sha256=digest(model_root / "initial-context.npz"), capture_sha256=digest(model_root / "capture-check.json"), initial_reference_sha256=digest(old_folder / "native-reference.npz"), no_new_trajectory=True)
            reports.append(report)
            write(model_root / "result.json", report)
            lib.mts_capture_reset()
            del native, output
    except BaseException as error:
        failure = repr(error)
        raise
    finally:
        flags["step"].value = flags["tangent"].value = 0
        lib.mts_capture_reset()
        write(ROOT / "readout-result.json", dict(state="complete" if failure is None and len(reports) == 2 else "failed", error=failure, reports=reports, source_sha256=digest(__file__), config_sha256=digest(ROOT / "readout-config.json"), build_sha256=digest(ROOT / "build/build-result.json"), coupled_owner_sha256=digest(CLOSURE / "prediction-result.json"), no_new_trajectory=True))


if __name__ == "__main__":
    main()
