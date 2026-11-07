from replay_stage189 import *
from assess_stage188 import curve_decimal, relative_change, comparison_check

REPRESENTATIONS = ["saved_old", "increment64", "precision80"]
METHODS = ["partial", "split"]
QUANTITIES = previous.QUANTITIES


def assess():
    assert read(ROOT / "progress.json")["state"] == "evolution_complete"
    assert not (ROOT / "results/status.json").exists()
    config = protocol()
    paths = authenticate()
    assert paths == read(ROOT / "authenticated-inputs.json")
    checks = list(read(ROOT / "pilot/status.json")["checks"])
    with mp.workdps(80):
        for ratio in (mp.mpf(1)/2, mp.mpf(1)/4, mp.mpf(1)):
            coefficient = (1+2*ratio)/(1+ratio)
            weight = ratio**2/(1+ratio)
            for degree in range(3):
                value = coefficient*mp.mpf(0)**degree-(1+ratio)*(-mp.mpf(1))**degree
                value += weight*(-1-1/ratio)**degree
                check(checks, f"restart/equal-step ratio {ratio}: polynomial {degree}",
                      value-(1 if degree==1 else 0))
    for digits in (80, 100):
        checks.extend(read(ROOT / "pilot" / f"digits-{digits}.json")["checks"])
    decimals, audit_decimals, sampled_states = {}, {}, []
    diagnostic_maxima = {}
    total_updates, probe_solves = 0, 0
    largest_state_changes = []
    for model in MODELS:
        for kind in KINDS:
            for grid in GRIDS:
                target = directory(model, kind, grid)
                states, local_checks, final_hash = read_history(model, kind, grid)
                checks.extend(dict(row, name=f"{model}:{kind}:{grid}: "+row["name"]) for row in local_checks)
                old = previous.history(model, kind, grid)
                assert len(states) == len(old["expansion"])
                total_updates += len(states)-1
                reference_meta = read(target / "reference.json")
                checks.extend(dict(row, name=f"{model}:{kind}:{grid}: "+row["name"]) for row in reference_meta["checks"])
                reference_data = packet(target / "reference.npz")
                with mp.workdps(80):
                    old_gas = [mp.mpf(float(value)) for value in old["gas"]]
                    binary_gas = [mp.mpf(float(value)) for value in reference_data["gas"]]
                    precise_gas = [mp.mpf(state["gas"]) for state in states]
                    largest_state_changes.append(dict(model=model, kind=kind, grid=grid,
                        precision_minus_old=max(float(abs(first-second)) for first,second in zip(precise_gas,old_gas)),
                        precision_minus_increment64=max(float(abs(first-second)) for first,second in zip(precise_gas,binary_gas))))
                for representation in REPRESENTATIONS:
                    if representation == "saved_old":
                        probes = [read(previous.destination(model, kind, grid, index)) for index in range(5)]
                    else:
                        result = read(target / f"probes-{representation}.json")
                        assert not result["failed_checks"]
                        checks.extend(dict(row, name=f"{model}:{kind}:{grid}:{representation}: "+row["name"]) for row in result["checks"])
                        probes = result["records"]
                        probe_solves += result["solves"]
                    for method in METHODS:
                        values = [record[method]["gas"] for record in probes]
                        key = (model, kind, representation, grid, method)
                        decimals[key] = curve_decimal(values)
                        sampled_states.append(dict(model=model,kind=kind,representation=representation,grid=grid,method=method,
                                                   gas_values=values,curvatures=decimals[key]))
                    if representation != "saved_old" and grid == "quarter":
                        audit = curve_decimal([record["audit"]["gas"] for record in probes], 100)
                        audit_decimals[(model,kind,representation)] = audit
                        for quantity, actual, reference in zip(QUANTITIES, audit, decimals[(model,kind,representation,grid,"partial")]):
                            comparison_check(checks,f"{model}:{kind}:{representation}:{quantity}: probe precision",
                                             relative_change(actual,reference),"identity",1e-10)
    assert total_updates == 1464 and probe_solves == 224
    curves = np.empty((2,2,3,2,2,3))
    for model_index,kind_index,representation_index,grid_index,method_index in np.ndindex(2,2,3,2,2):
        key = (MODELS[model_index], KINDS[kind_index], REPRESENTATIONS[representation_index], GRIDS[grid_index], METHODS[method_index])
        curves[model_index,kind_index,representation_index,grid_index,method_index] = [float(value) for value in decimals[key]]
    inherited = packet(PARENT / "results/comparison.npz")
    for model_index, kind_index, grid_index, method_index in np.ndindex(2,2,2,2):
        assert np.array_equal(curves[model_index,kind_index,0,grid_index,method_index],
                              inherited["curves"][model_index,kind_index,method_index+1,grid_index+1])
    check(checks,"saved Stage188 equation curvatures reproduced bitwise",0)
    steps, splits, decompositions = [], [], []
    for model in MODELS:
        for kind in KINDS:
            for representation in REPRESENTATIONS:
                for method in METHODS:
                    half = decimals[(model,kind,representation,"half",method)]
                    quarter = decimals[(model,kind,representation,"quarter",method)]
                    for quantity, first, second in zip(QUANTITIES,half,quarter):
                        error = relative_change(first,second)
                        comparison_check(checks,f"{model}:{kind}:{representation}:{method}:{quantity}: half/quarter",
                                         error,"step_comparison")
                        with mp.workdps(100):
                            absolute = str(abs(mp.mpf(first)-mp.mpf(second)))
                        steps.append(dict(model=model,kind=kind,representation=representation,method=method,quantity=quantity,
                                          half=first,quarter=second,relative_change=error,absolute_change=absolute,
                                          passed=bool(error is not None and error<=.01)))
                for grid in GRIDS:
                    single = decimals[(model,kind,representation,grid,"partial")]
                    split = decimals[(model,kind,representation,grid,"split")]
                    for quantity,first,second in zip(QUANTITIES,single,split):
                        error = relative_change(first,second)
                        comparison_check(checks,f"{model}:{kind}:{representation}:{grid}:{quantity}: single/split",
                                         error,"split_comparison")
                        splits.append(dict(model=model,kind=kind,representation=representation,grid=grid,quantity=quantity,
                                           relative_change=error,passed=bool(error is not None and error<=.01)))
            for grid in GRIDS:
                for method in METHODS:
                    old = decimals[(model,kind,"saved_old",grid,method)]
                    binary = decimals[(model,kind,"increment64",grid,method)]
                    precise = decimals[(model,kind,"precision80",grid,method)]
                    with mp.workdps(100):
                        for quantity, first, second, third in zip(QUANTITIES,old,binary,precise):
                            old_value,binary_value,precise_value = mp.mpf(first),mp.mpf(second),mp.mpf(third)
                            precision_term=precise_value-binary_value
                            representation_term=binary_value-old_value
                            total=precise_value-old_value
                            check(checks,f"{model}:{kind}:{grid}:{method}:{quantity}: fixed-step decomposition",
                                  total-precision_term-representation_term)
                            decompositions.append(dict(model=model,kind=kind,grid=grid,method=method,quantity=quantity,
                                old=first,increment64=second,precision80=third,
                                precision_term=str(precision_term),representation_term=str(representation_term),total=str(total)))
    kernels,components = inherited["kernels"],list(inherited["components"])
    responses=np.empty((2,3,2,2,3,6,98,4))
    for kind_index,representation_index,grid_index,method_index,quantity_index,component,column in np.ndindex(2,3,2,2,3,6,4):
        scalar=curves[column//2,kind_index,representation_index,grid_index,method_index,quantity_index]
        responses[kind_index,representation_index,grid_index,method_index,quantity_index,component,:,column]=scalar*kernels[component,:,column]
    for kind_index,grid_index,method_index in np.ndindex(2,2,2):
        assert np.array_equal(responses[kind_index,0,grid_index,method_index],
                              inherited["responses"][kind_index,method_index+1,grid_index+1])
    check(checks,"saved Stage188 source arrays reproduced bitwise",0)
    factor=linear.cholesky(packet(previous.source.ROOT / "results/preparation/basis.npz")["mass"],lower=True)

    def norm(vector):
        return float(np.linalg.norm(linear.solve_triangular(factor,vector[1:97],lower=True)))

    source_rows=[]
    for kind_index,representation_index,method_index,quantity_index,component,column in np.ndindex(2,3,2,3,3,4):
        component_index=[0,4,5][component]
        half=responses[kind_index,representation_index,0,method_index,quantity_index,component_index,:,column]
        quarter=responses[kind_index,representation_index,1,method_index,quantity_index,component_index,:,column]
        denominator=norm(quarter)
        error=norm(half-quarter)/denominator if denominator else None
        name=f"{KINDS[kind_index]}:{REPRESENTATIONS[representation_index]}:{METHODS[method_index]}:{QUANTITIES[quantity_index]}:{components[component_index]}:{column}"
        comparison_check(checks,name+": source half/quarter",error,"source_step_comparison")
        source_rows.append(dict(kind=KINDS[kind_index],representation=REPRESENTATIONS[representation_index],
                                method=METHODS[method_index],quantity=QUANTITIES[quantity_index],
                                component=str(components[component_index]),column=column,relative_change=error,
                                passed=bool(error is not None and error<=.01),quarter_norm=denominator))
    for kind_index,representation_index,grid_index,method_index,quantity_index,column in np.ndindex(2,3,2,2,3,4):
        vectors=responses[kind_index,representation_index,grid_index,method_index,quantity_index,:,:,column]
        label=f"{kind_index}:{representation_index}:{grid_index}:{method_index}:{quantity_index}:{column}"
        for component,vector in enumerate(vectors):
            check(checks,label+f":{component}: source energy",(vector[0]+vector[-1])/max(abs(vector[0]),abs(vector[-1]),1e-300))
        check(checks,label+": matched closure",norm(vectors[4]-vectors[1]-vectors[2]-vectors[3])/max(norm(vectors[4]),1e-300))
        check(checks,label+": total closure",norm(vectors[5]-vectors[0]-vectors[4])/max(norm(vectors[5]),1e-300))
    for path,checksum in config["bookmark_hashes"].items():
        assert saved.digest(path)==checksum
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"),str(path),"exec")
    assert not list(ROOT.rglob("__pycache__"))
    check(checks,"scripts compile without bytecode",0)
    check(checks,"all consumed/immediate inputs unchanged",0)
    started=datetime.fromisoformat(config["started_utc"]).timestamp()
    protected=BRANCH.parent.parent/"formalization-workbench"
    changed=[str(path) for path in protected.rglob("*") if path.is_file() and path.stat().st_mtime>=started]
    check(checks,"protected workbench recent changes",len(changed),0,"integrity")
    directory_results=ROOT/"results"
    directory_results.mkdir(exist_ok=True)
    np.savez_compressed(directory_results/"comparison.npz",curves=curves,responses=responses,kernels=kernels,
        components=np.array(components),models=np.array(MODELS),kinds=np.array(KINDS),grids=np.array(GRIDS),
        representations=np.array(REPRESENTATIONS),methods=np.array(METHODS),quantities=np.array(QUANTITIES))
    write(directory_results/"decimal-probes.json",sampled_states)
    write(directory_results/"saved-baseline-controls.json",read(PARENT/"results/saved-baseline-controls.json"))
    failed=[row for row in checks if not row["passed"]]
    integrity_failed=[row for row in failed if row["category"] in ("identity","integrity")]
    write(directory_results/"assessment.json",dict(step_comparisons=steps,split_comparisons=splits,
        decompositions=decompositions,source_rows=source_rows,largest_state_changes=largest_state_changes,
        primary_updates=total_updates,probe_solves=probe_solves,new_physical_integrals=0))
    write(directory_results/"status.json",dict(stage=189,state="validated",count=len(checks),passed_checks=len(checks)-len(failed),
        checks=checks,failed_checks=failed,identity_failures=integrity_failed,all_checks_passed=not failed,
        authenticated_inputs=paths,protocol_hashes=config["protocol_hashes"],candidate_sha256=config["candidate_sha256"],
        primary_history_updates=1464,pilot_additional_100digit_updates=8,probe_solves=probe_solves,
        binary64_reference_updates=1464,reused_gas_events=36,protected_workbench_recent_modified_file_count=len(changed),
        original_bank_changed=False,candidate_changed=False,original_histories_changed=False,tolerances_changed=False,
        source_curve_changed=False,full_source_gate_retested=False,new_observational_test=False,
        completed_at_utc=datetime.now(timezone.utc).isoformat()))
    write(ROOT/"progress.json",dict(state="validated"))
    print(json.dumps(dict(checks=len(checks),passed=len(checks)-len(failed),failures=len(failed),
        identity_failures=integrity_failed,precision_width=[row for row in steps if row["representation"]=="precision80"
        and row["quantity"]=="width_discrepancy"],precision_split=[row for row in splits if row["representation"]=="precision80"
        and row["grid"]=="quarter" and row["quantity"]=="width_discrepancy"])),flush=True)


if __name__=="__main__":
    assess()
