import ast
import ctypes
import os
import sys
import time
from datetime import datetime, timezone
from common import ROOT, PRIOR, PAIRED, SOURCE, HIERARCHY, NATIVE, BRANCH, EARLY, WAVE, ALGEBRA, modest, guard, check_prior, require, read, write, digest, load, BACKGROUND, ADAPTER, COUPLED
import numpy as np
from scipy.integrate import solve_ivp

POINTER = ctypes.POINTER(ctypes.c_double)
INTEGER_POINTER = ctypes.POINTER(ctypes.c_int)
CASES = [("L64-base",64,False,2e-11,1.,"dop-half-cap"),
         ("L64-fine",64,False,2e-12,1.,"dop-half-cap"),
         ("L128-base",128,False,2e-11,1.,"dop-half-cap"),
         ("L128-fine",128,False,2e-12,1.,"dop-half-cap"),
         ("G192-fine",192,True,2e-12,1.,"dop-half-cap"),
         ("L64-zero",64,False,2e-11,0.,"dop-half-cap"),
         ("L64-negative",64,False,2e-11,-1.,"dop-half-cap"),
         ("L128-background-fine",128,False,2e-12,1.,"dop-fine")]


def pointer(values):
    return values.ctypes.data_as(POINTER)


def row_error(left, right):
    return float(np.max(abs(left - right) / np.maximum(np.max(abs(right), axis=1, keepdims=True), 1e-80)))


