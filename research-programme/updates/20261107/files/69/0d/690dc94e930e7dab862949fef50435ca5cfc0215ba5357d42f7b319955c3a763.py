import ast
import csv
from common import ROOT, POST, PRIOR, BRIDGE, GATE, ALGEBRA, modest, guard, require, read, write, digest, load, verify_parent
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.integrate import simpson


def sup(values):
    return float(np.max(abs(values)))


def main():
    modest()
    verify_parent()
    result=read(ROOT/"result-common.json")
    config=read(ROOT/"config-common.json")
    plans=read(ROOT/"frozen-common-windows.json")
    domain=read(ROOT/"common-domain.json")
    legacy=read(ROOT/"symbolic-identities.json")
    current=read(ROOT/"symbolic-common-identities.json")
    require(result["identities_sha256"]==digest(ROOT/"symbolic-identities.json"),"reported legacy identity owner")
    require(legacy["identities"]==current["identities"],"identical symbolic mathematics")
    require(legacy["source_sha256"]==digest(ROOT/"derive_and_test.py"),"legacy identity source")
    require(current["source_sha256"]==digest(ROOT/"derive_and_test_common_domain.py"),"current identity source")
    reconciliation=dict(passed=True,result_sha256=digest(ROOT/"result-common.json"),
                        reported_identity_path="symbolic-identities.json",reported_identity_sha256=result["identities_sha256"],
                        current_identity_path="symbolic-common-identities.json",current_identity_sha256=digest(ROOT/"symbolic-common-identities.json"),
                        identities_equal=True,original_failed_validation_sha256=digest(ROOT/"validation-result.json"),
                        explanation="The common-domain driver wrote fresh identities but its result hash still references the preserved original identical symbolic calculation. This explicit overlay links both without changing any original artifact.")
    write(ROOT/"provenance-reconciliation.json",reconciliation)
    checks=[]
    summaries=[]
    def check(name,passed,value=None):
        checks.append(dict(check=name,passed=bool(passed),value=value))
    check("six complete paired families",result["passed"] and len(result["reports"])==6)
    check("unchanged gates",config["gate"]==GATE and config["algebra"]==ALGEBRA)
    check("no new evolution",result["new_evolutions"]==0 and not result["source_bank_changed"])
    check("frozen cycle and integration counts",config["cycles"]==[1,2,4,8] and config["strides"]==[1,2,4] and config["centers"]==17)
    check("analysis source",digest(ROOT/"derive_and_test_common_domain.py")==result["source_sha256"]==config["source_sha256"])
    for field,path in (("config_sha256","config-common.json"),("windows_sha256","frozen-common-windows.json"),("identities_sha256","symbolic-identities.json")):
        check("owned "+path,digest(ROOT/path)==result[field])
    for path,checksum in config["source_hashes"].items():
        check("physical source "+path,digest(path)==checksum)
    check("current symbolic source linked explicitly",current["source_sha256"]==result["source_sha256"] and reconciliation["identities_equal"])
    check("only original provenance check failed",[row["check"] for row in read(ROOT/"validation-result.json")["checks"] if not row["passed"]]==["owned symbolic-common-identities.json"])
    symbols=read(ROOT/"symbolic-common-identities.json")
    check("four exact identities",symbols["passed"] and len(symbols["identities"])==4 and set(symbols["identities"].values())=={"0"})
    check("common domain formed before readout",domain["left"]==max(row["second"] for row in domain["rows"]) and domain["right"]==min(row["penultimate"] for row in domain["rows"]))
    check("all12 domains recorded",len(domain["rows"])==12)
    check("strictly inside shared original domains",domain["full_left"]<domain["left"]<domain["right"]<domain["full_right"])
    for script in ROOT.glob("*.py"):
        compile(script.read_text(),str(script),"exec")
        check("syntax "+script.name,True)
    for family in result["reports"]:
        guard()
        model,label,wave=family["model"],family["label"],family["wave"]
        check(model+" "+label+" family passed",family["passed"])
        phase_plan=plans[label]
        check(label+" phase source",digest(phase_plan["source"])==phase_plan["source_sha256"])
        for tag,case in family["cases"].items():
            stem=model+" "+label+" "+tag
            check(stem+" source",digest(case["input"])==case["input_sha256"])
            check(stem+" averaged packet",digest(ROOT/"results-common"/case["output"])==case["output_sha256"])
            packet=load(case["input"])
            saved=load(ROOT/"results-common"/case["output"])
            names=packet["observer_names"].tolist()
            expected={0:"R",1:"Pbar",2:"D_sync",3:"Q_sync",4:"Pi",5:"sigma",7:"eta_sync",9:"Weyl"}
            check(stem+" named observer mapping",all(names[index]==name for index,name in expected.items()),{str(index):names[index] for index in expected})
            meta,terms,obs=packet["metadata"],packet["terms"],packet["observer"]
            alpha=obs[:,5]/wave
            if model=="heavy":
                field,velocity,field_rate,velocity_rate,mass,delta,speed=[meta[:,14+index] for index in range(7)]
                omega2=(packet["a"]*mass)**2
                native_accel=-2*packet["H"]*speed-(wave**2+omega2)*delta-wave*meta[:,2]*velocity
                predicted_density_rate=velocity_rate*speed+velocity*native_accel+omega2*((2*packet["H"]*field+field_rate)*delta+field*speed)
                density_rate_error=sup(predicted_density_rate-terms[:,6,3])/max(sup(terms[:,6,3]),1e-80)
                check(stem+" actual stored derivative matches canonical RHS",density_rate_error<ALGEBRA,density_rate_error)
                gauge_pressure=alpha*(velocity*velocity_rate-packet["H"]*velocity**2-omega2*field*field_rate)
                matter_p=terms[:,6,2]+gauge_pressure
                matter_d=terms[:,6,0]-3*packet["H"]*velocity**2*alpha
            else:
                matter_p=terms[:,0,2]
                matter_d=terms[:,0,0]-3*packet["H"]*terms[:,0,5]*alpha
                check(stem+" raw CDM pressure exactly zero",np.count_nonzero(matter_p)==0)
            independent_matrix=np.column_stack([matter_d,matter_p])
            endpoint=PchipInterpolator(packet["times"],independent_matrix)
            for cycles in (1,2,4,8):
                key=str(cycles)
                window=phase_plan["windows"][key]
                row=case["windows"][key]
                left,right=saved[key+"_left"],saved[key+"_right"]
                check(stem+" "+key+" windows inside original domain",left.min()>=packet["times"][0] and right.max()<=packet["times"][-1] and np.all(right>left))
                check(stem+" "+key+" physical endpoints shared",np.min(window["efold_left"])>=domain["left"]-1e-13 and np.max(window["efold_right"])<=domain["right"]+1e-13)
                check(stem+" "+key+" complete cycles",np.max(abs(np.array(window["phase_right"])-window["phase_left"]-2*np.pi*cycles))<1e-12)
                check(stem+" "+key+" pressure identity",row["pressure_reconstruction_error"]<GATE,row["pressure_reconstruction_error"])
                check(stem+" "+key+" integration refinement",max(row["integration_refinement"].values())<GATE)
                check(stem+" "+key+" averaged force split",row["force_identity"]<ALGEBRA and row["force_error"]<=row["force_bound"]+ALGEBRA)
                check(stem+" "+key+" force refinement",row["force_refinement"]<GATE)
                independent=[]
                for start,end in zip(left,right):
                    inside=(packet["times"]>start)&(packet["times"]<end)
                    times=np.r_[start,packet["times"][inside],end]
                    values=np.vstack([endpoint(start),independent_matrix[inside],endpoint(end)])
                    independent.append(simpson(values,x=times,axis=0)/(end-start))
                independent=np.array(independent)
                target=np.column_stack([saved[key+"_matter_D"],saved[key+"_matter_P"]])
                density_scale=max(sup(target[:,0]),1e-80)
                simpson_error=sup(independent-target)/density_scale
                check(stem+" "+key+" independent Simpson/PCHIP integration",simpson_error<GATE,simpson_error)
                pressure_ratio=sup(target[:,1])/density_scale
                if model=="cold":
                    check(stem+" "+key+" averaged CDM pressure exactly zero",np.count_nonzero(target[:,1])==0 and row["cold_pressure_exact_zero"])
                else:
                    reconstructed=sum(saved[key+"_"+name] for name in ("gradient","boundary","expansion","metric","dense_defect","gauge"))
                    error=sup(target[:,1]-reconstructed)/density_scale
                    check(stem+" "+key+" stored component sum",error<GATE,error)
                    check(stem+" "+key+" density gauge defect negligible",row["density_gauge_defect"]<ALGEBRA)
                    check(stem+" "+key+" positive derived coefficient",0<row["coefficient_min"]<=row["coefficient_max"]<1)
                if tag=="G192-fine":
                    summaries.append(dict(model=model,label=label,wave=wave,cycles=cycles,pressure_ratio=pressure_ratio,
                                          raw_pressure_ratio=sup(matter_p)/max(sup(matter_d),1e-80),
                                          pressure_reconstruction=row["pressure_reconstruction_error"],independent_integration=simpson_error,
                                          force_error=row["force_error"],force_bound=row["force_bound"],
                                          gradient_only_error=row.get("gradient_only_error"),boundary_omission_error=row.get("boundary_omission_error"),
                                          gauge_omission_error=row.get("gauge_omission_error")))
            del packet,saved
        for cycles,row in family["angular_control"].items():
            check(model+" "+label+" angular "+cycles,max(row.values())<GATE)
    for label in ("average-01","average-02"):
        receipt=read(ROOT/(label+".end.json"))
        check("receipt "+label,receipt["exit_code"]==(1 if label=="average-01" else 0))
    check("failed analysis preserved",digest(ROOT/"derive_and_test.py")==read(ROOT/"average-01.end.json")["source_sha256"])
    check("failed analysis has no completed result",not (ROOT/"result.json").exists())
    check("original bank coverage",digest(BRIDGE/"final-stable-real-batch-rays037-038/common-coverage.json")=="95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    check("no bytecode",not list(ROOT.rglob("__pycache__")))
    with (ROOT/"averaging-summary-verified.csv").open("x",newline="",encoding="utf-8") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(summaries[0]))
        writer.writeheader()
        writer.writerows(summaries)
    summary=dict(passed=all(row["passed"] for row in checks),count=len(checks),checks=checks,
                 source_hashes={str(path):digest(path) for path in ROOT.glob("*.py")},
                 result_sha256=digest(ROOT/"result-common.json"),csv_sha256=digest(ROOT/"averaging-summary-verified.csv"),
                 exact_zero_reporting="CSV uses true sup norm in numerators; common.norm's 1e-80 scale floor in original JSON ratios is not a nonzero cold pressure")
    write(ROOT/"validation-provenance-result.json",summary)
    print(dict(passed=summary["passed"],checks=len(checks),failed=[row for row in checks if not row["passed"]],
               maximum_independent_integration=max(row["independent_integration"] for row in summaries)),flush=True)
    require(summary["passed"],"validation failed; preserve and inspect")

if __name__=="__main__":
    main()

