from source_stage190 import *


def assess():
    assert read(ROOT/"progress.json")["state"]=="events_complete"
    assert not (ROOT/"results/status.json").exists()
    config=protocol()
    checks=list(read(ROOT/"results/preparation.json")["checks"])+list(read(ROOT/"pilot/original.json")["checks"])
    consumed=read(ROOT/"authenticated-inputs.json")
    for path,value in consumed.items():
        assert saved.digest(path)==value,path
    bank={}
    for tag in TAGS:
        pairs=[]
        for node in config["selected"]:
            path=new_path(tag,node)
            metadata=read(path.with_suffix(".json"))
            assert saved.digest(path)==metadata["sha256"] and not metadata["failed_checks"]
            assert saved.digest(metadata["loop_path"])==metadata["loop_sha256"]
            assert saved.digest(metadata["original_event"])==metadata["original_event_sha256"]
            data=packet(path)
            assert data["high"].shape==(4,6,98,4)
            pairs.append((data["high"],data["low"]))
            checks.extend(dict(row,name=tag+":"+event_common.event_key(node)+":"+row["name"]) for row in metadata["checks"])
        bank[tag]=pairs
    primary=curvature(bank,80)
    audit=curvature(bank,100)
    old=packet(ROOT/"results/original-curvature.npz")["vectors"]
    norm=norm_setup()
    for order in range(3):
        error=norm(primary[order]-audit[order])/np.maximum(norm(primary[order]),1e-300)
        for group,component,column in np.ndindex(error.shape):
            check(checks,f"curvature precision:{order}:{group}:{component}:{column}",error[group,component,column])
    for order,group in np.ndindex(3,4):
        array=primary[order,group]
        for component in range(6):
            for column in range(4):
                vector=array[component,:,column]
                check(checks,f"{order}:{group}:{component}:{column}: source energy",
                      (vector[0]+vector[-1])/max(abs(vector[0]),abs(vector[-1]),1e-300))
        for component,members in ((4,[1,2,3]),(5,[0,1,2,3])):
            error=norm(array[component]-sum(array[index] for index in members))/np.maximum(norm(array[component]),1e-300)
            for column in range(4):
                check(checks,f"{order}:{group}:{component}:{column}: source component closure",error[column])
    rows=[]
    for representation,vectors in (("original",old[:,:1]),("repaired",primary)):
        denominator=norm(vectors[1])
        numerator=norm(vectors[2])
        for group,component,column in np.ndindex(denominator.shape):
            relative=float(numerator[group,component,column]/denominator[group,component,column]) if denominator[group,component,column] else None
            label="saved-old" if representation=="original" else "-".join(GROUPS[group])
            passed=bool(relative is not None and relative<.01)
            checks.append(dict(name=f"{label}:{source.COMPONENTS[component]}:{column}: temperature-width curvature",
                value=relative,tolerance=.01,passed=passed,category="source_comparison"))
            rows.append(dict(group=label,component=source.COMPONENTS[component],column=column,
                             relative=relative,passed=passed,fine_norm=float(denominator[group,component,column]),
                             discrepancy_norm=float(numerator[group,component,column])))
    history_rows=[]
    for kind,half,quarter in (("bank",0,1),("candidate",2,3)):
        for order in range(3):
            denominator=norm(primary[order,quarter])
            difference=norm(primary[order,half]-primary[order,quarter])
            for component in (0,4,5):
                for column in range(4):
                    relative=float(difference[component,column]/denominator[component,column]) if denominator[component,column] else None
                    passed=bool(relative is not None and relative<.01)
                    checks.append(dict(name=f"{kind}:{order}:{source.COMPONENTS[component]}:{column}: history half/quarter",
                                       value=relative,tolerance=.01,passed=passed,category="history_comparison"))
                    history_rows.append(dict(kind=kind,quantity=["coarse_curvature","fine_curvature","width_discrepancy"][order],
                        component=source.COMPONENTS[component],column=column,relative=relative,passed=passed,
                        absolute_source_norm=float(difference[component,column])))
    impacts=[]
    for group in range(4):
        numerator=norm(primary[2,group]-old[2,0])
        denominator=norm(old[2,0])
        for component in (0,4,5):
            for column in range(4):
                impacts.append(dict(group="-".join(GROUPS[group]),component=source.COMPONENTS[component],column=column,
                    change_over_old_discrepancy=float(numerator[component,column]/denominator[component,column])))
    atomic_npz(ROOT/"results/comparison.npz",curvatures=primary,old_curvatures=old,
               groups=np.array(["-".join(group) for group in GROUPS]),components=np.array(source.COMPONENTS))
    write(ROOT/"results/comparison.json",dict(source_rows=rows,history_rows=history_rows,changes_from_old=impacts,
          infrared_tail_changed=False,scope=config["source_scope"]))
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
    write(ROOT/"results/status.json",dict(stage=190,state="validated",checks=checks,count=len(checks),
        passed_checks=len(checks)-len(failed),failed_checks=failed,identity_failures=fatal,all_checks_passed=not failed,
        authenticated_inputs=consumed,source_scope=config["source_scope"],infrared_tail_changed=False,
        original_bank_changed=False,original_histories_changed=False,candidate_coefficients_changed=False,
        tolerances_changed=False,source_curve_changed=False,new_observational_test=False,
        original_event_replays=1,repaired_event_evaluations=180,repaired_history_groups=4,
        new_virtual_integrations=0,reused_virtual_scalars=180,real_history_actions_reevaluated=True,
        protected_workbench_recent_modified_file_count=len(changed),completed_at_utc=datetime.now(timezone.utc).isoformat()))
    write(ROOT/"progress.json",dict(state="validated"))
    summary=[]
    for group in ("saved-old",*["-".join(group) for group in GROUPS]):
        summary.append(dict(group=group,maximum_percent={component:100*max(row["relative"] for row in rows
            if row["group"]==group and row["component"]==component) for component in ("control","remainder","total")}))
    print(json.dumps(dict(count=len(checks),failed=len(failed),identity_failures=fatal,summary=summary,
        history_failed=[row for row in history_rows if not row["passed"]])),flush=True)


if __name__=="__main__":
    assess()
