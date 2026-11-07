import ast
import csv
from pathlib import Path
from common import ROOT, ADAPTER, BACKGROUND, COUPLED, HIERARCHY, BRIDGE, GATE, ALGEBRA, modest, guard, check_prior, require, read, write, digest, load
import numpy as np

def main():
    modest()
    check_prior()
    rows=[]
    def check(label,passed,value=None):
        rows.append(dict(check=label,passed=bool(passed),value=value))
    prediction=read(ROOT/"prediction-configured-result.json")
    comparison=read(ROOT/"comparison-algebra-result.json")
    build=read(ROOT/"build/build-result.json")
    check("paired evolution completed",prediction["state"]=="complete" and len(prediction["reports"])==2)
    check("paired comparisons",comparison["passed"] and len(comparison["reports"])==2)
    check("frozen gates",comparison["numerical_gate"]==GATE and comparison["algebra_gate"]==ALGEBRA)
    check("prediction owner",prediction["source_sha256"]==digest(ROOT/"run_evolution_configured.py"))
    check("comparison owner",comparison["source_sha256"]==digest(ROOT/"check_evolution_algebra.py"))
    check("comparison predicts same inputs",comparison["prediction_result_sha256"]==digest(ROOT/"prediction-configured-result.json"))
    check("native build owner",build["dll_sha256"]==digest(ROOT/"build/native/camb/cambdll.dll"))
    check("compiled adapter",build["source_sha256"]==digest(ROOT/"build/camb_python.f90"))
    for path,checksum in build["reused_bridge_hashes"].items():
        check("bridge object preserved "+Path(path).name,digest(path)==checksum)
        check("bridge object reused "+Path(path).name,digest(ROOT/"build"/Path(path).name)==checksum)
    for path,checksum in build["reused_object_module_hashes"].items():
        check("original object preserved "+Path(path).name,digest(path)==checksum)
    for path,checksum in build["original_input_hashes"].items():
        check("original parent preserved "+path,digest(path)==checksum)
    adapter=(ROOT/"build/camb_python.f90").read_text()
    original=(ADAPTER/"build/camb_python.f90").read_text()
    start=adapter.index("    subroutine mts_evolution_point(")
    end=adapter.index("    subroutine GetAllocatableSize",start)
    check("only Friedmann adapter added",adapter[:start].rstrip()==original[:original.index("    subroutine GetAllocatableSize")].rstrip() and adapter[end:]==original[original.index("    subroutine GetAllocatableSize"):])
    check("temporary mappings removed",build["temporary_mappings_removed"] and all(not Path(drive).exists() for drive in ("R:/","S:/","T:/")))
    config=read(ROOT/"run-configured.json")
    check("case schema explicitly frozen",len(config["cases"])==8 and all(len(case)==6 for case in config["cases"]))
    check("same frozen cases",config["cases"]==[["L64-base",64,False,2e-11,1.,"dop-half-cap"],["L64-fine",64,False,2e-12,1.,"dop-half-cap"],
                                             ["L128-base",128,False,2e-11,1.,"dop-half-cap"],["L128-fine",128,False,2e-12,1.,"dop-half-cap"],
                                             ["G192-fine",192,True,2e-12,1.,"dop-half-cap"],["L64-zero",64,False,2e-11,0.,"dop-half-cap"],
                                             ["L64-negative",64,False,2e-11,-1.,"dop-half-cap"],["L128-background-fine",128,False,2e-12,1.,"dop-fine"]])
    failure=read(ROOT/"prediction-result.json")
    check("pre-solver configuration failure retained",failure["state"]=="failed" and "expected 6, got 5" in failure["error"])
    check("no failed numerical solve retried",len(list((ROOT/"runs").rglob("*-status.json")))==0)
    check("failed runner source retained",digest(ROOT/"run_evolution.py")==read(ROOT/"evolution-01.end.json")["source_sha256"])
    domain=read(ROOT/"comparison-domain-diagnostic.json")
    check("one ULP cross-library diagnostic",len(domain["records"])==16 and all(row["maximum_ulps"]<=1 and row["observer_scale_exact"] for row in domain["records"]))
    check("failed comparison retained",read(ROOT/"comparison-01.end.json")["exit_code"]!=0 and (ROOT/"COMPARISON-DOMAIN-REPAIR.md").exists())
    for path in ROOT.glob("*.py"):
        text=path.read_text()
        ast.parse(text)
        compile(text,str(path),"exec")
        check("python syntax "+path.name,True)
    for model in prediction["reports"]:
        guard()
        name=model["model"]
        root=ROOT/"runs-configured"/name
        initial=load(root/"initial-context.npz")
        physical=load(BACKGROUND/"inputs"/(name+"-input.npz"))
        capture=read(root/"capture-check.json")
        check(name+" exact initial capture",all(capture[key] for key in ("exact_state","exact_rate","exact_observer","exact_signature")))
        check(name+" disabled operator",model["old_operator_error"] < ALGEBRA,model["old_operator_error"])
        embedding=read(root/"embedding-check.json")
        check(name+" angular embedding",embedding["error"]<ALGEBRA,embedding["error"])
        check(name+" eight cases",len(model["cases"])==8)
        for case in model["cases"]:
            tag=case["tag"]
            packet=load(root/case["file"])
            check(name+" "+tag+" sealed output",digest(root/case["file"])==case["sha256"])
            status=read(root/(tag+"-status.json"))
            check(name+" "+tag+" solver",status["success"] and status["returned_points"]==len(physical["efold"]))
            check(name+" "+tag+" identical physical grid",np.array_equal(packet["efold"],physical["efold"]))
            check(name+" "+tag+" initial physical time",packet["times"][0]==float(physical["initial_time"]))
            check(name+" "+tag+" initial perturbation",np.array_equal(packet["projected_state"][0],case["amplitude"]*initial["initial"]))
            check(name+" "+tag+" shape",packet["projected_state"].shape==(len(physical["efold"]),len(initial["initial"])) and packet["terms"].shape==(len(physical["efold"]),7,7))
            check(name+" "+tag+" finite",all(np.isfinite(value).all() for value in packet.values() if value.dtype.kind in "fci"))
            check(name+" "+tag+" monotone clock",np.all(np.diff(packet["times"])>0))
            check(name+" "+tag+" same native a",np.array_equal(packet["a"],packet["observer"][:,27]))
            check(name+" "+tag+" same native clock",np.array_equal(packet["times"],packet["observer"][:,29]))
            check(name+" "+tag+" Friedmann source",case["hubble_consistency"]<ALGEBRA,case["hubble_consistency"])
            check(name+" "+tag+" H positive",np.min(packet["H"])>0)
            check(name+" "+tag+" exact-heavy regime",np.max(packet["a"])<.00028)
            check(name+" "+tag+" clock differential",np.max(abs(packet["background_points"][:,9]*packet["H"]-1))<GATE)
            check(name+" "+tag+" frozen tolerances",case["rtol"] in (2e-11,2e-12) and case["atol"]==case["rtol"]/100)
            check(name+" "+tag+" frozen phase cap",case["max_step_N"]==float(physical["step_cap"])/2)
            del packet
        paired=next(row for row in comparison["reports"] if row["model"]==name)
        check(name+" comparison accepted",paired["passed"])
        for item in paired["comparisons"]:
            check(name+" "+item["label"]+" convergence",max(item["state_error"],*item["physical_errors"].values())<GATE,item["state_error"])
        check(name+" zero control",paired["zero_state"] and paired["zero_sources"])
        check(name+" sign control",max(paired["negative_state"],*paired["negative_sources"].values())<GATE)
        for tag,record in paired["algebra"].items():
            for label,value in record.items():
                check(name+" "+tag+" Einstein "+label,value<ALGEBRA,value)
        for tag,record in paired["balance"].items():
            check(name+" "+tag+" raw conservation",max(record["raw_continuity"],record["raw_momentum"])<GATE,[record["raw_continuity"],record["raw_momentum"]])
            check(name+" "+tag+" integrated conservation",max(*record["integrals"][0]["raw_error"],*record["integral_refinement"])<GATE)
            check(name+" "+tag+" balance decomposition",max(*record["algebra"],*record["source_errors"].values())<ALGEBRA)
        for tag,record in paired["metric"].items():
            check(name+" "+tag+" independent metric evolution",max(record["physical_Phi_integral_errors"][0],record["source_refinement"])<GATE)
            check(name+" "+tag+" geometry rate",record["geometry_rate_identity"]<ALGEBRA)
        for tag,record in paired["newton"].items():
            check(name+" "+tag+" Newton force identity",record["split_error"]<ALGEBRA)
            check(name+" "+tag+" force replay",max(record["velocity_replay_error"],record["source_refinement"])<GATE)
            check(name+" "+tag+" interpolant bound",record["bound_excess"]<ALGEBRA)
            check(name+" "+tag+" approximation not promoted","not independently evolved Poisson" in record["scope"])
        for category in ("balance","metric","newton"):
            for tag,record in paired[category].items():
                check(name+" "+category+" "+tag+" evidence",digest(ROOT/"comparison-algebra"/record["file"])==record["sha256"])
    with (ROOT/"physical-comparison.csv").open(newline="") as stream:
        table=list(csv.DictReader(stream))
    check("paired CSV",len(table)==22 and {row["model"] for row in table}=={"heavy","cold"})
    check("CSV checksum",comparison["csv_sha256"]==digest(ROOT/"physical-comparison.csv"))
    coverage=BRIDGE/"final-stable-real-batch-rays037-038/common-coverage.json"
    check("scattering preserved",digest(coverage)=="95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    for label in ("build-01","evolution-02","domain-01","comparison-02"):
        check("successful receipt "+label,read(ROOT/(label+".end.json"))["exit_code"]==0)
    check("no bytecode directories",not list(ROOT.rglob("__pycache__")))
    result=dict(passed=all(row["passed"] for row in rows),count=len(rows),checks=rows,
                comparison_sha256=digest(ROOT/"comparison-algebra-result.json"),prediction_sha256=digest(ROOT/"prediction-configured-result.json"),
                source_hashes={str(path):digest(path) for path in ROOT.glob("*.py")},gate=GATE,algebra_gate=ALGEBRA)
    write(ROOT/"validation-result.json",result)
    print(dict(passed=result["passed"],count=len(rows),failed=[row for row in rows if not row["passed"]]),flush=True)
    require(result["passed"],"validation failed")

if __name__=="__main__":
    main()

