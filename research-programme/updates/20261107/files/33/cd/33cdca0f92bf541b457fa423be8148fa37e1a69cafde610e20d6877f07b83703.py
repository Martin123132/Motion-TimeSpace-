import ast
import ctypes
import os
import sys
import time
from datetime import datetime, timezone
from common import ROOT, PRIOR, PAIRED, SOURCE, HIERARCHY, NATIVE, BRANCH, EARLY, WAVE, ALGEBRA, modest, guard, check_prior, require, read, write, digest, load, BACKGROUND, CLOSURE, GATE
import numpy as np
from scipy.integrate import solve_ivp

POINTER = ctypes.POINTER(ctypes.c_double)
INTEGER_POINTER = ctypes.POINTER(ctypes.c_int)
CASES = [("L16-base", 16, False, 2e-11, 1.), ("L64-base", 64, False, 2e-11, 1.),
         ("L64-fine", 64, False, 2e-12, 1.), ("L128-base", 128, False, 2e-11, 1.),
         ("L128-fine", 128, False, 2e-12, 1.), ("G192-fine", 192, True, 2e-12, 1.),
         ("L64-zero", 64, False, 2e-11, 0.), ("L64-negative", 64, False, 2e-11, -1.)]


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

    lib.mts_dense_load.argtypes = [ctypes.c_int, POINTER, POINTER, POINTER, POINTER, POINTER, POINTER, ctypes.c_double]
    lib.mts_dense_load.restype = None
    lib.mts_dense_mode.argtypes, lib.mts_dense_mode.restype = [ctypes.c_int], None
    lib.mts_dense_point.argtypes, lib.mts_dense_point.restype = [ctypes.c_double, POINTER], None
    lib.mts_operator_stress.argtypes, lib.mts_operator_stress.restype = [ctypes.c_double, ctypes.c_int, POINTER, POINTER, POINTER], None
    lib.mts_bridge_thermal_read.argtypes, lib.mts_bridge_thermal_read.restype = [ctypes.c_double, POINTER], None
    lib.mts_bridge_thermal_rebuild.argtypes, lib.mts_bridge_thermal_rebuild.restype = [], None

    native_names = list(camb.model.evolve_names)
    owner_result = read(SOURCE / "phase-resolved/tangent-native-result.json")
    hierarchy_owner = read(HIERARCHY / "hierarchy-balanced-result.json")
    destination = ROOT / "checks"
    destination.mkdir(exist_ok=False)
    write(ROOT / "check-config.json", dict(source_sha256=digest(__file__), protocol_sha256=digest(ROOT / "PROTOCOL.md"), cases=CASES, created_utc=datetime.now(timezone.utc).isoformat(), scope="isolated pointwise bridge; reused amplitudes; thermal sensitivity, not new perturbation evolution"))
    reports, failure = [], None
    try:
        for model in ("heavy", "cold"):
            guard()
            lib.mts_dense_mode(0)
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

            old_operator_errors = []
            for index, stamp in enumerate(audit["times"]):
                guard()
                matrix = np.column_stack([original_rhs(stamp, basis) for basis in np.eye(dimension)])
                old_operator_errors.append(row_error(matrix, audit["matrices"][index]))
            require(max(old_operator_errors) < ALGEBRA, "disabled bridge changed original operator")
            dense_path = BACKGROUND / "runs" / model / "dop-half-cap.npz"
            dense = load(dense_path)
            supplied = load(BACKGROUND / "inputs" / (model + "-input.npz"))
            require(str(dense["method"]) == "DOP853", "dense polynomial kind")
            starts = np.ascontiguousarray(dense["segment_start"])
            ends = np.ascontiguousarray(dense["segment_end"])
            coefficients = np.asfortranarray(dense["coefficients"].transpose(2, 1, 0))
            segment_initial = np.asfortranarray(dense["segment_initial"].T)
            units = np.ascontiguousarray(dense["units"])
            anchors = np.ascontiguousarray(dense["initial_fields"])
            lib.mts_dense_load(len(starts), pointer(starts), pointer(ends), pointer(segment_initial),
                               pointer(coefficients), pointer(units), pointer(anchors), float(supplied["initial_time"]))
            lib.mts_operator_window(float(dense["times"][-1]), saved_signature.ctypes.data_as(INTEGER_POINTER))
            def point(efold):
                values = np.empty(12)
                lib.mts_dense_point(float(efold), pointer(values))
                return values
            def thermal(stamp):
                values = np.empty(6)
                lib.mts_bridge_thermal_read(float(stamp), pointer(values))
                return values
            def stress(stamp, vector):
                vector = np.ascontiguousarray(vector, dtype=np.float64)
                terms = np.zeros((7, 7), order="F")
                metadata = np.zeros(25)
                lib.mts_operator_stress(float(stamp), dimension, pointer(vector), pointer(terms), pointer(metadata))
                return terms.T.copy(), metadata
            probe_indices = np.unique(np.linspace(0, len(times)-1, 65, dtype=int))
            efolds = dense["efold"][probe_indices]
            records = np.array([point(efold) for efold in efolds])
            expected = np.column_stack([dense["normalized"][probe_indices] * units,
                                        dense["normalized_derivative"][probe_indices] * units,
                                        dense["a"][probe_indices], dense["times"][probe_indices]])
            dense_error = float(np.max(abs(records - expected) / np.maximum(np.max(abs(expected), axis=0), 1e-80)))
            require(dense_error < ALGEBRA, "dense transport mismatch")
            original_thermal = np.array([thermal(point(efold)[11]) for efold in efolds])
            def sample():
                rows, meta, observed, thermal_rows, rates, speeds = [], [], [], [], [], []
                for sample_index, efold in zip(probe_indices, efolds):
                    guard()
                    current = point(efold)
                    stamp = current[11]
                    state = reference["state"][sample_index]
                    terms, metadata = stress(stamp, state)
                    rows.append(terms)
                    meta.append(metadata)
                    observed.append(observe(stamp, state))
                    thermal_rows.append(thermal(stamp))
                    rates.append(original_rhs(stamp, state))
                    speeds.append(kinetic(stamp)[1])
                return dict(terms=np.array(rows), metadata=np.array(meta), observer=np.array(observed),
                            thermal=np.array(thermal_rows), rates=np.array(rates), speeds=np.array(speeds))
            initial_bridge = sample()
            lib.mts_dense_mode(0)
            lib.mts_bridge_thermal_rebuild()
            control_thermal = np.array([thermal(point(efold)[11]) for efold in efolds])
            lib.mts_dense_mode(1)
            lib.mts_bridge_thermal_rebuild()
            repaired = sample()
            updated_thermal = repaired["thermal"]
            thermal_scale = np.maximum(np.max(abs(original_thermal[:, 3:]), axis=0), 1e-80)
            thermal_control = np.max(abs(control_thermal[:, 3:] - original_thermal[:, 3:]), axis=0) / thermal_scale
            thermal_change = np.max(abs(updated_thermal[:, 3:] - control_thermal[:, 3:]), axis=0) / thermal_scale
            mapping_error = float(np.max(abs(updated_thermal[:, 0] - updated_thermal[:, 2]) / updated_thermal[:, 0]))
            hubble_error = float(np.max(abs(repaired["observer"][:, 28] - dense["H"][probe_indices])) / np.max(dense["H"][probe_indices]))
            require(max(mapping_error, hubble_error) < ALGEBRA, "inconsistent source background or scale factor")
            density, flux, pressure, density_rate, flux_rate, enthalpy, shear = [repaired["terms"][:, :, index] for index in range(7)]
            meta = repaired["metadata"]
            hubble, metric_z = meta[:, 1, None], meta[:, 2, None]
            c_terms = np.array([density_rate, hubble*(density+3*pressure), WAVE*flux, WAVE*metric_z*enthalpy])
            e_terms = np.array([flux_rate, 2*hubble*flux, -WAVE*pressure, 2*WAVE/3*shear])
            residual_c, residual_e = c_terms.sum(axis=0), e_terms.sum(axis=0)
            predicted_c = np.zeros_like(residual_c)
            predicted_e = np.zeros_like(residual_e)
            predicted_c[:, 1] = 3*hubble[:, 0]*pressure[:, 1]
            predicted_c[:, 4] = WAVE*metric_z[:, 0]*(enthalpy[:, 4]-meta[:, 3])
            field_checks = []
            for species, offset in ((5, 4), (6, 14)):
                field, velocity, field_rate, velocity_rate, mass, delta, delta_rate = [meta[:, offset + index] for index in range(7)]
                field_defect = field_rate - velocity
                velocity_defect = velocity_rate+2*hubble[:, 0]*velocity+(meta[:, 0]*mass)**2*field
                predicted_c[:, species] = velocity_defect*delta_rate+(meta[:, 0]*mass)**2*field_defect*delta
                predicted_e[:, species] = WAVE*velocity_defect*delta
                field_checks.append(dict(kinematic=float(np.max(abs(field_defect))/max(np.max(abs(velocity)),1e-80)),
                                         dynamic=float(np.max(abs(velocity_defect))/max(np.max(abs(velocity_rate)),np.max(abs(2*hubble[:,0]*velocity)),np.max(abs((meta[:,0]*mass)**2*field)),1e-80))))
            scale_c = max(float(np.max(abs(c_terms.sum(axis=2)))), 1e-80)
            scale_e = max(float(np.max(abs(e_terms.sum(axis=2)))), 1e-80)
            continuity = float(np.max(abs(residual_c.sum(axis=1)))/scale_c)
            momentum = float(np.max(abs(residual_e.sum(axis=1)))/scale_e)
            algebra_c = float(np.max(abs((residual_c-predicted_c).sum(axis=1)))/scale_c)
            algebra_e = float(np.max(abs((residual_e-predicted_e).sum(axis=1)))/scale_e)
            scalar_c = float(np.max(abs(residual_c[:, 5:].sum(axis=1)))/scale_c)
            source_checks = {
                "density": float(np.max(abs(density.sum(axis=1)-repaired["observer"][:, 2]))/max(np.max(abs(repaired["observer"][:, 2])),1e-80)),
                "flux": float(np.max(abs(flux.sum(axis=1)-repaired["observer"][:, 3]))/max(np.max(abs(repaired["observer"][:, 3])),1e-80)),
                "shear": float(np.max(abs(shear.sum(axis=1)-repaired["observer"][:, 4]))/max(np.max(abs(repaired["observer"][:, 4])),1e-80)),
                "enthalpy": float(np.max(abs(enthalpy.sum(axis=1)-repaired["observer"][:, 0]-repaired["observer"][:, 1]))/np.max(abs(repaired["observer"][:, 0]+repaired["observer"][:, 1])))}
            midpoint = len(efolds)//2
            current = point(efolds[midpoint])
            test_vector = np.sin(np.arange(1, dimension+1))*normalization
            response = original_rhs(current[11], test_vector)
            linearity = float(np.max(abs(response+original_rhs(current[11], -test_vector)))/max(np.max(abs(response)),1e-80))
            zero = bool(np.count_nonzero(original_rhs(current[11], np.zeros(dimension))) == 0)
            matrix = np.column_stack([original_rhs(current[11], basis) for basis in np.eye(dimension)])
            closure_diagonal = matrix[tail_slots[-1], tail_slots[-1]]
            closure_error = float(np.max(abs(closure_diagonal+17/current[11]))/(17/current[11]))
            speed_error = float(np.max(abs(matrix[tail_slots[0], low_slots]/(3*WAVE/7)-kinetic(current[11])[1])))
            directional = []
            differences = []
            difference_steps = (2e-7,1e-7,5e-8)
            selected = range(4, len(efolds)-4, 8)
            for local_index in selected:
                efold = efolds[local_index]
                current = point(efold)
                stamp = current[11]
                vector = reference["state"][probe_indices[local_index]]
                derivative = original_rhs(stamp, vector)
                direct = repaired["terms"][local_index, :, 3:5].sum(axis=0)
                numerical = []
                for step in difference_steps:
                    plus = point(efold+step)
                    plus_terms, _ = stress(plus[11], vector+(plus[11]-stamp)*derivative)
                    minus = point(efold-step)
                    minus_terms, _ = stress(minus[11], vector+(minus[11]-stamp)*derivative)
                    numerical.append((plus_terms[:, :2].sum(axis=0)-minus_terms[:, :2].sum(axis=0))/(plus[11]-minus[11]))
                directional.append(numerical)
                differences.append(direct)
            directional = np.array(directional)
            direct = np.array(differences)
            rate_scale = np.maximum(np.max(abs(repaired["terms"][:, :, 3:5].sum(axis=1)),axis=0),1e-80)
            richardson = (4*directional[:,1:]-directional[:,:-1])/3
            directional_errors = np.max(abs(richardson-direct[:,None,:]),axis=0)/rate_scale
            original_rate = initial_bridge["rates"]
            thermal_rate_change = float(np.max(np.max(abs(repaired["rates"]-original_rate),axis=0)/np.maximum(np.max(abs(original_rate),axis=0),1e-80)))
            checks = dict(dense_transport=dense_error, unchanged_operator=max(old_operator_errors), source_hubble=hubble_error,
                          thermal_inverse=mapping_error, continuity_decomposition=algebra_c, momentum_decomposition=algebra_e,
                          source_decomposition=source_checks, linearity=linearity, zero=zero, physical_closure=closure_error, physical_speeds=speed_error,
                          directional_errors=directional_errors.tolist(), canonical_fields=field_checks,
                          raw_continuity=continuity, raw_momentum=momentum, scalar_continuity=scalar_c,
                          thermal_control=thermal_control.tolist(), thermal_changed=thermal_change.tolist(), thermal_rhs_change=thermal_rate_change)
            algebra_pass = max(dense_error,max(old_operator_errors),hubble_error,mapping_error,algebra_c,algebra_e,
                               *source_checks.values(),linearity,closure_error,speed_error) < ALGEBRA and zero
            numerical_pass = max(continuity,momentum,float(np.max(directional_errors[-1])),*thermal_control,*thermal_change,
                                 *[value for field in field_checks for value in field.values()]) < GATE
            path = model_root / "bridge-checks.npz"
            np.savez_compressed(path, efold=efolds, indices=probe_indices, dense=records, expected_dense=expected,
                                terms=repaired["terms"], metadata=meta, observer=repaired["observer"], rates=repaired["rates"],
                                original_thermal=original_thermal, control_thermal=control_thermal, repaired_thermal=updated_thermal,
                                initial_bridge_rates=original_rate, continuity_terms=c_terms,momentum_terms=e_terms,
                                predicted_c=predicted_c,predicted_e=predicted_e,directional=directional,direct=direct,
                                repaired_operator=matrix)
            report = dict(model=model, passed=bool(algebra_pass and numerical_pass), checks=checks, dense_input_sha256=digest(dense_path),
                          packet=str(path), packet_sha256=digest(path), point_count=len(efolds), no_new_perturbation_trajectory=True,
                          thermal_scope="full native thermal rebuild with local scalar override; compare only inside declared a interval",
                          output_scope="30 metric/stress observables; no new line-of-sight spectra")
            reports.append(report)
            write(model_root / "result.json", report)
            print(model, report, flush=True)
            lib.mts_dense_mode(0)
            del native
    except BaseException as error:
        failure = repr(error)
        raise
    finally:
        result = dict(state="failed" if failure else "complete", passed=bool(failure is None and len(reports)==2 and all(row["passed"] for row in reports)),
                      error=failure,reports=reports,source_sha256=digest(__file__),build_sha256=digest(ROOT/"build/build-result.json"),
                      background_closeout_sha256=digest(BACKGROUND/"closeout.json"),gate=GATE,algebra_gate=ALGEBRA,
                      no_new_perturbation_evolution=True)
        write(ROOT/"check-result.json", result)
        print(dict(state=result["state"],passed=result["passed"]),flush=True)


if __name__ == "__main__":
    main()

