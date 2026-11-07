import ast
import csv
from pathlib import Path
from common import ROOT, ADAPTER, EVOLUTION, BACKGROUND, BRIDGE, GATE, ALGEBRA, modest, guard, check_prior, require, read, write, digest, load
import numpy as np

def main():
    modest()
    check_prior()
    rows=[]
    def check(name,passed,value=None):
        rows.append(dict(check=name,passed=bool(passed),value=value))
    inventory=read(ROOT/"inventory-result.json")
    owner=read(ROOT/"prediction-bound-result.json")
    comparison=read(ROOT/"comparison-roundtrip-result.json")
    config=read(ROOT/"inventory-config.json")
    check("complete frozen inventory",inventory["state"]=="complete" and len(inventory["reports"])==6)
    check("all frozen wavelengths retained",len(owner["reports"])==6 and comparison["all_frozen_wavelengths_retained"])
    check("all48 solves complete",owner["state"]=="complete" and sum(len(row["cases"]) for row in owner["reports"])==48)
    check("paired comparison passed",comparison["passed"])
    check("unchanged gates",comparison["numerical_gate"]==GATE and comparison["algebra_gate"]==ALGEBRA)
    check("prediction source",owner["source_sha256"]==digest(ROOT/"run_wavelengths_bound.py"))
    check("comparison source",comparison["source_sha256"]==digest(ROOT/"check_wavelengths_roundtrip.py"))
    check("comparison prediction",comparison["prediction_sha256"]==digest(ROOT/"prediction-bound-result.json"))
    star=next(row for row in read(EVOLUTION/"limit-budget-validation.json")["rows"] if row["model"]=="heavy")["balanced_wave_mpc_inverse"]
    check("derived scales not selected by performance",config["waves"]==[["half",star/2],["balanced",star],["double",2*star]])
    for folder in ("build","build-full-momentum"):
        build=read(ROOT/folder/"build-result.json")
        check(folder+" completed",build["state"]=="complete")
        check(folder+" DLL",digest(ROOT/folder/"native/camb/cambdll.dll")==build["dll_sha256"])
        check(folder+" source",digest(ROOT/folder/"camb_python.f90")==build["source_sha256"])
        check(folder+" mappings cleaned",build["temporary_mappings_removed"])
        for path,checksum in build["reused_bridge_hashes"].items():
            check(folder+" preserved "+Path(path).name,digest(path)==checksum)
        for path,checksum in build["original_input_hashes"].items():
            check(folder+" original source "+path,digest(path)==checksum)
    check("mappings absent",all(not Path(drive).exists() for drive in ("R:/","S:/","T:/")))
    for script in ROOT.glob("*.py"):
        text=script.read_text()
        tree=ast.parse(text)
        compile(text,str(script),"exec")
        check("syntax "+script.name,True)
        if script.name in ("run_wavelengths_bound.py","check_wavelengths_roundtrip.py"):
            check("runtime wavenumber bound "+script.name,not any(isinstance(node,ast.Name) and node.id=="WAVE" for node in ast.walk(tree)))
    failed=read(ROOT/"prediction-result.json")
    check("preflight failure retained",failed["state"]=="failed" and "embedding" in failed["error"])
    check("no failed numerical run retried",not list((ROOT/"runs").rglob("*-status.json")))
    check("failed source preserved",digest(ROOT/"run_wavelengths.py")==read(ROOT/"waves-01.end.json")["source_sha256"])
    diagnostic=read(ROOT/"initial-roundtrip-diagnostic.json")
    check("initial roundtrip diagnostic source",diagnostic["source_sha256"]==digest(ROOT/"diagnose_initial_roundtrip.py"))
    check("initial roundtrip diagnostic trajectories",diagnostic["prediction_sha256"]==digest(ROOT/"prediction-bound-result.json"))
    check("all48 roundtrips exact",diagnostic["passed"] and len(diagnostic["rows"])==48 and all(row["roundtrip_exact"] and row["unseeded_exact_zero"] for row in diagnostic["rows"]))
    check("initial roundtrip at most one ULP",max(row["maximum_ulps"] for row in diagnostic["rows"])<=1)
    check("failed original comparison retained",read(ROOT/"comparison-01.end.json")["exit_code"]==1 and digest(ROOT/"check_wavelengths.py")==read(ROOT/"comparison-01.end.json")["source_sha256"])
    check("partial original comparison retained",read(ROOT/"comparison/heavy-half-result.json")["passed"])
    for parent in owner["reports"]:
        guard()
        model,label,wave=parent["model"],parent["label"],parent["wave"]
        stem=model+"-"+label
        folder=ROOT/"runs-bound"/stem
        initial=load(folder/"initial-context.npz")
        captured=read(folder/"capture-check.json")
        passive=next(row for row in inventory["reports"] if row["model"]==model and row["label"]==label)
        original=load(ROOT/"inventory"/passive["file"])
        check(stem+" passive owner",digest(ROOT/"inventory"/passive["file"])==passive["sha256"])
        check(stem+" seed unchanged",captured["same_seed"] and captured["zero_unselected"] and captured["source_preserved"])
        check(stem+" original rate/source",captured["exact_initial_rate"] and captured["exact_initial_observer"])
        check(stem+" source wave",float(initial["wave"])==wave)
        check(stem+" full momentum channels",initial["signature"][30]==5 and initial["signature"][18]==0)
        promotion=initial["promotion"]
        check(stem+" exact source-preserving promotion",np.all(promotion[4:7]==0))
        if label=="half":
            check(stem+" actual one-to-five promotion",promotion[0]==1 and promotion[1]==5 and promotion[7]==1)
            check(stem+" full massless hierarchy retained",initial["signature"][12]==0)
        else:
            check(stem+" promotion no-op",promotion[0]==5 and promotion[1]==5 and promotion[7]==0)
            check(stem+" retained UFA",initial["signature"][12]==1)
        expected_order=40 if label=="half" else 16
        check(stem+" actual native angular layout",int(initial["native_order"])==expected_order)
        embedding=read(folder/"embedding-check.json")
        check(stem+" exact native-order embedding",embedding["error"]<ALGEBRA,embedding["error"])
        check(stem+" inherited normalization rule",len(initial["frozen_offsets"])==17 and np.all(initial["old_normalization"]>0))
        physical_grid=load(BACKGROUND/"inputs"/(model+"-input.npz"))
        for case in parent["cases"]:
            packet=load(folder/case["file"])
            tag=case["tag"]
            check(stem+" "+tag+" output",digest(folder/case["file"])==case["sha256"])
            check(stem+" "+tag+" successful solve",read(folder/(tag+"-status.json"))["success"])
            check(stem+" "+tag+" same physical grid",np.array_equal(packet["efold"],physical_grid["efold"]))
            expected_extended=(packet["initial_extended"]/packet["units"])*packet["units"]
            expected=np.zeros(len(initial["initial"]))
            expected[packet["core"]]=expected_extended[:len(packet["core"])]
            expected[packet["tail_slots"]]=expected_extended[len(packet["core"]):].reshape(case["maximum"]-2,5)[:int(initial["native_order"])-2]
            intended=case["amplitude"]*initial["initial"]
            initial_error=float(np.max(abs(packet["projected_state"][0]-intended))/max(np.max(abs(intended)),1e-80))
            check(stem+" "+tag+" exact initial roundtrip",np.array_equal(packet["projected_state"][0],expected))
            check(stem+" "+tag+" exact unseeded zeros",np.count_nonzero(packet["projected_state"][0][intended==0])==0)
            check(stem+" "+tag+" physical seed accuracy",initial_error<ALGEBRA,initial_error)
            check(stem+" "+tag+" actual source clock",np.array_equal(packet["times"],packet["observer"][:,29]))
            check(stem+" "+tag+" actual source scale",np.array_equal(packet["a"],packet["observer"][:,27]))
            check(stem+" "+tag+" source H",case["hubble_consistency"]<ALGEBRA)
            check(stem+" "+tag+" finite",all(np.isfinite(value).all() for value in packet.values() if value.dtype.kind in "fci"))
            check(stem+" "+tag+" heavy exact domain",float(np.max(packet["a"]))<.00028)
            check(stem+" "+tag+" monotone physical clock",np.all(np.diff(packet["times"])>0))
            check(stem+" "+tag+" inherited phase cap",case["max_step_N"]==float(physical_grid["step_cap"])/2)
            check(stem+" "+tag+" unchanged tolerances",case["rtol"] in (2e-11,2e-12) and case["atol"]==case["rtol"]/100)
            threshold=float(original["metadata"][0,6])
            if label=="half":
                check(stem+" "+tag+" no corrected UFA crossing",float(packet["times"][-1])<threshold)
            else:
                check(stem+" "+tag+" already past UFA threshold",float(packet["times"][0])>threshold)
            del packet
        report=next(row for row in comparison["reports"] if row["model"]==model and row["label"]==label)
        check(stem+" accepted",report["passed"])
        for pair in report["comparisons"]:
            check(stem+" "+pair["label"],max(pair["state_error"],*pair["physical_errors"].values())<GATE,pair["state_error"])
        check(stem+" zero/parity",report["zero"] and max(report["parity"],report["parity_sources"])<GATE)
        for tag,item in report["algebra"].items():
            check(stem+" "+tag+" Einstein constraints",max(item.values())<ALGEBRA)
        for tag,item in report["balance"].items():
            check(stem+" "+tag+" raw continuity/momentum",max(item["raw_continuity"],item["raw_momentum"])<GATE)
            check(stem+" "+tag+" raw integrated balance",max(*item["integrals"][0]["raw_error"],*item["integral_refinement"])<GATE)
            check(stem+" "+tag+" balance source",digest(ROOT/"comparison-roundtrip"/item["file"])==item["sha256"])
        for tag,item in report["metric"].items():
            check(stem+" "+tag+" integrated metric",item["passed"] and item["physical_Phi_integral_errors"][0]<GATE)
            check(stem+" "+tag+" metric source",digest(ROOT/"comparison-roundtrip"/item["file"])==item["sha256"])
        newton=report["newton"]
        check(stem+" Newton-source identity",newton["split_error"]<ALGEBRA)
        check(stem+" Newton-source velocity",max(newton["velocity_replay_error"],newton["source_refinement"])<GATE)
        check(stem+" Newton-source bound",newton["bound_excess"]<ALGEBRA)
        check(stem+" force evidence",digest(ROOT/"comparison-roundtrip"/newton["file"])==newton["sha256"])
        scale=report["scale_test"]
        derived=3*scale["H_over_k"]*scale["current_over_density"]+2*scale["shear_over_density"]
        check(stem+" exact force bound",derived==scale["triangle_bound"] and scale["poisson_normalized_force_error"]<=derived+ALGEBRA)
        check(stem+" no fictitious dust averaging",model=="cold" or "not an averaged" in scale["heavy"]["pressure_scope"])
    with (ROOT/"wavelength-comparison.csv").open(newline="") as stream:
        csv_rows=list(csv.DictReader(stream))
    check("all six CSV rows",len(csv_rows)==6 and {row["label"] for row in csv_rows}=={"half","balanced","double"} and {row["model"] for row in csv_rows}=={"heavy","cold"})
    check("CSV checksum",digest(ROOT/"wavelength-comparison.csv")==comparison["csv_sha256"])
    coverage=BRIDGE/"final-stable-real-batch-rays037-038/common-coverage.json"
    check("original scattering bank",digest(coverage)=="95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    check("no bytecode directories",not list(ROOT.rglob("__pycache__")))
    for label in ("build-01","inventory-01","full-build-01","waves-02","roundtrip-01","comparison-02"):
        check("successful owned receipt "+label,read(ROOT/(label+".end.json"))["exit_code"]==0)
    result=dict(passed=all(row["passed"] for row in rows),count=len(rows),checks=rows,
                comparison_sha256=digest(ROOT/"comparison-roundtrip-result.json"),prediction_sha256=digest(ROOT/"prediction-bound-result.json"),
                inventory_sha256=digest(ROOT/"inventory-result.json"),source_hashes={str(path):digest(path) for path in ROOT.glob("*.py")},
                gate=GATE,algebra_gate=ALGEBRA)
    write(ROOT/"validation-result.json",result)
    print(dict(passed=result["passed"],count=len(rows),failed=[row for row in rows if not row["passed"]]),flush=True)
    require(result["passed"],"validation failed")

if __name__=="__main__":
    main()

