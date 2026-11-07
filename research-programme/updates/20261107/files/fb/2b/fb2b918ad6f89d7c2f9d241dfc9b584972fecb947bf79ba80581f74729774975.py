from split_stage180 import *


def rebuild(parameters,coefficient,weight,left,spectra,gas_values,norms,mean,digits):
    high = np.zeros((3,5,98,4))
    low = np.zeros_like(high)
    curve_high = np.zeros((3,3,98,4))
    curve_low = np.zeros_like(curve_high)
    unit_high = np.zeros((98,4))
    unit_low = np.zeros_like(unit_high)
    with mp.workdps(digits):
        primitive = source.physics.exact_born_left(parameters)
        norm0,norm1 = [mp.mpf(float(value)) for value in norms[:2]]
        mean_mp = mp.mpf(float(mean))
        moment_left = {0:primitive[0],1:primitive[1]/norm0,2:(primitive[0]-mean_mp*primitive[1])/norm1,97:primitive[2]}
        prefactor = -mp.mpf(float(weight))*mp.mpf(float(coefficient))
        recoil = mp.mpf(float(left[-1]))
        for row,history in np.ndindex(98,4):
            kernel = prefactor*(moment_left[row] if row in moment_left else mp.mpf(float(left[row])))
            unit = kernel*recoil
            unit_high[row,history] = float(unit)
            unit_low[row,history] = float(unit-mp.mpf(float(unit)))
            values = []
            for tag in range(5):
                photon_jump = mp.mpf(float(spectra[tag,1,history]))-mp.mpf(float(spectra[tag,0,history]))
                gas_jump = recoil*mp.mpf(float(gas_values[tag,history]))
                channels = [kernel*(photon_jump+gas_jump),kernel*photon_jump,kernel*gas_jump]
                values.append(channels)
                for channel,value in enumerate(channels):
                    high[channel,tag,row,history] = float(value)
                    low[channel,tag,row,history] = float(value-mp.mpf(float(value)))
            for channel in range(3):
                coarse = 10000*(values[1][channel]-2*values[0][channel]+values[2][channel])
                fine = 40000*(values[3][channel]-2*values[0][channel]+values[4][channel])
                for order,value in enumerate([coarse,fine,coarse-fine]):
                    curve_high[order,channel,row,history] = float(value)
                    curve_low[order,channel,row,history] = float(value-mp.mpf(float(value)))
    return high,low,curve_high,curve_low,unit_high,unit_low


