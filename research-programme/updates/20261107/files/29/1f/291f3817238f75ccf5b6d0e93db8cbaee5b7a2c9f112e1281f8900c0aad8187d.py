from source_stage191 import *


def verify_events(root,config,checks,retain_checks=False):
    bank={}
    for tag in TAGS:
        pairs=[]
        for node in config["selected"]:
            path=event_path(root,tag,node)
            data=packet(path)
            metadata=read(path.with_suffix(".json"))
            assert saved.digest(path)==metadata["sha256"] and not metadata["failed_checks"]
            assert saved.digest(metadata["loop_path"])==metadata["loop_sha256"]
            assert saved.digest(metadata["original_event"])==metadata["original_event_sha256"]
            exact=json.loads(str(data["node"]))
            parameters,weight=source.physics.parameters_and_weight(float(data["theta"]),exact)
            assert weight==float(data["weight"])
            assert exact["frequency"]==config["incoming_frequency"]
            assert data["high"].shape==data["low"].shape==(4,6,98,4)
            assert list(data["groups"])==["-".join(group) for group in GROUPS]
            assert np.isfinite(data["high"]).all() and np.isfinite(data["low"]).all()
            loop=read(metadata["loop_path"])
            assert loop["finite"] and loop["identity"]==source.physics.event_owner.inherited.virtual_identity(parameters)
            pairs.append((data["high"],data["low"]))
            if retain_checks:
                checks.extend(dict(row,name=tag+":"+event_common.event_key(node)+":"+row["name"]) for row in metadata["checks"])
        bank[tag]=pairs
    return bank


def join_banks(first,second):
    assert set(first)==set(second)==set(TAGS)
    return {tag:first[tag]+second[tag] for tag in TAGS}


def comparison_rows(label,vectors,old,checks):
    norm=norm_setup()
    rows=[]
    for representation,array in (("original",old[:,:1]),("repaired",vectors)):
        denominator=norm(array[1])
        numerator=norm(array[2])
        for group,component,column in np.ndindex(denominator.shape):
            relative=float(numerator[group,component,column]/denominator[group,component,column]) if denominator[group,component,column] else None
            group_name="saved-old" if representation=="original" else "-".join(GROUPS[group])
            passed=bool(relative is not None and relative<.01)
            checks.append(dict(name=f"{label}:{group_name}:{source.COMPONENTS[component]}:{column}: temperature-width curvature",
                value=relative,tolerance=.01,passed=passed,category="source_comparison"))
            rows.append(dict(contribution=label,group=group_name,component=source.COMPONENTS[component],column=column,
                relative=relative,passed=passed,fine_norm=float(denominator[group,component,column]),
                discrepancy_norm=float(numerator[group,component,column])))
    return rows


def history_rows(label,vectors,checks):
    norm=norm_setup()
    rows=[]
    for kind,half,quarter in (("bank",0,1),("candidate",2,3)):
        for order in range(3):
            denominator=norm(vectors[order,quarter])
            difference=norm(vectors[order,half]-vectors[order,quarter])
            for component in (0,4,5):
                for column in range(4):
                    relative=float(difference[component,column]/denominator[component,column]) if denominator[component,column] else None
                    passed=bool(relative is not None and relative<.01)
                    checks.append(dict(name=f"{label}:{kind}:{order}:{source.COMPONENTS[component]}:{column}: history half/quarter",
                        value=relative,tolerance=.01,passed=passed,category="history_comparison"))
                    rows.append(dict(contribution=label,kind=kind,quantity=["coarse_curvature","fine_curvature","width_discrepancy"][order],
                        component=source.COMPONENTS[component],column=column,relative=relative,passed=passed,
                        absolute_source_norm=float(difference[component,column])))
    return rows


def identities(label,primary,audit,checks):
    norm=norm_setup()
    for order in range(3):
        errors=norm(primary[order]-audit[order])/np.maximum(norm(primary[order]),1e-300)
        for group,component,column in np.ndindex(errors.shape):
            check(checks,f"{label}:curvature precision:{order}:{group}:{component}:{column}",errors[group,component,column])
    for order,group in np.ndindex(3,primary.shape[1]):
        array=primary[order,group]
        for component,column in np.ndindex(6,4):
            vector=array[component,:,column]
            check(checks,f"{label}:{order}:{group}:{component}:{column}: source energy",
                (vector[0]+vector[-1])/max(abs(vector[0]),abs(vector[-1]),1e-300))
        for component,members in ((4,[1,2,3]),(5,[0,1,2,3])):
            errors=norm(array[component]-sum(array[index] for index in members))/np.maximum(norm(array[component]),1e-300)
            for column in range(4):
                check(checks,f"{label}:{order}:{group}:{component}:{column}: component closure",errors[column])


