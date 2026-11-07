import os
for variable in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime,timezone
import json
import hashlib
import argparse
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'anchor-operator-history-curvature-20261020'
PARENT_SHA = '33f2cceec3658852e58e4cf6aa4eb437392ec0f668c19a2f75046d743793e0ab'
STARTED = '2026-10-20T20:56:58+00:00'
sys.path.insert(0,str(PARENT))
import anchor_stage179 as previous
saved,source,np,mp = previous.saved,previous.source,previous.np,previous.mp
base = previous.previous
read,checked,atomic_npz = previous.read,previous.checked,previous.atomic_npz
import scipy.linalg as linear
HISTORY_TAGS = previous.HISTORY_TAGS
CHANNELS = ['combined','photon','gas']
TERMS = ['combined','photon','gas','closure_residual','unit_gas_prediction']


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


class ChannelHistory:
    def __init__(self,bundle,channel):
        assert channel in ['photon','gas','unit_gas']
        self.bundle,self.channel = bundle,channel
        self.basis,self.inputs = bundle.basis,bundle.inputs
        self.gas = ([0.]*len(bundle.gas) if channel=='photon' else
                    [1.]*len(bundle.gas) if channel=='unit_gas' else list(bundle.gas))

    def functions(self,frequency,chemical=False):
        values = self.bundle.functions(frequency,chemical).copy()
        if self.channel != 'photon':
            values[...,1:] = 0.
        return values

    def derivatives(self,frequency,chemical=False):
        values = self.bundle.derivatives(frequency,chemical).copy()
        if self.channel != 'photon':
            values[...,1:] = 0.
        return values