def main():
    base.guard()
    mp.mp.dps = 60
    config = read(ROOT/'configuration.json')
    authenticated = authenticate()
    initial = read(ROOT/'results/status.json')
    assert len([row for row in initial['checks'] if not row['passed']])==3
    for filename,checksum in initial['input_hashes'].items():
        assert saved.digest(filename)==checksum,filename
    contexts = [source.context(source.START-config['offsets'][tag]/config['expansion_span'])[0] for tag in HISTORY_TAGS]
    bundle = base.HistoryGroup(contexts)
    model = source.physics.FastSplit(bundle,'difference')
    basis_path = source.ROOT/'results/preparation/basis.npz'
    with np.load(basis_path) as basis:
        mass,norms,mean = basis['mass'].copy(),basis['norms'].copy(),float(basis['mean'])
    factor = linear.cholesky(mass,lower=True)
    def whiten(values):
        photons = np.moveaxis(values[...,1:97,:],-2,-1)
        return linear.solve_triangular(factor,photons.reshape(-1,96).T,lower=True).T.reshape(photons.shape)
    def dot(first,second):
        return np.sum(whiten(first)*whiten(second),axis=-1)
    def length(values):
        return np.sqrt(np.maximum(dot(values,values),0))
    checks,compatibility = [],[]
    def identity(name,residual,scale,destination=checks):
        checked(destination,name,np.max(length(residual)/np.maximum(length(scale),1e-300)))
    precision_root = ROOT/'results/precision'
    curve_pairs,unit_pairs,original_units = [],[],[]
    gas_values = None
    event_rows = []
    paths = {ROOT/'results/status.json',ROOT/'results/decomposition-vectors.npz',ROOT/'results/native-gas-law.json',basis_path}
    for ordinal,node in enumerate(config['selected']):
        raw_path = event_path(node)
        with np.load(raw_path) as packet:
            parameters,weight = source.physics.parameters_and_weight(float(packet['theta']),json.loads(str(packet['node'])))
            assert weight==float(packet['weight'])
            coefficient = float(packet['coefficient'])
            gas_values = packet['gas_values'].copy()
            raw = packet['high']+packet['low']
            original_units.append((packet['unit_high'].copy(),packet['unit_low'].copy()))
        left,unused = model.born_jumps(parameters)
        frequencies = [parameters['lab_energy']/parameters['temperature'],parameters['hard']*parameters['hard_doppler']/parameters['temperature']]
        spectra = np.array([context.functions(np.array(frequencies))[...,1:] for context in contexts])
        destination = precision_root/'events'/saved.angle_label(node['cosine'])/f"electron-{node['electron_index']:02d}.npz"
        if destination.exists():
            with np.load(destination) as packet:
                assert str(packet['raw_sha256'])==saved.digest(raw_path)
                first = tuple(packet[key].copy() for key in ['high','low','curve_high','curve_low','unit_high','unit_low'])
                second = tuple(packet[key].copy() for key in ['high100','low100','curve_high100','curve_low100','unit_high100','unit_low100'])
        else:
            first = rebuild(parameters,coefficient,weight,left,spectra,gas_values,norms,mean,80)
            second = rebuild(parameters,coefficient,weight,left,spectra,gas_values,norms,mean,100)
            names = ['high','low','curve_high','curve_low','unit_high','unit_low']
            atomic_npz(destination,**dict(zip(names,first)),**{name+'100':value for name,value in zip(names,second)},
                raw_path=str(raw_path),raw_sha256=saved.digest(raw_path),spectral_inputs=spectra,gas_values=gas_values,
                inherited_test_left=left,recoil_over_temperature=float(left[-1]),coefficient=coefficient,weight=weight,
                frequencies=np.array(frequencies),node=json.dumps(node,sort_keys=True))
        for index,label in [(0,'source'),(2,'curvature'),(4,'unit')]:
            assert np.array_equal(first[index],second[index]) and np.array_equal(first[index+1],second[index+1]),(node,label)
        precise = first[0]+first[1]
        identity(saved.event_key(node)+':80/100 source agreement',second[0]+second[1]-precise,precise)
        identity(saved.event_key(node)+':old/new source representation',precise-raw,raw)
        identity(saved.event_key(node)+':source channels close',precise[1]+precise[2]-precise[0],precise[0])
        scale = np.maximum(np.maximum(abs(precise[...,0,:]),abs(precise[...,97,:])),1e-300)
        checked(checks,saved.event_key(node)+':separate energy gas exchange',np.max(abs(precise[...,0,:]+precise[...,97,:])/scale))
        reconstructed_energy = mean*norms[0]*precise[...,1,:]+norms[1]*precise[...,2,:]
        checked(checks,saved.event_key(node)+':precise photon energy coordinate',np.max(abs(reconstructed_energy-precise[...,0,:])/scale))
        curve_pairs.append((first[2],first[3]))
        unit_pairs.append((first[4],first[5]))
        event_rows.append(first[2]+first[3])
        paths.update([raw_path,destination,*[path for context in contexts for path in context.inputs]])
        if (ordinal+1)%6==0:
            saved.write_json(ROOT/'precision-progress.json',dict(state='rebuilding',saved_events=ordinal+1,pid=os.getpid()))
            print(json.dumps(dict(precision_events=ordinal+1,expected=36)),flush=True)
    def precise_sum(pairs,digits):
        shape = pairs[0][0].shape
        result = np.zeros(shape)
        with mp.workdps(digits):
            for index in np.ndindex(shape):
                result[index] = float(mp.fsum(mp.mpf(float(pair[0][index]))+mp.mpf(float(pair[1][index])) for pair in pairs))
        return result
    curves = precise_sum(curve_pairs,80)
    curves100 = precise_sum(curve_pairs,100)
    identity('80/100 accumulated curvature agreement',curves100-curves,curves)
    with np.load(ROOT/'results/decomposition-vectors.npz') as packet:
        raw_curves = packet['vectors'].copy()
        inherited = packet['inherited_vectors'].copy()
        gas_curvatures = packet['native_gas_curvature'].copy()
    unit_predictions = np.zeros((3,98,4))
    with mp.workdps(100):
        for row,history in np.ndindex(98,4):
            unit = mp.fsum(mp.mpf(float(pair[0][row,history]))+mp.mpf(float(pair[1][row,history])) for pair in original_units)
            values = [mp.mpf(float(value)) for value in gas_values[:,history]]
            coarse = 10000*(values[1]-2*values[0]+values[2])
            fine = 40000*(values[3]-2*values[0]+values[4])
            unit_predictions[:,row,history] = [float(unit*value) for value in [coarse,fine,coarse-fine]]
    representation_residual = inherited[:,2]-curves[:,0]
    for order,width in enumerate(['coarse','fine','discrepancy']):
        identity(width+':precise photon/gas closure',curves[order,1]+curves[order,2]-curves[order,0],curves[order,0])
        identity(width+':independent original unit-gas law',curves[order,2]-unit_predictions[order],curves[order,2])
        identity(width+':legacy combined compatibility',curves[order,0]-raw_curves[order,0],raw_curves[order,0],compatibility)
        identity(width+':legacy photon compatibility',curves[order,1]-raw_curves[order,1],raw_curves[order,1],compatibility)
        identity(width+':legacy gas compatibility',curves[order,2]-raw_curves[order,2],raw_curves[order,2],compatibility)
        full = inherited[order,0]+inherited[order,1]+curves[order,1]+curves[order,2]+inherited[order,3]+inherited[order,4]
        identity(width+':full saved matched closure including explicit representation residual',full+representation_residual[order]-inherited[order,7],inherited[order,7])
    shares = []
    for order,width in enumerate(['coarse','fine','discrepancy']):
        for reference_name,reference in [('anchor_history',inherited[order,2]),('matched',inherited[order,7])]:
            for term,values in [('photon',curves[order,1]),('gas',curves[order,2]),('representation_residual',representation_residual[order])]:
                for history in range(4):
                    shares.append(dict(width=width,reference=reference_name,term=term,history=history,
                        signed_share=float(dot(values,reference)[history]/max(dot(reference,reference)[history],1e-300)),
                        norm_ratio=float(length(values)[history]/max(length(reference)[history],1e-300)),norm=float(length(values)[history])))
    gas_law = []
    for history in range(4):
        gas_law.append(dict(history=history,model='heavy' if history<2 else 'cold',
            native_relative_curvature_change=float(abs(gas_curvatures[2,history])/abs(gas_curvatures[1,history])),
            precise_gas_relative_curvature_change=float(length(curves[2,2])[history]/length(curves[1,2])[history]),
            unit_prediction_relative_error=float(length(curves[2,2]-unit_predictions[2])[history]/length(curves[2,2])[history])))
    cancellation = np.array([(length(curves[order,1])+length(curves[order,2]))/np.maximum(length(inherited[order,2]),1e-300) for order in range(3)])
    atomic_npz(precision_root/'decomposition-vectors.npz',curves=curves,representation_residual=representation_residual,
        independent_original_unit_predictions=unit_predictions,inherited_vectors=inherited,event_curves=np.array(event_rows),cancellation_factor=cancellation)
    saved.write_json(precision_root/'projection-shares.json',shares)
    saved.write_json(precision_root/'native-gas-law.json',gas_law)
    saved.write_json(precision_root/'legacy-compatibility-checks.json',compatibility)
    for filename,checksum in initial['input_hashes'].items():
        assert saved.digest(filename)==checksum,filename
    for filename,checksum in authenticated.items():
        assert saved.digest(filename)==checksum,filename
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    protected = BRANCH.parent.parent/'formalization-workbench'
    modified = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>datetime.fromisoformat(STARTED).timestamp()]
    checked(checks,'Protected workbench recent mtime guard',len(modified),.5)
    paths.update(ROOT.glob('*.py'))
    paths.update([ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',ROOT/'configuration.json'])
    retained = [dict(row,packet='initial split') for row in initial['checks'] if not row['passed']]
    retained += [dict(row,packet='legacy compatibility') for row in compatibility if not row['passed']]
    status = dict(state='complete',stage=180,scope='shared-primitive Born arithmetic, explicit legacy residual retained',
        finished_utc=datetime.now(timezone.utc).isoformat(),checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
        initial_split_checks=initial['count'],initial_split_failed_checks=3,retained_failed_checks=retained,
        compatibility_failed_checks=sum(not row['passed'] for row in compatibility),
        input_hashes={str(path):saved.digest(path) for path in sorted(paths)},authenticated_parent_inputs=authenticated,
        protected_modified_file_count=len(modified),protected_check_scope=initial['protected_check_scope'],
        original_source_packets_replaced=False,original_predictions_replaced=False,identity_tolerance=1e-10,source_prediction_tolerance=.01,
        post_test_diagnostic=True,tolerances_changed=False,source_curve_changed=False,new_integrals=0,
        cancellation_factor=cancellation.tolist(),max_saved_combined_discrepancy_relative=float(np.max(length(representation_residual[2])/length(inherited[2,2]))))
    saved.write_json(precision_root/'status.json',status)
    assert status['all_checks_passed'],'Keep failures; do not relax tolerances'
    (precision_root/'COMPLETE').write_text('complete\n',encoding='utf-8')
    saved.write_json(ROOT/'precision-progress.json',dict(state='analysis_complete',saved_events=36))
    print(json.dumps(dict(checks=len(checks),passed=True,retained_failures=len(retained),gas_law=gas_law,
        max_legacy_relative=status['max_saved_combined_discrepancy_relative'],
        worst_column=[row for row in shares if row['width']=='discrepancy' and row['history']==1])),flush=True)


if __name__=='__main__':
    source.modest()
    main()
