from source_stage196 import *
from assess_stage191 import verify_events,join_banks,comparison_rows,history_rows,identities
from assess_stage192 import original_bank
from decimal import Decimal, localcontext


def independent_samples(label,bank,vectors,checks):
    with localcontext() as context:
        context.prec=100
        for group in (1,3):
            for component,row,column in ((0,1,0),(2,48,2),(3,96,0)):
                summed={}
                for tag in TAGS:
                    summed[tag]=sum((Decimal.from_float(float(pair[0][group,component,row,column]))+
                        Decimal.from_float(float(pair[1][group,component,row,column])) for pair in bank[tag]),Decimal(0))
                coarse=(summed["plus"]-2*summed["anchor"]+summed["minus"])/Decimal(".01")**2
                fine=(summed["plus_half"]-2*summed["anchor"]+summed["minus_half"])/Decimal(".005")**2
                for order,expected in enumerate((coarse,fine,coarse-fine)):
                    reference=float(expected)
                    actual=float(vectors[order,group,component,row,column])
                    check(checks,f"{label}:independent Decimal sample:{order}:{group}:{component}:{row}:{column}",
                        abs(actual-reference)/max(abs(reference),1e-300))


def assess():
    assert read(ROOT/"progress.json")["state"]=="events_complete"
    assert not (ROOT/"results/status.json").exists()
    config=protocol()
    checks=list(read(ROOT/"results/preparation.json")["checks"])+list(read(ROOT/"pilot/original.json")["checks"])
    consumed=read(ROOT/"authenticated-inputs.json")
    for path,value in consumed.items():
        assert saved.digest(path)==value,path
    upper_edge=verify_events(ROOT,config,checks,True)
    edge_config,lower_outer_config,lower_config,central_config,neighbour_config,outer_config=[read(path/"configuration.json") for path in REFERENCE_ROOTS]
    lower_edge=verify_events(PARENT,edge_config,checks)
    lower_outer=verify_events(LOWER_OUTER,lower_outer_config,checks)
    lower_adjacent=verify_events(LOWER,lower_config,checks)
    central=verify_events(CENTRAL,central_config,checks)
    neighbour=verify_events(NEIGHBOUR,neighbour_config,checks)
    outer=verify_events(OUTER,outer_config,checks)
    four=join_banks(lower_adjacent,join_banks(central,join_banks(neighbour,outer)))
    five=join_banks(lower_outer,four)
    six=join_banks(lower_edge,five)
    banks={"upper-edge":upper_edge,"six-node":six,"seven-node":join_banks(upper_edge,six)}
    assert all(len(banks["seven-node"][tag])==252 for tag in TAGS)
    frequencies=[config["incoming_frequency"],*config["reference_frequencies"]]
    assert sorted(frequencies)==config["panel_frequencies"] and len(set(frequencies))==7
    configurations=[config,edge_config,lower_outer_config,lower_config,central_config,neighbour_config,outer_config]
    weights=[entry["selected"][0]["seed_weight"] for entry in configurations]
    assert all(len(entry["selected"])==36 and all(node["seed_weight"]==weight for node in entry["selected"])
        for entry,weight in zip(configurations,weights))
    check(checks,"full seven-frequency panel has252 events at every temperature",0,0,"integrity")
    check(checks,"incoming seven-node weights integrate unit function over8-20",abs(sum(weights)-12),1e-13)
    weighted_nodes=sorted((dict(frequency=entry["incoming_frequency"],seed_weight=weight)
        for entry,weight in zip(configurations,weights)),key=lambda item:item["frequency"])
    write(ROOT/"results/panel-coverage.json",dict(frequencies=sorted(frequencies),expected_frequencies=config["panel_frequencies"],
        nodes_per_temperature=252,temperatures=5,incoming_seed_weights=[item["seed_weight"] for item in weighted_nodes],
        incoming_nodes=weighted_nodes,weight_sum=sum(weights),
        full_finite_panel_coverage=True,full_population_integral=False,weights_reapplied=False))
    old_upper_edge=original_bank(BANK,config)
    for tag in TAGS:
        for node in config["selected"]:
            metadata=validate_packet(event_path(BANK,tag,node))
            checks.extend(dict(row,name=tag+":"+event_common.event_key(node)+":original:"+row["name"]) for row in metadata["checks"])
    old_lower_edge=original_bank(previous.BANK,edge_config)
    old_lower_outer=original_bank(previous.previous.BANK,lower_outer_config)
    old_lower_adjacent=original_bank(previous.previous.previous.BANK,lower_config)
    old_central=original_bank(completed.BANK,central_config,completed.original_path)
    old_neighbour=original_bank(completed.previous.BANK,neighbour_config)
    old_outer=original_bank(prior.BANK,outer_config)
    old_four=join_banks(old_lower_adjacent,join_banks(old_central,join_banks(old_neighbour,old_outer)))
    old_five=join_banks(old_lower_outer,old_four)
    old_six=join_banks(old_lower_edge,old_five)
    old_edge=curvature(old_upper_edge,80)
    identities("newly calculated original upper edge",old_edge,curvature(old_upper_edge,100),checks)
    old={"upper-edge":old_edge,"six-node":curvature(old_six,80),
         "seven-node":curvature(join_banks(old_upper_edge,old_six),80)}
    assert np.array_equal(old["six-node"],packet(PARENT/"results/six-node-curvature.npz")["old_vectors"])
    check(checks,"Stage195 original six-node sum reconstructed bitwise",0)
    vectors={}
    for label,bank in banks.items():
        print("Assembling "+label,flush=True)
        primary=curvature(bank,80)
        audit=curvature(bank,100)
        identities(label,primary,audit,checks)
        independent_samples(label,bank,primary,checks)
        vectors[label]=primary
        atomic_npz(ROOT/f"results/{label}-curvature.npz",vectors=primary,old_vectors=old[label],
            groups=np.array(["-".join(group) for group in GROUPS]),components=np.array(source.COMPONENTS))
    assert np.array_equal(vectors["six-node"],packet(PARENT/"results/six-node-curvature.npz")["vectors"])
    check(checks,"Stage195 weighted six-node sum reconstructed bitwise",0)
    for label,folder in (("lower-edge",PARENT),("lower-outer",LOWER_OUTER),("lower-adjacent",LOWER),("central",CENTRAL),("neighbour",NEIGHBOUR),
                         ("outer",NEIGHBOUR),("two-node",NEIGHBOUR),("three-node",CENTRAL),("four-node",LOWER),("five-node",LOWER_OUTER)):
        data=packet(folder/f"results/{label}-curvature.npz")
        vectors[label]=data["vectors"]
        old[label]=data["old_vectors"]
    norm=norm_setup()
    combinations=(("two-node",["neighbour","outer"]),("three-node",["central","two-node"]),
                  ("four-node",["lower-adjacent","three-node"]),("five-node",["lower-outer","four-node"]),("six-node",["lower-edge","five-node"]),("seven-node",["upper-edge","six-node"]))
    for representation,collection in (("repaired",vectors),("old",old)):
        for total,members in combinations:
            summed=sum(collection[member] for member in members)
            errors=norm(collection[total]-summed)/np.maximum(norm(collection[total]),1e-300)
            for order,group,component,column in np.ndindex(errors.shape):
                check(checks,f"{representation}:{total}:weighted linearity:{order}:{group}:{component}:{column}",errors[order,group,component,column])
    rows,histories,summary=[],[],[]
    for label in ("upper-edge","lower-edge","lower-outer","lower-adjacent","central","neighbour","outer","two-node","three-node","four-node","five-node","six-node","seven-node"):
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
        full_finite_panel_coverage=True,full_population_integral=False,frequency_weights_reapplied=False,
        new_edge_original_control="newly evaluated with original histories; saved-old is a comparison label, not a historical prediction"))
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
    loop_paths=list((ROOT/"virtual-cache").rglob("*.json"))
    assert len(loop_paths)==144
    assert len(list((BANK/"events").rglob("electron-*.npz")))==180
    candidate_rows=[row for row in rows if row["group"].startswith("candidate-")]
    write(ROOT/"results/status.json",dict(stage=196,state="validated",checks=checks,count=len(checks),
        passed_checks=len(checks)-len(failed),failed_checks=failed,identity_failures=fatal,all_checks_passed=not failed,
        all_candidate_checks_passed=all(row["passed"] for row in candidate_rows),
        all_history_checks_passed=all(row["passed"] for row in histories),
        new_original_control_evaluations=180,
        authenticated_inputs=consumed,source_scope=config["source_scope"],infrared_tail_changed=False,
        original_bank_changed=False,original_histories_changed=False,candidate_coefficients_changed=False,
        tolerances_changed=False,source_curve_changed=False,new_observational_test=False,
        original_event_replays=2,repaired_event_evaluations=180,repaired_history_groups=4,
        reused_parent_events=1080,new_virtual_integrations=144,reused_virtual_scalars=36,
        inherited_state_overlay_events=overlay_count,real_history_actions_reevaluated=True,full_finite_panel_coverage=True,full_population_integral=False,
        protected_workbench_recent_modified_file_count=len(changed),completed_at_utc=datetime.now(timezone.utc).isoformat()))
    write(ROOT/"progress.json",dict(state="validated"))
    print(json.dumps(dict(checks=len(checks),failed=len(failed),identity_failures=fatal,
        summary=[row for row in summary if row["contribution"] in ("upper-edge","seven-node")],
        history_failures=[row for row in histories if not row["passed"]])),flush=True)


if __name__=="__main__":
    assess()




