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
PARENT=BRANCH/"repaired-history-microscopic-source-20261021"
PARENT_SHA="4403ecfb136d3023dfb79d876e52d3a9197269e79ff47cd320ffa2186aa81786"
BANK=BRANCH/"upper-adjacent-frequency-temperature-test-20261020"
sys.path.insert(0,str(PARENT))
import source_stage190 as prior
np,mp,linear=prior.np,prior.mp,prior.linear
saved,read,write,check,packet=prior.saved,prior.read,prior.write,prior.check,prior.packet
source,event_common,crossed=prior.source,prior.event_common,prior.crossed
TAGS,GROUPS=prior.TAGS,prior.GROUPS
atomic_npz,curvature,norm_setup=prior.atomic_npz,prior.curvature,prior.norm_setup
repaired_bundle,weighted=prior.repaired_bundle,prior.weighted


def event_path(root,tag,node):
    return root/"events"/tag/event_common.angle_label(node["cosine"])/f"electron-{node['electron_index']:02d}.npz"


def protocol():
    config=read(ROOT/"configuration.json")
    for name,value in config["protocol_hashes"].items():
        assert saved.digest(ROOT/name)==value,name
    return config


def cached_event(tag,node,theta):
    path=event_path(BANK,tag,node)
    data=packet(path)
    exact=json.loads(str(data["node"]))
    assert event_common.event_key(exact)==event_common.event_key(node)
    assert exact["frequency"]==16.435070908264382 and float(data["theta"])==theta
    parameters,weight=source.physics.parameters_and_weight(theta,exact)
    assert weight==float(data["weight"])
    loop_path=Path(str(data["loop_path"]))
    loop=read(loop_path)
    assert loop["finite"] and loop["identity"]==source.physics.event_owner.inherited.virtual_identity(parameters)
    return data,parameters,weight,loop["scalar"],loop_path,exact


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
    config=read(BANK/"configuration.json")
    assert config["source_prediction_tolerance"]==.01 and config["identity_tolerance"]==1e-10
    parent_config=read(PARENT/"configuration.json")
    assert all(config[key]==parent_config[key] for key in ("offsets","theta0","expansion_span","start_fraction"))
    config.update(stage=191,parent_seal_sha256=PARENT_SHA,started_utc=datetime.now(timezone.utc).isoformat(),
        groups_repaired=GROUPS,source_scope="Two finite frequency nodes; repaired resolved photons/gas; fixed original infrared tail",
        parent_frequency=parent_config["incoming_frequency"],original_bank_changed=False,infrared_tail_changed=False,
        protocol_hashes={name:saved.digest(ROOT/name) for name in ("ACCEPTANCE.md","DERIVATION.md")},
        bookmark_hashes={str(path):saved.digest(path) for path in (BRANCH/"RESUME-CURRENT.md",BRANCH.parent/"CURRENT_LOCAL_RESUME.md")})
    write(ROOT/"configuration.json",config)
    checks,bank=[],{}
    for tag in TAGS:
        original,theta=source.context(source.START-config["offsets"][tag]/config["expansion_span"])
        bank[tag]=[]
        for node in config["selected"]:
            data,parameters,weight,scalar,loop_path,exact=cached_event(tag,node,theta)
            assert data["high"].shape==(2,6,98,4)
            bank[tag].append((data["high"],data["low"]))
            for path in (event_path(BANK,tag,node),loop_path):
                paths.setdefault(str(path),saved.digest(path))
        for path in original.inputs:
            paths.setdefault(str(path),saved.digest(path))
    frozen_path=BANK/"results/frozen/predictions.npz"
    frozen=packet(frozen_path)
    summed={tag:source.precise_combine(bank[tag],[1]*36) for tag in TAGS}
    predictions,derivatives=event_common.predictors(summed,config["delta_log_temperature"])
    position=list(frozen["groups"]).index("complete_sum")
    for label,pairs in (("",predictions),("derivative_",derivatives)):
        for ordinal,pair in enumerate(pairs):
            for component,key in enumerate(("high","low")):
                assert np.array_equal(pair[component],frozen[label+key][position,ordinal])
    check(checks,"Legacy Stage174 frozen predictions and derivatives bitwise reproduced",0)
    original_curvature=curvature(bank,80)
    atomic_npz(ROOT/"results/original-curvature.npz",vectors=original_curvature)
    for path in (BANK/"configuration.json",frozen_path):
        paths.setdefault(str(path),saved.digest(path))
    for module in list(sys.modules.values()):
        name=getattr(module,"__file__",None)
        if name and Path(name).suffix==".py":
            path=Path(name).resolve()
            if path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                paths.setdefault(str(path),saved.digest(path))
    write(ROOT/"results/weighting.json",dict(parameters_and_weight_source=inspect.getsource(source.physics.parameters_and_weight),
        function_path=inspect.getsourcefile(source.physics.parameters_and_weight),
        frequencies=[config["incoming_frequency"],config["parent_frequency"]],
        seed_weights=[config["selected"][0]["seed_weight"],parent_config["selected"][0]["seed_weight"]],
        packets_already_weighted=True,combination_coefficients=[1,1],full_population_integral=False))
    write(ROOT/"authenticated-inputs.json",paths)
    write(ROOT/"results/preparation.json",dict(checks=checks,failed_checks=[]))
    write(ROOT/"progress.json",dict(state="prepared",new_events=0))
    print(json.dumps(dict(state="prepared",inputs=len(paths),old_percent=(100*norm_setup()(original_curvature[2,0])/norm_setup()(original_curvature[1,0])).tolist())),flush=True)


