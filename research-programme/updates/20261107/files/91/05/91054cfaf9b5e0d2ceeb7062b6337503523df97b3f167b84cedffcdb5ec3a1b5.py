from __future__ import annotations
import os
for variable in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[variable]="1"
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json, hashlib, time, argparse, copy
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/"precision-carried-gas-evolution-20261021"
PARENT_SHA="487aec12840dc7006ead840bd4ed3314756dfc7a8dd645408429df794877ee0c"
BANK=BRANCH/"upper-outer-frequency-temperature-test-20261020"
ISOLATION=BRANCH/"curvature-history-isolation-20261020"
sys.path.insert(0,str(PARENT))
import replay_stage189 as prior
sys.path.insert(0,str(ISOLATION))
import isolate_stage177 as isolation
sys.path.insert(0,str(BRANCH/"crossed-history-virtual-response-20261020"))
import cross_stage178 as crossed

np,mp,linear=prior.np,prior.mp,prior.linear
saved,read,write,check,packet=prior.saved,prior.read,prior.write,prior.check,prior.packet
source=isolation.source
event_common=isolation.saved
TAGS=["anchor","plus","minus","plus_half","minus_half"]
GROUPS=[("bank","half"),("bank","quarter"),("candidate","half"),("candidate","quarter")]


def atomic_npz(path,**values):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+".partial")
    with temporary.open("wb") as handle:
        np.savez_compressed(handle,**values)
    os.replace(temporary,path)


def old_path(tag,node):
    return BANK/"events"/tag/event_common.angle_label(node["cosine"])/f"electron-{node['electron_index']:02d}.npz"


def new_path(tag,node):
    return ROOT/"events"/tag/event_common.angle_label(node["cosine"])/f"electron-{node['electron_index']:02d}.npz"


def authenticate():
    path=PARENT/"results/stage-integrity.json"
    assert saved.digest(path)==PARENT_SHA
    parent=read(path)
    paths=dict(parent["consumed_and_immediate_rehashed"])
    paths.update({str(PARENT/name):value for name,value in parent["file_hashes"].items()})
    paths[str(path)]=PARENT_SHA
    for name,value in paths.items():
        assert saved.digest(name)==value,name
    return paths


def protocol():
    config=read(ROOT/"configuration.json")
    for name,value in config["protocol_hashes"].items():
        assert saved.digest(ROOT/name)==value
    return config


def curvature(bank,digits=80):
    branch_count=bank["anchor"][0][0].shape[0]
    result=np.zeros((3,branch_count,6,98,4))
    tags=["plus","anchor","minus","plus_half","minus_half"]
    weights=[[10000,-20000,10000,0,0],[0,-80000,0,40000,40000]]
    with mp.workdps(digits):
        for branch,row,column in np.ndindex(branch_count,98,4):
            components=[]
            for component in range(4):
                accum=[]
                for event in range(len(bank["anchor"])):
                    values=[mp.mpf(float(bank[tag][event][0][branch,component,row,column]))+
                            mp.mpf(float(bank[tag][event][1][branch,component,row,column])) for tag in tags]
                    coarse=mp.fsum(weight*value for weight,value in zip(weights[0],values))
                    fine=mp.fsum(weight*value for weight,value in zip(weights[1],values))
                    accum.append((coarse,fine,coarse-fine))
                components.append([mp.fsum(value[index] for value in accum) for index in range(3)])
            components.extend([[mp.fsum(components[index][order] for index in members) for order in range(3)]
                               for members in ([1,2,3],[0,1,2,3])])
            for component in range(6):
                for order in range(3):
                    result[order,branch,component,row,column]=float(components[component][order])
    return result


def norm_setup():
    mass=packet(source.ROOT/"results/preparation/basis.npz")["mass"]
    factor=linear.cholesky(mass,lower=True)
    def norm(values):
        photons=np.moveaxis(values[...,1:97,:],-2,-1)
        flat=photons.reshape(-1,96)
        whitened=linear.solve_triangular(factor,flat.T,lower=True).T
        return np.linalg.norm(whitened,axis=-1).reshape(photons.shape[:-1])
    return norm


