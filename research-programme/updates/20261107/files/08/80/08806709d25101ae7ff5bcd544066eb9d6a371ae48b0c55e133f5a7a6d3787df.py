import ast
import ctypes
import sys
from datetime import datetime,timezone
from common import ROOT, EVOLUTION, SOURCE, HIERARCHY, NATIVE, PRIOR, EARLY, BRANCH, modest, guard, check_prior, require, read, write, digest, load
import numpy as np

def main():
    modest()
    check_prior()
    build=read(ROOT/"build/build-result.json")
    require(build["state"]=="complete" and digest(ROOT/"build/native/camb/cambdll.dll")==build["dll_sha256"],"build owner")
    scale_owner=read(EVOLUTION/"limit-budget-validation.json")
    star=next(row for row in scale_owner["rows"] if row["model"]=="heavy")["balanced_wave_mpc_inverse"]
    waves=[("half",star/2),("balanced",star),("double",star*2)]
    write(ROOT/"inventory-config.json",dict(waves=waves,scale_source_sha256=digest(EVOLUTION/"limit-budget-validation.json"),
                                          source_sha256=digest(__file__),protocol_sha256=digest(ROOT/"PROTOCOL.md"),
                                          created_utc=datetime.now(timezone.utc).isoformat(),purpose="native regime inventory only, no source-performance scoring"))
    sys.path.insert(0,str(ROOT/"build/native"))
    import camb
    from camb.mts import MTSTwoField
    sys.path.append(str(BRANCH/"radiation-and-slow-field-transfer-20261007"))
    import radiation_common
    factory_owner=NATIVE.parent/"matching_common.py"
    function=next(node for node in ast.parse(factory_owner.read_text()).body if isinstance(node,ast.FunctionDef) and node.name=="params_for")
    namespace=dict(np=np,previous=radiation_common,MTSTwoField=MTSTwoField)
    exec(compile(ast.Module(body=[function],type_ignores=[]),str(factory_owner),"exec"),namespace)
    lib=camb.baseconfig.camblib
    observer_dll=ctypes.CDLL(str(PRIOR/"observer.dll"))
    source_function=ctypes.cast(observer_dll.source_func_,ctypes.c_void_p)
    lib.mts_capture_reset.argtypes,lib.mts_capture_reset.restype=[],None
    lib.mts_dense_mode.argtypes,lib.mts_dense_mode.restype=[ctypes.c_int],None
    begin=ctypes.c_int.in_dll(lib,"mts_regime_begin")
    count=ctypes.c_int.in_dll(lib,"mts_regime_count")
    signatures=(ctypes.c_int*(96*64)).in_dll(lib,"mts_regime_signatures")
    metadata=(ctypes.c_double*(8*64)).in_dll(lib,"mts_regime_metadata")
    vectors=(ctypes.c_double*(1024*64)).in_dll(lib,"mts_regime_vectors")
    rates=(ctypes.c_double*(1024*64)).in_dll(lib,"mts_regime_rates")
    source_owner=read(SOURCE/"phase-resolved/tangent-native-result.json")
    destination=ROOT/"inventory"
    destination.mkdir(exist_ok=False)
    reports=[]
    failure=None
    try:
        for model in ("heavy","cold"):
            reference=load(HIERARCHY/"runs-balanced"/model/"native-reference.npz")
            row=next(row for row in source_owner["reports"] if row["model"]==model and row["tag"]=="one")
            source_path=SOURCE/"phase-resolved/packets"/row["file"]
            require(digest(source_path)==row["sha256"],"initial-prefix owner")
            packet=load(source_path)
            first=int(packet["original_indices"][0])
            prefix=packet["full_times"][:first]
            indices=np.unique(np.linspace(0,len(reference["times"])-1,17,dtype=int))
            window=reference["times"][indices]
            times=np.ascontiguousarray(np.r_[prefix,window])
            for label,wave in waves:
                guard()
                lib.mts_dense_mode(0)
                params=namespace["params_for"](EARLY/f"runs/backgrounds/{model}.npz")
                native=camb.get_background(params)
                native.Params.Accuracy.IntTolBoost=6
                native.Params.Accuracy.lAccuracyBoost=4
                lib.mts_capture_reset()
                ctypes.c_int.in_dll(lib,"mts_probe_step").value=0
                ctypes.c_int.in_dll(lib,"mts_probe_tangent").value=0
                begin.value=len(prefix)+1
                count.value=0
                ncustom=len(reference["observer_names"])
                total=len(camb.model.evolve_names)+ncustom
                output=np.zeros((1,len(times),total))
                code=camb.results.CAMB_TimeEvolution(ctypes.byref(native),ctypes.byref(ctypes.c_int(1)),np.array([wave]),
                    ctypes.byref(ctypes.c_int(len(times))),times,ctypes.byref(ctypes.c_int(total)),output,
                    ctypes.byref(ctypes.c_int(ncustom)),ctypes.byref(source_function))
                require(code==0 and count.value==17,"complete passive inventory")
                signature=np.ctypeslib.as_array(signatures).reshape((96,64),order="F")[:,:17].T.copy()
                meta=np.ctypeslib.as_array(metadata).reshape((8,64),order="F")[:,:17].T.copy()
                state=np.ctypeslib.as_array(vectors).reshape((1024,64),order="F")[:,:17].T.copy()
                derivative=np.ctypeslib.as_array(rates).reshape((1024,64),order="F")[:,:17].T.copy()
                require(np.array_equal(meta[:,0],window) and np.isfinite(meta).all(),"inventory timing")
                unique=np.unique(signature,axis=0)
                supported=bool(len(unique)==1 and signature[0,11]==0 and np.all(signature[:,16:19]==0) and np.all(signature[:,70:76]==0))
                path=destination/(model+"-"+label+".npz")
                np.savez_compressed(path,wave=wave,times=window,indices=indices,signature=signature,metadata=meta,
                                    state=state,derivative=derivative,observer=output[0,len(prefix):,-ncustom:],
                                    observer_names=reference["observer_names"])
                report=dict(model=model,label=label,wave=wave,signature_count=len(unique),signatures=unique.tolist(),
                            tight_coupling=signature[:,11].tolist(),massless_UFA=signature[:,12].tolist(),
                            propagated_dimensions=signature[:,1].tolist(),scalar_slots=signature[:,2].tolist(),
                            tight_switch_times=meta[:,5].tolist(),UFA_threshold_times=meta[:,6].tolist(),
                            capture_supported_without_extension=supported,source_sha256=row["sha256"],file=path.name,sha256=digest(path))
                reports.append(report)
                print(dict(model=model,label=label,wave=wave,signature_count=len(unique),TCA=np.unique(signature[:,11]).tolist(),
                           UFA=np.unique(signature[:,12]).tolist(),dimensions=np.unique(signature[:,1]).tolist(),supported=supported),flush=True)
                begin.value=0
                del native
    except BaseException as error:
        failure=repr(error)
        raise
    finally:
        write(ROOT/"inventory-result.json",dict(state="complete" if failure is None and len(reports)==6 else "failed",error=failure,reports=reports,
                                               source_sha256=digest(__file__),config_sha256=digest(ROOT/"inventory-config.json"),
                                               previous_closeout_sha256=digest(EVOLUTION/"closeout.json"),
                                               no_repaired_source_performance_scored=True))

if __name__=="__main__":
    main()

