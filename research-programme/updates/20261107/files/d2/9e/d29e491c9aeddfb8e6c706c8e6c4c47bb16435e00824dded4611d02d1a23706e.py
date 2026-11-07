import ast
import ctypes
import os
import sys
import time
from datetime import datetime, timezone
from common import ROOT, PRIOR, PAIRED, SOURCE, HIERARCHY, NATIVE, BRANCH, EARLY, ALGEBRA, modest, guard, check_prior, require, read, write, digest, load, BACKGROUND, ADAPTER, COUPLED, EVOLUTION, WAVELENGTH, AVERAGE, ENVELOPE, NORMAL, MEAN
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from envelope_math import identities
from near_identity_parent import NearIdentity
from micromotion import Micromotion,prepare_table

POINTER = ctypes.POINTER(ctypes.c_double)
INTEGER_POINTER = ctypes.POINTER(ctypes.c_int)
CASES = [("L128-full-fine",128,False,2e-12,1.,"dop-half-cap"),
         ("G192-full-fine",192,True,2e-12,1.,"dop-half-cap"),
         ("L128-reduced-base",128,False,2e-11,1.,"dop-half-cap"),
         ("L128-reduced-fine",128,False,2e-12,1.,"dop-half-cap"),
         ("G192-reduced-fine",192,True,2e-12,1.,"dop-half-cap"),
         ("L128-reduced-zero",128,False,2e-11,0.,"dop-half-cap"),
         ("L128-reduced-coarse",128,False,2e-12,1.,"dop-half-cap")]


def pointer(values):
    return values.ctypes.data_as(POINTER)


def row_error(left, right):
    return float(np.max(abs(left - right) / np.maximum(np.max(abs(right), axis=1, keepdims=True), 1e-80)))