def prepare():
    assert not (ROOT/'configuration.json').exists()
    authenticated = authenticate()
    inherited = read(PARENT/'configuration.json')
    assert inherited['source_prediction_tolerance']==.01 and inherited['identity_tolerance']==1e-10
    config = dict(stage=180,started_utc=STARTED,parent_seal_sha256=PARENT_SHA,
        incoming_frequency=inherited['incoming_frequency'],selected=inherited['selected'],
        offsets=inherited['offsets'],expansion_span=inherited['expansion_span'],
        operator_tag='anchor',history_tags=HISTORY_TAGS,channels=CHANNELS,
        source_prediction_tolerance=.01,identity_tolerance=1e-10,post_test_diagnostic=True,
        separated_history_actions=360,combined_history_reproductions=180,unit_gas_actions=36,
        prior_bookmark_normalized_sha256={str(path):hashlib.sha256(path.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
            for path in [BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md']})
    assert len(config['selected'])==36
    saved.write_json(ROOT/'configuration.json',config)
    saved.write_json(ROOT/'authenticated-inputs.json',authenticated)
    saved.write_json(ROOT/'progress.json',dict(state='prepared',expected_packets=36))
    print(json.dumps(dict(prepared=True,authenticated_paths=len(authenticated))),flush=True)


def evaluate(limit):
    config = read(ROOT/'configuration.json')
    base.guard()
    mp.mp.dps = 60
    contexts = {tag:source.context(source.START-config['offsets'][tag]/config['expansion_span']) for tag in HISTORY_TAGS}
    histories = [contexts[tag][0] for tag in HISTORY_TAGS]
    anchor,theta = contexts['anchor']
    photon = [ChannelHistory(bundle,'photon') for bundle in histories]
    gas = [ChannelHistory(bundle,'gas') for bundle in histories]
    unit = ChannelHistory(anchor,'unit_gas')
    combined = base.HistoryGroup([*histories,*photon,*gas,unit])
    full = source.physics.FastSplit(combined,'difference')
    primitive = source.physics.StableMoments(combined)
    paths = {path for bundle in histories for path in bundle.inputs}
    checks = []
    gas_values = np.array([np.repeat(bundle.gas,2) for bundle in histories])
    for ordinal,node in enumerate(config['selected']):
        path = event_path(node)
        parent_path = previous.event_path(node)
        if not path.exists():
            if limit <= 0:
                saved.write_json(ROOT/'progress.json',dict(state='safe_restart',next_ordinal=ordinal))
                return
            with np.load(parent_path) as packet:
                assert float(packet['theta'])==theta and float(packet['operator_offset'])==0
                selected = json.loads(str(packet['node']))
                parameters,weight = source.physics.parameters_and_weight(theta,selected)
                assert float(packet['weight'])==weight
                coefficient = float(packet['coefficient'])
                loop_path = Path(str(packet['loop_path']))
                assert saved.digest(loop_path)==str(packet['loop_sha256'])
                identity = source.physics.event_owner.inherited.virtual_identity(parameters)
                assert json.loads(str(packet['operator_identity']))==identity
            loop = read(loop_path)
            assert loop['identity']==identity and loop['finite']
            with mp.workdps(60):
                vacuum = float(source.physics.weak.vacuum.finite_virtual_ratio(parameters['energy'],parameters['cosine'])
                    +source.physics.weak.vacuum.soft_constant(parameters['energy'],parameters['cosine']))
            assert coefficient==.5*(vacuum+loop['scalar'])
            high,low = base.action(parameters,combined,full,primitive,coefficient,weight)
            groups_high,groups_low = np.stack(np.split(high,16,axis=-1)),np.stack(np.split(low,16,axis=-1))
            atomic_npz(path,high=groups_high[:15].reshape(3,5,98,4),low=groups_low[:15].reshape(3,5,98,4),
                unit_high=groups_high[15],unit_low=groups_low[15],gas_values=gas_values,
                theta=theta,operator_offset=0.,operator_tag='anchor',channels=np.array(CHANNELS),history_tags=np.array(HISTORY_TAGS),
                weight=weight,coefficient=coefficient,node=json.dumps(selected,sort_keys=True),operator_identity=json.dumps(identity,sort_keys=True),
                parent_path=str(parent_path),parent_sha256=saved.digest(parent_path),
                loop_path=str(loop_path),loop_sha256=saved.digest(loop_path),finished_utc=datetime.now(timezone.utc).isoformat())
            limit -= 1
        with np.load(path) as packet:
            assert packet['high'].shape==packet['low'].shape==(3,5,98,4)
            assert list(packet['channels'])==CHANNELS and list(packet['history_tags'])==HISTORY_TAGS
            assert float(packet['theta'])==theta and str(packet['operator_tag'])=='anchor' and float(packet['operator_offset'])==0
            assert np.array_equal(packet['gas_values'],gas_values)
            assert np.isfinite(packet['high']).all() and np.isfinite(packet['low']).all()
            assert saved.digest(str(packet['parent_path']))==str(packet['parent_sha256'])
            assert saved.digest(str(packet['loop_path']))==str(packet['loop_sha256'])
            selected = json.loads(str(packet['node']))
            parameters,weight = source.physics.parameters_and_weight(theta,selected)
            assert float(packet['weight'])==weight
            assert json.loads(str(packet['operator_identity']))==source.physics.event_owner.inherited.virtual_identity(parameters)
            frequency = np.array([parameters['lab_energy']/theta,parameters['hard']*parameters['hard_doppler']/theta])
            assert all(np.max(abs(bundle.functions(frequency)[...,1:]))==0 for bundle in [*gas,unit])
            assert all(np.max(np.abs(bundle.gas))==0 for bundle in photon)
            paths.update([path,parent_path,Path(str(packet['loop_path']))])
        if (ordinal+1)%6==0:
            saved.write_json(ROOT/'progress.json',dict(state='channel_actions',saved_packets=ordinal+1,expected_packets=36,pid=os.getpid()))
            print(json.dumps(dict(saved_packets=ordinal+1,expected_packets=36)),flush=True)
    saved.write_json(ROOT/'results/evaluation-status.json',dict(state='complete',separated_history_actions=360,
        combined_history_reproductions=180,unit_gas_actions=36,inputs_channels_isolated=True,
        input_hashes={str(path):saved.digest(path) for path in sorted(paths)}))
    saved.write_json(ROOT/'progress.json',dict(state='channel_actions_complete',saved_packets=36))


def reconstruct(pairs,units,gas_values,digits):
    vectors = np.zeros((3,len(TERMS),98,4))
    event_vectors = np.zeros((36,len(TERMS),98,4))
    native_gas = np.zeros((3,4))
    with mp.workdps(digits):
        gas_curvatures = []
        for history in range(4):
            coarse = 10000*(mp.mpf(float(gas_values[1,history]))-2*mp.mpf(float(gas_values[0,history]))+mp.mpf(float(gas_values[2,history])))
            fine = 40000*(mp.mpf(float(gas_values[3,history]))-2*mp.mpf(float(gas_values[0,history]))+mp.mpf(float(gas_values[4,history])))
            gas_curvatures.append([coarse,fine,coarse-fine])
            native_gas[:,history] = [float(coarse),float(fine),float(coarse-fine)]
        for row,history in np.ndindex(98,4):
            contributions = [[] for unused in TERMS]
            for event,pair in enumerate(pairs):
                def value(channel,tag):
                    index = (channel,HISTORY_TAGS.index(tag),row,history)
                    return mp.mpf(float(pair[0][index]))+mp.mpf(float(pair[1][index]))
                widths = []
                unit = mp.mpf(float(units[event][0][row,history]))+mp.mpf(float(units[event][1][row,history]))
                for order,(positive,negative,inverse) in enumerate([('plus','minus',10000),('plus_half','minus_half',40000)]):
                    channels = [inverse*(value(channel,positive)-2*value(channel,'anchor')+value(channel,negative)) for channel in range(3)]
                    widths.append([*channels,channels[0]-channels[1]-channels[2],unit*gas_curvatures[history][order]])
                for term in range(len(TERMS)):
                    values = [widths[0][term],widths[1][term],widths[0][term]-widths[1][term]]
                    contributions[term].append(values)
                    event_vectors[event,term,row,history] = float(values[2])
            for term in range(len(TERMS)):
                for order in range(3):
                    vectors[order,term,row,history] = float(mp.fsum(values[order] for values in contributions[term]))
    return vectors,event_vectors,native_gas


def analyse():
    config = read(ROOT/'configuration.json')
    authenticated = authenticate()
    assert authenticated==read(ROOT/'authenticated-inputs.json')
    evaluation = read(ROOT/'results/evaluation-status.json')
    for filename,checksum in evaluation['input_hashes'].items():
        assert saved.digest(filename)==checksum,filename
        if not Path(filename).is_relative_to(ROOT):
            assert authenticated[filename]==checksum
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
    checks = []
    def identity(name,residual,scale):
        checked(checks,name,np.max(length(residual)/np.maximum(length(scale),1e-300)))
    pairs,units = [],[]
    paths = {basis_path,PARENT/'results/decomposition-vectors.npz',PARENT/'results/saved-baseline-controls.json'}
    bitwise = 0
    gas_values = None
    for node in config['selected']:
        path = event_path(node)
        paths.add(path)
        with np.load(path) as packet:
            pair = (packet['high'].copy(),packet['low'].copy())
            unit = (packet['unit_high'].copy(),packet['unit_low'].copy())
            current_gas = packet['gas_values'].copy()
            if gas_values is None:
                gas_values = current_gas
            assert np.array_equal(gas_values,current_gas)
        pairs.append(pair)
        units.append(unit)
        old_path = previous.event_path(node)
        old = saved.read_pair(old_path)
        paths.add(old_path)
        bitwise += sum(np.array_equal(pair[0][0,tag],old[0][tag]) and np.array_equal(pair[1][0,tag],old[1][tag]) for tag in range(5))
        values = pair[0]+pair[1]
        identity(saved.event_key(node)+':event photon plus gas closure',values[1]+values[2]-values[0],values[0])
        scale = np.maximum(np.maximum(abs(values[...,0,:]),abs(values[...,97,:])),1e-300)
        checked(checks,saved.event_key(node)+':energy gas exchange',np.max(abs(values[...,0,:]+values[...,97,:])/scale))
        moment = mean*norms[0]*values[...,1,:]+norms[1]*values[...,2,:]
        checked(checks,saved.event_key(node)+':photon energy coordinate',np.max(abs(moment-values[...,0,:])/scale))
        for part in unit:
            assert all(np.array_equal(part[:,0],part[:,column]) for column in range(1,4))
        identity(saved.event_key(node)+':unit gas amplitude law',
            values[2]-(unit[0]+unit[1])[None,:,:]*gas_values[:,None,:],values[2])
    checked(checks,'All180 combined-history high/low reproductions are bitwise',180-bitwise,.5)
    print('Reconstructing photon/gas curvature and unit-gas law at80 and100digits.',flush=True)
    vectors,event_vectors,native_gas = reconstruct(pairs,units,gas_values,80)
    higher,higher_events,higher_gas = reconstruct(pairs,units,gas_values,100)
    identity('80 versus100 digit component arithmetic',higher-vectors,vectors)
    identity('80 versus100 digit event arithmetic',higher_events-event_vectors,event_vectors)
    checked(checks,'80 versus100 digit native gas arithmetic',np.max(abs(higher_gas-native_gas))/max(np.max(abs(native_gas)),1e-300))
    with np.load(PARENT/'results/decomposition-vectors.npz') as packet:
        inherited = packet['vectors'].copy()
    identity('Reproduce all Stage179 anchor curvatures',vectors[:,0]-inherited[:,2],inherited[:,2])
    for order,label in enumerate(['coarse','fine','discrepancy']):
        identity(label+':photon plus gas equals saved combined',vectors[order,3],inherited[order,2])
        identity(label+':gas curvature equals unit kernel times native gas curvature',vectors[order,2]-vectors[order,4],vectors[order,2])
        identity(label+':explicit arithmetic residual closes',vectors[order,1]+vectors[order,2]+vectors[order,3]-vectors[order,0],vectors[order,0])
    full = np.stack([inherited[:,0],inherited[:,1],vectors[:,1],vectors[:,2],inherited[:,3],inherited[:,4]],axis=1)
    for order,label in enumerate(['coarse','fine','discrepancy']):
        identity(label+':split full matched response closes',sum(full[order])-inherited[order,7],inherited[order,7])
    shares = []
    for order,width in enumerate(['coarse','fine','discrepancy']):
        for label,reference in [('anchor_history',inherited[order,2]),('matched',inherited[order,7])]:
            for term in [1,2,3]:
                values = vectors[order,term]
                for history in range(4):
                    shares.append(dict(width=width,reference=label,term=TERMS[term],history=history,
                        signed_share=float(dot(values,reference)[history]/max(dot(reference,reference)[history],1e-300)),
                        norm_ratio=float(length(values)[history]/max(length(reference)[history],1e-300)),norm=float(length(values)[history])))
    gas_rows = []
    for history in range(4):
        gas_rows.append(dict(history=history,model='heavy' if history<2 else 'cold',
            anchor_gas_departure=float(gas_values[0,history]),coarse_curvature=float(native_gas[0,history]),
            fine_curvature=float(native_gas[1,history]),curvature_difference=float(native_gas[2,history]),
            native_relative_curvature_change=float(abs(native_gas[2,history])/max(abs(native_gas[1,history]),1e-300)),
            evaluated_gas_relative_curvature_change=float(length(vectors[2,2])[history]/max(length(vectors[1,2])[history],1e-300)),
            frozen_unit_prediction_relative_error=float(length(vectors[2,2]-vectors[2,4])[history]/max(length(vectors[2,2])[history],1e-300))))
    controls = read(PARENT/'results/saved-baseline-controls.json')
    assert all(row['passed']==(row['original_relative']<.01) for row in controls)
    cancellation = np.array([(length(vectors[order,1])+length(vectors[order,2]))/np.maximum(length(inherited[order,2]),1e-300) for order in range(3)])
    saved.write_json(ROOT/'results/projection-shares.json',shares)
    saved.write_json(ROOT/'results/native-gas-law.json',gas_rows)
    saved.write_json(ROOT/'results/saved-baseline-controls.json',controls)
    atomic_npz(ROOT/'results/decomposition-vectors.npz',vectors=vectors,event_vectors=event_vectors,
        terms=np.array(TERMS),orders=np.array(['coarse','fine','discrepancy']),inherited_vectors=inherited,
        full_split=full,gas_values=gas_values,native_gas_curvature=native_gas,cancellation_factor=cancellation)
    for filename,checksum in authenticated.items():
        assert saved.digest(filename)==checksum,filename
    for path in paths:
        if not path.is_relative_to(ROOT):
            assert saved.digest(path)==authenticated[str(path)],path
    code_paths = {*ROOT.glob('*.py'),ROOT/'configuration.json',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md'}
    for module in list(sys.modules.values()):
        filename = getattr(module,'__file__',None)
        if filename and Path(filename).suffix=='.py' and Path(filename).resolve().is_relative_to(BRANCH):
            path = Path(filename).resolve()
            code_paths.add(path)
            if not path.is_relative_to(ROOT):
                assert authenticated[str(path)]==saved.digest(path),path
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    protected = BRANCH.parent.parent/'formalization-workbench'
    modified = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>datetime.fromisoformat(STARTED).timestamp()]
    checked(checks,'Protected workbench recent mtime guard',len(modified),.5)
    hashes = dict(evaluation['input_hashes'])
    hashes.update({str(path):saved.digest(path) for path in sorted(paths|code_paths)})
    status = dict(state='complete',stage=180,finished_utc=datetime.now(timezone.utc).isoformat(),
        checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
        input_hashes=hashes,authenticated_parent_inputs=authenticated,bitwise_combined_reproductions=bitwise,
        separated_history_actions=360,combined_history_reproductions=180,unit_gas_actions=36,reused_anchor_loops=36,
        real_emission_integrations=0,new_loop_integrations=0,source_prediction_tolerance=.01,identity_tolerance=1e-10,
        operator_frozen_at_anchor=True,tolerances_changed=False,source_curve_changed=False,post_test_diagnostic=True,
        baseline_controls_reused=True,crossed_real_baseline_evaluated=False,interpolation_error_proved=False,
        new_node_matched_moving_curvature_gate_passed=all(row['passed'] for row in controls if row['branch']=='moving_history' and row['component']=='remainder'),
        cancellation_factor=cancellation.tolist(),protected_modified_file_count=len(modified),
        protected_check_scope='Mtime guard since '+STARTED+'; not a pre-turn content snapshot')
    saved.write_json(ROOT/'results/status.json',status)
    print(json.dumps(dict(checks=len(checks),all_passed=status['all_checks_passed'],bitwise=bitwise,
        failures=[row for row in checks if not row['passed']],gas_law=gas_rows,
        worst_column_shares=[row for row in shares if row['history']==1 and row['width']=='discrepancy'])),flush=True)
    assert status['all_checks_passed'],'Retain failures and investigate without changing tolerances'
    (ROOT/'results/COMPLETE').write_text('complete\n',encoding='utf-8')
    saved.write_json(ROOT/'progress.json',dict(state='analysis_complete',saved_packets=36))


if __name__=='__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','evaluate','analyse'])
    parser.add_argument('--max-new-events',type=int,default=36)
    args = parser.parse_args()
    if args.phase=='prepare':
        prepare()
    elif args.phase=='evaluate':
        evaluate(args.max_new_events)
    else:
        analyse()
