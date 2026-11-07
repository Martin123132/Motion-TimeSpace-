import ast
import csv
from common import ROOT, WAVELENGTH, AVERAGE, ENVELOPE, NORMAL, MEAN, BACKGROUND, BRIDGE, GATE, ALGEBRA, modest, guard, check_prior, require, read, write, digest, load
import numpy as np


def main():
    modest()
    check_prior()
    owner=read(ROOT/"prediction-result.json")
    comparison=read(ROOT/"comparison-result.json")
    identities=read(ROOT/"symbolic-identities.json")
    mean=read(MEAN/"harmonic-identities.json")
    decomposition=read(MEAN/"decomposition-result.json")
    from second_symbolic import verify
    second_identities=verify()
    write(ROOT/"second-identities.json",dict(**second_identities,source_sha256=digest(ROOT/"second_symbolic.py")))
    rows=[]
    summaries=[]
    def check(name,passed,value=None):
        rows.append(dict(check=name,passed=bool(passed),value=value))
    check("42 completed evolutions",owner["state"]=="complete" and len(owner["reports"])==6 and sum(len(row["cases"]) for row in owner["reports"])==42)
    check("paired implementation valid",comparison["implementation_valid"] and len(comparison["reports"])==6)
    check("same gates",comparison["gate"]==GATE and comparison["algebra_gate"]==ALGEBRA)
    check("driver owned",owner["source_sha256"]==digest(ROOT/"run_second.py"))
    check("checker owned",comparison["source_sha256"]==digest(ROOT/"check_second.py"))
    check("comparison input",comparison["prediction_sha256"]==digest(ROOT/"prediction-result.json"))
    check("retained averaging source",comparison["retained_averaging_sha256"]==digest(AVERAGE/"derive_and_test_common_domain.py"))
    check("parent closeout",owner["previous_closeout_sha256"]==digest(MEAN/"closeout.json"))
    check("configuration frozen",owner["run_config_sha256"]==digest(ROOT/"run-config.json"))
    check("protocol frozen",read(ROOT/"run-config.json")["protocol_sha256"]==digest(ROOT/"PROTOCOL.md"))
    check("eight carrier identities",identities["passed"] and len(identities["identities"])==8 and set(identities["identities"].values())=={"0"})
    check("carrier algebra source",identities["source_sha256"]==digest(ROOT/"envelope_math.py"))
    check("four harmonic/IBP identities",mean["passed"] and len(mean["identities"])==4 and set(mean["identities"].values())=={"0"})
    check("harmonics source",mean["source_sha256"]==digest(ROOT/"harmonics.py") and owner["harmonics_sha256"]==digest(ROOT/"harmonics.py"))
    check("near-identity candidate source",owner["near_identity_sha256"]==digest(ROOT/"micromotion.py"))
    check("decomposition frozen",owner["decomposition_sha256"]==digest(MEAN/"decomposition-result.json"))
    check("six decompositions",decomposition["passed"] and len(decomposition["reports"])==6 and decomposition["no_new_evolution"] and decomposition["coefficients_not_fitted"])
    check("decomposition source",decomposition["source_sha256"]==digest(MEAN/"decompose.py"))
    check("six second-map identities",second_identities["passed"] and len(second_identities["identities"])==6)
    check("retained first-map source",owner["parent_map_sha256"]==digest(ROOT/"near_identity_parent.py"))
    check("explicit candidate identity",owner["second_micromotion_candidate"] and comparison["second_micromotion_candidate"])
    check("reused controls owned",comparison["previous_normal_prediction_sha256"]==digest(NORMAL/"prediction-owned-result.json"))
    for item in decomposition["reports"]:
        prefix=item["model"]+" "+item["label"]+" decomposition "
        check(prefix+"source",digest(item["input"])==item["input_sha256"])
        check(prefix+"accepted",item["passed"])
        if item["model"]=="heavy":
            check(prefix+"reconstruction",max(item["reconstruction_per_amplitude"],item["reconstruction_per_remainder"])<ALGEBRA)
            check(prefix+"output",digest(MEAN/"decomposition"/item["output"])==item["output_sha256"])
            check(prefix+"IBP",item["rapid_integral"]["passed"])
        else:
            check(prefix+"zero",item["cold_exact_zero"])
    for script in ROOT.glob("*.py"):
        source=script.read_text()
        compile(source,str(script),"exec")
        check("syntax "+script.name,True)
        if script.name in ("run_second.py","check_second.py"):
            check("no inherited fixed k "+script.name,not any(isinstance(node,ast.Name) and node.id=="WAVE" for node in ast.walk(ast.parse(source))))
    expected_tags={"L128-full-fine","G192-full-fine","L128-reduced-base","L128-reduced-fine","G192-reduced-fine","L128-reduced-zero","L128-reduced-coarse"}
    for family in owner["reports"]:
        guard()
        model,label,wave=family["model"],family["label"],family["wave"]
        stem=model+"-"+label
        folder=ROOT/"runs-second"/stem
        initial=load(folder/"initial-context.npz")
        original=load(WAVELENGTH/"runs-bound"/stem/"initial-context.npz")
        grid=load(BACKGROUND/"inputs"/(model+"-input.npz"))
        check(stem+" original native preparation",np.array_equal(initial["initial"],original["initial"]))
        check(stem+" original operator units",np.array_equal(initial["old_normalization"],original["old_normalization"]))
        check(stem+" no future perturbation forcing",family["no_future_species_histories_supplied"])
        check(stem+" case matrix",set(row["tag"] for row in family["cases"])==expected_tags and len(family["cases"])==7)
        check(stem+" embedding",read(folder/"embedding-check.json")["error"]<ALGEBRA)
        capture=read(folder/"capture-check.json")
        check(stem+" native capture",all(capture[name] for name in ("same_seed","zero_unselected","source_preserved","exact_initial_rate","exact_initial_observer")))
        table=read(folder/"micromotion-table-check.json")
        check(stem+" background-only coefficient table",table["passed"] and table["background_only"])
        if model=="heavy":
            check(stem+" coefficient source",table["source_sha256"]==digest(ROOT/"micromotion.py") and table["no_future_perturbations"])
            check(stem+" coefficient packet",digest(folder/table["output"])==table["output_sha256"])
            check(stem+" coefficient independent checks",table["support_error"]<ALGEBRA and max(table["midpoint_interpolation_error"],table["coefficient_derivative_refinement_per_unit"])<GATE and table["probes"]==97)
        for case in family["cases"]:
            tag=case["tag"]
            prefix=stem+" "+tag+" "
            packet=load(folder/case["file"])
            status=read(folder/(tag+"-status.json"))
            transform=read(folder/(tag+"-transform-check.json"))
            normal=read(folder/(tag+"-normal-check.json"))
            check(prefix+"packet",digest(folder/case["file"])==case["sha256"])
            check(prefix+"solver",status["success"] and status["returned_points"]==len(grid["efold"]))
            check(prefix+"physical grid",np.array_equal(packet["efold"],grid["efold"]))
            check(prefix+"finite",all(np.isfinite(value).all() for value in packet.values() if value.dtype.kind in "fci"))
            check(prefix+"unchanged tolerances",case["rtol"] in (2e-11,2e-12) and case["atol"]==case["rtol"]/100)
            check(prefix+"unchanged step cap",case["max_step_N"]==float(grid["step_cap"])/2)
            check(prefix+"unchanged background",case["background"]=="dop-half-cap")
            check(prefix+"physical clock",np.array_equal(packet["a"],packet["observer"][:,27]) and np.array_equal(packet["times"],packet["observer"][:,29]))
            check(prefix+"source H",case["hubble_consistency"]<ALGEBRA)
            check(prefix+"carrier preflight",max(transform["inverse_error"],transform["chain_error"])<ALGEBRA and transform["carrier_from_background_only"] and transform["no_terms_dropped"])
            check(prefix+"carrier phase",case["phase_offset"]==0 and transform["phase_offset"]==0)
            check(prefix+"normal inverse",normal["inverse_error"]<ALGEBRA)
            check(prefix+"normal chain",max(normal["chain_error"],normal["derivative_refinement"],normal["parity"])<GATE and normal["zero_exact"])
            check(prefix+"candidate label",case["reduced_candidate"]==("-reduced-" in tag))
            check(prefix+"coefficient resolution",case["coarse_coefficients"]==tag.endswith("-coarse") and normal["coarse_coefficients"]==tag.endswith("-coarse"))
            if "-full-" in tag:
                control=read(folder/(tag+"-control-check.json"))
                check(prefix+"inline full control",control["passed"] and control["state_error"]<GATE and case["inline_full_control_error"]<GATE)
                check(prefix+"inline control source",control["parent_sha256"]==digest(NORMAL/"runs-owned"/stem/(tag+".npz")))
            if model=="heavy":
                check(prefix+"normal pair",packet["normal_amplitude"].shape==(len(grid["efold"]),2) and packet["envelope"].shape==(len(grid["efold"]),2))
                check(prefix+"invertible query domain",np.max(packet["correction_size"])<1 and np.all(packet["inverse_bound"]>=1))
            else:
                check(prefix+"cold identity",packet["normal_amplitude"].shape==(len(grid["efold"]),0) and len(packet["envelope_slots"])==0 and np.array_equal(packet["units"],packet["envelope_units"]))
            if not case["reduced_candidate"] or model=="cold":
                check(prefix+"no physical rate modification",np.count_nonzero(packet["derivative_defect"])==0 and np.count_nonzero(packet["stress_rate_correction"])==0)
            if case["amplitude"]==0:
                check(prefix+"zero state",np.count_nonzero(packet["projected_state"])==0)
            del packet
        report=next(row for row in comparison["reports"] if row["model"]==model and row["label"]==label)
        check(stem+" implementation",report["implementation_valid"] and report["numerical_passed"] and report["full_physics_passed"] and report["accounted_passed"])
        for item in report["comparisons"]:
            numerical=max(item["state_error"],*item["physical_errors"].values())<GATE
            check(stem+" comparison flag "+item["label"],item["within_gate"]==numerical)
            if item["kind"]!="approximation":
                check(stem+" convergence "+item["label"],numerical)
        for tag,values in report["algebra"].items():
            check(stem+" "+tag+" algebraic constraints",max(values["Hamiltonian"],values["slip"])<ALGEBRA)
            if "-full-" in tag:
                check(stem+" "+tag+" Einstein momentum",values["momentum"]<ALGEBRA)
        for category in ("balance","metric","rotating","normal","averages","newton"):
            for tag,item in report[category].items():
                check(stem+" "+tag+" "+category+" source",digest(ROOT/"comparison"/item["file"])==item["sha256"])
                if category=="balance":
                    check(stem+" "+tag+" accounted stress",item["accounted_passed"])
                elif category in ("rotating","normal","averages") or "-full-" in tag:
                    check(stem+" "+tag+" "+category+" verified",item["passed"])
        for tag,item in report["metric_accounted"].items():
            check(stem+" "+tag+" actual metric evolution",item["passed"])
        full_average=max(value for item in report["average_comparisons"]["G192-full-fine"].values() for value in item.values())
        reduced_average=max(value for item in report["average_comparisons"]["G192-reduced-fine"].values() for value in item.values())
        check(stem+" full averaged agreement",full_average<GATE)
        reduced_tags=[tag for tag in report["balance"] if "-reduced-" in tag]
        independent_qualification=(
            all(item["within_gate"] for item in report["comparisons"] if item["kind"]=="approximation") and reduced_average<GATE
            and all(report["balance"][tag]["passed"] and max(report["metric"][tag]["physical_Phi_integral_errors"][0],report["metric"][tag]["source_refinement"],report["metric"][tag]["geometry_rate_identity"],report["algebra"][tag]["momentum"])<GATE for tag in reduced_tags)
            and report["newton"]["G192-reduced-fine"]["passed"])
        check(stem+" qualification matches evidence",report["reduced_candidate_qualified"]==independent_qualification)
        control=next(item for item in report["comparisons"] if item["label"]=="full parent192")
        reduced=next(item for item in report["comparisons"] if item["label"]=="reduced physical error192")
        normal=report["normal"].get("G192-reduced-fine",{})
        summaries.append(dict(model=model,label=label,wave=wave,implementation_valid=report["implementation_valid"],
                              reduced_candidate_qualified=report["reduced_candidate_qualified"],full_state_error=control["state_error"],
                              full_physical_error=max(control["physical_errors"].values()),reduced_state_error=reduced["state_error"],
                              reduced_physical_error=max(reduced["physical_errors"].values()),full_average_error=full_average,reduced_average_error=reduced_average,
                              reduced_raw_continuity=report["balance"]["G192-reduced-fine"]["raw_continuity"],
                              reduced_raw_momentum=report["balance"]["G192-reduced-fine"]["raw_momentum"],
                              reduced_metric_integral=report["metric"]["G192-reduced-fine"]["physical_Phi_integral_errors"][0],
                              maximum_inverse_bound=normal.get("maximum_inverse_bound",1.)))
    check("overall qualification matches families",comparison["reduced_all_qualified"]==all(row["reduced_candidate_qualified"] for row in comparison["reports"]))
    for label in ("second-01","comparison-01"):
        check("receipt "+label,read(ROOT/(label+".end.json"))["exit_code"]==0)
    check("original scattering unchanged",digest(BRIDGE/"final-stable-real-batch-rays037-038/common-coverage.json")=="95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    check("no bytecode",not list(ROOT.rglob("__pycache__")))
    with (ROOT/"second-micromotion-comparison.csv").open("x",newline="",encoding="utf-8") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(summaries[0]))
        writer.writeheader()
        writer.writerows(summaries)
    result=dict(passed=all(row["passed"] for row in rows),count=len(rows),checks=rows,
                source_hashes={str(path):digest(path) for path in ROOT.glob("*.py")},
                prediction_sha256=digest(ROOT/"prediction-result.json"),comparison_sha256=digest(ROOT/"comparison-result.json"),
                mean_identity_sha256=digest(MEAN/"harmonic-identities.json"),decomposition_sha256=digest(MEAN/"decomposition-result.json"),csv_sha256=digest(ROOT/"second-micromotion-comparison.csv"),
                scope="verifies implementation and honest qualification decisions; does not require the tested truncation to be physically successful")
    write(ROOT/"validation-result.json",result)
    print(dict(passed=result["passed"],count=len(rows),failed=[row for row in rows if not row["passed"]]),flush=True)
    require(result["passed"],"validation failed; preserve and inspect")


if __name__=="__main__":
    main()

