from __future__ import annotations
import os
for variable in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[variable]="1"
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/"lower-edge-repaired-source-combination-20261022"
sys.path.insert(0,str(PARENT))
import source_stage195 as previous
source,event_common=previous.source,previous.event_common
read,write,saved=previous.read,previous.write,previous.saved

def coverage():
    assert not (ROOT/"coverage.json").exists()
    seal_path=PARENT/"results/stage-integrity.json"
    assert saved.digest(seal_path)=="b2be3f330f5b641ff59989413752c6c4355e71901e3925326afcb9bfe9ebb384"
    old_coverage_path=PARENT/"coverage.json"
    assert saved.digest(old_coverage_path)==read(seal_path)["file_hashes"]["coverage.json"]
    old_coverage=read(old_coverage_path)
    verified=0
    for row in old_coverage["rows"]:
        if row["frequency"]==19.694647474056552:
            for match in row["loop_matches"]:
                assert saved.digest(match["path"])==match["sha256"]
                verified+=1
    config=read(PARENT/"configuration.json")
    cache_roots=sorted(path for path in BRANCH.glob("*/virtual-cache") if path.is_dir())
    configurations=[]
    for path in sorted(BRANCH.glob("*/configuration.json")):
        data=read(path)
        if data.get("incoming_frequency") in (19.694647474056552,):
            configurations.append(str(path))
    rows=[]
    for frequency in (19.694647474056552,):
        for tag,offset in config["offsets"].items():
            bundle,theta=source.context(source.START-offset/config["expansion_span"])
            for node in event_common.nodes(theta,frequency):
                parameters,weight=source.physics.parameters_and_weight(theta,node)
                identity=source.physics.event_owner.inherited.virtual_identity(parameters)
                key=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
                matches=[]
                for folder in cache_roots:
                    path=folder/key[:2]/(key+".json")
                    if path.exists():
                        data=read(path)
                        assert data["identity"]==identity and data["finite"] and previous.np.isfinite(data["scalar"])
                        matches.append(dict(path=str(path),sha256=saved.digest(path)))
                rows.append(dict(frequency=frequency,tag=tag,theta=theta,node=node,weight=weight,identity=identity,
                    key=key,loop_matches=matches))
    counts=[dict(frequency=frequency,tag=tag,total=36,cached_loops=sum(bool(row["loop_matches"]) for row in rows
        if row["frequency"]==frequency and row["tag"]==tag)) for frequency in (19.694647474056552,)
        for tag in config["offsets"]]
    write(ROOT/"coverage.json",dict(scope="All immediate branch virtual-cache directories; immediate configuration.json incoming_frequency inventory. Not an exhaustive content search of arbitrary historical NPZ files.",
        cache_roots=list(map(str,cache_roots)),matching_single_frequency_configurations=configurations,rows=rows,counts=counts,
        previous_coverage_path=str(old_coverage_path),previous_coverage_sha256=saved.digest(old_coverage_path),
        previous_upper_edge_cached_matches_rehashed=verified,
        predictions_evaluated=False,original_bank_changed=False))
    print(json.dumps(dict(counts=counts,matching_single_frequency_configurations=configurations,cache_roots=len(cache_roots),previous_cached_matches_rehashed=verified)),flush=True)

if __name__=="__main__":
    coverage()



