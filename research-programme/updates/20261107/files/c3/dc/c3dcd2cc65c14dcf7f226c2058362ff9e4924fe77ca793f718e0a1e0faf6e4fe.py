from __future__ import annotations
import os
for variable in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[variable]="1"
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json, time, argparse, inspect
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/"lower-edge-repaired-source-combination-20261022"
LOWER_OUTER=BRANCH/"lower-outer-repaired-source-combination-20261021"
LOWER=BRANCH/"lower-adjacent-repaired-source-combination-20261021"
CENTRAL=BRANCH/"central-repaired-source-combination-20261021"
NEIGHBOUR=BRANCH/"neighbour-repaired-source-combination-20261021"
OUTER=BRANCH/"repaired-history-microscopic-source-20261021"
REFERENCE_ROOTS=[PARENT,LOWER_OUTER,LOWER,CENTRAL,NEIGHBOUR,OUTER]
PARENT_SHA="b2be3f330f5b641ff59989413752c6c4355e71901e3925326afcb9bfe9ebb384"
BANK=ROOT/"original-bank"
sys.path.insert(0,str(PARENT))
import source_stage195 as previous
completed=previous.completed
prior=previous.prior
np,mp,linear=prior.np,prior.mp,prior.linear
saved,read,write,check,packet=prior.saved,prior.read,prior.write,prior.check,prior.packet
source,event_common,crossed=prior.source,prior.event_common,prior.crossed
TAGS,GROUPS=prior.TAGS,prior.GROUPS
atomic_npz,curvature,norm_setup=prior.atomic_npz,prior.curvature,prior.norm_setup
repaired_bundle,weighted=prior.repaired_bundle,prior.weighted
FREQUENCY=19.694647474056552

def event_path(root,tag,node):
    return root/"events"/tag/event_common.angle_label(node["cosine"])/f"electron-{node['electron_index']:02d}.npz"

def protocol():
    config=read(ROOT/"configuration.json")
    for name,value in config["protocol_hashes"].items():
        assert saved.digest(ROOT/name)==value,name
    return config

def prepare():
    assert not (ROOT/"configuration.json").exists()
    seal_path=PARENT/"results/stage-integrity.json"
    assert saved.digest(seal_path)==PARENT_SHA
    parent=read(seal_path)
    paths=dict(parent["consumed_and_immediate_rehashed"])
    paths.update({str(PARENT/name):value for name,value in parent["file_hashes"].items()})
    paths[str(seal_path)]=PARENT_SHA
    for name,value in paths.items():
        assert saved.digest(name)==value,name
    inherited=read(PARENT/"configuration.json")
    config={key:inherited[key] for key in ("start_fraction","target_fraction","theta0","delta_log_temperature",
        "expansion_span","offsets","source_prediction_tolerance","identity_tolerance","panel_frequencies")}
    coverage=read(ROOT/"coverage.json")
    rows=[row for row in coverage["rows"] if row["frequency"]==FREQUENCY]
    assert len(rows)==180 and sum(bool(row["loop_matches"]) for row in rows)==36
    config.update(stage=196,incoming_frequency=FREQUENCY,selected=[row["node"] for row in rows if row["tag"]=="anchor"],
        parent_seal_sha256=PARENT_SHA,started_utc=datetime.now(timezone.utc).isoformat(),groups_repaired=GROUPS,
        source_scope="Complete original seven-node 8-20 incoming panel; repaired resolved photons/gas; fixed original infrared tail",
        reference_frequencies=[read(path/"configuration.json")["incoming_frequency"] for path in REFERENCE_ROOTS],
        original_bank_changed=False,infrared_tail_changed=False,
        protocol_hashes={name:saved.digest(ROOT/name) for name in ("ACCEPTANCE.md","DERIVATION.md","coverage.json")},
        bookmark_hashes={str(path):saved.digest(path) for path in (BRANCH/"RESUME-CURRENT.md",BRANCH.parent/"CURRENT_LOCAL_RESUME.md")})
    assert config["source_prediction_tolerance"]==.01 and config["identity_tolerance"]==1e-10
    checks=[]
    frequencies=[FREQUENCY,*config["reference_frequencies"]]
    assert sorted(frequencies)==config["panel_frequencies"] and len(set(frequencies))==7
    check(checks,"all seven original incoming panel frequencies exactly covered",0,0,"integrity")
    for tag in TAGS:
        bundle,theta=source.context(source.START-config["offsets"][tag]/config["expansion_span"])
        selected=event_common.nodes(theta,FREQUENCY)
        expected=[row for row in rows if row["tag"]==tag]
        assert len(selected)==36 and [row["node"] for row in expected]==selected
        for row in expected:
            for match in row["loop_matches"]:
                assert saved.digest(match["path"])==match["sha256"]
                paths.setdefault(match["path"],match["sha256"])
        for path in bundle.inputs:
            paths.setdefault(str(path),saved.digest(path))
        hard=[node for node in selected if node["electron_index"]==0]
        for power in range(6):
            expected_moment=2/(power+1) if power%2==0 else 0.
            check(checks,f"{tag}:hard-angle moment{power}",sum(node["hard_weight"]*node["cosine"]**power for node in hard)-expected_moment,1e-14)
    for module in list(sys.modules.values()):
        name=getattr(module,"__file__",None)
        if name and Path(name).suffix==".py":
            path=Path(name).resolve()
            if path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                paths.setdefault(str(path),saved.digest(path))
    write(ROOT/"configuration.json",config)
    write(BANK/"configuration.json",config)
    write(ROOT/"authenticated-inputs.json",paths)
    write(ROOT/"results/preparation.json",dict(checks=checks,failed_checks=[row for row in checks if not row["passed"]]))
    assert all(row["passed"] for row in checks)
    write(ROOT/"results/weighting.json",dict(parameters_and_weight_source=inspect.getsource(source.physics.parameters_and_weight),
        function_path=inspect.getsourcefile(source.physics.parameters_and_weight),
        frequencies=[FREQUENCY,*config["reference_frequencies"]],packets_already_weighted=True,
        combination_coefficients=[1]*7,full_finite_panel=True,full_population_integral=False))
    write(ROOT/"progress.json",dict(state="prepared",new_events=0))
    print(json.dumps(dict(state="prepared",inputs=len(paths),cached_loops=36,missing_loops=144)),flush=True)