def main():
    modest()
    require(not any(isinstance(node,ast.Name) and node.id=="WAVE" for node in ast.walk(ast.parse(open(__file__,encoding="utf-8").read()))),"unbound inherited wavenumber")
    require(len(CASES)==7 and all(len(case)==6 for case in CASES), "case schema")
    check_prior()
    decomposition=read(MEAN/"decomposition-result.json")
    require(decomposition["passed"] and decomposition["harmonics_sha256"]==digest(ROOT/"harmonics.py") and decomposition["protocol_sha256"]==digest(MEAN/"PROTOCOL.md"),"frozen decomposition accepted")
    write(ROOT/"symbolic-identities.json",dict(passed=True,identities=identities(),source_sha256=digest(ROOT/"envelope_math.py")))
    build = read(WAVELENGTH / "build-full-momentum/build-result.json")
    require(build["state"] == "complete" and build["dll_sha256"] == digest(WAVELENGTH / "build-full-momentum/native/camb/cambdll.dll"), "isolated build ownership")
    sys.path.insert(0, str(WAVELENGTH / "build-full-momentum/native"))
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

    ctypes.c_int.in_dll(lib,"mts_promote_momenta").value=1
    ctypes.c_int.in_dll(lib,"mts_regime_begin").value=0
    inventory=read(WAVELENGTH/"inventory-result.json")
    require(inventory["state"]=="complete" and len(inventory["reports"])==6,"complete original regime inventory")
    waves=read(WAVELENGTH/"inventory-config.json")["waves"]
    promotion=(ctypes.c_double*8).in_dll(lib,"mts_promotion_audit")
    native_names = list(camb.model.evolve_names)
    owner_result = read(SOURCE / "phase-resolved/tangent-native-result.json")
    hierarchy_owner = read(HIERARCHY / "hierarchy-balanced-result.json")
    destination = ROOT / "runs-second"
    destination.mkdir(exist_ok=False)
    write(ROOT / "run-config.json", dict(source_sha256=digest(__file__), protocol_sha256=digest(ROOT / "PROTOCOL.md"), cases=CASES, created_utc=datetime.now(timezone.utc).isoformat(), scaling="prior initial-operator core units; maximum prior per-node unit for every extended angular moment; no future states", no_future_perturbation_history_supplied=True))
    reports, failure = [], None
    try:
        for model in ("heavy", "cold"):
            for wave_label,wave in waves:
                guard()
                lib.mts_dense_mode(0)
                old_folder = HIERARCHY / "runs-balanced" / model
                reference = load(old_folder / "native-reference.npz")
                audit = load(old_folder / "operator-audit.npz")
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
                code = camb.results.CAMB_TimeEvolution(ctypes.byref(native), ctypes.byref(ctypes.c_int(1)), np.array([wave]), ctypes.byref(ctypes.c_int(len(prefix))), prefix, ctypes.byref(ctypes.c_int(count)), output, ctypes.byref(ctypes.c_int(len(names))), ctypes.byref(source_function))
                require(code == 0 and capture["count"].value == 1, "single initial capture")
                dimension = capture["dimension"].value
                initial, initial_rate = np.zeros((dimension, 1), order="F"), np.zeros((dimension, 1), order="F")
                initial_time = np.zeros(1)
                lib.mts_capture_copy(dimension, 1, pointer(initial), pointer(initial_rate), pointer(initial_time))
                state_map=np.array(list(mapping)[:dimension])
                regime=np.array(list(signature))
                passive_owner=next(row for row in inventory["reports"] if row["model"]==model and row["label"]==wave_label)
                passive=load(WAVELENGTH/"inventory"/passive_owner["file"])
                require(digest(WAVELENGTH/"inventory"/passive_owner["file"])==passive_owner["sha256"],"passive inventory owner")
                old_slot=int(passive["signature"][0,2])
                selected_native=[2] if model=="cold" else [int(regime[2])+2,int(regime[2])+3]
                selected=np.array([int(np.flatnonzero(state_map==index)[0]) for index in selected_native])
                seed=passive["state"][0,1:2] if model=="cold" else passive["state"][0,old_slot+1:old_slot+3]
                require(np.array_equal(initial[:,0][selected],seed),"same primordial-prefix seed")
                unselected=np.array([index for index in range(dimension) if index not in selected])
                require(np.count_nonzero(initial[:,0][unselected])==0,"nonzero unselected preparation")
                require(np.all(np.array(list(promotion))[4:7]==0),"promotion changed preparation or stress")
                require(regime[18]==0 and regime[30]==5 and regime[11]==0,"explicit five-node non-TCA regime")
                reference=dict(times=times,initial=initial[:,0].copy(),mapping=state_map,signature=regime,observer_names=np.array(names))
                captured_observer=output[0,-1,len(native_names):].copy()
                captured_rate=initial_rate[:,0].copy()
                saved_signature = np.ascontiguousarray(reference["signature"], dtype=np.int32)
                lib.mts_operator_window(float(times[-1]), saved_signature.ctypes.data_as(INTEGER_POINTER))
                signature_values = reference["signature"]
                require(signature_values[20] == 1 and signature_values[30] == 5, "expected retained massive-neutrino layout")
                native_order=int(signature_values[40])
                def position(native_index):
                    return int(np.flatnonzero(reference["mapping"] == native_index)[0])
                all_moments = np.column_stack([[position(int(signature_values[50]) + node * (native_order+1) + ell) for ell in range(native_order+1)] for node in range(5)])
                tail_slots, low_slots = all_moments[3:], all_moments[2]
                core = np.array([index for index in range(dimension) if index not in tail_slots])
                require(np.count_nonzero(reference["initial"][tail_slots]) == 0, "initial high-moment preparation not zero")
                model_root = destination / (model+"-"+wave_label)
                model_root.mkdir()
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

                cached_folder=WAVELENGTH/"runs-bound"/(model+"-"+wave_label)
                cached=load(cached_folder/"initial-context.npz")
                require(np.array_equal(cached["initial"],reference["initial"]) and np.array_equal(cached["mapping"],state_map),"same cached initial native vector")
                matrix0=cached["initial_operator"]
                require(np.array_equal(original_rhs(times[0],reference["initial"]),captured_rate),"initial operator rate ownership")
                require(np.array_equal(observe(times[0],reference["initial"]),captured_observer),"initial observer ownership")
                offsets=cached["frozen_offsets"]
                frozen_states=cached["frozen_states"]
                normalization=cached["old_normalization"]
                tail_units=cached["tail_units"]
                native_first_step=read(cached_folder/"capture-check.json")["first_step_native"]
                mass=float(native.Params.DarkEnergy.heavy_mass_mpc) if model=="heavy" else 1.
                require(mass>0,"positive carrier mass")
                if model=="heavy":
                    heavy_native=position(int(signature_values[2])+2)
                    velocity_native=position(int(signature_values[2])+3)
                    envelope_slots=[int(np.flatnonzero(core==heavy_native)[0]),int(np.flatnonzero(core==velocity_native)[0])]
                else:
                    envelope_slots=[]
                np.savez_compressed(model_root/"initial-context.npz",initial=reference["initial"],initial_rate=captured_rate,
                                    mapping=state_map,signature=regime,core=core,tail_slots=tail_slots,low_slots=low_slots,
                                    old_normalization=normalization,tail_units=tail_units,frozen_states=frozen_states,
                                    frozen_offsets=offsets,initial_operator=matrix0,promotion=np.array(list(promotion)),
                                    native_order=native_order,wave=wave)
                write(model_root/"capture-check.json",dict(same_seed=True,zero_unselected=True,source_preserved=True,
                      exact_initial_rate=True,exact_initial_observer=True,prefix_points=len(prefix),passive_inventory_sha256=passive_owner["sha256"],
                      initial_time=float(initial_time[0]),native_order=native_order,signature=regime.tolist(),promotion=list(promotion),
                      normalization="initial frozen operator at17 offsets; no future species states",first_step_native=native_first_step))
                operator_errors=[0.]
                supplied = load(BACKGROUND / "inputs" / (model + "-input.npz"))
                efolds = supplied["efold"]
                max_step = float(supplied["step_cap"])/2
                old_first_step = native_first_step
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
                    lower = wave*moments/(2*moments+1)
                    upper = -wave*(moments+1)/(2*moments+1)
                    if not galerkin:
                        lower[-1] = wave
                    units = np.r_[normalization[core],np.tile(tail_units,len(moments))]
                    initial_extended = np.r_[reference["initial"][core],np.zeros(len(moments)*5)]
                    def project(state):
                        tail = state[len(core):].reshape(len(moments),5)
                        original = np.zeros(dimension)
                        original[core],original[tail_slots] = state[:len(core)],tail[:native_order-2]
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
                        derivative[0] += 3*wave/7*speeds*original[low_slots]
                        if not galerkin:
                            derivative[-1] -= (maximum+1)/current[11]*tail[-1]
                        return np.r_[rate[core],derivative.ravel()],current
                    return units,initial_extended,project,physical_rhs
                cases = []
                active_background = None
                motion_table=None
                table_prepared=False
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
                    if tag=="L128-full-fine":
                        original_units,original_initial,original_project,original_physical = extension(native_order,False)
                        point0 = point(test_n)
                        native_matrix = np.column_stack([original_rhs(point0[11],basis) for basis in np.eye(dimension)])
                        projected_matrix = np.column_stack([original_project(original_physical(test_n,np.r_[basis[core],basis[tail_slots].ravel()])[0]) for basis in np.eye(dimension)])
                        embedding_error = row_error(projected_matrix,native_matrix)
                        require(embedding_error<ALGEBRA,"actual native-order exact embedding")
                        write(model_root/"embedding-check.json",dict(error=embedding_error,old_operator_error=max(operator_errors)))
                    native_units=units.copy()
                    shift=np.pi/4 if tag.endswith("-shift") else 0.
                    carrier_rate=CubicSpline(efolds,background["a"]*mass/background["H"])
                    carrier_integral=carrier_rate.antiderivative()
                    carrier_origin=float(carrier_integral(efolds[0]))
                    def carrier(efold):
                        return float(carrier_integral(efold))-carrier_origin+shift,float(carrier_rate(efold))
                    if model=="heavy":
                        envelope_scale=float(np.max(background["a"]))*(
                            np.sqrt(float(np.max(background["a"]))*mass)*native_units[envelope_slots[0]]+
                            native_units[envelope_slots[1]]/np.sqrt(float(np.min(background["a"]))*mass))
                        units[envelope_slots]=envelope_scale
                    def rotate_encode(efold,state):
                        result=state.copy()
                        if model=="heavy":
                            scale=np.exp(efold)
                            omega=scale*mass
                            phase,_=carrier(efold)
                            amplitude=scale*(np.sqrt(omega)*state[envelope_slots[0]]+
                                             1j*state[envelope_slots[1]]/np.sqrt(omega))*np.exp(1j*phase)
                            result[envelope_slots]=[amplitude.real,amplitude.imag]
                        return result
                    def rotate_decode(efold,state):
                        result=state.copy()
                        if model=="heavy":
                            scale=np.exp(efold)
                            omega=scale*mass
                            phase,_=carrier(efold)
                            amplitude=complex(*state[envelope_slots])*np.exp(-1j*phase)
                            result[envelope_slots]=[amplitude.real/(scale*np.sqrt(omega)),amplitude.imag*np.sqrt(omega)/scale]
                        return result
                    def rotating_rhs(efold,state):
                        physical=rotate_decode(efold,state)
                        rate,current=physical_rhs(efold,physical)
                        derivative=rate/current[12]
                        if model=="heavy":
                            scale,hubble=current[10],current[12]
                            omega=scale*mass
                            phase,phase_derivative=carrier(efold)
                            amplitude=complex(*state[envelope_slots])
                            observed=observe(current[11],project(physical))
                            metric_z=observed[5]-1.5*observed[3]/wave**2
                            rotation=np.exp(1j*phase)
                            rotated_conjugate=rotation**2*np.conjugate(amplitude)
                            amplitude_rate=(1.5*rotated_conjugate
                                            -1j*wave**2/(2*omega*hubble)*(amplitude+rotated_conjugate)
                                            -1j*scale*wave*metric_z*current[3]*rotation/(np.sqrt(omega)*hubble)
                                            +1j*(phase_derivative-omega/hubble)*amplitude)
                            derivative[envelope_slots]=[amplitude_rate.real,amplitude_rate.imag]
                        return derivative
                    encoded_test=rotate_encode(test_n,test)
                    decoded_test=rotate_decode(test_n,encoded_test)
                    inverse_error=float(np.max(abs(decoded_test-test)/native_units))
                    chain=positive/point(test_n)[12]
                    if model=="heavy":
                        scale=np.exp(test_n)
                        omega=scale*mass
                        phase,phase_derivative=carrier(test_n)
                        rotation=np.exp(1j*phase)
                        expected=(rotation*(scale*np.sqrt(omega)*(1.5*test[envelope_slots[0]]+chain[envelope_slots[0]])+
                                  1j*scale/np.sqrt(omega)*(.5*test[envelope_slots[1]]+chain[envelope_slots[1]]))+
                                  1j*phase_derivative*complex(*encoded_test[envelope_slots]))
                        chain[envelope_slots]=[expected.real,expected.imag]
                    transformed_test=rotating_rhs(test_n,encoded_test)
                    chain_error=float(np.max(abs(transformed_test-chain)/np.maximum(abs(chain),units)))
                    require(inverse_error<ALGEBRA and chain_error<ALGEBRA,"exact rotating-coordinate preflight")
                    write(model_root/(tag+"-transform-check.json"),dict(inverse_error=inverse_error,chain_error=chain_error,
                          phase_offset=shift,heavy_transformed=model=="heavy",no_terms_dropped=True,carrier_from_background_only=True))
                    hubble_log=CubicSpline(efolds,np.log(background["H"]))
                    parent_form=NearIdentity(model,False,envelope_slots,mass,wave,float(background["initial_fields"][1]),
                                      point,carrier,carrier_rate,hubble_log,rotate_decode,rotating_rhs,project,observe,stress)
                    if not table_prepared:
                        print(model,wave_label,"building background-only micromotion row",flush=True)
                        motion_table=prepare_table(parent_form,efolds,units,core,state_map,signature_values,model_root)
                        table_prepared=True
                    form=Micromotion(parent_form,motion_table,"-reduced-" in tag,tag.endswith("-coarse"))
                    normal_preflight=form.preflight(test_n,encoded_test,units)
                    write(model_root/(tag+"-normal-check.json"),normal_preflight)
                    def encode(efold,state):
                        return form.forward(efold,rotate_encode(efold,state))
                    def decode(efold,state):
                        rotated,_,_=form.inverse(efold,state)
                        return rotate_decode(efold,rotated)
                    def transformed_rhs(efold,state):
                        return form.rhs(efold,state)
                    units[envelope_slots]*=2
                    initial_transformed=amplitude*encode(efolds[0],initial_extended)
                    last_guard = time.monotonic()
                    def rhs(efold,state):
                        nonlocal last_guard
                        if time.monotonic()-last_guard>2:
                            guard()
                            last_guard=time.monotonic()
                        return transformed_rhs(efold,state*units)/units
                    started = time.monotonic()
                    print(model,wave_label,tag,"starting",len(units),"states",flush=True)
                    solution = solve_ivp(rhs,(float(efolds[0]),float(efolds[-1])),initial_transformed/units,
                                         method="DOP853",rtol=tolerance,atol=tolerance/100,first_step=first_step,max_step=max_step,t_eval=efolds)
                    write(model_root/(tag+"-status.json"),dict(success=solution.success,message=solution.message,nfev=solution.nfev,
                                                             last_efold=float(solution.t[-1]),returned_points=len(solution.t)))
                    require(solution.success and len(solution.t)==len(efolds) and np.isfinite(solution.y).all(),"coupled envelope evolution failed")
                    rotated_state=solution.y.T*units
                    physical_state=np.array([decode(efold,state) for efold,state in zip(efolds,rotated_state)])
                    projected = np.array([project(state) for state in physical_state])
                    observers,terms_rows,metadata_rows,point_rows,diagnostic_rows,carrier_rows = [],[],[],[],[],[]
                    for sample,(efold,vector) in enumerate(zip(efolds,projected)):
                        if sample%512==0:
                            guard()
                        current = point(efold)
                        terms,metadata = stress(current[11],vector)
                        observed=observe(current[11],vector)
                        _,diagnostic=form.rates(efold,rotated_state[sample])
                        density_correction,momentum_correction=diagnostic["stress_correction"]
                        terms[6,3]+=density_correction
                        terms[6,4]+=momentum_correction
                        observed[6]+=density_correction/(2*wave*current[12])+1.5*momentum_correction/wave**2
                        observed[10]-=(density_correction+3*current[12]*momentum_correction/wave)/(2*wave**2)
                        diagnostic_rows.append(diagnostic)
                        carrier_rows.append(rotate_encode(efold,physical_state[sample])[envelope_slots])
                        observers.append(observed)
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
                                        terminal=tails[:,-1],final_extended=physical_state[-1],units=native_units,
                                        envelope_units=units,envelope=np.array(carrier_rows),normal_amplitude=rotated_state[:,envelope_slots],initial_transformed=initial_transformed,
                                        normal_remainder=np.array([row["remainder"] for row in diagnostic_rows]),
                                        retained_mean=np.array([row["retained_mean"] for row in diagnostic_rows]),
                                        represented_defect=np.array([row["represented_defect"] for row in diagnostic_rows]),
                                        second_remainder=np.array([row["second_remainder"] for row in diagnostic_rows]),
                                        second_full_rate=np.array([row["second_full_rate"] for row in diagnostic_rows]),
                                        second_desired_rate=np.array([row["second_desired_rate"] for row in diagnostic_rows]),
                                        map_primitive=np.array([row["map_primitive"] for row in diagnostic_rows]),
                                        direct_primitive=np.array([row["direct_primitive"] for row in diagnostic_rows]),
                                        map_chain_rate=np.array([row["map_chain_rate"] for row in diagnostic_rows]),
                                        first_amplitude=np.array([row["first_amplitude"] for row in diagnostic_rows]),
                                        derivative_defect=np.array([row["derivative_defect"] for row in diagnostic_rows]),
                                        stress_rate_correction=np.array([row["stress_correction"] for row in diagnostic_rows]),
                                        correction_size=np.array([row["correction_size"] for row in diagnostic_rows]),
                                        inverse_bound=np.array([row["inverse_bound"] for row in diagnostic_rows]),
                                        derivative_defect_bound=np.array([row["defect_bound"] for row in diagnostic_rows]),
                                        hubble_derivative_difference=np.array([row["hlog_difference"] for row in diagnostic_rows]),
                                        envelope_slots=np.array(envelope_slots,dtype=int),carrier_phase=np.array([carrier(value)[0] for value in efolds]),
                                        carrier_derivative=np.array([carrier(value)[1] for value in efolds]),mass=np.array(mass),
                                        initial_extended=amplitude*initial_extended,core=core,tail_slots=tail_slots,low_slots=low_slots,
                                        mapping=reference["mapping"],background_points=point_rows)
                    case = dict(tag=tag,maximum=maximum,galerkin=galerkin,rtol=tolerance,atol=tolerance/100,amplitude=amplitude,
                                background=background_tag,dimension=len(units),phase_offset=shift,rotating_coordinates=model=="heavy",reduced_candidate="-reduced-" in tag,nfev=solution.nfev,seconds=time.monotonic()-started,
                                first_step_N=first_step,max_step_N=max_step,linearity=linearity,hubble_consistency=hubble_consistency,
                                file=path.name,sha256=digest(path))
                    if "-full-" in tag:
                        previous=load(NORMAL/"runs-owned"/(model+"-"+wave_label)/(tag+".npz"))
                        difference=float(np.max(np.max(abs(projected-previous["projected_state"]),axis=0)/np.maximum(np.max(abs(previous["projected_state"]),axis=0),1e-30)))
                        require(np.array_equal(efolds,previous["efold"]) and difference<2e-5,"full second transform versus previous exact evolution")
                        case["inline_full_control_error"]=difference
                        write(model_root/(tag+"-control-check.json"),dict(passed=True,state_error=difference,parent_sha256=digest(NORMAL/"runs-owned"/(model+"-"+wave_label)/(tag+".npz"))))
                    case["coarse_coefficients"]=tag.endswith("-coarse")
                    cases.append(case)
                    write(model_root/(tag+".json"),case)
                    print(model,tag,"done",case["seconds"],"seconds",flush=True)
                    del solution,rotated_state,physical_state,projected,tails,observers,terms_rows,metadata_rows,point_rows
                report = dict(model=model,label=wave_label,wave=wave,cases=cases,initial_source_sha256=digest(source_path),original_state_sha256=digest(old_folder/"native-reference.npz"),
                              old_operator_error=max(operator_errors),same_initial_physical_slice=True,physical_grid_unchanged=True,no_future_species_histories_supplied=True)
                reports.append(report)
                write(model_root/"result.json",report)
                lib.mts_dense_mode(0)
                del native
    except BaseException as error:
        failure = repr(error)
        raise
    finally:
        write(ROOT/"prediction-result.json",dict(state="complete" if failure is None and len(reports)==6 else "failed",error=failure,reports=reports,
                                                source_sha256=digest(__file__),run_config_sha256=digest(ROOT/"run-config.json"),
                                                previous_closeout_sha256=digest(MEAN/"closeout.json"),decomposition_sha256=digest(MEAN/"decomposition-result.json"),
                                                second_micromotion_candidate=True,near_identity_sha256=digest(ROOT/"micromotion.py"),parent_map_sha256=digest(ROOT/"near_identity_parent.py"),harmonics_sha256=digest(ROOT/"harmonics.py"),inventory_sha256=digest(WAVELENGTH/"inventory-result.json"),native_background_and_clock_repaired=True,
                                                original_bank_unchanged=True))


if __name__ == "__main__":
    main()

