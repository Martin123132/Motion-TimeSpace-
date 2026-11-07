from source_stage194 import *
from assess_stage191 import verify_events,join_banks,comparison_rows,history_rows,identities
from assess_stage192 import original_bank


def assess():
    assert read(ROOT/"progress.json")["state"]=="events_complete"
    assert not (ROOT/"results/status.json").exists()
    config=protocol()
    checks=list(read(ROOT/"results/preparation.json")["checks"])+list(read(ROOT/"pilot/original.json")["checks"])
    consumed=read(ROOT/"authenticated-inputs.json")
    for path,value in consumed.items():
        assert saved.digest(path)==value,path
    lower_outer=verify_events(ROOT,config,checks,True)
    lower_config,central_config,neighbour_config,outer_config=[read(path/"configuration.json") for path in REFERENCE_ROOTS]
    lower_adjacent=verify_events(PARENT,lower_config,checks)
    central=verify_events(CENTRAL,central_config,checks)
    neighbour=verify_events(NEIGHBOUR,neighbour_config,checks)
    outer=verify_events(OUTER,outer_config,checks)
    four=join_banks(lower_adjacent,join_banks(central,join_banks(neighbour,outer)))
    banks={"lower-outer":lower_outer,"four-node":four,"five-node":join_banks(lower_outer,four)}
    assert all(len(banks["five-node"][tag])==180 for tag in TAGS)
    old_lower_outer=original_bank(BANK,config)
    old_lower_adjacent=original_bank(previous.BANK,lower_config)
    old_central=original_bank(completed.BANK,central_config,completed.original_path)
    old_neighbour=original_bank(completed.previous.BANK,neighbour_config)
    old_outer=original_bank(prior.BANK,outer_config)
    old_four=join_banks(old_lower_adjacent,join_banks(old_central,join_banks(old_neighbour,old_outer)))
    old={"lower-outer":packet(ROOT/"results/original-curvature.npz")["vectors"],
         "four-node":packet(PARENT/"results/four-node-curvature.npz")["old_vectors"],
         "five-node":curvature(join_banks(old_lower_outer,old_four),80)}
    vectors={}
    for label,bank in banks.items():
        print("Assembling "+label,flush=True)
        primary=curvature(bank,80)
        audit=curvature(bank,100)
        identities(label,primary,audit,checks)
        vectors[label]=primary
        atomic_npz(ROOT/f"results/{label}-curvature.npz",vectors=primary,old_vectors=old[label],
            groups=np.array(["-".join(group) for group in GROUPS]),components=np.array(source.COMPONENTS))
    assert np.array_equal(vectors["four-node"],packet(PARENT/"results/four-node-curvature.npz")["vectors"])
    check(checks,"Stage193 weighted four-node sum reconstructed bitwise",0)
    for label,folder in (("lower-adjacent",PARENT),("central",CENTRAL),("neighbour",NEIGHBOUR),
                         ("outer",NEIGHBOUR),("two-node",NEIGHBOUR),("three-node",CENTRAL)):
        data=packet(folder/f"results/{label}-curvature.npz")
        vectors[label]=data["vectors"]
        old[label]=data["old_vectors"]
    norm=norm_setup()
    combinations=(("two-node",["neighbour","outer"]),("three-node",["central","two-node"]),
                  ("four-node",["lower-adjacent","three-node"]),("five-node",["lower-outer","four-node"]))
    for representation,collection in (("repaired",vectors),("old",old)):
        for total,members in combinations:
            summed=sum(collection[member] for member in members)
            errors=norm(collection[total]-summed)/np.maximum(norm(collection[total]),1e-300)
            for order,group,component,column in np.ndindex(errors.shape):
                check(checks,f"{representation}:{total}:weighted linearity:{order}:{group}:{component}:{column}",errors[order,group,component,column])
    rows,histories,summary=[],[],[]
    for label in ("lower-outer","lower-adjacent","central","neighbour","outer","two-node","three-node","four-node","five-node"):
        rows.extend(comparison_rows(label,vectors[label],old[label],checks))
        histories.extend(history_rows(label,vectors[label],checks))
        for group in ("saved-old",*["-".join(group) for group in GROUPS]):
            summary.append(dict(contribution=label,group=group,maximum_percent={component:100*max(row["relative"] for row in rows
                if row["contribution"]==label and row["group"]==group and row["component"]==component)
                for component in source.COMPONENTS}))
    overlay_count=0
    for tag in TAGS:
        for node in central_config["selected"]:
            metadata=read(event_path(CENTRAL,tag,node).with_suffix(".json"))
            if metadata["state_overlay_applied"]:
                assert saved.digest(metadata["raw_metadata_path"])==metadata["raw_metadata_sha256"]
                overlay_count+=1
    check(checks,"all20 reused central state overlays preserved",overlay_count-20,0,"integrity")
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
    write(ROOT/"results/status.json",dict(stage=194,state="validated",checks=checks,count=len(checks),
        passed_checks=len(checks)-len(failed),failed_checks=failed,identity_failures=fatal,all_checks_passed=not failed,
        authenticated_inputs=consumed,source_scope=config["source_scope"],infrared_tail_changed=False,
        original_bank_changed=False,original_histories_changed=False,candidate_coefficients_changed=False,
        tolerances_changed=False,source_curve_changed=False,new_observational_test=False,
        original_event_replays=2,repaired_event_evaluations=180,repaired_history_groups=4,
        reused_parent_events=720,new_virtual_integrations=0,reused_virtual_scalars=180,
        inherited_state_overlay_events=overlay_count,real_history_actions_reevaluated=True,full_population_integral=False,
        protected_workbench_recent_modified_file_count=len(changed),completed_at_utc=datetime.now(timezone.utc).isoformat()))
    write(ROOT/"progress.json",dict(state="validated"))
    print(json.dumps(dict(checks=len(checks),failed=len(failed),identity_failures=fatal,
        summary=[row for row in summary if row["contribution"] in ("lower-outer","five-node")],
        history_failures=[row for row in histories if not row["passed"]])),flush=True)


if __name__=="__main__":
    assess()