def loop_for(row):
    if row["loop_matches"]:
        match=row["loop_matches"][0]
        path=Path(match["path"])
        assert saved.digest(path)==match["sha256"]
        data=read(path)
        reused=True
    else:
        path=ROOT/"virtual-cache"/row["key"][:2]/(row["key"]+".json")
        if path.exists():
            data=read(path)
        else:
            parameters,weight=source.physics.parameters_and_weight(row["theta"],row["node"])
            assert weight==row["weight"]
            began=time.monotonic()
            unused,response=source.physics.weak.source.virtual_map(parameters,2)
            data=dict(identity=row["identity"],scalar=float(response[0,0]),finite=bool(np.isfinite(response[0,0])),
                seconds=time.monotonic()-began)
            assert data["finite"]
            write(path,data)
        reused=False
    assert data["identity"]==row["identity"] and data["finite"] and np.isfinite(data["scalar"])
    return data["scalar"],path,reused

def cached_event(tag,node,theta):
    path=event_path(BANK,tag,node)
    data=packet(path)
    exact=json.loads(str(data["node"]))
    assert event_common.event_key(exact)==event_common.event_key(node)
    assert exact["frequency"]==FREQUENCY and float(data["theta"])==theta
    parameters,weight=source.physics.parameters_and_weight(theta,exact)
    assert weight==float(data["weight"])
    loop_path=Path(str(data["loop_path"]))
    loop=read(loop_path)
    assert loop["finite"] and loop["identity"]==source.physics.event_owner.inherited.virtual_identity(parameters)
    return data,parameters,weight,loop["scalar"],loop_path,exact

def validate_packet(path):
    metadata=read(path.with_suffix(".json"))
    assert saved.digest(path)==metadata["sha256"] and not metadata["failed_checks"]
    assert saved.digest(metadata["loop_path"])==metadata["loop_sha256"]
    return metadata