def assess():
    assert read(ROOT/"progress.json")["state"]=="events_complete"
    assert not (ROOT/"results/status.json").exists()
    config=protocol()
    checks=list(read(ROOT/"results/preparation.json")["checks"])+list(read(ROOT/"pilot/original.json")["checks"])
    consumed=read(ROOT/"authenticated-inputs.json")
    for path,value in consumed.items():
        assert saved.digest(path)==value,path
    neighbour=verify_events(ROOT,config,checks,True)
    parent_config=read(PARENT/"configuration.json")
    outer=verify_events(PARENT,parent_config,checks)
    banks={"neighbour":neighbour,"outer":outer,"two-node":join_banks(neighbour,outer)}
    vectors,old={},{}
    old_banks={}
    for label,folder,node_config in (("neighbour",BANK,config),("outer",prior.BANK,parent_config)):
        old_banks[label]={tag:[] for tag in TAGS}
        for tag in TAGS:
            for node in node_config["selected"]:
                data=packet(event_path(folder,tag,node))
                old_banks[label][tag].append((data["high"],data["low"]))
    old["neighbour"]=packet(ROOT/"results/original-curvature.npz")["vectors"]
    old["outer"]=packet(PARENT/"results/original-curvature.npz")["vectors"]
    old["two-node"]=curvature(join_banks(old_banks["neighbour"],old_banks["outer"]),80)
    rows,histories=[],[]
    for label,bank in banks.items():
        print("Assembling "+label,flush=True)
        primary=curvature(bank,80)
        audit=curvature(bank,100)
        identities(label,primary,audit,checks)
        vectors[label]=primary
        rows.extend(comparison_rows(label,primary,old[label],checks))
        histories.extend(history_rows(label,primary,checks))
        atomic_npz(ROOT/f"results/{label}-curvature.npz",vectors=primary,old_vectors=old[label],
            groups=np.array(["-".join(group) for group in GROUPS]),components=np.array(source.COMPONENTS))
    assert np.array_equal(vectors["outer"],packet(PARENT/"results/comparison.npz")["curvatures"])
    check(checks,"Stage190 reconstructed bitwise without source reevaluation",0)
    norm=norm_setup()
    for representation,collection in (("repaired",vectors),("old",old)):
        summed=collection["neighbour"]+collection["outer"]
        errors=norm(collection["two-node"]-summed)/np.maximum(norm(collection["two-node"]),1e-300)
        for order,group,component,column in np.ndindex(errors.shape):
            check(checks,f"{representation}:weighted two-node linearity:{order}:{group}:{component}:{column}",errors[order,group,component,column])
    summary=[]
    for label in banks:
        for group in ("saved-old",*["-".join(group) for group in GROUPS]):
            summary.append(dict(contribution=label,group=group,maximum_percent={component:100*max(row["relative"] for row in rows
                if row["contribution"]==label and row["group"]==group and row["component"]==component)
                for component in source.COMPONENTS}))
    write(ROOT/"results/comparison.json",dict(source_rows=rows,history_rows=histories,summary=summary,
        scope=config["source_scope"],infrared_tail_changed=False,packets_already_frequency_weighted=True,
        full_population_integral=False,frequency_weights_reapplied=False))
    for path,value in consumed.items():
        assert saved.digest(path)==value,path
    for path,value in config["bookmark_hashes"].items():
        assert saved.digest(path)==value
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"),str(path),"exec")
    assert not list(ROOT.rglob("__pycache__")) and not list(ROOT.rglob("*.partial"))
    check(checks,"scripts compile without bytecode",0)
    check(checks,"all consumed inputs unchanged",0)
    started=datetime.fromisoformat(config["started_utc"]).timestamp()
    protected=BRANCH.parent.parent/"formalization-workbench"
    changed=[str(path) for path in protected.rglob("*") if path.is_file() and path.stat().st_mtime>=started]
    check(checks,"protected workbench recent changes",len(changed),0,"integrity")
    failed=[row for row in checks if not row["passed"]]
    fatal=[row for row in failed if row["category"] in ("identity","integrity")]
    write(ROOT/"results/status.json",dict(stage=191,state="validated",checks=checks,count=len(checks),
        passed_checks=len(checks)-len(failed),failed_checks=failed,identity_failures=fatal,all_checks_passed=not failed,
        authenticated_inputs=consumed,source_scope=config["source_scope"],infrared_tail_changed=False,
        original_bank_changed=False,original_histories_changed=False,candidate_coefficients_changed=False,
        tolerances_changed=False,source_curve_changed=False,new_observational_test=False,
        original_event_replays=1,repaired_event_evaluations=180,repaired_history_groups=4,
        reused_parent_events=180,new_virtual_integrations=0,reused_virtual_scalars=180,
        real_history_actions_reevaluated=True,full_population_integral=False,
        protected_workbench_recent_modified_file_count=len(changed),completed_at_utc=datetime.now(timezone.utc).isoformat()))
    write(ROOT/"progress.json",dict(state="validated"))
    print(json.dumps(dict(checks=len(checks),failed=len(failed),identity_failures=fatal,summary=summary,
        history_failures=[row for row in histories if not row["passed"]])),flush=True)


if __name__=="__main__":
    assess()