def old_pilot():
    config=protocol()
    assert not (ROOT/"pilot/original.json").exists()
    original,theta=source.context(source.START)
    paired=source.PairedHistory(original,original)
    data,parameters,weight,scalar,loop_path,exact=cached_event("anchor",config["selected"][0],theta)
    began=time.monotonic()
    high,low,diagnostics=weighted(parameters,paired,source.models(paired),scalar,weight)
    difference=source.precise_combine([(high,low),(data["high"],data["low"])],[1,-1])
    norm=norm_setup()
    errors=norm(difference[0]+difference[1])/np.maximum(norm(data["high"]+data["low"]),1e-300)
    checks=[]
    for branch,component,column in np.ndindex(errors.shape):
        check(checks,f"original event replay:{branch}:{component}:{column}",errors[branch,component,column])
    for name,value in diagnostics.items():
        check(checks,name,value)
    atomic_npz(ROOT/"pilot/original.npz",high=high,low=low)
    write(ROOT/"pilot/original.json",dict(checks=checks,failed_checks=[row for row in checks if not row["passed"]],
          node=exact,loop_path=str(loop_path),seconds=time.monotonic()-began))
    assert all(row["passed"] for row in checks)
    write(ROOT/"progress.json",dict(state="original_pilot_passed"))
    print(json.dumps(dict(state="original_pilot_passed",max_relative=float(errors.max()),seconds=time.monotonic()-began)),flush=True)


def evaluate(max_events,seconds):
    config=protocol()
    assert not read(ROOT/"pilot/original.json")["failed_checks"]
    began=time.monotonic()
    completed=0
    for tag in TAGS:
        original,theta=source.context(source.START-config["offsets"][tag]/config["expansion_span"])
        bundles,mappings=[],[]
        for kind,grid in GROUPS:
            bundle,mapping=repaired_bundle(original,tag,kind,grid)
            bundles.append(bundle)
            mappings.append(dict(kind=kind,grid=grid,mapping=mapping))
        grouped=crossed.HistoryGroup(bundles)
        evaluators=source.models(grouped)
        for node in config["selected"]:
            destination=event_path(ROOT,tag,node)
            if destination.exists():
                metadata=read(destination.with_suffix(".json"))
                assert saved.digest(destination)==metadata["sha256"] and not metadata["failed_checks"]
                continue
            if completed>=max_events or time.monotonic()-began>=seconds:
                write(ROOT/"progress.json",dict(state="safe_restart",next_tag=tag,next_event=event_common.event_key(node),
                      saved_events=len(list((ROOT/"events").rglob("electron-*.npz"))),expected_events=180))
                print("Safe event boundary saved.",flush=True)
                return
            old,parameters,weight,scalar,loop_path,exact=cached_event(tag,node,theta)
            started=time.monotonic()
            high,low,diagnostics=weighted(parameters,grouped,evaluators,scalar,weight)
            assert high.shape==(4,6,98,4)
            checks=[]
            for name,value in diagnostics.items():
                check(checks,name,value)
            check(checks,"source energy exchange",float(np.max(abs((high[:,:,0,:]+low[:,:,0,:])+
                  (high[:,:,-1,:]+low[:,:,-1,:]))))/max(float(np.max(abs(high[:,:,0,:]+low[:,:,0,:]))),1e-300))
            atomic_npz(destination,high=high,low=low,theta=theta,weight=weight,node=json.dumps(exact,sort_keys=True),
                       groups=np.array(["-".join(group) for group in GROUPS]))
            metadata=dict(checks=checks,failed_checks=[row for row in checks if not row["passed"]],
                sha256=saved.digest(destination),loop_path=str(loop_path),loop_sha256=saved.digest(loop_path),
                original_event=str(event_path(BANK,tag,node)),original_event_sha256=saved.digest(event_path(BANK,tag,node)),
                mappings=mappings,infrared_tail_changed=False,physical_bank_changed=False,real_actions_reevaluated=True,
                new_virtual_integrals=0,seconds=time.monotonic()-started)
            write(destination.with_suffix(".json"),metadata)
            assert not metadata["failed_checks"]
            completed+=1
            write(ROOT/"progress.json",dict(state="evaluating",last_tag=tag,last_event=event_common.event_key(node),
                  saved_events=len(list((ROOT/"events").rglob("electron-*.npz"))),expected_events=180))
            print(json.dumps(dict(tag=tag,event=event_common.event_key(node),seconds=time.monotonic()-started)),flush=True)
    write(ROOT/"progress.json",dict(state="events_complete",saved_events=180))
    print("All180 neighbouring repaired-history events complete.",flush=True)


if __name__=="__main__":
    import psutil
    psutil.Process().nice(psutil.NORMAL_PRIORITY_CLASS)
    parser=argparse.ArgumentParser()
    parser.add_argument("phase",choices=["prepare","old-pilot","evaluate"])
    parser.add_argument("--max-events",type=int,default=180)
    parser.add_argument("--seconds",type=float,default=5400)
    arguments=parser.parse_args()
    if arguments.phase=="prepare":
        prepare()
    elif arguments.phase=="old-pilot":
        old_pilot()
    else:
        evaluate(arguments.max_events,arguments.seconds)