def evaluate(max_events,seconds):
    config=protocol()
    assert not read(ROOT/"results/preparation.json")["failed_checks"]
    rows=[row for row in read(ROOT/"coverage.json")["rows"] if row["frequency"]==FREQUENCY]
    anchor,unused=source.context(source.START)
    began=time.monotonic()
    count=0
    for tag in TAGS:
        original,theta=source.context(source.START-config["offsets"][tag]/config["expansion_span"])
        paired=source.PairedHistory(original,anchor)
        original_evaluators=source.models(paired)
        bundles,mappings=[],[]
        for kind,grid in GROUPS:
            bundle,mapping=repaired_bundle(original,tag,kind,grid)
            bundles.append(bundle)
            mappings.append(dict(kind=kind,grid=grid,mapping=mapping))
        grouped=crossed.HistoryGroup(bundles)
        evaluators=source.models(grouped)
        for row in [item for item in rows if item["tag"]==tag]:
            node=row["node"]
            destination=event_path(ROOT,tag,node)
            original_path=event_path(BANK,tag,node)
            if destination.exists():
                metadata=validate_packet(destination)
                validate_packet(original_path)
                assert saved.digest(original_path)==metadata["original_event_sha256"]
                continue
            if count>=max_events or time.monotonic()-began>=seconds:
                write(ROOT/"progress.json",dict(state="safe_restart",next_tag=tag,next_event=event_common.event_key(node),
                    saved_events=len(list((ROOT/"events").rglob("electron-*.npz"))),expected_events=180))
                print("Safe event boundary saved.",flush=True)
                return
            started=time.monotonic()
            scalar,loop_path,reused=loop_for(row)
            parameters,weight=source.physics.parameters_and_weight(theta,node)
            assert weight==row["weight"] and theta==row["theta"]
            if not original_path.exists():
                high,low,diagnostics=weighted(parameters,paired,original_evaluators,scalar,weight)
                assert high.shape==low.shape==(2,6,98,4)
                checks=[]
                for name,value in diagnostics.items():
                    check(checks,name,value)
                assert np.isfinite(high).all() and np.isfinite(low).all()
                atomic_npz(original_path,high=high,low=low,theta=theta,weight=weight,node=json.dumps(node,sort_keys=True),
                    loop_path=str(loop_path),loop_reused=reused,explicit_mp_precision=60)
                write(original_path.with_suffix(".json"),dict(checks=checks,failed_checks=[item for item in checks if not item["passed"]],
                    sha256=saved.digest(original_path),loop_path=str(loop_path),loop_sha256=saved.digest(loop_path),
                    original_history_control_newly_evaluated=True))
            validate_packet(original_path)
            high,low,diagnostics=weighted(parameters,grouped,evaluators,scalar,weight)
            assert high.shape==low.shape==(4,6,98,4)
            assert np.isfinite(high).all() and np.isfinite(low).all()
            checks=[]
            for name,value in diagnostics.items():
                check(checks,name,value)
            check(checks,"source energy exchange",float(np.max(abs((high[:,:,0,:]+low[:,:,0,:])+
                (high[:,:,-1,:]+low[:,:,-1,:]))))/max(float(np.max(abs(high[:,:,0,:]+low[:,:,0,:]))),1e-300))
            atomic_npz(destination,high=high,low=low,theta=theta,weight=weight,node=json.dumps(node,sort_keys=True),
                groups=np.array(["-".join(group) for group in GROUPS]))
            metadata=dict(checks=checks,failed_checks=[item for item in checks if not item["passed"]],
                sha256=saved.digest(destination),loop_path=str(loop_path),loop_sha256=saved.digest(loop_path),
                original_event=str(original_path),original_event_sha256=saved.digest(original_path),
                mappings=mappings,infrared_tail_changed=False,physical_bank_changed=False,real_actions_reevaluated=True,
                new_virtual_integrals=int(not reused),seconds=time.monotonic()-started)
            write(destination.with_suffix(".json"),metadata)
            assert not metadata["failed_checks"]
            count+=1
            write(ROOT/"progress.json",dict(state="evaluating",last_tag=tag,last_event=event_common.event_key(node),
                saved_events=len(list((ROOT/"events").rglob("electron-*.npz"))),expected_events=180))
            print(json.dumps(dict(tag=tag,event=event_common.event_key(node),loop_reused=reused,
                seconds=time.monotonic()-started)),flush=True)
    write(ROOT/"progress.json",dict(state="events_complete",saved_events=180))
    print("All180 upper-edge matched original and repaired events complete.",flush=True)

def old_pilot():
    config=protocol()
    assert read(ROOT/"progress.json")["state"]=="events_complete"
    assert not (ROOT/"pilot/original.json").exists()
    checks,records=[],[]
    anchor,unused=source.context(source.START)
    for tag,node_index in (("anchor",0),("minus_half",35)):
        original,theta=source.context(source.START-config["offsets"][tag]/config["expansion_span"])
        paired=source.PairedHistory(original,anchor)
        data,parameters,weight,scalar,loop_path,exact=cached_event(tag,config["selected"][node_index],theta)
        high,low,diagnostics=weighted(parameters,paired,source.models(paired),scalar,weight)
        difference=source.precise_combine([(high,low),(data["high"],data["low"])],[1,-1])
        norm=norm_setup()
        errors=norm(difference[0]+difference[1])/np.maximum(norm(data["high"]+data["low"]),1e-300)
        for branch,component,column in np.ndindex(errors.shape):
            check(checks,f"{tag}:original event repeat:{branch}:{component}:{column}",errors[branch,component,column])
        for name,value in diagnostics.items():
            check(checks,tag+":"+name,value)
        atomic_npz(ROOT/f"pilot/{tag}-{node_index:02d}.npz",high=high,low=low)
        records.append(dict(tag=tag,node=exact,maximum_relative=float(errors.max())))
    write(ROOT/"pilot/original.json",dict(checks=checks,records=records,failed_checks=[row for row in checks if not row["passed"]]))
    assert all(row["passed"] for row in checks)
    print(json.dumps(records),flush=True)

if __name__=="__main__":
    import psutil
    psutil.Process().nice(psutil.NORMAL_PRIORITY_CLASS)
    parser=argparse.ArgumentParser()
    parser.add_argument("phase",choices=["prepare","evaluate","old-pilot"])
    parser.add_argument("--max-events",type=int,default=180)
    parser.add_argument("--seconds",type=float,default=9000)
    arguments=parser.parse_args()
    if arguments.phase=="prepare":
        prepare()
    elif arguments.phase=="old-pilot":
        old_pilot()
    else:
        evaluate(arguments.max_events,arguments.seconds)