def prepare():
    assert not (ROOT/"configuration.json").exists()
    paths=authenticate()
    config=read(BANK/"configuration.json")
    assert config["source_prediction_tolerance"]==.01 and config["identity_tolerance"]==1e-10
    config.update(stage=190,parent_seal_sha256=PARENT_SHA,started_utc=datetime.now(timezone.utc).isoformat(),
        groups_repaired=GROUPS,source_scope="Complete saved finite node; resolved photons/gas repaired; original infrared tail held fixed",
        protocol_hashes={name:saved.digest(ROOT/name) for name in ["ACCEPTANCE.md","DERIVATION.md"]},
        bookmark_hashes={str(path):saved.digest(path) for path in [BRANCH/"RESUME-CURRENT.md",BRANCH.parent/"CURRENT_LOCAL_RESUME.md"]})
    write(ROOT/"configuration.json",config)
    bank={}
    for tag in TAGS:
        pairs=[]
        for node in config["selected"]:
            path=old_path(tag,node)
            data=packet(path)
            assert data["high"].shape==(2,6,98,4)
            pairs.append((data["high"],data["low"]))
            for item in [path,Path(str(data["loop_path"]))]:
                paths.setdefault(str(item),saved.digest(item))
        bank[tag]=pairs
    old_vectors=curvature(bank,80)
    authoritative=packet(ISOLATION/"results/diagnostic-vectors.npz")["exact_reconstruction"]
    assert np.array_equal(old_vectors,authoritative)
    norm=norm_setup()
    ratios=norm(old_vectors[2])/norm(old_vectors[1])
    check_rows=[]
    check(check_rows,"Stage177 original curvature reproduced bitwise",0)
    expected=max(row["relative"] for row in read(PARENT/"results/saved-baseline-controls.json")
                 if row["branch"]=="moving_history" and row["component"]=="remainder")
    check(check_rows,"old complete-node MTS remainder reproduced",float(ratios[0,4].max())-expected)
    atomic_npz(ROOT/"results/original-curvature.npz",vectors=old_vectors,ratios=ratios)
    paths.setdefault(str(ISOLATION/"results/diagnostic-vectors.npz"),saved.digest(ISOLATION/"results/diagnostic-vectors.npz"))
    for tag in TAGS:
        bundle,theta=source.context(source.START-config["offsets"][tag]/config["expansion_span"])
        for path in bundle.inputs:
            paths.setdefault(str(path),saved.digest(path))
    for module in list(sys.modules.values()):
        name=getattr(module,"__file__",None)
        if name and Path(name).suffix==".py" and Path(name).resolve().is_relative_to(BRANCH):
            path=Path(name).resolve()
            if not path.is_relative_to(ROOT):
                paths.setdefault(str(path),saved.digest(path))
    write(ROOT/"authenticated-inputs.json",paths)
    write(ROOT/"results/preparation.json",dict(checks=check_rows,failed_checks=[row for row in check_rows if not row["passed"]],
        old_baseline=float(ratios[0,0].max()),old_remainder=float(ratios[0,4].max()),old_total=float(ratios[0,5].max())))
    assert all(row["passed"] for row in check_rows)
    write(ROOT/"progress.json",dict(state="prepared",new_events=0))
    print(json.dumps(dict(state="prepared",old_ratios=ratios[0,[0,4,5]].tolist(),inputs=len(paths))),flush=True)


def repaired_bundle(original,tag,kind,grid):
    bundle=copy.deepcopy(original)
    epoch=bundle.epochs[0]
    index=TAGS.index(tag)
    mappings=[]
    new_values=[]
    for model_index,model in enumerate(prior.MODELS):
        path=prior.directory(model,kind,grid)/"probes-precision80.json"
        row=read(path)["records"][index]
        coordinate=row["geometry"]["target"]
        assert abs(coordinate-epoch.coordinate)<=1e-13
        state=row["partial"]
        profile=np.array([float(value) for value in state["profile"]])
        gas=float(state["gas"])
        epoch.original[model]=profile
        epoch.gas[model_index]=gas
        frequency,slope=epoch.tails[model]
        for lower,upper in ((1e-4,2e-4),(5e-5,1e-4)):
            phi=np.zeros(len(epoch.frequency))
            low_mask=epoch.frequency<upper
            low_phi=np.interp(np.log(epoch.frequency[low_mask]),np.log(frequency),slope)*epoch.frequency[low_mask]
            high_mask=epoch.frequency>lower
            phi[high_mask]=epoch.basis.evaluate(epoch.frequency[high_mask])@profile
            phase=np.clip((epoch.frequency[low_mask]-lower)/(upper-lower),0,1)
            blend=phase**3*(10-15*phase+6*phase**2)
            phi[low_mask]=(1-blend)*low_phi+blend*phi[low_mask]
            new_values.append(phi)
        mappings.append(dict(model=model,probe_path=str(path),coordinate=coordinate,
                             source_coordinate=epoch.coordinate,gas_input=state["gas"],gas_api=gas,
                             infrared_tail_changed=False))
    from scipy.interpolate import CubicSpline
    epoch.values=np.column_stack(new_values)
    epoch.spline=CubicSpline(np.log(epoch.frequency),epoch.values,axis=0,extrapolate=False)
    epoch.derivative_spline=epoch.spline.derivative()
    bundle.gas=list(epoch.gas)
    bundle.inputs=list(dict.fromkeys([*bundle.inputs,*[Path(row["probe_path"]) for row in mappings]]))
    return bundle,mappings


