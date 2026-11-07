import ast
import ctypes
import os
import sys
import time
from datetime import datetime, timezone
from common import ROOT, SOURCE, PRIOR, BRANCH, EARLY, NATIVE, modest, guard, require, read, write, digest
import numpy as np
from scipy.integrate import solve_ivp

POINTER = ctypes.POINTER(ctypes.c_double)


def ptr(values):
    return values.ctypes.data_as(POINTER)


def ratio(left, right):
    return float(np.max(abs(left - right) / np.maximum(np.max(abs(right), axis=0), 1e-30)))


def main():
    modest()
    build_root = ROOT / "build-corrected"
    build = read(build_root / "build-result.json")
    require(build["state"] == "complete" and digest(build_root / "native/camb/cambdll.dll") == build["dll_sha256"], "adapter ownership")
    sys.path.insert(0, str(build_root / "native"))
    import camb
    from camb.mts import MTSTwoField
    sys.path.append(str(BRANCH / "radiation-and-slow-field-transfer-20261007"))
    import radiation_common
    owner = NATIVE.parent / "matching_common.py"
    factory = next(node for node in ast.parse(owner.read_text()).body if isinstance(node, ast.FunctionDef) and node.name == "params_for")
    namespace = dict(np=np, previous=radiation_common, MTSTwoField=MTSTwoField)
    exec(compile(ast.Module(body=[factory], type_ignores=[]), str(owner), "exec"), namespace)
    lib = camb.baseconfig.camblib
    observer_dll = ctypes.CDLL(str(PRIOR / "observer.dll"))
    source_function = ctypes.cast(observer_dll.source_func_, ctypes.c_void_p)
    flags = {name: ctypes.c_int.in_dll(lib, "mts_probe_" + name) for name in ("step", "kind", "count", "tangent")}
    capture = {name: ctypes.c_int.in_dll(lib, "mts_capture_" + name) for name in ("begin", "end", "count", "dimension", "native_dimension", "selector")}
    epsilon = ctypes.c_double.in_dll(lib, "mts_probe_epsilon")
    mapping = (ctypes.c_int * 512).in_dll(lib, "mts_capture_map")
    signature = (ctypes.c_int * 96).in_dll(lib, "mts_capture_signature")
    lib.mts_capture_reset.argtypes = []
    lib.mts_capture_reset.restype = None
    lib.mts_capture_copy.argtypes = [ctypes.c_int, ctypes.c_int, POINTER, POINTER, POINTER]
    lib.mts_capture_copy.restype = None
    lib.mts_operator_rhs.argtypes = [ctypes.c_double, ctypes.c_int, POINTER, POINTER]
    lib.mts_operator_rhs.restype = None
    lib.mts_operator_observe.argtypes = [ctypes.c_double, ctypes.c_int, POINTER, ctypes.c_int, POINTER]
    lib.mts_operator_observe.restype = None
    names = list(camb.model.evolve_names)
    owner_result = read(SOURCE / "phase-resolved/tangent-native-result.json")
    destination = ROOT / "runs"
    destination.mkdir(exist_ok=False)
    reports, error = [], None
    write(ROOT / "run-config.json", dict(source_sha256=digest(__file__), protocol_sha256=digest(ROOT / "PROTOCOL.md"), state_cases=[["full", 2e-11, 1.], ["precision", 2e-12, 1.], ["zero", 2e-11, 0.], ["negative", 2e-11, -1.]], kernel_release_fractions=[0., .25, .5], kernel_tolerances=[2e-11, 2e-12], numerical_gate=2e-5, algebra_gate=1e-10, dynamic_scale="max(abs(initial_i), max(abs(initial))*1e-20, 1e-30); no future states used to set solver units"))
    try:
        for model in ("heavy", "cold"):
            guard()
            row = next(item for item in owner_result["reports"] if item["model"] == model and item["tag"] == "one")
            path = SOURCE / "phase-resolved/packets" / row["file"]
            require(digest(path) == row["sha256"], "reference owner")
            with np.load(path) as archive:
                full_times = np.ascontiguousarray(archive["full_times"])
                first, last = int(archive["original_indices"][0]), int(archive["original_indices"][-1])
                probes = archive["original_indices"] - first
                reference_observer = archive["full_observer"][first:last + 1].copy()
                observer_names = archive["observer_names"].tolist()
            params = namespace["params_for"](EARLY / f"runs/backgrounds/{model}.npz")
            native = camb.get_background(params)
            native.Params.Accuracy.IntTolBoost = 6
            native.Params.Accuracy.lAccuracyBoost = 4
            lib.mts_capture_reset()
            flags["step"].value = first + 1
            flags["kind"].value = 1 if model == "heavy" else 2
            flags["count"].value = 0
            flags["tangent"].value = 1
            epsilon.value = 1.
            capture["begin"].value, capture["end"].value = first + 1, last + 1
            count = len(names) + len(observer_names)
            output = np.zeros((1, len(full_times), count))
            code = camb.results.CAMB_TimeEvolution(ctypes.byref(native), ctypes.byref(ctypes.c_int(1)), np.array([5.]), ctypes.byref(ctypes.c_int(len(full_times))), full_times, ctypes.byref(ctypes.c_int(count)), output, ctypes.byref(ctypes.c_int(len(observer_names))), ctypes.byref(source_function))
            require(code == 0, "native capture")
            captured_observer = output[0, first:last + 1, len(names):].copy()
            overlap = ratio(captured_observer, reference_observer)
            require(overlap < 2e-5, "adapter capture changed original source")
            dimension, snapshots = capture["dimension"].value, capture["count"].value
            require(snapshots == last - first + 1 and 0 < dimension <= 512, "capture completeness")
            captured = np.zeros((dimension, snapshots), order="F")
            captured_rate = np.zeros_like(captured, order="F")
            times = np.zeros(snapshots)
            lib.mts_capture_copy(dimension, snapshots, ptr(captured), ptr(captured_rate), ptr(times))
            require(np.array_equal(times, full_times[first:last + 1]), "capture times")
            state_map = np.array(list(mapping)[:dimension])
            regime = np.array(list(signature))
            selector = capture["selector"].value
            require(selector not in state_map and len(np.unique(state_map)) == dimension, "discrete selector excluded")
            reference = np.ascontiguousarray(captured.T)
            rates = np.ascontiguousarray(captured_rate.T)
            initial = reference[0].copy()
            normalization = np.maximum(abs(initial), max(float(np.max(abs(initial))) * 1e-20, 1e-30))
            selected_native = [2] + ([int(regime[2]) + 2, int(regime[2]) + 3] if model == "heavy" else [])
            selected = np.array([int(np.flatnonzero(state_map == index)[0]) for index in selected_native])
            remaining = np.array([index for index in range(dimension) if index not in selected])
            require(np.count_nonzero(initial[remaining]) == 0, "nonzero preparation outside selected direction")
            model_root = destination / model
            model_root.mkdir()
            np.savez_compressed(model_root / "native-reference.npz", times=times, state=reference, derivative=rates, observer=captured_observer, observer_names=np.array(observer_names), mapping=state_map, signature=regime, selected=selected, remaining=remaining, initial=initial, normalization=normalization, probes=probes)

            def rhs(stamp, vector):
                vector = np.ascontiguousarray(vector, dtype=np.float64)
                result = np.empty(dimension)
                lib.mts_operator_rhs(float(stamp), dimension, ptr(vector), ptr(result))
                return result

            def observe(stamp, vector):
                vector = np.ascontiguousarray(vector, dtype=np.float64)
                result = np.empty(len(observer_names))
                lib.mts_operator_observe(float(stamp), dimension, ptr(vector), len(observer_names), ptr(result))
                return result

            matrix_times = np.linspace(times[0], times[-1], 9)
            matrices, linearity = [], []
            for stamp in matrix_times:
                guard()
                matrix = np.column_stack([rhs(stamp, basis) for basis in np.eye(dimension)])
                vector = np.sin(np.arange(1, dimension + 1)) / (1 + np.arange(dimension))
                second = np.cos(np.arange(1, dimension + 1)) / (2 + np.arange(dimension))
                direct = rhs(stamp, vector)
                checks = [float(np.max(abs(rhs(stamp, np.zeros(dimension))))), ratio(matrix @ vector, direct), ratio(rhs(stamp, -vector), -direct), ratio(rhs(stamp, vector + second), direct + rhs(stamp, second)), ratio(rhs(stamp, .5 * vector), .5 * direct)]
                require(max(checks) < 1e-10, "operator linearity")
                matrices.append(matrix)
                linearity.append(checks)
            readback = np.array([observe(times[index], reference[index]) for index in probes])
            observer_replay = ratio(readback, captured_observer[probes])
            require(observer_replay < 1e-10, "operator observer ownership")
            derivative_replay = ratio(np.array([rhs(times[index], reference[index]) for index in probes]), rates[probes])
            require(derivative_replay < 1e-10, "frozen regime derivative ownership")
            np.savez_compressed(model_root / "operator-audit.npz", times=matrix_times, matrices=np.array(matrices), linearity=np.array(linearity), selected=selected, remaining=remaining)
            case_reports = []
            last_guard = time.monotonic()

            def normalized_rhs(stamp, normalized):
                nonlocal last_guard
                if time.monotonic() - last_guard > 2:
                    guard()
                    last_guard = time.monotonic()
                return rhs(stamp, normalized * normalization) / normalization

            for tag, tolerance, amplitude in (("full", 2e-11, 1.), ("precision", 2e-12, 1.), ("zero", 2e-11, 0.), ("negative", 2e-11, -1.)):
                guard()
                started = time.monotonic()
                solution = solve_ivp(normalized_rhs, (times[0], times[-1]), amplitude * initial / normalization, method="DOP853", rtol=tolerance, atol=tolerance / 100, t_eval=times)
                require(solution.success and np.isfinite(solution.y).all(), "independent hierarchy integration")
                prediction = solution.y.T * normalization
                predicted_observer = np.array([observe(times[index], prediction[index]) for index in probes])
                np.savez_compressed(model_root / (tag + ".npz"), times=times, state=prediction, observer=predicted_observer, probes=probes)
                case = dict(tag=tag, rtol=tolerance, amplitude=amplitude, evaluations=solution.nfev, seconds=time.monotonic() - started, file=tag + ".npz", sha256=digest(model_root / (tag + ".npz")))
                case_reports.append(case)
                write(model_root / (tag + ".json"), case)
                print(model, tag, "complete", dimension, case["seconds"], flush=True)
            kernels = []
            for release_fraction in (0., .25, .5):
                release = times[0] + release_fraction * (times[-1] - times[0])
                initial_columns = np.column_stack([rhs(release, np.eye(dimension)[index])[remaining] for index in selected])
                retained_times = np.unique(np.r_[release, times[times >= release]])
                for tolerance in (2e-11, 2e-12):
                    guard()
                    kernel_scale = max(float(np.max(abs(initial_columns))), 1e-30)
                    def kernel_rhs(stamp, flattened):
                        nonlocal last_guard
                        if time.monotonic() - last_guard > 2:
                            guard()
                            last_guard = time.monotonic()
                        columns = flattened.reshape(len(remaining), len(selected)) * kernel_scale
                        derivative = np.empty_like(columns)
                        for index in range(len(selected)):
                            vector = np.zeros(dimension)
                            vector[remaining] = columns[:, index]
                            derivative[:, index] = rhs(stamp, vector)[remaining]
                        return (derivative / kernel_scale).ravel()
                    solution = solve_ivp(kernel_rhs, (release, times[-1]), (initial_columns / kernel_scale).ravel(), method="DOP853", rtol=tolerance, atol=tolerance / 100, t_eval=retained_times)
                    require(solution.success and np.isfinite(solution.y).all(), "retarded column integration")
                    columns = solution.y.T.reshape(-1, len(remaining), len(selected)) * kernel_scale
                    selected_probes = np.unique(np.r_[0, np.searchsorted(retained_times, times[probes][times[probes] >= release]), len(retained_times) - 1])
                    kernel = []
                    for point in selected_probes:
                        projected = []
                        for index in range(len(selected)):
                            vector = np.zeros(dimension)
                            vector[remaining] = columns[point, :, index]
                            projected.append(rhs(retained_times[point], vector)[selected])
                        kernel.append(np.column_stack(projected))
                    tag = "kernel-" + str(int(100 * release_fraction)) + ("-fine" if tolerance < 1e-11 else "-base")
                    np.savez_compressed(model_root / (tag + ".npz"), times=retained_times[selected_probes], kernel=np.array(kernel), initial_columns=initial_columns, final_columns=columns[-1], release=release, selected=selected, remaining=remaining, state_map=state_map)
                    item = dict(tag=tag, release_fraction=release_fraction, release=release, rtol=tolerance, evaluations=solution.nfev, file=tag + ".npz", sha256=digest(model_root / (tag + ".npz")))
                    kernels.append(item)
                    write(model_root / (tag + ".json"), item)
                    print(model, tag, "complete", flush=True)
            report = dict(model=model, dimension=dimension, native_dimension=capture["native_dimension"].value, selector=selector, regime=regime.tolist(), mapping=state_map.tolist(), selected_native=selected_native, selected_dynamic=selected.tolist(), remaining_initial_zero=True, snapshots=snapshots, adapter_overlap=overlap, operator_observer_error=observer_replay, operator_derivative_error=derivative_replay, maximum_linearity_error=float(np.max(linearity)), cases=case_reports, kernels=kernels, reference_owner=row["sha256"], captured_reference_sha256=digest(model_root / "native-reference.npz"), operator_audit_sha256=digest(model_root / "operator-audit.npz"))
            reports.append(report)
            write(model_root / "result.json", report)
            lib.mts_capture_reset()
            del native
    except BaseException as failure:
        error = repr(failure)
        raise
    finally:
        flags["step"].value = flags["tangent"].value = 0
        lib.mts_capture_reset()
        write(ROOT / "hierarchy-result.json", dict(state="complete" if error is None and len(reports) == 2 else "failed", error=error, pid=os.getpid(), finished=datetime.now(timezone.utc).isoformat(), reports=reports, source_sha256=digest(__file__), config_sha256=digest(ROOT / "run-config.json"), build_sha256=digest(build_root / "build-result.json"), background_only_operator=True, future_species_histories_supplied=False, inherited_hierarchy_approximations_retained=True))


if __name__ == "__main__":
    main()

