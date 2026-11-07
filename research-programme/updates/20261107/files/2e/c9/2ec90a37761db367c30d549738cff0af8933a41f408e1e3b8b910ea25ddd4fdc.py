import ast
import csv
from pathlib import Path
from common import ROOT, WAVELENGTH, AVERAGE, BACKGROUND, BRIDGE, GATE, ALGEBRA, modest, guard, check_prior, require, read, write, digest, load
import numpy as np


def main():
    modest()
    check_prior()
    owner=read(ROOT/"prediction-envelope-result.json")
    comparison=read(ROOT/"comparison-result.json")
    identities=read(ROOT/"symbolic-identities.json")
    rows=[]
    summaries=[]
    def check(name,passed,value=None):
        rows.append(dict(check=name,passed=bool(passed),value=value))
    check("36 complete forward solves",owner["state"]=="complete" and len(owner["reports"])==6 and sum(len(row["cases"]) for row in owner["reports"])==36)
    check("all paired comparisons pass",comparison["passed"] and len(comparison["reports"])==6)
    check("same gates",comparison["gate"]==GATE and comparison["algebra_gate"]==ALGEBRA)
    check("driver owned",owner["source_sha256"]==digest(ROOT/"run_envelope.py"))
    check("checker owned",comparison["source_sha256"]==digest(ROOT/"check_envelope.py"))
    check("comparison input",comparison["prediction_sha256"]==digest(ROOT/"prediction-envelope-result.json"))
    check("retained averaging implementation",comparison["averaging_function_sha256"]==digest(AVERAGE/"derive_and_test_common_domain.py"))
    check("parent averaged result",comparison["parent_averaging_sha256"]==digest(AVERAGE/"result-common.json"))
    check("eight symbolic identities",identities["passed"] and len(identities["identities"])==8 and set(identities["identities"].values())=={"0"})
    check("symbolic source",identities["source_sha256"]==digest(ROOT/"envelope_math.py"))
    for script in ROOT.glob("*.py"):
        text=script.read_text()
        compile(text,str(script),"exec")
        check("syntax "+script.name,True)
        if script.name in ("run_envelope.py","check_envelope.py"):
            check("no inherited fixed wavenumber "+script.name,not any(isinstance(node,ast.Name) and node.id=="WAVE" for node in ast.walk(ast.parse(text))))
    for family in owner["reports"]:
        guard()
        model,label,wave=family["model"],family["label"],family["wave"]
        stem=model+"-"+label
        folder=ROOT/"runs-envelope"/stem
        initial=load(folder/"initial-context.npz")
        parent_initial=load(WAVELENGTH/"runs-bound"/stem/"initial-context.npz")
        supplied=load(BACKGROUND/"inputs"/(model+"-input.npz"))
        check(stem+" same native initial state",np.array_equal(initial["initial"],parent_initial["initial"]))
        check(stem+" same initial-operator units",np.array_equal(initial["old_normalization"],parent_initial["old_normalization"]))
        check(stem+" no future perturbation source",family["no_future_species_histories_supplied"])
        check(stem+" native embedding",read(folder/"embedding-check.json")["error"]<ALGEBRA)
        capture=read(folder/"capture-check.json")
        check(stem+" native capture verified",all(capture[name] for name in ("same_seed","zero_unselected","source_preserved","exact_initial_rate","exact_initial_observer")))
        for case in family["cases"]:
            tag=case["tag"]
            packet=load(folder/case["file"])
            check(stem+" "+tag+" packet",digest(folder/case["file"])==case["sha256"])
            status=read(folder/(tag+"-status.json"))
            check(stem+" "+tag+" solve success",status["success"] and status["returned_points"]==len(supplied["efold"]))
            check(stem+" "+tag+" same physical grid",np.array_equal(packet["efold"],supplied["efold"]))
            check(stem+" "+tag+" finite",all(np.isfinite(value).all() for value in packet.values() if value.dtype.kind in "fci"))
            check(stem+" "+tag+" same tolerance",case["rtol"] in (2e-11,2e-12) and case["atol"]==case["rtol"]/100)
            check(stem+" "+tag+" same phase-step cap",case["max_step_N"]==float(supplied["step_cap"])/2)
            check(stem+" "+tag+" actual native a/time",np.array_equal(packet["a"],packet["observer"][:,27]) and np.array_equal(packet["times"],packet["observer"][:,29]))
            check(stem+" "+tag+" source H",case["hubble_consistency"]<ALGEBRA)
            transform=read(folder/(tag+"-transform-check.json"))
            check(stem+" "+tag+" exact coordinate preflight",max(transform["inverse_error"],transform["chain_error"])<ALGEBRA)
            check(stem+" "+tag+" no dropped terms",transform["no_terms_dropped"] and transform["carrier_from_background_only"])
            expected_shift=np.pi/4 if tag.endswith("-shift") else 0.
            check(stem+" "+tag+" frozen carrier phase",case["phase_offset"]==expected_shift and transform["phase_offset"]==expected_shift)
            check(stem+" "+tag+" model-specific transform",transform["heavy_transformed"]==(model=="heavy"))
            if model=="heavy":
                slots=packet["envelope_slots"]
                check(stem+" "+tag+" invertible pair",slots.shape==(2,) and packet["envelope"].shape==(len(packet["a"]),2) and float(packet["mass"])>0)
                check(stem+" "+tag+" common positive amplitude units",np.all(packet["envelope_units"]>0) and packet["envelope_units"][slots[0]]==packet["envelope_units"][slots[1]])
            else:
                check(stem+" "+tag+" identity cold coordinates",packet["envelope"].shape==(len(packet["a"]),0) and len(packet["envelope_slots"])==0 and np.array_equal(packet["units"],packet["envelope_units"]))
            del packet
        report=next(row for row in comparison["reports"] if row["model"]==model and row["label"]==label)
        check(stem+" accepted",report["passed"])
        for row in report["comparisons"]:
            check(stem+" "+row["label"],row["passed"] and max(row["state_error"],*row["source_errors"].values())<GATE)
        check(stem+" zero/sign",report["zero"] and max(report["parity"],report["parity_sources"])<GATE)
        for tag,values in report["algebra"].items():
            check(stem+" "+tag+" Einstein constraints",max(values.values())<ALGEBRA)
        for category in ("balance","metric","rotating"):
            for tag,row in report[category].items():
                check(stem+" "+tag+" "+category+" pass",row["passed"])
                check(stem+" "+tag+" "+category+" packet",digest(ROOT/"comparison"/row["file"])==row["sha256"])
        check(stem+" averaged predictions",report["averages"]["passed"] and all(row["passed"] and max(row["errors"].values())<GATE for row in report["average_comparisons"].values()))
        check(stem+" averaged source",digest(ROOT/"comparison"/report["averages"]["file"])==report["averages"]["sha256"])
        check(stem+" force identity/budget",report["newton"]["passed"])
        check(stem+" force source",digest(ROOT/"comparison"/report["newton"]["file"])==report["newton"]["sha256"])
        native=next(row for row in report["comparisons"] if row["label"]=="forward native G192")
        shift=next(row for row in report["comparisons"] if row["label"]=="carrier phase offset")
        average_error=max(value for row in report["average_comparisons"].values() for value in row["errors"].values())
        summaries.append(dict(model=model,label=label,wave=wave,native_state_error=native["state_error"],
                              native_source_error=max(native["source_errors"].values()),carrier_offset_error=max(shift["state_error"],*shift["source_errors"].values()),
                              averaged_pressure_source_error=average_error,raw_continuity=report["balance"]["G192-envelope-fine"]["raw_continuity"],
                              metric_integral=report["metric"]["G192-envelope-fine"]["physical_Phi_integral_errors"][0],
                              envelope_integral=max([row["integral_errors"][0] for row in report["rotating"].values()] or [0.])))
    with (ROOT/"forward-envelope-comparison.csv").open("x",newline="",encoding="utf-8") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(summaries[0]))
        writer.writeheader()
        writer.writerows(summaries)
    for label in ("envelope-01","comparison-01"):
        check("receipt "+label,read(ROOT/(label+".end.json"))["exit_code"]==0)
    check("original scattering unchanged",digest(BRIDGE/"final-stable-real-batch-rays037-038/common-coverage.json")=="95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    check("no bytecode",not list(ROOT.rglob("__pycache__")))
    result=dict(passed=all(row["passed"] for row in rows),count=len(rows),checks=rows,
                source_hashes={str(path):digest(path) for path in ROOT.glob("*.py")},
                prediction_sha256=digest(ROOT/"prediction-envelope-result.json"),comparison_sha256=digest(ROOT/"comparison-result.json"),
                csv_sha256=digest(ROOT/"forward-envelope-comparison.csv"))
    write(ROOT/"validation-result.json",result)
    print(dict(passed=result["passed"],count=len(rows),failed=[row for row in rows if not row["passed"]]),flush=True)
    require(result["passed"],"validation failed; preserve and inspect")

if __name__=="__main__":
    main()