def cached_event(tag,node,theta):
    data=packet(old_path(tag,node))
    exact_node=json.loads(str(data["node"]))
    assert event_common.event_key(exact_node)==event_common.event_key(node)
    assert float(data["theta"])==theta
    parameters,weight=source.physics.parameters_and_weight(theta,exact_node)
    assert weight==float(data["weight"])
    loop_path=Path(str(data["loop_path"]))
    loop=read(loop_path)
    assert loop["finite"] and loop["identity"]==source.physics.event_owner.inherited.virtual_identity(parameters)
    return data,parameters,weight,loop["scalar"],loop_path,exact_node


def weighted(parameters,bundle,evaluators,scalar,weight):
    mp.mp.dps=60
    high,low,diagnostics=source.evaluate(parameters,bundle,evaluators,scalar)
    assert high.shape[-1]%4==0
    groups=high.shape[-1]//4
    high=np.moveaxis(high.reshape(6,98,groups,4),2,0)
    low=np.moveaxis(low.reshape(6,98,groups,4),2,0)
    high,low=source.precise_combine([(high,low)],[-weight])
    assert np.isfinite(high).all() and np.isfinite(low).all()
    return high,low,diagnostics


def old_pilot():
    config=protocol()
    assert not (ROOT/"pilot/original.json").exists()
    original,theta=source.context(source.START)
    paired=source.PairedHistory(original,original)
    node=config["selected"][0]
    data,parameters,weight,scalar,loop_path,exact_node=cached_event("anchor",node,theta)
    began=time.monotonic()
    high,low,diagnostics=weighted(parameters,paired,source.models(paired),scalar,weight)
    norm=norm_setup()
    difference=source.precise_combine([(high,low),(data["high"],data["low"])],[1,-1])
    errors=norm(difference[0]+difference[1])/np.maximum(norm(data["high"]+data["low"]),1e-300)
    checks=[]
    for branch,component,column in np.ndindex(errors.shape):
        check(checks,f"original event replay:{branch}:{component}:{column}",errors[branch,component,column])
    for name,value in diagnostics.items():
        check(checks,name,value)
    atomic_npz(ROOT/"pilot/original.npz",high=high,low=low)
    write(ROOT/"pilot/original.json",dict(checks=checks,failed_checks=[row for row in checks if not row["passed"]],
          seconds=time.monotonic()-began,node=exact_node,loop_path=str(loop_path)))
    assert all(row["passed"] for row in checks)
    write(ROOT/"progress.json",dict(state="original_pilot_passed"))
    print(json.dumps(dict(state="original_pilot_passed",seconds=time.monotonic()-began,max_relative=float(errors.max()))),flush=True)


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
            destination=new_path(tag,node)
            if destination.exists():
                metadata=read(destination.with_suffix(".json"))
                assert saved.digest(destination)==metadata["sha256"] and not metadata["failed_checks"]
                continue
            if completed>=max_events or time.monotonic()-began>=seconds:
                write(ROOT/"progress.json",dict(state="safe_restart",next_tag=tag,next_event=event_common.event_key(node),
                      saved_events=len(list((ROOT/"events").rglob("electron-*.npz"))),expected_events=180))
                print("Safe event boundary saved.",flush=True)
                return
            old,parameters,weight,scalar,loop_path,exact_node=cached_event(tag,node,theta)
            started=time.monotonic()
            high,low,diagnostics=weighted(parameters,grouped,evaluators,scalar,weight)
            assert high.shape==(4,6,98,4)
            checks=[]
            for name,value in diagnostics.items():
                check(checks,name,value)
            check(checks,"source energy exchange",float(np.max(abs((high[:,:,0,:]+low[:,:,0,:])+
                 (high[:,:,-1,:]+low[:,:,-1,:]))))/max(float(np.max(abs(high[:,:,0,:]+low[:,:,0,:]))),1e-300))
            atomic_npz(destination,high=high,low=low,theta=theta,weight=weight,node=json.dumps(exact_node,sort_keys=True),
                       groups=np.array([kind+"-"+grid for kind,grid in GROUPS]))
            metadata=dict(checks=checks,failed_checks=[row for row in checks if not row["passed"]],
                sha256=saved.digest(destination),loop_path=str(loop_path),loop_sha256=saved.digest(loop_path),
                original_event=str(old_path(tag,node)),original_event_sha256=saved.digest(old_path(tag,node)),
                mappings=mappings,infrared_tail_changed=False,physical_bank_changed=False,real_actions_reevaluated=True,
                new_virtual_integrals=0,seconds=time.monotonic()-started)
            write(destination.with_suffix(".json"),metadata)
            assert not metadata["failed_checks"]
            completed+=1
            write(ROOT/"progress.json",dict(state="evaluating",last_tag=tag,last_event=event_common.event_key(node),
                  saved_events=len(list((ROOT/"events").rglob("electron-*.npz"))),expected_events=180))
            print(json.dumps(dict(tag=tag,event=event_common.event_key(node),seconds=time.monotonic()-started)),flush=True)
    write(ROOT/"progress.json",dict(state="events_complete",saved_events=180))
    print("All180 repaired-history source events complete.",flush=True)


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
