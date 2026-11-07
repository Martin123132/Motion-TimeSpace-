import os
for variable in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json
import hashlib
import argparse
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'crossed-history-virtual-response-20261020'
PARENT_SHA = '629a51ffe843b49fc0c2b0bbf31259efbc638376359328112e4f1395ac67ceed'
STARTED = '2026-10-20T19:58:04+00:00'
sys.path.insert(0,str(PARENT))
import cross_stage178 as previous
saved, source, np, mp = previous.saved, previous.source, previous.np, previous.mp
import scipy.linalg as linear
BANK = previous.BANK
HISTORY_TAGS = ['anchor','plus','minus','plus_half','minus_half']
TERMS = ['fixed_virtual','mixed_virtual','anchor_history_curvature','average_operator_change',
         'nonvirtual_matched','virtual_moving','transmitted_history_curvature','matched_moving']
read, checked, atomic_npz = previous.read, previous.checked, previous.atomic_npz


def authenticate():
    seal = PARENT/'results/stage-integrity.json'
    assert saved.digest(seal) == PARENT_SHA
    parent = read(seal)
    paths = {str(PARENT/name):checksum for name,checksum in parent['file_hashes'].items()}
    paths.update(parent['consumed_and_immediate_rehashed'])
    paths[str(seal)] = PARENT_SHA
    for filename,checksum in paths.items():
        assert saved.digest(filename) == checksum,filename
    return paths


def event_path(node):
    return ROOT/'events'/saved.angle_label(node['cosine'])/f"electron-{node['electron_index']:02d}.npz"


