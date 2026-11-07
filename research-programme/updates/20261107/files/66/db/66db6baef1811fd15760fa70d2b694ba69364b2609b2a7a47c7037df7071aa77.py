from __future__ import annotations
import continue199 as base
from continue199 import *
import assess199 as assessment
from assess199 import predict_versions
from propagate199 import lagrange
MAIN=ROOT
MID=MAIN/'cold-side-midpoint'
MID_OFFSET=-.0125

def midpoint_protocol():
    config=read(MID/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(name)==value,name
    return config

def activate():
    base.ROOT=MID;base.OFFSET=MID_OFFSET;base.checked_protocol=midpoint_protocol
    assessment.ROOT=MID;assessment.OFFSET=MID_OFFSET;assessment.checked_protocol=midpoint_protocol
    assessment.predict_versions=lambda data:(data['high'],data['low'])

def prepare():
    assert not (MID/'configuration.json').exists()
    original=checked_protocol()
    failed=read(MAIN/'results/source-assessment.json')
    assert not failed['permission_to_propagate'] and len(failed['failed_checks'])==48
    direct=packet(MAIN/'results/target-panel.npz')
    pairs=[(direct['high'],direct['low'])]
    for tag in ('minus','minus_half','anchor'):
        pairs.append(predict_versions(packet(saved.ROOT/f'sources/{tag}.npz')))
    weights=[5/16,15/16,-5/16,1/16]
    predicted=saved.parts_sum(np.stack([weight*pair[0] for weight,pair in zip(weights,pairs)]),
        np.stack([weight*pair[1] for weight,pair in zip(weights,pairs)]))
    save(MID/'frozen/panel-prediction.npz',high=predicted[0],low=predicted[1],offset=MID_OFFSET)
    operator=packet(MAIN/'frozen/operator-prediction.npz')
    save(MID/'frozen/operator-prediction.npz',block=operator['block'],tangent=operator['tangent'],curvature=operator['curvature'],
        prediction=smooth.candidate(MID_OFFSET,operator))
    config=dict(original,stage='199-cold-side-attempt',offset=MID_OFFSET,target_fraction=.875-MID_OFFSET/original['expansion_span'],
        offsets=[-.015,-.01,-.005,0.],prediction_weights=weights,started_utc=datetime.now(timezone.utc).isoformat(),
        source_prediction_tolerance=.01,identity_tolerance=1e-10,
        protocol_hashes={str(MAIN/name):digest(MAIN/name) for name in ('continue199.py','assess199.py','midpoint199.py','COLD-SIDE-ATTEMPT.md')},
        prediction_hashes={str(path.relative_to(MID)):digest(path) for path in (MID/'frozen').glob('*.npz')},
        old_endpoint_is_now_training_input=True,new_midpoint_used_to_set_weights=False)
    inputs=read(MAIN/'inputs.json')
    for path in (MAIN/'results/target-panel.npz',MAIN/'results/source-assessment.json',MAIN/'results/post-test-diagnosis.json'):
        saved.register(inputs,path)
    write(MID/'configuration.json',config);write(MID/'inputs.json',inputs)
    write(MID/'frozen/evaluation-protocol.json',config['protocol_hashes'])
    write(MID/'progress.json',dict(state='midpoint_prediction_frozen',target=config['target_fraction']))
    print(json.dumps(dict(state='midpoint_prediction_frozen',offset=MID_OFFSET,weights=weights)),flush=True)

def run(seconds):
    activate()
    if not (MID/'collision/status.json').exists():base.collision()
    assert not read(MID/'collision/status.json')['failed_checks']
    for model in ('heavy','cold'):
        for grid in ('half','quarter'):base.extend(model,grid)
    base.events(seconds,252)
    if read(MID/'progress.json')['state']=='events_complete':assessment.main()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['prepare','run']);parser.add_argument('--seconds',type=float,default=6000)
    args=parser.parse_args()
    if args.action=='prepare':prepare()
    else:run(args.seconds)