def main():
    modest()
    require(len(CASES)==8 and all(len(case)==6 for case in CASES), "case schema")
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

    lib.mts_dense_load.argtypes, lib.mts_dense_load.restype = [ctypes.c_int, POINTER, POINTER, POINTER, POINTER, POINTER, POINTER, ctypes.c_double], None
    lib.mts_dense_mode.argtypes, lib.mts_dense_mode.restype = [ctypes.c_int], None
    lib.mts_evolution_point.argtypes, lib.mts_evolution_point.restype = [ctypes.c_double, POINTER], None
    lib.mts_operator_stress.argtypes, lib.mts_operator_stress.restype = [ctypes.c_double, ctypes.c_int, POINTER, POINTER, POINTER], None
    lib.mts_bridge_thermal_rebuild.argtypes, lib.mts_bridge_thermal_rebuild.restype = [], None

    native_names = list(camb.model.evolve_names)
    owner_result = read(SOURCE / "phase-resolved/tangent-native-result.json")
    hierarchy_owner = read(HIERARCHY / "hierarchy-balanced-result.json")
    destination = ROOT / "runs-configured"
    destination.mkdir(exist_ok=False)
    write(ROOT / "run-configured.json", dict(source_sha256=digest(__file__), protocol_sha256=digest(ROOT / "PROTOCOL.md"), cases=CASES, created_utc=datetime.now(timezone.utc).isoformat(), scaling="prior initial-operator core units; maximum prior per-node unit for every extended angular moment; no future states", no_future_perturbation_history_supplied=True))
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

            operator_errors = []
            for index, stamp in enumerate(audit["times"]):
                guard()
                matrix = np.column_stack([original_rhs(stamp, basis) for basis in np.eye(dimension)])
                operator_errors.append(row_error(matrix, audit["matrices"][index]))
            require(max(operator_errors) < ALGEBRA, "disabled original operator changed")
            supplied = load(BACKGROUND / "inputs" / (model + "-input.npz"))
            efolds = supplied["efold"]
            max_step = float(supplied["step_cap"])/2
            old_first_step = float(read(old_folder / "initial-step.json")["first_step"])
            def point(efold):
                values = np.empty(13)
                lib.mts_evolution_point(float(efold),pointer(values))
                return values
            def stress(stamp, vector):
                vector = np.ascontiguousarray(vector,dtype=np.float64)
                terms, metadata = np.zeros((7,7),order="F"), np.zeros(25)
                lib.mts_operator_stress(float(stamp),dimension,pointer(vector),pointer(terms),pointer(metadata))
                return terms.T.copy(),metadata
            def activate_background(tag):
                packet = load(BACKGROUND / "runs" / model / (tag+".npz"))
                require(np.array_equal(packet["efold"],efolds), "physical grid changed")
                starts, ends = np.ascontiguousarray(packet["segment_start"]),np.ascontiguousarray(packet["segment_end"])
                initial = np.asfortranarray(packet["segment_initial"].T)
                coefficients = np.asfortranarray(packet["coefficients"].transpose(2,1,0))
                units, fields = np.ascontiguousarray(packet["units"]),np.ascontiguousarray(packet["initial_fields"])
                lib.mts_dense_load(len(starts),pointer(starts),pointer(ends),pointer(initial),pointer(coefficients),pointer(units),pointer(fields),float(supplied["initial_time"]))
                lib.mts_operator_window(float(packet["times"][-1]),saved_signature.ctypes.data_as(INTEGER_POINTER))
                lib.mts_dense_mode(1)
                lib.mts_bridge_thermal_rebuild()
                probes = np.unique(np.linspace(0,len(efolds)-1,17,dtype=int))
                check = []
                for index in probes:
                    current = point(efolds[index])
                    observed = observe(current[11],reference["initial"])
                    check.append([current[12],observed[28],packet["H"][index]])
                check = np.array(check)
                mismatch = float(np.max(abs(check[:,0,None]-check[:,1:]))/np.max(check[:,0]))
                require(mismatch < ALGEBRA,"native Friedmann point disagreement")
                write(model_root/(tag+"-background-check.json"),dict(sha256=digest(BACKGROUND/"runs"/model/(tag+".npz")),hubble_error=mismatch,physical_grid_unchanged=True,thermal_rebuilt=True))
                return packet
            def extension(maximum, galerkin):
                moments = np.arange(3,maximum+1)
                lower = WAVE*moments/(2*moments+1)
                upper = -WAVE*(moments+1)/(2*moments+1)
                if not galerkin:
                    lower[-1] = WAVE
                units = np.r_[normalization[core],np.tile(tail_units,len(moments))]
                initial_extended = np.r_[reference["initial"][core],np.zeros(len(moments)*5)]
                def project(state):
                    tail = state[len(core):].reshape(len(moments),5)
                    original = np.zeros(dimension)
                    original[core],original[tail_slots] = state[:len(core)],tail[:14]
                    return original
                def physical_rhs(efold,state):
                    current = point(efold)
                    original = project(state)
                    rate = original_rhs(current[11],original)
                    _,speeds = kinetic(current[11])
                    tail = state[len(core):].reshape(len(moments),5)
                    derivative = np.zeros_like(tail)
                    derivative[1:] += lower[1:,None]*tail[:-1]
                    derivative[:-1] += upper[:-1,None]*tail[1:]
                    derivative *= speeds
                    derivative[0] += 3*WAVE/7*speeds*original[low_slots]
                    if not galerkin:
                        derivative[-1] -= (maximum+1)/current[11]*tail[-1]
                    return np.r_[rate[core],derivative.ravel()],current
                return units,initial_extended,project,physical_rhs
            cases = []
            active_background = None
            for tag, maximum, galerkin, tolerance, amplitude, background_tag in CASES:
                guard()
                if active_background != background_tag:
                    background = activate_background(background_tag)
                    active_background = background_tag
                units, initial_extended, project, physical_rhs = extension(maximum,galerkin)
                current = point(efolds[0])
                first_step = min(old_first_step*current[12],max_step/8)
                test = np.sin(np.arange(1,len(units)+1))*units
                test_n = float(efolds[len(efolds)//2])
                positive,_ = physical_rhs(test_n,test)
                negative,_ = physical_rhs(test_n,-test)
                linearity = float(np.max(abs(positive+negative))/max(np.max(abs(positive)),1e-80))
                require(linearity<ALGEBRA and np.count_nonzero(physical_rhs(test_n,np.zeros(len(units)))[0])==0,"RHS linearity")
                if tag=="L64-base":
                    original_units,original_initial,original_project,original_physical = extension(16,False)
                    point0 = point(test_n)
                    native_matrix = np.column_stack([original_rhs(point0[11],basis) for basis in np.eye(dimension)])
                    projected_matrix = np.column_stack([original_project(original_physical(test_n,np.r_[basis[core],basis[tail_slots].ravel()])[0]) for basis in np.eye(dimension)])
                    embedding_error = row_error(projected_matrix,native_matrix)
                    require(embedding_error<ALGEBRA,"repaired16 exact embedding")
                    write(model_root/"embedding-check.json",dict(error=embedding_error,old_operator_error=max(operator_errors)))
                last_guard = time.monotonic()
                def rhs(efold,state):
                    nonlocal last_guard
                    if time.monotonic()-last_guard>2:
                        guard()
                        last_guard=time.monotonic()
                    rate,current = physical_rhs(efold,state*units)
                    return rate/current[12]/units
                started = time.monotonic()
                print(model,tag,"starting",len(units),"states",flush=True)
                solution = solve_ivp(rhs,(float(efolds[0]),float(efolds[-1])),amplitude*initial_extended/units,
                                     method="DOP853",rtol=tolerance,atol=tolerance/100,first_step=first_step,max_step=max_step,t_eval=efolds)
                write(model_root/(tag+"-status.json"),dict(success=solution.success,message=solution.message,nfev=solution.nfev,
                                                         last_efold=float(solution.t[-1]),returned_points=len(solution.t)))
                require(solution.success and len(solution.t)==len(efolds) and np.isfinite(solution.y).all(),"coupled evolution failed")
                physical_state = solution.y.T*units
                projected = np.array([project(state) for state in physical_state])
                observers,terms_rows,metadata_rows,point_rows = [],[],[],[]
                for sample,(efold,vector) in enumerate(zip(efolds,projected)):
                    if sample%512==0:
                        guard()
                    current = point(efold)
                    terms,metadata = stress(current[11],vector)
                    observers.append(observe(current[11],vector))
                    terms_rows.append(terms)
                    metadata_rows.append(metadata)
                    point_rows.append(current)
                point_rows = np.array(point_rows)
                observers = np.array(observers)
                hubble_consistency = float(np.max(abs(point_rows[:,12]-observers[:,28]))/np.max(point_rows[:,12]))
                require(hubble_consistency<ALGEBRA,"evolved source H mismatch")
                moments = np.arange(3,maximum+1)
                weights = (2*moments+1).astype(float)
                if not galerkin:
                    weights[-1] = maximum
                tails = physical_state[:,len(core):].reshape(len(efolds),len(moments),5)
                tail_norms = np.sqrt(np.sum(weights[None,:,None]*tails**2,axis=1))
                path = model_root/(tag+".npz")
                np.savez_compressed(path,efold=efolds,times=point_rows[:,11],a=point_rows[:,10],H=point_rows[:,12],
                                    projected_state=projected,observer=observers,observer_names=np.array(names),
                                    terms=np.array(terms_rows),metadata=np.array(metadata_rows),tail_norms=tail_norms,
                                    terminal=tails[:,-1],final_extended=physical_state[-1],units=units,
                                    initial_extended=amplitude*initial_extended,core=core,tail_slots=tail_slots,low_slots=low_slots,
                                    mapping=reference["mapping"],background_points=point_rows)
                case = dict(tag=tag,maximum=maximum,galerkin=galerkin,rtol=tolerance,atol=tolerance/100,amplitude=amplitude,
                            background=background_tag,dimension=len(units),nfev=solution.nfev,seconds=time.monotonic()-started,
                            first_step_N=first_step,max_step_N=max_step,linearity=linearity,hubble_consistency=hubble_consistency,
                            file=path.name,sha256=digest(path))
                cases.append(case)
                write(model_root/(tag+".json"),case)
                print(model,tag,"done",case["seconds"],"seconds",flush=True)
                del solution,physical_state,projected,tails,observers,terms_rows,metadata_rows,point_rows
            report = dict(model=model,cases=cases,initial_source_sha256=digest(source_path),original_state_sha256=digest(old_folder/"native-reference.npz"),
                          old_operator_error=max(operator_errors),same_initial_physical_slice=True,physical_grid_unchanged=True,no_future_species_histories_supplied=True)
            reports.append(report)
            write(model_root/"result.json",report)
            lib.mts_dense_mode(0)
            del native
    except BaseException as error:
        failure = repr(error)
        raise
    finally:
        write(ROOT/"prediction-configured-result.json",dict(state="complete" if failure is None and len(reports)==2 else "failed",error=failure,reports=reports,
                                                source_sha256=digest(__file__),run_config_sha256=digest(ROOT/"run-configured.json"),
                                                bridge_closeout_sha256=digest(ADAPTER/"closeout.json"),native_background_and_clock_repaired=True,
                                                original_bank_unchanged=True))


if __name__ == "__main__":
    main()