def prepare():
    assert not (ROOT/'configuration.json').exists()
    authenticated = authenticate()
    inherited = read(PARENT/'configuration.json')
    assert inherited['source_prediction_tolerance'] == .01 and inherited['identity_tolerance'] == 1e-10
    config = dict(stage=179,started_utc=STARTED,parent_seal_sha256=PARENT_SHA,
        incoming_frequency=inherited['incoming_frequency'],selected=inherited['selected'],
        offsets=inherited['offsets'],expansion_span=inherited['expansion_span'],
        operator_tag='anchor',history_tags=HISTORY_TAGS,source_prediction_tolerance=.01,identity_tolerance=1e-10,
        post_test_diagnostic=True,new_history_actions=144,anchor_reproductions=36,
        real_emission_integrations=0,new_loop_integrations=0,
        prior_bookmark_normalized_sha256={str(path):hashlib.sha256(path.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
            for path in [BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md']})
    assert len(config['selected']) == 36
    saved.write_json(ROOT/'configuration.json',config)
    saved.write_json(ROOT/'authenticated-inputs.json',authenticated)
    saved.write_json(ROOT/'progress.json',dict(state='prepared',expected_packets=36))
    print(json.dumps(dict(prepared=True,authenticated_paths=len(authenticated),new_history_actions=144)),flush=True)


def evaluate(limit):
    config = read(ROOT/'configuration.json')
    previous.guard()
    mp.mp.dps = 60
    contexts = {tag:source.context(source.START-config['offsets'][tag]/config['expansion_span']) for tag in HISTORY_TAGS}
    anchor, theta = contexts['anchor']
    histories = [contexts[tag][0] for tag in HISTORY_TAGS]
    combined = previous.HistoryGroup(histories)
    full = source.physics.FastSplit(combined,'difference')
    primitive = source.physics.StableMoments(combined)
    checks, paths = [], {path for bundle in histories for path in bundle.inputs}
    for tag,bundle in zip(HISTORY_TAGS,histories):
        assert bundle.basis.mean == anchor.basis.mean
        assert np.array_equal(bundle.basis.norms,anchor.basis.norms)
    for ordinal,selected in enumerate(config['selected']):
        path = event_path(selected)
        if not path.exists():
            if limit <= 0:
                saved.write_json(ROOT/'progress.json',dict(state='safe_restart',next_ordinal=ordinal))
                return
            original = previous.old_path('anchor',selected)
            with np.load(original) as packet:
                node = json.loads(str(packet['node']))
                assert float(packet['theta']) == theta and float(packet['offset']) == 0
                loop_path = Path(str(packet['loop_path']))
                weight_expected = float(packet['weight'])
            parameters,weight = source.physics.parameters_and_weight(theta,node)
            assert weight == weight_expected
            loop = read(loop_path)
            identity = source.physics.event_owner.inherited.virtual_identity(parameters)
            assert loop['identity'] == identity and loop['finite']
            with mp.workdps(60):
                vacuum = float(source.physics.weak.vacuum.finite_virtual_ratio(parameters['energy'],parameters['cosine'])
                    +source.physics.weak.vacuum.soft_constant(parameters['energy'],parameters['cosine']))
            coefficient = .5*(vacuum+loop['scalar'])
            high,low = previous.action(parameters,combined,full,primitive,coefficient,weight)
            atomic_npz(path,high=np.stack(np.split(high,5,axis=-1)),low=np.stack(np.split(low,5,axis=-1)),
                theta=theta,operator_tag='anchor',operator_offset=0.,history_tags=np.array(HISTORY_TAGS),
                weight=weight,coefficient=coefficient,node=json.dumps(node,sort_keys=True),
                operator_identity=json.dumps(identity,sort_keys=True),
                original_path=str(original),original_sha256=saved.digest(original),
                loop_path=str(loop_path),loop_sha256=saved.digest(loop_path),
                finished_utc=datetime.now(timezone.utc).isoformat())
            limit -= 1
        with np.load(path) as packet:
            assert float(packet['theta']) == theta and float(packet['operator_offset']) == 0
            assert str(packet['operator_tag']) == 'anchor' and list(packet['history_tags']) == HISTORY_TAGS
            assert packet['high'].shape == packet['low'].shape == (5,98,4)
            assert np.isfinite(packet['high']).all() and np.isfinite(packet['low']).all()
            original = Path(str(packet['original_path']))
            loop_path = Path(str(packet['loop_path']))
            assert saved.digest(original) == str(packet['original_sha256'])
            assert saved.digest(loop_path) == str(packet['loop_sha256'])
            with np.load(original) as original_packet:
                assert str(packet['node']) == str(original_packet['node'])
                assert float(packet['weight']) == float(original_packet['weight'])
                parameters,unused_weight = source.physics.parameters_and_weight(theta,json.loads(str(packet['node'])))
                assert json.loads(str(packet['operator_identity'])) == source.physics.event_owner.inherited.virtual_identity(parameters)
            paths.update([path,original,loop_path])
        if (ordinal+1) % 6 == 0:
            saved.write_json(ROOT/'progress.json',dict(state='anchor_actions',saved_packets=ordinal+1,new_history_actions=4*(ordinal+1),pid=os.getpid()))
            print(json.dumps(dict(saved_packets=ordinal+1,expected_packets=36)),flush=True)
    first_path = event_path(config['selected'][0])
    with np.load(first_path) as packet:
        parameters,weight = source.physics.parameters_and_weight(theta,json.loads(str(packet['node'])))
        coefficient = float(packet['coefficient'])
        for positive,negative in [('plus','minus'),('plus_half','minus_half')]:
            for label,coefficients in [('sum',[1,1]),('difference',[1,-1]),('zero',[0,0])]:
                history = previous.LinearHistory([contexts[positive][0],contexts[negative][0]],coefficients)
                test_full = source.physics.FastSplit(history,'difference')
                test_primitive = source.physics.StableMoments(history)
                direct = previous.action(parameters,history,test_full,test_primitive,coefficient,weight)
                indices = [HISTORY_TAGS.index(tag) for tag in [positive,negative]]
                expected = source.precise_combine([(packet['high'][index],packet['low'][index]) for index in indices],coefficients)
                residual = direct[0]+direct[1]-expected[0]-expected[1]
                scale = max(np.max(abs(direct[0])),np.max(abs(expected[0])),1e-300)
                checked(checks,positive+':anchor Born linearity:'+label,np.max(abs(residual))/scale)
                del test_full,test_primitive
    status = dict(state='complete',checks=checks,all_checks_passed=all(row['passed'] for row in checks),
        new_history_actions=144,anchor_reproductions=36,reused_anchor_loops=36,
        input_hashes={str(path):saved.digest(path) for path in sorted(paths)})
    saved.write_json(ROOT/'results/evaluation-status.json',status)
    assert status['all_checks_passed'],'Retain failures; no tolerance change'
    saved.write_json(ROOT/'progress.json',dict(state='anchor_actions_complete',saved_packets=36))


def reconstruct(bank,crosses,anchors,digits):
    result = np.zeros((3,len(TERMS),98,4))
    event_differences = np.zeros((36,len(TERMS),98,4))
    with mp.workdps(digits):
        for row,history in np.ndindex(98,4):
            contributions = [[] for unused in TERMS]
            for event in range(36):
                def old(tag,branch,component=2):
                    pair = bank[tag][event]
                    return mp.mpf(float(pair[0][branch,component,row,history]))+mp.mpf(float(pair[1][branch,component,row,history]))
                def crossed(tag):
                    pair = crosses[tag][event]
                    return mp.mpf(float(pair[0][2,row,history]))+mp.mpf(float(pair[1][2,row,history]))
                def anchored(tag):
                    pair = anchors[event]
                    index = HISTORY_TAGS.index(tag)
                    return mp.mpf(float(pair[0][index,row,history]))+mp.mpf(float(pair[1][index,row,history]))
                widths = []
                for positive,negative,inverse in [('plus','minus',10000),('plus_half','minus_half',40000)]:
                    direct_plus,direct_minus = old(positive,0),old(negative,0)
                    fixed_plus,fixed_minus = old(positive,1),old(negative,1)
                    cross_plus,cross_minus = crossed(positive),crossed(negative)
                    moving = inverse*(direct_plus-2*old('anchor',0)+direct_minus)
                    fixed = inverse*(fixed_plus-2*old('anchor',1)+fixed_minus)
                    mixed = inverse*(direct_plus-cross_plus-cross_minus+direct_minus)/2
                    transmitted = inverse*(direct_plus+cross_plus+cross_minus+direct_minus-2*fixed_plus-2*fixed_minus)/2
                    frozen = inverse*(anchored(positive)-2*anchored('anchor')+anchored(negative))
                    average_change = transmitted-frozen
                    nonvirtual = mp.fsum(inverse*(old(positive,0,component)-2*old('anchor',0,component)+old(negative,0,component)) for component in [1,3])
                    widths.append([fixed,mixed,frozen,average_change,nonvirtual,moving,transmitted,moving+nonvirtual])
                for term in range(len(TERMS)):
                    values = [widths[0][term],widths[1][term],widths[0][term]-widths[1][term]]
                    contributions[term].append(values)
                    event_differences[event,term,row,history] = float(values[2])
            for term in range(len(TERMS)):
                for order in range(3):
                    result[order,term,row,history] = float(mp.fsum(values[order] for values in contributions[term]))
    return result,event_differences


def analyse():
    config = read(ROOT/'configuration.json')
    authenticated = authenticate()
    assert authenticated == read(ROOT/'authenticated-inputs.json')
    evaluation = read(ROOT/'results/evaluation-status.json')
    assert evaluation['all_checks_passed']
    for filename,checksum in evaluation['input_hashes'].items():
        assert saved.digest(filename) == checksum,filename
        if not Path(filename).is_relative_to(ROOT):
            assert authenticated[filename] == checksum
    basis_path = source.ROOT/'results/preparation/basis.npz'
    with np.load(basis_path) as packet:
        mass,norms,mean = packet['mass'].copy(),packet['norms'].copy(),float(packet['mean'])
    factor = linear.cholesky(mass,lower=True)
    def whiten(values):
        photons = np.moveaxis(values[...,1:97,:],-2,-1)
        return linear.solve_triangular(factor,photons.reshape(-1,96).T,lower=True).T.reshape(photons.shape)
    def dot(first,second):
        return np.sum(whiten(first)*whiten(second),axis=-1)
    def length(values):
        return np.sqrt(np.maximum(dot(values,values),0))
    checks = list(evaluation['checks'])
    def identity(name,residual,scale):
        checked(checks,name,np.max(length(residual)/np.maximum(length(scale),1e-300)))
    bank,crosses,anchors = {},{},[]
    paths = {basis_path,PARENT/'results/decomposition-vectors.npz',PARENT/'results/saved-baseline-controls.json'}
    for tag in HISTORY_TAGS:
        bank[tag],crosses[tag] = [],[]
        for node in config['selected']:
            path = previous.old_path(tag,node)
            paths.add(path)
            bank[tag].append(saved.read_pair(path))
            if tag != 'anchor':
                path = previous.new_path(tag,node)
                paths.add(path)
                crosses[tag].append(saved.read_pair(path))
    exact_reproductions = 0
    for event,node in enumerate(config['selected']):
        path = event_path(node)
        paths.add(path)
        pair = saved.read_pair(path)
        anchors.append(pair)
        old = bank['anchor'][event]
        identity(saved.event_key(node)+':saved anchor reproduction',
            pair[0][0]+pair[1][0]-old[0][0,2]-old[1][0,2],old[0][0,2]+old[1][0,2])
        bitwise = np.array_equal(pair[0][0],old[0][0,2]) and np.array_equal(pair[1][0],old[1][0,2])
        exact_reproductions += int(bitwise)
        values = pair[0]+pair[1]
        scale = np.maximum(np.maximum(abs(values[:,0]),abs(values[:,97])),1e-300)
        checked(checks,saved.event_key(node)+':energy gas exchange',np.max(abs(values[:,0]+values[:,97])/scale))
        moment = mean*norms[0]*values[:,1]+norms[1]*values[:,2]
        checked(checks,saved.event_key(node)+':photon energy coordinate',np.max(abs(moment-values[:,0])/scale))
    checked(checks,'Bitwise high/low anchor reproduction',36-exact_reproductions,.5)
    print('Reconstructing anchored and inherited finite-width terms at80 and100digits.',flush=True)
    vectors,event_vectors = reconstruct(bank,crosses,anchors,80)
    higher,higher_events = reconstruct(bank,crosses,anchors,100)
    identity('80 versus100 digit whole decomposition',higher-vectors,vectors)
    identity('80 versus100 digit event decomposition',higher_events-event_vectors,event_vectors)
    with np.load(PARENT/'results/decomposition-vectors.npz') as packet:
        inherited = packet['vectors'].copy()
        matched = packet['matched_discrepancy'].copy()
        old_nonvirtual = packet['nonvirtual_matched'].copy()
    for new_index,old_index in [(0,1),(1,2),(5,0),(6,3)]:
        identity('Reproduce inherited '+TERMS[new_index],vectors[:,new_index]-inherited[:,old_index],inherited[:,old_index])
    identity('Reproduce inherited matched discrepancy',vectors[2,7]-matched,matched)
    identity('Reproduce saved nonvirtual discrepancy',vectors[2,4]-old_nonvirtual,old_nonvirtual)
    for order,label in enumerate(['coarse','fine','discrepancy']):
        identity(label+':anchor plus average correction equals transmitted',vectors[order,2]+vectors[order,3]-vectors[order,6],vectors[order,6])
        identity(label+':all virtual terms close',sum(vectors[order,:4])-vectors[order,5],vectors[order,5])
        identity(label+':complete matched closure',sum(vectors[order,:5])-vectors[order,7],vectors[order,7])
    records = []
    for order,width in enumerate(['coarse','fine','discrepancy']):
        for reference_name,reference_index in [('transmitted_history_curvature',6),('moving_virtual',5),('moving_matched',7)]:
            reference = vectors[order,reference_index]
            denominator = np.maximum(dot(reference,reference),1e-300)
            for term in range(5):
                values = vectors[order,term]
                for history in range(4):
                    records.append(dict(width=width,reference=reference_name,term=TERMS[term],history=history,
                        signed_share=float(dot(values,reference)[history]/denominator[history]),
                        norm_ratio=float(length(values)[history]/max(length(reference)[history],1e-300)),
                        norm=float(length(values)[history]),reference_norm=float(length(reference)[history])))
    controls = read(PARENT/'results/saved-baseline-controls.json')
    for row in controls:
        assert row['passed'] == (row['original_relative'] < .01)
    cancellation = np.array([sum(length(piece) for piece in vectors[order,:5])/np.maximum(length(vectors[order,7]),1e-300) for order in range(3)])
    saved.write_json(ROOT/'results/projection-shares.json',records)
    saved.write_json(ROOT/'results/saved-baseline-controls.json',controls)
    atomic_npz(ROOT/'results/decomposition-vectors.npz',vectors=vectors,event_vectors=event_vectors,
        terms=np.array(TERMS),orders=np.array(['coarse','fine','discrepancy']),cancellation_factor=cancellation)
    for filename,checksum in authenticated.items():
        assert saved.digest(filename) == checksum,filename
    for path in paths:
        if not path.is_relative_to(ROOT):
            assert saved.digest(path) == authenticated[str(path)],path
    code_paths = {*ROOT.glob('*.py'),ROOT/'configuration.json',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md'}
    for module in list(sys.modules.values()):
        filename = getattr(module,'__file__',None)
        if filename and Path(filename).suffix == '.py' and Path(filename).resolve().is_relative_to(BRANCH):
            path = Path(filename).resolve()
            code_paths.add(path)
            if not path.is_relative_to(ROOT):
                assert authenticated[str(path)] == saved.digest(path),path
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    protected = BRANCH.parent.parent/'formalization-workbench'
    modified = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > datetime.fromisoformat(STARTED).timestamp()]
    checked(checks,'Protected workbench recent mtime guard',len(modified),.5)
    hashes = dict(evaluation['input_hashes'])
    hashes.update({str(path):saved.digest(path) for path in sorted(paths|code_paths)})
    gate_passed = all(row['passed'] for row in controls if row['branch']=='moving_history' and row['component']=='remainder')
    status = dict(state='complete',stage=179,finished_utc=datetime.now(timezone.utc).isoformat(),
        checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
        input_hashes=hashes,authenticated_parent_inputs=authenticated,
        new_history_actions=144,anchor_reproductions=36,bitwise_anchor_reproductions=exact_reproductions,
        reused_anchor_loops=36,reused_stencil_packets=180,reused_crossed_packets=144,
        real_emission_integrations=0,new_loop_integrations=0,source_prediction_tolerance=.01,identity_tolerance=1e-10,
        operator_frozen_at_anchor=True,tolerances_changed=False,source_curve_changed=False,post_test_diagnostic=True,
        baseline_controls_reused=True,crossed_real_baseline_evaluated=False,interpolation_error_proved=False,
        new_node_matched_moving_curvature_gate_passed=gate_passed,cancellation_factor=cancellation.tolist(),
        protected_modified_file_count=len(modified),
        protected_check_scope='Mtime guard since '+STARTED+'; not a pre-turn content snapshot')
    saved.write_json(ROOT/'results/status.json',status)
    assert status['all_checks_passed'],'Retain failures; no tolerance changes'
    (ROOT/'results/COMPLETE').write_text('complete\n',encoding='utf-8')
    saved.write_json(ROOT/'progress.json',dict(state='analysis_complete',saved_packets=36))
    print(json.dumps(dict(checks=len(checks),all_passed=True,bitwise_anchor_reproductions=exact_reproductions,
        worst_column_shares=[row for row in records if row['history']==1 and row['width']=='discrepancy'])),flush=True)


if __name__ == '__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','evaluate','analyse'])
    parser.add_argument('--max-new-events',type=int,default=36)
    args = parser.parse_args()
    if args.phase == 'prepare':
        prepare()
    elif args.phase == 'evaluate':
        evaluate(args.max_new_events)
    else:
        analyse()
